#!/usr/bin/env python3
"""Génère les QR codes des Wooclap de la séance 3.

Remplace les URL ci-dessous par les vrais liens de tes événements Wooclap, puis lance :

    python3 make-qr.py

Les images sont écrites dans img/ ; décommente ensuite les blocs {.wc-qr} du deck.
Dépendance : pip install "qrcode[pil]"
"""

import qrcode
from pathlib import Path

# >>> À COMPLÉTER : les trois liens Wooclap <<<
LIENS = {
    "qr-echauffement": "https://app.wooclap.com/A_COMPLETER?from=instruction-slide",
    "qr-equation":     "https://app.wooclap.com/A_COMPLETER?from=instruction-slide",
    "qr-systeme":      "https://app.wooclap.com/A_COMPLETER?from=instruction-slide",
}

OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)

for nom, url in LIENS.items():
    if "A_COMPLETER" in url:
        print(f"ignoré : {nom} (lien à compléter)")
        continue
    qr = qrcode.QRCode(box_size=10, border=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#14304a", back_color="white")
    chemin = OUT / f"{nom}.png"
    img.save(chemin)
    print(f"écrit : {chemin}  ({url})")
