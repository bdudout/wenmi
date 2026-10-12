#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fiches des télégrammes à condensateur de 1916 : page JACAR recadrée (vignette + grande image) et mini-carte du trajet.
Mêmes traitements que make_fiches.py (scans d'archives à 300 dpi, carte dessinée par code sur fond Natural Earth, sans IA) ;
la carte descend jusqu'à Manille et le trajet est tracé en ocre (condensateurs), pour ne pas le confondre avec les canaux du Wenmi.
Usage : python3 tools/make_fiches_c1916.py <dossier d'enquête wenmi> <ne_110m_land.geojson> [scans|maps|all]
Sorties : assets/img/fiches/scan-c<image>.webp, scan-c<image>-full.webp, map-<id>.png ; et scan-0509 / scan-0511 (juin 1917)"""
import glob, json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_fiches as MF   # lit sys.argv[1] (dossier wenmi) et sys.argv[2] (fond de carte)
import make_media as M

WENMI, LAND, OUT = MF.WENMI, MF.LAND, MF.OUT
PDF = {'B03050088300': (os.path.join(WENMI, 'sources', 'c32', 'B03050088300.pdf'), 440),   # page du PDF = image − 440
       'B03050089100': (os.path.join(WENMI, 'sources', 'c14', 'B03050089100.pdf'), 59),    # page du PDF = image − 59
       'B03050090200': (os.path.join(WENMI, 'sources', 'B03050090200_0503-0513.pdf'), 502)}  # juin 1917 (non déchiffrés)
M.CITIES.update({'manila': ('Manila', '馬尼拉', 120.98, 14.60, (14, -6)), 'qingdao': ('Qingdao', '青島', 120.38, 36.07, (14, -6))})
CITY = {'Tokyo': 'tokyo', 'Shanghai': 'shanghai', 'Manila': 'manila', 'Qingdao': 'qingdao'}


def corpus():
    s = open(os.path.join(M.SITE, 'assets', 'js', 'corpus-c1916.js'), encoding='utf-8').read()
    a = s.index('window.WENMI_C1916 = ') + len('window.WENMI_C1916 = '); b = s.index(';\nwindow.WENMI_C1916_I18N')
    return json.loads(s[a:b])['messages']


def render(record, frame):
    pdf, off = PDF[record]; p = int(frame) - off
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['pdftoppm', '-r', '300', '-f', str(p), '-l', str(p), '-png', pdf, os.path.join(t, 'p')], check=True)
        return Image.open(glob.glob(os.path.join(t, 'p-*.png'))[0]).rotate(90, expand=True).convert('L')


def form_crop(im):
    """Comme make_fiches.form_crop, mais sur ces bobines le bandeau « REEL » commence plus loin (≈ 88 % de la largeur)."""
    W, H = im.size; x1 = int(W * 0.875)
    a = np.asarray(im.crop((0, 0, x1, H))) < 150
    cols = np.where(a.sum(axis=0) > H * 0.01)[0]; rows = np.where(a.sum(axis=1) > x1 * 0.01)[0]
    box = (max(0, cols.min() - 20), max(0, rows.min() - 20), min(x1, cols.max() + 20), min(H, rows.max() + 20))
    c = im.crop(box); d = (np.asarray(c) < 100).mean(axis=0)
    while c.width > 100 and d[c.width - 1] > 0.5: c = c.crop((0, 0, c.width - 1, c.height))   # bord noir du microfilm
    return c


def scans(msgs):
    done = set()
    for m in msgs + [{'record': 'B03050090200', 'fiche': {'img': n, 'n': n}} for n in ('0509', '0511')]:   # + juin 1917
        img = m['fiche']['img']
        if img in done: continue
        done.add(img)
        c = ImageOps.autocontrast(form_crop(render(m['record'], m['fiche']['n'])), cutoff=1)
        if (np.asarray(c) < 200).mean() > 0.12: c = c.filter(ImageFilter.MedianFilter(3))   # trame grisée des formulaires de réception
        full = c.copy(); full.thumbnail((1400, 2400)); fp = os.path.join(OUT, f'scan-{img}-full.webp'); full.save(fp, quality=60)
        if os.path.getsize(fp) > 450 * 1024: full.save(fp, quality=40)   # fond tramé : poids raisonnable, écriture lisible
        th = c.copy(); th.thumbnail((520, 820)); th.save(os.path.join(OUT, f'scan-{img}.webp'), quality=70)
        print('scan', img, c.size, os.path.getsize(os.path.join(OUT, f'scan-{img}-full.webp')) // 1024, 'Ko')


def stops_of(route):
    a, b = route.split(' → ')
    return [CITY[a.split(' ')[0]], CITY[b.split(' ')[0]]]


def mini_map(m, all_routes):
    lat0 = M.LAT0; M.LAT0 = 12.0          # jusqu'à Manille (14,6° N)
    try:
        W = 560; s = 2; im = M.base_map(LAND, W, s); W2, H2 = im.size; dr = ImageDraw.Draw(im)
        for o, d in sorted(all_routes):    # tous les trajets des condensateurs, en clair
            M.draw_arc(dr, M.route_points(o, d, W2, H2), (214, 206, 190), 2 * s, arrow=False)
        stops = stops_of(m['route'])
        for o, d in zip(stops, stops[1:]):
            M.draw_arc(dr, M.route_points(o, d, W2, H2), M.GOLD, 5 * s)
        for k in set(stops):
            x, y = M.city_xy(k, W2, H2); r = 7 * s; dr.ellipse([x - r, y - r, x + r, y + r], fill=M.INK)
            name, cjk = M.CITIES[k][:2]
            dx = {'tokyo': -120, 'qingdao': -128, 'manila': 20, 'shanghai': -138}.get(k, 14) * s; dy = {'tokyo': 14, 'manila': -66, 'shanghai': 12}.get(k, -30) * s
            dr.text((x + dx, y + dy), name, font=M.F('serif', 26 * s), fill=M.INK)
            dr.text((x + dx, y + dy + 28 * s), cjk, font=M.F('cjk', 26 * s), fill=M.MUTED)
        im = im.resize((W, im.height // s), Image.LANCZOS); im.save(os.path.join(OUT, f"map-{m['id']}.png"), optimize=True)
    finally:
        M.LAT0 = lat0


if __name__ == '__main__':
    what = sys.argv[3] if len(sys.argv) > 3 else 'all'
    msgs = corpus()
    if what in ('scans', 'all'): scans(msgs)
    if what in ('maps', 'all'):
        routes = {tuple(sorted(stops_of(m['route']))) for m in msgs}
        for m in msgs: mini_map(m, routes)
        print('cartes', len(msgs))
