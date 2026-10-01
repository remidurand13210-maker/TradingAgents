# Point de reprise — passage dans l'environnement « Akeb - production YouTube »

Préparé le 01/10/2026 dans la session cloud actuelle, qui tourne sur l'environnement **Default**. Rien n'a été détruit.
**Accès Gemini vérifié dans l'environnement Akeb** (session_01EaidoXE4psibiFYZg9VgPc) : `verifier-modele` a terminé avec le code 0 et une réponse 2xx, et la fiche `models/gemini-3.8-flash-tts` est arrivée par le proxy, sans audio généré. Default reste sans identifiant (403, normal).

## 1. Ce qui est déjà dans le dépôt (branche `claude/akeb-youtube-channel-kvu47n`)

Dépôt `remidurand13210-maker/TradingAgents` (public), dossier `akeb-youtube/`. Tout le travail de référence s'y trouve :
dossier de recherche fusionné avec provenance, audit Bionic, outils (identité visuelle, musique, narration, montage, sous-titres alignés, contrôle, accès YouTube), documents de chaîne et de publicité, sous-titres v2 et contrôle des Shorts, prompts de recherche, workflows, état, budget.
Les brouillons v0 des épisodes 2, 3 et 4 y sont versés dès qu'ils sont terminés (voir `ETAT.md`).

Pour reprendre : ouvrir une session sur l'environnement **Akeb - production YouTube**, branche `claude/akeb-youtube-channel-kvu47n`, et dire :
« Reprends la mission Akeb depuis akeb-youtube/REPRISE_ENVIRONNEMENT_AKEB.md. »

## 2. Fichiers hors dépôt à récupérer

| Élément | Où il était ici | Utilité | Comment le récupérer |
|---|---|---|---|
| Archive de Codex `Transmission_Akeb_Claude_Cloud_2026-10-01.zip` (36 fichiers, 16 Mo) | `/home/user/akeb-transmission/` | couvertures exactes, Shorts originaux (MP4, voix WAV, textes, SRT), synopsis, brief mis à jour | **la rejoindre de nouveau** dans la nouvelle session ; la décompresser HORS du dépôt (ex. `/home/user/akeb-transmission/`), puis copier `Livre/Couverture_ebook.png` → `akeb-youtube/montage/assets/couverture_akeb.png` et `Livre/Couverture_audio.png` → `akeb-youtube/montage/assets/couverture_akeb_audio.png` |
| Archive Bionic `Recherches_Bionic_a_verifier_2026-10-01.zip` | `/home/user/akeb-bionic/` | — | **inutile** : son contenu est déjà versé dans `recherche/contre_verif/bionic/` |
| Nappes musicales (3 × 52 Mo) | `akeb-youtube/audio/musique/` (hors Git) | fond musical original | **régénérables à l'identique** (graine fixe) : `python3 outils/musique.py audio/musique/nappe_archives.wav 180 archives`, puis `… nappe_enquete.wav 180 enquete` et `… nappe_conclusion.wav 180 conclusion` |
| Modèle de voix témoin Kokoro (338 Mo) | `akeb-youtube/outils/modeles/` | — | **inutile** : toute la narration se fait avec Gemini 3.8, à la demande de Rémi |
| Rendus et caches de test | `montage/rendu/`, `audio/cache/` | — | inutiles (aucun rendu réel n'existe encore) |

Ni le manuscrit, ni l'EPUB, ni le PDF, ni l'extrait audio ne doivent entrer dans le dépôt public.

## 3. Préparation de la nouvelle session (sans coût)

```
cd akeb-youtube
pip install pillow numpy scipy soundfile pyloudnorm   # gestionnaires de paquets autorisés
ffmpeg -version | head -1                             # requis pour le montage
python3 outils/narration_gemini.py presence           # attendu : mode_effectif = proxy, variable_presente = false
python3 outils/narration_gemini.py verifier-modele    # test REST non génératif via le proxy
```

- **Identifiant API Gemini** : le proxy ajoute l'en-tête `x-goog-api-key` après la sortie de la VM. `GEMINI_API_KEY` doit rester **absente** du conteneur. L'outil n'envoie alors aucun en-tête de clé, ni vide ni factice, et ne contourne pas le proxy.
  - Résultat attendu si l'identifiant est connecté : nom et méthodes du modèle `gemini-3.8-flash-tts`.
  - Si le modèle est introuvable (404) : arrêt, sans substitution.
  - Si la réponse est 401 ou 403 : l'identifiant n'est pas connecté dans cet environnement.
- **Aucune génération payante** avant le chiffrage des épisodes et l'accord de Rémi sur une enveloppe (`BUDGET.json › narration.enveloppe_accordee_eur`). De plus, l'outil refuse de narrer tout épisode sans `VALIDATION.md` (« valide: oui »).

## 4. Ordre de travail dans l'environnement Akeb

1. Relire `ETAT.md`, `BUDGET.json`, `PUBLICATIONS.csv`, `recherche/contre_verif/AUDIT_BIONIC.md`.
2. **Revérifier sur pages lues** les sources des brouillons v0. Le réseau autorise désormais les domaines des sources Bionic, et une nouvelle session dispose d'un nouveau quota de recherches. Priorité aux éléments fragiles listés dans l'audit, puis aux sources `extrait_moteur` qui portent une phrase des scripts.
3. **Compléter la recherche manquante** avec `outils/workflows/recherche_themes.js` :
   - groupe 1 : `bio_jeunesse`, `bio_famille`, `bio_travail_finances` (épisode 1) ;
   - groupe 2 : `decouverte_enquete`, `pistes_2011_2019` (épisode 3, dont Glasgow 2019) ;
   - groupe 3 : `plateformes`, `commerce_droits`, `emplacements_youtube`.
   Si un domaine est refusé, il faut l'ajouter à la liste du réseau personnalisé (rien n'est contourné).
