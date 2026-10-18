#!/usr/bin/env python3
"""Vérification de tous les résultats numériques et algébriques de la séance 5.
À lancer depuis n'importe quel répertoire temporaire :  python3 verif_seance05.py
Arithmétique exacte (fractions) quand c'est possible, balayage numérique sinon."""
from fractions import Fraction as F
import math
import numpy as np

n_ok = 0
def ok(cond, msg):
    global n_ok
    assert cond, "ÉCHEC : " + msg
    n_ok += 1

def close(a, b, tol=1e-9):
    return abs(a - b) <= tol

def count_solutions(f, a, lo, hi, N=400001):
    """Nombre de solutions de f(x)=a sur [lo,hi] : changements de signe de f-a,
    plus les tangences (minimum local de |f-a| quasi nul sans changement de signe)."""
    xs = np.linspace(lo, hi, N)
    v = f(xs) - a
    s = np.sign(v)
    sign_changes = np.where(s[:-1] * s[1:] < 0)[0]
    n = len(sign_changes) + int(abs(v[0]) < 1e-9) + int(abs(v[-1]) < 1e-9)
    av = np.abs(v)
    loc = np.where((av[1:-1] <= av[:-2]) & (av[1:-1] <= av[2:]) & (av[1:-1] < 1e-7))[0] + 1
    # regrouper les indices voisins, ignorer ceux proches d'un changement de signe
    groups = []
    for i in loc:
        if groups and i - groups[-1][-1] <= 2:
            groups[-1].append(i)
        else:
            groups.append([i])
    for gp in groups:
        i = gp[0]
        if len(sign_changes) and np.min(np.abs(sign_changes - i)) <= 3:
            continue
        n += 1
    return n

# ---------- Échauffement (slides) ----------
u, v = (3, 1), (-1, 2)
ok(u[0]*v[0] + u[1]*v[1] == -1, "Échauffement Q1 produit scalaire (3,1).(-1,2) = -1 < 0 : angle obtus")
ok(2*3 + 1 == 7, "Échauffement Q3 A = 2C + 1 : C = 3 donne A = 7")
ok(4**2 - 5 == 11 and (-4)**2 - 5 == 11, "Échauffement Q4 x^2 - 5 = 11 : x = +-4")

# ---------- R.1 : quatre courbes ----------
ok(1 == (-1)**2 and 1 == 1**2, "R.1 x = y^2 : deux ordonnées pour x = 1")
ok(0**2 + 2**2 == 4 and 0**2 + (-2)**2 == 4, "R.1 cercle x^2+y^2=4 : deux ordonnées pour x = 0")

# ---------- R.2 : parabole x^2 - 2x - 3 ----------
f2 = lambda x: x*x - 2*x - 3
ok(f2(4) == 5 and f2(-1) == 0, "R.2 f(4)=5, f(-1)=0")
ok(f2(4) == 5 and f2(-2) == 5, "R.2 antécédents de 5 : -2 et 4")
ok(sorted(r for r in range(-10, 11) if f2(r) == 5) == [-2, 4], "R.2 uniques entiers antécédents de 5")
ok(f2(1) == -4 and all(f2(x) >= -4 for x in np.linspace(-20, 20, 4001)), "R.2 minimum -4 en 1")
# f(x) = -5 : x^2-2x+2 = 0, discriminant
ok(4 - 4*1*2 < 0, "R.2 f(x)=-5 sans solution (disc. < 0)")
ok(2*2 - 4*1*(-3 + 4) == 0, "R.2 f(x)=-4 : discriminant nul, x=1 unique")

# ---------- R.3 : Tanaka 208 - 0.7 a ----------
tan = lambda a: F(208) - F(7, 10)*a
ok([tan(a) for a in (20, 30, 40, 50, 60)] == [194, 187, 180, 173, 166], "R.3 tableau Tanaka")
ok((tan(60) - tan(20)) / (60 - 20) == F(-7, 10), "R.3 pente -0,7")
ok(tan(0) == 208, "R.3 ordonnée à l'origine 208")

# ---------- R.5 : domaines et IMC ----------
def sample_dom(fn, lo=-15, hi=15, N=300001):
    out = []
    for x in np.linspace(lo, hi, N):
        try:
            with np.errstate(all="ignore"):
                y = fn(x)
            out.append(bool(np.isfinite(y)))
        except Exception:
            out.append(False)
    return np.array(out), np.linspace(lo, hi, N)
