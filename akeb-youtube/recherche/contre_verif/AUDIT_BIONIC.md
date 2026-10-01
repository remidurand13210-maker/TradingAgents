# Audit des quatre fichiers « Bionic » — 01/10/2026

**Provenance** : agent Bionic sous LM Studio, sur le PC de Rémi. Ce n'est **pas** DeepSeek, malgré le nom des fichiers. Ils ont été copiés par Codex le 01/10/2026 (`bionic/PROVENANCE-CODEX.txt`), qui a seulement contrôlé leur validité JSON et l'absence de secrets, sans revérifier les faits.
**Audit réalisé ici** : lecture intégrale des 61 assertions, des 62 entrées de sources, des contradictions et des lacunes ; contrôle de cohérence interne, avec le brief et avec le fichier préliminaire `bio_jeunesse.json`.
**Non fait** : réouverture des sources. La session cloud n'a pas accès à la presse ; aucune URL n'a donc pu être confirmée.

## Vue d'ensemble

| Fichier | Sources | lu_partiel | extrait_moteur | inaccessible | Assertions |
|---|---|---|---|---|---|
| avril_2011_avant | 10 | 6 | 3 | 1 | 12 |
| avril_2011_apres | 14 | 6 | 7 | 1 | 17 |
| pistes_2020_2026 | 24 | 11 | 13 | 0 | 21 |
| hypotheses_sort | 14 | 7 | 5 | 2 | 11 |

Après fusion : 51 sources distinctes (plusieurs entrées renvoient au même article, par exemple Le Télégramme du 15/04/2013 ou Nice-Matin du 07/12/2020).
Aucune source n'est marquée « lu_integral » : tout ce qui est « lu » l'est partiellement.

## Points forts

- **Les divergences sont signalées, non lissées** : date de la mort du père (janvier ou février 2011), date du dîner avec Thomas (4 ou 5 avril), datation de la mort d'Agnès (« date probable », témoignages de voisinage contraires), objet emporté le 15 avril (housse ou sac), date de découverte de la voiture (21 avril ou nuit du 21 au 22).
- **Positions attribuées et nommées** : procureurs successifs, anciens policiers aux convictions opposées (Le Tensorer : suicide ; Galloux : fuite aux États-Unis), troisième voie d'Anne-Sophie Martin, amis et famille.
- **Formule officielle répétée** : l'enquête n'a pas permis de déterminer s'il est mort ou en fuite. Aucune probabilité chiffrée.
- **Constat négatif prudent** pour juillet à septembre 2026 : aucune avancée publique identifiée, ce qui n'est pas une preuve d'absence.

## Points à confirmer avant toute narration (source unique, extrait seul ou reprise)

| Élément | Fragilité |
|---|---|
| Courriel du 14/04/2011 à 20 h 32 (« nettoyage final ») | une seule source (Nice-Matin), qui reprend Society (2020), non consulté |
| Nuit du 13 au 14 avril à La Seyne-sur-Mer | une seule source, étape la moins documentée |
| Faux nom « Xavier Laurent » et montant au Pontet | issus de Wikipédia (extrait), Nice-Matin en appui partiel |
| Témoins voyant Agnès les 5 et 7 avril | extrait de Wikipédia seulement ; à retrouver (RTL 2011, Envoyé spécial 2013) |
| Restaurant du dîner avec Thomas (Avrillé) | extrait encyclopédique ; Le Figaro inaccessible |
| Décès de la mère de XDDL en mars 2026 | seul le titre d'un article a été vu |
| Position de Jean-Paul Le Tensorer (2019) | attribution via une notice encyclopédique |
| Thèse de Gilles Galloux, faux papiers dans le Var | comptes rendus de presse ; livre non lu |
| Le Monde du 21/06/2011 (retrait de 30 €, compte fermé, « petite somme ») | article non ouvert ; passe par la reprise de Numerama |
| Nom du frère d'Agnès | graphie variable selon les médias |
| Modèle exact de la carabine et chargeur | divergent, et sans utilité pour la narration (détail opératoire à exclure) |

## Ce qui manque toujours pour la saison

- **Épisode 1** : famille d'Agnès et des enfants, parcours professionnel, situation financière, carnets (thèmes `bio_famille` et `bio_travail_finances`), plus une lecture réelle de la jeunesse (le fichier `bio_jeunesse` ne contient que des extraits).
- **Épisode 3** : découverte des corps et premières recherches (thème `decouverte_enquete`) ; pistes de 2011 à 2019, dont la **fausse arrestation de Glasgow en 2019** (thème `pistes_2011_2019`).
- **Plateformes, droits, emplacements publicitaires** : thèmes `plateformes`, `commerce_droits`, `emplacements_youtube`.

## Usage décidé

1. Les fichiers sont versés dans `recherche/contre_verif/bionic/` et fusionnés dans les CSV avec la provenance `bionic_lmstudio_non_reverifie`.
2. Ils peuvent nourrir des **brouillons v0**, signalés comme tels. Chaque phrase factuelle y porte son identifiant de source et son niveau d'accès. Un fait à source unique ou connu par simple extrait n'est dit qu'avec son attribution (« selon … »), ou n'est pas dit.
3. **Aucune narration** n'est produite sur un brouillon v0. L'outil de narration refuse tout épisode sans fichier `VALIDATION.md` attestant la vérification des sources sur pages lues.
