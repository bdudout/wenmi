#!/usr/bin/env python3
"""Reproduce full-page JACAR facsimiles for the reviewed batch (no generated imagery).
Keep page margins/frame numbers, and include continuation pages. Requires pdftoppm + Pillow.
Usage: python3 tools/make_fiches_inedits.py ../wenmi
"""
import json,subprocess,sys,tempfile
from pathlib import Path
from PIL import Image,ImageDraw
SITE=Path(__file__).resolve().parents[1];WENMI=Path(sys.argv[1]).resolve();OUT=SITE/'assets/img/fiches'
D=json.loads((WENMI/'cryptanalysis/c40/site/inedits_data.json').read_text())
cache={}
with tempfile.TemporaryDirectory() as tmp:
 for x in D:
  rec=x['src'].split(',')[0];pdf=(WENMI/'sources'/('c35' if rec=='B03050087500' else 'c39')/'jacar'/(rec+'.pdf'))
  a,*z=x['pages'].split('-');pages=list(range(int(a),int(z[0])+1 if z else int(a)+1));ims=[]
  for p in pages:
   key=(rec,p)
   if key not in cache:
    dest=Path(tmp)/(rec+'-'+str(p))
    subprocess.run(['pdftoppm','-f',str(p),'-l',str(p),'-scale-to','1900','-singlefile','-png',str(pdf),str(dest)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    cache[key]=Image.open(str(dest)+'.png').convert('RGB')
   ims.append(cache[key])
  im=Image.new('RGB',(max(v.width for v in ims),sum(v.height for v in ims)+36*(len(ims)-1)),'white');y=0
  for k,v in enumerate(ims):
   im.paste(v,(0,y));y+=v.height
   if k<len(ims)-1:ImageDraw.Draw(im).text((15,y+8),rec+' / PDF p. '+str(pages[k+1]),fill='black');y+=36
  im.save(OUT/('scan-'+x['id']+'-full.webp'),quality=82)
  thumb=im.copy();thumb.thumbnail((520,1100));thumb.save(OUT/('scan-'+x['id']+'.webp'),quality=78)
 print(len(D),'fiches;',len(cache),'source pages, with full margins and continuations')
