#!/usr/bin/env python3
"""incremental.py — build incrémental du site IMSV, par cache d'empreintes de contenu.

Principe. Chaque « produit » (PDF d'une séance, feuille de méthodes, deck de slides, site HTML d'une
vue…) a une EMPREINTE : le sha256 de TOUT ce dont il dépend (sources, filtres Lua, thème, script de
build, version de Quarto). Si l'empreinte est déjà dans le cache, le résultat est recopié ; sinon on
construit, puis on range le résultat dans le cache. Les dates de modification ne comptent pas : ça
marche donc dans les worktrees jetables de deploy.sh, et un fichier modifié puis remis à
l'identique ne coûte rien.

    python3 incremental.py assets                   PDF des séances, feuilles, méthodes (dans pdf/)
    python3 incremental.py site --view student|prof --dest DIR
                                                     assets + site HTML (Quarto) copié dans DIR
    python3 incremental.py slides --dest DIR         decks reveal.js + index, copiés dans DIR
    python3 incremental.py status | clean            contenu du cache / le vider

    --force (ou IMSV_FORCE=1)   ignore le cache en lecture : tout est reconstruit (et re-rangé).

Cache : <dépôt>/.deploy-cache/ (ignoré par git). Même dossier pour le dépôt et ses worktrees ;
variable IMSV_CACHE pour le changer, IMSV_CACHE_KEEP (défaut 4) = versions gardées par produit.

RÈGLE D'OR : une dépendance oubliée dans une empreinte = un résultat périmé publié. Si un build se
met à lire un nouveau fichier, il faut l'ajouter à l'empreinte du produit (fonctions assets(),
slides() et site() ci-dessous). En cas de doute : ./deploy.sh --force.
"""
from __future__ import annotations

import argparse
import filecmp
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ENGINE_VERSION = "1"   # à incrémenter si la logique des empreintes change (invalide tout le cache)
ROOT = Path(__file__).resolve().parent
KEEP = max(1, int(os.environ.get("IMSV_CACHE_KEEP", "4")))
SKIP_DIRS = {".git", ".quarto", "__pycache__", "_book", ".deploy-cache", "node_modules"}
STATS = {"cache": 0, "build": 0}


# --------------------------------------------------------------------------------------- affichage
def say(kind: str, label: str, dt: float | None = None) -> None:
    mark = "✓ cache" if kind == "cache" else "⚙ build"
    extra = f"  ({dt:.0f} s)" if dt is not None else ""
    print(f"  {mark}  {label}{extra}", flush=True)


def warn(msg: str) -> None:
    print(f"  ⚠ {msg}", file=sys.stderr, flush=True)


def die(msg: str) -> "None":
    print(f"✗ {msg}", file=sys.stderr, flush=True)
    sys.exit(1)


# ---------------------------------------------------------------------------------------- commandes
_QV: str | None = None


def quarto_version() -> str:
    global _QV
    if _QV is None:
        try:
            _QV = subprocess.run(["quarto", "--version"], capture_output=True, text=True,
                                 check=True).stdout.strip()
        except Exception:
            _QV = "quarto-inconnu"
    return _QV


def build_env() -> dict:
    env = dict(os.environ)
    env["IMSV_POSTRENDER"] = "1"   # le hook post-render ne doit pas relancer ce moteur
    return env


def run(cmd, cwd: Path, label: str, env: dict | None = None) -> float:
    """Lance une commande, sortie capturée ; en cas d'échec, affiche la fin du journal et quitte."""
    t0 = time.monotonic()
    with tempfile.TemporaryFile("w+", encoding="utf-8", errors="replace") as log:
        r = subprocess.run([str(c) for c in cmd], cwd=cwd, env=env, stdout=log,
                           stderr=subprocess.STDOUT)
        if r.returncode:
            log.seek(0)
            tail = log.read().splitlines()[-40:]
            print(f"\n✗ échec : {label}\n  commande : {' '.join(str(c) for c in cmd)}\n"
                  + "\n".join("    " + line for line in tail), file=sys.stderr, flush=True)
            sys.exit(r.returncode)
    return time.monotonic() - t0


