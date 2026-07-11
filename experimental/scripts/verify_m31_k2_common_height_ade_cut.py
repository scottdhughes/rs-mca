#!/usr/bin/env python3
"""Verify the M31 kappa=2 common-height ADE exclusion and census delta."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from verify_m31_rank_inertia_anchor_cut import (
    L,
    M,
    N,
    R,
    W,
    anchor_threshold,
    ceil_div,
    centroid_cut,
    rank_inertia_cut,
)


P = 2**31 - 1
D0 = N - W
T0 = 277_868
BASE_COMMIT = "8264eae23e9120a182218b3839aac024051ccf8d"
PR628_COMMIT = "edea20ce09bcb2241c831d7000ed3e4f0e8a9e87"
SOURCE_VERIFIER_SHA256 = (
    "1ea1c6a1188895223dfca82d62f1fb05e2b9c7139b98e1f1b80c2a49d17619db"
)
PR628_VERIFIER_SHA256 = (
    "34f9d4b2586b49e77f78131eb506a5ffa06de8928b6ecad6cb9b1287b48a4278"
)
BASE_INTEGRATED_HASH = (
    "49576339b6755e90f6f1997b294bad5d178aa9bc5c25c44aab345d9ccefd99da"
)
OLD_UNION_HASH = (
    "2f57a0a5379a4222869d4e6ab79aad39d7b352df6c0227996ab2da7ec10483a4"
)
OLD_RESIDUAL_HASH = (
    "40925c2c5a3c3928a42f6d92775de87608c7e260bf3c3ff7eda36b5e02193956"
)
CLASSIFIER_HASH = (
    "4801bb6740b214cf90590eafa827437fbb6b04da899db970c5f799af74b4750f"
)
NEW_EXCLUSIONS_HASH = (
    "b5f1a8c3d2916dd5077d641eef1dffcb2ae9385fd4707364a62ea37b01808a79"
)
NEW_UNION_HASH = (
    "842d33d8258fd69c14f6b69ca3a9d5a8880df46225f142f0ea8cdd8daa5bb973"
)
NEW_RESIDUAL_HASH = (
    "2dcc296964f1a131428baf100f2e5a1c6291c91778fe533655255a5b7e8dce35"
)

PR628_ROWS = {
    (2, 391_732, 391_732, 783_464),
    (2, 391_733, 391_733, 783_466),
    (2, 391_734, 391_734, 783_468),
    (2, 391_735, 391_735, 783_470),
}


def canonical_hash(rows):
    payload = ";".join(",".join(map(str, row)) for row in sorted(rows))
    return sha256(payload.encode("ascii")).hexdigest()


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def ceil_fraction(value):
    return -(-value.numerator // value.denominator)


def rho(t):
    return Fraction(N * t, 2 * N * t - R)


def root_count_rank_floor(t):
    value = Fraction(L, 1) / rho(t) - 64 + 4 * rho(t)
    return ceil_fraction(value)


def main():
    root = Path(__file__).resolve().parents[1]
    certificate = json.loads(
        (root / "data" / "cap25_v13_m31_k2_common_height_ade_cut.json").read_text(
            encoding="utf-8"
        )
    )
    source_verifier = Path(__file__).with_name(
        "verify_m31_rank_inertia_anchor_cut.py"
    )
    assert file_sha256(source_verifier) == SOURCE_VERIFIER_SHA256

    assert certificate["schema"] == "cap25-v13-m31-k2-common-height-ade-cut-v1"
    assert certificate["provenance"] == {
        "base_commit": BASE_COMMIT,
        "source_verifier_sha256": SOURCE_VERIFIER_SHA256,
        "pr628_commit": PR628_COMMIT,
        "pr628_verifier_sha256": PR628_VERIFIER_SHA256,
    }
    assert certificate["constants"] == {
        "p": P,
        "N": N,
        "m": M,
        "w": W,
        "d0": D0,
        "L": L,
        "R": R,
        "t0": T0,
    }

    thresholds = {kappa: anchor_threshold(kappa) for kappa in range(2, 775)}
    grid = []
    integrated = set()
    classifier = set()

    for kappa in range(2, 775):
        anchor = thresholds[kappa][0]
        low = ceil_div(W + 1, kappa - 1)
        high = min(M // kappa, R // (N * (kappa - 1)))
        for t in range(low, high + 1):
            row = (kappa, t, (kappa - 1) * t, kappa * t)
            grid.append(row)
            if rank_inertia_cut(kappa, t, anchor) or centroid_cut(kappa, t):
                integrated.add(row)
            if kappa == 2 and t >= T0:
                classifier.add(row)

    grid_set = set(grid)
    assert len(grid) == len(grid_set) == 3_254_885
    assert len(integrated) == 153_605
    assert canonical_hash(integrated) == BASE_INTEGRATED_HASH
    assert PR628_ROWS <= grid_set
    assert not (PR628_ROWS & integrated)

    old_union = integrated | PR628_ROWS
    old_residual = grid_set - old_union
    assert len(old_union) == 153_609
    assert len(old_residual) == 3_101_276
    assert canonical_hash(old_union) == OLD_UNION_HASH
    assert canonical_hash(old_residual) == OLD_RESIDUAL_HASH

    assert len(classifier) == 212_697
    assert min(classifier) == (2, 277_868, 277_868, 555_736)
    assert max(classifier) == (2, 490_564, 490_564, 981_128)
    assert canonical_hash(classifier) == CLASSIFIER_HASH
    assert len(classifier & integrated) == 98_829
    assert classifier & PR628_ROWS == PR628_ROWS

    new_exclusions = classifier - old_union
    assert len(new_exclusions) == 113_864
    assert min(new_exclusions) == (2, 277_868, 277_868, 555_736)
    assert max(new_exclusions) == (2, 391_731, 391_731, 783_462)
    assert canonical_hash(new_exclusions) == NEW_EXCLUSIONS_HASH

    new_union = old_union | classifier
    new_residual = grid_set - new_union
    assert len(new_union) == 267_473
    assert len(new_residual) == 2_987_412
    assert canonical_hash(new_union) == NEW_UNION_HASH
    assert canonical_hash(new_residual) == NEW_RESIDUAL_HASH

    boundary_rho = rho(T0)
    previous_rho = rho(T0 - 1)
    assert boundary_rho == Fraction(582_731_431_936, 70_500_333_905)
    assert previous_rho == Fraction(582_729_334_784, 70_496_139_601)
    assert 8 < boundary_rho < Fraction(17, 2)
    assert root_count_rank_floor(T0) == 2_029_720 == D0 + 15
    assert root_count_rank_floor(T0 - 1) == 2_029_606 == D0 - 99
    assert P > 2**30
    assert P**15 > 2**450
    assert (N + 1) ** 16 < 2**352

    expected = {
        "source_ledger": {
            "grid_count": len(grid),
            "base_integrated_count": len(integrated),
            "base_integrated_sha256": canonical_hash(integrated),
            "old_union_count": len(old_union),
            "old_union_sha256": canonical_hash(old_union),
            "old_residual_count": len(old_residual),
            "old_residual_sha256": canonical_hash(old_residual),
        },
        "classifier": {
            "count": len(classifier),
            "sha256": canonical_hash(classifier),
            "integrated_overlap_count": len(classifier & integrated),
            "pr628_overlap_count": len(classifier & PR628_ROWS),
            "new_exclusions_count": len(new_exclusions),
            "new_exclusions_sha256": canonical_hash(new_exclusions),
        },
        "new_ledger": {
            "union_count": len(new_union),
            "union_sha256": canonical_hash(new_union),
            "residual_count": len(new_residual),
            "residual_sha256": canonical_hash(new_residual),
        },
        "boundary": {
            "rho_numerator": boundary_rho.numerator,
            "rho_denominator": boundary_rho.denominator,
            "rank_floor": root_count_rank_floor(T0),
            "rank_gap": root_count_rank_floor(T0) - D0,
            "previous_rho_numerator": previous_rho.numerator,
            "previous_rho_denominator": previous_rho.denominator,
            "previous_rank_floor": root_count_rank_floor(T0 - 1),
        },
    }
    for key, value in expected.items():
        assert certificate[key] == value

    # Tamper tests pin the activation boundary and all three ledger layers.
    tampered_classifier = set(classifier)
    tampered_classifier.remove(min(tampered_classifier))
    assert canonical_hash(tampered_classifier) != certificate["classifier"]["sha256"]
    assert root_count_rank_floor(T0 + 1) != certificate["boundary"]["rank_floor"]
    assert OLD_UNION_HASH != NEW_UNION_HASH
    assert OLD_RESIDUAL_HASH != NEW_RESIDUAL_HASH

    print("RESULT: PASS")
    print(f"grid={len(grid)}")
    print(f"old_union={len(old_union)}")
    print(f"old_residual={len(old_residual)}")
    print(f"classifier_total={len(classifier)}")
    print(f"new_exclusions={len(new_exclusions)}")
    print(f"new_union={len(new_union)}")
    print(f"new_residual={len(new_residual)}")
    print(f"classifier_sha256={canonical_hash(classifier)}")
    print(f"new_exclusions_sha256={canonical_hash(new_exclusions)}")
    print(f"new_union_sha256={canonical_hash(new_union)}")
    print(f"new_residual_sha256={canonical_hash(new_residual)}")
    print(f"rho_boundary={boundary_rho}")
    print(f"rank_floor_boundary={root_count_rank_floor(T0)}")
    print(f"prefix_rank_cap={D0}")
    print(f"rank_gap={root_count_rank_floor(T0)-D0}")
    print(f"previous_row_rank_floor={root_count_rank_floor(T0-1)}")
    print("certificate=PASS")
    print("tamper_checks=PASS")


if __name__ == "__main__":
    main()
