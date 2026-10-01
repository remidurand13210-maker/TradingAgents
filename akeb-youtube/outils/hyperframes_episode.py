"""Rendu d'un épisode avec HyperFrames (HTML/GSAP + Chromium headless), piloté par storyboard.csv.

Usage (même commande pour la bande-annonce et les épisodes 01 à 04) :

    python3 outils/hyperframes_episode.py 00_bande_annonce
    python3 outils/hyperframes_episode.py 01_vie_avant_affaire
    python3 outils/hyperframes_episode.py 01_vie_avant_affaire --exporter      # + copie dans exports/videos/
    python3 outils/hyperframes_episode.py 02_avril_2011 --composition-seule    # HTML seulement, sans rendu MP4

Options : --musique enquete|archives|conclusion (nappe ; défaut selon le numéro d'épisode),
          --workers 3 (processus Chromium), --exporter (copie MP4 + SRT validés dans exports/videos/).

Entrées :
  episodes/<ep>/storyboard.csv          plans (types : avertissement, titre, chapitre, date, texte, citation,
                                        question, document, frise, carte, livre, sources ; photo en option)
  episodes/<ep>/narration.txt           segments [Sxx] et pauses « [pause 1.0] »
  audio/manifest.json                   WAV réels des segments (audio/cache/…), clé « <ep>/<Sxx> »
  audio/config_narration.json           pause_defaut_s (pause entre segments sans [pause])
  audio/musique/nappe_<variante>.wav    régénérée si absente : python3 outils/musique.py … 180 <variante>
  montage/assets/couverture_akeb.png    facultative (type livre) ; repli propre sans couverture

Sorties (hors Git) dans montage/rendu/<ep>/ :
  <ep>.mp4 (1920×1080, 30 i/s, H.264 + AAC 48 kHz, −16 LUFS, crête vraie ≤ −1,5 dBTP),
  <ep>.srt (aligné sur la voix réelle, 2 lignes max), chapitres.txt, timeline.json,
  hyperframes/index.html (+ assets/) : composition générée, rejouable avec `npx hyperframes preview`.

Prérequis (voir REPRISE_ENVIRONNEMENT_AKEB.md) : HyperFrames 0.8.99 et gsap@3 installés dans
/home/user/akeb-hf (variable AKEB_HF pour un autre dossier), télémétrie désactivée, Chromium headless
préinstallé (/opt/pw-browsers/chromium_headless_shell-*/…, variable HYPERFRAMES_BROWSER_PATH).
Aucun appel réseau payant : rendu 100 % local.

Le minutage, l'audio, les SRT et les chapitres réutilisent outils/montage.py (moteur Python de secours).
Contrôle ensuite : python3 outils/controle.py montage/rendu/<ep>/<ep>.mp4 --timeline montage/rendu/<ep>/timeline.json
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import unicodedata
import sys
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import identite as I  # noqa: E402
import montage as M  # noqa: E402
from narration_gemini import charger_json, lire_segments  # noqa: E402

RACINE = M.RACINE
FPS, SR, W, H = 30, M.SR, 1920, 1080
HF = Path(os.environ.get("AKEB_HF", "/home/user/akeb-hf"))
CIBLE_LUFS, CRETE_MAX = -16.0, -1.5
# zone sûre « action » (5 %) : rien ne sort de ce cadre
SUR_X, SUR_Y = 96, 54
MUSIQUE_DEFAUT = {"01": "archives", "02": "enquete", "03": "enquete", "04": "conclusion"}


def sh(cmd: list[str], **kw) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(" ".join(map(str, cmd[:6])) + "…\n" + (r.stdout + r.stderr)[-3000:])
    return r.stdout + r.stderr


def hexa(c: tuple) -> str:
    return "#%02X%02X%02X" % tuple(c[:3])


def q(t: float) -> float:
    """Temps arrondi à l'image."""
    return round(t * FPS) / FPS


# ------------------------------------------------------------------ typographie

POLICES = {  # nom PIL -> (famille CSS, graisse, style, ascendante, descendante)
    "regular": ("SSP", 400, "normal"), "semibold": ("SSP", 600, "normal"), "bold": ("SSP", 700, "normal"),
    "black": ("SSP", 900, "normal"), "light": ("SSP", 300, "normal"), "italic": ("SSP", 400, "italic"),
    "serif": ("LSerif", 400, "normal"), "serif-bold": ("LSerif", 700, "normal"), "serif-italic": ("LSerif", 400, "italic"),
}
LH = 1.2  # interligne CSS des lignes positionnées


def metriques(nom: str) -> tuple[float, float]:
    a, d = I.police(nom, 100).getmetrics()
    return a / 100, d / 100


def haut_ligne(y: float, ancre: str, nom: str, taille: float) -> float:
    """Ordonnée CSS (top) d'une ligne de hauteur LH·taille pour une ancre verticale PIL (a, m, s, b, t)."""
    a, d = metriques(nom)
    demi = (LH - a - d) / 2 * taille
    if ancre == "s":  # ligne de base
        return y - demi - a * taille
    if ancre == "m":
        return y - demi - (a + d) / 2 * taille
    if ancre in ("b",):
        return y - demi - (a + d) * taille
    return y - demi  # « a » / « t » : haut des ascendantes


def esc(t: str) -> str:
    return html.escape(t, quote=True)


def mots(ligne: str, classe: str = "m") -> str:
    """Mots animables ; les espaces insécables (typo_fr) restent dans le mot : « est-il ? » ne se coupe pas."""
    return " ".join(f'<span class="{classe}">{esc(m)}</span>' for m in ligne.split(" ") if m)


def lettres(ligne: str) -> str:
    return "".join('<span class="c">&nbsp;</span>' if ch == " " else f'<span class="c">{esc(ch)}</span>' for ch in ligne)


def ligne(texte_html: str, nom: str, taille: float, y: float, ancre: str = "s", x: float | None = None,
          align: str = "left", couleur=I.TEXTE, extra: str = "", classe: str = "l") -> str:
    fam, poids, style = POLICES[nom]
    top = haut_ligne(y, ancre, nom, taille)
    if align == "center":
        pos = f"left:{SUR_X}px;width:{W - 2 * SUR_X}px;text-align:center;"
        if x is not None and abs(x - W / 2) > 1:
            pos = f"left:{x - 900:.1f}px;width:1800px;text-align:center;"
    elif align == "right":
        pos = f"right:{W - x:.1f}px;text-align:right;"
    else:
        pos = f"left:{x:.1f}px;"
    return (f'<div class="{classe}" style="{pos}top:{top:.1f}px;font:{style} {poids} {taille}px/{LH} {fam};'
            f'color:{hexa(couleur)};{extra}">{texte_html}</div>')


def ajuste(texte: str, nom: str, tmax: int, largeur: int, lmax: int, tmin: int = 28) -> tuple[int, list[str]]:
    fnt, lignes_ = I.ajuster(I.typo_fr(texte), nom, tmax, largeur, lmax, tmin)
    return fnt.size, lignes_


def puce(cle: str, x: float, y: float, echelle: float = 1.0, ident: str = "") -> str:
    texte, c = I.ETIQUETTES[cle]
    ident = f' id="{ident}"' if ident else ""
    return (f'<div class="puce"{ident} style="left:{x}px;top:{y}px;'
            f'color:{hexa(c)};border-color:{hexa(c)};font-size:{26 * echelle:.0f}px">{esc(texte)}</div>')


def statut_valide(s: str) -> str:
    s = (s or "").strip().upper()
    return s if s in I.ETIQUETTES else ""


def bandeau(source: str, faits: str) -> str:
    """Bandeau bas : date de la source et date des faits."""
    if not source and not faits:
        return ""
    morceaux = (["Source : " + source] if source else []) + (["Faits : " + faits] if faits else [])
    texte = I.typo_fr("   ·   ".join(morceaux))
    taille = 26
    while I.police("regular", taille).getlength(texte) > W - 240 and taille > 18:
        taille -= 1
    return (f'<div class="bfilet" style="top:972px"></div>'
            + ligne(esc(texte).replace("   ", "&nbsp;&nbsp; "), "regular", taille, 1000, "m", 120, couleur=I.DISCRET,
                    extra="white-space:pre;", classe="l bas"))


# ------------------------------------------------------------------ gabarits

