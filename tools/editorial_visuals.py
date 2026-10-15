"""Responsive, source-linked reading aids. No generated historical claims or external assets."""
from html import escape
import re

from rosamonde_cipher_diagram import KEY

WORD = 'gowoisrjat'
DECODED = ''.join(KEY[c] for c in WORD)
assert DECODED == 'bemerciful'

# Shared dates and evidence links; translated labels below do not change the chronology.
EVENTS = [
    ('1915-02-17', '1915-02-17', 'rosamonde.html#1915', 0),
    ('1915-10-25', '1915-10-25', 'https://sswgw.org.cn/wwdc/szsww/4202.htm', 1),
    ('1915-12-25', '1915-12-25', 'history.html#chine', 1),
    ('1916-04', '1916-04 / 1916-05', 'rosamonde.html#1916', 1),
    ('1916-06-06', '1916-06-06', 'history.html#chine', 1),
    ('1916-06', '1916-06 → 1916-11', 'history.html#messages', 0),
    ('1917-06', '1917-06', 'telegrams.html#t0509a', 2),
]
TEXT = {
 'fr': {
  'timeline': '1915–1917 : se repérer dans les correspondances',
  'timeline_note': 'Repères sélectionnés, non à l’échelle. Les dates des documents sont distinctes de l’attribution de leurs auteurs.',
  'kinds': ['Télégrammes', 'Contexte historique', 'Chiffre non déchiffré'],
  'events': [
   'Premier télégramme de février présenté dans l’article Rosamonde. Attribution au couple par recoupements, non par les noms sur le formulaire.',
   'Mariage de Sun Yat-sen et Soong Ching-ling à Tokyo.',
   'Le Yunnan se soulève contre le projet impérial de Yuan Shikai.',
   'Sun revient à Shanghai ; Soong Ching-ling le rejoint le 19 mai 1916.',
   'Mort de Yuan Shikai.',
   'Correspondances de Zhao Shen : Wenmi vers le Conseil du Sud (G0), et canal du Yunnan (Y0).',
   'Sun ↔ Dai Jitao : un autre système, qui n’est pas déchiffré.'],
  'compare': 'Des mots en lettres latines, mais pas le même chiffre',
  'compare_note': 'Le code télégraphique public est une étape de codage, pas un secret. Le Wenmi de 1916 relève de la conversion en syllabes, avec deux grilles particulières.',
  'rows': [
   ['Rosamonde · 1915–1916', 'Anglais', 'Substitution réciproque des lettres', 'you ↔ hea', 'Une lettre remplace une lettre ; la même table sert dans les deux sens.'],
   ['Code télégraphique chinois', 'Caractère chinois', 'Répertoire public à quatre chiffres', '文 → 2429', 'Ce répertoire est public : il ne suffit pas, à lui seul, à cacher le texte.'],
   ['Condensateurs · plusieurs tables', 'Code chinois à quatre chiffres', 'Deux paires de chiffres → syllabes', '00–99 → CV', 'La table dépend du système employé. CV désigne une consonne et une voyelle.'],
   ['Wenmi 1916 · G0 / Y0', 'Code chinois à quatre chiffres', 'Deux grilles de syllabes distinctes', '報 → 1032 → fa | zi', 'Exemple G0 uniquement. Y0 emploie une autre grille : les tables ne sont pas interchangeables.']],
  'process': 'Du formulaire au sens : un exemple réel',
  'process_note': 'Rosamonde, Shanghai → Tokyo, 7 juillet 1915. Cet exemple emploie la substitution anglaise, pas la grille G0 du Wenmi.',
  'scan': '1 · Le document', 'scan_note': 'Copie japonaise conservée par JACAR : B03050087700, image 50. Cliquer pour agrandir.',
  'steps': ['2 · Transcrire le groupe', '3 · Appliquer la table', '4 · Séparer les mots et traduire'],
  'translation': '« Sois clément. »',
  'uncertain': 'Ce que l’exemple ne résout pas',
  'uncertain_note': 'Le texte publié garde une lacune après « Lovesick ». Un déchiffrement lisible ailleurs n’autorise pas à effacer ce passage incertain.',
  'read': 'Vérifier le texte et ses limites',
 },
 'en': {
  'timeline': '1915–1917: finding your way through the correspondence',
  'timeline_note': 'Selected milestones, not to scale. Document dates are separate from the attribution of their authors.',
  'kinds': ['Telegrams', 'Historical context', 'Undeciphered system'],
  'events': [
   'First February telegram presented in the Rosamonde article. Attribution to the couple rests on cross-checks, not names on the form.',
   'Sun Yat-sen and Soong Ching-ling marry in Tokyo.',
   'Yunnan rises against Yuan Shikai’s imperial project.',
   'Sun returns to Shanghai; Soong Ching-ling joins him on 19 May 1916.',
   'Death of Yuan Shikai.',
   'Zhao Shen’s correspondence: Wenmi to the southern Council (G0), and the Yunnan channel (Y0).',
   'Sun ↔ Dai Jitao: a different system, still undeciphered.'],
  'compare': 'Latin-letter words, but different systems',
  'compare_note': 'The public telegraph code is an encoding step, not a secret. The 1916 Wenmi uses conversion into syllables, with two particular grids.',
  'rows': [
   ['Rosamonde · 1915–1916', 'English', 'Reciprocal letter substitution', 'you ↔ hea', 'One letter replaces another; the same table works in both directions.'],
   ['Chinese telegraph code', 'Chinese character', 'Public four-digit directory', '文 → 2429', 'This directory is public: by itself it does not conceal the text.'],
   ['Condensers · several tables', 'Four-digit Chinese code', 'Two digit pairs → syllables', '00–99 → CV', 'The table depends on the system. CV means a consonant followed by a vowel.'],
   ['Wenmi 1916 · G0 / Y0', 'Four-digit Chinese code', 'Two distinct syllable grids', '報 → 1032 → fa | zi', 'G0 example only. Y0 uses a different grid: the tables are not interchangeable.']],
  'process': 'From the form to its meaning: a real example',
  'process_note': 'Rosamonde, Shanghai → Tokyo, 7 July 1915. This example uses the English substitution, not Wenmi’s G0 grid.',
  'scan': '1 · The document', 'scan_note': 'Japanese copy held by JACAR: B03050087700, image 50. Click to enlarge.',
  'steps': ['2 · Transcribe the group', '3 · Apply the table', '4 · Restore word boundaries'],
  'translation': '“Be merciful.”',
  'uncertain': 'What this example does not resolve',
  'uncertain_note': 'The published text retains a gap after “Lovesick”. Readable decipherment elsewhere does not justify erasing this uncertainty.',
  'read': 'Check the text and its limits',
 },
 'ja': {
  'timeline': '1915〜1917年：通信をたどる',
  'timeline_note': '主な出来事。時間の間隔は比例しない。史料の日付と筆者の推定は区別する。',
  'kinds': ['電報', '歴史的背景', '未解読の暗号'],
  'events': [
   'ロザモンドの記事に掲載した2月最初の電報。孫文と宋慶齢の通信という判断は、用紙上の実名ではなく照合に基づく。',
   '孫文と宋慶齢が東京で結婚。', '雲南が袁世凱の帝制計画に反対して蜂起。',
   '孫文が上海に戻り、宋慶齢が1916年5月19日に合流。', '袁世凱が死去。',
   '趙伸の通信。南方軍務院への文密（G0）と雲南系統（Y0）。',
   '孫文 ↔ 戴季陶。別の暗号方式で、未解読。'],
  'compare': '同じラテン文字でも、暗号方式は異なる',
  'compare_note': '公開電碼は符号化の段階であり、秘密そのものではない。1916年の文密は、二つの固有の表で音節に変換する。',
  'rows': [
   ['ロザモンド · 1915–1916', '英語', '文字を相互に置換', 'you ↔ hea', '一文字を別の文字に置き換える。同じ表で暗号化と復号を行う。'],
   ['中文電碼', '漢字', '公開の4桁番号表', '文 → 2429', '公開の表なので、これだけでは内容を隠せない。'],
   ['圧縮符号 · 複数の表', '4桁の中文電碼', '2桁ずつの数 → 音節', '00–99 → CV', '方式ごとに表が異なる。CVは子音と母音を表す。'],
   ['文密 1916 · G0 / Y0', '4桁の中文電碼', '二つの異なる音節表', '報 → 1032 → fa | zi', 'G0のみの例。Y0は別の表なので、相互に代用できない。']],
  'process': '用紙から意味へ：実際の例',
  'process_note': 'ロザモンド、上海 → 東京、1915年7月7日。英語の置換暗号の例であり、文密のG0ではない。',
  'scan': '1 · 史料', 'scan_note': 'JACAR所蔵の日本側写し：B03050087700、画像50。クリックで拡大。',
  'steps': ['2 · 文字群を書き起こす', '3 · 置換表を適用', '4 · 単語に区切って訳す'],
  'translation': '「どうか慈悲を。」', 'uncertain': 'この例でも解決しない点',
  'uncertain_note': '公表テキストでは「Lovesick」の後に未読部分が残る。他の箇所が読めても、この不確かさは消せない。',
  'read': '本文と限界を確認する',
 },
 'zh-hans': {
  'timeline': '1915—1917年：通信时间线',
  'timeline_note': '选取的时间节点，间距不代表时长。史料日期与作者身份的推定须加以区分。',
  'kinds': ['电报', '历史背景', '尚未破译'],
  'events': [
   'Rosamonde文章所列二月最早的一封电报。将通信归于孙中山与宋庆龄，依据的是史料互证，而非电报单上的实名。',
   '孙中山与宋庆龄在东京结婚。', '云南起兵反对袁世凯的帝制计划。',
   '孙中山回到上海；宋庆龄于1916年5月19日前来会合。', '袁世凯去世。',
   '赵伸的通信：致南方军务院的文密（G0）及云南渠道（Y0）。',
   '孙中山 ↔ 戴季陶：另一种密码，尚未破译。'],
  'compare': '同为拉丁字母，密码系统却不同',
  'compare_note': '公开中文电码是一种编码步骤，本身并非秘密。1916年的文密采用两张特定的表，将数字转换为音节。',
  'rows': [
   ['Rosamonde · 1915–1916', '英文', '字母互易替换', 'you ↔ hea', '一个字母替换另一个字母；同一张表既用于加密，也用于解密。'],
   ['中文电码', '汉字', '公开的四位数字码表', '文 → 2429', '码表是公开的，单凭这一步无法隐藏内容。'],
   ['压缩电码 · 多张码表', '四位中文电码', '两组两位数字 → 音节', '00–99 → CV', '不同系统使用不同码表。CV表示辅音加元音。'],
   ['文密 1916 · G0 / Y0', '四位中文电码', '两张不同的音节表', '報 → 1032 → fa | zi', '仅为G0示例。Y0使用另一张表，不能互换。']],
  'process': '从电报单到含义：一个真实例子',
  'process_note': 'Rosamonde，上海 → 东京，1915年7月7日。这里使用英文替换密码，而非文密的G0表。',
  'scan': '1 · 原始史料', 'scan_note': 'JACAR所藏日方抄件：B03050087700，图像50。点击放大。',
  'steps': ['2 · 转录字母组', '3 · 应用替换表', '4 · 划分单词并翻译'],
  'translation': '“请怜悯我。”', 'uncertain': '本例并未解决的问题',
  'uncertain_note': '已发表文本在“Lovesick”之后仍保留未读部分。其他段落能够读通，并不意味着可以抹去这里的不确定性。',
  'read': '核对原文及其局限',
 },
 'zh-hant': {
  'timeline': '1915—1917年：通信時間線',
  'timeline_note': '選取的時間節點，間距不代表時長。史料日期與作者身分的推定須加以區分。',
  'kinds': ['電報', '歷史背景', '尚未破譯'],
  'events': [
   'Rosamonde文章所列二月最早的一封電報。將通信歸於孫中山與宋慶齡，依據的是史料互證，而非電報單上的實名。',
   '孫中山與宋慶齡在東京結婚。', '雲南起兵反對袁世凱的帝制計畫。',
   '孫中山回到上海；宋慶齡於1916年5月19日前來會合。', '袁世凱去世。',
   '趙伸的通信：致南方軍務院的文密（G0）及雲南渠道（Y0）。',
   '孫中山 ↔ 戴季陶：另一種密碼，尚未破譯。'],
  'compare': '同為拉丁字母，密碼系統卻不同',
  'compare_note': '公開中文電碼是一種編碼步驟，本身並非秘密。1916年的文密採用兩張特定的表，將數字轉換為音節。',
  'rows': [
   ['Rosamonde · 1915–1916', '英文', '字母互易替換', 'you ↔ hea', '一個字母替換另一個字母；同一張表既用於加密，也用於解密。'],
   ['中文電碼', '漢字', '公開的四位數字碼表', '文 → 2429', '碼表是公開的，單憑這一步無法隱藏內容。'],
   ['壓縮電碼 · 多張碼表', '四位中文電碼', '兩組兩位數字 → 音節', '00–99 → CV', '不同系統使用不同碼表。CV表示子音加母音。'],
   ['文密 1916 · G0 / Y0', '四位中文電碼', '兩張不同的音節表', '報 → 1032 → fa | zi', '僅為G0示例。Y0使用另一張表，不能互換。']],
  'process': '從電報單到含義：一個真實例子',
  'process_note': 'Rosamonde，上海 → 東京，1915年7月7日。這裡使用英文替換密碼，而非文密的G0表。',
  'scan': '1 · 原始史料', 'scan_note': 'JACAR所藏日方抄件：B03050087700，圖像50。點擊放大。',
  'steps': ['2 · 轉錄字母組', '3 · 應用替換表', '4 · 劃分單詞並翻譯'],
  'translation': '「請憐憫我。」', 'uncertain': '本例並未解決的問題',
  'uncertain_note': '已發表文本在「Lovesick」之後仍保留未讀部分。其他段落能夠讀通，並不意味著可以抹去這裡的不確定性。',
  'read': '核對原文及其局限',
 },
}


