#!/usr/bin/env bash
# Génère les feuilles de méthodes à compléter (PDF imprimables) :
#   - chaque séance en ligne : pdf/feuille-seanceNN.pdf  (seances/feuille-seanceNN.qmd)
#   - la feuille vierge       : pdf/feuille-vierge.pdf    (seances/feuille-vierge.qmd)
# Rien de codé en dur : on rend toutes les feuilles présentes (hors ligne = préfixe « _ »).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/seances"; OUT="$ROOT/pdf"; TMP="$ROOT/.pdfbuild-meth"
mkdir -p "$OUT"
shopt -s nullglob
for q in "$SRC"/feuille-seance*.qmd "$SRC"/feuille-vierge.qmd; do
  b=$(basename "$q" .qmd)
  rm -rf "$TMP"; mkdir -p "$TMP"; cp "$q" "$TMP/"
  echo "→ $b"
  ( cd "$TMP" && quarto render "$b.qmd" --to typst --output "$b.pdf" >/dev/null )
  mv -f "$TMP/$b.pdf" "$OUT/"
done
rm -rf "$TMP"
echo "OK : pdf/feuille-*.pdf"
