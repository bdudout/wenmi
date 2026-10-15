#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Télégrammes de 1915 (JACAR B03050087600, B03050087700) au même format que les autres séries de la page « Télégrammes »
(fiche, lettres, code et caractère case par case, version lisible, traduction). Séance YC, 15/10/2026.
Données : wenmi/cryptanalysis/c35/site/t1915_data.json (lectures de Claude relues à l'aveugle par Brice, séance C35) ;
textes d'introduction : gen_t1915.py (même dossier) ; expéditeur / destinataire : persons.py (même dossier).
Sortie : assets/js/corpus-t1915.js. Usage : python3 tools/build_t1915.py <chemin du dossier d'enquête wenmi>"""
import ast, json, os, re, sys

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1])
C35 = os.path.join(WENMI, 'cryptanalysis', 'c35', 'site')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_condensateurs as BC                      # noqa: E402  (bkeys, LM, alts_for, edit_path, mean_score)
import restitution, c1916_i18n, form_times            # noqa: E402
sys.path.insert(0, C35)
from persons import who_html                          # noqa: E402
bkeys = BC.bkeys; C2CH, uni, REF = BC.C2CH, BC.uni, BC.REF
# tables de 1915 (cryptanalysis/c35/x1415/r15_apply.py)
bkeys.KEYS.setdefault('laisaosang1915', bkeys.make_table(1, 'oaeui'))
bkeys.KEYS.setdefault('k30', bkeys.make_table(16, 'uieoa'))
_ny = {c + v: (5 * i + j) % 100 for i, c in enumerate('bcdfghjklmnprstvwxyz') for j, v in enumerate('aeiou')}
_ny.update({'q' + v: _ny['p' + v] for v in 'aeiou'}); bkeys.KEYS.setdefault('newyork1915', _ny)
PREFIX = {'thirtieth', 'fourteen', 'bowery'}           # mots en clair (indicateur de table, adresse) : hors flux chiffré
# n° d'image JACAR : image du PDF + décalage du dossier (premier cadre : 087600 = 0163, 087700 = 0221 ; sources/c35/README.md)
OFF = {'B03050087600': 162, 'B03050087700': 220}
TIME = {}                                              # heures des formulaires (form_times.T1915 si présent)
TIME.update(getattr(form_times, 'T1915', {}))
KEYW = {'t1915-0106m': ['無其事'], 't1915-0131': ['富永', '在滬候命', '切勿回東'], 't1915-02p23': ['何日往港'],
        't1915-0202': ['不能乘平常船', '七號'], 't1915-0218': ['倭寇', '吾黨應持何態度', '林森'], 't1915-0220': ['日要求廿一款', '美報', '韓'],
        't1915-02ny': ['孤注一擲', '速來美'], 't1915-0226': ['上海', '周折', '犬塚'], 't1915-0227': ['電匯香港', '一星期'],
        't1915-0307': ['犬塚', '先生處存者卽匯'], 't1915-0310': ['謠言', '同人勿信']}
LANGS = ('fr', 'en', 'zh-Hant', 'ja')
SITE_LANG = {'fr': 'fr', 'en': 'en', 'zh-Hant': 'zh-hant', 'ja': 'ja'}


