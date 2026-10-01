"""Identité visuelle « Les Mystères d'Akeb » : cartons, frise, cartes, miniatures.

Tous les visuels sont originaux (texte, formes, fond de carte Natural Earth
du domaine public). Aucun portrait, aucune photo de presse, aucun document
imitant une pièce de police.
"""
from __future__ import annotations

import json
import math
import random
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = Path(__file__).resolve().parent
POLICES = ICI / "polices"
DONNEES = ICI / "donnees"

# Palette : fond presque noir, texte ivoire, un seul accent ambre.
FOND = (14, 17, 22)
PANNEAU = (24, 29, 37)
TEXTE = (237, 232, 224)
DISCRET = (140, 146, 156)
TRAIT = (60, 66, 76)
ACCENT = (200, 150, 62)

# Étiquettes de statut, désaturées pour rester sobres.
ETIQUETTES = {
    "FAIT": ("FAIT DOCUMENTÉ", (86, 138, 124)),
    "TEMOIGNAGE": ("TÉMOIGNAGE RAPPORTÉ", (112, 124, 170)),
    "RECONSTRUCTION": ("RECONSTITUTION DE L'ENQUÊTE", (104, 132, 150)),
    "HYPOTHESE": ("HYPOTHÈSE", ACCENT),
    "FICTION": ("FICTION", (168, 84, 84)),
    "SYNTHESE": ("DOCUMENT DE SYNTHÈSE — RÉALISÉ PAR LA CHAÎNE", (110, 116, 126)),
}

NBSP = " "


@lru_cache(maxsize=None)
def police(nom: str, taille: int) -> ImageFont.FreeTypeFont:
    fichiers = {
        "regular": "SourceSansPro-Regular.ttf",
        "semibold": "SourceSansPro-Semibold.ttf",
        "bold": "SourceSansPro-Bold.ttf",
        "black": "SourceSansPro-Black.ttf",
        "italic": "SourceSansPro-It.ttf",
        "light": "SourceSansPro-Light.ttf",
        "serif": "LiberationSerif-Regular.ttf",
        "serif-bold": "LiberationSerif-Bold.ttf",
        "serif-italic": "LiberationSerif-Italic.ttf",
    }
    return ImageFont.truetype(str(POLICES / fichiers[nom]), taille)


def typo_fr(texte: str) -> str:
    """Espaces insécables avant : ; ? ! » et après «."""
    for signe in (":", ";", "?", "!", "»"):
        texte = texte.replace(" " + signe, NBSP + signe)
    return texte.replace("« ", "«" + NBSP)


def couper(texte: str, fnt: ImageFont.FreeTypeFont, largeur: int) -> list[str]:
    lignes: list[str] = []
    for paragraphe in texte.split("\n"):
        mots = paragraphe.split(" ")
        courante = ""
        for mot in mots:
            essai = (courante + " " + mot).strip()
            if fnt.getlength(essai) <= largeur or not courante:
                courante = essai
            else:
                lignes.append(courante)
                courante = mot
        lignes.append(courante)
    return lignes


def ajuster(texte: str, nom: str, taille_max: int, largeur: int, lignes_max: int, taille_min: int = 28):
    """Réduit la taille jusqu'à tenir dans lignes_max lignes."""
    taille = taille_max
    while taille >= taille_min:
        fnt = police(nom, taille)
        lignes = couper(texte, fnt, largeur)
        if len(lignes) <= lignes_max:
            return fnt, lignes
        taille -= 2
    fnt = police(nom, taille_min)
    return fnt, couper(texte, fnt, largeur)


