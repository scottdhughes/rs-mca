#!/usr/bin/env python3
"""Strict certificate checker for the exact t=2 core-source cover census."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-t2-core-source-coordinate-cover-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_T2_CORE_SOURCE_COORDINATE_COVER_CENSUS"
STATUS = "PROVED_EXACT_TOY_CORE_SOURCE_LOW_CARRIER_CLOSURE"
SAGE_SCHEMA = SCHEMA + "-sage"
SAGE_PAYLOAD_SHA256 = (
    "9a45f639c6c87bb7cfdc554805895235cda62139c9a504279795fbb203097be3"
)
LINE_RECORDS_SHA256 = (
    "384b40b21b1cfc07420c14f75a2e3de37096b41b6c31c5cadc0e43a5c513a332"
)
CORE_HISTOGRAM_SHA256 = (
    "b9dea1936974d9e6c0b91f6d9bd4ec006362bcee009c1a33e2bb4c7a4d6e17a8"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-t2-core-source-coordinate-cover-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_t2_core_source_coordinate_cover_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_t2_core_source_coordinate_cover_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-t2-core-source-coordinate-cover-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.sage"
)
PREDECESSOR_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_t2_source_compatible_control_v1.md"
)
PREDECESSOR_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-t2-source-compatible-control-v1/"
    "m1_kb_branch3_rank9_t2_source_compatible_control_v1.json"
)
OWNER_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_low_excess_carrier_cut_v1.md"
)
OWNER_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-low-excess-carrier-cut-v1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.json"
)
CONTRACT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_5_mask_contract_v1.md"
)

NONCLAIMS = [
    "This packet does not instantiate the KoalaBear field or domain.",
    "This packet does not bind the deployed first-match owner projections.",
    "This packet does not check rank-nine geometry for every source line.",
    "This packet does not prove a deployed rank-nine aggregate bound.",
    "This packet does not determine U_Q or U_A.",
    "This packet does not move U_paid or B_remaining.",
    "This packet does not authorize Lean or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """A parser, source, schema, arithmetic, or semantic check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def reject_float(value: str) -> None:
    raise VerificationError(f"floating-point JSON number: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path}")
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing bound source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(
    binding_id: str, relative: Path, role: str
) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def predecessor_payload(relative: Path) -> str:
    value = load_json(ROOT / relative)
    require(
        value.get("payload_sha256") == payload_hash(value),
        f"bad predecessor payload hash: {relative}",
    )
    return str(value["payload_sha256"])


def positive_carrier_cap(R: int, j: int, kappa: int) -> int:
    require(type(R) is type(j) is type(kappa) is int, "noninteger cap input")
    require(kappa >= 1, "positive carrier cap requires kappa>=1")
    denominator = math.comb(R + kappa - j - 1, kappa)
    require(denominator > 0, "carrier cap denominator vanished")
    return math.comb(R + kappa, kappa + 1) // denominator


def public_line(
    *, alpha: list[int], beta: list[int], state: list[int], core_count: int
) -> dict[str, Any]:
    return {
        "alpha_coordinates": alpha,
        "beta_coordinates": beta,
        "post_deep_slope_count": 287,
        "common_available_coordinate_range": [3, 35],
        "common_available_coordinate_mask_hex": "1ffffffff",
        "common_available_coordinate_count": 33,
        "core_subset_count": core_count,
        "core_product_state": state,
        "classification": "AT_OR_BEFORE_LOW_CARRIER",
    }


