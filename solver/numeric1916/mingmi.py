#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les trois clés comme renumérotations d'un livre 明密 (reformulation de S. Tomokiyo, Cryptiana, 23/10/2026).

Dans le livre CTC, le code X est à la page (X-1)//100, colonne ((X-1)%100)//10, ligne (X-1)%10 + 1 : chaque
colonne contient xxx1…xxx9 puis xxx0 en bas (le 0 de la dizaine suivante). Ce script vérifie, pour chacune
des 10 000 valeurs de groupe, que chaque clé publiée se factorise en
    page = f(deux premiers chiffres)  ·  colonne = g(dizaine)  ·  ligne = h(unité)
sans aucune retenue résiduelle, et imprime f, g, h.
Usage : python3 mingmi.py"""
from collections import defaultdict
import common as C

KEYS = (('gongmi', '共密', C.decode_gongmi), ('rongmi', '容密', C.decode_rongmi), ('chenmi', '辰密', C.decode_chenmi))


def layout(p):
    y = (p - 1) % 10000
    return y // 100, (y % 100) // 10, y % 10 + 1


def factorize(dec):
    """-> (pages {écrit: page}, colonnes {chiffre: colonne}, lignes {chiffre: ligne}, non définis) ; lève si non factorisable."""
    f, g, h = defaultdict(set), defaultdict(set), defaultdict(set)
    undefined = 0
    for x in range(10000):
        s = f'{x:04d}'
        p = dec(s)
        if p is None:
            undefined += 1
            continue
        page, col, row = layout(p)
        f[s[:2]].add(page); g[int(s[2])].add(col); h[int(s[3])].add(row)
    for d in (f, g, h):
        bad = {k: v for k, v in d.items() if len(v) > 1}
        if bad: raise ValueError(f'non factorisable : {bad}')
    one = lambda d: {k: next(iter(v)) for k, v in sorted(d.items())}
    return one(f), one(g), one(h), undefined


if __name__ == '__main__':
    for key, name, dec in KEYS:
        f, g, h, und = factorize(dec)
        print(f'{name} ({key}) : factorisable sur les {10000 - und} groupes définis')
        print('  colonne :', ' '.join(f'{d}→{g[d]}' for d in range(10)))
        print('  ligne   :', ' '.join(f'{d}→{h[d]}' for d in range(10)))
        print('  pages   :', ' '.join(f'{w}→{f[w]:02d}' for w in sorted(f) if w[1] in '019'))
