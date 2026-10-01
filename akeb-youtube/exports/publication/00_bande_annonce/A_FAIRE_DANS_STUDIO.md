# Bande-annonce (00) — gestes à faire dans YouTube Studio (Codex / Rémi)

Chaîne : **Les Mystères d'Akeb** (`UCeY1bZMUcigbZX2VwJmln-Q`, @LesMysteresDAkeb). Vérifier l'avatar en haut à droite avant tout geste : **jamais** La Brig'ads.
Tous les fichiers sont dans ce dossier. Rien n'est public tant que Rémi n'a pas répondu « oui » (point 18).

## Ordre de mise en public de la saison
**00 → 01 → 02 → 03 → 04.** La bande-annonce passe en public la première (J0 du `chaine/CALENDRIER.md`), après la chaîne prête (point 19 de `CONTROLE_AVANT_PUBLICATION.md`).
L'épisode 3 a été produit avant l'épisode 2 mais reste **privé tant que l'épisode 2 n'est pas public**. Aucune vidéo n'est annoncée tant qu'elle est privée, planifiée ou en traitement.

## 1. Import en privé
1. Studio → **Créer → Importer des vidéos** → `video.mp4` (ou, depuis le cloud : `python3 outils/youtube_api.py envoyer exports/publication/00_bande_annonce/video.mp4 exports/publication/00_bande_annonce/metadonnees.json`, qui importe en privé et remplit titre, description, tags, catégorie).
2. Visibilité : **Privée** dès l'écran d'import.

## 2. Détails
3. **Titre** : copier `titre` de `metadonnees.json` (70 caractères, la limite fixée) :
   `Quatre épisodes, sources à l'appui | Dupont de Ligonnès, bande-annonce`
