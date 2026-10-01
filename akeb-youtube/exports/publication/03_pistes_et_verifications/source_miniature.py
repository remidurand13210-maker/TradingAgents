"""Miniature épisode 3 — charte « Les Mystères d'Akeb », sans visage ni photo."""
import sys
import unicodedata
from pathlib import Path

RACINE = Path("/home/user/TradingAgents/akeb-youtube")
sys.path.insert(0, str(RACINE / "outils"))
from PIL import Image, ImageDraw  # noqa: E402
from identite import fond, police, ACCENT, TEXTE, DISCRET, TRAIT, FOND  # noqa: E402

N = lambda s: unicodedata.normalize("NFC", s)
W, H = 1280, 720
img = fond(W, H, graine=33)
d = ImageDraw.Draw(img)

# barre d'accent à gauche (charte)
d.rectangle([0, 0, 18, H], fill=ACCENT)

# surtitre
d.text((70, 58), N("ÉPISODE 3"), font=police("bold", 44), fill=ACCENT, anchor="la")

# signature chaîne
d.text((W - 60, 66), N("LES MYSTÈRES D'AKEB"), font=police("semibold", 26), fill=(110, 116, 126), anchor="ra")

# motif : une rangée de pistes vérifiées (cercles barrés), la dernière encore ouverte (cercle ambre « ? »)
y_p, r = 205, 34
xs = [70 + r + i * 142 for i in range(8)]
d.line([(xs[0], y_p), (xs[-1], y_p)], fill=TRAIT, width=6)
for i, x in enumerate(xs):
    if i < len(xs) - 1:
        d.ellipse([x - r, y_p - r, x + r, y_p + r], fill=FOND, outline=DISCRET, width=5)
        k = 14
        d.line([(x - k, y_p - k), (x + k, y_p + k)], fill=DISCRET, width=6)
        d.line([(x - k, y_p + k), (x + k, y_p - k)], fill=DISCRET, width=6)
    else:
        d.ellipse([x - r - 4, y_p - r - 4, x + r + 4, y_p + r + 4], fill=FOND, outline=ACCENT, width=7)
        d.text((x, y_p + 2), "?", font=police("black", 56), fill=ACCENT, anchor="mm")

# titre principal : « plus de 1 850 signalements » (Le Parisien, 02/06/2026)
f0 = police("bold", 52)
d.text((70, 282), N("PLUS DE"), font=f0, fill=DISCRET, anchor="la")
f1 = police("black", 190)
d.text((62, 318), N("1 850"), font=f1, fill=TEXTE, anchor="la")
f2 = police("black", 142)
d.text((64, 500), N("signalements"), font=f2, fill=ACCENT, anchor="la")

sortie = RACINE / "exports/publication/03_pistes_et_verifications"
img.save(sortie / "miniature.png", optimize=True)
img.resize((168, 94), Image.LANCZOS).save(sortie / "miniature_test_168x94.png")
print((sortie / "miniature.png").stat().st_size)
