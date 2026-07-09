#!/usr/bin/env python3
"""KB-MCA Route-D v31: Type S union structure + A_SP free-1 high census.

Attacks (1) unions of Type S through-sets / Helly-common packing and
(2) # A_SP free-1 highs vs K_max budget.

Proved:
  (1) Global common intersection bound: for a multipad core set Cores,
        |⋂_{C∈Cores} C| ≤ free_core − 1
      (Δ between any pair vanishes on the common intersection and deg≤free_core−1).
  (2) Maximal common packing: if |I| = free_core−1 with I=⋂ Cores, then reduced
      cores are free-1 CS of size m_c−|I|, hence
        M_pad ≤ ⌊(n−2e−|I|)/(m_c−|I|)⌋.
      Deployed: |I|=free_core−1 ⇒ m_c−|I|=e, n−2e−|I|=A=1116048,
        M_pad ≤ ⌊A/e⌋ = 16.
  (3) mpad=2 Type S is connected (single intersection edge) with nonempty pair
      intersection of size ∈[1, free_core−1].
  (4) High counting: # active A_SP free-1 highs ≤ N_side (each active high has
      ≥1 free-1 CS ordered pair, actually ≥2). Fiber-local: # highs in fiber z
      ≤ N_ord(z). Budget (v30): need #highs ≤ K_max=2176 (M_pad1) or ≤1088
      (M_pad2 half-budget).
  (5) Toy bank: Type S intersection graphs always connected (1 component) on all
      tested rows (structural confirmation; general connectedness beyond mpad=2
      not claimed as theorem); Helly/common fraction partial; active highs and
      max highs/fiber vs K-scale recorded (toys often highs ≫ K when e small).

Does NOT prove general Type S connectedness, Type S M_pad≤2 deployed, or
#highs≤2176 deployed.

  python3 experimental/scripts/verify_kb_qatom_route_d_v31.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v31.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v31"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v31.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v31.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v31.report.md"
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
FLOOR_N_OVER_E = N // E
K_MAX = E // FLOOR_N_OVER_E  # 2176
K_MAX_MPAD2 = E // (2 * FLOOR_N_OVER_E)  # 1088
# maximal common |I|=free_core-1 packing
I_MAX = FREE_CORE - 1
M_RED = M_C - I_MAX  # = e
G_RED = N - 2 * E - I_MAX  # = A
PACK_MAXIMAL_COMMON = G_RED // M_RED  # 16


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


def lemma_common_inter_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_global_common_intersection_bound",
        "statement": (
            "For any multipad core set Cores with |Cores|≥2, "
            "|⋂_{C∈Cores} C| ≤ free_core − 1."
        ),
        "proof": [
            "Pick C≠C' in Cores. v27: deg(Λ_C−Λ_{C'}) ≤ free_core−1 and every "
            "common root of C,C' is a root of Δ.",
            "Global common I ⊆ C∩C' ⊆ roots of Δ ⇒ |I| ≤ deg(Δ) ≤ free_core−1 "
            "unless Δ≡0, which would force C=C'.",
        ],
        "deployed_bound": I_MAX,
    }


def lemma_maximal_common_packing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "maximal_common_intersection_packing",
        "statement": (
            "If a multipad core set has global common intersection I with "
            "|I| = free_core − 1, then the reduced cores C\\I are free-1 CS of "
            f"size m_c−|I|, pairwise disjoint on D\\(U∪V∪I), hence "
            f"M_pad ≤ ⌊(n−2e−|I|)/(m_c−|I|)⌋. "
            f"Deployed: |I|=free_core−1 ⇒ m_c−|I|=e={E}, n−2e−|I|=A={A}, "
            f"M_pad ≤ ⌊A/e⌋ = {PACK_MAXIMAL_COMMON}."
        ),
        "proof": [
            "All pairs share I of size free_core−1. For any C≠C', Δ vanishes on I "
            "with deg(Δ)≤ free_core−1 ⇒ Δ = α ∏_{r∈I}(X−r), α≠0.",
            "Hence reduced monics differ by a nonzero constant: free-1 CS of size "
            "m_c−|I| (v23/v25 style).",
            "v25 packing: free-1 family pairwise disjoint; ground set size "
            "n−2e−|I| (avoid U,V and I).",
            "Deployed arithmetic: free_core−1 = j−2w−2 = m_c−w−1, "
            "m_c−(free_core−1) = w+1 = e; n−2e−(free_core−1) = n−e−(j−w−1) "
            "... check: free_core−1 = j−2w−2 = (n−A)−2(t−1)−2 = n−A−2t; "
            "numerically n−2e−(free_core−1) = A.",
        ],
        "deployed": {
            "I_size": I_MAX,
            "m_reduced": M_RED,
            "g_reduced": G_RED,
            "M_pad_bound": PACK_MAXIMAL_COMMON,
            "equals_A_over_e_floor": PACK_MAXIMAL_COMMON == A // E,
        },
    }


def lemma_mpad2_connected() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "mpad_2_type_S_is_connected_edge",
        "statement": (
            "Any Type S multipad with M_pad=2 consists of a single intersecting "
            "pair: the intersection graph is one edge, and 1 ≤ |C∩C'| ≤ free_core−1."
        ),
        "proof": [
            "M_pad=2 ⇒ one pair of cores. Type S ⇒ t≥2 ⇒ they share a root.",
            "v27: |C∩C'| ≤ free_core−1.",
        ],
    }


def lemma_high_count() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "active_high_counting_bounds",
        "statement": (
            "Let H_A_SP be the set of free-1 highs that appear in at least one "
            "A_SP free-1 CS ordered pair. Then |H_A_SP| ≤ N_side ≤ N_ord. "
            "Fiber-local: for each z, |H_A_SP(z)| ≤ N_ord(z). "
            f"Payment needs |H_A_SP| ≤ {K_MAX} (M_pad≤1 path) or ≤ {K_MAX_MPAD2} "
            f"(M_pad≤2 half-budget path) for (κ,ι,δ) to fit e·p."
        ),
        "proof": [
            "Each active high has ≥1 CS ordered pair (actually ≥2: (U,V) and "
            "(V,U) when both directions appear; at least one direction).",
            "Map high ↦ one of its ordered pairs is injective into the set of "
            "side pairs counted by N_side / N_ord.",
            "v30 high-tag budget.",
        ],
        "deployed_targets": {"K_Mpad1": K_MAX, "K_Mpad2": K_MAX_MPAD2},
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_type_S_connected_Helly_and_highs_le_K",
        "statement": (
            "(1) Prove Type S multipads are always intersection-connected "
            "(toys: always 1 component), and/or Helly (common intersection) often "
            "enough to apply maximal-common packing M_pad≤16 deployed.\n"
            f"(2) Prove |H_A_SP| ≤ {K_MAX} (or constructive κ) at deployed scale.\n"
            "Maximal-common case already gives M_pad≤16 (near pack_ceil=17)."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_type_S = 0
    n_S_connected = 0
    n_S_common = 0
    n_S_maximal_common = 0  # |I|==free_core-1 on toy
    n_S_mpad2 = 0
    n_common_bound_ok = 0
    n_maximal_pack_ok = 0

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
        K2 = e // (2 * floor_ne) if floor_ne else 0

        # maximal common pack for this toy row
        if inter_bound >= 0 and m_c > inter_bound:
            pack_max_common = (n - 2 * e - inter_bound) // (m_c - inter_bound)
        else:
            pack_max_common = 0

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        active_highs: set = set()
        n_ord_total = 0
        n_side_keys = 0
        max_H_fib = 0
        n_S = 0
        n_D = 0
        max_mpad_S = 1
        max_comp = 0
        max_common = 0
        all_S_connected = True
        n_common = 0
        n_maximal = 0

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            pads: dict[Any, list] = defaultdict(list)
            Hfib: set = set()
            nord = 0
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
                        nord += 1
                        pads[(high, c0U, c0V)].append(C)
                        Hfib.add(high)
                        active_highs.add(high)

            if Hfib:
                max_H_fib = max(max_H_fib, len(Hfib))
                # highs in fiber ≤ nord
                ensure(len(Hfib) <= nord, "H fib <= nord")
            n_ord_total += nord
            n_side_keys += len(pads)

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

                # global common
                common = set.intersection(*cores)
                max_common = max(max_common, len(common))
                ensure(len(common) <= inter_bound, "common bound")
                n_common_bound_ok += 1
                if common:
                    n_common += 1
                    n_S_common += 1
                if len(common) == inter_bound and inter_bound >= 0:
                    n_maximal += 1
                    n_S_maximal_common += 1
                    # reduced free-1 packing
                    red = [c - common for c in cores]
                    for a, b in itertools.combinations(red, 2):
                        ensure(len(a & b) == 0, "maximal common => red disj")
                    if pack_max_common >= 1:
                        ensure(len(cores) <= pack_max_common, "max common pack")
                        n_maximal_pack_ok += 1

                # intersection graph components
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
                        inter = cores[i] & cores[j2]
                        if inter:
                            n_edges += 1
                            union(i, j2)
                            ensure(len(inter) <= inter_bound, "pair inter")
                n_comp = len({find(i) for i in range(k)})
                max_comp = max(max_comp, max(
                    sum(1 for i in range(k) if find(i) == find(r))
                    for r in range(k)
                ))
                if n_comp == 1:
                    n_S_connected += 1
                else:
                    all_S_connected = False
                if k == 2:
                    n_S_mpad2 += 1
                    ensure(n_comp == 1, "mpad2 connected")
                    ensure(n_edges == 1, "mpad2 one edge")

        # |active highs| ≤ n_ord (actually ≤ n_side unique keys loosely)
        if n_ord_total > 0:
            ensure(len(active_highs) <= n_ord_total, "highs <= nord")

        if free_core == 1:
            ensure(n_S == 0, "fc1 no S")
        if n_S > 0:
            ensure(all_S_connected, "toys S always connected")

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "m_c": m_c,
                "free_core": free_core,
                "inter_bound": inter_bound,
                "pack_maximal_common": pack_max_common,
                "K1": K1,
                "K2": K2,
                "n_type_D": n_D,
                "n_type_S": n_S,
                "max_Mpad_S": max_mpad_S,
                "max_common": max_common,
                "max_comp": max_comp,
                "n_S_with_common": n_common,
                "n_S_maximal_common": n_maximal,
                "n_active_highs": len(active_highs),
                "n_ord": n_ord_total,
                "n_side_keys": n_side_keys,
                "max_highs_per_fiber": max_H_fib,
                "highs_le_K1": (len(active_highs) <= K1) if K1 else False,
                "maxH_le_K1": (max_H_fib <= K1) if K1 else False,
                "all_S_connected": all_S_connected if n_S > 0 else None,
            }
        )

    ensure(n_type_S > 0, "have S")
    ensure(n_S_connected == n_type_S, "all S connected on toys")
    ensure(n_S_mpad2 > 0, "have mpad2")
    ensure(n_common_bound_ok == n_type_S, "common bounds")
    # maximal common may be rare on small toys
    ensure(FREE_CORE == 846161, "fc")
    ensure(PACK_MAXIMAL_COMMON == 16, "pack 16")
    ensure(M_RED == E, "m_red = e")
    ensure(G_RED == A, "g_red = A")
    ensure(K_MAX == 2176, "K")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_type_S": n_type_S,
            "n_S_connected": n_S_connected,
            "n_S_common": n_S_common,
            "n_S_maximal_common": n_S_maximal_common,
            "n_S_mpad2": n_S_mpad2,
            "n_common_bound_ok": n_common_bound_ok,
            "n_maximal_pack_ok": n_maximal_pack_ok,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v31",
        "title": "Type S common-intersection packing + A_SP high census",
        "status": "PARTIAL_UNION_HIGH_CENSUS",
        "claims": {
            "proves_global_common_inter_bound": True,
            "proves_maximal_common_packing_Mpad_le_16_deployed": True,
            "proves_mpad2_connected": True,
            "proves_general_type_S_connected": False,  # toy confirmed only
            "proves_high_counting_bounds": True,
            "proves_highs_le_Kmax_deployed": False,
            "proves_type_S_Mpad_le_2_deployed": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_S_connected_and_high_census": True,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "I_max": I_MAX,
            "m_reduced_at_Imax": M_RED,
            "g_reduced_at_Imax": G_RED,
            "M_pad_bound_maximal_common": PACK_MAXIMAL_COMMON,
            "K_max_Mpad1": K_MAX,
            "K_max_Mpad2": K_MAX_MPAD2,
            "pack_ceil_A_SP": 17,
            "e": E,
            "A": A,
            "t_p": T_P,
            "e_p": E_P,
        },
        "lemmas": {
            "common_bound": lemma_common_inter_bound(),
            "maximal_pack": lemma_maximal_common_packing(),
            "mpad2": lemma_mpad2_connected(),
            "high_count": lemma_high_count(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "type_S": (
                f"Maximal-common Type S ⇒ M_pad≤{PACK_MAXIMAL_COMMON} deployed "
                f"(near pack_ceil=17). Toys: Type S always intersection-connected. "
                "Need Helly/common or connectedness theorem for general Type S."
            ),
            "highs": (
                f"|H_A_SP|≤N_side≤N_ord; need |H_A_SP|≤{K_MAX} for side marks"
            ),
            "next": (
                "Prove Type S intersection-connected + Helly/common root when "
                "possible; bound |H_A_SP| via first-match high witnesses"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_type_S']} | "
        f"{r['max_Mpad_S']} | {r['max_common']} | {r['n_S_with_common']} | "
        f"{r['n_S_maximal_common']} | {r['all_S_connected']} | "
        f"{r['n_active_highs']} | {r['max_highs_per_fiber']} | {r['K1']} | "
        f"{r['highs_le_K1']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v31: Type S common packing + high census

Status: `PARTIAL` — maximal-common Type S packing **M_pad≤16** deployed PROVED;
Type S always connected on toys; highs≤K_max still **OPEN**.

## Global common intersection (PROVED)

```text
|⋂_{{C ∈ Cores}} C|  ≤  free_core − 1
```

## Maximal-common packing (PROVED)

If the multipad achieves `|I| = free_core − 1`:

```text
reduced cores are free-1 CS of size m_c − |I|
M_pad  ≤  ⌊(n − 2e − |I|) / (m_c − |I|)⌋
```

### Deployed arithmetic

```text
|I| = free_core − 1 = {d['I_max']}
m_c − |I| = e = {d['e']}
n − 2e − |I| = A = {d['A']}
M_pad ≤ ⌊A/e⌋ = {d['M_pad_bound_maximal_common']}
```

Note: `{d['M_pad_bound_maximal_common']}` is one below `pack_ceil = {d['pack_ceil_A_SP']}`
used in A_SP cost `|A_SP| ≤ 17·P_multi`.

## mpad=2 Type S (PROVED)

Single intersecting pair; `1 ≤ |C∩C'| ≤ free_core−1`.

## High counting (PROVED)

```text
|H_A_SP|  ≤  N_side  ≤  N_ord
|H_A_SP(z)|  ≤  N_ord(z)
```

Targets: `|H_A_SP| ≤ {d['K_max_Mpad1']}` (M_pad1) or ≤ `{d['K_max_Mpad2']}` (M_pad2 half).

## Toys

| j | w | free_core | #S | max M_pad S | max |I| | #S with I≠∅ | #S maximal I | connected? | #highs | max H/fib | K1 | highs≤K1? |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|
{tbl}

Census: Type S={cen['n_type_S']} all connected={cen['n_S_connected']};
with common={cen['n_S_common']}; maximal common={cen['n_S_maximal_common']};
mpad2={cen['n_S_mpad2']}.

## OPEN

1. Type S always intersection-connected (toys yes) + Helly/common often enough
   for M_pad≤16; or better union bound ⇒ M_pad≤2
2. `|H_A_SP| ≤ {d['K_max_Mpad1']}` at deployed scale

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v31.py --check
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
        "# kb-qatom-route-d-v31\n\n"
        "Type S common-intersection packing + A_SP high census.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v31 report\n\nstatus: {cert['status']}\n"
        f"maximal common M_pad bound deployed: {PACK_MAXIMAL_COMMON}\n"
        f"type S connected (toys): CONFIRMED\n"
        f"highs le Kmax: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  global common |I| ≤ free_core−1: PROVED")
    print(f"  maximal common ⇒ M_pad ≤ ⌊A/e⌋ = {PACK_MAXIMAL_COMMON} deployed: PROVED")
    print("  mpad=2 Type S connected edge: PROVED")
    print(f"  |H_A_SP| ≤ N_side ≤ N_ord: PROVED (need ≤{K_MAX} for payment)")
    print(
        f"  toys: Type S={cen['n_type_S']} all connected; "
        f"common={cen['n_S_common']}; maximal I={cen['n_S_maximal_common']}"
    )


if __name__ == "__main__":
    main()
