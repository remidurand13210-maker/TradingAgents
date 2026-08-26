import { BRAND, BLUR_SIGMA, MAX_FILE_MB, MAX_FILES_PER_UPLOAD } from './config.js';

export function esc(v) {
  if (v === null || v === undefined) return '';
  return String(v).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

export function octets(n) {
  if (!n) return '0 o';
  const u = ['o', 'Ko', 'Mo', 'Go'];
  const i = Math.min(u.length - 1, Math.floor(Math.log(n) / Math.log(1024)));
  return `${(n / 1024 ** i).toFixed(i === 0 ? 0 : 1)} ${u[i]}`;
}

export function dateFr(iso, avecHeure = false) {
  if (!iso) return '—';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return esc(iso);
  const date = d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
  if (!avecHeure) return date;
  return `${date} à ${d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`;
}

const STATUTS_CONTRAT = {
  signe: ['Autorisation signée', 'ok'],
  en_attente: ['Autorisation en attente', 'attente'],
  expire: ['Autorisation expirée', 'alerte'],
  resilie: ['Autorisation résiliée', 'alerte'],
};

export function badgeContrat(statut) {
  const [libelle, ton] = STATUTS_CONTRAT[statut] || STATUTS_CONTRAT.en_attente;
  return `<span class="badge ${ton}">${libelle}</span>`;
}

const STATUTS_DEPOT = {
  nouveau: ['Nouveau', 'accent'],
  traite: ['Traité', 'ok'],
  archive: ['Archivé', 'neutre'],
};

export function badgeDepot(statut) {
  const [libelle, ton] = STATUTS_DEPOT[statut] || STATUTS_DEPOT.nouveau;
  return `<span class="badge ${ton}">${libelle}</span>`;
}

export function layout({ titre, corps, nav = '', classe = '' }) {
  return `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="referrer" content="no-referrer">
<title>${esc(titre)} · ${esc(BRAND)}</title>
<link rel="stylesheet" href="/statique/styles.css">
</head>
<body class="${classe}">
<header class="entete">
  <a class="marque" href="/">${esc(BRAND)}</a>
  <nav>${nav}</nav>
</header>
<main>${corps}</main>
<footer class="pied">
  <p>Espace privé — les aperçus affichés ici sont volontairement floutés et filigranés. Les fichiers d'origine ne quittent jamais le coffre.</p>
</footer>
</body>
</html>`;
}

export function alerte(flash) {
  if (!flash) return '';
  const { type = 'info', texte } = flash;
  return `<p class="flash ${esc(type)}">${esc(texte)}</p>`;
}

/* ---------------------------------------------------------------- Public */

export function pageAccueil() {
  return layout({
    titre: 'Accueil',
    classe: 'centre',
    corps: `
<section class="carte hero">
  <p class="surtitre">Dépôt de visuels</p>
  <h1>Studio ${esc(BRAND)}</h1>
  <p class="chapeau">Un espace privé où nos égéries déposent leurs prises de vue. Les images
  s'affichent floutées et filigranées : même en cas d'accès non autorisé à l'outil,
  rien n'est exploitable. Les originaux, eux, sont conservés intacts hors ligne.</p>
  <div class="actions">
    <a class="bouton" href="/acces">Je suis une égérie</a>
    <a class="bouton fantome" href="/direction">Direction</a>
  </div>
</section>`,
  });
}

export function pageAccesEgerie({ egeries, erreur, slugChoisi }) {
  const options = egeries
    .map(
      (e) =>
        `<option value="${esc(e.slug)}" ${e.slug === slugChoisi ? 'selected' : ''}>${esc(e.nom)}${
          e.pays ? ` — ${esc(e.pays)}` : ''
        }</option>`
    )
    .join('');
  return layout({
    titre: 'Accès égérie',
    classe: 'centre',
    corps: `
<section class="carte etroite">
  <p class="surtitre">Espace égérie</p>
  <h1>Entrer dans le studio</h1>
  ${erreur ? `<p class="flash erreur">${esc(erreur)}</p>` : ''}
  ${
    egeries.length === 0
      ? `<p class="chapeau">Aucune égérie n'est encore enregistrée. La direction doit créer les accès.</p>`
      : `<form method="post" action="/acces" class="formulaire">
    <label>Votre nom
      <select name="slug" required>${options}</select>
    </label>
    <label>Votre code d'accès
      <input name="code" required autocomplete="one-time-code" autocapitalize="characters"
             spellcheck="false" placeholder="XXXX-XXXX" inputmode="text">
    </label>
    <button class="bouton" type="submit">Entrer</button>
  </form>
  <p class="note">Code perdu ? Demandez-en un nouveau à la direction : un code ne peut pas être retrouvé, seulement remplacé.</p>`
  }
</section>`,
  });
}

export function pageDepot({ egerie, depots, flash, totalOctets }) {
  const grille = depots.length
    ? `<div class="grille">${depots.map((d) => carteDepot(d, `/media/vignette/${d.id}`)).join('')}</div>`
    : `<p class="vide">Aucun dépôt pour l'instant. Vos photos apparaîtront ici, floutées.</p>`;

  const contratBloquant = egerie.contrat_statut !== 'signe';

  return layout({
    titre: `Studio — ${egerie.nom}`,
    nav: `<span class="qui">${esc(egerie.nom)}</span> <a href="/deconnexion">Quitter</a>`,
    corps: `
<section class="bandeau">
  <div>
    <p class="surtitre">Espace égérie</p>
    <h1>Bonjour ${esc(egerie.nom.split(' ')[0])}</h1>
    <p class="chapeau">Déposez ici vos prises de vue. Elles partent directement chez ${esc(BRAND)}
    en qualité d'origine ; ce que vous voyez à l'écran reste flouté.</p>
  </div>
  <div class="compteurs">
    <div><strong>${depots.length}</strong><span>photo${depots.length > 1 ? 's' : ''} déposée${depots.length > 1 ? 's' : ''}</span></div>
    <div><strong>${octets(totalOctets)}</strong><span>transmis</span></div>
  </div>
</section>

${alerte(flash)}

${
  contratBloquant
    ? `<p class="flash attention">Votre autorisation de droit à l'image n'est pas encore enregistrée comme signée.
       Vous pouvez déposer vos photos : elles seront conservées mais mises en attente d'exploitation jusqu'à réception du document signé.</p>`
    : ''
}

<section class="carte">
  <h2>Nouveau dépôt</h2>
  <form method="post" action="/depot/envoi" enctype="multipart/form-data" class="formulaire" id="formulaire-depot">
    <div class="zone-depot" id="zone-depot">
      <input type="file" name="photos" id="photos" multiple accept="image/*" required>
      <p><strong>Glissez vos photos ici</strong> ou touchez pour les choisir</p>
      <p class="note">JPEG, PNG, HEIC, WebP, TIFF — jusqu'à ${MAX_FILE_MB} Mo par fichier,
      ${MAX_FILES_PER_UPLOAD} fichiers par envoi.</p>
      <ul class="liste-fichiers" id="liste-fichiers"></ul>
    </div>
    <label>Série / shooting <span class="facultatif">(facultatif)</span>
      <input name="serie" maxlength="80" placeholder="Ex. Campagne été — Bali">
    </label>
    <label>Message pour la direction <span class="facultatif">(facultatif)</span>
      <textarea name="message" rows="3" maxlength="600" placeholder="Contexte, consignes, préférences…"></textarea>
    </label>
    <label class="case">
      <input type="checkbox" name="consentement" value="1" required>
      <span>Je confirme que ces images me représentent et sont couvertes par l'autorisation
      de droit à l'image que j'ai signée avec ${esc(BRAND)}.</span>
    </label>
    <button class="bouton" type="submit" id="bouton-envoi">Envoyer au studio</button>
    <p class="note" id="etat-envoi" hidden>Envoi en cours, gardez cette page ouverte…</p>
  </form>
</section>

<section>
  <h2>Vos dépôts</h2>
  ${grille}
</section>
<script src="/statique/depot.js" defer></script>`,
  });
}

function carteDepot(d, srcVignette, lien = null) {
  const image = `<img src="${srcVignette}" alt="Aperçu flouté de ${esc(d.nom_origine)}" loading="lazy">`;
  const contenu = `
  <figure class="carte-photo">
    <div class="cadre">${image}<span class="sceau">flouté</span></div>
    <figcaption>
      <strong>${esc(d.nom_origine)}</strong>
      <span>${dateFr(d.depose_le, true)} · ${octets(d.octets)}</span>
      ${d.serie ? `<span class="serie">${esc(d.serie)}</span>` : ''}
      ${d.egerie_nom ? `<span class="serie">${esc(d.egerie_nom)}</span>` : ''}
    </figcaption>
  </figure>`;
  return lien ? `<a class="lien-photo" href="${lien}">${contenu}</a>` : contenu;
}

/* ----------------------------------------------------------------- Admin */

export function pageDirection({ erreur }) {
  return layout({
    titre: 'Direction',
    classe: 'centre',
    corps: `
<section class="carte etroite">
  <p class="surtitre">Réservé</p>
  <h1>Direction ${esc(BRAND)}</h1>
  ${erreur ? `<p class="flash erreur">${esc(erreur)}</p>` : ''}
  <form method="post" action="/direction" class="formulaire">
    <label>Mot de passe
      <input type="password" name="motdepasse" required autocomplete="current-password">
    </label>
    <button class="bouton" type="submit">Entrer</button>
  </form>
</section>`,
  });
}

const NAV_ADMIN = `
  <a href="/admin">Tableau de bord</a>
  <a href="/admin/depots">Dépôts</a>
  <a href="/admin/egeries">Égéries</a>
  <a href="/admin/journal">Journal</a>
  <a href="/deconnexion">Quitter</a>`;

export function pageAdmin({ stats, egeries, derniers, flash }) {
  return layout({
    titre: 'Tableau de bord',
    nav: NAV_ADMIN,
    corps: `
<section class="bandeau">
  <div>
    <p class="surtitre">Direction</p>
    <h1>Tableau de bord</h1>
    <p class="chapeau">Aperçus floutés à l'écran, originaux intacts dans le coffre.</p>
  </div>
  <div class="compteurs">
    <div><strong>${stats.nouveaux}</strong><span>à traiter</span></div>
    <div><strong>${stats.total}</strong><span>photos au coffre</span></div>
    <div><strong>${octets(stats.poids)}</strong><span>volume</span></div>
    <div><strong>${stats.egeries}</strong><span>égéries actives</span></div>
  </div>
</section>

${alerte(flash)}

<section>
  <h2>Égéries</h2>
  <div class="cartes-egeries">
    ${
      egeries.length
        ? egeries
            .map(
              (e) => `
      <article class="carte mini">
        <h3>${esc(e.nom)}</h3>
        <p class="note">${esc(e.pays || 'Pays non renseigné')}</p>
        ${badgeContrat(e.contrat_statut)}
        ${e.contrat_fin_le ? `<p class="note">Jusqu'au ${dateFr(e.contrat_fin_le)}${e.preavis ? ' · <b>préavis à poser</b>' : ''}</p>` : ''}
        <p class="chiffre">${e.nb} photo${e.nb > 1 ? 's' : ''}</p>
        <a class="bouton fin" href="/admin/depots?egerie=${e.id}">Voir ses dépôts</a>
      </article>`
            )
            .join('')
        : `<p class="vide">Aucune égérie. <a href="/admin/egeries">Créer le premier accès</a>.</p>`
    }
  </div>
</section>

<section>
  <h2>Derniers dépôts</h2>
  ${
    derniers.length
      ? `<div class="grille">${derniers
          .map((d) => carteDepot(d, `/media/vignette/${d.id}`, `/admin/depot/${d.id}`))
          .join('')}</div>`
      : `<p class="vide">Rien n'a encore été déposé.</p>`
  }
</section>`,
  });
}

export function pageAdminEgeries({ egeries, flash, codeGenere }) {
  const lignes = egeries
    .map(
      (e) => `
  <tr>
    <td><strong>${esc(e.nom)}</strong><br><span class="note">${esc(e.slug)}</span></td>
    <td>${esc(e.pays || '—')}<br><span class="note">${esc(e.email || '')}</span></td>
    <td>${badgeContrat(e.contrat_statut)}<br><span class="note">${
      e.contrat_signe_le ? `signé le ${dateFr(e.contrat_signe_le)}` : 'non signé'
    }${e.contrat_fin_le ? ` · fin ${dateFr(e.contrat_fin_le)}` : ''}</span></td>
    <td>${e.nb}</td>
    <td>${e.active ? 'Actif' : 'Suspendu'}<br><span class="note">code …${esc(e.code_indice)}</span></td>
    <td class="actions-cellule">
      <form method="post" action="/admin/egeries/${e.id}/code"><button class="bouton fin">Nouveau code</button></form>
      <form method="post" action="/admin/egeries/${e.id}/actif"><button class="bouton fin fantome">${
        e.active ? 'Suspendre' : 'Réactiver'
      }</button></form>
    </td>
  </tr>
  <tr class="ligne-detail">
    <td colspan="6">
      <form method="post" action="/admin/egeries/${e.id}" class="ligne-formulaire">
        <label>Statut de l'autorisation
          <select name="contrat_statut">
            ${['en_attente', 'signe', 'expire', 'resilie']
              .map(
                (s) =>
                  `<option value="${s}" ${e.contrat_statut === s ? 'selected' : ''}>${
                    STATUTS_CONTRAT[s][0]
                  }</option>`
              )
              .join('')}
          </select>
        </label>
        <label>Signée le <input type="date" name="contrat_signe_le" value="${esc(
          (e.contrat_signe_le || '').slice(0, 10)
        )}"></label>
        <label>Échéance <input type="date" name="contrat_fin_le" value="${esc(
          (e.contrat_fin_le || '').slice(0, 10)
        )}"></label>
        <label>Pays <input name="pays" value="${esc(e.pays || '')}"></label>
        <label>E-mail <input name="email" value="${esc(e.email || '')}"></label>
        <button class="bouton fin" type="submit">Enregistrer</button>
      </form>
    </td>
  </tr>`
    )
    .join('');

  return layout({
    titre: 'Égéries',
    nav: NAV_ADMIN,
    corps: `
