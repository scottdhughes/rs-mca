from math import comb
from kb_rank_descent import R,D,resource

P=2_130_706_433
FIELD=P**6
FIXED=R-D+1

def fisher(k,T):
    n=R+k
    h=D+k-T
    lam=k-1
    den=h*h-n*lam
    if den<=0:
        return None
    return n*(h-lam)//den

def endpoint(k,T):
    r=fisher(k,T)
    if r is None:
        return None
    return r*FIXED+resource(k,k)//(T+1)

def best_endpoint(k,forced):
    best=None
    first=None
    for T in range(1,D+2):
        cap=endpoint(k,T)
        if cap is None:
            continue
        if best is None or cap<best[1]:
            best=(T,cap)
        if first is None and cap<=forced:
            first=(T,cap)
    return best,first

def pair_prefix(k,delta):
    h=D+k-delta
    lam=k-1
    caps=[]
    den=h*h-(R+k)*lam
    if den>0:
        caps.append((R+k)*(h-lam)//den)
    if h>=k:
        q=comb(R+k,k)//comb(h,k)
        if q*q<FIELD:
            caps.append(q)
    return min(caps) if caps else None

def coupled(k):
    remaining=resource(k,k)
    total=0
    prev=0
    last=0
    for delta in range(1,D+2):
        prefix=pair_prefix(k,delta)
        if prefix is None:
            take=remaining//delta
            total+=take
            remaining-=take*delta
            last=delta
            break
        assert prefix>=prev
        new=prefix-prev
        per=(R-D+delta)//delta
        slots=new*per
        take=min(slots,remaining//delta)
        total+=take
        remaining-=take*delta
        prev=prefix
        last=delta
        if take<slots or remaining<delta+1:
            break
    return total,remaining,last
