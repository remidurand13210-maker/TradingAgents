# Vérification v1 — épisode 01

Date : 01/10/2026. Règle appliquée : une phrase factuelle n'est dite affirmativement que si elle repose sur au moins une page relue intégralement ; sinon elle est attribuée à son média, ou retirée. Deux passes de relecture par curl le 01/10/2026 : passe 1 (S001, S079, S080, S097, S084, S081), passe 2 (S085, S098, S105, S104, S086, S107, S082, S101). Toute phrase qui ne reposait que sur une source bloquée ou sur une note de dossier Codex a été retirée de la narration ou réduite à ce que confirme une page relue.

## Méthode

`curl -sL` avec un User-Agent de navigateur courant, via le proxy configuré (TLS vérifié, aucun contournement de paywall, aucun contournement de blocage du proxy), puis extraction du texte avec `html.parser` (Python). Seul le texte servi dans la réponse HTML publique a été lu, jusqu'à la fin de l'article. WebFetch (essayé avant) n'a relu aucune page.

## Pages relues (curl, 01/10/2026)

| Source | Page | Résultat |
|---|---|---|
| S001 | 20 Minutes, 02/04/2021, entretien de Frédéric Brenon avec Bruno de Stabenrath | HTTP 200, entretien intégral |
| S079 | Nice-Matin / Var-Matin, 19/04/2022, Eric Marmottans | HTTP 200 ; marqué « réservé aux abonnés » mais texte complet présent dans la page servie (aucun contournement) ; lu jusqu'à la fin |
| S080 | Le Parisien, 22/04/2011, « Des Nantais croyants et discrets » | HTTP 200, `isAccessibleForFree: true`, intégral |
| S081 | Le Parisien, 30/04/2011, « La trajectoire d'un touche-à-tout » | HTTP 200, article libre, intégral |
| S084 | 20 Minutes, 26/04/2011, Frédéric Brenon avec Matthieu Goar | HTTP 200, intégral |
| S097 | Le Parisien, 18/05/2011, « Le rêve américain brisé… » | HTTP 200, article libre, intégral |
| S085 | RTL, publié le 31/07/2025 (Thomas Pierre et Mathieu Isidore), « Xavier Dupont de Ligonnès : qui se cache derrière l'homme le plus recherché de France ? » | passe 2 : HTTP 200, texte intégral (date de publication désormais connue : 31/07/2025) |
| S098 | RTL, 14/10/2020, « Jusqu'à la veille des crimes, c'était quelqu'un de bien », dit son ami | passe 2 : HTTP 200, intégral (article court) |
| S105 | Le Parisien, 15/04/2012, « Dans la tête de Xavier de Ligonnès » | passe 2 : HTTP 200, `isAccessibleForFree: true`, intégral |
| S104 | La Dépêche du Midi, 16/04/2012, « Les carnets intimes… dévoilés » | passe 2 : HTTP 200, `isAccessibleForFree: true`, intégral (reprise du Parisien) |
| S086 | Le Parisien, 22/04/2011, « Agnès et les enfants suivaient Xavier les yeux fermés » | passe 2 : HTTP 200, article libre, intégral |
| S107 | Le Parisien, 27/04/2011, « Xavier de Ligonnès pensait décrocher le jackpot » | passe 2 : HTTP 200, article libre, intégral |
| S082 | Le Parisien, 22/04/2011, « Nantes : les camarades d'Anne et Benoît bouleversés » | passe 2 : HTTP 200, article libre, intégral |
| S101 | Le Parisien, 29/05/2011, « La piste sectaire également explorée » | passe 2 : HTTP 200, article libre, intégral |

## Sources non relues

