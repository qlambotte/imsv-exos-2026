# Wooclap — Correction de S.4 (QCM)

Un événement Wooclap, quatre questions **QCM à réponse unique**, une par équation, posées juste
après le temps consacré au socle. Les résultats disent par où commencer la correction : on corrige
d'abord l'équation où les votes sont les plus partagés. Les distracteurs correspondent aux erreurs
classiques ; en (b), (c) et (d), une **valeur approchée** de la bonne solution figure parmi les
choix : elle est juste, mais l'énoncé demande la forme exacte. Résultats vérifiés par script.

---

## Q1 — (a) $3 \cdot 2^{x} = 48$

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Quelle est la solution de $3 \cdot 2^{x} = 48$ ?

**Choix :**
- (X) $x = 4$
- ( ) $x = 8$
- ( ) $x = \dfrac{\ln(48)}{\ln(6)}$
- ( ) $x = 16$

**Justification :** on divise par $3$ : $2^{x} = 16 = 2^{4}$, donc $x = 4$. Le distracteur $8$ confond $2^{x}$
avec $2x$ ($2x = 16$) ; $\frac{\ln(48)}{\ln(6)}$ colle le facteur à la base ($3 \cdot 2^{x} = 6^{x}$) ;
$16$ s'arrête à la valeur de la puissance $2^{x}$.

---

## Q2 — (b) $5 \cdot 2^{x} = 35$

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Quelle est la solution exacte de $5 \cdot 2^{x} = 35$ ?

**Choix :**
- (X) $x = \dfrac{\ln(7)}{\ln(2)}$
- ( ) $x \approx 2{,}81$
- ( ) $x = \dfrac{7}{2}$
- ( ) $x = \ln(7)$

**Justification :** on divise par $5$ : $2^{x} = 7$. Les deux membres sont strictement positifs, donc on applique
le logarithme népérien : $x\ln(2) = \ln(7)$, puis $x = \frac{\ln(7)}{\ln(2)}$. La valeur $2{,}81$ est une valeur
approchée de cette solution, et non sa forme exacte ; $\frac72$ « divise par la base », alors que la base n'est pas
un facteur ; $\ln(7)$ oublie de diviser par $\ln(2)$. L'encadrement $2 < x < 3$ est facultatif : il donne une
idée de la valeur de $x$.

---

## Q3 — (c) $100 \cdot \left(\tfrac12\right)^{t} = 20$

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Quelle est la solution exacte de $100 \cdot \left(\tfrac{1}{2}\right)^{t} = 20$ ?

**Choix :**
- (X) $t = \dfrac{\ln(5)}{\ln(2)}$
- ( ) $t \approx 2{,}32$
- ( ) $t = -\dfrac{\ln(5)}{\ln(2)}$
- ( ) $t = \ln(5)$

**Justification :** on divise par $100$ : $\left(\frac12\right)^{t} = \frac15$, donc $2^{t} = 5$, puis
$t\ln(2) = \ln(5)$ et $t = \frac{\ln(5)}{\ln(2)}$. La valeur $2{,}32$ est une valeur approchée, et non la forme
exacte ; $-\frac{\ln(5)}{\ln(2)}$ vient d'une erreur de signe en passant de $\left(\frac12\right)^{t}$ à $2^{t}$ ;
$\ln(5)$ oublie de diviser par $\ln(2)$.

---

## Q4 — (d) $4\,e^{0{,}5\,x} = 12$

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Quelle est la solution exacte de $4\,e^{0{,}5\,x} = 12$ ?

**Choix :**
- (X) $x = 2\ln(3)$
- ( ) $x \approx 2{,}20$
- ( ) $x = \dfrac{\ln(3)}{2}$
- ( ) $x = 2\ln(12)$

**Justification :** on divise par $4$ : $e^{0{,}5\,x} = 3$, puis on applique le logarithme népérien :
$0{,}5\,x = \ln(3)$, donc $x = 2\ln(3)$. La valeur $2{,}20$ est une valeur approchée, et non la forme exacte ;
$\frac{\ln(3)}{2}$ multiplie par $0{,}5$ au lieu de diviser ; $2\ln(12)$ oublie de diviser par $4$.

---

## Réglages Wooclap suggérés

- Affichage des résultats : après clôture du vote, pas en direct.
- Chronomètre : 30 secondes par question.
