#!/usr/bin/env node
// Corpus-derived editorial checks. Run after tools/build.py.
// Optional: --baseline <git-ref> checks preservation of telegrams and translations.
// Optional: --report <path> saves the inventory and checks as JSON.
const fs = require('fs'), path = require('path'), vm = require('vm');
const assert = require('assert/strict'), cp = require('child_process');
const root = path.resolve(__dirname, '..');
const langs = {fr:'fr', en:'en', ja:'ja', 'zh-hant':'zh-Hant', 'zh-hans':'zh-Hans'};
const arg = name => process.argv.includes(name) ? process.argv[process.argv.indexOf(name)+1] : null;
const baseline = arg('--baseline');
const read = p => fs.readFileSync(path.join(root,p),'utf8');
function load(source) {
  const context = {window:{}}; vm.createContext(context);
  vm.runInContext(source, context);
  return JSON.parse(JSON.stringify(context.window));
}
function previous(file) {
  return cp.execFileSync('git',['show',`${baseline}:${file}`],{cwd:root,encoding:'utf8'});
}
function numbers(s) { return (s.match(/\d+(?:[.,]\d+)?/g)||[]).map(Number); }
function text(s) { return s.replace(/<[^>]*>/g,''); }
const data = {}, files = fs.readdirSync(path.join(root,'assets/js')).filter(f=>/^corpus.*\.js$/.test(f));
const metrics = {}, checks = [], ids = new Set();
for (const file of files) {
  const relative = 'assets/js/'+file, current = load(read(relative));
  Object.assign(data,current);
  const old = baseline ? load(previous(relative)) : null;
  for (const [name, corpus] of Object.entries(current)) {
    if (!corpus.messages) continue;
    const m = {texts:corpus.messages.length,codes:0,doubtful:0,illegible:0,proposals:0,unresolved:0};
    for (const message of corpus.messages) {
      assert(!ids.has(message.id),`Duplicate message id: ${message.id}`);ids.add(message.id);
      assert.equal(message.codes.length,message.chars.length,message.id+' code/character length');
      assert.equal(message.codes.length,message.status.length,message.id+' status length');
      const proposed = new Set(message.readable.props.map(p=>p.i));
      m.codes += message.codes.length;m.proposals += proposed.size;
      message.status.forEach((s,i)=>{
        if(s==='douteux')m.doubtful++;
        if(s==='illisible')m.illegible++;
        if(['douteux','illisible'].includes(s)&&!proposed.has(i))m.unresolved++;
      });
    }
    for (const [field,value] of Object.entries({tels:m.texts,codes:m.codes,douteux:m.doubtful,illisible:m.illegible,props:m.proposals})) {
      if(field in corpus.stats)assert.equal(corpus.stats[field],value,`${name}.stats.${field}`);
    }
    if(old)assert.deepEqual(corpus.messages,old[name].messages,`${name}: telegram data changed`);
    const i18n = current[name+'_I18N'];
    if(i18n)for(const locale of Object.values(langs)) {
      assert(i18n[locale],name+' missing locale '+locale);
      for(const message of corpus.messages) {
        assert(i18n[locale].date[message.id],name+' missing date '+message.id);
        // Chinese pages use the Chinese original; the new batch additionally provides excerpts.
        if(!locale.startsWith('zh')||name==='WENMI_INEDITS')assert(i18n[locale].tr[message.id],name+' missing translation '+message.id+' '+locale);
      }
      if(old)assert.deepEqual(i18n[locale].tr,old[name+'_I18N'][locale].tr,`${name}: translations changed`);
    }
    metrics[name] = m;
  }
}
checks.push('All published corpus summaries match message arrays; dates and translations cover five languages.');
const systems=load(read('assets/js/systems.js')).WENMI_SYSTEMS;
for(const [corpus,mapping] of Object.entries(systems.map))for(const message of data['WENMI_'+corpus].messages) {
  assert(mapping[message.grid],`${corpus}: unmapped key ${message.grid}`);
  for(const locale of Object.values(langs))assert(systems.text[locale].sys[mapping[message.grid]],locale+' missing system');
}
const grids={};
for(const grid of ['G0','Y0']) {
  const messages=data.WENMI_CORPUS.messages.filter(m=>m.grid===grid);
  grids[grid]={texts:messages.length,codes:0,doubtful:0,illegible:0,unresolved:0};
  for(const m of messages) {
    const props=new Set(m.readable.props.map(p=>p.i));grids[grid].codes+=m.codes.length;
    m.status.forEach((s,i)=>{
      if(s==='douteux')grids[grid].doubtful++;
      if(s==='illisible')grids[grid].illegible++;
      if(['douteux','illisible'].includes(s)&&!props.has(i))grids[grid].unresolved++;
    });
  }
}
// The forms/text distinction comes from the documented assembly of the Y0 corpus.
assert.equal(grids.Y0.texts,10);
const initialCorrections=data.WENMI_C1916.stats.corr, laterCorrections=data.WENMI_C1916.stats.dx;
for(const [lang,locale]of Object.entries(langs)) {
  const home=read(`content/${lang}/index.html`);
  for(const corpus of ['T1915','F1916']) {
    const summary=home.match(new RegExp(`<span data-corpus-summary="${corpus}">([\\s\\S]*?)</span>`));
    assert(summary,lang+' missing summary '+corpus);
    assert.deepEqual(numbers(summary[1]).sort((a,b)=>a-b),[metrics['WENMI_'+corpus].codes,metrics['WENMI_'+corpus].doubtful,metrics['WENMI_'+corpus].illegible].sort((a,b)=>a-b),lang+' summary '+corpus);
  }
  const y0=home.match(/<li id="status-y0">([\s\S]*?)<\/li>/)[1], y=grids.Y0;
  const values=numbers(text(y0));
  for(const n of [15,y.texts,y.codes,y.doubtful,y.illegible,y.doubtful+y.illegible,y.unresolved])assert(values.includes(n),`${lang} Y0 lacks ${n}`);
  const uncertain=y.doubtful+y.illegible;
  for(const percent of [Number((100*uncertain/y.codes).toFixed(1)),Number((100*y.unresolved/y.codes).toFixed(1))]) {
    assert(text(y0).replaceAll(',','.').includes(String(percent)),lang+' Y0 percentage');
  }
  const card=home.match(/<a class="card" href="relecture.html">([\s\S]*?)<\/a>/)[1];
  for(const n of [initialCorrections,laterCorrections,initialCorrections+laterCorrections])assert(numbers(card).includes(n),lang+' review card');
  const corpusCard=home.match(/<a class="card" href="telegrams.html">([\s\S]*?)<\/a>/)[1];
  for(const m of Object.values(metrics))assert(numbers(corpusCard).includes(m.texts),lang+' corpus inventory');
  const ros=read(`content/${lang}/rosamonde.html`), method=read(`content/${lang}/method.html`), telegrams=read(`content/${lang}/telegrams.html`);
  assert.equal((ros.match(/<tbody>[\s\S]*?<\/tbody>/g)||[]).join('').match(/<tr>/g).length,22);
  assert(ros.includes('r23-note')&&method.includes('rosamonde-sample')&&method.includes('t1915-sample'),lang+' review scopes');
  const unresolved=telegrams.match(/<li id="wenmi-unresolved">([\s\S]*?)<\/li>/)[1];
  assert.equal(numbers(unresolved)[0],metrics.WENMI_CORPUS.unresolved,lang+' Wenmi unresolved count');
  const table=method.match(/<table class="tables-found">([\s\S]*?)<\/table>/)[1];
  assert.equal((table.match(/<tr>/g)||[]).length-1,14,lang+' table recap');
  assert(table.indexOf('Hong Kong')<table.indexOf('Laisaosang')&&table.indexOf('Laisaosang')<table.indexOf('New York')&&table.indexOf('Hsuweilin')<table.indexOf('Kai'),lang+' table chronology');
  for(const link of ['b45t','b51b'])assert(table.includes('#tinedits-c39-'+link),lang+' missing 1914 attestation');
  assert(method.includes('1.40')||method.includes('1,40'),lang+' Kai candidate gate');
  assert(method.includes('(20 × j + i + 1) modulo 100')&&method.includes('(5 × i + j + 1) modulo 100'),lang+' method definitions');
  assert(read(`${lang}/history.html`).includes('politique-militaire'),lang+' history missing');
  if(baseline) {
    const oldRos=previous(`content/${lang}/rosamonde.html`);
    assert.deepEqual(ros.match(/<tbody>[\s\S]*?<\/tbody>/g),oldRos.match(/<tbody>[\s\S]*?<\/tbody>/g),lang+' Rosamonde rows changed');
    assert.equal(telegrams.match(/<template id="y1917-tpl">[\s\S]*?<\/template>/)[0],previous(`content/${lang}/telegrams.html`).match(/<template id="y1917-tpl">[\s\S]*?<\/template>/)[0],lang+' 1917 template changed');
    const history=read(`content/${lang}/history.html`),oldHistory=previous(`content/${lang}/history.html`);
    const anchor='<h2 id="politique-militaire">';
    assert(history.includes(anchor)&&oldHistory.includes(anchor),lang+' political/military anchor missing');
    assert.equal(history.slice(history.indexOf(anchor)),oldHistory.slice(oldHistory.indexOf(anchor)),lang+' political/military article changed');
  }
}
checks.push('Home inventory, corrections, Y0 percentages, T1915/F1916 counters and Wenmi unresolved count agree in five languages.');
checks.push('Classification complete; 1914 attestations, 14 recap entries including Kai candidate, review scopes and method definitions present.');
if(baseline)checks.push(`All telegram arrays, translations, Rosamonde rows, 1917 template and political/military analysis unchanged from ${baseline}.`);
const report={baseline,metrics,grids,checks};
if(arg('--report'))fs.writeFileSync(arg('--report'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