# ------------------------------------------------------------------------------------- empreintes
class Key:
    """Empreinte cumulative : étiquettes, fichiers (nom relatif + taille + contenu), arbres."""

    def __init__(self, *tags):
        self.h = hashlib.sha256()
        self.tag("engine", ENGINE_VERSION, "quarto", quarto_version(), *tags)

    def tag(self, *items) -> None:
        for it in items:
            self.h.update(b"T" + str(it).encode() + b"\0")

    def file(self, path: Path, name: str | None = None) -> None:
        name = name or path.relative_to(ROOT).as_posix()
        if not path.is_file():
            self.h.update(b"M" + name.encode() + b"\0")   # absent : fait partie de l'empreinte
            return
        self.h.update(f"F{name}\0{path.stat().st_size}\0".encode())
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                self.h.update(chunk)

    def tree(self, base: Path, ignore=None) -> None:
        """Tous les fichiers sous base. ignore(rel) reçoit un chemin relatif à ROOT (« dossier/ »
        avec barre finale pour un dossier) ; True = exclu."""
        if not base.is_dir():
            self.tag("absent", base.relative_to(ROOT).as_posix())
            return
        for dp, dns, fns in os.walk(base):
            dpath = Path(dp)
            keep = []
            for d in sorted(dns):
                rel = (dpath / d).relative_to(ROOT).as_posix() + "/"
                if d in SKIP_DIRS or (ignore and ignore(rel)):
                    continue
                keep.append(d)
            dns[:] = keep
            for fn in sorted(fns):
                p = dpath / fn
                rel = p.relative_to(ROOT).as_posix()
                if ignore and ignore(rel):
                    continue
                self.file(p, rel)

    def digest(self) -> str:
        return self.h.hexdigest()[:32]


# ------------------------------------------------------------------------------------------ cache
def cache_root() -> Path:
    env = os.environ.get("IMSV_CACHE")
    if env:
        return Path(env).resolve()
    try:   # depuis un worktree, `git-common-dir` pointe vers le .git du dépôt principal
        out = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        common = (ROOT / out).resolve()
        if common.name == ".git":
            return common.parent / ".deploy-cache"
    except Exception:
        pass
    return ROOT / ".deploy-cache"


class Cache:
    def __init__(self, root: Path):
        self.root = root

    def lookup(self, name: str, key: str):
        """-> (dossier des fichiers, {chemin relatif: taille}) ou None."""
        if os.environ.get("IMSV_FORCE") == "1":
            return None
        e = self.root / name / key
        try:
            files = json.loads((e / "manifest.json").read_text())["files"]
            for rel, size in files.items():
                if (e / "files" / rel).stat().st_size != size:
                    raise ValueError(rel)
        except Exception:
            if e.exists():
                shutil.rmtree(e, ignore_errors=True)   # entrée incomplète ou corrompue : jetée
            return None
        try:
            os.utime(e, None)   # « utilisée récemment » : protège de l'élagage
        except OSError:
            pass
        return e / "files", files

    def store(self, name: str, key: str, base: Path, rels) -> None:
        parent = self.root / name
        parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix=".tmp-", dir=parent))
        try:
            sizes = {}
            for rel in rels:
                dst = tmp / "files" / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(base / rel, dst)
                sizes[rel] = dst.stat().st_size
            (tmp / "manifest.json").write_text(json.dumps({"files": sizes}))
            final = parent / key
            if final.exists():
                shutil.rmtree(final)
            os.rename(tmp, final)   # atomique : une entrée est complète ou n'existe pas
        except BaseException:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        self._prune(parent)

    @staticmethod
    def _prune(parent: Path) -> None:
        entries = [p for p in parent.iterdir() if p.is_dir() and not p.name.startswith(".tmp-")]
        entries.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        for p in entries[KEEP:]:
            shutil.rmtree(p, ignore_errors=True)
        for p in parent.glob(".tmp-*"):   # restes d'un build interrompu
            if time.time() - p.stat().st_mtime > 86400:
                shutil.rmtree(p, ignore_errors=True)


