#!/usr/bin/env sage
# -*- mode: python -*-
r"""
verify_e3_upper_bound.sage -- directly verify the CORE COMPUTATION of the proof of
  dim(sum_k V_k) <= ell-2   (the upper structural half of the KEY LEMMA E_3 <= ell-2).

Claim being checked (per excess coset / fiber F_k with shared value c_k):
  (1) coset factorization:  g_k * h_k = X^ell - w_k,   g_k = fiber locator, h_k = co-fiber locator.
  (2) fiber-constancy divisibility:  g_k | (Gamma - c_k),  i.e. Gamma = c_k + g_k*q_k,
                                     deg q_k <= (ell-1) - mu_k.
  (3) THE VANISHING:  [X^{ell-1}]( h_k * X^d * Gamma ) = 0   for all d = 0..mu_k-2.
      (=> V_k subset W := ker(A |-> [X^{ell-1}](A*Gamma)), dim W = ell-2, hence
          sum_k V_k subset W and dim(sum V_k) <= ell-2.)
Also reconfirms dim(sum V_k) <= ell-2 and prints dim, E_3.

Proof of (3) (checked here numerically for the witnesses): write Gamma = c_k + g_k q_k. Then
  h_k X^d Gamma = c_k h_k X^d + (X^ell - w_k) q_k X^d.
  * deg(h_k X^d) = (ell-mu_k)+d <= ell-2 < ell-1  => first term contributes 0 to [X^{ell-1}].
  * [X^{ell-1}]((X^ell - w_k) q_k X^d): X^ell-part gives coeff at X^{-1-d}=0; -w_k-part needs
    deg-(ell-1) term of q_k X^d, but deg(q_k X^d) <= (ell-1-mu_k)+(mu_k-2) = ell-3 < ell-1 => 0.
"""

ANCHORS = [
    (11,331,[97,29,97,239,171,92,143,155,270,1]),
    (13,313,[254,289,29,276,242,219,201,261,79,232,133,1]),
    (17,103,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
    (17,409,[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1]),
]

def run():
    all_ok = True
    for (ell,p,gm) in ANCHORS:
        F = GF(p); g = F.multiplicative_generator(); n=(p-1)//ell
        zeta = g**n; H=[zeta**j for j in range(ell)]
        Rx = PolynomialRing(F,'X'); X = Rx.gen()
        Gamma = sum(F(gm[r-1])*X**r for r in range(1,ell))
        rows = []; E3 = 0; K = 0; core_ok = True
        for i in range(n):
            b = g**i; coset=[b*h for h in H]; tally={}
            for x in coset: tally.setdefault(Gamma(x),[]).append(x)
            mu = max(len(v) for v in tally.values())
            if mu < 3: continue
            K += 1; E3 += mu-2
            modal = min((val for val,v in tally.items() if len(v)==mu), key=lambda z:int(z))
            fiber = tally[modal]; fs=set(fiber); cof=[x for x in coset if x not in fs]
            w = b**ell; c = modal
            gk = prod((X-x) for x in fiber)          # fiber locator, deg mu
            hk = prod((X-x) for x in cof)             # co-fiber locator, deg ell-mu
            # (1) coset factorization
            fac_ok = (gk*hk == X**ell - w)
            # (2) fiber-constancy divisibility Gamma - c = g_k q_k
            qk, rem = (Gamma - c).quo_rem(gk)
            div_ok = (rem == 0) and (qk.degree() <= (ell-1) - mu if (Gamma-c)!=0 else True)
            # (3) THE VANISHING [X^{ell-1}](h_k X^d Gamma) = 0 for d=0..mu-2
            vanish_ok = True
            for d in range(mu-1):
                prodpoly = hk * X**d * Gamma
                if prodpoly.degree() >= ell-1:
                    if prodpoly[ell-1] != 0: vanish_ok = False
                # else coeff is 0 trivially
            core_ok = core_ok and fac_ok and div_ok and vanish_ok
            # build V_k rows for the dim check
            for d in range(mu-1):
                poly = hk * X**d
                v = [poly[j] if j <= poly.degree() else F(0) for j in range(ell-1)]
                rows.append(v)
        dimsum = Matrix(F, rows).rank() if rows else 0
        ok = core_ok and (dimsum <= ell-2) and (dimsum >= E3)
        all_ok = all_ok and ok
        print(" ell=%2d p=%3d: K=%d E_3=%d  dim(sumV)=%d  (ell-2=%d)   core[fac&div&VANISH]=%s  "
              "E3<=dim<=ell-2=%s  -> %s"
              % (ell,p,K,E3,dimsum,ell-2, core_ok, (E3<=dimsum<=ell-2), "PASS" if ok else "FAIL"))
    print("="*90)
    print(" RESULT: %s" % ("PROOF CORE VERIFIED on all anchors: V_k subset ker([X^{ell-1}](.*Gamma)), "
                           "so dim(sum V_k) <= ell-2." if all_ok else "A CHECK FAILED — investigate."))
    return 0 if all_ok else 1

import sys
sys.exit(run())
