#!/usr/bin/env python3
"""Figures de l'échauffement (Q1, séance 5) : trois graphes, croissante / décroissante / ni l'une ni l'autre.
Usage : python3 figs-echauffement.py  (écrit q1-croissance.svg et q1-solution.svg à côté du script).
q1-solution.svg : parties croissantes en vert, parties décroissantes en rouge. Pas de gris."""
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
                     "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s05-q1"})
OUT = os.path.dirname(os.path.abspath(__file__))
BLUE, BLACK, GREEN, RED = "#1f5fbf", "#000000", "#2e7d46", "#c0392b"

panels = [
    ("A", lambda x: np.sqrt(x) - 2, (0, 4), (-2.6, 1.2), None),          # croissante, valeurs négatives
    ("B", lambda x: 3 / (x + 1) + 0.2, (0, 4), (-0.8, 3.6), None),       # décroissante, valeurs positives
    ("C", lambda x: 0.7 * (x - 2) ** 2 - 1.2, (0, 4), (-1.8, 2.0), 2.0),  # décroît puis croît (changement en x = 2)
]


def dessine(nom, solution):
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.7))
    for ax, (lab, f, xl, yl, cut) in zip(axes, panels):
        if not solution:
            x = np.linspace(xl[0], xl[1], 400)
            ax.plot(x, f(x), color=BLUE, lw=3, zorder=4)
        else:
            bornes = [xl[0], xl[1]] if cut is None else [xl[0], cut, xl[1]]
            for a, b in zip(bornes[:-1], bornes[1:]):
                xs = np.linspace(a, b, 300)
                m = (a + b) / 2
                croissante = f(m + 0.01) > f(m - 0.01)
                ax.plot(xs, f(xs), color=GREEN if croissante else RED, lw=3.4, zorder=4, solid_capstyle="butt")
        ax.set_xlim(xl[0] - 0.4, xl[1] + 0.7); ax.set_ylim(*yl)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_position(("data", 0)); ax.spines["bottom"].set_position(("data", 0))
        for s in ("left", "bottom"):
            ax.spines[s].set_linewidth(1.3)
        ax.set_xticks([]); ax.set_yticks([])
        ax.annotate(r"$x$", (xl[1] + 0.7, 0), xytext=(2, -4), textcoords="offset points", fontsize=17, ha="left", va="top")
        ax.annotate(r"$y$", (0, yl[1]), xytext=(6, -2), textcoords="offset points", fontsize=17, ha="left", va="top")
        ax.set_title(lab, fontsize=20, fontweight="bold", pad=6)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.84, wspace=0.12)
    fig.savefig(os.path.join(OUT, nom), facecolor="white", metadata={"Date": None})
    plt.close(fig)


dessine("q1-croissance.svg", False)
dessine("q1-solution.svg", True)
