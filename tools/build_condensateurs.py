#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Télégrammes à condensateur de 1916 pour la page « Télégrammes » (après le Wenmi), au même format que corpus.js.

Lettres : transcription publiée [1, 2] et ses corrections, rectifiées lettre par lettre par les lectures de scan retenues
(lots aveugles B1 et B2) — wenmi/cryptanalysis/c32/final_streams.py. Seuls figurent les télégrammes dont au moins un
caractère a été corrigé ou vérifié sur le scan.
Pour chaque code : statut (sûr, douteux, rare mais confirmé), caractère corrigé par rapport au texte publié, pistes d'une
lettre (Morse ou copie) pour les codes douteux, version lisible avec propositions (restitution_c1916.py).
Sortie : assets/js/corpus-c1916.js (données + textes dans les 5 langues, tools/c1916_i18n.py).
Usage : python3 tools/build_condensateurs.py <chemin du dossier d'enquête wenmi>"""
import json, os, sys

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c32'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from final_streams import SEL, final_stream          # noqa: E402  (dossier d'enquête)
from check_repro import stream as published_stream   # noqa: E402
import bkeys                                          # noqa: E402
import restitution, restitution_c1916 as RC, c1916_i18n  # noqa: E402
import dx_overrides  # noqa: E402
DX = dx_overrides.load(WENMI)

CONS, VOW = bkeys.CONS, bkeys.VOW
uni, REF, BI, BDEF, C2CH = bkeys.uni, bkeys.REF, bkeys.BI, bkeys.BDEF, bkeys.CODE2CH
CH2CODES = {}
for _c, _ch in C2CH.items(): CH2CODES.setdefault(_ch, []).append(_c)

# mécanismes d'erreur : mêmes définitions que build_corpus.py (Morse : un signe de différence ; copie : paires relevées)
MORSE = dict(a='.-', b='-...', c='-.-.', d='-..', e='.', f='..-.', g='--.', h='....', i='..', j='.---', k='-.-', l='.-..',
             m='--', n='-.', o='---', p='.--.', q='--.-', r='.-.', s='...', t='-', u='..-', v='...-', w='.--', x='-..-',
             y='-.--', z='--..')
def lev1(a, b):
    if a == b or abs(len(a) - len(b)) > 1: return False
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) == 1
    s, l = (a, b) if len(a) < len(b) else (b, a)
    return any(l[:k] + l[k + 1:] == s for k in range(len(l)))
MORSE_NB = {x: {y for y in MORSE if lev1(MORSE[x], MORSE[y])} for x in MORSE}
COPY_PAIRS = ['gq', 'xd', 'un', 'ao', 'eo', 'pf', 'kh', 'fb', 'fj', 'nm', 'ua', 'ph', 'kr', 'qa', 'cx', 'yg', 'wv', 'gf', 'lt', 'ce', 'ei', 'rv',
              'xs', 'xn', 'sr', 'bs', 'yj', 'zj']   # + confusions relevées sur les formulaires de 1916 (lots B1, B2)
COPY_NB = {x: set() for x in MORSE}
for a, b in COPY_PAIRS: COPY_NB[a].add(b); COPY_NB[b].add(a)
def kind_of(o, n):
    return ('morse+copie' if n in MORSE_NB.get(o, ()) and n in COPY_NB.get(o, ()) else 'morse' if n in MORSE_NB.get(o, ())
            else 'copie' if n in COPY_NB.get(o, ()) else 'autre')

def bi(a, b): return 0.0 if a is None or b is None else BI.get(a * 10000 + b, BDEF)
def local(prev, c, nxt): return float(uni[c]) - REF + bi(prev, c) + bi(c, nxt)
def code_of(T, l4):
    a, b = l4[:2], l4[2:]
    return '%02d%02d' % (T[a], T[b]) if a in T and b in T else None

def alts_for(letters, i, nums, T):
    """Variantes d'une lettre (Morse ou copie) qui restent des syllabes du condensateur, notées par le modèle de langue."""
    prev = nums[i - 1] if i > 0 else None; nxt = nums[i + 1] if i + 1 < len(nums) else None
    base = local(prev, nums[i], nxt); out = []
    for k in range(4):
        o = letters[4 * i + k]; pool = CONS if k % 2 == 0 else VOW
        for n in sorted((MORSE_NB.get(o, set()) | COPY_NB.get(o, set())) & set(pool)):
            L = list(letters[4 * i:4 * i + 4]); L[k] = n; code = code_of(T, ''.join(L))
            if not code or code not in C2CH: continue
            d = local(prev, int(code), nxt) - base
            out.append({'k': k, 'from': o, 'to': n, 'kind': kind_of(o, n), 'code': code, 'ch': C2CH[code], 'd': round(d, 2),
                        'morse': [MORSE[o], MORSE[n]]})
    return [a for a in sorted(out, key=lambda a: -a['d']) if a['d'] >= 1.5][:3]

