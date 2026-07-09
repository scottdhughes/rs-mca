#!/usr/bin/env python3
"""KB-MCA Route-D v23: free_core=1 multipads = free-1 CS cores + joint avoid.

Continues v22 multipad→core multi-mate reduction with the free_core stratification
and the joint CS-extension constraint.

Proved:
  (1) free_core dictionary restated: free_core = m_c − w = j − 2w − 1.
      Multipad cores are depth-w multi-mates: deg(Λ_C−Λ_{C'}) ≤ free_core−1.
  (2) free_core = 1 characterization: multipad cores are free-1 CS pairs of
      m_c-sets (same monic free-1 high, distinct constants). Proof: free_core=1
      ⇒ m_c = w+1 ⇒ Phi_w fixes all non-leading non-constant coeffs.
  (3) Fully-split monic recovery: a monic degree-e poly is determined by
      (high, c0) with |high|=e−1; fully split ⇒ unique root set. Thus side key
      φ=(high,c0U,c0V) determines a unique free-1 CS ordered pair (U,V).
  (4) Joint avoidance: if C and C' share multipad sides (U,V), then
      (U ∪ V) ∩ C = (U ∪ V) ∩ C' = ∅, i.e. U,V ⊆ D \\ (C ∪ C').
  (5) free_core ≤ 0 ⇒ M_pad ≤ 1 (recover v21/v22); free_core = 1 ⇒ multipads
      are free-1 CS core cliques jointly avoiding a common (U,V).
  (6) Toy bank: free_core=1 multipads always same core high + distinct c0;
      joint avoidance holds; free_core≤0 has no multipads; free_core≥2 multipads
      exist with deg(diff) ≤ free_core−1.

Does NOT prove M_pad≤1 at deployed free_core=846161, nor e·p CS-pair injection.

  python3 experimental/scripts/verify_kb_qatom_route_d_v23.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v23.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v23"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v23.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v23.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v23.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
M_C = J - E
FREE_CORE = M_C - W  # j - 2w - 1
T_P = T * P
E_P = E * P


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


def core_free1_high_c0(C: tuple[int, ...] | frozenset[int], vals: list[int], p: int, m_c: int):
    """For free_core=1 (m_c=w+1): free-1 high = all non-leading non-constant coeffs."""
    poly = monic_rev([vals[i] for i in sorted(C)], p)
    # poly[1:m_c] has length m_c-1 = w when m_c=w+1
    return tuple(poly[1:m_c]), poly[m_c]


def lemma_free1_characterization() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_1_multipads_are_free1_CS_cores",
        "statement": (
            "Suppose free_core = m_c − w = 1 (equivalently m_c = w+1, j = 2w+2). "
            "If C ≠ C' are multipad cores (share free-1 CS sides (U,V) in one "
            "j-fiber), then Λ_C and Λ_{C'} form a free-1 CS pair of monic "
            "degree-m_c locators: they share all monic free-1 high coefficients "
            "and have distinct constants. Equivalently multipad cores are free-1 "
            "CS m_c-sets that jointly avoid U ∪ V."
        ),
        "proof": [
            "v22: multipad cores satisfy Phi_w(C)=Phi_w(C').",
            "free_core=1 ⇒ m_c = w+1, so Phi_w = poly[1:w+1] = poly[1:m_c] "
            "covers every non-leading non-constant coefficient.",
            "Monic same degree + agreement on poly[1:m_c] ⇒ Λ_C − Λ_{C'} is "
            "constant. Distinct supports ⇒ constant ≠ 0 ⇒ free-1 CS.",
            "Joint avoidance: S=C⊔U and S'=C'⊔U force U∩C=U∩C'=∅; same for V.",
        ],
        "deployed_free_core": FREE_CORE,
        "deployed_is_free_core_1": FREE_CORE == 1,
    }


def lemma_monic_recovery() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "side_key_recovers_unique_UV",
        "statement": (
            "A monic degree-e polynomial over F_p is uniquely determined by "
            "(high, c0) with |high|=e−1 (all middle coeffs + constant). If it "
            "fully splits into distinct domain roots, the root set is unique. "
            "Hence φ=(high,c0U,c0V) recovers a unique free-1 CS ordered pair "
            "(U,V) among fully-split free-1 e-sets. Multipad fibers of φ are "
            "literally multi-cores over a single exact (U,V)."
        ),
        "proof": [
            "Degree-e monic has e free coefficients; high has e−1, plus c0.",
            "Unique monic ⇒ unique multiset of roots in algebraic closure; "
            "fully split into distinct F_p-domain roots ⇒ unique support set.",
            "v20 already used this for φ-injectivity when M_pad=1.",
        ],
    }


def lemma_joint_avoidance() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "joint_CS_extension_avoidance",
        "statement": (
            "If C ≠ C' share multipad sides (U,V), then "
            "(U ∪ V) ∩ C = (U ∪ V) ∩ C' = ∅. "
            "Equivalently U,V ⊆ D \\ (C ∪ C'). "
            "Thus multipad control ≤ multi-mate control of m_c-sets that admit "
            "a common free-1 CS e-pair in their common complement."
        ),
        "proof": [
            "Top-seam normal form: S=C⊔U, T=C⊔V with disjoint unions; same "
            "for C' with the same (U,V) (monic recovery).",
            "Disjointness is support-level, not merely monic.",
        ],
        "program": (
            "Filter multi-mates by common-complement CS-extendability — "
            "stricter than raw M_m(m_c,w)."
        ),
    }


def lemma_stratification() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_multipad_stratification",
        "statement": (
            "free_core = m_c − w = j − 2w − 1 stratifies multipad geometry:\n"
            "  free_core ≤ 0  ⇒  M_pad ≤ 1 (Phi_w determines monic core)\n"
            "  free_core = 1  ⇒  multipads are free-1 CS core cliques + joint avoid\n"
            "  free_core ≥ 2  ⇒  multipads are depth-w multi-mates with "
            "deg(diff) ≤ free_core−1 + joint avoid (open bound)"
        ),
        "proof": [
            "≤0: v21/v22 degree obstruction / free_core dictionary.",
            "=1: free-1 CS characterization above.",
            "≥2: v21 deg bound j−2w−2 = free_core−1; joint avoidance.",
        ],
        "deployed": {
            "free_core": FREE_CORE,
            "stratum": ">=2",
            "m_c": M_C,
            "w": W,
        },
    }


def lemma_path() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "payment_path_with_strata",
        "statement": (
            "A_SP ≤ t·p if M_pad≤1 and CS ordered pairs inject into e·p "
            f"(=t·p={T_P} deployed). At free_core=1, M_pad≤1 is equivalent to "
            "forbidding free-1 CS core pairs that jointly avoid a common (U,V) "
            "in one j-fiber — a CS-packing question at scale m_c."
        ),
        "proof": ["v20 bridge + free_core=1 characterization."],
        "deployed_note": (
            f"Deployed free_core={FREE_CORE} ≫ 1; free_core=1 packing reduction "
            "does not apply. Still need multi-mate control at free_core≫1 or "
            "structure-aware e·p marks."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_high_free_core_multimate_joint_extension",
        "statement": (
            f"(1) At free_core={FREE_CORE}, bound M_pad for depth-w multi-mates "
            f"of size m_c={M_C} that jointly avoid a free-1 CS e-pair.\n"
            "(2) Inject free-1 CS e-pairs into e·p (natural marks banked "
            "negative in v22).\n"
            "CAS: msolve/Sage on free_core=1 multipad ideal as model; lift "
            "obstructions to free_core≫1."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_fc1_events = 0
    n_fc1_same_high = 0
    n_joint_avoid_ok = 0
    n_joint_avoid_checked = 0
    n_mp_total = 0

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
        (17, 16, 10, 2),
        (17, 16, 10, 3),
    ]:
        e = w + 1
        m_c = j - e
        if m_c <= 0 or math.comb(n, j) > 20000:
            continue
        free_core = m_c - w
        bound = free_core - 1  # deg(Λ_C−Λ_C') ≤ free_core−1
        vals = domain_vals(p, n)
        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        max_Mpad = 1
        n_mp = 0
        max_dd = -1
        all_phi_eq = True
        all_fc1_free1 = True
        all_avoid = True
        n_fc1_row = 0

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                pU = monic_rev([vals[i] for i in sorted(U)], p)
                high = tuple(pU[1:-1])
                pencils[(tuple(sorted(C)), high)].append((C, U, pU[-1]))

            pads: dict[Any, list] = defaultdict(list)
            for key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                _ck, high = key
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U = a
                        _C2, V, c0V = b
                        if (c0U - c0V) % p == 0:
                            continue
                        # store exact supports — monic recovery says unique
                        pads[(high, c0U, c0V)].append((C, U, V))

            for _sk, items in pads.items():
                # unique cores with a representative (U,V)
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
                n_mp_total += 1
                cores = list(by_c.keys())
                # all cores must share same exact (U,V) by monic recovery + pad key
                UV0 = by_c[cores[0]]
                for t in cores:
                    ensure(by_c[t][0] == UV0[0] and by_c[t][1] == UV0[1], "UV monic recovery")
                U0, V0 = UV0

                # pairwise multipad checks
                for a, b in itertools.combinations(cores, 2):
                    C1, C2 = frozenset(a), frozenset(b)
                    p1 = monic_rev([vals[i] for i in sorted(C1)], p)
                    p2 = monic_rev([vals[i] for i in sorted(C2)], p)
                    if phi_w(p1, w) != phi_w(p2, w):
                        all_phi_eq = False
                    dd = deg_diff(p1, p2, m_c, p)
                    max_dd = max(max_dd, dd)
                    ensure(dd <= bound, f"deg {dd}>{bound} fc={free_core}")
                    ensure(phi_w(p1, w) == phi_w(p2, w), "core phi")

                    # joint avoidance
                    n_joint_avoid_checked += 1
                    ok = U0.isdisjoint(C1) and U0.isdisjoint(C2)
                    ok = ok and V0.isdisjoint(C1) and V0.isdisjoint(C2)
                    if ok:
                        n_joint_avoid_ok += 1
                    else:
                        all_avoid = False

                    # free_core=1 ⇒ free-1 CS cores
                    if free_core == 1:
                        n_fc1_events += 1
                        n_fc1_row += 1
                        h1, c1 = core_free1_high_c0(C1, vals, p, m_c)
                        h2, c2 = core_free1_high_c0(C2, vals, p, m_c)
                        if h1 == h2 and (c1 - c2) % p != 0:
                            n_fc1_same_high += 1
                        else:
                            all_fc1_free1 = False
                        ensure(h1 == h2, "fc1 same high")
                        ensure((c1 - c2) % p != 0, "fc1 distinct c0")
                        ensure(dd <= 0, "fc1 deg<=0")

        if free_core <= 0:
            ensure(max_Mpad <= 1, f"fc<=0 Mpad at j={j} w={w}")
        ensure(free_core == j - 2 * w - 1, "fc id")
        ensure(bound == m_c - w - 1, "bound id")
        ensure(bound == j - 2 * w - 2, "bound v21 id")

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
                "n_fc1_pair_checks": n_fc1_row,
                "all_core_phi_eq": all_phi_eq,
                "all_fc1_free1_CS": all_fc1_free1 if free_core == 1 else None,
                "all_joint_avoid": all_avoid if n_mp > 0 else None,
                "max_core_diff_deg": max_dd,
                "deg_bound": bound,
            }
        )

    ensure(all(r["all_core_phi_eq"] for r in rows), "phi eq")
    ensure(any(r["max_Mpad"] >= 2 for r in rows), "have multipad")
    ensure(any(r["free_core"] == 1 and r["max_Mpad"] >= 2 for r in rows), "fc1 multipad")
    ensure(any(r["free_core"] <= 0 and r["max_Mpad"] <= 1 for r in rows), "fc0 no multipad")
    ensure(any(r["free_core"] >= 2 and r["max_Mpad"] >= 2 for r in rows), "fc>=2 multipad")
    # free_core=1 characterization
    fc1_rows = [r for r in rows if r["free_core"] == 1 and r["n_multipad_events"] > 0]
    ensure(len(fc1_rows) >= 1, "need fc1 multipad rows")
    ensure(all(r["all_fc1_free1_CS"] for r in fc1_rows), "fc1 free1 CS")
    ensure(n_fc1_events > 0 and n_fc1_same_high == n_fc1_events, "fc1 all same high")
    ensure(n_joint_avoid_checked > 0 and n_joint_avoid_ok == n_joint_avoid_checked, "joint avoid")
    ensure(FREE_CORE == J - 2 * W - 1, "dep free")
    ensure(FREE_CORE == 846161, "dep free num")
    ensure(T == E, "t=e")
    ensure(FREE_CORE != 1, "deployed not fc1")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_multipad_events_total": n_mp_total,
            "n_fc1_pair_checks": n_fc1_events,
            "n_fc1_same_high": n_fc1_same_high,
            "n_joint_avoid_checked": n_joint_avoid_checked,
            "n_joint_avoid_ok": n_joint_avoid_ok,
            "fc1_characterization": "CONFIRMED",
            "joint_avoidance": "CONFIRMED",
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v23",
        "title": "free_core=1 multipads = free-1 CS cores + joint avoidance",
        "status": "PARTIAL_FC1_STRATUM",
        "claims": {
            "proves_free_core_1_are_free1_CS_cores": True,
            "proves_side_key_recovers_UV": True,
            "proves_joint_avoidance": True,
            "proves_free_core_stratification": True,
            "proves_M_pad_le_1_deployed": False,
            "proves_ep_cs_injection": False,
            "toy_confirms_fc1_and_avoidance": True,
        },
        "deployed": {
            "j": J,
            "w": W,
            "e": E,
            "m_c": M_C,
            "free_core": FREE_CORE,
            "free_core_stratum": ">=2",
            "t": T,
            "t_equals_e": T == E,
            "t_p": T_P,
            "e_p": E_P,
            "is_free_core_1": FREE_CORE == 1,
            "is_free_core_le_0": FREE_CORE <= 0,
        },
        "lemmas": {
            "free1_char": lemma_free1_characterization(),
            "monic_recovery": lemma_monic_recovery(),
            "joint_avoidance": lemma_joint_avoidance(),
            "stratification": lemma_stratification(),
            "path": lemma_path(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "win": (
                "free_core=1 multipads reduced to free-1 CS packing of cores "
                "with joint e-extension (same technology class as side CS)"
            ),
            "deployed": (
                f"free_core={FREE_CORE} ≥ 2 stratum — need multi-mate control "
                "with joint complement CS-extension, or e·p marks"
            ),
            "next": (
                "Attack free_core≫1 multi-mates via Newton/power-sum or residual "
                "split constraints; CAS model free_core=1 multipad ideal"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['m_c']} | {r['free_core']} | {r['max_Mpad']} | "
        f"{r['n_multipad_events']} | {r['all_fc1_free1_CS']} | {r['all_joint_avoid']} | "
        f"{r['deg_bound']} | {r['max_core_diff_deg']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v23: free_core=1 multipads = free-1 CS cores

Status: `PARTIAL` — free_core=1 stratum **PROVED** (free-1 CS cores + joint
avoidance); deployed free_core={d['free_core']} still **OPEN**.

## free_core stratification (PROVED)

```text
free_core = m_c − w = j − 2w − 1
```

| free_core | multipad geometry |
|---:|---|
| ≤ 0 | M_pad ≤ 1 (Phi_w determines monic core) |
| = 1 | free-1 CS core cliques + joint avoid (U,V) |
| ≥ 2 | depth-w multi-mates, deg(diff) ≤ free_core−1 + joint avoid |

Deployed:

```text
m_c         = {d['m_c']}
free_core   = {d['free_core']}   (stratum ≥ 2)
e·p = t·p   = {d['e_p']}
```

## Main theorem (PROVED): free_core = 1

If `free_core = 1` and `C ≠ C'` are multipad cores, then `Λ_C, Λ_{{C'}}` form a
**free-1 CS pair** of monic degree-`m_c` locators (same free-1 high, distinct
constants), and both jointly avoid the recovered sides `(U,V)`.

Proof: `m_c = w+1` ⇒ `Phi_w` fixes every non-leading non-constant coeff.

## Side-key recovery + joint avoidance (PROVED)

```text
φ = (high, c0U, c0V)  →  unique fully-split free-1 CS pair (U,V)
M_pad ≥ 2  ⇒  U,V ⊆ D \\ (C ∪ C')   for every multipad core pair
```

Multipad control ≤ multi-mate control of cores that admit a common free-1 CS
e-pair in their **common complement**.

## Payment path

```text
M_pad ≤ 1  +  CS pairs → e·p (= t·p)  ⇒  |A_SP| ≤ t·p
```

At free_core=1, forbidding multipads = forbidding free-1 CS core pairs with
joint e-extension (CS packing at scale `m_c`). Deployed free_core ≫ 1 so this
reduction does not fire.

## Toys

| j | w | m_c | free_core | max M_pad | #mp | fc1 free1 CS? | joint avoid? | deg bound | max dd |
|---|---|---:|---:|---:|---:|---|---|---:|---:|
{tbl}

Census: fc1 pair-checks={cen['n_fc1_pair_checks']} all same-high;
joint-avoid checks={cen['n_joint_avoid_checked']} all OK.

## OPEN

1. Bound/eliminate multipads at free_core=`{d['free_core']}` (depth-w multi-mates
   of size `m_c` with joint complement CS-extension)
2. Inject free-1 CS e-pairs into `e·p` (v22 natural marks banked negative)

## CAS

- Model free_core=1 multipad ideal (two monics free-1 CS cores × free-1 CS
  sides, fully split, joint avoid) in Sage/msolve
- Lift emptiness / degree obstructions toward free_core ≫ 1

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v23.py --check
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
        "# kb-qatom-route-d-v23\n\n"
        "free_core=1 multipads are free-1 CS cores + joint avoidance.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v23 report\n\nstatus: {cert['status']}\n"
        f"free_core deployed: {cert['deployed']['free_core']}\n"
        f"stratum: {cert['deployed']['free_core_stratum']}\n"
        f"fc1 characterization: PROVED\n"
        f"M_pad le 1 deployed: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free_core=1 multipads = free-1 CS cores: PROVED")
    print("  joint avoidance U,V ⊆ complement(C ∪ C'): PROVED")
    print("  side key recovers unique (U,V): PROVED")
    print(f"  deployed free_core = {FREE_CORE} (stratum ≥ 2)")
    print(f"  toys: {len(cert['toy_suite']['rows'])} rows, "
          f"fc1 checks={cen['n_fc1_pair_checks']}, "
          f"avoid checks={cen['n_joint_avoid_checked']}")


if __name__ == "__main__":
    main()
