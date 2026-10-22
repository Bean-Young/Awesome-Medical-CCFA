"""Run with Python 3 from this directory to verify and restore the current snapshot."""
import base64,gzip,hashlib,io,json,pathlib,tarfile
root=pathlib.Path(__file__).resolve().parent
m=json.loads((root/'current_snapshot_manifest.json').read_text())
parts=[]
for p in m['parts']:
 b=(root/p['path']).read_bytes()
 assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'],p['path']
 parts.append(b.strip())
encoded=b''.join(parts)
assert hashlib.sha256(encoded).hexdigest()==m['base64_sha256']
compressed=base64.b64decode(encoded,validate=True)
assert hashlib.sha256(compressed).hexdigest()==m['gzip_sha256']
raw=gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest()==m['tar_sha256']
out=root/'restored_current'; out.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as tar:
 for record in m['files']:
  name=record['path']; rel=pathlib.PurePosixPath(name)
  assert not rel.is_absolute() and '..' not in rel.parts
  b=tar.extractfile(name).read()
  assert len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256'],name
  dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
print('Verified and restored',len(m['files']),'files into',out.name)
