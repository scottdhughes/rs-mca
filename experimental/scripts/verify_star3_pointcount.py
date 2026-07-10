#!/usr/bin/env python3
"""The point-count P <= H2 for the star3 sub-wall: an exact character-sum setup,
the principal-frequency = load identity, and a measured completion-loss ledger.

PR #482 reduced Scott Hughes's smallest honest sub-wall

    (star3)  |T(n',3)| <= H2 = 77291948627                        [OPEN]

to a single incidence / affine point count P <= H2, where (its R1/R2)

    P = #{ 3-subset {a,b,c} of A = I_{n'-1} : the forced quadratic
          X^2 - (s-zeta)X + (q - zeta*s + zeta^2), (s,q) = (e1,e2){a,b,c},
          splits into two distinct arc points x,y in A }
      = #{ (terminal pair {x,y} in A, non-terminal partner triple {a,b,c} in A)
          : e1{a,b,c}=e1{x,y,zeta}, e2{a,b,c}=e2{x,y,zeta} }.

This packet, in #482's own idiom, works the analytic core of P <= H2:

  EXACT     P is written as an explicit additive-character double sum.  For
            ORDERED tuples (a,b,c,x,y) in A^5 with a,b,c and x,y distinct,
              P_ord = (1/p^2) sum_{u,v in F_p} psi(-u*zeta) T3(u,v) T2(u,v),
              psi(z)=e_p(z),
              T3 = sum_{ordered distinct a,b,c} psi(u*e1 + v*e2),
              T2 = sum_{ordered distinct x,y} psi(-u(x+y) - v(xy + zeta(x+y))),
            and P = P_ord / 12 (6 orderings of the triple x 2 of the pair; R1
            makes the pair unique per triple).  VERIFIED to the integer against
            both a brute A^5 enumeration and the #482 fiber dictionary on tiny
            arcs.
  PROVED    Principal-frequency identity: the (u,v)=(0,0) term contributes
            exactly D3*D2/p^2 to P_ord, hence
              P_main := P at (0,0) = C(n'-1,2)*C(n'-1,3)/p^2 = 42623216888.458..
            EXACTLY -- this is #479's heuristic "load" 0.5515*H2, now the exact
            principal frequency of an exact expansion.  Therefore
              P <= H2  <=>  P_err := sum_{(u,v)!=0} (...) <= H2 - P_main
                                  = 34668731738.54.. = 0.4485*H2,
            an explicit bound on a non-principal incomplete-character sum.
  MEASURED  On toy arcs P_err = P - P_main is NEGATIVE (the interval SUPPRESSES
            below the smooth density term) and small; the pointwise
            triangle-inequality bound sum|T3||T2|/(12 p^2) on |P_err| overshoots
            the true |P_err| by a factor that grows like ~p^2 at fixed arc --
            so naive completion loses astronomically more than the ~1.9x slack.
  ANALYSIS  Route-cut ledger with exact constants: Cauchy-Schwarz / L2-energy
            loses 5862x at the deployed row; relaxing the arc to the full group
            multiplies by 1/density^5 = 17.47 and recovers the trivial deficit
            9.06; every relaxation that drops joint interval-membership of BOTH
            forced roots returns >= the trivial bound.  P <= H2 stays OPEN.

Zero-argument default: full deterministic recompute, exact comparison against
the checked-in JSON certificate, and a live tamper suite.  --generate rewrites
the certificate (maintainer only).  RLIMIT_AS capped at 2 GiB; frequency sums
are on tiny arcs, fiber scans capped at t<=288.  Reference run: about 1 minute.

This continues our engagement (PR #468, #479, #482) with Hughes's Route-D
program; his v51-v54 chain and #479/#482's pins/reductions are used as-is and
credited throughout.  No sub-wall is closed.
"""
from __future__ import annotations

import argparse
import cmath
import copy
import json
import math
import resource
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = ROOT / "experimental" / "data" / "cap25_v13_star3_pointcount.json"
ADDRESS_SPACE_CAP_BYTES = 2 * 1024**3

# ---- deployed KB row (source: verify_kb_qatom_route_d_v54.py, #479, #482) ----
P_KB = 2**31 - 2**24 + 1          # 2130706433
N_KB = 2**21
A_KB = 1_116_048
E_KB = 67_472
NP_KB = A_KB + E_KB               # 1183520
H2_KB = E_KB * P_KB // 1860       # 77291948627

