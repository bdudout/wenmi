#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporte le second canal (grille Y0) pour le décodeur : unités, codes, caractères, codes douteux.
Lit le corpus v6 (lectures humaines) du dossier d'enquête, décode sous Y0 (aucun paramètre), puis vérifie que le texte
obtenu est identique à working/c31-decodage-Y0-v6.md. Écrit assets/js/messages-y0.js.
Usage : python3 tools/build_data_y0.py <chemin du dossier d'enquête wenmi>"""
import json, os, re, sys
WENMI = os.path.abspath(sys.argv[1]); C31 = os.path.join(WENMI, 'cryptanalysis', 'c31')
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c14')); sys.path.insert(0, C31); os.environ.setdefault('C14_LM', 'lm3')
os.chdir(C31)
import numpy as np
from fx_job import LM, code2ch
from grid_y0 import Y0
uni = np.fromfile(os.path.join(LM, 'uni.f32'), dtype=np.float32); REF = float(uni.mean()); cm = code2ch()
# Corpus v6 : lectures humaines de Brice (lots 10–14, 17, 18, R1) ; formulaires a+b mis bout à bout, comme dans c31-decodage-Y0-v6.md.
v3 = json.load(open(os.path.join(C31, 'c31-ychannel-human-v6.json'), encoding='utf-8'))
v3 = v3.get('messages', v3)
MERGE = {'0413': ['0413a', '0413b'], '0416a': ['0416a'], '0449': ['0449a', '0449b'], '0455a': ['0455a'], '0467': ['0467a', '0467b'],
         '0473': ['0473a', '0473b'], '0489a': ['0489a'], '0494a': ['0494a'], '0496a': ['0496a'], '0498': ['0498a', '0498b']}
msgs = {m: [u for part in parts for u in v3[part]] for m, parts in MERGE.items()}
assert set(p for ps in MERGE.values() for p in ps) <= set(v3), 'formulaires non couverts'

ref = {}
for m, txt in re.findall(r'^## (\S+) .*?\n\n(\S+)\n', open(os.path.join(WENMI, 'working', 'c31-decodage-Y0-v6.md'), encoding='utf-8').read(), re.M):
    if m in MERGE: ref[m] = txt

out = []
for m, us in msgs.items():
    if m not in ref: continue
    units, codes, chars, doubt = [], [], [], []
    for i in range(0, len(us) - 1, 2):
        a, b = us[i], us[i + 1]
        units += [a, b]
        if a not in Y0 or b not in Y0 or Y0[a] > 99 or Y0[b] > 99:
            codes.append('····'); chars.append('·'); doubt.append(len(chars) - 1); continue
        c = Y0[a] * 100 + Y0[b]; codes.append('%04d' % c); chars.append(cm.get('%04d' % c, '□'))
        if float(uni[c]) - REF < 1: doubt.append(len(chars) - 1)
    rebuilt = ''.join(('‹%s›' % ch) if (k in doubt and ch != '·') else ch for k, ch in enumerate(chars))
    assert rebuilt == ref[m], (m, rebuilt, ref[m])
    out.append({'id': m, 'grid': 'Y0', 'units': units, 'codes': codes, 'chars': chars, 'doubt': doubt})
# relecture ciblée des codes douteux (Brice, 13/10/2026), appliquée après la vérification contre l'édition
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dx_overrides
DX = dx_overrides.load(WENMI)
for o in out:
    for i, (old, new) in DX.get(('wenmi', o['id']), {}).items():
        assert ''.join(o['units'][2 * i:2 * i + 2]) == old, (o['id'], i, old)
        o['units'][2 * i:2 * i + 2] = [new[:2], new[2:]]; c = Y0[new[:2]] * 100 + Y0[new[2:]]
        print('DX :', o['id'], i, old, '→', new, o['chars'][i], '→', cm.get('%04d' % c, '□'))
        o['codes'][i] = '%04d' % c; o['chars'][i] = cm.get('%04d' % c, '□')
        o['doubt'] = sorted([k for k in o['doubt'] if k != i] + ([i] if float(uni[c]) - REF < 1 else []))
missing = set(ref) - {o['id'] for o in out}
assert not missing, missing
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'js', 'messages-y0.js')
open(dst, 'w', encoding='utf-8').write('// Généré par tools/build_data_y0.py — ne pas éditer à la main.\nwindow.WENMI_MESSAGES_Y0 = '
                                       + json.dumps(out, ensure_ascii=False) + ';\n')
print(len(out), 'messages Y0 :', ', '.join('%s (%d)' % (o['id'], len(o['codes'])) for o in out), '| total', sum(len(o['codes']) for o in out), 'codes')
