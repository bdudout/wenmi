// Page « Télégrammes » : classement par système de chiffrement, puis par date (séance YC, 15/10/2026).
// Chaque fiche des corpus (corpus.js, corpus-c1916.js, corpus-n1916.js, corpus-t1915.js, corpus-f1916.js) est rattachée
// à un système par son corpus et sa clé (m.grid) ; voir MAP. Textes en 5 langues ; [n] renvoie à la page Sources.
window.WENMI_SYSTEMS = {
  // corpus → { clé : système }
  map: {
    CORPUS: { G0: 'G0', Y0: 'Y0' },
    C1916: { manila1916: 'manila1916', shanghai1916: 'shanghai1916', seito1916: 'seito1916', yamada1916: 'yamada1916' },
    N1916: { honolulu1916w: 'honolulu1916', yamada1916: 'yamada1916', yamada1916w: 'yamada1916', man2: 'manila1916b', k38: 'k38', h16: 'h16' },
    T1915: { manila1916b: 'manila1916b', laisaosang1915: 'laisaosang1915', newyork1915: 'newyork1915', k30: 'k30', shanghai1916: 'shanghai1916', sanfran1916: 'sanfran1916' },
    F1916: { shanghai1916: 'shanghai1916', k13: 'k13', seito1916: 'seito1916', manila1916: 'manila1916', sanfran1916: 'sanfran1916' },
    NUM1916: { gongmi: 'gongmi', rongmi: 'rongmi', chenmi: 'chenmi', qianmi: 'qianmi', gaimusho: 'gaimusho', clair: 'clair' }
  },
  year: { CORPUS: 1916, C1916: 1916, N1916: 1916, T1915: 1915, F1916: 1916, NUM1916: 1916 },
  // jour approché pour le classement (date du formulaire illisible ; cf. tools/form_times.py)
  sortDay: { '1915-02p23': 1, '1915-02ny': 24 },
  groups: [
    { id: 'wenmi', systems: ['G0', 'Y0'] },
    { id: 'condensers', anchors: ['c1916', 'n1916', 't1915', 'f1916'],
      systems: ['manila1916b', 'laisaosang1915', 'newyork1915', 'k30', 'shanghai1916', 'k13', 'seito1916', 'manila1916', 'sanfran1916', 'honolulu1916', 'yamada1916', 'k38', 'h16'] },
    { id: 'numeric', anchors: ['num1916'], systems: ['gaimusho', 'gongmi', 'rongmi', 'chenmi', 'qianmi', 'clair'] }
  ],
  text: {
    fr: {
      toc: 'Les systèmes',
      groups: {
        wenmi: ['Le Wenmi (1916) : deux grilles de syllabes', '<p>Les télégrammes chiffrés de Zhao Shen (趙伸), commissaire du Conseil des affaires militaires à Tokyo, de juin à novembre 1916. Deux canaux, chacun avec sa grille : chaque syllabe donne un chiffre des dizaines et un chiffre des unités, et deux syllabes un code télégraphique chinois. Grilles retrouvées en octobre 2026 (voir la <a href="method.html">Méthode</a>).</p>'],
        condensers: ['Les condensateurs (1915–1916) : une table par correspondant', '<p>Chaque syllabe de deux lettres (consonne + voyelle) donne deux chiffres, et deux syllabes un code télégraphique chinois ; chaque correspondant de Sun Yat-sen a sa table. Les tables sont classées par date de leur premier télégramme, et les télégrammes par date dans chaque table. Une partie de ces télégrammes (mars–mai 1916) a été transcrite et déchiffrée par D. Bourdeau[1, 2] : les lettres sont alors celles de la transcription publiée, rectifiées sur les scans, et les caractères corrigés sont soulignés en vert (détail : <a href="relecture.html">Condensateurs 1916</a>). Les autres, absents des transcriptions publiées, ont été lus sur les scans par Claude et relus par Brice Dudout ; l\'intitulé « Lettres du formulaire » de chaque fiche précise la provenance.</p>'],
        numeric: ['Les codes numériques (juin 1916) : 共密, 容密, 辰密 et 乾密', '<p>Des télégrammes écrits en groupes de quatre chiffres, entre Tokyo (Huang Xing, Zhang Xiaozhun) et Shanghai, en juin 1916. Le premier groupe de deux codes est un préfixe en clair qui nomme le système (<span lang="zh-Hant">共密</span>, <span lang="zh-Hant">容密</span>) ; le reste est chiffré. Chaque chiffre lu est remplacé selon son rang, puis une constante est soustraite ou ajoutée avec retenues ; le résultat est un code télégraphique chinois. Clés reconstruites en octobre 2026 ; lecture des grilles par colonnes proposée par Brice Dudout. Le troisième, <span lang="zh-Hant">辰密</span>, renumérote les pages du code (nombres sans zéro) et permute dizaines et unités. Détails, scans et traductions alignées : pages <a href="gongmi.html">共密</a>, <a href="rongmi.html">容密</a> et <a href="chenmi.html">辰密</a>. Dans la version lisible, les caractères proposés sont soulignés : « probable » quand une variante du groupe à un seul chiffre près les donne, « possible » quand seul le contexte les appuie.</p>']
      },
      sys: {
        G0: ['Grille G0 — « 文密 »', 'Tokyo → Conseil des affaires militaires (Zhaoqing) et Shanghai, juin–septembre 1916. Grille de 20 consonnes × 5 voyelles en coordonnées, retrouvée en octobre 2026.'],
        Y0: ['Grille Y0 — indicateur « Cg »', 'Tokyo ↔ Yunnan, juillet–novembre 1916. Grille de 17 consonnes × 6 voyelles (y compris y), retrouvée en octobre 2026.'],
        manila1916b: ['Table « Manille » (seconde clé)', 'Tokyo → Manille (6 janvier 1915) et Manille → Tōyama Mitsuru (mai 1916). Table publiée à titre provisoire par D. Bourdeau[1], confirmée ici.'],
        laisaosang1915: ['Table « Laisaosang »', 'Tokyo (au nom de Tōyama Mitsuru) → « Laisaosang », Shanghai, et Shanghai → « Rosamonde », janvier–février 1915. Table retrouvée en octobre 2026. Également attestée le <a href="telegrams.html#tinedits-c39-b45t">28 juin 1914</a>.'],
        newyork1915: ['Table « New York »', 'New York → Sun Yat-sen, février 1915. Table retrouvée en octobre 2026. Également attestée de San Francisco le <a href="telegrams.html#tinedits-c39-b51b">5 juillet 1914</a>.'],
        k30: ['Table « Thirtieth »', 'Shanghai → « Rosamonde » et Tokyo → « Junzaburo », février–mai 1915 ; indicateur en clair « Thirtieth ». Table retrouvée en octobre 2026.'],
        shanghai1916: ['Table « Shanghai »', 'Shanghai ↔ Tokyo (« Rosamonde », Yamada Junzaburō), juin 1915–avril 1916. Table publiée par D. Bourdeau[1]. Également attestée de Changchun le <a href="telegrams.html#tinedits-c39-m10">31 juillet 1914</a>.'],
        k13: ['Table « Thirteenth »', 'Tokyo → « Junzaburo », février–mars 1916 ; indicateur en clair « Thirteenth ». Table retrouvée en octobre 2026.'],
        seito1916: ['Table « Qingdao »', 'Qingdao ↔ Tokyo (Ju Zheng, Kayano Nagatomo), mars–avril 1916. Table publiée par D. Bourdeau[1].'],
        manila1916: ['Table « Manille »', 'Tokyo ↔ Manille, mars 1916. Table publiée par D. Bourdeau[1].'],
        sanfran1916: ['Table « San Francisco »', 'San Francisco → « Dr Sunwen », Tokyo, octobre 1915–avril 1916 ; signé 森 (Lin Sen). Table publiée par D. Bourdeau[1]. Également attestée le <a href="telegrams.html#tinedits-c39-m17">18 septembre 1914</a>.'],
        honolulu1916: ['Table « Honolulu », variante « Aloha »', 'Honolulu → Tokyo, 30 avril 1916 ; indicateur « Aloha ». Table publiée par D. Bourdeau[1], ici avec w comme seconde forme de v.'],
        yamada1916: ['Table « Yamada » — « Thirtyseventh »', 'Tokyo ↔ Shanghai (« Junzaburo », « Linwailuk »), mai–juin 1916 ; indicateur en clair « Thirtyseventh » sur la plupart. Table publiée par D. Bourdeau[1].'],
        k38: ['Table « Thirtyeight »', 'Tokyo → « Junzaburo », 11–12 mai 1916 ; indicateur en clair « Thirtyeight ». Table retrouvée en octobre 2026.'],
        h16: ['Table de Huang Xing', 'Tokyo (Huang Xing) → « Junzaburo », sans indicateur, et Shanghai → « Ylchang » (Huang Xing), fin mai – juin 1916. Table retrouvée en octobre 2026. À ne pas confondre avec le code à trois kana d\'un autre télégramme de Huang Xing (25 mai 1916, à Lin Hu et Li Genyuan), dont le système a été identifié par D. Bourdeau et la formule par S. Tomokiyo[22, 23].'],
        gongmi: ['Clé « 共密 » (C51)', 'Tokyo ↔ Shanghai, 10–16 juin 1916 ; Huang Xing, Zhang Ji. Dizaines remplacées (0→9, 1→7, 2→6, 3→1, 4→4, 5→0, 6→5, 7→2, 8→8, 9→3), puis P = 9000 − C. Clé reconstruite par Codex en octobre 2026 (voir la page <a href="gongmi.html">共密</a>).'],
        rongmi: ['Clé « 容密 » (v2)', 'Tokyo ↔ Shanghai, 8–29 juin 1916 ; Zhang Xiaozhun, Huang Xing, Lü Gongwang, Yin Ruli, Ge Jing’en, Huang Fu. Chaque chiffre est remplacé selon son rang, puis P = C + 0901 avec retenues. Clé retrouvée en octobre 2026 (voir la page <a href="rongmi.html">容密</a> et la <a href="method.html#rongmi">méthode</a>).'],
        gaimusho: ['Tables du ministère japonais des Affaires étrangères (N01)', 'Shanghai → Tokyo (青山南町三ノ五三), mai 1916 ; appel des amis de Shanghai à Huang Xing. Sans préfixe. La clé est donnée par deux tables de déchiffrement sur papier du 外務省 conservées dans le même dossier (JACAR B03050089200, PDF 16, juin 1916) : elle est identique à celle que notre recherche avait trouvée sans elles (voir la <a href="method.html#gaimusho">méthode</a>) [27].'],
        qianmi: ['Clé « 乾密 » (C104)', 'Tokyo (青山南町三ノ五三) → Shanghai, 6–9 juin 1916 ; Huang Xing. Livre « 明密 » renuméroté : page = page écrite − 11, colonnes et lignes permutées. Modèle de clé : idée de S. Tomokiyo (Cryptiana) [22] ; clé retrouvée en octobre 2026 (voir la page <a href="qianmi.html">乾密</a> et la <a href="method.html#qianmi">méthode</a>).'],
        chenmi: ['Clé « 辰密 » (C92)', 'Tokyo → Shanghai (« ヒツキン », 霞飛路 277), 3–13 juin 1916 ; Huang Xing, Zhang Xiaozhun, le groupe hunanais de Shanghai. Pages renumérotées à rebours sur les nombres sans zéro (99 = page 00), dizaines et unités permutées, unité 9 = 10. Clé retrouvée en octobre 2026 (voir la page <a href="chenmi.html">辰密</a> et la <a href="method.html#chenmi">méthode</a>).'],
        clair: ['En clair', 'Télégrammes du même dossier envoyés sans chiffrement, directement en code télégraphique chinois : la réponse de Li Yuanhong à Huang Xing (14 juin), une lettre de Huang Xing à Tan Renfeng sur Li Yuanhong, un télégramme de Huang Xing sur le Shaanxi, un télégramme vers Mukden et un bref message signé 亞.']
      },
      rosamonde: ['L\'anglais chiffré de Rosamonde (1915–1916)', '<p>Vingt-deux télégrammes en anglais, chiffrés par une substitution réciproque de lettres, entre Sun Yat-sen et Soong Ching-ling : présentés sur une page à part, <a href="rosamonde.html">Les télégrammes de Rosamonde</a>.</p>'],
      count: '{n} télégrammes', count1: '1 télégramme'
    },
    en: {
      toc: 'The systems',
      groups: {
        wenmi: ['The Wenmi (1916): two syllable grids', '<p>The enciphered telegrams of Zhao Shen (趙伸), commissioner of the Military Affairs Council in Tokyo, June to November 1916. Two channels, each with its own grid: each syllable gives a tens digit and a units digit, and two syllables a Chinese telegraph code. Grids recovered in October 2026 (see the <a href="method.html">Method</a>).</p>'],
        condensers: ['The condensers (1915–1916): one table per correspondent', '<p>Each two-letter syllable (consonant + vowel) gives two digits, and two syllables a Chinese telegraph code; each of Sun Yat-sen\'s correspondents has his own table. Tables are ordered by the date of their first telegram, and telegrams by date within each table. Some of these telegrams (March–May 1916) were transcribed and deciphered by D. Bourdeau[1, 2]: their letters are those of the published transcription, rectified on the scans, and corrected characters are underlined in green (details: <a href="relecture.html">1916 condensers</a>). The others, absent from the published transcriptions, were read on the scans by Claude and reread by Brice Dudout; the “Letters of the form” label of each card gives the provenance.</p>'],
        numeric: ['The numeric codes (June 1916): Gongmi, Rongmi, Chenmi and Qianmi', '<p>Telegrams written in groups of four digits, between Tokyo (Huang Xing, Zhang Xiaozhun) and Shanghai, in June 1916. The first two codes are a clear prefix naming the system (<span lang="zh-Hant">共密</span>, <span lang="zh-Hant">容密</span>); the rest is enciphered. Each digit read is replaced according to its place, then a constant is subtracted or added with carries; the result is a Chinese telegraph code. Keys reconstructed in October 2026; column reading of the grids proposed by Brice Dudout. The third, <span lang="zh-Hant">辰密</span>, renumbers the code’s pages (numbers without a zero) and permutes tens and units. Details, scans and aligned translations: the <a href="gongmi.html">Gongmi</a>, <a href="rongmi.html">Rongmi</a> and <a href="chenmi.html">Chenmi</a> pages. In the readable version, proposed characters are underlined: “probable” when a variant of the group differing by a single digit gives them, “possible” when only context supports them.</p>']
      },
      sys: {
        G0: ['Grid G0 — “文密”', 'Tokyo → Military Affairs Council (Zhaoqing) and Shanghai, June–September 1916. Coordinate grid of 20 consonants × 5 vowels, recovered in October 2026.'],
        Y0: ['Grid Y0 — indicator “Cg”', 'Tokyo ↔ Yunnan, July–November 1916. Grid of 17 consonants × 6 vowels (including y), recovered in October 2026.'],
        manila1916b: ['“Manila” table (second key)', 'Tokyo → Manila (6 January 1915) and Manila → Tōyama Mitsuru (May 1916). Table published tentatively by D. Bourdeau[1], confirmed here.'],
        laisaosang1915: ['“Laisaosang” table', 'Tokyo (in the name of Tōyama Mitsuru) → “Laisaosang”, Shanghai, and Shanghai → “Rosamonde”, January–February 1915. Table recovered in October 2026. Also attested on <a href="telegrams.html#tinedits-c39-b45t">28 June 1914</a>.'],
        newyork1915: ['“New York” table', 'New York → Sun Yat-sen, February 1915. Table recovered in October 2026. Also attested from San Francisco on <a href="telegrams.html#tinedits-c39-b51b">5 July 1914</a>.'],
        k30: ['“Thirtieth” table', 'Shanghai → “Rosamonde” and Tokyo → “Junzaburo”, February–May 1915; clear indicator “Thirtieth”. Table recovered in October 2026.'],
        shanghai1916: ['“Shanghai” table', 'Shanghai ↔ Tokyo (“Rosamonde”, Yamada Junzaburō), June 1915–April 1916. Table published by D. Bourdeau[1]. Also attested from Changchun on <a href="telegrams.html#tinedits-c39-m10">31 July 1914</a>.'],
        k13: ['“Thirteenth” table', 'Tokyo → “Junzaburo”, February–March 1916; clear indicator “Thirteenth”. Table recovered in October 2026.'],
        seito1916: ['“Qingdao” table', 'Qingdao ↔ Tokyo (Ju Zheng, Kayano Nagatomo), March–April 1916. Table published by D. Bourdeau[1].'],
        manila1916: ['“Manila” table', 'Tokyo ↔ Manila, March 1916. Table published by D. Bourdeau[1].'],
        sanfran1916: ['“San Francisco” table', 'San Francisco → “Dr Sunwen”, Tokyo, October 1915–April 1916; signed 森 (Lin Sen). Table published by D. Bourdeau[1]. Also attested on <a href="telegrams.html#tinedits-c39-m17">18 September 1914</a>.'],
        honolulu1916: ['“Honolulu” table, “Aloha” variant', 'Honolulu → Tokyo, 30 April 1916; indicator “Aloha”. Table published by D. Bourdeau[1], here with w as a second form of v.'],
        yamada1916: ['“Yamada” table — “Thirtyseventh”', 'Tokyo ↔ Shanghai (“Junzaburo”, “Linwailuk”), May–June 1916; clear indicator “Thirtyseventh” on most. Table published by D. Bourdeau[1].'],
        k38: ['“Thirtyeight” table', 'Tokyo → “Junzaburo”, 11–12 May 1916; clear indicator “Thirtyeight”. Table recovered in October 2026.'],
        h16: ['Huang Xing\'s table', 'Tokyo (Huang Xing) → “Junzaburo”, without indicator, and Shanghai → “Ylchang” (Huang Xing), late May – June 1916. Table recovered in October 2026. Not to be confused with the three-kana code of another telegram of Huang Xing (25 May 1916, to Lin Hu and Li Genyuan), whose system was identified by D. Bourdeau and whose formula by S. Tomokiyo[22, 23].'],
        gongmi: ['“Gongmi” (共密) key (C51)', 'Tokyo ↔ Shanghai, 10–16 June 1916; Huang Xing, Zhang Ji. Tens digit replaced (0→9, 1→7, 2→6, 3→1, 4→4, 5→0, 6→5, 7→2, 8→8, 9→3), then P = 9000 − C. Key reconstructed by Codex in October 2026 (see the <a href="gongmi.html">Gongmi</a> page).'],
        rongmi: ['“Rongmi” (容密) key (v2)', 'Tokyo ↔ Shanghai, 8–29 June 1916; Zhang Xiaozhun, Huang Xing, Lü Gongwang, Yin Ruli, Ge Jing’en, Huang Fu. Each digit is replaced according to its place, then P = C + 0901 with carries. Key recovered in October 2026 (see the <a href="rongmi.html">Rongmi</a> page and the <a href="method.html#rongmi">method</a>).'],
        gaimusho: ['Japanese Foreign Ministry tables (N01)', 'Shanghai → Tokyo (青山南町三ノ五三), May 1916; an appeal from the Shanghai friends to Huang Xing. No prefix. The key is given by two decipherment tables on 外務省 paper kept in the same file (JACAR B03050089200, PDF 16, June 1916): it is identical to the key our search had found without them (see the <a href="method.html#gaimusho">method</a>) [27].'],
        qianmi: ['“Qianmi” (乾密) key (C104)', 'Tokyo (青山南町三ノ五三) → Shanghai, 6–9 June 1916; Huang Xing. Renumbered “明密” book: page = written page − 11, columns and rows permuted. Key model: S. Tomokiyo’s idea (Cryptiana) [22]; key recovered in October 2026 (see the <a href="qianmi.html">Qianmi</a> page and the <a href="method.html#qianmi">method</a>).'],
        chenmi: ['“Chenmi” (辰密) key (C92)', 'Tokyo → Shanghai (“ヒツキン”, 277 Avenue Joffre), 3–13 June 1916; Huang Xing, Zhang Xiaozhun, the Hunanese group in Shanghai. Pages renumbered backwards over the numbers without a zero (99 = page 00), tens and units permuted, units 9 = 10. Key recovered in October 2026 (see the <a href="chenmi.html">Chenmi</a> page and the <a href="method.html#chenmi">method</a>).'],
        clair: ['In clear', 'Telegrams from the same file sent without encipherment, directly in Chinese telegraph code: Li Yuanhong’s reply to Huang Xing (14 June), Huang Xing’s message to Tan Renfeng about Li Yuanhong, a telegram of Huang Xing about Shaanxi, one to Mukden, and a short message signed 亞.']
      },
      rosamonde: ['Rosamonde\'s enciphered English (1915–1916)', '<p>Twenty-two telegrams in English, enciphered by a reciprocal letter substitution, between Sun Yat-sen and Soong Ching-ling: presented on a separate page, <a href="rosamonde.html">The Rosamonde telegrams</a>.</p>'],
      count: '{n} telegrams', count1: '1 telegram'
    },
    'zh-Hant': {
      toc: '加密系統',
      groups: {
        wenmi: ['文密（1916年）：兩張音節表', '<p>1916年6月至11月，軍務院駐東京委員趙伸的加密電報。兩條通道，各用一張表：每個音節給出十位數和個位數，兩個音節組成一個漢字電碼。兩張表於2026年10月復原（見<a href="method.html">破譯方法</a>）。</p>'],
        condensers: ['壓縮碼（1915–1916年）：每位通信者一張表', '<p>每個兩字母音節（輔音＋元音）代表兩位數字，兩個音節組成一個漢字電碼；孫中山的每位通信者各有一張表。各表按其第一封電報的日期排列，表內電報按日期排列。其中一部分（1916年3月至5月）已由 D. Bourdeau 轉錄並破譯[1, 2]：字母取自已發表的轉錄，並依掃描件訂正，訂正的字以綠色底線標出（詳見<a href="relecture.html">1916年壓縮碼</a>）。其餘電報未見於已發表的轉錄，由 Claude 依掃描件讀出，再由 Brice Dudout 複核；各電報卡片上的「電報紙上的字母」一欄註明來源。</p>'],
        numeric: ['數字密碼（1916年6月）：共密、容密、辰密與乾密', '<p>1916年6月東京（黃興、張孝準）與上海之間以四位數字組書寫的電報。開頭兩個電碼是標明系統的明文前綴（<span lang="zh-Hant">共密</span>、<span lang="zh-Hant">容密</span>），其餘為密文。每位數字按其數位替換，再帶進位減去或加上一個常數，所得即中文電碼。密鑰於2026年10月復原；按列讀取方格的讀法由 Brice Dudout 提出。第三種<span lang="zh-Hant">辰密</span>則將電碼重新編頁（不含零的數）並置換十位與個位。詳情、掃描件與對照譯文見<a href="gongmi.html">共密</a>、<a href="rongmi.html">容密</a>與<a href="chenmi.html">辰密</a>頁面。可讀版本中，推定字加底線：組內僅改一位數字即得該字者為「較可能」，僅憑文意者為「可能」。</p>']
      },
      sys: {
        G0: ['G0 表——「文密」', '東京 → 軍務院（肇慶）及上海，1916年6月至9月。20個輔音 × 5個元音的座標表，2026年10月復原。'],
        Y0: ['Y0 表——標記「Cg」', '東京 ↔ 雲南，1916年7月至11月。17個輔音 × 6個元音（含 y）的表，2026年10月復原。'],
        manila1916b: ['「馬尼拉」表（第二密鑰）', '東京 → 馬尼拉（1915年1月6日）及馬尼拉 → 頭山滿（1916年5月）。D. Bourdeau 暫定發表的表[1]，此處得到證實。'],
        laisaosang1915: ['「Laisaosang」表', '東京（以頭山滿名義）→ 上海「Laisaosang」，及上海 →「Rosamonde」，1915年1月至2月。2026年10月復原。 亦見於<a href="telegrams.html#tinedits-c39-b45t">1914年6月28日</a>。'],
        newyork1915: ['「紐約」表', '紐約 → 孫中山，1915年2月。2026年10月復原。 亦見於<a href="telegrams.html#tinedits-c39-b51b">1914年7月5日</a>舊金山來電。'],
        k30: ['「Thirtieth」表', '上海 →「Rosamonde」及東京 →「Junzaburo」，1915年2月至5月；明碼標記「Thirtieth」。2026年10月復原。'],
        shanghai1916: ['「上海」表', '上海 ↔ 東京（「Rosamonde」、山田純三郎），1915年6月至1916年4月。D. Bourdeau 發表的表[1]。 亦見於<a href="telegrams.html#tinedits-c39-m10">1914年7月31日</a>長春來電。'],
        k13: ['「Thirteenth」表', '東京 →「Junzaburo」，1916年2月至3月；明碼標記「Thirteenth」。2026年10月復原。'],
        seito1916: ['「青島」表', '青島 ↔ 東京（居正、萱野長知），1916年3月至4月。D. Bourdeau 發表的表[1]。'],
        manila1916: ['「馬尼拉」表', '東京 ↔ 馬尼拉，1916年3月。D. Bourdeau 發表的表[1]。'],
        sanfran1916: ['「舊金山」表', '舊金山 →「Dr Sunwen」，東京，1915年10月至1916年4月；署名「森」（林森）。D. Bourdeau 發表的表[1]。 亦見於<a href="telegrams.html#tinedits-c39-m17">1914年9月18日</a>。'],
        honolulu1916: ['「檀香山」表，「Aloha」變體', '檀香山 → 東京，1916年4月30日；標記「Aloha」。D. Bourdeau 發表的表[1]，此處 w 作為 v 的第二寫法。'],
        yamada1916: ['「山田」表——「Thirtyseventh」', '東京 ↔ 上海（「Junzaburo」、「Linwailuk」），1916年5月至6月；多數帶明碼標記「Thirtyseventh」。D. Bourdeau 發表的表[1]。'],
        k38: ['「Thirtyeight」表', '東京 →「Junzaburo」，1916年5月11至12日；明碼標記「Thirtyeight」。2026年10月復原。'],
        h16: ['黃興的表', '東京（黃興）→「Junzaburo」（無標記）及上海 →「Ylchang」（黃興），1916年5月底至6月。2026年10月復原。勿與黃興另一封電報（1916年5月25日致林虎、李根源）的三假名電碼混淆：該系統由 D. Bourdeau 識別，其對應公式由 S. Tomokiyo 找出[22, 23]。'],
        gongmi: ['「共密」密鑰（C51）', '東京↔上海，1916年6月10–16日；黃興、張繼。替換十位數（0→9、1→7、2→6、3→1、4→4、5→0、6→5、7→2、8→8、9→3），再計算P = 9000 − C。密鑰由 Codex 於2026年10月復原（見<a href="gongmi.html">共密</a>頁面）。'],
        rongmi: ['「容密」密鑰（v2）', '東京↔上海，1916年6月8–29日；張孝準、黃興、呂公望、殷汝驪、葛敬恩、黃郛。每位數字按其數位替換，再以進位計算P = C + 0901。密鑰於2026年10月找到（見<a href="rongmi.html">容密</a>頁面及<a href="method.html#rongmi">破譯方法</a>）。'],
        gaimusho: ['日本外務省解讀表（N01）', '上海→東京（青山南町三ノ五三），1916年5月；上海同人致黃興的呼籲。無前綴。密鑰見於同一卷宗中兩張外務省用紙的解讀表（JACAR B03050089200，PDF第16頁，1916年6月），與我們未見此表時搜尋所得的密鑰完全相同（見<a href="method.html#gaimusho">破譯方法</a>）[27]。'],
        qianmi: ['「乾密」密鑰（C104）', '東京（青山南町三ノ五三）→上海，1916年6月6–9日；黃興。重新編號的「明密」電碼本：頁＝所寫頁數−11，列與行置換。密鑰模型：S. Tomokiyo的構想（Cryptiana）[22]；密鑰於2026年10月找到（見<a href="qianmi.html">乾密</a>頁面及<a href="method.html#qianmi">破譯方法</a>）。'],
        chenmi: ['「辰密」密鑰（C92）', '東京→上海（「ヒツキン」，霞飛路277號），1916年6月3–13日；黃興、張孝準、上海湘籍諸人。以不含零的數倒數編頁（99＝第00頁），十位與個位置換，個位9作10。密鑰於2026年10月找到（見<a href="chenmi.html">辰密</a>頁面及<a href="method.html#chenmi">破譯方法</a>）。'],
        clair: ['明碼', '同一卷宗中未加密、直接以中文電碼拍發的電報：黎元洪覆黃興電（6月14日）、黃興致譚人鳳論黎元洪電、黃興論陝事電、致奉天電及署名「亞」的短電。']
      },
      rosamonde: ['羅莎蒙德的加密英文（1915–1916年）', '<p>孫中山與宋慶齡之間二十二封以字母互換加密的英文電報，另見專頁：<a href="rosamonde.html">羅莎蒙德電報</a>。</p>'],
      count: '{n} 封電報', count1: '1 封電報'
    },
    'zh-Hans': {
      toc: '加密系统',
      groups: {
        wenmi: ['文密（1916年）：两张音节表', '<p>1916年6月至11月，军务院驻东京委员赵伸的加密电报。两条通道，各用一张表：每个音节给出十位数和个位数，两个音节组成一个汉字电码。两张表于2026年10月复原（见<a href="method.html">破译方法</a>）。</p>'],
        condensers: ['压缩码（1915–1916年）：每位通信者一张表', '<p>每个两字母音节（辅音＋元音）代表两位数字，两个音节组成一个汉字电码；孙中山的每位通信者各有一张表。各表按其第一封电报的日期排列，表内电报按日期排列。其中一部分（1916年3月至5月）已由 D. Bourdeau 转录并破译[1, 2]：字母取自已发表的转录，并依扫描件订正，订正的字以绿色下划线标出（详见<a href="relecture.html">1916年压缩码</a>）。其余电报未见于已发表的转录，由 Claude 依扫描件读出，再由 Brice Dudout 复核；各电报卡片上的“电报纸上的字母”一栏注明来源。</p>'],
        numeric: ['数字密码（1916年6月）：共密、容密、辰密与乾密', '<p>1916年6月东京（黄兴、张孝准）与上海之间以四位数字组书写的电报。开头两个电码是标明系统的明文前缀（<span lang="zh-Hant">共密</span>、<span lang="zh-Hant">容密</span>），其余为密文。每位数字按其数位替换，再带进位减去或加上一个常数，所得即中文电码。密钥于2026年10月复原；按列读取方格的读法由 Brice Dudout 提出。第三种<span lang="zh-Hant">辰密</span>则将电码重新编页（不含零的数）并置换十位与个位。详情、扫描件与对照译文见<a href="gongmi.html">共密</a>、<a href="rongmi.html">容密</a>与<a href="chenmi.html">辰密</a>页面。可读版本中，推定字加下划线：组内仅改一位数字即得该字者为“较可能”，仅凭文意者为“可能”。</p>']
      },
      sys: {
        G0: ['G0 表——“文密”', '东京 → 军务院（肇庆）及上海，1916年6月至9月。20个辅音 × 5个元音的坐标表，2026年10月复原。'],
        Y0: ['Y0 表——标记“Cg”', '东京 ↔ 云南，1916年7月至11月。17个辅音 × 6个元音（含 y）的表，2026年10月复原。'],
        manila1916b: ['“马尼拉”表（第二密钥）', '东京 → 马尼拉（1915年1月6日）及马尼拉 → 头山满（1916年5月）。D. Bourdeau 暂定发表的表[1]，此处得到证实。'],
        laisaosang1915: ['“Laisaosang”表', '东京（以头山满名义）→ 上海“Laisaosang”，及上海 →“Rosamonde”，1915年1月至2月。2026年10月复原。 亦见于<a href="telegrams.html#tinedits-c39-b45t">1914年6月28日</a>。'],
        newyork1915: ['“纽约”表', '纽约 → 孙中山，1915年2月。2026年10月复原。 亦见于<a href="telegrams.html#tinedits-c39-b51b">1914年7月5日</a>旧金山来电。'],
        k30: ['“Thirtieth”表', '上海 →“Rosamonde”及东京 →“Junzaburo”，1915年2月至5月；明码标记“Thirtieth”。2026年10月复原。'],
        shanghai1916: ['“上海”表', '上海 ↔ 东京（“Rosamonde”、山田纯三郎），1915年6月至1916年4月。D. Bourdeau 发表的表[1]。 亦见于<a href="telegrams.html#tinedits-c39-m10">1914年7月31日</a>长春来电。'],
        k13: ['“Thirteenth”表', '东京 →“Junzaburo”，1916年2月至3月；明码标记“Thirteenth”。2026年10月复原。'],
        seito1916: ['“青岛”表', '青岛 ↔ 东京（居正、萱野长知），1916年3月至4月。D. Bourdeau 发表的表[1]。'],
        manila1916: ['“马尼拉”表', '东京 ↔ 马尼拉，1916年3月。D. Bourdeau 发表的表[1]。'],
        sanfran1916: ['“旧金山”表', '旧金山 →“Dr Sunwen”，东京，1915年10月至1916年4月；署名“森”（林森）。D. Bourdeau 发表的表[1]。 亦见于<a href="telegrams.html#tinedits-c39-m17">1914年9月18日</a>。'],
        honolulu1916: ['“檀香山”表，“Aloha”变体', '檀香山 → 东京，1916年4月30日；标记“Aloha”。D. Bourdeau 发表的表[1]，此处 w 作为 v 的第二写法。'],
        yamada1916: ['“山田”表——“Thirtyseventh”', '东京 ↔ 上海（“Junzaburo”、“Linwailuk”），1916年5月至6月；多数带明码标记“Thirtyseventh”。D. Bourdeau 发表的表[1]。'],
        k38: ['“Thirtyeight”表', '东京 →“Junzaburo”，1916年5月11至12日；明码标记“Thirtyeight”。2026年10月复原。'],
        h16: ['黄兴的表', '东京（黄兴）→“Junzaburo”（无标记）及上海 →“Ylchang”（黄兴），1916年5月底至6月。2026年10月复原。勿与黄兴另一封电报（1916年5月25日致林虎、李根源）的三假名电码混淆：该系统由 D. Bourdeau 识别，其对应公式由 S. Tomokiyo 找出[22, 23]。'],
        gongmi: ['“共密”密钥（C51）', '东京↔上海，1916年6月10–16日；黄兴、张继。替换十位数（0→9、1→7、2→6、3→1、4→4、5→0、6→5、7→2、8→8、9→3），再计算P = 9000 − C。密钥由 Codex 于2026年10月复原（见<a href="gongmi.html">共密</a>页面）。'],
        rongmi: ['“容密”密钥（v2）', '东京↔上海，1916年6月8–29日；张孝准、黄兴、吕公望、殷汝骊、葛敬恩、黄郛。每位数字按其数位替换，再以进位计算P = C + 0901。密钥于2026年10月找到（见<a href="rongmi.html">容密</a>页面及<a href="method.html#rongmi">破译方法</a>）。'],
        gaimusho: ['日本外务省解读表（N01）', '上海→东京（青山南町三ノ五三），1916年5月；上海同人致黄兴的呼吁。无前缀。密钥见于同一卷宗中两张外务省用纸的解读表（JACAR B03050089200，PDF第16页，1916年6月），与我们未见此表时搜寻所得的密钥完全相同（见<a href="method.html#gaimusho">破译方法</a>）[27]。'],
        qianmi: ['“乾密”密钥（C104）', '东京（青山南町三ノ五三）→上海，1916年6月6–9日；黄兴。重新编号的“明密”电码本：页＝所写页数−11，列与行置换。密钥模型：S. Tomokiyo的构想（Cryptiana）[22]；密钥于2026年10月找到（见<a href="qianmi.html">乾密</a>页面及<a href="method.html#qianmi">破译方法</a>）。'],
        chenmi: ['“辰密”密钥（C92）', '东京→上海（“ヒツキン”，霞飞路277号），1916年6月3–13日；黄兴、张孝准、上海湘籍诸人。以不含零的数倒数编页（99＝第00页），十位与个位置换，个位9作10。密钥于2026年10月找到（见<a href="chenmi.html">辰密</a>页面及<a href="method.html#chenmi">破译方法</a>）。'],
        clair: ['明码', '同一卷宗中未加密、直接以中文电码拍发的电报：黎元洪复黄兴电（6月14日）、黄兴致谭人凤论黎元洪电、黄兴论陕事电、致奉天电及署名“亚”的短电。']
      },
      rosamonde: ['罗莎蒙德的加密英文（1915–1916年）', '<p>孙中山与宋庆龄之间二十二封以字母互换加密的英文电报，另见专页：<a href="rosamonde.html">罗莎蒙德电报</a>。</p>'],
      count: '{n} 封电报', count1: '1 封电报'
    },
    ja: {
      toc: '暗号方式',
      groups: {
        wenmi: ['文密（1916年）：二つの音節表', '<p>1916年6月から11月、東京駐在の軍務院委員・趙伸の暗号電報。二つの系統があり、それぞれ専用の表を使う。音節一つが十の位と一の位の数字を表し、音節二つで中国電信符号一つになる。二つの表は2026年10月に復元した（<a href="method.html">解読の方法</a>を参照）。</p>'],
        condensers: ['コンデンサー（1915–1916年）：通信相手ごとの表', '<p>二文字の音節（子音＋母音）一つが二桁の数字を表し、音節二つで中国電信符号一つになる。孫文の通信相手ごとに表が異なる。表は最初の電報の日付順、各表の中の電報も日付順に並べた。このうち一部（1916年3〜5月）は D. Bourdeau が翻字・解読している[1, 2]。その場合の文字は公表された翻字をスキャンで訂正したもので、訂正した字は緑の下線で示す（詳細：<a href="relecture.html">1916年のコンデンサー</a>）。残りは公表された翻字にない電報で、Claude がスキャンから読み、Brice Dudout が読み直した。各カードの「用紙の文字」の見出しに出所を記す。</p>'],
        numeric: ['数字暗号（1916年6月）：共密・容密・辰密・乾密', '<p>1916年6月、東京（黄興・張孝準）と上海の間で4桁の数字組で書かれた電報。最初の2つの電碼は方式を示す平文の前置き（<span lang="zh-Hant">共密</span>、<span lang="zh-Hant">容密</span>）で、残りが暗号文。各桁を位ごとに置き換え、繰り上がりつきで定数を引くか加えると中文電碼になる。鍵は2026年10月に復元。升目を列ごとに読む読み方はBrice Dudoutの提案。第三の<span lang="zh-Hant">辰密</span>は電碼の頁を（0を含まない数で）振り直し、十の位と一の位を置き換える。詳細・スキャン・対照訳は<a href="gongmi.html">共密</a>・<a href="rongmi.html">容密</a>・<a href="chenmi.html">辰密</a>のページ。読み下しでは推定字に下線を引く：組を1桁だけ変えるとその字になる場合は「可能性が高い」、文脈のみの場合は「可能性あり」。</p>']
      },
      sys: {
        G0: ['G0 表——「文密」', '東京 → 軍務院（肇慶）および上海、1916年6〜9月。子音20 × 母音5の座標表。2026年10月に復元。'],
        Y0: ['Y0 表——標識「Cg」', '東京 ↔ 雲南、1916年7〜11月。子音17 × 母音6（y を含む）の表。2026年10月に復元。'],
        manila1916b: ['「マニラ」表（第二の鍵）', '東京 → マニラ（1915年1月6日）およびマニラ → 頭山満（1916年5月）。D. Bourdeau が暫定的に公表した表[1]で、ここで裏付けられた。'],
        laisaosang1915: ['「Laisaosang」表', '東京（頭山満名義）→ 上海「Laisaosang」、および上海 →「Rosamonde」、1915年1〜2月。2026年10月に復元。 <a href="telegrams.html#tinedits-c39-b45t">1914年6月28日</a>にも確認。'],
        newyork1915: ['「ニューヨーク」表', 'ニューヨーク → 孫文、1915年2月。2026年10月に復元。 <a href="telegrams.html#tinedits-c39-b51b">1914年7月5日</a>のサンフランシスコ発にも確認。'],
        k30: ['「Thirtieth」表', '上海 →「Rosamonde」および東京 →「Junzaburo」、1915年2〜5月。平文の標識「Thirtieth」。2026年10月に復元。'],
        shanghai1916: ['「上海」表', '上海 ↔ 東京（「Rosamonde」、山田純三郎）、1915年6月〜1916年4月。D. Bourdeau が公表した表[1]。 <a href="telegrams.html#tinedits-c39-m10">1914年7月31日</a>の長春発にも確認。'],
        k13: ['「Thirteenth」表', '東京 →「Junzaburo」、1916年2〜3月。平文の標識「Thirteenth」。2026年10月に復元。'],
        seito1916: ['「青島」表', '青島 ↔ 東京（居正、萱野長知）、1916年3〜4月。D. Bourdeau が公表した表[1]。'],
        manila1916: ['「マニラ」表', '東京 ↔ マニラ、1916年3月。D. Bourdeau が公表した表[1]。'],
        sanfran1916: ['「サンフランシスコ」表', 'サンフランシスコ →「Dr Sunwen」、東京、1915年10月〜1916年4月。署名「森」（林森）。D. Bourdeau が公表した表[1]。 <a href="telegrams.html#tinedits-c39-m17">1914年9月18日</a>にも確認。'],
        honolulu1916: ['「ホノルル」表、「Aloha」変種', 'ホノルル → 東京、1916年4月30日。標識「Aloha」。D. Bourdeau が公表した表[1]で、ここでは w を v の別形として用いる。'],
        yamada1916: ['「山田」表——「Thirtyseventh」', '東京 ↔ 上海（「Junzaburo」、「Linwailuk」）、1916年5〜6月。多くに平文の標識「Thirtyseventh」。D. Bourdeau が公表した表[1]。'],
        k38: ['「Thirtyeight」表', '東京 →「Junzaburo」、1916年5月11〜12日。平文の標識「Thirtyeight」。2026年10月に復元。'],
        h16: ['黄興の表', '東京（黄興）→「Junzaburo」（標識なし）および上海 →「Ylchang」（黄興）、1916年5月末〜6月。2026年10月に復元。黄興の別の電報（1916年5月25日、林虎・李根源宛）の三仮名コードとは別物である。その方式は D. Bourdeau が、対応の公式は S. Tomokiyo が明らかにした[22, 23]。'],
        gongmi: ['「共密」の鍵（C51）', '東京↔上海、1916年6月10〜16日。黄興、張継。十の位を置き換え（0→9、1→7、2→6、3→1、4→4、5→0、6→5、7→2、8→8、9→3）、P = 9000 − C。鍵は2026年10月にCodexが復元（<a href="gongmi.html">共密</a>のページ参照）。'],
        rongmi: ['「容密」の鍵（v2）', '東京↔上海、1916年6月8〜29日。張孝準、黄興、呂公望、殷汝驪、葛敬恩、黄郛。各桁を位ごとに置き換え、繰り上がりつきでP = C + 0901。鍵は2026年10月に発見（<a href="rongmi.html">容密</a>のページと<a href="method.html#rongmi">方法</a>参照）。'],
        gaimusho: ['外務省の解読表（N01）', '上海→東京（青山南町三ノ五三）、1916年5月。上海の同志から黄興への呼びかけ。前置きなし。鍵は同じ綴りに残る外務省用紙の解読表2枚（JACAR B03050089200、PDF 16、1916年6月）に示され、私たちがそれを知らずに探索で得た鍵と完全に一致する（<a href="method.html#gaimusho">方法</a>参照）[27]。'],
        qianmi: ['「乾密」の鍵（C104）', '東京（青山南町三ノ五三）→上海、1916年6月6〜9日。黄興。番号を付け替えた「明密」電碼本：頁＝書かれた頁−11、列と行を置換。鍵のモデル：S. Tomokiyo氏の着想（Cryptiana）[22]。鍵は2026年10月に発見（<a href="qianmi.html">乾密</a>のページと<a href="method.html#qianmi">方法</a>参照）。'],
        chenmi: ['「辰密」の鍵（C92）', '東京→上海（「ヒツキン」、霞飛路277）、1916年6月3〜13日。黄興、張孝準、上海の湖南派。0を含まない数を逆に数えて頁とし（99＝00頁）、十の位と一の位を置換、一の位9＝10。鍵は2026年10月に発見（<a href="chenmi.html">辰密</a>のページと<a href="method.html#chenmi">方法</a>参照）。'],
        clair: ['平文', '同じ綴りのうち暗号化せず中文電碼で直接打たれた電報：黎元洪から黄興への返電（6月14日）、黎元洪について譚人鳳にあてた黄興の電報、陝西に関する黄興の電報、奉天宛ての電報、「亞」署名の短電。']
      },
      rosamonde: ['ロザモンドの暗号英語（1915–1916年）', '<p>孫文と宋慶齢のあいだの、文字の相互置換で暗号化した英語の電報二十二通。別ページで紹介する：<a href="rosamonde.html">ロザモンド電報</a>。</p>'],
      count: '{n} 通', count1: '1 通'
    }
  }
};