<h1>Égéries</h1>
${alerte(flash)}
${
  codeGenere
    ? `<div class="carte code-genere">
    <p class="surtitre">À transmettre maintenant</p>
    <p class="code">${esc(codeGenere.code)}</p>
    <p class="note">Code d'accès de <strong>${esc(codeGenere.nom)}</strong>. Il n'est affiché
    qu'une seule fois : seule son empreinte est conservée. Transmettez-le par un canal privé.</p>
  </div>`
    : ''
}

<section class="carte">
  <h2>Ajouter une égérie</h2>
  <form method="post" action="/admin/egeries" class="ligne-formulaire">
    <label>Nom complet <input name="nom" required placeholder="Prénom NOM"></label>
    <label>Pays <input name="pays" placeholder="Ex. Brésil"></label>
    <label>E-mail <input type="email" name="email" placeholder="facultatif"></label>
    <button class="bouton" type="submit">Créer l'accès</button>
  </form>
</section>

<section class="carte">
  <table class="tableau">
    <thead><tr><th>Égérie</th><th>Contact</th><th>Autorisation</th><th>Photos</th><th>Accès</th><th></th></tr></thead>
    <tbody>${lignes || '<tr><td colspan="6" class="vide">Aucune égérie.</td></tr>'}</tbody>
  </table>
