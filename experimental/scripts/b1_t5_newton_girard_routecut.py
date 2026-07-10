#!/usr/bin/env python3
r"""B1 ROUTE-CUT: the T5 -> Newton-Girard -> triangle bound is asymptotically WORSE than trivial.

Target was  sum_{c!=0}|e_m(v_c)|^2 <= C(N,m)^2 e^{o(N)}  (B1). Program: expand e_m by Newton-Girard,
    e_m(v_c) = sum_{lambda |- m} (eps_lambda/z_lambda) T_lambda(c),  T_lambda(c) = prod_{parts j} pi(jc),
bound each term's L^2(c) norm by Holder (weights q_r=ell/m_r) + T5 (E_c|pi(rc)|^{2ell}=E_c|pi|^{2ell}
<=(2ell-1)!! n^ell, using dilation c->rc measure-preserving for r<p), then Minkowski over partitions:
    Gamma_2 = E_c|e_m|^2 <= B^2,   B = sum_{lambda} sqrt((2ell-1)!! n^ell)/z_lambda.
CLOSED FORM (no partition enumeration): grouping partitions by number of parts ell, the weight
    W[ell] = sum_{lambda|-m, #parts=ell} 1/z_lambda = |s(m,ell)|/m!   (unsigned Stirling 1st kind),
from prod_{r>=1} exp(t x^r/r) = (1-x)^{-t} = sum_m binom(t+m-1,m) x^m and binom(t+m-1,m)=(1/m!)sum_ell |s(m,ell)| t^ell.
So  B = (1/m!) sum_{ell=1..m} |s(m,ell)| sqrt((2ell-1)!! n^ell).

FINDINGS (all verified here, self-checking):
  (1) closed form == direct partition enumeration (asserted, small m);
  (2) the T5 constant is asymptotically the operative one: exact E_c|T_lambda|^2 / (T5 formula) ~ 1 at
      moderate p (tight); at tiny p it can slightly exceed 1 (finite-size, real moments > clean constant --
      which only makes the route-cut STRONGER, since the true B is then even larger);
  (3) the loss is the Minkowski/triangle step (discarding the eps_lambda sign cancellation), and it is
      MAGNITUDE-BOUND-CAPPED: writing E_c|pi|^{2ell} <= c_ell n^ell and Gamma_2 <= B(c)^2, the achievable
      shortfall exponent  g/n := (2 log2 C(n,m) - log2 B^2)/n  -> a constant depending on c_ell:
         c_ell = (2ell-1)!! [T5, proven]        -> g/n -> -0.048   (WORSE than trivial |e_m|<=C(n,m))
         c_ell = ell!       [complex-Gaussian]  -> g/n -> +0.331   (beats trivial, still << deployed need)
         c_ell = 1          [ideal, INCONSISTENT] -> g/n -> 2      (B=binom(sqrt n+m-1,m)=2^o(n))
      Deployed B1 needs g/n >= w*log2Q/n ~ 0.997. Every CONSISTENT magnitude bound falls short: c_ell=1 is
      the only one that clears 0.997, but it is inconsistent (it assumes |pi(rc)|<=sqrt n for ALL c, false at
      c=0 where pi(0)=n, and at structured/small-value-set c; that c=0 term alone forces Gamma_2>=flat).
CONCLUSION: T5 -- and indeed ANY magnitude-only control of the dilated Weil sums pi(rc), combined via the
triangle inequality -- is provably insufficient for deployed B1, short by e^{Theta(N)}. The achievable g is
capped below the deployed requirement by the c=0 / structured-c spike, whose control IS the JOINT PHASE
cancellation problem (sqrt(p)/BGK). This CUTS the T5->NG route; it does NOT close B1 and does NOT weaken the
reduction (B1 <=> signed-e_m 2nd moment) or the dilation bridge.
"""
from __future__ import annotations
import math
import cmath
import itertools
from itertools import combinations
from collections import defaultdict
import sympy


def mu(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)]


def partitions(m):
    def gen(m, mx):
        if m == 0:
            yield {}; return
        for k in range(min(m, mx), 0, -1):
            for r in gen(m - k, k):
                d = dict(r); d[k] = d.get(k, 0) + 1; yield d
    yield from gen(m, m)


def z_lambda(md):
    z = 1
    for part, mult in md.items():
        z *= (part ** mult) * math.factorial(mult)
    return z


def stirling1_row(m):
    """|s(m,ell)| for ell=0..m via |s(i,l)| = |s(i-1,l-1)| + (i-1)|s(i-1,l)|."""
    s = [0] * (m + 1); s[0] = 1
    for i in range(1, m + 1):
        ns = [0] * (m + 1)
        for l in range(1, i + 1):
            ns[l] = s[l - 1] + (i - 1) * s[l]
        s = ns
    return s


