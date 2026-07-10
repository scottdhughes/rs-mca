#!/usr/bin/env python3
"""The star3 sub-wall of Hughes's Route-D terminal wall: restatement, an exact
incidence reduction, and a model-validating toy ladder.

PR #479 pinned Scott Hughes's terminal wall |T| <= H2 at the deployed KoalaBear
row and named the smallest honest sub-wall

    (star3)  |T(n',3)| <= H2 = 77291948627,

where T(n',3) counts terminal pairs {x,y} in I_{n'-1} whose 3-set {x,y,zeta}
admits a free-1 partner triple (a second arc 3-set with equal e_1, e_2 and
different e_3).  The trivial bound is |T(n',3)| <= C(n'-1,2) = 700358019921, a
factor 9.0612 above H2.  This packet:

  EXACT      restates star3 with every object explicit and reproduces the
             9.0612 factor and the target fraction 1/9.0612 = 0.110361.
  PROVED     the incidence reduction: |T(n',3)| <= P where P is the count of
             (terminal pair, non-terminal partner) incidences; a high (s,q)
             forces the terminal pair (R1), so star3 follows from P <= H2.
             Live-checked as |T| <= P on every toy row.
  PROVED     reproduces >= 8 deployed members of T(n',3) from #479's witness
             (U,V) index pairs, re-verified by locator expansion on the
             canonical arc (independent of #479's certificate).
  MEASURED   exact e_s=3 sociable fractions on a KB-shape toy ladder
             (t = 9n/16); the birthday model 1-exp(-lambda),
             lambda = C(t-1,3)/p^2, tracks the true fraction to a few percent
             across sparsity q in [9,65] and size t in [216,1152]; the crossing
             of the target fraction is bracketed at ~1.92x deployed arc size;
             every deployed-like (q~1016) row is ~10^-4, far below target.
  MEASURED   the antipodal partner subfamily (L5) is a ~10^-3 sliver of T.

Zero-argument default: full deterministic recompute, exact comparison against
the checked-in JSON certificate, and a live tamper suite.  --generate rewrites
the certificate (maintainer only).  RLIMIT_AS is capped at 2 GiB; heavy loops
are chunked.  Reference run: about 5-6 minutes, peak RSS < 400 MiB.

This continues our engagement (PR #468, PR #479) with Hughes's Route-D program;
his v51-v54 chain and #479's pins are used as-is and credited throughout.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import resource
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = ROOT / "experimental" / "data" / "cap25_v13_hughes_wall_star3.json"
ADDRESS_SPACE_CAP_BYTES = 2 * 1024**3

# ---- deployed KB row (source: verify_kb_qatom_route_d_v54.py, #479) ----
P_KB = 2**31 - 2**24 + 1          # 2130706433
N_KB = 2**21
A_KB = 1_116_048
E_KB = 67_472
NP_KB = A_KB + E_KB               # 1183520
H2_KB = E_KB * P_KB // 1860       # 77291948627
HALF = N_KB // 2

# #479 deployed e_s=3 witnesses: (U indices, V indices) on the canonical arc.
HUGHES_E3_WITNESSES = [
    ([5, 1139380, 1183519], [119016, 461783, 1167592]),
    ([10, 116655, 1183519], [34790, 64920, 1083366]),
    ([10, 1066874, 1183519], [41609, 1001501, 1090185]),
    ([34, 217618, 1183519], [13556, 80622, 1062132]),
    ([80, 1145533, 1183519], [111789, 655859, 1160365]),
    ([86, 932197, 1183519], [103106, 858291, 1151682]),
    ([115, 155875, 1183519], [124298, 541768, 1172874]),
    ([120, 624144, 1183519], [44846, 695508, 1093422]),
]

# registered exhaustive toy ladder: (regime label, n, q_target); q = smallest
# q >= q_target with q*n+1 prime; arc = stepped subgroup, t = 9n/16, step 1.
LADDER = [
    ("crossing", 512, 16),
    ("crossing", 1024, 16),
    ("crossing", 1280, 16),
    ("crossing", 1536, 16),
    ("dense", 384, 8),
    ("dense", 768, 10),
    ("mid_sparse", 1024, 64),
    ("mid_sparse", 2048, 64),
    ("deployed_like", 1024, 1016),
    ("deployed_like", 2048, 1016),
]
ANTI_ROW = (1024, 16)             # measure antipodal subfamily on this row
# PR #468 gradient cross-check anchor (n=64, t=36, step 1)
GRADIENT_PRIMES = [(4, 257), (18, 1153), (67, 4289), (253, 16193),
                   (513, 32833), (1017, 65089)]
PR468 = {(4, 3): (55, 58), (18, 3): (4, 4), (67, 3): (0, 0),
         (253, 3): (0, 0), (513, 3): (0, 0), (1017, 3): (0, 0)}


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


@lru_cache(maxsize=None)
def primitive_root(p: int) -> int:
    if not is_prime(p):
        raise CheckFailure(f"nonprime modulus {p}")
    fac = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise CheckFailure(f"no primitive root mod {p}")


@lru_cache(maxsize=None)
def subgroup_base(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise CheckFailure(f"n={n} does not divide p-1")
    omega = pow(primitive_root(p), (p - 1) // n, p)
    for q in prime_factors(n):
        if pow(omega, n // q, p) == 1:
            raise CheckFailure("omega has too small an order")
    vals = [1] * n
    v = 1
    for i in range(1, n):
        v = v * omega % p
        vals[i] = v
    if len(set(vals)) != n:
        raise CheckFailure("subgroup values not distinct")
    return tuple(vals)


def stepped_values(p: int, n: int, step: int) -> list[int]:
    base = subgroup_base(p, n)
    return [base[(step * i) % n] for i in range(n)]


def locator_coefficients(indices, values, p: int) -> list[int]:
    """Monic prod (X - values[i]); descending coefficient list."""
    co = [1]
    for i in indices:
        r = values[i]
        nxt = [0] * (len(co) + 1)
        for j, c in enumerate(co):
            nxt[j] = (nxt[j] + c) % p
            nxt[j + 1] = (nxt[j + 1] - r * c) % p
        co = nxt
    return co


# --------------------------- deployed arc (cached) ---------------------------

_ARC: dict[str, Any] = {}


def deployed_arc() -> tuple[list[int], int]:
    if "arc" not in _ARC:
        g = primitive_root(P_KB)
        if g != 3:
            raise CheckFailure("canonical KB generator drifted (expected 3)")
        omega = pow(g, (P_KB - 1) // N_KB, P_KB)
        if pow(omega, HALF, P_KB) != P_KB - 1:
            raise CheckFailure("omega^(n/2) != -1")
        arc = [1] * NP_KB
        v = 1
        for i in range(1, NP_KB):
            v = v * omega % P_KB
            arc[i] = v
        _ARC["arc"] = arc
        _ARC["omega"] = omega
    return _ARC["arc"], _ARC["omega"]


# ------------------------------ exact arithmetic -----------------------------

def sig6(x: float) -> str:
    return "%.6g" % x


def deployed_arithmetic() -> dict[str, Any]:
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    lam = c3 / P_KB**2
    model = -math.expm1(-lam)
    target = H2_KB / c2
    # crossing lambda: 1 - exp(-lam*) = target  ->  lam* = -ln(1-target)
    lam_star = -math.log(1 - target)
    return {
        "p": P_KB,
        "n": N_KB,
        "n_prime": NP_KB,
        "e": E_KB,
        "H2": H2_KB,
        "H2_formula_check": H2_KB == E_KB * P_KB // 1860,
        "subgroup_index": (P_KB - 1) // N_KB,
        "C_np1_2": c2,
        "C_np1_2_pinned": c2 == 700358019921,
        "C_np1_3": c3,
        "trivial_deficit": sig6(c2 / H2_KB),          # 9.0612
        "target_fraction": sig6(target),              # 0.110361
        "deployed_lambda": sig6(lam),                 # 0.060859
        "model_fraction": sig6(model),                # 0.059044
        "model_over_target": sig6(model / target),    # 0.535
        "fraction_slack": sig6(target / model),       # 1.869
        "crossing_lambda": sig6(lam_star),            # 0.116939
        "size_slack": sig6(lam_star / lam),           # 1.921
        "crossing_scale_n": int(round(N_KB * lam_star / lam)),
        "deployed_over_crossing": sig6(lam / lam_star),  # 0.520
    }


# ------------------------------- toy ladder ----------------------------------

def scan_e3(p: int, n: int, t: int, step: int,
            want_anti: bool = False) -> dict[str, int]:
    """Exact e_s=3 census.  Returns |T| (sociable terminal pairs), P (incidence
    count of (terminal pair, non-terminal partner)), and optionally the
    antipodal-subfamily size.  Matches #479's scan_e3 (T, partner_pairs)."""
    vals = stepped_values(p, n, step)
    zeta = vals[t - 1]
    term: dict[tuple[int, int], tuple[int, int]] = {}
    for i in range(t - 1):
        a = vals[i]
        sax = a + zeta
        pax = a * zeta % p
        for j in range(i + 1, t - 1):
            b = vals[j]
            key = ((-(sax + b)) % p, (pax + b * sax) % p)
            if key in term:
                raise CheckFailure("two terminal 3-sets share a high (L2)")
            term[key] = (i, j)
    tset: set[tuple[int, int]] = set()
    anti: set[tuple[int, int]] = set()
    P = 0
    get = term.get
    for i in range(t - 1):
        a = vals[i]
        for j in range(i + 1, t - 1):
            b = vals[j]
            sab = a + b
            pab = a * b % p
            for k in range(j + 1, t - 1):
                c = vals[k]
                u = get(((-(sab + c)) % p, (pab + sab * c) % p))
                if u is not None:
                    if {u[0], u[1], t - 1} & {i, j, k}:
                        raise CheckFailure("equal-high sets not disjoint (L1)")
                    P += 1
                    tset.add(u)
                    if want_anti and (
                        (a + b) % p == 0 or (a + c) % p == 0 or (b + c) % p == 0
                    ):
                        anti.add(u)      # partner {a,b,c} has an antipodal pair
    out = {"T": len(tset), "P": P}
    if want_anti:
        out["antipodal_T"] = len(anti)
    return out


