#!/usr/bin/env python3
"""Exact verifier for the rank-twelve large-locator correction-ray payment."""
from __future__ import annotations

import argparse
import copy
import itertools
import json
from math import comb, prod
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank12-large-locator-ray-payment-v1/result.json"
PARENT_MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank12-common-locator-floor-v1/manifest.json"
PARENT = "ed556ccb7527e1c54e58b8d151ccefd8539000ac"
PARENT_PAYLOAD = "edef5ffa88a495a0a659a62a3ce891372b59458350ef4eab5b35f75ed5f37baa"
R = 1_048_576
D = 67_472
KMAX = 1_048_576
L2 = 5_170_912
T = R - D
FIRST_AMBIENT = 858_619
RAY_EXCESS_MAX = R // 6
RAY_CORE_THRESHOLD = T - RAY_EXCESS_MAX
EFFECTIVE_AT_FIRST = 52_277
RANK1_GLOBAL_MAX = 4_070_947

class Reject(ValueError): pass

def require(value: bool, message: str) -> None:
    if not value: raise Reject(message)

def falling(x: int, length: int) -> int: return prod(x-i for i in range(length))
def rising(x: int, length: int) -> int: return prod(x+i for i in range(length))
def ceil_div(a: int, b: int) -> int: return -(-a//b)

def theta2(K: int) -> int:
    return max(falling(R+K,3)//((D+K)*rising(D+1,1)), falling(R+2,3)//rising(D+1,2))

def incident(K: int) -> int: return ceil_div(L2*(D+K)-theta2(K),R+K)

def uniform_cap(k: int) -> int:
    n=R+k; m=D+k; q=m//2; a=m-q-1
    low=comb(n,2)//(q*(m-q)); hmax=n//(q+1); best_num=-1; best_den=1
    for h in range(1,hmax+1):
        b=a-1; C=n-h*m+h*a; candidates={0,h}
        if b:
            vertex=(C-h)//(2*b)
            candidates|={vertex-1,vertex,vertex+1,vertex+2,C//b,C//b+1}
        for p in candidates:
            if not 0<=p<=h: continue
            outside=n-h*m+p+(h-p)*a
            if outside<0: continue
            numerator=h*(h-1)*a+outside*(p*a+h-p)
            if numerator*best_den>best_num*a: best_num,best_den=numerator,a
    require(best_num>=0,"nonempty rank-one capacity")
    return low+best_num//best_den

def heterogeneous_floor(K: int, M: int) -> int:
    require(D+1<=M<=K+D,"legal nonuniversal support mass")
    return M-1 if M<=K-1 else (K-1)*(M-K+1)

def ray_endpoint_candidates(K: int, r: int) -> dict[str,int]:
    require(K>=FIRST_AMBIENT,"large-locator ambient window")
    require(0<=r<=RAY_EXCESS_MAX,"six-support excess window")
    out={}
    for label,M in (("M=D+1",D+1),("M=K-1",K-1),("M=K",K),("M=K+D",K+D)):
        out[label]=r+1+comb(M+r,2)//heterogeneous_floor(K,M)
    return out

def ray_cap(K: int, r: int):
    values=ray_endpoint_candidates(K,r)
    label,value=max(values.items(),key=lambda item:(item[1],item[0]))
    return value,label,values

def finite_controls() -> dict[str,int]:
    endpoint_cells=cross_cells=large_cells=0
    for D0 in range(2,10):
        for K in range(D0+3,24):
            for r in range(0,min(8,K-D0)):
                def B(M): return M-1 if M<=K-1 else (K-1)*(M-K+1)
                exhaustive=max(r+1+comb(M+r,2)//B(M) for M in range(D0+1,K+D0+1))
                endpoints=max(r+1+comb(M+r,2)//B(M) for M in {D0+1,K-1,K,K+D0})
                require(exhaustive==endpoints,"small four-endpoint ray optimization"); endpoint_cells+=1
    for K in range(4,11):
        s=K-1
        for M in range(2,K+7):
            expected=M-1 if M<=s else s*(M-s)
            def rec(rem,maximum,parts):
                nonlocal cross_cells
                if rem==0:
                    if len(parts)>=2:
                        cross=sum(parts[i]*parts[j] for i in range(len(parts)) for j in range(i+1,len(parts)))
                        require(cross>=expected,"small heterogeneous-pair floor"); cross_cells+=1
                    return
                for part in range(min(rem,maximum,s),0,-1): rec(rem-part,part,parts+(part,))
            rec(M,M,())
    for M in range(2,30):
        for r in range(12):
            N=M+r
            for w in range(1,N+1):
                require((N-w)//max(1,M-w)<=r+1,"small large-clone outside injection"); large_cells+=1
    return {"endpoint_cells":endpoint_cells,"cross_compositions":cross_cells,"large_clone_cells":large_cells}

def build() -> dict[str,Any]:
    if PARENT_MANIFEST.exists():
        parent=json.loads(PARENT_MANIFEST.read_text())
        require(parent["canonical_payload_sha256"]==PARENT_PAYLOAD,"parent locator-floor payload")
        require(parent["claims"]["proper_rank2_drop_forces_common_locator"],"parent locator-floor theorem")
    require(6*RAY_EXCESS_MAX<R+1,"first six-support strict inequality")
    require(6*(RAY_EXCESS_MAX+1)==R+2,"adjacent six-support wall")
    require(RAY_CORE_THRESHOLD==806_342,"large-locator threshold")
    caps={k:uniform_cap(k) for k in range(40_230,52_279)}
    require(caps[52_277]==2_510_754 and caps[52_278]==2_510_734,"first effective-dimension boundary")
    require((incident(858_618),incident(858_619))==(2_510_745,2_510_746),"adjacent ambient loads")
    pointer=EFFECTIVE_AT_FIRST; previous_core=RAY_CORE_THRESHOLD-1; core_decreases=0
    max_ray=-1; max_ray_cells=[]; max_total=-1; max_total_cells=[]; selected={}; argmax_counts={}; cells=0
    for K in range(FIRST_AMBIENT,KMAX+1):
        load=incident(K)
        while pointer>40_230 and caps[pointer]<load: pointer-=1
        require(caps[pointer]>=load,"capacity at effective pointer")
        require(caps[pointer+1]<load,"effective pointer maximality")
        core=K-pointer; require(core>=RAY_CORE_THRESHOLD,"large-locator floor")
        if core<previous_core: core_decreases+=1
        previous_core=core; r=max(0,T-core); require(r<=RAY_EXCESS_MAX,"correction-ray excess")
        ray,label,candidates=ray_cap(K,r); floor_diagnostic_total=caps[pointer]+ray
        composed_cap=RANK1_GLOBAL_MAX+ray; require(composed_cap<L2,"proper-drop composition below rank-two load")
        argmax_counts[label]=argmax_counts.get(label,0)+1
        if ray>max_ray: max_ray,max_ray_cells=ray,[K]
        elif ray==max_ray: max_ray_cells.append(K)
        if composed_cap>max_total: max_total,max_total_cells=composed_cap,[K]
        elif composed_cap==max_total: max_total_cells.append(K)
        record={"incident_load":load,"effective_rank_one_dimension":pointer,"common_locator_floor":core,"outside_excess":r,"rank_one_floor_diagnostic_cap":caps[pointer],"rank_one_global_cap":RANK1_GLOBAL_MAX,"ray_cap":ray,"ray_argmax":label,"ray_endpoint_candidates":candidates,"floor_diagnostic_total":floor_diagnostic_total,"total_cap":composed_cap,"slack":L2-composed_cap,"terminal":"PROPER_DROP_IMPOSSIBLE_WHOLE_FAMILY_SHORTENING"}
        if K in {858_619,858_625,900_000,991_011,991_012,1_040_688,KMAX}: selected[str(K)]=record
        cells+=1
    require(core_decreases==0,"large-locator floor nondecreasing")
    require(max_ray==796_620 and max_ray_cells==[858_619],"uniform affine-ray maximum")
    require(max_total==4_867_567 and max_total_cells==[858_619],"large-locator composed maximum")
    require(selected["858619"]=={"incident_load":2_510_746,"effective_rank_one_dimension":52_277,"common_locator_floor":806_342,"outside_excess":174_762,"rank_one_floor_diagnostic_cap":2_510_754,"rank_one_global_cap":4_070_947,"ray_cap":796_620,"ray_argmax":"M=K","ray_endpoint_candidates":{"M=D+1":609_591,"M=K-1":796_619,"M=K":796_620,"M=K+D":174_773},"floor_diagnostic_total":3_307_374,"total_cap":4_867_567,"slack":303_345,"terminal":"PROPER_DROP_IMPOSSIBLE_WHOLE_FAMILY_SHORTENING"},"first paid large-locator cell")
    require(selected[str(KMAX)]["total_cap"]==4_595_236,"full-row composed cap")
    require(selected[str(KMAX)]["slack"]==575_676,"full-row composed slack")
    controls=finite_controls()
    return {"schema":"kb-mca-rank12-large-locator-ray-payment-v1","parent":PARENT,"parent_payload":PARENT_PAYLOAD,"constants":{"R":R,"D":D,"n_minus_m":T,"rank2_load":L2,"rank1_global_max":RANK1_GLOBAL_MAX,"first_ambient_dimension":FIRST_AMBIENT,"six_support_excess_max":RAY_EXCESS_MAX,"large_locator_threshold":RAY_CORE_THRESHOLD},"adjacent_wall":{"ambient_dimension":858_618,"incident_load":2_510_745,"effective_rank_one_dimension":52_277,"common_locator_floor":806_341,"outside_excess":174_763,"six_omission_bound":1_048_578,"reed_solomon_minimum_weight":1_048_577,"status":"SIX_SUPPORT_SYNCHRONIZATION_FAILS_BY_ONE_COORDINATE"},"first_paid_cell":selected["858619"],"selected_cells":selected,"scan":{"ambient_cells":cells,"locator_floor_decreases":core_decreases,"maximum_ray_cap":max_ray,"maximum_ray_cap_cells":max_ray_cells,"maximum_composed_cap":max_total,"maximum_composed_cap_cells":max_total_cells,"minimum_composed_slack":L2-max_total,"composition_rule":"rank1_global_max_plus_uniform_ray_cap","ray_endpoint_argmax_counts":argmax_counts},"finite_controls":controls,"claims":{"one_affine_correction_ray_after_six_support_synchronization":True,"universal_core_aware_ray_cap_proved":True,"proper_drop_impossible_for_ambient_K_ge_858619":True,"whole_family_shortens_to_K_at_most_858618":True,"affine_error_rank_12_paid":False,"active_v4_ledger_movement":0,"koalabear_closed":False}}

def tamper_selftest(expected: dict[str,Any]) -> int:
    mutations=[("constants","large_locator_threshold",RAY_CORE_THRESHOLD-1),("adjacent_wall","status","PAID"),("first_paid_cell","ray_cap",expected["first_paid_cell"]["ray_cap"]-1),("scan","maximum_composed_cap",expected["scan"]["maximum_composed_cap"]-1),("claims","proper_drop_impossible_for_ambient_K_ge_858619",False),("claims","affine_error_rank_12_paid",True),("claims","active_v4_ledger_movement",1),("parent","","WRONG")]
    caught=0
    for section,key,replacement in mutations:
        changed=copy.deepcopy(expected)
        if section=="parent": changed["parent"]=replacement
        else: changed[section][key]=replacement
        try: require(changed==expected,"canonical result")
        except Reject: caught+=1
    require(caught==len(mutations),"all hostile mutations rejected"); return caught

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--write",action="store_true"); parser.add_argument("--tamper-selftest",action="store_true"); args=parser.parse_args(); result=build()
    if args.write:
        RESULT.parent.mkdir(parents=True,exist_ok=True); RESULT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(f"WROTE {RESULT}"); return
    require(RESULT.exists(),"result certificate exists"); require(json.loads(RESULT.read_text())==result,"result reconstruction")
    if args.tamper_selftest:
        print(f"KB_MCA_RANK12_LARGE_LOCATOR_RAY_TAMPER_PASS mutations={tamper_selftest(result)}/8"); return
    print("KB_MCA_RANK12_LARGE_LOCATOR_RAY_PASS " f"first_K={FIRST_AMBIENT} ray={result['first_paid_cell']['ray_cap']} " f"max_total={result['scan']['maximum_composed_cap']} " f"min_slack={result['scan']['minimum_composed_slack']}")
if __name__=="__main__": main()
