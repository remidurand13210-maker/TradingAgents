"""Nappe musicale originale, synthétisée localement (aucun échantillon tiers).

Usage : python3 musique.py sortie.wav [durée_s] [variante]
Variantes : "enquete" (ré mineur, sombre), "archives" (plus clair), "conclusion".
La nappe est destinée à rester très basse sous la voix.
"""
from __future__ import annotations

import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter

SR = 48000

GRILLES = {
    # accords en demi-tons MIDI
    "enquete": [[50, 57, 62, 65], [46, 53, 58, 62], [48, 55, 60, 64], [45, 52, 57, 61]],
    "archives": [[48, 55, 60, 64], [45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59]],
    "conclusion": [[50, 57, 62, 65], [53, 60, 65, 69], [46, 53, 58, 62], [48, 55, 60, 67]],
}


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def passe_bas(x: np.ndarray, fc: float) -> np.ndarray:
    b, a = butter(2, fc / (SR / 2))
    return lfilter(b, a, x)


def nappe(duree: float, variante: str = "enquete", graine: int = 1) -> np.ndarray:
    rnd = np.random.default_rng(graine)
    n = int(duree * SR)
    t = np.arange(n) / SR
    grille = GRILLES[variante]
    duree_accord = 12.0
    sortie = np.zeros((n, 2))
    nb = int(np.ceil(duree / duree_accord)) + 1
    for k in range(nb):
        accord = grille[k % len(grille)]
        debut = k * duree_accord - 3.0
        fin = debut + duree_accord + 6.0
        i0, i1 = max(0, int(debut * SR)), min(n, int(fin * SR))
        if i1 <= i0:
            continue
        tt = t[i0:i1] - debut
        env = np.clip(np.minimum(tt / 3.0, (fin - debut - tt) / 3.0), 0, 1) ** 1.5
        for j, note in enumerate(accord):
            f = hz(note - 12 if j == 0 else note)
            for canal, desaccord in ((0, -0.0025), (1, 0.0025)):
                ph = rnd.uniform(0, 2 * np.pi)
                trem = 1 + 0.08 * np.sin(2 * np.pi * (0.07 + 0.02 * j) * tt + ph)
                onde = np.sin(2 * np.pi * f * (1 + desaccord) * tt + ph)
                onde += 0.25 * np.sin(2 * np.pi * 2 * f * (1 + desaccord) * tt + ph)
                sortie[i0:i1, canal] += 0.12 * env * trem * onde / (1 + 0.4 * j)
    # quelques notes graves espacées, attaque douce
    for k in range(int(duree / 7)):
        t0 = 3.5 + k * 7 + rnd.uniform(-0.8, 0.8)
        if t0 > duree - 5:
            break
        note = grille[int(t0 // duree_accord) % len(grille)][rnd.integers(1, 4)] - 12
        i0 = int(t0 * SR)
        m = min(n - i0, int(5 * SR))
        tt = np.arange(m) / SR
        env = (1 - np.exp(-tt / 0.02)) * np.exp(-tt / 1.6)
        f = hz(note)
        son = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt / 0.6)
        pan = rnd.uniform(0.35, 0.65)
        sortie[i0:i0 + m, 0] += 0.10 * env * son * (1 - pan)
        sortie[i0:i0 + m, 1] += 0.10 * env * son * pan
    # souffle très discret
    souffle = rnd.normal(0, 1, (n, 2)) * 0.004
    sortie += souffle
    for c in range(2):
        sortie[:, c] = passe_bas(sortie[:, c], 2200.0)
    fondu = int(4 * SR)
    rampe = np.linspace(0, 1, fondu) ** 2
    sortie[:fondu] *= rampe[:, None]
    sortie[-fondu:] *= rampe[::-1][:, None]
    crete = np.max(np.abs(sortie))
    return sortie / crete * 0.5


if __name__ == "__main__":
    chemin = sys.argv[1]
    duree = float(sys.argv[2]) if len(sys.argv) > 2 else 180.0
    variante = sys.argv[3] if len(sys.argv) > 3 else "enquete"
    sf.write(chemin, nappe(duree, variante), SR, subtype="PCM_24")
    print("ok", chemin, duree, variante)
