import cmath, math, itertools
from math import comb
def mu_n(p,n):
    assert (p-1)%n==0
    def order(x):
        o=1;v=x
        while v!=1: v=v*x%p;o+=1
        return o
    g=next(c for c in range(2,p) if order(c)==p-1)
    h=pow(g,(p-1)//n,p); S=[1];v=h
    while v!=1: S.append(v);v=v*h%p
    return S
def esym(vals,d):
    e=[0j]*(d+1);e[0]=1+0j
    for x in vals:
        for k in range(d,0,-1): e[k]+=x*e[k-1]
    return e[d]
def excess_ratio(p,n,w,d):
    S=mu_n(p,n); tp=2j*math.pi/p
    main=comb(n,d)**2; tot=0.0
    for c in itertools.product(range(p),repeat=w):
        s_list=[]
        for a in S:
            s=0;ap=a
            for j in range(w): s=(s+c[j]*ap)%p; ap=ap*a%p
            s_list.append(cmath.exp(tp*s))
        tot+=abs(esym(s_list,d))**2
    return (tot-main)/main
print("THRESHOLD TEST: excess/main vs  ratio r = n/(w*sqrt(p))   [expect collapse once r>1]")
print(f"{'p':>4} {'n':>4} {'w':>2} {'d':>3} {'w*sqrt(p)':>10} {'n/(w√p)':>8} {'excess/main':>14}")
for p,w in [(17,2),(41,2),(97,2)]:
    sp=math.sqrt(p); thr=w*sp
    # divisors n of p-1 with n>=8
    ns=[k for k in range(4,p) if (p-1)%k==0]
    for n in ns:
        d=max(2,round(0.33*n))
        if d>=n: continue
        try: r=excess_ratio(p,n,w,d)
        except Exception as e: print("err",e);continue
        print(f"{p:>4} {n:>4} {w:>2} {d:>3} {thr:>10.2f} {n/thr:>8.3f} {r:>14.4e}")
    print()