| Source | Résultat | Conséquence |
|---|---|---|
| S110 INPI (data.inpi.fr) | bloqué par le proxy (CONNECT 403) | date d'immatriculation, SARL, code 7990Z, fermeture au 16/04/2011 : retirés |
| S074 Ouest-France / Maville (angers.maville.com) | bloqué par le proxy (CONNECT 403) | « club de tir » de décembre 2010 : retiré de S32 |
| S088 Society / Marabout (actualitte.com, PDF) | bloqué par le proxy (CONNECT 403) | n'était qu'un appui secondaire ; retiré des sources |
| S016 et S114 Le Journal du Dimanche (lejdd.fr) | bloqué par le proxy | retirés ; S03 et S04 reposent désormais sur RTL et Le Parisien relus ; la reprise des 40 000 € (S19) et l'héritage investi (S23) selon le JDD : retirés |
| S113 registre de Floride (sunbiz.org) | bloqué par le proxy | dates de Netsurf (21/02/2003, 01/10/2004) retirées ; Netsurf n'est plus dit que d'après S097 relu |
| S116 BODACC | bloqué par le proxy | liquidation du 04/01/2012 retirée |
| S089 La Règle du jeu | bloqué par le proxy | « septembre 1976 » et « scolarité commune » retirés |
| S002 Le Monde | HTTP 402 (payant) | non utilisé |

Contradictions et écarts trouvés en passe 2 :
- S085 (RTL) dit « élève médiocre », pas « moyen » : S08 distingue désormais Le Parisien (« moyen ») et RTL (« médiocre »).
- S085 ne présente pas le départ du père comme un récit de proches et nomme le père « Bernard Hubert » : S04 attribue l'âge de dix ans à RTL ; le prénom du père n'est plus dit.
- S081 (relu) situe le divorce des parents « lorsqu'il est en terminale » : divergence désormais dite en S04.
- S082 ne dit pas « temps partiel » (il nomme Agnès « l'adjointe à la vie scolaire ») : S25 reprend S080 (« de temps à autre comme surveillante »).
- S086 ne dit pas « une famille très attachée à lui » mais « Agnès et les enfants le suivaient les yeux fermés » : S28 reprend la formule de la page.
- S098 ne donne que 1977 ; 1976 ne reposait que sur la lettre bloquée (S089).
- S107 : « un réseau d'hôtels et de restaurants » (et non d'hôtels seuls), « le chiffre d'affaires ne décolle pas » : S18 suit la page.
- S097 (relu) nomme Netsurf Concept, fondée à Miami à la fin du voyage de 2002, selon l'ami « Jean-Marc* » : S16 reformulé sur ce seul témoignage.
- S081 (relu) : « Sur des forums Internet, Agnès se plaint que Xavier dilapide l'argent de son héritage » : remplace en S23 l'affirmation du JDD 2026.

## Tableau phrase par phrase (narration finale)

Statut : « confirmé sur page relue » = dit affirmativement, au moins une page relue le dit ; « attribué (page relue) » = la phrase nomme sa source, relue. Aucune ligne ne repose plus sur la seule lecture Codex.

