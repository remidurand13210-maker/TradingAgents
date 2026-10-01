"""Montage d'un épisode : storyboard + narration -> MP4 1080p, SRT, chapitres, contrôles.

  python3 montage.py 01_vie_avant_affaire              # narration réelle (audio/manifest.json)
  python3 montage.py 01_vie_avant_affaire --maquette   # maquette muette minutée à 155 mots/min

La maquette porte un bandeau « MAQUETTE » sur chaque image : elle sert à relire
le rythme et les visuels, jamais à publier.
"""
from __future__ import annotations

import argparse
import csv
import os
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from PIL import ImageDraw
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
import animation as A  # noqa: E402
import identite as I  # noqa: E402
from narration_gemini import charger_json, lire_segments  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
FPS = 30
SR = 48000
MOTS_MINUTE_MAQUETTE = 155
PAUSE_DEFAUT = 0.45
CIBLE_LUFS = -16.0
LIMITE_CRETE_DB = -2.3  # crête échantillon ; vise une crête vraie ≤ -1,5 dBTP


def sh(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(" ".join(cmd[:6]) + "…\n" + r.stderr[-2000:])
    return r.stdout + r.stderr


# ------------------------------------------------------------------ storyboard

def lire_storyboard(ep: Path) -> list[dict]:
    with open(ep / "storyboard.csv", encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    for l in lignes:
        l["params"] = json.loads(l["params"]) if l.get("params", "").strip() else {}
        l["poids"] = float(l.get("poids") or 1)
    return lignes


def blocs(storyboard: list[dict], segments: list[dict]) -> list[dict]:
    """Séquence ordonnée de blocs : segment narré (avec ses plans) ou plan muet à durée fixe."""
    ids = [s["id"] for s in segments]
    vus, sortie = [], []
    for plan in storyboard:
        seg = plan["segment"].strip()
        if seg in ("", "-"):
            sortie.append({"type": "muet", "plans": [plan], "duree": float(plan["params"].get("duree", 3))})
            continue
        if seg not in ids:
            raise SystemExit(f"Plan {plan['plan']} : segment {seg} absent de narration.txt")
        if sortie and sortie[-1].get("segment") == seg:
            sortie[-1]["plans"].append(plan)
        else:
            if seg in vus:
                raise SystemExit(f"Segment {seg} non contigu dans le storyboard (plan {plan['plan']})")
            vus.append(seg)
            sortie.append({"type": "narre", "segment": seg, "plans": [plan]})
    manquants = [i for i in ids if i not in vus]
    if manquants:
        raise SystemExit("Segments sans plan dans le storyboard : " + ", ".join(manquants))
    if vus != [i for i in ids if i in vus]:
        raise SystemExit("L'ordre des segments du storyboard diffère de narration.txt")
    return sortie


# ------------------------------------------------------------------ visuels

ANIM_DEFAUT = {"titre": "revele", "chapitre": "revele", "date": "revele", "question": "revele", "citation": "revele",
               "texte": "revele", "sources": "revele", "livre": "revele", "avertissement": "revele", "document": "revele_lent",
               "frise": "curseur", "carte": "trace", "photo": "kenburns"}
VERSION_ANIM = 2


def evenements_frise(p: dict) -> list[dict]:
    """Frise large : jalons généraux. Frise zoomée (bornes) : jalons détaillés de la période, sans doublon."""
    evs = [e for e in frise_commune() if e["annee"] <= p.get("jusqua", 2100)]
    if p.get("bornes"):
        a0, a1 = p["bornes"]
        details = [e for e in evs if e.get("detail") and a0 <= e["annee"] <= a1]
        return details or [e for e in evs if a0 <= e["annee"] <= a1]
    return [e for e in evs if not e.get("detail")]


def images_plan(plan: dict, png: Path, n: int):
    """Générateur d'images animées du plan (rendu local)."""
    p, t = plan["params"], plan["type"]
    anim = p.get("anim") or ANIM_DEFAUT.get(t, "fixe")
    if anim == "fixe":
        return A.anim_fixe(png, n)
    if anim == "revele":
        return A.anim_revele(png, n)
    if anim == "revele_lent":
        return A.anim_revele(png, n, etalement=0.55, amplitude=0.015)
    if anim == "curseur" and t == "frise":
        cible = p.get("curseur") or p.get("jusqua", 2026.8)
        bornes = tuple(p["bornes"]) if p.get("bornes") else None
        depart = p.get("curseur_depart") or (bornes[0] if bornes else (p["focus"][0] if p.get("focus") else cible - 5))
        evs = evenements_frise(p)

        def rendu(x: float):
            c = depart + (cible - depart) * A.lisse(x / 0.75)
            return I.carton_frise([e for e in evs if e["annee"] <= c + 1e-6], tuple(p["focus"]) if p.get("focus") else None,
                                  plan.get("texte", ""), c, bornes)
        return A.anim_par_image(rendu, n, amplitude=0.0)
    if anim == "trace" and t == "carte":
        def rendu(x: float):
            return I.carton_carte(p["points"], tuple(p["bbox"]), plan.get("texte", ""), p.get("trajet", False),
                                  plan.get("source", ""), plan.get("faits", ""), plan.get("statut", "").strip(), A.lisse(x / 0.75))
        return A.anim_par_image(rendu, n, amplitude=0.02)
    if anim == "kenburns" and t == "photo":
        return A.anim_photo(RACINE / p["visuel"], n, p.get("mouvement", "zoom_avant"), p.get("amplitude", 0.05),
                            p.get("credit", ""), plan.get("statut", "").strip(), p.get("bandeau", ""))
    return A.anim_revele(png, n)


def _rendre_clip(tache: tuple) -> str:
    plan, png, n, clip, fin, fout, marque = tache
    if not Path(clip).exists():
        A.encoder(images_plan(plan, Path(png), n), n, Path(clip), fin, fout, marque)
    return clip


def frise_commune() -> list[dict]:
    return charger_json(RACINE / "episodes" / "frise_commune.json", {"evenements": []})["evenements"]


def rendre_plan(plan: dict, numero_ep: str, bandeau: str, dossier: Path) -> Path:
    p = plan["params"]
    cle = hashlib.sha256(json.dumps([plan, numero_ep, bandeau, Path(I.__file__).stat().st_mtime], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    sortie = dossier / f"{plan['plan']}_{cle}.png"
    if sortie.exists():
        return sortie
    t, statut = plan["type"], plan.get("statut", "").strip()
    texte, texte2 = plan.get("texte", ""), plan.get("texte2", "")
    src, faits = plan.get("source", ""), plan.get("faits", "")
    if t == "avertissement":
        img = I.carton_avertissement()
    elif t == "titre":
        img = I.carton_titre(p.get("numero", numero_ep), texte, texte2)
    elif t == "chapitre":
        img = I.carton_chapitre(p.get("numero", ""), texte)
    elif t == "date":
        img = I.carton_date(texte, texte2, p.get("precision", ""), statut, src, faits)
    elif t == "citation":
        img = I.carton_citation(texte, texte2, statut or "TEMOIGNAGE", src, faits)
    elif t == "question":
        img = I.carton_question(texte, texte2 or "LA QUESTION")
    elif t == "document":
        img = I.carton_document(texte, [x.strip() for x in texte2.split("|") if x.strip()], src)
    elif t == "frise":
        evs = evenements_frise(p)
        img = I.carton_frise(evs, tuple(p["focus"]) if p.get("focus") else None, texte, p.get("curseur"), tuple(p["bornes"]) if p.get("bornes") else None)
    elif t == "carte":
        img = I.carton_carte(p["points"], tuple(p["bbox"]), texte, p.get("trajet", False), src, faits, statut)
    elif t == "livre":
        cov = RACINE / "montage" / "assets" / "couverture_akeb.png"
        img = I.carton_livre(cov if cov.exists() else None, [x.strip() for x in texte.split("|") if x.strip()])
    elif t == "photo":
        img = next(A.anim_photo(RACINE / p["visuel"], 1, p.get("mouvement", "zoom_avant"), p.get("amplitude", 0.05),
                                p.get("credit", ""), statut, p.get("bandeau", "")))
    elif t == "sources":
        img = I.carton_sources(texte or "Sources principales", [x.strip() for x in texte2.split("|") if x.strip()])
    else:  # "texte" par défaut
        img = I.carton_texte(texte, statut, src, faits, texte2)
    if bandeau:
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 40 + I.police("bold", 24).getlength(bandeau), 44], fill=(150, 40, 40))
        d.text((16, 22), bandeau, font=I.police("bold", 24), fill=(255, 255, 255), anchor="lm")
    img.save(sortie)
    return sortie


def encoder_plan(png: Path, n_images: int, sortie: Path, fondu_entree: bool, fondu_sortie: bool) -> None:
    duree = n_images / FPS
    f = min(0.3, duree / 4)
    filtres = []
    if fondu_entree:
        filtres.append(f"fade=t=in:st=0:d={f:.3f}")
    if fondu_sortie:
        filtres.append(f"fade=t=out:st={duree - f:.3f}:d={f:.3f}")
    filtres.append("format=yuv420p")
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-i", str(png),
        "-frames:v", str(n_images), "-vf", ",".join(filtres), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-tune", "stillimage", "-g", str(FPS * 2), "-r", str(FPS), str(sortie)])


# ------------------------------------------------------------------ audio

def charger_voix(chemin: Path) -> np.ndarray:
    x, taux = sf.read(str(chemin), dtype="float32", always_2d=True)
    x = x.mean(axis=1)
    if taux != SR:
        g = math.gcd(SR, taux)
        x = resample_poly(x, SR // g, taux // g).astype(np.float32)
    return x


def boucle(musique: np.ndarray, n: int) -> np.ndarray:
    if len(musique) >= n:
        return musique[:n]
    fondu = SR * 4
    sortie = musique.copy()
    while len(sortie) < n:
        r = np.linspace(0, 1, fondu)[:, None]
        chevauche = sortie[-fondu:] * (1 - r) + musique[:fondu] * r
        sortie = np.concatenate([sortie[:-fondu], chevauche, musique[fondu:]])
    return sortie[:n]


def enveloppe_voix(voix: np.ndarray) -> np.ndarray:
    fen = int(0.05 * SR)
    rms = np.sqrt(np.convolve(voix ** 2, np.ones(fen) / fen, mode="same") + 1e-12)
    actif = (20 * np.log10(rms + 1e-9) > -45).astype(np.float32)
    # maintien 400 ms puis lissage (attaque rapide, relâchement lent)
    maintien = int(0.4 * SR)
    actif = np.convolve(actif, np.ones(maintien), mode="same") > 0
    lisse = np.convolve(actif.astype(np.float32), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    return np.clip(lisse, 0, 1)


def pauses_internes(voix: np.ndarray, seuil_db: float = -40, duree_min: float = 0.16) -> list[tuple[float, float]]:
    fen = int(0.02 * SR)
    n = len(voix) // fen
    if n == 0:
        return []
    e = 20 * np.log10(np.sqrt((voix[: n * fen].reshape(n, fen) ** 2).mean(axis=1)) + 1e-9)
    silence = e < seuil_db
    pauses, debut = [], None
    for i, s in enumerate(silence):
        if s and debut is None:
            debut = i
        elif not s and debut is not None:
            if (i - debut) * fen / SR >= duree_min:
                pauses.append((debut * fen / SR, i * fen / SR))
            debut = None
    return pauses


# ------------------------------------------------------------------ sous-titres

def phrases(texte: str) -> list[str]:
    morceaux = re.split(r"(?<=[.!?…»])\s+(?=[«A-ZÀÂÉÈÊÎÔÙÛÇ0-9])", texte.strip())
    return [m.strip() for m in morceaux if m.strip()]


def decouper_repliques(phrase: str, max_car: int = 84) -> list[str]:
    if len(phrase) <= max_car:
        return [phrase]
    for sep in ("; ", " : ", ", ", " — ", " "):
        idx = [m.start() for m in re.finditer(re.escape(sep), phrase)]
        idx = [i for i in idx if 25 <= i <= len(phrase) - 20]
        if idx:
            milieu = min(idx, key=lambda i: abs(i - len(phrase) / 2))
            coupe = milieu + len(sep.rstrip()) if sep != " " else milieu
            gauche, droite = phrase[:coupe].strip(), phrase[coupe:].strip()
            return decouper_repliques(gauche, max_car) + decouper_repliques(droite, max_car)
    return [phrase]


def deux_lignes(texte: str, max_ligne: int = 42) -> str:
    """Coupe en deux lignes équilibrées ; jamais avant : ; ? ! » ni après «, de préférence après une virgule."""
    if len(texte) <= max_ligne:
        return texte
    candidats = []
    for i, c in enumerate(texte):
        if c != " " or i + 1 >= len(texte):
            continue
        if texte[i + 1] in ":;?!»" or texte[i - 1] == "«":
            continue
        g, d = texte[:i], texte[i + 1:]
        cout = max(len(g), len(d)) - (4 if g.endswith((",", ";", ":")) else 0)
        candidats.append((cout, i))
    if not candidats:
        return texte
    i = min(candidats)[1]
    return texte[:i] + "\n" + texte[i + 1:]


def morceaux_texte(texte: str) -> list[dict]:
    """Propositions : coupe après . ! ? … (forte) et après , ; : — (faible)."""
    brut = re.split(r"(?<=[.!?…])\s+|(?<=[,;:])\s+|\s+(?=— )", texte.strip())
    sortie = []
    for m in brut:
        m = m.strip()
        if not m:
            continue
        fort = bool(re.search(r"[.!?…»]$", m))
        sortie.append({"texte": m, "fort": fort})
    return sortie


def aligner_morceaux(morceaux: list[dict], voix: np.ndarray) -> list[tuple[float, float]]:
    """Apparie les frontières de propositions aux pauses réelles (programmation dynamique
    sur le temps de parole effectif). Renvoie (début, fin) de chaque proposition, en secondes."""
    duree = len(voix) / SR
    if not morceaux:
        return []
    fen = int(0.01 * SR)
    energie = [20 * np.log10(np.sqrt((voix[i:i + fen] ** 2).mean()) + 1e-9) for i in range(0, max(1, len(voix) - fen), fen)]
    actifs = [k for k, e in enumerate(energie) if e > -40]
    s0 = actifs[0] * fen / SR if actifs else 0.0
    e0 = (actifs[-1] + 1) * fen / SR if actifs else duree
    pauses = [(a, b) for a, b in pauses_internes(voix) if a > s0 + 0.1 and b < e0 - 0.05]
    cumul_p, sp = 0.0, []
    for a, b in pauses:
        sp.append((a - s0) - cumul_p)
        cumul_p += b - a
    parole = max(0.1, (e0 - s0) - cumul_p)
    poids = [len(m["texte"]) + 2 for m in morceaux]
    total = sum(poids)
    attendu, c = [], 0
    for w in poids[:-1]:
        c += w
        attendu.append(c / total * parole)
    nb, npz = len(attendu), len(pauses)
    sigma = max(0.5, 0.06 * parole)
    INF = float("inf")
    D = [[INF] * (npz + 1) for _ in range(nb + 1)]
    choix = [[None] * (npz + 1) for _ in range(nb + 1)]
    D[0][0] = 0.0
    for i in range(nb + 1):
        for j in range(npz + 1):
            if D[i][j] == INF:
                continue
            if i < nb:  # frontière sans pause
                cout = 4.0 if morceaux[i]["fort"] else 0.4
                if D[i][j] + cout < D[i + 1][j]:
                    D[i + 1][j], choix[i + 1][j] = D[i][j] + cout, ("f", i, j)
            if j < npz:  # pause sans frontière
                dur = pauses[j][1] - pauses[j][0]
                cout = 0.3 + 6.0 * max(0.0, dur - 0.3)
                if D[i][j] + cout < D[i][j + 1]:
                    D[i][j + 1], choix[i][j + 1] = D[i][j] + cout, ("p", i, j)
            if i < nb and j < npz:  # appariement
                dur = pauses[j][1] - pauses[j][0]
                cout = ((sp[j] - attendu[i]) / sigma) ** 2 - min(dur, 1.0) * (1.5 if morceaux[i]["fort"] else 0.5)
                if D[i][j] + cout < D[i + 1][j + 1]:
                    D[i + 1][j + 1], choix[i + 1][j + 1] = D[i][j] + cout, ("m", i, j)
    i, j, appariement = nb, npz, {}
    while i or j:
        k, pi, pj = choix[i][j]
        if k == "m":
            appariement[pi] = pauses[pj]
        i, j = pi, pj
    # ancres : début, frontières appariées, fin ; interpolation au prorata des caractères ailleurs
    bornes = [None] * (nb + 2)
    bornes[0] = (s0, s0)
    bornes[-1] = (e0, e0)
    for k, (a, b) in appariement.items():
        bornes[k + 1] = (a, b)
    k = 0
    while k < len(bornes) - 1:
        n = k + 1
        while bornes[n] is None:
            n += 1
        if n > k + 1:
            t0, t1 = bornes[k][1], bornes[n][0]
            w = poids[k:n]
            acc = 0
            for m in range(k + 1, n):
                acc += w[m - k - 1]
                t = t0 + (t1 - t0) * acc / sum(w)
                bornes[m] = (t, t)
        k = n
    return [(bornes[m][1], bornes[m + 1][0]) for m in range(len(morceaux))]


def repliques(texte: str, voix: np.ndarray | None, duree: float, max_ligne: int = 42, max_duree: float = 6.0) -> list[dict]:
    """Répliques de sous-titres (≤ 2 lignes) calées sur la voix ; sans voix, au prorata des caractères."""
    morceaux = morceaux_texte(texte)
    if voix is not None and np.any(voix):
        spans = aligner_morceaux(morceaux, voix)
    else:
        total = sum(len(m["texte"]) for m in morceaux) or 1
        spans, t = [], 0.0
        for m in morceaux:
            d = duree * len(m["texte"]) / total
            spans.append((t, t + d))
            t += d
    sortie, courant = [], None
    for m, (a, z) in zip(morceaux, spans):
        if courant and len(courant["texte"]) + 1 + len(m["texte"]) <= 2 * max_ligne and z - courant["debut"] <= max_duree and not courant["ferme"]:
            courant["texte"] += " " + m["texte"]
            courant["fin"] = z
        else:
            if courant:
                sortie.append(courant)
            courant = {"debut": a, "fin": z, "texte": m["texte"]}
        courant["ferme"] = m["fort"]
    if courant:
        sortie.append(courant)
    for r in sortie:
        r.pop("ferme", None)
        if len(r["texte"]) > 2 * max_ligne:  # proposition trop longue : découpe au prorata
            pass
    return sortie


def aligner_phrases(ph: list[str], duree: float, pauses: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Frontières de phrases calées sur les pauses réelles les plus proches des positions attendues."""
    total = sum(len(p) for p in ph) or 1
    attendu, cumul = [], 0
    for p in ph[:-1]:
        cumul += len(p)
        attendu.append(cumul / total * duree)
    centres = [(a + b) / 2 for a, b in pauses]
    frontieres, dernier = [], 0.0
    for t in attendu:
        candidats = [c for c in centres if c > dernier + 0.4 and abs(c - t) < max(1.5, 0.25 * duree / len(ph))]
        choix = min(candidats, key=lambda c: abs(c - t)) if candidats else t
        frontieres.append(choix)
        dernier = choix
    bornes = [0.0] + frontieres + [duree]
    return list(zip(bornes[:-1], bornes[1:]))


def fmt_srt(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_chap(t: float) -> str:
    t = int(t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


# ------------------------------------------------------------------ principal

def monter(nom_ep: str, maquette: bool, variante_musique: str | None, temoin: bool = False) -> dict:
    ep = RACINE / "episodes" / nom_ep
    numero = nom_ep[:2]
    segments = {s["id"]: s for s in lire_segments(ep)}
    sb = lire_storyboard(ep)
    seq = blocs(sb, list(segments.values()))
    manifest = charger_json(RACINE / "audio" / ("manifest_temoin.json" if temoin else "manifest.json"), {"segments": {}})["segments"]
    suffixe = "_maquette" if maquette else ("_temoin" if temoin else "")
    bandeau = "MAQUETTE — NARRATION NON GÉNÉRÉE" if maquette else ("MAQUETTE — VOIX TÉMOIN, NON PUBLIABLE" if temoin else "")
    rendu = RACINE / "montage" / "rendu" / (nom_ep + suffixe)
    (rendu / "plans").mkdir(parents=True, exist_ok=True)
    (rendu / "clips").mkdir(parents=True, exist_ok=True)

    # 1. piste voix et minutage absolu
    morceaux, t, timeline, cues = [], 0.0, [], []
    for b in seq:
        if b["type"] == "muet":
            n = int(round(b["duree"] * SR))
            morceaux.append(np.zeros(n, np.float32))
            debut, fin = t, t + n / SR
            timeline.append({"bloc": "-", "debut": debut, "fin": fin, "plans": b["plans"]})
            t = fin
            continue
        s = segments[b["segment"]]
        if maquette:
            duree = len(s["texte"].split()) / (MOTS_MINUTE_MAQUETTE / 60)
            voix = np.zeros(int(duree * SR), np.float32)
            pauses = []
        else:
            info = manifest.get(f"{nom_ep}/{s['id']}")
            if not info or info.get("statut") not in ("genere", "controle"):
                raise SystemExit(f"Narration absente pour {nom_ep}/{s['id']} : lancer narration_gemini.py produire ou --maquette")
            voix = charger_voix(RACINE / info["wav"])
            pauses = pauses_internes(voix)
        pause = s["pause_apres"] if s["pause_apres"] is not None else PAUSE_DEFAUT
        debut = t
        for r in repliques(s["texte"], None if maquette else voix, len(voix) / SR):
            for morceau in decouper_repliques(r["texte"]):
                part = (r["fin"] - r["debut"]) * len(morceau) / len(r["texte"])
                cues.append({"debut": debut + r["debut"], "fin": debut + r["debut"] + part, "texte": morceau})
                r["debut"] += part
        morceaux.append(voix)
        morceaux.append(np.zeros(int(pause * SR), np.float32))
        t = debut + len(voix) / SR + int(pause * SR) / SR
        timeline.append({"bloc": s["id"], "debut": debut, "fin": t, "plans": b["plans"]})
    voix = np.concatenate(morceaux)
    total = len(voix) / SR

    # 2. plans : découpage au prorata des poids, frontières en images absolues
    plans_minutes = []
    for bloc in timeline:
        poids = sum(p["poids"] for p in bloc["plans"])
        c = bloc["debut"]
        for p in bloc["plans"]:
            d = (bloc["fin"] - bloc["debut"]) * p["poids"] / poids
            plans_minutes.append({"plan": p, "debut": c, "fin": c + d})
            c += d
    clips, taches = [], []
    coupe_franche = lambda a, b: a is not None and b is not None and a["segment"] == b["segment"] and a["segment"] not in ("", "-")
    for i, pm in enumerate(plans_minutes):
        f0, f1 = round(pm["debut"] * FPS), round(pm["fin"] * FPS)
        png = rendre_plan(pm["plan"], numero, "", rendu / "plans")  # bandeau ajouté image par image
        anim = pm["plan"]["params"].get("anim") or ANIM_DEFAUT.get(pm["plan"]["type"], "fixe")
        clip = rendu / "clips" / f"{i:03d}_{png.stem}_{anim}_v{VERSION_ANIM}_{f1 - f0}.mp4"
        precedent = plans_minutes[i - 1]["plan"] if i else None
        suivant = plans_minutes[i + 1]["plan"] if i + 1 < len(plans_minutes) else None
        taches.append((pm["plan"], str(png), f1 - f0, str(clip), not coupe_franche(precedent, pm["plan"]),
                       not coupe_franche(pm["plan"], suivant), bandeau))
        clips.append(clip)
        pm["png"] = str(png.relative_to(RACINE))
        pm["anim"] = anim
    from multiprocessing import Pool
    with Pool(max(1, min(3, (os.cpu_count() or 2) - 1))) as pool:
        pool.map(_rendre_clip, taches)
    liste = rendu / "concat.txt"
    liste.write_text("".join(f"file '{c.resolve()}'\n" for c in clips), encoding="utf-8")
    video_seule = rendu / "video_seule.mp4"
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(video_seule)])

    # 3. mixage : voix propre + nappe atténuée sous la voix, normalisation
    dossier_audio = RACINE / "audio" / (nom_ep + suffixe)
    dossier_audio.mkdir(parents=True, exist_ok=True)
    mesure = pyln.Meter(SR)
    if not maquette and np.any(voix):
        gain_voix = CIBLE_LUFS - 1.0 - mesure.integrated_loudness(voix)
        voix = voix * (10 ** (gain_voix / 20))
    sf.write(str(dossier_audio / "voix_propre.wav"), voix, SR, subtype="PCM_24")
    variante = variante_musique or {"01": "archives", "02": "enquete", "03": "enquete", "04": "conclusion"}.get(numero, "enquete")
    mus_f = RACINE / "audio" / "musique" / f"nappe_{variante}.wav"
    mus, _ = sf.read(str(mus_f), dtype="float32", always_2d=True)
    mus = boucle(mus, len(voix))
    env = enveloppe_voix(voix) if np.any(voix) else np.zeros(len(voix), np.float32)
    g = 10 ** ((-10 + (-24 - -10) * env) / 20)  # -10 dB hors voix, -24 dB sous la voix
    fondu = np.ones(len(voix), np.float32)
    nf = min(len(voix) // 2, SR * 3)
    fondu[:nf] = np.linspace(0, 1, nf)
    fondu[-nf:] = np.linspace(1, 0, nf)
    mix = np.stack([voix, voix], axis=1) + mus * (g * fondu)[:, None]
    if maquette:
        mix = mus * (10 ** (-12 / 20)) * fondu[:, None]
    gain = CIBLE_LUFS - mesure.integrated_loudness(mix)
    mix = mix * (10 ** (gain / 20))
    master_brut = dossier_audio / "master_avant_limiteur.wav"
    sf.write(str(master_brut), mix, SR, subtype="PCM_24")
    master = dossier_audio / "master.wav"
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(master_brut),
        "-af", f"alimiter=limit={10 ** (LIMITE_CRETE_DB / 20):.4f}:attack=5:release=80:level=disabled", "-ar", str(SR), "-c:a", "pcm_s24le", str(master)])
    master_brut.unlink()

    # 4. assemblage final
    sortie_dir = RACINE / "exports" / "episodes"
    sortie_dir.mkdir(parents=True, exist_ok=True)
    base = f"LMA_XDDL_EP{numero}" + suffixe.upper()
    mp4 = sortie_dir / f"{base}.mp4"
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video_seule), "-i", str(master),
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR),
        "-movflags", "+faststart", "-shortest", str(mp4)])

    # 5. sous-titres et chapitres mesurés
    srt = sortie_dir / f"{base}.srt"
    with open(srt, "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            f.write(f"{i}\n{fmt_srt(c['debut'])} --> {fmt_srt(max(c['fin'], c['debut'] + 0.8))}\n{deux_lignes(c['texte'])}\n\n")
    chapitres = [(pm["debut"], pm["plan"]["params"].get("chapitre") or pm["plan"]["texte"]) for pm in plans_minutes
                 if pm["plan"]["type"] == "chapitre" or pm["plan"]["params"].get("chapitre")]
    if not chapitres or chapitres[0][0] > 0.5:
        chapitres.insert(0, (0.0, "Introduction"))
    chap_txt = "\n".join(f"{fmt_chap(0 if i == 0 else d)} {titre}" for i, (d, titre) in enumerate(chapitres))
    (ep / f"chapitres_mesures{suffixe}.txt").write_text(chap_txt + "\n", encoding="utf-8")
    courts = [chapitres[i][1] for i in range(len(chapitres) - 1) if chapitres[i + 1][0] - chapitres[i][0] < 10]

    tl = {"episode": nom_ep, "maquette": maquette, "voix_temoin": temoin, "duree_s": round(total, 2), "musique": variante,
          "plans": [{"plan": pm["plan"]["plan"], "segment": pm["plan"]["segment"], "type": pm["plan"]["type"], "anim": pm.get("anim"),
                     "debut": round(pm["debut"], 3), "fin": round(pm["fin"], 3), "png": pm["png"]} for pm in plans_minutes],
          "chapitres": chap_txt.splitlines(), "chapitres_trop_courts": courts, "nb_sous_titres": len(cues)}
    (RACINE / "montage" / f"{base}_timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"mp4": str(mp4.relative_to(RACINE)), "srt": str(srt.relative_to(RACINE)), "duree_s": round(total, 1),
            "plans": len(plans_minutes), "sous_titres": len(cues), "chapitres": chap_txt.splitlines(), "chapitres_trop_courts": courts}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--maquette", action="store_true")
    ap.add_argument("--temoin", action="store_true", help="voix témoin locale (audio/manifest_temoin.json)")
    ap.add_argument("--musique")
    a = ap.parse_args()
    print(json.dumps(monter(a.episode, a.maquette, a.musique, a.temoin), ensure_ascii=False, indent=2))
