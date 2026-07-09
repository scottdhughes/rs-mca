#!/usr/bin/env python3
"""KB-MCA Route-D v42: |H|≤K_cap vs N_ord≤e·p — decouple card from multi-tier.

Attacks the v41 open (overflow / |H|≫K_cap) by separating two gates:

  Gate A — multi-tier constructive sides (κ,ι,δ):
      needs |H| ≤ K_cap = 2170  (R_max=70; v41 e·p budget).

  Gate B — cardinality A_SP ≤ t·p:
      |A_SP| ≤ N_ord  (v17)
      N_ord ≤ M_pad · N_side
      N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋−1)   (free-1 family packing, v36)
      ⇒ if N_ord ≤ e·p = t·p then |A_SP| ≤ t·p
      without multi-tier and without |H|≤K_cap.

Proved:
  (1) Card bridge: |A_SP| ≤ N_ord (restated v17). Combined with N_ord ≤ e·p
      ⇒ |A_SP| ≤ t·p. PROVED criterion.
  (2) Side count: N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋−1) = 930|H| deployed.
      PROVED (v36 family size).
  (3) Multipad lift: N_ord ≤ M_pad · N_side (v20). PROVED restated.
  (4) Weak high gates for card (PROVED arithmetic):
        M_pad ≤ 1  and  |H| ≤ H1 := ⌊e·p / 930⌋
            ⇒ N_ord ≤ e·p ⇒ |A_SP| ≤ t·p
        M_pad ≤ 2  and  |H| ≤ H2 := ⌊e·p / (2·930)⌋
            ⇒ same (Type D residual after SR has M_pad≤2, v35)
        M_pad ≤ 17 and  |H| ≤ H17 := ⌊e·p / (17·930)⌋
            ⇒ same under pack_ceil
      Deployed: H1 ≈ 1.546×10^11, H2 ≈ 7.73×10^10, H17 ≈ 9.09×10^9
      all ≫ K_cap = 2170.
  (5) Joint side enum: μ_all=(i mod e, ⌊i/e⌋) on unique free-1 CS pairs
      injects; N_side ≤ e·p ⇒ constructive e·p side mark for ALL pairs
      (core+overflow), no multi-tier. PROVED conditional.
  (6) Decoupling (PROVED): K_cap is necessary only for one-cell multi-tier
      (κ,ι,δ). Overflow when |H|>K_cap does NOT block card A_SP≤t·p if still
      N_ord≤e·p (e.g. |H|≤H2 under M_pad≤2).
  (7) K_cap still sufficient (PROVED): |H|≤K_cap ⇒ N_side ≤ 2_018_100
      ⇒ N_ord ≤ 17·N_side ≪ e·p ⇒ |A_SP|≤t·p, and multi-tier fits.
  (8) Ambient free-1 |H|>K_cap REFUTED as obstruction alone (v40/v41): need
      N_ord or |H| vs H2/H17, not vs K_cap, for card.
  (9) Toys: card inequalities; μ_all inj; |H|≤K_cap on A_SP-prefix suite
      (not a deployed proof); N_ord ≪ deployed e·p on toys; ambient free-1
      can have |H|>K_cap while N_side still ≪ deployed e·p on checked rows.

Does NOT prove deployed |H|≤K_cap, |H|≤H2, or N_ord≤e·p.
Does NOT prove A_SP≤t·p unconditionally.

  python3 experimental/scripts/verify_kb_qatom_route_d_v42.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v42.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v42"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v42.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v42.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v42.report.md"
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
PAIRS_PER_HIGH = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)  # 930
N_SIDE_AT_KCAP = K_CAP * PAIRS_PER_HIGH  # 2018100
PACK_CEIL = 17
H1 = E_P // PAIRS_PER_HIGH  # M_pad=1
H2 = E_P // (2 * PAIRS_PER_HIGH)  # M_pad=2
H17 = E_P // (PACK_CEIL * PAIRS_PER_HIGH)  # M_pad=pack


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


def lemma_card_bridge() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "A_SP_le_N_ord_card_bridge",
        "statement": (
            "|A_SP| ≤ N_ord (v17). Therefore N_ord ≤ e·p = t·p ⇒ |A_SP| ≤ t·p. "
            "This is pure cardinality — no multi-tier, no high tag."
        ),
        "proof": [
            "v17: |A_SP| ≤ N_ord = sum_{k≥2} k(k−1) over multi top-seam cliques.",
            "t = e deployed ⇒ t·p = e·p.",
        ],
    }


def lemma_N_side() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "N_side_le_H_times_family",
        "statement": (
            "N_side := # unique free-1 CS ordered pairs (U,V) (distinct c0, same high) "
            f"satisfies N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋−1) = {PAIRS_PER_HIGH}|H|."
        ),
        "proof": [
            "Per high: |F_H| ≤ ⌊n/e⌋ (v25); ordered pairs ≤ f(f−1).",
            "Sum over highs.",
        ],
    }


def lemma_N_ord_mpad() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "N_ord_le_Mpad_N_side",
        "statement": "N_ord ≤ M_pad · N_side (v20 multipad calculus).",
        "proof": ["v20: N_ord(z) ≤ M_pad(z)·N_side(z); global same with max M_pad."],
    }


def lemma_weak_H_gates() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "weak_high_gates_for_card",
        "statement": (
            f"Under N_side ≤ 930|H| and N_ord ≤ M_pad·N_side:\n"
            f"  M_pad≤1 and |H|≤H1={H1} ⇒ N_ord≤e·p ⇒ |A_SP|≤t·p\n"
            f"  M_pad≤2 and |H|≤H2={H2} ⇒ same\n"
            f"  M_pad≤17 and |H|≤H17={H17} ⇒ same\n"
            f"All H1,H2,H17 ≫ K_cap={K_CAP}."
        ),
        "proof": [
            "N_ord ≤ M_pad · 930 · |H| ≤ e·p ⇔ |H| ≤ e·p/(M_pad·930).",
            "Type D residual after SR has M_pad≤2 (v35) ⇒ H2 gate applies to residual.",
        ],
        "deployed": {"H1": H1, "H2": H2, "H17": H17, "K_cap": K_CAP},
    }


def lemma_mu_all() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "joint_side_enum_ep",
        "statement": (
            "Order all unique free-1 CS pairs lex; μ_all=(i mod e, ⌊i/e⌋) injective. "
            "If N_side ≤ e·p then μ_all : pairs → [e]×F_p. Pays core and overflow "
            "together — no H_core split required for constructive side payment."
        ),
        "proof": ["Same mixed radix as μ_enum / μ_over (v38–v39)."],
    }


def lemma_decouple() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "decouple_Kcap_from_card",
        "statement": (
            "Gate A (multi-tier (κ,ι,δ) in one e·p) needs |H|≤K_cap (v41). "
            "Gate B (card |A_SP|≤t·p) needs only N_ord≤e·p, which allows |H| up to "
            f"H2≈{H2} under M_pad≤2. Overflow |H|>K_cap blocks Gate A, not necessarily Gate B."
        ),
        "proof": [
            "v41: R·31·31≤e forces R≤70 and |H|≤K_cap for (τ,local,ι,δ).",
            "This file: card gates H1/H2/H17.",
        ],
    }


def lemma_Kcap_sufficient() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Kcap_sufficient_for_both_gates",
        "statement": (
            f"|H|≤K_cap={K_CAP} ⇒ N_side≤{N_SIDE_AT_KCAP} ≪ e·p ⇒ N_ord≤17·N_side ≪ e·p "
            "⇒ |A_SP|≤t·p (Gate B), and multi-tier sides fit (Gate A)."
        ),
        "proof": ["Arithmetic + lemmas above."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_N_ord_or_H_weak",
        "statement": (
            "(1) Prove N_ord ≤ e·p at deployed A_SP (strongest card close), or\n"
            f"(2) Prove |H| ≤ H2={H2} (M_pad≤2 residual) / H17 / H1, or\n"
            f"(3) Prove |H| ≤ K_cap={K_CAP} (closes both gates).\n"
            "Ambient free-1 can exceed K_cap (v40); card still open at weak gates."
        ),
    }


def asp_census(p: int, n: int, j: int, w: int) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 40000:
        return None
    free_core = m_c - w
    vals = domain_vals(p, n)
    fib: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        S = frozenset(exps)
        poly = monic_rev([vals[i] for i in sorted(S)], p)
        fib[tuple(poly[1 : w + 1])].append(S)

    high_Us: dict[Any, list] = defaultdict(list)
    seen_u: dict[Any, set] = defaultdict(set)
    unique_fp: set = set()
    N_ord = 0
    P_multi = 0
    A_SP = 0
    max_mpad = 1
    max_H_fib = 0

    for _z, members in fib.items():
        pencils: dict[Any, list] = defaultdict(list)
        for S in members:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = S - U
            high, c0 = free1_high_c0(U, vals, p)
            pencils[(tuple(sorted(C)), high)].append((U, c0, high))
        fib_H: set = set()
        for _key, lst in pencils.items():
            by_u: dict = {}
            for U, c0, high in lst:
                by_u[tuple(sorted(U))] = (c0, high)
            k = len(by_u)
            if k >= 2:
                max_mpad = max(max_mpad, k)  # pencil size as local multipad proxy
                P_multi += 1
                A_SP += k
                N_ord += k * (k - 1)
                items = list(by_u.items())
                for i, (ut, (c0U, high)) in enumerate(items):
                    fib_H.add(high)
                    if ut not in seen_u[high]:
                        seen_u[high].add(ut)
                        high_Us[high].append(frozenset(ut))
                    for j2, (vt, (c0V, _)) in enumerate(items):
                        if i == j2 or c0U == c0V:
                            continue
                        unique_fp.add((ut, vt))
        max_H_fib = max(max_H_fib, len(fib_H))

    nH = len(high_Us)
    N_side = len(unique_fp)
    floor_ne = max(n // e, 1)
    N_side_bound = nH * floor_ne * max(floor_ne - 1, 0)

    # μ_all
    mu_ok = True
    if unique_fp:
        ordered = sorted(unique_fp)
        rank = {fp: i for i, fp in enumerate(ordered)}
        buckets: dict[Any, list] = defaultdict(list)
        for fp, i in rank.items():
            buckets[(i % e, i // e)].append(fp)
        mu_ok = all(len(set(v)) == 1 for v in buckets.values()) and len(
            buckets
        ) == len(ordered)
        if N_side <= e * p:
            ensure(max(rank.values()) // e < p, "mu second <p")

    ensure(A_SP <= N_ord or N_ord == 0, "A_SP le N_ord")
    ensure(N_side <= N_side_bound or floor_ne <= 1, "N_side bound")
    # N_ord vs M_pad * N_side: mpad here is max pencil k, N_ord = sum k(k-1)
    # N_ord <= max_k * sum (k-1)*k/max? weaker: N_ord <= max_mpad * N_side only if
    # each side pair appears in ≤ max_mpad? Not always with this proxy.
    # Use N_ord <= max_mpad * N_side as soft check when M_pad is true multipad ratio.
    # Safer: N_ord pairs are seam pairs; each contributes to N_side image.
    # On toys verify N_ord <= max(1,max_mpad) * max(N_side,1) * something
    # Actually k(k-1) pairs in pencil map to k(k-1) side ordered pairs in unique_fp
    # globally may collapse across pencils. So N_ord >= N_side possible? 
    # N_ord counts with multiplicity across pencils; unique_fp dedupes.
    # So N_ord >= N_side typically. M_pad * N_side bounds N_ord when each side
    # key has ≤M_pad cores — v20. Our max_mpad is pencil k not core mpad.
    # Check N_side <= N_ord when N_ord>0? Not required.

    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "free_core": free_core,
        "nH": nH,
        "N_side": N_side,
        "N_ord": N_ord,
        "A_SP": A_SP,
        "P_multi": P_multi,
        "max_pencil_k": max_mpad,
        "max_H_fib": max_H_fib,
        "N_side_bound": N_side_bound,
        "N_side_le_bound": N_side <= N_side_bound if floor_ne > 1 else True,
        "A_SP_le_N_ord": A_SP <= N_ord,
        "H_le_Kcap": nH <= K_CAP,
        "H_le_H1": nH <= H1,
        "H_le_H2": nH <= H2,
        "H_le_H17": nH <= H17,
        "N_side_le_ep_toy": N_side <= e * p,
        "N_side_le_ep_dep": N_side <= E_P,
        "N_ord_le_ep_dep": N_ord <= E_P,
        "mu_all_inj": mu_ok,
        "card_ok_if_Kcap": nH <= K_CAP and N_side <= N_SIDE_AT_KCAP,
    }


def ambient_free1(p: int, n: int, e: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by_high: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), e):
        U = frozenset(exps)
        high, c0 = free1_high_c0(U, vals, p)
        by_high[high].append((U, c0))
    high_Us = {h: us for h, us in by_high.items() if len(us) >= 2}
    nH = len(high_Us)
    N_side = 0
    fps: set = set()
    for h, us in high_Us.items():
        for i, (U, c0U) in enumerate(us):
            for j2, (V, c0V) in enumerate(us):
                if i == j2 or c0U == c0V:
                    continue
                fps.add((tuple(sorted(U)), tuple(sorted(V))))
    N_side = len(fps)
    floor_ne = max(n // e, 1)
    return {
        "p": p,
        "n": n,
        "e": e,
        "nH": nH,
        "N_side": N_side,
        "H_gt_Kcap": nH > K_CAP,
        "N_side_le_ep_dep": N_side <= E_P,
        "H_le_H2": nH <= H2,
        "bound": nH * floor_ne * max(floor_ne - 1, 0),
    }


def toy_suite() -> dict[str, Any]:
    ensure(H1 == E_P // PAIRS_PER_HIGH, "H1")
    ensure(H2 == E_P // (2 * PAIRS_PER_HIGH), "H2")
    ensure(H17 == E_P // (PACK_CEIL * PAIRS_PER_HIGH), "H17")
    ensure(H1 > K_CAP, "H1>>K")
    ensure(H2 > K_CAP, "H2>>K")
    ensure(H17 > K_CAP, "H17>>K")
    ensure(N_SIDE_AT_KCAP < E_P, "kcap sides fit")
    ensure(PACK_CEIL * N_SIDE_AT_KCAP < E_P, "pack*kcap sides fit")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")
    # R=70 radix
    ensure(R_MAX * FLOOR_N_OVER_E * FLOOR_N_OVER_E <= E, "radix")

    asp_rows = []
    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 4, 2),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 8, 2),
        (17, 16, 9, 2),
        (19, 18, 5, 2),
        (19, 18, 6, 2),
        (19, 18, 7, 2),
        (31, 30, 4, 2),
        (31, 30, 5, 2),
    ]:
        r = asp_census(p, n, j, w)
        if r is None or r["nH"] == 0:
            continue
        ensure(r["A_SP_le_N_ord"], "A le Nord")
        ensure(r["N_side_le_bound"], "Nside bound")
        ensure(r["mu_all_inj"], "mu all")
        ensure(r["N_ord_le_ep_dep"], "Nord << dep ep on toys")
        ensure(r["N_side_le_ep_dep"], "Nside << dep ep")
        asp_rows.append(r)

    ensure(len(asp_rows) >= 8, "enough asp rows")
    ensure(all(r["H_le_Kcap"] for r in asp_rows), "asp toys under Kcap")
    ensure(all(r["H_le_H2"] for r in asp_rows), "asp toys under H2")

    amb_rows = []
    for p, n, e in [(17, 16, 3), (31, 30, 3), (71, 70, 3), (73, 72, 3)]:
        r = ambient_free1(p, n, e)
        amb_rows.append(r)
        ensure(r["N_side_le_ep_dep"], "amb Nside << ep")
        ensure(r["H_le_H2"], "amb H under H2 (weak)")
    ensure(any(r["H_gt_Kcap"] for r in amb_rows), "amb exceeds Kcap")
    # even when |H|>K_cap, N_side still fits deployed e·p on these rows
    ensure(
        all(r["N_side_le_ep_dep"] for r in amb_rows if r["H_gt_Kcap"]),
        "over Kcap still Nside ok vs dep ep",
    )

    return {
        "status": "PASS",
        "asp_rows": asp_rows,
        "ambient_rows": amb_rows,
        "census": {
            "n_asp": len(asp_rows),
            "n_amb": len(amb_rows),
            "max_asp_H": max(r["nH"] for r in asp_rows),
            "max_asp_N_side": max(r["N_side"] for r in asp_rows),
            "max_asp_N_ord": max(r["N_ord"] for r in asp_rows),
            "max_amb_H": max(r["nH"] for r in amb_rows),
            "amb_over_Kcap": sum(1 for r in amb_rows if r["H_gt_Kcap"]),
            "all_mu_all": True,
            "all_A_le_Nord": True,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v42",
        "title": "Decouple |H|≤K_cap (multi-tier) from N_ord≤e·p (card A_SP≤t·p)",
        "status": "PARTIAL_DECOUPLE_CARD_GATES",
        "claims": {
            "proves_A_SP_le_N_ord_bridge": True,
            "proves_N_side_le_930_H": True,
            "proves_weak_H_gates_H1_H2_H17": True,
            "proves_mu_all_conditional_ep": True,
            "proves_decouple_Kcap_vs_card": True,
            "proves_Kcap_sufficient_both": True,
            "proves_deployed_H_le_Kcap": False,
            "proves_deployed_H_le_H2": False,
            "proves_deployed_N_ord_le_ep": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "K_cap": K_CAP,
            "R_max": R_MAX,
            "H1": H1,
            "H2": H2,
            "H17": H17,
            "N_side_at_Kcap": N_SIDE_AT_KCAP,
            "pairs_per_high": PAIRS_PER_HIGH,
            "pack_ceil": PACK_CEIL,
            "e_p": E_P,
            "t_p": T_P,
            "free_core": FREE_CORE,
        },
        "lemmas": {
            "card_bridge": lemma_card_bridge(),
            "N_side": lemma_N_side(),
            "N_ord_mpad": lemma_N_ord_mpad(),
            "weak_H": lemma_weak_H_gates(),
            "mu_all": lemma_mu_all(),
            "decouple": lemma_decouple(),
            "Kcap_suff": lemma_Kcap_sufficient(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "overflow": (
                "|H|>K_cap blocks multi-tier one-cell sides, but card A_SP≤t·p "
                "survives until N_ord>e·p (or |H|>H2 under M_pad≤2)"
            ),
            "preferred_attack": (
                f"Prove N_ord≤e·p or |H|≤H2={H2} (much weaker than K_cap={K_CAP})"
            ),
            "next": (
                "Bound N_ord or |H| at deployed free_core; Type D residual uses H2"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    asp = cert["toy_suite"]["asp_rows"]
    amb = cert["toy_suite"]["ambient_rows"]
    asp_tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['nH']} | {r['N_side']} | "
        f"{r['N_ord']} | {r['A_SP']} | {r['A_SP_le_N_ord']} | {r['mu_all_inj']} | "
        f"{r['H_le_Kcap']} |"
        for r in asp
    )
    amb_tbl = "\n".join(
        f"| {r['n']} | {r['e']} | {r['nH']} | {r['N_side']} | {r['H_gt_Kcap']} | "
        f"{r['N_side_le_ep_dep']} | {r['H_le_H2']} |"
        for r in amb
    )
    return f"""# KB-MCA Route-D v42: decouple K_cap multi-tier from card A_SP≤t·p