</section>`,
  });
}

export function pageAdminDepots({ depots, egeries, filtres, flash }) {
  const options = (nom, valeurs, courant) =>
    `<select name="${nom}">${valeurs
      .map(([v, l]) => `<option value="${esc(v)}" ${String(courant) === String(v) ? 'selected' : ''}>${esc(l)}</option>`)
      .join('')}</select>`;

  return layout({
    titre: 'Dépôts',
    nav: NAV_ADMIN,
    corps: `
<h1>Dépôts</h1>
${alerte(flash)}
<form method="get" action="/admin/depots" class="ligne-formulaire carte">
  <label>Égérie ${options('egerie', [['', 'Toutes'], ...egeries.map((e) => [e.id, e.nom])], filtres.egerie)}</label>
  <label>Statut ${options(
    'statut',
    [['', 'Tous'], ['nouveau', 'Nouveaux'], ['traite', 'Traités'], ['archive', 'Archivés']],
    filtres.statut
  )}</label>
  <button class="bouton fin" type="submit">Filtrer</button>
  ${
    filtres.egerie
      ? `<a class="bouton fin fantome" href="/admin/archive/${esc(filtres.egerie)}">Télécharger les originaux (ZIP)</a>`
      : ''
  }
</form>
${
  depots.length
    ? `<div class="grille">${depots
        .map((d) => carteDepot(d, `/media/vignette/${d.id}`, `/admin/depot/${d.id}`))
        .join('')}</div>`
    : `<p class="vide">Aucun dépôt pour ce filtre.</p>`
}`,
  });
}

export function pageAdminDepot({ depot, flash }) {
  return layout({
    titre: depot.nom_origine,
    nav: NAV_ADMIN,
    corps: `
