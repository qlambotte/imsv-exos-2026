# Projet IMSV — instructions permanentes

CONTEXTE. Je maintiens un site Quarto (type « book ») + des PDF d'exercices pour le cours
« Introduction Mathématique aux Sciences de la Vie » (IMSV, UMONS), en français, pour des
étudiant·es de première année. Le dépôt est sur ma machine (accessible via le pont) :
/home/quentin/Documents/UMONS/2026-2027/Q1/imsv-exos-2026

ARCHITECTURE (pour ne pas la redécouvrir).
- Source unique : des fragments `seances/**/_*.qmd` inclus par les pages. Ne jamais dupliquer un
  contenu — éditer le fragment.
- Filtres Lua : `exercice.lua` (numérotation automatique des exercices par catégorie + boîtes
  d'aide en PDF) ; `methode.lua` (cartes de méthode, site + PDF).
- Les PDF sont produits par `post-render.py`, qui appelle les `build-*.sh` (typst, copie à plat).
  Tout est générique : ça boucle sur les séances, rien n'est codé en dur.
- « Boîte à outils » : une page d'accueil qui liste les séances (tableau dynamique) ; chaque séance
  a sa page de méthodes. Feuilles à compléter par séance + une feuille vierge.
- La taxonomie des exercices (socle / transfert / renforcement) est INTERNE : elle n'apparaît pas
  sur le site.

STYLE D'ÉCRITURE.
- Bon français, phrases complètes. Jamais de style télégraphique.
- Ne pas reformuler pour reformuler : le terme juste suffit, pas de glose entre parenthèses ni de
  « le but est de… » qui répète. SURTOUT PAS dans les titres et les libellés — un titre est court
  et net, sans explicatif accolé.
- Coller à mon style : sobre, direct, tutoiement de l'étudiant, pédagogique mais pas bavard.
  Reprendre mes tournures existantes plutôt qu'en inventer.

SYMBOLIQUE ET CONTENU.
- Respecter la notation du cours théorique. N'introduire AUCUN terme ni symbole nouveau qui n'y
  figure pas (p. ex. ⟺ et non ≡ ; α, β pour les propositions ; capitales latines pour les ensembles).
  En cas de doute sur un symbole ou un terme, me demander plutôt qu'inventer.
- Aucune promesse sur l'examen : ne pas écrire « à l'examen », « hors examen », « programme »,
  « hors programme ». Pas de catégorie « dépassement ».
- Pas de calculatrice : les étudiant·es n'y ont pas droit en évaluation, donc chaque exercice doit
  être faisable « à la main » --- valeurs simples, racines et puissances « rondes », fractions
  qui tombent juste, pas de décimales à rallonge ni de calculs pénibles.

MANIÈRE DE TRAVAILLER (pour éviter les allers-retours).
- Corriger, ne pas régénérer : éditions ciblées dans les sources, et NE PAS relancer les builds —
  je lance `quarto render` et les commits git moi-même.
- Avant d'éditer, lire seulement le(s) fichier(s) concerné(s), pas tout le dépôt.
- Pas d'aperçus ni de captures (PDF, screenshots) sauf si je les demande.
- Pour un vrai changement de structure : me proposer l'approche en une ou deux phrases et attendre
  mon accord, plutôt que de construire puis refaire.
- Une seule source, zéro dérive : si une notion apparaît à plusieurs endroits (titres, gabarits),
  la corriger partout, y compris le modèle `seances/_modele/`.
- Ne jamais être complaisant : dis-moi franchement ce qui est bancal, propose mieux, signale les
  compromis.
- Si tu es bloqué : UNE seule question précise ; sinon avance avec l'hypothèse la plus raisonnable
  en l'annonçant.

MODÈLE.
- Au début de chaque tâche, dis-moi en une ligne si un modèle plus léger (Sonnet, voire Haiku)
  suffirait pour ce travail — typiquement : renommages, corrections de libellés, sed/regex,
  éditions ciblées. Réserve Opus au raisonnement, à l'architecture, au contenu mathématique délicat.
- Si une tâche lourde peut être déléguée à un sous-agent sur un modèle moins cher, propose-le avant de commencer la tâche.