def edit_path(l4, T, target):
    inv = {v: k for k, v in T.items()}; best = None
    for code in CH2CODES.get(target, []):
        a, b = int(code[:2]), int(code[2:])
        if a not in inv or b not in inv: continue
        tgt = inv[a] + inv[b]; d = [k for k in range(4) if l4[k] != tgt[k]]
        if best is None or len(d) < len(best[1]): best = (code, d, tgt)
    if best is None: return None
    code, d, tgt = best
    return {'code': code, 'to_letters': tgt,
            'edits': [{'from': l4[k], 'to': tgt[k], 'kind': kind_of(l4[k], tgt[k]), 'morse': [MORSE[l4[k]], MORSE[tgt[k]]]} for k in d]}

def mean_score(nums):
    tot, n, prev = 0.0, 0, None
    for c in nums:
        tot += float(uni[c]) - REF + bi(prev, c); n += 1; prev = c
    return round(tot / max(n, 1), 2)

# ---- mots ajoutés ou fins relues : codes nouveaux par rapport au texte publié
OMIS = {'c0489': (65, 67)}           # mot omis par la transcription publiée (B48, papier 38, ligne 6) : codes 65–67
NEW_FROM = {'c0489': 68, 'c0069': 50}  # au-delà : le texte publié s'arrêtait (« suite non reprise » / fin illisible)
NOT_FIXED = {('c0495', 19),          # le texte publié portait 請 (correction supposée) ; le scan porte g : proposition
             ('c0087', 17), ('c0075', 72)}   # 否, 近 : déjà dans le texte publié (correction appliquée, confirmée sur le scan)
# Même classement que la page « Condensateurs 1916 » : 28 corrections (tableau), 12 lectures proposées confirmées, 4 lectures nouvelles
SUGG = {('c0470', '回'), ('c0473a', '款'), ('c0473b', '查'), ('c0473b', '有'), ('c0475', '告'), ('c0476', '此'), ('c0459', '知'),
        ('c0492', '警'), ('c0495', '匯'), ('c0069', '東'), ('c0069', '在'), ('c0087', '銷')}
NEW = {('c0475', '巳'), ('c0490b', '廖'), ('c0061', '京'), ('c0061', '無')}
FRAME0 = {'B03050088300': 440, 'B03050089100': 59}

