#!/usr/bin/env python3
"""Verify the KoalaBear rank-nine fixed-basis fibre route cut.

The checker proves the exact deployed basis-incidence compiler, validates the
sharp affine-line union threshold, and binds the explicit j=20 counterexample
replayed independently by Sage.  The counterexample refutes a generic-local
uniform cap of 20; it is not a deployed KoalaBear counterexample.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-rank9-fixed-basis-fibre-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_RANK9_FIXED_BASIS_FIBRE_ROUTE_CUT"
STATUS = "PROVED_AFFINE_LINE_REDUCTION_UNIFORM_CAP20_FALSE_AGGREGATE_GATE_OPEN"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-rank9-fixed-basis-fibre-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_rank9_fixed_basis_fibre_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-fixed-basis-fibre-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.sage"
)
MASK_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md"
)
MASK_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-rank9-mask-deficit-v1/"
    "m1_kb_branch3_rank9_mask_deficit_v1.json"
)
ACTUAL_CORE_REL = Path(
    "experimental/notes/thresholds/a6_actual_witness_core_rank_preflight.md"
)
SYNDROME_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md"
)
LOCATOR_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.md"
)
LOCATOR_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-rank9-regular-locator-span-shortcut-refuted-v1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.json"
)

N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
DELTA_ZERO = R - J
RANK_S = 9
CORE_R = 8
CUTOFF_D = 18_014
TAIL_TARGET = 17_907_572_507_584

Q_LINE = 2_130_706_433**6
DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID

CORE_BASIS_COUNT = math.comb(DELTA_ZERO + CORE_R, CORE_R)
AMBIENT_BASIS_COUNT = math.comb(N, CORE_R)
CAP_20 = 20 * AMBIENT_BASIS_COUNT // CORE_BASIS_COUNT
CAP_21 = 21 * AMBIENT_BASIS_COUNT // CORE_BASIS_COUNT
CAP_20_MARGIN = TAIL_TARGET - CAP_20
CAP_21_OVER = CAP_21 - TAIL_TARGET
M20 = (21 * J) // 20 + 1
LOW_UNION_MIN = J + 1
LOW_UNION_MAX = M20 - 1
AGGREGATE_EXCESS_MAX = (
    (TAIL_TARGET + 1) * CORE_BASIS_COUNT
    - 20 * AMBIENT_BASIS_COUNT
    - 1
)

TOY_J = 20
TOY_N = TOY_J + 14
TOY_K = 13
TOY_R = TOY_N - TOY_K
TOY_A = TOY_N - TOY_J
TOY_CARRIER = TOY_J + 12
TOY_EXCESS = TOY_CARRIER - TOY_R
TOY_PENCIL_SIZE = TOY_J + 1
TOY_SLOPES = 5 * TOY_PENCIL_SIZE

NONCLAIMS = [
    "This packet does not construct a deployed KoalaBear counterexample.",
    "This packet does not prove the aggregate fixed-basis excess bound.",
    "This packet does not exhaust the full bad-slope set in the toy family.",
    "This packet does not sum low-carrier owners over basis fibres.",
    "This packet does not call correlated agreement a paid owner.",
    "This packet does not move the KoalaBear ledger.",
    "This packet does not close rank nine, branch 3, or the KoalaBear row.",
    "This packet does not attack intrinsic rank at least ten.",
    "This packet does not determine U_Q or U_A.",
    "This packet does not authorize Lean or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """A schema, source, arithmetic, or semantic check failed."""


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


def source_binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def predecessor_payload(relative: Path) -> str:
    data = load_json(ROOT / relative)
    require(data.get("payload_sha256") == payload_hash(data), f"bad predecessor payload: {relative}")
    return str(data["payload_sha256"])


def expected_certificate() -> dict[str, Any]:
    source_bindings = [
        source_binding("packet-note", NOTE_REL, "load-bearing route-cut note"),
        source_binding("packet-readme", README_REL, "replay instructions"),
        source_binding("packet-verifier", PYTHON_REL, "exact compiler verifier"),
        source_binding("packet-sage", SAGE_REL, "independent finite-field counterexample"),
        source_binding("mask-note", MASK_NOTE_REL, "deficit-tail predecessor"),
        source_binding("actual-core-theorem", ACTUAL_CORE_REL, "MDS row-flat basis count"),
        source_binding("syndrome-note", SYNDROME_NOTE_REL, "column-far/sparse route cut"),
        source_binding("locator-note", LOCATOR_NOTE_REL, "five-pencil counterexample source"),
    ]
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": source_bindings,
        "predecessor_payloads": {
            "mask_deficit": predecessor_payload(MASK_CERT_REL),
            "locator_span_counterexample": predecessor_payload(LOCATOR_CERT_REL),
        },
        "row": {
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "Delta0": DELTA_ZERO,
            "rank_s": RANK_S,
            "core_r": CORE_R,
            "cutoff_D": CUTOFF_D,
            "tail_target": str(TAIL_TARGET),
        },
        "fixed_basis_lemma": {
            "restriction_K0_to_B": "ISOMORPHISM",
            "fibre_normal_form": "e_eta=a_B+eta*b_B",
            "syndromes": ["H*a_B=y_0", "H*b_B=y_1"],
            "basis_zeros": "a_B|_B=b_B|_B=0",
            "zero_incidence": "J_B*(M_B-j)+sum_eta(delta_eta)<=M_B",
        },
        "exact_trichotomy": {
            "common_support_max": J,
            "common_support_terminal": "CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA",
            "low_union_min": LOW_UNION_MIN,
            "low_union_max": LOW_UNION_MAX,
            "low_union_terminal": "LOW_UNION_FIXED_BASIS_AFFINE_LINE_ROUTE",
            "cap20_union_threshold": M20,
            "cap20_terminal": "FIXED_BASIS_AFFINE_LINE_CAP_20",
            "threshold_is_below_R": M20 < R,
            "threshold_left_check": 21 * (M20 - 1 - J) <= M20 - 1,
            "threshold_right_check": 21 * (M20 - J) > M20,
        },
        "deployed_compiler": {
            "core_basis_count": str(CORE_BASIS_COUNT),
            "ambient_basis_count": str(AMBIENT_BASIS_COUNT),
            "uniform_cap20_tail_bound": str(CAP_20),
            "uniform_cap20_margin": str(CAP_20_MARGIN),
            "uniform_cap21_tail_bound": str(CAP_21),
            "uniform_cap21_over_target": str(CAP_21_OVER),
            "aggregate_excess_definition": "sum_B(max(0,m_B-20))",
            "aggregate_excess_max": str(AGGREGATE_EXCESS_MAX),
            "at_excess_max_tail_bound": str(
                (20 * AMBIENT_BASIS_COUNT + AGGREGATE_EXCESS_MAX)
                // CORE_BASIS_COUNT
            ),
            "at_excess_max_plus_one_tail_bound": str(
                (20 * AMBIENT_BASIS_COUNT + AGGREGATE_EXCESS_MAX + 1)
                // CORE_BASIS_COUNT
            ),
            "aggregate_gate_status": "UNPROVEN_DEPLOYED_INCIDENCE_INPUT",
        },
        "counterexample": {
            "field": "GF(2^37)",
            "j": TOY_J,
            "n": TOY_N,
            "k": TOY_K,
            "R": TOY_R,
            "A": TOY_A,
            "carrier_size": TOY_CARRIER,
            "carrier_excess": TOY_EXCESS,
            "declared_slope_count": TOY_SLOPES,
            "rank_tuple": [9, 10, 11],
            "core_restriction_ranks": [8, 8, 8, 8, 8],
            "fixed_basis_multiplicity": TOY_PENCIL_SIZE,
            "all_deficits_zero": True,
            "complete_on_declared_Gamma": True,
            "declared_Gamma_exhausts_full_bad_set": False,
            "koalabear_domain_instantiated": False,
            "classification": "COUNTEREXAMPLE_TO_GENERIC_LOCAL_UNIFORM_FIXED_BASIS_CAP20",
        },
        "literature_audit": {
            "theoremsearch_direct_match": False,
            "srivastava_affine_ball_gate": "HIGH_DISTANCE_REGION_ALREADY_PAID_BY_EXISTING_M2B",
            "generic_higher_order_mds": "NO_FIXED_KOALABEAR_DOMAIN_CERTIFICATE",
            "point_polynomial_incidence": "STATED_REGIME_DOES_NOT_REACH_ROW",
            "load_bearing_external_import": False,
        },
        "classifier_contract": {
            "aggregate_gate_true": "PAID_BY_RANK9_FIXED_BASIS_AGGREGATE_EXCESS",
            "aggregate_gate_missing": "UNPAID_RANK9_FIXED_BASIS_AGGREGATION",
            "current_terminal": "UNPAID_RANK9_FIXED_BASIS_AGGREGATION",
        },
        "ledger": {
            "B_star": str(B_STAR),
            "U_paid_before": str(U_PAID),
            "U_paid_after": str(U_PAID),
            "B_remaining_before": str(B_REMAINING),
            "B_remaining_after": str(B_REMAINING),
            "movement": "0",
        },
        "audit": {
            "packet_verdict": "GREEN_ROUTE_CUT_AND_COUNTEREXAMPLE",
            "global_verdict": "YELLOW_RANK9_BRANCH3_AND_KOALABEAR_OPEN",
            "parameter_dependence": "EXACT_KOALABEAR_COMPILER_PLUS_FIELD_UNIFORM_LINE_LEMMA_PLUS_EXACT_GF2_37_CONTROL",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "deployed_field_census_performed": False,
        },
        "nonclaims": NONCLAIMS,
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def validate_certificate(data: dict[str, Any]) -> None:
    expected = expected_certificate()
    require(data == expected, "certificate differs from exact expected artifact")
    require(data["payload_sha256"] == payload_hash(data), "payload hash mismatch")
    require(CAP_20 <= TAIL_TARGET < CAP_21, "uniform cap boundary drift")
    require(M20 == 1_030_160, "sharp line-union threshold drift")
    require(LOW_UNION_MAX < R, "low-union interval crossed R")
    require(
        (20 * AMBIENT_BASIS_COUNT + AGGREGATE_EXCESS_MAX)
        // CORE_BASIS_COUNT
        == TAIL_TARGET,
        "aggregate maximum no longer pays target",
    )
    require(
        (20 * AMBIENT_BASIS_COUNT + AGGREGATE_EXCESS_MAX + 1)
        // CORE_BASIS_COUNT
        == TAIL_TARGET + 1,
        "aggregate maximum is not integer-sharp",
    )
    require(TOY_PENCIL_SIZE == 21 > 20, "toy no longer refutes cap 20")
    require(TOY_EXCESS == 11, "toy carrier excess drift")


def rehash(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


Mutation = tuple[str, Callable[[dict[str, Any]], None], bool]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-bad"), True),
        ("status", lambda d: d.__setitem__("status", "PROVED_CLOSED"), True),
        ("row-j", lambda d: d["row"].__setitem__("j", J + 1), True),
        ("tail-target", lambda d: d["row"].__setitem__("tail_target", str(TAIL_TARGET + 1)), True),
        ("line-form", lambda d: d["fixed_basis_lemma"].__setitem__("fibre_normal_form", "arbitrary"), True),
        ("common-owner", lambda d: d["exact_trichotomy"].__setitem__("common_support_terminal", "PAID"), True),
        ("low-min", lambda d: d["exact_trichotomy"].__setitem__("low_union_min", LOW_UNION_MIN - 1), True),
        ("low-max", lambda d: d["exact_trichotomy"].__setitem__("low_union_max", LOW_UNION_MAX + 1), True),
        ("threshold", lambda d: d["exact_trichotomy"].__setitem__("cap20_union_threshold", M20 - 1), True),
        ("threshold-left", lambda d: d["exact_trichotomy"].__setitem__("threshold_left_check", False), True),
        ("basis-count", lambda d: d["deployed_compiler"].__setitem__("core_basis_count", str(CORE_BASIS_COUNT + 1)), True),
        ("ambient-count", lambda d: d["deployed_compiler"].__setitem__("ambient_basis_count", str(AMBIENT_BASIS_COUNT - 1)), True),
        ("cap20", lambda d: d["deployed_compiler"].__setitem__("uniform_cap20_tail_bound", str(CAP_20 + 1)), True),
        ("cap21", lambda d: d["deployed_compiler"].__setitem__("uniform_cap21_tail_bound", str(CAP_21 - 1)), True),
        ("excess", lambda d: d["deployed_compiler"].__setitem__("aggregate_excess_max", str(AGGREGATE_EXCESS_MAX + 1)), True),
        ("aggregate-paid", lambda d: d["deployed_compiler"].__setitem__("aggregate_gate_status", "PROVED"), True),
        ("toy-field", lambda d: d["counterexample"].__setitem__("field", "GF(2^23)"), True),
        ("toy-j", lambda d: d["counterexample"].__setitem__("j", 19), True),
        ("toy-ranks", lambda d: d["counterexample"].__setitem__("rank_tuple", [8, 9, 11]), True),
        ("core-rank", lambda d: d["counterexample"].__setitem__("core_restriction_ranks", [8, 8, 8, 8, 7]), True),
        ("multiplicity", lambda d: d["counterexample"].__setitem__("fixed_basis_multiplicity", 20), True),
        ("full-exhaustion", lambda d: d["counterexample"].__setitem__("declared_Gamma_exhausts_full_bad_set", True), True),
        ("koalabear", lambda d: d["counterexample"].__setitem__("koalabear_domain_instantiated", True), True),
        ("literature-import", lambda d: d["literature_audit"].__setitem__("load_bearing_external_import", True), True),
        ("current-paid", lambda d: d["classifier_contract"].__setitem__("current_terminal", "PAID"), True),
        ("ledger", lambda d: d["ledger"].__setitem__("movement", "1"), True),
        ("verdict", lambda d: d["audit"].__setitem__("global_verdict", "GREEN_CLOSED"), True),
        ("nonclaim", lambda d: d["nonclaims"].pop(), True),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64), True),
        ("predecessor-hash", lambda d: d["predecessor_payloads"].__setitem__("mask_deficit", "0" * 64), True),
        ("type-bool-for-int", lambda d: d["row"].__setitem__("n", True), True),
        ("payload", lambda d: d.__setitem__("payload_sha256", "0" * 64), False),
    ]


def run_tamper_selftest() -> int:
    base = expected_certificate()
    passed = 0
    for name, mutate, should_rehash in mutation_cases():
        candidate = copy.deepcopy(base)
        mutate(candidate)
        if should_rehash:
            rehash(candidate)
        try:
            validate_certificate(candidate)
        except (VerificationError, KeyError, TypeError, ValueError):
            passed += 1
        else:
            raise VerificationError(f"mutation escaped validation: {name}")

    parser_cases = {
        "duplicate": '{"schema":"a","schema":"b"}',
        "nan": '{"x":NaN}',
        "infinity": '{"x":Infinity}',
        "float": '{"x":1.0}',
        "overflow-float": '{"x":1e9999}',
    }
    for name, text in parser_cases.items():
        try:
            parse_json(text, name)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"parser mutation escaped: {name}")

    print(f"tamper_selftest=PASS ({passed}/{passed})")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--tamper-selftest", action="store_true")
    action.add_argument("--print-template", action="store_true")
    args = parser.parse_args()

    if args.print_template:
        print(json.dumps(expected_certificate(), indent=2, sort_keys=True))
        return
    if args.tamper_selftest:
        run_tamper_selftest()
        return

    data = load_json(CERT_PATH)
    validate_certificate(data)
    print(f"schema={SCHEMA}")
    print(f"cap20_tail={CAP_20}")
    print(f"cap21_tail={CAP_21}")
    print(f"sharp_union_threshold={M20}")
    print(f"aggregate_excess_max={AGGREGATE_EXCESS_MAX}")
    print(f"toy_fixed_basis_multiplicity={TOY_PENCIL_SIZE}")
    print("classification=PROVED_ROUTE_CUT_NO_LEDGER_MOVEMENT")
    print("check=PASS")


if __name__ == "__main__":
    main()
