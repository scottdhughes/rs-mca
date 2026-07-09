#!/usr/bin/env python3
"""KB-MCA Route-D v40: ambient L≤70 REFUTED; matched L_rep≤R_max=70 PROVED.

Resolves the v38–v39 L-gate honestly:
  • Ambient free-1 multipad load L can exceed 70 and 2176 — REFUTED.
  • Full-cover load of matched highs is NOT ≤R_max (mates extend covers) —
    banked: L_cover_core can exceed R on toys.
  • Representative matched load L_rep ≤ R_max = 70 — PROVED
    (≤1 matched U_rep through r per tier).
  • |H_core| ≤ R_max·⌊n/e⌋ = 2170 by packing (v34/v39) — still the high gate.

Proved:
  (1) Injection: L(r) = #{active free-1 e-sets containing r} ≤ C(n−1, e−1)
      (one U per high through r by v25 family disjointness).
  (2) Multi-mate double count: |F_H|≥2 ⇒ |H| ≤ n·L/(2e).
  (3) Matched representative load: multi-tier first-match, R tiers;
      L_rep(r) := #{H∈H_core : r ∈ U_rep(H)} ≤ R.
      R=R_max=70 ⇒ L_rep ≤ 70. PROVED.
  (4) |H_core| ≤ R_max·⌊n/e⌋ = K_cap = 2170 by packing (not via full-cover L).
  (5) Ambient L≤70 REFUTED: (n,e,L)=(16,3,96),(30,3,406),(70,3,2346),…
      A_SP-prefix census: (n=16,j=4,w=2) L≥72.
  (6) Ambient L≤2176 REFUTED: (70,3,2346), (72,3,2485).
  (7) Banked: full-cover load on H_core can exceed R_toy (mates); do not claim
      L_cover_core ≤ 70.

Does NOT prove ambient L≤70 or ambient |H|≤2170.
Surviving L≤70 statement = matched representative load L_rep.

  python3 experimental/scripts/verify_kb_qatom_route_d_v40.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v40.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v40"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v40.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v40.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v40.report.md"
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
L_GATE = R_MAX  # 70 — now the *matched* load gate
# SR room via |H|≤(n/e)L: need L ≤ e·p / (floor·floor·(floor-1))
PAIRS_PER_HIGH_MAX = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)
L_SR_WEAK = E_P // (FLOOR_N_OVER_E * PAIRS_PER_HIGH_MAX)
# multi-tier full-side capacity
K_SIDE = K_MAX * FLOOR_N_OVER_E  # 67456
L_SIDE_WEAK = K_MAX  # 2176 if |H|≤(n/e)L and |H|≤K_SIDE


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


def lemma_injection() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "load_equals_active_e_sets_through_point",
        "statement": (
            "For fixed domain index r: each free-1 high through r has exactly one "
            "active U∋r (family disjointness, v25). Distinct highs ⇒ distinct U. "
            f"Hence L(r) ≤ C(n−1, e−1). Deployed C({N}-1, {E}-1) is huge — not a "
            f"useful gate toward L≤{L_GATE}."
        ),
        "proof": [
            "v25: root sets of H(X)+c for fixed high H are pairwise disjoint.",
            "So at most one U∈F_H contains r.",
            "Map high ↦ that U is injective on highs through r.",
            "U\\{r} is an (e−1)-subset of the remaining n−1 points.",
        ],
    }


def lemma_multimate_count() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multimate_double_count",
        "statement": (
            "If every counted high has |F_H|≥2 (A_SP multi-mate), then "
            "|cover(H)|≥2e and |H| ≤ n·L/(2e). Deployed |H| ≤ 15.5·L "
            f"(vs v38's |H|≤31·L from |F_H|≥1)."
        ),
        "proof": [
            "sum_H |cover(H)| = sum_r L(r) ≤ n·L.",
            "sum_H |cover(H)| ≥ 2e·|H| under |F_H|≥2 and disjoint U's.",
        ],
        "deployed": {"H_le": f"n*L/(2e) ≈ {N / (2 * E):.4f}*L"},
    }


def lemma_L_rep() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "matched_representative_load_L_rep_le_Rmax",
        "statement": (
            f"Run multi-tier first-match with R=R_max={R_MAX} tiers. Let H_core be "
            "highs matched in some tier < R_max, each with representative e-set "
            "U_rep(H). For each domain point r and tier τ, at most one matched high "
            "in that tier has r∈U_rep (U_rep leaves the free set). Hence "
            f"L_rep(r) := #{{H∈H_core: r∈U_rep(H)}} ≤ R_max = {R_MAX}."
        ),
        "proof": [
            "Tier τ: free := {0..n−1}. Matching claims U_rep ⊆ free; free -= U_rep.",
            "Later claims in the same tier cannot reuse any point of U_rep.",
            "Therefore ≤1 matched high per tier has r∈U_rep.",
            f"R_max tiers ⇒ L_rep(r) ≤ {R_MAX}.",
            "WARNING: this is representative incidence, NOT full-cover load. "
            "Full cover(H)=⋃ F_H can place r in a mate V≠U_rep, so "
            "L_cover_core(r) can exceed R_max (toys bank this).",
        ],
        "deployed": {"R_max": R_MAX, "L_rep_gate": L_GATE, "K_cap": K_CAP},
    }


def lemma_H_core_packing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "H_core_packing_Kcap",
        "statement": (
            f"|H_core| ≤ R_max·⌊n/e⌋ = {R_MAX}·{FLOOR_N_OVER_E} = {K_CAP}. "
            "High gate for ledger payment — from packing, not ambient L."
        ),
        "proof": [
            "v34 multi-tier: ≤⌊n/e⌋ matched highs per tier (disjoint U_rep).",
            f"R_max={R_MAX} tiers ⇒ |H_core|≤{K_CAP}.",
        ],
    }


def lemma_cover_load_not_R() -> dict[str, Any]:
    return {
        "status": "REFUTED",
        "name": "full_cover_L_core_le_R_false",
        "statement": (
            "L_cover_core(r) := #{H∈H_core: r∈cover(H)} is NOT bounded by R in "
            "general — a matched high can touch r via a mate V≠U_rep."
        ),
        "note": "Toys: L_cover_core can exceed R_toy while L_rep≤R_toy.",
    }


def lemma_ambient_refute() -> dict[str, Any]:
    return {
        "status": "REFUTED",
        "name": "ambient_L_le_70_and_L_le_2176",
        "statement": (
            "Ambient free-1 multipad load (all fully D-split free-1 multi-mate "
            "highs, no j-fiber cut) is NOT bounded by 70 or by 2176 in general."
        ),
        "counters": [
            {"n": 16, "e": 3, "L": 96, "nH": 224, "note": "L>70"},
            {"n": 30, "e": 3, "L": 406, "nH": 961, "note": "L>70"},
            {"n": 70, "e": 3, "L": 2346, "nH": 4970, "note": "L>70 and L>2176"},
            {"n": 72, "e": 3, "L": 2485, "nH": 5329, "note": "L>2176"},
            {
                "n": 16,
                "j": 4,
                "w": 2,
                "e": 3,
                "L": 72,
                "note": "A_SP-prefix census L>70",
            },
        ],
        "consequence": (
            "v38 ambient L≤70 gate is FALSE as a general free-1 load claim. "
            "The surviving L≤70 statement is the matched-ledger L_core (lemma above)."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_overflow_when_ambient_H_huge",
        "statement": (
            "H_core is paid (L_core≤70, |H_core|≤2170). Overflow highs / pairs "
            "still need μ_over with N_over≤e·p or another residual cell. Ambient "
            f"|H| and ambient L are not bounded by {L_GATE}."
        ),
    }


def multitier_fm_tags(
    high_Us: dict[Any, list], n: int, e: int, max_tiers: int
) -> tuple[dict[Any, tuple[int, int]], dict[Any, frozenset]]:
    """Honest multi-tier match. Returns (tags, U_rep)."""
    remaining = {h for h, us in high_Us.items() if us}
    tags: dict[Any, tuple[int, int]] = {}
    U_rep: dict[Any, frozenset] = {}
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
                        U_rep[h] = frozenset(U)
                        local += 1
                        claimed.add(h)
                        break
        remaining -= claimed
    return tags, U_rep


def ambient_free1_load(p: int, n: int, e: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by_high: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), e):
        U = frozenset(exps)
        high, _c0 = free1_high_c0(U, vals, p)
        by_high[high].append(U)
    high_Us = {h: us for h, us in by_high.items() if len(us) >= 2}
    # family disjointness check
    for h, us in high_Us.items():
        pts: list[int] = []
        for U in us:
            pts.extend(U)
        ensure(len(pts) == len(set(pts)), f"family not disj high={h!r}")
    covers = {h: set().union(*us) for h, us in high_Us.items()}
    pt_h: dict[int, set] = defaultdict(set)
    for h, cset in covers.items():
        for r in cset:
            pt_h[r].add(h)
    L = max((len(s) for s in pt_h.values()), default=0)
    # injection check: L(r) == #U through r
    for r, hs in pt_h.items():
        nU = 0
        for h in hs:
            nU += sum(1 for U in high_Us[h] if r in U)
        ensure(nU == len(hs), "inject L vs U count")
    return {"p": p, "n": n, "e": e, "nH": len(high_Us), "L": L}


def asp_prefix_census(
    p: int, n: int, j: int, w: int
) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 30000:
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
            for U, _c0, high in lst:
                ut = tuple(sorted(U))
                if ut not in seen[high]:
                    seen[high].add(ut)
                    high_Us[high].append(U)
    if not high_Us:
        return {
            "p": p,
            "n": n,
            "j": j,
            "w": w,
            "e": e,
            "free_core": free_core,
            "nH": 0,
            "L": 0,
            "L_rep": 0,
            "L_cover_core": 0,
            "n_H_core": 0,
            "L_rep_le_R": True,
            "cover_exceeds_R": False,
        }
    covers = {
        h: set().union(*[set(u) for u in us]) for h, us in high_Us.items()
    }
    pt_h: dict[int, set] = defaultdict(set)
    for h, cset in covers.items():
        for r in cset:
            pt_h[r].add(h)
    L = max((len(s) for s in pt_h.values()), default=0)
    nH = len(high_Us)
    if nH > 0 and L > 0:
        sum_cover = sum(len(covers[h]) for h in high_Us)
        ensure(sum_cover == sum(len(s) for s in pt_h.values()), "handshaking")
        ensure(all(len(high_Us[h]) >= 2 for h in high_Us), "all multimate")
        ensure(sum_cover >= 2 * e * nH, "cover >= 2e |H|")
        ensure(nH * 2 * e <= n * L, "multimate |H|<=nL/(2e)")

    floor_ne = max(n // e, 1)
    # enough tiers to attempt a large core (up to R_MAX)
    R_toy = min(R_MAX, max(1, nH // floor_ne + 3))
    tags, U_rep = multitier_fm_tags(high_Us, n, e, max_tiers=R_toy)
    H_core = set(tags.keys())
    # L_rep: representative incidence
    pt_rep: dict[int, set] = defaultdict(set)
    for h, U in U_rep.items():
        for r in U:
            pt_rep[r].add(h)
    L_rep = max((len(s) for s in pt_rep.values()), default=0)
    ensure(L_rep <= R_toy, f"L_rep {L_rep} > R_toy {R_toy}")
    # also ≤1 per tier: check tier partition
    by_tier: dict[int, list] = defaultdict(list)
    for h, (tau, _loc) in tags.items():
        by_tier[tau].append(h)
    for tau, hs in by_tier.items():
        pts_claimed: list[int] = []
        for h in hs:
            pts_claimed.extend(U_rep[h])
        ensure(len(pts_claimed) == len(set(pts_claimed)), f"tier {tau} U_rep overlap")
    # L_cover_core: full cover load on H_core (may exceed R)
    pt_cover: dict[int, set] = defaultdict(set)
    for h in H_core:
        for r in covers[h]:
            pt_cover[r].add(h)
    L_cover_core = max((len(s) for s in pt_cover.values()), default=0)
    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "free_core": free_core,
        "nH": nH,
        "L": L,
        "L_rep": L_rep,
        "L_cover_core": L_cover_core,
        "R_toy": R_toy,
        "n_H_core": len(H_core),
        "cap_toy": R_toy * floor_ne,
        "L_rep_le_R": L_rep <= R_toy,
        "H_core_le_cap": len(H_core) <= R_toy * floor_ne,
        "cover_exceeds_R": L_cover_core > R_toy,
        "L_gt_70": L > 70,
    }


def toy_suite() -> dict[str, Any]:
    ensure(R_MAX == 70, "Rmax")
    ensure(L_GATE == 70, "Lgate")
    ensure(K_CAP == 2170, "Kcap")
    ensure(FREE_CORE == 846161, "fc")
    ensure(L_SR_WEAK > 10**9, "SR weak L huge")
    ensure(K_SIDE == 67456, "Kside")

    # --- ambient free-1 multipad counters ---
    ambient_rows = []
    for p, n, e in [
        (17, 16, 2),
        (17, 16, 3),
        (17, 16, 4),
        (31, 30, 3),
        (71, 70, 3),
        (73, 72, 3),
    ]:
        row = ambient_free1_load(p, n, e)
        ambient_rows.append(row)
        print(f"  ambient n={n} e={e}: nH={row['nH']} L={row['L']}", flush=True)

    ensure(any(r["L"] > 70 for r in ambient_rows), "need L>70 ambient")
    ensure(any(r["L"] > 2176 for r in ambient_rows), "need L>2176 ambient")
    # specific known counters
    by_ne = {(r["n"], r["e"]): r for r in ambient_rows}
    ensure(by_ne[(16, 3)]["L"] >= 90, "n16e3")
    ensure(by_ne[(70, 3)]["L"] > 2176, "n70e3")
    ensure(by_ne[(72, 3)]["L"] > 2176, "n72e3")

    # --- A_SP prefix + L_rep / cover ---
    asp_rows = []
    n_Lrep_ok = 0
    n_cover_exceeds = 0
    n_asp_over70 = 0
    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 4, 2),
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
        (19, 18, 4, 2),
        (19, 18, 5, 2),
        (19, 18, 6, 2),
    ]:
        row = asp_prefix_census(p, n, j, w)
        if row is None:
            continue
        asp_rows.append(row)
        if row["nH"] > 0:
            ensure(row["L_rep_le_R"], "L_rep bound")
            ensure(row["H_core_le_cap"], "H_core packing")
            n_Lrep_ok += 1
            if row["cover_exceeds_R"]:
                n_cover_exceeds += 1
        if row["L"] > 70:
            n_asp_over70 += 1

    ensure(n_Lrep_ok > 0, "have L_rep rows")
    ensure(n_asp_over70 > 0, "A_SP census L>70 exists")
    ensure(n_cover_exceeds > 0, "bank cover exceeds R")
    asp_72 = [r for r in asp_rows if r["j"] == 4 and r["w"] == 2 and r["n"] == 16]
    ensure(len(asp_72) == 1 and asp_72[0]["L"] >= 70, "asp L>=70 counter")

    max_L_amb = max(r["L"] for r in ambient_rows)
    max_L_asp = max(r["L"] for r in asp_rows)
    max_L_rep = max(r["L_rep"] for r in asp_rows)
    max_L_cover_core = max(r["L_cover_core"] for r in asp_rows)

    return {
        "status": "PASS",
        "ambient_rows": ambient_rows,
        "asp_rows": asp_rows,
        "census": {
            "n_ambient": len(ambient_rows),
            "n_asp": len(asp_rows),
            "n_Lrep_ok": n_Lrep_ok,
            "n_cover_exceeds_R": n_cover_exceeds,
            "n_asp_L_gt_70": n_asp_over70,
            "max_L_ambient": max_L_amb,
            "max_L_asp": max_L_asp,
            "max_L_rep": max_L_rep,
            "max_L_cover_core": max_L_cover_core,
            "ambient_refutes_L70": True,
            "ambient_refutes_L2176": True,
            "L_rep_le_R_all": True,
        },
    }


def build() -> dict[str, Any]:
    print("v40 toy suite...", flush=True)
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v40",
        "title": "ambient L≤70 REFUTED; matched L_rep≤R_max=70 PROVED",
        "status": "PARTIAL_LREP_PROVED_AMBIENT_REFUTED",
        "claims": {
            "proves_L_rep_le_Rmax": True,
            "proves_H_core_le_Kcap_packing": True,
            "proves_injection_L_le_binom": True,
            "proves_multimate_H_le_nL_over_2e": True,
            "refutes_ambient_L_le_70": True,
            "refutes_ambient_L_le_2176": True,
            "refutes_full_cover_L_core_le_R": True,
            "proves_ambient_L_le_70": False,
            "proves_ambient_H_le_Kcap": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_L_rep_bound": True,
            "toy_confirms_cover_can_exceed_R": True,
            "toy_confirms_ambient_refutation": True,
        },
        "deployed": {
            "R_max": R_MAX,
            "L_gate_matched": L_GATE,
            "K_cap": K_CAP,
            "K_side": K_SIDE,
            "L_SR_weak": L_SR_WEAK,
            "L_side_weak": L_SIDE_WEAK,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "e_p": E_P,
            "free_core": FREE_CORE,
            "t_p": T_P,
        },
        "lemmas": {
            "injection": lemma_injection(),
            "multimate": lemma_multimate_count(),
            "L_rep": lemma_L_rep(),
            "H_core_packing": lemma_H_core_packing(),
            "cover_load_not_R": lemma_cover_load_not_R(),
            "ambient_refute": lemma_ambient_refute(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "resolution": (
                "Ambient L≤70 is false. Surviving L≤70 is matched representative "
                "load L_rep≤R_max. High gate remains |H_core|≤K_cap by packing "
                "(v39). Full-cover load on H_core is not ≤R."
            ),
            "path": (
                "H_core (|H|≤2170 packing, L_rep≤70) → multi-tier sides + SR on "
                "core; overflow by μ_over / residual (v39)."
            ),
            "next": (
                "Close overflow when ambient |H|≫K_cap; do not reopen ambient L≤70."
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    amb = cert["toy_suite"]["ambient_rows"]
    asp = cert["toy_suite"]["asp_rows"]
    amb_tbl = "\n".join(
        f"| {r['n']} | {r['e']} | {r['nH']} | {r['L']} | {r['L'] > 70} | {r['L'] > 2176} |"
        for r in amb
    )
    asp_tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['nH']} | {r['L']} | "
        f"{r['L_rep']} | {r['L_cover_core']} | {r['R_toy']} | {r['n_H_core']} | "
        f"{r['L_rep_le_R']} | {r['cover_exceeds_R']} |"
        for r in asp
    )
    return f"""# KB-MCA Route-D v40: ambient L≤70 REFUTED; L_rep≤70 PROVED

