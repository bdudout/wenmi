#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nouveaux déchiffrements (octobre 2026) : télégrammes Tokyo → Shanghai (« Junzaburo ») de mai–juin 1916, chiffrés avec le
condensateur « Yamada » [1, 2] et absents des transcriptions publiées. Lettres lues sur les scans JACAR (lecture de Claude,
vérifiée lettre par lettre par Brice Dudout) : wenmi/cryptanalysis/site/n1916_streams.py.
Même format que corpus-c1916.js ; sortie : assets/js/corpus-n1916.js.
Usage : python3 tools/build_n1916.py <chemin du dossier d'enquête wenmi>"""
import json, os, sys

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'site'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_condensateurs as BC                      # noqa: E402  (fonctions communes : alts_for, edit_path, mean_score)
import restitution, c1916_i18n                        # noqa: E402
from n1916_streams import SEL                         # noqa: E402
bkeys = BC.bkeys; C2CH, uni, REF = BC.C2CH, BC.uni, BC.REF

# version lisible : {x} = proposition (≤ 2 lettres), ‹x› = caractère décodé laissé douteux
R = {
 'n0517': ('款三仟，可否給席正銘二仟、趙瑾卿五百？望覆。持。篠', []),
 'n0531a': ('軍用票辦法，速覆。持。卅。‹不›', []),
 'n0531b': ('美僑駐濱者小達六十，欲往濰縣‹俶›力，如何？盼覆。聞美支部存款甚多。‹顆›‹電›‹傑›', []),
 'n0601': ('寄魯芳債券照辦。軍用票事，覺生來電：東京如不能應急，則渠將自‹悽›‹云›‹亢›。持', []),
 'n0603': ('先生曁仲愷兄鑒：軍票事何不復？覺生連電急索。中央銀行票不作用，可‹叢›參印發行。持。江', []),
 'n0604': ('華僑己到六十餘，請示安置方法。持。江', []),
 'n0605a': ('廖先生鑒：弟促‹姊›何‹下›覆。‹紀›‹文›', []),
 'n0605b': ('濰縣函索飛機，尾崎已赴‹担›，請先生就近商議。澳款用‹伐›‹苤›‹嬲›‹名›', []),
 'n0607': ('袁賊旣死，速定大計。持決乘春日丸歸。', []),
 'n0615': ('電悉。不兌換可否加暫順券面？應否署名？{如}署，以何人爲宜？但先生署名恐有抵觸。弟可否隨券到‹逆›？‹兆›‹銘›又萱{野}偕坂本攜‹剪›‹風›機往‹餽›。'
           '機校由立花代理，學‹玤›中‹坵›無或‹勁›‹丸›望，坂本商‹顆›改換，速‹訏›‹重›‹民›‹删›', [('P', ['lecture', 'sens']), ('P', ['contexte'])]),
}
# codes rares pour le modèle de langue mais sûrs : (caractère → type)
CONF = {'n0517': {'仟': 'mot', '瑾': 'nom', '篠': 'date'}, 'n0531a': {'卅': 'date'}, 'n0531b': {'濰': 'nom'},
        'n0603': {'曁': 'variante', '愷': 'nom'}, 'n0605b': {'濰': 'nom'}, 'n0607': {'旣': 'variante'},
        'n0615': {'萱': 'nom', '偕': 'mot', '坂': 'nom'}}
KEYS = {'n0517': ['席正銘', '趙瑾卿', '持'], 'n0531a': ['軍用票'], 'n0531b': ['美僑', '濰縣', '美支部'], 'n0601': ['債券', '軍用票', '覺生'],
        'n0603': ['仲愷', '軍票', '中央銀行'], 'n0604': ['華僑', '安置'], 'n0605a': ['廖先生'], 'n0605b': ['濰縣', '飛機', '尾崎'],
        'n0607': ['袁賊旣死', '春日丸'], 'n0615': ['不兌換券', '署名', '萱野', '坂本', '機校', '立花']}
ROUTE = 'Tokyo → Shanghai (Junzaburo)'
SUP = c1916_i18n.SUP

