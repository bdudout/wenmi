# Publication du lot 1915 — 16 octobre 2026

Paquet de Claude, relu par Brice (R23 puis R24), appliqué sans retraduire ni corriger les textes chinois : `tools/data/publication-1915.json`. Le paquet de travail reste dans `wenmi/cryptanalysis/c35/v877/publication-codex.json`.

- Neuf condensateurs ajoutés, de mars à octobre 1915 : corpus désormais de **20 télégrammes, 446 codes, 53 caractères douteux et 1 illisible**, dont 188 codes et 21 caractères marqués dans les neuf ajouts. Les onze anciennes entrées représentent 258 codes et 32 caractères douteux ; le compteur 28 de l’ancien accueil était obsolète.
- Deux Rosamonde des 6 et 7 mars : **22 télégrammes** au total, 15 dans le tableau 1915 et 7 dans celui de 1916. Traductions du paquet conservées ; ancienne estimation de 45 corrections sur 750 lettres explicitement rattachée à l’échantillon initial.
- Les 9 nouveaux décodages bruts, dates, heures, pages et étiquettes concordent exactement avec le paquet. Les 11 objets de messages antérieurs et les 20 anciennes lignes Rosamonde ont été comparés au commit précédent : textes inchangés.
- Vue **0274 = page 52**, malgré les sauts de numérotation après la page 50 de B03050087700. Correspondance corrigée dans les deux builds de données et d’images. Vues 0233a et 0233b distinctes ; les deux fiches partagent le scan de la page 13.
- Shanghai et San Francisco sont rattachées au classement existant ; les plages de dates sont étendues à juin et octobre 1915. Thirtieth couvre février–mai. Cartes et scans reconstruits par les outils existants.

## Demandes complémentaires de Brice

La partie Méthode définit explicitement Sixteenth, Seventeenth et Hsuweilin (alphabets complets, indices de départ zéro, formules, concaténation des demi-codes et exemples), Hong Kong (lettre → chiffre), critères de sélection, distinction transcription/recalage, R23/R24 et la particularité qq/[pp] de Rosamonde. Aucun nouveau solveur n’est revendiqué pour l’édition de 1915.

L’Histoire comporte une nouvelle section politique et militaire 1913–1916, avec liens vers les messages : réseaux de financement, arbitrages de dépenses et fonds navals, offre de rapprochement Kang/Liang, coordination de mars 1916 et Long Jiguang, projets navals/arsenal/江陰 d’avril, conditions des prêts et prudence vis-à-vis des relations japonaises, retour annoncé de Sun et répartition Tokyo/Yokohama. Les annonces et projets ne sont pas présentés comme des opérations réalisées. L’apparition de 介石 en avril ne sert pas à identifier Kai en 1914.

Ces ajouts, les comptes et les interfaces sont dans les cinq langues. Les deux Eighteenth, les fragments non retenus et les clairs Irliegon restent locaux ; aucun contenu supplémentaire de juin 1917.

## Rejouer

```sh
python3 tools/build_t1915.py ../wenmi
python3 tools/make_fiches_t1915.py ../wenmi <ne_110m_land.geojson>
python3 ../wenmi/cryptanalysis/c35/site/persons.py .
python3 tools/build.py
python3 tools/check_editorial_visuals.py
python3 tools/check_rosamonde_illustrations.py
```

Les dictionnaires de `gen_t1915.py` ont été mis à jour sans exécuter ce générateur. `persons.py` doit être lancé après l’insertion des deux lignes Rosamonde ; il attend 15 lignes en 1915. Les traductions des télégrammes n’ont pas été refaites pour enrichir les articles : l’analyse renvoie aux textes avec leurs réserves.
