#!/usr/bin/env python3
"""Replay the post-32221 ledger and charge the d=4,r=1 layer once.

The previously banked auxiliary-Johnson charge ``72`` is a bound for the
whole union of fixed ``(D_0,R_0)`` layers at ``d=4,r=1``.  The prior ledger
attached that charge to one occupancy profile while retaining separate bounds
for fourteen other profiles in the same layer.  This verifier reconstructs
the exact 75-row ledger, selects all fifteen common-layer profiles, keeps one
``72`` carrier charge, and assigns zero *incremental* charge to the other
fourteen rows.

The zero allocations are bookkeeping entries, not standalone profile bounds.
Together the fifteen disjoint cells are bounded by the one shared envelope.
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

from verify_l1_b9_frontier_32221_reduced_crt_ledger import (
    UNRESOLVED_ROUTES,
    is_32221,
    new_32221_replacement,
    reconstruct_current_banked_rows,
)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIR = ROOT / "experimental/data/certificates/l1-b9-frontier-41331"
CERTIFICATE_PATH = CERTIFICATE_DIR / "ledger_certificate.json"
OWNER_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-41331-owner-partition/certificate.json"
)
PRIOR_LEDGER_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-frontier-32221/ledger_certificate.json"
)
COMMON_CAP_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-m2-full-rank-ledger/certificate.json"
)
THEOREM_SOURCE_PATH = ROOT / "experimental/cap25_cap_v13_raw.tex"
SCOPE_NOTE_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_41331_shared_auxiliary_johnson.md"
)
INDEPENDENT_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_41331_shared_auxiliary_independent_review.md"
)
CROSS_MODEL_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_41331_shared_auxiliary_cross_model_review.md"
)

SHARED_ENVELOPE_ID = "GF19_D4_R1_FIXED_LAYER_AUXILIARY_JOHNSON"
SHARED_CHARGE = 72
EXPECTED_SCOPE_KEYS = (
    (2, (4, 4)),
    (2, (4, 3)),
    (3, (4, 4, 4)),
    (3, (4, 4, 3)),
    (3, (4, 4, 2)),
    (3, (4, 4, 1)),
    (3, (4, 3, 3)),
    (3, (4, 3, 2)),
    (3, (4, 3, 1)),
    (3, (4, 2, 2)),
    (3, (4, 2, 1)),
    (3, (3, 3, 3)),
    (3, (3, 3, 2)),
    (3, (3, 3, 1)),
    (3, (3, 2, 2)),
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
    marker = "__RS_MCA_SHARED_SCOPE_PROFILE_ROWS__"
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
    return int(row["d"]) == 4 and int(row["r"]) == 1


def is_carrier(row: dict[str, object]) -> bool:
    return (
        is_shared_scope(row)
        and int(row["t"]) == 3
        and row["a_i"] == [3, 2, 2]
    )


def profile_key(row: dict[str, object]) -> tuple[int, tuple[int, ...]]:
    return int(row["t"]), tuple(int(hit) for hit in row["a_i"])


def current_post_32221_rows() -> list[dict[str, object]]:
    rows = reconstruct_current_banked_rows()
    current = [
        new_32221_replacement(row) if is_32221(row) else dict(row)
        for row in rows
    ]
    prior = load_json(PRIOR_LEDGER_PATH)
    banked = prior["ledger_consequence"]["banked_result"]
    unresolved = [
        row for row in current if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    if (
        prior["schema"]
        != "rs-mca-l1-b9-frontier-32221-reduced-crt-ledger-v1"
        or not prior["ledger_consequence"]["banked"]
        or prior["verdict"] != "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED"
        or len(current) != 75
        or sum(int(row["refined_injection_bound"]) for row in current)
        != 1_192_927
        or sum(int(row["refined_injection_bound"]) for row in unresolved)
        != 357_763
        or sha256_json(current) != banked["profile_sha256"]
    ):
        raise RuntimeError("post-32221 ledger reconstruction drift")
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
        "original_B3_charge": int(row["selected_injection_bound"]),
        "post_32221_owner": row["refined_owner"],
        "post_32221_charge": int(row["refined_injection_bound"]),
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
                "PAID_AUXILIARY_JOHNSON_SHARED_LAYER_ENVELOPE"
                if carrier
                else "COVERED_BY_SHARED_AUXILIARY_JOHNSON_ENVELOPE"
            ),
            "refined_injection_exponent": None,
            "refined_injection_bound": SHARED_CHARGE if carrier else 0,
            "ledger_charge_semantics": (
                "SHARED_ENVELOPE_CHARGED_ONCE"
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
    owner = load_json(OWNER_CERTIFICATE_PATH)
    prior = load_json(PRIOR_LEDGER_PATH)
    common = load_json(COMMON_CAP_PATH)
    theorem_text = THEOREM_SOURCE_PATH.read_text(encoding="utf-8")
    note_text = SCOPE_NOTE_PATH.read_text(encoding="utf-8")
    independent_review_text = INDEPENDENT_REVIEW_PATH.read_text(encoding="utf-8")
    cross_model_review_text = CROSS_MODEL_REVIEW_PATH.read_text(encoding="utf-8")
    envelope = owner["aggregate_owner_envelope"]
    common_audit = common["cases"][0]["auxiliary_owner_target"]["audit"]
    valid = (
        owner["schema"] == "rs-mca-l1-b9-frontier-41331-owner-partition-v1"
        and owner["result"]["support_pattern_count"] == 384
        and owner["result"]["owner_histogram"]
        == {
            "PAID_AUXILIARY_JOHNSON": 383,
            "PAID_PERIODIC_SUPPORT_COUNT": 1,
        }
        and owner["result"]["restored_core_refinement_count"] == 0
        and owner["result"]["unpaid_primitive_patterns"] == 0
        and envelope["common_fixed_layer_cap"] == SHARED_CHARGE
        and envelope["integer_floor_bound_per_fixed_D_R0"] == 36
        and envelope["fixed_D_count"] == 1
        and envelope["fixed_R0_count"] == 2
        and envelope["periodic_owner_bound_added_to_cap"] is False
        and prior["schema"]
        == "rs-mca-l1-b9-frontier-32221-reduced-crt-ledger-v1"
        and prior["ledger_consequence"]["banked_result"]["all_profile_bound"]
        == 1_192_927
        and prior["ledger_consequence"]["banked_result"]["unresolved_bound"]
        == 357_763
        and common["schema"] == "rs-mca-l1-b9-m2-full-rank-ledger-v5"
        and common_audit["aggregate_owner_bound"] == SHARED_CHARGE
        and common_audit["strict_johnson_margin"] == 1
        and common_audit["integer_floor_bound_per_fixed_D_R0"] == 36
        and "label{prop:capf-pma}" in theorem_text
        and "label{cor:capf-pma-johnson}" in theorem_text
        and "The layer-level owner" in note_text
        and "416,020 -> 72" in note_text
        and "GREEN - proof obligation appears satisfied" in independent_review_text
        and "**YES.** Authorize the local regrouping" in independent_review_text
        and "## Verdict\n\n**GREEN.**" in cross_model_review_text
        and "## Ledger authorization\n\n**YES.**" in cross_model_review_text
    )
    if not valid:
        raise RuntimeError("shared auxiliary-owner input linkage failed")
    paths = {
        "owner_partition": OWNER_CERTIFICATE_PATH,
        "prior_banked_ledger": PRIOR_LEDGER_PATH,
        "common_fixed_layer_cap": COMMON_CAP_PATH,
        "sharp_theorem_source": THEOREM_SOURCE_PATH,
        "scope_note": SCOPE_NOTE_PATH,
        "independent_review": INDEPENDENT_REVIEW_PATH,
        "cross_model_review": CROSS_MODEL_REVIEW_PATH,
    }
    schemas = {
        "owner_partition": owner["schema"],
        "prior_banked_ledger": prior["schema"],
        "common_fixed_layer_cap": common["schema"],
        "sharp_theorem_source": "latex-source",
        "scope_note": "markdown",
        "independent_review": "markdown",
        "cross_model_review": "markdown",
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
    prior_rows = current_post_32221_rows()
    scope = [row for row in prior_rows if is_shared_scope(row)]
    if tuple(profile_key(row) for row in scope) != EXPECTED_SCOPE_KEYS:
        raise RuntimeError("shared d=4,r=1 profile scope drift")
    if len(scope) != 15 or sum(is_carrier(row) for row in scope) != 1:
        raise RuntimeError("shared owner carrier/scope multiplicity drift")

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
        sum(int(row["support_pattern_count"]) for row in scope) != 3_172
        or sum(int(row["selected_injection_bound"]) for row in scope) != 727_852
        or scope_current_charge != 416_020
        or scope_unresolved_charge != 145_080
        or Counter(str(row["b11_box_route"]) for row in scope)
        != Counter(
            {
                "FULL_PETAL_SEPARATE": 2,
                "PAID_JOHNSON": 9,
                "ESCAPES_BOUNDED_EXCESS_BOX": 4,
            }
        )
    ):
        raise RuntimeError("shared owner exact scope arithmetic drift")

    banked_rows = [
        apply_shared_scope(row) if is_shared_scope(row) else dict(row)
        for row in prior_rows
    ]
    prior_unresolved = [
        row for row in prior_rows if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    banked_unresolved = [
        row for row in banked_rows if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    banked_unresolved.sort(
        key=lambda row: int(row["refined_injection_bound"]), reverse=True
    )
    prior_all = sum(int(row["refined_injection_bound"]) for row in prior_rows)
    prior_unresolved_total = sum(
        int(row["refined_injection_bound"]) for row in prior_unresolved
    )
    banked_all = sum(int(row["refined_injection_bound"]) for row in banked_rows)
    banked_unresolved_total = sum(
        int(row["refined_injection_bound"]) for row in banked_unresolved
    )
    if (
        prior_all != 1_192_927
        or prior_unresolved_total != 357_763
        or banked_all != 776_979
        or banked_unresolved_total != 212_755
    ):
        raise RuntimeError("shared auxiliary-owner ledger total drift")

    largest = largest_row_record(banked_unresolved[0])
    if not (
        largest["ell"] == 4
        and largest["d"] == 4
        and largest["r"] == 0
        and largest["t"] == 3
        and largest["a_i"] == [3, 3, 2]
        and largest["G2"] == 2
        and largest["GR"] == 5
        and largest["support_pattern_count"] == 288
        and largest["refined_injection_bound"] == 103_968
    ):
        raise RuntimeError("post-shared-owner largest row drift")

    return {
        "schema": "rs-mca-l1-b9-frontier-41331-shared-auxiliary-ledger-v1",
        "status": "EXACT_SHARED_ENVELOPE_REPLAY_FRESH_REVIEWS_GREEN",
        "statement": (
            "the fixed-layer auxiliary Johnson cap 72 replaces the combined "
            "post-32221 charge of all fifteen d=4,r=1 profile cells"
        ),
        "shared_scope": {
            "envelope_id": SHARED_ENVELOPE_ID,
            "selection_rule": "d=4 and r=1 in the frozen GF(19) profile ledger",
            "profile_count": len(scope),
            "support_pattern_count": sum(
                int(row["support_pattern_count"]) for row in scope
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
                    "layer_id": "D=0.1.2.3;R0=16",
                    "D0": [0, 1, 2, 3],
                    "R0": [16],
                    "bound": 36,
                },
                {
                    "layer_id": "D=0.1.2.3;R0=17",
                    "D0": [0, 1, 2, 3],
                    "R0": [17],
                    "bound": 36,
                },
            ],
            "strict_johnson_audit": {
                "petal_domain_size": 12,
                "required_agreement": 7,
                "effective_degree_bound": 4,
                "margin": 1,
                "numerator": 36,
                "integer_floor_bound_per_fixed_D_R0": 36,
                "fixed_D_count": 1,
                "fixed_R0_count": 2,
                "shared_envelope_charge": SHARED_CHARGE,
            },
            "carrier_profile": {
                "t": 3,
                "a_i": [3, 2, 2],
                "charge": SHARED_CHARGE,
                "carrier_is_bookkeeping_only": True,
            },
        },
        "result": {
            "post_32221_scope_charge": scope_current_charge,
            "post_32221_scope_unresolved_charge": scope_unresolved_charge,
            "shared_envelope_charge": SHARED_CHARGE,
            "incremental_saved_mass": scope_current_charge - SHARED_CHARGE,
            "unresolved_saved_mass": scope_unresolved_charge - SHARED_CHARGE,
            "shared_charge_count": sum(
                int(row["shared_layer_envelope_carrier"])
                for row in banked_rows
                if is_shared_scope(row)
            ),
            "zero_increment_profile_count": sum(
                int(row["refined_injection_bound"] == 0)
                for row in banked_rows
                if is_shared_scope(row)
            ),
        },
        "ledger_consequence": {
            "prior_all_profile_bound": prior_all,
            "prior_unresolved_bound": prior_unresolved_total,
            "prior_profile_sha256": sha256_json(prior_rows),
            "candidate_result": {
                "all_profile_bound": banked_all,
                "unresolved_bound": banked_unresolved_total,
                "profile_sha256": sha256_json(banked_rows),
                "largest_remaining_unresolved_profile": largest,
            },
            "banked": True,
            "closure_verdict": "POSITIVE_UNRESOLVED_MASS_REMAINS",
        },
        "linked_inputs": links,
        "proof_status": {
            "exact": [
                "the post-32221 75-row ledger and profile hash are replayed",
                "all fifteen and only d=4,r=1 profile cells are selected",
                "the theorem bounds their disjoint union by 72 once",
                "one carrier receives 72 and fourteen cells receive zero incremental charge",
                "the all-profile and unresolved totals are recomputed from all 75 rows",
                "the next largest row is selected dynamically",
                "the prior ledger, owner partition, common cap, theorem source, and note are hash-linked",
            ],
            "review_gate": (
                "fresh independent and Claude cross-model reviews GREEN; "
                "ledger authorization YES"
            ),
        },
        "nonclaims": [
            "zero incremental charge is not a standalone zero bound for any profile",
            "the stronger possible cross-R0 charge 36 is not used",
            "no d=4,r=0 payment is included",
            "no global mixed-petal theorem, m>2, PR #763, or Lean claim is made",
        ],
        "verdict": "GREEN_LOCAL_SHARED_AUXILIARY_LEDGER_BANKED",
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
            and len(profiles) == 15
            and tuple(
                (
                    int(row["coordinates"]["t"]),
                    tuple(int(hit) for hit in row["coordinates"]["a_i"]),
                )
                for row in profiles
            )
            == EXPECTED_SCOPE_KEYS
            and scope["profile_sha256"] == sha256_json(profiles)
            and scope["strict_johnson_audit"]["margin"] == 1
            and scope["strict_johnson_audit"]["shared_envelope_charge"] == 72
            and result["shared_charge_count"] == 1
            and result["zero_increment_profile_count"] == 14
            and result["post_32221_scope_charge"] == 416_020
            and result["shared_envelope_charge"] == 72
            and ledger["candidate_result"]["all_profile_bound"] == 776_979
            and ledger["candidate_result"]["unresolved_bound"] == 212_755
            and ledger["banked"] is True
            and report["verdict"]
            == "GREEN_LOCAL_SHARED_AUXILIARY_LEDGER_BANKED"
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
    changed["shared_scope"]["profiles"][0]["incremental_charge_after_regrouping"] = 36
    changed["shared_scope"]["profile_sha256"] = sha256_json(
        changed["shared_scope"]["profiles"]
    )
    mutations.append(("per_profile_multiplication", changed))

    changed = copy.deepcopy(report)
    changed["result"]["shared_charge_count"] = 2
    mutations.append(("duplicate_72_charge", changed))

    changed = copy.deepcopy(report)
    changed["shared_scope"]["strict_johnson_audit"]["margin"] = 0
    mutations.append(("strict_margin", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"]["all_profile_bound"] += 1
    mutations.append(("all_profile_total", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"]["unresolved_bound"] -= 72
    mutations.append(("unresolved_convention", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["prior_banked_ledger"]["sha256"] = "0" * 64
    mutations.append(("prior_ledger_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["common_fixed_layer_cap"]["sha256"] = "0" * 64
    mutations.append(("common_cap_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["sharp_theorem_source"]["sha256"] = "0" * 64
    mutations.append(("theorem_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["independent_review"]["sha256"] = "0" * 64
    mutations.append(("independent_review_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["cross_model_review"]["sha256"] = "0" * 64
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
        raise RuntimeError("internally generated shared-owner ledger failed validation")
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
        raise RuntimeError("frozen shared-owner ledger certificate drift")
    ledger = report["ledger_consequence"]
    largest = ledger["candidate_result"]["largest_remaining_unresolved_profile"]
    print("PASS l1-b9-frontier-41331-shared-auxiliary-ledger")
    print(
        f"  shared scope: {report['shared_scope']['profile_count']} profiles, "
        f"{report['result']['post_32221_scope_charge']} -> "
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
