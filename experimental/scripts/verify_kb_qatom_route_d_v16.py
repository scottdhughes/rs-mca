#!/usr/bin/env python3
"""KB-MCA Route-D v16: H_seam from SP support assignment + isolated residual marks.

Continues v15 injection attack with precise SP/top-seam identification and
mark definitions for isolated residual leaves.

Proved:
  (1) Top-seam ⇒ shift-pair: if S≠S' form a top-seam edge in G_z (same can-core,
      free-1 CS sides), then monic locators satisfy deg(Λ_S−Λ_{S'}) = j−w−1
      and Phi_w(S)=Phi_w(S')=z, i.e. (Λ_S,Λ_{S'}) is a depth-w shift pair at
      the maximal stratum e_trade = j−|C| = w+1 on the side factors (and
      deg(Λ_S−Λ_{S'}) = |C| = j−w−1 on full locators).
  (2) Assignment rule A_SP: first-match assigns every support that participates
      in a top-seam edge of G_z to the SP (or BC chart) cell.
  (3) H_seam from A_SP: residual supports (not assigned by A_SP) are
      matching-free in G_z. Combined with v15 matching-free mass law,
      |R| = N_can_prim and pack=1.
  (4) Honesty: existing SP package (grande_finale second moment, quotient
      pullback, primitive census OPEN) does NOT prove A_SP. SP is largely
      pair/image/census, not support assignment. H_seam is therefore
      conditional on A_SP (or an equivalent SP/BC support payment theorem).
  (5) Isolated residual mark schemes (definitions):
        μ_E5(S) = (min_exp(S), a_{w+1}(Λ_S)) ∈ {0..n-1} × F_p   (size n·p)
        μ_E5U(S) = (min_exp(U(S)), a_{w+1}(Λ_S))
        μ_E2-shape: need index in {0..t-1}; proposed
        μ_piv(S) = (i_*(S), λ_*(S)) with i_* first nonvanishing pivot row
        among ≤t affine packet rows after rank-drop deletion (ledger shape).
      Well-defined under residual hypotheses stated; injectivity OPEN.
  (6) Bridge: H_seam + injective μ_E5 or μ_piv ⇒ residual mass atom (v14/v15).
  (7) Toy bank: on matching-free aperiodic proxy, μ_E5 / μ_E5U / (min,c_U)
      are NOT injective (max fiber ≥2). Marks are candidates, not proofs.

Does NOT prove unconditional H_seam or mark injectivity or U(1116048)≤B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v16.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v16.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v16"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v16.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v16.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v16.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
M = J - E
TARGET = 274_836_936_291_722_953
N_P = N * P
T_P = T * P


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


def monic_rev(pts: list[int], p: int) -> list[int]:
    poly = [1]
    for v in pts:
        new = [0] * (len(poly) + 1)
        mv = (-v) % p
        for i, c in enumerate(poly):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] + c * mv) % p
        poly = new
    return poly


def phi_w(poly: list[int], w: int) -> tuple[int, ...]:
    return tuple(poly[1 : w + 1])


def deg_diff_monic(pa: list[int], pb: list[int], deg: int, p: int) -> int:
    """Highest k with [X^k](pa-pb) nonzero; monic rev poly length deg+1."""
    for k in range(deg - 1, -1, -1):
        idx = deg - k
        if idx < len(pa) and (pa[idx] - pb[idx]) % p != 0:
            return k
    return -1


def aperiodic(exps: frozenset[int], n: int) -> bool:
    for d in range(1, n):
        if n % d == 0 and frozenset((i + d) % n for i in exps) == exps:
            return False
    return True


def lemma_topseam_is_shift_pair() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "topseam_support_pair_is_depth_w_shift_pair",
        "statement": (
            "Let S ≠ S' ∈ Fib_w(z) form a top-seam edge: C_can(S)=C_can(S')=C and "
            "lex sides U,V ∈ U(C,z) with Λ_U − Λ_V = c ∈ F_p^×. Then "
            "Λ_S − Λ_{S'} = c Λ_C, so deg(Λ_S − Λ_{S'}) = |C| = j − (w+1) = j − w − 1, "
            "and Phi_w(S)=Phi_w(S')=z. Hence (Λ_S, Λ_{S'}) is a depth-w shift pair "
            "of monic degree-j locators at the maximal allowed difference degree "
            "j−w−1. Equivalently the side pair (U,V) is a constant-shift split pair "
            "of degree e=w+1 (top nonzero SP stratum in the second-moment ledger)."
        ),
        "proof": [
            "Λ_S = Λ_C Λ_U, Λ_{S'} = Λ_C Λ_V (disjoint union core/side).",
            "Core pencil (v2): Λ_U − Λ_V = c ≠ 0 constant.",
            "Difference: Λ_S − Λ_{S'} = Λ_C (Λ_U − Λ_V) = c Λ_C, degree |C| = j−e = j−w−1.",
            "Depth-w shift pair definition (grande_finale prop second-moment / SP notes): "
            "deg(A−B) ≤ deg−w−1 with deg=j gives threshold j−w−1; equality holds.",
            "Side view: e=w+1 and deg(Λ_U−Λ_V)=0 is exactly the constant-shift top stratum.",
        ],
        "deployed": {"j": J, "w": W, "j_minus_w_minus_1": J - W - 1, "e": E},
    }


def lemma_A_SP() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_ASSIGNMENT_RULE",
        "name": "A_SP_support_level_topseam_assignment",
        "statement": (
            "Assignment rule A_SP (support-level SP/top-seam payment):\n"
            "  For each prefix z and each support S ∈ Fib_w(z), if S is incident "
            "to a top-seam edge in G_z (i.e. participates in a multi-member core "
            "pencil U(C,z) with |U(C,z)|≥2), assign S to the SP cell "
            "(or the BC chart cell that absorbs that seam pencil).\n"
            "Equivalently: delete every support that lies in a multi-member "
            "top-seam core pencil; residual supports lie only in singleton pencils."
        ),
        "proof": [
            "This is a definition of a first-match support assignment rule, not a "
            "theorem about the existing SP census. It is the precise rule that "
            "makes residual matching-free.",
        ],
        "relation_to_existing_SP": (
            "grande_finale/sp_notes prove structure (rigidity, second moment, "
            "quotient pullback) and leave primitive SP census OPEN. They do not "
            "state A_SP. Generated-field payment is explicitly image-cell "
            "(multiplicity unpaid). A_SP is stronger: support assignment."
        ),
    }


def lemma_H_seam_from_A_SP() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "H_seam_from_A_SP",
        "statement": (
            "Let R(z) be the set of supports in Fib_w(z) not assigned by A_SP. "
            "Then R(z) is matching-free in G_z (H_seam). By v15 matching-free mass "
            "law, |R(z)| = N_can_prim(z) and |R(z)| ≤ 1 · N_can_prim(z)."
        ),
        "proof": [
            "If S,S' ∈ R(z) formed a top-seam edge, both would be incident to a "
            "top-seam edge, hence both assigned by A_SP, contradiction.",
            "Apply v15 matching-free mass law.",
        ],
        "corollary_mass": (
            "Under A_SP residual, residual mass atom reduces to bounding "
            "N_can_prim or injecting residual supports/cores into size ≤ t·p or n·p."
        ),
    }


def lemma_H_seam_not_unconditional() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_GAP",
        "name": "H_seam_not_from_existing_SP_census",
        "statement": (
            "H_seam is NOT a consequence of currently proved SP theorems alone. "
            "The SP package does not supply A_SP (support assignment of all "
            "top-seam participants). Therefore residual mass via H_seam remains "
            "conditional on adopting A_SP (or proving an equivalent SP/BC "
            "support-level payment)."
        ),
        "proof": [
            "sp_notes / grande_finale: primitive SP census bound OPEN; proved "
            "parts are pair structure and quotient sieve, not residual support "
            "deletion of all multi-member seam pencils.",
            "v1 residual list names sp_shift_pair as a deleted branch, but without "
            "A_SP that name does not force matching-free residual.",
            "Image-cell payments (as in generated-field) can leave multiple "
            "supports per cell unpaid as raw mass.",
        ],
        "path_to_close_gap": (
            "Prove a theorem: every multi-member top-seam core pencil is first-match "
            "assigned at support level to SP/BC with printed cost, or pay residual "
            "multi-member pencils as an explicit cell with cost ≤ remaining budget."
        ),
    }


def lemma_isolated_marks() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_DEFINITIONS",
        "name": "isolated_residual_mark_schemes",
        "statement": (
            "Assume residual R(z) is matching-free (H_seam / A_SP). Every residual "
            "S is isolated in G_z. Define marks:\n"
            "  μ_E5(S)  = (min_exp(S), a_{w+1}(Λ_S)) ∈ {0,...,n-1} × F_p,\n"
            "             where a_{w+1} is the coefficient of X^{j-w-1} in monic Λ_S "
            "(first free monic coefficient below the fixed depth-w prefix z).\n"
            "  μ_E5U(S) = (min_exp(U(S)), a_{w+1}(Λ_S)), U=lex side.\n"
            "  μ_piv(S) = (i_*(S), λ_*(S)) where, after rank-drop deletion, the "
            "ledger affine row packet (L_i) has a first pivot row i_* < t with "
            "nonvanishing pivot coefficient, and λ_* is the normalized residual "
            "coordinate on that row (generated-field style slope when finite, or "
            "a fixed honest-lift coordinate when infinite/honest).\n"
            "Codomain sizes: |μ_E5|,|μ_E5U| ≤ n·p; |μ_piv| ≤ t·p if i_* ∈ {0..t-1} "
            "and λ_* ∈ F_p."
        ),
        "proof": [
            "Under H_seam, S is well-defined and isolated; lex side U(S) well-defined.",
            "Monic Λ_S has unique coefficient sequence; a_{w+1} is unique.",
            "Rank-drop deletion is in the residual definition; residual admits a "
            "pivot row in the ledger packet shape (kb first-match ledger: pivot "
            "failures removed before generated-field). The concrete λ_* formula "
            "must match the packet rows used for that residual class.",
            "Cardinality of codomains is immediate.",
        ],
        "injectivity": "OPEN (toy bank: μ_E5 and μ_E5U fail on aperiodic seam-free proxy)",
        "bridge": (
            "If any mark is injective on ledger residual for every z, then "
            "|R| ≤ n·p or t·p and residual mass closes (v14/v15)."
        ),
    }


def lemma_bridge_close() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "A_SP_plus_injective_mark_closes_mass",
        "statement": (
            "If residual is defined using A_SP (hence H_seam) and some mark "
            "μ: R(z) → L is injective with |L| ≤ t·p (resp. n·p) for every z, "
            "then max |R(z)| ≤ t·p (resp. n·p) ≤ TARGET, closing residual mass."
        ),
        "proof": [
            "A_SP ⇒ H_seam ⇒ matching-free mass law (v15/v16).",
            "Injection ⇒ |R| ≤ |L|.",
            "v14: t·p and n·p fit under TARGET.",
        ],
        "numbers": {"t_p": T_P, "n_p": N_P, "TARGET": TARGET},
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_A_SP_AND_MARK_INJECTIVITY",
        "statement": (
            "(1) Prove A_SP (or equivalent support-level SP/BC payment of all "
            "multi-member top-seam pencils) as a first-match theorem with cost.\n"
            "(2) Prove injectivity of μ_E5, μ_E5U, or μ_piv (or another mark) on "
            "ledger residual.\n"
            "Either (2) alone with H_seam, or both, closes residual mass."
        ),
        "falsifier": (
            "A residual fiber containing a top-seam edge after claimed A_SP "
            "payment; or two residual supports with the same mark under a claimed "
            "injection."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    # (1) Top-seam => shift pair identity on all seam edges
    for p, n, j, w in [(17, 16, 8, 2), (17, 16, 9, 2), (17, 16, 7, 2), (17, 16, 6, 2)]:
        e = w + 1
        if math.comb(n, j) > 12000:
            continue
        vals = domain_vals(p, n)
        fib: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        def split(S: frozenset[int]) -> tuple[Any, ...]:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = S - U
            polyU = monic_rev([vals[i] for i in sorted(U)], p)
            return C, phi_w(polyU, w), polyU[-1], U

        seam = 0
        shift_ok = 0
        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                C, high, c0, U = split(S)
                pencils[(tuple(sorted(C)), high)].append(S)
            for _key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                for i in range(len(lst)):
                    for j2 in range(i + 1, len(lst)):
                        S, T = lst[i], lst[j2]
                        seam += 1
                        pa = monic_rev([vals[i] for i in sorted(S)], p)
                        pb = monic_rev([vals[i] for i in sorted(T)], p)
                        ensure(phi_w(pa, w) == phi_w(pb, w), "same z")
                        dd = deg_diff_monic(pa, pb, j, p)
                        ensure(dd == j - w - 1, f"deg {dd} != {j-w-1}")
                        ensure(dd <= j - w - 1, "shift pair")
                        shift_ok += 1
        rows.append(
            {
                "check": "topseam_shift",
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "seam_pairs": seam,
                "shift_ok": shift_ok,
            }
        )
        ensure(seam == shift_ok, "all seam are shift pairs")

    # (2) A_SP residual = strong matching-free; marks
    mark_rows = []
    for p, n, j, w in [
        (17, 16, 9, 2),
        (17, 16, 7, 2),
        (17, 16, 10, 3),
        (17, 16, 6, 2),
        (17, 16, 5, 2),
        (17, 16, 9, 3),
    ]:
        e = w + 1
        if math.comb(n, j) > 12000:
            continue
        vals = domain_vals(p, n)
        fib = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append((S, poly))

        def split(S: frozenset[int]) -> tuple[Any, ...]:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = S - U
            polyU = monic_rev([vals[i] for i in sorted(U)], p)
            return C, phi_w(polyU, w), polyU[-1], U

        worst = {"mu_E5": 1, "mu_E5U": 1, "minS_cU": 1}
        max_R = 0
        for _z, members in fib.items():
            pencils = defaultdict(list)
            for S, poly in members:
                C, high, c0, U = split(S)
                pencils[(tuple(sorted(C)), high)].append(S)
            # A_SP residual proxy: not in multi-member pencil (+ aperiodic optional)
            R = []
            for S, poly in members:
                C, high, c0, U = split(S)
                if len(pencils[(tuple(sorted(C)), high)]) >= 2:
                    continue  # assigned by A_SP
                if not aperiodic(S, n):
                    continue  # optional extra residual proxy
                R.append((S, poly, c0, U))
            if not R:
                continue
            max_R = max(max_R, len(R))
            cores = {tuple(sorted(split(S)[0])) for S, _, _, _ in R}
            ensure(len(R) == len(cores), "A_SP => |R|=Ncan")
            inv = {k: defaultdict(int) for k in worst}
            for S, poly, c0, U in R:
                aw1 = poly[w + 1] if len(poly) > w + 1 else 0
                inv["mu_E5"][(min(S), aw1)] += 1
                inv["mu_E5U"][(min(U), aw1)] += 1
                inv["minS_cU"][(min(S), c0)] += 1
            for k in worst:
                worst[k] = max(worst[k], max(inv[k].values()))
        mark_rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "max_R_A_SP_ap": max_R,
                "worst_marks": worst,
                "n_p": n * p,
            }
        )

    ensure(any(r["worst_marks"]["mu_E5"] > 1 for r in mark_rows), "E5 mark fails toy")
    ensure(T_P < TARGET and N_P < TARGET, "budgets")
    return {
        "status": "PASS",
        "topseam_shift_rows": rows,
        "mark_rows": mark_rows,
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v16",
        "title": "H_seam via A_SP support assignment; isolated residual marks",
        "status": "PARTIAL_HSEAM_MARK",
        "claims": {
            "proves_topseam_is_shift_pair": True,
            "defines_A_SP": True,
            "proves_H_seam_from_A_SP": True,
            "proves_A_SP_from_existing_SP": False,
            "defines_isolated_marks": True,
            "proves_mark_injectivity": False,
            "proves_residual_mass_atom": False,
            "banks_mark_failures_on_proxy": True,
        },
        "deployed": {
            "a_plus": A,
            "n": N,
            "j": J,
            "t": T,
            "w": W,
            "e": E,
            "TARGET": TARGET,
            "t_p": T_P,
            "n_p": N_P,
            "j_minus_w_minus_1": J - W - 1,
        },
        "lemmas": {
            "topseam_shift_pair": lemma_topseam_is_shift_pair(),
            "A_SP": lemma_A_SP(),
            "H_seam_from_A_SP": lemma_H_seam_from_A_SP(),
            "H_seam_gap": lemma_H_seam_not_unconditional(),
            "isolated_marks": lemma_isolated_marks(),
            "bridge": lemma_bridge_close(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "reduction": "A_SP => H_seam => |R|=N_can; injective mark => mass atom",
            "gap": "A_SP not implied by existing SP census; marks not injective on toys",
            "next": (
                "Prove support-level SP/BC payment (A_SP) with cost, or different "
                "mark with injectivity proof for ledger residual"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    ts = cert["toy_suite"]["topseam_shift_rows"]
    mr = cert["toy_suite"]["mark_rows"]
    t1 = "\n".join(
        f"| {r['j']} | {r['w']} | {r['seam_pairs']} | {r['shift_ok']} |" for r in ts
    )
    t2 = "\n".join(
        f"| {r['j']} | {r['w']} | {r['max_R_A_SP_ap']} | {r['worst_marks']['mu_E5']} | "
        f"{r['worst_marks']['mu_E5U']} | {r['worst_marks']['minS_cU']} |"
        for r in mr
    )
    return f"""# KB-MCA Route-D v16: H_seam from A_SP + isolated residual marks

