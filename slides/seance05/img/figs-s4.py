#!/usr/bin/env python3
"""Figures de la correction de S.4 (séance 5) : f(x) = x^2 - 4x + 3 sur chaque intervalle.
La courbe entière est en trait pâle ; la portion qui correspond à l'intervalle est en orange, par-dessus.
Borne incluse : point plein ; borne exclue : point creux. Même chose sur l'axe des abscisses.
Usage : python3 figs-s4.py  (écrit s4-a.svg … s4-d.svg à côté du script). Pas de gris."""
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
                     "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s05-s4"})
OUT = os.path.dirname(os.path.abspath(__file__))
BLUE, ORANGE, BLACK = "#1f5fbf", "#c76e00", "#000000"
f = lambda x: x * x - 4 * x + 3
XLIM, YLIM = (-0.7, 5.7), (-2, 9.4)


def fig_intervalle(nom, a, b, a_incl, b_incl):
    fig = plt.figure(figsize=(6.4, 4.8))
    ax = fig.add_axes([0.09, 0.1, 0.88, 0.86])
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["left"].set_position(("data", 0))
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.3)
    ax.set_xticks(range(0, 6)); ax.set_yticks([-1, 3, 8])
    ax.tick_params(labelsize=17, width=1.1, length=5)
    ax.grid(True, color=BLACK, lw=0.5, ls=(0, (1, 3))); ax.set_axisbelow(True)
    ax.annotate(r"$x$", (XLIM[1], 0), xytext=(-2, 8), textcoords="offset points", fontsize=20, ha="right", va="bottom")
    ax.annotate(r"$y$", (0, YLIM[1]), xytext=(10, -2), textcoords="offset points", fontsize=20, ha="left", va="top")
    # courbe entière, en bleu pâle
    x = np.linspace(-0.45, 5.25, 400)
    ax.plot(x, f(x), color=BLUE, lw=3.4, alpha=0.35, zorder=3, solid_capstyle="butt")
    # portion de l'intervalle, en couleur
    xs = np.linspace(a, b, 300)
    ax.plot(xs, f(xs), color=ORANGE, lw=4.6, zorder=5, solid_capstyle="butt")
    # segment sur l'axe des abscisses
    ax.plot([a, b], [0, 0], color=ORANGE, lw=5, zorder=5, solid_capstyle="butt")
    for xv, incl in ((a, a_incl), (b, b_incl)):
        for yv in (f(xv), 0):
            ax.plot([xv], [yv], "o", ms=11, zorder=7, mfc=ORANGE if incl else "white", mec=ORANGE, mew=2.4)
    fig.savefig(os.path.join(OUT, nom), facecolor="white", metadata={"Date": None})
    plt.close(fig)


fig_intervalle("s4-a.svg", 0, 5, True, True)
fig_intervalle("s4-b.svg", 0, 5, True, False)
fig_intervalle("s4-c.svg", 2, 5, False, True)
fig_intervalle("s4-d.svg", 0, 4, True, False)


# ---------------------------------------------------------------------------
# (e) : borne exclue qui supprime le maximum (b) ou non (d) — la valeur dont f s'approche
def fig_e(nom, a, b, a_incl, b_incl, ligne, texte, tx, ty):
    fig = plt.figure(figsize=(6.4, 4.8))
    ax = fig.add_axes([0.09, 0.1, 0.88, 0.86])
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0)); ax.spines["left"].set_position(("data", 0))
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.3)
    ax.set_xticks(range(0, 6)); ax.set_yticks([-1, 3, 8])
    ax.tick_params(labelsize=17, width=1.1, length=5)
    ax.grid(True, color=BLACK, lw=0.5, ls=(0, (1, 3))); ax.set_axisbelow(True)
    ax.annotate(r"$x$", (XLIM[1], 0), xytext=(-2, 8), textcoords="offset points", fontsize=20, ha="right", va="bottom")
    ax.annotate(r"$y$", (0, YLIM[1]), xytext=(10, -2), textcoords="offset points", fontsize=20, ha="left", va="top")
    x = np.linspace(-0.45, 5.25, 400)
    ax.plot(x, f(x), color=BLUE, lw=3.4, alpha=0.35, zorder=3, solid_capstyle="butt")
    xs = np.linspace(a, b, 300)
    ax.plot(xs, f(xs), color=ORANGE, lw=4.6, zorder=5, solid_capstyle="butt")
    ax.plot([a, b], [0, 0], color=ORANGE, lw=5, zorder=5, solid_capstyle="butt")
    # niveau dont f s'approche : trait horizontal en pointillés
    ax.plot([0, max(a, b) + 0.5], [ligne, ligne], color=BLACK, lw=1.8, ls=(0, (5, 4)), zorder=4)
    for xv, incl in ((a, a_incl), (b, b_incl)):
        for yv in (f(xv), 0):
            ax.plot([xv], [yv], "o", ms=11, zorder=7, mfc=ORANGE if incl else "white", mec=ORANGE, mew=2.4)
    ax.annotate(texte, (tx, ty), fontsize=19, ha="center", va="bottom")
    fig.savefig(os.path.join(OUT, nom), facecolor="white", metadata={"Date": None})
    plt.close(fig)


