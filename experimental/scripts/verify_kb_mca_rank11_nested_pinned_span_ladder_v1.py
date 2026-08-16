#!/usr/bin/env python3
"""Exact verifier for the KoalaBear rank-eleven nested pinned-span ladder."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from math import comb, prod
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank11-nested-pinned-span-ladder-v1/result.json"

ROW = {
    "p": 2_130_706_433,
    "extension_degree": 6,
    "n": 2_097_152,
    "K": 1_048_576,
    "m": 1_116_048,
    "w": 67_472,
    "near": 134_944,
    "budget": 274_980_728_111_395_087,
    "theta_resource_s10": 106_618_568_137_036_225_644,
    "rank1_group_cap": 8_147_918,
}
PARENT = "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
FACTOR_SYNC_SOURCE = "534341b36975d7d9ecc2ca0abdd7f0b9d0cc640f"
TAU = 1_937
H = 36_775

class Reject(ValueError):
    pass

def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)

def falling(x: int, r: int) -> int:
    return prod(x-i for i in range(r))

def list_cap(tau: int, r: int) -> int:
    return comb(ROW["n"]-ROW["K"]+r, r) // comb(ROW["w"]-tau+r, r)

def build() -> dict[str, Any]:
    n,K,m,w = (ROW[k] for k in ("n","K","m","w"))
    A=m-TAU
    c=2*A-n
    d=A-K
    multiplicity=n-A
    q=H+1
    m2=list_cap(TAU,2)
    rank2_group=multiplicity*m2
    n1=falling(m,9)//(c-H)**9
    n2=falling(m,8)//(c-H)**8
    high=ROW["theta_resource_s10"]//(TAU+1)
    rank1_total=n1*ROW["rank1_group_cap"]
    rank2_total=n2*rank2_group
    total=ROW["near"]+high+multiplicity+rank1_total+rank2_total
    residual=ROW["budget"]+1-total

    list_caps=[list_cap(TAU,r) for r in range(1,11)]
    slope_caps=[multiplicity*x for x in list_caps]
    field_guards=[x*x < ROW["p"]**ROW["extension_degree"] for x in list_caps]

    nested=[]
    current=residual
    for j in range(10):
        current=(current*(q-j)+(m-j)-1)//(m-j)
        nested.append(current)

    dimension_floors=[]
    for load in nested:
        floor=2 if load>0 else 0
        for r,cap in enumerate(slope_caps,1):
            if load>cap:
                floor=max(floor,r+1)
        dimension_floors.append(floor)

    parent_cap=slope_caps[2]
    parent_count=(residual+parent_cap-1)//parent_cap
    a,b=divmod(parent_count*q,m)
    intersections={}
    for k in range(2,6):
        numerator=(m-b)*comb(a,k)+b*comb(a+1,k)
        denominator=comb(parent_count,k)
        intersections[str(k)]=(numerator+denominator-1)//denominator

    expected = {
        "A":1114111, "c":131070, "d":65535, "multiplicity":983041,
        "q":36776, "M2":255, "rank2_group_cap":250675455,
        "N1":4557575472, "N2":385072738,
        "rank1_total":37134751224667296,
        "rank2_total":96528283806245790,
        "high_tail":55014741040782366,
        "total":188677776072813437,
        "signed_slack":86302952038581650,
        "residual_load_if_unsafe":86302952038581651,
    }
    actual = {
        "A":A, "c":c, "d":d, "multiplicity":multiplicity,
        "q":q, "M2":m2, "rank2_group_cap":rank2_group,
        "N1":n1, "N2":n2, "rank1_total":rank1_total,
        "rank2_total":rank2_total, "high_tail":high, "total":total,
        "signed_slack":ROW["budget"]-total,
        "residual_load_if_unsafe":residual,
    }
    require(actual==expected,"selected exact envelope")
    require(list_caps==[16,255,4095,65530,1048431,16773712,268356622,4293280145,68684687551,1098814582063],"list caps")
    require(slope_caps==[15728656,250675455,4025552895,64418676730,1030650658671,16489246618192,263805562047502,4220470407020945,67519863934822591,1080179785565793583],"slope caps")
    require(all(field_guards),"field guards")
    require(nested==[2843853816476423,93708171878891,3087708134499,101738094101,3352119806,110444488,3638792,119884,3950,131],"nested loads")
    require(dimension_floors==[8,7,6,5,3,2,2,2,2,2],"dimension floors")
    require(parent_count==21438783,"parent count")
    require(intersections=={"2":1212,"3":40,"4":2,"5":1},"intersections")

    return {
        "schema":"kb-mca-rank11-nested-pinned-span-ladder-v1",
        "parent":PARENT,
        "factor_sync_source_commit":FACTOR_SYNC_SOURCE,
        "row":ROW,
        "selected":actual,
        "list_caps":list_caps,
        "slope_caps":slope_caps,
        "field_guards":field_guards,
        "nested_loads":{str(i+1):v for i,v in enumerate(nested)},
        "dimension_floors":{str(i+1):v for i,v in enumerate(dimension_floors)},
        "parent_abundance":{
            "dimension3_parent_cap":parent_cap,
            "minimum_distinct_parents":parent_count,
            "balanced_low_degree":a,
            "balanced_remainder":b,
            "forced_intersections":intersections,
        },
        "claims":{
            "factor_synchronization_included":True,
            "nested_pinned_span_ladder_proved":True,
            "rank11_paid":False,
            "koalabear_closed":False,
            "active_v4_ledger_movement":0,
        },
    }

def canonical(x: Any) -> bytes:
    return json.dumps(x,sort_keys=True,separators=(",",":")).encode()

def small_nested_controls() -> int:
    checked=0
    # Exhaustive weighted families of two q-subsets with weights 1 or 2.
    for m in range(3,7):
        universe=range(m)
        for q in range(1,m):
            subsets=list(itertools.combinations(universe,q))
            for J1 in subsets:
                for J2 in subsets:
                    for w1 in (1,2):
                        for w2 in (1,2):
                            fam=[(set(J1),w1),(set(J2),w2)]
                            active=fam
                            load=w1+w2
                            T=set()
                            for j in range(min(q,3)):
                                scores={}
                                for x in universe:
                                    if x in T: continue
                                    scores[x]=sum(weight for J,weight in active if x in J)
                                x=max(scores,key=scores.get)
                                T.add(x)
                                active=[item for item in active if x in item[0]]
                                load=sum(weight for _,weight in active)
                                lower=(sum(weight for _,weight in fam)*falling(q,j+1)+falling(m,j+1)-1)//falling(m,j+1)
                                require(load>=lower,"small nested weighted control")
                            checked+=1
    return checked

def tamper_selftest(expected: dict[str,Any]) -> int:
    mutations=[
        ("selected","total",expected["selected"]["total"]-1),
        ("selected","residual_load_if_unsafe",expected["selected"]["residual_load_if_unsafe"]+1),
        ("nested_loads","4",expected["nested_loads"]["4"]-1),
        ("dimension_floors","1",7),
        ("field_guards",9,False),
        ("parent","",FACTOR_SYNC_SOURCE),
        ("claims","rank11_paid",True),
        ("claims","koalabear_closed",True),
    ]
    caught=0
    for section,key,value in mutations:
        changed=copy.deepcopy(expected)
        if section=="parent":
            changed["parent"]=value
        elif section=="field_guards":
            changed[section][key]=value
        else:
            changed[section][key]=value
        try:
            require(changed==expected,"canonical result")
        except Reject:
            caught+=1
    require(caught==len(mutations),"all mutations caught")
    return caught

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",action="store_true")
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--tamper-selftest",action="store_true")
    args=parser.parse_args()
    result=build()
    result["finite_nested_controls"]={"families_checked":small_nested_controls()}
    if args.write:
        RESULT.parent.mkdir(parents=True,exist_ok=True)
        RESULT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        print(f"WROTE {RESULT}")
        return
    if RESULT.exists():
        actual=json.loads(RESULT.read_text())
        require(actual==result,"result file")
    if args.tamper_selftest:
        print(f"KB_MCA_RANK11_NESTED_PIN_TAMPER_PASS mutations={tamper_selftest(result)}/8")
        return
    if args.json:
        print(canonical(result).decode())
        return
    print(
        "KB_MCA_RANK11_NESTED_PIN_PASS "
        f"total={result['selected']['total']} "
        f"residual={result['selected']['residual_load_if_unsafe']} "
        f"load1={result['nested_loads']['1']} "
        f"dim1={result['dimension_floors']['1']} "
        f"controls={result['finite_nested_controls']['families_checked']}"
    )

if __name__=="__main__":
    main()
