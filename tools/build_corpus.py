#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corpus complet des télégrammes 文密 pour la page « Télégrammes » : lettres lues, codes, caractères, statut de chaque
code, et extrapolation des erreurs pour les codes douteux.

Extrapolation (conjecture, jamais substituée au texte) : pour chaque code douteux, on essaie toutes les variantes qui
changent UNE lettre de ses quatre lettres, selon deux mécanismes d'erreur :
  - Morse : la lettre transmise diffère d'un seul signe (point/trait en trop, en moins, ou inversé) ;
  - copie : paire de lettres que les copistes japonais confondent (relevées à l'image pendant l'enquête).
La variante doit donner une syllabe valide de la grille. Elle est notée par le modèle de langue (unigramme du code
+ bigrammes avec ses voisins) ; seules celles qui améliorent nettement le score sont retenues (au plus trois).

Entrées (dossier d'enquête) : assets/js/messages.js et messages-y0.js (générés), modèle de langue lm3,
lecture humaine de 0509a (lot 8). Sortie : assets/js/corpus.js.
Usage : python3 tools/build_corpus.py <chemin du dossier d'enquête wenmi>"""
import json, os, re, sys
import numpy as np

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1])
LM = os.path.join(WENMI, 'cryptanalysis', 'c14', 'lm3')

# ---- grilles
def g0():
    C, V = 'hgfdcbzyxwvtsrqpnmlk', 'aeiou'
    return {c + v: 10 * (i // 2) + (j if i % 2 == 0 else 9 - j) for i, c in enumerate(C) for j, v in enumerate(V)}
def y0():
    C = 'bdfghklmnprstvwxz'
    return {c + v: 6 * i + r for i, c in enumerate(C) for r, v in enumerate('yuoiea' if i % 2 == 0 else 'aeiouy')}
GRIDS = {'G0': g0(), 'Y0': y0()}

# ---- modèle de langue
uni = np.fromfile(os.path.join(LM, 'uni.f32'), dtype=np.float32); REF = float(uni.mean())
BI = dict(zip(np.fromfile(os.path.join(LM, 'bi.u32'), dtype=np.uint32).tolist(), np.fromfile(os.path.join(LM, 'bi.f32'), dtype=np.float32).tolist()))
BDEF = float(np.fromfile(os.path.join(LM, 'bidef.f32'), dtype=np.float32)[0])
C2CH = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(LM, 'code2ch.tsv'), encoding='utf-8'))
def bi(a, b): return 0.0 if a is None or b is None else BI.get(a * 10000 + b, BDEF)
def local(prev, c, nxt): return float(uni[c]) - REF + bi(prev, c) + bi(c, nxt)

# ---- mécanismes d'erreur
MORSE = dict(a='.-', b='-...', c='-.-.', d='-..', e='.', f='..-.', g='--.', h='....', i='..', j='.---', k='-.-', l='.-..',
             m='--', n='-.', o='---', p='.--.', q='--.-', r='.-.', s='...', t='-', u='..-', v='...-', w='.--', x='-..-',
             y='-.--', z='--..')
def lev1(a, b):
    if a == b or abs(len(a) - len(b)) > 1: return False
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) == 1
    s, l = (a, b) if len(a) < len(b) else (b, a)
    return any(l[:k] + l[k + 1:] == s for k in range(len(l)))
MORSE_NB = {x: {y for y in MORSE if lev1(MORSE[x], MORSE[y])} for x in MORSE}
# confusions de copie relevées à l'image pendant l'enquête (journal, lots de lecture)
COPY_PAIRS = ['gq', 'xd', 'un', 'ao', 'eo', 'pf', 'kh', 'fb', 'fj', 'nm', 'ua', 'ph', 'kr', 'qa', 'cx', 'yg', 'wv', 'gf', 'lt', 'ce', 'ei', 'rv']
COPY_NB = {x: set() for x in MORSE}
for a, b in COPY_PAIRS: COPY_NB[a].add(b); COPY_NB[b].add(a)

def load_js(path, var):
    s = open(path, encoding='utf-8').read()
    return json.loads(s[s.index('=') + 1:].strip().rstrip(';'))

