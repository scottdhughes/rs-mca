"""Exact order-32 minimizing-pair common-core router."""
from __future__ import annotations
from fractions import Fraction
from math import comb
from kb_mca_rank11_six_core_common_v1 import *

def stats(c:int,tau:int)->dict[str,object]:
    A=ROW["m"]-tau;required=low_required(tau)
    avg=Fraction(required*comb(A,c),comb(ROW["n"],c));slopes=ceil_fraction(avg)
    owner=pair_owner_cap(tau);types=(slopes+owner-1)//owner;q2=pair_list_cap(2,tau)
    return {"tau":tau,"core_size":c,"A":A,"d":ROW["w"]-tau,
      "high_tail":THETA_RESOURCE//(tau+1),"low_required_for_overbudget":required,
      "average_numerator":avg.numerator,"average_denominator":avg.denominator,
      "guaranteed_slopes":slopes,"one_pair_owner_cap":owner,
      "guaranteed_distinct_pair_types":types,"rank_two_pair_list_cap":q2,
      "pair_type_excess_over_rank_two_cap":types-q2,
      "field_guard":q2*q2<ROW["p"]**ROW["extension_degree"]}

def critical_common_core_router()->dict[str,object]:
    bestT=bestG=best33=None;forcing=0
    for tau in range(1,ROW["w"]):
        a=stats(32,tau);T=(int(a["guaranteed_distinct_pair_types"]),-tau,a)
        G=(int(a["pair_type_excess_over_rank_two_cap"]),-tau,a)
        if bestT is None or T[:2]>bestT[:2]:bestT=T
        if bestG is None or G[:2]>bestG[:2]:bestG=G
        if G[0]>0:forcing+=1
        b=stats(33,tau);W=(int(b["pair_type_excess_over_rank_two_cap"]),
          int(b["guaranteed_distinct_pair_types"]),int(b["guaranteed_slopes"]),-tau,b)
        if best33 is None or W[:4]>best33[:4]:best33=W
    chosen=bestT[2]
    require(chosen["tau"]==3304 and chosen["guaranteed_slopes"]==378013809,"core32")
    require(chosen["guaranteed_distinct_pair_types"]==385 and
            chosen["rank_two_pair_list_cap"]==267,"types/cap")
    require(chosen["pair_type_excess_over_rank_two_cap"]==118 and chosen["field_guard"],"gap")
    require(forcing==9675,"forcing count")
    wall=best33[4]
    require(best33[0]==-59 and wall["tau"]==2815,"core33 wall")
    require(wall["guaranteed_distinct_pair_types"]==203 and
            wall["rank_two_pair_list_cap"]==262,"core33 values")
    return {"chosen_32_core":chosen,"quotient_endpoint_variation_dimension_at_least":3,
      "number_of_cutoffs_forcing_dimension_three":forcing,
      "maximum_gap_32":bestG[2],"complete_33_core_method_wall":wall}
