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
# Usage :  ./deploy.sh [portée] [--force]          (depuis main)
#   ./deploy.sh                    tout publier (= « tout »)
#   ./deploy.sh tout               idem : livre (étudiants + prof) et slides, pages communes comprises
#   ./deploy.sh seance 5           fichiers de la séance 5 seulement (page, méthodes, PDF)
#   ./deploy.sh slides 5           slides de la séance 5 seulement
#   ./deploy.sh seance 5 tout      fichiers ET slides de la séance 5
#   ./deploy.sh seance 4 5         plusieurs séances (« slides 4 5 », « seance 4 5 tout » : idem)
#   --force                        tout reconstruire, cache ignoré en lecture (en cas de doute)
# Une publication ciblée ne touche, sur gh-pages, que les fichiers de la/des séance(s) demandée(s) ;
# menu, accueil et recherche ne sont mis à jour que par « ./deploy.sh tout ».
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"; cd "$ROOT"
BASE_URL="https://qlambotte.github.io/imsv-exos-2026"

usage(){ sed -n '2,30p' "$0"; }
die_usage(){ echo "✗ $1" >&2; echo "  (voir ./deploy.sh --help)" >&2; exit 2; }
norm(){ printf '%02d' "$((10#$1))"; }

# Grammaire : [seance|slides] N… [tout]   ou   tout   ou   (rien)
KIND=""; ALL=0; NUMS=()
for a in "$@"; do
  case "$a" in
    --force) export IMSV_FORCE=1 ;;
    -h|--help) usage; exit 0 ;;
    tout|tous|all) ALL=1 ;;
    seance|séance|seances|séances|s)
      [ -z "$KIND" ] || [ "$KIND" = seance ] || die_usage "« seance » et « slides » ne se combinent pas : utilise « seance N tout »."
      KIND=seance ;;
    slides|slide)
      [ -z "$KIND" ] || [ "$KIND" = slides ] || die_usage "« seance » et « slides » ne se combinent pas : utilise « seance N tout »."
      KIND=slides ;;
    seance[0-9]*|séance[0-9]*|s[0-9]*)
      n="${a#seance}"; n="${n#séance}"; n="${n#s}"
      [[ "$n" =~ ^[0-9]+$ ]] || die_usage "argument inconnu : $a"
      [ -z "$KIND" ] || [ "$KIND" = seance ] || die_usage "« seance » et « slides » ne se combinent pas : utilise « seance N tout »."
      KIND=seance; NUMS+=("$(norm "$n")") ;;
    slides[0-9]*)
      n="${a#slides}"; [[ "$n" =~ ^[0-9]+$ ]] || die_usage "argument inconnu : $a"
      [ -z "$KIND" ] || [ "$KIND" = slides ] || die_usage "« seance » et « slides » ne se combinent pas : utilise « seance N tout »."
      KIND=slides; NUMS+=("$(norm "$n")") ;;
    [0-9]*)
      [[ "$a" =~ ^[0-9]+$ ]] || die_usage "argument inconnu : $a"
      [ -n "$KIND" ] || die_usage "numéro sans « seance » ni « slides » : ./deploy.sh seance $a"
      NUMS+=("$(norm "$a")") ;;
    *) die_usage "argument inconnu : $a" ;;
  esac
done

# Portée : FULL = tout ; sinon FILES_N / SLIDES_N = séances dont on publie fichiers / slides
FULL=0; FILES_N=(); SLIDES_N=()
if [ "${#NUMS[@]}" -eq 0 ]; then
  [ -z "$KIND" ] || die_usage "numéro de séance manquant : ./deploy.sh $KIND N"
  FULL=1
else
  mapfile -t NUMS < <(printf '%s\n' "${NUMS[@]}" | sort -u)
  for n in "${NUMS[@]}"; do
    if [ "$KIND" = seance ] || [ "$ALL" = 1 ]; then FILES_N+=("$n"); fi
    if [ "$KIND" = slides ] || [ "$ALL" = 1 ]; then SLIDES_N+=("$n"); fi
  done
fi
DO_SITE=0; DO_SLIDES=0
if [ "$FULL" = 1 ]; then DO_SITE=1; DO_SLIDES=1; fi
if [ "${#FILES_N[@]}" -gt 0 ]; then DO_SITE=1; fi
if [ "${#SLIDES_N[@]}" -gt 0 ]; then DO_SLIDES=1; fi
export IMSV_CACHE="${IMSV_CACHE:-$ROOT/.deploy-cache}"   # le MÊME cache pour tous les worktrees
export IMSV_STATS_FILE="$(mktemp)"                          # détail des produits, pour le récapitulatif

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

# Les séances demandées doivent exister dans HEAD (en ligne « seanceNN » ou hors ligne « _seanceNN »).
in_head(){ git cat-file -e "HEAD:$1" 2>/dev/null || git cat-file -e "HEAD:$2" 2>/dev/null; }
for n in ${FILES_N[@]+"${FILES_N[@]}"}; do
  in_head "seances/seance$n" "seances/_seance$n" || { echo "✗ séance $n : seances/seance$n absente de HEAD (commité ?)." >&2; exit 1; }
