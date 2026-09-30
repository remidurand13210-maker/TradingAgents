# Métadonnées YouTube — règles communes

Les métadonnées propres à chaque vidéo sont dans `episodes/<épisode>/metadonnees.md` (générées avec les scripts).
Les chapitres sont insérés **après mesure de l'export** (`episodes/<épisode>/chapitres_mesures.txt`), jamais estimés.

## Liens traçables (UTM)

| Vidéo | E-book (EPUB + PDF, 2,99 €) | Livre audio (MP3 + M4B, 4,99 €) |
|---|---|---|
| Bande-annonce | `https://payhip.com/b/INPGL?utm_source=youtube&utm_medium=video&utm_campaign=lma_xddl&utm_content=ep00_ebook` | `https://payhip.com/b/0HWpa?utm_source=youtube&utm_medium=video&utm_campaign=lma_xddl&utm_content=ep00_audio` |
| Épisode 1 | `…INPGL?…&utm_content=ep01_ebook` | `…0HWpa?…&utm_content=ep01_audio` |
| Épisode 2 | `…&utm_content=ep02_ebook` | `…&utm_content=ep02_audio` |
| Épisode 3 | `…&utm_content=ep03_ebook` | `…&utm_content=ep03_audio` |
| Épisode 4 | `…&utm_content=ep04_ebook` | `…&utm_content=ep04_audio` |
| Short 1 | `…&utm_campaign=lma_shorts&utm_content=short01_ebook` | `…&utm_campaign=lma_shorts&utm_content=short01_audio` |
| Short 2 | `…&utm_content=short02_ebook` | `…&utm_content=short02_audio` |
| Short 3 | `…&utm_content=short03_ebook` | `…&utm_content=short03_audio` |
| Publicité | `utm_source=google_ads&utm_medium=video&utm_campaign=lma_test_xddl&utm_content=<annonce>_ebook` | idem `_audio` |

À vérifier avant publication : que Payhip conserve les paramètres jusqu'à la page produit et que ses statistiques les restituent.
Sinon, les clics resteront mesurables côté YouTube et Google Ads, mais **aucune vente ne sera attribuée à une vidéo** sans suivi fiable.

## Modèle de description (épisode)

```
[Résumé honnête en 2-3 phrases.]

⚠️ Chaîne indépendante liée à l'auteur Akeb. Ni police, ni enquête officielle, ni émission ; aucune autorisation ni caution des familles. Faits sourcés, témoignages attribués, hypothèses signalées.

Chapitres :
[insérés après mesure de l'export]

Sources principales :
– [Média, « Titre », date — URL]
…

Le roman (fiction, personnages inventés) — La dernière correction, d'Akeb :
📖 E-book (EPUB + PDF) : [lien UTM]
🎧 Livre audio (MP3 + M4B) : [lien UTM]

Crédits : narration par voix de synthèse (Gemini, voix Algieba) ; musique originale générée pour la chaîne ; cartes schématiques sur fond Natural Earth (domaine public) ; visuels originaux.
Une erreur factuelle ? Signalez-la en commentaire : les corrections sont épinglées.
```

## Déclarations YouTube (à confirmer au moment de l'envoi)

- **Public** : « Non, ce contenu n'est pas conçu pour les enfants ».
- **Contenu modifié ou synthétique** : la narration est une voix de synthèse d'un narrateur fictif. Aucune personne réelle n'est imitée, aucun événement réel n'est fabriqué, aucune image réaliste n'est générée.
  La case sera cochée ou non **selon le texte de la règle YouTube en vigueur**, lu le jour de l'envoi (non lisible depuis la session cloud).
  Dans tous les cas, la voix de synthèse est mentionnée dans les crédits.
- **Promotion payante** : sans objet (pas de partenariat tiers). Le lien commercial avec Akeb est dit dans la description.

## Interdits de métadonnées

Pas de mots-clés trompeurs ni de bourrage, pas de formulations « affaire résolue », « vérité cachée », « on l'a retrouvé », « vraies confessions », pas de visage réel en miniature, pas de nom d'une victime en titre.
