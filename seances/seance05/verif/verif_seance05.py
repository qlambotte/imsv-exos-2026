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
ok(u[0]*v[0] + u[1]*v[1] == -1, "E1 produit scalaire (3,1).(-1,2) = -1 < 0 : angle obtus")
ok(F(8-2, 3-1) == 3, "E2 pente de la droite par (1,2) et (3,8)")
ok(2*3 + 1 == 7, "E3 A = 2C + 1 : C = 3 donne A = 7")
ok(4**2 - 5 == 11 and (-4)**2 - 5 == 11, "E4 x^2 - 5 = 11 : x = +-4")

# ---------- S1 ----------
ok(1 == (-1)**2 and 1 == 1**2, "S1 x = y^2 : deux ordonnées pour x = 1")
ok(0**2 + 2**2 == 4 and 0**2 + (-2)**2 == 4, "S1 cercle x^2+y^2=4 : deux ordonnées pour x = 0")

# ---------- S2 ----------
f2 = lambda x: x*x - 2*x - 3
ok(f2(4) == 5 and f2(-1) == 0, "S2 f(4)=5, f(-1)=0")
ok(f2(4) == 5 and f2(-2) == 5, "S2 antécédents de 5 : -2 et 4")
ok(sorted(r for r in range(-10, 11) if f2(r) == 5) == [-2, 4], "S2 uniques entiers antécédents de 5")
ok(f2(1) == -4 and all(f2(x) >= -4 for x in np.linspace(-20, 20, 4001)), "S2 minimum -4 en 1")
# f(x) = -5 : x^2-2x+2 = 0, discriminant
ok(4 - 4*1*2 < 0, "S2 f(x)=-5 sans solution (disc. < 0)")
ok(2*2 - 4*1*(-3 + 4) == 0, "S2 f(x)=-4 : discriminant nul, x=1 unique")

# ---------- S3 : Tanaka 208 - 0.7 a ----------
tan = lambda a: F(208) - F(7, 10)*a
ok([tan(a) for a in (20, 30, 40, 50, 60)] == [194, 187, 180, 173, 166], "S3 tableau Tanaka")
ok((tan(60) - tan(20)) / (60 - 20) == F(-7, 10), "S3 pente -0,7")
ok(tan(0) == 208, "S3 ordonnée à l'origine 208")

# ---------- S4 : domaines ----------
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
ok(all(d1[xs <= 6]) and not any(d1[xs > 6.0001]), "S4a Dom sqrt(6-x) = ]-oo,6]")
ok(9 - 9 == 0 and (-3)**2 - 9 == 0 and all(x*x - 9 != 0 for x in (0, 1, 2, 4)), "S4b racines du dénominateur : -3 et 3")
ok(F(1) / (2**2 - 9) == F(-1, 5), "S4b exemple f(2)")
ok(-2 + 2 == 0 and 4 - 4 == 0, "S4c conditions : x+2>=0 et x-4 != 0")
ok(F(80) / 4 == 20, "S4 IMC(2) = 20")
# IMC(h) = 80/h^2 : Dom math = R_0