LAB = {
 'fr': dict(
  title='Télégrammes nouvellement déchiffrés, mai–juin 1916',
  intro=('<p><strong>Nouveaux déchiffrements (octobre 2026), inédits à notre connaissance.</strong> Dix télégrammes envoyés de Tokyo à « Junzaburo » '
         '(Yamada Junzaburō, Shanghai) entre le 17 mai et le 15 juin 1916, chiffrés avec le condensateur « Yamada » déjà identifié' + SUP + ', mais '
         'absents des transcriptions publiées : ils se trouvent dans les envois suivants du ministère des Communications (JACAR B03050089000, '
         'B03050089200, B03050089400). Les lettres ont été lues sur les scans par Claude, puis vérifiées lettre par lettre à l\'image par Brice Dudout. '
         'La plupart sont signés <span lang="zh-Hant">持</span> (Xie Chi, 謝持) et datés par une rime qui concorde avec le formulaire. Ils forment un dossier '
         'cohérent : volontaires chinois d\'outre-mer, avions et école d\'aviation, bons militaires et billets, mort de Yuan Shikai.</p>'),
  read='Lettres du formulaire (lues sur le scan, vérifiées)', stats='{tels} télégrammes, {codes} codes ; {conf} codes rares mais confirmés, {douteux} douteux.',
  label='Traduction de travail.', channel={'yamada1916': 'Condensateur « Yamada » (Tokyo → Shanghai)'}),
 'en': dict(
  title='Newly deciphered telegrams, May–June 1916',
  intro=('<p><strong>New decipherments (October 2026), unpublished as far as we know.</strong> Ten telegrams sent from Tokyo to “Junzaburo” '
         '(Yamada Junzaburō, Shanghai) between 17 May and 15 June 1916, enciphered with the “Yamada” condenser already identified' + SUP + ', but '
         'absent from the published transcriptions: they are in the following batches of the Ministry of Communications (JACAR B03050089000, '
         'B03050089200, B03050089400). The letters were read on the scans by Claude, then checked letter by letter on the image by Brice Dudout. '
         'Most are signed <span lang="zh-Hant">持</span> (Xie Chi, 謝持) and dated by a rhyme that matches the form. Together they form a coherent '
         'file: overseas Chinese volunteers, aircraft and a flying school, military notes and banknotes, the death of Yuan Shikai.</p>'),
  read='Letters on the form (read on the scan, checked)', stats='{tels} telegrams, {codes} codes; {conf} rare but confirmed codes, {douteux} doubtful.',
  label='Working translation.', channel={'yamada1916': 'Condenser “Yamada” (Tokyo → Shanghai)'}),
 'zh-Hant': dict(
  title='新破譯的電報（1916年5月至6月）',
  intro=('<p><strong>新破譯（2026年10月），據我們所知尚未發表。</strong>1916年5月17日至6月15日由東京發往「Junzaburo」（上海山田純三郎）的十封電報，'
         '使用已知的「山田」壓縮碼' + SUP + '，但不見於已發表的轉寫：它們收在遞信省其後幾批送件中（JACAR B03050089000、B03050089200、B03050089400）。'
         '字母由 Claude 依掃描影像讀出，再由 Brice Dudout 對照影像逐字母核對。多數署名<span lang="zh-Hant">持</span>（謝持），韻目日期與電報紙相符。'
         '內容前後連貫：海外華僑志願者、飛機與飛行學校、軍票與紙幣、袁世凱之死。</p>'),
  read='電報紙上的字母（依掃描影像讀出並核對）', stats='{tels}封電報，{codes}個電碼；罕見但已確認{conf}個，存疑{douteux}個。',
  label='斷句與白話大意（工作譯文）。', channel={'yamada1916': '壓縮碼「山田」（東京 → 上海）'}),
 'ja': dict(
  title='新たに解読した電報（1916年5〜6月）',
  intro=('<p><strong>新たな解読（2026年10月）、管見の限り未公表。</strong>1916年5月17日から6月15日に東京から「Junzaburo」（上海の山田純三郎）へ送られた10通。'
         'すでに知られた「山田」圧縮符号' + SUP + 'で暗号化されているが、公開された翻字には含まれず、逓信省のその後の送付分（JACAR B03050089000、B03050089200、'
         'B03050089400）にある。文字は Claude が画像から読み、Brice Dudout が画像と一文字ずつ照合した。多くは<span lang="zh-Hant">持</span>（謝持）の署名で、'
         '韻目の日付が用紙と一致する。海外華僑の志願者、飛行機と飛行学校、軍票と紙幣、袁世凱の死という一貫した内容である。</p>'),
  read='用紙の文字（画像から読み、照合済み）', stats='{tels}通、{codes}コード。まれだが確認済み{conf}、疑わしい字{douteux}。',
  label='作業訳。', channel={'yamada1916': '圧縮符号「山田」（東京 → 上海）'}),
}

