#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insère/actualise la section « tables du 外務省 / N01 » (id="gaimusho") de content/<langue>/method.html, après la section 乾密
(idempotent). Tables transcrites en C110 (JACAR B03050089200, PDF 16) ; clé identique à C104-A3."""
import os, re, sys
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))
HEAD = '9876543210'
T1 = ['9678012345', '0123456789', '0864297531', '0537846219']
T2 = ['9678012345', '0123456789', '4837261509', '0563847219']
def table(rows, labels):
    t = '<div class="table-wrap"><table><tr><th></th>' + ''.join(f'<td>{d}</td>' for d in HEAD) + '</tr>'
    return t + ''.join(f'<tr><th>{lab}</th>' + ''.join(f'<td>{d}</td>' for d in r) + '</tr>' for lab, r in zip(labels, rows)) + '</table></div>'
LAB = ['千位', '百位', '十位', '一位']
S = {
'fr': lambda t1, t2: (
 '<section class="article" id="gaimusho"><h2>Une clé tenue par le ministère japonais : N01</h2>'
 '<p><strong>Le document.</strong> Dans le même dossier que les télégrammes, la page 16 de B03050089200 est une feuille du ministère japonais des Affaires étrangères (papier marqué 外務省), datée de juin 1916 par son classement. Elle porte deux tables de chiffres, rang par rang (milliers, centaines, dizaines, unités), sous l’en-tête 9 8 7 6 5 4 3 2 1 0. La page 17 en est le brouillon ; la page 18, une grille de syllabes sans rapport avec ces télégrammes. Nous n’avions jamais su à quel télégramme elles s’appliquaient<sup class="fn"><a href="sources.html#s27">[27]</a></sup>.</p>'
 '<h3>Les deux tables (transcription)</h3>' + t1 + t2 +
 '<p>La seconde table est l’inverse exacte de la première : l’une sert à chiffrer, l’autre à déchiffrer. Une case de la seconde (dizaines, 6ᵉ) porte un 6 surchargé d’un 9 ; le 6 est le seul chiffre qui complète la ligne, et le brouillon le donne.</p>'
 '<p><strong>Le résultat.</strong> Ces tables ne lisent aucun des télégrammes déjà déchiffrés (共密, 容密, 辰密, 乾密), ni N03, N06 ou N07. Elles lisent <a href="telegrams.html#tnum-N01">N01</a>, un télégramme de Shanghai sans préfixe, reçu à Tokyo en mai 1916 : « 轉克強先生：袁逆將倒，時局益艱……盼承指導，俾有遵循 », suivi d’une quinzaine de signatures d’un caractère. Le score est très au-dessus de 200 témoins mélangés.</p>'
 '<p><strong>Une double confirmation.</strong> Peu auparavant, notre recherche selon le modèle de S. Tomokiyo (un livre 明密 renuméroté) avait trouvé pour N01, sans connaître ces tables, une clé candidate. Elle est identique case par case à celle du ministère. Deux reconstructions indépendantes, l’une de juin 1916, l’autre d’octobre 2026, donnent la même clé. Seule différence de forme : les tables, écrites chiffre par chiffre, ne peuvent pas noter les pages en boucle (étiquettes 90 à 99), ni la ligne 10 (un 0 en unité), que la lecture du texte exige.</p>'
 '<p><strong>Ce que cela dit.</strong> Le ministère japonais disposait en juin 1916 de la clé d’au moins un canal entre les amis de Shanghai et Huang Xing. Nous ne savons pas s’il l’a cassée ou obtenue autrement. Les autres feuilles de cryptanalyse du même dossier restent à étudier. Limites : une seule clé, un seul télégramme ; dans N01, 柬 n’est pas résolu et plusieurs signatures ne sont pas identifiées.</p></section>'),
'en': lambda t1, t2: (
 '<section class="article" id="gaimusho"><h2>A key held by the Japanese Foreign Ministry: N01</h2>'
 '<p><strong>The document.</strong> In the same file as the telegrams, page 16 of B03050089200 is a sheet of the Japanese Foreign Ministry (paper marked 外務省), dated June 1916 by its place in the file. It carries two tables of digits, place by place (thousands, hundreds, tens, units), under the heading 9 8 7 6 5 4 3 2 1 0. Page 17 is the draft; page 18 is a syllable grid unrelated to these telegrams. We had never known which telegram they applied to<sup class="fn"><a href="sources.html#s27">[27]</a></sup>.</p>'
 '<h3>The two tables (transcription)</h3>' + t1 + t2 +
 '<p>The second table is the exact inverse of the first: one enciphers, the other deciphers. One cell of the second (tens, 6th) has a 6 overwritten with a 9; 6 is the only digit that completes the row, and the draft gives it.</p>'
 '<p><strong>The result.</strong> These tables read none of the telegrams already deciphered (共密, 容密, 辰密, 乾密), nor N03, N06 or N07. They read <a href="telegrams.html#tnum-N01">N01</a>, a telegram from Shanghai without prefix, received in Tokyo in May 1916: “轉克強先生：袁逆將倒，時局益艱……盼承指導，俾有遵循”, followed by some fifteen one-character signatures. The score is far above 200 shuffled controls.</p>'
 '<p><strong>A double confirmation.</strong> Shortly before, our search with S. Tomokiyo’s model (a renumbered 明密 book) had found for N01, without knowing these tables, a candidate key. It is identical, cell by cell, to the Ministry’s. Two independent reconstructions, one from June 1916 and one from October 2026, give the same key. The only difference is one of form: the tables, written digit by digit, cannot express the cyclic pages (labels 90 to 99) or row 10 (a 0 in the units), which the reading of the text requires.</p>'
 '<p><strong>What it tells us.</strong> In June 1916 the Japanese Foreign Ministry held the key to at least one channel between the Shanghai friends and Huang Xing. We do not know whether it broke it or obtained it otherwise. The other cryptanalysis sheets in the same file remain to be studied. Limits: one key, one telegram; in N01, 柬 is unresolved and several signatures are unidentified.</p></section>'),
'ja': lambda t1, t2: (
 '<section class="article" id="gaimusho"><h2>外務省が持っていた鍵：N01</h2>'
 '<p><strong>史料。</strong>電報と同じ綴りのB03050089200の16頁は外務省用紙で、綴りの位置から1916年6月のものと見られる。見出し「9 8 7 6 5 4 3 2 1 0」の下に、千位・百位・十位・一位ごとの数字表が2つ書かれている。17頁はその下書き、18頁はこれらの電報と関係のない音節表である。どの電報に当たるのか、これまで分かっていなかった<sup class="fn"><a href="sources.html#s27">[27]</a></sup>。</p>'
 '<h3>2つの表（翻字）</h3>' + t1 + t2 +
 '<p>第2表は第1表のちょうど逆で、一方が暗号化、他方が解読用である。第2表の1か所（十位の6番目）は6に9が重ね書きされているが、行を完成させるのは6だけで、下書きも6である。</p>'
 '<p><strong>結果。</strong>この表は既解読の電報（共密・容密・辰密・乾密）もN03・N06・N07も読めない。読めるのは<a href="telegrams.html#tnum-N01">N01</a>、1916年5月に東京で受信した前置きのない上海からの電報で、「轉克強先生：袁逆將倒，時局益艱……盼承指導，俾有遵循」と読め、一字の署名が15ほど続く。値は攪拌した対照200通を大きく上回る。</p>'
 '<p><strong>二重の確認。</strong>その少し前、私たちはS. Tomokiyo氏のモデル（番号を付け替えた明密電碼本）による探索で、この表を知らずにN01の候補鍵を得ていた。それは外務省の表と升目ごとに一致する。1916年6月と2026年10月の独立した二つの復元が同じ鍵を与えたのである。違いは形式だけで、数字ごとに書かれた表は、本文の読みが必要とする循環する頁（90〜99）と10行目（一の位の0）を書き表せない。</p>'
 '<p><strong>意味するもの。</strong>外務省は1916年6月、上海の同志と黄興の間の少なくとも一つの通信経路の鍵を持っていた。解読したのか、別の方法で入手したのかは分からない。同じ綴りの他の解読用紙は今後の課題である。限界：鍵は一つ、電報は1通。N01の「柬」は未解決で、署名の多くは未比定。</p></section>'),
'zh-hant': lambda t1, t2: (
 '<section class="article" id="gaimusho"><h2>日本外務省掌握的密鑰：N01</h2>'
 '<p><strong>史料。</strong>與電報同一卷宗的B03050089200第16頁，是日本外務省用紙，據其在卷宗中的位置當屬1916年6月。上有兩張數字表，按千位、百位、十位、個位排列，表頭為「9 8 7 6 5 4 3 2 1 0」。第17頁是其草稿，第18頁是與這些電報無關的音節表。過去不知道它們對應哪一封電報<sup class="fn"><a href="sources.html#s27">[27]</a></sup>。</p>'
 '<h3>兩張表（謄錄）</h3>' + t1 + t2 +
 '<p>第二表恰是第一表的逆：一張用於加密，一張用於解讀。第二表有一格（十位第6格）是6上加寫9；只有6能補全該行，草稿亦作6。</p>'
 '<p><strong>結果。</strong>此表讀不出任何已破譯的電報（共密、容密、辰密、乾密），也讀不出N03、N06、N07；它讀出的是<a href="telegrams.html#tnum-N01">N01</a>：1916年5月東京收到、無前綴的上海來電，「轉克強先生：袁逆將倒，時局益艱……盼承指導，俾有遵循」，後附約十五個單字署名。分數遠高於200個打亂的對照。</p>'
 '<p><strong>雙重確認。</strong>稍早，我們依S. Tomokiyo的模型（重新編號的明密電碼本）搜尋，在不知此表的情況下已得出N01的候選密鑰，與外務省的表逐格相同：1916年6月與2026年10月兩次獨立的復原，得出同一把密鑰。差別只在形式：逐位書寫的表無法表示循環的頁（90至99）與第10行（個位的0），而讀通全文需要它們。</p>'
 '<p><strong>意義。</strong>1916年6月，日本外務省至少掌握了上海同人與黃興之間一條通訊線路的密鑰；是破譯還是另行取得，尚不可知。同一卷宗中的其他解讀用紙有待研究。局限：一把密鑰、一封電報；N01的「柬」未解，多數署名未比定。</p></section>'),
}
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import c1916_i18n as C
    T2t = C.t2s_table(WENMI)
    for L in ('fr', 'en', 'ja', 'zh-hant', 'zh-hans'):
        f = S['zh-hant'] if L == 'zh-hans' else S[L]
        sec = f(table(T1, LAB), table(T2, LAB))
        if L == 'zh-hans':
            sec = C.to_hans(sec, T2t).replace('干密', '乾密')
        p = os.path.join(SITE, 'content', L, 'method.html'); s = open(p, encoding='utf-8').read()
        s = re.sub(r'\n  <section class="article" id="gaimusho">.*?</section>', '', s, flags=re.S)
        i = s.find('id="qianmi"'); assert i > 0, L
        j = s.find('</section>', i) + len('</section>')
        s = s[:j] + '\n  ' + sec + s[j:]
        open(p, 'w', encoding='utf-8').write(s)
    print('method: section 外務省 / N01 (5 langues)')
