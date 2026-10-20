# Wooclap — QCM de remédiation : la logique, l'implication comme contrat

Un événement Wooclap, 7 questions **QCM à réponse unique**, dans l'ordre ci-dessous (noyau). Questions nouvelles, rédigées pour cette remédiation (elles ne viennent pas des quiz Moodle). Exemples sourcés : SNCB (Q1, Q5, Q6, Q7) et Manuel MSD (Q3, Q4). En fin de fichier : 5 questions de réserve, corrigées dans le deck « Annexe ».

Code Wooclap : **OBMKFUU** (version en autonomie : un seul événement pour les quatre thèmes).

---

## Q1 — Rupture d'un engagement

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Engagement de la SNCB : « Si un train arrive avec 60 minutes de retard ou plus, alors le voyageur reçoit 100 % du prix de son trajet. » Dans quelle situation la SNCB ne tient-elle pas son engagement ?

**Choix :**
- ( ) Retard de 45 minutes et aucune compensation.
- (X) Retard de 75 minutes et aucune compensation.
- ( ) Retard de 90 minutes et 100 % du prix du trajet reçu.
- ( ) Retard de 45 minutes et 100 % du prix du trajet reçu.

**Justification (à dire à voix haute après le vote) :** la condition est remplie ($\alpha$ vrai) et la promesse n'est pas exécutée ($\beta$ faux) : c'est la seule rupture possible. Avec 45 minutes de retard, la condition n'est pas remplie : l'engagement ne s'applique pas.

---

## Q2 — Colonne de l'implication

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Les colonnes de $\alpha$ et de $\beta$, de haut en bas, sont : $\alpha$ : V, V, F, F et $\beta$ : V, F, V, F. Quelle est la colonne de $\alpha \Rightarrow \beta$ ?

**Choix :**
- ( ) V, V, F, V
- ( ) V, F, F, F
- (X) V, F, V, V
- ( ) V, F, F, V

**Justification (à dire à voix haute après le vote) :** F uniquement sur la ligne $\alpha$ vrai, $\beta$ faux (2<sup>e</sup> ligne), V partout ailleurs.

---

## Q3 — Condition non remplie

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Critère diagnostique : « Si la glycémie à jeun d'une personne est d'au moins 7,0 mmol/L, alors cette personne a un diabète. » Une personne a une glycémie à jeun de 5,0 mmol/L. Que peut-on dire de l'implication pour cette personne ?

**Choix :**
- ( ) Elle est fausse, car le diabète n'est pas établi.
- (X) Elle est vraie, mais elle ne permet pas de conclure sur le diabète.
- ( ) Cette personne n'a pas de diabète.
- ( ) On ne peut pas savoir sans connaître le diagnostic.

**Justification (à dire à voix haute après le vote) :** la condition n'est pas remplie ($\alpha$ faux) : l'implication est automatiquement vérifiée, et elle ne dit rien de $\beta$.

---

## Q4 — Réciproque

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Critère diagnostique : « Si la glycémie à jeun d'une personne est d'au moins 7,0 mmol/L, alors cette personne a un diabète. » Quelle est la réciproque de cette implication ?

**Choix :**
- ( ) Si une personne n'a pas de diabète, alors sa glycémie à jeun est inférieure à 7,0 mmol/L.
- ( ) Si la glycémie à jeun est inférieure à 7,0 mmol/L, alors la personne n'a pas de diabète.
- (X) Si une personne a un diabète, alors sa glycémie à jeun est d'au moins 7,0 mmol/L.
- ( ) Si une personne a un diabète, alors sa glycémie à jeun est inférieure à 7,0 mmol/L.

**Justification (à dire à voix haute après le vote) :** on échange $\alpha$ et $\beta$ sans les nier : $\beta \Rightarrow \alpha$. Ce contrat n'est pas promis : une HbA1c d'au moins 6,5 % suffit aussi à retenir un diabète.

---

## Q5 — Contraposée

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Engagement de la SNCB : « Si un train arrive avec 60 minutes de retard ou plus, alors le voyageur reçoit 100 % du prix de son trajet. » Un voyageur ne reçoit aucune compensation, et la SNCB a tenu son engagement. Que peut-on en déduire ?

**Choix :**
- ( ) Le train a eu 60 minutes de retard ou plus.
- (X) Le train a eu moins de 60 minutes de retard.
- ( ) Le train n'a eu aucun retard.
- ( ) On ne peut rien en déduire sur le retard.

**Justification (à dire à voix haute après le vote) :** c'est la contraposée $\lnot\beta \Rightarrow \lnot\alpha$ : pas de compensation et engagement tenu imposent que la condition ne soit pas remplie. La négation de $\alpha$ est « moins de 60 minutes de retard », pas « aucun retard ».

---

## Q6 — Négation d'une implication

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Engagement de la SNCB : « Si un train arrive avec 60 minutes de retard ou plus, alors le voyageur reçoit 100 % du prix de son trajet. » Quelle est la négation de cet engagement ?

**Choix :**
- ( ) Si le train a 60 minutes de retard ou plus, alors le voyageur ne reçoit pas 100 % du prix de son trajet.
- ( ) Le train a moins de 60 minutes de retard et le voyageur reçoit 100 % du prix de son trajet.
- ( ) Le train a moins de 60 minutes de retard ou le voyageur ne reçoit pas 100 % du prix de son trajet.
- (X) Le train a 60 minutes de retard ou plus et le voyageur ne reçoit pas 100 % du prix de son trajet.

