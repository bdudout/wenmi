# Inédits 1913–1916 — édition du 16 octobre 2026

50 télégrammes : 11 C39 (1913–1914), 39 C40 (avril 1916). Les lettres de Claude ont été relues par Brice Dudout sur des transcriptions préremplies, non à l’aveugle. Édition et contrôles de publication : Codex. Autorisation de publication par lots donnée par Brice et transmise dans `CONSIGNES-CODEX-publication-inedits-1913-1916.md`.

## Construire

Comme les autres scripts de corpus, les builds emploient les tables et ressources linguistiques du dossier d’enquête voisin `wenmi` :

```sh
python3 tools/build_inedits.py ../wenmi
python3 tools/make_fiches_inedits.py ../wenmi
python3 tools/build.py
```

`tools/data/inedits_data.json` est la copie figée de l’édition (y compris les traductions). Le fichier de travail est `wenmi/cryptanalysis/c40/site/inedits_data.json`, préparé par `prepare_inedits.py` dans ce même dossier. Le build actualise la copie figée et la prend comme repli si le fichier de travail manque. Les images reproduisent 45 pages des cinq PDF JACAR, sans rognage des marges ni des numéros de microfilm ; les suites de formulaires sont jointes.

## Sélection et limites

- Chaque entrée publiée a un score ≥ 1,5 et strictement supérieur au témoin + 1,5, avec une table établie et un texte intelligible au moins en partie. Les scores C40 et les témoins sont ceux de `decodes.json` (recalage déjà retenu ; pour a18t, résultat `rescue`). Les contrôles numériques C39 et Hong Kong ont été vérifiés sur vingt mélanges, graines 3800–3819. Les contrôles des trois entrées 87500 sont ceux de `fam875-results.json`.
- Aucun nouveau solveur ni nouvelle recherche de clé pour cette publication. Les corrections sémantiques automatiques de `props` n’ont pas été appliquées. Seules six propositions explicitement retenues par les notes précédentes / consignes sont affichées : 廣, 到, 移, 內, 五 et 望.
- C40 exclus : a39, b23, b27t, b33t, b38b, b39t.
- C39 exclus supplémentaires : b07t (début illisible et score LM-T 1,414 sous 1,5), m12 « Kai » (3,013 − témoin 1,613 = 1,400 sous 1,5), m19 « Kai » (brouillon trop fragmentaire, malgré un score passant le seuil). Aucun des deux messages Kai n’est publié dans ce lot, et aucune identification de Kai/Ting n’est affirmée.
- Les lettres du formulaire restent intactes au-dessus des cases. Dans les cases, `?` est une insertion proposée par le recalage, pas une lecture humaine ; les insertions/suppressions sont détaillées. Le décodage avant recalage est également conservé. Les passages non résolus restent visiblement douteux, et les traductions / extraits les signalent sans compléter le sens.
- Le texte chinois traditionnel est conservé pour l’édition. Les éléments d’interface et traductions en chinois simplifié sont dérivés par le mécanisme commun du site.
- Hong Kong est une substitution lettre → chiffre, et les messages numériques sont en code télégraphique direct. Ils affichent donc quatre signes par case sans les séparer artificiellement en syllabes.
- Tables nouvellement représentées : Sixteenth, Seventeenth, Hsuweilin, Hong Kong. Les quatre tables connues de Shanghai, Qingdao, San Francisco et Manille sont attribuées à D. Bourdeau dans les sources [1, 24].

Le [manifest public](../../assets/data/inedits-1913-1916-provenance.json) contient les entrées retenues, transcriptions, recalages, scores/témoins, décisions d’exclusion, tables et empreintes SHA-256 des quatre jeux de lectures, trois exports humains et cinq PDF. Les PDF correspondent aux empreintes du journal de sources. Les limites du témoin initial et du recalage restent séparées dans les données, sans présenter un score de solveur comme une certification de chaque caractère.

## Vérification de publication

Contrôles du navigateur : FR / EN / JA / zh-Hant / zh-Hans, 1280 et 360 px ; 50 fiches et 1 635 cases par langue ; 386 caractères douteux, 5 illisibles, 6 propositions. Images et ancres vérifiées ; les sections préexistantes du corpus sont comparées au DOM produit par le JavaScript du commit précédent, sans changement. Les longs trains de points du décodage brut utilisent un retour à la ligne limité à la nouvelle section.
