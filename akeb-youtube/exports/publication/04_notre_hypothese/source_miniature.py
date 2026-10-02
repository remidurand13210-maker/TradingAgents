"""Miniature épisode 4 — charte « Les Mystères d'Akeb », sans visage ni photo."""
import sys
import unicodedata
from pathlib import Path

RACINE = Path("/home/user/TradingAgents/akeb-youtube")
sys.path.insert(0, str(RACINE / "outils"))
from PIL import Image, ImageDraw  # noqa: E402
from identite import fond, police, ACCENT, TEXTE, DISCRET, TRAIT, FOND  # noqa: E402

N = lambda s: unicodedata.normalize("NFC", s)
W, H = 1280, 720
img = fond(W, H, graine=44)
d = ImageDraw.Draw(img)

# barre d'accent à gauche (charte)
d.rectangle([0, 0, 18, H], fill=ACCENT)

# surtitre
d.text((70, 58), N("ÉPISODE 4 · HYPOTHÈSE"), font=police("bold", 44), fill=ACCENT, anchor="la")

# signature chaîne
d.text((W - 60, 66), N("LES MYSTÈRES D'AKEB"), font=police("semibold", 26), fill=(110, 116, 126), anchor="ra")

# motif : la dernière trace (15/04/2011), puis trois scénarios A, B, C, aucun tranché
x0, y0 = 92, 215
d.text((x0 - 18, y0 + 34), N("15/04/2011"), font=police("bold", 30), fill=DISCRET, anchor="la")
xf = 400
d.line([(x0, y0), (xf, y0)], fill=TRAIT, width=6)
fa = police("black", 38)
r = 27
for lettre, yy in (("A", 155), ("B", 215), ("C", 275)):
    xe = 660
    d.line([(xf, y0), (xe - r, yy)], fill=TRAIT, width=6)
    d.ellipse([xe - r, yy - r, xe + r, yy + r], fill=FOND, outline=DISCRET, width=5)
    d.text((xe, yy + 2), lettre, font=fa, fill=DISCRET, anchor="mm")
d.ellipse([x0 - 16, y0 - 16, x0 + 16, y0 + 16], fill=TEXTE)
# point d'interrogation ambre à l'embranchement : rien n'est démontré
d.ellipse([xf - 26, y0 - 26, xf + 26, y0 + 26], fill=FOND, outline=ACCENT, width=6)
d.text((xf, y0 + 2), "?", font=police("black", 40), fill=ACCENT, anchor="mm")

# titre principal : la question de l'épisode, posée et non tranchée
f1 = police("black", 190)
d.text((62, 318), N("MORT"), font=f1, fill=TEXTE, anchor="la")
f2 = police("black", 142)
d.text((64, 500), N("ou en fuite ?"), font=f2, fill=ACCENT, anchor="la")

sortie = RACINE / "exports/publication/04_notre_hypothese"
img.save(sortie / "miniature.png", optimize=True)
img.resize((168, 94), Image.LANCZOS).save(sortie / "miniature_test_168x94.png")
print((sortie / "miniature.png").stat().st_size)
