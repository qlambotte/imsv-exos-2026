#!/usr/bin/env python3
"""Figures des slides de la séance 5 — usage : python3 figs.py (écrit les SVG à côté du script).
matplotlib -> SVG, texte vectorisé, maths en Computer Modern. Noir + couleurs franches, fond blanc."""
import os
import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

for LM in ("/usr/share/texmf/fonts/opentype/public/lm/", "/usr/share/texlive/texmf-dist/fonts/opentype/public/lm/"):
    for f_ in ("lmroman10-regular.otf", "lmroman10-italic.otf", "lmroman10-bold.otf"):
        if os.path.exists(LM + f_):
            font_manager.fontManager.addfont(LM + f_)
plt.rcParams.update({"mathtext.fontset": "cm", "svg.fonttype": "path", "font.family": "serif",
                     "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s05-slides"})
OUT = os.path.dirname(os.path.abspath(__file__))
BLUE, RED, GREEN, BLACK = "#1f5fbf", "#c0392b", "#2e7d46", "#000000"


def repere(xlim, ylim, xlab, ylab, xt, yt, size=(7.2, 4.6)):
    fig = plt.figure(figsize=size)
    ax = fig.add_axes([0.1, 0.12, 0.86, 0.8])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if ylim[0] < 0:
        ax.spines["bottom"].set_position("zero")
    if xlim[0] < 0:
        ax.spines["left"].set_position("zero")
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.3)
    ax.set_xticks(xt); ax.set_yticks([y for y in yt if not (y == 0 and ylim[0] < 0)])
    ax.tick_params(labelsize=17, width=1.1, length=5)
    ax.grid(True, color=BLACK, lw=0.5, ls=(0, (1, 3)))
    ax.set_axisbelow(True)
    ax0 = 0 if xlim[0] < 0 else xlim[0]
    ay0 = 0 if ylim[0] < 0 else ylim[0]
    ax.annotate(xlab, (xlim[1], ay0), xytext=(-2, 8), textcoords="offset points", fontsize=20, ha="right", va="bottom")
    ax.annotate(ylab, (ax0, ylim[1]), xytext=(10, -2), textcoords="offset points", fontsize=20, ha="left", va="top")
    return fig, ax


def guide(ax, x, y, color=BLACK):
    ax.plot([x, x], [0, y], color=color, lw=1.4, ls=(0, (4, 3)), zorder=3)
    ax.plot([ax.get_xlim()[0], x], [y, y], color=color, lw=1.4, ls=(0, (4, 3)), zorder=3)
    ax.plot([x], [y], "o", color=color, ms=8, zorder=5)


