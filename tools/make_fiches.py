#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fiche de chaque télégramme : formulaire JACAR recadré (vignette + grande image) et mini-carte du trajet.
Aucune IA : scans d'archives (pages des PDF JACAR, 300 dpi) et carte dessinée par code (fond Natural Earth).
Usage : python3 tools/make_fiches.py <dossier d'enquête wenmi> <ne_110m_land.geojson>
Sorties : assets/img/fiches/scan-<image>.webp, scan-<image>-full.webp, map-<id>.png"""
import os, sys, glob, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_media as M

WENMI = os.path.abspath(sys.argv[1]); LAND = M.load_land(sys.argv[2])
OUT = os.path.join(M.SITE, 'assets', 'img', 'fiches'); os.makedirs(OUT, exist_ok=True)
SRC = os.path.join(WENMI, 'sources')
PDF = {'090000': os.path.join(SRC, 'B03050090000_0388-0446.pdf'), '090100': os.path.join(SRC, 'c14', 'B03050090100_0447.pdf'),
       '089900': os.path.join(SRC, 'c14', 'B03050089900.pdf')}
# image JACAR → (fichier, page du PDF) ; mêmes pages que les lots de lecture (working/blind-c31/build_lot.py)
PAGES = {'0348': ('089900', 20), '0386': ('089900', 58), '0406': ('090000', 19), '0415': ('090000', 28), '0416': ('090000', 29),
         '0455': ('090100', 9), '0462': ('090100', 16), '0413': ('090000', 26), '0449': ('090100', 3), '0467': ('090100', 21),
         '0473': ('090100', 27), '0489': ('090100', 43), '0494': ('090100', 48), '0496': ('090100', 50), '0498': ('090100', 52)}
# trajet de chaque télégramme (villes de make_media.CITIES) ; canal → couleur
ROUTES = {'0348': ['tokyo', 'zhaoqing'], '0386': ['tokyo', 'zhaoqing'], '0406': ['tokyo', 'shanghai'], '0415': ['tokyo', 'zhaoqing'],
          '0416b': ['tokyo', 'zhaoqing'], '0455b': ['tokyo', 'zhaoqing'], '0462': ['tokyo', 'zhaoqing'],
          '0413': ['tokyo', 'shanghai', 'kunming'], '0416a': ['tokyo', 'shanghai', 'kunming'], '0449': ['tokyo', 'kunming'],
          '0455a': ['tokyo', 'kunming'], '0467': ['tokyo', 'kunming'], '0473': ['tokyo', 'kunming'], '0489a': ['tokyo', 'kunming'],
          '0494a': ['tokyo', 'kunming'], '0496a': ['tokyo', 'kunming'], '0498': ['kunming', 'tokyo']}
GRID = {k: ('G0' if k in ('0348', '0386', '0406', '0415', '0416b', '0455b', '0462') else 'Y0') for k in ROUTES}

def render(img):
    doc, p = PAGES[img]
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['pdftoppm', '-r', '300', '-f', str(p), '-l', str(p), '-png', PDF[doc], os.path.join(t, 'p')], check=True)
        return Image.open(glob.glob(os.path.join(t, 'p-*.png'))[0]).rotate(90, expand=True).convert('L')

def form_crop(im):
    """Zone des formulaires : à gauche du bandeau « REEL » ; boîte de l'encre, petite marge."""
    W, H = im.size; x1 = int(W * 0.72)
    a = np.asarray(im.crop((0, 0, x1, H))) < 150
    cols = np.where(a.sum(axis=0) > H * 0.01)[0]; rows = np.where(a.sum(axis=1) > x1 * 0.01)[0]
    box = (max(0, cols.min() - 20), max(0, rows.min() - 20), min(x1, cols.max() + 20), min(H, rows.max() + 20))
    c = im.crop(box); d = (np.asarray(c) < 100).mean(axis=0)
    while c.width > 100 and d[c.width - 1] > 0.5: c = c.crop((0, 0, c.width - 1, c.height))   # bord noir du microfilm
    return c

def scans():
    for img in PAGES:
        c = ImageOps.autocontrast(form_crop(render(img)), cutoff=1)
        if img == '0498': c = c.filter(ImageFilter.MedianFilter(3))   # trame grisée du formulaire de réception
        full = c.copy(); full.thumbnail((1400, 2400)); full.save(os.path.join(OUT, f'scan-{img}-full.webp'), quality=60)
        th = c.copy(); th.thumbnail((520, 820)); th.save(os.path.join(OUT, f'scan-{img}.webp'), quality=70)
        print('scan', img, c.size, os.path.getsize(os.path.join(OUT, f'scan-{img}-full.webp')) // 1024, 'Ko')

def mini_map(tid):
    W = 560; s = 2; im = M.base_map(LAND, W, s); W2, H2 = im.size; dr = ImageDraw.Draw(im)
    for o, d, ch in {(t[1], t[2], t[3]) for t in M.TELEGRAMS}:   # tous les trajets, en clair
        M.draw_arc(dr, M.route_points(o, d, W2, H2), (214, 206, 190), 2 * s, dash=(o == 'kunming'), arrow=False)
    stops = ROUTES[tid]; col = M.CH_COLOR[GRID[tid]]
    for o, d in zip(stops, stops[1:]):
        M.draw_arc(dr, M.route_points(o, d, W2, H2), col, 5 * s, dash=(o == 'kunming'))
    for k in set(stops):
        x, y = M.city_xy(k, W2, H2); r = 7 * s; dr.ellipse([x - r, y - r, x + r, y + r], fill=M.INK)
        name, cjk, _, _, (ox, oy) = M.CITIES[k]
        dx = {'zhaoqing': -150, 'tokyo': -120}.get(k, 14) * s; dy = (14 if k in ('kunming', 'tokyo') else -30) * s
        dr.text((x + dx, y + dy), name, font=M.F('serif', 26 * s), fill=M.INK)
        dr.text((x + dx, y + dy + 28 * s), cjk, font=M.F('cjk', 26 * s), fill=M.MUTED)
    im = im.resize((W, im.height // s), Image.LANCZOS); im.save(os.path.join(OUT, f'map-{tid}.png'), optimize=True)

if __name__ == '__main__':
    what = sys.argv[3] if len(sys.argv) > 3 else 'all'
    if what in ('scans', 'all'): scans()
    if what in ('maps', 'all'):
        for t in ROUTES: mini_map(t)
        print('cartes', len(ROUTES))
