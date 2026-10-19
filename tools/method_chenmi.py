#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insère/actualise la section « 辰密 » (id="chenmi") de content/<langue>/method.html, après la section 容密 (idempotent)."""
import os, re, sys
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c92'))
import chenmi_key as K   # noqa: E402
ZF = [n for n in range(99, 10, -1) if '0' not in str(n)]
def tables(h):
    t = f'<div class="table-wrap"><table><tr><th>{h[0]}</th>' + ''.join(f'<td>{d}</td>' for d in range(10)) + '</tr>'
    t += f'<tr><th>{h[1]}</th>' + ''.join(f'<td>{v}</td>' for v in K.T) + '</tr><tr><th>{h[2]}</th>'.replace('{h[2]}', h[2]) + ''.join(f'<td>{v}</td>' for v in K.U) + '</tr></table></div>'
    pg = '<div class="table-wrap"><table><tr><th>' + h[3] + '</th>' + ''.join(f'<td>{c}</td>' for c in ZF[:10]) + '<td>…</td><td>11</td></tr><tr><th>' + h[4] + '</th>' + ''.join(f'<td>{i:02d}</td>' for i in range(10)) + '<td>…</td><td>80</td></tr></table></div>'
    return pg, t
def ex(h):
    rows = ''.join(f'<tr><td>{g}</td><td>{g[:2]} → {K.PG[int(g[:2])]:02d}</td><td>{g[2]} → {K.T[int(g[2])]}</td><td>{g[3]} → {K.U[int(g[3])]}</td><td>{K.decode(g):04d}</td><td>{K.glyph(g)}</td></tr>' for g in ('9950', '4220', '6219'))
    return '<div class="table-wrap"><table><tr>' + ''.join(f'<td>{x}</td>' for x in h) + '</tr>' + rows + '</table></div>'
