import sharp from 'sharp';
import { BLUR_SIGMA, PREVIEW_MAX, THUMB_MAX, BRAND } from './config.js';

sharp.cache(false);

function echapper(texte) {
  return String(texte).replace(/[<>&'"]/g, (c) => (
    { '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]
  ));
}

// Filigrane pose PAR-DESSUS le flou : il doit rester lisible sur une capture
// d'ecran, c'est lui qui rend l'apercu tracable.
function filigraneSvg(largeur, hauteur, ligne1, ligne2) {
  const pas = Math.max(190, Math.round(Math.min(largeur, hauteur) / 3.2));
  const taille = Math.max(13, Math.round(pas / 13));
  const textes = [];
  for (let y = -hauteur; y < hauteur * 2; y += pas) {
    for (let x = -largeur; x < largeur * 2; x += pas * 2) {
      textes.push(
        `<text x="${x}" y="${y}" font-family="Helvetica, Arial, sans-serif" font-size="${taille}" ` +
        `fill="#ffffff" fill-opacity="0.42" letter-spacing="${(taille / 5).toFixed(1)}">${echapper(ligne1)}</text>` +
        `<text x="${x}" y="${y + taille * 1.35}" font-family="Helvetica, Arial, sans-serif" font-size="${taille * 0.8}" ` +
        `fill="#ffffff" fill-opacity="0.34" letter-spacing="${(taille / 8).toFixed(1)}">${echapper(ligne2)}</text>`
      );
    }
  }
  return Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${largeur}" height="${hauteur}">` +
      `<g transform="rotate(-30 ${largeur / 2} ${hauteur / 2})">${textes.join('')}</g>` +
    `</svg>`
  );
}

async function rendre(source, taille, sigma, ligne1, ligne2) {
  // rotate() sans argument applique l'orientation EXIF : sans lui les photos
  // prises au telephone ressortent couchees.
  const base = sharp(source, { failOn: 'none' })
    .rotate()
    .resize({ width: taille, height: taille, fit: 'inside', withoutEnlargement: true });

  const { data, info } = await base.blur(sigma).toBuffer({ resolveWithObject: true });

  return sharp(data)
    .composite([{ input: filigraneSvg(info.width, info.height, ligne1, ligne2), top: 0, left: 0 }])
    .jpeg({ quality: 72, chromaSubsampling: '4:2:0' }) // sans .withMetadata() : l'EXIF (GPS inclus) ne sort pas
    .toBuffer();
}

/**
 * Fabrique les deux apercus floutes d'une image.
 * Retourne { ok, largeur, hauteur, apercu, vignette } ; ok = false si le
 * format n'a pas pu etre decode (HEIC sans libheif, RAW, fichier abime).
 * Dans ce cas l'original reste intact dans le coffre : rien n'est perdu.
 */
export async function fabriquerApercus(cheminOriginal, { egerie, date }) {
  const ligne1 = `${BRAND.toUpperCase()} - CONFIDENTIEL`;
  const ligne2 = `${egerie} - ${date}`;
  try {
    const meta = await sharp(cheminOriginal, { failOn: 'none' }).metadata();
    const pivote = (meta.orientation || 0) >= 5;
    const [apercu, vignette] = await Promise.all([
      rendre(cheminOriginal, PREVIEW_MAX, BLUR_SIGMA, ligne1, ligne2),
      rendre(cheminOriginal, THUMB_MAX, Math.max(6, BLUR_SIGMA / 2), ligne1, ligne2),
    ]);
    return {
      ok: true,
      largeur: pivote ? meta.height : meta.width,
      hauteur: pivote ? meta.width : meta.height,
      apercu,
      vignette,
    };
  } catch (err) {
    return { ok: false, erreur: err.message };
  }
}

/** Carte grise affichee quand l'apercu n'a pas pu etre genere. */
export function apercuIndisponible(nomFichier) {
  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" width="${THUMB_MAX}" height="${Math.round(THUMB_MAX * 0.72)}">` +
    `<rect width="100%" height="100%" fill="#2a2724"/>` +
    `<text x="50%" y="46%" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="20" fill="#c9bfb2">Original conserve</text>` +
    `<text x="50%" y="58%" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#8b8175">apercu impossible - ${echapper(nomFichier).slice(0, 42)}</text>` +
    `</svg>`;
  return sharp(Buffer.from(svg)).jpeg({ quality: 80 }).toBuffer();
}
