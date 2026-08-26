import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import express from 'express';
import cookieParser from 'cookie-parser';
import multer from 'multer';
import archiver from 'archiver';

import {
  ROOT,
  PORT,
  BRAND,
  NODE_ENV,
  ORIGINALS_DIR,
  PREVIEWS_DIR,
  TMP_DIR,
  STORAGE_DIR,
  ADMIN_PASSWORD,
  MAX_FILE_MB,
  MAX_FILES_PER_UPLOAD,
  IMAGE_MIME,
} from './config.js';
import { db, now, hashCode, creerEgerie, reinitialiserCode, journaliser } from './db.js';
import {
  chargerSession,
  ouvrirSession,
  fermerSession,
  exigerAdmin,
  exigerEgerie,
  limiter,
  reinitialiserLimite,
} from './auth.js';
import { fabriquerApercus, apercuIndisponible } from './images.js';
import * as vues from './views.js';

const app = express();
app.set('trust proxy', 1);
app.disable('x-powered-by');
app.use(express.urlencoded({ extended: false, limit: '256kb' }));
app.use(cookieParser());
app.use(chargerSession);

app.use((_req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Referrer-Policy', 'no-referrer');
  next();
});

app.use('/statique', express.static(path.join(ROOT, 'public'), { maxAge: '1h' }));

const ip = (req) => (req.headers['x-forwarded-for']?.split(',')[0] || req.ip || '').trim();

/* ------------------------------------------------------------ Messages */

const MESSAGES = {
  depot: (q) => {
    const n = Number(q.n || 0);
    const doublons = Number(q.d || 0);
    const echecs = Number(q.e || 0);
    const bouts = [`${n} photo${n > 1 ? 's' : ''} reçue${n > 1 ? 's' : ''} et mise${n > 1 ? 's' : ''} au coffre.`];
    if (doublons) bouts.push(`${doublons} doublon${doublons > 1 ? 's' : ''} ignoré${doublons > 1 ? 's' : ''}.`);
    if (echecs) bouts.push(`${echecs} fichier${echecs > 1 ? 's' : ''} non lisible${echecs > 1 ? 's' : ''} : conservé${echecs > 1 ? 's' : ''} tel quel, sans aperçu.`);
    return { type: 'succes', texte: bouts.join(' ') };
  },
  vide: () => ({ type: 'erreur', texte: 'Aucun fichier reçu.' }),
  trop_gros: () => ({
    type: 'erreur',
    texte: `Fichier refusé : ${MAX_FILE_MB} Mo maximum par photo, ${MAX_FILES_PER_UPLOAD} par envoi.`,
  }),
  type_refuse: () => ({ type: 'erreur', texte: "Seules les images sont acceptées." }),
  egerie_creee: () => ({ type: 'succes', texte: "Accès créé. Transmettez le code ci-dessous." }),
  egerie_maj: () => ({ type: 'succes', texte: 'Fiche mise à jour.' }),
  statut_maj: () => ({ type: 'succes', texte: 'Statut mis à jour.' }),
  actif_maj: () => ({ type: 'succes', texte: "Accès modifié." }),
};

function flash(req) {
  const code = req.query.m;
  return MESSAGES[code] ? MESSAGES[code](req.query) : null;
}

const rediriger = (res, url, code, extra = {}) => {
  const params = new URLSearchParams({ m: code, ...extra });
  res.redirect(`${url}${url.includes('?') ? '&' : '?'}${params}`);
};

/* -------------------------------------------------------------- Requetes */

const qEgeriesActives = db.prepare(
  'SELECT id, nom, slug, pays, contrat_statut FROM egeries WHERE active = 1 ORDER BY nom'
);
const qEgerieParSlug = db.prepare('SELECT * FROM egeries WHERE slug = ? AND active = 1');
const qEgerieParId = db.prepare('SELECT * FROM egeries WHERE id = ?');
const qDepotsEgerie = db.prepare(
  'SELECT * FROM depots WHERE egerie_id = ? ORDER BY depose_le DESC LIMIT 300'
);
const qDepot = db.prepare(`
  SELECT d.*, e.nom AS egerie_nom, e.slug AS egerie_slug, e.contrat_statut
  FROM depots d JOIN egeries e ON e.id = d.egerie_id WHERE d.id = ?`);

