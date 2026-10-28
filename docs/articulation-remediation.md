# Articulation des decks de remédiation et du dispositif « parcours »

Date : 22 octobre 2026. Analyse seule : aucun fichier existant du dépôt n'a été modifié.

Les abréviations ci-dessous sont celles du dispositif : « diag » pour la banque de diagnostic, « confirm » pour la banque du test de confirmation, « ET » pour erreur type. Les décks sont désignés par leur thème : logique, vecteurs, fonctions, trigo.

## 1. Périmètre lu et limites

Lus en entier : les quatre décks `01-remediation.qmd`, leurs annexes `02-annexe.qmd`, leurs fichiers `wooclap-*.md`, leurs trames (versions HTML), le deck `remed_accueil`, `CLAUDE.md`, `TAXONOMIE.md`, `GUIDE-SEANCES.md`, `exercice.lua`, et les exercices des séances 1, 4 et 5 (`_socle`, `_transfert`, `_supplementaires`). Le doc de projet a été lu en entier.

Non lus : les PDF de trames (le HTML équivalent a été lu), les images des décks, `a_supprimer/` (anciennes versions bio, biomed, vecteurs-et-fonctions), les exercices des séances 2 et 3, les solutions des annexes au-delà de la structure et de quelques échantillons.

Vérifié par script : pour les 45 questions des fichiers Wooclap (28 du noyau, 17 de réserve), l'énoncé et la bonne réponse figurent à l'identique dans le deck ou l'annexe. Il n'y a donc pas de dérive actuelle entre les trois copies, mais la même question existe en trois endroits (§2, point 1).

Les sources des exemples sont citées comme dans les decks et n'ont pas été revérifiées : SNCB[^sncb], Manuel MSD[^msd], Tanaka, Monahan et Seals[^tanaka], OMS[^oms].

## 2. Constats transversaux

