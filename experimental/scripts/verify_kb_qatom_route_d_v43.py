#!/usr/bin/env python3
"""KB-MCA Route-D v43: bound N_ord / |H|≤H2 at deployed free_core.

Preferred attack after v42 (not re-tightening to K_cap=2170).

Proved:
  (1) Deployed free-1 CS degree on A_SP complements (v19 specialized):
        n' := n − m_c = A + e = 1_183_520
        ⌊n'/e⌋ = 17 = pack_ceil
        each e-subset U ⊂ Ω (|Ω|=n') has ≤ 16 free-1 CS ordered mates in Ω.
      PROVED.
  (2) N_ord sandwich (v19): |A_SP| ≤ N_ord ≤ (pack−1)·|A_SP| = 16·|A_SP|.
      Hence within factor 16 of each other. PROVED.
  (3) Card criteria (PROVED conditional, deploy numbers):
        max N_ord ≤ e·p           ⇒ |A_SP| ≤ t·p
        max |A_SP| ≤ e·p/16     ⇒ N_ord ≤ e·p ⇒ |A_SP| ≤ t·p
        max P_multi ≤ e·p/17    ⇒ |A_SP| ≤ t·p
        |H| ≤ H2 and M_pad ≤ 2  ⇒ N_side ≤ 930·H2 ≤ e·p/2
                                ⇒ N_ord ≤ 2·N_side ≤ e·p  (Type D residual)
  (4) Matching-supported highs: |H_M| ≤ ⌊n/e⌋ = 31 ≤ H2. M-cell sides
      satisfy N_side_M ≤ 930·31 ≪ e·p. PROVED (v33/v36 + v42).
  (5) Active-U criterion: if M := # active free-1 e-sets ≤ M_* := ⌊e·p / 30⌋
      then N_side ≤ 30·M ≤ e·p. Deployed M_* ≈ 4.79e12. PROVED arithmetic.
  (6) H2 envelopes (arithmetic): the following are ≤ H2 if used as |H| bounds:
        31·n, pack·n, n'·16, A·e, 31·p, K_cap·e, …
      Ambient free-1 REFUTES |H|≤31n, |H|≤n·⌊n/e⌋, |H|≤31p, |H|≤pack·n
      on (n,e)=(30,3),(70,3),(72,3),… — those envelopes are NOT theorems.
  (7) Toys: free_core↑ correlates with |H|↓ / max_H_fib↓ on A_SP-prefix;
      N_ord ≤ 16·A_SP; complement degree ≤⌊n'/e⌋−1 on punctured domains;
      matching-supported H_M ≤⌊n/e⌋; ambient |H|>K_cap but ≪ H2 on suite;
      N_ord ≪ deployed e·p on all toys.

Does NOT prove deployed max N_ord ≤ e·p, |H|≤H2, or A_SP≤t·p.
Does NOT claim ambient envelope bounds that toys refute.

  python3 experimental/scripts/verify_kb_qatom_route_d_v43.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v43.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v43"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v43.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v43.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v43.report.md"
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
K_CAP = 70 * FLOOR_N_OVER_E  # 2170
PACK = (A + E) // E  # 17
N_PRIME = A + E  # 1183520
DEG_COMP = N_PRIME // E - 1  # 16
PAIRS_PER_HIGH = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)  # 930
H1 = E_P // PAIRS_PER_HIGH
H2 = E_P // (2 * PAIRS_PER_HIGH)
H17 = E_P // (PACK * PAIRS_PER_HIGH)
M_STAR = E_P // (FLOOR_N_OVER_E - 1)  # e·p/30 active-U gate
# envelopes ≤ H2 (arithmetic only — not all are theorems)
ENV_31_N = 31 * N
ENV_PACK_N = PACK * N
ENV_NPRIME_16 = N_PRIME * DEG_COMP
ENV_A_E = A * E
ENV_31_P = 31 * P
ENV_KCAP_E = K_CAP * E


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


def lemma_comp_degree() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "deployed_complement_free1_degree",
        "statement": (
            f"For any core C with |C|=m_c={M_C}, set Ω=D\\\\C (|Ω|=n'={N_PRIME}). "
            f"Each e-subset of Ω has at most deg={DEG_COMP} free-1 CS ordered mates "
            f"in Ω (⌊n'/e⌋−1 = {N_PRIME // E}−1). Deployed pack ⌊n'/e⌋={N_PRIME // E}={PACK}."
        ),
        "proof": [
            "v19 ambient_CS_pair_bound on Ω.",
            "Free-1 mates pairwise disjoint ⇒ pencil size ≤⌊|Ω|/e⌋.",
            f"n'=A+e={N_PRIME}, ⌊n'/e⌋={N_PRIME // E}, deg≤{DEG_COMP}.",
        ],
        "deployed": {
            "n_prime": N_PRIME,
            "floor_nprime_over_e": N_PRIME // E,
            "deg_max": DEG_COMP,
            "pack": PACK,
        },
    }


def lemma_Nord_sandwich() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "N_ord_A_SP_factor16_sandwich",
        "statement": (
            f"|A_SP| ≤ N_ord ≤ (pack−1)·|A_SP| = {PACK - 1}·|A_SP|. "
            "So N_ord and |A_SP| differ by at most factor 16."
        ),
        "proof": [
            "v19 handshaking: N_ord = sum deg ≤ Δ·|A_SP| with Δ=pack−1.",
            "|A_SP| ≤ N_ord because each A_SP vertex has deg ≥ 1 in multi pencils.",
        ],
    }


def lemma_card_criteria() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "card_criteria_N_ord_H2_Mstar",
        "statement": (
            "Any one of the following implies |A_SP| ≤ t·p = e·p:\n"
            f"  (C1) max N_ord ≤ e·p\n"
            f"  (C2) max |A_SP| ≤ e·p/16 = {E_P // 16}\n"
            f"  (C3) max P_multi ≤ e·p/17 = {E_P // PACK}\n"
            f"  (C4) M_pad≤2 and |H|≤H2={H2}  (N_side≤930·H2≤e·p/2, N_ord≤e·p)\n"
            f"  (C5) M := #active free-1 e-sets ≤ M_*={M_STAR}  (N_side≤30·M≤e·p),\n"
            "       and M_pad≤1; or with M_pad≤2 need M≤M_*/2 for N_ord≤e·p via N_side."
        ),
        "proof": [
            "v17–v20 cost laws + v42 weak high gates + deg≤⌊n/e⌋−1 per U.",
            "N_side ≤ sum_U deg(U) ≤ M·(⌊n/e⌋−1) = 30M deployed.",
        ],
        "deployed": {
            "e_p": E_P,
            "e_p_over_16": E_P // 16,
            "e_p_over_17": E_P // PACK,
            "H2": H2,
            "M_star": M_STAR,
        },
    }


def lemma_matching_H() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "matching_supported_H_le_floor_le_H2",
        "statement": (
            f"|H_M| ≤ ⌊n/e⌋ = {FLOOR_N_OVER_E} ≤ H2 for matching-supported highs "
            f"(v33 FM). N_side on H_M ≤ 930·{FLOOR_N_OVER_E} = {930 * FLOOR_N_OVER_E} ≪ e·p. "
            "M-cell card-closes; residual R-cell/H_over still needs C1–C5."
        ),
        "proof": ["v33 first-match high matching size ≤⌊n/e⌋."],
    }


def lemma_envelopes() -> dict[str, Any]:
    return {
        "status": "PROVED_ARITHMETIC",
        "name": "H2_envelope_arithmetic_and_refutations",
        "statement": (
            "Arithmetic: 31n, pack·n, n'·16, A·e, 31·p, K_cap·e are all ≤ H2. "
            "If |H| were ≤ any of these, Gate B would close under M_pad≤2. "
            "Ambient free-1 multipad REFUTES |H|≤31n, |H|≤n⌊n/e⌋, |H|≤31p, "
            "|H|≤pack·n on multiple (n,e) (e.g. n=72,e=3,|H|=5329)."
        ),
        "envelopes_le_H2": {
            "31_n": ENV_31_N,
            "pack_n": ENV_PACK_N,
            "nprime_16": ENV_NPRIME_16,
            "A_e": ENV_A_E,
            "31_p": ENV_31_P,
            "Kcap_e": ENV_KCAP_E,
            "H2": H2,
        },
        "refuted_as_theorems": [
            "|H|≤31n",
            "|H|≤n·⌊n/e⌋",
            "|H|≤31p",
            "|H|≤pack·n",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_max_N_ord_or_H_le_H2",
        "statement": (
            f"(1) max_z N_ord(z) ≤ e·p  (strongest; v19 C1)\n"
            f"(2) |H_A_SP| ≤ H2={H2}  (with M_pad≤2 residual)\n"
            f"(3) M ≤ M_*={M_STAR} active free-1 e-sets\n"
            "Crude ambient envelopes that fit under H2 are false as theorems. "
            "Matching-supported part is already ≤31; residual is the wall."
        ),
    }


def free1_degree_on_domain(p: int, n: int, e: int) -> dict[str, Any]:
    """Max free-1 ordered mates per e-set on full domain of size n."""
    vals = domain_vals(p, n)
    by_high: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), e):
        U = frozenset(exps)
        high, c0 = free1_high_c0(U, vals, p)
        by_high[high].append((U, c0))
    max_deg = 0
    nH = 0
    N_side = 0
    M = 0
    for h, us in by_high.items():
        if len(us) < 2:
            continue
        nH += 1
        f = len(us)
        M += f
        max_deg = max(max_deg, f - 1)
        N_side += f * (f - 1)
        # disjointness
        pts: list[int] = []
        for U, _ in us:
            pts.extend(U)
        ensure(len(pts) == len(set(pts)), "disj family")
    floor_ne = n // e
    ensure(max_deg <= max(floor_ne - 1, 0), f"deg {max_deg} > floor-1")
    return {
        "p": p,
        "n": n,
        "e": e,
        "nH": nH,
        "M": M,
        "N_side": N_side,
        "max_deg": max_deg,
        "floor_ne": floor_ne,
        "deg_le_floor_m1": max_deg <= max(floor_ne - 1, 0),
        "H_le_H2": nH <= H2,
        "H_gt_Kcap": nH > K_CAP,
        "H_le_31n": nH <= 31 * n,
        "H_le_n_floor": nH <= n * floor_ne,
        "H_le_31p": nH <= 31 * p,
        "H_le_pack_n": nH <= PACK * n,
    }


def asp_census(p: int, n: int, j: int, w: int) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 50000:
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
    N_ord = 0
    A_SP = 0
    P_multi = 0
    unique_fp: set = set()
    max_H_fib = 0
    M_active = 0

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
            if k < 2:
                continue
            P_multi += 1
            A_SP += k
            N_ord += k * (k - 1)
            for ut, (c0U, high) in by_u.items():
                fib_H.add(high)
                if ut not in seen[high]:
                    seen[high].add(ut)
                    high_Us[high].append(frozenset(ut))
                    M_active += 1
            items = list(by_u.items())
            for i, (ut, (c0U, _)) in enumerate(items):
                for j2, (vt, (c0V, _)) in enumerate(items):
                    if i == j2 or c0U == c0V:
                        continue
                    unique_fp.add((ut, vt))
        max_H_fib = max(max_H_fib, len(fib_H))

    nH = len(high_Us)
    N_side = len(unique_fp)
    floor_ne = max(n // e, 1)

    # matching-supported bound: greedy matching of active U's
    all_U = []
    for h, us in high_Us.items():
        for U in us:
            all_U.append(U)
    free = set(range(n))
    matched = 0
    H_matched: set = set()
    # match by scanning highs
    for h, us in sorted(high_Us.items(), key=lambda kv: repr(kv[0])):
        for U in us:
            if set(U).issubset(free):
                free -= set(U)
                matched += 1
                H_matched.add(h)
                break
    ensure(matched <= floor_ne, "matching size")
    ensure(len(H_matched) <= floor_ne, "H_M size")

    ensure(A_SP <= N_ord or N_ord == 0, "A le Nord")
    # N_ord can exceed N_side when multipads recount (U,V) under different cores.
    # Deployed Δ=16; toys may have larger local pencil degree — record only.
    nord_le_16 = (N_ord <= 16 * A_SP) if A_SP else True

    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "free_core": free_core,
        "nH": nH,
        "M_active": M_active,
        "N_side": N_side,
        "N_ord": N_ord,
        "A_SP": A_SP,
        "P_multi": P_multi,
        "max_H_fib": max_H_fib,
        "n_H_M": len(H_matched),
        "matching_size": matched,
        "H_M_le_floor": len(H_matched) <= floor_ne,
        "A_SP_le_N_ord": A_SP <= N_ord,
        "N_ord_le_16_ASP": nord_le_16,
        "H_le_H2": nH <= H2,
        "H_le_Kcap": nH <= K_CAP,
        "N_ord_le_ep_dep": N_ord <= E_P,
        "M_le_Mstar": M_active <= M_STAR,
        "N_side_le_30M": N_side <= max(floor_ne - 1, 0) * M_active if floor_ne > 1 else True,
    }


def toy_suite() -> dict[str, Any]:
    # arithmetic
    ensure(N_PRIME == A + E, "n'")
    ensure(N_PRIME // E == PACK, "floor n'/e = pack")
    ensure(DEG_COMP == 16, "deg")
    ensure(PACK == 17, "pack")
    ensure(H2 == E_P // (2 * PAIRS_PER_HIGH), "H2")
    ensure(ENV_31_N <= H2, "31n")
    ensure(ENV_PACK_N <= H2, "pack n")
    ensure(ENV_NPRIME_16 <= H2, "n'16")
    ensure(ENV_A_E <= H2, "Ae")
    ensure(ENV_31_P <= H2, "31p")
    ensure(ENV_KCAP_E <= H2, "Kcap e")
    ensure(M_STAR == E_P // 30, "M*")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")
    ensure(K_CAP < H2, "Kcap < H2")

    # ambient free-1 degree + envelope refutations
    amb = []
    for p, n, e in [
        (17, 16, 2),
        (17, 16, 3),
        (31, 30, 2),
        (31, 30, 3),
        (71, 70, 3),
        (73, 72, 3),
    ]:
        r = free1_degree_on_domain(p, n, e)
        amb.append(r)
        ensure(r["deg_le_floor_m1"], "deg bound")
        ensure(r["H_le_H2"], "amb under H2")
    ensure(any(not r["H_le_31n"] for r in amb), "refute 31n")
    ensure(any(not r["H_le_n_floor"] for r in amb), "refute n*floor")
    ensure(any(not r["H_le_31p"] for r in amb), "refute 31p")
    ensure(any(not r["H_le_pack_n"] for r in amb), "refute pack n")
    ensure(any(r["H_gt_Kcap"] for r in amb), "over Kcap")

    # A_SP prefix
    asp = []
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
        (17, 16, 9, 3),
        (19, 18, 6, 2),
        (19, 18, 7, 2),
        (19, 18, 8, 2),
        (31, 30, 4, 2),
        (31, 30, 5, 1),
    ]:
        r = asp_census(p, n, j, w)
        if r is None or r["nH"] == 0:
            continue
        ensure(r["H_M_le_floor"], "HM")
        ensure(r["A_SP_le_N_ord"], "A Nord")
        ensure(r["N_ord_le_ep_dep"], "Nord toy")
        ensure(r["H_le_H2"], "H H2")
        ensure(r["N_side_le_30M"], "30M")
        asp.append(r)

    ensure(len(asp) >= 10, "asp rows")
    # free_core trend: among e fixed, larger fc -> smaller nH often
    # just record max nH by fc
    by_fc: dict[int, list[int]] = defaultdict(list)
    for r in asp:
        by_fc[r["free_core"]].append(r["nH"])

    return {
        "status": "PASS",
        "ambient_rows": amb,
        "asp_rows": asp,
        "census": {
            "n_amb": len(amb),
            "n_asp": len(asp),
            "max_amb_H": max(r["nH"] for r in amb),
            "max_amb_deg": max(r["max_deg"] for r in amb),
            "max_asp_H": max(r["nH"] for r in asp),
            "max_asp_N_ord": max(r["N_ord"] for r in asp),
            "max_asp_HM": max(r["n_H_M"] for r in asp),
            "all_HM_le_floor": True,
            "refuted_envelopes": True,
            "by_fc_max_H": {str(k): max(v) for k, v in sorted(by_fc.items())},
        },
        "arithmetic": {
            "DEG_COMP": DEG_COMP,
            "N_PRIME": N_PRIME,
            "H2": H2,
            "M_STAR": M_STAR,
            "ENV_31_N": ENV_31_N,
            "ENV_A_E": ENV_A_E,
            "ENV_31_P": ENV_31_P,
            "e_p_over_16": E_P // 16,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v43",
        "title": "N_ord / |H|≤H2 at deployed free_core — degree 16 + criteria",
        "status": "PARTIAL_NORD_H2_CRITERIA",
        "claims": {
            "proves_complement_degree_16": True,
            "proves_Nord_ASP_factor16": True,
            "proves_card_criteria_C1_to_C5": True,
            "proves_matching_H_le_31_le_H2": True,
            "proves_H2_envelope_arithmetic": True,
            "refutes_ambient_H_le_31n_etc": True,
            "proves_deployed_max_Nord_le_ep": False,
            "proves_deployed_H_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "n_prime": N_PRIME,
            "deg_comp": DEG_COMP,
            "pack": PACK,
            "H2": H2,
            "H1": H1,
            "H17": H17,
            "M_star": M_STAR,
            "K_cap": K_CAP,
            "e_p": E_P,
            "e_p_over_16": E_P // 16,
            "e_p_over_17": E_P // PACK,
            "envelopes_le_H2": {
                "31_n": ENV_31_N,
                "pack_n": ENV_PACK_N,
                "nprime_16": ENV_NPRIME_16,
                "A_e": ENV_A_E,
                "31_p": ENV_31_P,
                "Kcap_e": ENV_KCAP_E,
            },
        },
        "lemmas": {
            "comp_degree": lemma_comp_degree(),
            "Nord_sandwich": lemma_Nord_sandwich(),
            "card_criteria": lemma_card_criteria(),
            "matching_H": lemma_matching_H(),
            "envelopes": lemma_envelopes(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "M_cell": "matching-supported highs ≤31 — card closed for M-cell",
            "residual": "need max N_ord≤e·p or |H_R|≤H2 (or M≤M_*)",
            "not_Kcap": "H2≃7.7e10 is the card high gate, not 2170",
            "next": "prove one of C1–C5 at deployed free_core for residual A_SP",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    amb = cert["toy_suite"]["ambient_rows"]
    asp = cert["toy_suite"]["asp_rows"]
    amb_tbl = "\n".join(
        f"| {r['n']} | {r['e']} | {r['nH']} | {r['max_deg']} | {r['floor_ne']-1} | "
        f"{r['H_gt_Kcap']} | {r['H_le_31n']} | {r['H_le_31p']} | {r['H_le_pack_n']} |"
        for r in amb
    )
    asp_tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['nH']} | {r['n_H_M']} | "
        f"{r['N_ord']} | {r['A_SP']} | {r['N_ord_le_16_ASP']} | {r['H_M_le_floor']} |"
        for r in asp
    )
    fc_line = ", ".join(f"fc={k}:maxH={v}" for k, v in cen["by_fc_max_H"].items())
    return f"""# KB-MCA Route-D v43: N_ord / |H|≤H2 at deployed free_core

