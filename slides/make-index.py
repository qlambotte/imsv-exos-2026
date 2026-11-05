#!/usr/bin/env python3
"""Génère slides/index.html : une ligne par séance d'exercices, rangée par mois,
sur deux colonnes, avec à droite la ou les remédiations qui reprennent la séance.

Appelé automatiquement au déploiement (incremental.py slides), qui écrit
directement dans le stage : le fichier n'est pas une source versionnée, il n'y a
donc rien à mettre à jour à la main quand une séance ou une remédiation s'ajoute.

Pour prévisualiser en local :
    python3 make-index.py            # écrit slides/index.html
    python3 make-index.py /tmp/x.html

Séances — un dossier seanceNN/ est repris dès qu'il contient un .qmd qui n'est
pas un fragment (préfixé par « _ »). Par deck :
  - le libellé vient de `title:` (convention : "Séance N — Nom") ;
  - le mois vient de `date:` (MM/JJ/AAAA ou AAAA-MM-JJ) ; sans date, la séance
    est rangée sous « Date à préciser » (et un avertissement est affiché) ;
  - le symbole vient de `symbole:` s'il est présent, sinon du tableau SYMBOLES
    ci-dessous, sinon la pastille n'affiche que le numéro.

Séances à venir — le tableau PROGRAMME ci-dessous liste les séances pas encore
en ligne ; elles apparaissent en grisé, sans lien, jusqu'à ce que leur deck
slides/seanceNN/ existe (le deck a alors priorité).

Remédiations — dossiers remed_*/. Par deck :
  - le thème vient de `subtitle:` ("Thème : Les vecteurs", sans « (séance N) »
    ni « · annexe … ») ;
  - la séance reprise vient de `seance:` s'il est présent, sinon d'une mention
    « séance N » dans `subtitle:` ou `description:` ;
  - un deck dont le nom de fichier ou le sous-titre contient « annexe » est
    l'annexe de la remédiation du même dossier.
Deux onglets : « Séances » (une ligne par séance, remédiations à droite) et
« Remédiations » (une ligne par remédiation, rangée par mois de la séance reprise ;
remed_accueil en tête). L'onglet ouvert suit l'ancre de l'URL (#seances ou
#remediations).
"""
import datetime
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Symbole affiché dans la pastille de chaque séance (HTML autorisé).
# Un champ `symbole:` dans le deck a priorité sur ce tableau.
VEC = ('<span class="vec">u<span>→</span></span>')
SYMBOLES = {
    1: "⟹", 2: "sin", 3: "y=", 4: VEC, 5: "f(x)", 6: "eˣ",
    7: "lim", 8: "f'", 9: "max", 10: "∫", 11: "∫ᵇₐ",
}

# Couleur de chaque séance (cycle si plus de séances que de couleurs).
COULEURS = ["#1f5fbf", "#b8325a", "#8a6d00", "#0e8a6b", "#6b4fbb", "#c25e12",
            "#2a7f9e", "#a3367e", "#4d7c0f", "#3f51b5", "#b0412e", "#5b6b7b"]

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]
MOIS_COURT = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
              "août", "sept.", "oct.", "nov.", "déc."]
SANS_DATE = "Date à préciser"

# Programme complet : séances pas encore en ligne, affichées en grisé (sans lien)
# tant que leur deck slides/seanceNN/ n'existe pas. Seul le mois sert (rangement).
PROGRAMME = {
    7: ("Variation, limite et dérivée", 2026, 11),
    8: ("Calcul différentiel", 2026, 11),
    9: ("Exploiter la dérivée : variations, optimisation et approximation", 2026, 11),
    10: ("Intégrale : mesurer une accumulation", 2026, 12),
    11: ("Calcul intégral et applications", 2026, 12),
}


def frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^(\w[\w-]*):\s*(.*?)\s*$', line)
        if km and km.group(2):
            v = km.group(2)
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            fm[km.group(1)] = v
    return fm


def parse_date(s):
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except (ValueError, TypeError):
            pass
    return None


