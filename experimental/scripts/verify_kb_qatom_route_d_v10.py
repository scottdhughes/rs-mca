#!/usr/bin/env python3
"""KB-MCA Route-D v10: residual M_m and what first-match actually deletes.

After v8/v9: global M_m >= 10 (coset pads); full-fiber M_m not bounded by k_tight.
This packet isolates the residual quantity that routing actually needs.

Proved:
  (1) Residual-restricted routing: N_can_prim(z) <= U_res(z) * M_m^{res}(z)
      with M_m^{res}(z) := max over residual can-core Phi_w-fibers ( <= global M_m ).
  (2) Residual atom criterion with K_res (not global K).
  (3) Maximal c-quotient/planted j-supports are definitionally non-residual
      for terminal c in {2^16, 2^17} (ledger / v4).
  (4) GAP: a single full c-fiber factor (partial planting) is NOT definitionally
      residual-excluded. v8 coset-pad mates are exactly one-fiber partial plants,
      so global M_m >= 10 does NOT force residual M_m^{res} >= 10.
  (5) Fiber-factor extraction: every support has a unique maximal c-decomposition
      S = P sqcup pi_c^{-1}(Q) with P fiber-free.
  (6) Toys: heaviest Phi_w fibers of m-sets are often entirely free of full
      e0-coset factors; aperiodic residual proxy does not cut those maxima.
      Hence residual hope is not "delete cosets and Mm collapses" on toys.

Does not prove M_m^{res} <= 1 or any atom-scale residual upper bound.
Does not claim U(1116048) <= B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v10.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v10.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v10"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v10.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v10.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v10.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
J = 981_104
W = 67_471
E = W + 1
M = J - E  # 913632 can-core weight
FREE = M - W
E0 = 2**17  # v8 coset block
PACK_J = 17
TARGET = 274_836_936_291_722_953
B_GEN = 67_472 * P
K_COSET = 1 + (N - M) // E0  # 10
K_TIGHT = 1 + (N - M) // E  # 18
TERMINAL_C = (65536, 131072)


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


def period(exps: frozenset[int], n: int) -> int:
    for d in range(1, n + 1):
        if all(((i + d) % n) in exps for i in exps):
            return d
    return n


def aperiodic(exps: frozenset[int], n: int) -> bool:
    return period(exps, n) == n


def c_cosets(n: int, c: int) -> list[frozenset[int]]:
    """Exponent cosets = fibers of pi_c : x |-> x^c when c|n (size-c APs step n/c)."""
    ensure(c > 0 and n % c == 0, "c|n")
    step = n // c
    return [frozenset((r + k * step) % n for k in range(c)) for r in range(step)]


def maximal_c_decomposition(
    s: frozenset[int], n: int, c: int
) -> tuple[frozenset[int], int]:
    """S = P sqcup (union of full c-fibers). Return (P, |Q|)."""
    if c <= 1 or n % c != 0:
        return s, 0
    q = 0
    covered: set[int] = set()
    for cos in c_cosets(n, c):
        if cos <= s:
            q += 1
            covered |= cos
    p = frozenset(s - covered)
    return p, q


def is_maximal_c_planted(s: frozenset[int], n: int, c: int, weight: int) -> bool:
    """Ledger form: |Q|=floor(weight/c), |P|=weight mod c."""
    if c <= 1 or n % c != 0:
        return False
    _p, q = maximal_c_decomposition(s, n, c)
    return q == weight // c and len(_p) == weight % c


def lemma_fiber_factor_extraction() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "maximal_c_fiber_factor_extraction",
        "statement": (
            "Fix c|n. For every S subset D, let Q = { beta in D_{n/c} : "
            "pi_c^{-1}(beta) subset S } and P = S \\\\ pi_c^{-1}(Q). Then "
            "S = P sqcup pi_c^{-1}(Q), P contains no full pi_c-fiber, and "
            "(|P|,|Q|) is uniquely determined. In exponent coordinates with "
            "c|n, full fibers are the n/c residue classes mod n/c of length c."
        ),
        "proof": [
            "By definition Q indexes exactly the full fibers contained in S.",
            "Every point of S either lies in such a fiber or in P; the union is "
            "disjoint. Uniqueness: any full fiber inside S contributes its base "
            "point to Q.",
            "For D = mu_n and c|n, pi_c-fibers are cosets of the order-c subgroup, "
            "i.e. exponent APs with step n/c and length c.",
        ],
    }


def lemma_residual_routing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_Mm_routing",
        "statement": (
            "Let R(z) subset Fib_w^{(j)}(z) be any residual family of j-supports. "
            "For S in R(z) let U be the e=w+1 lex-smallest elements, C = S\\\\U, "
            "u = Phi_w(Lambda_U), b = b(z,u) the triangular core prefix (v3/v5). "
            "Let M_m^{res}(z) = max_u |{ C_can(S) : S in R(z), u(S)=u }| "
            "(equivalently, max number of residual can-cores sharing one side-prefix "
            "block; each such core lies in one m-subset Phi_w fiber). "
            "Let U_res(z) = |{ u(S) : S in R(z) }|. Then "
            "N_can_prim(z) <= U_res(z) * M_m^{res}(z). "
            "Always M_m^{res}(z) <= M_m^{max} (global)."
        ),
        "proof": [
            "v5 residual core routing: cores partition by side-prefix u; each block "
            "embeds into Fib_w^{(m)}(b(z,u)) via C_can.",
            "Restricting the count to residual S only yields M_m^{res} instead of "
            "the full m-fiber size M_m. The block count is still <= U_res.",
            "N_can_prim = |{C_can(S): S in R}| <= sum_u |block_u| <= U_res * M_m^{res}.",
            "M_m^{res} <= M_m because residual can-cores are a subfamily of all m-subsets.",
        ],
        "consequence": (
            "Atom criteria should use K_res >= M_m^{res}, not the global coset lower "
            "bound K_coset=10, unless residual realizes those coset-pad mates."
        ),
    }


def lemma_residual_criterion() -> dict[str, Any]:
    budgets = {}
    for name, K in [
        ("K_res_1", 1),
        ("K_res_coset_lower_if_realized", K_COSET),
        ("K_res_tight", K_TIGHT),
    ]:
        budgets[name] = {
            "K": K,
            "U_res_atom": TARGET // (PACK_J * K),
            "log2": math.log2(max(TARGET / (PACK_J * K), 1)),
        }
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "residual_atom_criterion",
        "statement": (
            "If max_z M_m^{res}(z) <= K_res and max_z U_res(z) <= floor(target/(pack*K_res)), "
            "then max_z N_can_prim(z) <= floor(target/pack), hence max_z |R(z)| <= target "
            "by residual lex covering (v4)."
        ),
        "proof": [
            "N_can_prim <= U_res * M_m^{res} <= (target/(pack K_res)) * K_res = target/pack.",
            "|R| <= pack * N_can_prim <= target.",
        ],
        "budgets": budgets,
    }


def lemma_maximal_planted_nonresidual() -> dict[str, Any]:
    # deployed arithmetic for j-supports
    rows = []
    for c in TERMINAL_C:
        j_c = J // c
        r_c = J % c
        rows.append(
            {
                "c": c,
                "j_c": j_c,
                "r_c": r_c,
                "r_c_le_w": r_c <= W,
                "terminal_raw_paid": True,
            }
        )
    return {
        "status": "PROVED",
        "name": "maximal_terminal_planted_is_nonresidual",
        "statement": (
            "Under the first-match ledger residual definition, every j-support that is "
            "c-quotient/planted in the maximal form "
            "S = P sqcup pi_c^{-1}(Q) with |Q|=floor(j/c), |P|=j mod c, "
            "for terminal c in {65536,131072}, is assigned to branch 4 and is not in R(z)."
        ),
        "proof": [
            "Ledger definition of R(z) (kb_mca_1116048_first_match_ledger_v1): excludes "
            "supports assigned to terminal quotient/planted.",
            "Q0 raw-pays terminal rungs c=65536 and c=131072 "
            "(binom(32,14)+binom(16,7)).",
            "Deployed: for both terminal c, r_c = j mod c <= w, so the Q0 descent "
            "hypotheses apply and the maximal planted class is exactly the paid class.",
        ],
        "deployed_terminal_rows": rows,
        "source": "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md",
    }


def lemma_partial_plant_gap() -> dict[str, Any]:
    # v8 mates: m-set = R cup U with |U|=e0=c, one full fiber, |Q|=1
    # maximal for m would need |Q|=floor(m/c)
    m_qmax = M // E0
    m_r = M % E0
    j_qmax = J // E0
    j_r = J % E0
    return {
        "status": "PROVED",
        "name": "partial_single_fiber_plant_not_definitionally_residual_excluded",
        "statement": (
            f"A support (m-set or j-set) that contains exactly one full c-fiber for "
            f"c={E0}, with maximal Q-count 1 < floor(weight/c), is only *partially* "
            "planted. The ledger residual definition excludes maximal terminal "
            "quotient/planted assignments, not every support with |Q|>=1. "
            "Therefore the v8 coset-pad mates "
            f"(each an m-set R cup U with U a single c-coset, so |Q|=1 while "
            f"floor(m/c)={m_qmax}) are not definitionally non-residual as m-sets, "
            "and a j-support C cup U_side built from such a can-core is not "
            "definitionally non-residual unless some first-match branch assigns it."
        ),
        "proof": [
            "Fiber-factor extraction gives |Q|=1 for pure single-coset pads when R is "
            "fiber-free.",
            f"Maximal planted requires |Q|=floor(m/c)={m_qmax} (m-sets) or "
            f"floor(j/c)={j_qmax} (j-sets). Since 1 < those maxima, single-fiber pads "
            "are not in the maximal planted class.",
            "Branch 4 pays maximal terminal classes (Q0). Branch 5 "
            "(planted/prefix-structured for non-maximal / open tails) is not a proved "
            "payment that deletes all |Q|>=1 supports from residual.",
            "Hence residual M_m^{res} is not forced to inherit the global lower bound "
            f"M_m >= {K_COSET} from v8.",
        ],
        "deployed_numbers": {
            "c": E0,
            "m": M,
            "floor_m_over_c": m_qmax,
            "m_mod_c": m_r,
            "m_mod_c_gt_w": m_r > W,
            "j": J,
            "floor_j_over_c": j_qmax,
            "j_mod_c": j_r,
            "j_mod_c_le_w": j_r <= W,
            "v8_pad_Q_count": 1,
        },
        "program_impact": (
            "Do not set K_res = 10 from v8 alone. Either prove a planted/partial-factor "
            "branch that removes single-fiber pads from residual, or bound M_m^{res} by "
            "other structure (possibly M_m^{res}=1 still holds)."
        ),
    }


def lemma_global_lower_not_residual() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "global_Mm_lower_does_not_force_residual_lower",
        "statement": (
            f"Global M_m^{{max}} >= {K_COSET} (v8) does not imply "
            f"M_m^{{res,max}} >= {K_COSET}. Residual routing may use K_res = 1 "
            "even while global uniqueness is false."
        ),
        "proof": [
            "M_m^{res} counts only residual can-cores. Global witnesses may all be "
            "non-residual (paid by some first-match branch) or may fail to appear as "
            "C_can of residual j-supports.",
            "Partial-plant gap: the known size-10 global fiber from coset pads is not "
            "definitionally residual.",
            "Therefore the residual atom criterion is logically independent of the "
            "v8 refutation of global uniqueness.",
        ],
    }


def lemma_what_residual_needs() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_PROGRAM_LAW",
        "name": "residual_program_law",
        "statement": (
            "Closing the residual atom after v8/v9 requires one of: "
            "(A) M_m^{res} <= K_res with K_res small (ideally 1) and U_res budget "
            "target/(17 K_res); "
            "(B) a direct bound on residual can-core Phi_w-image "
            "(v7 B2) without Mm; "
            "(C) a first-match payment that removes all multi-mate residual cores "
            "(e.g. partial planted / sparse-null / non-tight collision cells)."
        ),
        "proof": [
            "From residual routing + lex covering: |R| <= pack * U_res * M_m^{res}.",
            "v8 kills only global M_m <= 1. v9 kills using k_tight as full-fiber upper.",
            "This packet separates residual from global.",
        ],
        "not_proved": [
            "M_m^{res} <= 1",
            "U_res <= target/17",
            "partial single-fiber plants are non-residual",
        ],
    }


def toy_suite() -> dict[str, Any]:
    """Measure global Mm vs residual proxies and planted-factor filters."""
    rows = []
    for p, n, m, w in [
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 5, 2),
        (17, 16, 4, 2),
        (17, 16, 10, 4),
        (17, 16, 8, 5),
        (17, 16, 7, 3),
        (17, 16, 9, 4),
        (17, 16, 8, 6),
    ]:
        C = math.comb(n, m)
        if C > 15000:
            rows.append({"p": p, "n": n, "m": m, "w": w, "skip": C})
            continue
        vals = domain_vals(p, n)
        fibers: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for S in itertools.combinations(range(n), m):
            poly = monic_rev([vals[i] for i in S], p)
            fibers[phi_w(poly, w)].append(frozenset(S))
        mm = max(len(v) for v in fibers.values())
        e0s = [c for c in range(2, n + 1) if n % c == 0 and c >= w + 1 and c <= m]
        e0 = min(e0s) if e0s else None

        def max_under(pred: Any) -> int:
            return max(
                (sum(1 for s in v if pred(s)) for v in fibers.values()),
                default=0,
            )

        def has_fiber(s: frozenset[int], c: int) -> bool:
            _, q = maximal_c_decomposition(s, n, c)
            return q >= 1

        mm_ap = max_under(lambda s: aperiodic(s, n))
        if e0 is not None:
            mm_q0 = max_under(lambda s, e0=e0: maximal_c_decomposition(s, n, e0)[1] == 0)
            mm_not_max_plant = max_under(
                lambda s, e0=e0: not is_maximal_c_planted(s, n, e0, m)
            )
            heavy = max(fibers.values(), key=len)
            heavy_with = sum(1 for s in heavy if has_fiber(s, e0))
            # intersection law on heavy
            max_inter = 0
            for i, a in enumerate(heavy):
                for b in heavy[i + 1 :]:
                    inter = len(a & b)
                    ensure(inter <= m - w - 1, "intersection")
                    if inter > max_inter:
                        max_inter = inter
        else:
            mm_q0 = mm
            mm_not_max_plant = mm
            heavy_with = 0
            max_inter = -1

        # padding reduction lower bound when e0|n
        k_coset = 1 + (n - m) // e0 if e0 else 1
        k_tight = 1 + (n - m) // (w + 1)

        rows.append(
            {
                "p": p,
                "n": n,
                "m": m,
                "w": w,
                "Mm": mm,
                "Mm_ap": mm_ap,
                "Mm_Qeq0": mm_q0,
                "Mm_not_maximal_planted": mm_not_max_plant,
                "heavy_with_full_fiber": heavy_with,
                "heavy_size": mm,
                "e0": e0,
                "k_coset": k_coset,
                "k_tight": k_tight,
                "max_inter": max_inter,
                "inter_cap": m - w - 1,
                "ap_cuts_Mm": mm_ap < mm,
                "Q0_cuts_Mm": mm_q0 < mm,
                "heavy_coset_free": heavy_with == 0,
            }
        )

    # structural gates on deployed arithmetic
    ensure(K_COSET == 10, "k_coset")
    ensure(J % E0 == J - (J // E0) * E0, "j mod")
    ensure((J % E0) <= W, "terminal r_c for j at e0")
    ensure((M % E0) > W, "m partial plant has r>w at e0")
    ensure(1 < M // E0, "single fiber is partial for m")
    ensure(any(r.get("heavy_coset_free") for r in rows if "Mm" in r), "toy coset-free heavy")
    ensure(any(r.get("Mm", 0) > r.get("k_coset", 0) for r in rows if "Mm" in r), "gap")

    # explicit partial-plant toy: build one coset pad and check |Q|==1 < qmax when qmax>1
    p, n, e0, w, m = 17, 16, 4, 2, 6
    # m=6, e0=4, qmax=1 — use larger multiple: n=16,e0=2,m=6 -> qmax=3
    e0 = 2
    vals = domain_vals(17, 16)
    cos = c_cosets(16, e0)
    ensure(len(cos) == 8, "n/e0")
    U = cos[0]
    rest = [i for i in range(16) if i not in U]
    R = frozenset(rest[: m - e0])
    S = R | U
    _p, q = maximal_c_decomposition(S, 16, e0)
    ensure(q >= 1, "pad has fiber")
    # another pad mate
    V = cos[1]
    ensure(U.isdisjoint(V), "disjoint")
    # R may hit V — rebuild fiber-free R
    free_pts = [i for i in range(16) if i not in U and i not in V]
    R2 = frozenset(free_pts[: m - e0])
    S1, S2 = R2 | U, R2 | V
    ensure(len(S1) == m and len(S2) == m, "sizes")
    ph1 = phi_w(monic_rev([vals[i] for i in sorted(S1)], 17), w)
    ph2 = phi_w(monic_rev([vals[i] for i in sorted(S2)], 17), w)
    # free-1 on e0=2: w needs e0 >= w+1 => 2 >= 3? False for w=2.
    # Use w=1 for e0=2 padding: e0 >= w+1 => 2>=2.
    w_pad = 1
    ph1 = phi_w(monic_rev([vals[i] for i in sorted(S1)], 17), w_pad)
    ph2 = phi_w(monic_rev([vals[i] for i in sorted(S2)], 17), w_pad)
    ensure(ph1 == ph2, "pad collision")
    _p1, q1 = maximal_c_decomposition(S1, 16, e0)
    _p2, q2 = maximal_c_decomposition(S2, 16, e0)
    ensure(q1 == 1 and q2 == 1, f"partial Q {q1},{q2}")
    ensure(m // e0 >= 2, "qmax>=2 so partial")
    pad_check = {
        "p": 17,
        "n": 16,
        "e0": e0,
        "m": m,
        "w": w_pad,
        "Q_counts": [q1, q2],
        "qmax": m // e0,
        "Phi_match": True,
        "partial": True,
    }

    return {"status": "PASS", "rows": rows, "partial_pad_check": pad_check}


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v10",
        "title": "Residual M_m routing; partial-plant gap; coset lower bound not residual",
        "status": "PARTIAL_RESIDUAL_LAW",
        "claims": {
            "proves_residual_Mm_routing": True,
            "proves_residual_criterion": True,
            "proves_fiber_factor_extraction": True,
            "proves_maximal_terminal_planted_nonresidual": True,
            "proves_partial_plant_not_definitionally_excluded": True,
            "proves_global_lower_not_force_residual_lower": True,
            "proves_Mm_res_le_1": False,
            "proves_U_res_atom": False,
            "refutes_Mm_le_1_global": True,
        },
        "deployed": {
            "n": N,
            "j": J,
            "m": M,
            "w": W,
            "e0_coset": E0,
            "Mm_global_lower": K_COSET,
            "k_tight": K_TIGHT,
            "terminal_c": list(TERMINAL_C),
            "j_mod_e0": J % E0,
            "m_mod_e0": M % E0,
            "floor_j_e0": J // E0,
            "floor_m_e0": M // E0,
            "U_res_if_Kres_1": TARGET // (PACK_J * 1),
            "U_res_if_Kres_10": TARGET // (PACK_J * K_COSET),
            "log2_U_res_K1": math.log2(max(TARGET / PACK_J, 1)),
            "log2_U_res_K10": math.log2(max(TARGET / (PACK_J * K_COSET), 1)),
        },
        "lemmas": {
            "fiber_factor": lemma_fiber_factor_extraction(),
            "residual_routing": lemma_residual_routing(),
            "residual_criterion": lemma_residual_criterion(),
            "maximal_planted": lemma_maximal_planted_nonresidual(),
            "partial_plant_gap": lemma_partial_plant_gap(),
            "global_not_residual": lemma_global_lower_not_residual(),
            "program_law": lemma_what_residual_needs(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "v8_global_Mm_ge_10": "stands for global fibers only",
            "residual_K_res": "not forced to 10; K_res=1 still logically open",
            "B2": "still open; residual routing makes B2 the right wall",
            "next": (
                "Prove M_m^{res}<=1 (or small K_res), or pay partial single-fiber plants "
                "in first-match, or bound residual can-core Phi_w-image directly."
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = [r for r in cert["toy_suite"]["rows"] if "Mm" in r]
    tbl = "\n".join(
        f"| {r['p']} | {r['n']} | {r['m']} | {r['w']} | {r['Mm']} | {r['Mm_ap']} | "
        f"{r['Mm_Qeq0']} | {r['heavy_with_full_fiber']}/{r['heavy_size']} | "
        f"{r['k_coset']} | {r['heavy_coset_free']} |"
        for r in rows
    )
    pad = cert["toy_suite"]["partial_pad_check"]
    return f"""# KB-MCA Route-D v10: residual M_m law