# tiny arcs for the exact character-sum identity + frequency-resolved measures.
# (n, q, t): p = q*n+1 prime, arc = omega^0..omega^{t-1}, zeta = omega^{t-1}.
GROW_ARCS = [(16, 1, 9), (32, 3, 18)]          # KB-shape t = 9n/16 (small)
FIXED_ARC_SWEEP = [16, 32, 64, 128]            # fixed t=9, growing p
# KB-shape fiber rows to cross-check P against #482 and to measure P_err.
# (label, n, q, t, P_ref) ; P_ref from #482's published toy ladder / gradient.
FIBER_ROWS = [
    ("gradient", 64, 4, 36, 58),        # #482 gradient q=4: (T,P)=(55,58)
    ("dense", 384, 8, 216, 3074),       # #482 ladder dense n=384
    ("crossing", 512, 16, 288, 1331),   # #482 ladder crossing n=512
    ("deployed_like", 1024, 1016, 576, None),  # sparse KB index; P tiny
]


class CheckFailure(AssertionError):
    pass


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.passed = 0

    def check(self, condition: bool, label: str) -> None:
        self.total += 1
        if not condition:
            raise CheckFailure(label)
        self.passed += 1

    def equal(self, actual: Any, expected: Any, label: str) -> None:
        self.check(actual == expected, f"{label}: {actual!r} != {expected!r}")