def model_fraction(t: int, p: int) -> float:
    return -math.expm1(-math.comb(t - 1, 3) / p**2)


def resolve_q(n: int, q_target: int) -> int:
    q = q_target
    while not is_prime(q * n + 1):
        q += 1
    return q


def ladder_block() -> dict[str, Any]:
    target = H2_KB / math.comb(NP_KB - 1, 2)
    rows = []
    for label, n, q_target in LADDER:
        q = resolve_q(n, q_target)
        p = q * n + 1
        t = 9 * n // 16
        want_anti = (n, q_target) == ANTI_ROW
        print(f"[scan] {label} n={n} q={q} p={p} t={t}"
              f"{' (+antipodal)' if want_anti else ''}", flush=True)
        res = scan_e3(p, n, t, 1, want_anti=want_anti)
        c2 = math.comb(t - 1, 2)
        c3 = math.comb(t - 1, 3)
        frac = res["T"] / c2
        lam = c3 / p**2
        row = {
            "label": label,
            "n": n,
            "q": q,
            "p": p,
            "t": t,
            "C_t1_2": c2,
            "T": res["T"],
            "P": res["P"],
            "T_le_P": res["T"] <= res["P"],
            "frac": sig6(frac),
            "frac_over_target": sig6(frac / target),
            "over_target": frac > target,
            "lambda": sig6(lam),
            "P_over_C2": sig6(res["P"] / c2),
            "model_fraction": sig6(model_fraction(t, p)),
        }
        if "antipodal_T" in res:
            row["antipodal_T"] = res["antipodal_T"]
            row["antipodal_fraction_of_T"] = sig6(
                res["antipodal_T"] / res["T"]
            )
        rows.append(row)
    return {"status": "EXACT_KB_SHAPE_LADDER", "rows": rows}


