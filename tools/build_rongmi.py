#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page « 容密 » (content/<langue>/rongmi.html) et bloc N23 de la page « 共密 », dans les cinq langues.

Usage : python3 tools/build_rongmi.py ../wenmi
Lit wenmi/cryptanalysis/c83/site-data.json (export_site.py) et les scans JACAR de wenmi/working/ylc-ocr/png ;
écrit data/rongmi.json, assets/img/rongmi/*.jpg, content/*/rongmi.html et insère/actualise le bloc
<!-- N23:begin --> … <!-- N23:end --> dans content/*/gongmi.html (idempotent). Lancer ensuite tools/build.py."""
import html, json, os, re, sys
from PIL import Image

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))
D = json.load(open(os.path.join(WENMI, 'cryptanalysis/c83/site-data.json'), encoding='utf-8'))
M = D['messages']
LANGS = ['fr', 'en', 'ja', 'zh-hans', 'zh-hant']
ORDER = ['N14', 'N19b', 'N02', 'N08', 'N11', 'N12', 'N19a', 'N28', 'N21', 'N25', 'N36', 'N24']
e = html.escape
JACAR = 'https://www.jacar.archives.go.jp/das/meta/'

# ---------------------------------------------------------------- images
IMG = os.path.join(SITE, 'assets', 'img', 'rongmi')
os.makedirs(IMG, exist_ok=True)
def scan_path(arch, page):
    for name in (f'{arch}-{page:02d}.png', f'{arch}-{page}.png'):
        p = os.path.join(WENMI, 'working', 'ylc-ocr', 'png', name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(arch, page)
def make_images(mid):
    out = []
    for n, (arch, page, side) in enumerate(M[mid]['meta']['sheets'], 1):
        name = f'{mid}-{n}.jpg'
        dst = os.path.join(IMG, name)
        if not os.path.exists(dst):
            im = Image.open(scan_path(arch, page)).convert('L')
            w, h = im.size
            box = (int(w * .47), int(h * .14), int(w * .81), int(h * .89)) if side == 'R' else (int(w * .19), int(h * .14), int(w * .53), int(h * .89))
            c = im.crop(box)
            c = c.resize((760, int(c.height * 760 / c.width)))
            c.save(dst, quality=72, optimize=True)
        out.append((n, arch, page, side, '../assets/img/rongmi/' + name))
    return out

# ---------------------------------------------------------------- textes
T = {
'fr': dict(
  title='容密 — douze télégrammes de juin 1916 et leur clé',
  desc='Édition des douze télégrammes 容密 lisibles (juin 1916, Huang Xing, Zhang Xiaozhun, Zhejiang) et de la clé retrouvée, avec lectures probables signalées.',
  kicker='Déchiffrement · Juin 1916', h1='容密 : douze télégrammes et leur clé',
  stand='Douze télégrammes chiffrés échangés en juin 1916 entre Tokyo et Shanghai, autour de Huang Xing et de Zhang Xiaozhun : achat d’armes au Japon pour le Zhejiang, emprunts, et négociation avec Pékin après la mort de Yuan Shikai. Une seule clé les lit tous.',
  credits='Parcours des grilles : Brice Dudout. Transcription des feuillets de suite, recherche de la clé, traduction et lectures probables : Claude (Anthropic). Relecture de tous les chiffres : Brice Dudout. Modèle de départ (quatre substitutions de chiffres) : essais de Codex.',
  warn='Clé reconstruite, pas retrouvée dans un livre de code historique. Les traductions sont des propositions de travail ; les lectures probables sont distinguées du texte décodé, jamais substituées à lui. Les identifications de personnes sont des candidats, avec leur source.',
  keyh='La clé',
  keyp='Les feuillets se lisent par colonnes, de droite à gauche et de haut en bas (parcours proposé par Brice Dudout), en groupes de quatre chiffres ; le préfixe public <code>1369 1378</code> = <span lang="zh-Hant">容密</span> reste en clair. Pour chaque groupe C : remplacer chaque chiffre selon le tableau de son rang, puis calculer <code>P = (σ(C) + 0901) mod 10000</code> par addition ordinaire avec retenues ; P est le numéro du caractère dans le code télégraphique chinois (CTC).',
  rows=['Chiffre lu', 'milliers', 'centaines', 'dizaines', 'unités'],
  keynote='Aucun groupe ne commence par 00 : le chiffreur écrit 90. Exemple : 2081 → σ = 2081 → 2081 + 0901 = 2982, mais avec les dizaines 8 → 4 et les unités 1 → 8 : σ(2081) = 2048, + 0901 = 2949 = <span lang="zh-Hant">款</span>.',
  keyhow='La clé a été retrouvée sur quatre télégrammes (N02, N08, N11, N12), puis lue sans réajustement sur les huit autres ; réajustée sur l’ensemble relu (590 groupes), elle redonne exactement les mêmes tableaux. Seule la règle « 90 = 00 » a été ajoutée ensuite, d’après tous les groupes en 90xx.',
  legend='Dans la lecture proposée, <b>{x}</b> remplace un caractère décodé anormal par une lecture probable ; la note précise si une variante du groupe chiffré à <b>un seul chiffre près</b> donne ce caractère, ou s’il s’agit d’une <b>lecture de contexte</b>. 〔x〕 : caractère conservé, non résolu.',
  groups='groupes', date='Date', dirl='Sens', sheets='feuillets', reread='chiffres relus par Brice Dudout', notreread='chiffres non encore relus',
  repair='cadrage : un chiffre {k} au feuillet {s} (déduit du décodage, à vérifier sur le scan)', omitted='omis', extra='en trop',
  raw='Décodage brut, sans correction', reading='Lecture proposée', summary='En bref',
  scans='Formulaires et sources JACAR', table='Chiffres et CTC, groupe par groupe', th=['#', 'C', 'CTC', '字', 'Feuillet'], prefix='préfixe',
  crit='Traduction critique alignée', critp='Traduction de travail par segments ; les lacunes et degrés d’incertitude restent visibles.',
  st={'literal': 'Segment lisible, non certifié', 'provisional': 'Interprétation provisoire', 'unresolved': 'Non restitué', 'conjectural': 'Conjecture explicite'},
  ctx='Contexte', ctxp=['Les télégrammes datés vont du 9 au 16 juin 1916, juste après la mort de Yuan Shikai (6 juin). Le Zhejiang, dont le dujun Lü Gongwang est en poste depuis le 6 mai, cherche à acheter des armes au Japon ; Zhang Xiaozhun (字 潤農), à Tokyo avec Huang Xing, mène les négociations (N02, N08, N12, N14) et rend compte à Huang Qun (溯初, N11) et à Jiang Fangzhen (百里, N19a, N28).',
                       'De Shanghai, Yin Ruli, Ge Jing’en et Huang Fu (signature abrégée 驪郛恩) transmettent les questions de Lü Gongwang (N21, N25, N36) et rendent compte à Huang Xing des tractations avec Pékin (N24) : Li Yuanhong invite les personnalités de Shanghai ; Tang Hualong (濟武), Gu Zhongxiu (九峯), Zhang Ji (溥泉) et Fan Yuanlian (靜生) sont pressentis ; on pose comme condition l’abolition des lois de Yuan et le retour à la Constitution provisoire de 1912, rétablie le 29 juin.'],
  srcp='Sources : formulaires JACAR <a href="sources.html#s27">[27]</a> ; noms de courtoisie et fonctions : biographies citées en <a href="sources.html#s28">[28]</a> ; codes de jours : <a href="https://archives.sinica.edu.tw/freePage/150/32">Academia Sinica</a>. Décodeur : <a href="https://github.com/bdudout/wenmi/tree/main/solver/rongmi">solver/rongmi</a>.',
  methodlink='Voir aussi la <a href="method.html#rongmi">méthode</a> et la page <a href="gongmi.html">共密</a>.',
  dirs={'TS': 'Tokyo → Shanghai', 'ST': 'Shanghai → Tokyo'},
  n23h='N23 — Zhang Ji à Huang Xing (13 juin 1916)',
  n23p='Lu après la publication de N17–N18, avec la même clé C51, sur une transcription de Claude relue par Brice Dudout (19 octobre 2026). Un chiffre manque entre les feuillets 2 et 3 (déduit du décodage). Lectures probables entre accolades.',
),
'en': dict(
  title='Rongmi — twelve telegrams of June 1916 and their key',
  desc='Edition of the eleven readable Rongmi (容密) telegrams (June 1916, Huang Xing, Zhang Xiaozhun, Zhejiang) and of the recovered key, with probable readings marked.',
  kicker='Decipherment · June 1916', h1='Rongmi (容密): twelve telegrams and their key',
  stand='Twelve cipher telegrams exchanged in June 1916 between Tokyo and Shanghai around Huang Xing and Zhang Xiaozhun: buying arms in Japan for Zhejiang, loans, and negotiations with Beijing after Yuan Shikai’s death. A single key reads them all.',
  credits='Grid reading order: Brice Dudout. Transcription of the continuation sheets, key recovery, translation and probable readings: Claude (Anthropic). All digits re-read by Brice Dudout. Starting model (four digit substitutions): Codex’s trials.',
  warn='The key is a reconstruction, not taken from a historical code book. Translations are working proposals; probable readings are shown beside the decoded text, never in place of it. Identifications of people are candidates, with their source.',
  keyh='The key',
  keyp='Sheets are read in columns, right to left and top to bottom (reading order proposed by Brice Dudout), in groups of four digits; the public prefix <code>1369 1378</code> = <span lang="zh-Hant">容密</span> stays in clear. For each group C: replace each digit using the table for its place, then compute <code>P = (σ(C) + 0901) mod 10000</code> by ordinary addition with carries; P is the character number in the Chinese Telegraph Code (CTC).',
  rows=['Digit read', 'thousands', 'hundreds', 'tens', 'units'],
  keynote='No group starts with 00: the encipherer writes 90. Example: σ(2081) = 2048 (tens 8 → 4, units 1 → 8), + 0901 = 2949 = <span lang="zh-Hant">款</span>.',
  keyhow='The key was recovered on four telegrams (N02, N08, N11, N12), then read the other seven without refitting; refitted on the whole re-read corpus (590 groups), it returns exactly the same tables. Only the “90 = 00” rule was added afterwards, from all groups beginning 90.',
  legend='In the proposed reading, <b>{x}</b> replaces an anomalous decoded character with a probable reading; the note says whether a variant of the cipher group differing by <b>a single digit</b> gives that character, or whether it is a <b>contextual reading</b>. 〔x〕: character kept, unresolved.',
  groups='groups', date='Date', dirl='Direction', sheets='sheets', reread='digits re-read by Brice Dudout', notreread='digits not yet re-read',
  repair='framing: one digit {k} on sheet {s} (inferred from decoding, to check on the scan)', omitted='missing', extra='too many',
  raw='Raw decoding, uncorrected', reading='Proposed reading', summary='In short',
  scans='Forms and JACAR sources', table='Digits and CTC, group by group', th=['#', 'C', 'CTC', 'Char.', 'Sheet'], prefix='prefix',
  crit='Aligned critical translation', critp='The segment-by-segment working translation is in French.', critlink='See the French aligned translation',
  ctx='Context', ctxp=['The dated telegrams run from 9 to 16 June 1916, just after Yuan Shikai’s death (6 June). Zhejiang, whose military governor Lü Gongwang took office on 6 May, is trying to buy arms in Japan; Zhang Xiaozhun (courtesy name 潤農), in Tokyo with Huang Xing, leads the talks (N02, N08, N12, N14) and reports to Huang Qun (溯初, N11) and Jiang Fangzhen (百里, N19a, N28).',
                       'From Shanghai, Yin Ruli, Ge Jing’en and Huang Fu (abbreviated signature 驪郛恩) relay Lü Gongwang’s questions (N21, N25, N36) and report to Huang Xing on the dealings with Beijing (N24): Li Yuanhong invites the Shanghai notables; Tang Hualong (濟武), Gu Zhongxiu (九峯), Zhang Ji (溥泉) and Fan Yuanlian (靜生) are approached; the condition set is the repeal of Yuan’s laws and a return to the 1912 Provisional Constitution, restored on 29 June.'],
  srcp='Sources: JACAR forms <a href="sources.html#s27">[27]</a>; courtesy names and offices: biographies cited in <a href="sources.html#s28">[28]</a>; day codes: <a href="https://archives.sinica.edu.tw/freePage/150/32">Academia Sinica</a>. Decoder: <a href="https://github.com/bdudout/wenmi/tree/main/solver/rongmi">solver/rongmi</a>.',
  methodlink='See also the <a href="method.html#rongmi">method</a> and the <a href="gongmi.html">Gongmi</a> page.',
  dirs={'TS': 'Tokyo → Shanghai', 'ST': 'Shanghai → Tokyo'},
  n23h='N23 — Zhang Ji to Huang Xing (13 June 1916)',
  n23p='Read after the publication of N17–N18, with the same C51 key, from Claude’s transcription re-read by Brice Dudout (19 October 2026). One digit is missing between sheets 2 and 3 (inferred from decoding). Probable readings in braces.',
),
'ja': dict(
  title='容密——1916年6月の電報12通とその鍵',
  desc='解読できた容密電報12通（1916年6月、黄興・張孝準・浙江）と復元した鍵。推定読みは区別して示す。',
  kicker='解読・1916年6月', h1='容密：電報12通とその鍵',
  stand='1916年6月、黄興と張孝準をめぐって東京と上海の間で交わされた暗号電報12通。浙江のための日本での武器購入、借款、袁世凱の死後の北京との交渉。ひとつの鍵ですべてが読める。',
  credits='升目の読み順：Brice Dudout。続き用紙の翻字、鍵の復元、翻訳と推定読み：Claude（Anthropic）。数字はすべてBrice Dudoutが再読。出発点のモデル（桁ごとの4つの置換）：Codexの試行。',
  warn='鍵は復元であり、歴史的な電碼本から得たものではない。翻訳は作業案であり、推定読みは解読文と並べて示し、置き換えない。人物の比定は出典つきの候補である。',
  keyh='鍵',
  keyp='用紙は列ごとに右から左、上から下へ読み（Brice Dudoutの提案した順序）、4桁ずつ区切る。公開の前置き<code>1369 1378</code>＝<span lang="zh-Hant">容密</span>は平文のまま。各組Cについて、各桁を位ごとの表で置き換え、<code>P = (σ(C) + 0901) mod 10000</code>を通常の繰り上がりつき加算で求める。Pが中文電碼（CTC）の番号である。',
  rows=['読んだ数字', '千の位', '百の位', '十の位', '一の位'],
  keynote='00で始まる組はなく、暗号作成者は90と書く。例：σ(2081) = 2048（十の位8→4、一の位1→8）、+0901 = 2949 = <span lang="zh-Hant">款</span>。',
  keyhow='鍵は4通（N02、N08、N11、N12）で復元し、残り8通は再調整なしで読めた。再読済みの全体（590組）で再調整しても同じ表に戻る。「90＝00」の規則だけは、90で始まるすべての組から後で加えた。',
  legend='推定読みでは<b>{x}</b>が異常な解読字を推定字に置き換える。注に、暗号組を<b>1桁だけ</b>変えるとその字になるか、<b>文脈による読み</b>かを記す。〔x〕：未解決のまま残した字。',
  groups='組', date='日付', dirl='発着', sheets='枚', reread='数字はBrice Dudoutが再読', notreread='数字は未再読',
  repair='区切り：用紙{s}で1桁{k}（解読から推定、スキャンで要確認）', omitted='脱落', extra='過剰',
  raw='未修正の解読結果', reading='推定読み', summary='概要',
  scans='用紙とJACAR出典', table='組ごとの数字とCTC', th=['#', 'C', 'CTC', '字', '用紙'], prefix='前置き',
  crit='対照校訂訳', critp='段落ごとの作業訳はフランス語版にある。', critlink='フランス語の対照訳を見る',
  ctx='背景', ctxp=['日付のある電報は1916年6月9日から16日、袁世凱の死（6月6日）の直後である。5月6日に就任した浙江督軍呂公望は日本で武器を買おうとしており、黄興とともに東京にいる張孝準（字潤農）が交渉にあたり（N02、N08、N12、N14）、黄群（溯初、N11）と蔣方震（百里、N19a、N28）に報告する。',
                     '上海からは殷汝驪・葛敬恩・黄郛（略署名「驪郛恩」）が呂公望の問い合わせを伝え（N21、N25、N36）、北京との交渉を黄興に報告する（N24）。黎元洪は上海の名士を招き、湯化龍（濟武）・谷鍾秀（九峯）・張継（溥泉）・范源濂（靜生）が候補とされ、袁の法令の廃止と1912年の臨時約法への復帰が条件とされた。約法は6月29日に回復される。'],
  srcp='出典：JACARの用紙<a href="sources.html#s27">[27]</a>、字と役職：<a href="sources.html#s28">[28]</a>の伝記、日付の韻目：<a href="https://archives.sinica.edu.tw/freePage/150/32">中央研究院</a>。解読プログラム：<a href="https://github.com/bdudout/wenmi/tree/main/solver/rongmi">solver/rongmi</a>。',
  methodlink='<a href="method.html#rongmi">方法</a>と<a href="gongmi.html">共密</a>のページも参照。',
  dirs={'TS': '東京→上海', 'ST': '上海→東京'},
  n23h='N23——張継から黄興へ（1916年6月13日）',
  n23p='N17・N18の公開後、同じC51の鍵で読んだもの。Claudeの翻字をBrice Dudoutが再読（2026年10月19日）。用紙2と3の間で1桁脱落（解読から推定）。推定読みは波括弧内。',
),
'zh-hans': dict(
  title='容密——1916年6月的十二封电报及其密钥',
  desc='可读的十二封容密电报（1916年6月，黄兴、张孝准、浙江）及复原的密钥，推定读法另行标出。',
  kicker='破译·1916年6月', h1='容密：十二封电报及其密钥',
  stand='1916年6月围绕黄兴与张孝准、在东京与上海之间往来的十二封密电：为浙江在日本购械、借款，以及袁世凯死后与北京的交涉。一把密钥即可读出全部。',
  credits='方格读序：Brice Dudout。续页誊录、密钥复原、翻译与推定读法：Claude（Anthropic）。全部数字由 Brice Dudout 复读。起点模型（逐位四重替换）：Codex 的试验。',
  warn='密钥为复原所得，并非取自历史电码本。译文为工作稿；推定读法与解码文字并列，绝不替代。人物比定为候选，并注明出处。',
  keyh='密钥',
  keyp='电报纸按列由右至左、由上而下读取（Brice Dudout 提出的读序），每四位一组；明文前缀<code>1369 1378</code>＝<span lang="zh-Hant">容密</span>不加密。对每组C：按所在数位的表替换各位数字，再以通常进位加法计算<code>P = (σ(C) + 0901) mod 10000</code>；P即中文电码（CTC）编号。',
  rows=['所读数字', '千位', '百位', '十位', '个位'],
  keynote='没有以00开头的组：发报者写作90。例：σ(2081) = 2048（十位8→4，个位1→8），+0901 = 2949 = <span lang="zh-Hant">款</span>。',
  keyhow='密钥在四封电报（N02、N08、N11、N12）上复原，其余八封无需重新拟合即可读出；以复读后的全部590组重新拟合，所得表格完全相同。仅“90＝00”一条规则是事后根据所有90开头的组补入的。',
  legend='推定读法中，<b>{x}</b>以推定字替换异常的解码字；注中说明暗号组<b>仅改一位数字</b>是否即得该字，或仅为<b>据文意推定</b>。〔x〕：保留未解的字。',
  groups='组', date='日期', dirl='方向', sheets='页', reread='数字经 Brice Dudout 复读', notreread='数字尚未复读',
  repair='分组：第{s}页一位数字{k}（据解码推断，待核对扫描件）', omitted='脱漏', extra='多出',
  raw='未经修正的解码结果', reading='推定读法', summary='提要',
  scans='电报纸与JACAR来源', table='逐组数字与CTC', th=['#', 'C', 'CTC', '字', '页'], prefix='前缀',
  crit='对照校订译文', critp='逐段工作译文见法文版。', critlink='查看法文逐段对照译稿',
  ctx='背景', ctxp=['有日期的电报在1916年6月9日至16日之间，正值袁世凯死后（6月6日）。5月6日就任的浙江督军吕公望欲向日本购械；与黄兴同在东京的张孝准（字润农）负责交涉（N02、N08、N12、N14），并向黄群（溯初，N11）和蒋方震（百里，N19a、N28）报告。',
                      '上海方面，殷汝骊、葛敬恩、黄郛（简署“骊郛恩”）转达吕公望的询问（N21、N25、N36），并向黄兴报告与北京的交涉（N24）：黎元洪邀请沪上名流；汤化龙（济武）、谷钟秀（九峯）、张继（溥泉）、范源濂（静生）被提名；条件是废除袁氏伪法、恢复元年约法。约法于6月29日恢复。'],
  srcp='来源：JACAR电报纸<a href="sources.html#s27">[27]</a>；字号与职务：<a href="sources.html#s28">[28]</a>所引传记；韵目代日：<a href="https://archives.sinica.edu.tw/freePage/150/32">中央研究院</a>。解码程序：<a href="https://github.com/bdudout/wenmi/tree/main/solver/rongmi">solver/rongmi</a>。',
  methodlink='另见<a href="method.html#rongmi">方法</a>与<a href="gongmi.html">共密</a>页面。',
  dirs={'TS': '东京→上海', 'ST': '上海→东京'},
  n23h='N23——张继致黄兴（1916年6月13日）',
  n23p='在N17、N18发表后，以同一C51密钥读出；据Claude誊录、Brice Dudout复读（2026年10月19日）。第2、3页之间脱漏一位数字（据解码推断）。推定读法见花括号。',
),
'zh-hant': dict(
  title='容密——1916年6月的十二封電報及其密鑰',
  desc='可讀的十二封容密電報（1916年6月，黃興、張孝準、浙江）及復原的密鑰，推定讀法另行標出。',
  kicker='破譯·1916年6月', h1='容密：十二封電報及其密鑰',
  stand='1916年6月圍繞黃興與張孝準、在東京與上海之間往來的十二封密電：為浙江在日本購械、借款，以及袁世凱死後與北京的交涉。一把密鑰即可讀出全部。',
  credits='方格讀序：Brice Dudout。續頁謄錄、密鑰復原、翻譯與推定讀法：Claude（Anthropic）。全部數字由 Brice Dudout 複讀。起點模型（逐位四重替換）：Codex 的試驗。',
  warn='密鑰為復原所得，並非取自歷史電碼本。譯文為工作稿；推定讀法與解碼文字並列，絕不替代。人物比定為候選，並注明出處。',
  keyh='密鑰',
  keyp='電報紙按列由右至左、由上而下讀取（Brice Dudout 提出的讀序），每四位一組；明文前綴<code>1369 1378</code>＝<span lang="zh-Hant">容密</span>不加密。對每組C：按所在數位的表替換各位數字，再以通常進位加法計算<code>P = (σ(C) + 0901) mod 10000</code>；P即中文電碼（CTC）編號。',
  rows=['所讀數字', '千位', '百位', '十位', '個位'],
  keynote='沒有以00開頭的組：發報者寫作90。例：σ(2081) = 2048（十位8→4，個位1→8），+0901 = 2949 = <span lang="zh-Hant">款</span>。',
  keyhow='密鑰在四封電報（N02、N08、N11、N12）上復原，其餘八封無需重新擬合即可讀出；以複讀後的全部590組重新擬合，所得表格完全相同。僅「90＝00」一條規則是事後根據所有90開頭的組補入的。',
  legend='推定讀法中，<b>{x}</b>以推定字替換異常的解碼字；注中說明暗號組<b>僅改一位數字</b>是否即得該字，或僅為<b>據文意推定</b>。〔x〕：保留未解的字。',
  groups='組', date='日期', dirl='方向', sheets='頁', reread='數字經 Brice Dudout 複讀', notreread='數字尚未複讀',
  repair='分組：第{s}頁一位數字{k}（據解碼推斷，待核對掃描件）', omitted='脫漏', extra='多出',
  raw='未經修正的解碼結果', reading='推定讀法', summary='提要',
  scans='電報紙與JACAR來源', table='逐組數字與CTC', th=['#', 'C', 'CTC', '字', '頁'], prefix='前綴',
  crit='對照校訂譯文', critp='逐段工作譯文見法文版。', critlink='查看法文逐段對照譯稿',
  ctx='背景', ctxp=['有日期的電報在1916年6月9日至16日之間，正值袁世凱死後（6月6日）。5月6日就任的浙江督軍呂公望欲向日本購械；與黃興同在東京的張孝準（字潤農）負責交涉（N02、N08、N12、N14），並向黃群（溯初，N11）和蔣方震（百里，N19a、N28）報告。',
                      '上海方面，殷汝驪、葛敬恩、黃郛（簡署「驪郛恩」）轉達呂公望的詢問（N21、N25、N36），並向黃興報告與北京的交涉（N24）：黎元洪邀請滬上名流；湯化龍（濟武）、谷鍾秀（九峯）、張繼（溥泉）、范源濂（靜生）被提名；條件是廢除袁氏偽法、恢復元年約法。約法於6月29日恢復。'],
  srcp='來源：JACAR電報紙<a href="sources.html#s27">[27]</a>；字號與職務：<a href="sources.html#s28">[28]</a>所引傳記；韻目代日：<a href="https://archives.sinica.edu.tw/freePage/150/32">中央研究院</a>。解碼程式：<a href="https://github.com/bdudout/wenmi/tree/main/solver/rongmi">solver/rongmi</a>。',
  methodlink='另見<a href="method.html#rongmi">方法</a>與<a href="gongmi.html">共密</a>頁面。',
  dirs={'TS': '東京→上海', 'ST': '上海→東京'},
  n23h='N23——張繼致黃興（1916年6月13日）',
  n23p='在N17、N18發表後，以同一C51密鑰讀出；據Claude謄錄、Brice Dudout複讀（2026年10月19日）。第2、3頁之間脫漏一位數字（據解碼推斷）。推定讀法見花括號。',
),
}
SUMMARY = {
 'en': {'N02': 'Zhang Xiaozhun to the Zhejiang governor: quantities of arms (rifles, mountain guns, machine guns), the Zhejiang and Zhaoqing loans, the wine monopoly.',
        'N08': 'Arms purchase and loan: talks under way, secrecy at customs, ammunition.',
        'N11': 'Zhang Xiaozhun to Huang Qun (溯初): he would like to return to Shanghai but is held in Japan by his business.',
        'N12': 'Arms ready to leave; an intermediary, Yoshikawa, offers a one-million loan; which security to choose.',
        'N14': 'Huang Xing to the Zhejiang governor after Yuan’s death: the arms go first, the one-million loan will follow.',
        'N19a': 'To Jiang Fangzhen (百里): asks that a Mr Guan come to Japan.',
        'N28': 'To Jiang Fangzhen: three hundred raised through Yongyi.',
        'N21': 'Lü Gongwang’s questions, relayed from Shanghai, on the models and quantities of arms and ammunition.',
        'N25': 'The securities offered by Zhejiang (tobacco and wine taxes); Wu Zhaolian sent to Japan.',
        'N36': 'Lü Gongwang to Huang Xing and Zhang Xiaozhun: ship the arms quickly, payment before 30 June.',
        'N24': 'Report from Shanghai to Huang Xing: conditions set to Beijing (repeal of Yuan’s laws, 1912 Constitution), Tang Hualong’s departure.',
        'N23': 'Zhang Ji to Huang Xing: Tanaka and Koike have cabled Aoki; go and press the loan.'},
 'ja': {'N02': '張孝準から浙江督軍へ：武器の数量（小銃・山砲・機関銃）、浙江と肇慶の借款、酒公売。',
        'N08': '武器購入と借款：交渉中、税関での秘密保持、弾薬。',
        'N11': '張孝準から黄群（溯初）へ：上海に戻りたいが日本での用務に引き止められている。',
        'N12': '武器は発送準備済み。仲介者芳川が百万の借款を申し出る。担保をどれにするか。',
        'N14': '袁の死後、黄興から浙江督軍へ：武器を先に送り、百万の借款も続く。',
        'N19a': '蔣方震（百里）へ：官某の来日を望む。',
        'N28': '蔣方震へ：詠儀を通じて三百を用意。',
        'N21': '上海から転送された呂公望の問い合わせ：武器と弾薬の型式と数量。',
        'N25': '浙江が示す担保（煙税・酒税）、呉兆蓮の日本派遣。',
        'N36': '呂公望から黄興・張孝準へ：武器を急いで送れ、代金は6月30日までに。',
        'N24': '上海から黄興への報告：北京への条件（袁の法令廃止、1912年約法）、湯化龍の上京。',
        'N23': '張継から黄興へ：田中と小池が青木に打電、借款の催促に行かれたい。'},
 'zh-hans': {'N02': '张孝准致浙江督军：械数（步枪、山炮、机枪）、浙江与肇庆借款、酒公卖。',
        'N08': '购械与借款：交涉中，海关保密，子弹。',
        'N11': '张孝准致黄群（溯初）：欲回沪，惟因在日事务未了。',
        'N12': '械已备运；经手人芳川愿借款百万；抵押品如何选择。',
        'N14': '袁死后黄兴致浙江督军：械先运，百万借款随后可成。',
        'N19a': '致蒋方震（百里）：盼官君来日一商。',
        'N28': '致蒋方震：已电咏仪筹三百。',
        'N21': '自上海转来吕公望的询问：枪械弹药的型式与数量。',
        'N25': '浙江所拟抵押品（烟捐、酒捐）；派吴兆莲赴日。',
        'N36': '吕公望致黄兴、张孝准：械速运，代价六月三十日前付清。',
        'N24': '上海向黄兴的报告：对北京的条件（取消袁氏伪法、恢复元年约法），汤化龙赴京。',
        'N23': '张继致黄兴：田中、小池皆有电至青木，请亲往催促借款。'},
 'zh-hant': {'N02': '張孝準致浙江督軍：械數（步槍、山砲、機槍）、浙江與肇慶借款、酒公賣。',
        'N08': '購械與借款：交涉中，海關保密，子彈。',
        'N11': '張孝準致黃群（溯初）：欲回滬，惟因在日事務未了。',
        'N12': '械已備運；經手人芳川願借款百萬；抵押品如何選擇。',
        'N14': '袁死後黃興致浙江督軍：械先運，百萬借款隨後可成。',
        'N19a': '致蔣方震（百里）：盼官君來日一商。',
        'N28': '致蔣方震：已電詠儀籌三百。',
        'N21': '自上海轉來呂公望的詢問：槍械彈藥的型式與數量。',
        'N25': '浙江所擬抵押品（煙捐、酒捐）；派吳兆蓮赴日。',
        'N36': '呂公望致黃興、張孝準：械速運，代價六月三十日前付清。',
        'N24': '上海向黃興的報告：對北京的條件（取消袁氏偽法、恢復元年約法），湯化龍赴京。',
        'N23': '張繼致黃興：田中、小池皆有電至青木，請親往催促借款。'},
}
SUMMARY['en'].update({'N17': 'Huang Xing to Shanghai after Li Yuanhong took office: five measures (Constitution and Parliament, Duan’s resignation, governors, consulting the South); Japan will not lend to Beijing without unification.',
 'N18': 'Reply to the telegram of the 10th: the Republic first, armed force as support; the return to China will wait.',
 'N27': 'Huang Xing: the matter of Puquan’s (Zhang Ji’s) funds is hopeless.',
 'N30': 'Huang Xing: according to Koike, Zhang Ji could obtain a small loan in his own name through Consul Ariyoshi.',
 'N32': 'From Shanghai: the Constitution will probably be restored; caution about Sun Yat-sen’s published reply; signed Ge, Yin, Huang.',
 'N33': 'From Shanghai: Beijing’s manoeuvres over the Constitution, Huang Qun in Beijing; the Shanghai parliamentarians object; wait and see.',
 'N35': 'Huang Xing: Beijing wants provincial delegates to revise the Constitution; Parliament should meet in a safe place; beware of Duan.'})
SUMMARY['ja'].update({'N17': '黎元洪の就任後、黄興から上海へ：五つの方策（約法と国会、段の辞職、督軍、南方との協議）。日本は統一なしには北京に借款しない。',
 'N18': '10日の電報への返電：まず共和、武力の後ろ盾。帰国は後で決める。',
 'N27': '黄興：溥泉（張継）の資金の件は望みがない。',
 'N30': '黄興：小池によれば、張継は有吉領事の紹介で個人名義の小口借款を得られる。',
 'N32': '上海から：約法は回復の見込み。孫文の公表された返電に注意。署名は葛・殷・黄。',
 'N33': '上海から：約法をめぐる北京の策動、黄群の上京。上海の議員は反対。静観を。',
 'N35': '黄興：北京は各省代表に約法を改めさせようとしている。国会は安全な場所で開くべき。段に警戒。'})
SUMMARY['zh-hant'].update({'N17': '黎元洪就任後黃興致上海：五項主張（約法與國會、段辭職、都督、南方協商）；日本非南北統一不借款於北京。',
 'N18': '覆十日電：擁護共和，須有武力後援；歸國事再決。',
 'N27': '黃興：溥泉（張繼）款事無望。',
 'N30': '黃興：據小池云，張繼以個人名義請有吉領事紹介，可借小款。',
 'N32': '上海來電：舊約法可望恢復；孫中山覆電已登報，宜慎；葛、殷、黃署名。',
 'N33': '上海來電：北京於約法之策動，黃群到京；滬議員反對；暫靜觀。',
 'N35': '黃興：北京欲召各省代表議約法；國會宜擇安全地自行開會；段有襲袁故智之勢。'})
SUMMARY['zh-hans'].update({'N17': '黎元洪就任后黄兴致上海：五项主张（约法与国会、段辞职、都督、南方协商）；日本非南北统一不借款于北京。',
 'N18': '复十日电：拥护共和，须有武力后援；归国事再决。',
 'N27': '黄兴：溥泉（张继）款事无望。',
 'N30': '黄兴：据小池云，张继以个人名义请有吉领事绍介，可借小款。',
 'N32': '上海来电：旧约法可望恢复；孙中山复电已登报，宜慎；葛、殷、黄署名。',
 'N33': '上海来电：北京于约法之策动，黄群到京；沪议员反对；暂静观。',
 'N35': '黄兴：北京欲召各省代表议约法；国会宜择安全地自行开会；段有袭袁故智之势。'})

SUMMARY['en']['N19b']='Huang Xing to the Shanghai senders (reply to the 8th and 9th): yes to the 1912 Constitution and Parliament, but nothing without armed force; Zhejiang must be the pillar of the South-East; Lu Rongting and Li Liejun should march on Hubei and Jiangxi; Japan will not lend to Beijing before unification.'
SUMMARY['ja']['N19b']='黄興から上海の発信者へ（8日・9日電への返電）：約法と国会の回復に賛成、ただし武力なしには無効。浙江は東南の砥柱たれ。陸栄廷・李烈鈞は鄂・贛に出兵を。日本は統一まで北京に借款しない。'
SUMMARY['zh-hant']['N19b']='黃興覆滬上諸君（齊、佳兩電）：贊成恢復約法與國會，惟非有武力後援必無効果；浙省宜作東南砥柱；陸榮廷、李烈鈞速出鄂贛；日本非南北統一不借款於北京。'
SUMMARY['zh-hans']['N19b']='黄兴复沪上诸君（齐、佳两电）：赞成恢复约法与国会，惟非有武力后援必无効果；浙省宜作东南砥柱；陆荣廷、李烈钧速出鄂赣；日本非南北统一不借款于北京。'
UNREAD = {'fr': 'date non lue', 'en': 'date not read', 'ja': '日付未読', 'zh-hans': '日期未读', 'zh-hant': '日期未讀'}
def date_str(mid, L):
    m = M[mid]['meta']
    if L == 'fr':
        return m['date_note']
    d = m['date']
    special = {'N11': 8, 'N12': 8}
    if mid in special:
        return {'en': 'day 8 (庚); month not read', 'ja': '8日（庚）、月は未読', 'zh-hans': '8日（庚），月份未读', 'zh-hant': '8日（庚），月份未讀'}[L]
    if mid == 'N24':
        return {'en': 'header not read; after 9 June', 'ja': '見出し未読、6月9日以降', 'zh-hans': '电头未读；6月9日之后', 'zh-hant': '電頭未讀；6月9日之後'}[L]
    if mid in ('N19a', 'N25'):
        dd = 11 if mid == 'N19a' else 14
        return {'en': f'June {dd}, 1916 ? (inventory)', 'ja': f'1916年6月{dd}日？（目録）', 'zh-hans': f'1916年6月{dd}日？（目录）', 'zh-hant': f'1916年6月{dd}日？（目錄）'}[L]
    if d is None:
        return UNREAD[L]
    return {'en': f'June {d}, 1916', 'ja': f'1916年6月{d}日', 'zh-hans': f'1916年6月{d}日', 'zh-hant': f'1916年6月{d}日'}[L]
def direction(mid, L):
    return T[L]['dirs']['TS' if M[mid]['meta']['dir'].startswith('Tokyo') else 'ST']
def summary(mid, L):
    return M[mid]['summary_fr'] if L == 'fr' else SUMMARY[L][mid]

def key_table(L):
    t = T[L]; s = D['key_rongmi']['sigma']
    rows = ''.join(f'<tr><th>{t["rows"][j + 1]}</th>' + ''.join(f'<td>{v}</td>' for v in s[j]) + '</tr>' for j in range(4))
    return f'<div class="gm-scroll"><table><tr><th>{t["rows"][0]}</th>' + ''.join(f'<td>{d}</td>' for d in range(10)) + f'</tr>{rows}</table></div>'

sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c84'))
import tr_i18n as TRX                                 # noqa: E402
TLABEL = {'fr': 'Traduction', 'en': 'Translation', 'ja': '日本語訳', 'zh-hans': '今译（推定读法加标点）', 'zh-hant': '今譯（推定讀法加標點）'}
def translation(mid, L):
    if L == 'fr':
        segs = M[mid]['segments'] if mid in M else [dict(fr=x[3]) for x in __import__('segments_gongmi').SEG[mid]]
        return ' '.join(x['fr'] for x in segs)
    if L == 'en': return TRX.EN.get(mid, '')
    if L == 'ja': return TRX.JA.get(mid, '')
    return ''

def message_section(mid, L, h2=None):
    t = T[L]; m = M[mid]; segs = m['segments']
    reading = ''.join(s['zh'] for s in segs)
    info = [f'{len(m["groups"]) - 2} {t["groups"]}', f'{t["date"]} : {e(date_str(mid, L))}' if L == 'fr' else f'{t["date"]}: {e(date_str(mid, L))}',
            f'{t["dirl"]} : {e(direction(mid, L))}' if L == 'fr' else f'{t["dirl"]}: {e(direction(mid, L))}',
            f'{m["sheet_count"]} {t["sheets"]}', t['reread'] if m['reread_by_brice'] else f'<mark class="unc">{t["notreread"]}</mark>']
    reps = []
    for kind, pos in m['repairs']:
        k = min(pos // 4, len(m['groups']) - 1)
        reps.append(t['repair'].format(k=t['omitted'] if kind == 'ins' else t['extra'], s=m['groups'][k]['sheet']))
    scans = ''.join(f'<p>{mid}-{n} · {a} PDF {p} {s} · <a href="{JACAR}{a}">JACAR</a> · <a href="{src}">scan</a></p>\n<img loading="lazy" src="{src}" alt="JACAR {a} {mid}-{n}">\n'
                    for n, a, p, s, src in make_images(mid))
    rows = []
    for g in m['groups']:
        idx = t['prefix'] if g is m['groups'][0] or g is m['groups'][1] else str(g['i'])
        rows.append(f'<tr><td>{idx}</td><td><code>{e(g["cipher"])}</code></td><td><code>{g["ctc"] or "—"}</code></td><td lang="zh-Hant">{e(g["glyph"])}</td><td>{mid}-{g["sheet"]}</td></tr>')
    return (f'<section id="{mid}" class="gm-message"><h2>{e(h2 or mid)}</h2>\n<p>{" · ".join(info)}</p>\n'
            + (f'<p><mark class="unc">{" ; ".join(e(r) for r in reps)}</mark></p>\n' if reps else '')
            + f'<p>{e(summary(mid, L))}</p>\n'
            f'<h3>{t["raw"]}</h3><p class="gm-han" lang="zh-Hant">{e(m["raw"])}</p>\n'
            f'<h3>{t["reading"]}</h3><p class="gm-han" lang="zh-Hant">{e(reading)}</p>\n'
            + (f'<h3>{TLABEL[L]}</h3><p class="gm-tr">{e(translation(mid, L))}</p>\n' if translation(mid, L) else '')
            + ''
            f'<details><summary>{t["scans"]}</summary>\n{scans}</details>'
            f'<details><summary>{t["table"]}</summary>\n<div class="gm-scroll"><table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in t['th']) + '</tr></thead><tbody>\n'
            + '\n'.join(rows) + '\n</tbody></table></div></details></section>\n')

def critical_rows(mid):
    t = T['fr']; out = []
    for s in M[mid]['segments']:
        note = f'<p>{e(s["note"])}</p>' if s['note'] else ''
        out.append(f'<tr class="gm-{s["status"]}"><td class="gm-cell-han" lang="zh-Hant">{e(s["zh"])}</td><td>{e(s["fr"])}<small class="gm-status">{t["st"][s["status"]]}</small>{note}</td></tr>')
    return f'<h3 id="crit-{mid}">{mid}</h3><div class="gm-scroll"><table><thead><tr><th>Lecture proposée</th><th>Traduction</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>'

def page(L):
    t = T[L]
    head = f'<!-- {json.dumps(dict(title=t["title"], description=t["desc"]), ensure_ascii=False)} -->\n<link rel="stylesheet" href="../assets/css/gongmi.css">\n'
    body = [f'<article class="article gongmi rongmi"><header class="lede">\n<p class="kicker">{t["kicker"]}</p>\n<h1>{t["h1"]}</h1><p class="standfirst">{t["stand"]}<sup class="fn"><a href="sources.html#s27">[27]</a></sup></p>\n<p>{t["credits"]}</p></header>',
            f'<div class="status warn"><p>{t["warn"]}</p></div>',
            f'<section id="key"><h2>{t["keyh"]}</h2><p>{t["keyp"]}</p>{key_table(L)}<p>{t["keynote"]}</p><p>{t["keyhow"]}</p><p>{t["legend"]}</p></section>',
            f'<section id="context"><h2>{t["ctx"]}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in t['ctxp']) + '</section>',
            '<nav class="gm-nav" aria-label="Messages">' + ''.join(f'<a href="#{m}">{m}</a>' for m in ORDER) + '</nav>']
    body += [message_section(m, L) for m in ORDER]
    if L == 'fr':
        body.append(f'<section id="critical"><h2>{t["crit"]}</h2><p>{t["critp"]}</p>' + ''.join(critical_rows(m) for m in ORDER) + '</section>')
    else:
        body.append(f'<section id="critical"><h2>{t["crit"]}</h2><p>{t["critp"]} <a href="../fr/rongmi.html#critical">{t["critlink"]}</a></p></section>')
    body.append(f'<p>{t["srcp"]}</p>\n<p>{t["methodlink"]}</p>\n</article>')
    return head + '\n'.join(body) + '\n'

def n23_block(L):
    t = T[L]
    inner = message_section('N23', L, h2=t['n23h']).replace('<section id="N23" class="gm-message">', '<section id="N23" class="gm-message">', 1)
    inner = inner.replace(f'<h2>{e(t["n23h"])}</h2>\n', f'<h2>{e(t["n23h"])}</h2>\n<p>{t["n23p"]}</p>\n', 1)
    crit = critical_rows('N23') if L == 'fr' else ''
    return f'<!-- N23:begin -->\n{inner}{crit}\n<!-- N23:end -->\n'

def insert_n23(L):
    p = os.path.join(SITE, 'content', L, 'gongmi.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!-- N23:begin -->.*?<!-- N23:end -->\n', '', s, flags=re.S)
    anchor = '<section id="critical">' if L == 'fr' else None
    blk = n23_block(L)
    if anchor and anchor in s:
        s = s.replace(anchor, blk + anchor, 1)
    else:  # avant le paragraphe des sources (dernier <p>Sources… / équivalent) : juste avant </article>
        i = s.rfind('<p>', 0, s.rfind('</article>'))
        i = s.rfind('<p>', 0, i)
        s = s[:i] + blk + s[i:]
    s = s.replace('<nav class="gm-nav" aria-label="Messages"><a href="#N17">N17</a><a href="#N18">N18</a></nav>',
                  '<nav class="gm-nav" aria-label="Messages"><a href="#N17">N17</a><a href="#N18">N18</a><a href="#N23">N23</a></nav>')
    open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- 共密 : six autres télégrammes et lectures probables (C84)
GM_EXTRA = ['N23', 'N27', 'N30', 'N32', 'N33', 'N35']
GM_HEAD = {
 'fr': ('共密 — huit télégrammes de juin 1916, une clé candidate', 'Édition critique partielle des télégrammes 共密 N17, N18, N23, N27, N30, N32, N33 et N35 sous la clé C51, avec lectures probables signalées.',
        'Édition critique partielle de huit télégrammes',
        'Huit télégrammes de juin 1916 (Huang Xing, Zhang Ji et le groupe de Shanghai) se lisent, au moins en partie, avec la clé candidate C51 ; N07 reste illisible. Les caractères incertains restent signalés.',
        'Six télégrammes de plus et lectures probables (octobre 2026)',
        'Après la publication de N17 et N18, les corps de N23, N27, N30, N32, N33 et N35 ont été rassemblés (transcriptions de Codex et de Claude, toutes relues par Brice Dudout le 19 octobre 2026, sans voir le déchiffrement). Les vérifications de contexte les relient au dossier 容密 : 溥 = 溥泉 (Zhang Ji) dans N27 et N30, qui reprend le « 以個人名義 » de N24 ; N32 est signé 葛、殷、黃 (Ge Jing’en, Yin Ruli, Huang Fu). N35 écrit 8 là où les autres télégrammes 共密 écrivent 3 pour les mêmes mots (表 3007, 袁 3087). La relecture a confirmé six lectures probables à un chiffre près (呂, 請, 咸, 張, 黃, 各) et restitué la signature 興 de N35 (lue 議 auparavant). Les lectures probables suivent la même convention que la page <a href="rongmi.html">容密</a>.',
        'Lectures probables pour N17 et N18', ['Brut', 'Lecture probable', 'Appui']),
 'en': ('Gongmi — eight telegrams from June 1916, a candidate key', 'A partial critical edition of Gongmi telegrams N17, N18, N23, N27, N30, N32, N33 and N35 under key C51, with probable readings marked.',
        'A partial critical edition of eight telegrams',
        'Eight telegrams of June 1916 (Huang Xing, Zhang Ji and the Shanghai group) can be read, at least in part, with candidate key C51; N07 remains unread. Uncertain characters remain marked.',
        'Six more telegrams and probable readings (October 2026)',
        'After N17 and N18 were published, the bodies of N23, N27, N30, N32, N33 and N35 were assembled (transcriptions by Codex and Claude, all re-read by Brice Dudout on 19 October 2026 without seeing the decipherment). Context checks tie them to the Rongmi file: 溥 = Puquan (Zhang Ji) in N27 and N30, echoing N24’s “in his personal capacity”; N32 is signed 葛、殷、黃 (Ge Jing’en, Yin Ruli, Huang Fu). N35 writes 8 where the other Gongmi telegrams write 3 for the same words (表 3007, 袁 3087). The re-reading confirmed six single-digit probable readings (呂, 請, 咸, 張, 黃, 各) and restored N35’s signature 興 (previously read 議). Probable readings follow the convention of the <a href="rongmi.html">Rongmi</a> page.',
        'Probable readings for N17 and N18', ['Raw', 'Probable reading', 'Support']),
 'ja': ('共密 — 1916年6月の電報8通と候補の鍵', '候補の鍵C51による共密電報N17・N18・N23・N27・N30・N32・N33・N35の部分校訂版。推定読みを明示する。',
        '1916年6月の電報8通 — 部分校訂版',
        '1916年6月の電報8通（黄興、張継、上海のグループ）が候補の鍵C51で少なくとも部分的に読める。N07は未解読。不確かな字は明示する。',
        'さらに6通と推定読み（2026年10月）',
        'N17・N18の公開後、N23・N27・N30・N32・N33・N35の本文をまとめた（CodexとClaudeの翻字を、2026年10月19日にBrice Dudoutが解読結果を見ずにすべて再読）。文脈の確認で容密の資料と結びつく：N27・N30の「溥」は溥泉（張継）で、N24の「以個人名義」と一致する。N32の署名は葛・殷・黄（葛敬恩・殷汝驪・黄郛）。N35は同じ語（表3007、袁3087）について、他の共密電報が3と書くところを8と書く。推定読みは<a href="rongmi.html">容密</a>のページと同じ表記。',
        'N17・N18の推定読み', ['原文', '推定読み', '根拠']),
 'zh-hans': ('共密——1916年6月的八封电报与候选密钥', '采用候选密钥C51对共密电报N17、N18、N23、N27、N30、N32、N33、N35进行部分校勘，推定读法另行标出。',
        '1916年6月的八封电报——部分校勘版',
        '1916年6月的八封电报（黄兴、张继及上海方面）可用候选密钥C51至少部分读出；N07仍未解。不确定的字均予标明。',
        '另外六封电报与推定读法（2026年10月）',
        'N17、N18发表后，又整理出N23、N27、N30、N32、N33、N35的正文（Codex 与 Claude 的誊录均于2026年10月19日经 Brice Dudout 在未见译文的情况下复读）。经背景核对，它们与容密档案相关联：N27、N30中的“溥”即溥泉（张继），与N24的“以个人名义”相合；N32署名葛、殷、黄（葛敬恩、殷汝骊、黄郛）。N35在相同的字（表3007、袁3087）上写8，其他共密电报写3。推定读法的标示与<a href="rongmi.html">容密</a>页面相同。',
        'N17与N18的推定读法', ['原文', '推定读法', '依据']),
 'zh-hant': ('共密——1916年6月的八封電報與候選密鑰', '採用候選密鑰C51對共密電報N17、N18、N23、N27、N30、N32、N33、N35進行部分校勘，推定讀法另行標出。',
        '1916年6月的八封電報——部分校勘版',
        '1916年6月的八封電報（黃興、張繼及上海方面）可用候選密鑰C51至少部分讀出；N07仍未解。不確定的字均予標明。',
        '另外六封電報與推定讀法（2026年10月）',
        'N17、N18發表後，又整理出N23、N27、N30、N32、N33、N35的正文（Codex 與 Claude 的謄錄均於2026年10月19日經 Brice Dudout 在未見譯文的情況下複讀）。經背景核對，它們與容密檔案相關聯：N27、N30中的「溥」即溥泉（張繼），與N24的「以個人名義」相合；N32署名葛、殷、黃（葛敬恩、殷汝驪、黃郛）。N35在相同的字（表3007、袁3087）上寫8，其他共密電報寫3。推定讀法的標示與<a href="rongmi.html">容密</a>頁面相同。',
        'N17與N18的推定讀法', ['原文', '推定讀法', '依據']),
}
SUPPORT = {'fr': ('1 chiffre', 'contexte'), 'en': ('1 digit', 'context'), 'ja': ('1桁', '文脈'), 'zh-hans': ('一位数字', '文意'), 'zh-hant': ('一位數字', '文意')}

def gongmi_block(L):
    title, desc, h1, stand, h2, intro, h3, th = GM_HEAD[L]
    rows = []
    for mid in ('N17', 'N18'):
        for s in M[mid]['segments']:
            for mm in re.finditer(r'\{([^}]*)\}', s['zh']):
                sup = SUPPORT[L][0] if '1 chiffre' in s['note'] else SUPPORT[L][1]
                rows.append(f'<tr><td>{mid}</td><td lang="zh-Hant">{e(s["raw"])}</td><td lang="zh-Hant">{e(mm.group(1))}</td><td>{sup}</td></tr>')
    table = f'<h3>{h3}</h3><div class="gm-scroll"><table><thead><tr><th>#</th><th>{th[0]}</th><th>{th[1]}</th><th>{th[2]}</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
    secs = ''.join(message_section(m, L, h2=(T[L]['n23h'] if m == 'N23' else None)) for m in GM_EXTRA)
    crit = ''.join(critical_rows(m) for m in GM_EXTRA + ['N17', 'N18']) if L == 'fr' else ''
    return f'<!-- C84:begin -->\n<section id="c84"><h2>{h2}</h2><p>{intro}</p>{table}</section>\n{secs}{crit}\n<!-- C84:end -->\n'

def update_gongmi(L):
    p = os.path.join(SITE, 'content', L, 'gongmi.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!-- TR:begin -->.*?<!-- TR:end -->', '', s, flags=re.S)
    for mid in ('N17', 'N18'):
        tr = translation(mid, L)
        if not tr: continue
        i = s.find(f'<section id="{mid}" class="gm-message">')
        if i < 0: continue
        j = s.find('</p>', s.find('class="gm-han"', i)) + 4
        s = s[:j] + f'<!-- TR:begin --><h3>{TLABEL[L]}</h3><p class="gm-tr">{e(tr)}</p><!-- TR:end -->' + s[j:]
    s = re.sub(r'<!-- (N23|C84):begin -->.*?<!-- \1:end -->\n', '', s, flags=re.S)
    title, desc, h1, stand, *_ = GM_HEAD[L]
    s = re.sub(r'^<!-- \{.*?\} -->', '<!-- ' + json.dumps(dict(title=title, description=desc), ensure_ascii=False) + ' -->', s, count=1)
    s = re.sub(r'<h1>.*?</h1><p class="standfirst">.*?<sup', f'<h1>{h1}</h1><p class="standfirst">{stand}<sup', s, count=1, flags=re.S)
    blk = gongmi_block(L)
    anchor = '<section id="critical">'
    if L == 'fr' and anchor in s:
        s = s.replace(anchor, blk + anchor, 1)
    else:
        i = s.rfind('<p>', 0, s.rfind('</article>')); i = s.rfind('<p>', 0, i)
        s = s[:i] + blk + s[i:]
    s = re.sub(r'<nav class="gm-nav" aria-label="Messages">.*?</nav>',
               '<nav class="gm-nav" aria-label="Messages">' + ''.join(f'<a href="#{m}">{m}</a>' for m in ['N17', 'N18'] + GM_EXTRA) + '<a href="#c84">+</a></nav>', s, count=1)
    open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    json.dump(D, open(os.path.join(SITE, 'data', 'rongmi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for L in LANGS:
        open(os.path.join(SITE, 'content', L, 'rongmi.html'), 'w', encoding='utf-8').write(page(L))
        update_gongmi(L)
    print('rongmi:', len(ORDER), 'messages,', len(os.listdir(IMG)), 'images ; 共密 mis à jour (5 langues)')


