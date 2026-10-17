# Wooclap — Méthodes (questions ouvertes)

Un événement Wooclap, **type « question ouverte »** (texte libre, pas de QCM) : à chaque étape,
les étudiant·es écrivent la règle avec leurs mots, les réponses s'affichent à l'écran, et tu en
fais la synthèse à voix haute. Ce document donne, pour chaque question, ce vers quoi orienter la synthèse.

---

## Calculer une fonction réciproque

### Question d'ouverture [O6]

**Question à coller :**
> Avec tes mots : comment obtiens-tu la formule de la fonction qui « défait » une fonction donnée ?

**Cible de synthèse :** on pose $y = f(x)$, on isole $x$, puis on échange les noms $x$ et $y$.
Si des réponses évoquent « une condition sur la fonction », s'en servir pour introduire l'injectivité.

### Étape 1

**Question à coller :**
> $h(x) = x^2 - 4$. Quelles entrées donnent la sortie $5$ ? La fonction « qui défait $h$ » existe-t-elle sur $\mathbb{R}$ ?

**Cible de synthèse :** $x = 3$ ou $x = -3$ ; $h(3) = h(-3)$, donc $h$ n'est pas injective sur $\mathbb{R}$ et n'a pas de réciproque.

### Étape 2

**Question à coller :**
> On trace le symétrique du graphe de $h$ par rapport à la droite $y = x$. Est-ce le graphe d'une fonction ?

**Cible de synthèse :** non : une droite verticale, par exemple $x = 5$, coupe la courbe en $(5\,;\,3)$ et $(5\,;\,-3)$ ; une même entrée aurait deux sorties.

### Étape 3

**Question à coller :**
> Comment restreindre le domaine de $h$ pour qu'elle devienne injective ?

**Cible de synthèse :** $x$ est une longueur, donc on garde $[0,\,+\infty[$ (la restriction à $]-\infty,\,0]$ conviendrait aussi, avec l'autre signe de racine).

### Étape 4

**Question à coller :**
> Écris la réciproque de la restriction : isole $x$, puis échange les noms.

**Cible de synthèse :** $x^2 = y + 4$, $x = \sqrt{y + 4}$ car $x \geq 0$ ; $h^{-1}(x) = \sqrt{x + 4}$, de domaine $[-4,\,+\infty[$.

### Étape 5

**Question à coller :**
> Comment vérifies-tu ton résultat ?

**Cible de synthèse :** $h^{-1}(h(3)) = \sqrt{9} = 3$ ; le point $(0\,;\,-4)$ devient $(-4\,;\,0)$ ; la courbe est le symétrique du graphe par rapport à $y = x$.

### Pour aller plus loin

**Question à coller :**
> $f(x) = 1{,}8\,x + 32$ convertit des °C en °F. Écris la formule qui donne les °C à partir des °F, puis convertis $98{,}6$ °F.

**Cible de synthèse :** $f^{-1}(x) = \dfrac{x - 32}{1{,}8}$, sans restriction car $f$ est injective ; $98{,}6$ °F correspond à $37$ °C.

---

## Réglages Wooclap suggérés

- Type de question : **« Question ouverte »** (texte libre), pas « Nuage de mots ».
- Affichage : réponses visibles au fur et à mesure (mode mur de réponses).
- Pas de minutage strict : le rythme est donné par la discussion.
