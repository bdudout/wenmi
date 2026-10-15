#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the reviewed C39/C40 batch, keeping diplomatic readings and alignment hypotheses distinct.
Usage: python3 tools/build_inedits.py ../wenmi
Input: cryptanalysis/c40/site/inedits_data.json, frozen by prepare_inedits.py.
Output: assets/js/corpus-inedits.js and a public selection/provenance manifest.
"""
import hashlib,html,json,re,sys
from pathlib import Path
SITE=Path(__file__).resolve().parents[1]
WENMI=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(SITE/'tools'))
import build_t1915 as BT
import c1916_i18n
BC=BT.BC;bkeys=BC.bkeys
bkeys.KEYS.update(k16=bkeys.make_table(15,'euoia'),k17=bkeys.make_table(11,'iuaeo'),kai=bkeys.make_table(4,'eoaui'),hsu1914={c+v:(5*i+j+1)%100 for i,c in enumerate('bcdfghjlmnpqrstvwxyz') for j,v in enumerate('aeiou')})
HK={c:str(i) for i,c in enumerate('ykulocapit')};HK['z']='0'
LANGS=('fr','en','zh-Hant','ja')
# These tables are credited in sources/acknowledgements, rather than in the new telegram text.
NAMES={'k16':'Sixteenth','k17':'Seventeenth','kai':'Kai','hsu1914':'Hsuweilin','hk1914':'Hong Kong','ctc':'CTC','laisaosang1915':'Laisaosang','newyork1915':'New York','shanghai1916':'Shanghai','seito1916':'Qingdao','sanfran1916':'San Francisco','manila1916':'Manila'}
TXT={
'fr':dict(title='Inédits 1913–1916',intro='<p><strong>50 télégrammes, inédits à notre connaissance : 11 de 1913–1914 et 39 d’avril 1916.</strong> Copies de la série japonaise <span lang="ja">特定人ノ発受郵便物取調</span>, JACAR B03050087300–87500 et B03050088500–88600, dossiers non encore étudiés dans cette enquête. Lettres lues par Claude, relecture de Brice Dudout appliquée sur transcription préremplie (non aveugle). Quatre tables nouvellement représentées : « Sixteenth », « Seventeenth », « Hsuweilin » et « Hong Kong » ; les autres sont déjà documentées (<a href="sources.html#s1">tables publiées</a>, <a href="sources.html#s24">archives et provenance du lot</a>). Les identités non établies restent non identifiées. Les six télégrammes d’avril non lus sont exclus, ainsi que trois lectures trop fragiles de 1914.</p><p><strong>Une lecture partielle reste partielle.</strong> Les caractères douteux sont signalés ; la traduction de travail ne comble pas les passages manquants. Les mots répétés les 14 et 21 avril, confirmés sur l’image par Brice, sont conservés. La transcription relue reste affichée intégralement : dans les cases, « ? » est une lettre ajoutée par le recalage du solveur, jamais une lettre certifiée sur le scan. Les détails indiquent aussi les suppressions. Le décodage brut précède la version ponctuée ; les propositions retenues restent marquées.</p>',read='Transcription du formulaire (Claude, puis relecture de Brice ; sans recalage)',label='Traduction de travail, passages incertains omis ou signalés.',rawLabel='Décodage brut de la transcription, avant recalage',alignmentLabel='Recalage proposé (positions à partir de 1 ; dans le flux après le préfixe)',alignmentLegend='? = lettre proposée, non confirmée sur le scan',noteLabel='Note',stats='{tels} télégrammes, {codes} codes ; {douteux} douteux, {illisible} illisibles ; {props} propositions.'),
'en':dict(title='Unpublished telegrams, 1913–1916',intro='<p><strong>50 telegrams, unpublished as far as we know: 11 from 1913–1914 and 39 from April 1916.</strong> Copies in the Japanese series <span lang="ja">特定人ノ発受郵便物取調</span>, JACAR B03050087300–87500 and B03050088500–88600, files not previously studied in this investigation. Claude’s readings incorporate Brice Dudout’s review of prefilled transcriptions (not blind). Four newly represented tables: “Sixteenth”, “Seventeenth”, “Hsuweilin” and “Hong Kong”; the others are already documented (<a href="sources.html#s1">published tables</a>, <a href="sources.html#s24">archives and batch provenance</a>). Unestablished identities remain unidentified. Six unreadable April telegrams and three fragile readings from 1914 are excluded.</p><p><strong>Partial readings remain partial.</strong> Doubtful characters stay marked; the working translation does not fill gaps. Repeated words on 14 and 21 April, confirmed on the images by Brice, are retained. The reviewed transcription is displayed in full: “?” in the cells is a letter added by the solver’s alignment, never a letter certified on the scan. The details also record deletions. Raw decoding precedes the punctuated edition; retained proposals stay marked.</p>',read='Form transcription (Claude, then Brice’s review; before alignment)',label='Working translation; uncertain passages omitted or indicated.',rawLabel='Raw decoding of the transcription, before alignment',alignmentLabel='Proposed alignment (positions from 1, in the stream after the prefix)',alignmentLegend='? = proposed letter, not confirmed on the scan',noteLabel='Note',stats='{tels} telegrams, {codes} codes; {douteux} doubtful, {illisible} unreadable; {props} proposals.'),
'zh-Hant':dict(title='1913–1916年未刊電報',intro='<p><strong>就我們所知此前未刊的50封電報：1913–1914年11封、1916年4月39封。</strong>日本「特定人ノ発受郵便物取調」抄件，JACAR B03050087300–87500及B03050088500–88600，為本調查此前未研究的卷宗。Claude讀出的字母已套用Brice Dudout對預填轉寫的複核（非盲讀）。本批新增展示「Sixteenth」「Seventeenth」「Hsuweilin」「Hong Kong」四張表；其餘表已有記錄（<a href="sources.html#s1">已發表碼表</a>、<a href="sources.html#s24">檔案與本批來源</a>）。未確定的身分不作認定。四月六封未讀出的電報及1914年三項脆弱讀法不予刊出。</p><p><strong>局部讀通不等於全文確定。</strong>存疑字保留標記，工作譯文不補足缺文。4月14日及21日的重複詞經Brice核對圖像後保留。複核的轉寫完整展示；格內「?」表示求解器為重新對齊而添加、尚未由圖像證實的字母，刪除操作亦有記錄。先列未重新對齊的直接解碼，再列加標點的讀本，保留已採納提案的標記。</p>',read='電報紙轉寫（Claude讀出，Brice複核；重新對齊前）',label='工作譯文／節錄；存疑段落不補足。',rawLabel='轉寫的直接解碼（重新對齊前）',alignmentLabel='建議重新對齊（扣除前綴後字流的位置，自1起）',alignmentLegend='?＝建議添加、未由圖像證實的字母',noteLabel='說明',stats='電報{tels}封，電碼{codes}個；存疑{douteux}個，未讀出{illisible}個；提案{props}個。'),
'ja':dict(title='1913〜1916年の未刊電報',intro='<p><strong>管見の限り未刊の電報50通：1913〜1914年11通、1916年4月39通。</strong>日本の「特定人ノ発受郵便物取調」の写し、JACAR B03050087300〜87500・B03050088500〜88600。本調査では未検討だった巻である。Claudeの読みにBrice Dudoutによる記入済み転写の校正を適用した（ブラインドではない）。本ロットでは「Sixteenth」「Seventeenth」「Hsuweilin」「Hong Kong」の4表を新たに展示する。他の表は既存のもの（<a href="sources.html#s1">公表済みの表</a>、<a href="sources.html#s24">史料と出所</a>）。未確定の人物は同定しない。4月の未解読6通と1914年の不確かな3件は掲載しない。</p><p><strong>部分的な読みを確定した全文とは扱わない。</strong>疑わしい字には印を付け、試訳で欠文を埋めない。4月14日・21日の重複語はBriceが画像で確認し、そのまま残した。校正済み転写を全文示す。升目の「?」はソルバーが整列のために補った、画像未確認の字母であり、削除も記録する。整列前の直接解読に続けて句読点付きの読みを示し、採用した提案にも印を残す。</p>',read='用紙の転写（Claudeの読み、Briceの校正；整列前）',label='試訳。未確定部分は省略または明記。',rawLabel='転写の直接解読（整列前）',alignmentLabel='整列の提案（接頭部を除いた文字列の位置、1から）',alignmentLegend='?＝画像未確認の補った字母',noteLabel='注',stats='電報{tels}通、符号{codes}個。疑問{douteux}個、判読不能{illisible}個、提案{props}個。')}
PERSON={'sun':{'fr':'Sun Yat-sen','en':'Sun Yat-sen','zh-Hant':'孫中山','ja':'孫文'},'lin':{'fr':'Lin Sen (林森)','en':'Lin Sen (林森)','zh-Hant':'林森','ja':'林森'},'yamada':{'fr':'Yamada Junzaburō (adresse « Junzaburo »)','en':'Yamada Junzaburō (address “Junzaburo”)','zh-Hant':'山田純三郎（「Junzaburo」地址）','ja':'山田純三郎（「Junzaburo」宛）'},'kayano':{'fr':'Kayano Nagatomo (萱野長知)','en':'Kayano Nagatomo (萱野長知)','zh-Hant':'萱野長知','ja':'萱野長知'},'yamanaka':{'fr':'Yamanaka Minetarō (山中峯太郎), Banzaikan','en':'Yamanaka Minetarō (山中峯太郎), Banzaikan','zh-Hant':'山中峯太郎，萬歲館','ja':'山中峯太郎、万歳館'},'toyama':{'fr':'Tōyama Mitsuru (adresse du formulaire)','en':'Tōyama Mitsuru (address on the form)','zh-Hant':'頭山滿（用紙上的地址）','ja':'頭山満（用紙の宛名）'}}
SIDE={'fr':('Expéditeur','Destinataire','non identifié'),'en':('Sender','Recipient','unidentified'),'zh-Hant':('發信人','收信人','未確定'),'ja':('発信者','受信者','未同定')}

def who(x,lang):
 labels=SIDE[lang]
 return '<p class="tg-who">'+'<br>'.join('<span class="who-k">'+labels[k]+'</span> <b>'+html.escape(PERSON[p][lang] if p else labels[2])+'</b>' for k,p in enumerate([x['who']['from'],x['who']['to']]))+'</p>'
def decode(x):
 s=x['effective'];key=x['key'];cs=[]
 for j in range(0,len(s)-3,4):
  g=s[j:j+4]
  if key=='ctc':code=g
  elif key=='hk1914':code=''.join(HK.get(c,'?') for c in g)
  else:code=BC.code_of(bkeys.KEYS[key],g)
  cs.append(code if code and code.isdigit() else '····')
 return cs

def path(g,key,ch):
 if key not in ('ctc','hk1914'):return BC.edit_path(g,bkeys.KEYS[key],ch)
 best=None
 for code in BC.CH2CODES.get(ch,[]):
  target=code if key=='ctc' else ''.join('ykulocapit'[int(c)] for c in code)
  dif=[k for k in range(4) if g[k]!=target[k] and not (g[k]=='z' and target[k]=='y')]
  if best is None or len(dif)<len(best['edits']):best=dict(code=code,to_letters=target,edits=[dict(**{'from':g[k],'to':target[k]},kind='autre',morse=['','']) for k in dif])
 return best

def build():
 source=WENMI/'cryptanalysis/c40/site/inedits_data.json'
 snapshot=SITE/'tools/data/inedits_data.json'
 data=json.loads((source if source.exists() else snapshot).read_text());msgs=[]
 snapshot.parent.mkdir(exist_ok=True)
 snapshot.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 for x in data:
  assert x['score']>=1.5 and x['score']>x['null']+1.5,x['id']
  codes=decode(x);chars=[BC.C2CH.get(c,'□') if c.isdigit() else '·' for c in codes]
  assert ''.join(chars)==x['aligned'],(x['id'],''.join(chars),x['aligned'])
  toks,props=BT.parse(x['read'],chars)
  marked=set();i=0;k=0;t=x['read']
  while k<len(t):
   c=t[k]
   if c=='「' and BT.restitution.is_clear(t,k):k=t.index('」',k)+1;continue
   if c in BT.PUNCT:k+=1;continue
   if c in '‹{':
    if c=='‹':marked.add(i)
    i+=1;k+=3;continue
   i+=1;k+=1
  inserted={p//4 for p in x['inserted']}
  statuses=['illisible' if not c.isdigit() or chars[i]=='□' else 'douteux' if i in marked or i in props or i in inserted else 'ok' for i,c in enumerate(codes)]
  pp=[]
  for i in props:
   ch=next(t[0] for t in toks if t[1]==i and t[2]);g=x['effective'][4*i:4*i+4];ep=path(g,x['key'],ch)
   assert ep and len(ep['edits'])<=2,(x['id'],i,ch,ep)
   pp.append(dict(i=i,ch=ch,orig=chars[i],level='P',reasons=['sens'],letters=g,image=None,**ep))
  # Any grouping hypothesis is visible via '?' and an explicit list; the original is displayed unaltered above.
  display=list(x['effective'])
  for p in x['inserted']:display[p]='?'
  tl=[''.join(display[j:j+4]) if x['key'] in ('ctc','hk1914') else ''.join(display[j:j+2])+'·'+''.join(display[j+2:j+4]) for j in range(0,len(display)-3,4)]
  y,m,d=x['date_iso'].split('-');page=int(re.search(r'image (\d+)',x['src']).group(1));record=x['src'].split(',')[0]
  nums=[int(c) if c.isdigit() else 0 for c in codes];after=nums[:]
  for p in pp:after[p['i']]=int(p['code'])
  msgs.append(dict(id=x['id'],label=x['frame'],grid=x['key'],toc=x['key'],year=int(y),md=[int(m),0 if '?' in d else int(d)],record=record,page=page,pages=x['pages'],time=None,fiche=dict(img=x['id'],n=x['frame']+' (PDF p. '+x['pages']+')',keys=x['keyw'],nomap=True),cipher=x['cipher'],letters=x['effective'][:4*len(codes)],tokenLetters=tl,rawText=x['raw'],alignment=dict(phase=x['phase'],edits=x['alignment_edits']),route=x['route']['en'],codes=codes,chars=chars,status=statuses,verified=[],fixed={},alts={},expected={},readable=dict(toks=toks,props=pp,score=[BC.mean_score(nums),BC.mean_score(after)]),validation=dict(score=x['score'],null=x['null']),_src=x))
 stats=dict(tels=len(msgs),codes=sum(len(m['codes']) for m in msgs),douteux=sum(s=='douteux' for m in msgs for s in m['status']),illisible=sum(s=='illisible' for m in msgs for s in m['status']),props=sum(len(m['readable']['props']) for m in msgs))
 i18n={}
 for l in LANGS:
  d=dict(TXT[l]);d['channel']={k:('code télégraphique en clair' if l=='fr' else 'unencrypted telegraph code' if l=='en' else '明碼電報' if l=='zh-Hant' else '平文の電信符号') if k=='ctc' else '“'+n+'”' for k,n in NAMES.items()}
  d['date']={m['id']:m['_src']['date']['zh' if l=='zh-Hant' else l] for m in msgs}
  d['route']={m['id']:m['_src']['route']['zh-hant' if l=='zh-Hant' else l] for m in msgs}
  d['who']={m['id']:who(m['_src'],l) for m in msgs}
  d['tr']={m['id']:m['_src']['tr'][l] for m in msgs};i18n[l]=d
 i18n['zh-Hans']=c1916_i18n.to_hans(i18n['zh-Hant'],c1916_i18n.t2s_table(str(WENMI)))
 for m in msgs:del m['_src']
 (SITE/'assets/js/corpus-inedits.js').write_text('// Generated by tools/build_inedits.py; reviewed readings and alignment hypotheses remain separate.\nwindow.WENMI_INEDITS = '+json.dumps(dict(messages=msgs,stats=stats),ensure_ascii=False)+';\nwindow.WENMI_INEDITS_I18N = '+json.dumps(i18n,ensure_ascii=False)+';\n')
 manifest=json.loads((WENMI/'cryptanalysis/c40/site/publication-audit.json').read_text())
 manifest['stats']=stats
 manifest['source_pdfs']={}
 for rec in sorted({x['src'].split(',')[0] for x in data}):
  p=WENMI/'sources'/('c35' if rec=='B03050087500' else 'c39')/'jacar'/(rec+'.pdf')
  manifest['source_pdfs'][rec]=dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
 manifest['tables']={k:bkeys.KEYS[k] for k in ['k16','k17','kai','hsu1914']};manifest['tables']['hk1914']=HK
 manifest['excluded_kai_note']='Kai is retained here for reproducibility, but no Kai telegram passes all publication criteria in this batch.'
 manifest['messages']=[dict(id=x['id'],source_id=x['source_id'],src=x['src'],cipher=x['cipher'],effective=x['effective'],inserted=x['inserted'],phase=x['phase'],alignment_edits=x['alignment_edits'],raw=x['raw'],read=x['read'],key=x['key'],score=x['score'],null=x['null']) for x in data]
 (SITE/'assets/data').mkdir(exist_ok=True)
 (SITE/'assets/data/inedits-1913-1916-provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 update_pages(msgs,stats,i18n)
 print(json.dumps(stats,ensure_ascii=False))

def update_pages(msgs,stats,i18n):
 facts={
 'fr':('télégrammes inédits de 1913–1916','quatre tables nouvellement représentées ; les passages incertains restent marqués'),
 'en':('unpublished telegrams from 1913–1916','four newly represented tables; uncertain passages remain marked'),
 'zh-hant':('1913–1916年未刊電報','新增展示四張碼表；存疑段落保留標記'),
 'zh-hans':('1913–1916年未刊电报','新增展示四张码表；存疑段落保留标记'),
 'ja':('1913〜1916年の未刊電報','新たに4表を展示。不確かな箇所には印を残す')}
 for lang,il in [('fr','fr'),('en','en'),('zh-hant','zh-Hant'),('zh-hans','zh-Hans'),('ja','ja')]:
  d=i18n[il];p=SITE/'content'/lang/'telegrams.html';t=p.read_text()
  block='<!-- inedits:start -->\n<section class="tg tg-group" id="inedits"><h2>'+d['title']+'</h2>'+d['intro']+'\n<p class="corpus-stats">'+d['stats'].format(**stats)+'</p>\n<nav class="tg-syslinks" aria-label="'+html.escape(d['title'],quote=True)+'">'+' '.join('<a href="#t'+m['id']+'">'+m['label']+'</a>' for m in msgs)+'</nav>\n<div id="inedits-corpus"></div>\n</section>\n<!-- inedits:end -->\n'
  if '<!-- inedits:start -->' in t:t=re.sub(r'<!-- inedits:start -->.*?<!-- inedits:end -->\n',lambda _:block,t,flags=re.S)
  else:t=t.replace('  <div id="corpus"></div>',block+'  <div id="corpus"></div>')
  p.write_text(t)
  p=SITE/'content'/lang/'index.html';t=p.read_text();a,b=facts[lang]
  fact='<!-- inedits-fact:start --><div class="fact"><b>'+str(stats['tels'])+'</b><span><a href="telegrams.html#inedits">'+a+'</a> : '+b+' ('+str(stats['codes'])+' codes, '+str(stats['douteux']+stats['illisible'])+' ?).</span></div><!-- inedits-fact:end -->'
  # Localized terminology for counters; only this new fact is generated here.
  phrase={'fr':f"{stats['codes']} codes, {stats['douteux']} douteux et {stats['illisible']} illisibles, {stats['props']} propositions",'en':f"{stats['codes']} codes, {stats['douteux']} doubtful and {stats['illisible']} unreadable, {stats['props']} proposals",'zh-hant':f"{stats['codes']}個電碼，{stats['douteux']}個存疑、{stats['illisible']}個未讀出，{stats['props']}項提案",'zh-hans':f"{stats['codes']}个电码，{stats['douteux']}个存疑、{stats['illisible']}个未读出，{stats['props']}项提案",'ja':f"{stats['codes']}符号、疑問{stats['douteux']}個、判読不能{stats['illisible']}個、提案{stats['props']}個"}[lang]
  fact=fact.replace(str(stats['codes'])+' codes, '+str(stats['douteux']+stats['illisible'])+' ?',phrase)
  if '<!-- inedits-fact:start -->' in t:t=re.sub(r'<!-- inedits-fact:start -->.*?<!-- inedits-fact:end -->',lambda _:fact,t,flags=re.S)
  else:
   t,n=re.subn(r'(<section class="facts"[^>]*>)',lambda m:m.group(1)+'\n    '+fact,t,count=1);assert n==1,lang
  p.write_text(t)
if __name__=='__main__':build()
