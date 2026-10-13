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
from n1916_streams import SEL, EXTRA_KEYS, KEY, ROUTE as ROUTES, LOCAL, IMG_OFFSET, POS   # noqa: E402
bkeys = BC.bkeys; C2CH, uni, REF = BC.C2CH, BC.uni, BC.REF
for _k, _t in EXTRA_KEYS.items(): bkeys.KEYS.setdefault(_k, _t)
# variante « Aloha » de la clé « Honolulu » (Bourdeau) : w à la place de v (Honolulu → Tokyo, avril 1916, signé 鐵城)
bkeys.KEYS.setdefault('honolulu1916w', {**bkeys.KEYS['honolulu1916'], **{'w' + v: bkeys.KEYS['honolulu1916']['v' + v] for v in 'aeiou'}})
def edit_path_alias(l4, T, target):
    """comme BC.edit_path, mais parmi les syllabes de même valeur (w/v, w/p…) garde celle qui est écrite si elle convient"""
    by = {}
    for k, v in T.items(): by.setdefault(v, []).append(k)
    best = None
    for code in BC.CH2CODES.get(target, []):
        a, b = int(code[:2]), int(code[2:])
        if a not in by or b not in by: continue
        cost = lambda x, o: (sum(p != q for p, q in zip(x, o)), x[0] not in BC.CONS)   # à égalité : la lettre de référence (p, v…)
        h1 = min(by[a], key=lambda x: cost(x, l4[:2])); h2 = min(by[b], key=lambda x: cost(x, l4[2:]))
        tgt = h1 + h2; d = [k for k in range(4) if l4[k] != tgt[k]]
        if best is None or len(d) < len(best[1]): best = (code, d, tgt)
    if best is None: return None
    code, d, tgt = best
    return {'code': code, 'to_letters': tgt, 'edits': [{'from': l4[k], 'to': tgt[k], 'kind': BC.kind_of(l4[k], tgt[k]),
            'morse': [BC.MORSE[l4[k]], BC.MORSE[tgt[k]]]} for k in d]}
CH = lambda c: C2CH.get(c, '□')                      # code absent du code télégraphique standard

