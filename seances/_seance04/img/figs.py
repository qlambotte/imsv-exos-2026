#!/usr/bin/env python3
"""Figures de la séance 4 — usage : python3 figs.py (depuis n'importe où).
Figures de la séance 4 (vecteurs) — matplotlib → SVG, texte VECTORISÉ (chemins),
maths en Computer Modern : rendu identique en Typst (PDF) et en HTML, aucune police requise.
Pas de gris : noir + couleurs franches. Fond blanc (lisible en mode sombre du site).
Chaque figure est dessinée à l'échelle 1 : on l'insère avec sa largeur naturelle (cm),
donc le texte a la même taille dans toutes les figures."""
import math, os, json
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch, Circle
from matplotlib import patheffects

# Latin Modern (paquet Debian « fonts-lmodern » ou TeX Live) ; sinon police serif par défaut.
for LM in ("/usr/share/texmf/fonts/opentype/public/lm/", "/usr/share/texlive/texmf-dist/fonts/opentype/public/lm/"):
    for f_ in ("lmroman10-regular.otf", "lmroman10-italic.otf", "lmroman10-bold.otf"):
        if os.path.exists(LM + f_):
            font_manager.fontManager.addfont(LM + f_)
plt.rcParams.update({
    "mathtext.fontset": "cm", "svg.fonttype": "path", "font.family": "serif",
    "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s04", "lines.scale_dashes": False,
})

OUT = os.path.dirname(os.path.abspath(__file__))   # les SVG sont écrits à côté de ce script
os.makedirs(OUT, exist_ok=True)
SIZES = {}

BLUE, RED, GREEN, PURPLE, ORANGE, BLACK = "#1f5fbf", "#c0392b", "#2e7d46", "#7b3fa0", "#c76e00", "#000000"
FILL_B, FILL_S = "#e6efff", "#fbe9d7"
PT = 0.75  # 1 px (96 dpi) = 0.75 pt


class Fig:
    def __init__(self, xmin, xmax, ymin, ymax, unit=40, margin=16):
        self.xmin, self.xmax, self.ymin, self.ymax, self.u = xmin, xmax, ymin, ymax, unit
        mu = margin / unit
        W = (xmax - xmin) * unit + 2 * margin
        H = (ymax - ymin) * unit + 2 * margin
        self.fig = plt.figure(figsize=(W / 96, H / 96))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(xmin - mu, xmax + mu); self.ax.set_ylim(ymin - mu, ymax + mu)
        self.ax.set_aspect("equal"); self.ax.axis("off")
        self.Wcm = W / 96 * 2.54
        self.z = 1

    def _z(self):
        self.z += 1
        return self.z

    def line(self, a, b, color=BLACK, w=1.2, dash=None):
        ls = (0, tuple(x * PT for x in dash)) if dash else "-"
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=w * PT, ls=ls,
                     solid_capstyle="round", dash_capstyle="butt", zorder=self._z())

    def arrow(self, a, b, color=BLUE, w=2.2, head=11, dash=None):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if L == 0:
            return
        h = head / self.u
        ux, uy = dx / L, dy / L
        bx, by = b[0] - ux * h * 0.9, b[1] - uy * h * 0.9
        self.line(a, (bx, by), color, w, dash)
        px, py = -uy, ux
        hw = h * 0.38
        self.ax.add_patch(Polygon([b, (b[0] - ux * h + px * hw, b[1] - uy * h + py * hw),
                                   (b[0] - ux * h * 0.78, b[1] - uy * h * 0.78),
                                   (b[0] - ux * h - px * hw, b[1] - uy * h - py * hw)],
                                  closed=True, fc=color, ec=color, lw=0.4, zorder=self._z()))

    def poly(self, pts, fill="none", stroke=BLACK, w=1.0, dash=None):
        ls = (0, tuple(x * PT for x in dash)) if dash else "-"
        self.ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=stroke, lw=w * PT, ls=ls, zorder=self._z()))

    def rect(self, x, y, w_, h_, fill=FILL_B, r=0.12):
        self.ax.add_patch(FancyBboxPatch((x, y), w_, h_, boxstyle=f"round,pad=0,rounding_size={r}",
                                         fc=fill, ec=BLACK, lw=1.1 * PT, zorder=self._z()))

    def dot(self, p, color=BLACK, r=3.2):
        self.ax.add_patch(Circle(p, r / self.u, fc=color, ec="none", zorder=self._z() + 50))

    def text(self, p, s, color=BLACK, size=15, dx=0, dy=0, ha="center", va="center"):
        # dx, dy en pixels (dy positif = vers le HAUT)
        self.ax.annotate(s, p, xytext=(dx * PT, dy * PT), textcoords="offset points",
                         ha=ha, va=va, color=color, fontsize=size * PT, zorder=200,
                         path_effects=[patheffects.withStroke(linewidth=3, foreground="white")])  # halo blanc : lisible sur la grille

    def vlabel(self, p, name, color=BLUE, size=18, dx=0, dy=0, sub=None):
        s = r"$\vec{%s}%s$" % (name, ("_{%s}" % sub) if sub else "")
        self.text(p, s, color, size, dx, dy)

    def grid(self):
        for x in range(math.ceil(self.xmin), math.floor(self.xmax) + 1):
            self.line((x, self.ymin), (x, self.ymax), BLACK, 0.45, (1, 3))
        for y in range(math.ceil(self.ymin), math.floor(self.ymax) + 1):
            self.line((self.xmin, y), (self.xmax, y), BLACK, 0.45, (1, 3))

    def axes(self, labels=("x", "y"), ticks=True):
        self.arrow((self.xmin, 0), (self.xmax, 0), BLACK, 1.1, 9)
        self.arrow((0, self.ymin), (0, self.ymax), BLACK, 1.1, 9)
        self.text((self.xmax, 0), f"${labels[0]}$", size=16, dx=-6, dy=-13)
        self.text((0, self.ymax), f"${labels[1]}$", size=16, dx=12, dy=-6)
        if ticks:
            for x in range(math.ceil(self.xmin), math.floor(self.xmax)):
                if x != 0:
                    self.text((x, 0), f"${x}$", size=12, dy=-11)
            for y in range(math.ceil(self.ymin), math.floor(self.ymax)):
                if y != 0:
                    self.text((0, y), f"${y}$", size=12, dx=-10)
            self.text((0, 0), "$0$", size=12, dx=-9, dy=-10)

    def arc(self, c, r, a0, a1, color=BLACK, w=1.0, label=None, lr=None, size=14):
        ts = [math.radians(a0 + (a1 - a0) * i / 60) for i in range(61)]
        self.ax.plot([c[0] + r * math.cos(t) for t in ts], [c[1] + r * math.sin(t) for t in ts],
                     color=color, lw=w * PT, zorder=self._z())
        if label:
            t = math.radians((a0 + a1) / 2)
            rr = lr or r + 0.45
            self.text((c[0] + rr * math.cos(t), c[1] + rr * math.sin(t)), label, color, size)

    def right_angle(self, c, d1, d2, s=0.25, color=BLACK):
        n1, n2 = math.hypot(*d1), math.hypot(*d2)
        a = (c[0] + s * d1[0] / n1, c[1] + s * d1[1] / n1)
        e = (c[0] + s * d2[0] / n2, c[1] + s * d2[1] / n2)
        b = (a[0] + e[0] - c[0], a[1] + e[1] - c[1])
        self.line(a, b, color, 0.9); self.line(b, e, color, 0.9)

    def save(self, name):
        self.fig.savefig(os.path.join(OUT, name), facecolor="white", metadata={"Date": None})
        plt.close(self.fig)
        SIZES[name] = round(self.Wcm, 1)


