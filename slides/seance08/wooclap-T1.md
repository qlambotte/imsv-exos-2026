# Wooclap — Correction de T.1 (QCM)

Un événement Wooclap, quatre questions **QCM à réponse unique**, une par sous-question, posées juste
après le temps consacré au transfert. L'énoncé de T.1 est projeté pendant le vote (slide « Quelles réponses
as-tu trouvées ? »). On corrige d'abord la sous-question où les votes sont les plus partagés.

---

## Q1 — (a) Le modèle

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Une culture de $1000$ bactéries double toutes les $20$ minutes. Quelle expression donne le nombre de bactéries $N(t)$ après $t$ minutes ?

**Choix :**
- (X) $N(t) = 1000 \cdot 2^{t/20}$
- ( ) $N(t) = 1000 \cdot 2^{20t}$
- ( ) $N(t) = 1000 \cdot 2^{t}$
- ( ) $N(t) = 1000 + 50t$

**Justification :** après $t$ minutes, l'effectif a doublé $\tfrac{t}{20}$ fois. Le distracteur $2^{20t}$ doublerait $20$ fois par
minute ; $2^{t}$ doublerait chaque minute ; $1000 + 50t$ est une croissance linéaire, de $1000$ bactéries en $20$ minutes.

---

## Q2 — (b) La dérivée

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut $N'(t)$, pour $N(t) = 1000 \cdot 2^{t/20}$ ?

**Choix :**
- (X) $50\ln(2) \cdot 2^{t/20}$
- ( ) $\dfrac{t}{20} \cdot 1000 \cdot 2^{t/20 - 1}$
- ( ) $1000\ln(2) \cdot 2^{t/20}$
- ( ) $50 \cdot 2^{t/20}$

**Justification :** exponentielle en base $2$ et chain rule : $1000 \cdot \ln(2) \cdot 2^{t/20} \cdot \tfrac{1}{20} = 50\ln(2) \cdot 2^{t/20} \approx 34{,}5 \cdot 2^{t/20}$. Le deuxième choix applique la
règle des puissances à une exponentielle ; le troisième oublie le facteur $\tfrac{1}{20}$ de la fonction intérieure ; le dernier
oublie $\ln(2)$.

---

## Q3 — (c) La valeur en $t = 60$

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut la valeur exacte de $N'(60)$ ?

**Choix :**
- (X) $400\ln(2)$ bactéries par minute
- ( ) $8000$ bactéries
- ( ) $400\ln(2)$ bactéries
- ( ) $400$ bactéries par minute

**Justification :** $N'(60) = 50\ln(2) \cdot 2^{3} = 400\ln(2) \approx 276$, en bactéries par minute. Le distracteur $8000$ est $N(60)$, une valeur ;
le troisième oublie l'unité d'une vitesse ; $400$ oublie le facteur $\ln(2)$, et c'est aussi le taux moyen entre $60$ et $80$ minutes, $\tfrac{16\,000 - 8000}{20}$.

---

## Q4 — (d) Le taux relatif

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Que vaut le quotient $\dfrac{N'(t)}{N(t)}$ ?

**Choix :**
- (X) $\dfrac{\ln(2)}{20}$ par minute, quel que soit $t$
- ( ) $\dfrac{1}{20} = 0{,}05$ par minute
- ( ) $2$
- ( ) Il augmente avec $t$, car $N$ augmente.

**Justification :** $\dfrac{N'(t)}{N(t)} = \dfrac{\ln(2)}{20} \approx 0{,}0345$ : la culture augmente de $\dfrac{\ln(2)}{20} \approx 3{,}45\,\%$ de son effectif par minute,
à chaque instant. Le distracteur $\tfrac{1}{20}$ oublie $\ln(2)$ ; $2$ est le facteur de doublement ; le dernier confond la vitesse
$N'(t)$, qui augmente, et le taux relatif, qui est constant.

---

## Réglages Wooclap suggérés

- Affichage des résultats : après clôture du vote, pas en direct.
- Chronomètre : 45 secondes par question.
