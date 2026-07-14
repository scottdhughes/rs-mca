#!/usr/bin/env sage
# Verifier: axis (worst monomial-resonance / g-damping) spectral-gap lattice bound.
#
# STATUS: EXPERIMENTAL / PROVED-LEMMA (single axis sub-case of the second-moment problem).
#
# CLAIM: reproduces, at the deployed KoalaBear list-row parameters, the two exact integer
# lattice minima and the resulting kappa^2 bound for the worst monomial-resonance axis
# (the g-fold-collapsed mu_32 direction).  This is a PROVED sub-lemma of the exact second
# moment (split-pair census) at the deployed band depth.  It does NOT close the finite
# problem: the off-axis (arc-cluster) theta-quotient remains conjectural.
#
# Two independent ingredients are checked:
#   (A) the exact lattice spectral gap at the deployment prime (this file, Sage/fplll);
#       cross-checked by PARI qfminim independently (see the note; M+ agrees exactly).
#   (B) the exact CRT-DP kappa^2 at head depths g=1,2,4 (matches the closed-form ladder),
#       confirming the object the axis bound controls.

import json
from datetime import datetime, timezone

STATUS = "EXPERIMENTAL / PROVED-LEMMA (axis sub-case)"
CLAIM = ("axis g-damping spectral-gap lattice bound at the deployed KoalaBear list row; "
         "PROVED sub-lemma of the exact second moment; does NOT close the finite problem "
         "(off-axis theta-quotient remains conjectural); no MCA/list prize-safety assertion")

# ---- deployed KoalaBear list-row parameters (verified to match towards-prize.md) ----
p = 2**31 - 2**24 + 1          # KoalaBear prime = 2130706433
n = 2**21                      # evaluation-subgroup order = 2097152
w = 67471                      # prefix depth (deployed band depth ~6.7e4)
m = n//2 - (w+1)               # 981104  (second-moment / split-pair parametrization)
h = 32                         # worst collapsed subgroup mu_h (h = n/gcd(j,n), j=65536)
g = 2**16                      # multiplicity (g = gcd(65536, 2^21) = 2^16)
zeta = 170455089               # element of exact order 32 mod p (zeta^16 = -1)

M_PLUS_EXPECT  = 523523694273046106
M_MINUS_EXPECT = 1853062447130638824

def check_zeta():
    return power_mod(zeta, 32, p) == 1 and power_mod(zeta, 16, p) == p-1

def lattice_minima():
    from sage.modules.free_module_integer import IntegerLattice
    # L = Z(1,zeta,...,zeta^15) + p Z^16 ; rows: b0=(zeta^k), b_k=p e_k (k=1..15)
    B = matrix(ZZ, 16, 16)
    for k in range(16):
        B[0, k] = power_mod(zeta, k, p)
    for k in range(1, 16):
        B[k, k] = p
    detL = B.determinant()
    L = IntegerLattice(B)
    sv = L.shortest_vector()
    Mplus = sv.dot_product(sv)                       # positive alignment (32 - G)
    # M-: closest vector of 2L to p*1 (negative alignment, affine coset 2L - p*1)
    from fpylll import IntegerMatrix, CVP, LLL as fLLL
    B2 = 2*B
    A = IntegerMatrix.from_matrix([[int(B2[i,j]) for j in range(16)] for i in range(16)])
    A = fLLL.reduction(A)
    closest = CVP.closest_vector(A, [int(p)]*16)
    diff = vector(ZZ, [closest[i] - p for i in range(16)])
    Mminus = diff.dot_product(diff)
    return detL, Mplus, Mminus

def deployment_bound(Mplus, Mminus):
    RR = RealField(200)
    r = RR(m)/RR(n-m)
    lam = RR(4)*RR(m)*RR(n-m)/RR(n)**2
    delta = min(RR(16)*RR(Mplus)/RR(p)**2, RR(4)*RR(Mminus)/RR(p)**2)
    # B = (1+r)^n / (r^m C(n,m)); log2 B via lgamma
    log2C = RR(log(binomial(n, m), 2))
    log2B = n*log(RR(1)+r, 2) - m*log(r, 2) - log2C
    # kappa^2 <= B^2 exp(-lam g delta / 2)
    log2_kappa2 = 2*log2B - (lam*RR(g)*delta/RR(2))/log(RR(2))
    return dict(r=r, lam=lam, delta=delta, log2B=log2B, log2_kappa2=log2_kappa2)

