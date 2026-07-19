#!/usr/bin/env python3
"""Fail-closed replay for the R32 fixed-27 quartic branch envelope."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
from dataclasses import dataclass, replace
from pathlib import Path


P = 2_130_706_433
N = 2_097_152
B = 32_768
A = 67_472
D = 63_601
W = 28_897
BASE_CAP = 12_997

SOURCE_HASHES = {
    "experimental/notes/l2/rank16_fixed27_quartic_repeated_resultant.md":
        "83ac3d4dcea6640a252becc21a0ac2d54eb6f3b48f524e51270867fdbc61acc7",
    "experimental/scripts/verify_rank16_fixed27_quartic_repeated_resultant.py":
        "9c4b8a1883bd46d3468e9489f2e89e57d47ced4f7300b09cfa720469f6692b18",
    "experimental/notes/l2/rank16_fixed27_quartic_high_triple_exclusion.md":
        "7ff29318d208cc7e78fae55b776737cad9702296ecadcca096ee0ba65b690d98",
    "experimental/scripts/verify_rank16_fixed27_quartic_high_triple.py":
        "c6892f0688d819fd62b16c4fcd205b855b2ae671d694d84033cf686de7221ed3",
    "experimental/notes/l2/rank16_fixed27_quartic_low_triple_band.md":
        "72346a834515f33951230a1418a90f926fcc1f989f292dd8b24111ea40bf6f2e",
    "experimental/scripts/verify_rank16_fixed27_quartic_low_triple.py":
        "92cd6ec81bf200452a0a8d62ca846a430cefb634a5391df9db4e8801f400bb06",
}

CERTIFICATE_DIR = (
    "experimental/data/certificates/"
    "rank16-fixed27-quartic-branch-envelope"
)
ENVELOPE_NAME = "fixed27_quartic_branch_envelope.csv"
STAGES_NAME = "fixed27_quartic_branch_internal_states.csv"
ENVELOPE_SHA256 = "6be4e7cf1367ebc142dddfc8734f29ade42053491052bfd8e9db986548bd1198"
STAGES_SHA256 = "d34f19be275028857dfbb76020cb5a06335cd7fe38f8b0dc48b559d83c59e039"


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def ceil_div(top: int, bottom: int) -> int:
    return -(-top // bottom)


def ordered_pair_min(parts: int, total: int) -> int:
    require(parts >= 1 and total >= 0, "invalid ordered-pair input")
    quotient, remainder = divmod(total, parts)
    return (
        remainder * (quotient + 1) * quotient
        + (parts - remainder) * quotient * (quotient - 1)
    )


def split_pair_min(left_parts: int, right_parts: int, cap: int, total: int) -> tuple[int, int]:
    lower = max(0, total - right_parts * cap)
    upper = min(cap, total)
    require(lower <= upper, "empty split-pair optimizer")

    def value(left_total: int) -> int:
        return (
            ordered_pair_min(left_parts, left_total)
            + ordered_pair_min(right_parts, total - left_total)
        )

    # The objective is discrete convex. Locate its first nonnegative forward
    # difference, then check the adjacent lattice point.
    lo, hi = lower, upper
    while lo < hi:
        mid = (lo + hi) // 2
        if value(mid + 1) - value(mid) >= 0:
            hi = mid
        else:
            lo = mid + 1
    candidates = [lo]
    if lo > lower:
        candidates.append(lo - 1)
    optimizer = min(candidates, key=lambda item: (value(item), item))
    return value(optimizer), optimizer


def maximum_admissible(limit: int, predicate) -> int:
    lo, hi = 0, limit
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if predicate(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


@dataclass(frozen=True)
class Config:
    block: int = B
    residual: int = D
    quotient: int = W
    base_cap: int = BASE_CAP
    max_stage_exponent: int = 13
    ceil_stage_degree: bool = False
    block_count_delta: int = -1
    three_parts: int = 5
    four_left_parts: int = 4
    four_right_parts: int = 3
    support_uses_ceiling: bool = True


@dataclass(frozen=True)
class Stage:
    c: int
    m: int
    stage_degree: int
    budget: int
    t3: int
    mt3: int
    t4: int
    mt4: int
    t4_optimizer: int


@dataclass(frozen=True)
class Row:
    c: int
    r: int
    lam: int
    k3: int
    k4: int
    twice_lam: int
    j: int
    pr930_wall: int
    removed_width: int
    support_floor: int


def build(config: Config) -> tuple[list[Row], list[Stage]]:
    rows: list[Row] = []
    stages: list[Stage] = []
    for c in range(config.base_cap + 1):
        residual = config.residual - c
        lam = config.quotient - c
        require(residual > 0 and lam > 0, "nonpositive deployed degree")
        current: list[Stage] = []
        for exponent in range(config.max_stage_exponent + 1):
            m = 1 << exponent
            if residual % m:
                continue
            stage_degree = (
                ceil_div(lam, m) if config.ceil_stage_degree else lam // m
            )
            block_count = config.block // m
            budget = (
                (block_count + config.block_count_delta)
                * (2 * stage_degree - 2)
            )
            t3 = maximum_admissible(
                config.three_parts * stage_degree,
                lambda total: ordered_pair_min(config.three_parts, total) <= budget,
            )

            def four_admissible(total: int) -> bool:
                value, _ = split_pair_min(
                    config.four_left_parts,
                    config.four_right_parts,
                    stage_degree,
                    total,
                )
                return value <= budget

            t4 = maximum_admissible(4 * stage_degree, four_admissible)
            _, optimizer = split_pair_min(
                config.four_left_parts,
                config.four_right_parts,
                stage_degree,
                t4,
            )
            stage = Stage(
                c=c,
                m=m,
                stage_degree=stage_degree,
                budget=budget,
                t3=t3,
                mt3=m * t3,
                t4=t4,
                mt4=m * t4,
                t4_optimizer=optimizer,
            )
            current.append(stage)
            stages.append(stage)
        require(current, f"no dyadic stage at c={c}")
        k3 = max(stage.mt3 for stage in current)
        k4 = max(stage.mt4 for stage in current)
        twice_lam = 2 * lam
        j = max(k3, k4, twice_lam)
        wall = 5 * lam - 7_320
        numerator = 7 * residual - j
        support_increment = (
            ceil_div(numerator, 2)
            if config.support_uses_ceiling
            else numerator // 2
        )
        rows.append(Row(
            c=c,
            r=residual,
            lam=lam,
            k3=k3,
            k4=k4,
            twice_lam=twice_lam,
            j=j,
            pr930_wall=wall,
            removed_width=wall - j,
            support_floor=c + support_increment,
        ))
    return rows, stages


SELECTED = {
    0: (97_307, 99_995, 99_995, 137_165, 37_170, 172_606),
    7_009: (84_688, 84_689, 84_689, 102_120, 17_431, 162_737),
    7_010: (84_686, 84_686, 84_686, 102_115, 17_429, 162_736),
    7_884: (82_978, 82_657, 82_978, 97_745, 14_767, 161_405),
    12_401: (73_520, 65_984, 73_520, 75_160, 1_640, 154_841),
    12_996: (72_182, 63_604, 72_182, 72_185, 3, 154_023),
    12_997: (72_180, 63_600, 72_180, 72_180, 0, 154_021),
}


def validate(rows: list[Row], stages: list[Stage], config: Config) -> None:
    require(P - 1 == 127 * 2**24, "wrong field factorization")
    require(N == 64 * B, "wrong deployed subgroup/block relation")
    require(len(rows) == 12_998, "wrong envelope row count")
    require(len(stages) == 25_996, "wrong admissible dyadic-state count")
    require(sum(1 for row in rows if row.k4 > row.k3) == 7_010, "wrong K4 region")
    require([row.c for row in rows if row.k4 == row.k3] == [7_010, 7_011, 7_012], "wrong tie region")
    require(sum(1 for row in rows if row.k3 > row.k4) == 5_985, "wrong K3 region")
    require(all(row.j > row.twice_lam for row in rows), "2lambda governs")
    require(all(row.removed_width > 0 for row in rows[:-1]), "nonendpoint gap closed")
    require(rows[-1].removed_width == 0, "endpoint is not equality")
    gains = [row.removed_width for row in rows[:-1]]
    require((min(gains), max(gains)) == (3, 37_170), "wrong gain range")
    nonendpoint_floor = min(row.support_floor for row in rows[:-1])
    minimizers = [row.c for row in rows[:-1] if row.support_floor == nonendpoint_floor]
    require((nonendpoint_floor, minimizers) == (154_023, [12_996]), "wrong support minimum")
    require(rows[-1].support_floor == 154_021, "wrong endpoint support floor")
    for c, expected in SELECTED.items():
        row = rows[c]
        actual = (
            row.k3,
            row.k4,
            row.j,
            row.pr930_wall,
            row.removed_width,
            row.support_floor,
        )
        require(actual == expected, f"wrong selected row c={c}")
    endpoint = rows[-1]
    require((endpoint.r, endpoint.lam) == (50_604, 15_900), "wrong endpoint degrees")
    require(4 * endpoint.c == 51_988, "wrong repeated-resultant saturation degree")
    require(4 * endpoint.lam == 63_600, "wrong endpoint factor-degree sum")


def csv_bytes(rows: list, fieldnames: list[str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({name: getattr(row, name) for name in fieldnames})
    return stream.getvalue().encode("ascii")


def certificates(rows: list[Row], stages: list[Stage]) -> tuple[bytes, bytes]:
    envelope = csv_bytes(rows, [
        "c", "r", "lam", "k3", "k4", "twice_lam", "j",
        "pr930_wall", "removed_width", "support_floor",
    ])
    internal = csv_bytes(stages, [
        "c", "m", "stage_degree", "budget", "t3", "mt3", "t4", "mt4",
        "t4_optimizer",
    ])
    return envelope, internal


def check_sources() -> None:
    base = root()
    for relative, expected in SOURCE_HASHES.items():
        path = base / relative
        require(path.is_file(), f"missing source: {relative}")
        require(sha256_file(path) == expected, f"source hash mismatch: {relative}")


def check_committed_certificates(envelope: bytes, stages: bytes) -> None:
    base = root() / CERTIFICATE_DIR
    envelope_path = base / ENVELOPE_NAME
    stages_path = base / STAGES_NAME
    require(envelope_path.is_file(), "missing committed envelope CSV")
    require(stages_path.is_file(), "missing committed internal-state CSV")
    require(envelope_path.read_bytes() == envelope, "envelope CSV byte mismatch")
    require(stages_path.read_bytes() == stages, "internal-state CSV byte mismatch")
    require(sha256_bytes(envelope) == ENVELOPE_SHA256, "envelope CSV hash mismatch")
    require(sha256_bytes(stages) == STAGES_SHA256, "internal-state CSV hash mismatch")


def run_check(write_certificates: bool = False) -> str:
    check_sources()
    rows, stages = build(Config())
    validate(rows, stages, Config())
    envelope, internal = certificates(rows, stages)
    if write_certificates:
        target = root() / CERTIFICATE_DIR
        target.mkdir(parents=True, exist_ok=True)
        (target / ENVELOPE_NAME).write_bytes(envelope)
        (target / STAGES_NAME).write_bytes(internal)
    else:
        check_committed_certificates(envelope, internal)
    return "\n".join([
        "R32_FIXED27_QUARTIC_BRANCH_ENVELOPE: PASS",
        f"p={P} n={N} B={B} d={D} w={W} Base_cap={BASE_CAP}",
        f"base_rows={len(rows)} dyadic_states={len(stages)} branch_evaluations={2 * len(stages)}",
        "branch_order=K4>K3:0..7009,tie:7010..7012,K3>K4:7013..12997",
        "J_vs_PR930=gain_min:3,gain_max:37170,endpoint_equal:72180",
        "support_floor=nonendpoint:154023@c12996,endpoint:154021@c12997",
        "endpoint=r:50604,lambda:15900,Qres:kappa*C_Base^4,e_degree:15900",
        f"envelope_sha256={sha256_bytes(envelope)}",
        f"internal_states_sha256={sha256_bytes(internal)}",
        "source_pins=6 scalar_orientation=a0(z)/(z-y_i)*(c_i-c(z))",
        "ledger_delta=0 official_score=0/2",
        "RESULT: PASS",
        "",
    ])


def run_tamper() -> str:
    mutations = [
        ("block", replace(Config(), block=B // 2)),
        ("residual", replace(Config(), residual=D - 1)),
        ("quotient", replace(Config(), quotient=W - 1)),
        ("base_cap", replace(Config(), base_cap=BASE_CAP - 1)),
        ("stage_depth", replace(Config(), max_stage_exponent=12)),
        ("stage_ceiling", replace(Config(), ceil_stage_degree=True)),
        ("budget", replace(Config(), block_count_delta=0)),
        ("three_parts", replace(Config(), three_parts=4)),
        ("four_left", replace(Config(), four_left_parts=3)),
        ("four_right", replace(Config(), four_right_parts=2)),
        ("support_rounding", replace(Config(), support_uses_ceiling=False)),
    ]
    rejected = []
    for name, config in mutations:
        try:
            rows, stages = build(config)
            validate(rows, stages, config)
        except (CheckError, ValueError):
            rejected.append(name)
        else:
            raise CheckError(f"mutation survived: {name}")
    require(len(rejected) == len(mutations), "not all mutations rejected")
    return (
        "R32_FIXED27_QUARTIC_BRANCH_ENVELOPE_TAMPER: PASS\n"
        f"mutations={len(mutations)} rejected={','.join(rejected)}\n"
        "RESULT: PASS\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--write-certificates", action="store_true")
    args = parser.parse_args()
    if not args.check and not args.tamper_selftest and not args.write_certificates:
        args.check = True
    try:
        if args.check or args.write_certificates:
            print(run_check(write_certificates=args.write_certificates), end="")
        if args.tamper_selftest:
            print(run_tamper(), end="")
    except CheckError as exc:
        print(f"RESULT: FAIL ({exc})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
