# Wooclap — QCM de remédiation : le calcul différentiel (séance 8)

Un événement Wooclap, 9 questions **QCM à réponse unique**, dans l'ordre ci-dessous (noyau), au moins une par objectif de la séance 8 (O1 à O6, AAV d'IMSV-8). Questions nouvelles, rédigées pour cette remédiation : elles ne reprennent ni les questions du QCM Moodle de la séance 8, ni les exemples des slides IMSV-8. Les distracteurs correspondent aux erreurs classiques ; tous les résultats ont été vérifiés par script. En fin de fichier : 3 questions de réserve, corrigées dans le deck « Annexe ».

Code Wooclap : **OBMKFUU** (version en autonomie : un seul événement pour tous les thèmes ; ajouter ce thème à l'événement, sous le titre « Le calcul différentiel »).

Aucune question ne comporte de figure.

---

## Q1 — Dérivée élémentaire et domaine (O1)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Soit $f(x) = 4\sqrt{x} - \dfrac{3}{x}$. Quelle proposition donne $f'(x)$ et le domaine de $f'$ ?

**Choix :**
- (X) $f'(x) = \dfrac{2}{\sqrt{x}} + \dfrac{3}{x^{2}}$, sur $\mathbb{R}^+_0$
- ( ) $f'(x) = \dfrac{2}{\sqrt{x}} - \dfrac{3}{x^{2}}$, sur $\mathbb{R}^+_0$
- ( ) $f'(x) = \dfrac{2}{\sqrt{x}} + \dfrac{3}{x^{2}}$, sur $\mathbb{R}^+$
- ( ) $f'(x) = 2\sqrt{x} + \dfrac{3}{x^{2}}$, sur $\mathbb{R}^+_0$

**Justification (à dire à voix haute après le vote) :** $4\sqrt{x} = 4x^{1/2}$ a pour dérivée $2x^{-1/2} = \dfrac{2}{\sqrt{x}}$, et $-3x^{-1}$ a pour dérivée $3x^{-2}$. Il faut $x > 0$ pour la racine au dénominateur. Distracteurs — « $f'(x) = \dfrac{2}{\sqrt{x}} - \dfrac{3}{x^{2}}$, sur $\mathbb{R}^+_0$ » : Erreur de signe : $\left(-3x^{-1}\right)' = -3 \cdot (-1)x^{-2} = +\dfrac{3}{x^{2}}$. « $f'(x) = \dfrac{2}{\sqrt{x}} + \dfrac{3}{x^{2}}$, sur $\mathbb{R}^+$ » : La formule n'est pas définie en $0$ : on divise par $\sqrt{x}$ et par $x^{2}$. « $f'(x) = 2\sqrt{x} + \dfrac{3}{x^{2}}$, sur $\mathbb{R}^+_0$ » : On a multiplié par l'exposant sans le diminuer de $1$ : $\left(x^{1/2}\right)' = \dfrac{1}{2}x^{-1/2}$.

**Exercices associés :** S.1, R.1, R.2.

---

## Q2 — Règle de Leibniz (O2)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut la dérivée de $f(x) = x^{3} \cdot e^{x}$ ?

**Choix :**
- (X) $(3x^{2} + x^{3}) \cdot e^{x}$
- ( ) $3x^{2} \cdot e^{x}$
- ( ) $3x^{2} + e^{x}$
- ( ) $x^{3} \cdot e^{x}$

**Justification (à dire à voix haute après le vote) :** Par la règle de Leibniz : $3x^{2} \cdot e^{x} + x^{3} \cdot e^{x}$. Distracteurs — « $3x^{2} \cdot e^{x}$ » : On a dérivé chaque facteur et multiplié les dérivées. Il manque la contribution $x^{3} \cdot e^{x}$. « $3x^{2} + e^{x}$ » : On a dérivé comme une somme : $f$ est un produit. « $x^{3} \cdot e^{x}$ » : Le facteur $e^{x}$ est égal à sa dérivée, mais le facteur $x^{3}$ change aussi.

**Exercices associés :** S.2, R.3.

---

## Q3 — Règle du quotient (O2)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut la dérivée de $f(x) = \dfrac{x + 1}{x - 1}$, pour $x \neq 1$ ?

**Choix :**
- (X) $-\dfrac{2}{(x - 1)^{2}}$
- ( ) $\dfrac{2}{(x - 1)^{2}}$
- ( ) $1$
- ( ) $\dfrac{2x}{(x - 1)^{2}}$

**Justification (à dire à voix haute après le vote) :** $\dfrac{1 \cdot (x - 1) - (x + 1) \cdot 1}{(x - 1)^{2}} = \dfrac{-2}{(x - 1)^{2}}$. Distracteurs — « $\dfrac{2}{(x - 1)^{2}}$ » : L'ordre du numérateur est inversé : c'est $u' \cdot v - u \cdot v'$. « $1$ » : C'est le quotient des dérivées $\dfrac{1}{1}$ : la dérivée d'un quotient n'est pas le quotient des dérivées. « $\dfrac{2x}{(x - 1)^{2}}$ » : Erreur de calcul au numérateur : $(x - 1) - (x + 1) = -2$, et non $2x$.

**Exercices associés :** S.2, R.3(c)(d), R.7(a).

---

## Q4 — Chain rule et exponentielle (O3)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut la dérivée de $f(x) = e^{x^{2} + 1}$ ?

**Choix :**
- (X) $2x \cdot e^{x^{2} + 1}$
- ( ) $e^{x^{2} + 1}$
- ( ) $(x^{2} + 1) \cdot e^{x^{2}}$
- ( ) $2x \cdot e^{2x}$

**Justification (à dire à voix haute après le vote) :** Fonction intérieure $g(x) = x^{2} + 1$, de dérivée $2x$ ; fonction extérieure $e^{y}$, de dérivée $e^{y}$. Donc $f'(x) = e^{x^{2} + 1} \cdot 2x$. Distracteurs — « $e^{x^{2} + 1}$ » : Il manque la multiplication par la dérivée de la fonction intérieure. « $(x^{2} + 1) \cdot e^{x^{2}}$ » : On a appliqué la règle des puissances à l'exposant : la variable est dans l'exposant, c'est une composée. « $2x \cdot e^{2x}$ » : On a remplacé l'exposant par sa dérivée : l'exponentielle garde la fonction intérieure, $e^{x^{2} + 1}$.

**Exercices associés :** S.3, R.4.

---

## Q5 — Chain rule et logarithme (O3)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut la dérivée de $f(x) = \ln(3x + 1)$, pour $x > -\tfrac{1}{3}$ ?

**Choix :**
- (X) $\dfrac{3}{3x + 1}$
- ( ) $\dfrac{1}{3x + 1}$
- ( ) $\dfrac{3}{x}$
- ( ) $\dfrac{1}{3x}$

**Justification (à dire à voix haute après le vote) :** Fonction intérieure $3x + 1$, de dérivée $3$ ; fonction extérieure $\ln(y)$, de dérivée $\dfrac{1}{y}$. Distracteurs — « $\dfrac{1}{3x + 1}$ » : Il manque la dérivée de la fonction intérieure, $3$. « $\dfrac{3}{x}$ » : On a mélangé la dérivée de $\ln(x)$ et celle de la fonction intérieure : $\ln$ reçoit $3x + 1$, pas $x$. « $\dfrac{1}{3x}$ » : On a oublié le terme $+1$ et la dérivée de la fonction intérieure.

**Exercices associés :** S.3, R.4(d), R.5(b).

---

## Q6 — Simplifier sans élargir le domaine (O4)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Soit $f(x) = \dfrac{x^{2} - 9}{x - 3}$. Quelle proposition est correcte ?

**Choix :**
- (X) $f'(x) = 1$, pour $x \neq 3$
- ( ) $f'(x) = 1$, sur $\mathbb{R}$
- ( ) $f'(x) = 2x$, pour $x \neq 3$
- ( ) $f'(x) = 0$, pour $x \neq 3$

**Justification (à dire à voix haute après le vote) :** $x^{2} - 9 = (x - 3)(x + 3)$, donc $f(x) = x + 3$ pour $x \neq 3$ : la simplification divise par $x - 3$, et $3$ reste exclu. Distracteurs — « $f'(x) = 1$, sur $\mathbb{R}$ » : La simplification a élargi le domaine : $f$ n'est pas définie en $3$, donc $f'$ non plus. « $f'(x) = 2x$, pour $x \neq 3$ » : C'est le quotient des dérivées, $\dfrac{2x}{1}$. « $f'(x) = 0$, pour $x \neq 3$ » : On a dérivé $x + 3$ comme une constante : seul le terme $3$ a une dérivée nulle.

**Exercices associés :** S.2 (k), R.6.

---

## Q7 — Contrôler une dérivée (O5)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Le volume d'air inspiré vaut $V(t) = 2\left(1 - e^{-3t}\right)$, en L, avec $t$ en secondes. Une étudiante obtient $V'(t) = -6e^{-3t}$. Quel contrôle montre que ce résultat est faux ?

**Choix :**
- (X) Le signe des pentes
- ( ) Le domaine
- ( ) L'unité
- ( ) Aucun : le résultat est correct.

**Justification (à dire à voix haute après le vote) :** $V$ est croissante, car $e^{-3t}$ diminue ; ses tangentes montent, donc $V'(t) > 0$. Or $-6e^{-3t} < 0$. La dérivée correcte est $V'(t) = 6e^{-3t}$. Distracteurs — « Le domaine » : $V$ et la proposition sont définies pour tout $t$ : le domaine ne détecte rien ici. « L'unité » : $6$ est en L/s (le facteur $3$ est en s$^{-1}$) : l'unité est correcte, c'est le signe qui est faux. « Aucun : le résultat est correct. » : La chain rule donne $\left(e^{-3t}\right)' = -3e^{-3t}$, donc $V'(t) = 2 \cdot \left(0 - (-3e^{-3t})\right) = 6e^{-3t}$.

**Exercices associés :** S.4, S.6, R.7.

---

## Q8 — Interpréter un taux (O6)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> La concentration d'un médicament vaut $C(t) = 20 \cdot e^{-0{,}1 t}$, en mg/L, avec $t$ en heures. Que vaut $C'(0)$ ?

**Choix :**
- (X) $-2$ mg/L par heure
- ( ) $-2$ mg/L
- ( ) $20$ mg/L par heure
- ( ) $-0{,}1$ par heure

**Justification (à dire à voix haute après le vote) :** $C'(t) = 20 \cdot (-0{,}1) \cdot e^{-0{,}1 t}$, donc $C'(0) = -2$ : juste après la prise, la concentration diminue de $2$ mg/L par heure. Distracteurs — « $-2$ mg/L » : La valeur est correcte, mais l'unité d'une dérivée par rapport au temps est l'unité de $C$ divisée par celle de $t$. « $20$ mg/L par heure » : $20$ mg/L est la valeur $C(0)$, une concentration, pas une vitesse de variation. « $-0{,}1$ par heure » : $-0{,}1$ est le taux relatif $\dfrac{C'(t)}{C(t)}$, pas la dérivée.

