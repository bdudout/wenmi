"""Editorial evocations for Rosamonde; never replace genuine archive scans."""
import html
import json
from pathlib import Path
import re
from rosamonde_cipher_diagram import TEXT as DIAGRAM_TEXT

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/img/rosamonde/illustrations'
SLUGS = ['rosamonde-correspondence', 'rosamonde-chiffre-maison-bund', 'rosamonde-traversee',
         'rosamonde-yung-maison-automobile']
TEXT = {
    'fr': ('Évocation générée par IA, non documentaire ; personnages non portraiturés.', [
        'Tokyo–Shanghai, 1915 : la distance et la correspondance secrète.',
        'Chiffrer à la maison : évocation de la consigne du télégramme du 11 mars 1915.',
        'Traverser la mer entre la Chine et le Japon, 1915–1916. Navire et port imaginés, non identifiés.',
        'Yung, la maison et l’automobile : évocation symbolique du télégramme du 25 février 1915. L’identité de Yung, les biens évoqués et leur interprétation comme dot ne sont pas établis.']),
    'en': ('AI-generated evocation, not documentary evidence; figures are not portraits.', [
        'Tokyo–Shanghai, 1915: distance and secret correspondence.',
        'Enciphering at home: evoking the instruction in the telegram of 11 March 1915.',
        'Crossing the sea between China and Japan, 1915–1916. The ship and port are imagined, not identified.',
        'Yung, the house and the automobile: a symbolic evocation of the telegram of 25 February 1915. Yung’s identity, the property mentioned and its interpretation as a dowry are not established.']),
    'ja': ('AI生成のイメージ画。史料ではなく、人物の肖像でもない。', [
        '1915年、東京と上海。距離を隔てた秘密の通信。',
        '自宅で暗号文を書く。1915年3月11日の電報の指示を想起させる場面。',
        '1915〜1916年、中国と日本を結ぶ船旅。船と港は架空であり、特定のものではない。',
        'Yung、家、自動車。1915年2月25日の電報を象徴的に描いた場面。Yungの身元、家と車の特定、持参金という解釈はいずれも確定していない。']),
    'zh-hans': ('AI生成的意境插画，并非史料，画中人物并非肖像。', [
        '1915年，东京与上海：相隔两地的秘密通信。',
        '在家加密：根据1915年3月11日电报中的嘱咐创作的场景。',
        '1915—1916年，中国与日本之间的海上旅程。船只与港口均为想象，并非特定实物。',
        'Yung、房屋与汽车：根据1915年2月25日电报创作的象征性场景。Yung的身份、房屋与汽车的具体所指，以及将其解释为嫁妆的说法均未确定。']),
    'zh-hant': ('AI生成的意境插畫，並非史料，畫中人物並非肖像。', [
        '1915年，東京與上海：相隔兩地的秘密通信。',
        '在家加密：根據1915年3月11日電報中的囑咐創作的場景。',
        '1915—1916年，中國與日本之間的海上旅程。船隻與港口均為想像，並非特定實物。',
        'Yung、房屋與汽車：根據1915年2月25日電報創作的象徵性場景。Yung的身分、房屋與汽車的具體所指，以及將其解釋為嫁妝的說法均未確定。']),
}


def figure(lang, index):
    slug = SLUGS[index]
    meta = json.loads((ASSETS / 'manifest.json').read_text())[slug]
    note, captions = TEXT[lang]
    caption = html.escape(captions[index])
    return (f'<figure id="{slug}" class="editorial-illustration rosamonde-illustration">\n'
            f'  <img src="../assets/img/rosamonde/illustrations/{slug}.webp" '
            f'alt="{caption}" width="{meta["width"]}" height="{meta["height"]}" '
            f'loading="lazy" decoding="async">\n'
            f'  <figcaption>{caption} {html.escape(note)}</figcaption>\n</figure>\n')


def add_rosamonde_illustrations(body, lang, page):
    if page == 'index':
        # The leading feature retains its genuine JACAR scan and exact caption.
        marker = '</section>'
        offset = body.index(marker) + len(marker)
        body = body[:offset] + '\n' + figure(lang, 0) + body[offset:]
    elif page == 'rosamonde':
        body = body.replace('<nav class="toc"', figure(lang, 0) + '<nav class="toc"', 1)
        body = re.sub(r'(<h2 id="systeme">.*?</h2>)',
                      lambda m: m[0] + '\n' + figure(lang, 1), body, count=1)
        body = re.sub(r'(<h2 id="1916">.*?</h2>)',
                      lambda m: m[0] + '\n' + figure(lang, 2), body, count=1)
        caption = html.escape(DIAGRAM_TEXT[lang][0] + ' — ' + DIAGRAM_TEXT[lang][3])
        diagram = (f'<figure id="chiffrement-illustre" class="editorial-illustration rosamonde-diagram">'
                   f'<a href="../assets/img/rosamonde/illustrations/rosamonde-chiffrement-{lang}.svg">'
                   f'<img src="../assets/img/rosamonde/illustrations/rosamonde-chiffrement-{lang}.svg" '
                   f'width="900" height="1160" alt="{caption}" loading="lazy" decoding="async">'
                   f'</a><figcaption>{caption}</figcaption></figure>\n')
        body = body.replace('<h2 id="1915">', diagram + '<h2 id="1915">', 1)
        # Keep the actual telegram table intact; place the symbolic vignette after it.
        start = body.index('<h2 id="1915">')
        marker = '</table></div>'
        offset = body.index(marker, start) + len(marker)
        body = body[:offset] + '\n' + figure(lang, 3) + body[offset:]
    return body