def gen_labels():
    """dictionnaire L de gen_t1915.py (intro, intitulés des tables), sans exécuter le script"""
    src = open(os.path.join(C35, 'gen_t1915.py'), encoding='utf-8').read()
    node = next(n for n in ast.parse(src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'L')
    env = {}; exec(compile(ast.Module([node], []), 'gen_t1915', 'exec'), {'dict': dict}, env)
    return env['L']


# la phrase sur ‹ › et { } ne vaut plus : la version lisible suit la légende commune de la page
DROP = {'fr': r" Dans la version lisible, ‹ › marque[^.]*\.\)?\.?", 'en': r" In the readable version, ‹ › marks[^.]*\.\)?\.?",
        'zh-Hant': r"可讀文本中，‹ › 表示[^。]*。", 'ja': r"読み下しでは、‹ › は[^。]*。"}
LAB = {
 'fr': dict(read='Lettres du formulaire (lues sur le scan, relues à l\'aveugle)', label='Traduction de travail.',
            stats='{tels} télégrammes, {codes} codes ; {douteux} douteux.'),
 'en': dict(read='Letters of the form (read on the scan, reread blind)', label='Working translation.',
            stats='{tels} telegrams, {codes} codes; {douteux} doubtful.'),
 'zh-Hant': dict(read='電報紙上的字母（依掃描件讀出，盲讀複核）', label='工作譯文。', stats='電報{tels}封，電碼{codes}個；存疑{douteux}個。'),
 'ja': dict(read='用紙の文字（スキャンから読み、ブラインドで読み直したもの）', label='試訳。', stats='電報{tels}通、符号{codes}個。疑わしいもの{douteux}個。'),
}


PUNCT = restitution.PUNCT | set('（）()…「」')


def parse(text, chars):
    """comme restitution.parse, mais un caractère en clair qui diffère du décodé est une variante graphique de l'édition
    (卄/廿, 謡/謠, 己/已) : affiché tel que dans l'édition, rattaché à son code"""
    toks, props, i, k = [], [], 0, 0
    while k < len(text):
        c = text[k]
        if c in PUNCT: toks.append((c, None, False)); k += 1; continue
        if c == '{': toks.append((text[k + 1], i, True)); props.append(i); i += 1; k += 3; continue
        if c == '‹': assert chars[i] == text[k + 1], (i, text[k + 1], chars[i]); toks.append((text[k + 1], i, False)); i += 1; k += 3; continue
        toks.append((c, i, False)); i += 1; k += 1
    assert i == len(chars), ('longueur', i, len(chars))
    return toks, props


def stream_of(cipher, T, raw):
    ws = [w for w in cipher.lower().split() if w not in PREFIX]
    s = ''.join(ws); best = None
    for al in (0, 1, 2, 3):
        t = s[al:]; d = [(t[i:i + 4], ('%02d%02d' % (T[t[i:i + 2]], T[t[i + 2:i + 4]])) if t[i:i + 2] in T and t[i + 2:i + 4] in T else '····')
                         for i in range(0, len(t) - 3, 4)]
        chars = ''.join(C2CH.get(c, '□') if c.isdigit() else '·' for _, c in d)
        ok = sum(a == b for a, b in zip(chars, raw))
        if best is None or ok > best[0]: best = (ok, al, d, chars)
    return best


def build():
    D = json.load(open(os.path.join(C35, 't1915_data.json'), encoding='utf-8')); G = gen_labels(); msgs = []
    for x in D:
        T = bkeys.KEYS[x['key']]
        ok, al, d, chars_s = stream_of(x['cipher'], T, x['raw'])
        assert chars_s == x['raw'], (x['id'], al, chars_s, x['raw'])
        codes = [c for _, c in d]; chars = list(chars_s); nums = [int(c) if c.isdigit() else 0 for c in codes]
        letters = ''.join(l4 for l4, _ in d)
        text = x['read']
        toks, props = parse(text, chars)
        marked, i, k = set(), 0, 0
        while k < len(text):
            c = text[k]
            if c in PUNCT: k += 1; continue
            if c in '{‹':
                if c == '‹': marked.add(i)
                i += 1; k += 3; continue
            i += 1; k += 1
        status = []
        for i, c in enumerate(codes):
            if not c.isdigit(): status.append('illisible')
            elif i in marked or i in props or chars[i] == '□': status.append('douteux')
            else: status.append('ok')
        alts = {str(i): a for i, st in enumerate(status) if st == 'douteux' and i not in props for a in [BC.alts_for(letters, i, nums, T)] if a}
        out = []
        for i in props:
            ch = next(t[0] for t in toks if t[1] == i and t[2])
            ep = BC.edit_path(letters[4 * i:4 * i + 4], T, ch)
            assert ep and len(ep['edits']) <= 2, (x['id'], i, ch, ep)
            out.append(dict(i=i, ch=ch, orig=chars[i], level='P', reasons=['sens'], letters=letters[4 * i:4 * i + 4], image=None, **ep))
        after = list(nums)
        for p in out: after[p['i']] = int(p['code'])
        rec, img = re.match(r'(B\d+), image (\d+)', x['src']).groups()
        n = '%04d' % (int(img) + OFF[rec])
        mo, da = (int(v) for v in re.match(r'1915年(\d+)月(\d+)?', x['date']['zh']).groups(default='0'))
        msgs.append({'id': x['id'][1:], 'verified': [], 'label': n + ('b' if x['id'] == 't1915-02ny' else ''), 'toc': x['key'], 'grid': x['key'],
                     'fiche': {'img': 't' + n, 'n': n, 'keys': KEYW[x['id']]}, 'route': x['route']['en'],
                     'routes': x['route'], 'record': rec, 'md': [mo, da], 'page': int(img), 'time': TIME.get(x['id']),
                     'letters': letters, 'codes': codes, 'chars': chars, 'status': status, 'fixed': {}, 'alts': alts, 'expected': {},
                     'readable': {'toks': [[c, i, p] for c, i, p in toks], 'props': out, 'score': [BC.mean_score(nums), BC.mean_score(after)]},
                     '_src': x})
    msgs.sort(key=lambda m: (m['md'][0], m['md'][1] or form_times.T1915_SORT_DAY.get('t' + m['id'], 0), form_times.minutes(m['time']), m['label']))
    stats = {'tels': len(msgs), 'codes': sum(len(m['codes']) for m in msgs), 'douteux': sum(s == 'douteux' for m in msgs for s in m['status'])}
    i18n = {}
    for lang in LANGS:
        g = G[SITE_LANG[lang]]; zh = 'zh' if lang.startswith('zh') else lang
        intro = re.sub(DROP[lang], '', g['intro'])
        dd = dict(LAB[lang]); dd.update(title=g['h2'], intro=intro, channel=dict(g['keys']), toc=dict(g['keys']))
        dd['tr'] = {m['id']: m['_src']['tr'][lang] for m in msgs if lang in m['_src']['tr']}
        dd['date'] = {m['id']: m['_src']['date'].get(lang) or m['_src']['date'][zh] for m in msgs}
        dd['route'] = {m['id']: m['_src']['route'].get(SITE_LANG[lang]) or m['_src']['route'].get(lang) for m in msgs}
        dd['who'] = {m['id']: who_html(m['_src']['id'], SITE_LANG[lang]) for m in msgs}
        i18n[lang] = dd
    T2 = c1916_i18n.t2s_table(WENMI)
    hans = c1916_i18n.to_hans({k: v for k, v in i18n['zh-Hant'].items() if k not in ('date', 'route', 'who', 'intro', 'title', 'channel', 'toc')}, T2)
    g = G['zh-hans']
    hans.update(date=dict(i18n['zh-Hant']['date']), title=g['h2'], intro=re.sub(r"可读文本中，‹ › 表示[^。]*。", '', g['intro']),
                channel=dict(g['keys']), toc=dict(g['keys']),
                route={m['id']: m['_src']['route']['zh-hans'] for m in msgs}, who={m['id']: who_html(m['_src']['id'], 'zh-hans') for m in msgs})
    i18n['zh-Hans'] = hans
    for m in msgs: del m['_src']; del m['routes']
    open(os.path.join(SITE, 'assets', 'js', 'corpus-t1915.js'), 'w', encoding='utf-8').write(
        '// Généré par tools/build_t1915.py — ne pas éditer à la main.\n'
        'window.WENMI_T1915 = ' + json.dumps({'messages': msgs, 'stats': stats}, ensure_ascii=False) + ';\n'
        'window.WENMI_T1915_I18N = ' + json.dumps(i18n, ensure_ascii=False) + ';\n')
    print(stats)
    for m in msgs: print(m['id'], m['label'], m['md'], ''.join(m['chars']), [p['ch'] for p in m['readable']['props']])


if __name__ == '__main__':
    build()
