# Plan publicitaire — plafond 100 € (dont 50 € maximum le premier jour)

Ce sont des **plafonds**, pas des objectifs de dépense. Les 50 € du premier jour sont **inclus** dans les 100 €.
Aucune recharge, aucune hausse automatique, aucun abonnement. Au plafond : arrêt. Pour aller au-delà, présenter les résultats à Rémi et lui demander.

## Mise à jour du 01/10/2026 — engagement Meta constaté (transmission de Codex)

| Plateforme | Campagne | Média | Réserve taxes/frais | Fin | Statut observé |
|---|---|---|---|---|---|
| Meta | 120249781441090097 (ensemble 120249781441100097, annonce 120249781441080097) | 40 € au total | 10 € | 04/10/2026 23 h 59 (Paris) | « Traitement en cours » |

Conséquences :
- l'enveloppe du **premier jour (50 €)** est consommée par ce lancement du 01/10 ; **ne pas le dupliquer** ;
- reste **au plus 50 €, taxes et frais compris**, pour tout le reste, YouTube compris, et seulement après inspection de Google Ads (brouillon Search et éventuels anciens brouillons « Test 20 EUR ») ;
- la répartition du tableau « Budgets » ci-dessous est **remplacée** par : YouTube A (in-stream sur emplacements) ≤ 25 €, YouTube B (fil Shorts) ≤ 15 €, réserve 10 € ; Search 0 € ; aucune nouvelle campagne Meta ;
- relever la dépense réellement facturée par Meta au 05/10 avant toute décision : si elle est inférieure à 50 €, le reliquat n'est **pas** réaffecté sans l'accord de Rémi.

## 0. Avant tout lancement (obligatoire)

1. Google Ads : lister **toutes** les campagnes (y compris le brouillon Search), leurs statuts, budgets, dépenses depuis la création, moyens de paiement, crédits promotionnels, alertes.
2. Meta : même inventaire (brouillon « Trafic Akeb », page Akeb), sans rien créer en double.
3. Reporter les montants constatés dans `BUDGET.json › publicite` (dépense et engagements) : **le plafond restant = 100 € − déjà dépensé − déjà engagé**.
4. Captures ou exports dans `preuves/` (sans données de paiement visibles).

Statut au 01/10/2026 : Meta inventorié par Codex (ci-dessus) ; **Google Ads non inspecté**. Ni l'un ni l'autre n'est accessible depuis la session cloud.

## 1. Campagne principale : YouTube, autour des vidéos traitant de l'affaire

Objectif de Rémi : que l'annonce apparaisse **auprès des vidéos consacrées à Xavier Dupont de Ligonnès**.

- **Type de campagne** : celui qui accepte **réellement** le ciblage par emplacements (chaînes et vidéos YouTube précises).
  À vérifier dans l'interface le jour J. Pas de substitution discrète par une audience large, Demand Gen ou un intérêt « faits divers » si les emplacements ne sont pas disponibles : dans ce cas, on s'arrête et on le dit à Rémi.
- **Emplacements** : `publicite/EMPLACEMENTS_YOUTUBE.csv` (URL, titre, chaîne, sujet, date du contrôle). Liste **à constituer** : la recherche a été bloquée dans la session cloud.
- **Deux groupes séparés** (idéalement deux campagnes, pour piloter chaque budget) :
  - **A. In-stream (pré/mid-roll) sur les vidéos de l'affaire** : il faut une **variante horizontale 16:9** du Short, dérivée sans déformation (vertical centré sur fond sombre, texte « THRILLER DE FICTION » et écran final lisibles). Nouveau nom de fichier, les exports d'origine restent intacts.
  - **B. Fil Shorts** : le Short vertical tel quel.
- **Réglages à vérifier et à noter en preuve** : pays France ; langue français ; 18 ans et plus ; **ciblage optimisé et extension d'audience désactivés** ; **partenaires vidéo Google désactivés** ; aucune inférence sur la vulnérabilité des personnes ; exclusion des contenus pour enfants.
  Type d'inventaire : les vidéos de faits divers relèvent souvent de catégories « sensibles ». Si l'inventaire standard exclut les vidéos visées, l'indiquer à Rémi avant de l'élargir.
- **Aucune garantie** d'apparaître sur toutes les vidéos : l'inventaire, les enchères, la monétisation des vidéos cibles et l'éligibilité décident.

## 2. Budgets

| Poste | Jour 1 (plafond) | Total lancement (plafond) |
|---|---|---|
| YouTube A (in-stream sur emplacements) | 20 € | 55 € |
| YouTube B (fil Shorts) | 10 € | 25 € |
| Search (brouillon existant, requêtes exactes et expressions proches) | 0 € par défaut | 10 € seulement si déjà prêt et si le test YouTube tourne |
| Meta (brouillon existant) | 0 € par défaut | 0 € sauf décision de Rémi |
| Marge taxes et frais | 10 € | 10 € |
| **Total facturable** | **≤ 40 €, sous le plafond de 50 €** | **≤ 100 €** |

Mise en œuvre conservatrice :
- **Budget total de campagne** avec **date de fin**, si l'interface le propose pour le type retenu. Sinon, budget quotidien bas et date de fin rapprochée, en tenant compte du fait qu'un budget quotidien moyen **peut être dépassé certains jours** (Google l'annonce jusqu'au double) : un budget quotidien n'est pas un plafond ferme.
- Premier jour : campagnes avec fin le soir du jour 1 (ou budget total égal au plafond du jour). Relevé des dépenses réelles facturées, puis prolongation dans la limite du reste disponible.
- Aucune coupure automatique n'est promise si l'interface ne la fournit pas : on contrôle manuellement la dépense et on met en pause.

## 3. Search (brouillon conservé, non lancé par défaut)

Mots-clés en correspondance exacte ou expression : « xavier dupont de ligonnès », « xavier dupont de ligonnes », « xavier dupont de ligones », « ligonnès », « ligones ».
Annonce : ne nomme pas l'affaire comme argument de vente du roman. Le ciblage contextuel fait le rapprochement ; le texte présente un thriller de fiction.

## 4. Annonces

Les trois Shorts existants (après contrôle de conformité : « THRILLER DE FICTION » au début et à la fin, couverture Akeb exacte, deux formats, pas de vrai nom).
Liens avec UTM `utm_source=google_ads&utm_medium=video&utm_campaign=lma_test_xddl&utm_content=<annonce>_<format>`.

## 5. Mesures

Coût, impressions, vues retenues, clics vers chaque offre (e-book, audio) et achats **réellement attribuables** si le suivi est fiable.
Aucun revenu fictif ; un clic n'est pas une vente. Aucune promesse de rentabilité.
Statut des campagnes consigné tel quel : brouillon, en examen, éligible, **diffusée**. Une campagne publiée ou en examen n'est pas une campagne qui diffuse.

## 6. Arrêt

Plafond atteint : pause immédiate, bilan chiffré à Rémi. Aucune dépense additionnelle pour compenser une absence de ventes.
