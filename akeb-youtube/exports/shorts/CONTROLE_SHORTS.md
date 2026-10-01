# Contrôle des trois Shorts existants — 01/10/2026

Fichiers reçus de Codex (transmission du 01/10/2026), empreintes SHA-256 conformes au manifeste. Originaux **non modifiés**.

## Ce qui a été vérifié

| Point | 01 Il aurait dû se taire | 02 Le faux prêtre | 03 Après la disparition |
|---|---|---|---|
| Format | 1080×1920, H.264, AAC mono 48 kHz | idem | idem |
| Durée | 24,64 s | 24,36 s | 25,60 s |
| Cadence | **24 i/s** (cahier des charges : 30) | **24 i/s** | **24 i/s** |
| Sonie intégrée | −16,8 LUFS | −16,7 LUFS | −17,6 LUFS |
| Crête vraie | −1,7 dBTP | −1,7 dBTP | −1,7 dBTP |
| Voix seule | 22,64 s, ≈ 138 mots/min | 22,36 s | 23,60 s |
| Décalage voix / vidéo | 0,005 s | 0,005 s | 0,005 s |
| « THRILLER DE FICTION » | présent du début à la fin | idem | idem |
| Écran final | couverture, « À lire · À écouter », EPUB+PDF 2,99 €, MP3+M4B 4,99 €, payhip.com/ladernierecorrection, ≈ 4 s | idem (dès ≈ 15 s) | idem |
| Vrai nom de l'affaire | absent | absent | absent |

Méthode : ffprobe, ebur128 (crête vraie), détection des silences sur la voix seule, intercorrélation voix/vidéo, planche de 24 images (8 instants × 3) relue visuellement.
**Non couvert** : écoute humaine (prononciation, intonation, consignes vocalisées éventuelles).

## Défauts constatés

1. **Mention « THRILLER DE FICTION » dans la zone masquée par l'interface Shorts.** Elle est placée à 83,7–84,8 % de la hauteur (y = 1607–1629 px), « Narration numérique · Akeb » à 86–87 %. Sur mobile, cette bande est en général couverte par le titre, le nom de chaîne et la légende. La mention obligatoire risque donc d'être invisible du début à la fin. L'adresse de la boutique (76–78 %) est en limite.
2. **24 i/s au lieu de 30 i/s.** Sans effet visible sur ces montages typographiques ; écart au cahier des charges seulement.
3. **Sous-titres SRT à minutage estimé, répliques longues** (jusqu'à 117 caractères sur une ligne). → Corrigé : `*_v2_aligne.srt` (ci-dessous).

## Corrections livrées ici

- `01_il_aurait_du_se_taire_v2_aligne.srt`, `02_le_faux_pretre_v2_aligne.srt`, `03_apres_la_disparition_v2_aligne.srt` : répliques de 2 lignes maximum (32 caractères par ligne, format vertical). Chaque frontière de proposition est appariée à une pause réellement mesurée dans le WAV de voix. Outil : `outils/srt_aligne.py`. À déposer comme sous-titres natifs dans YouTube Studio.

## Correction à faire à la source (Codex, sur le PC, avec `produire_shorts.py`)

Ré-exporter les trois Shorts **sans nouvelle narration** (réutiliser les WAV de voix existants, aucun coût) :
- placer « THRILLER DE FICTION » dans la zone sûre, au-dessus de 72 % de la hauteur, par exemple sous « LA DERNIÈRE CORRECTION » sur les plans de texte et au-dessus de la couverture sur l'écran final ;
- garder l'adresse de la boutique au-dessus de 75 % de la hauteur ;
- exporter à 30 i/s ; mêmes voix, même ambiance ;
- nouveaux noms : `0X_…_v2.mp4`. Les originaux restent intacts.

En attendant, les titres et descriptions des Shorts disent explicitement « fiction ».
