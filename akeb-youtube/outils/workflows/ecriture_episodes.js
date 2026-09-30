export const meta = {
  name: 'akeb-ecriture-episodes',
  description: 'Écrit les 4 épisodes XDDL + bande-annonce : plan de saison, analyse ép. 4, rédaction, double vérification, révision, raccords, métadonnées',
  phases: [
    { title: 'Saison', detail: 'frise commune, répartition des faits, questions par épisode' },
    { title: 'Analyse', detail: 'trois analyses indépendantes du sort de XDDL, puis synthèse' },
    { title: 'Écriture', detail: 'un rédacteur par épisode' },
    { title: 'Vérification', detail: 'vérificateur factuel + vérificateur éditorial par épisode' },
    { title: 'Révision', detail: 'application des corrections' },
    { title: 'Raccords', detail: 'cohérence entre épisodes' },
    { title: 'Métadonnées', detail: 'titres, descriptions, miniatures, commentaires épinglés' },
  ],
}

// args : { base, date_publication_prevue }
const BASE = args.base
const R = BASE + '/recherche'
const E = BASE + '/episodes'
const DOSSIER = `${R}/SOURCES.csv, ${R}/ASSERTIONS.csv, ${R}/CHRONOLOGIE.csv, ${R}/CONTRADICTIONS_ET_LIMITES.md, ${R}/DETAILS_MOINS_CONNUS.md, et au besoin les fichiers détaillés ${R}/brut/*.json`

const REGLES = `RÈGLES ÉDITORIALES (non négociables) — série « Les Mystères d’Akeb », affaire Xavier Dupont de Ligonnès :
- Français naturel, oral, clair. Récit chronologique avec de vraies transitions ; aucun passage « à développer ».
- Chaque information vient du dossier (${R}). Rien de mémoire. Si un fait utile manque au dossier, ne l’écris pas : note-le dans « LACUNES » en fin de script annoté.
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
- Narration par voix de synthèse : les citations sont brèves (≤ 20 mots), attribuées, lues sobrement sans imitation.`

const FORMATS = `FORMATS DE FICHIERS (exploités par les outils de montage ; respecte-les exactement) :

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
     carte : texte=titre, params {"points":[{"lon":…,"lat":…,"label":"…","date":"…","cote":"gauche|droite"}],"bbox":[lonmin,latmin,lonmax,latmax],"trajet":true} — coordonnées et cadres UNIQUEMENT tirés de ${BASE}/outils/donnees/lieux.json, et seulement pour des lieux sourcés ;
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
   - en fin : « DÉTAILS MOINS CONNUS UTILISÉS », « DIVERGENCES SIGNALÉES », « LACUNES » (faits voulus mais absents du dossier), « TRANSITION VERS L’ÉPISODE SUIVANT ».`