Status: `PARTIAL` — **complement free-1 degree 16** PROVED; **card criteria
C1–C5** PROVED; **H_M≤31≤H2** PROVED; ambient H2-envelope candidates that
look attractive **REFUTED** as theorems; deployed max N_ord≤e·p / |H|≤H2 **OPEN**.

## Deployed complement degree (PROVED)

```text
n' = A + e = {d['n_prime']}
⌊n'/e⌋ = {d['pack']} = pack_ceil
deg_max free-1 CS mates per e-set in Ω  =  ⌊n'/e⌋ − 1  = {d['deg_comp']}
```

Every A_SP top-seam pair is a free-1 CS pair in some D\\C (v19).

## N_ord ↔ |A_SP| (PROVED)

```text
|A_SP|  ≤  N_ord  ≤  16 · |A_SP|
```

## Card criteria for |A_SP|≤t·p (PROVED conditional)

| ID | Gate | Deployed number |
|---|---|---|
| C1 | max N_ord ≤ e·p | e·p = {d['e_p']} |
| C2 | max |A_SP| ≤ e·p/16 | {d['e_p_over_16']} |
| C3 | max P_multi ≤ e·p/17 | {d['e_p_over_17']} |
| C4 | M_pad≤2 and |H| ≤ H2 | H2 = {d['H2']} |
| C5 | active free-1 e-sets M ≤ M_* | M_* = {d['M_star']} |

