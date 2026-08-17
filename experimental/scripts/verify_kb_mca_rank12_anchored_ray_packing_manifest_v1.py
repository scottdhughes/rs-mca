#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'experimental/data/certificates/kb-mca-rank12-anchored-ray-packing-v1/manifest.json'
def blob_sha(data:bytes)->str:return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def main():
 m=json.loads(MANIFEST.read_text())
 if m['schema']!='kb-mca-rank12-anchored-ray-packing-manifest-v1':raise SystemExit('schema')
 for path,expected in m['git_blob_sha1'].items():
  if blob_sha((ROOT/path).read_bytes())!=expected:raise SystemExit('blob '+path)
 base={k:m[k] for k in ('schema','parent','result','claims','git_blob_sha1')}
 payload=hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 if payload!=m['canonical_payload_sha256']:raise SystemExit('payload')
 result=json.loads((ROOT/m['result']).read_text())
 if result['claims']!=m['claims'] or result['parent']!=m['parent']:raise SystemExit('result binding')
 print(f"KB_MCA_RANK12_ANCHORED_RAY_PACKING_MANIFEST_PASS files={len(m['git_blob_sha1'])} payload={payload}")
if __name__=='__main__':main()
