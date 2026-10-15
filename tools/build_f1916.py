#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Télégrammes de février–mars 1916 (JACAR B03050088000 – B03050088200) au même format que les autres séries de la page
« Télégrammes » (fiche, lettres, code et caractère case par case, version lisible, traduction). Calqué sur build_t1915.py.
Données : wenmi/cryptanalysis/c35/site/f1916_data.json (lecture aveugle de Brice R19 fusionnée à celle de Claude, caractères
marqués revus à l'image en R20) ; expéditeur / destinataire : persons.py (même dossier).
Sortie : assets/js/corpus-f1916.js. Usage : python3 tools/build_f1916.py <chemin du dossier d'enquête wenmi>"""
import json, os, re, sys

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1])
C35 = os.path.join(WENMI, 'cryptanalysis', 'c35', 'site')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_condensateurs as BC                      # noqa: E402  (bkeys, LM, alts_for, edit_path, mean_score)
import c1916_i18n                                     # noqa: E402
import build_t1915 as BT                              # noqa: E402  (parse, stream_of, PUNCT)
sys.path.insert(0, C35)
from persons import who_html                          # noqa: E402
bkeys = BC.bkeys; C2CH = BC.C2CH
bkeys.KEYS.setdefault('k13', bkeys.make_table(10, 'oaeiu'))   # « Thirteenth » (cryptanalysis/c35/y1916)
# n° d'image JACAR : image du PDF + décalage du dossier (premiers cadres 0280, 0336, 0383 ; sources/c35/README.md)
OFF = {'B03050088000': 279, 'B03050088100': 335, 'B03050088200': 382}
SUFFIX = {'f1916-0323': 'a', 'f1916-0322': 'b'}        # deux télégrammes sur la même image (0430)
LANGS = ('fr', 'en', 'zh-Hant', 'ja')
SITE_LANG = {'fr': 'fr', 'en': 'en', 'zh-Hant': 'zh-hant', 'ja': 'ja'}
S21 = '<sup class="fn"><a href="sources.html#s21">[21]</a></sup>'; S1 = '<sup class="fn"><a href="sources.html#s1">[1]</a></sup>'
KEYS = {
 'fr': {'shanghai1916': 'table « Shanghai » (D. Bourdeau)', 'k13': 'table « Thirteenth » (nouvelle)', 'seito1916': 'table « Qingdao » (D. Bourdeau)', 'manila1916': 'table « Manille » (D. Bourdeau)'},
 'en': {'shanghai1916': '“Shanghai” table (D. Bourdeau)', 'k13': '“Thirteenth” table (new)', 'seito1916': '“Qingdao” table (D. Bourdeau)', 'manila1916': '“Manila” table (D. Bourdeau)'},
 'zh-Hant': {'shanghai1916': '「上海」碼表（D. Bourdeau）', 'k13': '「Thirteenth」碼表（新）', 'seito1916': '「青島」碼表（D. Bourdeau）', 'manila1916': '「馬尼拉」碼表（D. Bourdeau）'},
 'zh-hans': {'shanghai1916': '“上海”码表（D. Bourdeau）', 'k13': '“Thirteenth”码表（新）', 'seito1916': '“青岛”码表（D. Bourdeau）', 'manila1916': '“马尼拉”码表（D. Bourdeau）'},
 'ja': {'shanghai1916': '「上海」表（D. Bourdeau）', 'k13': '「Thirteenth」表（新）', 'seito1916': '「青島」表（D. Bourdeau）', 'manila1916': '「マニラ」表（D. Bourdeau）'},
}
TXT = {
 'fr': dict(title='Février–mars 1916 : nouveaux déchiffrements', intro=(
   '<p><strong>Nouveaux déchiffrements (octobre 2026), inédits à notre connaissance.</strong> Dix télégrammes de février–mars 1916, '
   'tirés des envois du ministère des Communications qui précèdent ceux qu\'a transcrits D. Bourdeau (JACAR B03050088000 à B03050088200)' + S21 + '. '
   'Ils se lisent avec les tables de condensateur déjà publiées (Shanghai, Qingdao, Manille)' + S1 + ' et une table nouvelle, « Thirteenth » '
   '(voir <a href="method.html#t1915">Méthode</a>). Les lettres ont été lues sur les scans par Claude et relues à l\'aveugle par Brice Dudout ; les deux '
   'lectures ont été fusionnées code par code, puis les caractères restés incertains ont été revus à l\'image. On y suit la maladie de Chen Qimei '
   '(et les conseils de Sun sur la méthode du Dr Takano), les fonds pour l\'action à Shanghai et la défection annoncée de Long Jiguang.</p>'),
   read='Lettres du formulaire (deux lectures fusionnées)', label='Traduction de travail.', stats='{tels} télégrammes, {codes} codes ; {douteux} douteux.'),
 'en': dict(title='February–March 1916: new decipherments', intro=(
   '<p><strong>New decipherments (October 2026), unpublished as far as we know.</strong> Ten telegrams of February–March 1916, '
   'from the batches of the Ministry of Communications that precede those transcribed by D. Bourdeau (JACAR B03050088000 to B03050088200)' + S21 + '. '
   'They read with the condenser tables already published (Shanghai, Qingdao, Manila)' + S1 + ' and a new table, “Thirteenth” '
   '(see <a href="method.html#t1915">Method</a>). The letters were read on the scans by Claude and reread blind by Brice Dudout; the two readings were '
   'merged code by code, then the characters left uncertain were checked again on the images. They follow Chen Qimei\'s illness (and Sun\'s advice on '
   'Dr Takano\'s method), the funds for the action in Shanghai and the expected defection of Long Jiguang.</p>'),
   read='Letters of the form (two readings merged)', label='Working translation.', stats='{tels} telegrams, {codes} codes; {douteux} doubtful.'),
 'zh-Hant': dict(title='1916年2—3月：新破譯的電報', intro=(
   '<p><strong>新破譯（2026年10月），就我們所知此前未曾發表。</strong>1916年2月至3月的十封電報，出自 D. Bourdeau 所轉錄卷宗之前的遞信省抄送卷宗'
   '（JACAR B03050088000 至 B03050088200）' + S21 + '。它們以已發表的壓縮碼表（上海、青島、馬尼拉）' + S1 + '及一張新碼表「Thirteenth」讀出'
   '（見<a href="method.html#t1915">破譯方法</a>）。字母由 Claude 依掃描件讀出，再由 Brice Dudout 盲讀；兩種讀法逐碼合併，仍存疑的字再對照圖像核查。'
   '電文中可見陳其美的病情（以及孫中山關於高野醫師療法的建議）、上海舉事的款項，以及龍濟光的叛離。</p>'),
   read='電報紙上的字母（兩種讀法合併）', label='工作譯文。', stats='電報{tels}封，電碼{codes}個；存疑{douteux}個。'),
 'zh-hans': dict(title='1916年2—3月：新破译的电报', intro=(
   '<p><strong>新破译（2026年10月），就我们所知此前未曾发表。</strong>1916年2月至3月的十封电报，出自 D. Bourdeau 所转录卷宗之前的递信省抄送卷宗'
   '（JACAR B03050088000 至 B03050088200）' + S21 + '。它们以已发表的压缩码表（上海、青岛、马尼拉）' + S1 + '及一张新码表“Thirteenth”读出'
   '（见<a href="method.html#t1915">破译方法</a>）。字母由 Claude 依扫描件读出，再由 Brice Dudout 盲读；两种读法逐码合并，仍存疑的字再对照图像核查。'
   '电文中可见陈其美的病情（以及孙中山关于高野医师疗法的建议）、上海举事的款项，以及龙济光的叛离。</p>')),
 'ja': dict(title='1916年2〜3月：新たな解読', intro=(
   '<p><strong>新たな解読（2026年10月）、管見の限り未公表。</strong>1916年2〜3月の電報10通。D. Bourdeau が翻字した送付分より前の逓信省の送付分'
   '（JACAR B03050088000〜B03050088200）' + S21 + 'から採った。公表済みの圧縮符号表（上海・青島・マニラ）' + S1 + 'と新しい表「Thirteenth」で読める'
   '（<a href="method.html#t1915">解読の方法</a>を参照）。文字は Claude がスキャンから読み、Brice Dudout がブラインドで読み直した。二つの読みを符号ごとに統合し、'
   'なお不確かな字は画像で再確認した。陳其美の病（と高野博士の療法をめぐる孫文の助言）、上海での行動資金、龍済光の離反の動きがたどれる。</p>'),
   read='用紙の文字（二つの読みを統合）', label='試訳。', stats='電報{tels}通、符号{codes}個。疑わしいもの{douteux}個。'),
}