def mid(a, b, off, side=1):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    return ((a[0] + b[0]) / 2 - dy / L * off * side, (a[1] + b[1]) / 2 + dx / L * off * side)


# =====================================================================
# SOCLE
# =====================================================================

# S.1 — flèches
f = Fig(0, 13, 0, 6, unit=36)
f.grid()
arrows = {"a": ((1, 1), (4, 2)), "b": ((6, 3), (9, 4)), "c": ((9, 1), (6, 0)),
          "d": ((1, 3), (7, 5)), "e": ((11, 1), (11, 4)), "f": ((13, 6), (10, 5))}
for k, (a, b) in arrows.items():
    f.arrow(a, b, BLUE)
    side = -1 if k == "e" else 1
    f.vlabel(mid(a, b, 0.45, side), k, BLUE)
f.save("s-fleches.svg")

# S.2 — opérations graphiques : énoncé
f = Fig(0, 13, 0, 7, unit=36)
f.grid()
f.arrow((1, 5), (4, 6), BLUE); f.vlabel(mid((1, 5), (4, 6), 0.45), "u", BLUE)
f.arrow((1, 1), (2, 3), RED); f.vlabel(mid((1, 1), (2, 3), 0.45), "v", RED)
f.dot((6, 3)); f.text((6, 3), "$O$", size=16, dx=-10, dy=-11)
f.save("s-operations.svg")

# S.2 — opérations graphiques : solution (3 panneaux)
f = Fig(0, 21, -2, 5, unit=30)
f.grid()
O = (1, 1)
f.arrow(O, (2, 3), RED, 1.4, 9, dash=(5, 4)); f.arrow((2, 3), (5, 4), BLUE, 1.4, 9, dash=(5, 4))
f.arrow(O, (4, 2), BLUE); f.vlabel(mid(O, (4, 2), 0.42, -1), "u", BLUE, 16)
f.arrow((4, 2), (5, 4), RED); f.vlabel(mid((4, 2), (5, 4), 0.42, -1), "v", RED, 16)
f.arrow(O, (5, 4), GREEN, 2.6); f.text((5.25, 4.25), r"$\vec u+\vec v$", GREEN, 16, ha="left")
f.dot(O); f.text(O, "$O$", size=15, dx=-10, dy=-9)
O = (8, 1)
f.arrow(O, (11, 2), BLUE); f.vlabel(mid(O, (11, 2), 0.42), "u", BLUE, 16)
f.arrow((11, 2), (10, 0), RED); f.text(mid((11, 2), (10, 0), 0.5, -1), r"$-\vec v$", RED, 16)
f.arrow(O, (10, 0), GREEN, 2.6); f.text(mid(O, (10, 0), 0.55, -1), r"$\vec u-\vec v$", GREEN, 16)
f.dot(O); f.text(O, "$O$", size=15, dx=-10, dy=8)
O = (15, 1)
f.arrow(O, (21, 3), BLUE); f.text(mid(O, (21, 3), 0.45), r"$2\vec u$", BLUE, 16)
f.arrow(O, (14, -1), RED); f.text(mid(O, (14, -1), 0.5), r"$-\vec v$", RED, 16)
f.dot(O); f.text(O, "$O$", size=15, dx=10, dy=-9)
for x, s in [(3, r"(1)  $\vec u+\vec v$"), (10, r"(2)  $\vec u-\vec v$"), (18, r"(3)  $2\vec u$  et  $-\vec v$")]:
    f.text((x, -1.5), s, size=15)
