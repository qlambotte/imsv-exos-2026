# Guide — créer les séances suivantes

Ce guide explique, pas à pas, comment ajouter une séance en suivant la structure du site.
Tout est prévu pour être fait **à la main**, avec un générateur pour éviter la corvée.

---

## 1. La structure d'une séance

Chaque séance est un **dossier** `seances/seanceNN/` (NN sur 2 chiffres : `seance01`, `seance02`…).
Il contient des **pages** (affichées dans le site) et des **fragments** (préfixés `_`, réutilisés) :

| Fichier | Rôle | Affiché ? |
|---|---|---|
| `index.qmd` | Accueil : thème, **objectifs**, lien slides, « avant la séance » | oui (page d'accueil de la séance) |
| `socle.qmd` | Page Socle (inclut `_consignes` + `_socle`) | oui |
| `transfert.qmd` | Page Transfert (inclut `_consignes` + `_transfert`) | oui |
| `supplementaires.qmd` | Page Exercices supplémentaires (inclut `_supplementaires`) | oui |
| `institution.qmd` | Page Institutionnalisation : méthode + **auto-évaluation** | oui |
| `_socle.qmd` | **Contenu** des exercices du socle | non (inclus) |
| `_transfert.qmd` | **Contenu** des exercices de transfert | non (inclus) |
| `_supplementaires.qmd` | **Contenu** des exercices supplémentaires (renforcement) | non (inclus) |
| `_consignes.qmd` | Notation + encadré « À lire d'abord » | non (inclus) |
| `_download.qmd` | Le menu de téléchargement des PDF | non (inclus) |
| `_pdf.qmd` | Source d'assemblage de la **feuille PDF** unique | non (rendu par `build-pdf.sh`) |
| `_offline.qmd` | Source de la version **hors-ligne** (un seul fichier HTML) | non (rendu par `build-pdf.sh`) |
| `_metadata.yml` | `corrige-exos: true/false` — corrigé visible ou masqué (géré par `corrige.py`) | non |
| `img/` | Figures de la séance (SVG), copiées par `build-pdf.sh` pour le PDF | — |

**Idée clé — une seule source :** le *contenu* des exercices vit dans `_socle.qmd` et `_transfert.qmd`.
Il est **inclus** (`{{< include >}}`) à la fois dans les pages web *et* dans `_pdf.qmd`. Tu n'écris
donc chaque exercice qu'**une seule fois** ; le web et le PDF en découlent.

---

## 2. Créer une nouvelle séance (le générateur)

```bash
./new-seance.sh 2 "Fonctions et graphes"
```

Ça crée `seances/seance02/` depuis le modèle `seances/_modele/`, en remplaçant le numéro et le titre.
Le script affiche ensuite les **4 étapes restantes** (ci-dessous).

### Étape A — l'ajouter au sommaire

Dans `_quarto.yml`, sous `chapters:` :

```yaml
    - part: seances/seance02/index.qmd
      chapters:
        - seances/seance02/socle.qmd
        - seances/seance02/transfert.qmd
        - seances/seance02/supplementaires.qmd
        - seances/seance02/institution.qmd
```

### Étape B — rédiger le contenu

- **`_socle.qmd`**, **`_transfert.qmd`** et **`_supplementaires.qmd`** : les exercices (voir §3).
- **`index.qmd`** : les objectifs mesurables + le lien vers les slides + « avant la séance ».
- **`institution.qmd`** : la méthode dégagée + la grille d'auto-évaluation (reprend les objectifs).

### Étape C — le QR

```bash
python3 make_qr.py "https://URL-du-site/seance02" img/qr-02.png
```

### Étape D — construire

```bash
./build-all.sh          # QR + tous les PDF + le site
# ou, plus ciblé :
./build-pdf.sh seance02 # juste les 2 PDF de la séance 2
quarto render           # juste le site
```

---

## 3. Écrire un exercice

Un exercice = un **encadré énoncé** suivi d'un **bloc d'aides** en onglets :

```markdown
::: {.callout-caution .exo title="Exercice|Transfert|2|O1"}
Énoncé, consigne à l'infinitif………
:::

::: {.aides}
::: {.panel-tabset}

## Indice 1
Retourne à la théorie du cours : *………*.

## Indice 2
*Question à te poser.*
………

## Indice 3
*Étape.*
………

## Solution
………

## Piège
………

:::
:::
```

**Le titre `Exercice|Catégorie|niveau|Objectif` (sans numéro) :**

- `Catégorie` — `Socle`, `Transfert` ou `Renforcement`. Elle fixe le préfixe du numéro.
- `niveau` — `1`, `2` ou `3` → `★☆☆`, `★★☆`, `★★★`.
- `Objectif` — `O1`, `O2`… : l'objectif de la séance travaillé, affiché en pastille.

Le **numéro est automatique** (filtre `exercice.lua`) : S.1, S.2… pour le socle, T.1… pour le
transfert, R.1… pour le renforcement. Réordonner un exercice ou changer sa catégorie renumérote tout
seul.

**Les indices :** Indice 1 = renvoi à la théorie du cours (par nom de section) ; Indice 2 = une
**question** à se poser, sans sa réponse ; Indice 3 = une **étape** concrète. La solution explique le
pourquoi, le piège nomme la faute usuelle.

**Figures :** un SVG dans `img/`, inséré avec une largeur en cm pour garder la même taille de texte
d'une figure à l'autre :
`![](img/nom.svg){fig-alt="…" width="10cm" fig-align="center"}`.

**Le bloc d'aides** (`.aides` autour d'un `.panel-tabset`) : chaque `##` devient un onglet. Sur le web
il est **replié** derrière « Coups de pouce » (rien n'est montré tant qu'on ne clique pas). Dans le
PDF *complet* il s'aplatit en sous-sections ; dans le PDF *énoncés seuls* il est **retiré** (voir §5).

