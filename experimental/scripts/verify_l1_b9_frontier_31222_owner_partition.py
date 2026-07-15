#!/usr/bin/env python3
"""Exact existing-owner partition for the GF(19) ``(3,1,3,(2,2,2))`` frontier.

The frozen sequential sunflower has

    (p,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2).

For every retained background point and every labelled choice of two points in
each of the three petals, apply exactly one first-match status in this order:

    periodic quotient,
    invariant quotient descent,
    fixed-(D,R0) auxiliary Johnson,
    global Johnson,
    B11 G2,
    B11 GR,
    UNPAID_PRIMITIVE.

The 432 cofactor-support patterns do not record which one of the four core
points is the restored agreement.  The script therefore also enumerates all
1,728 restored-core refinements before testing periodicity.  The existing
one-support-one-line theorem pays each periodic full support directly, without
requiring witness-data descent.  A whole cofactor-support pattern is not
removed merely because one of its four refinements is periodic: the ``q^2``
cofactor injection has not been decomposed into disjoint per-core-hit charges.

``UNPAID_PRIMITIVE`` is the required terminal label, but it means unpaid only
relative to this named existing-owner stack.  It is not a certificate of full
primitivity and does not assert that later rank, planted, pencil, or saturation
charts are absent.  The script performs no algebraic rank classification.
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
    / "experimental/data/certificates/l1-b9-frontier-31222-owner-partition/certificate.json"
)
PREVIOUS_LEDGER_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-m2-full-rank-ledger/certificate.json"
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
    "r": 1,
    "t": 3,
    "a_i": [2, 2, 2],
    "G2": 4,
    "GR": 5,
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
    """Return nontrivial uniform fibre sizes whose cyclic shifts fix support."""
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
    tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]
]:
    support_choices = [tuple(itertools.combinations(petal, 2)) for petal in PETALS]
    return [
        (background_support, tuple(supports))
        for background_support in itertools.combinations(BACKGROUND, 1)
        for supports in itertools.product(*support_choices)
    ]


def canonical_assignment(
    background_support: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    selected = tuple(sorted(background_support + sum(supports, ())))
    return {
        "background_support": list(background_support),
        "petal_supports": [list(support) for support in supports],
        "selected_cofactor_support": list(selected),
        "selected_cofactor_support_mask": mask_from_indices(selected),
    }


def pattern_record(
    background_support: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    selected = tuple(sorted(background_support + sum(supports, ())))
    selected_mask = mask_from_indices(selected)
    selected_stabilizer = stabilizer_order(selected_mask, N)
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
    refinement_owner_histogram = Counter(str(row["owner"]) for row in refinements)
    stabilizer_histogram = Counter(str(row["stabilizer_order"]) for row in refinements)
    lambda_j = johnson_slack_needed(N, K, S)
    b11 = b11_frontier_record(
        ell=ELL,
        petal_count=len(PETALS),
        d=3,
        r=1,
        a_i=[2, 2, 2],
        agreement_slack=0,
        lambda_j=lambda_j,
        maximal=True,
    )
    box = classify_b11_box(b11, E=0, V2=0, VR=0)
    auxiliary = b11["auxiliary_johnson"]
    gates: dict[str, object] = {
        "periodicity": {
            "selected_cofactor_support_stabilizer_order": selected_stabilizer,
            "restored_core_refinement_count": len(refinements),
            "full_support_stabilizer_histogram": dict(sorted(stabilizer_histogram.items())),
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
            "periodic_refinements_removed_at_prior_owner": len(periodic_refinements),
            "remaining_aperiodic_refinement_count": len(refinements) - len(periodic_refinements),
            "data_certified_refinement_count": 0,
            "all_witness_data_descend": False,
            "data_gate_status": "NOT_REACHED_ON_REMAINING_APERIODIC_REFINEMENTS",
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
    owner = owner_from_gates(gates)
    return {
        "pattern_id": (
            f"b{background_support[0]}-"
            + "-".join("s" + ".".join(map(str, support)) for support in supports)
        ),
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
            "aggregate cofactor-support pattern remains unpaid; this is not "
            "a fully primitive residual certificate"
        ),
    }


def previous_ledger_record() -> dict[str, object]:
    previous = json.loads(PREVIOUS_LEDGER_PATH.read_text(encoding="utf-8"))
    if previous["schema"] != "rs-mca-l1-b9-m2-full-rank-ledger-v5":
        raise RuntimeError("previous ledger schema drift")
    q19 = previous["cases"][0]
    target = q19["largest_remaining_unresolved_profile"]
    expected_target = {
        "d": 3,
        "r": 1,
        "t": 3,
        "a_i": [2, 2, 2],
        "G2": 4,
        "GR": 5,
        "support_pattern_count": 432,
        "selected_injection_bound": 155_952,
    }
    if any(target[key] != value for key, value in expected_target.items()):
        raise RuntimeError("previous ledger target drift")
    addback = q19["complete_finite_addback"]
    return {
        "path": str(PREVIOUS_LEDGER_PATH.relative_to(ROOT)),
        "sha256": sha256_file(PREVIOUS_LEDGER_PATH),
        "schema": previous["schema"],
        "all_profile_bound": int(addback["new_all_profile_bound"]),
        "unresolved_bound": int(addback["new_unresolved_bound"]),
        "target": expected_target,
    }


def build_report() -> dict[str, object]:
    patterns = [
        pattern_record(background_support, supports)
        for background_support, supports in expected_support_assignments()
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
    residual_charge = unpaid_count * P**2
    paid_count = len(patterns) - unpaid_count
    paid_mass = 155_952 - residual_charge
    return {
        "schema": "rs-mca-l1-b9-frontier-31222-owner-partition-v3",
        "status": "AUDIT/EXACT_GF19_EXISTING_OWNER_PARTITION",
        "statement": (
            "assign exactly one first-match existing owner or UNPAID_PRIMITIVE "
            "to every support pattern in (ell,d,r,t,a_i)=(4,3,1,3,(2,2,2))"
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
            "support_pattern_formula": "binom(2,1)*binom(4,2)^3=432",
            "support_pattern_count": len(patterns),
            "restored_core_refinement_count": len(refinements),
            "periodic_full_support_refinement_count": len(periodic_refinements),
            "patterns_with_periodic_full_support_refinement": patterns_with_periodic_refinement,
            "paid_periodic_full_support_refinement_count": len(periodic_refinements),
            "periodic_support_owner_bound": len(periodic_refinements),
            "refinement_owner_histogram": dict(sorted(refinement_owner_histogram.items())),
            "owner_histogram": dict(sorted(owner_histogram.items())),
            "paid_existing_owner_patterns": paid_count,
            "unpaid_primitive_patterns": unpaid_count,
            "transcript_sha256": sha256_json(patterns),
        },
        "ledger_consequence": {
            "old_profile_charge": 155_952,
            "periodic_support_owner_bound": len(periodic_refinements),
            "why_periodic_bound_is_not_subtracted": (
                "the q^2 cofactor injection is aggregate over four restored-core "
                "refinements and no disjoint bound for the three aperiodic "
                "refinements has been proved"
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
                "all 432 labelled support patterns are enumerated",
                "all 1,728 restored-core full-support refinements are enumerated",
                "every pattern receives exactly one status under the frozen owner order",
                "nine full-support refinements are periodic and each has the existing one-support-one-line owner bound one",
                "the aggregate q^2 cofactor charge is unchanged because no disjoint per-core-hit cofactor injection has been proved",
                "periodicity and complete-fibre tests use the exact cyclic index action",
                "Johnson and B11 coordinates use exact integers",
            ],
            "still_required": [
                "algebraic classification of the unpaid primitive residual",
                "independent review before any later charge is banked",
            ],
        },
        "nonclaims": [
            "UNPAID_PRIMITIVE is relative to this existing-owner stack only",
            "UNPAID_PRIMITIVE is not a certificate of full primitivity",
            "the selected seven-point cofactor support is not the full eight-point agreement support",
            "periodic support counting is distinct from invariant quotient descent",
            "data descent is not required for the one-support-one-line periodic owner",
            "no rank, planted, pencil, or saturation classification is made",
            "no m>2 or PR #763 statement is made",
        ],
        "verdict": "YELLOW - all 432 patterns survive the existing-owner stack; algebra is required.",
    }


def validate_report(report: dict[str, object]) -> bool:
    patterns = report["patterns"]
    result = report["result"]
    ledger = report["ledger_consequence"]
    expected_assignments = [
        canonical_assignment(background_support, supports)
        for background_support, supports in expected_support_assignments()
    ]
    observed_assignments = [
        {
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
    current_previous_hash = sha256_file(PREVIOUS_LEDGER_PATH)
    return (
        report["schema"] == "rs-mca-l1-b9-frontier-31222-owner-partition-v3"
        and len(patterns) == 432
        and len(set(ids)) == 432
        and observed_assignments == expected_assignments
        and len(set(masks)) == 432
        and all(int(row["selected_cofactor_support_size"]) == 7 for row in patterns)
        and all(len(row["restored_core_refinements"]) == 4 for row in patterns)
        and all(row["profile"] == PROFILE for row in patterns)
        and all(row["owner_order"] == list(OWNER_ORDER) for row in patterns)
        and all(row["owner"] == owner_from_gates(row["gates"]) for row in patterns)
        and all(row["owner"] == "UNPAID_PRIMITIVE" for row in patterns)
        and all(row["gates"]["periodicity"]["selected_cofactor_support_stabilizer_order"] == 1 for row in patterns)
        and all(not row["gates"]["periodicity"]["paid"] for row in patterns)
        and sum(
            refinement["owner"] == "PAID_PERIODIC_SUPPORT_COUNT"
            for row in patterns
            for refinement in row["restored_core_refinements"]
        ) == 9
        and all(
            refinement["paid"] == refinement["support_periodic"]
            for row in patterns
            for refinement in row["restored_core_refinements"]
        )
        and all(not row["gates"]["quotient_descent"]["paid"] for row in patterns)
        and all(row["gates"]["auxiliary_johnson"]["margin"] == 0 for row in patterns)
        and all(not row["gates"]["global_johnson"]["paid"] for row in patterns)
        and all(row["gates"]["b11"]["classification"] == "ESCAPES_BOUNDED_EXCESS_BOX" for row in patterns)
        and dict(sorted(owner_histogram.items())) == result["owner_histogram"]
        and int(result["support_pattern_count"]) == 432
        and int(result["restored_core_refinement_count"]) == 1_728
        and int(result["periodic_full_support_refinement_count"]) == 9
        and int(result["patterns_with_periodic_full_support_refinement"]) == 9
        and int(result["paid_periodic_full_support_refinement_count"]) == 9
        and int(result["periodic_support_owner_bound"]) == 9
        and result["refinement_owner_histogram"]
        == {"PAID_PERIODIC_SUPPORT_COUNT": 9, "UNPAID_AFTER_PERIODICITY": 1_719}
        and int(result["unpaid_primitive_patterns"]) == 432
        and int(result["paid_existing_owner_patterns"]) == 0
        and result["transcript_sha256"] == sha256_json(patterns)
        and report["previous_ledger"]["sha256"] == current_previous_hash
        and int(ledger["old_profile_charge"]) == 155_952
        and int(ledger["periodic_support_owner_bound"]) == 9
        and int(ledger["paid_mass_removed"]) == 0
        and int(ledger["residual_profile_charge"]) == 155_952
        and int(ledger["new_all_profile_bound"]) == 1_503_967
        and int(ledger["new_unresolved_bound"]) == 668_803
    )


def tamper_selftest(report: dict[str, object]) -> int:
    mutations = []
    changed = copy.deepcopy(report)
    source = changed["patterns"][0]
    target = changed["patterns"][1]
    for field in (
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
    changed["patterns"][0]["owner"] = "PAID_B11_G2"
    mutations.append(("owner", changed))
    changed = copy.deepcopy(report)
    changed["patterns"][0]["gates"]["auxiliary_johnson"]["margin"] = 1
    mutations.append(("auxiliary_margin", changed))
    changed = copy.deepcopy(report)
    changed["result"]["periodic_full_support_refinement_count"] = 8
    mutations.append(("periodic_refinements", changed))
    changed = copy.deepcopy(report)
    changed["result"]["owner_histogram"] = {"PAID_PERIODIC_QUOTIENT": 432}
    mutations.append(("owner_histogram", changed))
    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["paid_mass_removed"] = 1
    mutations.append(("ledger_mass", changed))
    changed = copy.deepcopy(report)
    changed["previous_ledger"]["sha256"] = "0" * 64
    mutations.append(("ledger_link", changed))
    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<20}: {'CAUGHT' if caught else 'MISSED'}")
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
    print("L1 B9 frontier (3,1,3,(2,2,2)) existing-owner partition")
    print(f"  support patterns: {report['result']['support_pattern_count']}")
    print(
        "  full-support refinements: "
        f"{report['result']['restored_core_refinement_count']} "
        f"({report['result']['paid_periodic_full_support_refinement_count']} "
        "paid by periodic support count)"
    )
    print(f"  owner histogram: {report['result']['owner_histogram']}")
    print(
        "  ledger: unresolved "
        f"{report['ledger_consequence']['old_unresolved_bound']} -> "
        f"{report['ledger_consequence']['new_unresolved_bound']}"
    )
    print(f"  transcript: {report['result']['transcript_sha256']}")
    print(f"  proof status: {report['status']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