# version lisible : {x} = proposition (≤ 2 lettres), ‹x› = caractère décodé laissé douteux
R = {
 'n0517': ('款三仟，可否給席正銘二仟、趙瑾卿五百？望覆。持。篠', []),
 'n0531a': ('軍用票辦法，速覆。持。卅。‹不›', []),
 'n0531b': ('美僑駐濱者小達六十，欲往濰縣‹俶›力，如何？盼覆。聞美支部存款甚多。‹顆›‹電›‹傑›', []),
 'n0601': ('寄魯芳債券照辦。軍用票事，覺生來電：東京如不能應急，則渠將自印云‹亢›。持', []),
 'n0603': ('先生曁仲愷兄鑒：軍票事何不復？覺生連電急索。中央銀行票不作用，可‹叢›參印發行。持。江', []),
 'n0604': ('華僑己到六十餘，請示安置方法。持。江', []),
 'n0605a': ('廖先生鑒：弟促‹姊›何‹下›覆。‹紀›‹文›', []),
 'n0605b': ('濰縣函索飛機，尾崎已赴‹担›，請先生就近商議。澳款用‹伐›‹苤›‹嬲›‹名›', []),
 'n0607': ('袁賊旣死，速定大計。持決乘春日丸歸。', []),
 'n0615': ('電悉。不兌換可否加暫順券面？應否署名？{如}署，以何人爲宜？但先生署名恐有抵觸。弟可否隨券到‹逆›？‹兆›‹銘›又萱野偕坂本攜‹剪›‹風›機往‹餽›。'
           '機校由立花代理，學生中‹坵›無或‹勁›之望，坂本商‹説›改換，速覆。‹重›‹民›‹删›', [('P', ['lecture', 'sens'])]),
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
  title='Télégrammes nouvellement déchiffrés, avril–juin 1916',
  intro=('<p><strong>Nouveaux déchiffrements (octobre 2026), inédits à notre connaissance.</strong> Dix télégrammes envoyés de Tokyo à « Junzaburo » '
         '(Yamada Junzaburō, Shanghai) entre le 17 mai et le 15 juin 1916, chiffrés avec le condensateur « Yamada » déjà identifié' + SUP + ', mais '
         'absents des transcriptions publiées : ils se trouvent dans les envois suivants du ministère des Communications (JACAR B03050089000, '
         'B03050089200, B03050089400). Les lettres ont été lues sur les scans par Claude, puis vérifiées lettre par lettre à l\'image par Brice Dudout. '
         'La plupart sont signés <span lang="zh-Hant">持</span> (Xie Chi, 謝持) et datés par une rime qui concorde avec le formulaire. Ils forment un dossier '
         'cohérent : volontaires chinois d\'outre-mer, avions et école d\'aviation, bons militaires et billets, mort de Yuan Shikai.</p>'),
  read='Lettres du formulaire (lues sur le scan, vérifiées)', stats='{tels} télégrammes, {codes} codes ; {conf} codes rares mais confirmés, {douteux} douteux.',
  label='Traduction de travail.', channel={'yamada1916': 'Condensateur « Yamada » (Tokyo → Shanghai)'}),
 'en': dict(
  title='Newly deciphered telegrams, April–June 1916',
  intro=('<p><strong>New decipherments (October 2026), unpublished as far as we know.</strong> Ten telegrams sent from Tokyo to “Junzaburo” '
         '(Yamada Junzaburō, Shanghai) between 17 May and 15 June 1916, enciphered with the “Yamada” condenser already identified' + SUP + ', but '
         'absent from the published transcriptions: they are in the following batches of the Ministry of Communications (JACAR B03050089000, '
         'B03050089200, B03050089400). The letters were read on the scans by Claude, then checked letter by letter on the image by Brice Dudout. '
         'Most are signed <span lang="zh-Hant">持</span> (Xie Chi, 謝持) and dated by a rhyme that matches the form. Together they form a coherent '
         'file: overseas Chinese volunteers, aircraft and a flying school, military notes and banknotes, the death of Yuan Shikai.</p>'),
  read='Letters on the form (read on the scan, checked)', stats='{tels} telegrams, {codes} codes; {conf} rare but confirmed codes, {douteux} doubtful.',
  label='Working translation.', channel={'yamada1916': 'Condenser “Yamada” (Tokyo → Shanghai)'}),
 'zh-Hant': dict(
  title='新破譯的電報（1916年4月至6月）',
  intro=('<p><strong>新破譯（2026年10月），據我們所知尚未發表。</strong>1916年5月17日至6月15日由東京發往「Junzaburo」（上海山田純三郎）的十封電報，'
         '使用已知的「山田」壓縮碼' + SUP + '，但不見於已發表的轉寫：它們收在遞信省其後幾批送件中（JACAR B03050089000、B03050089200、B03050089400）。'
         '字母由 Claude 依掃描影像讀出，再由 Brice Dudout 對照影像逐字母核對。多數署名<span lang="zh-Hant">持</span>（謝持），韻目日期與電報紙相符。'
         '內容前後連貫：海外華僑志願者、飛機與飛行學校、軍票與紙幣、袁世凱之死。</p>'),
  read='電報紙上的字母（依掃描影像讀出並核對）', stats='{tels}封電報，{codes}個電碼；罕見但已確認{conf}個，存疑{douteux}個。',
  label='斷句與白話大意（工作譯文）。', channel={'yamada1916': '壓縮碼「山田」（東京 → 上海）'}),
 'ja': dict(
  title='新たに解読した電報（1916年4〜6月）',
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
  'n0601': "Pour les obligations envoyées à Lufang (魯芳), faites comme prévu. Au sujet des bons militaires, Juesheng (Ju Zheng) télégraphie : si Tokyo ne peut faire face à l'urgence, il les fera imprimer lui-même, dit-il […]. — Chi.",
  'n0603': "À Monsieur [Sun] et à frère Zhongkai (Liao Zhongkai) : pourquoi ne répondez-vous pas sur les bons militaires ? Juesheng (Ju Zheng) télégraphie sans cesse pour les réclamer d'urgence. Les billets de la Banque centrale ne servent à rien ; on peut [envisager] de les faire imprimer et émettre. — Chi. Le 3.",
  'n0604': "Plus de soixante Chinois d'outre-mer sont déjà arrivés ; indiquez comment les installer. — Chi. Le 3.",
  'n0605a': "À Monsieur Liao : […] répondez. […]",
  'n0605b': "Weixian demande des avions par lettre ; Ozaki est déjà parti pour […] ; prière à Monsieur de se concerter sur place. Les fonds de Macao (?) […]",
  'n0607': "Yuan le traître est mort : arrêtez vite le grand plan. Chi a décidé de rentrer par le Kasuga-maru.",
  'n0615': "Télégramme reçu. Les billets non convertibles : peut-on ajouter au recto la mention « billet provisoire » ? Faut-il les signer ? Si oui, qui vaut-il mieux faire signer ? Mais la signature de Monsieur [Sun] risque de poser problème. Puis-je partir avec les billets ? […] Kayano (萱野), avec Sakamoto (坂本), emporte […] avion(s) vers […]. L'école d'aviation est confiée à titre provisoire à Tachibana (立花) ; parmi les élèves, […] aucun espoir […]. Sakamoto propose (?) de changer […] ; répondez vite. […]",
 },
 'en': {
  'n0517': "As for the 3,000 in funds: may 2,000 be given to Xi Zhengming and 500 to Zhao Jinqing? Reply. — Chi (Xie Chi). The 17th.",
  'n0531a': "About the military notes (軍用票): how should we proceed? Reply quickly. — Chi. The 30th.",
  'n0531b': "The American Chinese staying in Yokohama number about sixty; they want to go to Weixian (濰縣) [to serve (?)]: what should be done? Reply. We hear that the American branch [of the party] has a great deal of funds on deposit. […]",
  'n0601': "For the bonds sent to Lufang (魯芳), proceed as planned. About the military notes, Juesheng (Ju Zheng) telegraphs: if Tokyo cannot meet the emergency, he will have them printed himself, he says […]. — Chi.",
  'n0603': "To Sir [Sun] and brother Zhongkai (Liao Zhongkai): why no reply about the military notes? Juesheng (Ju Zheng) keeps telegraphing to demand them urgently. The Central Bank notes are of no use; we could [consider] having them printed and issued. — Chi. The 3rd.",
  'n0604': "More than sixty overseas Chinese have already arrived; please say how to accommodate them. — Chi. The 3rd.",
  'n0605a': "To Mr Liao: […] reply. […]",
  'n0605b': "Weixian asks for aircraft by letter; Ozaki has already left for […]; please, Sir, consult on the spot. The Macao (?) funds […]",
  'n0607': "Yuan the traitor is dead: settle the great plan quickly. Chi has decided to return on the Kasuga-maru.",
  'n0615': "Telegram received. The inconvertible notes: may 'provisional note' be added on the face? Should they be signed? If so, who would be best to sign? But Sir [Sun]'s signature might cause problems. May I travel with the notes? […] Kayano (萱野), together with Sakamoto (坂本), takes […] aircraft to […]. The flying school is entrusted for the time being to Tachibana (立花); among the students, […] no hope […]. Sakamoto suggests (?) changing […]; reply quickly. […]",
 },
 'zh-Hant': {
  'n0517': "款三仟，可否給席正銘二仟、趙瑾卿五百？望覆。持。篠（十七日）。",
  'n0531a': "軍用票辦法，速覆。持。卅（三十日）。",
  'n0531b': "旅居橫濱的美洲華僑約六十人，欲往濰縣效力（？），如何？盼覆。聞美洲支部存款甚多。……",
  'n0601': "寄魯芳之債券照辦。軍用票事，覺生（居正）來電：東京如不能應急，則渠將自印云……。持。",
  'n0603': "先生暨仲愷兄鑒：軍票事何以不覆？覺生連電急索。中央銀行票不作用，可……印發行。持。江（三日）。",
  'n0604': "華僑已到六十餘人，請示安置方法。持。江（三日）。",
  'n0605a': "廖先生鑒：……覆。……",
  'n0605b': "濰縣來函索飛機，尾崎已赴……，請先生就近商議。澳款……",
  'n0607': "袁賊既死，速定大計。持決乘春日丸歸。",
  'n0615': "電悉。不兌換券可否加「暫順券」於券面？應否署名？如署，以何人為宜？但先生署名恐有抵觸。弟可否隨券到……？……萱野偕坂本攜……機往……。飛機學校由立花代理，學生中……無或……之望。坂本商（？）改換……，速覆。……",
 },
 'ja': {
  'n0517': "資金三千のうち、席正銘に二千、趙瑾卿に五百を与えてよいか。返電を。持（謝持）。篠（17日）。",
  'n0531a': "軍用票の件、どうするか。至急返電を。持。卅（30日）。",
  'n0531b': "横浜に滞在する米国華僑は約60人、濰県へ行き尽力（？）したいという。どうするか。返電を。米国支部には預金が多いと聞く。……",
  'n0601': "魯芳へ送った債券は予定どおり処理されたい。軍用票の件、覚生（居正）から電報：東京が急に応じられないなら、彼自身が印刷するという……。持。",
  'n0603': "先生および仲愷兄へ：軍票の件、なぜ返事がないのか。覚生がしきりに電報で至急求めている。中央銀行券は役に立たない。……印刷・発行してはどうか。持。江（3日）。",
  'n0604': "華僑がすでに60余人到着した。収容の方法を指示されたい。持。江（3日）。",
  'n0605a': "廖先生へ：……返電を。……",
  'n0605b': "濰県から書簡で飛行機を求めてきた。尾崎はすでに……へ向かった。先生には現地で協議されたい。澳門（？）の資金……",
  'n0607': "袁賊はすでに死んだ。速やかに大計を定められたい。持は春日丸で帰ることに決めた。",
  'n0615': "電報拝見。兌換されない券に「暫順券」と券面に加えてよいか。署名すべきか。署名するなら誰がよいか。ただし先生の署名は差し支えがあるかもしれない。私が券とともに……へ行ってよいか。……萱野は坂本とともに飛行機を持って……へ行く。飛行学校は立花が代理する。学生のうち……の望みはない……。坂本は……の変更を相談（？）。至急返電を。……",
 },
}

