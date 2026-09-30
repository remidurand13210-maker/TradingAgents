"""Contrôles techniques d'un export : flux, durée, sonie, crête vraie, noirs, silences, SRT, planche d'images.

  python3 controle.py exports/episodes/LMA_XDDL_EP01.mp4 [--attendu 1920x1080] [--timeline montage/..._timeline.json]

Ce contrôle automatique ne remplace pas une écoute humaine complète : le rapport
indique précisément ce qui a été vérifié.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

RACINE = Path(__file__).resolve().parent.parent


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout + r.stderr


def sonde(mp4: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(mp4)], capture_output=True, text=True).stdout
    return json.loads(out)


def srt_cues(srt: Path) -> list[tuple[float, float, str]]:
    def sec(t: str) -> float:
        h, m, s = t.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    cues = []
    for bloc in srt.read_text(encoding="utf-8").strip().split("\n\n"):
        lignes = bloc.splitlines()
        if len(lignes) >= 3 and "-->" in lignes[1]:
            a, b = [x.strip() for x in lignes[1].split("-->")]
            cues.append((sec(a), sec(b), "\n".join(lignes[2:])))
    return cues


def controler(mp4: Path, attendu: str, timeline: Path | None, voix: Path | None) -> dict:
    info = sonde(mp4)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    duree = float(info["format"]["duration"])
    rapport = {"fichier": str(mp4.relative_to(RACINE)), "verifie": [], "alertes": []}
    fps = eval(v["r_frame_rate"])  # « 30/1 »
    rapport["video"] = {"codec": v["codec_name"], "taille": f"{v['width']}x{v['height']}", "fps": fps, "pix_fmt": v.get("pix_fmt")}
    rapport["audio"] = {"codec": a["codec_name"], "taux": a["sample_rate"], "canaux": a["channels"]} if a else None
    rapport["duree_s"] = round(duree, 2)
    rapport["duree_audio_s"] = round(float(a.get("duration", duree)), 2) if a else None
    if rapport["video"]["taille"] != attendu:
        rapport["alertes"].append(f"taille {rapport['video']['taille']} ≠ {attendu}")
    if abs(fps - 30) > 0.01 or v["codec_name"] != "h264" or (a and a["codec_name"] != "aac"):
        rapport["alertes"].append("format hors cible (H.264 / AAC / 30 i/s)")
    if a and abs(float(a.get("duration", duree)) - float(v.get("duration", duree))) > 0.15:
        rapport["alertes"].append("écart de durée entre pistes audio et vidéo > 0,15 s")
    rapport["verifie"].append("flux, codecs, résolution, cadence, durées")

    # sonie intégrée et crête vraie
    e = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"])
    i_lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
    rapport["sonie_lufs"] = float(i_lufs[-1]) if i_lufs else None
    rapport["crete_vraie_dbtp"] = float(tp[-1]) if tp else None
    if rapport["sonie_lufs"] is not None and abs(rapport["sonie_lufs"] + 16) > 1.0:
        rapport["alertes"].append(f"sonie {rapport['sonie_lufs']} LUFS (cible -16 ± 1)")
    if rapport["crete_vraie_dbtp"] is not None and rapport["crete_vraie_dbtp"] > -1.5:
        rapport["alertes"].append(f"crête vraie {rapport['crete_vraie_dbtp']} dBTP > -1,5")
    rapport["verifie"].append("sonie intégrée EBU R128 et crête vraie")

    # écrans noirs (hors fondus brefs) et silences longs
    b = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-vf", "blackdetect=d=0.6:pix_th=0.02", "-an", "-f", "null", "-"])
    noirs = re.findall(r"black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)", b)
    rapport["sequences_noires"] = [tuple(map(float, n)) for n in noirs]
    if noirs:
        rapport["alertes"].append(f"{len(noirs)} séquence(s) noire(s) ≥ 0,6 s")
    s = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(voix or mp4), "-af", "silencedetect=n=-45dB:d=2.5", "-f", "null", "-"])
    sil = re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", s)
    rapport["silences_voix_sup_2_5s"] = [(round(float(x), 2), round(float(y), 2)) for x, y in sil]
    rapport["verifie"].append("séquences noires ≥ 0,6 s ; silences de voix ≥ 2,5 s")

    # sous-titres
    srt = mp4.with_suffix(".srt")
    if srt.exists():
        cues = srt_cues(srt)
        chev = sum(1 for x, y in zip(cues, cues[1:]) if y[0] < x[1] - 0.001)
        rapide = [c[2] for c in cues if len(c[2].replace("\n", "")) / max(0.1, c[1] - c[0]) > 21]
        longues = [c[2] for c in cues if any(len(l) > 42 for l in c[2].splitlines()) or len(c[2].splitlines()) > 2]
        rapport["sous_titres"] = {"nb": len(cues), "fin_derniere": round(cues[-1][1], 2) if cues else None,
                                  "chevauchements": chev, "trop_rapides_21cps": len(rapide), "lignes_trop_longues": len(longues)}
        if cues and cues[-1][1] > duree + 0.05:
            rapport["alertes"].append("sous-titre au-delà de la fin de la vidéo")
        if chev:
            rapport["alertes"].append(f"{chev} chevauchement(s) de sous-titres")
        if longues:
            rapport["alertes"].append(f"{len(longues)} sous-titre(s) > 2 lignes ou > 42 caractères par ligne")
        rapport["verifie"].append("sous-titres : chevauchements, vitesse de lecture, longueur des lignes (minutage théorique aligné sur les pauses)")
    else:
        rapport["alertes"].append("SRT absent")

    # planche : début, chaque changement de chapitre ou plan-clé, fin
    instants = [0.5, duree / 2, max(0, duree - 1.0)]
    if timeline and timeline.exists():
        tl = json.loads(timeline.read_text(encoding="utf-8"))
        for p in tl["plans"]:
            if p["type"] in ("titre", "chapitre", "livre", "question", "carte", "frise", "sources"):
                instants.append(p["debut"] + min(1.0, (p["fin"] - p["debut"]) / 2))
    instants = sorted(set(round(x, 2) for x in instants if x < duree))
    vignettes = []
    tmp = RACINE / "montage" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    for k, t in enumerate(instants):
        f = tmp / f"img_{k:03d}.png"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", "-vf", "scale=480:-2", str(f)])
        if f.exists():
            vignettes.append((t, Image.open(f).convert("RGB")))
    if vignettes:
        w, h = vignettes[0][1].size
        cols = 4
        lignes = (len(vignettes) + cols - 1) // cols
        planche = Image.new("RGB", (cols * (w + 6), lignes * (h + 30)), (255, 255, 255))
        d = ImageDraw.Draw(planche)
        for k, (t, im) in enumerate(vignettes):
            x, y = (k % cols) * (w + 6), (k // cols) * (h + 30)
            planche.paste(im, (x, y + 24))
            d.text((x + 4, y + 4), f"{int(t // 60):02d}:{t % 60:05.2f}", fill=(0, 0, 0))
        preuves = RACINE / "preuves" / "controles"
        preuves.mkdir(parents=True, exist_ok=True)
        chemin = preuves / (mp4.stem + "_planche.png")
        planche.save(chemin)
        rapport["planche"] = str(chemin.relative_to(RACINE))
        rapport["verifie"].append(f"planche de {len(vignettes)} images à relire (début, plans-clés, fin)")
    rapport["non_verifie"] = ["écoute humaine intégrale", "conformité texte/voix (transcription automatique non exécutée ici)"]
    rapport["conforme_technique"] = not rapport["alertes"]
    return rapport


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--attendu", default="1920x1080")
    ap.add_argument("--timeline")
    ap.add_argument("--voix")
    a = ap.parse_args()
    mp4 = (RACINE / a.mp4) if not Path(a.mp4).is_absolute() else Path(a.mp4)
    r = controler(mp4, a.attendu, Path(RACINE / a.timeline) if a.timeline else None, Path(RACINE / a.voix) if a.voix else None)
    sortie = RACINE / "preuves" / "controles" / (mp4.stem + "_controle.json")
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=2))
