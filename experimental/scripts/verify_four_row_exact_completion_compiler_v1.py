#!/usr/bin/env python3
"""Verify the Grande Finale v3 four-row exact-completion compiler.

The canonical certificate is intentionally open.  It recomputes the four
deployed row calibrations, inventories the exact currently compatible inputs,
and enforces a fail-closed architecture boundary.  In particular, the legacy
KoalaBear M1/#995 ledger is reported but is not silently transplanted into the
active Grande Finale v3 completion ledger.

This script proves arithmetic and composition contracts.  It does not prove
the mathematical theorem named by a future candidate's source binding.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


sys.set_int_max_str_digits(2_500_000)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-four-row-exact-completion-compiler-v1"
ARTIFACT_KIND = "FOUR_ROW_EXACT_COMPLETION_COMPILER"
STATUS = "PROVED_EXACT_COMPILER_CURRENT_ARTIFACT_ARCHITECTURE_ROUTE_CUT_ROWS_OPEN"
TERMINAL = "ARCHITECTURE_ROUTE_CUT_CURRENT_ARTIFACT_SET"
ACTIVE_ARCH = "GRANDE_FINALE_V3_EXACT_COMPLETION"
LEGACY_ARCH = "LEGACY_KB_M1_FIRST_MATCH_V2"
CANDIDATE_SCHEMA = "rs-mca-four-row-exact-completion-candidate-v1"
PARTITION_MANIFEST_SCHEMA = "rs-mca-four-row-exact-partition-manifest-v1"
ATOM_MANIFEST_SCHEMA = "rs-mca-four-row-exact-atom-manifest-v1"
Q_COMPONENT_MANIFEST_SCHEMA = "rs-mca-four-row-q-component-manifest-v1"
ARCHITECTURE_MAPPING_SCHEMA = "rs-mca-architecture-mapping-manifest-v1"
ARCHITECTURE_OWNER_MAP_SCHEMA = "rs-mca-architecture-owner-map-manifest-v1"
STRUCTURAL_PREFLIGHT = "PASS_INTERNAL_CONSISTENCY_ONLY_NOT_A_CLOSURE_CERTIFICATE"
UNIT = "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE"
UNIFORM_QUANTIFIER = "UNIFORM_OVER_ALL_ADMISSIBLE_RECEIVED_LINES"
ALLOWED_SOURCE_ROOTS = frozenset({"archived", "docs", "experimental", "site", "tex"})
ALLOWED_SOURCE_SUFFIXES = frozenset(
    {".bib", ".json", ".lean", ".md", ".pdf", ".py", ".sage", ".tex", ".txt", ".yaml", ".yml"}
)
MAX_BOUND_SOURCE_BYTES = 128 * 1024 * 1024
MAX_TOTAL_BOUND_SOURCE_BYTES = 512 * 1024 * 1024
MAX_CANDIDATE_BYTES = 16 * 1024 * 1024
MAX_OWNER_IDS = 100_000
MAX_EMBEDDED_JSON_DEPTH = 32
MAX_EMBEDDED_JSON_BYTES = 1024 * 1024

BASE_COMMIT = "4106fc84b7d78d72f68a61398cd04ea260f53df4"

CERT_REL = Path(
    "experimental/data/certificates/four-row-exact-completion-compiler-v1/"
    "four_row_exact_completion_compiler_v1.json"
)
NOTE_REL = Path(
    "experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/four-row-exact-completion-compiler-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/verify_four_row_exact_completion_compiler_v1.py"
)
INDEPENDENT_REL = Path(
    "experimental/scripts/verify_four_row_exact_completion_compiler_v1_independent.py"
)
SCHEMA_REL = Path(
    "experimental/data/schemas/four_row_exact_completion_candidate_v1.schema.json"
)
ACTIVE_SPINE_REL = Path("experimental/grande_finale.tex")
DIMENSION_DEGREE_CURRENT_REL = Path("tex/cs25_cap_v13_2.tex")
UPAID_REL = Path("experimental/data/certificates/upaid-ledger/upaid_ledger.json")
KB995_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-histogram-incidence-closure-v1/"
    "m1_kb_rank9_full_histogram_incidence_closure_v1.json"
)
KB994_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-outside-carrier-incidence-splice-v1/"
    "m1_kb_rank9_full_outside_carrier_incidence_splice_v1.json"
)
KB995_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_full_histogram_incidence_closure_v1.md"
)
EXT_CORRECTION_REL = Path(
    "experimental/data/certificates/frontier-extension-fixed-line-audit-v1/"
    "frontier_extension_fixed_line_audit_v1.json"
)
EXT_CORRECTION_NOTE_REL = Path(
    "experimental/notes/frontier-adjacent/frontier_extension_fixed_line_audit_v1.md"
)
M31_SHELL_REL = Path("experimental/data/cap25_v13_m31_chebyshev_entropy_inverse_shells.json")
M31_SHELL_NOTE_REL = Path(
    "experimental/notes/thresholds/cap25_v13_m31_chebyshev_entropy_inverse_shells.md"
)
M31_SHELL_LEAN_REL = Path(
    "experimental/lean/m31_few_shell/M31FewShell/ChebyshevPrefix.lean"
)

FRONTIER_PACKET_ROOT = Path(
    "experimental/Conjectures_and_Barriers_RS_MCA_v4_1_source/"
    "experimental/data/certificates/frontier-adjacent"
)

P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1
N = 2**21
K_BASE = 2**20

ROWS: list[dict[str, Any]] = [
    {
        "row_id": "kb_mca",
        "name": "KoalaBear MCA",
        "kind": "MCA",
        "p": P_KB,
        "extension_degree": 6,
        "security_bits": 128,
        "K": K_BASE + 1,
        "a0": 1_116_047,
        "a_plus": 1_116_048,
        "w": 67_471,
        "average_ceiling": 57_198_030_366,
        "B_star": 274_980_728_111_395_087,
        "full_budget_multiplier": 4_807_520,
        "packet": "kb_mca_v1.packet.json",
    },
    {
        "row_id": "kb_list",
        "name": "KoalaBear list",
        "kind": "LIST",
        "p": P_KB,
        "extension_degree": 6,
        "security_bits": 128,
        "K": K_BASE,
        "a0": 1_116_046,
        "a_plus": 1_116_047,
        "w": 67_471,
        "average_ceiling": 65_065_153_468,
        "B_star": 274_980_728_111_395_087,
        "full_budget_multiplier": 4_226_236,
        "packet": "kb_list_v1.packet.json",
    },
    {
        "row_id": "m31_mca",
        "name": "Mersenne-31 MCA",
        "kind": "MCA",
        "p": P_M31,
        "extension_degree": 4,
        "security_bits": 100,
        "K": K_BASE + 1,
        "a0": 1_116_023,
        "a_plus": 1_116_024,
        "w": 67_447,
        "average_ceiling": 1_752_700,
        "B_star": 16_777_215,
        "full_budget_multiplier": 9,
        "packet": "m31_mca_v1.packet.json",
    },
    {
        "row_id": "m31_list",
        "name": "Mersenne-31 list",
        "kind": "LIST",
        "p": P_M31,
        "extension_degree": 4,
        "security_bits": 100,
        "K": K_BASE,
        "a0": 1_116_022,
        "a_plus": 1_116_023,
        "w": 67_447,
        "average_ceiling": 1_993_678,
        "B_star": 16_777_215,
        "full_budget_multiplier": 8,
        "packet": "m31_list_v1.packet.json",
    },
]
ROW_BY_ID = {row["row_id"]: row for row in ROWS}

EXPECTED_KB995_SCHEMA = "rs-mca-m1-kb-rank9-full-histogram-incidence-closure-v1"
EXPECTED_KB995_PAYLOAD = "62a929dfc3936da808031926b0964ec68a19f5672fb72b2661def1b45da50cc7"
EXPECTED_KB995_U_PAID = 422_354_730_332
EXPECTED_KB995_B_REMAINING = 274_980_305_756_664_755
EXPECTED_KB995_K_REMAINING = 4_807_513
EXPECTED_KB995_RESIDUAL = [67_471, 209_552]

EXPECTED_EXT_SCHEMA = "rs-mca-frontier-extension-fixed-line-audit-v1"
EXPECTED_EXT_PAYLOAD = "f6747d646c459f5829ea624f54f8c2e73632a4892bc8e33e3aa09d4c532dcfc5"
EXPECTED_EXT_STATUS = "COUNTEREXAMPLE_AND_CONTRACT_CORRECTION"

SOURCE_FILES = [
    NOTE_REL,
    README_REL,
    SCRIPT_REL,
    INDEPENDENT_REL,
    SCHEMA_REL,
    ACTIVE_SPINE_REL,
    DIMENSION_DEGREE_CURRENT_REL,
    UPAID_REL,
    KB995_REL,
    KB995_NOTE_REL,
    EXT_CORRECTION_REL,
    EXT_CORRECTION_NOTE_REL,
    M31_SHELL_REL,
    M31_SHELL_NOTE_REL,
    M31_SHELL_LEAN_REL,
    *[FRONTIER_PACKET_ROOT / row["packet"] for row in ROWS],
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_noninteger_number(token: str) -> Any:
    raise RuntimeError(f"noninteger or nonstandard JSON number: {token}")


def parse_json_strict_text(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_float=reject_noninteger_number,
        parse_constant=reject_noninteger_number,
    )
    require(isinstance(value, dict), "JSON root is not an object")
    return value


def load_json_strict(path: Path) -> dict[str, Any]:
    try:
        return parse_json_strict_text(path.read_text())
    except RuntimeError as exc:
        raise RuntimeError(f"strict JSON failure in {path}: {exc}") from exc


def load_candidate_json_strict(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        text = handle.read(MAX_CANDIDATE_BYTES + 1)
    require(len(text.encode("utf-8")) <= MAX_CANDIDATE_BYTES, "completion candidate exceeds size bound")
    try:
        return parse_json_strict_text(text)
    except RuntimeError as exc:
        raise RuntimeError(f"strict completion-candidate JSON failure in {path}: {exc}") from exc


def load_legacy_json(path: Path) -> dict[str, Any]:
    """Read provenance JSON that predates the integer-only certificate rule.

    Decimal tokens are retained as strings and are never used by a gate.
    Duplicate keys and nonstandard constants are still rejected.
    """
    value = json.loads(
        path.read_text(),
        object_pairs_hook=strict_object,
        parse_float=lambda token: token,
        parse_constant=reject_noninteger_number,
    )
    require(isinstance(value, dict), f"legacy JSON root is not an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def exact_json_equal(left: Any, right: Any) -> bool:
    """JSON-semantic equality that does not conflate booleans and integers."""
    return canonical_bytes(left) == canonical_bytes(right)


def payload_sha256(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def decimal_int(value: Any, label: str) -> int:
    require(isinstance(value, str), f"{label} is not a decimal string")
    require(value == "0" or (value and value[0] != "0"), f"{label} has leading zeros")
    require(value and all("0" <= ch <= "9" for ch in value), f"{label} is not an ASCII nonnegative integer")
    return int(value)


def require_exact_keys(
    value: Any,
    required: set[str],
    optional: set[str],
    label: str,
) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    keys = set(value)
    missing = required - keys
    extra = keys - required - optional
    require(not missing, f"{label} missing keys: {sorted(missing)}")
    require(not extra, f"{label} has schema-forbidden keys: {sorted(extra)}")
    return value


def canonical_bound_path(root: Path, rel_text: Any) -> Path:
    require(isinstance(rel_text, str) and rel_text, "empty or non-string source path")
    require(len(rel_text) <= 4096, "source path exceeds length bound")
    rel = Path(rel_text)
    require(not rel.is_absolute(), f"absolute source path forbidden: {rel_text}")
    require(rel_text == rel.as_posix(), f"noncanonical source path forbidden: {rel_text}")
    require(rel.parts and rel.parts[0] in ALLOWED_SOURCE_ROOTS, f"source root not allowlisted: {rel_text}")
    require(
        all(part not in {"", ".", ".."} and not part.startswith(".") for part in rel.parts),
        f"hidden or traversing source path forbidden: {rel_text}",
    )
    lexical = root / rel
    require(lexical.is_file(), f"bound source missing: {rel_text}")
    require(lexical.suffix.lower() in ALLOWED_SOURCE_SUFFIXES, f"source type not allowlisted: {rel_text}")
    require(lexical.stat().st_size <= MAX_BOUND_SOURCE_BYTES, f"bound source too large: {rel_text}")
    resolved_root = root.resolve()
    resolved = lexical.resolve()
    require(resolved == lexical.absolute(), f"symlinked source path forbidden: {rel_text}")
    require(resolved == resolved_root or resolved_root in resolved.parents, f"source escapes repository: {rel_text}")
    return resolved


def load_bound_manifest(
    bindings: dict[str, str],
    paths: dict[str, Path],
    source_key: Any,
    label: str,
) -> dict[str, Any]:
    require(isinstance(source_key, str) and source_key in bindings, f"{label} source binding absent")
    manifest = load_json_strict(paths[source_key])
    require(manifest.get("payload_sha256") == payload_sha256(manifest), f"{label} manifest payload hash mismatch")
    return manifest


def require_bound_digest(
    bindings: dict[str, str],
    source_key: Any,
    expected_digest: Any,
    label: str,
) -> None:
    require(isinstance(source_key, str) and source_key in bindings, f"{label} source binding absent")
    require(is_sha256(expected_digest), f"{label} digest invalid")
    require(bindings[source_key] == expected_digest, f"{label} digest is not bound to its declared source")


def source_bindings() -> dict[str, str]:
    out: dict[str, str] = {}
    for rel in SOURCE_FILES:
        path = ROOT / rel
        require(path.is_file(), f"missing bound source: {rel}")
        key = rel.as_posix()
        require(key not in out, f"duplicate source binding: {key}")
        out[key] = sha256_file(path)
    return dict(sorted(out.items()))


def verify_embedded_payload(value: dict[str, Any], expected: str, label: str) -> None:
    require(value.get("payload_sha256") == expected, f"{label} payload constant drift")
    require(payload_sha256(value) == expected, f"{label} payload self-hash drift")


def exact_binomials() -> dict[int, int]:
    """One exact C(n,a) call, then exact adjacent ratio updates."""
    targets = sorted({int(row["a_plus"]) for row in ROWS})
    current_a = targets[0]
    current = math.comb(N, current_a)
    out = {current_a: current}
    for target in targets[1:]:
        while current_a < target:
            current = current * (N - current_a) // (current_a + 1)
            current_a += 1
        out[target] = current
    return out


def effective_packet_pair(packet: dict[str, Any], kind: str) -> tuple[int, int]:
    if kind == "MCA":
        moved = packet.get("v13_raw_moved_pair")
        require(isinstance(moved, dict), "MCA packet lacks v13-raw moved pair")
        pair = moved.get("new_pair")
        require(isinstance(pair, dict), "MCA packet lacks effective new pair")
        return int(pair["a0_prime"]), int(pair["a0_prime_plus_1"])
    one = packet["agreement_interval"]["one_step_target"]
    require("v13_raw_moved_pair" not in packet, "list packet unexpectedly carries moved pair")
    return int(one["a0"]), int(one["a0_plus_1"])


def verify_text_contracts() -> None:
    active = (ROOT / ACTIVE_SPINE_REL).read_text()
    current_paper_d = (ROOT / DIMENSION_DEGREE_CURRENT_REL).read_text()
    note = (ROOT / NOTE_REL).read_text()
    readme = (ROOT / README_REL).read_text()
    schema_text = (ROOT / SCHEMA_REL).read_text()
    schema_doc = parse_json_strict_text(schema_text)

    active_fragments = [
        "U_{\\rm total}=U_{\\rm paid}+U_Q+U_{\\rm BC}+U_{\\rm new}",
        "For a list row replace $U_{\\rm BC}$ by the arbitrary-word interior codeword-ray term $U_{\\rm list-int}$.",
        "Conversely, every proof by this compiler must supply literal definitions and exact integer bounds",
        "No theorem in this paper proves $B(a_0+1)\\le B^*$ for any of the four deployed rows.",
        "KoalaBear MCA & 1116047 & 1116048 & 67471 & 274980728111395087",
        "Mersenne-31 list & 1116022 & 1116023 & 67447 & 16777215",
    ]
    note_fragments = [
        TERMINAL,
        "422354730332",
        "274980305756664755",
        "4807513",
        "UNPAID_PRIMITIVE",
        "cannot be paid by this direct route",
    ]
    readme_fragments = [TERMINAL, "all four row-sharp `U_Q`", "does **not** certify any row safe"]
    schema_fragments = [
        CANDIDATE_SCHEMA,
        ACTIVE_ARCH,
        "JOINT_MAX_ON_FROZEN_RESIDUAL",
        UNIT,
        "partition_sha256",
        "evaluation_domain_source_binding",
        "separate_suprema_forbidden",
        "owner_map_source_binding",
    ]
    for fragment in active_fragments:
        require(fragment in active, f"active-spine contract missing: {fragment}")
    for fragment in [
        "\\label{thm:extension-line-dimension-degree-ledger}",
        "\\Delta_Y |\\B|^{e_Y}",
        "contributes at most $\\Delta q_{\\mathrm{gen}}^{\\,e}$",
    ]:
        require(fragment in current_paper_d, f"current dimension-degree contract missing: {fragment}")
    for fragment in note_fragments:
        require(fragment in note, f"note contract missing: {fragment}")
    for fragment in readme_fragments:
        require(fragment in readme, f"README contract missing: {fragment}")
    for fragment in schema_fragments:
        require(fragment in schema_text, f"candidate schema contract missing: {fragment}")
    require(set(schema_doc["required"]) == CANDIDATE_TOP_KEYS, "candidate schema/runtime top-key drift")
    require(set(schema_doc["properties"]) == CANDIDATE_TOP_KEYS, "candidate schema/runtime top-property drift")
    require(
        set(schema_doc["properties"]["row_parameters"]["required"]) == ROW_PARAMETER_KEYS,
        "candidate schema/runtime row-parameter drift",
    )
    require(
        set(schema_doc["properties"]["partition"]["required"]) == PARTITION_KEYS,
        "candidate schema/runtime partition drift",
    )
    require(set(schema_doc["$defs"]["atomBase"]["required"]) == ATOM_KEYS, "candidate schema/runtime atom drift")
    require(
        set(schema_doc["$defs"]["qContract"]["required"]) == Q_CONTRACT_KEYS
        and set(schema_doc["$defs"]["qContract"]["properties"]) == Q_CONTRACT_KEYS,
        "candidate schema/runtime Q-contract drift",
    )
    require(
        set(schema_doc["$defs"]["architectureMapping"]["required"]) == ARCHITECTURE_MAPPING_KEYS
        and set(schema_doc["$defs"]["architectureMapping"]["properties"]) == ARCHITECTURE_MAPPING_KEYS,
        "candidate schema/runtime architecture-mapping drift",
    )


def load_and_verify_sources() -> dict[str, Any]:
    upaid = load_json_strict(ROOT / UPAID_REL)
    kb995 = load_json_strict(ROOT / KB995_REL)
    extension = load_json_strict(ROOT / EXT_CORRECTION_REL)
    m31_shell = load_json_strict(ROOT / M31_SHELL_REL)

    require(kb995.get("schema") == EXPECTED_KB995_SCHEMA, "#995 schema drift")
    verify_embedded_payload(kb995, EXPECTED_KB995_PAYLOAD, "#995")
    require(int(kb995["ledger"]["U_paid_after"]) == EXPECTED_KB995_U_PAID, "#995 paid total drift")
    require(
        int(kb995["ledger"]["B_remaining_after"]) == EXPECTED_KB995_B_REMAINING,
        "#995 remaining budget drift",
    )
    require(kb995["ledger"]["K_remaining"] == EXPECTED_KB995_K_REMAINING, "#995 Q capacity drift")
    require(kb995["ledger"]["U_Q"] is None, "#995 unexpectedly determines U_Q")
    require(kb995["ledger"]["residual_U_A"] is None, "#995 unexpectedly determines U_A")
    require(
        kb995["revised_residual"]["only_remaining_full_outside_slack_interval"]
        == EXPECTED_KB995_RESIDUAL,
        "#995 residual interval drift",
    )
    require(kb995["scope_guards"]["koalabear_row_closed"] is False, "#995 overclaims row closure")
    require(
        kb995["scalar_route_cut"]["actual_selector_or_counterexample_claimed"] is False,
        "#995 scalar route cut promoted to counterexample",
    )

    require(extension.get("schema") == EXPECTED_EXT_SCHEMA, "extension correction schema drift")
    require(extension.get("status") == EXPECTED_EXT_STATUS, "extension correction status drift")
    verify_embedded_payload(extension, EXPECTED_EXT_PAYLOAD, "extension correction")
    require(
        extension["supersession_gate"]["historical_acceptance_gate"] is False,
        "superseded extension packet restored as acceptance gate",
    )
    require(
        "Delta_ext_ceiling_int is a direct extension-chart degree ceiling"
        in extension["supersession_gate"]["invalidated_interpretations"],
        "extension multiplier correction missing",
    )
    require(
        extension["corrected_contract"]["chart_terminal_without_source_binding"]
        == "UNPAID_PRIMITIVE",
        "source-free extension terminal drift",
    )
    require(
        extension["routing_audit"]["proper_subfield_strata"]["status"]
        == "ROUTED_NOT_EXACTLY_PAID",
        "tower routing silently promoted to payment",
    )

    shell_constants = m31_shell["certificate"]["deployed_m31"]
    require(shell_constants["one_shell_cap"] == 2_029_705, "M31 one-shell cap drift")
    require(shell_constants["Bstar"] == 16_777_215, "M31 one-shell budget drift")
    require("CONJECTURAL" in m31_shell["status"], "M31 unrestricted status lost")

    upaid_rows = {row["row_id"]: row for row in upaid["deployed_rows"]}
    require(set(upaid_rows) == set(ROW_BY_ID), "partial-ledger row set drift")
    packets: dict[str, dict[str, Any]] = {}
    for row in ROWS:
        packet_path = ROOT / FRONTIER_PACKET_ROOT / row["packet"]
        packet = load_legacy_json(packet_path)
        packets[row["row_id"]] = packet
        a0, a_plus = effective_packet_pair(packet, row["kind"])
        require((a0, a_plus) == (row["a0"], row["a_plus"]), f"{row['row_id']} packet pair drift")
        packet_b = int(packet["target"]["B_star"]["value"])
        require(packet_b == row["B_star"], f"{row['row_id']} packet budget drift")
        urow = upaid_rows[row["row_id"]]
        require((urow["a0"], urow["a1"]) == (row["a0"], row["a_plus"]), f"{row['row_id']} partial-ledger pair drift")
        require(urow["K_prefix"] == row["K"], f"{row['row_id']} K drift")
        require(urow["B_star"] == row["B_star"], f"{row['row_id']} partial-ledger budget drift")
        require(urow["lower_L_a1"] == row["average_ceiling"], f"{row['row_id']} average drift")

    return {
        "upaid": upaid,
        "kb995": kb995,
        "extension": extension,
        "m31_shell": m31_shell,
        "packets": packets,
    }


def largest_extension_dimension(p: int, budget: int) -> int:
    require(p > 1 and budget >= 0, "invalid direct-extension capacity input")
    e = 0
    power = 1
    while power * p <= budget:
        power *= p
        e += 1
    return e


def required_atoms(kind: str) -> list[str]:
    return ["U_paid", "U_Q", "U_BC" if kind == "MCA" else "U_list_int", "U_new"]


def row_record(row: dict[str, Any], comb_value: int) -> dict[str, Any]:
    p = int(row["p"])
    w = int(row["w"])
    denominator = pow(p, w)
    average_ceiling = (comb_value + denominator - 1) // denominator
    B_star = pow(p, int(row["extension_degree"])) // pow(2, int(row["security_bits"]))
    multiplier = B_star * denominator // comb_value
    ceiling_multiplier = B_star // average_ceiling

    require(row["a_plus"] - row["K"] == w, f"{row['row_id']} w identity failed")
    require(average_ceiling == row["average_ceiling"], f"{row['row_id']} exact average drift")
    require(B_star == row["B_star"], f"{row['row_id']} exact budget drift")
    require(multiplier == row["full_budget_multiplier"], f"{row['row_id']} multiplier drift")
    require(ceiling_multiplier == multiplier, f"{row['row_id']} ceiling convention drift")

    max_e = largest_extension_dimension(p, B_star)
    max_delta = B_star // pow(p, max_e)
    first_forbidden = max_e + 1
    require(pow(p, first_forbidden) > B_star, f"{row['row_id']} extension cut failed")

    blockers = [
        "U_PAID_COMPLETE_NOT_INSTANTIATED",
        "UNPAID_ROW_SHARP_Q",
        "UNPAID_EXHAUSTIVE_BALANCED_CORE" if row["kind"] == "MCA" else "UNPAID_EXHAUSTIVE_LIST_INTERIOR",
        "UNPAID_EXTENSION_SUBCELLS",
        "UNPAID_COMPLETE_ADDBACK_AND_ZERO_RESIDUAL",
    ]

    scoped_q: dict[str, Any] | None = None
    if row["row_id"] == "m31_list":
        scoped_q = {
            "subcell": "M31_CHEBYSHEV_ONE_SHELL_ONLY",
            "upper_integer": "2029705",
            "B_star": "16777215",
            "status": "PAID_BY_THEOREM_SCOPED_SUBCELL",
            "exhaustive_for_U_Q": False,
            "unrestricted_multishell_status": "OPEN",
            "ledger_movement": "0",
        }

    legacy: dict[str, Any] | None = None
    if row["row_id"] == "kb_mca":
        legacy_den = denominator
        legacy_multiplier = EXPECTED_KB995_B_REMAINING * legacy_den // comb_value
        require(legacy_multiplier == EXPECTED_KB995_K_REMAINING, "#995 multiplier replay drift")
        legacy_max_e = largest_extension_dimension(p, EXPECTED_KB995_B_REMAINING)
        legacy = {
            "architecture_id": LEGACY_ARCH,
            "source_payload_sha256": EXPECTED_KB995_PAYLOAD,
            "U_paid": str(EXPECTED_KB995_U_PAID),
            "B_remaining": str(EXPECTED_KB995_B_REMAINING),
            "Q_multiplier_capacity": legacy_multiplier,
            "U_Q": None,
            "residual_U_A": None,
            "residual_interval": EXPECTED_KB995_RESIDUAL,
            "packet_scope": "FULL_OUTSIDE_COEFFICIENT_RANK_TWO_SUBPROGRAM",
            "inherited_ledger_scope": "LEGACY_FIRST_MATCH_LEDGER_WITH_EARLIER_GLOBAL_OWNERS",
            "received_pair_quantifier": "ARBITRARY_FIXED_PAIR_POINTWISE_UNIFORM_CAP",
            "translation_scope": "ONE_SP3_NORMALIZATION_PER_ARBITRARY_FIXED_PAIR",
            "fixed_pair_scope_alone_is_not_route_cut": True,
            "union_over_received_pairs_translations_selectors_sources_or_r_forbidden": True,
            "complete_rank9_payment": False,
            "row_closed": False,
            "active_architecture_mapping": None,
            "consumed_by_active_ledger": False,
            "direct_extension_all_remainder_capacity": {
                "max_e_Y": legacy_max_e,
                "max_Delta_at_max_e_Y": EXPECTED_KB995_B_REMAINING // pow(p, legacy_max_e),
                "first_forbidden_e_Y": legacy_max_e + 1,
            },
        }

    return {
        "row_id": row["row_id"],
        "name": row["name"],
        "object_kind": row["kind"],
        "active_architecture_id": ACTIVE_ARCH,
        "parameters": {
            "n": N,
            "k": K_BASE,
            "K": row["K"],
            "a0": row["a0"],
            "a_plus": row["a_plus"],
            "w": w,
            "p": p,
            "extension_degree": row["extension_degree"],
            "security_bits": row["security_bits"],
        },
        "exact_calibration": {
            "B_star": str(B_star),
            "average_ceiling": str(average_ceiling),
            "full_budget_Q_multiplier_floor": multiplier,
            "full_budget_Q_multiplier_via_ceiling": ceiling_multiplier,
            "binomial_bit_length": comb_value.bit_length(),
            "prefix_denominator_bit_length": denominator.bit_length(),
            "all_gates_exact_integer": True,
        },
        "active_completion": {
            "required_atoms": required_atoms(row["kind"]),
            "complete_atom_values": {atom: None for atom in required_atoms(row["kind"])},
            "witness_exhaustive_partition_sha256": None,
            "unresolved_cells": blockers,
            "total_charge": None,
            "closed": False,
            "terminal": TERMINAL,
        },
        "q_contract": {
            "status": "UNPAID_ROW_SHARP_Q",
            "upper_integer": None,
            "quantity": "MAX_OVER_ONE_FROZEN_FIRST_MATCH_RESIDUAL",
            "targets_or_averages_are_upper_bounds": False,
            "separate_ledger_generations_may_be_mixed": False,
            "ambient_normalization_requires_full_image_certificate": True,
            "row_and_domain_transport_required": True,
            "scoped_partial_subcell": scoped_q,
        },
        "direct_extension_Delta_p_power_e_route_cut": {
            "charge_formula": "Delta*p^e_Y",
            "assumption": "Delta>=1 and every other charge is nonnegative",
            "available_integer": str(B_star),
            "max_e_Y": max_e,
            "max_Delta_at_max_e_Y": B_star // pow(p, max_e),
            "first_forbidden_e_Y": first_forbidden,
            "first_forbidden_power_minus_budget": str(pow(p, first_forbidden) - B_star),
            "capacities_are_allocations": False,
        },
        "legacy_stack_local_progress": legacy,
        "verdict": "RED_OPEN_EXACT_INPUTS_MISSING",
    }


def build_certificate() -> dict[str, Any]:
    verify_text_contracts()
    load_and_verify_sources()
    binomials = exact_binomials()
    rows = [row_record(row, binomials[row["a_plus"]]) for row in ROWS]

    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "stack": {
            "base_commit": BASE_COMMIT,
            "base_role": "HEAD_OF_PR_995_LEGACY_KB_M1_STACK",
            "active_spine": ACTIVE_SPINE_REL.as_posix(),
            "active_architecture_id": ACTIVE_ARCH,
            "legacy_architecture_id": LEGACY_ARCH,
        },
        "statement_audited": (
            "Whether the exact current artifact set instantiates the Grande Finale v3 "
            "four-row completion theorem without mixing ledger generations, units, "
            "partitions, or received-line quantifiers."
        ),
        "active_ledger_contract": {
            "MCA": "U_total=U_paid+U_Q+U_BC+U_new",
            "LIST": "U_total=U_paid+U_Q+U_list_int+U_new",
            "unit": UNIT,
            "quantifier": UNIFORM_QUANTIFIER,
            "one_partition_required": True,
            "witness_exhaustive_required": True,
            "complete_addback_required": True,
            "unresolved_cells_allowed_for_closure": False,
            "integer_gate": "U_total<=B_star",
        },
        "rows": rows,
        "architecture_route_cut": {
            "terminal": TERMINAL,
            "active_rows_closed": [],
            "all_four_rows_open": True,
            "legacy_kb_m1_payload": EXPECTED_KB995_PAYLOAD,
            "legacy_to_active_mapping_certificate": None,
            "legacy_charge_consumed_by_active_ledger": False,
            "reason": (
                "The current exact KB M1 stack is source-bound to the legacy archived-v2 "
                "first-match architecture, while the active completion theorem is Grande "
                "Finale v3. No source-bound partition/owner mapping joins them, and every "
                "row also lacks an exhaustive row-sharp U_Q atom."
            ),
            "current_hypotheses_can_close_any_row": False,
            "future_theorems_cut": False,
        },
        "q_inventory": {
            "deployed_exact_U_Q_by_row": {row["row_id"]: None for row in ROWS},
            "exact_calibration_consumable": True,
            "johnson_anticode_status": "PROVED_BOUND_TOO_LARGE",
            "shallow_fourier_depth_status": "PROVED_OUT_OF_DEPLOYED_RANGE",
            "m31_one_shell_status": "PAID_SCOPED_SUBCELL_NOT_EXHAUSTIVE",
            "moment_route_status": "OPEN_AT_REQUIRED_ORDERS",
            "small_row_scans_status": "EMPIRICAL_ONLY",
            "targets_are_not_upper_bounds": True,
            "lower_floors_are_not_upper_bounds": True,
            "conditional_allocations_are_not_upper_bounds": True,
        },
        "extension_route_cut": {
            "corrected_source_payload": EXPECTED_EXT_PAYLOAD,
            "current_dimension_degree_source": DIMENSION_DEGREE_CURRENT_REL.as_posix(),
            "current_dimension_degree_source_bound_directly": True,
            "correction_core_python_and_sage_replay_status": "PASS",
            "correction_full_python_acceptance_status": "STALE_SOURCE_PIN_AFTER_PROMOTION",
            "correction_stale_paths": ["tex/cs25_cap_v12.tex", "experimental/cap25_cap_v13_raw.tex"],
            "superseded_multiplier_interpretation_rejected": True,
            "proper_subfield_routing_is_not_payment": True,
            "source_free_chart_terminal": "UNPAID_PRIMITIVE",
            "M31_positive_dimensional_direct_charge_can_fit": False,
            "KB_dimension_at_least_two_direct_charge_can_fit": False,
            "all_remainder_capacities_are_banked_charges": False,
        },
        "candidate_interface": {
            "schema_path": SCHEMA_REL.as_posix(),
            "schema_id": CANDIDATE_SCHEMA,
            "audit_flag": "--audit-candidate",
            "runtime_schema_shape_enforced": True,
            "canonical_contained_source_paths_required": True,
            "typed_partition_atom_q_and_mapping_adapters_required": True,
            "exact_owner_order_coverage_required": True,
            "candidate_payload_identity_required": True,
            "candidate_audit_is_structural_preflight_only": True,
            "candidate_audit_can_close_row": False,
            "reviewed_source_registry_entry_required_for_banking": True,
            "trusted_review_registry_entries": 0,
            "mechanical_validation_replaces_proof_review": False,
            "recognized_legacy_input_requires_explicit_architecture_mapping": True,
            "provenance_transform_detection_complete": False,
        },
        "scope_guards": {
            "mathematical_row_closure_claimed": False,
            "new_U_Q_bound_claimed": False,
            "new_balanced_core_or_list_interior_bound_claimed": False,
            "legacy_M1_result_invalidated": False,
            "scalar_route_cut_promoted_to_counterexample": False,
            "M31_one_shell_promoted_to_multishell": False,
            "superseded_extension_target_consumed": False,
            "lean_authorized": False,
        },
        "nonclaims": [
            "does not prove any deployed adjacent row safe",
            "does not construct a Reed-Solomon counterexample",
            "does not supply U_Q on any row",
            "does not supply exhaustive balanced-core or list-interior coverage",
            "does not invalidate the exact local results in the KoalaBear M1 stack",
            "does not infer mathematical truth merely from a future manifest passing structural checks",
            "does not authorize theorem promotion or Lean formalization",
        ],
        "source_bindings": source_bindings(),
    }
    certificate["payload_sha256"] = ""
    certificate["payload_sha256"] = payload_sha256(certificate)
    validate_current_semantics(certificate)
    return certificate


def validate_source_binding_map(bindings: Any, root: Path = ROOT) -> dict[str, Path]:
    require(isinstance(bindings, dict) and bindings, "empty source binding map")
    require(len(bindings) <= MAX_OWNER_IDS, "source binding map too large")
    resolved_paths: dict[str, Path] = {}
    seen_resolved: set[Path] = set()
    seen_physical: set[tuple[int, int]] = set()
    total_source_bytes = 0
    for rel_text, digest in bindings.items():
        require(isinstance(rel_text, str), "non-string source path")
        path = canonical_bound_path(root, rel_text)
        require(path not in seen_resolved, f"duplicate physical source binding: {rel_text}")
        seen_resolved.add(path)
        stat = path.stat()
        total_source_bytes += stat.st_size
        require(total_source_bytes <= MAX_TOTAL_BOUND_SOURCE_BYTES, "aggregate bound-source size exceeds audit limit")
        physical_id = (stat.st_dev, stat.st_ino)
        require(physical_id not in seen_physical, f"hardlinked duplicate source binding: {rel_text}")
        seen_physical.add(physical_id)
        require(is_sha256(digest), f"invalid source digest: {rel_text}")
        require(sha256_file(path) == digest, f"bound source hash drift: {rel_text}")
        resolved_paths[rel_text] = path
    return resolved_paths


def validate_current_semantics(candidate: dict[str, Any]) -> None:
    require(candidate.get("schema") == SCHEMA, "current certificate schema mismatch")
    require(candidate.get("artifact_kind") == ARTIFACT_KIND, "current artifact kind mismatch")
    require(candidate.get("status") == STATUS, "current status mismatch")
    require(candidate.get("payload_sha256") == payload_sha256(candidate), "current payload self-hash mismatch")
    require(candidate["stack"]["base_commit"] == BASE_COMMIT, "stack base drift")
    require(candidate["stack"]["active_architecture_id"] == ACTIVE_ARCH, "active architecture drift")
    require(candidate["stack"]["legacy_architecture_id"] == LEGACY_ARCH, "legacy architecture drift")
    require(candidate["active_ledger_contract"]["one_partition_required"] is True, "one-partition gate disabled")
    require(candidate["active_ledger_contract"]["unit"] == UNIT, "ledger unit drift")
    require(candidate["active_ledger_contract"]["quantifier"] == UNIFORM_QUANTIFIER, "ledger quantifier drift")

    rows = candidate.get("rows")
    require(isinstance(rows, list) and len(rows) == 4, "current row count drift")
    require([row["row_id"] for row in rows] == [row["row_id"] for row in ROWS], "current row order drift")
    for record, expected in zip(rows, ROWS):
        require(record["name"] == expected["name"], f"{expected['row_id']} name drift")
        require(record["object_kind"] == expected["kind"], f"{expected['row_id']} object-kind drift")
        params = record["parameters"]
        for key in ["K", "a0", "a_plus", "w", "p", "extension_degree", "security_bits"]:
            require(params[key] == expected[key], f"{expected['row_id']} parameter drift: {key}")
        exact = record["exact_calibration"]
        require(decimal_int(exact["B_star"], "B_star") == expected["B_star"], f"{expected['row_id']} B* drift")
        require(decimal_int(exact["average_ceiling"], "average") == expected["average_ceiling"], f"{expected['row_id']} average drift")
        require(exact["full_budget_Q_multiplier_floor"] == expected["full_budget_multiplier"], f"{expected['row_id']} Q capacity drift")
        require(exact["all_gates_exact_integer"] is True, f"{expected['row_id']} nonexact gate")
        completion = record["active_completion"]
        require(completion["required_atoms"] == required_atoms(expected["kind"]), f"{expected['row_id']} atom set drift")
        require(all(value is None for value in completion["complete_atom_values"].values()), f"{expected['row_id']} invented atom value")
        require(completion["witness_exhaustive_partition_sha256"] is None, f"{expected['row_id']} invented partition")
        require(completion["unresolved_cells"], f"{expected['row_id']} unresolved cells erased")
        require(completion["total_charge"] is None and completion["closed"] is False, f"{expected['row_id']} false closure")
        require(completion["terminal"] == TERMINAL, f"{expected['row_id']} terminal drift")
        q = record["q_contract"]
        require(q["status"] == "UNPAID_ROW_SHARP_Q" and q["upper_integer"] is None, f"{expected['row_id']} invented U_Q")
        require(q["separate_ledger_generations_may_be_mixed"] is False, f"{expected['row_id']} ledger mixing enabled")
        ext = record["direct_extension_Delta_p_power_e_route_cut"]
        max_e = largest_extension_dimension(expected["p"], expected["B_star"])
        require(ext["max_e_Y"] == max_e, f"{expected['row_id']} extension max dimension drift")
        require(ext["first_forbidden_e_Y"] == max_e + 1, f"{expected['row_id']} extension cut drift")
        require(ext["capacities_are_allocations"] is False, f"{expected['row_id']} extension capacity banked")
        if expected["row_id"] == "kb_mca":
            legacy = record["legacy_stack_local_progress"]
            require(isinstance(legacy, dict), "KB legacy progress missing")
            require(legacy["architecture_id"] == LEGACY_ARCH, "KB legacy architecture drift")
            require(decimal_int(legacy["U_paid"], "legacy U_paid") == EXPECTED_KB995_U_PAID, "KB legacy charge drift")
            require(legacy["active_architecture_mapping"] is None, "invented legacy-active mapping")
            require(legacy["consumed_by_active_ledger"] is False, "legacy charge silently consumed")
            require(legacy["row_closed"] is False, "legacy row falsely closed")
            require(legacy["packet_scope"] == "FULL_OUTSIDE_COEFFICIENT_RANK_TWO_SUBPROGRAM", "KB local packet scope drift")
            require(legacy["inherited_ledger_scope"] == "LEGACY_FIRST_MATCH_LEDGER_WITH_EARLIER_GLOBAL_OWNERS", "KB inherited ledger scope drift")
            require(legacy["received_pair_quantifier"] == "ARBITRARY_FIXED_PAIR_POINTWISE_UNIFORM_CAP", "KB local received-pair scope drift")
            require(legacy["translation_scope"] == "ONE_SP3_NORMALIZATION_PER_ARBITRARY_FIXED_PAIR", "KB local translation scope drift")
            require(legacy["fixed_pair_scope_alone_is_not_route_cut"] is True, "KB fixed-pair scope mislabelled as route cut")
            require(
                legacy["union_over_received_pairs_translations_selectors_sources_or_r_forbidden"] is True,
                "KB local union prohibition erased",
            )
        else:
            require(record["legacy_stack_local_progress"] is None, f"{expected['row_id']} received KB legacy input")

    route = candidate["architecture_route_cut"]
    require(route["terminal"] == TERMINAL, "architecture terminal drift")
    require(route["active_rows_closed"] == [] and route["all_four_rows_open"] is True, "false active closure")
    require(route["legacy_to_active_mapping_certificate"] is None, "invented architecture mapping")
    require(route["legacy_charge_consumed_by_active_ledger"] is False, "legacy charge consumed")
    require(route["current_hypotheses_can_close_any_row"] is False, "current artifacts overclaimed")
    require(candidate["q_inventory"]["deployed_exact_U_Q_by_row"] == {row["row_id"]: None for row in ROWS}, "Q inventory drift")
    require(candidate["extension_route_cut"]["superseded_multiplier_interpretation_rejected"] is True, "superseded extension target restored")
    require(candidate["extension_route_cut"]["current_dimension_degree_source"] == DIMENSION_DEGREE_CURRENT_REL.as_posix(), "current extension theorem source drift")
    require(candidate["extension_route_cut"]["current_dimension_degree_source_bound_directly"] is True, "current extension theorem not directly bound")
    require(candidate["extension_route_cut"]["correction_full_python_acceptance_status"] == "STALE_SOURCE_PIN_AFTER_PROMOTION", "stale correction replay hidden")
    interface = candidate["candidate_interface"]
    require(interface["runtime_schema_shape_enforced"] is True, "candidate runtime schema gate disabled")
    require(interface["canonical_contained_source_paths_required"] is True, "candidate source containment gate disabled")
    require(interface["typed_partition_atom_q_and_mapping_adapters_required"] is True, "candidate typed-adapter gate disabled")
    require(interface["exact_owner_order_coverage_required"] is True, "candidate owner-coverage gate disabled")
    require(interface["candidate_payload_identity_required"] is True, "candidate payload identity gate disabled")
    require(interface["candidate_audit_is_structural_preflight_only"] is True, "candidate preflight scope widened")
    require(interface["candidate_audit_can_close_row"] is False, "candidate structural preflight can close a row")
    require(interface["reviewed_source_registry_entry_required_for_banking"] is True, "reviewed-source banking gate disabled")
    require(interface["trusted_review_registry_entries"] == 0, "unreviewed source registry entry invented")
    require(interface["mechanical_validation_replaces_proof_review"] is False, "candidate audit promoted to proof review")
    require(interface["recognized_legacy_input_requires_explicit_architecture_mapping"] is True, "recognized legacy mapping gate disabled")
    require(interface["provenance_transform_detection_complete"] is False, "heuristic provenance detector overclaimed")
    require(candidate["scope_guards"]["mathematical_row_closure_claimed"] is False, "scope guard permits closure")
    require(candidate["scope_guards"]["scalar_route_cut_promoted_to_counterexample"] is False, "route cut promoted")
    validate_source_binding_map(candidate["source_bindings"])


def validate_canonical(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    validate_current_semantics(actual)
    require(canonical_bytes(actual) == canonical_bytes(expected), "certificate differs from canonical payload")


def check_certificate() -> None:
    expected = build_certificate()
    actual = load_json_strict(ROOT / CERT_REL)
    validate_canonical(actual, expected)


Q_CONTRACT_KEYS = {
    "ledger_generation_id",
    "n",
    "K",
    "a_plus",
    "w",
    "p",
    "evaluation_domain_source_binding",
    "evaluation_domain_sha256",
    "priority_map_source_binding",
    "priority_map_sha256",
    "residual_predicate_source_binding",
    "residual_predicate_sha256",
    "target_map_source_binding",
    "target_map_sha256",
    "support_to_parameter_coalescing_source_binding",
    "support_to_parameter_coalescing_sha256",
    "support_orientation",
    "support_transport_binding",
    "support_transport_sha256",
    "normalization",
    "full_image_certificate_binding",
    "full_image_certificate_sha256",
    "effective_image_cardinality",
    "aggregation_mode",
    "separate_suprema_forbidden",
    "joint_max_certificate_binding",
    "joint_max_certificate_sha256",
    "upper_integer",
}
CANDIDATE_TOP_KEYS = {
    "schema",
    "payload_sha256",
    "row_id",
    "architecture_id",
    "row_parameters",
    "partition",
    "atoms",
    "claim",
    "source_bindings",
    "architecture_mapping",
}
ROW_PARAMETER_KEYS = {"n", "K", "a_plus", "w", "p", "object_kind"}
PARTITION_KEYS = {
    "partition_sha256",
    "source_binding",
    "witness_exhaustive",
    "uniform_over_received_lines",
    "same_partition_for_all_atoms",
    "addback_complete",
    "owner_order",
    "unresolved_cells",
}
ATOM_KEYS = {
    "atom_id",
    "row_id",
    "architecture_id",
    "partition_sha256",
    "value",
    "status",
    "unit",
    "quantifier",
    "owner_ids",
    "source_binding",
    "source_statement",
    "dependency_architecture_ids",
    "unresolved_hypotheses",
}
ARCHITECTURE_MAPPING_KEYS = {
    "from_architecture",
    "to_architecture",
    "row_id",
    "source_binding",
    "legacy_source_binding",
    "active_source_binding",
    "legacy_payload_sha256",
    "target_partition_sha256",
    "owner_map_source_binding",
    "owner_map_sha256",
    "target_atom_id",
    "legacy_charge_value",
    "mapped_charge_value",
    "target_atom_charge_includes_mapped_value",
    "legacy_owner_ids",
    "mapped_active_owner_ids",
    "owner_mapping",
    "unit",
    "quantifier",
    "uniform_over_received_lines",
    "complete_owner_map",
    "proof_source_bindings",
    "unresolved_hypotheses",
}


def validate_candidate_schema_shape(candidate: Any) -> dict[str, Any]:
    """Dependency-free runtime mirror of the published candidate schema."""
    top = require_exact_keys(
        candidate,
        CANDIDATE_TOP_KEYS,
        set(),
        "completion candidate",
    )
    require_exact_keys(top["row_parameters"], ROW_PARAMETER_KEYS, set(), "row_parameters")
    require_exact_keys(
        top["partition"],
        PARTITION_KEYS,
        set(),
        "partition",
    )
    atoms = top["atoms"]
    require(isinstance(atoms, list) and len(atoms) == 4, "candidate must contain exactly four atoms")
    for index, atom in enumerate(atoms):
        obj = require_exact_keys(atom, ATOM_KEYS, {"q_contract"}, f"atom[{index}]")
        if obj.get("atom_id") == "U_Q":
            require_exact_keys(obj.get("q_contract"), Q_CONTRACT_KEYS, set(), "U_Q.q_contract")
        else:
            require("q_contract" not in obj, f"{obj.get('atom_id')} carries a forbidden q_contract")
    require_exact_keys(top["claim"], {"closed", "total_charge", "B_star"}, set(), "claim")
    require(isinstance(top["source_bindings"], dict), "source_bindings is not an object")
    mapping = top["architecture_mapping"]
    if mapping is not None:
        require_exact_keys(
            mapping,
            ARCHITECTURE_MAPPING_KEYS,
            set(),
            "architecture_mapping",
        )
    return top


def validate_proof_source_list(
    value: Any,
    bindings: dict[str, str],
    used: set[str],
    label: str,
    source_consumers: dict[str, set[str]] | None = None,
    consumer: str | None = None,
) -> list[str]:
    require(isinstance(value, list) and value, f"{label} proof source list empty")
    require(len(value) <= MAX_OWNER_IDS, f"{label} proof source list too large")
    require(all(isinstance(key, str) and key in bindings for key in value), f"{label} has an unbound proof source")
    require(len(value) == len(set(value)), f"{label} duplicates a proof source")
    used.update(value)
    if source_consumers is not None:
        require(consumer is not None, f"{label} lacks a source-consumer scope")
        for key in value:
            source_consumers.setdefault(key, set()).add(consumer)
    return value


def validate_q_component_manifest(
    source_key: Any,
    digest: Any,
    component_kind: str,
    expected_claims: dict[str, Any],
    row_id: str,
    partition_hash: str,
    row: dict[str, Any],
    bindings: dict[str, str],
    paths: dict[str, Path],
    used: set[str],
    source_consumers: dict[str, set[str]],
) -> None:
    require_bound_digest(bindings, source_key, digest, f"U_Q {component_kind}")
    used.add(source_key)
    source_consumers.setdefault(source_key, set()).add("U_Q")
    manifest = load_bound_manifest(bindings, paths, source_key, f"U_Q {component_kind}")
    require_exact_keys(
        manifest,
        {
            "schema",
            "payload_sha256",
            "component_kind",
            "row_id",
            "architecture_id",
            "partition_sha256",
            "n",
            "K",
            "a_plus",
            "w",
            "p",
            "claims",
            "proof_source_bindings",
            "unresolved_hypotheses",
        },
        set(),
        f"U_Q {component_kind} manifest",
    )
    require(manifest["schema"] == Q_COMPONENT_MANIFEST_SCHEMA, f"U_Q {component_kind} schema mismatch")
    require(manifest["component_kind"] == component_kind, f"U_Q component kind mismatch: {component_kind}")
    require(manifest["row_id"] == row_id and manifest["architecture_id"] == ACTIVE_ARCH, f"U_Q {component_kind} row/architecture mismatch")
    require(manifest["partition_sha256"] == partition_hash, f"U_Q {component_kind} partition mismatch")
    require(all(type(manifest[key]) is int for key in ["n", "K", "a_plus", "w", "p"]), f"U_Q {component_kind} row parameters are not JSON integers")
    require(
        (manifest["n"], manifest["K"], manifest["a_plus"], manifest["w"], manifest["p"])
        == (N, row["K"], row["a_plus"], row["w"], row["p"]),
        f"U_Q {component_kind} row-parameter mismatch",
    )
    require(exact_json_equal(manifest["claims"], expected_claims), f"U_Q {component_kind} claim mismatch")
    require(manifest["unresolved_hypotheses"] == [], f"U_Q {component_kind} has unresolved hypotheses")
    validate_proof_source_list(
        manifest["proof_source_bindings"], bindings, used, f"U_Q {component_kind}", source_consumers, "U_Q"
    )


def validate_q_contract(
    q: dict[str, Any],
    atom_value: str,
    row_id: str,
    partition_hash: str,
    row: dict[str, Any],
    bindings: dict[str, str],
    paths: dict[str, Path],
    used: set[str],
    source_consumers: dict[str, set[str]],
) -> None:
    require(q["ledger_generation_id"] == ACTIVE_ARCH, "U_Q ledger generation mismatch")
    require(all(type(q[key]) is int for key in ["n", "K", "a_plus", "w", "p"]), "U_Q row parameters are not JSON integers")
    require(
        (q["n"], q["K"], q["a_plus"], q["w"], q["p"])
        == (N, row["K"], row["a_plus"], row["w"], row["p"]),
        "U_Q row-parameter contract mismatch",
    )
    component_specs = [
        ("evaluation_domain_source_binding", "evaluation_domain_sha256", "EVALUATION_DOMAIN", {"evaluation_domain_frozen": True}),
        ("priority_map_source_binding", "priority_map_sha256", "PRIORITY_MAP", {"first_match_priority_frozen": True}),
        ("residual_predicate_source_binding", "residual_predicate_sha256", "RESIDUAL_PREDICATE", {"residual_predicate_frozen": True}),
        ("target_map_source_binding", "target_map_sha256", "TARGET_MAP", {"target_map_frozen": True}),
        (
            "support_to_parameter_coalescing_source_binding",
            "support_to_parameter_coalescing_sha256",
            "SUPPORT_TO_PARAMETER_COALESCING",
            {"support_to_parameter_coalescing_exhaustive": True},
        ),
        (
            "joint_max_certificate_binding",
            "joint_max_certificate_sha256",
            "JOINT_MAXIMUM",
            {
                "evaluation_domain_sha256": q["evaluation_domain_sha256"],
                "priority_map_sha256": q["priority_map_sha256"],
                "residual_predicate_sha256": q["residual_predicate_sha256"],
                "target_map_sha256": q["target_map_sha256"],
                "support_to_parameter_coalescing_sha256": q["support_to_parameter_coalescing_sha256"],
                "support_orientation": q["support_orientation"],
                "support_transport_sha256": q["support_transport_sha256"],
                "normalization": q["normalization"],
                "full_image_certificate_sha256": q["full_image_certificate_sha256"],
                "effective_image_cardinality": q["effective_image_cardinality"],
                "aggregation_mode": "JOINT_MAX_ON_FROZEN_RESIDUAL",
                "separate_suprema_forbidden": True,
                "upper_integer": atom_value,
            },
        ),
    ]
    for source_field, digest_field, kind, claims in component_specs:
        validate_q_component_manifest(
            q[source_field], q[digest_field], kind, claims, row_id, partition_hash, row, bindings, paths, used, source_consumers
        )
    require(q["support_orientation"] in {"AGREEMENT", "COMPLEMENT_WITH_PROVED_TRANSPORT"}, "U_Q support orientation invalid")
    if q["support_orientation"] == "AGREEMENT":
        require(q["support_transport_binding"] is None and q["support_transport_sha256"] is None, "agreement Q carries spurious transport")
    else:
        validate_q_component_manifest(
            q["support_transport_binding"],
            q["support_transport_sha256"],
            "SUPPORT_TRANSPORT",
            {"support_orientation": "COMPLEMENT_WITH_PROVED_TRANSPORT", "transport_total": True},
            row_id,
            partition_hash,
            row,
            bindings,
            paths,
            used,
            source_consumers,
        )
    require(q["normalization"] in {"EFFECTIVE_IMAGE", "AMBIENT_WITH_FULL_IMAGE_CERTIFICATE"}, "U_Q normalization invalid")
    require(len(q["effective_image_cardinality"]) <= 10, "U_Q effective image decimal too long")
    image_size = decimal_int(q["effective_image_cardinality"], "U_Q effective image")
    require(1 <= image_size <= row["p"], "U_Q effective image outside base field")
    if q["normalization"] == "EFFECTIVE_IMAGE":
        require(q["full_image_certificate_binding"] is None and q["full_image_certificate_sha256"] is None, "effective-image Q carries spurious full-image certificate")
    else:
        require(image_size == row["p"], "ambient normalization lacks full image cardinality")
        validate_q_component_manifest(
            q["full_image_certificate_binding"],
            q["full_image_certificate_sha256"],
            "FULL_IMAGE",
            {
                "normalization": "AMBIENT_WITH_FULL_IMAGE_CERTIFICATE",
                "effective_image_cardinality": str(row["p"]),
                "full_image": True,
            },
            row_id,
            partition_hash,
            row,
            bindings,
            paths,
            used,
            source_consumers,
        )
    require(q["aggregation_mode"] == "JOINT_MAX_ON_FROZEN_RESIDUAL", "U_Q separate-supremum aggregation forbidden")
    require(q["separate_suprema_forbidden"] is True, "U_Q separate-supremum guard disabled")
    require(q["upper_integer"] == atom_value, "U_Q structured proof value differs from atom")


def audit_closure_candidate(candidate: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    """Structural preflight for a future claimed closing manifest.

    This verifies internal identity, scope, composition, and arithmetic only.
    Candidate-authored adapters are not trusted proof attestations, so a pass
    never banks an atom or certifies row closure.
    """
    candidate = validate_candidate_schema_shape(candidate)
    require(candidate["schema"] == CANDIDATE_SCHEMA, "completion candidate schema mismatch")
    require(candidate["payload_sha256"] == payload_sha256(candidate), "completion candidate payload hash mismatch")
    row_id = candidate["row_id"]
    require(row_id in ROW_BY_ID, "unknown completion candidate row")
    row = ROW_BY_ID[row_id]
    require(candidate["architecture_id"] == ACTIVE_ARCH, "candidate is not in active architecture")
    row_parameters = candidate["row_parameters"]
    require(all(type(row_parameters[key]) is int for key in ["n", "K", "a_plus", "w", "p"]), "candidate row parameters are not JSON integers")
    require(isinstance(row_parameters["object_kind"], str), "candidate object kind is not a string")
    require(
        (row_parameters["n"], row_parameters["K"], row_parameters["a_plus"], row_parameters["w"], row_parameters["p"], row_parameters["object_kind"])
        == (N, row["K"], row["a_plus"], row["w"], row["p"], row["kind"]),
        "candidate row parameters mismatch",
    )
    bindings = candidate["source_bindings"]
    paths = validate_source_binding_map(bindings, root)
    used_sources: set[str] = set()
    source_consumers: dict[str, set[str]] = {}

    partition = candidate["partition"]
    partition_hash = partition["partition_sha256"]
    require_bound_digest(bindings, partition["source_binding"], partition_hash, "partition")
    used_sources.add(partition["source_binding"])
    source_consumers.setdefault(partition["source_binding"], set()).add("partition")
    for key in ["witness_exhaustive", "uniform_over_received_lines", "same_partition_for_all_atoms", "addback_complete"]:
        require(partition[key] is True, f"candidate partition gate failed: {key}")
    owner_order = partition["owner_order"]
    require(isinstance(owner_order, list) and owner_order, "candidate owner order empty")
    require(len(owner_order) <= MAX_OWNER_IDS, "candidate owner order too large")
    require(all(isinstance(owner, str) and 1 <= len(owner) <= 1024 for owner in owner_order), "candidate owner id invalid")
    require(len(owner_order) == len(set(owner_order)), "candidate owner order duplicates")
    require(partition["unresolved_cells"] == [], "candidate has unresolved cells")

    partition_manifest = load_bound_manifest(bindings, paths, partition["source_binding"], "partition")
    require_exact_keys(
        partition_manifest,
        {
            "schema",
            "payload_sha256",
            "row_id",
            "architecture_id",
            "witness_exhaustive",
            "uniform_over_received_lines",
            "same_partition_for_all_atoms",
            "addback_complete",
            "owner_order",
            "unresolved_cells",
            "proof_source_bindings",
        },
        set(),
        "partition manifest",
    )
    require(partition_manifest["schema"] == PARTITION_MANIFEST_SCHEMA, "partition manifest schema mismatch")
    for key in ["row_id", "architecture_id", "witness_exhaustive", "uniform_over_received_lines", "same_partition_for_all_atoms", "addback_complete", "owner_order", "unresolved_cells"]:
        require(
            exact_json_equal(
                partition_manifest[key],
                row_id if key == "row_id" else ACTIVE_ARCH if key == "architecture_id" else partition[key],
            ),
            f"partition manifest mismatch: {key}",
        )
    validate_proof_source_list(
        partition_manifest["proof_source_bindings"], bindings, used_sources, "partition", source_consumers, "partition"
    )

    atoms = candidate["atoms"]
    required = required_atoms(row["kind"])
    require([atom["atom_id"] for atom in atoms] == required, "candidate atom set/order mismatch")
    flattened_owners: list[str] = []
    atom_proof_sources: dict[str, set[str]] = {}
    atom_dependency_architectures: dict[str, set[str]] = {}
    total = 0
    for atom in atoms:
        atom_id = atom["atom_id"]
        require(atom["row_id"] == row_id, f"{atom_id} row mismatch")
        require(atom["architecture_id"] == ACTIVE_ARCH, f"{atom_id} architecture mismatch")
        require(atom["partition_sha256"] == partition_hash, f"{atom_id} partition mismatch")
        require(atom["status"] in {"PAID_BY_THEOREM", "PAID_BY_EXACT_CERTIFICATE"}, f"{atom_id} status not exact")
        require(atom["unit"] == UNIT, f"{atom_id} unit mismatch")
        require(atom["quantifier"] == UNIFORM_QUANTIFIER, f"{atom_id} quantifier mismatch")
        require(atom["unresolved_hypotheses"] == [], f"{atom_id} unresolved hypotheses")
        require(isinstance(atom["source_statement"], str) and atom["source_statement"].strip(), f"{atom_id} source statement empty")
        require(len(atom["source_statement"]) <= 8192, f"{atom_id} source statement too long")
        dependency_architectures = atom["dependency_architecture_ids"]
        require(isinstance(dependency_architectures, list) and dependency_architectures, f"{atom_id} dependency architectures empty")
        require(len(dependency_architectures) == len(set(dependency_architectures)), f"{atom_id} dependency architectures duplicate")
        require(
            all(architecture in {ACTIVE_ARCH, LEGACY_ARCH} for architecture in dependency_architectures),
            f"{atom_id} dependency architecture unknown",
        )
        require(ACTIVE_ARCH in dependency_architectures, f"{atom_id} omits active architecture dependency")
        atom_dependency_architectures[atom_id] = set(dependency_architectures)
        require(len(atom["value"]) <= len(str(row["B_star"])), f"{atom_id}.value exceeds row-sized decimal input")
        value = decimal_int(atom["value"], f"{atom_id}.value")
        total += value
        owners = atom["owner_ids"]
        require(isinstance(owners, list) and owners, f"{atom_id} owner ids empty")
        require(len(owners) <= MAX_OWNER_IDS, f"{atom_id} owner list too large")
        require(all(isinstance(owner, str) and 1 <= len(owner) <= 1024 for owner in owners), f"{atom_id} owner id invalid")
        require(len(owners) == len(set(owners)), f"{atom_id} duplicates an owner")
        flattened_owners.extend(owners)

        source_key = atom["source_binding"]
        used_sources.add(source_key)
        source_consumers.setdefault(source_key, set()).add(atom_id)
        atom_manifest = load_bound_manifest(bindings, paths, source_key, atom_id)
        manifest_required = {
            "schema",
            "payload_sha256",
            "row_id",
            "atom_id",
            "architecture_id",
            "partition_sha256",
            "value",
            "status",
            "unit",
            "quantifier",
            "owner_ids",
            "source_statement",
            "dependency_architecture_ids",
            "proof_source_bindings",
            "unresolved_hypotheses",
        }
        require_exact_keys(atom_manifest, manifest_required, {"q_contract"}, f"{atom_id} manifest")
        require(atom_manifest["schema"] == ATOM_MANIFEST_SCHEMA, f"{atom_id} manifest schema mismatch")
        for key in ["row_id", "atom_id", "architecture_id", "partition_sha256", "value", "status", "unit", "quantifier", "owner_ids", "source_statement", "dependency_architecture_ids", "unresolved_hypotheses"]:
            require(exact_json_equal(atom_manifest[key], atom[key]), f"{atom_id} manifest mismatch: {key}")
        proof_sources = validate_proof_source_list(
            atom_manifest["proof_source_bindings"], bindings, used_sources, atom_id, source_consumers, atom_id
        )
        atom_proof_sources[atom_id] = set(proof_sources)

        if atom_id == "U_Q":
            require(exact_json_equal(atom_manifest.get("q_contract"), atom["q_contract"]), "U_Q manifest q_contract mismatch")
            validate_q_contract(
                atom["q_contract"], atom["value"], row_id, partition_hash, row, bindings, paths, used_sources, source_consumers
            )
        else:
            require("q_contract" not in atom_manifest, f"{atom_id} manifest carries a forbidden q_contract")

    require(flattened_owners == owner_order, "atom-owner assignment does not exactly reproduce first-match owner order")

    kb_path = root / KB995_REL
    kb_digest = sha256_file(kb_path) if kb_path.is_file() else None

    def carries_legacy_payload(path: Path) -> bool:
        raw_text: str
        try:
            raw_text = path.read_text()
            embedded: Any = json.loads(
                raw_text,
                object_pairs_hook=strict_object,
                parse_float=reject_noninteger_number,
                parse_constant=reject_noninteger_number,
            )
        except (RuntimeError, UnicodeDecodeError, json.JSONDecodeError):
            try:
                raw_text
            except UnboundLocalError:
                return False
            return (
                "rs-mca-m1-kb-" in raw_text
                and "rank9" in raw_text
                and "payload_sha256" in raw_text
            )

        parsed_string_bytes = 0

        def contains(value: Any, depth: int = 0) -> bool:
            nonlocal parsed_string_bytes
            if depth > MAX_EMBEDDED_JSON_DEPTH:
                raise RuntimeError("bound source exceeds embedded JSON inspection depth")
            if isinstance(value, dict):
                schema_value = value.get("schema")
                embedded_payload = value.get("payload_sha256")
                if (
                    isinstance(schema_value, str)
                    and schema_value.startswith("rs-mca-m1-kb-")
                    and "rank9" in schema_value
                ):
                    if is_sha256(embedded_payload) and payload_sha256(value) == embedded_payload:
                        return True
                return any(contains(child, depth + 1) for child in value.values())
            if isinstance(value, list):
                return any(contains(child, depth + 1) for child in value)
            if isinstance(value, str):
                stripped = value.lstrip()
                if not stripped.startswith(("{", "[")):
                    return False
                encoded_size = len(value.encode("utf-8"))
                if encoded_size > MAX_EMBEDDED_JSON_BYTES:
                    raise RuntimeError("bound source exceeds embedded JSON string inspection limit")
                parsed_string_bytes += encoded_size
                if parsed_string_bytes > MAX_EMBEDDED_JSON_BYTES:
                    raise RuntimeError("bound source exceeds cumulative embedded JSON inspection limit")
                try:
                    decoded = json.loads(
                        value,
                        object_pairs_hook=strict_object,
                        parse_float=reject_noninteger_number,
                        parse_constant=reject_noninteger_number,
                    )
                except (RuntimeError, json.JSONDecodeError):
                    return False
                return contains(decoded, depth + 1)
            return False

        return contains(embedded)

    legacy_source_keys = {
        key for key in used_sources
        if key == KB995_REL.as_posix()
        or (kb_digest is not None and bindings[key] == kb_digest)
        or carries_legacy_payload(paths[key])
    }
    for source_key in legacy_source_keys:
        consumers = source_consumers.get(source_key, set())
        require(consumers, "legacy source has no tracked consumer")
        require(consumers == {"U_paid"}, "legacy #995 source is consumed outside its mapped U_paid atom")
        require(
            LEGACY_ARCH in atom_dependency_architectures["U_paid"],
            "typed atom adapter hides a detected legacy dependency architecture",
        )
    require(
        all(LEGACY_ARCH not in atom_dependency_architectures[atom_id] for atom_id in atom_dependency_architectures if atom_id != "U_paid"),
        "legacy #995 dependency architecture declared outside U_paid",
    )
    legacy_dependency_declared = any(
        LEGACY_ARCH in architectures for architectures in atom_dependency_architectures.values()
    )
    mapping = candidate["architecture_mapping"]
    if legacy_source_keys or legacy_dependency_declared:
        require(isinstance(mapping, dict), "legacy source lacks a typed architecture mapping")
        require(row_id == "kb_mca", "legacy KoalaBear #995 source cannot map into another deployed row")
        require(mapping["from_architecture"] == LEGACY_ARCH, "legacy mapping source architecture drift")
        require(mapping["to_architecture"] == ACTIVE_ARCH, "legacy mapping target architecture drift")
        require(mapping["row_id"] == row_id, "legacy mapping row drift")
        require(mapping["legacy_payload_sha256"] == EXPECTED_KB995_PAYLOAD, "legacy mapping payload drift")
        require(mapping["target_partition_sha256"] == partition_hash, "legacy mapping target partition drift")
        require(mapping["target_atom_id"] == "U_paid", "legacy #995 mapping must target the active U_paid atom")
        require(len(mapping["legacy_charge_value"]) <= 18, "legacy mapping charge decimal too long")
        require(len(mapping["mapped_charge_value"]) <= 18, "legacy mapped charge decimal too long")
        legacy_charge = decimal_int(mapping["legacy_charge_value"], "legacy mapping charge")
        mapped_charge = decimal_int(mapping["mapped_charge_value"], "legacy mapped charge")
        require(legacy_charge == EXPECTED_KB995_U_PAID, "legacy mapping charge does not equal #995")
        require(mapped_charge == legacy_charge, "legacy mapping changes charge without a separately reviewed coalescing theorem")
        require(mapping["target_atom_charge_includes_mapped_value"] is True, "legacy mapped charge inclusion gate disabled")
        require(decimal_int(atoms[0]["value"], "active U_paid") >= mapped_charge, "active U_paid erases part of the mapped legacy charge")
        require(mapping["unit"] == UNIT and mapping["quantifier"] == UNIFORM_QUANTIFIER, "legacy mapping accounting contract drift")
        require(mapping["uniform_over_received_lines"] is True and mapping["complete_owner_map"] is True, "legacy mapping is not exhaustive")
        require(mapping["unresolved_hypotheses"] == [], "legacy mapping has unresolved hypotheses")
        require(mapping["legacy_source_binding"] in legacy_source_keys, "legacy mapping does not name the used #995 source")
        require(legacy_source_keys == {mapping["legacy_source_binding"]}, "legacy mapping does not cover exactly the detected legacy source set")
        require(mapping["legacy_source_binding"] in atom_proof_sources["U_paid"], "active U_paid adapter does not directly consume the legacy source")
        require(LEGACY_ARCH in atom_dependency_architectures["U_paid"], "active U_paid adapter omits legacy dependency architecture")
        require(mapping["legacy_source_binding"] == KB995_REL.as_posix(), "legacy mapping must bind the canonical #995 certificate")
        require(mapping["active_source_binding"] == ACTIVE_SPINE_REL.as_posix(), "legacy mapping must bind the canonical active spine")
        require(mapping["active_source_binding"] in bindings, "legacy mapping active source absent")
        require(
            bindings[mapping["legacy_source_binding"]] == sha256_file(ROOT / KB995_REL),
            "legacy mapping source is not the compiler-trusted #995 artifact",
        )
        require(
            bindings[mapping["active_source_binding"]] == sha256_file(ROOT / ACTIVE_SPINE_REL),
            "legacy mapping active source is not the compiler-trusted active spine",
        )
        legacy_document = load_json_strict(paths[mapping["legacy_source_binding"]])
        require(legacy_document.get("schema") == EXPECTED_KB995_SCHEMA, "legacy mapping source schema drift")
        verify_embedded_payload(legacy_document, EXPECTED_KB995_PAYLOAD, "legacy mapping source")
        require(
            decimal_int(legacy_document["ledger"]["U_paid_after"], "legacy source U_paid")
            == EXPECTED_KB995_U_PAID,
            "legacy mapping source charge drift",
        )
        legacy_owner_ids = mapping["legacy_owner_ids"]
        mapped_active_owner_ids = mapping["mapped_active_owner_ids"]
        owner_mapping = mapping["owner_mapping"]
        require(isinstance(legacy_owner_ids, list) and legacy_owner_ids, "legacy owner universe empty")
        require(len(legacy_owner_ids) <= MAX_OWNER_IDS, "legacy owner universe too large")
        require(all(isinstance(owner, str) and 1 <= len(owner) <= 1024 for owner in legacy_owner_ids), "legacy owner id invalid")
        require(len(legacy_owner_ids) == len(set(legacy_owner_ids)), "legacy owner universe duplicates")
        require(isinstance(mapped_active_owner_ids, list) and mapped_active_owner_ids, "mapped active owner universe empty")
        require(len(mapped_active_owner_ids) <= MAX_OWNER_IDS, "mapped active owner universe too large")
        require(all(isinstance(owner, str) and 1 <= len(owner) <= 1024 for owner in mapped_active_owner_ids), "mapped active owner id invalid")
        require(len(mapped_active_owner_ids) == len(set(mapped_active_owner_ids)), "mapped active owner universe duplicates")
        require(isinstance(owner_mapping, list) and len(owner_mapping) == len(legacy_owner_ids), "legacy owner map is not source-exhaustive")
        require(len(owner_mapping) <= MAX_OWNER_IDS, "legacy owner map too large")
        mapping_sources: list[str] = []
        mapping_targets: list[str] = []
        for index, record in enumerate(owner_mapping):
            require_exact_keys(record, {"legacy_owner_id", "active_owner_ids"}, set(), f"owner_mapping[{index}]")
            require(isinstance(record["legacy_owner_id"], str) and 1 <= len(record["legacy_owner_id"]) <= 1024, f"owner_mapping[{index}] legacy id invalid")
            targets = record["active_owner_ids"]
            require(isinstance(targets, list) and targets, f"owner_mapping[{index}] active targets empty")
            require(len(targets) <= MAX_OWNER_IDS, f"owner_mapping[{index}] active target list too large")
            require(all(isinstance(owner, str) and 1 <= len(owner) <= 1024 for owner in targets), f"owner_mapping[{index}] active target invalid")
            require(len(targets) == len(set(targets)), f"owner_mapping[{index}] active target duplicates")
            require(len(mapping_targets) + len(targets) <= MAX_OWNER_IDS, "legacy owner map flattened target list too large")
            mapping_sources.append(record["legacy_owner_id"])
            mapping_targets.extend(targets)
        require(mapping_sources == legacy_owner_ids, "legacy owner map source order/universe mismatch")
        require(mapping_targets == mapped_active_owner_ids, "legacy owner map target order/universe mismatch")
        require(len(mapping_targets) == len(set(mapping_targets)), "legacy owner map double-assigns an active owner")
        upaid_owner_order = atoms[0]["owner_ids"]
        upaid_positions = {owner: index for index, owner in enumerate(upaid_owner_order)}
        owner_positions = [upaid_positions.get(owner, -1) for owner in mapped_active_owner_ids]
        require(all(position >= 0 for position in owner_positions), "legacy owner map targets an owner outside active U_paid")
        require(owner_positions == sorted(owner_positions), "legacy owner map violates active first-match chronology")
        require_bound_digest(bindings, mapping["owner_map_source_binding"], mapping["owner_map_sha256"], "legacy owner map")
        used_sources.update({mapping["source_binding"], mapping["legacy_source_binding"], mapping["active_source_binding"], mapping["owner_map_source_binding"]})
        validate_proof_source_list(mapping["proof_source_bindings"], bindings, used_sources, "legacy mapping")
        require(mapping["legacy_source_binding"] in mapping["proof_source_bindings"], "legacy mapping proof omits #995")
        require(mapping["active_source_binding"] in mapping["proof_source_bindings"], "legacy mapping proof omits active architecture")
        mapping_source = mapping["source_binding"]
        require(mapping_source in bindings, "legacy mapping source binding absent")
        require(paths[mapping_source] not in {paths[key] for key in legacy_source_keys}, "#995 cannot self-certify its active mapping")
        require(bindings[mapping_source] not in {bindings[key] for key in legacy_source_keys}, "byte-identical #995 alias cannot self-certify its mapping")
        owner_map_manifest = load_bound_manifest(
            bindings, paths, mapping["owner_map_source_binding"], "architecture owner map"
        )
        require_exact_keys(
            owner_map_manifest,
            {
                "schema",
                "payload_sha256",
                "row_id",
                "from_architecture",
                "to_architecture",
                "legacy_payload_sha256",
                "target_partition_sha256",
                "unit",
                "quantifier",
                "complete_owner_map",
                "owner_order",
                "target_atom_id",
                "legacy_charge_value",
                "mapped_charge_value",
                "target_atom_charge_includes_mapped_value",
                "legacy_owner_ids",
                "mapped_active_owner_ids",
                "owner_mapping",
                "proof_source_bindings",
                "unresolved_hypotheses",
            },
            set(),
            "architecture owner-map manifest",
        )
        require(owner_map_manifest["schema"] == ARCHITECTURE_OWNER_MAP_SCHEMA, "architecture owner-map schema mismatch")
        owner_map_expected = {
            "row_id": row_id,
            "from_architecture": LEGACY_ARCH,
            "to_architecture": ACTIVE_ARCH,
            "legacy_payload_sha256": EXPECTED_KB995_PAYLOAD,
            "target_partition_sha256": partition_hash,
            "unit": UNIT,
            "quantifier": UNIFORM_QUANTIFIER,
            "complete_owner_map": True,
            "owner_order": owner_order,
            "target_atom_id": "U_paid",
            "legacy_charge_value": str(EXPECTED_KB995_U_PAID),
            "mapped_charge_value": str(EXPECTED_KB995_U_PAID),
            "target_atom_charge_includes_mapped_value": True,
            "legacy_owner_ids": legacy_owner_ids,
            "mapped_active_owner_ids": mapped_active_owner_ids,
            "owner_mapping": owner_mapping,
            "unresolved_hypotheses": [],
        }
        for key, expected_value in owner_map_expected.items():
            require(exact_json_equal(owner_map_manifest[key], expected_value), f"architecture owner-map mismatch: {key}")
        validate_proof_source_list(
            owner_map_manifest["proof_source_bindings"], bindings, used_sources, "architecture owner map"
        )
        mapping_manifest = load_bound_manifest(bindings, paths, mapping_source, "architecture mapping")
        manifest_required = {"schema", "payload_sha256"} | (set(mapping) - {"source_binding"})
        require_exact_keys(mapping_manifest, manifest_required, set(), "architecture mapping manifest")
        require(mapping_manifest["schema"] == ARCHITECTURE_MAPPING_SCHEMA, "architecture mapping manifest schema mismatch")
        for key in set(mapping) - {"source_binding"}:
            require(exact_json_equal(mapping_manifest[key], mapping[key]), f"architecture mapping manifest mismatch: {key}")
    else:
        require(mapping is None, "superfluous architecture mapping without a legacy input")

    require(used_sources == set(bindings), "source binding map contains unused or untyped artifacts")
    claim = candidate["claim"]
    require(claim["closed"] is True, "candidate does not claim closure")
    require(len(claim["total_charge"]) <= len(str(row["B_star"])), "claim.total_charge exceeds row-sized decimal input")
    require(len(claim["B_star"]) <= len(str(row["B_star"])), "claim.B_star exceeds row-sized decimal input")
    require(decimal_int(claim["total_charge"], "claim.total_charge") == total, "candidate total is not atom sum")
    require(decimal_int(claim["B_star"], "claim.B_star") == row["B_star"], "candidate B* mismatch")
    require(total <= row["B_star"], "candidate exact sum exceeds B*")
    return {
        "candidate_payload_sha256": candidate["payload_sha256"],
        "row_id": row_id,
        "total_charge": str(total),
        "B_star": str(row["B_star"]),
        "headroom": str(row["B_star"] - total),
        "structural_preflight": STRUCTURAL_PREFLIGHT,
        "closure_certified": False,
        "candidate_eligible_for_active_ledger": False,
        "required_external_gate": "INDEPENDENT_PROOF_REVIEW_AND_EXPLICIT_TRUSTED_SOURCE_REGISTRY_UPDATE",
        "mathematical_source_review_still_required": True,
    }


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def current_mutations() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-bad")),
        ("artifact", lambda d: d.__setitem__("artifact_kind", "WRONG")),
        ("status", lambda d: d.__setitem__("status", "SAFE")),
        ("base", lambda d: d["stack"].__setitem__("base_commit", "0" * 40)),
        ("active-arch", lambda d: d["stack"].__setitem__("active_architecture_id", LEGACY_ARCH)),
        ("unit", lambda d: d["active_ledger_contract"].__setitem__("unit", "SUPPORTS")),
        ("quantifier", lambda d: d["active_ledger_contract"].__setitem__("quantifier", "ONE_SAMPLED_LINE")),
        ("partition-gate", lambda d: d["active_ledger_contract"].__setitem__("one_partition_required", False)),
        ("row-order", lambda d: d["rows"].reverse()),
        ("kb-a", lambda d: d["rows"][0]["parameters"].__setitem__("a_plus", 1_116_047)),
        ("kb-kind", lambda d: d["rows"][0].__setitem__("object_kind", "LIST")),
        ("m31-p", lambda d: d["rows"][2]["parameters"].__setitem__("p", P_KB)),
        ("average", lambda d: d["rows"][3]["exact_calibration"].__setitem__("average_ceiling", "1993677")),
        ("B-star", lambda d: d["rows"][2]["exact_calibration"].__setitem__("B_star", "16777216")),
        ("Q-cap", lambda d: d["rows"][1]["exact_calibration"].__setitem__("full_budget_Q_multiplier_floor", 4_226_237)),
        ("float-gate", lambda d: d["rows"][0]["exact_calibration"].__setitem__("all_gates_exact_integer", False)),
        ("invent-Q", lambda d: d["rows"][0]["q_contract"].__setitem__("upper_integer", "0")),
        ("invent-Q-status", lambda d: d["rows"][0]["q_contract"].__setitem__("status", "PAID_BY_THEOREM")),
        ("mix-ledger", lambda d: d["rows"][0]["q_contract"].__setitem__("separate_ledger_generations_may_be_mixed", True)),
        ("close-null", lambda d: d["rows"][0]["active_completion"].__setitem__("closed", True)),
        ("erase-blockers", lambda d: d["rows"][1]["active_completion"].__setitem__("unresolved_cells", [])),
        ("invent-partition", lambda d: d["rows"][2]["active_completion"].__setitem__("witness_exhaustive_partition_sha256", "0" * 64)),
        ("invent-total", lambda d: d["rows"][3]["active_completion"].__setitem__("total_charge", "0")),
        ("atom-swap", lambda d: d["rows"][0]["active_completion"].__setitem__("required_atoms", ["U_paid", "U_Q", "U_list_int", "U_new"])),
        ("extension-max", lambda d: d["rows"][2]["direct_extension_Delta_p_power_e_route_cut"].__setitem__("max_e_Y", 1)),
        ("extension-bank", lambda d: d["rows"][1]["direct_extension_Delta_p_power_e_route_cut"].__setitem__("capacities_are_allocations", True)),
        ("legacy-charge", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("U_paid", str(EXPECTED_KB995_U_PAID + 1))),
        ("legacy-map", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("active_architecture_mapping", {"fake": True})),
        ("legacy-consume", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("consumed_by_active_ledger", True)),
        ("legacy-packet-scope", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("packet_scope", "ALL_LEGACY_OWNERS")),
        ("legacy-inherited-scope", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("inherited_ledger_scope", "LOCAL_ONLY")),
        ("legacy-pair-scope", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("received_pair_quantifier", "ONE_SAMPLED_PAIR")),
        ("legacy-translation-scope", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("translation_scope", "ONE_SPECIAL_TRANSLATION")),
        ("legacy-fixed-pair-cut", lambda d: d["rows"][0]["legacy_stack_local_progress"].__setitem__("fixed_pair_scope_alone_is_not_route_cut", False)),
        ("legacy-transplant", lambda d: d["rows"][2].__setitem__("legacy_stack_local_progress", copy.deepcopy(d["rows"][0]["legacy_stack_local_progress"]))),
        ("route-closed", lambda d: d["architecture_route_cut"].__setitem__("active_rows_closed", ["kb_mca"])),
        ("route-map", lambda d: d["architecture_route_cut"].__setitem__("legacy_to_active_mapping_certificate", "fake")),
        ("route-current", lambda d: d["architecture_route_cut"].__setitem__("current_hypotheses_can_close_any_row", True)),
        ("route-counterexample", lambda d: d["scope_guards"].__setitem__("scalar_route_cut_promoted_to_counterexample", True)),
        ("scope-close", lambda d: d["scope_guards"].__setitem__("mathematical_row_closure_claimed", True)),
        ("superseded-ext", lambda d: d["extension_route_cut"].__setitem__("superseded_multiplier_interpretation_rejected", False)),
        ("hide-stale-ext", lambda d: d["extension_route_cut"].__setitem__("correction_full_python_acceptance_status", "PASS")),
        ("extension-source", lambda d: d["extension_route_cut"].__setitem__("current_dimension_degree_source", "archived/cs25_cap_v12.tex")),
        ("candidate-schema-gate", lambda d: d["candidate_interface"].__setitem__("runtime_schema_shape_enforced", False)),
        ("candidate-path-gate", lambda d: d["candidate_interface"].__setitem__("canonical_contained_source_paths_required", False)),
        ("candidate-adapter-gate", lambda d: d["candidate_interface"].__setitem__("typed_partition_atom_q_and_mapping_adapters_required", False)),
        ("candidate-owner-gate", lambda d: d["candidate_interface"].__setitem__("exact_owner_order_coverage_required", False)),
        ("candidate-identity-gate", lambda d: d["candidate_interface"].__setitem__("candidate_payload_identity_required", False)),
        ("candidate-preflight-scope", lambda d: d["candidate_interface"].__setitem__("candidate_audit_is_structural_preflight_only", False)),
        ("candidate-closing-authority", lambda d: d["candidate_interface"].__setitem__("candidate_audit_can_close_row", True)),
        ("candidate-review-registry-gate", lambda d: d["candidate_interface"].__setitem__("reviewed_source_registry_entry_required_for_banking", False)),
        ("candidate-invent-registry", lambda d: d["candidate_interface"].__setitem__("trusted_review_registry_entries", 1)),
        ("candidate-proof-overclaim", lambda d: d["candidate_interface"].__setitem__("mechanical_validation_replaces_proof_review", True)),
        ("candidate-legacy-mapping-gate", lambda d: d["candidate_interface"].__setitem__("recognized_legacy_input_requires_explicit_architecture_mapping", False)),
        ("candidate-provenance-overclaim", lambda d: d["candidate_interface"].__setitem__("provenance_transform_detection_complete", True)),
        ("Q-inventory", lambda d: d["q_inventory"]["deployed_exact_U_Q_by_row"].__setitem__("m31_list", "2029705")),
        ("source-hash", lambda d: d["source_bindings"].__setitem__(ACTIVE_SPINE_REL.as_posix(), "0" * 64)),
        ("source-drop", lambda d: d["source_bindings"].pop(ACTIVE_SPINE_REL.as_posix())),
        ("payload", lambda d: d.__setitem__("payload_sha256", "f" * 64)),
    ]


def write_payload_manifest(path: Path, value: dict[str, Any]) -> None:
    value = copy.deepcopy(value)
    value["payload_sha256"] = ""
    value["payload_sha256"] = payload_sha256(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def build_typed_candidate_fixture(root: Path) -> dict[str, Any]:
    """Build a structurally valid, explicitly non-mathematical temp fixture."""
    fixture_root = root / "experimental/typed-candidate-fixture"
    fixture_root.mkdir(parents=True, exist_ok=True)
    common_rel = "experimental/typed-candidate-fixture/proof-source.md"
    (root / common_rel).write_text("TEST-ONLY typed-adapter fixture; not a theorem.\n")
    component_names = ["evaluation-domain", "priority-map", "residual", "target-map", "coalescing", "joint-max"]
    component_rels = {
        name: f"experimental/typed-candidate-fixture/{name}.json" for name in component_names
    }

    owner_order = [f"owner-{i}" for i in range(4)]
    partition_rel = "experimental/typed-candidate-fixture/partition.json"
    write_payload_manifest(
        root / partition_rel,
        {
            "schema": PARTITION_MANIFEST_SCHEMA,
            "row_id": "kb_mca",
            "architecture_id": ACTIVE_ARCH,
            "witness_exhaustive": True,
            "uniform_over_received_lines": True,
            "same_partition_for_all_atoms": True,
            "addback_complete": True,
            "owner_order": owner_order,
            "unresolved_cells": [],
            "proof_source_bindings": [common_rel],
        },
    )
    partition_hash = sha256_file(root / partition_rel)
    component_claims = {
        "evaluation-domain": {"evaluation_domain_frozen": True},
        "priority-map": {"first_match_priority_frozen": True},
        "residual": {"residual_predicate_frozen": True},
        "target-map": {"target_map_frozen": True},
        "coalescing": {"support_to_parameter_coalescing_exhaustive": True},
    }
    component_kinds = {
        "evaluation-domain": "EVALUATION_DOMAIN",
        "priority-map": "PRIORITY_MAP",
        "residual": "RESIDUAL_PREDICATE",
        "target-map": "TARGET_MAP",
        "coalescing": "SUPPORT_TO_PARAMETER_COALESCING",
        "joint-max": "JOINT_MAXIMUM",
    }
    for name in component_names:
        if name == "joint-max":
            continue
        write_payload_manifest(
            root / component_rels[name],
            {
                "schema": Q_COMPONENT_MANIFEST_SCHEMA,
                "component_kind": component_kinds[name],
                "row_id": "kb_mca",
                "architecture_id": ACTIVE_ARCH,
                "partition_sha256": partition_hash,
                "n": N,
                "K": ROWS[0]["K"],
                "a_plus": ROWS[0]["a_plus"],
                "w": ROWS[0]["w"],
                "p": ROWS[0]["p"],
                "claims": component_claims[name],
                "proof_source_bindings": [common_rel],
                "unresolved_hypotheses": [],
            },
        )
    component_claims["joint-max"] = {
        "evaluation_domain_sha256": sha256_file(root / component_rels["evaluation-domain"]),
        "priority_map_sha256": sha256_file(root / component_rels["priority-map"]),
        "residual_predicate_sha256": sha256_file(root / component_rels["residual"]),
        "target_map_sha256": sha256_file(root / component_rels["target-map"]),
        "support_to_parameter_coalescing_sha256": sha256_file(root / component_rels["coalescing"]),
        "support_orientation": "AGREEMENT",
        "support_transport_sha256": None,
        "normalization": "EFFECTIVE_IMAGE",
        "full_image_certificate_sha256": None,
        "effective_image_cardinality": "1",
        "aggregation_mode": "JOINT_MAX_ON_FROZEN_RESIDUAL",
        "separate_suprema_forbidden": True,
        "upper_integer": "0",
    }
    write_payload_manifest(
        root / component_rels["joint-max"],
        {
            "schema": Q_COMPONENT_MANIFEST_SCHEMA,
            "component_kind": component_kinds["joint-max"],
            "row_id": "kb_mca",
            "architecture_id": ACTIVE_ARCH,
            "partition_sha256": partition_hash,
            "n": N,
            "K": ROWS[0]["K"],
            "a_plus": ROWS[0]["a_plus"],
            "w": ROWS[0]["w"],
            "p": ROWS[0]["p"],
            "claims": component_claims["joint-max"],
            "proof_source_bindings": [common_rel],
            "unresolved_hypotheses": [],
        },
    )
    q_contract = {
        "ledger_generation_id": ACTIVE_ARCH,
        "n": N,
        "K": ROWS[0]["K"],
        "a_plus": ROWS[0]["a_plus"],
        "w": ROWS[0]["w"],
        "p": ROWS[0]["p"],
        "evaluation_domain_source_binding": component_rels["evaluation-domain"],
        "evaluation_domain_sha256": sha256_file(root / component_rels["evaluation-domain"]),
        "priority_map_source_binding": component_rels["priority-map"],
        "priority_map_sha256": sha256_file(root / component_rels["priority-map"]),
        "residual_predicate_source_binding": component_rels["residual"],
        "residual_predicate_sha256": sha256_file(root / component_rels["residual"]),
        "target_map_source_binding": component_rels["target-map"],
        "target_map_sha256": sha256_file(root / component_rels["target-map"]),
        "support_to_parameter_coalescing_source_binding": component_rels["coalescing"],
        "support_to_parameter_coalescing_sha256": sha256_file(root / component_rels["coalescing"]),
        "support_orientation": "AGREEMENT",
        "support_transport_binding": None,
        "support_transport_sha256": None,
        "normalization": "EFFECTIVE_IMAGE",
        "full_image_certificate_binding": None,
        "full_image_certificate_sha256": None,
        "effective_image_cardinality": "1",
        "aggregation_mode": "JOINT_MAX_ON_FROZEN_RESIDUAL",
        "separate_suprema_forbidden": True,
        "joint_max_certificate_binding": component_rels["joint-max"],
        "joint_max_certificate_sha256": sha256_file(root / component_rels["joint-max"]),
        "upper_integer": "0",
    }
    atoms: list[dict[str, Any]] = []
    atom_rels: list[str] = []
    for index, atom_id in enumerate(required_atoms("MCA")):
        rel = f"experimental/typed-candidate-fixture/{atom_id}.json"
        atom_rels.append(rel)
        atom: dict[str, Any] = {
            "atom_id": atom_id,
            "row_id": "kb_mca",
            "architecture_id": ACTIVE_ARCH,
            "partition_sha256": partition_hash,
            "value": "0",
            "status": "PAID_BY_EXACT_CERTIFICATE",
            "unit": UNIT,
            "quantifier": UNIFORM_QUANTIFIER,
            "owner_ids": [owner_order[index]],
            "source_binding": rel,
            "source_statement": "TEST-ONLY typed adapter; independent mathematical review still required.",
            "dependency_architecture_ids": [ACTIVE_ARCH],
            "unresolved_hypotheses": [],
        }
        manifest = {key: value for key, value in atom.items() if key != "source_binding"}
        manifest.update({"schema": ATOM_MANIFEST_SCHEMA, "proof_source_bindings": [common_rel]})
        if atom_id == "U_Q":
            atom["q_contract"] = copy.deepcopy(q_contract)
            manifest["q_contract"] = copy.deepcopy(q_contract)
        write_payload_manifest(root / rel, manifest)
        atoms.append(atom)

    source_rels = [common_rel, partition_rel, *atom_rels, *component_rels.values()]
    source_map = {rel: sha256_file(root / rel) for rel in source_rels}
    candidate = {
        "schema": CANDIDATE_SCHEMA,
        "payload_sha256": "",
        "row_id": "kb_mca",
        "architecture_id": ACTIVE_ARCH,
        "row_parameters": {
            "n": N,
            "K": ROWS[0]["K"],
            "a_plus": ROWS[0]["a_plus"],
            "w": ROWS[0]["w"],
            "p": ROWS[0]["p"],
            "object_kind": "MCA",
        },
        "partition": {
            "partition_sha256": partition_hash,
            "source_binding": partition_rel,
            "witness_exhaustive": True,
            "uniform_over_received_lines": True,
            "same_partition_for_all_atoms": True,
            "addback_complete": True,
            "owner_order": owner_order,
            "unresolved_cells": [],
        },
        "atoms": atoms,
        "claim": {"closed": True, "total_charge": "0", "B_star": str(ROWS[0]["B_star"])},
        "source_bindings": source_map,
        "architecture_mapping": None,
    }
    candidate["payload_sha256"] = payload_sha256(candidate)
    return candidate


def add_valid_legacy_mapping_fixture(root: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(candidate)
    legacy_rel = KB995_REL.as_posix()
    active_rel = ACTIVE_SPINE_REL.as_posix()
    (root / legacy_rel).parent.mkdir(parents=True, exist_ok=True)
    (root / active_rel).parent.mkdir(parents=True, exist_ok=True)
    (root / legacy_rel).write_bytes((ROOT / KB995_REL).read_bytes())
    (root / active_rel).write_bytes((ROOT / ACTIVE_SPINE_REL).read_bytes())
    value["source_bindings"][legacy_rel] = sha256_file(root / legacy_rel)
    value["source_bindings"][active_rel] = sha256_file(root / active_rel)

    value["atoms"][0]["value"] = str(EXPECTED_KB995_U_PAID)
    value["claim"]["total_charge"] = str(EXPECTED_KB995_U_PAID)
    upaid_path = root / value["atoms"][0]["source_binding"]
    upaid_manifest = load_json_strict(upaid_path)
    upaid_manifest["value"] = str(EXPECTED_KB995_U_PAID)
    upaid_manifest["proof_source_bindings"].append(legacy_rel)
    upaid_manifest["dependency_architecture_ids"] = [ACTIVE_ARCH, LEGACY_ARCH]
    write_payload_manifest(upaid_path, upaid_manifest)
    value["atoms"][0]["dependency_architecture_ids"] = [ACTIVE_ARCH, LEGACY_ARCH]
    value["source_bindings"][value["atoms"][0]["source_binding"]] = sha256_file(upaid_path)

    owner_map_rel = "experimental/typed-candidate-fixture/architecture-owner-map.json"
    mapping_rel = "experimental/typed-candidate-fixture/architecture-mapping.json"
    legacy_owner_ids = ["legacy-owner-0"]
    mapped_active_owner_ids = ["owner-0"]
    owner_mapping = [{"legacy_owner_id": "legacy-owner-0", "active_owner_ids": ["owner-0"]}]
    mapping_core = {
        "from_architecture": LEGACY_ARCH,
        "to_architecture": ACTIVE_ARCH,
        "row_id": "kb_mca",
        "legacy_source_binding": legacy_rel,
        "active_source_binding": active_rel,
        "legacy_payload_sha256": EXPECTED_KB995_PAYLOAD,
        "target_partition_sha256": value["partition"]["partition_sha256"],
        "owner_map_source_binding": owner_map_rel,
        "owner_map_sha256": "",
        "target_atom_id": "U_paid",
        "legacy_charge_value": str(EXPECTED_KB995_U_PAID),
        "mapped_charge_value": str(EXPECTED_KB995_U_PAID),
        "target_atom_charge_includes_mapped_value": True,
        "legacy_owner_ids": legacy_owner_ids,
        "mapped_active_owner_ids": mapped_active_owner_ids,
        "owner_mapping": owner_mapping,
        "unit": UNIT,
        "quantifier": UNIFORM_QUANTIFIER,
        "uniform_over_received_lines": True,
        "complete_owner_map": True,
        "proof_source_bindings": [legacy_rel, active_rel, owner_map_rel],
        "unresolved_hypotheses": [],
    }
    write_payload_manifest(
        root / owner_map_rel,
        {
            "schema": ARCHITECTURE_OWNER_MAP_SCHEMA,
            "row_id": "kb_mca",
            "from_architecture": LEGACY_ARCH,
            "to_architecture": ACTIVE_ARCH,
            "legacy_payload_sha256": EXPECTED_KB995_PAYLOAD,
            "target_partition_sha256": value["partition"]["partition_sha256"],
            "unit": UNIT,
            "quantifier": UNIFORM_QUANTIFIER,
            "complete_owner_map": True,
            "owner_order": value["partition"]["owner_order"],
            "target_atom_id": "U_paid",
            "legacy_charge_value": str(EXPECTED_KB995_U_PAID),
            "mapped_charge_value": str(EXPECTED_KB995_U_PAID),
            "target_atom_charge_includes_mapped_value": True,
            "legacy_owner_ids": legacy_owner_ids,
            "mapped_active_owner_ids": mapped_active_owner_ids,
            "owner_mapping": owner_mapping,
            "proof_source_bindings": [legacy_rel, active_rel],
            "unresolved_hypotheses": [],
        },
    )
    mapping_core["owner_map_sha256"] = sha256_file(root / owner_map_rel)
    mapping = {"source_binding": mapping_rel, **mapping_core}
    write_payload_manifest(root / mapping_rel, {"schema": ARCHITECTURE_MAPPING_SCHEMA, **mapping_core})
    value["source_bindings"][owner_map_rel] = sha256_file(root / owner_map_rel)
    value["source_bindings"][mapping_rel] = sha256_file(root / mapping_rel)
    value["architecture_mapping"] = mapping
    value["payload_sha256"] = payload_sha256(value)
    return value


def add_reformatted_legacy_laundering_fixture(
    root: Path,
    candidate: dict[str, Any],
    legacy_source: Path = KB995_REL,
    suffix: str = ".txt",
    envelope: bool = False,
    stringify: bool = False,
    nesting_depth: int = 0,
    string_padding_bytes: int = 0,
    markdown_envelope: bool = False,
) -> dict[str, Any]:
    value = copy.deepcopy(candidate)
    laundered_rel = f"experimental/typed-candidate-fixture/reformatted-legacy{suffix}"
    legacy_object = load_json_strict(ROOT / legacy_source)
    wrapped_object: Any = legacy_object
    for _ in range(nesting_depth):
        wrapped_object = {"provenance_wrapper": wrapped_object}
    if stringify:
        string_object: Any = wrapped_object
        if string_padding_bytes:
            string_object = {
                "provenance_wrapper": wrapped_object,
                "padding": "x" * string_padding_bytes,
            }
        wrapped_payload = json.dumps(string_object, sort_keys=True)
    else:
        wrapped_payload = wrapped_object
    wrapped: Any = {"provenance_wrapper": wrapped_payload} if envelope else wrapped_payload
    if markdown_envelope:
        rendered = "# Imported proof\n\n```json\n" + json.dumps(wrapped, sort_keys=True) + "\n```\n"
    else:
        rendered = json.dumps(wrapped, sort_keys=True) + "\n"
    (root / laundered_rel).write_text(rendered)
    value["source_bindings"][laundered_rel] = sha256_file(root / laundered_rel)
    value["atoms"][0]["value"] = str(EXPECTED_KB995_U_PAID)
    value["claim"]["total_charge"] = str(EXPECTED_KB995_U_PAID)
    upaid_path = root / value["atoms"][0]["source_binding"]
    upaid_manifest = load_json_strict(upaid_path)
    upaid_manifest["value"] = str(EXPECTED_KB995_U_PAID)
    upaid_manifest["proof_source_bindings"].append(laundered_rel)
    write_payload_manifest(upaid_path, upaid_manifest)
    value["source_bindings"][value["atoms"][0]["source_binding"]] = sha256_file(upaid_path)
    value["payload_sha256"] = payload_sha256(value)
    return value


def invalid_candidate_cases(base: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Callable[[dict[str, Any]], None], refresh_payload: bool = True) -> None:
        value = copy.deepcopy(base)
        mutate(value)
        if refresh_payload:
            value["payload_sha256"] = payload_sha256(value)
        cases.append((name, value))

    add("candidate-null-Q", lambda d: d["atoms"][1].__setitem__("value", None))
    add("candidate-stale-arch", lambda d: d.__setitem__("architecture_id", LEGACY_ARCH))
    add("candidate-row-swap", lambda d: d["atoms"][1].__setitem__("row_id", "m31_list"))
    add("candidate-row-parameters", lambda d: d["row_parameters"].__setitem__("K", K_BASE))
    add("candidate-partition-swap", lambda d: d["atoms"][2].__setitem__("partition_sha256", "9" * 64))
    add("candidate-unbound-partition", lambda d: d["partition"].__setitem__("partition_sha256", "9" * 64))
    add("candidate-sampled-line", lambda d: d["atoms"][0].__setitem__("quantifier", "ONE_SAMPLED_LINE"))
    add("candidate-duplicate-owner", lambda d: d["atoms"][2].__setitem__("owner_ids", ["owner-0"]))
    add("candidate-numeric-owner", lambda d: d["atoms"][2].__setitem__("owner_ids", [2]))
    add("candidate-unrelated-owner-order", lambda d: d["partition"].__setitem__("owner_order", ["declared-only"]))
    add("candidate-unresolved", lambda d: d["partition"].__setitem__("unresolved_cells", ["primitive"]))
    add("candidate-separate-sup", lambda d: d["atoms"][1]["q_contract"].__setitem__("aggregation_mode", "SEPARATE_SUPREMA"))
    add("candidate-separate-guard", lambda d: d["atoms"][1]["q_contract"].__setitem__("separate_suprema_forbidden", False))
    add("candidate-unbound-Q-digest", lambda d: d["atoms"][1]["q_contract"].__setitem__("priority_map_sha256", "2" * 64))
    add("candidate-ambient-no-full-image", lambda d: d["atoms"][1]["q_contract"].__setitem__("normalization", "AMBIENT_WITH_FULL_IMAGE_CERTIFICATE"))
    add("candidate-complement-no-transport", lambda d: d["atoms"][1]["q_contract"].__setitem__("support_orientation", "COMPLEMENT_WITH_PROVED_TRANSPORT"))
    add("candidate-Q-upper-drift", lambda d: d["atoms"][1]["q_contract"].__setitem__("upper_integer", "1"))
    add("candidate-target-as-upper", lambda d: d["atoms"][1].__setitem__("status", "TARGET_ONLY"))
    add("candidate-total-drift", lambda d: d["claim"].__setitem__("total_charge", "1"))
    add("candidate-budget-drift", lambda d: d["claim"].__setitem__("B_star", str(ROWS[0]["B_star"] + 1)))
    add("candidate-oversized-budget-decimal", lambda d: d["claim"].__setitem__("B_star", "9" * 19))
    add("candidate-unicode-zero", lambda d: d["atoms"][0].__setitem__("value", "٠"))
    add("candidate-oversized-atom-decimal", lambda d: d["atoms"][0].__setitem__("value", "9" * (len(str(ROWS[0]["B_star"])) + 1)))
    add("candidate-oversized-image-decimal", lambda d: d["atoms"][1]["q_contract"].__setitem__("effective_image_cardinality", "1" * 11))
    add("candidate-extra-property", lambda d: d.__setitem__("schema_bypass", True))
    add("candidate-shallow-mapping", lambda d: d.__setitem__("architecture_mapping", {"from_architecture": LEGACY_ARCH}))
    first_source = next(iter(base["source_bindings"]))
    alias = first_source.rsplit("/", 1)[0] + "/./" + first_source.rsplit("/", 1)[1]
    add("candidate-source-alias", lambda d: d["source_bindings"].__setitem__(alias, d["source_bindings"][first_source]))
    add("candidate-hidden-source", lambda d: d["source_bindings"].__setitem__(".git/config", "0" * 64))
    add("candidate-unused-source", lambda d: d["source_bindings"].__setitem__("experimental/typed-candidate-fixture/unused.md", "0" * 64))
    add("candidate-payload", lambda d: d.__setitem__("payload_sha256", "f" * 64), refresh_payload=False)
    return cases


def mutate_typed_q_component_fixture(
    root: Path,
    candidate: dict[str, Any],
    component_name: str,
    mutate: Callable[[dict[str, Any]], None],
    preserve_bad_joint_claim: bool = False,
) -> dict[str, Any]:
    value = copy.deepcopy(candidate)
    q = value["atoms"][1]["q_contract"]
    field_by_name = {
        "evaluation-domain": ("evaluation_domain_source_binding", "evaluation_domain_sha256"),
        "priority-map": ("priority_map_source_binding", "priority_map_sha256"),
        "residual": ("residual_predicate_source_binding", "residual_predicate_sha256"),
        "target-map": ("target_map_source_binding", "target_map_sha256"),
        "coalescing": ("support_to_parameter_coalescing_source_binding", "support_to_parameter_coalescing_sha256"),
        "joint-max": ("joint_max_certificate_binding", "joint_max_certificate_sha256"),
    }
    source_field, digest_field = field_by_name[component_name]
    component_path = root / q[source_field]
    manifest = load_json_strict(component_path)
    mutate(manifest)
    write_payload_manifest(component_path, manifest)
    new_digest = sha256_file(component_path)
    q[digest_field] = new_digest
    value["source_bindings"][q[source_field]] = new_digest

    if component_name != "joint-max":
        joint_path = root / q["joint_max_certificate_binding"]
        joint = load_json_strict(joint_path)
        joint_digest_key = {
            "evaluation-domain": "evaluation_domain_sha256",
            "priority-map": "priority_map_sha256",
            "residual": "residual_predicate_sha256",
            "target-map": "target_map_sha256",
            "coalescing": "support_to_parameter_coalescing_sha256",
        }[component_name]
        joint["claims"][joint_digest_key] = new_digest
        write_payload_manifest(joint_path, joint)
        q["joint_max_certificate_sha256"] = sha256_file(joint_path)
        value["source_bindings"][q["joint_max_certificate_binding"]] = q["joint_max_certificate_sha256"]
    elif not preserve_bad_joint_claim:
        raise RuntimeError("joint-max mutation must explicitly preserve its bad cross-binding claim")

    atom_path = root / value["atoms"][1]["source_binding"]
    atom_manifest = load_json_strict(atom_path)
    atom_manifest["q_contract"] = copy.deepcopy(q)
    write_payload_manifest(atom_path, atom_manifest)
    value["source_bindings"][value["atoms"][1]["source_binding"]] = sha256_file(atom_path)
    value["payload_sha256"] = payload_sha256(value)
    return value


def tamper_selftest() -> int:
    expected = build_certificate()
    rejected = 0
    total = 0
    for name, mutate in current_mutations():
        total += 1
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        if name != "payload":
            candidate["payload_sha256"] = payload_sha256(candidate)
        try:
            validate_canonical(candidate, expected)
        except RuntimeError:
            rejected += 1
        else:
            print(f"[FAIL] mutation survived: {name}")

    with tempfile.TemporaryDirectory(prefix="four-row-typed-candidate-") as tmp:
        fixture_root = Path(tmp).resolve()
        valid_candidate = build_typed_candidate_fixture(fixture_root)
        positive_result = audit_closure_candidate(valid_candidate, fixture_root)
        require(
            positive_result["structural_preflight"] == STRUCTURAL_PREFLIGHT
            and positive_result["closure_certified"] is False
            and positive_result["candidate_eligible_for_active_ledger"] is False,
            "typed candidate preflight gained closing authority",
        )
        print("[PASS] typed candidate positive control")
        for name, candidate in invalid_candidate_cases(valid_candidate):
            total += 1
            try:
                audit_closure_candidate(candidate, fixture_root)
            except (RuntimeError, KeyError, TypeError, ValueError):
                rejected += 1
            else:
                print(f"[FAIL] invalid completion candidate survived: {name}")

        hardlink_candidate = copy.deepcopy(valid_candidate)
        hardlink_rel = "experimental/typed-candidate-fixture/hardlinked-proof-source.md"
        os.link(
            fixture_root / "experimental/typed-candidate-fixture/proof-source.md",
            fixture_root / hardlink_rel,
        )
        hardlink_candidate["source_bindings"][hardlink_rel] = sha256_file(fixture_root / hardlink_rel)
        hardlink_candidate["payload_sha256"] = payload_sha256(hardlink_candidate)
        total += 1
        try:
            audit_closure_candidate(hardlink_candidate, fixture_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] hardlinked duplicate source survived")

        legacy_root = (fixture_root / "legacy-positive").resolve()
        legacy_root.mkdir()
        legacy_candidate = add_valid_legacy_mapping_fixture(
            legacy_root, build_typed_candidate_fixture(legacy_root)
        )
        legacy_positive_result = audit_closure_candidate(legacy_candidate, legacy_root)
        require(
            legacy_positive_result["structural_preflight"] == STRUCTURAL_PREFLIGHT
            and legacy_positive_result["closure_certified"] is False,
            "typed legacy preflight gained closing authority",
        )
        print("[PASS] typed legacy-mapping positive control")
        legacy_mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            (
                "legacy-mapping-self-certifies",
                lambda d: d["architecture_mapping"].__setitem__("source_binding", KB995_REL.as_posix()),
            ),
            (
                "legacy-owner-domain-incomplete",
                lambda d: d["architecture_mapping"].__setitem__("owner_mapping", []),
            ),
            (
                "legacy-active-target-undeclared",
                lambda d: d["architecture_mapping"]["owner_mapping"][0].__setitem__(
                    "active_owner_ids", ["undeclared-owner"]
                ),
            ),
            (
                "legacy-charge-oversized-decimal",
                lambda d: d["architecture_mapping"].__setitem__("legacy_charge_value", "9" * 19),
            ),
            (
                "legacy-mapped-charge-oversized-decimal",
                lambda d: d["architecture_mapping"].__setitem__("mapped_charge_value", "9" * 19),
            ),
        ]
        for name, mutate in legacy_mutations:
            tampered = copy.deepcopy(legacy_candidate)
            mutate(tampered)
            tampered["payload_sha256"] = payload_sha256(tampered)
            total += 1
            try:
                audit_closure_candidate(tampered, legacy_root)
            except (RuntimeError, KeyError, TypeError, ValueError):
                rejected += 1
            else:
                print(f"[FAIL] invalid legacy mapping survived: {name}")

        cross_atom_root = (fixture_root / "legacy-cross-atom").resolve()
        cross_atom_root.mkdir()
        cross_atom_candidate = add_valid_legacy_mapping_fixture(
            cross_atom_root, build_typed_candidate_fixture(cross_atom_root)
        )
        cross_q = cross_atom_candidate["atoms"][1]
        cross_q["dependency_architecture_ids"] = [ACTIVE_ARCH, LEGACY_ARCH]
        cross_q_path = cross_atom_root / cross_q["source_binding"]
        cross_q_manifest = load_json_strict(cross_q_path)
        cross_q_manifest["dependency_architecture_ids"] = [ACTIVE_ARCH, LEGACY_ARCH]
        cross_q_manifest["proof_source_bindings"].append(KB995_REL.as_posix())
        write_payload_manifest(cross_q_path, cross_q_manifest)
        cross_atom_candidate["source_bindings"][cross_q["source_binding"]] = sha256_file(cross_q_path)
        cross_atom_candidate["payload_sha256"] = payload_sha256(cross_atom_candidate)
        total += 1
        try:
            audit_closure_candidate(cross_atom_candidate, cross_atom_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] legacy #995 source consumed by an unmapped atom")

        extra_legacy_root = (fixture_root / "legacy-extra-predecessor").resolve()
        extra_legacy_root.mkdir()
        extra_legacy_candidate = add_valid_legacy_mapping_fixture(
            extra_legacy_root, build_typed_candidate_fixture(extra_legacy_root)
        )
        extra_rel = KB994_REL.as_posix()
        (extra_legacy_root / extra_rel).parent.mkdir(parents=True, exist_ok=True)
        (extra_legacy_root / extra_rel).write_bytes((ROOT / KB994_REL).read_bytes())
        extra_legacy_candidate["source_bindings"][extra_rel] = sha256_file(extra_legacy_root / extra_rel)
        extra_upaid_path = extra_legacy_root / extra_legacy_candidate["atoms"][0]["source_binding"]
        extra_upaid_manifest = load_json_strict(extra_upaid_path)
        extra_upaid_manifest["proof_source_bindings"].append(extra_rel)
        write_payload_manifest(extra_upaid_path, extra_upaid_manifest)
        extra_legacy_candidate["source_bindings"][extra_legacy_candidate["atoms"][0]["source_binding"]] = sha256_file(extra_upaid_path)
        extra_legacy_candidate["payload_sha256"] = payload_sha256(extra_legacy_candidate)
        total += 1
        try:
            audit_closure_candidate(extra_legacy_candidate, extra_legacy_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] extra unmapped legacy predecessor source survived")

        legacy_payload_drift_root = (fixture_root / "legacy-source-payload-drift").resolve()
        legacy_payload_drift_root.mkdir()
        legacy_payload_drift_candidate = add_valid_legacy_mapping_fixture(
            legacy_payload_drift_root, build_typed_candidate_fixture(legacy_payload_drift_root)
        )
        drift_legacy_path = legacy_payload_drift_root / KB995_REL
        drift_legacy_document = load_json_strict(drift_legacy_path)
        drift_legacy_document["ledger"]["U_paid_after"] = "1"
        drift_legacy_document["payload_sha256"] = payload_sha256(drift_legacy_document)
        drift_legacy_path.write_text(json.dumps(drift_legacy_document, indent=2, sort_keys=True) + "\n")
        legacy_payload_drift_candidate["source_bindings"][KB995_REL.as_posix()] = sha256_file(drift_legacy_path)
        legacy_payload_drift_candidate["payload_sha256"] = payload_sha256(legacy_payload_drift_candidate)
        total += 1
        try:
            audit_closure_candidate(legacy_payload_drift_candidate, legacy_payload_drift_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] mutated canonical #995 payload survived trusted identity gate")

        active_source_drift_root = (fixture_root / "active-source-drift").resolve()
        active_source_drift_root.mkdir()
        active_source_drift_candidate = add_valid_legacy_mapping_fixture(
            active_source_drift_root, build_typed_candidate_fixture(active_source_drift_root)
        )
        drift_active_path = active_source_drift_root / ACTIVE_SPINE_REL
        drift_active_path.write_text("TEST-ONLY: not the active architecture spine\n")
        active_source_drift_candidate["source_bindings"][ACTIVE_SPINE_REL.as_posix()] = sha256_file(drift_active_path)
        active_source_drift_candidate["payload_sha256"] = payload_sha256(active_source_drift_candidate)
        total += 1
        try:
            audit_closure_candidate(active_source_drift_candidate, active_source_drift_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] mutated canonical active spine survived trusted identity gate")

        zero_legacy_root = (fixture_root / "legacy-zero-charge").resolve()
        zero_legacy_root.mkdir()
        zero_legacy_candidate = add_valid_legacy_mapping_fixture(
            zero_legacy_root, build_typed_candidate_fixture(zero_legacy_root)
        )
        zero_legacy_candidate["atoms"][0]["value"] = "0"
        zero_legacy_candidate["claim"]["total_charge"] = "0"
        zero_upaid_path = zero_legacy_root / zero_legacy_candidate["atoms"][0]["source_binding"]
        zero_upaid_manifest = load_json_strict(zero_upaid_path)
        zero_upaid_manifest["value"] = "0"
        write_payload_manifest(zero_upaid_path, zero_upaid_manifest)
        zero_legacy_candidate["source_bindings"][zero_legacy_candidate["atoms"][0]["source_binding"]] = sha256_file(zero_upaid_path)
        zero_legacy_candidate["payload_sha256"] = payload_sha256(zero_legacy_candidate)
        total += 1
        try:
            audit_closure_candidate(zero_legacy_candidate, zero_legacy_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] mapped legacy charge erased from active U_paid")

        wrong_atom_root = (fixture_root / "legacy-wrong-target-atom").resolve()
        wrong_atom_root.mkdir()
        wrong_atom_candidate = add_valid_legacy_mapping_fixture(
            wrong_atom_root, build_typed_candidate_fixture(wrong_atom_root)
        )
        wrong_mapping = wrong_atom_candidate["architecture_mapping"]
        wrong_mapping["mapped_active_owner_ids"] = ["owner-1"]
        wrong_mapping["owner_mapping"] = [
            {"legacy_owner_id": "legacy-owner-0", "active_owner_ids": ["owner-1"]}
        ]
        wrong_owner_path = wrong_atom_root / wrong_mapping["owner_map_source_binding"]
        wrong_owner_manifest = load_json_strict(wrong_owner_path)
        wrong_owner_manifest["mapped_active_owner_ids"] = ["owner-1"]
        wrong_owner_manifest["owner_mapping"] = copy.deepcopy(wrong_mapping["owner_mapping"])
        write_payload_manifest(wrong_owner_path, wrong_owner_manifest)
        wrong_mapping["owner_map_sha256"] = sha256_file(wrong_owner_path)
        wrong_atom_candidate["source_bindings"][wrong_mapping["owner_map_source_binding"]] = wrong_mapping["owner_map_sha256"]
        wrong_mapping_path = wrong_atom_root / wrong_mapping["source_binding"]
        write_payload_manifest(
            wrong_mapping_path,
            {"schema": ARCHITECTURE_MAPPING_SCHEMA, **{key: val for key, val in wrong_mapping.items() if key != "source_binding"}},
        )
        wrong_atom_candidate["source_bindings"][wrong_mapping["source_binding"]] = sha256_file(wrong_mapping_path)
        wrong_atom_candidate["payload_sha256"] = payload_sha256(wrong_atom_candidate)
        total += 1
        try:
            audit_closure_candidate(wrong_atom_candidate, wrong_atom_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] legacy charge mapped into non-U_paid owner")

        laundering_root = (fixture_root / "legacy-laundering").resolve()
        laundering_root.mkdir()
        laundering_candidate = add_reformatted_legacy_laundering_fixture(
            laundering_root, build_typed_candidate_fixture(laundering_root)
        )
        total += 1
        try:
            audit_closure_candidate(laundering_candidate, laundering_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] reformatted legacy #995 provenance laundering survived")

        predecessor_laundering_root = (fixture_root / "legacy-predecessor-envelope").resolve()
        predecessor_laundering_root.mkdir()
        predecessor_laundering_candidate = add_reformatted_legacy_laundering_fixture(
            predecessor_laundering_root,
            build_typed_candidate_fixture(predecessor_laundering_root),
            legacy_source=KB994_REL,
            suffix=".json",
            envelope=True,
        )
        total += 1
        try:
            audit_closure_candidate(predecessor_laundering_candidate, predecessor_laundering_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] enveloped legacy predecessor provenance laundering survived")

        markdown_laundering_root = (fixture_root / "legacy-markdown-envelope").resolve()
        markdown_laundering_root.mkdir()
        markdown_laundering_candidate = add_reformatted_legacy_laundering_fixture(
            markdown_laundering_root,
            build_typed_candidate_fixture(markdown_laundering_root),
            suffix=".md",
            markdown_envelope=True,
        )
        total += 1
        try:
            audit_closure_candidate(markdown_laundering_candidate, markdown_laundering_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] Markdown-wrapped legacy provenance laundering survived")

        string_laundering_root = (fixture_root / "legacy-json-string-envelope").resolve()
        string_laundering_root.mkdir()
        string_laundering_candidate = add_reformatted_legacy_laundering_fixture(
            string_laundering_root,
            build_typed_candidate_fixture(string_laundering_root),
            envelope=True,
            stringify=True,
        )
        total += 1
        try:
            audit_closure_candidate(string_laundering_candidate, string_laundering_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] JSON-string legacy provenance laundering survived")

        deep_laundering_root = (fixture_root / "legacy-over-depth-envelope").resolve()
        deep_laundering_root.mkdir()
        deep_laundering_candidate = add_reformatted_legacy_laundering_fixture(
            deep_laundering_root,
            build_typed_candidate_fixture(deep_laundering_root),
            nesting_depth=MAX_EMBEDDED_JSON_DEPTH + 2,
        )
        total += 1
        try:
            audit_closure_candidate(deep_laundering_candidate, deep_laundering_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] over-depth legacy provenance laundering survived")

        oversized_string_root = (fixture_root / "legacy-oversized-json-string").resolve()
        oversized_string_root.mkdir()
        oversized_string_candidate = add_reformatted_legacy_laundering_fixture(
            oversized_string_root,
            build_typed_candidate_fixture(oversized_string_root),
            envelope=True,
            stringify=True,
            string_padding_bytes=MAX_EMBEDDED_JSON_BYTES + 1,
        )
        total += 1
        try:
            audit_closure_candidate(oversized_string_candidate, oversized_string_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] oversized JSON-string legacy provenance laundering survived")

        direct_component_mutations = [
            (
                "typed-Q-priority-row",
                "priority-map",
                lambda manifest: manifest.__setitem__("row_id", "m31_mca"),
                False,
            ),
            (
                "typed-Q-boolean-integer-confusion",
                "priority-map",
                lambda manifest: manifest["claims"].__setitem__("first_match_priority_frozen", 1),
                False,
            ),
            (
                "typed-Q-target-unresolved",
                "target-map",
                lambda manifest: manifest.__setitem__("unresolved_hypotheses", ["open"]),
                False,
            ),
            (
                "typed-Q-joint-cross-binding",
                "joint-max",
                lambda manifest: manifest["claims"].__setitem__("residual_predicate_sha256", "f" * 64),
                True,
            ),
        ]
        for index, (name, component_name, mutate, preserve_bad) in enumerate(direct_component_mutations):
            case_root = (fixture_root / f"direct-{index}").resolve()
            case_root.mkdir()
            case_base = build_typed_candidate_fixture(case_root)
            tampered = mutate_typed_q_component_fixture(
                case_root, case_base, component_name, mutate, preserve_bad
            )
            total += 1
            try:
                audit_closure_candidate(tampered, case_root)
            except (RuntimeError, KeyError, TypeError, ValueError):
                rejected += 1
            else:
                print(f"[FAIL] invalid typed component survived: {name}")

        transitive_legacy_root = (fixture_root / "legacy-transitive-q-component").resolve()
        transitive_legacy_root.mkdir()
        transitive_legacy_base = add_valid_legacy_mapping_fixture(
            transitive_legacy_root, build_typed_candidate_fixture(transitive_legacy_root)
        )
        transitive_legacy_candidate = mutate_typed_q_component_fixture(
            transitive_legacy_root,
            transitive_legacy_base,
            "priority-map",
            lambda manifest: manifest["proof_source_bindings"].append(KB995_REL.as_posix()),
        )
        total += 1
        try:
            audit_closure_candidate(transitive_legacy_candidate, transitive_legacy_root)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            print("[FAIL] transitive Q-component consumption of legacy #995 survived")

    duplicate = '{"schema":"x","schema":"y"}'
    float_json = '{"schema":"x","value":1.5}'
    for name, text in [("duplicate-json-key", duplicate), ("float-json-number", float_json)]:
        total += 1
        try:
            parse_json_strict_text(text)
        except RuntimeError:
            rejected += 1
        else:
            print(f"[FAIL] strict parser mutation survived: {name}")

    print(f"tamper self-test: rejected {rejected}/{total}")
    return 0 if rejected == total else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="check canonical open-state certificate")
    group.add_argument("--emit", action="store_true", help="print canonical certificate JSON")
    group.add_argument("--tamper-selftest", action="store_true", help="run semantic/parser mutations")
    group.add_argument(
        "--audit-candidate",
        type=Path,
        help="structurally preflight a future claimed manifest; never certify closure",
    )
    args = parser.parse_args()

    try:
        if args.tamper_selftest:
            return tamper_selftest()
        if args.audit_candidate is not None:
            result = audit_closure_candidate(load_candidate_json_strict(args.audit_candidate))
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        if args.emit:
            print(json.dumps(build_certificate(), indent=2, sort_keys=True))
            return 0
        check_certificate()
        print("[PASS] four-row exact-completion compiler certificate")
        print(f"[PASS] terminal: {TERMINAL}")
        print("[PASS] active rows closed: 0/4")
        print("[PASS] exact deployed U_Q atoms: 0/4")
        print("[PASS] legacy #995 charge kept outside active ledger without a mapping certificate")
        print("[PASS] direct-extension route cuts: M31 e_Y>=1; KB e_Y>=2")
        return 0
    except (RuntimeError, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
