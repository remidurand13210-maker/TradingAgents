"""Miniature épisode 2 — charte « Les Mystères d'Akeb », sans visage ni photo."""
import sys
import unicodedata
from pathlib import Path

RACINE = Path("/home/user/TradingAgents/akeb-youtube")
sys.path.insert(0, str(RACINE / "outils"))
from PIL import Image, ImageDraw  # noqa: E402
from identite import fond, police, ACCENT, TEXTE, DISCRET, TRAIT, FOND  # noqa: E402

N = lambda s: unicodedata.normalize("NFC", s)
W, H = 1280, 720
img = fond(W, H, graine=22)
d = ImageDraw.Draw(img)

# barre d'accent à gauche (charte)
d.rectangle([0, 0, 18, H], fill=ACCENT)

# surtitre
d.text((70, 58), N("ÉPISODE 2 · AVRIL 2011"), font=police("bold", 44), fill=ACCENT, anchor="la")

# signature chaîne
d.text((W - 60, 66), N("LES MYSTÈRES D'AKEB"), font=police("semibold", 26), fill=(110, 116, 126), anchor="ra")


def enveloppe(x0, y0, w, h, couleur, epais, etiquette, fonte):
    """Enveloppe schématique (rectangle + rabat en V) et sa destination annoncée."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=FOND, outline=couleur, width=epais)
    d.line([(x0, y0), (x0 + w // 2, y0 + int(h * 0.58)), (x0 + w, y0)], fill=couleur, width=epais, joint="curve")
    d.text((x0 + w + 26, y0 + h // 2), N(etiquette), font=fonte, fill=couleur, anchor="lm")


# motif : deux courriers partis en même temps, deux destinations annoncées
fe = police("bold", 40)
enveloppe(70, 168, 116, 72, DISCRET, 5, "AUSTRALIE", fe)
d.text((560, 204), "≠", font=police("black", 64), fill=DISCRET, anchor="mm")
enveloppe(650, 168, 116, 72, ACCENT, 6, "ÉTATS-UNIS", fe)

# titre principal : « un départ, deux versions » (titre du chapitre 3)
f1 = police("black", 168)
d.text((62, 318), N("UN DÉPART"), font=f1, fill=TEXTE, anchor="la")
f2 = police("black", 142)
d.text((64, 500), N("deux versions"), font=f2, fill=ACCENT, anchor="la")

sortie = RACINE / "exports/publication/02_avril_2011"
img.save(sortie / "miniature.png", optimize=True)
img.resize((168, 94), Image.LANCZOS).save(sortie / "miniature_test_168x94.png")
print((sortie / "miniature.png").stat().st_size)
