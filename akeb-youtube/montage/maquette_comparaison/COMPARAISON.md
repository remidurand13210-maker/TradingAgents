# Comparaison des moteurs de rendu — maquette de 27,1 s (01/10/2026)

**But** : choisir le moteur des quatre épisodes animés à partir d'un **rendu réel**, avec la même maquette de chaque côté.
- **Contenu** : titre, frise des énigmes historiques, carte de fiction, phrase, question, couverture, carton du livre, question finale, fin.
- **Son** : même voix (Gemini/Algieba du Short 3, déjà produite, aucun nouvel appel), même nappe musicale originale, mêmes minutages, même charte et mêmes polices.

Fichiers (hors Git, régénérables) : `maquette_moteur_akeb.mp4`, `maquette_hyperframes.mp4`, `comparaison_cote_a_cote.mp4`.
Sources : `moteur_akeb/` (storyboard et narration), `hyperframes/index.html` (composition), `preparer.py` (éléments).

## Mesures

| Critère | Moteur Akeb (Python + ffmpeg) | HyperFrames 0.8.99 (HTML/GSAP + Chromium headless) |
|---|---|---|
| Sortie | MP4 H.264 1920×1080, 30 i/s, AAC 48 kHz stéréo | identique |
| Durée | 27,10 s | 27,10 s |
| Calcul (3 processus, 4 cœurs) | 84 s | 59 s, plus 11 s de compilation au premier rendu |
| Taille | 12,3 Mo | 14,2 Mo |
| Sonie / crête vraie | −16,2 LUFS / −1,6 dBTP | −16,4 LUFS / −1,9 dBTP, après limiteur ajouté en post-traitement (−1,2 dBTP sans) |
| Animation | révélation par bandes, poussée lente, tracé de carte, curseur de frise, mouvement sur photo | même palette, plus : lettres et mots animés un à un, courbes d'accélération riches (GSAP), mise en page CSS souple, tracés SVG |
| Typographie | correcte ; mises en page fixes par type de carton | plus soignée : centrage, accents de couleur dans le texte, lignes équilibrées |
| Pilotage | entièrement par `storyboard.csv` : les 233 plans des brouillons sont déjà rendables | HTML écrit à la main pour cette maquette ; pour les épisodes, il faut des **gabarits** générés depuis le même `storyboard.csv` |
| Reproductibilité | élevée (Python, polices et données dans le dépôt) | bonne si l'on fige le paquet (0.8.99) et le navigateur (Chromium headless 1194). Le mode Docker, plus déterministe, n'est pas disponible ici |
| Coût | 0 € | 0 € : licence Apache 2.0, rendu local, aucun compte HeyGen ni crédit ; télémétrie désactivée |
| Défauts constatés et corrigés | libellé « ÉPISODE » hors épisode ; étiquette de statut sur la couverture | apparitions trop lentes ; espaces doubles entre mots ; crête vraie à −1,2 dBTP |

Contrôles effectués :
- ffprobe, mesure EBU R128 avec crête vraie, planches de 11 instants comparés côte à côte ;
- linter HyperFrames : l'erreur « audio sans id », qui aurait rendu le son muet, a été corrigée.

**Non effectué** : un visionnage humain en mouvement, à faire par Rémi sur `comparaison_cote_a_cote.mp4`.

## Claude Design (vérifié le 01/10/2026 dans cette session)

- **Ce qui existe** : le type d'artefact **« Design »** est disponible (canevas d'écrans HTML). Ses exports HTML/ZIP et le transfert vers HyperFrames sont des fonctions de l'interface claude.ai : aucun outil de cette session ne les déclenche, et aucun export MP4 natif n'existe.
- **Modèle de la session** : `claude-opus-5-5`, vérifié par l'API de session (dernier tour servi par le même modèle, aucun usage supplémentaire activé).
- **Modèle de Claude Design** : celui utilisé par l'application Design elle-même n'est pas vérifiable d'ici.
- **Non utilisé** : Claude Design n'a servi à rien dans cette maquette. La composition HTML a été écrite directement dans la session.
- **Commande `/design`** : absente de la liste des commandes de cette session. L'outil `DesignSync` existe, mais il sert seulement à synchroniser des systèmes de design ; il n'est pas adapté ici.

## Remotion

Évalué sur dossier, sans maquette : le paquet 4.0.531 est disponible. Il ajouterait une chaîne React et son outil d'assemblage, ainsi qu'une licence gratuite seulement pour les particuliers et les petites structures, sans apporter plus que HyperFrames pour ce besoin. **Non retenu**, pour ne pas multiplier les outils.

## Recommandation

**Rendu visuel par HyperFrames, piloté par le storyboard existant.**
- Un gabarit HTML/GSAP par type de plan (titre, date, citation, document, frise, carte, photo, livre, question), écrit une seule fois aux couleurs de la chaîne.
- Python garde tout le reste : minutage sur la voix réelle, mixage −16 LUFS avec limiteur, sous-titres alignés, chapitres mesurés, contrôles.
- Le moteur Python reste en secours ; il produit déjà les épisodes complets.
- Claude Design reste facultatif : Rémi peut s'en servir pour explorer l'habillage (titres, miniatures). La production n'en dépend pas, puisque les exports passent par l'interface.

**À confirmer par Rémi** après visionnage de `comparaison_cote_a_cote.mp4`. S'il préfère le rendu du moteur Python, rien n'est perdu.