d1, xs = sample_dom(lambda x: math.sqrt(6 - x) if 6 - x >= 0 else float("nan"), N=30001)
ok(all(d1[xs <= 6]) and not any(d1[xs > 6.0001]), "R.5a Dom sqrt(6-x) = ]-oo,6]")
ok(9 - 9 == 0 and (-3)**2 - 9 == 0 and all(x*x - 9 != 0 for x in (0, 1, 2, 4)), "R.5b racines du dénominateur : -3 et 3")
ok(F(1) / (2**2 - 9) == F(-1, 5), "R.5b exemple f(2)")
ok(-2 + 2 == 0 and 4 - 4 == 0, "R.5c conditions : x+2>=0 et x-4 != 0")
ok(F(80) / 4 == 20, "R.5 IMC(2) = 20")
# IMC(h) = 80/h^2 : Dom math = R_0

# ---------- S.3 et R.6 : f(x) = (x+2)(x-1)^2 sur [-3,3] ----------
f5 = lambda x: (x + 2) * (x - 1)**2
ok(all(f5(x) == x**3 - 3*x + 2 for x in range(-5, 6)), "R.6 forme développée")
ok(f5(-3) == -16 and f5(3) == 20, "R.6 extrémités -16 et 20")
ok(f5(-1) == 4 and f5(2) == 4, "R.6 f(-1)=f(2)=4")
ok(f5(-2) == 0 and f5(1) == 0 and f5(0) == 2, "R.6 racines, f(0)=2")
xs = np.linspace(-3, 3, 600001)
ys = f5(xs)
ok(close(ys.min(), -16, 1e-6) and close(ys.max(), 20, 1e-6), "R.6 Im(f) = [-16,20]")
ok(count_solutions(f5, 4, -3, 3) == 2, "R.6 antécédents de 4 : deux")
ok(count_solutions(f5, 2, -3, 3) == 3, "R.6 antécédents de 2 : trois (0 et +-sqrt3)")
ok(close(math.sqrt(3)**3 - 3*math.sqrt(3), 0, 1e-12), "R.6 f(x)=2 en x(x^2-3)=0")
ok(count_solutions(f5, 10, -3, 3) == 1, "R.6 antécédents de 10 : un")
ok(count_solutions(f5, 25, -3, 3) == 0, "R.6 antécédents de 25 : aucun")
m = (xs >= -3) & (xs <= 0)
ok(close(ys[m].min(), -16, 1e-6) and close(ys[m].max(), 4, 1e-6), "R.6 f([-3,0]) = [-16,4]")
m = (xs >= 1) & (xs <= 3)
ok(close(ys[m].min(), 0, 1e-6) and close(ys[m].max(), 20, 1e-6), "R.6 f([1,3]) = [0,20]")
# signe
ok(np.all(ys[xs < -2 - 1e-9] < 0) and np.all(ys[(xs > -2 + 1e-9) & (np.abs(xs - 1) > 1e-9)] > 0), "S.3 signe de f")
# variations
dx = np.diff(ys)
mid = (xs[:-1] + xs[1:]) / 2
ok(np.all(dx[mid < -1] > 0) and np.all(dx[(mid > -1) & (mid < 1)] < 0) and np.all(dx[mid > 1] > 0), "S.3 variations")
ok(f5(-1) == 4 and f5(1) == 0, "S.3 maximum local 4 en -1, minimum local 0 en 1")
ok(f5(3) == 20 and f5(3) > f5(-1) and all(f5(x / 100) <= 20 for x in range(-300, 301)), "S.3 (d) le maximum sur [-3,3] vaut 20 en 3, pas 4")
dom = lambda lo, hi, c: (xs >= lo) & (xs <= hi) & (np.abs(xs - c) < 0.5)
ok(f5(-3) == -16 and np.all(ys[dom(-3, 3, -3)] >= -16 - 1e-12), "S.3 (d) minimum local en -3 (extrémité), valeur -16")
ok(np.all(ys[dom(-3, 3, 3)] <= 20 + 1e-12), "S.3 (d) maximum local en 3 (extrémité), valeur 20")
ok(min(f5(x / 100) for x in range(-300, 301)) == -16, "S.3 (d) minimum de f sur [-3,3] vaut -16")
ok(np.all(ys[np.abs(xs + 1) < 0.5] <= 4 + 1e-12) and np.all(ys[np.abs(xs - 1) < 0.5] >= -1e-12), "S.3 extrema locaux")
# positive et décroissante sur ]-1,1[ ; négative et croissante sur [-3,-2[
mm = (xs > -1) & (xs < 1)
ok(np.all(ys[mm] > 0) and np.all(np.diff(ys[mm]) < 0), "S.3 positive et décroissante sur ]-1,1[")
mm = (xs >= -3) & (xs < -2)
ok(np.all(ys[mm] < 0) and np.all(np.diff(ys[mm]) > 0), "S.3 négative et croissante sur [-3,-2[")

