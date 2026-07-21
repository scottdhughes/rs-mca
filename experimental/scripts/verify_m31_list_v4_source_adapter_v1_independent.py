#!/usr/bin/env python3
"""Independent replay of the M31 LIST v4 source-adapter certificate.

This verifier intentionally does not import the primary verifier.  It derives
the M31 row, scalar-descent, packing, signed-occupancy, and coupled rank-46
arithmetic from first principles, verifies the five-atom LIST chronology, and
checks every pinned source byte-for-byte.  All assertions remain active under
``python -O``.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = (
    ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json"
)

SCHEMA_ID = "rs-mca-m31-list-v4-source-adapter-v1"
ARCHITECTURE_ID = "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
OPEN_STATUS = "OPEN_ROUTE_CUT_UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL"
ATOM_ORDER = ["U_paid", "U_Q", "U_list_int", "U_ext", "U_new"]
UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"
QUANTIFIER = "UNIFORM_OVER_ALL_RECEIVED_WORDS"

P = 2**31 - 1
M = 4
Q = P**M
N = 2**21
K = 2**20
A = 1_116_023
W = A - K
R = N - A
TARGET_EXPONENT = 100
B_STAR = Q // 2**TARGET_EXPONENT
L = B_STAR + 1

J0 = 614_160
LOW_CAP = 3_730
FIRST_EXCLUDED = LOW_CAP + 1
H = R - J0
FREE = 45
BASELINE_HIGH = FREE * H
BASE_MASS = LOW_CAP + BASELINE_HIGH
SAFE_XI = B_STAR - BASE_MASS
FORCED_XI = L - BASE_MASS
HIGH_MASS_MIN = L - LOW_CAP

COLUMNS = 46
ANCHORS = 45
FORNEY_COUNT = 44
FORNEY_SUM_MAX = 2 * R - K - 1
CUTOFF_MIN = K - R

GLOBAL_TERMINAL = "UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL"
BOUNDARY_CELL = "HIGH_BOUNDARY_EXACT_CODEWORD"
INTERIOR_CELL = "HIGH_INTERIOR_EXACT_CODEWORD"
BOUNDARY_TERMINAL = "UNPAID_BOUNDARY_CODEWORD_RESIDUAL"
INTERIOR_TERMINAL = "UNPAID_INTERIOR_CODEWORD_RESIDUAL"

SOURCE_PATHS: tuple[tuple[str, str], ...] = (
    ("adapter_schema", "experimental/data/schemas/m31_list_v4_source_adapter_v1.schema.json"),
    ("adapter_verifier", "experimental/scripts/verify_m31_list_v4_source_adapter_v1.py"),
    ("adapter_note", "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md"),
    ("adapter_independent_verifier", "experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py"),
    ("adapter_sage_verifier", "experimental/scripts/verify_m31_list_v4_source_adapter_v1.sage"),
    ("active_v4_ledger", "experimental/grande_finale.tex"),
    ("admissibility_authority", "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex"),
    ("deployed_row_packet", "experimental/data/certificates/frontier-adjacent/m31_list_v1.packet.json"),
    ("scalar_descent_theorem", "experimental/notes/thresholds/m31_scalar_descent_equivalence.md"),
    ("scalar_descent_verifier", "experimental/scripts/verify_m31_scalar_descent_equivalence.py"),
    ("full_layer_source", "experimental/notes/thresholds/m31_full_packet_pade_forney_source.md"),
    ("full_layer_verifier", "experimental/scripts/verify_m31_full_packet_pade_forney.py"),
    ("rank46_source", "experimental/notes/thresholds/m31_canonical_popov_rank46_compiler.md"),
    ("rank46_verifier", "experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py"),
    ("rank46_manifest", "experimental/data/certificates/m31-canonical-popov-rank46-compiler/manifest.json"),
    ("coupled_source", "experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md"),
    ("coupled_verifier", "experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py"),
    ("coupled_manifest", "experimental/data/certificates/m31-coupled-escape-forney-plucker-route-cut/manifest.json"),
)


class VerificationError(RuntimeError):
    """Fail-closed certificate error."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def strict_int(token: str) -> int:
    require(len(token.lstrip("-")) <= 96, "JSON integer digit bound")
    return int(token)


def reject_float(_token: str) -> Any:
    raise VerificationError("JSON floating-point values are forbidden")


