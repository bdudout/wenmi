# -*- coding: utf-8 -*-
"""Lettres relues par Brice Dudout sur les scans (relecture ciblée des codes douteux, 13/10/2026) : corrections lettre à lettre,
appliquées par chaque build sur le flux de lettres du télégramme. Source : wenmi/cryptanalysis/douteux/dx_corrections.json
(code i = lettres 4i…4i+3 ; ancien → nouveau, vérifié avant application)."""
import json, os

def load(wenmi):
    out = {}
    for c in json.load(open(os.path.join(wenmi, 'cryptanalysis', 'douteux', 'dx_corrections.json'), encoding='utf-8')):
        out.setdefault((c['corpus'], c['id']), {})[c['i']] = (c['old'], c['new'])
    return out

def apply_stream(s, ov, label=''):
    """Applique les corrections {i: (ancien, nouveau)} à un flux de lettres (code i = s[4i:4i+4])."""
    s = list(s)
    for i, (old, new) in sorted(ov.items()):
        assert ''.join(s[4 * i:4 * i + 4]) == old, (label, i, ''.join(s[4 * i:4 * i + 4]), old)
        s[4 * i:4 * i + 4] = new
    return ''.join(s)