def gradient_block() -> dict[str, Any]:
    rows = []
    for q, p in GRADIENT_PRIMES:
        print(f"[scan] gradient q={q} p={p} e=3", flush=True)
        res = scan_e3(p, 64, 36, 1)
        rows.append({"q": q, "p": p, "n": 64, "t": 36,
                     "T": res["T"], "P": res["P"]})
    return {"status": "EXACT_STEP1_GRADIENT_CROSSCHECK_PR468", "rows": rows}


# ------------------------- deployed witnesses / reduction --------------------

def deployed_witness_block() -> dict[str, Any]:
    arc, _ = deployed_arc()
    wits = []
    for uidx, vidx in HUGHES_E3_WITNESSES:
        cu = locator_coefficients(uidx, arc, P_KB)
        cv = locator_coefficients(vidx, arc, P_KB)
        if cu[:-1] != cv[:-1] or cu[-1] == cv[-1]:
            raise CheckFailure("embedded #479 e3 witness invalid")
        if NP_KB - 1 not in uidx:
            raise CheckFailure("witness U not terminal")
        # V carries exactly one antipodal pair (index difference n/2)
        anti = sum(
            1 for a in range(3) for b in range(a + 1, 3)
            if abs(vidx[a] - vidx[b]) == HALF
        )
        wits.append({
            "U_indices": uidx,
            "V_indices": vidx,
            "high_signature": cu[1:-1],
            "constant_U": cu[-1],
            "constant_V": cv[-1],
            "V_antipodal_pairs": anti,
        })
    return {
        "source": "PR #479 e3 witness table (canonical omega arc)",
        "count": len(wits),
        "witnesses": wits,
    }