fig_e("s4-e1.svg", 0, 5, True, False, 8, r"$8$ n'est jamais atteint", 3.0, 8.25)
fig_e("s4-e2.svg", 0, 4, True, False, 3, r"$3$ est atteint en $0$", 2.6, 3.25)


# ---------------------------------------------------------------------------
# Rappel « extrema » : deux graphes pour rafraîchir la mémoire
def repere_x(xlim, ylim, xt, yt, size=(6.4, 4.8)):
    fig = plt.figure(figsize=size)
    ax = fig.add_axes([0.09, 0.1, 0.88, 0.86])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0)); ax.spines["left"].set_position(("data", 0))
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.3)
    ax.set_xticks(xt); ax.set_yticks(yt)
    ax.tick_params(labelsize=16, width=1.1, length=5)
    ax.grid(True, color=BLACK, lw=0.5, ls=(0, (1, 3))); ax.set_axisbelow(True)
    ax.annotate(r"$x$", (xlim[1], 0), xytext=(-2, 8), textcoords="offset points", fontsize=20, ha="right", va="bottom")
    ax.annotate(r"$y$", (0, ylim[1]), xytext=(10, -2), textcoords="offset points", fontsize=20, ha="left", va="top")
    return fig, ax


# 1. f(x) = (x+2)(x-1)^2 sur [-3, 3] : extrema locaux et globaux
fig, ax = repere_x((-3.6, 3.7), (-19, 24), [-3, -2, -1, 0, 1, 2, 3], [-16, 0, 4, 20])
h = lambda x: (x + 2) * (x - 1) ** 2
xs = np.linspace(-3, 3, 400)
ax.plot(xs, h(xs), color=BLUE, lw=3.6, zorder=4)
for xv, glob in ((-3, True), (-1, False), (1, False), (3, True)):
    ax.plot([xv], [h(xv)], "o", ms=12, zorder=7, mfc=ORANGE if glob else BLUE, mec=ORANGE if glob else BLUE, mew=2)