def timeline(lang):
    t = TEXT[lang]
    parts = [f'<section class="reading-visual" id="reperes-1915-1917" aria-labelledby="reperes-title">',
             f'<h2 id="reperes-title">{escape(t["timeline"])}</h2>',
             f'<p class="visual-caption">{escape(t["timeline_note"])}</p>',
             '<ol class="reading-timeline">']
    for (date, label, link, kind), description in zip(EVENTS, t['events']):
        parts.append(f'<li><time datetime="{date}">{label}</time><div>'
                     f'<span class="evidence-label">{escape(t["kinds"][kind])}</span>'
                     f'<a href="{link}">{escape(description)}</a></div></li>')
    parts.append('</ol></section>\n')
    return '\n'.join(parts)


def comparison(lang):
    t = TEXT[lang]
    links = ['rosamonde.html#systeme', 'history.html#telegraphe', 'relecture.html#principe', 'method.html#g0']
    parts = [f'<section class="reading-visual" id="comparer-les-chiffres" aria-labelledby="compare-title">',
             f'<h2 id="compare-title">{escape(t["compare"])}</h2>',
             f'<p>{escape(t["compare_note"])}</p><ol class="cipher-comparison">']
    for row, link in zip(t['rows'], links):
        title, before, action, example, note = map(escape, row)
        parts.append(f'<li><h3><a href="{link}">{title}</a></h3>'
                     f'<div class="cipher-route"><span>{before}</span><span aria-hidden="true">→</span><span>{action}</span></div>'
                     f'<p class="cipher-example"><code>{example}</code></p><p class="visual-caption">{note}</p></li>')
    parts.append('</ol></section>\n')
    return '\n'.join(parts)


