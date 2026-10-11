#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de structure SANS CLÉ (test « S3 » de l'enquête) : les consonnes et les voyelles se répartissent-elles
différemment selon la parité du rang de la syllabe dans le message ?

Un code télégraphique à quatre chiffres est coupé en deux moitiés ; chaque moitié devient une syllabe. Les syllabes de rang
pair portent donc la première moitié (milliers, centaines), très déséquilibrée dans le code chinois, et celles de rang
impair la seconde, à peu près uniforme. Si la CONSONNE porte la dizaine, ses fréquences différeront fortement entre rangs
pairs et impairs, et pas celles des voyelles. Statistique G (rapport de vraisemblance) ; nul par permutation des syllabes à
l'intérieur de chaque message. Aucun paramètre de clé n'intervient.

    python3 rank_test.py data/cen_v8.json [permutations]
    python3 rank_test.py data/yunnan_v3.json

Dérivé de s3_position.py (enquête C31, 9/10/2026). Brice Dudout, avec Claude (Anthropic), 2026 — CC BY 4.0."""
import collections, json, math, random, sys


def G(table):
    rows, cols, n = collections.Counter(), collections.Counter(), 0
    for (r, c), o in table.items(): rows[r] += o; cols[c] += o; n += o
    return sum(2 * o * math.log(o / (rows[r] * cols[c] / n)) for (r, c), o in table.items())


def tables(seqs):
    tc, tv = collections.Counter(), collections.Counter()
    for seq in seqs:
        for i, u in seq: tc[(u[0], i % 2)] += 1; tv[(u[1], i % 2)] += 1
    return G(tc), G(tv)


def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    msgs = json.load(open(sys.argv[1], encoding='utf-8'))['messages']
    nperm = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    seqs = [[(i, u) for i, u in enumerate(units) if u != '--'] for units in msgs.values()]
    obs = tables(seqs); rng = random.Random(31); null = ([], [])
    for _ in range(nperm):
        ps = []
        for seq in seqs:
            idx = [i for i, _ in seq]; us = [u for _, u in seq]; rng.shuffle(us); ps.append(list(zip(idx, us)))
        g = tables(ps); null[0].append(g[0]); null[1].append(g[1])
    for j, lab in enumerate(('consonnes', 'voyelles')):
        mu = sum(null[j]) / nperm; sd = (sum((x - mu) ** 2 for x in null[j]) / nperm) ** 0.5
        print('%-10s G = %8.2f   nul %7.2f ± %5.2f   z = %6.1f' % (lab, obs[j], mu, sd, (obs[j] - mu) / sd))
    even = collections.Counter(u[0] for seq in seqs for i, u in seq if i % 2 == 0)
    print('consonnes au rang pair (1re moitié du code) :', ' '.join('%s %d' % kv for kv in even.most_common()))


if __name__ == '__main__':
    main()
