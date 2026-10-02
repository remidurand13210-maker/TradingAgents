# Épisode 2 — gestes à faire dans YouTube Studio (Codex / Rémi)

Chaîne : **Les Mystères d'Akeb** (`UCeY1bZMUcigbZX2VwJmln-Q`, @LesMysteresDAkeb). Vérifier l'avatar en haut à droite avant tout geste : **jamais** La Brig'ads.
Tous les fichiers sont dans ce dossier. Rien n'est public tant que Rémi n'a pas répondu « oui » (point 19).

## ⚠️ Ordre de mise en public : 00 → 01 → 02 → 03 → 04
L'épisode 2 passe en public **après l'épisode 1** (J+7 de `chaine/CALENDRIER.md`) et **avant l'épisode 3**, qui reste privé tant que celui-ci n'est pas public.
**Il reste privé tant que l'épisode 1 n'est pas public** (ni public, ni non répertorié, ni planifié à une date antérieure à celle du 1). Il peut être importé, réglé et relu en privé dès maintenant.

## 1. Import en privé
1. Studio → **Créer → Importer des vidéos** → `video.mp4` (ou, depuis le cloud : `python3 outils/youtube_api.py envoyer exports/publication/02_avril_2011/video.mp4 exports/publication/02_avril_2011/metadonnees.json`, qui importe en privé et remplit titre, description, tags, catégorie).
2. Visibilité : **Privée** dès l'écran d'import. Ne pas planifier tant que la date de l'épisode 1 n'est pas fixée.

## 2. Détails
3. **Titre** : copier `titre` de `metadonnees.json` (69 caractères) :
   `Avril 2011 : un départ, deux versions | Dupont de Ligonnès, épisode 2`
