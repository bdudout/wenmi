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
import dx_overrides                                   # noqa: E402
DX = dx_overrides.load(WENMI)
import form_times  # noqa: E402
from n1916_streams import SEL, EXTRA_KEYS, KEY, ROUTE as ROUTES, LOCAL, IMG_OFFSET, POS   # noqa: E402
bkeys = BC.bkeys; C2CH, uni, REF = BC.C2CH, BC.uni, BC.REF
for _k, _t in EXTRA_KEYS.items(): bkeys.KEYS.setdefault(_k, _t)
# clé « Honolulu » (grille de Bourdeau) avec l'alphabet « Aloha » : sans q, avec w (C111, 23/10/2026 ; avant : w = v)
bkeys.KEYS['honolulu1916w'] = json.load(open(os.path.join(WENMI, 'cryptanalysis', 'c111', 'honolulu-s5.json'), encoding='utf-8'))['table']
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
 'n0531a': ('軍用票辦法，速覆。持。卅一', []),
 'n0531b': ('美僑駐濱者小達六十，欲往濰縣効力，如何？盼覆。聞美支部存款甚多。請電催', []),
 'n0601': ('寄魯芳債券照辦。軍用票事，覺生來電：東京如不能應急，則渠將自印云云。持', []),
 'n0603': ('先生曁仲愷兄鑒：軍票事何不復？覺生連電急索。中央銀行票不作用，可‹叢›參印發行。持。江', []),
 'n0604': ('華僑己到六十餘，請示安置方法。持。江', []),
 'n0605a': ('廖先生鑒：弟促如何{不}覆。‹紀›‹文›', [('Q', ['sens'])]),
 'n0605b': ('濰縣函索飛機，尾崎已赴滬，請先生就近商議。澳款用孫逸仙名', []),
 'n0607': ('袁賊旣死，速定大計。持決乘春日丸歸。', []),
 'n0615': ('電悉。不兌換可否加暫順券面？應否署名？如署，以何人爲宜？但先生署名恐有抵觸。弟可否隨券到魯？兆銘又萱野偕坂本攜{兩}{飛}機往‹餽›。機校由立花代理，學生中半無成功之望，坂本商請改換，速覆。‹重›‹民›‹删›', [('Q', ['sens']), ('Q', ['sens'])]),
}
# codes rares pour le modèle de langue mais sûrs : (caractère → type)
CONF = {'n0517': {'仟': 'mot', '瑾': 'nom', '篠': 'date'}, 'n0531a': {'卅': 'date'}, 'n0531b': {'濰': 'nom'},
        'n0603': {'曁': 'variante', '愷': 'nom'}, 'n0605b': {'濰': 'nom'}, 'n0607': {'旣': 'variante'},
        'n0615': {'萱': 'nom', '偕': 'mot', '坂': 'nom'}}
KEYS = {'n0517': ['席正銘', '趙瑾卿', '持'], 'n0531a': ['軍用票'], 'n0531b': ['美僑', '濰縣', '美支部'], 'n0601': ['債券', '軍用票', '覺生'],
        'n0603': ['仲愷', '軍票', '中央銀行'], 'n0604': ['華僑', '安置'], 'n0605a': ['廖先生'], 'n0605b': ['濰縣', '飛機', '尾崎', '孫逸仙'],
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
  'n0531a': "Au sujet des bons militaires (軍用票) : comment procéder ? Réponds vite. — Chi. Le 31.",
  'n0531b': "Les Chinois d'Amérique séjournant à Yokohama sont une soixantaine ; ils veulent aller servir à Weixian (濰縣) : que faire ? Réponds. On apprend que la section d'Amérique [du parti] a beaucoup de fonds en dépôt. Prière de la relancer par télégramme.",
  'n0601': "Pour les obligations envoyées à Lufang (魯芳), faites comme prévu. Au sujet des bons militaires, Juesheng (Ju Zheng) télégraphie : si Tokyo ne peut faire face à l'urgence, il les fera imprimer lui-même, etc. — Chi.",
  'n0603': "À Monsieur [Sun] et à frère Zhongkai (Liao Zhongkai) : pourquoi ne répondez-vous pas sur les bons militaires ? Juesheng (Ju Zheng) télégraphie sans cesse pour les réclamer d'urgence. Les billets de la Banque centrale ne servent à rien ; on peut [envisager] de les faire imprimer et émettre. — Chi. Le 3.",
  'n0604': "Plus de soixante Chinois d'outre-mer sont déjà arrivés ; indiquez comment les installer. — Chi. Le 3.",
  'n0605a': "À Monsieur Liao : je vous ai pressé — pourquoi ne répondez-vous pas ? […]",
  'n0605b': "Weixian demande des avions par lettre ; Ozaki est déjà parti pour Shanghai ; prière à Monsieur de se concerter sur place. Pour les fonds de Macao (?), utiliser le nom de Sun Yat-sen (孫逸仙).",
  'n0607': "Yuan le traître est mort : arrêtez vite le grand plan. Chi a décidé de rentrer par le Kasuga-maru.",
  'n0615': "Télégramme reçu. Les billets non convertibles : peut-on ajouter au recto la mention « billet provisoire » ? Faut-il les signer ? Si oui, qui vaut-il mieux faire signer ? Mais la signature de Monsieur [Sun] risque de poser problème. Puis-je accompagner les billets jusqu'au Shandong (魯) ? [Wang] Zhaoming (兆銘), ainsi que Kayano (萱野) avec Sakamoto (坂本), emportent deux (?) avions vers […]. L'école d'aviation est confiée à titre provisoire à Tachibana (立花) ; parmi les élèves, la moitié n'a aucun espoir de réussir. Sakamoto, après concertation, demande qu'on les remplace ; répondez vite. […]",
 },
 'en': {
  'n0517': "As for the 3,000 in funds: may 2,000 be given to Xi Zhengming and 500 to Zhao Jinqing? Reply. — Chi (Xie Chi). The 17th.",
  'n0531a': "About the military notes (軍用票): how should we proceed? Reply quickly. — Chi. The 31st.",
  'n0531b': "The American Chinese staying in Yokohama number about sixty; they want to go and serve at Weixian (濰縣): what should be done? Reply. We hear that the American branch [of the party] has a great deal of funds on deposit. Please press it by telegram.",
  'n0601': "For the bonds sent to Lufang (魯芳), proceed as planned. About the military notes, Juesheng (Ju Zheng) telegraphs: if Tokyo cannot meet the emergency, he will have them printed himself, etc. — Chi.",
  'n0603': "To Sir [Sun] and brother Zhongkai (Liao Zhongkai): why no reply about the military notes? Juesheng (Ju Zheng) keeps telegraphing to demand them urgently. The Central Bank notes are of no use; we could [consider] having them printed and issued. — Chi. The 3rd.",
  'n0604': "More than sixty overseas Chinese have already arrived; please say how to accommodate them. — Chi. The 3rd.",
  'n0605a': "To Mr Liao: I have urged you — why no reply? […]",
  'n0605b': "Weixian asks for aircraft by letter; Ozaki has already left for Shanghai; please, Sir, consult on the spot. For the Macao (?) funds, use the name of Sun Yat-sen (孫逸仙).",
  'n0607': "Yuan the traitor is dead: settle the great plan quickly. Chi has decided to return on the Kasuga-maru.",
  'n0615': "Telegram received. The inconvertible notes: may 'provisional note' be added on the face? Should they be signed? If so, who would be best to sign? But Sir [Sun]'s signature might cause problems. May I accompany the notes to Shandong (魯)? [Wang] Zhaoming (兆銘), as well as Kayano (萱野) together with Sakamoto (坂本), take two (?) aircraft to […]. The flying school is entrusted for the time being to Tachibana (立花); among the students, half have no hope of success. Sakamoto, after consultation, asks for them to be replaced; reply quickly. […]",
 },
 'zh-Hant': {
  'n0517': "款三仟，可否給席正銘二仟、趙瑾卿五百？望覆。持。篠（十七日）。",
  'n0531a': "軍用票辦法，速覆。持。卅一（三十一日）。",
  'n0531b': "旅居橫濱的美洲華僑約六十人，欲往濰縣效力，如何？盼覆。聞美洲支部存款甚多。請電催。",
  'n0601': "寄魯芳之債券照辦。軍用票事，覺生（居正）來電：東京如不能應急，則渠將自印云云。持。",
  'n0603': "先生暨仲愷兄鑒：軍票事何以不覆？覺生連電急索。中央銀行票不作用，可……印發行。持。江（三日）。",
  'n0604': "華僑已到六十餘人，請示安置方法。持。江（三日）。",
  'n0605a': "廖先生鑒：弟促如何不覆？……",
  'n0605b': "濰縣來函索飛機，尾崎已赴滬，請先生就近商議。澳款用孫逸仙名。",
  'n0607': "袁賊既死，速定大計。持決乘春日丸歸。",
  'n0615': "電悉。不兌換券可否加「暫順券」於券面？應否署名？如署，以何人為宜？但先生署名恐有抵觸。弟可否隨券到魯？兆銘又萱野偕坂本攜兩（？）飛機往……。飛機學校由立花代理，學生中半無成功之望。坂本商請改換，速覆。……",
 },
 'ja': {
  'n0517': "資金三千のうち、席正銘に二千、趙瑾卿に五百を与えてよいか。返電を。持（謝持）。篠（17日）。",
  'n0531a': "軍用票の件、どうするか。至急返電を。持。卅一（31日）。",
  'n0531b': "横浜に滞在する米国華僑は約60人、濰県へ行き尽力したいという。どうするか。返電を。米国支部には預金が多いと聞く。電報で催促されたい。",
  'n0601': "魯芳へ送った債券は予定どおり処理されたい。軍用票の件、覚生（居正）から電報：東京が急に応じられないなら、彼自身が印刷する、云々。持。",
  'n0603': "先生および仲愷兄へ：軍票の件、なぜ返事がないのか。覚生がしきりに電報で至急求めている。中央銀行券は役に立たない。……印刷・発行してはどうか。持。江（3日）。",
  'n0604': "華僑がすでに60余人到着した。収容の方法を指示されたい。持。江（3日）。",
  'n0605a': "廖先生へ：催促したのに、なぜ返電がないのか。……",
  'n0605b': "濰県から書簡で飛行機を求めてきた。尾崎はすでに上海へ向かった。先生には現地で協議されたい。澳門（？）の資金は孫逸仙の名義を用いること。",
  'n0607': "袁賊はすでに死んだ。速やかに大計を定められたい。持は春日丸で帰ることに決めた。",
  'n0615': "電報拝見。兌換されない券に「暫順券」と券面に加えてよいか。署名すべきか。署名するなら誰がよいか。ただし先生の署名は差し支えがあるかもしれない。私が券とともに魯（山東）へ行ってよいか。兆銘、また萱野は坂本とともに飛行機二機（？）を持って……へ行く。飛行学校は立花が代理する。学生の半数は成功の見込みがない。坂本は協議のうえ入れ替えを求めている。至急返電を。……",
 },
}

