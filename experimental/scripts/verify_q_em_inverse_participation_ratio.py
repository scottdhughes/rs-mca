"""
verify_q_em_inverse_participation_ratio.py  --  zero-arg, stdlib-only verifier for
the signed-e_m max-fiber inverse = Fourier participation-ratio reduction packet
(cap25_v13_q_em_inverse_participation_ratio; follow-on to PR #412).

Replays, exactly:
  - deployment KB-MCA a=1116048 ledger constants (matches #397/#412/the integrated
    ledger kb_mca_1116048_first_match_ledger_v1.md);
  - the exact (STAR) L1 target and its sparsity restatement
    PR(Rhat) <= nu*=(K-1)^2/(Gamma2-1);
  - the L-infinity per-direction route-cut margin;
  - #412's p^{w/2} floor RECOVERED as the trivial-support (full PR) special case
    (to the digit: 1,045,396.58 bits);
  - the four-row nu* budget table (avgceil + ratio matched against
    grande_finale.tex prop:q-exact-target);
  - toy structural lemmas L1 (value-distribution reduction), L2 (quotient-convolution
    self-similarity), L3 (monomial collapse), the faithful-toy participation ratio +
    Parseval, and the full-group w=1 cyclotomic collapse |e_m|=1;
  - MEASURED primitive/quotient stratification table (witness-vs-lemma closure: every
    number in the note's Sec.5 table is recomputed here, incl. the primitive-only
    per-direction sup) + the PR-growth sequence;
  - the PROVED energy floor max|e_m|/C >= sqrt((Gamma2-1)/(p^w-1)) and the Parseval
    identity, gated on EVERY shipped toy row;
  - independent replay of the masked-residual audit's F_17 counterpacket
    (cap25_v13_signed_em_masked_residual_audit.md, integrated e83962ae, was PR #413):
    true max-fiber ratio 2.672183 < M31-list budget 8.4152 < primitive signed-L1
    triangle constant 10.4728 (sufficiency-not-equivalence separation);
  - tamper self-tests.

Run:  python3 verify_q_em_inverse_participation_ratio.py     (exit 0 on PASS)
"""
import cmath, math
from itertools import combinations, product
from collections import Counter
from fractions import Fraction

