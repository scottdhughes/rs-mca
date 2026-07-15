#!/usr/bin/env python3
"""Charge the frozen GF(19) ``d=4,r=0`` auxiliary layer once.

This verifier reconstructs the banked post-41331 75-row ledger, selects all
eleven exact profile cells with ``d=4,r=0``, and applies the sharp
fixed-layer auxiliary-Johnson bound

    |T|=12, a=8, d=4, a^2-d|T|=16, 12*(8-4)/16=3.

There is one fixed layer: the whole four-point core is missed and the retained
background set is empty.  One unresolved profile carries the shared charge
three; the other ten profiles receive zero *incremental* charge.  Those zeroes
are bookkeeping entries, not standalone profile bounds.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

from verify_l1_b9_frontier_41331_shared_auxiliary_ledger import (
    UNRESOLVED_ROUTES,
    apply_shared_scope as apply_d4r1_scope,
    current_post_32221_rows,
    is_shared_scope as is_d4r1_scope,
)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIR = (
    ROOT / "experimental/data/certificates/l1-b9-d4r0-shared-auxiliary"
)
CERTIFICATE_PATH = CERTIFICATE_DIR / "ledger_certificate.json"
PRIOR_LEDGER_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-frontier-41331/ledger_certificate.json"
)
PRIOR_LEDGER_VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py"
)
PROFILE_ENUMERATOR_PATH = (
    ROOT / "experimental/scripts/verify_l1_mixed_petal_frontier_ledger.py"
)
THEOREM_SOURCE_PATH = ROOT / "experimental/cap25_cap_v13_raw.tex"
SCOPE_NOTE_PATH = (
    ROOT / "experimental/notes/l1/l1_b9_d4r0_shared_auxiliary_johnson.md"
)
INDEPENDENT_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_d4r0_shared_auxiliary_independent_review.md"
)
CROSS_MODEL_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_d4r0_shared_auxiliary_cross_model_review.md"
)

SHARED_ENVELOPE_ID = "GF19_D4_R0_FIXED_LAYER_AUXILIARY_JOHNSON"
SHARED_CHARGE = 3
EXPECTED_SCOPE_KEYS = (
    (2, (4, 4)),
    (3, (4, 4, 4)),
    (3, (4, 4, 3)),
    (3, (4, 4, 2)),
    (3, (4, 4, 1)),
    (3, (4, 3, 3)),
    (3, (4, 3, 2)),
    (3, (4, 3, 1)),
    (3, (4, 2, 2)),
    (3, (3, 3, 3)),
    (3, (3, 3, 2)),
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def render_certificate_json(report: dict[str, object]) -> str:
    """Pretty-print metadata with one complete scope-profile row per line."""
    marker = "__RS_MCA_D4R0_SCOPE_PROFILE_ROWS__"
    rows = report["shared_scope"]["profiles"]
    compact = copy.deepcopy(report)
    compact["shared_scope"]["profiles"] = marker
    rendered = json.dumps(compact, indent=2, sort_keys=True)
    needle = f'    "profiles": "{marker}"'
    if rendered.count(needle) != 1:
        raise RuntimeError("hybrid certificate marker drift")
    row_block = (
        '    "profiles": [\n'
        + ",\n".join(
            "      " + json.dumps(row, sort_keys=True, separators=(",", ":"))
            for row in rows
        )
        + "\n    ]"
    )
    rendered = rendered.replace(needle, row_block) + "\n"
    if json.loads(rendered) != report:
        raise RuntimeError("hybrid certificate round-trip failed")
    return rendered


def is_shared_scope(row: dict[str, object]) -> bool:
    return int(row["d"]) == 4 and int(row["r"]) == 0


def is_carrier(row: dict[str, object]) -> bool:
    return (
        is_shared_scope(row)
        and int(row["t"]) == 3
        and row["a_i"] == [3, 3, 2]
    )


def profile_key(row: dict[str, object]) -> tuple[int, tuple[int, ...]]:
    return int(row["t"]), tuple(int(hit) for hit in row["a_i"])


def current_post_41331_rows() -> list[dict[str, object]]:
    rows = current_post_32221_rows()
    current = [
        apply_d4r1_scope(row) if is_d4r1_scope(row) else dict(row)
        for row in rows
    ]
    prior = load_json(PRIOR_LEDGER_PATH)
    candidate = prior["ledger_consequence"]["candidate_result"]
    unresolved = [
        row for row in current if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    if (
        prior["schema"]
        != "rs-mca-l1-b9-frontier-41331-shared-auxiliary-ledger-v1"
        or prior["verdict"] != "GREEN_LOCAL_SHARED_AUXILIARY_LEDGER_BANKED"
        or prior["ledger_consequence"]["banked"] is not True
        or len(current) != 75
        or sum(int(row["refined_injection_bound"]) for row in current)
        != 776_979
        or sum(int(row["refined_injection_bound"]) for row in unresolved)
        != 212_755
        or sha256_json(current) != candidate["profile_sha256"]
    ):
        raise RuntimeError("post-41331 ledger reconstruction drift")
    return current


def scope_profile_record(row: dict[str, object]) -> dict[str, object]:
    carrier = is_carrier(row)
    return {
        "coordinates": {
            "ell": int(row["d"]) - int(row["d_minus_ell"]),
            "d": int(row["d"]),
            "r": int(row["r"]),
            "t": int(row["t"]),
            "a_i": list(row["a_i"]),
            "G2": int(row["G2"]),
            "GR": int(row["GR"]),
            "lambda": int(row["lambda"]),
        },
        "prior_route": row["b11_box_route"],
        "support_pattern_count": int(row["support_pattern_count"]),
        "post_41331_owner": row["refined_owner"],
        "post_41331_charge": int(row["refined_injection_bound"]),
        "shared_envelope_id": SHARED_ENVELOPE_ID,
        "shared_envelope_carrier": carrier,
        "incremental_charge_after_regrouping": SHARED_CHARGE if carrier else 0,
        "zero_charge_semantics": (
            None
            if carrier
            else "COVERED_BY_COMMON_LAYER_ENVELOPE_NOT_STANDALONE_ZERO_BOUND"
        ),
    }


def apply_shared_scope(row: dict[str, object]) -> dict[str, object]:
    updated = dict(row)
    prior_owner = updated["refined_owner"]
    prior_bound = int(updated["refined_injection_bound"])
    carrier = is_carrier(updated)
    updated.update(
        {
            "prior_refined_owner": prior_owner,
            "prior_refined_injection_bound": prior_bound,
            "shared_layer_envelope_id": SHARED_ENVELOPE_ID,
            "shared_layer_envelope_carrier": carrier,
            "refined_owner": (
                "PAID_AUXILIARY_JOHNSON_D4R0_SHARED_LAYER_ENVELOPE"
                if carrier
                else "COVERED_BY_D4R0_SHARED_AUXILIARY_JOHNSON_ENVELOPE"
            ),
            "refined_injection_exponent": None,
            "refined_injection_bound": SHARED_CHARGE if carrier else 0,
            "ledger_charge_semantics": (
                "D4R0_SHARED_ENVELOPE_CHARGED_ONCE"
                if carrier
                else "ZERO_INCREMENT_ONLY_NOT_A_STANDALONE_PROFILE_BOUND"
            ),
        }
    )
    return updated


def largest_row_record(row: dict[str, object]) -> dict[str, object]:
    return {
        "ell": int(row["d"]) - int(row["d_minus_ell"]),
        **{
            key: row[key]
            for key in (
                "d",
                "r",
                "t",
                "a_i",
                "d_minus_ell",
                "G2",
                "GR",
                "lambda",
                "lambda_J",
                "lambda_minus_lambda_J",
                "support_pattern_count",
                "refined_injection_exponent",
                "refined_injection_bound",
                "b11_box_route",
            )
        },
    }


def linked_inputs() -> dict[str, object]:
    prior = load_json(PRIOR_LEDGER_PATH)
    theorem_text = THEOREM_SOURCE_PATH.read_text(encoding="utf-8")
    note_text = SCOPE_NOTE_PATH.read_text(encoding="utf-8")
    independent_review_text = INDEPENDENT_REVIEW_PATH.read_text(encoding="utf-8")
    cross_model_review_text = CROSS_MODEL_REVIEW_PATH.read_text(encoding="utf-8")
    candidate = prior["ledger_consequence"]["candidate_result"]
    valid = (
        prior["schema"]
        == "rs-mca-l1-b9-frontier-41331-shared-auxiliary-ledger-v1"
        and prior["verdict"] == "GREEN_LOCAL_SHARED_AUXILIARY_LEDGER_BANKED"
        and prior["ledger_consequence"]["banked"] is True
        and candidate["all_profile_bound"] == 776_979
        and candidate["unresolved_bound"] == 212_755
        and "label{prop:capf-concrete-sunflower}" in theorem_text
        and "label{prop:capf-pma}" in theorem_text
        and "label{cor:capf-pma-johnson}" in theorem_text
        and "## One fixed layer" in note_text
        and "135,470 -> 3" in note_text
        and "no cross-`r` aggregation" in note_text
        and "**GREEN - proof obligation appears satisfied with dependencies verified.**"
        in independent_review_text
        and "**YES, conditionally on certificate replay and hash-link only.**"
        in independent_review_text
        and "## Verdict\n\n**GREEN.**" in cross_model_review_text
        and "## Ledger authorization\n\n**YES.**" in cross_model_review_text
        and "## PR-worthiness\n\n**YES.**" in cross_model_review_text
    )
    if not valid:
        raise RuntimeError("d4r0 shared-owner input linkage failed")
    paths = {
        "prior_banked_ledger": PRIOR_LEDGER_PATH,
        "prior_ledger_verifier": PRIOR_LEDGER_VERIFIER_PATH,
        "profile_enumerator": PROFILE_ENUMERATOR_PATH,
        "sharp_theorem_source": THEOREM_SOURCE_PATH,
        "scope_note": SCOPE_NOTE_PATH,
        "independent_theorem_review": INDEPENDENT_REVIEW_PATH,
        "cross_model_packet_review": CROSS_MODEL_REVIEW_PATH,
    }
    schemas = {
        "prior_banked_ledger": prior["schema"],
        "prior_ledger_verifier": "python-source",
        "profile_enumerator": "python-source",
        "sharp_theorem_source": "latex-source",
        "scope_note": "markdown",
        "independent_theorem_review": "markdown-green-review",
        "cross_model_packet_review": "markdown-green-review",
    }
    return {
        name: {
            "path": str(path.relative_to(ROOT)),
            "schema": schemas[name],
            "sha256": sha256_file(path),
        }
        for name, path in paths.items()
    }


def build_report() -> dict[str, object]:
    links = linked_inputs()
    prior_rows = current_post_41331_rows()
    scope = [row for row in prior_rows if is_shared_scope(row)]
    if tuple(profile_key(row) for row in scope) != EXPECTED_SCOPE_KEYS:
        raise RuntimeError("shared d=4,r=0 profile scope drift")
    if len(scope) != 11 or sum(is_carrier(row) for row in scope) != 1:
        raise RuntimeError("d4r0 shared owner carrier/scope multiplicity drift")

    scope_profiles = [scope_profile_record(row) for row in scope]
    scope_current_charge = sum(
        int(row["refined_injection_bound"]) for row in scope
    )
    scope_unresolved_charge = sum(
        int(row["refined_injection_bound"])
        for row in scope
        if row["b11_box_route"] in UNRESOLVED_ROUTES
    )
    if (
        sum(int(row["support_pattern_count"]) for row in scope) != 794
        or scope_current_charge != 135_470
        or scope_unresolved_charge != 107_844
        or Counter(str(row["b11_box_route"]) for row in scope)
        != Counter(
            {
                "FULL_PETAL_SEPARATE": 2,
                "PAID_JOHNSON": 6,
                "ESCAPES_BOUNDED_EXCESS_BOX": 3,
            }
        )
    ):
        raise RuntimeError("d4r0 shared owner exact scope arithmetic drift")

    candidate_rows = [
        apply_shared_scope(row) if is_shared_scope(row) else dict(row)
        for row in prior_rows
    ]
    prior_unresolved = [
        row for row in prior_rows if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    candidate_unresolved = [
        row for row in candidate_rows if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    candidate_unresolved.sort(
        key=lambda row: int(row["refined_injection_bound"]), reverse=True
    )
    prior_all = sum(int(row["refined_injection_bound"]) for row in prior_rows)
    prior_unresolved_total = sum(
        int(row["refined_injection_bound"]) for row in prior_unresolved
    )
    candidate_all = sum(
        int(row["refined_injection_bound"]) for row in candidate_rows
    )
    candidate_unresolved_total = sum(
        int(row["refined_injection_bound"]) for row in candidate_unresolved
    )
    if (
        prior_all != 776_979
        or prior_unresolved_total != 212_755
        or candidate_all != 641_512
        or candidate_unresolved_total != 104_914
    ):
        raise RuntimeError("d4r0 shared auxiliary-owner ledger total drift")

    largest = largest_row_record(candidate_unresolved[0])
    if not (
        largest["ell"] == 4
        and largest["d"] == 3
        and largest["r"] == 1
        and largest["t"] == 3
        and largest["a_i"] == [3, 2, 1]
        and largest["G2"] == 3
        and largest["GR"] == 4
        and largest["support_pattern_count"] == 1_152
        and largest["refined_injection_bound"] == 21_888
    ):
        raise RuntimeError("post-d4r0 largest row drift")

    return {
        "schema": "rs-mca-l1-b9-d4r0-shared-auxiliary-ledger-v1",
        "status": "EXACT_D4R0_SHARED_ENVELOPE_REPLAY_FRESH_REVIEWS_GREEN",
        "statement": (
            "the fixed-layer auxiliary Johnson cap 3 replaces the combined "
            "banked-41331 charge of all eleven d=4,r=0 profile cells"
        ),
        "shared_scope": {
            "envelope_id": SHARED_ENVELOPE_ID,
            "selection_rule": "d=4 and r=0 only; no cross-r aggregation",
            "profile_count": len(scope),
            "support_pattern_count": sum(
                int(row["support_pattern_count"]) for row in scope
            ),
            "support_pattern_count_semantics": (
                "AGGREGATE_PROFILE_MULTIPLICITY_NOT_REALIZED_CODEWORD_CENSUS"
            ),
            "profile_sha256": sha256_json(scope_profiles),
            "profiles": scope_profiles,
            "route_profile_histogram": {
                key: value
                for key, value in sorted(
                    Counter(str(row["b11_box_route"]) for row in scope).items()
                )
            },
            "fixed_layers": [
                {
                    "layer_id": "D=0.1.2.3;R0=empty",
                    "D0": [0, 1, 2, 3],
                    "R0": [],
                    "bound": SHARED_CHARGE,
                }
            ],
            "concrete_layer_bridge": {
                "evaluation_partition": {
                    "core_Y": [0, 1, 2, 3],
                    "background": [16, 17],
                    "petal_domain_size": 12,
                },
                "D0_equals_Y": True,
                "retained_background_R0": [],
                "core_agreement_count": 0,
                "background_agreement_count": 0,
                "no_agreements_outside_petals": True,
                "injection_map": "G_P=P-P_star",
                "degree_bound": 4,
                "required_petal_agreements": 8,
                "single_auxiliary_word": True,
            },
            "strict_johnson_audit": {
                "petal_domain_size": 12,
                "required_agreement": 8,
                "effective_degree_bound": 4,
                "margin": 16,
                "numerator": 48,
                "denominator": 16,
                "integer_floor_bound_per_fixed_D_R0": 3,
                "fixed_D_count": 1,
                "fixed_R0_count": 1,
                "fixed_layer_count": 1,
                "shared_envelope_charge": SHARED_CHARGE,
            },
            "carrier_profile": {
                "t": 3,
                "a_i": [3, 3, 2],
                "charge": SHARED_CHARGE,
                "carrier_is_bookkeeping_only": True,
            },
        },
        "result": {
            "banked_41331_scope_charge": scope_current_charge,
            "banked_41331_scope_unresolved_charge": scope_unresolved_charge,
            "shared_envelope_charge": SHARED_CHARGE,
            "incremental_saved_mass": scope_current_charge - SHARED_CHARGE,
            "unresolved_saved_mass": scope_unresolved_charge - SHARED_CHARGE,
            "shared_charge_count": sum(
                int(row["shared_layer_envelope_carrier"])
                for row in candidate_rows
                if is_shared_scope(row)
            ),
            "zero_increment_profile_count": sum(
                int(row["refined_injection_bound"] == 0)
                for row in candidate_rows
                if is_shared_scope(row)
            ),
        },
        "ledger_consequence": {
            "prior_all_profile_bound": prior_all,
            "prior_unresolved_bound": prior_unresolved_total,
            "prior_profile_sha256": sha256_json(prior_rows),
            "candidate_result": {
                "all_profile_bound": candidate_all,
                "unresolved_bound": candidate_unresolved_total,
                "profile_sha256": sha256_json(candidate_rows),
                "largest_remaining_unresolved_profile": largest,
            },
            "banked": True,
            "closure_verdict": "POSITIVE_UNRESOLVED_MASS_REMAINS",
        },
        "linked_inputs": links,
        "proof_status": {
            "exact": [
                "the banked post-41331 75-row ledger and profile hash are replayed",
                "all eleven and only d=4,r=0 profile cells are selected",
                "the sharp theorem bounds their one fixed layer by 3",
                "one carrier receives 3 and ten cells receive zero incremental charge",
                "the all-profile and unresolved totals are recomputed from all 75 rows",
                "the next largest row is selected dynamically",
                "the prior ledger, reconstruction code, profile enumerator, theorem source, and note are hash-linked",
            ],
            "review_gate": (
                "fresh independent theorem and Claude cross-model packet "
                "reviews GREEN; ledger authorization YES"
            ),
        },
        "nonclaims": [
            "zero incremental charge is not a standalone zero bound for any profile",
            "no cross-r aggregation or common cap 36 is used",
            "no d=3,r=1 payment is included",
            "no global mixed-petal theorem, m>2, PR #763, or Lean claim is made",
        ],
        "verdict": "GREEN_LOCAL_D4R0_SHARED_AUXILIARY_LEDGER_BANKED",
    }


def validate_report(report: dict[str, object]) -> bool:
    try:
        expected = build_report()
        scope = report["shared_scope"]
        result = report["result"]
        ledger = report["ledger_consequence"]
        profiles = scope["profiles"]
        return (
            report == expected
            and len(profiles) == 11
            and tuple(
                (
                    int(row["coordinates"]["t"]),
                    tuple(int(hit) for hit in row["coordinates"]["a_i"]),
                )
                for row in profiles
            )
            == EXPECTED_SCOPE_KEYS
            and scope["profile_sha256"] == sha256_json(profiles)
            and scope["selection_rule"]
            == "d=4 and r=0 only; no cross-r aggregation"
            and scope["strict_johnson_audit"]["margin"] == 16
            and scope["strict_johnson_audit"]["denominator"] == 16
            and scope["strict_johnson_audit"]["fixed_layer_count"] == 1
            and scope["strict_johnson_audit"]["shared_envelope_charge"] == 3
            and scope["concrete_layer_bridge"]
            == {
                "evaluation_partition": {
                    "core_Y": [0, 1, 2, 3],
                    "background": [16, 17],
                    "petal_domain_size": 12,
                },
                "D0_equals_Y": True,
                "retained_background_R0": [],
                "core_agreement_count": 0,
                "background_agreement_count": 0,
                "no_agreements_outside_petals": True,
                "injection_map": "G_P=P-P_star",
                "degree_bound": 4,
                "required_petal_agreements": 8,
                "single_auxiliary_word": True,
            }
            and result["shared_charge_count"] == 1
            and result["zero_increment_profile_count"] == 10
            and result["banked_41331_scope_charge"] == 135_470
            and result["shared_envelope_charge"] == 3
            and ledger["candidate_result"]["all_profile_bound"] == 641_512
            and ledger["candidate_result"]["unresolved_bound"] == 104_914
            and ledger["banked"] is True
            and report["verdict"]
            == "GREEN_LOCAL_D4R0_SHARED_AUXILIARY_LEDGER_BANKED"
        )
    except (KeyError, RuntimeError, TypeError, ValueError):
        return False


def tamper_selftest(report: dict[str, object]) -> int:
    mutations: list[tuple[str, dict[str, object]]] = []

    changed = copy.deepcopy(report)
    changed["shared_scope"]["profiles"][1] = copy.deepcopy(
        changed["shared_scope"]["profiles"][0]
    )
    changed["shared_scope"]["profile_sha256"] = sha256_json(
        changed["shared_scope"]["profiles"]
    )
    mutations.append(("duplicate_scope_profile", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["profiles"].pop()
    changed["shared_scope"]["profile_count"] -= 1
    changed["shared_scope"]["profile_sha256"] = sha256_json(
        changed["shared_scope"]["profiles"]
    )
    mutations.append(("missing_scope_profile", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["profiles"][0], changed["shared_scope"]["profiles"][1] = (
        changed["shared_scope"]["profiles"][1],
        changed["shared_scope"]["profiles"][0],
    )
    changed["shared_scope"]["profile_sha256"] = sha256_json(
        changed["shared_scope"]["profiles"]
    )
    mutations.append(("scope_profile_order", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["profiles"][0]["coordinates"]["r"] = 1
    changed["shared_scope"]["profile_sha256"] = sha256_json(
        changed["shared_scope"]["profiles"]
    )
    mutations.append(("foreign_cross_r_profile", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["profiles"][0]["incremental_charge_after_regrouping"] = 3
    changed["shared_scope"]["profile_sha256"] = sha256_json(
        changed["shared_scope"]["profiles"]
    )
    mutations.append(("per_profile_multiplication", changed))

    changed = copy.deepcopy(report)
    old_carrier = changed["shared_scope"]["profiles"][-1]
    new_carrier = changed["shared_scope"]["profiles"][-2]
    old_carrier["shared_envelope_carrier"] = False
    old_carrier["incremental_charge_after_regrouping"] = 0
    old_carrier["zero_charge_semantics"] = (
        "COVERED_BY_COMMON_LAYER_ENVELOPE_NOT_STANDALONE_ZERO_BOUND"
    )
    new_carrier["shared_envelope_carrier"] = True
    new_carrier["incremental_charge_after_regrouping"] = 3
    new_carrier["zero_charge_semantics"] = None
    changed["shared_scope"]["carrier_profile"]["a_i"] = [3, 3, 3]
    changed["shared_scope"]["profile_sha256"] = sha256_json(
        changed["shared_scope"]["profiles"]
    )
    mutations.append(("carrier_placement", changed))

    changed = copy.deepcopy(report)
    changed["result"]["shared_charge_count"] = 2
    mutations.append(("duplicate_3_charge", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["strict_johnson_audit"]["margin"] = 0
    mutations.append(("strict_margin", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["strict_johnson_audit"]["fixed_R0_count"] = 2
    changed["shared_scope"]["strict_johnson_audit"]["fixed_layer_count"] = 2
    changed["shared_scope"]["strict_johnson_audit"]["shared_envelope_charge"] = 6
    mutations.append(("spurious_layer_factor", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["concrete_layer_bridge"][
        "background_agreement_count"
    ] = 1
    changed["shared_scope"]["concrete_layer_bridge"][
        "no_agreements_outside_petals"
    ] = False
    mutations.append(("concrete_layer_bridge", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["selection_rule"] = "d=4 and r in {0,1}"
    mutations.append(("cross_r_aggregation", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"]["all_profile_bound"] += 1
    mutations.append(("all_profile_total", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"]["unresolved_bound"] -= 3
    mutations.append(("unresolved_convention", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"][
        "largest_remaining_unresolved_profile"
    ]["refined_injection_bound"] += 1
    mutations.append(("next_largest_row", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["banked"] = False
    mutations.append(("banked_status", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["prior_banked_ledger"]["sha256"] = "0" * 64
    mutations.append(("prior_ledger_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["prior_ledger_verifier"]["sha256"] = "0" * 64
    mutations.append(("prior_verifier_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["profile_enumerator"]["sha256"] = "0" * 64
    mutations.append(("profile_enumerator_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["sharp_theorem_source"]["sha256"] = "0" * 64
    mutations.append(("theorem_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["scope_note"]["sha256"] = "0" * 64
    mutations.append(("scope_note_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["independent_theorem_review"]["sha256"] = "0" * 64
    mutations.append(("independent_review_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["cross_model_packet_review"]["sha256"] = "0" * 64
    mutations.append(("cross_model_review_link", changed))

    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<28}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))

    report = build_report()
    if not validate_report(report):
        raise RuntimeError("internally generated d4r0 ledger failed validation")
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_DIR.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            render_certificate_json(report), encoding="utf-8"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if not CERTIFICATE_PATH.exists():
        raise RuntimeError(f"frozen certificate missing: {CERTIFICATE_PATH}")
    frozen = load_json(CERTIFICATE_PATH)
    if frozen != report or not validate_report(frozen):
        raise RuntimeError("frozen d4r0 ledger certificate drift")
    ledger = report["ledger_consequence"]
    largest = ledger["candidate_result"]["largest_remaining_unresolved_profile"]
    print("PASS l1-b9-d4r0-shared-auxiliary-ledger")
    print(
        f"  shared scope: {report['shared_scope']['profile_count']} profiles, "
        f"{report['result']['banked_41331_scope_charge']} -> "
        f"{report['result']['shared_envelope_charge']}"
    )
    print(
        f"  all profiles: {ledger['prior_all_profile_bound']} -> "
        f"{ledger['candidate_result']['all_profile_bound']}"
    )
    print(
        f"  unresolved: {ledger['prior_unresolved_bound']} -> "
        f"{ledger['candidate_result']['unresolved_bound']}"
    )
    print(
        "  next largest: "
        f"(d,r,a_i)=({largest['d']},{largest['r']},{largest['a_i']}), "
        f"charge={largest['refined_injection_bound']}"
    )
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