# ---------- S.7 et R.9 : composition ----------
fg = {0: 2, 1: 0, 2: 1, 3: 3, 4: 2}           # f lue sur le graphe (aux entiers de [0,4])
gt = {0: 5, 1: -1, 2: 4, 3: 7}                # g donnée par un tableau
comp = {x: gt[fg[x]] for x in fg}
ok(comp == {0: 4, 1: 5, 2: -1, 3: 7, 4: 4}, "S.7 / R.9 (g o f)(x) pour x = 0..4")
ok(gt[2] == 4 and fg[4] == 2, "S.7 / R.9 (f o g)(2) = f(4) = 2")
ok(gt[1] == -1 and not (0 <= gt[1] <= 4), "S.7 / R.9 (f o g)(1) non défini : g(1) = -1 hors de [0,4]")
ok(gt[0] == 5 and not (0 <= gt[0] <= 4), "S.7 / R.9 (f o g)(0) non défini aussi")
ok(math.sqrt(4 - 2) != 4**0.5 - 2, "S.7 / R.9 (g o f)(4) = sqrt(2), (f o g)(4) = 0")
ok(close(math.sqrt(4 - 2)**2, 2) and 4**0.5 - 2 == 0, "S.7 / R.9 valeurs en x = 4")

# ---------- S.8 : réciproque ----------
f8 = lambda x: -2*x + 4
f8i = lambda x: 2 - F(x) / 2
ok(all(f8i(f8(F(x))) == x and f8(f8i(F(x))) == x for x in range(-6, 7)), "S.8 réciproque de -2x+4")
ok(f8(1) == 2 and f8i(2) == 1, "S.8 symétrie : (1,2) <-> (2,1)")
h = lambda x: x*x - 4
ok(h(3) == 5 and h(-3) == 5, "S.8 h non injective : h(3)=h(-3)")
hi = lambda y: -math.sqrt(y + 4)
ok(all(close(hi(h(x)), x) for x in (-5, -3, -1, 0)), "S.8 h^{-1}(h(x)) = x pour x<=0")
ok(close(hi(5), -3) and close(hi(-4), 0) and close(hi(0), -2), "S.8 valeurs de h^{-1}")

# ---------- T1 : Mosteller ----------
S = lambda h_, w_: math.sqrt(h_*w_/3600)
ok(close(S(180, 45), 1.5) and close(S(180, 80), 2.0), "T.1 S(45)=1,5 ; S(80)=2")
ok(F(180, 3600) == F(1, 20), "T.1 S(w) = sqrt(w/20)")
ok(all(close(S(180, 20*s*s), s) for s in (1, 1.5, 2, 2.5)), "T.1 w = 20 S^2 réciproque")
ok(20 * 2**2 == 80, "T.1 réciproque : 20*4 = 80")

# ---------- T2 : dilution NaCl ----------
m0 = F(9) * F(1, 2)
ok(m0 == F(9, 2), "T.2 m0 = 4,5 g")
C = lambda V: m0 / (F(1, 2) + V)
ok([C(V) for V in (0, F(1, 2), 1, F(9, 2))] == [9, F(9, 2), 3, F(9, 10)], "T.2 tableau C(0), C(0,5), C(1), C(4,5)")
ok(C(2) == F(9, 5), "T.2 C(2) = 1,8")
ok(C(1) == 3, "T.2 lecture : C=3 g/L pour V=1 L")
ok(F(9, 2) / F(9, 10) - F(1, 2) == F(9, 2), "T.2 V pour C = 0,9 : 4,5 L")
ok(all(C(V) > 0 and C(V) <= 9 for V in (0, 1, 10, 100, 1000)), "T.2 Im pratique ]0,9]")

