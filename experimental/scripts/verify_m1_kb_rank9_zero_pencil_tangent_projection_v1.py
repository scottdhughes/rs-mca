#!/usr/bin/env python3
"""Verify the rank-nine zero-pencil tangent projection packet.

The checker freezes the deployed statement and independently replays one exact
small-prime logical control.  It does not certify global first-match payment or
the nonzero determinant-weighted source-incidence bound.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-rank9-zero-pencil-tangent-projection-v1"
ARTIFACT_KIND = "M1_KB_RANK9_ZERO_PENCIL_TANGENT_PROJECTION"
STATUS = "PROVED_FIXED_TRANSLATION_ZERO_PENCIL_TANGENT_PROJECTION"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-zero-pencil-tangent-projection-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_zero_pencil_tangent_projection_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_zero_pencil_tangent_projection_v1.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py"
)
RICH_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)
RICH_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py"
)
SPARSE_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"
)
SPARSE_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py"
)
CONTRACT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_5_mask_contract_v1.md"
)

P = 2_130_706_433
EXTENSION_DEGREE = 6
N = 1 << 21
K = 1 << 20
A = 1_116_048
R = N - K
J = N - A
T = A - K
U_PAID = 2_602_502_999
B_REMAINING = 274_980_725_508_892_088

NONCLAIMS = [
    "This packet does not promote the tangent cap to a globally paid owner.",
    "This packet does not replace existential slope projection by one chosen witness.",
    "This packet does not assume rank nine survives slope deletion.",
    "This packet does not bound the determinant-weighted nonzero rich-line sum.",
    "This packet does not move U_paid or B_remaining.",
    "This packet does not determine U_Q or U_A.",
    "This packet does not authorize rank at least ten, Lean, or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """A parser, source, arithmetic, or semantic check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def exact_int(value: object, label: str) -> int:
    require(type(value) is int, f"{label} is not an exact integer")
    return int(value)


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


def mod_inv(value: int, prime: int) -> int:
    value %= prime
    require(value != 0, "attempted inversion of zero")
    return pow(value, prime - 2, prime)


