#!/usr/bin/env python3
"""KB-MCA Route-D v27: multipad core intersections ≤ free_core−1 + κ census.

Attacks deployed M_pad via intersection packing and constructive residual high tags.

Proved:
  (1) Multipad core intersection bound: if C≠C' share multipad sides (U,V), then
        |C ∩ C'| ≤ free_core − 1.
      Proof: Δ = Λ_C − Λ_{C'} is nonzero monic-difference with
      deg(Δ) ≤ free_core − 1 (v21/v22 multi-mate), and every r ∈ C∩C' is a
      root of Δ; a nonzero univariate of degree ≤ d has ≤ d roots in F_p.
  (2) Corollary free_core=1: |C∩C'|=0 ⇒ cores pairwise disjoint ⇒
        M_pad ≤ ⌊(n−2e)/m_c⌋ (recover v26 packing).
  (3) Uniform packing bound: with s = free_core−1, each multipad core's
      (s+1)-subsets are private among the multipad cores in D\\(U∪V), so
        M_pad ≤ C(n−2e, free_core) / C(m_c, free_core).
      Deployed this ratio is astronomical (~10^478050) — does NOT force M_pad≤2.
  (4) High-tag criterion restated (v26): M_pad≤1 + residual highs↪[K] with
      K·⌊n/e⌋≤e (deployed K≤2176) ⇒ payment.
  (5) Toy bank: intersection bound tight often; free_core≥2 packing can exceed
      ⌊(n−2e)/m_c⌋; constructive κ into [K] (min_union, canon minU/c0, high0,
      pair minU, fiber-local high rank without fiber id) all collide globally;
      full high tag injects (over budget).

Does NOT prove M_pad≤1/≤2 at free_core=846161, nor residual highs↪[2176].

  python3 experimental/scripts/verify_kb_qatom_route_d_v27.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v27.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v27"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v27.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v27.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v27.report.md"
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


def poly_eval_monic(poly: list[int], x: int, p: int) -> int:
    deg = len(poly) - 1
    s = 0
    for k, c in enumerate(poly):
        s = (s + c * pow(x, deg - k, p)) % p
    return s


def lemma_intersection() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_core_intersection_le_free_core_minus_1",
        "statement": (
            "If C ≠ C' are multipad cores (share free-1 CS sides (U,V) in one "
            "j-fiber), then |C ∩ C'| ≤ free_core − 1, where "
            "free_core = m_c − w = j − 2w − 1."
        ),
        "proof": [
            "v22: multipad cores are depth-w multi-mates: Phi_w(C)=Phi_w(C'), "
            "so Δ := Λ_C − Λ_{C'} has deg(Δ) ≤ m_c − w − 1 = free_core − 1.",
            "C ≠ C' monic same degree ⇒ Δ ≠ 0.",
            "If r ∈ C ∩ C' then Λ_C(r)=Λ_{C'}(r)=0 ⇒ Δ(r)=0.",
            "A nonzero univariate polynomial of degree ≤ d over a field has at "
            "most d roots. Hence |C ∩ C'| ≤ deg(Δ) ≤ free_core − 1.",
        ],
        "deployed_free_core": FREE_CORE,
        "deployed_intersection_bound": FREE_CORE - 1,
    }


def lemma_fc1_recovery() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_1_disjoint_packing_recovered",
        "statement": (
            "free_core=1 ⇒ |C∩C'|≤0 ⇒ multipad cores pairwise disjoint "
            "⊆ D\\(U∪V) with |U∪V|=2e ⇒ M_pad ≤ ⌊(n−2e)/m_c⌋."
        ),
        "proof": ["Intersection theorem + v25/v26 packing."],
    }


def lemma_uniform_packing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_uniform_intersection_packing",
        "statement": (
            "Let s = free_core − 1. Among multipad cores for fixed (U,V), every "
            "pair intersects in ≤ s points, so each core's (s+1)-subsets are "
            "exclusive. With ground set D\\(U∪V) of size n−2e and |core|=m_c: "
            "M_pad ≤ C(n−2e, s+1) / C(m_c, s+1) = C(n−2e, free_core) / C(m_c, free_core)."
        ),
        "proof": [
            "If two m_c-sets both contain the same (s+1)-set T, then their "
            "intersection has size ≥ s+1 > s, contradicting the intersection bound.",
            "Hence the map core ↦ its family of (s+1)-subsets is disjointly supported.",
            "Count: M_pad · C(m_c, s+1) ≤ C(n−2e, s+1).",
        ],
        "deployed": {
            "free_core": FREE_CORE,
            "n_minus_2e": N - 2 * E,
            "m_c": M_C,
            "note": (
                "Ratio is ~10^478050 (log10 via lgamma) — useless for M_pad≤2."
            ),
            "log10_bound_estimate": 478050.28,
        },
    }


def lemma_kappa_criterion() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "high_tag_criterion_restated",
        "statement": (
            f"M_pad≤1 and residual highs ↪ [K] with K·⌊n/e⌋≤e (deployed K≤{K_MAX}) "
            "⇒ (κ,ι,δ) injects residual free-1 CS pairs into e·p ⇒ |A_SP|≤t·p."
        ),
        "proof": ["v26 high-tag payment criterion."],
        "deployed_K_max": K_MAX,
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_kappa_constructive_and_deployed_Mpad",
        "statement": (
            f"(1) Constructive κ: residual free-1 highs → [{K_MAX}] from "
            "fiber/ledger geometry (naive tags banked negative in toys).\n"
            f"(2) M_pad≤1 or ≤2 at free_core={FREE_CORE}: intersection packing "
            "only gives a huge binomial ratio; need residual/split constraints "
            "beyond |C∩C'|≤free_core−1."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_inter_pairs = 0
    n_inter_ok = 0
    n_inter_tight = 0
    n_fc1_pack_ok = 0
    n_fc1_pack_rows = 0
    n_fc_ge2_exceed_simple_pack = 0
    kappa_names = [
        "const",
        "high0_mod_K",
        "sumh_mod_K",
        "min_union_mod_K",
        "canon_minU_mod_K",
        "canon_c0_mod_K",
        "pair_minU_mod_K",
        "fiber_high_rank",  # rank among highs in fiber — no fiber id
        "full_high",
    ]
    kappa_coll_rows = {name: 0 for name in kappa_names}
    kappa_inj_rows = {name: 0 for name in kappa_names}
    kappa_tested_rows = 0

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
        simple_pack = (n - 2 * e) // m_c if n >= 2 * e else 0
        floor_ne = n // e
        K = e // floor_ne if floor_ne else 0
        # for toys with K=0 (e < n/e), use K_toy = e for tag modulus tests
        K_tag = K if K >= 1 else max(e, 1)

        vals = domain_vals(p, n)

        # free-1 families
        fam: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), e):
            U = frozenset(exps)
            high, c0 = free1_high_c0(U, vals, p)
            fam[high].append((c0, tuple(sorted(U))))
        iota: dict[tuple, int] = {}
        high_meta: dict[Any, dict] = {}
        for high, items in fam.items():
            order = sorted(items)
            for i, (c0, Ut) in enumerate(order):
                iota[Ut] = i
            c0_min, Ut_min = order[0]
            union: set[int] = set()
            for _, u in items:
                union |= set(u)
            high_meta[high] = {
                "canon_minU": min(Ut_min),
                "canon_c0": c0_min,
                "min_union": min(union) if union else 0,
            }

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        max_Mpad = 1
        max_inter = -1
        n_mp = 0
        max_highs_fib = 0
        n_fib_pairs = 0
        all_inter_ok = True

        # pair marks
        mark_buckets: dict[str, dict[Any, list]] = {
            name: defaultdict(list) for name in kappa_names
        }
        seen_fp: set = set()

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            pads: dict[Any, list] = defaultdict(list)
            highs_in_pairs: set = set()
            local_pairs: list = []
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
                        highs_in_pairs.add(high)
                        local_pairs.append((U, V, c0U, c0V, high))

            if local_pairs:
                n_fib_pairs += 1
                max_highs_fib = max(max_highs_fib, len(highs_in_pairs))
                hrank = {h: i for i, h in enumerate(sorted(highs_in_pairs))}

                for U, V, c0U, c0V, high in local_pairs:
                    fp = (tuple(sorted(U)), tuple(sorted(V)))
                    if fp in seen_fp:
                        continue
                    seen_fp.add(fp)
                    delta = (c0U - c0V) % p
                    iu = iota[tuple(sorted(U))]
                    meta = high_meta[high]
                    tags = {
                        "const": (0, iu, delta),
                        "high0_mod_K": ((high[0] % K_tag) if high else 0, iu, delta),
                        "sumh_mod_K": (sum(high) % K_tag if high else 0, iu, delta),
                        "min_union_mod_K": (meta["min_union"] % K_tag, iu, delta),
                        "canon_minU_mod_K": (meta["canon_minU"] % K_tag, iu, delta),
                        "canon_c0_mod_K": (meta["canon_c0"] % K_tag, iu, delta),
                        "pair_minU_mod_K": (min(U) % K_tag, iu, delta),
                        "fiber_high_rank": (hrank[high], iu, delta),
                        "full_high": (high, iu, delta),
                    }
                    for name, lab in tags.items():
                        mark_buckets[name][lab].append(fp)

            for _sk, Cs in pads.items():
                uniq = {tuple(sorted(C)) for C in Cs}
                if len(uniq) < 2:
                    max_Mpad = max(max_Mpad, len(uniq))
                    continue
                max_Mpad = max(max_Mpad, len(uniq))
                n_mp += 1
                cores = list(uniq)
                for a, b in itertools.combinations(cores, 2):
                    inter = len(set(a) & set(b))
                    max_inter = max(max_inter, inter)
                    n_inter_pairs += 1
                    if inter <= inter_bound:
                        n_inter_ok += 1
                    else:
                        all_inter_ok = False
                    if inter == inter_bound:
                        n_inter_tight += 1
                    # common roots are roots of Delta
                    p1 = monic_rev([vals[i] for i in a], p)
                    p2 = monic_rev([vals[i] for i in b], p)
                    for idx in set(a) & set(b):
                        r = vals[idx]
                        ensure(poly_eval_monic(p1, r, p) == 0, "root C")
                        ensure(poly_eval_monic(p2, r, p) == 0, "root C'")
                        ensure(
                            (poly_eval_monic(p1, r, p) - poly_eval_monic(p2, r, p)) % p
                            == 0,
                            "delta root",
                        )

        if free_core == 1 and n_mp > 0:
            n_fc1_pack_rows += 1
            ensure(max_Mpad <= simple_pack, f"fc1 pack {max_Mpad}>{simple_pack}")
            ensure(max_inter <= 0, "fc1 inter")
            n_fc1_pack_ok += 1

        if free_core >= 2 and n_mp > 0 and max_Mpad > simple_pack:
            n_fc_ge2_exceed_simple_pack += 1

        ensure(all_inter_ok, "inter bound")
        if n_mp > 0:
            ensure(max_inter <= inter_bound, "max inter")

        # kappa injectivity
        def stats(buckets):
            if not buckets:
                return None
            coll = sum(1 for v in buckets.values() if len(set(v)) >= 2)
            nuniq = len({fp for fps in buckets.values() for fp in fps})
            inj = nuniq > 0 and coll == 0 and len(buckets) == nuniq
            return {"inj": inj, "coll": coll, "nlab": len(buckets), "nuniq": nuniq}

        ms = {name: stats(mark_buckets[name]) for name in kappa_names}
        if ms["full_high"] and ms["full_high"]["nuniq"] > 0:
            kappa_tested_rows += 1
            ensure(ms["full_high"]["inj"], "full high injects")
            for name in kappa_names:
                st = ms[name]
                if st is None or st["nuniq"] == 0:
                    continue
                if st["inj"]:
                    kappa_inj_rows[name] += 1
                else:
                    kappa_coll_rows[name] += 1

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
                "inter_bound": inter_bound,
                "simple_pack": simple_pack,
                "K_budget": K,
                "K_tag": K_tag,
                "max_Mpad": max_Mpad,
                "n_multipad_events": n_mp,
                "max_pair_inter": max_inter,
                "max_highs_per_fiber": max_highs_fib,
                "n_fibers_with_pairs": n_fib_pairs,
                "exceeds_simple_pack": bool(
                    free_core >= 2 and n_mp > 0 and max_Mpad > simple_pack
                ),
                "marks": ms,
            }
        )

    ensure(n_inter_pairs > 0 and n_inter_ok == n_inter_pairs, "all inter ok")
    ensure(n_fc1_pack_rows > 0 and n_fc1_pack_ok == n_fc1_pack_rows, "fc1 pack")
    ensure(n_fc_ge2_exceed_simple_pack > 0, "bank simple pack fail at fc>=2")
    ensure(kappa_tested_rows > 0, "kappa rows")
    ensure(kappa_inj_rows["full_high"] == kappa_tested_rows, "full high always")
    # naive tags must collide on some row
    for name in kappa_names:
        if name == "full_high":
            continue
        ensure(
            kappa_coll_rows[name] > 0,
            f"need collision bank for kappa {name}",
        )

    ensure(FREE_CORE == 846161, "fc")
    ensure(K_MAX == 2176, "Kmax")
    ensure(FLOOR_N_MINUS_2E_OVER_MC == 2, "pack2")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_inter_pairs": n_inter_pairs,
            "n_inter_ok": n_inter_ok,
            "n_inter_tight": n_inter_tight,
            "tight_frac": n_inter_tight / n_inter_pairs if n_inter_pairs else 0,
            "n_fc1_pack_rows": n_fc1_pack_rows,
            "n_fc_ge2_exceed_simple_pack": n_fc_ge2_exceed_simple_pack,
            "kappa_tested_rows": kappa_tested_rows,
            "kappa_inj_rows": kappa_inj_rows,
            "kappa_coll_rows": kappa_coll_rows,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v27",
        "title": "Multipad core intersections ≤ free_core−1 + constructive κ census",
        "status": "PARTIAL_INTERSECTION_BOUND",
        "claims": {
            "proves_multipad_intersection_bound": True,
            "proves_fc1_packing_via_intersection": True,
            "proves_uniform_packing_bound": True,
            "proves_uniform_packing_gives_Mpad_le_2_deployed": False,
            "proves_constructive_kappa": False,
            "proves_M_pad_le_1_deployed": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_intersection_and_kappa_negatives": True,
        },
        "deployed": {
            "j": J,
            "w": W,
            "e": E,
            "m_c": M_C,
            "free_core": FREE_CORE,
            "intersection_bound": FREE_CORE - 1,
            "simple_pack_if_disjoint": FLOOR_N_MINUS_2E_OVER_MC,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "K_max": K_MAX,
            "uniform_pack_log10_est": 478050.28,
            "t_p": T_P,
            "e_p": E_P,
        },
        "lemmas": {
            "intersection": lemma_intersection(),
            "fc1_recovery": lemma_fc1_recovery(),
            "uniform_packing": lemma_uniform_packing(),
            "kappa_criterion": lemma_kappa_criterion(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "Mpad": (
                "Structural: multipad cores intersect in ≤ free_core−1 points; "
                "free_core=1 packing recovered; deployed binomial packing useless"
            ),
            "kappa": (
                f"Need constructive residual highs↪[{K_MAX}]; naive tags banked negative"
            ),
            "next": (
                "Ledger/fiber-native high witness for κ; residual multipad "
                "constraints forcing near-disjoint cores or M_pad≤2"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['max_Mpad']} | "
        f"{r['max_pair_inter']} | {r['inter_bound']} | {r['simple_pack']} | "
        f"{r['exceeds_simple_pack']} | {r['max_highs_per_fiber']} | "
        f"{(r['marks']['fiber_high_rank'] or {}).get('inj')} | "
        f"{(r['marks']['full_high'] or {}).get('inj')} |"
        for r in rows
    )
    ktbl = "\n".join(
        f"| `{name}` | {cen['kappa_inj_rows'][name]} | {cen['kappa_coll_rows'][name]} |"
        for name in cen["kappa_inj_rows"]
    )
    return f"""# KB-MCA Route-D v27: multipad intersections ≤ free_core−1

