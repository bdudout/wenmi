#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle indépendant des trois clés : (1) chaque télégramme publié est reproduit à l'identique à partir des chiffres
relus ; (2) le score du texte (modèle de langue lm/) sous la clé est comparé à deux familles de témoins :
  - clés aléatoires de même structure (mêmes formules, tables tirées au hasard),
  - chiffres mélangés rang par rang entre les groupes de la famille (même profil de chiffres, ordre détruit).
  python3 verify.py [--nulls 200] [--seed 1916]"""
import argparse, random
import common as C

def random_decoder(fam, rng):
    if fam == 'gongmi':
        phi = rng.sample(range(10), 10); k = rng.randrange(10000)
        return lambda g: None if not g.isdigit() else (k - (int(g) - 10 * (int(g) // 10 % 10) + 10 * phi[int(g) // 10 % 10])) % 10000
    if fam == 'rongmi':
        s = [rng.sample(range(10), 10) for _ in range(4)]; k = rng.randrange(10000)
        return lambda g: None if not g.isdigit() else (sum(s[j][int(g[j])] * w for j, w in enumerate((1000, 100, 10, 1))) + k) % 10000
    if fam == 'chenmi':
        pg = dict(zip(C.ZERO_FREE, rng.sample(range(100), len(C.ZERO_FREE)))); t = rng.sample(range(10), 10); u = rng.sample(range(10), 10)
        return lambda g: None if not g.isdigit() or int(g[:2]) not in pg else (100 * pg[int(g[:2])] + 10 * t[int(g[2])] + u[int(g[3])]) % 10000

def shuffled(msgs, rng):
    pos = [[g[j] for m in msgs for g in m if g.isdigit()] for j in range(4)]
    for p in pos: rng.shuffle(p)
    out = []; k = 0
    for m in msgs:
        mm = []
        for g in m:
            if g.isdigit(): mm.append(''.join(pos[j][k] for j in range(4))); k += 1
            else: mm.append(g)
        out.append(mm)
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--nulls', type=int, default=200); ap.add_argument('--seed', type=int, default=1916)
    a = ap.parse_args(); rng = random.Random(a.seed)
    allm = C.messages(); ok = 0; tot = 0
    for mid, m in allm.items():
        if m['family'] == 'open' or not m['raw_published']: continue
        tot += 1; ok += ''.join(C.glyph(x) for x in C.decode_message(m)) == m['raw_published']
    print(f'Reproduction des textes bruts publiés : {ok}/{tot}')
    print(f'{"famille":8} {"msgs":>4} {"codes":>5} {"score clé":>9} {"max clés aléa.":>14} {"max chiffres mélangés":>21}')
    for fam in ('gongmi', 'rongmi', 'chenmi'):
        ms = [C.ciphers(m) for m in C.messages(fam).values()]
        real = C.score([[C.DECODERS[fam](g) for g in m] for m in ms])
        rk = max(C.score([[f(g) for g in m] for m in ms]) for f in (random_decoder(fam, rng) for _ in range(a.nulls)))
        sh = max(C.score([[C.DECODERS[fam](g) for g in m] for m in shuffled(ms, rng)]) for _ in range(a.nulls))
        print(f'{fam:8} {len(ms):4} {sum(map(len, ms)):5} {real:9.3f} {rk:14.3f} {sh:21.3f}')
    print('Lecture : un score de clé très au-dessus des deux maxima de témoins indique un texte non dû au hasard.')
