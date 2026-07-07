#!/usr/bin/env python3
"""VERIFY the pigeonhole approximate-freeze refutation of the n^0.81 spectral target -- and push its logic.

Model round: non-constructive f (difference of two same-box polynomials) with |f(x)|_p <= ceil(p/15) on all
of H = G_19 => A_H >= 2^19 cos(2pi/15) = 478,961 = n^0.8986 > n^0.81. Verify every arithmetic step:
 (V1) injectivity dims: r = |Jodd| = (w+1)/2; deg <= w < 2^19 => eval on R (2^18 pair-reps) injective.
 (V2) pigeonhole: 15^(2^18) < p^r  (bits).
 (V3) cosine/lower-bound arithmetic: W = ceil(p/15), A_H >= M cos(2 pi W / p), exponent of 478,961.
 (V4) G_20 worst-case impossibility: Q^(2^19) < p^r forces Q <= 3, cos(2pi/3) < 0 -- no worst-case guarantee.
PUSH (our analysis):
 (P1) AVERAGE-case coherence: typical same-box difference ~ triangular on [-W,W]; E[cos(2pi D/p)] =
      sinc^2(pi/Q). For G_20 at Q=3 (bits: 2^19 * log2(3) < r log2 p ?): E[cos]=sinc^2(pi/3)=0.684 =>
      HEURISTIC pi_odd ~ 0.684*2^20 = n^0.926 > n^0.905 -- the T15 SUP TARGET is heuristically dead too.
 (P2) MEASURE-TININESS (the escape): freeze-family c are ~2^(r log2 p - m log2 Q) pigeonhole classes; their
      contribution to the s-moment (s = n/4) is #freeze * (V/n)^s * n^-3 relative to target -- compute the
      exponent; if hugely negative, SP in its LARGE-VALUES form (round a) survives the freeze families.
"""
from __future__ import annotations
import math

P = 2**31 - 2**24 + 1
K = 21
N = 1 << K
W_DEG = 67471
R_DIM = (W_DEG + 1) // 2          # 33736

log2p = math.log2(P)

def bits(x_count, log2_base, mult):
    return mult * log2_base

def main():
    print(f"# p = {P}, n = 2^{K}, w = {W_DEG}, r = |Jodd| = {R_DIM}, log2 p = {log2p:.4f}")
    coeff_bits = R_DIM * log2p
    print(f"# coefficient-space bits: r log2 p = {coeff_bits:,.0f}")

    # V1 injectivity
    print(f"\n(V1) injectivity: deg w = {W_DEG} < 2^19 = {1<<19}? {W_DEG < (1<<19)}  "
          f"(odd f zero on R => zero on H = 2^19 points > deg => f = 0). r = {R_DIM} <= |R| = 2^18 = {1<<18}: {R_DIM <= 1<<18}")

    # V2 pigeonhole at G_19, Q = 15
    m19 = 1 << 18
    pat_bits = m19 * math.log2(15)
    print(f"(V2) pigeonhole G_19 Q=15: pattern bits = 2^18 log2 15 = {pat_bits:,.0f} < {coeff_bits:,.0f}? "
          f"{pat_bits < coeff_bits}  (margin {coeff_bits - pat_bits:,.0f} bits; model said 21,266)")

    # V3 cosine arithmetic
    W = -(-P // 15)
    ang = 2 * math.pi * W / P
    M19 = 1 << 19
    lower = M19 * math.cos(ang)
    print(f"(V3) W = ceil(p/15) = {W:,}; angle = {math.degrees(ang):.2f} deg; cos = {math.cos(ang):.6f}; "
          f"A_H >= {lower:,.1f} (model: 478,960.9)")
    print(f"     exponent: log_n({lower:.0f}) = {math.log(lower)/math.log(N):.5f} (model 0.89855); "
          f"n^0.81 = {N**0.81:,.0f} -> REFUTED by factor {lower/N**0.81:.2f}x: {lower > N**0.81}")
    print(f"     vs T15 target n^0.905 = {N**0.905:,.0f}: guaranteed construction UNDER it? {lower < N**0.905} "
          f"(margin {N**0.905/lower:.4f}x)")

    # V4 G_20 worst-case impossibility
    m20 = 1 << 19
    qmax_bits = coeff_bits / m20
    print(f"(V4) G_20: log2 Q < r log2 p / 2^19 = {qmax_bits:.4f} => Q <= {int(2**qmax_bits)}; "
          f"Q=3: cos(2pi/3) = {math.cos(2*math.pi/3):.2f} < 0 -> no WORST-case guarantee (model correct); "
          f"Q=4 bits {2*m20:,.0f} > {coeff_bits:,.0f}? {2*m20 > coeff_bits}")

    # P1 average-case coherence on G_20 at Q=3
    q3_bits = m20 * math.log2(3)
    sinc = lambda z: math.sin(z)/z
    Ecos3 = sinc(math.pi/3) ** 2
    heur20 = Ecos3 * (1 << 20)
    print(f"\n(P1) AVERAGE-case G_20 Q=3: bits = 2^19 log2 3 = {q3_bits:,.0f} < {coeff_bits:,.0f}? {q3_bits < coeff_bits}")
    print(f"     E[cos] = sinc^2(pi/3) = {Ecos3:.4f} => HEURISTIC pi_odd ~ {heur20:,.0f} = n^{math.log(heur20)/math.log(N):.4f}")
    print(f"     vs n^0.905 = {N**0.905:,.0f}: heuristically ABOVE T15 sup target? {heur20 > N**0.905}")
    Ecos15 = sinc(math.pi/15) ** 2
    heur19 = Ecos15 * (1 << 19)
    print(f"     (avg-case G_19 Q=15: E[cos] = {Ecos15:.4f} => ~{heur19:,.0f} = n^{math.log(heur19)/math.log(N):.4f}, "
          f"still under n^0.905? {heur19 < N**0.905})")

    # P2 measure-tininess: freeze family's contribution to the s-moment
    s = N // 4
    # generous overcount of freeze-family size: all pigeonhole classes ~ 2^(coeff_bits - pat_bits) diffs
    #   (even p^r as an absurd upper bound changes nothing at these scales)
    freeze_bits = coeff_bits - pat_bits            # ~21K bits (G_19 count); use also coeff_bits as ceiling
    V_exp = 0.926                                   # worst heuristic extremal exponent
    # contribution exponent (bits): freeze_bits + s * V_exp * K  vs target bits: s*K + 3*K
    contrib = freeze_bits + s * V_exp * K
    target = s * K + 3 * K
    print(f"\n(P2) s = n/4 = 2^{int(math.log2(s))}; freeze-family count <= 2^{freeze_bits:,.0f} (ceiling 2^{coeff_bits:,.0f})")
    print(f"     moment contribution bits {contrib:,.0f} vs target bits {target:,.0f} -> margin "
          f"{target - contrib:,.0f} bits ({'NEGLIGIBLE contribution, SP-large-values SURVIVES' if contrib < target else 'PROBLEM'})")
    contrib_ceiling = coeff_bits + s * V_exp * K
    print(f"     even with count = p^r: {contrib_ceiling:,.0f} vs {target:,.0f} -> margin {target - contrib_ceiling:,.0f} bits "
          f"({'still fine' if contrib_ceiling < target else 'fails'})")

if __name__ == "__main__":
    raise SystemExit(main())
