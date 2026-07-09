#!/usr/bin/env python3
"""KB-MCA Route-D v17: A_SP printed cost algebra + residual split; mark search bank.

Attacks the two real next theorems from v16:
  (1) Support-level A_SP payment with printed cost
  (2) Injective residual mark (beyond naive (min,a_{w+1}))

Proved:
  (1) Fiber partition: Fib_w(z) = A_SP(z) ⊔ R_sing(z), where A_SP = supports in
      multi-member top-seam core pencils, R_sing = singleton pencils (A_SP residual).
  (2) Cost identities for A_SP mass:
        |A_SP(z)| = sum_{pencils: k≥2} k
        P_multi(z) = # multi-member pencils
        |A_SP(z)| ≤ pack_ceil · P_multi(z)   (each k ≤ pack_ceil)
        |A_SP(z)| ≤ N_ord(z) where N_ord = sum_{k≥2} k(k-1)  (ordered seam pairs),
        because k ≤ k(k-1) for every integer k≥2.
  (3) First-match split: if A_SP is paid as a cell with |E|≤U_A_SP and residual
      is R_sing, then residual mass bound reduces to bounding R_sing (H_seam holds
      on R_sing by construction of A_SP).
  (4) Printed-cost criterion (conditional): if max_z P_multi(z) ≤ floor(B/pack_ceil)
      then |A_SP|≤B; taking B=t·p gives A_SP ≤ t·p. OPEN: bound P_multi.
  (5) R_sing bijection: S ↔ C_can(S) on R_sing (v15/v16); mark problem = inject
      residual cores or supports into size ≤ t·p or n·p.
  (6) Mark search bank (negative): on A_SP residual (singleton pencils), none of
      the tested n·p-scale marks is injective on all toys:
        (min S, a_{w+1}), (min U, a_{w+1}), (min C, a_{w+1}/b1/c0/sum/prod),
        (sum S, a_{w+1}), (prod U, a_{w+1}), (min S, sum S), ...
      (min S, a_{w+1}, a_{w+2}) works on some toys (n·p² scale, not E2/E5 budget).
      No proved injective E2/E5 mark found.

Does NOT prove A_SP cost ≤ t·p, nor mark injectivity, nor U(1116048)≤B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v17.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v17.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v17"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v17.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v17.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v17.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
PACK = 17
TARGET = 274_836_936_291_722_953
T_P = T * P
N_P = N * P


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


def lemma_partition() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "fiber_partition_A_SP_and_singleton",
        "statement": (
            "For each z, partition Fib_w(z) by top-seam core pencils U(C,z):\n"
            "  A_SP(z)  = union of multi-member pencils (|U(C,z)|≥2)\n"
            "  R_sing(z)= union of singleton pencils (|U(C,z)|=1)\n"
            "These are disjoint and cover Fib_w(z). R_sing is matching-free "
            "(H_seam) by construction. A_SP is exactly the support set assigned "
            "by rule A_SP (v16)."
        ),
        "proof": [
            "Every support has a unique lex can-core and lies in U(C,z) for that core.",
            "Pencils partition the fiber. Multi vs singleton is a partition of pencils.",
            "Singleton pencils have no internal top-seam edge.",
        ],
    }


def lemma_cost_identities() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "A_SP_printed_cost_identities",
        "statement": (
            "Let pencils of sizes k_1,...,k_r include multi-member ones with sizes "
            "k≥2. Write\n"
            "  |A_SP(z)| = sum_{k≥2} k\n"
            "  P_multi(z) = |{pencils : k≥2}|\n"
            "  N_ord(z) = sum_{k≥2} k(k-1)   (ordered top-seam pairs in G_z).\n"
            "Then:\n"
            "  (i)  |A_SP(z)| ≤ pack_ceil · P_multi(z)\n"
            "       (deployed pack_ceil=17, since k ≤ floor((n-|C|)/e) ≤ 17);\n"
            "  (ii) |A_SP(z)| ≤ N_ord(z)\n"
            "       because for every integer k≥2 one has k ≤ k(k-1)."
        ),
        "proof": [
            "(i) Each multi-member pencil has size k ≤ pack_ceil by core-pencil "
            "packing (v2). Sum of k over P_multi pencils ≤ pack_ceil · P_multi.",
            "(ii) k≤k(k-1) for k≥2: for k=2 equality; for k≥3, k-1≥2 so k(k-1)≥2k>k.",
            "Summing over multi-member pencils yields |A_SP| ≤ N_ord.",
        ],
        "deployed_pack_ceil": PACK,
        "printed_cost_forms": {
            "exact_support": "|A_SP|",
            "pack_P_multi": f"{PACK} * P_multi",
            "ordered_pairs": "N_ord",
        },
    }


def lemma_first_match_split() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "first_match_A_SP_cell_then_residual_sing",
        "statement": (
            "In a first-match ledger, pay cell C_A_SP with E ⊇ A_SP(z) for every z "
            "and bound |E|≤U_A_SP. The residual family after this cell may be taken "
            "as R ⊆ R_sing (supports not in A_SP). Then H_seam holds on R, "
            "|R|=N_can_prim(R), and\n"
            "  max |Fib residual| ≤ U_A_SP + max |R_sing|.\n"
            "If U_A_SP ≤ t·p and max |R_sing| ≤ t·p (or n·p), residual-scale mass "
            "fits E2/E5 budgets (whether or not the full Q residual equals R_sing)."
        ),
        "proof": [
            "First-match upper ledger (grande_finale): sum of cell bounds upper-bounds "
            "union. Partition Fib = A_SP ⊔ R_sing.",
            "R_sing matching-free ⇒ mass law |R_sing|=N_can (v15).",
            "v14: t·p and n·p fit under TARGET.",
        ],
        "note": (
            "This packages A_SP as a payable first-match cell with an explicit "
            "support set. The missing inputs are (a) U_A_SP ≤ printed budget and "
            "(b) injective mark / mass bound on R_sing."
        ),
    }


def lemma_P_multi_criterion() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "P_multi_bound_gives_A_SP_cost",
        "statement": (
            f"If max_z P_multi(z) ≤ floor(B / {PACK}), then max |A_SP(z)| ≤ B "
            f"by cost identity (i). In particular B = t·p gives the criterion "
            f"P_multi ≤ floor(t·p / 17) = {T_P // PACK}."
        ),
        "proof": ["Immediate from |A_SP| ≤ pack_ceil · P_multi."],
        "open": "Bound max_z P_multi(z) (number of multi-member top-seam pencils).",
        "numbers": {
            "t_p_over_pack": T_P // PACK,
            "log2_t_p_over_pack": math.log2(max(T_P // PACK, 1)),
        },
    }


def lemma_R_sing_mark_problem() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "R_sing_mark_equals_core_injection",
        "statement": (
            "On R_sing(z), C_can: R_sing → C_res is bijective. Therefore an "
            "injective mark on residual supports exists with codomain L iff "
            "residual can-cores inject into L. E2/E5 marks may be defined on "
            "supports or cores interchangeably for R_sing."
        ),
        "proof": [
            "Singleton pencil ⇒ unique support per core in the fiber (v15/v16).",
            "Cardinality bijection.",
        ],
    }


def lemma_mark_search_bank() -> dict[str, Any]:
    return {
        "status": "PROVED_NEGATIVE_TOY_BANK",
        "name": "no_tested_E2_E5_mark_injective",
        "statement": (
            "On A_SP residual R_sing (singleton top-seam pencils) for small dyadic "
            "rows, none of the following n·p-scale marks is injective on all tested "
            "rows: (min S, a_{w+1}), (min U, a_{w+1}), (min C, b1/c0/sum/prod), "
            "(sum S, a_{w+1}), (prod U, a_{w+1}), (min S, sum S). "
            "The n·p² mark (min S, a_{w+1}, a_{w+2}) is injective on some but not "
            "all toys, and n·p² is not an E2/E5 budget. Conclusion: plain local "
            "marks are unlikely to prove E2/E5; need ledger-specific pivots or a "
            "different label geometry."
        ),
        "proof": ["Computational certificates in toy_suite mark_rows."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_A_SP_COST_AND_R_SING_MARK",
        "statement": (
            "(1) Bound max P_multi or max |A_SP| by a printed constant (ideally "
            "≤ t·p), using SP/BC geometry — establishes A_SP as a paid cell.\n"
            "(2) Prove an injective mark on R_sing into size ≤ t·p or n·p "
            "(ledger pivot / RIM / selector), not a failed local (min,·) form."
        ),
        "falsifier": (
            "A fiber with |A_SP| larger than the claimed U_A_SP; or two R_sing "
            "supports with the same claimed mark."
        ),
    }


def toy_suite() -> dict[str, Any]:
    cost_rows = []
    mark_rows = []
    for p, n, j, w in [
        (17, 16, 8, 2),
        (17, 16, 9, 2),
        (17, 16, 7, 2),
        (17, 16, 6, 2),
        (17, 16, 10, 3),
        (17, 16, 5, 2),
        (17, 16, 9, 3),
    ]:
        e = w + 1
        pack_toy = n // e  # loose; real pack depends on core size
        if math.comb(n, j) > 20000:
            continue
        vals = domain_vals(p, n)
        fib: dict[Any, list] = defaultdict(list)
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

        total = multi_S = multi_P = n_ord = 0
        max_A = max_R = max_P = 0
        worst: dict[str, int] = defaultdict(lambda: 1)
        names = [
            "minS_aw1",
            "minU_aw1",
            "minC_b1",
            "minC_c0",
            "minC_sum",
            "sumS_aw1",
            "prodU_aw1",
            "minS_sum",
            "minS_aw1_aw2",
        ]
        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S, poly in members:
                C, high, c0, U = split(S)
                pencils[(tuple(sorted(C)), high)].append((S, poly, c0, U, C))
            A_list = []
            R_list = []
            n_ord_z = 0
            P_z = 0
            for _key, lst in pencils.items():
                k = len(lst)
                total += k
                if k >= 2:
                    multi_S += k
                    multi_P += 1
                    P_z += 1
                    n_ord_z += k * (k - 1)
                    n_ord += k * (k - 1)
                    A_list.extend(lst)
                    ensure(k <= k * (k - 1), "k<=k(k-1)")
                else:
                    R_list.extend(lst)
            max_A = max(max_A, len(A_list))
            max_R = max(max_R, len(R_list))
            max_P = max(max_P, P_z)
            # cost identities on this fiber
            if P_z:
                ensure(len(A_list) <= pack_toy * P_z or len(A_list) <= 17 * P_z, "pack")
                ensure(len(A_list) <= n_ord_z, "A<=N_ord")
            # marks on R_sing
            inv = {nm: defaultdict(int) for nm in names}
            for S, poly, c0, U, C in R_list:
                pts = [vals[i] for i in sorted(S)]
                ptsU = [vals[i] for i in sorted(U)]
                ptsC = [vals[i] for i in sorted(C)]
                polyC = monic_rev(ptsC, p)
                aw1 = poly[w + 1] if len(poly) > w + 1 else 0
                aw2 = poly[w + 2] if len(poly) > w + 2 else 0
                sS = sum(pts) % p
                prU = 1
                for x in ptsU:
                    prU = (prU * x) % p
                inv["minS_aw1"][(min(S), aw1)] += 1
                inv["minU_aw1"][(min(U), aw1)] += 1
                inv["minC_b1"][(min(C), polyC[1] if len(polyC) > 1 else 0)] += 1
                inv["minC_c0"][(min(C), polyC[-1])] += 1
                inv["minC_sum"][(min(C), sum(ptsC) % p)] += 1
                inv["sumS_aw1"][(sS, aw1)] += 1
                inv["prodU_aw1"][(prU, aw1)] += 1
                inv["minS_sum"][(min(S), sS)] += 1
                inv["minS_aw1_aw2"][(min(S), aw1, aw2)] += 1
            for nm in names:
                if inv[nm]:
                    worst[nm] = max(worst[nm], max(inv[nm].values()))

        # global cost identities
        ensure(multi_S <= n_ord or multi_S == 0, "global A<=N_ord")
        cost_rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "total_S": total,
                "multi_S": multi_S,
                "multi_P": multi_P,
                "n_ord": n_ord,
                "frac_multi": multi_S / total if total else 0,
                "max_A_SP_fiber": max_A,
                "max_R_sing_fiber": max_R,
                "max_P_multi_fiber": max_P,
                "A_le_N_ord": multi_S <= n_ord,
            }
        )
        mark_rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "worst": dict(worst),
                "any_np_injective": any(
                    worst[nm] == 1 for nm in names if nm != "minS_aw1_aw2"
                ),
                "aw1_aw2_injective": worst["minS_aw1_aw2"] == 1,
            }
        )

    ensure(all(r["A_le_N_ord"] for r in cost_rows), "cost id")
    ensure(any(not r["any_np_injective"] for r in mark_rows), "marks fail somewhere")
    ensure(T_P // PACK > 0, "budget")
    return {"status": "PASS", "cost_rows": cost_rows, "mark_rows": mark_rows}


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v17",
        "title": "A_SP printed cost algebra; R_sing mark search bank",
        "status": "PARTIAL_A_SP_COST",
        "claims": {
            "proves_fiber_partition": True,
            "proves_A_SP_cost_identities": True,
            "proves_first_match_split_form": True,
            "proves_P_multi_criterion": True,
            "proves_R_sing_core_bijection": True,
            "proves_A_SP_cost_le_tp": False,
            "proves_mark_injectivity": False,
            "banks_mark_search_failures": True,
        },
        "deployed": {
            "n": N,
            "j": J,
            "t": T,
            "w": W,
            "pack_ceil": PACK,
            "TARGET": TARGET,
            "t_p": T_P,
            "n_p": N_P,
            "P_multi_budget_for_A_SP_le_tp": T_P // PACK,
            "log2_P_multi_budget": math.log2(max(T_P // PACK, 1)),
        },
        "lemmas": {
            "partition": lemma_partition(),
            "cost_identities": lemma_cost_identities(),
            "first_match_split": lemma_first_match_split(),
            "P_multi_criterion": lemma_P_multi_criterion(),
            "R_sing_mark": lemma_R_sing_mark_problem(),
            "mark_bank": lemma_mark_search_bank(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "A_SP_path": "Pay |A_SP|≤17*P_multi or ≤N_ord; need P_multi or N_ord bound",
            "mark_path": "No tested E2/E5 mark works on toys; need ledger pivot geometry",
            "next": "Bound P_multi(z) or design injective R_sing mark from rank/RIM",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cr = cert["toy_suite"]["cost_rows"]
    mr = cert["toy_suite"]["mark_rows"]
    t1 = "\n".join(
        f"| {r['j']} | {r['w']} | {r['multi_S']} | {r['multi_P']} | {r['n_ord']} | "
        f"{r['frac_multi']:.4f} | {r['max_A_SP_fiber']} | {r['max_R_sing_fiber']} |"
        for r in cr
    )
    t2 = "\n".join(
        f"| {r['j']} | {r['w']} | {r['any_np_injective']} | {r['aw1_aw2_injective']} | "
        f"{max(r['worst'].values())} |"
        for r in mr
    )
    return f"""# KB-MCA Route-D v17: A_SP cost algebra + mark search