def expected_certificate() -> dict[str, Any]:
    source_bindings = [
        source_binding("packet-note", NOTE_REL, "exact finite theorem and scope"),
        source_binding("packet-readme", README_REL, "replay instructions"),
        source_binding("packet-python", PYTHON_REL, "strict certificate checker"),
        source_binding("packet-sage", SAGE_REL, "exact finite-field census"),
        source_binding(
            "predecessor-note",
            PREDECESSOR_NOTE_REL,
            "nonzero-witness classification and canonical control",
        ),
        source_binding("owner-note", OWNER_NOTE_REL, "low-carrier owner"),
        source_binding(
            "selector-contract", CONTRACT_NOTE_REL, "first-match quantifiers"
        ),
    ]
    low_examples = [
        public_line(alpha=[1, 0], beta=[1, 0], state=[27, 28], core_count=4281),
        public_line(alpha=[1, 0], beta=[2, 0], state=[158, 28], core_count=4222),
        public_line(alpha=[1, 0], beta=[3, 0], state=[111, 28], core_count=4208),
    ]
    canonical = public_line(
        alpha=[13, 7], beta=[5, 14], state=[69, 207], core_count=4295
    )
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": source_bindings,
        "predecessor_bindings": {
            "t2_source_control_payload": predecessor_payload(PREDECESSOR_CERT_REL),
            "low_excess_owner_payload": predecessor_payload(OWNER_CERT_REL),
        },
        "sage_replay": {
            "schema": SAGE_SCHEMA,
            "status": "PASS",
            "classification": "EXACT_TOY_CORE_SOURCE_COORDINATE_COVER_CENSUS",
            "payload_sha256": SAGE_PAYLOAD_SHA256,
            "compact_line_records_sha256": LINE_RECORDS_SHA256,
            "core_multiplicity_histogram_sha256": CORE_HISTOGRAM_SHA256,
        },
        "field": {
            "characteristic": 17,
            "degree": 2,
            "cardinality": 289,
            "modulus_coefficients_ascending": [3, 16, 1],
            "primitive_generator_order": 288,
            "omega_coordinates": [12, 16],
            "omega_order": 36,
        },
        "row": {"n": 36, "k": 14, "R": 22, "j": 20, "A": 16, "t": 2},
        "dynamic_program": {
            "coordinate_count": 33,
            "core_size": 12,
            "locator_root_size": 13,
            "state_space_size_per_cardinality": 83_521,
            "core_subset_count": 354_817_320,
            "locator_subset_count": 573_166_440,
            "reachable_core_product_states": 82_944,
            "reachable_locator_product_states": 82_944,
            "availability_mask_bits": 33,
            "full_witness_universe_enumerated": True,
            "every_nonzero_locator_state_has_full_coordinate_mask": True,
            "coordinate_order_invariant": True,
            "brute_force_control": {
                "fixture_coordinate_count": 6,
                "fixture_subset_size": 3,
                "fixture_subset_count": 20,
                "counts_and_masks_match": True,
            },
            "canonical_fixed_root_crosscheck": {
                "fixed_coordinate": 3,
                "post_deep_slope_count": 287,
                "compatible_support_count": 780_907,
                "witness_count_min": 2_571,
                "witness_count_max": 2_833,
                "matches_predecessor_mitm": True,
            },
        },
        "source_line_census": {
            "source_line_count": 82_944,
            "source_line_formula": "(q-1)^2",
            "source_line_map_injective_on_product_states": True,
            "all_nonzero_alpha_beta_pairs_realized": True,
            "post_deep_slope_count_min": 287,
            "post_deep_slope_count_max": 287,
            "post_deep_slope_count_histogram": {"287": 82_944},
            "core_multiplicity_min": 4_072,
            "core_multiplicity_max": 4_521,
            "core_multiplicity_distinct_values": 399,
            "core_multiplicity_histogram_sha256": CORE_HISTOGRAM_SHA256,
            "common_available_coordinate_count_histogram": {"33": 82_944},
            "low_carrier_line_count": 82_944,
            "unresolved_source_map_line_count": 0,
            "compact_line_records_sha256": LINE_RECORDS_SHA256,
            "low_examples": low_examples,
            "unresolved_examples": [],
        },
        "canonical_predecessor_line": canonical,
        "coordinate_cover_lemma": {
            "fixed_gamma_identity": (
                "kappa_star=max(0,k-3-max_selector_common_root_count)"
            ),
            "k14_low_equivalence": (
                "kappa_star<=10 iff intersection_eta A_eta is nonempty"
            ),
            "selector_choices_independent_across_slopes": True,
            "availability_is_full_for_every_censused_line": True,
            "singleton_gate_specific_to_k14": True,
            "multiple_available_coordinates_not_claimed_simultaneous": True,
            "low_direction_deletion_monotone": True,
            "high_direction_deletion_monotone": False,
        },
        "full_frontier": {
            "finite_slope_count_per_line": 289,
            "deep_exception_count_per_line": 2,
            "post_deep_slope_count_per_line": 287,
            "partition_exact_for_every_line": True,
            "deep_owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
        },
        "low_carrier_exit": {
            "certified_common_coordinate": 3,
            "selector_carrier_size_upper_bound": 32,
            "selector_carrier_excess_upper_bound": 10,
            "exact_kappa_star_claimed": False,
            "carrier_cap": 11_729_498,
            "post_deep_slope_count": 287,
            "cap_pays_every_line": True,
            "all_source_lines_paid_at_or_before_low_carrier": True,
        },
        "first_match": {
            "earlier_owner_projections_source_bound": False,
            "literal_first_match_gamma_available": False,
            "full_post_deep_envelope_exact_for_every_line": True,
            "low_certificate_restricts_to_every_retained_subset": True,
            "empty_cover_line_count": 0,
            "unpaid_primitive_source_line_count": 0,
            "conclusion": "DEEP_OR_AT_OR_BEFORE_LOW_CARRIER_FOR_ALL_CORE_SOURCE_LINES",
        },
        "scope_guards": {
            "toy_scale_only": True,
            "deployed_field_instantiated": False,
            "koalabear_rank9_closed": False,
            "rank9_geometry_checked_for_every_source_line": False,
            "ledger_movement": 0,
            "U_Q_determined": False,
            "U_A_determined": False,
            "lean_authorized": False,
        },
        "nonclaims": NONCLAIMS,
    }
    result["payload_sha256"] = canonical_hash(result)
    return result