/* ---------------------------------------------------------------- Public */

app.get('/', (req, res) => {
  if (req.session?.role === 'admin') return res.redirect('/admin');
  if (req.session?.role === 'egerie') return res.redirect('/depot');
  return res.send(vues.pageAccueil());
});

app.get('/acces', (req, res) => {
  if (req.session?.role === 'egerie') return res.redirect('/depot');
  res.send(
    vues.pageAccesEgerie({
      egeries: qEgeriesActives.all(),
      erreur: req.query.e ? "Nom ou code incorrect." : null,
      slugChoisi: req.query.slug || '',
    })
  );
});

app.post('/acces', (req, res) => {
  const { slug = '', code = '' } = req.body;
  const cle = `acces:${ip(res.req)}`;
  const jauge = limiter(cle, 10);
  if (!jauge.autorise) {
    return res.status(429).send(
      vues.pageErreur({
        code: 429,
        message: `Trop de tentatives. Réessayez dans ${Math.ceil(jauge.dansSecondes / 60)} minutes.`,
      })
    );
  }

  const egerie = qEgerieParSlug.get(slug);
  const attendu = egerie ? Buffer.from(egerie.code_hash) : Buffer.alloc(64);
  const fourni = Buffer.from(hashCode(code));
  const bon = egerie && attendu.length === fourni.length && crypto.timingSafeEqual(attendu, fourni);

  if (!bon) {
    journaliser({ acteur: slug || 'inconnu', action: 'acces_refuse', ip: ip(res.req) });
    return res.redirect(`/acces?e=1&slug=${encodeURIComponent(slug)}`);
  }

  reinitialiserLimite(cle);
  ouvrirSession(res, { role: 'egerie', id: egerie.id, nom: egerie.nom, slug: egerie.slug });
  journaliser({ acteur: egerie.nom, action: 'connexion_egerie', ip: ip(res.req) });
  res.redirect('/depot');
});

app.get('/deconnexion', (req, res) => {
  fermerSession(res);
  res.redirect('/');
});

/* --------------------------------------------------------- Espace egerie */

app.get('/depot', exigerEgerie, (req, res) => {
  const egerie = qEgerieParId.get(req.session.id);
  if (!egerie || !egerie.active) {
    fermerSession(res);
    return res.redirect('/acces');
  }
  const depots = qDepotsEgerie.all(egerie.id);
  res.send(
    vues.pageDepot({
      egerie,
      depots,
      flash: flash(req),
      totalOctets: depots.reduce((s, d) => s + d.octets, 0),
    })
  );
});

const televersement = multer({
  storage: multer.diskStorage({
    destination: (_req, _file, cb) => cb(null, TMP_DIR),
    filename: (_req, _file, cb) => cb(null, `${crypto.randomUUID()}.part`),
  }),
  limits: { fileSize: MAX_FILE_MB * 1024 * 1024, files: MAX_FILES_PER_UPLOAD },
  fileFilter: (_req, file, cb) => {
    if (IMAGE_MIME.has(file.mimetype) || file.mimetype === 'application/octet-stream') return cb(null, true);
    return cb(Object.assign(new Error('type refuse'), { code: 'TYPE_REFUSE' }));
  },
}).array('photos', MAX_FILES_PER_UPLOAD);

function nomSur(nom) {
  return (
    path
      .basename(String(nom || 'photo'))
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^A-Za-z0-9._-]+/g, '_')
      .replace(/^[._]+/, '')
      .slice(-90) || 'photo.jpg'
  );
}

function sha256Fichier(chemin) {
  return new Promise((resolve, reject) => {
    const h = crypto.createHash('sha256');
    fs.createReadStream(chemin)
      .on('data', (c) => h.update(c))
      .on('error', reject)
      .on('end', () => resolve(h.digest('hex')));
  });
}

async function cheminLibre(dossier, nom) {
  let candidat = path.join(dossier, nom);
  let n = 2;
  const ext = path.extname(nom);
  const base = nom.slice(0, nom.length - ext.length);
  // Deux egeries peuvent envoyer « IMG_0042.jpg » le meme jour : on ne perd
  // jamais un fichier au profit d'un autre.
  while (fs.existsSync(candidat)) {
    candidat = path.join(dossier, `${base}-${n}${ext}`);
    n += 1;
  }
  return candidat;
}