def decks(folder):
    """Decks (non-fragments) d'un dossier, triés par nom."""
    return [q for q in sorted(glob.glob(os.path.join(folder, "*.qmd")))
            if not os.path.basename(q).startswith("_")]


def href(folder, qmd):
    return f"{os.path.basename(folder)}/{os.path.splitext(os.path.basename(qmd))[0]}.html"


def find_seances():
    found = []
    for d in sorted(glob.glob(os.path.join(ROOT, "seance[0-9][0-9]"))):
        num = int(os.path.basename(d)[-2:])
        for qmd in decks(d):
            fm = frontmatter(qmd)
            title = fm.get("title", f"Séance {num}")
            found.append({
                "num": num,
                "label": re.sub(r"^Séance\s*\d+\s*[—-]\s*", "", title),
                "date": parse_date(fm.get("date")),
                "symbole": fm.get("symbole") or SYMBOLES.get(num),
                "href": href(d, qmd),
                "remeds": [],
            })
    return found


def find_remeds():
    """Une entrée par dossier remed_* : thème, séance reprise, slides, annexe."""
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, "remed_*"))):
        r = {"theme": None, "seance": None, "slides": None, "annexe": None,
             "dossier": os.path.basename(d)}
        for qmd in decks(d):
            fm = frontmatter(qmd)
            sub = fm.get("subtitle", "")
            est_annexe = "annexe" in os.path.basename(qmd).lower() or "annexe" in sub.lower()
            r["annexe" if est_annexe else "slides"] = r["annexe" if est_annexe else "slides"] or href(d, qmd)
            if r["seance"] is None:
                s = fm.get("seance")
                if s and s.isdigit():
                    r["seance"] = int(s)
                else:
                    m = re.search(r"séance\s+(\d+)", sub + " " + fm.get("description", ""), re.I)
                    if m:
                        r["seance"] = int(m.group(1))
            if not est_annexe and r["theme"] is None:
                th = re.sub(r"^Thème\s*:\s*", "", sub)
                th = re.sub(r"\s*\(séance\s+\d+\)", "", th).split("·")[0].strip()
                r["theme"] = th or fm.get("title", r["dossier"])
        if r["slides"] or r["annexe"]:
            out.append(r)
    return out


def esc(s):
    return html.escape(s, quote=True)


def couleur(num):
    return COULEURS[(num - 1) % len(COULEURS)]


def pastille(s):
    sy = f'<span class="sy">{s["symbole"]}</span>' if s["symbole"] else ""
    return f'<span class="p" style="--c:{couleur(s["num"])}">{sy}<span class="n">S{s["num"]}</span></span>'


def ligne(s):
    c = couleur(s["num"])
    if s.get("avenir"):
        return (f'<li class="row avenir" style="--c:{c}">{pastille(s)}'
                f'<span class="t" title="{esc(s["label"])}">{esc(s["label"])}</span>'
                f'<span class="av">à venir</span><span class="rms"></span></li>')
    rem = ""
    for r in s["remeds"]:
        rem += '<span class="rm">'
        if r["slides"]:
            rem += f'<a class="ch" href="{esc(r["slides"])}">{esc(r["theme"])}</a>'
        if r["annexe"]:
            rem += f'<a class="ax" href="{esc(r["annexe"])}" title="Annexe : {esc(r["theme"])}">annexe</a>'
        rem += '</span>'
    return (f'<li class="row" style="--c:{c}">{pastille(s)}'
            f'<a class="t" href="{esc(s["href"])}" title="{esc(s["label"])}">{esc(s["label"])}</a>'
            f'<a class="go" href="{esc(s["href"])}">▶ Slides</a>'
            f'<span class="rms">{rem}</span></li>')


