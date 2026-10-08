#!/usr/bin/env python3
"""Figures des slides de la séance 4 (même moteur que seances/_seance04/img/figs.py)."""

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

OUT = os.path.dirname(os.path.abspath(__file__))
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
# SLIDES — séance 4 (échauffement + méthodes). Même moteur que les figures de la séance.
# =====================================================================
import math as _m
S3 = math.sqrt(3)

# Échauffement Q4 : cercle trigonométrique, 120°
f = Fig(-1.5, 1.5, -1.3, 1.5, unit=120, margin=14)
t = [i * 2 * math.pi / 200 for i in range(201)]
f.ax.plot([math.cos(a) for a in t], [math.sin(a) for a in t], color=BLACK, lw=1.2 * PT)
f.arrow((-1.4, 0), (1.45, 0), BLACK, 1.1, 9); f.arrow((0, -1.25), (0, 1.45), BLACK, 1.1, 9)
P120, P60 = (-0.5, S3 / 2), (0.5, S3 / 2)
f.line((0, 0), P60, BLUE, 1.2, (4, 3)); f.line((0, 0), P120, RED, 2.0)
f.line(P120, (-0.5, 0), RED, 1.0, (3, 3)); f.line(P60, (0.5, 0), BLUE, 1.0, (3, 3))
f.dot(P120, RED, 4); f.dot(P60, BLUE, 4)
f.arc((0, 0), 0.28, 0, 120, RED); f.text((0.05, 0.42), "120°", RED, 15, ha="left")
f.text((-0.5, 0), r"$-\frac{1}{2}$", RED, 17, dy=-16); f.text((0.5, 0), r"$\frac{1}{2}$", BLUE, 17, dy=-16)
f.text(P120, r"$\left(-\frac{1}{2},\ \frac{\sqrt{3}}{2}\right)$", RED, 17, dx=-8, dy=16, ha="right")
f.text(P60, "60°", BLUE, 14, dx=10, dy=10, ha="left")
f.save("cercle-120.svg")

# Méthode 1 — vers les coordonnées : F de norme 8 à 150°
f = Fig(-8, 2, -1, 5.4, unit=46)
f.grid(); f.axes(ticks=False)
F = (8 * math.cos(math.radians(150)), 8 * math.sin(math.radians(150)))
f.line(F, (F[0], 0), BLACK, 1.1, (4, 3)); f.line(F, (0, F[1]), BLACK, 1.1, (4, 3))
f.arrow((0, 0), F, BLUE, 2.8, 14)
f.arc((0, 0), 1.0, 0, 150, BLUE, label="150°", lr=1.5, size=16)
f.vlabel((F[0] - 0.2, F[1] + 0.5), "F", BLUE, 22)
f.text((F[0], 0), r"$-4\sqrt{3}$", size=17, dy=-16)
f.text((0, F[1]), r"$4$", size=17, dx=14)
f.text(mid((0, 0), F, 0.55, -1), r"$\Vert\vec F\Vert=8$", BLUE, 17)
f.save("m1-coordonnees.svg")

# Méthode 1 — vers la norme et l'angle : v = (-1, -sqrt3)
f = Fig(-2.4, 2.4, -2.4, 1.8, unit=90)
f.grid(); f.axes(ticks=False)
V = (-1, -S3)
f.line(V, (-1, 0), BLACK, 1.1, (4, 3)); f.line(V, (0, -S3), BLACK, 1.1, (4, 3))
f.arrow((0, 0), V, RED, 2.8, 14)
f.arc((0, 0), 0.45, 0, 240, RED, label="240°", lr=0.75, size=16)
f.arc((0, 0), 0.8, 180, 240, BLACK, label="60°", lr=1.05, size=15)
f.vlabel((V[0] - 0.25, V[1] + 0.1), "v", RED, 22)
f.text((-1, 0), "$-1$", size=17, dy=14); f.text((0, -S3), r"$-\sqrt{3}$", size=17, dx=26)
f.text((-1.9, -1.9), "quadrant III", size=15, ha="left")
f.save("m1-norme-angle.svg")

# Méthode 2 — produit scalaire : u = (sqrt3, 1), v = (0, 2), projection de v sur u
f = Fig(-0.8, 2.6, -0.6, 2.5, unit=100)
f.grid(); f.axes(ticks=False)
U, V = (S3, 1), (0, 2)
H = (S3 / 2, 0.5)   # projeté de l'extrémité de v sur la droite de u (longueur 1)
f.line((-0.5, -0.5 / S3), (2.5, 2.5 / S3), BLUE, 0.9, (6, 4))
f.line(V, H, BLACK, 1.1, (4, 3))
f.right_angle(H, (-S3, -1), (-H[0], V[1] - H[1]), s=0.12)
f.arrow((0, 0), H, GREEN, 4.0, 12)
f.arrow((0, 0), U, BLUE, 2.6, 14); f.arrow((0, 0), V, RED, 2.6, 14)
f.arc((0, 0), 0.45, 30, 90, BLACK, label="60°", lr=0.68, size=16)
f.arc((0, 0), 0.75, 0, 30, BLUE, label="30°", lr=0.95, size=14)
f.vlabel((U[0] + 0.15, U[1] + 0.12), "u", BLUE, 22); f.vlabel((0.22, 2.05), "v", RED, 22)
f.text((0.95, 0.12), "longueur 1", GREEN, 15, ha="left")
f.save("m2-produit-scalaire.svg")
print(SIZES)
