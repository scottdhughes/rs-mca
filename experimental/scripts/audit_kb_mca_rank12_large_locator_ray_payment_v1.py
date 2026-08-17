#!/usr/bin/env python3
"""Independent exact audit for the rank-12 large-locator ray payment."""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank12-large-locator-ray-payment-v1/result.json"
R=1_048_576; D=67_472; T=981_104; L2=5_170_912
K0=858_619; KMAX=1_048_576; RANK1_GLOBAL=4_070_947


def fall(x,r): return prod(range(x-r+1,x+1))
def rise(x,r): return prod(range(x,x+r))
def ceilq(a,b): return (a+b-1)//b


def resource2(K):
    return max(fall(R+K,3)//((D+K)*(D+1)), fall(R+2,3)//((D+1)*(D+2)))


def load(K): return ceilq(L2*(D+K)-resource2(K),R+K)


def direct_rank1_cap(k):
    n=R+k; m=D+k; q=m//2; a=m-q-1
    low=comb(n,2)//(q*(m-q))
    best=Fraction(-1,1)
    for h in range(1,n//(q+1)+1):
        for p in range(h+1):
            outside=n-h*m+p+(h-p)*a
            if outside<0: continue
            value=Fraction(h*(h-1),1)+outside*(Fraction(p,1)+Fraction(h-p,a))
            best=max(best,value)
    assert best>=0
    return low+best.numerator//best.denominator


def B(K,M):
    return M-1 if M<=K-1 else (K-1)*(M-K+1)


def ray(K,r):
    choices={
        "M=D+1":D+1,
        "M=K-1":K-1,
        "M=K":K,
        "M=K+D":K+D,
    }
    values={name:r+1+comb(M+r,2)//B(K,M) for name,M in choices.items()}
    return max(values.values()),values


def main():
    result=json.loads(RESULT.read_text())
    caps={k:direct_rank1_cap(k) for k in range(40_230,52_279)}
    ptr=52_277
    maximum=(-1,[])
    maximum_ray=(-1,[])
    selected={}
    count=0
    for K in range(K0,KMAX+1):
        inc=load(K)
        while caps[ptr]<inc: ptr-=1
        assert caps[ptr]>=inc>caps[ptr+1]
        core=K-ptr
        r=max(0,T-core)
        assert 0<=r<=R//6
        raycap,vals=ray(K,r)
        diagnostic=caps[ptr]+raycap
        total=RANK1_GLOBAL+raycap
        assert total<L2
        if total>maximum[0]: maximum=(total,[K])
        elif total==maximum[0]: maximum[1].append(K)
        if raycap>maximum_ray[0]: maximum_ray=(raycap,[K])
        elif raycap==maximum_ray[0]: maximum_ray[1].append(K)
        if K in (858_619,858_625,900_000,991_011,1_048_576):
            selected[str(K)]=(inc,ptr,core,r,caps[ptr],raycap,diagnostic,total,vals)
        count+=1
    assert maximum==(4_867_567,[858_619])
    assert maximum_ray==(796_620,[858_619])
    assert count==189_958
    assert result["scan"]["maximum_composed_cap"]==maximum[0]
    assert result["scan"]["maximum_ray_cap"]==maximum_ray[0]
    assert result["first_paid_cell"]["floor_diagnostic_total"]==selected["858619"][6]
    assert result["first_paid_cell"]["total_cap"]==selected["858619"][7]
    assert result["selected_cells"]["1048576"]["total_cap"]==selected["1048576"][7]

    endpoint_controls=0
    for d in range(1,16):
        for K in range(d+2,40):
            for r in range(0,12):
                brute=max(r+1+comb(M+r,2)//(M-1 if M<=K-1 else (K-1)*(M-K+1))
                          for M in range(d+1,K+d+1))
                ends=max(r+1+comb(M+r,2)//(M-1 if M<=K-1 else (K-1)*(M-K+1))
                         for M in (d+1,K-1,K,K+d))
                assert brute==ends
                endpoint_controls+=1

    print("KB_MCA_RANK12_LARGE_LOCATOR_RAY_AUDIT_PASS",
          f"cells={count}",f"endpoint_controls={endpoint_controls}",
          f"max_ray={maximum_ray[0]}",f"max_total={maximum[0]}",
          f"slack={L2-maximum[0]}")

if __name__=='__main__': main()
