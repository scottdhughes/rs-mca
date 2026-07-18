#!/usr/bin/env python3
"""Verify the post-tangent rank-nine projective source-load route cut.

The symbolic lemma is recorded in the companion note.  This checker freezes
its exact KoalaBear arithmetic and independently reconstructs four small
source-bound controls: rank-one finite, rank-one projective-infinity, and
rank-two finite-only and finite/infinity cases.  The controls are local
implication tests, not deployed selectors.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import itertools
import json
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_deployed_source_incidence_contract_v1 as base


ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    ROOT
    / "experimental/data/certificates"
    / "m1-kb-rank9-projective-source-load-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_projective_source_load_v1.json"
NOTE_REL = Path("experimental/notes/m1/m1_kb_rank9_projective_source_load_v1.md")
README_REL = Path(
    "experimental/data/certificates/m1-kb-rank9-projective-source-load-v1/README.md"
)
SCRIPT_REL = Path("experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py")
SAGE_REL = Path("experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.sage")

ATLAS_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-rank9-rich-pencil-atlas-v1/"
    "m1_kb_branch3_rank9_rich_pencil_atlas_v1.json"
)
SOURCE_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-rank9-deployed-source-incidence-contract-v1/"
    "m1_kb_rank9_deployed_source_incidence_contract_v1.json"
)
ZERO_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-rank9-zero-pencil-tangent-projection-v1/"
    "m1_kb_rank9_zero_pencil_tangent_projection_v1.json"
)
TANGENT_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-rank9-tangent-owner-splice-v1/"
    "m1_kb_rank9_tangent_owner_splice_v1.json"
)

ATLAS_PAYLOAD = "343b3bbc6ac526da12ff06988c1a280b9845f2a6117c8bc75820d55b594f6258"
SOURCE_PAYLOAD = "f35c148c23f0ef939525ac273178473152e555f6dda8270e82339508f1bf88c8"
ZERO_PAYLOAD = "50a80bcdcdcf7a38b49174d3c7107ff417c1bb4c24b94546eee93251a463c4b5"
TANGENT_PAYLOAD = "0d5753ae6055d6f1dc0edb49f0e0322596da8a70b68b113993dcec11934e7eed"

P = 2_130_706_433
EXTENSION_DEGREE = 6
N = 2**21
K = 2**20
A = 1_116_048
R = N - K
J = N - A
T = A - K
UNIFORM_CAP = 20
CUTOFF_D = 18_014
U_PAID = 2_603_484_103
B_STAR = (P**EXTENSION_DEGREE - 1) // (1 << 128)
B_REMAINING = B_STAR - U_PAID
TAIL_TARGET = 17_907_571_352_523
E_MAX = 5_284_472_953_556_748_839_425_672_939_211_329_356_986_005_299
POINT_BUDGET_QUOTIENT, POINT_BUDGET_REMAINDER = divmod(E_MAX, J)

ContractError = base.ContractError
require = base.require
payload_hash = base.payload_hash
source_binding = base.source_binding
exact_int = base.exact_int
exact_int_list = base.exact_int_list
inverse_mod = base.inverse_mod
matrix_rank_mod = base.matrix_rank_mod
polynomial_values = base.polynomial_values
polynomial_degree = base.polynomial_degree


def fraction_record(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def pad_coefficients(coefficients: list[int], width: int, prime: int) -> list[int]:
    require(len(coefficients) <= width, "coefficient vector exceeds declared k")
    return [entry % prime for entry in coefficients] + [0] * (width - len(coefficients))


def in_rs_restriction(
    values: list[int], support: list[int], domain: list[int], k: int, prime: int
) -> bool:
    generator = [
        [pow(domain[index], degree, prime) for degree in range(k)]
        for index in support
    ]
    augmented = [row + [values[index] % prime] for row, index in zip(generator, support)]
    return matrix_rank_mod(generator, prime) == matrix_rank_mod(augmented, prime)


def make_fixture(kind: str) -> dict[str, Any]:
    prime = 11
    if kind in {"RANK_TWO", "RANK_TWO_INFINITY"}:
        domain = list(range(10))
        k = 3
    else:
        domain = list(range(9))
        k = 2
    n = len(domain)
    j = 6
    selected_slopes = [2, 3, 4]
    a_word = [0] * n
    b_word = [0] * n

    if kind == "RANK_TWO":
        # P=X(X-2), Q=X-2.  The common point 2 is outside the source,
        # so the control genuinely exercises removal of the forced factor.
        p_coefficients = [0, -2, 1]
        q_coefficients = [-2, 1]
        for index in range(3, n):
            point = domain[index]
            a_word[index] = -point * (point - 2)
            b_word[index] = -(point - 2)
    elif kind == "RANK_TWO_INFINITY":
        # P=X-2, Q=(X-2)(X-1).  The plant has one finite point and one
        # projective-infinity point, while 2 remains a forced outside factor.
        p_coefficients = [-2, 1]
        q_coefficients = [2, -3, 1]
        for index in range(3, n):
            point = domain[index]
            a_word[index] = -(point - 2)
            b_word[index] = -(point - 2) * (point - 1)
    elif kind == "RANK_ONE_FINITE":
        p_coefficients = [-1]
        q_coefficients = [-1]
        for index in range(2, n):
            a_word[index] = 1
            b_word[index] = 1
        for slope in selected_slopes:
            a_word[slope] = -slope
    elif kind == "RANK_ONE_INFINITY":
        p_coefficients = [-5]
        q_coefficients = [0]
        for index in range(2, n):
            a_word[index] = 5
            b_word[index] = 0
        for slope in selected_slopes:
            a_word[slope] = -slope
            b_word[slope] = 1
    else:
        raise ContractError(f"unknown fixture kind: {kind}")

    a_word = [entry % prime for entry in a_word]
    b_word = [entry % prime for entry in b_word]
    p_values = polynomial_values(p_coefficients, domain, prime)
    q_values = polynomial_values(q_coefficients, domain, prime)
    epsilon_0 = [(left + right) % prime for left, right in zip(a_word, p_values)]
    epsilon_1 = [(left + right) % prime for left, right in zip(b_word, q_values)]

    selected: list[dict[str, Any]] = []
    for slope in selected_slopes:
        word = [(left + slope * right) % prime for left, right in zip(a_word, b_word)]
        support = [index for index, value in enumerate(word) if value]
        selected.append(
            {
                "slope": slope,
                "z": [0, 0],
                "error_support": support,
                "delta": j - len(support),
            }
        )

    expected = {
        "RANK_TWO": {
            "polynomial_pair_rank": 2,
            "rank_class": "RANK_TWO",
            "tangent_image": [0, 10],
            "projective_fibers": ["FINITE:0", "FINITE:10"],
        },
        "RANK_TWO_INFINITY": {
            "polynomial_pair_rank": 2,
            "rank_class": "RANK_TWO",
            "tangent_image": [1],
            "projective_fibers": ["FINITE:1", "INFINITY"],
        },
        "RANK_ONE_FINITE": {
            "polynomial_pair_rank": 1,
            "rank_class": "RANK_ONE_FINITE",
            "tangent_image": [10],
            "projective_fibers": ["FINITE:10"],
        },
        "RANK_ONE_INFINITY": {
            "polynomial_pair_rank": 1,
            "rank_class": "RANK_ONE_INFINITY",
            "tangent_image": [7, 8, 9],
            "projective_fibers": ["INFINITY"],
        },
    }[kind]

    return {
        "schema": "rs-mca-rank9-projective-source-load-fixture-v1",
        "scope": "EXACT_GENERIC_LOCAL_SOURCE_COUPLING_CONTROL",
        "kind": kind,
        "field_prime": prime,
        "domain": domain,
        "k": k,
        "j": j,
        "core_rank": 2,
        "uniform_cap": 2,
        "generator_rows": [[1, point] for point in domain],
        "u": a_word,
        "v": b_word,
        "source_pair": {"epsilon_0": epsilon_0, "epsilon_1": epsilon_1},
        "selected": selected,
        "line_lift": {
            "P_coefficients": [entry % prime for entry in p_coefficients],
            "Q_coefficients": [entry % prime for entry in q_coefficients],
        },
        "expected": expected,
    }


def validate_fixture(document: dict[str, Any]) -> dict[str, Any]:
    require(
        document.get("schema") == "rs-mca-rank9-projective-source-load-fixture-v1",
        "fixture schema mismatch",
    )
    require(
        document.get("scope") == "EXACT_GENERIC_LOCAL_SOURCE_COUPLING_CONTROL",
        "fixture scope mismatch",
    )
    kind = document.get("kind")
    require(
        kind
        in {
            "RANK_TWO",
            "RANK_TWO_INFINITY",
            "RANK_ONE_FINITE",
            "RANK_ONE_INFINITY",
        },
        "fixture kind",
    )
    prime = exact_int(document.get("field_prime"), "field_prime")
    domain = exact_int_list(document.get("domain"), "domain")
    require(len(domain) == len(set(domain)), "duplicate domain point")
    require(all(0 <= point < prime for point in domain), "domain point outside field")
    n = len(domain)
    k = exact_int(document.get("k"), "k")
    j = exact_int(document.get("j"), "j")
    core_rank = exact_int(document.get("core_rank"), "core_rank")
    cap = exact_int(document.get("uniform_cap"), "uniform_cap")
    agreement = n - j
    t = agreement - k
    require(1 <= k < agreement <= n, "fixture must have positive source distance")

    rows_raw = document.get("generator_rows")
    require(type(rows_raw) is list and len(rows_raw) == n, "generator row count")
    rows = [exact_int_list(row, f"generator_rows[{index}]") for index, row in enumerate(rows_raw)]
    require(all(len(row) == core_rank for row in rows), "generator row width")
    require(matrix_rank_mod(rows, prime) == core_rank, "generator matrix rank")

    u = [entry % prime for entry in exact_int_list(document.get("u"), "u")]
    v = [entry % prime for entry in exact_int_list(document.get("v"), "v")]
    require(len(u) == len(v) == n, "word length")
    source = document.get("source_pair")
    require(type(source) is dict, "missing source pair")
    epsilon_0 = [entry % prime for entry in exact_int_list(source.get("epsilon_0"), "epsilon_0")]
    epsilon_1 = [entry % prime for entry in exact_int_list(source.get("epsilon_1"), "epsilon_1")]
    require(len(epsilon_0) == len(epsilon_1) == n, "source pair length")
    sigma = [
        index
        for index, pair in enumerate(zip(epsilon_0, epsilon_1))
        if pair != (0, 0)
    ]
    require(len(sigma) <= j, "sparse source union exceeds j")

    selected_raw = document.get("selected")
    require(type(selected_raw) is list and len(selected_raw) >= cap + 1, "selected family too small")
    selected: list[dict[str, Any]] = []
    seen_slopes: set[int] = set()
    for index, raw in enumerate(selected_raw):
        require(type(raw) is dict, f"selected[{index}] not an object")
        slope = exact_int(raw.get("slope"), f"selected[{index}].slope") % prime
        require(slope not in seen_slopes, "duplicate selected slope")
        seen_slopes.add(slope)
        z = [entry % prime for entry in exact_int_list(raw.get("z"), f"selected[{index}].z")]
        require(len(z) == core_rank, "graph coordinate width")
        word = [
            (
                u[coordinate]
                + slope * v[coordinate]
                + sum(z_entry * row_entry for z_entry, row_entry in zip(z, rows[coordinate]))
            )
            % prime
            for coordinate in range(n)
        ]
        support = [coordinate for coordinate, value in enumerate(word) if value]
        declared_support = exact_int_list(raw.get("error_support"), f"selected[{index}].support")
        require(declared_support == support, "declared support mismatch")
        require(len(support) <= j, "selected error exceeds j")
        delta = exact_int(raw.get("delta"), f"selected[{index}].delta")
        require(delta == j - len(support), "deficit mismatch")
        zero_support = [coordinate for coordinate in range(n) if coordinate not in support]
        contained_0 = in_rs_restriction(epsilon_0, zero_support, domain, k, prime)
        contained_1 = in_rs_restriction(epsilon_1, zero_support, domain, k, prime)
        require(not (contained_0 and contained_1), "support-wise noncontainment failed")
        selected.append({"slope": slope, "z": z, "support": support, "zero": zero_support})

    first, second = selected[0], selected[1]
    denominator = (second["slope"] - first["slope"]) % prime
    require(denominator != 0, "line derivation denominator vanished")
    beta_vector = [
        (right - left) * inverse_mod(denominator, prime) % prime
        for left, right in zip(first["z"], second["z"])
    ]
    alpha_vector = [
        (entry - first["slope"] * direction) % prime
        for entry, direction in zip(first["z"], beta_vector)
    ]
    require(
        all(
            record["z"]
            == [
                (left + record["slope"] * right) % prime
                for left, right in zip(alpha_vector, beta_vector)
            ]
            for record in selected
        ),
        "selected graph points are not on one line",
    )
    a_word = [
        (u[index] + sum(left * entry for left, entry in zip(alpha_vector, rows[index]))) % prime
        for index in range(n)
    ]
    b_word = [
        (v[index] + sum(right * entry for right, entry in zip(beta_vector, rows[index]))) % prime
        for index in range(n)
    ]
    common_zero = [
        index
        for index, pair in enumerate(zip(a_word, b_word))
        if pair == (0, 0)
    ]
    moving_support = [index for index in range(n) if index not in common_zero]
    x_value = len(moving_support) - j
    require(x_value == 1, "fixture x value drift")
    require(len(common_zero) == agreement - x_value, "common-zero size identity")

    independent_bases = [
        basis
        for basis in itertools.combinations(common_zero, core_rank)
        if matrix_rank_mod([rows[index] for index in basis], prime) == core_rank
    ]
    basis_mass = len(independent_bases)
    line_weight = basis_mass * (len(selected) - cap)
    require(line_weight > 0, "fixture line has no positive determinant load")

    lift = document.get("line_lift")
    require(type(lift) is dict, "missing line lift")
    p_coefficients = [entry % prime for entry in exact_int_list(lift.get("P_coefficients"), "P")]
    q_coefficients = [entry % prime for entry in exact_int_list(lift.get("Q_coefficients"), "Q")]
    require(polynomial_degree(p_coefficients, prime) < k, "P degree exceeds k")
    require(polynomial_degree(q_coefficients, prime) < k, "Q degree exceeds k")
    require(polynomial_degree(p_coefficients, prime) >= 0 or polynomial_degree(q_coefficients, prime) >= 0, "zero pencil survived")
    p_values = polynomial_values(p_coefficients, domain, prime)
    q_values = polynomial_values(q_coefficients, domain, prime)
    require(
        all((epsilon_0[index] - p_values[index]) % prime == a_word[index] for index in range(n)),
        "P source coupling failed",
    )
    require(
        all((epsilon_1[index] - q_values[index]) % prime == b_word[index] for index in range(n)),
        "Q source coupling failed",
    )

    plant = sorted(set(common_zero) & set(sigma))
    outside_common = sorted(set(common_zero) - set(sigma))
    plant_floor = t - x_value + 1
    require(len(plant) == agreement - x_value - len(outside_common), "plant identity")
    require(len(plant) >= plant_floor > 0, "plant floor failed")
    projective_degree_cap = len(plant) + x_value - t - 1
    require(
        projective_degree_cap == k - 1 - len(outside_common) >= 0,
        "reduced projective degree cap identity failed",
    )
    require(
        all(p_values[index] == epsilon_0[index] and q_values[index] == epsilon_1[index] for index in plant),
        "pointwise source equality failed on plant",
    )

    tangent_image = sorted(
        {
            (-epsilon_0[index] * inverse_mod(epsilon_1[index], prime)) % prime
            for index in sigma
            if epsilon_1[index] != 0
        }
    )
    require(not (seen_slopes & set(tangent_image)), "selected slope survived inside tangent owner")

    p_row = pad_coefficients(p_coefficients, k, prime)
    q_row = pad_coefficients(q_coefficients, k, prime)
    polynomial_pair_rank = matrix_rank_mod([p_row, q_row], prime)
    require(polynomial_pair_rank in {1, 2}, "nonzero polynomial pair has invalid rank")

    point_load = Fraction(line_weight, len(plant))
    point_records: list[dict[str, Any]] = []
    fiber_loads: dict[str, Fraction] = {}
    fiber_counts: dict[str, int] = {}
    for index in plant:
        if epsilon_1[index] == 0:
            require(q_values[index] == 0 and p_values[index] != 0, "infinity chart equation failed")
            fiber = "INFINITY"
            chart = "PROJECTIVE_INFINITY"
            theta: int | None = None
        else:
            theta = (-epsilon_0[index] * inverse_mod(epsilon_1[index], prime)) % prime
            require((p_values[index] + theta * q_values[index]) % prime == 0, "finite chart equation failed")
            fiber = f"FINITE:{theta}"
            chart = "FINITE"
        fiber_loads[fiber] = fiber_loads.get(fiber, Fraction()) + point_load
        fiber_counts[fiber] = fiber_counts.get(fiber, 0) + 1
        point_records.append(
            {
                "source_index": index,
                "chart": chart,
                "theta": theta,
                "projective_fiber": fiber,
                "normalized_load": fraction_record(point_load),
            }
        )
    require(sum(fiber_loads.values(), Fraction()) == line_weight, "source-load double count failed")

    if polynomial_pair_rank == 1:
        if any(q_row):
            pivot = next(index for index, value in enumerate(q_row) if value)
            scalar = p_row[pivot] * inverse_mod(q_row[pivot], prime) % prime
            require(p_row == [(scalar * value) % prime for value in q_row], "rank-one scalar mismatch")
            zero_slope = (-scalar) % prime
            require(zero_slope in tangent_image, "rank-one finite zero slope not tangent-owned")
            require(all(record["projective_fiber"] == f"FINITE:{zero_slope}" for record in point_records), "rank-one finite plant split across fibers")
            rank_class = "RANK_ONE_FINITE"
        else:
            require(any(p_row), "rank-one infinity pair vanished")
            require(all(record["projective_fiber"] == "INFINITY" for record in point_records), "rank-one infinity plant has finite point")
            zero_slope = None
            rank_class = "RANK_ONE_INFINITY"
    else:
        zero_slope = None
        rank_class = "RANK_TWO"
        require(
            all(count <= projective_degree_cap for count in fiber_counts.values()),
            "rank-two reduced exact-root bound failed",
        )

    expected = document.get("expected")
    require(type(expected) is dict, "missing expected fixture block")
    require(expected.get("polynomial_pair_rank") == polynomial_pair_rank, "expected pair rank drift")
    require(expected.get("rank_class") == rank_class, "expected rank class drift")
    require(expected.get("tangent_image") == tangent_image, "expected tangent image drift")
    require(expected.get("projective_fibers") == sorted(fiber_loads), "expected projective fibers drift")

    return {
        "kind": kind,
        "field": f"GF({prime})",
        "n": n,
        "k": k,
        "agreement_A": agreement,
        "j": j,
        "t": t,
        "selected_slopes": sorted(seen_slopes),
        "tangent_image": tangent_image,
        "support_wise_noncontainment_checked": True,
        "common_zero_size": len(common_zero),
        "moving_support_size_M": len(moving_support),
        "x_M_minus_j": x_value,
        "independent_basis_mass_beta": basis_mass,
        "line_size_J": len(selected),
        "uniform_cap": cap,
        "line_weight": line_weight,
        "plant": plant,
        "plant_size": len(plant),
        "plant_floor_t_minus_x_plus_1": plant_floor,
        "outside_common_zero_count": len(outside_common),
        "reduced_projective_degree_cap": projective_degree_cap,
        "rank_two_fiber_bound_checked": polynomial_pair_rank == 2,
        "polynomial_pair_rank": polynomial_pair_rank,
        "rank_class": rank_class,
        "rank_one_finite_zero_slope": zero_slope,
        "source_point_loads": point_records,
        "projective_fiber_loads": [
            {"fiber": key, "load": fraction_record(value)}
            for key, value in sorted(fiber_loads.items())
        ],
        "load_sum": fraction_record(sum(fiber_loads.values(), Fraction())),
        "terminal": "GENERIC_LOCAL_PRIMITIVE_PROJECTIVE_SOURCE_FIBER_CONTROL",
        "scope": "EXACT_GENERIC_LOCAL_CONTROL_NOT_DEPLOYED_SELECTOR",
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("packet-note", NOTE_REL, "symbolic lemma, proof, and route cut"),
        source_binding("packet-readme", README_REL, "replay and scope guardrails"),
        source_binding("packet-python", SCRIPT_REL, "strict exact certificate and controls"),
        source_binding("packet-sage", SAGE_REL, "independent GF(11) controls"),
        source_binding("atlas-certificate", ATLAS_CERT_REL, "canonical E20 graph-line identity"),
        source_binding("source-contract-certificate", SOURCE_CERT_REL, "same-selector source manifest"),
        source_binding("zero-pencil-certificate", ZERO_CERT_REL, "zero-pencil projection"),
        source_binding("tangent-owner-certificate", TANGENT_CERT_REL, "post-tangent selector restart and ledger"),
    ]


def load_predecessor_documents() -> dict[str, dict[str, Any]]:
    return {
        "atlas": base.load_json(ROOT / ATLAS_CERT_REL),
        "source_contract": base.load_json(ROOT / SOURCE_CERT_REL),
        "zero_pencil": base.load_json(ROOT / ZERO_CERT_REL),
        "tangent_owner": base.load_json(ROOT / TANGENT_CERT_REL),
    }


def validate_predecessors(
    documents: dict[str, dict[str, Any]] | None = None,
    *,
    enforce_pinned_hashes: bool = True,
) -> dict[str, str]:
    docs = load_predecessor_documents() if documents is None else documents
    require(
        set(docs) == {"atlas", "source_contract", "zero_pencil", "tangent_owner"},
        "predecessor document set mismatch",
    )
    expected_payloads = {
        "atlas": ATLAS_PAYLOAD,
        "source_contract": SOURCE_PAYLOAD,
        "zero_pencil": ZERO_PAYLOAD,
        "tangent_owner": TANGENT_PAYLOAD,
    }
    for name, document in docs.items():
        require(
            document.get("payload_sha256") == payload_hash(document),
            f"bad predecessor payload: {name}",
        )
        if enforce_pinned_hashes:
            require(
                document.get("payload_sha256") == expected_payloads[name],
                f"unpinned predecessor payload: {name}",
            )

    atlas = docs["atlas"]
    require(
        atlas.get("schema")
        == "rs-mca-m1-kb-branch3-rank9-rich-pencil-atlas-v1",
        "atlas schema",
    )
    canonical_atlas = atlas.get("canonical_atlas")
    moving_zero = atlas.get("moving_zero_system")
    sparse_pencil = atlas.get("sparse_pencil")
    first_match = atlas.get("first_match_contract")
    compiler = atlas.get("compiler")
    require(type(canonical_atlas) is dict, "atlas canonical block")
    require(type(moving_zero) is dict, "atlas moving-zero block")
    require(type(sparse_pencil) is dict, "atlas sparse-pencil block")
    require(type(first_match) is dict, "atlas first-match block")
    require(type(compiler) is dict, "atlas compiler block")
    require(
        canonical_atlas.get("identity")
        == "E_20=sum_{L:J_L>=21} beta_L*(J_L-20)",
        "atlas identity drift",
    )
    require(
        canonical_atlas.get("basis_owner_is_unique") is True,
        "atlas basis ownership drift",
    )
    require(
        moving_zero.get("x_definition") == "x_L=M_L-j",
        "atlas x definition drift",
    )
    require(moving_zero.get("rich_x_max") == 49_055, "atlas rich x cap drift")
    require(sparse_pencil.get("plant_is_paid") is False, "atlas plant payment drift")
    require(
        sparse_pencil.get("branch5_status") == "UNBOUND_SOURCE_FAMILY",
        "atlas branch-5 status drift",
    )
    require(
        first_match.get("post_branches_3_5_residual_allowed") is False,
        "atlas residual status drift",
    )
    require(
        compiler.get("aggregate_gate_status")
        == "UNPROVEN_DEPLOYED_RICH_PENCIL_INCIDENCE",
        "atlas aggregate gate drift",
    )

    source = docs["source_contract"]
    require(
        source.get("schema")
        == "rs-mca-m1-kb-rank9-deployed-source-incidence-contract-v1",
        "source schema",
    )
    source_row = source.get("row")
    manifest = source.get("producer_field_manifest")
    current_inputs = source.get("current_inputs")
    source_route = source.get("route_assessment")
    implementation = source.get("implementation_scope")
    require(type(source_row) is dict, "source row block")
    require(type(manifest) is dict, "source manifest block")
    require(type(current_inputs) is dict, "source current-inputs block")
    require(type(source_route) is dict, "source route block")
    require(type(implementation) is dict, "source implementation block")
    for key, value in {
        "p": P,
        "extension_degree": EXTENSION_DEGREE,
        "n": N,
        "k": K,
        "A": A,
        "R": R,
        "j": J,
        "t": T,
        "core_rank": 8,
        "cutoff_D": CUTOFF_D,
        "uniform_cap": UNIFORM_CAP,
    }.items():
        require(source_row.get(key) == value, f"source row {key} drift")
    require(
        manifest.get("source_equalities")
        == [
            "e_eta=f+eta*g-c_eta",
            "epsilon_0=f-c_0",
            "epsilon_1=g-c_1",
            "a_L=epsilon_0-ev(P_L)",
            "b_L=epsilon_1-ev(Q_L)",
        ],
        "source equalities drift",
    )
    require(
        manifest.get("nonzero_pencil_contract")
        == [
            "at least one of P_L,Q_L is nonzero",
            "G_L divides gcd(P_L,Q_L)",
            "deg_G_L>=A-x_L-|Sigma|",
            "planted_source_count>=t-x_L+1",
        ],
        "source nonzero-pencil contract drift",
    )
    for key in [
        "complete_global_first_match_replay",
        "deployed_complete_selector_inventory",
        "deployed_rich_pencil_census",
        "deployed_rich_pencil_selector_constructed",
        "paying_selector_source_family_coverage",
        "post_branches_3_5_residual",
    ]:
        require(
            current_inputs.get(key) is False,
            f"source deployed input unexpectedly present: {key}",
        )
    require(
        source_route.get("terminal") == "UNBOUND_DEPLOYED_SOURCE_INCIDENCE",
        "source terminal drift",
    )
    require(
        source_route.get("uniform_theorem_present") is False,
        "source uniform theorem drift",
    )
    require(
        implementation.get("nonzero_pencil_gcd_and_plant_checked_by_toy_kernel")
        is False,
        "source toy plant scope drift",
    )

    validate_zero_and_tangent_predecessors(docs["zero_pencil"], docs["tangent_owner"])
    return {
        name: "payload-sha256:" + str(document["payload_sha256"])
        for name, document in docs.items()
    }


def validate_zero_and_tangent_predecessors(
    zero: dict[str, Any], tangent: dict[str, Any]
) -> None:
    require(
        zero.get("schema")
        == "rs-mca-m1-kb-rank9-zero-pencil-tangent-projection-v1",
        "zero schema",
    )
    zero_integration = zero.get("first_match_integration")
    zero_scope = zero.get("scope_guards")
    require(type(zero_integration) is dict, "zero first-match block")
    require(type(zero_scope) is dict, "zero scope block")
    require(
        zero_scope.get("local_projection_lemma_proved") is True,
        "zero local projection drift",
    )
    require(
        zero_scope.get("global_first_match_payment_proved") is False,
        "zero global payment drift",
    )
    require(
        zero_scope.get("nonzero_plant_load_bound_proved") is False,
        "zero nonzero-load drift",
    )
    require(
        zero_integration.get("delete_zero_pencil_slopes_before_rich_selector")
        is True,
        "zero deletion order drift",
    )
    require(
        zero_integration.get("residual_complete_selector_must_be_rebuilt") is True,
        "zero selector restart drift",
    )
    require(
        zero_integration.get("residual_intrinsic_rank_must_be_recomputed") is True,
        "zero rank restart drift",
    )
    require(
        zero_integration.get("global_tangent_projector_banked") is False,
        "zero global tangent status drift",
    )
    require(
        zero_integration.get("zero_pencil_atlas_term_may_be_dropped_before_global_payment")
        is False,
        "zero atlas-drop status drift",
    )

    require(
        tangent.get("schema") == "rs-mca-m1-kb-rank9-tangent-owner-splice-v1",
        "tangent schema",
    )
    tangent_owner = tangent.get("global_tangent_owner")
    restart = tangent.get("residual_selector_contract")
    tangent_scope = tangent.get("scope_guards")
    tangent_ledger = tangent.get("ledger")
    updated_gate = tangent.get("rank9_updated_gate")
    require(type(tangent_owner) is dict, "tangent owner block")
    require(type(restart) is dict, "tangent restart block")
    require(type(tangent_scope) is dict, "tangent scope block")
    require(type(tangent_ledger) is dict, "tangent ledger block")
    require(type(updated_gate) is dict, "tangent updated-gate block")
    require(
        tangent_owner.get("zero_pencil_subset_absorbed") is True,
        "tangent zero absorption drift",
    )
    require(tangent_owner.get("uniform_cap") == J, "tangent cap drift")
    require(
        tangent_owner.get("zero_pencil_separate_charge") == 0,
        "tangent zero charge drift",
    )
    require(
        tangent_owner.get("pays_all_common_or_residue_lines") is False,
        "tangent overpayment drift",
    )
    require(
        restart.get("complete_selector_universe_must_be_rebuilt") is True,
        "tangent selector restart drift",
    )
    require(
        restart.get("affine_rank_minimizer_must_be_recomputed") is True,
        "tangent rank restart drift",
    )
    require(
        restart.get("same_sp3_translation_required_downstream") is True,
        "tangent translation drift",
    )
    require(
        restart.get("surviving_zero_explaining_witness_forbidden") is True,
        "tangent zero witness drift",
    )
    require(
        restart.get("surviving_zero_rich_pencil_forbidden") is True,
        "tangent zero pencil drift",
    )
    require(
        restart.get("stale_fields_forbidden")
        == ["carrier", "V", "H_V", "K_0", "d_V", "deficits", "rich_line_atlas"],
        "tangent stale-field contract drift",
    )
    require(
        tangent_scope.get("global_tangent_owner_proved") is True,
        "tangent owner status drift",
    )
    require(
        tangent_scope.get("selector_restart_splice_proved") is True,
        "tangent restart status drift",
    )
    require(
        tangent_scope.get("zero_pencil_absorbed") is True,
        "tangent zero status drift",
    )
    require(
        tangent_scope.get("nonzero_plant_load_bound_proved") is False,
        "tangent load status drift",
    )
    require(
        tangent_scope.get("complete_rank9_payment_proved") is False,
        "tangent rank-nine status drift",
    )
    require(
        tangent_ledger.get("U_paid_before") == "2602502999",
        "tangent U_paid before drift",
    )
    require(
        tangent_ledger.get("U_paid_after") == str(U_PAID),
        "tangent U_paid after drift",
    )
    require(
        tangent_ledger.get("B_remaining_before") == "274980725508892088",
        "tangent budget before drift",
    )
    require(
        tangent_ledger.get("B_remaining_after") == str(B_REMAINING),
        "tangent budget after drift",
    )
    require(tangent_ledger.get("tangent_charge") == str(J), "tangent charge drift")
    require(
        tangent_ledger.get("ledger_movement") == str(J),
        "tangent ledger movement drift",
    )
    require(
        tangent_ledger.get("inequality_status") == "UNDECIDED_OPEN_COMPONENTS",
        "tangent inequality drift",
    )
    require(
        tangent_ledger.get("U_Q") is None and tangent_ledger.get("U_A") is None,
        "tangent open terms drift",
    )
    require(
        updated_gate.get("new_tail_target") == str(TAIL_TARGET),
        "tangent tail target drift",
    )
    require(
        updated_gate.get("new_aggregate_excess_max") == str(E_MAX),
        "tangent excess target drift",
    )
    require(
        int(tangent_ledger["U_paid_after"])
        - int(tangent_ledger["U_paid_before"])
        == J,
        "tangent U_paid bridge",
    )
    require(
        int(tangent_ledger["B_remaining_before"])
        - int(tangent_ledger["B_remaining_after"])
        == J,
        "tangent budget bridge",
    )


def expected_certificate() -> dict[str, Any]:
    predecessors = validate_predecessors()
    controls = [
        validate_fixture(make_fixture(kind))
        for kind in [
            "RANK_ONE_FINITE",
            "RANK_ONE_INFINITY",
            "RANK_TWO",
            "RANK_TWO_INFINITY",
        ]
    ]
    certificate: dict[str, Any] = {
        "schema": "rs-mca-m1-kb-rank9-projective-source-load-v1",
        "status": "PROVED_EXACT_SOURCE_LOAD_DISINTEGRATION_AND_PROJECTIVE_DICHOTOMY_DEPLOYED_PAYMENT_OPEN",
        "deployed_row": {
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "t": T,
            "uniform_cap": UNIFORM_CAP,
            "deficit_cutoff": CUTOFF_D,
        },
        "theorem_contract": {
            "residual_lines": "beta_L>0, J_L>=21, (P_L,Q_L)!=(0,0), after tangent deletion and selector restart",
            "line_weight": "w_L=beta_L*(J_L-20)",
            "full_common_zero_size": "|D\\W_L|=A-x_L",
            "rich_x_upper_bound": "x_L<=floor(j/20)=49055",
            "support_nontriviality_does_not_force_x_positive": True,
            "plant": "S_L=(D\\W_L) INTERSECT Sigma",
            "plant_size": "s_L=A-x_L-deg(G_L)>=t-x_L+1>=18418",
            "normalized_incidence": "lambda_(L,h)=w_L/s_L for h in S_L, else 0",
            "source_point_load": "Lambda_h=sum_L lambda_(L,h)",
            "exact_identity": "E_20^nz=sum_L w_L=sum_(h in Sigma) Lambda_h",
            "finite_fiber": "Sigma_theta={h:epsilon_1(h)!=0,-epsilon_0(h)/epsilon_1(h)=theta}; P_L(h)+theta Q_L(h)=0",
            "infinity_fiber": "Sigma_infinity={h:epsilon_1(h)=0}; Q_L(h)=0 and P_L(h)!=0",
            "rank_split": "rank_F span(P_L,Q_L) is exactly 1 or 2",
            "rank_one_finite": "(P_L,Q_L)=(cH,H); S_L subset Sigma_(-c); slope -c lies in the tangent image and is absent residually, but is tangent-owner-charged only if incoming; residual line load remains",
            "rank_one_infinity": "Q_L=0 after normalization; S_L subset Sigma_infinity; no finite zero-pencil slope exists",
            "rank_two": "after factoring G_L, every projective fiber has size <=d_L^proj=s_L+x_L-t-1",
            "current_deployed_terminal": "UNBOUND_POST_TANGENT_SOURCE_LOAD",
            "future_actual_component_terminal": "UNPAID_PRIMITIVE_PROJECTIVE_SOURCE_FIBER",
        },
        "rank_two_reduced_root_gate": {
            "outside_common_root_count": "c_L=A-x_L-s_L",
            "reduced_degree": "k-1-c_L=s_L+x_L-t-1",
            "d_eff_zero_forces_rank_one": True,
            "d_eff_one_makes_source_labels_injective": True,
            "unreduced_k_minus_1": K - 1,
            "source_support_cap_j": J,
            "unreduced_bound_is_vacuous": K - 1 > J,
            "reduced_gate_pays_all_weight": False,
        },
        "same_selector_incidence": {
            "plant_equations": "g_h*alpha_L=-u(h) and g_h*beta_vec_L=-v(h)",
            "finite_projective_equation": "u(h)+theta*v(h)+g_h*(alpha_L+theta*beta_vec_L)=0",
            "ambient_exact_pair_rank_when_g_h_nonzero": 2,
            "component_restricted_rank_drop_requires_owner_or_exact_count": True,
            "source_h_outside_V_is_universal_rank_zero_edge_case": True,
            "non_source_h_outside_V_belongs_to_C_L_not_S_L": True,
        },
        "pointwise_sufficient_gate": {
            "E_max": str(E_MAX),
            "source_support_cap_j": J,
            "uniform_rational_cap": f"{E_MAX}/{J}",
            "quotient": str(POINT_BUDGET_QUOTIENT),
            "remainder": POINT_BUDGET_REMAINDER,
            "claim": "Lambda_h<=E_max/j for every h implies E_20^nz<=E_max",
            "implication_proved_here": True,
            "antecedent_proved_here": False,
        },
        "ledger": {
            "B_star": str(B_STAR),
            "U_paid": str(U_PAID),
            "B_remaining": str(B_REMAINING),
            "tail_target": str(TAIL_TARGET),
            "E_max": str(E_MAX),
            "ledger_movement": 0,
            "U_Q": None,
            "U_A": None,
            "row_status": "YELLOW_OPEN_NONZERO_PROJECTIVE_SOURCE_FIBER",
        },
        "same_selector_chain": {
            "fixed_sp3_translation": True,
            "tangent_deleted_before_selector_restart": True,
            "post_deletion_selector_data_required": True,
            "same_records_feed_line_weight_and_source_plant": True,
            "cross_selector_mixing_forbidden": True,
            "rank_at_least_ten_authorized": False,
        },
        "exact_controls": controls,
        "route_cut": {
            "rank_one_finite_positive_load_survives_tangent_deletion": True,
            "rank_one_infinity_positive_load_survives": True,
            "rank_two_positive_load_survives": True,
            "controls_are_deployed_selectors": False,
            "actual_deployed_primitive_component_exhibited": False,
            "local_identity_plus_rank_split_implies_payment": False,
            "current_deployed_terminal": "UNBOUND_POST_TANGENT_SOURCE_LOAD",
            "future_actual_component_terminal": "UNPAID_PRIMITIVE_PROJECTIVE_SOURCE_FIBER",
            "route_cut_is_new_nonpayment_information": True,
        },
        "nonclaims": [
            "The exact GF(11) controls are not rank-nine or deployed-field selectors.",
            "The packet does not prove a uniform projective source-fiber load bound.",
            "The packet does not route rank-one load to the tangent slope charge.",
            "The packet does not infer a post-branches-3--5 complement.",
            "The packet does not determine U_Q or U_A or close KoalaBear.",
            "The packet does not authorize rank at least ten, Lean, or stable-paper promotion.",
        ],
        "predecessors": predecessors,
        "source_bindings": expected_source_bindings(),
    }
    certificate["payload_sha256"] = payload_hash(certificate)
    return certificate


def strict_match(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type mismatch at {path}")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"key mismatch at {path}")
        for key in expected:
            strict_match(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_match(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"value mismatch at {path}")


def validate_certificate(document: dict[str, Any]) -> None:
    require(document.get("payload_sha256") == payload_hash(document), "payload hash mismatch")
    strict_match(document, expected_certificate())


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def certificate_mutations() -> list[Mutation]:
    return [
        ("status", lambda d: d.__setitem__("status", "PROVED_DEPLOYED_PAYMENT")),
        ("x-upper", lambda d: d["theorem_contract"].__setitem__("rich_x_upper_bound", "x_L<=49056")),
        ("false-x-floor", lambda d: d["theorem_contract"].__setitem__("support_nontriviality_does_not_force_x_positive", False)),
        ("plant-floor", lambda d: d["theorem_contract"].__setitem__("plant_size", "s_L>=0")),
        ("identity", lambda d: d["theorem_contract"].__setitem__("exact_identity", "E_20^nz=0")),
        ("finite-fiber", lambda d: d["theorem_contract"].__setitem__("finite_fiber", "UNBOUND")),
        ("infinity-fiber", lambda d: d["theorem_contract"].__setitem__("infinity_fiber", "EMPTY")),
        ("rank-split", lambda d: d["theorem_contract"].__setitem__("rank_split", "rank=2")),
        ("force-owner", lambda d: d["theorem_contract"].__setitem__("current_deployed_terminal", "SPARSE_TANGENT_OWNER")),
        ("root-cap", lambda d: d["rank_two_reduced_root_gate"].__setitem__("reduced_gate_pays_all_weight", True)),
        ("universal-source-point", lambda d: d["same_selector_incidence"].__setitem__("source_h_outside_V_is_universal_rank_zero_edge_case", False)),
        ("outside-nonsource-point", lambda d: d["same_selector_incidence"].__setitem__("non_source_h_outside_V_belongs_to_C_L_not_S_L", False)),
        ("point-budget", lambda d: d["pointwise_sufficient_gate"].__setitem__("quotient", str(POINT_BUDGET_QUOTIENT + 1))),
        ("point-remainder", lambda d: d["pointwise_sufficient_gate"].__setitem__("remainder", POINT_BUDGET_REMAINDER + 1)),
        ("implication-unproved", lambda d: d["pointwise_sufficient_gate"].__setitem__("implication_proved_here", False)),
        ("antecedent-proved", lambda d: d["pointwise_sufficient_gate"].__setitem__("antecedent_proved_here", True)),
        ("ledger", lambda d: d["ledger"].__setitem__("ledger_movement", 1)),
        ("UQ", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("cross-selector", lambda d: d["same_selector_chain"].__setitem__("cross_selector_mixing_forbidden", False)),
        ("rank10", lambda d: d["same_selector_chain"].__setitem__("rank_at_least_ten_authorized", True)),
        ("rank1-paid", lambda d: d["route_cut"].__setitem__("rank_one_finite_positive_load_survives_tangent_deletion", False)),
        ("deployed-controls", lambda d: d["route_cut"].__setitem__("controls_are_deployed_selectors", True)),
        ("payment", lambda d: d["route_cut"].__setitem__("local_identity_plus_rank_split_implies_payment", True)),
        ("control-load", lambda d: d["exact_controls"][0].__setitem__("line_weight", 0)),
        ("control-chart", lambda d: d["exact_controls"][1]["source_point_loads"][0].__setitem__("chart", "FINITE")),
        ("control-rank", lambda d: d["exact_controls"][2].__setitem__("polynomial_pair_rank", 1)),
        ("control-factor", lambda d: d["exact_controls"][2].__setitem__("outside_common_zero_count", 0)),
        ("control-reduced-cap", lambda d: d["exact_controls"][2].__setitem__("reduced_projective_degree_cap", 2)),
        ("control-rank2-infinity", lambda d: d["exact_controls"][3]["source_point_loads"][1].__setitem__("chart", "FINITE")),
        ("predecessor", lambda d: d["predecessors"].__setitem__("tangent_owner", "payload-sha256:00")),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "00")),
        ("payload", lambda d: d.__setitem__("payload_sha256", "00")),
    ]


def fixture_mutations() -> list[tuple[str, str, Callable[[dict[str, Any]], None]]]:
    return [
        ("rank2-tangent-slope", "RANK_TWO", lambda d: d["selected"][0].__setitem__("slope", 0)),
        ("rank2-zero-pencil", "RANK_TWO", lambda d: d.__setitem__("line_lift", {"P_coefficients": [0], "Q_coefficients": [0]})),
        ("rank2-source", "RANK_TWO", lambda d: d["source_pair"]["epsilon_0"].__setitem__(0, 1)),
        ("rank2-support", "RANK_TWO", lambda d: d["selected"][0].__setitem__("error_support", [])),
        ("rank2-contained", "RANK_TWO", lambda d: d.__setitem__("k", 4)),
        ("rank1f-tangent", "RANK_ONE_FINITE", lambda d: d["selected"][0].__setitem__("slope", 10)),
        ("rank1f-Q", "RANK_ONE_FINITE", lambda d: d["line_lift"].__setitem__("Q_coefficients", [1])),
        ("rank1f-sigma", "RANK_ONE_FINITE", lambda d: d["source_pair"]["epsilon_1"].__setitem__(8, 1)),
        ("rank1i-P", "RANK_ONE_INFINITY", lambda d: d["line_lift"].__setitem__("P_coefficients", [0])),
        ("rank1i-Q", "RANK_ONE_INFINITY", lambda d: d["line_lift"].__setitem__("Q_coefficients", [1])),
        ("rank1i-tangent", "RANK_ONE_INFINITY", lambda d: d["selected"][0].__setitem__("slope", 7)),
        ("rank1i-deficit", "RANK_ONE_INFINITY", lambda d: d["selected"][0].__setitem__("delta", 1)),
        ("rank2i-Q", "RANK_TWO_INFINITY", lambda d: d["line_lift"].__setitem__("Q_coefficients", [2, -3, 0])),
        ("rank2i-infinity", "RANK_TWO_INFINITY", lambda d: d["source_pair"]["epsilon_1"].__setitem__(1, 1)),
    ]


def predecessor_semantic_mutations() -> list[tuple[str, str, Callable[[dict[str, Any]], None]]]:
    return [
        (
            "atlas-identity",
            "atlas",
            lambda d: d["canonical_atlas"].__setitem__("identity", "E_20=0"),
        ),
        (
            "atlas-plant-paid",
            "atlas",
            lambda d: d["sparse_pencil"].__setitem__("plant_is_paid", True),
        ),
        (
            "source-selector-present",
            "source_contract",
            lambda d: d["current_inputs"].__setitem__(
                "deployed_complete_selector_inventory", True
            ),
        ),
        (
            "source-uniform-theorem",
            "source_contract",
            lambda d: d["route_assessment"].__setitem__(
                "uniform_theorem_present", True
            ),
        ),
        (
            "zero-global-payment",
            "zero_pencil",
            lambda d: d["scope_guards"].__setitem__(
                "global_first_match_payment_proved", True
            ),
        ),
        (
            "zero-no-restart",
            "zero_pencil",
            lambda d: d["first_match_integration"].__setitem__(
                "residual_complete_selector_must_be_rebuilt", False
            ),
        ),
        (
            "tangent-load-paid",
            "tangent_owner",
            lambda d: d["scope_guards"].__setitem__(
                "nonzero_plant_load_bound_proved", True
            ),
        ),
        (
            "tangent-ledger",
            "tangent_owner",
            lambda d: d["ledger"].__setitem__("U_paid_after", "2603484104"),
        ),
    ]


def run_tamper_selftest() -> int:
    expected = expected_certificate()
    rejected = 0
    for name, mutate in certificate_mutations():
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        if name != "payload":
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except ContractError:
            rejected += 1
        else:
            raise ContractError(f"certificate mutation survived: {name}")
    for name, kind, mutate in fixture_mutations():
        candidate = make_fixture(kind)
        mutate(candidate)
        try:
            validate_fixture(candidate)
        except ContractError:
            rejected += 1
        else:
            raise ContractError(f"fixture mutation survived: {name}")
    for name, predecessor, mutate in predecessor_semantic_mutations():
        candidate_documents = copy.deepcopy(load_predecessor_documents())
        mutate(candidate_documents[predecessor])
        candidate_documents[predecessor]["payload_sha256"] = payload_hash(
            candidate_documents[predecessor]
        )
        try:
            validate_predecessors(
                candidate_documents,
                enforce_pinned_hashes=False,
            )
        except ContractError:
            rejected += 1
        else:
            raise ContractError(f"predecessor semantic mutation survived: {name}")
    total = (
        len(certificate_mutations())
        + len(fixture_mutations())
        + len(predecessor_semantic_mutations())
    )
    require(rejected == total, "mutation count mismatch")
    print(f"M1 projective source-load mutations: {rejected}/{total} PASS")
    return 0


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(expected_certificate(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return run_tamper_selftest()
    if args.print_certificate:
        print(json.dumps(expected_certificate(), indent=2, sort_keys=True))
        return 0
    if args.write:
        write_certificate()
        print(CERT_PATH)
        return 0
    document = base.load_json(CERT_PATH)
    validate_certificate(document)
    print("M1 KoalaBear projective source-load route cut: PASS")
    print("  E_20^nz = sum_L w_L = sum_h Lambda_h")
    print("  positive plant floor and finite/infinity, rank-1/rank-2 split frozen")
    print("  current terminal: UNBOUND_POST_TANGENT_SOURCE_LOAD")
    print("  deployed incidence and KoalaBear row remain YELLOW; ledger movement 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