# ---- Lot du début mai 1916 (B03050089000) : lecture de Claude seule (13/10/2026), pas encore vérifiée à l'image par Brice ----
R.update({
 'n0503a': ('抵滬平安否？港拯日函、江門得而覆失。金山{及}羅省‹潑›崙代表馬醒‹馨›‹筊›三人昨日到東，可否促其赴{滬}？兆銘{擬}覓杜石助寫債券，請詢仲愷兄可否照辦。江', []),
 'n0503b': ('‹紉›秋乘博愛丸赴滬。持。‹復›', []),
 'n0504a': ('‹卲›子峯來電：懷仁描事王煥夏於四月儉日率懷專兩縣軍譚五百獨立，然勢力‹蘇›敗，擬將人械沿鴨綠江運至安東租界，再募數千待命。運往他省，望速覆云云。請示辦法，便辨覆。應時因坂本事改乘春日丸，決定‹齷›日開懇親會。持', []),
 'n0504b': ('有現款六仟，是否匯滬？‹帷›日人深谷來詢統一兄與中須賀之五浮能否實行。望覆。持。支', []),
 'n0506': ('楊丙交天津電：學生已到百貴人，需款{至}急。盼覆。魚', []),
 'n0508': ('昨夜得覺生電稱：四日占領周村，{本}軍以同日攻濰縣城，五日占其東關，正午稍却，晚復決計圍境，占領附近村落，士氣頗壯。特轉。‹弼›邵子峯遮義之軍‹警›可上，今其運適山東。楊丙又接津電，‹傞›款，請速辦。持。齊', []),
 'n0510': ('克強昨日到，避人，尚未晤。‹逖›‹惟›孟碩乘原船適滬。{請}以居正舉{事}。山東電告金山至要。持。{灰}', []),
 'n0512': ('箱已交犬塚，十五日附法船來。若有要事，請電如下：「Mrs …, steamer Porthos」。請派二人接，因行李甚多。', []),   # 「」 : anglais chiffré (clé Rosamonde), hors flux
 'n0511': ('聞張繼已回日，頗奇，是否？', []),
 'n0515': ('今日晤克強，頗稱先生‹但›赴滬從緩。又言參部局長某謂：山東事革軍軍隊過少，不增，且將議和，則其國外交殊難著手，擬緩其幫助之力。經換答以軍隊忠壘，決不苟和，務請積極幫助。某始諾，特電請亟謀擴充軍隊。再，席正銘急電請款，摘原電如下：保軍校來津填誓約已逾百人，代表終對服從，已囑校中拒絶。外派點段鉅{款}買收也。定‹嬙›五給憑分遣，釐速寄萬圓。模範團南逸‹寁›人保等軍確有可爲。{云}云。現在宜圖天津。持。删', []),
 's0505': ('江日官抵滬，馬代表等可來滬。並請速備百圓券二萬、十圓八萬、一圓五圓各一萬，交春洋丸帶港，‹耻›義會{轉}交梅喬林收。帳券人請兄酌奪。文', []),
 's0506': ('請覆邵：地點未備，人緩招募，械則安置安東，待時而用。款六千由正金購。所持人‹拂›票寄{到}', []),
 's0508': ('已{到}津學生請酌撥款維持，待得濟南令役餘令。楊丙停歷招集。邵事目前不能辦，本部文下足則六十勿匯可也。齊', []),
 's0515': ('速辦十圓、百圓券各二{萬}，加福建專用章，交陳羣轉黃展雲。此間款盡，難再籌。請酌覆各處', []),
 'h0430': ('黃鄧到日，換船赴滬。鐵城', []),
 'h0516': ('不能往金，卽歸國。公到滬如何？‹贛›‹箬›定‹吟›電{復}。鐵城', []),
 'm0503': ('款匯港，債券無存，請{該}趣漢英‹擐›券伍仟圓、証書及{陞}等功章速附來。弟擬日間回國。誠叩', []),
})

P_, Q_ = lambda *r: ('P', list(r)), lambda *r: ('Q', list(r))
_LV = {'n0503a': [Q_('sens'), P_('sens', 'contexte'), Q_('sens')], 'n0510': [P_('sens'), P_('sens'), P_('structure')], 'n0511': [], 'h0430': [], 'h0516': [P_('sens')], 'n0512': [], 'n0504a': [],
       'n0504b': [], 'n0506': [P_('sens')], 'n0508': [Q_('sens')], 'n0515': [P_('sens'), Q_('sens')],
       's0505': [Q_('sens')], 's0506': [Q_('sens')], 's0508': [P_('sens')], 's0515': [P_('sens', 'contexte')],
       'm0503': [Q_('sens'), P_('sens', 'jumeau')]}
# propositions maintenues alors que la relecture de Brice (lot V7) ne les voit pas sur l'image
DIVERGE = set()   # 14/10/2026 : toutes tranchées par la relecture V1 (une lettre comparée à la même main, aveugle au sens)
# relecture V1 : la lettre décodée est confirmée à l'image, la proposition est maintenue (erreur d'origine, 1916, supposée)
MAINT = {('n0503a', '滬'), ('n0503a', '擬'), ('n0515', '款'), ('s0515', '萬'), ('s0508', '到'), ('m0503', '陞')}
# (n0615 如 : lettre proposée lue à l'image au lot V1 → lettres corrigées, dx_corrections.json)
for _sid, _lv in _LV.items(): R[_sid] = (R[_sid][0], _lv)
CONF.update({'n0601': {'云': 'mot'}})   # 云云 (fin de citation) ; 兆銘 (Wang Zhaoming)
CONF.update({'n0503a': {'愷': 'nom', '江': 'date'}, 'n0512': {'塚': 'nom'}, 'n0504a': {'卲': 'variante', '儉': 'date', '坂': 'nom'}, 'n0504b': {'仟': 'mot', '支': 'date'},
             'n0508': {'占': 'mot', '濰': 'nom', '却': 'variante'}, 'n0515': {'絶': 'variante', '删': 'date'}, 'm0503': {'仟': 'mot', '証': 'variante'}})
KEYS.update({'n0503a': ['兆銘', '債券', '仲愷'], 'n0503b': ['博愛丸'], 'n0504a': ['邵子峯', '王煥夏', '鴨綠江', '安東', '坂本', '春日丸'],
             'n0504b': ['現款六仟', '深谷', '中須賀'], 'n0506': ['楊丙', '天津', '學生'], 'n0508': ['覺生', '周村', '濰縣', '邵子峯'],
             'n0510': ['克強', '避人', '舉事', '金山'], 'n0512': ['犬塚', '法船', 'Porthos', '行李'], 'n0511': ['張繼', '回日'], 'h0430': ['黃', '換船', '鐵城'], 'h0516': ['歸國', '到滬', '鐵城'], 'n0515': ['克強', '參謀部', '席正銘', '保定軍校', '天津'],
             's0505': ['百圓券', '春洋丸', '梅喬林', '文'], 's0506': ['邵', '安東', '正金'], 's0508': ['學生', '濟南', '楊丙', '邵'],
             's0515': ['福建', '陳羣', '黃展雲'], 'm0503': ['債券', '陞等功章', '誠']})
