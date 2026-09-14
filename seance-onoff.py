#!/usr/bin/env python3
"""Met une séance HORS LIGNE (préfixe « _ » : invisible dans le menu, les listes
et par URL) ou la REMET EN LIGNE. Rien n'est supprimé : on renomme les fichiers,
et on commente / décommente son bloc dans _quarto.yml (marqueur « #OFFnn# »).

    python3 seance.py 2 off     # séance 2 hors ligne (préparation)
    python3 seance.py 2 on      # séance 2 de nouveau en ligne

À lancer depuis la racine du dépôt, puis : quarto render (+ git add/commit).
"""
import os, re, sys

if len(sys.argv) != 3 or sys.argv[2] not in ("off", "on"):
    sys.exit("Usage : python3 seance.py <numéro> <off|on>")

num, action = int(sys.argv[1]), sys.argv[2]
nn = f"{num:02d}"
YML = "_quarto.yml"
MARK = f"#OFF{nn}# "

# --- 1) Renommer là où c'est pertinent (ajouter / retirer le « _ ») ---
paths = [
    f"seances/seance{nn}",                # dossier de la séance (exercices)
    f"seances/methodes/seance{nn}.qmd",   # page « méthodes » de la séance
    f"seances/feuille-seance{nn}.qmd",    # feuille à compléter de la séance
]
for p in paths:
    d, b = os.path.split(p)
    u = os.path.join(d, "_" + b)
    if action == "off" and os.path.exists(p):
        os.rename(p, u); print(f"hors ligne : {p} -> {u}")
    if action == "on" and os.path.exists(u):
        os.rename(u, p); print(f"en ligne  : {u} -> {p}")

# --- 2) Commenter / décommenter le bloc dans _quarto.yml ---
lines = open(YML, encoding="utf-8").read().splitlines()
part_re = re.compile(rf"^(\s*)- part:\s*seances/seance{nn}/index\.qmd\s*$")
meth_re = re.compile(rf"^\s*- seances/methodes/seance{nn}\.qmd\s*$")

if action == "off":
    res, i = [], 0
    while i < len(lines):
        l = lines[i]
        m = part_re.match(l)
        if m and MARK not in l:                       # bloc « - part: …seanceNN/index.qmd »
            indent = len(m.group(1))
            res.append(re.sub(r"^(\s*)", r"\g<1>" + MARK, l)); i += 1
            while i < len(lines) and lines[i].strip() and \
                  (len(lines[i]) - len(lines[i].lstrip())) > indent:   # ses « chapters: »
                res.append(re.sub(r"^(\s*)", r"\g<1>" + MARK, lines[i])); i += 1
            continue
        if meth_re.match(l) and MARK not in l:        # ligne « - seances/methodes/seanceNN.qmd »
            res.append(re.sub(r"^(\s*)", r"\g<1>" + MARK, l)); i += 1; continue
        res.append(l); i += 1
    lines = res
else:                                                 # on : on retire le marqueur
    lines = [l.replace(MARK, "", 1) for l in lines]

open(YML, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"_quarto.yml : séance {nn} {'commentée (hors ligne)' if action=='off' else 'réactivée'}.")
print("→ lance maintenant : quarto render")