4. Mettre à jour les brouillons, écrire l'épisode 1 et la bande-annonce, puis faire la vérification croisée. Créer `VALIDATION.md` par épisode seulement quand chaque phrase factuelle repose sur une page lue.
5. Lire le tarif officiel du modèle, renseigner `audio/config_narration.json › tarifs`, lancer `narration_gemini.py estimer` et envoyer **une seule** demande d'enveloppe à Rémi.
6. Après accord : échantillon de voix, contrôle, narration segmentée, montage, contrôles, miniatures, chapitres mesurés.
7. **Publication** : par le Studio local, côté Codex (aucun OAuth YouTube n'a été donné au conteneur). Les fichiers à importer sont préparés et consignés dans `PUBLICATIONS.csv`.

## 4 bis. Synchronisation avec l'environnement Akeb

1. `git fetch origin claude/akeb-youtube-channel-kvu47n && git checkout claude/akeb-youtube-channel-kvu47n && git pull`. Dernier commit à attendre : voir le message de clôture de la session Default.
2. Joindre de nouveau l'archive de Codex et la décompresser dans `/home/user/akeb-transmission/`. Recopier les couvertures dans `akeb-youtube/montage/assets/`.
3. `pip install pillow numpy scipy soundfile pyloudnorm`. Puis, pour l'option HyperFrames :
   `mkdir -p /home/user/akeb-hf && cd /home/user/akeb-hf && npm init -y && PUPPETEER_SKIP_DOWNLOAD=1 npm i hyperframes@0.8.99 gsap@3 && npx hyperframes telemetry disable`.
   Ensuite, exporter `HYPERFRAMES_BROWSER_PATH` vers le Chromium headless préinstallé (`/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell`), puis lancer `npx hyperframes doctor`.
4. Régénérer les nappes (`outils/musique.py`) et les éléments de maquette (`python3 montage/maquette_comparaison/preparer.py`).
5. Un seul environnement écrit à la fois sur la branche : avant d'y travailler, la session Akeb fait un `git pull`, et la session Default s'arrête.

## 5. Budgets (inchangés)

- Publicité : 100 € au total, dont 50 € déjà engagés sur Meta (40 € de média jusqu'au 04/10 à 23 h 59, plus 10 € de réserve). Il reste au plus 50 €, taxes comprises, après inspection de Google Ads.
- Livre et Shorts : 1,434 € réservés sur 5 €. Ce plafond ne finance pas les documentaires.
- Narration des documentaires : 0 € dépensé ; enveloppe à demander après chiffrage.
