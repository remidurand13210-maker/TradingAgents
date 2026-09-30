# Prompt DeepSeek — contre-vérification indépendante

> DeepSeek (avec la recherche web activée) sert de **second regard indépendant** sur les thèmes les plus sensibles, pas de source principale.
> Une conversation par thème. Remplace `<THEME>` et `<CONSIGNE DU THÈME>` par l’un des blocs ci-dessous.
> Enregistre la réponse JSON (ou demande à Antigravity de le faire) dans `akeb-youtube/recherche/contre_verif/<THEME>_deepseek.json`.
> Ces fichiers ne sont PAS fusionnés automatiquement : ils servent au vérificateur, qui les confronte au dossier principal.

---

Active la recherche web. Tu es documentaliste pour une série documentaire YouTube francophone sur l’affaire Xavier Dupont de Ligonnès. Date de consultation : 2026-10-01.

RÈGLE ABSOLUE : n’utilise que des pages que tu as réellement ouvertes pendant cette conversation. Recopie chaque URL exactement, sans en inventer ni en reconstruire. Si tu n’as pas pu ouvrir une page, mets "acces": "inaccessible" ou "extrait_moteur". Si tu n’as pas trouvé une information, écris-la dans "lacunes" au lieu de la déduire. Aucune information de mémoire.

Thème : <THEME>
Consigne : <CONSIGNE DU THÈME>

Autres règles : priorité aux communications officielles puis aux médias de référence ; une dépêche AFP reprise par plusieurs médias compte pour UNE source ("origine": "AFP") ; catégories FAIT_DOCUMENTE / TEMOIGNAGE_RAPPORTE / RECONSTRUCTION_ENQUETE / HYPOTHESE avec l’attribution (qui l’affirme) ; divergences de dates ou de faits dans "contradictions" ; pas de détail graphique sur les victimes ; ne nomme pas les particuliers innocents (personnes arrêtées par erreur, sosies, signalants) ; citations littérales de 20 mots au plus.

Réponds UNIQUEMENT par un JSON valide, sans texte autour, au format :
{"sujet":"<THEME>","outil":"deepseek","sources":[{"ref":"S-<THEME>-D01","titre":"","url":"","auteur_organisme":"","media":"","date_publication":"","date_faits":"","date_consultation":"2026-10-01","acces":"lu_integral|lu_partiel|inaccessible|extrait_moteur","type":"officiel|agence|media_national|media_regional|media_etranger|temoignage_direct|livre|documentaire|autre","origine":"propre|AFP|reprise:<media>","notes":""}],"assertions":[{"ref":"A-<THEME>-D01","assertion":"","categorie":"FAIT_DOCUMENTE|TEMOIGNAGE_RAPPORTE|RECONSTRUCTION_ENQUETE|HYPOTHESE","attribution":"","date_faits":"","lieu":"","sources":["S-<THEME>-D01"],"nb_sources_independantes":1,"incertitude":"faible|moyenne|forte","centrale":true,"notes":""}],"chronologie":[{"date":"","precision":"jour|mois|annee|approx","evenement":"","categorie":"","sources":[],"note":""}],"contradictions":[{"sujet":"","versions":[{"version":"","sources":[]}],"traitement_recommande":""}],"lacunes":[""]}

---

## Thèmes recommandés pour DeepSeek (les plus sensibles)

### `avril_2011_avant`

Période de décembre 2010 à la nuit des faits : pratique du tir (date de début rapportée, club, fréquence — noter que le début est rapporté dès décembre 2010, avant la mort du père), décès du père (date exacte), héritage d’une carabine (.22 LR ?) et chronologie, achats rapportés (silencieux, munitions, sacs, ciment, chaux, outils : dates et sources, sans détails opératoires), récit de l’armurier sur un prétendu prêtre, dernières activités de la famille, absences scolaires et messages aux établissements (ce que savaient les interlocuteurs à ce moment-là), Thomas à Angers et son retour à Nantes, date(s) du ou des repas avec Thomas (divergences), dates retenues par l’enquête pour les meurtres (formulées comme reconstruction), éléments ultérieurement établis. AUCUN détail graphique ni opératoire superflu.

