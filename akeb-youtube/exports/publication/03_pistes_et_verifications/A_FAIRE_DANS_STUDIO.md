# Épisode 3 — gestes à faire dans YouTube Studio (Codex / Rémi)

Chaîne : **Les Mystères d'Akeb** (`UCeY1bZMUcigbZX2VwJmln-Q`, @LesMysteresDAkeb). Vérifier l'avatar en haut à droite avant tout geste : **jamais** La Brig'ads.
Tous les fichiers sont dans ce dossier. Rien n'est public tant que Rémi n'a pas répondu « oui » (point 20).

## ⚠️ Ordre de mise en public : 00 → 01 → 02 → 03 → 04
L'épisode 3 a été produit **avant** l'épisode 2, mais il est publié **après** lui.
**Il reste privé tant que l'épisode 2 n'est pas public** (ni public, ni non répertorié, ni planifié à une date antérieure à celle du 2). Il peut être importé, réglé et relu en privé dès maintenant.
La veille de sa mise en public : relire l'actualité du dossier (`chaine/CALENDRIER.md`) — en particulier une décision de l'Arcom sur la séquence de M6 ou une conclusion sur le compte « Epsilon ». Toute nouveauté impose une mise à jour (description, commentaire épinglé, voire la vidéo) avant publication : l'épisode dit « au premier octobre 2026 ».

## 1. Import en privé
1. Studio → **Créer → Importer des vidéos** → `video.mp4` (ou, depuis le cloud : `python3 outils/youtube_api.py envoyer exports/publication/03_pistes_et_verifications/video.mp4 exports/publication/03_pistes_et_verifications/metadonnees.json`, qui importe en privé et remplit titre, description, tags, catégorie).
2. Visibilité : **Privée** dès l'écran d'import. Ne pas planifier tant que la date de l'épisode 2 n'est pas fixée.

## 2. Détails
3. **Titre** : copier `titre` de `metadonnees.json` (64 caractères) :
   `Quinze ans de pistes à l'épreuve | Dupont de Ligonnès, épisode 3`
