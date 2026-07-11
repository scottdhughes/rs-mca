import math
lg=math.lgamma
def lC(N,K):
    if K<0 or K>N or N<0: return -1e18
    return lg(N+1)-lg(K+1)-lg(N-K+1)
n=2**21; p=2**31-2**24+1; lp=math.log(p); ln_n=math.log(n)
THETA=1.7
target=THETA*ln_n                # want lC(n,m)-w*lp = target

# --- reconcile: which (w,m) are theta-consistent? ---
def solve_m(w):                  # smaller root m<n/2
    need=w*lp+target             # lC(n,m)=need
    lo,hi=1,n//2
    while hi-lo>1:
        mid=(lo+hi)//2
        if lC(n,mid)<need: lo=mid
        else: hi=mid
    return hi
def solve_w(m):                  # w = (lC(n,m)-target)/lp
    return (lC(n,m)-target)/lp

w_fixed=67471
m_from_w=solve_m(w_fixed)
m_033=round(0.33*n)
w_from_m=solve_w(m_033)
print("theta=1.7 reconciliation (n=2^21, KoalaBear p):")
print(f"  (A) keep w=67471  -> m={m_from_w} (m/n={m_from_w/n:.4f})")
print(f"  (B) keep m=0.33n  -> w={w_from_m:.0f}")
print(f"  check A: theta={(lC(n,m_from_w)-w_fixed*lp)/ln_n:.3f}   check B: theta={(lC(n,m_033)-w_from_m*lp)/ln_n:.3f}\n")

def analyze(w,m,tag):
    print(f"=== {tag}: w={w}, m={m} (m/n={m/n:.4f}), theta={(lC(n,m)-w*lp)/ln_n:.3f} ===")
    # m-subset energy sum: overlap decomposition Sigma_c N_c^2 = Sum_d C(n,d)C(n-d,d)C(n-2d,m-d)*[collision factor]
    # dominant-layer locator: g(d)=lC(n-2d,m-d)+logEd(d), logEd=min(2lC(n,d)-w lp, lC(n,d)+lC(n-d,d))
    def logEd(d):
        heur=2*lC(n,d)-w*lp
        cap =lC(n,d)+lC(n-d,d)
        return min(heur,cap)
    def g(d):
        if d<1 or 2*d>n or d>m: return -1e18
        return lC(n-2*d,m-d)+logEd(d)
    # collision threshold d0: C(n,d0)=p^{w/2}
    d0=None
    for d in range(1,m+1):
        if lC(n,d)>=0.5*w*lp: d0=d;break
    best=None;bv=-1e18
    for d in range(1,m+1):
        v=g(d)
        if v>bv: bv=v;best=d
    # 90% mass interval
    mx=bv
    import math as _m
    Z=sum(_m.exp(g(d)-mx) for d in range(1,m+1) if g(d)>-1e17)
    order=sorted((d for d in range(1,m+1) if g(d)>-1e17),key=lambda d:-g(d))
    acc=0;kept=[]
    for d in order:
        acc+=_m.exp(g(d)-mx);kept.append(d)
        if acc/Z>=0.90:break
    kept.sort()
    print(f"  collision threshold d0={d0} (d0-w={d0-w})")
    print(f"  saddle d*={best}  (d*/n={best/n:.4f}, d*/m={best/m:.4f})")
    print(f"  EFFECTIVE FIBER DIMENSION of dominant layer  d*-w = {best-w}")
    print(f"  ~90% energy mass in d in [{kept[0]},{kept[-1]}] -> dims d-w in [{kept[0]-w},{kept[-1]-w}]")
    print(f"  is dominant layer low-dim (d*-w<=3)? {'YES' if best-w<=3 else 'NO -- high-dim wall bites the bulk'}\n")

analyze(w_fixed,m_from_w,"(A) w=67471 fixed")
analyze(m_033 and 61870, m_033, "(B) m=0.33n fixed, w~61870")