Pour les **exercices supplémentaires**, l'échelle est plus courte : un seul onglet `## Indice`, puis
`## Solution`.

**Ancre :** chaque exercice reçoit une ancre HTML `#exercice-S1`, `#exercice-T2`… Pour pointer quelqu'un
vers un exercice : `.../seance01/transfert.html#exercice-T2`. Un petit « # » apparaît au survol du titre.

---

## 4. Les deux PDF

`build-pdf.sh seanceNN` produit, depuis `_pdf.qmd` :

- `pdf/seanceNN-enonces.pdf` — **énoncés seuls** (aides retirées) : la feuille à distribuer ;
- `pdf/seanceNN-complet.pdf` — **énoncés + coups de pouce + corrections**.

Le QR (présent seulement dans le PDF) pointe vers la page de correction ; il est **cliquable**.

---

## 5. Ce qui est automatique, ce qui ne l'est pas

- **Automatique :** le **numéro** et la mise en forme du titre (`✎ Exercice S.1 … Socle · O1 · ★★☆`), le retrait de l'icône,
  la version « énoncés seuls » (le filtre `exercice.lua` retire les blocs `.aides`), les ancres, le
  menu « Coups de pouce » repliable, le mode clair/sombre, les 3 boutons du titre.
- **Automatique aussi :** les fichiers de méthodes, créés par `new-seance.sh` depuis
  `seances/_modele-methodes/` (cartes `_methodes-seanceNN.qmd`, feuille `feuille-seanceNN.qmd`, page
  `methodes/seanceNN.qmd`). Les titres et objectifs ne s'écrivent **que** dans les cartes : la feuille à
  compléter les reprend toute seule (ligne `// @@METHODES@@`, remplie par `feuille-auto.py` au build).
- **À la main :** l'ajout au `_quarto.yml`, le QR, et bien sûr le **contenu** mathématique.

---

## 6. Réglages globaux (à faire une fois)

- **URL du site** : `_quarto.yml` (`site-url`), `build-all.sh` (`BASE_URL`), et l'URL du QR dans
  `make_qr.py`. Voir aussi `../A_COMPLETER.md`.
- **Bouton GitHub** : `_includes/tools.html` (`GITHUB_URL`).
- **Apparence** : `theme.scss` (couleurs clair/sombre, exercices, onglets).
- Le **modèle** dupliqué par le générateur : `seances/_modele/` — modifie-le pour changer le squelette
  de toutes les futures séances.
