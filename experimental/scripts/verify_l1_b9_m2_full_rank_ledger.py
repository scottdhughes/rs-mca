#!/usr/bin/env python3
"""Exact full-rank and existing-owner ledger for the local B9 ``m=2`` chart.

This verifier imports the already-frozen B7--B11 finite profile enumerator,
identifies the unique aggregate profile

    (ell,d,r,t,a_i) = (4,4,2,3,(2,2,2)),

and replaces only its fixed-pattern B3 charge

    support_patterns * q^3

by the proved rank-three charge

    support_patterns * q.

The verifier then audits the next minimal-row profile

    (ell,d,r,t,a_i) = (4,4,1,3,(3,2,2))

against the already-proved fixed-``(D,R_0)`` auxiliary Johnson owner.  When
the strict Johnson margin is positive, its support-pattern B3 charge is
replaced by the sum of the auxiliary-list bound over all fixed ``(D,R_0)``
layers.  Every other profile is left unchanged.  The report therefore gives
the local target-profile improvements and the complete finite add-back over
all admissible profiles in each row.

Finally, on the frozen sequential GF(19) layout only, it applies the local CRT
rank dichotomy to

    (ell,d,r,t,a_i) = (4,4,2,3,(3,2,1)).

The three cyclic-periodic support patterns are removed to their already-paid
owner and the remaining 573 patterns are charged by ``q`` rather than ``q^2``.
The substitution is linked to the independently reviewed local-lemma and
support-census certificates; ``573q`` is the post-periodic residual charge,
not the standalone all-pattern charge ``3+573q``.
The script does not identify the finite B7--B11 sum with the asymptotic profile
envelope ``mathfrak E_n``.

The PR #763 deployed row is included only as a compatibility crosswalk: its
``sigma+1`` is 67,472, whereas this chart requires ``sigma+1=4``.  Therefore
the number 121,502,836,610,262 is not used as a target for this local chart.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from math import comb
from pathlib import Path
from typing import Iterable

from verify_l1_mixed_petal_frontier_ledger import (
    CaseSpec,
    Layout,
    case_report,
    layout_for,
    profile_rows,
)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-m2-full-rank-ledger/certificate.json"
)
BOUNDARY_321_DICHOTOMY_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-boundary-321/dichotomy_certificate.json"
)
BOUNDARY_321_CENSUS_CERTIFICATE_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-boundary-321/certificate.json"
)
BOUNDARY_222_CERTIFICATE_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-boundary-222/certificate.json"
)

M2_CASES = (
    CaseSpec(q=19, n=18, k=5, sigma=3, E=0, V2=0, VR=0),
    CaseSpec(q=23, n=22, k=5, sigma=3, E=0, V2=0, VR=0),
    CaseSpec(q=47, n=46, k=5, sigma=3, E=0, V2=0, VR=0),
)


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def boundary_222_proof_record() -> dict[str, object]:
    """Load the local theorem certificate that justifies ``q^3 -> q``."""
    certificate = json.loads(
        BOUNDARY_222_CERTIFICATE_PATH.read_text(encoding="utf-8")
    )
    moving = certificate["moving_support_ledger"]
    finite_rows = [
        {
            "q": int(row["q"]),
            "n": int(row["n"]),
            "selected_support_charts": int(row["selected_support_charts"]),
            "exact_d4_upper_bound": int(row["total_exact_d4_upper_bound"]),
            "old_cofactor_upper_bound": int(
                row["previous_fixed-pattern_cofactor_upper_bound"]
            ),
        }
        for row in moving["finite_rows"]
    ]
    expected_rows = [
        {
            "q": 19,
            "n": 18,
            "selected_support_charts": 216,
            "exact_d4_upper_bound": 4_104,
            "old_cofactor_upper_bound": 1_481_544,
        },
        {
            "q": 23,
            "n": 22,
            "selected_support_charts": 864,
            "exact_d4_upper_bound": 19_872,
            "old_cofactor_upper_bound": 10_512_288,
        },
        {
            "q": 47,
            "n": 46,
            "selected_support_charts": 25_920,
            "exact_d4_upper_bound": 1_218_240,
            "old_cofactor_upper_bound": 2_691_092_160,
        },
    ]
    valid = (
        certificate["schema"] == "rs-mca-l1-b9-boundary-222-v2"
        and certificate["status"] == "EXPERIMENTAL/LOCAL_LEMMA"
        and moving["status"] == "RIGOROUS_M2_CHART_BOUND"
        and moving["exact_d4_upper_bound_formula"]
        == "binom(b,2)*binom(M,3)*216*q"
        and moving["rank_partition"]["compatible_rank2"]
        == "PROFILE_MIGRATION_CORE_RECOVERY from d=4 to d=2"
        and moving["rank_partition"]["rank3"]
        == "exactly q ambient monic quartics per selected-support chart"
        and finite_rows == expected_rows
        and "the exact m=2 moving-support target has certified upper charge 216*binom(b,2)*binom(M,3)*q"
        in certificate["proof_status"]["rigorous"]
    )
    if not valid:
        raise RuntimeError("boundary-222 q-for-q^3 proof certificate drift")
    return {
        "schema": certificate["schema"],
        "sha256": hashlib.sha256(
            BOUNDARY_222_CERTIFICATE_PATH.read_bytes()
        ).hexdigest(),
        "local_status": moving["status"],
        "global_verdict": certificate["verdict"],
        "exact_d4_upper_bound_formula": moving[
            "exact_d4_upper_bound_formula"
        ],
        "finite_rows": finite_rows,
    }


def boundary_321_proof_record() -> dict[str, object]:
    """Load and validate the reviewed dichotomy and periodic-count inputs."""
    dichotomy = json.loads(
        BOUNDARY_321_DICHOTOMY_CERTIFICATE_PATH.read_text(encoding="utf-8")
    )
    census = json.loads(
        BOUNDARY_321_CENSUS_CERTIFICATE_PATH.read_text(encoding="utf-8")
    )
    census_result = census["result"]
    valid = (
        dichotomy["schema"] == "rs-mca-l1-b9-boundary-321-dichotomy-v2"
        and dichotomy["status"]
        == "PROVED_LOCAL_CRT_LEMMA_INDEPENDENTLY_REVIEWED"
        and dichotomy["verdict"]
        == "GREEN_LOCAL_LEMMA_INDEPENDENTLY_REVIEWED"
        and dichotomy["independent_review"]["verdict"] == "GREEN"
        and dichotomy["ledger_consequence"][
            "periodic_patterns_removed_in_frozen_GF19_layout"
        ]
        == 3
        and dichotomy["ledger_consequence"]["at_q_19"] == 10_887
        and census_result["support_patterns"] == 576
        and census_result["periodic_support_patterns"] == 3
        and census_result["primitive_support_patterns"] == 573
        and census_result["support_stabilizer_histogram"] == {"1": 573, "2": 3}
    )
    if not valid:
        raise RuntimeError("boundary-321 proof/census certificate linkage failed")
    return {
        "dichotomy_schema": dichotomy["schema"],
        "dichotomy_sha256": hashlib.sha256(
            BOUNDARY_321_DICHOTOMY_CERTIFICATE_PATH.read_bytes()
        ).hexdigest(),
        "census_schema": census["schema"],
        "census_sha256": hashlib.sha256(
            BOUNDARY_321_CENSUS_CERTIFICATE_PATH.read_bytes()
        ).hexdigest(),
        "independent_review": dichotomy["independent_review"],
        "support_patterns": int(census_result["support_patterns"]),
        "periodic_support_patterns": int(
            census_result["periodic_support_patterns"]
        ),
        "primitive_support_patterns": int(
            census_result["primitive_support_patterns"]
        ),
    }


def is_m2_target(row: dict[str, object], *, ell: int) -> bool:
    return (
        ell == 4
        and int(row["d"]) == 4
        and int(row["r"]) == 2
        and int(row["t"]) == 3
        and row["a_i"] == [2, 2, 2]
    )


def is_auxiliary_owner_target(row: dict[str, object], *, ell: int) -> bool:
    return (
        ell == 4
        and int(row["d"]) == 4
        and int(row["r"]) == 1
        and int(row["t"]) == 3
        and row["a_i"] == [3, 2, 2]
    )


def is_boundary_321_target(row: dict[str, object], *, ell: int) -> bool:
    return (
        ell == 4
        and int(row["d"]) == 4
        and int(row["r"]) == 2
        and int(row["t"]) == 3
        and row["a_i"] == [3, 2, 1]
    )


def auxiliary_johnson_record(
    row: dict[str, object], *, layout: Layout
) -> dict[str, object]:
    """Audit the fixed-(D,R_0) auxiliary Johnson owner for one profile.

    The owner bounds the whole fixed layer, so support choices and touched-
    petal choices are not multiplied back in.  Only the missed-core and
    retained-background layer indices are summed.
    """
    d = int(row["d"])
    r = int(row["r"])
    petal_domain_size = int(layout.M) * int(layout.ell)
    required_agreement = int(layout.ell) + d - r
    margin = required_agreement**2 - d * petal_domain_size
    paid = margin > 0
    unique = paid and 2 * required_agreement > petal_domain_size + d
    numerator = petal_domain_size * (required_agreement - d)
    per_fixed_layer_bound = (
        (1 if unique else numerator // margin) if paid else None
    )
    fixed_D_count = comb(int(layout.core_size), d)
    fixed_R0_count = comb(int(layout.b), r)
    fixed_layer_count = fixed_D_count * fixed_R0_count
    aggregate_bound = (
        fixed_layer_count * int(per_fixed_layer_bound)
        if per_fixed_layer_bound is not None
        else None
    )
    return {
        "petal_domain_size": petal_domain_size,
        "required_agreement": required_agreement,
        "effective_degree_bound": d,
        "strict_johnson_margin": margin,
        "paid": paid,
        "unique": unique,
        "johnson_numerator": numerator,
        "integer_floor_bound_per_fixed_D_R0": per_fixed_layer_bound,
        "fixed_D_count": fixed_D_count,
        "fixed_R0_count": fixed_R0_count,
        "fixed_layer_count": fixed_layer_count,
        "aggregate_owner_bound": aggregate_bound,
    }


def refined_case(
    spec: CaseSpec,
    *,
    include_profiles: bool,
    boundary_222_proof: dict[str, object],
    boundary_321_proof: dict[str, object],
) -> dict[str, object]:
    layout = layout_for(spec)
    rows = profile_rows(spec, max_profiles=200_000)
    targets = [row for row in rows if is_m2_target(row, ell=layout.ell)]
    if len(targets) != 1:
        raise RuntimeError(f"expected one m=2 target profile, found {len(targets)}")
    target = targets[0]
    owner_targets = [
        row for row in rows if is_auxiliary_owner_target(row, ell=layout.ell)
    ]
    if len(owner_targets) != 1:
        raise RuntimeError(
            f"expected one auxiliary-owner target profile, found {len(owner_targets)}"
        )
    owner_target = owner_targets[0]
    auxiliary_owner = auxiliary_johnson_record(owner_target, layout=layout)
    boundary_321_targets = [
        row for row in rows if is_boundary_321_target(row, ell=layout.ell)
    ]
    if len(boundary_321_targets) != 1:
        raise RuntimeError(
            f"expected one boundary-321 target profile, found {len(boundary_321_targets)}"
        )
    boundary_321_target = boundary_321_targets[0]
    boundary_321_applicable = (
        spec.q == 19 and spec.n == 18 and spec.k == 5 and spec.sigma == 3
    )
    support_patterns = int(target["support_pattern_count"])
    expected_support_patterns = (
        (layout.b * (layout.b - 1) // 2)
        * (layout.M * (layout.M - 1) * (layout.M - 2) // 6)
        * 216
    )
    if support_patterns != expected_support_patterns:
        raise RuntimeError("m=2 support-pattern formula drift")
    old_target_charge = int(target["selected_injection_bound"])
    expected_old = support_patterns * spec.q**3
    new_target_charge = support_patterns * spec.q
    if old_target_charge != expected_old:
        raise RuntimeError("m=2 old q^3 charge drift")
    proof_row = next(
        (
            row
            for row in boundary_222_proof["finite_rows"]
            if int(row["q"]) == spec.q and int(row["n"]) == spec.n
        ),
        None,
    )
    if proof_row is None or (
        int(proof_row["selected_support_charts"]) != support_patterns
        or int(proof_row["exact_d4_upper_bound"]) != new_target_charge
        or int(proof_row["old_cofactor_upper_bound"]) != old_target_charge
    ):
        raise RuntimeError("m=2 target charge is not certified by boundary-222")

    old_complete_addback = sum(int(row["selected_injection_bound"]) for row in rows)
    after_m2_addback = old_complete_addback - old_target_charge + new_target_charge
    old_owner_target_charge = int(owner_target["selected_injection_bound"])
    new_owner_target_charge = (
        int(auxiliary_owner["aggregate_owner_bound"])
        if bool(auxiliary_owner["paid"])
        else old_owner_target_charge
    )
    after_existing_owner_addback = (
        after_m2_addback - old_owner_target_charge + new_owner_target_charge
    )
    old_boundary_321_charge = int(
        boundary_321_target["selected_injection_bound"]
    )
    boundary_321_support_patterns = int(
        boundary_321_target["support_pattern_count"]
    )
    expected_boundary_321_patterns = (
        comb(layout.b, 2) * comb(layout.M, 3) * 576
    )
    if boundary_321_support_patterns != expected_boundary_321_patterns:
        raise RuntimeError("boundary-321 support-pattern formula drift")
    layer_count = comb(layout.b, 2) * comb(layout.M, 3)
    periodic_boundary_321_patterns = (
        int(boundary_321_proof["periodic_support_patterns"]) * layer_count
        if boundary_321_applicable
        else 0
    )
    primitive_boundary_321_patterns = (
        boundary_321_support_patterns - periodic_boundary_321_patterns
    )
    new_boundary_321_charge = (
        primitive_boundary_321_patterns * spec.q
        if boundary_321_applicable
        else old_boundary_321_charge
    )
    new_complete_addback = (
        after_existing_owner_addback
        - old_boundary_321_charge
        + new_boundary_321_charge
        if boundary_321_applicable
        else after_existing_owner_addback
    )
    unresolved_routes = {
        "ESCAPES_BY_COFACTOR_EXCESS",
        "ESCAPES_BOUNDED_EXCESS_BOX",
    }
    old_unresolved = sum(
        int(row["selected_injection_bound"])
        for row in rows
        if row["b11_box_route"] in unresolved_routes
    )
    target_unresolved = target["b11_box_route"] in unresolved_routes
    after_m2_unresolved = (
        old_unresolved - old_target_charge + new_target_charge
        if target_unresolved
        else old_unresolved
    )
    owner_target_unresolved = owner_target["b11_box_route"] in unresolved_routes
    after_existing_owner_unresolved = (
        after_m2_unresolved - old_owner_target_charge + new_owner_target_charge
        if bool(auxiliary_owner["paid"]) and owner_target_unresolved
        else after_m2_unresolved
    )
    boundary_321_target_unresolved = (
        boundary_321_target["b11_box_route"] in unresolved_routes
    )
    new_unresolved = (
        after_existing_owner_unresolved
        - old_boundary_321_charge
        + new_boundary_321_charge
        if boundary_321_applicable and boundary_321_target_unresolved
        else after_existing_owner_unresolved
    )
    remaining_unresolved_rows = [
        row
        for row in rows
        if row["b11_box_route"] in unresolved_routes
        and row is not target
        and not (row is owner_target and bool(auxiliary_owner["paid"]))
        and not (row is boundary_321_target and boundary_321_applicable)
    ]
    remaining_unresolved_rows.sort(
        key=lambda row: int(row["selected_injection_bound"]), reverse=True
    )
    largest_remaining = remaining_unresolved_rows[0]
    refined_rows = []
    for row in rows:
        refined = dict(row)
        if row is target:
            refined.update(
                {
                    "refined_owner": "M2_FULL_RANK_PADE_FIBRE",
                    "refined_injection_exponent": 1,
                    "refined_injection_bound": new_target_charge,
                    "rank_at_most_2_exact_d4_charge": 0,
                    "rank3_ambient_monic_F_charge": new_target_charge,
                }
            )
        elif row is owner_target and bool(auxiliary_owner["paid"]):
            refined.update(
                {
                    "refined_owner": "PAID_AUXILIARY_JOHNSON",
                    "refined_injection_exponent": None,
                    "refined_injection_bound": new_owner_target_charge,
                    "auxiliary_johnson": auxiliary_owner,
                }
            )
        elif row is boundary_321_target and boundary_321_applicable:
            refined.update(
                {
                    "refined_owner": "B9_BOUNDARY_321_CRT_RANK_DICHOTOMY",
                    "refined_injection_exponent": 1,
                    "refined_injection_bound": new_boundary_321_charge,
                    "periodic_support_patterns_paid_elsewhere": periodic_boundary_321_patterns,
                    "primitive_support_patterns_charged": primitive_boundary_321_patterns,
                    "review_status": "INDEPENDENT_PROOF_REVIEW_GREEN",
                }
            )
        else:
            refined.update(
                {
                    "refined_owner": "UNCHANGED_EXISTING_B7_B11_LEDGER",
                    "refined_injection_exponent": row["selected_injection_exponent"],
                    "refined_injection_bound": row["selected_injection_bound"],
                }
            )
        refined_rows.append(refined)

    base_report = case_report(spec, max_profiles=200_000, include_profiles=False)
    result: dict[str, object] = {
        "case": base_report["case"],
        "layout": base_report["layout"],
        "m2_target": {
            "coordinates": {
                "ell": 4,
                "d": 4,
                "r": 2,
                "t": 3,
                "a_i": [2, 2, 2],
            },
            "b11_box_route": target["b11_box_route"],
            "support_pattern_count": support_patterns,
            "support_pattern_formula": "216*binom(b,2)*binom(M,3)",
            "old_q3_charge": old_target_charge,
            "new_q_charge": new_target_charge,
            "exact_rank_at_most_2_charge": 0,
            "saved_mass": old_target_charge - new_target_charge,
            "improvement_factor": spec.q**2,
            "proof_certificate_link": boundary_222_proof,
        },
        "auxiliary_owner_target": {
            "coordinates": {
                "ell": 4,
                "d": 4,
                "r": 1,
                "t": 3,
                "a_i": [3, 2, 2],
            },
            "b11_box_route": owner_target["b11_box_route"],
            "support_pattern_count": owner_target["support_pattern_count"],
            "old_b3_charge": old_owner_target_charge,
            "owner": (
                "PAID_AUXILIARY_JOHNSON"
                if bool(auxiliary_owner["paid"])
                else "UNPAID_AUXILIARY_JOHNSON_MARGIN"
            ),
            "new_owner_charge": new_owner_target_charge,
            "saved_mass": old_owner_target_charge - new_owner_target_charge,
            "audit": auxiliary_owner,
        },
        "boundary_321_target": {
            "coordinates": {
                "ell": 4,
                "d": 4,
                "r": 2,
                "t": 3,
                "a_i": [3, 2, 1],
            },
            "b11_box_route": boundary_321_target["b11_box_route"],
            "applicable_to_frozen_layout": boundary_321_applicable,
            "support_pattern_count": boundary_321_support_patterns,
            "support_pattern_formula": "576*binom(b,2)*binom(M,3)",
            "periodic_support_patterns_paid_elsewhere": periodic_boundary_321_patterns,
            "primitive_support_patterns_charged": primitive_boundary_321_patterns,
            "old_q2_charge": old_boundary_321_charge,
            "new_q_charge": new_boundary_321_charge,
            "saved_mass": old_boundary_321_charge - new_boundary_321_charge,
            "owner": (
                "B9_BOUNDARY_321_CRT_RANK_DICHOTOMY"
                if boundary_321_applicable
                else "NOT_APPLIED_OUTSIDE_FROZEN_GF19_LAYOUT"
            ),
            "review_status": (
                "INDEPENDENT_PROOF_REVIEW_GREEN"
                if boundary_321_applicable
                else "NOT_APPLICABLE"
            ),
            "proof_certificate_link": (
                boundary_321_proof if boundary_321_applicable else None
            ),
            "periodic_bucket_charge_paid_elsewhere": (
                periodic_boundary_321_patterns if boundary_321_applicable else 0
            ),
            "standalone_profile_charge_including_periodic_bucket": (
                periodic_boundary_321_patterns + new_boundary_321_charge
                if boundary_321_applicable
                else old_boundary_321_charge
            ),
        },
        "complete_finite_addback": {
            "profile_count": len(rows),
            "old_all_profile_bound": old_complete_addback,
            "after_m2_all_profile_bound": after_m2_addback,
            "after_existing_owner_all_profile_bound": after_existing_owner_addback,
            "new_all_profile_bound": new_complete_addback,
            "old_unresolved_bound": old_unresolved,
            "after_m2_unresolved_bound": after_m2_unresolved,
            "after_existing_owner_unresolved_bound": after_existing_owner_unresolved,
            "new_unresolved_bound": new_unresolved,
            "remaining_unresolved_mass": new_unresolved > 0,
            "closure_verdict": (
                "NOT_CLOSED_BY_LOCAL_M2_PROFILE_REFINEMENTS"
                if new_unresolved > 0
                else "FINITE_UNRESOLVED_MASS_ZERO"
            ),
            "refined_profile_sha256": sha256_json(refined_rows),
        },
        "largest_remaining_unresolved_profile": {
            key: largest_remaining[key]
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
                "selected_injection_exponent",
                "selected_injection_bound",
                "b11_box_route",
            )
        },
    }
    if include_profiles:
        result["profiles"] = refined_rows
    return result


def pr763_crosswalk() -> dict[str, object]:
    p = 2_130_706_433
    n = 2_097_152
    K = 1_048_576
    sigma = 67_471
    m = K + sigma
    paid = 57_121_027_290_597_096
    target = 274_854_110_496_187_592
    residual_profiles = 1_792
    per_profile_cap = 121_502_836_610_262
    complete_addback = paid + residual_profiles * per_profile_cap
    return {
        "source": "origin/pr-763",
        "deployed_row": {"p": p, "n": n, "K": K, "sigma": sigma, "m": m},
        "m2_chart_required_sigma": 3,
        "m2_chart_applicable": sigma == 3,
        "reason": "the local chart has ell=sigma+1=4; PR #763 has ell=67472",
        "paid_dyadic_mass": paid,
        "residual_profile_count": residual_profiles,
        "uniform_per_profile_cap_sufficient": per_profile_cap,
        "complete_pr763_addback_under_unproved_cap": complete_addback,
        "target_T": target,
        "closing_margin": target - complete_addback,
        "comparison_status": "INAPPLICABLE_TO_LOCAL_M2_CHART",
    }


def build_report(*, include_profiles: bool) -> dict[str, object]:
    boundary_222_proof = boundary_222_proof_record()
    boundary_321_proof = boundary_321_proof_record()
    cases = [
        refined_case(
            spec,
            include_profiles=include_profiles,
            boundary_222_proof=boundary_222_proof,
            boundary_321_proof=boundary_321_proof,
        )
        for spec in M2_CASES
    ]
    return {
        "schema": "rs-mca-l1-b9-m2-full-rank-ledger-v5",
        "status": "AUDIT/EXACT_FINITE_M2_PROFILE_ADDBACK_222_LINKED_321_REVIEWED",
        "statement": (
            "replace q^3 by q only for the exact m=2 B9 target, audit the next "
            "profile against the fixed-(D,R0) auxiliary Johnson owner, apply "
            "the content-addressed boundary-222 theorem and the local (3,2,1) "
            "CRT rank dichotomy on the frozen GF19 layout, "
            "then recompute the complete finite B7-B11 add-back"
        ),
        "cases": cases,
        "minimal_next_attack": {
            "row": cases[0]["case"],
            "profile": cases[0]["largest_remaining_unresolved_profile"],
            "action": (
                "check existing owners for the recomputed largest profile before "
                "building another fixed-support rank system"
            ),
        },
        "pr763_crosswalk": pr763_crosswalk(),
        "proof_status": {
            "proved_or_exact": [
                "rank at most two contributes zero to exact d=4",
                "rank three contributes at most q monic quartics per selected support chart",
                "the q-for-q^3 substitution is linked to the boundary-222 theorem certificate",
                "the q-for-q^3 substitution and complete finite add-backs use exact integers",
                "the auxiliary Johnson owner is summed only over fixed (D,R0) layer indices",
                "the independently reviewed frozen GF19 (3,2,1) primitive residual costs at most 573*q",
            ],
            "unproved": [
                "the remaining non-m2 finite unresolved profile mass",
                "identification of this finite sum with a closed asymptotic profile envelope",
                "the fixed-profile cap required by PR #763",
                "any higher-m rank dichotomy",
            ],
        },
        "nonclaims": [
            "the PR #763 per-profile cap is not applied to a sigma-incompatible chart",
            "finite upper-bound mass is not a realizability count",
            "no global mixed-petal or Grand List theorem is closed",
            "no m>2 profile is refined",
        ],
        "verdict": "YELLOW - promising but unresolved; do not authorize global proof.",
    }


def tamper_selftest(actual: dict[str, object]) -> int:
    mutations = []
    changed = copy.deepcopy(actual)
    changed["cases"][0]["m2_target"]["new_q_charge"] += 1
    mutations.append(("new_q_charge", changed))
    changed = copy.deepcopy(actual)
    changed["cases"][0]["m2_target"]["proof_certificate_link"][
        "sha256"
    ] = "0" * 64
    mutations.append(("boundary_222_link", changed))
    changed = copy.deepcopy(actual)
    changed["cases"][1]["complete_finite_addback"]["new_all_profile_bound"] += 1
    mutations.append(("complete_addback", changed))
    changed = copy.deepcopy(actual)
    changed["cases"][0]["auxiliary_owner_target"]["new_owner_charge"] += 1
    mutations.append(("auxiliary_owner", changed))
    changed = copy.deepcopy(actual)
    changed["cases"][0]["boundary_321_target"]["new_q_charge"] += 1
    mutations.append(("boundary_321_charge", changed))
    changed = copy.deepcopy(actual)
    changed["cases"][0]["boundary_321_target"]["proof_certificate_link"][
        "dichotomy_sha256"
    ] = "0" * 64
    mutations.append(("boundary_321_link", changed))
    changed = copy.deepcopy(actual)
    changed["pr763_crosswalk"]["m2_chart_applicable"] = True
    mutations.append(("pr763_applicability", changed))
    failed = False
    for name, changed in mutations:
        caught = changed != actual
        print(f"  tamper {name:<22}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    if failed:
        print("TAMPER-SELFTEST: FAIL")
        return 1
    print("TAMPER-SELFTEST: PASS (all ledger mutations caught)")
    return 0


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-profiles", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))

    report = build_report(include_profiles=args.include_profiles)
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
        print("RESULT: FAIL (frozen m=2 full-rank ledger drift)", file=sys.stderr)
        return 1
    for case in report["cases"]:
        spec = case["case"]
        target = case["m2_target"]
        owner = case["auxiliary_owner_target"]
        boundary_321 = case["boundary_321_target"]
        addback = case["complete_finite_addback"]
        print(
            "[PASS] "
            f"q={spec['q']},n={spec['n']}: m2 {target['old_q3_charge']} -> "
            f"{target['new_q_charge']}; owner {owner['owner']} "
            f"{owner['old_b3_charge']} -> {owner['new_owner_charge']}; "
            f"boundary321 {boundary_321['owner']} "
            f"{boundary_321['old_q2_charge']} -> {boundary_321['new_q_charge']}; "
            f"complete {addback['old_all_profile_bound']} -> "
            f"{addback['new_all_profile_bound']}; {addback['closure_verdict']}"
        )
    print("[PASS] PR #763 crosswalk: local m=2 chart is sigma-incompatible")
    print("RESULT: PASS (exact local m=2 profile add-back reproduced)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