# ---- Lot du début mai 1916 (B03050089000) : lecture de Claude seule (13/10/2026), pas encore vérifiée à l'image par Brice ----
R.update({
 'n0503a': ('抵滬平安否？港拯日函、江門得而覆失。金山‹倭›羅芳‹潑›崙代表馬醒‹馨›‹筊›三{人}昨日到東，可否促其赴{滬}？兆銘{擬}覓杜石助寫債券，請詢仲愷兄可否照辦。江', []),
 'n0503b': ('‹紉›秋乘博愛丸赴滬。持。‹復›', []),
 'n0504a': ('‹卲›子峯{來}電：懷仁描事王煥夏於四月儉日率懷專兩縣軍譚五百獨立，然勢力‹蘇›敗，擬將人械沿鴨綠江運至安東租界，再募數千待命。運很他芳，望速覆。‹亢›‹云›請示辦法，便辨覆。'
            '應時因坂本事改乘春日丸，決宅‹□›日開懇親會。持', []),
 'n0504b': ('有現款六仟，是否匯{滬}？‹帷›日人深谷來詢統一兄與中須賀之五浮能{否}實行。望覆。持。支', []),
 'n0506': ('楊丙交天津電：學生已到百貴人，需款{至}急。‹芰›覆。魚', []),
 'n0508': ('昨夜得覺生電稱：四日占誌周村，{本}軍以{同}日攻濰縣城，五日占其東關，正午稍却，晚復決計圍境，占領附近泌落，士氣頗壯。特轉。‹弼›邵子峯遮義之軍‹警›可上，今其運適山東。'
           '‹椒›丙又接津難‹傞›款，請速辦。持。齊', []),
 'n0510': ('克強昨日到，避人，尚未晤。‹□›‹惟›孟碩乘原船適滬。{請}以‹底›‹正›舉{事}。山東電告金山至要。持。{灰}', []),
 'n0512': ('箱已交犬塚，十五日附法船來。若有要事，請{電}如下：', []),
 'n0511': ('聞張繼已回日，頗奇，{是}否？', []),
 'n0515': ('今日晤克強，頗稱先生‹但›赴滬從緩。又言參部局長某謂：山東事革軍軍隊過少，不增，且將議和，則其國外交殊{難}著手，擬緩其幫助之力。經換答{以}軍隊忠壘，決不苟和，務請積極幫助。'
           '某始‹醛›，特電{請}亟謀擴充軍隊。再，席正銘急電{請}款，摘原電如下：保軍校{來}津填誓約已逾百人，{代}表終對服從，已囑‹涕›中拒絶。外派點段鉅{款}買收也。定‹嬙›五給憑分遣，'
           '釐速寄萬圓。模肘團南逸‹苑›人保等軍確有可爲。‹亢›‹亢›現{在}宜圖天津。持。删', []),
 's0505': ('江日官抵滬，馬代表等可來{滬}。並請速備百圓券二萬、十圓八萬、一圓五圓各‹不›萬，交春洋丸{帶}港，‹耻›義會‹曝›交梅喬林收。帳券人請兄酌奪。文', []),
 's0506': ('{請}覆邵：地點未備，人緩招募，械則安置安東，待時而用。款六千由正金購。所持人‹拂›票寄‹愷›', []),
 's0508': ('已{到}津學生請酌撥款維持，{待}得濟南令役餘‹孌›。楊丙停歷招集。邵事目前不能辦，本部文下足則六十勿匯奶也。齊', []),
 's0515': ('速辰十圓、百圓券各二{萬}，加福建專用章，交陳羣轉黃展雲。此間款盡，難再籌。請‹韞›覆各處', []),
 'h0430': ('{黃}{轉}到{日}，換船{赴}滬。鐵城', []),
 'm0503': ('款匯港，債券無存，請‹皤›趣漢‹苞›‹擎›券伍仟圓、証書及{陞}等功章速附佳弟。擬日間回國。誠叩', []),
})

