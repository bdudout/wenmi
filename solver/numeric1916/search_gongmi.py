#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recherche sans a priori de la clé 共密 dans la famille « dizaines permutées puis P = (K − C') mod 10000 ».
Pour chacune des 10 000 valeurs de K, la permutation des dizaines optimale (unigramme) est calculée exactement ;
les 20 meilleurs K sont reclassés au score complet. Témoins : même recherche sur les chiffres mélangés.
  python3 search_gongmi.py [--nulls 5]          (quelques secondes par recherche)"""
import argparse
import numpy as np
import common as C, search_common as S

def search(msgs):
    g = np.array([int(x) for m in msgs for x in m]); t = g // 10 % 10; base = g - 10 * t
    Ks = np.arange(10000)[:, None]; M = np.zeros((10000, 10, 10))
    for v in range(10):
        sc = C.U[(Ks - (base + 10 * v)[None, :]) % 10000]          # 10000 × n
        for tt in range(10): M[:, tt, v] = sc[:, t == tt].sum(1)
    uni = []
    for K in range(10000):
        col = S.assign_max(M[K])
        uni.append((M[K][range(10), col].sum(), K, col))
    uni.sort(reverse=True); best = None
    for _, K, col in uni[:20]:
        dec = lambda x, K=K, col=col: (K - (int(x) - 10 * (int(x) // 10 % 10) + 10 * col[int(x) // 10 % 10])) % 10000
        s = C.score([[dec(x) for x in m] for m in msgs])
        if best is None or s > best[0]: best = (s, K, col, dec)
    return best

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); ap.add_argument('--nulls', type=int, default=5); a = ap.parse_args()
    msgs = [[x for x in C.ciphers(m) if x.isdigit()] for m in C.messages('gongmi').values()]
    s, K, col, dec = search(msgs)
    print(f'réel : score {s:.3f}, K = {K:04d}, dizaines {col}  (clé publiée : K = 9000, {list(C.PHI)})')
    print('début de N17 :', ''.join(C.glyph(dec(x)) for x in msgs[list(C.messages("gongmi")).index("N17")][:40]))
    nul = [search(S.shuffle_digits(msgs, 100 + i))[0] for i in range(a.nulls)]
    print('témoins (chiffres mélangés) :', ' '.join(f'{x:.3f}' for x in nul))