TR = {
 'fr': {
  'n0517': "Pour les 3 000 de fonds : peut-on en donner 2 000 à Xi Zhengming et 500 à Zhao Jinqing ? Réponds. — Chi (Xie Chi). Le 17.",
  'n0531a': "Au sujet des bons militaires (軍用票) : comment procéder ? Réponds vite. — Chi. Le 30.",
  'n0531b': "Les Chinois d'Amérique séjournant à Yokohama sont une soixantaine ; ils veulent aller à Weixian (濰縣) [servir (?)] : que faire ? Réponds. On apprend que la section d'Amérique [du parti] a beaucoup de fonds en dépôt. […]",
  'n0601': "Pour les obligations envoyées à Lufang (魯芳), faites comme prévu. Au sujet des bons militaires, Juesheng (Ju Zheng) télégraphie : si Tokyo ne peut faire face à l'urgence, il va lui-même […]. — Chi.",
  'n0603': "À Monsieur [Sun] et à frère Zhongkai (Liao Zhongkai) : pourquoi ne répondez-vous pas sur les bons militaires ? Juesheng (Ju Zheng) télégraphie sans cesse pour les réclamer d'urgence. Les billets de la Banque centrale ne servent à rien ; on peut [envisager] de les faire imprimer et émettre. — Chi. Le 3.",
  'n0604': "Plus de soixante Chinois d'outre-mer sont déjà arrivés ; indiquez comment les installer. — Chi. Le 3.",
  'n0605a': "À Monsieur Liao : […] répondez. […]",
  'n0605b': "Weixian demande des avions par lettre ; Ozaki est déjà parti pour […] ; prière à Monsieur de se concerter sur place. Les fonds de Macao (?) […]",
  'n0607': "Yuan le traître est mort : arrêtez vite le grand plan. Chi a décidé de rentrer par le Kasuga-maru.",
  'n0615': "Télégramme reçu. Les billets non convertibles : peut-on ajouter au recto la mention « billet provisoire » ? Faut-il les signer ? Si oui, qui vaut-il mieux faire signer ? Mais la signature de Monsieur [Sun] risque de poser problème. Puis-je partir avec les billets ? […] Kayano (萱野), avec Sakamoto (坂本), emporte […] avion(s) vers […]. L'école d'aviation est confiée à titre provisoire à Tachibana (立花) […].",
 },
 'en': {
  'n0517': "As for the 3,000 in funds: may 2,000 be given to Xi Zhengming and 500 to Zhao Jinqing? Reply. — Chi (Xie Chi). The 17th.",
  'n0531a': "About the military notes (軍用票): how should we proceed? Reply quickly. — Chi. The 30th.",
  'n0531b': "The American Chinese staying in Yokohama number about sixty; they want to go to Weixian (濰縣) [to serve (?)]: what should be done? Reply. We hear that the American branch [of the party] has a great deal of funds on deposit. […]",
  'n0601': "For the bonds sent to Lufang (魯芳), proceed as planned. About the military notes, Juesheng (Ju Zheng) telegraphs: if Tokyo cannot meet the emergency, he will himself […]. — Chi.",
  'n0603': "To Sir [Sun] and brother Zhongkai (Liao Zhongkai): why no reply about the military notes? Juesheng (Ju Zheng) keeps telegraphing to demand them urgently. The Central Bank notes are of no use; we could [consider] having them printed and issued. — Chi. The 3rd.",
  'n0604': "More than sixty overseas Chinese have already arrived; please say how to accommodate them. — Chi. The 3rd.",
  'n0605a': "To Mr Liao: […] reply. […]",
  'n0605b': "Weixian asks for aircraft by letter; Ozaki has already left for […]; please, Sir, consult on the spot. The Macao (?) funds […]",
  'n0607': "Yuan the traitor is dead: settle the great plan quickly. Chi has decided to return on the Kasuga-maru.",
  'n0615': "Telegram received. The inconvertible notes: may 'provisional note' be added on the face? Should they be signed? If so, who would be best to sign? But Sir [Sun]'s signature might cause problems. May I travel with the notes? […] Kayano (萱野), together with Sakamoto (坂本), takes […] aircraft to […]. The flying school is entrusted for the time being to Tachibana (立花) […].",
 },
 'zh-Hant': {
  'n0517': "款三仟，可否給席正銘二仟、趙瑾卿五百？望覆。持。篠（十七日）。",
  'n0531a': "軍用票辦法，速覆。持。卅（三十日）。",
  'n0531b': "旅居橫濱的美洲華僑約六十人，欲往濰縣效力（？），如何？盼覆。聞美洲支部存款甚多。……",
  'n0601': "寄魯芳之債券照辦。軍用票事，覺生（居正）來電：東京如不能應急，則渠將自……。持。",
  'n0603': "先生暨仲愷兄鑒：軍票事何以不覆？覺生連電急索。中央銀行票不作用，可……印發行。持。江（三日）。",
  'n0604': "華僑已到六十餘人，請示安置方法。持。江（三日）。",
  'n0605a': "廖先生鑒：……覆。……",
  'n0605b': "濰縣來函索飛機，尾崎已赴……，請先生就近商議。澳款……",
  'n0607': "袁賊既死，速定大計。持決乘春日丸歸。",
  'n0615': "電悉。不兌換券可否加「暫順券」於券面？應否署名？如署，以何人為宜？但先生署名恐有抵觸。弟可否隨券到……？……萱野偕坂本攜……機往……。飛機學校由立花代理……。",
 },
 'ja': {
  'n0517': "資金三千のうち、席正銘に二千、趙瑾卿に五百を与えてよいか。返電を。持（謝持）。篠（17日）。",
  'n0531a': "軍用票の件、どうするか。至急返電を。持。卅（30日）。",
  'n0531b': "横浜に滞在する米国華僑は約60人、濰県へ行き尽力（？）したいという。どうするか。返電を。米国支部には預金が多いと聞く。……",
  'n0601': "魯芳へ送った債券は予定どおり処理されたい。軍用票の件、覚生（居正）から電報：東京が急に応じられないなら、彼自身が……。持。",
  'n0603': "先生および仲愷兄へ：軍票の件、なぜ返事がないのか。覚生がしきりに電報で至急求めている。中央銀行券は役に立たない。……印刷・発行してはどうか。持。江（3日）。",
  'n0604': "華僑がすでに60余人到着した。収容の方法を指示されたい。持。江（3日）。",
  'n0605a': "廖先生へ：……返電を。……",
  'n0605b': "濰県から書簡で飛行機を求めてきた。尾崎はすでに……へ向かった。先生には現地で協議されたい。澳門（？）の資金……",
  'n0607': "袁賊はすでに死んだ。速やかに大計を定められたい。持は春日丸で帰ることに決めた。",
  'n0615': "電報拝見。兌換されない券に「暫順券」と券面に加えてよいか。署名すべきか。署名するなら誰がよいか。ただし先生の署名は差し支えがあるかもしれない。私が券とともに……へ行ってよいか。……萱野は坂本とともに飛行機を……へ持って行く。飛行学校は立花が代理……。",
 },
}