<p class="fil"><a href="/admin/depots">← Tous les dépôts</a></p>
${alerte(flash)}
<section class="detail">
  <div class="cadre grand">
    <img src="/media/apercu/${depot.id}" alt="Aperçu flouté">
    <span class="sceau">aperçu flouté · intensité ${BLUR_SIGMA}</span>
  </div>
  <aside class="carte">
    <h1>${esc(depot.nom_origine)}</h1>
    <dl class="fiche">
      <dt>Égérie</dt><dd>${esc(depot.egerie_nom)} ${badgeContrat(depot.contrat_statut)}</dd>
      <dt>Déposé le</dt><dd>${dateFr(depot.depose_le, true)}</dd>
      <dt>Série</dt><dd>${esc(depot.serie || '—')}</dd>
      <dt>Dimensions</dt><dd>${depot.largeur ? `${depot.largeur} × ${depot.hauteur} px` : '—'}</dd>
      <dt>Poids</dt><dd>${octets(depot.octets)} · ${esc(depot.mime || '—')}</dd>
      <dt>Empreinte</dt><dd class="mono">${esc(depot.sha256.slice(0, 32))}…</dd>
      <dt>Fichier d'origine</dt><dd class="mono">${esc(depot.chemin_original)}</dd>
      <dt>Consentement</dt><dd>${depot.consentement ? 'Confirmé au dépôt' : 'Non confirmé'}</dd>
      <dt>Statut</dt><dd>${badgeDepot(depot.statut)}</dd>
    </dl>
    ${depot.message ? `<blockquote>${esc(depot.message)}</blockquote>` : ''}

    <div class="actions-fiche">
      <form method="post" action="/admin/depot/${depot.id}/statut">
        <input type="hidden" name="statut" value="${depot.statut === 'traite' ? 'nouveau' : 'traite'}">
        <button class="bouton fin">${depot.statut === 'traite' ? 'Remettre à traiter' : 'Marquer traité'}</button>
      </form>
      <form method="post" action="/admin/depot/${depot.id}/statut">
        <input type="hidden" name="statut" value="archive">
        <button class="bouton fin fantome">Archiver</button>
      </form>
    </div>

    <div class="urgence">
      <h2>Accès à l'original</h2>
      <p class="note">Le fichier d'origine, non flouté et non filigrané. Chaque
      téléchargement est horodaté dans le journal.</p>
      <a class="bouton alerte" href="/admin/original/${depot.id}" rel="noopener">Télécharger l'original</a>
    </div>
  </aside>