f.save("s-operations-sol.svg")

# S.3 — points et vecteurs dans un repère
f = Fig(-4, 5, -3, 6, unit=36)
f.grid(); f.axes()
A, B, C = (-2, 1), (2, 4), (2, -2)
f.arrow(A, B, BLUE); f.arrow(B, C, RED); f.arrow(A, C, GREEN)
for p, n, dx, dy in [(A, "A", -12, 8), (B, "B", 11, 8), (C, "C", 12, -8)]:
    f.dot(p); f.text(p, f"${n}$", size=17, dx=dx, dy=dy)
f.save("s-points.svg")

# S.4 — composantes : norme et angle
f = Fig(-6, 4, -1, 5, unit=38)
f.grid(); f.axes()
a = (4 * math.cos(math.radians(60)), 4 * math.sin(math.radians(60)))
b = (6 * math.cos(math.radians(150)), 6 * math.sin(math.radians(150)))
f.arrow((0, 0), a, BLUE, 2.4); f.vlabel((a[0] + 0.4, a[1] - 0.2), "u", BLUE)
f.arrow((0, 0), b, RED, 2.4); f.vlabel((b[0] - 0.1, b[1] + 0.45), "v", RED)
f.arc((0, 0), 0.9, 0, 60, BLUE, label="60°", lr=1.35)
f.arc((0, 0), 1.6, 0, 150, RED); f.text((-0.75, 1.95), "150°", RED, 14)
f.text((1.75, 1.75), r"$\Vert\vec u\Vert=4$", BLUE, 15, ha="left")
f.text(mid((0, 0), b, 0.75, -1), r"$\Vert\vec v\Vert=6$", RED, 15)
f.save("s-composantes.svg")


class Fig3(Fig):
    K, ALPHA = 0.55, math.radians(35)

    def p3(self, x, y, z):
        return (y - self.K * x * math.cos(self.ALPHA), z - self.K * x * math.sin(self.ALPHA))

    def line3(self, a, b, **kw): self.line(self.p3(*a), self.p3(*b), **kw)
    def arrow3(self, a, b, color=BLUE, **kw): self.arrow(self.p3(*a), self.p3(*b), color, **kw)

    def axes3(self, lx, ly, lz):
        o = (0, 0, 0)
        for e in [(lx, 0, 0), (0, ly, 0), (0, 0, lz)]:
            self.arrow3(o, e, BLACK, w=1.1, head=9)
        self.text(self.p3(lx, 0, 0), "$x$", size=16, dx=-8, dy=-10)
        self.text(self.p3(0, ly, 0), "$y$", size=16, dx=4, dy=-12)
        self.text(self.p3(0, 0, lz), "$z$", size=16, dx=12, dy=-4)


# S.5 — norme dans R^3 : P = (2, 4, 4)
f = Fig3(-2.2, 5.6, -2.2, 5.0, unit=44)
f.axes3(3.4, 5.4, 4.9)
P, Pp = (2, 4, 4), (2, 4, 0)
for a, b in [((2, 0, 0), (2, 4, 0)), ((0, 4, 0), (2, 4, 0)), ((2, 4, 0), (2, 4, 4)),
             ((0, 0, 4), (2, 0, 4)), ((0, 0, 4), (0, 4, 4)), ((2, 0, 4), (2, 4, 4)),
             ((0, 4, 4), (2, 4, 4)), ((2, 0, 0), (2, 0, 4)), ((0, 4, 0), (0, 4, 4))]:
    f.line3(a, b, color=BLACK, w=0.8, dash=(4, 3))
f.line3((0, 0, 0), Pp, color=GREEN, w=2.2)
f.line3(Pp, P, color=PURPLE, w=2.2)
f.arrow3((0, 0, 0), P, BLUE, w=2.4)
o2, pp2 = f.p3(0, 0, 0), f.p3(*Pp)
f.right_angle(pp2, (o2[0] - pp2[0], o2[1] - pp2[1]), (0, 1), s=0.28)
f.dot(f.p3(*P)); f.text(f.p3(*P), "$P$", size=17, dx=12, dy=8)
f.dot(pp2); f.text(pp2, "$P'$", size=17, dx=14, dy=-10)
f.text(o2, "$O$", size=16, dx=-12, dy=-4)
f.text(f.p3(2, 0, 0), "$2$", size=13, dx=-9, dy=-7)
f.text(f.p3(0, 4, 0), "$4$", size=13, dx=5, dy=-11)
f.text(f.p3(0, 0, 4), "$4$", size=13, dx=-10)
f.save("s-r3.svg")

# S.6 — signe du produit scalaire
f = Fig(0, 16, -1, 4, unit=34)
f.grid()
for O, u, v, lab in [((1, 0), (3, 1), (1, 2), "(1)"), ((7, 0), (2, 1), (-1, 2), "(2)"), ((12, 1), (3, 0), (-2, 2), "(3)")]:
    U, V = (O[0] + u[0], O[1] + u[1]), (O[0] + v[0], O[1] + v[1])
    f.arrow(O, U, BLUE); f.arrow(O, V, RED)
    f.vlabel(mid(O, U, 0.4, -1), "u", BLUE, 16)
    f.vlabel(mid(O, V, 0.4, 1), "v", RED, 16)
    f.dot(O)
    f.text((O[0] + 1, -0.6), lab, size=15)
f.save("s-signe-ps.svg")

