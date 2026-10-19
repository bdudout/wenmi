#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recherche sans a priori de la clé 容密 dans la famille « σ par rang, puis P = (σ(C) + K) mod 10000 avec retenues ».
Étape 1 (K = 0) : quatre substitutions de chiffres (une par rang), par recuit simulé sur l'unigramme.
Étape 2 : pour chacune des 10 000 valeurs de K, σ est reconstruite rang par rang (unités d'abord, retenues propagées)
par vote majoritaire pour reproduire le texte de l'étape 1 ; les meilleurs K sont reclassés au score complet, puis échanges. Témoins : même recherche sur les chiffres mélangés.
Ne modélise pas la règle « 90 = 00 » (ajoutée à la main d'après les groupes en 90xx).
  python3 search_rongmi.py [--nulls 3] [--starts 4]"""
import argparse, math, random
import numpy as np
import common as C, search_common as S
W = np.array([1000, 100, 10, 1])

def dec_all(D, s, K):
    return (sum(s[j][D[:, j]] * W[j] for j in range(4)) + K) % 10000

def anneal(D, rng, steps, s=None, K=0, compensated=False, T0=0.3, T1=0.003):
    s = [np.array(rng.sample(range(10), 10)) for _ in range(4)] if s is None else [x.copy() for x in s]
    cur = C.U[dec_all(D, s, K)].mean(); best = (cur, [x.copy() for x in s], K)
    for k in range(steps):
        T = T0 * (T1 / T0) ** (k / steps); j = rng.randrange(4); s2 = [x.copy() for x in s]; K2 = K
        if compensated and rng.random() < 0.3:
            a = rng.randrange(1, 10); kd = list(f'{K:04d}'); kd[j] = str((int(kd[j]) + a) % 10); K2 = int(''.join(kd)); s2[j] = (s2[j] - a) % 10
        else:
            x, y = rng.sample(range(10), 2); s2[j][x], s2[j][y] = s2[j][y], s2[j][x]
        v = C.U[dec_all(D, s2, K2)].mean()
        if v > cur or rng.random() < math.exp((v - cur) / T):
            s, K, cur = s2, K2, v
            if cur > best[0]: best = (cur, [x.copy() for x in s], K)
    return best

def rebuild(D, P1, K):
    """σ telle que (σ(C) + K) reproduise au mieux P1 (décodage de l'étape 1), rang par rang avec retenues."""
    s = [None] * 4; carry = np.zeros(len(D), dtype=int); kd = [int(c) for c in f'{K:04d}']; agree = 0
    for j in (3, 2, 1, 0):
        target = P1 // W[j] % 10; sj = np.zeros(10, dtype=int)
        for d in range(10):
            m = D[:, j] == d
            if m.any():
                need = (target[m] - kd[j] - carry[m]) % 10; v = np.bincount(need, minlength=10); sj[d] = v.argmax(); agree += v.max()
        s[j] = sj; tot = sj[D[:, j]] + kd[j] + carry; carry = tot // 10
    return agree, s

def search(msgs, seed, starts):
    rng = random.Random(seed); D = np.array([[int(c) for c in x] for m in msgs for x in m])
    st1 = max((anneal(D, rng, 60000) for _ in range(starts)), key=lambda b: b[0])
    P1 = dec_all(D, st1[1], 0)
    cand = sorted((rebuild(D, P1, K) + (K,) for K in range(10000)), key=lambda r: -r[0])[:30]
    def full(s, K): return C.score([[int(v) for v in dec_all(np.array([[int(c) for c in x] for x in m]), s, K)] for m in msgs])
    sc, s, K = max(((full(s, K), s, K) for _, s, K in cand), key=lambda r: r[0])
    for _ in range(1500):
        j = rng.randrange(4); x, y = rng.sample(range(10), 2); s2 = [z.copy() for z in s]; s2[j][x], s2[j][y] = s2[j][y], s2[j][x]
        v = full(s2, K)
        if v > sc: sc, s = v, s2
    return sc, s, K, full(st1[1], 0)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--nulls', type=int, default=3); ap.add_argument('--starts', type=int, default=4); a = ap.parse_args()
    ms = C.messages('rongmi'); msgs = [[x for x in C.ciphers(m) if x.isdigit()] for m in ms.values()]
    sc, s, K, p4 = search(msgs, 1916, a.starts)
    print(f'étape 1 (4 substitutions, K = 0) : score {p4:.3f}')
    print(f'étape 2 : score {sc:.3f}, K = {K:04d}')
    for j, n in enumerate(('milliers', 'centaines', 'dizaines', 'unités')): print(f'  {n:9} {[int(v) for v in s[j]]}   publiée {C.SIGMA[j]}')
    i = list(ms).index('N02'); print('début de N02 :', ''.join(C.glyph(int(v)) for v in dec_all(np.array([[int(c) for c in x] for x in msgs[i]]), s, K))[:40])
    print('clé publiée :', f'{C.score([[C.decode_rongmi(x) for x in m] for m in msgs]):.3f}')
    nul = [search(S.shuffle_digits(msgs, 200 + i), 300 + i, a.starts)[0] for i in range(a.nulls)]
    print('témoins (chiffres mélangés) :', ' '.join(f'{x:.3f}' for x in nul))
