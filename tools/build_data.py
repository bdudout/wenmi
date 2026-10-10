#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrait de l'édition provisoire (working/c31-edition-wenmi.md) les unités, codes et caractères
de chaque télégramme, vérifie que la grille G0 redonne bien les codes, et écrit assets/js/messages.js.
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
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'js', 'messages.js')
open(dst, 'w', encoding='utf-8').write('// Généré par tools/build_data.py — ne pas éditer à la main.\nwindow.WENMI_MESSAGES = ' + json.dumps(out, ensure_ascii=False, indent=1) + ';\n')
print(len(out), 'messages :', ', '.join(f"{o['id']} ({len(o['codes'])} codes, {len(o['doubt'])} douteux)" for o in out))