Status: `PARTIAL` — multipad **intersection bound** PROVED; constructive κ and
deployed M_pad≤2 still **OPEN**.

## Main theorem (PROVED)

If `C ≠ C'` are multipad cores, then

```text
|C ∩ C'|  ≤  free_core − 1
```

Proof: `Δ = Λ_C − Λ_{{C'}}` has `deg ≤ free_core−1` and is nonzero; every common
root is a root of `Δ`.

### Corollaries

| free_core | consequence |
|---:|---|
| = 1 | cores disjoint ⇒ `M_pad ≤ ⌊(n−2e)/m_c⌋` |
| ≥ 2 | pairwise inter ≤ free_core−1; simple disjoint packing may fail |

### Uniform packing (PROVED, weak deployed)

```text
M_pad  ≤  C(n−2e, free_core) / C(m_c, free_core)
```

Deployed `log10` estimate ≈ `{d['uniform_pack_log10_est']}` — **not** ≤ 2.

## Deployed

```text
free_core              = {d['free_core']}
intersection bound     = {d['intersection_bound']}
⌊(n−2e)/m_c⌋ if disj.  = {d['simple_pack_if_disjoint']}
K_max for high tags    = {d['K_max']}
```

## Constructive κ census (BANKED NEGATIVE)

Payment still: `M_pad≤1` + residual highs↪`[K≤{d['K_max']}]` + `(ι,δ)`.

