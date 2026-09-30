# Les Mystères d'Akeb — dossier de production

Chaîne documentaire distincte de La Brig'ads. Première saison : l'affaire Xavier Dupont de Ligonnès, en quatre épisodes et une bande-annonce, plus trois Shorts de promotion du roman **La dernière correction** (Akeb, fiction).

**Commencer par** : `ETAT.md` (où en est chaque élément), puis `MISSION_REPRISE.md` (ce qu'il reste à faire, dans l'ordre).

## Arborescence

| Chemin | Contenu |
|---|---|
| `ETAT.md` | état réel de chaque élément et blocages |
| `MISSION_REPRISE.md` | procédure de reprise pas à pas |
| `BUDGET.json` | plafonds (publicité 100 € dont 50 € le jour 1 ; narration sur enveloppe accordée) et dépenses constatées |
| `PUBLICATIONS.csv` | identifiants et liens réels, une ligne par publication |
| `PROMPT_RECHERCHE_ANTIGRAVITY.md` | prompt complet pour faire la recherche avec Antigravity sur le PC de Rémi |
| `PROMPT_RECHERCHE_DEEPSEEK.md` | prompt de contre-vérification indépendante (DeepSeek) |
| `recherche/` | `SOURCES.csv`, `ASSERTIONS.csv`, `CHRONOLOGIE.csv`, `DETAILS_MOINS_CONNUS.md`, `CONTRADICTIONS_ET_LIMITES.md`, `DROITS_MEDIAS.csv` ; `brut/` = Antigravity ; `brut_codex/` = seconde passe Codex (branche `codex/akeb-recherche`) ; `contre_verif/` = DeepSeek |
| `PROMPT_RECHERCHE_CODEX.md` | prompt de seconde recherche indépendante pour Codex |
| `episodes/<nn_nom>/` | `script_annote.md`, `narration.txt`, `storyboard.csv`, `metadonnees.md`, `chapitres_mesures.txt` |
| `chaine/` | présentation, identité, calendrier, métadonnées communes, visuels |
| `audio/` | direction vocale, configuration de narration, manifeste des segments, registre des dépenses de narration, musique |
| `montage/` | frises de temps mesurées ; `assets/couverture_akeb.png` (à fournir) |
| `exports/` | vidéos, sous-titres et miniatures (fichiers lourds hors Git) |
| `publicite/` | plan 100 €, emplacements YouTube |
| `preuves/` | rapports de contrôle, planches d'images, captures de configuration |
| `outils/` | scripts techniques (aucun secret) et workflows |

## Outils

| Commande | Rôle |
|---|---|
| `python3 outils/fusion_recherche.py` | fusionne `recherche/brut/*.json` en CSV à identifiants globaux |
| `python3 outils/narration_gemini.py estimer` | volumes et coût maximal de la narration, sans appel |
| `python3 outils/narration_gemini.py verifier-modele` | vérifie que `gemini-3.8-flash-tts` est disponible pour le compte (aucune substitution) |
| `python3 outils/narration_gemini.py echantillon` / `produire [--episode 01] [--segment S12]` | narration segmentée, cache par empreinte, verrou, plafond, reprise après quota |
| `python3 outils/montage.py <épisode> [--maquette]` | cartons, synchronisation, mixage, −16 LUFS, SRT, chapitres mesurés |
| `python3 outils/controle.py exports/episodes/<fichier>.mp4 --timeline … --voix …` | contrôles techniques et planche d'images |
| `python3 outils/identite.py` | avatar et bannière |
| `python3 outils/musique.py <sortie.wav> <durée> <variante>` | nappe musicale originale |

Dépendances Python : `pillow numpy scipy soundfile pyloudnorm` (+ `keyring` sur le PC de Rémi si la clé y est stockée). ffmpeg requis.

## Règles qui ne changent pas

Faits sourcés et attribués ; hypothèses signalées ; fiction nommée comme telle. Aucun portrait réel, aucun extrait télé, aucune musique tierce. Aucune identification de particuliers. Narration publiée : Gemini 3.8 Flash TTS, voix Algieba. Aucune dépense hors plafonds accordés.
