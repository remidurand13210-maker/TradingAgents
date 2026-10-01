# Plan visuel — saison 1 « Les Mystères d'Akeb »

Rémi a précisé que les quatre épisodes doivent être de **vraies vidéos à la mise en scène animée**, pas une piste audio illustrée de cartons fixes.
Le principe d'économie est le suivant : **presque tout s'anime au montage**, localement et sans coût. Les éléments générés sont réservés aux rares moments où ils apportent quelque chose, et chacun est clairement signalé.

## 1. Grammaire des plans

| Type de plan | Rôle | Animation au montage (locale, 0 €) | Durée type |
|---|---|---|---|
| **Carte** | trajets, lieux, distances | fond Natural Earth ; le tracé se dessine progressivement d'étape en étape ; chaque point s'allume avec sa date ; léger zoom vers la zone active | 8–14 s |
| **Frise commune** | situer l'épisode dans les quinze ans | le curseur avance jusqu'au moment raconté ; les jalons apparaissent dans l'ordre ; passage de la frise large à la frise zoomée (avril 2011) | 6–10 s |
| **Document de synthèse** | comparer, résumer (récits de départ, pistes et vérifications, scénarios) | tableau original de la chaîne, signé « réalisé par la chaîne » ; les lignes se révèlent au rythme de la voix ; surlignage ambre de la ligne commentée | 10–18 s |
| **Citation** | parole attribuée | texte bref (≤ 20 mots), révélé en deux temps, puis l'auteur et la source datée ; étiquette « témoignage rapporté » | 5–8 s |
| **Date / lieu** | repères | apparition en fondu-montée, chiffres de la date en léger décalé | 3–5 s |
| **Question / chapitre** | articulations | fondu sur fond sombre ; filet ambre qui se trace | 3–6 s |
| **Photo de lieu** | ancrage dans le réel | mouvement de caméra sobre (zoom ou panoramique de 3 à 6 % sur toute la durée), aucune secousse ; crédit et licence à l'écran | 5–9 s |
| **Illustration générée** (option) | atmosphère quand aucune image libre n'existe | même mouvement sobre ; bandeau permanent « ILLUSTRATION GÉNÉRÉE » | 4–6 s |
| **Vidéo générée** (option, très limitée) | respiration visuelle | bandeau permanent « RECONSTITUTION ILLUSTRATIVE — IMAGES GÉNÉRÉES » | 4–8 s |
| **Promotion du roman** | invitation finale | couverture exacte qui glisse, « THRILLER DE FICTION » permanent, deux formats à égalité | 15–25 s |

Constantes à l'écran :
- l'étiquette de statut (fait documenté, témoignage rapporté, reconstitution de l'enquête, hypothèse, fiction) reste visible tant que la voix parle de ce statut ;
- le bandeau bas indique la date de la source et la date des faits ;
- le filigrane de la chaîne est discret.

**Rythme** : un changement visuel toutes les 4 à 8 secondes, sous la forme d'un nouveau plan ou d'une étape animée du même plan, sans dépasser 12 secondes sur un même état. Les moments graves (victimes) respirent davantage : fond sobre, pas de mouvement superflu, musique plus basse.

**Sous-titres** : SRT natifs YouTube calés sur la voix réelle (`outils/srt_aligne.py`), deux lignes au maximum. Le titrage incrusté est réservé aux noms, dates et chiffres-clés.

## 2. Droits des images

| Catégorie | Usage | Conditions |
|---|---|---|
| Visuels originaux (cartons, cartes, frises, tableaux) | **base de la série** | créés par la chaîne : 0 € |
| Fond de carte Natural Earth | cartes | domaine public, mention à l'écran |
| Photos de lieux sous licence libre (Wikimedia Commons : domaine public, CC BY, CC BY-SA) | Versailles, Nantes, Angers, Roquebrune-sur-Argens et son rocher, paysages du comté de Brewster | licence vérifiée **fichier par fichier** ; auteur, licence et lien en crédit à l'écran et en description ; CC BY-SA : recadrage et mouvement dans le respect de la licence ; **jamais** la maison de la famille ni des personnes identifiables |
| Photos de presse et d'agence (AFP, Reuters, Sipa, journaux) | **exclues par défaut** | **une source journalistique n'autorise pas la réutilisation de ses photos** ; une licence éditoriale payante est nécessaire, sur devis de l'agence (option, voir devis) |
| Portrait de XDDL (photo AFP du 23/04/2011) et avis de recherche | **exclus par défaut** | droits de l'agence ou de l'auteur, et respect des personnes ; possible seulement avec une licence acquise et un usage sobre |
| Photos des victimes et de la famille | **jamais** | dignité des victimes, droit à l'image |
| Extraits télévisés (M6, reportages) | **jamais** | droits des diffuseurs ; description en texte avec la source datée |
| Illustrations et vidéos générées | option limitée | aucune personne réelle, aucune scène de crime, aucun lieu présenté comme fidèle ; bandeau permanent ; conditions d'utilisation du service à respecter |
| Banques d'images gratuites (Pexels, Pixabay) | option | licence propre à chaque fichier ; pas de personne identifiable reliée à l'affaire ; crédit facultatif mais conservé |

Chaque visuel non original reçoit une ligne dans `montage/REGISTRE_VISUELS.csv` (fichier, source, auteur, licence, URL, date de vérification, usage, plan) **avant** d'entrer dans un montage.

## 3. Reconstitutions

- Aucune reconstitution des crimes, aucune scène avec les victimes, aucune image du fugitif fabriquée.
- Une reconstitution illustrative, sans personnage identifiable, n'est admise que pour aider à comprendre un lieu ou une atmosphère, par exemple une route de nuit ou un massif boisé. Le bandeau « RECONSTITUTION ILLUSTRATIVE — IMAGES GÉNÉRÉES » reste affiché pendant toute sa durée.
- La voix ne dit jamais « voici » sur une image générée.

## 4. Découpage image/voix

Le découpage vit dans `episodes/<épisode>/storyboard.csv` : chaque plan est rattaché à un segment de voix. Une animation est appliquée **par défaut selon le type de plan** (tableau ci-dessus). Elle se règle au besoin dans `params` :
- `"anim"` : `"trace"`, `"revele"`, `"curseur"`, `"kenburns"`, `"fixe"` ;
- `"visuel"` : chemin du fichier, pour les photos et vidéos ;
- `"credit"`, `"licence"` ;
- `"bandeau"` : `"ILLUSTRATION GÉNÉRÉE"` ou `"RECONSTITUTION ILLUSTRATIVE — IMAGES GÉNÉRÉES"`.

Les brouillons v0 des épisodes 2 à 4 utilisent les types existants. Leurs animations par défaut et un passage de densification (photos de lieux, étapes animées) sont à ajouter lors de la révision, une fois les sources revérifiées.

## 5. Moteur d'animation

Il est à compléter dans `outils/montage.py`, rendu local à 30 i/s, sans coût :
- images calculées en Python (transformations subpixel, sans tremblement du texte), puis envoyées à ffmpeg ;
- plans fixes conservés pour les respirations ;
- temps de calcul estimé : 20 à 40 min par épisode sur ce conteneur à 4 cœurs.
