#!/usr/bin/env python3
"""Génère slides/index.html à partir des decks trouvés dans slides/seanceNN/*.qmd.

Appelé automatiquement par deploy.sh (build_slides), qui écrit directement dans
le stage de déploiement : le fichier n'est plus une source versionnée, il n'y a
donc plus rien à mettre à jour à la main quand une séance s'ajoute.

Pour prévisualiser en local :
    python3 make-index.py            # écrit slides/index.html
    python3 make-index.py /tmp/x.html

Un dossier seanceNN/ est repris dès qu'il contient un .qmd qui n'est pas un
fragment (préfixé par « _ »). Par deck :
  - le groupe et le libellé du lien viennent du champ `title:` du deck
    (convention : "Séance N — Nom") ;
  - la ligne grise sous le titre vient de `description:` si présent, sinon de
    `subtitle:`.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^(\w[\w-]*):\s*"(.*)"\s*$', line)
        if km:
            fm[km.group(1)] = km.group(2)
    return fm


def find_decks():
    found = []
    for d in sorted(glob.glob(os.path.join(ROOT, "seance[0-9][0-9]"))):
        n = os.path.basename(d)
        num = int(n.replace("seance", ""))
        for qmd in sorted(glob.glob(os.path.join(d, "*.qmd"))):
            if os.path.basename(qmd).startswith("_"):
                continue
            fm = frontmatter(qmd)
            title = fm.get("title", n)
            label = re.sub(r"^Séance\s*\d+\s*[—-]\s*", "", title)
            sub = fm.get("description") or fm.get("subtitle", "")
            html_name = os.path.splitext(os.path.basename(qmd))[0] + ".html"
            found.append({
                "num": num,
                "title": title,
                "label": label,
                "sub": sub,
                "href": f"{n}/{html_name}",
            })
    return found


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_groups(decks):
    groups = {}
    for d in decks:
        groups.setdefault((d["num"], d["title"]), []).append(d)

    parts = []
    for (num, title), items in sorted(groups.items()):
        items_html = "\n".join(f'''      <li>
        <a href="{esc(d['href'])}">
          <span class="deck-icon">S{num}</span>
          <span class="deck-info">
            <div class="deck-title">{esc(d['label'])}</div>
            <div class="deck-sub">{esc(d['sub'])}</div>
          </span>
        </a>
      </li>''' for d in items)
        parts.append(f'''  <div class="seance-group">
    <h2>{esc(title)}</h2>
    <ul class="decks">
{items_html}
    </ul>
  </div>''')
    return "\n\n".join(parts)


TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Slides — IMSV</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;1,400&family=Roboto+Slab:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root{{
    --accent:#1f5fbf;
    --h:#14304a;
    --muted:#5a6b7b;
    --rule:#e5e9ef;
    --page-bg:#ffffff;
    --text:#24313d;
    --card-bg:#f6f8fb;
    --card-brd:#e5e9ef;
    --hover-bg:#eef3fb;
  }}
  @media (prefers-color-scheme: dark){{
    :root{{
      --accent:#6ea8ff;
      --h:#e8eef6;
      --muted:#9db0c1;
      --rule:#26323d;
      --page-bg:#11171d;
      --text:#c7d2dc;
      --card-bg:#171f27;
      --card-brd:#2a3540;
      --hover-bg:#202b35;
    }}
  }}
  *{{box-sizing:border-box;}}
  body{{
    margin:0;
    background:var(--page-bg);
    color:var(--text);
    font-family:"Roboto", system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height:1.62;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap{{
    max-width:760px;
    margin:0 auto;
    padding:3.5rem 1.5rem 5rem;
  }}
  h1{{
    font-family:"Roboto Slab", Georgia, serif;
    font-weight:700;
    color:var(--h);
    letter-spacing:-0.005em;
    margin:0 0 .3rem;
    font-size:2rem;
  }}
  .subtitle{{
    color:var(--muted);
    margin:0 0 2.5rem;
    font-size:1.05rem;
  }}
  .seance-group{{
    margin-bottom:2.2rem;
  }}
  .seance-group h2{{
    font-family:"Roboto Slab", Georgia, serif;
    font-weight:600;
    color:var(--h);
    font-size:1.15rem;
    margin:0 0 .8rem;
    padding-top:0;
    border-top:none;
  }}
  ul.decks{{
    list-style:none;
    margin:0;
    padding:0;
    display:flex;
    flex-direction:column;
    gap:.7rem;
  }}
  ul.decks li a{{
    display:flex;
    align-items:center;
    gap:.9rem;
    padding:1rem 1.2rem;
    background:var(--card-bg);
    border:1px solid var(--card-brd);
    border-radius:.6rem;
    color:var(--text);
    text-decoration:none;
    transition:background .12s ease, border-color .12s ease;
  }}
  ul.decks li a:hover{{
    background:var(--hover-bg);
    border-color:var(--accent);
  }}
  .deck-icon{{
    flex:0 0 auto;
    width:2.1rem;
    height:2.1rem;
    border-radius:.4rem;
    background:var(--accent);
    color:#fff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:"Roboto Slab", Georgia, serif;
    font-weight:700;
    font-size:.95rem;
  }}
  .deck-info{{flex:1 1 auto; min-width:0;}}
  .deck-title{{
    font-weight:500;
    color:var(--h);
  }}
  .deck-sub{{
    color:var(--muted);
    font-size:.9rem;
    margin-top:.1rem;
  }}
  footer{{
    margin-top:3rem;
    padding-top:1.2rem;
    border-top:1px solid var(--rule);
    color:var(--muted);
    font-size:.85rem;
  }}
  footer a{{color:var(--accent);}}
</style>
</head>
<body>
<div class="wrap">
  <h1>Slides d'exercices</h1>
  <p class="subtitle">IMSV — supports de projection pour les séances d'exercices.</p>

{body}

  <footer>
    IMSV — Faculté des Sciences et Faculté de Médecine, Pharmacie et sciences Biomédicales, UMONS.
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    html = TEMPLATE.format(body=render_groups(find_decks()))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"écrit : {out}")
