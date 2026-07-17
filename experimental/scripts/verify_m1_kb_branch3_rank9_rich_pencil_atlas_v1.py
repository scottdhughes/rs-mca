#!/usr/bin/env python3
"""Verify the KoalaBear rank-nine rich-pencil aggregate route cut.

The checker binds the canonical graph-line atlas identity, exact deployed
aggregate arithmetic, the hostile x=1, J=109 scalar relaxation, source-bound
first-match guards, and the exact five-pencil Sage control.  It proves a route
cut, not the deployed rich-pencil incidence bound.
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

SCHEMA = "rs-mca-m1-kb-branch3-rank9-rich-pencil-atlas-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_RANK9_RICH_PENCIL_AGGREGATE_ROUTE_CUT"
STATUS = "PROVED_CANONICAL_ATLAS_AND_SCALAR_ROUTE_CUT_DEPLOYED_INCIDENCE_OPEN"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-rank9-rich-pencil-atlas-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_rank9_rich_pencil_atlas_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-rich-pencil-atlas-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.sage"
)
FIXED_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md"
)
FIXED_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-fixed-basis-fibre-v1/"
    "m1_kb_branch3_rank9_fixed_basis_fibre_v1.json"
)
CONTRACT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_5_mask_contract_v1.md"
)
CONTRACT_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-5-mask-contract-v1/"
    "m1_kb_branch3_5_mask_contract_v1.json"
)
SPARSE_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"
)
ACTUAL_CORE_REL = Path(
    "experimental/notes/thresholds/"
    "a6_actual_witness_core_rank_preflight.md"
)
LOCATOR_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.md"
)
PREDECESSOR_SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.sage"
)

N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
T = R - J
CUTOFF_D = 18_014
TAIL_TARGET = 17_907_572_507_584
CORE_R = 8
UNIFORM_CAP = 20

Q_LINE = 2_130_706_433**6
DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID

CORE_BASIS_COUNT = math.comb(T + CORE_R, CORE_R)
AMBIENT_BASIS_COUNT = math.comb(N, CORE_R)
AGGREGATE_EXCESS_MAX = (
    (TAIL_TARGET + 1) * CORE_BASIS_COUNT
    - UNIFORM_CAP * AMBIENT_BASIS_COUNT
    - 1
)
REGULAR_AGGREGATE_EXCESS_MAX = (
    (TAIL_TARGET - R + 1) * CORE_BASIS_COUNT
    - UNIFORM_CAP * AMBIENT_BASIS_COUNT
    - 1
)

RICH_X_MIN = 1 - CUTOFF_D
RICH_X_MAX = J // UNIFORM_CAP

HOSTILE_X = 1
HOSTILE_M = J + HOSTILE_X
HOSTILE_J = 109
HOSTILE_DELTA = 0
HOSTILE_COMMON_ZERO = N - HOSTILE_M
HOSTILE_BETA_ALL = math.comb(HOSTILE_COMMON_ZERO, CORE_R)
HOSTILE_J_MIN = (
    UNIFORM_CAP + AGGREGATE_EXCESS_MAX // HOSTILE_BETA_ALL + 1
)
HOSTILE_BETA_BREAK = (
    AGGREGATE_EXCESS_MAX // (HOSTILE_J - UNIFORM_CAP) + 1
)
HOSTILE_EXCESS = HOSTILE_BETA_ALL * (HOSTILE_J - UNIFORM_CAP)
HOSTILE_MARGIN = HOSTILE_EXCESS - AGGREGATE_EXCESS_MAX
HOSTILE_GCD_DEGREE_FLOOR = A - HOSTILE_X - J
HOSTILE_PLANT_FLOOR = T - HOSTILE_X + 1

TOY_BETA_PROFILE = [161, 165, 165, 161, 165]
TOY_LINE_COUNT = 5
TOY_LINE_SIZE = 21
TOY_CANDIDATE_INCIDENCES = 51_975
TOY_VALID_INCIDENCES = 51_765
TOY_DISTINCT_BASES = 35_238
TOY_MAX_MULTIPLICITY = 21
TOY_DIRECT_EXCESS = 817
TOY_ATLAS_EXCESS = 817

NONCLAIMS = [
    "This packet does not realize the hostile scalar profile as an RS selector.",
    "This packet does not prove beta_L equals every ambient eight-subset.",
    "This packet does not define a post-branches-3-5 residual.",
    "This packet does not turn arbitrary planted points into a paid owner.",
    "This packet does not globally bank the tangent or chart-boundary caps.",
    "This packet does not prove the deployed rich-pencil aggregate bound.",
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
    data = load_json(ROOT / relative)
    require(
        data.get("payload_sha256") == payload_hash(data),
        f"bad predecessor payload: {relative}",
    )
    return str(data["payload_sha256"])


def expected_certificate() -> dict[str, Any]:
    source_bindings = [
        source_binding("packet-note", NOTE_REL, "load-bearing atlas note"),
        source_binding("packet-readme", README_REL, "replay instructions"),
        source_binding("packet-verifier", PYTHON_REL, "exact route-cut verifier"),
        source_binding("packet-sage", SAGE_REL, "exact atlas replay"),
        source_binding("fixed-basis-note", FIXED_NOTE_REL, "aggregate predecessor"),
        source_binding("mask-contract-note", CONTRACT_NOTE_REL, "source quantifier contract"),
        source_binding("mask-contract-certificate", CONTRACT_CERT_REL, "exact contract artifact"),
        source_binding("sparse-chart-note", SPARSE_NOTE_REL, "regular sparse equations"),
        source_binding("actual-core-theorem", ACTUAL_CORE_REL, "MDS row-basis theorem"),
        source_binding("locator-note", LOCATOR_NOTE_REL, "five-pencil source"),
        source_binding("predecessor-sage", PREDECESSOR_SAGE_REL, "loaded exact witness"),
    ]
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": source_bindings,
        "predecessor_bindings": {
            "fixed_basis_payload": predecessor_payload(FIXED_CERT_REL),
            "branch3_5_contract_sha256": file_hash(CONTRACT_CERT_REL),
        },
        "row": {
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "t": T,
            "cutoff_D": CUTOFF_D,
            "tail_target": str(TAIL_TARGET),
            "core_r": CORE_R,
        },
        "canonical_atlas": {
            "graph_point": "(eta,z_eta) in F x F^8",
            "graph_line": "z=alpha+eta*beta",
            "word_pencil": "e_eta=a_L+eta*b_L",
            "common_zero": "Z_L={x:a_L(x)=b_L(x)=0}",
            "basis_mass": "beta_L=# independent K0 eight-subsets of Z_L",
            "identity": "E_20=sum_{L:J_L>=21} beta_L*(J_L-20)",
            "basis_owner_is_unique": True,
        },
        "moving_zero_system": {
            "x_definition": "x_L=M_L-j",
            "moving_zero_size": "|F_eta,L|=x_L+delta_eta",
            "moving_zero_disjoint": True,
            "incidence_inequality": "J_L*x_L+sum(delta_eta)<=j+x_L",
            "transversality_floor": "x_L+delta_eta>=1",
            "rich_x_min": RICH_X_MIN,
            "rich_x_max": RICH_X_MAX,
        },
        "sparse_pencil": {
            "codeword_form": [
                "a_L=epsilon_0-ev(P_L)",
                "b_L=epsilon_1-ev(Q_L)",
            ],
            "gcd_locator": "L_((D-W_L)-Sigma) divides gcd(P_L,Q_L)",
            "gcd_degree_floor": "A-x_L-|Sigma|",
            "plant_floor": "t-x_L+1",
            "branch5_status": "UNBOUND_SOURCE_FAMILY",
            "plant_is_paid": False,
        },
        "hostile_scalar_relaxation": {
            "classification": "EXACT_SCALAR_ROUTE_CUT_NOT_RS_SELECTOR",
            "carrier_size": N,
            "x": HOSTILE_X,
            "M": HOSTILE_M,
            "J": HOSTILE_J,
            "delta": HOSTILE_DELTA,
            "moving_zero_feasible": HOSTILE_J * HOSTILE_X <= HOSTILE_M,
            "common_zero_size": HOSTILE_COMMON_ZERO,
            "beta_all": str(HOSTILE_BETA_ALL),
            "minimum_J_at_beta_all": HOSTILE_J_MIN,
            "beta_break": str(HOSTILE_BETA_BREAK),
            "hostile_excess": str(HOSTILE_EXCESS),
            "aggregate_excess_max": str(AGGREGATE_EXCESS_MAX),
            "hostile_margin": str(HOSTILE_MARGIN),
            "gcd_degree_floor_at_full_sparse_support": HOSTILE_GCD_DEGREE_FLOOR,
            "gcd_degree_feasible": HOSTILE_GCD_DEGREE_FLOOR <= K - 1,
            "plant_floor": HOSTILE_PLANT_FLOOR,
            "plant_floor_feasible": HOSTILE_PLANT_FLOOR <= J,
            "deployed_selector_constructed": False,
        },
        "toy_atlas_control": {
            "field": "GF(2^37)",
            "row": [34, 13, 21, 20, 14],
            "declared_slopes": 105,
            "rank_tuple": [9, 10, 11],
            "rich_line_count": TOY_LINE_COUNT,
            "rich_line_sizes": [TOY_LINE_SIZE] * TOY_LINE_COUNT,
            "beta_profile": TOY_BETA_PROFILE,
            "candidate_mask_basis_incidences": TOY_CANDIDATE_INCIDENCES,
            "valid_mask_basis_incidences": TOY_VALID_INCIDENCES,
            "distinct_valid_bases": TOY_DISTINCT_BASES,
            "maximum_basis_multiplicity": TOY_MAX_MULTIPLICITY,
            "direct_excess": TOY_DIRECT_EXCESS,
            "atlas_excess": TOY_ATLAS_EXCESS,
            "identity_verified": TOY_DIRECT_EXCESS == TOY_ATLAS_EXCESS,
            "gcd_degrees": [11] * TOY_LINE_COUNT,
            "sparse_plant_sizes": [2] * TOY_LINE_COUNT,
            "koalabear_domain_instantiated": False,
        },
        "first_match_contract": {
            "post_branches_3_5_residual_allowed": False,
            "q0_membership_executable": True,
            "q0_globally_paid": False,
            "branch5_source_bound": False,
            "live_envelope": "WHOLE_DECLARED_SPARSE_RANK9_SUCCESSOR",
            "current_terminal": "UNPAID_SOURCE_BOUND_RICH_PENCIL_AGGREGATE",
        },
        "compiler": {
            "core_basis_count": str(CORE_BASIS_COUNT),
            "ambient_basis_count": str(AMBIENT_BASIS_COUNT),
            "aggregate_excess_max": str(AGGREGATE_EXCESS_MAX),
            "conditional_regular_excess_max": str(REGULAR_AGGREGATE_EXCESS_MAX),
            "regular_allowance_status": "DIAGNOSTIC_GLOBAL_AGGREGATION_UNPROVEN",
            "aggregate_gate_status": "UNPROVEN_DEPLOYED_RICH_PENCIL_INCIDENCE",
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
            "packet_verdict": "GREEN_COMPILER_AND_SCALAR_ROUTE_CUT",
            "global_verdict": "YELLOW_DEPLOYED_RICH_PENCIL_AND_RANK9_OPEN",
            "parameter_dependence": "EXACT_KOALABEAR_ARITHMETIC_PLUS_FIELD_UNIFORM_ATLAS_PLUS_EXACT_GF2_37_CONTROL",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "deployed_field_census_performed": False,
        },
        "nonclaims": NONCLAIMS,
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def strict_match(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type mismatch at {path}")
    if type(expected) is dict:
        require(actual.keys() == expected.keys(), f"key mismatch at {path}")
        for key in expected:
            strict_match(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_match(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"value mismatch at {path}")


def validate_certificate(data: dict[str, Any]) -> None:
    expected = expected_certificate()
    strict_match(data, expected)
    require(data["payload_sha256"] == payload_hash(data), "payload hash mismatch")
    require(RICH_X_MIN == -18_013, "rich x lower endpoint drift")
    require(RICH_X_MAX == 49_055, "rich x upper endpoint drift")
    require(HOSTILE_J_MIN == HOSTILE_J == 109, "hostile J threshold drift")
    require(HOSTILE_BETA_ALL >= HOSTILE_BETA_BREAK, "hostile beta no longer breaks")
    require(HOSTILE_MARGIN > 0, "hostile route-cut margin is not positive")
    require(
        HOSTILE_BETA_ALL * (HOSTILE_J - 1 - UNIFORM_CAP)
        <= AGGREGATE_EXCESS_MAX,
        "hostile J threshold is not integer-sharp",
    )
    require(
        HOSTILE_GCD_DEGREE_FLOOR == 134_943,
        "hostile GCD floor drift",
    )
    require(HOSTILE_PLANT_FLOOR == T, "hostile plant floor drift")
    require(TOY_DIRECT_EXCESS == TOY_ATLAS_EXCESS, "toy atlas identity drift")
    require(
        REGULAR_AGGREGATE_EXCESS_MAX
        == AGGREGATE_EXCESS_MAX - R * CORE_BASIS_COUNT,
        "conditional regular allowance drift",
    )


def rehash(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


Mutation = tuple[str, Callable[[dict[str, Any]], None], bool]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-bad"), True),
        ("status", lambda d: d.__setitem__("status", "PROVED_CLOSED"), True),
        ("row-j", lambda d: d["row"].__setitem__("j", J + 1), True),
        ("tail", lambda d: d["row"].__setitem__("tail_target", str(TAIL_TARGET + 1)), True),
        ("identity", lambda d: d["canonical_atlas"].__setitem__("identity", "pointwise cap"), True),
        ("owner", lambda d: d["canonical_atlas"].__setitem__("basis_owner_is_unique", False), True),
        ("x-min", lambda d: d["moving_zero_system"].__setitem__("rich_x_min", RICH_X_MIN - 1), True),
        ("x-max", lambda d: d["moving_zero_system"].__setitem__("rich_x_max", RICH_X_MAX + 1), True),
        ("disjoint", lambda d: d["moving_zero_system"].__setitem__("moving_zero_disjoint", False), True),
        ("plant-paid", lambda d: d["sparse_pencil"].__setitem__("plant_is_paid", True), True),
        ("branch5", lambda d: d["sparse_pencil"].__setitem__("branch5_status", "PAID"), True),
        ("hostile-x", lambda d: d["hostile_scalar_relaxation"].__setitem__("x", 2), True),
        ("hostile-carrier", lambda d: d["hostile_scalar_relaxation"].__setitem__("carrier_size", N - 1), True),
        ("hostile-J", lambda d: d["hostile_scalar_relaxation"].__setitem__("J", 108), True),
        ("hostile-beta", lambda d: d["hostile_scalar_relaxation"].__setitem__("beta_all", str(HOSTILE_BETA_ALL - 1)), True),
        ("hostile-break", lambda d: d["hostile_scalar_relaxation"].__setitem__("beta_break", str(HOSTILE_BETA_BREAK + 1)), True),
        ("hostile-margin", lambda d: d["hostile_scalar_relaxation"].__setitem__("hostile_margin", "0"), True),
        ("selector", lambda d: d["hostile_scalar_relaxation"].__setitem__("deployed_selector_constructed", True), True),
        ("gcd-floor", lambda d: d["hostile_scalar_relaxation"].__setitem__("gcd_degree_floor_at_full_sparse_support", HOSTILE_GCD_DEGREE_FLOOR - 1), True),
        ("plant-floor", lambda d: d["hostile_scalar_relaxation"].__setitem__("plant_floor", HOSTILE_PLANT_FLOOR - 1), True),
        ("toy-lines", lambda d: d["toy_atlas_control"].__setitem__("rich_line_count", 4), True),
        ("toy-beta", lambda d: d["toy_atlas_control"]["beta_profile"].__setitem__(0, 160), True),
        ("toy-direct", lambda d: d["toy_atlas_control"].__setitem__("direct_excess", 816), True),
        ("toy-atlas", lambda d: d["toy_atlas_control"].__setitem__("atlas_excess", 818), True),
        ("toy-domain", lambda d: d["toy_atlas_control"].__setitem__("koalabear_domain_instantiated", True), True),
        ("post-residual", lambda d: d["first_match_contract"].__setitem__("post_branches_3_5_residual_allowed", True), True),
        ("q0-paid", lambda d: d["first_match_contract"].__setitem__("q0_globally_paid", True), True),
        ("current-paid", lambda d: d["first_match_contract"].__setitem__("current_terminal", "PAID"), True),
        ("aggregate-paid", lambda d: d["compiler"].__setitem__("aggregate_gate_status", "PROVED"), True),
        ("regular-paid", lambda d: d["compiler"].__setitem__("regular_allowance_status", "BANKED"), True),
        ("ledger", lambda d: d["ledger"].__setitem__("movement", "1"), True),
        ("verdict", lambda d: d["audit"].__setitem__("global_verdict", "GREEN_CLOSED"), True),
        ("nonclaim", lambda d: d["nonclaims"].pop(), True),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64), True),
        ("predecessor-hash", lambda d: d["predecessor_bindings"].__setitem__("fixed_basis_payload", "0" * 64), True),
        ("type-confusion", lambda d: d["hostile_scalar_relaxation"].__setitem__("x", True), True),
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
    print(f"aggregate_excess_max={AGGREGATE_EXCESS_MAX}")
    print(f"rich_x_interval=[{RICH_X_MIN},{RICH_X_MAX}]")
    print(f"hostile_beta_all={HOSTILE_BETA_ALL}")
    print(f"hostile_J_min={HOSTILE_J_MIN}")
    print(f"hostile_margin={HOSTILE_MARGIN}")
    print(f"toy_direct_excess={TOY_DIRECT_EXCESS}")
    print(f"toy_atlas_excess={TOY_ATLAS_EXCESS}")
    print("classification=PROVED_COMPILER_AND_SCALAR_ROUTE_CUT_NO_LEDGER_MOVEMENT")
    print("check=PASS")


if __name__ == "__main__":
    main()