class Plan:
    """Un plan = un clip HyperFrames (HTML) + ses tweens GSAP (temps absolus)."""

    def __init__(self, i: int, pm: dict, assets: Path, suivant_meme_segment: bool, dernier: bool):
        # texte normalisé NFC : un accent décomposé (e + ◌̀) se détacherait de sa lettre dans l'animation lettre à lettre
        self.p = {k: unicodedata.normalize("NFC", v) if isinstance(v, str) else v for k, v in pm["plan"].items()}
        self.p["params"] = json.loads(unicodedata.normalize("NFC", json.dumps(pm["plan"]["params"], ensure_ascii=False)))
        self.i = i
        self.t0, self.t1 = pm["debut"], pm["fin"]
        self.d = self.t1 - self.t0
        self.par = self.p["params"]
        self.type = self.p["type"].strip()
        self.statut = statut_valide(self.p.get("statut", ""))
        self.anim = self.par.get("anim") or M.ANIM_DEFAUT.get(self.type, "revele")
        self.assets = assets
        self.id = f"p{i:03d}"
        self.html: list[str] = []
        self.js: list[str] = []
        self.dernier = dernier
        self.etapes: list[float] = []  # instants de changement visuel (contrôle du rythme)

    # -- outils d'animation
    def tw(self, sel: str, de: dict, a: dict, t: float, duree: float = 0.5, ease: str = "power2.out", stagger: float = 0):
        a = dict(a, duration=round(duree, 3), ease=ease)
        if stagger:
            a["stagger"] = round(stagger, 3)
        self.js.append(f"tl.fromTo({json.dumps(sel)}, {json.dumps(de)}, {json.dumps(a)}, {t:.3f});")

    def to(self, sel: str, a: dict, t: float, duree: float = 0.5, ease: str = "power2.out"):
        a = dict(a, duration=round(duree, 3), ease=ease)
        self.js.append(f"tl.to({json.dumps(sel)}, {json.dumps(a)}, {t:.3f});")

    def S(self, suffixe: str) -> str:
        return f"#{self.id} {suffixe}"

    def apparait(self, sel: str, t: float, dy: float = 18, duree: float = 0.5):
        self.tw(self.S(sel), {"opacity": 0, "y": dy}, {"opacity": 1, "y": 0}, t, duree)
        self.etapes.append(t)

    def mots_progressifs(self, sel: str, n: int, t: float, fenetre: float, dy: float = 22):
        """Mots qui apparaissent un à un, étalés sur « fenetre » secondes (au plus 0,17 s d'écart)."""
        if n <= 0:
            return
        st = min(0.17, max(0.03, (fenetre - 0.35) / max(1, n)))
        if self.anim == "fixe":
            self.tw(self.S(sel), {"opacity": 0}, {"opacity": 1}, t, 0.6, "power1.out")
        else:
            self.tw(self.S(sel), {"opacity": 0, "y": dy}, {"opacity": 1, "y": 0}, t, 0.35, stagger=st)
        self.etapes.append(t)

    def relances(self, x: float, y0: float, y1: float, deja: int = 1, centre: bool = False):
        """Plan long (> 8 s) : étapes animées internes, une toutes les 4 à 8 s (filet ambre qui progresse :
        vertical à gauche d'un texte aligné à gauche, horizontal sous un texte centré)."""
        n = math.ceil(self.d / 6.5)
        if self.d <= 8 or n <= deja:
            return
        if centre:
            self.html.append(f'<div class="relance h" style="left:{W / 2 - 200:.0f}px;top:{y1 + 10:.0f}px;width:400px;height:3px"></div>')
            prop = "scaleX"
        else:
            self.html.append(f'<div class="relance" style="left:{x}px;top:{y0:.0f}px;width:4px;height:{max(10, y1 - y0):.0f}px"></div>')
            prop = "scaleY"
        for k in range(1, n):
            t = self.t0 + k * self.d / n
            self.to(self.S(".relance"), {prop: k / (n - 1), "opacity": 1}, t, 0.6)
            self.etapes.append(t)

    # -- gabarits par type
    def construire(self) -> None:
        getattr(self, "g_" + self.type, self.g_texte)()

    def g_avertissement(self):
        self.html.append('<div class="filet" style="left:900px;top:236px;width:120px"></div>')
        lignes_ = ["Chaîne indépendante, liée à l'auteur Akeb.",
                   "Ni service de police, ni enquête officielle, ni émission de télévision.",
                   "Aucune autorisation ni caution des familles.",
                   "Faits sourcés · témoignages attribués · hypothèses signalées.",
                   "Narration par voix de synthèse."]
        y = H * 0.30
        for k, l in enumerate(lignes_):
            self.html.append(ligne(esc(I.typo_fr(l)), "semibold" if k == 0 else "regular", 46 if k == 0 else 40, y, "m",
                                   align="center", couleur=I.TEXTE if k == 0 else I.DISCRET, classe=f"l a{k}"))
            y += 82
        self.tw(self.S(".filet"), {"scaleX": 0}, {"scaleX": 1}, self.t0 + 0.1, 0.7)
        pas = min(0.55, (self.d * 0.6) / len(lignes_))
        for k in range(len(lignes_)):
            self.apparait(f".a{k}", self.t0 + 0.25 + k * pas, 14, 0.45)

    def g_titre(self):
        numero = str(self.par.get("numero", "")).strip()
        y_filet = H * 0.22
        self.html.append(f'<div class="filet" style="left:900px;top:{y_filet - 1.5:.0f}px;width:120px"></div>')
        if numero and numero not in ("—", "-", "00", "0"):
            self.html.append(ligne(f"ÉPISODE {esc(numero)}", "semibold", 34, H * 0.30, "m", align="center",
                                   couleur=I.ACCENT, extra="letter-spacing:3px;", classe="l num"))
        taille, lignes_ = ajuste(self.p["texte"], "bold", 104, W - 360, 3)
        y = H * 0.45
        for l in lignes_:
            self.html.append(ligne(lettres(l), "bold", taille, y, "m", align="center", extra="letter-spacing:1px;"))
            y += taille * 1.12
        if self.p.get("texte2"):
            t2, l2 = ajuste(self.p["texte2"], "light", 46, W - 480, 2)
            y += 24
            for l in l2:
                self.html.append(ligne(esc(l), "light", t2, y, "m", align="center", couleur=I.DISCRET, classe="l st"))
                y += t2 * 1.25
        self.tw(self.S(".filet"), {"scaleX": 0}, {"scaleX": 1}, self.t0 + 0.1, 0.8)
        if numero and numero not in ("—", "-", "00", "0"):
            self.apparait(".num", self.t0 + 0.15, 10, 0.4)
        n = sum(len(l) for l in lignes_)
        st = min(0.035, (self.d * 0.35) / max(1, n))
        self.tw(self.S(".c"), {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, self.t0 + 0.2, 0.5, stagger=st)
        if self.p.get("texte2"):
            self.apparait(".st", self.t0 + min(0.9, self.d * 0.35), 16, 0.6)
        self.etapes.append(self.t0)

    def g_chapitre(self):
        numero = str(self.par.get("numero", ""))
        self.html.append(ligne(esc(numero), "light", 60, H / 2 - 70, "s", 160, couleur=I.ACCENT, classe="l num"))
        self.html.append(f'<div class="filet" style="left:160px;top:{H / 2 - 41.5:.0f}px;width:200px;transform-origin:left center"></div>')
        taille, lignes_ = ajuste(self.p["texte"], "bold", 84, W - 420, 2)
        y = H / 2 + 10 + taille * 0.0
        nmots = 0
        for l in lignes_:
            self.html.append(ligne(mots(l), "bold", taille, y + taille * 0.75, "s", 160))
            nmots += len(l.split(" "))
            y += taille * 1.1
        self.tw(self.S(".filet"), {"scaleX": 0}, {"scaleX": 1}, self.t0 + 0.1, 0.8)
        self.apparait(".num", self.t0 + 0.15, 12, 0.45)
        self.mots_progressifs(".m", nmots, self.t0 + 0.4, min(1.6, self.d * 0.45))
        self.relances(130, H / 2 - 120, y + 20)

    def g_date(self):
        if self.statut:
            self.html.append(puce(self.statut, 160, 110))
        taille, lignes_ = ajuste(self.p["texte"], "black", 150, W - 300, 2, 70)
        y = H * 0.40
        for l in lignes_:
            self.html.append(ligne(mots(l), "black", taille, y, "m", align="center", classe="l dt"))
            y += taille * 1.05
        if self.p.get("texte2"):
            t2, l2 = ajuste(self.p["texte2"], "semibold", 52, W - 400, 2)
            y += 10
            for l in l2:
                self.html.append(ligne(esc(l), "semibold", t2, y, "m", align="center", couleur=I.ACCENT, classe="l lieu"))
                y += t2 * 1.2
        if self.par.get("precision"):
            t3, l3 = ajuste(self.par["precision"], "italic", 36, W - 500, 2)
            y += 14
            for l in l3:
                self.html.append(ligne(esc(l), "italic", t3, y, "m", align="center", couleur=I.DISCRET, classe="l prec"))
                y += t3 * 1.25
        self.html.append(bandeau(self.p.get("source", ""), self.p.get("faits", "")))
        if self.statut:
            self.apparait(".puce", self.t0 + 0.1, 0, 0.4)
        nm = sum(len(l.split(" ")) for l in lignes_)
        self.mots_progressifs(".dt .m", nm, self.t0 + 0.2, min(1.0, self.d * 0.3), 34)
        base = self.t0 + min(0.9, self.d * 0.25)
        if self.p.get("texte2"):
            self.apparait(".lieu", base, 16)
        if self.par.get("precision"):
            self.apparait(".prec", base + min(0.6, self.d * 0.15), 12)
        self.apparait(".bas, #%s .bfilet" % self.id, base + 0.3, 0, 0.5)
        self.relances(130, H * 0.40 - 90, y, centre=True)

    def g_texte(self):
        source, faits = self.p.get("source", ""), self.p.get("faits", "")
        if self.p["segment"].strip() in ("", "-") and not self.statut and not source and not faits:
            return self.g_carton()
        y0 = 120
        if self.statut:
            self.html.append(puce(self.statut, 160, y0))
            y0 += 90
        bas = H - 190
        court = len(self.p["texte"]) <= 70
        nom = "semibold" if court else "regular"
        sur = []
        if self.p.get("texte2"):
            t2, sur = ajuste(self.p["texte2"], "semibold", 44, W - 320, 2)
        h_sur = (len(sur) * t2 * 1.2 + 28) if sur else 0
        taille, lignes_ = ajuste(self.p["texte"], nom, 76 if court else 64, W - 320,
                                 max(2, int((bas - y0 - h_sur) / 84)), 34)
        haut = h_sur + len(lignes_) * taille * 1.28
        # surtitre et texte forment un seul bloc, centré verticalement sous l'étiquette
        y = y0 + max(0, (bas - y0 - haut) / 2) if self.statut else max(y0, (H - haut) / 2 - 20)
        for l in sur:
            self.html.append(ligne(esc(l), "semibold", t2, y, "a", 160, couleur=I.ACCENT, classe="l sur"))
            y += t2 * 1.2
        y += 28 if sur else 0
        ytop = y
        nm = 0
        couleurs = {"établi": "FAIT", "fait": "FAIT", "faits": "FAIT", "témoignage": "TEMOIGNAGE", "rapporté": "TEMOIGNAGE",
                    "reconstitution": "RECONSTRUCTION", "hypothèse": "HYPOTHESE", "hypothèses": "HYPOTHESE", "fiction": "FICTION"}
        liste_statuts = "·" in self.p["texte"] and sum(m.lower() in couleurs for m in self.p["texte"].split()) >= 2
        for l in lignes_:
            h_l = mots(l)
            if liste_statuts:  # « Établi · Témoignage rapporté · Hypothèse » : chaque registre à la couleur de son étiquette
                h_l = re.sub(r'<span class="m">([^<]+)</span>', lambda m: (
                    f'<span class="m" style="color:{hexa(I.ETIQUETTES[couleurs[m.group(1).lower()]][1])}">{m.group(1)}</span>'
                    if m.group(1).lower() in couleurs else m.group(0)), h_l)
            self.html.append(ligne(h_l, nom, taille, y, "a", 160, classe="l tx"))
            nm += len(l.split(" "))
            y += taille * 1.28
        self.html.append(bandeau(source, faits))
        if self.statut:
            self.apparait(".puce", self.t0 + 0.1, 0, 0.4)
        if sur:
            self.apparait(".sur", self.t0 + 0.15, 0 if self.anim == "fixe" else 12, 0.45)
        self.mots_progressifs(".tx .m", nm, self.t0 + 0.3, min(2.2, self.d * 0.5))
        self.apparait(".bas, #%s .bfilet" % self.id, self.t0 + min(1.2, self.d * 0.3), 0, 0.5)
        self.relances(130, ytop, y)

    def g_carton(self):
        """Carton muet centré (fin, transitions) : filet ambre, surtitre, phrase."""
        self.html.append('<div class="filet" style="left:900px;top:330px;width:120px"></div>')
        y = 420
        if self.p.get("texte2"):
            t2, l2 = ajuste(self.p["texte2"], "semibold", 40, W - 480, 2)
            for l in l2:
                self.html.append(ligne(esc(l), "semibold", t2, y, "m", align="center", couleur=I.ACCENT,
                                       extra="letter-spacing:2px;", classe="l sur"))
                y += t2 * 1.25
            y += 50
        taille, lignes_ = ajuste(self.p["texte"], "bold", 92, W - 360, 3, 44)
        y += taille * 0.5
        nm = 0
        for l in lignes_:
            self.html.append(ligne(mots(l), "bold", taille, y, "m", align="center", classe="l tx"))
            nm += len(l.split(" "))
            y += taille * 1.15
        self.tw(self.S(".filet"), {"scaleX": 0}, {"scaleX": 1}, self.t0 + 0.1, 0.8)
        if self.p.get("texte2"):
            self.apparait(".sur", self.t0 + 0.2, 12, 0.5)
        self.mots_progressifs(".tx .m", nm, self.t0 + 0.45, min(1.4, self.d * 0.4), 20)

    g_photo = g_texte  # sans visuel enregistré : repli texte

    def g_citation(self):
        statut = self.statut or "TEMOIGNAGE"
        self.html.append(puce(statut, 160, 120))
        self.html.append(ligne("«", "serif-bold", 220, 250, "a", 150, couleur=I.ACCENT, classe="l guil"))
        taille, lignes_ = ajuste(self.p["texte"], "serif-italic", 66, W - 440, 5, 36)
        y = 330
        nm = 0
        for l in lignes_:
            self.html.append(ligne(mots(l), "serif-italic", taille, y, "a", 300, classe="l ci"))
            nm += len(l.split(" "))
            y += taille * 1.3
        y += 30
        if self.p.get("texte2"):
            t2, l2 = ajuste("— " + self.p["texte2"], "semibold", 38, W - 520, 2)
            for l in l2:
                self.html.append(ligne(esc(l), "semibold", t2, y, "a", 300, couleur=I.DISCRET, classe="l aut"))
                y += t2 * 1.25
        self.html.append(bandeau(self.p.get("source", ""), self.p.get("faits", "")))
        self.apparait(".puce", self.t0 + 0.1, 0, 0.4)
        self.apparait(".guil", self.t0 + 0.15, 10, 0.5)
        # révélée en deux temps, puis l'auteur et la source datée
        moitie = max(1, nm // 2)
        st = min(0.12, (self.d * 0.25) / max(1, moitie))
        sel = self.S(".ci .m")
        self.js.append(f"tl.fromTo(Array.from(document.querySelectorAll({json.dumps(sel)})).slice(0,{moitie}), "
                       f"{{opacity:0,y:16}}, {{opacity:1,y:0,duration:0.4,ease:'power2.out',stagger:{st:.3f}}}, {self.t0 + 0.3:.3f});")
        t2 = self.t0 + max(1.2, self.d * 0.35)
        self.js.append(f"tl.fromTo(Array.from(document.querySelectorAll({json.dumps(sel)})).slice({moitie}), "
                       f"{{opacity:0,y:16}}, {{opacity:1,y:0,duration:0.4,ease:'power2.out',stagger:{st:.3f}}}, {t2:.3f});")
        self.etapes += [self.t0 + 0.3, t2]
        if self.p.get("texte2"):
            self.apparait(".aut", t2 + min(1.0, self.d * 0.2), 10)
        self.apparait(".bas, #%s .bfilet" % self.id, t2 + 0.4, 0, 0.5)
        self.relances(130, 330, y, deja=2)

    def g_question(self):
        if self.statut:
            self.html.append(puce(self.statut, 160, 120))
        sur = self.p.get("texte2") or "LA QUESTION"
        self.html.append(ligne(esc(I.typo_fr(sur)), "semibold", 34, H * 0.30, "m", align="center", couleur=I.ACCENT,
                               extra="letter-spacing:3px;", classe="l sur"))
        taille, lignes_ = ajuste(self.p["texte"], "bold", 88, W - 360, 4, 44)
        y = H * 0.52 - (len(lignes_) - 1) * taille * 0.6
        nm = 0
        for l in lignes_:
            self.html.append(ligne(mots(l), "bold", taille, y, "m", align="center", classe="l qu"))
            nm += len(l.split(" "))
            y += taille * 1.18
        if self.statut:
            self.apparait(".puce", self.t0 + 0.1, 0, 0.4)
        self.apparait(".sur", self.t0 + 0.1, 0, 0.4)
        # deux questions (« Est-il mort ? Est-il vivant ? ») : la seconde arrive après la première
        ph = re.split(r"(?<=[?!.])\s+", " ".join(lignes_))
        if len(ph) >= 2 and self.d > 2.5:
            k = len(ph[0].split(" "))
            sel = self.S(".qu .m")
            self.js.append(f"tl.fromTo(Array.from(document.querySelectorAll({json.dumps(sel)})).slice(0,{k}), "
                           f"{{opacity:0,y:24}}, {{opacity:1,y:0,duration:0.4,ease:'power2.out',stagger:0.12}}, {self.t0 + 0.25:.3f});")
            t2 = self.t0 + min(self.d * 0.45, 2.2)
            self.js.append(f"tl.fromTo(Array.from(document.querySelectorAll({json.dumps(sel)})).slice({k}), "
                           f"{{opacity:0,y:24}}, {{opacity:1,y:0,duration:0.4,ease:'power2.out',stagger:0.12}}, {t2:.3f});")
            self.etapes += [self.t0 + 0.25, t2]
        else:
            self.mots_progressifs(".qu .m", nm, self.t0 + 0.25, min(1.6, self.d * 0.45), 24)
        self.relances(130, H * 0.52 - 120, y - taille * 0.4, centre=True)

    def g_document(self):
        self.html.append(puce("SYNTHESE", 160, 100))
        if self.statut:
            larg = I.police("bold", 26).getlength(I.ETIQUETTES["SYNTHESE"][0]) + 36
            self.html.append(puce(self.statut, 160 + larg + 24, 100).replace('class="puce"', 'class="puce p2"'))
        x0, y0, x1, yb = 160, 190, W - 160, H - 150
        self.html.append(f'<div class="panneau" style="left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{yb - y0}px"></div>')
        tt, lt = ajuste(self.p["texte"], "bold", 56, x1 - x0 - 80, 2)
        y = y0 + 40
        for l in lt:
            self.html.append(ligne(esc(l), "bold", tt, y, "a", x0 + 50, classe="l dtit"))
            y += tt * 1.15
        y += 20
        self.html.append(f'<div class="sep" style="left:{x0 + 50}px;top:{y:.0f}px;width:{x1 - x0 - 100}px"></div>')
        y += 30
        rangs = [x.strip() for x in self.p.get("texte2", "").split("|") if x.strip()]
        dispo = H - 190 - y
        taille = 40
        while taille > 26:
            fnt = I.police("regular", taille)
            blocs_ = [I.couper(I.typo_fr(t), fnt, x1 - x0 - 150) for t in rangs]
            if sum(len(b) for b in blocs_) * taille * 1.3 + len(blocs_) * 14 <= dispo:
                break
            taille -= 2
        fnt = I.police("regular", taille)
        blocs_ = [I.couper(I.typo_fr(t), fnt, x1 - x0 - 150) for t in rangs]
        positions = []
        for k, bloc in enumerate(blocs_):
            ya = y
            self.html.append(f'<div class="rang r{k}">')
            self.html.append(f'<div class="pt" style="left:{x0 + 55}px;top:{y + taille * 0.45:.0f}px"></div>')
            for l in bloc:
                self.html.append(ligne(esc(l), "regular", taille, y, "a", x0 + 90))
                y += taille * 1.3
            self.html.append('</div>')
            positions.append((ya, y))
            y += 14
        self.html.append(bandeau(self.p.get("source", ""), self.p.get("faits", "")))
        self.apparait(".puce", self.t0 + 0.1, 0, 0.4)
        self.tw(self.S(".panneau"), {"opacity": 0, "scale": 0.985}, {"opacity": 1, "scale": 1}, self.t0 + 0.1, 0.5)
        self.apparait(".dtit", self.t0 + 0.25, 10)
        self.tw(self.S(".sep"), {"scaleX": 0}, {"scaleX": 1}, self.t0 + 0.4, 0.6)
        self.apparait(".bas, #%s .bfilet" % self.id, self.t0 + 0.6, 0, 0.5)
        # les lignes se révèlent au rythme de la voix ; surlignage ambre de la ligne commentée
        if positions:
            debut, fin = self.t0 + 0.8, self.t0 + max(1.0, self.d * (0.8 if self.anim == "revele_lent" else 0.65))
            pas = (fin - debut) / len(positions)
            ya, yz = positions[0]
            self.html.append(f'<div class="surligne" style="left:{x0 + 30}px;top:{ya - 8:.0f}px;width:{x1 - x0 - 60}px;'
                             f'height:{yz - ya + 10:.0f}px"></div>')
            for k, (ya, yz) in enumerate(positions):
                t = debut + k * pas
                self.apparait(f".r{k}", t, 10, 0.45)
                if k == 0:
                    self.tw(self.S(".surligne"), {"opacity": 0}, {"opacity": 1}, t, 0.4)
                else:
                    self.to(self.S(".surligne"), {"top": ya - 8, "height": yz - ya + 10}, t, 0.45, "power2.inOut")

    def g_frise(self):
        par = self.par
        bornes = tuple(par["bornes"]) if par.get("bornes") else None
        focus = tuple(par["focus"]) if par.get("focus") else None
        cible = par.get("curseur") or par.get("jusqua", 2026.8)
        depart = par.get("curseur_depart") or (bornes[0] if bornes else (focus[0] if focus else cible - 5))
        evs = M.evenements_frise(par)
        a0, a1 = bornes or I.FRISE_BORNES
        evs = sorted([e for e in evs if a0 <= e["annee"] <= a1], key=lambda e: e["annee"])
        if self.anim == "curseur":
            evs = [e for e in evs if e["annee"] <= cible + 1e-6]
        x0, x1, ya = 160, W - 160, H * 0.56

        def X(a: float) -> float:
            return x0 + (a - a0) / (a1 - a0) * (x1 - x0)

        if self.p.get("texte"):
            self.html.append(ligne(esc(I.typo_fr(self.p["texte"])), "semibold", 44, 120, "a", 160, couleur=I.ACCENT, classe="l ftit"))
        if self.statut:
            larg = I.police("semibold", 44).getlength(I.typo_fr(self.p.get("texte", ""))) + 40 if self.p.get("texte") else 0
            self.html.append(puce(self.statut, 160 + larg, 122))
        if focus:
            self.html.append(f'<div class="focus" style="left:{X(focus[0]):.1f}px;top:{ya - 250:.0f}px;'
                             f'width:{X(focus[1]) - X(focus[0]):.1f}px;height:500px"></div>')
        self.html.append(f'<div class="axe" style="left:{x0}px;top:{ya - 2:.0f}px;width:{x1 - x0}px"></div>')
        grad = []
        if a1 - a0 > 8:
            pas = 10 if a1 - a0 <= 80 else 20
            for dec in range(int(a0 // pas * pas), int(a1) + 1, pas):
                if a0 <= dec <= a1:
                    grad.append((X(dec), str(dec), 26))
        else:
            m = int(a0 * 12)
            while m / 12 <= a1:
                if m / 12 >= a0:
                    grad.append((X(m / 12), f"{I.MOIS[m % 12]} {m // 12}", 22))
                m += 1
        grads = ['<div class="grads">']
        for x, lab, tl_ in grad:
            dans = focus and X(focus[0]) - 30 <= x <= X(focus[1]) + 30
            grads.append(f'<div class="tick" style="left:{x - 1:.1f}px;top:{ya - 10:.0f}px"></div>')
            croise = any(abs(x - X(e["annee"])) < 45 for e in evs)  # une tige passe sur ce libellé : fond opaque
            fond_ = ("#1A1F28" if dans else "#12161C") if croise else "transparent"
            grads.append(ligne(f'<span class="annee" style="background:{fond_}">{esc(lab)}</span>',
                               "regular", tl_, ya + 34, "m", x, "center", I.DISCRET))
        grads.append('</div>')
        fnt = I.police("semibold", 28)
        places, jalons, tiges, etiquettes = [], [], [], []
        for k, ev in enumerate(evs):
            x = X(ev["annee"])
            couleur = I.ETIQUETTES.get(ev.get("statut", "FAIT"), ("", I.TEXTE))[1]
            haut = ev.get("haut", True)
            niveau = 0
            for (px, pn, ph) in places:
                if ph == haut and abs(px - x) < 230:
                    niveau = max(niveau, pn + 1)
            places.append((x, niveau, haut))
            dy = 70 + niveau * 62
            yt = ya - dy if haut else ya + dy + 30
            label = I.typo_fr(ev["label"])
            demi = fnt.getlength(label) / 2
            xt = min(max(x, SUR_X + 10 + demi), W - SUR_X - 10 - demi)
            y_tige0, y_tige1 = (yt + 18, ya) if haut else (ya, yt - 18)
            tiges.append(f'<div class="tige t{k}" style="left:{x - 1:.1f}px;top:{y_tige0:.0f}px;height:{y_tige1 - y_tige0:.0f}px;background:{hexa(couleur)};'
                         f'transform-origin:{"bottom" if haut else "top"} center"></div>'
                         f'<div class="pastille p{k}" style="left:{x - 9:.1f}px;top:{ya - 9:.0f}px;background:{hexa(couleur)}"></div>')
            etiquettes.append(ligne(f'<span class="etiq">{esc(label)}</span>', "semibold", 28, yt + (-4 if haut else 4),
                                    "b" if haut else "a", xt, "center", classe=f"l e{k}"))
            jalons.append(ev["annee"])
        # tiges sous les étiquettes : une tige ne barre jamais le libellé d'un autre jalon
        self.html += tiges + grads + etiquettes
        xc0, xc1 = X(depart), X(cible)
        self.html.append(f'<div class="curseur" style="left:{xc0 - 14:.1f}px;top:{ya + 46:.0f}px"></div>')
        # légende des statuts (remontée si un bandeau source occupe le bas)
        source = self.p.get("source", "") or self.p.get("faits", "")
        yl = H - 104 if not source else H - 150
        lx = 160
        self.html.append('<div class="legende">')
        for cle in ("FAIT", "TEMOIGNAGE", "RECONSTRUCTION", "HYPOTHESE"):
            texte, c = I.ETIQUETTES[cle]
            self.html.append(f'<div class="pastille" style="left:{lx}px;top:{yl - 8:.0f}px;width:16px;height:16px;background:{hexa(c)}"></div>')
            self.html.append(ligne(esc(texte.capitalize()), "regular", 24, yl, "m", lx + 28, couleur=I.DISCRET))
            lx += 60 + I.police("regular", 24).getlength(texte.capitalize()) + 40
        self.html.append('</div>')
        self.html.append(bandeau(self.p.get("source", ""), self.p.get("faits", "")))
        # animation : axe, graduations, curseur qui avance, jalons au passage du curseur
        self.apparait(".ftit", self.t0 + 0.1, 0, 0.5)
        if self.statut:
            self.apparait(".puce", self.t0 + 0.2, 0, 0.4)
        if focus:
            self.tw(self.S(".focus"), {"opacity": 0}, {"opacity": 1}, self.t0 + 0.2, 0.8)
        self.tw(self.S(".axe"), {"scaleX": 0}, {"scaleX": 1}, self.t0 + 0.1, 0.9, "power1.inOut")
        self.tw(self.S(".grads"), {"opacity": 0}, {"opacity": 1}, self.t0 + 0.5, 0.5)
        self.tw(self.S(".legende"), {"opacity": 0}, {"opacity": 1}, self.t0 + 0.7, 0.5)
        self.apparait(".bas, #%s .bfilet" % self.id, self.t0 + 0.7, 0, 0.5)
        tc0 = self.t0 + 0.6
        dc = max(0.8, 0.75 * self.d - 0.6) if self.anim == "curseur" else 0.8
        self.tw(self.S(".curseur"), {"opacity": 0, "x": 0}, {"opacity": 1, "x": xc1 - xc0}, tc0, dc, "power1.inOut")
        for k, a in enumerate(jalons):
            if self.anim != "curseur" or a <= depart or abs(cible - depart) < 0.5:
                t = self.t0 + 0.5 + 0.08 * k
            else:
                f = min(1.0, max(0.0, (a - depart) / (cible - depart)))
                p = math.sqrt(f / 2) if f < 0.5 else 1 - math.sqrt((1 - f) / 2)  # inverse de power1.inOut
                t = tc0 + dc * p
            self.tw(self.S(f".p{k}"), {"scale": 0}, {"scale": 1}, t, 0.35, "back.out(2)")
            self.tw(self.S(f".t{k}"), {"scaleY": 0}, {"scaleY": 1}, t + 0.05, 0.3)
            self.tw(self.S(f".e{k}"), {"opacity": 0}, {"opacity": 1}, t + 0.1, 0.4)
            self.etapes.append(t)

    def g_carte(self):
        par = self.par
        points, bbox = par["points"], tuple(par["bbox"])
        trajet = bool(par.get("trajet"))
        lon0, lat0, lon1, lat1 = bbox
        marge_h, marge_b = 190, 150
        zone_w, zone_h = W - 240, H - marge_h - marge_b
        lat_m = math.radians((lat0 + lat1) / 2)
        ech = min(zone_w / ((lon1 - lon0) * math.cos(lat_m)), zone_h / (lat1 - lat0))
        cx_px, cy_px = 120 + zone_w / 2, marge_h + zone_h / 2
        lonc, latc = (lon0 + lon1) / 2, (lat0 + lat1) / 2

        def P(lon, lat):
            return (cx_px + (lon - lonc) * math.cos(lat_m) * ech, cy_px - (lat - latc) * ech)

        nom = "carte_" + hashlib.sha1(json.dumps([bbox, sorted({p.get("pays", "") for p in points})]).encode()).hexdigest()[:10] + ".png"
        if not (self.assets / nom).exists():
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            pays = {p.get("pays") for p in points} | {"France"}
            for feat in I._pays()["features"]:
                geom = feat["geometry"]
                polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
                focus = feat["properties"].get("NAME") in pays
                for poly in polys:
                    anneau = poly[0]
                    if not any(lon0 - 5 <= x <= lon1 + 5 and lat0 - 5 <= y <= lat1 + 5 for x, y in anneau[:: max(1, len(anneau) // 50)]):
                        continue
                    d.polygon([P(x, y) for x, y in anneau], fill=(30, 36, 45) if focus else (21, 25, 32),
                              outline=(78, 86, 98) if focus else (45, 50, 58))
            img.save(self.assets / nom)
        pts = [P(p["lon"], p["lat"]) for p in points]
        self.html.append(f'<div class="cadre" style="transform-origin:50% 52%">')
        self.html.append(f'<div class="carte" style="background-image:url(assets/{nom})"></div>')
        if trajet and len(pts) > 1:
            self.html.append(f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">')
            for k, ((xa, ya), (xb, yb)) in enumerate(zip(pts, pts[1:])):
                lg = math.hypot(xb - xa, yb - ya)
                self.html.append(f'<line class="seg s{k}" x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{hexa(I.ACCENT)}" '
                                 f'stroke-width="4" stroke-linecap="round" stroke-dasharray="{lg:.1f}" stroke-dashoffset="{lg:.1f}"/>')
            self.html.append('</svg>')
        for k, (p, (x, y)) in enumerate(zip(points, pts)):
            couleur = I.ACCENT if trajet or k == len(points) - 1 else I.TEXTE
            gauche = p.get("cote") == "gauche"
            ax = x - 24 if gauche else x + 24
            al = "right" if gauche else "left"
            self.html.append(f'<div class="etape e{k}"><div class="point" style="left:{x - 14:.1f}px;top:{y - 14:.1f}px;background:{hexa(couleur)}"></div>'
                             + ligne(esc(I.typo_fr(p["label"])), "semibold", 34, y + 4, "s", ax, al, extra="white-space:nowrap;text-shadow:0 0 8px #0E1116;")
                             + (ligne(esc(I.typo_fr(p["date"])), "regular", 26, y + 38, "s", ax, al, I.DISCRET,
                                      extra="white-space:nowrap;text-shadow:0 0 8px #0E1116;") if p.get("date") else "")
                             + '</div>')
        self.html.append('</div>')
        titre = I.typo_fr(self.p.get("texte", ""))
        if titre:
            self.html.append('<div class="bande-titre"></div>')
            self.html.append(ligne(esc(titre), "semibold", 46, 95, "s", 120, classe="l ctit"))
        if self.statut:
            xe = 120 + (I.police("semibold", 46).getlength(titre) + 40 if titre else 0)
            self.html.append(puce(self.statut, round(xe), 62 if titre else 60))
        self.html.append(ligne("Carte schématique · fond Natural Earth (domaine public)", "regular", 22, H - 118, "s", W - 120, "right",
                               (96, 102, 112), classe="l credit"))
        self.html.append(bandeau(self.p.get("source", ""), self.p.get("faits", "")))
        # léger zoom, tracé qui se dessine d'étape en étape, chaque point s'allume avec sa date
        self.tw(self.S(".carte"), {"opacity": 0}, {"opacity": 1}, self.t0, 0.6)
        self.tw(self.S(".cadre"), {"scale": 1.0}, {"scale": 1.035}, self.t0, self.d, "none")
        self.apparait(".ctit", self.t0 + 0.15, -10, 0.5)
        if self.statut:
            self.apparait(".puce", self.t0 + 0.3, 0, 0.4)
        self.apparait(".credit, #%s .bas, #%s .bfilet" % (self.id, self.id), self.t0 + 0.5, 0, 0.5)
        n = len(points)
        debut = self.t0 + 0.6
        fen = max(0.6, 0.75 * self.d - 0.6)
        pas = fen / max(1, n - 1) if n > 1 else 0
        if self.anim == "revele":
            pas = min(pas, 0.9)
        for k in range(n):
            t = debut + k * pas
            if trajet and k > 0:  # le segment se trace jusqu'au point suivant
                xa, ya_ = pts[k - 1]
                xb, yb = pts[k]
                lg = math.hypot(xb - xa, yb - ya_)
                self.tw(self.S(f".s{k - 1}"), {"attr": {"stroke-dashoffset": round(lg, 1)}}, {"attr": {"stroke-dashoffset": 0}},
                        t - pas, max(0.3, pas * 0.85), "power1.inOut")
            self.tw(self.S(f".e{k} .point"), {"scale": 0}, {"scale": 1}, t, 0.35, "back.out(2)")
            self.tw(self.S(f".e{k} .l"), {"opacity": 0, "x": -10 if points[k].get("cote") == "gauche" else 10}, {"opacity": 1, "x": 0}, t + 0.1, 0.4)
            self.etapes.append(t)

    def g_livre(self):
        lignes_ = [x.strip() for x in self.p.get("texte", "").split("|") if x.strip()]
        deja = {"la dernière correction", "un roman d'akeb", "un roman d’akeb"}  # titre et sous-titre fixes
        lignes_ = [x for x in lignes_ if x.lower() not in deja]
        cov = RACINE / "montage" / "assets" / "couverture_akeb.png"
        rouge = I.ETIQUETTES["FICTION"][1]
        if cov.exists():
            shutil.copy(cov, self.assets / "couverture_akeb.png")
            self.html.append('<div class="livre-couv"></div>')
            cx, larg = 1310, 900
        else:  # repli propre : pas de couverture, mise en page centrée
            cx, larg = W / 2, 1400
        # « THRILLER DE FICTION » permanent pendant tout le plan
        self.html.append(ligne("THRILLER DE FICTION", "bold", 40, 170, "m", cx, "center", rouge,
                               extra="letter-spacing:2px;", classe="l fic"))
        self.html.append(ligne("La dernière correction", "serif-bold", 84, 330, "m", cx, "center", classe="l lt"))
        self.html.append(ligne("un roman d'Akeb", "serif-italic", 48, 420, "m", cx, "center", I.DISCRET, classe="l la"))
        y2 = 540
        for k, l in enumerate(lignes_):
            t, ls = ajuste(l, "regular", 42, larg, 2)
            for s in ls:
                self.html.append(ligne(esc(s), "regular", t, y2, "m", cx, "center", classe=f"l ll{k}"))
                y2 += t * 1.3
            y2 += 16
        self.html.append(ligne("Personnages inventés · fin imaginée", "italic", 32, H - 130, "m", cx, "center", I.DISCRET, classe="l men"))
        self.tw(self.S(".fic"), {"opacity": 0}, {"opacity": 1}, self.t0, 0.3)  # visible dès la première image
        if cov.exists():
            self.tw(self.S(".livre-couv"), {"opacity": 0, "x": -60}, {"opacity": 1, "x": 0}, self.t0 + 0.1, 0.7)
            self.tw(self.S(".livre-couv"), {"scale": 1.0}, {"scale": 1.03}, self.t0 + 0.8, max(0.5, self.d - 0.8), "none")
        self.apparait(".lt", self.t0 + 0.3, 16)
        self.apparait(".la", self.t0 + 0.5, 16)
        pas = min(1.2, max(0.25, (self.d * 0.6 - 0.8) / max(1, len(lignes_))))
        for k in range(len(lignes_)):
            self.apparait(f".ll{k}", self.t0 + 0.8 + k * pas, 14, 0.45)
        self.apparait(".men", self.t0 + 0.8 + len(lignes_) * pas, 10)

    def g_sources(self):
        self.html.append(ligne(esc(I.typo_fr(self.p.get("texte") or "Sources principales")), "bold", 54, 120, "a", 160, classe="l stit"))
        refs = [x.strip() for x in self.p.get("texte2", "").split("|") if x.strip()]
        ts = 36 if len(refs) <= 8 else 30
        fnt = I.police("regular", ts)
        y, k = 230, 0
        for s in refs:
            for l in I.couper(I.typo_fr(s), fnt, W - 360):
                if y > H - 140:
                    break
                self.html.append(ligne(esc(l), "regular", ts, y, "a", 180, couleur=I.DISCRET, classe="l src"))
                y += ts * 1.35
                k += 1
            y += 10
        self.apparait(".stit", self.t0 + 0.1, 12)
        self.tw(self.S(".src"), {"opacity": 0, "y": 10}, {"opacity": 1, "y": 0}, self.t0 + 0.4, 0.4,
                stagger=min(0.25, max(0.05, (self.d * 0.5) / max(1, k))))
        self.etapes.append(self.t0 + 0.4)

    # -- clip complet
    def rendu(self) -> tuple[str, list[str]]:
        self.construire()
        fi = 0.3 if self.i else 0.6
        fo = 0.6 if self.dernier else 0.25
        js = [f"tl.fromTo('#{self.id}', {{opacity:0}}, {{opacity:1,duration:{fi},ease:'none'}}, {self.t0:.3f});"] + self.js
        js.append(f"tl.to('#{self.id}', {{opacity:0,duration:{fo},ease:'none'}}, {self.t1 - fo:.3f});")
        h = (f'<div id="{self.id}" class="clip plan" data-start="{self.t0:.3f}" data-duration="{self.d:.3f}" data-track-index="1" '
             f'data-plan="{esc(self.p["plan"])}" data-type="{esc(self.type)}">\n' + "\n".join(x for x in self.html if x) + "\n</div>")
        return h, js


CSS = """
@font-face { font-family:"SSP"; src:url("assets/SourceSansPro-Light.ttf"); font-weight:300; }
@font-face { font-family:"SSP"; src:url("assets/SourceSansPro-Regular.ttf"); font-weight:400; }
@font-face { font-family:"SSP"; src:url("assets/SourceSansPro-It.ttf"); font-weight:400; font-style:italic; }
@font-face { font-family:"SSP"; src:url("assets/SourceSansPro-Semibold.ttf"); font-weight:600; }
@font-face { font-family:"SSP"; src:url("assets/SourceSansPro-Bold.ttf"); font-weight:700; }
@font-face { font-family:"SSP"; src:url("assets/SourceSansPro-Black.ttf"); font-weight:900; }
@font-face { font-family:"LSerif"; src:url("assets/LiberationSerif-Regular.ttf"); font-weight:400; }
@font-face { font-family:"LSerif"; src:url("assets/LiberationSerif-Italic.ttf"); font-weight:400; font-style:italic; }
@font-face { font-family:"LSerif"; src:url("assets/LiberationSerif-Bold.ttf"); font-weight:700; }
:root { --fond:#0E1116; --texte:#EDE8E0; --discret:#8C929C; --accent:#C8963E; --trait:#3C424C; --panneau:#181D25; }
html, body { margin:0; padding:0; background:var(--fond); }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; background:var(--fond);
        font-family:"SSP", sans-serif; color:var(--texte); -webkit-font-smoothing:antialiased; }
.clip { position:absolute; inset:0; }
#fond { background:url("assets/fond.png"); z-index:0; }
.plan { z-index:1; }
#filigrane { z-index:5; }
.filigrane { position:absolute; top:56px; right:96px; font:600 22px/1.2 "SSP"; color:#5C626C; letter-spacing:1px; }
.l { position:absolute; white-space:nowrap; }
.m, .c { display:inline-block; }
.puce { position:absolute; border:2px solid; border-radius:6px; padding:0 18px; height:40px; line-height:40px;
        font-family:"SSP"; font-weight:700; letter-spacing:.5px; white-space:nowrap; background:rgba(14,17,22,.55); }
.filet { position:absolute; height:3px; background:var(--accent); transform-origin:center; }
.bfilet { position:absolute; left:120px; width:1680px; height:1px; background:var(--trait); }
.relance { position:absolute; background:var(--accent); transform-origin:top center; transform:scaleY(0); opacity:0; }
.relance.h { transform-origin:center center; transform:scaleX(0); }
.panneau { position:absolute; background:var(--panneau); border:2px solid var(--trait); border-radius:10px; box-sizing:border-box; }
.sep { position:absolute; height:2px; background:var(--trait); transform-origin:left center; }
.pt { position:absolute; width:12px; height:12px; border-radius:50%; background:var(--accent); }
.surligne { position:absolute; background:rgba(200,150,62,.10); border-left:4px solid var(--accent); border-radius:4px; opacity:0; }
.focus { position:absolute; background:#1A1F28; }
.axe { position:absolute; height:4px; background:var(--trait); transform-origin:left center; }
.tick { position:absolute; width:2px; height:20px; background:var(--discret); }
.tige { position:absolute; width:2px; }
.annee { padding:0 4px; }
.etiq { background:rgba(24,29,37,.96); border-radius:4px; padding:2px 10px; }
.pastille { position:absolute; width:18px; height:18px; border-radius:50%; }
.curseur { position:absolute; width:0; height:0; border-left:14px solid transparent; border-right:14px solid transparent;
           border-bottom:24px solid var(--accent); }
.cadre { position:absolute; inset:0; }
.carte { position:absolute; inset:0; background-size:1920px 1080px; }
.point { position:absolute; width:22px; height:22px; border-radius:50%; border:3px solid var(--fond); }
.bande-titre { position:absolute; left:0; top:0; width:1920px; height:150px; background:var(--fond); }
.livre-couv { position:absolute; left:190px; top:135px; width:540px; height:810px; background:url("assets/couverture_akeb.png") center/contain no-repeat;
              box-shadow:0 30px 80px rgba(0,0,0,.6); }
"""


def composition(plans_min: list[dict], total: float, dossier: Path) -> Path:
    assets = dossier / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    if not (assets / "fond.png").exists():
        I.fond().save(assets / "fond.png")
    for f in ["SourceSansPro-Regular", "SourceSansPro-Semibold", "SourceSansPro-Bold", "SourceSansPro-Black", "SourceSansPro-Light",
              "SourceSansPro-It", "LiberationSerif-Regular", "LiberationSerif-Bold", "LiberationSerif-Italic"]:
        shutil.copy(RACINE / "outils" / "polices" / f"{f}.ttf", assets)
    gsap = HF / "node_modules" / "gsap" / "dist" / "gsap.min.js"
    if not gsap.exists():
        raise SystemExit(f"gsap absent ({gsap}) : voir REPRISE_ENVIRONNEMENT_AKEB.md (npm i hyperframes@0.8.99 gsap@3)")
    shutil.copy(gsap, assets)
    clips, js = [], []
    for i, pm in enumerate(plans_min):
        h, j = Plan(i, pm, assets, False, i == len(plans_min) - 1).rendu()
        clips.append(h)
        js += j
    # filigrane discret, masqué sur le carton titre (qui porte déjà le nom de la chaîne)
    for pm in plans_min:
        if pm["plan"]["type"] == "titre":
            js.append(f"tl.to('#filigrane', {{opacity:0,duration:0.3,ease:'none'}}, {pm['debut']:.3f});")
            js.append(f"tl.to('#filigrane', {{opacity:1,duration:0.3,ease:'none'}}, {max(pm['debut'] + 0.3, pm['fin'] - 0.1):.3f});")
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1920, height=1080">
<title>Les Mystères d'Akeb — {esc(dossier.parent.name)}</title>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-duration="{total:.3f}">
<div id="fond" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="0"></div>
{chr(10).join(clips)}
<div id="filigrane" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="2"><div class="filigrane">LES MYSTÈRES D'AKEB</div></div>
</div>
<script src="assets/gsap.min.js"></script>
<script>
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join("  " + x for x in js)}
  tl.set({{}}, {{}}, {total:.3f});
  window.__timelines = window.__timelines || {{}};
  window.__timelines["root"] = tl;
</script>
</body>
</html>
"""
    f = dossier / "index.html"
    f.write_text(page, encoding="utf-8")
    return f


# ------------------------------------------------------------------ audio

def musique(variante: str) -> Path:
    f = RACINE / "audio" / "musique" / f"nappe_{variante}.wav"
    if not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        print(f"nappe absente : génération locale de {f.name} (graine fixe)", flush=True)
        sh([sys.executable, str(RACINE / "outils" / "musique.py"), str(f), "180", variante])
    return f


def mesurer(fichier: Path) -> tuple[float, float]:
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(fichier), "-map", "0:a", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
    return float(i[-1]), float(tp[-1])


def mixer(voix: np.ndarray, variante: str, dossier: Path) -> np.ndarray:
    """Voix + nappe atténuée sous la voix (mêmes réglages que montage.py)."""
    mesure = pyln.Meter(SR)
    if np.any(voix):
        voix = voix * (10 ** ((CIBLE_LUFS - 1.0 - mesure.integrated_loudness(voix)) / 20))
    sf.write(str(dossier / "voix_propre.wav"), voix, SR, subtype="PCM_24")
    mus, taux = sf.read(str(musique(variante)), dtype="float32", always_2d=True)
    mus = M.boucle(mus, len(voix))
    env = M.enveloppe_voix(voix)
    g = 10 ** ((-10 + (-24 - -10) * env) / 20)  # -10 dB hors voix, -24 dB sous la voix
    fondu = np.ones(len(voix), np.float32)
    nf = min(len(voix) // 2, SR * 3)
    fondu[:nf] = np.linspace(0, 1, nf)
    fondu[-nf:] = np.linspace(1, 0, nf)
    return np.stack([voix, voix], axis=1) + mus * (g * fondu)[:, None]


# ------------------------------------------------------------------ principal

def preparer(nom_ep: str, maquette: bool = False) -> dict:
    ep = RACINE / "episodes" / nom_ep
    cfg = charger_json(RACINE / "audio" / "config_narration.json", {})
    pause_defaut = float(cfg.get("pause_defaut_s", M.PAUSE_DEFAUT))
    segments = {s["id"]: s for s in lire_segments(ep)}
    seq = M.blocs(M.lire_storyboard(ep), list(segments.values()))
    manifest = charger_json(RACINE / "audio" / "manifest.json", {"segments": {}})["segments"]
    morceaux, t, timeline, cues = [], 0.0, [], []
    for b in seq:
        if b["type"] == "muet":
            n = int(round(b["duree"] * SR))
            morceaux.append(np.zeros(n, np.float32))
            timeline.append({"bloc": "-", "debut": t, "fin": t + n / SR, "plans": b["plans"]})
            t += n / SR
            continue
        s = segments[b["segment"]]
        info = manifest.get(f"{nom_ep}/{s['id']}")
        if maquette:  # composition de relecture sans voix : 155 mots/min, jamais exportée
            info = None
            voix = np.zeros(int(len(s["texte"].split()) / (M.MOTS_MINUTE_MAQUETTE / 60) * SR), np.float32)
        elif not info or info.get("statut") not in ("genere", "controle") or not (RACINE / info["wav"]).exists():
            raise SystemExit(f"Narration absente pour {nom_ep}/{s['id']} (audio/manifest.json) : rendu impossible "
                             "(--maquette --composition-seule pour relire les gabarits sans voix)")
        if info:
            voix = M.charger_voix(RACINE / info["wav"])
        pause = s["pause_apres"] if s["pause_apres"] is not None else pause_defaut
        debut = t
        for r in M.repliques(s["texte"], None if maquette else voix, len(voix) / SR):
            for morceau in M.decouper_repliques(r["texte"]):
                part = (r["fin"] - r["debut"]) * len(morceau) / len(r["texte"])
                cues.append({"debut": debut + r["debut"], "fin": debut + r["debut"] + part, "texte": morceau})
                r["debut"] += part
        morceaux += [voix, np.zeros(int(pause * SR), np.float32)]
        t = debut + len(voix) / SR + int(pause * SR) / SR
        timeline.append({"bloc": s["id"], "debut": debut, "fin": t, "plans": b["plans"]})
    voix = np.concatenate(morceaux)
    total = q(len(voix) / SR)
    voix = np.pad(voix, (0, max(0, int(round(total * SR)) - len(voix))))[: int(round(total * SR))]
    plans_min = []
    for bloc in timeline:
        poids = sum(p["poids"] for p in bloc["plans"])
        c = bloc["debut"]
        for p in bloc["plans"]:
            d = (bloc["fin"] - bloc["debut"]) * p["poids"] / poids
            plans_min.append({"plan": p, "debut": q(c), "fin": q(c + d)})
            c += d
    plans_min[-1]["fin"] = total
    return {"ep": ep, "voix": voix, "total": total, "plans": plans_min, "cues": cues, "seq": seq}


COUPURES = {"et", "ou", "mais", "puis", "avant", "après", "qui", "que", "qu'il", "qu'elle", "sont", "est", "a", "ont",
            "dans", "pour", "comme", "sans", "car", "donc", "lorsque", "quand", "dont", "où"}


def scinder(texte: str) -> list[str]:
    """Coupe une réplique trop longue en deux, de préférence après une ponctuation ou avant une conjonction."""
    meilleur = None
    for m in re.finditer(" ", texte):
        g, d = texte[:m.start()], texte[m.end():]
        if len(g) < 15 or len(d) < 15 or d[0] in ":;?!»" or g.endswith("«"):
            continue
        score = abs(len(g) - len(d)) / len(texte)
        if g.endswith((",", ";", ":", ".")):
            score -= 0.35
        elif d.split(" ")[0].lower() in COUPURES:
            score -= 0.2
        if meilleur is None or score < meilleur[0]:
            meilleur = (score, g, d)
    return [meilleur[1], meilleur[2]] if meilleur else [texte]


def ecrire_srt(cues: list[dict], total: float, f: Path, max_ligne: int = 42) -> list[dict]:
    """SRT : 2 lignes de 42 caractères au plus ; une réplique trop longue est scindée (minutage au prorata) ;
    chaque réplique reste affichée assez longtemps pour être lue (≈ 17 car./s), sans chevaucher la suivante."""
    sortie = []
    for c in cues:
        file_ = [dict(c)]
        while file_:
            r = file_.pop(0)
            texte = M.deux_lignes(r["texte"], max_ligne)
            if max(len(l) for l in texte.splitlines()) <= max_ligne or len(r["texte"]) < 20:
                sortie.append(dict(r, texte=texte))
                continue
            morceaux = scinder(r["texte"])
            if len(morceaux) < 2:
                sortie.append(dict(r, texte=texte))
                continue
            t, dur, n = r["debut"], r["fin"] - r["debut"], len(r["texte"])
            nouveaux = []
            for m in morceaux:
                d = dur * len(m) / n
                nouveaux.append({"debut": t, "fin": t + d, "texte": m})
                t += d
            file_ = nouveaux + file_
    for i, c in enumerate(sortie):
        fin = max(c["fin"] + 0.3, c["debut"] + len(c["texte"].replace("\n", "")) / 17, c["debut"] + 0.8)
        if i + 1 < len(sortie):
            fin = min(fin, sortie[i + 1]["debut"] - 0.04)
        c["fin"] = min(max(fin, c["fin"]), total - 0.05)
    f.write_text("\n".join(f"{i + 1}\n{M.fmt_srt(c['debut'])} --> {M.fmt_srt(c['fin'])}\n{c['texte']}\n"
                           for i, c in enumerate(sortie)) + "\n", encoding="utf-8")
    return sortie


def rendre(nom_ep: str, variante: str | None, workers: int, composition_seule: bool, exporter: bool, maquette: bool = False) -> dict:
    if maquette:
        composition_seule, exporter = True, False
    d = preparer(nom_ep, maquette)
    numero = nom_ep[:2]
    rendu = RACINE / "montage" / "rendu" / nom_ep
    hf = rendu / ("hyperframes_maquette" if maquette else "hyperframes")
    hf.mkdir(parents=True, exist_ok=True)
    index = composition(d["plans"], d["total"], hf)
    # rythme : plus long état fixe (contrôle « changement visuel toutes les 4 à 8 s »)
    tl = {"episode": nom_ep, "moteur": "hyperframes 0.8.99", "duree_s": d["total"],
          "plans": [{"plan": pm["plan"]["plan"], "segment": pm["plan"]["segment"], "type": pm["plan"]["type"],
                     "statut": pm["plan"].get("statut", ""), "debut": pm["debut"], "fin": pm["fin"]} for pm in d["plans"]]}
    longs = [p for p in tl["plans"] if p["fin"] - p["debut"] > 8]
    tl["plans_sup_8s"] = [p["plan"] for p in longs]
    if maquette:
        return {"composition": str(index.relative_to(RACINE)), "duree_s": d["total"], "plans": len(d["plans"]),
                "plans_sup_8s": [p["plan"] for p in longs], "maquette": "minutage estimé à 155 mots/min, sans voix"}
    d["cues"] = ecrire_srt(d["cues"], d["total"], rendu / f"{nom_ep}.srt")
    chapitres = [(pm["debut"], pm["plan"]["params"].get("chapitre") or pm["plan"]["texte"]) for pm in d["plans"]
                 if pm["plan"]["type"] == "chapitre" or pm["plan"]["params"].get("chapitre")]
    if not chapitres or chapitres[0][0] > 0.5:
        chapitres.insert(0, (0.0, "Introduction" if numero != "00" else "Bande-annonce"))
    chap_txt = "\n".join(f"{M.fmt_chap(0 if i == 0 else t)} {titre}" for i, (t, titre) in enumerate(chapitres))
    (rendu / "chapitres.txt").write_text(chap_txt + "\n", encoding="utf-8")
    tl["chapitres"] = chap_txt.splitlines()
    tl["chapitres_trop_courts"] = [chapitres[i][1] for i in range(len(chapitres) - 1) if chapitres[i + 1][0] - chapitres[i][0] < 10]
    tl["nb_sous_titres"] = len(d["cues"])
    (rendu / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    env = dict(os.environ)
    if not env.get("HYPERFRAMES_BROWSER_PATH"):
        cands = sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"))
        if cands:
            env["HYPERFRAMES_BROWSER_PATH"] = cands[-1]
    env["HYPERFRAMES_TELEMETRY_DISABLED"] = "1"
    hf_bin = HF / "node_modules" / ".bin" / "hyperframes"
    lint = subprocess.run([str(hf_bin), "lint", str(hf)], capture_output=True, text=True, env=env, cwd=HF)
    print("lint :", (lint.stdout + lint.stderr).strip()[-1500:], flush=True)
    if composition_seule:
        return {"composition": str(index.relative_to(RACINE)), "duree_s": d["total"], "plans": len(d["plans"])}

    video = rendu / "video_seule.mp4"
    print(f"rendu HyperFrames : {len(d['plans'])} plans, {d['total']:.2f} s…", flush=True)
    sh([str(hf_bin), "render", str(hf), "-o", str(video), "--fps", str(FPS), "-w", str(workers), "--quiet"], env=env, cwd=HF)

    # audio : mixage, normalisation, limiteur ; boucle jusqu'à -16 LUFS et crête vraie ≤ -1,5 dBTP après AAC
    dossier_audio = RACINE / "audio" / nom_ep
    dossier_audio.mkdir(parents=True, exist_ok=True)
    mix = mixer(d["voix"], variante or MUSIQUE_DEFAUT.get(numero, "enquete"), dossier_audio)
    mesure = pyln.Meter(SR)
    gain = CIBLE_LUFS - mesure.integrated_loudness(mix)
    limite = -2.3
    mp4 = rendu / f"{nom_ep}.mp4"
    for essai in range(6):
        brut = dossier_audio / "master_avant_limiteur.wav"
        sf.write(str(brut), mix * (10 ** (gain / 20)), SR, subtype="FLOAT")
        master = dossier_audio / "master.wav"
        sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(brut), "-af",
            f"alimiter=limit={10 ** (limite / 20):.4f}:attack=5:release=80:level=disabled", "-ar", str(SR), "-c:a", "pcm_s24le", str(master)])
        sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video), "-i", str(master), "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2", "-movflags", "+faststart",
            "-t", f"{d['total']:.3f}", str(mp4)])
        lufs, tp = mesurer(mp4)
        print(f"  essai {essai + 1} : {lufs:.1f} LUFS, crête vraie {tp:.1f} dBTP (limiteur {limite:.1f} dB)", flush=True)
        ok_l, ok_p = abs(lufs - CIBLE_LUFS) <= 0.3, tp <= CRETE_MAX - 0.1
        if ok_l and ok_p:
            break
        if not ok_p:
            limite -= (tp - (CRETE_MAX - 0.3))
        if not ok_l:
            gain += CIBLE_LUFS - lufs
    brut.unlink(missing_ok=True)
    res = {"mp4": str(mp4.relative_to(RACINE)), "srt": str((rendu / f"{nom_ep}.srt").relative_to(RACINE)),
           "chapitres": tl["chapitres"], "duree_s": d["total"], "plans": len(d["plans"]), "sous_titres": len(d["cues"]),
           "sonie_lufs": lufs, "crete_vraie_dbtp": tp, "plans_sup_8s": tl["plans_sup_8s"]}
    if exporter:
        dest = RACINE / "exports" / "videos"
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(mp4, dest / f"{nom_ep}.mp4")
        shutil.copy(rendu / f"{nom_ep}.srt", dest / f"{nom_ep}.fr.srt")
        res["export"] = str((dest / f"{nom_ep}.mp4").relative_to(RACINE))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("episode", help="dossier dans episodes/, ex. 00_bande_annonce, 01_vie_avant_affaire")
    ap.add_argument("--musique", help="enquete | archives | conclusion")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--composition-seule", action="store_true", help="écrit la composition HTML sans rendre le MP4")
    ap.add_argument("--exporter", action="store_true", help="copie MP4 + SRT dans exports/videos/")
    ap.add_argument("--maquette", action="store_true", help="composition de relecture sans voix (155 mots/min), pas de MP4")
    a = ap.parse_args()
    print(json.dumps(rendre(a.episode, a.musique, a.workers, a.composition_seule, a.exporter, a.maquette), ensure_ascii=False, indent=2))
