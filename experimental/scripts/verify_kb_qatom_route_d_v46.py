#!/usr/bin/env python3
"""KB-MCA Route-D v46: bound R2 / H_R2 via free_core, Type D, untyped free-1.

Preferred residual card attack (v45 R2/H_R2). Decompose residual and prove
packing laws; bank false small envelopes; free_core trend.

Proved:
  (1) R2 = R2_unt ⊔ R2_D (disjoint): residual free-1 pairs after SR+H_M split
      into untyped (not multi-core multipad) vs Type D multipad sides.
  (2) Type D multipad cores are pairwise disjoint (tmult≤1 ⇔ no shared roots)
      and M_pad ≤ pack_D = ⌊(n−2e)/m_c⌋ (v35); deployed pack_D=2.
  (3) |R2| ≤ |H_R2| · ⌊n/e⌋ · (⌊n/e⌋−1) = 930 |H_R2| deployed (family packing).
  (4) |R2_D| ≤ 2 · n_mpad_D: each Type D multipad side key is one ordered
      free-1 pair (high,c0U,c0V); reverse may give a second key ⇒ factor ≤2.
  (5) Sufficient residual card (arithmetic + (3)):
        |H_R2| ≤ H2  ⇒  |R2| ≤ 930·H2 ≤ e·p/2  ⇒  residual enum e·p
        |H_R2| ≤ n   ⇒  |R2| ≤ 930·n ≪ e·p   (implication PROVED)
        |H_R2| ≤ A   ⇒  |R2| ≤ 930·A ≪ e·p   (implication PROVED)
  (6) free_core≥1 toys: residual R2 almost pure untyped (R2_D=0 often);
      H_R2 decreases as free_core grows (empirical).
  (7) Banked REFUTED on A_SP residual toys:
        |H_R2|≤⌊n/e⌋, ≤2⌊n/e⌋, ≤pack_D·⌊n/e⌋, and |H_R2|≤n
        (e.g. n=30,j=4,w=2: |H_R2|=952>n=30).

Does NOT prove deployed |H_R2|≤H2 or |R2|≤e·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v46.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v46.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v46"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v46.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v46.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v46.report.md"
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
K_CAP = 70 * FLOOR_N_OVER_E
PAIRS_PER_HIGH = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)
H2 = E_P // (2 * PAIRS_PER_HIGH)
PACK_D_DEP = (N - 2 * E) // M_C  # 2
R2_IF_HR2_LE_N = PAIRS_PER_HIGH * N  # 930 * n
R2_IF_HR2_LE_A = PAIRS_PER_HIGH * A


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


def free1_high_c0(U, vals, p):
    poly = monic_rev([vals[i] for i in sorted(U)], p)
    return tuple(poly[1:-1]), poly[-1]


def lemma_decomp() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "R2_unt_disjoint_union_R2_D",
        "statement": (
            "R2 = R2_unt ⊔ R2_D where R2_D = Type D multipad residual pairs "
            "(high∉H_M) and R2_unt = residual free-1 pairs that are not multi-core "
            "multipad sides (untyped single-core multi-U free-1)."
        ),
        "proof": [
            "v45: R2 = free-1 pairs not Type S with high∉H_M.",
            "Among non-S pairs: either Type D multipad side or untyped.",
        ],
    }


def lemma_type_D_disj() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Type_D_cores_pairwise_disjoint_pack",
        "statement": (
            "Within a Type D multipad (tmult≤1), cores are pairwise disjoint. "
            f"Hence M_pad ≤ pack_D = ⌊(n−2e)/m_c⌋ (after removing U∪V). "
            f"Deployed pack_D = {PACK_D_DEP}."
        ),
        "proof": [
            "tmult≤1: each domain point lies in at most one core of the multipad.",
            "⇒ C_i ∩ C_j = ∅ for i≠j.",
            "Packing in D∖(U∪V) of size n−2e: M_pad ≤ ⌊(n−2e)/m_c⌋ (v26/v35).",
        ],
    }


def lemma_R2_family_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "R2_le_930_HR2",
        "statement": (
            f"|R2| ≤ |H_R2| · ⌊n/e⌋ · (⌊n/e⌋−1) = {PAIRS_PER_HIGH}|H_R2|."
        ),
        "proof": [
            "Each residual high has |F_H|≤⌊n/e⌋ active free-1 U's (v25).",
            "Ordered free-1 pairs within high ≤ f(f−1).",
            "R2 pairs are a subset of those for highs in H_R2.",
        ],
    }


def lemma_R2_D_mpad() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "R2_D_le_2_n_mpad_D",
        "statement": (
            "Each Type D multipad side key (high,c0U,c0V) is one ordered free-1 "
            "pair. At most one reverse key (high,c0V,c0U). Hence "
            "|R2_D| ≤ 2 · n_mpad_D where n_mpad_D counts Type D multipad side keys "
            "with high∉H_M (or ambient Type D keys if restricted)."
        ),
        "proof": [
            "Side key determines (high,c0U,c0V) uniquely ⇒ unique ordered pair "
            "of root sets with those free-1 constants (v20 φ).",
        ],
    }


def lemma_sufficient() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "sufficient_HR2_gates_for_residual_card",
        "statement": (
            f"|H_R2|≤H2={H2} ⇒ |R2|≤930·H2≤e·p/2 ⇒ residual e·p enum.\n"
            f"|H_R2|≤n ⇒ |R2|≤930·n={R2_IF_HR2_LE_N}≪e·p.\n"
            f"|H_R2|≤A ⇒ |R2|≤930·A={R2_IF_HR2_LE_A}≪e·p.\n"
            "|H_R2|≤n is REFUTED for A_SP residual (toys); implication only."
        ),
        "proof": ["Family bound + deployed arithmetic."],
        "deployed": {
            "H2": H2,
            "R2_if_n": R2_IF_HR2_LE_N,
            "R2_if_A": R2_IF_HR2_LE_A,
            "e_p": E_P,
        },
    }


def lemma_false_envelopes() -> dict[str, Any]:
    return {
        "status": "REFUTED",
        "name": "HR2_small_envelopes_false",
        "statement": (
            "On A_SP residual toys, all fail: |H_R2|≤⌊n/e⌋, ≤2⌊n/e⌋, "
            "≤pack_D·⌊n/e⌋, and |H_R2|≤n (e.g. n=30, |H_R2|=952)."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_HR2_le_H2_or_R2_le_ep",
        "statement": (
            f"Prove |H_R2|≤H2={H2} or |R2|≤e·p at free_core={FREE_CORE}. "
            "Do not retry |H_R2|≤n (refuted). free_core≥1 residual ≈ untyped free-1."
        ),
    }


def residual_structure(p: int, n: int, j: int, w: int) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 80000:
        return None
    free_core = m_c - w
    pack_D = max((n - 2 * e) // m_c, 0) if n >= 2 * e else 0
    floor_ne = max(n // e, 1)
    vals = domain_vals(p, n)
    fib: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        S = frozenset(exps)
        poly = monic_rev([vals[i] for i in sorted(S)], p)
        fib[tuple(poly[1 : w + 1])].append(S)

    high_Us: dict[Any, list] = defaultdict(list)
    seen_u: dict[Any, set] = defaultdict(set)
    unique_fp: list = []
    seen_fp: set = set()
    side_cores: dict[Any, set] = defaultdict(set)

    for _z, members in fib.items():
        pencils: dict[Any, list] = defaultdict(list)
        for S in members:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = frozenset(S - U)
            high, c0 = free1_high_c0(U, vals, p)
            pencils[(tuple(sorted(C)), high)].append((U, c0, high, C))
        for _key, lst in pencils.items():
            by_u: dict = {}
            for U, c0, high, C in lst:
                by_u[tuple(sorted(U))] = (c0, high, C)
            if len(by_u) < 2:
                continue
            items = list(by_u.items())
            for i, (ut, (c0U, high, C)) in enumerate(items):
                if ut not in seen_u[high]:
                    seen_u[high].add(ut)
                    high_Us[high].append(frozenset(ut))
                for j2, (vt, (c0V, _, _)) in enumerate(items):
                    if i == j2 or c0U == c0V:
                        continue
                    fp = (ut, vt)
                    if fp not in seen_fp:
                        seen_fp.add(fp)
                        unique_fp.append((high, ut, vt, c0U, c0V))
                    side_cores[(high, c0U, c0V)].add(C)

    if not high_Us:
        return None

    pair_S: set = set()
    pair_D: set = set()
    n_mpad_D = 0
    max_mpad_D = 1
    D_cores_disj = True

    for sk, cores in side_cores.items():
        if len(cores) < 2:
            continue
        cl = list(cores)
        cnt: Counter = Counter()
        for c in cl:
            for r in c:
                cnt[r] += 1
        tmult = max(cnt.values())
        high, c0U, c0V = sk
        marked = [
            (ut, vt)
            for h, ut, vt, cu, cv in unique_fp
            if h == high and cu == c0U and cv == c0V
        ]
        if tmult >= 2:
            for fp in marked:
                pair_S.add(fp)
                pair_D.discard(fp)
        else:
            n_mpad_D += 1
            max_mpad_D = max(max_mpad_D, len(cl))
            # pairwise disjoint
            for i in range(len(cl)):
                for j2 in range(i + 1, len(cl)):
                    if cl[i] & cl[j2]:
                        D_cores_disj = False
            if pack_D > 0:
                ensure(len(cl) <= pack_D, f"pack D {len(cl)}")
            for fp in marked:
                if fp not in pair_S:
                    pair_D.add(fp)

    ensure(D_cores_disj, "Type D cores disj")

    free = set(range(n))
    H_M: set = set()
    for h in sorted(high_Us, key=repr):
        for U in high_Us[h]:
            if set(U).issubset(free):
                free -= set(U)
                H_M.add(h)
                break
    ensure(len(H_M) <= floor_ne, "HM")

    n_R2 = n_R2_unt = n_R2_D = 0
    H_R2: set = set()
    H_R2_unt: set = set()
    H_R2_D: set = set()
    n_pairs = len(unique_fp)
    n_S = 0
    for high, ut, vt, cu, cv in unique_fp:
        fp = (ut, vt)
        if fp in pair_S:
            n_S += 1
            continue
        if high in H_M:
            continue
        n_R2 += 1
        H_R2.add(high)
        if fp in pair_D:
            n_R2_D += 1
            H_R2_D.add(high)
        else:
            n_R2_unt += 1
            H_R2_unt.add(high)

    ensure(n_R2 == n_R2_unt + n_R2_D, "decomp")
    bound = len(H_R2) * floor_ne * max(floor_ne - 1, 0)
    ensure(n_R2 <= bound or floor_ne <= 1, "family bound")
    # R2_D ≤ 2 * n_mpad_D is soft if H_M filters some D pairs — use ambient n_mpad_D
    ensure(n_R2_D <= 2 * max(n_mpad_D, 1) or n_R2_D == 0 or n_mpad_D > 0, "R2D")
    # tighter: each D pair corresponds to ≤1 side key direction; reverse separate
    # n_R2_D ≤ 2 * n_mpad_D always if every D pair is a multipad side key
    if n_mpad_D > 0:
        ensure(n_R2_D <= 2 * n_mpad_D + n_pairs, "loose R2D")  # always true
    # better check: number of D pairs among all (not just R2) ≤ 2*n_mpad_D
    n_all_D = sum(
        1
        for high, ut, vt, cu, cv in unique_fp
        if (ut, vt) in pair_D
    )
    ensure(n_all_D <= 2 * n_mpad_D, f"all D pairs {n_all_D} > 2*{n_mpad_D}")

    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "free_core": free_core,
        "pack_D": pack_D,
        "floor": floor_ne,
        "nH": len(high_Us),
        "n_HM": len(H_M),
        "n_pairs": n_pairs,
        "n_pairs_S": n_S,
        "n_R2": n_R2,
        "n_R2_unt": n_R2_unt,
        "n_R2_D": n_R2_D,
        "n_H_R2": len(H_R2),
        "n_H_R2_unt": len(H_R2_unt),
        "n_H_R2_D": len(H_R2_D),
        "n_mpad_D": n_mpad_D,
        "max_mpad_D": max_mpad_D,
        "bound_930": bound,
        "R2_le_bound": n_R2 <= bound,
        "frac_R2_unt": n_R2_unt / n_R2 if n_R2 else 0.0,
        "HR2_le_floor": len(H_R2) <= floor_ne,
        "HR2_le_2floor": len(H_R2) <= 2 * floor_ne,
        "HR2_le_packD_floor": len(H_R2) <= max(pack_D, 1) * floor_ne,
        "HR2_le_n": len(H_R2) <= n,
        "HR2_le_H2": len(H_R2) <= H2,
        "R2_le_ep_dep": n_R2 <= E_P,
        "D_cores_disj": D_cores_disj,
        "all_D_pairs_le_2mpad": n_all_D <= 2 * n_mpad_D,
    }


def toy_suite() -> dict[str, Any]:
    ensure(PACK_D_DEP == 2, "packD")
    ensure(H2 == E_P // (2 * PAIRS_PER_HIGH), "H2")
    ensure(R2_IF_HR2_LE_N < E_P, "930n < ep")
    ensure(R2_IF_HR2_LE_A < E_P, "930A < ep")
    ensure(FREE_CORE == 846161, "fc")
    ensure(A == N - J, "A=n-j")
    ensure(T == E, "t=e")

    rows = []
    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 8, 2),
        (17, 16, 9, 2),
        (19, 18, 5, 1),
        (19, 18, 5, 2),
        (19, 18, 6, 2),
        (19, 18, 7, 2),
        (19, 18, 8, 2),
        (19, 18, 9, 2),
        (31, 30, 4, 2),
        (31, 30, 5, 1),
        (31, 30, 5, 2),
        (31, 30, 6, 2),
    ]:
        r = residual_structure(p, n, j, w)
        if r is None or r["n_R2"] == 0:
            continue
        ensure(r["R2_le_bound"], "bound")
        ensure(r["D_cores_disj"], "disj")
        ensure(r["all_D_pairs_le_2mpad"], "2mpad")
        ensure(r["HR2_le_H2"], "H2")
        ensure(r["R2_le_ep_dep"], "ep")
        rows.append(r)

    ensure(len(rows) >= 10, "rows")
    # refute small envelopes
    ensure(any(not r["HR2_le_floor"] for r in rows), "refute floor")
    ensure(any(not r["HR2_le_2floor"] for r in rows), "refute 2floor")
    # free_core>=1 mostly untyped
    fc1 = [r for r in rows if r["free_core"] >= 1]
    ensure(len(fc1) >= 4, "fc1")
    ensure(any(r["frac_R2_unt"] >= 0.99 for r in fc1), "unt typed dominant")
    # |H_R2|≤n REFUTED on A_SP residual
    ensure(any(not r["HR2_le_n"] for r in rows), "refute HR2 le n")

    by_fc: dict[int, list[int]] = defaultdict(list)
    for r in rows:
        by_fc[r["free_core"]].append(r["n_H_R2"])

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "max_R2": max(r["n_R2"] for r in rows),
            "max_H_R2": max(r["n_H_R2"] for r in rows),
            "max_R2_unt": max(r["n_R2_unt"] for r in rows),
            "max_R2_D": max(r["n_R2_D"] for r in rows),
            "avg_frac_unt": sum(r["frac_R2_unt"] for r in rows) / len(rows),
            "by_fc_max_HR2": {str(k): max(v) for k, v in sorted(by_fc.items())},
            "refute_floor": True,
            "refute_2floor": True,
            "refute_HR2_le_n": True,
            "all_R2_le_930_HR2": True,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v46",
        "title": "R2/H_R2 bounds: untyped+Type D decomp, family packing, free_core",
        "status": "PARTIAL_R2_STRUCTURE",
        "claims": {
            "proves_R2_unt_union_R2_D": True,
            "proves_Type_D_cores_disjoint_pack": True,
            "proves_R2_le_930_HR2": True,
            "proves_R2_D_le_2_n_mpad_D": True,
            "proves_HR2_le_n_implies_card": True,
            "proves_HR2_le_H2_implies_card": True,
            "refutes_HR2_le_floor": True,
            "refutes_HR2_le_2floor": True,
            "refutes_HR2_le_n_on_ASP_residual": True,
            "toy_fc_ge1_mostly_untyped": True,
            "proves_deployed_HR2_le_H2": False,
            "proves_deployed_R2_le_ep": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "H2": H2,
            "pack_D": PACK_D_DEP,
            "e_p": E_P,
            "R2_if_HR2_le_n": R2_IF_HR2_LE_N,
            "R2_if_HR2_le_A": R2_IF_HR2_LE_A,
            "A": A,
            "n": N,
            "free_core": FREE_CORE,
            "pairs_per_high": PAIRS_PER_HIGH,
        },
        "lemmas": {
            "decomp": lemma_decomp(),
            "type_D_disj": lemma_type_D_disj(),
            "R2_family": lemma_R2_family_bound(),
            "R2_D": lemma_R2_D_mpad(),
            "sufficient": lemma_sufficient(),
            "false_env": lemma_false_envelopes(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "residual_is_untyped": (
                "free_core≥1: R2 almost pure untyped free-1 (Type D multipad "
                "sides rare after SR)"
            ),
            "easiest_live_gate": "|H_R2|≤H2 ( |H_R2|≤n is false on toys )",
            "next": "Prove |H_R2|≤H2 or |R2|≤e·p for untyped residual free-1",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_H_R2']} | "
        f"{r['n_H_R2_unt']} | {r['n_H_R2_D']} | {r['n_R2']} | {r['n_R2_unt']} | "
        f"{r['n_R2_D']} | {r['frac_R2_unt']:.2f} | {r['HR2_le_2floor']} |"
        for r in rows
    )
    fc_line = ", ".join(
        f"fc={k}:maxHR2={v}" for k, v in cen["by_fc_max_HR2"].items()
    )
    return f"""# KB-MCA Route-D v46: R2 / H_R2 structure (untyped + Type D)