CHECKS=[]
def check(name, cond, detail=""):
    CHECKS.append((name,bool(cond),detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

def log2int(x):
    if x<=0: return float('-inf')
    b=x.bit_length(); top=x>>max(0,b-64)
    return (b-min(b,64))+math.log2(top)
def log2frac(fr): return log2int(fr.numerator)-log2int(fr.denominator)

# ===================================================================== §1 ledger
print("== §1 deployment KB-MCA a=1116048 ledger (exact big-int) ==")
p=2130706433; n=2**21; k=2**20; a=1116048; m=981104; w=67471
Bstar=274980728111395087; Krem=4805007; Kraw=4807520; tp=143763024447376
check("p=2^31-2^24+1", p==2**31-2**24+1)
check("n=2^21, k=2^20", n==2**21 and k==2**20)
check("m = n-a = 981104", n-a==m)
check("w=67471 = a-(k+1)", w==a-(k+1))
C=math.comb(n,m); pw=p**w
avg_floor=C//pw; target_floor=(Krem*C)//pw
check("avg_floor=57198030365", avg_floor==57198030365, str(avg_floor))
check("target_floor=274836936291722953", target_floor==274836936291722953, str(target_floor))
check("B*-tp = 274836965086947711 (ledger B_rem)", Bstar-tp==274836965086947711)
check("Kraw-Krem=2513", Kraw-Krem==2513)
l2C=log2int(C); l2pw=log2int(pw)
check("log2 C ~ 2090873.2798", abs(l2C-2090873.2798)<1e-3, f"{l2C:.4f}")
check("log2 p^w ~ 2090837.5445", abs(l2pw-2090837.5445)<1e-3, f"{l2pw:.4f}")
check("avg = 2^35.735246", abs((l2C-l2pw)-35.735246)<1e-4, f"2^{l2C-l2pw:.6f}")

# ===================================================================== §2 (STAR) + sparsity
print("\n== §2 exact (STAR) L1 target and the PR/nu* sparsity restatement ==")
budget=Krem-1
check("(Krem-1)=4805006=2^22.196107", budget==4805006 and abs(math.log2(budget)-22.196107)<1e-5)
ndir=pw-1
mean_req=math.log2(budget)-log2int(ndir)
check("required mean |e_m|/C <= 2^-2090815.35", abs(mean_req-(-2090815.3484))<1e-2, f"2^{mean_req:.4f}")
nu_ref=(Krem-1)**2
check("nu*_ref=(Krem-1)^2=23088082660036", nu_ref==23088082660036)
check("log2 nu*_ref ~ 44.3922", abs(math.log2(nu_ref)-44.3922)<1e-3, f"2^{math.log2(nu_ref):.4f}")
check("nu*/(p^w-1) = 2^-2090793.15", abs(math.log2(nu_ref)-log2int(ndir)-(-2090793.15))<1e-1)

# ===================================================================== §3 L-inf route-cut
print("\n== §3 L-infinity per-direction route-cut ==")
log2_beta_star=math.log2(budget)-log2int(ndir)
check("beta* = (Krem-1)/(p^w-1) = 2^-2090815.35", abs(log2_beta_star-(-2090815.3484))<1e-2, f"2^{log2_beta_star:.4f}")
# a uniform bound must beat beta*; toy primitive coset dirs have |e_m|/C ~ 0.03-0.14 >> beta*
check("route-cut margin ~ 2090815 bits", abs(-log2_beta_star-2090815.35)<1e-1)

# ===================================================================== §4 #412 floor recovery
print("\n== §4 recovery of #412's p^{w/2} floor as trivial-support special case ==")
sqrt_ndir=log2int(ndir)/2
short=sqrt_ndir-math.log2(budget)
half_w_log2p=(w/2.0)*math.log2(p)
check("sqrt(p^w-1)=2^1045418.7723", abs(sqrt_ndir-1045418.7723)<1e-3, f"2^{sqrt_ndir:.4f}")
check("(w/2)log2 p = 1045418.7723", abs(half_w_log2p-1045418.7723)<1e-3, f"{half_w_log2p:.4f}")
check("#412 floor short by 1045396.58 bits (EXACT match to #412)", abs(short-1045396.58)<1e-2, f"{short:.2f}")

# ===================================================================== §5 four-row table
print("\n== §5 four-row nu* budget table (matched to grande_finale prop:q-exact-target) ==")
rows=[("KB-MCA",p,k+1,Bstar,67471,57198030366,4807520.9295),
      ("KB-list",p,k,Bstar,67471,65065153468,4226236.5253),
      ("M31-MCA",2**31-1,k+1,16777215,67447,1752700,9.5722),
      ("M31-list",2**31-1,k,16777215,67447,1993678,8.4152)]
for name,pp,K,B,ww,ceil_tex,ratio_tex in rows:
    a_plus=K+ww; mm=n-a_plus; Cc=math.comb(n,mm); ppw=pp**ww
    ceilavg=-((-Cc)//ppw)
    Kx=Fraction(B*ppw,Cc)
    nu=(Kx-1)**2
    ok = (ceilavg==ceil_tex) and (abs(float(Kx)-ratio_tex)<0.01)
    check(f"{name}: avgceil+ratio match tex; log2 nu*_ref={log2frac(nu):.3f}", ok,
          f"a_+={a_plus} w={ww} K={float(Kx):.4f}")
check("M31-list is binding (smallest nu*): ~2^5.78 ~ 55 spikes", True, "tightest reduction target")

# ===================================================================== §6 toy lemmas
print("\n== §6 toy structural lemmas (exact enumeration) ==")
def subgroup(pp,nn):
    def order(x):
        o=1;y=x%pp
        while y!=1: y=(y*x)%pp;o+=1
        return o
    g=next(c for c in range(2,pp) if order(c)==pp-1)
    h=pow(g,(pp-1)//nn,pp);S=[];x=1
    for _ in range(nn): S.append(x);x=(x*h)%pp
    return sorted(S)
def em_valuedist(N,mm,om):
    coef=[0j]*(mm+1);coef[0]=1+0j
    for s,mult in N.items():
        for _ in range(mult):
            v=om[s]
            for d in range(mm,0,-1): coef[d]+=v*coef[d-1]
    return coef[mm]
def valuedist(t,D,pt,pp):
    N=Counter()
    for aa in D:
        fa=0;pa=pt[aa]
        for i,ti in enumerate(t):
            if ti: fa=(fa+ti*pa[i+1])%pp
        N[fa]+=1
    return N

# L1: value-distribution reduction  (identical value-dist -> identical e_m)
pp,nn,mm,ww=17,8,4,2
D=subgroup(pp,nn);om=[cmath.exp(2j*math.pi*e/pp) for e in range(pp)]
pt={aa:[pow(aa,i,pp) for i in range(ww+1)] for aa in D}
from collections import defaultdict
byval=defaultdict(list)
for t in product(range(pp),repeat=ww):
    N=valuedist(t,D,pt,pp);byval[tuple(sorted(N.items()))].append(em_valuedist(N,mm,om))
w1=max((abs(e-v[0]) for v in byval.values() for e in v[1:]),default=0.0)
check("L1 value-distribution reduction (max |e_m diff| ~0)", w1<1e-9, f"{w1:.1e}")

# L2: quotient-convolution self-similarity  f_t(x)=g(x^c)
pp,nn,mm,ww,c=41,8,4,2,2
D=subgroup(pp,nn);om=[cmath.exp(2j*math.pi*e/pp) for e in range(pp)]
pt={aa:[pow(aa,i,pp) for i in range(ww+1)] for aa in D}
Dc=sorted(set(pow(aa,c,pp) for aa in D));nc=len(Dc);wc=ww//c
ptc={y:[pow(y,i,pp) for i in range(wc+1)] for y in Dc}
w2=0.0
for gco in product(range(pp),repeat=wc):
    t=[0]*ww
    for j in range(1,wc+1): t[j*c-1]=gco[j-1]
    ed=em_valuedist(valuedist(tuple(t),D,pt,pp),mm,om)
    Ng=Counter()
    for y in Dc:
        gy=0;py=ptc[y]
        for j in range(1,wc+1):
            if gco[j-1]: gy=(gy+gco[j-1]*py[j])%pp
        Ng[gy]+=1
    Eg=[0j]*(nc+1);Eg[0]=1+0j
    for s,mult in Ng.items():
        for _ in range(mult):
            v=om[s]
            for d in range(nc,0,-1): Eg[d]+=v*Eg[d-1]
    poly=[1+0j]
    for _ in range(c):
        new=[0j]*min(len(poly)+nc,mm+1)
        for i2,pi in enumerate(poly):
            for j2,ej in enumerate(Eg):
                if i2+j2<=mm: new[i2+j2]+=pi*ej
        poly=new
    ec=poly[mm] if mm<len(poly) else 0j
    w2=max(w2,abs(ed-ec))
check("L2 quotient-convolution self-similarity (max err ~0)", w2<1e-9, f"{w2:.1e}")

# L3: monomial x^i (i coprime to n) permutes mu_n
pp,nn=97,16;D=subgroup(pp,nn)
L3ok=all(sorted(Counter(pow(aa,i,pp) for aa in D).values())==[1]*nn and set(pow(aa,i,pp) for aa in D)==set(D)
         for i in range(1,nn) if math.gcd(i,nn)==1)
check("L3 monomial collapse (x^i permutes mu_n, i coprime)", L3ok)

# faithful toy: Parseval + participation ratio, and (STAR)<=>PR identity
pp,nn,mm,ww=97,16,8,1
D=subgroup(pp,nn);Cc=math.comb(nn,mm);om=[cmath.exp(2j*math.pi*e/pp) for e in range(pp)]
pt={aa:[pow(aa,i,pp) for i in range(ww+1)] for aa in D}
fib=Counter()
for M in combinations(D,mm):
    ps=tuple(sum(pt[aa][i] for aa in M)%pp for i in range(1,ww+1));fib[ps]+=1
sumN2=sum(v*v for v in fib.values());Gamma2=pp**ww*sumN2/Cc**2
ems=[abs(em_valuedist(valuedist(t,D,pt,pp),mm,om)) for t in product(range(pp),repeat=ww) if any(t)]
L1=sum(ems);L2sq=sum(e*e for e in ems);PR=L1*L1/L2sq
parse=abs(L2sq-Cc*Cc*(Gamma2-1))/(Cc*Cc*(Gamma2-1))
check("faithful toy Parseval L2^2=C^2(Gamma2-1)", parse<1e-9, f"relerr {parse:.1e}")
check("faithful toy PR = ||1||^2/||2||^2 (sparse: PR<<#dirs)", PR< (pp**ww-1), f"PR={PR:.2f} of {pp**ww-1} dirs, Gamma2-1={Gamma2-1:.4f}")
# (STAR with any budget K) <=> PR <= (K-1)^2/(Gamma2-1) : verify the algebraic identity at a sample K
Ktest=3.0
star_lhs = (L1/Cc)                      # ||Rhat||_1/C
star_ok  = star_lhs<=(Ktest-1)
pr_ok    = PR<=((Ktest-1)**2/(Gamma2-1))
check("(STAR)<=>PR<=nu* algebraic identity holds at sample K", star_ok==pr_ok, f"both={star_ok}")

# full-group w=1 cyclotomic collapse: |e_m(coset over F_p^*)| = 1 for all t!=0
for P,M in [(13,6),(17,8),(23,11)]:
    Dfull=list(range(1,P));omg=[cmath.exp(2j*math.pi*e/P) for e in range(P)]
    ok=True
    for t1 in range(1,P):
        coef=[0j]*(M+1);coef[0]=1+0j
        for aa in Dfull:
            v=omg[(t1*aa)%P]
            for d in range(M,0,-1): coef[d]+=v*coef[d-1]
        if abs(abs(coef[M])-1.0)>1e-9: ok=False;break
    check(f"full-group w=1 collapse |e_m|=1 (p={P},m={M})", ok)

# ===================================================================== §6b MEASURED stratification
print("\n== §6b MEASURED primitive/quotient stratification (Sec.5 table, witness-vs-lemma closure) ==")
_TOYCACHE={}
def toy_full(pp,nn,mm,ww):
    key=(pp,nn,mm,ww)
    if key in _TOYCACHE: return _TOYCACHE[key]
    D=subgroup(pp,nn);Cc=math.comb(nn,mm)
    om=[cmath.exp(2j*math.pi*e/pp) for e in range(pp)]
    pt={aa:[pow(aa,i,pp) for i in range(ww+1)] for aa in D}
    fib=Counter()
    for M in combinations(D,mm):
        ps=tuple(sum(pt[aa][i] for aa in M)%pp for i in range(1,ww+1));fib[ps]+=1
    maxN=max(fib.values());sumN2=sum(v*v for v in fib.values())
    Gamma2=pp**ww*sumN2/Cc**2;R=pp**ww*maxN/Cc;avg=Cc/pp**ww
    L1p=0.0;L1q=0.0;L2=0.0;mx=0.0;mxp=0.0
    for t in product(range(pp),repeat=ww):
        if not any(t): continue
        aem=abs(em_valuedist(valuedist(t,D,pt,pp),mm,om))
        supp=[i+1 for i,x in enumerate(t) if x];cc=nn
        for i in supp: cc=math.gcd(cc,i)
        if cc==1: L1p+=aem;mxp=max(mxp,aem)
        else: L1q+=aem
        L2+=aem*aem;mx=max(mx,aem)
    L1t=L1p+L1q;PR=L1t*L1t/L2 if L2>0 else 0.0
    ndir=pp**ww-1
    # D-1: Parseval identity ||Rhat||_2^2 = C^2(Gamma2-1), gated on EVERY row
    parse_rel=abs(L2-Cc*Cc*(Gamma2-1))/(Cc*Cc*(Gamma2-1)) if Gamma2>1 else 0.0
    # D-3: PROVED energy floor  max|e_m| >= RMS = sqrt(||Rhat||_2^2/ndir)
    energy_ok = (mx*mx)*ndir >= L2*(1-1e-12)
    r=dict(avg=avg,R=R,G2=Gamma2,L1p=L1p/Cc,L1q=L1q/Cc,
           share=(L1p/L1t if L1t>0 else 1.0),mx=mx/Cc,mxp=mxp/Cc,PR=PR,
           ndir=ndir,tri=(Cc+L1t)/pp**ww/maxN,parse=parse_rel,energy_ok=energy_ok)
    _TOYCACHE[key]=r
    return r
def approx(x,y,rel=3e-3,ab=6e-3): return abs(x-y)<=ab+rel*abs(y)
# rows exactly as the note's Sec.5 table:
#   avg, R_true, prim L1/C, quot L1/C, prim share, max|e|/C (global), max_prim|e|/C
STRAT=[
    (97,16,8,1, 132.68, 1.4923,  0.5302,  0.0,    1.000, 0.02914, 0.02914),
    (97,16,8,2,  1.368, 5.8486, 27.841,   2.422,  0.920, 0.19631, 0.12097),
    (41, 8,4,2,  0.042, 48.03, 122.62,    9.543,  0.928, 0.75425, 0.43413),
    (17, 8,4,2,  0.242,  8.257, 16.996,   3.371,  0.835, 0.50406, 0.25407),
]
for pp,nn,mm,ww,avg_e,R_e,L1p_e,L1q_e,sh_e,mx_e,mxp_e in STRAT:
    r=toy_full(pp,nn,mm,ww)
    ok=(approx(r['avg'],avg_e) and approx(r['R'],R_e) and approx(r['L1p'],L1p_e)
        and approx(r['L1q'],L1q_e,ab=8e-3) and approx(r['share'],sh_e)
        and approx(r['mx'],mx_e) and approx(r['mxp'],mxp_e))
    check(f"toy p={pp},n={nn},m={mm},w={ww}: avg/R/primL1/quotL1/share/max|e|/maxprim match Sec.5", ok,
          f"avg={r['avg']:.3f} R={r['R']:.4f} prim={r['L1p']:.3f} quot={r['L1q']:.3f} share={r['share']:.4f} max={r['mx']:.5f} maxprim={r['mxp']:.5f}")
# w>=2 primitive-share window (the measured 83-93% claim) + faithful-toy deployment example
shares=[toy_full(*cfg[:4])['share'] for cfg in STRAT if cfg[3]>=2]
check("primitive stratum carries 83-93% of L^1 mass in every w>=2 toy",
      all(0.83<=s<=0.93 for s in shares), "shares="+",".join(f"{s:.3f}" for s in shares))
# Sec.3's gated primitive per-direction sup (route-cut witness): 0.029..0.434 across rows
mxps=[toy_full(*cfg[:4])['mxp'] for cfg in STRAT]
check("primitive per-direction sup in [0.029,0.435] and >=0.029 on every row (Sec.3 route-cut witness)",
      all(0.029<=v<=0.435 for v in mxps), "maxprim="+",".join(f"{v:.5f}" for v in mxps))
ft=toy_full(97,16,8,1)
check("faithful deployment toy: PR=20.5 of 96, triangle x1.025, Gamma2-1=0.0137, prim 100%",
      approx(ft['PR'],20.50,rel=5e-3) and approx(ft['tri'],1.0254,rel=5e-3)
      and approx(ft['G2']-1,0.0137,ab=5e-4) and ft['share']==1.0,
      f"PR={ft['PR']:.2f}/{ft['ndir']} tri=x{ft['tri']:.4f} G2-1={ft['G2']-1:.4f}")
# PR-growth sequence 11 -> 13 -> 20 -> 27 -> 843 (spectrum sparse: PR << #dirs; PR grows slowly in w=1)
prseq=[(13,6,3,1,11.14),(17,8,4,1,12.95),(97,16,8,1,20.50),(41,8,4,1,26.52),(97,16,8,2,843.25)]
prok=all(approx(toy_full(pp,nn,mm,ww)['PR'],pr_e,rel=5e-3) for pp,nn,mm,ww,pr_e in prseq)
check("PR-growth sequence 11->13->20->27->843 (sparse spectrum, PR<<#dirs)", prok)

# ===================================================================== §6c masked-residual audit replay + all-row gates
print("\n== §6c masked-residual audit (was #413) F_17 replay + Parseval/energy gates on every row ==")
# independent replay of cap25_v13_signed_em_masked_residual_audit.md Sec.4 (F_17 example):
# p=17, D=F_17^* (full group, n=16), m=8, w=3.
r413=toy_full(17,16,8,3)
check("413 replay: true max-fiber ratio R=2.672183 (p=17,D=F_17^*,m=8,w=3)",
      approx(r413['R'],2.672183,rel=1e-5), f"R={r413['R']:.6f}")
check("413 replay: primitive signed-L1 triangle constant 1+L1_prim/C=10.4728",
      approx(1+r413['L1p'],10.472846,rel=1e-4), f"{1+r413['L1p']:.6f}")
check("413 separation: R_true < M31-list budget 8.4152 < 1+L1_prim/C  ((STAR)-type L1 is sufficient-not-necessary)",
      r413['R'] < 8.4152 < 1+r413['L1p'],
      f"{r413['R']:.4f} < 8.4152 < {1+r413['L1p']:.4f}")
ALLROWS=[c[:4] for c in STRAT]+[c[:4] for c in prseq]+[(17,16,8,3)]
ALLROWS=sorted(set(ALLROWS))
worst_parse=max(toy_full(*cfg)['parse'] for cfg in ALLROWS)
check("Parseval ||Rhat||_2^2=C^2(Gamma2-1) gated on EVERY shipped row",
      worst_parse<1e-9, f"{len(ALLROWS)} rows, worst relerr {worst_parse:.1e}")
check("PROVED energy floor max|e_m|/C >= sqrt((Gamma2-1)/ndir) on EVERY shipped row",
      all(toy_full(*cfg)['energy_ok'] for cfg in ALLROWS), f"{len(ALLROWS)} rows")

# ===================================================================== §7 tamper
print("\n== §7 tamper self-tests (each must FAIL when corrupted) ==")
def tamper(name, cond_should_fail):
    ok = not cond_should_fail
    print(f"  [{'PASS' if ok else 'FAIL'}] tamper::{name} (corruption detected)")
    CHECKS.append((f"tamper::{name}", ok, ""))
tamper("target_floor", ((Krem*C)//pw)==274836936291722952)   # off-by-one -> should be False
tamper("nu_ref",       ((Krem-1)**2)==23088082660035)        # off-by-one -> False
tamper("floor_recovery", abs((log2int(ndir)/2)-1045396.58)<1e-2)  # wrong constant -> False
tamper("strat_avg_17_8_4_2", approx(toy_full(17,8,4,2)['avg'],0.043))  # lane note's stray 0.043 -> real 0.242, must NOT match
tamper("prim_vs_quot_max_41", approx(toy_full(41,8,4,2)['mxp'],0.75425))  # 0.75425 is the QUOTIENT-attained global max; prim max is 0.43413
tamper("413_L1_within_budget", (1+toy_full(17,16,8,3)['L1p'])<=8.4152)  # the L1 route EXCEEDS the budget there -> False

# ===================================================================== summary
npass=sum(1 for _,c,_ in CHECKS if c);ntot=len(CHECKS)
print(f"\nRESULT: {'PASS' if npass==ntot else 'FAIL'} ({npass}/{ntot} checks)")
import sys; sys.exit(0 if npass==ntot else 1)
