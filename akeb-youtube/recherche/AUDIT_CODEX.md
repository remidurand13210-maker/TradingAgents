# Audit de la recherche Codex — 01/10/2026

**Provenance** : branche `codex/akeb-recherche` (commit `c1252ea`), fusionnée dans `claude/akeb-youtube-channel-kvu47n` (commit `5683f6a`). 11 fichiers dans `recherche/brut_codex/`, JSON valides, aucun motif de secret détecté.

| Fichier | Sources | Lues intégralement | Lues partiellement | Inaccessibles | Assertions |
|---|---|---|---|---|---|
| bio_jeunesse | 19 | 11 | 8 | 0 | 17 |
| bio_famille | 23 | 12 | 5 | 6 | 17 |
| bio_travail_finances | 25 | 15 | 8 | 2 | 20 |
| avril_2011_avant | 15 | 8 | 3 | 4 | 16 |
| avril_2011_apres | 19 | 12 | 4 | 3 | 20 |
| decouverte_enquete | 32 | 20 | 8 | 4 | 21 |
| pistes_2011_2019 | 24 | 16 | 4 | 4 | 21 |
| pistes_2020_2026 | 25 | 15 | 6 | 4 | 20 |
| hypotheses_sort | 24 | 17 | 4 | 3 | 17 |
| youtube_apports_codex | 15 | 13 | 2 | 0 | 10 |
| youtube_pistes_2024_2026_codex | 36 | 4 | 32 | 0 | 3 |
| **Total** | **257** | **143** | **84** | **30** | **182** |

Après fusion avec Bionic et le préliminaire : **250 sources distinctes** (dont 104 lues intégralement, en comptant le meilleur accès obtenu par l'un des outils), **285 assertions**, 214 jalons. **20 sources ont été trouvées indépendamment par plusieurs outils.**

## Lacunes des brouillons v0 comblées (sur sources lues)

- **Glasgow 2019** : dénonciation anonyme puis interpellation d'un voyageur le vendredi 11 octobre 2019 (`pistes_2011_2019`, trois sources lues intégralement).
- **Enfants** : naissances d'Arthur (1990), Thomas (1992), Anne (1994) et Benoît (1997) ; âges en avril 2011 : 20, 18, 16 et 13 ans. Arthur n'était pas le fils biologique de Xavier, qui l'a élevé avec Agnès.
- **Agnès** : née Hodanger ; emploi à temps partiel à Blanche-de-Castille, catéchèse ; lieux de vie successifs (selon ses propres écrits rapportés).
- **Découverte** : 21 avril 2011, cinquième visite policière selon RTL ; mandat d'arrêt international du 10 mai 2011, distinct de la recherche antérieure comme témoin ; différence entre notice rouge Interpol et mandat.
- **Finances et travail** : activité de réseau hôtelier pour représentants, financée par des adhésions (témoignage d'un ancien partenaire) ; train de vie décrit malgré les difficultés.
- **Dîner avec Thomas** : chronologies anciennes au 4 avril, retour de Thomas à Nantes le 5 avril ; la divergence reste à présenter comme telle.

## Particularités à respecter

- Les deux fichiers « youtube_… » reposent sur des **transcriptions automatiques** de vidéos de médias. Noms, dates et montants y sont à contrôler sur une source écrite indépendante avant usage. Ils ont aussi servi à constituer `publicite/EMPLACEMENTS_YOUTUBE.csv` : 30 vidéos, 23 chaînes.
- Codex et Bionic se recoupent sur plusieurs points, par exemple le 15 avril à 16 h 10, le retrait de 30 €, le Texas, le faux prêtre et Epsilon. Les divergences sont listées dans `CONTRADICTIONS_ET_LIMITES.md` (à régénérer après chaque fusion).

## Suite

1. Révision v1 des épisodes 2, 3 et 4 : remplacer les appuis fragiles (extraits de moteur, Bionic) par les sources Codex lues, et combler les lacunes signalées.
2. Écriture de l'épisode 1 et de la bande-annonce : le matériau `bio_*` est désormais suffisant.
3. Revérification ciblée, dans l'environnement Akeb, des points encore à source unique.
4. `VALIDATION.md` par épisode, puis chiffrage final et demande d'enveloppe.