P_, Q_ = lambda *r: ('P', list(r)), lambda *r: ('Q', list(r))
_LV = {'n0503a': [P_('sens'), P_('sens', 'contexte'), Q_('sens')], 'n0510': [P_('sens'), P_('sens'), P_('structure')], 'n0511': [P_('sens', 'structure')], 'h0430': [Q_('contexte'), P_('sens'), P_('sens'), P_('sens')], 'n0512': [P_('sens')], 'n0504a': [P_('structure', 'sens')],
       'n0504b': [P_('sens', 'contexte'), P_('sens')], 'n0506': [P_('sens')], 'n0508': [Q_('sens'), P_('sens', 'lecture')], 'n0515': [P_('sens')] * 8,
       's0505': [P_('sens', 'contexte'), Q_('sens')], 's0506': [Q_('sens')], 's0508': [P_('sens'), Q_('sens')], 's0515': [P_('sens', 'contexte')],
       'm0503': [P_('sens', 'jumeau')]}
# propositions maintenues alors que la relecture de Brice (lot V7) ne les voit pas sur l'image
DIVERGE = {('n0503a', '滬'), ('n0503a', '擬'), ('n0615', '如'), ('n0515', '款'), ('s0515', '萬'), ('s0508', '到'), ('m0503', '陞')}
for _sid, _lv in _LV.items(): R[_sid] = (R[_sid][0], _lv)
CONF.update({'n0503a': {'愷': 'nom', '江': 'date'}, 'n0512': {'塚': 'nom'}, 'n0504a': {'卲': 'variante', '儉': 'date', '坂': 'nom'}, 'n0504b': {'仟': 'mot', '支': 'date'},
             'n0508': {'占': 'mot', '濰': 'nom', '却': 'variante'}, 'n0515': {'絶': 'variante', '删': 'date'}, 'm0503': {'仟': 'mot', '証': 'variante'}})
KEYS.update({'n0503a': ['兆銘', '債券', '仲愷'], 'n0503b': ['博愛丸'], 'n0504a': ['邵子峯', '王煥夏', '鴨綠江', '安東', '坂本', '春日丸'],
             'n0504b': ['現款六仟', '深谷', '中須賀'], 'n0506': ['楊丙', '天津', '學生'], 'n0508': ['覺生', '周村', '濰縣', '邵子峯'],
             'n0510': ['克強', '避人', '舉事', '金山'], 'n0512': ['犬塚', '法船'], 'n0511': ['張繼', '回日'], 'h0430': ['黃', '換船', '鐵城'], 'n0515': ['克強', '參謀部', '席正銘', '保定軍校', '天津'],
             's0505': ['百圓券', '春洋丸', '梅喬林', '文'], 's0506': ['邵', '安東', '正金'], 's0508': ['學生', '濟南', '楊丙', '邵'],
             's0515': ['福建', '陳羣', '黃展雲'], 'm0503': ['債券', '陞等功章', '誠']})
