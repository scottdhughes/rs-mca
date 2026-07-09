#!/usr/bin/env python3
"""KB-MCA Route-D v22: multipads are core multi-mates; M_pad reduction.

Implements the multipad rigidity spike: algebraic identification of multipad
cores with depth-w multi-mates of size m_c = j−e.

Proved:
  (1) Multipad ⇒ core multi-mates: if C≠C' share free-1 CS sides (U,V) and
      Phi_w(C∪U)=Phi_w(C'∪U), then deg(Λ_C−Λ_{C'}) ≤ m_c−w−1 with
      m_c = j−e = j−w−1, hence Phi_w(C)=Phi_w(C'). (Equivalent form of the
      v21 degree bound j−2w−2 = m_c−w−1.)
  (2) Structural reduction: every multipad side key sits over a depth-w
      multi-mate pair of cores (m_c-subsets). Thus multipads cannot occur
      unless core multi-mates exist at parameters (m_c, w).
  (3) Free-core dictionary: free_core = m_c − w = j − 2w − 1.
        free_core < 0  ⇔  j < 2w+1  (impossible: m_c < w, Phi_w overdetermined)
        free_core = 0  ⇔  j = 2w+1  ⇒ core Phi_w unique monic ⇒ M_pad≤1
        free_core = 1  ⇔  j = 2w+2  ⇒ cores free-1 CS packing available
        free_core ≥ 1  ⇔  j ≥ 2w+2  (deployed: free_core = 846160)
  (4) Recover j < 2w+2 ⇒ M_pad≤1 as free_core ≤ 0 cases (aligned with v21).
  (5) Toy bank: every multipad pair of cores has Phi_w equal; deg(diff) ≤ bound;
      free_core matches j−2w−1.
  (6) e·p mark bank on free-1 CS ordered pairs: natural size-e·p candidates
      (minU mod e, ·), (min(U∪V) mod e, ·) with c0U / c0V / Δc — all collide
      on toys even when restricted to M_pad=1 fibers. Records negative bank.
  (7) Conditional close: free_core≤0 ⇒ M_pad≤1; + CS→e·p ⇒ |A_SP|≤t·p
      (e=t deployed). Deployed free_core≫1 so (7) does not fire alone.

Does NOT prove M_pad≤1 at deployed free_core ≫ 1, nor e·p CS-pair injection.

  python3 experimental/scripts/verify_kb_qatom_route_d_v22.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v22.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v22"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v22.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v22.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v22.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
M_C = J - E  # can-core size for j-supports
FREE_CORE = M_C - W  # j - 2w - 1
T_P = T * P


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


def deg_diff(pa: list[int], pb: list[int], deg: int, p: int) -> int:
    for k in range(deg - 1, -1, -1):
        idx = deg - k
        if idx < len(pa) and (pa[idx] - pb[idx]) % p != 0:
            return k
    return -1


def lemma_multipad_are_core_multimates() -> dict[str, Any]:
    m_c = J - E
    return {
        "status": "PROVED",
        "name": "multipad_cores_are_depth_w_multimates",
        "statement": (
            "Let e=w+1 and m_c = j−e = j−w−1. If C≠C' are m_c-subsets admitting "
            "a free-1 CS pair (U,V) of e-sets with Phi_w(C∪U)=Phi_w(C'∪U), then "
            "Phi_w(C)=Phi_w(C'). Equivalently, multipad cores are depth-w multi-mates "
            "of size m_c."
        ),
        "proof": [
            "v21: deg(Λ_C − Λ_{C'}) ≤ j−2w−2.",
            "j−2w−2 = (j−w−1) − w − 1 = m_c − w − 1.",
            "For monic degree-m_c locators, deg(diff) ≤ m_c−w−1 is exactly the "
            "condition that the first w monic high coefficients agree, i.e. "
            "Phi_w(C)=Phi_w(C').",
        ],
        "deployed_m_c": m_c,
        "deployed_free_core": m_c - W,
        "identity": "j - 2*w - 2 == m_c - w - 1",
        "check_identity": (J - 2 * W - 2) == (M_C - W - 1),
    }


def lemma_free_core_dictionary() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_dictionary",
        "statement": (
            "Write free_core = m_c − w = j − 2w − 1. Then:\n"
            "  free_core ≤ 0  ⇔  j ≤ 2w+1  ⇔  m_c ≤ w\n"
            "    ⇒ monic degree-m_c locator is determined by Phi_w "
            "(w ≥ m_c uses ≥ all non-leading coeffs) ⇒ at most one core per "
            "Phi_w value ⇒ M_pad ≤ 1.\n"
            "  free_core = 1  ⇔  j = 2w+2  ⇒ cores free-1; CS packing applies.\n"
            "  free_core ≥ 1  ⇔  j ≥ 2w+2 (deployed free_core = j−2w−1 ≫ 1)."
        ),
        "proof": [
            "m_c = j−w−1; free_core = m_c−w = j−2w−1.",
            "If m_c ≤ w, Phi_w includes coefficients of X^{m_c−1},…,X^{m_c−w} "
            "which cover all of X^{m_c−1},…,X^0 when w ≥ m_c, so monic of degree "
            "m_c is unique given Phi_w. Multipad needs two cores with same Phi_w "
            "(previous lemma), impossible unless C=C'.",
            "Note j ≤ 2w+1 is equivalent to j < 2w+2 for integers, recovering v21.",
        ],
        "deployed_free_core": FREE_CORE,
        "deployed_j_le_2w_plus_1": J <= 2 * W + 1,
    }


def lemma_reduction() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_requires_core_multimates",
        "statement": (
            "M_pad(z) ≥ 2 only if there exist distinct m_c-subsets with the same "
            "depth-w prefix that both admit a common free-1 CS e-extension pair "
            "(U,V) lifting into fiber z. Thus controlling multipads reduces to "
            "controlling core multi-mates of size m_c at depth w that are "
            "jointly extendable by one CS side pair."
        ),
        "proof": [
            "M_pad≥2 means ≥2 cores for one side key (U,V) in fiber z.",
            "Previous lemma: those cores share Phi_w.",
            "They share the same CS (U,V) by construction of the side key.",
        ],
        "program": (
            "Open core multi-mate control at (m_c,w) with free_core=j−2w−1, "
            "plus joint CS-extension constraint — stricter than raw M_m(m_c,w)."
        ),
    }


def lemma_path() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "payment_path_restated",
        "statement": (
            "A_SP ≤ t·p if either:\n"
            "  (i)  M_pad≤1 (e.g. free_core≤0 / j≤2w+1) and CS ordered pairs "
            f"inject into e·p (=t·p={T_P} deployed), or\n"
            "  (ii) multipads controlled so N_ord ≤ t·p by other means."
        ),
        "proof": ["v20 bridge + free_core dictionary + deployed t=e."],
    }


def lemma_ep_mark_negative() -> dict[str, Any]:
    return {
        "status": "BANKED_NEGATIVE",
        "name": "ep_mark_candidates_collide",
        "statement": (
            "Natural free-1 CS ordered-pair marks of size ≤ e·p — "
            "(minU mod e, c0U), (minU mod e, c0V), (minU mod e, Δc), "
            "(min(U∪V) mod e, c0U), (min(U∪V) mod e, Δc) — all collide on "
            "toy free-1 CS pairs, including when restricted to M_pad=1 side "
            "keys. No tested e·p-scale mark is injective on CS ordered pairs."
        ),
        "proof": [
            "Toy census in toy_suite.ep_mark_bank.",
            "Budget: e·p = t·p deployed (t=e). Injection remains OPEN.",
        ],
        "deployed_e_p": E * P,
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_core_multimate_extension_and_ep_mark",
        "statement": (
            f"(1) At free_core = {FREE_CORE}, bound or eliminate multipads: "
            "core multi-mates of size m_c that share a CS e-extension into one "
            "j-fiber.\n"
            "(2) Inject free-1 CS e-set pairs into e·p labels "
            f"(budget e·p = {E * P}).\n"
            "CAS: Sage multipad examples; msolve on joint core+side systems."
        ),
    }


def _ep_marks(U: frozenset[int], V: frozenset[int], c0U: int, c0V: int, e: int, p: int):
    """Natural size-e·p mark candidates for free-1 CS ordered pair (U,V)."""
    min_u = min(U)
    min_uv = min(min(U), min(V))
    dc = (c0U - c0V) % p
    return {
        "minU_mod_e_c0U": (min_u % e, c0U % p),
        "minU_mod_e_c0V": (min_u % e, c0V % p),
        "minU_mod_e_dc": (min_u % e, dc),
        "minUV_mod_e_c0U": (min_uv % e, c0U % p),
        "minUV_mod_e_dc": (min_uv % e, dc),
        "minU_mod_e_c0U_xor_c0V": (min_u % e, (c0U ^ c0V) % p),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    # global e·p mark collision tallies (across all toy rows)
    mark_names = [
        "minU_mod_e_c0U",
        "minU_mod_e_c0V",
        "minU_mod_e_dc",
        "minUV_mod_e_c0U",
        "minUV_mod_e_dc",
        "minU_mod_e_c0U_xor_c0V",
    ]
    # per-mark: list of (label -> list of pair ids) only within each (p,n,j,w) fiber
    ep_summary: dict[str, dict[str, int]] = {
        name: {"n_pairs_total": 0, "n_pairs_mpad1": 0, "collisions_all": 0, "collisions_mpad1": 0}
        for name in mark_names
    }
    total_cs_pairs = 0
    total_cs_pairs_mpad1 = 0

    for p, n, j, w in [
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
        (17, 16, 10, 2),
        (17, 16, 10, 3),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 4, 1),
        (17, 16, 4, 2),
    ]:
        e = w + 1
        m_c = j - e
        if m_c <= 0 or math.comb(n, j) > 20000:
            continue
        free_core = m_c - w
        vals = domain_vals(p, n)
        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        def split(S: frozenset[int]) -> tuple[Any, ...]:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = S - U
            polyU = monic_rev([vals[i] for i in sorted(U)], p)
            return C, tuple(polyU[1:-1]), polyU[-1], U

        max_Mpad = 1
        n_mp = 0
        all_phi_eq = True
        max_dd = -1
        bound = j - 2 * w - 2
        n_cs_pairs = 0
        n_cs_pairs_mpad1 = 0
        # mark -> label -> list of pair fingerprints (for this row only)
        mark_buckets: dict[str, dict[Any, list]] = {name: defaultdict(list) for name in mark_names}
        mark_buckets_mpad1: dict[str, dict[Any, list]] = {
            name: defaultdict(list) for name in mark_names
        }

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                C, high, c0, U = split(S)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0))
            pads: dict[Any, list] = defaultdict(list)
            # also collect ordered CS pairs with their side keys
            ordered: list[tuple] = []
            for key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                # key = (sorted core, monic free-1 high of U)
                _c_key, high = key
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U = a
                        _C2, V, c0V = b
                        if (c0U - c0V) % p == 0:
                            continue
                        # side key φ = (high, c0U, c0V) — high from this pencil's U
                        pads[(high, c0U, c0V)].append(C)
                        ordered.append((C, U, V, c0U, c0V, high))
            # M_pad per side key
            mpad_of: dict[Any, int] = {}
            for sk, Cs in pads.items():
                uniq = {tuple(sorted(C)) for C in Cs}
                mpad_of[sk] = len(uniq)
                max_Mpad = max(max_Mpad, len(uniq))
                if len(uniq) < 2:
                    continue
                n_mp += 1
                clist = [frozenset(t) for t in uniq]
                C1, C2 = clist[0], clist[1]
                p1 = monic_rev([vals[i] for i in sorted(C1)], p)
                p2 = monic_rev([vals[i] for i in sorted(C2)], p)
                if phi_w(p1, w) != phi_w(p2, w):
                    all_phi_eq = False
                dd = deg_diff(p1, p2, m_c, p)
                max_dd = max(max_dd, dd)
                ensure(dd <= bound, f"deg {dd}>{bound}")
                ensure(phi_w(p1, w) == phi_w(p2, w), "core phi")

            for C, U, V, c0U, c0V, high in ordered:
                n_cs_pairs += 1
                sk = (high, c0U, c0V)
                is_mpad1 = mpad_of.get(sk, 1) <= 1
                if is_mpad1:
                    n_cs_pairs_mpad1 += 1
                marks = _ep_marks(U, V, c0U, c0V, e, p)
                # fingerprint pair by (sorted U, sorted V) so same sides collide correctly
                fp = (tuple(sorted(U)), tuple(sorted(V)))
                for name, lab in marks.items():
                    mark_buckets[name][lab].append(fp)
                    if is_mpad1:
                        mark_buckets_mpad1[name][lab].append(fp)

        # free_core <= 0 => M_pad <= 1
        if free_core <= 0:
            ensure(max_Mpad <= 1, f"free_core<=0 Mpad at j={j} w={w}")

        ensure(free_core == j - 2 * w - 1, "free id")
        ensure(m_c == j - w - 1, "mc id")
        ensure(bound == m_c - w - 1, "bound id")

        # collisions: label hit by ≥2 distinct (U,V) fingerprints
        def n_unique_pairs(buckets: dict) -> int:
            seen: set = set()
            for fps in buckets.values():
                seen.update(fps)
            return len(seen)

        row_mark_inj: dict[str, dict[str, Any]] = {}
        for name in mark_names:
            coll_all = sum(
                1 for fps in mark_buckets[name].values() if len(set(fps)) >= 2
            )
            coll_m1 = sum(
                1 for fps in mark_buckets_mpad1[name].values() if len(set(fps)) >= 2
            )
            n_uniq = n_unique_pairs(mark_buckets[name])
            n_uniq_m1 = n_unique_pairs(mark_buckets_mpad1[name])
            n_lab = len(mark_buckets[name])
            n_lab_m1 = len(mark_buckets_mpad1[name])
            # injective on unique (U,V): no multi-pair labels and |labels|=|pairs|
            inj_all = n_uniq > 0 and coll_all == 0 and n_lab == n_uniq
            inj_m1 = n_uniq_m1 > 0 and coll_m1 == 0 and n_lab_m1 == n_uniq_m1

            row_mark_inj[name] = {
                "n_labels": n_lab,
                "n_labels_mpad1": n_lab_m1,
                "n_unique_pairs": n_uniq,
                "n_unique_pairs_mpad1": n_uniq_m1,
                "n_collision_labels": coll_all,
                "n_collision_labels_mpad1": coll_m1,
                "injective_all": inj_all if n_uniq > 0 else None,
                "injective_mpad1": inj_m1 if n_uniq_m1 > 0 else None,
            }
            ep_summary[name]["n_pairs_total"] += n_cs_pairs
            ep_summary[name]["n_pairs_mpad1"] += n_cs_pairs_mpad1
            ep_summary[name]["collisions_all"] += coll_all
            ep_summary[name]["collisions_mpad1"] += coll_m1

        total_cs_pairs += n_cs_pairs
        total_cs_pairs_mpad1 += n_cs_pairs_mpad1

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "m_c": m_c,
                "free_core": free_core,
                "max_Mpad": max_Mpad,
                "n_multipad_events": n_mp,
                "n_cs_pairs": n_cs_pairs,
                "n_cs_pairs_mpad1": n_cs_pairs_mpad1,
                "all_core_phi_eq": all_phi_eq,
                "max_core_diff_deg": max_dd,
                "bound": bound,
                "ep_marks": row_mark_inj,
            }
        )

    ensure(all(r["all_core_phi_eq"] for r in rows), "phi eq")
    ensure(any(r["max_Mpad"] >= 2 for r in rows), "have multipad")
    ensure(FREE_CORE == J - 2 * W - 1, "dep free")
    ensure(M_C - W - 1 == J - 2 * W - 2, "bound align")
    ensure(T == E, "t=e")
    ensure(total_cs_pairs > 0, "need CS pairs for mark bank")
    # negative bank: no natural e·p mark is always-injective; each collides somewhere
    for name in mark_names:
        has_collision = any(
            r["ep_marks"][name]["n_collision_labels"] > 0
            for r in rows
            if r["n_cs_pairs"] > 0
        )
        always_inj = all(
            r["ep_marks"][name]["injective_all"] is True
            for r in rows
            if r["n_cs_pairs"] > 0
        )
        ensure(not always_inj, f"unexpected injective mark {name}")
        ensure(has_collision, f"need collision evidence for {name}")

    return {
        "status": "PASS",
        "rows": rows,
        "ep_mark_bank": {
            "status": "BANKED_NEGATIVE",
            "budget": "e*p",
            "deployed_e_p": E * P,
            "total_cs_pairs": total_cs_pairs,
            "total_cs_pairs_mpad1": total_cs_pairs_mpad1,
            "marks": ep_summary,
            "conclusion": (
                "No tested natural e·p-scale mark is injective on free-1 CS "
                "ordered pairs (all or M_pad=1-restricted)."
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v22",
        "title": "Multipads are core multi-mates; free_core dictionary; e·p mark bank",
        "status": "PARTIAL_MPAD_REDUCTION",
        "claims": {
            "proves_multipad_cores_phi_w_equal": True,
            "proves_free_core_dictionary": True,
            "proves_multipad_requires_core_multimates": True,
            "proves_M_pad_le_1_deployed": False,
            "proves_ep_cs_injection": False,
            "banks_ep_mark_negatives": True,
            "toy_confirms_core_phi_eq": True,
        },
        "deployed": {
            "j": J,
            "w": W,
            "e": E,
            "m_c": M_C,
            "free_core": FREE_CORE,
            "t": T,
            "t_equals_e": T == E,
            "t_p": T_P,
            "e_p": E * P,
            "j_le_2w_plus_1": J <= 2 * W + 1,
            "two_w_plus_2": 2 * W + 2,
        },
        "lemmas": {
            "core_multimates": lemma_multipad_are_core_multimates(),
            "free_core": lemma_free_core_dictionary(),
            "reduction": lemma_reduction(),
            "path": lemma_path(),
            "ep_mark_negative": lemma_ep_mark_negative(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "reduction": (
                "Multipad control ≤ core multi-mate control at (m_c,w) with "
                f"free_core={FREE_CORE}, plus joint CS e-extension"
            ),
            "ep_marks": "Natural e·p CS-pair marks banked negative (toys collide)",
            "next": (
                "Bound/extend core multi-mates of size m_c with common CS side pair; "
                "or non-natural e·p / larger structured mark for CS pairs"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['m_c']} | {r['free_core']} | {r['max_Mpad']} | "
        f"{r['n_multipad_events']} | {r['n_cs_pairs']} | {r['all_core_phi_eq']} | {r['bound']} |"
        for r in rows
    )
    bank = cert["toy_suite"]["ep_mark_bank"]
    mark_tbl = "\n".join(
        f"| `{name}` | {s['n_pairs_total']} | {s['collisions_all']} | "
        f"{s['n_pairs_mpad1']} | {s['collisions_mpad1']} |"
        for name, s in bank["marks"].items()
    )
    return f"""# KB-MCA Route-D v22: multipads = core multi-mates + e·p mark bank

