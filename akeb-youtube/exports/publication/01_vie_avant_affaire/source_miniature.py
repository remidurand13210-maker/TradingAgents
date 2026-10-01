"""Miniature épisode 1 — charte « Les Mystères d'Akeb », sans visage ni photo."""
import sys
import random
import unicodedata
from pathlib import Path

RACINE = Path("/home/user/TradingAgents/akeb-youtube")
sys.path.insert(0, str(RACINE / "outils"))
from PIL import Image, ImageDraw  # noqa: E402
from identite import fond, police, ACCENT, TEXTE, DISCRET, TRAIT  # noqa: E402

N = lambda s: unicodedata.normalize("NFC", s)
W, H = 1280, 720
img = fond(W, H, graine=21)
d = ImageDraw.Draw(img)

# barre d'accent à gauche (charte)
d.rectangle([0, 0, 18, H], fill=ACCENT)

# surtitre
d.text((70, 58), N("ÉPISODE 1"), font=police("bold", 44), fill=ACCENT, anchor="la")

# frise 1961 -> 2010, fissure à la fin (motif graphique, aucun visage)
y_f = 200
x0, x1 = 70, 1210
d.line([(x0, y_f), (x1, y_f)], fill=TRAIT, width=6)
for an, x in ((1961, x0 + 8), (1991, 640), (2010, x1 - 8)):
    d.ellipse([x - 13, y_f - 13, x + 13, y_f + 13], fill=DISCRET if an != 2010 else ACCENT)
    d.text((x, y_f + 26), str(an), font=police("semibold", 34), fill=DISCRET, anchor="ma" if an == 1991 else ("la" if an == 1961 else "ra"))
    if an == 1961:
        pass
# fissure : ligne brisée qui part de 2010 vers le haut et le bas
rnd = random.Random(4)
def fissure(xs, ys, pas, n, sens):
    pts = [(xs, ys)]
    x, y = xs, ys
    for _ in range(n):
        x += rnd.randint(-16, 16)
        y += sens * pas
        pts.append((x, y))
    return pts
for pts, w in ((fissure(1060, y_f, 22, 4, -1), 8), (fissure(1060, y_f, 22, 4, 1), 8)):
    d.line(pts, fill=ACCENT, width=w, joint="curve")

# titre principal : 4 mots
f1 = police("black", 200)
d.text((62, 300), N("AVANT 2011"), font=f1, fill=TEXTE, anchor="la")
f2 = police("black", 168)
d.text((64, 500), N("les fissures"), font=f2, fill=ACCENT, anchor="la")

# signature chaîne
d.text((W - 60, 66), N("LES MYSTÈRES D'AKEB"), font=police("semibold", 26), fill=(110, 116, 126), anchor="ra")

sortie = RACINE / "exports/publication/01_vie_avant_affaire"
img.save(sortie / "miniature.png", optimize=True)
img.resize((168, 94), Image.LANCZOS).save(sortie / "miniature_test_168x94.png")
print((sortie / "miniature.png").stat().st_size)