# ---------- T3 : Cockcroft-Gault ----------
cg = lambda a, w_, s_: F(140 - a) * w_ / (72 * F(s_))
ok(F(140 - 60) * 81 / 72 == 90, "T.3 constante 90")
ok(cg(60, 81, F(3, 2)) == 60 and cg(60, 81, 3) == 30 and cg(60, 81, F(9, 10)) == 100, "T.3 valeurs")
ok(all(30 <= cg(60, 81, F(s)) < 60 for s in (F(151, 100), 2, F(299, 100), 3)), "T.3 s dans ]1,5 ; 3] donne ClCr dans [30;60[")
ok(not (30 <= cg(60, 81, F(3, 2)) < 60) and not (30 <= cg(60, 81, F(301, 100)) < 60), "T.3 bornes exclues/hors")
ok(cg(60, 81, 4) * 2 == cg(60, 81, 2) , "T.3 doubler s divise par 2 (s=2 -> 4)")
ok(F(90, 45) == 2, "T.3 réciproque : s = 90/45 = 2")

# ---------- R.4 : Fox vs Tanaka ----------
fox = lambda a: 220 - a
ok([fox(a) for a in (20, 40, 60)] == [200, 180, 160], "R.4 Fox")
ok(all(fox(a) == tan(a) for a in [40]) and fox(60) < tan(60) and fox(20) > tan(20), "R.4 égalité en 40, Tanaka plus haut après")
ok(F(12) / F(3, 10) == 40, "R.4 220 - a = 208 - 0,7a : a = 40")

# ---------- R.7 : x^3 - 3x sur [-2,2] ----------
f5b = lambda x: x**3 - 3*x
xs = np.linspace(-2, 2, 400001)
ys = f5b(xs)
ok(f5b(-1) == 2 and f5b(1) == -2 and f5b(-2) == -2 and f5b(2) == 2, "R.7 valeurs clés")
ok(close(ys.max(), 2, 1e-6) and close(ys.min(), -2, 1e-6), "R.7 extrema globaux 2 et -2")
ok(count_solutions(f5b, 2, -2, 2) == 2 and count_solutions(f5b, -2, -2, 2) == 2, "R.7 max global atteint 2 fois, min 2 fois")
r3 = math.sqrt(3)
ok(close(f5b(r3), 0, 1e-12) and close(f5b(-r3), 0, 1e-12), "R.7 racines")
ok(np.all(ys[xs < -r3 - 1e-6] < 0) and np.all(ys[(xs > -r3 + 1e-6) & (xs < -1e-6)] > 0)
   and np.all(ys[(xs > 1e-6) & (xs < r3 - 1e-6)] < 0) and np.all(ys[xs > r3 + 1e-6] > 0), "R.7 signe")
dx = np.diff(ys); mid = (xs[:-1] + xs[1:]) / 2
ok(np.all(dx[mid < -1] > 0) and np.all(dx[(mid > -1) & (mid < 1)] < 0) and np.all(dx[mid > 1] > 0), "R.7 variations")

# ---------- R.10 : compositions et réciproques ----------
f6 = lambda x: 3*x - 2
g6 = lambda x: x*x
ok(all(g6(f6(x)) == (3*x - 2)**2 and f6(g6(x)) == 3*x*x - 2 for x in range(-5, 6)), "R.10 compositions")
ok(all(F(f6(F(x)) + 2, 3) == x for x in range(-5, 6)), "R.10 réciproque (x+2)/3")
ok(all(close(math.sqrt((x*x - 1) + 1), x) for x in (0, 1, 2, 5)), "R.10 h^{-1}(h(x)) = x sur R+")

# ---------- D1 : h = g o f, f(x) = (x+1)/(x-1), g = racine carrée ----------
fD = lambda x: (x + 1) / (x - 1)
hD = lambda x: math.sqrt(fD(x))
def in_dom(x):
    return x != 1 and fD(x) >= 0
# domaine : R \ ]-1, 1]
xs = np.concatenate([np.linspace(-60, 60, 240001), [-1.0, 1.0, 0.0]])
for x in xs:
    ok_dom = (x <= -1) or (x > 1)
    assert in_dom(x) == ok_dom or abs(x - 1) < 1e-12, f"D.1 domaine en x={x}"