**Exercices associés :** S.7, R.8, R.9.

---

## Q9 — Chain rule à partir de valeurs (O3)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> On sait que $g(2) = 5$, $g'(2) = 3$, $f'(2) = 4$ et $f'(5) = -1$. On pose $h(x) = f\big(g(x)\big)$. Que vaut $h'(2)$ ?

**Choix :**
- (X) $-3$
- ( ) $12$
- ( ) $-1$
- ( ) $3$

**Justification (à dire à voix haute après le vote) :** $h'(2) = f'\big(g(2)\big) \cdot g'(2) = f'(5) \cdot 3 = -3$. Distracteurs — « $12$ » : On a évalué $f'$ en $2$ au lieu de $g(2) = 5$ : $f'(2) \cdot g'(2) = 12$. « $-1$ » : $f'(5)$ est la bonne pente de la fonction extérieure, mais il manque le facteur $g'(2) = 3$. « $3$ » : $g'(2)$ seul ne tient pas compte de la fonction extérieure.

**Exercices associés :** S.5, R.5.

---

# Questions de réserve

À poser si le temps le permet ou en séance ; corrigées dans le deck « Annexe ».

---

## Réserve 1 — Chain rule et cosinus (O3)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut la dérivée de $f(x) = \cos(2x)$ ?