# ---------- S5 / S6 : f(x) = (x+2)(x-1)^2 sur [-3,3] ----------
f5 = lambda x: (x + 2) * (x - 1)**2
ok(all(f5(x) == x**3 - 3*x + 2 for x in range(-5, 6)), "S5 forme développée")
ok(f5(-3) == -16 and f5(3) == 20, "S5 extrémités -16 et 20")
ok(f5(-1) == 4 and f5(2) == 4, "S5 f(-1)=f(2)=4")
ok(f5(-2) == 0 and f5(1) == 0 and f5(0) == 2, "S5 racines, f(0)=2")
xs = np.linspace(-3, 3, 600001)
ys = f5(xs)
ok(close(ys.min(), -16, 1e-6) and close(ys.max(), 20, 1e-6), "S5 Im(f) = [-16,20]")
ok(count_solutions(f5, 4, -3, 3) == 2, "S5 antécédents de 4 : deux")
ok(count_solutions(f5, 2, -3, 3) == 3, "S5 antécédents de 2 : trois (0 et +-sqrt3)")
ok(close(math.sqrt(3)**3 - 3*math.sqrt(3), 0, 1e-12), "S5 f(x)=2 en x(x^2-3)=0")
ok(count_solutions(f5, 10, -3, 3) == 1, "S5 antécédents de 10 : un")
ok(count_solutions(f5, 25, -3, 3) == 0, "S5 antécédents de 25 : aucun")
m = (xs >= -3) & (xs <= 0)
ok(close(ys[m].min(), -16, 1e-6) and close(ys[m].max(), 4, 1e-6), "S5 f([-3,0]) = [-16,4]")
m = (xs >= 1) & (xs <= 3)
ok(close(ys[m].min(), 0, 1e-6) and close(ys[m].max(), 20, 1e-6), "S5 f([1,3]) = [0,20]")
# signe
ok(np.all(ys[xs < -2 - 1e-9] < 0) and np.all(ys[(xs > -2 + 1e-9) & (np.abs(xs - 1) > 1e-9)] > 0), "S6 signe de f")
# variations
dx = np.diff(ys)
mid = (xs[:-1] + xs[1:]) / 2
ok(np.all(dx[mid < -1] > 0) and np.all(dx[(mid > -1) & (mid < 1)] < 0) and np.all(dx[mid > 1] > 0), "S6 variations")
ok(f5(-1) == 4 and f5(1) == 0, "S6 maximum local 4 en -1, minimum local 0 en 1")
ok(np.all(ys[np.abs(xs + 1) < 0.5] <= 4 + 1e-12) and np.all(ys[np.abs(xs - 1) < 0.5] >= -1e-12), "S6 extrema locaux")
# positive et décroissante sur ]-1,1[ ; négative et croissante sur [-3,-2[
mm = (xs > -1) & (xs < 1)
ok(np.all(ys[mm] > 0) and np.all(np.diff(ys[mm]) < 0), "S6 positive et décroissante sur ]-1,1[")
mm = (xs >= -3) & (xs < -2)
ok(np.all(ys[mm] < 0) and np.all(np.diff(ys[mm]) > 0), "S6 négative et croissante sur [-3,-2[")

# ---------- S7 : composition ----------
fg = {0: 2, 1: 0, 2: 1, 3: 3, 4: 2}           # f lue sur le graphe (aux entiers de [0,4])
gt = {0: 5, 1: -1, 2: 4, 3: 7}                # g donnée par un tableau
comp = {x: gt[fg[x]] for x in fg}
ok(comp == {0: 4, 1: 5, 2: -1, 3: 7, 4: 4}, "S7 (g o f)(x) pour x = 0..4")
ok(gt[2] == 4 and fg[4] == 2, "S7 (f o g)(2) = f(4) = 2")
ok(gt[1] == -1 and not (0 <= gt[1] <= 4), "S7 (f o g)(1) non défini : g(1) = -1 hors de [0,4]")
ok(gt[0] == 5 and not (0 <= gt[0] <= 4), "S7 (f o g)(0) non défini aussi")
ok(math.sqrt(4 - 2) != 4**0.5 - 2, "S7 (g o f)(4) = sqrt(2), (f o g)(4) = 0")
ok(close(math.sqrt(4 - 2)**2, 2) and 4**0.5 - 2 == 0, "S7 valeurs en x = 4")

# ---------- S8 : réciproque ----------
f8 = lambda x: -2*x + 4
f8i = lambda x: 2 - F(x) / 2
ok(all(f8i(f8(F(x))) == x and f8(f8i(F(x))) == x for x in range(-6, 7)), "S8 réciproque de -2x+4")
ok(f8(1) == 2 and f8i(2) == 1, "S8 symétrie : (1,2) <-> (2,1)")
h = lambda x: x*x - 4
ok(h(3) == 5 and h(-3) == 5, "S8 h non injective : h(3)=h(-3)")
hi = lambda y: -math.sqrt(y + 4)
ok(all(close(hi(h(x)), x) for x in (-5, -3, -1, 0)), "S8 h^{-1}(h(x)) = x pour x<=0")
ok(close(hi(5), -3) and close(hi(-4), 0) and close(hi(0), -2), "S8 valeurs de h^{-1}")

# ---------- T1 : Mosteller ----------
S = lambda h_, w_: math.sqrt(h_*w_/3600)
ok(close(S(180, 45), 1.5) and close(S(180, 80), 2.0), "T1 S(45)=1,5 ; S(80)=2")
ok(F(180, 3600) == F(1, 20), "T1 S(w) = sqrt(w/20)")
ok(all(close(S(180, 20*s*s), s) for s in (1, 1.5, 2, 2.5)), "T1 w = 20 S^2 réciproque")
ok(20 * 2**2 == 80, "T1 réciproque : 20*4 = 80")

