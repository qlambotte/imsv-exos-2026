#!/usr/bin/env bash
# Prévisualise le deck d'une séance SANS toucher au dépôt, qu'il soit en ligne ou hors ligne
# (slides/seanceNN ou slides/_seanceNN : Quarto ignore les dossiers qui commencent par « _ »).
#
#   bash preview-slides.sh 6              # le seul deck .qmd de slides/_seance06 (ou slides/seance06)
#   bash preview-slides.sh 6 modeles      # un deck précis
#   bash preview-slides.sh 6 modeles --no-browser
#
# Le dossier du deck et slides/seance01 (thème, annotate.html, _travail.md, _minuteur.md) sont
# recopiés dans un dossier temporaire, avec le _quarto.yml de slides/. Une boucle recopie chaque
# seconde les fichiers modifiés : Quarto rafraîchit le navigateur. Ctrl+C arrête tout.
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage : bash preview-slides.sh <numéro> [deck] [options de quarto preview]" >&2
  exit 1
fi
NN=$(printf '%02d' "$1"); shift
DECK=""
if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then DECK="${1%.qmd}"; shift; fi

ROOT=$(cd "$(dirname "$0")" && pwd)/slides
src_dir() {
  if [ -d "$ROOT/seance$NN" ]; then echo "$ROOT/seance$NN"; else echo "$ROOT/_seance$NN"; fi
}
[ -d "$(src_dir)" ] || { echo "Slides de la séance $NN introuvables dans slides/." >&2; exit 1; }

if [ -z "$DECK" ]; then
  mapfile -t decks < <(cd "$(src_dir)" && ls *.qmd 2>/dev/null | grep -v '^_' || true)
  if [ "${#decks[@]}" -ne 1 ]; then
    echo "Précise le deck parmi : ${decks[*]:-aucun}" >&2; exit 1
  fi
  DECK="${decks[0]%.qmd}"
fi

TMP="${TMPDIR:-/tmp}/imsv-slides-$NN"
rm -rf "$TMP"; mkdir -p "$TMP/seance$NN" "$TMP/seance01"
cp "$ROOT/_quarto.yml" "$TMP/"

# Copie incrémentale ; un fichier inclus (_travail.md…) qui change fait « toucher » le deck.
sync_dir() {   # $1 = source, $2 = destination ; affiche 1 si un fichier a changé
  local s="$1" d="$2" f any=0
  while IFS= read -r -d '' f; do
    mkdir -p "$d/$(dirname "$f")"
    if [ ! -e "$d/$f" ] || [ "$s/$f" -nt "$d/$f" ]; then cp -p "$s/$f" "$d/$f"; any=1; fi
  done < <(cd "$s" && find . -type f \( ! -name '*.html' -o -name 'annotate.html' \) \
             ! -path './.quarto/*' ! -path '*_files/*' -print0)
  echo "$any"
}
sync_once() {
  local a b
  a=$(sync_dir "$(src_dir)" "$TMP/seance$NN")
  b=$(sync_dir "$ROOT/seance01" "$TMP/seance01")
  if [ "$b" = 1 ] && [ "${FIRST:-0}" != 1 ]; then touch "$TMP/seance$NN/$DECK.qmd"; fi
  return 0
}
FIRST=1 sync_once
[ -f "$TMP/seance$NN/$DECK.qmd" ] || { echo "Deck $DECK.qmd introuvable." >&2; exit 1; }

( while true; do sleep 1; sync_once 2>/dev/null || true; done ) &
SYNC=$!
trap 'kill "$SYNC" 2>/dev/null || true' EXIT INT TERM

cd "$TMP"
quarto preview "seance$NN/$DECK.qmd" "$@"