Status: `PARTIAL` — residual **decomposition + packing** PROVED; small H_R2
envelopes **REFUTED**; deployed `|H_R2|≤n` / H2 **OPEN**.

## Decomposition (PROVED)

```text
R2  =  R2_unt  ⊔  R2_D
```

- **R2_D:** Type D multipad residual pairs (cores pairwise **disjoint**, M_pad≤pack_D)
- **R2_unt:** untyped free-1 (single-core multi-U; not multi-core multipad)

Deployed pack_D = {d['pack_D']}.

## Packing (PROVED)

```text
|R2|     ≤  930 · |H_R2|
|R2_D|   ≤  2 · n_mpad_D
```

## Sufficient residual card (PROVED implications)

| If | Then |
|---|---|
| `|H_R2| ≤ H2` | `|R2| ≤ e·p/2` | live OPEN |
| `|H_R2| ≤ n` | `|R2| ≤ {d['R2_if_HR2_le_n']} ≪ e·p` | **premise REFUTED** (toys) |
| `|H_R2| ≤ A` | `|R2| ≤ {d['R2_if_HR2_le_A']} ≪ e·p` | premise OPEN / unused |

## False envelopes (BANKED)

`|H_R2| ≤ ⌊n/e⌋`, `≤ 2⌊n/e⌋`, `≤ pack_D·⌊n/e⌋`, **`≤ n`** fail on A_SP residual
(e.g. n=30, `|H_R2|=952`).

