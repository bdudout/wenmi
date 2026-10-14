# -*- coding: utf-8 -*-
"""Textes des télégrammes à condensateur de 1916 (page « Télégrammes ») : libellés, dates et traductions de travail.
Les traductions sont des traductions de travail, faites à partir du texte décodé et rectifié ; « […] » = passage non traduit
faute de lecture sûre ; « (?) » = identification ou lecture incertaine. Le chinois simplifié est dérivé du traditionnel
(table OpenCC STCharacters du dossier d'enquête, inversée)."""
import os

MONTHS_FR = ['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin']
MONTHS_EN = ['', 'January', 'February', 'March', 'April', 'May', 'June']
SUP = '<sup class="fn"><a href="sources.html#s1">[1, 2]</a></sup>'

LAB = {
 'fr': dict(
  title='Télégrammes à condensateur, mars–mai 1916',
  intro=('<p>Avant le <span lang="zh-Hant">文密</span>, de mars à mai 1916, le cercle de Sun Yat-sen chiffrait ses télégrammes avec des '
         '« condensateurs » plus simples : chaque syllabe de deux lettres donne deux chiffres, deux syllabes un code télégraphique chinois. '
         'Ces télégrammes ont été déchiffrés et publiés' + SUP + '. Nous donnons ici, au même format que le Wenmi, les {tels} télégrammes '
         'dont la relecture des scans a corrigé ou vérifié au moins un caractère (détail : <a href="relecture.html">Condensateurs 1916</a>). '
         'Les lettres sont celles de la transcription publiée, rectifiées sur les formulaires ; les caractères corrigés ou rétablis sont '
         '<span class="fixed-sample">soulignés en vert</span>. Classement : par clé, puis par date.</p>'),
  read='Lettres du formulaire (transcription publiée, rectifiée sur les scans)',
  fixed={'scan': 'corrigé sur le scan — texte publié : {from}', 'sugg': 'lecture proposée dans le texte publié, confirmée sur le scan',
         'new': 'lecture nouvelle sur le scan — texte publié : {from}', 'omis': 'mot omis dans la transcription publiée, rétabli sur le scan',
         'nouveau': 'lu sur le scan ; absent du texte publié', 'dx': 'relu sur le scan lors des relectures ciblées des codes douteux (13 et 14/10/2026) — texte publié : {from}'},
  stats=('{tels} télégrammes, {codes} codes. Par rapport au texte publié, la lecture des scans change {chg} caractères (les {corr} corrections de la page '
         'Condensateurs 1916, {sugg} lectures proposées dans le texte publié et confirmées, {new} lectures nouvelles, {dx} relues lors des relectures ciblées des codes douteux des 13 et 14 octobre 2026) et en rétablit {added} (mot omis, '
         'fin relue). {conf} codes rares mais confirmés, {douteux} douteux.'),
  toc='Condensateurs 1916', short={'manila1916': 'Manille', 'shanghai1916': 'Shanghai', 'seito1916': 'Qingdao', 'yamada1916': 'Yamada'}, label='Traduction de travail.',
  channel={'manila1916': 'Condensateur « Manille » (Tokyo ↔ Manille)', 'shanghai1916': 'Condensateur « Shanghai » (Tokyo ↔ Shanghai)',
           'seito1916': 'Condensateur « Qingdao » (Tokyo ↔ Qingdao)', 'yamada1916': 'Condensateur « Yamada » (Tokyo → Shanghai, mai 1916)'}),
 'en': dict(
  title='Condenser telegrams, March–May 1916',
  intro=('<p>Before the <span lang="zh-Hant">文密</span>, from March to May 1916, Sun Yat-sen’s circle enciphered its telegrams with simpler '
         '“condensers”: each two-letter syllable gives two digits, and two syllables give one Chinese telegraph code. '
         'These telegrams have been deciphered and published' + SUP + '. We give here, in the same format as the Wenmi, the {tels} telegrams '
         'in which re-reading the scans corrected or verified at least one character (details: <a href="relecture.html">1916 condensers</a>). '
         'The letters are those of the published transcription, rectified on the forms; corrected or restored characters are '
         '<span class="fixed-sample">underlined in green</span>. Order: by key, then by date.</p>'),
  read='Letters on the form (published transcription, rectified on the scans)',
  fixed={'scan': 'corrected on the scan — published text: {from}', 'sugg': 'reading suggested in the published text, confirmed on the scan',
         'new': 'new reading on the scan — published text: {from}', 'omis': 'word omitted in the published transcription, restored from the scan',
         'nouveau': 'read on the scan; not in the published text', 'dx': 're-read on the scan during the targeted checks of doubtful codes (13 and 14 Oct 2026) — published text: {from}'},
  stats=('{tels} telegrams, {codes} codes. Compared with the published text, reading the scans changes {chg} characters (the {corr} corrections of '
         'the 1916 condensers page, {sugg} readings suggested in the published text and confirmed, {new} new readings, {dx} re-read during the targeted checks of doubtful codes on 13 and 14 October 2026) and restores {added} '
         '(omitted word, re-read ending). {conf} rare but confirmed codes, {douteux} doubtful.'),
  toc='1916 condensers', short={'manila1916': 'Manila', 'shanghai1916': 'Shanghai', 'seito1916': 'Qingdao', 'yamada1916': 'Yamada'}, label='Working translation.',
  channel={'manila1916': 'Condenser “Manila” (Tokyo ↔ Manila)', 'shanghai1916': 'Condenser “Shanghai” (Tokyo ↔ Shanghai)',
           'seito1916': 'Condenser “Qingdao” (Tokyo ↔ Qingdao)', 'yamada1916': 'Condenser “Yamada” (Tokyo → Shanghai, May 1916)'}),
 'zh-Hant': dict(
  title='壓縮碼電報（1916年3月至5月）',
  intro=('<p>在<span lang="zh-Hant">文密</span>之前，1916年3月至5月，孫中山一方用較簡單的「壓縮碼」加密電報：每個兩字母的音節對應兩位數字，'
         '兩個音節合成一個中文電碼。這批電報的破譯已經發表' + SUP + '。此處以與文密相同的格式，列出經重讀掃描影像而訂正或核實了至少一個字的'
         '{tels}封電報（詳見<a href="relecture.html">1916年壓縮碼</a>）。字母取自已發表的轉寫，並依電報紙訂正；訂正或補回的字以'
         '<span class="fixed-sample">綠色底線</span>標出。排列：先按密鑰，再按日期。</p>'),
  read='電報紙上的字母（已發表的轉寫，依掃描影像訂正）',
  fixed={'scan': '依掃描影像訂正——已發表文本作：{from}', 'sugg': '已發表文本所提的讀法，經掃描影像證實', 'new': '從掃描影像得出的新讀法——已發表文本作：{from}',
         'omis': '已發表轉寫遺漏的詞，依掃描影像補回', 'nouveau': '從掃描影像讀出；已發表文本無此段', 'dx': '存疑電碼專項重讀時依掃描影像讀出（2026年10月13、14日）——已發表文本作：{from}'},
  stats='{tels}封電報，{codes}個電碼。與已發表文本相比，核對掃描影像後改動{chg}字（「1916年壓縮碼」頁的{corr}處訂正、已發表文本所提並經證實的讀法{sugg}處、新讀法{new}處、2026年10月13、14日存疑電碼專項重讀{dx}處），並補回{added}字（遺漏的詞、重讀的結尾）。罕見但已確認{conf}個，存疑{douteux}個。',
  toc='1916年壓縮碼', short={'manila1916': '馬尼拉', 'shanghai1916': '上海', 'seito1916': '青島', 'yamada1916': '山田'}, label='斷句與白話大意（工作譯文）。',
  channel={'manila1916': '壓縮碼「馬尼拉」（東京 ↔ 馬尼拉）', 'shanghai1916': '壓縮碼「上海」（東京 ↔ 上海）',
           'seito1916': '壓縮碼「青島」（東京 ↔ 青島）', 'yamada1916': '壓縮碼「山田」（東京 → 上海，1916年5月）'}),
 'ja': dict(
  title='圧縮符号電報（1916年3〜5月）',
  intro=('<p><span lang="zh-Hant">文密</span>以前の1916年3〜5月、孫文の周辺はより単純な「圧縮符号」で電報を暗号化していた。'
         '2文字の音節が2桁の数字に、2つの音節が1つの中文電碼に対応する。これらの電報の解読は公開されている' + SUP + '。ここでは文密と同じ形式で、'
         '画像の再読により少なくとも1字を訂正または確認した{tels}通を掲げる（詳細は<a href="relecture.html">1916年圧縮符号</a>）。'
         '文字は公開された翻字を用紙で訂正したもので、訂正・補完した字は<span class="fixed-sample">緑の下線</span>で示す。配列は符号表ごと、日付順。</p>'),
  read='用紙の文字（公開された翻字を画像で訂正）',
  fixed={'scan': '画像で訂正 — 公開テキストでは「{from}」', 'sugg': '公開テキストが示した読み。画像で確認', 'new': '画像による新たな読み — 公開テキストでは「{from}」',
         'omis': '公開された翻字で脱落していた語。画像から補完', 'nouveau': '画像から読んだ部分。公開テキストにはない', 'dx': '疑わしいコードの重点再読で画像から読んだ（2026年10月13・14日）— 公開テキストでは「{from}」'},
  stats='{tels}通、{codes}コード。公開テキストに対し、画像の照合で{chg}字を改めた（「1916年圧縮符号」の訂正{corr}、公開テキストが示し確認された読み{sugg}、新たな読み{new}、2026年10月13・14日の疑わしいコードの重点再読{dx}）。さらに{added}字を補完（脱落語・結尾の再読）。まれだが確認済み{conf}、疑わしい字{douteux}。',
  toc='1916年圧縮符号', short={'manila1916': 'マニラ', 'shanghai1916': '上海', 'seito1916': '青島', 'yamada1916': '山田'}, label='作業訳。',
  channel={'manila1916': '圧縮符号「マニラ」（東京 ↔ マニラ）', 'shanghai1916': '圧縮符号「上海」（東京 ↔ 上海）',
           'seito1916': '圧縮符号「青島」（東京 ↔ 青島）', 'yamada1916': '圧縮符号「山田」（東京 → 上海、1916年5月）'}),
}

