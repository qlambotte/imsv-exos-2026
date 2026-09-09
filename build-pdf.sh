#!/usr/bin/env bash
# Génère, pour une séance, DEUX PDF (une seule feuille chacun) depuis les mêmes
# fragments que le site :
#   pdf/<seance>-enonces.pdf   → énoncés seuls (aides retirées)
#   pdf/<seance>-complet.pdf   → énoncés + aides (coups de pouce + solutions)
#
# Usage :  ./build-pdf.sh [seance01]
#
# Le format typst est interdit dans un projet « book » : on rend la source
# d'assemblage (seances/<seance>/_pdf.qmd, qui inclut _consignes + _socle +
# _transfert) dans une copie isolée « à plat », hors du projet.
set -euo pipefail

SEANCE="${1:-seance01}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
DIR="$ROOT/seances/$SEANCE"
TMP="$ROOT/.pdfbuild"
OUT="$ROOT/pdf"

[ -f "$DIR/_pdf.qmd" ] || { echo "Introuvable : $DIR/_pdf.qmd"; exit 1; }

rm -rf "$TMP"; mkdir -p "$TMP" "$OUT"
cp -r "$ROOT/img" "$TMP/"
cp "$ROOT/exercice.lua" "$TMP/"
cp "$DIR"/_*.qmd "$TMP/"                       # _pdf, _consignes, _socle, _transfert…

# À plat : réécrit les chemins ../../ (img, exercice.lua) dans _pdf.qmd
sed -i -e 's#\.\./\.\./img/#img/#g' -e 's#\.\./\.\./exercice\.lua#exercice.lua#g' "$TMP/_pdf.qmd"

cd "$TMP"
echo "→ version complète (énoncés + aides)"
IMSV_ENONCES=0 quarto render "_pdf.qmd" --to typst --output "$SEANCE-complet.pdf" >/dev/null
echo "→ version énoncés seuls"
IMSV_ENONCES=1 quarto render "_pdf.qmd" --to typst --output "$SEANCE-enonces.pdf" >/dev/null

mv -f "$SEANCE-complet.pdf" "$SEANCE-enonces.pdf" "$OUT/"
cd "$ROOT"; rm -rf "$TMP"
echo "OK :"
echo "   $OUT/$SEANCE-enonces.pdf   (énoncés seuls)"
echo "   $OUT/$SEANCE-complet.pdf   (énoncés + aides)"
