# État de la mission — Les Mystères d'Akeb

Mise à jour : 01/10/2026, après réception de la transmission de Codex.
Statuts : préparé · généré · contrôlé · envoyé · soumis · publié · diffusé · **bloqué**.

## Synthèse

| Bloc | Statut | Détail |
|---|---|---|
| Dossier documentaire | **bloqué** | Réseau cloud fermé à la presse et quota de recherches de la session épuisé. Seul `bio_jeunesse.json` existe (extraits de moteur). Recherches confiées à Antigravity et Codex (prompts dans le dépôt) ; rien de reçu à ce jour. Le retour DeepSeek/LM Studio n'est **pas** parvenu à cette session. |
| Scripts des 4 épisodes + bande-annonce | **bloqué** (dépend du dossier) | Workflow d'écriture et de vérification prêt (`outils/workflows/ecriture_episodes.js`). Il démarre dès l'arrivée de la recherche. |
| Narration Gemini 3.8 (Algieba) | **bloqué** | `GEMINI_API_KEY` absente de la session ; chiffrage impossible tant que les scripts n'existent pas. Configuration alignée sur la direction validée des Shorts. |
| Outils de montage et de contrôle | contrôlé | Testés de bout en bout ; sous-titres désormais alignés par propositions sur les pauses réelles de la voix. |
| Musique | généré | 3 nappes originales (`audio/musique/`, hors Git). |
| Identité visuelle | contrôlé | Avatar 800×800 et bannière 2560×1440 prêts **à installer** sur la chaîne. |
| Couverture exacte | généré | Reçue ; installée localement en `montage/assets/` (hors Git). |
| Shorts 1 à 3 | contrôlé — **défaut** | Mention « THRILLER DE FICTION » dans la zone masquée par l'interface Shorts ; 24 i/s au lieu de 30. Sous-titres v2 alignés livrés. Ré-export v2 à faire par Codex (aucune nouvelle narration). Voir `exports/shorts/CONTROLE_SHORTS.md`. Non publiés. |
| Chaîne YouTube | **configurée par Codex** | Les Mystères d'Akeb, `UCeY1bZMUcigbZX2VwJmln-Q`, @LesMysteresDAkeb ; imports privés par défaut. Avatar, bannière et playlists à installer. Non relue depuis le cloud. |
| Accès YouTube depuis le cloud | préparé | `outils/youtube_api.py` (OAuth par code d'appareil, import privé idempotent). Il manque l'identifiant OAuth dans l'environnement. |
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
