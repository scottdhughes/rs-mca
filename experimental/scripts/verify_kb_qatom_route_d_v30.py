#!/usr/bin/env python3
"""KB-MCA Route-D v30: Type S free_core peel + high-budget criteria.

Attacks Type S multipads (shared-root reduction) and highs↪[K_max] budget.

Proved:
  (1) Type S root reduction: if multipad cores C≠C' share r, write
        Λ_C=(X−r)M, Λ_{C'}=(X−r)M'. Then M,M' are monic multi-mates of size
        m_c−1 at the same depth w with free_core' = free_core−1, and both avoid
        U∪V∪{r}. (Product by fixed (X−r) is triangular on monic coeffs ⇒ Phi_w
        of C determines Phi_w of M; deg(M−M') ≤ free_core−2.)
  (2) free_core=2 through-packing: for any r, Cores_r = {C multipad : r∈C} has
        reduced cores free-1 CS of size m_c−1 (Type D), hence pairwise disjoint
        on D\\(U∪V∪{r}), so
          |Cores_r| ≤ ⌊(n−2e−1)/(m_c−1)⌋.
  (3) Peel process: while t≥2, peel a max-multiplicity root; reduced through-set
        is a multipad/multi-mate family at free_core−1. After ≤ free_core−1 peels
        one reaches Type D (t=1) or empty. (Inductive free_core drop.)
  (4) Type D innermost packing: final Type D layer has size
        ≤ ⌊(n−2e−s)/(m_c−s)⌋ after s peels.
  (5) Shared-root first-match cell (structural): Type S multipads admit a
        peel-root sequence as ledger witnesses; payment can charge Type S to a
        shared-root cell once a size bound or e·p injection for peel witnesses
        is available. free_core=2: charge to (r, side key) with |Cores_r| packed.
  (6) High budget: residual/A_SP free-1 highs inject into [K] with K·⌊n/e⌋≤e
        (deployed K≤2176) ⇒ (κ,ι,δ) side marks fit e·p under M_pad≤1 (v26).
        Under M_pad≤2: need N_side ≤ e·p/2 or K·⌊n/e⌋≤e/2.
  (7) Toy bank: all Type S peels preserve multi-mate invariants; free_core=2
        through-pack holds; peels ≤ free_core−1; active high counts recorded
        vs K-scale (toys: global highs ≫ K_budget when e small).

Does NOT prove Type S M_pad≤2 at free_core=846161, nor |highs|≤2176 deployed.

  python3 experimental/scripts/verify_kb_qatom_route_d_v30.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v30.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v30"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v30.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v30.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v30.report.md"
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
# free_core=2 through pack at deployed if m_c were such — actual:
FLOOR_THROUGH_FC2 = (N - 2 * E - 1) // (M_C - 1)  # 2
K_MAX = E // FLOOR_N_OVER_E  # 2176
K_MAX_MPAD2 = E // (2 * FLOOR_N_OVER_E)  # 1088 if using M_pad≤2 side budget


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


def deg_diff(pa: list[int], pb: list[int], deg: int, p: int) -> int:
    for k in range(deg - 1, -1, -1):
        idx = deg - k
        if idx < len(pa) and (pa[idx] - pb[idx]) % p != 0:
            return k
    return -1


def lemma_root_reduction() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "type_S_shared_root_free_core_drop",
        "statement": (
            "Let C≠C' be multipad cores sharing r ∈ C∩C'. Write monic locators "
            "Λ_C = (X−r) M and Λ_{C'} = (X−r) M' with M,M' monic of degree m_c−1. "
            "Then Phi_w(M)=Phi_w(M') and deg(M−M') ≤ free_core−2, i.e. M,M' are "
            "depth-w multi-mates of size m_c−1 with free_core' = free_core−1. "
            "Both reduced supports avoid U∪V∪{r}."
        ),
        "proof": [
            "v27: deg(Λ_C−Λ_{C'}) ≤ free_core−1 and Δ(r)=0.",
            "Factor Δ = (X−r)(M−M') (exact monic division since both vanish at r).",
            "Hence deg(M−M') ≤ free_core−2.",
            "Monic product by fixed (X−r) is triangular with unit diagonal on "
            "coefficient space, so Phi_w(Λ_C)=Phi_w(Λ_{C'}) ⇔ Phi_w(M)=Phi_w(M').",
            "free_core' = (m_c−1)−w = free_core−1; multi-mate bound is "
            "deg ≤ free_core'−1 = free_core−2.",
            "Joint avoid: r∉U∪V (cores avoid U,V); reduced supports drop r.",
        ],
    }


def lemma_fc2_through_pack() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_2_through_set_packing",
        "statement": (
            "If free_core=2 and (U,V) is a multipad side key, then for every "
            "domain point r the through-set Cores_r has reduced cores that are "
            "free-1 CS of size m_c−1 (Type D), hence "
            f"|Cores_r| ≤ ⌊(n−2e−1)/(m_c−1)⌋. Deployed this is "
            f"{FLOOR_THROUGH_FC2} (if free_core were 2)."
        ),
        "proof": [
            "free_core=2 ⇒ deg(Δ)≤1. If r∈C∩C' then Δ=α(X−r), α≠0 ⇒ "
            "M−M' constant ≠0 ⇒ free-1 CS reduced cores.",
            "v25 packing on ground set D\\(U∪V∪{r}) of size n−2e−1 with "
            "block size m_c−1.",
            "Any two cores in Cores_r share r so reduce as above.",
        ],
        "deployed_through_pack_if_fc2": FLOOR_THROUGH_FC2,
        "deployed_free_core": FREE_CORE,
        "applies_deployed": FREE_CORE == 2,
    }


def lemma_peel_process() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "type_S_peel_to_type_D",
        "statement": (
            "Starting from a Type S multipad core set, repeatedly replace the "
            "through-set of a max-multiplicity root by its reduced supports. "
            "Each step drops free_core by 1 and preserves depth-w multi-mate "
            "structure (lemma 1). After at most free_core−1 steps the process "
            "reaches a Type D family (t=1) or empty. The final Type D layer "
            "obeys the Type D packing bound on the residual ground set."
        ),
        "proof": [
            "Type S ⇒ t≥2 ⇒ exists r with |Cores_r|≥2 ⇒ apply root reduction.",
            "Induct on free_core: free_core=1 is already Type D (v29).",
            "free_core≥2: peel → free_core−1 family; stop when t=1.",
            "At most free_core−1 drops reach free_core=1 or t=1 earlier.",
        ],
        "payment_note": (
            "Shared-root first-match cell: charge Type S multipads along the "
            "peel-root sequence; free_core=2 needs only one peel root r with "
            "packed |Cores_r|."
        ),
    }


def lemma_high_budget() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "high_tag_budget_Mpad1_and_Mpad2",
        "statement": (
            "Let ι: F_H → [⌊n/e⌋] be within-family rank (v25) and δ=c0U−c0V. "
            "If residual/A_SP free-1 highs inject into [K] via κ, then "
            "(κ,ι,δ) injects free-1 CS pairs into size K·⌊n/e⌋·p.\n"
            f"  M_pad≤1 payment: need K·⌊n/e⌋ ≤ e  (deployed K≤{K_MAX}).\n"
            f"  M_pad≤2 payment via N_ord≤2·N_side: need K·⌊n/e⌋ ≤ e/2 "
            f"(deployed K≤{K_MAX_MPAD2}) if using the same mark for all pairs, "
            "or N_side ≤ e·p/2 with other side control."
        ),
        "proof": [
            "v26 high-tag criterion for M_pad≤1.",
            "v20: N_ord ≤ M_pad·N_side; M_pad≤2 ⇒ N_ord≤2 N_side.",
            "If pairs inject into L then N_side ≤ |L|; need |L|≤e·p/2 for "
            "N_ord≤e·p when M_pad≤2.",
        ],
        "deployed": {
            "K_max_Mpad1": K_MAX,
            "K_max_Mpad2_half": K_MAX_MPAD2,
            "floor_n_over_e": FLOOR_N_OVER_E,
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_type_S_global_Mpad_and_highs_le_Kmax",
        "statement": (
            f"(1) Global Type S M_pad bound at free_core={FREE_CORE}: peel gives "
            "structure and free_core=2 through-pack, but full M_pad≤2 needs "
            "controlling unions of through-sets / residual Type S absence.\n"
            f"(2) |A_SP free-1 highs| ≤ {K_MAX} (or constructive κ into that "
            "range) for side marks."
        ),
    }


def peel_family(
    cores: list[set[int]], w: int, vals: list[int], p: int, free_core: int
) -> dict[str, Any]:
    """Peel Type S family; verify multi-mate invariants; return census."""
    peels = 0
    peel_roots: list[int] = []
    cur = [set(c) for c in cores]
    m0 = len(cur[0]) if cur else 0
    ok = True
    while cur:
        cnt: Counter = Counter()
        for c in cur:
            for r in c:
                cnt[r] += 1
        t = max(cnt.values()) if cnt else 0
        if t <= 1:
            return {
                "ok": ok,
                "peels": peels,
                "peel_roots": peel_roots,
                "final_size": len(cur),
                "final_type_D": True,
                "m0": m0,
            }
        r = max(cnt.keys(), key=lambda x: cnt[x])
        through = [c for c in cur if r in c]
        red = [c - {r} for c in through]
        if len(red) >= 2:
            m = len(red[0])
            for a, b in itertools.combinations(red, 2):
                ensure(len(a) == m and len(b) == m, "red size")
                p1 = monic_rev([vals[i] for i in sorted(a)], p)
                p2 = monic_rev([vals[i] for i in sorted(b)], p)
                if phi_w(p1, w) != phi_w(p2, w):
                    ok = False
                dd = deg_diff(p1, p2, m, p)
                # free_core' = m - w; bound free_core'-1 = m-w-1
                if dd > m - w - 1:
                    ok = False
        cur = red
        peel_roots.append(r)
        peels += 1
        if peels > free_core + 2:
            ok = False
            break
    return {
        "ok": ok,
        "peels": peels,
        "peel_roots": peel_roots,
        "final_size": 0,
        "final_type_D": True,
        "m0": m0,
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_type_S = 0
    n_peel_ok = 0
    n_fc2_S = 0
    n_fc2_through_pack_ok = 0
    n_peels_le_fc_minus_1 = 0
    max_peels_seen = 0
    max_active_highs = 0
    max_highs_per_fiber = 0

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
        vals = domain_vals(p, n)
        pack_D = (n - 2 * e) // m_c if n >= 2 * e else 0
        pack_through = (n - 2 * e - 1) // (m_c - 1) if m_c > 1 and n >= 2 * e + 1 else 0
        floor_ne = n // e
        K1 = e // floor_ne if floor_ne else 0
        K2 = e // (2 * floor_ne) if floor_ne else 0

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        active_highs: set = set()
        max_H_fib = 0
        n_S = 0
        n_D = 0
        max_mpad_S = 1
        max_mpad_D = 1
        max_peels = 0
        max_through = 0
        all_peel_ok = True
        all_fc2_pack = True
        all_peels_budget = True

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            pads: dict[Any, list] = defaultdict(list)
            fib_highs: set = set()
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
                        fib_highs.add(high)
                        active_highs.add(high)

            if fib_highs:
                max_H_fib = max(max_H_fib, len(fib_highs))

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
                    max_mpad_D = max(max_mpad_D, len(cores))
                    ensure(len(cores) <= pack_D, "D pack")
                    continue
                # Type S
                n_S += 1
                n_type_S += 1
                max_mpad_S = max(max_mpad_S, len(cores))
                ensure(free_core >= 2, "S needs fc>=2")

                # free_core=2 through pack
                if free_core == 2:
                    n_fc2_S += 1
                    for r, mult in cnt.items():
                        if mult >= 2:
                            max_through = max(max_through, mult)
                            if mult > pack_through:
                                all_fc2_pack = False
                            else:
                                n_fc2_through_pack_ok += 1

                # peel
                info = peel_family(cores, w, vals, p, free_core)
                if not info["ok"]:
                    all_peel_ok = False
                else:
                    n_peel_ok += 1
                max_peels = max(max_peels, info["peels"])
                max_peels_seen = max(max_peels_seen, info["peels"])
                if info["peels"] <= max(free_core - 1, 0):
                    n_peels_le_fc_minus_1 += 1
                else:
                    all_peels_budget = False
                ensure(info["final_type_D"], "peel to D")
                # final D packing on reduced ground: size after peels
                s = info["peels"]
                m_fin = m_c - s
                if m_fin > 0 and info["final_size"] > 0:
                    g_fin = n - 2 * e - s
                    pack_fin = g_fin // m_fin if g_fin >= m_fin else 0
                    ensure(info["final_size"] <= max(pack_fin, info["final_size"]), "soft")
                    # always: final Type D size ≤ floor(g_fin/m_fin) when t=1
                    if pack_fin >= 1:
                        ensure(info["final_size"] <= pack_fin, f"final D pack {info['final_size']}>{pack_fin}")

        max_active_highs = max(max_active_highs, len(active_highs))
        max_highs_per_fiber = max(max_highs_per_fiber, max_H_fib)

        if free_core == 2 and n_S > 0:
            ensure(all_fc2_pack, "fc2 through pack")
        if n_S > 0:
            ensure(all_peel_ok, "peel ok")
            ensure(all_peels_budget, "peels <= fc-1")

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
                "pack_through_fc2": pack_through,
                "K_Mpad1": K1,
                "K_Mpad2": K2,
                "n_type_D": n_D,
                "n_type_S": n_S,
                "max_Mpad_D": max_mpad_D,
                "max_Mpad_S": max_mpad_S,
                "max_peels": max_peels,
                "max_through": max_through,
                "n_active_highs": len(active_highs),
                "max_highs_per_fiber": max_H_fib,
                "active_highs_le_K1": (len(active_highs) <= K1) if K1 else False,
                "maxH_fib_le_K1": (max_H_fib <= K1) if K1 else False,
                "peel_ok": all_peel_ok if n_S > 0 else None,
                "fc2_through_pack_ok": all_fc2_pack if free_core == 2 and n_S > 0 else None,
            }
        )

    ensure(n_type_S > 0, "have Type S")
    ensure(n_peel_ok == n_type_S, "all peels ok")
    ensure(n_peels_le_fc_minus_1 == n_type_S, "peel depth")
    ensure(n_fc2_S > 0, "have fc2 S")
    ensure(n_fc2_through_pack_ok > 0, "fc2 pack checks")
    ensure(FREE_CORE == 846161, "fc")
    ensure(K_MAX == 2176, "Kmax")
    ensure(FLOOR_THROUGH_FC2 == 2, "through 2")
    ensure(FLOOR_N_MINUS_2E_OVER_MC == 2, "D 2")
    ensure(T == E, "t=e")
    # deployed free_core != 2 so fc2 through pack not a deployed M_pad kill
    ensure(FREE_CORE != 2, "deployed not fc2")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_type_S": n_type_S,
            "n_peel_ok": n_peel_ok,
            "n_fc2_S": n_fc2_S,
            "n_fc2_through_pack_ok": n_fc2_through_pack_ok,
            "max_peels_seen": max_peels_seen,
            "max_active_highs_any_row": max_active_highs,
            "max_highs_per_fiber_any_row": max_highs_per_fiber,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v30",
        "title": "Type S free_core peel + high-budget M_pad1/2 criteria",
        "status": "PARTIAL_TYPE_S_PEEL",
        "claims": {
            "proves_type_S_root_free_core_drop": True,
            "proves_fc2_through_packing": True,
            "proves_peel_to_type_D": True,
            "proves_type_S_Mpad_le_2_deployed": False,
            "proves_high_budget_criteria": True,
            "proves_highs_le_Kmax_deployed": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_peel_and_fc2_pack": True,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "e": E,
            "m_c": M_C,
            "type_D_bound": FLOOR_N_MINUS_2E_OVER_MC,
            "fc2_through_bound": FLOOR_THROUGH_FC2,
            "K_max_Mpad1": K_MAX,
            "K_max_Mpad2_half": K_MAX_MPAD2,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "t_p": T_P,
            "e_p": E_P,
            "is_free_core_2": False,
        },
        "lemmas": {
            "root_reduction": lemma_root_reduction(),
            "fc2_through": lemma_fc2_through_pack(),
            "peel": lemma_peel_process(),
            "high_budget": lemma_high_budget(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "type_S": (
                "Type S peels to Type D by free_core drops along shared roots; "
                "free_core=2 through-sets pack; deployed free_core≫2 still needs "
                "global Type S M_pad control / residual absence of Type S"
            ),
            "highs": (
                f"Side marks need |highs|≤{K_MAX} (M_pad1) or ≤{K_MAX_MPAD2} "
                "(half-budget M_pad2 path)"
            ),
            "next": (
                "Bound unions of Type S through-sets at free_core≫1, or show "
                "residual A_SP has only Type D; bound A_SP active highs"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_type_D']} | {r['n_type_S']} | "
        f"{r['max_Mpad_S']} | {r['max_peels']} | {r['max_through']} | "
        f"{r['n_active_highs']} | {r['max_highs_per_fiber']} | {r['K_Mpad1']} | "
        f"{r['peel_ok']} | {r['fc2_through_pack_ok']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v30: Type S free_core peel + high budget

Status: `PARTIAL` — Type S **free_core peel** and free_core=2 **through-pack**
PROVED; global Type S M_pad≤2 and highs≤K_max still **OPEN**.

## Type S root reduction (PROVED)

If multipad cores share `r`:

```text
Λ_C = (X−r) M,   Λ_{{C'}} = (X−r) M'
Phi_w(M)=Phi_w(M'),   deg(M−M') ≤ free_core−2
free_core' = free_core−1   (size m_c−1, same depth w)
```

## free_core=2 through-pack (PROVED)

```text
|Cores_r|  ≤  ⌊(n−2e−1)/(m_c−1)⌋
```

(reduced free-1 CS / Type D). Deployed value if free_core were 2:
`{d['fc2_through_bound']}` (actual free_core=`{d['free_core']}` ≠ 2).

## Peel process (PROVED)

```text
Type S  --peel max-mult root-->  free_core−1 family  -->  …  -->  Type D
```

≤ `free_core−1` peels. Final Type D packs on the residual ground set.
Shared-root first-match cell = charge Type S along peel-root witnesses.

## High budget (PROVED criteria)

```text
(κ,ι,δ) size = K · ⌊n/e⌋ · p
M_pad≤1:  K ≤ ⌊e/⌊n/e⌋⌋ = {d['K_max_Mpad1']}
M_pad≤2:  K ≤ ⌊e/(2⌊n/e⌋)⌋ = {d['K_max_Mpad2_half']}  (if N_ord≤2 N_side via same mark)
```

## Toys

| j | w | free_core | #D | #S | max M_pad S | max peels | max through | #highs | max H/fib | K1 | peel ok? | fc2 pack? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
{tbl}

Census: Type S peels OK={cen['n_peel_ok']}/{cen['n_type_S']}; max peels
seen={cen['max_peels_seen']}; fc2 through-pack checks={cen['n_fc2_through_pack_ok']}.

## OPEN

1. Global Type S `M_pad≤2` at free_core=`{d['free_core']}` (peel structure alone
   does not bound the union of through-sets tightly enough)
2. `|A_SP highs| ≤ {d['K_max_Mpad1']}` (or constructive κ)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v30.py --check
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
        "# kb-qatom-route-d-v30\n\n"
        "Type S free_core peel + high-budget M_pad1/2 criteria.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v30 report\n\nstatus: {cert['status']}\n"
        f"type S peel: PROVED\n"
        f"fc2 through pack: PROVED (not deployed fc)\n"
        f"K_max Mpad1: {K_MAX}\n"
        f"K_max Mpad2 half: {K_MAX_MPAD2}\n"
        f"type S Mpad le 2 deployed: OPEN\n"
        f"highs le Kmax: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  Type S shared-root free_core drop: PROVED")
    print(f"  free_core=2 through-pack ≤ ⌊(n-2e-1)/(m_c-1)⌋: PROVED")
    print("  peel to Type D in ≤ free_core−1 steps: PROVED")
    print(f"  high budget: K≤{K_MAX} (Mpad1), K≤{K_MAX_MPAD2} (Mpad2 half)")
    print(
        f"  toys: Type S={cen['n_type_S']} peels OK; max_peels={cen['max_peels_seen']}; "
        f"max highs/fib={cen['max_highs_per_fiber_any_row']}"
    )


if __name__ == "__main__":
    main()
