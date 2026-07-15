#!/usr/bin/env python3
"""Emit the fail-closed promotion certificate for the reduced-CRT lemma.

This verifier does not discover the local lemma.  It links the exact Sage
derivation/censuses, the representative Singular/Macaulay2 replay, the frozen
first-match owner partition, and the current finite B7--B11 ledger.  The
revised local lemma proves the pointwise bridge and exact-support assignment,
and the fresh cross-model review authorizes the ledger.  This verifier banks
the one-per-key charge ``432`` and rejects a duplicate canonical support
assignment even if its textual pattern identifier is fresh.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable

from verify_l1_b9_m2_full_rank_ledger import build_report as build_prior_ledger


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIR = (
    ROOT / "experimental/data/certificates/l1-b9-frontier-31222-reduced-crt"
)
CERTIFICATE_PATH = CERTIFICATE_DIR / "ledger_certificate.json"
LEMMA_CERTIFICATE_PATH = CERTIFICATE_DIR / "certificate.json"
CAS_CERTIFICATE_PATH = CERTIFICATE_DIR / "cas_certificate.json"
OWNER_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-owner-partition/certificate.json"
)
PRIOR_LEDGER_CERTIFICATE_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-m2-full-rank-ledger/certificate.json"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def render_certificate_json(report: dict[str, object]) -> str:
    """Pretty-print metadata while keeping each full owner row on one line."""
    marker = "__RS_MCA_CANONICAL_OWNER_ROWS__"
    rows = report["pattern_owners"]
    compact = dict(report)
    compact["pattern_owners"] = marker
    rendered = json.dumps(compact, indent=2, sort_keys=True)
    needle = f'  "pattern_owners": "{marker}"'
    if rendered.count(needle) != 1:
        raise RuntimeError("hybrid certificate marker drift")
    row_block = (
        '  "pattern_owners": [\n'
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


def target_row(row: dict[str, object]) -> bool:
    return (
        int(row["d"]) == 3
        and int(row["d_minus_ell"]) == -1
        and int(row["d"]) - int(row["d_minus_ell"]) == 4
        and int(row["r"]) == 1
        and int(row["t"]) == 3
        and row["a_i"] == [2, 2, 2]
        and int(row["G2"]) == 4
        and int(row["GR"]) == 5
    )


def canonical_assignment(pattern: dict[str, object]) -> dict[str, object]:
    return {
        "background_support": list(pattern["background_support"]),
        "petal_supports": [list(support) for support in pattern["petal_supports"]],
        "selected_cofactor_support": list(pattern["selected_cofactor_support"]),
        "selected_cofactor_support_mask": int(
            pattern["selected_cofactor_support_mask"]
        ),
    }


def linked_inputs() -> dict[str, object]:
    lemma = load_json(LEMMA_CERTIFICATE_PATH)
    cas = load_json(CAS_CERTIFICATE_PATH)
    owner = load_json(OWNER_CERTIFICATE_PATH)
    prior = load_json(PRIOR_LEDGER_CERTIFICATE_PATH)
    valid = (
        lemma["schema"]
        == "rs-mca-l1-b9-frontier-31222-reduced-crt-lemma-v3"
        and lemma["status"]
        == "PROVED_LOCAL_REDUCED_CRT_POINTWISE_BRIDGE_CROSS_MODEL_GREEN"
        and lemma["verdict"]
        == "GREEN_LOCAL_LEMMA_LEDGER_AUTHORIZED"
        and lemma["proof_certificate"]["semantic_bridge_status"]
        == "PROVED_POINTWISE_UNDER_EXPLICIT_HYPOTHESES"
        and lemma["exact_profile_assignment"]["codeword_to_key_injective"]
        and lemma["linked_inputs"]["fresh_cross_model_review"]["verdict"]
        == "GREEN"
        and lemma["linked_inputs"]["fresh_cross_model_review"]["ledger_authorization"]
        == "YES"
        and lemma["linked_inputs"]["fresh_cross_model_review"]["upstream_context_supplement"]
        == "GREEN"
        and bool(lemma["ledger_consequence"]["banked"])
        and cas["schema"] == "rs-mca-l1-b9-frontier-31222-reduced-crt-cas-v1"
        and cas["verdict"] == "GREEN_REPRESENTATIVE_CONTROL_ONLY"
        and not bool(cas["certificate"]["generic_saturation_used"])
        and owner["schema"] == "rs-mca-l1-b9-frontier-31222-owner-partition-v3"
        and owner["result"]["support_pattern_count"] == 432
        and owner["result"]["unpaid_primitive_patterns"] == 432
        and prior["schema"] == "rs-mca-l1-b9-m2-full-rank-ledger-v5"
        and prior["cases"][0]["complete_finite_addback"]["new_all_profile_bound"]
        == 1_503_967
        and prior["cases"][0]["complete_finite_addback"]["new_unresolved_bound"]
        == 668_803
    )
    if not valid:
        raise RuntimeError("reduced-CRT ledger input linkage failed")
    paths = {
        "lemma": LEMMA_CERTIFICATE_PATH,
        "cas": CAS_CERTIFICATE_PATH,
        "owner_partition": OWNER_CERTIFICATE_PATH,
        "prior_ledger": PRIOR_LEDGER_CERTIFICATE_PATH,
    }
    return {
        name: {
            "path": str(path.relative_to(ROOT)),
            "schema": load_json(path)["schema"],
            "sha256": sha256_file(path),
        }
        for name, path in paths.items()
    }


def build_report() -> dict[str, object]:
    links = linked_inputs()
    owner = load_json(OWNER_CERTIFICATE_PATH)
    prior = build_prior_ledger(include_profiles=True)
    prior_case = prior["cases"][0]
    rows = prior_case["profiles"]
    matches = [row for row in rows if target_row(row)]
    if len(matches) != 1:
        raise RuntimeError(f"expected one reduced-CRT target row, found {len(matches)}")
    old_row = matches[0]
    if (
        int(old_row["support_pattern_count"]) != 432
        or int(old_row["refined_injection_bound"]) != 155_952
        or int(old_row["refined_injection_exponent"]) != 2
    ):
        raise RuntimeError("target row charge drift")

    source_assignments = [canonical_assignment(pattern) for pattern in owner["patterns"]]
    if (
        len(source_assignments) != 432
        or len({sha256_json(assignment) for assignment in source_assignments}) != 432
        or len(
            {assignment["selected_cofactor_support_mask"] for assignment in source_assignments}
        )
        != 432
    ):
        raise RuntimeError("source owner certificate has duplicate canonical assignments")

    pattern_owners = []
    for pattern in owner["patterns"]:
        pattern_owners.append(
            {
                "pattern_id": pattern["pattern_id"],
                "canonical_assignment": canonical_assignment(pattern),
                "owner": "B9_FRONTIER_31222_REDUCED_CRT_DICHOTOMY",
                "charge": 1,
                "unpaid_primitive": False,
                "promotion_status": "BANKED_CROSS_MODEL_GREEN",
            }
        )
    if len(pattern_owners) != 432 or len(
        {entry["pattern_id"] for entry in pattern_owners}
    ) != 432:
        raise RuntimeError("pattern owner partition is not one-to-one")

    prior_rows = []
    banked_rows = []
    for row in rows:
        prior = dict(row)
        banked = dict(row)
        if row is old_row:
            prior.update(
                {
                    "refined_owner": "PRIOR_UNPAID_Q2_COFACTOR_INJECTION",
                    "refined_injection_exponent": 2,
                    "refined_injection_bound": 155_952,
                    "review_status": "PRIOR_BANKED_ROW",
                }
            )
            banked.update(
                {
                    "refined_owner": "B9_FRONTIER_31222_REDUCED_CRT_DICHOTOMY",
                    "refined_injection_exponent": 0,
                    "refined_injection_bound": 432,
                    "compatible_rankdrop_exact_d3_charge": 0,
                    "full_rank_monic_cubic_charge": 432,
                    "review_status": "CROSS_MODEL_GREEN_LEDGER_AUTHORIZED",
                }
            )
        prior_rows.append(prior)
        banked_rows.append(banked)

    unresolved_routes = {
        "ESCAPES_BY_COFACTOR_EXCESS",
        "ESCAPES_BOUNDED_EXCESS_BOX",
    }
    prior_unresolved_rows = [
        row for row in prior_rows if row["b11_box_route"] in unresolved_routes
    ]
    banked_unresolved_rows = [
        row
        for row in banked_rows
        if row["b11_box_route"] in unresolved_routes
    ]
    prior_unresolved_rows.sort(
        key=lambda row: int(row["refined_injection_bound"]), reverse=True
    )
    banked_unresolved_rows.sort(
        key=lambda row: int(row["refined_injection_bound"]), reverse=True
    )
    prior_largest = prior_unresolved_rows[0]
    banked_largest = banked_unresolved_rows[0]
    prior_all_profile_bound = sum(
        int(row["refined_injection_bound"]) for row in prior_rows
    )
    banked_all_profile_bound = sum(
        int(row["refined_injection_bound"]) for row in banked_rows
    )
    prior_unresolved_bound = sum(
        int(row["refined_injection_bound"]) for row in prior_unresolved_rows
    )
    banked_unresolved_bound = sum(
        int(row["refined_injection_bound"])
        for row in banked_unresolved_rows
    )
    if (
        prior_all_profile_bound != 1_503_967
        or prior_unresolved_bound != 668_803
        or banked_all_profile_bound != 1_348_447
        or banked_unresolved_bound != 513_283
    ):
        raise RuntimeError("recomputed ledger total drift")

    return {
        "schema": "rs-mca-l1-b9-frontier-31222-reduced-crt-ledger-v3",
        "status": "EXACT_BANKED_LEDGER_REPLAY_CROSS_MODEL_GREEN",
        "statement": (
            "the proved and cross-model-reviewed reduced-CRT bridge replaces "
            "the q^2 charge by one on each of 432 canonical cofactor-support "
            "keys"
        ),
        "profile": {
            "ell": 4,
            "d": 3,
            "r": 1,
            "t": 3,
            "a_i": [2, 2, 2],
            "G2": 4,
            "GR": 5,
        },
        "component_partition": [
            {
                "component": "rank(M)=3",
                "owner": "REDUCED_CRT_FULL_RANK_MONIC_UNIQUENESS",
                "bound_per_fixed_support_pattern": 1,
            },
            {
                "component": "rank(M)<3 and rank([M|u])>rank(M)",
                "owner": "EMPTY_AFFINE_INCONSISTENT",
                "bound_per_fixed_support_pattern": 0,
            },
            {
                "component": "rank(M)<3 and rank([M|u])=rank(M)",
                "algebraic_classification": "NONCONSTANT_GCD_PROVED",
                "owner": "EMPTY_EXACT_D3_BY_POINTWISE_CORE_AGREEMENT_MIGRATION",
                "bound_per_fixed_support_pattern": 0,
            },
        ],
        "pattern_owners": pattern_owners,
        "pattern_owner_sha256": sha256_json(pattern_owners),
        "result": {
            "support_pattern_count": 432,
            "owner_histogram": {
                "B9_FRONTIER_31222_REDUCED_CRT_DICHOTOMY": 432
            },
            "unpaid_primitive_patterns": 0,
            "prior_profile_charge": 155_952,
            "banked_profile_charge": 432,
            "banked_saved_mass": 155_520,
            "banked_change": -155_520,
        },
        "ledger_consequence": {
            "prior_all_profile_bound": prior_all_profile_bound,
            "prior_unresolved_bound": prior_unresolved_bound,
            "prior_profile_sha256": sha256_json(prior_rows),
            "prior_largest_remaining_unresolved_profile": {
                key: prior_largest[key]
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
            "banked_result": {
                "all_profile_bound": banked_all_profile_bound,
                "unresolved_bound": banked_unresolved_bound,
                "profile_sha256": sha256_json(banked_rows),
                "largest_remaining_unresolved_profile": {
                    **{"ell": int(banked_largest["d"]) - int(banked_largest["d_minus_ell"])},
                    **{
                    key: banked_largest[key]
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
                },
            },
            "banked": True,
            "closure_verdict": "POSITIVE_UNRESOLVED_MASS_REMAINS",
        },
        "linked_inputs": links,
        "proof_status": {
            "exact": [
                "all 432 canonical background-plus-three-petal assignments exactly match the owner certificate",
                "all canonical support tuples and masks are unique independently of pattern identifiers",
                "every banked pattern receives charge one and no exact-d3 rank-drop charge",
                "prior and banked integer sums are replayed from the v4 ledger",
                "all load-bearing inputs are linked by SHA-256",
            ],
            "review_gate": "fresh cross-model GREEN with ledger authorization YES",
        },
        "nonclaims": [
            "the banked 432 charge applies only to the frozen named profile",
            "no global mixed-petal theorem is proved",
            "no m>2 or PR #763 claim is made",
        ],
        "verdict": "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED",
    }


def validate_report(report: dict[str, object]) -> bool:
    try:
        links = report["linked_inputs"]
        current_links = linked_inputs()
        pattern_owners = report["pattern_owners"]
        result = report["result"]
        ledger = report["ledger_consequence"]
        component_partition = report["component_partition"]
        owner = load_json(OWNER_CERTIFICATE_PATH)
        expected_assignments = [
            canonical_assignment(pattern) for pattern in owner["patterns"]
        ]
        observed_assignments = [
            entry["canonical_assignment"] for entry in pattern_owners
        ]
        observed_assignment_hashes = {
            sha256_json(assignment) for assignment in observed_assignments
        }
        observed_masks = {
            int(assignment["selected_cofactor_support_mask"])
            for assignment in observed_assignments
        }
        largest = ledger["banked_result"][
            "largest_remaining_unresolved_profile"
        ]
        return (
            report["schema"]
            == "rs-mca-l1-b9-frontier-31222-reduced-crt-ledger-v3"
            and report["status"] == "EXACT_BANKED_LEDGER_REPLAY_CROSS_MODEL_GREEN"
            and links == current_links
            and len(pattern_owners) == 432
            and len({entry["pattern_id"] for entry in pattern_owners}) == 432
            and observed_assignments == expected_assignments
            and len(observed_assignment_hashes) == 432
            and len(observed_masks) == 432
            and all(
                entry["owner"]
                == "B9_FRONTIER_31222_REDUCED_CRT_DICHOTOMY"
                and int(entry["charge"]) == 1
                and not bool(entry["unpaid_primitive"])
                and entry["promotion_status"]
                == "BANKED_CROSS_MODEL_GREEN"
                for entry in pattern_owners
            )
            and report["pattern_owner_sha256"] == sha256_json(pattern_owners)
            and result["support_pattern_count"] == 432
            and result["unpaid_primitive_patterns"] == 0
            and result["prior_profile_charge"] == 155_952
            and result["banked_profile_charge"] == 432
            and result["banked_saved_mass"] == 155_520
            and result["banked_change"] == -155_520
            and component_partition[-1]["owner"]
            == "EMPTY_EXACT_D3_BY_POINTWISE_CORE_AGREEMENT_MIGRATION"
            and ledger["prior_all_profile_bound"] == 1_503_967
            and ledger["prior_unresolved_bound"] == 668_803
            and ledger["banked"]
            and ledger["prior_largest_remaining_unresolved_profile"][
                "refined_injection_bound"
            ]
            == 155_952
            and ledger["banked_result"]["all_profile_bound"]
            == 1_348_447
            and ledger["banked_result"]["unresolved_bound"]
            == 513_283
            and largest["ell"] == 4
            and largest["d"] == 3
            and largest["r"] == 2
            and largest["t"] == 3
            and largest["a_i"] == [2, 2, 1]
            and largest["G2"] == 4
            and largest["GR"] == 4
            and largest["refined_injection_bound"] == 155_952
            and report["verdict"]
            == "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED"
        )
    except (KeyError, TypeError, ValueError):
        return False


def tamper_selftest(report: dict[str, object]) -> int:
    mutations = []
    changed = copy.deepcopy(report)
    changed["pattern_owners"][0]["charge"] = 2
    mutations.append(("pattern_charge", changed))
    changed = copy.deepcopy(report)
    changed["pattern_owners"][1]["canonical_assignment"] = copy.deepcopy(
        changed["pattern_owners"][0]["canonical_assignment"]
    )
    changed["pattern_owners"][1]["pattern_id"] = "fresh-id-duplicate-assignment"
    changed["pattern_owner_sha256"] = sha256_json(changed["pattern_owners"])
    mutations.append(("duplicate_support_assignment", changed))
    changed = copy.deepcopy(report)
    changed["result"]["unpaid_primitive_patterns"] = 1
    mutations.append(("primitive_erasure", changed))
    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["banked_result"][
        "unresolved_bound"
    ] += 1
    mutations.append(("ledger_total", changed))
    changed = copy.deepcopy(report)
    changed["linked_inputs"]["lemma"]["sha256"] = "0" * 64
    mutations.append(("lemma_link", changed))
    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<22}: {'CAUGHT' if caught else 'MISSED'}")
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
        raise RuntimeError("internally generated ledger certificate failed validation")
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
        raise RuntimeError("frozen ledger certificate drift")
    print("PASS l1-b9-frontier-31222-reduced-crt-ledger")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
