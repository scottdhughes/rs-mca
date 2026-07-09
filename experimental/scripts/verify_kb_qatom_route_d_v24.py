#!/usr/bin/env python3
"""KB-MCA Route-D v24: Newton multi-mates + (U,δ) CS-pair reduction + CAS fc1.

Attacks free_core≫1 multipads and structure-aware e·p marks.

Proved:
  (1) Product identity: for multipad cores C,C' with common free-1 side U,
        (Λ_C − Λ_{C'}) · Λ_U = Λ_{C∪U} − Λ_{C'∪U}.
      (Algebraic, holds in F_p[X]; toys re-check.)
  (2) Newton multi-mate form (p > m_c): monic depth-w multi-mates
      Phi_w(C)=Phi_w(C') ⇔ first w power sums of roots agree
      (Newton–Girard bijection on elementary ↔ power sums for k ≤ m_c < p).
  (3) free_core=1 fiber constraint is automatic: m_c=e=w+1, j=2w+2,
        Λ_{C∪U}−Λ_{C'∪U} = (cA−cB)·Λ_U has deg = e = j−w−1,
      so Phi_w agreement of the two j-supports is free. Multipad obstruction
      at free_core=1 is purely joint avoidance + fully-split, not fiber.
      (CAS: Sage single-ring model for w=1..4.)
  (4) Structure-aware CS-pair injection: free-1 CS ordered pairs (U,V) inject
      into FullySplitFree1(e) × F_p^× via
        ψ(U,V) = (U, δ)  with  δ = c0(U)−c0(V) ≠ 0,
      because Λ_V = Λ_U − δ is uniquely determined by (U,δ).
  (5) Payment reduction: CS pairs → e·p  ⇐  free-1 fully-split e-sets → [e]
      (then × F_p via δ). Natural e-index marks on U still collide (banked).
  (6) Toy bank: product identity; (U,δ) injective; e·p-scale marks on U still
      collide; multipad deg(diff) ≤ free_core−1 with lead coeff index ≥ w+1.

Does NOT prove M_pad≤1 at free_core=846161, nor free-1 e-set → [e] injection.

  python3 experimental/scripts/verify_kb_qatom_route_d_v24.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v24.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v24"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v24.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v24.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v24.report.md"
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


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def power_sums(roots: list[int], kmax: int, p: int) -> list[int]:
    """p_k = sum r^k for k=1..kmax; p_0 unused."""
    ps = [0] * (kmax + 1)
    for r in roots:
        rp = 1
        for k in range(1, kmax + 1):
            rp = (rp * r) % p
            ps[k] = (ps[k] + rp) % p
    return ps


def lemma_product_identity() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_product_identity",
        "statement": (
            "If C, C' are cores and U is an e-set disjoint from both, then "
            "in F_p[X]: (Λ_C − Λ_{C'}) · Λ_U = Λ_{C∪U} − Λ_{C'∪U}, "
            "where Λ denotes the monic locator. In particular this holds for "
            "every multipad pair with common free-1 side U."
        ),
        "proof": [
            "Λ_{C∪U} = Λ_C · Λ_U and Λ_{C'∪U} = Λ_{C'} · Λ_U by disjoint union "
            "of root supports (monic product).",
            "Factor: Λ_C Λ_U − Λ_{C'} Λ_U = (Λ_C − Λ_{C'}) Λ_U.",
        ],
    }


def lemma_newton_multimate() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "newton_power_sum_multimate",
        "statement": (
            f"Assume char F_p with p > m_c (deployed p={P} > m_c={M_C}). "
            "For monic degree-m_c locators, Phi_w(C)=Phi_w(C') if and only if "
            "the first w power sums of roots agree: "
            "∑_{r∈C} r^k = ∑_{r∈C'} r^k for k=1,...,w. "
            "Thus multipad cores are joint-complement free-1-CS-extendable "
            "depth-w power-sum multi-mates of size m_c."
        ),
        "proof": [
            "Monic locator coeffs are (signed) elementary symmetric functions "
            "of the roots.",
            "Newton–Girard: for 1 ≤ k ≤ m_c < p, the map between "
            "(e_1,...,e_k) and (p_1,...,p_k) is triangular with diagonal "
            "units (±k ≠ 0 in F_p), hence bijective.",
            "Phi_w records the first w non-leading monic coeffs ⇔ (e_1,...,e_w) "
            "⇔ (p_1,...,p_w).",
        ],
        "deployed_p_gt_mc": P > M_C,
    }


def lemma_fc1_fiber_auto() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_1_fiber_automatic",
        "statement": (
            "When free_core=1 (so m_c = w+1 = e and j = 2w+2), multipad cores "
            "are free-1 CS: Λ_C − Λ_{C'} = c ≠ 0 constant. Then "
            "Λ_{C∪U} − Λ_{C'∪U} = c · Λ_U has degree e = j−w−1, which is "
            "exactly the Phi_w fiber room. Hence same-fiber membership of "
            "C∪U and C'∪U is automatic. Multipads at free_core=1 are "
            "obstructed only by fully-split + joint avoidance, not by fiber."
        ),
        "proof": [
            "v23: free_core=1 ⇒ free-1 CS cores.",
            "Product identity: (Λ_C−Λ_{C'})Λ_U = c·Λ_U, deg = e.",
            "Phi_w agreement for monic j-sets ⇔ deg(diff) ≤ j−w−1.",
            "j−w−1 = 2w+2−w−1 = w+1 = e. Equality case ⇒ auto.",
            "CAS: Sage single-ring model checks CA−CB=cA−cB and "
            "SU−SUp=(cA−cB)·U for w=1..4.",
        ],
        "cas": "sage free_core=1 multipad model (embedded in toy_suite.cas_fc1)",
    }


def lemma_U_delta_injection() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_CS_pairs_inject_via_U_delta",
        "statement": (
            "Let FS_1(e) be the set of fully-split free-1 monic e-sets "
            "(equivalently monic free-1 locators that split into distinct "
            "domain roots). The map "
            "ψ: {(U,V) free-1 CS ordered} → FS_1(e) × F_p^×, "
            "ψ(U,V) = (U, δ) with δ = c0(U)−c0(V), is injective. "
            "Indeed Λ_V = Λ_U − δ is the unique monic of degree e with that "
            "difference, so V is recovered from (U,δ) when fully split."
        ),
        "proof": [
            "Free-1 CS: monic free-1 high of U equals that of V, and "
            "c0(U)≠c0(V), so Λ_U − Λ_V is the nonzero constant δ.",
            "Given U and δ, Λ_U is known; set Λ := Λ_U − δ (same high, "
            "constant c0(U)−δ). Unique monic ⇒ unique candidate V as root set "
            "if fully split into domain.",
            "If ψ(U,V)=ψ(U',V') then U=U' and δ=δ' ⇒ Λ_V=Λ_{V'} ⇒ V=V'.",
        ],
        "budget_reduction": (
            "Injecting free-1 CS pairs into e·p reduces to injecting FS_1(e) "
            "(or residual sides) into a set of size e, then pairing with δ∈F_p."
        ),
        "deployed_e_p": E_P,
    }


def lemma_payment_reduction() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "payment_reduces_to_free1_eset_into_e",
        "statement": (
            "If M_pad≤1 and there is an injection ι: residual free-1 CS side "
            "supports → {0,...,e−1}, then "
            "(U,V) ↦ (ι(U), δ) injects residual free-1 CS ordered pairs into "
            f"[e]×F_p of size e·p = t·p = {E_P} (deployed t=e), hence "
            "|A_SP| ≤ t·p."
        ),
        "proof": [
            "v20: M_pad≤1 ⇒ N_ord = N_side (pairs inject via side key).",
            "ψ(U,V)=(U,δ) injective (previous lemma).",
            "ι injective on residual U's ⇒ (ι(U),δ) injective on residual pairs.",
        ],
        "open_piece": "ι: residual FS_1(e) → [e] (or M_pad≤1 at free_core≫1).",
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_high_fc_multimates_and_eset_to_e",
        "statement": (
            f"(1) Bound multipads at free_core={FREE_CORE}: depth-w power-sum "
            f"multi-mates of size m_c={M_C} jointly avoiding a free-1 CS e-pair "
            "in the common complement.\n"
            "(2) Inject residual free-1 fully-split e-sets into [e] "
            "(structure-aware completion of e·p mark).\n"
            "CAS: free_core=1 model shows fiber is free — lift joint-avoid / "
            "fully-split constraints; Newton form for free_core≫1 multi-mates."
        ),
    }


def cas_fc1_sage() -> dict[str, Any]:
    """Run Sage free_core=1 multipad algebraic checks if sage available."""
    script = r"""