# S.7 — projection
f = Fig(-1, 6, -1, 4, unit=42)
f.grid(); f.axes()
f.line((-0.6, -0.3), (5.8, 2.9), BLUE, 0.9, (6, 4))
f.arrow((0, 0), (4, 2), BLUE, 2.4); f.vlabel((4.25, 1.6), "u", BLUE)
f.arrow((0, 0), (1, 3), RED, 2.4); f.vlabel((0.55, 3.15), "v", RED)
f.line((1, 3), (2, 1), BLACK, 1.1, (4, 3))
f.right_angle((2, 1), (-1, -0.5), (-1, 2), s=0.22)
f.dot((2, 1)); f.text((2, 1), "$H$", size=16, dx=10, dy=-11)
f.save("s-projection.svg")

# S.8 — produit vectoriel : u = (3,0,0), v = (1,2,0), u × v = (0,0,6)
class Fig3b(Fig3):
    K, ALPHA = 0.7, math.radians(30)


def vectoriel(sol):
    top = 6.6 if sol else 3.2   # énoncé : axe des z court (la réponse n'y est pas)
    f = Fig3b(-2.6, 4.2, -1.9, top, unit=38)
    f.axes3(3.9, 3.9, top - 0.1)
    u, v, w = (3, 0, 0), (1, 2, 0), (4, 2, 0)
    f.poly([f.p3(0, 0, 0), f.p3(*u), f.p3(*w), f.p3(*v)], fill=FILL_B, stroke=BLUE, w=0.8, dash=(4, 3))
    f.arrow3((0, 0, 0), u, BLUE, w=2.4); f.arrow3((0, 0, 0), v, RED, w=2.4)
    if sol:
        f.arrow3((0, 0, 0), (0, 0, 6), GREEN, w=2.8)
        f.text((f.p3(0, 0, 6)[0] + 0.25, f.p3(0, 0, 6)[1] - 0.2), r"$\vec u\times\vec v$", GREEN, 17, ha="left")
    f.vlabel((f.p3(*u)[0] + 0.1, f.p3(*u)[1] + 0.45), "u", BLUE)
    f.vlabel((f.p3(*v)[0] + 0.35, f.p3(*v)[1] + 0.35), "v", RED)
    f.text(f.p3(0, 0, 0), "$O$", size=16, dx=-12, dy=4)
    f.save("s-vectoriel-sol.svg" if sol else "s-vectoriel.svg")


vectoriel(False); vectoriel(True)

# =====================================================================
# TRANSFERT
# =====================================================================

def traction(sol):
    f = Fig(-1, 9, -3.0, 3.0, unit=40)
    f.poly([(-1, 0.35), (0.95, 0.35), (0.95, -0.35), (-1, -0.35)], fill=FILL_S, stroke=BLACK, w=1)
    f.text((-0.05, 0), "pied", size=14)
    Pt, L = (1.2, 0), 4
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    a, b = (Pt[0] + L * c30, L * s30), (Pt[0] + L * c30, -L * s30)
    t = math.tan(math.radians(30))
    f.line(Pt, (8.8, (8.8 - Pt[0]) * t), BLACK, 0.9, (4, 4))
    f.line(Pt, (8.8, -(8.8 - Pt[0]) * t), BLACK, 0.9, (4, 4))
    f.line(Pt, (8.8, 0), BLACK, 0.8, (1, 4))
    f.arrow(Pt, a, BLUE, 2.4); f.arrow(Pt, b, RED, 2.4)
    f.vlabel(mid(Pt, a, 0.45), "F", BLUE, sub="1")
    f.vlabel(mid(Pt, b, 0.45, -1), "F", RED, sub="2")
    f.arc(Pt, 1.3, 0, 30, label="30°", lr=1.85)
    f.arc(Pt, 1.3, -30, 0, label="30°", lr=1.85)
    f.dot(Pt, r=4.5)
    if sol:
        R = (Pt[0] + 2 * L * c30, 0)
        f.line(a, R, RED, 1.2, (5, 4)); f.line(b, R, BLUE, 1.2, (5, 4))
        f.arrow(Pt, R, GREEN, 2.8)
        f.vlabel((R[0] - 0.55, 0.38), "R", GREEN)
    f.save("t-traction-sol.svg" if sol else "t-traction.svg")


traction(False); traction(True)


def perf(sol):
    f = Fig(-4.5, 4.5, -3.0, 2.6, unit=38)
    f.line((-4.2, 2), (4.2, 2), BLACK, 2.2)
    for i in range(17):
        x = -4 + 0.5 * i
        f.line((x, 2), (x + 0.3, 2.3), BLACK, 0.8)
    t = math.tan(math.radians(30))
    N = (0, 0)
    f.line((-2 / t, 2), N, BLACK, 1.4); f.line((2 / t, 2), N, BLACK, 1.4)
    f.arc((-2 / t, 2), 1.1, -30, 0, label="30°", lr=1.65)
    f.arc((2 / t, 2), 1.1, 180, 210, label="30°", lr=1.65)
    f.line(N, (0, -0.9), BLACK, 1.2)
    f.rect(-0.55, -2.4, 1.1, 1.5)
    f.text((-0.7, -1.65), "poche", size=13, ha="right")
    f.dot(N, r=4)
    if sol:
        L = 2.0
        f.arrow(N, (-L * math.cos(math.radians(30)), L * math.sin(math.radians(30))), BLUE, 2.6)
        f.arrow(N, (L * math.cos(math.radians(30)), L * math.sin(math.radians(30))), RED, 2.6)
        f.arrow(N, (0, -2.0), GREEN, 2.6)
        f.vlabel((-1.6, 0.35), "T", BLUE, sub="1"); f.vlabel((1.6, 0.35), "T", RED, sub="2")
        f.vlabel((0.5, -2.7), "P", GREEN)
    f.save("t-perfusion-sol.svg" if sol else "t-perfusion.svg")


