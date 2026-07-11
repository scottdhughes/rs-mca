#!/usr/bin/env python3
"""Verify the exact four-row M31 star-determinant rank-gap cut."""

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
INTEGRATED_HASH = "49576339b6755e90f6f1997b294bad5d178aa9bc5c25c44aab345d9ccefd99da"
TEN_HASH = "c18ab71c6450c9b22360c16c91944e98c5d5dedf50723a9fb133e254c69a4b15"
FOUR_HASH = "2809ec4892d507367920dcfd2480375a619033f61751aafe96efc6bebfbe473d"
NEW_UNION_HASH = "2f57a0a5379a4222869d4e6ab79aad39d7b352df6c0227996ab2da7ec10483a4"
NEW_RESIDUAL_HASH = "40925c2c5a3c3928a42f6d92775de87608c7e260bf3c3ff7eda36b5e02193956"


def canonical_hash(rows):
    payload = ";".join(",".join(map(str, row)) for row in sorted(rows))
    return sha256(payload.encode("ascii")).hexdigest()


def cubic_value(kappa, d, x):
    lam = kappa - 1
    q = L - d
    return (d - 1) ** 2 * (q * lam**3 + x**3) - (q * lam + x) ** 3


def rank_obstructed(kappa, d, u):
    lam = kappa - 1
    q = L - d
    return u < ceil_div(q * lam, d - 2) or cubic_value(kappa, d, u) < 0


