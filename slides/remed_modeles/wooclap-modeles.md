# Wooclap — QCM de remédiation : modèles (séance 6)

Un événement Wooclap, 7 questions **QCM à réponse unique**, dans l'ordre ci-dessous (noyau), une par objectif de la séance 6 (O1 à O7). Questions nouvelles, rédigées pour cette remédiation. Les distracteurs correspondent aux erreurs classiques ; tous les résultats ont été vérifiés par script. En fin de fichier : 4 questions de réserve, corrigées dans le deck « Annexe ».

Code Wooclap : **OBMKFUU** (version en autonomie : un seul événement pour tous les thèmes ; ajouter ce thème à l'événement).

---

## Q1 — Reconnaître le type de croissance

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une grandeur prend les valeurs $3$, $6$, $12$ et $24$ aux instants $t = 0$, $1$, $2$ et $3$. Quel modèle convient ?

**Choix :**
- ( ) Polynomial : $N(t) = 3 + 3t^{2}$
- (X) Exponentiel : $N(t) = 3 \cdot 2^{t}$
- ( ) Logarithmique
- ( ) Affine : $N(t) = 3 + 3t$

**Justification (à dire à voix haute après le vote) :** les quotients successifs $\frac{6}{3}$, $\frac{12}{6}$, $\frac{24}{12}$ valent tous $2$ : la grandeur est multipliée par $2$ à chaque unité de temps, donc $N(t) = 3 \cdot 2^{t}$.

---

## Q2 — Lire les paramètres d'un modèle exponentiel

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une grandeur vaut $N(t) = 200 \cdot 0{,}8^{t}$, où $t$ est le temps en heures. Que signifient les nombres $200$ et $0{,}8$ ?

**Choix :**
- ( ) La grandeur vaut $200$ en $t = 0$ et perd $80\,\%$ de sa valeur chaque heure.
- ( ) La grandeur vaut $200$ en $t = 0$ et augmente de $80\,\%$ chaque heure.
- (X) La grandeur vaut $200$ en $t = 0$ et perd $20\,\%$ de sa valeur chaque heure.
- ( ) La grandeur vaut $0{,}8$ en $t = 0$ et est multipliée par $200$ chaque heure.

**Justification (à dire à voix haute après le vote) :** $N(0) = 200$ ; multiplier par $0{,}8$ chaque heure, c'est garder $80\,\%$ de la valeur, donc en perdre $20\,\%$.

---

## Q3 — Changer de base

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> On écrit $2^{t} = e^{kt}$ pour tout réel $t$. Que vaut $k$ ?

**Choix :**
- ( ) $k = \log_{10}(2)$
- (X) $k = \ln(2)$
- ( ) $k = 2$
- ( ) $k = \dfrac{1}{\ln(2)}$

**Justification (à dire à voix haute après le vote) :** $2 = e^{\ln(2)}$, donc $2^{t} = e^{\ln(2)\,t}$ et $k = \ln(2)$.

---

## Q4 — Résoudre une équation exponentielle

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Quelle est la solution exacte de l'équation $3 \cdot 5^{x} = 12$ ?

**Choix :**
- ( ) $x \approx 0{,}86$
- ( ) $x = \dfrac{4}{5}$
- (X) $x = \dfrac{\ln(4)}{\ln(5)}$
- ( ) $x = \dfrac{\ln(12)}{\ln(15)}$

**Justification (à dire à voix haute après le vote) :** on divise par $3$ : $5^{x} = 4$ ; on applique $\ln$ : $x\ln(5) = \ln(4)$, donc $x = \frac{\ln(4)}{\ln(5)}$.

---

## Q5 — Demi-vie

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Le technétium-99m, utilisé en imagerie médicale, a une demi-vie de $6$ heures. Un échantillon a une activité de $800$ MBq. Quelle est son activité $18$ heures plus tard ?

**Choix :**
- ( ) Environ $267$ MBq
- (X) $100$ MBq
- ( ) $50$ MBq
- ( ) $200$ MBq

**Justification (à dire à voix haute après le vote) :** $18$ h, c'est $3$ demi-vies ; chacune divise l'activité par $2$ : $\frac{800}{2^{3}} = 100$ MBq.

Source : Washington State Department of Health, Office of Radiation Protection, « Technetium-99m (99mTc) », Fact Sheet 320-083, juillet 2002 : « It has a half-life of six hours ».

---

## Q6 — Croissances comparées

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Quand $x$ devient très grand, laquelle de ces fonctions finit par dépasser toutes les autres ?

**Choix :**
- ( ) $x^{5}$
- ( ) $1000\ln(x)$
- ( ) $100\sqrt{x}$
- (X) $1{,}1^{x}$

**Justification (à dire à voix haute après le vote) :** de la plus lente à la plus rapide : $\ln(x)$, $\sqrt{x}$, $x^{5}$, puis $1{,}1^{x}$ ; les facteurs $100$ et $1000$ ne changent pas l'ordre quand $x$ devient très grand.

---

## Q7 — Modèle périodique

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une grandeur oscille entre $2$ et $8$, avec une période de $12$, et atteint son maximum en $t = 3$. Quel modèle convient ?

**Choix :**
- ( ) $5 + 3\cos\left(\dfrac{\pi}{12}(t - 3)\right)$
- ( ) $5 + 6\cos\left(\dfrac{\pi}{6}(t - 3)\right)$
- (X) $5 + 3\cos\left(\dfrac{\pi}{6}(t - 3)\right)$
- ( ) $5 + 3\cos\left(\dfrac{\pi}{6}(t + 3)\right)$

**Justification (à dire à voix haute après le vote) :** $M = 5$, $A = 3$, $\frac{2\pi}{T} = \frac{\pi}{6}$ et $h = 3$, donc $5 + 3\cos\left(\frac{\pi}{6}(t - 3)\right)$.

---

# Questions de réserve

## Réserve 1 — Comparer deux pH

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une solution a un pH de $3$, une autre un pH de $5$. On rappelle que $\mathrm{pH} = -\log_{10}\left([\mathrm{H}^+]\right)$. Que peut-on dire de leurs concentrations en ions hydrogène ?

**Choix :**
- ( ) La première contient $2$ fois plus d'ions hydrogène par litre.
- (X) La première contient $100$ fois plus d'ions hydrogène par litre.
- ( ) La première contient $100$ fois moins d'ions hydrogène par litre.
- ( ) La première contient $\frac{5}{3}$ fois plus d'ions hydrogène par litre.

**Justification (à dire à voix haute après le vote) :** $[\mathrm{H}^+] = 10^{-3}$ et $10^{-5}$ mol/L : le quotient vaut $10^{2} = 100$.

---

## Réserve 2 — Un logarithme en base 2

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut $\log_{2}(32)$ ?

**Choix :**
- ( ) $64$
- (X) $5$
- ( ) $\frac{1}{5}$
- ( ) $16$

**Justification (à dire à voix haute après le vote) :** $32 = 2^{5}$, donc $\log_{2}(32) = 5$.

---

## Réserve 3 — Temps de doublement

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Dans un bouillon de culture riche, la bactérie *Escherichia coli* a un temps de doublement de $20$ minutes. Combien de temps faut-il pour que le nombre de bactéries soit multiplié par $8$ ?

**Choix :**
- ( ) $160$ minutes
- ( ) $80$ minutes
- (X) $60$ minutes
- ( ) $40$ minutes

**Justification (à dire à voix haute après le vote) :** $8 = 2^{3}$ : il faut $3$ doublements, soit $3 \cdot 20 = 60$ minutes.

Source : G. Sezonov, D. Joseleau-Petit et R. D'Ari, « Escherichia coli Physiology in Luria-Bertani Broth », Journal of Bacteriology, 189(23), 2007, p. 8746-8749 : « The doubling time during steady-state growth in Luria-Bertani broth was 20 min. »

---

## Réserve 4 — Lire une période

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Quelle est la période de la fonction $f(t) = 4 + 2\cos(3t)$ ?

**Choix :**
- ( ) $2$
- ( ) $6\pi$
- (X) $\dfrac{2\pi}{3}$
- ( ) $3$

**Justification (à dire à voix haute après le vote) :** Dans $\cos\left(\frac{2\pi}{T}\,t\right)$, on a $\frac{2\pi}{T} = 3$, donc $T = \frac{2\pi}{3}$.

---