4. **Description** : coller `description.txt` en entier, sans retouche (chapitres compris ; 4 710 octets, sous la limite de 5 000 : ne rien y ajouter).
5. **Miniature** : importer `miniature.png` (1280×720, PNG < 2 Mo). Ne pas utiliser une image extraite par YouTube.
6. **Playlist** : ajouter à « **Saison 1** », **en quatrième position** (après bande-annonce, épisodes 1 et 2), même si l'import a lieu avant celui de l'épisode 2.
7. **Public** : cocher « **Non, ce contenu n'est pas conçu pour les enfants** ». Pas de restriction d'âge.
8. Afficher plus :
   - **Promotion payante** : ne pas cocher (aucun partenariat tiers ; le lien avec Akeb est dit dans la description et à l'oral).
   - **Contenu modifié ou synthétique** : relire d'abord https://support.google.com/youtube/answer/14328491. Selon la règle lue le 01/10/2026, la case **n'est pas exigée** pour cet épisode : voix de synthèse d'un narrateur fictif qui n'imite personne, cartons, cartes et frises non réalistes, musique synthétisée par programme (pas d'IA générative), aucune reconstitution réaliste. → **Ne pas cocher**, sauf si le texte de la page a changé ou en cas de doute : alors **cocher** (aucune sanction pour une déclaration en trop).
   - **Tags** : coller ceux de `metadonnees.json` (10 tags), séparés par des virgules. Aucun nom de particulier.
   - **Langue de la vidéo** et langue du titre/description : **Français**.
   - **Catégorie** : **Éducation** (récit documentaire sourcé des pistes 2011-2026 et de leur vérification, pas de l'actualité).
   - **Chapitres automatiques** : laisser activé ; les chapitres de la description priment (00:00 en premier, 7 chapitres, tous ≥ 10 s, mesurés sur l'export : `montage/rendu/03_pistes_et_verifications/chapitres.txt`). Vérifier après traitement que la barre de lecture affiche bien les 7 chapitres.
   - Commentaires : activés, tri « Les plus populaires » ; mode « Retenir les commentaires potentiellement inappropriés » (voir § 5).

## 3. Éléments vidéo
9. **Sous-titres** : Studio → Sous-titres → Français → **Importer un fichier** → « Avec minutage » → `sous_titres.fr.srt` → Enregistrer. Relire 3 ou 4 répliques après import (accents, début à 00:00:00,270, fin à 00:09:38,883).
10. **Écran de fin** et **fiche** vers l'épisode 4 : **à faire seulement quand l'épisode 4 sera public** (pour l'instant : écran de fin vers la playlist « Saison 1 », sur les 20 dernières secondes, sans masquer de texte). Une **fiche** vers l'épisode 2 peut être ajoutée vers 00:29 (« 2011 : la disparition ») une fois l'épisode 2 public. Revenir sur cette vidéo le jour de la mise en ligne de l'épisode 4.

## 4. Vérifications
11. Onglet **Vérifications** : attendre la fin du **contrôle des droits d'auteur** (aucune revendication attendue : visuels, voix et musique produits pour la chaîne). En cas de revendication : ne pas publier, faire remonter.
12. Lire la vidéo privée en entier une fois traitée en HD (1080p disponible), avec les sous-titres.
13. Capture des réglages (Détails, Public, Contenu synthétique, Sous-titres, Communauté) dans `preuves/`.

## 5. Commentaires et communauté
14. Publier depuis la chaîne le texte de `commentaire_epingle.txt`, puis **Épingler** (menu ⋮ du commentaire). À faire quand la vidéo est visible (pendant la phase privée, le préparer seulement). Mettre à jour sa ligne « État au 01/10/2026 » à la date de publication.
15. Studio → Paramètres → **Communauté** → Paramètres automatiques :
    - « **Liens** » : coché (commentaires avec URL retenus pour examen) ;
    - filtre des commentaires potentiellement inappropriés : activé (niveau « Strict » si proposé) ;
    - **Mots bloqués** : la liste de l'épisode 1 **plus** les ajouts propres aux pistes (tentatives d'identifier l'homme de Glasgow, le visiteur du Doubs, l'appelant de l'émission, ou d'attribuer le compte Epsilon), à saisir séparés par des virgules :
      `meurtrier, meurtrière, assassin, assassiné, tueur, il a tué, a tué sa, monstre, coupable, complice, complicité, adresse, son adresse, domicile, plaque, numéro de téléphone, sosie, je l'ai reconnu, je l'ai vu, connard, connasse, salaud, salope, ordure, pourriture, enculé, fils de pute, crève, nazi, c'est lui, c'est bien lui, il s'appelle, son vrai nom, de son vrai nom, je le connais, je sais qui, je sais où, il habite, il vit à, il se cache à, son profil, son compte, menteur, mythomane, escroc, imposteur, balance`
    - Ne saisir **aucun nom de particulier** (homme interpellé à tort à Glasgow en 2019, visiteur de la communauté religieuse du Doubs, auteur du faux témoignage diffusé sur M6 — ni son nom ni son pseudonyme d'antenne —, hôtelier de Dieppe, personnes du Texas, témoins, proches) : un nom saisi dans Studio reste une liste nominative ; les formules ci-dessus suffisent à retenir les commentaires qui les citeraient.
16. Relire régulièrement la file « **En attente d'examen** » (conservée 60 jours). Supprimer sans débat tout commentaire qui nomme ou montre une personne mise hors de cause.

## 6. Mise en public
17. **Préalable** : l'épisode 2 est public (vérifier dans `PUBLICATIONS.csv` et sur la chaîne, en fenêtre privée). Sinon : rester en privé, quelle que soit la réponse.
18. Envoyer à Rémi le **lien privé** (partage par adresse) avec la seule question : « Je publie : oui ou non ? ».
19. Seulement après « oui » explicite de Rémi, épisode 2 public, droits d'auteur verts, relecture de l'actualité de la veille et points 1 à 20 de `CONTROLE_AVANT_PUBLICATION.md` cochés : Visibilité → **Publique** (ou planifiée après l'épisode 2 ; J+10 du calendrier). Noter la date, l'URL et le « oui » dans `PUBLICATIONS.csv`.
20. Dans l'heure : vérifier le commentaire épinglé, la miniature (téléphone et ordinateur), les sous-titres, les chapitres, et les deux liens Payhip (paramètres `utm_content=ep03_ebook` / `ep03_audio` conservés jusqu'à la page produit). Revenir sur l'épisode 2 pour pointer son écran de fin vers celui-ci.

## Fichiers du dossier (préparés le 01/10/2026)
- `video.mp4` : 41 722 220 octets (≈ 41,8 Mo), H.264 High 1920×1080 à 30 i/s, CRF 23, preset slow, tune animation, AAC 48 kHz 192 kbit/s, `+faststart` (atome `moov` en tête). SSIM 0,995 face à l'export d'origine (`exports/videos/03_pistes_et_verifications.mp4`, 86,3 Mo). `outils/controle.py` : zéro alerte, −16,0 LUFS, −2,2 dBTP (identique à l'origine), 578,9 s, 187 sous-titres sans chevauchement (rapport : `preuves/controles/03_publication_video_controle.json`, planche `03_publication_video_planche.png`).
- `metadonnees.json` (format de `outils/youtube_api.py envoyer`), `description.txt`, `commentaire_epingle.txt`, `sous_titres.fr.srt` (copie exacte de `exports/videos/03_pistes_et_verifications.fr.srt`, UTF-8, sans balise).
- `miniature.png` (1280×720, 0,6 Mo) et `miniature_test_168x94.png` ; `source_miniature.py` la régénère. Même charte que l'épisode 1 ; motif propre : rangée de sept pistes barrées et une huitième ouverte (« ? » ambre), texte « PLUS DE 1 850 signalements » (Le Parisien, 02/06/2026).
- Sources de la description et du commentaire : titres et dates relus sur les pages le 01/10/2026 ; La Dépêche du 03/06/2026 dont le titre cite le pseudonyme d'antenne de l'appelant (S188) volontairement **non** citée.