S = {
'fr': dict(h=['Chiffre lu', 'dizaines', 'unités', 'Page chiffrée', 'Page du CTC'], x=['Groupe lu', 'Page', 'Dizaine', 'Unité', 'Résultat', 'CTC'], body=lambda pg, t, x: (
 '<section class="article" id="chenmi"><h2>Une quatrième famille : les télégrammes « 辰密 »</h2>'
 '<p>Quatre télégrammes de juin 1916, envoyés de Tokyo par Huang Xing et Zhang Xiaozhun à l’adresse télégraphique « ヒツキン » (霞飛路 277, Shanghai), celle du groupe hunanais, commencent par le préfixe en clair <code>6591 1378</code>, c’est-à-dire <span lang="zh-Hant">辰密</span> (sauf N05, sans préfixe). Le nom se retrouve dans l’édition des brouillons de Huang Xing pour ses correspondants hunanais. Ici, pas de constante à ajouter : le code télégraphique est <b>réordonné</b>.</p>'
 '<p><strong>1. Lire les chiffres</strong> comme pour <span lang="zh-Hant">共密</span> et <span lang="zh-Hant">容密</span> : par colonnes, de droite à gauche et de haut en bas (parcours proposé par Brice Dudout), en groupes de quatre.</p>'
 '<p><strong>2. Les deux premiers chiffres donnent la page.</strong> Le CTC est rangé par pages de cent caractères (0000–0099, 0100–0199…). Dans <span lang="zh-Hant">辰密</span>, les pages sont numérotées à rebours, en sautant tout nombre qui contient un zéro : 99 est la page 00, 98 la page 01, …, 91 la page 08, puis 89 la page 09 (90 est sauté), et ainsi de suite jusqu’à 11 = page 80.</p>' + pg +
 '<p>C’est ce qui avait d’abord intrigué : dans ces télégrammes, aucun groupe n’a de 0 aux milliers ni aux centaines.</p>'
 '<p><strong>3. Les deux derniers chiffres donnent la place dans la page</strong>, après remplacement du chiffre des dizaines et de celui des unités :</p>' + t +
 '<p>L’unité 9 vaut « 10 » : elle ajoute une dizaine, avec retenue ordinaire. <strong>4. Lire le résultat</strong> P = 100 × page + 10 × dizaine + unité dans le CTC.</p><h3>Exemples</h3>' + x +
 '<p><strong>Comment la clé a été trouvée.</strong> Les essais des familles <span lang="zh-Hant">共密</span> et <span lang="zh-Hant">容密</span> échouaient, et aucun télégramme 辰密 n’avait de clair connu. Deux observations ont orienté la recherche : l’absence de 0 aux deux premiers rangs, et la concentration des groupes sur quelques « pages » (99, 96, 93 font un quart du texte), signe d’un livre rangé par fréquence. Un modèle « page permutée + dizaines et unités permutées » a été ajusté sur N13, N16 et N26 (201 groupes) ; les méthodes d’affectation exacte restaient bloquées dans de faux optimums, et c’est un <b>recuit simulé</b> qui a trouvé un texte lisible, très au-dessus des témoins mélangés (calibration 3/3). La table de pages trouvée suivait le décompte sans zéro, qui a été imposé ; deux caractères aberrants (劈 pour 力, 滠 pour 灰), tous deux venant de groupes finissant par 9, ont révélé la règle « 9 = 10 ».</p>'
 '<p><strong>Comment elle a été vérifiée.</strong> (1) N05, que la recherche n’avait pas utilisé et qui n’a même pas de préfixe, se lit d’un trait sous la clé. (2) N16, daté du 10 sur son en-tête, se termine par <span lang="zh-Hant">灰</span>, code du 10e jour. (3) N16 dit « hier, Keqiang a télégraphié pour… » et reprend la demande de N13, signé de Huang Xing la veille. (4) Les noms sont ceux de personnes réelles du Hunan en 1916 : 趙夷午 (趙恆惕), 湯督 (湯薌銘), 濟武 (湯化龍). (5) Aucun échange dans les tables de dizaines ou d’unités n’améliore le texte.</p>'
 '<p><strong>Limites.</strong> On ne sait pas comment ce code était noté en 1916, ni si le livre suivait exactement le CTC de référence ; quatre caractères sont des lectures probables à un chiffre près, « 一不 » (N13) est sans doute une inversion pour 不一, et 盻 (N05) se lit 盼 par le contexte, comme en 容密. Décodeur : <a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a> ; télégrammes : <a href="chenmi.html">page 辰密</a> et <a href="telegrams.html#grp-numeric">Télégrammes</a>.</p></section>')),
'en': dict(h=['Digit read', 'tens', 'units', 'Cipher page', 'CTC page'], x=['Group read', 'Page', 'Tens', 'Units', 'Result', 'CTC'], body=lambda pg, t, x: (
 '<section class="article" id="chenmi"><h2>A fourth family: the “Chenmi” (辰密) telegrams</h2>'
 '<p>Four telegrams of June 1916, sent from Tokyo by Huang Xing and Zhang Xiaozhun to the telegraphic address “ヒツキン” (277 Avenue Joffre, Shanghai), that of the Hunanese group, begin with the clear prefix <code>6591 1378</code>, that is <span lang="zh-Hant">辰密</span> (except N05, which has no prefix). The name also appears in the edition of Huang Xing’s drafts for his Hunanese correspondents. Here there is no constant to add: the telegraph code is <b>reordered</b>.</p>'
 '<p><strong>1. Read the digits</strong> as for <span lang="zh-Hant">共密</span> and <span lang="zh-Hant">容密</span>: in columns, right to left and top to bottom (reading order proposed by Brice Dudout), in groups of four.</p>'
 '<p><strong>2. The first two digits give the page.</strong> The CTC is arranged in pages of a hundred characters (0000–0099, 0100–0199…). In <span lang="zh-Hant">辰密</span> the pages are numbered backwards, skipping every number that contains a zero: 99 is page 00, 98 page 01, …, 91 page 08, then 89 page 09 (90 is skipped), and so on down to 11 = page 80.</p>' + pg +
 '<p>This is what first caught the eye: in these telegrams no group has a 0 in the thousands or hundreds.</p>'
 '<p><strong>3. The last two digits give the place on the page</strong>, after replacing the tens digit and the units digit:</p>' + t +
 '<p>The units digit 9 stands for “10”: it adds a ten, with ordinary carry. <strong>4. Read the result</strong> P = 100 × page + 10 × tens + units in the CTC.</p><h3>Examples</h3>' + x +
 '<p><strong>How the key was found.</strong> Trials of the <span lang="zh-Hant">共密</span> and <span lang="zh-Hant">容密</span> families failed, and no Chenmi telegram had a known plaintext. Two observations guided the search: no 0 in the first two places, and groups concentrated on a few “pages” (99, 96, 93 make up a quarter of the text), the mark of a book ordered by frequency. A “permuted page + permuted tens and units” model was fitted on N13, N16 and N26 (201 groups); exact-assignment methods got stuck in false optima, and it was <b>simulated annealing</b> that found readable text, far above shuffled controls (calibration 3/3). The page table found followed the zero-free countdown, which was then imposed; two aberrant characters (劈 for 力, 滠 for 灰), both from groups ending in 9, revealed the “9 = 10” rule.</p>'
 '<p><strong>How it was checked.</strong> (1) N05, not used in the search and without even a prefix, reads straight through under the key. (2) N16, dated the 10th on its header, ends with <span lang="zh-Hant">灰</span>, the code for the 10th day. (3) N16 says “yesterday Keqiang cabled to…” and repeats the request of N13, signed by Huang Xing the day before. (4) The names are those of real Hunan figures of 1916: 趙夷午 (Zhao Hengti), 湯督 (Tang Xiangming), 濟武 (Tang Hualong). (5) No swap in the tens or units tables improves the text.</p>'
 '<p><strong>Limits.</strong> We do not know how this code was written down in 1916, nor whether the book followed the reference CTC exactly; four characters are single-digit probable readings, “一不” (N13) is probably an inversion for 不一, and 盻 (N05) is read 盼 from context, as in Rongmi. Decoder: <a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a>; telegrams: <a href="chenmi.html">Chenmi page</a> and <a href="telegrams.html#grp-numeric">Telegrams</a>.</p></section>')),
'ja': dict(h=['読んだ数字', '十の位', '一の位', '暗号の頁', 'CTCの頁'], x=['読んだ組', '頁', '十', '一', '結果', 'CTC'], body=lambda pg, t, x: (
 '<section class="article" id="chenmi"><h2>第四の系統：「辰密」電報</h2>'
 '<p>1916年6月に黄興と張孝準が東京から上海の電信あて名「ヒツキン」（霞飛路277、湖南派のあて先）に送った電報4通は、平文の前置き<code>6591 1378</code>、すなわち<span lang="zh-Hant">辰密</span>で始まる（N05には前置きがない）。この名は黄興の電稿の刊本にも、湖南の同志あてとして見える。ここでは定数の加算はなく、電碼そのものが<b>並べ替え</b>られている。</p>'
 '<p><strong>1. 数字を読む</strong>：<span lang="zh-Hant">共密</span>・<span lang="zh-Hant">容密</span>と同じく、列ごとに右から左、上から下へ（Brice Dudoutの提案した順序）、4桁ずつ。</p>'
 '<p><strong>2. 最初の2桁が頁を示す。</strong>CTCは百字ずつの頁（0000〜0099、0100〜0199…）に並ぶ。<span lang="zh-Hant">辰密</span>では頁を逆順に、0を含む数を飛ばして数える：99が00頁、98が01頁、…、91が08頁、次に89が09頁（90は飛ばす）、以下11＝80頁まで。</p>' + pg +
 '<p>最初に目を引いたのはこの点で、これらの電報では千の位・百の位に0が一度も現れない。</p>'
 '<p><strong>3. 後の2桁が頁の中の位置を示す。</strong>十の位と一の位をそれぞれ置き換える：</p>' + t +
 '<p>一の位の9は「10」で、通常どおり十の位に繰り上がる。<strong>4. 結果</strong> P＝100×頁＋10×十の位＋一の位をCTCで読む。</p><h3>例</h3>' + x +
 '<p><strong>鍵の発見。</strong>共密・容密の系統の試みは失敗し、辰密には既知の平文がなかった。手がかりは二つ：最初の2桁に0がないこと、組が少数の「頁」に集中すること（99・96・93で全体の4分の1）で、頻度順に並べた本を思わせる。N13・N16・N26（201組）に「頁の置換＋十の位・一の位の置換」のモデルを当てはめた。厳密な割当て法は偽の最適解にとどまり、<b>焼きなまし法</b>が攪拌した対照を大きく上回る読める文を見つけた（較正3/3）。得られた頁表は0を含まない逆順に従っていたので、それを課した。9で終わる組から来る二つの異常字（力に劈、灰に滠）から「9＝10」の規則が分かった。</p>'
 '<p><strong>検証。</strong>（1）探索に使わず前置きもないN05が、この鍵でそのまま読める。（2）見出しが10日のN16は10日の韻目<span lang="zh-Hant">灰</span>で終わる。（3）N16は「昨日、克強が打電して…」と述べ、前日に黄興が署名したN13の依頼を繰り返す。（4）人名は1916年の湖南の実在の人物：趙夷午（趙恒惕）、湯督（湯薌銘）、濟武（湯化龍）。（5）十の位・一の位の表のどの入れ替えも文を改善しない。</p>'
 '<p><strong>限界。</strong>1916年にこの暗号がどう記されたか、本が参照CTCに正確に従っていたかは分からない。4字は1桁違いの推定読みで、N13の「一不」はおそらく「不一」の転倒で、N05の「盻」は容密と同じく文脈から「盼」と読む。解読プログラム：<a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a>、電報：<a href="chenmi.html">辰密のページ</a>と<a href="telegrams.html#grp-numeric">電報一覧</a>。</p></section>')),
'zh-hant': dict(h=['所讀數字', '十位', '個位', '密文頁', 'CTC頁'], x=['所讀之組', '頁', '十位', '個位', '結果', 'CTC'], body=lambda pg, t, x: (
 '<section class="article" id="chenmi"><h2>第四個系統：「辰密」電報</h2>'
 '<p>1916年6月黃興與張孝準自東京發往上海電報地址「ヒツキン」（霞飛路277號，湘籍諸人的地址）的四封電報，以明文前綴<code>6591 1378</code>開頭，即<span lang="zh-Hant">辰密</span>（N05無前綴）。此名亦見於《黃興等電稿》致湘籍同志的電報。這裡沒有加減常數，而是將電碼本身<b>重新排列</b>。</p>'
 '<p><strong>一、讀取數字。</strong>與<span lang="zh-Hant">共密</span>、<span lang="zh-Hant">容密</span>相同：按列由右至左、由上而下（Brice Dudout 提出的讀序），每四位一組。</p>'
 '<p><strong>二、前兩位表示頁。</strong>中文電碼按每頁百字排列（0000–0099、0100–0199……）。<span lang="zh-Hant">辰密</span>將頁倒數編號，並跳過一切含零的數：99為第00頁，98為第01頁，……，91為第08頁，其次89為第09頁（跳過90），依此類推至11＝第80頁。</p>' + pg +
 '<p>最初引人注意的正是這一點：這些電報的千位與百位從不出現0。</p>'
 '<p><strong>三、後兩位表示頁內位置，</strong>十位與個位各自替換：</p>' + t +
 '<p>個位的9作「10」，按通常進位向十位進一。<strong>四、在中文電碼中查讀結果</strong>P＝100×頁＋10×十位＋個位。</p><h3>示例</h3>' + x +
 '<p><strong>密鑰如何找到。</strong>共密、容密兩系統的嘗試均告失敗，辰密又無已知明文。兩點觀察指引了搜尋：前兩位沒有0；各組集中於少數「頁」（99、96、93三頁佔全文四分之一），像是按字頻排列的本子。在N13、N16、N26（201組）上擬合「頁置換＋十位與個位置換」的模型；精確指派法困於假最優，是<b>模擬退火</b>找到了遠高於打亂對照的可讀文字（校準3/3）。所得頁表遵循不含零的倒數，於是以此為規則；兩個反常字（「力」作「劈」、「灰」作「滠」）都來自以9結尾的組，由此發現「9＝10」。</p>'
 '<p><strong>如何驗證。</strong>（一）未參與搜尋、連前綴都沒有的N05，在此密鑰下一氣讀出。（二）電頭為十日的N16以「<span lang="zh-Hant">灰</span>」（十日）結尾。（三）N16說「昨克電請……」，重提前一天黃興署名的N13的請求。（四）人名是1916年湖南的真實人物：趙夷午（趙恆惕）、湯督（湯薌銘）、濟武（湯化龍）。（五）十位或個位表的任何對調都不能使文字更通順。</p>'
 '<p><strong>局限。</strong>不知1916年此密碼如何記錄，也不知所用之本是否完全依照參照的中文電碼；四個字是相差一位數字的推定讀法，N13的「一不」大概是「不一」的倒置，N05的「盻」與容密一樣據文意讀作「盼」。解碼程式：<a href="https://github.com/bdudout/wenmi/tree/main/solver/chenmi">solver/chenmi</a>；電報：<a href="chenmi.html">辰密頁面</a>及<a href="telegrams.html#grp-numeric">電報全文</a>。</p></section>')),
}
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import c1916_i18n as C
    T2 = C.t2s_table(WENMI)
    for L in ('fr', 'en', 'ja', 'zh-hant', 'zh-hans'):
        d = S['zh-hant'] if L == 'zh-hans' else S[L]
        pg, t = tables(d['h']); sec = d['body'](pg, t, ex(d['x']))
        if L == 'zh-hans':
            sec = C.to_hans(sec, T2).replace('lang="zh-Hant">辰密', 'lang="zh-Hant">辰密')
        p = os.path.join(SITE, 'content', L, 'method.html'); s = open(p, encoding='utf-8').read()
        s = re.sub(r'\n  <section class="article" id="chenmi">.*?</section>', '', s, flags=re.S)
        i = s.find('id="rongmi"'); j = s.find('</section>', i) + len('</section>')
        s = s[:j] + '\n  ' + sec + s[j:]
        open(p, 'w', encoding='utf-8').write(s)
    print('method: section 辰密 (5 langues)')
