#!/usr/bin/env bash
# Construit tout le site en une commande :
#   1) génère les 2 PDF (+ version hors-ligne) de chaque séance ;
#   2) génère la feuille de méthodes ;
#   3) rend le site (_book/).
#
# Note : le hook post-render de Quarto (post-render.sh) régénère déjà chaque PDF
# dont une source a changé, à chaque `quarto render`. Ce script force, lui, une
# reconstruction complète.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# Auto-guérison : un `git worktree add` (voir deploy.sh) peut extraire ces scripts
# sans leur bit exécutable si git ne l'a pas enregistré. On le remet ici à chaque
# lancement, pour ne plus jamais retomber sur « Permission non accordée ».
chmod +x build-pdf.sh build-methodes.sh build-boite.sh 2>/dev/null || true

for d in seances/seance*/; do
  s=$(basename "$d")
  [ -f "$d/_pdf.qmd" ] || continue
  echo "→ PDF $s"
  ./build-pdf.sh "$s" >/dev/null
done

echo "→ Feuille méthodes"
./build-methodes.sh >/dev/null

echo "→ Boîte à outils"
./build-boite.sh >/dev/null

echo "→ Site"
quarto render >/dev/null

echo ""
echo "✔ Terminé : site dans _book/ , PDF et hors-ligne dans pdf/"