const EPISODES = [
  { dir: '00_bande_annonce', num: '00', titre: 'Bande-annonce de la saison', brief: `Bande-annonce de 60 à 75 s (150 à 190 mots) présentant la chaîne et la saison : promesse « Disparitions, récits et zones d’ombre. Des faits sourcés, des hypothèses clairement identifiées et les chemins de la fiction. », les quatre épisodes (sans révéler la conclusion de l’épisode 4), le lien honnête avec l’auteur Akeb. Pas de promotion appuyée du livre (une phrase au plus). Pas de chapitres. Storyboard simple.` },
  { dir: '01_vie_avant_affaire', num: '01', titre: 'Xavier Dupont de Ligonnès : la vie avant l’affaire', brief: `Période : naissance, jeunesse, milieu familial, amitiés, vie adulte, voyages, mariage et enfants, travail et difficultés jusqu’à la veille de 2011. Frise biographique sourcée. Vérifie dates et lieux, projets américains, activités professionnelles ; ne comble aucun trou. Examine l’écart entre image sociale, témoignages de proches et situation matérielle documentée. Présente Agnès, Arthur, Thomas, Anne et Benoît comme des personnes, sans inventer leurs pensées. Les comportements familiaux rapportés sont attribués aux témoins ; une enfance ou une croyance ne prédit pas un crime. Point d’arrivée : qu’est-ce qui est déjà en crise avant les événements de 2011 ? Transition vers l’épisode 2.` },
  { dir: '02_avril_2011', num: '02', titre: 'Avril 2011 : les jours qui changent tout', brief: `Période : début 2011 jusqu’à la dernière trace authentifiée d’avril. Distingue activité observée, témoignage et reconstitution de l’enquête. Mort du père, pratique du tir (rapportée dès décembre 2010, AVANT la mort du père en janvier : ne pas la présenter comme causée par l’héritage), journées de la famille, absences, messages et courriers, trajets : vérifie l’ordre. Angle fort : les récits de départ ne sont pas identiques selon les destinataires (document de synthèse comparatif). Pas de description graphique ni de détail opératoire. Divergence sur la date du repas avec Thomas : notes + formulation prudente. Termine au dernier point vérifié, sans scène imaginée. Transition vers l’épisode 3.` },
  { dir: '03_pistes_et_verifications', num: '03', titre: 'Après la disparition : les pistes et leurs vérifications', brief: `Période : découverte des corps, premières recherches, puis évolution jusqu’à la date réelle de publication (${args.date_publication_prevue || 'à préciser'}). Pistes : fausse arrestation en Écosse (2019), signalement du Doubs écarté (2024), appel à informations au Texas (2026), émission et faux prêtre (2026), vérifications annoncées autour du compte Epsilon (2026), et toute évolution plus récente du dossier. Pour chacune : information initiale, auteur de l’affirmation, contrôle réalisé, résultat public ou inconnu (tableau de synthèse). Pas de compilation de ressemblances. Fil narratif : comment une piste acquiert une apparence de certitude, puis ce qui résiste à la vérification. Tournant télévisé = moment fort, sans prétendre que l’appelant était le fugitif. Promotion : c’est ici que l’on peut dire que l’appel du faux prêtre a inspiré le ressort du roman, avec la distinction fiction/réalité. Transition vers l’épisode 4.` },
  { dir: '04_notre_hypothese', num: '04', titre: 'Mort ou vivant ? Le scénario que nous retenons', brief: `Prise de position, pas une esquive. Compare sérieusement au moins trois scénarios : décès après la disparition ; fuite durable à l’étranger ; vie discrète plus proche. Pour chacun : appuis, objections, suppositions nécessaires, observations qui changeraient l’analyse. Aucun pourcentage. Appuie-toi sur ${E}/04_notre_hypothese/ANALYSE_SCENARIOS.md (synthèse de trois analyses indépendantes). Choisis l’hypothèse dominante qu’elle retient et explique franchement pourquoi. Ligne proposée à examiner : « un décès après avril 2011 paraît plus plausible qu’une cavale internationale démontrée » — retiens-en une autre seulement si le dossier la soutient mieux, et dis pourquoi. Ne transforme pas l’absence de preuve de survie en preuve de décès, ni une préparation de départ en preuve de survie pendant quinze ans. Présente la meilleure objection à ta propre conclusion, puis l’élément concret qui ferait changer d’avis. Formulation possible : « Si je dois retenir un scénario, je privilégie […], pour ces raisons. Je ne peux pas désigner un lieu, et aucun élément cité ici n’établit définitivement ce sort. » Conclusion intelligible, assumée et révisable ; aucun spectateur n’a besoin du roman pour l’entendre. Termine par une invitation à signaler les erreurs factuelles (commentaire épinglé de corrections) et une question de discussion centrée sur un document, jamais sur l’identification de quelqu’un.` },
]

const ISSUES = {
  type: 'object',
  properties: {
    problemes: { type: 'array', items: { type: 'object', properties: {
      segment: { type: 'string' }, gravite: { type: 'string', enum: ['bloquant', 'important', 'mineur'] },
      probleme: { type: 'string' }, correction: { type: 'string' },
    }, required: ['segment', 'gravite', 'probleme', 'correction'] } },
    bilan: { type: 'string' },
  },
  required: ['problemes', 'bilan'],
}

