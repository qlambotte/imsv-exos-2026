#!/usr/bin/env python3
"""Figures de la séance 8 (calcul différentiel).

    python3 figs.py      # écrit les SVG à côté du script, et copie ceux des slides dans slides/seance08/img

Socle : s-associer (S.4), s-graphes (S.5). Pas de gris (photocopie) : noir et bleu.
"""
import os
import shutil
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
                     "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s08"})
OUT = os.path.dirname(os.path.abspath(__file__))
_SL = os.path.normpath(os.path.join(OUT, "..", "..", "..", "slides"))
# Le deck suit l'interrupteur de seance-onoff.py : slides/seance07 en ligne, slides/_seance08 hors ligne.
SLIDES = os.path.join(_SL, "_seance08" if os.path.isdir(os.path.join(_SL, "_seance08")) else "seance08", "img")
BLUE, BLACK, ORANGE = "#1f5fbf", "#000000", "#c24a00"
LW = 2.2


def axes(ax, xlim, ylim, xt, yt, xlabel="$x$", ylabel="$y$", origin=True):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if origin:
        ax.spines["bottom"].set_position(("data", 0 if ylim[0] < 0 < ylim[1] else ylim[0]))
        ax.spines["left"].set_position(("data", 0 if xlim[0] < 0 < xlim[1] else xlim[0]))
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.1)
    ax.set_xticks([t for t in xt if not (origin and t == 0)])
    ax.set_yticks([t for t in yt if not (origin and t == 0)])
    ax.tick_params(labelsize=12, width=1, length=4)
    ax.grid(True, color=BLACK, lw=0.4, ls=(0, (1, 3))); ax.set_axisbelow(True)
    y0 = 0 if (origin and ylim[0] < 0 < ylim[1]) else ylim[0]
    x0 = 0 if (origin and xlim[0] < 0 < xlim[1]) else xlim[0]
    ax.annotate(xlabel, xy=(xlim[1], y0), xytext=(0, 6), textcoords="offset points", ha="right", fontsize=14)
    ax.annotate(ylabel, xy=(x0, ylim[1]), xytext=(6, -4), textcoords="offset points", va="top", fontsize=14)


def plein(ax, x, y):
    ax.plot([x], [y], "o", ms=7, color=BLUE, zorder=5)


def vide(ax, x, y):
    ax.plot([x], [y], "o", ms=7, mfc="white", mec=BLUE, mew=1.8, zorder=5)


def save(fig, nom, slides=False):
    p = os.path.join(OUT, nom)
    fig.savefig(p, facecolor="white", metadata={"Date": None})
    plt.close(fig)
    if slides:
        os.makedirs(SLIDES, exist_ok=True)
        shutil.copy(p, os.path.join(SLIDES, nom))



# --- S.4 : associer trois fonctions et leurs dérivées --------------------------------------
# A(x) = 2 - x^2/2  ->  -x (graphe 3) ; B(x) = 2 - e^{-x}  ->  e^{-x} (graphe 2) ; C(x) = x - x^3/3  ->  1 - x^2 (graphe 1)
fonctions = [("A", lambda x: 2 - x ** 2 / 2), ("B", lambda x: 2 - np.exp(-x)), ("C", lambda x: x - x ** 3 / 3)]
derivees = [("1", lambda x: 1 - x ** 2), ("2", lambda x: np.exp(-x)), ("3", lambda x: -x)]
fig, axs = plt.subplots(2, 3, figsize=(10, 6.6))
xs = np.linspace(-2.4, 2.4, 400)
for ligne, liste in enumerate((fonctions, derivees)):
    for col, (lab, f) in enumerate(liste):
        ax = axs[ligne][col]
        y = f(xs); y = np.where((y > 3.4) | (y < -3.4), np.nan, y)
        ax.plot(xs, y, color=BLUE, lw=LW)
        axes(ax, (-2.5, 2.5), (-3.4, 3.4), range(-2, 3), range(-3, 4))
        ax.text(-2.35, 3.1, lab, fontsize=15, fontweight="bold", va="top")
fig.tight_layout(h_pad=2.2)
save(fig, "s-associer.svg", slides=True)

# --- S.5 : graphes de f et de g, formés de segments -----------------------------------------
# g : (0;0) -> (2;4) -> (6;2) ; f : (0;3) -> (3;0) -> (6;3)
fig, axs = plt.subplots(1, 2, figsize=(10, 4.6))
for ax, (nom, xs_, ys_) in zip(axs, (("g", [0, 2, 6], [0, 4, 2]), ("f", [0, 3, 6], [3, 0, 3]))):
    ax.plot(xs_, ys_, color=BLUE, lw=LW)
    for x_, y_ in zip(xs_, ys_):
        ax.plot([x_], [y_], "o", ms=5, color=BLACK, zorder=5)
    axes(ax, (0, 6.4), (0, 5.4), range(0, 7), range(0, 6), origin=True)
    ax.text(5.6, 4.9, nom, fontsize=16, style="italic")
fig.tight_layout(w_pad=3)
save(fig, "s-graphes.svg", slides=True)

print("figures écrites dans", OUT)