def build():
    msgs = []
    for sid, rec, page, (mo, da), tm, s, prefix in SEL:
        T = bkeys.KEYS['yamada1916']
        d = bkeys.decode(s, 'yamada1916'); codes = [c for _, c in d]; chars = [C2CH[c] for c in codes]; nums = [int(c) for c in codes]
        letters = ''.join(syl for syl, _ in d)
        text, levels = R[sid]
        toks, props = restitution.parse(text, chars)
        assert len(props) == len(levels), sid
        marked, i, k = set(), 0, 0
        while k < len(text):
            c = text[k]
            if c in restitution.PUNCT: k += 1; continue
            if c in '{‹':
                if c == '‹': marked.add(i)
                i += 1; k += 3; continue
            i += 1; k += 1
        status = []
        for i, c in enumerate(codes):
            rare = float(uni[nums[i]]) - REF < 1; cf = CONF.get(sid, {}).get(chars[i])
            if rare and cf and i not in marked: status.append('confirmé:' + cf)
            elif rare or i in marked or i in props: status.append('douteux')
            else: status.append('ok')
        alts = {str(i): a for i, st in enumerate(status) if st == 'douteux' and i not in props for a in [BC.alts_for(letters, i, nums, T)] if a}
        out = []
        for (lvl, reasons), i in zip(levels, props):
            ch = next(t[0] for t in toks if t[1] == i and t[2])
            ep = BC.edit_path(letters[4 * i:4 * i + 4], T, ch)
            assert ep and len(ep['edits']) <= 2, (sid, i, ch, ep)
            out.append(dict(i=i, ch=ch, orig=chars[i], level=lvl, reasons=reasons, letters=letters[4 * i:4 * i + 4], image='divergente' if sid == 'n0615' and ch == '如' else None, **ep))
        after = list(nums)
        for p in out: after[p['i']] = int(p['code'])
        msgs.append({'id': sid, 'label': '%02d/%02d' % (da, mo), 'grid': 'yamada1916', 'route': ROUTE, 'record': rec, 'md': [mo, da], 'page': page,
                     'time': tm, 'prefix': prefix, 'letters': letters, 'codes': codes, 'chars': chars, 'status': status, 'fixed': {}, 'alts': alts,
                     'expected': {}, 'readable': {'toks': [[c, i, p] for c, i, p in toks], 'props': out, 'score': [BC.mean_score(nums), BC.mean_score(after)]}})
    stats = {'tels': len(msgs), 'codes': sum(len(m['codes']) for m in msgs), 'douteux': sum(s == 'douteux' for m in msgs for s in m['status']),
             'confirmé': sum(s.startswith('confirmé') for m in msgs for s in m['status'])}
    T2 = c1916_i18n.t2s_table(WENMI); i18n = {}
    for lang in ('fr', 'en', 'zh-Hant', 'ja'):
        dd = dict(LAB[lang]); dd['tr'] = dict(TR[lang]); dd['date'] = {m['id']: c1916_i18n.date_of(lang, *m['md']) + ', ' + m['time'] for m in msgs}
        assert set(dd['tr']) == {m['id'] for m in msgs}; i18n[lang] = dd
    hans = c1916_i18n.to_hans({k: v for k, v in i18n['zh-Hant'].items() if k != 'date'}, T2); hans['date'] = dict(i18n['zh-Hant']['date']); i18n['zh-Hans'] = hans
    open(os.path.join(SITE, 'assets', 'js', 'corpus-n1916.js'), 'w', encoding='utf-8').write(
        '// Généré par tools/build_n1916.py — ne pas éditer à la main.\n'
        'window.WENMI_N1916 = ' + json.dumps({'messages': msgs, 'stats': stats}, ensure_ascii=False) + ';\n'
        'window.WENMI_N1916_I18N = ' + json.dumps(i18n, ensure_ascii=False) + ';\n')
    print(stats)
    for m in msgs: print(m['id'], ''.join(m['chars']), [p['ch'] for p in m['readable']['props']])

if __name__ == '__main__':
    build()
