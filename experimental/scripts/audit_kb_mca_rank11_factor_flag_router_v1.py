#!/usr/bin/env python3
"""Independent audit for the rank-eleven factor-flag router."""
from __future__ import annotations
import hashlib, itertools, json
from math import comb, prod
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/"experimental/data/certificates/kb-mca-rank11-factor-flag-router-v1/result.json"

def falling(x,r):
    v=1
    for j in range(r): v*=x-j
    return v

def independent(v,w,p=3): return (v[0]*w[1]-v[1]*w[0])%p!=0

def compositions(total,parts,prefix=()):
    if parts==1:
        yield prefix+(total,); return
    for x in range(total+1):
        yield from compositions(total-x,parts-1,prefix+(x,))

def finite_terminal_line_control():
    vec=[(a,b) for a in range(3) for b in range(3)]
    lines=[{(1,0),(2,0)},{(0,1),(0,2)},{(1,1),(2,2)},{(1,2),(2,1)}]
    checked=0; minimum=None
    for c in compositions(6,len(vec)):
        zero=c[vec.index((0,0))]
        if zero>1: continue
        if any(zero+sum(c[vec.index(v)] for v in L)>3 for L in lines): continue
        bases=sum(c[i]*c[j] for i,v in enumerate(vec) for j,w in enumerate(vec)
                  if independent(v,w))
        if minimum is None or bases<minimum: minimum=bases
        assert bases>=15
        checked+=1
    assert checked>0 and minimum==16
    return checked,minimum

def finite_plane_control():
    vec=[(a,b) for a in range(3) for b in range(3)]
    lines=[{(1,0),(2,0)},{(0,1),(0,2)},{(1,1),(2,2)},{(1,2),(2,1)}]
    checked=0; minimum=None
    for c in compositions(6,len(vec)):
        zero=c[vec.index((0,0))]
        if any(zero+sum(c[vec.index(v)] for v in L)>3 for L in lines): continue
        bases=sum(c[i]*c[j] for i,v in enumerate(vec) for j,w in enumerate(vec)
                  if independent(v,w))
        if minimum is None or bases<minimum: minimum=bases
        assert bases>=9
        checked+=1
    assert checked>0 and minimum==12
    return checked,minimum

def main():
    r=json.loads(RESULT.read_text())
    n=2097152; K=1048576; m=1116048; tau=1936
    H0=m-4; A=m-tau; h=H0+A-n; Z2=117731; Z3=23354
    q1=(n-K+1)//(A-K+1)
    q2=((n-K+2)*(n-K+1)//2)//((A-K+2)*(A-K+1)//2)
    N1=falling(H0,9)//((h-Z2+1)*(h-Z3+1)**8)
    N2=falling(H0,8)//((Z2-Z3+1)**8)
    owner=n-A
    low=(N1*q1+N2*q2)*owner+owner
    assert (q1,q2,N1,N2,low)==(15,255,8415196932,382360905,219935524214538240)
    best=None
    for z2 in range(Z3,h+1):
        a=falling(H0,9)//((h-z2+1)*(h-Z3+1)**8)
        b=falling(H0,8)//((z2-Z3+1)**8)
        val=(a*q1+b*q2)*owner+owner
        if best is None or (val,z2)<best: best=(val,z2)
    assert best==(219935524214538240,117731)
    adjacent=None
    for z2 in range(Z3+1,h+1):
        a=falling(H0,9)//((h-z2+1)*(h-(Z3+1)+1)**8)
        b=falling(H0,8)//((z2-(Z3+1)+1)**8)
        val=(a*q1+b*q2)*owner+owner
        if adjacent is None or (val,z2)<adjacent: adjacent=(val,z2)
    assert adjacent==(219952702956503040,117731)
    t1=finite_terminal_line_control(); t2=finite_plane_control()
    assert r["total"]==274978667290066176 and r["Z3"]==23354
    print("KB_MCA_RANK11_FACTOR_FLAG_AUDIT_PASS "
          f"terminal_profiles={t1[0]} plane_profiles={t2[0]} "
          f"finite_minima={t1[1]},{t2[1]}")
if __name__=="__main__": main()