def restore(src_dir: Path, rels, dest: Path) -> None:
    """Copie les fichiers (chemins relatifs) de src_dir vers dest, sans toucher à ce qui est déjà
    identique."""
    for rel in rels:
        src, dst = src_dir / rel, dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_file() and filecmp.cmp(src, dst, shallow=False):
            continue
        shutil.copy2(src, dst)


def cached_unit(cache: Cache, name: str, label: str, key: str, *, build_base: Path,
                dest_base: Path, collect, build, on_hit=None) -> None:
    """Un produit : si `key` est en cache → recopie dans dest_base ; sinon build() puis rangement.
    collect() liste, après build, les fichiers produits (relatifs à build_base)."""
    hit = cache.lookup(name, key)
    if hit:
        files_dir, files = hit
        if on_hit:
            on_hit(set(files))
        restore(files_dir, list(files), dest_base)
        STATS["cache"] += 1
        say("cache", label)
        return
    dt = build()
    rels = collect()
    if not rels:
        die(f"{label} : le build n'a produit aucun fichier")
    cache.store(name, key, build_base, rels)
    if dest_base != build_base:
        restore(build_base, rels, dest_base)
    STATS["build"] += 1
    say("build", label, dt)


# ------------------------------------------------------------------------------------------ assets
def assets(cache: Cache, warn_orphans: bool = False) -> None:
    """PDF (+ hors-ligne) de chaque séance, feuilles de méthodes, méthodes remplies → pdf/."""
    env = build_env()
    pdf = ROOT / "pdf"
    pdf.mkdir(exist_ok=True)

    def pdf_files(prefix: str):
        return sorted(f"pdf/{p.name}" for p in pdf.glob(prefix + "*") if p.is_file())

    # --- 1) un jeu de PDF par séance en ligne (build-pdf.sh) --------------------------------------
    for d in sorted(p for p in (ROOT / "seances").glob("seance*") if p.is_dir()):
        s = d.name
        if not (d / "_pdf.qmd").is_file():
            continue
        k = Key("pdf", s)
        for f in sorted(d.glob("_*.qmd")):          # _pdf, _offline, _socle, _consignes…
            k.file(f)
        k.file(d / "_metadata.yml")                  # corrige-exos: false → pas de complet/offline
        for f in sorted((d / "img").glob("*.svg")):  # figures copiées par build-pdf.sh
            k.file(f)
        k.tree(ROOT / "img")                         # img/ racine, optionnel
        for rel in ("exercice.lua", "theme.scss", "_includes/aides.html", "build-pdf.sh"):
            k.file(ROOT / rel)

        def on_hit(keep, prefix=f"{s}-"):
            for p in pdf.glob(prefix + "*"):         # ex. complet/offline devenus masqués
                if f"pdf/{p.name}" not in keep and p.is_file():
                    p.unlink()

        cached_unit(cache, f"pdf-{s}", f"PDF {s}", k.digest(), build_base=ROOT, dest_base=ROOT,
                    collect=lambda s=s: pdf_files(f"{s}-"), on_hit=on_hit,
                    build=lambda s=s: run(["bash", "build-pdf.sh", s], ROOT, f"build-pdf.sh {s}", env))

    # --- 2) feuilles à compléter : une par séance en ligne + la vierge (build-methodes.sh) -------
    feuilles = sorted((ROOT / "seances").glob("feuille-seance*.qmd")) + [ROOT / "seances/feuille-vierge.qmd"]
    for q in feuilles:
        if not q.is_file():
            continue
        b = q.stem
        k = Key("feuille", b)
        k.file(q)
        k.file(ROOT / "feuille-auto.py")
        k.file(ROOT / "build-methodes.sh")
        m = re.fullmatch(r"feuille-seance(\d+)", b)
        if m:   # titres et objectifs lus dans les cartes de méthode de la séance
            for suf in (".qmd", ".qmd.off"):
                k.file(ROOT / f"seances/_methodes-seance{m.group(1)}{suf}")
        cached_unit(cache, f"feuille-{b}", f"feuille {b}", k.digest(), build_base=ROOT,
                    dest_base=ROOT,
                    collect=lambda b=b: [f"pdf/{b}.pdf"] if (pdf / f"{b}.pdf").is_file() else [],
                    build=lambda b=b: run(["bash", "build-methodes.sh", b], ROOT,
                                          f"build-methodes.sh {b}", env))

    # --- 3) méthodes « remplies », une par séance en ligne (build-boite.sh) -----------------------
    for page in sorted((ROOT / "seances/methodes").glob("seance*.qmd")):
        s = page.stem
        frag = ROOT / f"seances/_methodes-{s}.qmd"
        if not frag.is_file():
            warn(f"méthodes {s} : pas de fragment seances/_methodes-{s}.qmd, ignoré")
            continue
        k = Key("methodes", s)
        k.file(frag)
        k.file(ROOT / "methode.lua")
        k.tree(ROOT / "seances/methodes/img")
        k.file(ROOT / "build-boite.sh")
        cached_unit(cache, f"methodes-{s}", f"méthodes {s}", k.digest(), build_base=ROOT,
                    dest_base=ROOT,
                    collect=lambda s=s: [f"pdf/methodes-{s}.pdf"] if (pdf / f"methodes-{s}.pdf").is_file() else [],
                    build=lambda s=s: run(["bash", "build-boite.sh", s], ROOT,
                                          f"build-boite.sh {s}", env))

    if warn_orphans:
        warn_orphan_pdfs()


