#!/usr/bin/env python3
"""Manifest verifier for the rank-12 Delsarte route-cut packet."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'experimental/data/certificates/kb-mca-rank12-delsarte-route-cut-v1/manifest.json'
def main():
 m=json.loads(MANIFEST.read_text());assert m['schema']=='kb-mca-rank12-delsarte-route-cut-manifest-v1';assert m['parent']=='d01c546f4dca70e256c18c142873821b3bb48ab5'
 result=(ROOT/m['result']).read_bytes();assert hashlib.sha256(result).hexdigest()==m['result_sha256'];obj=json.loads(result);canonical=json.dumps(obj,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(canonical).hexdigest()==m['canonical_payload_sha256'];assert m['claims']==obj['claims']
 seen=set()
 for item in m['files']:
  path=item['path'];assert path not in seen;seen.add(path);data=(ROOT/path).read_bytes();assert len(data)==item['bytes'];assert hashlib.sha256(data).hexdigest()==item['sha256']
 print(f"KB_MCA_RANK12_DELSARTE_ROUTE_CUT_MANIFEST_PASS files={len(seen)} payload={m['canonical_payload_sha256']}")
if __name__=='__main__':main()