n_ok += 1
vals = np.array([hD(x) for x in xs if (x <= -1 or x > 1)])
ok(np.all(vals >= 0) and not np.any(np.isclose(vals, 1.0, atol=1e-12)), "D.1 la valeur 1 n'est jamais atteinte, aucune valeur négative")
ok(vals.min() == 0.0 and vals.max() > 50, "D.1 valeur 0 atteinte (en x = -1), valeurs arbitrairement grandes")
ok(np.any((vals > 0.9) & (vals < 1)) and np.any((vals > 1) & (vals < 1.1)), "D.1 valeurs proches de 1 des deux côtés")
# réciproque : h^{-1}(t) = (t^2+1)/(t^2-1) pour t >= 0, t != 1
hinv = lambda t: (t * t + 1) / (t * t - 1)
for t in [F(0), F(1, 2), F(2), F(3), F(10), F(1, 10), F(11, 10)]:
    x = hinv(t)
    ok((x <= -1 or x > 1) and fD(x) == t * t, f"D.1 t={t} a pour antécédent x={x}")
for x in [-50, -10, -3, -1, F(3, 2), 2, 5, 100]:
    x = F(x)
    t2 = fD(x)                      # t^2 exact
    ok(F(1) * (t2 + 1) / (t2 - 1) == x, f"D.1 h^-1(h(x)) = x pour x = {x}")
ok(F(0) * 0 == 0 and hinv(F(0)) == -1, "D.1 h^{-1}(0) = -1")

# ---------- D2 : involution ----------
def comp_ok(p, q):
    """f o f = identité sur les x où elle est définie, avec f injective."""
    inj = (-2*p - q) != 0
    if not inj:
        return False
    for x in (F(-7), F(-3), F(-1), F(0), F(1), F(3), F(5), F(11), F(1, 2)):
        if x == 2:
            continue
        y = (p*x + q) / (x - 2)
        if y == 2:
            continue
        if (p*y + q) / (y - 2) != x:
            return False
    return True
sols = [(p, q) for p in range(-8, 9) for q in range(-12, 13) if comp_ok(p, q)]
ok(all(p == 2 and q != -4 for p, q in sols) and len(sols) == 24, f"D.2 solutions entières : p=2, q<>-4 (trouvé {len(sols)})")
ok(all(comp_ok(2, q) for q in (-10, -3, 0, 1, 7)) and not comp_ok(2, -4) and not comp_ok(3, 0) and not comp_ok(1, 1), "D.2 contrôles")
# q = -4 : f constante égale à 2
ok(all((2*F(x) - 4) / (F(x) - 2) == 2 for x in (-3, 0, 1, 3, 10)), "D.2 q=-4 : f(x)=2")

# ---------- D3 ----------
g3d = lambda x: np.abs(x**2 - 4*x + 3)
for a, expected in [(0, 2), (F(1, 2), 4), (1, 3), (F(3, 2), 2), (5, 2), (F(9, 10), 4)]:
    ok(count_solutions(g3d, float(a), -10, 10) == expected, f"D.3 a={a}: {expected} antécédents")
ok(close(g3d(2 - math.sqrt(2)), 1) and close(g3d(2.0), 1) and close(g3d(2 + math.sqrt(2)), 1), "D.3 antécédents de 1")


# ---------- Slides et fiches de méthode (séance 5) ----------
# T.1 corrigé pas à pas (Mosteller, h = 180)
S1m = lambda w: math.sqrt(180 * w / 3600)
ok(close(S1m(45), 1.5) and close(S1m(80), 2) and close(S1m(20), 1), "Slides T.1 S(45)=1,5 ; S(80)=2 ; S(20)=1")
ok(all(close(20 * S1m(w) ** 2, w) for w in (5, 45, 80, 100)), "Slides T.1 w = 20 S^2")
ok(close(S1m(5), 0.5) and close(S1m(125), 2.5), "Slides T.1 S(5)=0,5")
ok(abs(104/1.8 - 32 - 25.8) < 0.05 and (7/2 - 1) == 2.5 and 2*2.5 + 1 != 7, "Slides pièges : 104/1,8-32 ~ 25,8 ; Q3 : 2,5")
ok(2*3 + 1 == 7 and F(8-2, 3-1) == 3, "Slides Q2/Q3")
# Méthode 1 : conversion F = 1,8 C + 32
ok(F(18, 10) * 40 + 32 == 104 and (F(104) - 32) / F(18, 10) == 40, "M1 104 F = 40 C")
ok((F(986, 10) - 32) / F(18, 10) == 37 and F(18, 10) * 20 + 32 == 68, "M1 98,6 F = 37 C ; 20 C = 68 F")
# Méthode 2 : signe de x(x^2-4) et de x(x-2)^2
fm = lambda x: x * (x * x - 4)
ok([fm(x) for x in (-3, -1, 1, 3)] == [-15, 3, -3, 15], "M2 signes de x(x^2-4)")
hm = lambda x: x * (x - 2) ** 2
ok([hm(x) for x in (-1, 1, 3)] == [-9, 1, 3] and hm(0) == 0 and hm(2) == 0, "M2 x(x-2)^2 : pas de changement de signe en 2")


