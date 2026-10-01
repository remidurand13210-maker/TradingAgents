# État de la mission — Les Mystères d'Akeb

Mise à jour : 01/10/2026, après la transmission de Codex, les recherches Bionic et la création de l'environnement Akeb.
Reprise dans l'environnement Akeb : voir `REPRISE_ENVIRONNEMENT_AKEB.md`.
**Passage de relais (01/10/2026)** : la révision v1 est confiée à la session de l'environnement Akeb. La session Default n'écrit plus sur la branche.
Statuts : préparé · généré · contrôlé · envoyé · soumis · publié · diffusé · **bloqué**.

## Synthèse

| Bloc | Statut | Détail |
|---|---|---|
| Dossier documentaire | **recherche Codex reçue** (11 dossiers, 143 sources lues intégralement) ; fusion faite : 250 sources, 285 assertions ; voir `recherche/AUDIT_CODEX.md`. Ancien état : partiel, à revérifier | 102 sources, 103 assertions, avec leur provenance : `bio_jeunesse` (extraits de moteur, session cloud) et 4 thèmes Bionic (LM Studio, 24 sources lues partiellement, non revérifiées ; voir `recherche/contre_verif/AUDIT_BIONIC.md`). Il manque : famille, travail et finances, découverte et enquête, pistes 2011-2019 (dont Glasgow), plateformes, emplacements. |
| Scripts des 4 épisodes + bande-annonce | **v1 écrits et validés** (01/10/2026, environnement Akeb) | 00 : 190 mots ; 01 : 1 711 ; 02 : 1 786 ; 03 : 1 544 ; 04 : 1 712 (total 6 943). `VERIFICATION_V1.md` et `VALIDATION.md` par épisode ; pages relues le 01/10 quand le réseau l'a permis, sinon lecture intégrale Codex. Ligne de l'épisode 4 **tranchée par Rémi** : « Un décès survenu après la disparition d'avril 2011 me paraît plus plausible qu'une fuite durable, à l'étranger ou plus près ; ni l'un ni l'autre n'est démontré. » Liste `CONTROLE_AVANT_PUBLICATION.md` à cocher pour chaque vidéo. |
| Narration Gemini 3.8 (Algieba) | prêt, non lancé — **enveloppe accordée** (`DEMANDE_ENVELOPPE.md`, scénario A 3,50 €, accord de Rémi le 01/10 ; tarif officiel lu : 0,50 $/M texte, 9 $/M audio, doublement le 01/01/2027) | Accès **vérifié dans l'environnement Akeb** (test non génératif réussi, aucun audio). Default reste sans identifiant. L'outil gère le mode proxy (clé ajoutée après la VM, `GEMINI_API_KEY` absente). Chiffrage après les scripts ; narration refusée sans `VALIDATION.md`. |
| Outils de montage et de contrôle | contrôlé | Testés de bout en bout ; sous-titres alignés sur la voix réelle ; moteur d'animation local. Maquette de comparaison de 27,1 s (moteur Python ou HyperFrames) produite en vrai MP4 1080p : voir `montage/maquette_comparaison/COMPARAISON.md`. **HyperFrames validé par Rémi le 01/10/2026** pour le rendu animé (gabarits pilotés par les storyboards) ; le moteur Python reste en secours. |
| Musique | généré | 3 nappes originales (`audio/musique/`, hors Git). |
| Identité visuelle | contrôlé | Avatar 800×800 et bannière 2560×1440 prêts **à installer** sur la chaîne. |
| Couverture exacte | généré | Reçue ; installée localement en `montage/assets/` (hors Git). |
| Shorts 1 à 3 | contrôlé — **défaut** | Mention « THRILLER DE FICTION » dans la zone masquée par l'interface Shorts ; 24 i/s au lieu de 30. Sous-titres v2 alignés livrés. Ré-export v2 à faire par Codex (aucune nouvelle narration). Voir `exports/shorts/CONTROLE_SHORTS.md`. Non publiés. |
| Chaîne YouTube | **configurée par Codex** | Les Mystères d'Akeb, `UCeY1bZMUcigbZX2VwJmln-Q`, @LesMysteresDAkeb ; imports privés par défaut. Avatar, bannière et playlists à installer. Non relue depuis le cloud. |
| Accès YouTube depuis le cloud | non donné | Aucun OAuth YouTube n'a été donné au conteneur ; publication par le Studio local côté Codex. `outils/youtube_api.py` reste prêt si un accès est un jour accordé. |
| Emplacements YouTube | préparé | 30 vidéos, 23 chaînes repérées par Codex (`publicite/EMPLACEMENTS_YOUTUBE.csv`) ; éligibilité publicitaire à contrôler dans Google Ads. |
| Publicité | Meta **soumis** (« Traitement en cours ») | 40 € média jusqu'au 04/10 23 h 59 + 10 € de réserve, soit 50 € engagés sur 100 €. Google Ads non inspecté. Reste au plus 50 €, taxes comprises. |

## Dépenses

| Poste | Montant | Source |
|---|---|---|
| Livre (API) | 1,409 € réservés | registre local transmis (estimation, pas une facture) |
| Shorts (API) | 0,025 € réservés | idem |
| Total sur le plafond de 5 € | 1,434 € | jamais remis à zéro |
| Narration des documentaires | 0 € | aucune enveloppe accordée |
| Publicité Meta | 50 € engagés (dépense réelle à relever) | transmission de Codex |
| Publicité Google | 0 € constaté | non inspecté |
| Cette session cloud | 0 € | aucun appel payant |

## Ce que cette session peut faire / ne peut pas faire

- **Peut** : écrire et vérifier les scripts à partir d'un dossier reçu par Git, monter, mixer, sous-titrer et contrôler ; produire la narration dès que la clé et une enveloppe existent (l'API Gemini est joignable) ; importer en privé sur YouTube par API dès qu'un identifiant OAuth existe (les hôtes Google d'authentification et d'API sont joignables).
- **Ne peut pas** : lire la presse, Wikipédia, YouTube ou Payhip (refus de la politique réseau) ; lancer de nouvelles recherches web (quota de la session épuisé) ; ouvrir un navigateur connecté ; lire le PC de Rémi.
- Les nouvelles variables d'environnement (`GEMINI_API_KEY`, `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, accès réseau, quota de recherches) **ne s'appliquent qu'à une nouvelle session**.
