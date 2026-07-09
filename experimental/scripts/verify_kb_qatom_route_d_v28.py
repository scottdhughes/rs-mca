#!/usr/bin/env python3
"""KB-MCA Route-D v28: ledger/fiber-native κ witnesses + residual multipad locus.

Attacks (1) fiber/ledger-native high tags and (2) residual M_pad≤2 constraints.

Proved:
  (1) Free-1 Newton invariants: for every U ∈ F_H, the power sums p_k(U) for
      k=1..e−1 are constant on F_H (Newton ↔ free-1 high). In particular
      high[0] = −p_1(U) for all U ∈ F_H. So the first monic high coefficient is
      the canonical 1-parameter family invariant (not a new residue class hash).
  (2) e=2 completeness: free-1 high is 1-dimensional; high ↔ p_1 is bijective
      among free-1 highs (high = (a1,) with a1=−p_1). Still F_p-valued.
  (3) Multipad locus: multipads require free-1 CS ordered pairs, hence only
      occur in fibers with a multi-member free-1 pencil. Matching-free residual
      fibers (R_sing / no top-seam pair) have N_ord=0 and M_pad=1 vacuously.
      Multipad control is purely an A_SP / top-seam problem.
  (4) Point-multiplicity form of packing: for fixed multipad (U,V), if every
      domain point lies in at most t multipad cores, then
        M_pad ≤ ⌊t(n−2e)/m_c⌋.
      t=1 ⇔ pairwise disjoint cores ⇒ M_pad ≤ ⌊(n−2e)/m_c⌋ (=2 deployed).
      free_core=1 ⇒ t=1 (v27 inter bound). free_core≥2 allows t≥2 (toys).
  (5) Fiber-native exclusive cover witness: in a fiber, a domain index exclusive
      to one high's side-cover tags that high locally; not always present / not
      globally unique (toys).
  (6) Ledger first-match native κ candidates (domain-order mins of family /
      fiber cover / exclusive cover) tested with (κ,ι,δ): F_p-scale tags can
      inject when they separate highs (e.g. p1 raw = high[0] for full high
      separation only if high is 1-dim or p1 unique); [K]-reduced tags collide.
      Full high still injects (over budget).

Does NOT prove residual t=1 at free_core=846161, nor κ into [2176].

  python3 experimental/scripts/verify_kb_qatom_route_d_v28.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v28.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v28"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v28.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v28.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v28.report.md"
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
FLOOR_N_MINUS_2E_OVER_MC = (N - 2 * E) // M_C
K_MAX = E // FLOOR_N_OVER_E


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


def lemma_newton_invariant() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_high_newton_invariants",
        "statement": (
            "For a free-1 high H and any U ∈ F_H, the monic free-1 coefficients "
            "of Λ_U are (H, c0(U)), and the power sums p_k(U) for k=1,...,e−1 "
            "depend only on H. In particular high[0] = −p_1(U) for every U ∈ F_H "
            "(with monic product convention Λ = ∏(X−r))."
        ),
        "proof": [
            "Free-1 high fixes monic coeffs of X^{e−1},...,X^1; only c0 varies.",
            "Newton–Girard: p_1,...,p_{e−1} are triangular functions of e_1,...,e_{e−1} "
            "hence of the free-1 high (p > e deployed).",
            "Explicitly p_1 = sum roots and monic coeff of X^{e−1} is −p_1.",
        ],
        "kappa_note": (
            "So κ_raw = high[0] is the ledger-native first Newton coordinate of "
            "the free-1 family — not an arbitrary hash. Still F_p-valued; "
            "reducing mod K loses injectivity (v27 bank)."
        ),
    }


def lemma_e2_complete() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e2_high_equals_p1",
        "statement": (
            "When e=2, free-1 high is a single coefficient a1=−p_1, so highs "
            "are bijective with their p_1 values. κ=high[0] completely separates "
            "free-1 highs (still in F_p, not [e])."
        ),
        "proof": [
            "e−1=1: high=(a1,) with a1=−(r+s) for the free-1 pair family.",
            "Distinct highs ⇔ distinct a1 ⇔ distinct p_1.",
        ],
    }


def lemma_multipad_locus() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipads_only_on_CS_pair_fibers",
        "statement": (
            "A multipad event requires a free-1 CS ordered pair (U,V), hence a "
            "fiber whose free-1 pencil has ≥2 members. Fibers with no top-seam "
            "CS pair (matching-free / R_sing style) have N_ord=0 and M_pad=1 "
            "vacuously. Multipad control is only needed on A_SP / top-seam fibers."
        ),
        "proof": [
            "Definition of multipad: ≥2 cores for one side key (high,c0U,c0V).",
            "Side key exists only when a free-1 CS ordered pair is present.",
            "No CS pair ⇒ no side key ⇒ M_pad:=1 by convention, N_ord=0.",
            "v17: Fib = A_SP ⊔ R_sing; R_sing is matching-free.",
        ],
    }


def lemma_point_multiplicity() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "M_pad_point_multiplicity_packing",
        "statement": (
            "Fix multipad sides (U,V). Let t = max_r |{multipad cores C ∋ r}| "
            "over r ∈ D\\(U∪V). Then M_pad ≤ ⌊t(n−2e)/m_c⌋. "
            "In particular t=1 ⇒ M_pad ≤ ⌊(n−2e)/m_c⌋ "
            f"(= {FLOOR_N_MINUS_2E_OVER_MC} deployed)."
        ),
        "proof": [
            "Double count pairs (core, root∈core): left M_pad·m_c; "
            "right ≤ t·|D\\(U∪V)| = t(n−2e).",
            "t=1 ⇔ cores pairwise disjoint (each root in ≤1 core).",
            "free_core=1 ⇒ |C∩C'|=0 (v27) ⇒ t=1 ⇒ packing bound (v26).",
        ],
        "deployed": {
            "floor_n_minus_2e_over_mc": FLOOR_N_MINUS_2E_OVER_MC,
            "t1_gives_Mpad_le": FLOOR_N_MINUS_2E_OVER_MC,
            "open": "t=1 at free_core≫1 on residual A_SP multipads",
        },
    }


def lemma_exclusive_witness() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "fiber_exclusive_cover_witness_definition",
        "statement": (
            "In a fiber z, let Cover(H) be the union of free-1 sides of high H "
            "that appear in z. An index r ∈ Cover(H) is exclusive if "
            "r ∉ Cover(H') for all other highs H' active in z. Any exclusive r "
            "is a fiber-native witness for H. Existence is not guaranteed; "
            "global uniqueness of min exclusive across fibers is not guaranteed."
        ),
        "proof": [
            "By definition exclusive r lies in only one active high's cover in z.",
            "Toys: exclusive often missing or colliding across fibers when used as κ.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_kappa_Kmax_and_residual_t1",
        "statement": (
            f"(1) Compress ledger-native high[0]=−p_1 (or exclusive first-match "
            f"witness) into [{K_MAX}] without collisions on residual highs, or "
            "prove ≤K_max residual highs.\n"
            f"(2) Residual multipad point-multiplicity t=1 at free_core={FREE_CORE} "
            f"(⇒ M_pad≤{FLOOR_N_MINUS_2E_OVER_MC}), or other residual constraint "
            "forcing near-disjoint multipad cores on A_SP."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_newton_ok = 0
    n_newton_checked = 0
    n_e2_bijective = 0
    n_e2_rows = 0
    n_rsing_no_mp = 0
    n_rsing_fibers = 0
    n_t1_fc1 = 0
    n_t_ge2_fc_ge2 = 0
    n_excl_present = 0
    n_pairs_total = 0

    mark_names = [
        "high0_iota_delta",  # F_p × [ι] × F_p  (ledger-native Newton)
        "high0_mod_K_iota_delta",
        "min_family_iota_delta",  # first-match min of global F_H
        "min_family_mod_K_iota_delta",
        "min_fiber_cover_iota_delta",
        "min_fiber_cover_mod_K_iota_delta",
        "min_excl_iota_delta",  # only when exclusive exists
        "full_high_iota_delta",
    ]
    mark_coll_rows = {m: 0 for m in mark_names}
    mark_inj_rows = {m: 0 for m in mark_names}
    mark_tested = {m: 0 for m in mark_names}

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
        K = e // floor_ne if floor_ne else 0
        K_tag = K if K >= 1 else max(e, 1)
        simple_pack = (n - 2 * e) // m_c if n >= 2 * e else 0

        # families + newton check
        fam: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), e):
            U = frozenset(exps)
            high, c0 = free1_high_c0(U, vals, p)
            p1 = sum(vals[i] for i in U) % p
            poly = monic_rev([vals[i] for i in sorted(U)], p)
            fam[high].append((c0, tuple(sorted(U)), p1, poly[1] if len(poly) > 1 else 0))

        iota: dict[tuple, int] = {}
        family_min: dict[Any, int] = {}
        p1_of_high: dict[Any, int] = {}
        for high, items in fam.items():
            n_newton_checked += 1
            p1s = {t[2] for t in items}
            a1s = {t[3] for t in items}
            if len(p1s) == 1 and len(a1s) == 1:
                n_newton_ok += 1
                p1 = next(iter(p1s))
                a1 = next(iter(a1s))
                ensure(a1 == (-p1) % p, "a1=-p1")
                if high:
                    ensure(high[0] == a1, "high0=a1")
                p1_of_high[high] = p1
            else:
                ensure(False, "newton constant")
            order = sorted(items, key=lambda t: t[0])
            for i, (c0, Ut, p1, a1) in enumerate(order):
                iota[Ut] = i
            union: set[int] = set()
            for _, Ut, _, _ in items:
                union |= set(Ut)
            family_min[high] = min(union)

        # e=2 bijective p1
        if e == 2:
            n_e2_rows += 1
            p1_to_h: dict[int, list] = defaultdict(list)
            for h, p1 in p1_of_high.items():
                p1_to_h[p1].append(h)
            if all(len(v) == 1 for v in p1_to_h.values()):
                n_e2_bijective += 1

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        max_Mpad = 1
        max_t = 0
        n_mp = 0
        n_fib_no_pair = 0
        n_fib_with_pair = 0
        max_highs = 0

        mark_b: dict[str, dict[Any, list]] = {m: defaultdict(list) for m in mark_names}
        seen_fp: set = set()
        n_excl_pairs = 0

        for _z, members in fib.items():
            supports = []
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                supports.append((S, U, C, high, c0))

            # covers per high in fiber
            cover: dict[Any, set] = defaultdict(set)
            for S, U, C, high, c0 in supports:
                cover[high] |= set(U)

            pencils: dict[Any, list] = defaultdict(list)
            for S, U, C, high, c0 in supports:
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            has_pair = False
            pads: dict[Any, list] = defaultdict(list)
            local_pairs = []
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
                        has_pair = True
                        pads[(high, c0U, c0V)].append(C)
                        local_pairs.append((U, V, c0U, c0V, high))

            if not has_pair:
                n_fib_no_pair += 1
                n_rsing_fibers += 1
                # no multipad possible
                ensure(all(len({tuple(sorted(C)) for C in Cs}) <= 1 for Cs in pads.values())
                       or not pads, "rsing mp")
                n_rsing_no_mp += 1
                continue

            n_fib_with_pair += 1
            highs_active = {h for *_, h in local_pairs}
            max_highs = max(max_highs, len(highs_active))

            # exclusive covers
            excl: dict[Any, list] = {h: [] for h in highs_active}
            for h in highs_active:
                for r in cover[h]:
                    if all(r not in cover[h2] for h2 in highs_active if h2 != h):
                        excl[h].append(r)

            for U, V, c0U, c0V, high in local_pairs:
                fp = (tuple(sorted(U)), tuple(sorted(V)))
                if fp in seen_fp:
                    continue
                seen_fp.add(fp)
                n_pairs_total += 1
                delta = (c0U - c0V) % p
                iu = iota[tuple(sorted(U))]
                h0 = high[0] if high else 0
                min_fam = family_min[high]
                min_fib = min(cover[high]) if cover[high] else 0
                exlist = excl.get(high, [])
                has_ex = len(exlist) > 0
                if has_ex:
                    n_excl_pairs += 1
                    n_excl_present += 1
                    min_ex = min(exlist)
                tags = {
                    "high0_iota_delta": (h0, iu, delta),
                    "high0_mod_K_iota_delta": (h0 % K_tag, iu, delta),
                    "min_family_iota_delta": (min_fam, iu, delta),
                    "min_family_mod_K_iota_delta": (min_fam % K_tag, iu, delta),
                    "min_fiber_cover_iota_delta": (min_fib, iu, delta),
                    "min_fiber_cover_mod_K_iota_delta": (min_fib % K_tag, iu, delta),
                    "full_high_iota_delta": (high, iu, delta),
                }
                if has_ex:
                    tags["min_excl_iota_delta"] = (min_ex, iu, delta)
                for name, lab in tags.items():
                    mark_b[name][lab].append(fp)

            for _sk, Cs in pads.items():
                uniq = {tuple(sorted(C)) for C in Cs}
                if len(uniq) < 2:
                    max_Mpad = max(max_Mpad, len(uniq))
                    continue
                max_Mpad = max(max_Mpad, len(uniq))
                n_mp += 1
                cores = [set(t) for t in uniq]
                # point multiplicity
                cnt: Counter = Counter()
                for c in cores:
                    for r in c:
                        cnt[r] += 1
                t_loc = max(cnt.values()) if cnt else 0
                max_t = max(max_t, t_loc)
                # U,V disjoint from cores
                # packing check with t
                ensure(
                    len(cores) * m_c <= t_loc * (n - 2 * e) or t_loc == 0,
                    "mult packing soft",
                )

        if free_core == 1 and n_mp > 0:
            ensure(max_t <= 1, "fc1 t<=1")
            ensure(max_Mpad <= simple_pack, "fc1 pack")
            n_t1_fc1 += 1
        if free_core >= 2 and n_mp > 0 and max_t >= 2:
            n_t_ge2_fc_ge2 += 1

        def stats(buckets):
            if not buckets:
                return None
            coll = sum(1 for v in buckets.values() if len(set(v)) >= 2)
            nuniq = len({fp for fps in buckets.values() for fp in fps})
            inj = nuniq > 0 and coll == 0 and len(buckets) == nuniq
            return {"inj": inj, "coll": coll, "nlab": len(buckets), "nuniq": nuniq}

        ms = {name: stats(mark_b[name]) for name in mark_names}
        if ms["full_high_iota_delta"] and ms["full_high_iota_delta"]["nuniq"] > 0:
            ensure(ms["full_high_iota_delta"]["inj"], "full high")
            for name in mark_names:
                st = ms[name]
                if st is None or st["nuniq"] == 0:
                    continue
                mark_tested[name] += 1
                if st["inj"]:
                    mark_inj_rows[name] += 1
                else:
                    mark_coll_rows[name] += 1

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
                "K_tag": K_tag,
                "simple_pack": simple_pack,
                "max_Mpad": max_Mpad,
                "max_point_mult_t": max_t,
                "n_multipad_events": n_mp,
                "n_fibers_no_pair": n_fib_no_pair,
                "n_fibers_with_pair": n_fib_with_pair,
                "max_highs_per_pair_fiber": max_highs,
                "n_excl_pairs": n_excl_pairs,
                "t1_packing_bound": simple_pack if max_t <= 1 else simple_pack * max(max_t, 1),
                "marks": ms,
            }
        )

    ensure(n_newton_checked > 0 and n_newton_ok == n_newton_checked, "newton")
    ensure(n_e2_rows > 0 and n_e2_bijective == n_e2_rows, "e2 bij")
    ensure(n_rsing_fibers > 0, "rsing fibs")
    ensure(n_t1_fc1 > 0, "fc1 t1")
    ensure(n_t_ge2_fc_ge2 > 0, "fc>=2 t>=2 bank")
    ensure(mark_tested["full_high_iota_delta"] > 0, "marks")
    ensure(mark_inj_rows["full_high_iota_delta"] == mark_tested["full_high_iota_delta"], "fh")
    # K-reduced high0 must collide somewhere
    ensure(mark_coll_rows["high0_mod_K_iota_delta"] > 0, "high0 mod K coll")
    # first-match family min mod K collides
    ensure(mark_coll_rows["min_family_mod_K_iota_delta"] > 0, "min fam mod K coll")

    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_N_MINUS_2E_OVER_MC == 2, "pack2")
    ensure(K_MAX == 2176, "Kmax")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_newton_checked": n_newton_checked,
            "n_newton_ok": n_newton_ok,
            "n_e2_bijective": n_e2_bijective,
            "n_rsing_fibers": n_rsing_fibers,
            "n_t1_fc1_rows": n_t1_fc1,
            "n_t_ge2_fc_ge2_rows": n_t_ge2_fc_ge2,
            "n_pairs_total": n_pairs_total,
            "n_excl_pair_instances": n_excl_present,
            "mark_tested": mark_tested,
            "mark_inj_rows": mark_inj_rows,
            "mark_coll_rows": mark_coll_rows,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v28",
        "title": "Ledger/fiber-native κ witnesses + residual multipad locus (t-packing)",
        "status": "PARTIAL_NATIVE_WITNESS",
        "claims": {
            "proves_free1_newton_invariants": True,
            "proves_e2_high_p1_bijective": True,
            "proves_multipads_only_on_CS_fibers": True,
            "proves_point_multiplicity_packing": True,
            "proves_t1_gives_Mpad_le_2_deployed": True,  # conditional on t=1
            "proves_residual_t1_deployed": False,
            "proves_kappa_into_Kmax": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_locus_newton_t_and_kappa_bank": True,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "e": E,
            "m_c": M_C,
            "floor_n_minus_2e_over_mc": FLOOR_N_MINUS_2E_OVER_MC,
            "K_max": K_MAX,
            "t1_implies_Mpad_le": FLOOR_N_MINUS_2E_OVER_MC,
            "e_p": E_P,
            "t_p": T_P,
        },
        "lemmas": {
            "newton": lemma_newton_invariant(),
            "e2": lemma_e2_complete(),
            "locus": lemma_multipad_locus(),
            "t_packing": lemma_point_multiplicity(),
            "exclusive": lemma_exclusive_witness(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "kappa": (
                "Ledger-native κ_raw = high[0] = −p_1 (Newton); need compression "
                f"to [{K_MAX}] or ≤{K_MAX} residual highs"
            ),
            "Mpad": (
                f"t=1 ⇒ M_pad≤{FLOOR_N_MINUS_2E_OVER_MC} deployed; multipads only "
                "on CS/A_SP fibers; residual t=1 OPEN at free_core≫1"
            ),
            "next": (
                "Prove residual A_SP multipad cores are pairwise disjoint (t=1), "
                "or bound # residual highs by K_max via ledger first-match"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['max_Mpad']} | "
        f"{r['max_point_mult_t']} | {r['simple_pack']} | {r['n_fibers_no_pair']} | "
        f"{r['n_fibers_with_pair']} | "
        f"{(r['marks']['high0_iota_delta'] or {}).get('inj')} | "
        f"{(r['marks']['high0_mod_K_iota_delta'] or {}).get('inj')} | "
        f"{(r['marks']['min_family_iota_delta'] or {}).get('inj')} |"
        for r in rows
    )
    mtbl = "\n".join(
        f"| `{name}` | {cen['mark_tested'][name]} | {cen['mark_inj_rows'][name]} | "
        f"{cen['mark_coll_rows'][name]} |"
        for name in cen["mark_tested"]
    )
    return f"""# KB-MCA Route-D v28: ledger/fiber-native κ + multipad locus

