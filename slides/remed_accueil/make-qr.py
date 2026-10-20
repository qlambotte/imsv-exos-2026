#!/usr/bin/env python3
"""Génère les QR codes du deck d'accueil (mur de questions, QCM en autonomie, page des slides).

    python3 make-qr.py        # depuis ce dossier ; dépendance : pip install "qrcode[pil]"
"""
from pathlib import Path
import qrcode

WOOCLAP = {
    "qr-mur": "XELAEPI",   # mur de questions (commun à tous les decks)
    "qr-qcm": "OBMKFUU",   # QCM en autonomie (logique, vecteurs, fonctions, trigo)
}
LIENS = {
    "qr-slides": "https://qlambotte.github.io/imsv-exos-2026/slides/",   # page des slides
}
OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)

cibles = {nom: f"https://app.wooclap.com/{code}?from=instruction-slide" for nom, code in WOOCLAP.items()}
cibles.update(LIENS)
for nom, url in cibles.items():
    qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color="#14304a", back_color="white").save(OUT / f"{nom}.png")
    print("écrit :", OUT / f"{nom}.png", url)