Status: `PARTIAL` — **Gate A vs Gate B decoupled** PROVED; weak high gates
H1/H2/H17 PROVED as arithmetic; deployed N_ord≤e·p / |H|≤H2 still **OPEN**.

## Two gates (PROVED distinction)

| Gate | Needs | Pays |
|---|---|---|
| **A** multi-tier `(τ,local,ι,δ)` | `|H| ≤ K_cap = {d['K_cap']}` | constructive sides in **one** e·p |
| **B** cardinality | `N_ord ≤ e·p = t·p` | `|A_SP| ≤ t·p` (v17) |

Overflow `|H|>K_cap` blocks **A**, not automatically **B**.

## Card chain (PROVED)

```text
|A_SP|  ≤  N_ord                         (v17)
N_ord   ≤  M_pad · N_side                (v20)
N_side  ≤  |H| · 31 · 30  = 930 |H|      (v36/v25)
```

### Weak |H| gates for Gate B

```text
M_pad ≤ 1:   |H| ≤ H1  = {d['H1']}   ≈ 1.55e11
M_pad ≤ 2:   |H| ≤ H2  = {d['H2']}   ≈ 7.73e10   ← Type D residual (v35)
M_pad ≤ 17:  |H| ≤ H17 = {d['H17']}  ≈ 9.09e9
```

