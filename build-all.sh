#!/usr/bin/env bash
# Construit tout le site en une commande, de façon INCRÉMENTALE :
#   1) PDF (+ version hors-ligne) de chaque séance, feuilles de méthodes, méthodes remplies :
#      seuls ceux dont une source a changé sont reconstruits (cache par empreinte de contenu,
#      voir incremental.py) ;
#   2) rend le site (_book/).
#
# Usage :  ./build-all.sh            (incrémental)
#          ./build-all.sh --force    (tout reconstruire, cache ignoré en lecture)
#
# Note : le hook post-render de Quarto (post-render.py) appelle le même moteur à chaque
# `quarto render` complet ; ici on le passe d'abord, puis on rend le site sans relancer le hook.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

case "${1:-}" in
  "") ;;
  --force) export IMSV_FORCE=1 ;;
  *) echo "Usage : ./build-all.sh [--force]" >&2; exit 2 ;;
esac

echo "→ PDF, feuilles de méthodes, boîte à outils"
python3 incremental.py assets

echo "→ Site"
IMSV_POSTRENDER=1 quarto render >/dev/null

echo ""
echo "✔ Terminé : site dans _book/ , PDF et hors-ligne dans pdf/"