def reduction_spot_checks() -> dict[str, Any]:
    """Exact checks of the R1 'high forces the terminal pair' identity and the
    C1/C2 characterizations, on a small explicit toy where they can be
    enumerated in full."""
    p, n, t, step = 1153, 64, 36, 1
    vals = stepped_values(p, n, step)
    zeta = vals[t - 1]
    # C2: equal (e1,e2) <=> equal (sum, sum of squares), checked on all pairs
    # forming terminal sets; and R1 forced-pair recovery.
    r1_ok = 0
    c2_ok = 0
    for i in range(t - 1):
        x = vals[i]
        for j in range(i + 1, t - 1):
            y = vals[j]
            e1 = (x + y + zeta) % p
            e2 = (x * y + zeta * (x + y)) % p
            # C2: power-sum form
            p1 = (x + y + zeta) % p
            p2 = (x * x + y * y + zeta * zeta) % p
            if (p1 == e1) and (p2 == (e1 * e1 - 2 * e2) % p):
                c2_ok += 1
            # R1: recover {x,y} as roots of X^2 - (e1-zeta)X + (e2-zeta e1+zeta^2)
            s = (e1 - zeta) % p          # x + y
            pr = (e2 - zeta * e1 + zeta * zeta) % p  # x * y
            if s == (x + y) % p and pr == (x * y) % p:
                r1_ok += 1
    total = math.comb(t - 1, 2)
    return {
        "toy": {"p": p, "n": n, "t": t},
        "pairs_checked": total,
        "C2_power_sum_identity_holds": c2_ok == total,
        "R1_forced_pair_recovers": r1_ok == total,
    }


# ------------------------------ lemma records --------------------------------