_MAI = {
 'fr': {
  'n0503a': "Bien arrivé à Shanghai ? […] la lettre de Jiangmen a été reçue, mais la réponse s'est perdue (?). De San Francisco (金山), […] Luo Fang […] et les représentants Ma Xing […], trois personnes, sont arrivés hier au Japon : peut-on les presser de se rendre à Shanghai ? [Wang] Zhaoming compte trouver Du Shi pour aider à rédiger les obligations ; demandez à frère [Liao] Zhongkai s'il peut s'en charger. — Le 3.",
  'n0503b': "[…]qiu prend le Hakuai-maru pour Shanghai. — Chi. […]",
  'n0504a': "Shao Zifeng télégraphie : à Huairen, Wang Huanxia a mené le 28 avril [les troupes de] deux districts, [Huairen] et […], cinq cents [hommes], qui se sont déclarés indépendants (獨立) ; mais leurs forces ayant été défaites (?), il compte acheminer hommes et armes le long du Yalu jusqu'à la concession d'Andong, recruter encore plusieurs milliers d'hommes et attendre les ordres. […] Réponds vite. […] Demande d'instructions : répondez. À cause de l'affaire Sakamoto, [je] prends plutôt le Kasuga-maru ; on a décidé de tenir une réunion amicale le […]. — Chi.",
  'n0504b': "Il y a 6 000 en espèces : faut-il les virer à Shanghai ? […] Le Japonais Fukaya (深谷) est venu demander si l'unification [proposée par] frère […] et Nakasuga (中須賀) […] peut être réalisée. Réponds. — Chi. Le 4.",
  'n0506': "Yang Bing transmet un télégramme de Tianjin : les étudiants arrivés sont une centaine (?) ; il faut des fonds de toute urgence. […] Réponds. — Le 6.",
  'n0508': "Hier soir, télégramme de Juesheng (Ju Zheng) : le 4, [nous avons] pris Zhoucun (周村) ; notre armée a attaqué la ville de Weixian le même jour (?) ; le 5, [nous avons] pris sa porte Est ; à midi léger recul ; le soir, [nous avons] décidé d'encercler [la ville] et occupé les villages voisins ; le moral est excellent. Je transmets. […] [L'armée] de Shao Zifeng […] est maintenant en route vers le Shandong. [Yang] Bing a aussi reçu de Tianjin une demande pressante de fonds : agissez vite. — Chi. Le 8.",
  'n0510': "Keqiang (Huang Xing) est arrivé hier ; il évite les visiteurs, je ne l'ai pas encore vu. […] Mengshuo (孟碩) a pris le même navire pour Shanghai. Prière de […] lancer l'action. Il est essentiel de télégraphier les nouvelles du Shandong à San Francisco (金山). — Chi. Le 10.",
  'n0512': "La caisse a été remise à Inuzuka (犬塚) ; elle partira le 15 par un navire français. Pour toute affaire urgente, télégraphier à l'adresse suivante : [adresse en clair, non lue].",
  'n0511': "J'apprends que Zhang Ji (張繼) est rentré au Japon ; c'est très surprenant — est-ce vrai ?",
  'n0515': "Vu aujourd'hui Keqiang (Huang Xing) : il insiste pour que la venue de Monsieur [Sun] à Shanghai soit différée. Il dit aussi qu'un chef de bureau (局長) de l'état-major a déclaré : au Shandong, les troupes de l'armée révolutionnaire sont trop peu nombreuses ; si elles n'augmentent pas et qu'on en vient à négocier la paix, la diplomatie de son pays aura bien du mal à agir, et il compte ralentir son aide. [Keqiang] a répondu que les troupes sont loyales et ne feront jamais une paix de compromis, et demandé une aide active. L'autre a alors […], et [Keqiang] télégraphie spécialement pour demander qu'on étende d'urgence les troupes. Par ailleurs, Xi Zhengming demande des fonds par télégramme urgent ; extrait de l'original : les élèves de l'école militaire [de Baoding] venus à Tianjin et ayant signé un engagement (誓約) dépassent la centaine ; leurs représentants jurent obéissance ; je leur ai dit de refuser […]. Au-dehors, on dépense de grosses sommes pour les acheter. [J'ai] fixé […] cinq, donné des certificats et réparti [les hommes] ; envoyez vite dix mille yuans. […] Les troupes de Bao et d'autres ont réellement de quoi faire. Il faut maintenant viser Tianjin. — Chi. Le 15.",
  's0505': "Le 3, […] est arrivé à Shanghai ; les représentants Ma et autres peuvent venir à Shanghai. Préparez aussi vite des billets : 20 000 de 100 yuans, 80 000 de 10 yuans, et […] de 1 et de 5 yuans chacun, à remettre au Harunoyō-maru (春洋丸) pour les porter à Hong Kong ; […] à remettre à Mei Qiaolin (梅喬林). Pour [les responsables] des comptes et des billets, je te laisse en décider, frère. — Wen (Sun Yat-sen).",
  's0506': "Répondez à Shao : le lieu n'est pas prêt ; ralentir le recrutement ; les armes, les garder à Andong jusqu'au moment de s'en servir. Les 6 000 de fonds passent par la Yokohama Specie Bank (正金). […]",
  's0508': "Les étudiants déjà arrivés à Tianjin : allouez[-leur] des fonds pour les entretenir, en attendant l'ordre de Jinan […]. Que Yang Bing cesse de recruter. L'affaire de Shao ne peut être traitée pour l'instant ; quand le document du quartier général sera parvenu, […] n'envoyez pas d'argent. — Le 8.",
  's0515': "Vite, des billets de 10 et de 100 yuans, 20 000 de chaque, avec le sceau spécial du Fujian, à remettre à Chen Qun (陳羣) pour Huang Zhanyun (黃展雲). Les fonds d'ici sont épuisés ; il est difficile d'en lever d'autres. Veuillez […] répondre partout.",
  'h0430': 'Huang (黃, Huang Xing) passe au Japon et y changera de navire pour Shanghai. — Tiecheng (鐵城, Wu Tiecheng).',
  'm0503': "Fonds virés à Hong Kong ; il ne reste plus d'obligations ; prière […] 5 000 yuans de billets ; les certificats et les médailles de promotion et de mérite, à envoyer vite par […]. Je compte rentrer au pays ces jours-ci. — Cheng (誠), salutations.",
 },
 'en': {
  'n0503a': 'Arrived safely in Shanghai? […] the Jiangmen letter was received, but the reply was lost (?). From San Francisco (金山), […] Luo Fang […] and the representatives Ma Xing […], three people, arrived in Japan yesterday: can they be urged to go to Shanghai? [Wang] Zhaoming means to find Du Shi to help draft the bonds; ask brother [Liao] Zhongkai whether he can see to it. — The 3rd.',
  'n0503b': "[…]qiu is taking the Hakuai-maru to Shanghai. — Chi. […]",
  'n0504a': "Shao Zifeng telegraphs: at Huairen, Wang Huanxia on 28 April led [the troops of] two districts, [Huairen] and […], five hundred [men], who declared themselves independent (獨立); but their forces having been defeated (?), he plans to move men and arms along the Yalu to the Andong concession, recruit several thousand more and await orders. […] Reply quickly. […] Instructions requested: reply. Because of the Sakamoto affair, [I] am taking the Kasuga-maru instead; a friendly gathering has been set for the […]. — Chi.",
  'n0504b': "There are 6,000 in cash: should they be remitted to Shanghai? […] The Japanese Fukaya (深谷) came to ask whether the unification [proposed by] brother […] and Nakasuga (中須賀) […] can be carried out. Reply. — Chi. The 4th.",
  'n0506': "Yang Bing forwards a telegram from Tianjin: the students who have arrived number about a hundred (?); funds are needed most urgently. […] Reply. — The 6th.",
  'n0508': "Last night, a telegram from Juesheng (Ju Zheng): on the 4th [we] took Zhoucun (周村); our army attacked the city of Weixian the same day (?); on the 5th [we] took its East Gate; at noon a slight pull-back; in the evening [we] decided to surround [the city] and occupied the nearby villages; morale is excellent. Forwarding this. […] Shao Zifeng's [army] […] is now on its way to Shandong. [Yang] Bing has also had an urgent request for funds from Tianjin: please act quickly. — Chi. The 8th.",
  'n0510': 'Keqiang (Huang Xing) arrived yesterday; he is avoiding visitors, I have not seen him yet. […] Mengshuo (孟碩) took the same ship to Shanghai. Please […] launch the action. It is essential to telegraph the Shandong news to San Francisco (金山). — Chi. The 10th.',
  'n0512': 'The box has been handed to Inuzuka (犬塚); it will leave on the 15th by a French ship. For any urgent matter, telegraph to the following address: [address in clear, unread].',
  'n0511': 'I hear that Zhang Ji (張繼) has returned to Japan; that is very surprising — is it true?',
  'n0515': "Saw Keqiang (Huang Xing) today: he strongly advises that Sir [Sun]'s journey to Shanghai be put off. He also says that a bureau chief (局長) of the General Staff stated: in Shandong the revolutionary army has too few troops; if they are not increased and it comes to peace talks, his country's diplomacy will find it very hard to act, and he means to slow down his help. [Keqiang] replied that the troops are loyal and will never make a compromise peace, and asked for active help. The other then […], and [Keqiang] telegraphs specially to ask that the troops be expanded urgently. Further, Xi Zhengming asks for funds by urgent telegram; extract of the original: the cadets of the [Baoding] military school who have come to Tianjin and signed a pledge (誓約) already exceed a hundred; their representatives pledge obedience; I have told them to refuse […]. Outsiders are spending large sums to buy them over. [I have] fixed […] five, issued certificates and assigned [the men]; send ten thousand yuan quickly. […] Bao's and the other troops really can do something. Tianjin should now be the target. — Chi. The 15th.",
  's0505': "On the 3rd […] arrived in Shanghai; the representatives Ma and others may come to Shanghai. Also prepare banknotes quickly: 20,000 of 100 yuan, 80,000 of 10 yuan, and […] each of 1 and 5 yuan, to be handed to the Harunoyō-maru (春洋丸) and carried to Hong Kong; […] to be handed to Mei Qiaolin (梅喬林). As for [those in charge of] accounts and notes, I leave it to you, brother. — Wen (Sun Yat-sen).",
  's0506': "Reply to Shao: the place is not ready; slow down recruitment; keep the arms at Andong until the time comes to use them. The 6,000 in funds go through the Yokohama Specie Bank (正金). […]",
  's0508': "The students already arrived in Tianjin: please allot funds to keep them, pending the Jinan order […]. Yang Bing should stop recruiting. Shao's affair cannot be handled for now; once the headquarters' document has arrived, […] do not remit money. — The 8th.",
  's0515': "Quickly, notes of 10 and 100 yuan, 20,000 of each, with the special seal for Fujian, to be handed to Chen Qun (陳羣) for Huang Zhanyun (黃展雲). Funds here are exhausted; it is hard to raise more. Please […] reply everywhere.",
  'h0430': 'Huang (黃, Huang Xing) is going on to Japan and will change ship there for Shanghai. — Tiecheng (鐵城, Wu Tiecheng).',
  'm0503': "Funds remitted to Hong Kong; no bonds are left; please […] 5,000 yuan in notes; the certificates and the promotion and merit medals, to be sent quickly by […]. I expect to return home in the next few days. — Cheng (誠), with respects.",
 },
 'ja': {
  'n0503a': '無事上海に着いたか。……江門の書簡は受け取ったが、返信は失われた（？）。金山（サンフランシスコ）から……羅芳……、代表の馬醒……の三人が昨日日本に着いた。上海へ行くよう促せるか。〔汪〕兆銘は杜石を探して債券の起草を手伝わせるつもり。〔廖〕仲愷兄に引き受けられるか尋ねられたい。江（3日）。',
  'n0503b': "……秋が博愛丸で上海へ向かう。持。……",
  'n0504a': "邵子峯から電報：懐仁で王煥夏が4月28日（儉）に懐〔仁〕・……両県の軍五百を率いて独立した。しかし勢力が敗れた（？）ため、人と武器を鴨緑江沿いに安東租界まで運び、さらに数千を募って命令を待つつもり。……至急返電を。……指示を請う。返電を。坂本の件で春日丸に乗り換える。……日に懇親会を開くことに決めた。持。",
  'n0504b': "現金六千がある。上海へ送金すべきか。……日本人深谷が来て、……兄と中須賀の統一……が実行できるかと尋ねた。返電を。持。支（4日）。",
  'n0506': "楊丙が天津の電報を伝える：到着した学生は百人ほど（？）、至急資金が必要。……返電を。魚（6日）。",
  'n0508': "昨夜、覚生（居正）から電報：4日に周村を占領、わが軍は同日（？）に濰県城を攻撃、5日にその東関を占領、正午やや後退、夜にまた包囲を決め、付近の村落を占領した。士気は非常に高い。転電する。……邵子峯の軍……は今や山東へ向かっている。〔楊〕丙はまた天津から資金の催促を受けた。速やかに処理されたい。持。齊（8日）。",
  'n0510': '克強（黄興）は昨日着いたが、人を避けており、まだ会っていない。……孟碩は同じ船で上海へ向かった。……挙事されたい。山東の情報を金山（サンフランシスコ）へ電報で知らせることが肝要。持。灰（10日）。',
  'n0512': '箱はすでに犬塚に渡した。15日にフランス船で送る。急用があれば次の宛先へ打電されたい：〔平文の宛先、未読〕。',
  'n0511': '張継が日本に戻ったと聞いた。たいへん意外だ。本当か。',
  'n0515': "今日、克強（黄興）に会った。先生の上海行きは延期すべきだと強く言う。また参謀本部の某局長は、山東の革命軍は兵が少なすぎ、増えないうえ講和にでもなれば、自国の外交は手をつけにくく、援助を緩めるつもりだと言ったという。〔克強は〕軍隊は忠実で決して妥協の講和はしないと答え、積極的な援助を求めた。某はそこで……、〔克強は〕軍の拡充を急ぐよう特に打電する。また席正銘が至急電で資金を求めている。原電の抜粋：〔保定〕軍官学校の学生で天津に来て応募した者はすでに百人を超え、代表は服従を誓っている。……を拒むよう言っておいた。外部は巨額で買収しようとしている。……五を定め、証明書を与えて分遣した。至急一万円送られたい。……保などの軍には確かに見込みがある。今は天津を図るべきである。持。刪（15日）。",
  's0505': "3日（江）に……が上海に着いた。馬代表らは上海に来てよい。また至急紙幣を用意されたい：百円券二万、十円券八万、一円・五円各……万。春洋丸に託して香港へ運び、……梅喬林に渡して受け取らせる。帳簿・券の担当は兄の判断に任せる。文（孫文）。",
  's0506': "邵に返電：場所の準備ができていない。募集は控え、武器は安東に保管して時機を待って使う。資金六千は正金（横浜正金銀行）経由。……",
  's0508': "すでに天津に着いた学生には資金を配分して維持し、済南の命令を待つ……。楊丙は募集を停止。邵の件は目下処理できない。本部の文書が届いたら……送金するな。齊（8日）。",
  's0515': "至急、十円券・百円券を各二万、福建専用印を付けて陳羣に渡し、黄展雲へ転送されたい。こちらの資金は尽き、これ以上調達しがたい。……各所に返答されたい。",
  'h0430': '黄（黄興）は日本へ回り、船を乗り換えて上海へ向かう。鉄城（呉鉄城）。',
  'm0503': "資金は香港へ送金した。債券は残っていない。……券五千円、証書および昇進・功労章を至急……で送られたい。近日中に帰国するつもり。誠拝。",
 },
}
def _zh(text):
    """version chinoise de travail : texte restitué, propositions intégrées, caractères douteux remplacés par « …… »"""
    import re
    t = re.sub(r'\{(.)\}', r'\1', text); t = re.sub(r'(‹.›)+', '……', t)
    return t.rstrip('。') + '。'
