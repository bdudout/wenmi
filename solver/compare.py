#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lit la sortie d'anchor_coord, compare la meilleure table à la grille G0, et décode le message tenu à l'écart (0406)
avec la table trouvée puis avec G0.

    python3 compare.py out.tsv

Brice Dudout, avec Claude (Anthropic), 2026 — CC BY 4.0."""
import json, os, sys
from wenmi import GRIDS, decode, score

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    lines = open(sys.argv[1]).read().splitlines()
    types = lines[0].split('\t')[1:]
    rows = [l.split('\t') for l in lines[1:]]
    best = {t: int(v) for t, v in zip(types, rows[0][2:])}
    G0 = GRIDS['G0']
    diff = sorted((t, best[t], G0[t]) for t in types if best[t] != G0[t])
    print('meilleur score : %s (second : %s)' % (rows[0][0], rows[1][0] if len(rows) > 1 else '—'))
    print('cases identiques à G0 : %d / 100' % (100 - len(diff)))
    if diff: print('différences (syllabe, trouvé, G0) :', ' '.join('%s %02d/%02d' % d for d in diff))
    held = json.load(open(os.path.join(HERE, 'data', 'cen_v8.json'), encoding='utf-8'))['messages']['0406']
    for lab, T in (('table trouvée', best), ('grille G0', G0)):
        codes = decode(held, T); s, n = score(codes)
        print('0406 sous %-13s : %+.2f/code  %s' % (lab, s, ''.join(ch for _, ch in codes)))


if __name__ == '__main__':
    main()
