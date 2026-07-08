#!/usr/bin/env python3
"""KB-MCA Route-D v6: B1 free-regime uniqueness + B2 U_res structure.

B1 PROVED regimes for M_m = max |m-subset depth-w fiber|:
  free=m-w=0 (w>=m): M_m <= 1
  free=1 (w=m-1):   M_m <= floor(n/m)  (constant-shift packing)

Deployed free = m-w = 846161: NOT in free-0/1; entropy still log2 avg ≈ -18820.

B2 PROVED:
  residual side e=w+1 has free=1, so |{U: Phi_w(U)=u}| <= floor(n/e)
  U_res(z) <= |R(z)|
  U_res(z) <= number of residual lex sides
  N_can_prim <= U_res * M_m  (v5)

Does not close deployed B1 (free>>1) or absolute U_res budget.

  python3 experimental/scripts/verify_kb_qatom_route_d_v6.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v6.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v6"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v6.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v6.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v6.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
J = 981_104
W = 67_471
E = W + 1
M = J - E
FREE_M = M - W  # free lower coeffs for m-locators at depth w
PACK_M_FREE1 = N // M  # floor(n/m) when free=1
PACK_E = N // E
PACK_J = (N - M) // E  # 17
TARGET = 274_836_936_291_722_953
B_GEN = 67_472 * P


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    if k > n - k:
        k = n - k
    s = 0.0
    for i in range(k):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


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


def aperiodic(S: frozenset[int], n: int) -> bool:
    for d in range(1, n):
        if n % d == 0 and frozenset((i + d) % n for i in S) == S:
            return False
    return True


def lemma_B1_free0() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Mm_unique_when_w_ge_m",
        "statement": (
            "If w >= m, then every depth-w monic-prefix fiber of m-subsets has size <= 1. "
            "In particular M_m^{max} <= 1."
        ),
        "proof": [
            "A monic degree-m polynomial has exactly m non-leading coefficients. "
            "Specifying w >= m of the high monic coefficients (the full coefficient vector "
            "when w=m, and overdetermined when w>m) determines at most one monic polynomial.",
            "A monic polynomial has at most one set of m distinct roots. "
            "Hence at most one m-subset lies in any depth-w fiber.",
        ],
        "deployed_applies": False,
        "deployed_free": FREE_M,
        "deployed_note": f"Deployed free = m-w = {FREE_M} >> 0, so free-0 does not apply.",
    }


def lemma_B1_free1() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Mm_pack_when_w_eq_m_minus_1",
        "statement": (
            "If w = m-1 (exactly one free lower coefficient), then the m-subsets sharing a "
            "fixed depth-w monic prefix form a constant-shift family of monic locators, "
            "and M_m^{max} <= floor(n/m)."
        ),
        "proof": [
            "Monic degree m with the top m-1 monic coefficients fixed: only the constant "
            "term remains free. That is a constant-shift pencil "
            "Lambda_c = X^m + a_1 X^{m-1} + ... + a_{m-1} X + c.",
            "If two distinct members both split completely over D into distinct roots, "
            "their root sets are disjoint: a shared root x would force Lambda_c(x)=Lambda_{c'}(x)=0 "
            "hence c=c'. Pack m-sets into a ground set of size n: at most floor(n/m) members.",
        ],
        "deployed_applies": False,
        "deployed_would_need_w": M - 1,
        "deployed_actual_w": W,
        "deployed_gap_in_w": (M - 1) - W,
        "bound_if_applied": PACK_M_FREE1,
    }


def lemma_B1_side_free1() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "side_e_subset_always_free1",
        "statement": (
            "For e = w+1, every depth-w monic-prefix fiber of e-subsets has size "
            "<= floor(n/e). (This is free = e-w = 1.)"
        ),
        "proof": [
            "Apply free-1 packing with m replaced by e=w+1: free = e-w = 1 automatically.",
        ],
        "deployed_bound": PACK_E,
        "deployed_applies": True,
    }


def lemma_B1_deployed_status() -> dict[str, Any]:
    log_avg = log2_binom(N, M) - W * math.log2(P)
    return {
        "status": "AUDIT",
        "name": "deployed_B1_status",
        "free_m": FREE_M,
        "log2_avg_m_fiber": log_avg,
        "conclusion": (
            "Deployed m-fiber uniqueness is outside the free-0/free-1 regimes. "
            "Entropy (log2 avg ≈ -18820) still predicts M_m^{max} is typically 0 or 1, "
            "but the only unconditional packing we prove for general free is the weak "
            "anticode / p^{free} envelope, which does not fit the atom. "
            "B1 at deployed remains OPEN as a uniqueness theorem for free=846161."
        ),
        "what_would_close_B1": (
            "Any proof that M_m^{max} <= 2^{53} (even much larger than 1) combines with "
            "a U_res bound; M_m^{max} <= 1 is the entropy-natural target."
        ),
    }


def lemma_B2_U_res_structure() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "U_res_structural_bounds",
        "statement": (
            "Let R(z) subset Fib_w(z) and U_res(z) = number of distinct monic length-w "
            "prefixes u of Lambda_U for residual/lex sides U of S in R(z). Then:\n"
            "(i) U_res(z) <= |R(z)|;\n"
            "(ii) for each u, the number of e-subsets with monic prefix u is <= floor(n/e);\n"
            "(iii) N_can_prim(z) <= U_res(z) * M_m^{max} (v5 routing);\n"
            "(iv) if M_m^{max} <= 1 then N_can_prim(z) <= U_res(z)."
        ),
        "proof": [
            "(i) Each residual S contributes one lex side and one u; map S |-> u has image size "
            "U_res and domain size |R|.",
            "(ii) Side free-1 packing (lemma_B1_side_free1).",
            "(iii)-(iv) Residual core routing (v5).",
        ],
        "budgets_if_Mm_one": {
            "U_res_for_atom": TARGET // PACK_J,
            "U_res_for_tp": B_GEN // PACK_J,
            "log2_atom": math.log2(TARGET // PACK_J),
            "log2_tp": math.log2(B_GEN // PACK_J),
        },
        "open": (
            "Prove an absolute upper bound U_res(z) <= target/17 without assuming |R| small. "
            "Circular bound U_res <= |R| does not close the atom alone."
        ),
    }


def lemma_B2_not_circular_partial() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "U_res_le_num_nonempty_side_fibers_global",
        "statement": (
            "U_res(z) is at most the number of depth-w monic prefixes u for which the "
            "e-subset fiber is nonempty AND at least one U in that fiber is the lex-min "
            "e-set of some S in R(z). In particular U_res(z) <= |{u : e-fiber(u) nonempty}| "
            "<= p^w, and more tightly U_res(z) <= C(n,e) with the free-1 refinement that "
            "the nonempty u are in bijection with constant-shift pencils that hit at least "
            "one residual lex side."
        ),
        "proof": [
            "By definition of U_res as a set of realized prefixes.",
            "Each nonempty e-fiber is one constant-shift pencil (free-1); distinct pencils "
            "have distinct length-w prefixes (the free constant does not affect the prefix).",
            "Hence nonempty e-prefixes inject into the set of such pencils, size <= C(n,e) "
            "and <= p^w.",
        ],
        "deployed_p_w_bits": W * math.log2(P),
        "deployed_note": (
            "p^w is ~2^{2.09e6}, far above the atom. The bound is structural, not finite-useful "
            "without a residual sparsity constraint on which pencils appear."
        ),
    }


def lemma_combined_criterion() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "atom_from_B1_and_B2",
        "statement": (
            "If M_m^{max} <= K and max_z U_res(z) <= floor(target_floor / (pack_ceil * K)) "
            "for a positive integer K, then max |R(z)| <= target_floor."
        ),
        "proof": [
            "N_can_prim <= U_res * M_m <= U_res * K.",
            "|R| <= pack * N_can_prim <= pack * K * U_res <= target.",
        ],
        "special_case_K_1": {
            "need_U_res_le": TARGET // PACK_J,
            "entropy_support_for_K_1": log2_binom(N, M) - W * math.log2(P),
        },
    }


def toy_suite() -> dict[str, Any]:
    """Verify free-0/free-1 on small fields; residual U_res structure."""
    results_free = []
    for p, n in [(17, 16), (97, 32)]:
        vals = domain_vals(p, n)
        for m in range(1, n):
            for free in (0, 1):
                w = m - free
                if w < 1:
                    continue
                if math.comb(n, m) > 80_000:
                    continue
                fibers: dict[tuple[int, ...], int] = defaultdict(int)
                for exps in itertools.combinations(range(n), m):
                    poly = monic([vals[i] for i in exps], p)
                    b = tuple(poly[1 : w + 1])
                    fibers[b] += 1
                maxM = max(fibers.values()) if fibers else 0
                if free == 0:
                    ensure(maxM <= 1, f"free0 fail p={p} m={m}")
                    bound = 1
                else:
                    bound = max(n // m, 1)
                    ensure(maxM <= bound, f"free1 fail p={p} m={m} max={maxM} bound={bound}")
                results_free.append(
                    {"p": p, "n": n, "m": m, "w": w, "free": free, "maxM": maxM, "bound": bound}
                )

    # residual U_res structure on j-fibers
    results_res = []
    for p, n, j, w in [
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (97, 32, 5, 2),
        (97, 32, 5, 3),
        (193, 64, 4, 2),
    ]:
        e = w + 1
        vals = domain_vals(p, n)
        fibers: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            poly = monic([vals[i] for i in exps], p)
            z = tuple(poly[1 : w + 1])
            fibers[z].append(frozenset(exps))
        max_U_res = 0
        max_R = 0
        max_U_per_u = 0
        max_S_per_u = 0
        for z, mem in fibers.items():
            R = [S for S in mem if aperiodic(S, n)]
            max_R = max(max_R, len(R))
            by_u_U: dict[tuple[int, ...], set[frozenset[int]]] = defaultdict(set)
            by_u_S: dict[tuple[int, ...], int] = defaultdict(int)
            for S in R:
                s = sorted(S)
                U = frozenset(s[:e])
                polyU = monic([vals[i] for i in sorted(U)], p)
                u = tuple(polyU[1 : w + 1])
                by_u_U[u].add(U)
                by_u_S[u] += 1
            max_U_res = max(max_U_res, len(by_u_U))
            if by_u_U:
                max_U_per_u = max(max_U_per_u, max(len(v) for v in by_u_U.values()))
                max_S_per_u = max(max_S_per_u, max(by_u_S.values()))
            ensure(max_U_per_u <= n // e or max_U_per_u == 0, "side free1")
            ensure(max_U_res <= max_R or max_R == 0, "U_res <= |R|")
        results_res.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "max_R": max_R,
                "max_U_res": max_U_res,
                "max_U_per_u": max_U_per_u,
                "max_S_per_u": max_S_per_u,
                "floor_n_e": n // e,
            }
        )

    return {
        "status": "PASS",
        "free01_checks": len(results_free),
        "free01_sample": results_free[:8] + results_free[-4:],
        "residual_rows": results_res,
    }


def build() -> dict[str, Any]:
    ensure(FREE_M == 846_161, f"free {FREE_M}")
    ensure(PACK_J == 17, f"pack_j {PACK_J}")
    return {
        "packet": "kb_qatom_route_d_v6",
        "title": "B1 free-regime uniqueness and B2 U_res structure",
        "status": "PARTIAL_PROVED_REGIMES_DEPLOYED_OPEN",
        "claims": {
            "proves_Mm_unique_free0": True,
            "proves_Mm_pack_free1": True,
            "proves_side_free1": True,
            "proves_deployed_Mm_unique": False,
            "proves_U_res_absolute_atom_budget": False,
            "proves_U_res_le_R_and_side_pack": True,
        },
        "deployed": {
            "m": M,
            "w": W,
            "e": E,
            "free_m": FREE_M,
            "pack_j": PACK_J,
            "pack_e": PACK_E,
            "pack_m_if_free1": PACK_M_FREE1,
            "log2_avg_m_fiber": log2_binom(N, M) - W * math.log2(P),
            "U_res_atom_budget_if_Mm_1": TARGET // PACK_J,
            "U_res_tp_budget_if_Mm_1": B_GEN // PACK_J,
        },
        "lemmas": {
            "B1_free0": lemma_B1_free0(),
            "B1_free1": lemma_B1_free1(),
            "B1_side_free1": lemma_B1_side_free1(),
            "B1_deployed_status": lemma_B1_deployed_status(),
            "B2_U_res_structure": lemma_B2_U_res_structure(),
            "B2_partial_global": lemma_B2_not_circular_partial(),
            "combined_criterion": lemma_combined_criterion(),
        },
        "toy_suite": toy_suite(),
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    toys = cert["toy_suite"]["residual_rows"]
    toy_tbl = "\n".join(
        f"| {r['p']} | {r['n']} | {r['w']} | {r['max_R']} | {r['max_U_res']} | "
        f"{r['max_U_per_u']} | {r['max_S_per_u']} | {r['floor_n_e']} |"
        for r in toys
    )
    return f"""# KB-MCA Route-D v6: B1 free-regime uniqueness and B2 U_res structure