Status: `PARTIAL` — A_SP **cost identities** PROVED; **P_multi bound** and
**mark injectivity** OPEN. Local E2/E5 marks **fail** on toys.

## Fiber partition (PROVED)

```text
Fib_w(z) = A_SP(z)  ⊔  R_sing(z)
```

- `A_SP` = multi-member top-seam core pencils (A_SP assignment set)
- `R_sing` = singleton pencils = matching-free residual after A_SP

## A_SP printed cost (PROVED)

```text
|A_SP| = sum_{{k≥2}} k
|A_SP| ≤ pack_ceil · P_multi     (deployed pack_ceil = {d['pack_ceil']})
|A_SP| ≤ N_ord = sum_{{k≥2}} k(k-1)   (ordered seam pairs)
```

**Conditional payment:** if `P_multi ≤ t·p/17 = {d['P_multi_budget_for_A_SP_le_tp']}`
(~2^{{{d['log2_P_multi_budget']:.2f}}}), then `|A_SP| ≤ t·p`.

**OPEN:** bound `max P_multi` (or `max |A_SP|` / `max N_ord`).

## First-match form (PROVED)

```text
pay A_SP cell (bound U_A_SP)
residual ⊆ R_sing
max residual mass ≤ U_A_SP + max |R_sing|
```

