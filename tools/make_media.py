#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Images et vidéos du site, générées par code (aucune image d'IA) :
  - assets/img/map-1916.png       carte des télégrammes (fond Natural Earth 1:110m, domaine public)
  - assets/media/history.mp4      vidéo de l'article historique (carte animée, juin–novembre 1916)
  - assets/media/decoder.mp4      animation du déchiffrement (début de l'article technique)
  - assets/media/*.<langue>.vtt   sous-titres dans les 5 langues
Les visuels n'utilisent que des noms bilingues, des chiffres et du chinois d'époque : le texte explicatif est dans les
sous-titres. Usage : python3 tools/make_media.py <ne_110m_land.geojson> [map|history|decoder|all]
Polices système macOS (Songti TC, Georgia, Menlo) ; ffmpeg requis pour les vidéos."""
import json, math, os, subprocess, sys, shutil, tempfile
from PIL import Image, ImageDraw, ImageFont

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
IMG, MEDIA = os.path.join(SITE, 'assets', 'img'), os.path.join(SITE, 'assets', 'media')
os.makedirs(MEDIA, exist_ok=True)
SONGTI, GEORGIA, MENLO = '/System/Library/Fonts/Supplemental/Songti.ttc', '/System/Library/Fonts/Supplemental/Georgia.ttf', '/System/Library/Fonts/Menlo.ttc'
def F(kind, size):
    if kind == 'cjk': return ImageFont.truetype(SONGTI, size, index=7)        # Songti TC Regular
    if kind == 'cjkb': return ImageFont.truetype(SONGTI, size, index=2)       # Songti TC Bold
    if kind == 'mono': return ImageFont.truetype(MENLO, size)
    return ImageFont.truetype(GEORGIA, size)

PAPER, SEA, LAND, COAST, INK, MUTED = (247, 243, 234), (236, 238, 233), (229, 219, 196), (203, 189, 156), (31, 28, 23), (122, 114, 102)
RED, TEAL, GOLD = (155, 44, 31), (47, 93, 98), (183, 121, 31)

# ---------------------------------------------------------------- carte
LON0, LON1, LAT0, LAT1 = 96.0, 145.0, 18.0, 43.0
COSL = math.cos(math.radians(31))
def proj(lon, lat, W, H):
    x = (lon - LON0) / (LON1 - LON0) * W
    y = (LAT1 - lat) / (LAT1 - LAT0) * H
    return x, y
def map_size(W): return W, int(W * (LAT1 - LAT0) / ((LON1 - LON0) * COSL))

CITIES = {  # nom latin, nom chinois/japonais, lon, lat, décalage du libellé (dx, dy en px à 1600 de large)
    'tokyo': ('Tokyo', '東京', 139.69, 35.69, (14, -6)), 'shanghai': ('Shanghai', '上海', 121.47, 31.23, (14, -4)),
    'zhaoqing': ('Zhaoqing', '肇慶', 112.47, 23.05, (-118, 10)), 'canton': ('Canton', '廣州', 113.26, 23.13, (12, 6)),
    'kunming': ('Kunming', '雲南府', 102.71, 25.04, (-30, 16)), 'hankou': ('Hankou', '漢口', 114.30, 30.59, (12, -2)),
    'fukuoka': ('Fukuoka', '福岡', 130.40, 33.59, (-96, 6)), 'moji': ('Moji', '門司', 130.96, 33.95, (10, -48)),
    'beijing': ('Beijing', '北京', 116.40, 39.90, (12, -4)),
}

def load_land(path):
    d = json.load(open(path, encoding='utf-8')); polys = []
    for f in d['features']:
        g = f['geometry']; parts = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in parts:
            ring = poly[0]
            if max(p[0] for p in ring) < LON0 - 30 or min(p[0] for p in ring) > LON1 + 30: continue
            polys.append(ring)
    return polys

def base_map(land, W, scale=2):
    W2, H2 = map_size(W * scale)
    im = Image.new('RGB', (W2, H2), SEA); dr = ImageDraw.Draw(im)
    # graticule discrète
    for lon in range(100, 145, 5):
        x, _ = proj(lon, 0, W2, H2); dr.line([(x, 0), (x, H2)], fill=(226, 229, 222), width=scale)
    for lat in range(20, 45, 5):
        _, y = proj(0, lat, W2, H2); dr.line([(0, y), (W2, y)], fill=(226, 229, 222), width=scale)
    for ring in land:
        pts = [proj(lon, lat, W2, H2) for lon, lat in ring]
        dr.polygon(pts, fill=LAND); dr.line(pts + [pts[0]], fill=COAST, width=scale)
    return im

def city_xy(k, W2, H2): _, _, lon, lat, _ = CITIES[k]; return proj(lon, lat, W2, H2)

def bezier(p0, p1, bend=0.18, n=60):
    (x0, y0), (x1, y1) = p0, p1; mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * bend, my + dx * bend
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in (i / n for i in range(n + 1))]

def draw_arc(dr, pts, color, width, frac=1.0, dash=False, arrow=True):
    k = max(2, int(len(pts) * frac)); seg = pts[:k]
    if dash:
        for i in range(0, len(seg) - 1, 4): dr.line(seg[i:i + 3], fill=color, width=width)
    else:
        dr.line(seg, fill=color, width=width, joint='curve')
    if arrow and frac >= 1.0:
        (xa, ya), (xb, yb) = pts[-4], pts[-1]; ang = math.atan2(yb - ya, xb - xa); L = width * 4.5
        dr.polygon([(xb, yb), (xb - L * math.cos(ang - 0.4), yb - L * math.sin(ang - 0.4)), (xb - L * math.cos(ang + 0.4), yb - L * math.sin(ang + 0.4))], fill=color)

def draw_cities(dr, W2, H2, s, which=None):
    for k, (lat_name, cjk, lon, lat, (ox, oy)) in CITIES.items():
        if which and k not in which: continue
        x, y = proj(lon, lat, W2, H2); r = 5 * s
        dr.ellipse([x - r, y - r, x + r, y + r], fill=INK)
        dr.text((x + ox * s, y + oy * s), lat_name, font=F('serif', 17 * s), fill=INK)
        dr.text((x + ox * s, y + oy * s + 20 * s), cjk, font=F('cjk', 17 * s), fill=MUTED)

# itinéraires (schématiques) : (origine, destination, canal, date)
TELEGRAMS = [
    ('0348', 'tokyo', 'zhaoqing', 'G0', (6, 23), '三十式槍萬一千'), ('0386', 'tokyo', 'zhaoqing', 'G0', (6, 30), '軍器飛機'),
    ('0406', 'tokyo', 'shanghai', 'G0', (7, 12), '段無組織內閣'), ('0413', 'tokyo', 'kunming', 'Y0', (7, 17), '建設航空隊'),
    ('0415', 'tokyo', 'zhaoqing', 'G0', (7, 18), '均置滇'), ('0416b', 'tokyo', 'zhaoqing', 'G0', (7, 19), '日人態度遽變'),
    ('0416a', 'tokyo', 'kunming', 'Y0', (7, 19), '滇索槍萬枝'), ('0449', 'tokyo', 'kunming', 'Y0', (9, 8), '軍用飛機六'),
    ('0455b', 'tokyo', 'zhaoqing', 'G0', (9, 13), '代滇購'), ('0455a', 'tokyo', 'kunming', 'Y0', (9, 13), '武器及飛機事'),
    ('0462', 'tokyo', 'zhaoqing', 'G0', (9, 30), '信用未免掃地'), ('0467', 'tokyo', 'kunming', 'Y0', (10, 11), '記念章'),
    ('0473', 'tokyo', 'kunming', 'Y0', (10, 20), '借款 無擔保'), ('0489a', 'tokyo', 'kunming', 'Y0', (11, 5), '擬十號南歸'),
    ('0496a', 'tokyo', 'kunming', 'Y0', (11, 9), '蔡公病故福岡'), ('0498', 'kunming', 'tokyo', 'Y0', (11, 9), '借款事'),
    ('0494a', 'tokyo', 'kunming', 'Y0', (11, 11), '擬歸'),
]
EVENTS = [('beijing', (6, 6), '袁世凱 †'), ('zhaoqing', (7, 14), '軍務院撤銷'), ('fukuoka', (11, 8), '蔡鍔 †')]
CH_COLOR = {'G0': RED, 'Y0': TEAL}

def route_points(o, d, W2, H2):
    p0, p1 = city_xy(o, W2, H2), city_xy(d, W2, H2)
    bend = 0.16 if d != 'shanghai' else 0.22
    if o == 'kunming': bend = 0.16
    return bezier(p0, p1, bend)

def make_map(land):
    W = 1600; s = 2; im = base_map(land, W, s); W2, H2 = im.size; dr = ImageDraw.Draw(im)
    seen = set()
    for tid, o, d, ch, date, snip in TELEGRAMS:
        key = (o, d, ch)
        if key in seen: continue
        seen.add(key); draw_arc(dr, route_points(o, d, W2, H2), CH_COLOR[ch], 4 * s, dash=(o == 'kunming'))
    # consulat de Hankou (déchiffrements d'avril–mai 1916)
    hx, hy = city_xy('hankou', W2, H2); dr.ellipse([hx - 12 * s, hy - 12 * s, hx + 12 * s, hy + 12 * s], outline=GOLD, width=3 * s)
    fx, fy = city_xy('fukuoka', W2, H2); dr.text((fx - 96 * s, fy + 52 * s), '蔡鍔 † 8.XI', font=F('cjk', 16 * s), fill=INK)
    draw_cities(dr, W2, H2, s)
    # légende neutre
    lx, ly = 40 * s, H2 - 120 * s
    dr.rounded_rectangle([lx - 16 * s, ly - 16 * s, lx + 300 * s, ly + 96 * s], radius=10 * s, fill=PAPER, outline=COAST, width=s)
    dr.line([(lx, ly + 10 * s), (lx + 60 * s, ly + 10 * s)], fill=RED, width=4 * s); dr.text((lx + 72 * s, ly), 'G0  東京 → 肇慶', font=F('cjk', 18 * s), fill=INK)
    dr.line([(lx, ly + 42 * s), (lx + 60 * s, ly + 42 * s)], fill=TEAL, width=4 * s); dr.text((lx + 72 * s, ly + 32 * s), 'Y0  東京 ↔ 雲南', font=F('cjk', 18 * s), fill=INK)
    dr.ellipse([lx + 18 * s, ly + 62 * s, lx + 42 * s, ly + 86 * s], outline=GOLD, width=3 * s); dr.text((lx + 72 * s, ly + 64 * s), '漢口 1916', font=F('cjk', 18 * s), fill=INK)
    dr.text((W2 - 330 * s, H2 - 34 * s), 'Natural Earth 1:110m · 1916', font=F('serif', 14 * s), fill=MUTED)
    im = im.resize((W, im.height // s), Image.LANCZOS); im.save(os.path.join(IMG, 'map-1916.png'), optimize=True)
    print('carte', im.size, os.path.getsize(os.path.join(IMG, 'map-1916.png')) // 1024, 'Ko')

# ---------------------------------------------------------------- vidéos : utilitaires
FPS = 24
def encode(frames_dir, out, fps=FPS):
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(frames_dir, 'f%05d.png'),
           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '26', '-preset', 'slow', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-c:v', 'libvpx-vp9', '-crf', '38', '-b:v', '0', '-row-mt', '1',
                    '-deadline', 'good', '-cpu-used', '2', out[:-4] + '.webm'], check=True)
def ease(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def vtt(path, cues):
    def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return '%02d:%02d:%06.3f' % (h, m, s)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('WEBVTT\n\n')
        for a, b, text in cues: f.write('%s --> %s\n%s\n\n' % (ts(a), ts(b), text))

# ---------------------------------------------------------------- vidéo de l'histoire
import datetime
D0, D1 = datetime.date(1916, 6, 1), datetime.date(1916, 11, 20)
INTRO, SPD, OUTRO = 3.0, 0.24, 5.0                  # secondes ; secondes par jour
def t_of(m, d): return INTRO + (datetime.date(1916, m, d) - D0).days * SPD
ROMAN = {6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI'}

HISTORY_CUES = {  # (début, fin, clé) ; textes par langue ci-dessous
    'intro': (0.2, INTRO + 1.0), 'jun23': (t_of(6, 21), t_of(6, 21) + 3.6), 'jun6': (t_of(6, 5), t_of(6, 5) + 3.2),
    'jul12': (t_of(7, 11), t_of(7, 11) + 3.2), 'jul19': (t_of(7, 18) + 0.4, t_of(7, 18) + 4.4), 'jul14': (t_of(7, 13) - 0.6, t_of(7, 13) + 1.2),
    'sep': (t_of(9, 7), t_of(9, 7) + 4.0), 'sep30': (t_of(9, 29), t_of(9, 29) + 3.4), 'oct': (t_of(10, 10), t_of(10, 10) + 4.0),
    'nov5': (t_of(11, 4), t_of(11, 4) + 1.9), 'nov8': (t_of(11, 7) + 0.3, t_of(11, 7) + 3.4), 'outro': (t_of(11, 20) + 0.2, t_of(11, 20) + OUTRO),
}
HISTORY_TEXT = {
 'fr': {'intro': "1916. Depuis Tokyo, Zhao Shen télégraphie en chiffre aux insurgés du Sud de la Chine.",
        'jun6': "6 juin : mort de Yuan Shikai, l'empereur manqué.", 'jun23': "23 juin, canal G0 vers Zhaoqing : 11 000 fusils japonais arrivés à Moji.",
        'jul12': "12 juillet : message vers Shanghai, le futur « témoin » du déchiffrement.", 'jul14': "14 juillet : le Conseil des affaires militaires se dissout.",
        'jul19': "19 juillet : même message sur les deux canaux. « L'attitude des Japonais a brusquement changé. »",
        'sep': "Septembre, canal Y0 vers le Yunnan : six avions militaires, huit postes de radio.", 'sep30': "30 septembre : « sinon notre crédit serait réduit à néant ».",
        'oct': "Octobre : médailles commémoratives, emprunt à 8 % sans garantie.", 'nov5': "5 novembre : « Je rentre au sud le 10. »",
        'nov8': "8 novembre : le général Cai E meurt à Fukuoka. Zhao Shen l'annonce au Yunnan.", 'outro': "17 télégrammes de 1916 déchiffrés, sur deux canaux. Ceux de 1917 résistent encore."},
 'en': {'intro': "1916. From Tokyo, Zhao Shen telegraphs in cipher to the insurgents of southern China.",
        'jun6': "6 June: death of Yuan Shikai, the would-be emperor.", 'jun23': "23 June, G0 channel to Zhaoqing: 11,000 Japanese rifles have arrived at Moji.",
        'jul12': "12 July: a message to Shanghai, the future held-out test of the decipherment.", 'jul14': "14 July: the Military Affairs Council dissolves itself.",
        'jul19': "19 July: the same message on both channels. \"The attitude of the Japanese has suddenly changed.\"",
        'sep': "September, Y0 channel to Yunnan: six military aircraft, eight wireless sets.", 'sep30': "30 September: \"otherwise our credit would be ruined\".",
        'oct': "October: commemorative medals, a loan at 8% without guarantee.", 'nov5': "5 November: \"I return south on the 10th.\"",
        'nov8': "8 November: General Cai E dies at Fukuoka. Zhao Shen announces it to Yunnan.", 'outro': "17 telegrams of 1916 deciphered, on two channels. Those of 1917 still resist."},
 'zh-hans': {'intro': "1916年，赵伸在东京以密电与中国南方的起义者联络。",
        'jun6': "6月6日：袁世凯去世。", 'jun23': "6月23日，G0 通道发往肇庆：一万一千支日本步枪运抵门司。",
        'jul12': "7月12日：发往上海的电报——日后验证破译的“留出电报”。", 'jul14': "7月14日：军务院宣布撤销。",
        'jul19': "7月19日：同一内容经两条通道发出。“日人态度遽变。”",
        'sep': "9月，Y0 通道发往云南：军用飞机六架，无线电机八台。", 'sep30': "9月30日：“否则对滇信用未免扫地。”",
        'oct': "10月：纪念章，年息八厘、无担保的借款。", 'nov5': "11月5日：“拟十号南归。”",
        'nov8': "11月8日：蔡锷将军在福冈病逝，赵伸电告云南。", 'outro': "1916年两条通道的17封电报已被破译；1917年的电报仍未攻破。"},
 'zh-hant': {'intro': "1916年，趙伸在東京以密電與中國南方的起義者聯絡。",
        'jun6': "6月6日：袁世凱去世。", 'jun23': "6月23日，G0 通道發往肇慶：一萬一千支日本步槍運抵門司。",
        'jul12': "7月12日：發往上海的電報——日後驗證破譯的「留出電報」。", 'jul14': "7月14日：軍務院宣布撤銷。",
        'jul19': "7月19日：同一內容經兩條通道發出。「日人態度遽變。」",
        'sep': "9月，Y0 通道發往雲南：軍用飛機六架，無線電機八台。", 'sep30': "9月30日：「否則對滇信用未免掃地。」",
        'oct': "10月：紀念章，息八釐、無擔保的借款。", 'nov5': "11月5日：「擬十號南歸。」",
        'nov8': "11月8日：蔡鍔將軍在福岡病逝，趙伸電告雲南。", 'outro': "1916年兩條通道的17封電報已被破譯；1917年的電報仍未攻破。"},
 'ja': {'intro': "1916年。東京の趙伸は、中国南部の蜂起勢力と暗号電報で連絡していた。",
        'jun6': "6月6日：袁世凱死去。", 'jun23': "6月23日、G0 系統で肇慶へ：日本の小銃一万一千挺が門司に到着。",
        'jul12': "7月12日：上海宛ての電報。のちに解読を検証する「検証用電報」となる。", 'jul14': "7月14日：軍務院が撤廃を宣言。",
        'jul19': "7月19日：同じ内容を二つの系統で発信。「日本側の態度が急変した。」",
        'sep': "9月、Y0 系統で雲南へ：軍用飛行機六機、無線電信機八台。", 'sep30': "9月30日：「さもなくば信用は地に落ちる」。",
        'oct': "10月：記念章、利息8%・無担保の借款。", 'nov5': "11月5日：「十日に南へ帰る」。",
        'nov8': "11月8日：蔡鍔将軍が福岡で死去。趙伸が雲南に伝える。", 'outro': "1916年の二つの系統の電報17通を解読。1917年の電報はなお破れていない。"},
}

def make_history(land):
    W, H, s = 1280, 720, 2
    base = base_map(land, W, s)                       # carte à 2x, recadrée au format 16:9
    W2, H2 = base.size; target_h = int(W2 * H / W)
    if H2 > target_h:
        top = (H2 - target_h) // 2; base = base.crop((0, top, W2, top + target_h))
        off_y = -top
    else:
        canvas = Image.new('RGB', (W2, target_h), SEA); canvas.paste(base, (0, (target_h - H2) // 2)); off_y = (target_h - H2) // 2; base = canvas
    MW, MH = W2, H2                                    # dimensions de projection (avant recadrage)
    def P(k): x, y = city_xy(k, MW, MH); return x, y + off_y
    routes = {t[0]: [(x, y + off_y) for x, y in route_points(t[1], t[2], MW, MH)] for t in TELEGRAMS}
    total = t_of(11, 20) + OUTRO; n = int(total * FPS)
    tmp = tempfile.mkdtemp(prefix='wenmi-hist-')
    fT, fS, fC, fCb = F('serif', 30 * s), F('serif', 18 * s), F('cjk', 24 * s), F('cjkb', 64 * s)
    for i in range(n):
        t = i / FPS; im = base.copy(); dr = ImageDraw.Draw(im, 'RGBA')
        day = max(0.0, (t - INTRO) / SPD); cur = D0 + datetime.timedelta(days=min(day, (D1 - D0).days))
        for tid, o, d, ch, (mm, dd), snip in TELEGRAMS:
            t0 = t_of(mm, dd)
            if t < t0: continue
            prog = ease((t - t0) / 1.1); col = CH_COLOR[ch]
            age = t - t0 - 1.1; alpha = 255 if age < 2.5 else max(90, int(255 - (age - 2.5) * 60))
            draw_arc(dr, routes[tid], col + (alpha,), 4 * s, frac=max(prog, 0.02), dash=(o == 'kunming'), arrow=prog >= 1)
            if 0 < t - t0 < 4.2:                           # extrait du télégramme près de la destination
                a = int(255 * min(1, (t - t0) / 0.4) * min(1, (4.2 - (t - t0)) / 0.6)); x, y = P(d)
                ox = -260 * s if d == 'tokyo' else (20 * s if d != 'kunming' else -40 * s)
                oy = -70 * s if d in ('zhaoqing', 'kunming') else 40 * s
                if d == 'shanghai': ox, oy = 26 * s, 64 * s
                bx, by = x + ox, y + oy; tw = dr.textlength(snip, font=fC)
                dr.rounded_rectangle([bx - 10 * s, by - 6 * s, bx + tw + 10 * s, by + 34 * s], radius=6 * s, fill=PAPER + (int(a * 0.92),), outline=col + (a,), width=2 * s)
                dr.text((bx, by), snip, font=fC, fill=INK + (a,))
        for k, (mm, dd), label in EVENTS:
            t0 = t_of(mm, dd)
            if t < t0: continue
            x, y = P(k); age = t - t0
            if age < 2.0:
                r = (8 + 40 * age) * s; a = int(200 * (1 - age / 2.0)); dr.ellipse([x - r, y - r, x + r, y + r], outline=GOLD + (a,), width=3 * s)
            a = 255 if age < 4 else 150
            ox, oy = {'fukuoka': (-150 * s, 34 * s), 'zhaoqing': (40 * s, 30 * s)}.get(k, (16 * s, -40 * s))
            dr.text((x + ox, y + oy), label, font=fC, fill=INK + (a,))
        draw_cities(dr, base.width, base.height, s, which={'tokyo', 'shanghai', 'zhaoqing', 'kunming', 'fukuoka', 'beijing', 'moji'})
        # date et frise
        if t >= INTRO - 0.3:
            dr.rounded_rectangle([24 * s, 22 * s, 300 * s, 84 * s], radius=10 * s, fill=PAPER + (230,))
            dr.text((40 * s, 34 * s), '%d · %s · 1916' % (cur.day, ROMAN.get(cur.month, '')), font=fT, fill=INK)
            y0 = base.height - 46 * s; x0, x1 = 60 * s, base.width - 60 * s
            dr.line([(x0, y0), (x1, y0)], fill=INK + (120,), width=2 * s)
            span = (D1 - D0).days
            for mth in range(6, 12):
                xm = x0 + (datetime.date(1916, mth, 1) - D0).days / span * (x1 - x0)
                dr.line([(xm, y0 - 8 * s), (xm, y0 + 8 * s)], fill=INK + (150,), width=2 * s); dr.text((xm + 6 * s, y0 + 6 * s), ROMAN[mth], font=fS, fill=MUTED)
            for tid, o, d, ch, (mm, dd), snip in TELEGRAMS:
                xt = x0 + (datetime.date(1916, mm, dd) - D0).days / span * (x1 - x0); dr.ellipse([xt - 4 * s, y0 - 4 * s, xt + 4 * s, y0 + 4 * s], fill=CH_COLOR[ch] + (220,))
            xc = x0 + min(day, span) / span * (x1 - x0); dr.polygon([(xc, y0 - 12 * s), (xc - 8 * s, y0 - 26 * s), (xc + 8 * s, y0 - 26 * s)], fill=INK)
        # titre (intro) et fin
        if t < INTRO + 0.8:
            a = int(255 * min(1, t / 0.5) * min(1, (INTRO + 0.8 - t) / 0.8)); dr.rectangle([0, 0, base.width, base.height], fill=PAPER + (int(a * 0.85),))
            tw = dr.textlength('文密 · 1916', font=fCb); dr.text(((base.width - tw) / 2, base.height / 2 - 70 * s), '文密 · 1916', font=fCb, fill=RED + (a,))
            sub = '東京 ↔ 肇慶 · 雲南'; tw = dr.textlength(sub, font=fC); dr.text(((base.width - tw) / 2, base.height / 2 + 20 * s), sub, font=fC, fill=INK + (a,))
        if t > t_of(11, 20) + 0.3:
            a = int(255 * min(1, (t - t_of(11, 20) - 0.3) / 0.8)); dr.rectangle([0, 0, base.width, base.height], fill=PAPER + (int(a * 0.6),))
            msg = '1916 · G0 7 · Y0 10'; tw = dr.textlength(msg, font=fT); dr.text(((base.width - tw) / 2, base.height / 2 - 20 * s), msg, font=fT, fill=INK + (a,))
        im.resize((W, H), Image.LANCZOS).save(os.path.join(tmp, 'f%05d.png' % i))
        if i == int((t_of(7, 19) + 1.6) * FPS): im.resize((W, H), Image.LANCZOS).save(os.path.join(MEDIA, 'history-poster.jpg'), quality=82)
    encode(tmp, os.path.join(MEDIA, 'history.mp4')); shutil.rmtree(tmp)
    for lang, T in HISTORY_TEXT.items():
        cues = sorted((a, b, T[k]) for k, (a, b) in HISTORY_CUES.items())
        vtt(os.path.join(MEDIA, 'history.%s.vtt' % lang), cues)
    print('vidéo histoire', round(total, 1), 's,', os.path.getsize(os.path.join(MEDIA, 'history.mp4')) // 1024, 'Ko')

# ---------------------------------------------------------------- animation du déchiffrement
G0C, G0V = 'hgfdcbzyxwvtsrqpnmlk', 'aeiou'
G0 = {c + v: 10 * (i // 2) + (j if i % 2 == 0 else 9 - j) for i, c in enumerate(G0C) for j, v in enumerate(G0V)}
UNITS_0416B = 'fa zi hi pe go we ze lu cu na ha mo da ro do vo ro ke si ya xo du go lu ro xo xo tu hi ca he ma te mi ba qi he yu xi fa'.split()
CHARS_0416B = '報傳取消日人態度遽變確否速示俾便行止伸睟'
DEC_CUES = {  # secondes
    'form': (0.2, 3.6), 'letters': (3.8, 7.0), 'pairs': (7.2, 11.5), 'grid': (11.6, 16.0), 'code': (16.1, 19.5),
    'fast': (19.6, 25.5), 'end': (25.6, 29.4), 'fix': (29.5, 35.5)}
DEC_TEXT = {
 'fr': {'form': "Un formulaire japonais du 19 juillet 1916 : « 2429 1378 » se lit 文密, puis viennent les lettres chiffrées.",
        'letters': "Le message est un flux de lettres, coupé en mots de dix.", 'pairs': "On le relit deux lettres à la fois : chaque syllabe vaut un nombre de 00 à 99.",
        'grid': "La grille G0 donne ce nombre : la consonne indique la dizaine, la voyelle l'unité.", 'code': "Deux syllabes forment un code télégraphique chinois à quatre chiffres, donc un caractère.",
        'fast': "Et ainsi de suite, sans aucune autre clé.", 'end': "« On annonce une annulation ; l'attitude des Japonais a brusquement changé… »",
        'fix': "Le dernier code n'a pas de sens : une seule lettre est fausse (i au lieu de e, ·· au lieu de · en Morse). Corrigé : 皓, « le 19 »."},
 'en': {'form': "A Japanese form of 19 July 1916: \"2429 1378\" reads 文密, followed by the enciphered letters.",
        'letters': "The message is a stream of letters, cut into ten-letter words.", 'pairs': "Read it two letters at a time: each syllable stands for a number from 00 to 99.",
        'grid': "The G0 grid gives that number: the consonant gives the tens, the vowel the units.", 'code': "Two syllables make a four-digit Chinese telegraph code, hence one character.",
        'fast': "And so on, with no other key.", 'end': "\"A cancellation is reported; the attitude of the Japanese has suddenly changed…\"",
        'fix': "The last code makes no sense: a single letter is wrong (i instead of e, ·· instead of · in Morse). Corrected: 皓, \"the 19th\"."},
 'zh-hans': {'form': "1916年7月19日的日本电报纸：“2429 1378”读作“文密”，其后是密文字母。",
        'letters': "电文是一串字母，每十个字母一组。", 'pairs': "每次读两个字母：每个音节代表 00 到 99 之间的一个数。",
        'grid': "G0 表给出这个数：辅音表示十位，元音表示个位。", 'code': "两个音节组成一个四位中文电码，也就是一个汉字。",
        'fast': "依此类推，不需要任何其他密钥。", 'end': "“报传取消，日人态度遽变……”",
        'fix': "最后一个电码没有意义：只错了一个字母（e 误为 i，莫尔斯电码 · 误为 ··）。改正后为“皓”，即十九日。"},
 'zh-hant': {'form': "1916年7月19日的日本電報紙：「2429 1378」讀作「文密」，其後是密文字母。",
        'letters': "電文是一串字母，每十個字母一組。", 'pairs': "每次讀兩個字母：每個音節代表 00 到 99 之間的一個數。",
        'grid': "G0 表給出這個數：子音表示十位，母音表示個位。", 'code': "兩個音節組成一個四位中文電碼，也就是一個漢字。",
        'fast': "依此類推，不需要任何其他密鑰。", 'end': "「報傳取消，日人態度遽變……」",
        'fix': "最後一個電碼沒有意義：只錯了一個字母（e 誤為 i，摩斯電碼 · 誤為 ··）。改正後為「皓」，即十九日。"},
 'ja': {'form': "1916年7月19日の日本の電報用紙：「2429 1378」は「文密」と読め、その後に暗号文字が続く。",
        'letters': "電文は文字の列で、10文字ずつに区切られている。", 'pairs': "2文字ずつ読む。各音節は00から99までの数を表す。",
        'grid': "G0 表がその数を与える。子音が十の位、母音が一の位。", 'code': "二つの音節で4桁の中国電信符号、つまり一つの漢字になる。",
        'fast': "以下同様。ほかの鍵は一切いらない。", 'end': "「取り消しとの報あり。日本側の態度が急変した……」",
        'fix': "最後の符号は意味をなさない。誤りは一文字だけ（e が i に、モールスで · が ··）。訂正すると「皓」、十九日。"},
}

def make_decoder():
    W, H, s = 1280, 720, 2; W2, H2 = W * s, H * s
    form = Image.open(os.path.join(IMG, 'jacar-B03050090000-fr0416b.jpg')).convert('RGB')
    fm, fs, fc, fcb, fsm = F('mono', 26 * s), F('serif', 18 * s), F('cjk', 46 * s), F('cjkb', 120 * s), F('mono', 15 * s)
    letters = ''.join(UNITS_0416B)
    # géométrie de la grille (à gauche)
    gx, gy, cw, chh = 40 * s, 70 * s, 50 * s, 28 * s
    def cell(c, v): return gx + (1 + G0V.index(v)) * cw, gy + (1 + G0C.index(c)) * chh
    total = DEC_CUES['fix'][1] + 0.6; n = int(total * FPS); tmp = tempfile.mkdtemp(prefix='wenmi-dec-')
    slow = 3                                            # codes décomposés lentement
    sched = []                                          # (t début, index du code)
    t = DEC_CUES['pairs'][0]
    for k in range(20):
        sched.append((t, k)); t += (4.2 if k == 0 else 1.6) if k < slow else 0.30
    for i in range(n):
        t = i / FPS; im = Image.new('RGB', (W2, H2), PAPER); dr = ImageDraw.Draw(im, 'RGBA')
        if t < DEC_CUES['form'][1] + 0.4:               # formulaire
            a = min(1, t / 0.5) * min(1, (DEC_CUES['form'][1] + 0.4 - t) / 0.5)
            fw = int(W2 * 0.86); fh = int(form.height * fw / form.width); fi = form.resize((fw, fh), Image.LANCZOS)
            im.paste(Image.blend(Image.new('RGB', fi.size, PAPER), fi, max(0, a)), ((W2 - fw) // 2, (H2 - fh) // 2))
        else:
            # grille G0
            for j, v in enumerate(G0V): dr.text((gx + (1 + j) * cw + 14 * s, gy), v, font=fsm, fill=MUTED)
            cur = None
            for st, k in sched:
                if t >= st: cur = (st, k)
            hl = set()
            if cur and t < DEC_CUES['end'][0]:
                st, k = cur; dt = t - st; dur = (4.2 if k == 0 else 1.6) if k < slow else 0.30
                if k < slow:
                    if dt > dur * 0.15: hl.add(UNITS_0416B[2 * k])
                    if dt > dur * 0.45: hl.add(UNITS_0416B[2 * k + 1])
                else: hl = {UNITS_0416B[2 * k], UNITS_0416B[2 * k + 1]}
            for r, c in enumerate(G0C):
                dr.text((gx + 10 * s, gy + (1 + r) * chh), c, font=fsm, fill=INK)
                for v in G0V:
                    x, y = cell(c, v); on = (c + v) in hl
                    if on: dr.rounded_rectangle([x - 2 * s, y - 2 * s, x + cw - 6 * s, y + chh - 4 * s], radius=4 * s, fill=RED)
                    dr.text((x + 8 * s, y + 2 * s), '%02d' % G0[c + v], font=fsm, fill=PAPER if on else (INK if r % 2 == 0 else TEAL))
            # flux de lettres (en haut à droite)
            rx = 360 * s; ry = 60 * s
            shown = len(letters) if t > DEC_CUES['letters'][1] else int(len(letters) * ease((t - DEC_CUES['letters'][0]) / 3.0))
            done = sum(1 for st, k in sched if t >= st)
            for p in range(shown):
                gi = p // 10; col = p % 10; line, pos = divmod(gi, 4)
                x = rx + (pos * 11 + col) * 19 * s; y = ry + line * 40 * s
                k = p // 4; color = INK
                if cur and k == cur[1] and t < DEC_CUES['end'][0]: color = RED
                elif k < done - 1 or (t >= DEC_CUES['end'][0]): color = MUTED
                dr.text((x, y), letters[p], font=fm, fill=color)
            # décomposition du code courant
            if cur and t < DEC_CUES['end'][0]:
                st, k = cur; dt = t - st; dur = (4.2 if k == 0 else 1.6) if k < slow else 0.30
                u1, u2 = UNITS_0416B[2 * k], UNITS_0416B[2 * k + 1]; code = '%02d%02d' % (G0[u1], G0[u2])
                bx, by = rx + 40 * s, 230 * s
                if k < slow:
                    dr.text((bx, by), u1, font=F('mono', 56 * s), fill=RED if dt > dur * 0.1 else MUTED)
                    dr.text((bx + 200 * s, by), u2, font=F('mono', 56 * s), fill=RED if dt > dur * 0.4 else MUTED)
                    if dt > dur * 0.25: dr.text((bx, by + 80 * s), '%02d' % G0[u1], font=F('mono', 56 * s), fill=INK)
                    if dt > dur * 0.55: dr.text((bx + 200 * s, by + 80 * s), '%02d' % G0[u2], font=F('mono', 56 * s), fill=INK)
                    if dt > dur * 0.70:
                        dr.text((bx + 420 * s, by + 80 * s), '→ ' + code, font=F('mono', 56 * s), fill=TEAL)
                        dr.text((bx + 470 * s, by - 40 * s), CHARS_0416B[k], font=fcb, fill=RED)
                else:
                    dr.text((bx, by + 40 * s), '%s %s → %s → ' % (u1, u2, code), font=F('mono', 44 * s), fill=INK)
                    dr.text((bx + 600 * s, by + 10 * s), CHARS_0416B[k], font=F('cjkb', 90 * s), fill=RED)
            # texte reconstitué (en bas)
            tx, ty = rx, 520 * s
            nchars = done if t < DEC_CUES['end'][0] else 20
            for k in range(nchars):
                if cur and k == cur[1] and t < DEC_CUES['end'][0] and k < slow and (t - cur[0]) < ((4.2 if k == 0 else 1.6) * 0.85): continue
                ch = CHARS_0416B[k]; color = INK
                if k == 19:
                    color = GOLD
                    if t > DEC_CUES['fix'][0] + 2.5: ch, color = '皓', RED
                dr.text((tx + k * 44 * s, ty), ch, font=fc, fill=color)
            if t > DEC_CUES['fix'][0]:
                a = int(255 * min(1, (t - DEC_CUES['fix'][0]) / 0.6))
                fx = tx; fm2 = F('mono', 28 * s)
                dr.text((fx, ty + 66 * s), 'xifa → 4210 ?', font=fm2, fill=GOLD + (a,))
                if t > DEC_CUES['fix'][0] + 1.2:
                    dr.text((fx, ty + 104 * s), 'xefa → 4110 →', font=fm2, fill=RED + (a,))
                    dr.text((fx + dr.textlength('xefa → 4110 → ', font=fm2), ty + 98 * s), '皓', font=F('cjkb', 34 * s), fill=RED + (a,))
                    dr.text((fx + 340 * s, ty + 66 * s), 'i ··', font=fm2, fill=GOLD + (a,))
                    dr.text((fx + 340 * s, ty + 104 * s), 'e ·', font=fm2, fill=RED + (a,))
            dr.text((W2 - 330 * s, H2 - 40 * s), '0416b · 19.VII.1916 · G0', font=fsm, fill=MUTED)
        im.resize((W, H), Image.LANCZOS).save(os.path.join(tmp, 'f%05d.png' % i))
        if i == int(13.0 * FPS): im.resize((W, H), Image.LANCZOS).save(os.path.join(MEDIA, 'decoder-poster.jpg'), quality=82)
    encode(tmp, os.path.join(MEDIA, 'decoder.mp4')); shutil.rmtree(tmp)
    for lang, T in DEC_TEXT.items():
        vtt(os.path.join(MEDIA, 'decoder.%s.vtt' % lang), [(a, b, T[k]) for k, (a, b) in DEC_CUES.items()])
    print('vidéo déchiffrement', round(total, 1), 's,', os.path.getsize(os.path.join(MEDIA, 'decoder.mp4')) // 1024, 'Ko')

if __name__ == '__main__':
    land = load_land(sys.argv[1]); what = sys.argv[2] if len(sys.argv) > 2 else 'all'
    if what in ('map', 'all'): make_map(land)
    if what in ('history', 'all'): make_history(land)
    if what in ('decoder', 'all'): make_decoder()