phase('Saison')
await agent(`Tu prépares la saison 1 de « Les Mystères d’Akeb » (quatre épisodes + bande-annonce sur l’affaire Xavier Dupont de Ligonnès). Lis le dossier : ${DOSSIER}.
${REGLES}
Produis deux fichiers (outil Write) :
1) ${E}/frise_commune.json : {"evenements":[{"annee":<décimal, ex. 2011.29 pour mi-avril>,"label":"<≤ 22 caractères>","statut":"FAIT|TEMOIGNAGE|HYPOTHESE","haut":true|false,"sources":["S###"]}]} — 14 à 20 jalons de 1961 à ${args.date_publication_prevue || '2026'}, uniquement des éléments du dossier, alternance haut/bas pour éviter les chevauchements. Valide le JSON avec python3 -m json.tool.
2) ${E}/PLAN_SAISON.md : pour chaque épisode (00 à 04) la question centrale, les chapitres (3 à 6), les faits clés assignés (identifiants A###) sans doublon entre épisodes sauf rappel bref, les 2 à 4 détails moins connus choisis, les cartes et documents de synthèse prévus, la place de la promotion, la phrase de transition vers l’épisode suivant. Signale les faits nécessaires absents du dossier.
Réponds « fait ».`, { label: 'saison:plan', phase: 'Saison' })

phase('Analyse')
const ANGLES = [
  'Analyse en enquêteur méthodique : pars des traces matérielles et de leur absence, du terrain et des moyens disponibles.',
  'Analyse en avocat de la défense de chaque scénario tour à tour : donne à chaque hypothèse sa meilleure version avant de la critiquer.',
  'Analyse en épistémologue : distingue ce que chaque élément prouve, rend plausible ou ne permet pas de dire ; traque les raisonnements circulaires et les biais de confirmation.',
]
const analyses = await parallel(ANGLES.map((angle, i) => () => agent(`Lis le dossier : ${DOSSIER}. Question : que peut-on raisonnablement penser du sort de Xavier Dupont de Ligonnès après avril 2011 ?
${angle}
Compare au moins : (A) décès après la disparition ; (B) fuite durable à l’étranger ; (C) vie discrète plus proche. Pour chacun : appuis (avec A###/S###), objections, suppositions nécessaires, observations qui changeraient l’analyse. Aucun pourcentage. Puis choisis une hypothèse dominante et justifie-la, avec la meilleure objection contre ton choix et l’élément concret qui te ferait changer d’avis. N’utilise que le dossier.`, { label: `analyse:${i + 1}`, phase: 'Analyse', schema: {
  type: 'object', properties: {
    scenarios: { type: 'array', items: { type: 'object', properties: { nom: { type: 'string' }, appuis: { type: 'array', items: { type: 'string' } }, objections: { type: 'array', items: { type: 'string' } }, suppositions: { type: 'array', items: { type: 'string' } }, ce_qui_changerait: { type: 'array', items: { type: 'string' } } }, required: ['nom', 'appuis', 'objections', 'suppositions', 'ce_qui_changerait'] } },
    hypothese_dominante: { type: 'string' }, justification: { type: 'string' }, meilleure_objection: { type: 'string' }, element_qui_ferait_changer: { type: 'string' },
  }, required: ['scenarios', 'hypothese_dominante', 'justification', 'meilleure_objection', 'element_qui_ferait_changer'] } })))
await agent(`Trois analyses indépendantes du sort de Xavier Dupont de Ligonnès (JSON) :
${JSON.stringify(analyses.filter(Boolean))}
Rédige ${E}/04_notre_hypothese/ANALYSE_SCENARIOS.md : tableau comparatif des scénarios (appuis, objections, suppositions, ce qui changerait l’analyse), convergences et désaccords entre les trois analyses, hypothèse retenue par la majorité (ou, en cas de désaccord, celle que le dossier soutient le mieux, en expliquant), meilleure objection, élément qui ferait changer d’avis. Aucun pourcentage. Vérifie chaque référence A###/S### dans ${R}/ASSERTIONS.csv et ${R}/SOURCES.csv. Réponds par l’hypothèse retenue en une phrase.`, { label: 'analyse:synthese', phase: 'Analyse' })

