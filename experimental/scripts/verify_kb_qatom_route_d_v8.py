#!/usr/bin/env python3
"""KB-MCA Route-D v8: B1 uniqueness REFUTED by coset constant-shift padding.

Main theorem:
  On D = mu_n with n=2^21, e0=2^17 | n, the e0-cosets have locators X^{e0}-a
  and form a free-1 pencil of size n/e0=16.
  Padding any two such cosets with a common R of size m-e0 yields two distinct
  m-subsets with the same depth-w monic prefix for every w < e0 (in particular
  the deployed w=67471). Hence M_m^{max} >= 2, so B1 uniqueness is FALSE.

  Stronger: one can fit k<=10 cosets disjoint from a single R, giving
  M_m^{max} >= 10 at deployed (m,w).

B2 sparseness law from v7 remains; criterion must use M_m >= 10 (or exact M_m).

  python3 experimental/scripts/verify_kb_qatom_route_d_v8.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v8.py --check
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v8"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v8.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v8.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v8.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
J = 981_104
W = 67_471
M = 913_632  # core size = j - (w+1) used as m-subset weight in B1
# Wait: in our B1, m-subsets have size M_CORE = j-e for can-cores, but the
# uniqueness question was for m-subset fibers of size M = can-core size.
# Double-check naming from v5: m = |C| = j - e = 913632, w=67471 for Phi_w on cores.
# The padding construction uses weight mu = M = 913632.

E0 = 2**17  # 131072
PACK_J = 17
TARGET = 274_836_936_291_722_953
B_GEN = 67_472 * P


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def prim_root(p: int) -> int:
    fac: list[int] = []
    n = p - 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no prim root")


def domain_vals(p: int, n: int) -> list[int]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    return [pow(om, i, p) for i in range(n)]


def monic(pts: list[int], p: int) -> list[int]:
    poly = [1]
    for v in pts:
        new = [0] * (len(poly) + 1)
        mv = (-v) % p
        for i, c in enumerate(poly):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] + c * mv) % p
        poly = new
    return poly


def lemma_coset_locator() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "coset_locator_is_pure_power",
        "statement": (
            "Let D = <omega> be cyclic of order n in F_p^x with n | (p-1). "
            "Let e0 | n and H = <omega^{n/e0}> the unique subgroup of order e0. "
            "For any coset gH, the monic locator is "
            "Lambda_{gH}(X) = X^{e0} - g^{e0}."
        ),
        "proof": [
            "The elements of gH are g, g zeta, ..., g zeta^{e0-1} where zeta = omega^{n/e0} "
            "has order e0.",
            "Pi_{k=0}^{e0-1} (X - g zeta^k) = g^{e0} Pi (g^{-1} X - zeta^k) "
            "= g^{e0} ((g^{-1} X)^{e0} - 1) = X^{e0} - g^{e0}.",
        ],
    }


def lemma_coset_free1_pencil() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "all_e0_cosets_share_one_free1_prefix",
        "statement": (
            "For e0 | n, every coset locator is of the form X^{e0} - a. "
            "Hence all n/e0 cosets share the same length-(e0-1) monic high-coefficient "
            "prefix (all zeros) and form a single free-1 fiber of size exactly n/e0."
        ),
        "proof": [
            "Immediate from Lambda_{gH} = X^{e0} - g^{e0}: only the constant term depends on g.",
            "Different cosets are disjoint and partition D, so there are exactly n/e0 of them, "
            "matching the free-1 packing ceiling floor(n/e0)=n/e0.",
        ],
        "deployed_e0": E0,
        "deployed_pencil_size": N // E0,
    }


def lemma_padding_collision() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "padding_CS_gives_depth_w_collision",
        "statement": (
            "Let e0 >= 1, w < e0, and m >= e0 with n >= m + e0. "
            "Suppose U, V are disjoint e0-subsets of D whose monic locators differ by a "
            "nonzero constant c. Let R be any (m-e0)-subset of D\\\\(U cup V). "
            "Set S = R cup U and T = R cup V. Then |S|=|T|=m, S != T, and "
            "Phi_w(S)=Phi_w(T)."
        ),
        "proof": [
            "Lambda_S = Lambda_R Lambda_U and Lambda_T = Lambda_R Lambda_V, so "
            "Lambda_S - Lambda_T = Lambda_R (Lambda_U - Lambda_V) = c Lambda_R.",
            "Hence deg(Lambda_S - Lambda_T) = deg(Lambda_R) = m - e0.",
            "The first w monic high coefficients of a monic degree-m polynomial are the "
            "coefficients of X^{m-1},...,X^{m-w}. These vanish in the difference whenever "
            "deg(difference) <= m-w-1, i.e. m-e0 <= m-w-1, i.e. e0 >= w+1.",
            "Under the weaker hypothesis e0 > w we have m-e0 < m-w, so coefficients of "
            "X^{m-1},...,X^{m-w} still vanish in the difference (deg <= m-e0 <= m-w-1 when "
            "e0 >= w+1; if only e0 > w then deg <= m-w-1 still holds for integer e0 >= w+1). "
            "For e0 > w, m-e0 <= m-w-1 iff e0 >= w+1. So we require e0 >= w+1.",
            "Deployed uses e0=2^17=131072 > w+1=67472, and m-e0=782560 <= m-w-1=846160.",
        ],
        "deployed_numbers": {
            "e0": E0,
            "w": W,
            "m": M,
            "m_minus_e0": M - E0,
            "m_minus_w_minus_1": M - W - 1,
            "deg_ok": (M - E0) <= (M - W - 1),
            "n_minus_2e0": N - 2 * E0,
            "room_for_R": (N - 2 * E0) >= (M - E0),
        },
    }


def lemma_B1_refuted() -> dict[str, Any]:
    # max k cosets disjoint from one R: n - k*e0 >= m - e0 => k <= 1 + (n-m)/e0
    k_max = 1 + (N - M) // E0
    return {
        "status": "PROVED",
        "name": "deployed_Mm_at_least_2_refutes_uniqueness",
        "statement": (
            f"At deployed (n,m,w)=({N},{M},{W}) with e0={E0}=2^17 | n, the coset "
            "constant-shift padding construction produces at least two distinct m-subsets "
            "with the same depth-w monic prefix. Therefore M_m^{max} >= 2, and the B1 "
            "claim M_m^{max} <= 1 is FALSE."
        ),
        "proof": [
            "By lemma_coset_locator and lemma_coset_free1_pencil, any two distinct e0-cosets "
            "form a CS pair.",
            "Choose two cosets U,V and R subset D\\\\(U cup V) with |R|=m-e0 "
            f"(possible because n-2*e0={N-2*E0} >= m-e0={M-E0}).",
            "Apply lemma_padding_collision with e0 > w (in fact e0 >= w+1).",
            "Hence Phi_w(R cup U)=Phi_w(R cup V) with R cup U != R cup V.",
        ],
        "lower_bound_Mm": 2,
        "improved_lower_bound_Mm": k_max,
        "improved_lower_bound_reason": (
            f"n-k*e0 >= m-e0 allows k <= 1+(n-m)/e0 = {k_max} cosets simultaneously "
            "disjoint from one R of size m-e0; all R cup U_i then share one Phi_w prefix."
        ),
    }


def lemma_revised_criterion() -> dict[str, Any]:
    Mm_lo = 1 + (N - M) // E0
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "atom_criterion_with_Mm_lower_bound",
        "statement": (
            f"Since M_m^{{max}} >= {Mm_lo}, the v5 criterion requiring M_m <= 1 is impossible. "
            "The corrected sufficient condition is: if M_m^{{max}} <= K and "
            "U_res <= floor(target/(pack_ceil*K)) for some K >= M_m^{{max}}, then |R| <= target. "
            f"Using only the proved lower bound, any proof must allow K >= {Mm_lo}, which "
            f"tightens the U_res budget to <= floor(target/(17*{Mm_lo}))."
        ),
        "U_res_budget_if_K_eq_lower": TARGET // (PACK_J * Mm_lo),
        "U_res_tp_budget_if_K_eq_lower": B_GEN // (PACK_J * Mm_lo),
        "log2_U_res_atom_tightened": math.log2(max(TARGET // (PACK_J * Mm_lo), 1)),
    }


def toy_suite() -> dict[str, Any]:
    """Verify coset locators and padding on small dyadic n."""
    tests = []
    for p, n, e0, w, m in [
        (17, 16, 4, 2, 6),
        (17, 16, 4, 2, 8),
        (97, 32, 8, 5, 12),
        (97, 32, 8, 3, 20),
        (193, 64, 16, 10, 40),
    ]:
        ensure(n % e0 == 0, "e0|n")
        vals = domain_vals(p, n)
        step = n // e0
        U = frozenset(range(0, n, step))
        V = frozenset(range(1, n, step))
        ensure(len(U) == e0 and len(V) == e0 and U.isdisjoint(V), "cosets")
        polyU = monic([vals[i] for i in sorted(U)], p)
        polyV = monic([vals[i] for i in sorted(V)], p)
        # middle coeffs zero, constants differ
        ensure(all(x == 0 for x in polyU[1:e0]), f"U middle {polyU[1:e0]}")
        ensure(all(x == 0 for x in polyV[1:e0]), f"V middle")
        ensure(polyU[-1] != polyV[-1], "const differ")
        rest = sorted(set(range(n)) - U - V)
        ensure(len(rest) >= m - e0, "room")
        R = frozenset(rest[: m - e0])
        S, T = R | U, R | V
        polyS = monic([vals[i] for i in sorted(S)], p)
        polyT = monic([vals[i] for i in sorted(T)], p)
        match = polyS[1 : w + 1] == polyT[1 : w + 1]
        ensure(match, f"Phi_w fail {(p,n,e0,w,m)}")
        # multi-coset lower bound when possible
        k_max = 1 + (n - m) // e0
        tests.append(
            {
                "p": p,
                "n": n,
                "e0": e0,
                "w": w,
                "m": m,
                "Phi_w_match": match,
                "k_max_cosets": k_max,
                "const_U": polyU[-1],
                "const_V": polyV[-1],
            }
        )
    # Deployed arithmetic gates
    ensure(N % E0 == 0, "deployed e0|n")
    ensure(E0 >= W + 1, "e0 >= w+1")
    ensure(M >= E0, "m >= e0")
    ensure(N - 2 * E0 >= M - E0, "room for R")
    ensure(M - E0 <= M - W - 1, "deg condition")
    k_max = 1 + (N - M) // E0
    ensure(k_max >= 2, "k_max")
    return {"status": "PASS", "padding_tests": tests, "deployed_k_max": k_max}


def build() -> dict[str, Any]:
    k_max = 1 + (N - M) // E0
    return {
        "packet": "kb_qatom_route_d_v8",
        "title": "B1 uniqueness REFUTED by coset CS padding; revised budgets",
        "status": "PROVED_REFUTATION_OF_Mm_UNIQUENESS",
        "claims": {
            "proves_Mm_le_1": False,
            "refutes_Mm_le_1": True,
            "proves_Mm_ge_2": True,
            "proves_Mm_ge_k_max": True,
            "proves_coset_locator": True,
            "proves_padding_collision": True,
        },
        "deployed": {
            "n": N,
            "m": M,
            "w": W,
            "e0": E0,
            "num_cosets": N // E0,
            "Mm_lower_bound": k_max,
            "pack_j": PACK_J,
            "U_res_budget_if_K_eq_Mm_lower": TARGET // (PACK_J * k_max),
            "U_res_tp_if_K_eq_Mm_lower": B_GEN // (PACK_J * k_max),
            "log2_U_res_atom_tightened": math.log2(max(TARGET // (PACK_J * k_max), 1)),
        },
        "lemmas": {
            "coset_locator": lemma_coset_locator(),
            "coset_free1_pencil": lemma_coset_free1_pencil(),
            "padding_collision": lemma_padding_collision(),
            "B1_refuted": lemma_B1_refuted(),
            "revised_criterion": lemma_revised_criterion(),
        },
        "toy_suite": toy_suite(),
        "impact_on_program": {
            "v5_criterion_Mm_le_1": "DEAD — premise false at deployed",
            "B1_as_uniqueness": "REFUTED",
            "B2_still_open": (
                "U_res / residual can-core prefix-image bound still needed; "
                f"budgets tighten by factor k_max={k_max} if K=M_m is only known via lower bound"
            ),
            "next": (
                "Determine exact M_m (or a tight upper bound), or bypass M_m by bounding "
                "N_can_prim / residual core-prefix image directly without uniqueness"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    toys = cert["toy_suite"]["padding_tests"]
    tbl = "\n".join(
        f"| {t['p']} | {t['n']} | {t['e0']} | {t['w']} | {t['m']} | {t['Phi_w_match']} | {t['k_max_cosets']} |"
        for t in toys
    )
    return f"""# KB-MCA Route-D v8: B1 uniqueness REFUTED