Status: `PARTIAL` — free-0/free-1 uniqueness **PROVED**; deployed B1 **OPEN**; B2 structure **PROVED**, absolute budget **OPEN**.

## B1 — M_m uniqueness

### Theorem B1.0 — free = 0 (PROVED)

If `w >= m`, then `M_m^{{max}} <= 1`.

Proof: full monic coefficient vector determined; unique roots.

### Theorem B1.1 — free = 1 (PROVED)

If `w = m-1`, then `M_m^{{max}} <= floor(n/m)` by constant-shift packing.

### Theorem B1.side — e = w+1 always free = 1 (PROVED)

Depth-w fibers of e-subsets have size `<= floor(n/e) = {PACK_E}` at deployed.

### Deployed B1 status (AUDIT)

```text
m = {M}
w = {W}
free = m-w = {FREE_M}
log2(avg m-fiber) ≈ {d['log2_avg_m_fiber']:.2f}
```

Deployed is **far** from free-0 (`w=m`) and free-1 (`w=m-1={M-1}`): gap in w is `{M-1-W}`.
Entropy still says max is typically 0/1; unconditional uniqueness at free=`{FREE_M}` remains OPEN.

## B2 — U_res bounds

### Theorem B2.structure (PROVED)

1. `U_res(z) <= |R(z)|`
2. Each side-prefix u has `<= floor(n/e)` realizing e-subsets
3. `N_can_prim <= U_res * M_m^{{max}}`
4. If `M_m^{{max}} <= 1` then `N_can_prim <= U_res`

