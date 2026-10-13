#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fiches des télégrammes nouvellement déchiffrés de mai–juin 1916 (corpus-n1916.js) : page JACAR recadrée (vignette + grande
image) et mini-carte du trajet. Mêmes traitements que make_fiches_c1916.py (scans d'archives à 300 dpi, carte dessinée par code
sur fond Natural Earth, sans IA) ; n° d'image = page du PDF + décalage du dossier (n1916_streams.IMG_OFFSET).
Usage : python3 tools/make_fiches_n1916.py <dossier d'enquête wenmi> <ne_110m_land.geojson> [scans|maps|all]
Sorties : assets/img/fiches/scan-n<image>.webp, scan-n<image>-full.webp, map-<id>.png"""
import json, os, sys
import numpy as np
from PIL import ImageFilter, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_fiches_c1916 as FC   # lit sys.argv[1] (dossier wenmi) et sys.argv[2] (fond de carte) ; fournit form_crop, mini_map
import make_media as M

WENMI, OUT = FC.WENMI, FC.OUT
sys.path.insert(0, os.path.join(WENMI, 'cryptanalysis', 'site'))
from n1916_streams import IMG_OFFSET   # noqa: E402
for rec, off in IMG_OFFSET.items():
    FC.PDF[rec] = (os.path.join(WENMI, 'sources', 'site', rec + '.pdf'), off)   # page du PDF = image − décalage


def corpus():
    s = open(os.path.join(M.SITE, 'assets', 'js', 'corpus-n1916.js'), encoding='utf-8').read()
    a = s.index('window.WENMI_N1916 = ') + len('window.WENMI_N1916 = '); b = s.index(';\nwindow.WENMI_N1916_I18N')
    return json.loads(s[a:b])['messages']


def scans(msgs):
    done = set()
    for m in msgs:
        img = m['fiche']['img']
        if img in done: continue
        done.add(img)
        c = ImageOps.autocontrast(FC.form_crop(FC.render(m['record'], m['fiche']['n'])), cutoff=1)
        if (np.asarray(c) < 200).mean() > 0.12: c = c.filter(ImageFilter.MedianFilter(3))   # trame grisée des formulaires de réception
        full = c.copy(); full.thumbnail((1400, 2400)); fp = os.path.join(OUT, f'scan-{img}-full.webp'); full.save(fp, quality=60)
        if os.path.getsize(fp) > 450 * 1024: full.save(fp, quality=40)
        th = c.copy(); th.thumbnail((520, 820)); th.save(os.path.join(OUT, f'scan-{img}.webp'), quality=70)
        print('scan', img, c.size, os.path.getsize(fp) // 1024, 'Ko')


if __name__ == '__main__':
    what = sys.argv[3] if len(sys.argv) > 3 else 'all'
    msgs = corpus()
    if what in ('scans', 'all'): scans(msgs)
    if what in ('maps', 'all'):
        routes = {tuple(sorted(FC.stops_of(m['route']))) for m in msgs}
        for m in msgs: FC.mini_map(m, routes)
        print('cartes', len(msgs))
