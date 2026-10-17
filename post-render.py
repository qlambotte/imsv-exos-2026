#!/usr/bin/env python3
"""Hook post-render de Quarto.

Garantit qu'une modification du CONTENU (donc du HTML) se répercute dans les PDF : à chaque
`quarto render` COMPLET (pas au preview d'un fichier), appelle incremental.py, qui régénère — DÈS
QU'UNE SOURCE a changé — les PDF de séance (énoncés, complet, hors-ligne), les feuilles de méthodes
et la boîte à outils, et recopie du cache tout ce qui n'a pas changé. IMSV_POSTRENDER évite toute
réentrance.
"""
import os
import subprocess
import sys

if os.environ.get("IMSV_POSTRENDER"):
    sys.exit(0)

# Uniquement au rendu COMPLET du projet (`quarto render` à la racine) : Quarto définit alors
# QUARTO_PROJECT_RENDER_ALL=1. Un preview / rendu d'un seul fichier ne reconstruit aucun PDF,
# ce qui garde la prévisualisation rapide (et fidèle : pas besoin de _quarto.yml local).
if os.environ.get("QUARTO_PROJECT_RENDER_ALL") != "1":
    sys.exit(0)

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
ENV = dict(os.environ, IMSV_POSTRENDER="1")

print("[post-render] PDF, feuilles, méthodes (incrémental)")
subprocess.run([sys.executable, "incremental.py", "assets"], check=True, env=ENV)