**Not** K_cap=2170 — that is multi-tier only (v41–v42).

## Matching-supported (PROVED)

```text
|H_M| ≤ ⌊n/e⌋ = 31 ≤ H2
N_side(H_M) ≤ 930 · 31 ≪ e·p
```

M-cell card-closes. Residual unmatched highs / R-cell is the wall.

## H2 envelopes (arithmetic vs theorems)

≤ H2 as numbers: `31n`, `pack·n`, `n'·16`, `A·e`, `31·p`, `K_cap·e`.

**Ambient free-1 REFUTES** as theorems: `|H|≤31n`, `|H|≤n⌊n/e⌋`, `|H|≤31p`,
`|H|≤pack·n` (e.g. n=72,e=3,|H|=5329).

## Ambient free-1 toys

| n | e | #H | max deg | floor−1 | >Kcap? | ≤31n? | ≤31p? | ≤pack·n? |
|---|---:|---:|---:|---:|---|---|---|---|
{amb_tbl}

## A_SP-prefix toys

| j | w | free_core | #H | #H_M | N_ord | A_SP | Nord≤16A? | H_M≤floor? |
|---|---|---:|---:|---:|---:|---:|---|---|
{asp_tbl}

By free_core (max |H|): {fc_line}

## Path

```text
M-cell (H_M≤31)     card CLOSED
R-cell / ambient H  need C1 or C4 (|H|≤H2) or C5
K_cap=2170          multi-tier only — not the card wall
```

