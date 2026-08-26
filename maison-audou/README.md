# Studio Maison Audou

Petite plateforme privée où les égéries déposent leurs prises de vue.

**Le principe :** ce que l'outil **affiche** est systématiquement flouté et filigrané —
donc inexploitable, y compris sur une capture d'écran. Ce que l'outil **conserve**
est l'original intact, dans un dossier sur disque, accessible à la seule direction.

```
coffre/
├── originaux/            ← les fichiers d'origine, octet pour octet
│   └── elsa-otaide/
│       └── 2026-08-26/
│           ├── IMG_1001.jpg
│           └── IMG_1002.jpg
├── apercus/              ← les versions floutées, celles que l'écran affiche
├── contrats/             ← où déposer les autorisations signées (PDF/scan)
└── maison-audou.db       ← index, comptes, journal d'accès
```

Le dossier `originaux/` est un dossier normal : en cas d'urgence, on l'ouvre
depuis le serveur, on le synchronise, on le copie. Aucun format propriétaire.

---

## Démarrage

```bash
cd maison-audou
npm install
cp .env.example .env          # puis renseigner ADMIN_PASSWORD
npm start                     # http://localhost:3000
```

Créer les accès des quatre égéries :

```bash
npm run egerie -- ajouter --nom "Elsa Otaide" --pays "France"
npm run egerie -- ajouter --nom "…"           --pays "…"
```

Chaque commande affiche **une seule fois** un code du type `H5M9-AWYR` :
seule son empreinte est stockée, il ne peut pas être retrouvé, seulement
remplacé (`npm run egerie -- code --id 1`). Transmettez-le par un canal privé.

Enregistrer l'autorisation signée d'une égérie (le contrat prévoit 10 ans à
compter de la signature) :

```bash
npm run egerie -- contrat --id 1 --statut signe --signe 2026-08-26 --fin 2036-08-26
```

Tout cela se fait aussi depuis l'interface, dans **Direction → Égéries**.

---

## Les deux espaces

**Égérie** — `/acces` : elle choisit son nom, saisit son code, glisse ses photos
(plusieurs à la fois, depuis un téléphone ou un ordinateur), ajoute une série et
un message, et coche la case confirmant que les images sont couvertes par son
autorisation. Elle revoit ses dépôts, floutés.

**Direction** — `/direction` : tableau de bord, dépôts de toutes les égéries,
fiche détaillée par photo, statut de chaque autorisation, journal d'accès.
Deux portes vers les originaux :

- `Télécharger l'original` sur une photo ;
- `Télécharger les originaux (ZIP)` sur une égérie filtrée.

Chacune est horodatée dans le journal (qui, quoi, quand, depuis quelle IP).

---

## Ce qui protège les images

| | |
|---|---|
| Flou | Gaussien, intensité réglable (`BLUR_SIGMA`, 20 par défaut). Vérifié en test : le contraste local chute d'un facteur ~15. |
| Filigrane | `MAISON AUDOU — CONFIDENTIEL` + nom de l'égérie + date, en diagonale répétée, posé **par-dessus** le flou. |
| Métadonnées | Les aperçus sont ré-encodés sans EXIF : ni GPS, ni modèle d'appareil, ni date de prise de vue ne fuient. Les originaux, eux, gardent tout. |
| Cloisonnement | Une égérie ne voit que ses propres dépôts. Sans session : rien, pas même une vignette. |
| Originaux | Jamais servis par une URL publique. Une seule route, réservée à la direction, journalisée. |
| Codes | Stockés en empreinte SHA-256, comparés en temps constant, 8 caractères sans lettres ambiguës. Limitation du nombre de tentatives. |
| Doublons | Détectés par empreinte SHA-256 : renvoyer deux fois la même photo n'encombre pas le coffre. |

Le flou est un rempart **contre la fuite d'un aperçu**, pas contre un accès
au serveur : qui a la main sur la machine a la main sur `originaux/`. C'est le
comportement voulu — le dossier de secours doit rester lisible.

---

## Vérification

```bash
npm run verif
```

Monte un coffre jetable et contrôle de bout en bout : connexion par code,
refus d'un mauvais code, dépôt, **original conservé octet pour octet**,
**aperçu réellement flouté** (mesure du contraste local), cloisonnement des
accès, retéléchargement conforme par la direction, journalisation, détection
de doublon, export ZIP.

---

## Mise en ligne

Les égéries sont réparties sur quatre fuseaux : il faut une URL joignable
depuis l'extérieur, en HTTPS.

```bash
docker compose up -d          # écoute sur 3000, coffre monté depuis ./coffre
```

Puis un reverse proxy (Caddy, Nginx, Traefik) devant, pour le certificat.
En production : `NODE_ENV=production`, `SECURE_COOKIES=true`, et un
`STORAGE_DIR` absolu pointant sur un volume sauvegardé.

**Sauvegarde.** Un seul dossier compte : `coffre/`. Une synchronisation
quotidienne suffit, par exemple `rclone sync coffre/ chiffre:maison-audou/`
vers un stockage distant. Sans elle, une panne de disque emporte les originaux.

### Réglages (`.env`)

| Variable | Défaut | Rôle |
|---|---|---|
| `ADMIN_PASSWORD` | — | Mot de passe direction. **Obligatoire.** |
| `STORAGE_DIR` | `coffre` | Emplacement du coffre. |
| `BLUR_SIGMA` | `20` | Force du flou (12 doux · 30 très opaque). |
| `PREVIEW_MAX` / `THUMB_MAX` | `1400` / `520` | Taille des aperçus, en pixels. |
| `MAX_FILE_MB` | `80` | Poids max par photo. |
| `MAX_FILES_PER_UPLOAD` | `40` | Nombre de photos par envoi. |
| `BRAND` | `Maison Audou` | Nom affiché et inscrit dans le filigrane. |

Changer `BLUR_SIGMA` n'affecte que les dépôts suivants : les aperçus déjà
générés restent tels quels.

---

## Formats

JPEG, PNG, WebP, TIFF, AVIF, GIF sont floutés normalement. Un HEIC d'iPhone
l'est aussi si la bibliothèque système sait le décoder — sinon **l'original
est conservé quand même** et la vignette affiche « original conservé, aperçu
impossible ». Rien n'est jamais perdu faute d'aperçu.

Les vidéos ne sont pas prises en charge pour l'instant : il faudrait ffmpeg
pour en flouter un extrait, faute de quoi un aperçu vidéo serait net.

---

## RGPD

Le contrat type (article 4) prévoit l'accès, la rectification, l'opposition et
l'effacement. En pratique :

- **Accès / portabilité** — `Direction → Dépôts`, filtrer sur l'égérie,
  `Télécharger les originaux (ZIP)`.
- **Effacement** — supprimer le dossier `coffre/originaux/<égérie>/`, les
  aperçus correspondants dans `coffre/apercus/<égérie>/`, puis les lignes de
  l'égérie dans la base. L'effacement ne vaut pas pour les visuels déjà
  diffusés de bonne foi (article 4 du contrat).
- **Opposition** — `Suspendre` coupe l'accès sans rien détruire.
- **Traçabilité** — le journal conserve chaque accès à un original.

Le tableau de bord signale une échéance d'autorisation à moins de 100 jours :
l'article 3 impose une dénonciation écrite **3 mois** avant, faute de quoi
l'autorisation se reconduit tacitement pour 2 ans.

Ce dépôt ne contient aucune donnée personnelle : le coffre est ignoré par git.
