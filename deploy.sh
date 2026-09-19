#!/usr/bin/env bash
# deploy.sh — publie DEUX rendus sur le même site GitHub Pages (branche gh-pages) :
#   racine  = branche main  → version élève
#   /prof/  = branche prof  → version complète (tout affiché : corrigés, brouillons)
#
# Prérequis :
#   - arbre de travail PROPRE (rien de non committé) : on change de branche ;
#   - les branches  main  et  prof  existent et sont à jour ;
#   - Pages sert déjà la branche  gh-pages  (déjà le cas ici).
#
# Usage :  ./deploy.sh
#
# NB : remplace l'ancien « quarto publish gh-pages » (qui ne publie qu'un seul site).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

BASE_URL="https://qlambotte.github.io/imsv-exos-2026"

# --- garde-fous ---
[ -x ./build-all.sh ] || { echo "✗ build-all.sh introuvable ou non exécutable." >&2; exit 1; }
if [ -n "$(git status --porcelain)" ]; then
  echo "✗ Arbre de travail non propre : committe (ou 'git stash') avant de déployer." >&2
  exit 1
fi
for b in main prof gh-pages; do
  git rev-parse --verify -q "$b" >/dev/null || { echo "✗ branche '$b' absente." >&2; exit 1; }
done

ORIG="$(git rev-parse --abbrev-ref HEAD)"
STAGE="$(mktemp -d)"
WT=""
cleanup() {
  git checkout -q -- . 2>/dev/null || true          # jette d'éventuels PDF régénérés
  [ -n "$WT" ] && git worktree remove --force "$WT" 2>/dev/null || true
  git checkout -q "$ORIG" 2>/dev/null || true        # revient à la branche de départ
  rm -rf "$STAGE"
}
trap cleanup EXIT

# --- rend une branche dans un sous-dossier de STAGE ("" = racine) ---
render() {   # $1 = branche, $2 = sous-dossier
  local branch="$1" dest="$STAGE${2:+/$2}"
  echo "→ rendu de '$branch'"
  git checkout -q "$branch"
  rm -rf _book
  ./build-all.sh >/dev/null
  mkdir -p "$dest"
  cp -a _book/. "$dest"/
  git checkout -q -- .        # les PDF régénérés (tracés) sont déjà dans _book : on nettoie l'arbre
}

render main ""       # élève → racine
render prof "prof"   # prof  → /prof

# --- publication sur gh-pages via un worktree isolé ---
echo "→ publication sur gh-pages"
WT="$(mktemp -d)"
git fetch -q origin gh-pages || true
git worktree add -q --force "$WT" gh-pages
git -C "$WT" reset -q --hard origin/gh-pages 2>/dev/null || true
find "$WT" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +   # vide (sauf .git)
cp -a "$STAGE/." "$WT"/
touch "$WT/.nojekyll"                                                # pas de traitement Jekyll
git -C "$WT" add -A
git -C "$WT" commit -q -m "Deploy : élève (/) + prof (/prof) — $(date '+%F %H:%M')" \
  || echo "  (rien de nouveau à publier)"
git -C "$WT" push -q origin gh-pages

echo ""
echo "✓ Publié :"
echo "   élève : $BASE_URL/"
echo "   prof  : $BASE_URL/prof/"
