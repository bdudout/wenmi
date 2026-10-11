#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wenmi (文密, 1916) — les deux clés retrouvées, le décodage et le score par le modèle de langue.

    python3 wenmi.py decode cen        # canal Tokyo → Zhaoqing, clé G0
    python3 wenmi.py decode yunnan     # canal Tokyo ↔ Yunnan, clé Y0
    python3 wenmi.py grid G0|Y0        # affiche la grille

Brice Dudout, avec Claude (Anthropic), 2026 — CC BY 4.0. Nécessite NumPy."""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LM = os.path.join(HERE, 'lm3')


def g0():
    """Canal Tokyo → Zhaoqing. 20 consonnes dans l'ordre alphabétique inversé depuis h, deux par dizaine ;
    voyelles a e i o u montantes pour la 1re consonne de la dizaine, descendantes pour la 2e (serpentin)."""
    C, V = 'hgfdcbzyxwvtsrqpnmlk', 'aeiou'
    return {c + v: 10 * (i // 2) + (j if i % 2 == 0 else 9 - j) for i, c in enumerate(C) for j, v in enumerate(V)}


def y0():
    """Canal Tokyo ↔ Yunnan. 17 consonnes dans l'ordre alphabétique sans c, j, q ; 6 voyelles en serpentin ;
    valeur = 6 × rang de la consonne + rang de la voyelle (ze = 100 et za = 101 inemployées)."""
    C = 'bdfghklmnprstvwxz'
    return {c + v: 6 * i + r for i, c in enumerate(C) for r, v in enumerate('yuoiea' if i % 2 == 0 else 'aeiouy')}


GRIDS = {'G0': g0(), 'Y0': y0()}
uni = np.fromfile(os.path.join(LM, 'uni.f32'), dtype=np.float32)
REF = float(uni.mean())
BI = dict(zip(np.fromfile(os.path.join(LM, 'bi.u32'), dtype=np.uint32).tolist(), np.fromfile(os.path.join(LM, 'bi.f32'), dtype=np.float32).tolist()))
BDEF = float(np.fromfile(os.path.join(LM, 'bidef.f32'), dtype=np.float32)[0])
CODE2CH = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(LM, 'code2ch.tsv'), encoding='utf-8'))


def decode(units, T):
    """Unités (syllabes) → liste de (code, caractère). Deux syllabes = un code à 4 chiffres."""
    out = []
    for i in range(0, len(units) - 1, 2):
        a, b = units[i], units[i + 1]
        if a not in T or b not in T or T[a] > 99 or T[b] > 99:
            out.append(('····', '·')); continue
        c = '%02d%02d' % (T[a], T[b]); out.append((c, CODE2CH.get(c, '□')))
    return out


def score(codes):
    """Gain moyen de log-vraisemblance par code (unigramme − moyenne + bigrammes) : > 0 si le texte « sonne » chinois."""
    tot, n, prev = 0.0, 0, None
    for c, _ in codes:
        if not c.isdigit(): prev = None; continue
        k = int(c); tot += float(uni[k]) - REF; n += 1
        if prev is not None: tot += BI.get(prev * 10000 + k, BDEF)
        prev = k
    return tot / max(n, 1), n


def show(units, T, label):
    codes = decode(units, T); s, n = score(codes)
    text = ''.join(ch if (c.isdigit() and float(uni[int(c)]) - REF >= 1) or not c.isdigit() else '‹%s›' % ch for c, ch in codes)
    print('%-6s %+.2f/code (n=%d)  %s' % (label, s, n, text))


def main():
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    if sys.argv[1] == 'grid':
        T = GRIDS[sys.argv[2]]
        for k, v in sorted(T.items(), key=lambda kv: kv[1]): print(k, '%02d' % v if v < 100 else '—')
        return
    which = sys.argv[2]
    if which == 'cen':
        msgs = json.load(open(os.path.join(HERE, 'data', 'cen_v8.json'), encoding='utf-8'))['messages']
        for m, u in msgs.items(): show(u, GRIDS['G0'], m)
    elif which == 'yunnan':
        forms = json.load(open(os.path.join(HERE, 'data', 'yunnan_v3.json'), encoding='utf-8'))['messages']
        merged = {}
        for f in sorted(forms):
            base = f[:-1] if f[-1] in 'ab' and (f[:-1] + 'a') in forms and (f[:-1] + 'b') in forms else f
            merged.setdefault(base, []).extend(forms[f])
        for m, u in merged.items(): show(u, GRIDS['Y0'], m)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
