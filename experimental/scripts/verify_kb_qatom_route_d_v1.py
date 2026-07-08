#!/usr/bin/env python3
"""KB-MCA Route-D / Q-atom support-certificate packet v1.

Status honesty:
  - PROVES structural lemmas used by the Route-D attack.
  - REPLAYS the exact conditional closure arithmetic (support mass <= t*p => atom).
  - Does NOT claim U(1116048) <= B* or the row-sharp Q atom theorem.
  - Isolates the remaining certificate as three equivalent finite forms.

Run:
  python3 experimental/scripts/verify_kb_qatom_route_d_v1.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v1.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v1"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v1.json"
CERT_README = CERT_DIR / "README.md"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v1.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v1.report.md"
)

# Deployed KoalaBear MCA adjacent row
P = 2**31 - 2**24 + 1
N = 2**21
K_DIM = 2**20
A = 1_116_048
J = N - A
T = A - K_DIM
W = T - 1
Q_LINE = P**6
B_STAR = (Q_LINE - 1) // 2**128
B_GEN = T * P
B_REM = B_STAR - B_GEN
K_RAW_EXPECTED = 4_807_520
K_REM_EXPECTED = 4_805_007
RETAINED_EXACT_LIFT = math.comb(16, 7)  # C(16,7)=11440
TARGET_FLOOR_EXPECTED = 274_836_936_291_722_953


def ensure(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def log2_int(x: int) -> float:
    ensure(x > 0, "log2_int expects positive")
    bits = x.bit_length()
    if bits <= 1024:
        return math.log2(x)
    shift = bits - 1024
    return math.log2(x >> shift) + shift


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
    raise RuntimeError(f"no primitive root for {p}")


def domain_vals(p: int, n: int) -> list[int]:
    ensure((p - 1) % n == 0, "n must divide p-1")
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    ensure(pow(om, n, p) == 1 and pow(om, n // 2, p) != 1, "bad order-n element")
    return [pow(om, i, p) for i in range(n)]


def monic_coeffs(points: list[int], p: int) -> list[int]:
    """Monic polynomial coeffs [1, c1, c2, ...] for prod (X - v)."""
    poly = [1]
    for v in points:
        new = [0] * (len(poly) + 1)
        mv = (-v) % p
        for i, c in enumerate(poly):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] + c * mv) % p
        poly = new
    return poly


def arithmetic_block() -> dict[str, Any]:
    """Exact integer ledger + conditional closure."""
    c = math.comb(N, J)
    p_to_w = pow(P, W)
    k_raw = (B_STAR * p_to_w) // c
    k_rem = (B_REM * p_to_w) // c
    # target floor = floor(K_rem * C / p^w)
    target_floor = (k_rem * c) // p_to_w
    # also recompute via expected K_rem for cross-check
    target_from_expected = (K_REM_EXPECTED * c) // p_to_w

    ensure(B_STAR == 274_980_728_111_395_087, "B* mismatch")
    ensure(J == 981_104 and T == 67_472 and W == 67_471, "row shape mismatch")
    ensure(B_GEN == 143_763_024_447_376, "t*p mismatch")
    ensure(RETAINED_EXACT_LIFT == 11_440, "C(16,7) mismatch")
    ensure(k_raw == K_RAW_EXPECTED, f"K_raw {k_raw} != {K_RAW_EXPECTED}")
    ensure(k_rem == K_REM_EXPECTED, f"K_rem {k_rem} != {K_REM_EXPECTED}")
    ensure(target_floor == TARGET_FLOOR_EXPECTED, f"target_floor {target_floor}")
    ensure(target_from_expected == TARGET_FLOOR_EXPECTED, "target via expected K_rem")

    support_budget = B_GEN  # t*p
    with_lift = support_budget + RETAINED_EXACT_LIFT
    ensure(with_lift < target_floor, "conditional closure inequality failed")
    slack = target_floor - with_lift
    slack_bits = log2_int(target_floor) - log2_int(with_lift)

    # Sufficient criteria ladder (any one closes the atom under the additive split)
    n_p = N * P
    w_p = W * P
    ensure(n_p + RETAINED_EXACT_LIFT < target_floor, "n*p criterion arithmetic")
    ensure(w_p + RETAINED_EXACT_LIFT < target_floor, "w*p criterion arithmetic")

    # Free-coeff filtration: |Fib_w(z)| <= p * mu_1(z); atom if max mu_1 <= floor(target/p)
    mu1_ceiling = target_floor // P
    ensure(mu1_ceiling == 128_988_645, f"mu1 ceiling {mu1_ceiling}")
    # p^2 alone is NOT enough
    ensure(P * P > target_floor, "sanity: p^2 exceeds target (known gap)")

    return {
        "status": "PROVED_BY_EXACT_INTEGER_ARITHMETIC",
        "row": {
            "p": P,
            "n": N,
            "k": K_DIM,
            "agreement_a_plus": A,
            "j": J,
            "t": T,
            "w": W,
            "q_line": str(Q_LINE),
            "B_star": B_STAR,
        },
        "paid_image_cells": {
            "B_gen_le_t_p": B_GEN,
            "scope": "IMAGE_CELL_NOT_SUPPORT",
            "formula": "R <= t row indices times p generated slopes",
        },
        "multipliers": {
            "K_raw": k_raw,
            "K_rem_after_image_gen": k_rem,
            "retained_exact_lift_C_16_7": RETAINED_EXACT_LIFT,
        },
        "conditional_closure": {
            "hypothesis": (
                "For every primitive finite prefix target z, after first-match deletion, "
                "|G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p"
            ),
            "with_retained_lift": with_lift,
            "target_floor": target_floor,
            "integer_slack": slack,
            "slack_bits": slack_bits,
            "closes_atom": True,
            "does_not_claim": "The hypothesis is not proved in this packet.",
        },
        "sufficient_support_budgets_that_fit": {
            "t*p": {"value": B_GEN, "slack_bits_with_lift": slack_bits},
            "w*p": {
                "value": w_p,
                "slack_bits_with_lift": log2_int(target_floor) - log2_int(w_p + RETAINED_EXACT_LIFT),
            },
            "n*p": {
                "value": n_p,
                "slack_bits_with_lift": log2_int(target_floor) - log2_int(n_p + RETAINED_EXACT_LIFT),
            },
            "mu1_ceiling_for_free_coeff_filtration": {
                "value": mu1_ceiling,
                "meaning": (
                    "If max_z max_alpha |Fib_{w+1}(z||alpha)| <= mu1_ceiling, "
                    "then max |Fib_w(z)| <= p*mu1_ceiling <= target_floor."
                ),
            },
        },
        "dead_shortcuts": {
            "p_squared_alone": {
                "value": P * P,
                "fits_target": False,
                "gap_bits": log2_int(P * P) - log2_int(target_floor),
            },
            "lift_class_keep_one": {
                "status": "REFUTED_UPSTREAM",
                "source": "PR #417 / verify_liftclass_cost_model_refuted.py",
            },
            "r2_moment_CS_Plancherel": {
                "status": "REFUTED_UPSTREAM",
                "source": "cap25_v13_q_pw2_concentration_floor.md",
            },
        },
    }


def lemma_fixed_core_clique_bound() -> dict[str, Any]:
    """PROVED: fixed-core top-seam cliques are pairwise-disjoint side sets.

    Let e = w+1 and |C| = j - e.  If U_1,...,U_r subset D\\C are pairwise the
    side sets of top-seam collisions sharing the exact common core C, then the
    U_i are pairwise disjoint e-sets, hence r <= floor((n-|C|)/e).
    """
    # Pure combinatorics — no field arithmetic required for the packing step.
    # We still toy-check constant-shift + disjointness on enumerable rows.
    return {
        "status": "PROVED",
        "name": "fixed_core_top_seam_clique_packing",
        "statement": (
            "For a fixed common core C of size j-(w+1), any family of top-seam "
            "mates sharing exactly that core has pairwise disjoint side sets of "
            "size e=w+1, hence size <= floor((n-|C|)/(w+1))."
        ),
        "proof_sketch": [
            "Top-seam means e = |S\\T| = |T\\S| = w+1 and S∩T = C with |C|=j-e.",
            "Side sets U=S\\C and V=T\\C are disjoint by construction of C=S∩T.",
            "Any two members of a same-core clique give side sets both disjoint from C "
            "and pairwise disjoint from each other (their supports meet exactly at C).",
            "Pack e-sets into a ground set of size n-|C|.",
        ],
        "deployed_numeric": {
            "e": T,  # w+1 = t
            "core_size": J - T,
            "packing_ceiling": (N - (J - T)) // T,
        },
    }


def lemma_free_coeff_filtration() -> dict[str, Any]:
    """PROVED: |Fib_w(z)| <= p * mu_1(z) with mu_1 the max next-coeff multiplicity."""
    return {
        "status": "PROVED",
        "name": "free_coefficient_filtration",
        "statement": (
            "Write Lambda_S = X^j + z_1 X^{j-1}+...+z_w X^{j-w} + a_{w+1} X^{j-w-1}+.... "
            "For fixed z=(z_1..z_w), partition Fib_w(z) by a_{w+1} in F_p. "
            "Each block is a fiber of the depth-(w+1) prefix map. "
            "Hence |Fib_w(z)| <= p * max_alpha |Fib_{w+1}(z||alpha)|."
        ),
        "proof_sketch": [
            "The first w monic coefficients are the fiber label z.",
            "The next monic coefficient a_{w+1} takes values in a set of size <= p.",
            "Fixing (z, a_{w+1}) is exactly the depth-(w+1) prefix fiber.",
        ],
        "atom_criterion": (
            "If max |Fib_{w+1}| <= floor(target_floor / p) = 128988645, the w-depth "
            "max fiber is <= target_floor and the additive residual split is not even needed."
        ),
        "self_similarity": (
            "The multiplier kappa = target/avg is invariant under this depth shift: "
            "avg_{w+1}=avg_w/p and target_{w+1}=target_w/p, so kappa is unchanged. "
            "Depth reduction alone does not ease the finite kappa demand."
        ),
    }


def lemma_kappa_self_similarity() -> dict[str, Any]:
    avg_log = log2_int(math.comb(N, J)) - W * log2_int(P)
    # use floats carefully only for display; exact kappa is K_rem
    return {
        "status": "PROVED",
        "name": "kappa_depth_self_similarity",
        "K_rem": K_REM_EXPECTED,
        "statement": (
            "For the full-fiber form of the atom, the admissible multiplier "
            "kappa = floor(B_rem * p^w / C(n,j)) is unchanged when the prefix depth "
            "increases by 1 and the target/average are both divided by p."
        ),
        "avg_log2_approx": avg_log,
    }


def toy_enumerate(p: int, n: int, j: int, w: int) -> dict[str, Any]:
    """Exact small-row checks for packing + filtration + top-seam structure."""
    vals = domain_vals(p, n)
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    supports: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)

    for exps in __import__("itertools").combinations(range(n), j):
        pts = [vals[i] for i in exps]
        poly = monic_coeffs(pts, p)
        # poly = [1, c1, c2, ... cj]
        z = tuple(poly[1 : w + 1])
        free = tuple(poly[w + 1 : w + 4]) if len(poly) > w + 1 else tuple()
        fibers[z].append(free)
        supports[z].append(frozenset(exps))

    max_fiber = max(len(v) for v in fibers.values())
    mu1 = 0
    mu2 = 0
    pack_violations = 0
    top_seam_cs_violations = 0
    clique_pack_checked = 0

    for z, rests in fibers.items():
        c1 = Counter(r[0] for r in rests if r)
        if c1:
            mu1 = max(mu1, max(c1.values()))
        if rests and len(rests[0]) >= 2:
            c2 = Counter(r[:2] for r in rests)
            mu2 = max(mu2, max(c2.values()))

    # Fixed-core packing check on a random sample of top-seam edges in max fibers
    # Take the largest fiber
    z_max = max(supports.keys(), key=lambda zz: len(supports[zz]))
    mem = supports[z_max]
    e = w + 1
    # Build cliques by core for top-seam pairs (full if |mem| small else sample)
    core_sides: dict[frozenset[int], list[frozenset[int]]] = defaultdict(list)
    pair_iter = __import__("itertools").combinations(range(len(mem)), 2)
    pairs = list(pair_iter)
    if len(pairs) > 3000:
        random.seed(p + 1000*n + 1000000*j + 100000000*w)
        pairs = random.sample(pairs, 3000)

    for a, b in pairs:
        A, B = set(mem[a]), set(mem[b])
        if len(A - B) != e:
            continue
        C = frozenset(A & B)
        if len(C) != j - e:
            continue
        U = frozenset(A - C)
        V = frozenset(B - C)
        # constant-shift check on side locators
        polyU = monic_coeffs([vals[i] for i in sorted(U)], p)
        polyV = monic_coeffs([vals[i] for i in sorted(V)], p)
        # poly = [1,c1,...,ce]; constant-shift <=> c1..c_{e-1} equal and ce differs
        if polyU[1:e] != polyV[1:e]:
            top_seam_cs_violations += 1
        core_sides[C].append(U)
        core_sides[C].append(V)

    for C, sides in core_sides.items():
        uniq = []
        for s in sides:
            if s not in uniq:
                uniq.append(s)
        # pairwise disjoint?
        ok = True
        for i in range(len(uniq)):
            for k in range(i + 1, len(uniq)):
                if uniq[i] & uniq[k]:
                    ok = False
        ceiling = (n - len(C)) // e
        if not ok or len(uniq) > ceiling:
            pack_violations += 1
        clique_pack_checked += 1

    # Filtration inequality on max fiber
    filtration_ok = max_fiber <= p * mu1 if mu1 else max_fiber <= 1

    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "num_fibers": len(fibers),
        "max_fiber": max_fiber,
        "mu1_max_next_coeff_mult": mu1,
        "mu2_max_two_free_mult": mu2,
        "p_times_mu1": p * mu1,
        "filtration_holds": filtration_ok,
        "top_seam_constant_shift_violations_in_sample": top_seam_cs_violations,
        "fixed_core_pack_violations": pack_violations,
        "fixed_core_cliques_checked": clique_pack_checked,
    }


def run_toy_suite() -> dict[str, Any]:
    rows = [
        (17, 16, 8, 1),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (97, 32, 5, 2),
        (97, 32, 5, 3),
        (193, 64, 4, 2),
        (257, 128, 3, 2),
    ]
    results = []
    for params in rows:
        r = toy_enumerate(*params)
        ensure(r["filtration_holds"], f"filtration failed on {params}")
        ensure(r["top_seam_constant_shift_violations_in_sample"] == 0, f"CS fail {params}")
        ensure(r["fixed_core_pack_violations"] == 0, f"pack fail {params}")
        results.append(r)
    return {
        "status": "PROVED_ON_TOY_SUITE_AND_GENERAL_PROOF",
        "rows": results,
        "notes": (
            "Filtration is general. Fixed-core packing is general. "
            "Toy suite checks constant-shift normal form + packing + filtration numerics."
        ),
    }


def remaining_certificate() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "route_d_support_certificate",
        "deployed_target": (
            "For every primitive finite prefix target z at KB-MCA a=1116048, after "
            "first-match deletion of generated_field / quotient_planted / sparse_pade_hankel / "
            "m1_window_shadow / rank_drop_pivot / bc_chart / sp_shift_pair / extension_slope, "
            "|G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p = 143763024447376."
        ),
        "equivalent_forms": [
            {
                "id": "E1_additive_support",
                "form": "|G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p",
            },
            {
                "id": "E2_marked_incidence_injection",
                "form": (
                    "Residual supports inject (controlled mult <=1 after first-match) into "
                    "a label space of size <= t*p, e.g. {0..t-1} x F_p or marked-incidence keys."
                ),
            },
            {
                "id": "E3_large_folding_defect_transfer",
                "form": (
                    "Every large signed folding defect satisfying the odd prefix equations is "
                    "quotient-descended, sparse/Pade-Hankel, M1/window-shadow, rank-drop with "
                    "printed pivot cost, generated-field support-paid, or lies in a primitive "
                    "full-rank defect stratum of mass <= t*p."
                ),
            },
            {
                "id": "E4_mu1_ceiling",
                "form": (
                    "max fiber at depth w+1 is <= 128988645 (closes full N_w without "
                    "additive residual split; kappa-self-similar so not obviously easier)."
                ),
            },
            {
                "id": "E5_np_injection",
                "form": (
                    "Residual supports inject into D x F_p (size n*p) after first-match; "
                    "slack ~5.94 bits with retained lift."
                ),
            },
        ],
        "falsifier": (
            "Exhibit a primitive residual leaf at a finite prefix target z with "
            "support mass > t*p after the named first-match deletions, or a full "
            "prefix fiber larger than target_floor."
        ),
        "upstream_dead_ends_not_to_repeat": [
            "lift-class keep-one payment (PR #417 refuted)",
            "r=2 / CS / Plancherel alone (pw2 concentration floor)",
            "absolute-value dual character sums (PR #398 barrier map)",
            "raw Delsarte distance packing (Gilbert gap ~1.37e6 bits)",
        ],
    }


def build_cert() -> dict[str, Any]:
    return {
        "packet": "kb_qatom_route_d_v1",
        "title": "KB-MCA Route-D support certificate attack: proved lemmas + exact closure arithmetic",
        "status": "PARTIAL_PROVED_LEMMAS_ATOM_OPEN",
        "claims": {
            "proves_row_sharp_q_atom": False,
            "proves_U_1116048_le_Bstar": False,
            "proves_fixed_core_clique_packing": True,
            "proves_free_coeff_filtration": True,
            "proves_conditional_closure_arithmetic": True,
            "proves_kappa_self_similarity": True,
        },
        "arithmetic": arithmetic_block(),
        "lemmas": {
            "fixed_core_clique": lemma_fixed_core_clique_bound(),
            "free_coeff_filtration": lemma_free_coeff_filtration(),
            "kappa_self_similarity": lemma_kappa_self_similarity(),
        },
        "toy_suite": run_toy_suite(),
        "remaining": remaining_certificate(),
        "provenance": [
            {
                "name": "KB first-match ledger",
                "path": "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md",
                "use": "row constants, image-cell t*p, exact-lift 11440, Route D naming",
            },
            {
                "name": "row-sharp reductions #397",
                "path": "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md",
                "use": "conditional closure shape; missing support certificate isolation",
            },
            {
                "name": "lift-class refutation #417",
                "path": "thresholds: lift-class cost model refuted",
                "use": "do not pay residual by keep-one lift class",
            },
            {
                "name": "pw2 concentration floor",
                "path": "experimental/notes/thresholds/cap25_v13_q_pw2_concentration_floor.md",
                "use": "r=2 routes dead; full N_w bound is sufficient for atom",
            },
            {
                "name": "grande_finale",
                "path": "experimental/grande_finale.tex",
                "use": "def:q-row-atom, prop:q-exact-target, prop:prefix-rigidity, top-seam constant shift",
            },
        ],
    }


def render_note(cert: dict[str, Any]) -> str:
    ar = cert["arithmetic"]
    cc = ar["conditional_closure"]
    rem = cert["remaining"]
    lines = [
        "# KB-MCA Route-D support certificate v1",
        "",
        "Status: `PARTIAL` — structural lemmas **PROVED**; conditional closure arithmetic "
        "**PROVED**; row-sharp Q atom / `U(1116048)<=B*` **OPEN**.",
        "",
        "This packet attacks the single remaining support certificate that closes the "
        "KoalaBear MCA adjacent safe side at agreement `a+ = 1116048`.  It does not "
        "edit Papers A–D and does not claim the atom.",
        "",
        "## Deployed row",
        "",
        "```text",
        f"p = {P} = 2^31-2^24+1",
        f"n = {N} = 2^21",
        f"k = {K_DIM} = 2^20",
        f"a+ = {A}",
        f"j = n-a+ = {J}",
        f"t = a+-k = {T}",
        f"w = t-1 = {W}",
        f"B* = {B_STAR}",
        f"t*p = {B_GEN}",
        "```",
        "",
        "## Conditional closure (PROVED arithmetic)",
        "",
        "If for every primitive finite prefix target `z`, after first-match deletion,",
        "",
        "```text",
        "|G_gen_support(z)| + |D_full_rank_prim(z)|  <=  t*p",
        "```",
        "",
        "then with the imported exact-lift retained class bound `C(16,7)=11440`,",
        "",
        "```text",
        f"t*p + 11440     = {cc['with_retained_lift']}",
        f"target_floor    = {cc['target_floor']}",
        f"integer slack   = {cc['integer_slack']}",
        f"slack bits      ≈ {cc['slack_bits']:.10f}",
        "```",
        "",
        "and the row-sharp Q-prefix atom inequality follows.  This replays and "
        "machine-checks the closure shape isolated in the #397 reductions packet.",
        "",
        "## Proved lemmas",
        "",
        "### Lemma A — fixed-core top-seam clique packing (PROVED)",
        "",
        cert["lemmas"]["fixed_core_clique"]["statement"],
        "",
        "Proof idea: top-seam pairs sharing exact core `C` have pairwise disjoint "
        f"side sets of size `e=w+1={T}`; pack into `D\\\\C`.  Deployed packing ceiling "
        f"`floor((n-|C|)/e) = {cert['lemmas']['fixed_core_clique']['deployed_numeric']['packing_ceiling']}`.",
        "",
        "### Lemma B — free-coefficient filtration (PROVED)",
        "",
        cert["lemmas"]["free_coeff_filtration"]["statement"],
        "",
        "Consequence: the atom holds if the depth-`(w+1)` max fiber is at most "
        f"`{ar['sufficient_support_budgets_that_fit']['mu1_ceiling_for_free_coeff_filtration']['value']}` "
        "(≈ `2^26.94`).  The admissible multiplier `kappa` is **self-similar** under "
        "depth shift (Lemma C), so this is not an automatic easing.",
        "",
        "### Lemma C — kappa depth self-similarity (PROVED)",
        "",
        cert["lemmas"]["kappa_self_similarity"]["statement"],
        "",
        "### Sufficient support budgets that fit under the target (PROVED arithmetic)",
        "",
        "| budget | value | slack bits (with +11440) |",
        "|---|---:|---:|",
        f"| `t*p` | {B_GEN} | {cc['slack_bits']:.4f} |",
        f"| `w*p` | {W*P} | {ar['sufficient_support_budgets_that_fit']['w*p']['slack_bits_with_lift']:.4f} |",
        f"| `n*p` | {N*P} | {ar['sufficient_support_budgets_that_fit']['n*p']['slack_bits_with_lift']:.4f} |",
        "",
        f"| `p^2` alone | {P*P} | **does not fit** (gap "
        f"{ar['dead_shortcuts']['p_squared_alone']['gap_bits']:.4f} bits) |",
        "",
        "## Remaining open certificate",
        "",
        rem["deployed_target"],
        "",
        "Equivalent finite forms:",
        "",
    ]
    for eq in rem["equivalent_forms"]:
        lines.append(f"- **{eq['id']}**: {eq['form']}")
    lines += [
        "",
        f"Falsifier: {rem['falsifier']}",
        "",
        "## Dead ends (do not re-grind)",
        "",
    ]
    for x in rem["upstream_dead_ends_not_to_repeat"]:
        lines.append(f"- {x}")
    lines += [
        "",
        "## Toy suite",
        "",
        "The verifier enumerates small dyadic rows and checks:",
        "",
        "1. free-coeff filtration numerics,",
        "2. top-seam constant-shift normal form on sampled edges,",
        "3. fixed-core side-set packing.",
        "",
        "All rows in the suite pass (see JSON).",
        "",
        "## Reproducibility",
        "",
        "```bash",
        "python3 experimental/scripts/verify_kb_qatom_route_d_v1.py",
        "python3 experimental/scripts/verify_kb_qatom_route_d_v1.py --check",
        "```",
        "",
        "Zero-arg, stdlib-only.  Exit 0 = all gates green.",
        "",
        "## Non-claims",
        "",
        "- Does not prove `U(1116048) <= B*`.",
        "- Does not prove `prob:row-sharp-q` / `def:q-row-atom`.",
        "- Does not pay generated-field **support** multiplicity (only image cells).",
        "- Does not refute or prove the entropy–subfield envelope.",
        "",
        "## Next attack steps (ordered)",
        "",
        "1. Prove a support-level injection of the primitive residual into a space of size "
        "   `<= n*p` or `<= t*p` (forms E2/E5), using marked incidence + first-match leaves.",
        "2. Or bound the large signed folding-defect stratum (form E3 / classical Route D).",
        "3. Or bound depth-`(w+1)` max fibers by `128988645` (form E4) — kappa-self-similar.",
        "4. Any success immediately upgrades this packet's conditional closure into an atom proof.",
        "",
    ]
    return "\n".join(lines) + "\n"


def render_report(cert: dict[str, Any]) -> str:
    return (
        "# kb_qatom_route_d_v1 report\n\n"
        f"status: {cert['status']}\n"
        f"conditional slack bits: {cert['arithmetic']['conditional_closure']['slack_bits']:.10f}\n"
        f"toy rows: {len(cert['toy_suite']['rows'])}\n"
        f"proves atom: {cert['claims']['proves_row_sharp_q_atom']}\n"
    )


def render_readme(cert: dict[str, Any]) -> str:
    return (
        "# kb-qatom-route-d-v1\n\n"
        "Certificate JSON for the KB-MCA Route-D / Q-atom support-certificate packet.\n\n"
        f"Status: `{cert['status']}`\n\n"
        "Verify with:\n\n"
        "```bash\n"
        "python3 experimental/scripts/verify_kb_qatom_route_d_v1.py --check\n"
        "```\n"
    )


def write_outputs(cert: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CERT_README.write_text(render_readme(cert), encoding="utf-8")
    NOTE_PATH.write_text(render_note(cert), encoding="utf-8")
    REPORT_PATH.write_text(render_report(cert), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="rebuild and verify against written cert")
    args = parser.parse_args()

    cert = build_cert()
    if args.check and CERT_PATH.exists():
        old = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        # Compare load-bearing arithmetic fields
        for key in ("conditional_closure", "multipliers", "row"):
            ensure(
                old["arithmetic"][key] == cert["arithmetic"][key]
                or key == "conditional_closure"
                and abs(old["arithmetic"][key]["slack_bits"] - cert["arithmetic"][key]["slack_bits"]) < 1e-9,
                f"arithmetic drift on {key}",
            )
        ensure(old["claims"] == cert["claims"], "claims drift")
        ensure(old["remaining"]["deployed_target"] == cert["remaining"]["deployed_target"], "target drift")

    write_outputs(cert)
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  slack_bits: {cert['arithmetic']['conditional_closure']['slack_bits']:.10f}")
    print(f"  toy_rows: {len(cert['toy_suite']['rows'])}")
    print(f"  wrote: {CERT_PATH.relative_to(ROOT)}")
    print(f"  wrote: {NOTE_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