def exact_int(value: Any, label: str) -> int:
    require(type(value) is int, f"{label} is not an exact integer")
    return value


def verify_semantics(value: dict[str, Any]) -> None:
    require(value == expected_certificate(), "certificate differs from exact fixture")
    require(value.get("payload_sha256") == payload_hash(value),
            "payload hash mismatch")

    field = value["field"]
    p = exact_int(field["characteristic"], "field.characteristic")
    q = exact_int(field["cardinality"], "field.cardinality")
    require((p, q) == (17, p * p), "field size drift")
    require(field["primitive_generator_order"] == q - 1
            and field["omega_order"] == 36
            and (q - 1) % 36 == 0,
            "field/domain order drift")

    row = value["row"]
    n = exact_int(row["n"], "row.n")
    k = exact_int(row["k"], "row.k")
    R = exact_int(row["R"], "row.R")
    j = exact_int(row["j"], "row.j")
    A = exact_int(row["A"], "row.A")
    t = exact_int(row["t"], "row.t")
    require((R, A, t) == (n - k, n - j, R - j), "row arithmetic drift")
    require((n, k, R, j, A, t) == (36, 14, 22, 20, 16, 2),
            "row left the audited interface")

    dp = value["dynamic_program"]
    require(dp["coordinate_count"] == n - 3 == 33,
            "nonsource coordinate count drift")
    require(dp["core_size"] == k - 2 == 12
            and dp["locator_root_size"] == k - 1 == 13,
            "core/locator size drift")
    require(dp["state_space_size_per_cardinality"] == q * q,
            "product-pair state-space drift")
    require(dp["core_subset_count"] == math.comb(33, 12)
            and dp["locator_subset_count"] == math.comb(33, 13),
            "subset census drift")
    nonzero_pairs = (q - 1) ** 2
    require(dp["reachable_core_product_states"] == nonzero_pairs
            and dp["reachable_locator_product_states"] == nonzero_pairs,
            "nonzero product-pair coverage drift")
    require(dp["availability_mask_bits"] == 33
            and dp["full_witness_universe_enumerated"] is True
            and dp["every_nonzero_locator_state_has_full_coordinate_mask"] is True
            and dp["coordinate_order_invariant"] is True,
            "availability DP completeness drift")
    brute = dp["brute_force_control"]
    require(brute == {
        "fixture_coordinate_count": 6,
        "fixture_subset_size": 3,
        "fixture_subset_count": math.comb(6, 3),
        "counts_and_masks_match": True,
    }, "brute-force DP control drift")
    fixed = dp["canonical_fixed_root_crosscheck"]
    require(fixed == {
        "fixed_coordinate": 3,
        "post_deep_slope_count": q - 2,
        "compatible_support_count": 780_907,
        "witness_count_min": 2_571,
        "witness_count_max": 2_833,
        "matches_predecessor_mitm": True,
    }, "canonical fixed-root cross-check drift")

    census = value["source_line_census"]
    require(census["source_line_count"] == nonzero_pairs
            and census["source_line_formula"] == "(q-1)^2"
            and census["all_nonzero_alpha_beta_pairs_realized"] is True,
            "source-line census drift")
    require(census["post_deep_slope_count_min"]
            == census["post_deep_slope_count_max"] == q - 2,
            "post-deep slope count drift")
    require(census["post_deep_slope_count_histogram"]
            == {str(q - 2): nonzero_pairs},
            "post-deep slope histogram drift")
    require(census["common_available_coordinate_count_histogram"]
            == {"33": nonzero_pairs},
            "coordinate-cover histogram drift")
    require(census["low_carrier_line_count"] == nonzero_pairs
            and census["unresolved_source_map_line_count"] == 0
            and census["unresolved_examples"] == [],
            "source-line owner partition drift")
    require(census["compact_line_records_sha256"] == LINE_RECORDS_SHA256
            and census["core_multiplicity_histogram_sha256"]
            == CORE_HISTOGRAM_SHA256,
            "census hash drift")

    for index, line in enumerate(
        census["low_examples"] + [value["canonical_predecessor_line"]]
    ):
        require(line["post_deep_slope_count"] == q - 2,
                f"example {index} slope count drift")
        require(line["common_available_coordinate_range"] == [3, n - 1]
                and line["common_available_coordinate_mask_hex"] == "1ffffffff"
                and line["common_available_coordinate_count"] == n - 3,
                f"example {index} cover drift")
        require(line["classification"] == "AT_OR_BEFORE_LOW_CARRIER",
                f"example {index} classification drift")

    lemma = value["coordinate_cover_lemma"]
    require(lemma["selector_choices_independent_across_slopes"] is True
            and lemma["availability_is_full_for_every_censused_line"] is True,
            "coordinate-cover lemma quantifier drift")
    require(lemma["singleton_gate_specific_to_k14"] is True
            and lemma["multiple_available_coordinates_not_claimed_simultaneous"] is True,
            "coordinate-cover scope drift")
    require(lemma["low_direction_deletion_monotone"] is True
            and lemma["high_direction_deletion_monotone"] is False,
            "deletion monotonicity drift")

    frontier = value["full_frontier"]
    require(frontier["finite_slope_count_per_line"] == q
            and frontier["deep_exception_count_per_line"] == 2
            and frontier["post_deep_slope_count_per_line"] == q - 2,
            "full/deep/post-deep partition drift")
    require(frontier["partition_exact_for_every_line"] is True
            and frontier["deep_owner_id"]
            == "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
            "full-frontier owner drift")

    low = value["low_carrier_exit"]
    require(low["certified_common_coordinate"] in range(3, n),
            "certified coordinate left B")
    require(low["selector_carrier_size_upper_bound"] == (n - 3) - 1 == 32,
            "selector carrier bound drift")
    require(low["selector_carrier_excess_upper_bound"] == 32 - R == 10,
            "selector excess bound drift")
    require(low["exact_kappa_star_claimed"] is False,
            "availability masks overclaimed exact kappa_star")
    require(low["carrier_cap"] == positive_carrier_cap(R, j, 10)
            == 11_729_498,
            "carrier cap drift")
    require(low["carrier_cap"] >= low["post_deep_slope_count"] == q - 2
            and low["cap_pays_every_line"] is True
            and low["all_source_lines_paid_at_or_before_low_carrier"] is True,
            "low-carrier payment drift")

    first_match = value["first_match"]
    require(first_match["earlier_owner_projections_source_bound"] is False
            and first_match["literal_first_match_gamma_available"] is False,
            "unbound earlier owner was silently promoted")
    require(first_match["full_post_deep_envelope_exact_for_every_line"] is True
            and first_match["low_certificate_restricts_to_every_retained_subset"] is True,
            "monotone full-envelope closure drift")
    require(first_match["empty_cover_line_count"] == 0
            and first_match["unpaid_primitive_source_line_count"] == 0,
            "primitive source line invented")
    require(first_match["conclusion"]
            == "DEEP_OR_AT_OR_BEFORE_LOW_CARRIER_FOR_ALL_CORE_SOURCE_LINES",
            "first-match conclusion drift")

    guards = value["scope_guards"]
    require(guards == {
        "toy_scale_only": True,
        "deployed_field_instantiated": False,
        "koalabear_rank9_closed": False,
        "rank9_geometry_checked_for_every_source_line": False,
        "ledger_movement": 0,
        "U_Q_determined": False,
        "U_A_determined": False,
        "lean_authorized": False,
    }, "scope guard drift")
    require(value["nonclaims"] == NONCLAIMS, "nonclaim list drift")


