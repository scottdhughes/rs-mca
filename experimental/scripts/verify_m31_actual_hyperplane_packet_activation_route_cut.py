#!/usr/bin/env python3
"""Verify the literal M31 packet-activation route cut and Forney replacement.

The artifact proves exact local/source theorems and deliberately fails closed
on the whole-ball M31 list bound.  Every gate uses explicit exceptions so the
optimized-Python replay is identical to the ordinary replay.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Sequence


P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
SIGMA = AGREEMENT - K
RADIUS = N - AGREEMENT
BUDGET = P**4 // 2**100
FORBIDDEN = BUDGET + 1
BASE_COMMIT = "aab74d5f882412cba3f37346b40c394086da1068"

IDENTITY_PREFIX_FLOOR = 1_993_678
GREEDY_PACKET = 230
GREEDY_LAST_FORBIDDEN = 229 + math.comb(229, 3)
GREEDY_NEXT_FORBIDDEN = 230 + math.comb(230, 3)
GREEDY_PAIR_COUNT = math.comb(GREEDY_PACKET, 2)

FIBRE_SIZE = 2**17
FIBRE_COUNT = 16
VARIABLE_FIBRES = 12
RESERVE_FIBRES = FIBRE_COUNT - VARIABLE_FIBRES
VARIABLE_WEIGHT = 4
VARIABLE_DEGREE = VARIABLE_WEIGHT * FIBRE_SIZE
COMMON_CORE = RADIUS - VARIABLE_DEGREE
RESERVE_CAPACITY = RESERVE_FIBRES * FIBRE_SIZE
ALL_FOUR_SUBSETS = math.comb(VARIABLE_FIBRES, VARIABLE_WEIGHT)
MODULE_BANDS = VARIABLE_WEIGHT + 1
MODULE_DIMENSION = MODULE_BANDS * SIGMA
ANNIHILATOR_DIMENSION_LOWER = K - MODULE_DIMENSION
LOWER_BAND_MAX_DEGREE = (VARIABLE_WEIGHT - 1) * FIBRE_SIZE + SIGMA - 1
VARIABLE_ESCAPE_DEGREE = VARIABLE_DEGREE - 1
PAIR_UNION_MIN = COMMON_CORE + (VARIABLE_WEIGHT + 1) * FIBRE_SIZE

LOW_WEIGHT_CAP = K // 2
HIGH_LAYER_COUNT = RADIUS - LOW_WEIGHT_CAP
HIGH_LAYER_MASS = FORBIDDEN - LOW_WEIGHT_CAP
SAME_WEIGHT_PACKET = (HIGH_LAYER_MASS + HIGH_LAYER_COUNT - 1) // HIGH_LAYER_COUNT

FORNEY_INDEX_COUNT = SAME_WEIGHT_PACKET - 1
SMALL_FORNEY_COUNT = FORNEY_INDEX_COUNT - 1
CUTOFF_MIN = K - RADIUS
SMALL_FORNEY_SUM_MAX = 2 * RADIUS - K - 1
MU1_MAX = SMALL_FORNEY_SUM_MAX // SMALL_FORNEY_COUNT
MU12_MAX = (2 * SMALL_FORNEY_SUM_MAX) // SMALL_FORNEY_COUNT
HIGH_SMALL_INDEX_MAX = SMALL_FORNEY_SUM_MAX // CUTOFF_MIN
LOW_INDEX_COUNT_MIN = FORNEY_INDEX_COUNT - (HIGH_SMALL_INDEX_MAX + 1)

LABEL_SUBSETS: tuple[tuple[int, int, int, int], ...] = (
    (0, 4, 7, 8),
    (1, 6, 7, 10),
    (2, 4, 7, 11),
    (3, 4, 9, 11),
    (0, 5, 6, 8),
    (2, 5, 7, 9),
    (1, 3, 7, 9),
    (4, 5, 6, 10),
    (1, 2, 4, 8),
    (0, 6, 7, 11),
    (2, 4, 7, 8),
    (5, 9, 10, 11),
    (0, 2, 4, 10),
    (0, 3, 5, 8),
    (1, 3, 4, 9),
    (2, 8, 10, 11),
    (3, 6, 9, 11),
    (1, 3, 4, 10),
    (4, 5, 7, 10),
    (2, 3, 5, 7),
    (3, 8, 9, 10),
    (1, 7, 10, 11),
    (1, 3, 8, 9),
    (0, 4, 9, 10),
    (1, 6, 9, 10),
    (4, 5, 6, 8),
    (0, 2, 9, 11),
    (2, 6, 9, 11),
    (1, 4, 8, 10),
    (1, 6, 7, 11),
    (2, 3, 4, 10),
    (0, 1, 3, 11),
    (1, 3, 5, 6),
    (2, 4, 7, 9),
    (0, 4, 6, 7),
    (1, 5, 6, 7),
)

ROOT = Path(__file__).resolve().parents[2]
PYTHON_PATH = ROOT / "experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_actual_hyperplane_packet_activation_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-actual-hyperplane-packet-activation-route-cut/README.md"
CERTIFICATE_PATH = ROOT / "experimental/data/certificates/m31-actual-hyperplane-packet-activation-route-cut/manifest.json"

SOURCE_PATHS = (
    ROOT / "tex/cs25_cap_v13_2.tex",
    ROOT / "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
    ROOT / "experimental/notes/thresholds/projective_line_lift_feasibility_wall.md",
    ROOT / "experimental/notes/thresholds/m31_scalar_descent_equivalence.md",
    ROOT / "experimental/notes/thresholds/m31_chebyshev_global_separator.md",
    ROOT / "experimental/notes/thresholds/m31_sidon_three_fibre_escape_compiler.md",
    NOTE_PATH,
    PYTHON_PATH,
    SAGE_PATH,
    README_PATH,
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(payload: Any) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal_certificate(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("certificate_sha256", None)
    out["certificate_sha256"] = hashlib.sha256(canonical_json(out)).hexdigest()
    return out


def verify_self_hash(payload: dict[str, Any]) -> None:
    claimed = payload.get("certificate_sha256")
    require(isinstance(claimed, str) and len(claimed) == 64, "certificate hash shape")
    unsealed = copy.deepcopy(payload)
    unsealed.pop("certificate_sha256", None)
    require(hashlib.sha256(canonical_json(unsealed)).hexdigest() == claimed, "certificate self hash")


def mask(labels: Sequence[int]) -> int:
    value = 0
    for label in labels:
        value ^= 1 << label
    return value


def identity_prefix_control() -> dict[str, Any]:
    numerator = math.comb(N, AGREEMENT)
    denominator = P**SIGMA
    floor_value = (numerator + denominator - 1) // denominator
    require(floor_value == IDENTITY_PREFIX_FLOOR, "identity-prefix exact ceiling")
    require(GREEDY_LAST_FORBIDDEN == 1_975_583, "230 greedy threshold")
    require(GREEDY_NEXT_FORBIDDEN == 2_001_690, "231 greedy threshold")
    require(GREEDY_LAST_FORBIDDEN < floor_value, "230 greedy extraction fits")
    require(GREEDY_NEXT_FORBIDDEN > floor_value, "same greedy proof stops before 231")
    require(GREEDY_PAIR_COUNT == 26_335, "230 pair count")
    return {
        "prefix_domain_size_formula": "p^sigma",
        "prefix_domain_size_bit_length": denominator.bit_length(),
        "support_count_formula": "binomial(n,agreement)",
        "support_count_bit_length": numerator.bit_length(),
        "heaviest_fibre_lower": floor_value,
        "locator_difference_is_exact": True,
        "exact_agreement": AGREEMENT,
        "exact_error_weight": RADIUS,
        "actual_received_word": True,
        "nonzero_syndrome": True,
        "global_projective_line_closure": True,
        "greedy_packet_size": GREEDY_PACKET,
        "greedy_last_forbidden": GREEDY_LAST_FORBIDDEN,
        "greedy_margin": floor_value - GREEDY_LAST_FORBIDDEN,
        "greedy_pair_count": GREEDY_PAIR_COUNT,
        "four_distinct_zero_xor": 0,
        "next_packet_not_certified_by_same_greedy_bound": GREEDY_PACKET + 1,
        "next_greedy_forbidden": GREEDY_NEXT_FORBIDDEN,
        "certified_lower_bound_below_budget": floor_value < BUDGET,
        "full_center_budget_status": "UNKNOWN",
    }


def explicit_fibre_control() -> dict[str, Any]:
    require(len(LABEL_SUBSETS) == SAME_WEIGHT_PACKET == 36, "36 pinned label subsets")
    require(all(tuple(sorted(labels)) == labels for labels in LABEL_SUBSETS), "labels canonical")
    require(all(len(labels) == VARIABLE_WEIGHT and len(set(labels)) == VARIABLE_WEIGHT
                for labels in LABEL_SUBSETS), "all labels have weight four")
    require(all(0 <= label < VARIABLE_FIBRES for labels in LABEL_SUBSETS for label in labels),
            "label range")
    masks = tuple(mask(labels) for labels in LABEL_SUBSETS)
    require(len(set(masks)) == len(masks), "label subsets distinct")

    pair_xors: dict[int, tuple[int, int]] = {}
    minimum_label_union = VARIABLE_FIBRES
    for left, right in itertools.combinations(range(len(masks)), 2):
        xor = masks[left] ^ masks[right]
        require(xor not in pair_xors, "all unordered pair XORs distinct")
        pair_xors[xor] = (left, right)
        minimum_label_union = min(
            minimum_label_union,
            len(set(LABEL_SUBSETS[left]) | set(LABEL_SUBSETS[right])),
        )
    require(len(pair_xors) == math.comb(36, 2) == 630, "630 pair XORs")
    require(minimum_label_union == VARIABLE_WEIGHT + 1 == 5, "minimum five-fibre union")

    zero_quartets = sum(
        1
        for indices in itertools.combinations(range(len(masks)), 4)
        if masks[indices[0]] ^ masks[indices[1]] ^ masks[indices[2]] ^ masks[indices[3]] == 0
    )
    require(zero_quartets == 0, "no zero-XOR quartet")

    require(N == FIBRE_COUNT * FIBRE_SIZE, "sixteen complete fibres")
    require(VARIABLE_DEGREE == 524_288, "variable locator degree")
    require(COMMON_CORE == 456_841, "common core size")
    require(RESERVE_CAPACITY == 524_288 and RESERVE_CAPACITY >= COMMON_CORE, "core reserve capacity")
    require(COMMON_CORE + VARIABLE_DEGREE == RADIUS, "support weight")
    require(PAIR_UNION_MIN == 1_112_201 and PAIR_UNION_MIN > K + 1, "pairwise MDS union")
    require(SIGMA < FIBRE_SIZE, "free-module band separation")
    require(MODULE_DIMENSION == 337_235 and MODULE_DIMENSION < K, "five-band module dimension")
    require(ANNIHILATOR_DIMENSION_LOWER == 711_341, "annihilator dimension lower")
    require(LOWER_BAND_MAX_DEGREE == 460_662, "lower band maximum")
    require(VARIABLE_ESCAPE_DEGREE == 524_287, "variable escape degree")
    require(LOWER_BAND_MAX_DEGREE < VARIABLE_ESCAPE_DEGREE < VARIABLE_DEGREE,
            "variable escape degree gap")
    require(ALL_FOUR_SUBSETS == 495 and ALL_FOUR_SUBSETS < P, "core-coordinate avoidance")
    require(RADIUS % 2 == AGREEMENT % 2 == 1, "odd support and agreement")

    return {
        "chebyshev_composition": "T_(2^21)=T_16(T_(2^17))",
        "fibre_count": FIBRE_COUNT,
        "fibre_size": FIBRE_SIZE,
        "variable_fibres": VARIABLE_FIBRES,
        "reserve_fibres": RESERVE_FIBRES,
        "variable_weight": VARIABLE_WEIGHT,
        "variable_degree": VARIABLE_DEGREE,
        "common_core": COMMON_CORE,
        "reserve_capacity": RESERVE_CAPACITY,
        "pinned_label_subsets": [list(labels) for labels in LABEL_SUBSETS],
        "pinned_packet_size": len(LABEL_SUBSETS),
        "pair_xor_count": len(pair_xors),
        "pair_xors_unique": True,
        "zero_xor_quartets": zero_quartets,
        "minimum_label_union": minimum_label_union,
        "minimum_support_union": PAIR_UNION_MIN,
        "mds_distance": K + 1,
        "all_four_subsets": ALL_FOUR_SUBSETS,
        "module_basis": "sum_(k=0)^4 T_s^k F_p[X]_<sigma",
        "module_band_count": MODULE_BANDS,
        "module_dimension": MODULE_DIMENSION,
        "annihilator_dimension_lower": ANNIHILATOR_DIMENSION_LOWER,
        "lower_band_max_degree": LOWER_BAND_MAX_DEGREE,
        "variable_escape_degree": VARIABLE_ESCAPE_DEGREE,
        "variable_escape_functional": "coefficient_of_Y^3_X^(s-1)",
        "variable_escapes_nonzero": True,
        "core_escape_forbidden_values_per_coordinate_upper": len(LABEL_SUBSETS),
        "all_495_core_forbidden_values_upper": ALL_FOUR_SUBSETS,
        "all_495_core_forbidden_values_below_field": True,
        "actual_common_hyperplane": True,
        "all_one_point_escapes": True,
        "global_projective_line_closure": True,
        "nontrivial_even_fibre_support_owner_blocked_by_odd_weight": True,
        "full_495_family_parity_free": False,
    }


def forney_control() -> dict[str, Any]:
    require(BUDGET == 16_777_215 and FORBIDDEN == 16_777_216, "budget arithmetic")
    require((HIGH_LAYER_MASS, HIGH_LAYER_COUNT, SAME_WEIGHT_PACKET)
            == (16_252_928, 456_841, 36), "same-weight extraction")
    require((FORNEY_INDEX_COUNT, SMALL_FORNEY_COUNT) == (35, 34), "Forney index counts")
    require(CUTOFF_MIN == SIGMA == 67_447, "minimum cutoff")
    require(SMALL_FORNEY_SUM_MAX == 913_681, "small-index sum maximum")
    require(MU1_MAX == 26_872, "mu1 maximum")
    require(MU12_MAX == 53_745 and MU12_MAX < CUTOFF_MIN, "two-row degree bound")
    require(HIGH_SMALL_INDEX_MAX == 13, "large-small-index maximum")
    require(LOW_INDEX_COUNT_MIN == 21, "at least 21 low indices")
    return {
        "forbidden_family_size": FORBIDDEN,
        "low_weight_support_cap": LOW_WEIGHT_CAP,
        "high_layer_count": HIGH_LAYER_COUNT,
        "high_layer_mass_lower": HIGH_LAYER_MASS,
        "same_weight_packet_lower": SAME_WEIGHT_PACKET,
        "admissible_error_weight_interval": [LOW_WEIGHT_CAP + 1, RADIUS],
        "common_core_symbol": "c",
        "reduced_locator_degree": "e=j-c",
        "cutoff": "D_0=K-j",
        "primitive_locator_row_columns": SAME_WEIGHT_PACKET,
        "forney_index_count": FORNEY_INDEX_COUNT,
        "forney_sum_identity": "sum(mu_i)=e",
        "source_non_surjectivity": True,
        "largest_index_lower": "mu_35>=D_0+1",
        "small_index_sum_formula": "sum_(i=1)^34 mu_i<=2j-K-c-1",
        "small_index_sum_uniform_max": SMALL_FORNEY_SUM_MAX,
        "mu1_uniform_max": MU1_MAX,
        "mu1_plus_mu2_uniform_max": MU12_MAX,
        "cutoff_uniform_min": CUTOFF_MIN,
        "mu1_plus_mu2_strictly_below_cutoff": True,
        "small_indices_at_or_above_cutoff_upper": HIGH_SMALL_INDEX_MAX,
        "indices_strictly_below_cutoff_lower": LOW_INDEX_COUNT_MIN,
        "two_independent_low_rows": True,
        "pluecker_minor_degree_upper": MU12_MAX,
        "some_pluecker_minor_nonzero": True,
        "two_column_syzygy_below_cutoff_impossible_by_mds": True,
        "multiplicity_sensitive_bound": "floor(2*(2j-K-c-1)/(M_j-2))",
        "factorized_four_face_forced": False,
        "general_rank_frame_classified": False,
    }


def validate_contract(payload: dict[str, Any]) -> None:
    require(payload["artifact_kind"] == "M31_LITERAL_PACKET_ACTIVATION_ROUTE_CUT", "artifact kind")
    require(payload["terminal"] == "MASS_PRESERVING_GENERAL_RANK_FRAME_REQUIRED", "terminal")
    require(payload["base_commit"] == BASE_COMMIT, "base commit")

    params = payload["parameters"]
    require(params == {
        "p": P,
        "n": N,
        "k": K,
        "agreement": AGREEMENT,
        "sigma": SIGMA,
        "radius": RADIUS,
        "budget": BUDGET,
        "forbidden_size": FORBIDDEN,
    }, "parameter block")

    identity = payload["identity_prefix_actual_source"]
    require(identity["heaviest_fibre_lower"] == IDENTITY_PREFIX_FLOOR, "prefix lower")
    require(identity["locator_difference_is_exact"] is True, "prefix exact support")
    require(identity["exact_error_weight"] == RADIUS, "prefix boundary weight")
    require(identity["actual_received_word"] is True, "prefix actual word")
    require(identity["global_projective_line_closure"] is True, "prefix global closure")
    require(identity["greedy_packet_size"] == GREEDY_PACKET, "prefix 230")
    require(identity["greedy_last_forbidden"] == GREEDY_LAST_FORBIDDEN, "prefix threshold")
    require(identity["four_distinct_zero_xor"] == 0, "prefix parity free")
    require(identity["certified_lower_bound_below_budget"] is True, "prefix certified lower below budget")
    require(identity["full_center_budget_status"] == "UNKNOWN", "prefix full-center budget unknown")

    fibre = payload["explicit_chebyshev_actual_source"]
    require(fibre["pinned_label_subsets"] == [list(labels) for labels in LABEL_SUBSETS], "pinned labels")
    require(fibre["pinned_packet_size"] == 36, "fibre packet")
    require(fibre["pair_xor_count"] == 630 and fibre["pair_xors_unique"] is True, "fibre pair XORs")
    require(fibre["zero_xor_quartets"] == 0, "fibre parity free")
    require(fibre["minimum_support_union"] == PAIR_UNION_MIN, "fibre MDS union")
    require(fibre["module_dimension"] == MODULE_DIMENSION, "fibre module dimension")
    require(fibre["actual_common_hyperplane"] is True, "fibre actual hyperplane")
    require(fibre["all_one_point_escapes"] is True, "fibre escapes")
    require(fibre["global_projective_line_closure"] is True, "fibre global closure")
    require(fibre["full_495_family_parity_free"] is False, "full family nonclaim")

    forney = payload["forbidden_list_forney_frame"]
    require(forney["same_weight_packet_lower"] == 36, "Forney packet")
    require(forney["source_non_surjectivity"] is True, "Forney source")
    require(forney["small_index_sum_uniform_max"] == SMALL_FORNEY_SUM_MAX, "Forney sum")
    require(forney["mu1_uniform_max"] == MU1_MAX, "Forney mu1")
    require(forney["mu1_plus_mu2_uniform_max"] == MU12_MAX, "Forney mu12")
    require(forney["mu1_plus_mu2_strictly_below_cutoff"] is True, "Forney cutoff")
    require(forney["indices_strictly_below_cutoff_lower"] == LOW_INDEX_COUNT_MIN, "Forney 21")
    require(forney["two_independent_low_rows"] is True, "Forney two rows")
    require(forney["some_pluecker_minor_nonzero"] is True, "Forney nonzero minor")
    require(forney["factorized_four_face_forced"] is False, "Forney face nonclaim")
    require(forney["general_rank_frame_classified"] is False, "Forney classification open")

    route = payload["route_cut"]
    require(route["arbitrary_packet_parity_activation_inside_retained_packet"] == "REFUTED",
            "route cut verdict")
    require(route["identity_prefix_parity_free_packet_proved"] == GREEDY_PACKET, "route cut size")
    require(route["mass_sensitive_special_packet_selection_refuted"] is False, "mass-sensitive nonclaim")
    require(route["replacement_object"] == "MULTIPLICITY_SENSITIVE_GENERAL_RANK_FORNEY_FRAME", "replacement")

    closure = payload["closure_state"]
    require(closure["closure_certified"] is False, "closure open")
    require(closure["prime_field_row_closed"] is False, "prime row open")
    require(closure["quartic_field_row_closed"] is False, "quartic row open")
    require(closure["global_add_back_proved"] is False, "add-back open")
    require(closure["ledger_movement"] == 0, "zero ledger")
    require(all(value is None for value in closure["ledger_atoms"].values()), "null atoms")
    require(closure["prize_claimed"] is False, "no prize claim")


def build_certificate() -> dict[str, Any]:
    require((P, N, K, AGREEMENT) == (2_147_483_647, 2_097_152, 1_048_576, 1_116_023),
            "deployed parameters")
    require((SIGMA, RADIUS) == (67_447, 981_129), "deployed sigma/radius")
    identity = identity_prefix_control()
    fibre = explicit_fibre_control()
    forney = forney_control()
    payload: dict[str, Any] = {
        "schema": "m31-actual-hyperplane-packet-activation-route-cut-v1",
        "artifact_kind": "M31_LITERAL_PACKET_ACTIVATION_ROUTE_CUT",
        "terminal": "MASS_PRESERVING_GENERAL_RANK_FRAME_REQUIRED",
        "base_commit": BASE_COMMIT,
        "status": "PROVED_ROUTE_CUT_AND_FORCED_GENERAL_RANK_FRAME_GLOBAL_LIST_OPEN",
        "parameters": {
            "p": P,
            "n": N,
            "k": K,
            "agreement": AGREEMENT,
            "sigma": SIGMA,
            "radius": RADIUS,
            "budget": BUDGET,
            "forbidden_size": FORBIDDEN,
        },
        "identity_prefix_actual_source": identity,
        "explicit_chebyshev_actual_source": fibre,
        "forbidden_list_forney_frame": forney,
        "route_cut": {
            "arbitrary_packet_parity_activation_inside_retained_packet": "REFUTED",
            "identity_prefix_parity_free_packet_proved": GREEDY_PACKET,
            "literal_same_weight": True,
            "actual_syndrome_hyperplane": True,
            "global_projective_line_closure_retained": True,
            "one_point_escape_retained": True,
            "mass_sensitive_special_packet_selection_refuted": False,
            "ambient_forbidden_mass_must_be_retained": True,
            "replacement_object": "MULTIPLICITY_SENSITIVE_GENERAL_RANK_FORNEY_FRAME",
        },
        "closure_state": {
            "closure_certified": False,
            "result": "MASS_PRESERVING_GENERAL_RANK_FRAME_REQUIRED",
            "prime_field_row_closed": False,
            "quartic_field_row_closed": False,
            "source_activation_to_four_face_proved": False,
            "general_rank_frame_classified": False,
            "interior_covered": False,
            "boundary_unrestricted_covered": False,
            "global_add_back_proved": False,
            "unresolved_terminals": [
                "MASS_PRESERVING_LAYER_COMPILER_OPEN",
                "MARKED_COMMON_CORE_ADDBACK_OPEN",
                "PRIMITIVE_GROWING_RANK_FRAME_INCIDENCE_OPEN",
                "INTERIOR_WEIGHT_ADDBACK_OPEN",
                "GLOBAL_DISJOINT_ADDBACK_OPEN",
            ],
            "ledger_atoms": {
                "U_paid": None,
                "U_Q": None,
                "U_A": None,
                "U_new": None,
            },
            "ledger_movement": 0,
            "prize_claimed": False,
        },
        "provenance": {
            "parent_pr": 1004,
            "parent_head": BASE_COMMIT,
            "identity_prefix_theorem": "tex/cs25_cap_v13_2.tex#lem:capff1-identity-prefix-floor",
            "forney_theorem": "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
            "global_line_theorem": "experimental/notes/thresholds/projective_line_lift_feasibility_wall.md",
            "scalar_descent": "experimental/notes/thresholds/m31_scalar_descent_equivalence.md",
            "predecessor_activation_wall": "experimental/notes/thresholds/m31_sidon_three_fibre_escape_compiler.md",
        },
        "source_sha256": {str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS},
    }
    validate_contract(payload)
    return seal_certificate(payload)


def validate_certificate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    verify_self_hash(candidate)
    validate_contract(candidate)
    require(candidate == expected, "canonical certificate payload")


def set_path(payload: dict[str, Any], path: Sequence[str], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations: tuple[tuple[tuple[str, ...], Any], ...] = (
        (("base_commit",), "0" * 40),
        (("parameters", "agreement"), AGREEMENT - 1),
        (("parameters", "sigma"), SIGMA - 1),
        (("parameters", "radius"), RADIUS - 1),
        (("parameters", "budget"), BUDGET + 1),
        (("identity_prefix_actual_source", "heaviest_fibre_lower"), IDENTITY_PREFIX_FLOOR - 1),
        (("identity_prefix_actual_source", "locator_difference_is_exact"), False),
        (("identity_prefix_actual_source", "exact_error_weight"), RADIUS - 1),
        (("identity_prefix_actual_source", "actual_received_word"), False),
        (("identity_prefix_actual_source", "global_projective_line_closure"), False),
        (("identity_prefix_actual_source", "greedy_packet_size"), 229),
        (("identity_prefix_actual_source", "greedy_last_forbidden"), GREEDY_LAST_FORBIDDEN + 1),
        (("identity_prefix_actual_source", "four_distinct_zero_xor"), 1),
        (("identity_prefix_actual_source", "certified_lower_bound_below_budget"), False),
        (("identity_prefix_actual_source", "full_center_budget_status"), "BELOW_BUDGET"),
        (("explicit_chebyshev_actual_source", "pinned_packet_size"), 35),
        (("explicit_chebyshev_actual_source", "pinned_label_subsets"), [list(x) for x in LABEL_SUBSETS[:-1]]),
        (("explicit_chebyshev_actual_source", "pair_xor_count"), 629),
        (("explicit_chebyshev_actual_source", "pair_xors_unique"), False),
        (("explicit_chebyshev_actual_source", "zero_xor_quartets"), 1),
        (("explicit_chebyshev_actual_source", "minimum_support_union"), K + 1),
        (("explicit_chebyshev_actual_source", "module_dimension"), MODULE_DIMENSION + 1),
        (("explicit_chebyshev_actual_source", "actual_common_hyperplane"), False),
        (("explicit_chebyshev_actual_source", "all_one_point_escapes"), False),
        (("explicit_chebyshev_actual_source", "global_projective_line_closure"), False),
        (("explicit_chebyshev_actual_source", "full_495_family_parity_free"), True),
        (("forbidden_list_forney_frame", "same_weight_packet_lower"), 35),
        (("forbidden_list_forney_frame", "source_non_surjectivity"), False),
        (("forbidden_list_forney_frame", "small_index_sum_uniform_max"), SMALL_FORNEY_SUM_MAX + 1),
        (("forbidden_list_forney_frame", "mu1_uniform_max"), MU1_MAX + 1),
        (("forbidden_list_forney_frame", "mu1_plus_mu2_uniform_max"), MU12_MAX + 1),
        (("forbidden_list_forney_frame", "mu1_plus_mu2_strictly_below_cutoff"), False),
        (("forbidden_list_forney_frame", "indices_strictly_below_cutoff_lower"), 20),
        (("forbidden_list_forney_frame", "two_independent_low_rows"), False),
        (("forbidden_list_forney_frame", "some_pluecker_minor_nonzero"), False),
        (("forbidden_list_forney_frame", "factorized_four_face_forced"), True),
        (("forbidden_list_forney_frame", "general_rank_frame_classified"), True),
        (("route_cut", "arbitrary_packet_parity_activation_inside_retained_packet"), "PROVED"),
        (("route_cut", "identity_prefix_parity_free_packet_proved"), 229),
        (("route_cut", "mass_sensitive_special_packet_selection_refuted"), True),
        (("route_cut", "replacement_object"), "FACTORIZED_FOUR_FACE"),
        (("closure_state", "closure_certified"), True),
        (("closure_state", "prime_field_row_closed"), True),
        (("closure_state", "quartic_field_row_closed"), True),
        (("closure_state", "global_add_back_proved"), True),
        (("closure_state", "ledger_atoms", "U_Q"), 0),
        (("closure_state", "ledger_movement"), 1),
        (("closure_state", "prize_claimed"), True),
        (("source_sha256", "experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py"),
         "0" * 64),
    )
    rejected = 0
    for path, value in mutations:
        mutated = copy.deepcopy(expected)
        set_path(mutated, path, value)
        mutated = seal_certificate(mutated)
        try:
            validate_certificate(mutated, expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {'.'.join(path)}")

    raw_hash = copy.deepcopy(expected)
    raw_hash["certificate_sha256"] = "0" * 64
    raw_payload = copy.deepcopy(expected)
    raw_payload["parameters"]["radius"] = RADIUS - 1
    for label, mutated in (("raw hash", raw_hash), ("raw payload", raw_payload)):
        try:
            validate_certificate(mutated, expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")
    require(rejected == len(mutations) + 2, "all tampers rejected")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare with the pinned manifest")
    parser.add_argument("--write", action="store_true", help="write the canonical manifest")
    parser.add_argument("--print-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    require(sum((args.check, args.write, args.print_certificate, args.tamper_selftest)) == 1,
            "select exactly one mode")
    expected = build_certificate()
    if args.print_certificate:
        print(json.dumps(expected, indent=2, sort_keys=True))
        return
    if args.write:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(f"wrote {CERTIFICATE_PATH.relative_to(ROOT)}")
        return
    if args.tamper_selftest:
        rejected = tamper_selftest(expected)
        print(f"M31 packet/Forney tampers: {rejected}/{rejected} rejected PASS")
        return
    require(CERTIFICATE_PATH.exists(), "pinned manifest exists")
    pinned = json.loads(CERTIFICATE_PATH.read_text())
    validate_certificate(pinned, expected)
    print(f"M31 actual-hyperplane packet activation route cut PASS ({CHECKS} exact checks)")
    print("RESULT: MASS_PRESERVING_GENERAL_RANK_FRAME_REQUIRED")
    print("M31 rows remain OPEN; ledger movement 0")


if __name__ == "__main__":
    main()