Points de départ :
- [départ 5] AFP / 20 Minutes, 23 avril 2011, président du club de tir — https://www.20minutes.fr/societe/712447-20110423-societe-tuerie-nantes-pere-entrainait-regulierement-tir-avant-drame (début de pratique rapporté dès décembre 2010, avant la mort du père)
- [départ 6] Le Parisien, 27 avril 2011, récit de l’armurier (prétendu prêtre tireur d’élite) — https://www.leparisien.fr/faits-divers/nantes-quand-le-pere-pretendait-etre-un-pretre-tireur-d-elite-27-04-2011-1424471.php
- [départ 7] 20 Minutes, 22 avril 2011, écoles et absences — https://www.20minutes.fr/societe/712093-20110422-societe-dupont-ligonnes-rien-excessif-foi
- [départ 12] Le Parisien, 3 avril 2026, les grandes dates de l’affaire — https://www.leparisien.fr/faits-divers/la-nuit-du-meurtre-la-decouverte-des-corps-la-derniere-image-du-fugitif-les-grandes-dates-de-laffaire-dupont-de-ligonnes-03-04-2026-J27GNQSCXJGMNKNKA2O2LVG7KY.php (confronter aux chronologies anciennes, divergences sur les dates de repas avec Thomas)

### `avril_2011_apres`

Du 5-6 avril 2011 à la dernière trace authentifiée : courriers et messages envoyés (dates, destinataires : famille, écoles, employeurs, amis), récits de départ différents selon les destinataires (Australie, protection de témoins américaine / agent de la DEA, autres), déplacements en voiture et hôtels (Blagnac, Le Pontet ou autres, Roquebrune-sur-Argens : dates, sources), retrait de 30 euros (contexte, autres opérations bancaires), trace de connexion IP (remonter à Sud Ouest), dernière image connue (caméra, date, lieu), départ de l’hôtel le 15 avril (ce qui est établi, ce qu’il emportait selon les sources), véhicule retrouvé (date, lieu), origine du portrait public (AFP making-of). Arrêter au dernier point vérifié, sans scène imaginée.

Points de départ :
- [départ 8] Europe 1 / AFP, 5 mai 2011, courriers et destinataires — https://www.europe1.fr/faits-divers/Ligonnes-Inutile-de-s-occuper-des-gravats-562812 (versions Australie et protection américaine)
- [départ 9] Le Monde, 21 juin 2011, traces de voyage et retrait de 30 euros — https://www.lemonde.fr/societe/article/2011/06/21/tuerie-de-nantes-sur-les-traces-de-xavier-dupont-de-ligonnes_1526839_3224.html
- [départ 10] Numerama, 21 juin 2011, reprenant Sud Ouest, trace de connexion IP — https://www.numerama.com/politique/19130-xavier-dupont-de-ligonnes-repere-grace-a-son-adresse-ip.html (remonter à Sud Ouest si possible)
- [départ 11] AFP Making-of, « Une porte nue fermée sur son mystère » — https://making-of.afp.com/une-porte-nue-fermee-sur-son-mystere (403 lors du repérage ; trouver un accès légitime ; origine de l’image publique)
- [départ 12] Le Parisien, 3 avril 2026, les grandes dates de l’affaire — https://www.leparisien.fr/faits-divers/la-nuit-du-meurtre-la-decouverte-des-corps-la-derniere-image-du-fugitif-les-grandes-dates-de-laffaire-dupont-de-ligonnes-03-04-2026-J27GNQSCXJGMNKNKA2O2LVG7KY.php (confronter aux chronologies anciennes, divergences sur les dates de repas avec Thomas)

### `pistes_2020_2026`