4. **Description** : coller `description.txt` en entier, sans retouche. **Pas de chapitres** : vidéo de 84 s, YouTube n'exige rien ; ne pas en ajouter.
5. **Miniature** : importer `miniature.png` (1280×720, PNG < 2 Mo). Ne pas utiliser une image extraite par YouTube.
6. **Playlist** : ajouter à « **Saison 1** » (la créer si elle n'existe pas encore), **en première position**.
7. **Public** : cocher « **Non, ce contenu n'est pas conçu pour les enfants** ». Pas de restriction d'âge.
8. Afficher plus :
   - **Promotion payante** : ne pas cocher (aucun partenariat tiers ; le lien avec Akeb est dit dans la description).
   - **Contenu modifié ou synthétique** : relire d'abord https://support.google.com/youtube/answer/14328491. Selon la règle lue le 01/10/2026, la case **n'est pas exigée** : voix de synthèse d'un narrateur fictif qui n'imite personne, cartons, carte et frise non réalistes, musique synthétisée par programme (pas d'IA générative), aucune reconstitution réaliste. → **Ne pas cocher**, sauf si le texte de la page a changé ou en cas de doute : alors **cocher** (aucune sanction pour une déclaration en trop).
   - **Tags** : coller ceux de `metadonnees.json` (9 tags), séparés par des virgules.
   - **Langue de la vidéo** et langue du titre/description : **Français**.
   - **Catégorie** : **Éducation** (présentation d'une série documentaire sourcée, pas de l'actualité).
   - **Chapitres automatiques** : désactiver (vidéo courte, aucun chapitre voulu).
   - Commentaires : activés, tri « Les plus populaires » ; mode « Retenir les commentaires potentiellement inappropriés » (voir § 5).

## 3. Éléments vidéo
9. **Sous-titres** : Studio → Sous-titres → Français → **Importer un fichier** → « Avec minutage » → `sous_titres.fr.srt` → Enregistrer. Relire 3 ou 4 répliques après import (accents, début à 00:00:00,180, fin à 00:01:15,520).
10. **Écran de fin** (les 20 dernières secondes, sans masquer de texte) : élément « Playlist » → « Saison 1 » + bouton « S'abonner ». Une fois l'épisode 1 public : remplacer par un élément « Vidéo » → épisode 1. **Fiche** vers l'épisode 1 seulement quand il est public.

## 4. Bande-annonce de la chaîne (non-abonnés)
11. **Seulement une fois la vidéo publique** : Studio → **Personnalisation → Disposition** → « **Bande-annonce de la chaîne pour les spectateurs non abonnés** » → Ajouter → choisir cette vidéo → **Publier**. (Optionnel : « Vidéo à la une pour les abonnés » = dernier épisode public.)
12. Vérifier dans une fenêtre privée (non connecté), sur ordinateur et téléphone, que la page d'accueil de la chaîne lance bien cette bande-annonce, avec la bonne miniature.

## 5. Vérifications
13. Onglet **Vérifications** : attendre la fin du **contrôle des droits d'auteur** (aucune revendication attendue : visuels, voix et musique produits pour la chaîne). En cas de revendication : ne pas publier, faire remonter.
14. Lire la vidéo privée en entier une fois traitée en HD (1080p disponible), avec les sous-titres.
15. Capture des réglages (Détails, Public, Contenu synthétique, Sous-titres, Communauté, Disposition) dans `preuves/`.

## 6. Commentaires et communauté
16. Publier depuis la chaîne le texte de `commentaire_epingle.txt`, puis **Épingler** (menu ⋮ du commentaire). À faire quand la vidéo est visible (pendant la phase privée, le préparer seulement).
17. Studio → Paramètres → **Communauté** → Paramètres automatiques (réglage valable pour toute la chaîne ; le faire une fois, avant la première vidéo publique) :
    - « **Liens** » : coché (commentaires avec URL retenus pour examen) ;
    - filtre des commentaires potentiellement inappropriés : activé (niveau « Strict » si proposé) ;
    - **Mots bloqués**, à saisir séparés par des virgules (même liste que l'épisode 1) :
      `meurtrier, meurtrière, assassin, assassiné, tueur, il a tué, a tué sa, monstre, coupable, complice, complicité, adresse, son adresse, domicile, plaque, numéro de téléphone, sosie, je l'ai reconnu, je l'ai vu, connard, connasse, salaud, salope, ordure, pourriture, enculé, fils de pute, crève, nazi`
    - Ne saisir **aucun nom de particulier** (homme interpellé à tort à Glasgow en 2019, témoins, voisins, personnes des pistes du Doubs ou du Texas, proches) : un nom saisi dans Studio reste une liste nominative.
    - Relire régulièrement la file « **En attente d'examen** » (conservée 60 jours). La bande-annonce de chaîne est la vidéo la plus vue par les nouveaux venus : y surveiller en priorité les commentaires qui « révèlent la fin » ou désignent quelqu'un.

## 7. Mise en public
18. Envoyer à Rémi le **lien privé** (partage par adresse) avec la seule question : « Je publie : oui ou non ? ». Seulement après « oui » explicite de Rémi, droits d'auteur verts et points 1 à 20 de `CONTROLE_AVANT_PUBLICATION.md` cochés : Visibilité → **Publique** (ou planifiée). Noter la date, l'URL et le « oui » dans `PUBLICATIONS.csv`. Puis faire le point 11.
19. Dans l'heure : vérifier le commentaire épinglé, la miniature (téléphone et ordinateur), les sous-titres, la bande-annonce de chaîne (point 12) et les deux liens Payhip (paramètres `utm_content=ep00_ebook` / `ep00_audio` conservés jusqu'à la page produit).

## Fichiers du dossier (préparés le 01/10/2026)
- `video.mp4` : 6 312 120 octets (≈ 6,3 Mo), H.264 High 1920×1080 à 30 i/s, CRF 23, preset slow, tune animation, AAC 48 kHz 192 kbit/s, `+faststart` (atome `moov` en tête). SSIM 0,995 face à l'export d'origine (`exports/videos/00_bande_annonce.mp4`, 14,4 Mo). `outils/controle.py` : zéro alerte, −16,0 LUFS, −2,1 dBTP (identique à l'origine), 84,0 s, 24 sous-titres sans chevauchement (rapport : `preuves/controles/00_publication_video_controle.json`, planche `00_publication_video_planche.png`).
- `metadonnees.json` (format de `outils/youtube_api.py envoyer`), `description.txt`, `commentaire_epingle.txt`, `sous_titres.fr.srt` (copie exacte de `exports/videos/00_bande_annonce.fr.srt`, UTF-8, sans balise).
- `miniature.png` (1280×720, 0,6 Mo) et `miniature_test_168x94.png` ; `source_miniature.py` la régénère. Même charte que l'épisode 1 (fond presque noir, barre ambre, Source Sans Pro) ; motif propre : quatre cases reliées 1-2-3-?, texte « SAISON 1 / 4 épisodes ».
