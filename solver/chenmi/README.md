# 辰密 — décodeur

Clé des télégrammes 辰密 de juin 1916 (dossiers JACAR B03050089200–B03050089400 : N05, N13, N16, N26), reconstruite en octobre 2026.
Voir la page « 辰密 » du site pour les tables, les télégrammes, les lectures probables et les réserves.

```
python3 decode_chenmi.py 9950 4220 6219      # -> 0001 5281 3500 (一 興 灰) en numéros CTC
python3 decode_chenmi.py --table ctc.tsv 9950
```

Pages : décompte à rebours des nombres sans zéro (99 = page 00, 89 = page 09…) ; dizaines 0–9 → 3 9 8 7 1 0 2 6 4 5 ;
unités 0–9 → 1 9 5 4 3 2 6 7 8 10 (9 vaut 10). Clé reconstruite, pas retrouvée dans un livre de code historique.
Licence CC BY 4.0 (voir LICENSE à la racine).
