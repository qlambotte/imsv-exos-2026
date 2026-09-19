#!/usr/bin/env bash
# deploy.sh — publie DEUX rendus sur le même site GitHub Pages (branche gh-pages) :
#   racine  = branche main  → version élève
#   /prof/  = branche prof  → version complète (tout affiché)
#
# ROBUSTE : chaque branche est rendue dans un WORKTREE ISOLÉ (checkout neuf dans un
# dossier temporaire). Ton arbre de travail courant n'est jamais touché, et le cache
# .quarto ne se mélange plus entre branches — c'était la cause de l'erreur « Deno.cwd() ».
# Marche que tu sois sur main, prof, avec ou sans modifs en cours.
#
# Usage :  ./deploy.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
BASE_URL="https://qlambotte.github.io/imsv-exos-2026"

rm -f .git/index.lock 2>/dev/null || true          # verrou résiduel éventuel

for b in main prof gh-pages; do
  git rev-parse --verify -q "$b" >/dev/null || { echo "✗ branche '$b' absente." >&2; exit 1; }
done

STAGE="$(mktemp -d)"
WTS=()
cleanup(){
  for w in "${WTS[@]:-}"; do [ -n "$w" ] && git worktree remove --force "$w" 2>/dev/null || true; done
  rm -rf "$STAGE"; git worktree prune 2>/dev/null || true
}
trap cleanup EXIT

build_ref(){   # $1 = branche, $2 = sous-dossier ("" = racine)
  local ref="$1" dest="$STAGE${2:+/$2}" wt
  wt="$(mktemp -d)"; WTS+=("$wt")
  echo "→ rendu de '$ref' (worktree isolé)"
  git worktree add -q --detach "$wt" "$ref"        # checkout neuf, HEAD détachée sur la branche
  ( cd "$wt" && ./build-all.sh >/dev/null )         # build complet dans le worktree (cache .quarto neuf)
  mkdir -p "$dest"
  cp -a "$wt/_book/." "$dest"/
  git worktree remove -q --force "$wt"
}

build_ref main ""       # élève → racine
build_ref prof "prof"   # prof  → /prof

echo "→ publication sur gh-pages"
WGH="$(mktemp -d)"; WTS+=("$WGH")
git fetch -q origin gh-pages || true
git worktree add -q --force "$WGH" gh-pages
git -C "$WGH" reset -q --hard origin/gh-pages 2>/dev/null || true
find "$WGH" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +   # vide (sauf .git)
cp -a "$STAGE/." "$WGH"/
touch "$WGH/.nojekyll"
git -C "$WGH" add -A
git -C "$WGH" commit -q -m "Deploy : élève (/) + prof (/prof) — $(date '+%F %H:%M')" || echo "  (rien de nouveau)"
git -C "$WGH" push -q origin gh-pages
git worktree remove -q --force "$WGH"

echo ""
echo "✓ Publié :"
echo "   élève : $BASE_URL/"
echo "   prof  : $BASE_URL/prof/"
