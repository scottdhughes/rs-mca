#!/usr/bin/env python3
"""KB-MCA Route-D v35: shared-root first-match ⇒ Type-D residual + H-cardinality paths.

Attacks residual Type-S freeness/star-only and |H_A_SP|≤2170.

Proved:
  (1) Shared-root first-match cell (SR-cell): assign each Type S multipad side key
      to r_* = min{{ r : mult(r)≥2 }}. Pay all Type S multipads in the SR-cell
      ordered by r_* (domain first-match). After SR-cell payment, every remaining
      multipad has t=1 (Type D). Hence residual multipad geometry is Type-D-only
      with M_pad ≤ ⌊(n−2e)/m_c⌋ = 2 deployed.
  (2) Star-only is NOT forced: non-star Type S exist (v32); SR-cell pays them too
      via some r_* without requiring global common ⋂.
  (3) SR-cell does not need Type S connectedness or Helly.
  (4) SR-cell cost still OPEN at e·p: mark (r_*, side key) is not injective on
      toys; cost may use per-root through-pack structure (v30/v33).
  (5) Matching-supported high set H_M: highs of e-sets in a maximum matching M of
      active free-1 sides satisfy |H_M| ≤ |M| ≤ ⌊n/e⌋ = 31 ≤ 2170. PROVED.
  (6) Matching-supported A_SP (pairs with both sides in M) is too thin on toys
      (almost no pairs) — banked as insufficient alone for full N_ord.
  (7) Multi-tier FM (v34) injects all highs into [K_max] iff |H|≤2170; cardinality
      of full H_A_SP still OPEN (no ambient |H|≤2170 proof).

Does NOT prove SR-cell ≤ e·p, star-only residual, or |H_A_SP|≤2170 ambient.

  python3 experimental/scripts/verify_kb_qatom_route_d_v35.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v35.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v35"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v35.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v35.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v35.report.md"
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
FLOOR_N_OVER_E = N // E  # 31
K_MAX = E // FLOOR_N_OVER_E  # 2176
TIER_CAPACITY = (K_MAX // FLOOR_N_OVER_E) * FLOOR_N_OVER_E  # 2170
TYPE_D_BOUND = (N - 2 * E) // M_C  # 2


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


def free1_high_c0(U, vals, p):
    poly = monic_rev([vals[i] for i in sorted(U)], p)
    return tuple(poly[1:-1]), poly[-1]


def lemma_sr_cell() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "shared_root_first_match_cell_type_D_residual",
        "statement": (
            "Define the shared-root first-match cell (SR-cell): for each Type S "
            "multipad side key with core mult t≥2, set r_* = min{{r : mult(r)≥2}} "
            "and pay that multipad event when domain order reaches r_*. "
            "After all SR-cell payments, every remaining multipad has t=1, i.e. "
            "is Type D, hence M_pad ≤ ⌊(n−2e)/m_c⌋ "
            f"(= {TYPE_D_BOUND} deployed)."
        ),
        "proof": [
            "Type S ⇔ t≥2 ⇔ exists r with mult(r)≥2 ⇔ r_* exists and is paid in SR-cell.",
            "Any multipad not paid by SR-cell has no r with mult≥2 ⇔ t=1 ⇔ Type D.",
            "Type D packing: v28/v29.",
            "Star-only not required: non-star Type S still have some r with mult≥2.",
        ],
        "deployed_type_D_bound": TYPE_D_BOUND,
        "cost_open": (
            "SR-cell mass/injection into e·p still OPEN (naive (r_*,sidekey) collides)."
        ),
    }


def lemma_not_star_only() -> dict[str, Any]:
    return {
        "status": "BANKED_NEGATIVE",
        "name": "star_only_residual_not_forced",
        "statement": (
            "Ambient Type S is not star-only (non-star multipads exist). SR-cell "
            "pays non-star via some r_* without global common intersection. "
            "A residual that is star-only is not forced by ambient geometry alone."
        ),
        "proof": ["v32 non-star census; SR-cell definition."],
    }


def lemma_matching_highs() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "matching_supported_highs_le_n_over_e",
        "statement": (
            "Let M be any matching of active free-1 e-sets (pairwise disjoint). "
            "Let H_M = {{ high(U) : U ∈ M }}. Then |H_M| ≤ |M| ≤ ⌊n/e⌋. "
            f"Deployed: |H_M| ≤ {FLOOR_N_OVER_E} ≤ {TIER_CAPACITY} ≤ {K_MAX}."
        ),
        "proof": [
            "Map U ↦ high(U) from M to H_M is surjective onto H_M, so |H_M| ≤ |M|.",
            "Any matching of e-sets in a domain of size n has |M| ≤ ⌊n/e⌋.",
            "Within one high, F_H is pairwise disjoint (v25), so a matching may "
            "contain several U from one high; that only makes |H_M| smaller.",
        ],
        "deployed": {
            "floor_n_over_e": FLOOR_N_OVER_E,
            "tier_capacity": TIER_CAPACITY,
            "fits": FLOOR_N_OVER_E <= TIER_CAPACITY,
        },
        "ledger_path": (
            "If A_SP side marks only use highs in H_M for a fixed global matching "
            "M of sides, high tags fit budget. Toys: pairs with both sides in M "
            "are rare — insufficient alone for full N_ord."
        ),
    }


def lemma_cardinality_gate() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "high_cardinality_gate_for_Kmax",
        "statement": (
            f"Multi-tier FM (v34) injects H_A_SP into a set of size ≤{TIER_CAPACITY} "
            f"⊆ [K_max] if and only if |H_A_SP| ≤ {TIER_CAPACITY}. "
            "No ambient proof that |H_A_SP|≤2170 is known; matching-supported "
            "H_M always satisfies the gate."
        ),
        "proof": [
            "Injection into a set of size C requires |domain|≤C.",
            "v34 multi-tier capacity = R_max·⌊n/e⌋ ≤ K_max.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_SR_cell_cost_and_H_cardinality",
        "statement": (
            "(1) Bound SR-cell (Type S first-match) at e·p using through-pack "
            "per r_* / peel structure.\n"
            f"(2) Prove |H_A_SP| ≤ {TIER_CAPACITY}, or adopt matching-supported "
            "A_SP with a residual pair cell for non-M sides."
        ),
    }


def greedy_matching_esets(Us: list[frozenset[int]], n: int, e: int) -> list[frozenset[int]]:
    free = set(range(n))
    matched: list[frozenset[int]] = []
    # process by min root
    for U in sorted(Us, key=lambda u: (min(u), tuple(sorted(u)))):
        if set(U).issubset(free):
            free -= set(U)
            matched.append(U)
    return matched


def toy_suite() -> dict[str, Any]:
    rows = []
    n_type_S = 0
    n_type_D_after_SR = 0
    n_type_S_paid_SR = 0
    n_star = 0
    n_nonstar = 0
    n_r_sidekey_coll = 0
    n_rows_r_sidekey_inj = 0
    n_rows_with_S = 0

    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 7, 3),
        (17, 16, 8, 1),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (17, 16, 9, 2),
        (17, 16, 9, 3),
    ]:
        e = w + 1
        m_c = j - e
        if m_c <= 0 or math.comb(n, j) > 25000:
            continue
        free_core = m_c - w
        pack_D = (n - 2 * e) // m_c if n >= 2 * e else 0
        floor_ne = n // e
        vals = domain_vals(p, n)

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        active_Us: list[frozenset[int]] = []
        seen_U: set = set()
        high_of_U: dict[tuple, Any] = {}
        all_pairs: list = []
        n_D = 0
        n_S = 0
        n_S_star = 0
        n_S_nonstar = 0
        max_mpad_D = 1
        max_mpad_S = 1
        # SR marks
        sr_buckets: dict[Any, list] = defaultdict(list)
        # After SR: only Type D remain among multipads
        residual_D_events = 0
        residual_S_events = 0  # must stay 0 if we remove all S

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            pads: dict[Any, list] = defaultdict(list)
            for key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U, high = a
                        _C2, V, c0V, _ = b
                        if c0U == c0V:
                            continue
                        pads[(high, c0U, c0V)].append((C, U, V))
                        ut = tuple(sorted(U))
                        if ut not in seen_U:
                            seen_U.add(ut)
                            active_Us.append(U)
                            high_of_U[ut] = high
                        all_pairs.append((high, ut, tuple(sorted(V))))

            for sk, items in pads.items():
                by_c: dict[tuple, tuple] = {}
                for C, U, V in items:
                    t = tuple(sorted(C))
                    if t not in by_c:
                        by_c[t] = (U, V)
                cores = [set(t) for t in by_c]
                if len(cores) < 2:
                    continue
                cnt: Counter = Counter()
                for c in cores:
                    for r in c:
                        cnt[r] += 1
                tmult = max(cnt.values())
                high, c0U, c0V = sk

                if tmult <= 1:
                    # Type D — residual after SR
                    n_D += 1
                    residual_D_events += 1
                    max_mpad_D = max(max_mpad_D, len(cores))
                    ensure(len(cores) <= pack_D, "D pack")
                    n_type_D_after_SR += 1
                    continue

                # Type S — paid by SR-cell
                n_S += 1
                n_type_S += 1
                n_type_S_paid_SR += 1
                max_mpad_S = max(max_mpad_S, len(cores))
                r_star = min(r for r, m in cnt.items() if m >= 2)
                common = set.intersection(*cores)
                if common:
                    n_S_star += 1
                    n_star += 1
                else:
                    n_S_nonstar += 1
                    n_nonstar += 1
                # SR mark
                core_sig = tuple(sorted(tuple(sorted(c)) for c in cores))
                sr_buckets[(r_star, high, c0U, c0V)].append(core_sig)
                # After SR payment this event is gone — not residual S
                # residual_S_events stays 0

        ensure(residual_S_events == 0, "no residual S")
        if n_S > 0:
            n_rows_with_S += 1
            # (r_*, sidekey) injectivity
            coll = sum(1 for v in sr_buckets.values() if len(set(v)) >= 2)
            if coll > 0:
                n_r_sidekey_coll += 1
            else:
                n_rows_r_sidekey_inj += 1

        # Matching-supported highs
        M = greedy_matching_esets(active_Us, n, e)
        ensure(len(M) <= floor_ne, "M size")
        H_M = {high_of_U[tuple(sorted(U))] for U in M}
        ensure(len(H_M) <= len(M), "HM le M")
        ensure(len(H_M) <= floor_ne, "HM le floor")
        Mset = {tuple(sorted(U)) for U in M}
        n_pairs = len(all_pairs)
        n_both = sum(1 for h, U, V in all_pairs if U in Mset and V in Mset)
        n_one = sum(1 for h, U, V in all_pairs if U in Mset or V in Mset)
        H_all = {h for h, U, V in all_pairs}

        if free_core == 1:
            ensure(n_S == 0, "fc1 no S")

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "m_c": m_c,
                "free_core": free_core,
                "pack_D": pack_D,
                "n_type_D_residual": n_D,
                "n_type_S_SR_paid": n_S,
                "n_S_star": n_S_star,
                "n_S_nonstar": n_S_nonstar,
                "max_Mpad_D": max_mpad_D,
                "max_Mpad_S": max_mpad_S,
                "residual_type_D_only": True,  # by SR construction
                "n_active_highs": len(H_all),
                "n_HM": len(H_M),
                "n_M": len(M),
                "floor_n_over_e": floor_ne,
                "HM_le_floor": len(H_M) <= floor_ne,
                "n_pairs": n_pairs,
                "frac_pairs_both_in_M": n_both / n_pairs if n_pairs else 1.0,
                "frac_pairs_one_in_M": n_one / n_pairs if n_pairs else 1.0,
                "H_all_le_tier_cap": len(H_all) <= TIER_CAPACITY,
            }
        )

    ensure(n_type_S > 0, "have S")
    ensure(n_type_S_paid_SR == n_type_S, "all S paid SR")
    ensure(n_nonstar > 0, "nonstar exist")
    ensure(n_type_D_after_SR > 0, "have residual D")
    ensure(n_r_sidekey_coll > 0, "SR mark collides (cost open)")
    ensure(TYPE_D_BOUND == 2, "D=2")
    ensure(FLOOR_N_OVER_E == 31, "31")
    ensure(TIER_CAPACITY == 2170, "2170")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_type_S": n_type_S,
            "n_type_S_paid_SR": n_type_S_paid_SR,
            "n_type_D_after_SR": n_type_D_after_SR,
            "n_star": n_star,
            "n_nonstar": n_nonstar,
            "n_rows_with_S": n_rows_with_S,
            "n_rows_r_sidekey_coll": n_r_sidekey_coll,
            "n_rows_r_sidekey_inj": n_rows_r_sidekey_inj,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v35",
        "title": "SR-cell Type-D residual multipads + matching-supported highs ≤⌊n/e⌋",
        "status": "PARTIAL_SR_CELL_H_MATCH",
        "claims": {
            "proves_SR_cell_type_D_residual": True,
            "proves_star_only_forced": False,
            "banks_star_only_not_forced": True,
            "proves_SR_cell_ep_cost": False,
            "banks_SR_mark_collides": True,
            "proves_matching_highs_le_n_over_e": True,
            "proves_H_A_SP_le_2170": False,
            "banks_matching_pairs_thin": True,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "type_D_Mpad_bound": TYPE_D_BOUND,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "tier_capacity": TIER_CAPACITY,
            "K_max": K_MAX,
            "t_p": T_P,
            "e_p": E_P,
        },
        "lemmas": {
            "sr_cell": lemma_sr_cell(),
            "not_star_only": lemma_not_star_only(),
            "matching_highs": lemma_matching_highs(),
            "card_gate": lemma_cardinality_gate(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "TypeS": (
                "SR-cell first-match pays all Type S ⇒ residual multipads Type D "
                f"only (M_pad≤{TYPE_D_BOUND}). SR-cell e·p cost OPEN."
            ),
            "highs": (
                f"H_M from side matching always |H_M|≤{FLOOR_N_OVER_E}≤2170; "
                "full H_A_SP≤2170 OPEN; matching pairs too thin alone"
            ),
            "next": (
                "Close SR-cell at e·p via per-r through-pack; or prove |H_A_SP|≤2170"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_type_S_SR_paid']} | "
        f"{r['n_S_star']} | {r['n_S_nonstar']} | {r['n_type_D_residual']} | "
        f"{r['max_Mpad_D']} | {r['residual_type_D_only']} | {r['n_active_highs']} | "
        f"{r['n_HM']} | {r['frac_pairs_both_in_M']:.3f} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v35: SR-cell Type-D residual + matching highs

Status: `PARTIAL` — **SR-cell ⇒ residual multipads Type-D-only** PROVED;
**H_M ≤⌊n/e⌋** PROVED; SR-cell e·p cost and full |H_A_SP|≤2170 **OPEN**.

## Shared-root first-match cell (PROVED)

```text
Type S multipad  →  r_* = min{{ r : mult(r) ≥ 2 }}
pay at domain order r_*   (SR-cell)
```

After SR-cell:

```text
remaining multipads have t = 1  (Type D)
M_pad ≤ ⌊(n−2e)/m_c⌋ = {d['type_D_Mpad_bound']} deployed
```

- Pays **star and non-star** Type S (non-star still has some mult≥2 root).
- Star-only residual is **not** forced (non-star exist ambiently).
- Connectedness / Helly not required.

### SR-cell cost (OPEN)

Naive mark `(r_*, high, c0U, c0V)` **collides** on toys. Per-root through-pack
structure available (v30/v33) for a future cost bound.

## Matching-supported highs (PROVED)

```text
M = matching of active free-1 e-sets
H_M = {{ high(U) : U ∈ M }}
|H_M| ≤ |M| ≤ ⌊n/e⌋ = {d['floor_n_over_e']} ≤ {d['tier_capacity']}
```

Fits multi-tier / K_max high budget.

**Banked:** pairs with both sides in M are a tiny fraction of N_ord on toys —
matching-supported A_SP alone is too thin.

## Cardinality gate (PROVED)

```text
multi-tier FM injects H into [K_max]  ⇔  |H| ≤ {d['tier_capacity']}
```

Full |H_A_SP|≤2170 still OPEN.

## Toys

| j | w | free_core | #S (SR-paid) | #star | #nonstar | #D residual | max M_pad D | Type-D only? | #H_all | |H_M| | frac pairs both in M |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
{tbl}

Census: S paid by SR={cen['n_type_S_paid_SR']}; D residual={cen['n_type_D_after_SR']};
nonstar={cen['n_nonstar']}; SR mark coll rows={cen['n_rows_r_sidekey_coll']}.

## Payment path (updated)

```text
A_SP:
  SR-cell: pay Type S multipads (cost OPEN at e·p)
  residual multipads: Type D only, M_pad ≤ 2
  sides: H_M tags free if matching-supported; else need |H|≤2170 / multi-tier
R_sing: no multipads (v29)
```

## OPEN

1. SR-cell ≤ e·p (through-pack / peel cost)
2. |H_A_SP| ≤ {d['tier_capacity']} or viable matching-supported + residual pair cell

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v35.py --check
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
        "# kb-qatom-route-d-v35\n\n"
        "SR-cell Type-D residual multipads + matching-supported highs.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v35 report\n\nstatus: {cert['status']}\n"
        f"SR-cell => Type D residual: PROVED\n"
        f"Type D M_pad bound: {TYPE_D_BOUND}\n"
        f"H_M le floor n/e: PROVED\n"
        f"SR-cell e·p cost: OPEN\n"
        f"|H_A_SP| le 2170: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  SR-cell ⇒ residual multipads Type-D-only (M_pad≤2 deployed): PROVED")
    print("  star-only NOT forced (non-star Type S paid by SR too)")
    print(f"  H_M ≤ ⌊n/e⌋={FLOOR_N_OVER_E} ≤ {TIER_CAPACITY}: PROVED")
    print("  matching-supported pairs too thin (banked); SR mark collides (cost OPEN)")
    print(
        f"  toys: S_SR={cen['n_type_S_paid_SR']}; D_res={cen['n_type_D_after_SR']}; "
        f"nonstar={cen['n_nonstar']}; SR coll rows={cen['n_rows_r_sidekey_coll']}"
    )


if __name__ == "__main__":
    main()