TR = {
 'fr': {
  'c0470': "Bacon (倍根) […] n'a pas rédigé de reçu : on craint que ce soit sans valeur devant la loi. Inutile de le poursuivre en justice ; on ne peut que [réclamer (?)] selon le simple bon sens. Voyez comment il répond ; nous aviserons ensuite d'autres moyens.",
  'c0445': "L'Oncle télégraphie que le Fujian a encore besoin de fonds : réunissez-en et virez-les au Japon, pour transmission à Shanghai ; faites aussi prévenir Iloilo (怡朗). — Wen (Sun Yat-sen).",
  'c0461b': "Qui emploie notre code pour télégraphier depuis Shanghai ? L'ordre de remettre 50 000 à Yamada (山田), à Shanghai, est suspect. Désormais, employez le code laissé par Zhantang (Hu Hanmin). — Ying.",
  'c0478a': "Veuillez retirer 4 000 yuans à la HSBC. Répondez. — Ying.",
  'c0468': "L'empire étant aboli, Feng et Zhu (sans doute Feng Guozhang et Zhu Rui) vont attendre et voir. À Shanghai, la faction adverse est faible : nous pouvons préparer nos dispositions sans hâte. Que la marine […] passe à l'action est le plan le plus sûr, mais [l'adversaire] reste sur ses gardes. On craint qu'une action à Shanghai gêne les plans de Wang : veuillez ordonner à Wang de venir vite se concerter, pour [saisir] le moment venu. […] agir ensuite.",
  'c0465a': "Lettre de Pékin : le plan de Morrison (George E. Morrison, conseiller politique de Yuan Shikai) est que Yuan se retire provisoirement et laisse Li [Yuanhong] assurer l'intérim ; la guerre en Europe terminée, on s'appuierait sur l'Angleterre pour […]. L'affaire de Shanghai doit donc éclater avant le retrait de Yuan. — Wen.",
  'c0460': "Les fonds pour le Jiangsu, le Zhejiang, Shanghai et la 2ᵉ escadre peuvent à peu près être couverts, mais sans aucune marge. En outre, le Hunan demande plus de 10 000, le Hubei plus de 10 000, les achats d'armes […], le Jiangxi 4 000, l'Anhui 20 000. Le bureau spécial a-t-il encore des fonds à répartir ? Xi Zhengming dit que les affaires du Zhili vont assez bien. Veuillez virer sans délai deux […] à Shanghai ; pour que tout soit sûr, il faudra deux semaines avant de pouvoir agir.",
  'c0473a': "À transmettre à Wu Shifu, Huang Jinqing, Xu Ruilin, Guanwen et aux autres frères : faites tout pour lever des fonds auprès de la communauté du Fujian ; si vous obtenez beaucoup, cela aidera grandement la cause. J'attends avec impatience de bonnes nouvelles. — Sun Wen (Sun Yat-sen).",
  'c0475': "Télégramme reçu. Pour les fonds, on s'en occupe aussitôt, sans savoir si l'on y parviendra. Que les troupes, maintenant que Yuan recule, se mettent au contraire à attendre et voir est inattendu ; on craint de ne jamais pouvoir s'y fier. Faute de mieux, alors […] Wang Tongyi prendra pied. Pour l'action à Shanghai, 10 000 sont déjà arrivés ; pas de fonds à prélever ici ; Iloilo (怡朗) a promis d'en lever plusieurs dizaines de milliers. Quand l'affaire de […] sera réglée, nous virerons tout. Chen Minzhong arrive à Shanghai : il faut vous concerter avec lui. Veuillez transmettre à Ruwei (Xu Chongzhi). Autre chose : les troupes de Chaozhou bougent-elles ? Zhong[yuan] s'en occupe : pouvez-vous le lui demander par télégramme ? — Wen.",
  'c0485': "Télégramme du Nord : l'empire est aboli et le moral des troupes remonte. Shanghai, au contraire, attend et voit. Je crains que les gens contactés auparavant soient pour la plupart peu sûrs et prennent ce prétexte […] pour obtenir encore de l'argent. Examinez cela de près, mon frère, et ne vous laissez pas tromper. — Sun Wen.",
  'c0486a': "Zhongyuan (Deng Keng) télégraphie pour presser Hong Zhaolin de revenir, mais Hong peut difficilement débarquer [à] Hong Kong. S'il doit aller à Chaozhou, mieux vaut alors qu'il passe par Taïwan pour gagner Shantou. Veuillez en discuter par télégramme avec Zhongyuan. Répondez.",
  'c0489': "Les fonds pour Ruwei (Xu Chongzhi) sont reçus. Au sujet de Chaozhou et Shantou, nous avons télégraphié deux fois à Zhongyuan, sans réponse. Ce que l'on rapporte ici ne semble pas venir de notre parti. Dans le Nord, l'état d'esprit des troupes diverge de celui de Shanghai, selon leur position pour ou contre l'empire. Les troupes de Shanghai y étant pour la plupart opposées, elles se laisseront facilement amadouer après l'abolition ; s'y ajoutent les discours de Yang Shande (commandant militaire de Shanghai) qui les égarent, et elles penchent de plus en plus vers l'apaisement (?). Enquête faite, ce n'est pas une fausse nouvelle ; mais on apprend de source sûre des mouvements de troupes : c'est très inquiétant. Nous proposons d'avancer vite.",
  'c0495': "Télégramme du Guangdong : Zhongyuan est parti pour Shantou ; Xia Sheng et Zhuowen restent pour les affaires du Guangdong. Si vous envoyez des fonds, [veuillez] les adresser à Hong Kong ; s'il y a des armes, veuillez les envoyer à Shantou, etc.",
  'c0459': "[Nos] deux télégrammes du 25 et du 26 attendent réponse. Ici les besoins sont très urgents : faites-le savoir vite. Dès que Du (杜) sera arrivé (?), envoyez sans faute par mandat télégraphique. — Zheng (Ju Zheng). Le 28.",
  'c0473b': "Pour les 50 000, nous ferons tout pour les réunir : vous pouvez vite commencer. Examinez aussi en détail si, depuis l'abolition de l'empire, les troupes ont l'intention de se retirer ; répondez aussitôt.",
  'c0476': "[La méthode (?)] pour faire face à […] est bien reçue. Ici, un coup de main pourrait mener directement à […] Jinan (?) ; il ne faut que 50 000 yuans : envoyez-les vite par mandat télégraphique. [Nous] espérons une réponse télégraphique le jour même.",
  'c0490b': "Frère Liao (sans doute Liao Zhongkai) : un million de yuans en billets militaires, envoyez vite. Répondez.",
  'c0492': "Nous virons aussitôt, par la Yokohama Specie Bank (正金), 50 000 [yens] or à l'intention de Kayano (萱野). Accusez réception. Les marchandises, expédiées de l'intérieur (?) au nom du gouvernement militaire (japonais) de Qingdao, doivent être déclarées à la police de la préfecture de Kanagawa ; elles ne pourront partir qu'une fois autorisées. Je crains que pour le 8 ce soit encore difficile à organiser. […] munitions : saisir vite […] pour combler le précédent […].",
  'c0061': "Cet après-midi, Honjō a transmis le télégramme de Zhao Jinqing (Tianjin) du 11, que voici : « Zhang Yunchou […] gagne Shanghai le 19 (?). Plus de trente étudiants sont arrivés chez moi ; l'école de Baoding (?) prévoit de les disperser le 17. Les étudiants [iront] dans les neuf provinces du Nord ; comme on veut les rassembler à l'avance, il faut d'urgence 4 500 yuans. Yan Xishan et Jin Yong s'affrontent en secret, et [l'un d'eux] penche pour notre parti ; les bandits ont déjà bougé. Kong Geng est pour avancer pas à pas, Wang et les autres pour agir vite, mais tous s'en tiennent au plan. Peut-on les laisser passer aussitôt à l'action ? Envoyez vite des fonds à Tianjin. » Par ailleurs, Ozaki est rentré à la capitale sans avions. Zhongmin (Xia Zhongmin) dit que le Maître a parlé de deux avions envoyés par les Japonais : où sont-ils ? Sinon il faudra en acheter. — Le 17.",
  'c0069': "Miyazaki […] a rencontré Yamamoto […]o (山本□夫) ; il dit que les fusils allemands (?) sont prêts : notre parti décide-t-il de les acheter ? […] répondez. Armes du Shandong […] ; de plus, Yingshi (Chen Qimei) est mort : il faut télégraphier outre-mer. Le Maître doit se garder strictement : on craint qu'un malheur n'ébranle les fondements. Les journaux disent que Ding […] était à ses côtés et a été blessé : est-ce exact ? Répondez en détail. — Chi (sans doute Xie Chi, 謝持). Le 20.",
  'c0071': "À Tianjin, Xi Zhengming compte employer des étudiants et réclame sans cesse de grosses sommes : l'affaire presse. Envoyez des fonds et dépêchez des militaires pour appliquer la méthode convenue ; il ne faut plus tarder. Veuillez décider et répondre vite. — Chi. Le 21.",
  'c0075': "Wu Fei (?) est rentré à Shanghai ; il habite au 26, avenue Joffre (霞飛路), dans la concession française. Sa lettre dit : « Une commande a été passée chez Ōkura & Co. à Dalian pour 300 fusils Type 30 et 100 pistolets Browning ; selon le contrat, le paiement est dû deux mois après la livraison ; un acompte de 2 000 taels a été versé, que le quartier général peut utiliser. Mais il faut d'abord en informer par lettre. » Veuillez envoyer quelqu'un traiter sur place. Mais on ne sait qui a versé l'acompte. — Chi. Le 23.",
  'c0087': "L'affaire des étudiants : avant-hier, suivant vos instructions, j'ai télégraphié à Tianjin d'arrêter. Maintenant [on me dit] de suspendre : est-ce bien cela ? Annulez l'ordre précédent ; répondez vite. Après avoir accueilli Keqiang (Huang Xing) le 27, je rentre le 28. — Chi. Le 25.",
  'c0092': "Keqiang (Huang Xing) dit que, selon le ministère des Affaires étrangères, le Maître devrait différer son départ pour Qingdao. Pour l'affaire des armes, un télégramme d'Aoki à l'état-major aurait plus de poids, etc. Je lui ai déjà communiqué le télégramme circulaire […] et l'ai pressé d'envoyer un télégramme détaillé, car les télégrammes qu'il fait passer par le bureau du journal Minguo restent sans réponse. — [Chi]. Le 26.",
 },
 'en': {
  'c0470': "Bacon (倍根) […] has not written a receipt: it is feared that this has no value in law. There is no need to sue him; we can only [press for payment (?)] on simple common sense. See how he replies; we will then find other means.",
  'c0445': "The Uncle telegraphs that Fujian still needs funds: raise some and remit them to Japan, for transfer to Shanghai; also have Iloilo (怡朗) informed. — Wen (Sun Yat-sen).",
  'c0461b': "Who is using our code to telegraph from Shanghai? The instruction to hand 50,000 to Yamada (山田) in Shanghai is suspicious. From now on, use the code left by Zhantang (Hu Hanmin). — Ying.",
  'c0478a': "Please draw 4,000 yuan at the HSBC. Reply. — Ying.",
  'c0468': "With the monarchy abolished, Feng and Zhu (presumably Feng Guozhang and Zhu Rui) will gradually wait and see. In Shanghai the opposing faction is weak: we can make our arrangements without haste. Having the navy […] move first is the safest plan, but [the other side] remains on its guard. We fear that action in Shanghai would hinder Wang's plans: please order Wang to come quickly for consultation, so as to [seize] the right moment. […] then act.",
  'c0465a': "Letter from Beijing: Morrison's plan (George E. Morrison, political adviser to Yuan Shikai) is for Yuan to step down temporarily and let Li [Yuanhong] act in his place; once the European war is over, British support would be used to […]. The Shanghai affair must therefore break out before Yuan steps down. — Wen.",
  'c0460': "Funds for Jiangsu, Zhejiang, Shanghai and the 2nd Squadron can more or less be covered, but with no margin. In addition, Hunan needs over 10,000, Hubei over 10,000, arms purchases […], Jiangxi 4,000, Anhui 20,000. Does the special office still have funds to distribute? Xi Zhengming says matters in Zhili are going fairly well. Please remit two […] to Shanghai at once; to make everything safe, it will take two weeks before we can act.",
  'c0473a': "To be passed on to Wu Shifu, Huang Jinqing, Xu Ruilin, Guanwen and the other brothers: do your utmost to raise funds from the Fujian community; if you obtain a great deal, it will greatly help the cause. I eagerly await good news. — Sun Wen (Sun Yat-sen).",
  'c0475': "Telegram received. The funds are being arranged at once, without knowing whether we will succeed. That the troops, now that Yuan is retreating, should on the contrary wait and see is unexpected; we fear it can never be relied upon. Failing anything better, then […] Wang Tongyi will gain a foothold. For the action in Shanghai, 10,000 have already arrived; there are no funds to allocate here; Iloilo (怡朗) has promised to raise several tens of thousands. When the […] affair is settled, we will remit everything. Chen Minzhong is coming to Shanghai: you should confer with him. Please pass this on to Ruwei (Xu Chongzhi). Further: are the Chaozhou troops moving? Zhong[yuan] is handling it: can you ask him by telegram? — Wen.",
  'c0485': "Telegram from the North: the monarchy is abolished and the troops' morale is rising. Shanghai, on the contrary, waits and sees. I fear the people contacted earlier are mostly unreliable and use this as a pretext […] to get more money. Look into it closely, brother, and do not let yourself be deceived. — Sun Wen.",
  'c0486a': "Zhongyuan (Deng Keng) telegraphs to urge Hong Zhaolin to come back, but Hong can hardly land [in] Hong Kong. If he has to go to Chaozhou, it would be better for him to go via Taiwan to reach Shantou. Please discuss it by telegram with Zhongyuan. Reply.",
  'c0489': "The funds for Ruwei (Xu Chongzhi) have been received. About Chaozhou and Shantou, we telegraphed Zhongyuan twice, without reply. What is being reported here does not seem to come from our party. In the North, the troops' mood diverges from Shanghai's, according to their stance for or against the monarchy. As the Shanghai troops were mostly opposed to it, they will easily soften after its abolition; on top of that, the speeches of Yang Shande (military commander of Shanghai) lead them astray, and they lean more and more towards appeasement (?). Having investigated, it is not a false report; but we learn from a reliable source of troop transfers: this is most worrying. We propose to move quickly.",
  'c0495': "Telegram from Guangdong: Zhongyuan has left for Shantou; Xia Sheng and Zhuowen remain to handle Guangdong affairs. If you send funds, [please] address them to Hong Kong; if there are arms, please send them to Shantou, etc.",
  'c0459': "[Our] two telegrams of the 25th and the 26th await a reply. Needs here are very urgent: let us know quickly. As soon as Du (杜) has arrived (?), be sure to send by telegraphic transfer. — Zheng (Ju Zheng). The 28th.",
  'c0473b': "We will do our utmost to raise the 50,000: you can start quickly. Also examine in detail whether, since the abolition of the monarchy, the troops intend to withdraw; reply at once.",
  'c0476': "[The method (?)] for dealing with […] is duly received. Here, one stroke could lead straight to […] Jinan (?); only 50,000 yuan is needed: please send it quickly by telegraphic transfer. [We] hope for a telegraphic reply the same day.",
  'c0490b': "Brother Liao (presumably Liao Zhongkai): one million yuan in military notes, send quickly. Reply.",
  'c0492': "We are remitting at once, through the Yokohama Specie Bank (正金), 50,000 [yen] in gold for Kayano (萱野). Acknowledge receipt. The goods, sent from the interior (?) in the name of the (Japanese) military government of Qingdao, must be declared to the Kanagawa prefectural police; they can only leave once authorised. I fear that for the 8th it will still be difficult to arrange. […] ammunition: seize quickly […] to make up the previous […].",
  'c0061': "This afternoon Honjō forwarded the telegram of the 11th from Zhao Jinqing (Tianjin), as follows: “Zhang Yunchou […] leaves for Shanghai on the 19th (?). More than thirty students have arrived at my place; the Baoding (?) school plans to disperse them on the 17th. The students [will go] to the nine northern provinces; as we want to gather them in advance, 4,500 yuan are urgently needed. Yan Xishan and Jin Yong are secretly at odds, and [one of them] leans towards our party; the bandits have already moved. Kong Geng favours a gradual approach, Wang and the others a quick one, but all keep to the plan. May they be allowed to rise at once? Remit funds to Tianjin quickly.” Furthermore, Ozaki has returned to the capital without aircraft. Zhongmin (Xia Zhongmin) says the Master spoke of two aircraft sent by the Japanese: where are they? Otherwise they will have to be bought. — The 17th.",
  'c0069': "Miyazaki […] has met Yamamoto […]o (山本□夫); he says the German (?) rifles are ready: does our party decide to buy them? […] reply. Shandong arms […]; moreover, Yingshi (Chen Qimei) is dead: we should telegraph overseas. The Master must be strictly on guard: we fear a disaster that would shake the foundations. The papers report that Ding […] was at his side and was wounded: is it true? Reply in detail. — Chi (presumably Xie Chi, 謝持). The 20th.",
  'c0071': "In Tianjin, Xi Zhengming plans to use students and keeps asking for large sums: the matter is urgent. Send funds and dispatch military men to carry out the agreed method; there must be no further delay. Please decide and reply quickly. — Chi. The 21st.",
  'c0075': "Wu Fei (?) has returned to Shanghai; he lives at 26 Avenue Joffre (霞飛路), in the French Concession. His letter says: “An order has been placed with Ōkura & Co. in Dalian for 300 Type 30 rifles and 100 Browning pistols; under the contract, payment is due two months after delivery; a deposit of 2,000 taels has been paid, which headquarters can draw on. But one must first give notice by letter.” Please send someone to deal with it on the spot. But it is not known who put up the deposit. — Chi. The 23rd.",
  'c0087': "The students' affair: the day before yesterday, following your instructions, I telegraphed Tianjin to stop. Now [I am told] to put it on hold: is that right? Cancel the previous order; reply quickly. After welcoming Keqiang (Huang Xing) on the 27th, I return on the 28th. — Chi. The 25th.",
  'c0092': "Keqiang (Huang Xing) says that, in the Foreign Ministry's view, the Master should delay going to Qingdao. For the arms matter, a telegram from Aoki to the General Staff would carry more weight, etc. I have already passed on the circular telegram […] to him and urged him to telegraph in detail, because the telegrams he relays through the Minguo newspaper office get no reply. — [Chi]. The 26th.",
 },
 'zh-Hant': {
  'c0470': '大意：倍根（人名）……未寫收條，恐在法律上無效。不必提起訴訟，只能按常理追討（？）。看他如何回答，再另行設法應對。',
  'c0445': '大意：舅（暗稱）來電稱福建仍需款項，請籌款匯往日本，轉至上海；並請轉告怡朗（菲律賓伊洛伊洛）。文（孫文）。',
  'c0461b': '大意：誰用我們的密碼從上海發電？囑交上海山田五萬，可疑。以後請用展堂（胡漢民）留下的電碼。英。',
  'c0478a': '大意：請向匯豐銀行領取四千圓。覆。英。',
  'c0468': '大意：帝制取消後，馮、朱（應為馮國璋、朱瑞）等當逐漸觀望。上海的異派力量薄弱，我方可以從容佈置。由海軍……發動，最為萬全之策，但對方仍急於戒備，未曾鬆懈。顧慮上海一動，妨礙王某的計畫，仍請飭令王某速來會商，以便……相當時機。……然後行動。',
  'c0465a': '大意：北京來信：莫理循（George E. Morrison，袁世凱的政治顧問）之策，是讓袁暫時退位，由黎（元洪）代理；待歐戰結束，再借英國之力……。故上海之事應在袁退位之前發動才行。文。',
  'c0460': '大意：江蘇、浙江、上海及第二艦隊等款項大致可以支應，但沒有餘裕。此外湖南需一萬餘，湖北一萬餘，購械……，江西四千，安徽二萬。專處尚有款項可分給否？席正銘說直隸方面事頗順利。請立即撥二……至上海，籌劃萬全，須兩星期才能發動。',
  'c0473a': '大意：轉吳世父、黃金慶、徐瑞林、貫聞諸兄：請盡力向福建幫籌款，能多得則有濟大局，甚幸。盼候佳音。孫文。',
  'c0475': '大意：來電已悉。款項即行設法，成否未知。軍隊因袁退而反觀望，殊出意外，恐終難依靠。不得已，則……王統（一）得手。上海進行，萬（元）已到，款無可撥；怡朗允籌數萬。……事辦妥即全數匯出。陳民鐘到滬，宜與接洽。請轉告汝爲（許崇智）。再，潮州軍隊是否有動靜？仲（元）去經手，能否去電詢問。文。',
  'c0485': '大意：北方來電，帝制取消，軍心益振，而上海反而觀望。恐怕先前聯絡的人多不可靠，故藉此為辭，……再得款項而已。望兄詳察，勿受其欺，幸甚。孫文。',
  'c0486a': '大意：仲元（鄧鏗）來電催促洪兆麟回來，但洪難以在香港登陸。如需他前往潮州，則經臺灣轉赴汕頭較妥。請與仲元電商。覆。',
  'c0489': '大意：汝爲（許崇智）的款項已收到。潮汕之事兩次電告仲元，無回覆。此間所傳似非本黨所為。北方軍心與上海異趣，關乎對帝制贊成與否。上海軍隊既然多屬反對，帝制取消後自然容易軟化；加上楊善德（上海鎮守使）的演說蠱惑，更趨和緩（？）。已徹底查明，並非誑騙。但近來有抽調部隊的確實消息，至為可慮。擬急進。',
  'c0495': '大意：廣東來電：仲元已赴汕頭，夏聲、卓文留下辦理廣東事務。如匯款，請寄香港；有軍械請送汕頭，等語。',
  'c0459': '大意：二十五日、二十六日兩電盼覆。此間用款甚急，懇請速示。俟杜（？）到後務必電匯。正（居正）。二十八日（勘）。',
  'c0473b': '大意：五萬當盡力籌措，可速著手。並詳查帝制取消後軍隊有無退志，即覆。',
  'c0476': '大意：對付……之法（？）謹悉。此間一舉，可直……濟（濟南？），唯需五萬元，懇速電匯。盼即日電覆。',
  'c0490b': '大意：廖兄（應為廖仲愷）：軍票百萬元，速寄。覆。',
  'c0492': '大意：即由（橫濱）正金銀行電匯五萬金予萱野轉交，收到即覆。貨物由內地（？）以青島軍政官名義，向神奈川縣警察部申報，獲准後才能運出。恐怕八日……仍難辦到。……子彈速迫取，以填前……',
  'c0061': '大意：今天下午本庄轉來天津趙瑾卿十一日（真）電如下：「張運籌……十九日（效？）赴滬。學生到敝處三十餘名，保（定）校（？）擬於十七日解散。學生於北方九省……，因欲提前召集，急需四千五百圓。閻錫山與金永暗鬥，傾心本黨；土匪已動。孔庚主張漸進，王等主張急進，但都遵守方略。可否令其隨即舉事？望速匯款至天津。」又，尾崎已回京，沒有飛機。重民（夏重民）說先生曾言日本人送來兩架飛機，現在何處？否則須購買。十七日（篠）。',
  'c0069': '大意：宮崎……見山本……夫，說德（？）槍已備，本黨是否決定購買？……覆。山東……軍械；又英士（陳其美）已死，宜電告海外。先生務須嚴加戒備，恐禍變動搖根本。報載丁……在旁受傷，確否？詳覆。持（應為謝持）。二十日（號）。',
  'c0071': '大意：天津席正銘爲擬使學生，連連索取巨款，事情急迫。撥款派軍人，按前述辦法進行，不宜再緩，請速決速覆。持。二十一日（箇）。',
  'c0075': '大意：吳非（？）已回上海，住法租界霞飛路二十六號。來函說：在大連大倉洋行訂購三十年式步槍三百枝、勃朗寧手槍一百枝，合同規定交貨後兩個月付款；已交定金二千兩，本部可以提用。但須先函知云云。請派人就近接洽。但不知定金由誰付出。持。二十三日（漾）。',
  'c0087': '大意：學生之事，前日已遵示電告天津停止，現在說暫時擱置，是否如此？取消前令，速覆。二十七日（沁）歡迎克強（黃興）後，二十八日（儉）回。持。二十五日（有）。',
  'c0092': '大意：克強（黃興）說，外務省之意，先生宜暫緩前往青島。又，軍械之事，若能得青木一電致參謀本部，更為有力，云云。已將通電……告知他，促他詳細電告，因他經民國報社轉電，得不到回覆。……持（？）。二十六日（宥）。',
 },
 'ja': {
  'c0470': '倍根（人名）は……受取証を書いていない。法律上無効となるおそれがある。訴える必要はなく、ただ常識に従って取り立てる（？）ほかない。どう答えるかを見て、別に対処の方法を講じる。',
  'c0445': '舅（隠語）の電報によれば、福建はなお資金を要する。資金を集めて日本へ送金し、上海へ転送されたい。また怡朗（イロイロ）にも伝えられたい。文（孫文）。',
  'c0461b': '誰が我々の暗号を用いて上海から打電したのか。上海の山田に五万を渡せという指示は疑わしい。今後は展堂（胡漢民）が残した電碼を用いられたい。英。',
  'c0478a': '香港上海銀行で四千円を受け取られたい。返電せよ。英。',
  'c0468': '帝制取り消しにより、馮・朱（馮国璋・朱瑞か）らはしだいに形勢を観望するだろう。上海の反対派は力が弱く、我が方はゆっくり配置できる。海軍が……発動するのが最も万全の策だが、相手はなお警戒を緩めていない。上海で動けば王の計画を妨げるおそれがあるので、王に至急来て協議するよう命じ、……時機に備えられたい。……その後に動く。',
  'c0465a': '北京からの書信：モリソン（袁世凱の政治顧問 G. E. モリソン）の策は、袁を一時退かせて黎（元洪）に代行させ、欧州大戦の終結を待ってイギリスの力を借りて……というもの。ゆえに上海の事は袁の退位前に起こさねばならない。文。',
  'c0460': '江蘇・浙江・上海および第二艦隊などの資金はほぼ賄えるが、余裕はない。そのほか湖南が一万余、湖北が一万余、武器購入……、江西四千、安徽二万を要する。専処にはなお分配できる資金があるか。席正銘によれば直隷の事はかなり順調。ただちに二……を上海へ送られたい。万全を期すには、発動まで二週間を要する。',
  'c0473a': '呉世父・黄金慶・徐瑞林・貫聞の諸兄に転送：福建幇から全力で資金を集められたい。多く得られれば大局を救い、まことに幸いである。吉報を待つ。孫文。',
  'c0475': '来電了承。資金はすぐに手配するが、成否は分からない。軍隊が袁の退位でかえって形勢観望に転じたのは意外であり、結局頼りにならないおそれがある。やむを得なければ、……王統（一）が地歩を得る。上海の進行は、一万はすでに届いた。資金は回せないが、怡朗（イロイロ）が数万の調達を約した。……の件が片づけば、すぐに全額送金する。陳民鐘が上海に着くので、連絡をとられたい。汝為（許崇智）に伝えられたい。また、潮州の軍隊に動きはあるか。仲（元）が担当する。電報で問い合わせられるか。文。',
  'c0485': '北方からの電報によれば、帝制取り消しで軍の士気はますます上がった。ところが上海はかえって形勢を観望している。以前連絡した人々の多くは当てにならず、これを口実に……さらに金を得ようとしているだけではないか。兄には詳しく調べ、だまされないよう願う。孫文。',
  'c0486a': '仲元（鄧鏗）が洪兆麟の帰還を電報で促したが、洪は香港に上陸しにくい。潮州へ行く必要があるなら、台湾経由で汕頭へ向かうのが妥当。仲元と電報で協議されたい。返電せよ。',
  'c0489': '汝為（許崇智）への資金は受領した。潮汕の件は仲元に二度打電したが返事がない。当地で伝えられていることは我が党によるものではないようだ。北方の軍心は上海とは趣を異にし、それは帝制への賛否にかかわる。上海の軍は多くが反対派なので、取り消し後はたやすく軟化するだろう。そのうえ楊善徳（上海鎮守使）の演説が惑わしており、ますます軟化（？）に傾いている。調べ尽くしたが、デマではない。ただし最近、部隊引き抜きの確かな情報があり、きわめて憂慮される。急ぎ進めるつもりである。',
  'c0495': '広東からの電報：仲元はすでに汕頭へ向かい、夏声・卓文が残って広東の事を処理する。送金するなら香港へ送られたい。武器があれば汕頭へ送られたい、とのこと。',
  'c0459': '二十五日・二十六日の二電への返事を待つ。当地は資金がきわめて急を要する。至急知らされたい。杜（？）が着いたら必ず電信送金されたい。正（居正）。二十八日（勘）。',
  'c0473b': '五万は全力で調達するので、すぐに着手されたい。また帝制取り消し後、軍隊に撤退の意思があるかどうかを詳しく調べ、ただちに返電されたい。',
  'c0476': '……への対処の方法（？）、承知した。当地の一挙はただちに……済（済南か）に及びうる。必要なのは五万元のみ。至急電信送金されたい。即日の返電を望む。',
  'c0490b': '廖兄（廖仲愷か）へ：軍票百万元、至急送られたい。返電せよ。',
  'c0492': 'ただちに（横浜）正金銀行から萱野へ五万金を電送する。受領したら返電されたい。荷物は内地（？）から青島軍政官の名義で神奈川県警察部に届け出て、認可を得てはじめて運べる。八日には……なお難しいおそれがある。……弾薬を至急取り立て、前の……を埋めよ。',
  'c0061': '本日午後、本庄が天津の趙瑾卿の十一日（真）の電報を転送してきた。以下のとおり：「張運籌……十九日（効か）に上海へ向かう。学生が当方に三十余名来ており、保（定）校（？）は十七日に解散の予定。学生は北方九省へ……。前もって召集したいので、至急四千五百円が必要。閻錫山と金永は暗闘しており、我が党に心を寄せている。土匪はすでに動いた。孔庚は漸進を、王らは急進を主張するが、いずれも方略を守っている。ただちに挙兵させてよいか。至急天津へ送金されたい。」また尾崎は帰京したが、飛行機はない。重民（夏重民）によれば、先生は日本人が飛行機二機を送ったと言われたが、いまどこにあるのか。さもなくば購入せねばならない。十七日（篠）。',
  'c0069': '宮崎……山本……夫に会い、ドイツ（？）製の銃はすでに準備できていると言う。我が党は購入を決めるか。……返電せよ。山東の……武器。また英士（陳其美）が死去した。海外へ打電すべし。先生は厳重に警戒されたい。禍変が根本を揺るがすおそれがある。新聞によれば丁……がそばにいて負傷したというが、確かか。詳しく返電せよ。持（謝持か）。二十日（号）。',
  'c0071': '天津の席正銘は学生を使うつもりで、たびたび巨額の資金を求めており、事は急を要する。資金を出して軍人を派遣し、前の方法で進めるべきで、これ以上遅らせてはならない。速やかに決定し、返電されたい。持。二十一日（箇）。',
  'c0075': '呉非（？）は上海に戻り、フランス租界の霞飛路（アヴニュー・ジョッフル）二十六号に住む。来信によれば：大連の大倉洋行に三十年式歩兵銃三百挺、ブローニング拳銃百挺を発注し、契約では引き渡しの二か月後に代金を支払う。手付金二千両はすでに払い込み済みで、本部が流用できる。ただし、まず書面で知らせねばならない、云々。人を派遣して現地で交渉されたい。ただし手付金を誰が出したのかは分からない。持。二十三日（漾）。',
  'c0087': '学生の件、一昨日指示に従い天津へ打電して中止させた。いま一時見合わせるとのことだが、そうか。前令を取り消す。至急返電されたい。二十七日（沁）に克強（黄興）を出迎えたのち、二十八日（倹）に帰る。持。二十五日（有）。',
  'c0092': '克強（黄興）によれば、外務省の意向では先生は青島行きを遅らせるのがよい。また武器の件は、青木から参謀本部へ一電あれば、より有力である、云々。すでに通電を……彼に伝え、詳しく打電するよう促した。彼は民国報社経由で転電しており、返事が得られないためである。……持（？）。二十六日（宥）。',
 },
}


