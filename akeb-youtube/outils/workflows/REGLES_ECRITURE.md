# Règles d'écriture — Les Mystères d'Akeb (saison 1)

Extrait de `outils/workflows/ecriture_episodes.js` : ce sont les mêmes règles pour tout rédacteur, humain ou agent.

## Mode BROUILLON v0 (en vigueur tant que le dossier n'est pas revérifié sur pages lues)

- Le dossier actuel mélange des sources partiellement lues (`lu_partiel`), des extraits de moteur (`extrait_moteur`) et des sources inaccessibles. Lire `recherche/contre_verif/AUDIT_BIONIC.md` avant d'écrire.
- Un fait ne se dit **affirmativement** que s'il repose sur au moins une source `lu_partiel` ET n'est pas signalé comme fragile dans l'audit ; sinon il se dit **avec son attribution** (« selon Nice-Matin… », « d'après une chronologie publiée par Le Télégramme en 2013… ») ou il ne se dit pas.
- Les éléments listés comme fragiles dans l'audit ne servent pas d'accroche et ne portent jamais une conclusion.
- Chaque segment de `script_annote.md` indique : identifiants des sources (S### de `recherche/SOURCES.csv`) avec leur niveau d'accès, identifiants d'assertions (A### de `recherche/ASSERTIONS.csv`), provenance (bionic / extraits), et une ligne « À REVÉRIFIER : … » listant ce qu'il faut confirmer sur page lue.
- En tête de `script_annote.md` : « STATUT : BROUILLON v0 — non narrable ». En tête de `narration.txt` : la ligne de commentaire `# BROUILLON v0 — NE PAS NARRER AVANT VALIDATION`.
- Ne jamais créer `VALIDATION.md` : c'est la vérification sur pages lues qui le créera.
- Lacunes du dossier (fait nécessaire absent) : pas de texte inventé ; dans `narration.txt`, une ligne de commentaire `# LACUNE : …` à l'endroit voulu ; dans `script_annote.md`, une section « LACUNES ».

RÈGLES ÉDITORIALES (non négociables) — série « Les Mystères d’Akeb », affaire Xavier Dupont de Ligonnès :
- Français naturel, oral, clair. Récit chronologique avec de vraies transitions ; aucun passage « à développer ».
- Chaque information vient du dossier (/home/user/TradingAgents/akeb-youtube/recherche). Rien de mémoire. Si un fait utile manque au dossier, ne l’écris pas : note-le dans « LACUNES » en fin de script annoté.
- Séparer à l’oral comme à l’écran : FAIT DOCUMENTÉ / TÉMOIGNAGE RAPPORTÉ (dire qui) / RECONSTITUTION DE L’ENQUÊTE (dire « selon l’enquête », « selon le parquet ») / HYPOTHÈSE (dire de qui) / FICTION (uniquement le roman). Une assertion à source unique se dit avec prudence (« selon X, seul à le rapporter »).
- Présomption : XDDL est recherché et désigné comme principal suspect par l’enquête ; il n’a jamais été jugé. Ne jamais énoncer sa culpabilité comme vérité judiciaire.
- Pas de faux dialogues, pas de pensées inventées, pas de scène imaginée (frontière, suicide, fuite). Les scènes ne sont reconstituées qu’à partir d’éléments attribuables.
- Victimes (Agnès, Arthur, Thomas, Anne, Benoît) présentées comme des personnes, avec respect, sans détail graphique ni opératoire, sans photo, sans les transformer en décor.
- Aucune identification ni localisation de particuliers (personnes arrêtées par erreur, sosies, signalants) ; aucun appel à traquer qui que ce soit.
- Divergences de sources : les signaler et formuler prudemment (notamment la date du ou des repas avec Thomas).
- Ne pas attribuer de dissimulation aux autorités sans preuve. Pas de probabilité chiffrée inventée. Pas de comparaison biométrique de voix.
- Interdits : « affaire résolue », « la vérité cachée », « on l’a retrouvé », « ses vraies confessions », « preuve exclusive », « inédit » (sauf preuve).
- « Moins connu » ≠ « inédit » : 2 à 4 détails moins souvent mis en avant par épisode, chacun utile à l’interprétation.
- Construction : accroche factuelle de 15 à 25 s posant UNE vraie question propre à l’épisode ; récit ; résolution de la question ; UNE transition vers l’épisode suivant (pas de cliffhanger mensonger).
- Longueur : 1 400 à 1 900 mots de narration (≈ 10 à 13 min à 155 mots/min). Plus court et dense vaut mieux qu’un remplissage. Ne jamais promettre une durée.
- Promotion du livre : 15 à 25 s (40 à 65 mots), à une transition naturelle ou en fin, JAMAIS pendant l’évocation des victimes ou des obsèques. Base à varier sobrement : « Cette affaire laisse un vide. Dans La dernière correction, Akeb a choisi de l’explorer par la fiction : un homme qui avait disparu commet l’erreur de reprendre la parole. C’est un roman, avec des personnages inventés et une fin imaginée. Vous pouvez le lire en e-book ou l’écouter en livre audio ; les deux liens sont dans la description. Revenons aux faits. » Les deux formats à égalité ; pas de pack ni d’offre gratuite. Le contenu doit valoir sans achat.
- Épisode 3 seulement : expliquer que l’appel du faux prêtre a inspiré le ressort du roman ; dans le roman l’appelant est le fugitif ; dans l’affaire réelle, ce lien n’est pas établi par les sources. Ne jamais laisser croire qu’une preuve est vendue dans le livre.
- Narration par voix de synthèse : les citations sont brèves (≤ 20 mots), attribuées, lues sobrement sans imitation.

FORMATS DE FICHIERS (exploités par les outils de montage ; respecte-les exactement) :

1) narration.txt — texte propre à prononcer, rien d’autre :
   - blocs « [S01] texte… » numérotés S01, S02… ; 1 à 4 phrases par segment (≈ 15 à 45 s), pour pouvoir régénérer un segment seul ;
   - lignes « [pause 1.2] » (secondes) après un segment pour laisser respirer une question ou un moment grave ;
   - lignes « # … » = commentaires ignorés. Pas d’étiquette de statut, pas de référence de source, pas de didascalie dans le texte prononcé ;
   - dates et nombres écrits comme on doit les dire si ambigu (« le 15 avril 2011 » va ; « XDDL » ne se prononce pas : écrire « Xavier Dupont de Ligonnès »).