const resultats = await pipeline(
  EPISODES,
  (ep) => agent(`Tu es scénariste-documentariste. Écris l’épisode ${ep.num} « ${ep.titre} » dans ${E}/${ep.dir}/ (crée le dossier si besoin).
Lis d’abord : ${E}/PLAN_SAISON.md, ${E}/frise_commune.json, le dossier (${DOSSIER}), ${BASE}/outils/donnees/lieux.json${ep.num === '04' ? `, ${E}/04_notre_hypothese/ANALYSE_SCENARIOS.md` : ''}.
CONSIGNE DE L’ÉPISODE : ${ep.brief}
${REGLES}
${FORMATS}
Écris les trois fichiers narration.txt, storyboard.csv, script_annote.md (outil Write). Vérifie ensuite avec Bash :
python3 -c "import csv,json,sys; r=list(csv.DictReader(open('${E}/${ep.dir}/storyboard.csv',encoding='utf-8'))); [json.loads(x['params']) for x in r if x['params'].strip()]; print(len(r),'plans')"
et compte les mots : python3 -c "import re;t=open('${E}/${ep.dir}/narration.txt',encoding='utf-8').read();print(sum(len(m.split()) for m in re.findall(r'^\\[S\\d+[a-z]?\\]\\s*(.*)$',t,re.M)))"
Réponds : nombre de mots, nombre de segments, nombre de plans, lacunes éventuelles.`, { label: `ecriture:${ep.num}`, phase: 'Écriture' }),
  (_r, ep) => parallel([
    () => agent(`VÉRIFICATION FACTUELLE ADVERSARIALE — épisode ${ep.num}. Lis ${E}/${ep.dir}/script_annote.md, narration.txt et storyboard.csv, puis le dossier (${DOSSIER}).
Pour CHAQUE affirmation factuelle (dates, lieux, âges, montants, citations, attributions, ordre des faits) : retrouve l’assertion et la source citées ; vérifie qu’elles disent bien cela, que le statut (fait / témoignage / reconstitution / hypothèse) est juste, que les divergences sont signalées, que les citations sont exactes et ≤ 20 mots, que les dates de source et d’événement à l’écran sont correctes, que les coordonnées de cartes viennent de lieux.json. Sois sceptique : toute affirmation sans appui dans le dossier est un problème « bloquant ». Si WebFetch fonctionne, tu peux relire une source pour trancher.`, { label: `verif-faits:${ep.num}`, phase: 'Vérification', schema: ISSUES }),
    () => agent(`VÉRIFICATION ÉDITORIALE ET ÉTHIQUE — épisode ${ep.num}. Lis ${E}/${ep.dir}/script_annote.md, narration.txt et storyboard.csv.
Contrôle le respect de TOUTES ces règles et relève chaque manquement :
${REGLES}
Contrôle aussi : accroche 15-25 s avec une vraie question ; transitions ; longueur (1 400-1 900 mots sauf bande-annonce) ; promotion à bonne place et bonne durée ; présomption ; pas de pensée ni dialogue inventés ; lisibilité orale (phrases prononçables par une voix de synthèse, pas d’abréviations, pas de parenthèses) ; format exact des fichiers (${FORMATS.slice(0, 400)}…).`, { label: `verif-edito:${ep.num}`, phase: 'Vérification', schema: ISSUES }),
  ]),
  (verifs, ep) => {
    const probs = (verifs || []).filter(Boolean).flatMap(v => v.problemes)
    return agent(`RÉVISION — épisode ${ep.num} (${E}/${ep.dir}/). Voici les problèmes relevés par deux vérificateurs indépendants (JSON) :
${JSON.stringify(probs)}
Corrige narration.txt, storyboard.csv et script_annote.md en conséquence (outil Edit ou Write) : tous les « bloquant » et « important », les « mineur » quand ils sont justes. Un fait sans appui dans le dossier est SUPPRIMÉ ou reformulé prudemment avec son attribution, jamais conservé tel quel. Garde la cohérence entre les trois fichiers (mêmes segments, même texte). Ajoute en fin de script_annote.md une section « JOURNAL DE VÉRIFICATION » : chaque problème, décision, correction. Revalide le CSV et le JSON des params comme lors de l’écriture. Réponds : nombre de corrections, nombre de mots final.`, { label: `revision:${ep.num}`, phase: 'Révision' })
  },
)