# ---------- S.1 : diagrammes sagittaux ----------
A1 = {-2: 4, -1: 1, 0: 0, 1: 1, 2: 4}
ok(all(v == k * k for k, v in A1.items()) and sorted(set(A1.values())) == [0, 1, 4], "S.1 (1) f(x)=x^2, Im={0,1,4}, 5 sans antécédent")
ok(sorted(k for k, v in A1.items() if v == 1) == [-1, 1], "S.1 (1) antécédents de 1 : -1 et 1")
R2 = [(1, 2), (2, 4), (2, 6), (3, 6)]
ok(len([a for a, b in R2 if a == 2]) == 2, "S.1 (2) 2 a deux images : pas une fonction")
A3 = {1: 1, 2: 4, 3: 9}
ok(all(v == k * k for k, v in A3.items()) and 4 not in A3 and 16 not in A3.values(), "S.1 (3) g(x)=x^2 sur {1,2,3}")
# ---------- S.2 : conversions de registres ----------
g5 = lambda x: 2 * x - 3
ok([g5(x) for x in (-1, 0, 1, 2, 3)] == [-5, -3, -1, 1, 3], "S.2 g(x)=2x-3")
f5 = lambda x: (x - 1) ** 2
ok([f5(x) for x in (-1, 0, 1, 2, 3)] == [4, 1, 0, 1, 4] and [1 - x for x in (-1, 0, 1, 2, 3)][0] == 2, "S.2 f(x)=(x-1)^2 ; piège 1-x donne 2 en -1")
k5 = lambda x: F(-1, 2) * x + 1
ok([k5(x) for x in (-2, 0, 2, 4)] == [2, 1, 0, -1] and k5(-1) == F(3, 2) and k5(3) == F(-1, 2), "S.2 k(x)=-x/2+1")
ok(2 * (0 - 3) == -6 and F(1, 2) * 2 + 1 == 2, "S.2 pièges")
vals = [f5(x) for x in (-1, 0, 1, 2, 3)]
ok(vals[:3] == sorted(vals[:3], reverse=True) and vals[2:] == sorted(vals[2:]) and vals != sorted(vals) and vals != sorted(vals, reverse=True), "S.2 f ni croissante ni décroissante")


# ---------- Corrections après relecture (discriminants, images, défis, méthodes, slides) ----------
disc = lambda a, b, c: b * b - 4 * a * c
ok(disc(1, -2, -8) == 36 and sorted([(2 - 6) / 2, (2 + 6) / 2]) == [-2, 4], "R.2 discriminant 36, solutions -2 et 4")
ok(18.5 <= 80 / 2 ** 2 < 25, "R.5 IMC 20 dans la corpulence normale OMS")
ok(all(close((-math.sqrt(y + 4)) ** 2 - 4, y) for y in (-4, -1, 0, 5, 12)), "S.8 tout y >= -4 est atteint")
ok(all(close((math.sqrt(y + 1)) ** 2 - 1, y) for y in (-1, 0, 3, 8)), "R.10 tout y >= -1 est atteint")
ok(all(close(4.5 / (0.5 + (4.5 / c - 0.5)), c) and 4.5 / c - 0.5 >= 0 for c in (0.01, 0.9, 3, 9)), "T.2 toute concentration de ]0, 9] est atteinte")
# D.1 : h^{-1} défait h sur des valeurs du domaine
hD = lambda x: math.sqrt((x + 1) / (x - 1))
hDi = lambda y: (y * y + 1) / (y * y - 1)
ok(all(close(hDi(hD(x)), x) for x in (-5, -2, -1, 1.5, 3, 10)), "D.1 h^{-1}(h(x)) = x")
ok(close(hD(-1), 0) and all(hD(x) < 1 for x in (-1, -3, -100)) and all(hD(x) > 1 for x in (1.01, 2, 100)), "D.1 image : [0,1[ à gauche, ]1,+inf[ à droite")
# D.3 : discussion selon a
for a, expected in [(-1, 0), (0, 2), (F(1, 4), 4), (1, 3), (2, 2)]:
    ok(count_solutions(g3d, float(a), -10, 10) == expected, f"D.3 a={a}: {expected} solutions")
