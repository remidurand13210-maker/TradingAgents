"""Régénère recherche/CONTRADICTIONS_ET_LIMITES.md à partir de tous les dossiers bruts (avec provenance).

  python3 outils/contradictions.py      (à relancer après chaque fusion : outils/fusion_recherche.py)
"""
from __future__ import annotations

import csv
import glob
import json
import os
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
R = RACINE / "recherche"


def main() -> int:
    idx = json.loads((R / "INDEX_REFS.json").read_text(encoding="utf-8"))
    src = {r["id"]: r for r in csv.DictReader(open(R / "SOURCES.csv", encoding="utf-8"))}

    def refs(theme: str, liste: list) -> str:
        out = []
        for r in liste:
            g = idx.get(f"{theme}:{r}", idx.get(r, r))
            s = src.get(g)
            out.append(f"{g} ({s['media']}, {s['date_publication']}, {s['acces']})" if s else str(r))
        return "; ".join(out)

    fichiers = []
    for f in sorted(glob.glob(str(R / "brut_codex" / "*.json"))):
        fichiers.append((f, Path(f).stem + "_codex", "Codex — sources lues (voir AUDIT_CODEX.md)"))
    for f in sorted(glob.glob(str(R / "brut" / "*.json"))):
        fichiers.append((f, Path(f).stem, "préliminaire — extraits de moteur, session cloud"))
    for f in sorted(glob.glob(str(R / "contre_verif" / "bionic" / "*.json"))):
        fichiers.append((f, os.path.basename(f).replace("_deepseek.json", "") + "_bionic", "Bionic (LM Studio), non revérifié"))
    out = ["# Contradictions et limites\n",
           "> Généré par `outils/contradictions.py` à partir de tous les dossiers bruts. Chaque source est donnée avec son niveau "
           "d'accès. Priorité aux sources lues (Codex) ; les autres provenances servent de contre-vérification.\n"]
    n = 0
    for f, theme, prov in fichiers:
        d = json.load(open(f, encoding="utf-8"))
        if not d.get("contradictions") and not d.get("lacunes"):
            continue
        out.append(f"\n## {theme} — {prov}\n")
        for c in d.get("contradictions", []):
            n += 1
            out.append(f"\n### {c.get('sujet', '')}\n")
            for v in c.get("versions", []):
                out.append(f"- {v.get('version', '')} — {refs(theme, v.get('sources', []))}\n")
            out.append(f"\n**Traitement recommandé :** {c.get('traitement_recommande', '')}\n")
        if d.get("lacunes"):
            out.append("\n**Lacunes signalées :**\n\n" + "".join(f"- {l}\n" for l in d["lacunes"]))
    out.append("""
## Limites structurelles

- Les pièces du dossier d'instruction ne sont pas publiques : la chaîne ne connaît l'enquête qu'à travers les communications officielles et la presse.
- « Fait documenté » ne veut pas dire « vérifié par la justice ». Aucun procès n'a eu lieu ; XDDL est le principal suspect selon l'enquête, visé par un mandat d'arrêt.
- La formule officielle, répétée par le parquet, est que l'enquête n'a pas permis de déterminer s'il est mort ou en fuite. Ne jamais écrire « la justice a conclu au suicide ».
- Une ressemblance, une absence de nouvelles ou un mobile supposé ne sont pas des preuves. Aucun chiffre de probabilité.

## Formulations bannies

« affaire résolue », « la vérité cachée », « on l'a retrouvé », « ses vraies confessions », « preuve exclusive », « ce que la police ne vous dit pas » ; toute dissimulation attribuée aux autorités sans preuve ; toute invitation à identifier, localiser ou suivre un particulier.
""")
    (R / "CONTRADICTIONS_ET_LIMITES.md").write_text("".join(out), encoding="utf-8")
    return n


if __name__ == "__main__":
    print(main(), "divergences")