| Segment | Phrase ou extrait | Page(s) relue(s) | Extrait de la page | Statut |
|---|---|---|---|---|
| S01 | maison louée, quatre voitures, enfants dans le privé (2010-2011) | S084 ; S081 | « location d'une maison en centre-ville, quatre voitures, écoles privées » | confirmé sur page relue |
| S01 | revenu déclaré d'environ 4 000 euros par an, selon la presse de 2011 | S084 | « très faibles revenus: 4.000 € par an » | attribué (page relue) |
| S02 | désigné par l'enquête comme principal suspect, jamais jugé | S085 | « le principal suspect » ; « qui reste présumé innocent » | confirmé sur page relue |
| S03 | naît en 1961 à Versailles | S085 ; S080 | « Il naît en 1961 à Versailles » ; « Natif de Versailles » | confirmé sur page relue |
| S03 | mère : Geneviève ; deux sœurs, selon Le Parisien | S085 ; S081 | « Sa mère, Geneviève » ; « près de ses deux sœurs » | confirmé (prénom) / attribué (sœurs) (page relue) |
| S03 | vieille noblesse française (RTL) ; petite noblesse aveyronnaise (Le Parisien) (MODIFIÉ) | S085 ; S081 | « vieille famille de la noblesse française » ; « petite noblesse aveyronnaise » | attribué (page relue) |
| S04 | père quitte le foyer quand Xavier a dix ans (RTL) ; divorce l'année de sa terminale (Le Parisien) (MODIFIÉ) | S085 ; S081 | « déserte le foyer familial lorsque Xavier est âgé de 10 ans » ; « Ses parents divorcent lorsqu'il est en terminale » | attribué (page relue) |
| S04 | sa mère fonde un groupe de prière, Philadelphie | S101 ; S085 | « à l'origine de la création d'un groupe de prière nommé Philadelphie » ; « fondera même un petit groupe religieux : l'Église de Philadelphie » | confirmé sur page relue |
| S04 | fin des années 1960 (Le Parisien) ; messages annonçant l'Apocalypse (Le Parisien, RTL) (MODIFIÉ) | S101 ; S085 | « à la fin des années 1960 » ; « Des messages annonçant notamment la venue prochaine de l'Apocalypse » ; « Selon les prédications de sa mère, "il survivra à l'Apocalypse" » | attribué (page relue) |
| S05 | texte de février 2008 attribué, publié par Le Parisien en 2012 : adolescence dominée par la religion, retour imminent du Christ | S105 ; S104 | « De 11 à 20 ans : toute cette période sera marquée par la FOI et la RELIGION » ; « le Christ va revenir » ; « je crois que c'est imminent » ; « (Février 2008.) » | attribué (page relue) |
| S06 | (mise en garde éditoriale, sans assertion factuelle) (MODIFIÉ) | — | la phrase « Rien, dans les sources que nous avons lues, n'établit de lien de cause… » (note Codex) est retirée | sans objet |
| S07 | amitié avec Bruno de Stabenrath depuis 1977, selon RTL en 2020 (MODIFIÉ) | S098 | « l'histoire d'amitié qu'il a entretenue avec Xavier Dupont de Ligonnès depuis 1977 » | attribué (page relue) |
| S07 | adolescent plein d'humour ; rêvaient des États-Unis, Elvis, Beach Boys | S001 | « Xavier avait beaucoup d'humour » ; « on rêvait des USA, on écoutait Elvis, les Beach boys » | attribué (page relue) |
| S08 | scolarisé au collège-lycée Saint-Exupéry, à Versailles (MODIFIÉ) | S081 | « Scolarisé au collège-lycée Saint-Exupéry » | confirmé sur page relue |
| S08 | élève moyen (Le Parisien), médiocre (RTL) (MODIFIÉ) | S081 ; S085 | « l'ado est un élève moyen » ; « c'est un élève médiocre » | attribué (page relue) |
| S08 | bac avec un an d'avance, selon un écrit de 2006 attribué ; non confirmé | S105 | « passer mon bac avec un an d'avance » ; « (Décembre 2006.) » | attribué (page relue) |
| S08 | passage en école de commerce (les deux médias) | S081 ; S085 | « Après son bac, Xavier s'inscrit dans une école de commerce » ; « Il s'inscrit plus tard dans une école de commerce » | confirmé sur page relue |
| S08 | aucun diplôme supérieur au bac selon Nice-Matin | S079 | « sans autre diplôme que le bac » | attribué (page relue) |
| S09 | à partir de 1981, petits emplois à Aix-en-Provence et dans l'ouest du Var (Toulon, La Seyne) ; obligations militaires brèves en 1984 ; commercial depuis Draguignan ; d'après des récits et Society | S079 | départ vers le Sud-Est en 1981, « petits boulots à Aix-en-Provence mais aussi dans l'ouest-Var » ; « En 1984, Xavier de Ligonnès est brièvement rattrapé par ses obligations militaires » ; « un emploi de commercial » | attribué (page relue) |
| S10 | Agnès née Hodanger | S079 ; S081 | « Agnès Hodanger » | confirmé sur page relue |
| S10 | rencontre à seize ans (ami d'enfance, Le Parisien) ; après le bac (autre article du Parisien) ; amour des années lycée à Versailles (Nice-Matin) (MODIFIÉ) | S086 ; S081 ; S079 | « Xavier et Agnès se sont rencontrés à 16 ans » ; « Après son bac […] il rencontre en soirée Agnès Hodanger » ; « amour des années lycée à Versailles » | attribué (page relue) |
| S10 | fiançailles en 1982 puis rupture, selon Nice-Matin | S079 | « En 1982 […] se fiancent » ; « la promesse de mariage est vite rompue » | attribué (page relue) |
| S11 | long séjour aux États-Unis en 1990, selon un ami (Le Parisien) | S097 | « part une première fois outre-Atlantique en 1990 » ; « pendant dix-huit mois » | attribué (page relue) |
| S11 | Arthur né en 1990, pas le fils biologique de Xavier, élevé avec Agnès | S079 ; S085 | « Arthur, né de père inconnu à Versailles en 1990 » ; Agnès « qui a déjà un petit garçon, Arthur » | confirmé sur page relue |
| S12 | mariage en 1991 ; le 11 septembre à Draguignan selon Nice-Matin | S079 ; S085 | « Ils se marient à Draguignan le 11 septembre 1991 » ; « Les deux se marient en 1991 » | confirmé / attribué (page relue) |
| S12 | Le Parisien place les retrouvailles en 1992 | S081 ; S097 | « En 1992, il fait une halte à Versailles et revoit la belle Agnès » | attribué (page relue) |
| S12 | Thomas 1992, Anne 1994, Benoît 1997 | S079 | naissances citées | confirmé sur page relue |
| S13 | domiciles dans le Var dont Roquebrune-sur-Argens, selon Nice-Matin | S079 | Draguignan, Lorgues, Roquebrune-sur-Argens, Sainte-Maxime | attribué (page relue) |
| S13 | arrivée à Nantes à la fin des années 1990, selon Le Parisien | S080 | « s'était installée à Nantes à la fin des années 1990 » | attribué (page relue) |
| S14 | Sainte-Maxime, juin 1995, miracle annoncé non réalisé (Bruno de Stabenrath, 20 Minutes) | S001 | « incident en juin 1995 : Geneviève avait réuni du monde à Sainte-Maxime » ; « il n'y a pas eu de miracle » | attribué (page relue) |
| S14 | RTL : épisode apocalyptique dans un château en Bretagne | S085 | « en 1995, […] l'homme se retrouve dans un château de Bretagne […] Ils y attendent l'Apocalypse... qui ne vient pas » | attribué (page relue) |
| S15 | voyage familial de neuf mois en 2002, selon un ami ; camping-car à la fin des années 1990 selon un autre reportage du Parisien | S097 ; S081 | « la famille entière part pour les Etats-Unis pendant neuf mois » ; « A la fin des années 1990, ils avaient fait le tour des Etats-Unis en camping-car » | attribué (page relue) |
| S16 | selon l'ami du Parisien, à la fin du séjour de 2002, Xavier reste à Miami et y fonde Netsurf Concept, « exactement la même société » « mais domiciliée aux États-Unis » (MODIFIÉ) | S097 | « Xavier reste quelques semaines supplémentaires à Miami, où il fonde Netsurf Concept. « C'était exactement la même société que la Route des commerciaux, mais domiciliée aux Etats-Unis » » | attribué (page relue) |
| S17 | Route des commerciaux : association créée en 1999 selon Le Parisien ; lancement en 2003 selon RTL et un autre article du Parisien (MODIFIÉ) | S080 ; S097 ; S081 ; S085 | « Créée en 1999 » ; « lancé par Xavier trois ans plus tôt » (que 2002) ; « En 2003, il crée la Route des commerciaux » (S081 et S085) | attribué (page relue) |
| S17 | depuis 2003, gérant et unique employé de la SELREF, installée à Pornic, qui propose à des hôtels et restaurants de figurer dans des guides sur Internet (MODIFIÉ) | S080 | « Depuis 2003, Xavier est gérant et unique employé d'une société, la Selref, installée à Pornic […], qui propose à des restaurants et des établissements hôteliers de figurer dans des guides touristiques sur Internet » | attribué (page relue) |
| S18 | activité réelle : réseau d'hôtels et de restaurants, avantages aux représentants adhérents, modestes cotisations (MODIFIÉ) | S107 | « une activité réelle » ; « un réseau d'hôtels et de restaurants dans lesquels les représentants de commerce auraient droit à des avantages » ; « une modique somme » ; « un faible montant » | attribué (page relue) |
| S18 | payé ; chiffre d'affaires qui ne décolle pas | S107 | « les factures de l'imprimeur sont payées rubis sur l'ongle. Mais le chiffre d'affaires ne décolle pas » | attribué (page relue) |
| S19 | six commerciaux, réclamation Urssaf de 40 000 euros, selon un ami ; non vérifié sur pièce | S097 | « embaucher six commerciaux » ; « L'Urssaf lui a réclamé 40000 € » | attribué (page relue) |
| S20 | résultat net 2008 de 3 200 euros, déficit cumulé de 13 000 euros, plus de bilan publié ensuite, association qui semble ne plus être en activité, selon Le Parisien (MODIFIÉ) | S080 | « aucun bilan financier n'a été publié depuis 2008, année où la société avait enregistré un modique bénéfice net de 3 200 € » ; « accumulé un déficit de 13 000 € » ; « elle semble ne plus être en activité » | attribué (page relue) |
| S21 | revenu déclaré d'environ 4 000 euros par an, selon 20 Minutes notamment | S084 | « 4.000 € par an » | attribué (page relue) |
| S21 | prêt de 50 000 euros consenti par une ancienne relation | S084 ; S081 | dette de « 50.000 € » « auprès d'une maîtresse » ; « il lui emprunte 50000 € » | attribué (page relue) |
| S22 | textes attribués, 2006-2008, récupérés sur une sauvegarde en ligne selon Le Parisien (2012) | S105 ; S104 | « Entre 2006 et 2008, Xavier Dupont de Ligonnès a stocké des centaines de textes […] sur un serveur » ; « grâce à des sauvegardes réalisées par Free » | attribué (page relue) |
| S22 | décembre 2006 : dépenses mensuelles estimées à 7 000 euros | S105 ; S104 | « nous dépensons énormément (avec 7000 €/mois » ; « (Décembre 2006.) » | attribué (page relue) |
| S23 | Le Parisien (2011) : Agnès se plaignait sur des forums que son mari dilapide l'argent de son héritage ; aucun montant (MODIFIÉ) | S081 | « Sur des forums Internet, Agnès se plaint que Xavier dilapide l'argent de son héritage » | attribué (page relue) |
| S24 | titre « Des Nantais croyants et discrets » ; maison louée, quatre voitures, privé | S080 ; S084 | titre exact ; idem S01 | confirmé sur page relue |
| S25 | Agnès surveillante de temps à autre à Blanche-de-Castille, école privée catholique de Nantes (MODIFIÉ) | S080 ; S082 | « travaillait de temps à autre comme surveillante à Blanche-de-Castille, école privée catholique réputée à Nantes » | confirmé sur page relue |
| S25 | ses collègues la décrivent comme « charmante, très conviviale » (MODIFIÉ) | S080 | « Décrite par ses collègues comme « charmante, très conviviale et d'un excellent relationnel » » | attribué (page relue) |
| S25 | propos attribués à Agnès sur un blog, rapportés par 20 Minutes (BFM) : « cassant, trop rigide, peu affectif » | S084 | citation exacte | attribué (page relue) |
| S26 | âges 20, 18, 16, 13 ; Arthur BTS en Vendée, pizzeria, employeur ; Thomas musicologie, université catholique de l'Ouest, Angers ; Anne 1re S, piano ; Benoît batterie | S080 | passages cités | confirmé / attribué (page relue) |
| S26 | Anne et Benoît à la Perverie-Sacré-Cœur ; le directeur évoque de nombreux amis | S082 | « collège-lycée La Perverie-Sacré coeur, où étaient scolarisés Anne et Benoît » ; « Anne et Benoît avaient plein, plein d'amis », raconte le directeur | attribué (page relue) |
| S28 | ami d'enfance (Le Parisien) : Agnès et les enfants le suivaient « les yeux fermés » ; pas de problèmes d'argent (MODIFIÉ) | S086 | « Agnès et les enfants le suivaient les yeux fermés » ; « Ils n'avaient pas de problèmes d'argent » | attribué (page relue) |
| S28 | Bruno de Stabenrath : le temps passé sur les routes de province | S001 | « Xavier passait beaucoup de temps sur les routes de province » | attribué (page relue) |
| S29 | argent : revenus déclarés faibles, prêt privé, dépenses estimées plus hautes | S084 ; S105 | voir S21, S22 | attribué (page relue) |
| S29 | rêve américain abandonné après la réclamation de l'Urssaf, selon un ami (MODIFIÉ) | S097 | « L'Urssaf lui a réclamé 40000 € […] Le rêve d'une vie américaine est repoussé, puis définitivement mis au placard » | attribué (page relue) |
| S29 | activité française sans la croissance espérée | S107 | « le chiffre d'affaires ne décolle pas » | attribué (page relue) |
| S30 | tensions dans le couple, d'après les propos attribués à Agnès rapportés en 2011 | S084 | idem S25 | attribué (page relue) |
| S30 | enfants : études et amitiés, d'après les témoignages publiés | S080 ; S082 | études des quatre enfants ; « plein, plein d'amis » | attribué (page relue) |
| S32 | annonce : Nantes, fin 2010 ; semaines menant au 15 avril 2011 (MODIFIÉ) | S085 | « La dernière trace de Xavier Dupont de Ligonnès remonte au 15 avril 2011 » | confirmé sur page relue |

## Phrases retirées ou modifiées en passe 2 (01/10/2026)

| Segment | Ancienne formulation | Raison | Décision |
|---|---|---|---|
| S03 | « Ses parents s'appellent Geneviève et Hubert ; il a deux sœurs. Le Journal du Dimanche et RTL décrivent une famille de vieille noblesse française. » | JDD (S016) bloqué ; RTL relu nomme le père « Bernard Hubert » ; sœurs dans S081 relu | « Sa mère s'appelle Geneviève ; selon Le Parisien, il grandit auprès de ses deux sœurs. RTL décrit une vieille famille de la noblesse française, Le Parisien une famille de petite noblesse aveyronnaise. » (P010-P012) |
| S04 | « Selon les récits de proches repris par le Journal du Dimanche et par RTL, son père quitte le foyer quand Xavier a une dizaine d'années. Sa mère anime un groupe religieux appelé Philadelphie, que plusieurs enquêtes de presse décrivent comme porteur de prédictions apocalyptiques. » | JDD bloqué ; RTL ne cite pas de proches ; S081 donne une autre date | attribution à RTL (dix ans), divergence Le Parisien (terminale), fondation de Philadelphie et messages apocalyptiques selon S101 et S085 (P013-P014) |
| S06 | « Rien, dans les sources que nous avons lues, n'établit de lien de cause entre cette enfance, cette foi familiale et ce qui se passera en 2011. » | note de dossier Codex | retirée ; remplacée par une mise en garde sans assertion (« et nous ne relirons pas ces années à la lumière de 2011 ») (P017 : surtitre retiré) |
| S07 | « se souvient de leur scolarité commune à Saint-Exupéry » ; « en septembre 1976 selon une lettre publique qu'il a écrite en 2013 » | La Règle du jeu (S089) bloquée ; aucune page relue ne dit la scolarité commune | retirées ; 1977 attribué à RTL (S098) ; humour, USA, Elvis, Beach Boys selon 20 Minutes (S001) (P019-P021) |
| S08 | « RTL et Le Parisien le décrivent comme un élève moyen » | S085 relu : « élève médiocre » | « élève moyen selon Le Parisien, médiocre selon RTL » ; Saint-Exupéry déplacé ici, d'après S081 (P022) |
| S10 | « Ils se rencontrent à Versailles, pendant leur jeunesse ; vers seize ans » | divergence avec S081 et S079 relus | « à seize ans, selon un ami d'enfance » + « après le bac » (autre article du Parisien) + « amour des années lycée, à Versailles » (Nice-Matin) (P028) |
| S16 | registre de Floride : manager, date d'effet 21/02/2003, dissolution administrative 01/10/2004 | Sunbiz (S113) bloqué | retirés ; Netsurf dit d'après S097 relu (Miami, fin du séjour de 2002, témoignage de l'ami) (P043-P045) |
| S17 | « Le 2 avril 2003, une société est immatriculée : SELREF, une SARL avec un établissement à Pornic […]. Son code d'activité la range dans les services de réservation. » | INPI (S110) bloqué | « Depuis 2003, selon Le Parisien, il est le gérant et l'unique employé d'une société installée à Pornic, la SELREF […] » (S080) ; divergence 1999 / 2003 sur la Route des commerciaux dite (P047-P048) |
| S18 | « un réseau d'hôtels pour représentants, financé par des adhésions » ; « progresser » | S107 relu : « hôtels et restaurants », « ne décolle pas » | formulation de la page (P049 : citation exacte ; P050) |
| S19 | « Ce montant, repris par le Journal du Dimanche en 2026, » | JDD (S114) bloqué | incise retirée (P052) |
| S20 | « Le registre officiel garde une trace plus sèche : la fermeture de l'établissement est enregistrée au 16 avril 2011, la liquidation prononcée le 4 janvier 2012. » | INPI (S110) et BODACC (S116) bloqués | remplacée par « Le journal ajoute que l'association la Route des commerciaux semble ne plus être en activité » (S080) (P054 devient un carton texte) |
| S23 | « En 2026, le Journal du Dimanche avance un héritage d'Agnès investi en partie dans le projet américain ; aucune autre source lue ne recoupe ces montants. » | JDD (S114) bloqué ; seconde moitié = note Codex | remplacée par S081 relu : plaintes attribuées à Agnès sur des forums, héritage dilapidé, aucun montant (P059) |
| S25 | « travaille à temps partiel » ; « une collègue a dit au Parisien l'estime qu'on lui portait » | « temps partiel » absent de S082 relu ; S080 cite « ses collègues » | « travaille de temps à autre comme surveillante dans une école privée catholique de Nantes » ; « ses collègues la décrivent au Parisien comme « charmante, très conviviale » » (P064) |
| S28 | « décrit une famille très attachée à lui, et dit n'avoir perçu aucune difficulté financière » | paraphrase ; S086 relu | « dit qu'Agnès et les enfants le suivaient « les yeux fermés », et qu'ils n'avaient pas de problèmes d'argent » (P069) |
| S29 | « la société américaine est dissoute administrativement dès 2004 » | Sunbiz (S113) bloqué | « selon un ami, le rêve américain est abandonné après la réclamation de l'Urssaf » (S097) (P073) |
| S32 | « s'ouvre en décembre 2010, à Nantes, dans un club de tir » | Maville (S074) bloqué | « reprend à Nantes, à la fin de 2010 » (P077) |

Storyboard : sources mises à jour (RTL daté du 31/07/2025 ; JDD, Society/Marabout, La Règle du jeu, INPI, BODACC et registre de Floride retirés des champs `source` et du carton P078). Contrôles passés : en-tête exact, 78 plans numérotés P001-P078, chaque segment S01-S32 a au moins un plan, segments contigus et dans l'ordre de narration.txt, 10 champs par ligne, `params` en JSON valide. script_annote.md : texte de chaque segment identique à narration.txt, sources, notes et décomptes de mots mis à jour, sections DÉTAILS MOINS CONNUS, DIVERGENCES, LACUNES, TRANSITION et RACCORDS mises à jour.

## Phrases retirées ou modifiées en passe 1 (01/10/2026)
| Élément | Raison | Décision |
|---|---|---|
| « Sa date de fondation varie selon les articles » (Philadelphie, S04) | second appui S102 seulement lu_partiel | retiré de la narration ; signalé en DIVERGENCES |
| « Cette date varie selon les articles » (arrivée à Nantes, S13) | version « vers 2002 » portée par Le Monde S002, lu_partiel | remplacé par « Nous ne fixons pas d'année plus précise » |
| « Le Monde et 20 Minutes ont rapporté » (messages d'Agnès, S25) | Le Monde S002 lu_partiel | remplacé par « la presse, dont 20 Minutes » (S084 lu_integral) |
| Liste des villes du profil d'Agnès (Draguignan, Lorgues, Sainte-Maxime, Vaison-la-Romaine, Pornic, Nantes) | Le Monde S083 seul, lu_partiel | non utilisée |
| Salaire d'Agnès (300 €/mois), loyer (1 400 ou 1 600 €) | Le Monde lu_partiel, divergence non résoluble | non utilisés |
| Jour et mois de naissance | Pappers et Nonfiction lu_partiel, aucun acte lu | non utilisés (année seule) |
| Études de droit à Assas | Nonfiction seule, lu_partiel, non confirmée | non utilisée |
| Montants JDD 2026 (350 000 € d'héritage, 300 000 € investis) | source unique, non recoupée | non prononcés ; seule l'existence de l'affirmation est dite, attribuée |
| Carte Crystal | témoignage unique, sans pièce | non utilisé |
| Profession du père | divergente (aéronautique / physique nucléaire) | omise |
| S09 : « de brèves obligations militaires en 1984, puis de petits emplois à Aix-en-Provence, à Toulon et à La Seyne-sur-Mer, avant un travail commercial dans le Var » | S079 relu : les petits boulots commencent vers 1981, avant 1984 ; Toulon est un lieu de vie cité dans une lettre, pas un emploi nommé | remplacé par « à partir de 1981, de petits emplois à Aix-en-Provence et dans l'ouest du Var, autour de Toulon et de La Seyne-sur-Mer ; de brèves obligations militaires en 1984 ; puis un travail commercial, depuis Draguignan » (storyboard P025-P026 réordonnés) |
| S25 : « la presse, dont 20 Minutes, a rapporté des messages qui lui sont attribués, de 2002 et de 2004, évoquant des difficultés d'argent et de couple » | contredit par S084 relu (ni dates ni argent) ; dates portées par Le Monde S002 seul, inaccessible (402) | remplacé par l'attribution exacte : « 20 Minutes, reprenant BFM, a rapporté des propos qui lui sont attribués sur un blog : elle reprochait à son mari d'être « cassant, trop rigide, peu affectif » » (storyboard P065) |
| S28 : « ses longues absences » (Bruno de Stabenrath) | paraphrase ; S001 relu dit « Xavier passait beaucoup de temps sur les routes de province » | remplacé par « le temps qu'il passait sur les routes de province » (storyboard P069) |
| S30 : « traverse des difficultés dès le début des années 2000 » | date issue des messages 2002-2004, non trouvée sur page relue | remplacé par « si l'on s'en tient aux propos attribués à Agnès et rapportés en 2011, connaît des tensions » (storyboard P074) |
| S26 : « université catholique d'Angers » | S080 relu : « université catholique de l'Ouest à Angers » | corrigé (storyboard P066) |

## Bilan

- Lignes factuelles du tableau final : **57** (S06, S27 et S31 sans assertion factuelle ; S31 = fiction).
- Appuyées sur au moins une page relue intégralement par curl le 01/10/2026 : **57 / 57**.
- Reposant sur la seule lecture Codex : **0**. Reposant sur une source bloquée ou une note de dossier : **0**.
- Pages relues : 14 (6 en passe 1, 8 en passe 2). Sources tentées mais bloquées par le proxy : INPI (S110), Maville (S074), actualitte (S088), plus JDD, Sunbiz, BODACC, La Règle du jeu déjà bloqués ; Le Monde (S002) payant (402).
- Phrases modifiées : 5 en passe 1 (S09, S25, S26, S28, S30, dont 1 contredite) ; 16 segments modifiés en passe 2 (S03, S04, S06, S07, S08, S10, S16, S17, S18, S19, S20, S23, S25, S28, S29, S32).
- Narration : **1735 mots** (décompte par espaces, segments seulement), dans la fourchette 1 400-1 900.

## Ce qui reste (hors validation)

Aucune phrase de la narration ne dépend plus d'une page non relue. Restent des lacunes de dossier, qui ne sont pas dites à l'antenne : actes d'état civil, comptes annuels de SELREF, pièce Urssaf, contrat du prêt, registre de Floride, attestation INPI, annonces BODACC (voir LACUNES du script annoté).
