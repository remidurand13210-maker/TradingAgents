# Reprise de la mission — procédure exacte

Branche : `claude/akeb-youtube-channel-kvu47n` du dépôt `remidurand13210-maker/TradingAgents` (dépôt **public** : aucune donnée privée, clé ou donnée de paiement ne doit y entrer).

## Pourquoi la mission s'est arrêtée le 30/09/2026

1. **Politique réseau de l'environnement cloud** : refus (403, `EGRESS_BLOCKED`) pour les sites de presse, Wikipédia, archive.org, youtube.com, payhip.com, ai.google.dev, support.google.com. Aucune page n'a pu être lue.
2. **Quota de recherches web de la session** épuisé (200/200) par la première vague d'agents, qui n'ont obtenu que des extraits de moteur.
3. Seul `recherche/brut/bio_jeunesse.json` a été sauvegardé (préliminaire, extraits de moteur uniquement). Aucun script d'épisode n'a été écrit : les écrire de mémoire aurait violé la règle « pas de biographie générée ».

## Deux façons de débloquer (au choix)

### Voie 1 — Antigravity (et DeepSeek) font la recherche sur le PC de Rémi

1. Coller `PROMPT_RECHERCHE_ANTIGRAVITY.md` dans Antigravity. Il clone la branche, écrit les 12 fichiers `recherche/brut/*.json` en lisant réellement les pages, corrobore, fusionne et pousse.
2. Facultatif : `PROMPT_RECHERCHE_DEEPSEEK.md` pour une contre-vérification indépendante des 4 thèmes sensibles (`recherche/contre_verif/`).
3. Puis, dans une session Claude Code (celle-ci ou une nouvelle) : « Reprends la mission Akeb depuis akeb-youtube/MISSION_REPRISE.md, étape Écriture. »
   L'écriture et la vérification n'ont besoin que du dossier : elles fonctionnent même avec le réseau restreint.

### Voie 2 — ouvrir le réseau de l'environnement cloud

Dans les réglages de l'environnement (menu de l'environnement cloud dans la barre de titre de la session, puis Modifier) :
- **Accès réseau** : niveau complet, ou ajout des domaines de presse et de référence utilisés par le dossier ;
- **Variable d'environnement** `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` = `800` ;
- **Variable d'environnement** `GEMINI_API_KEY` (la clé n'est jamais collée dans le chat ni écrite dans un fichier suivi).

Une **nouvelle session** prend ces réglages en compte. Lui dire : « Reprends la mission Akeb depuis akeb-youtube/MISSION_REPRISE.md. »

## Étapes (pour la session qui reprend)

1. **Lire** `ETAT.md`, `BUDGET.json`, `audio/manifest.json`, `PUBLICATIONS.csv`. Ne rien refaire qui soit déjà « généré », « contrôlé » ou « publié ».
2. **Recherche** (si non faite par Antigravity), en 4 workflows parallèles (plafond de 2 agents par workflow sur cette machine) :
   `Workflow({scriptPath: "akeb-youtube/outils/workflows/recherche_themes.js", args: {base, date, themes: [...], max_recherches: 14}})` avec les groupes
   `[bio_jeunesse, bio_famille, bio_travail_finances]`, `[avril_2011_avant, avril_2011_apres, decouverte_enquete]`, `[pistes_2011_2019, pistes_2020_2026, hypotheses_sort]`, `[plateformes, commerce_droits, emplacements_youtube]`.
   Un contrôle réseau préalable arrête le workflow si les pages restent illisibles.
3. **Fusion** : `python3 akeb-youtube/outils/fusion_recherche.py` → `SOURCES.csv`, `ASSERTIONS.csv`, `CHRONOLOGIE.csv`, `EMPLACEMENTS_YOUTUBE.csv`.
4. **Synthèse** (réseau requis pour la phase « Lacunes ») : `Workflow({scriptPath: "akeb-youtube/outils/workflows/recherche_synthese.js", args: {base, date}})`, puis refusion.
5. **Écriture** : `Workflow({scriptPath: "akeb-youtube/outils/workflows/ecriture_episodes.js", args: {base, date_publication_prevue}})`.
   Elle produit : frise commune, plan de saison, analyse des scénarios (trois analyses indépendantes), cinq scripts (bande-annonce et épisodes 1 à 4), double vérification, révision, raccords, métadonnées.
6. **Maquettes muettes** (relecture du rythme et des visuels, sans coût) : `python3 akeb-youtube/outils/montage.py <épisode> --maquette`, puis `controle.py`.
7. **Chiffrage de la narration** : relire la page de tarifs Gemini pour le modèle exact, remplir `audio/config_narration.json › tarifs`, lancer `python3 akeb-youtube/outils/narration_gemini.py estimer`, puis envoyer **une seule** demande d'enveloppe à Rémi (volumes réels, tarif vérifié, coût maximal réservé).
8. **Après accord** : inscrire l'enveloppe dans `BUDGET.json › narration.enveloppe_accordee_eur` ; `verifier-modele` (gemini-3.8-flash-tts, sans substitution) ; `echantillon` ; transcription de contrôle (aucune consigne vocalisée) ; `produire` (cache, verrou, reprise après quota).
   Toute la narration publiée est faite par Gemini 3.8 (voix Algieba), à la demande de Rémi.
9. **Montage final** : `montage.py <épisode>` puis `controle.py … --timeline … --voix …` ; miniatures (`identite.miniature`) ; chapitres mesurés dans les métadonnées.
10. **Chaîne, publication, campagne** : navigateur connecté de Rémi (Antigravity) ; suivre `chaine/*.md` et `publicite/PLAN_100_EUROS.md` ; consigner chaque statut réel dans `PUBLICATIONS.csv` et `ETAT.md`.