perf(False); perf(True)


def travail(sol):
    f = Fig(-0.8, 11, -3.6, 1.6, unit=36)
    f.line((-0.8, -1.3), (11, -1.3), BLACK, 1.6)
    f.rect(0, 0, 3, 0.55)
    for x in (0.5, 2.5):
        f.line((x, 0), (x, -0.95), BLACK, 1.2)
        f.ax.add_patch(Circle((x, -1.1), 0.19, fc="white", ec=BLACK, lw=1.1 * PT, zorder=f._z()))
    f.text((1.5, 0.28), "brancard", size=13)
    A = (3, 0.28)
    F = (A[0] + 3.2 * math.cos(math.radians(-60)), A[1] + 3.2 * math.sin(math.radians(-60)))
    f.line(A, (7, A[1]), BLACK, 0.8, (2, 4))
    f.arrow(A, F, BLUE, 2.4); f.vlabel((F[0] + 0.45, F[1] + 0.25), "F", BLUE)
    f.arc(A, 1.0, -60, 0, label="60°", lr=1.45)
    f.arrow((5, -2.8), (10.5, -2.8), RED, 2.2); f.vlabel((7.75, -2.35), "d", RED)
    f.text((7.75, -3.3), r"$10\ \mathrm{m}$", RED, 14)
    if sol:
        H = (F[0], A[1])
        f.arrow(A, H, GREEN, 2.6); f.arrow(H, F, PURPLE, 1.8, 9, dash=(5, 3))
        f.right_angle(H, (-1, 0), (0, -1), s=0.25)
    f.save("t-travail-sol.svg" if sol else "t-travail.svg")


travail(False); travail(True)


def riviere(sol):
    f = Fig(-1, 17, -0.9, 5.9, unit=32)
    f.ax.add_patch(Rectangle((-1, 0), 18, 5, fc=FILL_B, ec="none", zorder=0))
    f.line((-1, 0), (17, 0), BLACK, 1.8); f.line((-1, 5), (17, 5), BLACK, 1.8)
    for x in (4, 8, 12):
        f.arrow((x, 4.3), (x + 1.8, 4.3), BLACK, 1.1, 8)
    f.text((15.3, 4.3), "courant", size=13)
    S = (1, 0)
    f.arrow(S, (1, 2.4), BLUE, 2.4); f.text((0.75, 1.5), "nage", BLUE, 13, ha="right")
    f.arrow(S, (2.8, 0), RED, 2.4); f.text((2.2, -0.45), "courant", RED, 13)
    f.dot(S, r=4); f.text(S, "départ", size=13, dx=-6, dy=-14, ha="right")
    f.line((-0.3, 0), (-0.3, 5), BLACK, 0.9)
    f.line((-0.45, 0), (-0.15, 0), BLACK, 0.9); f.line((-0.45, 5), (-0.15, 5), BLACK, 0.9)
    f.text((-0.5, 2.9), r"$20\ \mathrm{m}$", size=13, ha="right")
    if sol:
        f.line((1, 2.4), (2.8, 2.4), RED, 1, (4, 3)); f.line((2.8, 0), (2.8, 2.4), BLUE, 1, (4, 3))
        f.line((2.8, 2.4), (1 + 3.75, 5), GREEN, 1.2, (6, 4))
        f.arrow(S, (2.8, 2.4), GREEN, 2.8)
        f.dot((4.75, 5), GREEN, 4); f.text((4.75, 5), "arrivée", GREEN, 13, dy=12)
        f.line((1, 5), (4.75, 5), BLACK, 1.2, (2, 3)); f.text((2.9, 5), r"$15\ \mathrm{m}$", size=13, dy=12)
    f.save("t-riviere-sol.svg" if sol else "t-riviere.svg")


riviere(False); riviere(True)

# T — biceps
f = Fig(-1.8, 9, -3.4, 4.2, unit=36)
f.poly([(-0.5, 4), (0.5, 4), (0.5, 0.4), (-0.5, 0.4)], fill=FILL_S, stroke=BLACK, w=1)
f.poly([(0, 0.4), (7.6, 0.3), (7.6, -0.3), (0, -0.4)], fill=FILL_S, stroke=BLACK, w=1)
f.dot((0, 0), r=4.5); f.text((0, 0), "$O$", size=16, dx=-13, dy=-9)
f.text((-0.6, 0.9), "coude", size=13, ha="right")
f.arrow((1, 0.35), (1, 3.3), RED, 2.4); f.vlabel((1.5, 2.3), "B", RED)
f.text((1.25, 3.6), "biceps", size=13, ha="left")
f.line((7.2, -0.3), (7.2, -0.9), BLACK, 1.0)
f.rect(6.6, -1.7, 1.2, 0.8)
f.arrow((7.2, -1.9), (7.2, -3.2), BLUE, 2.4); f.vlabel((7.75, -2.6), "P", BLUE)
f.line((0, -1.05), (1, -1.05), BLACK, 0.9); f.text((0.5, -1.05), r"$4\ \mathrm{cm}$", size=13, dy=-11)
f.line((0, -2.35), (7.2, -2.35), BLACK, 0.9); f.text((3.6, -2.35), r"$30\ \mathrm{cm}$", size=13, dy=-11)
for x, y in [(0, -1.05), (1, -1.05), (0, -2.35), (7.2, -2.35)]:
    f.line((x, y - 0.12), (x, y + 0.12), BLACK, 0.9)
f.save("t-biceps.svg")

