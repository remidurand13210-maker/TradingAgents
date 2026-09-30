# État de la mission — Les Mystères d'Akeb

Mise à jour : 30/09/2026, fin de la première session cloud.
Statuts : préparé · généré · contrôlé · envoyé · soumis · publié · diffusé · **bloqué**.

## Synthèse

| Bloc | Statut | Détail |
|---|---|---|
| Dossier documentaire | **bloqué** | Réseau cloud fermé aux sites + quota de recherches épuisé. Seul `bio_jeunesse.json` existe, bâti sur des extraits de moteur (non lus). Reprise : `MISSION_REPRISE.md` (voie Antigravity ou voie réseau). |
| Scripts des 4 épisodes + bande-annonce | **bloqué** (dépend du dossier) | Workflow d'écriture et de vérification prêt : `outils/workflows/ecriture_episodes.js`. |
| Narration Gemini 3.8 (Algieba) | **bloqué** | Scripts à écrire, tarif à vérifier, enveloppe à accorder, clé non disponible dans la session cloud. Outil prêt : `outils/narration_gemini.py` (cache, verrou, plafond, reprise). |
| Outils de montage et de contrôle | contrôlé | Testés de bout en bout sur un épisode fictif : 1920×1080, 30 i/s, H.264/AAC, −16,0 LUFS, crête vraie ≤ −1,5 dBTP, SRT sans chevauchement, planche d'images. |
| Musique | généré | 3 nappes originales synthétisées localement (`audio/musique/`, hors Git). |
| Identité visuelle | contrôlé (visuellement) | Avatar, bannière, modèles de cartons, cartes et miniature (`chaine/visuels/`). |
| Couverture exacte du roman | **bloqué** | Fichier absent de l'environnement cloud ; attendu en `montage/assets/couverture_akeb.png`. |
| Shorts 1 à 3 (existants) | non vérifié | Exports sur le PC de Rémi, inaccessibles ici. Rien n'est refait. |
| Chaîne YouTube « Les Mystères d'Akeb » | préparé | Textes, liens, playlists, visuels prêts. Chaîne non créée ; identifiant non vérifié (youtube.com bloqué). Création : connexion de Rémi. |
| Métadonnées | préparé | Règles communes et UTM : `chaine/METADONNEES_YOUTUBE.md`. Métadonnées par épisode générées avec les scripts. |
| Calendrier | préparé | `chaine/CALENDRIER.md` (J0 = tous les exports contrôlés). |
| Publicité | préparé | `publicite/PLAN_100_EUROS.md`. Campagnes existantes **non inspectées** (Google Ads et Meta inaccessibles ici). Liste d'emplacements à constituer. Aucune dépense. |
| Droits des médias | préparé | `recherche/DROITS_MEDIAS.csv`. |

## Éléments de publication

| Élément | Statut | Lien réel |
|---|---|---|
| Bande-annonce | bloqué (script) | — |
| Épisode 1 | bloqué (script) | — |
| Épisode 2 | bloqué (script) | — |
| Épisode 3 | bloqué (script) | — |
| Épisode 4 | bloqué (script) | — |
| Short 1 « Il aurait dû se taire » | non vérifié (PC de Rémi) | — |
| Short 2 « Le faux prêtre » | non vérifié (PC de Rémi) | — |
| Short 3 « Après la disparition » | non vérifié (PC de Rémi) | — |
| Chaîne | préparé | — |
| Campagne YouTube | préparé (plan) | — |

## Dépenses de cette session

- API payantes : **0 €** (aucun appel Gemini ni autre service facturé).
- Publicité : **0 €**.
- Registres du livre et des Shorts (`depenses.json`, `depenses_shorts.json`, `budget_resume.json`) : non lisibles ici ; à reprendre tels quels, jamais remis à zéro.

## Environnement constaté (sans secret)

- Session Claude Code dans le cloud (Linux) : pas d'accès à `C:/Users/rddur/…`, pas d'Antigravity, pas de navigateur connecté aux comptes.
- Joignables : GitHub, PyPI, API Gemini (`generativelanguage.googleapis.com`). Bloqués : presse, Wikipédia, archives, YouTube, Payhip, documentation Google.
- Voix témoin locale (Kokoro) installable pour mesurer des durées en interne : **jamais utilisée dans un export livré ou publié**. Toute la narration publiée sera Gemini 3.8.
