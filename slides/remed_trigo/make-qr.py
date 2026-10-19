#!/usr/bin/env python3
"""Génère les QR codes de la remédiation (mur de questions, Wooclap trigo).

    python3 make-qr.py        # depuis ce dossier ; dépendance : pip install "qrcode[pil]"

Tant qu'un code vaut « À COMPLÉTER », le script écrit une image de remplacement
(carré « QR À COMPLÉTER ») pour que le deck se rende sans image manquante.
Renseigne les codes Wooclap ci-dessous, relance le script, puis mets à jour les textes
« Code : À COMPLÉTER » dans 01-remediation.qmd (1 occurrence).
"""
from pathlib import Path

A_COMPLETER = "À COMPLÉTER"

CODES = {
    "qr-mur":       "XELAEPI",   # mur de questions
    "qr-trigo": "NSURPTC",   # QCM Wooclap « trigo »
}
OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)


def placeholder(path):
    from PIL import Image, ImageDraw, ImageFont
    n = 370
    img = Image.new("RGB", (n, n), "white")
    d = ImageDraw.Draw(img)
    for x in range(8, n - 8, 16):                     # cadre en pointillés
        d.line([(x, 8), (x + 8, 8)], fill="#14304a", width=3)
        d.line([(x, n - 9), (x + 8, n - 9)], fill="#14304a", width=3)
        d.line([(8, x), (8, x + 8)], fill="#14304a", width=3)
        d.line([(n - 9, x), (n - 9, x + 8)], fill="#14304a", width=3)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
    except OSError:
        font = ImageFont.load_default()
    for i, ligne in enumerate(("QR", "À COMPLÉTER")):
        w = d.textlength(ligne, font=font)
        d.text(((n - w) / 2, 140 + 50 * i), ligne, fill="#14304a", font=font)
    img.save(path)


for nom, code in CODES.items():
    cible = OUT / f"{nom}.png"
    if code == A_COMPLETER:
        placeholder(cible)
        print("image de remplacement :", cible)
        continue
    import qrcode
    url = f"https://app.wooclap.com/{code}?from=instruction-slide"
    qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color="#14304a", back_color="white").save(cible)
    print("écrit :", cible, url)
