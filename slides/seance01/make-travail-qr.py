#!/usr/bin/env python3
"""Change l'adresse du QR de la slide « Au travail » (_travail.md).

    python3 make-travail-qr.py https://qlambotte.github.io/imsv-exos-2026/

Dépendance : pip install "qrcode[pil]"  (la même que make-qr.py). Le QR est écrit en SVG, noir sur blanc,
entre les repères <!--QR--> et <!--/QR--> de _travail.md ; aucune image à gérer."""
import re, sys
from pathlib import Path
import qrcode

if len(sys.argv) != 2:
    sys.exit(__doc__)
url = sys.argv[1]
qr = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(url)
qr.make(fit=True)
m = qr.get_matrix()
n = len(m)
d = ""
for y, row in enumerate(m):
    x = 0
    while x < n:
        if row[x]:
            x2 = x
            while x2 < n and row[x2]:
                x2 += 1
            d += f"M{x} {y}h{x2 - x}v1h-{x2 - x}z"
            x = x2
        else:
            x += 1
svg = (f'<svg class="tv-qr-svg" viewBox="-2 -2 {n + 4} {n + 4}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="QR code du site">'
       f'<rect x="-2" y="-2" width="{n + 4}" height="{n + 4}" fill="#fff"/><path d="{d}" fill="#000" shape-rendering="crispEdges"/></svg>')
p = Path(__file__).with_name("_travail.md")
t = p.read_text(encoding="utf-8")
t2, k = re.subn(r"<!--QR-->.*?<!--/QR-->", lambda _: "<!--QR-->" + svg + "<!--/QR-->", t, flags=re.S)
assert k == 1, "repères <!--QR--> introuvables"
p.write_text(t2, encoding="utf-8")
print("QR mis à jour :", url)
