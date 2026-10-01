"""Narration Gemini TTS — segmentée, mise en cache, plafonnée, reprenable.

Garde-fous :
- aucun appel sans enveloppe accordée dans BUDGET.json (narration.enveloppe_accordee_eur) ;
- réservation du coût MAXIMAL avant chaque appel : arrêt si l'enveloppe serait dépassée ;
- cache par empreinte (modèle + voix + consignes + texte prononcé + paramètres) ;
- verrou de production (un seul processus) ; statut par segment dans audio/manifest.json ;
- quota (HTTP 429) : arrêt propre, reprise au prochain lancement ;
- la clé n'est jamais affichée, écrite, ni passée dans l'URL (en-tête x-goog-api-key) ;
- le modèle est vérifié auprès de l'API : aucun remplacement silencieux.

Usage :
  python3 narration_gemini.py estimer                 # volumes et coût maximal, sans appel
  python3 narration_gemini.py presence                # la clé est-elle injectée ? (oui/non, jamais la valeur)
  python3 narration_gemini.py verifier-modele         # GET du modèle (gratuit, clé requise)
  python3 narration_gemini.py echantillon             # court échantillon de voix
  python3 narration_gemini.py produire [--episode 01] [--segment S12] [--forcer]
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
AUDIO = RACINE / "audio"
CACHE = AUDIO / "cache"
CONFIG = AUDIO / "config_narration.json"
MANIFEST = AUDIO / "manifest.json"
REGISTRE = AUDIO / "registre_narration.jsonl"
VERROU = AUDIO / ".production.lock"
BUDGET = RACINE / "BUDGET.json"
EPISODES = RACINE / "episodes"
API = "https://generativelanguage.googleapis.com/v1beta"

SEG_RE = re.compile(r"^\[(S\d{2,3}[a-z]?)\]\s*(.*)$")
PAUSE_RE = re.compile(r"^\[pause\s+([\d.]+)\]$")


# ------------------------------------------------------------------ données

def charger_json(chemin: Path, defaut):
    if chemin.exists():
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    return defaut


def ecrire_json(chemin: Path, donnees) -> None:
    tmp = chemin.with_suffix(chemin.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
    tmp.replace(chemin)


def lire_segments(dossier_ep: Path) -> list[dict]:
    """narration.txt : blocs « [S01] texte » ; lignes « [pause 1.2] » ; # commentaires."""
    segments, courant = [], None
    for brut in (dossier_ep / "narration.txt").read_text(encoding="utf-8").splitlines():
        ligne = brut.strip()
        if not ligne or ligne.startswith("#"):
            continue
        m = SEG_RE.match(ligne)
        p = PAUSE_RE.match(ligne)
        if m:
            courant = {"id": m.group(1), "texte": m.group(2).strip(), "pause_apres": None}
            segments.append(courant)
        elif p:
            if segments:
                segments[-1]["pause_apres"] = float(p.group(1))
        elif courant is not None:
            courant["texte"] += " " + ligne
    return segments


def texte_prononce(texte: str, prononciations: dict) -> str:
    """Graphies d'aide à la prononciation, appliquées au texte envoyé au TTS seulement."""
    for mot, graphie in prononciations.items():
        texte = re.sub(rf"\b{re.escape(mot)}\b", graphie, texte)
    return texte