def build():
    D = json.load(open(os.path.join(C35, 'f1916_data.json'), encoding='utf-8')); msgs = []
    for x in D:
        T = bkeys.KEYS[x['key']]
        ok, al, d, chars_s = BT.stream_of(x['cipher'], T, x['raw'])
        assert chars_s == x['raw'], (x['id'], al, chars_s, x['raw'])
        codes = [c for _, c in d]; chars = list(chars_s); nums = [int(c) if c.isdigit() else 0 for c in codes]
        letters = ''.join(l4 for l4, _ in d)
        text = x['read']; toks, props = BT.parse(text, chars)
        marked, i, k = set(), 0, 0
        while k < len(text):
            c = text[k]
            if c in BT.PUNCT: k += 1; continue
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
        mo, da = (int(v) for v in re.match(r'1916年(\d+)月(\d+)', x['date']['zh']).groups())
        msgs.append({'id': x['id'][1:], 'verified': [], 'label': n + SUFFIX.get(x['id'], ''), 'toc': x['key'], 'grid': x['key'],
                     'fiche': {'img': 'f' + n, 'n': n, 'keys': x['keyw']}, 'route': x['route']['en'],
                     'record': rec, 'md': [mo, da], 'page': int(img), 'time': None,
                     'letters': letters, 'codes': codes, 'chars': chars, 'status': status, 'fixed': {}, 'alts': alts, 'expected': {},
                     'readable': {'toks': [[c, i, p] for c, i, p in toks], 'props': out, 'score': [BC.mean_score(nums), BC.mean_score(after)]},
                     '_src': x})
    msgs.sort(key=lambda m: (m['md'][0], m['md'][1], m['label']))
    stats = {'tels': len(msgs), 'codes': sum(len(m['codes']) for m in msgs), 'douteux': sum(s == 'douteux' for m in msgs for s in m['status'])}
    i18n = {}
    for lang in LANGS:
        zh = 'zh' if lang.startswith('zh') else lang
        dd = dict(TXT[lang]); dd.update(channel=dict(KEYS[lang]), toc=dict(KEYS[lang]))
        dd['tr'] = {m['id']: m['_src']['tr'][lang] for m in msgs if lang in m['_src']['tr']}
        dd['date'] = {m['id']: m['_src']['date'].get(lang) or m['_src']['date'][zh] for m in msgs}
        dd['route'] = {m['id']: m['_src']['route'][SITE_LANG[lang]] for m in msgs}
        dd['who'] = {m['id']: who_html(m['_src']['id'], SITE_LANG[lang]) for m in msgs}
        i18n[lang] = dd
    T2 = c1916_i18n.t2s_table(WENMI)
    hans = c1916_i18n.to_hans({k: v for k, v in i18n['zh-Hant'].items() if k not in ('date', 'route', 'who', 'intro', 'title', 'channel', 'toc')}, T2)
    hans.update(date=dict(i18n['zh-Hant']['date']), title=TXT['zh-hans']['title'], intro=TXT['zh-hans']['intro'],
                channel=dict(KEYS['zh-hans']), toc=dict(KEYS['zh-hans']),
                route={m['id']: m['_src']['route']['zh-hans'] for m in msgs}, who={m['id']: who_html(m['_src']['id'], 'zh-hans') for m in msgs})
    i18n['zh-Hans'] = hans
    for m in msgs: del m['_src']
    open(os.path.join(SITE, 'assets', 'js', 'corpus-f1916.js'), 'w', encoding='utf-8').write(
        '// Généré par tools/build_f1916.py — ne pas éditer à la main.\n'
        'window.WENMI_F1916 = ' + json.dumps({'messages': msgs, 'stats': stats}, ensure_ascii=False) + ';\n'
        'window.WENMI_F1916_I18N = ' + json.dumps(i18n, ensure_ascii=False) + ';\n')
    print(stats)
    for m in msgs: print(m['id'], m['label'], m['md'], ''.join(m['chars']), [p['ch'] for p in m['readable']['props']])


if __name__ == '__main__':
    build()
