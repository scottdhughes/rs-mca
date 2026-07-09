#!/usr/bin/env python3
"""KB-MCA Route-D v36: SR-cell e·p cardinality + matching/residual side split.

Closes SR-cell under |H| gate; formalizes matching-supported + residual pair cells.

Proved:
  (1) SR-cell Type-D residual (v35): after paying Type S at r_*, multipads are Type D.
  (2) SR-event count: N_S := # Type S side keys ≤ N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋−1)
      because each high has |F_H|≤⌊n/e⌋ and free-1 CS ordered pairs within high
      number ≤ |F_H|(|F_H|−1).
  (3) e·p room under high gate: if |H| ≤ K_cap := 2170 (= multi-tier capacity),
      then N_S ≤ 2170 · 31 · 30 = 2_018_100 ≪ e·p deployed, so abstract injection
      of SR-events into e·p exists (cardinality). Constructive e·p mark still OPEN;
      toys: (r_*, c0U, c0V) injective on Type S side keys (n·p² scale, not e·p).
  (4) Matching-supported side cell (M-cell): M matching of active free-1 e-sets;
      pairs with both sides in M; highs H_M with |H_M|≤⌊n/e⌋≤K_cap; pay with
      (κ,ι,δ) on H_M (v33–v34).
  (5) Residual pair cell (R-cell): pairs with U∉M or V∉M. Natural e·p marks
      (minU mod e, δ), (c0U, δ), … banked negative on toys (incomplete injection).
  (6) Combined path: SR-cell (Type S multipads) + Type D residual (M_pad≤2) +
      M-cell sides + R-cell sides. Closes at e·p if |H|≤K_cap (for SR+highs)
      and R-cell injects — R-cell injection OPEN.
  (7) Toy bank: N_S bound vs |H|·floor·(floor-1); (r_*,c0U,c0V) inj; M-cell thin;
      R-cell natural marks collide; Type D residual after SR.

Does NOT prove |H|≤2170, constructive SR e·p mark, or R-cell e·p injection.

  python3 experimental/scripts/verify_kb_qatom_route_d_v36.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v36.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v36"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v36.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v36.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v36.report.md"
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
K_CAP = (K_MAX // FLOOR_N_OVER_E) * FLOOR_N_OVER_E  # 2170
# max pairs per high under family size bound
PAIRS_PER_HIGH_MAX = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)  # 31*30=930
N_S_UNDER_HCAP = K_CAP * PAIRS_PER_HIGH_MAX  # 2018100
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


def lemma_SR_cardinality() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "SR_event_count_under_high_gate",
        "statement": (
            "Let N_S be the number of Type S multipad side keys (SR-events) and "
            "H the set of free-1 highs appearing in A_SP CS pairs. Then "
            "N_S ≤ N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋ − 1). "
            f"If |H| ≤ K_cap = {K_CAP}, then "
            f"N_S ≤ {N_S_UNDER_HCAP} ≪ e·p = {E_P} deployed, so an abstract "
            "injection of SR-events into a set of size e·p exists."
        ),
        "proof": [
            "Each Type S side key is an A_SP free-1 CS ordered pair, so N_S ≤ N_side.",
            "v25: |F_H| ≤ ⌊n/e⌋ per high; free-1 CS ordered pairs with a fixed high "
            "number at most |F_H|(|F_H|−1).",
            "Sum over highs: N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋−1).",
            f"Deployed: K_cap·31·30 = {N_S_UNDER_HCAP} < e·p ≈ 1.44e14.",
        ],
        "deployed": {
            "K_cap": K_CAP,
            "pairs_per_high_max": PAIRS_PER_HIGH_MAX,
            "N_S_under_Hcap": N_S_UNDER_HCAP,
            "e_p": E_P,
            "N_S_under_Hcap_lt_ep": N_S_UNDER_HCAP < E_P,
        },
        "constructive_gap": (
            "Cardinality ≠ constructive mark. Toys: (r_*, c0U, c0V) injects Type S "
            "keys at size n·p² (not e·p)."
        ),
    }


def lemma_SR_type_D() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "SR_cell_type_D_residual",
        "statement": (
            f"After SR-cell payment of all Type S, residual multipads are Type D "
            f"with M_pad ≤ {TYPE_D_BOUND} deployed (v35)."
        ),
        "proof": ["v35 shared-root first-match cell."],
    }


def lemma_MR_split() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "matching_and_residual_pair_cells",
        "statement": (
            "Fix a matching M of active free-1 e-sets. Split A_SP ordered pairs:\n"
            "  M-cell: both U,V ∈ M; highs ⊆ H_M with |H_M|≤⌊n/e⌋≤K_cap; "
            "  pay via (κ,ι,δ) on H_M.\n"
            "  R-cell: U∉M or V∉M; needs independent e·p mark (OPEN constructively)."
        ),
        "proof": [
            "v35 matching-supported highs.",
            "Partition of pairs is exhaustive.",
        ],
        "toy_note": "M-cell captures few pairs; R-cell is the bulk on toys.",
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_constructive_SR_ep_and_R_cell_and_Hcap",
        "statement": (
            "(1) Constructive SR-event mark of size ≤e·p (or per-r through-pack "
            "cost without full listing).\n"
            "(2) R-cell e·p injection for non-matching pairs.\n"
            f"(3) |H_A_SP| ≤ {K_CAP} to unlock SR cardinality + multi-tier high tags."
        ),
    }


def greedy_matching(Us: list, n: int) -> list:
    free = set(range(n))
    matched = []
    for U in sorted(Us, key=lambda u: (min(u), tuple(sorted(u)))):
        if set(U).issubset(free):
            free -= set(U)
            matched.append(U)
    return matched


def toy_suite() -> dict[str, Any]:
    rows = []
    n_type_S = 0
    n_type_D = 0
    n_rc0_inj_rows = 0
    n_rc0_rows = 0
    n_r_mark_coll_rows = 0

    # deployed arithmetic checks
    ensure(N_S_UNDER_HCAP < E_P, "N_S room")
    ensure(K_CAP == 2170, "Kcap")
    ensure(PAIRS_PER_HIGH_MAX == 930, "pph")
    ensure(TYPE_D_BOUND == 2, "D2")

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
        floor_ne = n // e
        pack_D = (n - 2 * e) // m_c if n >= 2 * e else 0
        pph = floor_ne * max(floor_ne - 1, 0)
        vals = domain_vals(p, n)

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        active_Us: list = []
        seen_U: set = set()
        high_of: dict = {}
        pairs: list = []
        S_keys: list = []  # (r_star, high, c0U, c0V) fiber-local events
        S_sidekeys: set = set()  # unique Type S side keys (high,c0U,c0V)
        n_D = 0
        n_S_events = 0  # fiber-local Type S multipad events
        max_mpad_D = 1
        max_mpad_S = 1
        highs_all: set = set()
        pairs_per_high: dict = defaultdict(set)

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
                        pads[(high, c0U, c0V)].append(C)
                        ut = tuple(sorted(U))
                        vt = tuple(sorted(V))
                        pairs.append((high, ut, vt, c0U, c0V))
                        highs_all.add(high)
                        pairs_per_high[high].add((ut, vt))
                        if ut not in seen_U:
                            seen_U.add(ut)
                            active_Us.append(U)
                            high_of[ut] = high

            for sk, Cs in pads.items():
                cores = [set(t) for t in {tuple(sorted(C)) for C in Cs}]
                if len(cores) < 2:
                    continue
                cnt: Counter = Counter()
                for c in cores:
                    for r in c:
                        cnt[r] += 1
                tmult = max(cnt.values())
                high, c0U, c0V = sk
                if tmult <= 1:
                    n_D += 1
                    n_type_D += 1
                    max_mpad_D = max(max_mpad_D, len(cores))
                    ensure(len(cores) <= pack_D, "D pack")
                else:
                    n_S_events += 1
                    max_mpad_S = max(max_mpad_S, len(cores))
                    r_star = min(r for r, m in cnt.items() if m >= 2)
                    S_keys.append((r_star, high, c0U, c0V))
                    S_sidekeys.add((high, c0U, c0V))

        n_S = len(S_sidekeys)  # unique Type S side keys for cardinality
        n_type_S += n_S

        # N_S / N_side bounds on UNIQUE ordered side pairs
        nH = len(highs_all)
        N_side_bound = nH * pph
        unique_side_pairs = {(h, U, V) for h, U, V, cu, cv in pairs}
        n_side_unique = len(unique_side_pairs)
        ensure(n_S <= n_side_unique, "S le unique sides")
        for h, ps in pairs_per_high.items():
            us = {u for u, v in ps} | {v for u, v in ps}
            ensure(len(us) <= floor_ne or floor_ne == 0, "family size")
            ensure(len(ps) <= len(us) * max(len(us) - 1, 0), "pairs per high")
        ensure(n_side_unique <= N_side_bound or nH == 0, "Nside bound")
        ensure(n_S <= N_side_bound or nH == 0, "NS bound")

        # (r_*, c0U, c0V) injectivity on unique S side keys
        # use one r_* per side key (min r_* over fiber events for that key)
        if S_sidekeys:
            n_rc0_rows += 1
            rstar_of: dict[Any, int] = {}
            for r_star, high, c0U, c0V in S_keys:
                sk = (high, c0U, c0V)
                if sk not in rstar_of or r_star < rstar_of[sk]:
                    rstar_of[sk] = r_star
            buckets: dict[Any, list] = defaultdict(list)
            for sk, r_star in rstar_of.items():
                high, c0U, c0V = sk
                buckets[(r_star, c0U, c0V)].append(sk)
            coll = sum(1 for v in buckets.values() if len(set(v)) >= 2)
            if coll == 0 and len(buckets) == len(S_sidekeys):
                n_rc0_inj_rows += 1
            else:
                n_r_mark_coll_rows += 1
            ensure(coll == 0, "toy (r*,c0U,c0V) inj on unique S keys")
            ensure(len(buckets) == len(S_sidekeys), "bucket count")

        # Matching split
        M = greedy_matching(active_Us, n)
        ensure(len(M) <= floor_ne, "M size")
        Mset = {tuple(sorted(U)) for U in M}
        H_M = {high_of[tuple(sorted(U))] for U in M if tuple(sorted(U)) in high_of}
        ensure(len(H_M) <= len(M), "HM")
        pairs_M = [
            (h, U, V, cu, cv)
            for h, U, V, cu, cv in pairs
            if U in Mset and V in Mset
        ]
        pairs_R = [
            (h, U, V, cu, cv)
            for h, U, V, cu, cv in pairs
            if not (U in Mset and V in Mset)
        ]

        # R-cell natural marks
        def r_inj(plist, fn):
            seen = set()
            buckets = defaultdict(list)
            for h, U, V, cu, cv in plist:
                fp = (U, V)
                if fp in seen:
                    continue
                seen.add(fp)
                buckets[fn(h, U, V, cu, cv)].append(fp)
            if not seen:
                return None
            coll = sum(1 for v in buckets.values() if len(set(v)) >= 2)
            return coll == 0 and len(buckets) == len(seen)

        r_marks = {}
        if pairs_R:
            r_marks["minU_mod_e_delta"] = r_inj(
                pairs_R, lambda h, U, V, cu, cv: (min(U) % e, (cu - cv) % p)
            )
            r_marks["c0U_delta"] = r_inj(
                pairs_R, lambda h, U, V, cu, cv: (cu, (cu - cv) % p)
            )
            r_marks["minU_delta"] = r_inj(
                pairs_R, lambda h, U, V, cu, cv: (min(U), (cu - cv) % p)
            )

        if free_core == 1:
            ensure(n_S == 0, "fc1")
        if free_core <= 0:
            ensure(max_mpad_S <= 1, "fc0")

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "m_c": m_c,
                "free_core": free_core,
                "n_type_D": n_D,
                "n_type_S": n_S,
                "max_Mpad_D": max_mpad_D,
                "max_Mpad_S": max_mpad_S,
                "n_highs": nH,
                "N_side_bound": N_side_bound,
                "n_pairs": len(pairs),
                "n_S_le_bound": n_S <= N_side_bound,
                "rstar_c0_injective": (n_S == 0) or True,  # ensured above when S
                "n_M": len(M),
                "n_HM": len(H_M),
                "n_pairs_M": len(pairs_M),
                "n_pairs_R": len(pairs_R),
                "frac_pairs_R": len(pairs_R) / len(pairs) if pairs else 0.0,
                "R_marks": r_marks,
                "pack_D": pack_D,
            }
        )

    ensure(n_type_S > 0, "S")
    ensure(n_type_D > 0, "D")
    ensure(n_rc0_rows > 0 and n_rc0_inj_rows == n_rc0_rows, "r*c0 inj all")
    # R marks should fail on some row
    ensure(
        any(
            r["R_marks"].get("minU_mod_e_delta") is False
            for r in rows
            if r["R_marks"]
        ),
        "R mark bank neg",
    )
    ensure(FREE_CORE == 846161, "fc")
    ensure(N_S_UNDER_HCAP == K_CAP * 31 * 30, "arith")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_type_S": n_type_S,
            "n_type_D": n_type_D,
            "n_rc0_inj_rows": n_rc0_inj_rows,
            "n_rc0_rows": n_rc0_rows,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v36",
        "title": "SR-cell e·p cardinality under |H| gate + M/R side split",
        "status": "PARTIAL_SR_CARD_MR_SPLIT",
        "claims": {
            "proves_SR_cardinality_under_Hcap": True,
            "proves_SR_type_D_residual": True,
            "proves_constructive_SR_ep_mark": False,
            "toy_confirms_rstar_c0_injection_np2": True,
            "proves_MR_pair_split": True,
            "proves_R_cell_ep_injection": False,
            "banks_R_cell_natural_negative": True,
            "proves_H_le_Kcap": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "K_cap": K_CAP,
            "K_max": K_MAX,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "pairs_per_high_max": PAIRS_PER_HIGH_MAX,
            "N_S_under_Hcap": N_S_UNDER_HCAP,
            "e_p": E_P,
            "type_D_bound": TYPE_D_BOUND,
            "N_S_under_Hcap_lt_ep": N_S_UNDER_HCAP < E_P,
            "t_p": T_P,
        },
        "lemmas": {
            "SR_card": lemma_SR_cardinality(),
            "SR_typeD": lemma_SR_type_D(),
            "MR_split": lemma_MR_split(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "SR": (
                f"If |H|≤{K_CAP} then N_S≤{N_S_UNDER_HCAP}≪e·p — SR-cell has e·p "
                "room (cardinality). Constructive mark OPEN; (r*,c0U,c0V) works at n·p²."
            ),
            "sides": (
                "M-cell: |H_M|≤31, few pairs; R-cell: bulk pairs, e·p mark OPEN"
            ),
            "next": (
                "Constructive SR e·p mark; R-cell injection; prove |H|≤K_cap"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_type_S']} | "
        f"{r['n_type_D']} | {r['n_highs']} | {r['n_pairs']} | {r['n_pairs_M']} | "
        f"{r['n_pairs_R']} | {r['frac_pairs_R']:.2f} | {r['rstar_c0_injective']} | "
        f"{r['R_marks'].get('minU_mod_e_delta')} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v36: SR-cell e·p cardinality + M/R side split

Status: `PARTIAL` — SR-cell has **e·p room under |H|≤K_cap** PROVED; M/R side
split PROVED; constructive SR/R marks and |H|≤K_cap still **OPEN**.

## SR-cell cardinality (PROVED)

```text
N_S ≤ N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋ − 1)
```

If `|H| ≤ K_cap = {d['K_cap']}`:

```text
N_S ≤ {d['N_S_under_Hcap']}  ≪  e·p = {d['e_p']}
```

⇒ abstract injection of SR-events into e·p exists.

Type-D residual after SR: `M_pad ≤ {d['type_D_bound']}` deployed.

### Constructive mark (OPEN / toy)

Toys: `(r_*, c0U, c0V)` injects Type S side keys (size `n·p²`, not `e·p`).

## M-cell / R-cell side split (PROVED)

```text
M = matching of active free-1 e-sets
M-cell: both sides in M, |H_M| ≤ ⌊n/e⌋ ≤ K_cap
R-cell: remaining pairs
```

Toys: R-cell is ~98–100% of pairs; natural R-cell e·p marks collide.

## Combined path

```text
1. SR-cell: Type S multipads     (e·p room if |H|≤K_cap; constructive OPEN)
2. Type D residual multipads     (M_pad ≤ 2)
3. M-cell sides                  (high tags free)
4. R-cell sides                  (e·p mark OPEN)
```

Closes full A_SP at e·p if |H|≤K_cap and R-cell injects.

## Toys

| j | w | free_core | #S | #D | #H | #pairs | #M-pairs | #R-pairs | frac R | (r*,c0) inj? | R minU mod e? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
{tbl}

Census: S={cen['n_type_S']}; D={cen['n_type_D']}; (r*,c0) inj rows={cen['n_rc0_inj_rows']}/{cen['n_rc0_rows']}.

## OPEN

1. Constructive SR mark size ≤e·p
2. R-cell e·p injection
3. `|H_A_SP| ≤ {d['K_cap']}`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v36.py --check
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
        "# kb-qatom-route-d-v36\n\n"
        "SR-cell e·p cardinality under |H| gate + matching/residual side split.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v36 report\n\nstatus: {cert['status']}\n"
        f"N_S under Hcap: {N_S_UNDER_HCAP} << e·p\n"
        f"SR constructive e·p: OPEN\n"
        f"R-cell e·p: OPEN\n"
        f"|H| le Kcap: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(
        f"  SR-cell: if |H|≤{K_CAP} then N_S≤{N_S_UNDER_HCAP}≪e·p (cardinality PROVED)"
    )
    print("  SR Type-D residual M_pad≤2: PROVED")
    print("  M/R side split: PROVED; R-cell natural marks banked negative")
    print(
        f"  toys: S={cen['n_type_S']}; (r*,c0U,c0V) inj={cen['n_rc0_inj_rows']}/{cen['n_rc0_rows']}"
    )


if __name__ == "__main__":
    main()
