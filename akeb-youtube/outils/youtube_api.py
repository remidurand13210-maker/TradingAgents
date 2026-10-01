"""Accès YouTube depuis le conteneur cloud, par OAuth « appareil à saisie limitée ».

Pourquoi ce flux : pas de navigateur ni de redirection localhost dans le cloud. Rémi saisit
un code court sur https://www.google.com/device (téléphone ou PC), accepte l'écran de
consentement de SA chaîne, et le conteneur reçoit un jeton. Aucune clé ni jeton n'est
affiché, écrit dans Git ou dans un journal.

Prérequis (Rémi, une fois) : projet Google Cloud avec « YouTube Data API v3 » activée,
identifiant OAuth de type « TV et appareils à saisie limitée », puis dans les réglages
de l'environnement cloud : YOUTUBE_CLIENT_ID et YOUTUBE_CLIENT_SECRET (nouvelle session).

  python3 youtube_api.py etat                 # présence des variables, jeton en cache (oui/non)
  python3 youtube_api.py connecter            # affiche l'adresse et le code à saisir, attend l'accord
  python3 youtube_api.py chaine               # lecture authentifiée : la chaîne attendue est-elle la bonne ?
  python3 youtube_api.py envoyer <mp4> <metadonnees.json>   # import PRIVÉ, idempotent

Limites à connaître (documentation Google à relire au moment de l'usage) :
- un projet API non audité peut voir ses imports forcés en « privé » : la mise en public se fait dans Studio ;
- les sous-titres (captions.insert) et miniatures personnalisées demandent d'autres autorisations ou une
  chaîne vérifiée : ils se déposent dans Studio si l'API les refuse.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
JETON = Path.home() / ".config" / "akeb" / "youtube_jeton.json"  # hors dépôt
CHAINE_ATTENDUE = "UCeY1bZMUcigbZX2VwJmln-Q"  # Les Mystères d'Akeb (@LesMysteresDAkeb)
CHAINES_INTERDITES = {"UCffzp_A-m10RrjLhnuQhvjg"}  # La Brig'ads : ne jamais y publier
PORTEE = "https://www.googleapis.com/auth/youtube"
PUBLICATIONS = RACINE / "PUBLICATIONS.csv"


def _post(url: str, champs: dict) -> dict:
    req = urllib.request.Request(url, data=urllib.parse.urlencode(champs).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}") | {"_http": e.code}


def _client() -> tuple[str, str]:
    cid, sec = os.environ.get("YOUTUBE_CLIENT_ID"), os.environ.get("YOUTUBE_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET absents de l'environnement (valeurs jamais affichées).")
    return cid, sec


def _sauver(jeton: dict) -> None:
    JETON.parent.mkdir(parents=True, exist_ok=True)
    jeton["obtenu_a"] = time.time()
    JETON.write_text(json.dumps(jeton), encoding="utf-8")
    os.chmod(JETON, 0o600)


def _acces() -> str:
    if not JETON.exists():
        sys.exit("Pas de jeton : lancer « connecter ».")
    j = json.loads(JETON.read_text(encoding="utf-8"))
    if time.time() > j["obtenu_a"] + j.get("expires_in", 3600) - 120:
        cid, sec = _client()
        r = _post("https://oauth2.googleapis.com/token", {"client_id": cid, "client_secret": sec,
                                                           "refresh_token": j["refresh_token"], "grant_type": "refresh_token"})
        if "access_token" not in r:
            sys.exit(f"Renouvellement refusé ({r.get('error', r.get('_http'))}) : relancer « connecter ».")
        j.update(r)
        _sauver(j)
    return j["access_token"]


def _api(methode: str, url: str, corps: dict | None = None, entetes: dict | None = None):
    req = urllib.request.Request(url, data=json.dumps(corps).encode() if corps is not None else None, method=methode)
    req.add_header("Authorization", "Bearer " + _acces())
    req.add_header("Content-Type", "application/json; charset=UTF-8")
    for k, v in (entetes or {}).items():
        req.add_header(k, v)
    return urllib.request.urlopen(req, timeout=120)


def cmd_etat() -> None:
    print(json.dumps({"YOUTUBE_CLIENT_ID": bool(os.environ.get("YOUTUBE_CLIENT_ID")),
                      "YOUTUBE_CLIENT_SECRET": bool(os.environ.get("YOUTUBE_CLIENT_SECRET")),
                      "jeton_en_cache": JETON.exists()}, ensure_ascii=False))


def cmd_connecter() -> None:
    cid, sec = _client()
    d = _post("https://oauth2.googleapis.com/device/code", {"client_id": cid, "scope": PORTEE})
    if "device_code" not in d:
        sys.exit(f"Demande refusée par Google : {d.get('error', d.get('_http'))} {d.get('error_description', '')}")
    print(f"Ouvrir {d['verification_url']} et saisir le code {d['user_code']} (valable {d['expires_in'] // 60} min).")
    print("Choisir le compte propriétaire de « Les Mystères d'Akeb », vérifier l'écran de consentement, accepter.", flush=True)
    attente = d.get("interval", 5)
    fin = time.time() + d["expires_in"]
    while time.time() < fin:
        time.sleep(attente)
        r = _post("https://oauth2.googleapis.com/token", {"client_id": cid, "client_secret": sec, "device_code": d["device_code"],
                                                           "grant_type": "urn:ietf:params:oauth:grant-type:device_code"})
        if "access_token" in r:
            _sauver(r)
            print("Accord reçu ; jeton stocké hors dépôt. Lancer « chaine » pour vérifier la chaîne.")
            return
        if r.get("error") == "slow_down":
            attente += 5
        elif r.get("error") not in ("authorization_pending",):
            sys.exit(f"Arrêt : {r.get('error')}")
    sys.exit("Code expiré : relancer « connecter ».")


def cmd_chaine() -> dict:
    with _api("GET", "https://www.googleapis.com/youtube/v3/channels?part=snippet,status&mine=true") as r:
        d = json.loads(r.read())
    chaines = [{"id": c["id"], "titre": c["snippet"]["title"], "identifiant": c["snippet"].get("customUrl")} for c in d.get("items", [])]
    ok = any(c["id"] == CHAINE_ATTENDUE for c in chaines)
    print(json.dumps({"chaines_du_jeton": chaines, "chaine_attendue_presente": ok}, ensure_ascii=False, indent=2))
    return {"ok": ok, "chaines": chaines}


def _deja_envoye(empreinte: str) -> str | None:
    if PUBLICATIONS.exists():
        for ligne in PUBLICATIONS.read_text(encoding="utf-8").splitlines():
            if empreinte in ligne and ",youtube," in ligne:
                return ligne
    return None


def cmd_envoyer(mp4: Path, meta_json: Path) -> None:
    verif = cmd_chaine()
    if not verif["ok"] or any(c["id"] in CHAINES_INTERDITES for c in verif["chaines"]):
        sys.exit("Chaîne inattendue pour ce jeton : aucun import.")
    empreinte = hashlib.sha256(mp4.read_bytes()).hexdigest()[:16]
    deja = _deja_envoye(empreinte)
    if deja:
        sys.exit(f"Déjà importé (aucun doublon) : {deja}")
    meta = json.loads(meta_json.read_text(encoding="utf-8"))
    corps = {
        "snippet": {"title": meta["titre"], "description": meta["description"], "tags": meta.get("tags", []),
                    "categoryId": meta.get("categoryId", "27"), "defaultLanguage": "fr", "defaultAudioLanguage": "fr"},
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False, "embeddable": True},
    }
    taille = mp4.stat().st_size
    with _api("POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", corps,
              {"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(taille)}) as r:
        session = r.headers["Location"]
    req = urllib.request.Request(session, data=mp4.read_bytes(), method="PUT")
    req.add_header("Authorization", "Bearer " + _acces())
    req.add_header("Content-Type", "video/mp4")
    with urllib.request.urlopen(req, timeout=3600) as r:
        video = json.loads(r.read())
    vid = video["id"]
    with open(PUBLICATIONS, "a", encoding="utf-8") as f:
        f.write(f"{mp4.stem},video,youtube,\"{meta['titre']}\",{mp4.name},envoye_prive,{vid},https://youtu.be/{vid},"
                f"{time.strftime('%Y-%m-%d')},empreinte:{empreinte},statut de traitement à contrôler dans Studio\n")
    print(f"Importé en PRIVÉ : https://youtu.be/{vid} (traitement en cours côté YouTube ; non public).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    c = sys.argv[1]
    if c == "etat":
        cmd_etat()
    elif c == "connecter":
        cmd_connecter()
    elif c == "chaine":
        cmd_chaine()
    elif c == "envoyer":
        cmd_envoyer(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        sys.exit(__doc__)