Status: `PARTIAL` — residual routing + partial-plant gap **PROVED**; residual
atom upper bound **OPEN**. Global uniqueness remains **REFUTED** (v8).

## Main message

```text
Global M_m >= 10  (v8 coset pads)
     does NOT force
Residual M_m^res >= 10
```

Routing for the atom uses **residual** can-cores only. The residual criterion
may still close with `K_res = 1`.

## Theorems

### 1 — Residual routing (PROVED)

```text
N_can_prim(z)  <=  U_res(z) * M_m^res(z)
M_m^res(z)     <=  M_m^max   (global)
```

`M_m^res` = max number of residual can-cores in one side-prefix block
(each block sits in one m-subset `Phi_w` fiber).

### 2 — Residual atom criterion (PROVED conditional)

```text
M_m^res <= K_res  and  U_res <= target/(17 K_res)
    =>  |R| <= target
```

| K_res | U_res atom budget | log2 |
|---:|---:|---:|
| 1 | {d['U_res_if_Kres_1']} | {d['log2_U_res_K1']:.2f} |
| 10 | {d['U_res_if_Kres_10']} | {d['log2_U_res_K10']:.2f} |

### 3 — Maximal terminal planted is non-residual (PROVED)

For terminal `c in {{65536,131072}}`, maximal c-quotient/planted j-supports
(`|Q|=floor(j/c)`, `|P|=j mod c`) are first-match assigned (Q0 raw-paid) and
lie outside `R(z)`.