# M1 : x^2 - 4 = 5
ok(3 ** 2 - 4 == 5 and (-3) ** 2 - 4 == 5, "M1 deux solutions 3 et -3")
# M2 : (x-1)/(x+2)
q = lambda x: F(x - 1, x + 2)
ok(q(-3) == 4 and q(0) == F(-1, 2) and q(2) == F(1, 4) and q(1) == 0, "M2 signes de (x-1)/(x+2)")
# Slides T.1 : nouveau tableau
ok(close(S1m(61.25), 1.75) and close(S1m(125), 2.5), "Slides T.1 S(61,25)=1,75 ; S(125)=2,5")


# ---------- Extrema sur un intervalle (S.4, R.8, fiche) ----------
def extrema(f, a, b, ia, ib, n=6000):
    """Renvoie (max existe, min existe) pour f continue sur l'intervalle de bornes a, b (ia, ib : bornes incluses)."""
    xs = [a + (b - a) * k / n for k in range(n + 1)]
    closed = [f(x) for x in xs]
    inside = [f(x) for k, x in enumerate(xs) if (0 < k < n) or (k == 0 and ia) or (k == n and ib)]
    return abs(max(inside) - max(closed)) < 1e-9, abs(min(inside) - min(closed)) < 1e-9
def lettre(mx, mn):
    return {(True, True): "A", (True, False): "B", (False, True): "C", (False, False): "D"}[(mx, mn)]
f9 = lambda x: x * x - 4 * x + 3
for (a, b, ia, ib), L in [((0, 5, True, True), "A"), ((0, 5, True, False), "C"), ((2, 5, False, True), "B"),
                          ((2, 5, False, False), "D"), ((0, 4, True, False), "A")]:
    ok(lettre(*extrema(f9, a, b, ia, ib)) == L, f"S.4 intervalle {a},{b} ({ia},{ib}) : réponse {L}")
ok([f9(x) for x in (0, 2, 4, 5)] == [3, -1, 3, 8], "S.4 valeurs f(0), f(2), f(4), f(5)")
h7 = lambda x: abs(x - 1) + 1
for (a, b, ia, ib), L in [((-1, 3, True, False), "A"), ((-1, 3, False, False), "C"), ((1, 3, False, True), "B"), ((0, 2, True, True), "A")]:
    ok(lettre(*extrema(h7, a, b, ia, ib)) == L, f"R.8 intervalle {a},{b} ({ia},{ib}) : réponse {L}")
ok([h7(x) for x in (-1, 0, 1, 2, 3)] == [3, 2, 1, 2, 3], "R.8 valeurs de h")
# Question type de l'évaluation (non reprise sur le site) : -x^2 + 4 sur [-2 ; 3[ -> uniquement un maximum
ok(lettre(*extrema(lambda x: -x * x + 4, -2, 3, True, False)) == "B", "Question d'évaluation : uniquement un maximum")
g_fiche = lambda x: 2 * x - 1
ok([lettre(*extrema(g_fiche, 0, 3, True, True)), lettre(*extrema(g_fiche, 0, 3, True, False)), lettre(*extrema(g_fiche, 0, 3, False, False))] == ["A", "C", "D"], "Fiche extrema : 2x - 1 sur [0,3], [0,3[, ]0,3[")
# Fiches domaine, image, réciproque
ok(3 - (-1) >= 0, "Fiche domaine : -1 vérifie x <= 3, donc on le retire")
fi = lambda x: (x - 1) ** 2
ok(fi(2) == 1 and fi(-1) == 4 and fi(3) == 4 and fi(4) == 9 and fi(-2) == 9 and min(fi(x / 100) for x in range(-100, 401)) == 0, "Fiche image : (x-1)^2 sur [-1,4]")
ok(all(close(math.sqrt(x - 1) ** 2 + 1, x) for x in (1, 2, 5, 10)), "Fiche réciproque : sqrt(x-1) et x^2 + 1")
# T.1 : piège S(40)
ok(close(S1m(40), math.sqrt(2)), "T.1 piège : S(40) = racine de 2")
# Échauffement Q2
ok([x for x in (-1, 0, 2.5, 3) if 0 <= x < 3] == [0, 2.5], "Échauffement Q2 : 0 et 2,5 dans [0, 3[")