def polynomial_fit_exists(
    *,
    prime: int,
    domain: list[int],
    support: list[int],
    values: list[int],
    dimension: int,
) -> bool:
    """Return whether degree-<dimension data interpolate on the support."""

    require(dimension >= 1, "toy code dimension must be positive")
    matrix: list[list[int]] = []
    for index in support:
        x = domain[index] % prime
        row = [pow(x, degree, prime) for degree in range(dimension)]
        row.append(values[index] % prime)
        matrix.append(row)

    pivot_row = 0
    for column in range(dimension):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = mod_inv(matrix[pivot_row][column], prime)
        matrix[pivot_row] = [(entry * scale) % prime for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            factor = matrix[row][column] % prime
            if factor:
                matrix[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_row += 1

    for row in matrix:
        if all(entry % prime == 0 for entry in row[:dimension]):
            if row[dimension] % prime != 0:
                return False
    return True


def tangent_image(
    *, prime: int, epsilon_0: list[int], epsilon_1: list[int]
) -> tuple[list[int], dict[str, int], list[int]]:
    sigma = [
        index
        for index, pair in enumerate(zip(epsilon_0, epsilon_1))
        if (pair[0] % prime, pair[1] % prime) != (0, 0)
    ]
    histogram: dict[str, int] = {}
    for index in sigma:
        denominator = epsilon_1[index] % prime
        if denominator == 0:
            continue
        eta = (-epsilon_0[index] * mod_inv(denominator, prime)) % prime
        key = str(eta)
        histogram[key] = histogram.get(key, 0) + 1
    return sorted(int(key) for key in histogram), histogram, sigma


def analyze_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    prime = exact_int(fixture["prime"], "fixture.prime")
    require(prime > 2, "fixture prime too small")
    domain = fixture["domain"]
    require(type(domain) is list and domain, "fixture domain missing")
    require(all(type(x) is int for x in domain), "noninteger domain point")
    require(len({x % prime for x in domain}) == len(domain), "domain points repeat")

    n = len(domain)
    dimension = exact_int(fixture["k"], "fixture.k")
    agreement = exact_int(fixture["A"], "fixture.A")
    radius = exact_int(fixture["j"], "fixture.j")
    require(radius == n - agreement, "toy row A/j arithmetic drift")
    require(1 <= dimension < agreement <= n, "toy row dimensions invalid")

    epsilon_0 = fixture["epsilon_0"]
    epsilon_1 = fixture["epsilon_1"]
    require(
        type(epsilon_0) is list
        and type(epsilon_1) is list
        and len(epsilon_0) == len(epsilon_1) == n,
        "toy source vectors have wrong length",
    )
    require(
        all(type(value) is int for value in epsilon_0 + epsilon_1),
        "toy source vector is not integral",
    )

    image, ratio_histogram, sigma = tangent_image(
        prime=prime, epsilon_0=epsilon_0, epsilon_1=epsilon_1
    )
    require(len(sigma) <= radius, "toy sparse support exceeds j")

    witnesses = fixture["zero_pencil_witnesses"]
    require(type(witnesses) is list and witnesses, "toy witnesses missing")
    witness_slopes: list[int] = []
    witness_records: list[dict[str, Any]] = []
    for witness_index, witness in enumerate(witnesses):
        require(type(witness) is dict, "toy witness is not an object")
        eta = exact_int(witness["eta"], f"witness[{witness_index}].eta")
        require(0 <= eta < prime, "toy slope left the field")
        support = witness["support"]
        require(type(support) is list, "toy support is not a list")
        require(len(support) == agreement, "toy support does not have size A")
        require(
            all(type(index) is int and 0 <= index < n for index in support),
            "toy support index invalid",
        )
        require(len(set(support)) == len(support), "toy support repeats a point")
        require(
            all(
                (epsilon_0[index] + eta * epsilon_1[index]) % prime == 0
                for index in support
            ),
            "zero codeword does not agree on toy support",
        )

        fit_0 = polynomial_fit_exists(
            prime=prime,
            domain=domain,
            support=support,
            values=epsilon_0,
            dimension=dimension,
        )
        fit_1 = polynomial_fit_exists(
            prime=prime,
            domain=domain,
            support=support,
            values=epsilon_1,
            dimension=dimension,
        )
        require(not (fit_0 and fit_1), "toy witness is support-wise contained")

        forced_points = [
            index
            for index in support
            if (epsilon_0[index] % prime, epsilon_1[index] % prime) != (0, 0)
        ]
        require(forced_points, "noncontainment did not force a source point")
        for index in forced_points:
            require(epsilon_1[index] % prime != 0, "forced point has zero denominator")
            forced_eta = (
                -epsilon_0[index] * mod_inv(epsilon_1[index], prime)
            ) % prime
            require(forced_eta == eta, "forced point has wrong tangent ratio")

        require(eta in image, "zero-pencil slope escaped tangent image")
        witness_slopes.append(eta)
        witness_records.append(
            {
                "eta": eta,
                "support": support,
                "epsilon_0_code_fit_exists": fit_0,
                "epsilon_1_code_fit_exists": fit_1,
                "support_wise_noncontained": True,
                "forced_source_points": forced_points,
            }
        )

    projected = sorted(set(witness_slopes))
    require(set(projected).issubset(image), "projection inclusion failed")
    require(len(projected) <= len(image) <= len(sigma) <= radius, "projection cap failed")
    return {
        "sigma": sigma,
        "sigma_size": len(sigma),
        "tangent_image": image,
        "tangent_ratio_histogram": ratio_histogram,
        "zero_pencil_slope_projection": projected,
        "zero_pencil_slope_count": len(projected),
        "witness_records": witness_records,
        "inclusion_verified": True,
        "cap_chain": [len(projected), len(image), len(sigma), radius],
    }


def toy_fixture() -> dict[str, Any]:
    return {
        "prime": 11,
        "domain": list(range(9)),
        "k": 1,
        "A": 3,
        "j": 6,
        "epsilon_0": [10, 9, 8, 9, 7, 5, 0, 0, 0],
        "epsilon_1": [1, 2, 3, 1, 2, 3, 0, 0, 0],
        "zero_pencil_witnesses": [
            {"eta": 1, "support": [0, 1, 2]},
            {"eta": 2, "support": [3, 4, 5]},
        ],
    }


def expected_certificate() -> dict[str, Any]:
    fixture = toy_fixture()
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": [
            source_binding("packet-note", NOTE_REL, "statement, proof, and scope"),
            source_binding("packet-python", PYTHON_REL, "strict checker and toy replay"),
            source_binding("rich-pencil-note", RICH_NOTE_REL, "zero/nonzero pencil split"),
            source_binding("rich-pencil-checker", RICH_SCRIPT_REL, "atlas contract"),
            source_binding("sparse-note", SPARSE_NOTE_REL, "tangent slope cap"),
            source_binding("sparse-checker", SPARSE_SCRIPT_REL, "tangent classifier"),
            source_binding("mask-contract", CONTRACT_NOTE_REL, "first-match quantifiers"),
        ],
        "deployed_row": {
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "q_line": P**EXTENSION_DEGREE,
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "t": T,
        },
        "projection_lemma": {
            "fixed_sp3_translation_required": True,
            "slope_projection_existential_over_all_eligible_witnesses": True,
            "support_wise_noncontainment_required": True,
            "zero_witness_condition": "translated explaining codeword h=0",
            "rich_zero_pencil_implication": "P_L=Q_L=0 implies Gamma_L subset Z_0",
            "translated_explaining_codeword": "0",
            "tangent_image": "{-epsilon_0(x)/epsilon_1(x):x in Sigma,epsilon_1(x)!=0}",
            "inclusion": "Z_0(epsilon_0,epsilon_1) subset tangent_image",
            "cap": "|Z_0|<=|tangent_image|<=|Sigma|<=j",
            "deployed_cap": J,
            "zero_word_pencil_unique_for_fixed_translation": True,
            "W_L_equals_Sigma_alone_is_insufficient": True,
        },
        "first_match_integration": {
            "existing_route": "SPARSE_TANGENT_RANK9_CONDITIONAL_CAP",
            "unpaid_primitive": False,
            "earlier_owner_dedup_required": True,
            "global_tangent_projector_banked": False,
            "delete_zero_pencil_slopes_before_rich_selector": True,
            "residual_complete_selector_must_be_rebuilt": True,
            "residual_intrinsic_rank_must_be_recomputed": True,
            "lower_rank_must_route_to_declared_predecessor": True,
            "zero_pencil_atlas_term_may_be_dropped_before_global_payment": False,
        },
        "toy_fixture": fixture,
        "toy_replay": analyze_fixture(fixture),
        "ledger": {
            "U_paid_before": U_PAID,
            "U_paid_after": U_PAID,
            "B_remaining_before": B_REMAINING,
            "B_remaining_after": B_REMAINING,
            "ledger_movement": 0,
            "U_Q": None,
            "U_A": None,
        },
        "scope_guards": {
            "local_projection_lemma_proved": True,
            "global_first_match_payment_proved": False,
            "deployed_source_family_census_present": False,
            "nonzero_plant_load_bound_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": NONCLAIMS,
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def verify_source_bindings(value: dict[str, Any]) -> None:
    expected = expected_certificate()["source_bindings"]
    require(value["source_bindings"] == expected, "source binding drift")


def verify_semantics(value: dict[str, Any]) -> None:
    require(value.get("schema") == SCHEMA, "schema drift")
    require(value.get("artifact_kind") == ARTIFACT_KIND, "artifact kind drift")
    require(value.get("status") == STATUS, "status drift")
    require(value.get("payload_sha256") == payload_hash(value), "payload hash mismatch")
    verify_source_bindings(value)

    row = value["deployed_row"]
    for key in ("p", "extension_degree", "q_line", "n", "k", "A", "R", "j", "t"):
        exact_int(row[key], f"deployed_row.{key}")
    require(
        row
        == {
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "q_line": P**EXTENSION_DEGREE,
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "t": T,
        },
        "deployed row drift",
    )
    require((R, J, T) == (N - K, N - A, A - K), "row arithmetic drift")

    lemma = value["projection_lemma"]
    require(
        lemma["fixed_sp3_translation_required"] is True
        and lemma["slope_projection_existential_over_all_eligible_witnesses"] is True
        and lemma["support_wise_noncontainment_required"] is True,
        "projection quantifier weakened",
    )
    require(
        lemma["zero_witness_condition"] == "translated explaining codeword h=0"
        and lemma["rich_zero_pencil_implication"]
        == "P_L=Q_L=0 implies Gamma_L subset Z_0"
        and lemma["translated_explaining_codeword"] == "0",
        "zero-pencil hypothesis drift",
    )
    require(
        lemma["tangent_image"]
        == "{-epsilon_0(x)/epsilon_1(x):x in Sigma,epsilon_1(x)!=0}"
        and lemma["inclusion"]
        == "Z_0(epsilon_0,epsilon_1) subset tangent_image"
        and lemma["cap"] == "|Z_0|<=|tangent_image|<=|Sigma|<=j"
        and lemma["deployed_cap"] == J,
        "projection statement drift",
    )
    require(
        lemma["zero_word_pencil_unique_for_fixed_translation"] is True
        and lemma["W_L_equals_Sigma_alone_is_insufficient"] is True,
        "zero-pencil edge case drift",
    )

    integration = value["first_match_integration"]
    require(
        integration
        == {
            "existing_route": "SPARSE_TANGENT_RANK9_CONDITIONAL_CAP",
            "unpaid_primitive": False,
            "earlier_owner_dedup_required": True,
            "global_tangent_projector_banked": False,
            "delete_zero_pencil_slopes_before_rich_selector": True,
            "residual_complete_selector_must_be_rebuilt": True,
            "residual_intrinsic_rank_must_be_recomputed": True,
            "lower_rank_must_route_to_declared_predecessor": True,
            "zero_pencil_atlas_term_may_be_dropped_before_global_payment": False,
        },
        "first-match integration drift",
    )

    replay = analyze_fixture(value["toy_fixture"])
    require(value["toy_replay"] == replay, "toy replay drift")
    require(
        replay["sigma"] == [0, 1, 2, 3, 4, 5]
        and replay["tangent_image"] == [1, 2]
        and replay["tangent_ratio_histogram"] == {"1": 3, "2": 3}
        and replay["zero_pencil_slope_projection"] == [1, 2]
        and replay["cap_chain"] == [2, 2, 6, 6],
        "canonical toy output drift",
    )

    ledger = value["ledger"]
    require(
        ledger
        == {
            "U_paid_before": U_PAID,
            "U_paid_after": U_PAID,
            "B_remaining_before": B_REMAINING,
            "B_remaining_after": B_REMAINING,
            "ledger_movement": 0,
            "U_Q": None,
            "U_A": None,
        },
        "ledger drift",
    )
    require(
        value["scope_guards"]
        == {
            "local_projection_lemma_proved": True,
            "global_first_match_payment_proved": False,
            "deployed_source_family_census_present": False,
            "nonzero_plant_load_bound_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "scope guard drift",
    )
    require(value["nonclaims"] == NONCLAIMS, "nonclaim list drift")


def run_check() -> None:
    value = load_json(CERT_PATH)
    verify_semantics(value)
    print("M1 rank-nine zero-pencil tangent projection: PASS")
    print("  fixed-translation inclusion: Z_0 subset tangent_image")
    print(f"  deployed local cap: |Z_0| <= j = {J:,}")
    print("  global tangent payment: OPEN; deployed ledger unchanged")


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-mutated")),
        ("kind", lambda d: d.__setitem__("artifact_kind", "DEPLOYED_CLOSURE")),
        ("status", lambda d: d.__setitem__("status", "KOALABEAR_CLOSED")),
        ("row", lambda d: d["deployed_row"].__setitem__("A", A - 1)),
        ("q-line", lambda d: d["deployed_row"].__setitem__("q_line", P**5)),
        ("translation", lambda d: d["projection_lemma"].__setitem__("fixed_sp3_translation_required", False)),
        ("existential", lambda d: d["projection_lemma"].__setitem__("slope_projection_existential_over_all_eligible_witnesses", False)),
        ("noncontainment", lambda d: d["projection_lemma"].__setitem__("support_wise_noncontainment_required", False)),
        ("zero-condition", lambda d: d["projection_lemma"].__setitem__("zero_witness_condition", "W_L=Sigma")),
        ("rich-implication", lambda d: d["projection_lemma"].__setitem__("rich_zero_pencil_implication", "unproved")),
        ("image", lambda d: d["projection_lemma"].__setitem__("tangent_image", "all slopes")),
        ("inclusion", lambda d: d["projection_lemma"].__setitem__("inclusion", "equality")),
        ("cap", lambda d: d["projection_lemma"].__setitem__("deployed_cap", J + 1)),
        ("unique", lambda d: d["projection_lemma"].__setitem__("zero_word_pencil_unique_for_fixed_translation", False)),
        ("W-alone", lambda d: d["projection_lemma"].__setitem__("W_L_equals_Sigma_alone_is_insufficient", False)),
        ("owner", lambda d: d["first_match_integration"].__setitem__("existing_route", "UNPAID_PRIMITIVE")),
        ("primitive", lambda d: d["first_match_integration"].__setitem__("unpaid_primitive", True)),
        ("global", lambda d: d["first_match_integration"].__setitem__("global_tangent_projector_banked", True)),
        ("delete", lambda d: d["first_match_integration"].__setitem__("delete_zero_pencil_slopes_before_rich_selector", False)),
        ("rebuild", lambda d: d["first_match_integration"].__setitem__("residual_complete_selector_must_be_rebuilt", False)),
        ("rank", lambda d: d["first_match_integration"].__setitem__("residual_intrinsic_rank_must_be_recomputed", False)),
        ("drop-term", lambda d: d["first_match_integration"].__setitem__("zero_pencil_atlas_term_may_be_dropped_before_global_payment", True)),
        ("toy-source", lambda d: d["toy_fixture"]["epsilon_0"].__setitem__(0, 9)),
        ("toy-slope", lambda d: d["toy_fixture"]["zero_pencil_witnesses"][0].__setitem__("eta", 2)),
        ("toy-support", lambda d: d["toy_fixture"]["zero_pencil_witnesses"][0].__setitem__("support", [0, 1])),
        ("toy-repeat", lambda d: d["toy_fixture"]["zero_pencil_witnesses"][0].__setitem__("support", [0, 0, 1])),
        ("toy-image", lambda d: d["toy_replay"].__setitem__("tangent_image", [1, 2, 3])),
        ("toy-cap", lambda d: d["toy_replay"].__setitem__("cap_chain", [2, 2, 6, 5])),
        ("ledger", lambda d: d["ledger"].__setitem__("ledger_movement", 1)),
        ("UQ", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("global-proof", lambda d: d["scope_guards"].__setitem__("global_first_match_payment_proved", True)),
        ("plant-proof", lambda d: d["scope_guards"].__setitem__("nonzero_plant_load_bound_proved", True)),
        ("closure", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("lean", lambda d: d["scope_guards"].__setitem__("lean_authorized", True)),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
        ("type-bool-int", lambda d: d["deployed_row"].__setitem__("n", True)),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("payload", lambda d: d.__setitem__("payload_sha256", "1" * 64)),
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
    print(f"M1 zero-pencil tangent mutations: {passed}/{expected} PASS")


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
