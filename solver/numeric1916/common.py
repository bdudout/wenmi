# -*- coding: utf-8 -*-
"""Télégrammes numériques de juin 1916 — module commun : les trois clés, le modèle de langue, les données.

Clés reconstruites en octobre 2026 (Brice Dudout, avec Claude) ; aucune n'a été retrouvée dans un livre de code historique.
Chaque fonction decode_* prend un groupe de 4 chiffres (chaîne) et rend le numéro CTC (0–9999) ou None."""
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------ 共密 (clé candidate C51)
PHI = (9, 7, 6, 1, 4, 0, 5, 2, 8, 3)                  # dizaines : chiffre lu -> chiffre normalisé
def decode_gongmi(g):
    """C' = C dont la dizaine t est remplacée par PHI[t] ; P = (9000 - C') mod 10000."""
    if not g.isdigit(): return None
    c = int(g); t = c // 10 % 10
    return (9000 - (c - 10 * t + 10 * PHI[t])) % 10000

# ------------------------------------------------------------------ 容密 (clé v2)
SIGMA = [[0, 1, 2, 3, 4, 5, 6, 7, 9, 0],               # milliers (90 tient lieu de 00)
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],               # centaines
         [0, 1, 9, 8, 2, 7, 6, 5, 4, 3],               # dizaines
         [9, 8, 0, 1, 7, 2, 3, 4, 5, 6]]               # unités
def decode_rongmi(g):
    """σ par rang, puis P = (σ(C) + 0901) mod 10000 avec retenues ordinaires."""
    if not g.isdigit(): return None
    return (sum(SIGMA[j][int(g[j])] * w for j, w in enumerate((1000, 100, 10, 1))) + 901) % 10000

# ------------------------------------------------------------------ 辰密 (clé C92)
ZERO_FREE = [n for n in range(99, 10, -1) if '0' not in str(n)]   # 99, 98, …, 91, 89, …, 11
PAGE = {c: i for i, c in enumerate(ZERO_FREE)}                    # 99 -> 00, 89 -> 09, 11 -> 80
T_CHEN = [3, 9, 8, 7, 1, 0, 2, 6, 4, 5]                           # dizaines
U_CHEN = [1, 9, 5, 4, 3, 2, 6, 7, 8, 10]                          # unités (9 vaut 10 : retenue)
def decode_chenmi(g):
    """P = 100 × page + 10 × T[dizaine] + U[unité] ; page = rang dans le décompte des nombres sans zéro."""
    if not g.isdigit() or int(g[:2]) not in PAGE: return None
    return 100 * PAGE[int(g[:2])] + 10 * T_CHEN[int(g[2])] + U_CHEN[int(g[3])]

def decode_clair(g):
    return int(g) if g.isdigit() else None

DECODERS = {'gongmi': decode_gongmi, 'rongmi': decode_rongmi, 'chenmi': decode_chenmi, 'clair': decode_clair}
PREFIX = {'gongmi': '0364 1378', 'rongmi': '1369 1378', 'chenmi': '6591 1378'}   # 共密, 容密, 辰密 en clair

# ------------------------------------------------------------------ code télégraphique et modèle de langue
LM = HERE / 'lm'
CTC = dict(l.rstrip('\n').split('\t') for l in (LM / 'code2ch.tsv').open(encoding='utf-8'))
U = np.fromfile(LM / 'uni.f32', dtype=np.float32).astype(float); U -= U.mean()
BK = np.fromfile(LM / 'bi.u32', dtype=np.uint32).astype(np.int64)
BV = np.fromfile(LM / 'bi.f32', dtype=np.float32).astype(float)
BD = float(np.fromfile(LM / 'bidef.f32', dtype=np.float32)[0])

def glyph(p):
    return '□' if p is None else CTC.get(f'{p:04d}', '□')

def score(messages_codes):
    """Score moyen par code (unigramme centré + bigramme) d'une liste de messages (listes de numéros CTC)."""
    tot = 0.0; n = 0
    for m in messages_codes:
        m = np.asarray([x for x in m if x is not None], dtype=np.int64)
        if len(m) == 0: continue
        tot += U[m].sum(); n += len(m)
        if len(m) > 1:
            k = m[:-1] * 10000 + m[1:]; i = np.searchsorted(BK, k); cap = np.minimum(i, len(BK) - 1)
            tot += np.where((i < len(BK)) & (BK[cap] == k), BV[cap], BD).sum()
    return tot / max(n, 1)

def messages(family=None):
    d = json.load(open(HERE / 'data' / 'messages.json', encoding='utf-8'))['messages']
    return {k: v for k, v in d.items() if family is None or v['family'] == family}

def ciphers(m):
    return [g['cipher'] for g in m['groups']]

def decode_message(m, family=None):
    f = DECODERS[family or m['family']]
    return [f(c) for c in ciphers(m)]
