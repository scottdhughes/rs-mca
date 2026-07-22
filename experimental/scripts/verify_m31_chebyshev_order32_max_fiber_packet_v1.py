#!/usr/bin/env python3
"""Release verifier for the M31 order-32 Chebyshev route-cut packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_chebyshev_order32_max_fiber_route_cut_v1.schema.json"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-chebyshev-order32-max-fiber-route-cut-v1/manifest.json"
PRIMARY_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_order32_max_fiber_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_order32_rotation_injectivity_v1.sage"
CPP_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_order32_sum_fiber_census_v1.cpp"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_chebyshev_order32_max_fiber_route_cut_v1.md"
README_PATH = ROOT / "experimental/data/certificates/m31-chebyshev-order32-max-fiber-route-cut-v1/README.md"
PARENT_PACKET_PATH = ROOT / "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_packet_v1.py"

SCHEMA_ID = "rs-mca-m31-chebyshev-order32-max-fiber-route-cut-v1"
THEOREM_ID = "M31_CHEBYSHEV_ORDER32_MAX_FIBER_ROUTE_CUT_V1"
STATUS = "PROVED_EXACT_DEPLOYED_MAX_FIBER_AND_ROTATION_ROUTE_CUT_ROW_OPEN"


class VerificationError(RuntimeError):
    """Raised when a release gate fails."""


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


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_load(path: Path, *, canonical: bool) -> dict[str, Any]:
    raw = path.read_bytes()
    require(len(raw) <= 16 * 1024 * 1024, f"size cap: {path.name}")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"ASCII JSON: {path.name}") from exc
    try:
        value = json.loads(text, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        raise VerificationError(f"valid JSON: {path.name}") from exc
    require(type(value) is dict, f"object JSON: {path.name}")
    if canonical:
        require(raw == canonical_json(value), f"canonical JSON: {path.name}")
    return value


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unsigned)).hexdigest()


def run_process(command: list[str], *, timeout: int, label: str,
                env: dict[str, str] | None = None) -> str:
    try:
        result = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True,
            timeout=timeout, check=False, env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationError(f"{label}: execution failed") from exc
    require(result.returncode == 0, f"{label}: exit status; {result.stderr.strip()}")
    require(result.stderr == "", f"{label}: stderr empty")
    require(result.stdout.endswith("\n"), f"{label}: final newline")
    return result.stdout


def validate_schema() -> None:
    schema = strict_load(SCHEMA_PATH, canonical=False)
    required = {
        "census", "deployed_parameters", "exact_lift",
        "higher_mds_diagnostic", "nonclaims", "payload_sha256",
        "quotient_labels", "rotation_route_cut", "route_cut", "schema",
        "scope", "source_bindings", "status", "theorem_id",
    }
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
            "schema draft")
    require(schema.get("$id") == SCHEMA_ID, "schema id")
    require(schema.get("type") == "object", "schema object")
    require(schema.get("additionalProperties") is False, "schema top closed")
    require(set(schema.get("required", [])) == required, "schema exact required keys")
    require(set(schema.get("properties", {})) == required, "schema exact property keys")
    for name, definition in schema["properties"].items():
        if definition.get("type") == "object":
            require(definition.get("additionalProperties") is False,
                    f"schema nested object closed: {name}")


def validate_semantics(manifest: dict[str, Any]) -> None:
    require(manifest.get("schema") == SCHEMA_ID, "manifest schema")
    require(manifest.get("theorem_id") == THEOREM_ID, "manifest theorem")
    require(manifest.get("status") == STATUS, "manifest status")
    require(payload_sha256(manifest) == manifest.get("payload_sha256"), "manifest payload seal")
    require(manifest["scope"] == {
        "deployed_row_closed": False,
        "is_counterexample": False,
        "ledger_movement": 0,
        "object": "LIST",
        "row": "Mersenne-31 list at 2^-100",
        "stable_paper_modified": False,
        "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
        "workboard_items": ["M0", "M1"],
    }, "manifest exact scope")
    require(manifest["census"]["maximum_fiber"] == 6435, "manifest max fiber")
    require(manifest["census"]["all_punctures_certified"] == 32, "manifest punctures")
    require(manifest["census"]["subsets_per_puncture"] == 265_182_525,
            "manifest subset count")
    require(manifest["exact_lift"]["counterexample_threshold"] == 16_777_216,
            "manifest forbidden endpoint")
    require(manifest["exact_lift"]["free_anchor_exists"] is False,
            "manifest no free anchor")
    require(manifest["rotation_route_cut"]["high_map_rank"] == 16,
            "manifest rotation rank")
    require(manifest["rotation_route_cut"]["maximum_rotated_prefix_fiber"] == 1,
            "manifest rotation injective")
    require(manifest["rotation_route_cut"]["intrinsic_high_map_rank"] == 16,
            "manifest intrinsic rotation rank")
    require(manifest["rotation_route_cut"]["intrinsic_integer_resultant"] == "2^496",
            "manifest intrinsic resultant")
    require(manifest["rotation_route_cut"]["maximum_intrinsic_rotated_prefix_fiber"] == 1,
            "manifest intrinsic rotation injective")
    require(manifest["higher_mds_diagnostic"]["required_gate_holds"] is False,
            "manifest higher-MDS specialization fails")
    require(manifest["route_cut"]["U_Q_proved"] is False, "manifest U_Q open")
    require(manifest["route_cut"]["row_safety_proved"] is False, "manifest row open")
    require(manifest["route_cut"]["next_terminal"] ==
            "UNPAID_C32768_ORDER64_TWO_PREFIX_OR_GLOBAL_Q_AGGREGATION",
            "manifest exact next terminal")

def validate_manifest() -> dict[str, Any]:
    manifest = strict_load(MANIFEST_PATH, canonical=True)
    validate_semantics(manifest)
    bindings = manifest["source_bindings"]
    require(type(bindings) is list and len(bindings) == 11, "eleven source bindings")
    require(len({item["binding_id"] for item in bindings}) == len(bindings),
            "unique source binding ids")
    for item in bindings:
        path = ROOT / item["path"]
        require(path.exists() and path.is_file() and not path.is_symlink(),
                f"bound regular source: {item['binding_id']}")
        require(path.resolve().is_relative_to(ROOT.resolve()),
                f"bound source contained: {item['binding_id']}")
        require(sha256_path(path) == item["sha256"],
                f"fresh source hash: {item['binding_id']}")
    return manifest


def verify_text_contracts() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# M31 order-32 Chebyshev maximum fiber and rotation route cut",
        "=\\binom{15}{8}=6435",
        "B_*+1=16{,}777{,}216",
        "There is no additional zero anchor",
        "265{,}182{,}525",
        "The rotated map is therefore injective.",
        "The exact 6435-member fiber shows",
        "Ledger movement is zero.",
        "UNPAID_C32768_ORDER64_TWO_PREFIX_OR_GLOBAL_Q_AGGREGATION",
    ):
        require(anchor in note, f"note anchor: {anchor}")
    readme = README_PATH.read_text(encoding="utf-8")
    for anchor in (
        "largest fiber of the 17-subset sum map has size exactly 6435",
        "Ledger movement is zero.",
        "--full-census --workers 4",
        "There is no sampling",
    ):
        require(anchor in readme, f"README anchor: {anchor}")


def replay_lightweight() -> None:
    normal = run_process(
        [sys.executable, str(PRIMARY_PATH), "--check", "--tamper-selftest"],
        timeout=120, label="primary replay",
    )
    optimized = run_process(
        [sys.executable, "-O", str(PRIMARY_PATH), "--check", "--tamper-selftest"],
        timeout=120, label="primary optimized replay",
    )
    require("LIGHTWEIGHT_OK max_fiber=6435 forbidden=16777216" in normal,
            "primary result")
    require("TAMPER_OK rejected=23" in normal, "primary tamper count")
    require(normal == optimized, "ordinary and optimized Python agree")

    sage_env = dict(os.environ)
    sage_home = Path("/tmp/rs-mca-cheb32-sage-home")
    sage_home.mkdir(parents=True, exist_ok=True)
    sage_env["HOME"] = str(sage_home)
    sage = run_process(
        ["/usr/local/bin/sage", str(SAGE_PATH), "--check"],
        timeout=900, label="Sage replay", env=sage_env,
    )
    require("M31 Chebyshev order-32 rotation injectivity Sage replay: PASS" in sage,
            "Sage rotation result")
    require("literal Y^31 high map: dimensions=(16,17) rank=16" in sage,
            "Sage literal rank")
    require("intrinsic T_31 high map: dimensions=(16,17) rank=16" in sage,
            "Sage intrinsic rank")
    require("Res_Z(U16,T32)=2^496" in sage, "Sage intrinsic resultant")
    sage_tamper = run_process(
        ["/usr/local/bin/sage", str(SAGE_PATH), "--tamper-selftest"],
        timeout=900, label="Sage tamper replay", env=sage_env,
    )
    require("tamper-selftest: PASS (40/40 rejected)" in sage_tamper,
            "Sage tamper result")

    with tempfile.TemporaryDirectory(prefix="m31-cheb32-packet-") as directory:
        binary = Path(directory) / "census"
        compile_result = subprocess.run(
            ["/usr/bin/clang++", "-std=c++20", "-O3", "-DNDEBUG",
             str(CPP_PATH), "-o", str(binary)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        require(compile_result.returncode == 0, "packet C++ compilation")
        require(compile_result.stderr == "", "packet C++ clean compilation")
        one = run_process([str(binary), "0"], timeout=180, label="C++ omission-0 census")
    require("subsets=265182525 distinct=14269003 max_fiber=6435" in one,
            "C++ omission-0 exact result")
    require("max_key=631865295 keys_at_max=1" in one, "C++ unique structural maximum")
    require("structural_family_count=6435 structural_target_fiber=6435 status=PASS" in one,
            "C++ structural match")


def replay_parent() -> None:
    output = run_process(
        [sys.executable, str(PARENT_PACKET_PATH), "--check"],
        timeout=1_800, label="fixed-G predecessor packet",
    )
    require("PASS" in output, "fixed-G predecessor PASS")


def packet_mutations(manifest: dict[str, Any]) -> int:
    mutations = []

    def changed(name: str, mutator: Any) -> None:
        value = copy.deepcopy(manifest)
        mutator(value)
        mutations.append((name, value))

    changed("max", lambda x: x["census"].__setitem__("maximum_fiber", 6436))
    changed("threshold", lambda x: x["exact_lift"].__setitem__("counterexample_threshold", 16_777_215))
    changed("anchor", lambda x: x["exact_lift"].__setitem__("free_anchor_exists", True))
    changed("rank", lambda x: x["rotation_route_cut"].__setitem__("high_map_rank", 1))
    changed("fiber", lambda x: x["rotation_route_cut"].__setitem__("maximum_rotated_prefix_fiber", 2))
    changed("intrinsic_rank", lambda x: x["rotation_route_cut"].__setitem__("intrinsic_high_map_rank", 15))
    changed("intrinsic_resultant", lambda x: x["rotation_route_cut"].__setitem__("intrinsic_integer_resultant", "2^495"))
    changed("intrinsic_fiber", lambda x: x["rotation_route_cut"].__setitem__("maximum_intrinsic_rotated_prefix_fiber", 2))
    changed("higher_mds", lambda x: x["higher_mds_diagnostic"].__setitem__("required_gate_holds", True))
    changed("ledger", lambda x: x["scope"].__setitem__("ledger_movement", 1))
    changed("closed", lambda x: x["scope"].__setitem__("deployed_row_closed", True))
    changed("U_Q", lambda x: x["route_cut"].__setitem__("U_Q_proved", True))
    changed("terminal", lambda x: x["route_cut"].__setitem__("next_terminal", "SAFE"))

    rejected = 0
    for name, value in mutations:
        value["payload_sha256"] = payload_sha256(value)
        try:
            validate_semantics(value)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"packet mutation survived: {name}")
    require(rejected == 13, "13/13 packet semantic mutations rejected")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--skip-parent", action="store_true",
                        help="developer-only narrow replay; release check must not use this")
    args = parser.parse_args()
    if not args.check and not args.tamper_selftest:
        args.check = True

    try:
        validate_schema()
        manifest = validate_manifest()
        verify_text_contracts()
        replay_lightweight()
        if not args.skip_parent:
            replay_parent()
        if args.tamper_selftest:
            rejected = packet_mutations(manifest)
            print(f"PACKET_TAMPER_OK rejected={rejected}")
        print(
            "M31 order-32 Chebyshev maximum-fiber packet v1: PASS\n"
            "exact max fiber: 6435; counterexample threshold: 16777216\n"
            "literal/intrinsic rotation fibers: 1/1; v4 ledger movement: 0; M31 row: OPEN\n"
            f"checks={CHECKS}"
        )
    except (KeyError, OSError, VerificationError) as exc:
        print(f"PACKET_FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