def process(lang):
    t = TEXT[lang]
    scan = '../assets/img/rosamonde/B03050087700-p50-1915-07-07.jpg'
    steps = [WORD, ' '.join(WORD) + '\n↕\n' + ' '.join(DECODED), 'be merciful']
    parts = [f'<section class="reading-visual" id="du-scan-au-texte" aria-labelledby="process-title">',
             f'<h3 id="process-title">{escape(t["process"])}</h3><p>{escape(t["process_note"])}</p>',
             '<ol class="evidence-path">', f'<li><h4>{escape(t["scan"])}</h4>',
             f'<a href="{scan}"><img src="{scan}" width="1400" height="964" alt="{escape(t["scan_note"])}" loading="lazy" decoding="async"></a>',
             f'<p class="visual-caption">{escape(t["scan_note"])}</p></li>']
    for i, (label, value) in enumerate(zip(t['steps'], steps)):
        parts.append(f'<li><h4>{escape(label)}</h4><pre class="evidence-word"><code>{escape(value)}</code></pre>'
                     + (f'<p>{escape(t["translation"])}</p>' if i == 2 else '') + '</li>')
    parts.append(f'</ol><aside class="note"><strong>{escape(t["uncertain"])}</strong>'
                 f'<p>{escape(t["uncertain_note"])}</p><a href="rosamonde.html#1915">{escape(t["read"])}</a></aside></section>\n')
    return '\n'.join(parts)


def add_editorial_visuals(body, lang, page):
    if page == 'index':
        body = body.replace('<section class="cards">', timeline(lang) + '<section class="cards">', 1)
        covers = {
            'rosamonde.html': ('rosamonde/illustrations/rosamonde-correspondence.webp', 1600, 900),
            'history.html': ('map-1916.png', 1600, 952),
            'method.html': ('illustrations/a-telegraph-office.webp', 1600, 900),
        }
        for href, (asset, width, height) in covers.items():
            marker = f'<a class="card" href="{href}">'
            body = body.replace(marker, marker + f'<img class="article-cover" src="../assets/img/{asset}" '
                                f'width="{width}" height="{height}" alt="" loading="lazy" decoding="async">', 1)
    elif page == 'method':
        body = body.replace('<h2 id="tldr">', comparison(lang) + '<h2 id="tldr">', 1)
        body = re.sub(r'(<h2 id="transcription">.*?</h2>)',
                      lambda m: m[0] + '\n' + process(lang), body, count=1)
    return body
