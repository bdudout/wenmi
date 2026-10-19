# Wenmi (文密, 1916) — solveur et clés

*Brice Dudout, avec Claude (Anthropic), 2026 — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). English below.*

Ce dossier contient de quoi **vérifier et rejouer** le déchiffrement présenté sur le site
(<https://bdudout.github.io/wenmi/>), sans le reste de l'enquête (journal, essais négatifs, lots de lecture).

| Fichier | Rôle |
|---|---|
| `wenmi.py` | les deux clés retrouvées (grilles **G0** et **Y0**), le décodage et le score par le modèle de langue |
| `rank_test.py` | le test **sans clé** qui a tout débloqué : la consonne porte la dizaine du demi-code |
| `anchor_coord.cpp` | le moteur de recherche (recuit simulé sur les tables « de coordonnées »), tel qu'utilisé dans l'enquête |
| `make_job.py`, `compare.py` | préparer une recherche avec le jeu d'ancres « D », puis comparer le résultat à G0 |
| `data/cen_v8.json` | canal Tokyo → Zhaoqing : syllabes lues sur les formulaires (lectures humaines), 7 télégrammes |
| `data/yunnan_v3.json` | canal Tokyo ↔ Yunnan : syllabes lues (lectures humaines), 15 formulaires |
| `data/relecture-1916.csv` | relecture des télégrammes à condensateur de mars–mai 1916 (transcription publiée) sur les scans, en deux lots de lecture aveugle : B1 (45 propositions d'une lettre), B2 (propositions du crible, lectures du texte publié, corrections appliquées) ; mot transcrit, mot lu sur le scan, lettre, caractères avant/après, verdict (voir la page « Condensateurs 1916 ») |
| `numeric1916/` | télégrammes numériques de juin 1916 (共密, 容密, 辰密) : les trois clés, les chiffres relus, la reproduction des textes publiés, les recherches de clé avec témoins (voir son README) |
| `rongmi/`, `chenmi/` | décodeurs autonomes 容密 et 辰密 |
| `lm3/` | modèle de langue (unigrammes et bigrammes de codes télégraphiques) et table code → caractère |

## Décoder

```bash
pip install numpy
python3 wenmi.py decode cen      # G0
python3 wenmi.py decode yunnan   # Y0
```

## Le test sans clé

```bash
python3 rank_test.py data/cen_v8.json
```

Résultat attendu : consonnes z ≈ 30, voyelles z ≈ 2. Les consonnes se répartissent très différemment aux rangs pairs
(première moitié du code) et impairs ; les voyelles presque pas. C'est la signature d'une table où la consonne code la
dizaine et la voyelle l'unité.

## Rejouer la recherche

```bash
clang++ -O3 -march=native -std=c++17 -pthread -o anchor_coord anchor_coord.cpp
python3 make_job.py job.txt
./anchor_coord job.txt out.tsv 32 15000000 8 8 10 2000000 6 0.6 1234 100 0 0.3
python3 compare.py out.tsv
```

Arguments : restarts, itérations, graine, threads, puis recherche locale itérée (tours, itérations, perturbations,
température), et quatre options neutres ici (arrangement 1234, retenue 100, décalage 0, probabilité 0,3 d'échanger deux
consonnes). Environ 2 minutes sur 8 cœurs.

Résultat obtenu en préparant ce dossier : table trouvée identique à G0 sur **83 cases sur 100** ; le message 0406,
**tenu à l'écart** de la recherche, se lit à +3,87 par caractère sous la table trouvée et à **+4,28 sous G0**. La grille
régulière lit mieux que la table ajustée dont on l'a déduite : c'est l'argument central du déchiffrement. Le jeu d'ancres
« D » contient d'ailleurs une ancre fausse (`xi` = 41, issue de l'erreur de copie e → i de 0416b), que la recherche
absorbe.

`python3 make_job.py job_null.txt null` prépare le **témoin nul** (syllabes mélangées dans chaque message) : son score
doit rester très inférieur.

Les scores de ce dossier sont calculés sur les lectures les plus récentes. Ceux cités dans les articles (par exemple
+3,99 pour 0406) ont été calculés par les scripts de l'enquête sur une lecture antérieure du même formulaire.

## Sources des données

- Formulaires : Archives diplomatiques du ministère des Affaires étrangères du Japon, via JACAR (B03050089900,
  B03050090000, B03050090100). Lectures : Brice Dudout, à l'aveugle (extraits anonymes mélangés).
- Code télégraphique chinois : Unicode Unihan (`kTaiwanTelegraph`, `kMainlandTelegraph`).
- Modèle de langue : 225 textes de Sun Yat-sen sur Wikisource chinois (≈ 430 000 caractères), convertis en codes.
- Travaux à l'origine de l'enquête : Daniel Bourdeau, « Sun Yat-sen's circle on the wire, 1916–17 » et
  [dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver).

---

# Wenmi (文密, 1916) — solver and keys

*Brice Dudout, with Claude (Anthropic), 2026 — CC BY 4.0.*

This folder lets anyone **check and re-run** the decipherment presented on the site, without the rest of the
investigation. `wenmi.py` holds both recovered keys (G0, Y0) and decodes the two channels; `rank_test.py` is the keyless
test (the consonant carries the tens digit); `anchor_coord.cpp` is the annealing engine used in the investigation;
`make_job.py` + `compare.py` re-run the search with anchor set "D" and compare the result with G0. Expected outcome: 83/100
cells identical to G0, and the held-out message 0406 reads at +3.87 per character under the found table versus +4.28
under G0. Data: human readings of the JACAR forms (Brice Dudout), Unihan telegraph codes, a language model built from
Sun Yat-sen's writings on Chinese Wikisource. Built on Daniel Bourdeau's work.

The June 1916 numeric telegrams (Gongmi 共密, Rongmi 容密, Chenmi 辰密) have their own folder, `numeric1916/`: the three keys,
the digits as re-read, exact reproduction of the 29 published raw texts, and from-scratch key searches with null controls (see its README).
