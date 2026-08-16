from fractions import Fraction
from math import prod

R=1_048_576
D=67_472
KMAX=1_048_576
BUDGET=274_980_728_111_395_087
NEAR=134_944
LOAD0=BUDGET-NEAR+1

def fall(x,r):
    return prod(x-i for i in range(r))

def rise(x,r):
    return prod(x+i for i in range(r))

def ceilq(a,b):
    return -(-a//b)

def resource(s,K):
    vals=[Fraction(R+K)]
    for r in range(1,s+1):
        vals += [
            Fraction(fall(R+K,r+1),(D+K)*rise(D+1,r-1)),
            Fraction(fall(R+r,r+1),rise(D+1,r)),
        ]
    q=max(vals)
    return q.numerator//q.denominator

def descend(start,stop=1,capped=False):
    out={start:LOAD0}
    for s in range(start,stop,-1):
        c=resource(s,s)
        if capped:
            c=min(c,out[s]*(D+1))
        out[s-1]=ceilq(out[s]*(D+s)-c,R+s)
    return out

def scan(loads,stop,capped=False):
    checked=0
    rows={}
    for s in range(max(loads),stop,-1):
        L=loads[s]; expected=loads[s-1]
        constant=fall(R+s,s+1)//rise(D+1,s)
        denom=rise(D+1,s-1)
        P=fall(R+s,s+1)
        low=None
        first=None
        decreases=0
        previous=None
        for K in range(s,KMAX+1):
            c=max(P//((D+K)*denom),constant)
            if capped:
                c=min(c,L*(D+1))
            value=ceilq(L*(D+K)-c,R+K)
            if low is None or value<low:
                low=value
                first=K
            if previous is not None and value<previous:
                decreases+=1
            previous=value
            checked+=1
            if K<KMAX:
                P=P*(R+K+1)//(R+K-s)
        assert low==loads[s-1] and first==s
        rows[s]=(low,decreases,KMAX-s+1)
    return checked,rows
