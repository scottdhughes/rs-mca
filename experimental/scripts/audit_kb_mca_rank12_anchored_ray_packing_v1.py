#!/usr/bin/env python3
"""Independent arithmetic and finite-model audit for anchored ray packing."""
from __future__ import annotations
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'experimental/data/certificates/kb-mca-rank12-anchored-ray-packing-v1/result.json'
R=1_048_576;D=67_472;T=981_104;L2=5_170_912;M0=D+1
class AuditError(ValueError): pass
def need(x,msg):
    if not x: raise AuditError(msg)

def line_cap(k:int)->int:
    n=R+k;m=D+k;q=m//2;s=m-q-1
    low=comb(n,2)//(q*(m-q));best=Fraction(-1,1)
    for h in range(1,n//(q+1)+1):
        for p in range(h+1):
            w=n-h*m+p+(h-p)*s
            if w<0:continue
            best=max(best,Fraction(h*(h-1),1)+Fraction(w*(p*s+h-p),s))
    return low+best.numerator//best.denominator

def ray_cap(r:int)->int:
    A=(M0-1)//2;low=comb(M0+r,2)//((M0//2)*(M0-M0//2));best=Fraction(-1,1)
    for parity in (0,1):
        for h in range(1,(M0+r)//(M0//2+1)+1):
            for p in range(h+1):
                b=h-p;C=r-(h-1)+p if parity==0 else r-2*(h-1)+p;d=h+p-2;cand={A}
                if d>0:cand|={C//d,C//d-1}
                for x in cand:
                    if x<A:continue
                    W=C-d*x
                    if W<0:continue
                    best=max(best,Fraction(h*(h-1),1)+Fraction(W*(p*x+b),x))
    return low+best.numerator//best.denominator

def finite_set_audit()->int:
    checked=0
    for N in range(6,11):
        universe=set(range(N))
        for r in range(1,N//3):
            for Ftuple in combinations(range(N),min(2*r,N)):
                F=set(Ftuple);Y=universe-F;b=N-len(F)-r
                if b<=0:continue
                need(len(Y)//b<=(N-2*r)//(N-3*r),'finite anchored packing');checked+=1
    return checked

def main():
    data=json.loads(RESULT.read_text())
    need(data['parent']=='ed556ccb7527e1c54e58b8d151ccefd8539000ac','parent')
    need((line_cap(1),line_cap(35142),line_cap(57259))==(4070947,2853508,2427829),'rank caps')
    rays=(ray_cap(262144),ray_cap(274493),ray_cap(309634),ray_cap(335114),ray_cap(344037))
    need(rays==(389395,418707,524141,600590,627362),'ray bounds')
    first=(1_118_121-2*344_037,1_118_121-3*344_037);adjacent=(1_118_121-2*344_038,1_118_121-3*344_038)
    need((first[0]//first[1],adjacent[0]//adjacent[1])==(4,5),'ray-count wall')
    caps={'q1':4070947+389395,'q2':4070947+2*418707,'q3':2853508+3*524141,'q4':2427829+4*627362}
    need(caps==data['branch_caps'],'branch caps');need(max(caps.values())==4_937_277,'maximum');need(L2-max(caps.values())==233_635,'slack')
    controls=finite_set_audit()
    print('KB_MCA_RANK12_ANCHORED_RAY_PACKING_AUDIT_PASS '+f'rays={rays} max={max(caps.values())} slack={L2-max(caps.values())} finite={controls}')
if __name__=='__main__':main()