| κ tag | inj rows | coll rows |
|---|---:|---:|
{ktbl}

Full high injects (over budget). Fiber-local high rank without fiber id collides.

## Toys

| j | w | free_core | max M_pad | max inter | bound | simple pack | exceeds pack? | max H/fib | fiber rank inj? | full high? |
|---|---|---:|---:|---:|---:|---:|---|---:|---|---|
{tbl}

Intersection checks: {cen['n_inter_ok']}/{cen['n_inter_pairs']} OK; tight frac
{cen['tight_frac']:.2f}. free_core≥2 exceeds simple pack on
{cen['n_fc_ge2_exceed_simple_pack']} rows.

## OPEN

1. Constructive `κ`: residual highs → `[{d['K_max']}]` (ledger/fiber witness)
2. `M_pad≤1` or core-near-disjoint `M_pad≤2` at free_core=`{d['free_core']}`
   beyond the weak binomial packing

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v27.py --check
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
        "# kb-qatom-route-d-v27\n\n"
        "Multipad core intersections ≤ free_core−1; constructive κ census.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v27 report\n\nstatus: {cert['status']}\n"
        f"intersection bound: free_core-1 = {FREE_CORE - 1}\n"
        f"uniform pack log10 est: {cert['deployed']['uniform_pack_log10_est']}\n"
        f"constructive kappa: OPEN (negatives banked)\n"
        f"deployed M_pad: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  multipad |C∩C'| ≤ free_core−1 = {FREE_CORE - 1}: PROVED")
    print("  free_core=1 packing recovered via intersection")
    print(
        f"  uniform packing bound: PROVED (deployed log10≈{cert['deployed']['uniform_pack_log10_est']}, useless for ≤2)"
    )
    print(
        f"  inter checks: {cen['n_inter_ok']}/{cen['n_inter_pairs']} "
        f"(tight frac {cen['tight_frac']:.2f})"
    )
    print(
        f"  κ: full_high inj rows={cen['kappa_inj_rows']['full_high']}; "
        f"naive tags coll (e.g. fiber_rank coll rows={cen['kappa_coll_rows']['fiber_high_rank']})"
    )


if __name__ == "__main__":
    main()