Status: `PARTIAL` — top-seam/SP identification + A_SP⇒H_seam **PROVED**;
unconditional H_seam and mark injectivity **OPEN**.

## 1. Top-seam pairs are depth-w shift pairs (PROVED)

If `S,S'` form a top-seam edge (same can-core, free-1 CS sides):

```text
Λ_S − Λ_{{S'}} = c Λ_C
deg(Λ_S − Λ_{{S'}}) = j − w − 1   (maximal depth-w shift stratum)
```

Deployed: `j−w−1 = {d['j_minus_w_minus_1']}`.

Toy: all seam pairs satisfy the identity.

| j | w | #seam | #shift-ok |
|---|---|---:|---:|
{t1}

## 2. Assignment rule A_SP (definition)

Assign every support incident to a top-seam edge in `G_z` to the SP/BC cell
(equivalently: delete multi-member core pencils from residual).

## 3. H_seam from A_SP (PROVED)

```text
A_SP residual  ⇒  matching-free  ⇒  |R| = N_can_prim  (pack=1)
```

## 4. Gap (PROVED as gap)

Existing SP theorems (structure + quotient sieve; **census OPEN**) do **not**
imply A_SP. Image-cell payments need not assign all supports. Unconditional
H_seam is **not** available from current SP package alone.

