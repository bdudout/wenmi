#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insère/actualise la section « 乾密 » (id="qianmi") de content/<langue>/method.html, après la section 辰密 (idempotent).
Le modèle de clé (livre 明密 renuméroté) est l'idée de S. Tomokiyo (Cryptiana, 23/10/2026), source [22]."""
import os, re, sys
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'c107'))
import qianmi_key as K   # noqa: E402
SRC = '<a href="sources.html#s22">[22]</a>'
def tables(h):
    t = f'<div class="table-wrap"><table><tr><th>{h[0]}</th>' + ''.join(f'<td>{d}</td>' for d in range(10)) + '</tr>'
    t += f'<tr><th>{h[1]}</th>' + ''.join(f'<td>{v}</td>' for v in K.COL) + f'</tr><tr><th>{h[2]}</th>' + ''.join(f'<td>{v}</td>' for v in K.ROW) + '</tr></table></div>'
    return t
def ex(h):
    rows = ''.join(f'<tr><td>{g}</td><td>{g[:2]} → {K.page(g[:2]):02d}</td><td>{g[2]} → {K.COL[int(g[2])]}</td><td>{g[3]} → {K.ROW[int(g[3])]}</td><td>{K.decode(g):04d}</td><td>{K.glyph(g)}</td></tr>' for g in ('7096', '4044', '1114'))
    return '<div class="table-wrap"><table><tr>' + ''.join(f'<td>{x}</td>' for x in h) + '</tr>' + rows + '</table></div>'
