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

for d in "$DEST" "$ROOT/seances/_seance$NN"; do
  [ -e "$d" ] && { echo "Existe déjà : $d (rien fait)"; exit 1; }
done
cp -r "$ROOT/seances/_modele" "$DEST"

# Remplace les marqueurs @@NN@@ (numéro sur 2 chiffres), @@N@@ (numéro) et @@TITRE@@
grep -rl -e '@@NN@@' -e '@@N@@' -e '@@TITRE@@' "$DEST" | while read -r f; do
  sed -i -e "s|@@NN@@|$NN|g" -e "s|@@N@@|$N|g" -e "s|@@TITRE@@|$TITRE|g" "$f"
done

# Fiches méthodes : cartes (source unique des titres), feuille à compléter, page de la boîte à outils.
MOD="$ROOT/seances/_modele-methodes"
while read -r src dst; do
  alt="$(dirname "$dst")/_$(basename "$dst")"          # version hors ligne (préfixe « _ »)
  if [ -e "$dst" ] || [ -e "$alt" ]; then echo "  (existe déjà, pas touché : $dst)"; continue; fi
  sed -e "s|@@NN@@|$NN|g" -e "s|@@N@@|$N|g" -e "s|@@TITRE@@|$TITRE|g" "$MOD/$src" > "$dst"
done <<LISTE
_methodes.qmd $ROOT/seances/_methodes-seance$NN.qmd
feuille.qmd $ROOT/seances/feuille-seance$NN.qmd
page.qmd $ROOT/seances/methodes/seance$NN.qmd
_corrige.qmd $ROOT/seances/methodes/_corrige-seance$NN.qmd
LISTE

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

     et, sous la partie « seances/methode.qmd », la page de méthodes :

            - seances/methodes/seance$NN.qmd

  2) Rédige les exercices dans :
        seances/seance$NN/_socle.qmd            (socle)
        seances/seance$NN/_transfert.qmd        (transfert)
        seances/seance$NN/_supplementaires.qmd  (renforcement)
     Numérotation AUTOMATIQUE (filtre exercice.lua) : par catégorie (Socle → S.1, S.2… ;
     Transfert → T.1… ; Renforcement → R.1…). Titre source « Exercice|Catégorie|niveau|Objectif »,
     SANS numéro écrit ; réordonner un exercice le renumérote tout seul.
     Complète aussi index.qmd (objectifs, slides) et institution.qmd (méthode, auto-éval).
     Écris les méthodes dans seances/_methodes-seance$NN.qmd (cartes) : la feuille à compléter
     (seances/feuille-seance$NN.qmd) en reprend les titres et objectifs toute seule.

  3) Construis tout :
        ./build-all.sh
EOF