# --- T.1 : S(w) = sqrt(w/20) -------------------------------------------------
fig, ax = repere((0, 135), (0, 2.8), r"$w$ (kg)", r"$S$ (m$^2$)", range(0, 121, 20), [0, 0.5, 1, 1.5, 2, 2.5])
w = np.linspace(0, 135, 500)
ax.plot(w, np.sqrt(w / 20), color=BLUE, lw=3, zorder=4)
guide(ax, 45, 1.5); guide(ax, 80, 2); guide(ax, 125, 2.5)
ax.annotate(r"$(45\ ;\ 1{,}5)$", (45, 1.5), xytext=(6, -26), textcoords="offset points", fontsize=17)
ax.annotate(r"$(80\ ;\ 2)$", (80, 2), xytext=(6, -26), textcoords="offset points", fontsize=17)
fig.savefig(os.path.join(OUT, "t1-graphe.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)

# --- Méthode 1 : F = 1,8 C + 32 ---------------------------------------------
fig, ax = repere((-10, 55), (0, 135), r"$C$ (°C)", r"$F$ (°F)", range(-10, 51, 10), range(0, 131, 20))
c = np.linspace(-10, 55, 100)
ax.plot(c, 1.8 * c + 32, color=BLUE, lw=3, zorder=4)
guide(ax, 40, 104, BLACK)
ax.annotate(r"$(40\ ;\ 104)$", (40, 104), xytext=(-110, 12), textcoords="offset points", fontsize=17)
ax.set_ylim(0, 135)
fig.savefig(os.path.join(OUT, "m1-conversion.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)


# --- Méthode 2 : signe de f(x) = x(x^2 - 4) ---------------------------------
def signe(f, xlim, ylim, xt, yt, roots, name, size=(7.2, 4.6)):
    fig, ax = repere(xlim, ylim, r"$x$", r"$f(x)$", xt, yt, size)
    x = np.linspace(xlim[0], xlim[1], 1200)
    y = f(x)
    ax.plot(x, np.where(y >= 0, y, np.nan), color=BLUE, lw=3.4, zorder=4)
    ax.plot(x, np.where(y <= 0, y, np.nan), color=RED, lw=3.4, zorder=4)
    for r in roots:
        ax.plot([r], [0], "o", color=BLACK, ms=9, zorder=6, mfc="white", mew=2)
    fig.savefig(os.path.join(OUT, name), facecolor="white", metadata={"Date": None}); plt.close(fig)


def signe_quotient():
    fig, ax = repere((-6, 5.6), (-5, 5), "", r"$f(x)$", range(-6, 6), [-4, -2, 0, 2, 4])
    ax.annotate(r"$x$", (5.6, 0), xytext=(-4, -8), textcoords="offset points", fontsize=20, ha="right", va="top")
    for x0, x1 in ((-6, -2.02), (-1.98, 5.6)):
        x = np.linspace(x0, x1, 800)
        y = (x - 1) / (x + 2)
        y = np.where(np.abs(y) <= 5, y, np.nan)
        ax.plot(x, np.where(y >= 0, y, np.nan), color=BLUE, lw=3.4, zorder=4)
        ax.plot(x, np.where(y <= 0, y, np.nan), color=RED, lw=3.4, zorder=4)
    ax.plot([-2, -2], [-5, 5], color=BLACK, lw=1.6, ls=(0, (5, 4)), zorder=3)
    ax.plot([1], [0], "o", color=BLACK, ms=9, zorder=6, mfc="white", mew=2)
    fig.savefig(os.path.join(OUT, "m2-signe.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)
signe_quotient()
signe(lambda x: x * (x - 2) ** 2, (-1, 3.5), (-8, 8), [-1, 0, 1, 2, 3], [-8, -4, 0, 4, 8], [0, 2], "m2-racine-double.svg")

# --- Méthode 1 : diagramme sagittal de la conversion C -> F, avec la flèche remontée -------
from matplotlib.patches import Ellipse
fig = plt.figure(figsize=(7.2, 4.8))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 7.2); ax.set_ylim(0, 4.8); ax.axis("off")
for cx in (1.5, 5.7):
    ax.add_patch(Ellipse((cx, 2.55), 2.2, 3.3, fc="none", ec=BLACK, lw=1.6))
ax.text(1.5, 4.55, r"$C$ (°C)", ha="center", va="center", fontsize=20)
ax.text(5.7, 4.55, r"$F$ (°F)", ha="center", va="center", fontsize=20)
L = [(20, 3.45), (37, 2.55), (40, 1.65)]
R = [("68", 3.45), ("98,6", 2.55), ("104", 1.65)]
for (v, y), (w, y2) in zip(L, R):
    ax.plot([1.5], [y], "o", color=BLACK, ms=8); ax.plot([5.7], [y2], "o", color=BLACK, ms=8)
    ax.text(1.5 - 0.3, y, str(v), ha="right", va="center", fontsize=19)
    ax.text(5.7 + 0.3, y2, w, ha="left", va="center", fontsize=19)
    dy = 0.07 if v == 40 else 0
    ax.annotate("", xy=(5.55, y2 + dy), xytext=(1.65, y + dy), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.4, shrinkA=0, shrinkB=0))
ax.annotate("", xy=(1.65, 1.65 - 0.12), xytext=(5.55, 1.65 - 0.12), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4, ls=(0, (5, 3)), shrinkA=0, shrinkB=0))
ax.text(3.6, 3.95, r"$1{,}8\,C + 32$", ha="center", va="center", fontsize=19, color=BLUE)
ax.text(3.6, 0.4, r"on remonte la flèche : $C = (F - 32)\,/\,1{,}8$", ha="center", va="center", fontsize=18, color=GREEN)
fig.savefig(os.path.join(OUT, "m1-sagittal.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)

print("figures écrites dans", OUT)
