#!/usr/bin/env sage
# -*- mode: python -*-
r"""
bridge_probe_directions.sage -- first numerical probe of the "prime-ell frontier = Redei-Szonyi
directions" bridge (see notes/l1/l1_e3_lacunary_directions_connection.md).

Calibration + signal, per frontier witness AND matched random Gamma:
  (1) N_add(Gamma) = # additive directions {(Gamma(a)-Gamma(b))/(a-b)}  -- EXPECTED ~ p
      (Gamma has degree << p, so it is NOT literally the (ell+3)/2 additive-directions extremal;
       this confirms the correspondence is MULTIPLICATIVE/dual, not off-the-shelf additive).
  (2) |V(Gamma)| = value-set size = #{Gamma(x): x in F_p}  -- small value set = classical special class.
  (3) coincidence count C = #{(x,x'): x^ell=x'^ell, x!=x', Gamma(x)=Gamma(x')} = sum_w sum_c f_c(f_c-1),
      and E_3.  These are the objects our bound controls; compare witness vs random.
  (4) does the witness stand out from random Gamma on |V| / C / E_3?  (structural specialness = bridge signal)
"""
WIT = [
    (331,11,[97,29,97,239,171,92,143,155,270,1]),
    (313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
    (103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
]

def analyze(p, ell, gamma, F, Rx, X):
    G = sum(F(gamma[r-1])*X**r for r in range(1,ell))
    gvals = [G(F(a)) for a in range(p)]                 # Gamma on all of F_p
    # (1) additive directions
    dirs = set()
    for a in range(p):
        ga = gvals[a]
        for b in range(a+1, p):
            dirs.add((ga - gvals[b])/F(a-b))
    Nadd = len(dirs)
    # (2) value set
    Vsize = len(set(gvals))
    # (3) coincidence count + E_3 over cosets of mu_ell
    g = F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    C = 0; E3 = 0
    for i in range(n):
        b = g**i; tally={}
        for h in H:
            v = G(b*h); tally[v]=tally.get(v,0)+1
        for f in tally.values(): C += f*(f-1)
        mu = max(tally.values())
        if mu>=3: E3 += mu-2
    return Nadd, Vsize, C, E3

def main():
    import random
    for (p,ell,gm) in WIT:
        F=GF(p); Rx=PolynomialRing(F,'X'); X=Rx.gen()
        Nadd,Vsize,C,E3 = analyze(p,ell,gm,F,Rx,X)
        print("="*84)
        print(" WITNESS ell=%d p=%d  (E_3=%d=ell-2, frontier extremal)" % (ell,p,E3))
        print("   N_add(Gamma) = %d   (p=%d, (ell+3)/2=%d)  -> additive dirs ~ p, NOT literal" % (Nadd,p,(ell+3)//2))
        print("   |value set|  = %d   (p=%d)" % (Vsize,p))
        print("   coincidences C = %d   E_3 = %d" % (C,E3))
        # matched random Gamma (dense, nonzero) for contrast
        rng=random.Random(int(7*ell+p)); rN=[]; rV=[]; rC=[]; rE=[]
        for _ in range(8):
            rg=[rng.randrange(p) for _ in range(ell-1)]
            if not any(rg): continue
            Na,Vs,Cc,Ee = analyze(p,ell,rg,F,Rx,X)
            rN.append(Na); rV.append(Vs); rC.append(Cc); rE.append(Ee)
        import statistics as st
        print("   random Gamma (n=%d): N_add~%d, |V|~%d, C~%.0f, E_3 max=%d"
              % (len(rN), int(st.median(rN)), int(st.median(rV)), st.median(rC), max(rE)))
        print("   witness stands out? |V| smaller: %s ; C larger: %s ; E_3 higher: %s"
              % (Vsize < min(rV), C > max(rC), E3 >= max(rE)))
    print("="*84)
    print(" Read: if the witness has anomalously small |V| / large C / max E_3 vs random,")
    print(" that is structural specialness consistent with the lacunary/small-value-set bridge.")
    return 0

import sys
sys.exit(main())
