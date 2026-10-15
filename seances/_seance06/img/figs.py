"""Figures de la séance 6 (texte vectorisé, noir uniquement : rendu identique en PDF et sur le site).
Usage : python3 figs.py   (écrit les SVG dans le dossier courant)"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"svg.fonttype": "path", "font.size": 10, "axes.linewidth": 0.8})

def temperature():
    t = np.linspace(0, 24, 481)
    T = 37 + 0.5 * np.sin(np.pi * t / 12 + np.pi)
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.plot(t, T, color="black", lw=1.8)
    ax.axhline(37.25, color="black", lw=0.8, ls=(0, (4, 3)))
    ax.set_xlim(0, 24); ax.set_ylim(36.4, 37.6)
    ax.set_xticks(range(0, 25, 2)); ax.set_yticks([36.5, 36.75, 37.0, 37.25, 37.5])
    ax.set_yticklabels(["36,5", "36,75", "37,0", "37,25", "37,5"])
    ax.grid(True, color="black", lw=0.25, ls=(0, (1, 3)))
    ax.set_xlabel("heure de la journée $t$ (h)"); ax.set_ylabel("température $T(t)$ (°C)")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig("t-temperature.svg"); plt.close(fig)

if __name__ == "__main__":
    temperature()
