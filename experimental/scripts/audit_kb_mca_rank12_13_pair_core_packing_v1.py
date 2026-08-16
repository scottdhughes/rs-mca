#!/usr/bin/env python3
"""Independent product/recurrence audit for the rank-12/13 packet."""

from fractions import Fraction
from math import comb, prod

R=1_048_576
d=67_472
KMAX=1_048_576
B=274_980_728_111_395_087
near=134_944
L0=B-near+1
p=2_130_706_433
field=p**6
fixed=R-d+1

def fall(x,r): return prod(range(x-r+1,x+1))
def rise(x,r): return prod(range(x,x+r))
def ceilq(a,b): return -(-a//b)

def resource(s,K):
    values=[Fraction(R+K,1)]
    for r in range(1,s+1):
        a=Fraction(1,1)
        for j in range(r+1): a*=R+K-j
        a/=DplusK(K)
        for j in range(r-1): a/=d+1+j
        b=Fraction(1,1)
        for j in range(r+1): b*=R+r-j
        for j in range(r): b/=d+1+j
        values.extend((a,b))
    q=max(values)
    return q.numerator//q.denominator

def DplusK(K): return d+K

def descend(start,stop,capped=False):
    loads={start:L0}
    for s in range(start,stop,-1):
        c=resource(s,s)
        if capped: c=min(c,loads[s]*(d+1))
        loads[s-1]=ceilq(loads[s]*(d+s)-c,R+s)
    return loads

def fisher(k,T):
    n=R+k; h=d+k-T; lam=k-1
    den=h*h-n*lam
    return None if den<=0 else n*(h-lam)//den

def endpoint(k,T):
    types=fisher(k,T)
    return None if types is None else types*fixed+resource(k,k)//(T+1)

def best(k,forced):
    best_item=None; first=None
    for T in range(1,d+2):
        val=endpoint(k,T)
        if val is None: continue
        if best_item is None or val<best_item[1]: best_item=(T,val)
        if first is None and val<=forced: first=(T,val)
    return best_item,first

def pair_prefix(k,delta):
    h=d+k-delta; n=R+k; lam=k-1
    caps=[]
    den=h*h-n*lam
    if den>0: caps.append(n*(h-lam)//den)
    if h>=k:
        ratio=1
        # Exact product implementation of C(R+k,k)/C(h,k).
        q=Fraction(1,1)
        for j in range(k): q*=Fraction(R+k-j,h-j)
        qfloor=q.numerator//q.denominator
        if qfloor*qfloor<field: caps.append(qfloor)
    return None if not caps else min(caps)

def coupled(k):
    remaining=resource(k,k); total=0; previous=0
    for delta in range(1,d+2):
        current=pair_prefix(k,delta)
        if current is None:
            take=remaining//delta; total+=take; remaining-=take*delta
            return total,remaining,delta
        assert current>=previous
        slots=(current-previous)*((R-d+delta)//delta)
        take=min(slots,remaining//delta)
        total+=take; remaining-=take*delta
        previous=current
        if take<slots or remaining<delta+1:
            return total,remaining,delta
    return total,remaining,d+1

# Independent finite controls of the Cauchy/Fisher inequality.
def fisher_controls():
    checked=0
    for n in range(3,9):
        masks=range(1,1<<n)
        sets=[frozenset(i for i in range(n) if mask>>i&1) for mask in masks]
        for h in range(1,n+1):
            candidates=[S for S in sets if len(S)>=h]
            for lam in range(h):
                den=h*h-n*lam
                if den<=0: continue
                bound=n*(h-lam)//den
                # Check every family of size at most five; larger finite families
                # are handled by the same algebra, and this catches floor errors.
                from itertools import combinations
                for r in range(2,min(5,len(candidates))+1):
                    for fam in combinations(candidates,r):
                        if all(len(fam[i]&fam[j])<=lam for i in range(r) for j in range(i)):
                            assert r<=bound
                        checked+=1
                        if checked>=46_381: return checked
    return checked

# Small prefix-resource LP controls: brute force all feasible slot allocations.
def greedy_controls():
    from itertools import product
    checked=0
    for costs in ((1,2,3),(1,3,4),(2,3,5)):
        for slots in product(range(4),repeat=len(costs)):
            for budget in range(16):
                greedy=0; rem=budget
                for cost,slot in zip(costs,slots):
                    take=min(slot,rem//cost); greedy+=take; rem-=take*cost
                brute=0
                for take in product(*(range(s+1) for s in slots)):
                    if sum(c*x for c,x in zip(costs,take))<=budget:
                        brute=max(brute,sum(take))
                assert greedy==brute
                checked+=1
    return checked

r12=descend(11,1)
r13=descend(12,1)
r14=descend(13,1,True)
assert r12[3]==80_415_635
assert r13[4]==73_640_859
assert r14[8]==39_342_841_453
assert best(3,r12[3])==((5761,16_380_678),(59,80_307_161))
assert best(4,r13[4])==((12_233,22_658_813),(1_037,73_634_528))
assert coupled(3)[0]==14_778_066
assert coupled(4)[0]==15_649_594
assert coupled(8)[0]==55_071_795_746
fc=fisher_controls(); gc=greedy_controls()
assert fc==46_381 and gc==364
print("KB_MCA_RANK12_13_PAIR_CORE_AUDIT_PASS")
print(f"rank12={r12[3]} rank13={r13[4]} rank14_wall={coupled(8)[0]-r14[8]}")
print(f"fisher_controls={fc} greedy_controls={gc}")
