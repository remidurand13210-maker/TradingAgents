# Demande d'enveloppe — saison 1 (01/10/2026)

**Une seule demande. Rien n'est dépensé tant que Rémi n'a pas répondu.**

## Base de calcul

- Tarifs officiels lus le 01/10/2026 sur https://ai.google.dev/gemini-api/docs/pricing (palier payant Standard) :
  - `gemini-3.8-flash-tts` : 0,50 $ par million de tokens de texte en entrée et 9,00 $ par million de tokens d'audio en sortie, à raison de 25 tokens par seconde d'audio. **Ces prix doublent le 01/01/2027** ; la production doit se faire avant cette date.
  - Conversion : 0,93 € pour 1 $.
- Volumes v1 comptés par `outils/narration_gemini.py estimer` :

| Vidéo | Segments | Mots | Durée estimée | Coût maximal réservé |
|---|---|---|---|---|
| 00 Bande-annonce | 7 | 190 | 1,3 min | 0,031 € |
| 01 Avant 2011 | 32 | 1 711 | 11,3 min | 0,273 € |
| 02 Avril 2011 | 37 | 1 786 | 11,9 min | 0,285 € |
| 03 Après la disparition | 29 | 1 544 | 10,3 min | 0,246 € |
| 04 Mort ou en fuite ? | 28 | 1 712 | 11,3 min | 0,273 € |
| **Total** | **133** | **6 943** | **≈ 46 min** | **1,11 €** |

Le « coût maximal » prend le débit de parole le plus lent et une marge ; le coût réel sera plus bas.

## Postes

| Poste | Calcul | Estimation | Plafond |
|---|---|---|---|
| 1. Narration (voix Algieba) | 1,11 € maximum pour le texte, plus un échantillon de prononciation (noms difficiles) et environ 30 % de reprises segment par segment | ≈ 1,5 € | **3,00 €** |
| 2. Contrôle voix/texte (transcription par `gemini-2.5-flash`, 1,00 $ par million de tokens audio en entrée) | ≈ 46 min × 60 × 25 tokens ≈ 69 000 tokens, plus la sortie texte | ≈ 0,10 € | **0,50 €** |
| 3. Visuels animés, cartes, frises, tableaux, photos de lieux sous licence libre | rendu local HyperFrames | 0 € | — |
| 4. Illustrations générées (option B) | 12 images × 3 essais × 0,067 $ (Gemini 3.1 Flash Image, 1K) | ≈ 2,25 € | **2,50 €** |
| 5. Vidéo générée (option C, toujours signalée à l'écran) | 54 s générées × 0,12 $/s (Veo 3.1 Fast, 1080p) | ≈ 6,0 € | **7,00 €** |
| 6. Licences, calcul, abonnements | — | 0 € | — |

## Scénarios

| Scénario | Contenu | Plafond ferme |
|---|---|---|
| **A — recommandé** | narration + contrôle + animations + photos libres | **3,50 €** |
| B | A + illustrations générées limitées | 6,00 € |
| C | B + quelques secondes de vidéo générée | 13,00 € |

Garde-fous : coût maximal réservé avant chaque appel, arrêt automatique au plafond, cache (jamais de double paiement), registre unique, aucune narration sans `VALIDATION.md`.
Ce budget est distinct de la publicité et du plafond de 5 € du livre et des Shorts.

## Question à Rémi

**Réponse de Rémi (01/10/2026) : oui, scénario A, 3,50 €.**
