#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Décoder des groupes ou un télégramme publié.

  python3 decode.py --key chenmi 9950 4220 6219      # 一興灰
  python3 decode.py --message N16                    # télégramme N16 avec sa clé
  python3 decode.py --list                           # liste des télégrammes et de leur clé"""
import argparse
import common as C

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--key', choices=sorted(C.DECODERS))
ap.add_argument('--message')
ap.add_argument('--list', action='store_true')
ap.add_argument('groups', nargs='*')
a = ap.parse_args()
if a.list:
    for mid, m in C.messages().items():
        print(f"{mid:5} {m['family']:7} {len(m['groups']):4} groupes  {m.get('date_note') or ''}")
elif a.message:
    m = C.messages()[a.message]
    if m['family'] == 'open':
        raise SystemExit(f"{a.message} n'est pas lu : {m['note']}")
    p = C.decode_message(m, a.key)
    print('préfixe :', m['prefix'] or '—')
    print(' '.join(f'{x:04d}' if x is not None else '????' for x in p))
    print(''.join(C.glyph(x) for x in p))
    if m['raw_published'] and not a.key:
        print('identique au texte brut publié :', ''.join(C.glyph(x) for x in p) == m['raw_published'])
    print('lecture publiée :', m['reading_published'])
else:
    p = [C.DECODERS[a.key or 'clair'](g) for g in a.groups]
    print(' '.join(f'{x:04d}' if x is not None else '????' for x in p)); print(''.join(C.glyph(x) for x in p))
