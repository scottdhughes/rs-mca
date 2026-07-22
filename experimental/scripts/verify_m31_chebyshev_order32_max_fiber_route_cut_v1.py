#!/usr/bin/env python3
"""Verify the exact M31 order-32 Chebyshev maximum-fiber route cut.

The lightweight replay checks the deployed arithmetic, normalized quotient
labels, antipodal lower family, strict manifest, source hashes, and hostile
mutations.  ``--full-census`` compiles the companion C++ program and
exhausts all 17-subset sums for one representative of every negation-paired
puncture.  It then transports the results to all 32 punctures exactly.

This packet proves a finite route cut.  It does not close the M31 LIST row.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import itertools
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_ID = "rs-mca-m31-chebyshev-order32-max-fiber-route-cut-v1"
THEOREM_ID = "M31_CHEBYSHEV_ORDER32_MAX_FIBER_ROUTE_CUT_V1"
STATUS = "PROVED_EXACT_DEPLOYED_MAX_FIBER_AND_ROTATION_ROUTE_CUT_ROW_OPEN"

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
B_STAR = P**4 // 2**100
FORBIDDEN = B_STAR + 1
FOLD_DEGREE = 2**16
QUOTIENT_SIZE = N // FOLD_DEGREE
PARTIAL_FIBER = 1_911
MOVING_LABELS = 17
LOW_DEGREE = 15 * FOLD_DEGREE + PARTIAL_FIBER
HIGH_DEGREE = 16 * FOLD_DEGREE + PARTIAL_FIBER
SUBSET_COUNT = math.comb(31, 17)
MAX_FIBER = math.comb(15, 8)

LABELS = (
    1515618352, 2142581798, 519472958, 942646298,
    419097603, 7265015, 1945140650, 1179963362,
    970712266, 1077313983, 114254582, 186614876,
    869502427, 1006664095, 2113254329, 1972112504,
    175371143, 34229318, 1140819552, 1277981220,
    1960868771, 2033229065, 1070169664, 1176771381,
    967520285, 202342997, 2140218632, 1728386044,
    1204837349, 1628010689, 4901849, 631865295,
)

DISTINCT_SUM_COUNTS = (
    14269003, 14244093, 14262839, 14249825,
    14244487, 14249841, 14262617, 14247825,
    14253497, 14262119, 14304595, 14248081,
    14263481, 14290175, 14257265, 14306833,
    14306833, 14257265, 14290175, 14263481,
    14248081, 14304595, 14262119, 14253497,
    14247825, 14262617, 14249841, 14244487,
    14249825, 14262839, 14244093, 14269003,
)

KERNEL_COEFFICIENTS = (
    1, 0, 922883926, 0, 1787128909, 0, 237254192, 0,
    577962578, 0, 30724201, 0, 53081916, 0, 1776865326, 0,
    821554693,
)

INTRINSIC_KERNEL_COEFFICIENTS = (
    1, 0, 2147483503, 0, 3360, 0, 2147454079, 0,
    126720, 0, 2147190783, 0, 372736, 0, 2147237887, 0,
    65536,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_chebyshev_order32_max_fiber_route_cut_v1.schema.json"
SCRIPT_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_order32_max_fiber_route_cut_v1.py"
CPP_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_order32_sum_fiber_census_v1.cpp"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_order32_rotation_injectivity_v1.sage"
PACKET_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_order32_max_fiber_packet_v1.py"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_chebyshev_order32_max_fiber_route_cut_v1.md"
README_PATH = ROOT / "experimental/data/certificates/m31-chebyshev-order32-max-fiber-route-cut-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-chebyshev-order32-max-fiber-route-cut-v1/manifest.json"
FOUNDATION_PATH = ROOT / "tex/cs25_cap_v13_2.tex"
FIXED_G_PATH = ROOT / "experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md"
PARENT_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-fixed-g-universal-rs-embedding-v1/manifest.json"
PARENT_PACKET_PATH = ROOT / "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_packet_v1.py"

SOURCE_PATHS = (
    ("schema", SCHEMA_PATH, "Closed packet schema."),
    ("python_replay", SCRIPT_PATH, "Exact arithmetic, census orchestration, and mutations."),
    ("cpp_census", CPP_PATH, "Exhaustive meet-in-the-middle subset-sum census."),
    ("sage_rotation", SAGE_PATH, "Independent exact finite-field rank and gcd replay."),
    ("packet_verifier", PACKET_PATH, "Cross-runtime packet and predecessor verifier."),
    ("proof_note", NOTE_PATH, "Lift proof, exact census theorem, and route-cut scope."),
    ("certificate_readme", README_PATH, "Replay instructions and nonclaim contract."),
    ("deployed_domain_authority", FOUNDATION_PATH, "Pinned M31 Chebyshev domain and row parameters."),
    ("ordinary_rs_terminal", FIXED_G_PATH, "Broader fixed-G ordinary-RS terminal left open."),
    ("parent_manifest", PARENT_MANIFEST_PATH, "Sealed fixed-G predecessor certificate."),
    ("parent_packet_verifier", PARENT_PACKET_PATH, "Fail-closed fixed-G predecessor replay."),
)


class VerificationError(RuntimeError):
    """Raised when an exact packet gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value, sort_keys=True, separators=(",", ":"),
            ensure_ascii=True, allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (text + "\n").encode("ascii")


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unsigned)).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity JSON forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(len(raw) <= 16 * 1024 * 1024, "manifest size cap")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("manifest must be ASCII") from exc
    try:
        value = json.loads(
            text, object_pairs_hook=unique_object,
            parse_float=reject_float, parse_constant=reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise VerificationError("invalid JSON") from exc
    require(type(value) is dict, "manifest top-level object")
    require(raw == canonical_json(value), "canonical manifest bytes")
    return value


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def repo_relative(path: Path) -> str:
    resolved = path.resolve()
    require(resolved.is_relative_to(ROOT.resolve()), f"source inside repository: {path}")
    require(path.exists() and path.is_file() and not path.is_symlink(), f"regular source: {path}")
    relative = resolved.relative_to(ROOT.resolve())
    pure = PurePosixPath(relative.as_posix())
    require("." not in pure.parts and ".." not in pure.parts, "canonical source path")
    return pure.as_posix()


def chebyshev_power_two(value: int, log_degree: int) -> int:
    for _ in range(log_degree):
        value = (2 * value * value - 1) % P
    return value


def exact_arithmetic() -> dict[str, Any]:
    require(P == 2_147_483_647, "deployed prime")
    require(N == 2_097_152 and K == 1_048_576, "deployed code dimensions")
    require(B_STAR == 16_777_215 and FORBIDDEN == 16_777_216, "exact budget endpoint")
    require(RADIUS == 981_129, "exact radius")
    require(QUOTIENT_SIZE == 32, "order-32 quotient")
    require(17 * FOLD_DEGREE + PARTIAL_FIBER == AGREEMENT, "exact support size")
    require(LOW_DEGREE == 984_951 and LOW_DEGREE < K, "low degree below K")
    require(HIGH_DEGREE == 1_050_487 and K < HIGH_DEGREE, "one-prefix degree cut")
    require(SUBSET_COUNT == 265_182_525, "subset count")
    require(MAX_FIBER == 6_435, "antipodal family count")
    require(MAX_FIBER < FORBIDDEN, "route does not refute row")
    require(len(LABELS) == len(set(LABELS)) == 32, "32 distinct quotient labels")
    require(all(0 < value < P for value in LABELS), "nonzero quotient labels")
    require(sum(LABELS) % P == 0, "zero total quotient sum")
    require(all(chebyshev_power_two(2 * value % P, 5) == 0 for value in LABELS),
            "labels are roots of T_32(2Y)")
    require(all((LABELS[index] + LABELS[31 - index]) % P == 0 for index in range(32)),
            "pinned negation pairing")
    require(all(DISTINCT_SUM_COUNTS[index] == DISTINCT_SUM_COUNTS[31 - index]
                for index in range(32)), "distinct-count negation symmetry")

    small_histogram: dict[int, int] = {}
    for selected in itertools.combinations(LABELS[1:], 4):
        key = sum(selected) % P
        small_histogram[key] = small_histogram.get(key, 0) + 1
    require(len(small_histogram) == 25_931, "independent 4-subset distinct control")
    require(max(small_histogram.values()) == 105, "independent 4-subset max control")

    for omitted in range(32):
        negative = 31 - omitted
        other = [index for index in range(32) if index not in (omitted, negative)]
        pairs = {(min(index, 31 - index), max(index, 31 - index)) for index in other}
        require(len(pairs) == 15, f"15 complete antipodal pairs: omission {omitted}")
        require(1 + 2 * 8 == MOVING_LABELS, "structural family cardinality")
        require(math.comb(len(pairs), 8) == MAX_FIBER, "structural family count")
        require((-LABELS[omitted]) % P == LABELS[negative], "unique structural target")

    return {
        "B_star": B_STAR,
        "forbidden_size": FORBIDDEN,
        "subset_count_per_puncture": SUBSET_COUNT,
        "max_fiber": MAX_FIBER,
        "max_to_forbidden_gap": FORBIDDEN - MAX_FIBER,
        "small_control_distinct": len(small_histogram),
        "small_control_max": max(small_histogram.values()),
    }


LINE_RE = re.compile(
    r"^CHEB32_SUM_CENSUS_V1 omitted=(?P<omitted>\d+) "
    r"omitted_label=(?P<omitted_label>\d+) subsets=(?P<subsets>\d+) "
    r"distinct=(?P<distinct>\d+) max_fiber=(?P<max_fiber>\d+) "
    r"max_key=(?P<max_key>\d+) keys_at_max=(?P<keys_at_max>\d+) "
    r"structural_key=(?P<structural_key>\d+) "
    r"structural_family_count=(?P<structural_count>\d+) "
    r"structural_target_fiber=(?P<structural_target_fiber>\d+) status=PASS$"
)


def compile_census(output: Path) -> None:
    compiler = os.environ.get("CXX", "clang++")
    result = subprocess.run(
        [compiler, "-std=c++20", "-O3", "-DNDEBUG", str(CPP_PATH), "-o", str(output)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    require(result.returncode == 0, f"C++ compilation: {result.stderr.strip()}")


def run_omission(binary: Path, omitted: int) -> dict[str, int]:
    result = subprocess.run(
        [str(binary), str(omitted)], cwd=ROOT,
        text=True, capture_output=True, check=False,
    )
    require(result.returncode == 0, f"C++ omission {omitted}: {result.stderr.strip()}")
    lines = [line for line in result.stdout.splitlines() if line.startswith("CHEB32_SUM_CENSUS_V1 ")]
    require(len(lines) == 1, f"one census line: omission {omitted}")
    match = LINE_RE.fullmatch(lines[0])
    require(match is not None, f"parse census line: omission {omitted}")
    return {key: int(value) for key, value in match.groupdict().items()}


def full_census(workers: int) -> list[dict[str, int]]:
    require(1 <= workers <= 8, "census worker range")
    exact_arithmetic()
    with tempfile.TemporaryDirectory(prefix="m31-cheb32-census-") as directory:
        binary = Path(directory) / "census"
        compile_census(binary)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(run_omission, binary, omitted): omitted for omitted in range(16)}
            first_half = [future.result() for future in concurrent.futures.as_completed(futures)]
    first_half.sort(key=lambda row: row["omitted"])
    require([row["omitted"] for row in first_half] == list(range(16)), "all representative omissions")

    rows: list[dict[str, int] | None] = [None] * 32
    for row in first_half:
        omitted = row["omitted"]
        require(row["subsets"] == SUBSET_COUNT, f"full subset count: omission {omitted}")
        require(row["omitted_label"] == LABELS[omitted], f"omitted label: omission {omitted}")
        require(row["distinct"] == DISTINCT_SUM_COUNTS[omitted], f"distinct sums: omission {omitted}")
        require(row["max_fiber"] == MAX_FIBER, f"maximum fiber: omission {omitted}")
        require(row["max_key"] == (-LABELS[omitted]) % P, f"maximum key: omission {omitted}")
        require(row["keys_at_max"] == 1, f"unique maximum: omission {omitted}")
        require(row["structural_count"] == MAX_FIBER, f"structural family: omission {omitted}")
        require(row["structural_key"] == row["max_key"], f"structural key: omission {omitted}")
        require(row["structural_target_fiber"] == MAX_FIBER,
                f"structural target fiber: omission {omitted}")
        rows[omitted] = row
        partner = 31 - omitted
        rows[partner] = {
            **row,
            "omitted": partner,
            "omitted_label": LABELS[partner],
            "distinct": DISTINCT_SUM_COUNTS[partner],
            "max_key": (-LABELS[partner]) % P,
            "structural_key": (-LABELS[partner]) % P,
        }
    require(all(row is not None for row in rows), "transport covers all 32 punctures")
    return [row for row in rows if row is not None]


def source_bindings() -> list[dict[str, str]]:
    bindings = []
    for binding_id, path, role in SOURCE_PATHS:
        bindings.append({
            "binding_id": binding_id,
            "path": repo_relative(path),
            "role": role,
            "sha256": sha256_path(path),
        })
    return bindings


def build_payload() -> dict[str, Any]:
    arithmetic = exact_arithmetic()
    payload: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "scope": {
            "workboard_items": ["M0", "M1"],
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "deployed_row_closed": False,
            "ledger_movement": 0,
            "is_counterexample": False,
            "stable_paper_modified": False,
        },
        "deployed_parameters": {
            "p": P,
            "code_field_cardinality": str(P**4),
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "B_star": B_STAR,
            "forbidden_size": FORBIDDEN,
            "fold": "T_65536 on the pinned M31 Chebyshev domain",
            "fold_degree": FOLD_DEGREE,
            "quotient_size": QUOTIENT_SIZE,
            "partial_fiber_size": PARTIAL_FIBER,
            "moving_quotient_labels": MOVING_LABELS,
            "low_degree": LOW_DEGREE,
            "high_degree": HIGH_DEGREE,
        },
        "exact_lift": {
            "puncture_exclusion_required": True,
            "common_prefix": "e1(M)=sum(M)",
            "received_polynomial": "E*(T_c^17-e1(M)*T_c^16)",
            "codeword_polynomial": "received-E*prod_{b in M}(T_c-b)",
            "degree_below_K": LOW_DEGREE,
            "exact_agreement": AGREEMENT,
            "distinct_codewords": True,
            "base_field_embeds_in_deployed_code": True,
            "free_anchor_exists": False,
            "counterexample_threshold": FORBIDDEN,
        },
        "quotient_labels": list(LABELS),
        "census": {
            "algorithm": "exact meet-in-the-middle materialization, sort, and full run scan",
            "representative_omissions_exhausted": list(range(16)),
            "other_omissions_transport": "q -> -q exact bijection",
            "all_punctures_certified": 32,
            "subsets_per_puncture": SUBSET_COUNT,
            "distinct_sum_counts": list(DISTINCT_SUM_COUNTS),
            "maximum_fiber": MAX_FIBER,
            "keys_at_maximum_per_puncture": 1,
            "maximum_key_rule": "-omitted_label mod p",
            "structural_family": "negative omitted label plus both labels from any 8 of 15 remaining antipodal pairs",
            "structural_family_count": MAX_FIBER,
            "maximum_is_structured_T2_owner": True,
            "finite_computational_theorem": True,
        },
        "rotation_route_cut": {
            "modulus": "monic 2^-31*T_32(Y)",
            "rotation": "literal multiplicative-style Y^31*P_M mod modulus",
            "high_rows": [16, 31],
            "high_map_shape": [16, 17],
            "high_map_rank": 16,
            "kernel_dimension": 1,
            "kernel_coefficients_low_to_high": list(KERNEL_COEFFICIENTS),
            "rotated_kernel_remainder_degree_upper": 15,
            "kernel_coprime_to_quotient_locator": True,
            "intersection_contradiction": "equal high parts force disjoint 17-subsets of a 31-point set",
            "maximum_rotated_prefix_fiber": 1,
            "intrinsic_rotation": "T_31(Y)*P_M mod T_32(Y)",
            "intrinsic_chebyshev_identity_count": 17,
            "intrinsic_high_map_shape": [16, 17],
            "intrinsic_high_map_rank": 16,
            "intrinsic_kernel_dimension": 1,
            "intrinsic_kernel": "Chebyshev second-kind polynomial U_16",
            "intrinsic_kernel_coefficients_low_to_high": list(INTRINSIC_KERNEL_COEFFICIENTS),
            "intrinsic_integer_resultant": "2^496",
            "intrinsic_kernel_coprime_to_quotient_locator": True,
            "maximum_intrinsic_rotated_prefix_fiber": 1,
        },
        "higher_mds_diagnostic": {
            "primary_source": "Brakensiek-Gopi-Makam arXiv:2206.05256v4 Theorem 1.13",
            "punctured_quotient_code": "RS[F_p,Q\\{b0},16] of length 31",
            "agreement": 17,
            "distance": 14,
            "forbidden_list_size_under_LD_MDS_le_14": 15,
            "required_dual_gate": "MDS(15), equivalently the correctly scaled dual higher-MDS condition",
            "required_gate_holds": False,
            "failure_witness_size": MAX_FIBER,
        },
        "route_cut": {
            "arithmetic": arithmetic,
            "counterexample_route_eliminated": "complete scale-65536 order-32 one-prefix Chebyshev family",
            "rotation_adapter_eliminated": "literal Y^31 and intrinsic T_31 rotations on the Chebyshev quotient",
            "row_safety_proved": False,
            "U_Q_proved": False,
            "next_terminal": "UNPAID_C32768_ORDER64_TWO_PREFIX_OR_GLOBAL_Q_AGGREGATION",
        },
        "nonclaims": [
            "No M31 LIST row upper bound is proved.",
            "No Grande Finale v4 atom or refund is moved.",
            "No arbitrary-unit boundary census is bounded.",
            "No uniform deterministic punctured-RS cap is proved.",
            "No asymptotic maximum-fiber theorem is inferred from this finite census.",
            "Axle output is not used as proof evidence for this packet.",
        ],
        "source_bindings": source_bindings(),
    }
    return seal(payload)


def validate_payload(payload: dict[str, Any]) -> None:
    expected = build_payload()
    deep_exact(payload, expected)
    require(payload_sha256(payload) == payload["payload_sha256"], "payload seal")


def mutation_selftest() -> int:
    base = build_payload()
    mutations: list[tuple[str, Any]] = []

    def changed(name: str, mutator: Any) -> None:
        value = copy.deepcopy(base)
        mutator(value)
        mutations.append((name, value))

    changed("budget", lambda x: x["deployed_parameters"].__setitem__("B_star", B_STAR + 1))
    changed("forbidden", lambda x: x["exact_lift"].__setitem__("counterexample_threshold", B_STAR))
    changed("free_anchor", lambda x: x["exact_lift"].__setitem__("free_anchor_exists", True))
    changed("puncture", lambda x: x["exact_lift"].__setitem__("puncture_exclusion_required", False))
    changed("max_fiber", lambda x: x["census"].__setitem__("maximum_fiber", MAX_FIBER + 1))
    changed("max_keys", lambda x: x["census"].__setitem__("keys_at_maximum_per_puncture", 2))
    changed("sum_count", lambda x: x["census"]["distinct_sum_counts"].__setitem__(0, 1))
    changed("transport", lambda x: x["census"].__setitem__("other_omissions_transport", "assumed"))
    changed("label", lambda x: x["quotient_labels"].__setitem__(0, 0))
    changed("rank", lambda x: x["rotation_route_cut"].__setitem__("high_map_rank", 1))
    changed("kernel", lambda x: x["rotation_route_cut"]["kernel_coefficients_low_to_high"].__setitem__(0, 0))
    changed("gcd", lambda x: x["rotation_route_cut"].__setitem__("kernel_coprime_to_quotient_locator", False))
    changed("rotated_fiber", lambda x: x["rotation_route_cut"].__setitem__("maximum_rotated_prefix_fiber", 2))
    changed("intrinsic_rank", lambda x: x["rotation_route_cut"].__setitem__("intrinsic_high_map_rank", 15))
    changed("intrinsic_resultant", lambda x: x["rotation_route_cut"].__setitem__("intrinsic_integer_resultant", "2^495"))
    changed("intrinsic_fiber", lambda x: x["rotation_route_cut"].__setitem__("maximum_intrinsic_rotated_prefix_fiber", 2))
    changed("higher_mds", lambda x: x["higher_mds_diagnostic"].__setitem__("required_gate_holds", True))
    changed("ledger", lambda x: x["scope"].__setitem__("ledger_movement", 1))
    changed("closed", lambda x: x["scope"].__setitem__("deployed_row_closed", True))
    changed("terminal", lambda x: x["route_cut"].__setitem__("next_terminal", "SAFE"))
    changed("source_hash", lambda x: x["source_bindings"][0].__setitem__("sha256", "0" * 64))
    changed("source_drop", lambda x: x["source_bindings"].pop())
    changed("seal", lambda x: x.__setitem__("payload_sha256", "0" * 64))

    rejected = 0
    for name, value in mutations:
        try:
            validate_payload(value)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"mutation survived: {name}")
    require(rejected == len(mutations) == 23, "23/23 hostile mutations rejected")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate the pinned manifest")
    parser.add_argument("--full-census", action="store_true", help="run the exhaustive C++ census")
    parser.add_argument("--workers", type=int, default=4, help="parallel representative omissions (1..8)")
    parser.add_argument("--tamper-selftest", action="store_true", help="run hostile manifest mutations")
    parser.add_argument("--print-template", action="store_true", help="print canonical manifest template")
    args = parser.parse_args()
    if not any((args.check, args.full_census, args.tamper_selftest, args.print_template)):
        args.check = True

    try:
        arithmetic = exact_arithmetic()
        if args.print_template:
            sys.stdout.buffer.write(canonical_json(build_payload()))
        if args.check:
            validate_payload(strict_load(MANIFEST_PATH))
            print(f"LIGHTWEIGHT_OK max_fiber={MAX_FIBER} forbidden={FORBIDDEN} checks={CHECKS}")
        if args.full_census:
            rows = full_census(args.workers)
            print(
                "FULL_CENSUS_OK"
                f" punctures={len(rows)} subsets_each={SUBSET_COUNT}"
                f" max_fiber={MAX_FIBER} unique_max_each=1 checks={CHECKS}"
            )
        if args.tamper_selftest:
            print(f"TAMPER_OK rejected={mutation_selftest()} checks={CHECKS}")
        require(arithmetic["max_fiber"] == MAX_FIBER, "arithmetic result retained")
    except (OSError, VerificationError) as exc:
        print(f"VERIFICATION_FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
