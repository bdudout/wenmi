#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble le site statique : content/<langue>/<page>.html (corps seul) + gabarit commun → <langue>/<page>.html.
Chaque fichier de contenu commence par un commentaire JSON : <!-- {"title": "...", "description": "..."} -->.
Usage : python3 tools/build.py   (depuis la racine du dépôt)"""
import json, os, re, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PAGES = ['index', 'history', 'method', 'telegrams', 'sources']
LANGS = {
    'en': dict(code='en', label='English', brand='The Wenmi code',
               nav=['Home', 'The history', 'The method', 'Telegrams', 'Sources'], theme='Toggle light/dark theme',
               footer='© 2026 Brice Dudout, with Claude (Anthropic). Text and code: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Telegram images: JACAR (Japan Center for Asian Historical Records), Diplomatic Archives of the Ministry of Foreign Affairs of Japan. Prior work: Daniel Bourdeau (CC BY 4.0). <a href="sources.html">All sources</a>.',
               langs='Language'),
    'fr': dict(code='fr', label='Français', brand='Le code Wenmi',
               nav=['Accueil', "L'histoire", 'La méthode', 'Télégrammes', 'Sources'], theme='Basculer le thème clair/sombre',
               footer='© 2026 Brice Dudout, avec Claude (Anthropic). Textes et code : <a href="https://creativecommons.org/licenses/by/4.0/deed.fr">CC BY 4.0</a>. Images des télégrammes : JACAR (Japan Center for Asian Historical Records), Archives diplomatiques du ministère des Affaires étrangères du Japon. Travaux antérieurs : Daniel Bourdeau (CC BY 4.0). <a href="sources.html">Toutes les sources</a>.',
               langs='Langue'),
    'zh-hans': dict(code='zh-Hans', label='简体中文', brand='文密电码',
               nav=['首页', '历史背景', '破译方法', '电报全文', '资料来源'], theme='切换浅色/深色',
               footer='© 2026 Brice Dudout，与 Claude（Anthropic）合作。文字与代码：<a href="https://creativecommons.org/licenses/by/4.0/deed.zh-hans">CC BY 4.0</a>。电报图像：日本亚洲历史资料中心（JACAR），日本外务省外交史料馆。前人研究：Daniel Bourdeau（CC BY 4.0）。<a href="sources.html">全部资料来源</a>。',
               langs='语言'),
    'zh-hant': dict(code='zh-Hant', label='繁體中文', brand='文密電碼',
               nav=['首頁', '歷史背景', '破譯方法', '電報全文', '資料來源'], theme='切換淺色/深色',
               footer='© 2026 Brice Dudout，與 Claude（Anthropic）合作。文字與程式碼：<a href="https://creativecommons.org/licenses/by/4.0/deed.zh-hant">CC BY 4.0</a>。電報影像：日本亞洲歷史資料中心（JACAR），日本外務省外交史料館。前人研究：Daniel Bourdeau（CC BY 4.0）。<a href="sources.html">全部資料來源</a>。',
               langs='語言'),
    'ja': dict(code='ja', label='日本語', brand='文密暗号',
               nav=['ホーム', '歴史的背景', '解読の方法', '電報一覧', '出典'], theme='ライト／ダークを切り替え',
               footer='© 2026 Brice Dudout（Claude〔Anthropic〕との共同作業）。文章とコード：<a href="https://creativecommons.org/licenses/by/4.0/deed.ja">CC BY 4.0</a>。電報画像：アジア歴史資料センター（JACAR）、外務省外交史料館。先行研究：Daniel Bourdeau（CC BY 4.0）。<a href="sources.html">出典一覧</a>。',
               langs='言語'),
}
# Drapeau (assets/img/flags/<code>.svg, généré par make_flags.py) et étiquette courte affichés dans le sélecteur.
FLAGS = {'en': ('gb', 'EN'), 'fr': ('fr', 'FR'), 'zh-hans': ('cn', '简'), 'zh-hant': ('hk', '繁'), 'ja': ('jp', '日')}
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='5' "
        "fill='%239b2c1f'/%3E%3Ctext x='16' y='23' font-size='20' text-anchor='middle' fill='%23f7f3ea' font-family='serif'%3E%E6%96%87%3C/text%3E%3C/svg%3E")

TEMPLATE = '''<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{alternates}
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="icon" href="{icon}">
</head>
<body>
<header class="site-header"><div class="inner">
  <a class="brand" href="index.html"><span class="seal" lang="zh-Hant">文密</span> {brand}</a>
  <nav class="menu">
{nav}
  </nav>
  <nav class="lang-switch" aria-label="{langs}">
{switch}
  </nav>
  <button class="theme-toggle" type="button" aria-label="{theme}">◐</button>
</div></header>

<main>
{body}
</main>

<footer class="site-footer"><div class="inner">
  {footer}
</div></footer>
{scripts}
</body>
</html>
'''

import hashlib
def bust(html):
    """Ajoute ?v=<empreinte> aux CSS/JS locaux pour que les navigateurs rechargent les fichiers modifiés."""
    def rep(m):
        path = os.path.normpath(os.path.join(ROOT, 'fr', m.group(2)))
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10] if os.path.exists(path) else None
        return m.group(1) + m.group(2) + ('?v=' + h if h else '') + m.group(3)
    return re.sub(r'((?:href|src)=")(\.\./assets/(?:css|js)/[^"?]+)(")', rep, html)

def build():
    n = 0
    for lang, L in LANGS.items():
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        for page in PAGES:
            src = os.path.join(ROOT, 'content', lang, page + '.html')
            if not os.path.exists(src):
                continue
            raw = open(src, encoding='utf-8').read()
            m = re.match(r'\s*<!--\s*(\{.*?\})\s*-->\s*', raw, re.S)
            meta = json.loads(m.group(1)) if m else {}
            body = raw[m.end():] if m else raw
            nav = '\n'.join('    <a href="%s.html"%s>%s</a>' % (p, ' aria-current="page"' if p == page else '', L['nav'][i])
                            for i, p in enumerate(PAGES))
            switch = '\n'.join('    <a href="../%s/%s.html" hreflang="%s" lang="%s" data-lang="%s" title="%s" aria-label="%s"%s>'
                                '<img class="flag" src="../assets/img/flags/%s.svg" width="20" height="15" alt=""><span class="lc">%s</span></a>'
                                % (l, page, LL['code'], LL['code'], l, LL['label'], LL['label'], ' aria-current="true"' if l == lang else '',
                                   FLAGS[l][0], FLAGS[l][1]) for l, LL in LANGS.items())
            alternates = '\n'.join('<link rel="alternate" hreflang="%s" href="../%s/%s.html">' % (LL['code'], l, page) for l, LL in LANGS.items())
            scripts = ''
            if 'id="corpus"' in body:
                scripts += '<script src="../assets/js/corpus.js"></script>\n<script src="../assets/js/translations.js"></script>\n'
            if 'decoder' in body:
                scripts += ('<script src="../assets/js/messages.js"></script>\n<script src="../assets/js/messages-y0.js"></script>\n'
                            '<script src="../assets/js/translations.js"></script>\n')
            scripts += '<script src="../assets/js/site.js"></script>'
            out = TEMPLATE.format(code=L['code'], title=html.escape(meta.get('title', L['brand'])),
                                  description=html.escape(meta.get('description', '')), alternates=alternates,
                                  icon=ICON, brand=L['brand'], nav=nav, langs=L['langs'], switch=switch,
                                  theme=L['theme'], body=body.rstrip(), footer=L['footer'], scripts=scripts)
            open(os.path.join(ROOT, lang, page + '.html'), 'w', encoding='utf-8').write(bust(out))
            n += 1
    print(n, 'pages générées')

if __name__ == '__main__':
    build()
