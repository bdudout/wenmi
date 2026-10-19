#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page « 辰密 » (content/<langue>/chenmi.html), dans les cinq langues.

Usage : python3 tools/build_chenmi.py ../wenmi
Lit wenmi/cryptanalysis/c92/site-data.json (export_site.py) et segments_chenmi.py (traductions, 白話, résumés),
les scans JACAR de wenmi/working/ylc-ocr/png ; écrit data/chenmi.json, assets/img/chenmi/*.jpg et content/*/chenmi.html.
Réutilise la mise en page de build_rongmi.py (sections de message, table critique). Lancer ensuite tools/build.py."""
import html, json, os, sys
from PIL import Image

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:1] + [WENMI]
import build_rongmi as BR                               # noqa: E402
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c92'))
import segments_chenmi as SC, chenmi_key as K           # noqa: E402
import c1916_i18n as _C                                 # noqa: E402
D = json.load(open(os.path.join(WENMI, 'cryptanalysis/c92/site-data.json'), encoding='utf-8'))
M = D['messages']
LANGS = BR.LANGS
ORDER = ['N05', 'N13', 'N16', 'N26']
e = html.escape
JACAR = BR.JACAR
_T2 = _C.t2s_table(WENMI)

IMG = os.path.join(SITE, 'assets', 'img', 'chenmi')
os.makedirs(IMG, exist_ok=True)
def make_images(mid):
    out = []
    for n, (arch, page, side) in enumerate(M[mid]['meta']['sheets'], 1):
        name = f'{mid}-{n}.jpg'; dst = os.path.join(IMG, name)
        if not os.path.exists(dst):
            im = Image.open(BR.scan_path(arch, page)).convert('L'); w, h = im.size
            box = (int(w * .47), int(h * .14), int(w * .81), int(h * .89)) if side == 'R' else (int(w * .19), int(h * .14), int(w * .53), int(h * .89))
            c = im.crop(box); c = c.resize((760, int(c.height * 760 / c.width))); c.save(dst, quality=72, optimize=True)
        out.append((n, arch, page, side, '../assets/img/chenmi/' + name))
    return out

ZF = [n for n in range(99, 10, -1) if '0' not in str(n)]
EX = ['9950', '4220', '6219']
T = {
'fr': dict(
  hist='Contexte historique', histp=['Yuan Shikai meurt le 6 juin 1916 ; Li Yuanhong prend la présidence le lendemain. Les provinces du Sud soulevées contre Yuan (Armée de protection de la nation, 護國軍 ; Conseil militaire de Zhaoqing, 軍務院, dont Cen Chunxuan est le vice-chef) posent leurs conditions : retour à la Constitution provisoire de 1912 et au Parlement. N13 (9 juin) porte sur le télégramme collectif à adresser à Li, à Cen et aux provinces : Huang Xing veut une position unanime, appuyée par l’Armée de protection, et sans paraître opportuniste ; le lendemain, il détaille ses conditions dans le 共密 N17.', 'Au Hunan, le dujun Tang Xiangming (湯薌銘), nommé par Yuan, avait proclamé l’indépendance de la province le 29 mai sous la pression des révolutionnaires hunanais ; il quitte Changsha début juillet. Zhao Hengti (趙恆惕, 字 夷午), emprisonné après la Seconde Révolution de 1913 et libéré en 1915, a retrouvé en 1916 le commandement de la 1re division hunanaise : c’est le « 今又在湯督下練兵 » de N16. Zhang Xiaozhun y propose de passer par Tang Hualong (湯化龍, 濟武), frère aîné du dujun, pour que Zhao forme une division d’élite à la disposition de Li : donner au nouveau président une force sûre, l’idée que Huang Xing répète dans N18 (« 湏有武力爲之後援 »).', 'Les destinataires sont les Hunanais de Shanghai : 組 = Tan Yankai (譚延闓, 組安), ancien dujun du Hunan, que ses compatriotes pousseront en juillet vers le gouvernement de la province (il est nommé en août) ; 鳳 = Chen Jiahui (陳嘉會, 鳳先), député du Hunan. « Le Japon reste très attentiste » (N13) rejoint la phrase d’un brouillon de Huang Xing du 20 juin (« 實日當局意存觀望 ») et l’attente des emprunts des télégrammes 容密 et 共密.', 'N05 (3 juin, avant la mort de Yuan) concerne le Shandong, où plusieurs forces anti-Yuan coexistent alors : on y envisage de confier un commandement unifié à « 烈武 » (identification à Bo Wenwei, 柏文蔚, à vérifier), avec Zhang Ji. N26 recoupe le 容密 N28 : trois cents yuans pour Jiang Fangzhen (百里).'], whoh='Qui est ヒツキン ? Ce n’est sans doute pas un nom occidental : sur les mêmes formulaires, l’employé japonais écrit les adresses de Shanghai en lecture japonaise des caractères chinois — カヒロ = 霞飛路, フランスソカイ = 法租界, リショジョウ = 李書城. ヒツキン est donc probablement la lecture japonaise de deux caractères (ヒツ : 畢, 筆, 必… ; キン : 金, 欽, 勤, 錦…), nom ou adresse télégraphique du groupe hunanais ; il reste à identifier.',
  title='辰密 — quatre télégrammes de juin 1916 et leur clé',
  desc='Édition des quatre télégrammes 辰密 (juin 1916, Huang Xing, Zhang Xiaozhun, le groupe hunanais de Shanghai) et de la clé retrouvée, avec lectures probables signalées.',
  kicker='Déchiffrement · Juin 1916', h1='辰密 : quatre télégrammes et leur clé',
  stand='Quatre télégrammes chiffrés envoyés de Tokyo en juin 1916 par Huang Xing et Zhang Xiaozhun, tous à l’adresse du groupe hunanais de Shanghai (l’un à faire suivre à Bo Wenwei) : la formation d’une division pour Li Yuanhong, le télégramme collectif à Li et à Cen Chunxuan, le Shandong. La clé est un code télégraphique chinois réordonné.',
  credits='Parcours des grilles : Brice Dudout. Piste hunanaise, transcription, recherche de la clé, traduction et lectures probables : Claude (Anthropic). Relecture de tous les chiffres : Brice Dudout.',
  warn='Clé reconstruite, pas retrouvée dans un livre de code historique. Les traductions sont des propositions de travail ; les lectures probables sont distinguées du texte décodé, jamais substituées à lui. Les identifications de personnes sont des candidats.',
  keyh='La clé',
  keyp='Les feuillets se lisent par colonnes, de droite à gauche et de haut en bas (parcours proposé par Brice Dudout), en groupes de quatre chiffres ; le préfixe public <code>6591 1378</code> = <span lang="zh-Hant">辰密</span> reste en clair (N05 n’en a pas). Chaque groupe se lit comme <b>page + dizaine + unité</b> : <code>P = 100 × page + 10 × T(dizaine) + U(unité)</code>, avec retenue ordinaire ; P est le numéro du caractère dans le code télégraphique chinois (CTC).',
  pagep='<b>Page</b> (deux premiers chiffres) : les pages sont numérotées à rebours sur les nombres <b>sans zéro</b> : 99 = page 00, 98 = 01, …, 91 = 08, puis 89 = 09 (90 est sauté), 88 = 10, …, 11 = 80. C’est pourquoi aucun groupe 辰密 n’a de 0 aux milliers ni aux centaines.',
  rows=['Chiffre lu', 'dizaines', 'unités'],
  keynote='L’unité 9 vaut « 10 » : elle ajoute une dizaine (retenue). Exemples :',
  exh=['Groupe', 'Page', 'Dizaine', 'Unité', 'P', 'CTC'],
  keyhow='La clé a été trouvée sur N13, N16 et N26 (201 groupes) : un modèle « page permutée + dizaines et unités permutées », ajusté par recuit simulé, a donné un texte lisible très au-dessus des témoins mélangés ; la table de pages obtenue suivait le décompte sans zéro, qui a ensuite été imposé ; enfin deux caractères aberrants (劈 pour 力, 滠 pour 灰) ont révélé que l’unité 9 vaut 10. N05, qui n’avait pas servi, se lit ensuite d’un trait (contrôle aveugle), et N16 se termine par 灰, code du 10, comme son en-tête.',
  legend=BR.T['fr']['legend'],
  ctx='Contexte',
  ctxp=['Le préfixe 辰密 figure aussi dans l’édition des brouillons de Huang Xing (《黃興等電稿》), pour des télégrammes de juillet 1916 à ses correspondants hunanais (曾繼梧, 程潛) et à 林辰, prête-nom de sa maison de Tokyo qui, en avril, télégraphiait à Sun Yat-sen pour « l’affaire du Hunan ». Les quatre 辰密 de juin vont tous à la même adresse télégraphique, ヒツキン, 霞飛路 277 (concession française de Shanghai) ; le 共密 N27, envoyé le même jour, va à Li Shucheng dans la même rue.',
        'N13 (9 juin, Huang Xing) et N16 (10 juin, Zhang Xiaozhun) traitent du même projet : un télégramme collectif à Li Yuanhong, à Cen Chunxuan et aux provinces, à faire approuver par l’Armée de protection de la nation ; N16 propose aussi de donner à Li une division sûre en faisant former des troupes par Zhao Hengti (趙夷午) au Hunan, sous le dujun Tang Xiangming, frère de Tang Hualong (濟武). N05 (3 juin) concerne le Shandong et Bo Wenwei (烈武) ; N26 recoupe le 容密 N28 (300 yuans pour Jiang Fangzhen).'],
  srcp='Sources : formulaires JACAR <a href="sources.html#s27">[27]</a> ; édition des brouillons de Huang Xing <a href="sources.html#s29">[29]</a> ; noms de courtoisie : biographies citées en <a href="sources.html#s28">[28]</a> ; codes de jours : <a href="https://archives.sinica.edu.tw/freePage/150/32">Academia Sinica</a>. Décodeur : <a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a>.',
  methodlink='Voir aussi la <a href="method.html#chenmi">méthode</a> et les pages <a href="rongmi.html">容密</a> et <a href="gongmi.html">共密</a>.',
  noprefix='sans préfixe public'),
'en': dict(
  hist='Historical context', histp=['Yuan Shikai died on 6 June 1916; Li Yuanhong became president the next day. The southern provinces that had risen against Yuan (the National Protection Army, 護國軍; the Military Council at Zhaoqing, 軍務院, with Cen Chunxuan as vice-head) set their conditions: a return to the 1912 Provisional Constitution and Parliament. N13 (9 June) is about the joint telegram to be sent to Li, Cen and the provinces: Huang Xing wants a unanimous position, backed by the Protection Army, without appearing opportunistic; the next day he sets out his conditions in Gongmi N17.', 'In Hunan, Governor Tang Xiangming (湯薌銘), Yuan’s appointee, had declared the province independent on 29 May under pressure from Hunanese revolutionaries; he left Changsha in early July. Zhao Hengti (趙恆惕, courtesy name 夷午), imprisoned after the 1913 Second Revolution and freed in 1915, was restored in 1916 to command of the 1st Hunan Division: this is N16’s “now training troops under Governor Tang”. Zhang Xiaozhun proposes going through Tang Hualong (湯化龍, 濟武), the governor’s elder brother, to have Zhao form an elite division at Li’s disposal: giving the new president a reliable force, the idea Huang Xing repeats in N18 (“armed backing is needed”).', 'The recipients are the Hunanese in Shanghai: 組 = Tan Yankai (譚延闓, 組安), former governor of Hunan, whom his compatriots would push in July towards the provincial governorship (appointed in August); 鳳 = Chen Jiahui (陳嘉會, 鳳先), a Hunan deputy. “Japan is very much wait-and-see” (N13) echoes a draft of Huang Xing of 20 June (“實日當局意存觀望”) and the stalled loans of the Rongmi and Gongmi telegrams.', 'N05 (3 June, before Yuan’s death) concerns Shandong, where several anti-Yuan forces then coexisted: unified command there is to be offered to “烈武” (identification with Bo Wenwei, 柏文蔚, to be checked), together with Zhang Ji. N26 matches Rongmi N28: three hundred yuan for Jiang Fangzhen (百里).'], whoh='Who is ヒツキン? Probably not a Western name: on the same forms the Japanese clerk writes Shanghai addresses as Japanese readings of the Chinese characters — カヒロ = 霞飛路 (Avenue Joffre), フランスソカイ = French Concession, リショジョウ = 李書城. ヒツキン is thus probably the Japanese reading of two characters (ヒツ: 畢, 筆, 必…; キン: 金, 欽, 勤, 錦…), a name or telegraphic address of the Hunanese group; it remains to be identified.',
  title='Chenmi — four telegrams of June 1916 and their key',
  desc='Edition of the four Chenmi (辰密) telegrams (June 1916, Huang Xing, Zhang Xiaozhun, the Hunanese group in Shanghai) and of the recovered key, with probable readings marked.',
  kicker='Decipherment · June 1916', h1='Chenmi (辰密): four telegrams and their key',
  stand='Four cipher telegrams sent from Tokyo in June 1916 by Huang Xing and Zhang Xiaozhun, all to the address of the Hunanese group in Shanghai (one to be passed on to Bo Wenwei): a division for Li Yuanhong, the joint telegram to Li and Cen Chunxuan, Shandong. The key is a reordered Chinese telegraph code.',
  credits='Grid reading order: Brice Dudout. Hunan lead, transcription, key recovery, translation and probable readings: Claude (Anthropic). All digits re-read by Brice Dudout.',
  warn='The key is a reconstruction, not taken from a historical code book. Translations are working proposals; probable readings are shown beside the decoded text, never in place of it. Identifications of people are candidates.',
  keyh='The key',
  keyp='Sheets are read in columns, right to left and top to bottom (reading order proposed by Brice Dudout), in groups of four digits; the public prefix <code>6591 1378</code> = <span lang="zh-Hant">辰密</span> stays in clear (N05 has none). Each group reads as <b>page + tens + units</b>: <code>P = 100 × page + 10 × T(tens) + U(units)</code>, with ordinary carry; P is the character number in the Chinese Telegraph Code (CTC).',
  pagep='<b>Page</b> (first two digits): pages are numbered backwards over the numbers <b>without a zero</b>: 99 = page 00, 98 = 01, …, 91 = 08, then 89 = 09 (90 is skipped), 88 = 10, …, 11 = 80. This is why no Chenmi group has a 0 in the thousands or hundreds.',
  rows=['Digit read', 'tens', 'units'],
  keynote='The units digit 9 stands for “10”: it adds a ten (carry). Examples:',
  exh=['Group', 'Page', 'Tens', 'Units', 'P', 'CTC'],
  keyhow='The key was found on N13, N16 and N26 (201 groups): a “permuted page + permuted tens and units” model, fitted by simulated annealing, gave readable text far above shuffled controls; the page table it found followed the zero-free countdown, which was then imposed; finally two aberrant characters (劈 for 力, 滠 for 灰) showed that units 9 means 10. N05, not used in the search, then reads straight through (blind check), and N16 ends with 灰, the code for the 10th, as on its header.',
  legend=BR.T['en']['legend'],
  ctx='Context',
  ctxp=['The 辰密 prefix also appears in the edition of Huang Xing’s drafts (《黃興等電稿》), for telegrams of July 1916 to his Hunanese correspondents (曾繼梧, 程潛) and to 林辰, a cover name of his Tokyo household which in April cabled Sun Yat-sen about “the Hunan affair”. The four June Chenmi telegrams all go to the same telegraphic address, ヒツキン, 277 Avenue Joffre (French Concession, Shanghai); the Gongmi N27, sent the same day, goes to Li Shucheng on the same street.',
        'N13 (9 June, Huang Xing) and N16 (10 June, Zhang Xiaozhun) deal with the same plan: a joint telegram to Li Yuanhong, Cen Chunxuan and the provinces, to be approved by the National Protection Army; N16 also proposes giving Li a reliable division by having Zhao Hengti (趙夷午) train troops in Hunan, under Governor Tang Xiangming, brother of Tang Hualong (濟武). N05 (3 June) concerns Shandong and Bo Wenwei (烈武); N26 matches Rongmi N28 (300 yuan for Jiang Fangzhen).'],
  srcp='Sources: JACAR forms <a href="sources.html#s27">[27]</a>; edition of Huang Xing’s drafts <a href="sources.html#s29">[29]</a>; courtesy names: biographies cited in <a href="sources.html#s28">[28]</a>; day codes: <a href="https://archives.sinica.edu.tw/freePage/150/32">Academia Sinica</a>. Decoder: <a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a>.',
  methodlink='See also the <a href="method.html#chenmi">method</a> and the <a href="rongmi.html">Rongmi</a> and <a href="gongmi.html">Gongmi</a> pages.',
  noprefix='no public prefix'),
'ja': dict(
  hist='歴史的背景', histp=['1916年6月6日に袁世凱が死去し、翌日黎元洪が大総統に就いた。袁に対して蜂起した南方諸省（護国軍、岑春煊を副撫軍長とする肇慶の軍務院）は、1912年の臨時約法と国会の回復を条件とした。N13（6月9日）は黎・岑・各省にあてる連名電を扱う。黄興は護国軍の支持を得た一致した立場を求め、機会主義と見られることを避けようとする。翌日、共密N17で条件を詳述する。', '湖南では、袁が任命した督軍湯薌銘が5月29日、湖南の革命派の圧力で独立を宣言し、7月初めに長沙を去る。趙恒惕（字夷午）は1913年の第二革命後に投獄され1915年に釈放、1916年に湖南第一師の指揮に復帰した。N16の「今又在湯督下練兵」である。張孝準は督軍の兄湯化龍（濟武）を通じて、趙に黎の指揮下の精兵一個師を練らせることを提案する。新大総統に確かな武力を与えるという考えは、黄興がN18（「湏有武力爲之後援」）でも繰り返す。', 'あて先は上海の湖南人である。組＝譚延闓（組安）、もと湖南都督で、7月に同郷人に省の長に推され8月に任命される。鳳＝陳嘉会（鳳先）、湖南選出の議員。「日本の態度はかなり観望的」（N13）は、6月20日の黄興の電稿の「實日當局意存觀望」や、容密・共密電報の借款の停滞と一致する。', 'N05（6月3日、袁の死の前）は山東に関する。当時山東には反袁の諸勢力が並存しており、「烈武」（柏文蔚との比定は要確認）に張継とともに統一の指揮を任せることが考えられている。N26は容密N28（蔣方震＝百里への三百元）と一致する。'], whoh='ヒツキンとは誰か。おそらく西洋人の名ではない。同じ用紙で日本の係員は上海のあて先を漢字の音読みで書いている（カヒロ＝霞飛路、フランスソカイ＝仏租界、リショジョウ＝李書城）。したがってヒツキンも二字の音読み（ヒツ：畢・筆・必…、キン：金・欽・勤・錦…）で、湖南派の名か電信あて名と考えられるが、未比定である。',
  title='辰密——1916年6月の電報4通とその鍵',
  desc='辰密電報4通（1916年6月、黄興・張孝準・上海の湖南派）と復元した鍵。推定読みは区別して示す。',
  kicker='解読・1916年6月', h1='辰密：電報4通とその鍵',
  stand='1916年6月に黄興と張孝準が東京から送った暗号電報4通。すべて上海の湖南派のあて名あて（1通は柏文蔚への転送）：黎元洪のための一個師、黎と岑春煊あての連名電、山東。鍵は並べ替えた中文電碼である。',
  credits='升目の読み順：Brice Dudout。湖南の手がかり、翻字、鍵の復元、翻訳と推定読み：Claude（Anthropic）。数字はすべてBrice Dudoutが再読。',
  warn='鍵は復元であり、歴史的な電碼本から得たものではない。翻訳は作業案であり、推定読みは解読文と並べて示し、置き換えない。人物の比定は候補である。',
  keyh='鍵',
  keyp='用紙は列ごとに右から左、上から下へ読み（Brice Dudoutの提案した順序）、4桁ずつ区切る。公開の前置き<code>6591 1378</code>＝<span lang="zh-Hant">辰密</span>は平文のまま（N05にはない）。各組は<b>頁＋十の位＋一の位</b>として読む：<code>P = 100 × 頁 + 10 × T(十の位) + U(一の位)</code>（通常の繰り上がりつき）。Pが中文電碼（CTC）の番号である。',
  pagep='<b>頁</b>（最初の2桁）：<b>0を含まない</b>数を逆順に数えて頁とする。99＝00頁、98＝01、…、91＝08、89＝09（90は飛ばす）、88＝10、…、11＝80。そのため辰密の組には千の位・百の位に0がない。',
  rows=['読んだ数字', '十の位', '一の位'],
  keynote='一の位の9は「10」で、十の位に1を繰り上げる。例：',
  exh=['組', '頁', '十', '一', 'P', 'CTC'],
  keyhow='鍵はN13・N16・N26（201組）で発見した。「頁の置換＋十の位・一の位の置換」のモデルを焼きなまし法で当てはめると、攪拌した対照を大きく上回る読める文が得られ、得られた頁表は0を含まない逆順の数え方に従っていたので、それを課した。最後に二つの異常字（力に劈、灰に滠）から一の位9＝10が分かった。探索に使わなかったN05はそのまま読め（盲検）、N16は見出しと同じ10日の韻目「灰」で終わる。',
  legend=BR.T['ja']['legend'],
  ctx='背景',
  ctxp=['辰密の前置きは黄興の電稿の刊本（《黃興等電稿》）にも見え、1916年7月の湖南の同志（曾繼梧・程潛）や、東京の黄興宅の変名「林辰」あての電報に使われている。林辰は4月に「湖南ノ件」で孫文に打電している。6月の辰密4通はすべて同じ電信あて名「ヒツキン」、霞飛路277（上海フランス租界）あてである。同じ日に送られた共密N27は同じ通りの李書城あて。',
        'N13（6月9日、黄興）とN16（6月10日、張孝準）は同じ計画を扱う：黎元洪・岑春煊・各省あての連名電を護国軍の同意を得て出すこと。N16はさらに、湖南で湯薌銘督軍のもとにいる趙恒惕（夷午）に兵を練らせ、黎に確かな一個師を与えることを提案する。湯薌銘は湯化龍（濟武）の弟。N05（6月3日）は山東と柏文蔚（烈武）、N26は容密N28（蔣方震への三百元）と一致する。'],
  srcp='出典：JACARの用紙<a href="sources.html#s27">[27]</a>、黄興電稿の刊本<a href="sources.html#s29">[29]</a>、字：<a href="sources.html#s28">[28]</a>の伝記、日付の韻目：<a href="https://archives.sinica.edu.tw/freePage/150/32">中央研究院</a>。解読プログラム：<a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a>。',
  methodlink='<a href="method.html#chenmi">方法</a>と<a href="rongmi.html">容密</a>・<a href="gongmi.html">共密</a>のページも参照。',
  noprefix='公開の前置きなし'),
'zh-hant': dict(
  hist='歷史背景', histp=['1916年6月6日袁世凱死，翌日黎元洪繼任大總統。起兵反袁的南方各省（護國軍；以岑春煊為副撫軍長的肇慶軍務院）提出條件：恢復元年約法與國會。N13（6月9日）談致黎、岑及各省的聯名電：黃興要求主張一致、取得護國軍同意，免被視為取巧；次日他在共密N17中詳列條件。', '湖南方面，袁所任命的督軍湯薌銘在湘籍革命黨人壓力下於5月29日宣布獨立，7月初離開長沙。趙恆惕（字夷午）在1913年二次革命後入獄，1915年獲釋，1916年復任湖南第一師師長，即N16所謂「今又在湯督下練兵」。張孝準提議經由督軍之兄湯化龍（濟武）設法，使趙迅練精兵一師以備黎公驅遣：使新總統有可靠武力，正是黃興在N18中重申的「湏有武力爲之後援」。', '收電人為上海的湘籍人士：組＝譚延闓（組安），前湖南都督，7月間湘人推他主湘，8月獲任命；鳳＝陳嘉會（鳳先），湘籍國會議員。「日態度頗觀望」（N13）與黃興6月20日電稿「實日當局意存觀望」相合，也與容密、共密電報中借款的停頓一致。', 'N05（6月3日，袁死之前）涉及山東：當時山東有數支反袁武力並存，擬請「烈武」（比定為柏文蔚，待核）偕張繼統一事任。N26與容密N28相合：以三百元交蔣方震（百里）。'], whoh='ヒツキン是誰？大概不是西方人名：同一批電報紙上，日本電報員以漢字的日語音讀書寫上海地址——カヒロ＝霞飛路、フランスソカイ＝法租界、リショジョウ＝李書城。因此ヒツキン多半是兩個漢字的日語音讀（ヒツ：畢、筆、必……；キン：金、欽、勤、錦……），為湘籍諸人的名字或電報掛號，尚待查明。',
  title='辰密——1916年6月的四封電報及其密鑰',
  desc='四封辰密電報（1916年6月，黃興、張孝準、上海湘籍諸人）及復原的密鑰，推定讀法另行標出。',
  kicker='破譯·1916年6月', h1='辰密：四封電報及其密鑰',
  stand='1916年6月黃興與張孝準自東京發出的四封密電，均發往上海湘籍諸人的地址（其一轉柏文蔚）：為黎元洪練一師可靠之兵、致黎與岑春煊的聯名電、山東之事。密鑰是重新排列的中文電碼。',
  credits='方格讀序：Brice Dudout。湖南線索、謄錄、密鑰復原、翻譯與推定讀法：Claude（Anthropic）。全部數字由 Brice Dudout 複讀。',
  warn='密鑰為復原所得，並非取自歷史電碼本。譯文為工作稿；推定讀法與解碼文字並列，絕不替代。人物比定為候選。',
  keyh='密鑰',
  keyp='電報紙按列由右至左、由上而下讀取（Brice Dudout 提出的讀序），每四位一組；明文前綴<code>6591 1378</code>＝<span lang="zh-Hant">辰密</span>不加密（N05無前綴）。每組讀作<b>頁＋十位＋個位</b>：<code>P = 100 × 頁 + 10 × T(十位) + U(個位)</code>，按通常進位；P即中文電碼（CTC）編號。',
  pagep='<b>頁</b>（前兩位）：以<b>不含零</b>的數倒數編頁：99＝第00頁，98＝01，…，91＝08，其次89＝09（跳過90），88＝10，…，11＝80。所以辰密各組的千位與百位從不出現0。',
  rows=['所讀數字', '十位', '個位'],
  keynote='個位的9作「10」，向十位進一。示例：',
  exh=['組', '頁', '十位', '個位', 'P', 'CTC'],
  keyhow='密鑰在N13、N16、N26（201組）上找到：以模擬退火擬合「頁置換＋十位與個位置換」的模型，得出遠高於打亂對照的可讀文字；所得頁表遵循不含零的倒數，隨後即以此為規則；最後兩個反常字（「力」作「劈」，「灰」作「滠」）顯示個位9即10。未參與搜尋的N05隨即一氣讀出（盲測），N16以「灰」（十日）結尾，與電頭相符。',
  legend=BR.T['zh-hant']['legend'],
  ctx='背景',
  ctxp=['辰密之名亦見於《黃興等電稿》，用於1916年7月致湘籍同志（曾繼梧、程潛）及致「林辰」的電報。林辰是黃興東京寓所的化名，4月間曾為「湖南之事」致電孫中山。6月的四封辰密均發往同一電報地址「ヒツキン」，霞飛路277號（上海法租界）；同日所發的共密N27則致同一條路上的李書城。',
        'N13（6月9日，黃興）與N16（6月10日，張孝準）談同一件事：致黎元洪、岑春煊及各省的聯名電，須先取得護國軍同意；N16又提議讓在湘督湯薌銘麾下的趙恆惕（夷午）迅練精兵一師，以備黎公驅遣。湯薌銘是湯化龍（濟武）之弟。N05（6月3日）涉及山東與柏文蔚（烈武）；N26與容密N28相合（交蔣方震三百元）。'],
  srcp='來源：JACAR電報紙<a href="sources.html#s27">[27]</a>；《黃興等電稿》<a href="sources.html#s29">[29]</a>；字號：<a href="sources.html#s28">[28]</a>所引傳記；韻目代日：<a href="https://archives.sinica.edu.tw/freePage/150/32">中央研究院</a>。解碼程式：<a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a>。',
  methodlink='另見<a href="method.html#chenmi">方法</a>與<a href="rongmi.html">容密</a>、<a href="gongmi.html">共密</a>頁面。',
  noprefix='無明文前綴'),
}
T['zh-hans'] = {k: (_C.to_hans(v, _T2) if isinstance(v, str) else [_C.to_hans(x, _T2) for x in v] if isinstance(v, list) else v) for k, v in T['zh-hant'].items()}
for k in ('srcp', 'methodlink', 'keyp', 'pagep'):   # liens et balises lang="zh-Hant" intacts
    T['zh-hans'][k] = _C.to_hans(T['zh-hant'][k], _T2).replace('lang="zh-Hant">辰密', 'lang="zh-Hant">辰密')
T['zh-hans']['legend'] = BR.T['zh-hans']['legend']
T['zh-hans']['title'] = '辰密——1916年6月的四封电报及其密钥'

def summary(mid, L): return SC.SUMMARY[L][mid]
def translation(mid, L):
    if L == 'fr': return ' '.join(s['fr'] for s in M[mid]['segments'])
    if L == 'en': return SC.EN[mid]
    if L == 'ja': return SC.JA[mid]
    if L == 'zh-hant': return SC.BAIHUA[mid]
    return _C.to_hans(SC.BAIHUA[mid], _T2)
def date_str(mid, L):
    m = M[mid]['meta']; d = m['date']
    if L == 'fr': return m['date_note']
    q = ' ?' if mid == 'N26' else ''
    return {'en': f'June {d}, 1916{q}', 'ja': f'1916年6月{d}日{q}', 'zh-hans': f'1916年6月{d}日{q}', 'zh-hant': f'1916年6月{d}日{q}'}[L]

def key_tables(L):
    t = T[L]
    tab = (f'<div class="gm-scroll"><table><tr><th>{t["rows"][0]}</th>' + ''.join(f'<td>{d}</td>' for d in range(10)) + '</tr>'
           f'<tr><th>{t["rows"][1]}</th>' + ''.join(f'<td>{v}</td>' for v in K.T) + '</tr>'
           f'<tr><th>{t["rows"][2]}</th>' + ''.join(f'<td>{v}</td>' for v in K.U) + '</tr></table></div>')
    pages = '<div class="gm-scroll"><table><tr>' + ''.join(f'<td><code>{c}</code>→{i:02d}</td>' for i, c in enumerate(ZF[:12])) + '<td>…</td><td><code>11</code>→80</td></tr></table></div>'
    ex = (f'<div class="gm-scroll"><table><tr>' + ''.join(f'<th>{h}</th>' for h in t['exh']) + '</tr>' +
          ''.join(f'<tr><td><code>{g}</code></td><td>{g[:2]} → {K.PG[int(g[:2])]:02d}</td><td>{g[2]} → {K.T[int(g[2])]}</td><td>{g[3]} → {K.U[int(g[3])]}</td>'
                  f'<td>{K.decode(g):04d}</td><td lang="zh-Hant">{K.glyph(g)}</td></tr>' for g in EX) + '</table></div>')
    return pages, tab, ex

def message_section(mid, L):
    t = T[L]; tb = BR.T[L]; m = M[mid]; segs = m['segments']; npre = 2 if m['meta']['prefix'] else 0
    reading = ''.join(s['zh'] for s in segs)
    sep = ' : ' if L == 'fr' else ': '
    info = [f'{len(m["groups"]) - npre} {tb["groups"]}', f'{tb["date"]}{sep}{e(date_str(mid, L))}', f'{tb["dirl"]}{sep}{e(tb["dirs"]["TS"])}',
            f'{m["sheet_count"]} {tb["sheets"]}', tb['reread']] + ([t['noprefix']] if not npre else [])
    scans = ''.join(f'<p>{mid}-{n} · {a} PDF {p} {s} · <a href="{JACAR}{a}">JACAR</a> · <a href="{src}">scan</a></p>\n<img loading="lazy" src="{src}" alt="JACAR {a} {mid}-{n}">\n'
                    for n, a, p, s, src in make_images(mid))
    rows = []
    for k, g in enumerate(m['groups']):
        idx = tb['prefix'] if k < npre else str(g['i'])
        rows.append(f'<tr><td>{idx}</td><td><code>{e(g["cipher"])}</code></td><td><code>{g["ctc"]}</code></td><td lang="zh-Hant">{e(g["glyph"])}</td><td>{mid}-{g["sheet"]}</td></tr>')
    return (f'<section id="{mid}" class="gm-message"><h2>{mid}</h2>\n<p>{" · ".join(info)}</p>\n<p>{e(summary(mid, L))}</p>\n'
            f'<h3>{tb["raw"]}</h3><p class="gm-han" lang="zh-Hant">{e(m["raw"])}</p>\n'
            f'<h3>{tb["reading"]}</h3><p class="gm-han" lang="zh-Hant">{e(reading)}</p>\n'
            f'<h3>{BR.TLABEL[L]}</h3><p class="gm-tr">{e(translation(mid, L))}</p>\n'
            f'<details><summary>{tb["scans"]}</summary>\n{scans}</details>'
            f'<details><summary>{tb["table"]}</summary>\n<div class="gm-scroll"><table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in tb['th']) + '</tr></thead><tbody>\n'
            + '\n'.join(rows) + '\n</tbody></table></div></details></section>\n')

def critical_rows(mid):
    st = BR.T['fr']['st']; out = []
    for s in M[mid]['segments']:
        note = f'<p>{e(s["note"])}</p>' if s['note'] else ''
        out.append(f'<tr class="gm-{s["status"]}"><td class="gm-cell-han" lang="zh-Hant">{e(s["zh"])}</td><td>{e(s["fr"])}<small class="gm-status">{st[s["status"]]}</small>{note}</td></tr>')
    return f'<h3 id="crit-{mid}">{mid}</h3><div class="gm-scroll"><table><thead><tr><th>Lecture proposée</th><th>Traduction</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>'

def page(L):
    t = T[L]; tb = BR.T[L]; pages, tab, ex = key_tables(L)
    head = f'<!-- {json.dumps(dict(title=t["title"], description=t["desc"]), ensure_ascii=False)} -->\n<link rel="stylesheet" href="../assets/css/gongmi.css">\n'
    body = [f'<article class="article gongmi rongmi chenmi"><header class="lede">\n<p class="kicker">{t["kicker"]}</p>\n<h1>{t["h1"]}</h1><p class="standfirst">{t["stand"]}<sup class="fn"><a href="sources.html#s27">[27]</a></sup></p>\n<p>{t["credits"]}</p></header>',
            f'<div class="status warn"><p>{t["warn"]}</p></div>',
            f'<section id="key"><h2>{t["keyh"]}</h2><p>{t["keyp"]}</p><p>{t["pagep"]}</p>{pages}{tab}<p>{t["keynote"]}</p>{ex}<p>{t["keyhow"]}</p><p>{t["legend"]}</p></section>',
            f'<section id="context"><h2>{t["ctx"]}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in t['ctxp']) + f'<p>{e(t["whoh"])}</p></section>',
            f'<section id="history"><h2>{t["hist"]}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in t['histp']) + '</section>',
            '<nav class="gm-nav" aria-label="Messages">' + ''.join(f'<a href="#{m}">{m}</a>' for m in ORDER) + '</nav>']
    body += [message_section(m, L) for m in ORDER]
    if L == 'fr':
        body.append(f'<section id="critical"><h2>{tb["crit"]}</h2><p>{tb["critp"]}</p>' + ''.join(critical_rows(m) for m in ORDER) + '</section>')
    else:
        body.append(f'<section id="critical"><h2>{tb["crit"]}</h2><p>{tb["critp"]} <a href="../fr/chenmi.html#critical">{tb["critlink"]}</a></p></section>')
    body.append(f'<p>{t["srcp"]}</p>\n<p>{t["methodlink"]}</p>\n</article>')
    return head + '\n'.join(body) + '\n'

if __name__ == '__main__':
    json.dump(D, open(os.path.join(SITE, 'data', 'chenmi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for L in LANGS:
        open(os.path.join(SITE, 'content', L, 'chenmi.html'), 'w', encoding='utf-8').write(page(L))
    print('chenmi:', len(ORDER), 'messages,', len(os.listdir(IMG)), 'images')
