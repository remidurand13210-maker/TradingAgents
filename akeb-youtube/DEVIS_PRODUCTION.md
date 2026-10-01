# Devis de production — saison 1 (4 épisodes + bande-annonce)

**Préliminaire, établi le 01/10/2026. Aucune dépense engagée.**
Ce budget est distinct de la publicité (100 €, dont 50 € déjà engagés sur Meta) et du plafond de 5 € du livre et des Shorts (1,434 € réservés).
Le devis définitif sera recalculé sur les scripts **validés**, à partir des mots réellement comptés, et avec les **tarifs officiels lus dans l'environnement Akeb**. Ces tarifs ne sont pas lisibles depuis cette session, car ai.google.dev y est bloqué.

## Base de calcul

- Volume de narration visé : 1 400 à 1 900 mots par épisode × 4, plus environ 170 mots pour la bande-annonce, soit **5 800 à 7 800 mots**, environ **40 à 52 minutes de voix** à 150 mots/min.
- Seule référence réelle disponible : le registre local des trois Shorts, qui compte 0,0249 € réservés pour 158 mots et 68,6 s de voix avec `gemini-3.8-flash-tts`, soit **≈ 0,16 € pour 1 000 mots**. C'est une estimation prudente du registre, pas une facture Google.

## Postes

| Poste | Hypothèse | Estimation | Plafond proposé | Statut |
|---|---|---|---|---|
| **1. Narration Gemini** (`gemini-3.8-flash-tts`, voix Algieba) | 5 800–7 800 mots ; 2 échantillons de 30 s ; environ 30 % de reprises segment par segment | 0,9–1,3 € pour le texte, **1,2–1,7 €** avec échantillons et reprises | **3,00 €** (plafond ferme dans `BUDGET.json`, coût maximal réservé avant chaque appel) | tarif à confirmer |
| **2. Contrôle voix/texte** (transcription Gemini des narrations pour repérer omissions, répétitions et consignes vocalisées) | environ 52 min d'audio en entrée | **≈ 0,10–0,30 €** | **0,50 €** | modèle et tarif à confirmer ; recommandé |
| **3. Images** — visuels originaux (cartes, frises, documents, titres) | animés au montage | **0 €** | — | production locale |
| **3 bis. Images** — photos de lieux sous licence libre (Wikimedia Commons, Pexels, Pixabay) | 20 à 30 photos ; licence vérifiée fichier par fichier | **0 €** | — | registre des visuels obligatoire |
| **3 ter. Images** — illustrations générées (option) | au plus 3 par épisode (12 au total), 3 essais chacune, soit 36 générations | **≈ 1–2 €** selon le modèle | **2,00 €** | option ; modèle et tarif à confirmer |
| **4. Vidéo générée** (option très limitée) | 0 s recommandé pour la version 1 ; au maximum 6 plans de 6 s (36 s), soit environ 54 s générées avec les essais | coût = secondes générées × tarif par seconde du modèle retenu ; **non chiffrable sans le tarif officiel** (ordre de grandeur : une dizaine d'euros pour environ 54 s) | **10,00 €** si l'option est retenue, sinon **0 €** | option ; tarif à confirmer |
| **5. Licences** — musique originale, polices OFL, Natural Earth, photos libres | — | **0 €** | — | conditions documentées |
| **5 bis. Licences** — photos d'agence ou de presse, dont le portrait AFP (option) | usage éditorial sur YouTube | **sur devis de l'agence** ; aucun tarif public vérifié | hors enveloppe ; décision de Rémi | **non recommandé** |
| **6. Calcul** — montage, animation, rendu, contrôles | conteneur cloud Claude ; 20–40 min de calcul par épisode | **0 € supplémentaire** | — | aucun service payant de rendu |
| **7. Abonnements** | aucun | **0 €** | — | interdit sans accord |

## Enveloppes possibles

| Scénario | Contenu | Plafond total |
|---|---|---|
| **A — recommandé** | narration + contrôle + animations au montage + photos libres | **3,50 €** |
| **B** | A + illustrations générées limitées | **5,50 €** |
| **C** | B + quelques secondes de vidéo générée, toujours signalée | **15,50 €** |
| Option hors enveloppe | photos d'agence sous licence | sur devis |

## Garde-fous de dépense

- **Avant chaque appel**, réservation du coût maximal : l'outil s'arrête si le total dépassait l'enveloppe accordée.
- **Cache par empreinte** (texte, modèle, voix, consignes) : on ne régénère jamais un passage déjà produit, et on corrige une phrase en régénérant uniquement son segment.
- **Quota (429)** : arrêt propre et reprise plus tard, sans changer de compte ni de modèle.
- **Validation préalable** : aucune narration sans `VALIDATION.md` (« valide: oui ») dans l'épisode.
- **Registre unique** (`audio/registre_narration.jsonl`), jamais remis à zéro.

## Décision demandée à Rémi (plus tard, en une seule fois)

Elle sera posée quand les scripts seront validés et les tarifs officiels relus. Le choix portera sur un scénario (A, B ou C) et son plafond ferme, inscrit ensuite dans `BUDGET.json › narration.enveloppe_accordee_eur` (et sur une ligne « visuels » pour les options B et C).
