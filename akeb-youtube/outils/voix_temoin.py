"""Voix témoin locale (Kokoro, Apache 2.0) : mesure des durées réelles et maquettes écoutables.

NON PUBLIABLE. Sert uniquement à caler le montage, les sous-titres et les durées
avant la narration Gemini/Algieba. Manifeste séparé : audio/manifest_temoin.json.

  python3 voix_temoin.py 01_vie_avant_affaire
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from narration_gemini import charger_json, ecrire_json, lire_segments  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
MODELES = Path(__file__).resolve().parent / "modeles"
MANIFEST = RACINE / "audio" / "manifest_temoin.json"
VOIX, VITESSE = "ff_siwis", 1.0


def main(nom_ep: str) -> None:
    from kokoro_onnx import Kokoro
    k = Kokoro(str(MODELES / "kokoro-v1.0.onnx"), str(MODELES / "voices-v1.0.bin"))
    man = charger_json(MANIFEST, {"avertissement": "voix témoin locale, non publiable", "segments": {}})
    dossier = RACINE / "audio" / "temoin" / nom_ep
    dossier.mkdir(parents=True, exist_ok=True)
    total_mots, total_s = 0, 0.0
    for s in lire_segments(RACINE / "episodes" / nom_ep):
        h = hashlib.sha256(f"{VOIX}|{VITESSE}|{s['texte']}".encode()).hexdigest()[:16]
        wav = dossier / f"{s['id']}_{h}.wav"
        if not wav.exists():
            audio, sr = k.create(s["texte"], voice=VOIX, speed=VITESSE, lang="fr-fr")
            sf.write(str(wav), audio, sr, subtype="PCM_16")
        info = sf.info(str(wav))
        mots = len(s["texte"].split())
        man["segments"][f"{nom_ep}/{s['id']}"] = {"wav": str(wav.relative_to(RACINE)), "duree_s": round(info.duration, 3),
                                                 "mots": mots, "statut": "genere", "voix": f"kokoro:{VOIX}"}
        total_mots += mots
        total_s += info.duration
    ecrire_json(MANIFEST, man)
    print(json.dumps({"episode": nom_ep, "mots": total_mots, "duree_voix_min": round(total_s / 60, 2),
                      "debit_mpm": round(total_mots / (total_s / 60), 1)}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
