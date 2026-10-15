"""Validate public payload, referential integrity, and safe missing-value handling."""
import json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[1];d=json.loads((root/'data/snapshot.json').read_text());papers=d['papers'];assert len(d['scope']['conferences'])==58
keys=set();ids=set()
for p in papers:
 assert p['id'] not in ids;ids.add(p['id'])
 k=(re.sub(r'[^a-z0-9]','',p['title'].lower()),p['year']);assert k not in keys;keys.add(k)
 assert 2020<=p['year']<=2025
 assert p['venue'] in {v['acronym'] for v in d['scope']['conferences']}
 assert 'abstract' not in p,'Full abstract leaked into public snapshot'
 assert p.get('summary') and p.get('summary_method')
 if p.get('citation_count') is not None:
  assert p['citation_count']>=0 and p.get('citation_date') and p.get('citation_source')
 if p.get('main_figure') and not p['main_figure'].startswith('http'):
  assert (root/p['main_figure']).is_file()
for f in ['papers.json','pending_candidates.json']:
 for p in json.loads((root/'data'/f).read_text()):assert 'abstract' not in p
for c in d['coverage']:
 den=c.get('denominator');assert den is None or den>=0
 n=sum(p['venue']==c['venue'] and p['year']==c['year'] for p in papers)
 if den:assert n<=den,(c,n)
js=(root/'data/snapshot.js').read_text();assert json.loads(js.removeprefix('window.ATLAS_DATA = ').strip().removesuffix(';').replace('<\\/','</'))==d
print(f'PASS: {len(papers)} unique paper records; 58-venue scope; citations, assets, denominators, public-text boundaries, snapshot equivalence.')