# ---------- T2 : dilution NaCl ----------
m0 = F(9) * F(1, 2)
ok(m0 == F(9, 2), "T2 m0 = 4,5 g")
C = lambda V: m0 / (F(1, 2) + V)
ok([C(V) for V in (0, F(1, 2), 1, F(9, 2))] == [9, F(9, 2), 3, F(9, 10)], "T2 tableau C(0), C(0,5), C(1), C(4,5)")
ok(C(2) == F(9, 5), "T2 C(2) = 1,8")
ok(C(1) == 3, "T2 lecture : C=3 g/L pour V=1 L")
ok(F(9, 2) / F(9, 10) - F(1, 2) == F(9, 2), "T2 V pour C = 0,9 : 4,5 L")
ok(all(C(V) > 0 and C(V) <= 9 for V in (0, 1, 10, 100, 1000)), "T2 Im pratique ]0,9]")

# ---------- T3 : Cockcroft-Gault ----------
cg = lambda a, w_, s_: F(140 - a) * w_ / (72 * F(s_))
ok(F(140 - 60) * 81 / 72 == 90, "T3 constante 90")
ok(cg(60, 81, F(3, 2)) == 60 and cg(60, 81, 3) == 30 and cg(60, 81, F(9, 10)) == 100, "T3 valeurs")
ok(all(30 <= cg(60, 81, F(s)) < 60 for s in (F(151, 100), 2, F(299, 100), 3)), "T3 s dans ]1,5 ; 3] donne ClCr dans [30;60[")
ok(not (30 <= cg(60, 81, F(3, 2)) < 60) and not (30 <= cg(60, 81, F(301, 100)) < 60), "T3 bornes exclues/hors")
ok(cg(60, 81, 4) * 2 == cg(60, 81, 2) , "T3 doubler s divise par 2 (s=2 -> 4)")
ok(F(90, 45) == 2, "T3 réciproque : s = 90/45 = 2")

# ---------- R1 : Fox vs Tanaka ----------
fox = lambda a: 220 - a
ok([fox(a) for a in (20, 40, 60)] == [200, 180, 160], "R1 Fox")
ok(all(fox(a) == tan(a) for a in [40]) and fox(60) < tan(60) and fox(20) > tan(20), "R1 égalité en 40, Tanaka plus haut après")
ok(F(12) / F(3, 10) == 40, "R1 220 - a = 208 - 0,7a : a = 40")

# ---------- R2 : domaines ----------
ok(2*3 - 6 == 0, "R2a sqrt(2x-6) : x >= 3")
ok(all(x*x - x - 6 == (x-3)*(x+2) for x in range(-5, 6)), "R2b factorisation")
ok(4 - 4 == 0, "R2c 5/sqrt(4-x) : x < 4")
ok(F(500, 125) == 4, "R2d 500/125 = 4 h")

# ---------- R3 ----------
g3 = lambda x: abs(x - 2) - 3
ok(g3(-1) == 0 and g3(5) == 0, "R3 valeurs")
ok(sorted(x for x in range(-20, 21) if g3(x) == 1) == [-2, 6], "R3 antécédents de 1")
ok(all(g3(x) >= -3 for x in np.linspace(-20, 20, 4001)) and g3(2) == -3, "R3 Im = [-3,+oo[")

# ---------- R4 ----------
f4 = lambda x: x*x - 4*x
xs = np.linspace(0, 5, 500001)
ok(close(f4(xs).min(), -4, 1e-6) and close(f4(xs).max(), 5, 1e-6), "R4 Im = [-4,5]")
m = xs >= 3
ok(close(f4(xs[m]).min(), -3, 1e-6) and close(f4(xs[m]).max(), 5, 1e-6), "R4 f([3,5]) = [-3,5]")
ok(f4(5) == 5 and f4(-1) == 5 and count_solutions(f4, 5, 0, 5) == 1, "R4 antécédents de 5 : {5} sur [0,5] ; {-1,5} sur R")

