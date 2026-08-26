#!/usr/bin/env node
// Vérification de bout en bout, sur un coffre jetable.
// Le point qui compte : ce que sert la plateforme est bien flouté, et ce
// qu'elle garde sur disque est bien l'original intact.
//
//   npm run verif

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const coffre = fs.mkdtempSync(path.join(os.tmpdir(), 'ma-verif-'));
process.env.STORAGE_DIR = coffre;
process.env.ADMIN_PASSWORD = 'secret-de-verification';
process.env.NODE_TEST = '1';
process.env.SESSION_SECRET = 'verif';
process.env.BLUR_SIGMA = '20';

const sharp = (await import('sharp')).default;
const { default: app } = await import('../src/server.js');
const { creerEgerie, db } = await import('../src/db.js');

const serveur = app.listen(0);
await new Promise((r) => serveur.once('listening', r));
const base = `http://127.0.0.1:${serveur.address().port}`;

let reussis = 0;
const ok = (nom) => {
  reussis += 1;
  console.log(`  ✓ ${nom}`);
};

function cookiesDe(reponse) {
  return reponse.headers
    .getSetCookie()
    .map((c) => c.split(';')[0])
    .join('; ');
}

/* --- Image source : damier très contrasté, idéal pour mesurer le flou --- */
const CARREAU = 16;
const COTE = 512;
const pixels = Buffer.alloc(COTE * COTE * 3);
for (let y = 0; y < COTE; y += 1) {
  for (let x = 0; x < COTE; x += 1) {
    const v = (Math.floor(x / CARREAU) + Math.floor(y / CARREAU)) % 2 ? 255 : 0;
    const i = (y * COTE + x) * 3;
    pixels[i] = pixels[i + 1] = pixels[i + 2] = v;
  }
}
const original = await sharp(pixels, { raw: { width: COTE, height: COTE, channels: 3 } })
  .jpeg({ quality: 100 })
  .toBuffer();
const shaOriginal = crypto.createHash('sha256').update(original).digest('hex');

/** Contraste local moyen : élevé sur une image nette, effondré sur un flou. */
async function nettete(buffer) {
  const { data, info } = await sharp(buffer).greyscale().raw().toBuffer({ resolveWithObject: true });
  let somme = 0;
  let n = 0;
  for (let y = 0; y < info.height; y += 1) {
    for (let x = 1; x < info.width; x += 1) {
      somme += Math.abs(data[y * info.width + x] - data[y * info.width + x - 1]);
      n += 1;
    }
  }
  return somme / n;
}