## 5. Isolated residual marks (definitions)

Under H_seam every residual leaf is isolated. Candidate marks:

```text
μ_E5(S)  = (min_exp(S), a_{{w+1}}(Λ_S))     ∈  [n] × F_p     (size n·p)
μ_E5U(S) = (min_exp(U), a_{{w+1}}(Λ_S))     ∈  [n] × F_p
μ_piv(S) = (i_*(S), λ_*(S))                 ∈  [t] × F_p     (size t·p)
```

`a_{{w+1}}` = first free monic coefficient below fixed prefix `z`.
`i_*` = first pivot row among ≤t ledger affine rows after rank-drop deletion.

**Injectivity OPEN.** If injective, residual mass closes (v14/v15).

## 6. Toy bank (A_SP + aperiodic proxy)

| j | w | max |R| | max μ_E5 fiber | max μ_E5U | max (minS,cU) |
|---|---|---:|---:|---:|---:|
{t2}

Marks collide ⇒ not proofs of E2/E5.

## Bridge

```text
A_SP + injective mark  ⇒  |R| ≤ t·p or n·p  ⇒  residual mass atom
```

## OPEN

1. Prove **A_SP** (support-level SP/BC payment with cost), or equivalent.
2. Prove **injectivity** of a residual mark (μ_E5 / μ_piv / better).

## Non-claims

Not unconditional H_seam. Not mark injectivity. Not `U(1116048)≤B*`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v16.py
python3 experimental/scripts/verify_kb_qatom_route_d_v16.py --check
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
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v16\n\n"
        "H_seam via A_SP; isolated residual mark schemes.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v16.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v16 report\n\nstatus: {cert['status']}\n"
        f"topseam_is_shift_pair: PROVED\n"
        f"H_seam_from_A_SP: PROVED\n"
        f"A_SP_from_existing_SP: FALSE/OPEN\n"
        f"mark_injectivity: OPEN\n"
        f"toy seam rows: {len(cert['toy_suite']['topseam_shift_rows'])}\n"
        f"toy mark rows: {len(cert['toy_suite']['mark_rows'])}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  top-seam => depth-w shift pair: PROVED")
    print("  A_SP => H_seam => |R|=N_can: PROVED")
    print("  A_SP from existing SP census: NOT PROVED (gap)")
    print("  isolated marks μ_E5 / μ_piv: DEFINED; injectivity OPEN")
    print(f"  toy: all seam pairs are shift pairs; μ_E5 collides on proxy")


if __name__ == "__main__":
    main()
