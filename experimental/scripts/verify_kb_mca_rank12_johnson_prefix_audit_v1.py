#!/usr/bin/env python3
from fractions import Fraction
from math import comb, prod
import json

N=1_052_933
H=67_701
LAM=4_356
ACTIVE=(3104,3105,4356)
Y=(
 Fraction(783407435505036310,1777114341209059),
 Fraction(894939334590448235317,3356227749370360),
 Fraction(16360924804832711925677,27945375053210112),
)
EXPECTED_BOUND=54_568_751
R=1_048_576
D=67_472
K=4_357
S=11
T=4_128
FIXED=981_105

def ff(x,k): return prod(x-j for j in range(k))

def q(i,r):
    j=H-r
    return Fraction(sum(
        (-1)**t*comb(i,t)*ff(j,t)**2*ff(r,i-t)*ff(N-2*H+r,i-t)
        for t in range(i+1)
    ),ff(H,i)*ff(N-H,i))

def falling(x,k): return prod(x-j for j in range(k))
def rising(x,k): return prod(x+j for j in range(k))

def resource():
    return max(
        falling(R+K,S+1)//((D+K)*rising(D+1,S-1)),
        falling(R+S,S+1)//rising(D+1,S),
    )

def build():
    assert all(y>0 for y in Y)
    minimum=None
    minimizers=[]
    for r in range(LAM+1):
        value=-sum(Y[i-1]*q(i,r) for i in range(1,4))
        assert value>=1
        if minimum is None or value<minimum:
            minimum=value; minimizers=[r]
        elif value==minimum:
            minimizers.append(r)
    assert minimum==1 and tuple(minimizers)==ACTIVE
    objective=1+sum(Y)
    assert objective.numerator//objective.denominator==EXPECTED_BOUND
    old_prefix=comb(R+S,S)//comb(D-T+S,S)
    high=resource()//(T+1)
    low=EXPECTED_BOUND*FIXED
    total=low+high
    assert old_prefix==25_551_333_830_332
    assert high==3_240_390_795_118_310
    assert low==53_536_228_373_355
    assert total==3_293_927_023_491_665
    return {
      'schema':'kb-mca-rank12-johnson-prefix-audit-v1',
      'parent':'d01c546f4dca70e256c18c142873821b3bb48ab5',
      'retracted_exploratory_head':'74baa3a7a3661120ee760efd8e20f845077e67e8',
      'cell':{'n':N,'h':H,'lambda':LAM,'ambient_K':K,'deficiency_cutoff':T},
      'dual':{'active_intersections':list(ACTIVE),'coefficients':[[x.numerator,x.denominator] for x in Y],'objective':[objective.numerator,objective.denominator],'integer_floor':EXPECTED_BOUND,'constraints_checked':LAM+1},
      'application':{'old_pair_list_prefix':old_prefix,'johnson_prefix':EXPECTED_BOUND,'fixed_pair_multiplicity':FIXED,'low_slope_cap':low,'high_slope_cap':high,'one_threshold_total':total},
      'claims':{'degree_three_prefix_proved':True,'rank12_paid':False,'rank13_paid':False,'active_v4_ledger_movement':0,'koalabear_closed':False},
    }

if __name__=='__main__':
    print('KB_MCA_RANK12_JOHNSON_PREFIX_AUDIT_PASS',json.dumps(build(),sort_keys=True,separators=(',',':')))
