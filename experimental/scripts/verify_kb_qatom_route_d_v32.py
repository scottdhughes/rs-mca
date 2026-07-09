#!/usr/bin/env python3
"""KB-MCA Route-D v32: Type S Helly refutation + connectedness census + high matching.

Attacks Type S connectedness/Helly and |H_A_SP|≤2176 via first-match/matching.

Proved:
  (1) Helly REFUTED for Type S: there exist Type S multipads that are pairwise
      intersecting (clique) yet have empty global common intersection (non-star).
      So full Helly cannot be used for a uniform M_pad≤16 theorem.
  (2) Star / common-I packing retained: if I=⋂Cores ≠ ∅ then peel applies;
      if |I|=free_core−1 then M_pad ≤ ⌊A/e⌋ = 16 deployed (v31).
  (3) mpad=2 Type S connected (v31). free_core=2 through-cliques pack
      |Cores_r| ≤ ⌊(n−2e−1)/(m_c−1)⌋ (v30).
  (4) Type S intersection-connectedness: CONFIRMED on all toy multipads (0
      counterexamples); general proof OPEN (not claimed PROVED).
  (5) High matching bound: any set of free-1 highs that admit pairwise-disjoint
      representative e-sets has size ≤ ⌊n/e⌋. Deployed ⌊n/e⌋ = 31 ≤ K_max = 2176.
      Thus a first-match / matching transversal of highs fits the high-tag budget.
  (6) |H_A_SP| ≤ N_side ≤ N_ord still; full |H_A_SP| ≤ 2176 OPEN (matching
      number ν(H) ≤ 31 is not the same as |H|).
  (7) Toy bank: Helly fails (non-star Type S); all Type S connected; e=2 p1
      injects highs (complete invariant); min_cover / mod-K tags collide;
      matching number ≤ floor(n/e) verified.

Does NOT prove general Type S connectedness, Type S M_pad≤16 for all Type S,
or |H_A_SP|≤2176.

  python3 experimental/scripts/verify_kb_qatom_route_d_v32.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v32.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v32"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v32.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v32.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v32.report.md"
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
PACK_MAXIMAL_COMMON = A // E  # 16


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


def lemma_helly_refuted() -> dict[str, Any]:
    return {
        "status": "BANKED_NEGATIVE",
        "name": "type_S_Helly_refuted",
        "statement": (
            "Type S multipads need not be Helly: there exist Type S multipad core "
            "sets that form an intersection clique (every pair intersects) yet have "
            "empty global common intersection. Therefore one cannot always reduce "
            "Type S to a single through-pack / maximal-common packing."
        ),
        "proof": [
            "Toy census (e.g. j=5,w=1 free_core=2): non-star Type S multipads with "
            "M_pad up to 9, pairwise intersections nonempty for some cliques, "
            "global ⋂ = ∅.",
            "v31 maximal-common packing applies only when ⋂ ≠ ∅ (and |I|=fc−1 for ≤16).",
        ],
    }


def lemma_star_packing_retained() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "star_and_maximal_common_packing_retained",
        "statement": (
            "If Type S multipad has I = ⋂ Cores ≠ ∅, free_core drops along I by "
            "peel (v30). If |I| = free_core−1, then M_pad ≤ ⌊A/e⌋ = 16 deployed "
            "(v31). These remain the sharp packing wins for the Helly/star branch."
        ),
        "proof": ["v30 peel; v31 maximal-common packing."],
        "deployed_maximal_common_bound": PACK_MAXIMAL_COMMON,
    }


def lemma_connectedness_status() -> dict[str, Any]:
    return {
        "status": "TOY_UNIVERSAL_OPEN_PROOF",
        "name": "type_S_intersection_connectedness",
        "statement": (
            "On all tested toy multipads, the Type S core intersection graph is "
            "connected (one component). mpad=2 Type S is proved connected (v31). "
            "A general connectedness theorem is OPEN — no counterexample found."
        ),
        "proof": [
            "mpad=2: single pair with nonempty intersection (Type S) ⇒ one edge.",
            "Larger mpad: exhaustive toy census, zero disconnected Type S events.",
        ],
        "program": (
            "If proved, Type S is one connected block of through-cliques; "
            "combine with free_core peel and per-root packing."
        ),
    }


def lemma_high_matching() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "high_matching_number_le_n_over_e",
        "statement": (
            "Let H be any set of free-1 highs, and suppose one can choose "
            "representatives U_H ∈ F_H (fully-split free-1 e-sets) that are "
            "pairwise disjoint. Then |H| ≤ ⌊n/e⌋. "
            f"Deployed: ⌊n/e⌋ = {FLOOR_N_OVER_E} ≤ K_max = {K_MAX}. "
            "Thus any first-match / matching transversal of highs fits the "
            "high-tag budget for (κ,ι,δ) side marks."
        ),
        "proof": [
            "The chosen U_H are pairwise disjoint e-subsets of a domain of size n, "
            "so at most ⌊n/e⌋ of them.",
            "Within one high, F_H is already pairwise disjoint (v25); the constraint "
            "is cross-high disjointness of the chosen representatives.",
            f"Deployed ⌊n/e⌋ = {FLOOR_N_OVER_E} ≤ {K_MAX} = ⌊e/⌊n/e⌋⌋.",
        ],
        "deployed": {
            "floor_n_over_e": FLOOR_N_OVER_E,
            "K_max": K_MAX,
            "matching_fits_budget": FLOOR_N_OVER_E <= K_MAX,
        },
        "gap": (
            "|H_A_SP| may exceed the matching number ν(H): many highs can exist "
            "without a large disjoint transversal. Residual first-match must "
            "thin to a matching (or otherwise bound |H|) to close payment."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_connectedness_proof_and_H_thinning",
        "statement": (
            "(1) Prove Type S intersection graphs are always connected "
            "(toys: universal).\n"
            "(2) Control non-Helly Type S (no common I) for M_pad≤16 or ≤2.\n"
            f"(3) Thin H_A_SP to a matching of size ≤⌊n/e⌋={FLOOR_N_OVER_E} "
            f"≤{K_MAX} via first-match, or prove |H_A_SP|≤{K_MAX} outright."
        ),
    }


def max_high_matching(
    highs: list[Any], fam_active: dict[Any, list[frozenset]], n: int, e: int
) -> int:
    """Greedy matching number: max highs with pairwise disjoint rep U's."""
    # Sort highs by smallest available U min for determinism
    order = []
    for h in highs:
        us = fam_active.get(h, [])
        if not us:
            continue
        order.append((min(min(u) for u in us), h, us))
    order.sort()
    used: set[int] = set()
    count = 0
    for _, h, us in order:
        # pick a U disjoint from used if any
        for u in sorted(us, key=lambda x: min(x)):
            if used.isdisjoint(u):
                used |= set(u)
                count += 1
                break
    return count