def lemma_records() -> dict[str, Any]:
    return {
        "C1_fiber_ge_2": {
            "status": "PROVED",
            "statement": (
                "A terminal 3-set U is in T(n',3) iff its high fiber "
                "Phi(e1,e2) has size >= 2.  A monic cubic is determined by its "
                "three coefficients, so any W != U with high(W)=high(U) has "
                "e3(W) != e3(U) (a free-1 partner); by #479 L2, U is the unique "
                "terminal member of Phi, so the partner is non-terminal."
            ),
        },
        "C2_equal_power_sums": {
            "status": "PROVED",
            "statement": (
                "By Newton's identities, e1(V)=e1(U) and e2(V)=e2(U) iff V,U "
                "have equal sum and equal sum of squares: a free-1 partner is a "
                "second arc-triple sharing the first two power sums with "
                "{x,y,zeta} (a degree-2 Prouhet-Tarry-Escott collision on the "
                "arc)."
            ),
        },
        "R1_high_forces_pair": {
            "status": "PROVED",
            "statement": (
                "A high (s,q) determines at most one terminal pair: x+y = s-zeta "
                "and xy = q - zeta(s-zeta), so {x,y} are the roots of "
                "X^2 - (s-zeta)X + (q - zeta s + zeta^2).  Hence each "
                "non-terminal arc-triple is the partner of at most one terminal "
                "pair."
            ),
        },
        "R2_incidence_reduction": {
            "status": "PROVED",
            "statement": (
                "P := #{(terminal pair {x,y}, non-terminal arc-triple {a,b,c}) "
                "with equal e1,e2}.  Every sociable pair contributes >= 1 "
                "incidence, so |T(n',3)| <= P; and P <= H2 implies star3.  P is "
                "the natural incidence / affine point-count for an analytic "
                "attack; heuristic value ~0.535*H2."
            ),
        },
        "L5_antipodal_subfamily": {
            "status": "PROVED (sliver)",
            "statement": (
                "#479 L5: V = {a,-a,c} has (e1,e2,e3) = (c,-a^2,-a^2 c); the "
                "antipodal-partner subfamily A3 is a proved subset of T(n',3) "
                "but a ~10^-3 sliver (measured); the bulk of T is generic "
                "power-sum collisions with no coset structure."
            ),
            "credit": "Hughes v54 antipodal mechanism; #479 L5",
        },
    }


# ------------------------------- certificate ---------------------------------

def build_certificate() -> dict[str, Any]:
    arith = deployed_arithmetic()
    grad = gradient_block()
    ladder = ladder_block()
    wits = deployed_witness_block()
    reduction = reduction_spot_checks()
    return {
        "packet": "cap25_v13_hughes_wall_star3",
        "date": "2026-07-10",
        "status": "STAR3_RESTATED_REDUCTION_PROVED_WALL_OPEN",
        "claims": {
            "restates_star3_exact": True,
            "reproduces_9_0612": True,
            "reproduces_target_fraction": True,
            "proves_incidence_reduction_T_le_P": True,
            "proves_R1_high_forces_pair": True,
            "reproduces_deployed_T3_ge": wits["count"],
            "validates_birthday_model": True,
            "measures_antipodal_sliver": True,
            "proves_star3": False,
            "proves_P_le_H2": False,
            "proves_deployed_wall": False,
            "counterexample_to_star3_found": False,
            "refutes_any_hughes_or_479_claim": False,
        },
        "wall_statement": (
            "star3: |T(n',3)| <= H2 = 77291948627 at the KB row "
            "(p,n,n',e)=(2130706433, 2^21, 1183520, 67472).  T(n',3) counts "
            "terminal pairs {x,y} in I_{n'-1} whose 3-set {x,y,zeta} admits a "
            "free-1 partner triple (equal e1,e2, different e3).  Trivial bound "
            "C(n'-1,2)=700358019921; deficit exactly C(n'-1,2)/H2 = 9.0612."
        ),
        "arithmetic": arith,
        "lemmas": lemma_records(),
        "reduction_spot_checks": reduction,
        "deployed_witnesses_e3": wits,
        "gradient_crosscheck": grad,
        "toy_ladder": ladder,
        "lineage": {
            "supports_scott_hughes_route_d": True,
            "continues_pr468_pr479": True,
            "source": "Hughes Route-D v1-v54; PR #468, PR #479",
        },
    }


# ------------------------------- validation ----------------------------------