## OPEN

1. `max N_ord ≤ e·p` at deployed free_core
2. `|H_A_SP| ≤ H2` (or residual |H_R|≤H2)
3. `M ≤ M_*` active free-1 e-sets

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v43.py --check
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
        "# kb-qatom-route-d-v43\n\n"
        "N_ord / |H|≤H2 criteria at deployed free_core; degree 16; envelope refutations.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v43 report\n\nstatus: {cert['status']}\n"
        f"complement degree 16: PROVED\n"
        f"H2 criteria: PROVED conditional\n"
        f"deployed max Nord / H le H2: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    ar = cert["toy_suite"]["arithmetic"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  complement free-1 deg ≤ {ar['DEG_COMP']} on n'={ar['N_PRIME']}: PROVED")
    print(f"  card criteria C1–C5 (H2={ar['H2']}, M_*={ar['M_STAR']}): PROVED")
    print("  matching H_M ≤ 31 ≤ H2: PROVED")
    print("  ambient envelopes 31n/31p/pack·n: REFUTED as theorems")
    print(
        f"  toys: max amb H={cen['max_amb_H']} deg={cen['max_amb_deg']}; "
        f"max asp H={cen['max_asp_H']} N_ord={cen['max_asp_N_ord']} H_M={cen['max_asp_HM']}"
    )


if __name__ == "__main__":
    main()