# ---------- S.5 : domaines et perfusion ----------
ok((-3 + 3) >= 0 and 1 > -3, "S.5 (a) Dom = [-3, +inf[ privé de 1")
ok(F(500, 125) == 4 and F(500, 5) == 100 and F(500, 100) == 5, "S.5 (b) t(125) = 4 h ; t(d) = 5 donne d = 100 mL/h")

# ---------- R.7 (d) : extrema locaux, extrémités comprises ----------
h7 = lambda x: x**3 - 3 * x
xs7 = np.linspace(-2, 2, 400001)
ys7 = h7(xs7)
ok(h7(-2) == -2 and h7(-1) == 2 and h7(1) == -2 and h7(2) == 2, "R.7 (d) valeurs aux quatre abscisses")
ok(np.all(ys7[xs7 < -2 + 0.3] >= -2 - 1e-12) and np.all(ys7[xs7 > 2 - 0.3] <= 2 + 1e-12), "R.7 (d) minimum local en -2, maximum local en 2")
ok(abs(ys7.max() - 2) < 1e-9 and abs(ys7.min() + 2) < 1e-9, "R.7 (d) extrema globaux 2 et -2")

# ---------- S.6 : étude de signe de x(x-3)/(x+1) ----------
g6 = lambda x: x * (x - 3) / (x + 1)
xs6 = np.linspace(-10, 10, 400001); xs6 = xs6[np.abs(xs6 + 1) > 1e-9]
ys6 = g6(xs6)
ok(g6(0) == 0 and g6(3) == 0, "S.6 racines 0 et 3")
ok(np.all(ys6[xs6 < -1] < 0) and np.all(ys6[(xs6 > -1) & (xs6 < 0)] > 0), "S.6 signe sur ]-inf,-1[ et ]-1,0[")
ok(np.all(ys6[(xs6 > 0) & (xs6 < 3)] < 0) and np.all(ys6[xs6 > 3] > 0), "S.6 signe sur ]0,3[ et ]3,+inf[")
ok(g6(-2) == -10 and abs(g6(-0.5) - 3.5) < 1e-12, "S.6 contrôles f(-2) = -10 et f(-1/2) = 7/2")
ok(set(np.where(ys6 >= 0, 1, 0)[(xs6 > -1) & (xs6 <= 0)]) == {1} and set(np.where(ys6 >= 0, 1, 0)[(xs6 >= 3)]) == {1}, "S.6 f >= 0 sur ]-1,0] et [3,+inf[")

# ---------- S.7 : k(x) = -sqrt(x), h(x) = x-2 ----------
koh = lambda x: -math.sqrt(x - 2)
hok = lambda x: -math.sqrt(x) - 2
ok(close(koh(4), -math.sqrt(2)) and hok(4) == -4 and koh(4) != hok(4), "S.7 (b) valeurs en 4 : -sqrt2 et -4")
ok(koh(2) == 0 and koh(6) == -2 and koh(2) > koh(6), "S.7 (c) contre-exemple à la croissance : 2<6 mais koh(2)>koh(6)")
xs7c = [2 + i / 50 for i in range(0, 1001)]
ok(all(koh(a_) >= koh(b_) for a_, b_ in zip(xs7c, xs7c[1:])), "S.7 (c) k o h décroissante sur [2,+inf[")
ok(sorted(set((-1 < x <= 0) or x >= 3 for x in (-0.5, 0, 3, 5))) == [True], "S.6 (c) ensemble des solutions ]-1,0] U [3,+inf[")

print(f"Toutes les vérifications passent ({n_ok} contrôles).")
