#!/usr/bin/env python3
"""incremental.py — build incrémental du site IMSV, par cache d'empreintes de contenu.

Principe. Chaque « produit » (PDF d'une séance, feuille de méthodes, deck de slides, site HTML d'une
vue…) a une EMPREINTE : le sha256 de ce dont il dépend (sources, filtres Lua, thème, script de
build, version de Quarto). Si l'empreinte est déjà dans le cache, le résultat est recopié ; sinon on
construit, puis on range le résultat dans le cache. Les dates de modification ne comptent pas : ça
marche donc dans les worktrees jetables de deploy.sh, et un fichier modifié puis remis à
l'identique ne coûte rien.

Dépendances DYNAMIQUES. Quand `strace` est disponible, chaque build de PDF, de feuille, de méthodes
et de deck est tracé : on enregistre, avec le résultat, les fichiers du dépôt qu'il a réellement lus
(avec leur empreinte), ceux qu'il a cherchés sans les trouver, et les dossiers dont il a testé
l'existence. Au déploiement suivant, l'entrée n'est réutilisée que si tout cela est inchangé. Un
nouvel include, une nouvelle image, un fichier lu par un script modifié sont donc pris en compte
sans rien déclarer. L'empreinte statique ci-dessus reste une première barrière (on invalide donc au
plus plus souvent, jamais moins). Sans strace : empreintes statiques seules, avec un avertissement.
Le site HTML n'est pas tracé : son empreinte couvre déjà tout le dépôt sauf des exclusions explicites.

    python3 incremental.py assets                   PDF des séances, feuilles, méthodes (dans pdf/)
    python3 incremental.py site --view student|prof --dest DIR
                                                     assets + site HTML (Quarto) copié dans DIR
    python3 incremental.py slides --view V --dest DIR
                                                     decks reveal.js + index, copiés dans DIR
    python3 incremental.py status | clean            contenu du cache / le vider
    python3 incremental.py deps [PRÉFIXE]            dépendances tracées de chaque produit en cache
    python3 incremental.py recap                     récapitulatif d'un déploiement (IMSV_STATS_FILE)

    --force (ou IMSV_FORCE=1)   ignore le cache en lecture : tout est reconstruit (et re-rangé).

Cache : <dépôt>/.deploy-cache/ (ignoré par git). Même dossier pour le dépôt et ses worktrees ;
variable IMSV_CACHE pour le changer, IMSV_CACHE_KEEP (défaut 4) = versions gardées par produit.

IMSV_NOTRACE=1 désactive le traçage. IMSV_STATS_FILE=<fichier> : chaque appel y ajoute le détail de
ses produits (utilisé par deploy.sh pour son récapitulatif).

Limites : le traçage ne voit que les fichiers (pas le réseau — polices Google Fonts —, ni les
variables d'environnement, ni l'horloge). En cas de doute : ./deploy.sh --force.
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

ENGINE_VERSION = "2"   # à incrémenter si la logique des empreintes change (invalide tout le cache)
ROOT = Path(__file__).resolve().parent
KEEP = max(1, int(os.environ.get("IMSV_CACHE_KEEP", "4")))
SKIP_DIRS = {".git", ".quarto", "__pycache__", "_book", ".deploy-cache", "node_modules"}
STATS = {"cache": 0, "build": 0}
UNITS: list[dict] = []     # un enregistrement par produit traité (pour le résumé et le récapitulatif)
VIEW = "local"             # étiquette de la vue en cours (student / prof / local)
CATS = {"pdf": "PDF", "feuille": "feuilles", "methodes": "méthodes", "slide": "slides", "site": "site"}


# --------------------------------------------------------------------------------------- affichage
def say(kind: str, label: str, dt: float | None = None, note: str = "") -> None:
    mark = "✓ cache" if kind == "cache" else "⚙ build"
    extra = f"  ({dt:.0f} s)" if dt is not None else ""
    print(f"  {mark}  {label}{extra}{note}", flush=True)


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


# ------------------------------------------------------------------ dépendances tracées (strace)
TRACKED = {
    "open", "openat", "openat2", "creat",
    "stat", "lstat", "stat64", "lstat64", "newfstatat", "fstatat64", "statx",
    "access", "faccessat", "faccessat2", "readlink", "readlinkat", "statfs",
    "chdir", "fchdir", "execve", "clone", "clone3", "fork", "vfork",
    "mkdir", "mkdirat", "symlink", "symlinkat", "link", "linkat",
    "rename", "renameat", "renameat2", "unlink", "unlinkat", "rmdir",
}
# Dans le dépôt, ce qui n'est jamais une dépendance : sorties, caches, métadonnées git.
DEP_IGNORE_TOP = {".git", ".quarto", ".deploy-cache", "_book", "pdf", "node_modules", "__pycache__"}
_PID = re.compile(r"^(?:\[pid\s+(\d+)\]|(\d+))\s+(.*)$")
_CALL = re.compile(r"^(\w+)\((.*)$")
_RESUMED = re.compile(r"^<\.\.\. (\w+) resumed>(.*)$")
_WRITE_FLAGS = re.compile(r"O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND|O_TMPFILE")
_ESC = {"n": 10, "t": 9, "r": 13, "a": 7, "b": 8, "f": 12, "v": 11, "e": 27, "\\": 92, '"': 34}
_TRACE_FLAGS = None


def strace_flags():
    """Options strace utilisables, ou False si le traçage est indisponible (testé une fois)."""
    global _TRACE_FLAGS
    if _TRACE_FLAGS is None:
        _TRACE_FLAGS = False
        if os.environ.get("IMSV_NOTRACE") != "1" and shutil.which("strace"):
            base = ["-f", "-qq", "-y", "-s", "4096", "-e", "trace=%file,%process,fchdir",
                    "-e", "signal=none"]
            for extra in (["--seccomp-bpf"], []):      # --seccomp-bpf : bien plus rapide si dispo
                try:
                    r = subprocess.run(["strace", *base, *extra, "-o", os.devnull, "true"],
                                       capture_output=True)
                except OSError:
                    break
                if r.returncode == 0:
                    _TRACE_FLAGS = base + extra
                    break
        if _TRACE_FLAGS is False:
            warn("strace indisponible (ou IMSV_NOTRACE=1) : dépendances non tracées, "
                 "empreintes statiques seules")
    return _TRACE_FLAGS


def split_args(s: str) -> list:
    """Découpe les arguments d'un appel système strace (chaînes, {}, [], fd annotés 3</chemin>)."""
    out, cur, depth, i, n = [], [], 0, 0, len(s)
    while i < n:
        c = s[i]
        if c == '"':
            j = i + 1
            while j < n and s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            cur.append(s[i:j + 1])
            i = j + 1
            if s[i:i + 3] == "...":
                cur.append("...")
                i += 3
            continue
        if c == "<" and i > 0 and s[i - 1].isdigit():
            j = s.find(">", i)
            j = n - 1 if j < 0 else j
            cur.append(s[i:j + 1])
            i = j + 1
            continue
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif c == "," and depth == 0:
            out.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    if cur:
        out.append("".join(cur).strip())
    return out