_MAI = {
 'fr': {
  'n0503a': "Bien arrivé à Shanghai ? […] la lettre de Jiangmen a été reçue, mais la réponse s'est perdue (?). Les représentants de San Francisco (金山) et de Los Angeles (羅省) […], Ma Xing […], trois personnes, sont arrivés hier au Japon : peut-on les presser de se rendre à Shanghai ? [Wang] Zhaoming compte trouver Du Shi pour aider à rédiger les obligations ; demandez à frère [Liao] Zhongkai s'il peut s'en charger. — Le 3.",
  'n0503b': "[…]qiu prend le Hakuai-maru pour Shanghai. — Chi. […]",
  'n0504a': "Shao Zifeng télégraphie : à Huairen, Wang Huanxia a mené le 28 avril [les troupes de] deux districts, [Huairen] et […], cinq cents [hommes], qui se sont déclarés indépendants (獨立) ; mais leurs forces ayant été défaites (?), il compte acheminer hommes et armes le long du Yalu jusqu'à la concession d'Andong, recruter encore plusieurs milliers d'hommes et attendre les ordres. Les acheminer vers une autre province ; réponds vite », etc. Demande d'instructions : répondez. À cause de l'affaire Sakamoto, [je] prends plutôt le Kasuga-maru ; on a décidé de tenir une réunion amicale le […]. — Chi.",
  'n0504b': "Il y a 6 000 en espèces : faut-il les virer à Shanghai ? […] Le Japonais Fukaya (深谷) est venu demander si l'unification [proposée par] frère […] et Nakasuga (中須賀) […] peut être réalisée. Réponds. — Chi. Le 4.",
  'n0506': "Yang Bing transmet un télégramme de Tianjin : les étudiants arrivés sont une centaine (?) ; il faut des fonds de toute urgence. Dans l'attente de ta réponse. — Le 6.",
  'n0508': "Hier soir, télégramme de Juesheng (Ju Zheng) : le 4, [nous avons] pris Zhoucun (周村) ; notre armée a attaqué la ville de Weixian le même jour (?) ; le 5, [nous avons] pris sa porte Est ; à midi léger recul ; le soir, [nous avons] décidé d'encercler [la ville] et occupé les villages voisins ; le moral est excellent. Je transmets. […] [L'armée] de Shao Zifeng […] est maintenant en route vers le Shandong. Yang Bing a aussi reçu un télégramme de Tianjin : […] des fonds ; agissez vite. — Chi. Le 8.",
  'n0510': "Keqiang (Huang Xing) est arrivé hier ; il évite les visiteurs, je ne l'ai pas encore vu. […] Mengshuo (孟碩) a pris le même navire pour Shanghai. Prière de lancer l'action avec Ju Zheng (居正). Il est essentiel de télégraphier les nouvelles du Shandong à San Francisco (金山). — Chi. Le 10.",
  'n0512': "La malle a été remise à Inuzuka (犬塚). Le 15, [je] viens par un navire français. Pour toute affaire urgente, télégraphier comme suit : « Mrs …, steamer Porthos ». Prière d'envoyer deux personnes [m']attendre : il y a beaucoup de bagages.",
  'n0511': "J'apprends que Zhang Ji (張繼) est rentré au Japon ; c'est très surprenant — est-ce vrai ?",
  'n0515': "Vu aujourd'hui Keqiang (Huang Xing) : il insiste pour que la venue de Monsieur [Sun] à Shanghai soit différée. Il dit aussi qu'un chef de bureau (局長) de l'état-major a déclaré : au Shandong, les troupes de l'armée révolutionnaire sont trop peu nombreuses ; si elles n'augmentent pas et qu'on en vient à négocier la paix, la diplomatie de son pays aura bien du mal à agir, et il compte ralentir son aide. [Keqiang] a répondu que les troupes sont loyales et ne feront jamais une paix de compromis, et demandé une aide active. L'autre a alors acquiescé, et [Keqiang] télégraphie spécialement pour demander qu'on étende d'urgence les troupes. Par ailleurs, Xi Zhengming demande des fonds par télégramme urgent ; extrait de l'original : les élèves de l'école militaire [de Baoding] venus à Tianjin et ayant signé un engagement (誓約) dépassent la centaine ; leurs représentants jurent obéissance ; j'ai fait dire à l'école de refuser. Au-dehors, on dépense de grosses sommes pour les acheter. [J'ai] fixé […] cinq, donné des certificats et réparti [les hommes] ; envoyez vite dix mille yuans. Le Régiment modèle (模範團) […], les troupes de Bao et d'autres ont réellement de quoi faire », etc. Il faut maintenant viser Tianjin. — Chi. Le 15.",
  's0505': "Le 3, […] est arrivé à Shanghai ; les représentants Ma et autres peuvent venir à Shanghai. Préparez aussi vite des billets : 20 000 de 100 yuans, 80 000 de 10 yuans, et 10 000 de 1 et de 5 yuans chacun, à remettre au Shun’yō-maru (春洋丸) pour les porter à Hong Kong ; la société 耻義會 (?) les transmettra à Mei Qiaolin (梅喬林). Pour [les responsables] des comptes et des billets, je te laisse en décider, frère. — Wen (Sun Yat-sen).",
  's0506': "Répondez à Shao : le lieu n'est pas prêt ; ralentir le recrutement ; les armes, les garder à Andong jusqu'au moment de s'en servir. Les 6 000 de fonds passent par la Yokohama Specie Bank (正金). Les chèques au porteur sont envoyés (?).",
  's0508': "Les étudiants déjà arrivés à Tianjin : allouez[-leur] des fonds pour les entretenir, en attendant l'ordre de Jinan […]. Que Yang Bing cesse de recruter. L'affaire de Shao ne peut être traitée pour l'instant ; une fois le document du quartier général arrivé, s'il y a assez, inutile de virer les soixante (?). — Le 8.",
  's0515': "Faites vite [faire] des billets de 10 et de 100 yuans, 20 000 de chaque, avec le sceau spécial du Fujian, à remettre à Chen Qun (陳羣) pour Huang Zhanyun (黃展雲). Les fonds d'ici sont épuisés ; il est difficile d'en lever d'autres. Veuillez en décider et répondre partout.",
  'h0430': 'Huang (黃, Huang Xing) et Deng (鄧) arrivent au Japon et y changent de navire pour Shanghai. — Tiecheng (鐵城, Wu Tiecheng).',
  'h0516': 'Je ne peux pas aller à Jin (金, Jinshan, San Francisco ?) ; je rentre aussitôt au pays. Comment vont les choses depuis votre arrivée à Shanghai ? […] répondez par télégramme. — Tiecheng (鐵城, Wu Tiecheng).',
  'm0503': "Fonds virés à Hong Kong ; il ne reste plus d'obligations ; prière […] 5 000 yuans de billets ; les certificats et les médailles de promotion et de mérite, envoyez-les vite. Je compte rentrer au pays ces jours-ci. — Cheng (誠), salutations.",
 },
 'en': {
  'n0503a': 'Arrived safely in Shanghai? […] the Jiangmen letter was received, but the reply was lost (?). The representatives of San Francisco (金山) and Los Angeles (羅省) […], Ma Xing […], three people, arrived in Japan yesterday: can they be urged to go to Shanghai? [Wang] Zhaoming means to find Du Shi to help draft the bonds; ask brother [Liao] Zhongkai whether he can see to it. — The 3rd.',
  'n0503b': "[…]qiu is taking the Hakuai-maru to Shanghai. — Chi. […]",
  'n0504a': "Shao Zifeng telegraphs: at Huairen, Wang Huanxia on 28 April led [the troops of] two districts, [Huairen] and […], five hundred [men], who declared themselves independent (獨立); but their forces having been defeated (?), he plans to move men and arms along the Yalu to the Andong concession, recruit several thousand more and await orders. Move them on to another province; reply quickly,” etc. Instructions requested: reply. Because of the Sakamoto affair, [I] am taking the Kasuga-maru instead; a friendly gathering has been set for the […]. — Chi.",
  'n0504b': "There are 6,000 in cash: should they be remitted to Shanghai? […] The Japanese Fukaya (深谷) came to ask whether the unification [proposed by] brother […] and Nakasuga (中須賀) […] can be carried out. Reply. — Chi. The 4th.",
  'n0506': "Yang Bing forwards a telegram from Tianjin: the students who have arrived number about a hundred (?); funds are needed most urgently. Awaiting your reply. — The 6th.",
  'n0508': "Last night, a telegram from Juesheng (Ju Zheng): on the 4th [we] took Zhoucun (周村); our army attacked the city of Weixian the same day (?); on the 5th [we] took its East Gate; at noon a slight pull-back; in the evening [we] decided to surround [the city] and occupied the nearby villages; morale is excellent. Forwarding this. […] Shao Zifeng's [army] […] is now on its way to Shandong. Yang Bing has also had a telegram from Tianjin: […] funds; please act quickly. — Chi. The 8th.",
  'n0510': 'Keqiang (Huang Xing) arrived yesterday; he is avoiding visitors, I have not seen him yet. […] Mengshuo (孟碩) took the same ship to Shanghai. Please launch the action with Ju Zheng (居正). It is essential to telegraph the Shandong news to San Francisco (金山). — Chi. The 10th.',
  'n0512': 'The trunk has been handed to Inuzuka (犬塚). On the 15th [I] come by a French ship. For any urgent matter, telegraph as follows: “Mrs …, steamer Porthos”. Please send two people to meet [me]: there is a lot of luggage.',
  'n0511': 'I hear that Zhang Ji (張繼) has returned to Japan; that is very surprising — is it true?',
  'n0515': "Saw Keqiang (Huang Xing) today: he strongly advises that Sir [Sun]'s journey to Shanghai be put off. He also says that a bureau chief (局長) of the General Staff stated: in Shandong the revolutionary army has too few troops; if they are not increased and it comes to peace talks, his country's diplomacy will find it very hard to act, and he means to slow down his help. [Keqiang] replied that the troops are loyal and will never make a compromise peace, and asked for active help. The other then agreed, and [Keqiang] telegraphs specially to ask that the troops be expanded urgently. Further, Xi Zhengming asks for funds by urgent telegram; extract of the original: the cadets of the [Baoding] military school who have come to Tianjin and signed a pledge (誓約) already exceed a hundred; their representatives pledge obedience; I have told [those in] the school to refuse. Outsiders are spending large sums to buy them over. [I have] fixed […] five, issued certificates and assigned [the men]; send ten thousand yuan quickly. The Model Regiment (模範團) […], Bao's and the other troops really can do something,” etc. Tianjin should now be the target. — Chi. The 15th.",
  's0505': "On the 3rd […] arrived in Shanghai; the representatives Ma and others may come to Shanghai. Also prepare banknotes quickly: 20,000 of 100 yuan, 80,000 of 10 yuan, and 10,000 each of 1 and 5 yuan, to be handed to the Shun’yō-maru (春洋丸) and carried to Hong Kong; the 耻義會 society (?) is to pass them on to Mei Qiaolin (梅喬林). As for [those in charge of] accounts and notes, I leave it to you, brother. — Wen (Sun Yat-sen).",
  's0506': "Reply to Shao: the place is not ready; slow down recruitment; keep the arms at Andong until the time comes to use them. The 6,000 in funds go through the Yokohama Specie Bank (正金). The bearer cheques are being sent (?).",
  's0508': "The students already arrived in Tianjin: please allot funds to keep them, pending the Jinan order […]. Yang Bing should stop recruiting. Shao's affair cannot be handled for now; once the headquarters' document has come, if it is enough, there is no need to remit the sixty (?). — The 8th.",
  's0515': "Get notes of 10 and 100 yuan made quickly, 20,000 of each, with the special seal for Fujian, to be handed to Chen Qun (陳羣) for Huang Zhanyun (黃展雲). Funds here are exhausted; it is hard to raise more. Please decide and reply everywhere.",
  'h0430': 'Huang (黃, Huang Xing) and Deng (鄧) arrive in Japan and change ship there for Shanghai. — Tiecheng (鐵城, Wu Tiecheng).',
  'h0516': 'I cannot go to Jin (金, Jinshan, San Francisco?); I am returning home at once. How are things since your arrival in Shanghai? […] reply by telegram. — Tiecheng (鐵城, Wu Tiecheng).',
  'm0503': "Funds remitted to Hong Kong; no bonds are left; please […] 5,000 yuan in notes; the certificates and the promotion and merit medals, send them quickly. I expect to return home in the next few days. — Cheng (誠), with respects.",
 },
 'ja': {
  'n0503a': '無事上海に着いたか。……江門の書簡は受け取ったが、返信は失われた（？）。金山（サンフランシスコ）および羅省（ロサンゼルス）……の代表、馬醒……ら三人が昨日日本に着いた。上海へ行くよう促せるか。〔汪〕兆銘は杜石を探して債券の起草を手伝わせるつもり。〔廖〕仲愷兄に引き受けられるか尋ねられたい。江（3日）。',
  'n0503b': "……秋が博愛丸で上海へ向かう。持。……",
  'n0504a': "邵子峯から電報：懐仁で王煥夏が4月28日（儉）に懐〔仁〕・……両県の軍五百を率いて独立した。しかし勢力が敗れた（？）ため、人と武器を鴨緑江沿いに安東租界まで運び、さらに数千を募って命令を待つつもり。他省へ運ぶ。至急返電を」云々。指示を請う。返電を。坂本の件で春日丸に乗り換える。……日に懇親会を開くことに決めた。持。",
  'n0504b': "現金六千がある。上海へ送金すべきか。……日本人深谷が来て、……兄と中須賀の統一……が実行できるかと尋ねた。返電を。持。支（4日）。",
  'n0506': "楊丙が天津の電報を伝える：到着した学生は百人ほど（？）、至急資金が必要。返電を待つ。魚（6日）。",
  'n0508': "昨夜、覚生（居正）から電報：4日に周村を占領、わが軍は同日（？）に濰県城を攻撃、5日にその東関を占領、正午やや後退、夜にまた包囲を決め、付近の村落を占領した。士気は非常に高い。転電する。……邵子峯の軍……は今や山東へ向かっている。楊丙はまた天津から電報を受けた：……資金。速やかに処理されたい。持。齊（8日）。",
  'n0510': '克強（黄興）は昨日着いたが、人を避けており、まだ会っていない。……孟碩は同じ船で上海へ向かった。居正をもって挙事されたい。山東の情報を金山（サンフランシスコ）へ電報で知らせることが肝要。持。灰（10日）。',
  'n0512': '箱はすでに犬塚に渡した。15日にフランス船で行く。急用があれば次のとおり打電されたい：「Mrs ……, steamer Porthos」。荷物が多いので、二人迎えによこされたい。',
  'n0511': '張継が日本に戻ったと聞いた。たいへん意外だ。本当か。',
  'n0515': "今日、克強（黄興）に会った。先生の上海行きは延期すべきだと強く言う。また参謀本部の某局長は、山東の革命軍は兵が少なすぎ、増えないうえ講和にでもなれば、自国の外交は手をつけにくく、援助を緩めるつもりだと言ったという。〔克強は〕軍隊は忠実で決して妥協の講和はしないと答え、積極的な援助を求めた。某はそこで承諾し、〔克強は〕軍の拡充を急ぐよう特に打電する。また席正銘が至急電で資金を求めている。原電の抜粋：〔保定〕軍官学校の学生で天津に来て応募した者はすでに百人を超え、代表は服従を誓っている。学校の中で拒むよう言っておいた。外部は巨額で買収しようとしている。……五を定め、証明書を与えて分遣した。至急一万円送られたい。模範団……保などの軍には確かに見込みがある。今は天津を図るべきである。持。刪（15日）。",
  's0505': "3日（江）に……が上海に着いた。馬代表らは上海に来てよい。また至急紙幣を用意されたい：百円券二万、十円券八万、一円・五円各一万。春洋丸に託して香港へ運び、耻義会（？）から梅喬林に転送して受け取らせる。帳簿・券の担当は兄の判断に任せる。文（孫文）。",
  's0506': "邵に返電：場所の準備ができていない。募集は控え、武器は安東に保管して時機を待って使う。資金六千は正金（横浜正金銀行）経由。持参人払手形を送る（？）。",
  's0508': "すでに天津に着いた学生には資金を配分して維持し、済南の命令を待つ……。楊丙は募集を停止。邵の件は目下処理できない。本部の文書が届き、足りるなら六十（？）は送金しなくてよい。齊（8日）。",
  's0515': "至急、十円券・百円券を各二万作り、福建専用印を付けて陳羣に渡し、黄展雲へ転送されたい。こちらの資金は尽き、これ以上調達しがたい。斟酌して各所に返答されたい。",
  'h0430': '黄（黄興）と鄧が日本に着き、船を乗り換えて上海へ向かう。鉄城（呉鉄城）。',
  'h0516': '金（金山＝サンフランシスコ？）へは行けない。すぐに帰国する。上海に着かれてからいかがか。〔…〕電報で返事を。鉄城（呉鉄城）。',
  'm0503': "資金は香港へ送金した。債券は残っていない。……券五千円、証書および昇進・功労章を至急送られたい。近日中に帰国するつもり。誠拝。",
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
        ' et porte la signature <span lang="zh-Hant">誠</span>. Un télégramme d\'Honolulu (préfixe « Aloha »), signé <span lang="zh-Hant">鐵城</span> (Wu Tiecheng), se lit avec la clé « Honolulu » déjà publiée' + SUP + ', avec un alphabet sans q et avec w (le même que la table de New York 1915 ; retrouvé le 23 octobre 2026, la première lecture prenait w pour v) ; il annonce que Huang [Xing] et Deng arrivent au Japon. Un second, du 16 mai, est ajouté le 23 octobre 2026. Les lettres ont été lues par Claude ; les mots douteux ont été '
        '<strong>vérifiés à l\'image par Brice Dudout</strong>, puis des relectures ciblées des 13 et 14 octobre 2026, menées sans connaître le sens, ont vérifié tous les codes douteux restants et les confusions g/q/y et d/x/n (les autres lettres n\'ont pas été relues une à une).</p>'),
 'en': ('<p><strong>Added 13 October 2026: early May 1916 (JACAR B03050089000).</strong> Sixteen more telegrams, from 30 April to 15 May. '
        'Besides the messages from Tokyo to “Junzaburo”, this batch contains <em>replies</em> sent from Shanghai to Tokyo (address “Linwailuk”), '
        'enciphered with the same condenser; one is signed <span lang="zh-Hant">文</span> (Sun Wen, that is, Sun Yat-sen). The telegrams of 11 and 12 May carry a different prefix, “Thirtyeight”, and read with a <strong>new table</strong>, recovered here (see the <a href="method.html#thirtyeight">Method</a> article). '
        'A telegram from Manila to Tōyama Mitsuru (頭山滿), relayed verbatim to Shanghai, reads with the Manila-to-Tōyama key already published' + SUP +
        ' and is signed <span lang="zh-Hant">誠</span>. A telegram from Honolulu (prefix “Aloha”), signed <span lang="zh-Hant">鐵城</span> (Wu Tiecheng), reads with the “Honolulu” key already published' + SUP + ', with an alphabet without q and with w (the same as the New York 1915 table; recovered on 23 October 2026, the first reading took w for v); it announces that Huang [Xing] and Deng are arriving in Japan. A second one, of 16 May, was added on 23 October 2026. The letters were read by Claude; the 23 doubtful words were '
        '<strong>checked against the image by Brice Dudout</strong>, then targeted re-readings on 13 and 14 October 2026, made without knowing the meaning, checked every remaining doubtful code and the g/q/y and d/x/n confusions (the other letters were not re-read one by one).</p>'),
 'zh-Hant': ('<p><strong>2026年10月13日補充：1916年5月上旬（JACAR B03050089000）。</strong>新增十六封電報（4月30日至5月15日）。除東京致「Junzaburo」的電報外，'
        '本批還有由上海發往東京（地址「Linwailuk」）的<em>覆電</em>，使用同一壓縮碼；其中一封署名<span lang="zh-Hant">文</span>（孫文）。5月11日、12日兩電冠以另一前綴「Thirtyeight」，以此處找出的<strong>新碼表</strong>讀出（見<a href="method.html#thirtyeight">方法</a>一文）。'
        '一封馬尼拉致頭山滿的電報，原樣轉發上海，以已發表的馬尼拉→頭山密鑰' + SUP + '讀出，署名<span lang="zh-Hant">誠</span>。一封檀香山電報（前綴「Aloha」），署名<span lang="zh-Hant">鐵城</span>（吳鐵城），以已發表的「檀香山」密鑰' + SUP + '讀出，其字母表無 q 而有 w（與1915年紐約碼表相同；2026年10月23日找出，初讀誤以 w 為 v）；內容是黃、鄧抵日。另有5月16日一電，於2026年10月23日補入。'
        '字母由 Claude 讀出，存疑詞已由 Brice Dudout <strong>對照影像核對</strong>；2026年10月13、14日的專項重讀（在不知文意的情況下進行）又核對了其餘全部存疑電碼及 g/q/y、d/x/n 易混字母（其餘字母未逐一重讀）。</p>'),
 'ja': ('<p><strong>2026年10月13日追加：1916年5月上旬（JACAR B03050089000）。</strong>4月30日から5月15日までの電報16通を追加。東京から「Junzaburo」宛の電報に加え、'
        'この束には上海から東京（宛名「Linwailuk」）への<em>返電</em>があり、同じ圧縮符号で暗号化されている。うち1通は<span lang="zh-Hant">文</span>（孫文）の署名。5月11日と12日の電報は別の前置語「Thirtyeight」を持ち、ここで復元した<strong>新しい表</strong>で読める（<a href="method.html#thirtyeight">方法</a>の記事を参照）。'
        'マニラから頭山満宛の電報は、そのまま上海へ転送されており、既発表のマニラ→頭山鍵' + SUP + 'で読め、<span lang="zh-Hant">誠</span>の署名がある。ホノルル発の電報（前置語「Aloha」）は<span lang="zh-Hant">鐵城</span>（呉鉄城）の署名で、既発表の「ホノルル」鍵' + SUP + 'を、q がなく w を含む文字表（1915年ニューヨーク表と同じ。2026年10月23日に判明、初読では w を v とみなしていた）で読み、黄と鄧の日本到着を伝える。5月16日の1通を2026年10月23日に追加。'
        '文字は Claude が読み、疑わしい語は Brice Dudout が<strong>画像と照合した</strong>。さらに2026年10月13・14日の重点再読（意味を知らずに行った）で、残る疑わしい符号すべてと g/q/y・d/x/n の紛らわしい文字を確認した（その他の文字は一字ずつは再読していない）。</p>'),
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
    LAB[_lang]['intro'] += _INTRO_MAI[_lang]; LAB[_lang]['channel'].update({'honolulu1916w': {'fr': 'Clé « Honolulu » (grille de Bourdeau), alphabet « Aloha » sans q, avec w', 'en': '“Honolulu” key (Bourdeau’s grid), “Aloha” alphabet without q, with w', 'zh-Hant': '「檀香山」密鑰（Bourdeau 的方格），「Aloha」字母表無 q 有 w', 'ja': '「ホノルル」鍵（Bourdeauの表）、「Aloha」文字表（q なし、w あり）'}[_lang], 'yamada1916w': {'fr': 'Condensateur « Yamada » (w = p)', 'en': 'Condenser “Yamada” (w = p)', 'zh-Hant': '壓縮碼「山田」（w = p）', 'ja': '圧縮符号「山田」（w = p）'}[_lang], 'k38': {'fr': 'Table « Thirtyeight »', 'en': '“Thirtyeight” table', 'zh-Hant': '「Thirtyeight」碼表', 'ja': '「Thirtyeight」表'}[_lang], 'man2': {'fr': 'Clé Manille → Tōyama', 'en': 'Manila → Tōyama key', 'zh-Hant': '馬尼拉→頭山密鑰', 'ja': 'マニラ→頭山鍵'}[_lang]}); LAB[_lang]['read'] = _READ[_lang]

CONF['n0504a']['云'] = 'mot'   # 云云 (fin de citation), relu le 13/10/2026
CONF.setdefault('n0615', {})['銘'] = 'nom'; CONF.setdefault('n0515', {})['云'] = 'mot'   # 兆銘 ; 云云
CONF['n0531b']['効'] = 'variante'   # 効力 (= 效力), relu le 14/10/2026 (lot 3)

# ---- Table de Huang Xing (séance C38, 15/10/2026) : 6 télégrammes Tokyo → Junzaburo sans préfixe (signés 興) et
# 3 télégrammes Shanghai → « Ylchang » (signés 文) ; lettres lues par Brice (lot R3), lettres douteuses vérifiées à l'aveugle (H1) ----
R.update({
 'n0526': ('械事已電日{當}局否？彼有不{欲}公急赴魯意。乞覆。興', []),
 'n0528': ('敬電因移居後到。昨彼{無}暇，今晚往商，{如}何，再覆。興', []),
 'n0531c': ('借款事弟未與聞，日當局亦未通告，內容尚不詳。‹旦›', []),
 'n0531d': ('款二十萬、武器若干，囑漢民親請青木再電當局，可望成功。興', []),
 'n0603b': ('今夜晤商田中：槍二千、砲六門，不日可運。後仍‹曹›望，惟不欲先及一{有}資望軍人調和，而統一之。彼意在‹炧›‹棲›，如何？請覆。興', []),
 'n0606': ('仍‹曹›望，惟不欲先生急赴該處，可請溥{泉}及一有資望軍人調和', []),
 'y0602': ('電悉。已{告}青木，請‹兇›亦盡力{所}能至。文', []),
 'y0606': ('烈武往‹雌›統一各軍，皆請溥{泉}。已遣‹掫›日偕許崇智往。卄萬事，青木謂已電‹筦›，請力促成。應‹懸›需。孫文。魚', []),
 'y0530': ('‹綹›海軍三井消息：三井、三菱、大倉□·‹揜›‹蓓›‹睞›萬，供南軍‹租›但‹頍›‹岑›黃·逝署借約‹岑›覆謂‹岑›滇合‹叱›‹巫›贛確否？成行如‹侍›應如·因應谷酌奪', []),
})
_LV16 = {'n0526': [P_('sens'), P_('sens', 'jumeau')], 'n0528': [P_('sens'), Q_('sens')], 'n0603b': [P_('jumeau')], 'n0606': [P_('sens', 'contexte')],
         'y0602': [Q_('sens'), Q_('sens')], 'y0606': [P_('sens', 'contexte')]}
for _sid, _lv in _LV16.items(): R[_sid] = (R[_sid][0], _lv)
# relecture H1 (15/10/2026) : la lettre décodée est bien écrite ainsi ⇒ proposition « maintenue » (erreur de 1916 supposée)
MAINT |= {('n0526', '當'), ('n0526', '欲'), ('n0528', '無'), ('n0606', '泉'), ('y0606', '泉')}
CONF.update({'n0531d': {'干': 'mot'}, 'n0606': {'溥': 'nom'}, 'y0606': {'溥': 'nom', '偕': 'mot', '卄': 'variante'}})
KEYS.update({'n0526': ['械事', '魯'], 'n0528': ['移居', '今晚往商'], 'n0531c': ['借款', '日當局'], 'n0531d': ['二十萬', '漢民', '青木'],
             'n0603b': ['田中', '槍二千', '砲六門'], 'n0606': ['溥泉', '軍人調和'], 'y0602': ['青木', '盡力'], 'y0606': ['烈武', '許崇智', '青木', '孫文'],
             'y0530': ['三井', '三菱', '大倉']})
_TR16 = {
 'fr': {
  'n0526': "L'affaire des armes a-t-elle été télégraphiée aux autorités japonaises (?) ? Ils ne souhaitent pas que vous vous rendiez en hâte au Shandong (魯). Veuillez répondre. — Xing (Huang Xing).",
  'n0528': "Votre télégramme m'est parvenu après mon déménagement. Hier ils n'avaient pas le temps ; ce soir j'irai en discuter. Quoi qu'il en soit, je répondrai à nouveau. — Xing.",
  'n0531c': "Je n'ai pas été mis au courant de l'emprunt ; les autorités japonaises n'ont rien notifié non plus ; le contenu en est encore inconnu. […]",
  'n0531d': "Fonds : 200 000 ; armes : une certaine quantité. J'ai demandé à [Hu] Hanmin (漢民) d'aller en personne prier Aoki (青木) de télégraphier à nouveau aux autorités ; on peut espérer le succès. — Xing.",
  'n0603b': "Ce soir, entretien avec Tanaka (田中) : 2 000 fusils et 6 canons pourront être expédiés sous peu. Ensuite […], mais [ils] ne souhaitent pas que vous [vous précipitiez là-bas ; on pourrait prier Puquan] et un militaire de prestige de servir de médiateurs et d'unifier [les forces]. Leur intention est […] : qu'en pensez-vous ? Veuillez répondre. — Xing. (Entre crochets, neuf codes perdus à la transmission, rétablis par le télégramme du 6 juin.)",
  'n0606': "(Retransmission du passage du 3 juin) […] mais [ils] ne souhaitent pas que vous, Monsieur, vous précipitiez là-bas ; on pourrait prier Puquan (溥泉, Zhang Ji) et un militaire de prestige de servir de médiateurs.",
  'y0602': "Télégramme reçu. J'ai déjà informé (?) Aoki (青木) ; prière […] de faire aussi tout ce qui est en votre pouvoir (?). — Wen (Sun Yat-sen).",
  'y0606': "Liewu (烈武, Bai Wenwei) part […] unifier les armées ; tous demandent Puquan (溥泉, Zhang Ji). J'ai envoyé […], qui part le […] avec Xu Chongzhi (許崇智). Pour l'affaire des 200 000, Aoki dit avoir déjà télégraphié […] ; prière de pousser à la conclusion. […] — Sun Wen (孫文). Le 6.",
  'y0530': "(Lecture lacunaire.) […] nouvelles de la Marine et de Mitsui : Mitsui, Mitsubishi, Ōkura […] l'armée du Sud […] Cen [Chunxuan] (岑) […] contrat d'emprunt […] le Yunnan […] est-ce exact ? […] décidez."},
 'en': {
  'n0526': "Has the arms matter been telegraphed to the Japanese authorities (?)? They do not wish you to rush to Shandong (魯). Please reply. — Xing (Huang Xing).",
  'n0528': "Your telegram reached me after I moved. Yesterday they had no time; this evening I shall go and discuss it. Whatever happens, I shall reply again. — Xing.",
  'n0531c': "I have not been informed about the loan; the Japanese authorities have not notified anything either; its content is still unknown. […]",
  'n0531d': "Funds: 200,000; arms: a certain quantity. I have asked [Hu] Hanmin (漢民) to go in person and ask Aoki (青木) to telegraph the authorities again; success can be hoped for. — Xing.",
  'n0603b': "This evening I met Tanaka (田中) and discussed: 2,000 rifles and 6 guns can be shipped shortly. Then […], but [they] do not wish you [to rush there; Puquan could be asked,] together with a respected military man, to mediate and unify [the forces]. Their intention is […]: what do you think? Please reply. — Xing. (In brackets, nine codes lost in transmission, restored by the telegram of 6 June.)",
  'n0606': "(Retransmission of the passage of 3 June) […] but [they] do not wish you, Sir, to rush there; Puquan (溥泉, Zhang Ji) and a respected military man could be asked to mediate.",
  'y0602': "Telegram received. I have already informed (?) Aoki (青木); please […] also do all you can (?). — Wen (Sun Yat-sen).",
  'y0606': "Liewu (烈武, Bai Wenwei) is going […] to unify the armies; all ask for Puquan (溥泉, Zhang Ji). I have sent […], leaving on the […] with Xu Chongzhi (許崇智). On the 200,000 matter, Aoki says he has already telegraphed […]; please press for its conclusion. […] — Sun Wen (孫文). The 6th.",
  'y0530': "(Partial reading.) […] news of the Navy and of Mitsui: Mitsui, Mitsubishi, Ōkura […] the Southern army […] Cen [Chunxuan] (岑) […] the loan contract […] Yunnan […] is it confirmed? […] please decide."},
 'ja': {
  'n0526': "武器の件は日本当局（？）に打電したか。彼らは公が急いで魯（山東）へ赴くことを望んでいない。返電を乞う。興（黄興）。",
  'n0528': "貴電は転居後に届いた。昨日は彼らに暇がなく、今晩相談に行く。いずれにせよ改めて返電する。興。",
  'n0531c': "借款の件は私は聞かされておらず、日本当局からも通告はなく、内容はなお不詳。……",
  'n0531d': "資金二十万、武器若干。漢民（胡漢民）に自ら青木に当局へ再び打電するよう頼ませた。成功が見込める。興。",
  'n0603b': "今夜、田中と会って相談した。小銃二千、砲六門は近日中に送れる。その後……、ただし〔彼らは〕先〔生が急いでそこへ赴くことを望まず、溥泉〕と声望ある軍人に調停させ、統一させるのがよい。彼の意図は……、いかがか。返電を請う。興。（〔 〕内の9符号は送信中に失われ、6月6日の電報で補われる。）",
  'n0606': "（6月3日の電報の一節の再送）……ただし〔彼らは〕先生が急いでそこへ赴くことを望まない。溥泉（張継）と声望ある軍人に調停を頼むのがよい。",
  'y0602': "電報拝見。すでに青木に伝えた（？）。……もできる限り尽力されたい（？）。文（孫文）。",
  'y0606': "烈武（柏文蔚）は……へ赴いて各軍を統一する。皆、溥泉（張継）を請う。すでに……を派遣し、……日に許崇智とともに出発。二十万の件は青木がすでに……に打電したという。成立を促されたい。……孫文。魚（6日）。",
  'y0530': "（部分的な読み）……海軍と三井の消息：三井・三菱・大倉……南軍……岑（岑春煊）……借款契約……雲南……確かか。……斟酌されたい。"},
 'zh-Hant': {
  'n0526': "械事已電日[當]局否？彼有不[欲]公急赴魯意。乞覆。興（黃興）。",
  'n0528': "敬電因移居後到。昨彼[無]暇，今晚往商，[如]何，再覆。興。",
  'n0531c': "借款事弟未與聞，日當局亦未通告，內容尚不詳。……",
  'n0531d': "款二十萬、武器若干，囑漢民（胡漢民）親請青木再電當局，可望成功。興。",
  'n0603b': "今夜晤商田中：槍二千、砲六門，不日可運。後仍……望，惟不欲先〔生急赴該處，可請溥泉〕及一有資望軍人調和，而統一之。彼意在……，如何？請覆。興。（〔 〕內九碼傳送時遺失，由6月6日電補回。）",
  'n0606': "（重發6月3日電文一段）仍……望，惟不欲先生急赴該處，可請溥泉（張繼）及一有資望軍人調和。",
  'y0602': "電悉。已[告]青木，請……亦盡力[所]能至。文（孫文）。",
  'y0606': "烈武（柏文蔚）往……統一各軍，皆請溥泉（張繼）。已遣……日偕許崇智往。廿萬事，青木謂已電……，請力促成。……孫文。魚（六日）。",
  'y0530': "（部分讀出）……海軍三井消息：三井、三菱、大倉……南軍……岑（岑春煊）……借約……滇……確否？……酌奪。"},
}
for _lang in ('fr', 'en', 'zh-Hant', 'ja'): TR[_lang].update(_TR16[_lang])
_INTRO16 = {
 'fr': ('<p><strong>Ajout du 15 octobre 2026 : la table de Huang Xing (fin mai – juin 1916).</strong> Neuf télégrammes de plus, lus avec une table nouvelle '
        'que nous avons retrouvée (voir la <a href="method.html#huangxing">Méthode</a>) : six de Tokyo à « Junzaburo », envoyés sans préfixe et signés '
        '<span lang="zh-Hant">興</span> (Huang Xing, à Tokyo depuis le 9 mai), et trois de Shanghai à « Ylchang » (Huang Xing), signés <span lang="zh-Hant">文</span> '
        '(Sun Yat-sen). Les lettres ont été lues par Brice Dudout ; les lettres douteuses ont été vérifiées à l\'image sans connaître le sens. Le télégramme du 30 mai '
        'reste en grande partie illisible.</p>'),
 'en': ('<p><strong>Added 15 October 2026: Huang Xing\'s table (late May – June 1916).</strong> Nine more telegrams, read with a new table we recovered '
        '(see <a href="method.html#huangxing">Method</a>): six from Tokyo to “Junzaburo”, sent without a prefix and signed <span lang="zh-Hant">興</span> '
        '(Huang Xing, in Tokyo since 9 May), and three from Shanghai to “Ylchang” (Huang Xing), signed <span lang="zh-Hant">文</span> (Sun Yat-sen). '
        'The letters were read by Brice Dudout; doubtful letters were checked against the image without knowing the meaning. The telegram of 30 May remains largely unreadable.</p>'),
 'zh-Hant': ('<p><strong>2026年10月15日補充：黃興的碼表（1916年5月底至6月）。</strong>新增九封電報，以我們找出的新碼表讀出（見<a href="method.html#huangxing">方法</a>）：'
        '六封由東京發往「Junzaburo」，不冠前綴，署名<span lang="zh-Hant">興</span>（黃興，5月9日抵東京）；三封由上海發往「Ylchang」（黃興），署名<span lang="zh-Hant">文</span>（孫文）。'
        '字母由 Brice Dudout 讀出，存疑字母已在不知文意的情況下對照影像核對。5月30日一封大部分仍無法讀出。</p>'),
 'ja': ('<p><strong>2026年10月15日追加：黄興の表（1916年5月末〜6月）。</strong>我々が復元した新しい表で、さらに9通を読んだ（<a href="method.html#huangxing">方法</a>を参照）。'
        '東京から「Junzaburo」宛の6通は前置語なしで、<span lang="zh-Hant">興</span>（5月9日から東京にいた黄興）の署名がある。上海から「Ylchang」（黄興）宛の3通は'
        '<span lang="zh-Hant">文</span>（孫文）の署名がある。文字はBrice Dudoutが読み、疑わしい文字は意味を知らずに画像と照合した。5月30日の電報は大部分がなお読めない。</p>'),
}
_TOC16 = {'fr': ('Table de Huang Xing (Tokyo → Shanghai, signée 興)', 'Table de Huang Xing (Shanghai → « Ylchang », signée 文)', 'Table de Huang Xing'),
          'en': ("Huang Xing's table (Tokyo → Shanghai, signed 興)", "Huang Xing's table (Shanghai → “Ylchang”, signed 文)", "Huang Xing's table"),
          'zh-Hant': ('黃興的碼表（東京 → 上海，署名「興」）', '黃興的碼表（上海 → 「Ylchang」，署名「文」）', '黃興的碼表'),
          'ja': ('黄興の表（東京 → 上海、「興」署名）', '黄興の表（上海 → 「Ylchang」、「文」署名）', '黄興の表')}
for _lang in LAB:
    LAB[_lang]['intro'] += _INTRO16[_lang]
    LAB[_lang]['toc']['h16'], LAB[_lang]['toc']['h16-y'], LAB[_lang]['channel']['h16'] = _TOC16[_lang]

# ---- Gloses des noms de navires (14/10/2026) : affichées sous la traduction ; sources : Wikipédia japonaise
# (博愛丸, 春洋丸), indicateurs de la Tōyō Kisen ; 春日丸 : ligne de 1916 non vérifiée ----
_G = {
 'fr': {'hakuai': "Hakuai-maru (博愛丸), navire-hôpital de la Croix-Rouge japonaise (1898), exploité en temps de paix par la compagnie Nippon Yūsen (NYK) comme cargo-passagers sur la ligne de Shanghai.",
        'kasuga': "Kasuga-maru (春日丸), paquebot de la compagnie Nippon Yūsen (NYK) ; la ligne qu'il desservait en 1916 n'est pas vérifiée.",
        'shunyo': "Shun’yō-maru (春洋丸), paquebot de la Tōyō Kisen (1911), ligne de San Francisco, avec escales à Honolulu, Yokohama, Kobe, Nagasaki, Shanghai et Hong Kong."},
 'en': {'hakuai': "Hakuai-maru (博愛丸), a hospital ship of the Japanese Red Cross (1898), run in peacetime by the Nippon Yūsen company (NYK) as a cargo-passenger ship on the Shanghai line.",
        'kasuga': "Kasuga-maru (春日丸), a liner of the Nippon Yūsen company (NYK); the line she served in 1916 has not been checked.",
        'shunyo': "Shun’yō-maru (春洋丸), a liner of the Tōyō Kisen company (1911), San Francisco line, calling at Honolulu, Yokohama, Kobe, Nagasaki, Shanghai and Hong Kong."},
 'zh-Hant': {'hakuai': "博愛丸為日本赤十字社醫院船（1898年建成），平時由日本郵船公司作為上海航線客貨船營運。",
        'kasuga': "春日丸為日本郵船公司輪船；1916年所行航線尚未查證。",
        'shunyo': "春洋丸為東洋汽船公司客輪（1911年建成），舊金山航線，停靠檀香山、橫濱、神戶、長崎、上海、香港。"},
 'ja': {'hakuai': "博愛丸は日本赤十字社の病院船（1898年竣工）。平時は日本郵船が上海航路の貨客船として運航した。",
        'kasuga': "春日丸は日本郵船の汽船。1916年当時の就航航路は未確認。",
        'shunyo': "春洋丸は東洋汽船の客船（1911年竣工）。サンフランシスコ航路（ホノルル・横浜・神戸・長崎・上海・香港に寄港）。"},
}
_SHIPS = {'n0503b': ['hakuai'], 'n0504a': ['kasuga'], 'n0607': ['kasuga'], 's0505': ['shunyo']}
NOTE = {lang: {sid: ' '.join(_G[lang][k] for k in ks) for sid, ks in _SHIPS.items()} for lang in _G}
NOTE_LAB = {'fr': 'Note :', 'en': 'Note:', 'zh-Hant': '註：', 'ja': '注：'}
_N16 = {
 'fr': {'n0603b': "Deux copies du formulaire (images 0145 et 0151–0152) : les lettres suivent la première, la seconde tranchant là où elles diffèrent. Neuf codes ont été perdus à la transmission après 先 ; le télégramme du 6 juin (0152b) renvoie ce passage.",
        'n0606': "Retransmission du passage du 3 juin (0145) où neuf codes s'étaient perdus ; deux copies du formulaire (images 0152 et 0159).",
        'y0530': "Lecture lacunaire : deux groupes ne se lisent pas comme syllabes (« hopt », « kbji ») et plusieurs codes restent douteux ; suite sur l'image 0116.",
        'n0531c': "La fin (旦) diffère de la signature 興 des autres télégrammes de Tokyo ; une copie dactylographiée existe."},
 'en': {'n0603b': "Two copies of the form (images 0145 and 0151–0152): the letters follow the first, the second deciding where they differ. Nine codes were lost in transmission after 先; the telegram of 6 June (0152b) resends this passage.",
        'n0606': "Retransmission of the passage of 3 June (0145) in which nine codes had been lost; two copies of the form (images 0152 and 0159).",
        'y0530': "Partial reading: two groups do not read as syllables (“hopt”, “kbji”) and several codes remain doubtful; continued on image 0116.",
        'n0531c': "The ending (旦) differs from the signature 興 of the other Tokyo telegrams; a typed copy exists."},
 'zh-Hant': {'n0603b': "電報紙有兩份抄本（影像0145及0151–0152）：字母依第一份，兩者不同處以第二份為準。「先」字後有九碼在傳送中遺失；6月6日電（0152b）補發此段。",
        'n0606': "補發6月3日電（0145）中遺失九碼的一段；電報紙有兩份抄本（影像0152及0159）。",
        'y0530': "部分讀出：兩組字母不成音節（「hopt」、「kbji」），多個電碼仍存疑；續見影像0116。",
        'n0531c': "結尾（旦）與東京其他電報的署名「興」不同；另有一份打字抄本。"},
 'ja': {'n0603b': "用紙の写しが二通ある（画像0145、0151–0152）。文字は一通目に従い、異なる箇所は二通目で決めた。「先」の後の9符号は送信中に失われ、6月6日の電報（0152b）がこの一節を再送している。",
        'n0606': "6月3日の電報（0145）で9符号が失われた一節の再送。用紙の写しが二通ある（画像0152、0159）。",
        'y0530': "部分的な読み：二つの組は音節として読めず（「hopt」「kbji」）、いくつかの符号はなお疑わしい。続きは画像0116。",
        'n0531c': "末尾（旦）は東京発の他の電報の署名「興」と異なる。タイプ打ちの写しがある。"},
}
for _lang in _N16: NOTE[_lang].update(_N16[_lang])
# 0512 : passage en anglais chiffré avec la clé de Rosamonde (15/10/2026)
_P12 = {
 'fr': "Après 如下 (« comme suit »), entre zoxeyujore et kuzixacujo, le formulaire porte deux groupes qui ne sont pas des syllabes (absents de la ligne de lettres ci-dessus) : « wicuhaelou woipeilyce » est de l'anglais chiffré avec la clé des télégrammes de Rosamonde. Lettre à lettre : « mrsayuoteamerporthso », soit « Mrs …, steamer Porthos » à deux écarts près (le s de steamer, l'ordre de os) ; le nom de la passagère reste incertain (« Ayu » ?). C'est l'adresse où télégraphier pendant la traversée : le Porthos, le « navire français » (法船) du texte, que le télégramme de Tokyo du 13 mai (« Rosamonde. Porthos. ») nomme aussi. Le chiffre chinois reprend ensuite (請派二人接…).",
 'en': "After 如下 (“as follows”), between zoxeyujore and kuzixacujo, the form carries two groups that are not syllables (left out of the letter line above): “wicuhaelou woipeilyce” is English enciphered with the key of the Rosamonde telegrams. Letter by letter: “mrsayuoteamerporthso”, i.e. “Mrs …, steamer Porthos” with two slips (the s of steamer, the order of os); the passenger's name is uncertain (“Ayu”?). This is the address to telegraph to during the voyage: the Porthos, the “French ship” (法船) of the text, also named in the Tokyo telegram of 13 May (“Rosamonde. Porthos.”). The Chinese cipher then resumes (請派二人接…).",
 'zh-Hant': "「如下」之後、zoxeyujore 與 kuzixacujo 之間，電報紙上有兩組字母不成音節（上方字母行未列入）：「wicuhaelou woipeilyce」是用 Rosamonde 電報的密鑰加密的英文。逐字母解出「mrsayuoteamerporthso」，即「Mrs …, steamer Porthos」，有兩處出入（steamer 的 s、os 的次序）；乘客姓名仍不確定（「Ayu」？）。這是航行途中的收電地址：Porthos 號即電文中的「法船」，5月13日東京發出的電報（「Rosamonde. Porthos.」）亦提及此船。其後恢復中文密碼（請派二人接……）。",
 'ja': "「如下」の後、zoxeyujore と kuzixacujo の間に、音節にならない二組がある（上の文字列には含めていない）。「wicuhaelou woipeilyce」は Rosamonde 電報の鍵で暗号化された英語である。一字ずつ解くと「mrsayuoteamerporthso」、すなわち「Mrs …, steamer Porthos」（steamer の s と os の順序の二か所が異なる）。乗客の名は不確か（「Ayu」？）。航海中の打電先であり、Porthos 号は本文の「法船」（フランス船）、5月13日の東京発の電報（「Rosamonde. Porthos.」）にも出てくる。その後、中国語の暗号に戻る（請派二人接……）。",
}
for _lang in _P12: NOTE[_lang]['n0512'] = _P12[_lang]

def build():
    msgs = []
    for sid, rec, page, (mo, da), tm, s, prefix in SEL:
        if sid in LOCAL: continue                      # en cours en local : pas sur le site
        key = KEY.get(sid, 'yamada1916'); T = bkeys.KEYS[key]
        s = dx_overrides.apply_stream(s, DX.get(('n1916', sid), {}), sid)   # relecture ciblée (Brice, 13/10/2026)
        d = [(s[i:i + 4], ('%02d%02d' % (T[s[i:i + 2]], T[s[i + 2:i + 4]])) if s[i:i + 2] in T and s[i + 2:i + 4] in T else '····') for i in range(0, len(s) - 3, 4)]; codes = [c for _, c in d];   # accepte w (yamada1916w) ; comme bkeys.decode, ignore une syllabe finale seule ; syllabe hors table → « ···· » (illisible)
        chars = [CH(c) if c.isdigit() else '·' for c in codes]; nums = [int(c) if c.isdigit() else 0 for c in codes]
        letters = ''.join(syl for syl, _ in d)
        text, levels = R[sid]
        toks, props = restitution.parse(text, chars)
        assert len(props) == len(levels), sid
        marked, i, k = set(), 0, 0
        while k < len(text):
            c = text[k]
            if c in restitution.PUNCT: k += 1; continue
            if c == '「' and restitution.is_clear(text, k): k = text.index('」', k) + 1; continue
            if c in '{‹':
                if c == '‹': marked.add(i)
                i += 1; k += 3; continue
            i += 1; k += 1
        status = []
        for i, c in enumerate(codes):
            rare = float(uni[nums[i]]) - REF < 1; cf = CONF.get(sid, {}).get(chars[i])
            if not c.isdigit(): status.append('illisible')
            elif rare and cf and i not in marked: status.append('confirmé:' + cf)
            elif rare or i in marked or i in props: status.append('douteux')
            else: status.append('ok')
        alts = {str(i): a for i, st in enumerate(status) if st == 'douteux' and i not in props for a in [BC.alts_for(letters, i, nums, T)] if a}
        out = []
        for (lvl, reasons), i in zip(levels, props):
            ch = next(t[0] for t in toks if t[1] == i and t[2])
            ep = edit_path_alias(letters[4 * i:4 * i + 4], T, ch)
            assert ep and len(ep['edits']) <= 2, (sid, i, ch, ep)
            out.append(dict(i=i, ch=ch, orig=chars[i], level=lvl, reasons=reasons, letters=letters[4 * i:4 * i + 4], image='divergente' if (sid, ch) in DIVERGE else 'maintenue' if (sid, ch) in MAINT else None, **ep))
        after = list(nums)
        for p in out: after[p['i']] = int(p['code'])
        toc = {'yamada1916w': 'yamada1916'}.get(key, key) + ('-sh' if sid.startswith('s') else '-y' if sid.startswith('y') else '')
        n = '%04d' % (page + IMG_OFFSET[rec])            # n° d'image JACAR, comme les autres télégrammes du site
        VER = dx_overrides.verified(WENMI).get(('n1916', sid), [])
        msgs.append({'id': sid, 'verified': [i for i in VER if status[i] in ('douteux', 'illisible')], 'label': n + POS.get(sid, ''), 'toc': toc, 'grid': key, 'fiche': {'img': 'n' + n, 'n': n, 'keys': KEYS[sid]}, 'route': ROUTES.get(sid, ROUTE), 'record': rec, 'md': [mo, da], 'page': page,
                     'time': tm, 'prefix': prefix, 'letters': letters, 'codes': codes, 'chars': chars, 'status': status, 'fixed': {}, 'alts': alts,
                     'expected': {}, 'readable': {'toks': [[c, i, p] for c, i, p in toks], 'props': out, 'score': [BC.mean_score(nums), BC.mean_score(after)]}})
    msgs.sort(key=lambda m: (m['md'], form_times.minutes(m['time']), m['label']))   # par date et heure du formulaire, comme les autres séries
    stats = {'tels': len(msgs), 'codes': sum(len(m['codes']) for m in msgs), 'douteux': sum(s == 'douteux' for m in msgs for s in m['status']),
             'confirmé': sum(s.startswith('confirmé') for m in msgs for s in m['status'])}
    T2 = c1916_i18n.t2s_table(WENMI); i18n = {}
    for lang in ('fr', 'en', 'zh-Hant', 'ja'):
        dd = dict(LAB[lang]); dd['tr'] = {k: v for k, v in TR[lang].items() if k not in LOCAL}; dd['note'] = {k: v for k, v in NOTE[lang].items() if k not in LOCAL}; dd['noteLabel'] = NOTE_LAB[lang]; dd['date'] = {m['id']: c1916_i18n.date_of(lang, *m['md']) + (', ' + m['time'] if m['time'] else '') for m in msgs}
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
