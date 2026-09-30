"""Fusionne recherche/brut/*.json en CSV de référence à identifiants globaux.

Sorties : recherche/SOURCES.csv, recherche/ASSERTIONS.csv, recherche/CHRONOLOGIE.csv,
recherche/INDEX_REFS.json (réf. brute -> identifiant global), publicite/EMPLACEMENTS_YOUTUBE.csv,
recherche/CONSTATS_PLATEFORMES.csv.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

RACINE = Path(__file__).resolve().parent.parent
BRUT = RACINE / "recherche" / "brut"
SPECIAUX = {"plateformes", "commerce_droits", "emplacements_youtube"}
ORDRE_INCERT = {"faible": 0, "moyenne": 1, "forte": 2}


def norm_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return ""
    p = urlsplit(u)
    hote = p.netloc.lower().removeprefix("www.")
    chemin = p.path.rstrip("/")
    return urlunsplit(("https", hote, chemin, "", ""))


def ecrire_csv(chemin: Path, champs: list[str], lignes: list[dict]) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        for l in lignes:
            w.writerow({k: ("; ".join(map(str, v)) if isinstance(v, list) else v) for k, v in l.items()})


def main() -> dict:
    fichiers = sorted(BRUT.glob("*.json"))
    sources: dict[str, dict] = {}
    index: dict[str, str] = {}
    assertions, chrono, constats = [], [], []
    erreurs = []

    def sid_pour(src: dict, theme: str) -> str:
        cle = norm_url(src.get("url", "")) or f"sans-url:{src.get('titre','')}|{src.get('media','')}|{src.get('date_publication','')}"
        if cle not in sources:
            sources[cle] = {"id": f"S{len(sources) + 1:03d}", **{k: src.get(k, "") for k in (
                "titre", "url", "auteur_organisme", "media", "date_publication", "date_faits", "date_consultation",
                "acces", "type", "origine", "notes")}, "themes": [theme], "assertions": [], "incertitudes": []}
        else:
            s = sources[cle]
            if theme not in s["themes"]:
                s["themes"].append(theme)
            ordre_acces = ["extrait_moteur", "inaccessible", "lu_partiel", "lu_integral"]
            if src.get("acces") in ordre_acces and s.get("acces") in ordre_acces and ordre_acces.index(src["acces"]) > ordre_acces.index(s["acces"]):
                s["acces"] = src["acces"]
            if src.get("notes") and src["notes"] not in s["notes"]:
                s["notes"] = (s["notes"] + " | " + src["notes"]).strip(" |")
        return sources[cle]["id"]

    for f in fichiers:
        theme = f.stem
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            erreurs.append(f"{f.name}: {e}")
            continue
        for src in d.get("sources", []):
            gid = sid_pour(src, theme)
            if src.get("ref"):
                index[f"{theme}:{src['ref']}"] = gid
                index.setdefault(src["ref"], gid)
        if theme == "emplacements_youtube":
            continue
        for c in d.get("constats", []):
            constats.append({"ref": c.get("ref", ""), "theme": theme, "domaine": c.get("domaine", ""), "constat": c.get("constat", ""),
                             "sources": [index.get(f"{theme}:{r}", index.get(r, r)) for r in c.get("sources", [])],
                             "fiabilite": c.get("fiabilite", ""), "notes": c.get("notes", "")})
        for a in d.get("assertions", []):
            gid = f"A{len(assertions) + 1:03d}"
            refs = [index.get(f"{theme}:{r}", index.get(r, r)) for r in a.get("sources", [])]
            v = a.get("verification") or {}
            ligne = {"id": gid, "ref_brute": a.get("ref", ""), "theme": theme, "assertion": a.get("assertion", ""),
                     "categorie": a.get("categorie", ""), "attribution": a.get("attribution", ""), "date_faits": a.get("date_faits", ""),
                     "lieu": a.get("lieu", ""), "sources": refs, "nb_sources_independantes": a.get("nb_sources_independantes", ""),
                     "incertitude": a.get("incertitude", ""), "centrale": a.get("centrale", ""),
                     "verification": v.get("statut", ""), "commentaire_verification": v.get("commentaire", ""), "notes": a.get("notes", "")}
            assertions.append(ligne)
            index[f"{theme}:{a.get('ref', '')}"] = gid
            for r in refs:
                for s in sources.values():
                    if s["id"] == r:
                        s["assertions"].append(gid)
                        s["incertitudes"].append(a.get("incertitude", ""))
        for c in d.get("chronologie", []):
            chrono.append({"date": c.get("date", ""), "precision": c.get("precision", ""), "evenement": c.get("evenement", ""),
                           "categorie": c.get("categorie", ""), "sources": [index.get(f"{theme}:{r}", index.get(r, r)) for r in c.get("sources", [])],
                           "theme": theme, "note": c.get("note", "")})

    lignes_src = []
    for s in sources.values():
        inc = [i for i in s.pop("incertitudes") if i in ORDRE_INCERT]
        s["incertitude_max"] = max(inc, key=ORDRE_INCERT.get) if inc else ""
        s["assertions_etayees"] = s.pop("assertions")
        lignes_src.append(s)
    ecrire_csv(RACINE / "recherche" / "SOURCES.csv",
               ["id", "titre", "url", "auteur_organisme", "media", "date_publication", "date_faits", "date_consultation", "acces",
                "type", "origine", "assertions_etayees", "incertitude_max", "themes", "notes"], lignes_src)
    ecrire_csv(RACINE / "recherche" / "ASSERTIONS.csv",
               ["id", "theme", "assertion", "categorie", "attribution", "date_faits", "lieu", "sources", "nb_sources_independantes",
                "incertitude", "centrale", "verification", "commentaire_verification", "notes", "ref_brute"], assertions)
    chrono.sort(key=lambda c: (re.sub(r"[^0-9-]", "", c["date"]) or "9999"))
    ecrire_csv(RACINE / "recherche" / "CHRONOLOGIE.csv",
               ["date", "precision", "evenement", "categorie", "sources", "theme", "note"], chrono)
    if constats:
        ecrire_csv(RACINE / "recherche" / "CONSTATS_PLATEFORMES.csv",
                   ["ref", "theme", "domaine", "constat", "sources", "fiabilite", "notes"], constats)
    emp = BRUT / "emplacements_youtube.json"
    nb_videos = 0
    if emp.exists():
        try:
            d = json.loads(emp.read_text(encoding="utf-8"))
            vids = d.get("videos", [])
            nb_videos = len(vids)
            ecrire_csv(RACINE / "publicite" / "EMPLACEMENTS_YOUTUBE.csv",
                       ["type", "url", "titre", "chaine", "url_chaine", "date_publication", "duree", "sujet_principal", "langue",
                        "date_controle", "confirme_par_lecture_page", "notes"],
                       [{"type": "video", **v} for v in vids] + [{"type": "chaine", "url": c.get("url", ""), "titre": c.get("nom", ""),
                        "chaine": c.get("nom", ""), "url_chaine": c.get("url", ""), "date_controle": c.get("date_controle", ""),
                        "notes": (c.get("pertinence", "") + " " + c.get("notes", "")).strip()} for c in d.get("chaines", [])])
        except Exception as e:  # noqa: BLE001
            erreurs.append(f"emplacements: {e}")
    (RACINE / "recherche" / "INDEX_REFS.json").write_text(json.dumps(index, ensure_ascii=False, indent=0), encoding="utf-8")
    return {"fichiers": len(fichiers), "sources": len(lignes_src), "assertions": len(assertions), "chronologie": len(chrono),
            "constats": len(constats), "videos_emplacements": nb_videos, "erreurs": erreurs}


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
