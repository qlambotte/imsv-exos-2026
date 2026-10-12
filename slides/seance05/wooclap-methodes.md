# Wooclap — Méthodes (questions ouvertes)

Un événement Wooclap, **type « question ouverte »** (texte libre, pas de QCM) : à chaque étape,
les étudiant·es écrivent la règle avec leurs mots, les réponses s'affichent à l'écran, et tu en
fais la synthèse à voix haute. Ce document donne, pour chaque question, ce vers quoi orienter la synthèse.

---

## Méthode 1 — Retrouver l'entrée à partir de la sortie

### Question d'ouverture [O3]

**Question à coller :**
> Avec tes mots : comment retrouves-tu la valeur de départ d'une formule quand tu connais le résultat ?

**Cible de synthèse :** on remplace la sortie par sa valeur dans la formule, puis on **défait les
opérations dans l'ordre inverse**. Les réponses « on essaie des valeurs » sont l'occasion de dire que
la méthode évite de tâtonner.

### Étape 1

**Question à coller :**
> Un thermomètre américain indique $104$ °F et la conversion est $F = 1{,}8\,C + 32$. Qu'est-ce qui est donné, et qu'est-ce qui est cherché ?

**Cible de synthèse :** la sortie $F = 104$ est donnée, l'entrée $C$ est cherchée.

### Étape 2

**Question à coller :**
> Écris l'équation obtenue quand on remplace la sortie par sa valeur.

**Cible de synthèse :** $104 = 1{,}8\,C + 32$.

### Étape 3

**Question à coller :**
> Résous cette équation. Dans quel ordre défais-tu les opérations ?

**Cible de synthèse :** la formule multiplie par $1{,}8$ puis ajoute $32$ ; on soustrait donc $32$
d'abord, puis on divise par $1{,}8$ : $C = 72 / 1{,}8 = 40$. Les réponses qui divisent d'abord
montrent le piège : $104/1{,}8 - 32 \approx 25{,}8$ ne redonne pas $104$.

### Étape 4

**Question à coller :**
> Comment vérifies-tu ton résultat ?

**Cible de synthèse :** on remet $C = 40$ dans la formule : $1{,}8 \cdot 40 + 32 = 104$ ; on vérifie aussi
que la valeur appartient au domaine.

### Plusieurs solutions

**Question à coller :**
> $f(x) = x^2 - 4$, où $x$ est une longueur en cm. Quelle entrée donne la sortie $5$ ?

**Cible de synthèse :** $x^2 = 9$ donne $3$ et $-3$ ; une longueur n'est pas négative, donc on garde $3$ cm. Sans contexte, deux solutions resteraient possibles : pas de réciproque sans restreindre le domaine.

### Pour aller plus loin

**Question à coller :**
> Écris la formule qui donne $C$ à partir de $F$, puis convertis $98{,}6$ °F.

**Cible de synthèse :** $C = \dfrac{F - 32}{1{,}8}$ (fonction réciproque) ; $98{,}6$ °F correspond à $37$ °C.

---

## Méthode 2 — Étudier le signe d'une fonction

### Question d'ouverture [O2]

**Question à coller :**
> Avec tes mots : comment sais-tu où une fonction est positive et où elle est négative ?

**Cible de synthèse :** on cherche les **racines**, qui découpent le domaine en intervalles, puis on
détermine le signe sur chaque intervalle. Les réponses « on regarde le graphe » sont valables : c'est un autre registre
de la même information.

### Étape 1

**Question à coller :**
> $f(x) = \dfrac{x - 1}{x + 2}$. Quel est son domaine, et quelles sont ses racines ?

**Cible de synthèse :** le dénominateur s'annule en $-2$, donc $\mathit{Dom}(f) = \mathbb{R} \setminus \{-2\}$ et la valeur $-2$ est exclue ; la seule racine est $1$.

### Étape 2

**Question à coller :**
> Quels points découpent le domaine en intervalles ? Écris ces intervalles.

**Cible de synthèse :** la racine $1$ **et** la valeur exclue $-2$ : $]-\infty, -2[$, $]-2, 1[$ et $]1, +\infty[$. Les réponses qui oublient $-2$ montrent pourquoi la méthode place aussi les valeurs exclues.

### Étape 3

**Question à coller :**
> Choisis un point dans chaque intervalle et donne le signe de $f$ en ce point.

**Cible de synthèse :** $f(-3) = 4$, $f(0) = -\frac12$, $f(2) = \frac14$ : signes $+$, $-$, $+$.

### Étape 4

**Question à coller :**
> Écris une phrase de conclusion.

**Cible de synthèse :** $f$ est strictement positive sur $]-\infty, -2[$ et sur $]1, +\infty[$, strictement négative sur $]-2, 1[$ et nulle en $1$ ; elle change de signe en $-2$ sans s'y annuler.

### Piège

**Question à coller :**
> $h(x) = x\,(x - 2)^2$ change-t-elle de signe en $2$ ? Pourquoi ?

**Cible de synthèse :** non : le facteur $(x - 2)^2$ est positif ou nul des deux côtés de $2$, donc
$h$ garde le signe de $x$ ($h(1) = 1$ et $h(3) = 3$).

---

## Réglages Wooclap suggérés

- Type de question : **« Question ouverte »** (texte libre), pas « Nuage de mots ».
- Affichage : réponses visibles au fur et à mesure (mode mur de réponses).
- Pas de minutage strict : le rythme est donné par la discussion.
