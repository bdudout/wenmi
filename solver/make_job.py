#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare un fichier de travail pour anchor_coord (canal Tokyo → Zhaoqing) avec le jeu d'ancres « D » de l'enquête :
les fins de quatre télégrammes datés, lues comme « signature + rime du jour » d'après la date écrite sur le formulaire.

    0348  zo so = 漾 3363 (le 23)    0415  du su = 巧 1564 (le 18)
    0416b xi fa = 皓 4110 (le 19)    0455b ho yi = 元 0337 (le 13)

(L'ancre de 0416b contient l'erreur de copie e → i découverte ensuite : le solveur doit s'en accommoder.)
Le message 0406 est TENU À L'ÉCART : il n'entre pas dans le fichier ; on le décode après coup avec la table trouvée.

    python3 make_job.py job.txt            # données réelles
    python3 make_job.py job_null.txt null  # témoin nul : syllabes mélangées dans chaque message (fins conservées)

Brice Dudout, avec Claude (Anthropic), 2026 — CC BY 4.0."""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONS, VOW = 'bcdfghklmnpqrstvwxyz', 'aeiou'          # alphabet du canal : 20 consonnes × 5 voyelles = 100 syllabes
TYPES = [c + v for c in CONS for v in VOW]
ANCHORS = {'0348': ('zoso', '3363'), '0415': ('dusu', '1564'), '0416b': ('xifa', '4110'), '0455b': ('hoyi', '0337')}
HELD_OUT = '0406'


def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    out, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else 'real')
    msgs = json.load(open(os.path.join(HERE, 'data', 'cen_v8.json'), encoding='utf-8'))['messages']
    msgs = {m: u for m, u in msgs.items() if m != HELD_OUT}
    anc = {}
    for m, (pair, code) in ANCHORS.items():
        assert msgs[m][-2:] == [pair[:2], pair[2:]], (m, msgs[m][-2:])
        anc[pair[:2]] = int(code[:2]); anc[pair[2:]] = int(code[2:])
    if mode == 'null':
        rng = random.Random(900)
        for m, u in msgs.items():
            body, tail = u[:-4], u[-4:]; ev, od = body[0::2], body[1::2]; rng.shuffle(ev); rng.shuffle(od)
            b2 = [None] * len(body); b2[0::2] = ev; b2[1::2] = od; msgs[m] = b2 + tail
    with open(out, 'w') as f:
        f.write('LM %s\nTYPES %s\n' % (os.path.join(HERE, 'lm3'), ' '.join(TYPES)))
        for m, u in msgs.items(): f.write('MSG %s %s\n' % (m, ' '.join(u)))
        for u, v in anc.items(): f.write('ANCHOR %s %d\n' % (u, v))
    print('écrit', out, '—', len(msgs), 'messages,', len(anc), 'unités ancrées, 0406 tenu à l\'écart')


if __name__ == '__main__':
    main()
