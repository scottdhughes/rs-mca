#!/usr/bin/env python3
"""KB-MCA Route-D v41: overflow when ambient |H| ≫ K_cap.

Closes the post-v40 pressure point: H_core is paid, but unmatched highs /
overflow pairs need a payment path when |H| > K_cap = 2170.

Proved:
  (1) e·p budget for multi-tier side marks (κ,ι,δ)=(τ,local,ι,δ):
        R · ⌊n/e⌋ · ⌊n/e⌋ ≤ e  ⇒  R ≤ R_max = 70
        |H| · ⌊n/e⌋ ≤ e        ⇒  |H| ≤ K_MAX = 2176
      Deployed: R_max·31·31 = 67270 ≤ e=67472 (slack 202). PROVED arithmetic.
      Explains why R_max=70 / K_cap=2170 are tight for a *single* e·p side cell
      with within-family ι — not an arbitrary ledger choice.
  (2) Pigeonhole overflow size: any R_max-tier matching leaves
        |H_over| ≥ max(0, |H| − K_cap)
      and honest multi-tier can achieve |H_over| = max(0, |H|−K_cap) when a
      packing of that size exists (Hall). PROVED.
  (3) Overflow pair count: N_over ≤ |H_over| · ⌊n/e⌋ · (⌊n/e⌋−1)
      (same as N_side, v36). PROVED.
  (4) μ_over enum (v39) injects overflow pairs; lands in [e]×F_p iff
        N_over ≤ e·p
      Under worst |F_H|=⌊n/e⌋: equivalent to
        |H_over| ≤ ⌊e·p / (⌊n/e⌋(⌊n/e⌋−1))⌋ = H_OVER_ENUM_MAX ≈ 1.546e11.
      PROVED conditional gate.
  (5) Single e·p cannot host Λ≥2 full multi-tier layers with ι:
        Λ · 67270 ≤ e ⇒ Λ = 1 only. PROVED arithmetic.
  (6) TARGET multi-cell capacity (arithmetic, strategy OPEN as proof goal):
        ⌊TARGET / (e·p)⌋ = 1911 e·p-cells fit in residual TARGET.
        Layered multi-tier ⇒ |H| ≤ 1911 · K_cap = 4_146_870 highs
        payable against TARGET (not against the single A_SP≤t·p goal).
  (7) Hybrid two-cell sketch (structure PROVED, A_SP≤t·p NOT):
        cell1 = core (κ,ι,δ) on H_core; cell2 = μ_over on overflow if N_over≤e·p.
        Total side cost 2·e·p when both land — exceeds single t·p unless one cell
        is charged outside A_SP.
  (8) Toy bank: local overflow marks (c0U,δ), (c0U,c0V), (minU mod e, δ), …
      collide (NEGATIVE); μ_over injects; pigeon |H_over|≥|H|−cap when
      R forced small; e·p arithmetic identities.

Does NOT prove ambient |H|≤K_cap, N_over≤e·p at deployed scale, or A_SP≤t·p.
Does NOT reopen ambient L≤70 (v40 refuted).

  python3 experimental/scripts/verify_kb_qatom_route_d_v41.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v41.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v41"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v41.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v41.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v41.report.md"
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
TARGET = 274_836_936_291_722_953
FLOOR_N_OVER_E = N // E  # 31
K_MAX = E // FLOOR_N_OVER_E  # 2176
R_MAX = K_MAX // FLOOR_N_OVER_E  # 70
K_CAP = R_MAX * FLOOR_N_OVER_E  # 2170
# (τ,local,ι) radix product
SIDE_RADIX = R_MAX * FLOOR_N_OVER_E * FLOOR_N_OVER_E  # 67270
SIDE_SLACK = E - SIDE_RADIX  # 202
PAIRS_PER_HIGH_MAX = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)  # 930
N_CORE_PAIRS_MAX = K_CAP * PAIRS_PER_HIGH_MAX  # 2018100
H_OVER_ENUM_MAX = E_P // PAIRS_PER_HIGH_MAX  # under worst fam size
TARGET_EP_CELLS = TARGET // E_P  # 1911
TARGET_H_LAYERS = TARGET_EP_CELLS * K_CAP  # 4146870


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


def lemma_ep_budget() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "single_ep_side_mark_budget",
        "statement": (
            "Side mark (τ, local, ι, δ) with τ<R, local<⌊n/e⌋, ι<⌊n/e⌋, δ∈F_p "
            f"injects into [e]×F_p (via mixed radix on first three coords) iff "
            f"R·⌊n/e⌋·⌊n/e⌋ ≤ e. Deployed: R_max={R_MAX} gives "
            f"{SIDE_RADIX} ≤ e={E} (slack {SIDE_SLACK}). Hence a single e·p cell "
            f"supports at most R_max={R_MAX} tiers and |H|≤K_cap={K_CAP} "
            f"(or |H|≤K_MAX={K_MAX} if local slots are fully used without the "
            "R·floor packing gap)."
        ),
        "proof": [
            "Encode k = (τ·⌊n/e⌋ + local)·⌊n/e⌋ + ι ∈ [0, R·floor²).",
            "Need k < e to pair with δ∈F_p as (k mod e is free if k<e; or (k,δ)).",
            f"R=70: 70·31·31={SIDE_RADIX}≤{E}. R=71: 71·31·31={71*31*31}>e.",
            "This is why R_max=70 is forced for one e·p side cell with ι.",
        ],
        "deployed": {
            "R_max": R_MAX,
            "side_radix": SIDE_RADIX,
            "e": E,
            "slack": SIDE_SLACK,
            "K_cap": K_CAP,
        },
    }


def lemma_pigeon_over() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "pigeonhole_overflow_size",
        "statement": (
            f"Any matching schedule with capacity K_cap={K_CAP} (R_max tiers × "
            f"≤⌊n/e⌋ highs/tier) leaves at least max(0, |H|−K_cap) highs unmatched. "
            "When a packing of size min(|H|,K_cap) exists, multi-tier can achieve "
            "equality |H_over|=max(0,|H|−K_cap)."
        ),
        "proof": [
            "Capacity of R_max tiers ≤ R_max·⌊n/e⌋ = K_cap matched highs.",
            "Pigeonhole: unmatched ≥ |H| − capacity.",
        ],
    }


def lemma_N_over() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "overflow_pair_count",
        "statement": (
            "N_over ≤ |H_over| · ⌊n/e⌋ · (⌊n/e⌋−1) "
            f"(≤ 930 |H_over| deployed). Hence N_over ≤ e·p whenever "
            f"|H_over| ≤ H_OVER_ENUM_MAX = {H_OVER_ENUM_MAX}."
        ),
        "proof": [
            "Per high: ≤⌊n/e⌋ active U's (v25); ordered free-1 CS pairs ≤ f(f−1).",
            f"e·p / 930 = {H_OVER_ENUM_MAX}.",
        ],
        "deployed": {
            "H_OVER_ENUM_MAX": H_OVER_ENUM_MAX,
            "N_core_pairs_max": N_CORE_PAIRS_MAX,
            "e_p": E_P,
        },
    }


def lemma_mu_over() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "mu_over_enum_conditional_ep",
        "statement": (
            "Order overflow pairs lex; rank i; μ_over=(i mod e, ⌊i/e⌋) injective. "
            "If N_over ≤ e·p then μ_over lands in [e]×F_p (v39)."
        ),
        "proof": ["v39 mixed-radix rank."],
    }


def lemma_no_multilayer_one_ep() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "no_second_multitier_layer_in_one_ep",
        "statement": (
            f"Λ full multi-tier layers each using radix {SIDE_RADIX} need "
            f"Λ·{SIDE_RADIX} ≤ e to share one e·p cell with ι. Only Λ=1 works "
            f"({SIDE_RADIX}≤e < 2·{SIDE_RADIX})."
        ),
        "proof": [f"2·{SIDE_RADIX}={2*SIDE_RADIX} > e={E}."],
    }


def lemma_target_layers() -> dict[str, Any]:
    return {
        "status": "PROVED_ARITHMETIC",
        "name": "TARGET_multicell_capacity",
        "statement": (
            f"⌊TARGET/(e·p)⌋ = {TARGET_EP_CELLS}. If each e·p-cell pays one "
            f"multi-tier layer of ≤K_cap highs, then ≤{TARGET_H_LAYERS} highs "
            "are payable against residual TARGET. This is NOT a proof that A_SP "
            "may use TARGET multi-cells (A_SP≤t·p is the single-cell goal); it "
            "bounds how far layered multi-tier can go if charged to TARGET."
        ),
        "deployed": {
            "TARGET": TARGET,
            "e_p": E_P,
            "cells": TARGET_EP_CELLS,
            "max_H_layered": TARGET_H_LAYERS,
        },
    }


def lemma_local_marks_negative() -> dict[str, Any]:
    return {
        "status": "BANKED_NEGATIVE",
        "name": "local_overflow_marks_collide",
        "statement": (
            "Natural local overflow marks (c0U,δ), (c0U,c0V), (minU mod e, δ), "
            "(minU, c0U), (sumU mod e, δ) fail injectivity on overflow pairs in "
            "toys. No local e·p replacement for μ_over found."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_overflow_deployed",
        "statement": (
            "(1) Prove N_over ≤ e·p (or |H_over|≤H_OVER_ENUM_MAX) at deployed A_SP, "
            "or ambient |H|≤K_cap so H_over=∅.\n"
            "(2) Or accept hybrid/TARGET multi-cell accounting outside single A_SP≤t·p.\n"
            "(3) Or find a local overflow mark of size e·p (toys negative so far)."
        ),
    }


def multitier_fm(
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
        if not claimed:
            break
    return tags


def mark_inj(pairs: list, mark_fn) -> bool:
    buckets: dict[Any, list] = defaultdict(list)
    seen: set = set()
    for t in pairs:
        fp = (t[1], t[2])
        if fp in seen:
            continue
        seen.add(fp)
        buckets[mark_fn(t)].append(fp)
    if not seen:
        return True
    return all(len(set(v)) == 1 for v in buckets.values()) and len(buckets) == len(
        seen
    )


def unique_pairs(pairs: list) -> list:
    seen: set = set()
    out = []
    for t in pairs:
        fp = (t[1], t[2])
        if fp in seen:
            continue
        seen.add(fp)
        out.append(t)
    return out


def asp_data(p: int, n: int, j: int, w: int):
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 35000:
        return None
    free_core = m_c - w
    vals = domain_vals(p, n)
    fib: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        S = frozenset(exps)
        poly = monic_rev([vals[i] for i in sorted(S)], p)
        fib[tuple(poly[1 : w + 1])].append(S)
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
        for _key, lst in pencils.items():
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
                    ut, vt = tuple(sorted(U)), tuple(sorted(V))
                    pairs.append((high, ut, vt, c0U, c0V))
                    if ut not in seen[high]:
                        seen[high].add(ut)
                        high_Us[high].append(U)
    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "free_core": free_core,
        "high_Us": high_Us,
        "pairs": pairs,
    }


def toy_suite() -> dict[str, Any]:
    # arithmetic identities
    ensure(R_MAX == 70, "R")
    ensure(K_CAP == 2170, "K")
    ensure(SIDE_RADIX == 67270, "radix")
    ensure(SIDE_RADIX <= E, "radix fits e")
    ensure(71 * FLOOR_N_OVER_E * FLOOR_N_OVER_E > E, "R=71 overflows e")
    ensure(2 * SIDE_RADIX > E, "two layers no fit")
    ensure(TARGET_EP_CELLS == 1911, "cells")
    ensure(H_OVER_ENUM_MAX == E_P // PAIRS_PER_HIGH_MAX, "hover")
    ensure(N_CORE_PAIRS_MAX < E_P, "core pairs << ep")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")

    rows = []
    n_over_enum = 0
    n_over_rows = 0
    n_local_fail = 0
    n_pigeon_ok = 0
    local_names = [
        "c0U_delta",
        "c0U_c0V",
        "minU_mod_e_delta",
        "minU_c0U",
        "sumU_mod_e_delta",
    ]

    for p, n, j, w in [
        (17, 16, 4, 2),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 8, 2),
        (19, 18, 4, 2),
        (19, 18, 5, 2),
        (19, 18, 6, 2),
    ]:
        data = asp_data(p, n, j, w)
        if data is None or not data["high_Us"]:
            continue
        e = data["e"]
        high_Us = data["high_Us"]
        nH = len(high_Us)
        floor_ne = max(n // e, 1)
        need = max(1, (nH + floor_ne - 1) // floor_ne)
        # force overflow: use about 1/3 of needed tiers, at least 1, < need when need>1
        R = max(1, need // 3) if need > 1 else 1
        if need > 1:
            ensure(R < need or nH > R * floor_ne, "expect possible overflow")
        tags = multitier_fm(high_Us, n, e, R)
        H_core = set(tags)
        H_over = set(high_Us) - H_core
        # pigeon: |H_over| >= max(0, nH - R*floor_ne)
        cap = R * floor_ne
        ensure(len(H_over) >= max(0, nH - cap), "pigeon")
        n_pigeon_ok += 1

        upairs = unique_pairs(data["pairs"])
        core_p = [t for t in upairs if t[0] in H_core]
        over_p = [t for t in upairs if t[0] in H_over]
        N_over = len(over_p)
        # N_over bound
        bound = len(H_over) * floor_ne * max(floor_ne - 1, 0)
        ensure(N_over <= bound or floor_ne <= 1, f"N_over bound {N_over}>{bound}")

        # μ_over
        over_enum_ok = None
        if over_p:
            n_over_rows += 1
            ordered = sorted(
                over_p, key=lambda t: (t[3], t[4], t[1], t[2], repr(t[0]))
            )
            rank = {(t[1], t[2]): i for i, t in enumerate(ordered)}

            def mu_over(t):
                i = rank[(t[1], t[2])]
                return (i % e, i // e)

            over_enum_ok = mark_inj(over_p, mu_over)
            ensure(over_enum_ok, "over enum")
            n_over_enum += 1
            if N_over <= e * p:
                ensure(max(rank.values()) // e < p, "second coord")

            # local marks — expect failures when enough pairs
            local_results = {}
            for name, fn in [
                ("c0U_delta", lambda t: (t[3], (t[3] - t[4]) % p)),
                ("c0U_c0V", lambda t: (t[3], t[4])),
                ("minU_mod_e_delta", lambda t: (min(t[1]) % e, (t[3] - t[4]) % p)),
                ("minU_c0U", lambda t: (min(t[1]), t[3])),
                ("sumU_mod_e_delta", lambda t: (sum(t[1]) % e, (t[3] - t[4]) % p)),
            ]:
                ok = mark_inj(over_p, fn)
                local_results[name] = ok
            if N_over >= 4 and not all(local_results.values()):
                n_local_fail += 1
            # at least one local fails when N_over large
            if N_over >= 10:
                ensure(not all(local_results.values()), "expect some local fail")
        else:
            local_results = {nm: None for nm in local_names}

        # core structured mark with minU as ι proxy
        core_mark_ok = None
        if core_p:
            def core_m(t):
                tau, loc = tags[t[0]]
                return (tau, loc, min(t[1]), (t[3] - t[4]) % p)

            core_mark_ok = mark_inj(core_p, core_m)

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "free_core": data["free_core"],
                "nH": nH,
                "R": R,
                "cap": cap,
                "n_H_core": len(H_core),
                "n_H_over": len(H_over),
                "pigeon_ge": len(H_over) >= max(0, nH - cap),
                "n_pairs_core": len(core_p),
                "n_pairs_over": N_over,
                "N_over_bound": bound,
                "N_over_le_bound": N_over <= bound if floor_ne > 1 else True,
                "over_enum_inj": over_enum_ok,
                "core_mark_inj": core_mark_ok,
                "local_marks": local_results,
            }
        )

    ensure(n_over_rows > 0, "have overflow")
    ensure(n_over_enum == n_over_rows, "enum all")
    ensure(n_local_fail > 0, "local fails banked")
    ensure(n_pigeon_ok == len(rows), "pigeon all")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "n_over_rows": n_over_rows,
            "n_over_enum_inj": n_over_enum,
            "n_local_fail_rows": n_local_fail,
            "n_pigeon_ok": n_pigeon_ok,
        },
        "arithmetic": {
            "SIDE_RADIX": SIDE_RADIX,
            "SIDE_SLACK": SIDE_SLACK,
            "H_OVER_ENUM_MAX": H_OVER_ENUM_MAX,
            "TARGET_EP_CELLS": TARGET_EP_CELLS,
            "TARGET_H_LAYERS": TARGET_H_LAYERS,
            "N_CORE_PAIRS_MAX": N_CORE_PAIRS_MAX,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v41",
        "title": "overflow when |H|≫K_cap: e·p budget, enum gate, TARGET layers",
        "status": "PARTIAL_OVERFLOW_GATES",
        "claims": {
            "proves_ep_budget_Rmax_70": True,
            "proves_pigeon_H_over": True,
            "proves_N_over_bound": True,
            "proves_mu_over_conditional_ep": True,
            "proves_no_second_layer_in_one_ep": True,
            "proves_TARGET_multicell_arithmetic": True,
            "banks_local_overflow_marks_negative": True,
            "proves_N_over_le_ep_deployed": False,
            "proves_ambient_H_le_Kcap": False,
            "proves_A_SP_le_tp": False,
            "reopens_ambient_L_le_70": False,
        },
        "deployed": {
            "R_max": R_MAX,
            "K_cap": K_CAP,
            "K_max": K_MAX,
            "side_radix": SIDE_RADIX,
            "side_slack": SIDE_SLACK,
            "H_OVER_ENUM_MAX": H_OVER_ENUM_MAX,
            "N_core_pairs_max": N_CORE_PAIRS_MAX,
            "TARGET": TARGET,
            "e_p": E_P,
            "TARGET_EP_CELLS": TARGET_EP_CELLS,
            "TARGET_H_LAYERS": TARGET_H_LAYERS,
            "free_core": FREE_CORE,
            "t_p": T_P,
        },
        "lemmas": {
            "ep_budget": lemma_ep_budget(),
            "pigeon": lemma_pigeon_over(),
            "N_over": lemma_N_over(),
            "mu_over": lemma_mu_over(),
            "no_multilayer": lemma_no_multilayer_one_ep(),
            "TARGET_layers": lemma_target_layers(),
            "local_neg": lemma_local_marks_negative(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "core": f"H_core ≤{K_CAP} sides in one e·p via (τ,local,ι,δ) — tight",
            "overflow": (
                f"μ_over in second e·p-shaped cell if |H_over|≤{H_OVER_ENUM_MAX} "
                f"or N_over≤e·p; local marks banked negative"
            ),
            "single_tp": (
                "Single A_SP≤t·p still needs H_over≈∅ or overflow folded into "
                "the same e·p without double-booking (OPEN)"
            ),
            "next": (
                "Prove |H|≤K_cap or N_over≤e·p at deployed A_SP; or justify "
                "TARGET multi-cell / hybrid 2·e·p accounting"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['nH']} | {r['R']} | {r['n_H_core']} | "
        f"{r['n_H_over']} | {r['n_pairs_over']} | {r['N_over_le_bound']} | "
        f"{r['over_enum_inj']} | {r['pigeon_ge']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v41: overflow when |H| ≫ K_cap

Status: `PARTIAL` — **e·p side budget forces R_max=70** PROVED; **overflow
cardinality/enum gates** PROVED; local overflow marks **BANKED NEGATIVE**;
deployed N_over≤e·p / A_SP≤t·p still **OPEN**. Ambient L≤70 not reopened.

## Why K_cap / R_max are tight (PROVED)

Side mark `(τ, local, ι, δ)` with full within-family `ι < ⌊n/e⌋`:

```text
R · 31 · 31  ≤  e
R_max = 70  ⇒  70·31·31 = {d['side_radix']} ≤ e = 67472   (slack {d['side_slack']})
R = 71      ⇒  overflows e
```

One e·p cell ⇒ at most one multi-tier layer of |H|≤K_cap={d['K_cap']}.

**Λ≥2 layers cannot share one e·p** (2·{d['side_radix']} > e).

## Overflow size (PROVED)

```text
|H_over|  ≥  max(0, |H| − K_cap)
N_over    ≤  |H_over| · 31 · 30  = 930 |H_over|
```

## Overflow payment (PROVED conditional)

```text
μ_over = (i mod e, ⌊i/e⌋)   on overflow pairs (lex rank i)
N_over ≤ e·p  ⇒  lands in [e]×F_p
```

Worst-family gate:

```text
|H_over| ≤ H_OVER_ENUM_MAX = {d['H_OVER_ENUM_MAX']}  ≈ 1.546×10^11
```

## TARGET multi-cell arithmetic (PROVED numbers; strategy OPEN)

```text
⌊TARGET / (e·p)⌋ = {d['TARGET_EP_CELLS']}
⇒ ≤ {d['TARGET_H_LAYERS']} highs via layered multi-tier charged to TARGET
```

Does **not** by itself give A_SP ≤ t·p (single-cell goal).

## Hybrid sketch

| Cell | Content | Size gate |
|---|---|---|
| 1 | H_core (κ,ι,δ) | |H_core|≤K_cap (always by ledger) |
| 2 | μ_over on H_over | N_over≤e·p |

Total 2·e·p if both land — fine vs TARGET ({d['TARGET_EP_CELLS']} cells),
not fine vs single A_SP≤t·p unless cell2 is out-of-A_SP residual.

## Local marks (BANKED NEGATIVE)

`(c0U,δ)`, `(c0U,c0V)`, `(minU mod e, δ)`, `(minU,c0U)`, `(sumU mod e, δ)`
all collide on overflow pairs in toys with enough pairs.

## Toys

| j | w | #H | R | #H_core | #H_over | #pairs over | N≤bound? | enum? | pigeon? |
|---|---|---:|---:|---:|---:|---:|---|---|---|
{tbl}

Census: over enum {cen['n_over_enum_inj']}/{cen['n_over_rows']}; local-fail rows
{cen['n_local_fail_rows']}; pigeon {cen['n_pigeon_ok']}/{cen['n_rows']}.

## Path (updated)

```text
H_core ≤ 2170          paid in 1 e·p (tight)
H_over                 μ_over if N_over≤e·p
                       else TARGET layers / hybrid OPEN
Ambient L≤70           DEAD (v40)
A_SP ≤ t·p             needs H_over≈∅ or fold overflow into one e·p
```

## OPEN

1. Deployed `N_over ≤ e·p` or `|H|≤K_cap`
2. Local e·p overflow mark (negatives banked)
3. Policy: single t·p vs TARGET multi-cell for overflow

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v41.py --check
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
        "# kb-qatom-route-d-v41\n\n"
        "Overflow when |H|≫K_cap: e·p budget, enum gate, TARGET layers.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v41 report\n\nstatus: {cert['status']}\n"
        f"ep budget R_max=70: PROVED\n"
        f"mu_over conditional: PROVED\n"
        f"local overflow marks: BANKED NEGATIVE\n"
        f"N_over le ep deployed: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    ar = cert["toy_suite"]["arithmetic"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  e·p side budget ⇒ R_max=70 (radix {ar['SIDE_RADIX']}≤e): PROVED")
    print(f"  |H_over|≥|H|−K_cap pigeon: PROVED")
    print(f"  μ_over e·p iff N_over≤e·p (|H_over|≤{ar['H_OVER_ENUM_MAX']}): PROVED gate")
    print(f"  no 2nd multi-tier layer in one e·p: PROVED")
    print(f"  TARGET cells={ar['TARGET_EP_CELLS']} (max layered |H|={ar['TARGET_H_LAYERS']})")
    print(
        f"  toys: enum {cen['n_over_enum_inj']}/{cen['n_over_rows']}; "
        f"local-fail {cen['n_local_fail_rows']}; pigeon {cen['n_pigeon_ok']}"
    )


if __name__ == "__main__":
    main()