# Codes rares pour le modèle de langue mais confirmés par ailleurs (raison) : ils ne sont pas « douteux ».
CONFIRMED = {
    '0462': {28: 'mot', 52: 'date'}, '0348': {35: 'mot', 43: 'mot', 56: 'mot', 63: 'date'},
    '0413': {20: 'mot', 41: 'date'}, '0416a': {28: 'date'}, '0449': {12: 'mot', 18: 'nom'},
    '0455a': {15: 'variante'}, '0467': {43: 'variante'}, '0473': {30: 'variante', 58: 'nom'},
    '0494a': {3: 'variante', 17: 'mot'}, '0496a': {10: 'mot'}, '0498': {40: 'mot', 43: 'mot', 71: 'variante', 76: 'mot'},
}
# Fins de message dont la valeur attendue est connue par une autre source (formulaire, télégramme jumeau).
EXPECTED = {'0416b': (19, '皓', 'jumeau'), '0386': (37, '卅', 'cartouche')}
CH2C = {v: k for k, v in C2CH.items()}

def single_letter_paths(letters4, T, target):
    """Toutes les façons d'obtenir le code cible en changeant une seule lettre (quel que soit le mécanisme)."""
    out = []
    for k in range(4):
        for new in 'abcdefghijklmnopqrstuvwxyz':
            if new == letters4[k]: continue
            L = list(letters4); L[k] = new; a, b = ''.join(L[:2]), ''.join(L[2:])
            if a in T and b in T and T[a] <= 99 and T[b] <= 99 and '%02d%02d' % (T[a], T[b]) == target:
                o = letters4[k]
                kind = ('morse+copie' if new in MORSE_NB.get(o, ()) and new in COPY_NB.get(o, ()) else 'morse' if new in MORSE_NB.get(o, ())
                        else 'copie' if new in COPY_NB.get(o, ()) else 'autre')
                out.append({'k': k, 'from': o, 'to': new, 'kind': kind, 'morse': [MORSE[o], MORSE[new]]})
    return out

def analyse(m, grid):
    T = GRIDS[grid]; units = m['units']; codes = m['codes']
    letters = list(''.join(units))
    num = [int(c) if c.isdigit() else None for c in codes]
    out = []
    for i, code in enumerate(codes):
        status = 'ok'
        if num[i] is None: status = 'illisible'
        elif i in m['doubt']: status = 'douteux'
        conf = CONFIRMED.get(m['id'], {}).get(i)
        if conf:
            assert status == 'douteux', (m['id'], i, 'confirmé mais non douteux')
            status = 'confirmé:' + conf
        alts = []
        if status in ('douteux', 'illisible'):
            prev = num[i - 1] if i > 0 else None; nxt = num[i + 1] if i + 1 < len(num) else None
            base = local(prev, num[i], nxt) if num[i] is not None else -6.0
            for k in range(4):
                p = 4 * i + k; orig = letters[p]
                for new in sorted(MORSE_NB.get(orig, set()) | COPY_NB.get(orig, set())):
                    L = letters[4 * i:4 * i + 4]; L[k] = new
                    a, b = ''.join(L[:2]), ''.join(L[2:])
                    if a not in T or b not in T or T[a] > 99 or T[b] > 99: continue
                    c = T[a] * 100 + T[b]; ch = C2CH.get('%04d' % c)
                    if not ch: continue
                    d = local(prev, c, nxt) - base
                    kind = 'morse+copie' if (new in MORSE_NB.get(orig, ()) and new in COPY_NB.get(orig, ())) else ('morse' if new in MORSE_NB.get(orig, ()) else 'copie')
                    alts.append({'k': k, 'from': orig, 'to': new, 'kind': kind, 'code': '%04d' % c, 'ch': ch, 'd': round(d, 2),
                                 'morse': [MORSE[orig], MORSE[new]]})
            alts = [a for a in sorted(alts, key=lambda a: -a['d']) if a['d'] >= 1.5][:3]
        exp = None
        if m['id'] in EXPECTED and EXPECTED[m['id']][0] == i:
            _, ch, why = EXPECTED[m['id']]; target = CH2C[ch]
            exp = {'ch': ch, 'code': target, 'why': why, 'paths': single_letter_paths(letters[4 * i:4 * i + 4], T, target)}
        out.append({'s': status, 'alts': alts, 'exp': exp})
    return out