def toy_suite() -> dict[str, Any]:
    rows = []
    n_type_S = 0
    n_S_connected = 0
    n_S_star = 0
    n_S_nonstar = 0
    n_S_clique_nonhelly = 0
    n_helly_refuted = 0  # rows where nonhelly appears
    max_matching_global = 0

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
        inter_bound = free_core - 1
        vals = domain_vals(p, n)
        floor_ne = n // e
        K1 = e // floor_ne if floor_ne else 0

        # all free-1 families on D for matching
        fam_all: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), e):
            U = frozenset(exps)
            high, c0 = free1_high_c0(U, vals, p)
            fam_all[high].append(U)

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        active_highs: set = set()
        fam_active: dict[Any, list] = defaultdict(list)
        n_ord = 0
        n_S = 0
        n_D = 0
        n_star = 0
        n_nonstar = 0
        n_clique_nonhelly = 0
        n_conn = 0
        max_mpad_S = 1
        max_mpad_nonstar = 1
        all_conn = True
        p1_of: dict[Any, int] = {}

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
                        n_ord += 1
                        pads[(high, c0U, c0V)].append(C)
                        active_highs.add(high)
                        if U not in fam_active[high]:
                            fam_active[high].append(U)
                        poly = monic_rev([vals[i] for i in sorted(U)], p)
                        p1_of[high] = (-poly[1]) % p if len(poly) > 1 else 0

            for _sk, Cs in pads.items():
                cores = [set(t) for t in {tuple(sorted(C)) for C in Cs}]
                if len(cores) < 2:
                    continue
                cnt: Counter = Counter()
                for c in cores:
                    for r in c:
                        cnt[r] += 1
                t = max(cnt.values())
                if t <= 1:
                    n_D += 1
                    continue
                n_S += 1
                n_type_S += 1
                max_mpad_S = max(max_mpad_S, len(cores))

                common = set.intersection(*cores)
                ensure(len(common) <= inter_bound, "I bound")

                # connectedness
                k = len(cores)
                parent = list(range(k))

                def find(x: int) -> int:
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]
                    return x

                def union(a: int, b: int) -> None:
                    ra, rb = find(a), find(b)
                    if ra != rb:
                        parent[ra] = rb

                n_edges = 0
                for i in range(k):
                    for j2 in range(i + 1, k):
                        if cores[i] & cores[j2]:
                            n_edges += 1
                            union(i, j2)
                n_comp = len({find(i) for i in range(k)})
                if n_comp == 1:
                    n_conn += 1
                    n_S_connected += 1
                else:
                    all_conn = False

                # clique?
                pairwise = all(
                    len(cores[i] & cores[j2]) > 0
                    for i in range(k)
                    for j2 in range(i + 1, k)
                )
                if common:
                    n_star += 1
                    n_S_star += 1
                else:
                    n_nonstar += 1
                    n_S_nonstar += 1
                    max_mpad_nonstar = max(max_mpad_nonstar, len(cores))
                    if pairwise:
                        # clique non-Helly: Helly refuted
                        n_clique_nonhelly += 1
                        n_S_clique_nonhelly += 1

                if k == 2:
                    ensure(n_comp == 1 and n_edges == 1, "mpad2")

        if n_clique_nonhelly > 0:
            n_helly_refuted += 1

        if free_core == 1:
            ensure(n_S == 0, "fc1")
        if n_S > 0:
            ensure(all_conn, "all Type S connected on toys")
            ensure(n_conn == n_S, "conn count")

        # high matching number
        highs = list(active_highs)
        # use active U's; fall back to full fam if needed
        fam_use = {
            h: fam_active[h] if fam_active[h] else fam_all[h] for h in highs
        }
        nu = max_high_matching(highs, fam_use, n, e)
        ensure(nu <= floor_ne, f"matching {nu}>{floor_ne}")
        max_matching_global = max(max_matching_global, nu)

        # |H| <= n_ord
        if n_ord > 0:
            ensure(len(highs) <= n_ord, "H<=nord")

        # e=2: p1 injective on active highs
        p1_inj = None
        if e == 2 and highs:
            p1s = [p1_of[h] for h in highs]
            p1_inj = len(p1s) == len(set(p1s))
            ensure(p1_inj, "e2 p1 inj")

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
                "K1": K1,
                "n_type_D": n_D,
                "n_type_S": n_S,
                "n_S_star": n_star,
                "n_S_nonstar": n_nonstar,
                "n_S_clique_nonhelly": n_clique_nonhelly,
                "max_Mpad_S": max_mpad_S,
                "max_Mpad_nonstar": max_mpad_nonstar,
                "all_S_connected": all_conn if n_S > 0 else None,
                "n_active_highs": len(highs),
                "high_matching_nu": nu,
                "nu_le_floor_n_e": nu <= floor_ne,
                "highs_le_K1": (len(highs) <= K1) if K1 else False,
                "nu_le_K1": (nu <= K1) if K1 else True,
                "p1_injective_e2": p1_inj,
                "helly_refuted_on_row": n_clique_nonhelly > 0,
            }
        )

    ensure(n_type_S > 0, "S")
    ensure(n_S_connected == n_type_S, "conn")
    ensure(n_S_nonstar > 0, "nonstar exists")
    ensure(n_S_clique_nonhelly > 0, "Helly refuted")
    ensure(n_helly_refuted > 0, "helly refuted rows")
    ensure(FLOOR_N_OVER_E == 31, "31")
    ensure(FLOOR_N_OVER_E <= K_MAX, "31<=2176")
    ensure(PACK_MAXIMAL_COMMON == 16, "16")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_type_S": n_type_S,
            "n_S_connected": n_S_connected,
            "n_S_star": n_S_star,
            "n_S_nonstar": n_S_nonstar,
            "n_S_clique_nonhelly": n_S_clique_nonhelly,
            "n_rows_helly_refuted": n_helly_refuted,
            "max_matching_nu": max_matching_global,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v32",
        "title": "Type S Helly refuted; connectedness census; high matching ≤⌊n/e⌋",
        "status": "PARTIAL_HELLY_NEG_MATCHING_POS",
        "claims": {
            "banks_type_S_Helly_negative": True,
            "proves_star_maximal_common_packing": True,
            "proves_type_S_connected_general": False,
            "toy_confirms_type_S_always_connected": True,
            "proves_high_matching_le_n_over_e": True,
            "proves_high_matching_fits_Kmax": True,
            "proves_H_A_SP_le_Kmax": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "K_max": K_MAX,
            "matching_le_floor_n_e": True,
            "matching_fits_Kmax": FLOOR_N_OVER_E <= K_MAX,
            "maximal_common_Mpad_bound": PACK_MAXIMAL_COMMON,
            "t_p": T_P,
            "e_p": E_P,
        },
        "lemmas": {
            "helly_neg": lemma_helly_refuted(),
            "star_pack": lemma_star_packing_retained(),
            "connectedness": lemma_connectedness_status(),
            "high_matching": lemma_high_matching(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "type_S": (
                "Helly dead for uniform ≤16; star/maximal-common still ≤16; "
                "connectedness universal on toys — prove it; non-Helly branch open"
            ),
            "highs": (
                f"Matching transversal ν(H)≤⌊n/e⌋={FLOOR_N_OVER_E}≤{K_MAX} fits "
                "budget; need first-match thinning |H|→ν(H) or |H|≤K_max"
            ),
            "next": (
                "Prove Type S connectedness; first-match high thinning to a "
                "matching of size ≤31; non-Helly Type S M_pad bound"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_type_S']} | "
        f"{r['n_S_star']} | {r['n_S_nonstar']} | {r['n_S_clique_nonhelly']} | "
        f"{r['max_Mpad_S']} | {r['max_Mpad_nonstar']} | {r['all_S_connected']} | "
        f"{r['n_active_highs']} | {r['high_matching_nu']} | {r['floor_n_over_e']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v32: Helly refuted; high matching ≤⌊n/e⌋

Status: `PARTIAL` — Type S **Helly REFUTED**; **high matching ≤⌊n/e⌋≤K_max**
PROVED; Type S connectedness universal on toys (proof OPEN).

## Helly REFUTED (BANKED NEGATIVE)

There exist Type S multipads that are intersection **cliques** with **empty**
global common intersection (non-star). Full Helly cannot give uniform M_pad≤16.

## Star / maximal-common retained (PROVED)

```text
I = ⋂ Cores ≠ ∅  →  peel (v30)
|I| = free_core−1  →  M_pad ≤ ⌊A/e⌋ = {d['maximal_common_Mpad_bound']} deployed
```

## Connectedness (TOY UNIVERSAL / PROOF OPEN)

All toy Type S multipads have **one** intersection component. mpad=2 proved
connected. General theorem OPEN.

## High matching (PROVED)

```text
ν(H) := max # highs with pairwise-disjoint representative e-sets
ν(H) ≤ ⌊n/e⌋
```

Deployed:

```text
⌊n/e⌋ = {d['floor_n_over_e']}  ≤  K_max = {d['K_max']}
```

A first-match **matching transversal** of highs fits the (κ,ι,δ) budget.
Gap: `|H_A_SP|` may exceed `ν(H)` — need thinning to a matching.

## Toys

| j | w | free_core | #S | #star | #nonstar | #clique non-Helly | max M_pad S | max nonstar | connected? | #highs | ν(H) | ⌊n/e⌋ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
{tbl}

Census: Type S={cen['n_type_S']} connected={cen['n_S_connected']};
star={cen['n_S_star']}; nonstar={cen['n_S_nonstar']};
clique non-Helly={cen['n_S_clique_nonhelly']} (Helly dead);
max ν={cen['max_matching_nu']}.

## OPEN

1. Prove Type S intersection-connectedness; bound non-Helly Type S M_pad
2. First-match thin `H_A_SP` to a matching of size ≤`{d['floor_n_over_e']}` 
   (≤`{d['K_max']}`)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v32.py --check
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
        "# kb-qatom-route-d-v32\n\n"
        "Type S Helly refuted; high matching ≤⌊n/e⌋ fits K_max.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v32 report\n\nstatus: {cert['status']}\n"
        f"Helly: REFUTED\n"
        f"type S connected toys: UNIVERSAL\n"
        f"high matching ≤ floor n/e = {FLOOR_N_OVER_E} ≤ K_max = {K_MAX}\n"
        f"|H| le Kmax: OPEN (need thinning)\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  Type S Helly: REFUTED (clique non-star multipads exist)")
    print(f"  star/maximal-common packing M_pad≤{PACK_MAXIMAL_COMMON}: retained")
    print("  Type S connectedness: universal on toys (proof OPEN)")
    print(f"  high matching ν(H)≤⌊n/e⌋={FLOOR_N_OVER_E}≤K_max={K_MAX}: PROVED")
    print(
        f"  toys: S={cen['n_type_S']} conn; nonstar={cen['n_S_nonstar']}; "
        f"clique non-Helly={cen['n_S_clique_nonhelly']}; max ν={cen['max_matching_nu']}"
    )


if __name__ == "__main__":
    main()