# =====================================================================
# RENFORCEMENT
# =====================================================================
f = Fig(0, 12, 0, 6, unit=34)
f.grid()
O = (1, 2)
f.arrow(O, (2, 3), BLUE); f.vlabel(mid(O, (2, 3), 0.4), "u", BLUE, 17)
f.arrow(O, (3, 1), RED); f.vlabel(mid(O, (3, 1), 0.4, -1), "v", RED, 17)
f.arrow((5, 1), (8, 1), GREEN); f.vlabel(mid((5, 1), (8, 1), 0.4), "a", GREEN, 17)
f.arrow((6, 2), (6, 5), PURPLE); f.vlabel(mid((6, 2), (6, 5), 0.4), "b", PURPLE, 17)
f.arrow((8, 3), (12, 4), ORANGE); f.vlabel(mid((8, 3), (12, 4), 0.4), "c", ORANGE, 17)
f.dot(O)
f.save("r-decomposer.svg")



# =====================================================================
# PRODUIT VECTORIEL — dessins pour choisir le SENS (règle de la main droite)
# Vue « du dessus » du plan de u et v (côté où pointe u × v), légèrement inclinée :
# de u vers v, la flèche courbe tourne dans le sens inverse des aiguilles d'une montre,
# et u × v monte. Projection orthographique dans le repère (e1, e2, n) du plan.
# =====================================================================
def _norm(a): return math.sqrt(sum(x * x for x in a))
def _unit(a): n = _norm(a); return tuple(x / n for x in a)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def main_droite(u, v, name, lab_w, lab_mw, phi=-15, alpha=24, unit=46, box=None, axes_at=None,
                arc_r=1.0, outdir=OUT, wlen=2.6, axlen=2.2):
    w = _cross(u, v)
    e1 = _unit(u); n = _unit(w); e2 = _cross(n, e1)
    ph, al = math.radians(phi), math.radians(alpha)

    def P(p):
        a, b, h = _dot(p, e1), _dot(p, e2), _dot(p, n)
        x = a * math.cos(ph) - b * math.sin(ph)
        d = a * math.sin(ph) + b * math.cos(ph)
        return (x, d * math.sin(al) + h * math.cos(al))

    f = Fig(*box, unit=unit)
    O = (0, 0, 0)
    # repère : axes x, y, z depuis l'origine (partie négative en pointillés)
    for e, lab in [((1, 0, 0), "x"), ((0, 1, 0), "y"), ((0, 0, 1), "z")]:
        neg = P(tuple(-axlen * 0.6 * c for c in e)); pos = P(tuple(axlen * c for c in e))
        f.line(neg, P(O), BLACK, 0.8, (2, 3))
        f.arrow(P(O), pos, BLACK, 1.0, 8)
        f.text(pos, f"${lab}$", size=15, dx=9 if pos[0] >= 0 else -9, dy=6)
    # parallélogramme
    f.poly([P(O), P(u), P(tuple(x + y for x, y in zip(u, v))), P(v)], fill=FILL_B, stroke=BLUE, w=0.8, dash=(4, 3))
    # -w (en pointillés, sous le plan) puis w
    w = tuple(wlen * x for x in _unit(w))   # longueur d'affichage (le sens seul compte ici)
    mw = tuple(-x for x in w)
    f.arrow(P(O), P(mw), BLACK, 1.6, 11, dash=(5, 4))
    f.arrow(P(O), P(u), BLUE, 2.6, 13)
    f.arrow(P(O), P(v), RED, 2.6, 13)
    # flèche courbe de u vers v (plus petit angle), dans le plan
    th = math.acos(_dot(u, v) / (_norm(u) * _norm(v)))
    pts = [P(tuple(arc_r * (math.cos(t) * a + math.sin(t) * b) for a, b in zip(e1, e2)))
           for t in [th * k / 40 for k in range(41)]]
    f.ax.plot([p[0] for p in pts[:-3]], [p[1] for p in pts[:-3]], color=GREEN, lw=1.8 * PT, zorder=f._z())
    f.arrow(pts[-6], pts[-1], GREEN, 1.8, 10)
    f.arrow(P(O), P(w), GREEN, 2.8, 14)
    f.dot(P(O))
    f.vlabel((P(u)[0] + 0.35, P(u)[1] - 0.05), "u", BLUE, 20)
    f.vlabel((P(v)[0] - 0.05, P(v)[1] + 0.4), "v", RED, 20)
    f.text(P(w), lab_w, GREEN, 15, dx=10, dy=4, ha="left")
    f.text(P(mw), lab_mw, BLACK, 15, dx=10, dy=-2, ha="left")
    # petit trièdre des axes, pour situer la vue
    if axes_at:
        for e, lab in [((1, 0, 0), "x"), ((0, 1, 0), "y"), ((0, 0, 1), "z")]:
            q = P(tuple(0.9 * c for c in e))
            end = (axes_at[0] + q[0], axes_at[1] + q[1])
            f.arrow(axes_at, end, BLACK, 1.0, 7)
            f.text(end, f"${lab}$", size=13, dx=7 * (1 if q[0] >= 0 else -1), dy=5)
    f.save(name) if outdir == OUT else _save_to(f, name, outdir)
    return f


def _save_to(f, name, outdir):
    os.makedirs(outdir, exist_ok=True)
    f.fig.savefig(os.path.join(outdir, name), facecolor="white", metadata={"Date": None})
    plt.close(f.fig)
    SIZES[name] = round(f.Wcm, 1)


