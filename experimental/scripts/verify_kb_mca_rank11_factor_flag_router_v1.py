#!/usr/bin/env python3
"""Exact verifier for the KoalaBear rank-eleven factor-flag router."""
from __future__ import annotations
import argparse, copy, hashlib, json
from fractions import Fraction
from itertools import product
from math import comb, prod
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]
CERT=ROOT/"experimental/data/certificates/kb-mca-rank11-factor-flag-router-v1"
RESULT_PATH=CERT/"result.json"
MANIFEST_PATH=CERT/"manifest.json"
PARENT="193b7bf99a5cc7ccea042f25677e698d9f988eee"
ROW={"p":2130706433,"extension_degree":6,"n":2097152,"K":1048576,
     "m":1116048,"w":67472,"near":134944,"budget":274980728111395087}
C10_EXPECTED=106618568137036225644
CENTER_TAU=1795
TAU=1936
Z2=117731
Z3=23354

class Reject(ValueError): pass
def require(v:bool,msg:str)->None:
    if not v: raise Reject(msg)
def falling(x:int,r:int)->int: return prod(x-i for i in range(r))
def rising(x:int,r:int)->int: return prod(x+i for i in range(r))
def ceil_div(a:int,b:int)->int: return -(-a//b)

def theta_resource(s:int)->int:
    n,K,m,w=(ROW[k] for k in ("n","K","m","w"))
    vals=[Fraction(n)]
    for r in range(1,s+1):
        vals += [Fraction(falling(n,r+1),m*rising(w+1,r-1)),
                 Fraction(falling(n-K+r,r+1),rising(w+1,r))]
    v=max(vals)
    return v.numerator//v.denominator

def pair_cap(r:int,tau:int)->int:
    n,K,m=(ROW[k] for k in ("n","K","m"))
    A=m-tau
    require(0<=r<=10 and A>K,"pair-cap range")
    return comb(n-K+r,r)//comb(A-K+r,r)

def center_replay()->dict[str,int]:
    E=ROW["budget"]-ROW["near"]+1
    q=pair_cap(10,CENTER_TAU)
    mass=max(0,(CENTER_TAU+1)*E-theta_resource(10))
    weight=ceil_div(mass,q)
    records=ceil_div(weight,CENTER_TAU)
    def capacity(delta:int)->int:
        return ((ROW["n"]-ROW["m"]+delta)//delta)*(CENTER_TAU+1-delta)
    max_delta=max(d for d in range(1,CENTER_TAU+1) if capacity(d)>=weight)
    return {"cutoff":CENTER_TAU,"pair_cap":q,"forced_weight":weight,
            "forced_records":records,"max_core_deficiency":max_delta,
            "capacity_delta4":capacity(4),"capacity_delta5":capacity(5)}

def profile(s:int,z3:int=Z3,z2:int=Z2)->dict[str,int]:
    n,K,m=(ROW[k] for k in ("n","K","m"))
    H0=m-4; A=m-TAU; h=H0+A-n; owner=n-A
    q1=pair_cap(1,TAU); q2=pair_cap(2,TAU)
    if s<=2:
        N1,N2=0,1
        low=q2*owner+owner
    else:
        c12=h-z2+1; c13=h-z3+1; c23=z2-z3+1
        require(min(c12,c13,c23)>0,"positive flag denominators")
        N1=falling(H0,s-1)//(c12*c13**(s-2))
        N2=falling(H0,s-2)//(c23**(s-2))
        low=(N1*q1+N2*q2)*owner+owner
    return {"s":s,"N1":N1,"N2":N2,"low":low}

def best_z2(z3:int)->dict[str,int]:
    h=(ROW["m"]-4)+(ROW["m"]-TAU)-ROW["n"]
    best=None
    for z2 in range(z3,h+1):
        item=profile(10,z3,z2)
        key=(item["low"],z2)
        if best is None or key<(best["low"],best["z2"]):
            best={"z2":z2,**item}
    assert best is not None
    return best

def build()->dict[str,Any]:
    c10=theta_resource(10)
    require(c10==C10_EXPECTED,"theta resource")
    center=center_replay()
    require(center=={"cutoff":1795,"pair_cap":1075288922022,
      "forced_weight":360132809,"forced_records":200632,
      "max_core_deficiency":4,"capacity_delta4":439536384,
      "capacity_delta5":351431811},"dense center replay")
    table=[profile(s) for s in range(1,11)]
    expected_lows=[251658240,251658240,13714391040,146454282240,
      1550397603840,16464466083840,175651195453440,
      1883268839178240,20297059763159040,219935524214538240]
    require([x["low"] for x in table]==expected_lows,"dimension table")
    chosen=best_z2(Z3)
    adjacent=best_z2(Z3+1)
    require((chosen["z2"],chosen["low"],chosen["N1"],chosen["N2"])==
      (117731,219935524214538240,8415196932,382360905),"chosen optimum")
    require((adjacent["z2"],adjacent["low"])==
      (117731,219952702956503040),"adjacent optimum")
    high=c10//(TAU+1)
    total=ROW["near"]+high+chosen["low"]
    adjacent_total=ROW["near"]+high+adjacent["low"]
    require((high,total,ROW["budget"]-total)==
      (55043143075392992,274978667290066176,2060821328911),"row total")
    require(adjacent_total-ROW["budget"]==15117920635889,"adjacent excess")
    q1,q2=pair_cap(1,TAU),pair_cap(2,TAU)
    require((q1,q2)==(15,255),"container pair caps")
    require(q2*q2<ROW["p"]**ROW["extension_degree"],"line-field guard")
    return {"schema":"kb-mca-rank11-factor-flag-router-v1","parent":PARENT,
      "row":ROW,"theta_resource":c10,"center":center,"cutoff":TAU,
      "center_subset":ROW["m"]-4,"low_pair_core_floor":ROW["m"]-TAU,
      "center_intersection":(ROW["m"]-4)+(ROW["m"]-TAU)-ROW["n"],
      "Z2":Z2,"Z3":Z3,"Q1":q1,"Q2":q2,
      "fixed_pair_slope_cap":ROW["n"]-(ROW["m"]-TAU),
      "dimension_table":table,"chosen":chosen,"high_tail":high,
      "total":total,"slack":ROW["budget"]-total,
      "adjacent":{"Z3":Z3+1,**adjacent,"total":adjacent_total,
                  "over_budget":adjacent_total-ROW["budget"]},
      "claims":{"rank_three_factor_subcode_forced":True,
                "active_v4_ledger_movement":0,"rank11_paid":False,
                "koalabear_closed":False}}

def canonical(x:Any)->bytes:
    return json.dumps(x,sort_keys=True,separators=(",",":")).encode()
def result_sha(x:dict[str,Any])->str: return hashlib.sha256(canonical(x)).hexdigest()
def verify_manifest()->None:
    manifest=json.loads(MANIFEST_PATH.read_text())
    require(manifest["parent"]==PARENT,"manifest parent")
    actual=json.loads(RESULT_PATH.read_text())
    require(manifest["result_sha256"]==result_sha(actual),"result hash")
    for item in manifest["files"]:
        data=(ROOT/item["path"]).read_bytes()
        require(len(data)==item["bytes"],f"size {item['path']}")
        require(hashlib.sha256(data).hexdigest()==item["sha256"],f"hash {item['path']}")

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--write",action="store_true")
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--tamper-selftest",action="store_true")
    ap.add_argument("--skip-manifest",action="store_true")
    args=ap.parse_args()
    expected=build()
    if args.write:
        CERT.mkdir(parents=True,exist_ok=True)
        RESULT_PATH.write_text(json.dumps(expected,indent=2,sort_keys=True)+"\n")
        print(f"WROTE {RESULT_PATH}")
        return
    actual=json.loads(RESULT_PATH.read_text())
    require(actual==expected,"canonical result")
    if not args.skip_manifest: verify_manifest()
    if args.tamper_selftest:
        mutations=[("Z3",23355),("total",expected["total"]-1),
                   ("slack",expected["slack"]+1)]
        caught=0
        for key,val in mutations:
            x=copy.deepcopy(actual); x[key]=val
            try: require(x==expected,"tamper")
            except Reject: caught+=1
        for key in ("rank11_paid","koalabear_closed","active_v4_ledger_movement"):
            x=copy.deepcopy(actual)
            x["claims"][key]=True if key!="active_v4_ledger_movement" else 1
            try: require(x==expected,"claim tamper")
            except Reject: caught+=1
        require(caught==6,"tamper count")
        print("KB_MCA_RANK11_FACTOR_FLAG_TAMPER_PASS mutations=6/6")
        return
    if args.json: print(json.dumps(actual,sort_keys=True))
    else: print("KB_MCA_RANK11_FACTOR_FLAG_PASS "
      f"Z3={actual['Z3']} total={actual['total']} slack={actual['slack']} "
      f"result_sha256={result_sha(actual)}")
if __name__=="__main__": main()