@lru_cache(maxsize=8)
def _fond_cache(w: int, h: int, graine: int) -> Image.Image:
    img = Image.new("RGB", (w, h), FOND)
    px = img.load()
    cx, cy = w / 2, h * 0.45
    rmax = math.hypot(cx, cy)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = math.hypot(x - cx, y - cy) / rmax
            k = 1.0 + 0.55 * (1 - d) ** 2
            c = tuple(min(255, int(v * k)) for v in FOND)
            px[x, y] = c
            if x + 1 < w:
                px[x + 1, y] = c
            if y + 1 < h:
                px[x, y + 1] = c
                if x + 1 < w:
                    px[x + 1, y + 1] = c
    rnd = random.Random(graine)
    grain = Image.new("L", (w // 2, h // 2))
    grain.putdata([rnd.randint(0, 255) for _ in range((w // 2) * (h // 2))])
    grain = grain.resize((w, h)).filter(ImageFilter.GaussianBlur(0.6))
    bruit = Image.merge("RGB", (grain, grain, grain))
    return Image.blend(img, bruit, 0.035)


def fond(w: int = 1920, h: int = 1080, graine: int = 7) -> Image.Image:
    return _fond_cache(w, h, graine).copy()


def etiquette(d: ImageDraw.ImageDraw, x: int, y: int, cle: str, echelle: float = 1.0) -> int:
    texte, couleur = ETIQUETTES[cle]
    fnt = police("bold", int(26 * echelle))
    tw = fnt.getlength(texte)
    pad_x, h = int(18 * echelle), int(44 * echelle)
    d.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + h], radius=int(6 * echelle), outline=couleur, width=max(2, int(2 * echelle)))
    d.text((x + pad_x, y + h / 2), texte, font=fnt, fill=couleur, anchor="lm")
    return int(tw + 2 * pad_x)


def ligne_source(d: ImageDraw.ImageDraw, w: int, h: int, source: str, faits: str = "") -> None:
    """Bandeau bas : date et origine de la source, date des faits."""
    if not source and not faits:
        return
    fnt = police("regular", 26)
    y = h - 70
    d.line([(120, y - 22), (w - 120, y - 22)], fill=TRAIT, width=1)
    morceaux = []
    if source:
        morceaux.append("Source : " + source)
    if faits:
        morceaux.append("Faits : " + faits)
    texte = typo_fr("   ·   ".join(morceaux))
    while fnt.getlength(texte) > w - 240 and fnt.size > 18:
        fnt = police("regular", fnt.size - 1)
    d.text((120, y + 8), texte, font=fnt, fill=DISCRET, anchor="lm")


def filigrane(d: ImageDraw.ImageDraw, w: int, h: int) -> None:
    fnt = police("semibold", 22)
    d.text((w - 60, 50), "LES MYSTÈRES D'AKEB", font=fnt, fill=(92, 98, 108), anchor="ra")


# ---------------------------------------------------------------- cartons 16:9

def carton_titre(numero: str, titre: str, sous_titre: str = "", w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    if numero and numero not in ("—", "-"):
        d.text((w / 2, h * 0.30), f"ÉPISODE {numero}", font=police("semibold", 34), fill=ACCENT, anchor="mm")
    fnt, lignes = ajuster(typo_fr(titre), "bold", 92, w - 360, 3)
    y = h * 0.44
    for l in lignes:
        d.text((w / 2, y), l, font=fnt, fill=TEXTE, anchor="mm")
        y += fnt.size * 1.12
    if sous_titre:
        f2, l2 = ajuster(typo_fr(sous_titre), "light", 40, w - 480, 2)
        y += 20
        for l in l2:
            d.text((w / 2, y), l, font=f2, fill=DISCRET, anchor="mm")
            y += f2.size * 1.25
    d.line([(w / 2 - 60, h * 0.22), (w / 2 + 60, h * 0.22)], fill=ACCENT, width=3)
    return img


def carton_chapitre(numero: str, titre: str, w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    filigrane(d, w, h)
    d.text((160, h / 2 - 70), numero, font=police("light", 60), fill=ACCENT, anchor="ls")
    fnt, lignes = ajuster(typo_fr(titre), "bold", 84, w - 420, 2)
    y = h / 2 + 10
    for l in lignes:
        d.text((160, y), l, font=fnt, fill=TEXTE, anchor="ls")
        y += fnt.size * 1.1
    d.line([(160, h / 2 - 40), (360, h / 2 - 40)], fill=ACCENT, width=3)
    return img


def carton_date(date_txt: str, lieu: str = "", precision: str = "", statut: str = "", source: str = "", faits: str = "", w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    filigrane(d, w, h)
    if statut:
        etiquette(d, 120, 110, statut)
    fnt, lignes = ajuster(typo_fr(date_txt), "black", 150, w - 300, 2, 70)
    y = h * 0.40
    for l in lignes:
        d.text((w / 2, y), l, font=fnt, fill=TEXTE, anchor="mm")
        y += fnt.size * 1.05
    if lieu:
        f2, l2 = ajuster(typo_fr(lieu), "semibold", 52, w - 400, 2)
        y += 10
        for l in l2:
            d.text((w / 2, y), l, font=f2, fill=ACCENT, anchor="mm")
            y += f2.size * 1.2
    if precision:
        f3, l3 = ajuster(typo_fr(precision), "italic", 36, w - 500, 2)
        y += 14
        for l in l3:
            d.text((w / 2, y), l, font=f3, fill=DISCRET, anchor="mm")
            y += f3.size * 1.25
    ligne_source(d, w, h, source, faits)
    return img


def carton_texte(texte: str, statut: str = "", source: str = "", faits: str = "", titre: str = "", w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    filigrane(d, w, h)
    y0 = 120
    if statut:
        etiquette(d, 160, y0, statut)
        y0 += 90
    if titre:
        ft, lt = ajuster(typo_fr(titre), "semibold", 44, w - 320, 2)
        for l in lt:
            d.text((160, y0), l, font=ft, fill=ACCENT, anchor="la")
            y0 += ft.size * 1.2
        y0 += 20
    zone_h = h - y0 - 170
    fnt, lignes = ajuster(typo_fr(texte), "regular", 64, w - 320, max(2, int(zone_h / 80)), 34)
    hauteur = len(lignes) * fnt.size * 1.28
    y = y0 + max(0, (zone_h - hauteur) / 2)
    for l in lignes:
        d.text((160, y), l, font=fnt, fill=TEXTE, anchor="la")
        y += fnt.size * 1.28
    ligne_source(d, w, h, source, faits)
    return img


def carton_citation(citation: str, auteur: str, statut: str = "TEMOIGNAGE", source: str = "", faits: str = "", w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    filigrane(d, w, h)
    if statut:
        etiquette(d, 160, 120, statut)
    d.text((150, 250), "«", font=police("serif-bold", 220), fill=ACCENT, anchor="la")
    fnt, lignes = ajuster(typo_fr(citation), "serif-italic", 66, w - 440, 5, 36)
    y = 330
    for l in lignes:
        d.text((300, y), l, font=fnt, fill=TEXTE, anchor="la")
        y += fnt.size * 1.3
    f2, l2 = ajuster("— " + typo_fr(auteur), "semibold", 38, w - 520, 2)
    y += 30
    for l in l2:
        d.text((300, y), l, font=f2, fill=DISCRET, anchor="la")
        y += f2.size * 1.25
    ligne_source(d, w, h, source, faits)
    return img


def carton_question(question: str, surtitre: str = "LA QUESTION", w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    filigrane(d, w, h)
    d.text((w / 2, h * 0.30), surtitre, font=police("semibold", 34), fill=ACCENT, anchor="mm")
    fnt, lignes = ajuster(typo_fr(question), "bold", 84, w - 360, 4, 44)
    y = h * 0.52 - (len(lignes) - 1) * fnt.size * 0.6
    for l in lignes:
        d.text((w / 2, y), l, font=fnt, fill=TEXTE, anchor="mm")
        y += fnt.size * 1.18
    return img


def carton_document(titre: str, lignes_doc: list[str], source: str = "", w=1920, h=1080) -> Image.Image:
    """Tableau de synthèse original, explicitement signé par la chaîne."""
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    filigrane(d, w, h)
    etiquette(d, 160, 100, "SYNTHESE")
    x0, y0, x1 = 160, 190, w - 160
    ft, lt = ajuster(typo_fr(titre), "bold", 56, x1 - x0 - 80, 2)
    y = y0 + 40
    d.rounded_rectangle([x0, y0, x1, h - 150], radius=10, fill=PANNEAU, outline=TRAIT, width=2)
    for l in lt:
        d.text((x0 + 50, y), l, font=ft, fill=TEXTE, anchor="la")
        y += ft.size * 1.15
    y += 20
    d.line([(x0 + 50, y), (x1 - 50, y)], fill=TRAIT, width=2)
    y += 30
    dispo = h - 190 - y
    taille = 40
    while taille > 26:
        fnt = police("regular", taille)
        blocs = [couper(typo_fr(t), fnt, x1 - x0 - 150) for t in lignes_doc]
        if sum(len(b) for b in blocs) * taille * 1.3 + len(blocs) * 14 <= dispo:
            break
        taille -= 2
    fnt = police("regular", taille)
    blocs = [couper(typo_fr(t), fnt, x1 - x0 - 150) for t in lignes_doc]
    for bloc in blocs:
        d.ellipse([x0 + 55, y + taille * 0.45, x0 + 67, y + taille * 0.45 + 12], fill=ACCENT)
        for l in bloc:
            d.text((x0 + 90, y), l, font=fnt, fill=TEXTE, anchor="la")
            y += taille * 1.3
        y += 14
    ligne_source(d, w, h, source)
    return img


# Frise commune de la saison : elle progresse d'un épisode à l'autre.
FRISE_BORNES = (1961, 2027)


MOIS = ["janv.", "févr.", "mars", "avril", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]


def carton_frise(evenements: list[dict], focus: tuple[int, int] | None = None, titre: str = "", curseur: float | None = None, bornes: tuple[float, float] | None = None, w=1920, h=1080) -> Image.Image:
    """evenements : [{"annee": 1961.4, "label": "Naissance", "statut": "FAIT", "haut": True}]"""
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    filigrane(d, w, h)
    if titre:
        d.text((160, 120), typo_fr(titre), font=police("semibold", 44), fill=ACCENT, anchor="la")
    a0, a1 = bornes or FRISE_BORNES
    evenements = [e for e in evenements if a0 <= e["annee"] <= a1]
    x0, x1, ya = 160, w - 160, h * 0.56

    def X(annee: float) -> float:
        return x0 + (annee - a0) / (a1 - a0) * (x1 - x0)

    if focus:
        d.rectangle([X(focus[0]), ya - 250, X(focus[1]), ya + 250], fill=(26, 31, 40))
    d.line([(x0, ya), (x1, ya)], fill=TRAIT, width=4)
    if a1 - a0 > 8:
        pas = 10 if a1 - a0 <= 80 else 20
        for dec in range(int(a0 // pas * pas), int(a1) + 1, pas):
            if a0 <= dec <= a1:
                d.line([(X(dec), ya - 10), (X(dec), ya + 10)], fill=DISCRET, width=2)
                d.text((X(dec), ya + 34), str(dec), font=police("regular", 26), fill=DISCRET, anchor="mm")
    else:  # frise zoomée : graduations mensuelles
        m = int(a0 * 12)
        while m / 12 <= a1:
            if m / 12 >= a0:
                d.line([(X(m / 12), ya - 8), (X(m / 12), ya + 8)], fill=DISCRET, width=2)
                d.text((X(m / 12), ya + 34), f"{MOIS[m % 12]} {m // 12}", font=police("regular", 22), fill=DISCRET, anchor="mm")
            m += 1
    fnt = police("semibold", 28)
    places: list[tuple[float, float, bool]] = []
    for ev in sorted(evenements, key=lambda e: e["annee"]):
        x = X(ev["annee"])
        couleur = ETIQUETTES.get(ev.get("statut", "FAIT"), ("", TEXTE))[1]
        haut = ev.get("haut", True)
        niveau = 0
        for (px, pn, ph) in places:
            if ph == haut and abs(px - x) < 230:
                niveau = max(niveau, pn + 1)
        places.append((x, niveau, haut))
        dy = 70 + niveau * 62
        yt = ya - dy if haut else ya + dy + 30
        d.line([(x, ya), (x, yt + (18 if haut else -18))], fill=couleur, width=2)
        d.ellipse([x - 9, ya - 9, x + 9, ya + 9], fill=couleur)
        label = typo_fr(ev["label"])
        demi = fnt.getlength(label) / 2
        xt = min(max(x, 60 + demi), w - 60 - demi)  # étiquette maintenue dans le cadre
        d.text((xt, yt), label, font=fnt, fill=TEXTE, anchor="mb" if haut else "mt")
    if curseur is not None:
        xc = X(curseur)
        d.polygon([(xc - 14, ya + 70), (xc + 14, ya + 70), (xc, ya + 46)], fill=ACCENT)
    # légende des statuts
    lx = 160
    for cle in ("FAIT", "TEMOIGNAGE", "RECONSTRUCTION", "HYPOTHESE"):
        texte, couleur = ETIQUETTES[cle]
        d.ellipse([lx, h - 112, lx + 16, h - 96], fill=couleur)
        d.text((lx + 28, h - 104), texte.capitalize(), font=police("regular", 24), fill=DISCRET, anchor="lm")
        lx += 60 + police("regular", 24).getlength(texte.capitalize()) + 40
    return img


# ------------------------------------------------------------------ cartes

@lru_cache(maxsize=1)
def _pays() -> dict:
    with open(DONNEES / "ne_50m_admin_0_countries.geojson", encoding="utf-8") as f:
        return json.load(f)


def carton_carte(points: list[dict], bbox: tuple[float, float, float, float], titre: str = "", trajet: bool = False, source: str = "", faits: str = "", statut: str = "", progression: float | None = None, w=1920, h=1080) -> Image.Image:
    """Carte schématique. bbox = (lon_min, lat_min, lon_max, lat_max).
    points : [{"lon":..,"lat":..,"label":..,"date":..,"cote":"droite|gauche"}]
    Fond : Natural Earth (domaine public)."""
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    lon0, lat0, lon1, lat1 = bbox
    marge_h, marge_b = 190, 150
    zone_w, zone_h = w - 240, h - marge_h - marge_b
    lat_m = math.radians((lat0 + lat1) / 2)
    ech_x = zone_w / ((lon1 - lon0) * math.cos(lat_m))
    ech_y = zone_h / (lat1 - lat0)
    ech = min(ech_x, ech_y)
    cx_px = 120 + zone_w / 2
    cy_px = marge_h + zone_h / 2
    lonc, latc = (lon0 + lon1) / 2, (lat0 + lat1) / 2

    def P(lon: float, lat: float) -> tuple[float, float]:
        return (cx_px + (lon - lonc) * math.cos(lat_m) * ech, cy_px - (lat - latc) * ech)

    for feat in _pays()["features"]:
        geom = feat["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        focus = feat["properties"].get("NAME") in {p.get("pays") for p in points} | {"France"}
        for poly in polys:
            anneau = poly[0]
            if not any(lon0 - 5 <= x <= lon1 + 5 and lat0 - 5 <= y <= lat1 + 5 for x, y in anneau[:: max(1, len(anneau) // 50)]):
                continue
            pts = [P(x, y) for x, y in anneau]
            d.polygon(pts, fill=(30, 36, 45) if focus else (21, 25, 32), outline=(78, 86, 98) if focus else (45, 50, 58))
    # progression (0→1) : le trajet se dessine et les étapes s'allument une à une
    etapes = (len(points) - 1) * progression if progression is not None else len(points)
    if trajet and len(points) > 1:
        for k, (a, b) in enumerate(zip(points, points[1:])):
            part = min(1.0, max(0.0, etapes - k))
            if part <= 0:
                break
            pa, pb = P(a["lon"], a["lat"]), P(b["lon"], b["lat"])
            d.line([pa, (pa[0] + (pb[0] - pa[0]) * part, pa[1] + (pb[1] - pa[1]) * part)], fill=ACCENT, width=4)
    fnt, fdate = police("semibold", 34), police("regular", 26)
    for i, p in enumerate(points):
        if progression is not None and i > etapes + 1e-6:
            continue
        x, y = P(p["lon"], p["lat"])
        r = 11
        d.ellipse([x - r, y - r, x + r, y + r], fill=ACCENT if trajet or i == len(points) - 1 else TEXTE, outline=FOND, width=3)
        gauche = p.get("cote") == "gauche"
        ax = x - 24 if gauche else x + 24
        anc = "rs" if gauche else "ls"
        d.text((ax, y + 4), typo_fr(p["label"]), font=fnt, fill=TEXTE, anchor=anc)
        if p.get("date"):
            d.text((ax, y + 38), typo_fr(p["date"]), font=fdate, fill=DISCRET, anchor=anc)
    x_etiquette = 120
    if titre:
        d.rectangle([0, 0, w, 150], fill=FOND)
        d.text((120, 95), typo_fr(titre), font=police("semibold", 46), fill=TEXTE, anchor="ls")
        x_etiquette = 120 + police("semibold", 46).getlength(typo_fr(titre)) + 40
    if statut:
        etiquette(d, int(x_etiquette), 62 if titre else 60, statut)
    filigrane(d, w, h)
    d.text((w - 120, h - 118), "Carte schématique · fond Natural Earth (domaine public)", font=police("regular", 22), fill=(96, 102, 112), anchor="rs")
    ligne_source(d, w, h, source, faits)
    return img


# ---------------------------------------------------------------- promotion

def carton_livre(couverture: Path | None, lignes: list[str], w=1920, h=1080) -> Image.Image:
    """Carton de promotion : THRILLER DE FICTION, couverture exacte si fournie."""
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    d.text((w * 0.60, 170), "THRILLER DE FICTION", font=police("bold", 40), fill=ETIQUETTES["FICTION"][1], anchor="mm")
    cw, ch = 540, 810
    x, y = 190, (h - ch) // 2
    if couverture and Path(couverture).exists():
        cov = Image.open(couverture).convert("RGB")
        cov.thumbnail((cw, ch))
        img.paste(cov, (x + (cw - cov.width) // 2, y + (ch - cov.height) // 2))
    else:
        d.rectangle([x, y, x + cw, y + ch], outline=ACCENT, width=3)
        d.text((x + cw / 2, y + ch / 2), "COUVERTURE\nAKEB\n(à insérer)", font=police("semibold", 40), fill=ACCENT, anchor="mm", align="center")
    d.text((w * 0.60, 330), "La dernière correction", font=police("serif-bold", 84), fill=TEXTE, anchor="mm")
    d.text((w * 0.60, 420), "un roman d'Akeb", font=police("serif-italic", 48), fill=DISCRET, anchor="mm")
    y2 = 540
    for l in lignes:
        fnt, ls = ajuster(typo_fr(l), "regular", 42, 900, 2)
        for s in ls:
            d.text((w * 0.60, y2), s, font=fnt, fill=TEXTE, anchor="mm")
            y2 += fnt.size * 1.3
        y2 += 16
    d.text((w * 0.60, h - 130), "Personnages inventés · fin imaginée", font=police("italic", 32), fill=DISCRET, anchor="mm")
    return img


def carton_avertissement(w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    lignes = [
        "Chaîne indépendante, liée à l'auteur Akeb.",
        "Ni service de police, ni enquête officielle, ni émission de télévision.",
        "Aucune autorisation ni caution des familles.",
        "Faits sourcés · témoignages attribués · hypothèses signalées.",
        "Narration par voix de synthèse.",
    ]
    y = h * 0.30
    for i, l in enumerate(lignes):
        fnt = police("semibold" if i == 0 else "regular", 46 if i == 0 else 40)
        d.text((w / 2, y), typo_fr(l), font=fnt, fill=TEXTE if i == 0 else DISCRET, anchor="mm")
        y += 82
    d.line([(w / 2 - 60, h * 0.22), (w / 2 + 60, h * 0.22)], fill=ACCENT, width=3)
    return img


def carton_sources(titre: str, sources: list[str], w=1920, h=1080) -> Image.Image:
    img = fond(w, h)
    d = ImageDraw.Draw(img)
    d.text((160, 120), titre, font=police("bold", 54), fill=TEXTE, anchor="la")
    fnt = police("regular", 30)
    y = 220
    for s in sources:
        for l in couper(typo_fr(s), fnt, w - 360):
            if y > h - 120:
                break
            d.text((180, y), l, font=fnt, fill=DISCRET, anchor="la")
            y += 40
        y += 10
    return img


# ------------------------------------------------------------------ chaîne

def avatar(taille=800) -> Image.Image:
    img = fond(taille, taille, graine=3)
    d = ImageDraw.Draw(img)
    c = taille / 2
    r = taille * 0.40
    d.ellipse([c - r, c - r, c + r, c + r], outline=ACCENT, width=max(4, taille // 120))
    d.text((c, c - taille * 0.03), "M", font=police("serif-bold", int(taille * 0.42)), fill=TEXTE, anchor="mm")
    d.text((c, c + taille * 0.22), "D'AKEB", font=police("semibold", int(taille * 0.075)), fill=ACCENT, anchor="mm")
    return img


def banniere(w=2560, h=1440) -> Image.Image:
    """Zone sûre YouTube (tous appareils) : 1546 x 423 centrée."""
    img = fond(w, h, graine=5)
    d = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    d.text((cx, cy - 70), "LES MYSTÈRES D'AKEB", font=police("black", 118), fill=TEXTE, anchor="mm")
    d.text((cx, cy + 32), typo_fr("Disparitions, récits et zones d'ombre."), font=police("light", 54), fill=DISCRET, anchor="mm")
    d.text((cx, cy + 118), "FAITS SOURCÉS  ·  HYPOTHÈSES SIGNALÉES  ·  FICTION ASSUMÉE", font=police("semibold", 36), fill=ACCENT, anchor="mm")
    return img


def miniature(numero: str, haut: str, bas: str, accent_mot: str = "", w=1280, h=720) -> Image.Image:
    """Miniature sobre : gros titre, un mot en accent, pas de visage."""
    img = fond(w, h, graine=11)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 18, h], fill=ACCENT)
    d.text((70, 70), f"XDDL · ÉPISODE {numero}", font=police("bold", 40), fill=ACCENT, anchor="la")
    fnt, lignes = ajuster(typo_fr(haut), "black", 124, w - 140, 3, 70)
    y = 150
    for l in lignes:
        mots = l.split(" ")
        x = 70
        for m in mots:
            couleur = ACCENT if accent_mot and m.strip("?!.,:«»").lower() == accent_mot.lower() else TEXTE
            d.text((x, y), m, font=fnt, fill=couleur, anchor="la")
            x += fnt.getlength(m + " ")
        y += fnt.size * 1.02
    if bas:
        f2, l2 = ajuster(typo_fr(bas), "semibold", 46, w - 140, 2)
        y = h - 70 - len(l2) * f2.size * 1.15
        for l in l2:
            d.text((70, y), l, font=f2, fill=DISCRET, anchor="la")
            y += f2.size * 1.15
    d.text((w - 40, h - 36), "LES MYSTÈRES D'AKEB", font=police("semibold", 24), fill=(110, 116, 126), anchor="rs")
    return img


if __name__ == "__main__":
    import sys

    sortie = Path(sys.argv[1] if len(sys.argv) > 1 else ICI.parent / "chaine" / "visuels")
    sortie.mkdir(parents=True, exist_ok=True)
    avatar().save(sortie / "avatar_800.png")
    banniere().save(sortie / "banniere_2560x1440.png")
    carton_avertissement().save(sortie / "exemple_avertissement.png")
    print("ok", sortie)
