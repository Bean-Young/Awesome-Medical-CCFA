"""Merge reviewed collector records. Run with --source-dir pointing to collectors' output."""
import argparse,json,pathlib,re,datetime,shutil
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',default='/workspace/shared');args=ap.parse_args();src=pathlib.Path(args.source_dir);root=pathlib.Path(__file__).resolve().parents[1];out=root/'data';out.mkdir(exist_ok=True)
def read(name,default):
 p=src/name
 try:return json.loads(p.read_text()) if p.exists() else default
 except json.JSONDecodeError:return default
def key(p):return re.sub(r'[^a-z0-9]','',p['title'].lower())+'_'+str(p['year'])
assets=read('paper_assets.json',{});enrich=read('paper_enrichment.json',{});scope=read('ccfa_scope.json',{});allowed={x['acronym'].lower() for x in scope.get('conferences',[])};papers=[];pending=[];seen=set()
for name in ['vision_papers.json','language_papers.json','ml_enriched_papers.json','ml_papers.json']:
 records=read(name,[])
 if isinstance(records,dict):records=records.get('papers',[])
 for p in records:
  if not p.get('title') or not 2021<=int(p.get('year',0))<=2025:continue
  if allowed and p.get('venue','').lower() not in allowed:continue
  status=p.get('screening_status','').lower()
  if name=='ml_enriched_papers.json' and (p.get('relevance_tier')!='primary_medical_biomedical' or not p.get('abstract')):
   pending.append(p);continue
  if 'candidate' in status or 'pending' in status:pending.append(p);continue
  k=key(p)
  if k in seen:continue
  seen.add(k)
  p['authors']=[a.get('name',str(a)) if isinstance(a,dict) else a for a in p.get('authors',[])]
  topics=p.get('domain_tags',[]) or p.get('tags',[]) or p.get('keywords',[])
  topic=', '.join(topics[:2]).replace('_',' ') or 'medical and biomedical research'
  p['summary']='This '+str(p['year'])+' '+p['venue']+' paper addresses '+p['title'].rstrip('.').lower()+', in the area of '+topic+'.'
  p['summary_method']='Title-based descriptive introduction; consult the abstract for methods and findings.'
  asset=assets.get(p.get('id'))
  if asset:
   p['paper_asset']={k:v for k,v in asset.items() if k!='local_path'}
   p['main_figure']=asset.get('main_figure') or asset.get('figure_url') or asset.get('image_path') or asset.get('figure_path') or asset.get('path')
  if asset and asset.get('local_path') and pathlib.Path(asset['local_path']).exists():
   dest=root/asset['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(asset['local_path'],dest)
  p['keywords']=list(dict.fromkeys(p.get('domain_tags',[])+p.get('tags',[])+p.get('keywords',[])))
  p['pdf_url']=p.get('pdf_url') or p.get('pdf');p['citation_count']=None;p['citation_date']=None
  e=enrich.get(k)
  if e and e.get('status')=='matched':
   p['enrichment']=e;p['citation_count']=e.get('citation_count');p['citation_date']=e.get('retrieved_at');p['citation_source']=e.get('openalex_id')
   if not p.get('affiliations'):
    p['affiliations']=list(dict.fromkeys(i['name'] for a in e.get('author_affiliations',[]) for i in a.get('institutions',[])));p['affiliations_source']=e.get('openalex_id');p['affiliations_status']='Publication-linked OpenAlex metadata; not independently checked against PDF'
  p['affiliations']=p.get('affiliations') or [];p['id']=p.get('id') or k
  p['abstract_available']=bool(p.get('abstract'))
  p.pop('abstract',None)
  papers.append(p)
pending=list({key(p):p for p in pending if key(p) not in seen}.values())
for p in pending:
 p.pop('abstract',None);p.pop('summary',None);p.pop('summary_en',None)
coverage=[]
for name in ['vision_coverage.json','language_coverage.json','ml_coverage.json']:
 rows=read(name,[])
 if isinstance(rows,dict):rows=rows.get('events',rows.get('coverage',[]))
 for c in rows:
  c['denominator']=c.get('eligible_papers',c.get('full_paper_count',c.get('total_papers',c.get('full_paper_denominator'))))
  c['source_url']=c.get('source_url',c.get('source'));c['track']=c.get('track','main conference papers')
  coverage.append(c)
papers.sort(key=lambda p:(-int(p['year']),p['title'].lower()))
data={'papers':papers,'coverage':coverage,'scope':scope,'pending_candidate_count':len(pending),'built_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
for name,obj in [('papers.json',papers),('coverage.json',coverage),('scope.json',scope),('pending_candidates.json',pending),('snapshot.json',data)]: (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
(out/'snapshot.js').write_text('window.ATLAS_DATA = '+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';\n')
print(json.dumps({'papers':len(papers),'pending_candidates':len(pending),'events':len(coverage),'citations':sum(p['citation_count'] is not None for p in papers)}))