def t2s_table(wenmi):
    """Table traditionnel → simplifié : OpenCC STCharacters (simplifié → traditionnel·s), inversée. Un caractère n'est converti que
    s'il est rare en chinois simplifié (fréquences du dictionnaire jieba, corpus simplifié) : sinon « 呆 → 呆 待 » ferait de 待 un 呆,
    et « 坐 → 坐 座 » de 座 un 坐. Entre plusieurs cibles, la plus fréquente l'emporte (劃 → 划, et non 㓰)."""
    import collections
    freq = collections.Counter()
    for line in open(os.path.join(wenmi, 'sources', 'language', 'jieba-dict.txt'), encoding='utf-8'):
        p = line.split()
        if len(p) >= 2 and p[1].isdigit():
            for c in p[0]: freq[c] += int(p[1])
    cand = collections.defaultdict(set)
    for line in open(os.path.join(wenmi, 'sources', 'language', 'STCharacters.txt'), encoding='utf-8'):
        if line.startswith('#') or '\t' not in line: continue
        s, ts = line.rstrip('\n').split('\t')
        for t in ts.split():
            if t != s: cand[t].add(s)
    m = {}
    for t, ss in cand.items():
        s = max(ss, key=lambda x: (freq[x], x))
        if freq[t] > 2000 and freq[t] > 0.2 * freq[s]: continue   # caractère courant en simplifié : on le garde
        m[t] = s
    m.update({'為': '为', '篠': '篠', '著': '着'})   # 為 → 为 ; 篠 : nom de rime (date) ; 著手 → 着手
    return m