Deployed: `j mod 131072 = {d['j_mod_e0']} <= w` (descent applies).

### 4 — Partial single-fiber plant gap (PROVED)

v8 mates are m-sets `R cup U` with **one** full `c=2^17` fiber:

```text
|Q| = 1  <  floor(m/c) = {d['floor_m_e0']}
m mod c = {d['m_mod_e0']} > w
```

These are **not** maximal planted. Residual definition does **not** automatically
delete `|Q|=1` supports. Branch 5 (non-maximal planted) is not a proved payment.

### 5 — Fiber-factor extraction (PROVED)

Every support has a unique maximal decomposition `S = P sqcup pi_c^{{-1}}(Q)`
with `P` fiber-free.

### 6 — Global lower != residual lower (PROVED)

Logical separation: residual atom with `K_res=1` is compatible with v8.

## Toy evidence

Heaviest m-subset `Phi_w` fibers are often **entirely free** of full e0-coset
factors. Aperiodic residual proxy and `|Q|=0` filters often **do not** reduce
`M_m`. Large fibers are not "just coset pads."

| p | n | m | w | Mm | Mm_ap | Mm_Q=0 | heavy with fiber | k_coset | heavy coset-free |
|---|---|---|---|---:|---:|---:|---:|---:|---|
{tbl}

