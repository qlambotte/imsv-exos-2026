#!/usr/bin/env bash
# Génère, pour CHAQUE séance en ligne ayant une page de méthodes
# (seances/methodes/seanceNN.qmd), le PDF « méthodes » rempli — UNE méthode par page :
#   pdf/methodes-seanceNN.pdf
# Source unique : seances/_methodes-seanceNN.qmd, mis en forme par methode.lua.
# Typst interdit dans un projet « book » : rendu dans une copie plate hors projet.
# Les séances hors ligne (préfixe « _ ») ne sont pas prises : rien de codé en dur.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/seances"; OUT="$ROOT/pdf"; TMP="$ROOT/.pdfbuild-boite"
mkdir -p "$OUT"
shopt -s nullglob
for page in "$SRC"/methodes/seance*.qmd; do
  S=$(basename "$page" .qmd)
  NUM=$(echo "$S" | sed 's/seance0*//')
  FRAG="$SRC/_methodes-$S.qmd"
  [ -f "$FRAG" ] || { echo "  (pas de fragment pour $S, ignoré)"; continue; }
  rm -rf "$TMP"; mkdir -p "$TMP"
  cp "$FRAG" "$TMP/_frag.qmd"; cp "$ROOT/methode.lua" "$TMP/"
  cat > "$TMP/_w.qmd" <<INNER
---
title: "Méthodes — Séance $NUM"
format:
  typst:
    papersize: a4
    margin: {x: 2cm, y: 2cm}
    toc: false
filters:
  - methode.lua
---

{{< include _frag.qmd >}}
INNER
  echo "→ méthodes $S"
  ( cd "$TMP" && quarto render "_w.qmd" --to typst --output "methodes-$S.pdf" >/dev/null )
  mv -f "$TMP/methodes-$S.pdf" "$OUT/"
done
rm -rf "$TMP"
echo "OK : pdf/methodes-*.pdf"
