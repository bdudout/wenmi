# Le code Wenmi · 文密

Site statique présentant le déchiffrement du code **文密 (Wenmi)** : télégrammes chiffrés de 1916
entre Tokyo et le Sud de la Chine, interceptés et recopiés par l'administration japonaise
(archives JACAR). Deux articles, en cinq langues (français, anglais, chinois simplifié,
chinois traditionnel, japonais) :

1. **L'histoire** — contexte historique pour non-spécialistes et contenu des télégrammes ;
2. **La méthode** — write-up technique : transcription aveugle, tests sans clé, solveurs,
   validation sur message tenu à l'écart, grille G0 (avec décodeur interactif).

Ce travail prolonge celui de **Daniel Bourdeau**,
[« Sun Yat-sen's circle on the wire, 1916–17 »](https://dbourdeau.github.io/cyphersolver/sunintercepts.html)
([dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver), CC BY 4.0).

## Structure

```
index.html              page de choix de langue (redirige selon la langue du navigateur)
fr/ en/ zh-hans/ zh-hant/ ja/
                        pages GÉNÉRÉES (ne pas éditer à la main)
content/<langue>/       corps des pages (index, history, method, sources) — à éditer
assets/css/style.css    styles (thème clair/sombre, marqueur « non confirmé »)
assets/js/site.js       thème, grille G0, décodeur pas à pas
assets/js/messages.js   unités, codes et caractères des 7 télégrammes (GÉNÉRÉ)
assets/js/translations.js  dates et traductions de travail, par langue
assets/img/             scan JACAR (B03050090000, image 0416)
assets/img/flags/       drapeaux du sélecteur de langue (SVG, GÉNÉRÉS)
tools/build.py          assemble content/ + gabarit → <langue>/*.html
tools/build_data.py     extrait messages.js de l'édition et vérifie la grille G0
tools/make_flags.py     dessine les drapeaux en SVG
```

## Construire

```bash
python3 tools/build.py
```

Régénérer les données des télégrammes depuis l'édition de travail (dossier d'enquête) :

```bash
python3 tools/build_data.py "../wenmi/working/c31-edition-wenmi.md"
```

Le script vérifie que la grille G0 redonne exactement les 351 codes.

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

## Crédits

Images des télégrammes : Archives diplomatiques du ministère des Affaires étrangères du Japon,
via JACAR. Enquête : Brice Dudout, avec des assistants de code IA.
