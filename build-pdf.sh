#!/usr/bin/env bash
# Génère, pour une séance, DEUX PDF (une seule feuille chacun) depuis les mêmes
# fragments que le site :
#   pdf/<seance>-enonces.pdf   → énoncés seuls (aides retirées)
#   pdf/<seance>-complet.pdf   → énoncés + aides (coups de pouce + solutions)
# et, si _offline.qmd existe, UN fichier HTML autonome (hors-ligne) :
#   pdf/<seance>-offline.html  → tout le contenu + coups de pouce, sans réseau
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

# --- Version HTML « hors-ligne » : un seul fichier autonome (CSS/JS/maths embarqués) ---
# Additif : n'affecte en rien les deux PDF ci-dessus. Ne tourne que si _offline.qmd existe.
if [ -f "$DIR/_offline.qmd" ]; then
  echo "→ version hors-ligne (HTML autonome)"
  cp "$ROOT/theme.scss" .
  # Hors-ligne : on retire l'@import Google Fonts pour zéro requête réseau ;
  # les polices système prennent le relais. Le thème du SITE (theme.scss) n'est pas touché.
  sed -i "/fonts\.googleapis\.com/d" theme.scss
  mkdir -p _includes && cp "$ROOT/_includes/aides.html" _includes/
  sed -i -e 's#\.\./\.\./theme\.scss#theme.scss#g' \
         -e 's#\.\./\.\./exercice\.lua#exercice.lua#g' \
         -e 's#\.\./\.\./_includes/aides\.html#_includes/aides.html#g' "_offline.qmd"
  IMSV_ENONCES=0 quarto render "_offline.qmd" --to html --output "$SEANCE-offline.html" >/dev/null
  mv -f "$SEANCE-offline.html" "$OUT/"
fi

cd "$ROOT"; rm -rf "$TMP"
echo "OK :"
echo "   $OUT/$SEANCE-enonces.pdf    (énoncés seuls)"
echo "   $OUT/$SEANCE-complet.pdf    (énoncés + aides)"
[ -f "$OUT/$SEANCE-offline.html" ] && echo "   $OUT/$SEANCE-offline.html  (site hors-ligne, 1 fichier)"
