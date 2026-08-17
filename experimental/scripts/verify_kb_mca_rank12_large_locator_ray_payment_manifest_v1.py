#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
M=ROOT/'experimental/data/certificates/kb-mca-rank12-large-locator-ray-payment-v1/manifest.json'
def blob_sha(data:bytes)->str:
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def main():
 m=json.loads(M.read_text()); assert m['parent']=='ed556ccb7527e1c54e58b8d151ccefd8539000ac'
 rp=ROOT/m['result']; rb=rp.read_bytes(); assert blob_sha(rb)==m['result_git_blob_sha']
 r=json.loads(rb); assert hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()==m['canonical_payload_sha256']; assert m['claims']==r['claims']
 seen=set()
 for x in m['files']:
  assert x['path'] not in seen; seen.add(x['path']); assert blob_sha((ROOT/x['path']).read_bytes())==x['git_blob_sha']
 print('KB_MCA_RANK12_LARGE_LOCATOR_RAY_MANIFEST_PASS',f'files={len(seen)}',f"payload={m['canonical_payload_sha256']}")
if __name__=='__main__':main()
