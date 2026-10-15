#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fiches des télégrammes de 1915 (corpus-t1915.js) : page JACAR recadrée (vignette + grande image), mêmes traitements que
make_fiches_c1916.py, et mini-carte du trajet (même dessin ; New York, hors cadre, est placé au bord est comme Honolulu).
Usage : python3 tools/make_fiches_t1915.py <dossier d'enquête wenmi> <ne_110m_land.geojson>
Sorties : assets/img/fiches/scan-t<image>.webp, scan-n<image>-full.webp"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_fiches_c1916 as FC
import make_media as M

WENMI, OUT = FC.WENMI, FC.OUT
for rec, off in {'B03050087600': 162, 'B03050087700': 220}.items():   # page du PDF = image − décalage
    FC.PDF[rec] = (os.path.join(WENMI, 'sources', 'c35', 'jacar', rec + '.pdf'), off)


def corpus():
    s = open(os.path.join(M.SITE, 'assets', 'js', 'corpus-t1915.js'), encoding='utf-8').read()
    a = s.index('window.WENMI_T1915 = ') + len('window.WENMI_T1915 = '); b = s.index(';\nwindow.WENMI_T1915_I18N')
    return json.loads(s[a:b])['messages']


M.CITIES['newyork'] = ('New York', '紐約', 144.2, 27.0, (14, -6))      # hors cadre : bord est, direction d'arrivée
CITY = {'Tokyo': 'tokyo', 'Shanghai': 'shanghai', 'Manila': 'manila', 'New York': 'newyork'}


def stops_of(route):
    a, b = route.split(' → ')
    return [next(v for k, v in CITY.items() if k in a), next(v for k, v in CITY.items() if k in b.split('(')[0])]


def mini_map(m, all_routes):
    lat0 = M.LAT0; M.LAT0 = 12.0
    try:
        W = 560; s = 2; im = M.base_map(FC.LAND, W, s); W2, H2 = im.size; dr = ImageDraw.Draw(im)
        for o, d in sorted(all_routes):
            M.draw_arc(dr, M.route_points(o, d, W2, H2), (214, 206, 190), 2 * s, arrow=False)
        stops = stops_of(m['route'])
        for o, d in zip(stops, stops[1:]):
            M.draw_arc(dr, M.route_points(o, d, W2, H2), M.GOLD, 5 * s)
        for k in set(stops):
            x, y = M.city_xy(k, W2, H2); r = 7 * s; dr.ellipse([x - r, y - r, x + r, y + r], fill=M.INK)
            name, cjk = M.CITIES[k][:2]
            dx = {'tokyo': -120, 'manila': 20, 'shanghai': -138, 'newyork': -170}.get(k, 14) * s
            dy = {'tokyo': 14, 'manila': -66, 'shanghai': 12, 'newyork': 14}.get(k, -30) * s
            dr.text((x + dx, y + dy), name, font=M.F('serif', 26 * s), fill=M.INK)
            dr.text((x + dx, y + dy + 28 * s), cjk, font=M.F('cjk', 26 * s), fill=M.MUTED)
        im = im.resize((W, im.height // s), Image.LANCZOS); im.save(os.path.join(OUT, f"map-{m['id']}.png"), optimize=True)
    finally:
        M.LAT0 = lat0


if __name__ == '__main__':
    msgs = corpus(); routes = {tuple(sorted(stops_of(m['route']))) for m in msgs}
    for m in msgs: mini_map(m, routes)
    print('cartes', len(msgs))
    if len(sys.argv) > 3 and sys.argv[3] == 'maps': sys.exit(0)
    done = set()
    for m in msgs:
        img = m['fiche']['img']
        if img in done: continue
        done.add(img)
        c = ImageOps.autocontrast(FC.form_crop(FC.render(m['record'], m['fiche']['n'])), cutoff=1)
        if (np.asarray(c) < 200).mean() > 0.12: c = c.filter(ImageFilter.MedianFilter(3))
        full = c.copy(); full.thumbnail((1400, 2400)); fp = os.path.join(OUT, f'scan-{img}-full.webp'); full.save(fp, quality=60)
        if os.path.getsize(fp) > 450 * 1024: full.save(fp, quality=40)
        th = c.copy(); th.thumbnail((520, 820)); th.save(os.path.join(OUT, f'scan-{img}.webp'), quality=70)
        print('scan', img, c.size, os.path.getsize(fp) // 1024, 'Ko')
