#!/usr/bin/env bash
# Construit tout le site en une commande :
#   1) (option) régénère les QR de chaque séance depuis BASE_URL ;
#   2) génère les 2 PDF de chaque séance ;
#   3) rend le site (_book/).
#
# Usage :  ./build-all.sh            (tout)
#          ./build-all.sh --no-qr    (sans régénérer les QR)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# >>> À ADAPTER : base de l'URL publique du site (sans slash final) <<<
BASE_URL="https://github.com/qlambotte/imsv-exos-2026/"

DO_QR=1
[ "${1:-}" = "--no-qr" ] && DO_QR=0

for d in seances/seance*/; do
  s=$(basename "$d")                 # ex. seance01
  [ -f "$d/_pdf.qmd" ] || continue
  num=${s#seance}                    # ex. 01

  if [ "$DO_QR" = 1 ]; then
    echo "→ QR $s"
    python3 make_qr.py "$BASE_URL/$s" "img/qr-$num.png" >/dev/null || \
      echo "  (QR non régénéré — vérifie make_qr.py / l'URL)"
  fi

  echo "→ PDF $s"
  ./build-pdf.sh "$s" >/dev/null
done

echo "→ Site"
quarto render >/dev/null

echo ""
echo "✔ Terminé : site dans _book/ , PDF dans pdf/"