**Choix :**
- (X) $-2\sin(2x)$
- ( ) $-\sin(2x)$
- ( ) $2\sin(2x)$
- ( ) $-\sin(2)$

**Justification (à dire à voix haute après le vote) :** $\big(\cos(y)\big)' = -\sin(y)$, multiplié par la dérivée de $2x$, qui vaut $2$. Distracteurs — « $-\sin(2x)$ » : Il manque la dérivée de la fonction intérieure. « $2\sin(2x)$ » : Le signe est faux : la dérivée du cosinus est $-\sin$. « $-\sin(2)$ » : On a dérivé la fonction intérieure à la place de la variable : le sinus reçoit $2x$.

**Exercices associés :** S.3, R.4(e).

---

## Réserve 2 — Exponentielle en base quelconque (O1)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut la dérivée de $f(x) = 3^{x}$ ?

**Choix :**
- (X) $\ln(3) \cdot 3^{x}$
- ( ) $x \cdot 3^{x - 1}$
- ( ) $3^{x}$
- ( ) $\dfrac{3^{x}}{\ln(3)}$

**Justification (à dire à voix haute après le vote) :** Pour $a > 0$, $(a^{x})' = \ln(a) \cdot a^{x}$. Distracteurs — « $x \cdot 3^{x - 1}$ » : La règle des puissances ne s'applique pas : la variable est dans l'exposant. « $3^{x}$ » : Seule l'exponentielle de base $e$ est égale à sa dérivée, car $\ln(e) = 1$. « $\dfrac{3^{x}}{\ln(3)}$ » : Le facteur $\ln(3)$ multiplie, il ne divise pas.

**Exercices associés :** S.3 (f₄), R.1.

---

## Réserve 3 — Valeur et pente lues sur un graphe (O5)

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Le graphe de $f$ passe par $(1\,;\,4)$, et la tangente en ce point passe aussi par $(3\,;\,0)$. Que vaut $f'(1)$ ?

**Choix :**
- (X) $-2$
- ( ) $4$
- ( ) $2$
- ( ) $-\dfrac{1}{2}$

**Justification (à dire à voix haute après le vote) :** La pente de la tangente vaut $\dfrac{0 - 4}{3 - 1} = -2$. Distracteurs — « $4$ » : $4$ est la valeur $f(1)$, pas la pente. « $2$ » : Le signe est faux : la tangente descend de $(1\,;\,4)$ à $(3\,;\,0)$. « $-\dfrac{1}{2}$ » : Le quotient est inversé : la pente est la variation de $y$ divisée par la variation de $x$.

**Exercices associés :** S.4, S.5.

---

## Réglages Wooclap suggérés

- Version en autonomie : afficher la bonne réponse et la justification après chaque question.
- Pas de chronomètre : les étudiants avancent à leur rythme.