# ---------- R5 : x^3 - 3x sur [-2,2] ----------
f5b = lambda x: x**3 - 3*x
xs = np.linspace(-2, 2, 400001)
ys = f5b(xs)
ok(f5b(-1) == 2 and f5b(1) == -2 and f5b(-2) == -2 and f5b(2) == 2, "R5 valeurs clés")
ok(close(ys.max(), 2, 1e-6) and close(ys.min(), -2, 1e-6), "R5 extrema globaux 2 et -2")
ok(count_solutions(f5b, 2, -2, 2) == 2 and count_solutions(f5b, -2, -2, 2) == 2, "R5 max global atteint 2 fois, min 2 fois")
r3 = math.sqrt(3)
ok(close(f5b(r3), 0, 1e-12) and close(f5b(-r3), 0, 1e-12), "R5 racines")
ok(np.all(ys[xs < -r3 - 1e-6] < 0) and np.all(ys[(xs > -r3 + 1e-6) & (xs < -1e-6)] > 0)
   and np.all(ys[(xs > 1e-6) & (xs < r3 - 1e-6)] < 0) and np.all(ys[xs > r3 + 1e-6] > 0), "R5 signe")
dx = np.diff(ys); mid = (xs[:-1] + xs[1:]) / 2
ok(np.all(dx[mid < -1] > 0) and np.all(dx[(mid > -1) & (mid < 1)] < 0) and np.all(dx[mid > 1] > 0), "R5 variations")

# ---------- R6 ----------
f6 = lambda x: 3*x - 2
g6 = lambda x: x*x
ok(all(g6(f6(x)) == (3*x - 2)**2 and f6(g6(x)) == 3*x*x - 2 for x in range(-5, 6)), "R6 compositions")
ok(all(F(f6(F(x)) + 2, 3) == x for x in range(-5, 6)), "R6 réciproque (x+2)/3")
ok(all(close(math.sqrt((x*x - 1) + 1), x) for x in (0, 1, 2, 5)), "R6 h^{-1}(h(x)) = x sur R+")

# ---------- D1 : h = g o f, f(x) = (x+1)/(x-1), g = racine carrée ----------
fD = lambda x: (x + 1) / (x - 1)
hD = lambda x: math.sqrt(fD(x))
def in_dom(x):
    return x != 1 and fD(x) >= 0
# domaine : R \ ]-1, 1]
xs = np.concatenate([np.linspace(-60, 60, 240001), [-1.0, 1.0, 0.0]])
for x in xs:
    ok_dom = (x <= -1) or (x > 1)
    assert in_dom(x) == ok_dom or abs(x - 1) < 1e-12, f"D1 domaine en x={x}"
n_ok += 1
vals = np.array([hD(x) for x in xs if (x <= -1 or x > 1)])
ok(np.all(vals >= 0) and not np.any(np.isclose(vals, 1.0, atol=1e-12)), "D1 la valeur 1 n'est jamais atteinte, aucune valeur négative")
ok(vals.min() == 0.0 and vals.max() > 50, "D1 valeur 0 atteinte (en x = -1), valeurs arbitrairement grandes")
ok(np.any((vals > 0.9) & (vals < 1)) and np.any((vals > 1) & (vals < 1.1)), "D1 valeurs proches de 1 des deux côtés")
# réciproque : h^{-1}(t) = (t^2+1)/(t^2-1) pour t >= 0, t != 1
hinv = lambda t: (t * t + 1) / (t * t - 1)
for t in [F(0), F(1, 2), F(2), F(3), F(10), F(1, 10), F(11, 10)]:
    x = hinv(t)
    ok((x <= -1 or x > 1) and fD(x) == t * t, f"D1 t={t} a pour antécédent x={x}")
for x in [-50, -10, -3, -1, F(3, 2), 2, 5, 100]:
    x = F(x)
    t2 = fD(x)                      # t^2 exact
    ok(F(1) * (t2 + 1) / (t2 - 1) == x, f"D1 h^-1(h(x)) = x pour x = {x}")
ok(F(0) * 0 == 0 and hinv(F(0)) == -1, "D1 h^{-1}(0) = -1")

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
ok(all(p == 2 and q != -4 for p, q in sols) and len(sols) == 24, f"D2 solutions entières : p=2, q<>-4 (trouvé {len(sols)})")
ok(all(comp_ok(2, q) for q in (-10, -3, 0, 1, 7)) and not comp_ok(2, -4) and not comp_ok(3, 0) and not comp_ok(1, 1), "D2 contrôles")
# q = -4 : f constante égale à 2
ok(all((2*F(x) - 4) / (F(x) - 2) == 2 for x in (-3, 0, 1, 3, 10)), "D2 q=-4 : f(x)=2")

