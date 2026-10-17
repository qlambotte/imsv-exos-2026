#!/usr/bin/env bash
# deploy.sh — publie sur gh-pages, depuis la branche courante (main), DEUX vues :
#   /       = site étudiant  (séances prêtes ; les séances en cours, préfixe « _ », exclues)
#   /prof/  = vue prof complète (TOUTES les séances et TOUS les slides activés, y compris ceux en cours),
#             NON référencée depuis le site étudiant.
#
# Une seule branche, pas de bascule à la main. Chaque vue est rendue dans un WORKTREE
# ISOLÉ : ton arbre de travail n'est jamais touché et le cache .quarto ne se mélange pas
# (c'était la cause de l'erreur « Deno.cwd() »).
#
# INCRÉMENTAL : rien n'est reconstruit si ses sources n'ont pas changé. Les PDF, feuilles,
# méthodes, decks de slides et le site HTML de chaque vue sont rangés dans .deploy-cache/
# (ignoré par git), par empreinte de contenu — voir incremental.py. Une modification dans un
# seul deck ne reconstruit que ce deck ; une modification dans une séance ne reconstruit que
# les PDF de cette séance (+ le rendu HTML du livre, que Quarto ne sait pas faire par morceaux).
# Le déploiement part de HEAD : ce qui n'est pas commité n'est pas publié.
#
# Usage :  ./deploy.sh            (depuis main)
#          ./deploy.sh --force    (tout reconstruire, cache ignoré en lecture ; en cas de doute)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"; cd "$ROOT"
BASE_URL="https://qlambotte.github.io/imsv-exos-2026"

for a in "$@"; do
  case "$a" in
    --force) export IMSV_FORCE=1 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "Option inconnue : $a   (usage : ./deploy.sh [--force])" >&2; exit 2 ;;
  esac
done
export IMSV_CACHE="${IMSV_CACHE:-$ROOT/.deploy-cache}"   # le MÊME cache pour tous les worktrees

rm -f .git/index.lock 2>/dev/null || true
git rev-parse --verify -q gh-pages >/dev/null || { echo "✗ branche gh-pages absente." >&2; exit 1; }

# Les worktrees sont extraits de HEAD : l'outillage de build doit donc y être commité.
git cat-file -e HEAD:incremental.py 2>/dev/null \
  || { echo "✗ incremental.py n'est pas commité sur HEAD : commite-le (et les build-*.sh modifiés) avant de déployer." >&2; exit 1; }
if ! git diff --quiet HEAD -- incremental.py deploy.sh build-all.sh build-pdf.sh build-boite.sh build-methodes.sh post-render.py 2>/dev/null; then
  echo "⚠ outillage de build modifié mais non commité : le déploiement utilise la version de HEAD." >&2
fi
NDIRTY="$(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
[ "$NDIRTY" = 0 ] || echo "⚠ $NDIRTY fichier(s) modifié(s) non commité(s) : ils ne seront PAS publiés (le déploiement part de HEAD)." >&2

STAGE="$(mktemp -d)"; WTS=()
cleanup(){
  for w in "${WTS[@]:-}"; do [ -n "$w" ] && git worktree remove --force "$w" 2>/dev/null || true; done
  rm -rf "$STAGE"; git worktree prune 2>/dev/null || true
}
trap cleanup EXIT

build_view(){   # $1 = student|prof ; $2 = sous-dossier de destination ("" ou "prof")
  local mode="$1" dest="$STAGE${2:+/$2}" wt orphans=()
  wt="$(mktemp -d)"; WTS+=("$wt")
  echo "→ site ($mode)"
  git worktree add --detach "$wt" HEAD >/dev/null
  [ "$mode" = student ] && orphans=(--warn-orphans)
  (
    cd "$wt"
    # Auto-guérison : ce worktree est extrait depuis l'index git, qui peut ne pas
    # avoir enregistré le bit exécutable de ces scripts (cf. « Permission non
    # accordée » sur build-pdf.sh). On le remet ici, dans CE worktree seulement.
    chmod +x build-all.sh build-pdf.sh build-methodes.sh build-boite.sh 2>/dev/null || true
    if [ "$mode" = prof ]; then
      # active toutes les séances en cours (dossiers seances/_seanceNN)
      for d in seances/_seance[0-9][0-9]; do
        [ -e "$d" ] || continue
        n=$(basename "$d" | sed 's/^_seance0*//')
        python3 seance-onoff.py "$n" on --garder-statut >/dev/null   # garde l'étiquette « en construction »…
      done
      # site-url sous /prof pour des liens cohérents dans la vue prof
      sed -i 's#imsv-exos-2026/"#imsv-exos-2026/prof/"#' _quarto.yml
    fi
    # PDF / feuilles / méthodes (cache), puis site HTML (cache) → copié dans le stage
    python3 incremental.py site --view "$mode" --dest "$dest" ${orphans[@]+"${orphans[@]}"}
  )
  git worktree remove --force "$wt"
}

build_view student ""     # site étudiant  -> racine
build_view prof   "prof"  # vue prof       -> /prof

# slides/ : deck(s) reveal.js, projet Quarto indépendant du livre (son propre
# _quarto.yml dans slides/ fait écran à celui du livre) -> rendu à part, dans son propre
# worktree isolé, puis seuls les fichiers publiés (pas les sources .qmd/.scss/img) sont
# copiés dans le stage. Volontairement non référencé dans le livre/menus : accessible
# seulement par lien direct.
#
# Deux vues, comme pour le livre :
#   /slides        = decks des séances EN LIGNE (slides/seanceNN) + remédiations
#   /prof/slides   = TOUS les decks, y compris ceux hors ligne (slides/_seanceNN, activés
#                    dans le worktree de rendu uniquement ; ton arbre n'est pas touché)
#
# Chaque deck slides/seanceNN/<nom>.qmd ou slides/remed_*/<nom>.qmd (hors fragments _*.qmd) est découvert et
# rendu automatiquement : ajouter une séance n'implique de toucher ni ce script,
# ni index.html (regénéré à chaque déploiement par make-index.py).
# Un deck n'est re-rendu que si lui-même, ses fragments, ses images ou les fichiers qu'il cite
# (« ../seance01/theme.scss »…) ont changé ; le même deck, dans les deux vues, n'est rendu qu'une fois.
build_slides(){   # $1 = student|prof ; $2 = dossier de destination
  [ -d "$ROOT/slides" ] || return 0
  local mode="$1" dest="$2" wt d
  wt="$(mktemp -d)"; WTS+=("$wt")
  echo "→ slides ($mode)"
  git worktree add --detach "$wt" HEAD >/dev/null
  if [ "$mode" = prof ]; then
    for d in "$wt"/slides/_seance[0-9][0-9]; do
      [ -d "$d" ] || continue
      mv "$d" "$wt/slides/${d##*/_}"      # _seanceNN -> seanceNN (worktree seulement)
    done
  fi
  ( cd "$wt" && python3 incremental.py slides --dest "$dest" )
  git worktree remove --force "$wt"
}
build_slides student "$STAGE/slides"
build_slides prof    "$STAGE/prof/slides"

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
echo "✓ Publié en ${SECONDS} s :"
echo "   étudiants : $BASE_URL/"
echo "   prof      : $BASE_URL/prof/"
[ -d "$ROOT/slides" ] && echo "   slides    : $BASE_URL/slides   (prof : $BASE_URL/prof/slides)"
