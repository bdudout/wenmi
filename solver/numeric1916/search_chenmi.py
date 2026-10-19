#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recherche sans a priori de la clé 辰密 dans la famille « page permutée + dizaines et unités permutées » :
P = 100·π(page) + 10·t(dizaine) + u(unité). t et u par recuit simulé sur un proxy unigramme (meilleure page CTC pour
chaque page chiffrée), π par affectation exacte, puis échanges au score complet. On compare ensuite π au décompte des
nombres sans zéro (99 → 00, 89 → 09…) et l'on teste la règle « unité 9 = 10 ». Témoins : queues mélangées.
  python3 search_chenmi.py [--nulls 3] [--anneals 6] [--jobs 4]      (≈ 1 h avec les réglages par défaut)"""
import argparse, math, random, concurrent.futures as cf
import numpy as np
import common as C, search_common as S
U3 = C.U[:10000].reshape(100, 10, 10)

def fit(msgs, seed, anneals, steps=200000):
    rng = random.Random(seed); G = np.array([int(g) for m in msgs for g in m]); P = G // 100; T = G // 10 % 10; N = G % 10
    u = np.unique(P); Pi = np.searchsorted(u, P); n = len(P)
    def proxy(a, b):
        M = np.zeros((len(u), 100)); np.add.at(M, Pi, U3[:, a[T], b[N]].T); return M.max(1).sum() / n
    best = None
    for _ in range(anneals):
        a = np.array(rng.sample(range(10), 10)); b = np.array(rng.sample(range(10), 10)); sc = proxy(a, b); bb = (sc, a.copy(), b.copy())
        for k in range(steps):
            t = 0.05 * 0.01 ** (k / steps); w = rng.random() < 0.5; x, y = rng.sample(range(10), 2)
            c = (a if w else b).copy(); c[x], c[y] = c[y], c[x]; s = proxy(c, b) if w else proxy(a, c)
            if s > sc or rng.random() < math.exp((s - sc) / t):
                sc = s; a, b = (c, b) if w else (a, c)
                if sc > bb[0]: bb = (sc, a.copy(), b.copy())
        if best is None or bb[0] > best[0]: best = bb
    _, st, su = best
    M = np.zeros((100, 100)); np.add.at(M, P, U3[:, st[T], su[N]].T); pi = np.array(S.assign_max(M))
    dec = lambda pi, st, su: [[int(pi[int(g) // 100] * 100 + st[int(g) // 10 % 10] * 10 + su[int(g) % 10]) for g in m] for m in msgs]
    sc = C.score(dec(pi, st, su))
    for _ in range(4000):
        k = rng.random(); p2, s2, u2 = pi.copy(), st.copy(), su.copy()
        if k < 0.7: x, y = rng.sample(range(100), 2); p2[x], p2[y] = p2[y], p2[x]
        elif k < 0.85: x, y = rng.sample(range(10), 2); s2[x], s2[y] = s2[y], s2[x]
        else: x, y = rng.sample(range(10), 2); u2[x], u2[y] = u2[y], u2[x]
        v = C.score(dec(p2, s2, u2))
        if v > sc: sc, pi, st, su = v, p2, s2, u2
    return sc, pi, st, su, dec(pi, st, su)

def job(args): return fit(*args)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--nulls', type=int, default=3); ap.add_argument('--anneals', type=int, default=6); ap.add_argument('--jobs', type=int, default=4); a = ap.parse_args()
    ms = C.messages('chenmi'); msgs = [C.ciphers(m) for m in ms.values()]
    nulls = []
    for i in range(a.nulls):
        flat = [g for m in msgs for g in m]; tails = [g[2:] for g in flat]; random.Random(500 + i).shuffle(tails); it = iter(tails)
        nulls.append([[g[:2] + next(it) for g in m] for m in msgs])
    with cf.ProcessPoolExecutor(max_workers=a.jobs) as ex:
        res = list(ex.map(job, [(msgs, 11, a.anneals)] + [(nm, 20 + i, a.anneals) for i, nm in enumerate(nulls)]))
    sc, pi, st, su, dec = res[0]
    used = sorted({int(g[:2]) for m in msgs for g in m})
    rule = sum(pi[c] == C.PAGE[c] for c in used)
    print(f'réel : score {sc:.3f} ; dizaines {list(map(int, st))} (publiée {C.T_CHEN}) ; unités {list(map(int, su))} (publiée {C.U_CHEN})')
    print(f'pages trouvées conformes au décompte sans zéro : {rule}/{len(used)} pages utilisées')
    for mid, d in zip(ms, dec): print(f'  {mid} :', ''.join(C.glyph(x) for x in d)[:50])
    rule_dec = [[100 * C.PAGE[int(g[:2])] + 10 * int(st[int(g[2])]) + int(su[int(g[3])]) for g in m] for m in msgs]
    su10 = su.copy(); su10[list(su).index(0)] = 10 if 0 in su else su10[0]
    rule10 = [[100 * C.PAGE[int(g[:2])] + 10 * int(st[int(g[2])]) + int(su10[int(g[3])]) for g in m] for m in msgs]
    print(f'avec la règle de pages imposée : {C.score(rule_dec):.3f} ; et l’unité qui donnait 0 valant 10 : {C.score(rule10):.3f} ; clé publiée : {C.score([[C.decode_chenmi(g) for g in m] for m in msgs]):.3f}')
    print('témoins (queues mélangées) :', ' '.join(f'{r[0]:.3f}' for r in res[1:]))