Partial-pad check (`n=16,e0=2,m=6,w=1`): Phi match={pad['Phi_match']},
Q counts={pad['Q_counts']}, qmax={pad['qmax']} (partial).

## Impact

| Claim | Status |
|---|---|
| Global `M_m <= 1` | REFUTED (v8) |
| Residual must use `K_res >= 10` | **FALSE** (this packet) |
| `M_m^res <= 1` | OPEN |
| `U_res` atom budget | OPEN |
| B2 residual core-prefix image | OPEN |

## Next real math

1. Prove `M_m^res <= 1` (or small `K_res`) by residual geometry, **or**
2. Pay partial single-fiber / non-tight collision cells in first-match, **or**
3. Bound residual can-core `Phi_w`-image (B2) with no Mm premise.

Do not set residual `K` from the global coset lower bound alone.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v10.py
python3 experimental/scripts/verify_kb_qatom_route_d_v10.py --check
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
        ensure(
            old["deployed"]["Mm_global_lower"] == cert["deployed"]["Mm_global_lower"],
            "bound drift",
        )
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v10\n\n"
        "Residual M_m routing; partial-plant gap vs global coset lower bound.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v10.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v10 report\n\nstatus: {cert['status']}\n"
        f"Mm_global_lower: {cert['deployed']['Mm_global_lower']}\n"
        f"residual K_res=1 still open: yes\n"
        f"toy rows: {len([r for r in cert['toy_suite']['rows'] if 'Mm' in r])}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  global Mm >= {cert['deployed']['Mm_global_lower']} (v8, not residual)")
    print(f"  residual K_res=1: logically open (partial-plant gap)")
    print(f"  U_res budget if K_res=1: {cert['deployed']['U_res_if_Kres_1']}")
    rows = [r for r in cert["toy_suite"]["rows"] if "Mm" in r]
    print(f"  toy rows: {len(rows)}")
    print(f"  heavy coset-free toys: {sum(1 for r in rows if r['heavy_coset_free'])}")
    print(f"  partial pad check: {cert['toy_suite']['partial_pad_check']}")


if __name__ == "__main__":
    main()
