# Cohérence de l’édition — 16 octobre 2026

Relecture d’ensemble après les publications `7a11d27` (50 inédits) et `74fcb25` (1915, Rosamonde, Méthode et Histoire). Les corrections sont appliquées dans les cinq langues.

## Écarts corrigés

- L’accueil décrit désormais les six lots effectivement présentés, sans confondre textes et formulaires : 17 textes Wenmi = 7 G0 + 10 Y0 ; ces derniers réunissent 15 formulaires.
- Le bilan Y0 est recalculé sur les objets publiés : 24 caractères douteux + 2 illisibles sur 456, soit 26 (5,7 %). Cinq n’ont pas de proposition (1,1 %). Le total Wenmi sans proposition passe de l’ancien texte « quatorze » à 12.
- Le corpus 1915 compte 53 caractères douteux **et 1 illisible** sur 446 ; février–mars 1916 compte 48 douteux **et 1 illisible** sur 741. Les générateurs incluent désormais `stats.illisible` et l’affichent.
- La carte de relecture de l’accueil reprend les 71 corrections déjà détaillées ailleurs : 28 initiales + 43 ciblées. La page de relecture indique explicitement qu’elle développe la première étape.
- Les introductions ne présentent plus tous les lots comme des lectures aveugles, ni toutes les séries comme des condensateurs G0/Y0. Elles distinguent lectures sur scan, transcription antérieure, relectures aveugles et préremplies, transcription diplomatique, propositions et recalage.
- Le classement du lot Inédits par date est explicite ; les autres séries gardent leur classement par système puis par date. Les numéros de vue JACAR et de page PDF sont distingués.
- Les usages de Laisaosang et New York en juin/juillet 1914 figurent au récapitulatif. Les descriptions de ces systèmes et de Shanghai/San Francisco renvoient aux attestations antérieures. Le récapitulatif est remis dans l’ordre des premières dates ; Kai est clairement une **candidate**, hors corpus publié, dont l’écart de 1,40 ne passe pas le seuil strict de 1,5.
- Les statistiques historiques de Rosamonde (absence de f/q, 750 lettres, 109/611, 59/1 061 et comparaisons de relectures) sont rattachées à l’échantillon initial, hors ajouts des 6 et 7 mars 1915. L’usage qq/[pp] est expliqué près de la table de base.
- Le passage présentant encore la permutation des consonnes comme une recherche ouverte renvoie maintenant au résultat déjà publié : la table de Huang Xing. Il ne contredit plus la description de G0 comme alphabet inversé.
- Le sens de rotation de Sixteenth/Seventeenth est précisé (vers la gauche). Le titre de l’Histoire et sa carte d’accueil couvrent 1913–1916 ; les descriptions des pages reflètent leurs périmètres élargis.

## Contrôles et conservation

`tools/check_site_coherence.cjs` recalcule les effectifs depuis les fichiers de corpus, compare les résumés des cinq accueils, vérifie la couverture du classement, des dates et traductions, et les mentions de périmètre. Son option `--baseline` compare intégralement les objets des télégrammes, dictionnaires de traduction, lignes Rosamonde, gabarit 1917 et analyse politique et militaire au commit choisi.

```sh
python3 tools/build_t1915.py ../wenmi
python3 tools/build_f1916.py ../wenmi
python3 tools/build_inedits.py ../wenmi
python3 tools/build.py
node tools/check_site_coherence.cjs --baseline 74fcb25
python3 tools/check_editorial_visuals.py
python3 tools/check_rosamonde_illustrations.py
git diff --check
```

Une seconde exécution des quatre commandes de génération laisse les fichiers suivis identiques. Les deux contrôles d’illustrations passent. Le contrôle navigateur couvre les 35 pages à 360 et 1 280 pixels, les images, les identifiants, les erreurs JavaScript et les liens locaux, y compris les ancres produites par JavaScript sur la page des télégrammes.

Les corps, lectures, traductions et propositions des télégrammes sont conservés. Aucune nouvelle méthode de recherche de clé ni nouveau déchiffrement n’est revendiqué. L’analyse politique et militaire ajoutée précédemment est conservée ; ses renvois aux télégrammes sont contrôlés avec les autres liens. Aucun contenu nouveau sur juin 1917.