def build():
    msgs = []
    for sid, tid, key, route, rec, img, (mo, da) in SEL:
        t, s = final_stream(tid); T = bkeys.KEYS[key]
        s = dx_overrides.apply_stream(s, DX.get(('c1916', sid), {}), sid)   # relecture ciblée (Brice, 13/10/2026)
        d = bkeys.decode(s, key); codes = [c for _, c in d]; chars = [C2CH[c] for c in codes]; nums = [int(c) for c in codes]
        letters = ''.join(syl for syl, _ in d)
        assert letters == s[:len(letters)], sid
        ps = published_stream(t); ps = ps[:len(ps) - len(ps) % 2]
        pub = [c for _, c in bkeys.decode(ps, key)]
        fixed = {}
        for i, c in enumerate(codes):
            if sid in OMIS and OMIS[sid][0] <= i <= OMIS[sid][1]: fixed[str(i)] = {'how': 'omis'}
            elif sid in NEW_FROM and i >= NEW_FROM[sid]: fixed[str(i)] = {'how': 'nouveau'}
            elif i in DX.get(('c1916', sid), {}) and i < len(pub) and pub[i] != c: fixed[str(i)] = {'how': 'dx', 'from': C2CH.get(pub[i], '□')}
            elif i < len(pub) and pub[i] != c and (sid, i) not in NOT_FIXED:
                k = 'sugg' if (sid, C2CH[c]) in SUGG else 'new' if (sid, C2CH[c]) in NEW else 'scan'
                fixed[str(i)] = {'how': k, 'from': C2CH.get(pub[i], '□')}
        text, levels = RC.R[sid]
        toks, props = restitution.parse(text, chars)
        assert len(props) == len(levels), (sid, len(props), len(levels))
        # douteux : rares pour le modèle de langue (hors confirmés) + caractères laissés ‹ › dans la version lisible + cibles des propositions
        marked, i, k = set(), 0, 0
        while k < len(text):
            c = text[k]
            if c in restitution.PUNCT: k += 1; continue
            if c in '{‹':
                if c == '‹': marked.add(i)
                i += 1; k += 3; continue
            i += 1; k += 1
        conf = RC.CONFIRMED.get(sid, {})
        status = []
        for i, c in enumerate(codes):
            rare = float(uni[nums[i]]) - REF < 1
            if i in conf:
                assert rare, (sid, i, chars[i], 'confirmé mais non rare'); status.append('confirmé:' + conf[i])
            elif rare or i in marked or i in props: status.append('douteux')
            else: status.append('ok')
        alts = {str(i): a for i, st in enumerate(status) if st == 'douteux' and i not in props for a in [alts_for(letters, i, nums, T)] if a}
        out = []
        for (lvl, reasons), i in zip(levels, props):
            ch = next(t[0] for t in toks if t[1] == i and t[2])
            ep = edit_path(letters[4 * i:4 * i + 4], T, ch)
            assert ep and len(ep['edits']) <= 2, (sid, i, ch, ep)
            out.append(dict(i=i, ch=ch, orig=chars[i], level=lvl, reasons=reasons, letters=letters[4 * i:4 * i + 4],
                            image=RC.IMAGE.get((sid, i)), **ep))
        after = list(nums)
        for p in out: after[p['i']] = int(p['code'])
        n = img[:4]
        msgs.append({'id': sid, 'label': sid[1:], 'grid': key, 'route': route, 'record': rec, 'md': [mo, da], 'old': tid,
                     'letters': letters, 'codes': codes, 'chars': chars, 'status': status, 'fixed': fixed, 'alts': alts, 'expected': {},
                     'readable': {'toks': [[c, i, p] for c, i, p in toks], 'props': out, 'score': [mean_score(nums), mean_score(after)]},
                     'fiche': {'img': 'c' + n, 'n': n, 'keys': RC.KEYS[sid]}})
    order = ['manila1916', 'shanghai1916', 'seito1916', 'yamada1916']   # par date du premier télégramme de chaque clé
    msgs.sort(key=lambda m: (order.index(m['grid']), m['md'], m['label']))
    stats = {'tels': len(msgs), 'codes': sum(len(m['codes']) for m in msgs),
             'corr': sum(1 for m in msgs for v in m['fixed'].values() if v['how'] == 'scan'),
             'sugg': sum(1 for m in msgs for v in m['fixed'].values() if v['how'] == 'sugg'),
             'new': sum(1 for m in msgs for v in m['fixed'].values() if v['how'] == 'new'),
             'dx': sum(1 for m in msgs for v in m['fixed'].values() if v['how'] == 'dx'),
             'added': sum(1 for m in msgs for v in m['fixed'].values() if v['how'] in ('omis', 'nouveau')),
             'douteux': sum(s == 'douteux' for m in msgs for s in m['status']),
             'confirmé': sum(s.startswith('confirmé') for m in msgs for s in m['status']),
             'props': sum(len(m['readable']['props']) for m in msgs)}
    assert (stats['corr'], stats['sugg'], stats['new']) == (28, 12, 3), stats   # = page « Condensateurs 1916 » (la lecture nouvelle 巳 de 0475, relue 已 le 13/10, passe en « dx »)
    i18n = c1916_i18n.build(msgs, stats, WENMI)
    path = os.path.join(SITE, 'assets', 'js', 'corpus-c1916.js')
    open(path, 'w', encoding='utf-8').write(
        '// Généré par tools/build_condensateurs.py — ne pas éditer à la main.\n'
        'window.WENMI_C1916 = ' + json.dumps({'order': order, 'messages': msgs, 'stats': stats}, ensure_ascii=False) + ';\n'
        'window.WENMI_C1916_I18N = ' + json.dumps(i18n, ensure_ascii=False) + ';\n')
    print(stats)
    for m in msgs:
        print(m['id'], m['old'], m['grid'], m['md'], 'changés', [(m['chars'][int(i)], v['how']) for i, v in m['fixed'].items() if v['how'] in ('scan', 'sugg', 'new')],
              'props', [(p['orig'], p['ch'], p['level'], ''.join(e['from'] + '→' + e['to'] for e in p['edits'])) for p in m['readable']['props']],
              'score', m['readable']['score'])

if __name__ == '__main__':
    build()