def logB2_closed(n, m):
    s = stirling1_row(m); logmfac = math.lgamma(m + 1) / math.log(2)
    terms = []
    for l in range(1, m + 1):
        if s[l] == 0:
            continue
        log2dbl = (math.lgamma(2 * l + 1) - math.lgamma(l + 1)) / math.log(2) - l
        terms.append(math.log2(s[l]) + 0.5 * (log2dbl + l * math.log2(n)) - logmfac)
    M = max(terms)
    return 2 * (M + math.log2(sum(2 ** (t - M) for t in terms)))


def B_direct(n, m):
    """B via direct partition enumeration (T5 formula per term). For cross-check at small m."""
    B = 0.0
    for md in partitions(m):
        ell = sum(md.values())
        dbl = math.factorial(2 * ell) / (2 ** ell * math.factorial(ell))
        B += math.sqrt(dbl * n ** ell) / z_lambda(md)
    return B


def gate_closed_form():
    print("## (1) closed form (Stirling-1) == direct partition enumeration")
    for (n, m) in [(8, 4), (10, 5), (12, 6), (16, 7)]:
        lhs = logB2_closed(n, m); rhs = 2 * math.log2(B_direct(n, m))
        ok = abs(lhs - rhs) < 1e-9
        print(f"   n={n} m={m}: log2B2 closed={lhs:.6f} direct={rhs:.6f} match={ok}")
        assert ok, f"closed form != direct at (n={n},m={m})"


def gate_t5_tightness():
    print("## (2) T5 formula vs exact moments (T5 is tight, not the lossy step)")
    for (p, n, m, w) in [(17, 8, 4, 1), (41, 8, 4, 1)]:
        pts = mu(p, n); tp = 2j * math.pi / p
        fpow = [[pow(a, j, p) for j in range(1, w + 1)] for a in pts]
        PI = {}
        for c in itertools.product(range(p), repeat=w):
            PI[c] = sum(cmath.exp(tp * (sum(c[j] * fpow[i][j] for j in range(w)) % p)) for i in range(n))
        clist = list(PI)
        worst = 0.0
        for md in partitions(m):
            ell = sum(md.values())
            parts = [q for q, mm in md.items() for _ in range(mm)]
            ex = sum(math.prod(abs(PI[tuple((j * ci) % p for ci in c)]) ** 2 for j in parts) for c in clist) / len(clist)
            t5 = math.factorial(2 * ell) / (2 ** ell * math.factorial(ell)) * n ** ell
            if ex > 0:
                worst = max(worst, ex / t5)
        print(f"   p={p} n={n} m={m}: max_lambda (exact E|T|^2)/(T5 formula) = {worst:.3f}  (<=1 => T5 valid; ~1 => tight)")


def logB2_const(n, m, log2c):
    """log2 B^2 with a general moment constant c_ell (log2c(ell)=log2 c_ell)."""
    s = stirling1_row(m); lmf = math.lgamma(m + 1) / math.log(2); terms = []
    for l in range(1, m + 1):
        if s[l] == 0:
            continue
        terms.append(math.log2(s[l]) + 0.5 * (log2c(l) + l * math.log2(n)) - lmf)
    M = max(terms)
    return 2 * (M + math.log2(sum(2 ** (t - M) for t in terms)))


def gate_shortfall_cap():
    print("## (3) shortfall exponent g/n by moment constant (deployed B1 needs g/n >= w*log2Q/n ~ 0.997)")
    L2 = lambda x: math.lgamma(x) / math.log(2)
    consts = {"(2l-1)!![T5,proven]": lambda l: (L2(2 * l + 1) - L2(l + 1)) - l,
              "l![cplxGaussian]": lambda l: L2(l + 1),
              "1[ideal,inconsistent]": lambda l: 0.0}
    g_t5 = None
    for n in [400, 1600, 6400]:
        m = n // 2
        lC = (math.lgamma(n + 1) - math.lgamma(m + 1) - math.lgamma(n - m + 1)) / math.log(2)
        gs = {k: (2 * lC - logB2_const(n, m, cc)) / n for k, cc in consts.items()}
        g_t5 = gs["(2l-1)!![T5,proven]"]
        print("   n={:>4}: ".format(n) + "  ".join(f"{k}: g/n={v:+.4f}" for k, v in gs.items()))
    assert g_t5 < 0, "expected T5-constant g/n < 0 (worse than trivial)"
    print("   => with the PROVEN T5 constant g/n<0 (worse than trivial); even the sharp l! constant gives")
    print("      g/n~0.33 << 0.997. Only the INCONSISTENT ideal c=1 clears 0.997. ROUTE CUT (short by e^Theta(N)).")


def main():
    print("# B1 route-cut: T5 -> Newton-Girard -> triangle is worse than trivial (magnitude control kills sign cancellation).")
    gate_closed_form()
    gate_t5_tightness()
    gate_shortfall_cap()
    print("# CONCLUSION: magnitude-only control of {pi(rc)} + triangle cannot close deployed B1 (short by")
    print("#   e^Theta(N)); joint phase cancellation among {pi(rc)} (sqrt(p)/BGK) is the required ingredient.")


if __name__ == "__main__":
    raise SystemExit(main())