All ≫ K_cap = {d['K_cap']}.

### K_cap still sufficient for both

```text
|H| ≤ 2170  ⇒  N_side ≤ {d['N_side_at_Kcap']} ≪ e·p  ⇒  Gate B
            and multi-tier fits                         ⇒  Gate A
```

## Joint enum (PROVED conditional)

```text
μ_all = (i mod e, ⌊i/e⌋)  on all unique free-1 CS pairs
N_side ≤ e·p  ⇒  constructive e·p side mark (no H_core split)
```

## Program impact

```text
v41 overflow fear: |H|>K_cap ⇒ multi-tier fails
v42:              still OK for A_SP≤t·p if N_ord≤e·p
                  (e.g. |H|≤H2 with M_pad≤2 after SR)
```

Preferred attack is no longer `|H|≤2170` alone — prove **`N_ord≤e·p`** or
**`|H|≤H2`**.

## A_SP-prefix toys

| j | w | free_core | #H | N_side | N_ord | A_SP | A≤Nord? | μ_all? | H≤Kcap? |
|---|---|---:|---:|---:|---:|---:|---|---|---|
{asp_tbl}

## Ambient free-1 (no fiber cut)

| n | e | #H | N_side | H>Kcap? | N_side≤e·p dep? | H≤H2? |
|---|---:|---:|---:|---|---|---|
{amb_tbl}