def warn_orphan_pdfs() -> None:
    """pdf/ est copié tel quel dans le site (resources) : un PDF d'une séance hors ligne, resté dans
    git, serait donc publié alors que la séance ne l'est pas."""
    active = {p.name for p in (ROOT / "seances").glob("seance[0-9][0-9]") if p.is_dir()}
    for f in sorted((ROOT / "pdf").glob("*")):
        m = re.match(r"(?:feuille-|methodes-)?(seance\d+)[-.]", f.name)
        if m and m.group(1) not in active:
            warn(f"pdf/{f.name} : séance hors ligne, mais ce fichier est publié (il est suivi par git)")


# ------------------------------------------------------------------------------------------ slides
TEXT_EXT = {".scss", ".css", ".qmd", ".yml", ".yaml", ".html", ".js", ".lua", ".md"}
REF_RE = re.compile(r"""(?<![\w./-])((?:\.\./)+[^\s"'`()<>\[\],;{}|#?]+)""")
IMPORT_RE = re.compile(r"""@(?:import|use|forward)\s+["']([^"':]+)["']""")


def referenced_paths(start_files, depth: int = 3):
    """Chemins « ../xxx » (et @import sass) cités par ces fichiers, puis par les fichiers texte cités
    (jusqu'à `depth` niveaux). Seuls ceux situés dans le dépôt sont gardés."""
    seen, found = set(), []
    stack = [(p, 0) for p in start_files]
    while stack:
        p, lvl = stack.pop()
        try:
            text = p.read_text(encoding="utf-8", errors="ignore") if p.stat().st_size < 4_000_000 else ""
        except OSError:
            continue
        cands = [p.parent / m.group(1) for m in REF_RE.finditer(text)]
        if p.suffix == ".scss":
            for m in IMPORT_RE.finditer(text):
                base = p.parent / m.group(1)
                cands += [base, base.parent / (base.name + ".scss"),
                          base.parent / ("_" + base.name + ".scss")]
        for c in cands:
            try:
                c = c.resolve()
            except OSError:
                continue
            if c in seen or not c.is_relative_to(ROOT):
                continue
            seen.add(c)
            found.append(c)
            if c.is_file() and c.suffix in TEXT_EXT and lvl < depth:
                stack.append((c, lvl + 1))
    return sorted(found)


