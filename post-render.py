#!/usr/bin/env python3
"""Hook post-render de Quarto.

Garantit qu'une modification du CONTENU (donc du HTML) se répercute dans les PDF.
À chaque `quarto render`/`quarto preview`, régénère — DÈS QU'UNE SOURCE a changé —
les PDF de séance (énoncés, complet, hors-ligne), la feuille de méthodes et la
boîte à outils. Incrémental → rapide. IMSV_POSTRENDER évite toute réentrance.
"""
import glob
import os
import subprocess
import sys

if os.environ.get("IMSV_POSTRENDER"):
    sys.exit(0)

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
ENV = dict(os.environ, IMSV_POSTRENDER="1")


def newest(paths):
    return max([os.path.getmtime(p) for p in paths if os.path.exists(p)], default=0.0)


def stale(sources, target):
    if not os.path.exists(target):
        return True
    return newest(sources) > os.path.getmtime(target)


# --- Un PDF par séance (build-pdf.sh : énoncés + complet + hors-ligne) ---
for d in sorted(glob.glob("seances/seance*/")):
    s = os.path.basename(d.rstrip("/"))
    if not os.path.exists(os.path.join(d, "_pdf.qmd")):
        continue
    sources = glob.glob(os.path.join(d, "_*.qmd"))
    if stale(sources, f"pdf/{s}-complet.pdf"):
        print(f"[post-render] {s} : source modifiée → rebuild PDF + hors-ligne")
        subprocess.run(["./build-pdf.sh", s], check=True, env=ENV)

# --- Feuilles à compléter (build-methodes.sh) : chaque séance en ligne + la vierge ---
if os.path.exists("build-methodes.sh"):
    feuilles = glob.glob("seances/feuille-seance*.qmd") + ["seances/feuille-vierge.qmd"]
    if any(stale([q], f"pdf/{os.path.basename(q)[:-4]}.pdf") for q in feuilles if os.path.exists(q)):
        print("[post-render] feuilles de méthodes : source modifiée → rebuild")
        subprocess.run(["./build-methodes.sh"], check=True, env=ENV)

# --- Méthodes « remplies » par séance (build-boite.sh) : boucle sur les pages en ligne ---
if os.path.exists("build-boite.sh"):
    need = False
    for page in glob.glob("seances/methodes/seance*.qmd"):
        s = os.path.basename(page)[:-4]  # seance01, seance02, …
        if stale([f"seances/_methodes-{s}.qmd", "methode.lua"], f"pdf/methodes-{s}.pdf"):
            need = True
    if need:
        print("[post-render] méthodes (boîte) : source modifiée → rebuild")
        subprocess.run(["./build-boite.sh"], check=True, env=ENV)