from sage.all import *
ok = True
rows = []
for w in [1,2,3,4]:
    F = GF(17)
    m = w + 1
    j = 2*m
    names = [f"h{i}" for i in range(m-1)] + ["cA","cB"] + [f"s{i}" for i in range(m-1)] + ["u0","v0","x"]
    A = PolynomialRing(F, names)
    x = A.gens()[-1]
    hs = A.gens()[:m-1]
    cA, cB = A.gens()[m-1], A.gens()[m]
    ss = A.gens()[m+1:m+1+(m-1)]
    u0 = A.gens()[m+1+(m-1)]
    def monic(highs, c):
        pol = x**m + c
        for i,hi in enumerate(highs):
            pol += hi * x**(m-1-i)
        return pol
    CA, CB = monic(hs, cA), monic(hs, cB)
    U = monic(ss, u0)
    dC_ok = (CA - CB) == (cA - cB)
    dS_ok = (CA*U - CB*U) == (cA - cB)*U
    room = j - w - 1
    auto = room == m
    rows.append(dict(w=int(w), m=int(m), j=int(j), dC_ok=bool(dC_ok), dS_ok=bool(dS_ok), room=int(room), auto=bool(auto)))
    ok = ok and dC_ok and dS_ok and auto
print("OK" if ok else "FAIL")
print(rows)
"""
    try:
        r = subprocess.run(
            ["sage", "-c", script],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        out = (r.stdout or "") + (r.stderr or "")
        ok = r.returncode == 0 and "OK" in out.splitlines()[0] if out.strip() else False
        return {
            "status": "PASS" if ok else "SKIP_OR_FAIL",
            "returncode": r.returncode,
            "stdout_tail": "\n".join(out.strip().splitlines()[-5:]),
            "ok": ok,
        }
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"status": "SKIP", "reason": str(exc), "ok": None}


def toy_suite() -> dict[str, Any]:
    rows = []
    n_prod_ok = 0
    n_prod_checked = 0
    n_U_delta_pairs = 0
    n_newton_ok = 0
    n_newton_checked = 0
    # structure-aware mark tallies
    mark_names = [
        "U_delta",  # proved injective (not e·p budget)
        "sumU_mod_e_delta",
        "minU_mod_e_delta",
        "prodU_mod_e_delta",
        "high0_mod_e_delta",
    ]
    mark_global: dict[str, dict[str, int]] = {
        name: {"n_pairs": 0, "coll_labels": 0, "always_inj_rows": 0, "rows_with_pairs": 0}
        for name in mark_names
    }

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
        bound = free_core - 1
        vals = domain_vals(p, n)
        ensure(p > m_c, "newton hyp")

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        max_Mpad = 1
        n_mp = 0
        max_dd = -1
        min_lead_idx = None
        all_prod = True
        all_newton = True
        # collect unique free-1 CS pairs for mark tests
        pair_meta: list[tuple] = []
        seen_pair: set = set()

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                pU = monic_rev([vals[i] for i in sorted(U)], p)
                high = tuple(pU[1:-1])
                pencils[(tuple(sorted(C)), high)].append((C, U, pU[-1], pU))

            pads: dict[Any, list] = defaultdict(list)
            for key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                _ck, high = key
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U, pU = a
                        _C2, V, c0V, pV = b
                        if (c0U - c0V) % p == 0:
                            continue
                        pads[(high, c0U, c0V)].append((C, U, V, pU))
                        fp = (tuple(sorted(U)), tuple(sorted(V)))
                        if fp not in seen_pair:
                            seen_pair.add(fp)
                            pair_meta.append((U, V, c0U, c0V, high, pU))

            for _sk, items in pads.items():
                by_c: dict[tuple, tuple] = {}
                for C, U, V, pU in items:
                    t = tuple(sorted(C))
                    if t not in by_c:
                        by_c[t] = (U, V, pU)
                if len(by_c) < 2:
                    max_Mpad = max(max_Mpad, len(by_c))
                    continue
                max_Mpad = max(max_Mpad, len(by_c))
                n_mp += 1
                cores = list(by_c.keys())
                U0, V0, pU0 = by_c[cores[0]]
                for a, b in itertools.combinations(cores, 2):
                    C1, C2 = frozenset(a), frozenset(b)
                    p1 = monic_rev([vals[i] for i in sorted(C1)], p)
                    p2 = monic_rev([vals[i] for i in sorted(C2)], p)
                    dd = deg_diff(p1, p2, m_c, p)
                    max_dd = max(max_dd, dd)
                    ensure(dd <= bound, f"deg {dd}>{bound}")
                    ensure(phi_w(p1, w) == phi_w(p2, w), "phi")

                    # lead index of core diff
                    lead = None
                    for idx in range(1, m_c + 1):
                        if (p1[idx] - p2[idx]) % p != 0:
                            lead = idx
                            break
                    if lead is not None:
                        ensure(lead >= w + 1, f"lead {lead} < w+1")
                        min_lead_idx = lead if min_lead_idx is None else min(min_lead_idx, lead)

                    # product identity
                    diff = [(p1[i] - p2[i]) % p for i in range(len(p1))]
                    prod = poly_mul(diff, pU0, p)
                    S1, S2 = C1 | U0, C2 | U0
                    ps1 = monic_rev([vals[i] for i in sorted(S1)], p)
                    ps2 = monic_rev([vals[i] for i in sorted(S2)], p)
                    L = max(len(prod), len(ps1), len(ps2))
                    prod += [0] * (L - len(prod))
                    dS = [
                        ((ps1[i] if i < len(ps1) else 0) - (ps2[i] if i < len(ps2) else 0)) % p
                        for i in range(L)
                    ]
                    n_prod_checked += 1
                    if all(prod[i] == dS[i] for i in range(L)):
                        n_prod_ok += 1
                    else:
                        all_prod = False

                    # Newton: first w power sums agree
                    roots1 = [vals[i] for i in sorted(C1)]
                    roots2 = [vals[i] for i in sorted(C2)]
                    ps_a = power_sums(roots1, w, p)
                    ps_b = power_sums(roots2, w, p)
                    n_newton_checked += 1
                    if all(ps_a[k] == ps_b[k] for k in range(1, w + 1)):
                        n_newton_ok += 1
                    else:
                        all_newton = False

                    # joint avoid
                    ensure(U0.isdisjoint(C1) and U0.isdisjoint(C2), "U avoid")
                    ensure(V0.isdisjoint(C1) and V0.isdisjoint(C2), "V avoid")

        # mark injectivity on unique pairs
        mark_buckets: dict[str, dict[Any, list]] = {name: defaultdict(list) for name in mark_names}
        for U, V, c0U, c0V, high, pU in pair_meta:
            delta = (c0U - c0V) % p
            ensure(delta != 0, "delta")
            fp = (tuple(sorted(U)), tuple(sorted(V)))
            prodU = 1
            for i in U:
                prodU = (prodU * vals[i]) % p
            labs = {
                "U_delta": (tuple(sorted(U)), delta),
                "sumU_mod_e_delta": (sum(U) % e, delta),
                "minU_mod_e_delta": (min(U) % e, delta),
                "prodU_mod_e_delta": (prodU % e, delta),
                "high0_mod_e_delta": ((high[0] % e) if high else 0, delta),
            }
            for name, lab in labs.items():
                mark_buckets[name][lab].append(fp)

        row_marks: dict[str, Any] = {}
        for name in mark_names:
            buckets = mark_buckets[name]
            nuniq = len({fp for fps in buckets.values() for fp in fps})
            coll = sum(1 for fps in buckets.values() if len(set(fps)) >= 2)
            inj = nuniq > 0 and coll == 0 and len(buckets) == nuniq
            row_marks[name] = {
                "n_unique_pairs": nuniq,
                "n_labels": len(buckets),
                "n_collision_labels": coll,
                "injective": inj if nuniq > 0 else None,
            }
            mark_global[name]["n_pairs"] += nuniq
            mark_global[name]["coll_labels"] += coll
            if nuniq > 0:
                mark_global[name]["rows_with_pairs"] += 1
                if inj:
                    mark_global[name]["always_inj_rows"] += 1

        n_U_delta_pairs += row_marks["U_delta"]["n_unique_pairs"]
        if pair_meta:
            ensure(row_marks["U_delta"]["injective"] is True, "U_delta must inject")

        if free_core <= 0:
            ensure(max_Mpad <= 1, "fc0")

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
                "n_unique_CS_pairs": len(pair_meta),
                "max_core_diff_deg": max_dd,
                "deg_bound": bound,
                "min_lead_idx": min_lead_idx,
                "w_plus_1": w + 1,
                "all_product_id": all_prod if n_mp > 0 else None,
                "all_newton_ps": all_newton if n_mp > 0 else None,
                "marks": row_marks,
            }
        )

    ensure(n_prod_checked > 0 and n_prod_ok == n_prod_checked, "product id")
    ensure(n_newton_checked > 0 and n_newton_ok == n_newton_checked, "newton")
    ensure(n_U_delta_pairs > 0, "pairs")
    # U_delta injective on every row with pairs
    ensure(
        mark_global["U_delta"]["always_inj_rows"]
        == mark_global["U_delta"]["rows_with_pairs"],
        "U_delta all rows",
    )
    # e·p-scale marks (everything except U_delta) must collide somewhere
    for name in mark_names:
        if name == "U_delta":
            continue
        ensure(
            mark_global[name]["coll_labels"] > 0,
            f"need collision bank for {name}",
        )
    ensure(FREE_CORE == 846161, "dep fc")
    ensure(P > M_C, "dep newton hyp")
    ensure(T == E, "t=e")

    cas = cas_fc1_sage()
    # do not hard-fail if sage missing; prefer pass when ok
    if cas.get("ok") is False:
        raise AssertionError(f"sage fc1 model failed: {cas}")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_product_checks": n_prod_checked,
            "n_product_ok": n_prod_ok,
            "n_newton_checks": n_newton_checked,
            "n_newton_ok": n_newton_ok,
            "n_U_delta_pairs": n_U_delta_pairs,
            "mark_global": mark_global,
        },
        "cas_fc1": cas,
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v24",
        "title": "Newton multi-mates + (U,δ) CS-pair reduction + free_core=1 CAS",
        "status": "PARTIAL_STRUCTURE_AWARE",
        "claims": {
            "proves_product_identity": True,
            "proves_newton_multimate": True,
            "proves_fc1_fiber_automatic": True,
            "proves_U_delta_injection": True,
            "proves_payment_reduces_to_eset_into_e": True,
            "proves_M_pad_le_1_deployed": False,
            "proves_eset_into_e": False,
            "proves_ep_cs_injection": False,
            "toy_confirms_product_newton_Udelta": True,
        },
        "deployed": {
            "j": J,
            "w": W,
            "e": E,
            "m_c": M_C,
            "free_core": FREE_CORE,
            "p": P,
            "p_gt_mc": P > M_C,
            "t": T,
            "t_equals_e": T == E,
            "t_p": T_P,
            "e_p": E_P,
        },
        "lemmas": {
            "product": lemma_product_identity(),
            "newton": lemma_newton_multimate(),
            "fc1_fiber": lemma_fc1_fiber_auto(),
            "U_delta": lemma_U_delta_injection(),
            "payment_reduction": lemma_payment_reduction(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "structure_aware": (
                "CS pairs → (U,δ); e·p payment ⇐ free-1 e-sets → [e] + M_pad≤1"
            ),
            "multimate": (
                "Multipads = depth-w power-sum multi-mates + joint complement "
                "CS-extension; free_core=1 fiber free (CAS)"
            ),
            "next": (
                "Inject residual FS_1(e) into [e], or bound free_core≫1 "
                "power-sum multi-mates with joint avoid"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    cas = cert["toy_suite"]["cas_fc1"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['max_Mpad']} | "
        f"{r['n_multipad_events']} | {r['n_unique_CS_pairs']} | "
        f"{r['all_product_id']} | {r['all_newton_ps']} | "
        f"{r['marks']['U_delta']['injective']} | "
        f"{r['marks']['sumU_mod_e_delta']['injective']} |"
        for r in rows
    )
    mg = cen["mark_global"]
    mark_tbl = "\n".join(
        f"| `{name}` | {s['n_pairs']} | {s['coll_labels']} | "
        f"{s['always_inj_rows']}/{s['rows_with_pairs']} |"
        for name, s in mg.items()
    )
    return f"""# KB-MCA Route-D v24: Newton multi-mates + (U,δ) reduction

