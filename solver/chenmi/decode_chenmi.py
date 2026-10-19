#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Décodeur 辰密 (juin 1916) — clé reconstruite en octobre 2026 (Brice Dudout, avec Claude).

Lecture des feuillets : colonnes de droite à gauche, chiffres de haut en bas, groupes de 4 chiffres ;
le préfixe public 6591 1378 (辰密) reste en clair. Pour chaque groupe C = p1 p2 d u :
  1. page : rang de « p1p2 » dans le décompte des nombres sans zéro 99, 98, …, 91, 89, …, 11
     (99 -> page 00, 91 -> 08, 89 -> 09, 11 -> 80) ;
  2. P = 100 × page + 10 × T[d] + U[u], retenue ordinaire (U[9] = 10) ;
  3. P est le numéro du caractère dans le code télégraphique chinois (CTC).

Usage : python3 decode_chenmi.py 9950 4220 6219        -> 0001 5281 3500
        python3 decode_chenmi.py --table ctc.tsv 9950   -> caractères (fichier « code<TAB>caractère »)
"""
import sys

ZERO_FREE = [n for n in range(99, 10, -1) if '0' not in str(n)]
PAGE = {c: i for i, c in enumerate(ZERO_FREE)}
T = [3, 9, 8, 7, 1, 0, 2, 6, 4, 5]        # dizaines : chiffre lu -> chiffre du CTC
U = [1, 9, 5, 4, 3, 2, 6, 7, 8, 10]       # unités : 9 vaut 10 (retenue)

def decode(group):
    g = group.strip()
    if len(g) != 4 or not g.isdigit() or int(g[:2]) not in PAGE:
        raise ValueError(f'groupe 辰密 invalide : {group!r}')
    return 100 * PAGE[int(g[:2])] + 10 * T[int(g[2])] + U[int(g[3])]

if __name__ == '__main__':
    args = sys.argv[1:]; table = None
    if args[:1] == ['--table']:
        table = dict(l.rstrip('\n').split('\t')[:2] for l in open(args[1], encoding='utf-8') if '\t' in l); args = args[2:]
    out = [f'{decode(a):04d}' for a in args]
    print(' '.join(table.get(p, '□') for p in out) if table else ' '.join(out))
