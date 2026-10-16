#!/usr/bin/env python3
"""Figures de la méthode « Calculer une réciproque » (séance 5) : h(x) = x^2 - 4.
Écrit r1-parabole.svg, r2-restriction.svg, r3-symetrie-complete.svg, r4-symetrie-restriction.svg à côté du script.
Noir et couleurs franches, pas de gris."""
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
                     "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s05-recip"})
OUT = os.path.dirname(os.path.abspath(__file__))
BLUE, LBLUE, RED, BLACK = "#1f5fbf", "#8fb1e6", "#c0392b", "#000000"

def base(lim=(-5.2, 6.2)):
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_aspect("equal")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_position(("data", 0)); ax.spines["bottom"].set_position(("data", 0))
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.3)
    ticks = [t for t in range(-5, 7) if t != 0]
    ax.set_xticks(ticks); ax.set_yticks(ticks)
    ax.tick_params(labelsize=11, length=3)
    ax.grid(True, color=BLACK, lw=0.4, ls=(0, (1, 4)))
    ax.set_axisbelow(True)
    ax.annotate(r"$x$", (lim[1], 0), xytext=(2, -4), textcoords="offset points", fontsize=16, ha="left", va="top")
    ax.annotate(r"$y$", (0, lim[1]), xytext=(6, -2), textcoords="offset points", fontsize=16, ha="left", va="top")
    return fig, ax

def save(fig, name):
    fig.subplots_adjust(left=0.04, right=0.96, bottom=0.04, top=0.97)
    fig.savefig(os.path.join(OUT, name), facecolor="white", metadata={"Date": None}); plt.close(fig)

def pt(ax, x, y, label=None, color=BLACK, off=(8, 6)):
    ax.plot([x], [y], "o", color=color, ms=7, zorder=6)
    if label:
        ax.annotate(label, (x, y), xytext=off, textcoords="offset points", fontsize=13, color=color)

xs = np.linspace(-3.45, 3.45, 600)
xr = np.linspace(0, 3.45, 400)

# 1. la parabole entière : deux entrées pour la sortie 5
fig, ax = base()
ax.plot(xs, xs**2 - 4, color=BLUE, lw=3, zorder=4)
ax.plot([-5.2, 6.2], [5, 5], color=RED, lw=2, ls=(0, (5, 3)), zorder=3)
pt(ax, -3, 5, r"$(-3\,;\,5)$", RED, (-62, 8)); pt(ax, 3, 5, r"$(3\,;\,5)$", RED, (8, 8))
ax.annotate(r"$h$", (2.6, 2.76), xytext=(8, -2), textcoords="offset points", fontsize=16, color=BLUE)
save(fig, "r1-parabole.svg")

# 2. la restriction à [0, +oo[
fig, ax = base()
ax.plot(-xr, xr**2 - 4, color=LBLUE, lw=2.5, ls=(0, (4, 3)), zorder=3)
ax.plot(xr, xr**2 - 4, color=BLUE, lw=3.5, zorder=4)
pt(ax, 0, -4, r"$(0\,;\,-4)$", BLUE, (8, -14)); pt(ax, 3, 5, r"$(3\,;\,5)$", BLUE, (8, 6))
ax.annotate(r"branche écartée", (-5.1, 3.8), xytext=(0, 0), textcoords="offset points", fontsize=13, color=BLUE)
save(fig, "r2-restriction.svg")

# 3. symétrique par rapport à y = x de la parabole entière : ce n'est pas une fonction
fig, ax = base()
t = np.linspace(-3.45, 3.45, 600)
ax.plot([-5.2, 6.2], [-5.2, 6.2], color=BLACK, lw=1.6, ls=(0, (6, 3)), zorder=2)
ax.plot(t, t**2 - 4, color=LBLUE, lw=2.5, zorder=3)
ax.plot(t**2 - 4, t, color=RED, lw=3, zorder=4)
ax.plot([5, 5], [-5.2, 6.2], color=BLACK, lw=1.6, ls=(0, (2, 2)), zorder=3)
pt(ax, 5, 3, r"$(5\,;\,3)$", RED, (-34, 10)); pt(ax, 5, -3, r"$(5\,;\,-3)$", RED, (-34, -20))
ax.annotate(r"$y = x$", (5.3, 5.3), xytext=(-52, -2), textcoords="offset points", fontsize=13, color=BLACK)
save(fig, "r3-symetrie-complete.svg")

# 4. symétrique de la restriction : c'est une fonction, la réciproque
fig, ax = base()
ax.plot([-5.2, 6.2], [-5.2, 6.2], color=BLACK, lw=1.6, ls=(0, (6, 3)), zorder=2)
ax.plot(xr, xr**2 - 4, color=BLUE, lw=3.5, zorder=4)
xq = np.linspace(-4, 5.4, 500)
ax.plot(xq, np.sqrt(xq + 4), color=RED, lw=3.5, zorder=4)
pt(ax, 0, -4, r"$(0\,;\,-4)$", BLUE, (8, -14)); pt(ax, -4, 0, r"$(-4\,;\,0)$", RED, (-44, 10))
ax.annotate(r"$y = x$", (5.3, 5.3), xytext=(-52, -2), textcoords="offset points", fontsize=13, color=BLACK)
ax.annotate(r"$h^{-1}$", (4.6, 2.94), xytext=(4, 8), textcoords="offset points", fontsize=16, color=RED)
ax.annotate(r"$h$", (3.1, 5.6), xytext=(-24, -2), textcoords="offset points", fontsize=16, color=BLUE)
save(fig, "r4-symetrie-restriction.svg")