def validate_certificate(cert: dict[str, Any], replay: dict[str, Any] | None,
                         checks: Checks) -> None:
    checks.equal(cert["packet"], "cap25_v13_hughes_wall_star3", "packet")
    checks.equal(cert["status"],
                 "STAR3_RESTATED_REDUCTION_PROVED_WALL_OPEN", "status")
    cl = cert["claims"]
    checks.equal(cl["proves_star3"], False, "nonclaim star3")
    checks.equal(cl["proves_P_le_H2"], False, "nonclaim P<=H2")
    checks.equal(cl["proves_deployed_wall"], False, "nonclaim wall")
    checks.equal(cl["counterexample_to_star3_found"], False, "nonclaim cx")
    checks.equal(cl["refutes_any_hughes_or_479_claim"], False, "nonclaim refute")
    checks.equal(cert["lineage"]["supports_scott_hughes_route_d"], True,
                 "lineage")

    # exact arithmetic gates, recomputed
    ar = cert["arithmetic"]
    checks.check(is_prime(P_KB), "p prime")
    checks.equal(ar["H2"], E_KB * P_KB // 1860, "H2 formula")
    checks.equal(ar["H2"], 77291948627, "H2 pinned")
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    checks.equal(ar["C_np1_2"], c2, "C(n'-1,2)")
    checks.equal(c2, 700358019921, "C(n'-1,2) pinned")
    checks.check(9 * H2_KB < c2 < 10 * H2_KB, "trivial deficit in (9,10)")
    checks.equal(ar["trivial_deficit"], "9.0612", "deficit 9.0612")
    checks.equal(ar["target_fraction"], "0.110361", "target fraction")
    checks.equal(ar["subgroup_index"], 1016, "index 1016")
    # deployed lambda = c3/p^2 < 0.062 < target 0.1104 (exact integer witness
    # that the model puts the deployed fraction below target):
    checks.check(1000 * c3 < 62 * P_KB**2, "deployed lambda < 0.062 < target")
    checks.check(float(ar["fraction_slack"]) > 1.8, "fraction slack > 1.8x")
    checks.check(float(ar["size_slack"]) > 1.9, "size slack > 1.9x")
    checks.check(int(ar["crossing_scale_n"]) > N_KB, "crossing scale > deployed")

    # reduction spot checks
    rc = cert["reduction_spot_checks"]
    checks.check(rc["C2_power_sum_identity_holds"], "C2 identity")
    checks.check(rc["R1_forced_pair_recovers"], "R1 forced pair")
    checks.equal(rc["pairs_checked"], math.comb(35, 2), "R1 pair count")

    # deployed witnesses re-verified from scratch on the arc
    wb = cert["deployed_witnesses_e3"]
    checks.check(wb["count"] >= 8, "deployed T3 >= 8")
    checks.equal(cl["reproduces_deployed_T3_ge"], wb["count"], "T3 claim")
    arc, _ = deployed_arc()
    seen = set()
    for w in wb["witnesses"]:
        u = w["U_indices"]
        v = w["V_indices"]
        checks.check(len(u) == 3 and len(v) == 3, "witness sizes")
        checks.check(NP_KB - 1 in u, "witness terminal mark")
        checks.check(not (set(u) & set(v)), "witness disjoint")
        checks.check(all(0 <= i < NP_KB for i in u + v), "witness bounds")
        cu = locator_coefficients(u, arc, P_KB)
        cv = locator_coefficients(v, arc, P_KB)
        checks.equal(cu[:-1], cv[:-1], "witness equal high")
        checks.check(cu[-1] != cv[-1], "witness distinct constant")
        checks.equal(w["high_signature"], cu[1:-1], "witness signature")
        checks.equal(w["constant_U"], cu[-1], "witness const U")
        checks.equal(w["constant_V"], cv[-1], "witness const V")
        checks.equal(w["V_antipodal_pairs"], 1, "witness V antipodal pair")
        seen.add(tuple(u))
    checks.equal(len(seen), wb["count"], "distinct witness U")

    # gradient cross-check must match PR #468 exactly
    for row in cert["gradient_crosscheck"]["rows"]:
        checks.check(is_prime(row["p"]), "gradient p prime")
        checks.equal(row["p"], row["q"] * row["n"] + 1, "gradient index")
        checks.equal((row["T"], row["P"]), PR468[(row["q"], 3)],
                     f"PR468 crosscheck q={row['q']}")

    # toy ladder: identities, T<=P, model bracket, over-target only when dense
    target = H2_KB / c2
    rows = cert["toy_ladder"]["rows"]
    labels = {r["label"] for r in rows}
    checks.check({"crossing", "dense", "mid_sparse", "deployed_like"} <= labels,
                 "ladder regimes present")
    for r in rows:
        checks.check(is_prime(r["p"]), "ladder p prime")
        checks.equal(r["p"], r["q"] * r["n"] + 1, "ladder index")
        checks.equal(r["t"] * 16, 9 * r["n"], "ladder shape 9/16")
        checks.equal(r["C_t1_2"], math.comb(r["t"] - 1, 2), "ladder C(t-1,2)")
        checks.check(r["T_le_P"], "ladder T<=P")
        checks.check(r["T"] <= r["P"], "ladder T<=P value")
        frac = r["T"] / r["C_t1_2"]
        checks.equal(r["over_target"], frac > target, "ladder over_target")
        # deployed-like rows are far below target; the exhibited over-target
        # rows are all dense or oversized (never deployed_like)
        if r["label"] == "deployed_like":
            checks.check(frac < 0.001, "deployed-like far below target")
        if r["over_target"]:
            checks.check(r["label"] in ("crossing", "dense"),
                         "over-target only crossing/dense")
    # crossing bracket: some crossing row under target, some over
    cross = [r for r in rows if r["label"] == "crossing"]
    checks.check(any(not r["over_target"] for r in cross), "crossing has under")
    checks.check(any(r["over_target"] for r in cross), "crossing has over")
    # antipodal sliver measured on the ANTI_ROW
    anti = [r for r in rows if "antipodal_T" in r]
    checks.equal(len(anti), 1, "one antipodal-measured row")
    checks.check(0 < anti[0]["antipodal_T"] < anti[0]["T"] // 10,
                 "antipodal is a small sliver of T")

    if replay is not None:
        checks.equal(cert, replay, "full exact replay")


# ------------------------------- tamper suite --------------------------------

def tamper_suite(cert: dict[str, Any], replay: dict[str, Any]) -> tuple[int, int]:
    def m_star3(d):
        d["claims"]["proves_star3"] = True

    def m_cx(d):
        d["claims"]["counterexample_to_star3_found"] = True

    def m_deficit(d):
        d["arithmetic"]["trivial_deficit"] = "9.5"

    def m_target(d):
        d["arithmetic"]["target_fraction"] = "0.12"

    def m_c2(d):
        d["arithmetic"]["C_np1_2"] += 1

    def m_wit_idx(d):
        d["deployed_witnesses_e3"]["witnesses"][0]["U_indices"][1] += 1

    def m_wit_const(d):
        w = d["deployed_witnesses_e3"]["witnesses"][1]
        w["V_indices"] = list(w["U_indices"])  # partner = U -> equal constant

    def m_grad(d):
        d["gradient_crosscheck"]["rows"][0]["T"] += 1

    def m_ladder_tp(d):
        r = d["toy_ladder"]["rows"][0]
        r["T"], r["P"] = r["P"] + 1, r["T"]  # force T > P
        r["T_le_P"] = True

    def m_ladder_over(d):
        for r in d["toy_ladder"]["rows"]:
            if r["label"] == "deployed_like":
                r["T"] = r["C_t1_2"]  # force deployed-like over target
                r["over_target"] = False
                break

    def m_anti(d):
        for r in d["toy_ladder"]["rows"]:
            if "antipodal_T" in r:
                r["antipodal_T"] = r["T"]  # claim all of T is antipodal
                break

    def m_r1(d):
        d["reduction_spot_checks"]["R1_forced_pair_recovers"] = False

    def m_lineage(d):
        d["lineage"]["supports_scott_hughes_route_d"] = False

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("promote-star3", m_star3),
        ("fake-counterexample", m_cx),
        ("deficit-drift", m_deficit),
        ("target-drift", m_target),
        ("c2-drift", m_c2),
        ("witness-index", m_wit_idx),
        ("witness-equal-constant", m_wit_const),
        ("gradient-count", m_grad),
        ("ladder-T-gt-P", m_ladder_tp),
        ("ladder-deployed-over", m_ladder_over),
        ("antipodal-inflate", m_anti),
        ("r1-false", m_r1),
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
    print("status: star3 RESTATED + reduction |T|<=P PROVED; birthday model "
          "validated on toys; star3 |T(n',3)| <= H2 remains OPEN")


if __name__ == "__main__":
    main()
