#!/usr/bin/env bash
# Génère, pour une séance, les PDF depuis les mêmes fragments que le site :
#   pdf/<seance>-enonces.pdf   → énoncés seuls (aides retirées)  — TOUJOURS
#   pdf/<seance>-complet.pdf   → énoncés + aides (coups de pouce + solutions)
#   pdf/<seance>-offline.html  → tout le contenu, sans réseau (si _offline.qmd existe)
#
# Le complet et le hors-ligne (qui contiennent le corrigé) ne sont produits QUE si
# le corrigé des exos est activé. Ils sont retirés sinon. Le corrigé est masqué
# quand seances/<seance>/_metadata.yml contient « corrige-exos: false ».
#
# Usage :  ./build-pdf.sh [seance01]
#
# Le format typst est interdit dans un projet « book » : on rend la source
# d'assemblage (seances/<seance>/_pdf.qmd) dans une copie isolée « à plat ».
set -euo pipefail

SEANCE="${1:-seance01}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
DIR="$ROOT/seances/$SEANCE"
TMP="$ROOT/.pdfbuild"
OUT="$ROOT/pdf"

[ -f "$DIR/_pdf.qmd" ] || { echo "Introuvable : $DIR/_pdf.qmd"; exit 1; }

# Corrigé des exos actif ? (défaut : oui)
CORRIGE=1
if [ -f "$DIR/_metadata.yml" ] && grep -Eq '^[[:space:]]*corrige-exos:[[:space:]]*false' "$DIR/_metadata.yml"; then
  CORRIGE=0
fi

rm -rf "$TMP"; mkdir -p "$TMP" "$OUT"
[ -d "$ROOT/img" ] && cp -r "$ROOT/img" "$TMP/" || true   # img/ optionnel (supprimé avec les QR)
cp "$ROOT/exercice.lua" "$TMP/"
cp "$DIR"/_*.qmd "$TMP/"                       # _pdf, _consignes, _socle, _transfert…

# À plat : réécrit les chemins ../../ (img, exercice.lua) dans _pdf.qmd
sed -i -e 's#\.\./\.\./img/#img/#g' -e 's#\.\./\.\./exercice\.lua#exercice.lua#g' "$TMP/_pdf.qmd"

cd "$TMP"
echo "→ version énoncés seuls"
IMSV_ENONCES=1 quarto render "_pdf.qmd" --to typst --output "$SEANCE-enonces.pdf" >/dev/null
mv -f "$SEANCE-enonces.pdf" "$OUT/"

if [ "$CORRIGE" = 1 ]; then
  echo "→ version complète (énoncés + aides)"
  IMSV_ENONCES=0 quarto render "_pdf.qmd" --to typst --output "$SEANCE-complet.pdf" >/dev/null
  mv -f "$SEANCE-complet.pdf" "$OUT/"

  # --- Version HTML « hors-ligne » : un seul fichier autonome (CSS/JS/maths embarqués) ---
  if [ -f "$DIR/_offline.qmd" ]; then
    echo "→ version hors-ligne (HTML autonome)"
    cp "$ROOT/theme.scss" .
    # Hors-ligne : on retire l'@import Google Fonts pour zéro requête réseau.
    sed -i "/fonts\.googleapis\.com/d" theme.scss
    mkdir -p _includes && cp "$ROOT/_includes/aides.html" _includes/
    sed -i -e 's#\.\./\.\./theme\.scss#theme.scss#g' \
           -e 's#\.\./\.\./exercice\.lua#exercice.lua#g' \
           -e 's#\.\./\.\./_includes/aides\.html#_includes/aides.html#g' "_offline.qmd"
    IMSV_ENONCES=0 quarto render "_offline.qmd" --to html --output "$SEANCE-offline.html" >/dev/null
    mv -f "$SEANCE-offline.html" "$OUT/"
  fi
else
  echo "→ corrigé des exos masqué : ni PDF complet ni hors-ligne"
  rm -f "$OUT/$SEANCE-complet.pdf" "$OUT/$SEANCE-offline.html" || true
fi

cd "$ROOT"; rm -rf "$TMP"
echo "OK :"
echo "   $OUT/$SEANCE-enonces.pdf    (énoncés seuls)"
if [ "$CORRIGE" = 1 ]; then
  echo "   $OUT/$SEANCE-complet.pdf    (énoncés + aides)"
  [ -f "$OUT/$SEANCE-offline.html" ] && echo "   $OUT/$SEANCE-offline.html  (site hors-ligne, 1 fichier)"
fi