Status: `PARTIAL` — **matched representative load L_rep ≤ R_max = {d['L_gate_matched']}
PROVED**; ambient **L≤70 / L≤2176 REFUTED**; full-cover L_core≤R **REFUTED**.

## Resolution of the L-gate

| Claim | Status |
|---|---|
| Ambient free-1 load L ≤ 70 | **REFUTED** |
| Ambient free-1 load L ≤ 2176 | **REFUTED** |
| Full-cover load on H_core ≤ R | **REFUTED** (mates) |
| Matched **representative** load L_rep ≤ R_max = 70 | **PROVED** |
| |H_core| ≤ R_max·⌊n/e⌋ = 2170 | **PROVED** (packing) |

```text
ambient L        can be ≫ 70, ≫ 2176
L_rep (U_rep)    ≤ R_max = 70     ← surviving L≤70
L_cover_core     can exceed R     ← mates touch extra points
|H_core|         ≤ 70 · 31 = 2170 ← packing (v39)
```

## Matched representative load (PROVED)

Multi-tier first-match, R = R_max tiers, each matched high has U_rep:

- Within one tier, claiming U_rep∋r removes r from `free` ⇒ ≤1 matched high with r∈U_rep per tier.
- R_max tiers ⇒ **L_rep(r) ≤ 70**.