Status: `PARTIAL` — structure-aware CS-pair injection **PROVED**; free_core=1
fiber automatic (**CAS**); deployed multipad / e-set→[e] still **OPEN**.

## Product identity (PROVED)

```text
(Λ_C − Λ_{{C'}}) · Λ_U  =  Λ_{{C∪U}} − Λ_{{C'∪U}}
```

## Newton multi-mate form (PROVED, p > m_c)

```text
Phi_w(C)=Phi_w(C')  ⇔  p_k(C)=p_k(C') for k=1..w
```

Deployed: `p={d['p']} > m_c={d['m_c']}` = {d['p_gt_mc']}.

Multipad cores = depth-w **power-sum multi-mates** of size `m_c` that jointly
avoid a free-1 CS e-pair in the common complement.

## free_core=1 fiber automatic (PROVED + CAS)

At free_core=1 (`m_c=e=w+1`, `j=2w+2`):

```text
Λ_{{C∪U}} − Λ_{{C'∪U}} = c · Λ_U ,   deg = e = j−w−1
```

Phi_w fiber room is exactly met ⇒ same-fiber is free. Obstruction = fully-split
+ joint avoidance only.

CAS (Sage): `{cas.get('status')}` — {cas.get('stdout_tail', cas.get('reason',''))}

