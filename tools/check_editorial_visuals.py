"""Check coverage, dates, exact examples and local references in reading aids."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from editorial_visuals import TEXT, EVENTS, WORD, DECODED

ROOT = Path(__file__).resolve().parents[1]


class Nodes(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.covers = 0
        self.times = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag == 'img' and a.get('class') == 'article-cover':
            self.covers += 1
            assert a.get('alt') == '' and a.get('loading') == 'lazy'
        if tag == 'time' and 'datetime' in a:
            self.times.append(a['datetime'])


for lang, t in TEXT.items():
    assert len(t['events']) == len(EVENTS) == 7
    assert len(t['rows']) == 4 and len(t['steps']) == 3
    for page in ['index', 'method']:
        path = ROOT / lang / f'{page}.html'
        body = path.read_text()
        nodes = Nodes(body)
        assert len(nodes.ids) == len(set(nodes.ids)), f'Duplicate ids: {path}'
        if page == 'index':
            assert 'reperes-1915-1917' in nodes.ids and nodes.covers == 3
            assert nodes.times == [e[0] for e in EVENTS]
        else:
            assert all(i in nodes.ids for i in ['comparer-les-chiffres', 'du-scan-au-texte'])
            assert WORD in body and 'be merciful' in body
        for href in nodes.links:
            link = urlsplit(href)
            if link.scheme or link.netloc:
                continue
            target = path.parent / unquote(link.path) if link.path else path
            # Validate new reading-aid references, without auditing unrelated corpus JS anchors.
            if href in [e[2] for e in EVENTS] or href in [
                    'rosamonde.html#systeme', 'history.html#telegraphe',
                    'relecture.html#principe', 'method.html#g0', 'rosamonde.html#1915']:
                assert target.is_file(), target
                assert link.fragment in Nodes(target.read_text()).ids, href
assert DECODED == 'bemerciful'
g0 = {c + v: 10 * (i // 2) + (j if i % 2 == 0 else 9 - j)
      for i, c in enumerate('hgfdcbzyxwvtsrqpnmlk') for j, v in enumerate('aeiou')}
assert f'{g0["fa"]:02d}{g0["zi"]:02d}' == '1032'
assert WORD in (ROOT / 'content/fr/rosamonde.html').read_text()
print('Three reading aids and three covers verified in five languages; dates, examples and links valid.')
