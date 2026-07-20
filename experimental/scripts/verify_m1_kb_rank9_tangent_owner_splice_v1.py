#!/usr/bin/env python3
"""Verify the KoalaBear tangent first-match owner splice.

The packet promotes one fixed SP3 tangent image to a global-once slope owner
for each received pair, restarts the residual selector ladder, and recomputes
the exact post-charge rank-nine thresholds.  It does not prove the remaining
nonzero determinant-weighted incidence bound or close the KoalaBear row.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-rank9-tangent-owner-splice-v1"
ARTIFACT_KIND = "M1_KB_RANK9_TANGENT_FIRST_MATCH_OWNER_SPLICE"
STATUS = (
    "PROVED_GLOBAL_FIXED_TRANSLATION_TANGENT_OWNER_"
    "SELECTOR_RESTART_EXACT_LEDGER_MOVEMENT_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-tangent-owner-splice-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_tangent_owner_splice_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_tangent_owner_splice_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-tangent-owner-splice-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.sage"
)

THRESHOLDS_REL = Path("experimental/rs_mca_thresholds.tex")
GRANDE_REL = Path("archived/grande_finale_v2.tex")
ZERO_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_zero_pencil_tangent_projection_v1.md"
)
ZERO_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-zero-pencil-tangent-projection-v1/"
    "m1_kb_rank9_zero_pencil_tangent_projection_v1.json"
)
ZERO_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py"
)
READINESS_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-deployed-source-incidence-contract-v1/"
    "m1_kb_rank9_deployed_source_incidence_contract_v1.json"
)
READINESS_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py"
)
SPARSE_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"
)
BASE_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_base_slope_universe_v2.md"
)
BASE_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2/"
    "kb_mca_1116048_base_slope_universe_v2.json"
)
LOW_CARRIER_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-low-excess-carrier-cut-v1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.json"
)
TDD_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-tdd-excess-v1/"
    "m1_kb_branch3_tdd_excess_v1.json"
)
RANK_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-actual-core-mds-v1/"
    "m1_kb_branch3_actual_core_mds_v1.json"
)
MASK_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-rank9-mask-deficit-v1/"
    "m1_kb_branch3_rank9_mask_deficit_v1.json"
)
MASK_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py"
)
RICH_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 1 << 21
K = 1 << 20
A = 1_116_048
R = N - K
J = N - A
DELTA_ZERO = R - J
W = DELTA_ZERO - 1

DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID_BEFORE = 2_602_502_999
B_REMAINING_BEFORE = B_STAR - U_PAID_BEFORE
TANGENT_CHARGE = J
U_PAID_AFTER = U_PAID_BEFORE + TANGENT_CHARGE
B_REMAINING_AFTER = B_STAR - U_PAID_AFTER

LOW_CARRIER_CAP = 78_289_526_705_722_101
SMALL_FAMILY_CAP = 15
RANK_LE_3_CAP = 157_397_034_144_292_985
RANK_4_TO_8_CAP = 58_747_334_643_050_472

RANK_S = 9
CORE_R = 8
UNIFORM_CAP = 20
CUTOFF_D = 18_014
OLD_TAIL_TARGET = 17_907_572_507_584
EXPECTED_NEW_TAIL_TARGET = 17_907_571_352_523
EXPECTED_NEW_E_MAX = int(
    "5284472953556748839425672939211329356986005299"
)
EXPECTED_K_REMAINING = 4_807_520
AUDITED_PAID_CARRIER = 1_699_344
AUDITED_PAID_CUTOFF = 0
EXPECTED_AUDITED_PAID_COARSE_CAP = 274_980_655_093_567_589

FIRST_MATCH_ORDER = [
    "contained_or_noncontained_failure",
    "rank_drop_or_pivot_failure",
    "tangent_common_line_residue",
    "quotient_periodic_or_divisor_stabilized",
    "planted_prefix_structured",
    "extension_valued_slope",
    "residual_base_slope_universe",
    "sparse_sigma_or_sparse_support",
    "m1_half_turn_or_coefficient_shadow",
    "primitive_qfin_residual",
]

RESTART_ORDER = [
    "GLOBAL_CARRIER_EXCESS_LE_10",
    "HIGH_UNION_SMALL_FAMILY_AT_MOST_15",
    "ACTUAL_SELECTED_WITNESS_CORE_RANK_LE_3",
    "ACTUAL_CORE_MDS_INTRINSIC_RANK_4_TO_8",
    "RANK9_COARSE_ACTUAL_CORE_MDS_REPLAY",
    "RANK9_REBUILT_NONZERO_PENCIL_ATLAS",
]

NONCLAIMS = [
    "This packet does not union tangent images from different SP3 translations.",
    "This packet does not count witnesses, supports, coordinates, selectors, or graph lines.",
    "This packet does not pay every common-line or residue-line component.",
    "This packet does not charge the zero-pencil subset separately.",
    "This packet does not retain selector-derived data after tangent deletion.",
    "This packet does not convert the tangent slope cap directly into atlas excess.",
    "This packet does not prove the determinant-weighted nonzero source load.",
    "This packet does not determine U_Q or U_A or close the KoalaBear row.",
    "This packet does not authorize rank at least ten, Lean, or stable-paper promotion.",
    "This packet does not treat mutation cases as independent mathematical proofs.",
]

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "deployed_row",
    "counted_object_contract",
    "global_tangent_owner",
    "first_match_partition",
    "residual_selector_contract",
    "owner_restart",
    "rank9_updated_gate",
    "toy_fixture",
    "toy_replay",
    "ledger",
    "scope_guards",
    "nonclaims",
    "payload_sha256",
}


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


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator > 0, "invalid ceiling division")
    return (numerator + denominator - 1) // denominator


def mod_inv(value: int, prime: int) -> int:
    value %= prime
    require(value != 0, "attempted inversion of zero")
    return pow(value, prime - 2, prime)


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    require(prime > 2, "rank prime too small")
    if not matrix:
        return 0
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "ragged rank matrix")
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = mod_inv(work[rank][column], prime)
        work[rank] = [(entry * scale) % prime for entry in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def tangent_image(
    *, prime: int, epsilon_0: list[int], epsilon_1: list[int]
) -> tuple[list[int], dict[str, int], list[int]]:
    require(len(epsilon_0) == len(epsilon_1), "source-vector length mismatch")
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


def affine_rank(
    records: dict[int, list[int]], slopes: list[int], prime: int
) -> int:
    if len(slopes) <= 1:
        return 0
    anchor = records[slopes[0]]
    differences = [
        [(left - right) % prime for left, right in zip(records[eta], anchor)]
        for eta in slopes[1:]
    ]
    return matrix_rank_mod(differences, prime)


def carrier_size(
    records: dict[int, list[int]], slopes: list[int], prime: int
) -> int:
    require(prime > 2, "carrier prime too small")
    return len(
        {
            index
            for eta in slopes
            for index, value in enumerate(records[eta])
            if value % prime != 0
        }
    )


def analyze_toy(fixture: dict[str, Any]) -> dict[str, Any]:
    prime = exact_int(fixture["prime"], "toy.prime")
    radius = exact_int(fixture["j"], "toy.j")
    epsilon_0 = fixture["epsilon_0"]
    epsilon_1 = fixture["epsilon_1"]
    require(
        type(epsilon_0) is list
        and type(epsilon_1) is list
        and all(type(value) is int for value in epsilon_0 + epsilon_1),
        "toy source vectors invalid",
    )
    image, histogram, sigma = tangent_image(
        prime=prime, epsilon_0=epsilon_0, epsilon_1=epsilon_1
    )
    require(len(sigma) <= radius, "toy source support exceeds j")

    def exact_set(key: str) -> set[int]:
        raw = fixture[key]
        require(type(raw) is list, f"toy {key} is not a list")
        require(all(type(value) is int for value in raw), f"toy {key} is not integral")
        require(len(raw) == len(set(raw)), f"toy {key} repeats a slope")
        require(all(0 <= value < prime for value in raw), f"toy {key} leaves field")
        return set(raw)

    bad = exact_set("bad_slopes")
    earlier = exact_set("earlier_owner_slopes")
    base = exact_set("later_base_slopes")
    zero = exact_set("zero_witness_slopes")
    require(earlier <= bad, "earlier owner is not a bad-slope subset")
    require(zero <= bad and zero <= set(image), "toy zero witness escaped tangent image")

    incoming = bad - earlier
    tangent_cell = incoming & set(image)
    outgoing = incoming - tangent_cell
    later_base_cell = outgoing & base
    require(not (tangent_cell & later_base_cell), "tangent/base first-match overlap")
    require(not (outgoing & zero), "zero witness survived tangent deletion")

    selector_rows = fixture["selector_records"]
    require(type(selector_rows) is list, "toy selector records missing")
    records: dict[int, list[int]] = {}
    for index, row in enumerate(selector_rows):
        require(type(row) is dict, f"toy selector row {index} is not an object")
        eta = exact_int(row["eta"], f"toy selector row {index} eta")
        error = row["error"]
        require(
            type(error) is list and error and all(type(value) is int for value in error),
            f"toy selector row {index} error invalid",
        )
        require(eta not in records, "toy selector repeats a slope")
        records[eta] = error
    require(set(records) == incoming, "toy selector is not complete on incoming residual")
    width = len(next(iter(records.values())))
    require(all(len(row) == width for row in records.values()), "toy error width drift")

    incoming_sorted = sorted(incoming)
    outgoing_sorted = sorted(outgoing)
    incoming_rank = affine_rank(records, incoming_sorted, prime)
    outgoing_rank = affine_rank(records, outgoing_sorted, prime)
    redundancy = exact_int(fixture["selector_redundancy_R"], "toy selector redundancy")
    incoming_carrier = carrier_size(records, incoming_sorted, prime)
    outgoing_carrier = carrier_size(records, outgoing_sorted, prime)
    incoming_kappa = max(0, incoming_carrier - redundancy)
    outgoing_kappa = max(0, outgoing_carrier - redundancy)
    require(outgoing_rank <= incoming_rank, "toy affine rank increased under restriction")

    return {
        "sigma": sigma,
        "sigma_size": len(sigma),
        "tangent_image": image,
        "tangent_ratio_histogram": histogram,
        "bad_slopes": sorted(bad),
        "earlier_owner_slopes": sorted(earlier),
        "incoming_residual": incoming_sorted,
        "tangent_cell": sorted(tangent_cell),
        "outgoing_residual": outgoing_sorted,
        "later_base_cell": sorted(later_base_cell),
        "zero_witness_slopes": sorted(zero),
        "zero_witnesses_surviving": sorted(outgoing & zero),
        "selector_complete_before": True,
        "restricted_selector_exists": True,
        "incoming_affine_rank": incoming_rank,
        "outgoing_affine_rank": outgoing_rank,
        "incoming_carrier_size": incoming_carrier,
        "outgoing_carrier_size": outgoing_carrier,
        "incoming_kappa": incoming_kappa,
        "outgoing_kappa": outgoing_kappa,
        "empty_affine_rank": affine_rank(records, [], prime),
        "singleton_affine_rank": affine_rank(records, incoming_sorted[:1], prime),
    }


def toy_fixture() -> dict[str, Any]:
    return {
        "prime": 11,
        "j": 6,
        "epsilon_0": [10, 9, 8, 9, 7, 5, 0, 0],
        "epsilon_1": [1, 2, 3, 1, 2, 3, 0, 0],
        "bad_slopes": [0, 1, 2, 3, 4],
        "earlier_owner_slopes": [1],
        "later_base_slopes": [0, 1, 2, 3],
        "zero_witness_slopes": [1, 2],
        "selector_redundancy_R": 2,
        "selector_records": [
            {"eta": 0, "error": [1, 0, 0, 0]},
            {"eta": 2, "error": [0, 1, 0, 0]},
            {"eta": 3, "error": [0, 0, 1, 0]},
            {"eta": 4, "error": [0, 0, 0, 1]},
        ],
    }


def m2b_multiplicity(deficit: int, source_distance: int = 1) -> int:
    require(0 <= deficit <= J - 349_526, "deficit outside imported M2b range")
    require(source_distance >= 1, "source distance must be positive")
    basis_count = math.comb(DELTA_ZERO + CORE_R + deficit, CORE_R)
    lift_factor = max(1, source_distance - J + deficit)
    return ceil_div(lift_factor * basis_count, RANK_S)


def coarse_cap(carrier_size: int, source_distance: int = 1) -> int:
    require(RANK_S <= carrier_size <= N, "carrier size outside deployed range")
    return math.comb(carrier_size, RANK_S) // m2b_multiplicity(
        0, source_distance
    )


def max_count_with_one_cut(
    cutoff: int,
    low_cap: int,
    carrier_size: int = N,
    source_distance: int = 1,
) -> int:
    ambient_budget = math.comb(carrier_size, RANK_S)
    mu_zero = m2b_multiplicity(0, source_distance)
    mu_high = m2b_multiplicity(cutoff + 1, source_distance)
    cheap = min(low_cap, ambient_budget // mu_zero)
    return cheap + (ambient_budget - cheap * mu_zero) // mu_high


def one_cut_gate(
    remaining_budget: int,
    cutoff: int,
    carrier_size: int = N,
    source_distance: int = 1,
) -> dict[str, Any]:
    require(0 <= remaining_budget < B_STAR, "invalid remaining budget")
    require(RANK_S <= carrier_size <= N, "carrier size outside deployed range")
    require(source_distance >= 1, "source distance must be positive")
    ambient_budget = math.comb(carrier_size, RANK_S)
    target_size = remaining_budget + 1
    mu_zero = m2b_multiplicity(0, source_distance)
    current_coarse_cap = ambient_budget // mu_zero
    require(
        current_coarse_cap > remaining_budget,
        "one-cut gate is only defined on predecessor coarse-failure cells",
    )
    mu_high = m2b_multiplicity(cutoff + 1, source_distance)
    gain = mu_high - mu_zero
    require(gain > 0, "M2b multiplicity did not increase")
    excess_needed = ambient_budget + 1 - target_size * mu_zero
    required_high = 0 if excess_needed <= 0 else ceil_div(excess_needed, gain)
    maximum_low = target_size - required_high
    require(maximum_low >= 0, "one-cut gate has no useful threshold")
    return {
        "cutoff_D": cutoff,
        "first_high_deficit": cutoff + 1,
        "carrier_size_N_V": carrier_size,
        "source_minimum_lift_d_V": source_distance,
        "ambient_budget_C_n_choose_9": str(ambient_budget),
        "remaining_slope_budget": str(remaining_budget),
        "predecessor_coarse_cap": str(current_coarse_cap),
        "predecessor_coarse_failure_required": True,
        "predecessor_coarse_failure_margin": str(
            current_coarse_cap - remaining_budget
        ),
        "target_counterexample_size": str(target_size),
        "mu_0": str(mu_zero),
        "mu_D_plus_1": str(mu_high),
        "per_high_item_gain": str(gain),
        "required_high_deficit_count": str(required_high),
        "largest_sufficient_low_deficit_cap_T_star": str(maximum_low),
        "cap_at_T_star": str(
            max_count_with_one_cut(
                cutoff, maximum_low, carrier_size, source_distance
            )
        ),
        "cap_at_T_star_plus_1": str(
            max_count_with_one_cut(
                cutoff, maximum_low + 1, carrier_size, source_distance
            )
        ),
    }


def aggregate_excess_max(tail_target: int) -> int:
    core_basis_count = math.comb(DELTA_ZERO + CORE_R, CORE_R)
    ambient_basis_count = math.comb(N, CORE_R)
    return (
        (tail_target + 1) * core_basis_count
        - UNIFORM_CAP * ambient_basis_count
        - 1
    )


@functools.lru_cache(maxsize=None)
def exact_k_remaining(remaining_budget: int) -> int:
    require(remaining_budget >= 0, "negative multiplier budget")
    return remaining_budget * P**W // math.comb(N, J)


def validate_payload(certificate: dict[str, Any], schema: str) -> None:
    require(certificate.get("schema") == schema, f"predecessor schema drift: {schema}")
    require(
        certificate.get("payload_sha256") == payload_hash(certificate),
        f"predecessor payload drift: {schema}",
    )


def validate_predecessors() -> None:
    threshold_text = (ROOT / THRESHOLDS_REL).read_text(encoding="utf-8")
    require(
        "B_{C,\\Gamma}^{\\rm MCA}(a)" in threshold_text
        and "\\sigma_{C,\\Gamma}(a)" in threshold_text
        and "\\tag{SP3}" in threshold_text,
        "SP3 theorem anchors drift",
    )

    zero = load_json(ROOT / ZERO_CERT_REL)
    validate_payload(zero, "rs-mca-m1-kb-rank9-zero-pencil-tangent-projection-v1")
    require(
        zero["projection_lemma"]["deployed_cap"] == J
        and zero["scope_guards"]["local_projection_lemma_proved"] is True
        and zero["scope_guards"]["global_first_match_payment_proved"] is False,
        "zero-pencil predecessor contract drift",
    )

    readiness = load_json(ROOT / READINESS_CERT_REL)
    validate_payload(
        readiness, "rs-mca-m1-kb-rank9-deployed-source-incidence-contract-v1"
    )
    require(
        readiness["ledger"]["U_paid_before"] == str(U_PAID_BEFORE)
        and readiness["ledger"]["movement"] == "0",
        "readiness predecessor ledger drift",
    )

    base = load_json(ROOT / BASE_CERT_REL)
    validate_payload(base, "rs-mca-kb-1116048-base-slope-universe-v2")
    require(
        base["first_match"]["v2_order"] == FIRST_MATCH_ORDER
        and FIRST_MATCH_ORDER.index("tangent_common_line_residue")
        < FIRST_MATCH_ORDER.index("residual_base_slope_universe"),
        "tangent/base owner order drift",
    )

    low = load_json(ROOT / LOW_CARRIER_CERT_REL)
    validate_payload(low, "rs-mca-m1-kb-branch3-low-excess-carrier-cut-v1")
    require(
        low["ledger"]["conditional_max_low_excess_cap"] == str(LOW_CARRIER_CAP),
        "low-carrier cap drift",
    )

    tdd = load_json(ROOT / TDD_CERT_REL)
    validate_payload(tdd, "rs-mca-m1-kb-branch3-tdd-excess-v1")
    require(
        tdd["ledger"]["conditional_rank3_cap"] == str(RANK_LE_3_CAP)
        and tdd["ledger"]["conditional_terminal_proved"] is True,
        "rank-at-most-three terminal drift",
    )
    require(
        tdd["predecessor_state"]["global_carrier_checked_first"] is True
        and tdd["predecessor_state"]["small_family_cap"]
        == SMALL_FAMILY_CAP
        and tdd["predecessor_state"][
            "rank_minimizing_selector_gets_fresh_tdd_when_family_gt_15"
        ]
        is True,
        "carrier/small-family restart order drift",
    )

    rank = load_json(ROOT / RANK_CERT_REL)
    validate_payload(rank, "rs-mca-m1-kb-branch3-actual-core-mds-v1")
    require(
        rank["rank_ladder"]["worst_paid_rank"] == 8
        and rank["rank_ladder"]["worst_paid_cap"] == str(RANK_4_TO_8_CAP)
        and rank["rank_ladder"]["first_rank_not_uniformly_paid"] == 9,
        "rank ladder drift",
    )

    mask = load_json(ROOT / MASK_CERT_REL)
    validate_payload(mask, "rs-mca-m1-kb-branch3-rank9-mask-deficit-v1")
    old_gate = mask["one_cut_tail_frontier"]["universal_first_gate"]
    require(
        old_gate["cutoff_D"] == CUTOFF_D
        and old_gate["largest_sufficient_low_deficit_cap_T_star"]
        == str(OLD_TAIL_TARGET)
        and mask["row"]["B_remaining"] == str(B_REMAINING_BEFORE),
        "old M2b gate drift",
    )


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("packet-note", NOTE_REL, "proof, owner splice, and scope"),
        source_binding("packet-readme", README_REL, "replay and guardrails"),
        source_binding("packet-python", PYTHON_REL, "strict certificate and arithmetic"),
        source_binding("packet-sage", SAGE_REL, "independent extension-field control"),
        source_binding("sp3-theorem", THRESHOLDS_REL, "exact per-received-pair sparsification"),
        source_binding("first-match-source", GRANDE_REL, "global first-match disjointness"),
        source_binding("zero-pencil-note", ZERO_NOTE_REL, "zero witness tangent inclusion"),
        source_binding("zero-pencil-certificate", ZERO_CERT_REL, "proved local projection contract"),
        source_binding("zero-pencil-verifier", ZERO_SCRIPT_REL, "predecessor replay"),
        source_binding("readiness-certificate", READINESS_CERT_REL, "same-selector readiness boundary"),
        source_binding("readiness-verifier", READINESS_SCRIPT_REL, "predecessor readiness replay"),
        source_binding("sparse-tangent-note", SPARSE_NOTE_REL, "conditional tangent cell"),
        source_binding("base-owner-note", BASE_NOTE_REL, "distinct-slope global-once semantics"),
        source_binding("base-owner-certificate", BASE_CERT_REL, "tangent-before-base order"),
        source_binding("low-carrier-certificate", LOW_CARRIER_CERT_REL, "kappa<=10 terminal"),
        source_binding(
            "rank3-certificate",
            TDD_CERT_REL,
            "small-family and rank-at-most-three terminals",
        ),
        source_binding("rank-ladder-certificate", RANK_CERT_REL, "ranks four through nine"),
        source_binding("mask-deficit-certificate", MASK_CERT_REL, "old sharp one-cut gate"),
        source_binding("mask-deficit-verifier", MASK_SCRIPT_REL, "M2b compiler formulas"),
        source_binding("rich-pencil-note", RICH_NOTE_REL, "atlas excess conversion"),
    ]


def expected_certificate() -> dict[str, Any]:
    validate_predecessors()
    full_coarse_cap = coarse_cap(N, 1)
    paid_coarse_cap = coarse_cap(AUDITED_PAID_CARRIER, 1)
    require(
        paid_coarse_cap == EXPECTED_AUDITED_PAID_COARSE_CAP
        and paid_coarse_cap <= B_REMAINING_BEFORE,
        "audited predecessor-paid coarse cell drift",
    )
    try:
        one_cut_gate(
            B_REMAINING_BEFORE,
            AUDITED_PAID_CUTOFF,
            AUDITED_PAID_CARRIER,
            1,
        )
    except VerificationError as exc:
        require(
            str(exc)
            == "one-cut gate is only defined on predecessor coarse-failure cells",
            "audited paid cell rejected before the coarse-failure guard",
        )
    else:
        raise VerificationError("one-cut helper accepted a predecessor-paid cell")
    old_gate = one_cut_gate(B_REMAINING_BEFORE, CUTOFF_D, N, 1)
    new_gate = one_cut_gate(B_REMAINING_AFTER, CUTOFF_D, N, 1)
    require(
        old_gate["predecessor_coarse_cap"]
        == new_gate["predecessor_coarse_cap"]
        == str(full_coarse_cap),
        "predecessor coarse cap drift",
    )
    old_tail = int(old_gate["largest_sufficient_low_deficit_cap_T_star"])
    new_tail = int(new_gate["largest_sufficient_low_deficit_cap_T_star"])
    require(old_tail == OLD_TAIL_TARGET, "old tail target did not replay")
    require(new_tail == EXPECTED_NEW_TAIL_TARGET, "new tail target drift")
    new_e_max = aggregate_excess_max(new_tail)
    require(new_e_max == EXPECTED_NEW_E_MAX, "new aggregate excess drift")
    k_before = exact_k_remaining(B_REMAINING_BEFORE)
    k_after = exact_k_remaining(B_REMAINING_AFTER)
    require(
        k_before == k_after == EXPECTED_K_REMAINING,
        "exact remaining multiplier drift",
    )

    fixture = toy_fixture()
    replay = analyze_toy(fixture)
    require(
        carrier_size({0: [0, 11, 12]}, [0], 11) == 1,
        "carrier support did not normalize entries modulo the field",
    )
    require(
        replay["tangent_image"] == [1, 2]
        and replay["tangent_ratio_histogram"] == {"1": 3, "2": 3}
        and replay["incoming_residual"] == [0, 2, 3, 4]
        and replay["tangent_cell"] == [2]
        and replay["outgoing_residual"] == [0, 3, 4]
        and replay["later_base_cell"] == [0, 3]
        and replay["incoming_affine_rank"] == 3
        and replay["outgoing_affine_rank"] == 2
        and replay["incoming_kappa"] == 2
        and replay["outgoing_kappa"] == 1,
        "canonical toy replay drift",
    )

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "deployed_row": {
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "q_line": str(Q_LINE),
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "t": DELTA_ZERO,
            "B_star": str(B_STAR),
        },
        "counted_object_contract": {
            "object": "distinct support-wise MCA-bad finite slopes of one received pair",
            "global_once_means": "one uniform charge inside the maximum over received pairs",
            "cross_received_pair_union_required": False,
            "witness_support_coordinate_selector_counts_forbidden": True,
            "sp3_one_translation_fixed_for_entire_received_pair": True,
            "alternative_translation_union_forbidden": True,
        },
        "global_tangent_owner": {
            "owner_id": "sparse_tangent_slope_image",
            "parent_first_match_cell": "tangent_common_line_residue",
            "fixed_translation": "(epsilon_0,epsilon_1)",
            "source_support": "Sigma=supp(epsilon_0) UNION supp(epsilon_1)",
            "source_support_cap": J,
            "tangent_image": "{-epsilon_0(x)/epsilon_1(x):x in Sigma,epsilon_1(x)!=0}",
            "image_is_set_not_multiset": True,
            "assigned_cell": "Z_tan=Gamma_in INTERSECT tangent_image",
            "outgoing_cell": "Gamma_out=Gamma_in SETMINUS Z_tan",
            "uniform_cap": J,
            "charge_scope": "FIRST_MATCH_GLOBAL_ONCE_PER_RECEIVED_PAIR",
            "zero_pencil_subset_absorbed": True,
            "zero_pencil_separate_charge": 0,
            "pays_all_common_or_residue_lines": False,
        },
        "first_match_partition": {
            "order": FIRST_MATCH_ORDER,
            "tangent_index_one_based": FIRST_MATCH_ORDER.index(
                "tangent_common_line_residue"
            )
            + 1,
            "base_index_one_based": FIRST_MATCH_ORDER.index(
                "residual_base_slope_universe"
            )
            + 1,
            "incoming_exact_residual_required": True,
            "earlier_owner_intersection_removed": True,
            "later_owners_receive_exact_set_difference": True,
            "tangent_base_double_charge_forbidden": True,
            "later_uniform_caps_valid_on_smaller_residual": True,
        },
        "residual_selector_contract": {
            "selector_restriction_certifies_nonempty_new_selector_universe": True,
            "old_rank9_selector_restricts_to_rank_at_most_9": True,
            "rank_at_least_10_can_be_new_minimum": False,
            "complete_selector_universe_must_be_rebuilt": True,
            "global_carrier_gate_must_be_rerun": True,
            "affine_rank_minimizer_must_be_recomputed": True,
            "stale_fields_forbidden": [
                "carrier",
                "V",
                "H_V",
                "K_0",
                "d_V",
                "deficits",
                "rich_line_atlas",
            ],
            "surviving_zero_explaining_witness_forbidden": True,
            "surviving_zero_rich_pencil_forbidden": True,
            "same_sp3_translation_required_downstream": True,
        },
        "owner_restart": {
            "order": RESTART_ORDER,
            "empty_and_singleton_affine_rank": 0,
            "global_carrier_checked_first": True,
            "low_carrier_cap": str(LOW_CARRIER_CAP),
            "low_carrier_post_charge_total": str(U_PAID_AFTER + LOW_CARRIER_CAP),
            "low_carrier_post_charge_margin": str(
                B_STAR - U_PAID_AFTER - LOW_CARRIER_CAP
            ),
            "small_family_cap": SMALL_FAMILY_CAP,
            "small_family_terminal_applies_only_after_high_carrier": True,
            "small_family_post_charge_total": str(
                U_PAID_AFTER + SMALL_FAMILY_CAP
            ),
            "small_family_post_charge_margin": str(
                B_STAR - U_PAID_AFTER - SMALL_FAMILY_CAP
            ),
            "family_gt_15_gets_fresh_rank_minimizing_selector": True,
            "rank_le_3_cap": str(RANK_LE_3_CAP),
            "rank_le_3_post_charge_total": str(U_PAID_AFTER + RANK_LE_3_CAP),
            "rank_le_3_post_charge_margin": str(
                B_STAR - U_PAID_AFTER - RANK_LE_3_CAP
            ),
            "rank_4_to_8_cap": str(RANK_4_TO_8_CAP),
            "rank_4_to_8_post_charge_total": str(U_PAID_AFTER + RANK_4_TO_8_CAP),
            "rank_4_to_8_post_charge_margin": str(
                B_STAR - U_PAID_AFTER - RANK_4_TO_8_CAP
            ),
            "rank_caps_are_alternatives_not_sum": True,
            "rank9_coarse_gate_must_be_replayed": True,
            "rank9_paid_coarse_cells_exit_before_one_cut": True,
            "rank9_full_carrier_d1_coarse_cap": str(full_coarse_cap),
            "rank9_full_carrier_d1_coarse_cap_exceeds_post_charge_budget": (
                full_coarse_cap > B_REMAINING_AFTER
            ),
            "rank9_requires_nonzero_pencil_atlas": True,
        },
        "rank9_updated_gate": {
            "cutoff_D": CUTOFF_D,
            "old_gate": old_gate,
            "new_gate": new_gate,
            "old_tail_target": str(old_tail),
            "new_tail_target": str(new_tail),
            "tail_target_drop": str(old_tail - new_tail),
            "naive_old_tail_minus_j": str(old_tail - J),
            "naive_threshold_too_large_by": str((old_tail - J) - new_tail),
            "naive_subtraction_valid_after_reselection": False,
            "new_aggregate_excess_max": str(new_e_max),
            "aggregate_excess_formula": "(T_star+1)C(t+8,8)-20C(n,8)-1",
        },
        "toy_fixture": fixture,
        "toy_replay": replay,
        "ledger": {
            "U_paid_before": str(U_PAID_BEFORE),
            "tangent_charge": str(TANGENT_CHARGE),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "K_remaining_before": k_before,
            "K_remaining_after": k_after,
            "ledger_movement": str(TANGENT_CHARGE),
            "U_Q": None,
            "U_A": None,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "scope_guards": {
            "global_tangent_owner_proved": True,
            "selector_restart_splice_proved": True,
            "zero_pencil_absorbed": True,
            "nonzero_plant_load_bound_proved": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": NONCLAIMS,
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def verify_semantics(value: dict[str, Any]) -> None:
    require(set(value) == TOP_KEYS, "top-level key set drift")
    require(value.get("schema") == SCHEMA, "schema drift")
    require(value.get("artifact_kind") == ARTIFACT_KIND, "artifact kind drift")
    require(value.get("status") == STATUS, "status drift")
    require(value.get("payload_sha256") == payload_hash(value), "payload hash mismatch")

    row = value["deployed_row"]
    for key in ("p", "extension_degree", "n", "k", "A", "R", "j", "t"):
        exact_int(row[key], f"deployed_row.{key}")
    exact_int(value["global_tangent_owner"]["source_support_cap"], "source cap")
    exact_int(value["global_tangent_owner"]["uniform_cap"], "owner cap")
    exact_int(value["global_tangent_owner"]["zero_pencil_separate_charge"], "zero charge")
    exact_int(value["first_match_partition"]["tangent_index_one_based"], "tangent index")
    exact_int(value["first_match_partition"]["base_index_one_based"], "base index")
    exact_int(value["owner_restart"]["empty_and_singleton_affine_rank"], "rank convention")
    exact_int(value["owner_restart"]["small_family_cap"], "small-family cap")
    require(
        value["toy_replay"] == analyze_toy(value["toy_fixture"]),
        "toy replay drift",
    )

    expected = expected_certificate()
    require(
        canonical_bytes(value) == canonical_bytes(expected),
        "certificate semantic or source-binding drift",
    )


def run_check() -> None:
    value = load_json(CERT_PATH)
    verify_semantics(value)
    print("M1 KoalaBear tangent first-match owner splice: PASS")
    print(f"  tangent charge: {TANGENT_CHARGE:,} slopes (global once per received pair)")
    print(f"  U_paid: {U_PAID_BEFORE:,} -> {U_PAID_AFTER:,}")
    print(f"  B_remaining: {B_REMAINING_BEFORE:,} -> {B_REMAINING_AFTER:,}")
    print(f"  rebuilt rank-nine T_{CUTOFF_D}: {EXPECTED_NEW_TAIL_TARGET:,}")
    print("  nonzero rank-nine incidence: OPEN; KoalaBear row remains YELLOW")


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-mutated")),
        ("kind", lambda d: d.__setitem__("artifact_kind", "ROW_CLOSURE")),
        ("status", lambda d: d.__setitem__("status", "KOALABEAR_CLOSED")),
        ("row-A", lambda d: d["deployed_row"].__setitem__("A", A - 1)),
        ("row-q", lambda d: d["deployed_row"].__setitem__("q_line", str(P**5))),
        ("count-supports", lambda d: d["counted_object_contract"].__setitem__("object", "supports")),
        ("cross-pair-union", lambda d: d["counted_object_contract"].__setitem__("cross_received_pair_union_required", True)),
        ("multiple-translations", lambda d: d["counted_object_contract"].__setitem__("alternative_translation_union_forbidden", False)),
        ("not-fixed", lambda d: d["counted_object_contract"].__setitem__("sp3_one_translation_fixed_for_entire_received_pair", False)),
        ("multiset", lambda d: d["global_tangent_owner"].__setitem__("image_is_set_not_multiset", False)),
        ("per-selector-charge", lambda d: d["global_tangent_owner"].__setitem__("charge_scope", "PER_SELECTOR")),
        ("charge-cap", lambda d: d["global_tangent_owner"].__setitem__("uniform_cap", J + 1)),
        ("zero-double-charge", lambda d: d["global_tangent_owner"].__setitem__("zero_pencil_separate_charge", 1)),
        ("all-common-lines", lambda d: d["global_tangent_owner"].__setitem__("pays_all_common_or_residue_lines", True)),
        ("owner-order", lambda d: d["first_match_partition"]["order"].__setitem__(2, "residual_base_slope_universe")),
        ("base-before-tangent", lambda d: d["first_match_partition"].__setitem__("base_index_one_based", 2)),
        ("earlier-overlap", lambda d: d["first_match_partition"].__setitem__("earlier_owner_intersection_removed", False)),
        ("base-double-charge", lambda d: d["first_match_partition"].__setitem__("tangent_base_double_charge_forbidden", False)),
        ("not-exact-difference", lambda d: d["first_match_partition"].__setitem__("later_owners_receive_exact_set_difference", False)),
        ("reuse-selector", lambda d: d["residual_selector_contract"].__setitem__("complete_selector_universe_must_be_rebuilt", False)),
        ("skip-carrier", lambda d: d["residual_selector_contract"].__setitem__("global_carrier_gate_must_be_rerun", False)),
        ("stale-rank", lambda d: d["residual_selector_contract"].__setitem__("affine_rank_minimizer_must_be_recomputed", False)),
        ("rank10", lambda d: d["residual_selector_contract"].__setitem__("rank_at_least_10_can_be_new_minimum", True)),
        ("stale-HV", lambda d: d["residual_selector_contract"]["stale_fields_forbidden"].remove("H_V")),
        ("zero-survives", lambda d: d["residual_selector_contract"].__setitem__("surviving_zero_explaining_witness_forbidden", False)),
        ("translation-mismatch", lambda d: d["residual_selector_contract"].__setitem__("same_sp3_translation_required_downstream", False)),
        ("restart-order", lambda d: d["owner_restart"]["order"].reverse()),
        ("rank-sum", lambda d: d["owner_restart"].__setitem__("rank_caps_are_alternatives_not_sum", False)),
        ("carrier-not-first", lambda d: d["owner_restart"].__setitem__("global_carrier_checked_first", False)),
        ("low-cap", lambda d: d["owner_restart"].__setitem__("low_carrier_cap", str(LOW_CARRIER_CAP + 1))),
        ("small-family-cap", lambda d: d["owner_restart"].__setitem__("small_family_cap", SMALL_FAMILY_CAP - 1)),
        ("small-family-order", lambda d: d["owner_restart"].__setitem__("small_family_terminal_applies_only_after_high_carrier", False)),
        ("fresh-rank-after-15", lambda d: d["owner_restart"].__setitem__("family_gt_15_gets_fresh_rank_minimizing_selector", False)),
        ("rank8-cap", lambda d: d["owner_restart"].__setitem__("rank_4_to_8_cap", str(RANK_4_TO_8_CAP + 1))),
        ("skip-rank9-coarse", lambda d: d["owner_restart"].__setitem__("rank9_coarse_gate_must_be_replayed", False)),
        ("old-budget", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_BEFORE))),
        ("wrong-U", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("double-subtract", lambda d: d["ledger"].__setitem__("ledger_movement", str(2 * J))),
        ("K-rem", lambda d: d["ledger"].__setitem__("K_remaining_after", EXPECTED_K_REMAINING - 1)),
        ("UQ", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("old-tail", lambda d: d["rank9_updated_gate"].__setitem__("new_tail_target", str(OLD_TAIL_TARGET))),
        ("naive-tail", lambda d: d["rank9_updated_gate"].__setitem__("new_tail_target", str(OLD_TAIL_TARGET - J))),
        ("tail-plus-one", lambda d: d["rank9_updated_gate"].__setitem__("new_tail_target", str(EXPECTED_NEW_TAIL_TARGET + 1))),
        ("old-Emax", lambda d: d["rank9_updated_gate"].__setitem__("new_aggregate_excess_max", str(aggregate_excess_max(OLD_TAIL_TARGET)))),
        ("Emax-off-one", lambda d: d["rank9_updated_gate"].__setitem__("new_aggregate_excess_max", str(EXPECTED_NEW_E_MAX + 1))),
        ("D-plus-one", lambda d: d["rank9_updated_gate"].__setitem__("cutoff_D", CUTOFF_D + 1)),
        ("coarse-failure", lambda d: d["rank9_updated_gate"]["new_gate"].__setitem__("predecessor_coarse_failure_required", False)),
        ("naive-valid", lambda d: d["rank9_updated_gate"].__setitem__("naive_subtraction_valid_after_reselection", True)),
        ("toy-duplicate-bad", lambda d: d["toy_fixture"]["bad_slopes"].append(0)),
        ("toy-source", lambda d: d["toy_fixture"]["epsilon_0"].__setitem__(0, 9)),
        ("toy-over-j", lambda d: d["toy_fixture"].__setitem__("j", 5)),
        ("toy-zero-escape", lambda d: d["toy_fixture"]["zero_witness_slopes"].append(3)),
        ("toy-selector-missing", lambda d: d["toy_fixture"]["selector_records"].pop()),
        ("toy-selector-rank", lambda d: d["toy_fixture"]["selector_records"][1]["error"].__setitem__(1, 0)),
        ("toy-replay", lambda d: d["toy_replay"].__setitem__("outgoing_affine_rank", 3)),
        ("global-proof", lambda d: d["scope_guards"].__setitem__("nonzero_plant_load_bound_proved", True)),
        ("closure", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("rank10-authorized", lambda d: d["scope_guards"].__setitem__("rank_at_least_ten_authorized", True)),
        ("lean", lambda d: d["scope_guards"].__setitem__("lean_authorized", True)),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
        ("bool-int", lambda d: d["deployed_row"].__setitem__("n", True)),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("source-path", lambda d: d["source_bindings"][0].__setitem__("path", d["source_bindings"][1]["path"])),
        ("duplicate-binding", lambda d: d["source_bindings"][1].__setitem__("binding_id", d["source_bindings"][0]["binding_id"])),
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
        except (VerificationError, KeyError, ValueError):
            passed += 1
        else:
            raise VerificationError(f"semantic mutation survived: {label}")

    parser_cases = [
        ('{"schema":"x","schema":"y"}', "duplicate-key"),
        ('{"x":1.25}', "float"),
        ('{"x":NaN}', "nan"),
        ('{"x":Infinity}', "infinity"),
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
    print(f"M1 tangent-owner splice mutations: {passed}/{expected} PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check:
        run_check()
    elif args.tamper_selftest:
        run_tamper_selftest()
    elif args.write:
        CERT_PATH.write_text(
            json.dumps(expected_certificate(), sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        print(json.dumps(expected_certificate(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
