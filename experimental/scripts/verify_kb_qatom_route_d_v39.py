#!/usr/bin/env python3
"""KB-MCA Route-D v39: H^{≤R_max} ledger + overflow pair cell; L-gate restated.

Fixes high cardinality via ledger thinning; overflow pairs get enum e·p mark
under cardinality; L≤70 remains a parallel ambient gate.

Proved:
  (1) Load bound (v38): |H| ≤ (n/e)·L with L = max point-high load.
      Deployed: L≤70 ⇒ |H|≤2170. Ambient L≤70 still OPEN.
  (2) Ledger core-high set: H_core := highs matched by multi-tier FM with
      tier < R_max (R_max = ⌊K_cap/⌊n/e⌋⌋ = 70). Then
        |H_core| ≤ R_max · ⌊n/e⌋ ≤ K_cap = 2170.
      PROVED by construction (v34 multi-tier).
  (3) Overflow highs H_over := H_A_SP \\ H_core. Overflow pairs =
      A_SP pairs whose high ∈ H_over (or either side’s high ∈ H_over).
  (4) Core-side payment: pairs with high ∈ H_core pay via multi-tier κ on H_core
      (size ≤K_cap) and (ι,δ) within family — fits e·p under M_pad≤1 path.
  (5) Overflow pair enum mark: order overflow unique pairs by
      (high_repr, c0U, c0V) or (minU, c0U, c0V); rank i; μ_over=(i mod e, ⌊i/e⌋).
      Injective. If N_over ≤ e·p then lands in [e]×F_p.
  (6) Under |H_over| ≤ K_cap: N_over ≤ |H_over|·⌊n/e⌋·(⌊n/e⌋−1) ≤ N_S-style
      bound ≪ e·p, so μ_over is size-e·p. (If H_over large, same cardinality gate.)
  (7) Combined ledger: SR-cell (v35–v38) + Type D residual + core sides (H_core)
      + overflow enum sides. Closes when overflow cardinality ≤e·p (true if
      |H_over|≤K_cap or N_over≤e·p directly).
  (8) Toy bank: H_core size ≤ capacity; overflow enum inj; L measured;
      ambient L can exceed 70 on small fields (not a counter to deployed L-gate
      without scale); core/overflow pair split.

Does NOT prove ambient L≤70 or ambient |H|≤2170 without thinning.

  python3 experimental/scripts/verify_kb_qatom_route_d_v39.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v39.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v39"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v39.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v39.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v39.report.md"
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
R_MAX = K_MAX // FLOOR_N_OVER_E  # 70
K_CAP = R_MAX * FLOOR_N_OVER_E  # 2170
L_GATE = K_CAP // FLOOR_N_OVER_E  # 70
PAIRS_PER_HIGH_MAX = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)
N_OVER_UNDER_HCAP = K_CAP * PAIRS_PER_HIGH_MAX


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


def lemma_H_core() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "ledger_H_core_bounded_by_Kcap",
        "statement": (
            f"Define H_core = {{ highs matched by multi-tier FM with tier < R_max }} "
            f"with R_max = {R_MAX}. Then |H_core| ≤ R_max · ⌊n/e⌋ = {K_CAP}. "
            "Core A_SP pairs (high ∈ H_core) pay via multi-tier κ + (ι,δ)."
        ),
        "proof": [
            "Each tier matches ≤⌊n/e⌋ highs (v33 FM-match).",
            f"R_max tiers ⇒ ≤{K_CAP} highs.",
            f"Deployed R_max·⌊n/e⌋ = {R_MAX}·{FLOOR_N_OVER_E} = {K_CAP} ≤ K_max={K_MAX}.",
        ],
        "deployed": {"R_max": R_MAX, "K_cap": K_CAP},
    }


def lemma_overflow_enum() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "overflow_pair_enum_mark_ep",
        "statement": (
            "Let overflow pairs be unique free-1 CS ordered pairs whose high "
            "∉ H_core. Order them by (c0U, c0V, high_repr) lex; rank i; set "
            "μ_over=(i mod e, ⌊i/e⌋). Injective. If N_over ≤ e·p then "
            "μ_over injects into [e]×F_p. Under |H_over|≤K_cap, "
            f"N_over ≤ {N_OVER_UNDER_HCAP} ≤ e·p."
        ),
        "proof": [
            "Same mixed-radix rank as SR μ_enum (v38).",
            "N_over ≤ |H_over|·⌊n/e⌋·(⌊n/e⌋−1) as for N_side (v36).",
        ],
        "note": (
            "If multi-tier is run with enough tiers to match ALL highs, H_over=∅ "
            "and N_over=0 whenever |H|≤K_cap (v37). Overflow cell is for the "
            "ledger choice that freezes R_max and leaves late-tier highs unpaid "
            "by core tags — or for |H|>K_cap."
        ),
    }


def lemma_load_gate() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "load_gate_L_le_70",
        "statement": (
            f"|H| ≤ (n/e)·L with L=max point-high load (v38). "
            f"Hence L≤{L_GATE} ⇒ |H|≤{K_CAP}. Ambient proof of L≤{L_GATE} OPEN."
        ),
        "proof": ["v38 load bound."],
        "deployed_L_gate": L_GATE,
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_L_le_70_or_overflow_when_H_huge",
        "statement": (
            f"(1) Prove L≤{L_GATE} at deployed A_SP activity.\n"
            "(2) If |H|>K_cap, bound N_over or inject overflow without |H_over|≤K_cap."
        ),
    }


def multitier_fm_tags(
    high_Us: dict[Any, list], n: int, e: int, max_tiers: int
) -> dict[Any, tuple[int, int]]:
    remaining = {h for h, us in high_Us.items() if us}
    tags: dict[Any, tuple[int, int]] = {}
    for tau in range(max_tiers):
        if not remaining:
            break
        free = set(range(n))
        local = 0
        highs = sorted(
            remaining, key=lambda h: (min(min(u) for u in high_Us[h]), repr(h))
        )
        claimed: set = set()
        for r in range(n):
            if r not in free:
                continue
            for h in highs:
                if h in claimed or h not in remaining:
                    continue
                for U in high_Us[h]:
                    Us = set(U)
                    if r in Us and Us.issubset(free):
                        free -= Us
                        tags[h] = (tau, local)
                        local += 1
                        claimed.add(h)
                        break
        remaining -= claimed
        if not claimed and remaining:
            h = min(remaining, key=repr)
            tags[h] = (tau, 0)
            remaining.discard(h)
    return tags


def toy_suite() -> dict[str, Any]:
    rows = []
    n_core_ok = 0
    n_over_enum_inj = 0
    n_over_rows = 0
    max_L = 0

    ensure(K_CAP == 2170, "Kcap")
    ensure(R_MAX == 70, "Rmax")
    ensure(L_GATE == 70, "Lgate")
    ensure(N_OVER_UNDER_HCAP < E_P, "over room")
    ensure((N_OVER_UNDER_HCAP - 1) // E < P, "over enum second < p")

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
        # toy R_max: use same formula scaled — min tiers so capacity ~ e
        R_toy = max(1, e // max(floor_ne, 1))
        cap_toy = R_toy * floor_ne
        vals = domain_vals(p, n)

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        high_Us: dict[Any, list] = defaultdict(list)
        seen: dict[Any, set] = defaultdict(set)
        pairs: list = []

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((U, c0, high))
            for key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        U, c0U, high = a
                        V, c0V, _ = b
                        if c0U == c0V:
                            continue
                        ut = tuple(sorted(U))
                        vt = tuple(sorted(V))
                        pairs.append((high, ut, vt, c0U, c0V))
                        if ut not in seen[high]:
                            seen[high].add(ut)
                            high_Us[high].append(U)

        nH = len(high_Us)
        # Load L
        covers = {
            h: set().union(*[set(u) for u in us]) if us else set()
            for h, us in high_Us.items()
        }
        pt_h: dict[int, set] = defaultdict(set)
        for h, cset in covers.items():
            for r in cset:
                pt_h[r].add(h)
        L = max((len(s) for s in pt_h.values()), default=0)
        max_L = max(max_L, L)
        if nH > 0 and L > 0:
            ensure(all(len(covers[h]) == e * len(high_Us[h]) for h in high_Us), "disj")
            ensure(nH * e <= n * L, "load")

        # Multi-tier with many tiers to assign all, then split by R_toy
        R_all = max(nH + 3, R_toy + 3)
        tags = multitier_fm_tags(high_Us, n, e, max_tiers=R_all)
        ensure(len(tags) == nH, "all tagged")
        H_core = {h for h, (tau, _) in tags.items() if tau < R_toy}
        H_over = {h for h, (tau, _) in tags.items() if tau >= R_toy}
        ensure(len(H_core) <= cap_toy, f"core {len(H_core)}>{cap_toy}")
        n_core_ok += 1

        # unique pairs
        seen_fp: set = set()
        pairs_core = []
        pairs_over = []
        for h, U, V, cu, cv in pairs:
            fp = (U, V)
            if fp in seen_fp:
                continue
            seen_fp.add(fp)
            if h in H_core:
                pairs_core.append((h, U, V, cu, cv))
            else:
                pairs_over.append((h, U, V, cu, cv))

        # overflow enum
        over_enum_inj = None
        if pairs_over:
            n_over_rows += 1
            ordered = sorted(
                pairs_over, key=lambda t: (t[3], t[4], min(t[1]), min(t[2]), repr(t[0]))
            )
            rank = { (t[1], t[2]): i for i, t in enumerate(ordered) }
            buckets: dict[Any, list] = defaultdict(list)
            for t in ordered:
                i = rank[(t[1], t[2])]
                buckets[(i % e, i // e)].append((t[1], t[2]))
            over_enum_inj = (
                all(len(set(v)) == 1 for v in buckets.values())
                and len(buckets) == len(ordered)
            )
            ensure(over_enum_inj, "over enum")
            n_over_enum_inj += 1
            if len(ordered) <= e * p:
                ensure(max(i // e for i in rank.values()) < p, "over second <p")

        # core pairs: (tau, local, delta) should inject among core pairs
        core_inj = None
        if pairs_core:
            buckets_c: dict[Any, list] = defaultdict(list)
            seen_c: set = set()
            for h, U, V, cu, cv in pairs_core:
                fp = (U, V)
                if fp in seen_c:
                    continue
                seen_c.add(fp)
                tau, local = tags[h]
                # need iota within high — use min U rank among high's U by c0
                # simpler: (tau, local, cu, delta) may be large; use (tau, local, delta)
                # may collide across U of same high
                buckets_c[(tau, local, (cu - cv) % p)].append(fp)
            # strengthen with min(U)
            buckets_c2: dict[Any, list] = defaultdict(list)
            seen_c2: set = set()
            for h, U, V, cu, cv in pairs_core:
                fp = (U, V)
                if fp in seen_c2:
                    continue
                seen_c2.add(fp)
                tau, local = tags[h]
                buckets_c2[(tau, local, min(U), (cu - cv) % p)].append(fp)
            core_inj = all(len(set(v)) == 1 for v in buckets_c2.values()) and len(
                buckets_c2
            ) == len(seen_c2)

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "free_core": free_core,
                "n_H": nH,
                "L": L,
                "H_bound": (n * L) // e if L else 0,
                "R_toy": R_toy,
                "cap_toy": cap_toy,
                "n_H_core": len(H_core),
                "n_H_over": len(H_over),
                "n_pairs_core": len(pairs_core),
                "n_pairs_over": len(pairs_over),
                "frac_over": len(pairs_over) / max(len(pairs_core) + len(pairs_over), 1),
                "over_enum_inj": over_enum_inj,
                "core_mark_inj": core_inj,
                "H_core_le_cap": len(H_core) <= cap_toy,
            }
        )

    ensure(n_core_ok == len(rows), "core cap all rows")
    # some rows have overflow when R_toy small
    ensure(n_over_rows > 0, "have overflow rows")
    ensure(n_over_enum_inj == n_over_rows, "over enum")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "n_over_rows": n_over_rows,
            "n_over_enum_inj": n_over_enum_inj,
            "max_L": max_L,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v39",
        "title": "H_core ledger ≤K_cap + overflow pair enum e·p",
        "status": "PARTIAL_HCORE_OVERFLOW",
        "claims": {
            "proves_H_core_le_Kcap": True,
            "proves_overflow_enum_ep_under_cardinality": True,
            "proves_L_le_70_deployed": False,
            "proves_ambient_H_le_Kcap": False,
            "proves_load_bound": True,
            "proves_A_SP_le_tp": False,
            "toy_confirms_core_overflow_split": True,
        },
        "deployed": {
            "R_max": R_MAX,
            "K_cap": K_CAP,
            "L_gate": L_GATE,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "N_over_under_Hcap": N_OVER_UNDER_HCAP,
            "e_p": E_P,
            "free_core": FREE_CORE,
            "t_p": T_P,
        },
        "lemmas": {
            "H_core": lemma_H_core(),
            "overflow": lemma_overflow_enum(),
            "load": lemma_load_gate(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "ledger": (
                f"Fix H_core with |H_core|≤{K_CAP}; pay overflow pairs by μ_over "
                f"when N_over≤e·p (ensured if |H_over|≤{K_CAP})"
            ),
            "ambient": f"L≤{L_GATE} still the ambient path to |H|≤{K_CAP}",
            "next": (
                f"Prove L≤{L_GATE}, or show multi-tier with R≤R_max matches all "
                "deployed A_SP highs (H_over=∅)"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_H']} | {r['L']} | "
        f"{r['n_H_core']} | {r['n_H_over']} | {r['n_pairs_core']} | "
        f"{r['n_pairs_over']} | {r['over_enum_inj']} | {r['H_core_le_cap']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v39: H_core ≤K_cap ledger + overflow enum

Status: `PARTIAL` — **H_core ≤{d['K_cap']}** PROVED by ledger; overflow **μ_over
e·p under cardinality** PROVED; ambient **L≤{d['L_gate']}** still OPEN.

## Path A — Ledger thinning (PROVED structure)

```text
R_max = {d['R_max']}
H_core = highs with multi-tier FM tier < R_max
|H_core| ≤ R_max · ⌊n/e⌋ = {d['K_cap']}
```

- **Core pairs** (high ∈ H_core): pay with multi-tier κ + (ι,δ)
- **Overflow pairs** (high ∉ H_core): pay with μ_over enum

### Overflow enum (PROVED)

```text
order overflow pairs → rank i
μ_over = (i mod e, ⌊i/e⌋)
```

If `N_over ≤ e·p` (e.g. `|H_over|≤{d['K_cap']}`), lands in `[e]×F_p`.

If multi-tier is allowed enough tiers to match all highs and `|H|≤K_cap`, then
`H_over=∅` and overflow is empty (v37).

## Path B — Ambient load gate (PROVED inequality, OPEN gate)

```text
|H| ≤ (n/e) · L
L ≤ {d['L_gate']}  ⇒  |H| ≤ {d['K_cap']}
```

Toys: max L={cen['max_L']} (can exceed 70 on small fields; not a deployed refutation).

## Full A_SP sketch with ledger

```text
1. SR-cell (Type S) — μ_enum e·p if |H|≤K_cap (v38)
2. Type D residual — M_pad ≤ 2
3. Core sides — H_core tags (≤K_cap)
4. Overflow sides — μ_over e·p if N_over≤e·p
```

## Toys

| j | w | free_core | #H | L | #H_core | #H_over | #pairs core | #pairs over | over enum? | core≤cap? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
{tbl}

## OPEN

1. `L ≤ {d['L_gate']}` at deployed A_SP
2. Show deployed A_SP highs fit in R_max tiers (H_over=∅), or bound N_over

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v39.py --check
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
        "# kb-qatom-route-d-v39\n\n"
        "H_core ≤K_cap ledger + overflow pair enum e·p.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v39 report\n\nstatus: {cert['status']}\n"
        f"H_core le {K_CAP}: PROVED\n"
        f"overflow enum e·p under cardinality: PROVED\n"
        f"L le {L_GATE}: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  H_core ≤ R_max·⌊n/e⌋ = {K_CAP}: PROVED (ledger)")
    print(
        f"  overflow μ_over e·p under |H_over|≤{K_CAP} / N_over≤e·p: PROVED"
    )
    print(f"  ambient L≤{L_GATE} for |H|≤{K_CAP}: OPEN (load bound PROVED)")
    print(
        f"  toys: over enum inj={cen['n_over_enum_inj']}/{cen['n_over_rows']}; "
        f"max L={cen['max_L']}"
    )


if __name__ == "__main__":
    main()