_DAY = {'江': '三日', '支': '四日', '魚': '六日', '齊': '八日', '灰': '十日', '删': '十五日'}
for _sid in _MAI['fr']:
    _t = _zh(R[_sid][0])
    for _r, _d in _DAY.items():
        if _t.endswith(_r + '。'): _t = _t[:-1] + '（' + _d + '）。'
    _MAI.setdefault('zh-Hant', {})[_sid] = _t
for _lang in ('fr', 'en', 'zh-Hant', 'ja'): TR[_lang].update(_MAI[_lang])

# lot du début mai : paragraphe ajouté à l'introduction, clés supplémentaires, lettres pas toutes vérifiées
_INTRO_MAI = {
 'fr': ('<p><strong>Ajout du 13 octobre 2026 : le début de mai 1916 (JACAR B03050089000).</strong> Seize télégrammes de plus, du 30 avril au 15 mai. '
        'Outre les messages de Tokyo à « Junzaburo », ce lot contient des <em>réponses</em> parties de Shanghai vers Tokyo (adresse « Linwailuk »), '
        'chiffrées avec le même condensateur ; l\'une est signée <span lang="zh-Hant">文</span> (Sun Wen, c\'est-à-dire Sun Yat-sen). Les télégrammes des 11 et 12 mai portent un autre préfixe, « Thirtyeight », et se lisent avec une <strong>table nouvelle</strong>, retrouvée ici (voir l\'article <a href="method.html#thirtyeight">Méthode</a>). '
        'Un télégramme de Manille à Tōyama Mitsuru (頭山滿), relayé tel quel vers Shanghai, se lit avec la clé de Manille à Tōyama déjà publiée' + SUP +
        ' et porte la signature <span lang="zh-Hant">誠</span>. Un télégramme d\'Honolulu (préfixe « Aloha »), signé <span lang="zh-Hant">鐵城</span> (Wu Tiecheng), se lit avec la clé « Honolulu » déjà publiée' + SUP + ', dans une variante où w s\'emploie comme seconde forme du v ; il annonce le passage de Huang Xing par le Japon. Les lettres ont été lues par Claude ; les 23 mots douteux ont été '
        '<strong>vérifiés à l\'image par Brice Dudout</strong> (les autres n\'ont pas été relus lettre par lettre).</p>'),
 'en': ('<p><strong>Added 13 October 2026: early May 1916 (JACAR B03050089000).</strong> Sixteen more telegrams, from 30 April to 15 May. '
        'Besides the messages from Tokyo to “Junzaburo”, this batch contains <em>replies</em> sent from Shanghai to Tokyo (address “Linwailuk”), '
        'enciphered with the same condenser; one is signed <span lang="zh-Hant">文</span> (Sun Wen, that is, Sun Yat-sen). The telegrams of 11 and 12 May carry a different prefix, “Thirtyeight”, and read with a <strong>new table</strong>, recovered here (see the <a href="method.html#thirtyeight">Method</a> article). '
        'A telegram from Manila to Tōyama Mitsuru (頭山滿), relayed verbatim to Shanghai, reads with the Manila-to-Tōyama key already published' + SUP +
        ' and is signed <span lang="zh-Hant">誠</span>. A telegram from Honolulu (prefix “Aloha”), signed <span lang="zh-Hant">鐵城</span> (Wu Tiecheng), reads with the “Honolulu” key already published' + SUP + ', in a variant where w is used as a second form of v; it announces Huang Xing\'s passage through Japan. The letters were read by Claude; the 23 doubtful words were '
        '<strong>checked against the image by Brice Dudout</strong> (the others were not re-read letter by letter).</p>'),
 'zh-Hant': ('<p><strong>2026年10月13日補充：1916年5月上旬（JACAR B03050089000）。</strong>新增十六封電報（4月30日至5月15日）。除東京致「Junzaburo」的電報外，'
        '本批還有由上海發往東京（地址「Linwailuk」）的<em>覆電</em>，使用同一壓縮碼；其中一封署名<span lang="zh-Hant">文</span>（孫文）。5月11日、12日兩電冠以另一前綴「Thirtyeight」，以此處找出的<strong>新碼表</strong>讀出（見<a href="method.html#thirtyeight">方法</a>一文）。'
        '一封馬尼拉致頭山滿的電報，原樣轉發上海，以已發表的馬尼拉→頭山密鑰' + SUP + '讀出，署名<span lang="zh-Hant">誠</span>。一封檀香山電報（前綴「Aloha」），署名<span lang="zh-Hant">鐵城</span>（吳鐵城），以已發表的「檀香山」密鑰' + SUP + '讀出，其中 w 作為 v 的另一寫法；內容是黃興取道日本。'
        '字母由 Claude 讀出，其中23個存疑詞已由 Brice Dudout <strong>對照影像核對</strong>（其餘未逐字母重讀）。</p>'),
 'ja': ('<p><strong>2026年10月13日追加：1916年5月上旬（JACAR B03050089000）。</strong>4月30日から5月15日までの電報16通を追加。東京から「Junzaburo」宛の電報に加え、'
        'この束には上海から東京（宛名「Linwailuk」）への<em>返電</em>があり、同じ圧縮符号で暗号化されている。うち1通は<span lang="zh-Hant">文</span>（孫文）の署名。5月11日と12日の電報は別の前置語「Thirtyeight」を持ち、ここで復元した<strong>新しい表</strong>で読める（<a href="method.html#thirtyeight">方法</a>の記事を参照）。'
        'マニラから頭山満宛の電報は、そのまま上海へ転送されており、既発表のマニラ→頭山鍵' + SUP + 'で読め、<span lang="zh-Hant">誠</span>の署名がある。ホノルル発の電報（前置語「Aloha」）は<span lang="zh-Hant">鐵城</span>（呉鉄城）の署名で、既発表の「ホノルル」鍵' + SUP + 'を w を v のもう一つの書き方とする変種で読み、黄興の日本経由を伝える。'
        '文字は Claude が読み、疑わしい23語は Brice Dudout が<strong>画像と照合した</strong>（その他は一文字ずつは再読していない）。</p>'),
}
_CH_MAI = {'fr': {'k38': 'Préfixe « Thirtyeight » (nouvelle table, Tokyo → Shanghai)', 'man2': 'Clé Manille → Tōyama (Manille → Tokyo)'},
           'en': {'k38': 'Prefix “Thirtyeight” (new table, Tokyo → Shanghai)', 'man2': 'Manila → Tōyama key (Manila → Tokyo)'},
           'zh-Hant': {'k38': '前綴「Thirtyeight」（新碼表，東京 → 上海）', 'man2': '馬尼拉→頭山密鑰（馬尼拉 → 東京）'},
           'ja': {'k38': '前置語「Thirtyeight」（新しい表、東京 → 上海）', 'man2': 'マニラ→頭山鍵（マニラ → 東京）'}}
