#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Article « Les livres X密 » (content/<langue>/ximi.html, 5 langues) : l'idée de S. Tomokiyo (livre 明密 renuméroté),
un code par correspondant, le télégramme 乾密 N09, ce qui résiste encore. Idempotent. Même gabarit que build_juin1916.py ;
le chinois simplifié est dérivé du traditionnel (c1916_i18n.to_hans), 乾密 rétabli après conversion."""
import os, sys
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1916_i18n as C
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))

def tg(n): return f'<a href="telegrams.html#tnum-{n}">{n}</a>'
def S(*n): return '<sup class="fn">' + ''.join(f'<a href="sources.html#s{x}">[{x}]</a>' for x in n) + '</sup>'
def Q(zh): return f'<span lang="zh-Hant">{zh}</span>'
def unc(t): return f'<mark class="unc">{t}</mark>'

FR = f'''<!-- {{"title": "Les livres X密 : un code par correspondant", "description": "Octobre 2026 : l’idée de S. Tomokiyo (des livres de code 明密 renumérotés à la main), un code par correspondant chez Huang Xing, et un télégramme de plus déchiffré, écrit au lendemain de la mort de Yuan Shikai."}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">Histoire · Octobre 2026</p>
    <h1>Les livres « X密 » : un code par correspondant</h1>
    <p class="standfirst">Les télégrammes numériques de juin 1916 portent en tête un nom de code : {Q('共密')}, {Q('容密')}, {Q('辰密')}… Satoshi Tomokiyo a montré qu’il ne s’agissait pas de calculs, mais de livres de code renumérotés à la main. Cette idée a permis de lire un télégramme de plus, écrit par Huang Xing au lendemain de la mort de Yuan Shikai.</p>
    <p class="byline">Brice Dudout, avec Claude (Anthropic), d’après une idée de Satoshi Tomokiyo. Octobre 2026.</p>
  </header>

  <h2 id="idee">L’idée de Satoshi Tomokiyo</h2>
  <p>Nous avions décrit nos trois clés numériques par des formules : une soustraction pour {Q('共密')}, des chiffres substitués puis une addition pour {Q('容密')}, des pages comptées à rebours sans zéro pour {Q('辰密')}. Le 23 octobre 2026, Satoshi Tomokiyo (site Cryptiana) a proposé de les relire comme l’employé de 1916 s’en servait : avec un exemplaire du code télégraphique « {Q('明密')} » dont on avait réécrit à la main les numéros de pages, de colonnes et de lignes{S(22)}. Il l’a montré sur un exemplaire de juin 1916 qu’il possède.</p>
  <p>Nous l’avons vérifié : pour les 10 000 groupes possibles, nos trois clés se ramènent exactement à trois renumérotations, une pour les pages, une pour les colonnes, une pour les lignes. Il ne reste aucune retenue : ce que nous appelions « retenue » n’était que le caractère xxx0, rangé au bas de la colonne précédente. Une seule page divergeait, et le seul groupe concerné, dans {tg('N25')}, est en fait une inversion de deux chiffres. Corrigé, il donne {Q('一切')}. Chaque page de clé du site renvoie désormais à son idée.</p>

  <h2 id="correspondants">Un livre par correspondant</h2>
  <p>Les brouillons de Huang Xing publiés pour l’été 1916 nomment, en tête de chaque télégramme, le code employé{S(29)}. On y voit {Q('嚴密')} pour Peng Yunyi (彭允彝) à Pékin, {Q('辰密')} pour Zeng Jiwu (曾繼梧) à Changsha, et {Q('共密')} pour Chen Jiahui (陳嘉會) et Li Shucheng (李書城). Suivent {Q('仁密')} pour Gu Zhongxiu (谷鍾秀), {Q('信密')} et {Q('安密')} pour Tan Yankai (譚延闓), et {Q('箴密')} pour Sun Hongyi (孫洪伊). Satoshi Tomokiyo signale aussi que de nombreux livres « X密 » de 1913–1923 sont conservés à Taïwan{S(22)}.</p>
  <p>Son idée explique ce système. Chaque correspondant recevait le même livre imprimé, mais avec ses propres numéros, réécrits à la main. Distribuer une clé ne coûtait qu’un exemplaire et quelques heures de copie. En contrepartie, tout le secret tenait dans cette renumérotation : une fois le principe compris, chaque livre se casse comme les autres.</p>

  <h2 id="qianmi">{Q('乾密')} : le télégramme du lendemain</h2>
  <p>Nous avons donc appliqué le modèle aux télégrammes « X密 » encore illisibles, avec des contrôles fixés avant le calcul. L’un d’eux s’ouvre : <a href="qianmi.html">N09</a>, préfixé {Q('乾密')}, parti de la maison de Huang Xing à Tokyo (青山南町三ノ五三). La copie japonaise n’est pas datée, mais elle est rangée entre les télégrammes du 6 et du 9 juin{S(27)}.</p>
  <blockquote><p>{Q('袁死。此間態度未變，候交涉有望，再電告。興。')}<br>« Yuan est mort. Ici, l’attitude n’a pas changé ; j’attendrai que les négociations soient en bonne voie pour télégraphier de nouveau. Xing. »</p></blockquote>
  <p>C’est la première réaction de Huang Xing que nous ayons à la mort de Yuan Shikai, le 6 juin. Elle est sobre : la nouvelle ne change rien à Tokyo, et il ne relancera ses correspondants qu’avec du concret. Les « négociations » sont sans doute celles que racontent les télégrammes {Q('容密')} : des armes et des emprunts au Japon pour les provinces soulevées. La suite confirme ce jugement. Le 9 juin, dans {tg('N13')}, il écrit que « le Japon reste très attentiste » ; le 10, dans {tg('N17')}, que les autorités japonaises ne prêteront pas à Pékin avant l’unification du Nord et du Sud.</p>
  <p>L’adresse, en clair, demande de transmettre à « Ma et Geng, mes deux frères ». Ils ne sont pas identifiés. Pour Geng, une piste : dans une lettre du 1er juin 1916 publiée avec les brouillons, Sun Hongyi dit s’être concerté avec Zhang Ji, Bo Wenwei, {unc('耿鶴生')} et He Chengjun (何成濬), « hommes du parti qui ont des forces »{S(29)}. Le destinataire japonais, ジヨンシヨウ, habite comme le groupe hunanais l’avenue Joffre (霞飛路) de la concession française.</p>

  <h2 id="gaimusho">Le ministère japonais avait la clé de N01</h2>
  <p>Dans le même dossier, une feuille du ministère japonais des Affaires étrangères, de juin 1916, porte deux tables de chiffres rang par rang, l’une pour chiffrer, l’autre pour déchiffrer{S(27)}. Nous ne savions pas à quoi elles servaient. Elles lisent {tg('N01')}, un appel de Shanghai à Huang Xing reçu en mai : « {Q('袁逆將倒，時局益艱……盼承指導，俾有遵循')} » (« Yuan va tomber, la situation se tend… nous attendons vos directives »), signé d’une quinzaine de caractères (建 pour Niu Yongjian, 闓 pour Tan Yankai, 秀 pour Gu Zhongxiu, 驪 pour Yin Ruli…). Mieux : la clé que notre recherche avait trouvée pour N01, avec le modèle de Satoshi Tomokiyo et sans ces tables, est identique à celle du ministère. Le Japon lisait donc ce canal dès 1916 ; nous ignorons s’il en avait cassé ou obtenu la clé. Voir la <a href="method.html#gaimusho">méthode</a>.</p>

  <h2 id="resiste">Ce qui résiste encore</h2>
  <ul>
    <li><strong>N03</strong>, autre {Q('乾密')} parti de la même maison au début de juin, reste illisible avec la clé de N09 : autre jour, autre clé, ou chiffres fautifs.</li>
    <li><strong>N06</strong> ({Q('和密')}, onze groupes) est trop court ; <strong>N07</strong> ne s’ouvre pas avec ce modèle.</li>
  </ul>
  <p>Pour avancer, il faudrait d’autres télégrammes des mêmes livres. Les recueils de Taïwan signalés par Satoshi Tomokiyo, ou les livres eux-mêmes, en seraient le meilleur chemin.</p>

  <h2 id="limites">Prudence</h2>
  <p>La clé de N09 repose sur un seul télégramme de 17 groupes. Elle passe nos contrôles : un score nettement au-dessus des témoins, la signature attendue et une cohérence avec la date. Mais trois caractères restent des lectures probables : {Q('未')}, {Q('候')} et {Q('告')}. Les chiffres ont été relus deux fois sur l’image par Brice Dudout, la seconde fois en aveugle. Voir la <a href="method.html#qianmi">méthode</a> et la page <a href="qianmi.html">{Q('乾密')}</a>.</p>
</article>
'''

EN = f'''<!-- {{"title": "The X密 books: one code per correspondent", "description": "October 2026: S. Tomokiyo’s idea (明密 code books renumbered by hand), one code per correspondent around Huang Xing, and one more telegram deciphered, written just after Yuan Shikai’s death."}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">History · October 2026</p>
    <h1>The “X密” books: one code per correspondent</h1>
    <p class="standfirst">The numeric telegrams of June 1916 open with a code name: {Q('共密')}, {Q('容密')}, {Q('辰密')}… Satoshi Tomokiyo showed that these were not calculations but code books renumbered by hand. The idea made it possible to read one more telegram, written by Huang Xing just after Yuan Shikai’s death.</p>
    <p class="byline">Brice Dudout, with Claude (Anthropic), after an idea of Satoshi Tomokiyo. October 2026.</p>
  </header>

  <h2 id="idee">Satoshi Tomokiyo’s idea</h2>
  <p>We had described our three numeric keys with formulae: a subtraction for {Q('共密')}, substituted digits plus an addition for {Q('容密')}, pages counted backwards without zeros for {Q('辰密')}. On 23 October 2026 Satoshi Tomokiyo (Cryptiana website) proposed reading them as the 1916 clerk used them: with a copy of the “{Q('明密')}” telegraph code whose page, column and row numbers had been rewritten by hand{S(22)}. He showed it on a June 1916 copy in his possession.</p>
  <p>We checked it: over all 10,000 possible groups, our three keys reduce exactly to three renumberings, one for pages, one for columns, one for rows. No carry is left: what we called a “carry” was only the xxx0 character, placed at the foot of the previous column. Only one page diverged, and the one group concerned, in {tg('N25')}, is in fact two swapped digits. Corrected, it gives {Q('一切')}. Every key page on the site now points to his idea.</p>

  <h2 id="correspondants">One book per correspondent</h2>
  <p>Huang Xing’s drafts published for the summer of 1916 name the code used at the head of each telegram{S(29)}. They show {Q('嚴密')} for Peng Yunyi (彭允彝) in Beijing, {Q('辰密')} for Zeng Jiwu (曾繼梧) in Changsha, and {Q('共密')} for Chen Jiahui (陳嘉會) and Li Shucheng (李書城). Then come {Q('仁密')} for Gu Zhongxiu (谷鍾秀), {Q('信密')} and {Q('安密')} for Tan Yankai (譚延闓), and {Q('箴密')} for Sun Hongyi (孫洪伊). Satoshi Tomokiyo also notes that many “X密” books of 1913–1923 are preserved in Taiwan{S(22)}.</p>
  <p>His idea explains the system. Each correspondent received the same printed book, but with his own numbers, rewritten by hand. Handing out a key cost only one copy and a few hours of copying. In return, all the secrecy lay in that renumbering: once the principle is understood, each book breaks like the others.</p>

  <h2 id="qianmi">{Q('乾密')}: the telegram of the day after</h2>
  <p>So we applied the model to the “X密” telegrams that were still unreadable, with controls fixed before computing. One of them opens: <a href="qianmi.html">N09</a>, prefixed {Q('乾密')}, sent from Huang Xing’s house in Tokyo (青山南町三ノ五三). The Japanese copy is undated, but it is filed between the telegrams of 6 and 9 June{S(27)}.</p>
  <blockquote><p>{Q('袁死。此間態度未變，候交涉有望，再電告。興。')}<br>“Yuan is dead. Here the attitude has not changed; I shall wait until the negotiations look promising and cable again. Xing.”</p></blockquote>
  <p>This is the first reaction of Huang Xing to Yuan Shikai’s death (6 June) that we have. It is sober: the news changes nothing in Tokyo, and he will contact his correspondents again only with something concrete. The “negotiations” are probably those told in the {Q('容密')} telegrams: arms and loans in Japan for the provinces in revolt. What follows bears this out. On 9 June, in {tg('N13')}, he writes that “Japan is still waiting and seeing”; on the 10th, in {tg('N17')}, that the Japanese authorities will not lend to Beijing before North and South are unified.</p>
  <p>The address, in clear, asks for the message to be passed to “Ma and Geng, my two brothers”. They are not identified. For Geng, one lead: in a letter of 1 June 1916 published with the drafts, Sun Hongyi says he conferred with Zhang Ji, Bo Wenwei, {unc('耿鶴生')} and He Chengjun (何成濬), “men of the party who have forces”{S(29)}. The Japanese addressee, ジヨンシヨウ, lives, like the Hunanese group, on Avenue Joffre (霞飛路) in the French concession.</p>

  <h2 id="gaimusho">The Japanese Ministry had N01’s key</h2>
  <p>In the same file, a sheet of the Japanese Foreign Ministry from June 1916 carries two tables of digits, place by place, one to encipher and one to decipher{S(27)}. We did not know what they were for. They read {tg('N01')}, an appeal from Shanghai to Huang Xing received in May: “{Q('袁逆將倒，時局益艱……盼承指導，俾有遵循')}” (“Yuan is about to fall, the situation grows tense… we await your guidance”), signed with some fifteen characters (建 for Niu Yongjian, 闓 for Tan Yankai, 秀 for Gu Zhongxiu, 驪 for Yin Ruli…). Better still: the key our search had found for N01, with Satoshi Tomokiyo’s model and without these tables, is identical to the Ministry’s. Japan was therefore reading this channel in 1916; we do not know whether it broke or obtained the key. See the <a href="method.html#gaimusho">method</a>.</p>

  <h2 id="resiste">What still resists</h2>
  <ul>
    <li><strong>N03</strong>, another {Q('乾密')} telegram sent from the same house in early June, stays unreadable with N09’s key: another day, another key, or faulty digits.</li>
    <li><strong>N06</strong> ({Q('和密')}, eleven groups) is too short; <strong>N07</strong> does not open with this model.</li>
  </ul>
  <p>Further progress needs other telegrams in the same books. The collections in Taiwan mentioned by Satoshi Tomokiyo, or the books themselves, would be the best way.</p>

  <h2 id="limites">Caution</h2>
  <p>N09’s key rests on a single telegram of 17 groups. It passes our checks: a score well above the controls, the expected signature and consistency with the date. But three characters remain probable readings: {Q('未')}, {Q('候')} and {Q('告')}. The digits were re-read twice on the image by Brice Dudout, the second time blind. See the <a href="method.html#qianmi">method</a> and the <a href="qianmi.html">{Q('乾密')}</a> page.</p>
</article>
'''

HANT = f'''<!-- {{"title": "X密電碼本：一人一本", "description": "2026年10月：S. Tomokiyo的構想（手寫重新編號的明密電碼本）、黃興通訊中一人一本密碼，以及袁世凱死後黃興所發、新讀出的一封電報。"}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">歷史 · 2026年10月</p>
    <h1>「X密」電碼本：一人一本</h1>
    <p class="standfirst">1916年6月的數字電報開頭都有一個密碼名：{Q('共密')}、{Q('容密')}、{Q('辰密')}……Satoshi Tomokiyo指出，這些不是計算，而是手寫重新編號的電碼本。依此構想，我們又讀出一封電報，是黃興在袁世凱死後所發。</p>
    <p class="byline">Brice Dudout與Claude（Anthropic），據Satoshi Tomokiyo的構想。2026年10月。</p>
  </header>

  <h2 id="idee">Satoshi Tomokiyo的構想</h2>
  <p>我們原以公式描述三種數字密鑰：{Q('共密')}用減法，{Q('容密')}先換數字再加常數，{Q('辰密')}以不含零的數倒數編頁。2026年10月23日，Satoshi Tomokiyo（Cryptiana網站）提出按1916年電報員的用法來讀：用一本頁、列、行編號都經手寫改過的「{Q('明密')}」電碼本{S(22)}。他以自藏的1916年6月版加以圖示。</p>
  <p>我們作了驗證：在全部10,000個可能的組上，三種密鑰都精確地歸結為三種重新編號：頁、列、行各一。沒有剩餘的進位：我們所說的「進位」，只是排在前一列底端的xxx0字。唯一不合的一頁，涉及{tg('N25')}中的一組，其實是兩位數字互倒；改正後得「{Q('一切')}」。本站每個密鑰頁面都已註明他的構想。</p>

  <h2 id="correspondants">一人一本</h2>
  <p>已刊的1916年夏黃興電稿，在每封電報開頭註明所用密碼{S(29)}：{Q('嚴密')}致北京彭允彝，{Q('辰密')}致長沙曾繼梧，{Q('共密')}致陳嘉會、李書城。此外還有{Q('仁密')}致谷鍾秀，{Q('信密')}與{Q('安密')}致譚延闓，{Q('箴密')}致孫洪伊。Satoshi Tomokiyo又指出，臺灣保存有許多1913–1923年的「X密」電碼本{S(22)}。</p>
  <p>他的構想解釋了這一制度：每位通訊者拿到同一本印刷的電碼本，只是編號各自手寫改過。分發一把密鑰，只需一本書和幾小時的抄寫；代價是全部機密都在這重新編號上——原理一旦明白，每一本都能同樣破解。</p>

  <h2 id="qianmi">{Q('乾密')}：袁死之後的電報</h2>
  <p>於是我們把這一模型用於尚未讀出的「X密」電報，計算前即定下對照規程。其中一封打開了：<a href="qianmi.html">N09</a>，前綴{Q('乾密')}，自黃興東京寓所（青山南町三ノ五三）發出。日方抄件無日期，但夾在6日與9日的電報之間{S(27)}。</p>
  <blockquote><p>{Q('袁死。此間態度未變，候交涉有望，再電告。興。')}</p></blockquote>
  <p>這是我們所見黃興對袁世凱之死（6月6日）的第一個反應，語氣冷靜：消息並未改變東京的情勢，有了實際結果才再聯絡。所說「交涉」，大概就是{Q('容密')}電報所記在日本為起義各省購械借款之事。其後的電報印證了這一判斷：6月9日的{tg('N13')}說「日態度頗觀望」，10日的{tg('N17')}說日本當局在南北統一前不借款予北京。</p>
  <p>電文地址為明碼，「轉馬、耿兩兄」，二人未比定。關於耿，有一條線索：與電稿同刊的孫洪伊1916年6月1日函，說曾與張溥泉、柏烈武、{unc('耿鶴生')}、何成濬諸君再四磋商，「皆民黨中確有實力之人」{S(29)}。日方記錄的收報人「ジヨンシヨウ」，與湘籍諸人一樣住在法租界霞飛路。</p>

  <h2 id="gaimusho">日本外務省握有N01的密鑰</h2>
  <p>同一卷宗中，有一張1916年6月的日本外務省用紙，上有兩張按位排列的數字表，一張加密，一張解讀{S(27)}。過去不知其用途。它們讀出了{tg('N01')}：5月收到的上海致黃興呼籲，「{Q('袁逆將倒，時局益艱……盼承指導，俾有遵循')}」，附約十五個單字署名（建＝鈕永建，闓＝譚延闓，秀＝谷鍾秀，驪＝殷汝驪……）。更有甚者：我們依Satoshi Tomokiyo的模型、在不知此表時為N01找到的密鑰，與外務省的表完全相同。可見日本早在1916年已能讀這條線路；是破譯還是取得密鑰，尚不可知。見<a href="method.html#gaimusho">破譯方法</a>。</p>

  <h2 id="resiste">仍未讀出的</h2>
  <ul>
    <li><strong>N03</strong>：六月初自同一寓所發出的另一封{Q('乾密')}，用N09的密鑰仍不可讀——另一日、另一把鑰匙，或數字有誤。</li>
    <li><strong>N06</strong>（{Q('和密')}，十一組）太短；<strong>N07</strong>用此模型打不開。</li>
  </ul>
  <p>要再前進，需要同一批電碼本的其他電報；Satoshi Tomokiyo提到的臺灣藏本，或電碼本本身，是最好的途徑。</p>

  <h2 id="limites">審慎</h2>
  <p>N09的密鑰只建立在一封17組的電報上。它通過了我們的檢驗：分數明顯高於對照，有預期的署名，與日期相符。但有三字仍是推定讀法（{Q('未')}、{Q('候')}、{Q('告')}）；數字由Brice Dudout在影像上複讀兩次，第二次為盲讀。見<a href="method.html#qianmi">破譯方法</a>與<a href="qianmi.html">{Q('乾密')}</a>頁面。</p>
</article>
'''

JA = f'''<!-- {{"title": "X密の電碼本：相手ごとに一冊", "description": "2026年10月：S. Tomokiyo氏の着想（手書きで番号を付け替えた明密電碼本）、黄興の通信相手ごとの暗号、そして袁世凱の死の直後に黄興が送った電報1通の新解読。"}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">歴史 · 2026年10月</p>
    <h1>「X密」の電碼本：相手ごとに一冊</h1>
    <p class="standfirst">1916年6月の数字電報は、冒頭に暗号名を掲げる：{Q('共密')}、{Q('容密')}、{Q('辰密')}……。Satoshi Tomokiyo氏は、これらが計算ではなく、手書きで番号を付け替えた電碼本であることを示した。この着想で、袁世凱の死の直後に黄興が送った電報がもう1通読めた。</p>
    <p class="byline">Brice Dudout、Claude（Anthropic）と共同、Satoshi Tomokiyo氏の着想にもとづく。2026年10月。</p>
  </header>

  <h2 id="idee">Satoshi Tomokiyo氏の着想</h2>
  <p>私たちは三つの数字鍵を式で記述していた：{Q('共密')}は引き算、{Q('容密')}は数字の置換と加算、{Q('辰密')}は0を含まない数で逆に数えた頁。2026年10月23日、Satoshi Tomokiyo氏（Cryptiana）は、1916年の電信係の使い方で読み直すことを提案した。頁・列・行の番号を手書きで書き換えた「{Q('明密')}」電碼本を使ったというのである{S(22)}。同氏は所蔵する1916年6月版でそれを示した。</p>
  <p>私たちはこれを確かめた。10,000通りのすべての組で、三つの鍵は頁・列・行それぞれの番号の付け替えに正確に帰着し、繰り上がりは残らない。「繰り上がり」と呼んでいたのは、前の列の最下段に置かれたxxx0の字にすぎなかった。食い違う頁は一つだけで、それにかかわる{tg('N25')}の1組は、実は隣接2桁の入れ替えだった。直すと「{Q('一切')}」になる。本サイトの鍵の各ページは、いまは同氏の着想に言及している。</p>

  <h2 id="correspondants">相手ごとに一冊</h2>
  <p>刊行された1916年夏の黄興電稿は、各電報の冒頭に用いた暗号の名を記している{S(29)}。北京の彭允彝には{Q('嚴密')}、長沙の曾繼梧には{Q('辰密')}、陳嘉會・李書城には{Q('共密')}を用いる。さらに谷鍾秀には{Q('仁密')}、譚延闓には{Q('信密')}と{Q('安密')}、孫洪伊には{Q('箴密')}がある。同氏はまた、1913〜1923年の「X密」電碼本が台湾に多数保存されていると指摘している{S(22)}。</p>
  <p>同氏の着想はこの仕組みを説明する。相手はみな同じ印刷本を受け取り、番号だけを手で書き換えたものを持つ。鍵を配るには本1冊と数時間の書き写しで足りた。その代わり秘密はこの付け替えだけにあり、原理が分かれば、どの本も同じように破れる。</p>

  <h2 id="qianmi">{Q('乾密')}：翌日の電報</h2>
  <p>そこで私たちは、計算前に対照の手順を定め、このモデルを未解読の「X密」電報に適用した。1通が開いた。<a href="qianmi.html">N09</a>である。前置きは{Q('乾密')}で、東京の黄興宅（青山南町三ノ五三）から出ている。日本側の写しに日付はないが、6日と9日の電報の間に綴じられている{S(27)}。</p>
  <blockquote><p>{Q('袁死。此間態度未變，候交涉有望，再電告。興。')}<br>「袁死す。当地の態度は変わらない。交渉に望みが出るのを待って、改めて打電する。興」</p></blockquote>
  <p>袁世凱の死（6月6日）に対する黄興の反応として、私たちが手にする最初のものである。調子は冷静で、知らせは東京では何も変えず、具体的な成果が出てから連絡するという。「交渉」はおそらく、{Q('容密')}電報が伝える、蜂起した諸省のための日本での武器購入と借款である。その後の電報もこの判断を裏づける。6月9日の{tg('N13')}は「日本はなお観望」と書き、10日の{tg('N17')}は、日本当局は南北統一まで北京に貸さないと述べる。</p>
  <p>平文のあて先には「馬・耿の両兄に転送」とある。二人は未比定である。耿については手がかりがある。電稿とともに刊行された1916年6月1日付の孫洪伊の書簡に、張溥泉・柏烈武・{unc('耿鶴生')}・何成濬の諸君と再三協議したとあり、「みな民党中の実力ある人」とされる{S(29)}。日本側が記した受信人「ジヨンシヨウ」は、湖南派と同じくフランス租界の霞飛路に住んでいる。</p>

  <h2 id="gaimusho">外務省はN01の鍵を持っていた</h2>
  <p>同じ綴りに、1916年6月の外務省用紙があり、桁ごとの数字表が2つ（暗号化用と解読用）書かれている{S(27)}。用途はこれまで不明だった。この表で読めるのは{tg('N01')}、5月に受信した上海から黄興への呼びかけである：「{Q('袁逆將倒，時局益艱……盼承指導，俾有遵循')}」。一字の署名が15ほど続く（建＝鈕永建、闓＝譚延闓、秀＝谷鍾秀、驪＝殷汝驪など）。さらに、私たちがSatoshi Tomokiyo氏のモデルで、この表を知らずにN01について得た鍵は、外務省の表と完全に一致する。日本は1916年にこの経路を読んでいたことになる。解読したのか入手したのかは分からない。<a href="method.html#gaimusho">方法</a>参照。</p>

  <h2 id="resiste">まだ読めないもの</h2>
  <ul>
    <li><strong>N03</strong>：6月初めに同じ家から出た別の{Q('乾密')}電報。N09の鍵では読めない。日が違うのか、鍵が別なのか、数字が誤っているのか。</li>
    <li><strong>N06</strong>（{Q('和密')}、11組）は短すぎる。<strong>N07</strong>はこのモデルでは開かない。</li>
  </ul>
  <p>先へ進むには、同じ電碼本による別の電報が必要である。Satoshi Tomokiyo氏の言う台湾の所蔵本、あるいは電碼本そのものが、最良の道だろう。</p>

  <h2 id="limites">留意点</h2>
  <p>N09の鍵は、17組の電報1通だけにもとづく。検証は通っている。対照をはっきり上回る値、期待どおりの署名、日付との整合である。ただし3字（{Q('未')}・{Q('候')}・{Q('告')}）は推定読みである。数字はBrice Dudoutが画像上で2回、2回目は盲検で読み直した。<a href="method.html#qianmi">方法</a>と<a href="qianmi.html">{Q('乾密')}</a>のページを参照。</p>
</article>
'''

if __name__ == '__main__':
    T2 = C.t2s_table(WENMI)
    HANS = C.to_hans({'x': HANT}, T2)['x'].replace('干密', '乾密')
    for L, body in {'fr': FR, 'en': EN, 'ja': JA, 'zh-hant': HANT, 'zh-hans': HANS}.items():
        open(os.path.join(SITE, 'content', L, 'ximi.html'), 'w', encoding='utf-8').write(body)
    print('ximi : 5 langues')
