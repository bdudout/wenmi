#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrait de l'édition provisoire (working/c31-edition-wenmi.md) les unités, codes et caractères
de chaque télégramme, vérifie que la grille G0 redonne bien les codes, et écrit assets/js/messages.js.
Les unités sont ensuite mises à jour depuis le corpus de référence Cen v9 (c31-consensus-corpus-v9.json, mêmes dossiers) :
seuls les codes listés dans ses v9_changes peuvent différer de l'édition (0348 code 36 乞, 0386 code 26 準, relus au lot R1).
Usage : python3 tools/build_data.py <chemin vers c31-edition-wenmi.md>"""
import json, re, sys, os
ORDER, V = 'hgfdcbzyxwvtsrqpnmlk', 'aeiou'
G0 = {c + v: 10 * (i // 2) + (j if i % 2 == 0 else 9 - j) for i, c in enumerate(ORDER) for j, v in enumerate(V)}
src = open(sys.argv[1], encoding='utf-8').read()
out = []
for block in re.split(r'\n## ', src)[1:]:
    head = block.split('\n', 1)[0]
    m = re.match(r'(\d{4}[a-z]?) — (.*)', head)
    if not m: continue
    get = lambda k: re.search(r'- ' + k + r' : `([^`]*)`', block)
    units, codes = get('unités').group(1).split(), get('codes').group(1).split()
    text = re.search(r'\*\*texte\*\* : (\S+)', block).group(1)
    chars = [(mm.group(1) or mm.group(2), mm.group(1) is not None) for mm in re.finditer(r'‹(.)›|(.)', text)]
    assert len(units) == 2 * len(codes), (m.group(1), len(units), len(codes))
    assert len(chars) == len(codes), (m.group(1), len(chars), len(codes))
    bad = [i for i in range(len(codes)) if '%02d%02d' % (G0[units[2*i]], G0[units[2*i+1]]) != codes[i]]
    assert not bad, (m.group(1), bad)
    out.append({'id': m.group(1), 'units': units, 'codes': codes,
                'chars': [c for c, _ in chars], 'doubt': [i for i, (_, d) in enumerate(chars) if d]})
WENMI = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[1])))
v9 = json.load(open(os.path.join(WENMI, 'cryptanalysis', 'c31', 'c31-consensus-corpus-v9.json'), encoding='utf-8'))
LM = os.path.join(WENMI, 'cryptanalysis', 'c14', 'lm3')
C2CH = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(LM, 'code2ch.tsv'), encoding='utf-8'))
import numpy as np
uni = np.fromfile(os.path.join(LM, 'uni.f32'), dtype=np.float32); REF = float(uni.mean())
for o in out:
    us = v9['messages'].get(o['id'])
    if us is None: continue
    assert len(us) == len(o['units']), o['id']
    for i in range(len(o['codes'])):
        if us[2 * i:2 * i + 2] == o['units'][2 * i:2 * i + 2]: continue
        c = '%02d%02d' % (G0[us[2 * i]], G0[us[2 * i + 1]])
        print('v9 :', o['id'], i, o['units'][2 * i:2 * i + 2], '→', us[2 * i:2 * i + 2], o['chars'][i], '→', C2CH[c])
        o['units'][2 * i:2 * i + 2] = us[2 * i:2 * i + 2]; o['codes'][i] = c; o['chars'][i] = C2CH[c]
        o['doubt'] = [k for k in o['doubt'] if k != i] + ([i] if float(uni[int(c)]) - REF < 1 else [])
        o['doubt'].sort()
# relecture ciblée des codes douteux (Brice, 13/10/2026) : lettres corrigées sur le scan
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dx_overrides
DX = dx_overrides.load(WENMI)
for o in out:
    for i, (old, new) in DX.get(('wenmi', o['id']), {}).items():
        assert ''.join(o['units'][2 * i:2 * i + 2]) == old, (o['id'], i, o['units'][2 * i:2 * i + 2], old)
        o['units'][2 * i:2 * i + 2] = [new[:2], new[2:]]; c = '%02d%02d' % (G0[new[:2]], G0[new[2:]])
        print('DX :', o['id'], i, old, '→', new, o['chars'][i], '→', C2CH[c])
        o['codes'][i] = c; o['chars'][i] = C2CH[c]
        o['doubt'] = sorted([k for k in o['doubt'] if k != i] + ([i] if float(uni[int(c)]) - REF < 1 else []))
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'js', 'messages.js')
open(dst, 'w', encoding='utf-8').write('// Généré par tools/build_data.py — ne pas éditer à la main.\nwindow.WENMI_MESSAGES = ' + json.dumps(out, ensure_ascii=False, indent=1) + ';\n')
print(len(out), 'messages :', ', '.join(f"{o['id']} ({len(o['codes'])} codes, {len(o['doubt'])} douteux)" for o in out))
