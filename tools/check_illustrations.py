#!/usr/bin/env python3
"""Check generated image references, metadata and coverage after tools/build.py."""
import json
from html.parser import HTMLParser
from pathlib import Path

from illustrations import SLUGS, TEXT

ROOT = Path(__file__).resolve().parents[1]


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs = dict(attrs)
            if '/illustrations/' in attrs.get('src', ''):
                self.images.append(attrs)


def check():
    manifest = json.loads((ROOT / 'assets/img/illustrations/manifest.json').read_text())
    assert set(manifest) == set(SLUGS), 'Incomplete illustration manifest'
    count = 0
    for lang in TEXT:
        for page, expected in [('index', []), ('method', [0]), ('history', [1, 4, 3])]:
            path = ROOT / lang / f'{page}.html'
            parser = Images()
            parser.feed(path.read_text())
            assert [Path(img['src']).stem for img in parser.images] == [SLUGS[i] for i in expected], path
            for img in parser.images:
                slug = Path(img['src']).stem
                asset = path.parent / img['src']
                assert asset.is_file() and asset.stat().st_size == manifest[slug]['bytes'], asset
                assert img['alt'] and img['decoding'] == 'async', asset
                for dimension in ('width', 'height'):
                    assert int(img[dimension]) == manifest[slug][dimension], asset
                count += 1
    print(f'{count} image placements checked across five languages; four assets used, six in the manifest.')


if __name__ == '__main__':
    check()