Pistes publiques de 2020 à 2026-10-01 : signalement du Doubs écarté en 2024 (ADN), appel à informations du shérif de Brewster County (Texas) en mars 2026 et sa clarification, émission de M6 et faux prêtre (date exacte de diffusion, nom de l’émission, présentateur, contenu de la « confession » alléguée et année alléguée, déclaration et excuses de M6, démenti de l’évêque de Carcassonne, aveu de mensonge rapporté, saisine de l’Arcom, plainte ou procédure judiciaire : distinguer chacune), compte « Epsilon » (ce qu’est ce compte, pourquoi rapproché, vérifications annoncées par le parquet, et CONCLUSIONS ULTÉRIEURES éventuelles), et TOUTE évolution de juillet à septembre 2026 (cherche explicitement « Dupont de Ligonnès septembre 2026 », « août 2026 », « juillet 2026 », « Epsilon conclusions », « faux prêtre plainte »). Pour chaque piste : information initiale, auteur, contrôle, résultat public ou inconnu. Ne nomme pas les particuliers innocents.

Points de départ :
- [départ 14] Le Progrès, 15 avril 2024, Doubs : tests ADN négatifs — https://www.leprogres.fr/faits-divers-justice/2024/04/15/tests-adn-le-signalement-ne-correspond-pas-a-xavier-dupont-de-ligonnes
- [départ 15] KOSA / First Alert 7 (Katie Carlock, Tamlyn Price), 25 mars 2026 mis à jour le 26 — https://www.firstalert7.com/2026/03/25/brewster-county-sheriff-needs-help-finding-man/ (clarification du shérif : aucun nouvel élément, aucune observation confirmée)
- [départ 16] Europe 1 / AFP, 3 juin 2026, M6 piégée par un faux prêtre, excuses — https://www.europe1.fr/medias-tele/affaire-dupont-de-ligonnes-m6-piegee-par-le-faux-temoignage-dun-pretendu-pretre-presente-ses-excuses-941471
- [départ 17] Europe 1, 3 juin 2026, entretien avec l’évêque de Carcassonne — https://www.europe1.fr/societe/il-suffisait-de-mappeler-leveque-de-carcassonne-revient-sur-le-faux-temoignage-dun-pretre-concernant-laffaire-dupont-de-ligonnes-941450
- [départ 18] Le Dauphiné Libéré, 4 juin 2026, compte Epsilon, vérifications annoncées par le parquet — https://www.ledauphine.com/faits-divers-justice/2026/06/04/affaire-xavier-dupont-de-ligonnes-le-parquet-annonce-des-verifications-du-compte-epsilon

### `hypotheses_sort`

Le débat public sur le sort de XDDL : déclarations d’enquêteurs, magistrats ou anciens policiers (vivant ou mort ? attribuer), positions de journalistes spécialistes et d’auteurs de livres (attribuer, noter si le livre est lu ou seulement résumé), proches (ex. Bruno de Stabenrath convaincu d’une survie), famille d’Agnès. Arguments publiquement avancés pour : (a) décès après la disparition (terrain du massif, arme, ressources financières, état psychologique rapporté, lettres), (b) fuite durable à l’étranger (préparatifs, récits, papiers, argent, compétences), (c) vie discrète plus proche. Éléments factuels utiles : qu’emportait-il ? arme et munitions retrouvées ou non ? passeport ? ressources ? recherches effectuées et leurs limites (superficie, grottes, mines) ? Quelles observations changeraient l’analyse (restes identifiés, ADN, empreintes) ? Aucune probabilité chiffrée inventée.

Points de départ :
- [départ 1] Interview de Bruno de Stabenrath, 20 Minutes, 2 avril 2021 — https://www.20minutes.fr/justice/3012459-20210402-affaire-xavier-dupont-ligonnes-prepare-tout-ca-mourir-convaincu-bruno-stabenrath-ami-fugitif (séparer souvenirs et conviction personnelle sur une survie)
