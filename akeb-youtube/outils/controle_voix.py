"""Contrôle voix/texte : transcription Gemini d'un WAV narré, puis comparaison mot à mot avec le texte attendu.

Repère les mots sautés, doublés ou ajoutés (consigne lue à voix haute, artefact).
Coût journalisé dans audio/registre_narration.jsonl (même enveloppe que la narration).
La clé n'est jamais lue ni affichée : mode proxy de narration_gemini.

Usage :
  python3 controle_voix.py <wav> --texte "texte attendu"
  python3 controle_voix.py --manifest [--episode 00]      # tous les segments générés d'un épisode
"""
from __future__ import annotations

import argparse
import base64
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import narration_gemini as ng  # noqa: E402

MODELE = "gemini-3.8-flash"  # gemini-2.5-flash : 404 « no longer available to new users » (01/10/2026)
# Tarifs de gemini-3.8-flash non confirmés pour l'audio (lecture du 01/10/2026 ambiguë : 0,75 $/M général, 3,00 $/M audio ?).
# Majorants prudents : 3,00 $/M en entrée audio, 20 $/M en sortie (réflexion comprise). Coût réel ≤ coût journalisé.
USD_ENTREE_AUDIO, USD_SORTIE = 3.00, 20.00
CONSIGNE = ("Transcris exactement, mot pour mot, ce qui est prononcé dans cet audio en français. "
            "N'ajoute rien, ne corrige rien, n'écris aucun commentaire ; écris les nombres comme ils sont prononcés, en lettres.")


def normaliser(t: str) -> list[str]:
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[’'\-]", " ", t)
    return re.findall(r"[a-z0-9]+", t)


def homophone(mot: str) -> str:
    """Forme sonore grossière : les marques d'accord muettes du français ne s'entendent pas."""
    for fin in ("aient", "ait", "ent", "es", "e", "s", "x"):
        if mot.endswith(fin) and len(mot) > len(fin) + 1:
            return mot[: -len(fin)] + ("ai" if fin in ("aient", "ait") else "")
    return mot


def transcrire(cfg: dict, wav: Path) -> tuple[str, float]:
    cle = ng.cle_api(cfg)
    corps = {"contents": [{"parts": [
        {"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(wav.read_bytes()).decode()}},
        {"text": CONSIGNE}]}],
        "generationConfig": {"temperature": 0}}
    rep = ng.requete("POST", f"{ng.API}/models/{MODELE}:generateContent", cle, corps)
    texte = "".join(p.get("text", "") for p in rep["candidates"][0]["content"]["parts"])
    u = rep.get("usageMetadata", {})
    usd = u.get("promptTokenCount", 0) / 1e6 * USD_ENTREE_AUDIO + u.get("candidatesTokenCount", 0) / 1e6 * USD_SORTIE
    return texte.strip(), usd * cfg["tarifs"]["eur_par_usd"]


def comparer(attendu: str, entendu: str) -> list[str]:
    a, e = normaliser(attendu), normaliser(entendu)
    ecarts = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=e, autojunk=False).get_opcodes():
        if op == "replace" and any(c.isdigit() for x in a[i1:i2] for c in x):
            continue  # nombres ou sigles en chiffres (M6, 2011), entendus en lettres
        if "".join(a[i1:i2]) == "".join(e[j1:j2]):
            continue  # simple découpage (net surf / netsurf)
        if op == "replace" and i2 - i1 == j2 - j1 and all(
                homophone(x) == homophone(y) for x, y in zip(a[i1:i2], e[j1:j2])):
            continue  # homophones (accords muets : vue/vu, avaient/avait)
        if op != "equal":
            ecarts.append(f"{op}: attendu « {' '.join(a[i1:i2])} » / entendu « {' '.join(e[j1:j2])} »")
    return ecarts


def controler(cfg: dict, wav: Path, attendu: str, etiquette: str) -> dict:
    env = ng.enveloppe_eur()
    if env is None or ng.depense_cumulee_eur() + 0.01 > env:
        sys.exit("Enveloppe absente ou épuisée : contrôle non lancé.")
    entendu, cout = transcrire(cfg, wav)
    ng.journaliser({"segment": f"controle/{etiquette}", "modele": MODELE, "cout_eur": round(cout, 6)})
    ecarts = comparer(attendu, entendu)
    return {"segment": etiquette, "ecarts": ecarts, "entendu": entendu, "cout_eur": round(cout, 5)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("wav", nargs="?")
    ap.add_argument("--texte")
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--episode")
    a = ap.parse_args()
    cfg = ng.charger_json(ng.CONFIG, None)
    if not a.manifest:
        r = controler(cfg, Path(a.wav), a.texte, Path(a.wav).stem)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    manifest = ng.charger_json(ng.MANIFEST, {"segments": {}})
    prononc = cfg.get("prononciations", {})
    bilan = []
    for ep in ng.episodes_cibles(a.episode):
        for s in ng.lire_segments(ep):
            cle_seg = f"{ep.name}/{s['id']}"
            m = manifest["segments"].get(cle_seg, {})
            if m.get("statut") != "genere":
                continue
            if m.get("controle", {}).get("empreinte") == m.get("empreinte"):
                bilan.append({"segment": cle_seg, "ecarts": m["controle"]["ecarts"], "deja": True})
                continue
            r = controler(cfg, ng.RACINE / m["wav"], s["texte"], cle_seg)
            m["controle"] = {"empreinte": m["empreinte"], "ecarts": r["ecarts"]}
            ng.ecrire_json(ng.MANIFEST, manifest)
            bilan.append({"segment": cle_seg, "ecarts": r["ecarts"]})
    print(json.dumps({"segments": len(bilan), "avec_ecarts": [b for b in bilan if b["ecarts"]]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