def unq(tok: str) -> str:
    """Chaîne C de strace (« "..." ») → str. Gère \\n, \\", \\ooo, \\xHH."""
    if tok.endswith("..."):
        tok = tok[:-3]
    body = tok[1:-1] if len(tok) >= 2 and tok[0] == '"' else tok
    out, i, n = bytearray(), 0, len(body)
    while i < n:
        c = body[i]
        if c == "\\" and i + 1 < n:
            d = body[i + 1]
            if d in "01234567":
                k = i + 1
                while k < n and k < i + 4 and body[k] in "01234567":
                    k += 1
                out.append(int(body[i + 1:k], 8) & 255)
                i = k
            elif d == "x":
                k = i + 2
                while k < n and k < i + 4 and body[k] in "0123456789abcdefABCDEF":
                    k += 1
                out.append(int(body[i + 2:k] or "0", 16))
                i = k
            else:
                out.append(_ESC.get(d, ord(d) & 255))
                i += 2
        else:
            out.extend(c.encode("utf-8", "surrogateescape"))
            i += 1
    return out.decode("utf-8", "surrogateescape")


class TraceParser:
    """Analyse une trace `strace -f -y` : fichiers lus, sondés (présents / absents), écrits.
    Suit le répertoire courant de chaque processus (chdir, fork/clone) pour résoudre les chemins
    relatifs ; les événements d'un processus dont le cwd n'est pas encore connu sont mis en attente."""

    def __init__(self, root_cwd: str):
        self.root_cwd = root_cwd
        self.cwd: dict = {}
        self.deferred: dict = {}
        self.pending: dict = {}
        self.first = None
        self.fallback_events = 0
        self.reads, self.exists, self.missing = set(), set(), set()
        self.touched, self.created_dirs = set(), set()

    # -- lecture des lignes
    def feed(self, line: str) -> None:
        m = _PID.match(line)
        if not m:
            return
        pid = int(m.group(1) or m.group(2))
        rest = m.group(3)
        if rest.startswith(("+++", "---")):
            return
        if rest.startswith("<... "):
            m2 = _RESUMED.match(rest)
            if not m2:
                return
            name, tail = m2.group(1), m2.group(2)
            pend = self.pending.pop(pid, None)
            if pend is None or pend[0] != name:
                return
            body = pend[1] + tail
        else:
            m2 = _CALL.match(rest)
            if not m2 or m2.group(1) not in TRACKED:
                return
            name, body = m2.group(1), m2.group(2)
            if body.endswith("<unfinished ...>"):
                self.pending[pid] = (name, body[:-len("<unfinished ...>")])
                return
        if name not in TRACKED:
            return
        idx = body.rfind(") = ")
        if idx < 0:
            return
        ret = body[idx + 4:]
        rm = re.match(r"(-?\d+|0x[0-9a-fA-F]+|\?)", ret)
        if not rm or rm.group(1) == "?":
            return
        val = int(rm.group(1), 16) if rm.group(1).startswith("0x") else int(rm.group(1))
        em = re.search(r"\b([A-Z][A-Z0-9]{2,})\b", ret[rm.end():])
        ev = (name, split_args(body[:idx]), val != -1, em.group(1) if em else "", val)
        if pid not in self.cwd:
            if self.first is None:
                self.first = pid
                self.cwd[pid] = self.root_cwd
            else:
                self.deferred.setdefault(pid, []).append(ev)
                return
        self.apply(pid, ev)

    def finish(self) -> None:
        for pid, evs in list(self.deferred.items()):   # processus dont on n'a jamais vu le clone
            if pid not in self.cwd:
                self.cwd[pid] = self.root_cwd
                self.fallback_events += len(evs)
            self.drain(pid)

    def drain(self, pid: int) -> None:
        for ev in self.deferred.pop(pid, []):
            self.apply(pid, ev)

    # -- chemins
    def res(self, pid: int, dirfd: str | None, tok: str) -> str:
        p = unq(tok)
        if p.startswith("/"):
            return os.path.normpath(p)
        base = None
        if dirfd and not dirfd.startswith("AT_FDCWD"):
            m = re.search(r"<(.*)>$", dirfd)
            base = m.group(1) if m else None
        if base is None:
            base = self.cwd.get(pid, self.root_cwd)
        return os.path.normpath(os.path.join(base, p))

    def apply(self, pid: int, ev) -> None:
        name, a, ok, err, val = ev
        gone = err in ("ENOENT", "ENOTDIR")
        try:
            if name == "chdir":
                if ok:
                    self.cwd[pid] = self.res(pid, None, a[0])
            elif name == "fchdir":
                m = re.search(r"<(.*)>", a[0]) if a else None
                if ok and m:
                    self.cwd[pid] = m.group(1)
            elif name in ("clone", "clone3", "fork", "vfork"):
                if ok and val > 0:
                    self.cwd.setdefault(val, self.cwd[pid])
                    self.drain(val)
            elif name == "execve":
                if ok:
                    self.reads.add(self.res(pid, None, a[0]))
            elif name in ("open", "creat", "openat", "openat2"):
                at = name in ("openat", "openat2")
                path = self.res(pid, a[0] if at else None, a[1] if at else a[0])
                flags = " ".join(a[2:]) if at else (" ".join(a[1:]) if name == "open" else "O_CREAT")
                write = name == "creat" or bool(_WRITE_FLAGS.search(flags))
                if ok:
                    (self.touched if write else self.reads).add(path)
                elif gone and not write:
                    self.missing.add(path)
            elif name in ("stat", "lstat", "stat64", "lstat64", "access", "readlink", "statfs",
                          "newfstatat", "fstatat64", "statx", "faccessat", "faccessat2", "readlinkat"):
                at = name in ("newfstatat", "fstatat64", "statx", "faccessat", "faccessat2", "readlinkat")
                tok = a[1] if at else a[0]
                if unq(tok) == "":
                    return                                  # fstat sur un fd (AT_EMPTY_PATH)
                path = self.res(pid, a[0] if at else None, tok)
                if ok:
                    self.exists.add(path)
                elif gone:
                    self.missing.add(path)
            elif name in ("mkdir", "mkdirat"):
                if ok:
                    self.created_dirs.add(self.res(pid, a[0] if name == "mkdirat" else None,
                                                   a[1] if name == "mkdirat" else a[0]))
            elif name in ("symlink", "symlinkat"):
                if ok:
                    self.touched.add(self.res(pid, a[1] if name == "symlinkat" else None,
                                              a[2] if name == "symlinkat" else a[1]))
            elif name in ("link", "linkat"):
                if ok:
                    self.touched.add(self.res(pid, a[2] if name == "linkat" else None,
                                              a[3] if name == "linkat" else a[1]))
            elif name in ("rename", "renameat", "renameat2"):
                if ok:
                    if name == "rename":
                        old, new = self.res(pid, None, a[0]), self.res(pid, None, a[1])
                    else:
                        old, new = self.res(pid, a[0], a[1]), self.res(pid, a[2], a[3])
                    self.touched.update((old, new))
            elif name in ("unlink", "unlinkat", "rmdir"):
                if ok:
                    self.touched.add(self.res(pid, a[0] if name == "unlinkat" else None,
                                              a[1] if name == "unlinkat" else a[0]))
        except (IndexError, KeyError):
            pass   # ligne inattendue : on ignore l'événement plutôt que de planter le build


