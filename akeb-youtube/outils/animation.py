"""Animations de montage, calculées localement (aucun service payant).

Principe : chaque plan est rendu image par image en Python (transformations subpixel, donc
sans tremblement du texte), puis encodé par ffmpeg. Animations par défaut selon le type :

- cartons (titre, chapitre, date, question, citation, texte, sources, livre, avertissement) :
  « revele » — les bandes de contenu apparaissent de haut en bas avec une légère montée, puis
  « poussée » lente (zoom de 2,5 %) ;
- document : révélation ligne à ligne étalée sur la durée du plan (au rythme de la voix) ;
- frise : « curseur » — le curseur avance, les jalons apparaissent à son passage ;
- carte : « trace » — le trajet se dessine d'étape en étape ;
- photo : « kenburns » — zoom ou panoramique de 3 à 6 %, crédit et licence à l'écran ;
- « fixe » : plan immobile (respiration).
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path
from typing import Callable, Iterator

import numpy as np
from PIL import Image, ImageDraw

import identite as I

W, H, FPS = 1920, 1080, 30


def lisse(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def poussee(img: Image.Image, echelle: float, cx: float = W / 2, cy: float = H / 2) -> Image.Image:
    """Zoom subpixel centré (échelle ≥ 1)."""
    if abs(echelle - 1) < 1e-4:
        return img
    a = 1 / echelle
    return img.transform((W, H), Image.AFFINE, (a, 0, cx - cx * a, 0, a, cy - cy * a), resample=Image.BICUBIC)


def bandeau(img: Image.Image, texte: str, couleur=(150, 40, 40), droite: bool = False) -> Image.Image:
    """Bandeau d'avertissement : à gauche (maquette), à droite (illustration ou reconstitution générée)."""
    if not texte:
        return img
    d = ImageDraw.Draw(img)
    f = I.police("bold", 24)
    largeur = 40 + f.getlength(texte)
    x0 = W - largeur if droite else 0
    d.rectangle([x0, 0, x0 + largeur, 44], fill=couleur)
    d.text((x0 + 16, 22), texte, font=f, fill=(255, 255, 255), anchor="lm")
    return img


# ------------------------------------------------------------------ révélation par bandes

def bandes_contenu(carte: np.ndarray, fond: np.ndarray, seuil: int = 14, ecart: int = 10) -> list[tuple[int, int]]:
    diff = np.abs(carte.astype(np.int16) - fond.astype(np.int16)).max(axis=2)
    lignes = np.where((diff > seuil).sum(axis=1) > 0)[0]
    if len(lignes) == 0:
        return []
    bandes, debut, prec = [], lignes[0], lignes[0]
    for y in lignes[1:]:
        if y - prec > ecart:
            bandes.append((max(0, debut - 3), min(H, prec + 4)))
            debut = y
        prec = y
    bandes.append((max(0, debut - 3), min(H, prec + 4)))
    return bandes


def anim_revele(png: Path, n: int, etalement: float = 0.0, amplitude: float = 0.025) -> Iterator[Image.Image]:
    """etalement = 0 : révélation rapide (≈ 1,2 s) ; > 0 : fraction de la durée sur laquelle s'étalent les bandes."""
    carte = np.asarray(Image.open(png).convert("RGB"))
    fond = np.asarray(I.fond(W, H).convert("RGB"))
    delta = carte.astype(np.int16) - fond.astype(np.int16)
    bandes = bandes_contenu(carte, fond)
    duree = n / FPS
    if etalement > 0:
        fenetre = max(1.2, etalement * duree)
        departs = [fenetre * k / max(1, len(bandes)) for k in range(len(bandes))]
        montee = 0.45
    else:
        departs = [0.12 + 0.16 * k for k in range(len(bandes))]
        montee = 0.55
    fond16 = fond.astype(np.int16)
    for i in range(n):
        t = i / FPS
        sortie = fond16.copy()
        for (y0, y1), t0 in zip(bandes, departs):
            v = lisse((t - t0) / montee)
            if v <= 0:
                continue
            dy = int(round(12 * (1 - v)))
            a0, a1 = y0 + dy, min(H, y1 + dy)
            sortie[a0:a1] += (delta[y0:y0 + (a1 - a0)] * v).astype(np.int16)
        img = Image.fromarray(np.clip(sortie, 0, 255).astype(np.uint8))
        yield poussee(img, 1 + amplitude * lisse(t / duree))


