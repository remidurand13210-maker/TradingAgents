# Direction vocale — Les Mystères d'Akeb

## Voix et modèle

- **Modèle demandé** : `gemini-3.8-flash-tts` (Gemini API, synthèse vocale ; ce n'est pas Gemini Live).
  Avant tout appel : `python3 outils/narration_gemini.py verifier-modele` (requête gratuite, clé requise).
  Si le modèle n'est pas disponible pour le compte, **la production s'arrête** : aucun remplacement silencieux.
- **Voix** : `Algieba`, celle du narrateur déjà validé pour le livre audio et les Shorts.
  Une seule voix de narrateur pour toute la série.
- **Interdits** : aucune voix clonée ou imitée d'une personne réelle (protagonistes de l'affaire, animateurs, journalistes).
  Les citations sont lues comme des citations, sans imitation de la personne citée.

## Intention

Rémi a rejeté une première voix trop rapide et agressive, puis validé une narration plus posée.
Pour la chaîne, il demande **plus de vie** sans perdre cette sobriété :

| Paramètre | Cible |
|---|---|
| Débit | 150–160 mots/min en moyenne, mesuré après génération (`debit_mpm` dans `audio/manifest.json`) |
| Timbre | chaleureux, proche, français naturel |
| Dates, noms propres, chiffres | ralentir nettement |
| Transitions | relancer, avec une légère montée d'énergie |
| Questions | laisser respirer : courte pause après |
| À éviter | ton publicitaire criard, lenteur molle, chuchotement inquiétant, effets dramatiques |

Le débit ne sera **jamais** corrigé en accélérant mécaniquement l'audio. Si un segment est trop lent ou trop rapide,
on ajuste la consigne ou le texte, puis on régénère **ce segment seulement** (`--segment S12`).

## Consignes envoyées au modèle

Les consignes sont séparées du texte à prononcer (voir `config_narration.json` › `consignes` et `marqueur_texte`).
Le mode exact (consigne dans le prompt ou instruction système) dépend de ce que la documentation Google
et l'API acceptent réellement ; il est vérifié sur l'échantillon, qui doit être transcrit pour s'assurer
qu'**aucune consigne n'a été vocalisée**.

## Prononciations à contrôler à l'écoute

| Mot | Attendu | Méthode si écart |
|---|---|---|
| Ligonnès | li-go-NESS (accent sur la fin, s final prononcé) | graphie d'aide dans `prononciations`, appliquée au texte envoyé au modèle seulement ; les sous-titres gardent l'orthographe exacte |
| Roquebrune-sur-Argens | rok-brune-sur-ar-JINSS (prononciation locale usuelle : à confirmer à l'écoute, sans la présenter comme validée par Rémi) | idem |
| Akeb | a-KÈB | idem |
| Dupont de Ligonnès | du-pon-de-li-go-NESS | idem |
| Stabenrath | sta-bène-rat | idem |
| Dates | « le 15 avril 2011 » lu « le quinze avril deux mille onze » | écrire les dates en toutes lettres si le modèle hésite |

Aucune prononciation n'est présentée comme validée par Rémi tant qu'il ne l'a pas écoutée.

## Échantillon de validation

`python3 outils/narration_gemini.py echantillon` génère environ 30 secondes représentatives
(une date, un nom propre, une transition, une question). On compare avec la direction déjà validée :
on ne redemande une validation à Rémi que si le timbre change sensiblement.

## Traitement audio

- WAV maître par segment (24 kHz mono en sortie de l'API, rééchantillonné en 48 kHz au montage).
- Voix propre conservée séparément de la musique (`audio/<épisode>/voix_propre.wav`).
- Musique : nappes originales synthétisées localement (`outils/musique.py`), −24 dB sous la voix, −10 dB hors voix, fondus.
- Master : −16 LUFS intégrés, crête vraie ≤ −1,5 dBTP (limiteur), sans écrêtage ; export AAC 192 kb/s.