Status: `PARTIAL` — Newton-native high witness + multipad locus + t-packing
**PROVED**; residual `t=1` and κ→`[K_max]` still **OPEN**.

## Ledger-native high witness (PROVED)

On each free-1 family `F_H`:

```text
high[0]  =  −p_1(U)   for every U ∈ F_H
```

(Newton / monic convention). So `κ_raw = high[0]` is the **first Newton
coordinate** of the free-1 high — the natural ledger invariant, not a mod-hash.

- **e=2:** high is 1-dimensional; `high[0] ↔ p_1` bijective among highs.
- **Budget:** `(high[0], ι, δ)` has size `p·⌊n/e⌋·p` ≫ `e·p`; need compress
  `high[0]` into `[{d['K_max']}]` or ≤`{d['K_max']}` residual highs.

## Multipad locus (PROVED)

```text
multipads  ⇒  free-1 CS pairs  ⇒  only on multi-pencil / A_SP-type fibers
R_sing / no CS pair  ⇒  N_ord = 0, M_pad = 1 vacuous
```

## Point-multiplicity packing (PROVED)

```text
M_pad  ≤  ⌊ t (n−2e) / m_c ⌋
t = max_r  (number of multipad cores containing r)
```

| t | bound |
|---:|---|
| 1 | `⌊(n−2e)/m_c⌋` = **{d['floor_n_minus_2e_over_mc']} deployed** |
| free_core=1 | t=1 forced (v27) |
| free_core≥2 | t≥2 possible (toys) |