**Justification (à dire à voix haute après le vote) :** $\lnot(\alpha \Rightarrow \beta) \iff \alpha \land \lnot\beta$ : la négation décrit la rupture.

---

## Q7 — Suffisant, nécessaire

**Type Wooclap :** QCM · réponse unique

**Énoncé à coller :**
> Engagement de la SNCB : « Si un train arrive avec 60 minutes de retard ou plus, alors le voyageur reçoit 100 % du prix de son trajet. » Quelle affirmation est correcte ?

**Choix :**
- ( ) Un retard d'au moins 60 minutes est une condition nécessaire pour recevoir 100 % du prix du trajet.
- ( ) Recevoir 100 % du prix du trajet est une condition suffisante pour avoir eu un retard d'au moins 60 minutes.
- (X) Un retard d'au moins 60 minutes est une condition suffisante pour recevoir 100 % du prix du trajet.
- ( ) Ne pas recevoir 100 % du prix du trajet est une condition nécessaire pour avoir un retard d'au moins 60 minutes.

**Justification (à dire à voix haute après le vote) :** « $\alpha$ suffisante pour $\beta$ » et « $\beta$ nécessaire pour $\alpha$ » traduisent la même implication $\alpha \Rightarrow \beta$ ; les deux autres sens donnent la réciproque, et la dernière phrase décrit la rupture.

---

# Réserve (non projetée ; corrections dans le deck « Annexe »)

## Réserve 1 — Condition non remplie, conclusion vraie

**Énoncé à coller :**
> Engagement de la SNCB : « Si un train arrive avec 60 minutes de retard ou plus, alors le voyageur reçoit 100 % du prix de son trajet. » Un train arrive avec 20 minutes de retard et, par geste commercial, la SNCB rembourse 100 % du trajet. L'engagement est-il rompu ?

**Choix :**
- ( ) Oui : la SNCB verse une compensation alors que la condition n'est pas remplie.
- ( ) On ne peut pas le savoir sans connaître la cause du retard.
- (X) Non : la condition n'est pas remplie, l'engagement ne s'applique pas.
- ( ) Non, mais seulement parce que la compensation a été versée.

**Justification :** $\alpha$ est faux et $\beta$ est vrai : ligne 3 de la table, où l'implication est vraie.

---

## Réserve 2 — Écriture équivalente

**Énoncé à coller :**
> Laquelle de ces propositions est équivalente à $\alpha \Rightarrow \beta$ ?

**Choix :**
- ( ) $\alpha \lor \lnot\beta$
- ( ) $\alpha \land \lnot\beta$
- ( ) $\lnot\alpha \land \beta$
- (X) $\lnot\alpha \lor \beta$

**Justification :** colonne V, F, V, V : vraie si la condition n'est pas remplie ou si la promesse est exécutée.

---

## Réserve 3 — Contraposée

**Énoncé à coller :**
> Critère diagnostique : « Si l'HbA1c d'une personne est d'au moins 6,5 %, alors cette personne a un diabète. » Quelle est la contraposée de cette implication ?

**Choix :**
- ( ) Si l'HbA1c est inférieure à 6,5 %, alors la personne n'a pas de diabète.
- ( ) Si une personne a un diabète, alors son HbA1c est d'au moins 6,5 %.
- (X) Si une personne n'a pas de diabète, alors son HbA1c est inférieure à 6,5 %.
- ( ) Si une personne n'a pas de diabète, alors son HbA1c est d'au moins 6,5 %.

**Justification :** on nie les deux propositions et on les échange : $\lnot\beta \Rightarrow \lnot\alpha$.

---

## Réserve 4 — Négation

**Énoncé à coller :**
> Critère diagnostique : « Si la glycémie à jeun d'une personne est d'au moins 7,0 mmol/L, alors cette personne a un diabète. » Quelle est la négation de cette implication ?

**Choix :**
- ( ) La glycémie à jeun est inférieure à 7,0 mmol/L et la personne a un diabète.
- (X) La glycémie à jeun est d'au moins 7,0 mmol/L et la personne n'a pas de diabète.
- ( ) Si la glycémie à jeun est d'au moins 7,0 mmol/L, alors la personne n'a pas de diabète.
- ( ) Si la glycémie à jeun est inférieure à 7,0 mmol/L, alors la personne n'a pas de diabète.

**Justification :** $\lnot(\alpha \Rightarrow \beta) \iff \alpha \land \lnot\beta$ : la négation décrit la rupture du critère.

---

## Réserve 5 — Suffisant ou nécessaire

**Énoncé à coller :**
> Critère diagnostique : « Si la glycémie à jeun d'une personne est d'au moins 7,0 mmol/L, alors cette personne a un diabète. » Une glycémie à jeun d'au moins 7,0 mmol/L est…

**Choix :**
- ( ) une condition suffisante et nécessaire pour retenir un diabète.
- (X) une condition suffisante, mais pas nécessaire, pour retenir un diabète.
- ( ) une condition nécessaire, mais pas suffisante, pour retenir un diabète.
- ( ) ni suffisante ni nécessaire pour retenir un diabète.

**Justification :** elle suffit ($\alpha \Rightarrow \beta$) ; elle n'est pas nécessaire, car une HbA1c d'au moins 6,5 % suffit aussi.
