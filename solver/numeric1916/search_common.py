# -*- coding: utf-8 -*-
"""Outils des recherches de clé : affectation exacte (algorithme hongrois), témoins par mélange des chiffres."""
import random
import numpy as np

def assign_max(M):
    """Affectation maximisant sum M[i, col[i]] (Kuhn-Munkres, O(n³)) ; renvoie col."""
    a = -np.asarray(M, float); n = a.shape[0]; INF = 1e18
    u = [0.] * (n + 1); v = [0.] * (n + 1); p = [0] * (n + 1); way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i; j0 = 0; minv = [INF] * (n + 1); used = [False] * (n + 1)
        while True:
            used[j0] = True; i0 = p[j0]; delta = INF; j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = a[i0 - 1, j - 1] - u[i0] - v[j]
                    if cur < minv[j]: minv[j] = cur; way[j] = j0
                    if minv[j] < delta: delta = minv[j]; j1 = j
            for j in range(n + 1):
                if used[j]: u[p[j]] += delta; v[j] -= delta
                else: minv[j] -= delta
            j0 = j1
            if p[j0] == 0: break
        while True:
            j1 = way[j0]; p[j0] = p[j1]; j0 = j1
            if j0 == 0: break
    col = [0] * n
    for j in range(1, n + 1): col[p[j] - 1] = j - 1
    return col

def shuffle_digits(msgs, seed):
    """Témoin : chaque rang de chiffre est mélangé entre tous les groupes (profil conservé, structure détruite)."""
    rng = random.Random(seed)
    cols = [[g[j] for m in msgs for g in m] for j in range(4)]
    for c in cols: rng.shuffle(c)
    out = []; k = 0
    for m in msgs:
        out.append([''.join(cols[j][k + i] for j in range(4)) for i in range(len(m))]); k += len(m)
    return out