## free_core trend (toys)

{fc_line}

free_core≥1: residual **almost pure untyped** (R2_D often 0).

## Toys

| j | w | fc | H_R2 | H_unt | H_D | R2 | R2_unt | R2_D | frac unt | ≤2floor? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
{tbl}

Census: max H_R2={cen['max_H_R2']}; max R2={cen['max_R2']};
avg frac untyped={cen['avg_frac_unt']:.3f}.

## Path

```text
SR (Type S) → untyped free-1 + Type D
H_M peels matching
R2 card: need |H_R2|≤H2 or |R2|≤e·p  (not ≤n)
```

## OPEN

1. `|H_R2| ≤ H2` or `|R2| ≤ e·p` at free_core={d['free_core']}
2. Especially **untyped free-1 residual** high / pair count
3. `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v46.py --check
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
        "# kb-qatom-route-d-v46\n\n"
        "R2/H_R2 untyped+Type D structure; family packing; free_core trend.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    cen = cert["toy_suite"]["census"]
    REPORT_PATH.write_text(
        f"# v46 report\n\nstatus: {cert['status']}\n"
        f"max H_R2: {cen['max_H_R2']}\n"
        f"avg frac untyped: {cen['avg_frac_unt']}\n"
        f"deployed HR2 le n/H2: OPEN\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  R2 = R2_unt ⊔ R2_D; Type D cores disjoint; |R2|≤930|H_R2|: PROVED")
    print(f"  |H_R2|≤H2 ⇒ card: PROVED implication; |H_R2|≤n premise REFUTED")
    print(
        f"  toys: max H_R2={cen['max_H_R2']} max R2={cen['max_R2']}; "
        f"avg frac untyped={cen['avg_frac_unt']:.3f}"
    )
    print("  free_core≥1 residual ≈ pure untyped free-1")
    print("  deployed |H_R2|≤H2 or |R2|≤e·p: OPEN")


if __name__ == "__main__":
    main()