app.post('/depot/envoi', exigerEgerie, (req, res) => {
  televersement(req, res, async (err) => {
    if (err) {
      if (err.code === 'TYPE_REFUSE') return rediriger(res, '/depot', 'type_refuse');
      return rediriger(res, '/depot', 'trop_gros');
    }

    const egerie = qEgerieParId.get(req.session.id);
    if (!egerie || !egerie.active) {
      fermerSession(res);
      return res.redirect('/acces');
    }

    const fichiers = req.files || [];
    if (!fichiers.length) return rediriger(res, '/depot', 'vide');

    const lot = crypto.randomUUID();
    const jour = new Date().toISOString().slice(0, 10);
    const dossierOriginaux = path.join(ORIGINALS_DIR, egerie.slug, jour);
    const dossierApercus = path.join(PREVIEWS_DIR, egerie.slug);
    await fsp.mkdir(dossierOriginaux, { recursive: true });
    await fsp.mkdir(dossierApercus, { recursive: true });

    const serie = String(req.body.serie || '').slice(0, 80);
    const message = String(req.body.message || '').slice(0, 600);
    const consentement = req.body.consentement === '1' ? 1 : 0;

    let recues = 0;
    let doublons = 0;
    let echecs = 0;

    for (const fichier of fichiers) {
      try {
        const sha = await sha256Fichier(fichier.path);
        const dejaLa = db
          .prepare('SELECT id FROM depots WHERE egerie_id = ? AND sha256 = ?')
          .get(egerie.id, sha);
        if (dejaLa) {
          await fsp.rm(fichier.path, { force: true });
          doublons += 1;
          continue;
        }

        const nom = nomSur(fichier.originalname);
        const destination = await cheminLibre(dossierOriginaux, nom);
        await fsp.rename(fichier.path, destination).catch(async (e) => {
          if (e.code !== 'EXDEV') throw e;
          await fsp.copyFile(fichier.path, destination);
          await fsp.rm(fichier.path, { force: true });
        });
        await fsp.chmod(destination, 0o640).catch(() => {});

        const jeton = crypto.randomUUID();
        const rendu = await fabriquerApercus(destination, {
          egerie: egerie.nom,
          date: new Date().toLocaleDateString('fr-FR'),
        });

        let apercu = null;
        let vignette = null;
        if (rendu.ok) {
          apercu = path.join(egerie.slug, `${jeton}.jpg`);
          vignette = path.join(egerie.slug, `${jeton}-v.jpg`);
          await fsp.writeFile(path.join(PREVIEWS_DIR, apercu), rendu.apercu);
          await fsp.writeFile(path.join(PREVIEWS_DIR, vignette), rendu.vignette);
        } else {
          echecs += 1;
          vignette = path.join(egerie.slug, `${jeton}-v.jpg`);
          apercu = vignette;
          await fsp.writeFile(path.join(PREVIEWS_DIR, vignette), await apercuIndisponible(nom));
        }

        db.prepare(
          `INSERT INTO depots (egerie_id, lot, serie, message, nom_origine, chemin_original,
             apercu, vignette, apercu_ok, mime, octets, largeur, hauteur, sha256, consentement, depose_le)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
        ).run(
          egerie.id,
          lot,
          serie,
          message,
          fichier.originalname.slice(0, 160),
          path.relative(STORAGE_DIR, destination),
          apercu,
          vignette,
          rendu.ok ? 1 : 0,
          fichier.mimetype,
          fichier.size,
          rendu.largeur || null,
          rendu.hauteur || null,
          sha,
          consentement,
          now()
        );
        recues += 1;
      } catch (e) {
        echecs += 1;
        await fsp.rm(fichier.path, { force: true }).catch(() => {});
        console.error('[depot] echec sur', fichier.originalname, e.message);
      }
    }

    journaliser({
      acteur: egerie.nom,
      action: 'depot',
      cible: lot,
      detail: `${recues} reçue(s), ${doublons} doublon(s), ${echecs} échec(s)${serie ? ` — ${serie}` : ''}`,
      ip: ip(req),
    });

    rediriger(res, '/depot', 'depot', { n: recues, d: doublons, e: echecs });
  });
});

/* ---------------------------------------------------------------- Medias */

function peutVoir(req, depot) {
  if (req.session?.role === 'admin') return true;
  return req.session?.role === 'egerie' && req.session.id === depot.egerie_id;
}

function servirApercu(champ) {
  return (req, res) => {
    const depot = qDepot.get(req.params.id);
    if (!depot) return res.status(404).end();
    if (!peutVoir(req, depot)) return res.status(403).end();
    const rel = depot[champ] || depot.vignette;
    if (!rel) return res.status(404).end();
    const chemin = path.join(PREVIEWS_DIR, rel);
    if (!chemin.startsWith(PREVIEWS_DIR) || !fs.existsSync(chemin)) return res.status(404).end();
    res.setHeader('Cache-Control', 'private, max-age=600');
    res.type('image/jpeg');
    fs.createReadStream(chemin).pipe(res);
  };
}

app.get('/media/apercu/:id', servirApercu('apercu'));
app.get('/media/vignette/:id', servirApercu('vignette'));

/* ----------------------------------------------------------------- Admin */

app.get('/direction', (req, res) => {
  if (req.session?.role === 'admin') return res.redirect('/admin');
  const erreur = !ADMIN_PASSWORD
    ? "Aucun mot de passe direction n'est configuré. Renseignez ADMIN_PASSWORD dans le fichier .env, puis relancez."
    : req.query.e
      ? 'Mot de passe incorrect.'
      : null;
  res.send(vues.pageDirection({ erreur }));
});

app.post('/direction', (req, res) => {
  const cle = `direction:${ip(req)}`;
  const jauge = limiter(cle, 8);
  if (!jauge.autorise) {
    return res.status(429).send(
      vues.pageErreur({
        code: 429,
        message: `Trop de tentatives. Réessayez dans ${Math.ceil(jauge.dansSecondes / 60)} minutes.`,
      })
    );
  }
  const fourni = crypto.createHash('sha256').update(String(req.body.motdepasse || '')).digest();
  const attendu = crypto.createHash('sha256').update(ADMIN_PASSWORD).digest();
  if (!ADMIN_PASSWORD || !crypto.timingSafeEqual(fourni, attendu)) {
    journaliser({ acteur: 'direction', action: 'connexion_refusee', ip: ip(req) });
    return res.redirect('/direction?e=1');
  }
  reinitialiserLimite(cle);
  ouvrirSession(res, { role: 'admin', nom: 'Direction' });
  journaliser({ acteur: 'direction', action: 'connexion_admin', ip: ip(req) });
  res.redirect('/admin');
});

app.get('/admin', exigerAdmin, (req, res) => {
  const stats = db
    .prepare(
      `SELECT COUNT(*) AS total,
              COALESCE(SUM(octets), 0) AS poids,
              COALESCE(SUM(statut = 'nouveau'), 0) AS nouveaux
       FROM depots`
    )
    .get();
  stats.egeries = db.prepare('SELECT COUNT(*) AS n FROM egeries WHERE active = 1').get().n;

  const egeries = db
    .prepare(
      `SELECT e.*, (SELECT COUNT(*) FROM depots d WHERE d.egerie_id = e.id) AS nb
       FROM egeries e WHERE e.active = 1 ORDER BY e.nom`
    )
    .all()
    .map((e) => ({ ...e, preavis: echeanceProche(e.contrat_fin_le) }));

  const derniers = db
    .prepare(
      `SELECT d.*, e.nom AS egerie_nom FROM depots d JOIN egeries e ON e.id = d.egerie_id
       ORDER BY d.depose_le DESC LIMIT 12`
    )
    .all();

  res.send(vues.pageAdmin({ stats, egeries, derniers, flash: flash(req) }));
});

// L'article 3 du contrat impose une denonciation ecrite 3 mois avant l'echeance,
// faute de quoi l'autorisation se reconduit tacitement pour 2 ans.
function echeanceProche(fin) {
  if (!fin) return false;
  const reste = new Date(fin).getTime() - Date.now();
  return reste > 0 && reste < 1000 * 60 * 60 * 24 * 100;
}

app.get('/admin/egeries', exigerAdmin, (req, res) => {
  const egeries = db
    .prepare(
      `SELECT e.*, (SELECT COUNT(*) FROM depots d WHERE d.egerie_id = e.id) AS nb
       FROM egeries e ORDER BY e.active DESC, e.nom`
    )
    .all();
  const codeGenere = req.query.code
    ? { code: req.query.code, nom: req.query.nom || '' }
    : null;
  res.send(vues.pageAdminEgeries({ egeries, flash: flash(req), codeGenere }));
});

app.post('/admin/egeries', exigerAdmin, (req, res) => {
  const nom = String(req.body.nom || '').trim();
  if (!nom) return res.redirect('/admin/egeries');
  const { code, id } = creerEgerie({
    nom,
    pays: String(req.body.pays || ''),
    email: String(req.body.email || ''),
  });
  journaliser({ acteur: 'direction', action: 'egerie_creee', cible: id, detail: nom, ip: ip(req) });
  rediriger(res, '/admin/egeries', 'egerie_creee', { code, nom });
});

app.post('/admin/egeries/:id', exigerAdmin, (req, res) => {
  const { contrat_statut = 'en_attente', contrat_signe_le = '', contrat_fin_le = '', pays = '', email = '' } = req.body;
  db.prepare(
    `UPDATE egeries SET contrat_statut = ?, contrat_signe_le = ?, contrat_fin_le = ?, pays = ?, email = ?
     WHERE id = ?`
  ).run(
    ['en_attente', 'signe', 'expire', 'resilie'].includes(contrat_statut) ? contrat_statut : 'en_attente',
    contrat_signe_le || null,
    contrat_fin_le || null,
    String(pays).slice(0, 60),
    String(email).slice(0, 120),
    req.params.id
  );
  journaliser({
    acteur: 'direction',
    action: 'egerie_modifiee',
    cible: req.params.id,
    detail: `autorisation=${contrat_statut}`,
    ip: ip(req),
  });
  rediriger(res, '/admin/egeries', 'egerie_maj');
});

app.post('/admin/egeries/:id/code', exigerAdmin, (req, res) => {
  const egerie = qEgerieParId.get(req.params.id);
  if (!egerie) return res.redirect('/admin/egeries');
  const code = reinitialiserCode(egerie.id);
  journaliser({ acteur: 'direction', action: 'code_regenere', cible: egerie.id, detail: egerie.nom, ip: ip(req) });
  rediriger(res, '/admin/egeries', 'egerie_creee', { code, nom: egerie.nom });
});

app.post('/admin/egeries/:id/actif', exigerAdmin, (req, res) => {
  const egerie = qEgerieParId.get(req.params.id);
  if (!egerie) return res.redirect('/admin/egeries');
  db.prepare('UPDATE egeries SET active = ? WHERE id = ?').run(egerie.active ? 0 : 1, egerie.id);
  journaliser({
    acteur: 'direction',
    action: egerie.active ? 'egerie_suspendue' : 'egerie_reactivee',
    cible: egerie.id,
    detail: egerie.nom,
    ip: ip(req),
  });
  rediriger(res, '/admin/egeries', 'actif_maj');
});

app.get('/admin/depots', exigerAdmin, (req, res) => {
  const filtres = { egerie: req.query.egerie || '', statut: req.query.statut || '' };
  const conditions = [];
  const valeurs = [];
  if (filtres.egerie) {
    conditions.push('d.egerie_id = ?');
    valeurs.push(filtres.egerie);
  }
  if (['nouveau', 'traite', 'archive'].includes(filtres.statut)) {
    conditions.push('d.statut = ?');
    valeurs.push(filtres.statut);
  }
  const depots = db
    .prepare(
      `SELECT d.*, e.nom AS egerie_nom FROM depots d JOIN egeries e ON e.id = d.egerie_id
       ${conditions.length ? `WHERE ${conditions.join(' AND ')}` : ''}
       ORDER BY d.depose_le DESC LIMIT 400`
    )
    .all(...valeurs);
  res.send(
    vues.pageAdminDepots({ depots, egeries: qEgeriesActives.all(), filtres, flash: flash(req) })
  );
});

app.get('/admin/depot/:id', exigerAdmin, (req, res) => {
  const depot = qDepot.get(req.params.id);
  if (!depot) return res.status(404).send(vues.pageErreur({ code: 404, message: 'Dépôt introuvable.' }));
  res.send(vues.pageAdminDepot({ depot, flash: flash(req) }));
});

app.post('/admin/depot/:id/statut', exigerAdmin, (req, res) => {
  const statut = ['nouveau', 'traite', 'archive'].includes(req.body.statut) ? req.body.statut : 'nouveau';
  db.prepare('UPDATE depots SET statut = ? WHERE id = ?').run(statut, req.params.id);
  rediriger(res, `/admin/depot/${req.params.id}`, 'statut_maj');
});

// Le « en cas d'urgence » : la seule porte vers le fichier non flouté.
app.get('/admin/original/:id', exigerAdmin, (req, res) => {
  const depot = qDepot.get(req.params.id);
  if (!depot) return res.status(404).end();
  const chemin = path.resolve(STORAGE_DIR, depot.chemin_original);
  if (!chemin.startsWith(ORIGINALS_DIR) || !fs.existsSync(chemin)) {
    return res.status(410).send(vues.pageErreur({ code: 410, message: "Le fichier d'origine est introuvable dans le coffre." }));
  }
  journaliser({
    acteur: 'direction',
    action: 'telechargement_original',
    cible: depot.id,
    detail: `${depot.egerie_nom} — ${depot.nom_origine}`,
    ip: ip(req),
  });
  res.setHeader('Cache-Control', 'private, no-store');
  res.download(chemin, depot.nom_origine);
});

app.get('/admin/archive/:egerieId', exigerAdmin, (req, res) => {
  const egerie = qEgerieParId.get(req.params.egerieId);
  if (!egerie) return res.status(404).end();
  const depots = db.prepare('SELECT * FROM depots WHERE egerie_id = ?').all(egerie.id);
  if (!depots.length) return res.status(404).send(vues.pageErreur({ code: 404, message: 'Rien à archiver.' }));

  journaliser({
    acteur: 'direction',
    action: 'archive_originaux',
    cible: egerie.id,
    detail: `${depots.length} fichier(s) — ${egerie.nom}`,
    ip: ip(req),
  });

  res.setHeader('Content-Type', 'application/zip');
  res.setHeader(
    'Content-Disposition',
    `attachment; filename="originaux-${egerie.slug}-${new Date().toISOString().slice(0, 10)}.zip"`
  );
  const zip = archiver('zip', { zlib: { level: 0 } }); // photos deja compressees : zip = conteneur, pas compression
  zip.on('error', (e) => {
    console.error('[archive]', e.message);
    res.destroy();
  });
  zip.pipe(res);
  for (const d of depots) {
    const chemin = path.resolve(STORAGE_DIR, d.chemin_original);
    if (chemin.startsWith(ORIGINALS_DIR) && fs.existsSync(chemin)) {
      zip.file(chemin, { name: path.relative(ORIGINALS_DIR, chemin) });
    }
  }
  zip.finalize();
});

app.get('/admin/journal', exigerAdmin, (req, res) => {
  const entrees = db.prepare('SELECT * FROM journal ORDER BY quand DESC LIMIT 400').all();
  res.send(vues.pageAdminJournal({ entrees }));
});

/* ---------------------------------------------------------------- Divers */

app.use((req, res) => {
  res.status(404).send(vues.pageErreur({ code: 404, message: 'Page introuvable.' }));
});

app.use((err, _req, res, _next) => {
  console.error('[erreur]', err);
  res.status(500).send(vues.pageErreur({ code: 500, message: 'Une erreur est survenue.' }));
});

// Les fragments d'un envoi interrompu ne doivent pas s'accumuler dans le coffre.
function nettoyerTmp() {
  const limite = Date.now() - 6 * 60 * 60 * 1000;
  for (const f of fs.readdirSync(TMP_DIR)) {
    const p = path.join(TMP_DIR, f);
    try {
      if (fs.statSync(p).mtimeMs < limite) fs.rmSync(p, { force: true });
    } catch { /* fichier deja parti */ }
  }
}

if (process.env.NODE_TEST !== '1') {
  nettoyerTmp();
  setInterval(nettoyerTmp, 60 * 60 * 1000).unref();

  app.listen(PORT, () => {
    console.log(`\n  ${BRAND} — studio de dépôt`);
    console.log(`  http://localhost:${PORT}   (${NODE_ENV})`);
    console.log(`  Coffre : ${STORAGE_DIR}`);
    if (!ADMIN_PASSWORD) console.log('  ⚠  ADMIN_PASSWORD non défini : l\'espace direction est inaccessible.');
    console.log('');
  });
}

export default app;
