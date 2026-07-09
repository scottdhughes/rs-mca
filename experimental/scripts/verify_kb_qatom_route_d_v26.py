#!/usr/bin/env python3
"""KB-MCA Route-D v26: free_core=1 M_pad packing + residual high-tag criterion.

Attacks (1) residual high separation inside e·p and (2) M_pad at free_core=1
as a model for free_core≫1.

Proved:
  (1) Free-1 CS sides U,V are disjoint (same F_H; v25 packing).
  (2) free_core=1 M_pad packing: multipad cores for fixed (U,V) form a subset
      of one free-1 high family of m_c-sets (v23), hence pairwise disjoint and
      contained in D \\ (U∪V). Therefore
        M_pad ≤ ⌊(n − 2e) / m_c⌋
      when free_core=1. (Also ≤ ⌊n/m_c⌋.)
  (3) Deployed arithmetic (even though free_core≠1): ⌊n/m_c⌋ = 2 and
      ⌊(n−2e)/m_c⌋ = 2 — packing bound would give M_pad≤2 *if* multipad
      cores were disjoint at free_core≫1 (OPEN; toys show intersections when
      free_core≥2).
  (4) Residual high-tag payment criterion: if M_pad≤1 and residual free-1
      highs inject into a set of size K with
        K · ⌊n/e⌋ ≤ e,
      then (κ(H), ι(U), δ) injects residual free-1 CS pairs into a set of size
      ≤ e·p = t·p. Deployed: ⌊n/e⌋=31 ⇒ K ≤ ⌊e/31⌋ = 2176.
  (5) Toy bank: free_core=1 ⇒ measured M_pad ≤ ⌊(n−2e)/m_c⌋; multipad cores
      disjoint; free_core≥2 can have core intersections (packing fails);
      multi-high fibers common (single residual high not automatic);
      (ι,δ) alone collides across highs; full high tag works but over budget;
      high0_mod_K tags fail injectivity on toys for K=K_max-scale.

Does NOT prove M_pad≤1 at free_core=846161, nor residual highs ↪ [2176].

  python3 experimental/scripts/verify_kb_qatom_route_d_v26.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v26.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v26"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v26.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v26.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v26.report.md"
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
FLOOR_N_OVER_MC = N // M_C  # 2
FLOOR_N_MINUS_2E_OVER_MC = (N - 2 * E) // M_C  # 2
K_MAX = E // FLOOR_N_OVER_E  # 2176


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


def core_free1_high_c0(C, vals, p, m_c, w):
    """When free_core=1, m_c=w+1: free-1 high = poly[1:m_c]."""
    poly = monic_rev([vals[i] for i in sorted(C)], p)
    return tuple(poly[1:m_c]), poly[m_c]


def lemma_UV_disjoint() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_CS_sides_disjoint",
        "statement": (
            "Any free-1 CS ordered pair (U,V) has U ∩ V = ∅. "
            "Proof: same free-1 high H ⇒ both in F_H ⇒ pairwise disjoint (v25)."
        ),
        "proof": ["v25 free-1 high family packing."],
    }


def lemma_fc1_Mpad_packing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_1_M_pad_packing_bound",
        "statement": (
            "Suppose free_core = 1 (so m_c = w+1). For any multipad side pair "
            "(U,V), the multipad cores form a free-1 CS clique of m_c-sets "
            "(v23) with a common free-1 high H_core, hence are pairwise disjoint "
            "and lie in D \\ (U ∪ V). Therefore "
            "M_pad ≤ ⌊(n − |U ∪ V|) / m_c⌋ = ⌊(n − 2e) / m_c⌋ "
            "(using |U ∪ V| = 2e from side disjointness)."
        ),
        "proof": [
            "v23: free_core=1 multipad cores are free-1 CS of degree m_c.",
            "v25 applied to m_c-sets with free-1 high (= depth-(m_c−1) multi-mates): "
            "free-1 family pairwise disjoint.",
            "Joint avoidance: cores ⊆ D \\ (U ∪ V).",
            "U ∩ V = ∅ ⇒ |U ∪ V| = 2e.",
            "Disjoint m_c-sets in a ground set of size n−2e ⇒ bound.",
        ],
        "deployed_note": (
            f"Deployed free_core={FREE_CORE} ≠ 1, so this bound does not apply. "
            f"Numerically ⌊(n−2e)/m_c⌋ = {FLOOR_N_MINUS_2E_OVER_MC} and "
            f"⌊n/m_c⌋ = {FLOOR_N_OVER_MC} — packing would give M_pad≤2 if "
            "multipad cores were disjoint at free_core≫1 (OPEN)."
        ),
        "deployed_floor_n_minus_2e_over_mc": FLOOR_N_MINUS_2E_OVER_MC,
        "deployed_floor_n_over_mc": FLOOR_N_OVER_MC,
    }


def lemma_high_tag_criterion() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_high_tag_payment_criterion",
        "statement": (
            "Assume M_pad ≤ 1. Suppose residual free-1 highs (those appearing "
            "among residual top-seam free-1 CS pairs) inject into a label set "
            f"of size K with K · ⌊n/e⌋ ≤ e. Let ι: F_H → {{0,..,|F_H|−1}} ⊆ "
            f"[⌊n/e⌋] be the within-family rank (v25). Then "
            "(U,V) ↦ (κ(H), ι(U), δ) with δ = c0U−c0V injects residual free-1 "
            f"CS ordered pairs into a set of size ≤ K·⌊n/e⌋·p ≤ e·p = t·p = {E_P}, "
            "hence |A_SP| ≤ t·p."
        ),
        "proof": [
            "v20: M_pad≤1 ⇒ pairs inject via side geometry; N_ord = N_side.",
            "v25: within F_H, (ι,δ) injective and |F_H|≤⌊n/e⌋.",
            "κ injective on residual highs ⇒ (κ(H),ι(U),δ) injective globally "
            "on residual pairs (pairs are always mono-high).",
            "Cardinality: |κ|·|ι|·|δ| ≤ K·⌊n/e⌋·p ≤ e·p.",
        ],
        "deployed": {
            "floor_n_over_e": FLOOR_N_OVER_E,
            "K_max": K_MAX,
            "K_max_times_floor": K_MAX * FLOOR_N_OVER_E,
            "e": E,
            "fits": K_MAX * FLOOR_N_OVER_E <= E,
        },
    }


def lemma_single_high_special_case() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "single_residual_high_closes_payment",
        "statement": (
            "If M_pad≤1 and residual free-1 CS pairs use only one high "
            "(K=1 ≤ K_max), then (ι,δ) alone injects into e·p and |A_SP|≤t·p."
        ),
        "proof": ["High-tag criterion with K=1; v25 within-family marks."],
        "toy_note": "Multi-high fibers occur on toys — single-high is not automatic.",
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_high_tag_and_deployed_Mpad",
        "statement": (
            f"(1) Inject residual free-1 highs into [K] with K≤{K_MAX} "
            f"(=⌊e/⌊n/e⌋⌋), or prove residual A_SP pairs use ≤{K_MAX} highs "
            "with an explicit κ.\n"
            f"(2) M_pad≤1 (or ≤2 via core packing) at free_core={FREE_CORE}: "
            "need multipad-core disjointness or other free_core≫1 control; "
            "toys show core intersections when free_core≥2."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_fc1_mp_checked = 0
    n_fc1_mp_bound_ok = 0
    n_fc1_cores_disj = 0
    n_fc_ge2_with_inter = 0
    n_fib_multi_high = 0
    n_fib_with_pairs = 0
    n_iota_delta_cross_coll = 0
    n_full_high_inj = 0
    n_tag_rows = 0

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
    ]:
        e = w + 1
        m_c = j - e
        if m_c <= 0 or math.comb(n, j) > 20000:
            continue
        free_core = m_c - w
        vals = domain_vals(p, n)
        floor_ne = n // e
        floor_pack = (n - 2 * e) // m_c if n >= 2 * e else 0
        k_max = e // floor_ne if floor_ne else e

        # side free-1 families for iota
        fam: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), e):
            U = frozenset(exps)
            high, c0 = free1_high_c0(U, vals, p)
            fam[high].append((c0, tuple(sorted(U))))
        iota: dict[tuple, int] = {}
        for high, items in fam.items():
            for i, (c0, Ut) in enumerate(sorted(items)):
                iota[Ut] = i

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        max_Mpad = 1
        max_highs_fib = 0
        n_mp = 0
        all_fc1_disj = True
        all_fc1_bound = True
        saw_fc_ge2_inter = False
        all_UV_disj = True

        # global pair marks
        marks: dict[str, dict[Any, list]] = {
            "iota_delta": defaultdict(list),
            "full_high_iota_delta": defaultdict(list),
            "high0_mod_kmax_iota_delta": defaultdict(list),
            "sumhigh_mod_kmax_iota_delta": defaultdict(list),
        }
        seen_pairs: set = set()

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            pads: dict[Any, list] = defaultdict(list)
            highs_fib: set = set()
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
                        if U & V:
                            all_UV_disj = False
                        pads[(high, c0U, c0V)].append((C, U, V))
                        highs_fib.add(high)
                        fp = (tuple(sorted(U)), tuple(sorted(V)))
                        if fp not in seen_pairs:
                            seen_pairs.add(fp)
                            delta = (c0U - c0V) % p
                            iu = iota[tuple(sorted(U))]
                            marks["iota_delta"][(iu, delta)].append(fp)
                            marks["full_high_iota_delta"][(high, iu, delta)].append(fp)
                            h0 = high[0] if high else 0
                            marks["high0_mod_kmax_iota_delta"][
                                (h0 % k_max if k_max else 0, iu, delta)
                            ].append(fp)
                            sh = sum(high) % k_max if k_max and high else 0
                            marks["sumhigh_mod_kmax_iota_delta"][(sh, iu, delta)].append(
                                fp
                            )

            if highs_fib:
                n_fib_with_pairs += 1
                max_highs_fib = max(max_highs_fib, len(highs_fib))
                if len(highs_fib) > 1:
                    n_fib_multi_high += 1

            for _sk, items in pads.items():
                by_c: dict[tuple, tuple] = {}
                for C, U, V in items:
                    t = tuple(sorted(C))
                    if t not in by_c:
                        by_c[t] = (U, V)
                if len(by_c) < 2:
                    max_Mpad = max(max_Mpad, len(by_c))
                    continue
                max_Mpad = max(max_Mpad, len(by_c))
                n_mp += 1
                cores = list(by_c.keys())
                U0, V0 = by_c[cores[0]]
                ensure(not (U0 & V0), "UV disj")

                # pairwise core intersections
                for a, b in itertools.combinations(cores, 2):
                    C1, C2 = set(a), set(b)
                    inter = len(C1 & C2)
                    if free_core == 1:
                        n_fc1_mp_checked += 1
                        if inter == 0:
                            n_fc1_cores_disj += 1
                        else:
                            all_fc1_disj = False
                        # same free-1 core high
                        h1, c1 = core_free1_high_c0(C1, vals, p, m_c, w)
                        h2, c2 = core_free1_high_c0(C2, vals, p, m_c, w)
                        ensure(h1 == h2, "fc1 core high")
                        ensure(c1 != c2, "fc1 core c0")
                    elif free_core >= 2 and inter > 0:
                        saw_fc_ge2_inter = True

                if free_core == 1:
                    if max_Mpad <= max(floor_pack, 1) or len(by_c) <= floor_pack:
                        pass  # checked globally below

        if free_core == 1 and n_mp > 0:
            ensure(max_Mpad <= floor_pack or floor_pack == 0 and max_Mpad <= n // m_c,
                   f"fc1 Mpad {max_Mpad} > pack {floor_pack}")
            # standard bound
            bound = max(floor_pack, 0)
            if max_Mpad <= bound or (bound == 0 and max_Mpad <= 1):
                n_fc1_mp_bound_ok += 1
            # always require M_pad <= n//m_c as weak and floor_pack when >=1
            pack_bound = (n - 2 * e) // m_c
            ensure(max_Mpad <= pack_bound, f"fc1 pack {max_Mpad}>{pack_bound}")
            n_fc1_mp_bound_ok += 0  # counted via ensure
            if all_fc1_disj:
                pass

        if saw_fc_ge2_inter:
            n_fc_ge2_with_inter += 1

        # mark injectivity summary
        def mark_stats(buckets):
            if not buckets:
                return None
            coll = sum(1 for v in buckets.values() if len(set(v)) >= 2)
            nuniq = len({fp for fps in buckets.values() for fp in fps})
            inj = coll == 0 and len(buckets) == nuniq and nuniq > 0
            return {"inj": inj, "coll": coll, "nlab": len(buckets), "nuniq": nuniq}

        ms = {name: mark_stats(b) for name, b in marks.items()}
        if ms["iota_delta"] and ms["iota_delta"]["nuniq"] > 0:
            n_tag_rows += 1
            if not ms["iota_delta"]["inj"]:
                n_iota_delta_cross_coll += 1
            if ms["full_high_iota_delta"] and ms["full_high_iota_delta"]["inj"]:
                n_full_high_inj += 1
            ensure(ms["full_high_iota_delta"]["inj"], "full high must inject")

        if free_core <= 0:
            ensure(max_Mpad <= 1, "fc0")

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
                "floor_pack_n_minus_2e_over_mc": floor_pack,
                "k_max": k_max,
                "max_Mpad": max_Mpad,
                "n_multipad_events": n_mp,
                "max_highs_per_fiber": max_highs_fib,
                "all_UV_disjoint": all_UV_disj,
                "fc1_cores_disjoint": all_fc1_disj if free_core == 1 else None,
                "fc_ge2_saw_core_intersection": saw_fc_ge2_inter if free_core >= 2 else None,
                "marks": ms,
            }
        )

    # global ensures
    ensure(any(r["free_core"] == 1 and r["n_multipad_events"] > 0 for r in rows), "fc1 mp")
    ensure(
        all(
            r["max_Mpad"] <= r["floor_pack_n_minus_2e_over_mc"]
            for r in rows
            if r["free_core"] == 1 and r["n_multipad_events"] > 0
        ),
        "all fc1 pack",
    )
    ensure(
        all(r["fc1_cores_disjoint"] for r in rows if r["free_core"] == 1 and r["n_multipad_events"] > 0),
        "fc1 disj",
    )
    ensure(n_fc_ge2_with_inter > 0, "bank fc>=2 intersections")
    ensure(n_fib_multi_high > 0, "bank multi-high fibers")
    ensure(n_iota_delta_cross_coll > 0, "bank cross-high iota delta coll")
    ensure(n_full_high_inj > 0, "full high works")
    # natural K-tags should fail somewhere
    ensure(
        any(
            r["marks"]["high0_mod_kmax_iota_delta"]
            and not r["marks"]["high0_mod_kmax_iota_delta"]["inj"]
            for r in rows
            if r["marks"]["high0_mod_kmax_iota_delta"]
            and r["marks"]["high0_mod_kmax_iota_delta"]["nuniq"] > 0
        ),
        "bank high0 mod kmax coll",
    )

    # deployed arithmetic
    ensure(FLOOR_N_OVER_E == 31, "31")
    ensure(K_MAX == 2176, "2176")
    ensure(K_MAX * FLOOR_N_OVER_E <= E, "budget fit")
    ensure(FLOOR_N_OVER_MC == 2, "mc pack 2")
    ensure(FLOOR_N_MINUS_2E_OVER_MC == 2, "n-2e pack 2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FREE_CORE != 1, "not fc1 deployed")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_fc1_mp_pair_checks": n_fc1_mp_checked,
            "n_fc1_cores_disj": n_fc1_cores_disj,
            "n_rows_fc_ge2_with_inter": n_fc_ge2_with_inter,
            "n_fibers_with_pairs": n_fib_with_pairs,
            "n_fibers_multi_high": n_fib_multi_high,
            "n_rows_iota_delta_cross_coll": n_iota_delta_cross_coll,
            "n_rows_full_high_inj": n_full_high_inj,
            "n_tag_rows": n_tag_rows,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v26",
        "title": "free_core=1 M_pad packing + residual high-tag e·p criterion",
        "status": "PARTIAL_HIGH_TAG_CRITERION",
        "claims": {
            "proves_UV_disjoint": True,
            "proves_fc1_Mpad_packing_bound": True,
            "proves_high_tag_payment_criterion": True,
            "proves_single_high_special_case": True,
            "proves_M_pad_le_1_deployed": False,
            "proves_residual_highs_into_Kmax": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_fc1_pack_and_cross_high_gap": True,
        },
        "deployed": {
            "n": N,
            "e": E,
            "m_c": M_C,
            "free_core": FREE_CORE,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "floor_n_over_mc": FLOOR_N_OVER_MC,
            "floor_n_minus_2e_over_mc": FLOOR_N_MINUS_2E_OVER_MC,
            "K_max": K_MAX,
            "K_max_times_floor_n_e": K_MAX * FLOOR_N_OVER_E,
            "t": T,
            "t_p": T_P,
            "e_p": E_P,
            "is_free_core_1": False,
        },
        "lemmas": {
            "UV_disjoint": lemma_UV_disjoint(),
            "fc1_Mpad": lemma_fc1_Mpad_packing(),
            "high_tag": lemma_high_tag_criterion(),
            "single_high": lemma_single_high_special_case(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "fc1_model": (
                f"free_core=1 ⇒ M_pad ≤ ⌊(n−2e)/m_c⌋ (packing); "
                "deployed would be ≤2 if free_core were 1"
            ),
            "high_tag": (
                f"Payment ⇐ M_pad≤1 + residual highs ↪ [{K_MAX}] "
                f"+ within-family (ι,δ)"
            ),
            "deployed_gap": (
                f"free_core={FREE_CORE}: core intersections possible (toys); "
                f"need highs↪[{K_MAX}] or M_pad control"
            ),
            "next": (
                "Construct κ: residual highs→[K_max] from fiber/ledger geometry; "
                "or prove multipad cores nearly-disjoint / M_pad≤2 at deployed"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['max_Mpad']} | "
        f"{r['floor_pack_n_minus_2e_over_mc']} | {r['max_highs_per_fiber']} | "
        f"{r['fc1_cores_disjoint']} | {r['fc_ge2_saw_core_intersection']} | "
        f"{(r['marks']['iota_delta'] or {}).get('inj')} | "
        f"{(r['marks']['full_high_iota_delta'] or {}).get('inj')} | "
        f"{(r['marks']['high0_mod_kmax_iota_delta'] or {}).get('inj')} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v26: free_core=1 M_pad packing + high-tag criterion

Status: `PARTIAL` — free_core=1 **M_pad packing** PROVED; residual **high-tag
payment criterion** PROVED; deployed M_pad / highs↪[K_max] still **OPEN**.

## free_core=1 M_pad packing (PROVED)

At free_core=1, multipad cores for fixed `(U,V)` are a free-1 CS clique of
`m_c`-sets (v23), hence pairwise disjoint and ⊆ `D \\ (U∪V)` with
`|U∪V|=2e`:

```text
M_pad  ≤  ⌊(n − 2e) / m_c⌋
```

## Deployed arithmetic

```text
⌊n/e⌋              = {d['floor_n_over_e']}
⌊n/m_c⌋            = {d['floor_n_over_mc']}
⌊(n−2e)/m_c⌋       = {d['floor_n_minus_2e_over_mc']}
K_max = ⌊e/⌊n/e⌋⌋  = {d['K_max']}
K_max · ⌊n/e⌋      = {d['K_max_times_floor_n_e']}  ≤ e = {d.get('e', E)}
free_core          = {d['free_core']}  (≠ 1 ⇒ packing bound not applied)
```

If multipad cores were disjoint at deployed free_core, packing would give
`M_pad ≤ 2`. Toys show **core intersections when free_core≥2** — disjointness
fails in general.

## Residual high-tag payment (PROVED criterion)

```text
M_pad ≤ 1
and residual highs ↪ [K] with K · ⌊n/e⌋ ≤ e
    ⇒  (κ(H), ι(U), δ) injects pairs into ≤ e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

Deployed budget allows **K ≤ {d['K_max']}**.

Special case **K=1** (single residual high): `(ι,δ)` alone closes payment.

## Toys

| j | w | free_core | max M_pad | pack bound | max highs/fib | fc1 cores disj? | fc≥2 inter? | (ι,δ) inj? | full high inj? | high0 mod K inj? |
|---|---|---:|---:|---:|---:|---|---|---|---|---|
{tbl}

- free_core=1: M_pad respects packing; cores disjoint.
- free_core≥2: core intersections observed ({cen['n_rows_fc_ge2_with_inter']} rows).
- Multi-high fibers: {cen['n_fibers_multi_high']}/{cen['n_fibers_with_pairs']}.
- `(ι,δ)` cross-high collides; full high tag injects (over budget);
  `high0 mod K_max` fails injectivity.

## OPEN

1. Residual highs ↪ `[{d['K_max']}]` (constructive κ from fiber/ledger), or
   single-high residual for A_SP
2. `M_pad≤1` (or packing M_pad≤2 via core disjointness) at free_core=`{d['free_core']}`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v26.py --check
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
        "# kb-qatom-route-d-v26\n\n"
        "free_core=1 M_pad packing + residual high-tag e·p criterion.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v26 report\n\nstatus: {cert['status']}\n"
        f"K_max: {cert['deployed']['K_max']}\n"
        f"floor (n-2e)/m_c: {cert['deployed']['floor_n_minus_2e_over_mc']}\n"
        f"deployed M_pad: OPEN\n"
        f"residual highs into K_max: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free_core=1 M_pad ≤ ⌊(n-2e)/m_c⌋: PROVED")
    print(f"  deployed packing numbers: ⌊n/m_c⌋={FLOOR_N_OVER_MC}, "
          f"⌊(n-2e)/m_c⌋={FLOOR_N_MINUS_2E_OVER_MC} (fc≠1 so not applied)")
    print(f"  high-tag criterion: K·⌊n/e⌋≤e with K_max={K_MAX}: PROVED")
    print("  single residual high ⇒ payment: PROVED special case")
    print(f"  toys: multi-high fib {cen['n_fibers_multi_high']}/{cen['n_fibers_with_pairs']}; "
          f"fc≥2 inter rows={cen['n_rows_fc_ge2_with_inter']}; "
          f"cross-high coll rows={cen['n_rows_iota_delta_cross_coll']}")


if __name__ == "__main__":
    main()