META = {  # canal, trajet, archive (JACAR) — dates et traductions dans translations.js
    '0348': ('G0', 'Tokyo → Zhaoqing (軍務院, 岑)', 'B03050089900'), '0386': ('G0', 'Tokyo → Zhaoqing (軍務院, 岑)', 'B03050089900'),
    '0406': ('G0', 'Tokyo → Shanghai (中華新報, 轉文羣)', 'B03050090000'), '0415': ('G0', 'Tokyo → Zhaoqing (軍務院)', 'B03050090000'),
    '0416b': ('G0', 'Tokyo → Zhaoqing (軍務院)', 'B03050090000'), '0455b': ('G0', 'Tokyo → Zhaoqing (岑都司令)', 'B03050090100'),
    '0462': ('G0', 'Tokyo → Zhaoqing (都司令部, 李印泉)', 'B03050090100'),
    '0413': ('Y0', 'Tokyo → Shanghai (中華新報) → Yunnan', 'B03050090000'), '0416a': ('Y0', 'Tokyo → Shanghai (中華新報, 轉文羣轉滇督)', 'B03050090000'),
    '0449': ('Y0', 'Tokyo → Kunming (唐都督)', 'B03050090100'), '0455a': ('Y0', 'Tokyo → Kunming (唐都督)', 'B03050090100'),
    '0467': ('Y0', 'Tokyo → Kunming (唐都督)', 'B03050090100'), '0473': ('Y0', 'Tokyo → Kunming (唐督軍)', 'B03050090100'),
    '0489a': ('Y0', 'Tokyo → Kunming (唐督軍)', 'B03050090100'), '0494a': ('Y0', 'Tokyo → Kunming (財政廳)', 'B03050090100'),
    '0496a': ('Y0', 'Tokyo → Kunming (唐督軍)', 'B03050090100'), '0498': ('Y0', 'Kunming → Tokyo (趙伸 c/o 関正雄)', 'B03050090100'),
}
msgs = load_js(os.path.join(SITE, 'assets', 'js', 'messages.js'), 'WENMI_MESSAGES') + load_js(os.path.join(SITE, 'assets', 'js', 'messages-y0.js'), 'WENMI_MESSAGES_Y0')
corpus = []
for m in msgs:
    grid = m.get('grid', 'G0'); ch, route, rec = META[m['id']]; assert ch == grid, m['id']
    codes = analyse(m, grid)
    corpus.append({'id': m['id'], 'grid': grid, 'route': route, 'record': rec, 'letters': ''.join(m['units']),
                   'codes': m['codes'], 'chars': m['chars'], 'status': [c['s'] for c in codes], 'alts': {str(i): c['alts'] for i, c in enumerate(codes) if c['alts']},
                   'expected': {str(i): c['exp'] for i, c in enumerate(codes) if c['exp']}})

# 1917 : lettres seulement (non déchiffrés)
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c14')); sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c31'))
os.environ.setdefault('C14_LM', 'lm3'); cwd = os.getcwd(); os.chdir(os.path.join(WENMI, 'cryptanalysis', 'c31'))
ans = json.load(open(os.path.join(WENMI, 'working', 'blind-c31', 'reponses', 'lot8', 'reponse-Brice-lot8.json'), encoding='utf-8'))['answers']
mp = {x['id']: x for x in json.load(open(os.path.join(WENMI, 'working', 'blind-c31', 'lot8', 'admin', 'mapping.json'), encoding='utf-8'))}
os.chdir(cwd)
r0509 = ' '.join(r for _, r in sorted((mp[e]['line'], ans[e]['reading']) for e in ans))
undeciphered = [{'id': '0509a', 'route': 'Shanghai → Tokyo (Sun Yat-sen → Dai Jitao)', 'record': 'B03050090200', 'reading': r0509},
                {'id': '0511a/b', 'route': 'Sun Yat-sen ↔ Dai Jitao', 'record': 'B03050090200', 'reading': None}]

stats = {'codes': sum(len(c['codes']) for c in corpus), 'douteux': sum(s == 'douteux' for c in corpus for s in c['status']),
         'confirmé': sum(s.startswith('confirmé') for c in corpus for s in c['status']),
         'illisible': sum(s == 'illisible' for c in corpus for s in c['status']), 'alts': sum(len(c['alts']) for c in corpus)}
open(os.path.join(SITE, 'assets', 'js', 'corpus.js'), 'w', encoding='utf-8').write(
    '// Généré par tools/build_corpus.py — ne pas éditer à la main.\nwindow.WENMI_CORPUS = '
    + json.dumps({'messages': corpus, 'undeciphered': undeciphered, 'stats': stats, 'morse': MORSE}, ensure_ascii=False) + ';\n')
print(stats)
for c in corpus:
    for i, e in c['expected'].items(): print('ATTENDU', c['id'], i, c['chars'][int(i)], '→', e['ch'], e['code'], e['why'], [(p['from'] + '→' + p['to'], p['kind']) for p in e['paths']])
for c in corpus:
    for i, al in c['alts'].items():
        print(c['id'], i, c['chars'][int(i)], c['codes'][int(i)], '→', ', '.join('%s %s (%s %s→%s %+.1f)' % (a['ch'], a['code'], a['kind'], a['from'], a['to'], a['d']) for a in al))
