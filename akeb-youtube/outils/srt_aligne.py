"""Sous-titres calés sur une voix réelle : frontières de phrases sur les pauses détectées.

  python3 srt_aligne.py voix.wav texte.txt sortie.srt [--decalage 0.0] [--max-ligne 42]

Le texte est connu : on ne transcrit pas, on aligne. Chaque phrase devient une ou
plusieurs répliques (2 lignes maximum), minutées au prorata des caractères entre
les pauses réelles de la voix.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montage import SR, charger_voix, deux_lignes, fmt_srt, repliques  # noqa: E402


def aligner(wav: Path, texte: str, decalage: float = 0.0, max_ligne: int = 42) -> list[dict]:
    voix = charger_voix(wav)
    cues = repliques(texte.replace("…", "… ").replace("  ", " "), voix, len(voix) / SR, max_ligne)
    for c in cues:
        c["debut"] += decalage
        c["fin"] += decalage
        c["texte"] = deux_lignes(c["texte"], max_ligne)
    return cues


def ecrire(cues: list[dict], sortie: Path) -> None:
    with open(sortie, "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            f.write(f"{i}\n{fmt_srt(c['debut'])} --> {fmt_srt(max(c['fin'], c['debut'] + 0.8))}\n{c['texte']}\n\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("texte")
    ap.add_argument("sortie")
    ap.add_argument("--decalage", type=float, default=0.0)
    ap.add_argument("--max-ligne", type=int, default=42)
    a = ap.parse_args()
    cues = aligner(Path(a.wav), Path(a.texte).read_text(encoding="utf-8").strip(), a.decalage, a.max_ligne)
    ecrire(cues, Path(a.sortie))
    print(f"{len(cues)} répliques -> {a.sortie}")