PHRASES = {'座標': '坐标'}   # formes simplifiées propres à un mot (座 reste 座 ailleurs)


def to_hans(x, T):
    if isinstance(x, dict): return {k: to_hans(v, T) for k, v in x.items()}
    conv = lambda seg: ''.join(T.get(c, c) for c in __import__('functools').reduce(lambda a, kv: a.replace(*kv), PHRASES.items(), seg))
    # les balises et les caractères explicitement marqués lang="zh-Hant" restent en traditionnel
    out, i = [], 0
    while i < len(x):
        j = x.find('<span lang="zh-Hant">', i)
        if j < 0: out.append(conv(x[i:])); break
        k = x.index('</span>', j) + 7
        out.append(conv(x[i:j])); out.append(x[j:k]); i = k
    return ''.join(out)


def date_of(lang, mo, da):
    if lang == 'fr': return '%s %s 1916' % ('1er' if da == 1 else da, MONTHS_FR[mo])
    if lang == 'en': return '%d %s 1916' % (da, MONTHS_EN[mo])
    return '1916年%d月%d日' % (mo, da)


def build(msgs, stats, wenmi):
    T = t2s_table(wenmi); out = {}
    for lang in ('fr', 'en', 'zh-Hant', 'ja'):
        d = dict(LAB[lang]); d['tr'] = dict(TR[lang]); d['date'] = {m['id']: date_of(lang, *m['md']) for m in msgs}
        d['intro'] = d['intro'].replace('{tels}', str(stats['tels']))
        assert set(d['tr']) == {m['id'] for m in msgs}, (lang, set(d['tr']) ^ {m['id'] for m in msgs})
        out[lang] = d
    hans = to_hans({k: v for k, v in out['zh-Hant'].items() if k != 'date'}, T)
    hans['date'] = dict(out['zh-Hant']['date']); out['zh-Hans'] = hans
    return out
