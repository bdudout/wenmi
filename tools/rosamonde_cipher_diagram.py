"""Generate exact, translatable SVG diagrams from the reciprocal Rosamonde key."""
from html import escape
from pathlib import Path

PAIRS = 'au bg cs eo fj hy ir kz lt mw nv qx'.split()
KEY = {c: pair[1 - i] for pair in PAIRS for i, c in enumerate(pair)} | {'d': 'd', 'p': 'p'}
EXAMPLE = 'love you love you'
PLAIN = EXAMPLE.replace(' ', '')
CIPHER = ''.join(KEY[c] for c in PLAIN)
GROUPED = ' '.join(CIPHER[i:i+10] for i in range(0, len(CIPHER), 10))
TEXT = {
    'fr': ['Le chiffre de Rosamonde', 'Une substitution réciproque · 1915–1916', '1 · Un message en anglais',
           'Exemple pédagogique inventé, non extrait d’un télégramme.', '2 · Remplacer chaque lettre par sa partenaire',
           'd et p restent inchangés', '3 · Supprimer les espaces, puis grouper par dix',
           'Espaces d’origine supprimés', 'Groupes transmis (dernier groupe incomplet ici)',
           '4 · La même table permet de lire le message', 'Chaque paire fonctionne dans les deux sens.'],
    'en': ['The Rosamonde cipher', 'A reciprocal substitution · 1915–1916', '1 · A message in English',
           'Invented teaching example, not a quotation from a telegram.', '2 · Replace each letter with its partner',
           'd and p remain unchanged', '3 · Remove spaces, then group by ten',
           'Original spaces removed', 'Transmitted groups (last group incomplete here)',
           '4 · The same table reads the message', 'Every pair works in both directions.'],
    'ja': ['ロザモンドの暗号', '相互置換暗号 · 1915–1916', '1 · 英語のメッセージ',
           '説明用の例文。実際の電報からの引用ではない。', '2 · 各文字を対の文字に置き換える',
           'd と p は変わらない', '3 · 空白を除き、10文字ずつに区切る',
           '元の空白を除く', '送信する文字群（この例の末尾は10文字未満）',
           '4 · 同じ表で元の文に戻せる', '文字の対は双方向に対応する。'],
    'zh-hans': ['Rosamonde 的密码', '互易字母替换 · 1915—1916', '1 · 英文消息',
                '为讲解而编写的例句，并非电报原文。', '2 · 将每个字母换成配对字母',
                'd 和 p 保持不变', '3 · 去除空格，再按十个字母分组',
                '去除原有空格', '发送的字母组（本例最后一组不足十个字母）',
                '4 · 使用同一张表还原原文', '每一对字母均可双向替换。'],
    'zh-hant': ['Rosamonde 的密碼', '互易字母替換 · 1915—1916', '1 · 英文訊息',
                '為講解而編寫的例句，並非電報原文。', '2 · 將每個字母換成配對字母',
                'd 和 p 保持不變', '3 · 去除空格，再按十個字母分組',
                '去除原有空格', '發送的字母組（本例最後一組不足十個字母）',
                '4 · 使用同一張表還原原文', '每一對字母均可雙向替換。'],
}


def render(lang):
    t = TEXT[lang]
    pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="1160" viewBox="0 0 900 1160" role="img" aria-labelledby="title desc" xml:lang="{lang}">',
              f'<title id="title">{escape(t[0])}</title><desc id="desc">{escape(t[1])}; you ↔ hea; love ↔ teno.</desc>',
              '<rect width="900" height="1160" rx="16" fill="#f7f3ea"/>',
              '<style>text{font-family:Georgia,"Noto Serif CJK SC",serif;fill:#28251f}.small{font-size:22px;fill:#605b50}.mono{font-family:monospace;letter-spacing:2px}.heading{font-size:28px;fill:#8c3d2c}</style>']
    def text(x, y, value, css='', size=30):
        pieces.append(f'<text x="{x}" y="{y}" class="{css}" font-size="{size}">{escape(value)}</text>')
    text(42, 64, t[0], size=40)
    text(42, 104, t[1], 'small')
    for y, h in [(140, 150), (310, 310), (640, 250), (910, 205)]:
        pieces.append(f'<rect x="24" y="{y}" width="852" height="{h}" rx="10" fill="#efe8d9" stroke="#d5c8b3"/>')
    text(44, 181, t[2], 'heading')
    text(44, 234, EXAMPLE, 'mono', 38)
    text(44, 270, t[3], 'small')
    text(44, 351, t[4], 'heading')
    text(44, 408, 'y  o  u       l  o  v  e', 'mono', 34)
    text(44, 449, '↕  ↕  ↕       ↕  ↕  ↕  ↕', 'mono', 34)
    text(44, 492, 'h  e  a       t  e  n  o', 'mono', 34)
    text(44, 548, 'a↔u  b↔g  c↔s  e↔o  f↔j  h↔y', 'mono', 25)
    text(44, 584, 'i↔r  k↔z  l↔t  m↔w  n↔v  q↔x', 'mono', 25)
    text(600, 607, t[5], 'small')
    text(44, 681, t[6], 'heading')
    text(44, 724, t[7], 'small')
    text(44, 772, CIPHER, 'mono', 38)
    text(44, 815, t[8], 'small')
    text(44, 863, GROUPED, 'mono', 38)
    text(44, 951, t[9], 'heading')
    text(44, 1006, f'{CIPHER}  →', 'mono', 34)
    text(44, 1053, PLAIN, 'mono', 34)
    text(44, 1091, t[10], 'small')
    pieces.append('</svg>')
    return '\n'.join(pieces) + '\n'


def build_diagrams():
    assert all(KEY[KEY[c]] == c for c in KEY)
    assert ''.join(KEY[c] for c in 'you') == 'hea'
    assert ''.join(KEY[c] for c in 'love') == 'teno'
    assert ''.join(KEY[c] for c in CIPHER) == PLAIN
    dest = Path(__file__).resolve().parents[1] / 'assets/img/rosamonde/illustrations'
    dest.mkdir(parents=True, exist_ok=True)
    for lang in TEXT:
        (dest / f'rosamonde-chiffrement-{lang}.svg').write_text(render(lang))


if __name__ == '__main__':
    build_diagrams()
