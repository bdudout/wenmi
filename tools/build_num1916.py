#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Télégrammes numériques de juin 1916 (容密 et 共密) pour la page « Télégrammes » : même format de fiche que corpus-n1916.js.

Usage : python3 tools/build_num1916.py ../wenmi
Lit : wenmi/cryptanalysis/c83/site-data.json + segments.py (容密 ×11, 共密 N23), c84/segments_gongmi.py (共密 ×7) et
c62/publication-v3/data/gongmi.json (groupes 共密), c84/tr_i18n.py (traductions en/ja, notes).
Écrit : assets/js/corpus-num1916.js (WENMI_NUM1916 + WENMI_NUM1916_I18N), assets/img/fiches/scan-<id>.webp (+ -full) et map-<id>.png.
Lecture proposée : {x} = lecture probable (niveau P si une variante à un chiffre près du groupe la donne, Q si contexte seul)."""
import json, os, re, shutil, sys
from PIL import Image, ImageOps

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c84'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segments_gongmi as SG, tr_i18n as TR          # noqa: E402
import c1916_i18n                                     # noqa: E402
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c47'))
import additive_fft as LM                             # noqa: E402  (modèle de langue C39 lmt30, comme les autres fiches)
import numpy as np                                    # noqa: E402
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c51'))
from decode_common import decode_code                 # noqa: E402

D = json.load(open(os.path.join(WENMI, 'cryptanalysis', 'c83', 'site-data.json'), encoding='utf-8'))['messages']
CLEAR = json.load(open(os.path.join(WENMI, 'cryptanalysis', 'c88', 'clear-data.json'), encoding='utf-8'))['messages']
D.update(CLEAR)
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c88'))
import segments_clear as SCL                          # noqa: E402
for _L, _d in (('EN', SCL.EN), ('JA', SCL.JA)): getattr(TR, _L).update(_d)
for _L in SCL.NOTE: TR.NOTE.setdefault(_L, {}).update(SCL.NOTE[_L])
G = json.load(open(os.path.join(WENMI, 'cryptanalysis', 'c62', 'publication-v3', 'data', 'gongmi.json'), encoding='utf-8'))['messages']
V = {}
for f in ('c83/variants.json', 'c84/gongmi-variants.json'):
    for r in json.load(open(os.path.join(WENMI, 'cryptanalysis', f), encoding='utf-8')):
        for h in r.get('hits', []):
            gl, var = (h['glyph'], h['variant']) if isinstance(h, dict) else (h[0], h[1])
            V.setdefault((r['mid'], r['cipher']), {})[gl] = var
CTC = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(WENMI, 'cryptanalysis', 'c39', 'lmt', 'lmt30', 'code2ch.tsv'), encoding='utf-8'))
INV = {}
for k, v in CTC.items():
    INV.setdefault(v, k)
SIG2 = [[0, 1, 2, 3, 4, 5, 6, 7, 9, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 9, 8, 2, 7, 6, 5, 4, 3], [9, 8, 0, 1, 7, 2, 3, 4, 5, 6]]
PUNCT = set('，。、：；？！「」『』（）…—　 ,.;:?!()')

KEYS = {'N04': ['西北', '北伐', '陝軍'], 'N31': ['第三銀行', '正隆'], 'N34': ['黎元洪', '陽夏同舟', '根本大計'], 'N19b': ['約法', '武力', '南北統一'], 'N02': ['步鎗', '肇慶借款', '酒公賣'], 'N08': ['購械', '子彈', '借款'], 'N11': ['溯初', '歸滬'], 'N12': ['芳川', '百萬', '抵當品'],
        'N14': ['袁死', '械先運'], 'N19a': ['百里', '官君'], 'N28': ['百里', '詠儀'], 'N21': ['張潤農', '機關銃', '呂公望'],
        'N25': ['烟捐', '酒捐', '吳兆蓮'], 'N36': ['黃克強', '六月三十日'], 'N24': ['黎電', '元年約法', '殷汝驪'], 'N23': ['田中', '小池', '張繼'],
        'N17': ['黎總統', '舊約法', '日當局'], 'N18': ['擁護共和', '武力'], 'N27': ['溥', '無望'], 'N30': ['小池', '有吉領事'],
        'N32': ['舊約法', '中山', '葛殷黃'], 'N33': ['馮', '黃羣', '約法'], 'N35': ['國會', '段', '袁']}
ORDER = ['N04', 'N31', 'N34', 'N14', 'N19b', 'N02', 'N08', 'N11', 'N12', 'N19a', 'N28', 'N21', 'N25', 'N36', 'N24', 'N17', 'N18', 'N23', 'N27', 'N30', 'N32', 'N33', 'N35']
FAM = {m: '容密' for m in D if D[m]['family'] == '容密'}
FAM.update({m: '明碼' for m in CLEAR})
FAM.update({m: '共密' for m in ['N17', 'N18', 'N23', 'N27', 'N30', 'N32', 'N33', 'N35']})

def lm_score(codes):
    c = [int(x) for x in codes if x is not None]
    if not c: return 0.0
    m = np.asarray(c); s = LM.U[m].sum()
    if len(m) > 1:
        k = m[:-1].astype(np.int64) * 10000 + m[1:]; i = np.searchsorted(LM.BK, k); cap = np.minimum(i, len(LM.BK) - 1)
        s += np.where((i < len(LM.BK)) & (LM.BK[cap] == k), LM.BV[cap], LM.BD).sum()
    return float(s / len(m))

def encode_rongmi(p):
    """Groupe chiffré qui donnerait le code p sous la clé 容密 v2 (première solution)."""
    for c in range(10000):
        g = f'{c:04d}'
        if (sum(SIG2[j][int(g[j])] * w for j, w in enumerate((1000, 100, 10, 1))) + 901) % 10000 == p: return g
def encode_gongmi(p):
    for c in range(10000):
        if decode_code(c) == p: return f'{c:04d}'

def message(mid):
    fam = FAM[mid]
    if mid in D:
        d = D[mid]; segs = [(s['raw'], s['status'], s['zh'], s['fr'], s['note']) for s in d['segments']]
        if fam == '明碼':
            groups = list(d['groups']); prefix = ''
        else:
            groups = [g for g in d['groups']][2:]; prefix = ' '.join(g['cipher'] for g in d['groups'][:2])
        meta = d['meta']
        summary_fr = d['summary_fr']
    else:
        segs = SG.SEG[mid]; meta = SG.META[mid]; summary_fr = SG.SUMMARY[mid]
        groups = [dict(cipher=g['cipher'], ctc=g['ctc'], glyph=g['glyph_raw']) for g in G[mid]['groups']]; prefix = '0364 1378'
    raw = ''.join(s[0] for s in segs)
    assert raw == ''.join(g['glyph'] for g in groups), mid
    status = []; toks = []; props = []; k = 0
    for raw_s, st, zh, fr, note in segs:
        i = 0
        while i < len(zh):
            ch = zh[i]
            if ch == '{':
                j = zh.index('}', i); new = zh[i + 1:j]
                g = groups[k]; code = INV.get(new)
                via = V.get((mid, g['cipher']), {}).get(new)
                level = 'P' if via else 'Q'
                to = via or (code if fam == '明碼' else (code and (encode_rongmi(int(code)) if fam == '容密' else encode_gongmi(int(code))))) or g['cipher']
                edits = [dict(**{'from': a, 'to': b}, kind=('copie' if via else 'autre')) for a, b in zip(g['cipher'], to) if a != b]
                props.append(dict(i=k, ch=new, orig=g['glyph'], level=level, reasons=['sens'] if via else ['contexte'], letters=g['cipher'],
                                  image=None, code=code or '', to_letters=to, edits=edits))
                toks.append([new, k, True]); status.append('douteux'); k += 1; i = j + 1; continue
            if ch == '〔':
                j = zh.index('〕', i)
                for c2 in zh[i + 1:j]:
                    if k < len(groups) and c2 == groups[k]['glyph']:
                        toks.append([c2, k, False]); status.append('illisible' if c2 == '□' else 'douteux'); k += 1
                    else:
                        toks.append([c2, None, False])
                i = j + 1; continue
            if k < len(groups) and ch == groups[k]['glyph']:
                toks.append([ch, k, False]); status.append('illisible' if ch == '□' else 'ok'); k += 1
            else:
                assert ch in PUNCT or ch in '僞', (mid, ch, zh)
                if ch == '僞' and k < len(groups) and groups[k]['glyph'] == '偽':   # graphie normalisée
                    toks.append([ch, k, False]); status.append('ok'); k += 1
                else:
                    toks.append([ch, None, False])
            i += 1
    assert k == len(groups), (mid, k, len(groups))
    codes = [g['ctc'] or '----' for g in groups]
    dec = [g['ctc'] for g in groups]; withp = list(dec)
    for p in props:
        withp[p['i']] = p['code'] or dec[p['i']]
    arch, page, side = meta['sheets'][0]
    mm = dict(id='num-' + mid, label=mid, toc={'容密': 'rongmi', '共密': 'gongmi', '明碼': 'clair'}[fam], grid={'容密': 'rongmi', '共密': 'gongmi', '明碼': 'clair'}[fam],
              route=meta['dir'].split(',')[0], record=arch, md=[6, meta['date'] or 0], page=page, time='', prefix=True,
              letters=''.join(g['cipher'] for g in groups), cipher=(prefix + ' · ' if prefix else '') + ' '.join(g['cipher'] for g in groups),
              tokenLetters=[g['cipher'] for g in groups], codes=codes, chars=[g['glyph'] for g in groups], status=status,
              fixed={}, alts={}, expected={}, verified=[],
              fiche=dict(img='num-' + mid, n=f'{arch[-4:]}-{page}{side}', keys=KEYS[mid], **({'nomap': True} if 'Mukden' in meta['dir'] else {})),
              readable=dict(toks=toks, props=props, score=[lm_score(dec), lm_score(withp)]))
    return mm, segs, summary_fr

def fiche(mid, mm, meta):
    out = os.path.join(SITE, 'assets', 'img', 'fiches')
    arch, page, side = meta['sheets'][0]
    for name in (f'{arch}-{page:02d}.png', f'{arch}-{page}.png'):
        p = os.path.join(WENMI, 'working', 'ylc-ocr', 'png', name)
        if os.path.exists(p): break
    im = Image.open(p).convert('L'); w, h = im.size
    box = (int(w * .47), int(h * .14), int(w * .81), int(h * .89)) if side == 'R' else (int(w * .19), int(h * .14), int(w * .53), int(h * .89))
    c = ImageOps.autocontrast(im.crop(box), cutoff=1)
    full = c.copy(); full.thumbnail((1400, 2400)); full.save(os.path.join(out, f'scan-num-{mid}-full.webp'), quality=60)
    th = c.copy(); th.thumbnail((520, 820)); th.save(os.path.join(out, f'scan-num-{mid}.webp'), quality=70)
    src = 'map-n0517.png' if meta['dir'].startswith('Tokyo') else 'map-s0505.png'   # même trajet Tokyo ↔ Shanghai
    if 'Mukden' not in meta['dir']: shutil.copyfile(os.path.join(out, src), os.path.join(out, f'map-num-{mid}.png'))

def zh_reading(segs, day):
    t = ''.join(s[2] for s in segs)
    t = re.sub(r'\{([^}]*)\}', r'\1', t).replace('〔', '').replace('〕', '')
    return t

DAYZH = {8: '八日', 9: '九日', 10: '十日', 11: '十一日', 13: '十三日', 14: '十四日', 15: '十五日', 16: '十六日', 12: '十二日'}
DATE = {
 'fr': lambda d, n: n, 'en': lambda d, n: f'{d} June 1916' if d else 'June 1916 (day not read)',
 'ja': lambda d, n: f'1916年6月{d}日' if d else '1916年6月（日付未読）', 'zh-Hant': lambda d, n: f'1916年6月{d}日' if d else '1916年6月（日期未讀）',
}
I18N = {
 'fr': dict(title='Télégrammes numériques de juin 1916 (容密, 共密)', read='Groupes de chiffres du formulaire (préfixe en clair éventuel, puis corps)', label='Traduction de travail.', noteLabel='Note :',
            channel={'rongmi': 'Clé 容密 (v2)', 'gongmi': 'Clé 共密 (C51)', 'clair': 'En clair (code télégraphique chinois)'}),
 'en': dict(title='Numeric telegrams of June 1916 (Rongmi, Gongmi)', read='Digit groups of the form (clear prefix if any, then body)', label='Working translation.', noteLabel='Note:',
            channel={'rongmi': 'Rongmi key (v2)', 'gongmi': 'Gongmi key (C51)', 'clair': 'In clear (Chinese telegraph code)'}),
 'ja': dict(title='1916年6月の数字電報（容密・共密）', read='用紙の数字組（平文の前置きがあればその後に本文）', label='作業訳。', noteLabel='注：',
            channel={'rongmi': '容密の鍵（v2）', 'gongmi': '共密の鍵（C51）', 'clair': '平文（中文電碼）'}),
 'zh-Hant': dict(title='1916年6月的數字電報（容密、共密）', read='電報紙上的數字組（如有明文前綴，其後為正文）', label='推定讀法（加標點）。', noteLabel='注：',
            channel={'rongmi': '容密密鑰（v2）', 'gongmi': '共密密鑰（C51）', 'clair': '明碼（中文電碼）'}),
}
ROUTE = {'fr': {'T': 'Tokyo → Shanghai', 'S': 'Shanghai → Tokyo'}, 'en': {'T': 'Tokyo → Shanghai', 'S': 'Shanghai → Tokyo'},
         'ja': {'T': '東京→上海', 'S': '上海→東京'}, 'zh-Hant': {'T': '東京→上海', 'S': '上海→東京'}}

if __name__ == '__main__':
    msgs = []; i18n = {L: dict(I18N[L], date={}, route={}, tr={}, note={}) for L in I18N}
    for mid in ORDER:
        mm, segs, sfr = message(mid)
        meta = D[mid]['meta'] if mid in D else SG.META[mid]
        fiche(mid, mm, meta); msgs.append(mm)
        d = meta['date']; rk = 'T' if meta['dir'].startswith('Tokyo') else 'S'
        for L in I18N:
            i18n[L]['date'][mm['id']] = DATE[L](d, meta['date_note'])
            i18n[L]['route'][mm['id']] = ROUTE[L][rk]
        i18n['fr']['tr'][mm['id']] = ' '.join(s[3] for s in segs)
        i18n['en']['tr'][mm['id']] = TR.EN[mid]
        i18n['ja']['tr'][mm['id']] = TR.JA[mid]
        i18n['zh-Hant']['tr'][mm['id']] = zh_reading(segs, d) + (f'（{DAYZH[d]}）' if d in DAYZH else '')
        rr = D[mid]['reread_by_brice']
        UNR = {'fr': 'Chiffres pas encore relus par Brice Dudout.', 'en': 'Digits not yet re-read by Brice Dudout.', 'ja': '数字はまだBrice Dudoutが再読していない。', 'zh-Hant': '數字尚未經 Brice Dudout 複讀。'}
        RR = {'fr': 'Chiffres relus par Brice Dudout.', 'en': 'Digits re-read by Brice Dudout.', 'ja': '数字はBrice Dudoutが再読済み。', 'zh-Hant': '數字已經 Brice Dudout 複讀。'}
        for L in ('fr', 'en', 'ja', 'zh-Hant'):
            i18n[L]['note'][mm['id']] = ((TR.NOTE[L][mid] + ' ') if mid in TR.NOTE[L] else '') + (RR if rr else UNR)[L]
    T2 = c1916_i18n.t2s_table(WENMI)
    i18n['zh-Hans'] = c1916_i18n.to_hans(i18n['zh-Hant'], T2)
    i18n['zh-Hans']['channel'] = {'rongmi': '容密密钥（v2）', 'gongmi': '共密密钥（C51）', 'clair': '明码（中文电码）'}
    i18n['zh-Hans']['label'] = '推定读法（加标点）。'
    open(os.path.join(SITE, 'assets', 'js', 'corpus-num1916.js'), 'w', encoding='utf-8').write(
        '// Généré par tools/build_num1916.py — ne pas éditer à la main.\nwindow.WENMI_NUM1916 = ' + json.dumps(dict(messages=msgs), ensure_ascii=False) +
        ';\nwindow.WENMI_NUM1916_I18N = ' + json.dumps(i18n, ensure_ascii=False) + ';\n')
    print(len(msgs), 'fiches ;', sum(len(m['readable']['props']) for m in msgs), 'lectures probables')
