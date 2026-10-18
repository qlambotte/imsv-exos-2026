#!/usr/bin/env python3
"""Figures de la séance 5 (fonctions et représentations) — usage : python3 figs.py (depuis n'importe où).
matplotlib → SVG, texte VECTORISÉ (chemins),
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
    "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s05", "lines.scale_dashes": False,
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




# =====================================================================
# Outils pour les graphes de fonctions
# =====================================================================
def num(v):
    """Nombre en mathtext, virgule décimale."""
    s = ("%g" % v).replace("-", "−")
    return "$" + s.replace(".", "{,}") + "$"


class G(Fig):
    """Repère avec échelles : le point de données (x, y) est dessiné en (x/sx, y/sy)."""
    def __init__(self, xr, yr, sx=1, sy=1, unit=40, margin=32):
        self.sx, self.sy, self.xr, self.yr = sx, sy, xr, yr
        super().__init__(xr[0] / sx, xr[1] / sx, yr[0] / sy, yr[1] / sy, unit, margin)

    def P(self, x, y):
        return (x / self.sx, y / self.sy)

    def grid_xy(self, dx, dy):
        x = math.ceil(self.xr[0] / dx - 1e-9) * dx
        while x <= self.xr[1] + 1e-9:
            self.line(self.P(x, self.yr[0]), self.P(x, self.yr[1]), BLACK, 0.45, (1, 3)); x += dx
        y = math.ceil(self.yr[0] / dy - 1e-9) * dy
        while y <= self.yr[1] + 1e-9:
            self.line(self.P(self.xr[0], y), self.P(self.xr[1], y), BLACK, 0.45, (1, 3)); y += dy

    def axes_xy(self, xt, yt, xl="x", yl="y", ox=None, oy=None, xlab=None, ylab=None):
        ox = (0 if self.xr[0] <= 0 <= self.xr[1] else self.xr[0]) if ox is None else ox
        oy = (0 if self.yr[0] <= 0 <= self.yr[1] else self.yr[0]) if oy is None else oy
        self.arrow(self.P(self.xr[0], oy), self.P(self.xr[1], oy), BLACK, 1.1, 9)
        self.arrow(self.P(ox, self.yr[0]), self.P(ox, self.yr[1]), BLACK, 1.1, 9)
        self.text(self.P(self.xr[1], oy), f"${xl}$" if xlab is None else xlab, size=16, dx=0, dy=15, ha="right")
        self.text(self.P(ox, self.yr[1]), f"${yl}$" if ylab is None else ylab, size=16, dx=8, dy=16, ha="left")
        for x in xt:
            if abs(x - ox) > 1e-9:
                self.line(self.P(x, oy), (self.P(x, oy)[0], self.P(x, oy)[1] - 4 / self.u), BLACK, 1.0)
                self.text(self.P(x, oy), num(x), size=12, dy=-14)
        for y in yt:
            if abs(y - oy) > 1e-9:
                self.line(self.P(ox, y), (self.P(ox, y)[0] - 4 / self.u, self.P(ox, y)[1]), BLACK, 1.0)
                self.text(self.P(ox, y), num(y), size=12, dx=-14)
        if ox == 0 and oy == 0 and self.xr[0] < 0 and self.yr[0] < 0:
            self.text((0, 0), "$0$", size=12, dx=-9, dy=-10)

    def curve(self, fn, x0, x1, color=BLUE, w=2.4, N=1200, breaks=()):
        xs = [x0 + (x1 - x0) * i / N for i in range(N + 1)]
        segs, cur = [], []
        for x in xs:
            try:
                y = fn(x)
            except Exception:
                y = None
            ok_ = y is not None and math.isfinite(y) and self.yr[0] - 1e-9 <= y <= self.yr[1] + 1e-9
            if ok_ and not any(abs(x - b) < (x1 - x0) / N for b in breaks):
                cur.append(self.P(x, y))
            else:
                if len(cur) > 1: segs.append(cur)
                cur = []
        if len(cur) > 1: segs.append(cur)
        for s in segs:
            self.ax.plot([p[0] for p in s], [p[1] for p in s], color=color, lw=w * PT,
                         solid_capstyle="round", zorder=self._z())

    def pt(self, x, y, label=None, color=BLACK, dx=10, dy=10, size=15, r=3.6):
        p = self.P(x, y)
        self.dot(p, color, r)
        if label:
            self.text(p, label, color, size, dx, dy)

    def hline(self, y, x0=None, x1=None, color=RED, dash=(5, 4), w=1.4):
        self.line(self.P(self.xr[0] if x0 is None else x0, y), self.P(self.xr[1] if x1 is None else x1, y), color, w, dash)

    def vline(self, x, y0=None, y1=None, color=RED, dash=(5, 4), w=1.4):
        self.line(self.P(x, self.yr[0] if y0 is None else y0), self.P(x, self.yr[1] if y1 is None else y1), color, w, dash)

    def seg(self, a, b, color=BLUE, w=2.4, dash=None):
        self.line(self.P(*a), self.P(*b), color, w, dash)

    def tx(self, x, y, s, color=BLACK, size=15, dx=0, dy=0, ha="center"):
        self.text(self.P(x, y), s, color, size, dx, dy, ha=ha)


# =====================================================================
# SOCLE
# =====================================================================

# S.1 — quatre courbes : fonction ou non ?
f = Fig(0, 15, 0, 15, unit=26)
panels = [(0.5, 8.0), (8.0, 8.0), (0.5, 0.5), (8.0, 0.5)]   # coin bas-gauche de chaque cadre (largeur 6.5)
def plane(ox, oy, curve_fn, num_label):
    cx, cy = ox + 3.25, oy + 3.25
    f.line((ox, cy), (ox + 6.5, cy), BLACK, 1.0); f.line((cx, oy), (cx, oy + 6.5), BLACK, 1.0)
    f.poly([(ox, oy), (ox + 6.5, oy), (ox + 6.5, oy + 6.5), (ox, oy + 6.5)], stroke=BLACK, w=0.8)
    for k in range(-3, 4):
        if k:
            f.line((cx + k, cy - 0.07), (cx + k, cy + 0.07), BLACK, 0.8); f.line((cx - 0.07, cy + k), (cx + 0.07, cy + k), BLACK, 0.8)
    for k in (-2, 2):
        f.text((cx + k, cy), num(k), size=11, dy=-11); f.text((cx, cy + k), num(k), size=11, dx=-11)
    curve_fn(cx, cy)
    f.text((ox + 0.45, oy + 6.05), num_label.replace("$", "") if False else f"({num_label})", size=15)
def line_pts(pts, color=BLUE):
    f.ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=2.4 * PT, zorder=f._z(), solid_capstyle="round")
def c1(cx, cy):
    line_pts([(cx + t, cy + t * t - 2) for t in [i / 40 for i in range(-104, 105)] if abs(t * t - 2) <= 3.1])
def c2(cx, cy):
    line_pts([(cx + 2 * math.cos(t), cy + 2 * math.sin(t)) for t in [i * math.pi / 100 for i in range(0, 201)]])
def c3(cx, cy):
    line_pts([(cx + t, cy + 1 / t) for t in [0.34 + i * (3.0 - 0.34) / 200 for i in range(201)]])
    line_pts([(cx - t, cy - 1 / t) for t in [0.34 + i * (3.0 - 0.34) / 200 for i in range(201)]])
def c4(cx, cy):
    line_pts([(cx + t * t, cy + t) for t in [i / 40 for i in range(-68, 69)]])
for (ox, oy), fn, lab in zip([(0.5, 8.0), (8.0, 8.0), (0.5, 0.5), (8.0, 0.5)], [c1, c2, c3, c4], ["1", "2", "3", "4"]):
    plane(ox, oy, fn, lab)
f.save("s-fonctions.svg")

# S.2 — parabole f(x) = x^2 - 2x - 3
def parab(sol=False):
    g = G((-3, 5), (-5, 7), unit=34)
    g.grid_xy(1, 1); g.axes_xy(range(-3, 5), range(-5, 7))
    g.curve(lambda x: x * x - 2 * x - 3, -2.6, 4.6, BLUE)
    g.tx(4.6, 6.1, r"$f$", BLUE, 17)
    if sol:
        g.hline(5, color=RED); g.pt(-2, 5, None, RED); g.pt(4, 5, None, RED)
        g.tx(-2, 5, r"$(-2;\,5)$", RED, 13, dy=12, dx=-18); g.tx(4, 5, r"$(4;\,5)$", RED, 13, dy=12, dx=2)
        g.hline(-4, color=GREEN); g.pt(1, -4, None, GREEN); g.tx(1, -4, r"$(1;\,-4)$", GREEN, 13, dy=-14)
    return g
parab(False).save("s-parabole.svg")
parab(True).save("s-parabole-sol.svg")

# S.3 — fréquence cardiaque maximale
g = G((0, 70), (150, 210), sx=10, sy=10, unit=44)
g.grid_xy(10, 10)
g.axes_xy(range(10, 70, 10), range(160, 210, 10), xl="a", yl="FC", ox=0, oy=150,
          xlab=r"$a$ (ans)", ylab=r"$FC$ (batt./min)")
g.seg((10, 201), (70, 159), BLUE)
for (a_, fc) in [(20, 194), (60, 166)]:
    g.vline(a_, 150, fc, BLACK, (3, 3), 1.0); g.hline(fc, 0, a_, BLACK, (3, 3), 1.0)
    g.pt(a_, fc, None, RED)
g.tx(20, 194, r"$(20\,;\,194)$", RED, 14, dx=10, dy=14)
g.tx(60, 166, r"$(60\,;\,166)$", RED, 14, dx=-4, dy=16)
g.save("s-fc.svg")

# S.5 / S.6 — f(x) = (x+2)(x-1)^2 sur [-3, 3]
def cubique(extra=None):
    g = G((-3.4, 3.6), (-17, 22), sy=4, unit=36)
    g.grid_xy(1, 2)
    g.axes_xy(range(-3, 4), range(-16, 21, 4), ox=0, oy=0)
    g.curve(lambda x: (x + 2) * (x - 1) ** 2, -3, 3, BLUE)
    g.pt(-3, -16, None, BLUE); g.pt(3, 20, None, BLUE)
    g.tx(2.35, 17, r"$f$", BLUE, 17)
    if extra: extra(g)
    return g
cubique().save("s-cubique.svg")
def sol_cub(g):
    g.hline(4, -3, 3, RED); g.pt(-1, 4, None, RED); g.pt(2, 4, None, RED)
    g.hline(2, -3, 3, GREEN); [g.pt(x, 2, None, GREEN) for x in (-math.sqrt(3), 0, math.sqrt(3))]
    g.hline(10, -3, 3, PURPLE); g.pt(2.4946, 10, None, PURPLE)
cubique(sol_cub).save("s-cubique-sol.svg")

# S.7 — graphe de f (lignes brisées)
g = G((0, 5), (0, 4), unit=42)
g.grid_xy(1, 1); g.axes_xy(range(1, 5), range(1, 4))
pts = [(0, 2), (1, 0), (2, 1), (3, 3), (4, 2)]
for a_, b_ in zip(pts[:-1], pts[1:]):
    g.seg(a_, b_, BLUE)
for p in pts: g.pt(*p, None, BLUE)
g.tx(3.6, 3.15, r"$f$", BLUE, 17)
g.save("s-composition.svg")

# S.8 — f(x) = -2x + 4, la diagonale, (et la réciproque en solution)
def recip(sol=False):
    g = G((-3, 7), (-3, 7), unit=34)
    g.grid_xy(1, 1); g.axes_xy(range(-3, 7), range(-3, 7))
    g.curve(lambda x: -2 * x + 4, -1.5, 3.5, BLUE)
    g.curve(lambda x: x, -3, 6.8, BLACK, w=1.2)
    g.tx(3.4, 6.2, r"$f$", BLUE, 17); g.tx(6.35, 6.0, r"$y=x$", BLACK, 14)
    g.pt(1, 2, r"$(1;\,2)$", BLUE, dx=22, dy=12, size=13)
    if sol:
        g.curve(lambda x: (4 - x) / 2, -3, 7, GREEN)
        g.tx(-2.2, 4.4, r"$f^{-1}$", GREEN, 17)
        g.pt(2, 1, r"$(2;\,1)$", GREEN, dx=22, dy=-10, size=13)
        g.seg((1, 2), (2, 1), RED, 1.4, (4, 3))
    return g
recip(False).save("s-reciproque.svg")
recip(True).save("s-reciproque-sol.svg")


# S.2 — trois diagrammes sagittaux
from matplotlib.patches import Ellipse
def sagittal(fg, ox, left, right, arrows, label, colors=None, lname="", rname=""):
    """Panneau sagittal : deux ovales, points alignés, flèches. (ox, 0) = coin bas-gauche, largeur 4.6, hauteur 6."""
    for cx_, items in ((ox + 1.45, left), (ox + 4.5, right)):
        fg.ax.add_patch(Ellipse((cx_, 3.0), 2.8, 5.4, fc="none", ec=BLACK, lw=1.2 * PT, zorder=fg._z()))
    def ys(items):
        n = len(items); step = min(1.25, 4.0 / max(n - 1, 1)) if n > 1 else 0
        return [3.0 + (n - 1) * step / 2 - i * step for i in range(n)]
    ly, ry = ys(left), ys(right)
    for (x_, items, yy, side) in ((ox + 1.45, left, ly, -1), (ox + 4.5, right, ry, 1)):
        for it, y_ in zip(items, yy):
            fg.dot((x_, y_), BLACK, 3.4)
            fg.text((x_, y_), num(it) if isinstance(it, (int, float)) else it, size=14, dx=side * 17, dy=0)
    for (i, j) in arrows:
        a, b = (ox + 1.45 + 0.1, ly[i]), (ox + 4.5 - 0.12, ry[j])
        fg.arrow(a, b, BLUE, 1.6, 9)
    fg.text((ox + 3.0, 6.0), f"({label})", size=15)
fg = Fig(0, 17.9, 0, 6.3, unit=28, margin=10)
sagittal(fg, 0.0, [-2, -1, 0, 1, 2], [0, 1, 4, 5], [(0, 2), (1, 1), (2, 0), (3, 1), (4, 2)], "1")
sagittal(fg, 6.0, [1, 2, 3], [2, 4, 6, 8], [(0, 0), (1, 1), (1, 2), (2, 2)], "2")
sagittal(fg, 12.0, [1, 2, 3, 4], [1, 4, 9, 16], [(0, 0), (1, 1), (2, 2)], "3")
fg.save("s-sagittal.svg")

# S.5 — conversions de registres : grille vide et graphe de k(x) = -x/2 + 1
g = G((-3, 5), (-6, 6), unit=30)
g.grid_xy(1, 1); g.axes_xy(range(-3, 5), range(-6, 6))
g.save("s-registres-grille.svg")
g = G((-3, 5), (-2, 4), unit=40)
g.grid_xy(1, 1); g.axes_xy(range(-3, 5), range(-2, 4))
g.seg((-2, 2), (4, -1), BLUE)
for p in [(-2, 2), (0, 1), (2, 0), (4, -1)]:
    g.pt(*p, None, BLUE)
g.tx(-1.6, 2.5, r"$k$", BLUE, 17)
g.save("s-registres-k.svg")

# =====================================================================
# TRANSFERT
# =====================================================================
# T.2 — dilution du sérum physiologique : C(V) = 4,5 / (0,5 + V)
g = G((0, 5.5), (0, 10), unit=40)
g.grid_xy(0.5, 1) if False else g.grid_xy(1, 1)
g.axes_xy(range(1, 6), range(1, 10), xl="V", yl="C", xlab=r"$V$ (L)", ylab=r"$C$ (g/L)")
g.curve(lambda V: 4.5 / (0.5 + V), 0, 5.4, BLUE)
g.pt(0, 9, None, BLUE)
g.save("t-dilution.svg")
def dil_sol():
    g = G((0, 5.5), (0, 10), unit=40)
    g.grid_xy(1, 1); g.axes_xy(range(1, 6), range(1, 10), xlab=r"$V$ (L)", ylab=r"$C$ (g/L)")
    g.curve(lambda V: 4.5 / (0.5 + V), 0, 5.4, BLUE)
    g.pt(0, 9, None, BLUE)
    g.vline(1, 0, 3, RED); g.hline(3, 0, 1, RED); g.pt(1, 3, r"$(1\,;\,3)$", RED, dx=26, dy=12, size=13)
    g.vline(4.5, 0, 0.9, GREEN); g.hline(0.9, 0, 4.5, GREEN); g.pt(4.5, 0.9, r"$(4{,}5\,;\,0{,}9)$", GREEN, dx=2, dy=18, size=13)
    return g
dil_sol().save("t-dilution-sol.svg")

# T.3 — clairance en fonction de la créatinine : ClCr(s) = 90 / s
def clairance(sol=False):
    g = G((0, 6), (0, 105), sy=20, unit=60, margin=22)
    g.grid_xy(1, 20)
    g.axes_xy(range(1, 6), range(20, 101, 20), xl="s", yl="C", xlab=r"$s$ (mg/dL)", ylab=r"$ClCr$ (mL/min)")
    g.curve(lambda s: 90 / s, 0.86, 5.9, BLUE)
    for yy in (15, 30, 45, 60, 90):
        g.hline(yy, 0, 6, BLACK, (6, 3), 0.9)
    for yy, lab in [(100, "G1"), (75, "G2"), (52.5, "G3a"), (37.5, "G3b"), (22.5, "G4"), (7.5, "G5")]:
        g.tx(5.92, yy, lab, BLACK, 13, ha="right")
    if sol:
        for s_, c_ in [(1.5, 60), (3, 30)]:
            g.vline(s_, 0, c_, RED); g.pt(s_, c_, None, RED)
    return g
clairance(False).save("t-clairance.svg")
clairance(True).save("t-clairance-sol.svg")

# =====================================================================
# RENFORCEMENT
# =====================================================================
# R.1 — Tanaka, puis Fox en solution
def fc2(sol=False):
    g = G((0, 70), (150, 210), sx=10, sy=10, unit=44)
    g.grid_xy(10, 10)
    g.axes_xy(range(10, 70, 10), range(160, 210, 10), ox=0, oy=150, xlab=r"$a$ (ans)", ylab=r"$FC$ (batt./min)")
    g.seg((10, 201), (70, 159), BLUE)
    g.tx(63, 160, r"Tanaka", BLUE, 14, dy=-1, ha="right") if False else None
    if sol:
        g.seg((10, 210), (70, 150), RED)
        g.vline(40, 150, 180, BLACK, (3, 3), 1.0); g.hline(180, 0, 40, BLACK, (3, 3), 1.0)
        g.pt(40, 180, r"$(40\,;\,180)$", BLACK, dx=34, dy=14, size=14)
    return g
fc2(False).save("r-fc.svg")
fc2(True).save("r-fc-sol.svg")

# R.3 — g(x) = |x-2| - 3
g = G((-4, 8), (-4, 6), unit=34)
g.grid_xy(1, 1); g.axes_xy(range(-4, 8), range(-4, 6))
g.curve(lambda x: abs(x - 2) - 3, -3.9, 7.9, BLUE)
g.tx(7.2, 3.2, r"$g$", BLUE, 17)
g.save("r-absolue.svg")

# R.4 — f(x) = x^2 - 4x sur [0, 5]
g = G((-1, 6), (-5, 7), unit=38)
g.grid_xy(1, 1); g.axes_xy(range(-1, 6), range(-5, 7))
g.curve(lambda x: x * x - 4 * x, 0, 5, BLUE)
g.pt(0, 0, None, BLUE); g.pt(5, 5, None, BLUE)
g.tx(0.6, 2.0, r"$f$", BLUE, 17)
g.save("r-parabole.svg")

# R.5 — h(x) = x^3 - 3x sur [-2, 2]
g = G((-2.6, 2.8), (-3.6, 3.8), unit=44)
g.grid_xy(1, 1); g.axes_xy(range(-2, 3), range(-3, 4))
g.curve(lambda x: x ** 3 - 3 * x, -2, 2, BLUE)
g.pt(-2, -2, None, BLUE); g.pt(2, 2, None, BLUE)
g.tx(1.85, 3.0, r"$h$", BLUE, 17)
g.save("r-cubique.svg")

print("figures écrites :", len([n for n in os.listdir(OUT) if n.endswith(".svg")]))
print(json.dumps(SIZES))