S = {
'fr': dict(h=['Chiffre lu', 'colonne', 'ligne'], x=['Groupe lu', 'Page', 'Colonne', 'Ligne', 'Résultat', 'CTC'], body=lambda t, x: (
 '<section class="article" id="qianmi"><h2>Un livre renuméroté : l’idée de S. Tomokiyo et le télégramme « 乾密 »</h2>'
 f'<p><strong>L’idée.</strong> Le 23 octobre 2026, S. Tomokiyo (Cryptiana) a proposé de relire nos trois clés numériques comme l’aurait fait l’employé de 1916 : non par un calcul, mais avec un exemplaire du code télégraphique « 明密 » dont on aurait réécrit à la main les numéros de pages, de colonnes et de lignes {SRC}. Nous l’avons vérifié : pour les 10 000 groupes possibles, les clés <span lang="zh-Hant">共密</span>, <span lang="zh-Hant">容密</span> et <span lang="zh-Hant">辰密</span> se décomposent exactement en page (deux premiers chiffres), colonne (dizaine) et ligne (unité), la ligne 10 étant le caractère xxx0 au bas de chaque colonne. Les pages sont numérotées à rebours (<span lang="zh-Hant">共密</span>), en boucle à partir de la page 10 (<span lang="zh-Hant">容密</span>) ou sans zéro (<span lang="zh-Hant">辰密</span>). L’idée et cette reformulation sont les siennes ; chaque page de clé du site le signale.</p>'
 '<p><strong>Notre découverte.</strong> Si les livres « X密 » ne différaient que par ces numérotations, un même modèle devait pouvoir ouvrir les télégrammes encore illisibles. Nous avons cherché, pour chacun, une règle de pages simple (à rebours, en boucle ou sans zéro, avec un point de départ libre) et deux permutations libres, des colonnes et des lignes, ajustées sur un modèle de langue. Le protocole a été fixé avant tout calcul sur les vrais messages : chaque essai était comparé à des messages synthétiques de même longueur, chiffrés avec une clé de ce type (la méthode devait les retrouver), et à des chiffres mélangés (elle ne devait rien y trouver).</p>'
 '<p>Le télégramme N09, préfixé <span lang="zh-Hant">乾密</span> et parti de la maison de Huang Xing à Tokyo, se détache nettement : score 4,47 contre 2,88 pour le meilleur témoin. Sa clé : <strong>page = page écrite − 11</strong>, puis :</p>' + t +
 '<h3>Exemples</h3>' + x +
 '<p>Le texte se lit : « 袁死。此間態度未變，候交涉有望，再電告。興 » (« Yuan est mort. Ici, l’attitude n’a pas changé ; j’attendrai que les négociations soient en bonne voie pour télégraphier de nouveau. Xing »). Il finit par la signature attendue 興, et commence par la mort de Yuan Shikai (6 juin), ce qui s’accorde avec sa place dans le dossier. Les trois caractères aberrants (卵, 侯, 命) ont été relus deux fois sur l’image par Brice Dudout, la seconde en aveugle : les chiffres sont sûrs, et nous proposons 未 (un chiffre d’écart), 候 et 告 (contexte).</p>'
 '<p><strong>Limites.</strong> Un seul télégramme, 17 groupes : la clé n’est vérifiée que sur lui. N03, autre <span lang="zh-Hant">乾密</span> du même expéditeur, reste illisible avec elle. Le même modèle donne pour N01 une lecture partielle encore trop incertaine pour être publiée. Pour N07, le résultat est négatif. Édition : <a href="qianmi.html">page 乾密</a> ; vérification de la factorisation des trois premières clés : <a href="https://github.com/bdudout/wenmi/blob/main/solver/numeric1916/mingmi.py">mingmi.py</a>.</p></section>')),
'en': dict(h=['Digit read', 'column', 'row'], x=['Group read', 'Page', 'Column', 'Row', 'Result', 'CTC'], body=lambda t, x: (
 '<section class="article" id="qianmi"><h2>A renumbered book: S. Tomokiyo’s idea and the “Qianmi” (乾密) telegram</h2>'
 f'<p><strong>The idea.</strong> On 23 October 2026, S. Tomokiyo (Cryptiana) suggested re-reading our three numeric keys as the 1916 clerk would have used them: not by calculation, but with a copy of the “明密” telegraph code whose page, column and row numbers had been rewritten by hand {SRC}. We checked it: over all 10,000 possible groups, the <span lang="zh-Hant">共密</span>, <span lang="zh-Hant">容密</span> and <span lang="zh-Hant">辰密</span> keys split exactly into page (first two digits), column (tens) and row (units), row 10 being the xxx0 character at the foot of each column. Pages are numbered backwards (<span lang="zh-Hant">共密</span>), cyclically from page 10 (<span lang="zh-Hant">容密</span>) or without zeros (<span lang="zh-Hant">辰密</span>). The idea and this reformulation are his; every key page on this site says so.</p>'
 '<p><strong>Our finding.</strong> If the “X密” books differed only in such numbering, one model should open the telegrams that were still unreadable. For each we searched for a simple page rule (backwards, cyclic or zero-free, with a free starting point) and two free permutations, of columns and of rows, fitted to a language model. The protocol was fixed before any computation on the real messages: each trial was compared with synthetic messages of the same length enciphered with such a key (the method had to recover them) and with shuffled digits (it had to find nothing).</p>'
 '<p>Telegram N09, prefixed <span lang="zh-Hant">乾密</span> and sent from Huang Xing’s house in Tokyo, stands out clearly: score 4.47 against 2.88 for the best control. Its key: <strong>page = written page − 11</strong>, then:</p>' + t +
 '<h3>Examples</h3>' + x +
 '<p>The text reads: “袁死。此間態度未變，候交涉有望，再電告。興” (“Yuan is dead. Here the attitude has not changed; I shall wait until the negotiations look promising and cable again. Xing”). It ends with the expected signature 興 and opens with Yuan Shikai’s death (6 June), which fits its place in the file. The three aberrant characters (卵, 侯, 命) were re-read twice on the image by Brice Dudout, the second time blind: the digits are sound, and we propose 未 (one digit off), 候 and 告 (context).</p>'
 '<p><strong>Limits.</strong> One telegram, 17 groups: the key is checked on it alone. N03, another <span lang="zh-Hant">乾密</span> from the same sender, stays unreadable with it. The same model gives N01 a partial reading still too uncertain to publish. For N07, the result is negative. Edition: <a href="qianmi.html">Qianmi page</a>; check of the factorisation of the first three keys: <a href="https://github.com/bdudout/wenmi/blob/main/solver/numeric1916/mingmi.py">mingmi.py</a>.</p></section>')),
'ja': dict(h=['読んだ数字', '列', '行'], x=['読んだ組', '頁', '列', '行', '結果', 'CTC'], body=lambda t, x: (
 '<section class="article" id="qianmi"><h2>番号を付け替えた本：S. Tomokiyo氏の着想と「乾密」電報</h2>'
 f'<p><strong>着想。</strong>2026年10月23日、S. Tomokiyo氏（Cryptiana）は、私たちの三つの数字鍵を1916年の電信係のやり方で読み直すことを提案した。計算ではなく、頁・列・行の番号を手書きで付け替えた「明密」電碼本を使ったというのである{SRC}。私たちはこれを確かめた：10,000通りのすべての組について、<span lang="zh-Hant">共密</span>・<span lang="zh-Hant">容密</span>・<span lang="zh-Hant">辰密</span>の鍵は頁（上2桁）・列（十の位）・行（一の位）に正確に分解でき、10行目は各列の最下段のxxx0である。頁の番号は逆順（共密）、10頁から循環（容密）、0を含まない数（辰密）。着想とこの再定式化は同氏のものであり、本サイトの各鍵のページにそう記している。</p>'
 '<p><strong>私たちの発見。</strong>「X密」の本がこうした番号付けだけで異なるのなら、同じモデルで未解読の電報も開けるはずである。各電報について、単純な頁の規則（逆順・循環・0なし、起点は自由）と、列と行の二つの自由な置換を探し、言語モデルで当てはめた。実際の電報で計算する前に手順を定め、同じ長さでこの型の鍵により暗号化した合成電文（方法が復元できるはずのもの）と、攪拌した数字（何も見つからないはずのもの）と比べた。</p>'
 '<p>黄興の東京の家から出た、前置き<span lang="zh-Hant">乾密</span>のN09がはっきり抜きんでた（4.47、最良の対照は2.88）。鍵は<strong>頁＝書かれた頁−11</strong>、さらに：</p>' + t +
 '<h3>例</h3>' + x +
 '<p>本文は「袁死。此間態度未變，候交涉有望，再電告。興」（袁死す。当地の態度は変わらない。交渉に望みが出るのを待って改めて打電する。興）と読める。期待どおり署名「興」で終わり、袁世凱の死（6月6日）で始まり、綴りの中の位置と合う。異常な3字（卵・侯・命）はBrice Dudoutが画像上で2回、2回目は盲検で読み直し、数字は確かである。未（1桁違い）、候・告（文脈）と読む。</p>'
 '<p><strong>限界。</strong>電報1通・17組で、鍵はこれだけで検証されている。同じ差出人の乾密N03はこの鍵では読めない。同じモデルはN01に部分的な読みを与えるが、公表するにはまだ不確かである。N07は陰性。校訂：<a href="qianmi.html">乾密のページ</a>。最初の三つの鍵の分解の検証：<a href="https://github.com/bdudout/wenmi/blob/main/solver/numeric1916/mingmi.py">mingmi.py</a>。</p></section>')),
'zh-hant': dict(h=['所讀數字', '列', '行'], x=['所讀之組', '頁', '列', '行', '結果', 'CTC'], body=lambda t, x: (
 '<section class="article" id="qianmi"><h2>重新編號的電碼本：S. Tomokiyo的構想與「乾密」電報</h2>'
 f'<p><strong>構想。</strong>2026年10月23日，S. Tomokiyo（Cryptiana）提出按1916年電報員的做法重讀我們的三種數字密鑰：不是計算，而是使用一本頁、列、行編號都經手寫改過的「明密」電碼本{SRC}。我們加以驗證：在全部10,000個可能的組上，<span lang="zh-Hant">共密</span>、<span lang="zh-Hant">容密</span>、<span lang="zh-Hant">辰密</span>的密鑰都能精確分解為頁（前兩位）、列（十位）與行（個位），第10行即每列底端的xxx0。頁的編號或倒數（共密），或自第10頁起循環（容密），或不含零（辰密）。構想與這一重新表述都屬於他；本站每個密鑰頁面都已註明。</p>'
 '<p><strong>我們的發現。</strong>若「X密」各本只在這類編號上不同，同一模型應能打開尚未讀出的電報。我們為每封電報尋找簡單的頁規則（倒數、循環或不含零，起點不限）以及列、行兩個自由置換，以語言模型擬合。在對真實電報計算之前即定下規程：每次試驗都與同長度、以此類密鑰加密的合成電文（方法須能復原）以及打亂的數字（方法須一無所得）相比。</p>'
 '<p>前綴<span lang="zh-Hant">乾密</span>、自黃興東京寓所發出的N09明顯突出：4.47，最佳對照2.88。其密鑰：<strong>頁＝所寫頁數−11</strong>，其次：</p>' + t +
 '<h3>示例</h3>' + x +
 '<p>全文可讀：「袁死。此間態度未變，候交涉有望，再電告。興」。以預期的署名「興」作結，以袁世凱之死（6月6日）開頭，與它在卷宗中的位置相符。三個反常字（卵、侯、命）由Brice Dudout在影像上複讀兩次，第二次為盲讀：數字可靠；我們推定為未（差一位數字）、候、告（據文意）。</p>'
 '<p><strong>局限。</strong>僅一封電報、17組：密鑰只在此電上得到驗證。同一發報人的另一封乾密N03用此密鑰仍不可讀。同一模型給N01的部分讀法尚不足以發表。N07為陰性。校訂：<a href="qianmi.html">乾密頁面</a>；前三種密鑰分解的驗證：<a href="https://github.com/bdudout/wenmi/blob/main/solver/numeric1916/mingmi.py">mingmi.py</a>。</p></section>')),
}
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import c1916_i18n as C
    T2 = C.t2s_table(WENMI)
    for L in ('fr', 'en', 'ja', 'zh-hant', 'zh-hans'):
        d = S['zh-hant'] if L == 'zh-hans' else S[L]
        sec = d['body'](tables(d['h']), ex(d['x']))
        if L == 'zh-hans':
            sec = C.to_hans(sec, T2).replace('lang="zh-Hant">乾密', 'lang="zh-Hant">乾密')
        p = os.path.join(SITE, 'content', L, 'method.html'); s = open(p, encoding='utf-8').read()
        s = re.sub(r'\n  <section class="article" id="qianmi">.*?</section>', '', s, flags=re.S)
        i = s.find('id="chenmi"'); assert i > 0, L
        j = s.find('</section>', i) + len('</section>')
        s = s[:j] + '\n  ' + sec + s[j:]
        open(p, 'w', encoding='utf-8').write(s)
    print('method: section 乾密 (5 langues)')
