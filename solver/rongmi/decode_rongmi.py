#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Décodeur 容密 (juin 1916) — clé reconstruite en octobre 2026 (Brice Dudout, avec Claude).

Lecture des feuillets : colonnes de droite à gauche, chiffres de haut en bas, groupes de 4 chiffres ;
le préfixe public 1369 1378 (容密) reste en clair. Pour chaque groupe C :
  1. remplacer chaque chiffre selon la table de son rang (SIGMA ci-dessous) ;
  2. P = (σ(C) + 0901) mod 10000, addition ordinaire avec retenues ;
  3. P est le numéro du caractère dans le code télégraphique chinois (CTC).
Aucun groupe ne commence par 00 : le chiffreur écrit 90 (d'où 9 -> 0 aux milliers).

Usage : python3 decode_rongmi.py 2081 4874 ...          -> numéros CTC
        python3 decode_rongmi.py --table ctc.tsv 2081    -> caractères (fichier « code<TAB>caractère »)
"""
import sys

K = 901
SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 9, 0],  # milliers
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # centaines
    [0, 1, 9, 8, 2, 7, 6, 5, 4, 3],  # dizaines
    [9, 8, 0, 1, 7, 2, 3, 4, 5, 6],  # unités
]

def decode(group):
    """'2081' -> 2949 ; None si le groupe n'est pas formé de 4 chiffres."""
    if len(group) != 4 or not group.isdigit():
        return None
    return (sum(SIGMA[j][int(group[j])] * w for j, w in enumerate((1000, 100, 10, 1))) + K) % 10000

if __name__ == '__main__':
    args = sys.argv[1:]
    table = None
    if args[:1] == ['--table']:
        table = dict(l.rstrip('\n').split('\t')[:2] for l in open(args[1], encoding='utf-8') if '\t' in l)
        args = args[2:]
    out = []
    for g in args:
        p = decode(g)
        out.append('?' if p is None else (table.get(f'{p:04d}', '□') if table else f'{p:04d}'))
    print(('' if table else ' ').join(out))
