#!/usr/bin/env python3
"""Exact existing-owner partition for the GF(19) ``(4,1,3,(3,3,1))`` row.

The frozen sequential sunflower has

    (p,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2).

There are

    binom(2,1) * 3 * binom(4,3)^2 * binom(4,1) = 384

canonical labelled patterns.  Since ``d=ell=4``, the missed core is the
entire four-point core: the selected eight-point cofactor support is already
the full agreement support, and there is no restored-core refinement.

Each pattern receives exactly one first-match status in the frozen order

    periodic support;
    invariant quotient descent;
    auxiliary Johnson;
    global Johnson;
    B11 G2;
    B11 GR;
    UNPAID_PRIMITIVE.

The one periodic pattern is recorded at the pattern level.  The bankable row
charge nevertheless remains the already-proved common fixed-(D,R0) auxiliary
Johnson envelope ``2 * 36 = 72``: that envelope covers the whole row,
including the periodic pattern.  Pattern counts, periodic owner bounds, and
the common layer envelope must not be added or multiplied together.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from math import comb
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
    / "experimental/data/certificates/l1-b9-frontier-41331-owner-partition/certificate.json"
)
PREVIOUS_LEDGER_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-32221/ledger_certificate.json"
)
COMMON_CAP_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-m2-full-rank-ledger/certificate.json"
)
SHARP_THEOREM_PATH = ROOT / "experimental/cap25_cap_v13_raw.tex"

P = 19
N = 18
K = 5
SIGMA = 3
ELL = 4
M = 3
BACKGROUND_SIZE = 2
S = K + SIGMA
CORE = tuple(range(4))
PETALS = (
    tuple(range(4, 8)),
    tuple(range(8, 12)),
    tuple(range(12, 16)),
)
BACKGROUND = tuple(range(16, 18))
PROFILE = {
    "ell": 4,
    "d": 4,
    "d_minus_ell": 0,
    "r": 1,
    "t": 3,
    "a_i": [3, 3, 1],
    "G2": 2,
    "GR": 4,
    "lambda": 0,
    "lambda_J": 1,
    "lambda_minus_lambda_J": -1,
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
OLD_PROFILE_CHARGE = 384 * P**2
COMMON_FIXED_LAYER_CAP = 72


def sha256_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_certificate_json(report: dict[str, object]) -> str:
    """Pretty-print metadata while keeping each full pattern on one line."""
    marker = "__RS_MCA_CANONICAL_PATTERN_ROWS__"
    rows = report["patterns"]
    compact = dict(report)
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
    """Return nontrivial uniform cyclic fibre sizes fixing the full support."""
    return [
        scale
        for scale in range(2, N + 1)
        if N % scale == 0 and shifted_mask(mask, N // scale) == mask
    ]


def canonical_key(
    background_support: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> list[object]:
    return [list(background_support), *[list(support) for support in supports]]


def expected_assignments() -> list[tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]]:
    rows = []
    for short_petal in range(len(PETALS)):
        occupancies = tuple(
            1 if label == short_petal else 3 for label in range(len(PETALS))
        )
        support_choices = [
            tuple(itertools.combinations(petal, occupancy))
            for petal, occupancy in zip(PETALS, occupancies, strict=True)
        ]
        for background_support in itertools.combinations(BACKGROUND, 1):
            for supports in itertools.product(*support_choices):
                rows.append((background_support, tuple(supports)))
    return rows


def uniform_gate_record() -> dict[str, object]:
    lambda_j = johnson_slack_needed(N, K, S)
    b11 = b11_frontier_record(
        ell=ELL,
        petal_count=M,
        d=4,
        r=1,
        a_i=[3, 3, 1],
        agreement_slack=0,
        lambda_j=lambda_j,
        maximal=True,
    )
    auxiliary = b11["auxiliary_johnson"]
    return {
        "auxiliary_johnson": {
            "required_agreement": int(auxiliary["required_agreement"]),
            "petal_domain_size": int(auxiliary["petal_domain_size"]),
            "effective_degree_bound": int(auxiliary["effective_degree_bound"]),
            "strict_johnson_margin": int(auxiliary["margin"]),
            "paid": bool(auxiliary["paid"]),
            "unique": bool(auxiliary["unique"]),
            "integer_floor_bound_per_fixed_D_R0": int(
                auxiliary["integer_floor_bound_per_fixed_D_R0"]
            ),
        },
        "global_johnson": {
            "lambda": 0,
            "lambda_J": lambda_j,
            "paid": 0 >= lambda_j,
        },
        "b11": {
            "E": 0,
            "V2": 0,
            "VR": 0,
            "d_minus_ell": int(b11["d_minus_ell"]),
            "G2": int(b11["G2"]),
            "GR": int(b11["GR"]),
            "classification": classify_b11_box(b11, E=0, V2=0, VR=0),
        },
    }


def first_match_owner(
    *, support_periodic: bool, quotient_paid: bool, gates: dict[str, object]
) -> str:
    candidates = {
        "PAID_PERIODIC_SUPPORT_COUNT": support_periodic,
        "PAID_INVARIANT_QUOTIENT_DESCENT": quotient_paid,
        "PAID_AUXILIARY_JOHNSON": bool(gates["auxiliary_johnson"]["paid"]),
        "PAID_GLOBAL_JOHNSON": bool(gates["global_johnson"]["paid"]),
        "PAID_B11_G2": gates["b11"]["classification"] == "PAID_G2",
        "PAID_B11_GR": gates["b11"]["classification"] == "PAID_GR",
        "UNPAID_PRIMITIVE": True,
    }
    return next(owner for owner in OWNER_ORDER if candidates[owner])


def pattern_record(
    background_support: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
    gates: dict[str, object],
) -> dict[str, object]:
    occupancies = tuple(len(support) for support in supports)
    short_petal = occupancies.index(1)
    selected = tuple(sorted(background_support + sum(supports, ())))
    selected_mask = mask_from_indices(selected)
    scales = quotient_scales(selected_mask)
    periodic = bool(scales)
    quotient_status = (
        "REMOVED_AT_PRIOR_PERIODIC_OWNER"
        if periodic
        else "NO_SUPPORT_INVARIANT_UNIFORM_FOLD"
    )
    owner = first_match_owner(
        support_periodic=periodic, quotient_paid=False, gates=gates
    )
    key = canonical_key(background_support, supports)
    return {
        "pattern_id": (
            f"short{short_petal}-b{background_support[0]}-"
            + "-".join("s" + ".".join(map(str, support)) for support in supports)
        ),
        "canonical_assignment": key,
        "canonical_assignment_sha256": sha256_json(key),
        "short_petal_label": short_petal,
        "labelled_occupancies": list(occupancies),
        "background_support": list(background_support),
        "petal_supports": [list(support) for support in supports],
        "selected_cofactor_support": list(selected),
        "selected_cofactor_support_mask": selected_mask,
        "selected_cofactor_support_size": len(selected),
        "full_agreement_support": list(selected),
        "selected_cofactor_support_is_full_agreement_support": True,
        "restored_core_refinements": [],
        "periodicity": {
            "stabilizer_order": stabilizer_order(selected_mask, N),
            "complete_fibre_scales": scales,
            "support_periodic": periodic,
            "paid": periodic,
            "direct_support_owner_bound": 1 if periodic else None,
        },
        "quotient_descent": {
            "raw_support_fold_candidate": periodic,
            "candidate_uniform_fibre_scales": scales,
            "removed_at_prior_periodic_owner": periodic,
            "reached_after_periodic_first_match": not periodic,
            "all_witness_data_descend": False,
            "data_gate_status": quotient_status,
            "paid": False,
        },
        "owner": owner,
        "per_pattern_charge": None,
    }


def previous_ledger_record() -> dict[str, object]:
    previous = json.loads(PREVIOUS_LEDGER_PATH.read_text(encoding="utf-8"))
    if previous["schema"] != "rs-mca-l1-b9-frontier-32221-reduced-crt-ledger-v1":
        raise RuntimeError("previous ledger schema drift")
    consequence = previous["ledger_consequence"]
    if not consequence["banked"] or previous["verdict"] != "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED":
        raise RuntimeError("previous ledger is not banked GREEN")
    banked = consequence["banked_result"]
    expected_target = {
        "G2": 2,
        "GR": 4,
        "a_i": [3, 3, 1],
        "b11_box_route": "ESCAPES_BOUNDED_EXCESS_BOX",
        "d": 4,
        "d_minus_ell": 0,
        "ell": 4,
        "lambda": 0,
        "lambda_J": 1,
        "lambda_minus_lambda_J": -1,
        "r": 1,
        "refined_injection_bound": OLD_PROFILE_CHARGE,
        "refined_injection_exponent": 2,
        "support_pattern_count": 384,
        "t": 3,
    }
    if banked["largest_remaining_unresolved_profile"] != expected_target:
        raise RuntimeError("previous ledger target drift")
    if banked["all_profile_bound"] != 1_192_927 or banked["unresolved_bound"] != 357_763:
        raise RuntimeError("previous ledger total drift")
    return {
        "path": str(PREVIOUS_LEDGER_PATH.relative_to(ROOT)),
        "sha256": sha256_file(PREVIOUS_LEDGER_PATH),
        "schema": previous["schema"],
        "verdict": previous["verdict"],
        "profile_sha256": banked["profile_sha256"],
        "all_profile_bound": int(banked["all_profile_bound"]),
        "unresolved_bound": int(banked["unresolved_bound"]),
        "target": expected_target,
    }


def common_cap_record() -> dict[str, object]:
    common = json.loads(COMMON_CAP_PATH.read_text(encoding="utf-8"))
    if common["schema"] != "rs-mca-l1-b9-m2-full-rank-ledger-v5":
        raise RuntimeError("common cap schema drift")
    q19 = common["cases"][0]
    source = q19["auxiliary_owner_target"]
    audit = source["audit"]
    expected_audit = {
        "aggregate_owner_bound": 72,
        "effective_degree_bound": 4,
        "fixed_D_count": 1,
        "fixed_R0_count": 2,
        "fixed_layer_count": 2,
        "integer_floor_bound_per_fixed_D_R0": 36,
        "johnson_numerator": 36,
        "paid": True,
        "petal_domain_size": 12,
        "required_agreement": 7,
        "strict_johnson_margin": 1,
        "unique": False,
    }
    if audit != expected_audit:
        raise RuntimeError("common fixed-layer cap drift")
    if source["owner"] != "PAID_AUXILIARY_JOHNSON" or source["new_owner_charge"] != 72:
        raise RuntimeError("common fixed-layer owner drift")
    theorem_text = SHARP_THEOREM_PATH.read_text(encoding="utf-8")
    for anchor in ("label{prop:capf-pma}", "label{cor:capf-pma-johnson}"):
        if anchor not in theorem_text:
            raise RuntimeError(f"sharp auxiliary theorem anchor missing: {anchor}")
    return {
        "path": str(COMMON_CAP_PATH.relative_to(ROOT)),
        "sha256": sha256_file(COMMON_CAP_PATH),
        "schema": common["schema"],
        "source_profile": source["coordinates"],
        "audit": audit,
        "applicability_key": {
            "ell": ELL,
            "d": 4,
            "r": 1,
            "M": M,
            "b": BACKGROUND_SIZE,
            "required_agreement": 7,
            "petal_domain_size": 12,
        },
        "support_profile_independence": (
            "the fixed-layer cap depends on (ell,d,r,M,b,a), not on the "
            "distribution of the seven petal hits among labelled petals"
        ),
        "sharp_theorem": {
            "path": str(SHARP_THEOREM_PATH.relative_to(ROOT)),
            "sha256": sha256_file(SHARP_THEOREM_PATH),
            "reduction_label": "prop:capf-pma",
            "payment_label": "cor:capf-pma-johnson",
        },
    }


def build_report() -> dict[str, object]:
    gates = uniform_gate_record()
    patterns = [
        pattern_record(background, supports, gates)
        for background, supports in expected_assignments()
    ]
    owners = Counter(str(row["owner"]) for row in patterns)
    periodic = [row for row in patterns if row["periodicity"]["paid"]]
    raw_quotient_candidates = [
        row for row in patterns if row["quotient_descent"]["raw_support_fold_candidate"]
    ]
    prior = previous_ledger_record()
    common_cap = common_cap_record()
    fixed_D_count = comb(ELL, 4)
    fixed_R0_count = comb(BACKGROUND_SIZE, 1)
    return {
        "schema": "rs-mca-l1-b9-frontier-41331-owner-partition-v1",
        "status": "AUDIT/EXACT_GF19_EXISTING_OWNER_PARTITION",
        "statement": (
            "assign exactly one first-match existing owner or UNPAID_PRIMITIVE "
            "to every full-support pattern in "
            "(ell,d,r,t,a_i)=(4,4,1,3,(3,3,1))"
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
            "profile": dict(PROFILE),
            "owner_order": list(OWNER_ORDER),
            "b11_cuts": {"E": 0, "V2": 0, "VR": 0},
        },
        "linked_inputs": {
            "previous_banked_ledger": prior,
            "common_fixed_layer_cap": common_cap,
        },
        "uniform_gates": gates,
        "patterns": patterns,
        "result": {
            "support_pattern_formula": (
                "binom(2,1)*3*binom(4,3)^2*binom(4,1)=384"
            ),
            "support_pattern_count": len(patterns),
            "canonical_assignment_count": len(
                {sha256_json(row["canonical_assignment"]) for row in patterns}
            ),
            "selected_full_support_mask_count": len(
                {int(row["selected_cofactor_support_mask"]) for row in patterns}
            ),
            "restored_core_refinement_count": 0,
            "full_support_pattern_count": len(patterns),
            "support_stabilizer_histogram": dict(
                sorted(
                    Counter(
                        str(row["periodicity"]["stabilizer_order"])
                        for row in patterns
                    ).items()
                )
            ),
            "periodic_support_pattern_count": len(periodic),
            "periodic_pattern_ids": [row["pattern_id"] for row in periodic],
            "raw_uniform_fold_support_candidate_count": len(raw_quotient_candidates),
            "quotient_candidates_after_periodic_first_match": 0,
            "owner_histogram": dict(sorted(owners.items())),
            "paid_existing_owner_patterns": len(patterns),
            "unpaid_primitive_patterns": int(owners["UNPAID_PRIMITIVE"]),
            "transcript_sha256": sha256_json(patterns),
        },
        "aggregate_owner_envelope": {
            "owner": "PAID_AUXILIARY_JOHNSON",
            "applies_to_entire_profile_including_periodic_pattern": True,
            "fixed_D_count": fixed_D_count,
            "fixed_R0_count": fixed_R0_count,
            "fixed_layer_count": fixed_D_count * fixed_R0_count,
            "integer_floor_bound_per_fixed_D_R0": 36,
            "common_fixed_layer_cap": COMMON_FIXED_LAYER_CAP,
            "support_pattern_count_not_multiplied_into_cap": True,
            "no_per_pattern_charge": True,
            "periodic_owner_bound_added_to_cap": False,
            "bankable_profile_charge": COMMON_FIXED_LAYER_CAP,
            "prior_profile_charge": OLD_PROFILE_CHARGE,
            "saved_mass": OLD_PROFILE_CHARGE - COMMON_FIXED_LAYER_CAP,
            "full_ledger_recomputed": False,
        },
        "proof_status": {
            "exact": [
                "all 384 canonical labelled full-support assignments are enumerated",
                "d=ell gives no restored-core refinement",
                "exactly one full support has cyclic stabilizer order two",
                "all remaining 383 patterns first-match to auxiliary Johnson",
                "the common fixed-layer cap is content-addressed and not "
                "multiplied by support patterns",
                "global Johnson and B11 coordinates use exact integers",
            ],
            "review_gate": (
                "local owner partition only; full-ledger banking requires a separate "
                "content-addressed replay and independent review"
            ),
        },
        "nonclaims": [
            "no invariant quotient payment is claimed without all-data descent",
            "the periodic owner bound is not added to the stronger whole-row auxiliary envelope",
            "no algebraic rank or component classification is needed or claimed",
            "no complete ledger, global mixed-petal theorem, m>2, PR #763, or Lean claim is made",
        ],
        "verdict": (
            "GREEN_LOCAL_OWNER_PARTITION - no UNPAID_PRIMITIVE pattern remains; "
            "the whole row is covered by the common fixed-layer cap 72."
        ),
    }


def validate_report(report: dict[str, object]) -> bool:
    patterns = report["patterns"]
    result = report["result"]
    gates = report["uniform_gates"]
    envelope = report["aggregate_owner_envelope"]
    links = report["linked_inputs"]
    expected = expected_assignments()
    expected_keys = [canonical_key(background, supports) for background, supports in expected]
    actual_keys = [row["canonical_assignment"] for row in patterns]
    ids = [str(row["pattern_id"]) for row in patterns]
    masks = [int(row["selected_cofactor_support_mask"]) for row in patterns]
    owners = Counter(str(row["owner"]) for row in patterns)
    current_gates = uniform_gate_record()
    try:
        current_prior = previous_ledger_record()
        current_cap = common_cap_record()
    except (KeyError, RuntimeError, TypeError, ValueError):
        return False
    rows_valid = True
    for row in patterns:
        background_support = tuple(int(value) for value in row["background_support"])
        petal_supports = tuple(
            tuple(int(value) for value in support) for support in row["petal_supports"]
        )
        canonical_selected = tuple(sorted(background_support + sum(petal_supports, ())))
        selected = tuple(int(value) for value in row["selected_cofactor_support"])
        mask = int(row["selected_cofactor_support_mask"])
        scales = quotient_scales(mask)
        periodic = bool(scales)
        short_petal = tuple(len(support) for support in petal_supports).index(1)
        expected_pattern_id = (
            f"short{short_petal}-b{background_support[0]}-"
            + "-".join(
                "s" + ".".join(map(str, support)) for support in petal_supports
            )
        )
        expected_quotient_status = (
            "REMOVED_AT_PRIOR_PERIODIC_OWNER"
            if periodic
            else "NO_SUPPORT_INVARIANT_UNIFORM_FOLD"
        )
        expected_owner = first_match_owner(
            support_periodic=periodic, quotient_paid=False, gates=current_gates
        )
        rows_valid &= (
            row["pattern_id"] == expected_pattern_id
            and row["canonical_assignment"]
            == canonical_key(background_support, petal_supports)
            and row["canonical_assignment_sha256"] == sha256_json(row["canonical_assignment"])
            and row["labelled_occupancies"].count(1) == 1
            and row["labelled_occupancies"].count(3) == 2
            and row["short_petal_label"] == row["labelled_occupancies"].index(1)
            and selected == canonical_selected
            and len(selected) == 8
            and not (set(selected) & set(CORE))
            and row["full_agreement_support"] == list(selected)
            and row["selected_cofactor_support_is_full_agreement_support"] is True
            and row["restored_core_refinements"] == []
            and mask == mask_from_indices(selected)
            and row["periodicity"]["stabilizer_order"] == stabilizer_order(mask, N)
            and row["periodicity"]["complete_fibre_scales"] == scales
            and row["periodicity"]["support_periodic"] == periodic
            and row["periodicity"]["paid"] == periodic
            and row["periodicity"]["direct_support_owner_bound"] == (1 if periodic else None)
            and row["quotient_descent"]["raw_support_fold_candidate"] == periodic
            and row["quotient_descent"]["candidate_uniform_fibre_scales"] == scales
            and row["quotient_descent"]["removed_at_prior_periodic_owner"] == periodic
            and row["quotient_descent"]["reached_after_periodic_first_match"] == (not periodic)
            and row["quotient_descent"]["all_witness_data_descend"] is False
            and row["quotient_descent"]["data_gate_status"] == expected_quotient_status
            and row["quotient_descent"]["paid"] is False
            and row["owner"] == expected_owner
            and row["per_pattern_charge"] is None
        )
    periodic_rows = [row for row in patterns if row["periodicity"]["paid"]]
    return (
        report["schema"] == "rs-mca-l1-b9-frontier-41331-owner-partition-v1"
        and report["input"]["profile"] == PROFILE
        and report["input"]["owner_order"] == list(OWNER_ORDER)
        and gates == current_gates
        and len(patterns) == 384
        and len(set(ids)) == 384
        and actual_keys == expected_keys
        and len(set(sha256_json(key) for key in actual_keys)) == 384
        and len(set(masks)) == 384
        and rows_valid
        and len(periodic_rows) == 1
        and periodic_rows[0]["selected_cofactor_support"] == [4, 5, 6, 8, 13, 14, 15, 17]
        and periodic_rows[0]["periodicity"]["complete_fibre_scales"] == [2]
        and owners
        == Counter({"PAID_AUXILIARY_JOHNSON": 383, "PAID_PERIODIC_SUPPORT_COUNT": 1})
        and int(result["support_pattern_count"]) == 384
        and int(result["canonical_assignment_count"]) == 384
        and int(result["selected_full_support_mask_count"]) == 384
        and int(result["restored_core_refinement_count"]) == 0
        and int(result["full_support_pattern_count"]) == 384
        and result["support_stabilizer_histogram"] == {"1": 383, "2": 1}
        and int(result["periodic_support_pattern_count"]) == 1
        and result["periodic_pattern_ids"] == [periodic_rows[0]["pattern_id"]]
        and int(result["raw_uniform_fold_support_candidate_count"]) == 1
        and int(result["quotient_candidates_after_periodic_first_match"]) == 0
        and result["owner_histogram"]
        == {"PAID_AUXILIARY_JOHNSON": 383, "PAID_PERIODIC_SUPPORT_COUNT": 1}
        and int(result["paid_existing_owner_patterns"]) == 384
        and int(result["unpaid_primitive_patterns"]) == 0
        and result["transcript_sha256"] == sha256_json(patterns)
        and links["previous_banked_ledger"] == current_prior
        and links["common_fixed_layer_cap"] == current_cap
        and envelope["owner"] == "PAID_AUXILIARY_JOHNSON"
        and envelope["applies_to_entire_profile_including_periodic_pattern"] is True
        and int(envelope["fixed_D_count"]) == 1
        and int(envelope["fixed_R0_count"]) == 2
        and int(envelope["fixed_layer_count"]) == 2
        and int(envelope["integer_floor_bound_per_fixed_D_R0"]) == 36
        and int(envelope["common_fixed_layer_cap"]) == 72
        and envelope["support_pattern_count_not_multiplied_into_cap"] is True
        and envelope["no_per_pattern_charge"] is True
        and envelope["periodic_owner_bound_added_to_cap"] is False
        and int(envelope["bankable_profile_charge"]) == 72
        and int(envelope["prior_profile_charge"]) == OLD_PROFILE_CHARGE
        and int(envelope["saved_mass"]) == OLD_PROFILE_CHARGE - 72
        and envelope["full_ledger_recomputed"] is False
    )


def tamper_selftest(report: dict[str, object]) -> int:
    mutations: list[tuple[str, dict[str, object]]] = []

    changed = copy.deepcopy(report)
    source = changed["patterns"][0]
    target = changed["patterns"][1]
    for field in (
        "canonical_assignment",
        "canonical_assignment_sha256",
        "short_petal_label",
        "labelled_occupancies",
        "background_support",
        "petal_supports",
        "selected_cofactor_support",
        "selected_cofactor_support_mask",
        "full_agreement_support",
    ):
        target[field] = copy.deepcopy(source[field])
    target["pattern_id"] = "fresh-id-for-duplicated-assignment"
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("duplicate_assignment", changed))

    changed = copy.deepcopy(report)
    order = list(changed["input"]["owner_order"])
    order[0], order[1] = order[1], order[0]
    changed["input"]["owner_order"] = order
    mutations.append(("owner_order", changed))

    changed = copy.deepcopy(report)
    periodic = next(row for row in changed["patterns"] if row["periodicity"]["paid"])
    periodic["periodicity"] = {
        "stabilizer_order": 1,
        "complete_fibre_scales": [],
        "support_periodic": False,
        "paid": False,
        "direct_support_owner_bound": None,
    }
    periodic["owner"] = "PAID_AUXILIARY_JOHNSON"
    changed["result"]["periodic_support_pattern_count"] = 0
    changed["result"]["periodic_pattern_ids"] = []
    changed["result"]["support_stabilizer_histogram"] = {"1": 384}
    changed["result"]["owner_histogram"] = {"PAID_AUXILIARY_JOHNSON": 384}
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("periodic_support", changed))

    changed = copy.deepcopy(report)
    changed["uniform_gates"]["auxiliary_johnson"]["strict_johnson_margin"] = 0
    mutations.append(("auxiliary_margin", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["restored_core_refinements"] = [{"core_hit": 0}]
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("restored_core_refinement", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["previous_banked_ledger"]["sha256"] = "0" * 64
    mutations.append(("previous_ledger_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["common_fixed_layer_cap"]["sha256"] = "0" * 64
    mutations.append(("common_cap_link", changed))

    changed = copy.deepcopy(report)
    changed["aggregate_owner_envelope"]["bankable_profile_charge"] = 73
    changed["aggregate_owner_envelope"]["saved_mass"] = OLD_PROFILE_CHARGE - 73
    changed["aggregate_owner_envelope"]["periodic_owner_bound_added_to_cap"] = True
    mutations.append(("double_charged_periodic", changed))

    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<28}: {'CAUGHT' if caught else 'MISSED'}")
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
        CERTIFICATE_PATH.write_text(render_certificate_json(report), encoding="utf-8")
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
    result = report["result"]
    envelope = report["aggregate_owner_envelope"]
    print("L1 B9 frontier (4,1,3,(3,3,1)) existing-owner partition")
    print(f"  full-support patterns: {result['support_pattern_count']}")
    print(f"  restored-core refinements: {result['restored_core_refinement_count']}")
    print(f"  support stabilizers: {result['support_stabilizer_histogram']}")
    print(f"  owner histogram: {result['owner_histogram']}")
    print(
        "  common fixed-layer envelope: "
        f"{envelope['fixed_layer_count']}*"
        f"{envelope['integer_floor_bound_per_fixed_D_R0']}="
        f"{envelope['bankable_profile_charge']}"
    )
    print(f"  transcript: {result['transcript_sha256']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
