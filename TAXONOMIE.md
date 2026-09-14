# Taxonomie des exercices — IMSV

But : que **chaque exercice** ait une place claire (famille + objectif + niveau), lisible dans son
en-tête (« ✎ Exercice **S.3**  ·  Socle · **O2** · **★★☆** ») et cohérente d'une séance à l'autre.

## Les quatre familles (la lettre = le préfixe de numérotation)

| Famille | Rôle | Pour qui | À l'examen ? |
|---|---|---|---|
| **Socle (S)** | le **noyau** : les savoir-faire de routine, directement issus de la théorie | **tous** | oui (esprit du QCM) |
| **Transfert (T)** | appliquer les savoir-faire du socle à un **contexte nouveau** (un vrai problème) | tous | oui |
| **Renforcement (R)** | **variations** du socle, même compétence, entraînement en plus | les rapides / à domicile | oui |

La **catégorie pilote le numéro** : Socle → S.1, S.2… ; Transfert → T.1… ; Renforcement → R.1… ;
Dépassement → D.1… La numérotation est **automatique** (filtre `exercice.lua`) : réordonner un
exercice, ou changer sa catégorie, renumérote tout seul.

## Qu'est-ce qu'un exercice de **socle** ?

Un exercice est « socle » quand **tous** ces critères sont réunis :

1. **Une compétence de routine, bien identifiée**, prise directement dans la théorie (une définition,
   une règle, une méthode montrée au cours).
2. **Attendu de tout le monde** : c'est la base commune, pas un supplément.
3. **Méthode non ambiguë** : il y a une « bonne façon » de faire (ce n'est pas une exploration
   ouverte).
4. **Court et autonome** : se fait en séance **ou** à la maison, sans dépendre d'un autre exercice.
5. **Réussite = correct *et* fluide** (automatisme visé), et il **travaille un seul objectif** (Ox).
6. Règle du pouce : *pourrait figurer, dans l'esprit, au **QCM** post-cours.*

Ce **n'est pas** du socle si l'exercice : demande un **contexte nouveau** (→ *Transfert*) ; n'est qu'un
**entraînement en plus** (→ *Renforcement*) ; ou **dépasse** le programme requis (→ *Dépassement*).

## Les niveaux de difficulté (★)

Le niveau mesure la **longueur du chemin** (nombre d'étapes, choix à faire), **pas** la difficulté
« intellectuelle » du sujet. Un même sujet peut donc avoir des exercices ★☆☆ **et** ★★★.

| Niveau | Ce qu'on demande | Ce que ça vérifie |
|---|---|---|
| **★☆☆** | application **directe d'une seule** règle ou définition, en **une** étape ; réponse immédiate une fois la règle connue | on **connaît** |
| **★★☆** | **enchaîner 2–3 étapes**, **ou** choisir la bonne règle parmi plusieurs, **ou** une petite manipulation / traduction | on **sait faire** |
| **★★★** | **plusieurs étapes** avec un raisonnement, un **cas particulier / piège** à gérer, ou une **justification** à produire | on **maîtrise / raisonne** |

Repères concrets :

- **★☆☆** — « Calcule $5^{-2}$. » ; « Convertis $90°$ en radians. »
- **★★☆** — « Développe $(2a-5)(2a+5)$. » ; « Après $+35\,\%$ on atteint $54$ : valeur initiale ? »
- **★★★** — « Montre pourquoi $\sqrt{x^2}=|x|$ et pas $x$. » ; un problème contextuel à modéliser puis
  contrôler par l'ordre de grandeur.

## En pratique, dans le titre d'un exercice

Format source (pas de numéro à la main) : `Exercice|Catégorie|niveau|Objectif`, p.ex.
`Exercice|Socle|2|O1`. Rendu : « ✎ **Exercice S.k** … Socle · O1 · ★★☆ ».
