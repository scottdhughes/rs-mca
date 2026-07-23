#!/usr/bin/env python3
"""Verify the M31 rank-six generalized-weight/codimension-one closure.

The packet is a finite, source-bound consequence for the reconstructed
base-field boundary shallow family.  It refines the inherited marked-line
count with the actual generalized Hamming weights of a hypothetical
six-dimensional codeword span, then feeds a minimum-support hyperplane into
the proved coset-free codimension-one compiler.

The result excludes rank six.  It does not prove the complete M31 LIST row,
does not pay a Grande Finale v4 atom, and leaves every rank at least seven
open.  All deployed arithmetic is exact integer or rational arithmetic.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
DEEP_CAP = 1_001_282
SHALLOW_SIZE = B_STAR - DEEP_CAP
SHALLOW_TARGET = SHALLOW_SIZE - 1
S_MAX = 366_886
RANK = 6
LINE_MULTIPLICITY = (N - K + 1) // (W + 1)
G_MIN = 781_458
G_MAX = 1_033_227

SCHEMA_ID = "m31-rank6-generalized-weight-codim1-closure-summary-v1"
THEOREM_ID = "M31_RANK6_GENERALIZED_WEIGHT_CODIM_ONE_CLOSURE_V1"
ARCHITECTURE_ID = (
    "M31_BASE_FIELD_BOUNDARY_RANK6_WEIGHT_HIERARCHY_CODIM_ONE_COMPILER_V1"
)
ARTIFACT_KIND = (
    "EXACT_GENERALIZED_WEIGHT_MARKED_LINE_AND_CODIMENSION_ONE_RANK6_CLOSURE"
)
STATUS = "PROVED_BASE_FIELD_BOUNDARY_SHALLOW_RANK6_EXCLUDED_RANK_GE7_OPEN"
TERMINAL = "UNPAID_RANK_GE7_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE"
PARENT_PAYLOAD = (
    "28f18608d3552ffe42e6dc8fcb6c03c1338fd349e1d52a0a3f52de6629bcbf6b"
)

ROOT = Path(__file__).resolve().parents[2]
PRIMARY_PATH = Path(__file__).resolve()
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_rank6_generalized_weight_codim1_closure_v1.schema.json"
)
SAGE_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank6_generalized_weight_codim1_closure_v1.sage"
)
PACKET_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank6_generalized_weight_codim1_closure_packet_v1.py"
)
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank6_generalized_weight_codim_one_closure_v1.md"
)
README_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank6-generalized-weight-codim1-closure-v1/README.md"
)
DEFAULT_MANIFEST = ROOT / (
    "experimental/data/certificates/"
    "m31-rank6-generalized-weight-codim1-closure-v1/manifest.json"
)
PARENT_MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-varying-g-first-pivot-basis-route-cut-v1/manifest.json"
)
PARENT_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_varying_g_first_pivot_basis_route_cut_v1.md"
)
PARENT_PACKET_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_varying_g_first_pivot_basis_route_cut_packet_v1.py"
)
GRANDE_FINALE_PATH = ROOT / "experimental/grande_finale.tex"


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            indent=2 if pretty else None,
            separators=None if pretty else (",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON encoding") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_sha256(result)
    return result


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"JSON exists: {path}")
    try:
        value = json.loads(path.read_text(encoding="ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"valid ASCII JSON: {path}") from exc
    require(type(value) is dict, f"JSON object: {path}")
    return value


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def falling(value: int, length: int) -> int:
    require(length >= 0, "falling length nonnegative")
    require(value >= length, "falling argument large enough")
    result = 1
    for offset in range(length):
        result *= value - offset
    return result


def fraction_record(value: Fraction) -> dict[str, int]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "floor": value.numerator // value.denominator,
    }


def q5_capacity(union_size: int) -> int:
    require(G_MIN <= union_size <= G_MAX, "rank-six union in inherited window")
    numerator = LINE_MULTIPLICITY * falling(R + union_size, 5)
    fixed_denominator = (
        SHALLOW_SIZE
        * union_size
        * (W + 2)
        * (W + 3)
        * (W + 4)
    )
    return numerator // fixed_denominator - (W + 5)


def generalized_weight_window() -> dict[str, Any]:
    capacities = [q5_capacity(union_size) for union_size in range(G_MIN, G_MAX + 1)]
    require(capacities == sorted(capacities), "q5 capacities monotone on full g window")
    maximum = capacities[-1]
    require(maximum == 32_004, "q5 ceiling")

    fixed_denominator = (
        SHALLOW_SIZE * G_MAX * (W + 2) * (W + 3) * (W + 4)
    )
    rhs = LINE_MULTIPLICITY * falling(R + G_MAX, 5)
    cap_slack = rhs - fixed_denominator * (W + 5 + maximum)
    next_slack = rhs - fixed_denominator * (W + 5 + maximum + 1)
    require(
        cap_slack == 2_961_522_295_037_039_379_410_352_000,
        "q5 cap exact slack",
    )
    require(
        next_slack == -2_040_396_785_852_186_139_127_420_050,
        "q5 successor exact slack",
    )

    d5_min = N - K + 5
    d5_max = d5_min + maximum
    require((d5_min, d5_max) == (1_048_581, 1_080_585), "d5 range")
    return {
        "q_definitions": "q_j=d_j-(n-K+j)",
        "q_monotonicity": "0<=q_1<=q_2<=q_3<=q_4<=q_5",
        "marked_line_inequality": (
            "sum_i (g+s_i)*prod_{j=2}^5(d_j-R+eta+s_i) "
            "<= 15*(d_6)_5"
        ),
        "weakened_q5_gate": (
            "L*g*(w+2)*(w+3)*(w+4)*(w+5+q_5) <= 15*(R+g)_5"
        ),
        "g_ratio_monotonicity_gate": "4*(g+1)>=R",
        "union_values_exhausted": G_MAX - G_MIN + 1,
        "maximizing_union": G_MAX,
        "q5_ceiling": maximum,
        "q5_cap_slack": cap_slack,
        "q5_successor_slack": next_slack,
        "d5_range": [d5_min, d5_max],
    }


def pi_profile(d5: int, common_mismatch: int, layer_mismatch: int) -> int:
    require(d5 >= N - K + 5, "legal d5")
    require(common_mismatch >= 0, "nonnegative common mismatch")
    require(layer_mismatch >= 0, "nonnegative layer mismatch")
    return (d5 - R + common_mismatch + layer_mismatch) * _product(
        W + index + common_mismatch + layer_mismatch for index in range(1, 5)
    )


def _product(values: Any) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def old_support_term(d5: int, common_mismatch: int = 0) -> Fraction:
    return Fraction(falling(d5, 5), pi_profile(d5, common_mismatch, 0))


def new_layer_term(d5: int, union_size: int, common_mismatch: int = 0) -> Fraction:
    d6 = R + union_size - common_mismatch
    layer = d6 - d5
    require(layer >= 1, "strict generalized-weight support layer")
    q_value = W + 1 + common_mismatch
    return Fraction(
        falling(d5, 6),
        q_value * pi_profile(d5, common_mismatch, layer),
    )


def codimension_one_envelope(weight_window: dict[str, Any]) -> dict[str, Any]:
    d5_min, d5_max = weight_window["d5_range"]

    interpolation_margin = 4 * (W + 1) - (d5_max - R)
    require(interpolation_margin == 170_336, "profile interpolation margin")

    old_values = [old_support_term(d5) for d5 in range(d5_min, d5_max + 1)]
    require(
        all(left >= right for left, right in zip(old_values, old_values[1:])),
        "old-support term decreases over every d5",
    )
    old_maximum = old_values[0]

    new_d_values = [new_layer_term(d5, G_MIN) for d5 in range(d5_min, d5_max + 1)]
    require(
        all(left <= right for left, right in zip(new_d_values, new_d_values[1:])),
        "new-layer term increases over every d5",
    )
    new_g_values = [new_layer_term(d5_max, union_size) for union_size in range(G_MIN, G_MAX + 1)]
    require(
        all(left >= right for left, right in zip(new_g_values, new_g_values[1:])),
        "new-layer term decreases over every g",
    )
    new_maximum = new_d_values[-1]

    require(
        old_maximum
        == Fraction(13_595_760_770_200_795_755_215_673, 14_972_954_495_361_184_520),
        "old-support exact fraction",
    )
    require(
        new_maximum
        == Fraction(
            10_050_609_557_311_530_989_539_114_985_523,
            104_976_882_945_190_479_108_637_352_042,
        ),
        "new-layer exact fraction",
    )
    mixed = old_maximum + new_maximum
    require(
        mixed
        == Fraction(
            84_651_350_625_295_573_259_786_319_574_408_928_533_881_774_479_223,
            93_216_349_863_788_082_545_281_107_999_500_921_518_287_320,
        ),
        "mixed exact fraction",
    )
    whole_chart_upper = mixed.numerator // mixed.denominator
    require(whole_chart_upper == 908_116, "whole-chart floor")
    require(whole_chart_upper < SHALLOW_SIZE, "rank-six contradiction")

    return {
        "chosen_hyperplane": "a d_5-minimizing 5-dimensional subcode V<W_c",
        "support_saturated": True,
        "compiler_source": "Grande Finale Corollary codim-one-mds-soft",
        "parameter_map": {
            "j": 5,
            "d": "d_5(W_c)",
            "full_support": "d_6(W_c)=R+g-eta",
            "support_layer": "Delta=d_6-d_5",
            "outside_common_mismatch": "b_0=eta",
            "Q": "w+1+eta",
            "Pi_b": "(d_5-R+eta+b)*prod_{i=1}^4(w+i+eta+b)",
        },
        "profile_interpolation": {
            "largest_initial_factor": "A_profile=d_5-R+eta",
            "criterion": "4*Q-A_profile>=0",
            "uniform_margin": interpolation_margin,
        },
        "monotonicity": {
            "old_support_term": "decreases in d_5 and eta",
            "new_layer_term": (
                "increases in d_5; decreases in g and eta; Pi_Delta is eta-independent"
            ),
            "d5_values_exhausted": d5_max - d5_min + 1,
            "g_values_exhausted": G_MAX - G_MIN + 1,
        },
        "old_support_maximum": fraction_record(old_maximum),
        "new_layer_maximum": fraction_record(new_maximum),
        "mixed_majorant": fraction_record(mixed),
        "whole_chart_upper": whole_chart_upper,
        "contradiction_gap": SHALLOW_SIZE - whole_chart_upper,
    }


def source_bindings() -> list[dict[str, Any]]:
    specifications = (
        (
            "packet_schema",
            SCHEMA_PATH,
            None,
            "Closed top-level schema for the rank-six closure packet.",
        ),
        (
            "primary_exact_replay",
            PRIMARY_PATH,
            None,
            "Standard-library generalized-weight and codimension-one arithmetic.",
        ),
        (
            "independent_sage_replay",
            SAGE_PATH,
            None,
            "Independent exact arithmetic and exhaustive GF(7) source control.",
        ),
        (
            "packet_verifier",
            PACKET_PATH,
            None,
            "Fail-closed source, replay, schema, dependency, and mutation verifier.",
        ),
        (
            "theorem_note",
            NOTE_PATH,
            None,
            "Proof of the generalized marked-line refinement and compiler splice.",
        ),
        (
            "packet_readme",
            README_PATH,
            None,
            "Replay and scope instructions.",
        ),
        (
            "parent_manifest",
            PARENT_MANIFEST_PATH,
            PARENT_PAYLOAD,
            "Sealed #1065 marked-basis rank-six window and shallow-family source.",
        ),
        (
            "parent_note",
            PARENT_NOTE_PATH,
            None,
            "Parent definitions, actual-codeword unit, and affine-line multiplicity.",
        ),
        (
            "parent_packet_verifier",
            PARENT_PACKET_PATH,
            None,
            "Fail-closed replay of the immediate predecessor.",
        ),
        (
            "codimension_one_theorem_source",
            GRANDE_FINALE_PATH,
            None,
            "Two-resource recursion, profile interpolation, and MDS-soft compiler.",
        ),
    )
    return [
        {
            "binding_id": f"M31_RANK6_CLOSURE::{role}",
            "role": role,
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal_payload,
            "scope": scope,
        }
        for role, path, internal_payload, scope in specifications
    ]


def build_payload() -> dict[str, Any]:
    require(P == 2_147_483_647, "M31 prime")
    require(N == 2 * K, "deployed half-rate identity")
    require(N == A + R, "domain partition")
    require(W == A - K, "agreement surplus")
    require(R + W == N - K == K, "deployed R+w identity")
    require(B_STAR == 16_777_215, "row budget")
    require(SHALLOW_SIZE == 15_775_933, "shallow family size")
    require(SHALLOW_TARGET == 15_775_932, "shallow target")
    require(LINE_MULTIPLICITY == 15, "affine-line multiplicity")

    parent = load_json(PARENT_MANIFEST_PATH)
    require(parent.get("payload_sha256") == PARENT_PAYLOAD, "parent payload pin")
    require(
        parent.get("rank_consequences", {}).get("rank6_surviving_union_interval")
        == [G_MIN, G_MAX],
        "parent rank-six interval",
    )
    require(
        parent.get("deployed_parameters", {}).get("shallow_size") == SHALLOW_SIZE,
        "parent shallow source size",
    )

    weight_window = generalized_weight_window()
    compiler = codimension_one_envelope(weight_window)

    payload: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "terminal": TERMINAL,
        "row_contract": {
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "agreement": A,
            "budget": B_STAR,
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "quantifier": (
                "EVERY_RECONSTRUCTED_BASE_FIELD_BOUNDARY_SHALLOW_SUBFAMILY"
            ),
        },
        "deployed_parameters": {
            "p": P,
            "n": N,
            "K": K,
            "a": A,
            "R": R,
            "w": W,
            "B_star": B_STAR,
            "deep_cap": DEEP_CAP,
            "shallow_size": SHALLOW_SIZE,
            "shallow_target": SHALLOW_TARGET,
            "shallow_excess_range": [0, S_MAX],
            "rank6_parent_union_interval": [G_MIN, G_MAX],
            "affine_line_multiplicity": LINE_MULTIPLICITY,
        },
        "imported_rank6_source": {
            "parent_payload_sha256": PARENT_PAYLOAD,
            "family_cardinality": SHALLOW_SIZE,
            "family_unit": "ACTUAL_DISTINCT_BASE_FIELD_CODEWORDS",
            "rank": RANK,
            "union_interval": [G_MIN, G_MAX],
            "common_zero_identity": "z=a-g+eta",
            "full_support_identity": "d_6(W_c)=n-z=R+g-eta",
            "fixed_received_word": True,
        },
        "generalized_weight_refinement": weight_window,
        "codimension_one_compiler": compiler,
        "rank_consequence": {
            "rank_1_through_5_excluded_by_parent": True,
            "rank_6_excluded_by_this_packet": True,
            "rank_1_through_6_excluded": True,
            "minimum_surviving_rank": 7,
            "shallow_family_required": SHALLOW_SIZE,
            "whole_rank6_chart_upper": compiler["whole_chart_upper"],
            "contradiction_gap": compiler["contradiction_gap"],
        },
        "toy_controls": {
            "scope": "EXACT_GF7_CONTROL_ONLY",
            "field": 7,
            "n": 7,
            "K": 6,
            "agreement": 6,
            "whole_list_size": 7,
            "affine_span_rank": 6,
            "d5": 6,
            "d6": 7,
            "support_layer": 1,
            "compiler_old_resource": 6,
            "compiler_new_resource": 1,
            "compiler_bound": 7,
            "marked_line_left": 4_320,
            "marked_line_right": 5_040,
            "deployed_evidence": False,
        },
        "dependency_contract": {
            "stacked_on_parent": True,
            "parent_payload_sha256": PARENT_PAYLOAD,
            "imports_proved_codimension_one_compiler": True,
            "reviewer_not_generator_required": True,
        },
        "ledger_state": {
            "movement_from_this_packet": 0,
            "official_endpoint_or_score_movement": 0,
            "row_closed": False,
            "rank6_route_closed": True,
            "route_cut_not_v4_payment": True,
        },
        "nonclaims": {
            "complete_M31_list_bound_proved": False,
            "rank7_or_higher_paid": False,
            "fixed_syndrome_incidence_theorem_proved": False,
            "toy_control_is_deployed_evidence": False,
            "v4_atom_paid": False,
            "stable_paper_modified": False,
        },
        "source_bindings": source_bindings(),
    }
    return seal(payload)


def validate_schema_top_level(payload: dict[str, Any]) -> None:
    schema = load_json(SCHEMA_PATH)
    require(schema.get("additionalProperties") is False, "closed schema")
    properties = schema.get("properties")
    required = schema.get("required")
    require(type(properties) is dict and type(required) is list, "schema shape")
    require(set(payload) == set(properties) == set(required), "schema exact keys")
    for key, specification in properties.items():
        if isinstance(specification, dict) and "const" in specification:
            require(payload[key] == specification["const"], f"schema const {key}")


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")
    expected = build_payload()
    deep_exact(payload, expected)

    require(
        payload["generalized_weight_refinement"]["q5_ceiling"] == 32_004,
        "q5 semantic pin",
    )
    require(
        payload["generalized_weight_refinement"]["d5_range"]
        == [1_048_581, 1_080_585],
        "d5 semantic pin",
    )
    require(
        payload["codimension_one_compiler"]["whole_chart_upper"] == 908_116,
        "whole-chart semantic pin",
    )
    require(
        payload["rank_consequence"]["rank_6_excluded_by_this_packet"] is True,
        "rank-six closure semantic pin",
    )
    require(payload["ledger_state"]["row_closed"] is False, "row remains open")
    require(
        payload["ledger_state"]["movement_from_this_packet"] == 0,
        "zero ledger movement",
    )

    bindings = payload.get("source_bindings")
    require(type(bindings) is list and len(bindings) == 10, "source binding count")
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for binding in bindings:
        require(type(binding) is dict, "source binding object")
        require(
            set(binding)
            == {
                "binding_id",
                "role",
                "path",
                "sha256",
                "internal_payload_sha256",
                "scope",
            },
            "source binding keys",
        )
        binding_id = binding["binding_id"]
        path_text = binding["path"]
        require(type(binding_id) is str and binding_id not in seen_ids, "unique binding id")
        require(type(path_text) is str and not path_text.startswith("/"), "relative source path")
        require(".." not in Path(path_text).parts, "no source traversal")
        require(path_text not in seen_paths, "unique source path")
        seen_ids.add(binding_id)
        seen_paths.add(path_text)
        path = ROOT / path_text
        require(path.is_file(), f"bound source exists: {path_text}")
        require(sha256_path(path) == binding["sha256"], f"fresh source hash: {path_text}")
        if binding["role"] == "parent_manifest":
            parent = load_json(path)
            require(
                binding["internal_payload_sha256"] == parent.get("payload_sha256") == PARENT_PAYLOAD,
                "parent internal payload pin",
            )
        else:
            require(binding["internal_payload_sha256"] is None, "nonmanifest internal pin null")


def tamper_selftest(payload: dict[str, Any]) -> dict[str, Any]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("status", lambda value: value.__setitem__("status", "SAFE")),
        ("terminal", lambda value: value.__setitem__("terminal", "PAID")),
        (
            "q5-ceiling",
            lambda value: value["generalized_weight_refinement"].__setitem__("q5_ceiling", 32_005),
        ),
        (
            "q5-slack",
            lambda value: value["generalized_weight_refinement"].__setitem__("q5_cap_slack", 1),
        ),
        (
            "d5-high",
            lambda value: value["generalized_weight_refinement"]["d5_range"].__setitem__(1, 1_080_586),
        ),
        (
            "marked-line",
            lambda value: value["generalized_weight_refinement"].__setitem__(
                "marked_line_inequality", "false"
            ),
        ),
        (
            "support-saturation",
            lambda value: value["codimension_one_compiler"].__setitem__("support_saturated", False),
        ),
        (
            "parameter-map",
            lambda value: value["codimension_one_compiler"]["parameter_map"].__setitem__(
                "outside_common_mismatch", "b_0=0"
            ),
        ),
        (
            "interpolation-margin",
            lambda value: value["codimension_one_compiler"]["profile_interpolation"].__setitem__(
                "uniform_margin", 170_335
            ),
        ),
        (
            "old-resource",
            lambda value: value["codimension_one_compiler"]["old_support_maximum"].__setitem__(
                "floor", 908_020
            ),
        ),
        (
            "new-resource",
            lambda value: value["codimension_one_compiler"]["new_layer_maximum"].__setitem__(
                "floor", 96
            ),
        ),
        (
            "whole-chart",
            lambda value: value["codimension_one_compiler"].__setitem__("whole_chart_upper", 908_117),
        ),
        (
            "rank6-open",
            lambda value: value["rank_consequence"].__setitem__(
                "rank_6_excluded_by_this_packet", False
            ),
        ),
        (
            "rank7-paid",
            lambda value: value["nonclaims"].__setitem__("rank7_or_higher_paid", True),
        ),
        (
            "toy-promoted",
            lambda value: value["toy_controls"].__setitem__("deployed_evidence", True),
        ),
        (
            "ledger",
            lambda value: value["ledger_state"].__setitem__("movement_from_this_packet", 1),
        ),
        (
            "row-closed",
            lambda value: value["ledger_state"].__setitem__("row_closed", True),
        ),
        (
            "parent-payload",
            lambda value: value["dependency_contract"].__setitem__(
                "parent_payload_sha256", "0" * 64
            ),
        ),
        (
            "source-traversal",
            lambda value: value["source_bindings"][0].__setitem__("path", "../escape"),
        ),
        (
            "source-hash",
            lambda value: value["source_bindings"][0].__setitem__("sha256", "0" * 64),
        ),
        (
            "source-alias",
            lambda value: value["source_bindings"][1].__setitem__(
                "path", value["source_bindings"][0]["path"]
            ),
        ),
        ("seal", lambda value: value.__setitem__("payload_sha256", "0" * 64)),
    ]
    detected: list[str] = []
    for name, mutate in mutations:
        changed = copy.deepcopy(payload)
        mutate(changed)
        if name != "seal":
            changed = seal(changed)
        try:
            validate_payload(changed)
        except (VerificationError, KeyError, TypeError, IndexError):
            detected.append(name)
    require(len(detected) == len(mutations), "all mutations detected")
    return {"count": len(mutations), "detected": detected}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    payload = build_payload()
    validate_payload(payload)
    validate_schema_top_level(payload)

    if args.tamper_selftest:
        result = tamper_selftest(payload)
        result["status"] = STATUS
        print(canonical_json(result, pretty=True).decode("ascii"), end="")
        return

    if args.write_manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_bytes(canonical_json(payload))

    if args.check:
        committed = load_json(args.manifest)
        deep_exact(committed, payload)
        require(args.manifest.read_bytes() == canonical_json(committed), "manifest canonical bytes")

    print(canonical_json(payload).decode("ascii"), end="")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
