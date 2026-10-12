#!/usr/bin/env python3
"""Régénère les QR codes de la remédiation (mur de questions, Wooclap thèmes 1 et 2).

    python3 make-qr.py        # depuis ce dossier ; dépendance : pip install "qrcode[pil]"
"""
import qrcode
from pathlib import Path

LIENS = {
    "qr-mur":    "https://app.wooclap.com/XELAEPI?from=instruction-slide",
    "qr-theme1": "https://app.wooclap.com/CKFEYZG?from=instruction-slide",
    "qr-theme2": "https://app.wooclap.com/SJDJDYG?from=instruction-slide",
}
OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)
for nom, url in LIENS.items():
    qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color="#14304a", back_color="white").save(OUT / f"{nom}.png")
    print("écrit :", OUT / f"{nom}.png", url)
