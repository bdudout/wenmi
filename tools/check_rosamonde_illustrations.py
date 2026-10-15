"""Verify diagram key, image coverage and preservation of archive scans."""
import json
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
from rosamonde_cipher_diagram import KEY, TEXT, GROUPED, CIPHER

ROOT = Path(__file__).resolve().parents[1]


class Images(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.images = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs))


key_source = ROOT.parent / 'wenmi/cryptanalysis/c35/ns/key-rosamonde.json'
assert KEY == json.loads(key_source.read_text())['involution']
assert GROUPED.replace(' ', '') == CIPHER
count = 0
for lang in TEXT:
    for page, expected in [('index', 1), ('rosamonde', 5)]:
        output = ROOT / lang / f'{page}.html'
        images = Images(output.read_text()).images
        source_images = Images((ROOT / 'content' / lang / f'{page}.html').read_text()).images
        assert all(any(i['src'] == s['src'] for i in images) for s in source_images), output
        additions = [i for i in images if '/rosamonde/illustrations/' in i['src']
                     and i.get('class') != 'article-cover']
        assert len(additions) == expected, output
        for image in additions:
            path = output.parent / image['src']
            assert path.is_file() and image.get('alt'), path
            assert int(image['width']) > 0 and int(image['height']) > 0, path
            if path.suffix == '.svg':
                ET.parse(path)
            count += 1
print(f'{count} placements verified; five languages; archive images preserved; key matches research data.')