def kappa2_crt(pp, hh, gg, mfrac=0.4677):
    # exact CRT-DP kappa^2 = sum_v N_j(v)^2 / C^2 - 1/p for the collapsed statistic (head-depth sanity)
    import numpy as np
    from sympy import prevprime, primitive_root
    from fractions import Fraction as Fr
    nn = hh*gg; jj = gg; mm = round(mfrac*nn)
    ggen = int(primitive_root(pp)); hgen = pow(ggen, (pp-1)//nn, pp)
    roots = [pow(hgen, i, pp) for i in range(nn)]
    syn = [pow(a, jj, pp) for a in roots]
    C = binomial(nn, mm)
    need = 2*int(C).bit_length()+5; mods=[]; x=2**31
    while len(mods)*30 < need: x=int(prevprime(x)); mods.append(x)
    S2mods=[]
    for P in mods:
        dp=[np.zeros(pp,dtype=np.int64) for _ in range(mm+1)]; dp[0][0]=1
        for v in syn:
            for k in range(mm,0,-1): dp[k]=(dp[k]+np.roll(dp[k-1],v))%P
        S2mods.append(int(((dp[mm]**2)%P).sum()%P))
    from math import prod, log2
    Mm=prod(mods); S2=0
    for P,rr in zip(mods,S2mods):
        Mi=Mm//P; S2=(S2+int(rr)*Mi*pow(Mi,-1,P))%Mm
    num=int(S2); den=int(C)*int(C); pi=int(pp)
    k2=Fr(num*pi - den, den*pi)          # = S2/C^2 - 1/p, all Python ints (exact)
    return log2(float(k2))

def main():
    results={}; ok=True
    results['zeta_order_32']= check_zeta(); ok &= results['zeta_order_32']
    detL, Mp, Mm = lattice_minima()
    results['detL_is_p15']= (detL == p**15 or detL == -p**15)
    results['Mplus']=int(Mp); results['Mplus_match']= (Mp==M_PLUS_EXPECT)
    results['Mminus']=int(Mm); results['Mminus_match']= (Mm==M_MINUS_EXPECT)
    ok &= results['detL_is_p15'] and results['Mplus_match'] and results['Mminus_match']
    bd = deployment_bound(Mp, Mm)
    results['delta']=float(bd['delta']); results['lambda']=float(bd['lam'])
    results['log2_B']=float(bd['log2B']); results['log2_kappa2']=float(bd['log2_kappa2'])
    # requirement: kappa^2 <= 2^-82.8 (axis contribution O(1)); we assert the proven bound clears it
    results['clears_requirement']= (bd['log2_kappa2'] <= -82.8); ok &= results['clears_requirement']
    # head-depth CRT-DP sanity (small p, exact); closed-form ladder gives ~ -22.50,-35.33,-60.36 (p=61441)
    ladder={}
    for gg,exp in [(1,-22.50),(2,-35.33),(4,-60.36)]:
        val=kappa2_crt(61441,32,gg); ladder[f'g={gg}']=float(round(val,2))
        ok &= abs(val-exp)<0.1
    results['head_depth_ladder_h32_p61441']=ladder
    report={'status':STATUS,'claim':CLAIM,
            'params':dict(p=int(p),n=int(n),w=int(w),m=int(m),h=int(h),g=int(g)),
            'results':results,'all_passed':bool(ok),
            'timestamp':datetime.now(timezone.utc).isoformat()}
    print(json.dumps(report, indent=2))
    print("\nAXIS BOUND:  log2 kappa^2 <= %.2f   (requirement <= -82.8;  margin %.0f bits)"
          % (results['log2_kappa2'], -82.8 - results['log2_kappa2']))
    print("ALL PASSED:", ok)
    return 0 if ok else 1

if __name__ == "__main__":
    import sys; sys.exit(main())
