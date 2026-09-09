#!/usr/bin/env bash
# Génère la « feuille de méthodes à compléter » en PDF (feuille imprimable) :
#   pdf/feuille-methodes.pdf
#
# Usage :  ./build-methodes.sh
#
# Le format typst est interdit dans un projet « book » : on rend la source
# (seances/feuille-methodes.qmd, qui inclut _methodes-cadres.qmd) dans une copie
# isolée « à plat », hors du projet. N'affecte ni le site ni les PDF de séance.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/seances"
TMP="$ROOT/.pdfbuild-meth"
OUT="$ROOT/pdf"

[ -f "$SRC/feuille-methodes.qmd" ] || { echo "Introuvable : seances/feuille-methodes.qmd"; exit 1; }

rm -rf "$TMP"; mkdir -p "$TMP" "$OUT"
cp "$SRC/feuille-methodes.qmd" "$SRC/_methodes-cadres.qmd" "$TMP/"

cd "$TMP"
echo "→ feuille de méthodes (PDF à compléter)"
quarto render "feuille-methodes.qmd" --to typst --output "feuille-methodes.pdf" >/dev/null
mv -f "feuille-methodes.pdf" "$OUT/"

cd "$ROOT"; rm -rf "$TMP"
echo "OK : $OUT/feuille-methodes.pdf"