def strip_book_block(text: str) -> str:
    """_quarto.yml sans son bloc « book: » (chapitres, site-url…) : il change entre la vue étudiant
    et la vue prof sans influencer les PDF ni les slides rendus hors projet."""
    out, skipping = [], False
    for line in text.splitlines(keepends=True):
        if re.match(r"^book:\s*(#.*)?$", line):
            skipping = True
            continue
        if skipping and re.match(r"^[A-Za-z_]", line):
            skipping = False
        if not skipping:
            out.append(line)
    return "".join(out)


def dep_digest(path: Path, rel: str) -> str:
    h = hashlib.sha256()
    if rel == "_quarto.yml":
        h.update(strip_book_block(path.read_text(encoding="utf-8", errors="replace")).encode())
    else:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()[:24]


def deps_from_trace(tp: TraceParser) -> dict | None:
    def rel(p: str):
        try:
            r = Path(p).relative_to(ROOT).as_posix()
        except ValueError:
            return None
        return None if r == "." else r

    owned = {r for r in (rel(p) for p in tp.touched | tp.created_dirs) if r}   # écrit par le build

    def ignored(r: str) -> bool:
        parts = r.split("/")
        if parts[0] in DEP_IGNORE_TOP or parts[0].startswith(".pdfbuild") or ".quarto" in parts:
            return True
        if parts[0] == output_dir() or r.endswith(".quarto_ipynb"):
            return True
        return any("/".join(parts[:k]) in owned for k in range(1, len(parts) + 1))

    read, exists, absent = {}, {}, []
    for p in sorted(tp.reads):
        r = rel(p)
        if r and not ignored(r) and (ROOT / r).is_file():
            read[r] = dep_digest(ROOT / r, r)
    for p in sorted(tp.missing):
        r = rel(p)
        if r and not ignored(r) and r not in read and not os.path.lexists(ROOT / r):
            absent.append(r)
    anc = set()
    for r in list(read) + absent:
        parts = r.split("/")
        anc.update("/".join(parts[:k]) for k in range(1, len(parts)))
    for p in sorted(tp.exists):
        r = rel(p)
        if r and not ignored(r) and r not in read and r not in anc:
            if (ROOT / r).is_dir():
                exists[r] = "dir"
            elif (ROOT / r).is_file():
                exists[r] = "file"
    if not read:
        return None
    return {"read": read, "exists": exists, "absent": absent}


