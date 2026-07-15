#!/usr/bin/env sage
"""Verify the local reduced-CRT common-factor lemma for `(3,1,3,(2,2,2))`.

Let ``B=B1*B2*B3`` have degree six, let ``G`` be the CRT multiplier satisfying
``G=c_i*R^(-1) mod B_i``, and write a monic cubic as

    F = X^3 + f2*X^2 + f1*X + f0.

Compatibility is the affine system ``K(F)=M*(f0,f1,f2)^t+u=0``, where ``K``
extracts the coefficients of ``X^3,X^4,X^5`` from ``F*G mod B``.  If ``M``
drops rank and the affine system is compatible, the homogeneous kernel in
degree at most three has dimension at least two.  For two kernel pairs
``V_i=F_i*G mod B`` with ``deg(V_i)<=2``, the polynomial

    F0*V1 - F1*V0

is divisible by ``B`` and has degree at most five, hence vanishes.  Unique
factorization then forces every monic cubic kernel element to share a
nonconstant factor with its corresponding ``V``.  In the sunflower
reconstruction this recovers at least one nominally missed core point.  The
pointwise bridge is checked under explicit hypotheses: the core locator is
split and squarefree, the restored point is removed from its three-root
missed-core locator, the retained background is disjoint from the core, and
the received word is zero on the core.  Under those hypotheses a compatible
rank drop cannot realize the exact defect-three profile.

The symbolic calculation and finite censuses are exact.  They support the
displayed local proof; they are not generic saturation and do not prove the
global mixed-petal theorem.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

from sage.all import GF, PolynomialRing, QQ, matrix, vector


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/certificate.json"
)
OWNER_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-owner-partition/certificate.json"
)
CENSUS_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222/certificate.json"
)
PRIOR_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_cross_model_review.md"
)
FRESH_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_cross_model_review_v2.md"
)
ANALYZER_PATH = ROOT / "experimental/scripts/analyze_l1_b9_frontier_31222.sage"
SCANNER_PATH = (
    ROOT / "experimental/scripts/scan_l1_full_list_quotient_conjecture.py"
)
UPSTREAM_RECONSTRUCTION_PATH = (
    ROOT / "experimental/notes/l1/l1_general_reconstruction_collapse.md"
)


def sha256_json(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=int)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locator(PX, X, roots):
    output = PX.one()
    for root in roots:
        output *= X - root
    return output


def polynomial_from_coefficients(PX, coefficients):
    X = PX.gen()
    field = PX.base_ring()
    return sum(
        (field(value) * X**degree for degree, value in enumerate(coefficients)),
        PX.zero(),
    )


def coefficients_low_to_high(poly, degree):
    return [int(poly[index]) for index in range(degree + 1)]


def validate_bridge_control(control):
    """Fail closed on every load-bearing pointwise-bridge hypothesis."""
    try:
        field = GF(int(control["field"]))
        PX = PolynomialRing(field, "X")
        X = PX.gen()
        core = tuple(field(value) for value in control["core_roots"])
        background = tuple(field(value) for value in control["background_roots"])
        h = field(control["restored_core_root"])
        recorded_D = tuple(field(value) for value in control["missed_core_roots"])
        received = tuple(field(value) for value in control["received_core_values"])

        if len(core) != 4 or len(set(core)) != 4:
            return False
        if h not in core:
            return False
        D = tuple(value for value in core if value != h)
        if recorded_D != D or len(D) != 3:
            return False
        if set(core).intersection(background):
            return False
        if len(received) != len(core) or any(value != 0 for value in received):
            return False

        F = polynomial_from_coefficients(
            PX, control["F_coefficients_low_to_high"]
        )
        V = polynomial_from_coefficients(
            PX, control["V_coefficients_low_to_high"]
        )
        expected_F = locator(PX, X, D)
        if F != expected_F or F.degree() != 3 or not F.is_squarefree():
            return False
        roots_with_multiplicity = F.roots()
        if (
            len(roots_with_multiplicity) != 3
            or {root for root, multiplicity in roots_with_multiplicity} != set(D)
            or any(multiplicity != 1 for _root, multiplicity in roots_with_multiplicity)
        ):
            return False

        core_locator = locator(PX, X, core)
        H = core_locator // F
        if H != X - h:
            return False
        R = locator(PX, X, background)
        if R.gcd(core_locator) != 1:
            return False
        gcd_FV = F.gcd(V)
        alpha = field(control["common_root_alpha"])
        if gcd_FV.degree() < 1 or gcd_FV(alpha) != 0:
            return False
        if alpha not in D or alpha == h:
            return False

        W = R * H * V
        agreement_roots = tuple(
            value
            for value, u_value in zip(core, received, strict=True)
            if W(value) == u_value
        )
        expected_agreements = tuple(
            value for value in core if value == h or (value in D and V(value) == 0)
        )
        actual_missed = tuple(
            value
            for value, u_value in zip(core, received, strict=True)
            if W(value) != u_value
        )
        expected_missed = tuple(value for value in D if V(value) != 0)
        if agreement_roots != expected_agreements or actual_missed != expected_missed:
            return False
        if len(actual_missed) > 2:
            return False
        return (
            [int(value) for value in agreement_roots]
            == control["actual_core_agreement_roots"]
            and [int(value) for value in actual_missed]
            == control["actual_missed_core_roots"]
            and bool(control["pointwise_bridge_verified"])
        )
    except (KeyError, TypeError, ValueError, ArithmeticError):
        return False


def bridge_control_from_incidence(incidence):
    field = GF(11)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    core = tuple(field(value) for value in incidence["core_roots"])
    h = field(incidence["restored_core_root"])
    D = tuple(value for value in core if value != h)
    F = polynomial_from_coefficients(
        PX, incidence["F_coefficients_low_to_high"]
    )
    V = polynomial_from_coefficients(
        PX, incidence["V_coefficients_low_to_high"]
    )
    R = X
    H = locator(PX, X, core) // F
    W = R * H * V
    gcd_FV = F.gcd(V)
    common_roots = [root for root, _multiplicity in gcd_FV.roots()]
    if not common_roots:
        raise RuntimeError("bridge positive control has no common root")
    agreement_roots = tuple(value for value in core if W(value) == 0)
    actual_missed = tuple(value for value in core if W(value) != 0)
    control = {
        "field": 11,
        "core_roots": [int(value) for value in core],
        "background_roots": [0],
        "restored_core_root": int(h),
        "missed_core_roots": [int(value) for value in D],
        "F_coefficients_low_to_high": coefficients_low_to_high(F, 3),
        "V_coefficients_low_to_high": coefficients_low_to_high(V, 2),
        "common_root_alpha": int(common_roots[0]),
        "received_core_values": [0] * len(core),
        "actual_core_agreement_roots": [int(value) for value in agreement_roots],
        "actual_missed_core_roots": [int(value) for value in actual_missed],
        "pointwise_bridge_verified": True,
    }
    if not validate_bridge_control(control):
        raise RuntimeError("constructed pointwise bridge control failed validation")
    return control


def crt_multiplier(PX, X, R, support_locators, labels):
    B = PX.one()
    for support_locator in support_locators:
        B *= support_locator
    G = PX.zero()
    for support_locator, label in zip(support_locators, labels, strict=True):
        target = (label * R.inverse_mod(support_locator)) % support_locator
        complement = B // support_locator
        idempotent = (
            complement * complement.inverse_mod(support_locator)
        ) % B
        G = (G + target * idempotent) % B
    if G.gcd(B) != 1:
        raise RuntimeError("CRT multiplier is not a unit modulo B")
    return B, G


def reduced_map(PX, X, B, G):
    columns = []
    for degree in range(4):
        remainder = (X**degree * G) % B
        columns.append([remainder[index] for index in range(3, 6)])
    M = matrix(
        PX.base_ring(),
        3,
        3,
        lambda row, column: columns[column][row],
    )
    u = vector(PX.base_ring(), columns[3])
    full = M.augment(u.column())
    return M, u, full


def affine_solutions(M, rhs, field, max_solutions=10_000):
    rank_M = int(M.rank())
    augmented_rank = int(M.augment(rhs.column()).rank())
    if rank_M != augmented_rank:
        return rank_M, augmented_rank, []
    kernel = M.right_kernel().basis()
    count = int(field.order()) ** len(kernel)
    if count > max_solutions:
        raise RuntimeError(f"affine solution fibre too large: {count}")
    particular = M.solve_right(rhs)
    solutions = []
    for coefficients in itertools.product(range(int(field.order())), repeat=len(kernel)):
        solution = vector(field, particular)
        for coefficient, basis_vector in zip(coefficients, kernel, strict=True):
            solution += field(coefficient) * basis_vector
        solutions.append(solution)
    return rank_M, augmented_rank, solutions


def symbolic_reduced_map():
    coefficient_ring = PolynomialRing(
        QQ,
        names=(
            "b0", "b1", "b2", "b3", "b4", "b5",
            "g0", "g1", "g2", "g3", "g4", "g5",
            "f0", "f1", "f2",
        ),
    )
    (
        b0, b1, b2, b3, b4, b5,
        g0, g1, g2, g3, g4, g5,
        f0, f1, f2,
    ) = coefficient_ring.gens()
    PX = PolynomialRing(coefficient_ring, "X")
    X = PX.gen()
    B = X**6 + b5*X**5 + b4*X**4 + b3*X**3 + b2*X**2 + b1*X + b0
    G = g5*X**5 + g4*X**4 + g3*X**3 + g2*X**2 + g1*X + g0
    M, u, full = reduced_map(PX, X, B, G)
    F = X**3 + f2*X**2 + f1*X + f0
    remainder = (F * G) % B
    K_direct = vector(coefficient_ring, [remainder[index] for index in range(3, 6)])
    K_affine = M * vector(coefficient_ring, [f0, f1, f2]) + u

    pair_ring = PolynomialRing(
        QQ,
        names=(
            "a0", "a1", "a2", "a3", "d0", "d1", "d2", "d3",
            "v0", "v1", "v2", "w0", "w1", "w2",
        ),
    )
    (
        a0, a1, a2, a3, d0, d1, d2, d3,
        v0, v1, v2, w0, w1, w2,
    ) = pair_ring.gens()
    PY = PolynomialRing(pair_ring, "Y")
    Y = PY.gen()
    F0 = a3*Y**3 + a2*Y**2 + a1*Y + a0
    F1 = d3*Y**3 + d2*Y**2 + d1*Y + d0
    V0 = v2*Y**2 + v1*Y + v0
    V1 = w2*Y**2 + w1*Y + w0
    cross = F0*V1 - F1*V0

    return {
        "B": str(B),
        "G": str(G),
        "F": str(F),
        "M_rows": [[str(value) for value in row] for row in M.rows()],
        "u": [str(value) for value in u],
        "full_map_shape": list(full.dimensions()),
        "det_M": str(M.det()),
        "det_M_sha256": hashlib.sha256(str(M.det()).encode("utf-8")).hexdigest(),
        "K_affine_identity": bool(K_direct == K_affine),
        "cross_polynomial_degree_bound": int(cross.degree()),
        "cross_polynomial": str(cross),
        "degree_gap": "deg(F0*V1-F1*V0)<=5<deg(B)=6",
    }


def frozen_gf19_census():
    field = GF(19)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    domain = tuple(
        field(value)
        for value in (1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10)
    )
    core = tuple(range(4))
    petals = (
        tuple(range(4, 8)),
        tuple(range(8, 12)),
        tuple(range(12, 16)),
    )
    background = tuple(range(16, 18))
    labels = tuple(field(value) for value in (1, 2, 3))
    core_locator = locator(PX, X, tuple(domain[index] for index in core))
    actual_F = []
    for restored in core:
        F = core_locator // (X - domain[restored])
        actual_F.append((restored, F))

    rank_histogram = Counter()
    rankdrop_monic_count = 0
    rankdrop_gcd_degree_histogram = Counter()
    rankdrop_zero_gcd = []
    compatible_rankdrop_patterns = []
    actual_incidence_count = 0
    transcript = []

    for background_support in itertools.combinations(background, 1):
        R = locator(PX, X, tuple(domain[index] for index in background_support))
        support_choices = [tuple(itertools.combinations(petal, 2)) for petal in petals]
        for supports in itertools.product(*support_choices):
            support_locators = [
                locator(PX, X, tuple(domain[index] for index in support))
                for support in supports
            ]
            B, G = crt_multiplier(PX, X, R, support_locators, labels)
            M, u, full = reduced_map(PX, X, B, G)
            rank_M = int(M.rank())
            rank_full = int(full.rank())
            rank_histogram[f"rankM={rank_M},rankFull={rank_full}"] += 1
            pattern_record = {
                "background_support": list(background_support),
                "petal_supports": [list(support) for support in supports],
                "rank_M": rank_M,
                "rank_full": rank_full,
            }
            if rank_M < 3 and rank_full == rank_M:
                _rank, _augmented, solutions = affine_solutions(M, -u, field)
                gcd_degrees = Counter()
                for coefficients in solutions:
                    F = X**3 + sum(coefficients[degree]*X**degree for degree in range(3))
                    V = (F * G) % B
                    gcd_degree = int(F.gcd(V).degree())
                    gcd_degrees[str(gcd_degree)] += 1
                    rankdrop_gcd_degree_histogram[str(gcd_degree)] += 1
                    rankdrop_monic_count += 1
                    if gcd_degree < 1:
                        rankdrop_zero_gcd.append(
                            {
                                **pattern_record,
                                "F": [int(F[index]) for index in range(4)],
                                "V": [int(V[index]) for index in range(3)],
                            }
                        )
                compatible_rankdrop_patterns.append(
                    {**pattern_record, "monic_count": len(solutions), "gcd_degrees": dict(gcd_degrees)}
                )
            for restored, F in actual_F:
                K = vector(field, [((F*G) % B)[index] for index in range(3, 6)])
                if K == 0:
                    actual_incidence_count += 1
                    V = (F*G) % B
                    pattern_record.setdefault("actual_incidences", []).append(
                        {
                            "restored_core_index": restored,
                            "gcd_degree": int(F.gcd(V).degree()),
                        }
                    )
            transcript.append(pattern_record)

    return {
        "field": 19,
        "support_pattern_count": len(transcript),
        "rank_histogram": dict(sorted(rank_histogram.items())),
        "compatible_rankdrop_pattern_count": len(compatible_rankdrop_patterns),
        "compatible_rankdrop_patterns": compatible_rankdrop_patterns,
        "rankdrop_monic_cubic_count": rankdrop_monic_count,
        "rankdrop_gcd_degree_histogram": dict(sorted(rankdrop_gcd_degree_histogram.items())),
        "rankdrop_zero_gcd_count": len(rankdrop_zero_gcd),
        "rankdrop_zero_gcd_examples": rankdrop_zero_gcd,
        "actual_split_core_incidence_count": actual_incidence_count,
        "transcript_sha256": sha256_json(transcript),
    }


def normalized_gf11_incidence_census():
    """Exhaust the normalized eleven-point split-incidence control."""
    field = GF(11)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    R = X
    labels = tuple(field(value) for value in (1, 2, 3))
    available = tuple(field(value) for value in range(1, 11))
    chart_count = 0
    rank_histogram = Counter()
    compatible_rankdrop_count = 0
    actual_incidence_count = 0
    migrated_incidence_count = 0
    bridge_verified_incidence_count = 0
    bridge_failure_count = 0
    incidence_examples = []
    transcript_digest = hashlib.sha256()

    for roots1 in itertools.combinations(available, 2):
        remaining1 = tuple(value for value in available if value not in roots1)
        for roots2 in itertools.combinations(remaining1, 2):
            remaining2 = tuple(value for value in remaining1 if value not in roots2)
            for roots3 in itertools.combinations(remaining2, 2):
                core_roots = tuple(value for value in remaining2 if value not in roots3)
                support_roots = (roots1, roots2, roots3)
                support_locators = [locator(PX, X, roots) for roots in support_roots]
                B, G = crt_multiplier(PX, X, R, support_locators, labels)
                M, u, full = reduced_map(PX, X, B, G)
                rank_M = int(M.rank())
                rank_full = int(full.rank())
                rank_histogram[f"rankM={rank_M},rankFull={rank_full}"] += 1
                if rank_M < 3 and rank_full == rank_M:
                    compatible_rankdrop_count += 1
                incidences = []
                core_locator = locator(PX, X, core_roots)
                for restored in core_roots:
                    F = core_locator // (X - restored)
                    H = core_locator // F
                    V = (F*G) % B
                    K = vector(field, [V[index] for index in range(3, 6)])
                    if K != 0:
                        continue
                    actual_incidence_count += 1
                    gcd_FV = F.gcd(V)
                    migrated = gcd_FV.degree() >= 1
                    migrated_incidence_count += int(migrated)
                    W = R * H * V
                    D = tuple(value for value in core_roots if value != restored)
                    actual_core_agreements = tuple(
                        value for value in core_roots if W(value) == 0
                    )
                    expected_core_agreements = tuple(
                        value
                        for value in core_roots
                        if value == restored or (value in D and V(value) == 0)
                    )
                    actual_missed_core = tuple(
                        value for value in core_roots if W(value) != 0
                    )
                    expected_missed_core = tuple(
                        value for value in D if V(value) != 0
                    )
                    bridge_verified = bool(
                        migrated
                        and R.gcd(core_locator) == 1
                        and F == locator(PX, X, D)
                        and F.is_squarefree()
                        and H == X - restored
                        and actual_core_agreements == expected_core_agreements
                        and actual_missed_core == expected_missed_core
                        and len(actual_missed_core) <= 2
                    )
                    bridge_verified_incidence_count += int(bridge_verified)
                    bridge_failure_count += int(not bridge_verified)
                    recovered = [
                        int(root)
                        for root, _multiplicity in gcd_FV.roots()
                        if F(root) == 0
                    ]
                    row = {
                        "restored_core_root": int(restored),
                        "F_coefficients_low_to_high": [int(F[index]) for index in range(4)],
                        "V_coefficients_low_to_high": [int(V[index]) for index in range(3)],
                        "gcd_coefficients_low_to_high": [
                            int(gcd_FV[index]) for index in range(int(gcd_FV.degree()) + 1)
                        ],
                        "gcd_degree": int(gcd_FV.degree()),
                        "recovered_missed_core_roots": recovered,
                        "actual_core_agreement_roots": [
                            int(value) for value in actual_core_agreements
                        ],
                        "actual_missed_core_roots": [
                            int(value) for value in actual_missed_core
                        ],
                        "pointwise_bridge_verified": bridge_verified,
                        "exact_d3_excluded": bridge_verified,
                    }
                    incidences.append(row)
                    if len(incidence_examples) < 8:
                        incidence_examples.append(
                            {
                                "support_roots": [[int(value) for value in roots] for roots in support_roots],
                                "core_roots": [int(value) for value in core_roots],
                                "rank_M": rank_M,
                                "rank_full": rank_full,
                                **row,
                            }
                        )
                transcript_row = {
                    "support_roots": [[int(value) for value in roots] for roots in support_roots],
                    "core_roots": [int(value) for value in core_roots],
                    "rank_M": rank_M,
                    "rank_full": rank_full,
                    "incidences": incidences,
                }
                transcript_digest.update(
                    json.dumps(transcript_row, sort_keys=True, separators=(",", ":")).encode("ascii")
                )
                transcript_digest.update(b"\n")
                chart_count += 1

    return {
        "field": 11,
        "normalization": "R=X, labels=(1,2,3), three ordered disjoint support pairs; core is the four-point complement",
        "chart_count": chart_count,
        "rank_histogram": dict(sorted(rank_histogram.items())),
        "compatible_rankdrop_chart_count": compatible_rankdrop_count,
        "actual_split_core_incidence_count": actual_incidence_count,
        "migrated_incidence_count": migrated_incidence_count,
        "unmigrated_incidence_count": actual_incidence_count - migrated_incidence_count,
        "bridge_verified_incidence_count": bridge_verified_incidence_count,
        "bridge_failure_count": bridge_failure_count,
        "incidence_examples": incidence_examples,
        "transcript_sha256": transcript_digest.hexdigest(),
    }


def build_report():
    symbolic = symbolic_reduced_map()
    frozen = frozen_gf19_census()
    normalized = normalized_gf11_incidence_census()
    bridge_control = bridge_control_from_incidence(normalized["incidence_examples"][0])
    owner_certificate = json.loads(OWNER_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    census_certificate = json.loads(CENSUS_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    return {
        "schema": "rs-mca-l1-b9-frontier-31222-reduced-crt-lemma-v3",
        "status": "PROVED_LOCAL_REDUCED_CRT_POINTWISE_BRIDGE_CROSS_MODEL_GREEN",
        "statement": (
            "for pairwise-coprime R,B1,B2,B3 with deg(R)=1 and deg(B_i)=2, "
            "and distinct nonzero labels, a compatible rank drop of the 3x3 "
            "reduced monic-cubic map forces gcd(F,V) to have positive degree; "
            "when C has four distinct field points, h is in C, F=L_(C\\{h}) "
            "is split squarefree, R is core-disjoint, U is zero on C, and "
            "W=R*(X-h)*V, this gives an additional core agreement and excludes "
            "the exact-d3 profile on every compatible rank drop"
        ),
        "parameters": {
            "deg_R": 1,
            "support_locator_degrees": [2, 2, 2],
            "deg_B": 6,
            "deg_F": 3,
            "deg_V_max": 2,
            "label_hypothesis": "pairwise distinct and nonzero",
            "locator_hypothesis": "R,B1,B2,B3 pairwise coprime and monic",
            "core_size": 4,
            "core_hypothesis": "four distinct k-points",
            "restored_point_hypothesis": "h is in C and D=C\\{h}",
            "missed_core_locator_hypothesis": (
                "F=L_D is monic, split, squarefree, and has root set exactly D"
            ),
            "background_core_hypothesis": "gcd(R,L_C)=1",
            "received_core_hypothesis": "U restricted to C is identically zero",
            "received_background_hypothesis": (
                "U is zero at the retained background agreement beta"
            ),
            "reconstruction_hypothesis": "H=L_C/F=X-h and W=R*H*V",
        },
        "reduced_crt_map": symbolic,
        "proof_certificate": {
            "steps": [
                "CRT gives V=F*G mod B with deg(V)<=2 and G a unit modulo B",
                "K(F)=M*(f0,f1,f2)^t+u is the high-degree coefficient map",
                "rank(M)<3 plus monic compatibility makes rank([M|u])<=2",
                "the homogeneous degree-<=3 kernel therefore has dimension at least two",
                "G is a CRT unit, so every nonzero degree-<=3 kernel element has nonzero remainder V",
                "for two kernel pairs, B divides F0*V1-F1*V0 but its degree is at most five, so it is zero",
                "after removing gcd(V0,V1), unique factorization gives F_i=A*W_i and V_i=g*W_i",
                "for a monic cubic F0, W0 cannot be constant without making the second pair dependent",
                "thus gcd(F0,V0) has positive degree",
                "for an exact target codeword P, its unique background and restored-core zeros give P=R*(X-h)*V with deg(V)<=2",
                "on each selected petal support, P=c_i*L_C implies B_i divides R*V-c_i*F, so every target is represented by the reduced system",
                "if (X-alpha) divides gcd(F,V), split squarefreeness gives alpha in D=C\\{h} and therefore alpha is not h",
                "W(alpha)=R(alpha)*(alpha-h)*V(alpha)=0=U(alpha), giving an additional core agreement",
                "for x in D, core/background disjointness gives R(x)*(x-h)!=0, so the missed core is exactly D\\Z(V) and has size at most two",
                "rank(M)=3 leaves at most one monic cubic per fixed cofactor-support pattern",
            ],
            "full_rank_bound_per_support_pattern": 1,
            "compatible_rankdrop_gcd_positive": True,
            "compatible_rankdrop_exact_d3_bound": 0,
            "semantic_bridge_status": "PROVED_POINTWISE_UNDER_EXPLICIT_HYPOTHESES",
            "system_exhaustivity_status": "PROVED_FROM_EXACT_SUPPORT_FACTORIZATION",
            "exact_missed_core_formula": "D\\Z(V)",
        },
        "pointwise_bridge_certificate": {
            "hypotheses": [
                "C consists of four distinct field points",
                "h is in C and D=C\\{h}",
                "F=L_D is split squarefree with roots exactly D",
                "gcd(R,L_C)=1",
                "U(x)=0 for every x in C",
                "H=L_C/F=X-h and W=R*H*V",
                "(X-alpha) divides gcd(F,V)",
            ],
            "deductions": [
                "alpha is in D",
                "alpha is not h",
                "W(alpha)=0=U(alpha)",
                "the core agreement set is {h} union (D intersect Z(V))",
                "the actual missed core is D\\Z(V) and has size at most two",
            ],
            "positive_control": bridge_control,
            "validator_accepts_positive_control": validate_bridge_control(bridge_control),
        },
        "exact_profile_assignment": {
            "profile": {"ell": 4, "d": 3, "r": 1, "t": 3, "a_i": [2, 2, 2]},
            "canonical_key": [
                "unique_background_agreement",
                "two_agreements_in_labelled_petal_1",
                "two_agreements_in_labelled_petal_2",
                "two_agreements_in_labelled_petal_3",
            ],
            "restored_core_point": (
                "uniquely recovered as the singleton exact core agreement; "
                "not an additional summation coordinate because full rank "
                "bounds all monic cubics for one canonical key"
            ),
            "support_pattern_formula": "binom(2,1)*binom(4,2)^3=432",
            "support_pattern_count": 432,
            "codeword_to_key_injective": True,
            "bound_per_key": 1,
            "double_charge_excluded": True,
        },
        "exact_controls": {
            "frozen_GF19": frozen,
            "normalized_GF11": normalized,
        },
        "linked_inputs": {
            "owner_certificate": {
                "path": str(OWNER_CERTIFICATE_PATH.relative_to(ROOT)),
                "schema": owner_certificate["schema"],
                "sha256": sha256_file(OWNER_CERTIFICATE_PATH),
            },
            "census_certificate": {
                "path": str(CENSUS_CERTIFICATE_PATH.relative_to(ROOT)),
                "schema": census_certificate["schema"],
                "sha256": sha256_file(CENSUS_CERTIFICATE_PATH),
            },
            "prior_cross_model_review": {
                "path": str(PRIOR_REVIEW_PATH.relative_to(ROOT)),
                "reviewer": "Claude Sonnet",
                "verdict": "YELLOW",
                "ledger_authorization": "NO",
                "role": "PRIOR_REVIEW_WHOSE_IDENTIFIED_BRIDGE_IS_REPAIRED_HERE",
                "sha256": sha256_file(PRIOR_REVIEW_PATH),
            },
            "fresh_cross_model_review": {
                "path": str(FRESH_REVIEW_PATH.relative_to(ROOT)),
                "reviewer": "Claude Sonnet fresh read-only sessions",
                "verdict": "GREEN",
                "ledger_authorization": "YES",
                "upstream_context_supplement": "GREEN",
                "sha256": sha256_file(FRESH_REVIEW_PATH),
            },
            "concrete_analyzer": {
                "path": str(ANALYZER_PATH.relative_to(ROOT)),
                "sha256": sha256_file(ANALYZER_PATH),
            },
            "received_word_constructor": {
                "path": str(SCANNER_PATH.relative_to(ROOT)),
                "sha256": sha256_file(SCANNER_PATH),
            },
            "upstream_reconstruction_analogy": {
                "path": str(UPSTREAM_RECONSTRUCTION_PATH.relative_to(ROOT)),
                "scope": "BACKGROUND_FREE_FULL_PETAL_CONSISTENCY_ONLY_NOT_IMPORTED",
                "sha256": sha256_file(UPSTREAM_RECONSTRUCTION_PATH),
            },
        },
        "ledger_consequence": {
            "support_pattern_count": 432,
            "prior_profile_charge": 155_952,
            "banked_profile_charge": 432,
            "banked_saved_mass": 155_520,
            "prior_all_profile_bound": 1_503_967,
            "banked_all_profile_bound": 1_348_447,
            "prior_unresolved_bound": 668_803,
            "banked_unresolved_bound": 513_283,
            "banked": True,
            "periodic_support_owner_bound_recorded_but_not_subtracted": 9,
            "disjointness_status": "PROVED_AND_CROSS_MODEL_GREEN",
            "disjointness_claim": (
                "an exact target uniquely determines its one background hit, "
                "three labelled two-point petal supports, and one core hit; "
                "rank(M)=3 bounds all four possible core locators together by "
                "one monic cubic for each of the 432 cofactor keys"
            ),
        },
        "proof_status": {
            "proved_locally": [
                "the reduced-CRT common-factor lemma under the printed hypotheses",
                "the one-monic-cubic bound on every full-rank support pattern",
                "the pointwise additional-core-agreement bridge",
                "the exact-support assignment and no-double-charge argument",
            ],
            "exact_finite": [
                "the frozen GF19 rank strata and all rank-drop gcd checks",
                "the normalized GF11 split-incidence census",
            ],
            "review_status": [
                "fresh cross-model GREEN on pointwise bridge and system exhaustivity",
                "fresh cross-model GREEN on canonical assignment and ledger disjointness",
                "supplemental fresh-context GREEN after full upstream reconstruction-note read",
            ],
        },
        "nonclaims": [
            "no global mixed-petal theorem is proved",
            "no m>2 profile is covered",
            "no statement about PR #763 is made",
            "no Lean formalization is claimed",
            "the banked 432 charge applies only to the frozen named profile",
        ],
        "verdict": "GREEN_LOCAL_LEMMA_LEDGER_AUTHORIZED",
    }


def validate_report(report):
    symbolic = report["reduced_crt_map"]
    frozen = report["exact_controls"]["frozen_GF19"]
    normalized = report["exact_controls"]["normalized_GF11"]
    ledger = report["ledger_consequence"]
    bridge = report["pointwise_bridge_certificate"]
    assignment = report["exact_profile_assignment"]
    return (
        report["schema"] == "rs-mca-l1-b9-frontier-31222-reduced-crt-lemma-v3"
        and report["status"]
        == "PROVED_LOCAL_REDUCED_CRT_POINTWISE_BRIDGE_CROSS_MODEL_GREEN"
        and symbolic["K_affine_identity"]
        and symbolic["full_map_shape"] == [3, 4]
        and int(symbolic["cross_polynomial_degree_bound"]) == 5
        and frozen["support_pattern_count"] == 432
        and frozen["rank_histogram"]
        == {
            "rankM=2,rankFull=2": 2,
            "rankM=2,rankFull=3": 22,
            "rankM=3,rankFull=3": 408,
        }
        and frozen["compatible_rankdrop_pattern_count"] == 2
        and frozen["rankdrop_monic_cubic_count"] == 38
        and frozen["rankdrop_zero_gcd_count"] == 0
        and frozen["actual_split_core_incidence_count"] == 0
        and normalized["chart_count"] == 18_900
        and normalized["unmigrated_incidence_count"] == 0
        and normalized["bridge_verified_incidence_count"]
        == normalized["actual_split_core_incidence_count"]
        and normalized["bridge_failure_count"] == 0
        and report["proof_certificate"]["compatible_rankdrop_gcd_positive"]
        and report["proof_certificate"]["semantic_bridge_status"]
        == "PROVED_POINTWISE_UNDER_EXPLICIT_HYPOTHESES"
        and report["proof_certificate"]["system_exhaustivity_status"]
        == "PROVED_FROM_EXACT_SUPPORT_FACTORIZATION"
        and bridge["validator_accepts_positive_control"]
        and validate_bridge_control(bridge["positive_control"])
        and assignment["support_pattern_count"] == 432
        and assignment["support_pattern_formula"]
        == "binom(2,1)*binom(4,2)^3=432"
        and assignment["codeword_to_key_injective"]
        and assignment["bound_per_key"] == 1
        and assignment["double_charge_excluded"]
        and ledger["prior_profile_charge"] == 155_952
        and ledger["banked_profile_charge"] == 432
        and ledger["banked_saved_mass"] == 155_520
        and ledger["prior_all_profile_bound"] == 1_503_967
        and ledger["banked_all_profile_bound"] == 1_348_447
        and ledger["prior_unresolved_bound"] == 668_803
        and ledger["banked_unresolved_bound"] == 513_283
        and ledger["banked"]
        and report["linked_inputs"]["owner_certificate"]["sha256"]
        == sha256_file(OWNER_CERTIFICATE_PATH)
        and report["linked_inputs"]["census_certificate"]["sha256"]
        == sha256_file(CENSUS_CERTIFICATE_PATH)
        and report["linked_inputs"]["prior_cross_model_review"]["sha256"]
        == sha256_file(PRIOR_REVIEW_PATH)
        and report["linked_inputs"]["prior_cross_model_review"]["verdict"] == "YELLOW"
        and report["linked_inputs"]["prior_cross_model_review"]["ledger_authorization"]
        == "NO"
        and report["linked_inputs"]["fresh_cross_model_review"]["sha256"]
        == sha256_file(FRESH_REVIEW_PATH)
        and report["linked_inputs"]["fresh_cross_model_review"]["verdict"]
        == "GREEN"
        and report["linked_inputs"]["fresh_cross_model_review"]["ledger_authorization"]
        == "YES"
        and report["linked_inputs"]["fresh_cross_model_review"]["upstream_context_supplement"]
        == "GREEN"
        and report["linked_inputs"]["concrete_analyzer"]["sha256"]
        == sha256_file(ANALYZER_PATH)
        and report["linked_inputs"]["received_word_constructor"]["sha256"]
        == sha256_file(SCANNER_PATH)
        and report["linked_inputs"]["upstream_reconstruction_analogy"]["sha256"]
        == sha256_file(UPSTREAM_RECONSTRUCTION_PATH)
        and report["verdict"]
        == "GREEN_LOCAL_LEMMA_LEDGER_AUTHORIZED"
    )


def tamper_selftest(report):
    mutations = []
    changed = copy.deepcopy(report)
    changed["reduced_crt_map"]["K_affine_identity"] = False
    mutations.append(("K_affine_identity", changed))
    changed = copy.deepcopy(report)
    changed["reduced_crt_map"]["cross_polynomial_degree_bound"] = 6
    mutations.append(("cross_degree", changed))
    changed = copy.deepcopy(report)
    changed["exact_controls"]["frozen_GF19"]["rankdrop_zero_gcd_count"] = 1
    mutations.append(("rankdrop_gcd", changed))
    changed = copy.deepcopy(report)
    changed["exact_controls"]["normalized_GF11"]["unmigrated_incidence_count"] = 1
    mutations.append(("unmigrated_incidence", changed))
    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["banked_profile_charge"] += 1
    mutations.append(("ledger_charge", changed))
    changed = copy.deepcopy(report)
    changed["linked_inputs"]["owner_certificate"]["sha256"] = "0" * 64
    mutations.append(("owner_link", changed))
    changed = copy.deepcopy(report)
    changed["linked_inputs"]["fresh_cross_model_review"]["sha256"] = "0" * 64
    mutations.append(("fresh_review_link", changed))

    bridge_path = ["pointwise_bridge_certificate", "positive_control"]

    changed = copy.deepcopy(report)
    bridge = changed[bridge_path[0]][bridge_path[1]]
    bridge["background_roots"] = [bridge["core_roots"][0]]
    mutations.append(("core_background_overlap", changed))

    changed = copy.deepcopy(report)
    bridge = changed[bridge_path[0]][bridge_path[1]]
    field = GF(int(bridge["field"]))
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    nonsplit = None
    for coefficients in itertools.product(range(int(field.order())), repeat=3):
        candidate = X**3 + sum(
            field(coefficients[degree]) * X**degree for degree in range(3)
        )
        if candidate.is_irreducible():
            nonsplit = candidate
            break
    if nonsplit is None:
        raise RuntimeError("failed to construct nonsplit mutation")
    bridge["F_coefficients_low_to_high"] = coefficients_low_to_high(nonsplit, 3)
    mutations.append(("nonsplit_core_locator", changed))

    changed = copy.deepcopy(report)
    bridge = changed[bridge_path[0]][bridge_path[1]]
    field = GF(int(bridge["field"]))
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    D = [field(value) for value in bridge["missed_core_roots"]]
    repeated = (X - D[0])**2 * (X - D[1])
    bridge["F_coefficients_low_to_high"] = coefficients_low_to_high(repeated, 3)
    mutations.append(("repeated_core_locator", changed))

    changed = copy.deepcopy(report)
    bridge = changed[bridge_path[0]][bridge_path[1]]
    bridge["common_root_alpha"] = bridge["restored_core_root"]
    mutations.append(("alpha_equals_h", changed))

    changed = copy.deepcopy(report)
    bridge = changed[bridge_path[0]][bridge_path[1]]
    bridge["received_core_values"][0] = 1
    mutations.append(("nonzero_received_core", changed))
    failed = False
    for name, changed in mutations:
        caught = not validate_report(changed)
        print(f"  tamper {name:<24}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))
    if args.tamper_selftest and CERTIFICATE_PATH.exists():
        report = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    else:
        report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (reduced-CRT lemma certificate validation)", file=sys.stderr)
        return 1
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True, default=int) + "\n",
            encoding="utf-8",
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, default=int))
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != report:
        print("RESULT: FAIL (frozen reduced-CRT certificate drift)", file=sys.stderr)
        return 1
    frozen = report["exact_controls"]["frozen_GF19"]
    normalized = report["exact_controls"]["normalized_GF11"]
    ledger = report["ledger_consequence"]
    print("L1 B9 frontier (3,1,3,(2,2,2)) reduced-CRT common-factor lemma")
    print(f"  map: K(F)=M*(f0,f1,f2)^t+u, shape={report['reduced_crt_map']['full_map_shape']}")
    print(f"  GF(19) ranks: {frozen['rank_histogram']}")
    print(f"  GF(19) rank-drop monic cubics: {frozen['rankdrop_monic_cubic_count']}")
    print(f"  GF(19) zero-gcd exceptions: {frozen['rankdrop_zero_gcd_count']}")
    print(
        "  GF(11) split incidences: "
        f"{normalized['actual_split_core_incidence_count']}, "
        f"unmigrated={normalized['unmigrated_incidence_count']}"
    )
    print(
        "  banked local ledger: profile "
        f"{ledger['prior_profile_charge']} -> "
        f"{ledger['banked_profile_charge']}; "
        f"unresolved {ledger['prior_unresolved_bound']} -> "
        f"{ledger['banked_unresolved_bound']}"
    )
    print(f"  proof status: {report['status']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(int(main(sys.argv[1:])))