1. **Triple copie de chaque question.** Énoncé et choix dans `wooclap-*.md`, énoncé, choix et explication par distracteur dans le deck, réserve dans l'annexe. Le fichier de données par thème du dispositif remplace les trois ; les explications par distracteur du deck sont la matière des constats d'ET.
2. **Les distracteurs sont déjà reliés à des erreurs.** Chaque distracteur a une explication qui nomme la confusion. Sur 84 distracteurs (4 thèmes × 7 questions × 3), 80 correspondent à une ET identifiable (tableaux du §3). Les quatre autres sont signalés en §3. Ces ET sont des hypothèses de l'auteur : aucune fréquence de réponse n'est mesurée.
3. **Aucune option « Je ne sais pas »** dans les 45 questions. Elle est requise par le dispositif.
4. **Une seule question par compétence ou presque.** Chaque QCM compte 7 questions sur 5 à 7 savoir-faire distincts. Le dispositif demande deux questions par compétence pour 6 à 8 questions (§5, décision ouverte 1).
5. **Les décks n'utilisent que les exercices de renforcement.** Les trames le précisent (« exercices de renforcement uniquement »). Or les exercices du socle comblent plusieurs écarts relevés par les trames : S.5(a) de la séance 4 pour la combinaison `3u − 2v` (V2), S.7 et S.8 de la séance 4 pour le signe du produit scalaire (V6), S.5(c) de la séance 4 pour la colinéarité (V7), S.5(b)(c) de la séance 5 pour l'étude de signe avec ∄ (F7), S.6(a) de la séance 5 pour le domaine d'une composée (F4), S.4 de la séance 4 pour cos et sin du deuxième quadrant (T1).
6. **Échelle d'indices non conforme au standard.** Standard : indice 1 théorie, indice 2 question à se poser, indice 3 une étape, puis solution, puis pièges. Dans les sources : séance 5 (R, S, T) et séance 4 (S, T) ont trois indices ; séance 4 R : un seul « Indice » pour les 12 exercices ; séance 1 R : un indice pour R.4 à R.13, deux indices pour R.1 à R.3 et R.14 à R.17 ; séance 1 S : deux indices, trois pour S.6. Les décks pointent surtout vers les exercices à un seul indice.
7. **Solutions des annexes.** Elles enchaînent les étapes et donnent le résultat à la fin de chaque partie (ex. R.4 vecteurs). Le standard demande la réponse finale d'abord, puis les étapes. Les annexes ne contiennent pas les pièges.
8. **Identifiants d'exercices instables.** Le numéro R.n est calculé par ordre dans le fichier (`exercice.lua`) ; les decks écrivent « R.5(d) (séance 4) ». Réordonner un fichier d'exercices casse tous les renvois. Les parties (a)(b)(c) n'ont pas d'identifiant, alors que le plan doit dédoublonner par exercice et que R.7 (trigo) sert à cinq questions sur sept.
9. **Énoncés d'exercices dupliqués dans les decks** (diapositives « Exercice R.n »). Cela contredit la règle « une seule source » de `CLAUDE.md` ; R.2 et R.5(d) sont déjà des extraits reformulés.
10. **Règle « pas de calculatrice » non respectée** à trois endroits : fonctions Q2 (`h = √3,2 ≈ 1,79 m`), vecteurs Q4 (`43 N` à l'unité près), annexe vecteurs R.4(c) (`√13 ≈ 3,6`). Corrections proposées en §5.
11. **Données inventées** dans vecteurs et trigo (la trame le dit : « situations inventées, sans donnée sourcée »). Cela contredit le standard « données réelles et sourcées ». Logique (SNCB, MSD) et fonctions (Tanaka, OMS) sont conformes.
12. **Doublon entre vecteurs et trigo.** Les diapositives `cle-t1`, `cle-t3`, `cle-t4` sont identiques à `cle-v3`, `cle-v4`, `cle-v5`. Les questions V4 et T5, V5 et T4 testent les mêmes ET. Le fichier de données doit partager les compétences, pas les copier.
13. **Vocabulaire hors cours à vérifier.** `CLAUDE.md` interdit tout terme absent du cours théorique. Les decks emploient « tenue » et « rompue » (la trame logique le note) et « condition suffisante / nécessaire » : à confirmer dans le cours.
14. **Poids des ancres.** Chaque deck est un HTML autonome de 4,9 à 6 Mo. Un lien théorique `01-remediation.html#/cle-f2` charge tout le deck, mauvais sur téléphone.

## 3. Analyse par thème

Conventions : les minutes sont des valeurs de départ calculées avec la règle ★1 = 3 min, ★2 = 5 min, ★3 = 8 min par exercice entier, proratisées pour les parties citées. Elles sont à chronométrer au pilote. « Confirm » donne la question de réserve qui teste les mêmes ET avec un autre énoncé ; « à écrire » signifie qu'aucune n'existe. « Ancre » est l'identifiant de diapositive du deck.

### 3.1 Logique (séance 1)

| Q | Compétence | Erreurs types (distracteurs) | Ancre | Exercices (min.) | Confirm |
|---|---|---|---|---|---|
| Q1 | Lire un engagement : une seule rupture | L1 conclut à une rupture quand la condition n'est pas remplie. L2 voit une rupture dans une compensation versée sans obligation. Distracteur « tenu » : pas d'ET propre (consigne « ne tient pas » mal lue) | `contrat-2`, `contrat-3` | R.3 (5), R.9 (5), tables abstraites | Réserve 1 |
| Q2 | Colonne de α ⇒ β | L3 colonne de la réciproque. L4 colonne de ⟺. L5 colonne de ∧ | `contrat-4`, `contrat-6` | R.10(a) (3), R.14(a) (3) | à écrire |
| Q3 | Condition non remplie | L1 (« fausse car le diabète n'est pas établi »). L6 conclut ¬β. « On ne peut pas savoir » : équivaut à « je ne sais pas » | `contrat-3`, `contrat-4` | R.2(c) (2), R.10(a) | Réserve 1 |
| Q4 | Réciproque | L7 inverse (nie sans échanger). L8 prend la contraposée pour la réciproque. L9 échange puis nie la conclusion | `contrat-5`, `contrat-6` | R.6 (5), R.14(b) (2) | Réserve 3 (mêmes confusions) |
| Q5 | Déduire par contraposée | L10 affirme la condition. L11 nie « ≥ 60 min » par « aucun retard ». L12 « on ne peut rien déduire » | `contrat-7`, `contrat-8` | R.6, R.14(a) : écrire la contraposée, jamais déduire | à écrire |
| Q6 | Négation d'une implication | L13 nie la conclusion seule. L14 nie la condition et garde la conclusion. L15 écrit ¬α ∨ ¬β | `contrat-9` | R.10(b) (2) ; R.8 hors sujet (quantificateurs) | Réserve 4 |
| Q7 | Suffisant, nécessaire | L16 sens inversé (deux formulations). L17 « ¬β nécessaire pour α » (c'est la rupture) | `contrat-sn1` à `sn3` | aucun | Réserve 5 |

Ancres manquantes : négation d'une condition numérique en mots (L11, seule `contrat-9` s'en approche).
Exercices manquants : engagement ou règlement en contexte réel (Q1, Q4, Q5, Q6) ; item « α faux » (Q3) ; déduction par contraposée (Q5) ; suffisant et nécessaire (Q7).
Exercices S de la séance 1 utilisables : S.6 (réciproque et contraposée, trois indices).
Banque de confirmation : 4 réserves sur 5 sont des variantes (R1, R3, R4, R5). La Réserve 2 (écriture ¬α ∨ β) teste une autre compétence.

### 3.2 Vecteurs (séance 4)

| Q | Compétence | Erreurs types | Ancre | Exercices (min.) | Confirm |
|---|---|---|---|---|---|
| V1 | Coordonnées d'un déplacement | V1a départ moins arrivée. V1b additionne. V1c signe perdu en `−1 − 3` : erreur de calcul, pas de concept | `cle-v1` | R.8(a) (3), R.3(b) (3) | à écrire |
| V2 | Combinaison `3u − 2v` | V2a soustraction non appliquée. V2b coefficients échangés. V2c facteur oublié | `cle-v2` (sans exemple de combinaison) | R.4(a)(b) (3), contexte seulement ; S.5(a) (3) | à écrire |
| V3 | Enchaîner des déplacements | V3a sens inversé. V3b terme oublié. V3c « pas un seul vecteur » | `cle-v2` (retrancher = ajouter l'opposé non énoncé) | R.1 (5) | à écrire |
| V4 | Sinus ou cosinus selon l'axe de mesure | V4a cosinus au lieu de sinus. V4b coordonnée égale à la norme. V4c tangente | `cle-v5` | R.5(d) (5), R.6(a)(b) (3) ; R.6 mesure toujours depuis x | VR3 |
| V5 | Angle d'un vecteur | V5a tangente seule. V5b 180 − θ au lieu de 180 + θ. V5c 360 − θ | `cle-v4`, `cle-v3` | R.7 (5), R.6(c) (2) | à écrire |
| V6 | Produit scalaire : valeur et signe | V6a confond « petit positif » et nul (orthogonal). V6b soustrait les produits. V6c écrit un vecteur | `cle-v6` | R.9 (5), pas sur le signe ; S.7 (5), S.8 (3) | VR4 (partiel) |
| V7 | Colinéarité | V7a signe de λ perdu. V7b confond avec orthogonalité. V7c produit en croix mal posé | aucune diapositive dédiée (une phrase dans `cle-v2`, une ligne dans `cle-v7`) | R.3(a)(b) (5) ; S.5(c) (3) | à écrire |

Sans diag : VR1 (norme dans ℝ³, couvert par R.8) et VR2 (produit vectoriel, aucun exercice, aucune diapositive de théorie).
Exercices manquants : angle mesuré depuis la verticale avec les deux coordonnées (V4) ; produit scalaire et signe sans calculer l'angle (couvert par S.7, S.8) ; produit vectoriel (VR2).
Banque de confirmation : une seule variante (VR3) ; 6 questions à écrire.

### 3.3 Fonctions (séance 5)

| Q | Compétence | Erreurs types | Ancre | Exercices (min.) | Confirm |
|---|---|---|---|---|---|
| F1 | Domaine | F1a oublie le dénominateur. F1b exclut la borne (inégalité stricte). F1c oublie la racine | `cle-f2` | R.5(a)(b)(c) (4) ; S.4(a) | à écrire |
| F2 | Évaluer ou résoudre | F2a garde la solution négative (domaine pratique). F2b oublie la racine (donne h²). F2c inverse le quotient | `cle-f1`, `cle-f2` | R.2(a)(b)(c) (4), R.5(d)(e) (2) ; S.4(b) | FR4 (partiel) |
| F3 | Composition : valeur | F3a ordre inversé. F3b additionne. F3c multiplie | `cle-f3` | R.9(a) (2), R.10(a) (2) ; S.6(b) | à écrire |
| F4 | Domaine d'une composée | F4a ne garde que Dom f. F4b prend Dom g (sorties) pour des entrées. F4c inverse l'inégalité en passant à l'inverse | `cle-f3` (une phrase, sans exemple) | R.9(b) insuffisant ; S.6(a) (3) | à écrire |
| F5 | Extrema, intervalle ouvert | F5a extremum « atteint » en une borne exclue. F5b ne voit que le maximum. F5c « ni minimum ni maximum » | `cle-f4` | R.8 (5), R.7(d) (2) | à écrire |
| F6 | Fonction réciproque | F6a signe perdu. F6b répète f. F6c prend 1/f | `cle-f5` | R.10(b)(c)(d) (4) | à écrire |
| F7 | Signe d'un quotient | F7a inclut la valeur interdite. F7b signes inversés. F7c retire seulement la valeur interdite | `cle-f6` | R.7(a)(b) sans ∄ ; S.5(b)(c) (5) | à écrire |

Exercices manquants : aucun, si S.5 et S.6(a) de la séance 5 sont admis dans le pool (3 indices, solution, piège).
Sans diag : FR1 (reconnaître une fonction), FR2 (définition de la croissance), FR3 (injectivité) : trois compétences absentes de la banque de diag.
Banque de confirmation : 6 questions à écrire, FR4 comme variante partielle de F2.

### 3.4 Trigonométrie (exercices de la séance 4)

| Q | Compétence | Erreurs types | Ancre | Exercices (min.) | Confirm |
|---|---|---|---|---|---|
| T1 | cos et sin d'un angle associé | T1a oublie le signe. T1b échange cos et sin (30° pour 60°). T1c signes du troisième quadrant | `cle-t1` ; tableau des valeurs remarquables absent | R.7 (5), R.6(b) (2) ; S.4(b), angle 150° | TR1, TR2 (partiel) |
| T2 | Angle aigu avec l'axe des x | T2a angle avec l'axe des y. T2b 360 − θ. Distracteur « angle donné » : pas d'ET propre | `cle-t1` | R.7 (5) | à écrire |
| T3 | Norme et angle vers coordonnées | T3a oublie le signe. T3b signes du troisième quadrant. T3c utilise ±1/2 au lieu de ±√2/2 | `cle-t2` ; aucune valeur pour 45° | R.6(a)(b) (3) ; S.4(a)(b) | TR1 |
| T4 | Angle d'un vecteur | T4a tangente seule. T4b 180 + θ au lieu de 180 − θ. T4c 360 − θ | `cle-t3` | R.7 (5), R.6(c) (2) | TR3 (cas d'un axe, partiel) |
| T5 | Sinus ou cosinus selon l'axe de mesure | T5a sinus au lieu de cosinus. T5b tangente. T5c divise par cos | `cle-t4` | R.5(d) (5) | TR4 |
| T6 | Norme et angle | T6a tangente seule. T6b 180 − θ. T6c norme = carré de la norme | `cle-t3` ; calcul de la norme dans `cle-t2` | R.6(c) (2), R.7 | à écrire |
| T7 | sin dans le quatrième quadrant | T7a oublie le signe. T7b angle aigu faux (30° pour 300° − 270°). T7c confond cos et sin | `cle-t1` | R.6(b) (2), R.7 | TR1 |

ET partagées avec vecteurs : T4a = T6a = V5a (tangente seule) ; T5a = V4a (sinus ou cosinus) ; T1a = T3a = T7a (signe oublié). Un code d'ET commun évite de proposer deux fois le même travail.
Compétences naturelles : angles associés (T1, T2, T7), coordonnées (T3, T5), angle d'un vecteur (T4, T6). Le thème respecte déjà « deux questions par compétence ».
Ancres manquantes : tableau des valeurs remarquables (30°, 45°, 60°) ; vecteur parallèle à un axe (TR3).
Banque de confirmation : trois réserves utilisables (TR1, TR3 partiel, TR4) ; TR2 (tangente d'un angle associé) teste une autre ET. Questions à écrire : T2, T6, et T1 si TR1 est affecté à T3.

## 4. Trames, mur de questions, zones

### 4.1 Les trames

Chaque trame est un déroulé de 60 minutes pour **toute la salle sur un seul thème** : accueil 1 min, QCM 9 min, notions clés 15 à 18 min, corrections ciblées 8 min, exercices 21 à 23 min (minuteur), clôture 4 min. Les étudiants qui ne sont pas sur le thème n'ont pas de tâche prévue : seule la diapositive d'accueil du deck `remed_accueil` dit « soit tu m'écoutes, soit tu travailles en autonomie, avec les slides et les exercices ». Seul le bloc d'exercices est individuel.

Réutilisation dans le dispositif en zones :

| Élément de la trame | Devenir |
|---|---|
| Colonnes « Ce que je dis » et « Ce que je montre » des notions clés (2 à 4 min chacune) | Interventions courtes à la demande dans la zone du thème, une par ET ou groupe d'ET (la diapositive `cle-*` en est le support, ancre de l'ET) |
| Seuils de décision (≥ 80 %, 60-79 %, < 60 %) | Règle de circulation de l'enseignant : aller d'abord à la zone dont l'effectif est le plus grand. Pas de pourcentage par question sans Wooclap |
| Tableau « Résultats du QCM à remplir » | Remplacé par le corrigé enseignant avec tableau de décompte (livret) |
| Section 4 « QCM → exercices, écarts de couverture » | Point de départ du tableau ET → exercices (§3). Les écarts de la trame sont repris en §5 |
| Section 6 « Questions du mur, à trier » | Devient la file de la zone « questions libres » |
| Minuteur (`et-box`, 21 à 23 min) | Réutilisable pour le « mode séance » (chronomètre) |

### 4.2 Le mur de questions devient la zone « questions libres »

État actuel (deck `remed_accueil`) : mur Wooclap (code XELAEPI, QR), 2 à 3 questions par personne, vote, « je ne répondrai pas à toutes », aucune réponse écrite ensuite. Les réponses se donnent en plénière, 4 min en fin de séance.

Dans le dispositif :

1. Le mur reste ouvert pendant tout le travail en zones. Les étudiants qui ont un plan vide ou une question hors plan y vont.
2. La zone « questions libres » traite les questions les plus votées, en petit groupe, au lieu d'une plénière de 4 minutes.
3. Chaque question est rattachée, après coup, à une ET existante ou à une nouvelle. Les nouvelles ET alimentent la banque (une question sans ET devient un candidat de distracteur).
4. Le principe « pas de réponse écrite » se conserve : le recueil de corrigés ne contient que les tests et les exercices.

Le deck d'accueil n'est plus la porte d'entrée : « Un seul code, quatre thèmes » et « Que faire quand le QCM est fini ? » sont remplacés par la page « Mon parcours ». Le Wooclap OBMKFUU (28 questions) peut rester comme repli sans écran ; le diag passe sur le site.

## 5. Synthèse

### 5.1 Réutilisable tel quel

| Élément | Où | Usage dans le dispositif |
|---|---|---|
| 28 questions du noyau, avec bonne réponse et explication par distracteur | `01-remediation.qmd` | Banque de diag (après ajout de « Je ne sais pas ») ; explications = constats d'ET |
| 17 questions de réserve | `02-annexe.qmd` | Banque de confirm partielle (§3) |
| Diapositives de notions clés (`contrat-*`, `cle-v*`, `cle-f*`, `cle-t*`) | decks | Ancres « théorie » (réserves de §3, §5.2 point 9) et supports d'interventions en zone |
| Tableaux « QCM → exercices » des decks et sections 4 des trames | decks, trames | Table ET → exercices à compléter |
| Exemples sourcés SNCB, MSD, Tanaka, OMS | logique, fonctions | Énoncés de diag et de confirm |
| Exercices de la séance 5 (3 indices, solution, piège) et S/T de la séance 4 | `seances/` | Pool d'exercices des plans |
| Ancres `#exercice-S1`, `#exercice-R3` | `exercice.lua` | Liens des plans, après stabilisation (§5.2 point 6) |
| Slide du mur, minuteur `et-box` | `remed_accueil`, decks | Zone « questions libres », mode séance |

### 5.2 À adapter (modification précise)

1. **Fichier de données par thème.** Extraire des trois copies : énoncé, quatre choix, ET de chaque distracteur (une phrase de constat tirée de l'explication existante, une phrase de rectification), ancre, exercices, minutes. Générer ensuite Wooclap (si conservé), la diapositive Q du deck et la réserve de l'annexe.
2. **Ajouter « Je ne sais pas »** comme cinquième choix de toutes les questions, relié à la théorie.
3. **Codes d'ET** (L1, V4a, F2c, T5a) et fusion des ET partagées (§3.4).
4. **Calculatrice.** Fonctions Q2 : masse de 81 kg, IMC 25 kg/m², `h² = 81/25 = 3,24`, `h = 1,8 m` ; distracteurs : `± 1,8 m`, `3,24 m`, `h = 5/9 m`. Vecteurs Q4 : réponse « 25√3 N » avec distracteurs `25 N`, `50 N`, `50√3 N`. Annexe vecteurs R.4(c) : conserver `√13`, sans valeur décimale.
5. **Indices en trois niveaux** sur les exercices utilisés : séance 4 R.1 à R.12 (un seul « Indice » : le séparer en théorie, question, étape) ; séance 1 R.2, R.3, R.6, R.8, R.9, R.10, R.14 (un ou deux indices). Pour vecteurs et trigo, préférer d'abord S.4, S.5, S.7, S.8 de la séance 4, déjà à trois niveaux.
6. **Identifiants stables.** Ajouter un identifiant optionnel dans le titre `Exercice|Catégorie|niveau|Objectif` (par exemple un cinquième champ lu par `exercice.lua` pour l'ancre), en gardant la numérotation affichée. Les parties (a)(b)(c) reçoivent un sous-identifiant pour l'affectation aux ET.
7. **Annexes.** Pour les exercices du plan : réponse finale en tête de chaque partie, puis étapes, puis piège ; générer depuis la source des exercices, pas depuis une copie.
8. **Sources des exemples inventés** (vecteurs, trigo) : remplacer par des données réelles et sourcées. Aucune source n'est proposée ici sans vérification.
9. **Ancres de théorie à préciser.** Vecteurs : ajouter une diapositive ou une section « colinéarité » et une phrase « retrancher = ajouter l'opposé ». Fonctions : un exemple dans `cle-f3` pour Dom(g ∘ f). Trigo : tableau des valeurs remarquables. Logique : négation de « au moins 60 minutes ». Pour le site, découper les decks en pages légères par ancre (§2, point 14).
10. **Vocabulaire.** Confirmer dans le cours théorique « suffisante », « nécessaire », « tenue », « rompue » (§2, point 13).
11. **Minutes.** Remplacer la règle ★ par des durées mesurées au pilote. Avec les valeurs de §3, la somme dédoublonnée de tous les exercices d'un thème est d'environ 25 à 40 min : le seuil « long » (50 min) n'est jamais atteint tant que « Je ne sais pas » ne renvoie pas à la théorie. Les seuils sont à recalibrer par thème (décision ouverte 2).

### 5.3 Ce qui manque

| Thème | Questions de diag à ajouter | Questions de confirm à écrire | Exercices à écrire ou à compléter | Ancres à créer |
|---|---|---|---|---|
| Logique | « Je ne sais pas » ×7 | Q2, Q5 ; contrôle des distracteurs de R1, R3, R4, R5 | Engagement réel ; α faux ; déduction par contraposée ; suffisant et nécessaire ; indices 3 niveaux sur 7 exercices | Négation d'une condition numérique |
| Vecteurs | idem | 6 (V1, V2, V3, V5, V6, V7) | Angle depuis la verticale ; produit vectoriel (si gardé) ; indices 3 niveaux sur R.1 à R.12 ou usage de S | Colinéarité ; retrancher |
| Fonctions | idem | 6 (F1, F3, F4, F5, F6, F7) ; F2 depuis FR4 | Aucun nouvel exercice si S.5 et S.6(a) sont admis | Exemple de Dom(g ∘ f) |
| Trigo | idem | T2, T6 ; T1 | Sinus et cosinus de 150°, 210°, 300° sans calculatrice ; vecteur parallèle à un axe | Valeurs remarquables |

Pour tous les thèmes : minutes par exercice, lettre, couleur et forme de zone, phrase « acquis » par compétence, fichier de calendrier (logique : séance 1 ; vecteurs et trigo : séance 4 ; fonctions : séance 5).

## 6. Thème pilote et ordre de travail

### 6.1 Thème recommandé : la logique

Raisons :

1. Le doc de projet le désigne comme candidat, avec des erreurs déjà observées en séance (la trame cite 56 % de réussite à la contraposée et 67 % à la négation aux quiz Moodle de la séance 1) : les valeurs de départ des seuils peuvent être calibrées sur du réel.
2. Données déjà sourcées (SNCB, MSD), énoncés conformes au standard.
3. Sur 7 ET groupées, 4 ont déjà une question de confirm quasi parallèle (Réserves 1, 3, 4, 5) : il reste 2 questions à écrire, contre 6 pour vecteurs et fonctions.
4. La théorie forme une suite unique de 13 diapositives (`contrat-1` à `contrat-10`, `sn1` à `sn3`), avec des ancres déjà posées.
5. Les erreurs sont conceptuelles et de durées inégales (lecture d'une table : 3 min ; déduire par contraposée : 8 min), ce qui met le plan à l'épreuve.

Coût : quatre exercices à écrire ou compléter (suffisant et nécessaire, engagement réel, α faux, déduction) et sept exercices à passer à trois indices.

Alternative si le coût d'écriture d'exercices doit être minimal : **fonctions**. Aucun exercice à écrire (S.5, S.6(a) comblent F7 et F4), indices déjà à trois niveaux, données sourcées ; en contrepartie 6 questions de confirm à écrire et le calcul de Q2 à corriger. Ordre conseillé pour les thèmes suivants : fonctions, trigo, vecteurs (trigo avant vecteurs, qui réutilise ses compétences).

### 6.2 Ordre de travail du pilote (logique)

| # | Étape | Livrable | Modèle |
|---|---|---|---|
| 1 | Figer le schéma de thème et son validateur (étape 1 du doc de projet) | Schéma, validateur | Modèle courant (architecture) |
| 2 | Convertir les 7 Q + 5 réserves vers le schéma : codes d'ET, constats, rectifications, ancres, « Je ne sais pas » | `themes/logique.yml` | Sonnet |
| 3 | Vérifier le vocabulaire dans le cours théorique | Liste validée | Toi |
| 4 | Écrire Q2 et Q5 de confirm ; vérifier les distracteurs de R1, R3, R4, R5 | Banque confirm complète | Modèle courant (contenu mathématique) |
| 5 | Écrire les quatre exercices manquants, passer R.2, R.3, R.6, R.8, R.9, R.10, R.14 à trois indices, ajouter les identifiants stables | Exercices de séance 1 | Modèle courant pour l'écriture ; Sonnet pour la restructuration |
| 6 | Affecter exercices et minutes aux ET, dédoublonner | Table ET → exercices | Sonnet |
| 7 | Générer le site (diag, plan, confirm) et le livret | Pages, PDF | Sonnet |
| 8 | Relecture de toutes les questions avant impression | Validation | Toi |
| 9 | Séance pilote : relever la répartition réelle des réponses par distracteur, la durée réelle des exercices | Mesures | Toi |

## 7. Décisions ouvertes

1. Regrouper les compétences pour obtenir deux questions chacune (logique : lire le contrat Q1-Q3, réciproque et contraposée Q4-Q5, négation, suffisant et nécessaire) ou accepter une question par compétence avec moindre fiabilité. Seule la trigo respecte déjà deux questions par compétence.
2. Seuils court, intermédiaire, long : 20 et 50 min ne sont jamais dépassés avec les valeurs de §3.
3. Les exercices S et T entrent-ils dans les plans, ou seulement R ? Le §3 suppose qu'ils entrent.
4. Faut-il conserver le Wooclap OBMKFUU comme repli sans écran ?
5. Le fichier `docs/articulation-remediation.md` n'est pas dans `BOOK_IGNORE_TOP` de `incremental.py` : son ajout change l'empreinte du site et force un rendu complet. Ajouter `docs` à cette liste, ou déplacer le fichier dans `slides/`, est à décider.

[^sncb]: SNCB, « Réclamation pour retard en train : compensation », belgiantrain.be, consulté le 13 octobre 2026 selon les decks ; énoncé simplifié.
[^msd]: Manuel MSD, version professionnelle, « Revue générale du diabète sucré », msdmanuals.com, consulté le 13 octobre 2026 selon les decks ; critère simplifié.
[^tanaka]: Tanaka, Monahan et Seals, J. Am. Coll. Cardiol. 37(1), 2001, formule simplifiée, selon la trame fonctions.
[^oms]: OMS, WHO Technical Report Series 894, 2000 (indice de masse corporelle), selon la trame fonctions.