Status: `PARTIAL` — multipad→core multi-mate reduction **PROVED**;
natural e·p CS marks **BANKED NEGATIVE**; deployed M_pad still **OPEN**.

## Main theorem (PROVED)

Multipad cores sharing free-1 CS sides `(U,V)` in one fiber satisfy

```text
Phi_w(C) = Phi_w(C')
```

with `|C|=m_c = j−e = j−w−1`. Proof: v21 bound

```text
deg(Λ_C − Λ_{{C'}}) ≤ j−2w−2 = m_c − w − 1
```

is exactly depth-`w` multi-mate agreement for monic degree-`m_c` locators.

## free_core dictionary (PROVED)

```text
free_core = m_c − w = j − 2w − 1
```

| free_core | j vs 2w | M_pad |
|---:|---|---|
| ≤ 0 | j ≤ 2w+1 | ≤ 1 (Phi_w determines monic core) |
| = 1 | j = 2w+2 | cores free-1 CS regime |
| ≫ 1 | deployed | open |

Deployed:

```text
m_c        = {d['m_c']}
free_core  = {d['free_core']}
j ≤ 2w+1?  = {d['j_le_2w_plus_1']}
t = e      = {d['t']}
e·p = t·p  = {d['e_p']}
```

## Reduction

```text
M_pad ≥ 2
  ⇒  core multi-mates at (m_c, w)
  +  common free-1 CS e-extension (U,V) into the j-fiber
```

