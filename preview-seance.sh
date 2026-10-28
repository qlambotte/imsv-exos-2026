#!/usr/bin/env bash
# Prévisualise les pages d'une séance SANS toucher au dépôt, qu'elle soit en ligne ou hors ligne.
#
#   bash preview-seance.sh 6            # toute la séance 6 (page d'accueil, liens entre pages)
#   bash preview-seance.sh 6 socle      # ouvre directement socle.qmd
#   bash preview-seance.sh 5 transfert --no-browser
#
# Le dossier de la séance (seances/seanceNN ou seances/_seanceNN) est recopié dans un dossier
# temporaire, avec les filtres, le thème et les includes, et un _quarto.yml minimal y est créé.
# Quarto rend donc dans ce dossier temporaire : aucun déchet (.quarto/, *_files/, *.html) dans le
# dépôt, et pas besoin de seance-onoff.py.
#
# Aperçu DYNAMIQUE : tant que le preview tourne, une boucle recopie chaque seconde les fichiers
# modifiés du dépôt vers le dossier temporaire ; Quarto détecte la copie et rafraîchit la page.
# Ne pas passer --no-watch-inputs : cette option empêche justement le nouveau rendu.
# Le PDF des énoncés (comme build-pdf.sh, mais dans le dossier temporaire) est produit au
# lancement puis refait après chaque modification d'un fragment, d'une figure ou du filtre ;
# le lien « Énoncés seuls (PDF) » de la séance pointe vers lui. Les autres liens vers le reste
# du livre (boîte à outils, PDF complet) ne marchent pas dans cet aperçu.
# Ctrl+C arrête le preview et la boucle.
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage : bash preview-seance.sh <numéro> [page] [options de quarto preview]" >&2
  exit 1
fi
NN=$(printf '%02d' "$1"); shift
PAGE=""
if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then PAGE="$1"; shift; fi

ROOT=$(cd "$(dirname "$0")" && pwd)
src_dir() {   # la séance peut changer de nom (seance-onoff.py) pendant le preview
  if [ -d "$ROOT/seances/seance$NN" ]; then echo "$ROOT/seances/seance$NN"
  else echo "$ROOT/seances/_seance$NN"; fi
}
[ -d "$(src_dir)" ] || { echo "Séance $NN introuvable dans seances/." >&2; exit 1; }

TMP="${TMPDIR:-/tmp}/imsv-preview-$NN"
DIR="$TMP/seances/seance$NN"
rm -rf "$TMP"
mkdir -p "$DIR"

