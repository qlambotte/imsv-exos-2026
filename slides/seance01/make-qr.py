#!/usr/bin/env python3
"""Génère les QR codes des Wooclap de la séance 1.

Remplace les trois URL ci-dessous par les vrais liens de tes événements Wooclap
(un par méthode), puis lance :

    python3 make-qr.py

Les images sont écrites dans img/ et sont déjà référencées par le deck.
Dépendance : pip install "qrcode[pil]"
"""

import qrcode
from pathlib import Path

# >>> À COMPLÉTER : les trois liens Wooclap <<<
LIENS = {
    "qr-echauffement": "https://app.wooclap.com/MSKHLGY?from=instruction-slide",
    "qr-nier":         "https://app.wooclap.com/MQTNSRK?from=instruction-slide",
    # Celui-ci pointe déjà vers la vraie page de la séance (pas un placeholder).
    "qr-site":         "https://qlambotte.github.io/imsv-exos-2026/",
}

OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)

for nom, url in LIENS.items():
    qr = qrcode.QRCode(box_size=10, border=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#14304a", back_color="white")
    chemin = OUT / f"{nom}.png"
    img.save(chemin)
    print(f"écrit : {chemin}  ({url})")
