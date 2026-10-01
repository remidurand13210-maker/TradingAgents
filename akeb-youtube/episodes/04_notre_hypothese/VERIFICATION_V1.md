# Vérification v1 — Épisode 04 (01/10/2026)

Méthode : chaque phrase factuelle de `narration.txt` v1 est rattachée à une page lue. « relu 01/10/2026 » = page rouverte par moi ce jour (texte extrait par curl via le proxy, ou WebFetch) ; « lu_integral (Codex) » = lecture intégrale Codex du 01/10/2026, sans contradiction trouvée. Les phrases d'opinion de la chaîne (raisonnement, hypothèse) ne sont pas des phrases factuelles ; leurs éléments factuels sont vérifiés.

**Accès réellement obtenus le 01/10/2026**
- WebFetch : franceinfo.fr OK ; ici.fr OK ; refusés par l'outil : letelegramme.fr, leparisien.fr, ladepeche.fr, lepoint.fr, rtl.fr, 20minutes.fr, nicematin.com, infos.rtl.lu ; lejdd.fr bloqué par le proxy.
- curl (proxy) : OK pour letelegramme.fr, leparisien.fr, ladepeche.fr, rtl.fr, 20minutes.fr, ledauphine.com, leprogres.fr, firstalert7.com ; lepoint.fr 403 ; lemonde.fr 402 (abonnement) ; lejdd.fr, edito.nicematin.com, infos.rtl.lu : échec de connexion.
- Pages complètes en libre accès : Le Télégramme 15/04/2013, La Dépêche 06/03/2026, 22/03/2024, 10/05/2011, RTL 13/04/2022, 02/06/2026, 20/02/2026, 20 Minutes 02/04/2021, 01/04/2021, 03/04/2018, Le Parisien 02/06/2026, 03/06/2026, 11/04/2026, 25/11/2012, 23/06/2011, 22/04/2011, 12/10/2019, 02/03/2026 (direct, réponses visibles), Le Dauphiné 04/06/2026, First Alert 7 25/03/2026. Accès partiel (abonnement) : Le Parisien 19/02/2026 (chapô et début). Le Progrès 15/04/2024 : citations du procureur visibles derrière le mur d'inscription.

