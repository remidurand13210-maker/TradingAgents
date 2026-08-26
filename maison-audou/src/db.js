import Database from 'better-sqlite3';
import crypto from 'node:crypto';
import { DB_PATH } from './config.js';

export const db = new Database(DB_PATH);
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

db.exec(`
CREATE TABLE IF NOT EXISTS egeries (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  nom               TEXT NOT NULL,
  slug              TEXT NOT NULL UNIQUE,
  pays              TEXT DEFAULT '',
  email             TEXT DEFAULT '',
  code_hash         TEXT NOT NULL,
  code_indice       TEXT NOT NULL DEFAULT '',
  active            INTEGER NOT NULL DEFAULT 1,
  contrat_statut    TEXT NOT NULL DEFAULT 'en_attente',
  contrat_signe_le  TEXT,
  contrat_fin_le    TEXT,
  contrat_fichier   TEXT,
  notes             TEXT DEFAULT '',
  cree_le           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS depots (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  egerie_id         INTEGER NOT NULL REFERENCES egeries(id) ON DELETE CASCADE,
  lot               TEXT NOT NULL,
  serie             TEXT DEFAULT '',
  message           TEXT DEFAULT '',
  nom_origine       TEXT NOT NULL,
  chemin_original   TEXT NOT NULL,
  apercu            TEXT,
  vignette          TEXT,
  apercu_ok         INTEGER NOT NULL DEFAULT 0,
  mime              TEXT DEFAULT '',
  octets            INTEGER NOT NULL DEFAULT 0,
  largeur           INTEGER,
  hauteur           INTEGER,
  sha256            TEXT NOT NULL,
  statut            TEXT NOT NULL DEFAULT 'nouveau',
  consentement      INTEGER NOT NULL DEFAULT 0,
  depose_le         TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_depots_egerie ON depots(egerie_id, depose_le DESC);
CREATE INDEX IF NOT EXISTS idx_depots_sha ON depots(egerie_id, sha256);

CREATE TABLE IF NOT EXISTS journal (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  quand     TEXT NOT NULL,
  acteur    TEXT NOT NULL,
  action    TEXT NOT NULL,
  cible     TEXT DEFAULT '',
  detail    TEXT DEFAULT '',
  ip        TEXT DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_journal_quand ON journal(quand DESC);
`);

export function now() {
  return new Date().toISOString();
}

export function hashCode(code) {
  return crypto.createHash('sha256').update(String(code).trim().toUpperCase()).digest('hex');
}

// Alphabet sans caracteres ambigus (0/O, 1/I/L) : les codes circulent par
// message vocal ou WhatsApp entre quatre fuseaux horaires.
const ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';

export function genererCode(longueur = 8) {
  const octets = crypto.randomBytes(longueur);
  let out = '';
  for (let i = 0; i < longueur; i += 1) out += ALPHABET[octets[i] % ALPHABET.length];
  return `${out.slice(0, 4)}-${out.slice(4)}`;
}

export function slugifier(texte) {
  return String(texte)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48) || 'egerie';
}

export function journaliser({ acteur, action, cible = '', detail = '', ip = '' }) {
  db.prepare(
    'INSERT INTO journal (quand, acteur, action, cible, detail, ip) VALUES (?, ?, ?, ?, ?, ?)'
  ).run(now(), acteur, action, String(cible), detail, ip);
}

export function creerEgerie({ nom, pays = '', email = '', contratStatut = 'en_attente' }) {
  const base = slugifier(nom);
  let slug = base;
  let n = 2;
  while (db.prepare('SELECT 1 FROM egeries WHERE slug = ?').get(slug)) {
    slug = `${base}-${n}`;
    n += 1;
  }
  const code = genererCode();
  const info = db
    .prepare(
      `INSERT INTO egeries (nom, slug, pays, email, code_hash, code_indice, contrat_statut, cree_le)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .run(nom.trim(), slug, pays.trim(), email.trim(), hashCode(code), code.slice(-3), contratStatut, now());
  return { id: info.lastInsertRowid, slug, code };
}

export function reinitialiserCode(egerieId) {
  const code = genererCode();
  db.prepare('UPDATE egeries SET code_hash = ?, code_indice = ? WHERE id = ?').run(
    hashCode(code),
    code.slice(-3),
    egerieId
  );
  return code;
}
