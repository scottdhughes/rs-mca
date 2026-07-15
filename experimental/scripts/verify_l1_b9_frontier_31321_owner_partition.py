#!/usr/bin/env python3
"""Exact existing-owner partition for the GF(19) ``(3,1,3,(3,2,1))`` frontier.

The frozen sequential sunflower has

    (p,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2).

The three labelled petals receive the distinct support sizes 3, 2, and 1 in
all six possible orders.  Together with the retained background point this
gives

    binom(2,1) * 3! * binom(4,3) * binom(4,2) * binom(4,1) = 1,152

canonical cofactor-support keys.  Each key has four restored-core refinements,
for 4,608 full-support records.

Apply exactly one first-match aggregate status in this order:

    periodic support count,
    invariant quotient descent,
    fixed-(D,R0) auxiliary Johnson,
    global Johnson,
    B11 G2,
    B11 GR,
    UNPAID_PRIMITIVE.

Twelve full-support refinements are periodic, in twelve distinct aggregate
keys.  The selected seven-point cofactor support is aperiodic in every key.
The existing cofactor injection has not been split into disjoint charges by
restored core point, so none of the twelve aggregate keys is paid by the
refinement-level periodic owner.  Quotient descent fails closed because no
uniform witness-data descent certificate is supplied.  The auxiliary Johnson
margin is exactly zero, global Johnson has lambda=0<lambda_J=1, and B11
escapes.  Thus all 1,152 aggregate keys terminate as ``UNPAID_PRIMITIVE``.

That terminal label is relative only to the frozen existing-owner stack.  It
does not assert full algebraic primitivity and makes no reduced-CRT claim.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "experimental/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    b11_frontier_record,
    classify_b11_box,
    johnson_slack_needed,
    stabilizer_order,
)


CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31321-owner-partition/certificate.json"
)
PREVIOUS_LEDGER_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-d4r0-shared-auxiliary/ledger_certificate.json"
)

P = 19
N = 18
K = 5
SIGMA = 3
ELL = 4
S = K + SIGMA
CORE = tuple(range(4))
PETALS = (
    tuple(range(4, 8)),
    tuple(range(8, 12)),
    tuple(range(12, 16)),
)
BACKGROUND = tuple(range(16, 18))
PETAL_SIZE_MULTISET = (3, 2, 1)
PROFILE = {
    "ell": 4,
    "d": 3,
    "r": 1,
    "t": 3,
    "a_i": [3, 2, 1],
    "G2": 3,
    "GR": 4,
    "lambda": 0,
    "lambda_J": 1,
}
OWNER_ORDER = (
    "PAID_PERIODIC_SUPPORT_COUNT",
    "PAID_INVARIANT_QUOTIENT_DESCENT",
    "PAID_AUXILIARY_JOHNSON",
    "PAID_GLOBAL_JOHNSON",
    "PAID_B11_G2",
    "PAID_B11_GR",
    "UNPAID_PRIMITIVE",
)


def sha256_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_certificate_json(report: dict[str, object]) -> str:
    """Pretty-print metadata while keeping each complete key on one line."""
    marker = "__RS_MCA_CANONICAL_31321_PATTERN_ROWS__"
    rows = report["patterns"]
    compact = copy.deepcopy(report)
    compact["patterns"] = marker
    rendered = json.dumps(compact, indent=2, sort_keys=True)
    needle = f'  "patterns": "{marker}"'
    if rendered.count(needle) != 1:
        raise RuntimeError("hybrid certificate marker drift")
    row_block = (
        '  "patterns": [\n'
        + ",\n".join(
            "    " + json.dumps(row, sort_keys=True, separators=(",", ":"))
            for row in rows
        )
        + "\n  ]"
    )
    rendered = rendered.replace(needle, row_block) + "\n"
    if json.loads(rendered) != report:
        raise RuntimeError("hybrid certificate round-trip failed")
    return rendered


def mask_from_indices(indices: tuple[int, ...]) -> int:
    return sum(1 << index for index in indices)


def shifted_mask(mask: int, shift: int) -> int:
    output = 0
    for index in range(N):
        if mask & (1 << index):
            output |= 1 << ((index + shift) % N)
    return output


def quotient_scales(mask: int) -> list[int]:
    """Return nontrivial uniform fibre sizes fixed by the cyclic action."""
    scales = []
    for scale in range(2, N + 1):
        if N % scale:
            continue
        if shifted_mask(mask, N // scale) == mask:
            scales.append(scale)
    return scales


def owner_from_gates(gates: dict[str, object]) -> str:
    if bool(gates["periodicity"]["paid"]):
        return "PAID_PERIODIC_SUPPORT_COUNT"
    if bool(gates["quotient_descent"]["paid"]):
        return "PAID_INVARIANT_QUOTIENT_DESCENT"
    if bool(gates["auxiliary_johnson"]["paid"]):
        return "PAID_AUXILIARY_JOHNSON"
    if bool(gates["global_johnson"]["paid"]):
        return "PAID_GLOBAL_JOHNSON"
    box = str(gates["b11"]["classification"])
    if box == "PAID_G2":
        return "PAID_B11_G2"
    if box == "PAID_GR":
        return "PAID_B11_GR"
    return "UNPAID_PRIMITIVE"


def expected_support_assignments() -> list[
    tuple[
        tuple[int, ...],
        tuple[int, ...],
        tuple[tuple[int, ...], ...],
    ]
]:
    assignments = []
    for petal_sizes in itertools.permutations(PETAL_SIZE_MULTISET):
        support_choices = [
            tuple(itertools.combinations(petal, size))
            for petal, size in zip(PETALS, petal_sizes)
        ]
        for background_support in itertools.combinations(BACKGROUND, 1):
            for supports in itertools.product(*support_choices):
                assignments.append((petal_sizes, background_support, tuple(supports)))
    return assignments


def canonical_assignment(
    petal_sizes: tuple[int, ...],
    background_support: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    selected = tuple(sorted(background_support + sum(supports, ())))
    return {
        "petal_size_assignment": list(petal_sizes),
        "background_support": list(background_support),
        "petal_supports": [list(support) for support in supports],
        "selected_cofactor_support": list(selected),
        "selected_cofactor_support_mask": mask_from_indices(selected),
    }


def pattern_record(
    petal_sizes: tuple[int, ...],
    background_support: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    selected = tuple(sorted(background_support + sum(supports, ())))
    selected_mask = mask_from_indices(selected)
    selected_scales = quotient_scales(selected_mask)
    refinements = []
    for core_hit in CORE:
        full_support = tuple(sorted(selected + (core_hit,)))
        full_mask = mask_from_indices(full_support)
        scales = quotient_scales(full_mask)
        refinements.append(
            {
                "core_hit": core_hit,
                "full_agreement_support": list(full_support),
                "full_agreement_mask": full_mask,
                "stabilizer_order": stabilizer_order(full_mask, N),
                "complete_fibre_scales": scales,
                "support_periodic": bool(scales),
                "periodic_support_count_certificate": bool(scales),
                "witness_data_descent_certificate": False,
                "owner": (
                    "PAID_PERIODIC_SUPPORT_COUNT"
                    if scales
                    else "UNPAID_AFTER_PERIODICITY"
                ),
                "owner_bound": 1 if scales else None,
                "paid": bool(scales),
            }
        )
    periodic_refinements = [row for row in refinements if row["support_periodic"]]
    stabilizer_histogram = Counter(str(row["stabilizer_order"]) for row in refinements)
    lambda_j = johnson_slack_needed(N, K, S)
    b11 = b11_frontier_record(
        ell=ELL,
        petal_count=len(PETALS),
        d=3,
        r=1,
        a_i=list(PETAL_SIZE_MULTISET),
        agreement_slack=0,
        lambda_j=lambda_j,
        maximal=True,
    )
    box = classify_b11_box(b11, E=0, V2=0, VR=0)
    auxiliary = b11["auxiliary_johnson"]
    gates: dict[str, object] = {
        "periodicity": {
            "selected_cofactor_support_stabilizer_order": stabilizer_order(
                selected_mask, N
            ),
            "selected_cofactor_complete_fibre_scales": selected_scales,
            "selected_cofactor_support_aperiodic": not selected_scales,
            "restored_core_refinement_count": len(refinements),
            "full_support_stabilizer_histogram": dict(
                sorted(stabilizer_histogram.items())
            ),
            "periodic_refinement_count": len(periodic_refinements),
            "periodic_core_hits": [row["core_hit"] for row in periodic_refinements],
            "paid_periodic_refinement_count": len(periodic_refinements),
            "periodic_support_owner_bound": len(periodic_refinements),
            "aggregate_pattern_paid": False,
            "status": (
                "MIXED_PAID_PERIODIC_AND_UNPAID_REFINEMENTS"
                if periodic_refinements
                else "NO_PERIODIC_FULL_SUPPORT_REFINEMENT"
            ),
            "paid": False,
        },
        "quotient_descent": {
            "candidate_uniform_fibre_scales": [2, 3, 6, 9, 18],
            "periodic_refinements_removed_at_prior_owner": len(
                periodic_refinements
            ),
            "remaining_aperiodic_refinement_count": len(refinements)
            - len(periodic_refinements),
            "data_certified_refinement_count": 0,
            "all_witness_data_descend": False,
            "data_gate_status": "FAIL_CLOSED_NO_UNIFORM_DATA_DESCENT_CERTIFICATE",
            "paid": False,
        },
        "auxiliary_johnson": {
            "required_agreement": int(auxiliary["required_agreement"]),
            "petal_domain_size": int(auxiliary["petal_domain_size"]),
            "effective_degree_bound": int(auxiliary["effective_degree_bound"]),
            "margin": int(auxiliary["margin"]),
            "paid": bool(auxiliary["paid"]),
        },
        "global_johnson": {
            "lambda": 0,
            "lambda_J": lambda_j,
            "strict_inequality": 0 < lambda_j,
            "paid": 0 >= lambda_j,
        },
        "b11": {
            "E": 0,
            "V2": 0,
            "VR": 0,
            "d_minus_ell": int(b11["d_minus_ell"]),
            "G2": int(b11["G2"]),
            "GR": int(b11["GR"]),
            "classification": box,
        },
    }
    owner = owner_from_gates(gates)
    return {
        "pattern_id": (
            "z"
            + ".".join(map(str, petal_sizes))
            + f"-b{background_support[0]}-"
            + "-".join("s" + ".".join(map(str, support)) for support in supports)
        ),
        "petal_size_assignment": list(petal_sizes),
        "background_support": list(background_support),
        "petal_supports": [list(support) for support in supports],
        "selected_cofactor_support": list(selected),
        "selected_cofactor_support_mask": selected_mask,
        "selected_cofactor_support_size": len(selected),
        "restored_core_refinements": refinements,
        "profile": dict(PROFILE),
        "gates": gates,
        "owner_order": list(OWNER_ORDER),
        "owner": owner,
        "terminal_status_scope": (
            "aggregate cofactor-support key remains unpaid under the named "
            "existing-owner stack; this is not a full primitivity certificate"
        ),
    }


def previous_ledger_record() -> dict[str, object]:
    previous = json.loads(PREVIOUS_LEDGER_PATH.read_text(encoding="utf-8"))
    candidate = previous["ledger_consequence"]["candidate_result"]
    target = candidate["largest_remaining_unresolved_profile"]
    expected_target = {
        "ell": 4,
        "d": 3,
        "r": 1,
        "t": 3,
        "a_i": [3, 2, 1],
        "d_minus_ell": -1,
        "G2": 3,
        "GR": 4,
        "lambda": 0,
        "lambda_J": 1,
        "lambda_minus_lambda_J": -1,
        "support_pattern_count": 1_152,
        "refined_injection_exponent": 1,
        "refined_injection_bound": 21_888,
        "b11_box_route": "ESCAPES_BOUNDED_EXCESS_BOX",
    }
    if (
        previous["schema"]
        != "rs-mca-l1-b9-d4r0-shared-auxiliary-ledger-v1"
        or previous["status"]
        != "EXACT_D4R0_SHARED_ENVELOPE_REPLAY_FRESH_REVIEWS_GREEN"
        or previous["verdict"]
        != "GREEN_LOCAL_D4R0_SHARED_AUXILIARY_LEDGER_BANKED"
        or previous["ledger_consequence"]["banked"] is not True
        or candidate["all_profile_bound"] != 641_512
        or candidate["unresolved_bound"] != 104_914
        or target != expected_target
    ):
        raise RuntimeError("banked d4r0 ledger linkage drift")
    return {
        "path": str(PREVIOUS_LEDGER_PATH.relative_to(ROOT)),
        "sha256": sha256_file(PREVIOUS_LEDGER_PATH),
        "schema": previous["schema"],
        "status": previous["status"],
        "verdict": previous["verdict"],
        "banked": True,
        "all_profile_bound": int(candidate["all_profile_bound"]),
        "unresolved_bound": int(candidate["unresolved_bound"]),
        "target": expected_target,
    }


def build_report() -> dict[str, object]:
    patterns = [
        pattern_record(petal_sizes, background_support, supports)
        for petal_sizes, background_support, supports in expected_support_assignments()
    ]
    owner_histogram = Counter(str(row["owner"]) for row in patterns)
    refinements = [
        refinement
        for pattern in patterns
        for refinement in pattern["restored_core_refinements"]
    ]
    periodic_refinements = [row for row in refinements if row["support_periodic"]]
    refinement_owner_histogram = Counter(str(row["owner"]) for row in refinements)
    patterns_with_periodic_refinement = sum(
        bool(pattern["gates"]["periodicity"]["periodic_refinement_count"])
        for pattern in patterns
    )
    previous = previous_ledger_record()
    unpaid_count = int(owner_histogram["UNPAID_PRIMITIVE"])
    residual_charge = unpaid_count * P
    paid_count = len(patterns) - unpaid_count
    paid_mass = 21_888 - residual_charge
    return {
        "schema": "rs-mca-l1-b9-frontier-31321-owner-partition-v1",
        "status": "AUDIT/EXACT_GF19_EXISTING_OWNER_PARTITION",
        "statement": (
            "assign exactly one first-match existing owner or UNPAID_PRIMITIVE "
            "to every canonical cofactor-support key in "
            "(ell,d,r,t,a_i)=(4,3,1,3,(3,2,1))"
        ),
        "input": {
            "p": P,
            "n": N,
            "k": K,
            "sigma": SIGMA,
            "ell": ELL,
            "core": list(CORE),
            "petals": [list(petal) for petal in PETALS],
            "background": list(BACKGROUND),
            "petal_size_multiset": list(PETAL_SIZE_MULTISET),
            "profile": dict(PROFILE),
            "owner_order": list(OWNER_ORDER),
            "b11_cuts": {"E": 0, "V2": 0, "VR": 0},
        },
        "previous_ledger": previous,
        "patterns": patterns,
        "result": {
            "support_pattern_formula": (
                "binom(2,1)*3!*binom(4,3)*binom(4,2)*binom(4,1)=1152"
            ),
            "support_pattern_count": len(patterns),
            "restored_core_refinement_count": len(refinements),
            "aperiodic_selected_cofactor_support_count": sum(
                row["gates"]["periodicity"][
                    "selected_cofactor_support_aperiodic"
                ]
                for row in patterns
            ),
            "periodic_full_support_refinement_count": len(periodic_refinements),
            "patterns_with_periodic_full_support_refinement": patterns_with_periodic_refinement,
            "paid_periodic_full_support_refinement_count": len(periodic_refinements),
            "periodic_support_owner_bound": len(periodic_refinements),
            "refinement_owner_histogram": dict(
                sorted(refinement_owner_histogram.items())
            ),
            "owner_histogram": dict(sorted(owner_histogram.items())),
            "paid_existing_owner_patterns": paid_count,
            "unpaid_primitive_patterns": unpaid_count,
            "transcript_sha256": sha256_json(patterns),
        },
        "ledger_consequence": {
            "old_profile_charge_formula": "1152*19=21888",
            "old_profile_charge": 21_888,
            "cofactor_injection_exponent": 1,
            "periodic_support_owner_bound": len(periodic_refinements),
            "why_periodic_bound_is_not_subtracted": (
                "the q cofactor injection is aggregate over four restored-core "
                "refinements and no disjoint per-core-hit cofactor charge has "
                "been proved"
            ),
            "paid_mass_removed": paid_mass,
            "residual_profile_charge": residual_charge,
            "old_all_profile_bound": previous["all_profile_bound"],
            "new_all_profile_bound": previous["all_profile_bound"] - paid_mass,
            "old_unresolved_bound": previous["unresolved_bound"],
            "new_unresolved_bound": previous["unresolved_bound"] - paid_mass,
        },
        "proof_status": {
            "exact": [
                "all 1,152 canonical labelled cofactor-support keys are enumerated",
                "all 4,608 restored-core full-support refinements are enumerated",
                "every selected seven-point cofactor support is aperiodic",
                "exactly twelve full-support refinements in twelve distinct keys are periodic",
                "none of the twelve aggregate keys is removed without a disjoint per-core-hit cofactor charge",
                "quotient descent fails closed without uniform witness-data descent",
                "the auxiliary Johnson margin is exactly zero",
                "global Johnson has lambda=0<lambda_J=1",
                "every key escapes B11 and terminates UNPAID_PRIMITIVE",
            ],
            "still_required": [
                "this owner partition alone does not classify the unpaid residual algebraically",
                "this owner partition alone does not authorize a reduced-CRT ledger charge",
            ],
        },
        "nonclaims": [
            "UNPAID_PRIMITIVE is relative to this existing-owner stack only",
            "UNPAID_PRIMITIVE is not a certificate of full primitivity",
            "the selected seven-point cofactor support is not the full eight-point agreement support",
            "periodic support counting is distinct from invariant quotient descent",
            "no restored-core refinement payment is promoted to an aggregate key payment",
            "no reduced-CRT, rank, planted, pencil, or saturation classification is made",
            "no m>2 or PR #763 statement is made",
        ],
        "verdict": (
            "YELLOW - all 1,152 aggregate keys survive the existing-owner stack; "
            "algebra is required."
        ),
    }


def validate_report(report: dict[str, object]) -> bool:
    patterns = report["patterns"]
    result = report["result"]
    ledger = report["ledger_consequence"]
    expected_assignments = [
        canonical_assignment(petal_sizes, background_support, supports)
        for petal_sizes, background_support, supports in expected_support_assignments()
    ]
    observed_assignments = [
        {
            "petal_size_assignment": list(row["petal_size_assignment"]),
            "background_support": list(row["background_support"]),
            "petal_supports": [list(support) for support in row["petal_supports"]],
            "selected_cofactor_support": list(row["selected_cofactor_support"]),
            "selected_cofactor_support_mask": int(
                row["selected_cofactor_support_mask"]
            ),
        }
        for row in patterns
    ]
    owner_histogram = Counter(str(row["owner"]) for row in patterns)
    ids = [str(row["pattern_id"]) for row in patterns]
    masks = [int(row["selected_cofactor_support_mask"]) for row in patterns]
    refinements = [
        refinement
        for row in patterns
        for refinement in row["restored_core_refinements"]
    ]
    periodic_refinements = [row for row in refinements if row["support_periodic"]]
    periodic_pattern_count = sum(
        bool(row["gates"]["periodicity"]["periodic_refinement_count"])
        for row in patterns
    )
    current_previous_hash = sha256_file(PREVIOUS_LEDGER_PATH)
    fixed_quotient_gate = {
        "candidate_uniform_fibre_scales": [2, 3, 6, 9, 18],
        "data_certified_refinement_count": 0,
        "all_witness_data_descend": False,
        "data_gate_status": "FAIL_CLOSED_NO_UNIFORM_DATA_DESCENT_CERTIFICATE",
        "paid": False,
    }
    return (
        report["schema"] == "rs-mca-l1-b9-frontier-31321-owner-partition-v1"
        and len(patterns) == 1_152
        and len(set(ids)) == 1_152
        and observed_assignments == expected_assignments
        and len(set(masks)) == 1_152
        and all(int(row["selected_cofactor_support_size"]) == 7 for row in patterns)
        and all(
            sorted(row["petal_size_assignment"], reverse=True) == [3, 2, 1]
            and [len(support) for support in row["petal_supports"]]
            == row["petal_size_assignment"]
            for row in patterns
        )
        and all(len(row["restored_core_refinements"]) == 4 for row in patterns)
        and all(
            [refinement["core_hit"] for refinement in row["restored_core_refinements"]]
            == list(CORE)
            for row in patterns
        )
        and all(row["profile"] == PROFILE for row in patterns)
        and all(row["owner_order"] == list(OWNER_ORDER) for row in patterns)
        and all(row["owner"] == owner_from_gates(row["gates"]) for row in patterns)
        and all(row["owner"] == "UNPAID_PRIMITIVE" for row in patterns)
        and all(
            row["gates"]["periodicity"][
                "selected_cofactor_support_stabilizer_order"
            ]
            == 1
            and row["gates"]["periodicity"][
                "selected_cofactor_complete_fibre_scales"
            ]
            == []
            and row["gates"]["periodicity"][
                "selected_cofactor_support_aperiodic"
            ]
            is True
            and row["gates"]["periodicity"]["aggregate_pattern_paid"] is False
            and row["gates"]["periodicity"]["paid"] is False
            and row["gates"]["periodicity"]["periodic_refinement_count"] <= 1
            for row in patterns
        )
        and len(refinements) == 4_608
        and len(periodic_refinements) == 12
        and periodic_pattern_count == 12
        and all(
            refinement["paid"] == refinement["support_periodic"]
            and refinement["periodic_support_count_certificate"]
            == refinement["support_periodic"]
            and refinement["witness_data_descent_certificate"] is False
            and refinement["owner_bound"]
            == (1 if refinement["support_periodic"] else None)
            for refinement in refinements
        )
        and all(
            all(row["gates"]["quotient_descent"][key] == value for key, value in fixed_quotient_gate.items())
            and row["gates"]["quotient_descent"][
                "periodic_refinements_removed_at_prior_owner"
            ]
            == row["gates"]["periodicity"]["periodic_refinement_count"]
            and row["gates"]["quotient_descent"][
                "remaining_aperiodic_refinement_count"
            ]
            == 4 - row["gates"]["periodicity"]["periodic_refinement_count"]
            for row in patterns
        )
        and all(
            row["gates"]["auxiliary_johnson"]
            == {
                "required_agreement": 6,
                "petal_domain_size": 12,
                "effective_degree_bound": 3,
                "margin": 0,
                "paid": False,
            }
            for row in patterns
        )
        and all(
            row["gates"]["global_johnson"]
            == {
                "lambda": 0,
                "lambda_J": 1,
                "strict_inequality": True,
                "paid": False,
            }
            for row in patterns
        )
        and all(
            row["gates"]["b11"]
            == {
                "E": 0,
                "V2": 0,
                "VR": 0,
                "d_minus_ell": -1,
                "G2": 3,
                "GR": 4,
                "classification": "ESCAPES_BOUNDED_EXCESS_BOX",
            }
            for row in patterns
        )
        and dict(sorted(owner_histogram.items())) == result["owner_histogram"]
        and result["owner_histogram"] == {"UNPAID_PRIMITIVE": 1_152}
        and int(result["support_pattern_count"]) == 1_152
        and int(result["restored_core_refinement_count"]) == 4_608
        and int(result["aperiodic_selected_cofactor_support_count"]) == 1_152
        and int(result["periodic_full_support_refinement_count"]) == 12
        and int(result["patterns_with_periodic_full_support_refinement"]) == 12
        and int(result["paid_periodic_full_support_refinement_count"]) == 12
        and int(result["periodic_support_owner_bound"]) == 12
        and result["refinement_owner_histogram"]
        == {"PAID_PERIODIC_SUPPORT_COUNT": 12, "UNPAID_AFTER_PERIODICITY": 4_596}
        and int(result["unpaid_primitive_patterns"]) == 1_152
        and int(result["paid_existing_owner_patterns"]) == 0
        and result["transcript_sha256"] == sha256_json(patterns)
        and report["previous_ledger"]["sha256"] == current_previous_hash
        and report["previous_ledger"]["banked"] is True
        and report["previous_ledger"]["all_profile_bound"] == 641_512
        and report["previous_ledger"]["unresolved_bound"] == 104_914
        and ledger["old_profile_charge_formula"] == "1152*19=21888"
        and int(ledger["old_profile_charge"]) == 21_888
        and int(ledger["cofactor_injection_exponent"]) == 1
        and int(ledger["periodic_support_owner_bound"]) == 12
        and int(ledger["paid_mass_removed"]) == 0
        and int(ledger["residual_profile_charge"]) == 21_888
        and int(ledger["old_all_profile_bound"]) == 641_512
        and int(ledger["new_all_profile_bound"]) == 641_512
        and int(ledger["old_unresolved_bound"]) == 104_914
        and int(ledger["new_unresolved_bound"]) == 104_914
    )


def tamper_selftest(report: dict[str, object]) -> int:
    mutations: list[tuple[str, dict[str, object]]] = []

    changed = copy.deepcopy(report)
    source = changed["patterns"][0]
    target = changed["patterns"][1]
    for field in (
        "petal_size_assignment",
        "background_support",
        "petal_supports",
        "selected_cofactor_support",
        "selected_cofactor_support_mask",
    ):
        target[field] = copy.deepcopy(source[field])
    target["pattern_id"] = "fresh-id-duplicate-assignment"
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("duplicate_assignment", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["owner_order"][0:2] = list(
        reversed(changed["patterns"][0]["owner_order"][0:2])
    )
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("owner_order", changed))

    changed = copy.deepcopy(report)
    changed["result"]["support_pattern_count"] = 1_151
    mutations.append(("support_pattern_count", changed))

    changed = copy.deepcopy(report)
    changed["result"]["restored_core_refinement_count"] = 4_607
    mutations.append(("refinement_count", changed))

    changed = copy.deepcopy(report)
    changed["result"]["periodic_full_support_refinement_count"] = 11
    mutations.append(("periodic_refinement_count", changed))

    changed = copy.deepcopy(report)
    changed["result"]["patterns_with_periodic_full_support_refinement"] = 11
    mutations.append(("periodic_key_count", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["gates"]["periodicity"][
        "selected_cofactor_support_aperiodic"
    ] = False
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("selected_aperiodicity", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["gates"]["auxiliary_johnson"]["margin"] = 1
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("auxiliary_margin", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["gates"]["quotient_descent"]["paid"] = True
    changed["patterns"][0]["owner"] = "PAID_INVARIANT_QUOTIENT_DESCENT"
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("quotient_paid", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["gates"]["quotient_descent"][
        "all_witness_data_descend"
    ] = True
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("quotient_data_gate", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["gates"]["global_johnson"]["lambda"] = 1
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("global_lambda", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["gates"]["b11"]["classification"] = "PAID_G2"
    changed["patterns"][0]["owner"] = "PAID_B11_G2"
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("b11_classification", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["owner"] = "PAID_PERIODIC_SUPPORT_COUNT"
    mutations.append(("terminal_owner", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["paid_mass_removed"] = 12
    changed["ledger_consequence"]["residual_profile_charge"] = 21_876
    mutations.append(("aggregate_charge", changed))

    changed = copy.deepcopy(report)
    changed["previous_ledger"]["sha256"] = "0" * 64
    mutations.append(("ledger_link", changed))

    changed = copy.deepcopy(report)
    changed["result"]["transcript_sha256"] = "0" * 64
    mutations.append(("transcript", changed))

    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<27}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (owner partition validation)", file=sys.stderr)
        return 1
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            render_certificate_json(report), encoding="utf-8"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != report:
        print("RESULT: FAIL (frozen owner certificate drift)", file=sys.stderr)
        return 1
    print("L1 B9 frontier (3,1,3,(3,2,1)) existing-owner partition")
    print(f"  cofactor-support keys: {report['result']['support_pattern_count']}")
    print(
        "  full-support refinements: "
        f"{report['result']['restored_core_refinement_count']} "
        f"({report['result']['paid_periodic_full_support_refinement_count']} "
        "periodic refinements in "
        f"{report['result']['patterns_with_periodic_full_support_refinement']} keys)"
    )
    print(f"  aggregate owner histogram: {report['result']['owner_histogram']}")
    print(
        "  ledger unchanged: unresolved "
        f"{report['ledger_consequence']['old_unresolved_bound']} -> "
        f"{report['ledger_consequence']['new_unresolved_bound']}"
    )
    print(f"  transcript: {report['result']['transcript_sha256']}")
    print(f"  proof status: {report['status']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