2) storyboard.csv — en-tête exact : plan,segment,type,statut,texte,texte2,source,faits,poids,params
   - plan : P001, P002… dans l’ordre d’apparition ; segment : S01… (le plan couvre ce segment ; plusieurs plans d’un même segment se partagent sa durée selon « poids ») ou « - » pour un carton muet à durée fixe (params {"duree": 3}) ;
   - chaque segment de narration.txt a au moins un plan ; segments contigus et dans le même ordre ;
   - type ∈ avertissement | titre | chapitre | date | texte | citation | question | document | frise | carte | livre | sources ;
     titre : texte=titre, texte2=sous-titre, params {"numero":"01"} ; chapitre : texte=titre du chapitre, params {"numero":"1"} (sert aux chapitres YouTube : 3 minimum, ≥ 10 s chacun) ;
     date : texte=date, texte2=lieu, params {"precision":"…"} ; texte : texte=phrase courte à l’écran (≤ 30 mots), texte2=surtitre facultatif ;
     citation : texte=citation brève exacte du dossier, texte2=auteur et qualité ; question : texte=question ;
     document : tableau de synthèse ORIGINAL de la chaîne, texte=titre, texte2=lignes séparées par « | » (jamais un faux document de police) ;
     frise : frise commune, texte=titre, params {"jusqua":2011.3,"focus":[1961,2011],"curseur":2011.3} ;
     carte : texte=titre, params {"points":[{"lon":…,"lat":…,"label":"…","date":"…","cote":"gauche|droite"}],"bbox":[lonmin,latmin,lonmax,latmax],"trajet":true} — coordonnées et cadres UNIQUEMENT tirés de /home/user/TradingAgents/akeb-youtube/outils/donnees/lieux.json, et seulement pour des lieux sourcés ;
     livre : texte=lignes séparées par « | » (ex. « À lire en e-book | ou à écouter en livre audio | Liens dans la description ») ;
     sources : texte=titre, texte2=références courtes séparées par « | » ;
     avertissement : carton muet d’honnêteté (params {"duree":4}).
   - statut ∈ FAIT | TEMOIGNAGE | RECONSTRUCTION | HYPOTHESE | FICTION | vide ;
   - source = « Média, JJ/MM/AAAA » (date de la SOURCE) ; faits = date de l’ÉVÉNEMENT (les deux dates à l’écran) ;
   - CSV valide : champs contenant virgules ou guillemets entre guillemets doubles, guillemets internes doublés ; params en JSON valide.
   - Ouverture type : accroche (S01, cartons date/question), puis carton titre muet (3 s), puis carton avertissement muet (4 s), puis le récit.
   - Un visuel toutes les 6 à 12 s en moyenne ; frise commune au moins deux fois par épisode ; cartes sobres pour les trajets et lieux.

3) script_annote.md — version de travail :
   - en-tête : titre de travail, question de l’épisode, durée estimée (mots ÷ 155), liste des chapitres ;
   - pour chaque segment : « ### S01 », le texte exact de narration.txt, puis une liste : Statut ; Sources (identifiants S### de SOURCES.csv) ; Assertions (A### d’ASSERTIONS.csv) ; Incertitude ; Visuels (plans) ; Note de prudence éventuelle ;
   - en fin : « DÉTAILS MOINS CONNUS UTILISÉS », « DIVERGENCES SIGNALÉES », « LACUNES » (faits voulus mais absents du dossier), « TRANSITION VERS L’ÉPISODE SUIVANT ».