</section>`,
  });
}

export function pageAdminJournal({ entrees }) {
  return layout({
    titre: 'Journal',
    nav: NAV_ADMIN,
    corps: `
<h1>Journal d'accès</h1>
<p class="chapeau">Trace de tous les accès aux originaux et des mouvements de comptes.
Utile pour prouver, le cas échéant, qui a manipulé quoi.</p>
<section class="carte">
  <table class="tableau">
    <thead><tr><th>Quand</th><th>Acteur</th><th>Action</th><th>Cible</th><th>Détail</th><th>IP</th></tr></thead>
    <tbody>
    ${
      entrees.length
        ? entrees
            .map(
              (e) => `<tr>
        <td>${dateFr(e.quand, true)}</td>
        <td>${esc(e.acteur)}</td>
        <td><code>${esc(e.action)}</code></td>
        <td>${esc(e.cible)}</td>
        <td>${esc(e.detail)}</td>
        <td class="mono">${esc(e.ip)}</td>
      </tr>`
            )
            .join('')
        : '<tr><td colspan="6" class="vide">Journal vide.</td></tr>'
    }
    </tbody>
  </table>
</section>`,
  });
}

export function pageErreur({ code, message }) {
  return layout({
    titre: `Erreur ${code}`,
    classe: 'centre',
    corps: `<section class="carte etroite">
      <p class="surtitre">Erreur ${code}</p>
      <h1>${esc(message)}</h1>
      <a class="bouton fantome" href="/">Retour à l'accueil</a>
    </section>`,
  });
}