def slide_decks():
    slides = ROOT / "slides"
    decks = []
    for pat in ("seance[0-9][0-9]/*.qmd", "remed_*/*.qmd"):   # mêmes motifs que l'ancien deploy.sh
        for q in sorted(slides.glob(pat)):
            if not q.name.startswith("_"):                       # _*.qmd = fragments
                decks.append(q)
    return decks


def slides(cache: Cache, dest: Path) -> None:
    sl = ROOT / "slides"
    if not sl.is_dir():
        return
    dest.mkdir(parents=True, exist_ok=True)
    for q in slide_decks():
        d = q.parent
        rel_sl = q.relative_to(sl).as_posix()              # seance04/vecteurs.qmd
        stem_rel = rel_sl[:-len(".qmd")]
        siblings = {p.stem for p in d.glob("*.qmd") if not p.name.startswith("_")}
        dir_rel = d.relative_to(ROOT).as_posix()

        def ignore(rel: str, d=d, siblings=siblings, dir_rel=dir_rel, q=q) -> bool:
            sub = rel[len(dir_rel) + 1:]
            if "/" in sub.rstrip("/"):
                return rel.endswith(".quarto_ipynb")
            if sub.endswith("/"):                                  # dossier de 1er niveau
                return sub[:-1].endswith("_files") and sub[:-7] in siblings
            if sub.endswith(".html") and sub[:-5] in siblings:     # rendu d'un deck du dossier
                return True
            if sub.endswith(".qmd") and sub[:-4] in siblings and sub[:-4] != q.stem:
                return True                                        # autre deck : pas une entrée
            return sub.endswith(".quarto_ipynb")

        k = Key("slide", rel_sl)
        k.file(sl / "_quarto.yml")
        k.file(sl / "_metadata.yml")
        k.tree(d, ignore)                                          # le deck, ses fragments, img/…
        for ref in referenced_paths([q] + sorted(d.glob("_*.qmd"))):
            name = ref.relative_to(ROOT).as_posix()
            if ref.is_file():
                k.file(ref)
            elif ref.is_dir():
                k.tree(ref)
            else:
                k.tag("manquant", name)

        def collect(stem_rel=stem_rel) -> list:
            out = []
            html = sl / f"{stem_rel}.html"
            if html.is_file():
                out.append(f"{stem_rel}.html")
                aux = sl / f"{stem_rel}_files"
                if aux.is_dir():
                    out += sorted(p.relative_to(sl).as_posix() for p in aux.rglob("*") if p.is_file())
            return out

        cached_unit(cache, "slide-" + stem_rel.replace("/", "__"), f"slides {stem_rel}",
                    k.digest(), build_base=sl, dest_base=dest, collect=collect,
                    build=lambda rel_sl=rel_sl: run(["quarto", "render", rel_sl], sl,
                                                    f"quarto render slides/{rel_sl}"))
    run(["python3", "slides/make-index.py", dest / "index.html"], ROOT, "slides/make-index.py")


# -------------------------------------------------------------------------------------------- site
BOOK_IGNORE_TOP = {"slides", "a_supprimer", "Claude outputs", "scrcpy", ".git", ".quarto",
                   ".deploy-cache", "__pycache__"}
BOOK_IGNORE_FILES = {"CLAUDE.md", "GUIDE-SEANCES.md", "TAXONOMIE.md", "purge-history.sh",
                     "git-filter-repo.py", "new-seance.sh"}