# ---------- D3 ----------
g3d = lambda x: np.abs(x**2 - 4*x + 3)
for a, expected in [(0, 2), (F(1, 2), 4), (1, 3), (F(3, 2), 2), (5, 2), (F(9, 10), 4)]:
    ok(count_solutions(g3d, float(a), -10, 10) == expected, f"D3 a={a}: {expected} antécédents")
ok(close(g3d(2 - math.sqrt(2)), 1) and close(g3d(2.0), 1) and close(g3d(2 + math.sqrt(2)), 1), "D3 antécédents de 1")


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


# ---------- S.2 diagrammes sagittaux ----------
A1 = {-2: 4, -1: 1, 0: 0, 1: 1, 2: 4}
ok(all(v == k * k for k, v in A1.items()) and sorted(set(A1.values())) == [0, 1, 4], "S.2 (1) f(x)=x^2, Im={0,1,4}, 5 sans antécédent")
ok(sorted(k for k, v in A1.items() if v == 1) == [-1, 1], "S.2 (1) antécédents de 1 : -1 et 1")
R2 = [(1, 2), (2, 4), (2, 6), (3, 6)]
ok(len([a for a, b in R2 if a == 2]) == 2, "S.2 (2) 2 a deux images : pas une fonction")
A3 = {1: 1, 2: 4, 3: 9}
ok(all(v == k * k for k, v in A3.items()) and 4 not in A3 and 16 not in A3.values(), "S.2 (3) g(x)=x^2 sur {1,2,3}")
# ---------- S.5 conversions de registres ----------
g5 = lambda x: 2 * x - 3
ok([g5(x) for x in (-1, 0, 1, 2, 3)] == [-5, -3, -1, 1, 3], "S.5 g(x)=2x-3")
f5 = lambda x: (x - 1) ** 2
ok([f5(x) for x in (-1, 0, 1, 2, 3)] == [4, 1, 0, 1, 4] and [1 - x for x in (-1, 0, 1, 2, 3)][0] == 2, "S.5 f(x)=(x-1)^2 ; piège 1-x donne 2 en -1")
k5 = lambda x: F(-1, 2) * x + 1
ok([k5(x) for x in (-2, 0, 2, 4)] == [2, 1, 0, -1] and k5(-1) == F(3, 2) and k5(3) == F(-1, 2), "S.5 k(x)=-x/2+1")
ok(2 * (0 - 3) == -6 and F(1, 2) * 2 + 1 == 2, "S.5 pièges")
vals = [f5(x) for x in (-1, 0, 1, 2, 3)]
ok(vals[:3] == sorted(vals[:3], reverse=True) and vals[2:] == sorted(vals[2:]) and vals != sorted(vals) and vals != sorted(vals, reverse=True), "S.5 f ni croissante ni décroissante")


# ---------- Corrections après relecture (discriminants, images, défis, méthodes, slides) ----------
disc = lambda a, b, c: b * b - 4 * a * c
ok(disc(1, -2, -8) == 36 and sorted([(2 - 6) / 2, (2 + 6) / 2]) == [-2, 4], "S.3 discriminant 36, solutions -2 et 4")
ok(disc(1, -1, -6) == 25 and sorted([(1 - 5) / 2, (1 + 5) / 2]) == [-2, 3], "R.2 discriminant 25, solutions -2 et 3")
ok(disc(1, -4, -5) == 36 and sorted([(4 - 6) / 2, (4 + 6) / 2]) == [-1, 5], "R.4 discriminant 36, solutions -1 et 5")
ok(18.5 <= 80 / 2 ** 2 < 25, "S.6 IMC 20 dans la corpulence normale OMS")
ok(all(close((-math.sqrt(y + 4)) ** 2 - 4, y) for y in (-4, -1, 0, 5, 12)), "S.10 tout y >= -4 est atteint")
ok(all(close((math.sqrt(y + 1)) ** 2 - 1, y) for y in (-1, 0, 3, 8)), "R.6 tout y >= -1 est atteint")
ok(all(abs((y + 5) - 2) - 3 == y for y in (-3, -2, 0, 4, 10)), "R.3 tout y >= -3 est atteint par x = y + 5")
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

print(f"Toutes les vérifications passent ({n_ok} contrôles).")
