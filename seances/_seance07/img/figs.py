#!/usr/bin/env python3
"""Figures de la séance 7 (variations, limites et dérivées).

    python3 figs.py      # écrit les SVG à côté du script, et copie ceux des slides dans slides/seance07/img

Socle : s-secante, s-limites, s-continuite. Transfert : t-taille, t-paracetamol, t-michaelis.
Renforcement : r-limites, r-cubique, r-vitesse. Pas de gris (photocopie) : noir et bleu.
Données de t-taille : OMS, référence de croissance 5-19 ans, taille pour l'âge, garçons, médiane (P50).
"""
import os
import shutil
import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.interpolate import PchipInterpolator

for LM in ("/usr/share/texmf/fonts/opentype/public/lm/", "/usr/share/texlive/texmf-dist/fonts/opentype/public/lm/"):
    for f_ in ("lmroman10-regular.otf", "lmroman10-italic.otf", "lmroman10-bold.otf"):
        if os.path.exists(LM + f_):
            font_manager.fontManager.addfont(LM + f_)
plt.rcParams.update({"mathtext.fontset": "cm", "svg.fonttype": "path", "font.family": "serif",
                     "font.serif": ["Latin Modern Roman"], "svg.hashsalt": "imsv-s07"})
OUT = os.path.dirname(os.path.abspath(__file__))
_SL = os.path.normpath(os.path.join(OUT, "..", "..", "..", "slides"))
# Le deck suit l'interrupteur de seance-onoff.py : slides/seance07 en ligne, slides/_seance07 hors ligne.
SLIDES = os.path.join(_SL, "_seance07" if os.path.isdir(os.path.join(_SL, "_seance07")) else "seance07", "img")
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


# --- S.2 : f(x) = (x - 1)^2 / 2 + 1, points d'abscisses 1, 3, 5 --------------------------
fig, ax = plt.subplots(figsize=(5.2, 4.6))
xs = np.linspace(-0.6, 5.6, 400)
ax.plot(xs, (xs - 1) ** 2 / 2 + 1, color=BLUE, lw=LW)
for x in (1, 3, 5):
    ax.plot([x], [(x - 1) ** 2 / 2 + 1], "o", ms=6, color=BLACK, zorder=5)
axes(ax, (-0.8, 6), (-0.8, 11), range(0, 6), range(0, 11))
save(fig, "s-secante.svg")

# --- S.3 : limites lues sur un graphique -------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.4))
x1 = np.linspace(-8.5, -3.17, 500)
ax.plot(x1, 1 + 1 / (-3 - x1), color=BLUE, lw=LW)              # x < -3
x2 = np.linspace(-2.52, 1, 500)
y2 = 3 - 4 / (x2 + 3)
ax.plot(x2, y2, color=BLUE, lw=LW)                               # -3 < x < 1, sauf -1
x3 = np.linspace(1, 5, 300)
ax.plot(x3, 4 - (x3 - 1) ** 2 / 4, color=BLUE, lw=LW)            # 1 <= x <= 5
ax.plot([-8.5, -3], [1, 1], color=BLACK, lw=1.1, ls=(0, (5, 4)))
ax.plot([-3, -3], [-5.5, 6.5], color=BLACK, lw=1.1, ls=(0, (5, 4)))
vide(ax, -1, 1); plein(ax, -1, 3)
vide(ax, 1, 2); plein(ax, 1, 4)
plein(ax, 5, 0)
axes(ax, (-8.5, 6.5), (-5.5, 6.5), range(-8, 7), range(-5, 7))
save(fig, "s-limites.svg", slides=True)

# --- S.5 : continuité et dérivabilité, points A à D ---------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.6))
xa = np.linspace(0, 2, 50); ax.plot(xa, 1 + xa, color=BLUE, lw=LW)
xb = np.linspace(2, 4, 50); ax.plot(xb, 3 - (xb - 2) / 2, color=BLUE, lw=LW)
xc = np.linspace(4, 10, 2000)
yc = 5 + np.cbrt(xc - 6)
m = np.abs(xc - 9) > 0.06
ax.plot(np.where(m, xc, np.nan), yc, color=BLUE, lw=LW)
vide(ax, 4, 2); plein(ax, 4, 5 + np.cbrt(-2))
vide(ax, 9, 5 + np.cbrt(3)); plein(ax, 9, 4)
axes(ax, (0, 10.4), (0, 7.4), range(0, 11), range(0, 8), origin=True)
for x, lab in ((2, "A"), (4, "B"), (6, "C"), (9, "D")):
    ax.plot([x, x], [0, 7.2], color=BLACK, lw=0.8, ls=(0, (4, 3)))
    ax.text(x, 7.25, lab, ha="center", va="bottom", fontsize=14, fontweight="bold")
ax.set_xticks([]); ax.set_ylim(0, 7.9)
save(fig, "s-continuite.svg")

