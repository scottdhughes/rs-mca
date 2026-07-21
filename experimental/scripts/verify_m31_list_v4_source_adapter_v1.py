#!/usr/bin/env python3
"""Verify the open M31 LIST Grande Finale v4 source-adapter route cut.

This standard-library verifier checks a source-bound, fail-closed interface.
It certifies one bankable low-weight payment and an exhaustive fixed-predicate
partition of the remaining *codewords* into boundary and interior U_new
residuals.  Rank-46 marked keys are nested diagnostic witnesses, not owners or
additional ledger charges.  The script deliberately does not close the row.

Every check raises an explicit exception, so ``python -O`` has identical
semantics.  ``--print-template`` emits the canonical manifest to stdout; this
script never writes the manifest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Sequence


SCHEMA_ID = "rs-mca-m31-list-v4-source-adapter-v1"
ARCHITECTURE_ID = "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
STATUS = "OPEN_ROUTE_CUT_UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL"
UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"
QUANTIFIER = "UNIFORM_OVER_ALL_RECEIVED_WORDS"
ATOM_ORDER = ("U_paid", "U_Q", "U_list_int", "U_ext", "U_new")

P = 2**31 - 1
EXTENSION_DEGREE = 4
Q = P**EXTENSION_DEGREE
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
SHIFT = AGREEMENT - K
RADIUS = N - AGREEMENT
TARGET_EXPONENT = 100
BUDGET = Q // 2**TARGET_EXPONENT
FORBIDDEN = BUDGET + 1

T = RADIUS
G = AGREEMENT - K + 1
PROJECTIVE_FUNCTIONALS = (P**EXTENSION_DEGREE - 1) // (P - 1)
KILLING_FUNCTIONALS = (P ** (EXTENSION_DEGREE - 1) - 1) // (P - 1)
SCALAR_LEFT = FORBIDDEN * T * KILLING_FUNCTIONALS
SCALAR_RIGHT = G * PROJECTIVE_FUNCTIONALS
SCALAR_MARGIN = SCALAR_RIGHT - SCALAR_LEFT

SMALL_BALL_CUTOFF = K // 2
LARGE_LAYER_COUNT = RADIUS - SMALL_BALL_CUTOFF
J0 = 614_160
PACKING_SET_SIZE = N - J0
PAIR_INTERSECTION = K - 1
LOW_CAP = 3_730
FIRST_EXCLUDED = LOW_CAP + 1
HIGH_LAYER_COUNT = RADIUS - J0
FREE_BASELINE = 45
BASELINE_HIGH_MASS = FREE_BASELINE * HIGH_LAYER_COUNT
BASE_MASS = LOW_CAP + BASELINE_HIGH_MASS
SAFE_SIGNED_OCCUPANCY = BUDGET - BASE_MASS
FORCED_SIGNED_OCCUPANCY = FORBIDDEN - BASE_MASS
HIGH_MASS_LOWER = FORBIDDEN - LOW_CAP

PACKET_COLUMNS = 46
ANCHOR_COLUMNS = 45
SMALL_FORNEY_INDICES = 44
SMALL_INDEX_SUM_MAX = 913_681
CUTOFF_UNIFORM_MIN = K - RADIUS
ONE_ROW_BOUND = 20_765
RANK2_BOUND = 41_530
RANK3_BOUND = 62_295

GLOBAL_TERMINAL = "UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL"
BOUNDARY_CODEWORD_CELL = "HIGH_BOUNDARY_EXACT_CODEWORD"
INTERIOR_CODEWORD_CELL = "HIGH_INTERIOR_EXACT_CODEWORD"
BOUNDARY_CODEWORD_TERMINAL = "UNPAID_BOUNDARY_CODEWORD_RESIDUAL"
INTERIOR_CODEWORD_TERMINAL = "UNPAID_INTERIOR_CODEWORD_RESIDUAL"
BOUNDARY_KEY_TERMINAL = "UNPAID_BOUNDARY_COUPLED_RANK46_KEY"
INTERIOR_KEY_TERMINAL = "UNPAID_INTERIOR_COUPLED_RANK46_KEY"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_list_v4_source_adapter_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_list_v4_source_adapter_v1.py"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md"
INDEPENDENT_PATH = ROOT / "experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py"
SAGE_ADAPTER_PATH = ROOT / "experimental/scripts/verify_m31_list_v4_source_adapter_v1.sage"
DEFAULT_MANIFEST_PATH = (
    ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json"
)


class VerificationError(RuntimeError):
    """Raised whenever a fail-closed contract condition is violated."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    """Always-active assertion with a stable diagnostic label."""
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def reject_float(_value: str) -> Any:
    raise VerificationError("JSON floating-point values are forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("JSON NaN and infinity are forbidden")


def strict_integer(value: str) -> int:
    require(len(value.lstrip("-")) <= 96, "JSON integer digit bound")
    return int(value)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_json_loads(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_int=strict_integer,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )


def strict_json_path(path: Path, *, canonical_file: bool = False) -> tuple[Any, bytes]:
    raw = path.read_bytes()
    require(len(raw) <= 64 * 1024 * 1024, f"JSON file size bound: {path}")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"non-ASCII JSON: {path}") from exc
    value = strict_json_loads(text)
    if canonical_file:
        require(raw == canonical_json(value), f"canonical JSON bytes: {path}")
    return value, raw


def canonical_json(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("payload is not canonical-JSON serializable") from exc
    return (rendered + "\n").encode("ascii")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal_payload(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


def partition_sha256(partition: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(partition)
    unsigned.pop("partition_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal_partition(partition: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(partition)
    out.pop("partition_sha256", None)
    out["partition_sha256"] = partition_sha256(out)
    return out


def deep_exact(actual: Any, expected: Any, path: str) -> None:
    """Type-sensitive recursive equality (notably, bool is not an integer)."""
    require(type(actual) is type(expected), f"{path}: exact JSON type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact list length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def require_ascii_strings(value: Any, path: str = "payload") -> None:
    if isinstance(value, str):
        require(value.isascii(), f"{path}: ASCII string")
    elif isinstance(value, dict):
        for key, child in value.items():
            require(isinstance(key, str) and key.isascii(), f"{path}: ASCII object key")
            require_ascii_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            require_ascii_strings(child, f"{path}[{index}]")


def balanced_pair_lower(member_count: int, set_size: int) -> tuple[int, int, int]:
    quotient, remainder = divmod(member_count * set_size, N)
    lower = N * quotient * (quotient - 1) // 2 + remainder * quotient
    return lower, quotient, remainder


def low_weight_packing() -> dict[str, Any]:
    feasible_lower, _, _ = balanced_pair_lower(LOW_CAP, PACKING_SET_SIZE)
    feasible_upper = math.comb(LOW_CAP, 2) * PAIR_INTERSECTION
    excluded_lower, _, _ = balanced_pair_lower(FIRST_EXCLUDED, PACKING_SET_SIZE)
    excluded_upper = math.comb(FIRST_EXCLUDED, 2) * PAIR_INTERSECTION
    require(feasible_upper - feasible_lower == 202_311, "low-cap feasible margin")
    require(excluded_lower - excluded_upper == 19_019, "first-excluded contradiction margin")
    return {
        "selected_agreement_subset_size": PACKING_SET_SIZE,
        "pair_intersection_upper": PAIR_INTERSECTION,
        "feasible_count": LOW_CAP,
        "feasible_margin": feasible_upper - feasible_lower,
        "first_excluded_count": FIRST_EXCLUDED,
        "first_excluded_contradiction_margin": excluded_lower - excluded_upper,
        "integer_rounding_is_load_bearing": True,
        "codeword_to_selected_subset_injective": True,
    }


def ordered_prefix_max(total: int, count: int, prefix: int) -> int:
    quotient, remainder = divmod(total, count)
    return prefix * quotient + max(0, remainder - (count - prefix))


def expected_extremizer_blocks() -> list[dict[str, Any]]:
    return [
        {
            "weight_start": J0,
            "weight_end": J0,
            "multiplicity_per_weight": LOW_CAP,
            "layer_class": "LOW_PREFIX",
            "rank46_keys_per_weight": 0,
        },
        {
            "weight_start": J0 + 1,
            "weight_end": 721_248,
            "multiplicity_per_weight": FREE_BASELINE,
            "layer_class": "HIGH_INTERIOR",
            "rank46_keys_per_weight": 0,
        },
        {
            "weight_start": 721_249,
            "weight_end": RADIUS - 1,
            "multiplicity_per_weight": PACKET_COLUMNS,
            "layer_class": "HIGH_INTERIOR",
            "rank46_keys_per_weight": 1,
        },
        {
            "weight_start": RADIUS,
            "weight_end": RADIUS,
            "multiplicity_per_weight": PACKET_COLUMNS,
            "layer_class": "BOUNDARY",
            "rank46_keys_per_weight": 1,
        },
    ]


def compute_extremizer(blocks: Sequence[dict[str, Any]]) -> dict[str, Any]:
    require(len(blocks) >= 1, "extremizer has an occupied block")
    previous_end = -1
    previous: dict[str, Any] | None = None
    occupied_weights = 0
    total_mass = 0
    low_mass = 0
    high_mass = 0
    raw_tail = 0
    interior_keys = 0
    boundary_keys = 0
    level_counts = [0] * PACKET_COLUMNS

    exact_keys = {
        "weight_start",
        "weight_end",
        "multiplicity_per_weight",
        "layer_class",
        "rank46_keys_per_weight",
    }
    for index, block in enumerate(blocks):
        require(type(block) is dict and set(block) == exact_keys, f"extremizer block {index} keys")
        start = block["weight_start"]
        end = block["weight_end"]
        multiplicity = block["multiplicity_per_weight"]
        keys = block["rank46_keys_per_weight"]
        layer_class = block["layer_class"]
        for name, value in (("start", start), ("end", end), ("multiplicity", multiplicity), ("keys", keys)):
            require(type(value) is int, f"extremizer block {index} {name} integer")
        require(0 <= start <= end <= RADIUS, f"extremizer block {index} range")
        require(start > previous_end, f"extremizer block {index} sorted and disjoint")
        require(multiplicity >= 1, f"extremizer block {index} positive multiplicity")
        if end <= J0:
            require(layer_class == "LOW_PREFIX", f"extremizer block {index} low class")
            expected_keys = 0
        elif end < RADIUS and start > J0:
            require(layer_class == "HIGH_INTERIOR", f"extremizer block {index} interior class")
            expected_keys = max(0, multiplicity - FREE_BASELINE)
        else:
            require(start == end == RADIUS, f"extremizer block {index} boundary singleton")
            require(layer_class == "BOUNDARY", f"extremizer block {index} boundary class")
            expected_keys = max(0, multiplicity - FREE_BASELINE)
        require(keys == expected_keys, f"extremizer block {index} exact rank-46 key count")
        if previous is not None and start == previous_end + 1:
            require(
                not (
                    previous["multiplicity_per_weight"] == multiplicity
                    and previous["layer_class"] == layer_class
                    and previous["rank46_keys_per_weight"] == keys
                ),
                f"extremizer block {index} maximal run-length encoding",
            )

        length = end - start + 1
        occupied_weights += length
        total_mass += length * multiplicity
        if layer_class == "LOW_PREFIX":
            low_mass += length * multiplicity
        else:
            high_mass += length * multiplicity
            raw_tail += length * keys
            for level in range(1, PACKET_COLUMNS + 1):
                if multiplicity >= level:
                    level_counts[level - 1] += length
            if layer_class == "BOUNDARY":
                boundary_keys += length * keys
            else:
                interior_keys += length * keys
        previous_end = end
        previous = block

    low_credit = LOW_CAP - low_mass
    require(low_credit >= 0, "extremizer low credit nonnegative")
    level_credit_sum = sum(HIGH_LAYER_COUNT - level_counts[level - 1] for level in range(1, FREE_BASELINE + 1))
    require(level_credit_sum >= 0, "extremizer level credits nonnegative")
    signed = raw_tail - low_credit - level_credit_sum
    require(total_mass == BASE_MASS + signed, "extremizer exact signed mass identity")

    return {
        "occupancy_level_counts": [
            {"level": level, "occupied_high_layers": level_counts[level - 1]}
            for level in range(1, PACKET_COLUMNS + 1)
        ],
        "occupied_weight_count": occupied_weights,
        "total_mass": total_mass,
        "low_mass": low_mass,
        "high_mass": high_mass,
        "base_mass": BASE_MASS,
        "raw_rank46_tail": raw_tail,
        "low_credit": low_credit,
        "level_credit_sum": level_credit_sum,
        "signed_occupancy": signed,
        "safe_signed_occupancy_max": SAFE_SIGNED_OCCUPANCY,
        "forbidden_signed_occupancy_min": FORCED_SIGNED_OCCUPANCY,
        "interior_rank46_keys": interior_keys,
        "boundary_rank46_keys": boundary_keys,
        "all_rank46_keys": raw_tail,
        "exact_mass_identity": "total_mass=3730+45*366969+signed_occupancy",
    }


def arithmetic_extremizer() -> dict[str, Any]:
    blocks = expected_extremizer_blocks()
    computed = compute_extremizer(blocks)
    require(computed["total_mass"] == FORBIDDEN, "extremizer forbidden mass")
    require(computed["signed_occupancy"] == FORCED_SIGNED_OCCUPANCY, "extremizer signed occupancy")
    require(computed["all_rank46_keys"] == FORCED_SIGNED_OCCUPANCY, "extremizer marked keys")
    require(computed["interior_rank46_keys"] == 259_880, "extremizer interior keys")
    require(computed["boundary_rank46_keys"] == 1, "extremizer boundary keys")
    return {
        "role": "SHARP_ARITHMETIC_RELAXATION_ONLY",
        "source_realized": False,
        "zero_multiplicity_weights_omitted": True,
        "blocks_are_maximal_run_length_encoding": True,
        "weight_blocks": blocks,
        **computed,
    }


def row_contract() -> dict[str, Any]:
    return {
        "row_id": "m31_list",
        "object_kind": "LIST",
        "base_prime": P,
        "extension_degree": EXTENSION_DEGREE,
        "code_field_cardinality": str(Q),
        "q_gen": P,
        "q_line": str(Q),
        "q_chal": str(Q),
        "q_list": str(Q),
        "n": N,
        "K": K,
        "agreement": AGREEMENT,
        "shift": SHIFT,
        "radius": RADIUS,
        "target_exponent": TARGET_EXPONENT,
        "B_star": BUDGET,
        "forbidden_size": FORBIDDEN,
        "endpoint": "CLOSED_RADIUS",
        "domain_in_base_field": True,
        "unit": UNIT,
        "quantifier": QUANTIFIER,
    }


def source_transport() -> dict[str, Any]:
    return {
        "kind": "DIRECT_TARGET_FIELD_LIFT",
        "direct_target_field_lift": {
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
            "source_binding_roles": [
                "adapter_note",
                "admissibility_authority",
                "full_layer_source",
                "coupled_source",
            ],
        },
        "scalar_descent_crosscheck": {
            "transport_id": "M31_SCALAR_DESCENT_THRESHOLD_L",
            "kind": "THRESHOLD_L_INJECTION_NOT_FULL_LIST_BIJECTION",
            "role": "INDEPENDENT_THRESHOLD_CROSSCHECK_ONLY",
            "from_field": "F_(p^4)",
            "to_field": "F_p",
            "extension_degree": EXTENSION_DEGREE,
            "threshold_L": FORBIDDEN,
            "t": T,
            "g": G,
            "projective_functionals": str(PROJECTIVE_FUNCTIONALS),
            "functionals_killing_fixed_nonzero": str(KILLING_FUNCTIONALS),
            "left_LtH": str(SCALAR_LEFT),
            "right_gN": str(SCALAR_RIGHT),
            "strict_margin": str(SCALAR_MARGIN),
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
        },
        "scalar_descent_is_sole_transport": False,
        "U_ext_zero_claimed": False,
    }


def occupancy_identity() -> dict[str, Any]:
    return {
        "N_low_definition": "sum_(0<=j<=J0) M_j",
        "T46_definition": "sum_(J0<j<=R) max(M_j-45,0)",
        "H_r_definition": "#(j in [J0+1,R] with M_j>=r)",
        "C_low_definition": "3730-N_low",
        "C_r_definition": "366969-H_r for 1<=r<=45",
        "Xi46_definition": "T46-C_low-sum_(r=1)^45 C_r",
        "exact_mass_identity": "sum_(j=0)^R M_j=16517335+Xi46",
        "base_mass": BASE_MASS,
        "safe_signed_occupancy_max": SAFE_SIGNED_OCCUPANCY,
        "forbidden_signed_occupancy_min": FORCED_SIGNED_OCCUPANCY,
        "forbidden_forces_T46_at_least": FORCED_SIGNED_OCCUPANCY,
    }


def marked_key_contract() -> dict[str, Any]:
    return {
        "canonical_order": "LEXICOGRAPHIC_EXACT_SUPPORT_INCIDENCE_VECTOR",
        "anchor_count": ANCHOR_COLUMNS,
        "full_same_weight_layer_loaded_as_context": True,
        "key_count_definition": "T46",
        "keys_have_distinct_distinguished_codewords": True,
        "anchors_charged_as_owners": False,
        "signed_credits_retained": True,
        "forced_key_count_lower_bound": FORCED_SIGNED_OCCUPANCY,
        "lexicographic_keying_is_payment_owner": False,
    }


def source_universe() -> dict[str, Any]:
    forced_layer = (FORBIDDEN - 1 + LARGE_LAYER_COUNT - 1) // LARGE_LAYER_COUNT
    require(forced_layer == 37, "whole-ball same-weight layer lower bound")
    return {
        "object": "FULL_TARGET_QUARTIC_FIELD_LIST_EXACT_WEIGHT_HISTOGRAM",
        "full_target_list_used": True,
        "projected_list_used": False,
        "selected_L_sublist_used_for_histogram": False,
        "source_realized_counterexample_constructed": False,
        "full_list_mass_lower_bound": FORBIDDEN,
        "support_weight_interval": [0, RADIUS],
        "weight_layer_count": RADIUS + 1,
        "M_j_definition": "# distinct target-field codewords c with |E(c)|=j",
        "nonzero_syndrome": True,
        "exact_containment_retained": True,
        "every_one_point_escape_retained": True,
        "support_to_codeword_injective": True,
        "small_ball_weight_interval": [0, SMALL_BALL_CUTOFF],
        "small_ball_total_mass_cap": 1,
        "large_layer_weight_interval": [SMALL_BALL_CUTOFF + 1, RADIUS],
        "large_layer_count": LARGE_LAYER_COUNT,
        "same_weight_layer_forced_lower": forced_layer,
        "low_weight_cutoff": J0,
        "low_weight_cap": LOW_CAP,
        "low_weight_packing": low_weight_packing(),
        "high_weight_interval": [J0 + 1, RADIUS],
        "high_weight_layer_count": HIGH_LAYER_COUNT,
        "free_baseline": FREE_BASELINE,
        "high_baseline_is_owner": False,
        "occupancy_identity": occupancy_identity(),
        "marked_key_contract": marked_key_contract(),
        "sharp_arithmetic_extremizer": arithmetic_extremizer(),
    }


def partition_contract() -> dict[str, Any]:
    raw = {
        "partition_digest_method": "SHA256_CANONICAL_JSON_WITHOUT_PARTITION_SHA256",
        "architecture_id": ARCHITECTURE_ID,
        "preprocess": "DIRECT_TARGET_FIELD_LIFT_WITH_SCALAR_DESCENT_CROSSCHECK",
        "object_kind": "LIST",
        "unit": UNIT,
        "quantifier": QUANTIFIER,
        "atom_order": list(ATOM_ORDER),
        "chronology_stages": [
            {
                "atom_id": "U_paid",
                "declared_predicate": "EXACT_ERROR_WEIGHT_AT_MOST_J0",
                "predicate_available": True,
                "assigns_codewords": True,
            },
            {
                "atom_id": "U_Q",
                "declared_predicate": "CERTIFIED_BOUNDARY_PREFIX_OWNER",
                "predicate_available": False,
                "assigns_codewords": False,
            },
            {
                "atom_id": "U_list_int",
                "declared_predicate": "CERTIFIED_ARBITRARY_WORD_INTERIOR_OWNER",
                "predicate_available": False,
                "assigns_codewords": False,
            },
            {
                "atom_id": "U_ext",
                "declared_predicate": "CERTIFIED_ADDITIVE_EXTENSION_PROJECTION_OWNER",
                "predicate_available": False,
                "assigns_codewords": False,
            },
            {
                "atom_id": "U_new",
                "declared_predicate": "FIXED_HIGH_WEIGHT_BOUNDARY_OR_INTERIOR_RESIDUAL",
                "predicate_available": True,
                "assigns_codewords": True,
            },
        ],
        "owner_order": [
            "LOW_EXACT_WEIGHT_PACKING",
            BOUNDARY_CODEWORD_CELL,
            INTERIOR_CODEWORD_CELL,
        ],
        "first_match": True,
        "first_match_disjoint": True,
        "uniform_over_all_received_words": True,
        "same_partition_for_all_atoms": True,
        "source_codeword_partition_exhaustive": True,
        "source_codeword_partition_disjoint": True,
        "source_codeword_addback_complete": True,
        "payment_partition_complete": False,
        "global_closure_addback_complete": False,
        "low_weight_owner": {
            "owner_id": "LOW_EXACT_WEIGHT_PACKING",
            "atom_id": "U_paid",
            "priority": 0,
            "predicate": "EXACT_ERROR_WEIGHT_AT_MOST_J0",
            "weight_interval": [0, J0],
            "exact_upper": LOW_CAP,
            "charge_mode": "UNIFORM_GLOBAL_UPPER_NOT_OBSERVED_MASS",
            "bankable": True,
            "source_binding_roles": [
                "adapter_note",
                "rank46_source",
                "rank46_verifier",
                "rank46_manifest",
            ],
        },
        "residual_terminals": [
            {
                "cell_id": BOUNDARY_CODEWORD_CELL,
                "terminal_id": BOUNDARY_CODEWORD_TERMINAL,
                "atom_id": "U_new",
                "priority": 1,
                "weight_predicate": "j=R",
                "automatically_owned_by_U_Q": False,
                "paid": False,
            },
            {
                "cell_id": INTERIOR_CODEWORD_CELL,
                "terminal_id": INTERIOR_CODEWORD_TERMINAL,
                "atom_id": "U_new",
                "priority": 2,
                "weight_predicate": "J0<j<R",
                "automatically_owned_by_U_list_int": False,
                "paid": False,
            },
        ],
        "diagnostic_key_subterminals": [BOUNDARY_KEY_TERMINAL, INTERIOR_KEY_TERMINAL],
        "unresolved_cells": [BOUNDARY_CODEWORD_TERMINAL, INTERIOR_CODEWORD_TERMINAL],
    }
    return seal_partition(raw)


def coupled_rank46() -> dict[str, Any]:
    p1 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_FORNEY_INDICES, 1)
    p2 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_FORNEY_INDICES, 2)
    p3 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_FORNEY_INDICES, 3)
    p4 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_FORNEY_INDICES, 4)
    require((p1, p2, p3, p4) == (20_765, 41_530, 62_295, 83_060), "coupled ordered partial bounds")
    require(p3 < CUTOFF_UNIFORM_MIN < p4, "rank-three strict cutoff and rank-four route cut")
    rank2_keys = SAFE_SIGNED_OCCUPANCY // p2
    rank3_keys = SAFE_SIGNED_OCCUPANCY // p3
    require((rank2_keys, rank3_keys) == (6, 4), "global root-key allowances")
    rank2_charged = rank2_keys * p2
    rank3_charged = rank3_keys * p3
    require(rank2_charged == rank3_charged == 249_180, "global root-key charged mass")
    require(SAFE_SIGNED_OCCUPANCY - rank2_charged == 10_700, "rank-two allowance remainder")
    require(SAFE_SIGNED_OCCUPANCY - rank3_charged == 10_700, "rank-three allowance remainder")
    return {
        "packet_columns": PACKET_COLUMNS,
        "anchor_columns": ANCHOR_COLUMNS,
        "small_forney_indices": SMALL_FORNEY_INDICES,
        "small_index_sum_uniform_max": SMALL_INDEX_SUM_MAX,
        "cutoff_uniform_min": CUTOFF_UNIFORM_MIN,
        "ordered_partial_sum_max": {"1": p1, "2": p2, "3": p3},
        "one_row_key_bound": p1,
        "rank2_key_bound": p2,
        "rank3_key_bound": p3,
        "rank3_strictly_below_cutoff": True,
        "rank4_certified_by_aggregate_bound": False,
        "global_safe_key_allowance": {
            "signed_occupancy_budget": SAFE_SIGNED_OCCUPANCY,
            "rank2_distinct_keys": rank2_keys,
            "rank3_distinct_keys": rank3_keys,
            "rank2_charged": rank2_charged,
            "rank3_charged": rank3_charged,
            "residual_after_rank2_max": SAFE_SIGNED_OCCUPANCY - rank2_charged,
            "residual_after_rank3_max": SAFE_SIGNED_OCCUPANCY - rank3_charged,
        },
        "boundary_vs_interior": {
            "boundary_weight": RADIUS,
            "boundary_locator_is_actual_error_locator": True,
            "actual_error_locator_coupled_frame_has_agreement_padding": False,
            "canonical_padded_v4_adapter_bridge": "UNPAID_PADDING_BRIDGE",
            "interior_automatically_owned_by_U_list_int": False,
            "boundary_terminals": ["UNPAID_COMMON_CORE_ADD_BACK", "UNPAID_RANK2_COLOOP"],
            "all_source_keys_classified_by_weight": True,
            "exact_boundary_interior_split_claimed": False,
            "combined_key_count_lower_bound": FORCED_SIGNED_OCCUPANCY,
            "interior_key_count": None,
            "boundary_key_count": None,
        },
        "hyperplane_nonforcing_certified_at_most": 67,
        "literal_prime_field_68_cutoff_transferred": False,
        "high_baseline_is_owner": False,
        "independent_per_layer_root_unions_close_row": False,
        "global_terminal": GLOBAL_TERMINAL,
    }


def atom_records(partition_digest: str) -> list[dict[str, Any]]:
    common = {
        "architecture_id": ARCHITECTURE_ID,
        "partition_sha256": partition_digest,
        "unit": UNIT,
        "quantifier": QUANTIFIER,
    }
    return [
        {
            "atom_id": "U_paid",
            **common,
            "value": LOW_CAP,
            "status": "BANKABLE_SOURCE_BOUND_EXACT_UPPER",
            "bankable": True,
            "bankability_gate": "PARTITION_DIGEST_UNIT_QUANTIFIER_AND_SOURCE_HASHES_VERIFIED",
            "owner_ids": ["LOW_EXACT_WEIGHT_PACKING"],
            "source_binding_roles": [
                "adapter_note",
                "rank46_source",
                "rank46_verifier",
                "rank46_manifest",
            ],
            "predicate_source_role": "adapter_note",
            "theorem_pointer": "m31_list_v4_source_adapter_global_coupled_residual.md#3",
            "source_statement": "Uniformly in the received word, exact-error weights 0<=j<=614160 contain at most 3730 codewords.",
            "transport_role": "NOT_APPLICABLE",
            "unresolved_hypotheses": [],
        },
        {
            "atom_id": "U_Q",
            **common,
            "value": None,
            "status": "OPEN_UNPAID",
            "bankable": False,
            "bankability_gate": "NOT_APPLICABLE",
            "owner_ids": [],
            "source_binding_roles": ["active_v4_ledger", "adapter_note", "admissibility_authority"],
            "predicate_source_role": "active_v4_ledger",
            "theorem_pointer": "experimental/grande_finale.tex:7556",
            "source_statement": "No certified boundary-prefix target-map owner is supplied by this adapter.",
            "transport_role": "NOT_APPLICABLE",
            "unresolved_hypotheses": ["M31_CERTIFIED_BOUNDARY_PREFIX_OWNER_OPEN"],
        },
        {
            "atom_id": "U_list_int",
            **common,
            "value": None,
            "status": "OPEN_UNPAID",
            "bankable": False,
            "bankability_gate": "NOT_APPLICABLE",
            "owner_ids": [],
            "source_binding_roles": ["active_v4_ledger", "adapter_note", "admissibility_authority"],
            "predicate_source_role": "active_v4_ledger",
            "theorem_pointer": "experimental/grande_finale.tex:7556",
            "source_statement": "No certified arbitrary-word interior chart inventory and add-back is supplied by this adapter.",
            "transport_role": "NOT_APPLICABLE",
            "unresolved_hypotheses": ["M31_ARBITRARY_WORD_INTERIOR_OWNER_OPEN"],
        },
        {
            "atom_id": "U_ext",
            **common,
            "value": None,
            "status": "OPEN_UNPAID",
            "bankable": False,
            "bankability_gate": "NOT_APPLICABLE",
            "owner_ids": [],
            "source_binding_roles": [
                "active_v4_ledger",
                "adapter_note",
                "scalar_descent_theorem",
                "scalar_descent_verifier",
            ],
            "predicate_source_role": "active_v4_ledger",
            "theorem_pointer": "experimental/grande_finale.tex:7556",
            "source_statement": "Direct target-field lift and scalar-descent cross-check do not constitute an additive extension-projection payment.",
            "transport_role": "SCALAR_DESCENT_IS_PREPROCESSING_NOT_EXTENSION_PAYMENT",
            "unresolved_hypotheses": ["M31_ADDITIVE_EXTENSION_PROJECTION_OWNER_OPEN"],
        },
        {
            "atom_id": "U_new",
            **common,
            "value": None,
            "status": "OPEN_UNPAID",
            "bankable": False,
            "bankability_gate": "NOT_APPLICABLE",
            "owner_ids": [],
            "source_binding_roles": [
                "adapter_note",
                "admissibility_authority",
                "full_layer_source",
                "coupled_source",
                "coupled_verifier",
                "coupled_manifest",
            ],
            "predicate_source_role": "adapter_note",
            "theorem_pointer": "m31_list_v4_source_adapter_global_coupled_residual.md#6",
            "source_statement": "Every high-weight codeword reaches a fixed boundary or interior residual; rank-46 marked keys are diagnostic subwitnesses only.",
            "transport_role": "NOT_APPLICABLE",
            "unresolved_hypotheses": [BOUNDARY_CODEWORD_TERMINAL, INTERIOR_CODEWORD_TERMINAL],
        },
    ]


def closure_state() -> dict[str, Any]:
    return {
        "closed": False,
        "row_closed": False,
        "banked_atoms": ["U_paid"],
        "banked_atom_count": 1,
        "known_sum": LOW_CAP,
        "high_residual_payment_movement": 0,
        "official_row_score_movement": 0,
        "closed_total": None,
        "B_star": BUDGET,
        "unresolved_atom_ids": ["U_Q", "U_list_int", "U_ext", "U_new"],
        "unpaid_global_residual": {
            "terminal": GLOBAL_TERMINAL,
            "high_weight_codeword_mass_lower_bound": HIGH_MASS_LOWER,
            "baseline_high_codeword_mass": BASELINE_HIGH_MASS,
            "marked_key_count_lower_bound": FORCED_SIGNED_OCCUPANCY,
            "exact_boundary_interior_key_split_claimed": False,
            "interior_rank46_key_count": None,
            "boundary_rank46_key_count": None,
            "exact_owner_charge": None,
            "residual_atom": "U_new",
            "forced_into_existing_owner": False,
            "source_realized_counterexample_constructed": False,
        },
        "official_theorem_claimed": False,
    }


SOURCE_SPECS: tuple[tuple[str, str, str], ...] = (
    ("adapter_schema", "experimental/data/schemas/m31_list_v4_source_adapter_v1.schema.json", "RUNTIME_SCHEMA_CONTRACT"),
    ("adapter_verifier", "experimental/scripts/verify_m31_list_v4_source_adapter_v1.py", "PRIMARY_STANDARD_LIBRARY_REPLAY"),
    ("adapter_note", "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md", "SOURCE_ADAPTER_THEOREM_AND_SCOPE"),
    ("active_v4_ledger", "experimental/grande_finale.tex", "CURRENT_V4_FIVE_ATOM_LIST_CHRONOLOGY"),
    ("admissibility_authority", "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex", "NON_ORACULAR_DECLARED_PARTITION_AND_OWNER_ADMISSIBILITY"),
    ("deployed_row_packet", "experimental/data/certificates/frontier-adjacent/m31_list_v1.packet.json", "DEPLOYED_ROW_CONSTANTS_ONLY_STALE_V3_ARCHITECTURE_NOT_IMPORTED"),
    ("scalar_descent_theorem", "experimental/notes/thresholds/m31_scalar_descent_equivalence.md", "THRESHOLD_L_SCALAR_DESCENT_THEOREM"),
    ("scalar_descent_verifier", "experimental/scripts/verify_m31_scalar_descent_equivalence.py", "THRESHOLD_L_SCALAR_DESCENT_ARITHMETIC"),
    ("full_layer_source", "experimental/notes/thresholds/m31_full_packet_pade_forney_source.md", "EXACT_SUPPORT_FULL_LAYER_SOURCE_THEOREM"),
    ("full_layer_verifier", "experimental/scripts/verify_m31_full_packet_pade_forney.py", "EXACT_SUPPORT_FULL_LAYER_ARITHMETIC_REPLAY"),
    ("rank46_source", "experimental/notes/thresholds/m31_canonical_popov_rank46_compiler.md", "LOW_WEIGHT_PACKING_AND_SIGNED_OCCUPANCY_SOURCE"),
    ("rank46_verifier", "experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py", "LOW_WEIGHT_PACKING_AND_SIGNED_OCCUPANCY_REPLAY"),
    ("rank46_manifest", "experimental/data/certificates/m31-canonical-popov-rank46-compiler/manifest.json", "PREDECESSOR_ARITHMETIC_PAYLOAD_STALE_V4_SOURCE_PIN_NOT_IMPORTED"),
    ("coupled_source", "experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md", "COUPLED_LOCATOR_NUMERATOR_KERNEL_THEOREM"),
    ("coupled_verifier", "experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py", "COUPLED_KERNEL_ARITHMETIC_AND_MUTATION_REPLAY"),
    ("coupled_manifest", "experimental/data/certificates/m31-coupled-escape-forney-plucker-route-cut/manifest.json", "COUPLED_PACKET_SCOPE_AND_NONCLAIMS"),
)

INDEPENDENT_SOURCE_SPEC = (
    "adapter_independent_verifier",
    "experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py",
    "INDEPENDENT_STANDARD_LIBRARY_REPLAY",
)

SAGE_SOURCE_SPEC = (
    "adapter_sage_verifier",
    "experimental/scripts/verify_m31_list_v4_source_adapter_v1.sage",
    "EXACT_CROSS_FIELD_SOURCE_TRANSPORT_REPLAY",
)


def source_specs() -> list[tuple[str, str, str]]:
    specs = list(SOURCE_SPECS[:3])
    if INDEPENDENT_PATH.exists():
        specs.append(INDEPENDENT_SOURCE_SPEC)
    if SAGE_ADAPTER_PATH.exists():
        specs.append(SAGE_SOURCE_SPEC)
    specs.extend(SOURCE_SPECS[3:])
    return specs


def validate_relative_source_path(relative: str) -> Path:
    require(isinstance(relative, str) and relative.isascii(), "source path ASCII string")
    require("\\" not in relative and "\x00" not in relative, "source path separators")
    pure = PurePosixPath(relative)
    require(not pure.is_absolute(), "source path relative")
    require(len(pure.parts) >= 2, "source path depth")
    require(pure.parts[0] in {"archived", "docs", "experimental", "site", "tex"}, "source path root")
    require(all(part not in {"", ".", ".."} and not part.startswith(".") for part in pure.parts), "source path canonical components")
    require(str(pure) == relative, "source path canonical spelling")
    path = ROOT.joinpath(*pure.parts)
    require(path.exists() and path.is_file(), f"source path exists: {relative}")
    require(not path.is_symlink(), f"source path is not symlink: {relative}")
    current = ROOT
    for part in pure.parts[:-1]:
        current = current / part
        require(not current.is_symlink(), f"source parent is not symlink: {relative}")
    require(path.resolve().is_relative_to(ROOT.resolve()), f"source path remains in repository: {relative}")
    return path


def internal_payload_sha(role: str, path: Path) -> str | None:
    if role != "rank46_manifest":
        return None
    value, _ = strict_json_path(path)
    require(type(value) is dict, "rank46 manifest object")
    claimed = value.get("certificate_sha256")
    require(isinstance(claimed, str) and len(claimed) == 64, "rank46 internal certificate hash shape")
    unsigned = copy.deepcopy(value)
    unsigned.pop("certificate_sha256", None)
    require(sha256_bytes(canonical_json(unsigned)) == claimed, "rank46 internal certificate hash")
    return claimed


def source_bindings() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen_inodes: set[tuple[int, int]] = set()
    for role, relative, scope in source_specs():
        path = validate_relative_source_path(relative)
        stat = path.stat()
        inode = (stat.st_dev, stat.st_ino)
        require(inode not in seen_inodes, f"source hardlink alias: {relative}")
        seen_inodes.add(inode)
        result.append(
            {
                "binding_id": f"M31_LIST_V4_SOURCE::{role}",
                "role": role,
                "path": relative,
                "sha256": sha256_path(path),
                "internal_payload_sha256": internal_payload_sha(role, path),
                "scope": scope,
            }
        )
    return result


def build_template() -> dict[str, Any]:
    require(P == 2_147_483_647, "Mersenne-31 prime value")
    require((N, K, AGREEMENT, SHIFT, RADIUS) == (2_097_152, 1_048_576, 1_116_023, 67_447, 981_129), "M31 row constants")
    require((BUDGET, FORBIDDEN) == (16_777_215, 16_777_216), "M31 budget boundary")
    require(SCALAR_LEFT < SCALAR_RIGHT and SCALAR_MARGIN == 592_061_458_020_761_914_489_814_638_395_392, "strict scalar-descent margin")
    require((HIGH_LAYER_COUNT, BASELINE_HIGH_MASS, BASE_MASS) == (366_969, 16_513_605, 16_517_335), "rank-46 occupancy base")
    require((SAFE_SIGNED_OCCUPANCY, FORCED_SIGNED_OCCUPANCY) == (259_880, 259_881), "signed occupancy boundary")
    require(HIGH_MASS_LOWER == 16_773_486, "high codeword mass lower bound")

    partition = partition_contract()
    payload = {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "row_contract": row_contract(),
        "source_transport": source_transport(),
        "source_universe": source_universe(),
        "partition": partition,
        "coupled_rank46": coupled_rank46(),
        "atoms": atom_records(partition["partition_sha256"]),
        "closure_state": closure_state(),
        "source_bindings": source_bindings(),
    }
    return seal_payload(payload)


def schema_pointer(document: Any, pointer: str) -> Any:
    require(pointer.startswith("#/"), f"local schema pointer: {pointer}")
    value = document
    for raw in pointer[2:].split("/"):
        part = raw.replace("~1", "/").replace("~0", "~")
        require(isinstance(value, dict) and part in value, f"schema pointer resolves: {pointer}")
        value = value[part]
    return value


def validate_schema_document() -> None:
    schema, _ = strict_json_path(SCHEMA_PATH)
    require(type(schema) is dict, "schema document object")
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft")
    require(schema.get("properties", {}).get("schema", {}).get("const") == SCHEMA_ID, "schema ID const")
    require(schema.get("properties", {}).get("architecture_id", {}).get("const") == ARCHITECTURE_ID, "schema architecture const")
    require(schema.get("properties", {}).get("status", {}).get("const") == STATUS, "schema open status const")
    atoms = schema.get("properties", {}).get("atoms", {})
    require(atoms.get("minItems") == atoms.get("maxItems") == 5, "schema five atoms")
    prefix = atoms.get("prefixItems")
    require(isinstance(prefix, list) and len(prefix) == 5 and atoms.get("items") is False, "schema fixed atom tuple")
    found_atom_ids = [
        item["allOf"][1]["properties"]["atom_id"]["const"] for item in prefix
    ]
    require(found_atom_ids == list(ATOM_ORDER), "schema v4 atom order")
    require(schema["$defs"]["atom"]["properties"]["unit"]["const"] == UNIT, "schema codeword unit")
    require(schema["$defs"]["atom"]["properties"]["quantifier"]["const"] == QUANTIFIER, "schema received-word quantifier")
    bindings = schema["properties"]["source_bindings"]
    require((bindings["minItems"], bindings["maxItems"]) == (16, 18), "schema source registry cardinality")

    def walk(value: Any) -> Iterable[str]:
        if isinstance(value, dict):
            if "$ref" in value:
                yield value["$ref"]
            for child in value.values():
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)

    for pointer in walk(schema):
        require(isinstance(pointer, str) and pointer.startswith("#/"), "schema uses only local refs")
        schema_pointer(schema, pointer)


def validate_source_registry(candidate: list[dict[str, Any]]) -> None:
    require(type(candidate) is list, "source registry list")
    expected = source_bindings()
    deep_exact(candidate, expected, "source_bindings")
    roles = [entry["role"] for entry in candidate]
    binding_ids = [entry["binding_id"] for entry in candidate]
    paths = [entry["path"] for entry in candidate]
    require(len(roles) == len(set(roles)), "source roles unique")
    require(len(binding_ids) == len(set(binding_ids)), "source binding IDs unique")
    require(len(paths) == len(set(paths)), "source paths unique")


def validate_payload(candidate: dict[str, Any]) -> None:
    require(type(candidate) is dict, "manifest object")
    require_ascii_strings(candidate)
    require(candidate.get("payload_sha256") == payload_sha256(candidate), "canonical payload hash")

    expected = build_template()
    require(set(candidate) == set(expected), "manifest exact top-level keys")
    deep_exact(candidate["row_contract"], row_contract(), "row_contract")

    transport = candidate["source_transport"]
    deep_exact(transport, source_transport(), "source_transport")
    direct = transport["direct_target_field_lift"]
    require(direct["field_generic"] is True and direct["full_target_list_objectwise"] is True, "direct quartic objectwise lift")
    require(transport["scalar_descent_is_sole_transport"] is False, "scalar descent is not sole transport")
    require(transport["U_ext_zero_claimed"] is False, "transport does not set U_ext to zero")
    scalar = transport["scalar_descent_crosscheck"]
    require(int(scalar["left_LtH"]) == FORBIDDEN * RADIUS * KILLING_FUNCTIONALS, "scalar left recomputation")
    require(int(scalar["right_gN"]) == G * PROJECTIVE_FUNCTIONALS, "scalar right recomputation")
    require(int(scalar["strict_margin"]) == int(scalar["right_gN"]) - int(scalar["left_LtH"]), "scalar margin recomputation")
    require(int(scalar["left_LtH"]) < int(scalar["right_gN"]), "scalar inequality remains strict")

    universe = candidate["source_universe"]
    deep_exact(universe, source_universe(), "source_universe")
    recomputed_extremizer = compute_extremizer(universe["sharp_arithmetic_extremizer"]["weight_blocks"])
    for key, value in recomputed_extremizer.items():
        deep_exact(universe["sharp_arithmetic_extremizer"][key], value, f"source_universe.sharp_arithmetic_extremizer.{key}")
    require(universe["low_weight_cap"] + universe["high_weight_layer_count"] * universe["free_baseline"] == BASE_MASS, "occupancy baseline recomputation")
    require(universe["full_list_mass_lower_bound"] - BASE_MASS == FORCED_SIGNED_OCCUPANCY, "occupancy forbidden threshold recomputation")
    require(universe["high_baseline_is_owner"] is False, "baseline 45 is not an owner")

    partition = candidate["partition"]
    require(partition.get("partition_sha256") == partition_sha256(partition), "partition canonical digest")
    deep_exact(partition, partition_contract(), "partition")
    require([stage["atom_id"] for stage in partition["chronology_stages"]] == list(ATOM_ORDER), "five-stage chronology")
    require(partition["owner_order"] == ["LOW_EXACT_WEIGHT_PACKING", BOUNDARY_CODEWORD_CELL, INTERIOR_CODEWORD_CELL], "fixed first-match owner order")

    coupled = candidate["coupled_rank46"]
    deep_exact(coupled, coupled_rank46(), "coupled_rank46")
    require(coupled["one_row_key_bound"] * 2 == coupled["rank2_key_bound"], "rank-two degree arithmetic")
    require(coupled["one_row_key_bound"] * 3 == coupled["rank3_key_bound"], "rank-three degree arithmetic")
    require(coupled["rank3_key_bound"] < coupled["cutoff_uniform_min"], "rank-three strict source cutoff")

    atoms = candidate["atoms"]
    require(type(atoms) is list and len(atoms) == 5, "five atom records")
    deep_exact(atoms, atom_records(partition["partition_sha256"]), "atoms")
    require([atom["atom_id"] for atom in atoms] == list(ATOM_ORDER), "atom record order")
    require(all(atom["partition_sha256"] == partition["partition_sha256"] for atom in atoms), "atoms share partition digest")
    require(atoms[0]["value"] == LOW_CAP and all(atom["value"] is None for atom in atoms[1:]), "one non-null bankable atom")
    require(atoms[3]["transport_role"] == "SCALAR_DESCENT_IS_PREPROCESSING_NOT_EXTENSION_PAYMENT", "U_ext preprocessing guard")

    deep_exact(candidate["closure_state"], closure_state(), "closure_state")
    validate_source_registry(candidate["source_bindings"])
    deep_exact(candidate, expected, "manifest")


def reseal_all(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    if isinstance(out.get("partition"), dict):
        out["partition"] = seal_partition(out["partition"])
        digest = out["partition"]["partition_sha256"]
        if isinstance(out.get("atoms"), list):
            for atom in out["atoms"]:
                if isinstance(atom, dict):
                    atom["partition_sha256"] = digest
    return seal_payload(out)


def set_path(payload: dict[str, Any], path: Sequence[Any], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def path_mutation(path: Sequence[Any], value: Any, *, repartition: bool = False) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def mutate(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        set_path(out, path, value)
        return reseal_all(out) if repartition else seal_payload(out)
    return mutate


def delete_path_mutation(path: Sequence[Any], *, repartition: bool = False) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def mutate(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        target: Any = out
        for key in path[:-1]:
            target = target[key]
        del target[path[-1]]
        return reseal_all(out) if repartition else seal_payload(out)
    return mutate


def tamper_selftest(expected: dict[str, Any]) -> int:
    source_hash_index = next(index for index, row in enumerate(expected["source_bindings"]) if row["role"] == "rank46_source")
    source_path_index = next(index for index, row in enumerate(expected["source_bindings"]) if row["role"] == "deployed_row_packet")
    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("stale-v3-architecture", path_mutation(("architecture_id",), "GRANDE_FINALE_V3_EXACT_COMPLETION")),
        ("slope-unit", path_mutation(("row_contract", "unit"), "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE")),
        ("received-line-quantifier", path_mutation(("row_contract", "quantifier"), "UNIFORM_OVER_ALL_RECEIVED_LINES")),
        ("q-gen-line-swap", path_mutation(("row_contract", "q_gen"), Q)),
        ("q-line-base-field", path_mutation(("row_contract", "q_line"), str(P))),
        ("direct-lift-field-generic", path_mutation(("source_transport", "direct_target_field_lift", "field_generic"), False)),
        ("scalar-kind-as-primary", path_mutation(("source_transport", "kind"), "THRESHOLD_L_INJECTION_NOT_FULL_LIST_BIJECTION")),
        ("direct-lift-prime-only", path_mutation(("source_transport", "direct_target_field_lift", "field"), "F_p")),
        ("direct-lift-not-objectwise", path_mutation(("source_transport", "direct_target_field_lift", "full_target_list_objectwise"), False)),
        ("scalar-sole-transport", path_mutation(("source_transport", "scalar_descent_is_sole_transport"), True)),
        ("transport-sets-U-ext-zero", path_mutation(("source_transport", "U_ext_zero_claimed"), True)),
        ("L-equals-budget", path_mutation(("source_transport", "scalar_descent_crosscheck", "threshold_L"), BUDGET)),
        ("scalar-nonstrict", path_mutation(("source_transport", "scalar_descent_crosscheck", "strict_inequality"), False)),
        ("domain-outside-base", path_mutation(("source_transport", "scalar_descent_crosscheck", "domain_in_base_field"), False)),
        ("projection-collision", path_mutation(("source_transport", "scalar_descent_crosscheck", "selected_codewords_injective"), False)),
        ("false-support-preservation", path_mutation(("source_transport", "scalar_descent_crosscheck", "exact_error_supports_preserved"), True)),
        ("forbid-new-agreements", path_mutation(("source_transport", "scalar_descent_crosscheck", "new_agreements_may_appear"), False)),
        ("scalar-public-map-overclaim", path_mutation(("source_transport", "scalar_descent_crosscheck", "public_objectwise_partition_map"), True)),
        ("scalar-as-extension-payment", path_mutation(("source_transport", "scalar_descent_crosscheck", "ledger_atom"), "U_ext")),
        ("full-list-capped-by-L", path_mutation(("source_universe", "object"), "SELECTED_L_SUBLIST_EXACT_WEIGHT_HISTOGRAM")),
        ("projected-universe", path_mutation(("source_universe", "projected_list_used"), True)),
        ("selected-sublist-histogram", path_mutation(("source_universe", "selected_L_sublist_used_for_histogram"), True)),
        ("construct-counterexample", path_mutation(("source_universe", "source_realized_counterexample_constructed"), True)),
        ("omit-containment", path_mutation(("source_universe", "exact_containment_retained"), False)),
        ("omit-escapes", path_mutation(("source_universe", "every_one_point_escape_retained"), False)),
        ("support-not-codeword", path_mutation(("source_universe", "support_to_codeword_injective"), False)),
        ("small-ball-one-per-weight", path_mutation(("source_universe", "small_ball_total_mass_cap"), SMALL_BALL_CUTOFF + 1)),
        ("same-weight-36", path_mutation(("source_universe", "same_weight_layer_forced_lower"), 36)),
        ("cutoff-off-by-one", path_mutation(("source_universe", "low_weight_cutoff"), J0 - 1)),
        ("low-cap-off-by-one", path_mutation(("source_universe", "low_weight_cap"), LOW_CAP + 1)),
        ("packing-rounding", path_mutation(("source_universe", "low_weight_packing", "first_excluded_contradiction_margin"), 0)),
        ("baseline-as-owner", path_mutation(("source_universe", "high_baseline_is_owner"), True)),
        ("discard-low-credit", path_mutation(("source_universe", "occupancy_identity", "C_low_definition"), "0")),
        ("discard-level-credit", path_mutation(("source_universe", "occupancy_identity", "C_r_definition"), "0")),
        ("signed-threshold-minus-one", path_mutation(("source_universe", "occupancy_identity", "forbidden_signed_occupancy_min"), 259_880)),
        ("marked-key-lower-minus-one", path_mutation(("source_universe", "marked_key_contract", "forced_key_count_lower_bound"), 259_880)),
        ("anchors-as-owners", path_mutation(("source_universe", "marked_key_contract", "anchors_charged_as_owners"), True)),
        ("lex-key-as-payment", path_mutation(("source_universe", "marked_key_contract", "lexicographic_keying_is_payment_owner"), True)),
        ("extremizer-realized", path_mutation(("source_universe", "sharp_arithmetic_extremizer", "source_realized"), True)),
        ("extremizer-multiplicity", path_mutation(("source_universe", "sharp_arithmetic_extremizer", "weight_blocks", 2, "multiplicity_per_weight"), 47)),
        ("extremizer-key-count", path_mutation(("source_universe", "sharp_arithmetic_extremizer", "weight_blocks", 2, "rank46_keys_per_weight"), 0)),
        ("extremizer-overlap", path_mutation(("source_universe", "sharp_arithmetic_extremizer", "weight_blocks", 2, "weight_start"), 721_248)),
        ("occupancy-level-46", path_mutation(("source_universe", "sharp_arithmetic_extremizer", "occupancy_level_counts", 45, "occupied_high_layers"), 259_880)),
        ("partition-atom-order", path_mutation(("partition", "atom_order"), ["U_paid", "U_Q", "U_ext", "U_list_int", "U_new"], repartition=True)),
        ("partition-owner-order", path_mutation(("partition", "owner_order"), ["LOW_EXACT_WEIGHT_PACKING", INTERIOR_CODEWORD_CELL, BOUNDARY_CODEWORD_CELL], repartition=True)),
        ("partition-codeword-incomplete", path_mutation(("partition", "source_codeword_partition_exhaustive"), False, repartition=True)),
        ("partition-addback-incomplete", path_mutation(("partition", "source_codeword_addback_complete"), False, repartition=True)),
        ("payment-complete-overclaim", path_mutation(("partition", "payment_partition_complete"), True, repartition=True)),
        ("low-owner-not-bankable", path_mutation(("partition", "low_weight_owner", "bankable"), False, repartition=True)),
        ("boundary-auto-Q", path_mutation(("partition", "residual_terminals", 0, "automatically_owned_by_U_Q"), True, repartition=True)),
        ("interior-auto-list", path_mutation(("partition", "residual_terminals", 1, "automatically_owned_by_U_list_int"), True, repartition=True)),
        ("U-paid-value", path_mutation(("atoms", 0, "value"), LOW_CAP - 1)),
        ("U-paid-not-bankable", path_mutation(("atoms", 0, "bankable"), False)),
        ("U-paid-unbound", path_mutation(("atoms", 0, "bankability_gate"), "NOT_APPLICABLE")),
        ("U-Q-zero", path_mutation(("atoms", 1, "value"), 0)),
        ("U-list-int-zero", path_mutation(("atoms", 2, "value"), 0)),
        ("U-ext-zero", path_mutation(("atoms", 3, "value"), 0)),
        ("U-ext-folded", path_mutation(("atoms", 3, "transport_role"), "NOT_APPLICABLE")),
        ("U-new-zero", path_mutation(("atoms", 4, "value"), 0)),
        ("missing-U-ext", delete_path_mutation(("atoms", 3))),
        ("swap-U-ext-list", lambda payload: seal_payload({**copy.deepcopy(payload), "atoms": [payload["atoms"][0], payload["atoms"][1], payload["atoms"][3], payload["atoms"][2], payload["atoms"][4]]})),
        ("packet-columns", path_mutation(("coupled_rank46", "packet_columns"), 45)),
        ("joint-index-count-45", path_mutation(("coupled_rank46", "small_forney_indices"), 45)),
        ("one-row-bound", path_mutation(("coupled_rank46", "one_row_key_bound"), 20_766)),
        ("rank2-bound", path_mutation(("coupled_rank46", "rank2_key_bound"), 41_531)),
        ("rank3-bound", path_mutation(("coupled_rank46", "rank3_key_bound"), 62_296)),
        ("strict-cutoff-equality", path_mutation(("coupled_rank46", "cutoff_uniform_min"), RANK3_BOUND)),
        ("rank4-overclaim", path_mutation(("coupled_rank46", "rank4_certified_by_aggregate_bound"), True)),
        ("padded-actual-frame", path_mutation(("coupled_rank46", "boundary_vs_interior", "actual_error_locator_coupled_frame_has_agreement_padding"), True)),
        ("padding-bridge-paid", path_mutation(("coupled_rank46", "boundary_vs_interior", "canonical_padded_v4_adapter_bridge"), "PAID")),
        ("interior-auto-owner", path_mutation(("coupled_rank46", "boundary_vs_interior", "interior_automatically_owned_by_U_list_int"), True)),
        ("exact-key-split-overclaim", path_mutation(("coupled_rank46", "boundary_vs_interior", "exact_boundary_interior_split_claimed"), True)),
        ("per-key-root-union-closes", path_mutation(("coupled_rank46", "independent_per_layer_root_unions_close_row"), True)),
        ("hyperplane-68-transfer", path_mutation(("coupled_rank46", "literal_prime_field_68_cutoff_transferred"), True)),
        ("hyperplane-nonforcing-68", path_mutation(("coupled_rank46", "hyperplane_nonforcing_certified_at_most"), 68)),
        ("force-global-owner", path_mutation(("coupled_rank46", "global_terminal"), "PAID_OWNER")),
        ("row-closed", path_mutation(("closure_state", "row_closed"), True)),
        ("banked-atom-omitted", path_mutation(("closure_state", "banked_atoms"), [])),
        ("banked-atom-count", path_mutation(("closure_state", "banked_atom_count"), 0)),
        ("known-sum", path_mutation(("closure_state", "known_sum"), LOW_CAP - 1)),
        ("high-residual-payment-movement", path_mutation(("closure_state", "high_residual_payment_movement"), 1)),
        ("official-row-score-movement", path_mutation(("closure_state", "official_row_score_movement"), 1)),
        ("closed-total", path_mutation(("closure_state", "closed_total"), LOW_CAP)),
        ("residual-mass-minus-one", path_mutation(("closure_state", "unpaid_global_residual", "high_weight_codeword_mass_lower_bound"), HIGH_MASS_LOWER - 1)),
        ("residual-key-minus-one", path_mutation(("closure_state", "unpaid_global_residual", "marked_key_count_lower_bound"), 259_880)),
        ("residual-charge-zero", path_mutation(("closure_state", "unpaid_global_residual", "exact_owner_charge"), 0)),
        ("residual-forced-owner", path_mutation(("closure_state", "unpaid_global_residual", "forced_into_existing_owner"), True)),
        ("official-theorem", path_mutation(("closure_state", "official_theorem_claimed"), True)),
        ("source-hash", path_mutation(("source_bindings", source_hash_index, "sha256"), "0" * 64)),
        ("source-path-alias", path_mutation(("source_bindings", source_path_index, "path"), "experimental/data/certificates/frontier-adjacent/../frontier-adjacent/m31_list_v1.packet.json")),
        ("source-binding-id", path_mutation(("source_bindings", source_hash_index, "binding_id"), "M31_LIST_V4_SOURCE::wrong")),
        ("unicode", path_mutation(("atoms", 0, "source_statement"), "weight \u2264 614160")),
        ("float", path_mutation(("atoms", 0, "value"), 3730.0)),
        ("extra-key", path_mutation(("row_contract", "unexpected"), 1)),
        ("missing-key", delete_path_mutation(("row_contract", "unit"))),
    ]

    rejected = 0
    for label, mutator in mutations:
        candidate = mutator(expected)
        try:
            validate_payload(candidate)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")

    malformed_json = (
        '{"a":1,"a":2}',
        '{"a":1.0}',
        '{"a":NaN}',
        '{"a":Infinity}',
    )
    for index, text in enumerate(malformed_json):
        try:
            strict_json_loads(text)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"malformed JSON accepted: {index}")

    require(rejected == len(mutations) + len(malformed_json), "all semantic and JSON mutations rejected")
    return rejected


def check_manifest(path: Path) -> None:
    require(path.exists() and path.is_file(), f"manifest exists: {path}")
    candidate, _ = strict_json_path(path, canonical_file=True)
    validate_payload(candidate)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--check", action="store_true", help="validate the pinned or supplied manifest")
    parser.add_argument("--tamper-selftest", action="store_true", help="run hostile semantic mutations")
    parser.add_argument("--print-template", action="store_true", help="emit the canonical open manifest to stdout")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.check or args.tamper_selftest or args.print_template):
        args.check = True

    validate_schema_document()
    expected = build_template()
    validate_payload(expected)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
    if args.check:
        check_manifest(args.manifest)
    if args.tamper_selftest:
        rejected = tamper_selftest(expected)
        print(f"M31 LIST v4 source-adapter mutations: {rejected}/{rejected} rejected PASS")

    if not args.print_template:
        print("M31 LIST v4 source adapter: PASS")
        print("atoms: U_paid=3730 BANKED; U_Q/U_list_int/U_ext/U_new=null")
        print("source chronology: direct quartic lift / full target-codeword partition PASS")
        print("diagnostic occupancy: Xi46>=259881; baseline 45H is not an owner PASS")
        print("coupled key bounds: 20765 / 41530 / 62295 < 67447 PASS")
        print(f"terminal: {GLOBAL_TERMINAL}; row OPEN; high-residual payment movement 0; official row/score movement 0")
        print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
