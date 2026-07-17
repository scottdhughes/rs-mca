#!/usr/bin/env python3
"""Strict certificate checker for the exact t=2 cyclic source controls."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-rank9-t2-source-compatible-control-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_RANK9_T2_SOURCE_COMPATIBLE_TOY_CONTROLS"
STATUS = "PROVED_EXACT_T2_TOY_DEEP_AND_POSTDEEP_LOW_CARRIER_EXITS"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-rank9-t2-source-compatible-control-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_rank9_t2_source_compatible_control_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_t2_source_compatible_control_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-t2-source-compatible-control-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.sage"
)
ATLAS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)
ATLAS_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-rich-pencil-atlas-v1/"
    "m1_kb_branch3_rank9_rich_pencil_atlas_v1.json"
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
T1_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.md"
)
T1_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-cyclic-rich-pencil-control-v1/"
    "m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.json"
)
DEEP_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_deep_ccl_tdd_v1.md"
)
DEEP_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-deep-ccl-tdd-v1/"
    "m1_kb_branch3_deep_ccl_tdd_v1.json"
)

SAGE_SCHEMA = (
    "rs-mca-m1-kb-branch3-rank9-t2-source-compatible-control-v1-sage"
)
SAGE_PAYLOAD_SHA256 = (
    "a29ddccaca0acd5e95efe7cab1ef113fa07ceff2816541681abeac83a6afa0fe"
)
N35_INVENTORY_SHA256 = (
    "24150857548e5bc9ee199e1d088bdcfb458191579db247a65ed311e5dfbc590e"
)
N36_INVENTORY_SHA256 = (
    "ceeef4c9024450f0c935a0ae0aaf6b4dab693a7605f404f65f1655eac8ae0452"
)

N35_OUTLIERS = [
    [3, 4, 8, 9, 11, 12, 14, 16, 19, 20, 28, 30],
    [7, 14, 16, 19, 20, 23, 24, 27, 29, 30, 31, 32],
    [4, 7, 9, 11, 12, 15, 21, 23, 29, 30, 32, 33],
    [4, 6, 7, 16, 19, 22, 24, 28, 29, 30, 31, 34],
    [4, 5, 7, 11, 12, 13, 17, 18, 20, 28, 30, 31],
    [4, 5, 7, 11, 12, 22, 23, 27, 28, 30, 33, 34],
    [3, 7, 10, 13, 18, 19, 22, 24, 30, 31, 33, 34],
    [4, 5, 6, 7, 10, 11, 17, 18, 25, 26, 27, 33],
]

N36_OUTLIERS = [
    [4, 6, 7, 10, 12, 13, 14, 17, 18, 19, 21, 22, 34],
    [6, 7, 11, 13, 15, 18, 21, 22, 24, 26, 27, 30, 34],
    [7, 8, 12, 13, 15, 17, 18, 19, 21, 23, 30, 32, 35],
    [6, 7, 8, 9, 10, 13, 15, 16, 18, 19, 20, 22, 31],
    [3, 6, 18, 21, 23, 24, 25, 26, 27, 30, 32, 33, 35],
    [5, 8, 9, 13, 19, 21, 22, 24, 25, 26, 29, 31, 32],
    [5, 6, 10, 12, 13, 18, 23, 25, 26, 31, 32, 33, 34],
    [3, 6, 11, 15, 17, 19, 20, 22, 23, 29, 31, 33, 35],
]

NONCLAIMS = [
    "This packet does not instantiate the KoalaBear field or cyclic domain.",
    "This packet does not provide a deployed complete-selector inventory.",
    "This packet does not promote either 29-slope local family to a complete selector.",
    "This packet does not prove a deployed rank-nine residual or aggregate bound.",
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


def expected_row(
    *,
    p: int,
    modulus: list[int],
    omega: list[int],
    row: dict[str, int],
    core: list[int],
    alpha: list[int],
    beta: list[int],
    outliers: list[list[int]],
    local_carrier: int,
    local_excess: int,
    gcd_degree: int,
    compatible: int,
    slopes: int,
    count_range: list[int],
    excluded: list[list[int]],
    inventory_hash: str,
    fixed_root: int | None,
    common_roots: list[int],
    complete_carrier: int,
    complete_excess: int,
    structural_maximum_excess: int,
) -> dict[str, Any]:
    moving = [index for index in range(3, row["n"]) if index not in core]
    k = row["k"]
    R = row["R"]
    A = row["A"]
    n = row["n"]
    deep_threshold = R // 3
    exact_B_part = list(range(3, A + 2))
    full_B = list(range(3, n))
    deep_exceptions = [
        {
            "label": "ETA_ZERO",
            "slope_coordinates": [0, 0],
            "witness_codeword": "ZERO_POLYNOMIAL",
            "exact_A_witness_support": [1] + exact_B_part,
            "full_agreement_set": [1] + full_B,
            "actual_error_support": [0, 2],
            "actual_error_weight": 2,
            "restricted_generator_rank": k,
            "augmented_epsilon1_rank": k + 1,
            "hankel_rank": 2,
            "deep_threshold": deep_threshold,
            "owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
        },
        {
            "label": "ETA_NEG_ALPHA_OVER_BETA",
            "slope_coordinates": excluded[1],
            "witness_codeword": "ZERO_POLYNOMIAL",
            "exact_A_witness_support": [2] + exact_B_part,
            "full_agreement_set": [2] + full_B,
            "actual_error_support": [0, 1],
            "actual_error_weight": 2,
            "restricted_generator_rank": k,
            "augmented_epsilon1_rank": k + 1,
            "hankel_rank": 2,
            "deep_threshold": deep_threshold,
            "owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
        },
    ]
    uniform_nt = {
        "target_source": "EPSILON_0",
        "forced_zero_set": "S_UNION_{b}",
        "forced_zero_count": k,
        "degree_strict_upper_bound": k,
        "contradictory_value_index": 0,
        "applies_to_every_compatible_support": True,
        "applies_to_every_lex_representative": True,
    }
    return {
        "field": {
            "characteristic": p,
            "degree": 2,
            "cardinality": p * p,
            "modulus_coefficients_ascending": modulus,
            "primitive_generator_order": p * p - 1,
            "omega_coordinates": omega,
            "omega_order": row["n"],
        },
        "row": row,
        "source": {
            "sparse_indices": [0, 1, 2],
            "core": core,
            "moving_indices": moving,
            "canonical_alpha_coordinates": alpha,
            "canonical_beta_coordinates": beta,
            "compatibility_equation": "q_S(c)=alpha+beta*q_S(b)",
            "nonzero_witness_profile": [k - 1, 3],
            "uniform_nonzero_locator_noncontainment": {
                "target_source": "EPSILON_0",
                "forced_zero_set": "S_UNION_{b}",
                "forced_zero_count": k,
                "degree_strict_upper_bound": k,
                "contradictory_value_index": 0,
                "selected_direct_rank_check": True,
                "proof_covers_all_inventory_representatives": True,
            },
        },
        "rank9_local_control": {
            "complete_selector": False,
            "root_set_count": 29,
            "outliers": outliers,
            "slope_count": 29,
            "affine_rank": 9,
            "raw_rank": 10,
            "carrier_size": local_carrier,
            "carrier_excess": local_excess,
            "hankel_rank": 2,
            "transverse_tuple": [20, 21, 21],
            "source_syndrome_frobenius_rank": 4,
            "noncontainment_target": "EPSILON_0",
            "restricted_generator_rank": k,
            "augmented_target_rank": k + 1,
            "uniform_nonzero_locator_noncontainment": True,
            "rich_line_size": 21,
            "rich_gcd_degree": gcd_degree,
            "rich_moving_support_size": 21,
            "rich_x": 1,
        },
        "full_finite_frontier": {
            "finite_slope_count": p * p,
            "deep_exception_count": 2,
            "post_deep_nonzero_locator_slope_count": slopes,
            "partition_exact": True,
        },
        "deep_exceptions": {
            "owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
            "deep_threshold": deep_threshold,
            "exception_count": 2,
            "exceptions": deep_exceptions,
            "zero_word_contained_for_every_nonspecial_slope": True,
            "nonzero_codeword_minimum_weight": R + 1,
            "received_word_maximum_weight": 3,
            "nonzero_codeword_error_lower_bound": R + 1 - 3,
            "exceptions_are_exact": True,
        },
        "post_deep_nonzero_locator_inventory": {
            "root_sets_represented": math.comb(32, 12),
            "half_table_size_each": 1 << 16,
            "fixed_root": fixed_root,
            "compatible_support_count": compatible,
            "slope_count": slopes,
            "witness_count_min": count_range[0],
            "witness_count_max": count_range[1],
            "omitted_deep_slopes": excluded,
            "inventory_sha256": inventory_hash,
            "lex_selector_common_roots": common_roots,
            "lex_selector_carrier_size": complete_carrier,
            "lex_selector_carrier_excess": complete_excess,
            "uniform_nonzero_locator_noncontainment": uniform_nt,
        },
        "post_deep_low_carrier_exit": {
            "ansatz_structural_maximum_excess": structural_maximum_excess,
            "lex_selector_excess": complete_excess,
            "lex_selector_cap": positive_carrier_cap(22, 20, complete_excess),
            "exact_post_deep_slope_count": slopes,
            "owner_applies_at_or_before_low_carrier": True,
            "no_rank9_residual_from_local_subfamily": True,
        },
    }


def expected_certificate() -> dict[str, Any]:
    bindings = [
        source_binding("packet-note", NOTE_REL, "exact theorem and scope"),
        source_binding("packet-readme", README_REL, "replay instructions"),
        source_binding("packet-python", PYTHON_REL, "strict certificate checker"),
        source_binding("packet-sage", SAGE_REL, "exact finite-field replay"),
        source_binding("atlas-note", ATLAS_NOTE_REL, "rich-pencil atlas identity"),
        source_binding("owner-note", OWNER_NOTE_REL, "low-carrier owner"),
        source_binding("selector-contract", CONTRACT_NOTE_REL, "selector quantifiers"),
        source_binding("t1-control-note", T1_NOTE_REL, "preceding cyclic toy control"),
        source_binding("deep-owner-note", DEEP_NOTE_REL, "extended deep owner theorem interface"),
    ]
    n35 = expected_row(
        p=29,
        modulus=[2, 24, 1],
        omega=[26, 16],
        row={"n": 35, "k": 13, "R": 22, "j": 20, "A": 15, "t": 2},
        core=list(range(3, 14)),
        alpha=[28, 28],
        beta=[2, 23],
        outliers=N35_OUTLIERS,
        local_carrier=32,
        local_excess=10,
        gcd_degree=11,
        compatible=268_998,
        slopes=839,
        count_range=[259, 390],
        excluded=[[0, 0], [12, 15]],
        inventory_hash=N35_INVENTORY_SHA256,
        fixed_root=None,
        common_roots=[3, 4, 5],
        complete_carrier=29,
        complete_excess=7,
        structural_maximum_excess=10,
    )
    n36 = expected_row(
        p=17,
        modulus=[3, 16, 1],
        omega=[12, 16],
        row={"n": 36, "k": 14, "R": 22, "j": 20, "A": 16, "t": 2},
        core=list(range(3, 15)),
        alpha=[13, 7],
        beta=[5, 14],
        outliers=N36_OUTLIERS,
        local_carrier=33,
        local_excess=11,
        gcd_degree=12,
        compatible=780_907,
        slopes=287,
        count_range=[2_571, 2_833],
        excluded=[[0, 0], [1, 15]],
        inventory_hash=N36_INVENTORY_SHA256,
        fixed_root=3,
        common_roots=[3, 4, 5, 6, 7, 8],
        complete_carrier=27,
        complete_excess=5,
        structural_maximum_excess=11,
    )
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": bindings,
        "predecessor_bindings": {
            "rich_pencil_atlas_payload": predecessor_payload(ATLAS_CERT_REL),
            "low_excess_owner_payload": predecessor_payload(OWNER_CERT_REL),
            "t1_cyclic_control_payload": predecessor_payload(T1_CERT_REL),
            "extended_deep_owner_payload": predecessor_payload(DEEP_CERT_REL),
        },
        "sage_replay": {
            "schema": SAGE_SCHEMA,
            "status": "PASS",
            "classification": (
                "EXACT_T2_CYCLIC_SOURCE_COMPATIBLE_DEEP_PLUS_LOW_CARRIER_CONTROLS"
            ),
            "payload_sha256": SAGE_PAYLOAD_SHA256,
            "n35_inventory_sha256": N35_INVENTORY_SHA256,
            "n36_inventory_sha256": N36_INVENTORY_SHA256,
        },
        "n35": n35,
        "n36": n36,
        "minimality": {
            "scope": (
                "POST_DEEP_NONZERO_LOCATOR_THREE_SOURCE_"
                "ONE_MOVING_ROOT_ANSATZ"
            ),
            "rich_moving_root_target": 21,
            "three_sparse_source_coordinates": 3,
            "t": 2,
            "minimum_R": 22,
            "maximum_carrier_excess_formula": "k-3",
            "minimum_k_for_excess_11": 14,
            "minimum_n_for_excess_11": 36,
        },
        "first_match": {
            "conclusion": "DEEP_OR_AT_OR_BEFORE_LOW_CARRIER",
            "full_frontier_partitioned_exactly": True,
            "two_zero_polynomial_slopes_owned_by_extended_deep": True,
            "owner_is_existential_over_complete_selectors": True,
            "earlier_deletion_is_monotone_safe": True,
            "n35_every_post_deep_nonzero_locator_selector_excess_at_most_10": True,
            "n36_fixed_root_inventory_is_complete_post_deep_frontier": True,
            "local_rank9_families_are_not_complete_selectors": True,
        },
        "scope_guards": {
            "toy_scale_only": True,
            "deployed_field_instantiated": False,
            "deployed_complete_selector_inventory": False,
            "koalabear_rank9_closed": False,
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
    for label in ("n35", "n36"):
        item = value[label]
        row = item["row"]
        n = exact_int(row["n"], f"{label}.n")
        k = exact_int(row["k"], f"{label}.k")
        R = exact_int(row["R"], f"{label}.R")
        j = exact_int(row["j"], f"{label}.j")
        A = exact_int(row["A"], f"{label}.A")
        t = exact_int(row["t"], f"{label}.t")
        require((R, A, t) == (n - k, n - j, R - j),
                f"{label} row arithmetic drift")
        require(A == k + 2 and t == 2, f"{label} left t=2 interface")
        field = item["field"]
        p = exact_int(field["characteristic"], f"{label}.p")
        require(field["cardinality"] == p * p,
                f"{label} field cardinality drift")
        require((p * p - 1) % n == 0 and field["omega_order"] == n,
                f"{label} cyclic order drift")
        source = item["source"]
        require(len(source["core"]) == k - 2
                and len(source["moving_indices"]) == 21,
                f"{label} rich core/moving dimensions drift")
        require(source["nonzero_witness_profile"] == [k - 1, 3],
                f"{label} witness profile drift")
        source_nt = source["uniform_nonzero_locator_noncontainment"]
        require(source_nt["forced_zero_count"] == k
                and source_nt["degree_strict_upper_bound"] == k
                and source_nt["proof_covers_all_inventory_representatives"] is True,
                f"{label} uniform nonzero-locator NT drift")
        local = item["rank9_local_control"]
        require(local["complete_selector"] is False,
                f"{label} local family promoted to complete")
        require((local["root_set_count"], local["slope_count"])
                == (29, 29), f"{label} local inventory drift")
        require((local["affine_rank"], local["raw_rank"])
                == (9, 10), f"{label} rank tuple drift")
        require(local["hankel_rank"] == 2
                and local["source_syndrome_frobenius_rank"] == 4,
                f"{label} Hankel/Frobenius drift")
        require((local["restricted_generator_rank"],
                 local["augmented_target_rank"]) == (k, k + 1)
                and local["uniform_nonzero_locator_noncontainment"] is True,
                f"{label} selected direct NT drift")

        full = item["full_finite_frontier"]
        require(full == {
            "finite_slope_count": p * p,
            "deep_exception_count": 2,
            "post_deep_nonzero_locator_slope_count": p * p - 2,
            "partition_exact": True,
        }, f"{label} full/deep/post-deep partition drift")

        deep = item["deep_exceptions"]
        require(deep["owner_id"]
                == "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
                f"{label} deep owner drift")
        require(deep["deep_threshold"] == R // 3 == 7
                and deep["exception_count"] == 2
                and deep["exceptions_are_exact"] is True,
                f"{label} deep threshold/count drift")
        require(deep["nonzero_codeword_minimum_weight"] == R + 1 == 23
                and deep["received_word_maximum_weight"] == 3
                and deep["nonzero_codeword_error_lower_bound"] == 20 > R // 3,
                f"{label} exact-deep MDS separation drift")
        require(deep["zero_word_contained_for_every_nonspecial_slope"] is True,
                f"{label} nonspecial zero-word containment drift")
        special = deep["exceptions"]
        require([entry["label"] for entry in special]
                == ["ETA_ZERO", "ETA_NEG_ALPHA_OVER_BETA"],
                f"{label} deep labels drift")
        require([entry["slope_coordinates"] for entry in special]
                == [[0, 0], item["post_deep_nonzero_locator_inventory"]
                    ["omitted_deep_slopes"][1]],
                f"{label} exceptional slopes drift")
        for position, entry in enumerate(special):
            anchor = 1 + position
            require(entry["witness_codeword"] == "ZERO_POLYNOMIAL"
                    and entry["actual_error_weight"] == 2
                    and entry["hankel_rank"] == 2
                    and entry["deep_threshold"] == 7,
                    f"{label} special witness weight/Hankel drift")
            require(entry["exact_A_witness_support"]
                    == [anchor] + list(range(3, A + 2))
                    and len(entry["exact_A_witness_support"]) == A,
                    f"{label} special exact-A support drift")
            require(entry["full_agreement_set"]
                    == [anchor] + list(range(3, n)),
                    f"{label} special full agreement drift")
            require(entry["actual_error_support"]
                    == ([0, 2] if position == 0 else [0, 1]),
                    f"{label} special actual support drift")
            require((entry["restricted_generator_rank"],
                     entry["augmented_epsilon1_rank"]) == (k, k + 1),
                    f"{label} special NT ranks drift")

        post_deep_inventory = item["post_deep_nonzero_locator_inventory"]
        require(post_deep_inventory["root_sets_represented"] == math.comb(32, 12),
                f"{label} represented support total drift")
        require(post_deep_inventory["half_table_size_each"] == 1 << 16,
                f"{label} half-table size drift")
        require(post_deep_inventory["slope_count"] == p * p - 2,
                f"{label} post-deep frontier is not q-2")
        require(post_deep_inventory["omitted_deep_slopes"][0] == [0, 0]
                and len(post_deep_inventory["omitted_deep_slopes"]) == 2,
                f"{label} omitted deep slope interface drift")
        inventory_nt = post_deep_inventory[
            "uniform_nonzero_locator_noncontainment"
        ]
        require(inventory_nt["forced_zero_count"] == k
                and inventory_nt["applies_to_every_compatible_support"] is True,
                f"{label} inventory NT quantifier drift")
        complete_excess = exact_int(
            post_deep_inventory["lex_selector_carrier_excess"],
            f"{label}.complete_excess",
        )
        require(post_deep_inventory["lex_selector_carrier_size"]
                - R == complete_excess,
                f"{label} selector carrier arithmetic drift")
        exit_data = item["post_deep_low_carrier_exit"]
        require(exit_data["lex_selector_cap"]
                == positive_carrier_cap(R, j, complete_excess),
                f"{label} carrier cap drift")
        require(exit_data["lex_selector_cap"]
                >= post_deep_inventory["slope_count"],
                f"{label} low-carrier cap does not pay frontier")
        require(exit_data["owner_applies_at_or_before_low_carrier"] is True,
                f"{label} first-match conclusion drift")

    n35 = value["n35"]
    require(len(range(3, 35)) - n35["row"]["R"] == 10,
            "n35 structural carrier cut drift")
    require(positive_carrier_cap(22, 20, 10) == 11_729_498,
            "n35 structural excess-ten cap drift")
    require(n35["post_deep_low_carrier_exit"]
            ["ansatz_structural_maximum_excess"] == 10,
            "n35 structural maximum excess drift")

    n36 = value["n36"]
    require(n36["rank9_local_control"]["carrier_excess"] == 11,
            "n36 local high-carrier control drift")
    require(n36["post_deep_nonzero_locator_inventory"]["fixed_root"] == 3
            and n36["post_deep_nonzero_locator_inventory"]
            ["lex_selector_carrier_excess"] == 5,
            "n36 complete fixed-root selector drift")
    minimality = value["minimality"]
    require(minimality == {
        "scope": "POST_DEEP_NONZERO_LOCATOR_THREE_SOURCE_ONE_MOVING_ROOT_ANSATZ",
        "rich_moving_root_target": 21,
        "three_sparse_source_coordinates": 3,
        "t": 2,
        "minimum_R": 22,
        "maximum_carrier_excess_formula": "k-3",
        "minimum_k_for_excess_11": 14,
        "minimum_n_for_excess_11": 36,
    }, "minimality route cut drift")
    first_match = value["first_match"]
    require(first_match["conclusion"]
            == "DEEP_OR_AT_OR_BEFORE_LOW_CARRIER",
            "first-match conclusion strengthened or weakened")
    require(first_match["full_frontier_partitioned_exactly"] is True
            and first_match["two_zero_polynomial_slopes_owned_by_extended_deep"] is True,
            "first-match deep partition drift")
    require(first_match["owner_is_existential_over_complete_selectors"] is True,
            "complete-selector owner quantifier drift")
    require(first_match["local_rank9_families_are_not_complete_selectors"] is True,
            "selected/complete quantifier drift")
    guards = value["scope_guards"]
    require(guards == {
        "toy_scale_only": True,
        "deployed_field_instantiated": False,
        "deployed_complete_selector_inventory": False,
        "koalabear_rank9_closed": False,
        "ledger_movement": 0,
        "U_Q_determined": False,
        "U_A_determined": False,
        "lean_authorized": False,
    }, "scope guard drift")
    require(value["nonclaims"] == NONCLAIMS, "nonclaim list drift")


def run_check() -> None:
    value = load_json(CERT_PATH)
    verify_semantics(value)
    print("M1 rank-nine t=2 source-compatible control: PASS")
    print("  n=35: full 841 = 2 deep + 839 post-deep; lex kappa=7")
    print("  n=36: full 289 = 2 deep + 287 post-deep; lex kappa=5")
    print("  conclusion: DEEP_OR_AT_OR_BEFORE_LOW_CARRIER; ledger unchanged")


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-mutated")),
        ("kind", lambda d: d.__setitem__("artifact_kind", "PROMOTED_THEOREM")),
        ("status", lambda d: d.__setitem__("status", "DEPLOYED_GREEN")),
        ("sage-payload", lambda d: d["sage_replay"].__setitem__("payload_sha256", "0" * 64)),
        ("sage-status", lambda d: d["sage_replay"].__setitem__("status", "SKIPPED")),
        ("n35-p", lambda d: d["n35"]["field"].__setitem__("characteristic", 31)),
        ("n35-modulus", lambda d: d["n35"]["field"]["modulus_coefficients_ascending"].__setitem__(1, 23)),
        ("n35-omega", lambda d: d["n35"]["field"].__setitem__("omega_coordinates", [25, 16])),
        ("n35-row", lambda d: d["n35"]["row"].__setitem__("A", 14)),
        ("n35-t", lambda d: d["n35"]["row"].__setitem__("t", 1)),
        ("n35-core", lambda d: d["n35"]["source"]["core"].pop()),
        ("n35-alpha", lambda d: d["n35"]["source"].__setitem__("canonical_alpha_coordinates", [27, 28])),
        ("n35-compatibility", lambda d: d["n35"]["source"].__setitem__("compatibility_equation", "support-only")),
        ("n35-outlier", lambda d: d["n35"]["rank9_local_control"]["outliers"][0].__setitem__(0, 2)),
        ("n35-local-complete", lambda d: d["n35"]["rank9_local_control"].__setitem__("complete_selector", True)),
        ("n35-affine-rank", lambda d: d["n35"]["rank9_local_control"].__setitem__("affine_rank", 8)),
        ("n35-hankel", lambda d: d["n35"]["rank9_local_control"].__setitem__("hankel_rank", 1)),
        ("n35-frobenius", lambda d: d["n35"]["rank9_local_control"].__setitem__("source_syndrome_frobenius_rank", 3)),
        ("n35-full-q", lambda d: d["n35"]["full_finite_frontier"].__setitem__("finite_slope_count", 839)),
        ("n35-deep-count", lambda d: d["n35"]["full_finite_frontier"].__setitem__("deep_exception_count", 0)),
        ("n35-special-slope", lambda d: d["n35"]["deep_exceptions"]["exceptions"][1].__setitem__("slope_coordinates", [11, 15])),
        ("n35-special-exact-A", lambda d: d["n35"]["deep_exceptions"]["exceptions"][0]["exact_A_witness_support"].pop()),
        ("n35-special-actual-support", lambda d: d["n35"]["deep_exceptions"]["exceptions"][1].__setitem__("actual_error_support", [0, 2])),
        ("n35-special-weight", lambda d: d["n35"]["deep_exceptions"]["exceptions"][0].__setitem__("actual_error_weight", 3)),
        ("n35-special-hankel", lambda d: d["n35"]["deep_exceptions"]["exceptions"][0].__setitem__("hankel_rank", 1)),
        ("n35-deep-owner", lambda d: d["n35"]["deep_exceptions"].__setitem__("owner_id", "UNPAID")),
        ("n35-deep-threshold", lambda d: d["n35"]["deep_exceptions"].__setitem__("deep_threshold", 6)),
        ("n35-zero-contained", lambda d: d["n35"]["deep_exceptions"].__setitem__("zero_word_contained_for_every_nonspecial_slope", False)),
        ("n35-uniform-NT", lambda d: d["n35"]["source"]["uniform_nonzero_locator_noncontainment"].__setitem__("proof_covers_all_inventory_representatives", False)),
        ("n35-compatible", lambda d: d["n35"]["post_deep_nonzero_locator_inventory"].__setitem__("compatible_support_count", 268_997)),
        ("n35-postdeep-slopes", lambda d: d["n35"]["post_deep_nonzero_locator_inventory"].__setitem__("slope_count", 840)),
        ("n35-inventory-hash", lambda d: d["n35"]["post_deep_nonzero_locator_inventory"].__setitem__("inventory_sha256", "1" * 64)),
        ("n35-common-roots", lambda d: d["n35"]["post_deep_nonzero_locator_inventory"]["lex_selector_common_roots"].pop()),
        ("n35-excess", lambda d: d["n35"]["post_deep_nonzero_locator_inventory"].__setitem__("lex_selector_carrier_excess", 8)),
        ("n35-structural", lambda d: d["n35"]["post_deep_low_carrier_exit"].__setitem__("ansatz_structural_maximum_excess", 11)),
        ("n36-p", lambda d: d["n36"]["field"].__setitem__("characteristic", 19)),
        ("n36-row", lambda d: d["n36"]["row"].__setitem__("k", 13)),
        ("n36-beta", lambda d: d["n36"]["source"].__setitem__("canonical_beta_coordinates", [6, 14])),
        ("n36-outlier", lambda d: d["n36"]["rank9_local_control"]["outliers"][7].pop()),
        ("n36-local-excess", lambda d: d["n36"]["rank9_local_control"].__setitem__("carrier_excess", 10)),
        ("n36-full-q", lambda d: d["n36"]["full_finite_frontier"].__setitem__("finite_slope_count", 287)),
        ("n36-special-rank", lambda d: d["n36"]["deep_exceptions"]["exceptions"][1].__setitem__("augmented_epsilon1_rank", 14)),
        ("n36-MDS-lower", lambda d: d["n36"]["deep_exceptions"].__setitem__("nonzero_codeword_error_lower_bound", 7)),
        ("n36-fixed-root", lambda d: d["n36"]["post_deep_nonzero_locator_inventory"].__setitem__("fixed_root", None)),
        ("n36-compatible", lambda d: d["n36"]["post_deep_nonzero_locator_inventory"].__setitem__("compatible_support_count", 780_908)),
        ("n36-postdeep-slopes", lambda d: d["n36"]["post_deep_nonzero_locator_inventory"].__setitem__("slope_count", 288)),
        ("n36-count-min", lambda d: d["n36"]["post_deep_nonzero_locator_inventory"].__setitem__("witness_count_min", 2_570)),
        ("n36-inventory-hash", lambda d: d["n36"]["post_deep_nonzero_locator_inventory"].__setitem__("inventory_sha256", "2" * 64)),
        ("n36-complete-excess", lambda d: d["n36"]["post_deep_nonzero_locator_inventory"].__setitem__("lex_selector_carrier_excess", 11)),
        ("n36-cap", lambda d: d["n36"]["post_deep_low_carrier_exit"].__setitem__("lex_selector_cap", 286)),
        ("minimum-R", lambda d: d["minimality"].__setitem__("minimum_R", 21)),
        ("minimum-k", lambda d: d["minimality"].__setitem__("minimum_k_for_excess_11", 13)),
        ("first-match", lambda d: d["first_match"].__setitem__("conclusion", "AFTER_BRANCH_5")),
        ("owner-quantifier", lambda d: d["first_match"].__setitem__("owner_is_existential_over_complete_selectors", False)),
        ("selected-quantifier", lambda d: d["first_match"].__setitem__("local_rank9_families_are_not_complete_selectors", False)),
        ("deployed", lambda d: d["scope_guards"].__setitem__("deployed_field_instantiated", True)),
        ("ledger", lambda d: d["scope_guards"].__setitem__("ledger_movement", 1)),
        ("UQ", lambda d: d["scope_guards"].__setitem__("U_Q_determined", True)),
        ("lean", lambda d: d["scope_guards"].__setitem__("lean_authorized", True)),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
        ("type-bool-int", lambda d: d["n35"]["row"].__setitem__("n", True)),
        ("type-string-int", lambda d: d["n36"]["row"].__setitem__("A", "16")),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "3" * 64)),
        ("predecessor", lambda d: d["predecessor_bindings"].__setitem__("low_excess_owner_payload", "4" * 64)),
        ("deep-predecessor", lambda d: d["predecessor_bindings"].__setitem__("extended_deep_owner_payload", "6" * 64)),
        ("payload", lambda d: d.__setitem__("payload_sha256", "5" * 64)),
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
    print(f"M1 t=2 source-compatible mutations: {passed}/{expected} PASS")


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
