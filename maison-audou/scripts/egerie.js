#!/usr/bin/env node
// Gestion des accès égéries en ligne de commande.
//
//   npm run egerie -- lister
//   npm run egerie -- ajouter --nom "Prénom NOM" --pays "Brésil" --email x@y.z
//   npm run egerie -- code --id 3          (remplace le code d'accès)
//   npm run egerie -- contrat --id 3 --statut signe --signe 2026-08-26 --fin 2036-08-26
//   npm run egerie -- suspendre --id 3 | reactiver --id 3

import { db, creerEgerie, reinitialiserCode, journaliser } from '../src/db.js';

const [, , commande = 'lister', ...reste] = process.argv;

const options = {};
for (let i = 0; i < reste.length; i += 1) {
  if (reste[i].startsWith('--')) {
    const cle = reste[i].slice(2);
    const valeur = reste[i + 1] && !reste[i + 1].startsWith('--') ? reste[i + 1] : '1';
    options[cle] = valeur;
    if (valeur !== '1') i += 1;
  }
}

const STATUTS = {
  signe: 'signée',
  en_attente: 'en attente',
  expire: 'expirée',
  resilie: 'résiliée',
};

function exiger(cle) {
  if (!options[cle]) {
    console.error(`Option --${cle} requise.`);
    process.exit(1);
  }
  return options[cle];
}

function lister() {
  const lignes = db
    .prepare(
      `SELECT e.id, e.nom, e.slug, e.pays, e.active, e.contrat_statut, e.contrat_fin_le,
              (SELECT COUNT(*) FROM depots d WHERE d.egerie_id = e.id) AS nb
       FROM egeries e ORDER BY e.nom`
    )
    .all();
  if (!lignes.length) return console.log('Aucune égérie enregistrée.');
  console.log('');
  for (const l of lignes) {
    console.log(
      `  #${String(l.id).padEnd(3)} ${l.nom.padEnd(24)} ${(l.pays || '—').padEnd(14)} ` +
        `${l.nb} photo(s)  autorisation ${STATUTS[l.contrat_statut] || l.contrat_statut}` +
        `${l.contrat_fin_le ? ` (fin ${l.contrat_fin_le})` : ''}${l.active ? '' : '  [SUSPENDU]'}`
    );
  }
  console.log('');
}

switch (commande) {
  case 'lister':
    lister();
    break;

  case 'ajouter': {
    const nom = exiger('nom');
    const { id, slug, code } = creerEgerie({
      nom,
      pays: options.pays || '',
      email: options.email || '',
    });
    journaliser({ acteur: 'cli', action: 'egerie_creee', cible: id, detail: nom });
    console.log(`\n  ${nom} créée (#${id}, ${slug})`);
    console.log(`  Code d'accès : ${code}`);
    console.log(`  À transmettre par canal privé — il ne sera plus jamais affiché.\n`);
    break;
  }

  case 'code': {
    const id = exiger('id');
    const egerie = db.prepare('SELECT * FROM egeries WHERE id = ?').get(id);
    if (!egerie) {
      console.error('Égérie introuvable.');
      process.exit(1);
    }
    const code = reinitialiserCode(egerie.id);
    journaliser({ acteur: 'cli', action: 'code_regenere', cible: egerie.id, detail: egerie.nom });
    console.log(`\n  Nouveau code pour ${egerie.nom} : ${code}\n`);
    break;
  }

  case 'contrat': {
    const id = exiger('id');
    const statut = options.statut || 'signe';
    if (!STATUTS[statut]) {
      console.error(`Statut inconnu. Valeurs : ${Object.keys(STATUTS).join(', ')}`);
      process.exit(1);
    }
    db.prepare(
      'UPDATE egeries SET contrat_statut = ?, contrat_signe_le = ?, contrat_fin_le = ? WHERE id = ?'
    ).run(statut, options.signe || null, options.fin || null, id);
    journaliser({ acteur: 'cli', action: 'egerie_modifiee', cible: id, detail: `autorisation=${statut}` });
    console.log(`Autorisation mise à jour : ${STATUTS[statut]}.`);
    break;
  }

  case 'suspendre':
  case 'reactiver': {
    const id = exiger('id');
    db.prepare('UPDATE egeries SET active = ? WHERE id = ?').run(commande === 'reactiver' ? 1 : 0, id);
    journaliser({ acteur: 'cli', action: `egerie_${commande}e`, cible: id });
    console.log(commande === 'reactiver' ? 'Accès réactivé.' : 'Accès suspendu.');
    break;
  }

  default:
    console.error(`Commande inconnue : ${commande}`);
    console.error('Commandes : lister, ajouter, code, contrat, suspendre, reactiver');
    process.exit(1);
}
