#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];M=ROOT/'experimental/data/certificates/kb-mca-rank12-three-slope-wall-v1/manifest.json'
def main():
 m=json.loads(M.read_text());assert m['schema']=='kb-mca-rank12-three-slope-wall-manifest-v1';assert m['parent']=='8911e26e78c8d91173c413f079a13f88a04701fe';x=json.loads((ROOT/m['result']).read_text());c=json.dumps(x,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(c).hexdigest()==m['canonical_payload_sha256'];assert m['claims']==x['claims'];print(f"KB_MCA_RANK12_THREE_SLOPE_MANIFEST_PASS payload={m['canonical_payload_sha256']}")
if __name__=='__main__':main()