ax.annotate("max. local", (-1, 4), xytext=(-6, 12), textcoords="offset points", fontsize=17, ha="right", va="bottom")
ax.annotate("min. local", (1, 0), xytext=(10, -22), textcoords="offset points", fontsize=17, ha="left", va="top")
ax.annotate("min. global", (-3, -16), xytext=(14, 8), textcoords="offset points", fontsize=17, ha="left", va="bottom")
ax.annotate("max. global", (3, 20), xytext=(-10, -2), textcoords="offset points", fontsize=17, ha="right", va="center")
fig.savefig(os.path.join(OUT, "x1-locaux-globaux.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)

# 2. S.4 : f(x) = x^2 - 4x + 3 sur [0, 5[ : le minimum existe, pas le maximum
fig, ax = repere_x(XLIM, YLIM, range(0, 6), [-1, 3, 8])
ax.plot(np.linspace(-0.45, 5.25, 400), f(np.linspace(-0.45, 5.25, 400)), color=BLUE, lw=3.4, alpha=0.35, zorder=3, solid_capstyle="butt")
xs = np.linspace(0, 5, 300)
ax.plot(xs, f(xs), color=ORANGE, lw=4.6, zorder=5, solid_capstyle="butt")
ax.plot([0, 5], [0, 0], color=ORANGE, lw=5, zorder=5, solid_capstyle="butt")
ax.plot([0, 5.5], [8, 8], color=BLACK, lw=1.8, ls=(0, (5, 4)), zorder=4)
for xv, incl in ((0, True), (5, False)):
    for yv in (f(xv), 0):
        ax.plot([xv], [yv], "o", ms=11, zorder=7, mfc=ORANGE if incl else "white", mec=ORANGE, mew=2.4)
ax.plot([2], [-1], "o", ms=11, zorder=7, mfc=ORANGE, mec=ORANGE)
ax.annotate("min. : $-1$, en $2$", (2, -1), xytext=(14, -3), textcoords="offset points", fontsize=17, ha="left", va="top")
ax.annotate("pas de max.", (2.6, 8), xytext=(0, 8), textcoords="offset points", fontsize=17, ha="center", va="bottom")
fig.savefig(os.path.join(OUT, "x1-borne-exclue.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)


# ---------------------------------------------------------------------------
# Rappels : tracer une fonction du 1er degré, puis du 2e degré
GREEN, PURPLE, RED = "#2e7d46", "#7b3fa0", "#c0392b"
NAVY = "#14304a"

# 1er degré : g(x) = 2x - 3 ; pente (orange) et ordonnée à l'origine (bleu).
# Une figure par étape (cumulatives, même cadre) : x2-premier-0.svg (repère vide) … x2-premier-3.svg (tracé).
def premier(k):
    fig, ax = repere_x((-1.3, 4.3), (-4.6, 4.4), range(-1, 5), [-3, -1, 1, 3])
    if k >= 1:
        ax.plot([0], [-3], "o", ms=12, color=BLUE, zorder=8)
        ax.annotate(r"$(0\,;\,-3)$", (0, -3), xytext=(-14, 12), textcoords="offset points", fontsize=19, color=BLUE, ha="right", va="bottom")
    if k >= 2:
        ax.plot([0, 1], [-3, -3], color=ORANGE, lw=4, zorder=6, solid_capstyle="butt")
        ax.plot([1, 1], [-3, -1], color=ORANGE, lw=4, zorder=6, solid_capstyle="butt")
        ax.plot([1], [-1], "o", ms=10, color=ORANGE, zorder=8)
        ax.annotate(r"$+1$", (0.5, -3), xytext=(0, -8), textcoords="offset points", fontsize=19, color=ORANGE, ha="center", va="top")
        ax.annotate(r"$+2$", (1, -2), xytext=(10, 0), textcoords="offset points", fontsize=19, color=ORANGE, ha="left", va="center")
    if k >= 3:
        xs = np.linspace(-0.6, 3.7, 50)
        ax.plot(xs, 2 * xs - 3, color=NAVY, lw=3.4, zorder=4)
        ax.annotate(r"$g$", (3.45, 3.9), xytext=(12, 0), textcoords="offset points", fontsize=21, color=NAVY, ha="left", va="center")
    fig.savefig(os.path.join(OUT, f"x2-premier-{k}.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)


for k in range(4):
    premier(k)


# 2e degré : f(x) = x^2 - 4x + 3 ; racines (orange), ordonnée à l'origine (bleu), axe de symétrie (vert), sommet (violet).
# x2-second-0.svg (repère vide) … x2-second-5.svg (tracé de la parabole).
def second(k):
    fig, ax = repere_x((-0.9, 5.0), (-2, 5.4), range(0, 5), [-1, 3])
    if k >= 1:
        ax.plot([1, 3], [0, 0], "o", ms=12, color=ORANGE, zorder=8)
        ax.annotate(r"$1$", (1, 0), xytext=(-2, 12), textcoords="offset points", fontsize=19, color=ORANGE, ha="right", va="bottom")
        ax.annotate(r"$3$", (3, 0), xytext=(4, 12), textcoords="offset points", fontsize=19, color=ORANGE, ha="left", va="bottom")
    if k >= 2:
        ax.plot([0], [3], "o", ms=12, color=BLUE, zorder=8)
        ax.annotate(r"$(0\,;\,3)$", (0, 3), xytext=(12, 8), textcoords="offset points", fontsize=19, color=BLUE, ha="left", va="bottom")
    if k >= 3:
        ax.plot([2, 2], [-2, 5.4], color=GREEN, lw=2.6, ls=(0, (6, 4)), zorder=5)
        ax.annotate(r"$x = 2$", (2, 5.4), xytext=(8, -4), textcoords="offset points", fontsize=19, color=GREEN, ha="left", va="top")
        ax.plot([0, 4], [3, 3], color=BLUE, lw=1.6, ls=(0, (2, 3)), zorder=5)
        ax.plot([4], [3], "o", ms=12, mfc="white", mec=BLUE, mew=2.4, zorder=8)
    if k >= 4:
        ax.plot([2], [-1], "o", ms=12, color=PURPLE, zorder=8)
        ax.annotate(r"$(2\,;\,-1)$", (2, -1), xytext=(12, -6), textcoords="offset points", fontsize=19, color=PURPLE, ha="left", va="top")
    if k >= 5:
        xs = np.linspace(-0.55, 4.55, 400)
        ax.plot(xs, f(xs), color=NAVY, lw=3.4, zorder=4)
        ax.annotate(r"$f$", (4.55, f(4.55)), xytext=(10, 0), textcoords="offset points", fontsize=21, color=NAVY, ha="left", va="center")
    fig.savefig(os.path.join(OUT, f"x2-second-{k}.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)


for k in range(6):
    second(k)
