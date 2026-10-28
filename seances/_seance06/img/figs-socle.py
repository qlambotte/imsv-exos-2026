#!/usr/bin/env python3
"""Figure de S.1 (séance 6) : six graphiques numérotés 1 à 6.
1 = log2 x · 2 = 7 - 2x · 3 = 3 + 2cos(pi x/2) · 4 = racine de x · 5 = 2^x · 6 = x^2 + 1.
Usage : python3 figs-socle.py  (écrit s-types.svg à côté du script). Pas de gris."""
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
                     "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s06-types"})
OUT = os.path.dirname(os.path.abspath(__file__))
BLUE, BLACK = "#1f5fbf", "#000000"

# (numéro, fonction, x_min, x_max, y_min, y_max, graduations x, graduations y)
G = [
    (1, lambda x: np.log2(x), 0.06, 16.5, -3.4, 5, [0, 4, 8, 12, 16], [-2, 0, 2, 4]),
    (2, lambda x: 7 - 2 * x, 0, 4.4, -2, 8.5, [0, 1, 2, 3, 4], [0, 2, 4, 6]),
    (3, lambda x: 3 + 2 * np.cos(np.pi * x / 2), 0, 8.4, 0, 6, [0, 2, 4, 6, 8], [0, 2, 4, 6]),
    (4, lambda x: np.sqrt(x), 0, 16.5, -0.6, 4.8, [0, 4, 8, 12, 16], [0, 2, 4]),
    (5, lambda x: 2.0 ** x, 0, 4.4, -1, 19, [0, 1, 2, 3, 4], [0, 8, 16]),
    (6, lambda x: x ** 2 + 1, 0, 4.4, -1, 19, [0, 1, 2, 3, 4], [0, 8, 16]),
]
fig, axs = plt.subplots(2, 3, figsize=(9.6, 5.6))
fig.subplots_adjust(left=0.05, right=0.98, top=0.9, bottom=0.08, wspace=0.28, hspace=0.5)
for ax, (n, f, x0, x1, y0, y1, xt, yt) in zip(axs.flat, G):
    xs = np.linspace(x0, x1 - 0.05, 700)
    ax.plot(xs, f(xs), color=BLUE, lw=2.2)
    ax.set_xlim(x0 if n != 1 else 0, x1); ax.set_ylim(y0, y1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0 if y0 < 0 < y1 else y0))
    ax.spines["left"].set_position(("data", 0))
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(1.1)
    ax.set_xticks([t for t in xt if t != 0]); ax.set_yticks([t for t in yt if t != 0])
    ax.tick_params(labelsize=12, width=1, length=4)
    ax.grid(True, color=BLACK, lw=0.4, ls=(0, (1, 3))); ax.set_axisbelow(True)
    ax.set_title(str(n), fontsize=17, fontweight="bold", pad=6)
fig.savefig(os.path.join(OUT, "s-types.svg"), facecolor="white", metadata={"Date": None})
