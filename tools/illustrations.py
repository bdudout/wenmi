"""Insert generated editorial illustrations; captions remain distinct from archive evidence."""
import html
import json
from pathlib import Path
import re

SLUGS = ['a-telegraph-office', 'b-japanese-clerk', 'c-tokyo-south-china',
         'd-aircraft-negotiation', 'e-rifle-shipment', 'f-sun-yat-sen']
TEXT = {
    'fr': ('Illustration de reconstitution générée par IA.', [
        'Bureau télégraphique japonais, évocation de 1916. Les formulaires Wenmi réels portent des mots chiffrés en lettres latines (voir le scan en page d’accueil).',
        'Un employé japonais recopie un télégramme à la plume. Sur les copies réelles, les mots chiffrés sont écrits en lettres latines cursives.',
        'Tokyo et le Sud de la Chine : liaison symbolique, sans indication du tracé réel des câbles.',
        'Négociation d’avions : scène illustrative avec un biplan de conception antérieure à 1917 ; modèle acheté non identifié.',
        'Livraison de fusils Type 30 : évocation d’un quai à Moji en 1916, sans prétendre restituer une livraison documentée.',
        'Sun Yat-sen : portrait dessiné d’après sa photographie de 1911, et non une photographie de 1916.']),
    'en': ('AI-generated historical reconstruction.', [
        'A Japanese telegraph office, evoking 1916. The real Wenmi forms carry cipher words in Latin letters (see the scan on the home page).',
        'A Japanese clerk copies a telegram with a dip pen. On the real copies, the cipher words are written in cursive Latin letters.',
        'Tokyo and southern China: a symbolic connection, not the actual cable route.',
        'Aircraft negotiations: an illustrative scene with a pre-1917 biplane design; the purchased model is unknown.',
        'Type 30 rifle shipment: an imagined Moji dock in 1916, not a reconstruction of a documented delivery.',
        'Sun Yat-sen: a drawn adaptation of his 1911 photograph, not a photograph taken in 1916.']),
    'ja': ('AIによる歴史的再現イラスト。', [
        '1916年の日本の電信局を想起させる場面。実際の「文密」電報用紙には、ラテン文字の暗号語が記されている（トップページの画像を参照）。',
        'つけペンで電報を書き写す日本人職員。実際の写しでは、暗号語はラテン文字の筆記体で書かれている。',
        '東京と中国南部の象徴的な通信経路。実際の海底ケーブル経路ではない。',
        '航空機購入交渉の想像図。1917年以前の複葉機設計を示すが、購入機種は不明。',
        '三十年式歩兵銃の輸送を想起させる1916年の門司埠頭。記録された納入の再現ではない。',
        '孫文：1911年の写真に基づく肖像画。1916年に撮影された写真ではない。']),
    'zh-hans': ('AI生成的历史重构插画。', [
        '1916年日本电报局的想象场景。真实的“文密”电报单上写的是拉丁字母密语（见首页扫描件）。',
        '日本职员用蘸水笔抄写电报。真实抄件上的密语以拉丁字母草体书写。',
        '东京与中国南部的象征性联系，并非实际电缆路线。',
        '采购飞机的想象场景，图纸采用1917年以前的双翼机设计；实际采购型号不明。',
        '三十年式步枪运输：1916年门司码头的想象场景，并非某次有记录交货的还原。',
        '孙中山：根据1911年照片绘制的肖像，并非1916年拍摄的照片。']),
    'zh-hant': ('AI生成的歷史重構插畫。', [
        '1916年日本電報局的想像場景。真實的「文密」電報單上寫的是拉丁字母密語（見首頁掃描件）。',
        '日本職員用蘸水筆抄寫電報。真實抄件上的密語以拉丁字母草體書寫。',
        '東京與中國南部的象徵性聯繫，並非實際電纜路線。',
        '採購飛機的想像場景，圖紙採用1917年以前的雙翼機設計；實際採購型號不明。',
        '三十年式步槍運輸：1916年門司碼頭的想像場景，並非某次有記錄交貨的還原。',
        '孫中山：根據1911年照片繪製的肖像，並非1916年拍攝的照片。']),
}


def figure(lang, index, banner=False):
    note, captions = TEXT[lang]
    slug = SLUGS[index]
    caption = html.escape(captions[index])
    loading = 'fetchpriority="high"' if banner else 'loading="lazy"'
    css = 'illustration-banner' if banner else 'editorial-illustration'
    manifest = json.loads((Path(__file__).resolve().parents[1] /
                           'assets/img/illustrations/manifest.json').read_text())
    dimensions = manifest[slug]
    return (f'<figure class="{css}">\n'
            f'  <img src="../assets/img/illustrations/{slug}.webp" alt="{caption}" '
            f'width="{dimensions["width"]}" height="{dimensions["height"]}" '
            f'{loading} decoding="async">\n'
            f'  <figcaption>{caption} {html.escape(note)}</figcaption>\n</figure>\n')


def add_illustrations(body, lang, page):
    # Accueil : le scan JACAR reste la seule image d'ouverture (document réel). Carte C et portrait F non utilisés :
    # la carte documentée (map-1916.png) et la photographie de 1911 de Sun Yat-sen sont déjà dans l'article.
    if page == 'method':
        body = body.replace('<h2 id="tldr">', figure(lang, 0) + '<h2 id="tldr">', 1)
    elif page == 'history':
        for anchor, index in [('telegraphe', 1)]:
            body = re.sub(r'(<h2 id="' + anchor + r'">.*?</h2>)',
                          lambda m: m[0] + figure(lang, index), body, count=1)
        # Stable insertion within the shared seven-message section in all five languages.
        start = body.index('<h2 id="messages">')
        end = body.index('<h2 id="yunnan">', start)
        section = body[start:end]
        headings = list(re.finditer(r'<h3>.*?</h3>', section))
        for position, index in [(1, 3), (0, 4)]:
            offset = headings[position].end()
            section = section[:offset] + figure(lang, index) + section[offset:]
        body = body[:start] + section + body[end:]
    return body