def main_droite_cav(u, v, name, lab_w, lab_mw, box, unit=40, wlen=2.6, ax=(3.2, 3.2, 3.2),
                    arc_r=1.0, outdir=OUT, lab_off=None, cls=None):
    """Dessin dans le repère habituel (projection cavalière : x vers toi, y à droite, z en haut)."""
    f = (cls or Fig3b)(*box, unit=unit)
    f.axes3(*ax)
    O = (0, 0, 0)
    w = _cross(u, v); w = tuple(wlen * x for x in _unit(w)); mw = tuple(-x for x in w)
    s_uv = tuple(x + y for x, y in zip(u, v))
    f.poly([f.p3(*O), f.p3(*u), f.p3(*s_uv), f.p3(*v)], fill=FILL_B, stroke=BLUE, w=0.8, dash=(4, 3))
    f.arrow3(O, mw, BLACK, w=1.6, head=11, dash=(5, 4))
    f.arrow3(O, u, BLUE, w=2.6, head=13); f.arrow3(O, v, RED, w=2.6, head=13)
    e1 = _unit(u); n = _unit(_cross(u, v)); e2 = _cross(n, e1)
    th = math.acos(_dot(u, v) / (_norm(u) * _norm(v)))
    pts = [f.p3(*tuple(arc_r * (math.cos(t) * a + math.sin(t) * b) for a, b in zip(e1, e2)))
           for t in [th * k / 40 for k in range(41)]]
    f.ax.plot([p[0] for p in pts[:-3]], [p[1] for p in pts[:-3]], color=GREEN, lw=1.8 * PT, zorder=f._z())
    f.arrow(pts[-6], pts[-1], GREEN, 1.8, 10)
    f.arrow3(O, w, GREEN, w=2.8, head=14)
    f.dot(f.p3(*O))
    lo = lab_off or {}
    pu, pv, pw, pm = f.p3(*u), f.p3(*v), f.p3(*w), f.p3(*mw)
    f.vlabel((pu[0] + lo.get("u", (0.3, 0))[0], pu[1] + lo.get("u", (0.3, 0))[1]), "u", BLUE, 19)
    f.vlabel((pv[0] + lo.get("v", (0.3, 0.3))[0], pv[1] + lo.get("v", (0.3, 0.3))[1]), "v", RED, 19)
    f.text(pw, lab_w, GREEN, 14, dx=8, dy=6, ha="left")
    if lo.get("mw_left"):
        f.text(pm, lab_mw, BLACK, 14, dx=-8, dy=-2, ha="right")
    else:
        f.text(pm, lab_mw, BLACK, 14, dx=8, dy=-4, ha="left")
    if outdir == OUT: f.save(name)
    else: _save_to(f, name, outdir)


class Fig3c(Fig3):
    K, ALPHA = 0.7, math.radians(20)


# Transfert : u = (1, 1, -1), v = (0, 2, -1), u × v = (1, 1, 2).
# u et v pointent sous le plan (x, y) ; de u vers v, la flèche courbe tourne dans le sens inverse
# des aiguilles d'une montre : le pouce monte, vers les z positifs.
main_droite_cav((1, 1, -1), (0, 2, -1), "t-main-droite.svg", r"$(1,\,1,\,2)$", r"$(-1,\,-1,\,-2)$",
                box=(-2.8, 3.9, -2.6, 3.6), unit=44, wlen=2.6, ax=(2.8, 3.2, 3.2), arc_r=0.85,
                lab_off={"u": (0.35, -0.15), "v": (0.3, 0.3), "mw_left": True})

# Fiche de méthode : u = (3, 0, 0), v = (1, 2, 0), u × v = (0, 0, 6)  -> seances/methodes/img/
main_droite_cav((3, 0, 0), (1, 2, 0), "m-vectoriel.svg", r"$(0,\,0,\,6)$", r"$(0,\,0,\,-6)$",
                box=(-2.6, 3.6, -3.0, 3.6), unit=40, wlen=2.6, ax=(3.6, 3.2, 3.2), arc_r=0.9,
                outdir=os.path.join(OUT, "..", "..", "methodes", "img"),
                lab_off={"u": (-0.35, -0.3), "v": (0.25, 0.35)})

# =====================================================================
# FICHES DE MÉTHODE — figures des exemples (-> seances/methodes/img/)
# =====================================================================
MDIR = os.path.join(OUT, "..", "..", "methodes", "img")


def _msave(f, name):
    _save_to(f, name, MDIR)


# Additionner et soustraire sur un dessin : u = (3, 1), v = (1, 2)
f = Fig(0, 12.5, -1.6, 4.4, unit=30)
f.grid()
O = (0.5, 0.5)
f.arrow(O, (3.5, 1.5), BLUE); f.vlabel(mid(O, (3.5, 1.5), 0.42, -1), "u", BLUE, 16)
f.arrow((3.5, 1.5), (4.5, 3.5), RED); f.vlabel(mid((3.5, 1.5), (4.5, 3.5), 0.42, -1), "v", RED, 16)
f.arrow(O, (4.5, 3.5), GREEN, 2.6); f.text((2.4, 3.9), r"$\vec u+\vec v=(4,3)$", GREEN, 15)
f.dot(O)
O = (7, 1.5)
f.arrow(O, (10, 2.5), BLUE); f.vlabel(mid(O, (10, 2.5), 0.42), "u", BLUE, 16)
f.arrow((10, 2.5), (9, 0.5), RED); f.text(mid((10, 2.5), (9, 0.5), 0.5, -1), r"$-\vec v$", RED, 16)
f.arrow(O, (9, 0.5), GREEN, 2.6); f.text((8.2, -0.7), r"$\vec u-\vec v=(2,-1)$", GREEN, 15)
f.dot(O)
_msave(f, "m-somme.svg")