def empreinte(cfg: dict, texte: str) -> str:
    cle = json.dumps({
        "modele": cfg["modele"], "voix": cfg["voix"], "consignes": cfg["consignes"],
        "mode_consignes": cfg["mode_consignes"], "texte": texte, "version": 1,
    }, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(cle.encode("utf-8")).hexdigest()[:24]


# ------------------------------------------------------------------ budget

def tokens_texte(texte: str) -> int:
    return max(1, len(texte) // 4 + 1)


def cout_max_eur(cfg: dict, texte: str, consignes: str) -> float:
    t = cfg["tarifs"]
    mots = len(texte.split())
    duree_max_s = mots / (cfg["debit_mots_minute_min"] / 60.0)
    tok_out = duree_max_s * t["tokens_audio_par_seconde"] * cfg["marge_reservation"]
    tok_in = (tokens_texte(texte) + tokens_texte(consignes)) * cfg["marge_reservation"]
    usd = tok_in / 1e6 * t["entree_texte_usd_par_million"] + tok_out / 1e6 * t["sortie_audio_usd_par_million"]
    return usd * t["eur_par_usd"]


def cout_reel_eur(cfg: dict, usage: dict) -> float:
    t = cfg["tarifs"]
    usd = usage.get("promptTokenCount", 0) / 1e6 * t["entree_texte_usd_par_million"] \
        + usage.get("candidatesTokenCount", 0) / 1e6 * t["sortie_audio_usd_par_million"]
    return usd * t["eur_par_usd"]


def depense_cumulee_eur() -> float:
    total = 0.0
    if REGISTRE.exists():
        for ligne in REGISTRE.read_text(encoding="utf-8").splitlines():
            if ligne.strip():
                total += json.loads(ligne).get("cout_eur", 0.0)
    return total


def enveloppe_eur() -> float | None:
    b = charger_json(BUDGET, {})
    return (b.get("narration") or {}).get("enveloppe_accordee_eur")


def journaliser(entree: dict) -> None:
    entree["horodatage"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    with open(REGISTRE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ clé et API

def cle_api(cfg: dict) -> str:
    source = cfg.get("cle", {})
    if source.get("type") == "keyring":
        import keyring  # stockage chiffré du système (Windows : Gestionnaire d'identification)
        valeur = keyring.get_password(source["service"], source["utilisateur"])
    else:
        valeur = os.environ.get(source.get("variable", "GEMINI_API_KEY"))
    if not valeur:
        sys.exit("Clé Gemini introuvable dans le stockage configuré (aucune valeur affichée). "
                 "Configurer audio/config_narration.json › cle, sans jamais coller la clé dans un fichier suivi.")
    return valeur


def requete(methode: str, url: str, cle: str, corps: dict | None = None, delai: int = 300) -> dict:
    donnees = json.dumps(corps).encode("utf-8") if corps is not None else None
    req = urllib.request.Request(url, data=donnees, method=methode)
    req.add_header("x-goog-api-key", cle)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=delai) as r:
        return json.loads(r.read().decode("utf-8"))


def verifier_modele(cfg: dict) -> dict:
    cle = cle_api(cfg)
    try:
        info = requete("GET", f"{API}/models/{cfg['modele']}", cle)
    except urllib.error.HTTPError as e:
        sys.exit(f"Modèle {cfg['modele']} non disponible pour ce compte (HTTP {e.code}). Aucun remplacement automatique.")
    return {k: info.get(k) for k in ("name", "displayName", "version", "supportedGenerationMethods", "inputTokenLimit", "outputTokenLimit")}


def corps_requete(cfg: dict, texte: str) -> dict:
    speech = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": cfg["voix"]}}}
    if cfg["mode_consignes"] == "system_instruction":
        return {
            "systemInstruction": {"parts": [{"text": cfg["consignes"]}]},
            "contents": [{"parts": [{"text": texte}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": speech},
        }
    # Mode documenté « consigne en langage naturel » : séparée du texte par un marqueur explicite.
    prompt = f"{cfg['consignes']}\n\n{cfg['marqueur_texte']}\n{texte}"
    return {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": speech}}


def ecrire_wav(chemin: Path, pcm: bytes, taux: int) -> float:
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(taux)
        w.writeframes(pcm)
    return len(pcm) / 2 / taux


def synthese(cfg: dict, cle: str, texte: str) -> tuple[bytes, int, dict]:
    url = f"{API}/models/{cfg['modele']}:generateContent"
    rep = requete("POST", url, cle, corps_requete(cfg, texte))
    part = rep["candidates"][0]["content"]["parts"][0]["inlineData"]
    taux = 24000
    m = re.search(r"rate=(\d+)", part.get("mimeType", ""))
    if m:
        taux = int(m.group(1))
    return base64.b64decode(part["data"]), taux, rep.get("usageMetadata", {})


# ------------------------------------------------------------------ verrou

class Verrou:
    def __enter__(self):
        if VERROU.exists():
            age = time.time() - VERROU.stat().st_mtime
            if age < 6 * 3600:
                sys.exit(f"Production déjà en cours (verrou de {int(age)} s : {VERROU}). Arrêt.")
        VERROU.write_text(json.dumps({"pid": os.getpid(), "debut": time.time()}), encoding="utf-8")
        return self

    def __exit__(self, *exc):
        VERROU.unlink(missing_ok=True)


# ------------------------------------------------------------------ commandes

def episodes_cibles(filtre: str | None) -> list[Path]:
    ds = sorted(p for p in EPISODES.iterdir() if p.is_dir() and (p / "narration.txt").exists())
    return [p for p in ds if not filtre or p.name.startswith(filtre)]


def cmd_estimer(cfg: dict, filtre: str | None) -> dict:
    prononc = cfg.get("prononciations", {})
    bilan = {"episodes": [], "total_mots": 0, "total_caracteres": 0, "cout_max_eur": 0.0}
    for ep in episodes_cibles(filtre):
        segs = lire_segments(ep)
        mots = sum(len(s["texte"].split()) for s in segs)
        car = sum(len(s["texte"]) for s in segs)
        cmax = sum(cout_max_eur(cfg, texte_prononce(s["texte"], prononc), cfg["consignes"]) for s in segs)
        pauses = sum((s["pause_apres"] or cfg["pause_defaut_s"]) for s in segs)
        duree_cible = mots / (cfg["debit_mots_minute_cible"] / 60.0) + pauses
        bilan["episodes"].append({
            "episode": ep.name, "segments": len(segs), "mots": mots, "caracteres": car,
            "duree_estimee_min": round(duree_cible / 60, 1), "cout_max_eur": round(cmax, 3),
        })
        bilan["total_mots"] += mots
        bilan["total_caracteres"] += car
        bilan["cout_max_eur"] += cmax
    bilan["cout_max_eur"] = round(bilan["cout_max_eur"], 3)
    bilan["deja_depense_eur"] = round(depense_cumulee_eur(), 4)
    bilan["enveloppe_accordee_eur"] = enveloppe_eur()
    return bilan


def produire(cfg: dict, filtre: str | None, segment: str | None, forcer: bool, echantillon: str | None = None) -> None:
    env = enveloppe_eur()
    if env is None:
        sys.exit("Aucune enveloppe de narration accordée dans BUDGET.json : aucun appel payant. Utiliser « estimer ».")
    manifest = charger_json(MANIFEST, {"segments": {}})
    prononc = cfg.get("prononciations", {})
    CACHE.mkdir(parents=True, exist_ok=True)
    cle = cle_api(cfg)
    if echantillon:
        travaux = [("echantillon", {"id": "E01", "texte": echantillon})]
    else:
        travaux = [(ep.name, s) for ep in episodes_cibles(filtre) for s in lire_segments(ep)
                   if not segment or s["id"] == segment]
    with Verrou():
        for ep_nom, s in travaux:
            dit = texte_prononce(s["texte"], prononc)
            h = empreinte(cfg, dit)
            cle_seg = f"{ep_nom}/{s['id']}"
            wav = CACHE / f"{h}.wav"
            if wav.exists() and not forcer:
                entree = manifest["segments"].get(cle_seg, {})
                if entree.get("empreinte") != h:
                    manifest["segments"][cle_seg] = {**entree, "empreinte": h, "wav": str(wav.relative_to(RACINE)), "statut": "genere", "source": "cache"}
                continue
            cmax = cout_max_eur(cfg, dit, cfg["consignes"])
            deja = depense_cumulee_eur()
            if deja + cmax > env:
                manifest["segments"][cle_seg] = {"empreinte": h, "statut": "bloque_budget"}
                ecrire_json(MANIFEST, manifest)
                sys.exit(f"Arrêt avant appel : {deja:.3f} € dépensés + {cmax:.3f} € réservés > enveloppe {env:.2f} €.")
            try:
                pcm, taux, usage = synthese(cfg, cle, dit)
            except urllib.error.HTTPError as e:
                statut = "quota" if e.code == 429 else f"erreur_http_{e.code}"
                manifest["segments"][cle_seg] = {"empreinte": h, "statut": statut}
                ecrire_json(MANIFEST, manifest)
                journaliser({"segment": cle_seg, "statut": statut, "cout_eur": 0.0})
                sys.exit(f"{cle_seg} : {statut}. État sauvegardé ; relancer plus tard reprendra ici.")
            duree = ecrire_wav(wav, pcm, taux)
            cout = cout_reel_eur(cfg, usage)
            journaliser({"segment": cle_seg, "empreinte": h, "modele": cfg["modele"], "voix": cfg["voix"],
                         "usage": usage, "cout_eur": round(cout, 6), "cout_max_reserve_eur": round(cmax, 6), "duree_s": round(duree, 2)})
            manifest["segments"][cle_seg] = {"empreinte": h, "wav": str(wav.relative_to(RACINE)), "duree_s": round(duree, 3),
                                           "taux": taux, "mots": len(s["texte"].split()), "statut": "genere",
                                           "debit_mpm": round(len(s["texte"].split()) / (duree / 60), 1) if duree else None}
            ecrire_json(MANIFEST, manifest)
            print(f"{cle_seg} : {duree:.1f} s, {cout:.4f} €")
    ecrire_json(MANIFEST, manifest)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("commande", choices=["presence", "estimer", "verifier-modele", "echantillon", "produire"])
    ap.add_argument("--episode")
    ap.add_argument("--segment")
    ap.add_argument("--forcer", action="store_true")
    a = ap.parse_args()
    cfg = charger_json(CONFIG, None)
    if cfg is None:
        sys.exit(f"Configuration absente : {CONFIG}")
    if a.commande == "presence":
        source = cfg.get("cle", {})
        nom = source.get("variable", "GEMINI_API_KEY")
        print(json.dumps({"variable": nom, "presente": bool(os.environ.get(nom))}, ensure_ascii=False))
        return
    if a.commande == "estimer":
        print(json.dumps(cmd_estimer(cfg, a.episode), ensure_ascii=False, indent=2))
    elif a.commande == "verifier-modele":
        print(json.dumps(verifier_modele(cfg), ensure_ascii=False, indent=2))
    elif a.commande == "echantillon":
        produire(cfg, None, None, a.forcer, echantillon=cfg["texte_echantillon"])
    else:
        produire(cfg, a.episode, a.segment, a.forcer)


if __name__ == "__main__":
    main()
