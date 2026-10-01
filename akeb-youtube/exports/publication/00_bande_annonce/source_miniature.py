"""Miniature bande-annonce saison 1 — charte « Les Mystères d'Akeb », sans visage ni photo."""
import sys
import unicodedata
from pathlib import Path

RACINE = Path("/home/user/TradingAgents/akeb-youtube")
sys.path.insert(0, str(RACINE / "outils"))
from PIL import Image, ImageDraw  # noqa: E402
from identite import fond, police, ACCENT, TEXTE, DISCRET, TRAIT, FOND  # noqa: E402

N = lambda s: unicodedata.normalize("NFC", s)
W, H = 1280, 720
img = fond(W, H, graine=5)
d = ImageDraw.Draw(img)

# barre d'accent à gauche (charte)
d.rectangle([0, 0, 18, H], fill=ACCENT)

# surtitre
d.text((70, 58), N("BANDE-ANNONCE"), font=police("bold", 44), fill=ACCENT, anchor="la")

# signature chaîne
d.text((W - 60, 66), N("LES MYSTÈRES D'AKEB"), font=police("semibold", 26), fill=(110, 116, 126), anchor="ra")

# motif : quatre cases reliées (les quatre épisodes) ; la quatrième reste une question
y_c, cote = 200, 92
xs = [70, 380, 690, 1000]
d.line([(xs[0] + cote, y_c), (xs[3], y_c)], fill=TRAIT, width=6)
f_num = police("black", 64)
for i, x in enumerate(xs):
    box = [x, y_c - cote // 2, x + cote, y_c + cote // 2]
    if i < 3:
        d.rounded_rectangle(box, radius=10, fill=FOND, outline=DISCRET, width=5)
        d.text((x + cote / 2, y_c + 2), str(i + 1), font=f_num, fill=DISCRET, anchor="mm")
    else:
        d.rounded_rectangle(box, radius=10, fill=FOND, outline=ACCENT, width=7)
        d.text((x + cote / 2, y_c + 2), "?", font=f_num, fill=ACCENT, anchor="mm")

# titre principal : 3 mots
f1 = police("black", 200)
d.text((62, 300), N("SAISON 1"), font=f1, fill=TEXTE, anchor="la")
f2 = police("black", 168)
d.text((64, 500), N("4 épisodes"), font=f2, fill=ACCENT, anchor="la")

sortie = RACINE / "exports/publication/00_bande_annonce"
img.save(sortie / "miniature.png", optimize=True)
img.resize((168, 94), Image.LANCZOS).save(sortie / "miniature_test_168x94.png")
print((sortie / "miniature.png").stat().st_size)