@functools.lru_cache(maxsize=None)
def output_dir() -> str:
    try:
        m = re.search(r"^\s*output-dir:\s*(\S+)", (ROOT / "_quarto.yml").read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip("\"'")
    except OSError:
        pass
    return "_book"


def book_ignore(rel: str) -> bool:
    """Ce qui n'influence pas le rendu du livre. Tout le reste compte (règle de prudence)."""
    p = rel.rstrip("/")
    top = p.split("/", 1)[0]
    if top in BOOK_IGNORE_TOP or top.startswith(".pdfbuild") or top == output_dir():
        return True
    if p in BOOK_IGNORE_FILES or p.endswith((".pyc", ".quarto_ipynb")):
        return True
    if rel.endswith("/") and p.endswith("_files"):          # sous-produits d'un rendu isolé
        return True
    if p.startswith("seances/") and p.endswith(".html"):    # idem (cf. .gitignore)
        return True
    # Séance hors ligne (seances/_seanceNN/) : seul index.qmd compte (lu par seances.lua)
    m = re.match(r"seances/_seance\d+/(.+)$", p)
    return bool(m and m.group(1) != "index.qmd")


def site(cache: Cache, view: str, dest: Path, warn_orphans: bool) -> None:
    assets(cache, warn_orphans)
    out = ROOT / output_dir()
    k = Key("site", view)
    k.tag("annee", time.strftime("%Y"))   # `date: today` + date-format YYYY dans _quarto.yml
    k.tree(ROOT, book_ignore)             # APRÈS assets : pdf/ y est dans son état final

    def collect() -> list:
        return sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())

    def build() -> float:
        shutil.rmtree(out, ignore_errors=True)
        dt = run(["quarto", "render"], ROOT, "quarto render (site)", build_env())
        if not (out / "index.html").is_file():
            die(f"quarto render n'a pas produit {out.name}/index.html")
        return dt

    dest.mkdir(parents=True, exist_ok=True)
    cached_unit(cache, f"site-{view}", f"site ({view})", k.digest(), build_base=out,
                dest_base=dest, collect=collect, build=build)


# ------------------------------------------------------------------------------------------- outils
def status(cache: Cache) -> None:
    if not cache.root.is_dir():
        print(f"cache vide ({cache.root})")
        return
    total = 0
    for prod in sorted(p for p in cache.root.iterdir() if p.is_dir()):
        entries = [e for e in prod.iterdir() if e.is_dir() and not e.name.startswith(".tmp-")]
        size = sum(f.stat().st_size for e in entries for f in e.rglob("*") if f.is_file())
        total += size
        print(f"  {prod.name:<40} {len(entries)} version(s)  {size / 1e6:7.1f} Mo")
    print(f"total : {total / 1e6:.1f} Mo  ({cache.root})")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build incrémental IMSV (cache par empreinte).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("assets")
    ps = sub.add_parser("site")
    ps.add_argument("--view", required=True, choices=["student", "prof"])
    ps.add_argument("--dest", required=True)
    pl = sub.add_parser("slides")
    pl.add_argument("--dest", required=True)
    for p in (pa, ps):
        p.add_argument("--warn-orphans", action="store_true",
                       help="signale les PDF de séances hors ligne qui seraient publiés")
    for p in (pa, ps, pl):
        p.add_argument("--force", action="store_true", help="ignorer le cache en lecture")
    sub.add_parser("status")
    sub.add_parser("clean")
    args = ap.parse_args()

    dest = Path(args.dest).resolve() if getattr(args, "dest", None) else None
    if getattr(args, "force", False):
        os.environ["IMSV_FORCE"] = "1"
    os.chdir(ROOT)
    cache = Cache(cache_root())

    if args.cmd == "status":
        status(cache)
        return
    if args.cmd == "clean":
        shutil.rmtree(cache.root, ignore_errors=True)
        print(f"cache vidé : {cache.root}")
        return
    if args.cmd == "assets":
        assets(cache, args.warn_orphans)
    elif args.cmd == "site":
        site(cache, args.view, dest, args.warn_orphans)
    elif args.cmd == "slides":
        slides(cache, dest)
    print(f"  → {STATS['cache']} en cache, {STATS['build']} reconstruit(s)", flush=True)


if __name__ == "__main__":
    main()
