// Confort de dépôt : liste des fichiers choisis, glisser-déposer, et
// verrouillage du bouton pendant l'envoi (les fichiers sont lourds et les
// connexions de nos égéries pas toujours rapides).
(() => {
  const zone = document.getElementById('zone-depot');
  const champ = document.getElementById('photos');
  const liste = document.getElementById('liste-fichiers');
  const formulaire = document.getElementById('formulaire-depot');
  const bouton = document.getElementById('bouton-envoi');
  const etat = document.getElementById('etat-envoi');
  if (!zone || !champ) return;

  const poids = (n) => {
    const u = ['o', 'Ko', 'Mo', 'Go'];
    const i = Math.min(u.length - 1, Math.floor(Math.log(n || 1) / Math.log(1024)));
    return `${(n / 1024 ** i).toFixed(i === 0 ? 0 : 1)} ${u[i]}`;
  };

  function afficher() {
    liste.innerHTML = '';
    const fichiers = [...champ.files];
    for (const f of fichiers) {
      const li = document.createElement('li');
      const nom = document.createElement('b');
      nom.textContent = f.name;
      const taille = document.createElement('span');
      taille.textContent = poids(f.size);
      li.append(nom, taille);
      liste.append(li);
    }
    if (fichiers.length) {
      const total = document.createElement('li');
      const b = document.createElement('b');
      b.textContent = `${fichiers.length} fichier${fichiers.length > 1 ? 's' : ''}`;
      const s = document.createElement('span');
      s.textContent = poids(fichiers.reduce((t, f) => t + f.size, 0));
      total.append(b, s);
      liste.append(total);
    }
  }

  champ.addEventListener('change', afficher);

  ['dragenter', 'dragover'].forEach((e) =>
    zone.addEventListener(e, (ev) => {
      ev.preventDefault();
      zone.classList.add('survol');
    })
  );
  ['dragleave', 'drop'].forEach((e) =>
    zone.addEventListener(e, () => zone.classList.remove('survol'))
  );
  zone.addEventListener('drop', (ev) => {
    ev.preventDefault();
    if (!ev.dataTransfer?.files?.length) return;
    champ.files = ev.dataTransfer.files;
    afficher();
  });

  formulaire?.addEventListener('submit', () => {
    if (!champ.files.length) return;
    bouton.disabled = true;
    bouton.textContent = 'Envoi en cours…';
    etat.hidden = false;
  });

  // Un envoi de 40 photos peut durer plusieurs minutes sur un réseau mobile.
  window.addEventListener('beforeunload', (e) => {
    if (bouton?.disabled) {
      e.preventDefault();
      e.returnValue = '';
    }
  });
})();
