#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
M=ROOT/'experimental/data/certificates/kb-mca-rank11-uniform-line-repair-v1/manifest.json'
def main():
 m=json.loads(M.read_text());assert m['schema']=='kb-mca-rank11-uniform-line-repair-manifest-v1';assert m['parent']=='d01c546f4dca70e256c18c142873821b3bb48ab5'
 x=json.loads((ROOT/m['result']).read_text());c=json.dumps(x,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(c).hexdigest()==m['canonical_payload_sha256'];assert m['claims']==x['claims']
 print(f"KB_MCA_RANK11_UNIFORM_LINE_MANIFEST_PASS payload={m['canonical_payload_sha256']}")
if __name__=='__main__':main()