def anim_fixe(png: Path, n: int) -> Iterator[Image.Image]:
    img = Image.open(png).convert("RGB")
    for _ in range(n):
        yield img


# ------------------------------------------------------------------ rendus image par image

def anim_par_image(rendu: Callable[[float], Image.Image], n: int, amplitude: float = 0.02) -> Iterator[Image.Image]:
    duree = n / FPS
    for i in range(n):
        p = i / max(1, n - 1)
        yield poussee(rendu(p), 1 + amplitude * lisse(p * duree / max(duree, 0.01)))


def anim_photo(chemin: Path, n: int, mouvement: str = "zoom_avant", amplitude: float = 0.05,
               credit: str = "", statut: str = "", texte_bandeau: str = "") -> Iterator[Image.Image]:
    src = Image.open(chemin).convert("RGB")
    marge = 1 + amplitude + 0.01
    r = max(W * marge / src.width, H * marge / src.height)
    src = src.resize((int(src.width * r), int(src.height * r)), Image.LANCZOS)
    sw, sh = src.size
    for i in range(n):
        p = lisse(i / max(1, n - 1))
        if mouvement == "zoom_arriere":
            z = 1 + amplitude * (1 - p)
            cx, cy = sw / 2, sh / 2
        elif mouvement in ("pan_gauche", "pan_droite"):
            z = 1 + amplitude / 2
            course = (sw - W * z) / 2 * 0.9
            cx = sw / 2 + (course if mouvement == "pan_gauche" else -course) * (1 - 2 * p)
            cy = sh / 2
        else:  # zoom_avant
            z = 1 + amplitude * p
            cx, cy = sw / 2, sh / 2
        fw, fh = W * marge / z, H * marge / z
        boite = (cx - fw / 2, cy - fh / 2, cx + fw / 2, cy + fh / 2)
        img = src.transform((W, H), Image.EXTENT, boite, resample=Image.BICUBIC)
        d = ImageDraw.Draw(img)
        if credit:
            f = I.police("regular", 22)
            tw = f.getlength(credit)
            d.rectangle([W - tw - 44, H - 52, W - 16, H - 16], fill=(14, 17, 22))
            d.text((W - 30, H - 34), credit, font=f, fill=I.DISCRET, anchor="rm")
        if statut:
            I.etiquette(d, 40, 60, statut)
        yield bandeau(img, texte_bandeau, (120, 90, 30), droite=True)


# ------------------------------------------------------------------ encodage

def encoder(images: Iterator[Image.Image], n: int, sortie: Path, fondu_entree: bool, fondu_sortie: bool, marque: str = "") -> None:
    duree = n / FPS
    f = min(0.3, duree / 4)
    filtres = []
    if fondu_entree:
        filtres.append(f"fade=t=in:st=0:d={f:.3f}")
    if fondu_sortie:
        filtres.append(f"fade=t=out:st={duree - f:.3f}:d={f:.3f}")
    filtres.append("format=yuv420p")
    proc = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-frames:v", str(n), "-vf", ",".join(filtres),
                             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-g", str(FPS * 2), "-r", str(FPS), str(sortie)],
                            stdin=subprocess.PIPE)
    ecrites = 0
    for img in images:
        if marque:
            img = bandeau(img.copy(), marque)
        proc.stdin.write(img.tobytes())
        ecrites += 1
        if ecrites >= n:
            break
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"échec d'encodage : {sortie}")