def main():
    certificate_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "cap25_v13_m31_star_determinant_rank_gap.json"
    )
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert certificate["schema"] == "cap25-v13-m31-star-determinant-rank-gap-v1"
    assert certificate["constants"] == {
        "p": P,
        "N": N,
        "m": M,
        "w": W,
        "d0": D0,
        "L": L,
        "R": R,
    }
    thresholds = {kappa: anchor_threshold(kappa) for kappa in range(2, 775)}

    grid = []
    integrated = set()
    candidates = []

    for kappa in range(2, 775):
        anchor = thresholds[kappa][0]
        low = ceil_div(W + 1, kappa - 1)
        high = min(M // kappa, R // (N * (kappa - 1)))
        for t in range(low, high + 1):
            row = (kappa, t, (kappa - 1) * t, kappa * t)
            grid.append(row)
            if rank_inertia_cut(kappa, t, anchor) or centroid_cut(kappa, t):
                integrated.add(row)
                continue

            c0 = N * kappa * kappa * t - R * (kappa + 1)
            if c0 <= 0:
                continue
            u = R * (kappa - 1) // c0
            if rank_obstructed(kappa, D0, u):
                candidates.append((row, u))

    assert len(grid) == 3_254_885
    assert len(integrated) == 153_605
    assert len(grid) - len(integrated) == 3_101_280
    assert canonical_hash(integrated) == INTEGRATED_HASH
    assert certificate["source_ledger"] == {
        "grid_count": len(grid),
        "integrated_count": len(integrated),
        "residual_count": len(grid) - len(integrated),
        "integrated_sha256": canonical_hash(integrated),
    }

    candidate_rows = [row for row, _ in candidates]
    assert len(candidate_rows) == 10
    assert canonical_hash(candidate_rows) == TEN_HASH

    expected = [
        ((2, 391_732, 391_732, 783_464), 913, 2_032_856, 3_151),
        ((2, 391_733, 391_733, 783_466), 907, 2_049_267, 19_562),
        ((2, 391_734, 391_734, 783_468), 900, 2_068_679, 38_974),
        ((2, 391_735, 391_735, 783_470), 894, 2_085_550, 55_845),
        ((3, 232_117, 464_234, 696_351), 1_807, 2_058_936, 29_231),
        ((4, 163_198, 489_594, 652_792), 2_729, 2_041_947, 12_242),
        ((6, 101_539, 507_695, 609_234), 4_561, 2_035_032, 5_327),
        ((8, 73_432, 514_024, 587_456), 6_316, 2_062_308, 32_603),
        ((14, 39_961, 519_493, 559_454), 11_831, 2_040_825, 11_120),
        ((15, 37_131, 519_834, 556_965), 12_737, 2_041_622, 11_917),
    ]

    rank_gap = []
    new_cut = []
    for row, u in candidates:
        d = D0
        while d <= N and rank_obstructed(row[0], d, u):
            d += 1
        assert d <= N
        r0 = d
        g = r0 - D0
        assert cubic_value(row[0], r0 - 1, u) < 0
        assert cubic_value(row[0], r0, u) >= 0
        rank_gap.append((row, u, r0, g))

        if row[0] == 2:
            exponent = (u - 1).bit_length() + 2 * u
            if exponent < 30 * g:
                assert P > 2**30
                new_cut.append(row)

    assert rank_gap == expected
    computed_certificate_rows = [
        {
            "row": list(row),
            "u": u,
            "r0": r0,
            "g": g,
            "T_left": cubic_value(row[0], r0 - 1, u),
            "T_right": cubic_value(row[0], r0, u),
        }
        for row, u, r0, g in rank_gap
    ]
    assert certificate["rank_gap_candidates"] == computed_certificate_rows
    assert certificate["rank_gap_rows_sha256"] == canonical_hash(candidate_rows)
    assert len(new_cut) == 4
    assert canonical_hash(new_cut) == FOUR_HASH
    assert certificate["new_exclusions"] == [list(row) for row in new_cut]
    assert certificate["new_exclusions_sha256"] == canonical_hash(new_cut)

    boundary_values = [
        (-2_856_450_446_557_696, 945_834_330_667_008),
        (-680_064_577_435_368, 3_085_005_285_217_536),
        (-740_413_100_966_670, 2_981_396_363_301_855),
        (-2_304_227_262_464_577, 1_380_637_241_602_650),
    ]
    for (row, u, r0, _), (left, right) in zip(rank_gap[:4], boundary_values):
        assert cubic_value(row[0], r0 - 1, u) == left
        assert cubic_value(row[0], r0, u) == right

    new_union = integrated | set(new_cut)
    residual = set(grid) - new_union
    assert len(new_union) == 153_609
    assert len(residual) == 3_101_276
    assert canonical_hash(new_union) == NEW_UNION_HASH
    assert canonical_hash(residual) == NEW_RESIDUAL_HASH
    assert certificate["new_ledger"] == {
        "union_count": len(new_union),
        "residual_count": len(residual),
        "union_sha256": canonical_hash(new_union),
        "residual_sha256": canonical_hash(residual),
    }

    # Tampering with a canonical row or a boundary value must be detected.
    tampered_rows = [tuple(row) for row in certificate["new_exclusions"]]
    tampered_rows[0] = (
        tampered_rows[0][0],
        tampered_rows[0][1] + 1,
        tampered_rows[0][2],
        tampered_rows[0][3],
    )
    assert canonical_hash(tampered_rows) != certificate["new_exclusions_sha256"]
    assert (
        certificate["rank_gap_candidates"][0]["T_left"] + 1
        != cubic_value(rank_gap[0][0][0], rank_gap[0][2] - 1, rank_gap[0][1])
    )

    print("RESULT: PASS")
    print(f"grid={len(grid)}")
    print(f"integrated={len(integrated)}")
    print(f"old_residual={len(grid)-len(integrated)}")
    print(f"rank_gap_candidates={len(rank_gap)}")
    print(f"new_cut={len(new_cut)}")
    print(f"new_union={len(new_union)}")
    print(f"new_residual={len(residual)}")
    print(f"four_sha256={canonical_hash(new_cut)}")
    print(f"new_union_sha256={canonical_hash(new_union)}")
    print(f"new_residual_sha256={canonical_hash(residual)}")
    print("certificate=PASS")
    print("tamper_checks=PASS")


if __name__ == "__main__":
    main()