_READ = {'fr': 'Lettres du formulaire (lues sur le scan, vérifiées)',
         'en': 'Letters on the form (read on the scan, checked)',
         'zh-Hant': '電報紙上的字母（依掃描影像讀出並核對）', 'ja': '用紙の文字（画像から読み、照合済み）'}
_TOC_SH = {'fr': 'Condensateur « Yamada » (Shanghai → Tokyo, réponses)', 'en': 'Condenser “Yamada” (Shanghai → Tokyo, replies)',
           'zh-Hant': '壓縮碼「山田」（上海 → 東京，覆電）', 'ja': '圧縮符号「山田」（上海 → 東京、返電）'}
for _lang in LAB:
    _c = LAB[_lang]['channel']; LAB[_lang]['toc'] = {'yamada1916': _c['yamada1916'], 'k38': _CH_MAI[_lang]['k38'], 'yamada1916-sh': _TOC_SH[_lang], 'man2': _CH_MAI[_lang]['man2'], 'honolulu1916w': {'fr': 'Clé « Honolulu », variante « Aloha » (Honolulu → Tokyo)', 'en': '“Honolulu” key, “Aloha” variant (Honolulu → Tokyo)', 'zh-Hant': '「檀香山」密鑰「Aloha」變體（檀香山 → 東京）', 'ja': '「ホノルル」鍵の「Aloha」変種（ホノルル → 東京）'}[_lang]}
    _c['yamada1916'] = {'fr': 'Condensateur « Yamada »', 'en': 'Condenser “Yamada”', 'zh-Hant': '壓縮碼「山田」', 'ja': '圧縮符号「山田」'}[_lang]
    LAB[_lang]['intro'] += _INTRO_MAI[_lang]; LAB[_lang]['channel'].update({'honolulu1916w': {'fr': 'Clé « Honolulu », variante « Aloha » (w = v)', 'en': '“Honolulu” key, “Aloha” variant (w = v)', 'zh-Hant': '「檀香山」密鑰「Aloha」變體（w = v）', 'ja': '「ホノルル」鍵の「Aloha」変種（w = v）'}[_lang], 'yamada1916w': {'fr': 'Condensateur « Yamada » (w = p)', 'en': 'Condenser “Yamada” (w = p)', 'zh-Hant': '壓縮碼「山田」（w = p）', 'ja': '圧縮符号「山田」（w = p）'}[_lang], 'k38': {'fr': 'Table « Thirtyeight »', 'en': '“Thirtyeight” table', 'zh-Hant': '「Thirtyeight」碼表', 'ja': '「Thirtyeight」表'}[_lang], 'man2': {'fr': 'Clé Manille → Tōyama', 'en': 'Manila → Tōyama key', 'zh-Hant': '馬尼拉→頭山密鑰', 'ja': 'マニラ→頭山鍵'}[_lang]}); LAB[_lang]['read'] = _READ[_lang]

