"""Exact five/six rank-one-anticode router."""
from __future__ import annotations
from fractions import Fraction
from math import comb
from kb_mca_rank11_six_core_common_v1 import *

def six_anticode_router()->dict[str,object]:
    tau=1798
    n,K,m,w,budget,near=(ROW[k] for k in ("n","K","m","w","budget","near"))
    A=m-tau;d=w-tau;qmax=n-A;high=THETA_RESOURCE//(tau+1);required=low_required(tau)
    full_cap=-1;maximizers=[]
    for q in range(qmax+1):
        value=fixed_left_cap_at_q(q,tau)
        if value>full_cap:full_cap=value;maximizers=[q]
        elif value==full_cap:maximizers.append(q)
    require(maximizers==[95326],"unique fixed-left q maximizer")
    q_peak=maximizers[0];pair_count_at_peak=list_count_for_outside(q_peak,tau)
    five_total=near+high+5*full_cap;six_total=near+high+6*full_cap
    require(five_total<budget<six_total,"five paid and six not scalar-paid")
    require(5*full_cap+FIXED_RIGHT_RAY_CAP<required,"mixed cover paid")
    per_clique_floor=required-5*full_cap
    q_high=max(q for q in range(q_peak,qmax+1)
               if fixed_left_cap_at_q(q,tau)>=per_clique_floor)
    require(fixed_left_cap_at_q(q_high+1,tau)<per_clique_floor,"adjacent boundary")
    g_low=n-q_high;triple=3*g_low-2*n
    require(triple>K,"triple coherence")

    qI=(2*K+11)//11;high_min=qI+1
    require(qI==190651 and q_peak==K//11+1,"shape thresholds")
    G=[numerator_sequence(q) for q in range(qmax+1)]
    for q in range(1,qI+1):require(G[q+1]-2*G[q]+G[q-1]<=0,"concavity")
    for q in range(high_min,qmax):
        require(G[q+1]-2*G[q]+G[q-1]>=0,"convexity")
        require(G[q+1]<G[q],"high decrease")

    e0=167814;S=5*e0;D=comb(d+AFFINE_DIMENSION,AFFINE_DIMENSION)
    def lowmax(count:int,need:int):
        need=max(0,need)
        if count==0:return (0,[]) if need==0 else None
        if need>count*qI:return None
        if need<=count*q_peak:return count*G[q_peak],[q_peak]*count
        a,r=divmod(need,count);vals=[a]*(count-r)+[a+1]*r
        return sum(G[q] for q in vals),vals
    cases=[]
    for h in range(7):
        l=6-h;best=None;config=None
        if h==0:
            best,lows=lowmax(l,S);config={"upper_endpoint_entries":0,
              "residual_high_entry":None,"lower_high_endpoint_entries":0,"low_values":lows}
        else:
            for up in range(h):
                lower=h-up-1;baseT=up*qmax+lower*high_min
                baseV=up*G[qmax]+lower*G[high_min]
                for residual in range(high_min,qmax+1):
                    low=lowmax(l,S-baseT-residual)
                    if low is None:continue
                    lv,lows=low;value=baseV+G[residual]+lv
                    if best is None or value>best:
                        best=value;config={"upper_endpoint_entries":up,
                          "residual_high_entry":residual,
                          "lower_high_endpoint_entries":lower,"low_values":lows}
        require(best is not None and config is not None,f"case {h}")
        bound=Fraction(best,D)+6;gap=Fraction(required)-bound
        require(gap>0,f"support case {h}")
        cases.append({"high_entries":h,"configuration":config,
          "bound_numerator":bound.numerator,"bound_denominator":bound.denominator,
          "signed_gap_numerator":gap.numerator,"signed_gap_denominator":gap.denominator})
    worst=max(cases,key=lambda x:Fraction(x["bound_numerator"],x["bound_denominator"]))
    require(worst["high_entries"]==0 and worst["configuration"]["low_values"]==[139845]*6,
            "worst support case")
    require(worst["signed_gap_numerator"]==5039866042250644297697303907940552741600048679872,
            "gap numerator")
    require(worst["signed_gap_denominator"]==7575576854420300947226509036769468677,
            "gap denominator")
    emax=e0-1;prefix=96150
    return {"tau":tau,"A":A,"d":d,"qmax":qmax,"high_tail":high,
      "low_required_for_overbudget":required,
      "fixed_left":{"unique_q_maximizer":q_peak,"common_endpoint_g_at_max":n-q_peak,
       "pair_list_at_max":pair_count_at_peak,"low_slope_cap":full_cap,
       "five_clique_total_with_high_and_near":five_total,"five_clique_slack":budget-five_total,
       "six_clique_total_with_high_and_near":six_total,"six_clique_overage":six_total-budget,
       "fixed_right_ray_cap":FIXED_RIGHT_RAY_CAP,
       "mixed_five_left_one_right_low_cap":5*full_cap+FIXED_RIGHT_RAY_CAP},
      "six_clique_coherence":{"minimum_capacity_per_clique":per_clique_floor,
       "largest_legal_outside_q":q_high,"minimum_common_endpoint_g":g_low,
       "triple_intersection_floor":triple,"K":K},
      "sparse_pair_router":{"first_excluded_error_support":e0,
       "maximum_surviving_pair_error_support":emax,"imported_paid_direction_support_through":prefix,
       "surviving_direction_support_window":[prefix+1,emax],"q_peak":q_peak,
       "q_concavity_end":qI,"high_interval_minimum":high_min,
       "critical_total_outside_load":S,"support_exclusion_cases":cases,
       "worst_support_case":worst}}
