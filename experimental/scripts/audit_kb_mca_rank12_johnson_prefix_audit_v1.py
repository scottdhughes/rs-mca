#!/usr/bin/env python3
from fractions import Fraction
from math import comb
from verify_kb_mca_rank12_johnson_prefix_audit_v1 import N,H,LAM,ACTIVE,Y,EXPECTED_BOUND

def falling(x,k):
    z=1
    for a in range(k): z*=x-a
    return z

def kernel(i,r):
    numerator=0
    for t in range(i+1):
        a=falling(H-r,t)
        numerator += (-1)**t*comb(i,t)*a*a*falling(r,i-t)*falling(N-2*H+r,i-t)
    return Fraction(numerator,falling(H,i)*falling(N-H,i))

minimum=None
where=[]
for r in range(LAM+1):
    value=-(Y[0]*kernel(1,r)+Y[1]*kernel(2,r)+Y[2]*kernel(3,r))
    if value<1: raise AssertionError((r,value))
    if minimum is None or value<minimum:
        minimum=value; where=[r]
    elif value==minimum:
        where.append(r)
assert minimum==1 and tuple(where)==ACTIVE
objective=1+sum(Y)
assert objective.numerator//objective.denominator==EXPECTED_BOUND
print('KB_MCA_RANK12_JOHNSON_PREFIX_AUDIT_INDEPENDENT_PASS',EXPECTED_BOUND,where)