def reject_constant(_token: str) -> Any:
    raise VerificationError("JSON non-finite values are forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("non-canonicalizable JSON value") from exc
    return (text + "\n").encode("ascii")


def strict_load(path: Path) -> tuple[dict[str, Any], bytes]:
    require(path.is_file(), f"manifest exists: {path}")
    raw = path.read_bytes()
    require(len(raw) <= 64 * 1024 * 1024, "manifest size bound")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("manifest is not ASCII") from exc
    value = json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_int=strict_int,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, "manifest root object")
    require(raw == canonical_json(value), "manifest canonical JSON bytes")
    return value, raw


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def payload_digest(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def partition_digest(partition: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(partition)
    unsigned.pop("partition_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def exact_keys(value: Any, keys: Iterable[str], label: str) -> None:
    require(type(value) is dict, f"{label}: object")
    require(set(value) == set(keys), f"{label}: exact keys")


def exact_type_value(actual: Any, expected: Any, label: str) -> None:
    require(type(actual) is type(expected), f"{label}: exact type")
    require(actual == expected, f"{label}: exact value")


def integer(value: Any, label: str) -> int:
    require(type(value) is int, f"{label}: integer")
    return value


def decimal(value: Any, label: str) -> int:
    require(type(value) is str and re.fullmatch(r"0|[1-9][0-9]*", value) is not None, f"{label}: decimal string")
    require(len(value) <= 96, f"{label}: decimal length")
    return int(value)


def check_ascii(value: Any, path: str = "manifest") -> None:
    if isinstance(value, str):
        require(value.isascii(), f"{path}: ASCII")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_ascii(child, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, child in value.items():
            require(type(key) is str and key.isascii(), f"{path}: ASCII key")
            check_ascii(child, f"{path}.{key}")


def balanced_pair_lower(member_count: int, set_size: int) -> int:
    quotient, remainder = divmod(member_count * set_size, N)
    return N * math.comb(quotient, 2) + remainder * quotient


def ordered_prefix_bound(total: int, count: int, prefix: int) -> int:
    """Maximum first-prefix sum for a nondecreasing nonnegative count-tuple."""
    quotient, remainder = divmod(total, count)
    return prefix * quotient + max(0, remainder - (count - prefix))


def validate_row(row: Any) -> None:
    expected = {
        "row_id": "m31_list",
        "object_kind": "LIST",
        "base_prime": P,
        "extension_degree": M,
        "code_field_cardinality": str(Q),
        "q_gen": P,
        "q_line": str(Q),
        "q_chal": str(Q),
        "q_list": str(Q),
        "n": N,
        "K": K,
        "agreement": A,
        "shift": W,
        "radius": R,
        "target_exponent": TARGET_EXPONENT,
        "B_star": B_STAR,
        "forbidden_size": L,
        "endpoint": "CLOSED_RADIUS",
        "domain_in_base_field": True,
        "unit": UNIT,
        "quantifier": QUANTIFIER,
    }
    exact_keys(row, expected, "row_contract")
    for key, value in expected.items():
        exact_type_value(row[key], value, f"row_contract.{key}")
    require(P == 2_147_483_647, "M31 prime constant")
    require((N, K, A, W, R) == (2_097_152, 1_048_576, 1_116_023, 67_447, 981_129), "row arithmetic")
    require(Q == 21_267_647_892_944_572_736_998_860_269_687_930_881, "quartic field cardinality")
    require((B_STAR, L) == (16_777_215, 16_777_216), "target floor and forbidden size")


def validate_transport(transport: Any) -> None:
    exact_keys(
        transport,
        {
            "kind",
            "direct_target_field_lift",
            "scalar_descent_crosscheck",
            "scalar_descent_is_sole_transport",
            "U_ext_zero_claimed",
        },
        "source_transport",
    )
    require(transport["kind"] == "DIRECT_TARGET_FIELD_LIFT", "transport kind")
    require(transport["scalar_descent_is_sole_transport"] is False, "scalar descent is not sole transport")
    require(transport["U_ext_zero_claimed"] is False, "transport does not claim U_ext=0")

    direct = transport["direct_target_field_lift"]
    direct_expected = {
        "transport_id": "M31_DIRECT_TARGET_FIELD_SOURCE_LIFT",
        "kind": "DIRECT_TARGET_FIELD_LIFT",
        "field": "F_(p^4)",
        "evaluation_domain_subfield": "F_p",
        "field_generic": True,
        "full_target_list_objectwise": True,
        "exact_supports_objectwise": True,
        "one_point_escapes_objectwise": True,
        "full_layer_common_core_objectwise": True,
        "pade_and_coupled_kernel_objectwise": True,
        "low_weight_packing_field_independent": True,
        "uniform_over_all_received_words": True,
        "ledger_atom": None,
        "theorem_pointer": "m31_list_v4_source_adapter_global_coupled_residual.md#lemma-2.1",
        "source_binding_roles": ["adapter_note", "admissibility_authority", "full_layer_source", "coupled_source"],
    }
    exact_keys(direct, direct_expected, "direct_target_field_lift")
    for key, value in direct_expected.items():
        exact_type_value(direct[key], value, f"direct_target_field_lift.{key}")

    scalar = transport["scalar_descent_crosscheck"]
    scalar_keys = {
        "transport_id", "kind", "role", "from_field", "to_field", "extension_degree",
        "threshold_L", "t", "g", "projective_functionals",
        "functionals_killing_fixed_nonzero", "left_LtH", "right_gN", "strict_margin",
        "strict_inequality", "domain_in_base_field", "agreement_preserved",
        "new_agreements_may_appear", "exact_error_supports_preserved",
        "selected_codewords_injective", "selected_L_sublist_only",
        "public_objectwise_partition_map", "uniform_over_all_received_words",
        "threshold_predicates_equivalent", "full_list_cardinality_bijection_claimed",
        "ledger_atom", "source_binding_roles",
    }
    exact_keys(scalar, scalar_keys, "scalar_descent_crosscheck")
    fixed = {
        "transport_id": "M31_SCALAR_DESCENT_THRESHOLD_L",
        "kind": "THRESHOLD_L_INJECTION_NOT_FULL_LIST_BIJECTION",
        "role": "INDEPENDENT_THRESHOLD_CROSSCHECK_ONLY",
        "from_field": "F_(p^4)",
        "to_field": "F_p",
        "extension_degree": M,
        "threshold_L": L,
        "t": R,
        "g": W + 1,
        "strict_inequality": True,
        "domain_in_base_field": True,
        "agreement_preserved": True,
        "new_agreements_may_appear": True,
        "exact_error_supports_preserved": False,
        "selected_codewords_injective": True,
        "selected_L_sublist_only": True,
        "public_objectwise_partition_map": False,
        "uniform_over_all_received_words": True,
        "threshold_predicates_equivalent": True,
        "full_list_cardinality_bijection_claimed": False,
        "ledger_atom": None,
        "source_binding_roles": ["scalar_descent_theorem", "scalar_descent_verifier"],
    }
    for key, value in fixed.items():
        exact_type_value(scalar[key], value, f"scalar_descent_crosscheck.{key}")

    projective = (P**M - 1) // (P - 1)
    killing = (P ** (M - 1) - 1) // (P - 1)
    left = L * R * killing
    right = (W + 1) * projective
    margin = right - left
    require(projective == 9_903_520_305_059_670_166_633_185_280, "projective functional count")
    require(killing == 4_611_686_016_279_904_257, "annihilating functional count")
    require(decimal(scalar["projective_functionals"], "projective_functionals") == projective, "projective functional replay")
    require(decimal(scalar["functionals_killing_fixed_nonzero"], "killing_functionals") == killing, "killing functional replay")
    require(decimal(scalar["left_LtH"], "left_LtH") == left, "scalar left replay")
    require(decimal(scalar["right_gN"], "right_gN") == right, "scalar right replay")
    require(decimal(scalar["strict_margin"], "strict_margin") == margin, "scalar margin replay")
    require(left < right, "strict scalar-descent inequality")
    require(margin == 592_061_458_020_761_914_489_814_638_395_392, "scalar-descent exact margin")


def validate_low_packing(universe: Any) -> None:
    require(universe["small_ball_weight_interval"] == [0, K // 2], "small-ball interval")
    require(universe["small_ball_total_mass_cap"] == 1, "small-ball total cap")
    large_count = R - K // 2
    require(universe["large_layer_weight_interval"] == [K // 2 + 1, R], "large-layer interval")
    require(universe["large_layer_count"] == large_count == 456_841, "large-layer count")
    forced_layer = (L - 1 + large_count - 1) // large_count
    require(universe["same_weight_layer_forced_lower"] == forced_layer == 37, "same-weight layer lower bound")

    packing = universe["low_weight_packing"]
    packing_keys = {
        "selected_agreement_subset_size", "pair_intersection_upper", "feasible_count",
        "feasible_margin", "first_excluded_count", "first_excluded_contradiction_margin",
        "integer_rounding_is_load_bearing", "codeword_to_selected_subset_injective",
    }
    exact_keys(packing, packing_keys, "low_weight_packing")
    set_size = N - J0
    intersection = K - 1
    feasible_lower = balanced_pair_lower(LOW_CAP, set_size)
    feasible_upper = math.comb(LOW_CAP, 2) * intersection
    excluded_lower = balanced_pair_lower(FIRST_EXCLUDED, set_size)
    excluded_upper = math.comb(FIRST_EXCLUDED, 2) * intersection
    expected = {
        "selected_agreement_subset_size": set_size,
        "pair_intersection_upper": intersection,
        "feasible_count": LOW_CAP,
        "feasible_margin": feasible_upper - feasible_lower,
        "first_excluded_count": FIRST_EXCLUDED,
        "first_excluded_contradiction_margin": excluded_lower - excluded_upper,
        "integer_rounding_is_load_bearing": True,
        "codeword_to_selected_subset_injective": True,
    }
    for key, value in expected.items():
        exact_type_value(packing[key], value, f"low_weight_packing.{key}")
    require(expected["feasible_margin"] == 202_311, "feasible packing margin")
    require(expected["first_excluded_contradiction_margin"] == 19_019, "first-excluded packing contradiction")


def recompute_extremizer(blocks: Any) -> dict[str, Any]:
    require(type(blocks) is list and len(blocks) >= 1, "extremizer blocks")
    levels = [0] * COLUMNS
    previous_end = -1
    previous_signature: tuple[int, str, int] | None = None
    occupied = total = low = high = raw_tail = boundary = interior = 0
    block_keys = {"weight_start", "weight_end", "multiplicity_per_weight", "layer_class", "rank46_keys_per_weight"}
    for index, block in enumerate(blocks):
        exact_keys(block, block_keys, f"extremizer block {index}")
        start = integer(block["weight_start"], f"extremizer block {index} start")
        end = integer(block["weight_end"], f"extremizer block {index} end")
        multiplicity = integer(block["multiplicity_per_weight"], f"extremizer block {index} multiplicity")
        keys = integer(block["rank46_keys_per_weight"], f"extremizer block {index} keys")
        layer_class = block["layer_class"]
        require(0 <= start <= end <= R and start > previous_end, f"extremizer block {index} ordered range")
        require(multiplicity >= 1, f"extremizer block {index} positive multiplicity")
        if end <= J0:
            require(layer_class == "LOW_PREFIX", f"extremizer block {index} low class")
            expected_keys = 0
        elif J0 < start and end < R:
            require(layer_class == "HIGH_INTERIOR", f"extremizer block {index} interior class")
            expected_keys = max(0, multiplicity - FREE)
        else:
            require(start == end == R and layer_class == "BOUNDARY", f"extremizer block {index} boundary class")
            expected_keys = max(0, multiplicity - FREE)
        require(keys == expected_keys, f"extremizer block {index} marked keys")
        signature = (multiplicity, layer_class, keys)
        require(not (start == previous_end + 1 and signature == previous_signature), f"extremizer block {index} maximal RLE")
        length = end - start + 1
        occupied += length
        total += length * multiplicity
        if layer_class == "LOW_PREFIX":
            low += length * multiplicity
        else:
            high += length * multiplicity
            raw_tail += length * keys
            for level in range(1, COLUMNS + 1):
                if multiplicity >= level:
                    levels[level - 1] += length
            if layer_class == "BOUNDARY":
                boundary += length * keys
            else:
                interior += length * keys
        previous_end = end
        previous_signature = signature

    low_credit = LOW_CAP - low
    require(low_credit >= 0, "extremizer low credit")
    level_credit = sum(H - levels[level - 1] for level in range(1, FREE + 1))
    require(level_credit >= 0, "extremizer level credit")
    signed = raw_tail - low_credit - level_credit
    require(total == BASE_MASS + signed, "extremizer signed mass identity")
    return {
        "occupancy_level_counts": [
            {"level": level, "occupied_high_layers": levels[level - 1]}
            for level in range(1, COLUMNS + 1)
        ],
        "occupied_weight_count": occupied,
        "total_mass": total,
        "low_mass": low,
        "high_mass": high,
        "base_mass": BASE_MASS,
        "raw_rank46_tail": raw_tail,
        "low_credit": low_credit,
        "level_credit_sum": level_credit,
        "signed_occupancy": signed,
        "safe_signed_occupancy_max": SAFE_XI,
        "forbidden_signed_occupancy_min": FORCED_XI,
        "interior_rank46_keys": interior,
        "boundary_rank46_keys": boundary,
        "all_rank46_keys": raw_tail,
        "exact_mass_identity": "total_mass=3730+45*366969+signed_occupancy",
    }


def validate_universe(universe: Any) -> None:
    required = {
        "object", "full_target_list_used", "projected_list_used",
        "selected_L_sublist_used_for_histogram", "source_realized_counterexample_constructed",
        "full_list_mass_lower_bound", "support_weight_interval", "weight_layer_count",
        "M_j_definition", "nonzero_syndrome", "exact_containment_retained",
        "every_one_point_escape_retained", "support_to_codeword_injective",
        "small_ball_weight_interval", "small_ball_total_mass_cap", "large_layer_weight_interval",
        "large_layer_count", "same_weight_layer_forced_lower", "low_weight_cutoff",
        "low_weight_cap", "low_weight_packing", "high_weight_interval",
        "high_weight_layer_count", "free_baseline", "high_baseline_is_owner",
        "occupancy_identity", "marked_key_contract", "sharp_arithmetic_extremizer",
    }
    exact_keys(universe, required, "source_universe")
    fixed = {
        "object": "FULL_TARGET_QUARTIC_FIELD_LIST_EXACT_WEIGHT_HISTOGRAM",
        "full_target_list_used": True,
        "projected_list_used": False,
        "selected_L_sublist_used_for_histogram": False,
        "source_realized_counterexample_constructed": False,
        "full_list_mass_lower_bound": L,
        "support_weight_interval": [0, R],
        "weight_layer_count": R + 1,
        "M_j_definition": "# distinct target-field codewords c with |E(c)|=j",
        "nonzero_syndrome": True,
        "exact_containment_retained": True,
        "every_one_point_escape_retained": True,
        "support_to_codeword_injective": True,
        "low_weight_cutoff": J0,
        "low_weight_cap": LOW_CAP,
        "high_weight_interval": [J0 + 1, R],
        "high_weight_layer_count": H,
        "free_baseline": FREE,
        "high_baseline_is_owner": False,
    }
    for key, value in fixed.items():
        exact_type_value(universe[key], value, f"source_universe.{key}")
    validate_low_packing(universe)

    identity = universe["occupancy_identity"]
    identity_expected = {
        "N_low_definition": "sum_(0<=j<=J0) M_j",
        "T46_definition": "sum_(J0<j<=R) max(M_j-45,0)",
        "H_r_definition": "#(j in [J0+1,R] with M_j>=r)",
        "C_low_definition": "3730-N_low",
        "C_r_definition": "366969-H_r for 1<=r<=45",
        "Xi46_definition": "T46-C_low-sum_(r=1)^45 C_r",
        "exact_mass_identity": "sum_(j=0)^R M_j=16517335+Xi46",
        "base_mass": BASE_MASS,
        "safe_signed_occupancy_max": SAFE_XI,
        "forbidden_signed_occupancy_min": FORCED_XI,
        "forbidden_forces_T46_at_least": FORCED_XI,
    }
    exact_keys(identity, identity_expected, "occupancy_identity")
    for key, value in identity_expected.items():
        exact_type_value(identity[key], value, f"occupancy_identity.{key}")
    require((H, BASELINE_HIGH, BASE_MASS) == (366_969, 16_513_605, 16_517_335), "45H baseline arithmetic")
    require((SAFE_XI, FORCED_XI, HIGH_MASS_MIN) == (259_880, 259_881, 16_773_486), "signed occupancy boundary")

    marked = universe["marked_key_contract"]
    marked_expected = {
        "canonical_order": "LEXICOGRAPHIC_EXACT_SUPPORT_INCIDENCE_VECTOR",
        "anchor_count": ANCHORS,
        "full_same_weight_layer_loaded_as_context": True,
        "key_count_definition": "T46",
        "keys_have_distinct_distinguished_codewords": True,
        "anchors_charged_as_owners": False,
        "signed_credits_retained": True,
        "forced_key_count_lower_bound": FORCED_XI,
        "lexicographic_keying_is_payment_owner": False,
    }
    exact_keys(marked, marked_expected, "marked_key_contract")
    for key, value in marked_expected.items():
        exact_type_value(marked[key], value, f"marked_key_contract.{key}")

    extremizer = universe["sharp_arithmetic_extremizer"]
    require(extremizer["role"] == "SHARP_ARITHMETIC_RELAXATION_ONLY", "extremizer role")
    require(extremizer["source_realized"] is False, "extremizer not source-realized")
    require(extremizer["zero_multiplicity_weights_omitted"] is True, "extremizer zero runs omitted")
    require(extremizer["blocks_are_maximal_run_length_encoding"] is True, "extremizer maximal RLE flag")
    replay = recompute_extremizer(extremizer["weight_blocks"])
    for key, value in replay.items():
        exact_type_value(extremizer[key], value, f"sharp_arithmetic_extremizer.{key}")
    require(replay["total_mass"] == L, "extremizer forbidden mass")
    require(replay["signed_occupancy"] == FORCED_XI, "extremizer exact signed occupancy")
    require(replay["all_rank46_keys"] == FORCED_XI, "extremizer exact marked-key count")
    require((replay["interior_rank46_keys"], replay["boundary_rank46_keys"]) == (259_880, 1), "extremizer diagnostic key split")


def validate_partition(partition: Any) -> None:
    require(partition["partition_sha256"] == partition_digest(partition), "partition digest")
    require(partition["partition_digest_method"] == "SHA256_CANONICAL_JSON_WITHOUT_PARTITION_SHA256", "partition digest method")
    require(partition["architecture_id"] == ARCHITECTURE_ID, "partition architecture")
    require(partition["preprocess"] == "DIRECT_TARGET_FIELD_LIFT_WITH_SCALAR_DESCENT_CROSSCHECK", "partition preprocessing")
    require(partition["object_kind"] == "LIST", "partition LIST object")
    require(partition["unit"] == UNIT and partition["quantifier"] == QUANTIFIER, "partition unit and quantifier")
    require(partition["atom_order"] == ATOM_ORDER, "partition five-atom order")
    stages = partition["chronology_stages"]
    require(type(stages) is list and [stage["atom_id"] for stage in stages] == ATOM_ORDER, "five chronology stages")
    expected_stages = [
        ("EXACT_ERROR_WEIGHT_AT_MOST_J0", True, True),
        ("CERTIFIED_BOUNDARY_PREFIX_OWNER", False, False),
        ("CERTIFIED_ARBITRARY_WORD_INTERIOR_OWNER", False, False),
        ("CERTIFIED_ADDITIVE_EXTENSION_PROJECTION_OWNER", False, False),
        ("FIXED_HIGH_WEIGHT_BOUNDARY_OR_INTERIOR_RESIDUAL", True, True),
    ]
    for index, (predicate, available, assigns) in enumerate(expected_stages):
        require(stages[index]["declared_predicate"] == predicate, f"chronology stage {index} predicate")
        require(stages[index]["predicate_available"] is available, f"chronology stage {index} availability")
        require(stages[index]["assigns_codewords"] is assigns, f"chronology stage {index} assignment")
    require(partition["owner_order"] == ["LOW_EXACT_WEIGHT_PACKING", BOUNDARY_CELL, INTERIOR_CELL], "first-match owner order")
    for flag in (
        "first_match", "first_match_disjoint", "uniform_over_all_received_words",
        "same_partition_for_all_atoms", "source_codeword_partition_exhaustive",
        "source_codeword_partition_disjoint", "source_codeword_addback_complete",
    ):
        require(partition[flag] is True, f"partition {flag}")
    require(partition["payment_partition_complete"] is False, "payment partition remains open")
    require(partition["global_closure_addback_complete"] is False, "global closure remains open")

    low = partition["low_weight_owner"]
    require(low["owner_id"] == "LOW_EXACT_WEIGHT_PACKING" and low["atom_id"] == "U_paid", "low owner identity")
    require(low["priority"] == 0 and low["predicate"] == "EXACT_ERROR_WEIGHT_AT_MOST_J0", "low owner priority and predicate")
    require(low["weight_interval"] == [0, J0] and low["exact_upper"] == LOW_CAP, "low owner interval and cap")
    require(low["charge_mode"] == "UNIFORM_GLOBAL_UPPER_NOT_OBSERVED_MASS" and low["bankable"] is True, "low owner charge semantics")

    residuals = partition["residual_terminals"]
    require(type(residuals) is list and len(residuals) == 2, "two high-weight codeword cells")
    expected = [
        (BOUNDARY_CELL, BOUNDARY_TERMINAL, 1, "j=R", "automatically_owned_by_U_Q"),
        (INTERIOR_CELL, INTERIOR_TERMINAL, 2, "J0<j<R", "automatically_owned_by_U_list_int"),
    ]
    for row, (cell, terminal, priority, predicate, auto_key) in zip(residuals, expected, strict=True):
        require(row["cell_id"] == cell and row["terminal_id"] == terminal, f"residual {cell} identity")
        require(row["atom_id"] == "U_new" and row["priority"] == priority, f"residual {cell} chronology")
        require(row["weight_predicate"] == predicate and row[auto_key] is False and row["paid"] is False, f"residual {cell} unpaid predicate")
    require(partition["unresolved_cells"] == [BOUNDARY_TERMINAL, INTERIOR_TERMINAL], "unresolved codeword cells")


def validate_coupled(coupled: Any) -> None:
    require(coupled["packet_columns"] == COLUMNS and coupled["anchor_columns"] == ANCHORS, "rank46 packet dimensions")
    require(coupled["small_forney_indices"] == FORNEY_COUNT, "joint kernel rank 44")
    require(coupled["small_index_sum_uniform_max"] == FORNEY_SUM_MAX == 913_681, "Forney index sum")
    require(coupled["cutoff_uniform_min"] == CUTOFF_MIN == 67_447, "uniform locator cutoff")
    p1 = ordered_prefix_bound(FORNEY_SUM_MAX, FORNEY_COUNT, 1)
    p2 = ordered_prefix_bound(FORNEY_SUM_MAX, FORNEY_COUNT, 2)
    p3 = ordered_prefix_bound(FORNEY_SUM_MAX, FORNEY_COUNT, 3)
    p4 = ordered_prefix_bound(FORNEY_SUM_MAX, FORNEY_COUNT, 4)
    require((p1, p2, p3, p4) == (20_765, 41_530, 62_295, 83_060), "balanced partial-sum replay")
    require(coupled["ordered_partial_sum_max"] == {"1": p1, "2": p2, "3": p3}, "certified partial sums")
    require((coupled["one_row_key_bound"], coupled["rank2_key_bound"], coupled["rank3_key_bound"]) == (p1, p2, p3), "rank-key degree bounds")
    require(coupled["rank3_strictly_below_cutoff"] is True and p3 < CUTOFF_MIN < p4, "rank-three cutoff and rank-four route cut")
    require(coupled["rank4_certified_by_aggregate_bound"] is False, "no rank-four aggregate overclaim")

    allowance = coupled["global_safe_key_allowance"]
    expected = {
        "signed_occupancy_budget": SAFE_XI,
        "rank2_distinct_keys": SAFE_XI // p2,
        "rank3_distinct_keys": SAFE_XI // p3,
        "rank2_charged": (SAFE_XI // p2) * p2,
        "rank3_charged": (SAFE_XI // p3) * p3,
        "residual_after_rank2_max": SAFE_XI % p2,
        "residual_after_rank3_max": SAFE_XI % p3,
    }
    for key, value in expected.items():
        exact_type_value(allowance[key], value, f"global_safe_key_allowance.{key}")
    require((expected["rank2_distinct_keys"], expected["rank3_distinct_keys"]) == (6, 4), "global distinct-key allowances")
    require(expected["rank2_charged"] == expected["rank3_charged"] == 249_180, "global charged allowance")
    require(expected["residual_after_rank2_max"] == expected["residual_after_rank3_max"] == 10_700, "global allowance remainder")

    split = coupled["boundary_vs_interior"]
    require(split["boundary_weight"] == R and split["boundary_locator_is_actual_error_locator"] is True, "boundary locator frame")
    require(split["actual_error_locator_coupled_frame_has_agreement_padding"] is False, "no implicit agreement padding")
    require(split["canonical_padded_v4_adapter_bridge"] == "UNPAID_PADDING_BRIDGE", "padding bridge remains unpaid")
    require(split["interior_automatically_owned_by_U_list_int"] is False, "interior is not auto-owned")
    require(split["all_source_keys_classified_by_weight"] is True, "all source keys weight-classified")
    require(split["exact_boundary_interior_split_claimed"] is False, "no exact diagnostic key split overclaim")
    require(split["combined_key_count_lower_bound"] == FORCED_XI, "combined marked-key lower bound")
    require(split["interior_key_count"] is None and split["boundary_key_count"] is None, "unknown diagnostic key split remains null")
    require(coupled["hyperplane_nonforcing_certified_at_most"] == 67, "67-support hyperplane nonforcing ceiling")
    require(coupled["literal_prime_field_68_cutoff_transferred"] is False, "no literal quartic 68-cutoff transfer")
    require(coupled["high_baseline_is_owner"] is False, "45H baseline is not an owner")
    require(coupled["independent_per_layer_root_unions_close_row"] is False, "per-layer root unions do not close row")
    require(coupled["global_terminal"] == GLOBAL_TERMINAL, "global unpaid terminal")


def validate_atoms(atoms: Any, partition_sha: str) -> None:
    require(type(atoms) is list and len(atoms) == 5, "exactly five atoms")
    require([atom["atom_id"] for atom in atoms] == ATOM_ORDER, "v4 atom order")
    for atom in atoms:
        require(atom["architecture_id"] == ARCHITECTURE_ID, f"{atom['atom_id']} architecture")
        require(atom["partition_sha256"] == partition_sha, f"{atom['atom_id']} partition digest")
        require(atom["unit"] == UNIT and atom["quantifier"] == QUANTIFIER, f"{atom['atom_id']} unit and quantifier")
    paid = atoms[0]
    require(paid["value"] == LOW_CAP and type(paid["value"]) is int, "U_paid exact value")
    require(paid["status"] == "BANKABLE_SOURCE_BOUND_EXACT_UPPER" and paid["bankable"] is True, "U_paid bankability")
    require(paid["bankability_gate"] == "PARTITION_DIGEST_UNIT_QUANTIFIER_AND_SOURCE_HASHES_VERIFIED", "U_paid bankability gate")
    require(paid["owner_ids"] == ["LOW_EXACT_WEIGHT_PACKING"], "U_paid sole owner")
    for atom in atoms[1:]:
        require(atom["value"] is None, f"{atom['atom_id']} remains null")
        require(atom["status"] == "OPEN_UNPAID" and atom["bankable"] is False, f"{atom['atom_id']} remains open")
        require(atom["owner_ids"] == [], f"{atom['atom_id']} has no forced owner")
    require(atoms[3]["transport_role"] == "SCALAR_DESCENT_IS_PREPROCESSING_NOT_EXTENSION_PAYMENT", "U_ext scalar-descent guard")


def validate_closure(closure: Any) -> None:
    require(closure["closed"] is False and closure["row_closed"] is False, "row remains open")
    require(closure["banked_atoms"] == ["U_paid"] and closure["banked_atom_count"] == 1, "U_paid banked in adapter chronology")
    require(closure["known_sum"] == LOW_CAP, "known source-bound sum")
    require(closure["high_residual_payment_movement"] == 0, "no high-residual payment movement")
    require(closure["official_row_score_movement"] == 0, "no official row-score movement")
    require(closure["closed_total"] is None and closure["B_star"] == B_STAR, "open closure total")
    require(closure["unresolved_atom_ids"] == ATOM_ORDER[1:], "four unresolved atoms")
    residual = closure["unpaid_global_residual"]
    require(residual["terminal"] == GLOBAL_TERMINAL and residual["residual_atom"] == "U_new", "global residual identity")
    require(residual["high_weight_codeword_mass_lower_bound"] == HIGH_MASS_MIN, "high-weight codeword lower bound")
    require(residual["baseline_high_codeword_mass"] == BASELINE_HIGH, "45H baseline in closure")
    require(residual["marked_key_count_lower_bound"] == FORCED_XI, "closure marked-key lower bound")
    require(residual["exact_boundary_interior_key_split_claimed"] is False, "closure key split not claimed")
    require(residual["interior_rank46_key_count"] is None and residual["boundary_rank46_key_count"] is None, "closure split counts null")
    require(residual["exact_owner_charge"] is None and residual["forced_into_existing_owner"] is False, "global residual unpaid")
    require(residual["source_realized_counterexample_constructed"] is False, "no realized counterexample overclaim")
    require(closure["official_theorem_claimed"] is False, "no official theorem overclaim")


def safe_source_path(relative: str) -> Path:
    require(type(relative) is str and relative.isascii(), "source path ASCII")
    require("\\" not in relative and "\x00" not in relative, "source path separators")
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and str(pure) == relative, "source path canonical relative")
    require(all(part not in {"", ".", ".."} and not part.startswith(".") for part in pure.parts), "source path components")
    path = ROOT.joinpath(*pure.parts)
    require(path.is_file() and not path.is_symlink(), f"source file exists and is not symlink: {relative}")
    current = ROOT
    for part in pure.parts[:-1]:
        current = current / part
        require(not current.is_symlink(), f"source parent not symlink: {relative}")
    require(path.resolve().is_relative_to(ROOT.resolve()), f"source remains in repository: {relative}")
    return path


def strict_json_value(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"non-ASCII pinned JSON: {path}") from exc
    value = json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_int=strict_int,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"pinned JSON root object: {path}")
    return value


def validate_sources(bindings: Any) -> None:
    require(type(bindings) is list and len(bindings) == len(SOURCE_PATHS), "complete 18-source registry")
    require([row["role"] for row in bindings] == [role for role, _ in SOURCE_PATHS], "source role order")
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    seen_inodes: set[tuple[int, int]] = set()
    for row, (role, expected_path) in zip(bindings, SOURCE_PATHS, strict=True):
        exact_keys(row, {"binding_id", "role", "path", "sha256", "internal_payload_sha256", "scope"}, f"source {role}")
        require(row["binding_id"] == f"M31_LIST_V4_SOURCE::{role}", f"source {role} binding ID")
        require(row["role"] == role and row["path"] == expected_path, f"source {role} fixed path")
        require(type(row["scope"]) is str and row["scope"].isascii() and len(row["scope"]) >= 1, f"source {role} scope")
        require(row["binding_id"] not in seen_ids and row["path"] not in seen_paths, f"source {role} uniqueness")
        seen_ids.add(row["binding_id"])
        seen_paths.add(row["path"])
        path = safe_source_path(row["path"])
        stat = path.stat()
        inode = (stat.st_dev, stat.st_ino)
        require(inode not in seen_inodes, f"source {role} hardlink uniqueness")
        seen_inodes.add(inode)
        claimed = row["sha256"]
        require(type(claimed) is str and re.fullmatch(r"[0-9a-f]{64}", claimed) is not None, f"source {role} hash shape")
        require(sha256_bytes(path.read_bytes()) == claimed, f"source {role} live hash")
        if role == "rank46_manifest":
            internal = row["internal_payload_sha256"]
            require(type(internal) is str and re.fullmatch(r"[0-9a-f]{64}", internal) is not None, "rank46 internal hash shape")
            predecessor = strict_json_value(path)
            require(predecessor.get("certificate_sha256") == internal, "rank46 internal hash claim")
            unsigned = copy.deepcopy(predecessor)
            unsigned.pop("certificate_sha256", None)
            require(sha256_bytes(canonical_json(unsigned)) == internal, "rank46 internal hash replay")
        else:
            require(row["internal_payload_sha256"] is None, f"source {role} has no imported internal payload")


def validate_payload(payload: dict[str, Any], *, check_sources: bool = True) -> None:
    check_ascii(payload)
    top_keys = {
        "schema", "architecture_id", "status", "payload_sha256", "row_contract",
        "source_transport", "source_universe", "partition", "coupled_rank46",
        "atoms", "closure_state", "source_bindings",
    }
    exact_keys(payload, top_keys, "manifest")
    require(payload["schema"] == SCHEMA_ID, "manifest schema ID")
    require(payload["architecture_id"] == ARCHITECTURE_ID, "manifest architecture")
    require(payload["status"] == OPEN_STATUS, "manifest open status")
    require(payload["payload_sha256"] == payload_digest(payload), "payload canonical digest")
    validate_row(payload["row_contract"])
    validate_transport(payload["source_transport"])
    validate_universe(payload["source_universe"])
    validate_partition(payload["partition"])
    validate_coupled(payload["coupled_rank46"])
    validate_atoms(payload["atoms"], payload["partition"]["partition_sha256"])
    validate_closure(payload["closure_state"])
    if check_sources:
        validate_sources(payload["source_bindings"])


def set_path(payload: dict[str, Any], path: Sequence[Any], value: Any) -> None:
    target: Any = payload
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value


def reseal(payload: dict[str, Any], *, partition_changed: bool = False) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    if partition_changed:
        unsigned_partition = copy.deepcopy(out["partition"])
        unsigned_partition.pop("partition_sha256", None)
        digest = sha256_bytes(canonical_json(unsigned_partition))
        out["partition"]["partition_sha256"] = digest
        for atom in out["atoms"]:
            atom["partition_sha256"] = digest
    unsigned = copy.deepcopy(out)
    unsigned.pop("payload_sha256", None)
    out["payload_sha256"] = sha256_bytes(canonical_json(unsigned))
    return out


def path_mutation(path: Sequence[Any], value: Any, *, partition_changed: bool = False) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def mutate(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        set_path(out, path, value)
        return reseal(out, partition_changed=partition_changed)
    return mutate


def tamper_selftest(payload: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("wrong-unit", path_mutation(("row_contract", "unit"), "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE")),
        ("prime-only-direct-lift", path_mutation(("source_transport", "direct_target_field_lift", "field"), "F_p")),
        ("scalar-as-sole-transport", path_mutation(("source_transport", "scalar_descent_is_sole_transport"), True)),
        ("scalar-pays-extension", path_mutation(("source_transport", "U_ext_zero_claimed"), True)),
        ("scalar-margin", path_mutation(("source_transport", "scalar_descent_crosscheck", "strict_margin"), str(1))),
        ("projected-histogram", path_mutation(("source_universe", "M_j_definition"), "# distinct projected codewords with exact error weight j")),
        ("low-cap", path_mutation(("source_universe", "low_weight_cap"), LOW_CAP + 1)),
        ("packing-rounding", path_mutation(("source_universe", "low_weight_packing", "first_excluded_contradiction_margin"), 0)),
        ("baseline-owner", path_mutation(("source_universe", "high_baseline_is_owner"), True)),
        ("marked-key-lower", path_mutation(("source_universe", "marked_key_contract", "forced_key_count_lower_bound"), SAFE_XI)),
        ("partition-order", path_mutation(("partition", "atom_order"), ["U_paid", "U_Q", "U_ext", "U_list_int", "U_new"], partition_changed=True)),
        ("partition-incomplete", path_mutation(("partition", "source_codeword_partition_exhaustive"), False, partition_changed=True)),
        ("boundary-auto-owner", path_mutation(("partition", "residual_terminals", 0, "automatically_owned_by_U_Q"), True, partition_changed=True)),
        ("rank44-to-45", path_mutation(("coupled_rank46", "small_forney_indices"), 45)),
        ("rank3-degree", path_mutation(("coupled_rank46", "rank3_key_bound"), 62_296)),
        ("quartic-68-overclaim", path_mutation(("coupled_rank46", "literal_prime_field_68_cutoff_transferred"), True)),
        ("U-paid-unbankable", path_mutation(("atoms", 0, "bankable"), False)),
        ("U-Q-zero", path_mutation(("atoms", 1, "value"), 0)),
        ("U-ext-zero", path_mutation(("atoms", 3, "value"), 0)),
        ("row-closed", path_mutation(("closure_state", "row_closed"), True)),
        ("baseline-erased", path_mutation(("closure_state", "unpaid_global_residual", "baseline_high_codeword_mass"), 0)),
        ("source-hash", path_mutation(("source_bindings", 2, "sha256"), "0" * 64)),
    ]
    rejected = 0
    for label, mutate in mutations:
        candidate = mutate(payload)
        try:
            validate_payload(candidate, check_sources=True)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"independent mutation accepted: {label}")
    require(rejected == len(mutations), "all independent mutations rejected")
    return rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true", help="verify the canonical manifest")
    parser.add_argument("--tamper-selftest", action="store_true", help="run independent semantic mutations")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.check or args.tamper_selftest):
        args.check = True
    payload, _ = strict_load(args.manifest)
    validate_payload(payload, check_sources=True)
    rejected = 0
    if args.tamper_selftest:
        rejected = tamper_selftest(payload)
    print("M31 LIST v4 source adapter independent replay: PASS")
    print("five atoms: U_paid=3730 bankable; U_Q/U_list_int/U_ext/U_new=null")
    print("global residual: Xi46>=259881; 45H baseline retained; rank3 bound=62295")
    print("literal quartic 68-cutoff transfer: rejected")
    if args.tamper_selftest:
        print(f"independent mutations: {rejected}/{rejected} rejected PASS")
    print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
