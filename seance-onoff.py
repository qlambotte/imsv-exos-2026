#!/usr/bin/env python3
"""Met une séance HORS LIGNE (préfixe « _ ») ou EN LIGNE, et gère son STATUT
d'affichage dans le tableau d'accueil (« à relire », « en construction »…).

    python3 seance-onoff.py 2 off "à relire"        # hors ligne + étiquette
    python3 seance-onoff.py 3 off "en construction"
    python3 seance-onoff.py 2 on                     # remet en ligne (ne touche PAS l'étiquette)
    python3 seance-onoff.py 2 statut "à relire"      # change juste l'étiquette
    python3 seance-onoff.py 2 statut prête           # efface l'étiquette (redevient « en ligne »)

L'étiquette est stockée dans _seances-statut.yml, indépendante du on/off (pour survivre
à la réactivation « prof » du deploy). À lancer depuis la racine, puis quarto render / ./deploy.sh.
"""
import os, re, sys

STATUT_FILE = "_seances-statut.yml"
CLEAR = {"", "prête", "prete", "prêt", "-", "none", "en ligne"}

def read_statut():
    d = {}
    if os.path.exists(STATUT_FILE):
        for line in open(STATUT_FILE, encoding="utf-8"):
            if line.strip().startswith("#"):
                continue
            m = re.match(r"\s*(\d+)\s*:\s*(.+?)\s*$", line)
            if m:
                d[int(m.group(1))] = m.group(2).strip().strip('"').strip("'")
    return d

def write_statut(d):
    head = ("# Statut des séances EN PRÉPARATION (num: étiquette). Séance absente = prête.\n"
            "# Géré par seance-onoff.py.\n")
    open(STATUT_FILE, "w", encoding="utf-8").write(head + "".join(f"{n}: {d[n]}\n" for n in sorted(d)))

def set_statut(num, label):
    d = read_statut()
    if label is None or label.strip().lower() in CLEAR:
        d.pop(num, None); print(f"statut : séance {num} → prête (étiquette retirée)")
    else:
        d[num] = label.strip(); print(f"statut : séance {num} → « {label.strip()} »")
    write_statut(d)

if len(sys.argv) < 3 or sys.argv[2] not in ("off", "on", "statut"):
    sys.exit('Usage : python3 seance-onoff.py <numéro> <on|off|statut> [étiquette]')
num, action = int(sys.argv[1]), sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 else None
nn = f"{num:02d}"

if action == "statut":
    set_statut(num, label if label is not None else "")
    sys.exit(0)

# --- on/off : renommage + _quarto.yml ---
YML, MARK = "_quarto.yml", f"#OFF{nn}# "
paths = [f"seances/seance{nn}", f"seances/methodes/seance{nn}.qmd", f"seances/feuille-seance{nn}.qmd"]
for p in paths:
    d, b = os.path.split(p); u = os.path.join(d, "_" + b)
    if action == "off" and os.path.exists(p): os.rename(p, u); print(f"hors ligne : {p} -> {u}")
    if action == "on"  and os.path.exists(u): os.rename(u, p); print(f"en ligne  : {u} -> {p}")

lines = open(YML, encoding="utf-8").read().splitlines()
part_re = re.compile(rf"^(\s*)- part:\s*seances/seance{nn}/index\.qmd\s*$")
meth_re = re.compile(rf"^\s*- seances/methodes/seance{nn}\.qmd\s*$")
if action == "off":
    res, i = [], 0
    while i < len(lines):
        l = lines[i]; m = part_re.match(l)
        if m and MARK not in l:
            indent = len(m.group(1)); res.append(re.sub(r"^(\s*)", r"\g<1>" + MARK, l)); i += 1
            while i < len(lines) and lines[i].strip() and (len(lines[i]) - len(lines[i].lstrip())) > indent:
                res.append(re.sub(r"^(\s*)", r"\g<1>" + MARK, lines[i])); i += 1
            continue
        if meth_re.match(l) and MARK not in l:
            res.append(re.sub(r"^(\s*)", r"\g<1>" + MARK, l)); i += 1; continue
        res.append(l); i += 1
    lines = res
else:
    lines = [l.replace(MARK, "", 1) for l in lines]
open(YML, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"_quarto.yml : séance {nn} {'commentée (hors ligne)' if action == 'off' else 'réactivée'}.")

if action == "off" and label is not None:
    set_statut(num, label)
print("→ lance maintenant : quarto render  (ou ./deploy.sh)")