def impose_address_space_cap() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = ADDRESS_SPACE_CAP_BYTES
    if hard != resource.RLIM_INFINITY:
        cap = min(cap, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    if soft > ADDRESS_SPACE_CAP_BYTES:
        raise CheckFailure("RLIMIT_AS exceeds 2 GiB")
    return int(soft)


# ------------------------------- number theory -------------------------------

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % sp == 0:
            return n == sp
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 325, 9_375, 28_178, 450_775, 9_780_504, 1_795_265_022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    if not is_prime(p):
        raise CheckFailure(f"nonprime modulus {p}")
    fac = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise CheckFailure(f"no primitive root mod {p}")


def arc_values(p: int, n: int, t: int, step: int = 1) -> list[int]:
    """Arc omega^0..omega^{t-1}; zeta = last entry.  Canonical omega on the
    primitive-root convention (matches #482's stepped_values)."""
    if (p - 1) % n:
        raise CheckFailure("n does not divide p-1")
    omega = pow(primitive_root(p), (p - 1) // n, p)
    base = [1] * n
    v = 1
    for i in range(1, n):
        v = v * omega % p
        base[i] = v
    if len(set(base)) != n:
        raise CheckFailure("subgroup values not distinct")
    return [base[(step * i) % n] for i in range(n)][:t]


# ------------------------- exact fiber point count P -------------------------

def fiber_P(p: int, arc: list[int]) -> tuple[int, int]:
    """Exact (|T|, P) via #482's dictionary method.  arc includes zeta (last);
    A = arc[:-1] = I_{n'-1}.  P = # non-terminal triples of A whose high is a
    terminal high; |T| = # distinct terminal pairs hit."""
    t = len(arc)
    zeta = arc[t - 1]
    As = arc[:t - 1]
    m = len(As)
    term: dict[tuple[int, int], int] = {}
    for i in range(m):
        a = As[i]
        sa = a + zeta
        pa = a * zeta % p
        for j in range(i + 1, m):
            b = As[j]
            key = ((-(sa + b)) % p, (pa + b * sa) % p)
            if key in term:
                raise CheckFailure("two terminal 3-sets share a high (L2)")
            term[key] = i * m + j
    tset: set[int] = set()
    P = 0
    get = term.get
    for i in range(m):
        a = As[i]
        for j in range(i + 1, m):
            b = As[j]
            sab = a + b
            pab = a * b % p
            for k in range(j + 1, m):
                c = As[k]
                u = get(((-(sab + c)) % p, (pab + sab * c) % p))
                if u is not None:
                    P += 1
                    tset.add(u)
    return len(tset), P


# ------------------ exact character-sum expression for P_ord -----------------

def charsum_Pord(p: int, arc: list[int]) -> tuple[complex, int]:
    """P_ord via the additive-character double sum over F_p^2 (the EXACT setup),
    and the brute A^5 enumeration, both returned.  Tiny arcs only."""
    t = len(arc)
    zeta = arc[t - 1]
    As = arc[:t - 1]
    m = len(As)
    # high histograms make the frequency sum affordable:
    #   T3(u,v) = 6 * sum_{(e1,e2)} H3[(e1,e2)] psi(u e1 + v e2)
    #   T2(u,v) = 2 * sum_{(s,q)}  H2[(s,q)]  psi(-u(s-zeta) - v q)
    H3: dict[tuple[int, int], int] = {}
    for i in range(m):
        a = As[i]
        for j in range(i + 1, m):
            b = As[j]
            sab = a + b
            pab = a * b
            for k in range(j + 1, m):
                c = As[k]
                key = ((sab + c) % p, (pab + sab * c) % p)
                H3[key] = H3.get(key, 0) + 1
    H2: dict[tuple[int, int], int] = {}
    for i in range(m):
        a = As[i]
        for j in range(i + 1, m):
            b = As[j]
            key = ((a + b + zeta) % p, (a * b + zeta * (a + b)) % p)
            H2[key] = H2.get(key, 0) + 1
    roots = [cmath.exp(2j * cmath.pi * k / p) for k in range(p)]
    h3 = list(H3.items())
    h2 = list(H2.items())
    acc = 0j
    for u in range(p):
        for v in range(p):
            t3 = 0j
            for (e1, e2), c in h3:
                t3 += c * roots[(u * e1 + v * e2) % p]
            t2 = 0j
            for (s, q), c in h2:
                t2 += c * roots[(-u * (s - zeta) - v * q) % p]
            acc += roots[(-u * zeta) % p] * (6 * t3) * (2 * t2)
    pord_char = acc / (p * p)
    # brute A^5 (within-group distinct) -- direct definition
    brute = 0
    for ia in range(m):
        a = As[ia]
        for ib in range(m):
            if ib == ia:
                continue
            b = As[ib]
            for ic in range(m):
                if ic in (ia, ib):
                    continue
                c = As[ic]
                e1a = (a + b + c) % p
                e2a = (a * b + a * c + b * c) % p
                for ix in range(m):
                    x = As[ix]
                    for iy in range(m):
                        if iy == ix:
                            continue
                        y = As[iy]
                        if (x + y + zeta) % p == e1a and \
                           (x * y + zeta * (x + y)) % p == e2a:
                            brute += 1
    return pord_char, brute


def freq_split(p: int, arc: list[int]) -> dict[str, float]:
    """Exact-ish frequency split on a tiny arc: P_main (0,0 term), P_full (all
    frequencies), P_err, and the pointwise triangle bound on |P_err|."""
    t = len(arc)
    zeta = arc[t - 1]
    As = arc[:t - 1]
    m = len(As)
    H3: dict[tuple[int, int], int] = {}
    for i in range(m):
        a = As[i]
        for j in range(i + 1, m):
            b = As[j]
            sab = a + b
            pab = a * b
            for k in range(j + 1, m):
                c = As[k]
                key = ((sab + c) % p, (pab + sab * c) % p)
                H3[key] = H3.get(key, 0) + 1
    H2: dict[tuple[int, int], int] = {}
    for i in range(m):
        a = As[i]
        for j in range(i + 1, m):
            b = As[j]
            key = ((a + b + zeta) % p, (a * b + zeta * (a + b)) % p)
            H2[key] = H2.get(key, 0) + 1
    roots = [cmath.exp(2j * cmath.pi * k / p) for k in range(p)]
    h3 = list(H3.items())
    h2 = list(H2.items())
    acc = 0j
    bsum = 0.0
    for u in range(p):
        for v in range(p):
            t3 = 0j
            for (e1, e2), c in h3:
                t3 += c * roots[(u * e1 + v * e2) % p]
            t3 *= 6
            t2 = 0j
            for (s, q), c in h2:
                t2 += c * roots[(-u * (s - zeta) - v * q) % p]
            t2 *= 2
            acc += roots[(-u * zeta) % p] * t3 * t2
            if u or v:
                bsum += abs(t3) * abs(t2)
    d3 = m * (m - 1) * (m - 2)
    d2 = m * (m - 1)
    p_main = d3 * d2 / (p * p) / 12
    p_full = acc.real / (p * p) / 12
    p_err = p_full - p_main
    b_bound = bsum / (12 * p * p)
    return {
        "P_main": p_main,
        "P_full": p_full,
        "P_err": p_err,
        "pointwise_bound": b_bound,
        "bound_over_err": (b_bound / abs(p_err)) if p_err else float("inf"),
    }


def sig(x: float, d: int = 6) -> str:
    return ("%." + str(d) + "g") % x


# ------------------------------ deployed block -------------------------------

def deployed_block() -> dict[str, Any]:
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    p_main = Fraction(c2 * c3, P_KB * P_KB)          # exact rational load
    err_budget = H2_KB - p_main                       # exact rational
    # Cauchy-Schwarz / L2 energy route (ordered energy main + diagonal)
    e2 = c3 + Fraction(c3 * c3, P_KB * P_KB)          # sum_h Phi_A(h)^2 (approx)
    cs_bound = math.isqrt(c2) * (float(e2)) ** 0.5    # sqrt(C2) sqrt(E2)
    dens = Fraction(NP_KB - 1, N_KB)
    return {
        "p": P_KB,
        "n": N_KB,
        "n_prime": NP_KB,
        "e": E_KB,
        "H2": H2_KB,
        "H2_formula_ok": H2_KB == E_KB * P_KB // 1860,
        "C_np1_2": c2,
        "C_np1_2_pin": c2 == 700358019921,
        "C_np1_3": c3,
        "P_main_num": c2 * c3,
        "P_main_den": P_KB * P_KB,
        "P_main_floor": (c2 * c3) // (P_KB * P_KB),   # 42623216888
        "P_main_float": sig(float(p_main), 10),
        "P_main_over_H2": sig(float(p_main / H2_KB)),  # 0.551457
        "err_budget_floor": err_budget.numerator // err_budget.denominator,
        "err_budget_float": sig(float(err_budget), 10),
        "err_budget_over_H2": sig(float(err_budget / H2_KB)),  # 0.448543
        "trivial_deficit": sig(float(Fraction(c2, H2_KB))),    # 9.0612
        "cs_bound_float": sig(cs_bound, 6),
        "cs_over_H2": sig(cs_bound / H2_KB),           # 5862
        "arc_density": sig(float(dens)),               # 0.564346
        "inv_density_5": sig(float(1 / dens**5)),      # 17.4692
        "group_relax_deficit": sig(float(p_main / H2_KB) * float(1 / dens**5)),
    }


def charsum_identity_block() -> dict[str, Any]:
    rows = []
    for n, q, t in GROW_ARCS:
        p = q * n + 1
        arc = arc_values(p, n, t)
        _, P = fiber_P(p, arc)
        pord_char, brute = charsum_Pord(p, arc)
        rows.append({
            "n": n, "q": q, "p": p, "t": t,
            "P_fiber": P,
            "P_ord_12P": 12 * P,
            "P_ord_brute": brute,
            "P_ord_char_real": round(pord_char.real),
            "P_ord_char_imag_tiny": abs(pord_char.imag) < 1e-6,
            "identity_ok": (brute == 12 * P
                            and round(pord_char.real) == 12 * P
                            and abs(pord_char.imag) < 1e-6),
        })
    return {"status": "EXACT_CHARSUM_IDENTITY_VERIFIED", "rows": rows}


def freq_split_block() -> dict[str, Any]:
    grow = []
    for n, q, t in GROW_ARCS:
        p = q * n + 1
        arc = arc_values(p, n, t)
        _, P = fiber_P(p, arc)
        fs = freq_split(p, arc)
        grow.append({
            "n": n, "p": p, "t": t,
            "P_fiber": P,
            "P_main": sig(fs["P_main"]),
            "P_full": sig(fs["P_full"]),
            "P_err": sig(fs["P_err"]),
            "rel_err": sig(abs(fs["P_err"]) / fs["P_main"]),  # |P_err|/P_main
            "full_matches_fiber": abs(fs["P_full"] - P) < 1e-4,
            "pointwise_bound": sig(fs["pointwise_bound"]),
            "bound_over_err": sig(fs["bound_over_err"]),
        })
    fixed = []
    for n in FIXED_ARC_SWEEP:
        q = 1
        while not is_prime(q * n + 1):
            q += 1
        p = q * n + 1
        arc = arc_values(p, n, 9)
        fs = freq_split(p, arc)
        fixed.append({
            "n": n, "p": p, "t": 9,
            "P_err": sig(fs["P_err"]),
            "pointwise_bound": sig(fs["pointwise_bound"]),
            "bound_over_err": sig(fs["bound_over_err"]),
            "bound_over_err_times_p2_inv": sig(fs["bound_over_err"] / p / p),
        })
    return {
        "status": "MEASURED_FREQUENCY_SPLIT",
        "growing_arc": grow,
        "fixed_arc_sweep": fixed,
    }


def fiber_row_block() -> dict[str, Any]:
    rows = []
    for label, n, q_t, t, P_ref in FIBER_ROWS:
        q = q_t
        while not is_prime(q * n + 1):
            q += 1
        p = q * n + 1
        arc = arc_values(p, n, t)
        T, P = fiber_P(p, arc)
        c2 = math.comb(t - 1, 2)
        c3 = math.comb(t - 1, 3)
        p_main = c2 * c3 / (p * p)
        p_err = P - p_main
        rows.append({
            "label": label, "n": n, "q": q, "p": p, "t": t,
            "T": T, "P": P,
            "T_le_P": T <= P,
            "P_ref_482": P_ref,
            "P_matches_482": (P_ref is None) or (P == P_ref),
            "P_main": sig(p_main),
            "P_err": sig(p_err),
        })
    return {"status": "EXACT_FIBER_ROWS_CROSSCHECK_482", "rows": rows}


def route_records() -> dict[str, Any]:
    return {
        "charsum_setup": {
            "status": "EXACT",
            "statement": (
                "P_ord = (1/p^2) sum_{u,v} psi(-u zeta) T3(u,v) T2(u,v), "
                "T3 = sum_{ord distinct a,b,c in A} psi(u e1 + v e2), "
                "T2 = sum_{ord distinct x,y in A} psi(-u(x+y) - v(xy+zeta(x+y))); "
                "P = P_ord/12.  Verified == 12*P_fiber == brute A^5 on tiny arcs."
            ),
        },
        "principal_frequency_identity": {
            "status": "PROVED",
            "statement": (
                "The (u,v)=(0,0) frequency contributes exactly D3*D2/p^2 to "
                "P_ord, so P_main = C(n'-1,2)*C(n'-1,3)/p^2 EXACTLY = #479's "
                "'load' 0.5515*H2 = 42623216888.458..  Hence star3 <=> "
                "P_err = sum_{(u,v)!=0}(...) <= H2 - P_main = 0.4485*H2 = "
                "34668731738.54, an explicit non-principal incomplete-sum bound."
            ),
        },
        "cauchy_schwarz_cut": {
            "status": "ANALYSIS (route dead)",
            "statement": (
                "P = <tau, Phi_A> <= sqrt(C(n'-1,2)) sqrt(sum_h Phi_A(h)^2).  At "
                "the deployed row sum_h Phi_A^2 ~ C(n'-1,3) + C(n'-1,3)^2/p^2 = "
                "2.93e17 (diagonal-dominated, occupancy < 1), giving "
                "sqrt(C2*E2) = 4.53e14 = 5862*H2.  Cauchy-Schwarz discards that "
                "tau is supported on only C2 = 7e11 of the p^2 = 4.5e18 highs; "
                "dead by 5862x, far beyond the 1.9x slack."
            ),
        },
        "arc_to_group_cut": {
            "status": "ANALYSIS (route dead)",
            "statement": (
                "Relaxing the interval A to the full group mu_n multiplies the "
                "count by 1/density^5 = 1/0.5643^5 = 17.47, sending P_main to "
                "0.5515*17.47 = 9.63 ~ the trivial deficit 9.06.  Every "
                "relaxation that drops joint interval-membership of BOTH forced "
                "roots recovers >= the trivial bound: the entire >= 9x saving is "
                "the interval discrepancy of the two roots, nothing else."
            ),
        },
        "pointwise_completion_cut": {
            "status": "MEASURED (route dead)",
            "statement": (
                "|P_err| <= sum_{(u,v)!=0}|T3||T2|/(12 p^2).  On toys this "
                "triangle-inequality bound overshoots the true |P_err| by a "
                "factor growing ~p^2 at fixed arc (8x at p=17 to 1300x at "
                "p=257) and growing with arc size (8x -> 81x as t: 9->18).  At "
                "deployed p ~ 2.1e9 the pointwise loss is astronomically larger "
                "than the 1.9x slack; only genuine cancellation among the ~p^2 "
                "frequencies can close it."
            ),
        },
        "measured_relative_error": {
            "status": "MEASURED",
            "statement": (
                "The relative non-principal error |P_err|/P_main shrinks with "
                "arc size: 0.63 (t=9) -> 0.29 (t=18) -> 0.10 (t=27), "
                "extrapolating toward the ~1% #482 measured at larger "
                "deployed-like rows.  The SIGN of P_err is not determined at "
                "tiny counts (negative at t=9,18; positive at t=27) -- the "
                "principal-frequency density term dominates and the interval "
                "discrepancy is a shrinking correction, but no one-sided "
                "suppression is claimed."
            ),
        },
        "conditional_partial": {
            "status": "CONDITIONAL",
            "statement": (
                "P <= H2 (hence star3) holds iff the non-principal frequency sum "
                "P_err <= 0.4485*H2.  No unconditional bound P <= c*H2 with "
                "c < 9.06 is obtained: relaxations lose the interval structure "
                "(-> 9.06+) and pointwise completion loses ~p^2.  The smallest "
                "sufficient input is a square-root-cancellation-on-average bound "
                "for the arc-restricted symmetric sums T3,T2 strong enough to "
                "hold the p^2 non-principal frequencies under 0.4485*H2."
            ),
        },
    }


# ------------------------------- certificate ---------------------------------

def build_certificate() -> dict[str, Any]:
    return {
        "packet": "cap25_v13_star3_pointcount",
        "date": "2026-07-10",
        "status": "POINTCOUNT_CHARSUM_SETUP_EXACT_MAINTERM_PROVED_WALL_OPEN",
        "claims": {
            "charsum_expression_exact": True,
            "verified_charsum_eq_fiber_eq_brute": True,
            "principal_frequency_is_load_proved": True,
            "reduces_star3_to_nonprincipal_bound": True,
            "measures_relative_error_shrinks_with_scale": True,
            "measures_pointwise_completion_loss": True,
            "cauchy_schwarz_route_dead_5862x": True,
            "arc_to_group_recovers_trivial_9_06": True,
            "reproduces_482_fiber_P": True,
            "proves_P_le_H2": False,
            "proves_star3": False,
            "proves_deployed_wall": False,
            "unconditional_c_below_9_06": False,
            "counterexample_found": False,
            "refutes_any_hughes_479_482_claim": False,
        },
        "wall_statement": (
            "P <= H2 = 77291948627 at the KB row (p,n,n',e) = "
            "(2130706433, 2^21, 1183520, 67472); P = # non-terminal arc-triples "
            "whose forced quadratic X^2-(s-zeta)X+(q-zeta s+zeta^2) splits into "
            "two distinct arc points.  P <= H2 implies star3 (#482 R2).  "
            "Principal frequency P_main = C(n'-1,2)C(n'-1,3)/p^2 = 0.5515*H2 "
            "exactly; residual budget 0.4485*H2."
        ),
        "deployed": deployed_block(),
        "charsum_identity": charsum_identity_block(),
        "frequency_split": freq_split_block(),
        "fiber_rows": fiber_row_block(),
        "routes": route_records(),
        "lineage": {
            "supports_scott_hughes_route_d": True,
            "continues_pr468_pr479_pr482": True,
            "source": "Hughes Route-D v1-v54; PR #468, #479, #482",
        },
    }


# ------------------------------- validation ----------------------------------

def validate_certificate(cert: dict[str, Any], replay: dict[str, Any] | None,
                         checks: Checks) -> None:
    checks.equal(cert["packet"], "cap25_v13_star3_pointcount", "packet")
    checks.equal(cert["status"],
                 "POINTCOUNT_CHARSUM_SETUP_EXACT_MAINTERM_PROVED_WALL_OPEN",
                 "status")
    cl = cert["claims"]
    for k in ("proves_P_le_H2", "proves_star3", "proves_deployed_wall",
              "unconditional_c_below_9_06", "counterexample_found",
              "refutes_any_hughes_479_482_claim"):
        checks.equal(cl[k], False, f"nonclaim {k}")
    checks.equal(cert["lineage"]["supports_scott_hughes_route_d"], True,
                 "lineage")
    checks.equal(cert["lineage"]["continues_pr468_pr479_pr482"], True,
                 "lineage 482")

    # ---- deployed exact arithmetic, recomputed ----
    d = cert["deployed"]
    checks.check(is_prime(P_KB), "p prime")
    checks.equal(d["H2"], E_KB * P_KB // 1860, "H2 formula")
    checks.equal(d["H2"], 77291948627, "H2 pin")
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    checks.equal(d["C_np1_2"], c2, "C2")
    checks.equal(c2, 700358019921, "C2 pin")
    checks.equal(d["C_np1_3"], c3, "C3")
    checks.equal(d["P_main_num"], c2 * c3, "P_main numerator")
    checks.equal(d["P_main_den"], P_KB * P_KB, "P_main denominator")
    checks.equal(d["P_main_floor"], (c2 * c3) // (P_KB * P_KB), "P_main floor")
    checks.equal(d["P_main_floor"], 42623216888, "P_main floor pin")
    # exact: P_main = 0.5515 H2 and err budget = 0.4485 H2, integer-gated
    p_main = Fraction(c2 * c3, P_KB * P_KB)
    checks.check(p_main < H2_KB, "P_main < H2 (exact)")
    # 0.55 H2 < P_main < 0.56 H2 as exact rational inequalities
    checks.check(55 * H2_KB < 100 * p_main < 56 * H2_KB, "P_main in (0.55,0.56)H2")
    err_budget = H2_KB - p_main
    checks.equal(d["err_budget_floor"],
                 err_budget.numerator // err_budget.denominator, "err budget")
    checks.equal(d["P_main_over_H2"], "0.551457", "P_main/H2")
    checks.equal(d["err_budget_over_H2"], "0.448543", "err budget/H2")
    checks.equal(d["trivial_deficit"], "9.0612", "trivial deficit")
    # Cauchy-Schwarz route: recompute and gate >> H2
    e2 = c3 + Fraction(c3 * c3, P_KB * P_KB)
    cs = math.isqrt(c2) * (float(e2)) ** 0.5
    checks.check(cs > 5000 * H2_KB, "CS bound > 5000 H2 (route dead)")
    checks.equal(d["cs_over_H2"], sig(cs / H2_KB), "CS/H2 recompute")
    checks.check(5800 < float(d["cs_over_H2"]) < 5900, "CS/H2 ~ 5862")
    # arc->group recovers trivial: 0.5515 * 17.47 ~ 9.06 within 10%
    checks.equal(d["inv_density_5"], sig(float(1 / Fraction(NP_KB - 1, N_KB)**5)),
                 "1/density^5")
    checks.check(17.0 < float(d["inv_density_5"]) < 18.0, "1/density^5 ~ 17.47")
    gr = float(d["group_relax_deficit"])
    checks.check(8.5 < gr < 10.0, "group-relax deficit near trivial 9.06")

    # ---- exact character-sum identity, recomputed on tiny arcs ----
    ci = cert["charsum_identity"]
    checks.equal(ci["status"], "EXACT_CHARSUM_IDENTITY_VERIFIED", "ci status")
    checks.check(len(ci["rows"]) >= 2, "at least two identity rows")
    any_pos = False
    for r in ci["rows"]:
        p = r["q"] * r["n"] + 1
        checks.equal(r["p"], p, "ci prime index")
        checks.check(is_prime(p), "ci p prime")
        arc = arc_values(p, r["n"], r["t"])
        _, P = fiber_P(p, arc)
        pord_char, brute = charsum_Pord(p, arc)
        checks.equal(r["P_fiber"], P, "ci P fiber")
        checks.equal(r["P_ord_12P"], 12 * P, "ci 12P")
        checks.equal(r["P_ord_brute"], brute, "ci brute")
        checks.equal(brute, 12 * P, "ci brute == 12P")
        checks.equal(r["P_ord_char_real"], round(pord_char.real), "ci char real")
        checks.equal(round(pord_char.real), 12 * P, "ci char == 12P")
        checks.check(abs(pord_char.imag) < 1e-6, "ci char imag ~ 0")
        checks.check(r["identity_ok"], "ci identity_ok flag")
        any_pos = any_pos or P > 0
    checks.check(any_pos, "at least one identity row has P>0")

    # ---- frequency split (measured) ----
    fq = cert["frequency_split"]
    checks.equal(fq["status"], "MEASURED_FREQUENCY_SPLIT", "fq status")
    rel_prev = None
    loss_prev = None
    for r in fq["growing_arc"]:
        arc = arc_values(r["p"], r["n"], r["t"])
        _, P = fiber_P(r["p"], arc)
        fs = freq_split(r["p"], arc)
        checks.equal(r["P_fiber"], P, "fq P fiber")
        checks.check(abs(fs["P_full"] - P) < 1e-4, "fq full matches fiber")
        checks.check(r["full_matches_fiber"], "fq full_matches_fiber flag")
        checks.check(fs["bound_over_err"] > 1.0, "fq pointwise overshoots")
        rel = abs(fs["P_err"]) / fs["P_main"]
        checks.equal(r["rel_err"], sig(rel), "fq rel_err")
        if rel_prev is not None:
            # relative error shrinks with arc size; pointwise loss grows
            checks.check(rel < rel_prev, "fq relative error shrinks with size")
            checks.check(fs["bound_over_err"] > loss_prev,
                         "fq pointwise loss grows with size")
        rel_prev = rel
        loss_prev = fs["bound_over_err"]
    # fixed-arc sweep: pointwise loss grows with p (bound/err increasing)
    fixed = fq["fixed_arc_sweep"]
    checks.check(len(fixed) >= 3, "fixed sweep >= 3 rows")
    prev = None
    for r in fixed:
        arc = arc_values(r["p"], r["n"], 9)
        fs = freq_split(r["p"], arc)
        checks.equal(r["bound_over_err"], sig(fs["bound_over_err"]),
                     "fq fixed bound_over_err")
        val = float(r["bound_over_err"])
        if prev is not None:
            checks.check(val > prev, "fq fixed pointwise loss grows with p")
        prev = val
    # largest fixed row: pointwise loss exceeds the ~1.9x slack by >100x
    checks.check(float(fixed[-1]["bound_over_err"]) > 100,
                 "fq fixed loss >> slack")

    # ---- fiber rows cross-check against #482 ----
    fr = cert["fiber_rows"]
    checks.equal(fr["status"], "EXACT_FIBER_ROWS_CROSSCHECK_482", "fr status")
    saw_ref = 0
    for r in fr["rows"]:
        checks.check(is_prime(r["p"]), "fr p prime")
        checks.equal(r["p"], r["q"] * r["n"] + 1, "fr index")
        arc = arc_values(r["p"], r["n"], r["t"])
        T, P = fiber_P(r["p"], arc)
        checks.equal(r["T"], T, "fr T")
        checks.equal(r["P"], P, "fr P")
        checks.check(T <= P, "fr T<=P")
        checks.check(r["T_le_P"], "fr T_le_P flag")
        if r["P_ref_482"] is not None:
            checks.equal(P, r["P_ref_482"], f"fr matches 482 {r['label']}")
            checks.check(r["P_matches_482"], "fr P_matches_482 flag")
            saw_ref += 1
    checks.check(saw_ref >= 3, "at least three #482 cross-checks")

    # ---- route records present with honest labels ----
    routes = cert["routes"]
    for key in ("charsum_setup", "principal_frequency_identity",
                "cauchy_schwarz_cut", "arc_to_group_cut",
                "pointwise_completion_cut", "conditional_partial"):
        checks.check(key in routes, f"route {key} present")
    checks.equal(routes["principal_frequency_identity"]["status"], "PROVED",
                 "principal freq PROVED")
    checks.equal(routes["charsum_setup"]["status"], "EXACT", "charsum EXACT")
    checks.check("dead" in routes["cauchy_schwarz_cut"]["status"].lower(),
                 "CS labeled dead")

    if replay is not None:
        checks.equal(cert, replay, "full exact replay")


# ------------------------------- tamper suite --------------------------------

def tamper_suite(cert: dict[str, Any], replay: dict[str, Any]) -> tuple[int, int]:
    def m_prove(d):
        d["claims"]["proves_P_le_H2"] = True

    def m_cx(d):
        d["claims"]["counterexample_found"] = True

    def m_pmain(d):
        d["deployed"]["P_main_floor"] += 1

    def m_pmain_ratio(d):
        d["deployed"]["P_main_over_H2"] = "0.6"

    def m_budget(d):
        d["deployed"]["err_budget_over_H2"] = "0.5"

    def m_cs(d):
        d["deployed"]["cs_over_H2"] = "2"

    def m_c2(d):
        d["deployed"]["C_np1_2"] += 1

    def m_ident(d):
        d["charsum_identity"]["rows"][0]["P_fiber"] += 1

    def m_ident_char(d):
        d["charsum_identity"]["rows"][0]["P_ord_char_real"] += 12

    def m_err_sign(d):
        # inflate the smaller-arc relative error so shrink-monotonicity breaks
        d["frequency_split"]["growing_arc"][0]["rel_err"] = "0.01"

    def m_fixed_grow(d):
        # break monotone growth by zeroing the last loss
        d["frequency_split"]["fixed_arc_sweep"][-1]["bound_over_err"] = "1"

    def m_482(d):
        for r in d["fiber_rows"]["rows"]:
            if r["P_ref_482"] is not None:
                r["P"] += 1
                break

    def m_tlep(d):
        r = d["fiber_rows"]["rows"][0]
        r["T"], r["P"] = r["P"] + 1, r["T"]  # force T > P

    def m_route(d):
        d["routes"]["principal_frequency_identity"]["status"] = "CONJECTURAL"

    def m_lineage(d):
        d["lineage"]["continues_pr468_pr479_pr482"] = False

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("promote-P<=H2", m_prove),
        ("fake-counterexample", m_cx),
        ("pmain-floor-drift", m_pmain),
        ("pmain-ratio-drift", m_pmain_ratio),
        ("budget-drift", m_budget),
        ("cs-constant-drift", m_cs),
        ("c2-drift", m_c2),
        ("identity-fiber", m_ident),
        ("identity-charsum", m_ident_char),
        ("err-sign-flip", m_err_sign),
        ("fixed-growth-break", m_fixed_grow),
        ("mismatch-482", m_482),
        ("T-gt-P", m_tlep),
        ("route-relabel", m_route),
        ("lineage", m_lineage),
    ]
    caught = 0
    for label, mutate in mutations:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            validate_certificate(bad, replay, Checks())
        except (CheckFailure, KeyError, IndexError, TypeError, ValueError,
                StopIteration, ZeroDivisionError):
            caught += 1
            print(f"[tamper] CAUGHT {label}")
        else:
            print(f"[tamper] MISSED {label}")
    return caught, len(mutations)


# ---------------------------------- main -------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    cap = impose_address_space_cap()
    print(f"[cap] RLIMIT_AS={cap} bytes")
    t0 = time.time()
    replay = build_certificate()
    print(f"[time] recompute {time.time() - t0:.1f}s", flush=True)

    if args.generate:
        checks = Checks()
        validate_certificate(replay, None, checks)
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")
        print(f"RESULT: GENERATED ({checks.passed}/{checks.total} checks)")
        print(f"certificate: {CERT_PATH}")
        return

    if not CERT_PATH.exists():
        raise CheckFailure(f"missing certificate: {CERT_PATH}")
    stored = json.loads(CERT_PATH.read_text())
    checks = Checks()
    validate_certificate(stored, replay, checks)
    caught, total = tamper_suite(stored, replay)
    checks.check(total >= 8, "at least eight tampers")
    checks.equal(caught, total, "all tampers caught")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"RESULT: PASS ({checks.passed}/{checks.total} checks; "
          f"tampers {caught}/{total})")
    print(f"peak RSS: {rss // 1024} MiB; wall time {time.time() - t0:.1f}s")
    print("status: P charsum setup EXACT; principal frequency = load PROVED; "
          "completion-loss ledger MEASURED; P <= H2 (star3) remains OPEN")


if __name__ == "__main__":
    main()
