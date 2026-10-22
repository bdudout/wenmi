#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bloc « lecture 明密 » (reformulation de S. Tomokiyo, Cryptiana, 23/10/2026) dans les pages 共密, 容密 et 辰密,
cinq langues. Insère ou actualise <!-- MINGMI:begin --> … <!-- MINGMI:end --> (idempotent) :
共密 avant <section id="N17">, 容密 et 辰密 avant <section id="context">. Les tables viennent de
solver/numeric1916/mingmi.py (factorisation vérifiée des clés publiées).
À relancer après tools/build_rongmi.py et tools/build_chenmi.py (qui réécrivent ces pages), puis tools/build.py."""
import html, os, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SITE, 'solver', 'numeric1916'))
import common as C        # noqa: E402
import mingmi as M        # noqa: E402

LANGS = ('fr', 'en', 'ja', 'zh-hans', 'zh-hant')
DEC = {'gongmi': C.decode_gongmi, 'rongmi': C.decode_rongmi, 'chenmi': C.decode_chenmi}
ANCHOR = {'gongmi': '<section id="N17"', 'rongmi': '<section id="context">', 'chenmi': '<section id="context">'}
SRC = '<sup class="fn"><a href="sources.html#s22">[22]</a></sup>'
CODE = 'https://github.com/bdudout/wenmi/blob/main/solver/numeric1916/mingmi.py'
URL = 'https://cryptiana.web.fc2.com/code/chinesecrypto_e2.htm'

T = {
 'fr': dict(
  h2='Une autre lecture de la clé : un livre 明密 renuméroté (S. Tomokiyo)',
  credit=f'<b>Cette interprétation est due à S. Tomokiyo</b> (<a href="{URL}">Cryptiana</a>, 23 octobre 2026){SRC}. '
         'Il propose que l’employé n’ait fait aucun calcul : il disposait d’un exemplaire du code « 明密 » dont les numéros de '
         'pages, de colonnes et de lignes avaient été réécrits à la main pour l’usage secret (密) ; il a illustré chaque clé sur '
         'une édition de juin 1916 du 明密碼電報書 qu’il possède. Nos formules décrivent donc la même table par le calcul.',
  check='Contrôle : pour les 10 000 valeurs de groupe, la clé publiée se décompose exactement en page (deux premiers '
        'chiffres), colonne (dizaine) et ligne (unité), sans retenue résiduelle (<a href="' + CODE + '">mingmi.py</a>). '
        'Dans le livre, chaque colonne contient xxx1 à xxx9 puis, en bas, xxx0 : c’est ce que nos « retenues » traduisaient.',
  digit='Chiffre écrit', col='colonne', row='ligne (1–10)',
  gongmi='Pages numérotées à rebours : page écrite 89 = page 00, 88 = 01, …, 01 = 88 (89 − n). Les dizaines donnent la '
         'colonne, les unités la ligne comptée depuis le bas. La soustraction de 9000 de notre formule n’est que ce double '
         'comptage à rebours.',
  rongmi='Pages numérotées en boucle à partir de la page 10 : page écrite 01 = 10, 02 = 11, …, 79 = 88, puis 81 = 00, …, '
         '90 = 09. Le « + 0901 » de notre formule est ce décalage de pages et le passage d’une ligne. '
         'Seule différence : la page écrite 80, qui vaut 89 selon S. Tomokiyo et 99 selon notre formule. Le seul groupe '
         'concerné, 8012 (N25), ne se lisait ni dans un cas (9911, hors table) ni dans l’autre (8911 窔) ; '
         'S. Tomokiyo l’avait relevé. Avec deux chiffres voisins échangés, 8102 donne 一, d’où « 一切到乞賜教 » : la lecture '
         'de N25 est corrigée en ce sens. La numérotation en boucle de S. Tomokiyo, plus simple, est la plus probable.',
  chenmi='Notre clé était déjà une renumérotation (pages comptées à rebours sur les nombres sans zéro) ; S. Tomokiyo la '
         'montre directement sur une page du livre. L’unité 9 qui « vaut 10 » est la ligne du bas, xxx0.',
  taiwan='S. Tomokiyo signale aussi que de nombreux livres « X密 » de 1913–1923 sont conservés à Taïwan ; beaucoup ne '
         'différaient sans doute que par ces numérotations.'),
 'en': dict(
  h2='Another reading of the key: a renumbered 明密 codebook (S. Tomokiyo)',
  credit=f'<b>This interpretation is due to S. Tomokiyo</b> (<a href="{URL}">Cryptiana</a>, 23 October 2026){SRC}. '
         'He suggests that the clerk did no arithmetic: he used a copy of the “明密” code whose page, column and row numbers '
         'had been rewritten by hand for secret (密) use; he illustrated each key on a June 1916 edition of the 明密碼電報書 '
         'in his possession. Our formulae describe the same table by calculation.',
  check='Check: for all 10,000 group values, the published key splits exactly into page (first two digits), column (tens) '
        'and row (units), with no residual carry (<a href="' + CODE + '">mingmi.py</a>). In the book each column holds xxx1 '
        'to xxx9 and then, at the bottom, xxx0: this is what our “carries” expressed.',
  digit='Written digit', col='column', row='row (1–10)',
  gongmi='Pages numbered backwards: written page 89 = page 00, 88 = 01, …, 01 = 88 (89 − n). Tens give the column, units '
         'the row counted from the bottom. The subtraction from 9000 in our formula is just this double backward count.',
  rongmi='Pages numbered cyclically from page 10: written page 01 = 10, 02 = 11, …, 79 = 88, then 81 = 00, …, 90 = 09. The '
         '“+ 0901” of our formula is this page shift plus one row. The only difference is written page 80: 89 according '
         'to S. Tomokiyo, 99 by our formula. The only group concerned, 8012 (N25), read in neither case (9911, not in the '
         'table; 8911 窔), as S. Tomokiyo noted. With two adjacent digits swapped, 8102 gives 一, hence “一切到乞賜教”: the '
         'reading of N25 is corrected accordingly. S. Tomokiyo’s simpler cyclic numbering is the more probable.',
  chenmi='Our key was already a renumbering (pages counted backwards over the numbers without a zero); S. Tomokiyo shows it '
         'directly on a page of the book. The unit 9 that “counts as 10” is the bottom row, xxx0.',
  taiwan='S. Tomokiyo also notes that many “X密” codebooks of 1913–1923 are preserved in Taiwan; many probably differed only '
         'in such numbering.'),
 'ja': dict(
  h2='鍵のもう一つの読み方：番号を付け替えた明密電碼本（S. Tomokiyo）',
  credit=f'<b>この解釈は S. Tomokiyo 氏による</b>（<a href="{URL}">Cryptiana</a>、2026年10月23日）{SRC}。'
         '電信係は計算をせず、秘密用（密）にページ・列・行の番号を手書きで付け替えた「明密」電碼本を使ったという提案で、'
         '同氏所蔵の1916年6月版『明密碼電報書』上で各鍵を図示している。我々の式は同じ表を計算で記述したものである。',
  check='検証：10,000通りの数字群すべてについて、公開した鍵はページ（上2桁）・列（十の位）・行（一の位）に'
        '繰り上がりなしで正確に分解できる（<a href="' + CODE + '">mingmi.py</a>）。電碼本の各列は xxx1〜xxx9 の後、'
        '最下段に xxx0 を置く。我々の「繰り上がり」はこの配置を表していた。',
  digit='書かれた数字', col='列', row='行（1〜10）',
  gongmi='ページは逆順：書かれたページ89＝00ページ、88＝01、…、01＝88（89−n）。十の位が列、一の位が下から数えた行。'
         '我々の式の「9000から引く」は、この二重の逆順にすぎない。',
  rongmi='ページは10ページから循環：書かれた01＝10、02＝11、…、79＝88、81＝00、…、90＝09。式の「+0901」はこのページの'
         'ずれと1行分である。唯一の違いは書かれたページ80で、Tomokiyo 氏は89、我々の式は99。該当する唯一の数字群'
         ' 8012（N25）は、どちらでも読めなかった（9911は表外、8911は窔）。これは同氏の指摘による。隣接2桁を入れ替えた 8102 は'
         '「一」となり「一切到乞賜教」と読めるので、N25の読みをそのように訂正した。より単純な同氏の循環番号の方が蓋然性が高い。',
  chenmi='我々の鍵はもともと番号の付け替え（0を含まない数で逆順に数えたページ）であり、Tomokiyo 氏はそれを電碼本の'
         '1ページ上で直接示した。「10に当たる」一の位9は最下段の xxx0 である。',
  taiwan='同氏はまた、1913〜1923年の「X密」電碼本が台湾に多数保存されており、その多くはこうした番号付けだけが'
         '異なっていたのだろうと指摘している。'),
 'zh-hans': dict(
  h2='密钥的另一种读法：重新编号的明密电码本（S. Tomokiyo）',
  credit=f'<b>这一解释出自 S. Tomokiyo</b>（<a href="{URL}">Cryptiana</a>，2026年10月23日）{SRC}。'
         '他认为电报员并未计算，而是使用一本为密用而手写改编页码、列号和行号的“明密”电码本；他在自藏的1916年6月版'
         '《明密码电报书》上逐一图示了各密钥。我们的公式只是用计算来描述同一张表。',
  check='验证：对全部10,000个数字组，已发表的密钥都可无残余进位地精确分解为页（前两位）、列（十位）和行（个位）'
        '（<a href="' + CODE + '">mingmi.py</a>）。电码本每列先列 xxx1 至 xxx9，最下一格为 xxx0：我们所说的“进位”即此排法。',
  digit='写出的数字', col='列', row='行（1–10）',
  gongmi='页码倒排：写出的89页 = 第00页，88 = 01，…，01 = 88（89 − n）。十位定列，个位为自下而上的行。'
         '公式中的“以9000相减”不过是这双重倒数。',
  rongmi='页码自第10页起循环：写出的01 = 10，02 = 11，…，79 = 88，再 81 = 00，…，90 = 09。公式中的“+0901”即此页码偏移'
         '加一行。唯一的差别是写出的第80页：Tomokiyo 认为是89，我们的公式给出99。唯一相关的数字组 8012（N25）两种都读不通'
         '（9911 不在表内，8911 为窔），此点由他指出。交换相邻两位后 8102 为“一”，得“一切到乞赐教”，N25 的读法据此更正。'
         '他的循环编号更简单，可能性更大。',
  chenmi='我们的密钥本已是重新编号（页码在不含0的数上倒数）；Tomokiyo 直接在电码本的一页上展示了它。“当作10”的个位9'
         '即最下一格 xxx0。',
  taiwan='他还指出，台湾保存有许多1913–1923年的“X密”电码本，其中很多可能只是这类编号不同。'),
 'zh-hant': dict(
  h2='密鑰的另一種讀法：重新編號的明密電碼本（S. Tomokiyo）',
  credit=f'<b>這一解釋出自 S. Tomokiyo</b>（<a href="{URL}">Cryptiana</a>，2026年10月23日）{SRC}。'
         '他認為電報員並未計算，而是使用一本為密用而手寫改編頁碼、列號和行號的「明密」電碼本；他在自藏的1916年6月版'
         '《明密碼電報書》上逐一圖示了各密鑰。我們的公式只是用計算來描述同一張表。',
  check='驗證：對全部10,000個數字組，已發表的密鑰都可無殘餘進位地精確分解為頁（前兩位）、列（十位）和行（個位）'
        '（<a href="' + CODE + '">mingmi.py</a>）。電碼本每列先列 xxx1 至 xxx9，最下一格為 xxx0：我們所說的「進位」即此排法。',
  digit='寫出的數字', col='列', row='行（1–10）',
  gongmi='頁碼倒排：寫出的89頁 = 第00頁，88 = 01，…，01 = 88（89 − n）。十位定列，個位為自下而上的行。'
         '公式中的「以9000相減」不過是這雙重倒數。',
  rongmi='頁碼自第10頁起循環：寫出的01 = 10，02 = 11，…，79 = 88，再 81 = 00，…，90 = 09。公式中的「+0901」即此頁碼偏移'
         '加一行。唯一的差別是寫出的第80頁：Tomokiyo 認為是89，我們的公式給出99。唯一相關的數字組 8012（N25）兩種都讀不通'
         '（9911 不在表內，8911 為窔），此點由他指出。交換相鄰兩位後 8102 為「一」，得「一切到乞賜教」，N25 的讀法據此更正。'
         '他的循環編號更簡單，可能性更大。',
  chenmi='我們的密鑰本已是重新編號（頁碼在不含0的數上倒數）；Tomokiyo 直接在電碼本的一頁上展示了它。「當作10」的個位9'
         '即最下一格 xxx0。',
  taiwan='他還指出，臺灣保存有許多1913–1923年的「X密」電碼本，其中很多可能只是這類編號不同。'),
}


def block(key, L):
    t = T[L]
    _, g, h, _ = M.factorize(DEC[key])
    cells = lambda d: ''.join(f'<td>{d[i]}</td>' for i in range(10))
    table = (f'<div class="gm-scroll"><table><tr><th>{t["digit"]}</th>' + ''.join(f'<td>{i}</td>' for i in range(10)) +
             f'</tr><tr><th>{t["col"]}</th>{cells(g)}</tr><tr><th>{t["row"]}</th>{cells(h)}</tr></table></div>')
    return (f'<!-- MINGMI:begin -->\n<section id="mingmi"><h2>{html.escape(t["h2"])}</h2><p>{t["credit"]}</p>'
            f'<p>{html.escape(t[key])}</p>{table}<p>{t["check"]}</p><p>{html.escape(t["taiwan"])}</p></section>\n<!-- MINGMI:end -->\n')


def insert(key, L):
    p = os.path.join(SITE, 'content', L, f'{key}.html')
    s = open(p, encoding='utf-8').read()
    b, e = s.find('<!-- MINGMI:begin -->'), s.find('<!-- MINGMI:end -->')
    if b >= 0:
        s = s[:b] + s[e + len('<!-- MINGMI:end -->\n'):]
    i = s.find(ANCHOR[key])
    if i < 0:
        raise SystemExit(f'ancre absente : {p}')
    s = s[:i] + block(key, L) + s[i:]
    open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    for key in DEC:
        for L in LANGS:
            insert(key, L)
    print('bloc MINGMI inséré dans', len(DEC) * len(LANGS), 'pages')
