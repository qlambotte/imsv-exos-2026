# Wooclap — Correction de T.1 (QCM)

Un événement Wooclap, quatre questions **QCM à réponse unique**, une par sous-question de T.1
(charge virale du VIH), posées juste après le temps consacré au transfert. Les résultats disent par
où commencer la correction : on corrige d'abord la sous-question où les votes sont les plus
partagés. Les distracteurs correspondent aux erreurs classiques. On donne $\log_{10}(2) \approx 0{,}30$.
Résultats vérifiés par script.

---

## Q1 — (a) Logarithme d'une charge de 20 copies/mL

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Combien vaut $L = \log_{10}(C)$ pour une charge virale de $20$ copies/mL ?

**Choix :**
- (X) $L \approx 1{,}3$
- ( ) $L = 2$
- ( ) $L \approx 0{,}3$
- ( ) $L \approx 0{,}6$

**Justification :** $20 = 2 \cdot 10$, donc $L = \log_{10}(2) + \log_{10}(10) \approx 0{,}30 + 1 = 1{,}3$.
Le distracteur $2$ compte les chiffres de $20$ ; $0{,}3$ oublie $\log_{10}(10) = 1$ ; $0{,}6$ remplace
le produit $2 \cdot 10$ par $2 \cdot 2$, ce qui donne $\log_{10}(4)$.

---

## Q2 — (b) Baisse nécessaire pour devenir indétectable

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une charge virale de départ vaut $100\,000$ copies/mL. De combien de log doit-elle baisser pour devenir indétectable (moins de $20$ copies/mL) ?

**Choix :**
- (X) environ $3{,}7$ log
- ( ) $3$ log
- ( ) environ $4{,}7$ log
- ( ) $5000$ log

**Justification :** $L$ passe de $5$ à environ $1{,}3$, donc la baisse vaut $5 - 1{,}3 = 3{,}7$ log. Le distracteur
$3$ vient de $\log_{10}(20) = 2$ ; $4{,}7$ vient de $\log_{10}(20) \approx 0{,}3$ ; $5000$ est le facteur
$\frac{100\,000}{20}$ par lequel la charge est divisée, et non la baisse en log.

---

## Q3 — (c) Baisse de 2 log

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une charge virale de $100\,000$ copies/mL baisse de $2$ log. Par quel nombre est-elle divisée, et combien vaut-elle ensuite ?

**Choix :**
- (X) Elle est divisée par $100$ : elle vaut $1000$ copies/mL.
- ( ) Elle est divisée par $2$ : elle vaut $50\,000$ copies/mL.
- ( ) Elle est divisée par $20$ : elle vaut $5000$ copies/mL.
- ( ) Elle est divisée par $1000$ : elle vaut $100$ copies/mL.

**Justification :** $L$ passe de $5$ à $3$, donc $C = 10^{3} = 1000$ copies/mL : la charge est divisée par
$10^{2} = 100$. Le distracteur « par $2$ » lit l'écart de log comme un facteur ; « par $20$ » confond $10^{2}$
avec $2 \cdot 10$ ; « par $1000$ » prend la nouvelle valeur de $L$, $3$, pour l'écart.

---

## Q4 — (d) Patients A et B

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Patient A : la charge passe de $40\,000$ à $10\,000$ copies/mL. Patient B : de $20\,000$ à $10\,000$ copies/mL. Une baisse est significative si elle atteint au moins $0{,}5$ log. Que conclus-tu ?

**Choix :**
- (X) A : environ $0{,}6$ log, significative ; B : environ $0{,}3$ log, non significative.
- ( ) A : environ $4{,}5$ log ; B : $4$ log ; les deux baisses sont significatives.
- ( ) A : $4$ log ; B : $2$ log ; les deux baisses sont significatives.
- ( ) A : $0{,}75$ log ; B : $0{,}5$ log ; les deux baisses sont significatives.

**Justification :** la baisse en log est la différence des logarithmes, c'est-à-dire le logarithme du quotient :
pour A, $\log_{10}(4) = 2\log_{10}(2) \approx 0{,}6 \geq 0{,}5$ ; pour B, $\log_{10}(2) \approx 0{,}3 < 0{,}5$. Le
deuxième choix prend le logarithme de la différence ($\log_{10}(30\,000) \approx 4{,}5$ et
$\log_{10}(10\,000) = 4$) ; le troisième prend le quotient des charges ($4$ et $2$) pour la baisse en log ; le
quatrième prend la diminution relative ($\frac{30\,000}{40\,000} = 0{,}75$ et $\frac{10\,000}{20\,000} = 0{,}5$)
pour la baisse en log.

---

## Réglages Wooclap suggérés

- Affichage des résultats : après clôture du vote, pas en direct.
- Chronomètre : 30 à 45 secondes par question.