## R_sing marks (PROVED reduction + negative bank)

On `R_sing`, `S ↔ C_can` bijective — mark supports or cores equivalently.

**Toy search:** no tested **n·p-scale** mark is injective on all rows.
`(min, a_{{w+1}}, a_{{w+2}})` (n·p²) works sometimes, not always, and is too large for E2/E5.

### A_SP mass toys

| j | w | multi_S | P_multi | N_ord | frac multi | max |A_SP| | max |R_sing| |
|---|---|---:|---:|---:|---:|---:|---:|
{t1}

### Mark injectivity toys (R_sing)

| j | w | any n·p mark inj? | aw1_aw2 inj? | worst max fiber |
|---|---|---|---|---:|
{t2}

## Bridge to atom

```text
U_A_SP ≤ t·p  and  |R_sing| ≤ t·p (or n·p)
    ⇒  full fiber mass controlled at E2 scale after A_SP payment
```

## OPEN (real next theorems, refined)

1. **Bound P_multi or |A_SP|** with printed cost (establish A_SP as paid cell).
2. **Injective R_sing mark** into t·p or n·p via ledger structure (pivot/RIM/selector) —
   not another local (min, ·) experiment without new geometry.

## Non-claims

Not A_SP ≤ t·p. Not mark injectivity. Not `U(1116048)≤B*`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v17.py
python3 experimental/scripts/verify_kb_qatom_route_d_v17.py --check
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
        "# kb-qatom-route-d-v17\n\n"
        "A_SP printed cost algebra; R_sing mark search bank.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v17.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v17 report\n\nstatus: {cert['status']}\n"
        f"A_SP cost identities: PROVED\n"
        f"P_multi bound: OPEN\n"
        f"mark injectivity: OPEN (banked failures)\n"
        f"P_multi budget for A_SP<=t*p: {cert['deployed']['P_multi_budget_for_A_SP_le_tp']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  A_SP cost: |A_SP| <= 17*P_multi and |A_SP| <= N_ord PROVED")
    print(f"  criterion: P_multi <= t*p/17 = {T_P // PACK} => A_SP <= t*p")
    print("  mark search: no n*p-scale injective mark on all toys")
    print(f"  cost rows: {len(cert['toy_suite']['cost_rows'])}")


if __name__ == "__main__":
    main()