done
for n in ${SLIDES_N[@]+"${SLIDES_N[@]}"}; do
  in_head "slides/seance$n" "slides/_seance$n" || { echo "✗ slides de la séance $n : slides/seance$n absent de HEAD (commité ?)." >&2; exit 1; }
done

STAGE="$(mktemp -d)"; WTS=()
cleanup(){
  for w in "${WTS[@]:-}"; do [ -n "$w" ] && git worktree remove --force "$w" 2>/dev/null || true; done
  rm -rf "$STAGE" "$IMSV_STATS_FILE"; git worktree prune 2>/dev/null || true
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

if [ "$DO_SITE" = 1 ]; then
  build_view student ""     # site étudiant  -> racine
  build_view prof   "prof"  # vue prof       -> /prof
fi

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
  ( cd "$wt" && python3 incremental.py slides --view "$mode" --dest "$dest" )
  git worktree remove --force "$wt"
}
if [ "$DO_SLIDES" = 1 ]; then
  [ "$FULL" = 1 ] || export IMSV_ONLY_SEANCES="${SLIDES_N[*]}"   # decks des autres séances : non construits
  build_slides student "$STAGE/slides"
  build_slides prof    "$STAGE/prof/slides"
fi

# Publication ciblée : sur gh-pages, on remplace uniquement les fichiers de la séance (supprimés
# s'ils n'existent plus dans le stage : gh-pages reste le reflet du stage pour ces chemins).
sync_path(){   # $1 = chemin relatif (stage -> gh-pages)
  rm -rf "${WGH:?}/$1"
  if [ -e "$STAGE/$1" ]; then mkdir -p "$WGH/$(dirname "$1")"; cp -a "$STAGE/$1" "$WGH/$1"; fi
}
sync_glob(){   # $1 = dossier relatif, $2 = motif
  local f
  shopt -s nullglob
  for f in "$WGH/$1"/$2; do rm -rf "$f"; done
  for f in "$STAGE/$1"/$2; do mkdir -p "$WGH/$1"; cp -a "$f" "$WGH/$1/"; done
  shopt -u nullglob
}

echo "→ publication gh-pages"
WGH="$(mktemp -d)"; WTS+=("$WGH")
git fetch -q origin gh-pages || true
git worktree add --force "$WGH" gh-pages >/dev/null
git -C "$WGH" reset -q --hard origin/gh-pages 2>/dev/null || true
if [ "$FULL" = 1 ]; then
  find "$WGH" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  cp -a "$STAGE/." "$WGH"/
  MSG="Deploy : étudiants (/) + prof (/prof)"
else
  PARTS=()
  for n in ${FILES_N[@]+"${FILES_N[@]}"}; do
    for b in "" "prof/"; do
      [ -e "$WGH/${b}seances/seance$n" ] || [ ! -e "$STAGE/${b}seances/seance$n" ] \
        || echo "  ⚠ séance $n : première publication dans ${b:-/} — menu et accueil ne la listent qu'après « ./deploy.sh tout »."
      sync_path "${b}seances/seance$n"
      sync_path "${b}seances/methodes/seance$n.html"
      sync_glob "${b}pdf" "seance$n-*"
      sync_path "${b}pdf/feuille-seance$n.pdf"
      sync_path "${b}pdf/methodes-seance$n.pdf"
    done
    PARTS+=("séance $n (fichiers)")
  done
  for n in ${SLIDES_N[@]+"${SLIDES_N[@]}"}; do
    for b in "" "prof/"; do sync_path "${b}slides/seance$n"; done
    PARTS+=("séance $n (slides)")
  done
  if [ "${#SLIDES_N[@]}" -gt 0 ]; then
    for b in "" "prof/"; do sync_path "${b}slides/index.html"; done
  fi
  MSG="Deploy ciblé : $(IFS=', '; echo "${PARTS[*]}")"
fi
touch "$WGH/.nojekyll"
git -C "$WGH" add -A
git -C "$WGH" commit -q -m "$MSG — $(date '+%F %H:%M')" || echo "  (rien de nouveau)"
git -C "$WGH" push origin gh-pages
git worktree remove --force "$WGH"

echo ""
python3 "$ROOT/incremental.py" recap || true   # ce qui a été reconstruit / réutilisé, slides comprises
echo ""
echo "✓ Publié en ${SECONDS} s :"
if [ "$FULL" = 1 ]; then
  echo "   étudiants : $BASE_URL/"
  echo "   prof      : $BASE_URL/prof/"
  [ -d "$ROOT/slides" ] && echo "   slides    : $BASE_URL/slides   (prof : $BASE_URL/prof/slides)"
else
  for n in ${FILES_N[@]+"${FILES_N[@]}"}; do
    echo "   séance $n : $BASE_URL/seances/seance$n/   (prof : $BASE_URL/prof/seances/seance$n/)"
  done
  for n in ${SLIDES_N[@]+"${SLIDES_N[@]}"}; do
    echo "   slides $n : $BASE_URL/slides/seance$n/   (prof : $BASE_URL/prof/slides/seance$n/)"
  done
  echo "   (menu, accueil et recherche inchangés : « ./deploy.sh tout » pour les mettre à jour)"
fi
