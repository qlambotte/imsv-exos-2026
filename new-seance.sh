#!/usr/bin/env bash
# Crée une nouvelle séance à partir du modèle (seances/_modele/).
#
# Usage :  ./new-seance.sh <numéro> "Titre du thème"
#   ex.  ./new-seance.sh 2 "Fonctions et graphes"
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
N="${1:?Usage: ./new-seance.sh <numéro> \"Titre\"}"
TITRE="${2:?Usage: ./new-seance.sh <numéro> \"Titre\"}"
NN=$(printf "%02d" "$N")
DEST="$ROOT/seances/seance$NN"

[ -e "$DEST" ] && { echo "Existe déjà : $DEST (rien fait)"; exit 1; }
cp -r "$ROOT/seances/_modele" "$DEST"

# Remplace les marqueurs @@NN@@ et @@TITRE@@
grep -rl -e '@@NN@@' -e '@@TITRE@@' "$DEST" | while read -r f; do
  sed -i -e "s|@@NN@@|$NN|g" -e "s|@@TITRE@@|$TITRE|g" "$f"
done

cat <<EOF
✔ Séance créée : seances/seance$NN/

Étapes restantes (à la main) :
  1) Ajoute la séance au sommaire dans _quarto.yml, sous « chapters: » :

        - part: seances/seance$NN/index.qmd
          chapters:
            - seances/seance$NN/socle.qmd
            - seances/seance$NN/transfert.qmd
            - seances/seance$NN/supplementaires.qmd
            - seances/seance$NN/institution.qmd

  2) Rédige les exercices dans :
        seances/seance$NN/_socle.qmd            (socle)
        seances/seance$NN/_transfert.qmd        (transfert)
        seances/seance$NN/_supplementaires.qmd  (renforcement + dépassement)
     Numérotation CONTINUE : le transfert reprend après le dernier numéro du socle.
     Complète aussi index.qmd (objectifs, slides) et institution.qmd (méthode, auto-éval).

  3) Génère le QR (adapte l'URL réelle du site) :
        python3 make_qr.py "https://URL-du-site/seance$NN" img/qr-$NN.png

  4) Construis tout :
        ./build-all.sh
EOF