def run_check() -> None:
    value = load_json(CERT_PATH)
    verify_semantics(value)
    print("M1 t=2 core-source coordinate-cover census: PASS")
    print("  82,944/82,944 source lines: AT_OR_BEFORE_LOW_CARRIER")
    print("  every line: 287 post-deep slopes; 33/33 coordinates available")
    print("  empty-cover lines: 0; deployed ledger unchanged")


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-mutated")),
        ("kind", lambda d: d.__setitem__("artifact_kind", "DEPLOYED_THEOREM")),
        ("status", lambda d: d.__setitem__("status", "KOALABEAR_CLOSED")),
        ("sage-payload", lambda d: d["sage_replay"].__setitem__("payload_sha256", "0" * 64)),
        ("line-hash", lambda d: d["sage_replay"].__setitem__("compact_line_records_sha256", "1" * 64)),
        ("field", lambda d: d["field"].__setitem__("cardinality", 288)),
        ("modulus", lambda d: d["field"]["modulus_coefficients_ascending"].__setitem__(1, 15)),
        ("row", lambda d: d["row"].__setitem__("k", 13)),
        ("state-space", lambda d: d["dynamic_program"].__setitem__("state_space_size_per_cardinality", 82_944)),
        ("core-count", lambda d: d["dynamic_program"].__setitem__("core_subset_count", 354_817_319)),
        ("locator-count", lambda d: d["dynamic_program"].__setitem__("locator_subset_count", 573_166_439)),
        ("core-states", lambda d: d["dynamic_program"].__setitem__("reachable_core_product_states", 82_943)),
        ("witness-states", lambda d: d["dynamic_program"].__setitem__("reachable_locator_product_states", 82_943)),
        ("mask-width", lambda d: d["dynamic_program"].__setitem__("availability_mask_bits", 32)),
        ("witness-scope", lambda d: d["dynamic_program"].__setitem__("full_witness_universe_enumerated", False)),
        ("state-cover", lambda d: d["dynamic_program"].__setitem__("every_nonzero_locator_state_has_full_coordinate_mask", False)),
        ("order", lambda d: d["dynamic_program"].__setitem__("coordinate_order_invariant", False)),
        ("brute", lambda d: d["dynamic_program"]["brute_force_control"].__setitem__("counts_and_masks_match", False)),
        ("fixed-root", lambda d: d["dynamic_program"]["canonical_fixed_root_crosscheck"].__setitem__("fixed_coordinate", 4)),
        ("fixed-total", lambda d: d["dynamic_program"]["canonical_fixed_root_crosscheck"].__setitem__("compatible_support_count", 780_906)),
        ("source-lines", lambda d: d["source_line_census"].__setitem__("source_line_count", 82_943)),
        ("all-lines", lambda d: d["source_line_census"].__setitem__("all_nonzero_alpha_beta_pairs_realized", False)),
        ("slope-histogram", lambda d: d["source_line_census"]["post_deep_slope_count_histogram"].__setitem__("287", 82_943)),
        ("cover-histogram", lambda d: d["source_line_census"]["common_available_coordinate_count_histogram"].__setitem__("33", 82_943)),
        ("low-count", lambda d: d["source_line_census"].__setitem__("low_carrier_line_count", 82_943)),
        ("unresolved", lambda d: d["source_line_census"].__setitem__("unresolved_source_map_line_count", 1)),
        ("example-cover", lambda d: d["source_line_census"]["low_examples"][0].__setitem__("common_available_coordinate_mask_hex", "0ffffffff")),
        ("canonical-alpha", lambda d: d["canonical_predecessor_line"].__setitem__("alpha_coordinates", [12, 7])),
        ("lemma", lambda d: d["coordinate_cover_lemma"].__setitem__("k14_low_equivalence", "support-only")),
        ("simultaneous", lambda d: d["coordinate_cover_lemma"].__setitem__("multiple_available_coordinates_not_claimed_simultaneous", False)),
        ("low-monotonicity", lambda d: d["coordinate_cover_lemma"].__setitem__("low_direction_deletion_monotone", False)),
        ("high-monotonicity", lambda d: d["coordinate_cover_lemma"].__setitem__("high_direction_deletion_monotone", True)),
        ("deep-count", lambda d: d["full_frontier"].__setitem__("deep_exception_count_per_line", 0)),
        ("deep-owner", lambda d: d["full_frontier"].__setitem__("deep_owner_id", "UNPAID")),
        ("coordinate", lambda d: d["low_carrier_exit"].__setitem__("certified_common_coordinate", 2)),
        ("carrier", lambda d: d["low_carrier_exit"].__setitem__("selector_carrier_size_upper_bound", 33)),
        ("excess", lambda d: d["low_carrier_exit"].__setitem__("selector_carrier_excess_upper_bound", 11)),
        ("exact-kappa", lambda d: d["low_carrier_exit"].__setitem__("exact_kappa_star_claimed", True)),
        ("cap", lambda d: d["low_carrier_exit"].__setitem__("carrier_cap", 286)),
        ("earlier-bound", lambda d: d["first_match"].__setitem__("earlier_owner_projections_source_bound", True)),
        ("literal-gamma", lambda d: d["first_match"].__setitem__("literal_first_match_gamma_available", True)),
        ("primitive", lambda d: d["first_match"].__setitem__("unpaid_primitive_source_line_count", 1)),
        ("conclusion", lambda d: d["first_match"].__setitem__("conclusion", "RANK9_PRIMITIVE")),
        ("deployed", lambda d: d["scope_guards"].__setitem__("deployed_field_instantiated", True)),
        ("rank9", lambda d: d["scope_guards"].__setitem__("koalabear_rank9_closed", True)),
        ("ledger", lambda d: d["scope_guards"].__setitem__("ledger_movement", 1)),
        ("UQ", lambda d: d["scope_guards"].__setitem__("U_Q_determined", True)),
        ("lean", lambda d: d["scope_guards"].__setitem__("lean_authorized", True)),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
        ("type-bool-int", lambda d: d["row"].__setitem__("n", True)),
        ("type-string-int", lambda d: d["dynamic_program"].__setitem__("core_size", "12")),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "2" * 64)),
        ("predecessor", lambda d: d["predecessor_bindings"].__setitem__("t2_source_control_payload", "3" * 64)),
        ("payload", lambda d: d.__setitem__("payload_sha256", "4" * 64)),
    ]


def run_tamper_selftest() -> None:
    baseline = expected_certificate()
    verify_semantics(baseline)
    passed = 0
    for label, mutate in mutation_cases():
        changed = copy.deepcopy(baseline)
        mutate(changed)
        if label != "payload":
            changed["payload_sha256"] = payload_hash(changed)
        try:
            verify_semantics(changed)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"semantic mutation survived: {label}")

    parser_cases = [
        ('{"schema":"x","schema":"y"}', "duplicate-key"),
        ('{"x":1.25}', "float"),
        ('{"x":NaN}', "nonstandard-constant"),
        ('[1,2,3]', "top-level-list"),
    ]
    for text, label in parser_cases:
        try:
            parse_json(text, label)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"parser mutation survived: {label}")
    expected = len(mutation_cases()) + len(parser_cases)
    require(passed == expected, "tamper selftest count drift")
    print(f"M1 t=2 core-source cover mutations: {passed}/{expected} PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    args = parser.parse_args()
    if args.check:
        run_check()
    elif args.tamper_selftest:
        run_tamper_selftest()
    else:
        print(json.dumps(expected_certificate(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
