#!/usr/bin/env python3
"""Regression battery for the append-only B11 scanner coordinates.

The synthetic masks test schema and classification only; they are not asserted
to be Reed--Solomon codewords.  A separate small sample/seed-sweep replay checks
that aggregate histograms conserve every classified sunflower extra.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

from scan_l1_full_list_quotient_conjecture import (
    b11_frontier_record,
    classify_b11_box,
    classify_sunflower_listing,
    img_list,
    mask_from_indices,
    sample_scan,
    seed_sweep_scan,
    subgroup,
    sunflower_words,
)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


class Battery:
    def __init__(self, tamper: str | None = None):
        self.tamper = tamper
        self.checks: list[Check] = []

    def expected(self, name: str, value: object) -> object:
        if self.tamper != name:
            return value
        if isinstance(value, bool):
            return not value
        if isinstance(value, int):
            return value + 1
        if isinstance(value, str):
            return value + "_TAMPERED"
        raise TypeError(f"no tamper rule for {name}: {type(value)}")

    def check(self, name: str, ok: bool, detail: str) -> None:
        self.checks.append(Check(name, bool(ok), detail))


def rejects_record(**kwargs: object) -> bool:
    try:
        b11_frontier_record(**kwargs)
    except ValueError:
        return True
    return False


def without_b11_fields(value: object) -> object:
    """Project an extended result back to the pre-extension JSON schema."""
    if isinstance(value, dict):
        return {
            key: without_b11_fields(item)
            for key, item in value.items()
            if not (isinstance(key, str) and key.startswith("b11_"))
        }
    if isinstance(value, list):
        return [without_b11_fields(item) for item in value]
    return value


def projection_sha256(value: object) -> str:
    payload = json.dumps(
        without_b11_fields(value), sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def retained_sunflower_extra_total(result: dict[str, object]) -> tuple[int, int]:
    rows = result["max_primitive_examples"]
    assert isinstance(rows, list)
    classifications = [
        row["sunflower_listing_classification"]
        for row in rows
        if isinstance(row, dict) and "sunflower_listing_classification" in row
    ]
    return len(classifications), sum(
        int(classification["extra_count"]) for classification in classifications
    )


@lru_cache(maxsize=1)
def exact_frontier_fixture() -> tuple[int, dict[str, object]]:
    """Exact support-subset decode of a genuine low-Johnson toy frontier."""
    p, n, k, s = 17, 16, 8, 10
    word = sunflower_words(p, n, k, s, seed=0, random_count=0)[0]
    listed = img_list(word["values"], subgroup(p, n), k, s, p, "support")
    classification = classify_sunflower_listing(
        listed.values(),
        word["sunflower"],
        n,
        1000,
        frontier_E=0,
        frontier_V2=0,
        frontier_VR=0,
    )
    return len(listed), classification


@lru_cache(maxsize=1)
def exact_unpaid_frontier_fixture() -> tuple[int, dict[str, object]]:
    """Exact M=5 row beyond the fixed-layer auxiliary Johnson boundary."""
    p, n, k, s = 17, 16, 6, 7
    word = sunflower_words(p, n, k, s, seed=0, random_count=0)[0]
    listed = img_list(word["values"], subgroup(p, n), k, s, p, "support")
    classification = classify_sunflower_listing(
        listed.values(),
        word["sunflower"],
        n,
        2000,
        frontier_E=0,
        frontier_V2=0,
        frontier_VR=0,
    )
    return len(listed), classification


@lru_cache(maxsize=1)
def exact_g2_paid_frontier_fixture() -> tuple[int, dict[str, object]]:
    """Reclassify the same M=5 row at the first positive B11 G2 cut."""
    p, n, k, s = 17, 16, 6, 7
    word = sunflower_words(p, n, k, s, seed=0, random_count=0)[0]
    listed = img_list(word["values"], subgroup(p, n), k, s, p, "support")
    classification = classify_sunflower_listing(
        listed.values(),
        word["sunflower"],
        n,
        2000,
        frontier_E=0,
        frontier_V2=1,
        frontier_VR=0,
    )
    return len(listed), classification


def synthetic_classification() -> dict[str, object]:
    core = list(range(7))
    petals = [list(range(7, 10)), list(range(10, 13)), list(range(13, 16))]
    intended = [sorted(core + petal) for petal in petals]
    sunflower = {
        "core": core,
        "petals": petals,
        "intended_list_size": 3,
        "intended_agreement_sets": intended,
        "intended_stabilizer_orders": [1, 1, 1],
    }
    # Four extras, chosen to exercise the low-overagreement, growing-excess,
    # Johnson, and full-petal classifications.  They are schema fixtures only.
    extra_sets = [
        [0, 1, 2, 3, 4, 7, 8, 10, 11, 13],       # d=2, hits 2,2,1
        [0, 1, 2, 7, 8, 9, 10, 11, 13, 14],       # d=4, hits 3,2,2
        [0, 1, 2, 3, 4, 7, 8, 10, 11, 13, 14],   # lambda=lambda_J
        [0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    ]
    masks = [mask_from_indices(indices) for indices in intended + extra_sets]
    return classify_sunflower_listing(
        masks,
        sunflower,
        16,
        20,
        frontier_E=0,
        frontier_V2=0,
        frontier_VR=0,
    )


def run_battery(tamper: str | None = None) -> list[Check]:
    battery = Battery(tamper)
    result = synthetic_classification()
    examples = result["extra_examples"]
    assert isinstance(examples, list)
    records = [example["b11_frontier"] for example in examples]

    battery.check(
        "extra_count",
        result["extra_count"] == battery.expected("extra_count", 4),
        f"extra_count={result['extra_count']}",
    )
    battery.check(
        "histogram_conservation",
        result["b11_box_histogram_count"]
        == battery.expected("histogram_conservation", result["extra_count"]),
        f"box_count={result['b11_box_histogram_count']}",
    )
    battery.check(
        "coordinate_conservation",
        sum(result["b11_coordinate_histogram"].values())
        == battery.expected("coordinate_conservation", result["extra_count"]),
        f"coordinate_count={sum(result['b11_coordinate_histogram'].values())}",
    )

    target = next(record for record in records if record["a_i"] == [2, 2, 1])
    battery.check(
        "a_i",
        target["a_i"] == [2, 2, battery.expected("a_i", 1)],
        f"a_i={target['a_i']}",
    )
    battery.check(
        "t",
        target["t"] == battery.expected("t", len(target["a_i"])),
        f"t={target['t']}",
    )
    battery.check(
        "d_minus_ell",
        target["d_minus_ell"] == battery.expected("d_minus_ell", -1),
        f"d_minus_ell={target['d_minus_ell']}",
    )
    battery.check(
        "G2",
        target["G2"] == battery.expected("G2", 2),
        f"G2={target['G2']}",
    )
    battery.check(
        "GR",
        target["GR"] == battery.expected("GR", 4),
        f"GR={target['GR']}",
    )
    battery.check(
        "lambda_minus",
        target["lambda_minus_lambda_J"] == battery.expected("lambda_minus", -1),
        f"lambda-lambdaJ={target['lambda_minus_lambda_J']}",
    )
    battery.check(
        "bounded_escape",
        target["finite_box"]["classification"]
        == battery.expected("bounded_escape", "ESCAPES_BOUNDED_EXCESS_BOX"),
        f"class={target['finite_box']['classification']}",
    )

    equality_record = next(
        record
        for record in records
        if record["lambda_minus_lambda_J"] == 0 and not record["all_full"]
    )
    battery.check(
        "johnson_equality",
        equality_record["finite_box"]["classification"]
        == battery.expected("johnson_equality", "PAID_JOHNSON"),
        f"class={equality_record['finite_box']['classification']}",
    )
    growing_record = next(
        record
        for record in records
        if record["finite_box"]["classification"] == "ESCAPES_BY_COFACTOR_EXCESS"
    )
    battery.check(
        "growing_excess",
        growing_record["d_minus_ell"] == battery.expected("growing_excess", 1),
        f"excess={growing_record['d_minus_ell']}",
    )
    full_record = next(record for record in records if record["all_full"])
    battery.check(
        "full_separate",
        full_record["finite_box"]["classification"]
        == battery.expected("full_separate", "FULL_PETAL_SEPARATE"),
        f"class={full_record['finite_box']['classification']}",
    )

    battery.check(
        "impossible_one_petal_rejected",
        rejects_record(
            ell=3,
            petal_count=3,
            d=3,
            r=0,
            a_i=[3],
            agreement_slack=0,
            lambda_j=1,
            maximal=True,
        )
        == battery.expected("impossible_one_petal_rejected", True),
        "maximal one-petal data violates the exact slack identity",
    )
    battery.check(
        "maximal_background_guard",
        rejects_record(
            ell=3,
            petal_count=3,
            d=3,
            r=5,
            a_i=[2, 2],
            agreement_slack=3,
            lambda_j=1,
            maximal=True,
        )
        == battery.expected("maximal_background_guard", True),
        "r >= ell rejected in maximal domain",
    )
    battery.check(
        "petal_defect_guard",
        rejects_record(
            ell=3,
            petal_count=3,
            d=1,
            r=2,
            a_i=[2, 1],
            agreement_slack=1,
            lambda_j=1,
            maximal=True,
        )
        == battery.expected("petal_defect_guard", True),
        "a_i > d rejected",
    )
    battery.check(
        "slack_identity_guard",
        rejects_record(
            ell=3,
            petal_count=3,
            d=3,
            r=0,
            a_i=[2, 2],
            agreement_slack=99,
            lambda_j=1,
            maximal=True,
        )
        == battery.expected("slack_identity_guard", True),
        "inconsistent lambda rejected",
    )
    battery.check(
        "petal_count_guard",
        rejects_record(
            ell=2,
            petal_count=2,
            d=2,
            r=1,
            a_i=[1, 1, 1],
            agreement_slack=0,
            lambda_j=1,
            maximal=True,
        )
        == battery.expected("petal_count_guard", True),
        "t > M rejected",
    )

    anchor_record = b11_frontier_record(
        ell=3,
        petal_count=3,
        d=3,
        r=0,
        a_i=[3, 2, 1],
        agreement_slack=0,
        lambda_j=1,
        maximal=True,
    )
    battery.check(
        "paid_g2",
        classify_b11_box(anchor_record, E=0, V2=1, VR=0)
        == battery.expected("paid_g2", "PAID_G2"),
        "G2 equality is paid",
    )
    battery.check(
        "paid_gr",
        classify_b11_box(anchor_record, E=0, V2=0, VR=3)
        == battery.expected("paid_gr", "PAID_GR"),
        "GR equality is paid",
    )

    sample = sample_scan(
        17, 8, 4, 5, 0.0, 1.0, 0, 0, 0, "support", 4, 0, 0, 0
    )
    sample_summary = sample["sunflower_summary"]
    sample_rows, sample_extra_total = retained_sunflower_extra_total(sample)
    sample_coordinate_total = sum(sample_summary["b11_coordinate_summary"].values())
    battery.check(
        "sample_aggregation",
        (
            sample_rows == sample_summary["rows"]
            and sample_summary["b11_box_summary_count"] == sample_extra_total
            and sample_summary["b11_known_owner_summary_count"] == sample_extra_total
            and sample_coordinate_total == sample_extra_total
        )
        == battery.expected("sample_aggregation", True),
        (
            f"rows={sample_rows}/{sample_summary['rows']},"
            f"box={sample_summary['b11_box_summary_count']},"
            f"coordinates={sample_coordinate_total},extras={sample_extra_total}"
        ),
    )
    battery.check(
        "sample_legacy_projection",
        projection_sha256(sample)
        == battery.expected(
            "sample_legacy_projection",
            "9061192619990d74224005c55572727935d141f680279a9f3bb4f12e7cb99864",
        ),
        f"sha256={projection_sha256(sample)}",
    )
    sweep = seed_sweep_scan(
        17, 8, 4, 5, 0.0, 1.0, 0, 0, 2, 0, "support", 4, 0, 0, 0
    )
    sweep_summary = sweep["sunflower_summary"]
    seed_results = [
        sample,
        sample_scan(17, 8, 4, 5, 0.0, 1.0, 0, 1, 0, "support", 4, 0, 0, 0),
    ]
    seed_row_totals = [retained_sunflower_extra_total(result) for result in seed_results]
    sweep_rows = sum(item[0] for item in seed_row_totals)
    sweep_extra_total = sum(item[1] for item in seed_row_totals)
    sweep_coordinate_total = sum(sweep_summary["b11_coordinate_summary"].values())
    battery.check(
        "sweep_aggregation",
        (
            sweep_rows == sweep_summary["rows"]
            and sweep_summary["b11_box_summary_count"] == sweep_extra_total
            and sweep_summary["b11_known_owner_summary_count"] == sweep_extra_total
            and sweep_coordinate_total == sweep_extra_total
        )
        == battery.expected("sweep_aggregation", True),
        (
            f"rows={sweep_rows}/{sweep_summary['rows']},"
            f"box={sweep_summary['b11_box_summary_count']},"
            f"coordinates={sweep_coordinate_total},extras={sweep_extra_total}"
        ),
    )
    battery.check(
        "sweep_legacy_projection",
        projection_sha256(sweep)
        == battery.expected(
            "sweep_legacy_projection",
            "76048db2e50c7009b752cadcd626896b776dbffe95aa01ca99488732a736472c",
        ),
        f"sha256={projection_sha256(sweep)}",
    )

    exact_list_size, exact_fixture = exact_frontier_fixture()
    exact_examples = exact_fixture["extra_examples"]
    b11_low_mixed = [
        example
        for example in exact_examples
        if example["b11_frontier"]["status"]
        == "B11_LOW_OVERAGREEMENT_COORDINATE"
        and example["b11_frontier"]["mixed_partial_target"]
    ]
    profile_221 = [
        example
        for example in b11_low_mixed
        if example["core_defect"] == 2
        and example["background_hits"] == 0
        and example["b11_frontier"]["a_i"] == [2, 2, 1]
    ]
    battery.check(
        "exact_frontier_list",
        (exact_list_size == 19 and exact_fixture["extra_count"] == 16)
        == battery.expected("exact_frontier_list", True),
        f"list={exact_list_size},extras={exact_fixture['extra_count']}",
    )
    battery.check(
        "exact_frontier_classes",
        (
            exact_fixture["b11_box_histogram"]
            == {
                "ESCAPES_BOUNDED_EXCESS_BOX": 13,
                "ESCAPES_BY_COFACTOR_EXCESS": 1,
                "FULL_PETAL_SEPARATE": 1,
                "PAID_JOHNSON": 1,
            }
        )
        == battery.expected("exact_frontier_classes", True),
        f"classes={exact_fixture['b11_box_histogram']}",
    )
    battery.check(
        "exact_b11_low_mixed",
        len(b11_low_mixed) == battery.expected("exact_b11_low_mixed", 14),
        f"B11_low_Johnson_mixed={len(b11_low_mixed)}",
    )
    battery.check(
        "exact_profile_221",
        len(profile_221) == battery.expected("exact_profile_221", 7),
        f"d=2,r=0,a_i=(2,2,1) count={len(profile_221)}",
    )
    battery.check(
        "exact_auxiliary_owner",
        (
            exact_fixture["b11_known_owner_histogram"]
            == {
                "FULL_PETAL_SEPARATE": 1,
                "PAID_AUXILIARY_JOHNSON": 14,
                "PAID_GLOBAL_JOHNSON": 1,
            }
        )
        == battery.expected("exact_auxiliary_owner", True),
        f"owners={exact_fixture['b11_known_owner_histogram']}",
    )
    battery.check(
        "exact_auxiliary_margin",
        all(
            example["b11_frontier"]["auxiliary_johnson"]
            == {
                "petal_count": 3,
                "petal_domain_size": 9,
                "required_agreement": 5,
                "effective_degree_bound": 2,
                "margin": 7,
                "paid": True,
                "unique": False,
                "integer_floor_bound_per_fixed_D_R0": 3,
            }
            for example in profile_221
        )
        == battery.expected("exact_auxiliary_margin", True),
        "profile (2,2,1) has sharp auxiliary bound floor(27/7)=3",
    )
    battery.check(
        "exact_genuine_after_owners",
        sum(
            1
            for example in exact_examples
            if example["b11_frontier"]["genuine_frontier_after_known_owners"]
        )
        == battery.expected("exact_genuine_after_owners", 0),
        "no unpaid residual remains after auxiliary Johnson",
    )

    unpaid_list_size, unpaid_fixture = exact_unpaid_frontier_fixture()
    unpaid_examples = unpaid_fixture["extra_examples"]
    unpaid_residuals = [
        example
        for example in unpaid_examples
        if example["b11_frontier"]["genuine_frontier_after_known_owners"]
    ]
    unpaid_profile_211 = [
        example
        for example in unpaid_residuals
        if example["core_defect"] == 2
        and example["background_hits"] == 0
        and example["b11_frontier"]["a_i"] == [2, 1, 1]
    ]
    battery.check(
        "exact_unpaid_frontier_list",
        (
            unpaid_list_size == 452
            and unpaid_fixture["extra_count"] == 447
            and unpaid_fixture["b11_known_owner_histogram"]
            == {"FULL_PETAL_SEPARATE": 11, "UNPAID_B11_RESIDUAL": 436}
        )
        == battery.expected("exact_unpaid_frontier_list", True),
        (
            f"list={unpaid_list_size},extras={unpaid_fixture['extra_count']},"
            f"owners={unpaid_fixture['b11_known_owner_histogram']}"
        ),
    )
    battery.check(
        "exact_unpaid_profile_211",
        len(unpaid_profile_211)
        == battery.expected("exact_unpaid_profile_211", 59),
        f"d=2,r=0,a_i=(2,1,1) unpaid count={len(unpaid_profile_211)}",
    )
    battery.check(
        "exact_subauxiliary_margin_211",
        all(
            example["b11_frontier"]["auxiliary_johnson"]["margin"] == -4
            and not example["b11_frontier"]["auxiliary_johnson"]["paid"]
            for example in unpaid_profile_211
        )
        == battery.expected("exact_subauxiliary_margin_211", True),
        "profile (2,1,1) has auxiliary margin 16-20=-4",
    )
    battery.check(
        "exact_unpaid_primitive",
        all(
            example["b11_frontier"]["agreement_stabilizer_order"] == 1
            for example in unpaid_residuals
        )
        == battery.expected("exact_unpaid_primitive", True),
        "all 436 unpaid mixed residuals have stabilizer order one",
    )

    paid_list_size, paid_fixture = exact_g2_paid_frontier_fixture()
    paid_profile_211 = [
        example
        for example in paid_fixture["extra_examples"]
        if example["core_defect"] == 2
        and example["background_hits"] == 0
        and example["b11_frontier"]["a_i"] == [2, 1, 1]
    ]
    battery.check(
        "exact_profile_211_paid_at_V2_1",
        (
            paid_list_size == unpaid_list_size
            and len(paid_profile_211) == 59
            and all(
                example["b11_frontier"]["known_owner"] == "PAID_B11_G2"
                and not example["b11_frontier"][
                    "genuine_frontier_after_known_owners"
                ]
                for example in paid_profile_211
            )
        )
        == battery.expected("exact_profile_211_paid_at_V2_1", True),
        "all 59 profile-(2,1,1) rows route to B11 G2 when V2=1",
    )

    return battery.checks


def main(argv: list[str]) -> int:
    tamper = "--tamper-selftest" in argv
    checks = run_battery()
    for check in checks:
        print(f"[{'PASS' if check.ok else 'FAIL'}] {check.name}: {check.detail}")
    if not all(check.ok for check in checks):
        print("RESULT: FAIL")
        return 1
    print(f"RESULT: PASS ({len(checks)}/{len(checks)})")
    if not tamper:
        return 0

    failed = False
    for check in checks:
        changed = run_battery(tamper=check.name)
        caught = not all(item.ok for item in changed)
        print(f"  tamper {check.name:<24}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    if failed:
        print("TAMPER-SELFTEST: FAIL")
        return 1
    print("TAMPER-SELFTEST: PASS (every corruption caught)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
