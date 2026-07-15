#!/usr/bin/env python3
"""Exact existing-owner partition for the GF(19) ``(3,2,3,(2,2,1))`` row.

The frozen sequential sunflower has

    (p,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2).

There are

    3 * binom(4,2)^2 * binom(4,1) = 432

canonical labelled patterns: both background points are retained, exactly one
labelled petal contributes one point, and the other two labelled petals
contribute two points each.  Each pattern is assigned exactly one status in
the frozen first-match order

    periodic support;
    invariant quotient descent;
    auxiliary Johnson;
    global Johnson;
    B11 G2;
    B11 GR;
    UNPAID_PRIMITIVE.

The q^2 cofactor injection is aggregate over the four possible restored core
points.  A periodic full-support refinement is recorded and paid at the
refinement level, but it does not pay the whole canonical pattern unless the
aggregate injection has been decomposed.  No such decomposition is imported
here.  Likewise, quotient descent is fail-closed unless all witness data on
the remaining refinements are certified to descend through one declared
uniform fold.

``UNPAID_PRIMITIVE`` means only unpaid relative to this named existing-owner
stack.  It is the gate that authorizes a separate fixed-syndrome analysis; it
does not assert geometric primitivity.
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
    / "experimental/data/certificates/l1-b9-frontier-32221-owner-partition/certificate.json"
)
PREVIOUS_LEDGER_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/ledger_certificate.json"
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
PROFILE = {
    "ell": 4,
    "d": 3,
    "d_minus_ell": -1,
    "r": 2,
    "t": 3,
    "a_i": [2, 2, 1],
    "G2": 4,
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
OLD_PROFILE_CHARGE = 432 * P**2


def sha256_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask_from_indices(indices: tuple[int, ...]) -> int:
    return sum(1 << index for index in indices)


def shifted_mask(mask: int, shift: int) -> int:
    output = 0
    for index in range(N):
        if mask & (1 << index):
            output |= 1 << ((index + shift) % N)
    return output


def quotient_scales(mask: int) -> list[int]:
    """Return nontrivial uniform fibre sizes whose cyclic shift fixes support."""
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
        labelled_occupancies = tuple(
            1 if index == short_petal else 2 for index in range(len(PETALS))
        )
        support_choices = [
            tuple(itertools.combinations(petal, occupancy))
            for petal, occupancy in zip(PETALS, labelled_occupancies, strict=True)
        ]
        for supports in itertools.product(*support_choices):
            rows.append((BACKGROUND, tuple(supports)))
    return rows


def first_match_owner(gates: dict[str, object]) -> str:
    candidates = {
        "PAID_PERIODIC_SUPPORT_COUNT": bool(gates["periodicity"]["paid"]),
        "PAID_INVARIANT_QUOTIENT_DESCENT": bool(gates["quotient_descent"]["paid"]),
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
) -> dict[str, object]:
    occupancies = tuple(len(support) for support in supports)
    short_petal = occupancies.index(1)
    selected = tuple(sorted(background_support + sum(supports, ())))
    selected_mask = mask_from_indices(selected)
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
                "periodic_owner_bound": 1 if scales else None,
                "witness_data_descent_certified": False,
            }
        )
    periodic_refinements = [row for row in refinements if row["support_periodic"]]
    lambda_j = johnson_slack_needed(N, K, S)
    b11 = b11_frontier_record(
        ell=ELL,
        petal_count=len(PETALS),
        d=3,
        r=2,
        a_i=[2, 2, 1],
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
            "restored_core_refinement_count": len(refinements),
            "periodic_refinement_count": len(periodic_refinements),
            "periodic_core_hits": [row["core_hit"] for row in periodic_refinements],
            "partial_refinement_owner_bound": len(periodic_refinements),
            "aggregate_q2_injection_decomposed": False,
            "aggregate_pattern_paid": False,
            "paid": False,
        },
        "quotient_descent": {
            "periodic_refinements_removed_at_prior_owner": len(periodic_refinements),
            "remaining_aperiodic_refinement_count": len(refinements)
            - len(periodic_refinements),
            "declared_uniform_fold": None,
            "evaluation_domain_invariant": False,
            "support_descends": False,
            "received_data_descends": False,
            "explaining_polynomial_descends": False,
            "data_gate_status": "NO_DECLARED_ALL_DATA_DESCENT_CERTIFICATE",
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
    owner = first_match_owner(gates)
    key = canonical_key(background_support, supports)
    return {
        "pattern_id": (
            f"short{short_petal}-b16.17-"
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
        "restored_core_refinements": refinements,
        "profile": dict(PROFILE),
        "owner_order": list(OWNER_ORDER),
        "gates": gates,
        "owner": owner,
        "owner_charge": P**2 if owner == "UNPAID_PRIMITIVE" else None,
        "terminal_status_scope": (
            "unpaid only under the frozen existing-owner stack; algebraic "
            "primitivity is not asserted"
        ),
    }


def previous_ledger_record() -> dict[str, object]:
    previous = json.loads(PREVIOUS_LEDGER_PATH.read_text(encoding="utf-8"))
    if previous["schema"] != "rs-mca-l1-b9-frontier-31222-reduced-crt-ledger-v3":
        raise RuntimeError("previous ledger schema drift")
    consequence = previous["ledger_consequence"]
    if not consequence["banked"] or previous["verdict"] != "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED":
        raise RuntimeError("previous ledger is not banked GREEN")
    banked = consequence["banked_result"]
    target = banked["largest_remaining_unresolved_profile"]
    expected_target = {
        "ell": 4,
        "d": 3,
        "r": 2,
        "t": 3,
        "a_i": [2, 2, 1],
        "G2": 4,
        "GR": 4,
        "d_minus_ell": -1,
        "lambda": 0,
        "lambda_J": 1,
        "lambda_minus_lambda_J": -1,
        "b11_box_route": "ESCAPES_BOUNDED_EXCESS_BOX",
        "support_pattern_count": 432,
        "refined_injection_exponent": 2,
        "refined_injection_bound": OLD_PROFILE_CHARGE,
    }
    if target != expected_target:
        raise RuntimeError("previous ledger target drift")
    if banked["all_profile_bound"] != 1_348_447 or banked["unresolved_bound"] != 513_283:
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


def build_report() -> dict[str, object]:
    patterns = [pattern_record(background, supports) for background, supports in expected_assignments()]
    owner_histogram = Counter(str(row["owner"]) for row in patterns)
    refinements = [
        refinement
        for pattern in patterns
        for refinement in pattern["restored_core_refinements"]
    ]
    periodic_refinements = [row for row in refinements if row["support_periodic"]]
    patterns_with_periodic = sum(
        bool(pattern["gates"]["periodicity"]["periodic_refinement_count"])
        for pattern in patterns
    )
    previous = previous_ledger_record()
    unpaid_count = int(owner_histogram["UNPAID_PRIMITIVE"])
    paid_count = len(patterns) - unpaid_count
    residual_charge = sum(int(row["owner_charge"] or 0) for row in patterns)
    paid_mass = OLD_PROFILE_CHARGE - residual_charge
    return {
        "schema": "rs-mca-l1-b9-frontier-32221-owner-partition-v1",
        "status": "AUDIT/EXACT_GF19_EXISTING_OWNER_PARTITION",
        "statement": (
            "assign exactly one first-match existing owner or UNPAID_PRIMITIVE "
            "to every canonical support pattern in "
            "(ell,d,r,t,a_i)=(4,3,2,3,(2,2,1))"
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
        "previous_ledger": previous,
        "patterns": patterns,
        "result": {
            "support_pattern_formula": "3*binom(4,2)^2*binom(4,1)=432",
            "support_pattern_count": len(patterns),
            "canonical_assignment_count": len(
                {json.dumps(row["canonical_assignment"]) for row in patterns}
            ),
            "selected_cofactor_mask_count": len(
                {int(row["selected_cofactor_support_mask"]) for row in patterns}
            ),
            "restored_core_refinement_count": len(refinements),
            "periodic_full_support_refinement_count": len(periodic_refinements),
            "patterns_with_periodic_full_support_refinement": patterns_with_periodic,
            "periodic_refinement_owner_bound": len(periodic_refinements),
            "owner_histogram": dict(sorted(owner_histogram.items())),
            "paid_existing_owner_patterns": paid_count,
            "unpaid_primitive_patterns": unpaid_count,
            "transcript_sha256": sha256_json(patterns),
        },
        "ledger_consequence": {
            "old_profile_charge": OLD_PROFILE_CHARGE,
            "paid_existing_owner_patterns": paid_count,
            "periodic_refinement_owner_bound": len(periodic_refinements),
            "why_partial_periodic_mass_is_not_subtracted": (
                "the q^2 cofactor injection is aggregate over four restored-core "
                "refinements; each periodic refinement occurs in a different "
                "otherwise-unpaid canonical pattern"
            ),
            "paid_mass_removed": paid_mass,
            "residual_profile_charge": residual_charge,
            "old_all_profile_bound": previous["all_profile_bound"],
            "new_all_profile_bound": previous["all_profile_bound"] - paid_mass,
            "old_unresolved_bound": previous["unresolved_bound"],
            "new_unresolved_bound": previous["unresolved_bound"] - paid_mass,
            "largest_remaining_unresolved_profile": previous["target"],
            "ledger_recomputed": paid_mass > 0,
        },
        "proof_status": {
            "exact": [
                "all 432 canonical labelled support assignments are enumerated",
                "all 1,728 restored-core full-support refinements are enumerated",
                "every canonical pattern receives exactly one first-match status",
                "twelve full-support refinements have the existing periodic owner bound one",
                "the twelve periodic refinements lie in twelve distinct aggregate patterns",
                "auxiliary Johnson, global Johnson, and B11 coordinates use exact integers",
                "the banked 513,283 ledger is content-addressed and its target row is revalidated",
            ],
            "still_required": [
                "fixed-syndrome analysis of the 432 unpaid aggregate patterns",
                "independent review before any new algebraic charge is banked",
            ],
        },
        "nonclaims": [
            "UNPAID_PRIMITIVE is relative to this existing-owner stack only",
            "partial restored-core periodicity does not pay an aggregate q^2 pattern",
            "no invariant quotient descent is claimed without all-data descent",
            "no algebraic rank or component classification is made here",
            "no m>2, PR #763, Lean, commit, or GitHub action is made",
        ],
        "verdict": (
            "YELLOW - all 432 aggregate patterns survive the existing-owner stack; "
            "the fixed-syndrome gate is authorized."
        ),
    }


def validate_report(report: dict[str, object]) -> bool:
    patterns = report["patterns"]
    result = report["result"]
    ledger = report["ledger_consequence"]
    expected = expected_assignments()
    expected_keys = {
        json.dumps(canonical_key(background, supports), separators=(",", ":"))
        for background, supports in expected
    }
    actual_keys = [
        json.dumps(row["canonical_assignment"], separators=(",", ":"))
        for row in patterns
    ]
    ids = [str(row["pattern_id"]) for row in patterns]
    masks = [int(row["selected_cofactor_support_mask"]) for row in patterns]
    owner_histogram = Counter(str(row["owner"]) for row in patterns)
    current_previous_hash = sha256_file(PREVIOUS_LEDGER_PATH)
    return (
        report["schema"] == "rs-mca-l1-b9-frontier-32221-owner-partition-v1"
        and report["input"]["owner_order"] == list(OWNER_ORDER)
        and len(patterns) == 432
        and len(set(ids)) == 432
        and len(set(actual_keys)) == 432
        and set(actual_keys) == expected_keys
        and len(set(masks)) == 432
        and all(
            row["canonical_assignment"]
            == canonical_key(
                tuple(row["background_support"]),
                tuple(tuple(support) for support in row["petal_supports"]),
            )
            for row in patterns
        )
        and all(
            row["canonical_assignment_sha256"] == sha256_json(row["canonical_assignment"])
            for row in patterns
        )
        and all(row["labelled_occupancies"].count(1) == 1 for row in patterns)
        and all(row["labelled_occupancies"].count(2) == 2 for row in patterns)
        and all(row["short_petal_label"] == row["labelled_occupancies"].index(1) for row in patterns)
        and all(int(row["selected_cofactor_support_size"]) == 7 for row in patterns)
        and all(len(row["restored_core_refinements"]) == 4 for row in patterns)
        and all(row["profile"] == PROFILE for row in patterns)
        and all(row["owner_order"] == list(OWNER_ORDER) for row in patterns)
        and all(row["owner"] == first_match_owner(row["gates"]) for row in patterns)
        and all(row["owner"] == "UNPAID_PRIMITIVE" for row in patterns)
        and all(int(row["owner_charge"]) == P**2 for row in patterns)
        and all(not row["gates"]["periodicity"]["paid"] for row in patterns)
        and all(not row["gates"]["quotient_descent"]["paid"] for row in patterns)
        and all(row["gates"]["auxiliary_johnson"]["margin"] == -11 for row in patterns)
        and all(not row["gates"]["auxiliary_johnson"]["paid"] for row in patterns)
        and all(not row["gates"]["global_johnson"]["paid"] for row in patterns)
        and all(
            row["gates"]["b11"]["classification"] == "ESCAPES_BOUNDED_EXCESS_BOX"
            for row in patterns
        )
        and all(row["gates"]["b11"]["G2"] == 4 for row in patterns)
        and all(row["gates"]["b11"]["GR"] == 4 for row in patterns)
        and sum(
            refinement["support_periodic"]
            for row in patterns
            for refinement in row["restored_core_refinements"]
        )
        == 12
        and dict(sorted(owner_histogram.items())) == result["owner_histogram"]
        and int(result["support_pattern_count"]) == 432
        and int(result["canonical_assignment_count"]) == 432
        and int(result["selected_cofactor_mask_count"]) == 432
        and int(result["restored_core_refinement_count"]) == 1_728
        and int(result["periodic_full_support_refinement_count"]) == 12
        and int(result["patterns_with_periodic_full_support_refinement"]) == 12
        and int(result["periodic_refinement_owner_bound"]) == 12
        and int(result["paid_existing_owner_patterns"]) == 0
        and int(result["unpaid_primitive_patterns"]) == 432
        and result["transcript_sha256"] == sha256_json(patterns)
        and report["previous_ledger"]["sha256"] == current_previous_hash
        and report["previous_ledger"]["unresolved_bound"] == 513_283
        and int(ledger["old_profile_charge"]) == OLD_PROFILE_CHARGE
        and int(ledger["paid_existing_owner_patterns"]) == 0
        and int(ledger["paid_mass_removed"]) == 0
        and int(ledger["residual_profile_charge"]) == OLD_PROFILE_CHARGE
        and int(ledger["old_all_profile_bound"]) == 1_348_447
        and int(ledger["new_all_profile_bound"]) == 1_348_447
        and int(ledger["old_unresolved_bound"]) == 513_283
        and int(ledger["new_unresolved_bound"]) == 513_283
        and not ledger["ledger_recomputed"]
        and ledger["largest_remaining_unresolved_profile"] == report["previous_ledger"]["target"]
    )


def tamper_selftest(report: dict[str, object]) -> int:
    mutations = []

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
    ):
        target[field] = copy.deepcopy(source[field])
    target["pattern_id"] = "fresh-id-for-duplicated-assignment"
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("duplicate_assignment", changed))

    changed = copy.deepcopy(report)
    swapped_order = list(changed["input"]["owner_order"])
    swapped_order[0], swapped_order[1] = swapped_order[1], swapped_order[0]
    changed["input"]["owner_order"] = swapped_order
    for row in changed["patterns"]:
        row["owner_order"] = list(swapped_order)
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("owner_order", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["owner"] = "PAID_B11_G2"
    mutations.append(("owner_assignment", changed))

    changed = copy.deepcopy(report)
    changed["patterns"][0]["owner_charge"] -= 1
    changed["result"]["transcript_sha256"] = sha256_json(changed["patterns"])
    mutations.append(("charge", changed))

    changed = copy.deepcopy(report)
    changed["previous_ledger"]["sha256"] = "0" * 64
    mutations.append(("ledger_link", changed))

    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<24}: {'CAUGHT' if caught else 'MISSED'}")
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
    result = report["result"]
    ledger = report["ledger_consequence"]
    print("L1 B9 frontier (3,2,3,(2,2,1)) existing-owner partition")
    print(f"  support patterns: {result['support_pattern_count']}")
    print(
        "  full-support refinements: "
        f"{result['restored_core_refinement_count']} "
        f"({result['periodic_full_support_refinement_count']} periodic)"
    )
    print(f"  owner histogram: {result['owner_histogram']}")
    print(
        "  ledger: unresolved "
        f"{ledger['old_unresolved_bound']} -> {ledger['new_unresolved_bound']}"
    )
    print(f"  transcript: {result['transcript_sha256']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
