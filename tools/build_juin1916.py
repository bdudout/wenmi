#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Article « Juin 1916 : ce que disent les télégrammes de Huang Xing » (content/<langue>/juin1916.html, 5 langues)
et source [29] (édition 黃興等電稿). Idempotent. Le chinois simplifié est dérivé du traditionnel (c1916_i18n.to_hans)."""
import os, re, sys
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1916_i18n as C
WENMI = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'wenmi'))

def tg(n):  # lien vers une fiche de la page Télégrammes (N04, N34 : en clair, pas encore de fiche)
    return f'<a href="telegrams.html#tnum-{n}">{n}</a>'
def S(*n):
    return '<sup class="fn">' + ''.join(f'<a href="sources.html#s{x}">[{x}]</a>' for x in n) + '</sup>'
def Q(zh):
    return f'<span lang="zh-Hant">{zh}</span>'
def unc(t):
    return f'<mark class="unc">{t}</mark>'

FR = f'''<!-- {{"title": "Juin 1916 : ce que disent les télégrammes de Huang Xing", "description": "Ce que vingt télégrammes chiffrés de juin 1916, déchiffrés en octobre 2026, apprennent sur Huang Xing, le Japon, le Zhejiang et le retour à la Constitution de 1912 après la mort de Yuan Shikai."}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">Histoire · Juin 1916</p>
    <h1>Juin 1916 : ce que disent les télégrammes de Huang Xing</h1>
    <p class="standfirst">Yuan Shikai meurt le 6 juin 1916. Pendant les dix jours qui suivent, Huang Xing, à Tokyo, et ses amis de Shanghai échangent des télégrammes chiffrés que la police japonaise recopie. Déchiffrés en octobre 2026, ils éclairent une période que l’on connaissait mal : la négociation avec Pékin, l’achat d’armes au Japon pour le Zhejiang et la position japonaise sur les emprunts.</p>
    <p class="byline">Brice Dudout, avec Claude (Anthropic). Octobre 2026.</p>
  </header>

  <h2 id="corpus">Un trou dans les archives</h2>
  <p>Les brouillons des télégrammes de Huang Xing pour mai–octobre 1916, conservés par l’historien Hsueh Chun-tu (薛君度), ont été publiés en Chine sous le titre {Q("黃興等電稿")} : 126 pièces, présentées comme inédites jusque-là{S(29)}. Entre la pièce du 8 juin et celle du 20 juin, elles ne contiennent <strong>rien</strong>. Or les télégrammes interceptés au Japon et déchiffrés ici ({Q("容密")}, {Q("共密")}) sont datés, pour la plupart, du 8 au 16 juin{S(25, 27)} : ils tombent exactement dans ce trou. Nous n’avons retrouvé aucun de leurs textes dans cette édition ni en ligne ; une vérification dans le recueil {Q("黃興集")} et dans les correspondances de Li Yuanhong reste à faire.</p>
  <p>L’édition de 1916 confirme aussi le contexte des nôtres : Huang Xing y répond le 20 juin aux télégrammes {Q("寒")} (14) et {Q("洽")} de Li Yuanhong — le premier est {tg("N34")}, que nous lisons en clair ; la pièce du 8 juin, signée Yin Ruli, Ge Jing’en et Huang Fu, annonce la réunion « chez Tang » dont {tg("N24")} donne la suite.</p>

  <h2 id="codes">Un code par correspondant</h2>
  <p>Les brouillons publiés notent, en tête de chaque télégramme, le nom du code employé : {Q("辰密")} pour Zeng Jiwu (曾繼梧) au Hunan, {Q("共密")} pour Li Shucheng et Chen Jiahui, {Q("安密")} pour Tan Yankai, {Q("嚴密")} pour Peng Yunyi, etc.{S(29)} Les préfixes en clair des formulaires interceptés ({Q("容密")}, {Q("共密")}, {Q("辰密")}, {Q("和密")}, {Q("乾密")}) sont donc les noms de livres de chiffrement attribués à des correspondants. Cela explique pourquoi chaque famille a sa propre clé, et pourquoi la clé de {Q("辰密")} reste à trouver : elle n’a rien à voir avec les deux autres.</p>

  <h2 id="japon">Le Japon : des armes, des emprunts, et une condition</h2>
  <p>Les télégrammes {Q("容密")} de Zhang Xiaozhun (張孝準), ancien élève de l’École des officiers de Tokyo installé près de Huang Xing, détaillent une commande d’armes japonaises pour le Zhejiang, dont le gouverneur militaire Lü Gongwang est en poste depuis le 6 mai : environ dix mille fusils, une dizaine de canons de montagne, des mitrailleuses ({tg("N02")}, {tg("N12")}) ; des munitions comptées par pièce ({tg("N21")}) ; un paiement promis « avant le 30 juin » ({tg("N36")}). Le financement passe par un emprunt d’un million proposé par un intermédiaire nommé {Q("芳川")} ({tg("N12")}) et par l’emprunt de cinq millions du Conseil des affaires militaires de Zhaoqing ({tg("N02")}). Le Zhejiang offre en gage ses taxes sur le tabac (environ 280 000 et 140 000 par an) et juge sa taxe sur l’alcool (environ 900 000) trop précieuse ({tg("N25")}) ; il envoie un émissaire, Wu Zhaolian, au Japon ({tg("N25")}, {tg("N36")}).</p>
  <p>Surtout, Huang Xing affirme à deux reprises que les autorités japonaises ont décidé de ne pas prêter au gouvernement de Pékin tant que le Nord et le Sud ne seront pas unifiés ({tg("N17")}, 10 juin ; {tg("N19b")}, 11 juin){S(25, 27)}. Le 20 juin, il écrit pourtant au Conseil des affaires militaires que « l’emprunt n’a pas abouti, les autorités japonaises restant dans l’expectative »{S(29)} : la promesse de juin n’a pas suffi. {unc("L’identité de « 芳川 » et celle de Wu Zhaolian ne sont pas établies.")}</p>

  <h2 id="constitution">Le retour à la Constitution de 1912</h2>
  <p>Dès le 10 juin, Huang Xing fixe cinq conditions pour Li Yuanhong : rétablir la Constitution provisoire de 1912 et l’ancien Parlement, refuser toute amnistie, faire démissionner le cabinet de Duan Qirui, déplacer Wang Zhanyuan, faire venir à Pékin les chefs républicains ({tg("N17")}). Le lendemain, il ajoute qu’« une solution juridique n’aura aucun effet sans force armée pour l’appuyer », demande au Zhejiang d’être « le pilier du Sud-Est » et à Lu Rongting et Li Liejun de marcher sur le Hubei et le Jiangxi ({tg("N19b")}).</p>
  <p>À Shanghai, le groupe de Huang Fu raconte la suite ({tg("N24")}) : Li Yuanhong invite les notables à Pékin ; on pense à y envoyer Tang Hualong, Gu Zhongxiu, Zhang Ji et Fan Yuanlian à titre personnel ; puis on décide que Tang Shaoyi et Tang Hualong répondront qu’ils ne viendront pas tant qu’un ordre n’aura pas aboli les lois de Yuan et rétabli la Constitution de 1912. Zhang Guogan, secrétaire général de la présidence, télégraphie que Duan y consent ; Tang Hualong part pour Pékin le soir même. Le 14, Li Yuanhong répond lui-même à Huang Xing ({tg("N34")}) : il rappelle leur combat commun à Wuhan en 1911 ({Q("陽夏同舟")}), lui demande de « le soutenir et de corriger ses erreurs », et promet de consulter le pays sur les « grandes affaires de l’État ». Le 16, Huang Xing met encore en garde contre une manœuvre de Pékin pour réviser la Constitution par des délégués des provinces et contre Duan, qui « reprend les vieilles ruses de Yuan » ({tg("N35")}). La Constitution de 1912 est rétablie le 29 juin.</p>

  <h2 id="autres">Autres éclairages</h2>
  <ul>
    <li>Sun Yat-sen ordonne par télégramme à ses troupes de cesser le combat ; sa réponse publiée dans la presse inquiète les amis de Huang Xing ({tg("N32")}).</li>
    <li>Huang Xing soutient l’armée du Shaanxi et pousse les provinces indépendantes à marcher vers le nord ({tg("N04")}, en clair).</li>
    <li>Les intermédiaires japonais : le consul Koike et le consul général Ariyoshi ({tg("N30")}), Tanaka et Aoki ({tg("N23")}) {unc("— identifications probables, non démontrées")}.</li>
  </ul>

  <h2 id="limites">Limites</h2>
  <p>Les clés sont reconstruites, pas retrouvées dans un livre de code ; tous les chiffres ont été relus par Brice Dudout sur les scans, mais quelques caractères restent non résolus et les traductions sont des propositions. Les points ci-dessus ne prétendent pas à la nouveauté absolue : ils n’apparaissent ni dans l’édition des brouillons de Huang Xing ni dans les sources consultées en ligne, ce qui ne prouve pas qu’ils soient inconnus des historiens. Textes, clés et scans : pages <a href="rongmi.html">容密</a>, <a href="gongmi.html">共密</a> et <a href="telegrams.html#grp-numeric">Télégrammes</a>.</p>
</article>
'''

EN = f'''<!-- {{"title": "June 1916: what Huang Xing’s telegrams say", "description": "What twenty cipher telegrams of June 1916, deciphered in October 2026, tell us about Huang Xing, Japan, Zhejiang and the return to the 1912 Constitution after Yuan Shikai’s death."}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">History · June 1916</p>
    <h1>June 1916: what Huang Xing’s telegrams say</h1>
    <p class="standfirst">Yuan Shikai died on 6 June 1916. In the ten days that followed, Huang Xing in Tokyo and his friends in Shanghai exchanged cipher telegrams that the Japanese police copied. Deciphered in October 2026, they shed light on a little-known period: the bargaining with Beijing, the purchase of Japanese arms for Zhejiang, and Japan’s position on loans.</p>
    <p class="byline">Brice Dudout, with Claude (Anthropic). October 2026.</p>
  </header>

  <h2 id="corpus">A gap in the record</h2>
  <p>The drafts of Huang Xing’s telegrams for May–October 1916, kept by the historian Hsueh Chun-tu (薛君度), were published in China as {Q("黃興等電稿")}: 126 pieces, described as previously unpublished{S(29)}. Between the piece of 8 June and that of 20 June they contain <strong>nothing</strong>. The telegrams intercepted in Japan and deciphered here ({Q("容密")}, {Q("共密")}) are mostly dated 8 to 16 June{S(25, 27)}: they fall exactly into that gap. We found none of their texts in that edition or online; the {Q("黃興集")} collection and Li Yuanhong’s correspondence still have to be checked.</p>
  <p>The edition also confirms their context: on 20 June Huang Xing answers Li Yuanhong’s telegrams {Q("寒")} (14th) and {Q("洽")} — the first is {tg("N34")}, which we read in clear; the piece of 8 June, signed Yin Ruli, Ge Jing’en and Huang Fu, announces the meeting “at Tang’s house” whose sequel is {tg("N24")}.</p>

  <h2 id="codes">One code per correspondent</h2>
  <p>The published drafts record, at the head of each telegram, the name of the code used: {Q("辰密")} for Zeng Jiwu (曾繼梧) in Hunan, {Q("共密")} for Li Shucheng and Chen Jiahui, {Q("安密")} for Tan Yankai, {Q("嚴密")} for Peng Yunyi, and so on{S(29)}. The clear prefixes on the intercepted forms ({Q("容密")}, {Q("共密")}, {Q("辰密")}, {Q("和密")}, {Q("乾密")}) are therefore names of cipher books assigned to correspondents. This explains why each family has its own key, and why the {Q("辰密")} key is still to be found: it has nothing to do with the other two.</p>

  <h2 id="japon">Japan: arms, loans, and a condition</h2>
  <p>The {Q("容密")} telegrams of Zhang Xiaozhun (張孝準), a graduate of the Tokyo military academy working alongside Huang Xing, detail an order of Japanese arms for Zhejiang, whose military governor Lü Gongwang had taken office on 6 May: about ten thousand rifles, ten or so mountain guns, machine guns ({tg("N02")}, {tg("N12")}); ammunition counted per weapon ({tg("N21")}); payment promised “before 30 June” ({tg("N36")}). Funding comes from a one-million loan offered by an intermediary named {Q("芳川")} ({tg("N12")}) and from the five-million loan of the Military Affairs Council at Zhaoqing ({tg("N02")}). Zhejiang offers its tobacco taxes as security (about 280,000 and 140,000 a year) and judges its wine tax (about 900,000) too valuable ({tg("N25")}); it sends an envoy, Wu Zhaolian, to Japan ({tg("N25")}, {tg("N36")}).</p>
  <p>Above all, Huang Xing twice states that the Japanese authorities have decided not to lend to the Beijing government until North and South are unified ({tg("N17")}, 10 June; {tg("N19b")}, 11 June){S(25, 27)}. Yet on 20 June he writes to the Military Affairs Council that “the loan has failed, the Japanese authorities remaining in wait-and-see”{S(29)}: the June promise was not enough. {unc("The identity of “芳川” and of Wu Zhaolian is not established.")}</p>

  <h2 id="constitution">The return to the 1912 Constitution</h2>
  <p>On 10 June Huang Xing sets five conditions for Li Yuanhong: restore the 1912 Provisional Constitution and the old Parliament, refuse any amnesty, make Duan Qirui’s cabinet resign, move Wang Zhanyuan, and bring the republican leaders to Beijing ({tg("N17")}). The next day he adds that “a legal solution will have no effect without armed force behind it”, asks Zhejiang to be “the pillar of the South-East”, and asks Lu Rongting and Li Liejun to march on Hubei and Jiangxi ({tg("N19b")}).</p>
  <p>In Shanghai, Huang Fu’s group reports what followed ({tg("N24")}): Li Yuanhong invites the notables to Beijing; Tang Hualong, Gu Zhongxiu, Zhang Ji and Fan Yuanlian are considered for a personal mission; then it is decided that Tang Shaoyi and Tang Hualong will answer that they will not come until an order abolishes Yuan’s laws and restores the 1912 Constitution. Zhang Guogan, the presidential secretary-general, wires that Duan agrees; Tang Hualong leaves for Beijing that evening. On the 14th Li Yuanhong himself answers Huang Xing ({tg("N34")}): he recalls their common fight at Wuhan in 1911 ({Q("陽夏同舟")}), asks him to “support him and correct his mistakes”, and promises to consult the country on “the great affairs of State”. On the 16th Huang Xing still warns against a Beijing manoeuvre to revise the Constitution through provincial delegates, and against Duan, “taking up Yuan’s old tricks” ({tg("N35")}). The 1912 Constitution was restored on 29 June.</p>

  <h2 id="autres">Other glimpses</h2>
  <ul>
    <li>Sun Yat-sen orders his troops by telegram to cease fighting; his reply, published in the press, worries Huang Xing’s friends ({tg("N32")}).</li>
    <li>Huang Xing backs the Shaanxi army and urges the independent provinces to march north ({tg("N04")}, in clear).</li>
    <li>Japanese go-betweens: Consul Koike and Consul General Ariyoshi ({tg("N30")}), Tanaka and Aoki ({tg("N23")}) {unc("— probable identifications, not proven")}.</li>
  </ul>

  <h2 id="limites">Limits</h2>
  <p>The keys are reconstructions, not taken from a code book; every digit was re-read on the scans by Brice Dudout, but a few characters remain unresolved and the translations are proposals. The points above do not claim absolute novelty: they appear neither in the edition of Huang Xing’s drafts nor in the sources consulted online, which does not prove that historians do not know them. Texts, keys and scans: the <a href="rongmi.html">Rongmi</a>, <a href="gongmi.html">Gongmi</a> and <a href="telegrams.html#grp-numeric">Telegrams</a> pages.</p>
</article>
'''

HANT = f'''<!-- {{"title": "1916年6月：黃興電報所見", "description": "2026年10月破譯的1916年6月二十封密電，對黃興、日本、浙江以及袁世凱死後恢復元年約法的新見。"}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">歷史·1916年6月</p>
    <h1>1916年6月：黃興電報所見</h1>
    <p class="standfirst">1916年6月6日袁世凱死。其後十日間，在東京的黃興與上海友人往來密電，為日本警察抄錄。這些電報於2026年10月破譯，照亮了一段鮮為人知的時期：與北京的交涉、為浙江在日本購械，以及日本對借款的態度。</p>
    <p class="byline">Brice Dudout，與 Claude（Anthropic）合作。2026年10月。</p>
  </header>

  <h2 id="corpus">檔案中的空白</h2>
  <p>黃興1916年5月至10月的電稿，由薛君度保存，後以《黃興等電稿》為題在中國發表，共126件，稱此前從未發表{S(29)}。其中6月8日一件與6月20日一件之間<strong>別無他件</strong>。而本站破譯的日本截獲電報（容密、共密）大多在6月8日至16日之間{S(25, 27)}，恰好填補此一空白。我們在該書及網上均未找到其電文；《黃興集》與黎元洪函電尚待查核。</p>
  <p>該書亦印證其背景：6月20日黃興覆黎元洪「寒」（十四日）、「洽」兩電——前者即{tg("N34")}，本站可直接讀出；6月8日殷汝驪、葛敬恩、黃郛來電提及「唐宅會議」，其後續見{tg("N24")}。</p>

  <h2 id="codes">一位通信者一種密碼</h2>
  <p>已發表的電稿在每電之首註明所用密碼之名：致湖南曾繼梧用「辰密」，李書城、陳嘉會用「共密」，譚延闓用「安密」，彭允彝用「嚴密」等{S(29)}。截獲電報紙上的明文前綴（容密、共密、辰密、和密、乾密）因此是分配給各通信者的密碼本名稱。這解釋了為何各系統各有其密鑰，也解釋了「辰密」的密鑰為何仍未找到：它與另外兩種毫無關係。</p>

  <h2 id="japon">日本：軍械、借款與條件</h2>
  <p>張孝準（日本陸軍士官學校出身，在黃興身邊）的容密電報詳述為浙江向日本訂購軍械：浙江督軍呂公望5月6日就任；步槍約萬枝，山砲十餘門，另有機槍（{tg("N02")}、{tg("N12")}）；每門、每挺彈藥數（{tg("N21")}）；代價准於「六月三十日以前」付清（{tg("N36")}）。經費來自經手人「芳川」所提百萬借款（{tg("N12")}）及肇慶軍務院五百萬借款（{tg("N02")}）。浙江以烟捐（全年約二十八萬及十四萬）作抵押，認為酒捐（約九十萬）不宜（{tg("N25")}），並派吳兆蓮赴日（{tg("N25")}、{tg("N36")}）。</p>
  <p>尤其重要的是，黃興兩次表示日本當局已決定非南北統一不借款於北京政府（{tg("N17")}，6月10日；{tg("N19b")}，6月11日）{S(25, 27)}。然而6月20日他致電軍務院稱「款事不成，實日當局意存觀望」{S(29)}：6月的承諾並不足夠。{unc("「芳川」與吳兆蓮的身分尚未確定。")}</p>

  <h2 id="constitution">恢復元年約法</h2>
  <p>6月10日，黃興向黎元洪提出五項主張：恢復舊約法及國會，勿發赦令，使段祺瑞內閣辭職，將王占元調開，招民黨要人入京（{tg("N17")}）。翌日又稱「惟求法律上之解決，非有充實武力為之後援，必無効果」，望浙省「作東南之砥柱」，並請陸榮廷、李烈鈞速出鄂贛（{tg("N19b")}）。</p>
  <p>上海黃郛等人報告其後經過（{tg("N24")}）：黎元洪電邀滬上巨公入京；初議請湯化龍、谷鍾秀、張繼、范源濂以個人名義入京；後決定由唐紹儀、湯化龍覆電，非下令取消袁逆偽法、實行遵照元年約法，暫不入京。張國淦自京電告段已贊同；湯化龍當晚赴京。14日黎元洪親覆黃興（{tg("N34")}）：提及「往年陽夏同舟」，望其「左提右挈，糾繆繩愆」，並稱國家根本大計將謀及國人。16日黃興仍警告北京欲召各省代表議約法之策，及段「有襲袁故智之勢」（{tg("N35")}）。元年約法於6月29日恢復。</p>

  <h2 id="autres">其他</h2>
  <ul>
    <li>孫中山電令所部停兵；其覆電已登報，黃興友人以為宜慎（{tg("N32")}）。</li>
    <li>黃興支持陝軍，並促獨立各省北伐（{tg("N04")}，明碼）。</li>
    <li>日方中介：小池領事、有吉總領事（{tg("N30")}），田中、青木（{tg("N23")}）{unc("——可能的比定，尚未證實")}。</li>
  </ul>

  <h2 id="limites">局限</h2>
  <p>密鑰為復原所得，並非取自電碼本；全部數字已由 Brice Dudout 依掃描件複讀，但仍有少數字未解，譯文為推定。上述各點並不宣稱絕對首見：它們既不見於黃興電稿，也不見於網上所查資料，但這不證明史家未曾知悉。電文、密鑰與掃描件見<a href="rongmi.html">容密</a>、<a href="gongmi.html">共密</a>及<a href="telegrams.html#grp-numeric">電報全文</a>頁面。</p>
</article>
'''

JA = f'''<!-- {{"title": "1916年6月：黄興の電報が語ること", "description": "2026年10月に解読された1916年6月の暗号電報20通から、黄興・日本・浙江と、袁世凱死後の元年約法回復について分かること。"}} -->
<article class="article">
  <header class="lede">
    <p class="kicker">歴史・1916年6月</p>
    <h1>1916年6月：黄興の電報が語ること</h1>
    <p class="standfirst">1916年6月6日、袁世凱が死去した。その後の十日間、東京の黄興と上海の同志は暗号電報を交わし、日本の警察がそれを写し取った。2026年10月に解読されたこれらの電報は、北京との交渉、浙江のための日本での武器購入、借款をめぐる日本の態度という、あまり知られていない時期を照らし出す。</p>
    <p class="byline">Brice Dudout、Claude（Anthropic）との共同作業。2026年10月。</p>
  </header>

  <h2 id="corpus">史料の空白</h2>
  <p>薛君度が保存していた黄興の1916年5〜10月の電稿は『黄興等電稿』として中国で公刊された（126件、それまで未発表とされる）{S(29)}。そこには6月8日の一件と6月20日の一件の間に<strong>何もない</strong>。日本で傍受され本サイトで解読した電報（容密・共密）の大半は6月8〜16日付であり{S(25, 27)}、ちょうどこの空白に当たる。同書にもインターネット上にもその本文は見つからなかった。『黄興集』と黎元洪の函電の確認は今後の課題である。</p>
  <p>同書は背景も裏づける。6月20日、黄興は黎元洪の「寒」（14日）・「洽」両電に返電しているが、前者が{tg("N34")}（平文で読める）である。また6月8日の殷汝驪・葛敬恩・黄郛の電報は「唐宅の会議」を伝え、その続きが{tg("N24")}である。</p>

  <h2 id="codes">通信相手ごとの暗号</h2>
  <p>公刊された電稿は各電の冒頭に使用した暗号の名を記している。湖南の曾継梧には「辰密」、李書城・陳嘉会には「共密」、譚延闓には「安密」、彭允彝には「厳密」などである{S(29)}。傍受された用紙の平文の前置き（容密・共密・辰密・和密・乾密）は、通信相手ごとに割り当てられた暗号書の名なのである。各系統が独自の鍵を持つこと、そして「辰密」の鍵が他の二つと無関係でまだ見つからないことは、これで説明がつく。</p>

  <h2 id="japon">日本：武器、借款、そして条件</h2>
  <p>黄興のそばにいた張孝準（陸軍士官学校出身）の容密電報は、5月6日に就任した浙江督軍呂公望のための日本製武器の注文を詳しく伝える。小銃約一万挺、山砲十余門、機関銃（{tg("N02")}、{tg("N12")}）、一門・一挺あたりの弾薬数（{tg("N21")}）、代金は「6月30日までに」支払うとの約束（{tg("N36")}）。資金は仲介者「芳川」の提示する百万の借款（{tg("N12")}）と、肇慶軍務院の五百万の借款（{tg("N02")}）による。浙江は煙税（年約28万と14万）を担保とし、酒税（約90万）は適当でないとして（{tg("N25")}）、呉兆蓮を日本に派遣した（{tg("N25")}、{tg("N36")}）。</p>
  <p>とりわけ黄興は二度にわたり、日本当局が南北統一まで北京政府に借款しないと決めたと述べている（{tg("N17")}、6月10日、{tg("N19b")}、6月11日）{S(25, 27)}。しかし6月20日、彼は軍務院に「款事成らず、実に日本当局の観望による」と打電している{S(29)}。6月の約束だけでは足りなかった。{unc("「芳川」と呉兆蓮の身元は確定していない。")}</p>

  <h2 id="constitution">元年約法の回復</h2>
  <p>6月10日、黄興は黎元洪に対する五つの条件を示した。旧約法と旧国会の回復、赦令を出さないこと、段祺瑞内閣の辞職、王占元の転任、民党要人の北京招致である（{tg("N17")}）。翌日には「法律上の解決も、充実した武力の後ろ盾がなければ効果はない」と述べ、浙江に「東南の砥柱」となるよう、陸栄廷と李烈鈞には鄂・贛へ出兵するよう求めた（{tg("N19b")}）。</p>
  <p>上海の黄郛らはその後の経過を伝える（{tg("N24")}）。黎元洪は上海の名士を北京に招き、湯化龍・谷鍾秀・張継・范源濂を個人名義で派遣する案が出たが、結局、唐紹儀と湯化龍が「袁逆の偽法を取り消し元年約法の遵守を命じないかぎり北京には入らない」と返電することになった。総統府秘書長の張国淦は段の同意を北京から伝え、湯化龍はその晩北京へ向かった。14日、黎元洪自身が黄興に返電した（{tg("N34")}）。1911年の武漢での共闘（「陽夏同舟」）に触れ、「左提右挈、糾繆縄愆」を求め、国家の根本大計を国民に諮ると約した。16日にも黄興は、各省代表に約法を議させる北京の策と、「袁の故智を襲う」段への警戒を説いている（{tg("N35")}）。元年約法は6月29日に回復された。</p>

  <h2 id="autres">その他</h2>
  <ul>
    <li>孫文は電報で所部に停戦を命じ、新聞に出たその返電が黄興の同志を心配させた（{tg("N32")}）。</li>
    <li>黄興は陝西軍を支持し、独立各省に北伐を促した（{tg("N04")}、平文）。</li>
    <li>日本側の仲介者：小池領事と有吉総領事（{tg("N30")}）、田中と青木（{tg("N23")}）{unc("——推定であり、証明されていない")}。</li>
  </ul>

  <h2 id="limites">限界</h2>
  <p>鍵は復元であり電碼本から得たものではない。全数字はBrice Dudoutがスキャンで再読したが、いくつかの字は未解決で、翻訳は作業案である。以上の点は絶対の新発見を主張するものではない。黄興の電稿にもインターネット上の資料にも見当たらないが、それは歴史家が知らないことを意味しない。本文・鍵・スキャンは<a href="rongmi.html">容密</a>、<a href="gongmi.html">共密</a>、<a href="telegrams.html#grp-numeric">電報一覧</a>のページを参照。</p>
</article>
'''

S29 = {
 'fr': '« <span lang="zh-Hans">黄兴等电稿</span> » (télégrammes de Huang Xing et d’autres, mai–octobre 1916), éd. Yang Pengcheng (楊鵬程), <i><span lang="zh-Hans">近代史资料</span></i> (numéro non vérifié), d’après les brouillons donnés en 1981 par Hsueh Chun-tu (薛君度) à l’Institut d’histoire moderne de l’Académie chinoise des sciences sociales ; <a href="https://www.krzzjn.com/uploadfile/2020/0916/20200916120919469.pdf">scan en ligne</a>.',
 'en': '“<span lang="zh-Hans">黄兴等电稿</span>” (telegrams of Huang Xing and others, May–October 1916), ed. Yang Pengcheng (楊鵬程), <i><span lang="zh-Hans">近代史资料</span></i> (issue not verified), from the drafts given in 1981 by Hsueh Chun-tu (薛君度) to the Institute of Modern History, Chinese Academy of Social Sciences; <a href="https://www.krzzjn.com/uploadfile/2020/0916/20200916120919469.pdf">online scan</a>.',
 'ja': '「<span lang="zh-Hans">黄兴等电稿</span>」（黄興らの電報、1916年5〜10月）、楊鵬程整理、『<span lang="zh-Hans">近代史资料</span>』（号数未確認）。1981年に薛君度が中国社会科学院近代史研究所に寄贈した電稿による。<a href="https://www.krzzjn.com/uploadfile/2020/0916/20200916120919469.pdf">オンラインのスキャン</a>。',
 'zh-hant': '〈黃興等電稿〉（1916年5月至10月），楊鵬程整理，《近代史資料》（期號未核），據薛君度1981年贈中國社會科學院近代史研究所之電稿；<a href="https://www.krzzjn.com/uploadfile/2020/0916/20200916120919469.pdf">網上掃描件</a>。',
}

if __name__ == '__main__':
    T2 = C.t2s_table(WENMI)
    HANS = C.to_hans({'x': HANT}, T2)['x']
    HANS = HANS.replace('<span lang="zh-Hant">', '<span lang="zh-Hant">')  # termes cités gardés en traditionnel (déjà marqués)
    S29['zh-hans'] = C.to_hans({'x': S29['zh-hant']}, T2)['x']
    pages = {'fr': FR, 'en': EN, 'ja': JA, 'zh-hant': HANT, 'zh-hans': HANS}
    for L, body in pages.items():
        open(os.path.join(SITE, 'content', L, 'juin1916.html'), 'w', encoding='utf-8').write(body)
        p = os.path.join(SITE, 'content', L, 'sources.html'); s = open(p, encoding='utf-8').read()
        s = re.sub(r'\n    <li id="s29" value="29">.*?</li>', '', s)
        i = s.index('<li id="s28"'); j = s.index('</li>', i) + 5
        s = s[:j] + f'\n    <li id="s29" value="29">{S29[L]}</li>' + s[j:]
        open(p, 'w', encoding='utf-8').write(s)
    print('juin1916 : 5 langues ; source [29]')
