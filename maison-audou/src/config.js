import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(HERE, '..');

dotenv.config({ path: path.join(ROOT, '.env') });

function bool(v, def) {
  if (v === undefined || v === '') return def;
  return ['1', 'true', 'oui', 'yes'].includes(String(v).toLowerCase());
}

// Emplacement du coffre. Tout ce qui compte vit ici : c'est le seul dossier
// a sauvegarder / synchroniser.
export const STORAGE_DIR = path.resolve(
  ROOT,
  process.env.STORAGE_DIR || 'coffre'
);

export const ORIGINALS_DIR = path.join(STORAGE_DIR, 'originaux');
export const PREVIEWS_DIR = path.join(STORAGE_DIR, 'apercus');
export const CONTRACTS_DIR = path.join(STORAGE_DIR, 'contrats');
export const TMP_DIR = path.join(STORAGE_DIR, '.tmp');
export const DB_PATH = path.join(STORAGE_DIR, 'maison-audou.db');

for (const dir of [STORAGE_DIR, ORIGINALS_DIR, PREVIEWS_DIR, CONTRACTS_DIR, TMP_DIR]) {
  fs.mkdirSync(dir, { recursive: true });
}

export const PORT = Number(process.env.PORT || 3000);
export const NODE_ENV = process.env.NODE_ENV || 'development';
export const BRAND = process.env.BRAND || 'Maison Audou';

// Force du flou applique aux apercus. 0 = pas de flou (deconseille),
// 18 = lisible mais inexploitable, 30 = tres opaque.
export const BLUR_SIGMA = Number(process.env.BLUR_SIGMA || 20);
export const PREVIEW_MAX = Number(process.env.PREVIEW_MAX || 1400);
export const THUMB_MAX = Number(process.env.THUMB_MAX || 520);
export const MAX_FILE_MB = Number(process.env.MAX_FILE_MB || 80);
export const MAX_FILES_PER_UPLOAD = Number(process.env.MAX_FILES_PER_UPLOAD || 40);

export const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '';
export const SECURE_COOKIES = bool(process.env.SECURE_COOKIES, NODE_ENV === 'production');

// Un secret volatile invaliderait les sessions a chaque redemarrage : on le
// persiste dans le coffre s'il n'est pas fourni.
export const SESSION_SECRET = (() => {
  if (process.env.SESSION_SECRET) return process.env.SESSION_SECRET;
  const file = path.join(STORAGE_DIR, '.session-secret');
  if (!fs.existsSync(file)) {
    fs.writeFileSync(file, crypto.randomBytes(32).toString('hex'), { mode: 0o600 });
  }
  return fs.readFileSync(file, 'utf8').trim();
})();

export const IMAGE_MIME = new Set([
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/tiff',
  'image/heic',
  'image/heif',
  'image/avif',
  'image/gif',
]);
