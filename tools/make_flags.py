#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les drapeaux du sélecteur de langue en SVG autonomes (aucune ressource externe).
Usage : python3 tools/make_flags.py"""
import math, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img', 'flags')

def star(cx, cy, r, rot=0.0):
    """Étoile à cinq branches, pointe dirigée selon rot (radians, 0 = vers le haut)."""
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.381966
        a = rot - math.pi / 2 + k * math.pi / 5
        pts.append('%.3f,%.3f' % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return '<polygon points="%s"/>' % ' '.join(pts)

def svg(w, h, body, label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s">%s</svg>\n'
            % (w, h, w, h, label, body))

flags = {}
# France : bleu, blanc, rouge.
flags['fr'] = svg(3, 2, '<rect width="1" height="2" fill="#002654"/><rect x="1" width="1" height="2" fill="#fff"/>'
                        '<rect x="2" width="1" height="2" fill="#CE1126"/>', 'France')
# Japon : disque rouge de diamètre 3/5 de la hauteur, centré.
flags['jp'] = svg(900, 600, '<rect width="900" height="600" fill="#fff"/><circle cx="450" cy="300" r="180" fill="#BC002D"/>', 'Japan')
# Royaume-Uni (Union Jack), construction standard 60 × 30.
flags['gb'] = svg(60, 30,
    '<clipPath id="s"><path d="M0,0v30h60V0z"/></clipPath>'
    '<clipPath id="t"><path d="M30,15h30v15zv15H0zH0V0zV0h30z"/></clipPath>'
    '<g clip-path="url(#s)"><path d="M0,0v30h60V0z" fill="#012169"/>'
    '<path d="M0,0L60,30M60,0L0,30" stroke="#fff" stroke-width="6"/>'
    '<path d="M0,0L60,30M60,0L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4"/>'
    '<path d="M30,0v30M0,15h60" stroke="#fff" stroke-width="10"/>'
    '<path d="M30,0v30M0,15h60" stroke="#C8102E" stroke-width="6"/></g>', 'United Kingdom')
# Chine : grille 30 × 20 ; grande étoile (5,5) r=3 ; petites étoiles r=1 orientées vers la grande.
cn = ['<rect width="30" height="20" fill="#EE1C25"/><g fill="#FFFF00">', star(5, 5, 3)]
for (x, y) in [(10, 2), (12, 4), (12, 7), (10, 9)]:
    rot = math.atan2(5 - y, 5 - x) + math.pi / 2   # une pointe dirigée vers le centre de la grande étoile
    cn.append(star(x, y, 1, rot))
cn.append('</g>')
flags['cn'] = svg(30, 20, ''.join(cn), 'China')
# Hong Kong : fond rouge, fleur de bauhinia blanche à cinq pétales (stylisée), une étoile rouge par pétale.
petal = 'M0,0 C-2.6,-1.1 -3.3,-5.0 -0.7,-7.6 C-0.3,-5.6 2.0,-4.6 2.8,-2.9 C3.2,-1.6 1.7,-0.3 0,0 Z'
hk = ['<rect width="30" height="20" fill="#DE2910"/><g transform="translate(15,10)">']
for k in range(5):
    a = k * 72
    hk.append('<g transform="rotate(%d)"><path d="%s" fill="#fff"/>'
              '<path d="M0,0 C-0.6,-1.8 -0.5,-3.4 0.3,-4.6" fill="none" stroke="#DE2910" stroke-width="0.22"/>'
              '<g fill="#DE2910">%s</g></g>' % (a, petal, star(-0.2, -3.6, 0.6)))
hk.append('</g>')
flags['hk'] = svg(30, 20, ''.join(hk), 'Hong Kong')

for code, s in flags.items():
    open(os.path.join(OUT, code + '.svg'), 'w', encoding='utf-8').write(s)
print('drapeaux :', ', '.join(sorted(flags)))
