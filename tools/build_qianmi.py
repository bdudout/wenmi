#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page « 乾密 » (content/<langue>/qianmi.html), dans les cinq langues.

Usage : python3 tools/build_qianmi.py ../wenmi
Lit wenmi/cryptanalysis/c107/site-data.json (export_site.py) et segments_qianmi.py (traductions, 白話, résumés),
les scans JACAR de wenmi/working/ylc-ocr/png ; écrit data/qianmi.json, assets/img/qianmi/*.jpg et content/*/qianmi.html.
Même mise en page que build_chenmi.py. Modèle de clé (livre 明密 renuméroté) : S. Tomokiyo, Cryptiana [22]. Lancer ensuite tools/build.py."""
import html, json, os, sys
from PIL import Image

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:1] + [WENMI]
import build_rongmi as BR                               # noqa: E402
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c107'))
import segments_qianmi as SQ, qianmi_key as K           # noqa: E402
import c1916_i18n as _C                                 # noqa: E402
D = json.load(open(os.path.join(WENMI, 'cryptanalysis/c107/site-data.json'), encoding='utf-8'))
M = D['messages']
LANGS = BR.LANGS
ORDER = ['N09']
e = html.escape
JACAR = BR.JACAR
_T2 = _C.t2s_table(WENMI)

IMG = os.path.join(SITE, 'assets', 'img', 'qianmi')
os.makedirs(IMG, exist_ok=True)
def make_images(mid):
    out = []
    for n, (arch, page, side) in enumerate(M[mid]['meta']['sheets'], 1):
        name = f'{mid}-{n}.jpg'; dst = os.path.join(IMG, name)
        if not os.path.exists(dst):
            im = Image.open(BR.scan_path(arch, page)).convert('L'); w, h = im.size
            box = (int(w * .47), int(h * .14), int(w * .81), int(h * .89)) if side == 'R' else (int(w * .19), int(h * .14), int(w * .53), int(h * .89))
            c = im.crop(box); c = c.resize((760, int(c.height * 760 / c.width))); c.save(dst, quality=72, optimize=True)
        out.append((n, arch, page, side, '../assets/img/qianmi/' + name))
    return out

EX = ['7096', '4044', '1114']
SRC22 = '<a href="sources.html#s22">[22]</a>'
T = {
'fr': dict(
  title='乾密 — un télégramme de juin 1916 et sa clé',
  desc='Édition du télégramme 乾密 N09 (Huang Xing, Tokyo, juin 1916) et de sa clé, un livre de code « 明密 » renuméroté, retrouvée d’après une idée de S. Tomokiyo.',
  kicker='Déchiffrement · Juin 1916', h1='乾密 : un télégramme et sa clé',
  stand='Un télégramme chiffré envoyé de Tokyo par Huang Xing juste après la mort de Yuan Shikai : à Tokyo, l’attitude n’a pas changé, il attend que les négociations avancent. La clé, un livre de code « 明密 » renuméroté, a été retrouvée en suivant une idée de S. Tomokiyo.',
  credits=f'Idée du modèle de clé (livre 明密 renuméroté) : S. Tomokiyo (Cryptiana) {SRC22}. Parcours des grilles et relecture de tous les chiffres : Brice Dudout. Transcription, recherche de la clé, lectures probables et traduction : Claude (Anthropic).',
  warn='Un seul télégramme lu : la clé repose sur 17 groupes. Elle passe les contrôles (témoins, signature, date), mais trois caractères sont des lectures probables, et N03, autre télégramme 乾密 du même expéditeur, reste illisible avec elle (autre clé ou chiffres fautifs). Les traductions sont des propositions de travail ; les identifications de personnes, des candidats.',
  keyh='La clé',
  keyp='Les feuillets se lisent par colonnes, de droite à gauche et de haut en bas (parcours proposé par Brice Dudout), en groupes de quatre chiffres. Les six premiers groupes sont l’adresse, en clair (code télégraphique public) ; suit le préfixe public <code>0051 1378</code> = <span lang="zh-Hant">乾密</span> ; les 17 groupes suivants sont chiffrés. Chaque groupe se lit <b>page + colonne + ligne</b> dans un livre de code « 明密 » dont les numéros ont été réécrits : <code>P = 100 × page + 10 × colonne + ligne</code>, la ligne allant de 1 à 10 (la ligne 10 est le caractère xxx0, en bas de la colonne) ; P est le numéro du caractère dans le code télégraphique chinois (CTC).',
  pagep='<b>Page</b> (deux premiers chiffres) : page écrite moins 11 — 11 = page 00, 12 = 01, …, 50 = 39, etc.',
  rows=['Chiffre lu', 'colonne', 'ligne'],
  keynote='Exemples :', exh=['Groupe', 'Page', 'Colonne', 'Ligne', 'P', 'CTC'],
  keyhow=f'<b>L’idée de S. Tomokiyo.</b> Le 23 octobre 2026, S. Tomokiyo a montré que nos trois clés <a href="gongmi.html">共密</a>, <a href="rongmi.html">容密</a> et <a href="chenmi.html">辰密</a> ne sont que des renumérotations des pages, des colonnes et des lignes d’un livre « 明密 », sans aucun calcul {SRC22}. <b>Notre découverte.</b> Nous avons appliqué ce modèle aux télégrammes « X密 » encore illisibles : pages numérotées selon une règle simple (à rebours, en boucle ou sans zéro), colonnes et lignes permutées librement, ajustées sur un modèle de langue, avec un protocole fixé avant le calcul : messages synthétiques de même longueur (témoins positifs) et chiffres mélangés (témoins négatifs). N09 se détache nettement (score 4,47 contre 2,88 pour le meilleur témoin) ; le texte se lit, finit par la signature attendue 興 et commence par « 袁死 », ce qui s’accorde avec sa place dans le dossier (6–9 juin). Les trois groupes aberrants ont été relus deux fois sur l’image par Brice Dudout, la seconde en aveugle : les chiffres sont sûrs.',
  legend=BR.T['fr']['legend'],
  ctx='Contexte',
  ctxp=['Le formulaire (JACAR B03050089200, PDF 49) est une copie (« Copy ») sans date. L’expéditeur est la maison de Huang Xing à Tokyo, 青山南町三ノ五三 ; le destinataire, dans la concession française de Shanghai, rue カヒロ (霞飛路, avenue Joffre), au nom écrit ジヨンシヨウ, lecture japonaise de deux caractères que nous n’identifions pas. L’adresse intérieure, en clair, demande de transmettre à « Ma et Geng, mes deux frères » (馬, 耿), non identifiés.',
        'Le préfixe 乾密 figure aussi sur N03, autre télégramme parti de la même maison au début de juin ; N03 reste illisible avec la clé de N09. Les deux télégrammes sont rangés dans le dossier entre ceux du 3 et du 8 juin.'],
  whoh='« 此間態度未變 » (l’attitude ici n’a pas changé) répond en écho à N13, du 9 juin : « 日態度頗觀望 », le Japon reste très attentiste.',
  hist='Contexte historique', histp=['Yuan Shikai meurt le 6 juin 1916. Huang Xing, alors à Tokyo, négocie depuis des semaines des achats d’armes et des emprunts au Japon pour les provinces soulevées (voir les télégrammes <a href="rongmi.html">容密</a>). N09 en donne l’état au lendemain de la nouvelle : l’attitude japonaise n’a pas bougé, et il attend que les négociations prennent tournure avant de télégraphier de nouveau. Quelques jours plus tard, N13 et N17 précisent : le Japon reste attentiste et ne prêtera pas à Pékin tant que le Nord et le Sud ne seront pas unifiés.'],
  srcp=f'Sources : formulaire JACAR <a href="sources.html#s27">[27]</a> ; modèle de clé : S. Tomokiyo {SRC22} ; codes de jours : <a href="https://archives.sinica.edu.tw/freePage/150/32">Academia Sinica</a>. Décodeur et contrôle de la factorisation des clés : <a href="https://github.com/bdudout/wenmi/tree/main/solver/numeric1916">solver/numeric1916</a>.',
  methodlink='Voir aussi la <a href="method.html#qianmi">méthode</a> et les pages <a href="chenmi.html">辰密</a>, <a href="rongmi.html">容密</a> et <a href="gongmi.html">共密</a>.'),
'en': dict(
  title='Qianmi — a telegram of June 1916 and its key',
  desc='Edition of the Qianmi (乾密) telegram N09 (Huang Xing, Tokyo, June 1916) and of its key, a renumbered “明密” code book, recovered following an idea of S. Tomokiyo.',
  kicker='Decipherment · June 1916', h1='Qianmi (乾密): a telegram and its key',
  stand='A cipher telegram sent from Tokyo by Huang Xing just after Yuan Shikai’s death: in Tokyo the attitude has not changed, and he waits for the negotiations to progress. The key, a renumbered “明密” code book, was recovered following an idea of S. Tomokiyo.',
  credits=f'Idea of the key model (renumbered 明密 book): S. Tomokiyo (Cryptiana) {SRC22}. Grid reading order and re-reading of all digits: Brice Dudout. Transcription, key search, probable readings and translation: Claude (Anthropic).',
  warn='Only one telegram is read: the key rests on 17 groups. It passes the checks (controls, signature, date), but three characters are probable readings, and N03, another 乾密 telegram from the same sender, stays unreadable with it (another key or faulty digits). Translations are working proposals; identifications of people are candidates.',
  keyh='The key',
  keyp='Sheets are read in columns, right to left and top to bottom (reading order proposed by Brice Dudout), in groups of four digits. The first six groups are the address, in clear (public telegraph code); then comes the public prefix <code>0051 1378</code> = <span lang="zh-Hant">乾密</span>; the next 17 groups are enciphered. Each group reads as <b>page + column + row</b> in a “明密” code book whose numbers were rewritten: <code>P = 100 × page + 10 × column + row</code>, the row running from 1 to 10 (row 10 is the xxx0 character at the foot of the column); P is the character’s number in the Chinese telegraph code (CTC).',
  pagep='<b>Page</b> (first two digits): written page minus 11 — 11 = page 00, 12 = 01, …, 50 = 39, and so on.',
  rows=['Digit read', 'column', 'row'],
  keynote='Examples:', exh=['Group', 'Page', 'Column', 'Row', 'P', 'CTC'],
  keyhow=f'<b>S. Tomokiyo’s idea.</b> On 23 October 2026, S. Tomokiyo showed that our three keys <a href="gongmi.html">共密</a>, <a href="rongmi.html">容密</a> and <a href="chenmi.html">辰密</a> are mere renumberings of the pages, columns and rows of a “明密” book, with no arithmetic at all {SRC22}. <b>Our finding.</b> We applied this model to the “X密” telegrams that were still unreadable: pages numbered by a simple rule (backwards, cyclic or zero-free), columns and rows freely permuted, fitted to a language model, under a protocol fixed before computing: synthetic messages of the same length (positive controls) and shuffled digits (negative controls). N09 stands out clearly (score 4.47 against 2.88 for the best control); the text reads, ends with the expected signature 興 and begins with “袁死” (Yuan is dead), which fits its place in the file (6–9 June). The three aberrant groups were re-read twice on the image by Brice Dudout, the second time blind: the digits are sound.',
  legend=BR.T['en']['legend'],
  ctx='Context',
  ctxp=['The form (JACAR B03050089200, PDF 49) is a copy (“Copy”) without date. The sender is Huang Xing’s house in Tokyo, 青山南町三ノ五三; the addressee, in the French concession of Shanghai, on カヒロ (霞飛路, Avenue Joffre), is written ジヨンシヨウ, a Japanese reading of two characters we cannot identify. The inner address, in clear, asks for the message to be passed to “Ma and Geng, my two brothers” (馬, 耿), not identified.',
        'The 乾密 prefix also appears on N03, another telegram sent from the same house in early June; N03 stays unreadable with N09’s key. Both telegrams are filed between those of 3 and 8 June.'],
  whoh='“此間態度未變” (the attitude here has not changed) echoes N13 of 9 June: “日態度頗觀望”, Japan is still waiting and seeing.',
  hist='Historical context', histp=['Yuan Shikai died on 6 June 1916. Huang Xing, then in Tokyo, had for weeks been negotiating arms purchases and loans in Japan for the provinces in revolt (see the <a href="rongmi.html">容密</a> telegrams). N09 gives the state of things just after the news: the Japanese attitude has not moved, and he will wait for the negotiations to take shape before cabling again. A few days later N13 and N17 add that Japan is waiting and will not lend to Beijing until North and South are unified.'],
  srcp=f'Sources: JACAR form <a href="sources.html#s27">[27]</a>; key model: S. Tomokiyo {SRC22}; day codes: <a href="https://archives.sinica.edu.tw/freePage/150/32">Academia Sinica</a>. Decoder and check of the key factorisation: <a href="https://github.com/bdudout/wenmi/tree/main/solver/numeric1916">solver/numeric1916</a>.',
  methodlink='See also the <a href="method.html#qianmi">method</a> and the <a href="chenmi.html">Chenmi</a>, <a href="rongmi.html">Rongmi</a> and <a href="gongmi.html">Gongmi</a> pages.'),
'ja': dict(
  title='乾密——1916年6月の電報1通とその鍵',
  desc='乾密電報N09（黄興、東京、1916年6月）と、S. Tomokiyo氏の着想にもとづいて復元した鍵（番号を付け替えた「明密」電碼本）。',
  kicker='解読・1916年6月', h1='乾密：電報1通とその鍵',
  stand='袁世凱の死の直後に黄興が東京から送った暗号電報。東京の態度は変わらず、交渉の進展を待つという。鍵は番号を付け替えた「明密」電碼本で、S. Tomokiyo氏の着想にしたがって復元した。',
  credits=f'鍵のモデル（番号を付け替えた明密電碼本）の着想：S. Tomokiyo（Cryptiana）{SRC22}。升目の読み順と全数字の再読：Brice Dudout。翻字、鍵の探索、推定読み、翻訳：Claude（Anthropic）。',
  warn='読めた電報は1通のみで、鍵は17組にもとづく。対照・署名・日付の検証は通るが、3字は推定読みであり、同じ差出人の乾密電報N03はこの鍵では読めない（別の鍵か数字の誤り）。翻訳は作業案、人物の比定は候補である。',
  keyh='鍵',
  keyp='用紙は列ごとに右から左、上から下へ読み（Brice Dudoutの提案した順序）、4桁ずつ区切る。最初の6組はあて先で平文（公開の電碼）、続いて公開の前置き<code>0051 1378</code>＝<span lang="zh-Hant">乾密</span>、以下17組が暗号。各組は番号を書き換えた「明密」電碼本の<b>頁＋列＋行</b>として読む：<code>P = 100 × 頁 + 10 × 列 + 行</code>。行は1〜10（10行目は列の最下段のxxx0）。Pは中文電碼（CTC）の番号。',
  pagep='<b>頁</b>（最初の2桁）：書かれた頁から11を引く。11＝00頁、12＝01、…、50＝39など。',
  rows=['読んだ数字', '列', '行'],
  keynote='例：', exh=['組', '頁', '列', '行', 'P', 'CTC'],
  keyhow=f'<b>S. Tomokiyo氏の着想。</b>2026年10月23日、S. Tomokiyo氏は、私たちの<a href="gongmi.html">共密</a>・<a href="rongmi.html">容密</a>・<a href="chenmi.html">辰密</a>の三つの鍵が、計算を伴わない「明密」電碼本の頁・列・行の番号の付け替えにすぎないことを示した{SRC22}。<b>私たちの発見。</b>このモデルを未解読の「X密」電報に適用した：頁は単純な規則（逆順・循環・0なし）で番号づけ、列と行は自由に置換し、言語モデルで当てはめる。計算前に定めた手順で、同じ長さの合成電文（陽性対照）と攪拌した数字（陰性対照）を用いた。N09ははっきり抜きんでて（4.47、最良の対照は2.88）、本文が読め、期待どおり署名「興」で終わり、「袁死」で始まる。これは綴りの中の位置（6月6〜9日）と合う。異常な3組はBrice Dudoutが画像上で2回、2回目は盲検で読み直し、数字は確かである。',
  legend=BR.T['ja']['legend'],
  ctx='背景',
  ctxp=['用紙（JACAR B03050089200、PDF 49）は日付のない写し（「Copy」）。差出人は東京の黄興宅、青山南町三ノ五三。受信人は上海フランス租界カヒロ（霞飛路）の「ジヨンシヨウ」で、二字の日本語読みだが比定できない。本文のあて先は平文で「馬・耿の両兄に転送」とあり、馬・耿は未比定。',
        '乾密の前置きは、6月初めに同じ家から出たN03にも見えるが、N03はN09の鍵では読めない。両電報は綴りの中で6月3日と8日の電報の間に置かれている。'],
  whoh='「此間態度未變」（当地の態度は変わらない）は、6月9日のN13「日態度頗觀望」（日本はなお観望）と呼応する。',
  hist='歴史的背景', histp=['袁世凱は1916年6月6日に死去した。東京にいた黄興は、蜂起した諸省のため日本での武器購入と借款を何週間も交渉していた（<a href="rongmi.html">容密</a>の電報を参照）。N09は知らせ直後の状況を伝える：日本の態度は動かず、交渉がまとまるのを待って改めて打電する。数日後のN13・N17は、日本は観望しており、南北統一までは北京に貸さないと補っている。'],
  srcp=f'出典：JACARの用紙<a href="sources.html#s27">[27]</a>、鍵のモデル：S. Tomokiyo{SRC22}、日付の韻目：<a href="https://archives.sinica.edu.tw/freePage/150/32">中央研究院</a>。解読プログラムと鍵の分解の検証：<a href="https://github.com/bdudout/wenmi/tree/main/solver/numeric1916">solver/numeric1916</a>。',
  methodlink='<a href="method.html#qianmi">方法</a>と<a href="chenmi.html">辰密</a>・<a href="rongmi.html">容密</a>・<a href="gongmi.html">共密</a>のページも参照。'),
'zh-hant': dict(
  title='乾密——1916年6月的一封電報及其密鑰',
  desc='乾密電報N09（黃興，東京，1916年6月）及依S. Tomokiyo的構想復原的密鑰（重新編號的「明密」電碼本）。',
  kicker='破譯·1916年6月', h1='乾密：一封電報及其密鑰',
  stand='袁世凱死後不久，黃興自東京發出的一封密電：此間態度未變，俟交涉有望再電告。密鑰是重新編號的「明密」電碼本，依S. Tomokiyo的構想復原。',
  credits=f'密鑰模型（重新編號的明密電碼本）的構想：S. Tomokiyo（Cryptiana）{SRC22}。方格讀序與全部數字複讀：Brice Dudout。謄錄、密鑰搜尋、推定讀法與翻譯：Claude（Anthropic）。',
  warn='僅讀出一封電報，密鑰建立在17組之上。它通過了對照、署名與日期的檢驗，但有三字為推定讀法；同一發報人的另一封乾密電報N03用此密鑰仍不可讀（另有密鑰或數字有誤）。譯文為工作稿，人物比定為候選。',
  keyh='密鑰',
  keyp='電報紙按列由右至左、由上而下讀取（Brice Dudout 提出的讀序），每四位一組。前六組是收電地址，為明碼（公開電碼）；其次是明文前綴<code>0051 1378</code>＝<span lang="zh-Hant">乾密</span>；以下17組為密文。每組讀作改寫了編號的「明密」電碼本中的<b>頁＋列＋行</b>：<code>P = 100 × 頁 + 10 × 列 + 行</code>，行由1至10（第10行即列底的xxx0）；P為中文電碼的號碼。',
  pagep='<b>頁</b>（前兩位）：所寫頁數減11——11＝第00頁，12＝01，……，50＝39，餘類推。',
  rows=['所讀數字', '列', '行'],
  keynote='示例：', exh=['組', '頁', '列', '行', 'P', 'CTC'],
  keyhow=f'<b>S. Tomokiyo的構想。</b>2026年10月23日，S. Tomokiyo指出我們的<a href="gongmi.html">共密</a>、<a href="rongmi.html">容密</a>、<a href="chenmi.html">辰密</a>三種密鑰，只是「明密」電碼本頁、列、行編號的改寫，毫無計算{SRC22}。<b>我們的發現。</b>我們把這一模型用於尚未讀出的「X密」電報：頁按簡單規則編號（倒數、循環或不含零），列與行自由置換，以語言模型擬合；計算前即定下規程：同長度的合成電文（陽性對照）與打亂的數字（陰性對照）。N09明顯突出（4.47，最佳對照2.88）；全文可讀，以預期的署名「興」作結，以「袁死」開頭，與它在卷宗中的位置（6月6至9日）相符。三個反常的組由Brice Dudout在影像上複讀兩次，第二次為盲讀：數字可靠。',
  legend=BR.T['zh-hant']['legend'],
  ctx='背景',
  ctxp=['電報紙（JACAR B03050089200，PDF第49頁）是無日期的抄件（「Copy」）。發報人是黃興在東京的寓所「青山南町三ノ五三」；收報人在上海法租界カヒロ（霞飛路），名為「ジヨンシヨウ」，是兩個漢字的日語讀音，未能比定。電文內的地址為明碼：「轉馬、耿兩兄」，馬、耿未比定。',
        '乾密前綴亦見於六月初自同一寓所發出的N03；N03用N09的密鑰仍不可讀。兩封電報在卷宗中位於6月3日與8日的電報之間。'],
  whoh='「此間態度未變」與6月9日N13的「日態度頗觀望」相呼應。',
  hist='歷史背景', histp=['袁世凱於1916年6月6日死去。黃興當時在東京，數週來為起義各省在日本洽購軍械、商借款項（見<a href="rongmi.html">容密</a>電報）。N09報告消息傳來後的情形：日本態度未變，俟交涉有望再電告。數日後的N13、N17補充：日本仍在觀望，南北未統一前不借款予北京。'],
  srcp=f'來源：JACAR電報紙<a href="sources.html#s27">[27]</a>；密鑰模型：S. Tomokiyo{SRC22}；韻目代日：<a href="https://archives.sinica.edu.tw/freePage/150/32">中央研究院</a>。解碼程式與密鑰分解的驗證：<a href="https://github.com/bdudout/wenmi/tree/main/solver/numeric1916">solver/numeric1916</a>。',
  methodlink='另見<a href="method.html#qianmi">方法</a>與<a href="chenmi.html">辰密</a>、<a href="rongmi.html">容密</a>、<a href="gongmi.html">共密</a>頁面。'),
}
T['zh-hans'] = {k: (_C.to_hans(v, _T2) if isinstance(v, str) else [_C.to_hans(x, _T2) for x in v] if isinstance(v, list) else v) for k, v in T['zh-hant'].items()}
for k in ('srcp', 'methodlink', 'keyp', 'pagep', 'keyhow', 'credits', 'histp'):   # liens et balises lang="zh-Hant" intacts
    v = T['zh-hant'][k]
    T['zh-hans'][k] = ([_C.to_hans(x, _T2) for x in v] if isinstance(v, list) else _C.to_hans(v, _T2))
T['zh-hans'] = {k: (v.replace('干密', '乾密') if isinstance(v, str) else [x.replace('干密', '乾密') for x in v] if isinstance(v, list) else v) for k, v in T['zh-hans'].items()}   # 乾密 : nom propre
T['zh-hans']['legend'] = BR.T['zh-hans']['legend']
T['zh-hans']['title'] = '乾密——1916年6月的一封电报及其密钥'

def summary(mid, L): return SQ.SUMMARY[L][mid]
def translation(mid, L):
    if L == 'fr': return ' '.join(s['fr'] for s in M[mid]['segments'])
    if L == 'en': return SQ.EN[mid]
    if L == 'ja': return SQ.JA[mid]
    if L == 'zh-hant': return SQ.BAIHUA[mid]
    return _C.to_hans(SQ.BAIHUA[mid], _T2).replace('干密', '乾密')
def date_str(mid, L):
    return {'fr': M[mid]['meta']['date_note'], 'en': 'between 6 and 9 June 1916 (undated “Copy” form)', 'ja': '1916年6月6〜9日（日付のない写し）',
            'zh-hant': '1916年6月6日至9日之間（無日期抄件）', 'zh-hans': '1916年6月6日至9日之间（无日期抄件）'}[L]

def key_tables(L):
    t = T[L]
    tab = (f'<div class="gm-scroll"><table><tr><th>{t["rows"][0]}</th>' + ''.join(f'<td>{d}</td>' for d in range(10)) + '</tr>'
           f'<tr><th>{t["rows"][1]}</th>' + ''.join(f'<td>{v}</td>' for v in K.COL) + '</tr>'
           f'<tr><th>{t["rows"][2]}</th>' + ''.join(f'<td>{v}</td>' for v in K.ROW) + '</tr></table></div>')
    pages = '<div class="gm-scroll"><table><tr>' + ''.join(f'<td><code>{w}</code>→{w - 11:02d}</td>' for w in range(11, 21)) + '<td>…</td><td><code>50</code>→39</td></tr></table></div>'
    ex = (f'<div class="gm-scroll"><table><tr>' + ''.join(f'<th>{h}</th>' for h in t['exh']) + '</tr>' +
          ''.join(f'<tr><td><code>{g}</code></td><td>{g[:2]} → {K.page(g[:2]):02d}</td><td>{g[2]} → {K.COL[int(g[2])]}</td><td>{g[3]} → {K.ROW[int(g[3])]}</td>'
                  f'<td>{K.decode(g):04d}</td><td lang="zh-Hant">{K.glyph(g)}</td></tr>' for g in EX) + '</table></div>')
    return pages, tab, ex

KIND = {'fr': {'clair': 'en clair', 'prefix': 'préfixe'}, 'en': {'clair': 'in clear', 'prefix': 'prefix'}, 'ja': {'clair': '平文', 'prefix': '前置き'},
        'zh-hant': {'clair': '明碼', 'prefix': '前綴'}, 'zh-hans': {'clair': '明码', 'prefix': '前缀'}}
def message_section(mid, L):
    t = T[L]; tb = BR.T[L]; m = M[mid]; segs = m['segments']
    reading = ''.join(s['zh'] for s in segs)
    sep = ' : ' if L == 'fr' else ': '
    nbody = sum(g['kind'] == 'key' for g in m['groups'])
    info = [f'{nbody} {tb["groups"]}', f'{tb["date"]}{sep}{e(date_str(mid, L))}', f'{tb["dirl"]}{sep}{e(tb["dirs"]["TS"])}',
            f'{m["sheet_count"]} {tb["sheets"]}', tb['reread']]
    scans = ''.join(f'<p>{mid}-{n} · {a} PDF {p} {s} · <a href="{JACAR}{a}">JACAR</a> · <a href="{src}">scan</a></p>\n<img loading="lazy" src="{src}" alt="JACAR {a} {mid}-{n}">\n'
                    for n, a, p, s, src in make_images(mid))
    rows = []
    for g in m['groups']:
        idx = KIND[L].get(g['kind'], str(g['i']))
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
    body = [f'<article class="article gongmi rongmi chenmi qianmi"><header class="lede">\n<p class="kicker">{t["kicker"]}</p>\n<h1>{t["h1"]}</h1><p class="standfirst">{t["stand"]}<sup class="fn"><a href="sources.html#s27">[27]</a></sup></p>\n<p>{t["credits"]}</p></header>',
            f'<div class="status warn"><p>{t["warn"]}</p></div>',
            f'<section id="key"><h2>{t["keyh"]}</h2><p>{t["keyp"]}</p><p>{t["pagep"]}</p>{pages}{tab}<p>{t["keynote"]}</p>{ex}<p>{t["keyhow"]}</p><p>{t["legend"]}</p></section>',
            f'<section id="context"><h2>{t["ctx"]}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in t['ctxp']) + f'<p>{e(t["whoh"])}</p></section>',
            f'<section id="history"><h2>{t["hist"]}</h2>' + ''.join(f'<p>{p}</p>' for p in t['histp']) + '</section>']
    body += [message_section(m, L) for m in ORDER]
    if L == 'fr':
        body.append(f'<section id="critical"><h2>{tb["crit"]}</h2><p>{tb["critp"]}</p>' + ''.join(critical_rows(m) for m in ORDER) + '</section>')
    else:
        body.append(f'<section id="critical"><h2>{tb["crit"]}</h2><p>{tb["critp"]} <a href="../fr/qianmi.html#critical">{tb["critlink"]}</a></p></section>')
    body.append(f'<p>{t["srcp"]}</p>\n<p>{t["methodlink"]}</p>\n</article>')
    return head + '\n'.join(body) + '\n'

if __name__ == '__main__':
    json.dump(D, open(os.path.join(SITE, 'data', 'qianmi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for L in LANGS:
        open(os.path.join(SITE, 'content', L, 'qianmi.html'), 'w', encoding='utf-8').write(page(L))
    print('qianmi:', len(ORDER), 'message,', len(os.listdir(IMG)), 'images')
