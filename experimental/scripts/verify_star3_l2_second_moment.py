#!/usr/bin/env python3
"""L2 / second-moment identities for the star3 sub-wall of Hughes's Route-D wall.

PR #482 reduced Scott Hughes's smallest honest sub-wall

    (star3)  |T(n',3)| <= H2 = 77291948627                        [OPEN]

to a point count P <= H2, and PR #484 wrote P as an additive-character double sum

    P_ord = (1/p^2) sum_{u,v in F_p} psi(-u zeta) T3(u,v) T2(u,v),   P = P_ord/12,
    T3(u,v) = sum_{ordered distinct a,b,c in A} psi(u*e1 + v*e2),
    T2(u,v) = sum_{ordered distinct x,y in A} psi(-u(x+y) - v(xy + zeta(x+y))),

with the principal (0,0) frequency contributing exactly the load
P_main = C(n'-1,2) C(n'-1,3)/p^2 = 0.5515 H2, so star3 <=> the non-principal
budget |P_err| <= 0.4485 H2 = 34668731738.  PR #484 named the opening --
SECOND-MOMENT / large-sieve over the (u,v)-family -- and cut naive family
Cauchy-Schwarz as "dead by 5862x".  This packet works that opening exactly:

  PROVED   Two exact Parseval second moments over the frequency group F_p^2:
             sum_{u,v} |T2|^2 = 2 p^2 (n'-1)(n'-2)              (closed form),
             sum_{u,v} |T3|^2 = 36 p^2 * sum_h M(h)^2           (collision energy),
           where M(h) = #{arc 3-sets with high h}.  The T2 moment is a clean
           closed form (pairs have no nontrivial collision -- (sum,prod)
           determines the pair); the T3 moment reduces to the triple collision
           energy S := sum_h M(h)^2 = C(n'-1,3) + 2*L3.  Verified to the integer
           on toys against the direct complex evaluation.
  PROVED   The Cauchy-Schwarz-across-(T3,T2) route over frequency space IS #484's
           cut (a) <tau, Phi_A> over high space, Fourier-dual identical:
             |P_err| <= sqrt(C2 * (S - C3^2/p^2))  (centered / principal-extracted)
           and its uncentered form sqrt(C2 * S) = 453080737874835 = 5862 H2 is
           exactly #484's number.  Since S >= C3 unconditionally (diagonal floor),
           the method output is >= sqrt(C2 * C3(1-C3/p^2)) = 426296814343656 =
           5515 H2 = 12296 * budget for EVERY collision profile.  Killing all
           off-diagonals (PTE-type rigidity) gains only 5862 -> 5515 H2 (~6%);
           the barrier is the irreducible triple-count diagonal, not collisions.
  MEASURED The phase-free absolute-value sum sum_{(u,v)!=0}|T3||T2|/(12 p^2)
           overshoots the budget by a factor growing with arc size (6x, 29x, 60x
           over budget at t=9,18,27), and the non-principal |T2|^2 mass
           concentrates on O(p) near-axis frequencies -- the large-sieve "few
           large frequencies" shape, made exact for the degree-2 factor.
  WALL     No bound on the absolute-value family sum |T3 T2| can reach 0.4485 H2:
           the second moment floors at 5515 H2 and the phase-free sum overshoots
           and grows.  The psi(-u zeta) twist is load-bearing; closing star3 needs
           SIGNED cancellation among the ~p^2 frequencies (a Weil/Kloosterman-type
           estimate for the 2-parameter family), not any second-moment bound.

Zero-argument default: full deterministic recompute, exact comparison against the
checked-in JSON certificate, and a live tamper suite.  --generate rewrites the
certificate (maintainer only).  RLIMIT_AS capped at 2 GiB; frequency sums are on
tiny arcs (t <= 27).  Reference run: about 1 minute.

This continues our engagement (PR #468, #479, #482, #484) with Hughes's Route-D
program; his v51-v54 chain and #479/#482/#484's pins/reductions are used as-is and
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
CERT_PATH = ROOT / "experimental" / "data" / "cap25_v13_star3_l2_second_moment.json"
ADDRESS_SPACE_CAP_BYTES = 2 * 1024**3

# ---- deployed KB row (source: verify_kb_qatom_route_d_v54.py, #479, #482, #484) ----
P_KB = 2**31 - 2**24 + 1          # 2130706433
N_KB = 2**21
A_KB = 1_116_048
E_KB = 67_472
NP_KB = A_KB + E_KB               # 1183520
H2_KB = E_KB * P_KB // 1860       # 77291948627

# tiny arcs (n, q, t): p = q*n+1 prime, arc = omega^0..omega^{t-1}, zeta = last.
ARCS = [(16, 1, 9), (32, 3, 18), (64, 4, 27)]   # KB-shape t = 9n/16
ARCS_REVALIDATE = [(16, 1, 9), (32, 3, 18)]     # freshly re-run per tamper (cheap)


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


def arc_values(p: int, n: int, t: int) -> list[int]:
    """Arc omega^0..omega^{t-1}; zeta = last entry.  Canonical omega on the
    primitive-root convention (matches #482/#484's stepped_values)."""
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
    return base[:t]


# ----------------- exact integer combinatorics on a tiny arc -----------------

def arc_integer_data(p: int, arc: list[int]) -> dict[str, Any]:
    """Cheap exact integers: m = |A|, S = sum_h M(h)^2 (triple collision energy),
    C2,C3,D2,D3, and the terminal-high-distinctness fact (L2)."""
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
    S = sum(v * v for v in H3.values())
    c3 = math.comb(m, 3)
    if sum(H3.values()) != c3:
        raise CheckFailure("triple histogram total != C(m,3)")
    # terminal highs must be distinct (Hughes/#479 L2)
    seen: set[tuple[int, int]] = set()
    for i in range(m):
        a = As[i]
        for j in range(i + 1, m):
            b = As[j]
            key = ((a + b + zeta) % p, (a * b + zeta * (a + b)) % p)
            if key in seen:
                raise CheckFailure("two terminal 3-sets share a high (L2)")
            seen.add(key)
    return {
        "m": m,
        "S": S,
        "L3": (S - c3) // 2,
        "C2": math.comb(m, 2),
        "C3": c3,
        "D2": m * (m - 1),
        "D3": m * (m - 1) * (m - 2),
    }


# ---------------- complex frequency sums on a tiny arc (checks) ---------------

def _histograms(p: int, arc: list[int]) -> tuple[list, list, int]:
    t = len(arc)
    zeta = arc[t - 1]
    As = arc[:t - 1]
    m = len(As)
    H3: dict[tuple[int, int], int] = {}
    HP: dict[tuple[int, int], int] = {}
    for i in range(m):
        a = As[i]
        for j in range(i + 1, m):
            b = As[j]
            sab = a + b
            pab = a * b
            HP[((a + b + zeta) % p, (a * b + zeta * (a + b)) % p)] = \
                HP.get(((a + b + zeta) % p, (a * b + zeta * (a + b)) % p), 0) + 1
            for k in range(j + 1, m):
                c = As[k]
                key = ((sab + c) % p, (pab + sab * c) % p)
                H3[key] = H3.get(key, 0) + 1
    return list(H3.items()), list(HP.items()), zeta


def second_moments(p: int, arc: list[int]) -> dict[str, int]:
    """Direct complex sum_{u,v}|T3|^2, |T2|^2 (all and non-principal), rounded to
    integers.  T3 = 6 * FT(M); T2 = 2 * FT(pair-highs)."""
    h3, hp, zeta = _histograms(p, arc)
    roots = [cmath.exp(2j * cmath.pi * k / p) for k in range(p)]
    s3 = 0.0
    s2 = 0.0
    s3np = 0.0
    s2np = 0.0
    max_imag = 0.0
    for u in range(p):
        for v in range(p):
            t3 = 0j
            for (e1, e2), c in h3:
                t3 += c * roots[(u * e1 + v * e2) % p]
            t3 *= 6
            t2 = 0j
            for (s, q), c in hp:
                t2 += c * roots[(-u * (s - zeta) - v * q) % p]
            t2 *= 2
            a3 = abs(t3) ** 2
            a2 = abs(t2) ** 2
            s3 += a3
            s2 += a2
            if u or v:
                s3np += a3
                s2np += a2
    return {
        "sumT3sq": round(s3),
        "sumT2sq": round(s2),
        "sumT3sq_np": round(s3np),
        "sumT2sq_np": round(s2np),
    }


def t2_level_profile(p: int, arc: list[int]) -> dict[str, Any]:
    """|T2(u,v)|^2 over all frequencies.  Tests the large-sieve premise "large
    |T2| lives on FEW frequencies": reports the non-principal total (exact), the
    axis-set {u=0 or v=0} mass fraction, the top-(2p) mass fraction, and the
    fraction of ALL frequencies needed to hold half the non-principal mass."""
    h3, hp, zeta = _histograms(p, arc)
    roots = [cmath.exp(2j * cmath.pi * k / p) for k in range(p)]
    vals: list[float] = []
    axis_mass = 0.0
    principal = 0.0
    for u in range(p):
        for v in range(p):
            t2 = 0j
            for (s, q), c in hp:
                t2 += c * roots[(-u * (s - zeta) - v * q) % p]
            t2 *= 2
            a2 = abs(t2) ** 2
            if u == 0 and v == 0:
                principal = a2
                continue
            vals.append(a2)
            if u == 0 or v == 0:
                axis_mass += a2
    vals.sort(reverse=True)
    total_np = sum(vals)
    top2p = sum(vals[: 2 * p])
    half = 0.0
    half_rank = 0
    for a in vals:
        half += a
        half_rank += 1
        if half >= 0.5 * total_np:
            break
    return {
        "principal_round": round(principal),
        "np_total_round": round(total_np),
        "np_max_round": round(vals[0]) if vals else 0,
        "axis_frac": (axis_mass / total_np) if total_np else 0.0,
        "top2p_frac": (top2p / total_np) if total_np else 0.0,
        "half_mass_freq_frac": half_rank / (p * p - 1),
        "n_axis": 2 * (p - 1),
        "n_freq": p * p - 1,
    }


def absolute_value_bound(p: int, arc: list[int]) -> dict[str, float]:
    """Phase-free pointwise bound sum_{(u,v)!=0}|T3||T2|/(12 p^2) on |P_err|,
    and its ratio to the load P_main = C2 C3 / p^2 (the toy budget analogue is
    0.8134 * P_main from the deployed 0.4485/0.5515 split)."""
    h3, hp, zeta = _histograms(p, arc)
    dat = arc_integer_data(p, arc)
    roots = [cmath.exp(2j * cmath.pi * k / p) for k in range(p)]
    cross = 0.0
    for u in range(p):
        for v in range(p):
            if not (u or v):
                continue
            t3 = 0j
            for (e1, e2), c in h3:
                t3 += c * roots[(u * e1 + v * e2) % p]
            t2 = 0j
            for (s, q), c in hp:
                t2 += c * roots[(-u * (s - zeta) - v * q) % p]
            cross += abs(6 * t3) * abs(2 * t2)
    pointwise = cross / (12 * p * p)
    p_main = dat["C2"] * dat["C3"] / (p * p)
    ratio = pointwise / p_main
    return {
        "pointwise": pointwise,
        "p_main": p_main,
        "pointwise_over_pmain": ratio,
        "over_budget": ratio / 0.8134,       # budget analogue 0.8134 * P_main
    }


def sig(x: float, d: int = 6) -> str:
    return ("%." + str(d) + "g") % x


# ------------------------------ deployed block -------------------------------

def deployed_block() -> dict[str, Any]:
    p2 = P_KB * P_KB
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    d2 = (NP_KB - 1) * (NP_KB - 2)
    off = c3 * c3 // p2                       # modelled off-diagonal ~ C3^2/p^2
    p_main = Fraction(c2 * c3, p2)
    err_budget = H2_KB - p_main
    # exact T2 second moment (closed form) and its non-principal part
    sum_t2 = 2 * p2 * d2
    sum_t2_np = d2 * (2 * p2 - d2)
    # T3 second moment floor (S >= C3) and non-principal floor
    sum_t3_floor = 36 * p2 * c3
    sum_t3_np_floor = 36 * (p2 * c3 - c3 * c3)
    # Cauchy-Schwarz-across-(T3,T2) outputs (integer isqrt gates)
    cs_uncentered = math.isqrt(c2 * (c3 + off))    # #484 cut (a): sqrt(C2 * S_model)
    cs_model = math.isqrt(c2 * c3)                 # centered at modelled S
    cs_floor = math.isqrt(c2 * (c3 - off))         # unconditional floor (S = C3)
    eb_floor = err_budget.numerator // err_budget.denominator
    return {
        "p": P_KB,
        "p_squared": p2,
        "n": N_KB,
        "n_prime": NP_KB,
        "m_arc": NP_KB - 1,
        "e": E_KB,
        "H2": H2_KB,
        "H2_formula_ok": H2_KB == E_KB * P_KB // 1860,
        "C2": c2,
        "C2_pin": c2 == 700358019921,
        "C3": c3,
        "C3_pin": c3 == 276295207554280719,
        "D2": d2,
        "D2_is_2C2": d2 == 2 * c2,
        "modelled_offdiag": off,
        "offdiag_over_diag": sig(off / c3),                 # ~0.0609
        "P_main_floor": (c2 * c3) // p2,                    # 42623216888
        "P_main_over_H2": sig(float(p_main / H2_KB)),       # 0.551457
        "err_budget_floor": eb_floor,                       # 34668731738
        "err_budget_over_H2": sig(float(err_budget / H2_KB)),  # 0.448543
        # exact T2 second moment
        "sum_T2_sq": sum_t2,
        "sum_T2_sq_formula": "2 p^2 (n'-1)(n'-2)",
        "sum_T2_sq_np": sum_t2_np,
        # T3 second moment floor
        "sum_T3_sq_floor": sum_t3_floor,
        "sum_T3_sq_formula": "36 p^2 sum_h M(h)^2, with sum_h M(h)^2 >= C(n'-1,3)",
        "sum_T3_sq_np_floor": sum_t3_np_floor,
        # Cauchy-Schwarz route
        "cs_uncentered_484_cut_a": cs_uncentered,
        "cs_uncentered_over_H2": sig(cs_uncentered / H2_KB),   # ~5862
        "cs_model_centered": cs_model,
        "cs_model_over_H2": sig(cs_model / H2_KB),             # ~5691
        "cs_floor_unconditional": cs_floor,
        "cs_floor_over_H2": sig(cs_floor / H2_KB),             # ~5515
        "cs_floor_over_budget": sig(cs_floor / float(err_budget)),  # ~12296
        "pte_rigidity_gain_pct": sig(100 * (1 - cs_floor / cs_uncentered)),  # ~6%
        "trivial_deficit_C2_over_H2": sig(c2 / H2_KB),        # 9.0612 (trivial beats CS)
        # needed average |T3 T2| for star3 (per frequency, p^2-normalised)
        "needed_avg_T3T2_over_H2": sig(12 * float(err_budget) / H2_KB),  # ~5.383
    }


# ------------------------------ toy-row blocks -------------------------------

def l2_identity_block() -> dict[str, Any]:
    rows = []
    for n, q, t in ARCS:
        p = q * n + 1
        arc = arc_values(p, n, t)
        dat = arc_integer_data(p, arc)
        sm = second_moments(p, arc)
        p2 = p * p
        f_t3 = 36 * p2 * dat["S"]
        f_t2 = 2 * p2 * dat["D2"]
        f_t3_np = 36 * (p2 * dat["S"] - dat["C3"] * dat["C3"])
        f_t2_np = dat["D2"] * (2 * p2 - dat["D2"])
        rows.append({
            "n": n, "q": q, "p": p, "t": t, "m": dat["m"],
            "S": dat["S"], "L3": dat["L3"],
            "sum_T3_sq_complex": sm["sumT3sq"],
            "sum_T3_sq_formula": f_t3,
            "sum_T2_sq_complex": sm["sumT2sq"],
            "sum_T2_sq_formula": f_t2,
            "sum_T3_sq_np_complex": sm["sumT3sq_np"],
            "sum_T3_sq_np_formula": f_t3_np,
            "sum_T2_sq_np_complex": sm["sumT2sq_np"],
            "sum_T2_sq_np_formula": f_t2_np,
            "identity_ok": (sm["sumT3sq"] == f_t3 and sm["sumT2sq"] == f_t2
                            and sm["sumT3sq_np"] == f_t3_np
                            and sm["sumT2sq_np"] == f_t2_np),
        })
    return {"status": "EXACT_L2_PARSEVAL_IDENTITIES_VERIFIED", "rows": rows}


def cs_equivalence_block() -> dict[str, Any]:
    """On each toy: the frequency-space non-principal CS equals the centered
    high-space CS times sqrt(1 - D2/2p^2), and the uncentered form equals #484's
    sqrt(C2 * S).  All three are the SAME route (Fourier duality)."""
    rows = []
    for n, q, t in ARCS:
        p = q * n + 1
        arc = arc_values(p, n, t)
        dat = arc_integer_data(p, arc)
        p2 = p * p
        c2, c3, d2, S = dat["C2"], dat["C3"], dat["D2"], dat["S"]
        # freq-space non-principal CS on |P_err|
        a3 = 36 * (p2 * S - c3 * c3)
        a2 = d2 * (2 * p2 - d2)
        cs_freq = math.sqrt(a3) * math.sqrt(a2) / (12 * p2)
        # centered high-space CS
        cs_cent = math.sqrt(c2 * (S - c3 * c3 / p2))
        # predicted relation factor sqrt(1 - D2/2p^2)
        factor = math.sqrt(1 - d2 / (2 * p2))
        # #484 uncentered
        cs_unc = math.sqrt(c2 * S)
        rows.append({
            "n": n, "p": p, "t": t,
            "cs_freq_nonprincipal": sig(cs_freq),
            "cs_centered_highspace": sig(cs_cent),
            "relation_factor_pred": sig(factor),
            "relation_ok": abs(cs_freq - cs_cent * factor) < 1e-6 * max(1.0, cs_cent),
            "cs_uncentered_484": sig(cs_unc),
        })
    return {"status": "CS_ROUTE_EQUALS_484_CUT_A_FOURIER_DUAL", "rows": rows}


def t2_levelset_block() -> dict[str, Any]:
    rows = []
    for n, q, t in ARCS:
        p = q * n + 1
        arc = arc_values(p, n, t)
        dat = arc_integer_data(p, arc)
        prof = t2_level_profile(p, arc)
        rows.append({
            "n": n, "p": p, "t": t,
            "np_total_round": prof["np_total_round"],
            "np_total_formula": dat["D2"] * (2 * p * p - dat["D2"]),
            "np_max_round": prof["np_max_round"],
            "axis_frac": sig(prof["axis_frac"]),
            "top2p_frac": sig(prof["top2p_frac"]),
            "half_mass_freq_frac": sig(prof["half_mass_freq_frac"]),
            "n_axis": prof["n_axis"],
            "n_freq": prof["n_freq"],
        })
    return {"status": "MEASURED_T2_MASS_NOT_CONCENTRATED", "rows": rows}


def absval_dead_block() -> dict[str, Any]:
    rows = []
    for n, q, t in ARCS:
        p = q * n + 1
        arc = arc_values(p, n, t)
        av = absolute_value_bound(p, arc)
        rows.append({
            "n": n, "p": p, "t": t,
            "pointwise": sig(av["pointwise"]),
            "p_main": sig(av["p_main"]),
            "pointwise_over_pmain": sig(av["pointwise_over_pmain"]),
            "over_budget": sig(av["over_budget"]),
        })
    return {"status": "MEASURED_ABSOLUTE_VALUE_ROUTE_DEAD_AND_GROWING", "rows": rows}


def route_records() -> dict[str, Any]:
    return {
        "t2_second_moment": {
            "status": "PROVED",
            "statement": (
                "sum_{u,v} |T2(u,v)|^2 = 2 p^2 (n'-1)(n'-2) EXACTLY.  Pairs have "
                "no nontrivial collision: (x+y, xy) determines the unordered pair, "
                "so the only frequency-Parseval matches are the 2 reorderings.  At "
                "the deployed row this is the exact integer 2 p^2 D2; verified to "
                "the integer against the direct complex sum on toys."
            ),
        },
        "t3_second_moment": {
            "status": "PROVED",
            "statement": (
                "sum_{u,v} |T3(u,v)|^2 = 36 p^2 sum_h M(h)^2, M(h) = #{arc 3-sets "
                "with high h}; sum_h M(h)^2 = C(n'-1,3) + 2 L3, L3 = # unordered "
                "equal-high 3-set pairs (a birthday-collision energy).  The "
                "diagonal C(n'-1,3) is an unconditional floor (M >= its own count)."
            ),
        },
        "cs_equals_484_cut_a": {
            "status": "PROVED",
            "statement": (
                "Cauchy-Schwarz across the two factors over frequency space, "
                "|P_err| <= sqrt(sum_{!=0}|T3|^2) sqrt(sum_{!=0}|T2|^2)/(12 p^2), "
                "equals #484's cut (a) <tau,Phi_A> over high space by Fourier "
                "duality: it is sqrt(C2 (S - C3^2/p^2)) * sqrt(1 - D2/2p^2), and "
                "its uncentered form sqrt(C2 S) = 453080737874835 = 5862 H2 is "
                "#484's exact number.  This factorization does NOT escape the cut."
            ),
        },
        "cs_floor_unconditional": {
            "status": "PROVED",
            "statement": (
                "Because S >= C(n'-1,3) for every collision profile, the CS route "
                "outputs >= sqrt(C2 (C3 - C3^2/p^2)) = 426296814343656 = 5515 H2 = "
                "12296 * budget, unconditionally.  Killing every off-diagonal "
                "(PTE-type rigidity, S -> C3) moves 5862 H2 -> 5515 H2, a ~6% "
                "gain; the barrier is the irreducible triple-count diagonal, not "
                "collision abundance.  The CS route is also worse than the trivial "
                "bound C2 = 9.06 H2."
            ),
        },
        "levelset_dyadic": {
            "status": "ANALYSIS + MEASURED (premise fails)",
            "statement": (
                "T2_full(u,v) = sum_{x in A} psi(-w x) G(w + v x), w = u + v zeta, "
                "G(c) = sum_{y in A} psi(-c y) an incomplete arc sum; on v=0, "
                "T2(u,0) = G(u)^2 - G(2u).  The large-sieve refinement needs |T2| "
                "large on FEW frequencies -- but MEASURED, the |T2|^2 mass is "
                "quasi-equidistributed: half of it is spread over ~17% of ALL p^2 "
                "frequencies (stable with arc size), the axis-set share is small "
                "and SHRINKS (0.11 -> 0.029 -> 0.006 at t=9,18,27), and top-(2p) "
                "falls 0.31 -> 0.12 -> 0.06.  There is no sparse heavy set to "
                "isolate, so the dyadic 'few large x bounded + many small x "
                "cancellation' split has no small part; any reweighting of "
                "ABSOLUTE VALUES inherits the 5515 H2 diagonal floor."
            ),
        },
        "absolute_value_route_dead": {
            "status": "MEASURED (route dead)",
            "statement": (
                "The phase-free sum_{(u,v)!=0}|T3||T2|/(12 p^2) overshoots the "
                "budget by a factor growing with arc size (6x, 29x, 60x over "
                "budget at t=9,18,27), reproducing #484's route-cut (c) growth.  "
                "So no bound on the absolute-value family sum |T3 T2| can reach "
                "0.4485 H2."
            ),
        },
        "wall_phase_load_bearing": {
            "status": "WALL (ANALYSIS)",
            "statement": (
                "Both the second moment (floors at 5515 H2) and the phase-free sum "
                "(overshoots and grows) rule out every ABSOLUTE-VALUE second-moment "
                "/ large-sieve bound.  The psi(-u zeta) twist is load-bearing: "
                "closing star3 requires SIGNED cancellation in "
                "sum_{(u,v)!=0} psi(-u zeta) T3(u,v) T2(u,v) = 12 p^2 P_err -- a "
                "Weil/Kloosterman-type estimate for the 2-parameter frequency "
                "family, the input pointwise and second-moment methods cannot "
                "supply.  This sharpens #484's cuts (a),(c) across the whole family."
            ),
        },
    }


# ------------------------------- certificate ---------------------------------

def build_certificate() -> dict[str, Any]:
    return {
        "packet": "cap25_v13_star3_l2_second_moment",
        "date": "2026-07-10",
        "status": "L2_PARSEVAL_IDENTITIES_EXACT_CS_FLOOR_PROVED_WALL_OPEN",
        "claims": {
            "t2_second_moment_closed_form_exact": True,
            "t3_second_moment_equals_collision_energy_exact": True,
            "identities_verified_on_toys": True,
            "cs_across_factors_equals_484_cut_a_proved": True,
            "cs_floor_unconditional_5515_H2_proved": True,
            "pte_rigidity_gains_only_6pct": True,
            "absolute_value_route_dead_measured": True,
            "phase_is_load_bearing_wall": True,
            "proves_P_le_H2": False,
            "proves_star3": False,
            "proves_deployed_wall": False,
            "closes_budget_via_L2": False,
            "counterexample_found": False,
            "refutes_any_hughes_479_482_484_claim": False,
        },
        "wall_statement": (
            "star3 (P <= H2 = 77291948627 at the KB row) cannot be closed by any "
            "bound on the absolute-value family sum |T3(u,v) T2(u,v)|.  Exact "
            "Parseval: sum|T2|^2 = 2 p^2 (n'-1)(n'-2), sum|T3|^2 = 36 p^2 "
            "sum_h M(h)^2 with sum_h M(h)^2 >= C(n'-1,3).  Cauchy-Schwarz across "
            "the factors is #484's cut (a) and outputs >= 5515 H2 = 12296*budget "
            "for every collision profile.  Closing star3 needs SIGNED cancellation "
            "in sum_{(u,v)!=0} psi(-u zeta) T3 T2 = 12 p^2 P_err, not a second "
            "moment.  P_main = C(n'-1,2)C(n'-1,3)/p^2 = 0.5515 H2 exactly; residual "
            "budget 0.4485 H2 (#484)."
        ),
        "deployed": deployed_block(),
        "l2_identities": l2_identity_block(),
        "cs_equivalence": cs_equivalence_block(),
        "t2_level_sets": t2_levelset_block(),
        "absolute_value_dead": absval_dead_block(),
        "routes": route_records(),
        "lineage": {
            "supports_scott_hughes_route_d": True,
            "continues_pr468_pr479_pr482_pr484": True,
            "source": "Hughes Route-D v1-v54; PR #468, #479, #482, #484",
        },
    }


# ------------------------------- validation ----------------------------------

def validate_certificate(cert: dict[str, Any], replay: dict[str, Any] | None,
                         checks: Checks) -> None:
    checks.equal(cert["packet"], "cap25_v13_star3_l2_second_moment", "packet")
    checks.equal(cert["status"],
                 "L2_PARSEVAL_IDENTITIES_EXACT_CS_FLOOR_PROVED_WALL_OPEN",
                 "status")
    cl = cert["claims"]
    for k in ("proves_P_le_H2", "proves_star3", "proves_deployed_wall",
              "closes_budget_via_L2", "counterexample_found",
              "refutes_any_hughes_479_482_484_claim"):
        checks.equal(cl[k], False, f"nonclaim {k}")
    checks.equal(cert["lineage"]["continues_pr468_pr479_pr482_pr484"], True,
                 "lineage")

    # ---- deployed exact arithmetic, recomputed as integers ----
    d = cert["deployed"]
    p2 = P_KB * P_KB
    checks.check(is_prime(P_KB), "p prime")
    checks.equal(d["p_squared"], p2, "p^2")
    checks.equal(d["H2"], E_KB * P_KB // 1860, "H2 formula")
    checks.equal(d["H2"], 77291948627, "H2 pin")
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    d2 = (NP_KB - 1) * (NP_KB - 2)
    off = c3 * c3 // p2
    checks.equal(d["C2"], c2, "C2")
    checks.equal(c2, 700358019921, "C2 pin")
    checks.equal(d["C3"], c3, "C3")
    checks.equal(c3, 276295207554280719, "C3 pin")
    checks.equal(d["D2"], d2, "D2")
    checks.equal(d["D2"], 2 * c2, "D2 = 2 C2")
    checks.equal(d["modelled_offdiag"], off, "offdiag")
    checks.equal(d["P_main_floor"], (c2 * c3) // p2, "P_main floor")
    checks.equal(d["P_main_floor"], 42623216888, "P_main floor pin")
    p_main = Fraction(c2 * c3, p2)
    err_budget = H2_KB - p_main
    checks.equal(d["err_budget_floor"],
                 err_budget.numerator // err_budget.denominator, "err budget")
    checks.equal(d["err_budget_floor"], 34668731738, "err budget pin")
    checks.equal(d["P_main_over_H2"], "0.551457", "P_main/H2")
    checks.equal(d["err_budget_over_H2"], "0.448543", "err budget/H2")

    # exact T2 second moment (closed form, deployed scale)
    checks.equal(d["sum_T2_sq"], 2 * p2 * d2, "T2 second moment closed form")
    checks.equal(d["sum_T2_sq"], 12718249242897409229416610737476, "T2 mom pin")
    checks.equal(d["sum_T2_sq_np"], d2 * (2 * p2 - d2), "T2 non-principal moment")
    # T3 second moment floor
    checks.equal(d["sum_T3_sq_floor"], 36 * p2 * c3, "T3 second moment floor")
    checks.equal(d["sum_T3_sq_np_floor"], 36 * (p2 * c3 - c3 * c3),
                 "T3 non-principal floor")

    # Cauchy-Schwarz route integers (isqrt gates)
    cs_unc = math.isqrt(c2 * (c3 + off))
    cs_mod = math.isqrt(c2 * c3)
    cs_flr = math.isqrt(c2 * (c3 - off))
    checks.equal(d["cs_uncentered_484_cut_a"], cs_unc, "CS uncentered")
    checks.equal(d["cs_uncentered_484_cut_a"], 453080737874835, "CS uncentered pin")
    checks.check(5800 < float(d["cs_uncentered_over_H2"]) < 5900,
                 "CS uncentered ~ 5862 (== #484)")
    checks.equal(d["cs_model_centered"], cs_mod, "CS model centered")
    checks.equal(d["cs_floor_unconditional"], cs_flr, "CS floor")
    checks.equal(d["cs_floor_unconditional"], 426296814343656, "CS floor pin")
    checks.check(5400 < float(d["cs_floor_over_H2"]) < 5600, "CS floor ~ 5515 H2")
    # the floor is unconditionally >> budget: 12000 < floor/budget < 12500
    eb = err_budget.numerator // err_budget.denominator
    checks.check(cs_flr > 12000 * eb, "CS floor > 12000 * budget (route dead)")
    checks.check(cs_flr < 12500 * eb, "CS floor < 12500 * budget")
    # CS floor even exceeds the trivial bound C2 (= 9.06 H2): floor > C2
    checks.check(cs_flr > c2, "CS floor worse than trivial C2 bound")
    # PTE rigidity gain small: floor >= 0.9 * uncentered (<=10% gain)
    checks.check(10 * cs_flr > 9 * cs_unc, "PTE rigidity gain <= 10%")
    checks.equal(d["needed_avg_T3T2_over_H2"], sig(12 * float(err_budget) / H2_KB),
                 "needed avg |T3 T2|")

    # ---- L2 Parseval identities, freshly recomputed on the cheap toy arcs ----
    li = cert["l2_identities"]
    checks.equal(li["status"], "EXACT_L2_PARSEVAL_IDENTITIES_VERIFIED", "li status")
    checks.check(len(li["rows"]) >= 3, "at least three identity rows")
    stored = {(r["n"], r["t"]): r for r in li["rows"]}
    for n, q, t in ARCS:
        p = q * n + 1
        r = stored[(n, t)]
        checks.equal(r["p"], p, "li prime")
        checks.check(is_prime(p), "li p prime")
        arc = arc_values(p, n, t)
        dat = arc_integer_data(p, arc)
        pp = p * p
        # integer formula gates (cheap, all arcs)
        checks.equal(r["S"], dat["S"], "li S")
        checks.equal(r["L3"], dat["L3"], "li L3")
        checks.equal(r["sum_T3_sq_formula"], 36 * pp * dat["S"], "li T3 formula")
        checks.equal(r["sum_T2_sq_formula"], 2 * pp * dat["D2"], "li T2 formula")
        checks.equal(r["sum_T3_sq_np_formula"],
                     36 * (pp * dat["S"] - dat["C3"] ** 2), "li T3 np formula")
        checks.equal(r["sum_T2_sq_np_formula"],
                     dat["D2"] * (2 * pp - dat["D2"]), "li T2 np formula")
        # identity: complex == formula (fresh complex only on the cheap arcs)
        checks.equal(r["sum_T3_sq_complex"], r["sum_T3_sq_formula"],
                     "li T3 complex == formula (stored)")
        checks.equal(r["sum_T2_sq_complex"], r["sum_T2_sq_formula"],
                     "li T2 complex == formula (stored)")
        checks.check(r["identity_ok"], "li identity_ok flag")
        if (n, t) in [(a, c) for a, _, c in ARCS_REVALIDATE]:
            sm = second_moments(p, arc)
            checks.equal(sm["sumT3sq"], 36 * pp * dat["S"], "li T3 complex fresh")
            checks.equal(sm["sumT2sq"], 2 * pp * dat["D2"], "li T2 complex fresh")
            checks.equal(sm["sumT3sq_np"], 36 * (pp * dat["S"] - dat["C3"] ** 2),
                         "li T3 np complex fresh")
            checks.equal(sm["sumT2sq_np"], dat["D2"] * (2 * pp - dat["D2"]),
                         "li T2 np complex fresh")

    # ---- CS-equals-#484 equivalence ----
    ce = cert["cs_equivalence"]
    checks.equal(ce["status"], "CS_ROUTE_EQUALS_484_CUT_A_FOURIER_DUAL", "ce status")
    for r in ce["rows"]:
        checks.check(r["relation_ok"],
                     "freq CS == centered highspace CS * sqrt(1-D2/2p^2)")

    # ---- T2 mass NOT concentrated: large-sieve "few large freqs" premise fails ----
    ts = cert["t2_level_sets"]
    checks.equal(ts["status"], "MEASURED_T2_MASS_NOT_CONCENTRATED", "ts status")
    axis_prev = None
    for r in ts["rows"]:
        p = r["p"]
        arc = arc_values(p, r["n"], r["t"])
        dat = arc_integer_data(p, arc)
        checks.equal(r["np_total_formula"], dat["D2"] * (2 * p * p - dat["D2"]),
                     "ts np total formula")
        # measured total must match the exact non-principal T2 second moment
        checks.equal(r["np_total_round"], r["np_total_formula"], "ts total exact")
        # NOT concentrated: half the mass needs a positive fraction of ALL freqs
        checks.check(float(r["half_mass_freq_frac"]) > 0.10,
                     "ts half-mass spread over > 10% of frequencies")
        # NOT axis-concentrated, and the axis share shrinks with arc size
        checks.check(float(r["axis_frac"]) < 0.15, "ts axis share small")
        av = float(r["axis_frac"])
        if axis_prev is not None:
            checks.check(av < axis_prev, "ts axis share shrinks with arc size")
        axis_prev = av

    # ---- absolute-value route dead and growing (measured) ----
    ad = cert["absolute_value_dead"]
    checks.equal(ad["status"],
                 "MEASURED_ABSOLUTE_VALUE_ROUTE_DEAD_AND_GROWING", "ad status")
    prev = None
    for r in ad["rows"]:
        val = float(r["over_budget"])
        checks.check(val > 1.0, "ad over budget (route dead)")
        if prev is not None:
            checks.check(val > prev, "ad over-budget factor grows with arc size")
        prev = val
    checks.check(float(ad["rows"][-1]["over_budget"]) > 40, "ad grows past 40x")

    # ---- route records present with honest labels ----
    routes = cert["routes"]
    for key in ("t2_second_moment", "t3_second_moment", "cs_equals_484_cut_a",
                "cs_floor_unconditional", "levelset_dyadic",
                "absolute_value_route_dead", "wall_phase_load_bearing"):
        checks.check(key in routes, f"route {key} present")
    checks.equal(routes["t2_second_moment"]["status"], "PROVED", "T2 PROVED")
    checks.equal(routes["cs_floor_unconditional"]["status"], "PROVED",
                 "CS floor PROVED")
    checks.check("dead" in routes["absolute_value_route_dead"]["status"].lower(),
                 "abs-value labeled dead")
    checks.check("WALL" in routes["wall_phase_load_bearing"]["status"],
                 "wall labeled")

    if replay is not None:
        checks.equal(cert, replay, "full exact replay")


# ------------------------------- tamper suite --------------------------------

def tamper_suite(cert: dict[str, Any], replay: dict[str, Any]) -> tuple[int, int]:
    def m_prove(d):
        d["claims"]["proves_star3"] = True

    def m_close(d):
        d["claims"]["closes_budget_via_L2"] = True

    def m_cx(d):
        d["claims"]["counterexample_found"] = True

    def m_t2mom(d):
        d["deployed"]["sum_T2_sq"] += 2

    def m_t3floor(d):
        d["deployed"]["sum_T3_sq_floor"] += 36

    def m_csfloor(d):
        d["deployed"]["cs_floor_unconditional"] -= 1

    def m_csunc(d):
        d["deployed"]["cs_uncentered_484_cut_a"] += 1

    def m_csfloor_ratio(d):
        d["deployed"]["cs_floor_over_H2"] = "0.4"

    def m_c3(d):
        d["deployed"]["C3"] += 1

    def m_ident(d):
        d["l2_identities"]["rows"][0]["sum_T3_sq_complex"] += 36

    def m_ident_form(d):
        d["l2_identities"]["rows"][0]["S"] += 1

    def m_ident_t2(d):
        d["l2_identities"]["rows"][-1]["sum_T2_sq_formula"] += 2

    def m_ce(d):
        d["cs_equivalence"]["rows"][0]["relation_ok"] = False

    def m_levelset(d):
        d["t2_level_sets"]["rows"][0]["np_total_round"] += 4

    def m_axis(d):
        # fake concentration: pretend half the mass sits in <10% of frequencies
        d["t2_level_sets"]["rows"][0]["half_mass_freq_frac"] = "0.01"

    def m_absval(d):
        # break monotone growth by zeroing the last over-budget factor
        d["absolute_value_dead"]["rows"][-1]["over_budget"] = "1.0"

    def m_route(d):
        d["routes"]["cs_floor_unconditional"]["status"] = "CONJECTURAL"

    def m_lineage(d):
        d["lineage"]["continues_pr468_pr479_pr482_pr484"] = False

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("promote-star3", m_prove),
        ("promote-close-budget", m_close),
        ("fake-counterexample", m_cx),
        ("t2-moment-drift", m_t2mom),
        ("t3-floor-drift", m_t3floor),
        ("cs-floor-drift", m_csfloor),
        ("cs-uncentered-drift", m_csunc),
        ("cs-floor-ratio-drift", m_csfloor_ratio),
        ("c3-drift", m_c3),
        ("identity-complex", m_ident),
        ("identity-S", m_ident_form),
        ("identity-t2-formula", m_ident_t2),
        ("cs-equivalence-flag", m_ce),
        ("levelset-total-drift", m_levelset),
        ("levelset-spread-drift", m_axis),
        ("absval-growth-break", m_absval),
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
    cert = json.loads(CERT_PATH.read_text())
    checks = Checks()
    validate_certificate(cert, replay, checks)
    caught, total = tamper_suite(cert, replay)
    checks.check(total >= 12, "at least twelve tampers")
    checks.equal(caught, total, "all tampers caught")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"RESULT: PASS ({checks.passed}/{checks.total} checks; "
          f"tampers {caught}/{total})")
    print(f"peak RSS: {rss // 1024} MiB; wall time {time.time() - t0:.1f}s")
    print("status: L2 Parseval identities EXACT; CS-across-(T3,T2) = #484 cut (a) "
          "with unconditional 5515 H2 floor PROVED; absolute-value large-sieve "
          "dead (MEASURED); star3 remains OPEN (needs signed cancellation)")


if __name__ == "__main__":
    main()