### Budgets if M_m = 1

```text
U_res <= {d['U_res_atom_budget_if_Mm_1']}  (~2^{{{math.log2(d['U_res_atom_budget_if_Mm_1']):.2f}}}) for K_rem atom form
U_res <= {d['U_res_tp_budget_if_Mm_1']}   (~2^{{{math.log2(d['U_res_tp_budget_if_Mm_1']):.2f}}}) for |D_prim|<=t*p
```

Absolute (non-circular) atom-scale bound on `U_res` is still OPEN.

## Combined criterion (PROVED conditional)

If `M_m^{{max}} <= K` and `U_res <= floor(target/(17 K))`, then `|R| <= target`.

## Toy suite

Free-0/free-1: {cert['toy_suite']['free01_checks']} checks, all OK.

Residual structure:

| p | n | w | max R | max U_res | max U/u | max S/u | floor(n/e) |
|---|---|---|---:|---:|---:|---:|---:|
{toy_tbl}

## What closes the atom

| Piece | Status |
|---|---|
| free-0 / free-1 uniqueness | PROVED (wrong free for deployed m) |
| side free-1 packing | PROVED (deployed) |
| residual routing N_can_prim <= U_res M_m | PROVED |
| deployed M_m^{{max}} <= 1 | **OPEN (B1)** |
| U_res <= target/17 | **OPEN (B2)** |

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v6.py
python3 experimental/scripts/verify_kb_qatom_route_d_v6.py --check
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
        ensure(old["deployed"]["free_m"] == cert["deployed"]["free_m"], "free drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v6\n\nB1 free regimes + B2 U_res structure.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v6.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v6 report\n\nstatus: {cert['status']}\nfree_m: {FREE_M}\n"
        f"log2_avg_m: {cert['deployed']['log2_avg_m_fiber']:.4f}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  deployed free m-w: {FREE_M}")
    print(f"  free-0 applies: False; free-1 applies: False")
    print(f"  side free-1 bound floor(n/e): {PACK_E}")
    print(f"  free01 toy checks: {cert['toy_suite']['free01_checks']}")
    print(f"  residual rows: {len(cert['toy_suite']['residual_rows'])}")


if __name__ == "__main__":
    main()
