# Le code Wenmi · 文密

Par **Brice Dudout**, en collaboration avec Claude (Anthropic) — licence [CC BY 4.0](LICENSE) (mentions et exceptions : [NOTICE.md](NOTICE.md)).

Site statique présentant le déchiffrement du code **文密 (Wenmi)** : télégrammes chiffrés de 1916
entre Tokyo et le Sud de la Chine, interceptés et recopiés par l'administration japonaise
(archives JACAR). Deux articles, en cinq langues (français, anglais, chinois simplifié,
chinois traditionnel, japonais) :

1. **L'histoire** — contexte historique pour non-spécialistes et contenu des télégrammes ;
2. **La méthode** — write-up technique : transcription aveugle, tests sans clé, solveurs,
   validation sur messages tenus à l'écart, grilles G0 et Y0 (avec animation et décodeur interactif) ;
3. **Les télégrammes** — les 17 télégrammes de 1916, caractère par caractère, avec pistes d'erreur
   (Morse, copie) pour les passages douteux.

Le dossier [`solver/`](solver/) contient le solveur, les deux clés, les données de lecture et le
modèle de langue, de quoi rejouer le déchiffrement.

Ce travail prolonge celui de **Daniel Bourdeau**,
[« Sun Yat-sen's circle on the wire, 1916–17 »](https://dbourdeau.github.io/cyphersolver/sunintercepts.html)
([dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver), CC BY 4.0).

## Structure

```
index.html              page de choix de langue (redirige selon la langue du navigateur)
fr/ en/ zh-hans/ zh-hant/ ja/
                        pages GÉNÉRÉES (ne pas éditer à la main)
content/<langue>/       corps des pages (index, history, method, telegrams, sources) — à éditer
assets/css/style.css    styles (thème clair/sombre, marqueur « non confirmé »)
assets/js/site.js       thème, grille G0, décodeur pas à pas
assets/js/messages.js   canal Tokyo → Zhaoqing (grille G0) : unités, codes, caractères (GÉNÉRÉ)
assets/js/messages-y0.js  canal Tokyo ↔ Yunnan (grille Y0) : idem (GÉNÉRÉ)
assets/js/translations.js  dates et traductions de travail, par langue
assets/img/             scan JACAR (B03050090000, image 0416)
assets/img/flags/       drapeaux du sélecteur de langue (SVG, GÉNÉRÉS)
tools/build.py          assemble content/ + gabarit → <langue>/*.html
tools/build_data.py     extrait messages.js de l'édition et vérifie la grille G0
tools/build_data_y0.py  décode le second canal sous Y0 et vérifie contre c31-decodage-Y0.md
tools/make_flags.py     dessine les drapeaux en SVG
tools/build_corpus.py   page « Télégrammes » : statut de chaque code, pistes d'erreur Morse/copie
tools/make_media.py     carte, vidéo de l'histoire, animation du déchiffrement, sous-titres (5 langues)
assets/media/           vidéos MP4 et sous-titres WebVTT (GÉNÉRÉS)
assets/img/portraits/   portraits du domaine public (Wikimedia Commons), crédits dans credits.json
solver/                 solveur publié (voir solver/README.md)
```

## Construire

```bash
python3 tools/build.py
```

Régénérer les données des télégrammes depuis l'édition de travail (dossier d'enquête) :

```bash
python3 tools/build_data.py "../wenmi/working/c31-edition-wenmi.md"
```

Le script vérifie que la grille G0 redonne exactement les 351 codes. Pour le second canal
(nécessite NumPy et le modèle de langue du dossier d'enquête) :

```bash
python3 tools/build_data_y0.py ../wenmi
```

Il vérifie que le décodage est identique, caractère pour caractère, à `working/c31-decodage-Y0.md`.

Puis la page « Télégrammes » et les médias (le fond de carte Natural Earth `ne_110m_land.geojson`
n'est pas versionné ; ffmpeg requis) :

```bash
python3 tools/build_corpus.py ../wenmi
python3 tools/make_media.py chemin/vers/ne_110m_land.geojson all
```

Prévisualiser :

```bash
python3 -m http.server 8765
```

## Site autonome

Aucune ressource externe n'est chargée : pas de police web, pas de CDN, pas de traceur. Les
polices sont celles du système (Songti / SimSun / Noto CJK pour le chinois, Hiragino / Yu Mincho
pour le japonais, Charter / Georgia pour le latin), les drapeaux sont des SVG du dépôt. Le site
reste ainsi lisible là où Google Fonts ou les CDN sont bloqués (Chine continentale notamment).
Ne pas réintroduire de `<link>`/`<script>` vers un domaine tiers.

La langue est choisie à l'arrivée sur la racine : choix déjà fait sur le site (mémorisé), puis
langue du navigateur, sinon **anglais**. `index.html?choose` affiche le sélecteur sans redirection.

## Publication (GitHub Pages)

Le site est entièrement statique (aucune étape de build côté serveur, `.nojekyll` présent).
Pousser le dépôt puis activer *Settings → Pages → Deploy from a branch → main / (root)*.

## Conventions éditoriales

- `<mark class="unc">…</mark>` signale une information **non confirmée** ou une hypothèse ;
  l'étiquette est traduite automatiquement selon la langue de la page.
- Les références `[n]` renvoient à `sources.html#sn` ; la numérotation est identique dans les
  cinq langues.
- Les citations chinoises des télégrammes restent en caractères traditionnels (`lang="zh-Hant"`),
  telles qu'elles ont été décodées.

## Crédits et licence

Enquête et lectures : Brice Dudout, en collaboration avec Claude (Anthropic). Textes, code et
médias générés : CC BY 4.0 (texte complet dans [LICENSE](LICENSE) ; voir [NOTICE.md](NOTICE.md) pour les exceptions : scan JACAR,
portraits du domaine public, fond Natural Earth, données dérivées). Images des télégrammes :
Archives diplomatiques du ministère des Affaires étrangères du Japon, via JACAR.