phase('Raccords')
await agent(`RACCORDS DE SAISON. Lis les cinq dossiers ${E}/00_bande_annonce, 01_vie_avant_affaire, 02_avril_2011, 03_pistes_et_verifications, 04_notre_hypothese (narration.txt, storyboard.csv, script_annote.md) et ${E}/PLAN_SAISON.md.
Vérifie : continuité chronologique sans trou ni doublon injustifié ; chaque transition annonce correctement l’épisode suivant ; même vocabulaire de statut ; mêmes dates et orthographes partout (Ligonnès, Roquebrune-sur-Argens…) ; frise commune utilisée de façon progressive (curseur qui avance) ; promotions variées et bien placées ; aucune contradiction entre épisodes ; la conclusion de l’épisode 4 n’est pas révélée avant. Corrige directement les fichiers concernés (un fichier à la fois), en maintenant la cohérence narration/storyboard/annoté, puis ajoute ${E}/RACCORDS.md listant chaque correction. Réponds par le nombre de corrections.`, { label: 'raccords', phase: 'Raccords' })

phase('Métadonnées')
const meta = await pipeline(EPISODES, (ep) => agent(`Rédige ${E}/${ep.dir}/metadonnees.md pour la vidéo YouTube de l’épisode ${ep.num}, d’après ses fichiers et ${R}/SOURCES.csv :
- 3 propositions de titre descriptif (≤ 70 caractères, nom de l’affaire autorisé car l’épisode la traite ; pas de racolage, pas de formulation interdite), puis le titre recommandé ;
- description complète : résumé honnête (2-3 phrases), avertissement (chaîne indépendante liée à l’auteur Akeb ; ni police ni enquête officielle ni émission ; aucune caution des familles), « Chapitres : » suivi de la mention « [insérés après mesure de l’export] », sources principales (média, titre, date, URL), crédits (narration par voix de synthèse Gemini — voix Algieba ; musique originale générée pour la chaîne ; cartes : fond Natural Earth, domaine public ; visuels originaux), lien commercial transparent vers les deux formats du roman avec liens UTM :
  E-book : https://payhip.com/b/INPGL?utm_source=youtube&utm_medium=video&utm_campaign=lma_xddl&utm_content=ep${ep.num}_ebook
  Livre audio : https://payhip.com/b/0HWpa?utm_source=youtube&utm_medium=video&utm_campaign=lma_xddl&utm_content=ep${ep.num}_audio
  (préciser : roman de fiction, personnages inventés ; e-book EPUB + PDF 2,99 € ; livre audio MP3 + M4B 4,99 €) ;
- mots-clés (10 à 15, sans bourrage) ; catégorie suggérée ;
- texte de miniature : 2 à 5 mots forts + un mot d’accent, sans visage réel ni formulation interdite ;
- commentaire épinglé « corrections factuelles » + une question de discussion centrée sur un document (jamais sur l’identification de quelqu’un) ;
- déclarations : public « Non, cette vidéo n’est pas conçue pour les enfants » ; contenu modifié ou synthétique : réponse à déterminer selon la règle YouTube en vigueur (voix de synthèse d’un narrateur non réel, aucune personne réelle imitée, aucun événement réel fabriqué) — l’indiquer comme point à vérifier au moment de l’envoi.
Réponds « fait ».`, { label: `meta:${ep.num}`, phase: 'Métadonnées' }))

return { episodes: resultats.map((r, i) => ({ ep: EPISODES[i].num, revision: r })), metadonnees: meta.length }
