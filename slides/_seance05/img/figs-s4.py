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