# --- T.1 : taille médiane des garçons (OMS), tangente en 13 ans --------------------------
age = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18])
taille = np.array([137.8, 143.1, 149.1, 156.0, 163.2, 169.0, 172.9, 175.2, 176.1])
H = PchipInterpolator(age, taille)
fig, ax = plt.subplots(figsize=(7.6, 5.2))
xs = np.linspace(10, 18, 400)
ax.plot(xs, H(xs), color=BLUE, lw=LW)
ax.plot(age, taille, "o", ms=5.5, color=BLACK, zorder=5)
xt = np.linspace(11.2, 15.4, 10)
ax.plot(xt, 156 + 7 * (xt - 13), color=ORANGE, lw=1.8, ls=(0, (6, 3)))
ax.plot([13, 15], [156, 170], "s", ms=5, color=ORANGE, zorder=6)
ax.set_xlim(9.6, 18.4); ax.set_ylim(134, 180)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xticks(range(10, 19)); ax.set_yticks(range(135, 181, 5))
ax.tick_params(labelsize=12)
ax.grid(True, color=BLACK, lw=0.4, ls=(0, (1, 3))); ax.set_axisbelow(True)
ax.set_xlabel("âge $t$ (années)", fontsize=13); ax.set_ylabel("taille $H$ (cm)", fontsize=13)
save(fig, "t-taille.svg", slides=True)

# --- T.2 : paracétamol, C(t) = 20 (1/2)^(t/2) ---------------------------------------------
fig, ax = plt.subplots(figsize=(6.6, 4.6))
xs = np.linspace(0, 8, 400)
ax.plot(xs, 20 * 0.5 ** (xs / 2), color=BLUE, lw=LW)
for t in (0, 2, 4, 6):
    ax.plot([t], [20 * 0.5 ** (t / 2)], "o", ms=6, color=BLACK, zorder=5)
ax.set_xlim(0, 8.3); ax.set_ylim(0, 22)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xticks(range(0, 9))
ax.set_yticks([0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20]); ax.set_yticklabels(["0", "2,5", "5", "7,5", "10", "12,5", "15", "17,5", "20"])
ax.tick_params(labelsize=12)
ax.grid(True, color=BLACK, lw=0.4, ls=(0, (1, 3))); ax.set_axisbelow(True)
ax.set_xlabel("temps $t$ (h)", fontsize=13); ax.set_ylabel("concentration $C$ (mg/L)", fontsize=13)
save(fig, "t-paracetamol.svg")

# --- T.3 : Michaelis-Menten, v(s) = 10 s / (2 + s) -----------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.4))
xs = np.linspace(0, 30, 600)
ax.plot(xs, 10 * xs / (2 + xs), color=BLUE, lw=LW)
ax.plot([0, 30], [10, 10], color=BLACK, lw=1.1, ls=(0, (5, 4)))
for s_ in (2, 6, 18):
    ax.plot([s_], [10 * s_ / (2 + s_)], "o", ms=6, color=BLACK, zorder=5)
ax.set_xlim(0, 30.5); ax.set_ylim(0, 11.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xticks(range(0, 31, 2)); ax.set_yticks(range(0, 12, 1))
ax.tick_params(labelsize=11)
ax.grid(True, color=BLACK, lw=0.4, ls=(0, (1, 3))); ax.set_axisbelow(True)
ax.set_xlabel("concentration du substrat $s$ (mmol/L)", fontsize=13)
ax.set_ylabel("vitesse $v$ (µmol/min)", fontsize=13)
save(fig, "t-michaelis.svg")

# --- R.2 : limites lues sur un graphique (2) ------------------------------------------------
fig, ax = plt.subplots(figsize=(7.6, 5))
x1 = np.linspace(-2, -0.8, 300); ax.plot(x1, 4 / x1 ** 2, color=BLUE, lw=LW)
x2 = np.linspace(0.8, 2, 300); ax.plot(x2, 4 / x2 ** 2, color=BLUE, lw=LW)
x3 = np.linspace(2, 6.2, 600); y3 = (x3 - 2) ** 2 / 2
y3[np.abs(x3 - 4) < 0.07] = np.nan
ax.plot(x3, y3, color=BLUE, lw=LW)
ax.plot([0, 0], [0, 6.6], color=BLACK, lw=1.1, ls=(0, (5, 4)))
plein(ax, -2, 1); plein(ax, 2, 1); vide(ax, 2, 0); vide(ax, 4, 2)
axes(ax, (-3.6, 6.6), (-0.6, 6.6), range(-3, 7), range(0, 7))
save(fig, "r-limites.svg")

# --- R.5 : f(x) = x^3 - 3x ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.4, 4.8))
xs = np.linspace(-2.3, 2.3, 400)
ax.plot(xs, xs ** 3 - 3 * xs, color=BLUE, lw=LW)
for x in (-1, 1):
    ax.plot([x], [x ** 3 - 3 * x], "o", ms=6, color=BLACK, zorder=5)
axes(ax, (-2.6, 2.6), (-5, 5), range(-2, 3), range(-4, 5))
save(fig, "r-cubique.svg")

# --- R.6 : vitesse d'un mobile ----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.plot([0, 4, 10, 14], [0, 8, 8, 0], color=BLUE, lw=LW)
ax.set_xlim(0, 15); ax.set_ylim(0, 10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xticks(range(0, 16)); ax.set_yticks(range(0, 11))
ax.tick_params(labelsize=11)
ax.grid(True, color=BLACK, lw=0.4, ls=(0, (1, 3))); ax.set_axisbelow(True)
ax.set_xlabel("temps $t$ (s)", fontsize=13); ax.set_ylabel("vitesse $v$ (m/s)", fontsize=13)
save(fig, "r-vitesse.svg")

print("figures écrites dans", OUT)
