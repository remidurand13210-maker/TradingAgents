"""Régénère les éléments hors Git de la maquette de comparaison (aucun appel payant).

Prérequis : l'archive de Codex décompressée dans /home/user/akeb-transmission (voix du Short 3,
couvertures) et les nappes musicales générées (outils/musique.py).
    python3 montage/maquette_comparaison/preparer.py
"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent.parent
sys.path.insert(0, str(RACINE / "outils"))
import identite as I  # noqa: E402
import soundfile as sf  # noqa: E402

TRANSMISSION = Path("/home/user/akeb-transmission")
VOIX = TRANSMISSION / "Shorts" / "03_apres_la_disparition_voix.wav"

# 1. Voix découpée aux pauses mesurées (moteur Akeb)
x, sr = sf.read(VOIX)
coupes = [0.0, 3.10, 10.25, 12.56, 17.47, 20.48, len(x) / sr]
(ICI / "audio").mkdir(exist_ok=True)
man = {"_note": "Voix Gemini/Algieba du Short 3, déjà produite (aucun nouvel appel), découpée aux pauses mesurées.", "segments": {}}
for i in range(6):
    a, b = int(coupes[i] * sr), int(coupes[i + 1] * sr)
    f = ICI / "audio" / f"S0{i + 1}.wav"
    sf.write(f, x[a:b], sr, subtype="PCM_16")
    man["segments"][f"maquette_comparaison/S0{i + 1}"] = {"wav": str(f.relative_to(RACINE)), "statut": "genere", "duree_s": round((b - a) / sr, 3)}
(ICI / "audio" / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")

# 2. Éléments HyperFrames
A = ICI / "hyperframes" / "assets"
A.mkdir(parents=True, exist_ok=True)
I.fond().save(A / "fond.png")
I.carton_carte([], (-5.5, 41.2, 9.8, 51.3), "", False, "", "", "").save(A / "carte_fond.png")
for nom in ["SourceSansPro-Regular", "SourceSansPro-Semibold", "SourceSansPro-Bold", "SourceSansPro-Black", "SourceSansPro-Light",
            "LiberationSerif-Bold", "LiberationSerif-Italic"]:
    shutil.copy(RACINE / "outils" / "polices" / f"{nom}.ttf", A)
shutil.copy(TRANSMISSION / "Livre" / "Couverture_audio.png", A / "couverture_akeb_audio.png")
shutil.copy(TRANSMISSION / "Livre" / "Couverture_ebook.png", A / "couverture_akeb.png")
shutil.copy(VOIX, A / "voix.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(RACINE / "audio" / "musique" / "nappe_enquete.wav"), "-t", "28",
                "-af", "afade=t=out:st=25.5:d=2.5", "-ar", "48000", str(A / "nappe.wav")], check=True)
gsap = Path("/home/user/akeb-hf/node_modules/gsap/dist/gsap.min.js")
if gsap.exists():
    shutil.copy(gsap, A)
else:
    print("gsap.min.js absent : npm i gsap@3 dans /home/user/akeb-hf puis relancer")
print("éléments régénérés")
