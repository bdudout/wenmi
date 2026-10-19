# Télégrammes numériques de juin 1916 — 共密, 容密, 辰密 : outils de contrôle

*Brice Dudout, avec Claude (Anthropic), octobre 2026 — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). English below.*

Ce dossier permet de **refaire indépendamment** le déchiffrement des télégrammes numériques de juin 1916 publiés sur le site
(pages [共密](https://bdudout.github.io/wenmi/fr/gongmi.html), [容密](https://bdudout.github.io/wenmi/fr/rongmi.html),
[辰密](https://bdudout.github.io/wenmi/fr/chenmi.html)) : relire les chiffres sur les scans JACAR, rejouer les clés, et
relancer la recherche des clés sans a priori, avec des témoins. Python 3 + NumPy suffisent.

| Fichier | Rôle |
|---|---|
| `common.py` | les trois clés (共密 C51, 容密 v2, 辰密 C92), le code télégraphique, le modèle de langue, le chargement des données |
| `decode.py` | décoder des groupes (`--key rongmi 2081 3308`) ou un télégramme publié (`--message N16`) ; `--list` |
| `verify.py` | contrôle : reproduction exacte des 32 textes bruts publiés à partir des chiffres ; score de chaque clé contre des clés aléatoires de même forme et contre les chiffres mélangés |
| `search_gongmi.py` | recherche de la clé 共密 : les 10 000 constantes K, permutation des dizaines optimale pour chacune |
| `search_rongmi.py` | recherche de la clé 容密 : quatre substitutions de chiffres (recuit), puis constante K et retenues |
| `search_chenmi.py` | recherche de la clé 辰密 : pages, dizaines et unités permutées (recuit + affectation), comparaison avec le décompte sans zéro |
| `search_common.py` | affectation exacte (algorithme hongrois) et témoins par mélange |
| `data/messages.json` | 37 télégrammes : chiffres **tels que relus** par Brice Dudout, feuillets JACAR (cote, page PDF, côté), date, texte brut et lecture proposés tels que publiés ; 5 télégrammes non lus (premier feuillet) |
| `data/reread/` | les exports bruts des relectures de Brice Dudout, case par case, colonne par colonne (droite → gauche) |
| `lm/` | modèle de langue des clés (unigrammes et bigrammes de codes CTC, entraîné sur les textes déjà publiés du site, 1915–1916) et table code → caractère |

## Remarque sur V4B, V4D, V4E

Pour ces trois télégrammes du vol. 4, les groupes de `data/messages.json` intègrent les glissements de cadrage déduits du décodage
(un chiffre manquant ou en trop, champ `repairs` des pages du site) ; ils restent à vérifier sur les scans.

## Lecture des feuillets

Colonnes de droite à gauche, chaque colonne de haut en bas, feuillet après feuillet (parcours proposé par Brice Dudout) ;
le flux est coupé en groupes de quatre chiffres ; « ? » = chiffre illisible. Les deux premiers groupes sont un préfixe en clair qui nomme
le code : `0364 1378` = 共密, `1369 1378` = 容密, `6591 1378` = 辰密 (N05 n'en a pas). Scans : JACAR, série « 特定人ノ発受郵便物取調 »,
B03050089200 à B03050089500 (`https://www.jacar.archives.go.jp/das/meta/<cote>`).

## Les trois clés

- **共密 (C51)** : remplacer la dizaine t par φ(t), φ = 9 7 6 1 4 0 5 2 8 3, puis P = (9000 − C′) mod 10000.
- **容密 (v2)** : remplacer chaque chiffre selon son rang (milliers 0123456790, centaines identité, dizaines 0198276543, unités 9801723456),
  puis P = (σ(C) + 0901) mod 10000 avec retenues ; aucun groupe ne commence par 00, le chiffreur écrit 90.
- **辰密 (C92)** : page = rang des deux premiers chiffres dans le décompte des nombres sans zéro (99 → 00, 91 → 08, 89 → 09…, 11 → 80) ;
  P = 100 × page + 10 × T(dizaine) + U(unité), T = 3987102645, U = 1 9 5 4 3 2 6 7 8 10 (9 vaut 10, retenue).

P est le numéro du caractère dans le code télégraphique chinois (CTC). Aucune clé n'a été retrouvée dans un livre de code historique.

## Résultats attendus

```
python3 verify.py                 # 32/32 ; 共密 3,50 · 容密 3,26 · 辰密 3,77 contre des témoins ≤ −1,2
python3 search_gongmi.py          # retrouve K = 9000 et φ exactement (quelques secondes)
python3 search_rongmi.py          # étape 1 lisible (≈ 2,2, avec l'anomalie historique 借甸 pour 借款) ; étape 2 : K = 0900
                                  #   et des tables équivalentes à une retenue près (la clé publiée, K = 0901, fait mieux : 3,26)
python3 search_chenmi.py          # long (≈ 1 h avec les réglages par défaut ; --anneals 2 pour aller plus vite) :
                                  #   dizaines et unités exactes (unité 9 lue 0), 2,71 contre des témoins ≤ 0,94 ; pages
                                  #   imposées par le décompte sans zéro : 3,20 ; avec 9 = 10 : 3,77 = clé publiée
```

Les recherches ne reproduisent pas les dernières étapes faites à la main et documentées sur la page Méthode du site
(règle « 90 = 00 » de 容密, imposition du décompte sans zéro et règle « 9 = 10 » de 辰密) ; `verify.py` contrôle la clé finale.

## Ce qui reste ouvert

N01, N03 (sans préfixe connu), N06 (和密), N07 (préfixe 共密, illisible sous C51), N09 (乾密) : seul le premier feuillet est transcrit.
Corrections de lecture, autres hypothèses et contre-vérifications bienvenues (issues GitHub).

---

## English

This folder lets anyone **independently re-check** the decipherment of the June 1916 numeric telegrams published on the site
(Gongmi, Rongmi and Chenmi pages): re-read the digits on the JACAR scans, replay the keys, and re-run the key searches from
scratch against null controls. Python 3 + NumPy only. `data/messages.json` holds the digits **as re-read** by Brice Dudout,
with sheet references and the published raw text and proposed reading; `data/reread/` holds the raw cell-by-cell re-reading exports.
`verify.py` reproduces all 32 published raw texts and scores each key against random keys of the same form and shuffled digits;
`search_*.py` recover the keys without prior knowledge (Gongmi exactly; Rongmi up to one carry; Chenmi's page table compared with
the zero-free countdown). The final manual steps (Rongmi “90 = 00”, Chenmi page rule and “9 = 10”) are described on the site’s
Method page. Corrections and counter-checks are welcome.
