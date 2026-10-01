# contre_verif — second regard indépendant

Ce dossier reçoit les contre-vérifications des thèmes sensibles de la série Dupont de Ligonnès.

## Convention de nommage

```
<THEME>_deepseek.json
```

Thèmes : `avril_2011_avant`, `avril_2011_apres`, `pistes_2020_2026`, `hypotheses_sort`.

Ces fichiers **ne sont pas fusionnés automatiquement** dans le dossier principal : ils servent au vérificateur, qui les confronte aux sources primaires.

## Règle de traçabilité

Le nom de fichier suppose un second regard produit par DeepSeek avec recherche web. Ce n'est pas une garantie : **lire le champ `outil` du JSON avant de s'en servir.** Les quatre fichiers présents ici portent un `outil` différent de « deepseek » et un bloc `note_meta` explicatif. Ils restent exploitables comme contre-vérification, mais ne doivent pas être présentés comme une vérification DeepSeek.

Une seconde règle compte au moins autant : le champ `acces` de chaque source. `extrait_moteur` signifie que la page n'a **pas** été ouverte, seulement aperçue via un moteur de recherche ; `inaccessible` signifie qu'elle n'a pas pu être consultée du tout. Plusieurs affirmations reposent sur des sources en `extrait_moteur` — elles sont signalées dans `notes` et auraient besoin d'être confirmées.

## État au 1er octobre 2026

| Thème | Fichier | Outil | Sources | Statut |
|---|---|---|---|---|
| `pistes_2020_2026` | `pistes_2020_2026_deepseek.json` | bionic-agent | 24 | produit — **pas** DeepSeek |
| `avril_2011_avant` | `avril_2011_avant_deepseek.json` | bionic-agent | 10 | produit — **pas** DeepSeek |
| `avril_2011_apres` | `avril_2011_apres_deepseek.json` | bionic-agent | 14 | produit — **pas** DeepSeek |
| `hypotheses_sort` | `hypotheses_sort_deepseek.json` | bionic-agent | 14 | produit — **pas** DeepSeek |

Le prompt à donner à DeepSeek, avec les quatre blocs de consignes, est dans `../prompts/prompt_deepseek_contre_verif.md`. **Il n'a été exécuté par aucun outil à ce jour** : les quatre fichiers ci-dessus sont un second regard produit autrement, pas le livrable initialement prévu.

## Tentative d'envoi à Claude — 1er octobre 2026

Le thème `pistes_2020_2026` a été envoyé à Claude via `routeur-ia.mjs` (modèle `fable`). Le prompt envoyé est archivé dans `../prompts/envois/pistes_2020_2026_prompt.md`, la réponse brute dans `../prompts/envois/reponses/`.

**Résultat : inexploitable.** Le routeur est un appel de conversation simple, sans outil de recherche web. Claude a donc respecté la règle absolue du prompt et renvoyé un squelette vide (`sources`, `assertions`, `chronologie`, `contradictions` à zéro) avec des `lacunes` décrivant tout ce qu'il n'a pas pu vérifier. Aucune information n'a été produite de mémoire — c'est le comportement correct, mais ce n'est pas un livrable.

Conséquence : **passer par `routeur-ia.mjs` ne peut pas produire un second regard documentaire**, quel que soit le modèle choisi. Il faut soit un modèle avec recherche web activée dans son interface, soit fournir le corpus au modèle.

Fichiers `_claude.json` : aucun n'a été déposé dans ce dossier, précisément pour ne pas laisser croire à une vérification qui n'existe pas.

## État de la réponse à ces limites

1. ~~Envoi à Claude via `routeur-ia.mjs`~~ — fait le 1er octobre 2026, sans résultat exploitable.
2. **Envoi à Claude dans une interface avec recherche web activée** — recommandé, non exécuté.
3. **Fourniture du corpus au modèle** (recherche faite ici, tri et structuration par Claude) — recommandé, non exécuté ; attention, Claude n'est alors plus un chercheur indépendant.

## Points sensibles, par thème

### `pistes_2020_2026`

Trois pistes **sans conclusion publique** au 1er octobre 2026, à écrire comme telles à l'antenne :

1. le compte « Epsilon » — existence et caractéristiques documentées, attribution au suspect **non établie** ;
2. la saisine de l'Arcom après la séquence du 2 juin 2026 — annoncée, **aucune décision publiée** à cette date ;
3. l'appel à informations du comté de Brewster (Texas) — **aucune observation confirmée**, parquet de Nantes non informé.

Juillet-septembre 2026 n'a livré aucune évolution d'enquête : seulement des reprises médiatiques (France 2 le 5 juillet, Le Nouvel Obs le 29 juillet). Constat négatif, à ne pas présenter comme une preuve d'absence.

### `avril_2011_avant`

Deux divergences à ne pas lisser :

- **la date du décès du père** — janvier (Le Télégramme, Wikipédia : 20 janvier 2011) contre février (Le Parisien du 27 avril 2011) ;
- **la date du dîner avec Thomas** — 4 avril (flash du Figaro, chronologie du Télégramme de 2013) contre 5 avril (reconstitutions récentes). C'est la divergence explicitement signalée par le prompt.

S'y ajoute un point plus important encore : **la date du décès d'Agnès n'est pas certaine**. Le parquet a dit qu'elle ne pouvait être fixée « au jour près » et des témoins de voisinage disent l'avoir vue les 5 et 7 avril. La « nuit du 3 au 4 avril » est une reconstruction, jamais un fait.

### `avril_2011_apres`

- Ne pas écrire « il est parti le 12 avril » : trois sources situent le départ au 10 avril, avec une nuit à Puilboreau.
- Ce qu'il emportait en quittant l'hôtel le 15 avril est **divergent** (housse de costume / sac à dos) — et rien n'établit qu'il portait l'arme.
- Le Monde du 21 juin 2011 (point de départ 9 du prompt) n'a **pas pu être ouvert** : tout ce qui lui est attribué passe par une reprise.
- Arrêt strict au 15 avril, 16 h 10.

### `hypotheses_sort`

Deux anciens policiers du même dossier portent des convictions **opposées** : Jean-Paul Le Tensorer (suicide) et Gilles Galloux (fuite aux États-Unis). C'est un point éditorial fort, à présenter en le nommant.

Ne pas réduire le débat à « suicide ou Amérique » : Anne-Sophie Martin défend une troisième position — disparition orchestrée sans fuite américaine.

Ne jamais écrire « la justice a conclu au suicide » : la formule officielle constante est que l'enquête n'a pas déterminé s'il était mort ou en fuite.

Aucune probabilité chiffrée n'est proposée, conformément à la consigne.

## Ce qui reste à faire

- Faire passer le prompt à DeepSeek pour obtenir les quatre vrais fichiers `_deepseek.json`, puis confronter les deux jeux.
- Rouvrir les sources marquées `inaccessible` : Le Monde du 21 juin 2011, le flash du Figaro du 28 avril 2011, La Montagne et Le Point.
- Vérifier les affirmations qui reposent sur une seule source en `extrait_moteur`.