# Norme et angle -> coordonnées : 8 N à 150°
f = Fig(-8, 1.6, -1, 5.2, unit=30)
f.grid(); f.axes(ticks=False)
F = (8 * math.cos(math.radians(150)), 8 * math.sin(math.radians(150)))
f.line(F, (F[0], 0), BLACK, 1.0, (4, 3)); f.line(F, (0, F[1]), BLACK, 1.0, (4, 3))
f.arrow((0, 0), F, BLUE, 2.4, 12)
f.arc((0, 0), 1.0, 0, 150, BLUE, label="150°", lr=1.55, size=14)
f.vlabel((F[0] - 0.1, F[1] + 0.55), "F", BLUE, 19)
f.text((F[0], 0), r"$-4\sqrt{3}$", size=15, dy=-14)
f.text((0, F[1]), r"$4$", size=15, dx=12)
f.text(mid((0, 0), F, 0.55, -1), r"$\Vert\vec F\Vert=8$", BLUE, 15)
_msave(f, "m-norme-coord.svg")

# Coordonnées -> norme et angle : v = (-1, -sqrt3)
S3 = math.sqrt(3)
f = Fig(-2.3, 2.3, -2.3, 1.6, unit=58)
f.grid(); f.axes(ticks=False)
V = (-1, -S3)
f.line(V, (-1, 0), BLACK, 1.0, (4, 3)); f.line(V, (0, -S3), BLACK, 1.0, (4, 3))
f.arrow((0, 0), V, RED, 2.4, 12)
f.arc((0, 0), 0.45, 0, 240, RED, label="240°", lr=0.78, size=14)
f.arc((0, 0), 0.85, 180, 240, BLACK, label="60°", lr=1.12, size=13)
f.vlabel((V[0] - 0.28, V[1] + 0.1), "v", RED, 19)
f.text((-1, 0), "$-1$", size=15, dy=13); f.text((0, -S3), r"$-\sqrt{3}$", size=15, dx=24)
_msave(f, "m-coord-norme.svg")

# Calcul en coordonnées : somme (2,-1) + (-3,4) et colinéarité (2,-6) = -2 (-1,3)
f = Fig(-3.5, 10.5, -5.0, 4.8, unit=24)
f.grid()
f.arrow((-3.5, 0), (2.6, 0), BLACK, 1.0, 8); f.arrow((0, -2.2), (0, 4.4), BLACK, 1.0, 8)
f.text((2.6, 0), "$x$", size=14, dx=-4, dy=-11); f.text((0, 4.4), "$y$", size=14, dx=9, dy=-4)
f.arrow((0, 0), (2, -1), BLUE, 2.2, 10); f.text((2, -1), r"$(2,-1)$", BLUE, 14, dx=4, dy=-10, ha="left")
f.arrow((2, -1), (-1, 3), RED, 2.2, 10); f.text(mid((2, -1), (-1, 3), 0.55, -1), r"$(-3,4)$", RED, 14, ha="left")
f.arrow((0, 0), (-1, 3), GREEN, 2.6, 11); f.text((-1, 3), r"$(-1,3)$", GREEN, 14, dx=-6, dy=8, ha="right")
f.dot((0, 0))
O2 = (6.5, 1.5)
f.line((O2[0] + 2.6, O2[1] - 7.8), (O2[0] - 1.3, O2[1] + 3.9), BLACK, 0.8, (5, 4))
f.arrow(O2, (O2[0] + 2, O2[1] - 6), ORANGE, 2.4, 11)
f.arrow(O2, (O2[0] - 1, O2[1] + 3), PURPLE, 2.4, 11)
f.text((O2[0] - 1, O2[1] + 3), r"$(-1,3)$", PURPLE, 14, dx=8, dy=-4, ha="left")
f.text((O2[0] + 2, O2[1] - 6), r"$(2,-6)$", ORANGE, 14, dx=8, dy=4, ha="left")
f.text((O2[0] + 1.5, O2[1] - 2.0), r"$=-2\,(-1,3)$", ORANGE, 13, ha="left")
f.dot(O2)
_msave(f, "m-coordonnees.svg")

# Produit scalaire : u = (sqrt3, 1), v = (0, 2), projection de longueur 1
f = Fig(-0.6, 2.4, -0.5, 2.4, unit=70)
f.grid(); f.axes(ticks=False)
U, V = (S3, 1), (0, 2)
H = (S3 / 2, 0.5)
f.line((-0.45, -0.45 / S3), (2.35, 2.35 / S3), BLUE, 0.9, (6, 4))
f.line(V, H, BLACK, 1.0, (4, 3))
f.right_angle(H, (-S3, -1), (-H[0], V[1] - H[1]), s=0.12)
f.arrow((0, 0), H, GREEN, 3.6, 11)
f.arrow((0, 0), U, BLUE, 2.4, 12); f.arrow((0, 0), V, RED, 2.4, 12)
f.arc((0, 0), 0.42, 30, 90, BLACK, label="60°", lr=0.64, size=14)
f.arc((0, 0), 0.72, 0, 30, BLUE, label="30°", lr=0.93, size=13)
f.vlabel((U[0] + 0.12, U[1] + 0.14), "u", BLUE, 19); f.vlabel((0.2, 2.05), "v", RED, 19)
f.text((0.95, 0.12), "longueur 1", GREEN, 14, ha="left")
_msave(f, "m-produit-scalaire.svg")

print("Largeurs naturelles (cm) — à reporter dans width=… :", SIZES)