# Copie incrémentale : ne recopie qu'un fichier nouveau ou plus récent que sa copie
# (cp -u), sans les restes de rendus éventuels présents dans le dépôt.
# Quarto ne re-rend une page que si CE fichier change : quand un fragment (_socle.qmd…) ou une
# image change, on « touche » donc les pages qui l'incluent (toutes les pages pour une image,
# un filtre ou le thème), ce qui déclenche le nouveau rendu et le rafraîchissement du navigateur.
pages_touch() {   # $1 = nom du fichier modifié (vide = toutes les pages)
  local p
  for p in "$DIR"/*.qmd; do
    case "$(basename "$p")" in _*) continue ;; esac
    if [ -z "$1" ] || grep -q "include $1" "$p"; then touch "$p"; fi
  done
}
# PDF des énoncés seuls : même recette que build-pdf.sh (copie « à plat » + typst), hors dépôt.
build_pdf() {
  local B="$TMP/pdfbuild" out="seance$NN-enonces.pdf"
  rm -rf "$B"; mkdir -p "$B/img"
  cp "$TMP/exercice.lua" "$B/"
  cp "$DIR"/_*.qmd "$B/"
  cp "$DIR"/img/*.svg "$B/img/" 2>/dev/null || true
  sed -i -e 's#\.\./\.\./img/#img/#g' -e 's#\.\./\.\./exercice\.lua#exercice.lua#g' "$B/_pdf.qmd"
  if (cd "$B" && IMSV_ENONCES=1 quarto render _pdf.qmd --to typst --output "$out" >"$TMP/pdf.log" 2>&1); then
    cp "$B/$out" "$DIR/$out"; mkdir -p "$DIR/_site"; cp "$B/$out" "$DIR/_site/$out"
    echo "[preview] PDF des énoncés mis à jour : $DIR/$out"
  else
    echo "[preview] Échec du PDF des énoncés : voir $TMP/pdf.log"
  fi
}
# Le lien de téléchargement des énoncés vise ../../pdf/ dans le livre : dans l'aperçu, il vise
# le PDF produit à côté des pages.
fix_download() {
  [ -f "$DIR/_download.qmd" ] && sed -i "s#\.\./\.\./pdf/seance$NN-enonces\.pdf#seance$NN-enonces.pdf#g" "$DIR/_download.qmd" || true
}
sync_once() {
  local s changed=() f c; s=$(src_dir)
  while IFS= read -r -d '' f; do
    mkdir -p "$DIR/$(dirname "$f")"
    if [ ! -e "$DIR/$f" ] || [ "$s/$f" -nt "$DIR/$f" ]; then
      cp -p "$s/$f" "$DIR/$f"; changed+=("${f#./}")
      [ "${f#./}" = "_download.qmd" ] && fix_download
    fi
  done < <(cd "$s" && find . -type f \
      ! -name '_quarto.yml' ! -name '*.html' ! -path './.quarto/*' ! -path '*_files/*' -print0)
  for f in exercice.lua methode.lua theme.scss; do
    if [ ! -e "$TMP/$f" ] || [ "$ROOT/$f" -nt "$TMP/$f" ]; then cp -p "$ROOT/$f" "$TMP/$f"; changed+=("$f"); fi
  done
  mkdir -p "$TMP/_includes"
  for f in "$ROOT"/_includes/*; do
    c="$TMP/_includes/$(basename "$f")"
    if [ ! -e "$c" ] || [ "$f" -nt "$c" ]; then cp -p "$f" "$c"; changed+=("_includes"); fi
  done
  if [ -d "$ROOT/fonts" ]; then mkdir -p "$TMP/fonts"; cp -rup "$ROOT/fonts/." "$TMP/fonts/"; fi
  for f in ${changed[@]+"${changed[@]}"}; do
    case "$f" in _*.qmd|img/*|exercice.lua) touch "$TMP/pdf.todo" ;; esac
  done
  [ "${FIRST:-0}" = 1 ] && return 0
  for f in ${changed[@]+"${changed[@]}"}; do
    case "$f" in
      _*.qmd) pages_touch "$f" ;;          # fragment : les pages qui l'incluent
      *.qmd)  : ;;                         # page : Quarto la voit déjà
      *)      pages_touch "" ;;            # image, filtre, thème, includes : toutes les pages
    esac
  done
}
FIRST=1 sync_once

# Mêmes réglages HTML que le livre (_quarto.yml de la racine), sans la structure « book ».
# Type « website » : toutes les pages de la séance sont rendues et les liens .qmd → .html résolus.
cat > "$DIR/_quarto.yml" <<YML
project:
  type: website
  resources:
    - "*.pdf"
website:
  title: "Séance $NN — aperçu"
lang: fr
format:
  html:
    theme:
      - cosmo
      - ../../theme.scss
    include-in-header:
      - ../../_includes/theme-init.html
    include-after-body:
      - ../../_includes/aides.html
      - ../../_includes/tools.html
    toc: true
    toc-title: "Sur cette page"
    toc-depth: 3
    number-sections: false
    html-math-method: mathml
    fig-cap-location: bottom
YML

# Boucle de synchronisation en arrière-plan, arrêtée avec le preview.
# Elle refait aussi le PDF des énoncés quand un fragment, une figure ou le filtre a changé.
( while true; do
    if [ -e "$TMP/pdf.todo" ]; then rm -f "$TMP/pdf.todo"; build_pdf; fi
    sleep 1
    sync_once 2>/dev/null || true
  done ) &
SYNC=$!
trap 'kill "$SYNC" 2>/dev/null || true' EXIT INT TERM

cd "$DIR"
if [ -n "$PAGE" ]; then
  quarto preview "${PAGE%.qmd}.qmd" "$@"
else
  quarto preview "$@"
fi