Status: `PROVED REFUTATION` — `M_m^{{max}} <= 1` is **FALSE** at deployed parameters.

## Main theorem

On the deployed domain `D = mu_n`, `n = 2^{{21}}`, set `e0 = 2^{{17}} = {E0}` (divides `n`).

1. Cosets of the order-`e0` subgroup have locators `X^{{e0}} - a` and form one free-1
   pencil of size `n/e0 = {N//E0}`.
2. Padding any two such cosets with a common `R` of size `m - e0` produces two
   distinct m-subsets with **identical** depth-`w` monic prefixes for deployed `w`.
3. Therefore **`M_m^{{max}} >= 2`**. Uniqueness is refuted.

### Improved lower bound

```text
M_m^{{max}}  >=  k_max  =  1 + floor((n-m)/e0)  =  {d['Mm_lower_bound']}
```

(one can keep `k_max` cosets simultaneously disjoint from a single admissible `R`).

## Proof ingredients

### Coset locator
`Lambda_{{gH}}(X) = X^{{e0}} - g^{{e0}}` for `|H|=e0 | n`.

### Padding
`Lambda_{{R cup U}} - Lambda_{{R cup V}} = c Lambda_R` has degree `m-e0 <= m-w-1`
when `e0 >= w+1`, so the first `w` high monic coefficients agree.

