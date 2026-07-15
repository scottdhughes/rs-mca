#!/usr/bin/env python3
"""Bank the independently reviewed 32221 reduced-CRT row refinement.

This verifier reconstructs the complete v4 finite profile list, replays the
already-banked 31222 replacement, checks that the result exactly matches the
content-addressed 513,283 ledger, and then applies one further replacement:

    (ell,d,r,t,a_i) = (4,3,2,3,(2,2,1))
    432*19^2 = 155,952  ->  432.

It links the owner, Sage, CAS, proof-note, independent-review, and prior-ledger
inputs; validates all 432 canonical assignments; recomputes both complete
integer sums and the next largest unresolved row; and rejects mutation of a
pattern charge, canonical assignment, total, or load-bearing link.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable

from verify_l1_b9_m2_full_rank_ledger import build_report as build_v4_ledger


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIR = ROOT / "experimental/data/certificates/l1-b9-frontier-32221"
CERTIFICATE_PATH = CERTIFICATE_DIR / "ledger_certificate.json"
SAGE_CERTIFICATE_PATH = CERTIFICATE_DIR / "certificate.json"
CAS_CERTIFICATE_PATH = CERTIFICATE_DIR / "cas_certificate.json"
OWNER_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-32221-owner-partition/certificate.json"
)
PRIOR_BANKED_LEDGER_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/ledger_certificate.json"
)
LEMMA_NOTE_PATH = (
    ROOT / "experimental/notes/l1/l1_b9_frontier_32221_reduced_crt_lemma.md"
)
REVIEW_NOTE_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_32221_reduced_crt_independent_review.md"
)

UNRESOLVED_ROUTES = {
    "ESCAPES_BY_COFACTOR_EXCESS",
    "ESCAPES_BOUNDED_EXCESS_BOX",
}


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


def is_31222(row: dict[str, object]) -> bool:
    return (
        int(row["d"]) == 3
        and int(row["d_minus_ell"]) == -1
        and int(row["r"]) == 1
        and int(row["t"]) == 3
        and row["a_i"] == [2, 2, 2]
        and int(row["G2"]) == 4
        and int(row["GR"]) == 5
    )


def is_32221(row: dict[str, object]) -> bool:
    return (
        int(row["d"]) == 3
        and int(row["d_minus_ell"]) == -1
        and int(row["r"]) == 2
        and int(row["t"]) == 3
        and row["a_i"] == [2, 2, 1]
        and int(row["G2"]) == 4
        and int(row["GR"]) == 4
    )


def canonical_assignment(pattern: dict[str, object]) -> dict[str, object]:
    return {
        "background_support": list(pattern["background_support"]),
        "petal_supports": [list(support) for support in pattern["petal_supports"]],
        "labelled_occupancies": list(pattern["labelled_occupancies"]),
        "short_petal_label": int(pattern["short_petal_label"]),
        "selected_cofactor_support": list(pattern["selected_cofactor_support"]),
        "selected_cofactor_support_mask": int(
            pattern["selected_cofactor_support_mask"]
        ),
    }


def prior_31222_replacement(row: dict[str, object]) -> dict[str, object]:
    updated = dict(row)
    updated.update(
        {
            "refined_owner": "B9_FRONTIER_31222_REDUCED_CRT_DICHOTOMY",
            "refined_injection_exponent": 0,
            "refined_injection_bound": 432,
            "compatible_rankdrop_exact_d3_charge": 0,
            "full_rank_monic_cubic_charge": 432,
            "review_status": "CROSS_MODEL_GREEN_LEDGER_AUTHORIZED",
        }
    )
    return updated


def new_32221_replacement(row: dict[str, object]) -> dict[str, object]:
    updated = dict(row)
    updated.update(
        {
            "refined_owner": "B9_FRONTIER_32221_REDUCED_CRT_DICHOTOMY",
            "refined_injection_exponent": 0,
            "refined_injection_bound": 432,
            "compatible_rankdrop_exact_d3_charge": 0,
            "full_rank_monic_cubic_charge": 432,
            "review_status": "FRESH_INDEPENDENT_GREEN_LEDGER_AUTHORIZED",
        }
    )
    return updated


def linked_inputs() -> dict[str, object]:
    owner = load_json(OWNER_CERTIFICATE_PATH)
    sage = load_json(SAGE_CERTIFICATE_PATH)
    cas = load_json(CAS_CERTIFICATE_PATH)
    prior = load_json(PRIOR_BANKED_LEDGER_PATH)
    lemma_text = LEMMA_NOTE_PATH.read_text(encoding="utf-8")
    review_text = REVIEW_NOTE_PATH.read_text(encoding="utf-8")

    valid = (
        owner["schema"] == "rs-mca-l1-b9-frontier-32221-owner-partition-v1"
        and owner["result"]["support_pattern_count"] == 432
        and owner["result"]["unpaid_primitive_patterns"] == 432
        and owner["result"]["paid_existing_owner_patterns"] == 0
        and owner["ledger_consequence"]["new_unresolved_bound"] == 513_283
        and owner["previous_ledger"]["sha256"] == sha256_file(PRIOR_BANKED_LEDGER_PATH)
        and sage["schema"] == "rs-mca-l1-b9-frontier-32221-census-v1"
        and sage["result"]["support_pattern_count"] == 432
        and sage["result"]["fixed_matrix_rank_histogram"] == {"9": 432}
        and sage["result"]["moving_rank_histogram"]
        == {
            "rankC=11,rankAug=11": 1,
            "rankC=11,rankAug=12": 23,
            "rankC=12,rankAug=12": 408,
        }
        and sage["result"]["exact_target_codeword_count"] == 0
        and sage["owner_certificate"]["sha256"] == sha256_file(OWNER_CERTIFICATE_PATH)
        and cas["schema"] == "rs-mca-l1-b9-frontier-32221-reduced-crt-cas-v1"
        and cas["verdict"] == "GREEN_REPRESENTATIVE_CONTROL_ONLY"
        and cas["rank_census"]["histogram"]
        == {
            "rankM=2,rankAug=2": 1,
            "rankM=2,rankAug=3": 23,
            "rankM=3,rankAug=3": 408,
        }
        and not cas["certificate"]["generic_saturation_used"]
        and cas["linked_sage_certificate"]["sha256"] == sha256_file(SAGE_CERTIFICATE_PATH)
        and prior["schema"] == "rs-mca-l1-b9-frontier-31222-reduced-crt-ledger-v3"
        and prior["verdict"] == "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED"
        and prior["ledger_consequence"]["banked"]
        and prior["ledger_consequence"]["banked_result"]["all_profile_bound"]
        == 1_348_447
        and prior["ledger_consequence"]["banked_result"]["unresolved_bound"]
        == 513_283
        and "PROVED-LOCAL / fresh independent GREEN / BANKED" in lemma_text
        and "## Verdict" in review_text
        and "**GREEN - the local proof obligation is satisfied" in review_text
        and "## Ledger authorization" in review_text
        and "**YES.**" in review_text
    )
    if not valid:
        raise RuntimeError("32221 ledger input linkage failed")

    paths = {
        "owner_partition": OWNER_CERTIFICATE_PATH,
        "sage_census": SAGE_CERTIFICATE_PATH,
        "cas_replay": CAS_CERTIFICATE_PATH,
        "prior_banked_ledger": PRIOR_BANKED_LEDGER_PATH,
        "lemma_note": LEMMA_NOTE_PATH,
        "independent_review": REVIEW_NOTE_PATH,
    }
    schemas = {
        "owner_partition": owner["schema"],
        "sage_census": sage["schema"],
        "cas_replay": cas["schema"],
        "prior_banked_ledger": prior["schema"],
        "lemma_note": "markdown",
        "independent_review": "markdown",
    }
    return {
        name: {
            "path": str(path.relative_to(ROOT)),
            "schema": schemas[name],
            "sha256": sha256_file(path),
        }
        for name, path in paths.items()
    }


def reconstruct_current_banked_rows() -> list[dict[str, object]]:
    v4 = build_v4_ledger(include_profiles=True)
    rows = v4["cases"][0]["profiles"]
    if sum(is_31222(row) for row in rows) != 1:
        raise RuntimeError("expected exactly one 31222 row")
    current = [prior_31222_replacement(row) if is_31222(row) else dict(row) for row in rows]
    prior = load_json(PRIOR_BANKED_LEDGER_PATH)
    expected = prior["ledger_consequence"]["banked_result"]
    unresolved = [row for row in current if row["b11_box_route"] in UNRESOLVED_ROUTES]
    if (
        sum(int(row["refined_injection_bound"]) for row in current)
        != expected["all_profile_bound"]
        or sum(int(row["refined_injection_bound"]) for row in unresolved)
        != expected["unresolved_bound"]
        or sha256_json(current) != expected["profile_sha256"]
    ):
        raise RuntimeError("reconstructed post-31222 ledger drift")
    return current


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


def build_report() -> dict[str, object]:
    links = linked_inputs()
    owner = load_json(OWNER_CERTIFICATE_PATH)
    prior_rows = reconstruct_current_banked_rows()
    matches = [row for row in prior_rows if is_32221(row)]
    if len(matches) != 1:
        raise RuntimeError(f"expected one 32221 row, found {len(matches)}")
    target = matches[0]
    if (
        int(target["support_pattern_count"]) != 432
        or int(target["refined_injection_exponent"]) != 2
        or int(target["refined_injection_bound"]) != 155_952
    ):
        raise RuntimeError("32221 target charge drift")

    source_assignments = [canonical_assignment(pattern) for pattern in owner["patterns"]]
    if (
        len(source_assignments) != 432
        or len({sha256_json(assignment) for assignment in source_assignments}) != 432
        or len(
            {assignment["selected_cofactor_support_mask"] for assignment in source_assignments}
        )
        != 432
    ):
        raise RuntimeError("owner certificate has duplicate canonical assignments")

    pattern_owners = [
        {
            "pattern_id": pattern["pattern_id"],
            "canonical_assignment": canonical_assignment(pattern),
            "owner": "B9_FRONTIER_32221_REDUCED_CRT_DICHOTOMY",
            "charge": 1,
            "unpaid_primitive": False,
            "promotion_status": "FRESH_INDEPENDENT_GREEN_BANKED",
        }
        for pattern in owner["patterns"]
    ]

    banked_rows = [
        new_32221_replacement(row) if row is target else dict(row)
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
        prior_all != 1_348_447
        or prior_unresolved_total != 513_283
        or banked_all != 1_192_927
        or banked_unresolved_total != 357_763
    ):
        raise RuntimeError("recomputed 32221 ledger total drift")

    largest = banked_unresolved[0]
    largest_record = largest_row_record(largest)
    if not (
        largest_record["ell"] == 4
        and largest_record["d"] == 4
        and largest_record["r"] == 1
        and largest_record["t"] == 3
        and largest_record["a_i"] == [3, 3, 1]
        and largest_record["G2"] == 2
        and largest_record["GR"] == 4
        and largest_record["support_pattern_count"] == 384
        and largest_record["refined_injection_bound"] == 138_624
    ):
        raise RuntimeError("new largest unresolved row drift")

    return {
        "schema": "rs-mca-l1-b9-frontier-32221-reduced-crt-ledger-v1",
        "status": "EXACT_BANKED_LEDGER_REPLAY_FRESH_INDEPENDENT_GREEN",
        "statement": (
            "the independently reviewed 32221 reduced-CRT dichotomy replaces "
            "the q^2 charge by one on each of 432 canonical support keys"
        ),
        "profile": {
            "ell": 4,
            "d": 3,
            "r": 2,
            "t": 3,
            "a_i": [2, 2, 1],
            "G2": 4,
            "GR": 4,
        },
        "component_partition": [
            {
                "component": "rank(M)=3",
                "owner": "REDUCED_CRT_FULL_RANK_MONIC_UNIQUENESS",
                "bound_per_canonical_pattern": 1,
            },
            {
                "component": "rank(M)<3 and rank([M|-u])>rank(M)",
                "owner": "EMPTY_AFFINE_INCONSISTENT",
                "bound_per_canonical_pattern": 0,
            },
            {
                "component": "rank(M)<3 and rank([M|-u])=rank(M)",
                "algebraic_classification": "NONCONSTANT_GCD_PROVED",
                "owner": "EMPTY_EXACT_D3_BY_POINTWISE_CORE_AGREEMENT_MIGRATION",
                "bound_per_canonical_pattern": 0,
            },
        ],
        "pattern_owners": pattern_owners,
        "pattern_owner_sha256": sha256_json(pattern_owners),
        "result": {
            "support_pattern_count": 432,
            "owner_histogram": {
                "B9_FRONTIER_32221_REDUCED_CRT_DICHOTOMY": 432
            },
            "unpaid_primitive_patterns": 0,
            "prior_profile_charge": 155_952,
            "banked_profile_charge": 432,
            "banked_saved_mass": 155_520,
            "banked_change": -155_520,
        },
        "ledger_consequence": {
            "prior_all_profile_bound": prior_all,
            "prior_unresolved_bound": prior_unresolved_total,
            "prior_profile_sha256": sha256_json(prior_rows),
            "banked_result": {
                "all_profile_bound": banked_all,
                "unresolved_bound": banked_unresolved_total,
                "profile_sha256": sha256_json(banked_rows),
                "largest_remaining_unresolved_profile": largest_record,
            },
            "banked": True,
            "closure_verdict": "POSITIVE_UNRESOLVED_MASS_REMAINS",
        },
        "linked_inputs": links,
        "proof_status": {
            "exact": [
                "the full v4 profile list is reconstructed and the prior 31222 bank is hash-replayed",
                "all 432 canonical labelled assignments and masks are unique",
                "every 32221 pattern receives charge one after fresh independent GREEN review",
                "the complete all-profile and unresolved sums are recomputed from profile rows",
                "the new largest unresolved row is selected dynamically from the banked rows",
                "all load-bearing inputs are linked by SHA-256",
            ],
            "review_gate": "two fresh read-only GREEN reviews with ledger authorization YES",
        },
        "nonclaims": [
            "the 432 charge applies only to the frozen named profile",
            "positive unresolved mass remains",
            "no global mixed-petal theorem is proved",
            "no m>2, PR #763, or Lean claim is made",
        ],
        "verdict": "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED",
    }


def validate_report(report: dict[str, object]) -> bool:
    try:
        owner = load_json(OWNER_CERTIFICATE_PATH)
        expected_assignments = [
            canonical_assignment(pattern) for pattern in owner["patterns"]
        ]
        pattern_owners = report["pattern_owners"]
        observed_assignments = [
            entry["canonical_assignment"] for entry in pattern_owners
        ]
        observed_masks = {
            int(assignment["selected_cofactor_support_mask"])
            for assignment in observed_assignments
        }
        ledger = report["ledger_consequence"]
        largest = ledger["banked_result"]["largest_remaining_unresolved_profile"]
        return (
            report["schema"]
            == "rs-mca-l1-b9-frontier-32221-reduced-crt-ledger-v1"
            and report["status"]
            == "EXACT_BANKED_LEDGER_REPLAY_FRESH_INDEPENDENT_GREEN"
            and report["linked_inputs"] == linked_inputs()
            and len(pattern_owners) == 432
            and len({entry["pattern_id"] for entry in pattern_owners}) == 432
            and len({sha256_json(assignment) for assignment in observed_assignments})
            == 432
            and len(observed_masks) == 432
            and observed_assignments == expected_assignments
            and all(
                entry["owner"]
                == "B9_FRONTIER_32221_REDUCED_CRT_DICHOTOMY"
                and int(entry["charge"]) == 1
                and not entry["unpaid_primitive"]
                and entry["promotion_status"]
                == "FRESH_INDEPENDENT_GREEN_BANKED"
                for entry in pattern_owners
            )
            and report["pattern_owner_sha256"] == sha256_json(pattern_owners)
            and report["result"]["support_pattern_count"] == 432
            and report["result"]["unpaid_primitive_patterns"] == 0
            and report["result"]["prior_profile_charge"] == 155_952
            and report["result"]["banked_profile_charge"] == 432
            and report["result"]["banked_saved_mass"] == 155_520
            and ledger["prior_all_profile_bound"] == 1_348_447
            and ledger["prior_unresolved_bound"] == 513_283
            and ledger["banked"]
            and ledger["banked_result"]["all_profile_bound"] == 1_192_927
            and ledger["banked_result"]["unresolved_bound"] == 357_763
            and largest["ell"] == 4
            and largest["d"] == 4
            and largest["r"] == 1
            and largest["t"] == 3
            and largest["a_i"] == [3, 3, 1]
            and largest["G2"] == 2
            and largest["GR"] == 4
            and largest["support_pattern_count"] == 384
            and largest["refined_injection_bound"] == 138_624
            and report["component_partition"][-1]["owner"]
            == "EMPTY_EXACT_D3_BY_POINTWISE_CORE_AGREEMENT_MIGRATION"
            and report["verdict"] == "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED"
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
    mutations.append(("duplicate_assignment", changed))

    changed = copy.deepcopy(report)
    changed["pattern_owners"][0]["canonical_assignment"] = {
        "background_support": [99],
        "petal_supports": [[4, 5], [8, 9], [12]],
        "labelled_occupancies": [2, 2, 1],
        "short_petal_label": 2,
        "selected_cofactor_support": [4, 5, 8, 9, 12, 99],
        "selected_cofactor_support_mask": 1 << 99,
    }
    changed["pattern_owners"][0]["pattern_id"] = "fresh-id-foreign-assignment"
    changed["pattern_owner_sha256"] = sha256_json(changed["pattern_owners"])
    mutations.append(("foreign_assignment", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["banked_result"]["unresolved_bound"] += 1
    mutations.append(("ledger_total", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["banked_result"][
        "largest_remaining_unresolved_profile"
    ]["refined_injection_bound"] -= 1
    mutations.append(("largest_row_charge", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["prior_banked_ledger"]["sha256"] = "0" * 64
    mutations.append(("prior_ledger_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["independent_review"]["sha256"] = "0" * 64
    mutations.append(("review_link", changed))

    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<24}: {'CAUGHT' if caught else 'MISSED'}")
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
        raise RuntimeError("internally generated 32221 ledger failed validation")
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
        raise RuntimeError("frozen 32221 ledger certificate drift")
    result = report["result"]
    ledger = report["ledger_consequence"]
    largest = ledger["banked_result"]["largest_remaining_unresolved_profile"]
    print("PASS l1-b9-frontier-32221-reduced-crt-ledger")
    print(
        f"  profile: {result['prior_profile_charge']} -> "
        f"{result['banked_profile_charge']}"
    )
    print(
        f"  all profiles: {ledger['prior_all_profile_bound']} -> "
        f"{ledger['banked_result']['all_profile_bound']}"
    )
    print(
        f"  unresolved: {ledger['prior_unresolved_bound']} -> "
        f"{ledger['banked_result']['unresolved_bound']}"
    )
    print(
        "  next largest: "
        f"(d,r,a_i)=({largest['d']},{largest['r']},{largest['a_i']}), "
        f"charge={largest['refined_injection_bound']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