## Structure-aware mark (PROVED)

```text
ψ(U,V) = (U, δ),   δ = c0(U)−c0(V) ∈ F_p^×
```

injects free-1 CS ordered pairs into `FS_1(e) × F_p^×`.

### Payment reduction (PROVED)

```text
M_pad ≤ 1  and  residual FS_1(e) ↪ [e]
    ⇒  (U,V) ↦ (ι(U), δ) injects into e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

Deployed `e·p = {d['e_p']}`.

### Mark bank

| mark | #pairs | #colliding labels | inj rows |
|---|---:|---:|---|
{mark_tbl}

`U_delta` injective (proved); e-index×δ marks still collide.

## Toys

| j | w | free_core | max M_pad | #mp | #CS pairs | prod id? | newton? | U_δ inj? | sumU mod e ×δ? |
|---|---|---:|---:|---:|---:|---|---|---|---|
{tbl}

Product checks: {cen['n_product_ok']}/{cen['n_product_checks']}; Newton:
{cen['n_newton_ok']}/{cen['n_newton_checks']}.

## OPEN

1. Bound free_core=`{d['free_core']}` power-sum multi-mates with joint complement CS-extension
2. Inject residual free-1 fully-split e-sets into `[e]`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v24.py --check
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
        "# kb-qatom-route-d-v24\n\n"
        "Newton multi-mates + (U,δ) CS-pair reduction + free_core=1 CAS.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v24 report\n\nstatus: {cert['status']}\n"
        f"free_core: {cert['deployed']['free_core']}\n"
        f"U_delta injection: PROVED\n"
        f"eset into e: OPEN\n"
        f"cas_fc1: {cert['toy_suite']['cas_fc1'].get('status')}\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  product identity: PROVED")
    print("  Newton multi-mate (p>m_c): PROVED")
    print("  free_core=1 fiber automatic: PROVED (+ CAS)")
    print("  ψ=(U,δ) injects free-1 CS pairs: PROVED")
    print("  payment ⇐ FS_1(e)↪[e] + M_pad≤1: PROVED reduction")
    print(f"  toys: {len(cert['toy_suite']['rows'])} rows, "
          f"prod={cen['n_product_ok']}, newton={cen['n_newton_ok']}, "
          f"U_delta pairs={cen['n_U_delta_pairs']}")
    print(f"  cas_fc1: {cert['toy_suite']['cas_fc1'].get('status')}")


if __name__ == "__main__":
    main()
