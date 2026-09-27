#!/usr/bin/env python3
"""Feuille de méthodes à compléter : remplace la ligne « // @@METHODES@@ » d'une feuille
(seances/feuille-seanceNN.qmd) par une page par méthode, avec le titre et l'objectif lus dans
les cartes de méthode de la séance (seances/_methodes-seanceNN.qmd, ou .qmd.off si le correctif
est masqué). Une seule source : renommer une méthode la renomme aussi sur la feuille.

    python3 feuille-auto.py seances/feuille-seance04.qmd > copie.qmd

Appelé par build-methodes.sh. Une feuille sans la ligne « // @@METHODES@@ » est recopiée telle quelle.
"""
import os, re, sys

MARK = "// @@METHODES@@"
feuille = sys.argv[1]
src = open(feuille, encoding="utf-8").read()
if MARK not in src:
    sys.stdout.write(src); sys.exit(0)

m = re.search(r"feuille-seance(\d+)\.qmd$", feuille)
if not m:
    sys.exit(f"feuille-auto : numéro de séance introuvable dans {feuille}")
d = os.path.dirname(os.path.abspath(feuille))
frag = next((p for p in (os.path.join(d, f"_methodes-seance{m.group(1)}.qmd"),
                         os.path.join(d, f"_methodes-seance{m.group(1)}.qmd.off")) if os.path.exists(p)), None)
if frag is None:
    sys.exit(f"feuille-auto : pas de cartes de méthode pour {feuille}")

def typ(s):  # chaîne typst
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

pages = []
for line in open(frag, encoding="utf-8"):
    if re.match(r"^:::+\s*\{\.methode\b", line):
        t = re.search(r'titre="([^"]*)"', line)
        o = re.search(r'obj="([^"]*)"', line)
        pages.append(f"#page_methode({typ(t.group(1) if t else '')}, {typ(o.group(1) if o else '')})")
if not pages:
    sys.exit(f"feuille-auto : aucune carte « .methode » dans {frag}")

out = []
for line in src.splitlines(keepends=True):
    if line.strip().startswith(MARK):
        out.append("\n#pagebreak()\n".join(pages) + "\n")
    else:
        out.append(line)
sys.stdout.write("".join(out))
