# Wooclap — Méthodes (questions ouvertes)

Un événement Wooclap, **type « question ouverte »** (texte libre, pas de QCM) : à chaque étape,
les étudiant·es écrivent la règle avec leurs mots, réponses affichées à l'écran, tu en fais la
synthèse à voix haute. Ce document donne, pour chaque question, ce vers quoi orienter la synthèse.

---

## Méthode 1 — De la norme et de l'angle aux coordonnées

### Question d'ouverture [O3]

**Question à coller :**
> Comment obtiens-tu les coordonnées d'un vecteur dont tu connais la norme et l'angle avec
> l'horizontale ?

**Cible de synthèse :** on part du **cercle trigonométrique** : le point d'angle $\theta$ est
$(\cos\theta, \sin\theta)$, un vecteur de norme $1$ ; on le « met à l'échelle » en multipliant par
la norme. Les réponses « Pythagore » sont l'occasion de dire que Pythagore sert dans l'autre sens
(des coordonnées vers la norme).

### Étape 1

**Question à coller :**
> Une force de $8$ N fait un angle de $150°$ avec l'horizontale. Dans quel quadrant est-elle, et
> quels signes attends-tu pour ses coordonnées ?

**Cible de synthèse :** deuxième quadrant, $F_x < 0$ et $F_y > 0$. Dessiner d'abord donne un
contrôle pour la fin.

### Étape 2

**Question à coller :**
> Écris les coordonnées de la force à l'aide de $\cos$ et $\sin$.

**Cible de synthèse :** $\vec F = (8\cos 150°,\ 8\sin 150°)$ : même direction et même sens que
le point du cercle, norme $8$ fois plus grande.

### Étape 3

**Question à coller :**
> Que valent $\cos 150°$ et $\sin 150°$, sans calculatrice ? En déduire les coordonnées.

**Cible de synthèse :** $150° = 180° - 30°$, symétrique de $30°$ par rapport à l'axe vertical :
$\cos 150° = -\frac{\sqrt3}{2}$ et $\sin 150° = \frac12$, d'où $\vec F = (-4\sqrt3,\ 4)$.

### Étape 4

**Question à coller :**
> Comment vérifies-tu ton résultat ?

**Cible de synthèse :** les **signes** correspondent au quadrant, et la **norme** des coordonnées
redonne $8$ : $\sqrt{48 + 16} = 8$.

### Et dans l'autre sens

**Question à coller :**
> Une algue est entraînée à la vitesse $(-1, -\sqrt3)$ m/s. Quelle est la valeur de cette vitesse,
> et quel angle fait-elle avec l'horizontale ?

**Cible de synthèse :** norme $\sqrt{1 + 3} = 2$ m/s ; troisième quadrant ; $\tan\theta = \sqrt3$,
angle aigu $60°$, donc $\theta = 180° + 60° = 240°$. Les réponses « $60°$ » montrent pourquoi la
tangente seule ne suffit pas : le quadrant tranche.

---

## Méthode 2 — Calculer et interpréter un produit scalaire

### Question d'ouverture [O2]

**Question à coller :**
> Que t'apprend le **signe** du produit scalaire de deux vecteurs ?

**Cible de synthèse :** comme $\vec u \cdot \vec v = \Vert\vec u\Vert\,\Vert\vec v\Vert\cos\theta$ et
que les normes sont positives, le signe est celui de $\cos\theta$ : positif si l'angle est aigu,
nul si les vecteurs sont orthogonaux, négatif s'il est obtus.

### Étape 1

**Question à coller :**
> $\vec u = (\sqrt3, 1)$ et $\vec v = (0, 2)$. Sans calculer, l'angle entre eux est-il aigu, droit
> ou obtus ?

**Cible de synthèse :** $\vec u$ fait $30°$ avec l'axe des $x$, $\vec v$ est vertical : angle
aigu, on attend un produit scalaire positif.

### Étape 2

**Question à coller :**
> Calcule $\vec u \cdot \vec v$.

**Cible de synthèse :** $\sqrt3 \cdot 0 + 1 \cdot 2 = 2 > 0$, comme prévu.

### Étape 3

**Question à coller :**
> Déduis-en l'angle entre $\vec u$ et $\vec v$.

**Cible de synthèse :** $\cos\theta = \frac{2}{2 \cdot 2} = \frac12$, donc $\theta = 60°$ ; contrôle
sur le dessin : $90° - 30° = 60°$.

### Étape 4

**Question à coller :**
> Que représente $\Vert\vec v\Vert\cos\theta$ sur le dessin ?

**Cible de synthèse :** la longueur (signée) de la projection orthogonale de $\vec v$ sur la droite
de $\vec u$, ici $\frac{\vec u \cdot \vec v}{\Vert\vec u\Vert} = 1$.

### Étape 5

**Question à coller :**
> Pour quelle valeur de $a$ le vecteur $(a, 3)$ est-il orthogonal à $\vec u$ ?

**Cible de synthèse :** produit scalaire nul : $\sqrt3\,a + 3 = 0$, donc $a = -\sqrt3$.

**Résultat final à faire apparaître :** calculer, lire le signe, en déduire l'angle, interpréter
comme une projection, tester l'orthogonalité.

---

## Réglages Wooclap suggérés

- Type de question : **« Question ouverte »** (texte libre), pas « Nuage de mots ».
- Affichage : réponses visibles au fur et à mesure (mode mur de réponses).
- Pas de minutage strict : le rythme est donné par la discussion.
