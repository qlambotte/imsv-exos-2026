#!/usr/bin/env bash
# deploy.sh — publie sur gh-pages, depuis la branche courante (main), DEUX vues :
#   /       = site étudiant  (séances prêtes ; les séances en cours, préfixe « _ », exclues)
#   /prof/  = vue prof complète (TOUTES les séances activées, y compris celles en cours),
#             NON référencée depuis le site étudiant.
#
# Une seule branche, pas de bascule à la main. Chaque vue est rendue dans un WORKTREE
# ISOLÉ : ton arbre de travail n'est jamais touché et le cache .quarto ne se mélange pas
# (c'était la cause de l'erreur « Deno.cwd() »).
#
# Usage :  ./deploy.sh      (depuis main)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"; cd "$ROOT"
BASE_URL="https://qlambotte.github.io/imsv-exos-2026"

rm -f .git/index.lock 2>/dev/null || true
git rev-parse --verify -q gh-pages >/dev/null || { echo "✗ branche gh-pages absente." >&2; exit 1; }

STAGE="$(mktemp -d)"; WTS=()
cleanup(){
  for w in "${WTS[@]:-}"; do [ -n "$w" ] && git worktree remove --force "$w" 2>/dev/null || true; done
  rm -rf "$STAGE"; git worktree prune 2>/dev/null || true
}
trap cleanup EXIT

build_view(){   # $1 = student|prof ; $2 = sous-dossier de destination ("" ou "prof")
  local mode="$1" dest="$STAGE${2:+/$2}" wt
  wt="$(mktemp -d)"; WTS+=("$wt")
  echo "→ rendu ($mode)"
  git worktree add --detach "$wt" HEAD >/dev/null
  (
    cd "$wt"
    if [ "$mode" = prof ]; then
      # active toutes les séances en cours (dossiers seances/_seanceNN)
      for d in seances/_seance[0-9][0-9]; do
        [ -e "$d" ] || continue
        n=$(basename "$d" | sed 's/^_seance0*//')
        python3 seance-onoff.py "$n" on >/dev/null
      done
      # site-url sous /prof pour des liens cohérents dans la vue prof
      sed -i 's#imsv-exos-2026/"#imsv-exos-2026/prof/"#' _quarto.yml
    fi
    ./build-all.sh >/dev/null
  )
  mkdir -p "$dest"; cp -a "$wt/_book/." "$dest"/
  git worktree remove --force "$wt"
}

build_view student ""     # site étudiant  -> racine
build_view prof   "prof"  # vue prof       -> /prof

# slides/ : deck(s) reveal.js autonomes, HORS pipeline Quarto (pas un chapitre, pas une
# ressource du livre) -> copiés tels quels, verbatim, depuis le répertoire de travail.
# Volontairement non référencés dans le livre/menus : accessibles seulement par lien direct.
if [ -d "$ROOT/slides" ]; then
  echo "→ copie slides/ (verbatim, hors pipeline Quarto)"
  mkdir -p "$STAGE/slides"
  cp -a "$ROOT/slides/." "$STAGE/slides"/
fi

echo "→ publication gh-pages"
WGH="$(mktemp -d)"; WTS+=("$WGH")
git fetch -q origin gh-pages || true
git worktree add --force "$WGH" gh-pages >/dev/null
git -C "$WGH" reset -q --hard origin/gh-pages 2>/dev/null || true
find "$WGH" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -a "$STAGE/." "$WGH"/
touch "$WGH/.nojekyll"
git -C "$WGH" add -A
git -C "$WGH" commit -q -m "Deploy : étudiants (/) + prof (/prof) — $(date '+%F %H:%M')" || echo "  (rien de nouveau)"
git -C "$WGH" push origin gh-pages
git worktree remove --force "$WGH"

echo ""
echo "✓ Publié :"
echo "   étudiants : $BASE_URL/"
echo "   prof      : $BASE_URL/prof/"
[ -d "$ROOT/slides" ] && echo "   slides    : $BASE_URL/slides"