def deps_problem(deps: dict) -> str | None:
    """Première dépendance enregistrée qui a changé, ou None si tout est identique."""
    for r, dg in deps["read"].items():
        p = ROOT / r
        if not p.is_file():
            return f"{r} (disparu)"
        if dep_digest(p, r) != dg:
            return r
    for r, kind in deps["exists"].items():
        p = ROOT / r
        if not (p.is_dir() if kind == "dir" else p.is_file()):
            return f"{r} (disparu)"
    for r in deps["absent"]:
        if os.path.lexists(ROOT / r):
            return f"{r} (nouveau fichier)"
    return None


def build_cmd(cmd, cwd: Path, label: str, env: dict | None = None):
    """Lance un build en le traçant si possible → (durée, dépendances | None)."""
    flags = strace_flags()
    if not flags:
        return run(cmd, cwd, label, env), None
    fd, tpath = tempfile.mkstemp(prefix="imsv-trace-")
    os.close(fd)
    try:
        dt = run(["strace", *flags, "-o", tpath, *cmd], cwd, label, env)
        tp = TraceParser(str(cwd))
        with open(tpath, "r", encoding="utf-8", errors="surrogateescape") as f:
            for line in f:
                tp.feed(line.rstrip("\n"))
        tp.finish()
    finally:
        try:
            os.unlink(tpath)
        except OSError:
            pass
    deps = deps_from_trace(tp)
    if deps is None:
        warn(f"{label} : trace inexploitable (aucun fichier du dépôt lu) — empreinte statique seule")
        return dt, False   # False = traçage tenté mais inexploitable (None = traçage indisponible)
    return dt, deps


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
        self.reason = ""   # pourquoi le dernier lookup a échoué, quand c'est instructif

    def lookup(self, name: str, key: str):
        """-> (dossier des fichiers, {chemin relatif: taille}) ou None."""
        self.reason = ""
        if os.environ.get("IMSV_FORCE") == "1":
            self.reason = "forcé"
            return None
        e = self.root / name / key
        try:
            manifest = json.loads((e / "manifest.json").read_text())
            files = manifest["files"]
            for rel, size in files.items():
                if (e / "files" / rel).stat().st_size != size:
                    raise ValueError(rel)
        except Exception:
            if e.exists():
                shutil.rmtree(e, ignore_errors=True)   # entrée incomplète ou corrompue : jetée
            return None
        if manifest.get("trace") == "off" and strace_flags():
            self.reason = "construit auparavant sans traçage"   # on le refait, cette fois tracé
            return None
        if manifest.get("deps"):   # dépendances tracées au moment du build : toujours identiques ?
            bad = deps_problem(manifest["deps"])
            if bad:
                self.reason = f"dépendance modifiée : {bad}"
                return None
        try:
            os.utime(e, None)   # « utilisée récemment » : protège de l'élagage
        except OSError:
            pass
        return e / "files", files

    def store(self, name: str, key: str, base: Path, rels, deps=None, trace: str = "n/a") -> None:
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
            (tmp / "manifest.json").write_text(json.dumps({"files": sizes, "deps": deps, "trace": trace}))
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
                dest_base: Path, collect, build, on_hit=None, announce: str = "") -> None:
    """Un produit : si `key` est en cache → recopie dans dest_base ; sinon build() puis rangement.
    build() renvoie la durée, ou (durée, dépendances tracées). collect() liste, après build, les
    fichiers produits (relatifs à build_base). `announce` : si non vide, ligne « rendu en cours »
    affichée avant un build (pour les builds longs, comme les slides)."""
    cat = CATS.get(name.split("-")[0], name.split("-")[0])
    hit = cache.lookup(name, key)
    if hit:
        files_dir, files = hit
        if on_hit:
            on_hit(set(files))
        restore(files_dir, list(files), dest_base)
        STATS["cache"] += 1
        UNITS.append({"cat": cat, "label": label, "view": VIEW, "status": "cache", "secs": 0.0})
        say("cache", label)
        return
    reason = cache.reason
    if announce:
        print(f"  … rendu   {announce}", flush=True)
    res = build()
    if isinstance(res, tuple):
        dt, deps = res
        trace = "ok" if deps else ("failed" if deps is False else "off")
        deps = deps or None
    else:
        dt, deps, trace = res, None, "n/a"   # produit non tracé (site)
    rels = collect()
    if not rels:
        die(f"{label} : le build n'a produit aucun fichier")
    cache.store(name, key, build_base, rels, deps, trace)
    if dest_base != build_base:
        restore(build_base, rels, dest_base)
    STATS["build"] += 1
    UNITS.append({"cat": cat, "label": label, "view": VIEW, "status": "build", "secs": round(dt, 1),
                  "why": reason})
    notes = []
    if deps:
        notes.append(f"{len(deps['read'])} fichiers lus")
    if reason and reason != "forcé":
        notes.append(reason)
    say("build", announce or label, dt, f"  [{' · '.join(notes)}]" if notes else "")


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
                    build=lambda s=s: build_cmd(["bash", "build-pdf.sh", s], ROOT, f"build-pdf.sh {s}", env))

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
                    build=lambda b=b: build_cmd(["bash", "build-methodes.sh", b], ROOT,
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
                    build=lambda s=s: build_cmd(["bash", "build-boite.sh", s], ROOT,
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
    decks = slide_decks()
    only = {x for x in os.environ.get("IMSV_ONLY_SEANCES", "").replace(",", " ").split() if x}
    if only:        # déploiement ciblé : seuls les decks des séances demandées sont (re)construits
        decks = [q for q in decks if q.parent.name.startswith("seance") and q.parent.name[6:] in only]
    print(f"  slides ({VIEW}) : {len(decks)} deck(s) — "
          + ", ".join(q.relative_to(sl).with_suffix("").as_posix() for q in decks), flush=True)
    for i, q in enumerate(decks, 1):
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

        tag = f"slides [{i}/{len(decks)}] {stem_rel}"
        cached_unit(cache, "slide-" + stem_rel.replace("/", "__"), tag,
                    k.digest(), build_base=sl, dest_base=dest, collect=collect, announce=tag,
                    build=lambda rel_sl=rel_sl: build_cmd(["quarto", "render", rel_sl], sl,
                                                          f"quarto render slides/{rel_sl}"))
    run(["python3", "slides/make-index.py", dest / "index.html"], ROOT, "slides/make-index.py")
    print(f"  ✓ index   slides/index.html ({len(decks)} deck(s) listés)", flush=True)


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


def print_summary() -> None:
    by: dict = {}
    for u in UNITS:
        c = by.setdefault(u["cat"], {"cache": 0, "build": 0, "secs": 0.0})
        c[u["status"]] += 1
        c["secs"] += u["secs"]
    for cat in ("PDF", "feuilles", "méthodes", "slides", "site"):
        if cat in by:
            c = by[cat]
            n = c["cache"] + c["build"]
            unit = "deck(s)" if cat == "slides" else "produit(s)"
            secs = f" ({c['secs']:.0f} s)" if c["build"] else ""
            print(f"  → {cat:<9} {n} {unit} : {c['cache']} en cache, {c['build']} reconstruit(s){secs}",
                  flush=True)


def flush_stats(cmd: str) -> None:
    path = os.environ.get("IMSV_STATS_FILE")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        for u in UNITS:
            f.write(json.dumps(dict(u, cmd=cmd), ensure_ascii=False) + "\n")


def recap() -> None:
    """Récapitulatif d'un déploiement, lu dans IMSV_STATS_FILE (rempli par les appels précédents)."""
    path = os.environ.get("IMSV_STATS_FILE")
    units = []
    if path and os.path.isfile(path):
        for line in open(path, encoding="utf-8"):
            if line.strip():
                units.append(json.loads(line))
    if not units:
        return
    names = {"student": "étudiant", "prof": "prof", "local": "local"}
    print("Récapitulatif")
    site_rows = [u for u in units if u["cat"] == "site"]
    for u in site_rows:
        txt = f"rendu Quarto ({u['secs']:.0f} s)" if u["status"] == "build" else "réutilisé du cache"
        print(f"  site {names.get(u['view'], u['view']):<9}: {txt}")
    asset = {}
    for u in units:
        if u["cat"] in ("PDF", "feuilles", "méthodes"):
            a = asset.setdefault(u["label"], [])
            a.append(u)
    built = {l: us for l, us in asset.items() if any(x["status"] == "build" for x in us)}
    secs = sum(x["secs"] for us in built.values() for x in us if x["status"] == "build")
    print(f"  PDF, feuilles, méthodes : {len(asset)} produit(s) — {len(built)} reconstruit(s)"
          + (f" ({secs:.0f} s)" if built else ""))
    for l in sorted(built):
        print(f"      ⚙ {l}")
    decks: dict = {}
    for u in units:
        if u["cat"] == "slides":
            name = re.sub(r"^slides \[\d+/\d+\] ", "", u["label"])
            decks.setdefault(name, {})[u["view"]] = u
    nb = sum(1 for d in decks.values() if any(x["status"] == "build" for x in d.values()))
    ssecs = sum(x["secs"] for d in decks.values() for x in d.values() if x["status"] == "build")
    print(f"  slides : {len(decks)} deck(s) — {nb} reconstruit(s)" + (f" ({ssecs:.0f} s)" if nb else ""))
    for name in sorted(decks):
        d = decks[name]
        parts = []
        for v in ("student", "prof"):
            if v in d:
                x = d[v]
                parts.append(f"{names[v]} : " + (f"reconstruit ({x['secs']:.0f} s)" if x["status"] == "build"
                                                  else "cache"))
        mark = "⚙" if any(x["status"] == "build" for x in d.values()) else "✓"
        print(f"      {mark} {name:<42} " + " · ".join(parts))


def show_deps(cache: Cache, prefix: str) -> None:
    """Dépendances tracées de la version la plus récente de chaque produit."""
    if not cache.root.is_dir():
        print("cache vide")
        return
    for prod in sorted(p for p in cache.root.iterdir() if p.is_dir() and p.name.startswith(prefix)):
        entries = sorted((e for e in prod.iterdir() if e.is_dir() and not e.name.startswith(".tmp-")),
                         key=lambda e: e.stat().st_mtime, reverse=True)
        if not entries:
            continue
        try:
            deps = json.loads((entries[0] / "manifest.json").read_text()).get("deps")
        except Exception:
            deps = None
        if not deps:
            print(f"{prod.name} : pas de dépendances tracées")
            continue
        print(f"{prod.name} : {len(deps['read'])} fichier(s) lu(s), {len(deps['exists'])} existence(s), "
              f"{len(deps['absent'])} absent(s) surveillé(s)")
        for r in deps["read"]:
            print(f"    lu      {r}")
        for r, kind in deps["exists"].items():
            print(f"    existe  {r} ({kind})")
        for r in deps["absent"]:
            print(f"    absent  {r}")


def main() -> None:
    global VIEW
    ap = argparse.ArgumentParser(description="Build incrémental IMSV (cache par empreinte).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("assets")
    ps = sub.add_parser("site")
    ps.add_argument("--view", required=True, choices=["student", "prof"])
    ps.add_argument("--dest", required=True)
    pl = sub.add_parser("slides")
    pl.add_argument("--dest", required=True)
    pl.add_argument("--view", default="local", choices=["student", "prof", "local"])
    for p in (pa, ps):
        p.add_argument("--warn-orphans", action="store_true",
                       help="signale les PDF de séances hors ligne qui seraient publiés")
    for p in (pa, ps, pl):
        p.add_argument("--force", action="store_true", help="ignorer le cache en lecture")
    sub.add_parser("status")
    sub.add_parser("clean")
    pd = sub.add_parser("deps")
    pd.add_argument("prefix", nargs="?", default="")
    sub.add_parser("recap")
    args = ap.parse_args()

    dest = Path(args.dest).resolve() if getattr(args, "dest", None) else None
    if getattr(args, "force", False):
        os.environ["IMSV_FORCE"] = "1"
    VIEW = getattr(args, "view", None) or "local"
    os.chdir(ROOT)
    cache = Cache(cache_root())

    if args.cmd == "status":
        status(cache)
        return
    if args.cmd == "clean":
        shutil.rmtree(cache.root, ignore_errors=True)
        print(f"cache vidé : {cache.root}")
        return
    if args.cmd == "deps":
        show_deps(cache, args.prefix)
        return
    if args.cmd == "recap":
        recap()
        return
    if args.cmd == "assets":
        assets(cache, args.warn_orphans)
    elif args.cmd == "site":
        site(cache, args.view, dest, args.warn_orphans)
    elif args.cmd == "slides":
        slides(cache, dest)
    print_summary()
    flush_stats(args.cmd)


if __name__ == "__main__":
    main()
