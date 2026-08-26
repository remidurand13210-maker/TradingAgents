import crypto from 'node:crypto';
import { SESSION_SECRET, SECURE_COOKIES } from './config.js';

const COOKIE = 'ma_session';
const DUREE_MS = 1000 * 60 * 60 * 12; // 12 h

function signer(charge) {
  const donnees = Buffer.from(JSON.stringify(charge)).toString('base64url');
  const sig = crypto.createHmac('sha256', SESSION_SECRET).update(donnees).digest('base64url');
  return `${donnees}.${sig}`;
}

function verifier(jeton) {
  if (!jeton || typeof jeton !== 'string') return null;
  const [donnees, sig] = jeton.split('.');
  if (!donnees || !sig) return null;
  const attendu = crypto.createHmac('sha256', SESSION_SECRET).update(donnees).digest('base64url');
  const a = Buffer.from(sig);
  const b = Buffer.from(attendu);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  try {
    const charge = JSON.parse(Buffer.from(donnees, 'base64url').toString('utf8'));
    if (!charge.exp || charge.exp < Date.now()) return null;
    return charge;
  } catch {
    return null;
  }
}

export function ouvrirSession(res, charge) {
  res.cookie(COOKIE, signer({ ...charge, exp: Date.now() + DUREE_MS }), {
    httpOnly: true,
    sameSite: 'lax',
    secure: SECURE_COOKIES,
    maxAge: DUREE_MS,
  });
}

export function fermerSession(res) {
  res.clearCookie(COOKIE, { httpOnly: true, sameSite: 'lax', secure: SECURE_COOKIES });
}

export function chargerSession(req, _res, next) {
  req.session = verifier(req.cookies?.[COOKIE]) || null;
  next();
}

export function exigerEgerie(req, res, next) {
  if (req.session?.role === 'egerie') return next();
  return res.redirect('/acces');
}

export function exigerAdmin(req, res, next) {
  if (req.session?.role === 'admin') return next();
  return res.redirect('/direction');
}

// Anti-force brute simple, en memoire : suffisant pour un outil a cinq
// utilisateurs, et sans dependance supplementaire.
const tentatives = new Map();

export function limiter(cle, max = 8, fenetreMs = 10 * 60 * 1000) {
  const maintenant = Date.now();
  const entree = tentatives.get(cle);
  if (!entree || maintenant > entree.reset) {
    tentatives.set(cle, { n: 1, reset: maintenant + fenetreMs });
    return { autorise: true, restant: max - 1 };
  }
  entree.n += 1;
  if (entree.n > max) {
    return { autorise: false, restant: 0, dansSecondes: Math.ceil((entree.reset - maintenant) / 1000) };
  }
  return { autorise: true, restant: max - entree.n };
}

export function reinitialiserLimite(cle) {
  tentatives.delete(cle);
}