def groupes(seances):
    """[(libellé du mois, [séances])] dans l'ordre chronologique."""
    g = {}
    for s in seances:
        key = (s["date"].year, s["date"].month) if s["date"] else (9999, 0)
        g.setdefault(key, []).append(s)
    out = []
    for key in sorted(g):
        lab = MOIS[key[1] - 1].capitalize() if key[0] != 9999 else SANS_DATE
        out.append((lab, sorted(g[key], key=lambda s: s["num"])))
    return out


def deux_colonnes(gs, taille=len):
    """Coupe la liste des mois en deux colonnes les plus équilibrées possible
    (un intertitre compte pour une ligne)."""
    poids = [taille(x) + 1 for _, x in gs]
    tot = sum(poids)
    best, acc = 0, 0
    for i, w in enumerate(poids):
        acc += w
        if abs(tot - 2 * acc) <= abs(tot - 2 * sum(poids[:best])):
            best = i + 1
    return gs[:best], gs[best:]


def colonne(gs):
    out = ""
    for lab, ss in gs:
        out += f'<section><h2>{esc(lab)}</h2><ul>' + "".join(ligne(s) for s in ss) + "</ul></section>"
    return f'<div class="col">{out}</div>'


def ligne_remed(r, s):
    """Ligne de l'onglet Remédiations ; s = séance reprise (ou None)."""
    c = couleur(s["num"]) if s else "#5a6b7b"
    pas = pastille(s) if s else '<span class="p" style="--c:#5a6b7b"><span class="sy">R</span></span>'
    lien = r["slides"] or r["annexe"]
    ref = f'Séance {s["num"]} — {esc(s["label"])}' if s else "&nbsp;"
    go = f'<a class="go" href="{esc(r["slides"])}">▶ Slides</a>' if r["slides"] else "<span></span>"
    ax = f'<a class="ax" href="{esc(r["annexe"])}">annexe</a>' if r["annexe"] else "<span></span>"
    return (f'<li class="row rrow" style="--c:{c}">{pas}'
            f'<span class="tt"><a class="t" href="{esc(lien)}">{esc(r["theme"])}</a><span class="ref">{ref}</span></span>'
            f'{go}{ax}</li>')


def colonne_remed(gs):
    out = ""
    for lab, items in gs:
        out += f'<section><h2>{esc(lab)}</h2><ul>' + "".join(ligne_remed(r, s) for r, s in items) + "</ul></section>"
    return f'<div class="col">{out}</div>'


def completer(seances):
    """Ajoute, en grisé, les séances du PROGRAMME dont le deck n'existe pas encore."""
    nums = {s["num"] for s in seances}
    for n, (label, an, mois) in PROGRAMME.items():
        if n not in nums:
            seances.append({"num": n, "label": label, "date": datetime.date(an, mois, 1),
                            "symbole": SYMBOLES.get(n), "href": None, "remeds": [], "avenir": True})
    return sorted(seances, key=lambda s: s["num"])


def render(seances, remeds):
    nb_en_ligne = len(seances)
    seances = completer(seances)
    par_num = {s["num"]: s for s in seances}
    accueil, autres = None, []
    for r in remeds:
        if r["seance"] in par_num:
            par_num[r["seance"]]["remeds"].append(r)
        elif r["dossier"] == "remed_accueil":
            accueil = r
        else:
            autres.append(r)
    for s in seances:
        if not s["date"]:
            print(f"  ! séance {s['num']} : pas de `date:` dans le deck → rangée sous « {SANS_DATE} »",
                  file=sys.stderr)
    for r in autres:
        print(f"  ! {r['dossier']} : séance reprise inconnue (ajouter `seance: N` au deck)",
              file=sys.stderr)

    # Onglet Séances
    gauche, droite = deux_colonnes(groupes(seances))
    p_seances = f'<div class="cols">{colonne(gauche)}{colonne(droite)}</div>'

    # Onglet Remédiations : rangées par mois de la séance reprise
    gs = [(lab, [(r, s) for s in ss for r in s["remeds"]]) for lab, ss in groupes(seances)]
    gs = [(lab, items) for lab, items in gs if items]
    if autres:
        gs.append(("Autres", [(r, None) for r in autres]))
    nb_remed = sum(len(items) for _, items in gs)
    p_remed = ""
    if accueil:
        p_remed += (f'<a class="accueil" href="{esc(accueil["slides"] or accueil["annexe"])}">'
                    f'<span class="i">★</span><span><b>Accueil du dispositif</b>'
                    f'<span> · mur de questions, QCM en autonomie, choix du thème</span></span>'
                    f'<span class="go2">▶ Slides</span></a>')
    rg, rd = deux_colonnes(gs, taille=lambda items: len(items))
    p_remed += f'<div class="cols">{colonne_remed(rg)}{colonne_remed(rd)}</div>'

    tabs = ('<nav class="tabs" role="tablist">'
            f'<a href="#seances" data-tab="seances" role="tab">Séances <span class="ct">{nb_en_ligne}/{len(seances)}</span></a>'
            f'<a href="#remediations" data-tab="remediations" role="tab">Remédiations <span class="ct">{nb_remed}</span></a>'
            '</nav>')
    body = (tabs + f'<div class="panel" id="seances" role="tabpanel">{p_seances}</div>'
            f'<div class="panel" id="remediations" role="tabpanel">{p_remed}</div>')
    return TEMPLATE.replace("{body}", body)


TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Slides — IMSV</title>
<script>document.documentElement.classList.add("js");</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Slab:wght@600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --h:#14304a; --muted:#5a6b7b; --rule:#e5e9ef; --strong:#14304a;
    --page-bg:#ffffff; --text:#24313d; --hover:#f3f7fe; --tint:14%;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --h:#e8eef6; --muted:#9db0c1; --rule:#26323d; --strong:#9db0c1;
      --page-bg:#11171d; --text:#c7d2dc; --hover:#18222c; --tint:26%;
    }
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--page-bg);color:var(--text);
    font-family:"Roboto",system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
    line-height:1.5;-webkit-font-smoothing:antialiased;}
  a{color:inherit;text-decoration:none;}
  .wrap{max-width:1320px;margin:0 auto;padding:3rem 1.5rem 4rem;}
  h1{font-family:"Roboto Slab",Georgia,serif;font-weight:700;color:var(--h);margin:0 0 .25rem;font-size:2rem;}
  .subtitle{color:var(--muted);margin:0 0 2rem;}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:2.2rem;align-items:start;}
  section{margin-bottom:1.6rem;}
  h2{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--muted);
    margin:0;padding-bottom:.4rem;border-bottom:1.5px solid var(--strong);}
  ul{list-style:none;margin:0;padding:0;}
  .row{display:grid;grid-template-columns:2.6rem minmax(0,1fr) 4.8rem 11.5rem;align-items:center;gap:.6rem;
    min-height:3.1rem;padding:.3rem .4rem;margin:0 -.4rem;border-bottom:1px solid var(--rule);border-radius:.4rem;}
  .row:hover{background:var(--hover);}
  .p{width:2.4rem;height:2.4rem;border-radius:.55rem;background:var(--c);color:#fff;display:flex;flex-direction:column;
    align-items:center;justify-content:center;line-height:1.05;}
  .p .sy{font-family:"Roboto Slab",Georgia,serif;font-style:italic;font-weight:700;font-size:.8rem;}
  .p .n{font-size:.62rem;font-weight:700;letter-spacing:.05em;opacity:.92;}
  .vec{position:relative;display:inline-block;}
  .vec span{position:absolute;left:.05em;top:-.62em;font-size:.62em;font-style:normal;}
  .t{font-weight:500;color:var(--h);line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
  .t:hover{text-decoration:underline;}
  .go{font-weight:700;color:var(--c);white-space:nowrap;font-size:.95rem;}
  .go:hover{text-decoration:underline;}
  .rms{display:flex;flex-direction:column;align-items:flex-end;gap:.25rem;}
  .rm{display:flex;align-items:baseline;gap:.45rem;}
  .ch{font-size:.85rem;font-weight:500;padding:.12rem .55rem;border-radius:.4rem;white-space:nowrap;
    color:var(--c);background:color-mix(in srgb,var(--c) var(--tint),transparent);}
  .ch:hover{background:color-mix(in srgb,var(--c) calc(var(--tint) + 10%),transparent);}
  .ax{font-size:.78rem;color:var(--muted);}
  .avenir .p{opacity:.35;}
  .avenir .t{color:var(--muted);opacity:.75;}
  .av{font-size:.85rem;font-style:italic;color:var(--muted);opacity:.75;white-space:nowrap;}
  .ax:hover{color:var(--c);text-decoration:underline;}
  .tabs{display:flex;gap:2rem;border-bottom:1px solid var(--rule);margin:0 0 1.8rem;}
  .tabs a{padding:.7rem .1rem;font-weight:700;color:var(--muted);border-bottom:3px solid transparent;margin-bottom:-1px;}
  .tabs a:hover{color:var(--h);}
  .tabs a.on{color:var(--h);border-bottom-color:var(--strong);}
  .tabs .ct{font-weight:500;font-size:.75rem;background:var(--rule);color:var(--muted);border-radius:1rem;padding:.05rem .5rem;margin-left:.35rem;}
  .js .panel{display:none;}
  .js .panel.on{display:block;}
  .rrow{grid-template-columns:2.6rem minmax(0,1fr) 4.8rem 3.6rem;}
  .tt{display:flex;flex-direction:column;min-width:0;}
  .tt .t{-webkit-line-clamp:1;}
  .ref{font-size:.8rem;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .rrow .ax{justify-self:end;}
  .accueil{display:flex;align-items:center;gap:.9rem;padding:.6rem 1rem .6rem .6rem;margin-bottom:1.6rem;
    border:1.5px dashed #d9b48a;border-radius:.6rem;color:var(--text);}
  .accueil:hover{background:var(--hover);}
  .accueil .i{width:2.4rem;height:2.4rem;border-radius:.55rem;background:#b5651d;color:#fff;display:flex;align-items:center;justify-content:center;flex:none;}
  .accueil b{color:var(--h);font-weight:700;}
  .accueil span span{color:var(--muted);font-size:.92rem;}
  .accueil .go2{margin-left:auto;font-weight:700;color:#b5651d;white-space:nowrap;}
  footer{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--rule);color:var(--muted);font-size:.85rem;}
  @media (max-width: 960px){ .cols{grid-template-columns:1fr;gap:0;} }
  @media (max-width: 560px){
    .wrap{padding:2rem 1rem 3rem;}
    .row{grid-template-columns:2.6rem minmax(0,1fr) auto;}
    .t{-webkit-line-clamp:3;}
    .rms{grid-column:2 / -1;align-items:flex-start;padding-bottom:.2rem;}
    .rrow{grid-template-columns:2.6rem minmax(0,1fr) auto auto;}
  }
</style>
</head>
<body>
<div class="wrap">
  <h1>Slides</h1>
  <p class="subtitle">IMSV — supports de projection : séances d'exercices et remédiations.</p>
{body}
  <script>
    (function(){
      var tabs=document.querySelectorAll(".tabs a"), panels=document.querySelectorAll(".panel");
      function show(id){
        if(!document.getElementById(id)) id="seances";
        tabs.forEach(function(a){var on=a.dataset.tab===id;a.classList.toggle("on",on);a.setAttribute("aria-selected",on);});
        panels.forEach(function(p){p.classList.toggle("on",p.id===id);});
      }
      tabs.forEach(function(a){a.addEventListener("click",function(e){
        e.preventDefault();show(a.dataset.tab);
        try{history.replaceState(null,"","#"+a.dataset.tab);}catch(err){}});});
      show(location.hash.slice(1));
    })();
  </script>
  <footer>IMSV — Faculté des Sciences et Faculté de Médecine, Pharmacie et sciences Biomédicales, UMONS.</footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    page = render(find_seances(), find_remeds())
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"écrit : {out}")
