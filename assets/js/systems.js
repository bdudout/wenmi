// Page « Télégrammes » : classement par système de chiffrement, puis par date (séance YC, 15/10/2026).
// Chaque fiche des corpus (corpus.js, corpus-c1916.js, corpus-n1916.js, corpus-t1915.js, corpus-f1916.js) est rattachée
// à un système par son corpus et sa clé (m.grid) ; voir MAP. Textes en 5 langues ; [n] renvoie à la page Sources.
window.WENMI_SYSTEMS = {
  // corpus → { clé : système }
  map: {
    CORPUS: { G0: 'G0', Y0: 'Y0' },
    C1916: { manila1916: 'manila1916', shanghai1916: 'shanghai1916', seito1916: 'seito1916', yamada1916: 'yamada1916' },
    N1916: { honolulu1916w: 'honolulu1916', yamada1916: 'yamada1916', yamada1916w: 'yamada1916', man2: 'manila1916b', k38: 'k38', h16: 'h16' },
    T1915: { manila1916b: 'manila1916b', laisaosang1915: 'laisaosang1915', newyork1915: 'newyork1915', k30: 'k30' },
    F1916: { shanghai1916: 'shanghai1916', k13: 'k13', seito1916: 'seito1916', manila1916: 'manila1916', sanfran1916: 'sanfran1916' }
  },
  year: { CORPUS: 1916, C1916: 1916, N1916: 1916, T1915: 1915, F1916: 1916 },
  // jour approché pour le classement (date du formulaire illisible ; cf. tools/form_times.py)
  sortDay: { '1915-02p23': 1, '1915-02ny': 24 },
  groups: [
    { id: 'wenmi', systems: ['G0', 'Y0'] },
    { id: 'condensers', anchors: ['c1916', 'n1916', 't1915', 'f1916'],
      systems: ['manila1916b', 'laisaosang1915', 'newyork1915', 'k30', 'shanghai1916', 'k13', 'seito1916', 'manila1916', 'sanfran1916', 'honolulu1916', 'yamada1916', 'k38', 'h16'] }
  ],
  text: {
    fr: {
      toc: 'Les systèmes',
      groups: {
        wenmi: ['Le Wenmi (1916) : deux grilles de syllabes', '<p>Les télégrammes chiffrés de Zhao Shen (趙伸), commissaire du Conseil des affaires militaires à Tokyo, de juin à novembre 1916. Deux canaux, chacun avec sa grille : chaque syllabe donne un chiffre des dizaines et un chiffre des unités, et deux syllabes un code télégraphique chinois. Grilles retrouvées en octobre 2026 (voir la <a href="method.html">Méthode</a>).</p>'],
        condensers: ['Les condensateurs (1915–1916) : une table par correspondant', '<p>Chaque syllabe de deux lettres (consonne + voyelle) donne deux chiffres, et deux syllabes un code télégraphique chinois ; chaque correspondant de Sun Yat-sen a sa table. Les tables sont classées par date de leur premier télégramme, et les télégrammes par date dans chaque table. Une partie de ces télégrammes (mars–mai 1916) a été transcrite et déchiffrée par D. Bourdeau[1, 2] : les lettres sont alors celles de la transcription publiée, rectifiées sur les scans, et les caractères corrigés sont soulignés en vert (détail : <a href="relecture.html">Condensateurs 1916</a>). Les autres, absents des transcriptions publiées, ont été lus sur les scans par Claude et relus par Brice Dudout ; l\'intitulé « Lettres du formulaire » de chaque fiche précise la provenance.</p>']
      },
      sys: {
        G0: ['Grille G0 — « 文密 »', 'Tokyo → Conseil des affaires militaires (Zhaoqing) et Shanghai, juin–septembre 1916. Grille de 20 consonnes × 5 voyelles en coordonnées, retrouvée en octobre 2026.'],
        Y0: ['Grille Y0 — indicateur « Cg »', 'Tokyo ↔ Yunnan, juillet–novembre 1916. Grille de 17 consonnes × 6 voyelles (y compris y), retrouvée en octobre 2026.'],
        manila1916b: ['Table « Manille » (seconde clé)', 'Tokyo → Manille (6 janvier 1915) et Manille → Tōyama Mitsuru (mai 1916). Table publiée à titre provisoire par D. Bourdeau[1], confirmée ici.'],
        laisaosang1915: ['Table « Laisaosang »', 'Tokyo (au nom de Tōyama Mitsuru) → « Laisaosang », Shanghai, et Shanghai → « Rosamonde », janvier–février 1915. Table retrouvée en octobre 2026.'],
        newyork1915: ['Table « New York »', 'New York → Sun Yat-sen, février 1915. Table retrouvée en octobre 2026.'],
        k30: ['Table « Thirtieth »', 'Shanghai → « Rosamonde » et Tokyo → « Junzaburo », février–mars 1915 ; indicateur en clair « Thirtieth ». Table retrouvée en octobre 2026.'],
        shanghai1916: ['Table « Shanghai »', 'Shanghai ↔ Tokyo (« Rosamonde », Yamada Junzaburō), février–avril 1916. Table publiée par D. Bourdeau[1].'],
        k13: ['Table « Thirteenth »', 'Tokyo → « Junzaburo », février–mars 1916 ; indicateur en clair « Thirteenth ». Table retrouvée en octobre 2026.'],
        seito1916: ['Table « Qingdao »', 'Qingdao ↔ Tokyo (Ju Zheng, Kayano Nagatomo), mars–avril 1916. Table publiée par D. Bourdeau[1].'],
        manila1916: ['Table « Manille »', 'Tokyo ↔ Manille, mars 1916. Table publiée par D. Bourdeau[1].'],
        sanfran1916: ['Table « San Francisco »', 'San Francisco → « Dr Sunwen », Tokyo, mars 1916 ; signé 森 (Lin Sen). Table publiée par D. Bourdeau[1].'],
        honolulu1916: ['Table « Honolulu », variante « Aloha »', 'Honolulu → Tokyo, 30 avril 1916 ; indicateur « Aloha ». Table publiée par D. Bourdeau[1], ici avec w comme seconde forme de v.'],
        yamada1916: ['Table « Yamada » — « Thirtyseventh »', 'Tokyo ↔ Shanghai (« Junzaburo », « Linwailuk »), mai–juin 1916 ; indicateur en clair « Thirtyseventh » sur la plupart. Table publiée par D. Bourdeau[1].'],
        k38: ['Table « Thirtyeight »', 'Tokyo → « Junzaburo », 11–12 mai 1916 ; indicateur en clair « Thirtyeight ». Table retrouvée en octobre 2026.'],
        h16: ['Table de Huang Xing', 'Tokyo (Huang Xing) → « Junzaburo », sans indicateur, et Shanghai → « Ylchang » (Huang Xing), fin mai – juin 1916. Table retrouvée en octobre 2026. À ne pas confondre avec le code à trois kana d\'un autre télégramme de Huang Xing (25 mai 1916, à Lin Hu et Li Genyuan), dont le système a été identifié par D. Bourdeau et la formule par S. Tomokiyo[22, 23].']
      },
      rosamonde: ['L\'anglais chiffré de Rosamonde (1915–1916)', '<p>Une vingtaine de télégrammes en anglais, chiffrés par une substitution réciproque de lettres, entre Sun Yat-sen et Soong Ching-ling : présentés sur une page à part, <a href="rosamonde.html">Les télégrammes de Rosamonde</a>.</p>'],
      count: '{n} télégrammes', count1: '1 télégramme'
    },
    en: {
      toc: 'The systems',
      groups: {
        wenmi: ['The Wenmi (1916): two syllable grids', '<p>The enciphered telegrams of Zhao Shen (趙伸), commissioner of the Military Affairs Council in Tokyo, June to November 1916. Two channels, each with its own grid: each syllable gives a tens digit and a units digit, and two syllables a Chinese telegraph code. Grids recovered in October 2026 (see the <a href="method.html">Method</a>).</p>'],
        condensers: ['The condensers (1915–1916): one table per correspondent', '<p>Each two-letter syllable (consonant + vowel) gives two digits, and two syllables a Chinese telegraph code; each of Sun Yat-sen\'s correspondents has his own table. Tables are ordered by the date of their first telegram, and telegrams by date within each table. Some of these telegrams (March–May 1916) were transcribed and deciphered by D. Bourdeau[1, 2]: their letters are those of the published transcription, rectified on the scans, and corrected characters are underlined in green (details: <a href="relecture.html">1916 condensers</a>). The others, absent from the published transcriptions, were read on the scans by Claude and reread by Brice Dudout; the “Letters of the form” label of each card gives the provenance.</p>']
      },
      sys: {
        G0: ['Grid G0 — “文密”', 'Tokyo → Military Affairs Council (Zhaoqing) and Shanghai, June–September 1916. Coordinate grid of 20 consonants × 5 vowels, recovered in October 2026.'],
        Y0: ['Grid Y0 — indicator “Cg”', 'Tokyo ↔ Yunnan, July–November 1916. Grid of 17 consonants × 6 vowels (including y), recovered in October 2026.'],
        manila1916b: ['“Manila” table (second key)', 'Tokyo → Manila (6 January 1915) and Manila → Tōyama Mitsuru (May 1916). Table published tentatively by D. Bourdeau[1], confirmed here.'],
        laisaosang1915: ['“Laisaosang” table', 'Tokyo (in the name of Tōyama Mitsuru) → “Laisaosang”, Shanghai, and Shanghai → “Rosamonde”, January–February 1915. Table recovered in October 2026.'],
        newyork1915: ['“New York” table', 'New York → Sun Yat-sen, February 1915. Table recovered in October 2026.'],
        k30: ['“Thirtieth” table', 'Shanghai → “Rosamonde” and Tokyo → “Junzaburo”, February–March 1915; clear indicator “Thirtieth”. Table recovered in October 2026.'],
        shanghai1916: ['“Shanghai” table', 'Shanghai ↔ Tokyo (“Rosamonde”, Yamada Junzaburō), February–April 1916. Table published by D. Bourdeau[1].'],
        k13: ['“Thirteenth” table', 'Tokyo → “Junzaburo”, February–March 1916; clear indicator “Thirteenth”. Table recovered in October 2026.'],
        seito1916: ['“Qingdao” table', 'Qingdao ↔ Tokyo (Ju Zheng, Kayano Nagatomo), March–April 1916. Table published by D. Bourdeau[1].'],
        manila1916: ['“Manila” table', 'Tokyo ↔ Manila, March 1916. Table published by D. Bourdeau[1].'],
        sanfran1916: ['“San Francisco” table', 'San Francisco → “Dr Sunwen”, Tokyo, March 1916; signed 森 (Lin Sen). Table published by D. Bourdeau[1].'],
        honolulu1916: ['“Honolulu” table, “Aloha” variant', 'Honolulu → Tokyo, 30 April 1916; indicator “Aloha”. Table published by D. Bourdeau[1], here with w as a second form of v.'],
        yamada1916: ['“Yamada” table — “Thirtyseventh”', 'Tokyo ↔ Shanghai (“Junzaburo”, “Linwailuk”), May–June 1916; clear indicator “Thirtyseventh” on most. Table published by D. Bourdeau[1].'],
        k38: ['“Thirtyeight” table', 'Tokyo → “Junzaburo”, 11–12 May 1916; clear indicator “Thirtyeight”. Table recovered in October 2026.'],
        h16: ['Huang Xing\'s table', 'Tokyo (Huang Xing) → “Junzaburo”, without indicator, and Shanghai → “Ylchang” (Huang Xing), late May – June 1916. Table recovered in October 2026. Not to be confused with the three-kana code of another telegram of Huang Xing (25 May 1916, to Lin Hu and Li Genyuan), whose system was identified by D. Bourdeau and whose formula by S. Tomokiyo[22, 23].']
      },
      rosamonde: ['Rosamonde\'s enciphered English (1915–1916)', '<p>Some twenty telegrams in English, enciphered by a reciprocal letter substitution, between Sun Yat-sen and Soong Ching-ling: presented on a separate page, <a href="rosamonde.html">The Rosamonde telegrams</a>.</p>'],
      count: '{n} telegrams', count1: '1 telegram'
    },
    'zh-Hant': {
      toc: '加密系統',
      groups: {
        wenmi: ['文密（1916年）：兩張音節表', '<p>1916年6月至11月，軍務院駐東京委員趙伸的加密電報。兩條通道，各用一張表：每個音節給出十位數和個位數，兩個音節組成一個漢字電碼。兩張表於2026年10月復原（見<a href="method.html">破譯方法</a>）。</p>'],
        condensers: ['壓縮碼（1915–1916年）：每位通信者一張表', '<p>每個兩字母音節（輔音＋元音）代表兩位數字，兩個音節組成一個漢字電碼；孫中山的每位通信者各有一張表。各表按其第一封電報的日期排列，表內電報按日期排列。其中一部分（1916年3月至5月）已由 D. Bourdeau 轉錄並破譯[1, 2]：字母取自已發表的轉錄，並依掃描件訂正，訂正的字以綠色底線標出（詳見<a href="relecture.html">1916年壓縮碼</a>）。其餘電報未見於已發表的轉錄，由 Claude 依掃描件讀出，再由 Brice Dudout 複核；各電報卡片上的「電報紙上的字母」一欄註明來源。</p>']
      },
      sys: {
        G0: ['G0 表——「文密」', '東京 → 軍務院（肇慶）及上海，1916年6月至9月。20個輔音 × 5個元音的座標表，2026年10月復原。'],
        Y0: ['Y0 表——標記「Cg」', '東京 ↔ 雲南，1916年7月至11月。17個輔音 × 6個元音（含 y）的表，2026年10月復原。'],
        manila1916b: ['「馬尼拉」表（第二密鑰）', '東京 → 馬尼拉（1915年1月6日）及馬尼拉 → 頭山滿（1916年5月）。D. Bourdeau 暫定發表的表[1]，此處得到證實。'],
        laisaosang1915: ['「Laisaosang」表', '東京（以頭山滿名義）→ 上海「Laisaosang」，及上海 →「Rosamonde」，1915年1月至2月。2026年10月復原。'],
        newyork1915: ['「紐約」表', '紐約 → 孫中山，1915年2月。2026年10月復原。'],
        k30: ['「Thirtieth」表', '上海 →「Rosamonde」及東京 →「Junzaburo」，1915年2月至3月；明碼標記「Thirtieth」。2026年10月復原。'],
        shanghai1916: ['「上海」表', '上海 ↔ 東京（「Rosamonde」、山田純三郎），1916年2月至4月。D. Bourdeau 發表的表[1]。'],
        k13: ['「Thirteenth」表', '東京 →「Junzaburo」，1916年2月至3月；明碼標記「Thirteenth」。2026年10月復原。'],
        seito1916: ['「青島」表', '青島 ↔ 東京（居正、萱野長知），1916年3月至4月。D. Bourdeau 發表的表[1]。'],
        manila1916: ['「馬尼拉」表', '東京 ↔ 馬尼拉，1916年3月。D. Bourdeau 發表的表[1]。'],
        sanfran1916: ['「舊金山」表', '舊金山 →「Dr Sunwen」，東京，1916年3月；署名「森」（林森）。D. Bourdeau 發表的表[1]。'],
        honolulu1916: ['「檀香山」表，「Aloha」變體', '檀香山 → 東京，1916年4月30日；標記「Aloha」。D. Bourdeau 發表的表[1]，此處 w 作為 v 的第二寫法。'],
        yamada1916: ['「山田」表——「Thirtyseventh」', '東京 ↔ 上海（「Junzaburo」、「Linwailuk」），1916年5月至6月；多數帶明碼標記「Thirtyseventh」。D. Bourdeau 發表的表[1]。'],
        k38: ['「Thirtyeight」表', '東京 →「Junzaburo」，1916年5月11至12日；明碼標記「Thirtyeight」。2026年10月復原。'],
        h16: ['黃興的表', '東京（黃興）→「Junzaburo」（無標記）及上海 →「Ylchang」（黃興），1916年5月底至6月。2026年10月復原。勿與黃興另一封電報（1916年5月25日致林虎、李根源）的三假名電碼混淆：該系統由 D. Bourdeau 識別，其對應公式由 S. Tomokiyo 找出[22, 23]。']
      },
      rosamonde: ['羅莎蒙德的加密英文（1915–1916年）', '<p>孫中山與宋慶齡之間二十來封以字母互換加密的英文電報，另見專頁：<a href="rosamonde.html">羅莎蒙德電報</a>。</p>'],
      count: '{n} 封電報', count1: '1 封電報'
    },
    'zh-Hans': {
      toc: '加密系统',
      groups: {
        wenmi: ['文密（1916年）：两张音节表', '<p>1916年6月至11月，军务院驻东京委员赵伸的加密电报。两条通道，各用一张表：每个音节给出十位数和个位数，两个音节组成一个汉字电码。两张表于2026年10月复原（见<a href="method.html">破译方法</a>）。</p>'],
        condensers: ['压缩码（1915–1916年）：每位通信者一张表', '<p>每个两字母音节（辅音＋元音）代表两位数字，两个音节组成一个汉字电码；孙中山的每位通信者各有一张表。各表按其第一封电报的日期排列，表内电报按日期排列。其中一部分（1916年3月至5月）已由 D. Bourdeau 转录并破译[1, 2]：字母取自已发表的转录，并依扫描件订正，订正的字以绿色下划线标出（详见<a href="relecture.html">1916年压缩码</a>）。其余电报未见于已发表的转录，由 Claude 依扫描件读出，再由 Brice Dudout 复核；各电报卡片上的“电报纸上的字母”一栏注明来源。</p>']
      },
      sys: {
        G0: ['G0 表——“文密”', '东京 → 军务院（肇庆）及上海，1916年6月至9月。20个辅音 × 5个元音的坐标表，2026年10月复原。'],
        Y0: ['Y0 表——标记“Cg”', '东京 ↔ 云南，1916年7月至11月。17个辅音 × 6个元音（含 y）的表，2026年10月复原。'],
        manila1916b: ['“马尼拉”表（第二密钥）', '东京 → 马尼拉（1915年1月6日）及马尼拉 → 头山满（1916年5月）。D. Bourdeau 暂定发表的表[1]，此处得到证实。'],
        laisaosang1915: ['“Laisaosang”表', '东京（以头山满名义）→ 上海“Laisaosang”，及上海 →“Rosamonde”，1915年1月至2月。2026年10月复原。'],
        newyork1915: ['“纽约”表', '纽约 → 孙中山，1915年2月。2026年10月复原。'],
        k30: ['“Thirtieth”表', '上海 →“Rosamonde”及东京 →“Junzaburo”，1915年2月至3月；明码标记“Thirtieth”。2026年10月复原。'],
        shanghai1916: ['“上海”表', '上海 ↔ 东京（“Rosamonde”、山田纯三郎），1916年2月至4月。D. Bourdeau 发表的表[1]。'],
        k13: ['“Thirteenth”表', '东京 →“Junzaburo”，1916年2月至3月；明码标记“Thirteenth”。2026年10月复原。'],
        seito1916: ['“青岛”表', '青岛 ↔ 东京（居正、萱野长知），1916年3月至4月。D. Bourdeau 发表的表[1]。'],
        manila1916: ['“马尼拉”表', '东京 ↔ 马尼拉，1916年3月。D. Bourdeau 发表的表[1]。'],
        sanfran1916: ['“旧金山”表', '旧金山 →“Dr Sunwen”，东京，1916年3月；署名“森”（林森）。D. Bourdeau 发表的表[1]。'],
        honolulu1916: ['“檀香山”表，“Aloha”变体', '檀香山 → 东京，1916年4月30日；标记“Aloha”。D. Bourdeau 发表的表[1]，此处 w 作为 v 的第二写法。'],
        yamada1916: ['“山田”表——“Thirtyseventh”', '东京 ↔ 上海（“Junzaburo”、“Linwailuk”），1916年5月至6月；多数带明码标记“Thirtyseventh”。D. Bourdeau 发表的表[1]。'],
        k38: ['“Thirtyeight”表', '东京 →“Junzaburo”，1916年5月11至12日；明码标记“Thirtyeight”。2026年10月复原。'],
        h16: ['黄兴的表', '东京（黄兴）→“Junzaburo”（无标记）及上海 →“Ylchang”（黄兴），1916年5月底至6月。2026年10月复原。勿与黄兴另一封电报（1916年5月25日致林虎、李根源）的三假名电码混淆：该系统由 D. Bourdeau 识别，其对应公式由 S. Tomokiyo 找出[22, 23]。']
      },
      rosamonde: ['罗莎蒙德的加密英文（1915–1916年）', '<p>孙中山与宋庆龄之间二十来封以字母互换加密的英文电报，另见专页：<a href="rosamonde.html">罗莎蒙德电报</a>。</p>'],
      count: '{n} 封电报', count1: '1 封电报'
    },
    ja: {
      toc: '暗号方式',
      groups: {
        wenmi: ['文密（1916年）：二つの音節表', '<p>1916年6月から11月、東京駐在の軍務院委員・趙伸の暗号電報。二つの系統があり、それぞれ専用の表を使う。音節一つが十の位と一の位の数字を表し、音節二つで中国電信符号一つになる。二つの表は2026年10月に復元した（<a href="method.html">解読の方法</a>を参照）。</p>'],
        condensers: ['コンデンサー（1915–1916年）：通信相手ごとの表', '<p>二文字の音節（子音＋母音）一つが二桁の数字を表し、音節二つで中国電信符号一つになる。孫文の通信相手ごとに表が異なる。表は最初の電報の日付順、各表の中の電報も日付順に並べた。このうち一部（1916年3〜5月）は D. Bourdeau が翻字・解読している[1, 2]。その場合の文字は公表された翻字をスキャンで訂正したもので、訂正した字は緑の下線で示す（詳細：<a href="relecture.html">1916年のコンデンサー</a>）。残りは公表された翻字にない電報で、Claude がスキャンから読み、Brice Dudout が読み直した。各カードの「用紙の文字」の見出しに出所を記す。</p>']
      },
      sys: {
        G0: ['G0 表——「文密」', '東京 → 軍務院（肇慶）および上海、1916年6〜9月。子音20 × 母音5の座標表。2026年10月に復元。'],
        Y0: ['Y0 表——標識「Cg」', '東京 ↔ 雲南、1916年7〜11月。子音17 × 母音6（y を含む）の表。2026年10月に復元。'],
        manila1916b: ['「マニラ」表（第二の鍵）', '東京 → マニラ（1915年1月6日）およびマニラ → 頭山満（1916年5月）。D. Bourdeau が暫定的に公表した表[1]で、ここで裏付けられた。'],
        laisaosang1915: ['「Laisaosang」表', '東京（頭山満名義）→ 上海「Laisaosang」、および上海 →「Rosamonde」、1915年1〜2月。2026年10月に復元。'],
        newyork1915: ['「ニューヨーク」表', 'ニューヨーク → 孫文、1915年2月。2026年10月に復元。'],
        k30: ['「Thirtieth」表', '上海 →「Rosamonde」および東京 →「Junzaburo」、1915年2〜3月。平文の標識「Thirtieth」。2026年10月に復元。'],
        shanghai1916: ['「上海」表', '上海 ↔ 東京（「Rosamonde」、山田純三郎）、1916年2〜4月。D. Bourdeau が公表した表[1]。'],
        k13: ['「Thirteenth」表', '東京 →「Junzaburo」、1916年2〜3月。平文の標識「Thirteenth」。2026年10月に復元。'],
        seito1916: ['「青島」表', '青島 ↔ 東京（居正、萱野長知）、1916年3〜4月。D. Bourdeau が公表した表[1]。'],
        manila1916: ['「マニラ」表', '東京 ↔ マニラ、1916年3月。D. Bourdeau が公表した表[1]。'],
        sanfran1916: ['「サンフランシスコ」表', 'サンフランシスコ →「Dr Sunwen」、東京、1916年3月。署名「森」（林森）。D. Bourdeau が公表した表[1]。'],
        honolulu1916: ['「ホノルル」表、「Aloha」変種', 'ホノルル → 東京、1916年4月30日。標識「Aloha」。D. Bourdeau が公表した表[1]で、ここでは w を v の別形として用いる。'],
        yamada1916: ['「山田」表——「Thirtyseventh」', '東京 ↔ 上海（「Junzaburo」、「Linwailuk」）、1916年5〜6月。多くに平文の標識「Thirtyseventh」。D. Bourdeau が公表した表[1]。'],
        k38: ['「Thirtyeight」表', '東京 →「Junzaburo」、1916年5月11〜12日。平文の標識「Thirtyeight」。2026年10月に復元。'],
        h16: ['黄興の表', '東京（黄興）→「Junzaburo」（標識なし）および上海 →「Ylchang」（黄興）、1916年5月末〜6月。2026年10月に復元。黄興の別の電報（1916年5月25日、林虎・李根源宛）の三仮名コードとは別物である。その方式は D. Bourdeau が、対応の公式は S. Tomokiyo が明らかにした[22, 23]。']
      },
      rosamonde: ['ロザモンドの暗号英語（1915–1916年）', '<p>孫文と宋慶齢のあいだの、文字の相互置換で暗号化した英語の電報二十通ほど。別ページで紹介する：<a href="rosamonde.html">ロザモンド電報</a>。</p>'],
      count: '{n} 通', count1: '1 通'
    }
  }
};