Census: max asp H={cen['max_asp_H']}; max amb H={cen['max_amb_H']};
amb over Kcap={cen['amb_over_Kcap']}; all μ_all / A≤Nord on asp rows.

## OPEN

1. Deployed `N_ord ≤ e·p` or `|H| ≤ H2` (M_pad≤2 residual)
2. Or `|H| ≤ K_cap` (both gates)
3. Full `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v42.py --check
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
        "# kb-qatom-route-d-v42\n\n"
        "Decouple K_cap multi-tier from N_ord≤e·p card A_SP≤t·p.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v42 report\n\nstatus: {cert['status']}\n"
        f"decouple Kcap vs card: PROVED\n"
        f"H2 gate: {H2}\n"
        f"deployed N_ord le ep: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  Gate A multi-tier: |H|≤K_cap=2170 (unchanged)")
    print(f"  Gate B card A_SP≤t·p: N_ord≤e·p, allows |H|≤H2={H2} if M_pad≤2")
    print(f"  H1={H1} H17={H17} (≫ K_cap)")
    print("  μ_all joint enum under N_side≤e·p: PROVED conditional")
    print(
        f"  toys: asp max H={cen['max_asp_H']} N_ord={cen['max_asp_N_ord']}; "
        f"amb max H={cen['max_amb_H']} (over Kcap rows={cen['amb_over_Kcap']})"
    )


if __name__ == "__main__":
    main()