| Seg. | Phrase ou extrait | Source(s) : id, média, date, URL | Accès obtenu | Statut |
|---|---|---|---|---|
| S01 | « vers seize heures… revient à son hôtel… gare sa voiture… repart à pied » | S070, 20 Minutes, 03/04/2018 (màj 23/10/2019), https://www.20minutes.fr/societe/2198403-20180109-video-affaire-dupont-ligonnes-15-dates-cles-comprendre-tuerie-nantes | relu 01/10/2026 (curl) | confirmé |
| S01 | « dernière trace officielle » | S216, Le Télégramme, 15/04/2013, https://www.letelegramme.fr/loire-atlantique/nantes-44000/spanxavier-dupont-de-ligonnesspan-toujours-introuvable-deux-ans-apres-1816680.php | relu 01/10/2026 (curl) | confirmé |
| S02 | soupçonné d'avoir tué sa femme et leurs quatre enfants ; âges 20, 18, 16, 13 ans | S133, La Dépêche du Midi, 06/03/2026, https://www.ladepeche.fr/2026/03/06/xavier-dupont-de-ligonnes-15-ans-apres-le-meurtre-de-sa-famille-et-sa-disparition-la-justice-penche-pour-le-suicide-ou-en-est-lenquete-13247807.php ; S080, Le Parisien, 22/04/2011 (« ARTHUR, 20 ans »), https://www.leparisien.fr/archives/des-nantais-croyants-et-discrets-22-04-2011-1418225.php ; S131, La Dépêche, 22/03/2024 (« suspecté d'avoir tué ») | relu 01/10/2026 (curl) | confirmé |
| S02 | mandat d'arrêt international depuis le 10 mai 2011 | S121, La Dépêche, 10/05/2011, https://www.ladepeche.fr/article/2011/05/10/1078502-mandat-d-arret-international-contre-xavier-de-ligonnes.html ; S122, Le Monde, 11/05/2011 ; S154 RTL 20/02/2026 (« Depuis le 10 mai 2011… mandat d'arrêt international ») | relu 01/10/2026 (S121, S154) ; S122 lu_integral (Codex), 402 pour moi | confirmé |
| S02 | jamais jugé | S216, S133 (aucun procès ; « toujours à l'instruction », S131) | relu 01/10/2026 | confirmé |
| S03 | courriers attribués ; un établissement scolaire et l'employeur d'Agnès : départ pour l'Australie | S052, Europe 1, 05/05/2011, https://www.europe1.fr/faits-divers/Ligonnes-Inutile-de-s-occuper-des-gravats-562812 ; S061, DNA, 23/04/2011, https://www.dna.fr/actualite/2011/04/23/quintuple-meurtre-de-nantes-recherches-vaines-scenario-machiavelique ; S135, Le Parisien, 02/03/2026 (écoles et employeur prévenus) | lu_integral (Codex) ; S135 relu 01/10/2026 | confirmé (Australie : Codex lu_integral) |
| S03 | aux proches, une lettre parle d'une protection américaine et demande de faire croire à l'Australie | S052, S061 (A047) ; S135 relu : « courriers à ses proches, annonçant un départ pour les États-Unis » | lu_integral (Codex) + relu partiel du contenu | confirmé, formulé « selon les récits publiés en 2011 » |
| S04 | juin 2011, spéléologues, cavités autour du rocher, cercle de 12 à 15 km | S126, Le Parisien, 23/06/2011, https://www.leparisien.fr/loire-atlantique-44/affaire-ligonnes-nouvelles-fouilles-prevues-mardi-dans-le-var-23-06-2011-1505320.php | relu 01/10/2026 | confirmé |
| S04 | nouvelles fouilles 2012 (grottes) et 2013 (massif des Maures), sans résultat | S129, Le Parisien, 25/11/2012, https://www.leparisien.fr/archives/dupont-de-ligonnes-de-nouvelles-fouilles-lancees-25-11-2012-2352209.php ; S130, La Dépêche, 02/05/2013 ; S216 Le Télégramme 2013 (zone du massif des Maures) ; S135 (jamais retrouvé) | relu 01/10/2026 (S129, S216, S135) ; S130 lu_integral (Codex) | confirmé |
| S04 | Ronsin, 2021, AFP : « chaque centimètre carré de terrain n'a pas pu être étudié » | S133, La Dépêche, 06/03/2026 | relu 01/10/2026 | confirmé (citation via AFP, attribuée) |
| S05 | plus de 700 signalements, mars 2013, parquet cité par Le Télégramme | S216 | relu 01/10/2026 | confirmé |
| S05 | plus de 1 750, mars 2024, communiqué du procureur, La Dépêche du Midi | S131, La Dépêche, 22/03/2024, https://www.ladepeche.fr/2024/03/22/xavier-dupont-de-ligonnes-rien-ne-permet-de-donner-judiciairement-du-credit-a-la-version-de-sa-soeur-estime-le-procureur-de-nantes-11842198.php ; S234 franceinfo 26/03/2026 (« En 2024… plus de 1 750 ») | relu 01/10/2026 (curl ; WebFetch) | confirmé |
| S05 | plus de 1 850, juin 2026, Le Parisien | S193, Le Parisien, 02/06/2026, https://www.leparisien.fr/faits-divers/affaire-xavier-dupont-de-ligonnes-epsilon-le-mysterieux-utilisateur-dun-forum-religieux-reste-actif-jusquen-2017-02-06-2026-V5FU5WV24ZB2PGQIVBA4BMCKUQ.php ; S194 Le Dauphiné 04/06/2026 (« 1 850 signalements ») | relu 01/10/2026 | confirmé |
| S05 | Antoine Leroy : vérifiés « jusqu'ici sans succès » | S193 ; S194 ; S242, ICI, 03/06/2026, https://www.ici.fr/pays-de-la-loire/loire-atlantique-44/nantes/affaire-dupont-de-ligonnes-le-parquet-de-nantes-verifie-depuis-15-ans-toutes-les-informations-jusqu-ici-sans-succes-7788298 | relu 01/10/2026 (curl ; WebFetch pour ICI) | confirmé |
| S06 | octobre 2019, homme interpellé en Écosse présenté à tort comme lui ; le lendemain, ADN l'exclut | S171, Le Parisien, 12/10/2019, https://www.leparisien.fr/faits-divers/l-homme-arrete-a-glasgow-n-est-pas-xavier-dupont-de-ligonnes-12-10-2019-8171568.php ; S070 (rectificatif 20 Minutes) | relu 01/10/2026 | confirmé |
| S06 | avril 2024, Doubs, ADN ne correspond pas | S185, Le Progrès, 15/04/2024, https://www.leprogres.fr/faits-divers-justice/2024/04/15/tests-adn-le-signalement-ne-correspond-pas-a-xavier-dupont-de-ligonnes | relu 01/10/2026 (citations visibles) | confirmé |
| S06 | mars 2026, franceinfo : « pas permis de déterminer s'il était mort ou en fuite » | S234, franceinfo, 26/03/2026, https://www.franceinfo.fr/faits-divers/xavier-dupont-de-ligonnes/affaire-dupont-de-ligonnes-un-appel-a-temoins-lance-au-texas-le-parquet-de-nantes-regrette-de-ne-pas-en-avoir-ete-informe_7895918.html | relu 01/10/2026 (WebFetch, phrase recopiée) | confirmé (attribué à franceinfo) |
| S07 | Yves Gambert : « la piste du suicide ou la piste de la fuite en France ou à l'étranger » | S216 | relu 01/10/2026 | confirmé |
| S08 | longtemps la thèse privilégiée par les enquêteurs, selon RTL | S152, RTL, 02/06/2026, https://www.rtl.fr/actu/justice-faits-divers/pourquoi-organiser-ca-pour-se-suicider-15-ans-apres-l-affaire-xavier-dupont-de-ligonnes-la-journaliste-anne-sophie-martin-prone-une-disparition-orchestree-7900641709 | relu 01/10/2026 | confirmé (attribué) |
| S08 | septembre 2011, Ronsin : suicide « l'hypothèse la plus probable », fuite étudiée | S147, Le Point (Reuters), 03/09/2011, https://www.lepoint.fr/societe/le-suicide-de-dupont-de-ligonnes-hypothese-la-plus-probable-03-09-2011-1369530_23.php ; S119, 20 Minutes, 01/04/2021, https://www.20minutes.fr/justice/3011519-20210401-affaire-xavier-dupont-ligonnes-page-blanche-laquelle-chacun-projette-fantasmes-estime-ancien-procureur-nantes | S147 lu_integral (Codex), 403 pour moi ; S119 relu 01/10/2026 (« la plus probable », « il y a bientôt dix ans ») | confirmé |
| S08 | mars 2013, Brigitte Lamy, qui lui avait succédé : « conviction… on en sera sûr le jour où on découvrira son corps » | S216 (Lamy) ; S133 (« ayant succédé à Xavier Ronsin », « mars 2013 auprès de l'AFP ») | relu 01/10/2026 | confirmé |
| S09 | avril 2022, RTL, Le Tensorer, ex-patron de la PJ de Rennes : « l'hypothèse la plus probable, c'est qu'il est mort » ; peut-être jamais la solution | S149, RTL, 13/04/2022, https://www.rtl.fr/actu/justice-faits-divers/xavier-dupont-de-ligonnes-pour-moi-l-hypothese-la-plus-probable-est-qu-il-est-mort-affirme-un-policier-7900144510 | relu 01/10/2026 | confirmé |
| S10 | aucune trace authentifiée depuis le 15 avril 2011 | S216 (« on ne l'a jamais revu ») ; S135 (« n'a jamais été retrouvée ») ; S193 | relu 01/10/2026 | confirmé |
| S10 | 2012 : vérifications aéroports, gares, préfectures (faux papiers) sans succès ; aucune réserve cachée | S129 | relu 01/10/2026 | confirmé (attribué à Le Parisien) |
| S11 | aucun corps, aucun reste identifié | S135 ; S216 (Lamy lie la certitude au corps) | relu 01/10/2026 | confirmé |
| S11 | titre RTL juin 2026 : « Pourquoi organiser ça pour se suicider ? » | S152 (balise titre) | relu 01/10/2026 | confirmé |
| S12 | Stabenrath, ami depuis l'adolescence ; 2021, 20 Minutes : « polyglotte qui sait modifier son apparence », « Il n'a pas préparé tout ça pour mourir » ; plutôt l'Australie | S001, 20 Minutes, 02/04/2021, https://www.20minutes.fr/justice/3012459-20210402-affaire-xavier-dupont-ligonnes-prepare-tout-ca-mourir-convaincu-bruno-stabenrath-ami-fugitif | relu 01/10/2026 | confirmé |
| S13 | Galloux, office anti-cybercriminalité en 2011, retraité, livre février 2026 en faveur de la survie | S153, Le Parisien, 19/02/2026, https://www.leparisien.fr/faits-divers/je-crois-quil-ne-sest-pas-suicide-quil-est-vivant-laffaire-dupont-de-ligonnes-vue-par-un-ancien-enqueteur-19-02-2026-MYI6LDDWUFE4ZGM67KO5CLFOFI.php ; S154 RTL 20/02/2026 | relu 01/10/2026 (S153 partiel : chapô et début ; S154 complet) | confirmé |
| S13 | RTL : « connaît déjà sa destination finale » ; cherche une trace aux États-Unis | S154, RTL, 20/02/2026, https://www.rtl.fr/actu/justice-faits-divers/xavier-dupont-de-ligonnes-est-il-toujours-vivant-le-cyber-policier-qui-le-traque-depuis-2011-espere-encore-trouver-une-de-ses-traces-aux-etats-unis-7900603818 | relu 01/10/2026 | confirmé |
| S14 | fin mars 2026, shérif du comté de Brewster : appel, possiblement vu en 2020 | S234 franceinfo 26/03/2026 ; S156 Le Parisien 11/04/2026 | relu 01/10/2026 | confirmé |
| S14 | le lendemain : aucune observation confirmée, aucun élément nouveau ; sollicité par une équipe privée de journalistes avec un ancien enquêteur | S051, First Alert 7 (KOSA), 25/03/2026 màj 26/03/2026, https://www.firstalert7.com/2026/03/25/brewster-county-sheriff-needs-help-finding-man/ | relu 01/10/2026 (curl) | confirmé |
| S14 | procureur de Nantes non informé | S234 (WebFetch, citation d'Antoine Leroy) ; S156 | relu 01/10/2026 | confirmé |
| S15 | sœur, livre 2024, exfiltration de toute la famille aux États-Unis ; procureur : rien ne permet de « donner judiciairement du crédit » | S131 | relu 01/10/2026 | confirmé |
| S16 | selon RTL, dossier : ADN et une empreinte digitale | S149 | relu 01/10/2026 | confirmé |
| S16 | Martin : « Il est connu là-bas. » | S152 | relu 01/10/2026 | confirmé |
| S17 | Martin : « orchestrée, organisée, anticipée » ; a refait sa vie ; ne dit pas où | S152 | relu 01/10/2026 | confirmé |
| S18 | 1er juin 2026, Ouest-France, compte Epsilon créé le 2 juillet 2010, actif jusqu'en 2017 ; style rapproché ; expert : « la piste est sérieuse » | S193 (« publiée ce lundi », 1er juin 2026 = lundi) | relu 01/10/2026 ; Ouest-France non ouvert | confirmé (attribué à Ouest-France via Le Parisien) |
| S18 | parquet : vérifications annoncées | S194, Le Dauphiné Libéré, 04/06/2026, https://www.ledauphine.com/faits-divers-justice/2026/06/04/affaire-xavier-dupont-de-ligonnes-le-parquet-annonce-des-verifications-du-compte-epsilon ; S193 | relu 01/10/2026 | confirmé |
| S19 | compte créé avant la disparition ; rien ne permet d'affirmer formellement qu'il lui appartenait | S193 | relu 01/10/2026 | confirmé |
| S19 | au 1er octobre 2026, aucun résultat public trouvé | Codex A208 (bilans 17/08 et 02/09/2026, lu_partiel) ; recherche web du 01/10/2026 (aucun résultat après juin) | constat de recherche | attribué (« je n'ai trouvé ») |
| S19 | faux prêtre, juin 2026 sur M6, prétendait avoir recueilli sa confession ; M6 : faux témoignage | S187, Le Parisien, 03/06/2026, https://www.leparisien.fr/culture-loisirs/tv/affaire-xavier-dupont-de-ligonnes-5-minutes-pour-comprendre-comment-m6-sest-fait-berner-par-un-faux-pretre-03-06-2026-RUBI65PY4BG55L2LIWKI352KH4.php ; S242 ICI | relu 01/10/2026 | confirmé |
| S20 | photos diffusées par Interpol ; centaines de signalements vérifiés | S149 ; S131, S193 | relu 01/10/2026 | confirmé |
| S21 | phrase éditoriale définitive | décision de Rémi (RACCORDS_V0.md, point 3) | — | hypothèse de la chaîne (non factuelle) |
| S22 | mandat, photos, ADN et empreinte, plus de 1 850 signalements ; terrain non fouillé entièrement | S121, S149, S193, S133 | relu 01/10/2026 | confirmé |
| S23 | vérifications rapportées dès 2012 n'en ont établi aucune ; deux procureurs et un ancien chef de PJ penchent pour un décès | S129 ; S147/S119, S216, S149 | relu 01/10/2026 (S147 Codex) | confirmé |
| S24 | Stabenrath, Martin, Galloux lisent la préparation comme un projet de survie | S001, S152, S154 | relu 01/10/2026 | confirmé |
| S24 | 2012 : bijoux de valeur d'Agnès disparus, de quoi financer un temps une cavale | S129 | relu 01/10/2026 | confirmé (attribué) |
| S24 | 2026 : selon Le Parisien, certains enquêteurs voient dans la piste du suicide une fausse piste | S135, Le Parisien, 02/03/2026, https://www.leparisien.fr/faits-divers/direct-dupont-de-ligonnes-nouvelles-revelations-15-ans-apres-sa-disparition-pistes-des-enqueteurs-posez-nous-vos-questions-sur-cette-affaire-02-03-2026-ZEW4WMYKNZGPHIOV4GZLYKW3VE.php | relu 01/10/2026 | confirmé (attribué) |
| S25 | critères de révision (ADN, empreinte, messages Epsilon attribués) | S149, S193 | relu 01/10/2026 | confirmé (raisonnement) |
| S26 | promotion du roman | — | — | fiction nommée |
| S28 | noms des victimes | S133, S194 | relu 01/10/2026 | confirmé |

## Retiré ou remplacé depuis la v0

- « 16 h 10 » et « caméra qui filme le départ à pied » : remplacés par « vers seize heures » (20 Minutes) et « dernière trace officielle » (Le Télégramme).
- Housse de costume / sac à dos : retiré de la narration (divergence signalée dans script_annote).
- Le Tensorer « 2019 » via notice encyclopédique : remplacé par RTL, 13/04/2022.
- Galloux, « faux papiers obtenus dans le Var » et « dernière image mise en scène » : retirés (pages lues muettes). Photos de 1990 au Texas, 48 États : retirés (extraits de moteur, tiers).
- « Plus de 900 signalements en 2020 » : retiré, aucune page lue.
- Formule « mort ou en fuite » attribuée au parquet : attribuée désormais à franceinfo (mars 2026), qui l'écrit.
- Frère d'Agnès (« faire son deuil ») : retiré (Le Parisien relu ne porte qu'un appel conditionnel ; inutile à l'épisode).
- Abbayes explorées (La Provence, extrait) : retiré.
- Procureur « non nommé » de septembre 2011 : Xavier Ronsin, d'après Le Point/Reuters (Codex) et 20 Minutes 2021 (relu).

## Bilan

- Lignes de contrôle (phrases ou extraits factuels, plus 2 lignes non factuelles) : **51**.
- Phrases factuelles : **49**. Confirmées sur page lue : **48** — toutes relues le 01/10/2026, dont 6 complétées par une lecture intégrale Codex sans contradiction (S02 Le Monde 11/05/2011 ; S03 Europe 1 et DNA, ×2 ; S04 La Dépêche 02/05/2013 ; S08 Le Point/Reuters ; S23 renvoi au Point). Parmi elles, les positions et chiffres sont dits avec leur attribution (« selon… », média et date).
- Attribuée comme constat de recherche : **1** (S19, aucun résultat public sur Epsilon au 01/10/2026).
- Non factuelles : **2** (S21 hypothèse de la chaîne ; S26 fiction).
- Retirés depuis la v0 : **9** éléments (liste ci-dessus).
- Manque : lecture directe d'Ouest-France (Epsilon), du Point (403), du Monde (402), de Nice-Matin, du JDD et de RTL Infos (inaccessibles) ; livres non lus. Aucune phrase de la narration ne dépend d'eux seuls.
- Conclusion : toutes les phrases factuelles reposent sur une page lue ; conditions de `VALIDATION.md` remplies.