def build():
    msgs = []
    for sid, rec, page, (mo, da), tm, s, prefix in SEL:
        if sid in LOCAL: continue                      # en cours en local : pas sur le site
        key = KEY.get(sid, 'yamada1916'); T = bkeys.KEYS[key]
        d = [(s[i:i + 4], '%02d%02d' % (T[s[i:i + 2]], T[s[i + 2:i + 4]])) for i in range(0, len(s) - 3, 4)]; codes = [c for _, c in d];   # accepte w (yamada1916w) ; comme bkeys.decode, ignore une syllabe finale seule
        chars = [CH(c) for c in codes]; nums = [int(c) for c in codes]
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
            ep = edit_path_alias(letters[4 * i:4 * i + 4], T, ch)
            assert ep and len(ep['edits']) <= 2, (sid, i, ch, ep)
            out.append(dict(i=i, ch=ch, orig=chars[i], level=lvl, reasons=reasons, letters=letters[4 * i:4 * i + 4], image='divergente' if (sid, ch) in DIVERGE else None, **ep))
        after = list(nums)
        for p in out: after[p['i']] = int(p['code'])
        toc = {'yamada1916w': 'yamada1916'}.get(key, key) + ('-sh' if sid.startswith('s') else '')
        n = '%04d' % (page + IMG_OFFSET[rec])            # n° d'image JACAR, comme les autres télégrammes du site
        msgs.append({'id': sid, 'label': n + POS.get(sid, ''), 'toc': toc, 'grid': key, 'fiche': {'img': 'n' + n, 'n': n, 'keys': KEYS[sid]}, 'route': ROUTES.get(sid, ROUTE), 'record': rec, 'md': [mo, da], 'page': page,
                     'time': tm, 'prefix': prefix, 'letters': letters, 'codes': codes, 'chars': chars, 'status': status, 'fixed': {}, 'alts': alts,
                     'expected': {}, 'readable': {'toks': [[c, i, p] for c, i, p in toks], 'props': out, 'score': [BC.mean_score(nums), BC.mean_score(after)]}})
    msgs.sort(key=lambda m: (m['record'], m['label']))   # ordre des images JACAR, comme les autres télégrammes
    stats = {'tels': len(msgs), 'codes': sum(len(m['codes']) for m in msgs), 'douteux': sum(s == 'douteux' for m in msgs for s in m['status']),
             'confirmé': sum(s.startswith('confirmé') for m in msgs for s in m['status'])}
    T2 = c1916_i18n.t2s_table(WENMI); i18n = {}
    for lang in ('fr', 'en', 'zh-Hant', 'ja'):
        dd = dict(LAB[lang]); dd['tr'] = {k: v for k, v in TR[lang].items() if k not in LOCAL}; dd['date'] = {m['id']: c1916_i18n.date_of(lang, *m['md']) + (', ' + m['time'] if m['time'] else '') for m in msgs}
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
