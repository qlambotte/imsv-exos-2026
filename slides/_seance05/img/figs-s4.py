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

# 2. g(x) = 2x - 1 sur [0, 3[ : le minimum existe, pas le maximum
fig, ax = repere_x((-0.8, 3.9), (-2, 6.6), [0, 1, 2, 3], [-1, 5])
g = lambda x: 2 * x - 1
ax.plot(np.linspace(-0.6, 3.7, 50), g(np.linspace(-0.6, 3.7, 50)), color=BLUE, lw=3.4, alpha=0.35, zorder=3, solid_capstyle="butt")
ax.plot([0, 3], [-1, 5], color=ORANGE, lw=4.6, zorder=5, solid_capstyle="butt")
ax.plot([0, 3], [0, 0], color=ORANGE, lw=5, zorder=5, solid_capstyle="butt")
ax.plot([0, 3.4], [5, 5], color=BLACK, lw=1.8, ls=(0, (5, 4)), zorder=4)
for xv, incl in ((0, True), (3, False)):
    for yv in (g(xv), 0):
        ax.plot([xv], [yv], "o", ms=11, zorder=7, mfc=ORANGE if incl else "white", mec=ORANGE, mew=2.4)
ax.annotate("min. : $-1$, atteint en $0$", (0, -1), xytext=(14, -4), textcoords="offset points", fontsize=17, ha="left", va="top")
ax.annotate("pas de max.", (1.4, 5), xytext=(0, 8), textcoords="offset points", fontsize=17, ha="center", va="bottom")
fig.savefig(os.path.join(OUT, "x1-borne-exclue.svg"), facecolor="white", metadata={"Date": None}); plt.close(fig)
