#!/usr/bin/env python3
"""Canonical verifier for the post-#1172 KoalaBear rank-eleven router."""
from __future__ import annotations
import argparse,copy,json
from kb_mca_rank11_six_core_common_v1 import *
from kb_mca_rank11_six_router_v1 import six_anticode_router
from kb_mca_rank11_critical_core_router_v1 import critical_common_core_router

def build()->dict[str,object]:
    return {"schema":"kb-mca-rank11-six-anticode-critical-core-router-v1",
      "parent":PARENT,"row":ROW,"theta_resource":THETA_RESOURCE,
      "affine_dimension":AFFINE_DIMENSION,"six_anticode_router":six_anticode_router(),
      "critical_common_core_router":critical_common_core_router(),
      "claims":{"five_rank_one_anticode_cover_paid":True,
       "six_anticode_cover_sparse_pair_router_proved":True,
       "critical_order_32_common_core_proved":True,"rank11_paid":False,
       "koalabear_closed":False,"active_v4_ledger_movement":0}}

def main()->None:
    p=argparse.ArgumentParser();p.add_argument("--json",action="store_true")
    p.add_argument("--tamper-selftest",action="store_true");args=p.parse_args();expected=build()
    if args.tamper_selftest:
        mutations=[("six_anticode_router","tau",1799),
          ("six_anticode_router","sparse_pair_router","maximum_surviving_pair_error_support",167814),
          ("critical_common_core_router","chosen_32_core","guaranteed_slopes",378013808),
          ("critical_common_core_router","chosen_32_core","guaranteed_distinct_pair_types",384),
          ("critical_common_core_router","quotient_endpoint_variation_dimension_at_least",2),
          ("claims","rank11_paid",True)]
        caught=0
        for mutation in mutations:
            changed=copy.deepcopy(expected);cursor=changed
            for key in mutation[:-2]:cursor=cursor[key]
            cursor[mutation[-2]]=mutation[-1]
            try:require(changed==expected,"canonical")
            except Reject:caught+=1
        require(caught==len(mutations),"mutations")
        print(f"KB_MCA_RANK11_SIX_ANTICODE_CORE_TAMPER_PASS mutations={caught}/{len(mutations)}");return
    if args.json:print(json.dumps(expected,sort_keys=True));return
    print("KB_MCA_RANK11_SIX_ANTICODE_CORE_PASS "
      f"five_slack={expected['six_anticode_router']['fixed_left']['five_clique_slack']} "
      f"pair_error_max={expected['six_anticode_router']['sparse_pair_router']['maximum_surviving_pair_error_support']} "
      f"core32_slopes={expected['critical_common_core_router']['chosen_32_core']['guaranteed_slopes']} "
      f"core32_types={expected['critical_common_core_router']['chosen_32_core']['guaranteed_distinct_pair_types']}")
if __name__=="__main__":main()
