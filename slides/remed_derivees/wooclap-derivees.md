# Wooclap — QCM de remédiation : variations, limites et dérivées (séance 7)

Un événement Wooclap, 9 questions **QCM à réponse unique**, dans l'ordre ci-dessous (noyau), une par objectif de la séance 7 (O1 à O9). Questions nouvelles, rédigées pour cette remédiation : elles ne reprennent pas les questions du QCM Moodle de la séance 7. Les distracteurs correspondent aux erreurs classiques ; tous les résultats ont été vérifiés par script. En fin de fichier : 4 questions de réserve, corrigées dans le deck « Annexe ».

Code Wooclap : **OBMKFUU** (version en autonomie : un seul événement pour tous les thèmes ; ajouter ce thème à l'événement).

Une seule question comporte une figure (Q3) : importer l'image indiquée dans la question.

---

## Q1 — Variation relative et taux moyen

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une culture passe de $200$ cellules à $t = 1$ h à $250$ cellules à $t = 3$ h. Quelle est la variation relative sur $[1,\,3]$ ?

**Choix :**
- ( ) $+20\,\%$
- (X) $+25\,\%$
- ( ) $+50\,\%$
- ( ) $+25$ cellules par heure

**Justification (à dire à voix haute après le vote) :** $\Delta_{[1,3]} = 50$, et $\dfrac{50}{200} = 0{,}25$ : on divise par la valeur de départ.

---

## Q2 — Taux moyen et sécante

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> On sait que $f(1) = 2$ et $f(5) = 10$, donc $T_{[1,5]}(f) = \dfrac{10 - 2}{5 - 1} = 2$. Que représente ce nombre sur le graphe de $f$ ?

**Choix :**
- (X) La pente de la droite qui passe par $(1\,;\,2)$ et $(5\,;\,10)$.
- ( ) La pente de la tangente au graphe de $f$ en $x = 3$.
- ( ) La pente de la tangente au graphe de $f$ en $x = 1$.
- ( ) La variation absolue de $f$ sur $[1,\,5]$.

**Justification (à dire à voix haute après le vote) :** $T_{[a,b]}(f)$ est la pente de la sécante qui passe par $(a\,;\,f(a))$ et $(b\,;\,f(b))$.

---

## Q3 — Limite et image

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> On considère la fonction $g$ représentée ci-dessous. Que valent $\lim\limits_{x \to 3} g(x)$ et $g(3)$ ?

**Image à importer :** `img/q3-limite.png` (version PNG de la figure du deck).

**Choix :**
- ( ) $\lim\limits_{x \to 3} g(x) = 1$ et $g(3) = 1$
- ( ) $\lim\limits_{x \to 3} g(x) = 5$ et $g(3) = 5$
- (X) $\lim\limits_{x \to 3} g(x) = 5$ et $g(3) = 1$
- ( ) $g$ n'a pas de limite en $3$.

**Justification (à dire à voix haute après le vote) :** Limite à gauche et à droite : $5$. L'image est l'ordonnée du point plein : $1$. Comme $5 \neq 1$, $g$ n'est pas continue en $3$.

---

## Q4 — Propriétés algébriques des limites

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> On sait que $\lim\limits_{x \to 2} f(x) = 3$, $\lim\limits_{x \to 2} g(x) = 2$, $f(2) = 5$ et $g(2) = 0$. Soit $h(x) = x^{2} - 3$, continue en tout réel. Que vaut $\lim\limits_{x \to 2} \sqrt{\dfrac{h\big(f(x)\big) + f(x)}{g(x)^{2}}}$ ?

**Choix :**
- ( ) $\dfrac{9}{4}$
- ( ) $3$
- ( ) La limite n'existe pas : $g(2) = 0$ annule le dénominateur.
- (X) $\dfrac{3}{2}$

**Justification (à dire à voix haute après le vote) :** Numérateur $\to 6 + 3 = 9$, dénominateur $\to 4$, puis la racine : $\sqrt{9/4} = 3/2$.

---

## Q5 — Asymptotes

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> On sait que $\lim\limits_{x \to +\infty} f(x) = 4$ et que $\lim\limits_{x \to 1^+} f(x) = +\infty$. Quelles droites sont des asymptotes au graphe de $f$ ?

**Choix :**
- ( ) La droite $x = 4$ et la droite $y = 1$.
- (X) La droite $y = 4$ et la droite $x = 1$.
- ( ) Seulement la droite $y = 4$.
- ( ) Seulement la droite $x = 1$.

**Justification (à dire à voix haute après le vote) :** Limite finie $L$ à l'infini : asymptote $y = L$. Limite infinie en $a$ : asymptote $x = a$.

---

## Q6 — Continue ou dérivable

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Soit $f(x) = |x - 1|$. En $x = 1$, la fonction $f$ est :

**Choix :**
- (X) continue, mais pas dérivable.
- ( ) continue et dérivable.
- ( ) dérivable, mais pas continue.
- ( ) ni continue, ni dérivable.

**Justification (à dire à voix haute après le vote) :** Continue : la limite vaut $f(1) = 0$. Non dérivable : les pentes à gauche et à droite, $-1$ et $1$, sont différentes.

---

## Q7 — Dérivée et pente de la tangente

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Le nombre de cellules d'une culture est $N(t)$, avec $t$ en heures. La tangente à la courbe en $t = 3$ passe par $(3\,;\,50)$ et $(5\,;\,110)$. Que vaut $N'(3)$ ?

**Choix :**
- ( ) $50$ cellules
- ( ) $60$ cellules par heure
- (X) $30$ cellules par heure
- ( ) $110$ cellules par heure

**Justification (à dire à voix haute après le vote) :** $N'(3)$ est la pente de la tangente : $\dfrac{110 - 50}{5 - 3} = 30$ cellules par heure.

---

## Q8 — Plausibilité d'une dérivée

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Le graphe de $f$ est une parabole tournée vers le haut, de sommet $(2\,;\,-4)$. Quelle expression de $f'$ est plausible ?

**Choix :**
- ( ) $f'(x) = 4 - 2x$
- ( ) $f'(x) = 2x + 4$
- ( ) $f'(x) = x^{2} - 4$
- (X) $f'(x) = 2x - 4$

**Justification (à dire à voix haute après le vote) :** Contrôle du signe et du zéro : $f'$ négative avant $2$, nulle en $2$, positive après.

---

## Q9 — Dérivée seconde

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Un mobile a pour position $p(t) = 5t^{2}$, en mètres, avec $t$ en secondes. On admet que $p'(t) = 10t$. Que vaut $p''(t)$, avec son unité ?

**Choix :**
- ( ) $10t$ m/s
- (X) $10$ m/s²
- ( ) $10$ m/s
- ( ) $0$ m/s²

**Justification (à dire à voix haute après le vote) :** $p''(t) = 10$ : la vitesse augmente de $10$ m/s par seconde ; l'unité est m/s².

---

# Questions de réserve

## Réserve 1 — Une diminution en pourcentage

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une grandeur passe de $80$ à $60$. Quelle est sa variation relative ?

**Choix :**
- ( ) $+25\,\%$
- ( ) $-20\,\%$
- (X) $-25\,\%$
- ( ) environ $-33\,\%$

**Justification (à dire à voix haute après le vote) :** $\dfrac{60 - 80}{80} = -0{,}25$.

---

## Réserve 2 — Limite d'une fonction définie par morceaux

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Soit $f(x) = x + 1$ si $x < 2$ et $f(x) = 5 - x$ si $x \geq 2$. Que vaut $\lim\limits_{x \to 2} f(x)$ ?

**Choix :**
- (X) $3$
- ( ) Elle n'existe pas, car $f$ est définie par deux formules.
- ( ) $6$
- ( ) $2$

**Justification (à dire à voix haute après le vote) :** Limite à gauche $3$, limite à droite $3$ : la limite vaut $3$.

---

## Réserve 3 — Quotient et limite nulle au dénominateur

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> On sait que $\lim\limits_{x \to 1} f(x) = 2$ et $\lim\limits_{x \to 1} g(x) = 0$. Que peut-on affirmer sur $\lim\limits_{x \to 1} \dfrac{f(x)}{g(x)}$ ?

**Choix :**
- ( ) La limite vaut $0$.
- ( ) La limite vaut $2$.
- ( ) La limite vaut $+\infty$.
- (X) La règle du quotient ne s'applique pas : on ne peut pas conclure avec elle.

**Justification (à dire à voix haute après le vote) :** La limite du dénominateur est nulle : la règle du quotient ne s'applique pas.

---

## Réserve 4 — Signes de la vitesse et de l'accélération

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Un mobile avance dans le sens positif d'un axe en accélérant. On note $p(t)$ sa position. Que peut-on dire de $p'(t)$ et de $p''(t)$ ?

**Choix :**
- ( ) $p'(t) > 0$ et $p''(t) < 0$
- (X) $p'(t) > 0$ et $p''(t) > 0$
- ( ) $p'(t) < 0$ et $p''(t) > 0$
- ( ) $p'(t) < 0$ et $p''(t) < 0$

**Justification (à dire à voix haute après le vote) :** Avancer : $p' > 0$ ; accélérer : $p'' > 0$.