This is **not** full-cover load: cover(H)=⋃F_H can include mates V≠U_rep through r.

## |H_core| (PROVED, packing)

```text
|H_core| ≤ R_max · ⌊n/e⌋ = 70 · 31 = 2170 = K_cap
```

## Ambient refutation (BANKED)

| n | e | #H | L | L>70? | L>2176? |
|---|---:|---:|---:|---|---|
{amb_tbl}

Max ambient L: **{cen['max_L_ambient']}**. A_SP-prefix also hits L>70.

## Other proved lemmas

1. **Injection:** L(r) ≤ C(n−1,e−1).
2. **Multi-mate count:** |F_H|≥2 ⇒ |H| ≤ n·L/(2e).

## A_SP toys

| j | w | free_core | #H | L | L_rep | L_cover_core | R | #H_core | L_rep≤R? | cover>R? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
{asp_tbl}

Census: L_rep ok={cen['n_Lrep_ok']}; cover exceeds R on {cen['n_cover_exceeds_R']} rows;
max L_rep={cen['max_L_rep']}; max L_cover_core={cen['max_L_cover_core']};
A_SP L>70 rows={cen['n_asp_L_gt_70']}.

## Program path

```text
Ambient L≤70     DEAD
L_rep ≤ 70       PROVED (representatives only)
|H_core| ≤ 2170  PROVED (packing / v39 ledger)
SR + sides       on H_core
Overflow         v39 μ_over / residual OPEN
```

## OPEN

1. Overflow when ambient |H| ≫ K_cap
2. A_SP ≤ t·p full close

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v40.py --check
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
        "# kb-qatom-route-d-v40\n\n"
        "Ambient L≤70 REFUTED; matched L_rep≤R_max=70 PROVED; "
        "full-cover L_core≤R REFUTED.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v40 report\n\nstatus: {cert['status']}\n"
        f"L_rep le {L_GATE}: PROVED\n"
        f"full-cover L_core le R: REFUTED\n"
        f"ambient L le 70: REFUTED\n"
        f"ambient L le 2176: REFUTED\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  L_rep ≤ R_max = {L_GATE}: PROVED (matched representatives)")
    print("  full-cover L_core ≤ R: REFUTED (mates)")
    print("  ambient L≤70: REFUTED")
    print("  ambient L≤2176: REFUTED")
    print(
        f"  toys: max ambient L={cen['max_L_ambient']}; max A_SP L={cen['max_L_asp']}; "
        f"max L_rep={cen['max_L_rep']}; max L_cover_core={cen['max_L_cover_core']}; "
        f"cover>R rows={cen['n_cover_exceeds_R']}"
    )


if __name__ == "__main__":
    main()