### Deployed arithmetic
```text
e0 = {E0} | n
e0 >= w+1 = {W+1}
m-e0 = {M-E0} <= m-w-1 = {M-W-1}
n-2*e0 = {N-2*E0} >= m-e0
```

## Impact

| Previous hope | Status |
|---|---|
| B1: `M_m <= 1` | **REFUTED** |
| v5 criterion needing `M_m <= 1` | **Dead premise** |
| B2 / residual core-prefix image | Still OPEN; still the right wall |

### Revised budgets (if one only knows `M_m >= k_max` and uses `K = k_max`)

```text
U_res <= target/(17 * {d['Mm_lower_bound']}) = {d['U_res_budget_if_K_eq_Mm_lower']}
         ≈ 2^{{{d['log2_U_res_atom_tightened']:.2f}}}
```

A tight **upper** bound on `M_m` would restore a better budget.

## Toy verification of padding

| p | n | e0 | w | m | Phi_w match | k_max |
|---|---|---|---|---|---|---|
{tbl}

## Next real math

1. Upper-bound `M_m` (coset pencil gives only a lower bound of {d['Mm_lower_bound']}).
2. Or bound residual can-core `Phi_w`-image (B2) without going through small `M_m`.
3. Do not spend effort proving `M_m <= 1`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v8.py
python3 experimental/scripts/verify_kb_qatom_route_d_v8.py --check
```
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    cert = build()
    if args.check and CERT_PATH.exists():
        old = json.loads(CERT_PATH.read_text())
        ensure(old["claims"] == cert["claims"], "claims drift")
        ensure(old["deployed"]["Mm_lower_bound"] == cert["deployed"]["Mm_lower_bound"], "bound drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v8\n\nB1 uniqueness REFUTED by coset CS padding.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v8.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v8 report\n\nstatus: {cert['status']}\n"
        f"Mm_lower_bound: {cert['deployed']['Mm_lower_bound']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  B1 M_m <= 1: REFUTED")
    print(f"  M_m >= {cert['deployed']['Mm_lower_bound']} (coset padding)")
    print(f"  tightened U_res atom budget: {cert['deployed']['U_res_budget_if_K_eq_Mm_lower']}")
    print(f"  toy padding tests: {len(cert['toy_suite']['padding_tests'])} OK")


if __name__ == "__main__":
    main()