**Deployed win condition:** residual A_SP multipads have **t=1** ⇒ `M_pad≤2`.

## Fiber exclusive cover (defined)

`r` exclusive to `Cover(H)` in a fiber is a fiber-native high witness; existence
and global uniqueness not guaranteed (toys).

## κ census

| mark | tested | inj rows | coll rows |
|---|---:|---:|---:|
{mtbl}

## Toys

| j | w | free_core | max M_pad | max t | pack if t=1 | #no-pair fib | #pair fib | high0 inj? | high0 mod K? | min family inj? |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
{tbl}

Newton checks: {cen['n_newton_ok']}/{cen['n_newton_checked']}. e=2 bijective:
{cen['n_e2_bijective']} rows. R_sing fibers: {cen['n_rsing_fibers']}.

## OPEN

1. Compress Newton/first-match high witness into `[{d['K_max']}]` on residual, or
   prove ≤`{d['K_max']}` residual highs
2. Residual A_SP multipad **t=1** at free_core=`{d['free_core']}` ⇒ M_pad≤`{d['t1_implies_Mpad_le']}`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v28.py --check
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
        "# kb-qatom-route-d-v28\n\n"
        "Ledger/fiber-native κ witnesses + residual multipad locus.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v28 report\n\nstatus: {cert['status']}\n"
        f"t1 => M_pad <= {FLOOR_N_MINUS_2E_OVER_MC} deployed\n"
        f"residual t1: OPEN\n"
        f"kappa into K_max: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free-1 Newton: high[0]=−p_1 constant on F_H: PROVED")
    print("  e=2: high ↔ p_1 bijective: PROVED")
    print("  multipads only on CS-pair fibers (not R_sing): PROVED")
    print(f"  t=1 ⇒ M_pad ≤ ⌊(n−2e)/m_c⌋ = {FLOOR_N_MINUS_2E_OVER_MC} deployed: PROVED")
    print(f"  newton {cen['n_newton_ok']}/{cen['n_newton_checked']}; "
          f"R_sing fibs={cen['n_rsing_fibers']}; "
          f"fc>=2 t>=2 rows={cen['n_t_ge2_fc_ge2_rows']}")
    print(f"  κ: full_high inj; high0 mod K coll rows={cen['mark_coll_rows']['high0_mod_K_iota_delta']}")


if __name__ == "__main__":
    main()
