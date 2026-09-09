#!/usr/bin/env python3
"""Génère le QR code (PNG) pointant vers le site de la séance.

Usage :
    python3 make_qr.py "https://url-reelle-du-site/seance01" img/qr.png

Dépend uniquement de reportlab (encodeur QR) + Pillow (rendu),
tous deux sans accès réseau. Niveau de correction d'erreur M.
Relancer ce script chaque fois que l'URL du site change.
"""
import sys
from reportlab.graphics.barcode import qr
from PIL import Image

def make_qr_png(url: str, path: str, box: int = 10, border: int = 4, level: str = "M") -> None:
    widget = qr.QrCodeWidget(url, barLevel=level)
    code = widget.qr
    code.make()
    n = code.getModuleCount()
    size = (n + 2 * border) * box
    img = Image.new("1", (size, size), 1)  # fond blanc
    px = img.load()
    for r in range(n):
        for c in range(n):
            if code.isDark(r, c):
                x0, y0 = (c + border) * box, (r + border) * box
                for x in range(x0, x0 + box):
                    for y in range(y0, y0 + box):
                        px[x, y] = 0
    img.save(path)
    print(f"QR écrit ({n} modules) -> {path}  pour  {url}")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://github.com/qlambotte/imsv-exos-2026/"
    out = sys.argv[2] if len(sys.argv) > 2 else "img/qr.png"
    make_qr_png(url, out)
