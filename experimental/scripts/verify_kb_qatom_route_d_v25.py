#!/usr/bin/env python3
"""KB-MCA Route-D v25: free-1 high families are disjoint; residual side census.

Attacks residual FS_1(e) ↪ [e] for the structure-aware e·p mark (v24).

Proved:
  (1) Free-1 high family packing: for fixed free-1 high H (middle monic
      coeffs of degree-e locators), the fully D-split free-1 e-sets F_H are
      pairwise disjoint. Proof: if r ∈ U ∈ F_H then c0(U) = −H(r) is forced,
      so r determines at most one member of F_H.
  (2) Consequence: |F_H| ≤ ⌊n/e⌋ for every high H.
  (3) Deployed arithmetic: ⌊n/e⌋ = ⌊2^21 / 67472⌋ = 31 ≤ e = 67472.
      Hence every free-1 high family injects into [e] (e.g. by sorting c0).
  (4) Within-family CS-pair marks: free-1 CS pairs share a high (by def);
      (c0U, δ) with δ=c0U−c0V injects pairs inside each F_H; combining with
      a family index ι: F_H → [|F_H|] ⊆ [e] gives (ι(U), δ) injective
      *within* each high family.
  (5) Payment reduction (refined): residual free-1 CS pairs inject into e·p
      if either (a) residual pairs use a single high, or (b) highs among
      residual sides are separated by an additional injective tag into a set
      of size 1 (i.e. one residual high class), or more generally if residual
      highs inject into a set of size 1 when paired with (ι,δ) — the remaining
      OPEN is cross-high collision of (ι,δ).
  (6) Toy census: families pairwise disjoint; |F_H| ≤ ⌊n/e⌋ tight-ish;
      fiber-local |U| can exceed e (so naive fiber↪[e] fails); natural
      global e-marks on U collide; within-high (c0U,δ) injective; deployed
      ⌊n/e⌋≤e holds.

Does NOT prove global residual FS_1(e)↪[e] (cross-high), nor M_pad≤1.

  python3 experimental/scripts/verify_kb_qatom_route_d_v25.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v25.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v25"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v25.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v25.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v25.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
M_C = J - E
FREE_CORE = M_C - W
T_P = T * P
E_P = E * P
FLOOR_N_OVER_E = N // E  # 31 deployed


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


def free1_high_c0(U: frozenset[int], vals: list[int], p: int) -> tuple[tuple[int, ...], int]:
    poly = monic_rev([vals[i] for i in sorted(U)], p)
    # free-1 high = all middle coeffs poly[1:-1]
    return tuple(poly[1:-1]), poly[-1]


def lemma_family_disjoint() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_high_families_pairwise_disjoint",
        "statement": (
            "Fix a free-1 high H (the e−1 middle coefficients of a monic degree-e "
            "locator). Let F_H be the set of e-subsets U ⊂ D whose monic locator "
            "has free-1 high H and is fully split on D. Then the members of F_H "
            "are pairwise disjoint: U ≠ U' in F_H ⇒ U ∩ U' = ∅."
        ),
        "proof": [
            "Write Λ_U(X) = X^e + H_1 X^{e−1} + ⋯ + H_{e−1} X + c0(U) "
            "(high H fixed across F_H).",
            "If r ∈ U then Λ_U(r) = 0 ⇒ H(r) + c0(U) = 0 ⇒ c0(U) = −H(r), "
            "where H(r) means the evaluation of the high part at r.",
            "Thus any root r determines c0 uniquely for that high, hence "
            "determines Λ_U uniquely, hence determines U uniquely among F_H.",
            "Therefore no r can lie in two distinct members of F_H.",
        ],
    }


def lemma_family_size() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_high_family_size_le_n_over_e",
        "statement": (
            "For every free-1 high H: |F_H| ≤ ⌊n/e⌋. "
            f"Deployed: ⌊n/e⌋ = ⌊{N}/{E}⌋ = {FLOOR_N_OVER_E} ≤ e = {E}."
        ),
        "proof": [
            "Pairwise disjoint e-sets in a domain of size n ⇒ at most ⌊n/e⌋ of them.",
            "Previous lemma.",
        ],
        "deployed_floor_n_over_e": FLOOR_N_OVER_E,
        "deployed_e": E,
        "deployed_floor_le_e": FLOOR_N_OVER_E <= E,
    }


def lemma_within_family_marks() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "within_high_family_pair_marks",
        "statement": (
            "Free-1 CS ordered pairs (U,V) always share a high H. Inside F_H:\n"
            "  • c0: F_H → F_p is injective (monic recovery);\n"
            "  • (c0U, δ) with δ=c0U−c0V injects ordered pairs in F_H × F_H;\n"
            "  • any bijection ι: F_H → {0,...,|F_H|−1} (e.g. sort by c0) "
            "gives (ι(U), δ) injective on ordered pairs inside F_H.\n"
            f"Deployed |F_H| ≤ {FLOOR_N_OVER_E} ≤ e ⇒ ι lands in [e]."
        ),
        "proof": [
            "Free-1 CS ⇔ same free-1 high and distinct constants.",
            "c0 injective: monic (H,c0) determines U among fully split.",
            "Given (c0U,δ): c0V=c0U−δ; Λ_U, Λ_V determined by (H,c0); "
            "recover U,V. So (c0U,δ) injective within F_H.",
            "ι injective ⇒ (ι(U),δ) injective within F_H.",
            "Size: |F_H| ≤ ⌊n/e⌋ ≤ e deployed ⇒ ι(U) ∈ [e].",
        ],
    }


def lemma_payment_reduction() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "payment_reduction_cross_high_gap",
        "statement": (
            "If M_pad≤1 and residual free-1 CS ordered pairs all lie in a "
            "single free-1 high family F_H, then "
            "(U,V) ↦ (ι(U), δ) injects them into [e]×F_p (size e·p=t·p "
            f"deployed), hence |A_SP| ≤ t·p.\n"
            "More generally, if residual highs can be injectively tagged by a "
            "label in a set of size 1 (one residual high), same conclusion.\n"
            "OPEN gap: cross-high collisions of (ι,δ) when many residual highs."
        ),
        "proof": [
            "v24: (U,δ) injects pairs into FS_1(e)×F_p^×.",
            "Within F_H: (ι,δ) injects into [e]×F_p when |F_H|≤e.",
            "Single residual high ⇒ global (ι,δ) works.",
            "Multiple highs: (ι,δ) may collide across highs (toy bank).",
        ],
        "deployed_e_p": E_P,
        "deployed_floor_n_e": FLOOR_N_OVER_E,
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_cross_high_residual_and_Mpad",
        "statement": (
            "(1) Separate residual free-1 highs without blowing the e·p budget "
            "(or prove residual top-seam pairs use one high / O(1) highs).\n"
            f"(2) M_pad≤1 at free_core={FREE_CORE}.\n"
            "Together with within-family (ι,δ) this closes |A_SP|≤t·p."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_fam_checked = 0
    n_fam_disjoint = 0
    n_size_ok = 0
    n_c0_inj = 0
    n_c0_delta_inj = 0
    n_iota_delta_within = 0
    n_iota_delta_global_coll = 0
    n_global_pair_rows = 0

    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 7, 2),
        (17, 16, 7, 3),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (17, 16, 9, 2),
        (17, 16, 9, 3),
        (17, 16, 10, 3),
    ]:
        e = w + 1
        m_c = j - e
        if m_c < 0 or e >= n or math.comb(n, e) > 20000:
            continue
        free_core = m_c - w if m_c >= 0 else None
        vals = domain_vals(p, n)
        floor_ne = n // e

        # --- global free-1 high families on D ---
        fam: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), e):
            U = frozenset(exps)
            high, c0 = free1_high_c0(U, vals, p)
            fam[high].append((U, c0))

        max_fam = 0
        all_disj = True
        all_c0_inj = True
        all_c0_delta = True
        all_iota_within = True
        n_fams = 0
        for high, items in fam.items():
            if len(items) < 1:
                continue
            n_fams += 1
            n_fam_checked += 1
            max_fam = max(max_fam, len(items))
            ensure(len(items) <= floor_ne, f"|F|={len(items)} > n/e={floor_ne}")
            n_size_ok += 1

            # disjointness
            for i in range(len(items)):
                for j2 in range(i + 1, len(items)):
                    if items[i][0] & items[j2][0]:
                        all_disj = False
            if all(
                not (items[i][0] & items[j2][0])
                for i in range(len(items))
                for j2 in range(i + 1, len(items))
            ):
                n_fam_disjoint += 1

            # c0 injective
            c0s = [c for _, c in items]
            if len(c0s) == len(set(c0s)):
                n_c0_inj += 1
            else:
                all_c0_inj = False

            # (c0U, delta) on ordered pairs
            buckets: dict[Any, list] = defaultdict(list)
            for c1, u1 in ((c, u) for u, c in items):
                for c2, u2 in ((c, u) for u, c in items):
                    if c1 == c2:
                        continue
                    delta = (c1 - c2) % p
                    buckets[(c1, delta)].append((tuple(sorted(u1)), tuple(sorted(u2))))
            if all(len(set(v)) <= 1 for v in buckets.values()):
                n_c0_delta_inj += 1
            else:
                all_c0_delta = False

            # ι by sorted c0 → (ι, delta) within family
            order = sorted(items, key=lambda t: t[1])
            iota = {tuple(sorted(u)): i for i, (u, c) in enumerate(order)}
            b2: dict[Any, list] = defaultdict(list)
            for u1, c1 in items:
                for u2, c2 in items:
                    if c1 == c2:
                        continue
                    delta = (c1 - c2) % p
                    b2[(iota[tuple(sorted(u1))], delta)].append(
                        (tuple(sorted(u1)), tuple(sorted(u2)))
                    )
            if all(len(set(v)) <= 1 for v in b2.values()):
                n_iota_delta_within += 1
            else:
                all_iota_within = False

        ensure(all_disj, "disjoint")
        ensure(all_c0_inj, "c0 inj")
        ensure(all_c0_delta, "c0 delta")
        ensure(all_iota_within, "iota delta within")
        ensure(max_fam <= floor_ne, "max fam")

        # --- residual-style top-seam census (j-fibers) if feasible ---
        max_U_fiber = 0
        max_pencil = 0
        max_nord = 0
        n_fib_pairs = 0
        n_fib_U_le_e = 0
        cross_high_iota_delta_coll = 0
        iota_delta_global_inj = None

        if m_c > 0 and math.comb(n, j) <= 20000:
            # precompute ι global by family
            global_iota: dict[tuple, int] = {}
            for high, items in fam.items():
                order = sorted(items, key=lambda t: t[1])
                for i, (u, c) in enumerate(order):
                    global_iota[tuple(sorted(u))] = i

            fib: dict[Any, list] = defaultdict(list)
            for exps in itertools.combinations(range(n), j):
                S = frozenset(exps)
                poly = monic_rev([vals[i] for i in sorted(S)], p)
                fib[phi_w(poly, w)].append(S)

            # global residual pairs across all fibers for cross-high test
            all_pairs_marks: dict[Any, list] = defaultdict(list)

            for _z, members in fib.items():
                pencils: dict[Any, list] = defaultdict(list)
                for S in members:
                    ss = sorted(S)
                    U = frozenset(ss[:e])
                    C = S - U
                    high, c0 = free1_high_c0(U, vals, p)
                    pencils[(tuple(sorted(C)), high)].append((U, c0, high))

                U_fib: set = set()
                pairs_fib = 0
                for key, lst in pencils.items():
                    by_c0 = {c0: U for U, c0, high in lst}
                    k = len(by_c0)
                    max_pencil = max(max_pencil, k)
                    if k < 2:
                        continue
                    pairs_fib += k * (k - 1)
                    for U, c0, high in lst:
                        U_fib.add(tuple(sorted(U)))
                    for i, a in enumerate(lst):
                        for j2, b in enumerate(lst):
                            if i == j2:
                                continue
                            U, c0U, high = a
                            V, c0V, _ = b
                            if c0U == c0V:
                                continue
                            delta = (c0U - c0V) % p
                            fp = (tuple(sorted(U)), tuple(sorted(V)))
                            # within pencil same high
                            mark = (global_iota[tuple(sorted(U))], delta)
                            all_pairs_marks[mark].append(fp)

                if pairs_fib > 0:
                    n_fib_pairs += 1
                    max_U_fiber = max(max_U_fiber, len(U_fib))
                    max_nord = max(max_nord, pairs_fib)
                    if len(U_fib) <= e:
                        n_fib_U_le_e += 1

            # cross-high: does (ι,δ) collide globally on top-seam pairs?
            if all_pairs_marks:
                n_global_pair_rows += 1
                coll = sum(
                    1 for fps in all_pairs_marks.values() if len(set(fps)) >= 2
                )
                cross_high_iota_delta_coll = coll
                nuniq = len({fp for fps in all_pairs_marks.values() for fp in fps})
                iota_delta_global_inj = coll == 0 and len(all_pairs_marks) == nuniq
                if coll > 0:
                    n_iota_delta_global_coll += 1

        # natural e-marks on all e-sets: bank negative if many e-sets
        e_mark_coll = 0
        if math.comb(n, e) <= 20000:
            buckets_e: dict[Any, list] = defaultdict(list)
            for exps in itertools.combinations(range(n), e):
                U = frozenset(exps)
                buckets_e[min(U) % e].append(tuple(sorted(U)))
            e_mark_coll = sum(
                1 for v in buckets_e.values() if len(set(v)) >= 2
            )

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "m_c": m_c,
                "free_core": free_core,
                "floor_n_over_e": floor_ne,
                "n_high_families": n_fams,
                "max_fam_size": max_fam,
                "max_fam_le_floor": max_fam <= floor_ne,
                "max_fam_le_e": max_fam <= e,
                "all_families_disjoint": all_disj,
                "all_c0_injective": all_c0_inj,
                "all_c0_delta_injective": all_c0_delta,
                "all_iota_delta_within": all_iota_within,
                "max_U_per_fiber": max_U_fiber,
                "max_pencil": max_pencil,
                "max_nord": max_nord,
                "n_fibers_with_pairs": n_fib_pairs,
                "n_fibers_U_le_e": n_fib_U_le_e,
                "iota_delta_global_injective": iota_delta_global_inj,
                "cross_high_iota_delta_coll_labels": cross_high_iota_delta_coll,
                "minU_mod_e_coll_labels_on_esets": e_mark_coll,
            }
        )

    ensure(n_fam_checked > 0, "fams")
    ensure(n_fam_disjoint == n_fam_checked, "all disj")
    ensure(n_size_ok == n_fam_checked, "all size")
    ensure(n_c0_inj == n_fam_checked, "all c0")
    ensure(n_c0_delta_inj == n_fam_checked, "all c0d")
    ensure(n_iota_delta_within == n_fam_checked, "all iota")
    # cross-high collisions must appear on some toy row (bank the gap)
    ensure(n_iota_delta_global_coll > 0, "need cross-high collision bank")
    # deployed arithmetic
    ensure(FLOOR_N_OVER_E == N // E, "floor")
    ensure(FLOOR_N_OVER_E == 31, "deployed floor 31")
    ensure(FLOOR_N_OVER_E <= E, "deployed floor le e")
    ensure(T == E, "t=e")
    ensure(FREE_CORE == 846161, "fc")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_families_checked": n_fam_checked,
            "n_families_disjoint": n_fam_disjoint,
            "n_c0_inj": n_c0_inj,
            "n_c0_delta_inj": n_c0_delta_inj,
            "n_iota_delta_within": n_iota_delta_within,
            "n_rows_with_cross_high_coll": n_iota_delta_global_coll,
            "n_global_pair_rows": n_global_pair_rows,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v25",
        "title": "Free-1 high families disjoint; |F_H|≤⌊n/e⌋; residual side census",
        "status": "PARTIAL_SIDE_FAMILY",
        "claims": {
            "proves_free1_families_disjoint": True,
            "proves_family_size_le_n_over_e": True,
            "proves_deployed_family_le_e": True,
            "proves_within_family_iota_delta": True,
            "proves_global_FS1_into_e": False,
            "proves_cross_high_free": False,
            "proves_M_pad_le_1_deployed": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_disjoint_and_cross_high_gap": True,
        },
        "deployed": {
            "n": N,
            "e": E,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "floor_le_e": FLOOR_N_OVER_E <= E,
            "j": J,
            "w": W,
            "m_c": M_C,
            "free_core": FREE_CORE,
            "t": T,
            "t_equals_e": T == E,
            "t_p": T_P,
            "e_p": E_P,
        },
        "lemmas": {
            "disjoint": lemma_family_disjoint(),
            "size": lemma_family_size(),
            "within_marks": lemma_within_family_marks(),
            "payment": lemma_payment_reduction(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "win": (
                f"Within each free-1 high family, sides inject into "
                f"[⌊n/e⌋]=[{FLOOR_N_OVER_E}] ⊆ [e]; pairs via (ι,δ)"
            ),
            "gap": "Cross-high (ι,δ) collisions; need residual high separation or M_pad+single-high",
            "next": (
                "Prove residual top-seam pairs involve one high (or O(1) highs "
                "with budget), or tag highs inside e·p; continue M_pad"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['e']} | {r['j']} | {r['w']} | {r['floor_n_over_e']} | {r['max_fam_size']} | "
        f"{r['max_fam_le_e']} | {r['max_U_per_fiber']} | {r['max_pencil']} | "
        f"{r['iota_delta_global_injective']} | {r['cross_high_iota_delta_coll_labels']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v25: free-1 high families are disjoint

Status: `PARTIAL` — family packing **PROVED** (`|F_H|≤⌊n/e⌋`, deployed ≤e);
within-family `(ι,δ)` **PROVED**; **cross-high** residual tag still **OPEN**.

## Main theorem (PROVED)

For fixed free-1 high `H`, the fully `D`-split free-1 e-sets `F_H` are
**pairwise disjoint**:

```text
r ∈ U ∈ F_H  ⇒  c0(U) = −H(r)  ⇒  U unique in F_H
```

### Size bound

```text
|F_H|  ≤  ⌊n/e⌋
```

### Deployed

```text
n          = {d['n']}
e          = {d['e']}
⌊n/e⌋      = {d['floor_n_over_e']}
⌊n/e⌋ ≤ e  = {d['floor_le_e']}
e·p = t·p  = {d['e_p']}
```

So every free-1 high family injects into `[e]` (e.g. rank by `c0`).

## Within-family pair marks (PROVED)

Free-1 CS pairs share a high. Inside `F_H`:

```text
(U,V)  ↦  (ι(U), δ),   δ = c0U − c0V,   ι = rank by c0 in F_H
```

is injective, and deployed `ι(U) ∈ [e]`.

## Payment reduction (PROVED conditional)

```text
M_pad ≤ 1  and  residual pairs lie in a single high family
    ⇒  (ι,δ) injects into e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

**OPEN gap:** `(ι,δ)` collides across different highs (toys confirm).

## Residual census (toys)

| e | j | w | floor n/e | max |F_H| | max|F|<=e? | max |U|/fiber | max pencil | (ι,δ) global inj? | cross-high coll |
|---|---|---|---:|---:|---|---:|---:|---|---:|
{tbl}

- All families disjoint; `|F_H|≤⌊n/e⌋`; within-family marks injective.
- Fiber-local `|U|` can exceed `e` (naive fiber↪[e] fails on small-w toys).
- Cross-high `(ι,δ)` collisions on {cen['n_rows_with_cross_high_coll']} rows.

Census: families checked={cen['n_families_checked']} all disjoint.

## OPEN

1. Residual high separation inside e·p budget (or single residual high for A_SP)
2. `M_pad≤1` at free_core=`{d['free_core']}`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v25.py --check
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
        "# kb-qatom-route-d-v25\n\n"
        "Free-1 high families pairwise disjoint; |F_H|≤⌊n/e⌋.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v25 report\n\nstatus: {cert['status']}\n"
        f"floor n/e: {cert['deployed']['floor_n_over_e']}\n"
        f"floor le e: {cert['deployed']['floor_le_e']}\n"
        f"cross high gap: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free-1 high families pairwise disjoint: PROVED")
    print(f"  |F_H| ≤ ⌊n/e⌋ = {FLOOR_N_OVER_E} ≤ e = {E}: PROVED (deployed)")
    print("  within-family (ι,δ) pair mark: PROVED")
    print("  cross-high (ι,δ): OPEN (toys collide)")
    print(f"  families checked: {cen['n_families_checked']} all disjoint")
    print(f"  cross-high coll rows: {cen['n_rows_with_cross_high_coll']}")


if __name__ == "__main__":
    main()