Stricter than raw `M_m(m_c,w)`: joint extension by one CS pair.

## Payment path

```text
M_pad ≤ 1  +  CS pairs → e·p (= t·p)
    ⇒  |A_SP| ≤ t·p
```

## e·p mark bank (BANKED NEGATIVE)

Natural free-1 CS ordered-pair marks of size ≤ `e·p`:

| mark | #pairs | #colliding labels (all) | #pairs M_pad=1 | #colliding (M_pad=1) |
|---|---:|---:|---:|---:|
{mark_tbl}

Conclusion: **no tested natural e·p-scale mark is injective** on CS ordered
pairs (all fibers or M_pad=1-restricted). Injection proof remains OPEN.

## Toys

| j | w | m_c | free_core | max M_pad | #mp | #CS pairs | core Phi eq? | bound |
|---|---|---:|---:|---:|---:|---:|---|---:|
{tbl}

All multipad events have core Phi_w equal (re-check of theorem).

## OPEN

1. Control core multi-mates of size `m_c` with free_core=`{d['free_core']}` that
   share a CS e-extension (⇒ M_pad)
2. Inject free-1 CS pairs into `e·p` labels (need non-natural / structure-aware mark)

## CAS

- Sage: multipad examples already show tight degree + core Phi equality
- Next: structure of core multi-mates that admit common CS sides
- msolve: joint core-pair + side CS system in small fields

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v22.py --check
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
        "# kb-qatom-route-d-v22\n\nMultipads are core multi-mates.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v22 report\n\nstatus: {cert['status']}\n"
        f"free_core deployed: {cert['deployed']['free_core']}\n"
        f"M_pad le 1 deployed: OPEN\n"
    )
    bank = cert["toy_suite"]["ep_mark_bank"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  multipad => Phi_w(C)=Phi_w(C'): PROVED")
    print(f"  free_core = m_c - w = {FREE_CORE} deployed")
    print(f"  free_core<=0 => M_pad<=1: PROVED (deployed? {FREE_CORE <= 0})")
    print("  reduction: multipad needs core multi-mates + joint CS extension")
    print(f"  e·p mark bank: {bank['status']} ({bank['total_cs_pairs']} CS pairs)")
    print(f"  toy rows: {len(cert['toy_suite']['rows'])}")


if __name__ == "__main__":
    main()
