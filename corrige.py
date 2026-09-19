#!/usr/bin/env python3
"""Affiche ou masque le CORRIGÉ d'une séance, indépendamment pour les exercices
ou pour les méthodes. La page reste toujours visible ; seuls les corrigés basculent.
Les feuilles à remplir (énoncés seuls / méthodes vierges) restent disponibles.

    python3 corrige.py 2 exos off       # site : énoncés seuls ; retire PDF complet + hors-ligne
    python3 corrige.py 2 exos on
    python3 corrige.py 2 methodes off   # masque le correctif des méthodes (HTML + PDF)
    python3 corrige.py 2 methodes on

Indépendant de seance-onoff.py : marche que la séance soit en ligne ou en préparation.
À lancer depuis la racine, puis : quarto render (ou ./build-all.sh).
"""
import os, re, sys

if len(sys.argv) != 4 or sys.argv[2] not in ("exos", "methodes") or sys.argv[3] not in ("on", "off"):
    sys.exit("Usage : python3 corrige.py <numéro> <exos|methodes> <on|off>")

num, part, action = int(sys.argv[1]), sys.argv[2], sys.argv[3]
nn = f"{num:02d}"
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

def variant(*cands):
    """Renvoie le chemin existant (avec ou sans « _ » de mise hors ligne)."""
    for c in cands:
        if os.path.exists(c):
            return c
    return cands[0]

def set_correction(path, value):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'^correction:\s*.*$', f'correction: "{value}"', s, count=1, flags=re.M)
    open(path, "w", encoding="utf-8").write(s)

def rm(path):
    """Suppression tolérante : n'interrompt pas le script si l'OS la refuse."""
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError as e:
            print(f"  (à supprimer à la main : {path} — {e.strerror})")

# ---------------------------------------------------------------- EXOS
if part == "exos":
    sdir = variant(f"seances/seance{nn}", f"seances/_seance{nn}")
    meta = os.path.join(sdir, "_metadata.yml")
    dl   = os.path.join(sdir, "_download.qmd")
    idx  = os.path.join(sdir, "index.qmd")

    DL_ON = """::: {.content-visible when-format="html"}
::: {.dl}
<details class="dl-menu">
<summary>Télécharger (PDF · hors-ligne)</summary>
<a href="../../pdf/seance@@NN@@-enonces.pdf">Énoncés seuls (PDF)</a>
<a href="../../pdf/seance@@NN@@-complet.pdf">Énoncés + coups de pouce &amp; corrections (PDF)</a>
<a href="../../pdf/seance@@NN@@-offline.html" download>Corrections hors-ligne — 1 fichier (à garder)</a>
</details>
:::
:::
""".replace("@@NN@@", nn)

    DL_OFF = """::: {.content-visible when-format="html"}
::: {.dl}
<details class="dl-menu">
<summary>Télécharger (PDF)</summary>
<a href="../../pdf/seance@@NN@@-enonces.pdf">Énoncés seuls (PDF)</a>
</details>
:::
:::

::: {.callout-note appearance="simple"}
Le corrigé (coups de pouce + solutions) sera publié après la séance.
:::
""".replace("@@NN@@", nn)

    if action == "off":
        open(meta, "w", encoding="utf-8").write("corrige-exos: false\n")
        open(dl, "w", encoding="utf-8").write(DL_OFF)
        set_correction(idx, "à venir")
        rm(f"pdf/seance{nn}-complet.pdf")
        rm(f"pdf/seance{nn}-offline.html")
        print(f"Corrigé EXOS séance {nn} : MASQUÉ (site énoncés seuls ; PDF complet + hors-ligne retirés).")
    else:
        open(meta, "w", encoding="utf-8").write("corrige-exos: true\n")
        open(dl, "w", encoding="utf-8").write(DL_ON)
        set_correction(idx, "✅ en ligne")
        print(f"Corrigé EXOS séance {nn} : VISIBLE.")

# ---------------------------------------------------------------- METHODES
else:
    page  = variant(f"seances/methodes/seance{nn}.qmd", f"seances/methodes/_seance{nn}.qmd")
    relay = f"seances/methodes/_corrige-seance{nn}.qmd"
    frag_on, frag_off = f"seances/_methodes-seance{nn}.qmd", f"seances/_methodes-seance{nn}.qmd.off"

    RELAY_ON = """::: {.content-visible when-format="html"}
::: {.dl}
<details class="dl-menu">
<summary>Télécharger — correctif (PDF)</summary>
<a href="../../pdf/methodes-seance@@NN@@.pdf">Méthodes de la séance — correctif (PDF)</a>
</details>
:::
:::

{{< include ../_methodes-seance@@NN@@.qmd >}}
""".replace("@@NN@@", nn)

    RELAY_OFF = """::: {.callout-note appearance="simple"}
Le correctif des méthodes sera publié après la séance. La **feuille à compléter** reste disponible ci-dessus.
:::
"""

    if action == "off":
        open(relay, "w", encoding="utf-8").write(RELAY_OFF)
        if os.path.exists(frag_on):
            os.rename(frag_on, frag_off)
        set_correction(page, "à venir")
        rm(f"pdf/methodes-seance{nn}.pdf")
        print(f"Correctif MÉTHODES séance {nn} : MASQUÉ (page + PDF retirés ; feuille à compléter conservée).")
    else:
        open(relay, "w", encoding="utf-8").write(RELAY_ON)
        if os.path.exists(frag_off):
            os.rename(frag_off, frag_on)
        set_correction(page, "✅ en ligne")
        print(f"Correctif MÉTHODES séance {nn} : VISIBLE.")

print("→ lance maintenant : quarto render  (ou ./build-all.sh)")