4. **Description** : coller `description.txt` en entier, sans retouche (chapitres compris ; 4 368 octets, sous la limite de 5 000 : ne rien y ajouter).
5. **Miniature** : importer `miniature.png` (1280×720, PNG < 2 Mo). Ne pas utiliser une image extraite par YouTube.
6. **Playlist** : ajouter à « **Saison 1** », **en troisième position** (après la bande-annonce et l'épisode 1, avant les épisodes 3 et 4), même si l'épisode 3 a été importé avant lui.
7. **Public** : cocher « **Non, ce contenu n'est pas conçu pour les enfants** ». Pas de restriction d'âge.
8. Afficher plus :
   - **Promotion payante** : ne pas cocher (aucun partenariat tiers ; le lien avec Akeb est dit dans la description et à l'oral).
   - **Contenu modifié ou synthétique** : relire d'abord https://support.google.com/youtube/answer/14328491. Selon la règle lue le 01/10/2026, la case **n'est pas exigée** pour cet épisode : voix de synthèse d'un narrateur fictif qui n'imite personne, cartons, cartes et frises non réalistes, musique synthétisée par programme (pas d'IA générative), aucune reconstitution réaliste. → **Ne pas cocher**, sauf si le texte de la page a changé ou en cas de doute : alors **cocher** (aucune sanction pour une déclaration en trop).
   - **Tags** : coller ceux de `metadonnees.json` (10 tags), séparés par des virgules. Aucun nom de victime ni de particulier.
   - **Langue de la vidéo** et langue du titre/description : **Français**.
   - **Catégorie** : **Éducation** (récit documentaire sourcé des jours d'avril 2011, pas de l'actualité).
   - **Chapitres automatiques** : laisser activé ; les chapitres de la description priment (00:00 en premier, 7 chapitres, tous ≥ 10 s, mesurés sur l'export : `montage/rendu/02_avril_2011/chapitres.txt`). Vérifier après traitement que la barre de lecture affiche bien les 7 chapitres.
   - Commentaires : activés, tri « Les plus populaires » ; mode « Retenir les commentaires potentiellement inappropriés » (voir § 5).

## 3. Éléments vidéo
9. **Sous-titres** : Studio → Sous-titres → Français → **Importer un fichier** → « Avec minutage » → `sous_titres.fr.srt` → Enregistrer. Relire 3 ou 4 répliques après import (accents, début à 00:00:00,330, fin à 00:10:27,117).
10. **Écran de fin** et **fiche** vers l'épisode 3 : **à faire seulement quand l'épisode 3 sera public** (pour l'instant : écran de fin vers la playlist « Saison 1 », sur les 20 dernières secondes, sans masquer de texte). Une **fiche** vers l'épisode 1 peut être ajoutée vers 00:30 (« Avant avril : le club, le deuil, les achats »). Revenir sur cette vidéo le jour de la mise en ligne de l'épisode 3.

## 4. Vérifications
11. Onglet **Vérifications** : attendre la fin du **contrôle des droits d'auteur** (aucune revendication attendue : visuels, voix et musique produits pour la chaîne). En cas de revendication : ne pas publier, faire remonter.
12. Lire la vidéo privée en entier une fois traitée en HD (1080p disponible), avec les sous-titres.
13. Capture des réglages (Détails, Public, Contenu synthétique, Sous-titres, Communauté) dans `preuves/`.

## 5. Commentaires et communauté
14. Publier depuis la chaîne le texte de `commentaire_epingle.txt`, puis **Épingler** (menu ⋮ du commentaire). À faire quand la vidéo est visible (pendant la phase privée, le préparer seulement).
15. Studio → Paramètres → **Communauté** → Paramètres automatiques :
    - « **Liens** » : coché (commentaires avec URL retenus pour examen) ;
    - filtre des commentaires potentiellement inappropriés : activé (niveau « Strict » si proposé) ;
    - **Mots bloqués** : la liste de l'épisode 3 (qui contient celle de l'épisode 1), déjà saisie pour toute la chaîne ; ne rien retirer :
      `meurtrier, meurtrière, assassin, assassiné, tueur, il a tué, a tué sa, monstre, coupable, complice, complicité, adresse, son adresse, domicile, plaque, numéro de téléphone, sosie, je l'ai reconnu, je l'ai vu, connard, connasse, salaud, salope, ordure, pourriture, enculé, fils de pute, crève, nazi, c'est lui, c'est bien lui, il s'appelle, son vrai nom, de son vrai nom, je le connais, je sais qui, je sais où, il habite, il vit à, il se cache à, son profil, son compte, menteur, mythomane, escroc, imposteur, balance`
    - Ne saisir **aucun nom de particulier ni de victime** (proches, voisins, collègues, armurier, patron, hôteliers, témoins) : un nom saisi dans Studio reste une liste nominative.
16. Relire régulièrement la file « **En attente d'examen** » (conservée 60 jours). Supprimer sans débat tout commentaire qui décrit les violences subies par les victimes ou désigne un particulier.

## 6. Mise en public
17. **Préalable** : l'épisode 1 est public (vérifier dans `PUBLICATIONS.csv` et sur la chaîne, en fenêtre privée). Sinon : rester en privé, quelle que soit la réponse.
18. Envoyer à Rémi le **lien privé** (partage par adresse) avec la seule question : « Je publie : oui ou non ? ».
19. Seulement après « oui » explicite de Rémi, épisode 1 public, droits d'auteur verts et points 1 à 20 de `CONTROLE_AVANT_PUBLICATION.md` cochés : Visibilité → **Publique** (ou planifiée après l'épisode 1 ; J+7 du calendrier). Noter la date, l'URL et le « oui » dans `PUBLICATIONS.csv`.
20. Dans l'heure : vérifier le commentaire épinglé, la miniature (téléphone et ordinateur), les sous-titres, les chapitres, et les deux liens Payhip (paramètres `utm_content=ep02_ebook` / `ep02_audio` conservés jusqu'à la page produit). Revenir sur l'épisode 1 pour pointer son écran de fin et sa fiche vers celui-ci.

## Fichiers du dossier (préparés le 02/10/2026)
- `video.mp4` : 44 415 996 octets (≈ 44,4 Mo), H.264 High 1920×1080 à 30 i/s, CRF 23, preset slow, tune animation, AAC 48 kHz 192 kbit/s, `+faststart` (atome `moov` en tête). SSIM 0,995 face à l'export d'origine (`exports/videos/02_avril_2011.mp4`, 89,1 Mo). `outils/controle.py` : zéro alerte, −16,0 LUFS, −2,1 dBTP (origine −2,0), 627,2 s, 197 sous-titres sans chevauchement (rapport : `preuves/controles/02_publication_video_controle.json`, planche `02_publication_video_planche.png`).
- `metadonnees.json` (format de `outils/youtube_api.py envoyer`), `description.txt`, `commentaire_epingle.txt`, `sous_titres.fr.srt` (copie exacte de `exports/videos/02_avril_2011.fr.srt`, UTF-8, sans balise).
- `miniature.png` (1280×720, 0,6 Mo) et `miniature_test_168x94.png` ; `source_miniature.py` la régénère. Même charte que les épisodes 1 et 3 ; motif propre : deux enveloppes « AUSTRALIE ≠ ÉTATS-UNIS », texte « UN DÉPART / deux versions » (titre du chapitre 3).
- Sources de la description et du commentaire : titres et dates relus sur les pages le 02/10/2026 (curl, titre de la page et date de publication) ; contenu relu le 01/10/2026 (`episodes/02_avril_2011/VERIFICATION_V1.md`). Le Parisien du 22/04/2011 (S082), dont le titre nomme deux des enfants, volontairement **non** cité ; pour 20 Minutes du 03/04/2018 (S070), on cite le titre actuel de la page, le titre d'origine (arrestation de Glasgow) ayant été rectifié.
