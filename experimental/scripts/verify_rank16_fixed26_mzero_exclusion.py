#!/usr/bin/env python3
"""Fail-closed replay for the conditional fixed-26 M=0 exclusion."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Callable


class VerificationError(RuntimeError):
    """Raised when a pinned theorem or replay check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError("CHECK FAILED: " + message)


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
CERT_REL = "experimental/data/certificates/rank16-fixed26-mzero-exclusion"
CERT_DIR = REPO_ROOT / CERT_REL
MANIFEST_PATH = CERT_DIR / "manifest.json"
EXPECTED_PATH = CERT_DIR / "verify_rank16_fixed26_mzero_exclusion.expected.txt"
CHECKSUM_PATH = CERT_DIR / "SHA256SUMS"

NOTE_REL = "experimental/notes/l2/rank16_fixed26_mzero_exclusion.md"
SCRIPT_REL = "experimental/scripts/verify_rank16_fixed26_mzero_exclusion.py"
MANIFEST_REL = CERT_REL + "/manifest.json"
EXPECTED_REL = CERT_REL + "/verify_rank16_fixed26_mzero_exclusion.expected.txt"
ARTIFACTS = (NOTE_REL, SCRIPT_REL, MANIFEST_REL, EXPECTED_REL)

SCHEMA = "rs-mca.rank16-fixed26-mzero-exclusion.v1"
BASE = "3404d21b64c876c6d9b995ad3e29d7120ab27a54"
PROOF_AUDIT_PACKET = "55df7721f45642841be1e65e3f7717da3e5411e6055a70981669a320f7808937"
PROOF_AUDIT_RESPONSE = "b82da9df90723b8c2f7df3d95447f063208fbfc430242e6c2ef7f4693a0f237f"
SOURCE_AUDIT_PACKET = "ad5e8223e91a6d84aadd23f16fd2fccbfe47d1d8c5a2af2f3caa436a48b2d91c"
SOURCE_AUDIT_RESPONSE = "3205bf0cf6a67c86759aa918067a22e2a5e3284dbe0b4c462537a9339ef25dcf"
DEPENDENCY_HEADS = {
    "PR_957": "7e85fd0fa3f7ab4f1be9a968b2382a56eafe2c98",
    "PR_958": "7252e9de66ea1ae05332c82c7079d86eb0c20662",
}
SOURCE_PINS = {
    "experimental/notes/l2/rank16_fixed26_divided_difference_source_compiler.md":
        "e508b1847228475e5a71ab12df15d69d4091e7558a91f53e68261f06c42205ab",
    "experimental/scripts/verify_rank16_fixed26_divided_difference_source_compiler.py":
        "2dd8cd4d2df24510a4faa57d4ad70feda1b4505814233547f06dea7293afc744",
    "experimental/notes/l2/rank16_fixed26_polynomial_cross_minor_lift.md":
        "a8828bffa507b56ebc9795d9c2badc904a24df02ecbbd980faef1eafa28b81ea",
    "experimental/scripts/verify_rank16_fixed26_polynomial_cross_minor_lift.py":
        "1a5bec7dd8aefb8079c7cfa5e9d5b732c57e2365adfa94a8e5e28e12c6d2a86e",
    "experimental/notes/l2/rank16_fixed26_spectral_resolvent.md":
        "3c8aaddaa9993cb486d918c62101938f9c7bf4604a852863778f0ccd6886f0cd",
    "experimental/scripts/verify_rank16_fixed26_spectral_resolvent.py":
        "1327c517be7d87050785980b2780bbd99862e6de71e50d188b2a353706336014",
    "experimental/notes/l2/rank16_fixed26_global_spectral_rank_gap.md":
        "4d212b4dd1821cefb3866f67a6303e034be88e7ade3b57bd941aedb93e32dcdb",
    "experimental/scripts/verify_rank16_fixed26_global_spectral_rank_gap.py":
        "37a26c742f09b271f567c2a000810e15cd904ad7f301ff538679766980e0a53d",
    "experimental/notes/l2/rank16_fixed26_weighted_primary_rank_extension.md":
        "96098ea465e9d65a56a9b73e76c0aeaf437c58819a4e3bd1767a5b9efb8e46d7",
    "experimental/scripts/verify_rank16_fixed26_weighted_primary_rank_extension.py":
        "e4e59e0029c231736f3ec2e432fd9e46da4567c16620c5e24ffa152acf04825f",
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_manifest() -> dict[str, Any]:
    try:
        value = json.loads(
            MANIFEST_PATH.read_text(encoding="ascii"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError("cannot read strict ASCII manifest") from exc
    require(type(value) is dict, "manifest root object")
    return value


def manifest_contract(expected_sha256: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "base": BASE,
        "dependency_heads": DEPENDENCY_HEADS,
        "audits": {
            "hostile_proof_packet_sha256": PROOF_AUDIT_PACKET,
            "hostile_proof_response_sha256": PROOF_AUDIT_RESPONSE,
            "source_compiler_packet_sha256": SOURCE_AUDIT_PACKET,
            "source_compiler_response_sha256": SOURCE_AUDIT_RESPONSE,
        },
        "source_pins": SOURCE_PINS,
        "field_and_parameters": {
            "field_prime": 2_130_706_433,
            "domain_order": 2_097_152,
            "block_size_b": 32_768,
            "generator_degree_a": 67_472,
            "residual_degree_r": 63_601,
            "adjacent_gcd_degree_d": 28_897,
            "cofactor_quotient_degree_L3": 59_730,
            "scalar_group_order": 64,
        },
        "source_contract": {
            "literal_cell_only": True,
            "fixed_received_word_and_first_match_owner": True,
            "fixed_core_labels": 26,
            "external_labels": 8,
            "actual_valid_cross_edges": 16,
            "source_normalized_entries": True,
            "all_3x3_cross_minors_zero": True,
            "nonzero_2x2_gap": 5_807,
        },
        "theorem": {
            "transfer_degrees": [2, 3],
            "M_nonzero": True,
            "repeated_generator_factors_allowed": True,
            "cubic_J_degree_cap": 26_962,
            "cubic_scalar_roots": 0,
            "M_degree_caps": {"2": 100_237, "3": 133_003},
            "finite_ledger_delta": 0,
            "official_score": "0/2",
        },
        "nonclaims": {
            "source_cell_existence": False,
            "quadratic_rigidity_C_zero_D_equals_B": False,
            "all_eight_denominator_degree_bounds": False,
            "source_incidence_divisor_of_M": False,
            "strict_valuation_excess": False,
            "owner_collision": False,
            "global_aggregation": False,
            "grand_list": False,
            "grand_mca": False,
            "score_movement": False,
        },
        "remaining_wall": (
            "prove a literal source-cell existence or incidence theorem that "
            "consumes M!=0, then prove separate source-valid global aggregation"
        ),
        "expected_output": {"path": EXPECTED_REL, "sha256": expected_sha256},
        "artifacts": list(ARTIFACTS),
    }


def validate_manifest(value: dict[str, Any]) -> None:
    output = value.get("expected_output")
    require(type(output) is dict, "expected output object")
    digest = output.get("sha256")
    require(
        type(digest) is str and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
        "expected output SHA-256",
    )
    require(value == manifest_contract(digest), "semantic manifest contract")


def verify_source_pins() -> int:
    for relative, digest in SOURCE_PINS.items():
        path = (REPO_ROOT / relative).resolve()
        require(REPO_ROOT in path.parents, "source pin confinement")
        require(path.is_file(), "source pin exists: " + relative)
        require(sha256_path(path) == digest, "source pin digest: " + relative)
    return len(SOURCE_PINS)


def verify_artifacts(manifest: dict[str, Any]) -> int:
    raw = CHECKSUM_PATH.read_bytes()
    require(raw.endswith(b"\n"), "checksum final newline")
    lines = raw.decode("ascii").splitlines()
    require(len(lines) == len(ARTIFACTS), "checksum entry count")
    pattern = re.compile(r"([0-9a-f]{64})  ([!-~]+)")
    for line, expected_relative in zip(lines, ARTIFACTS):
        match = pattern.fullmatch(line)
        require(match is not None, "checksum syntax")
        digest, relative = match.groups()
        require(relative == expected_relative, "checksum order")
        require(sha256_path(REPO_ROOT / relative) == digest, "artifact digest")
    require(tuple(manifest["artifacts"]) == ARTIFACTS, "artifact manifest order")
    require(manifest["expected_output"]["path"] == EXPECTED_REL, "expected path")
    require(
        sha256_path(EXPECTED_PATH) == manifest["expected_output"]["sha256"],
        "expected output digest",
    )
    return len(lines)


def minimum_hitting_size(edges: set[frozenset[int]]) -> int:
    for size in range(9):
        for subset in combinations(range(8), size):
            low = frozenset(subset)
            if all(not edge.isdisjoint(low) for edge in edges):
                return size
    raise VerificationError("CHECK FAILED: no hitting set")


def verify_endpoints(manifest: dict[str, Any]) -> dict[str, Any]:
    params = manifest["field_and_parameters"]
    b = params["block_size_b"]
    a = params["generator_degree_a"]
    r = params["residual_degree_r"]
    d = params["adjacent_gcd_degree_d"]
    l3 = params["cofactor_quotient_degree_L3"]

    require(r - 2 * d == 5_807 > 0, "strict cross-minor endpoint")
    require(2 * b - 1 == 65_535 < a, "cancelled linear specialization")

    j2_cap = 3 * b - 1 - a
    j3_cap = l3 + 2 * b - a
    cubic_cap = a + j3_cap - 3 * b
    content_cap = j3_cap - b
    omitted_cap = a + content_cap
    require(j2_cap == 30_831, "quadratic unnormalized J0 cap")
    require(j3_cap == 57_794, "cubic unnormalized J0 cap")
    require(cubic_cap == 26_962 < b, "surviving cubic J cap")
    require(content_cap == 25_026, "M=0 cubic content cap")
    require(omitted_cap == 92_498 < 3 * b, "M=0 omitted-triple cap")
    require(a + j2_cap == 3 * b - 1 == 98_303, "all-choice endpoint")

    survivors: list[tuple[int, int, int]] = []
    for m in (2, 3):
        for h in range(1, m):
            q = m - h
            if (q + 1) * b - 1 >= a:
                survivors.append((m, h, q))
    require(survivors == [(3, 1, 2)], "cancellation degree classification")

    rows = tuple(range(4))
    columns = tuple(range(4, 8))
    edges = {
        frozenset((row, first, second))
        for row in rows
        for first, second in combinations(columns, 2)
    }
    require(len(edges) == 24, "omitted-triple count")
    hitting = minimum_hitting_size(edges)
    require(hitting == 3, "minimum low-label hitting set")

    m_caps = {}
    for m in (2, 3):
        resultant_cap = m * (a - 1) + (m - 1) * (b - 1)
        m_caps[str(m)] = resultant_cap - (m - 1) * a
    require(m_caps == {"2": 100_237, "3": 133_003}, "M-degree caps")
    require(manifest["theorem"]["M_degree_caps"] == m_caps, "manifest M caps")

    return {
        "j2": j2_cap,
        "j3": j3_cap,
        "cubic": cubic_cap,
        "content": content_cap,
        "omitted": omitted_cap,
        "survivors": survivors,
        "edges": len(edges),
        "hitting": hitting,
        "m_caps": m_caps,
    }


def semantic_mutation_selftests(manifest: dict[str, Any]) -> int:
    def mutation(path: tuple[str, ...], value: Any) -> Callable[[], None]:
        def run() -> None:
            changed = copy.deepcopy(manifest)
            target = changed
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            validate_manifest(changed)
        return run

    tests = (
        ("dependency head", mutation(("dependency_heads", "PR_957"), "0" * 40)),
        ("literal-cell guard", mutation(("source_contract", "literal_cell_only"), False)),
        ("edge count", mutation(("source_contract", "actual_valid_cross_edges"), 15)),
        ("minor gap", mutation(("source_contract", "nonzero_2x2_gap"), 5_806)),
        ("M nonzero", mutation(("theorem", "M_nonzero"), False)),
        ("cubic cap", mutation(("theorem", "cubic_J_degree_cap"), 26_963)),
        ("repeated factors", mutation(("theorem", "repeated_generator_factors_allowed"), False)),
        ("quadratic overclaim", mutation(("nonclaims", "quadratic_rigidity_C_zero_D_equals_B"), True)),
        ("aggregation overclaim", mutation(("nonclaims", "global_aggregation"), True)),
        ("score overclaim", mutation(("theorem", "official_score"), "1/2")),
    )
    for name, test in tests:
        try:
            test()
        except VerificationError:
            continue
        raise VerificationError("semantic mutation survived: " + name)
    return len(tests)


def render_report(
    source_count: int,
    endpoint: dict[str, Any],
    mutation_count: int,
    artifact_count: int,
) -> str:
    return "\n".join((
        "RANK16_FIXED26_MZERO_EXCLUSION: PASS",
        "schema=" + SCHEMA,
        "base=" + BASE,
        "dependency_heads=PR957:" + DEPENDENCY_HEADS["PR_957"]
        + ",PR958:" + DEPENDENCY_HEADS["PR_958"],
        f"source_pins=PASS,count={source_count}",
        "deployed=p2130706433,n2097152,b32768,a67472,r63601,d28897,L3_59730",
        f"cancelled_survivors={endpoint['survivors']}",
        "2b-1=65535<a=67472",
        f"J0_caps=quadratic:{endpoint['j2']},cubic:{endpoint['j3']}",
        "quadratic_all_choice_triple_cap=98303=3b-1",
        f"cubic_survival_J_cap={endpoint['cubic']}<b=32768",
        f"M0_cubic_content_cap={endpoint['content']}",
        f"M0_omitted_triple_cap={endpoint['omitted']}<3b=98304",
        f"hyperedges={endpoint['edges']};minimum_low_label_hitting_set={endpoint['hitting']}",
        "degree_caps=M2:100237,M3:133003",
        f"semantic_mutation_selftests=PASS,count={mutation_count}",
        f"artifact_checksums=PASS,count={artifact_count}",
        "finite_ledger_delta=0 official_score=0/2",
        "RESULT=PASS",
    )) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mutation-selftest-only",
        action="store_true",
        help="run only the fail-closed semantic mutation suite",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest()
        validate_manifest(manifest)
        if args.mutation_selftest_only:
            count = semantic_mutation_selftests(manifest)
            print(f"SEMANTIC_MUTATION_SELFTESTS: PASS count={count}")
            return 0
        source_count = verify_source_pins()
        endpoint = verify_endpoints(manifest)
        mutation_count = semantic_mutation_selftests(manifest)
        artifact_count = verify_artifacts(manifest)
        sys.stdout.write(render_report(source_count, endpoint, mutation_count, artifact_count))
        return 0
    except (OSError, UnicodeError, VerificationError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