try {
  console.log(`\n  Coffre de test : ${coffre}\n`);

  /* 1. Accès égérie */
  const { code } = creerEgerie({ nom: 'Test Égérie', pays: 'Test' });
  const connexion = await fetch(`${base}/acces`, {
    method: 'POST',
    redirect: 'manual',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ slug: 'test-egerie', code }),
  });
  assert.equal(connexion.headers.get('location'), '/depot', 'la connexion doit mener au dépôt');
  const cookieEgerie = cookiesDe(connexion);
  ok("connexion d'une égérie avec son code");

  const refus = await fetch(`${base}/acces`, {
    method: 'POST',
    redirect: 'manual',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ slug: 'test-egerie', code: 'AAAA-AAAA' }),
  });
  assert.match(refus.headers.get('location'), /^\/acces\?e=1/, 'un mauvais code doit être refusé');
  ok('un code erroné est refusé');

  /* 2. Dépôt */
  const formulaire = new FormData();
  formulaire.append('photos', new Blob([original], { type: 'image/jpeg' }), 'Shooting Bali.jpg');
  formulaire.append('serie', 'Campagne test');
  formulaire.append('consentement', '1');
  const envoi = await fetch(`${base}/depot/envoi`, {
    method: 'POST',
    redirect: 'manual',
    headers: { cookie: cookieEgerie },
    body: formulaire,
  });
  assert.match(envoi.headers.get('location'), /n=1/, 'une photo doit être enregistrée');
  ok('dépôt accepté');

  const depot = db.prepare('SELECT * FROM depots ORDER BY id DESC LIMIT 1').get();
  assert.ok(depot, 'le dépôt doit être en base');
  assert.equal(depot.consentement, 1, 'le consentement doit être tracé');

  /* 3. L'original est intact dans le dossier */
  const cheminOriginal = path.join(coffre, depot.chemin_original);
  assert.ok(fs.existsSync(cheminOriginal), "l'original doit exister sur disque");
  const surDisque = fs.readFileSync(cheminOriginal);
  assert.equal(
    crypto.createHash('sha256').update(surDisque).digest('hex'),
    shaOriginal,
    "l'original doit être conservé octet pour octet"
  );
  assert.match(depot.chemin_original, /^originaux[\\/]test-egerie[\\/]\d{4}-\d{2}-\d{2}[\\/]/);
  ok(`original intact dans ${path.dirname(depot.chemin_original)}`);

  /* 4. Ce qui est servi est flouté */
  const rApercu = await fetch(`${base}/media/apercu/${depot.id}`, { headers: { cookie: cookieEgerie } });
  assert.equal(rApercu.status, 200);
  const apercu = Buffer.from(await rApercu.arrayBuffer());
  assert.notEqual(
    crypto.createHash('sha256').update(apercu).digest('hex'),
    shaOriginal,
    "l'aperçu ne doit jamais être l'original"
  );

  const netteteOriginal = await nettete(original);
  const netteteApercu = await nettete(apercu);
  assert.ok(
    netteteApercu < netteteOriginal / 8,
    `l'aperçu doit être franchement flouté (net ${netteteOriginal.toFixed(1)} → ${netteteApercu.toFixed(1)})`
  );
  ok(`aperçu flouté : contraste local ${netteteOriginal.toFixed(1)} → ${netteteApercu.toFixed(1)}`);

  /* 5. Cloisonnement */
  const anonyme = await fetch(`${base}/media/apercu/${depot.id}`, { redirect: 'manual' });
  assert.equal(anonyme.status, 403, 'un visiteur non connecté ne voit rien');
  const originalAnonyme = await fetch(`${base}/admin/original/${depot.id}`, { redirect: 'manual' });
  assert.equal(originalAnonyme.status, 302, "l'original est réservé à la direction");
  const adminAnonyme = await fetch(`${base}/admin`, { redirect: 'manual' });
  assert.equal(adminAnonyme.headers.get('location'), '/direction');
  ok('aperçus et originaux inaccessibles sans session');

  /* 6. La direction récupère l'original */
  const direction = await fetch(`${base}/direction`, {
    method: 'POST',
    redirect: 'manual',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ motdepasse: 'secret-de-verification' }),
  });
  assert.equal(direction.headers.get('location'), '/admin');
  const cookieAdmin = cookiesDe(direction);

  const recup = await fetch(`${base}/admin/original/${depot.id}`, { headers: { cookie: cookieAdmin } });
  assert.equal(recup.status, 200);
  const recupere = Buffer.from(await recup.arrayBuffer());
  assert.equal(
    crypto.createHash('sha256').update(recupere).digest('hex'),
    shaOriginal,
    "la direction doit récupérer l'original exact"
  );
  assert.match(recup.headers.get('content-disposition') || '', /Shooting Bali\.jpg/);
  ok("la direction retélécharge l'original à l'identique");

  /* 7. Journal */
  const trace = db.prepare("SELECT * FROM journal WHERE action = 'telechargement_original'").get();
  assert.ok(trace, "l'accès à un original doit être journalisé");
  ok('accès à un original journalisé');

  /* 8. Doublon */
  const bis = new FormData();
  bis.append('photos', new Blob([original], { type: 'image/jpeg' }), 'copie.jpg');
  bis.append('consentement', '1');
  const renvoi = await fetch(`${base}/depot/envoi`, {
    method: 'POST',
    redirect: 'manual',
    headers: { cookie: cookieEgerie },
    body: bis,
  });
  assert.match(renvoi.headers.get('location'), /n=0&d=1/, 'un doublon doit être ignoré');
  ok('doublon détecté et ignoré');

  /* 9. Archive ZIP */
  const zip = await fetch(`${base}/admin/archive/${depot.egerie_id}`, { headers: { cookie: cookieAdmin } });
  assert.equal(zip.status, 200);
  const contenu = Buffer.from(await zip.arrayBuffer());
  assert.equal(contenu.subarray(0, 2).toString(), 'PK', 'un ZIP doit être renvoyé');
  ok('archive ZIP des originaux téléchargeable');

  console.log(`\n  ${reussis} vérifications passées.\n`);
} catch (err) {
  console.error(`\n  ✗ ${err.message}\n`);
  process.exitCode = 1;
} finally {
  serveur.close();
  db.close();
  fs.rmSync(coffre, { recursive: true, force: true });
}
