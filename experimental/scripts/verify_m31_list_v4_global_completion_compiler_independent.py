#!/usr/bin/env python3
"""Independent exact replay of the M31 v4 global completion compiler.

This implementation imports no code from the primary verifier.  It checks
canonical JSON, every live file and predecessor payload pin, the five-atom
source contract, both sharp RLE occupancy fixtures, and the fail-closed
route-cut verdict.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json"
SCHEMA = ROOT / "experimental/data/schemas/m31_list_v4_global_completion_compiler_v2.schema.json"

SCHEMA_ID = "rs-mca-m31-list-v4-global-completion-compiler-v2"
COMPILER_ID = "M31_LIST_V4_GLOBAL_COMPLETION_COMPILER_V2"
ARCHITECTURE = "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
PARTITION = "816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc"
UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"
QUANTIFIER = "UNIFORM_OVER_ALL_RECEIVED_WORDS"
ATOMS = ["U_paid", "U_Q", "U_list_int", "U_ext", "U_new"]

GRAPH = [
    ("global_source_adapter", "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json", "21b213e2b3dfc7f8f99049aea44542ce5ae06dd59b62c10555f9faf5aaa882ce", 3730),
    ("canonical_masked_pade", "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json", "b23186b09c7017fc80e836b70eea042077a30db22706763d33a98c053a44b0c3", 0),
    ("full_span_forced_collision", "experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json", "5b139aaea139cc0d0440927d7df04e267b6e13a1775dc48c79acb1abc8bbc5d3", 0),
    ("fixed_remainder_boundary_source", "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json", "056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7", 0),
    ("boundary_occupancy_30carrier", "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json", "c312bd2c108634af51cd351a004cdb2942bc10a145eca3e49dbcfe8fe8873a7c", 0),
    ("boundary_multiprefix_activation", "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json", "dacb9136f5818a5f86d9ca8987fbe4d361a57a70ebb490eac50dfc3822e062e4", 0),
    ("boundary_65column_route_cut", "experimental/data/certificates/m31-c2048-65column-fixed-anchor-route-cut-v1/manifest.json", "1474cf06d7a058a010462ca06758df0576de9464441fa9245ddaf1b8e7d23245", 0),
    ("fixed_template_interleaved_quotient", "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json", "99febb07f517aac958e55eeba466e268a4ada793ef7960a189374603ea4a3ec9", 0),
    ("fixed_template_module_rank", "experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json", "c164f24810e0ed5015b3e538607e8867c7f634d5797de645c455447a08aaa303", 0),
    ("guarded_support_flat_separator", "experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/manifest.json", "d0aa51bd3811ad5e93269f7174afc249fc2865715cb484e41cd233bcab775960", 0),
    ("vt_multitemplate_global_rank", "experimental/data/certificates/m31-c2048-vt-multitemplate-global-rank-route-cut-v1/manifest.json", "34fe14e21ebcb7a3932cc44e73d19c7f39a154fcb7581821c538ab2c751bc1d8", 0),
]

TERMINALS = {
    "global_source_adapter": "UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL",
    "canonical_masked_pade": "UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND",
    "full_span_forced_collision": "UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER",
    "fixed_remainder_boundary_source": "M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL",
    "boundary_occupancy_30carrier": "M31_C2048_BIDEEP_30COLUMN_OWNER",
    "boundary_multiprefix_activation": "M31_C2048_FIXED_SYNDROME_MULTIPREFIX_FACE_CARRIER_OWNER",
    "boundary_65column_route_cut": "M31_C2048_65COLUMN_FIXED_ANCHOR_OWNER",
    "fixed_template_interleaved_quotient": "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER",
    "fixed_template_module_rank": "UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP",
    "guarded_support_flat_separator": "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER",
    "vt_multitemplate_global_rank": "UNPAID_VT_MULTITEMPLATE_GUARDED_LINE_INCIDENCE",
}

TERMINAL_PATHS = {
    "global_source_adapter": ("closure_state", "unpaid_global_residual", "terminal"),
    "canonical_masked_pade": ("route_cut", "deployed_terminal"),
    "full_span_forced_collision": ("deployed_context", "successor_terminal"),
    "fixed_remainder_boundary_source": ("chronology_specialization", "route_terminal"),
    "boundary_occupancy_30carrier": ("carrier_reduction", "route_terminal"),
    "boundary_multiprefix_activation": ("chronology", "boundary_diagnostic_subterminal"),
    "boundary_65column_route_cut": ("chronology", "successor_terminal"),
    "fixed_template_interleaved_quotient": ("chronology", "successor_terminal"),
    "fixed_template_module_rank": ("chronology", "nested_diagnostic_subterminal"),
    "guarded_support_flat_separator": ("chronology", "boundary_subterminal"),
    "vt_multitemplate_global_rank": ("chronology", "diagnostic"),
}


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, f"duplicate key: {key}")
        out[key] = value
    return out


def reject_float(_value: str) -> Any:
    raise RuntimeError("floats forbidden")


def reject_constant(_value: str) -> Any:
    raise RuntimeError("nonfinite values forbidden")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_without_seal(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return digest(canonical(unsigned))


def legacy_digest(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return digest(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load_json(path: Path, *, require_canonical: bool = True) -> dict[str, Any]:
    raw = path.read_bytes()
    need(len(raw) <= 64 * 1024 * 1024, f"oversized JSON: {path}")
    value = json.loads(
        raw.decode("ascii"),
        object_pairs_hook=unique_object,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )
    need(type(value) is dict, f"object required: {path}")
    if require_canonical:
        need(raw == canonical(value), f"canonical bytes: {path}")
    return value


def repo_path(text: str) -> Path:
    need(type(text) is str and text.isascii(), "ASCII source path")
    pure = PurePosixPath(text)
    need(not pure.is_absolute() and "." not in pure.parts and ".." not in pure.parts, "canonical relative source path")
    path = ROOT.joinpath(*pure.parts)
    need(path.exists() and path.is_file() and not path.is_symlink(), f"regular source: {text}")
    need(path.resolve().is_relative_to(ROOT.resolve()), f"contained source: {text}")
    return path


def decimal(text: Any) -> int:
    need(type(text) is str and text.isascii() and 1 <= len(text) <= 256, "bounded ASCII decimal")
    need(all("0" <= char <= "9" for char in text), "decimal digits")
    need(text == "0" or text[0] != "0", "no leading zero")
    return int(text)


def at_path(value: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = value
    for key in path:
        need(type(current) is dict and key in current, f"terminal path: {'.'.join(path)}")
        current = current[key]
    return current


def verify_embedded_bindings(source: dict[str, Any], *, role: str) -> tuple[int, int]:
    bindings = source.get("source_bindings")
    need(type(bindings) is list and len(bindings) > 0, f"{role} source registry")
    internal_pin_count = 0
    for index, binding in enumerate(bindings):
        need(type(binding) is dict and type(binding.get("path")) is str, f"{role} binding {index}")
        path = repo_path(binding["path"])
        need(binding.get("sha256") == digest(path.read_bytes()), f"{role} fresh source {index}")
        internal = binding.get("internal_payload_sha256")
        if internal is not None:
            internal_pin_count += 1
            need(type(internal) is str and len(internal) == 64, f"{role} internal pin type {index}")
            nested = load_json(path, require_canonical=False)
            need(nested.get("payload_sha256") == internal or nested.get("certificate_sha256") == internal, f"{role} internal pin {index}")
    return len(bindings), internal_pin_count


def verify_fixture(fixture: dict[str, Any], *, forbidden: bool) -> None:
    p = 2**31 - 1
    q = p**4
    budget = q // 2**100
    target_total = budget + (1 if forbidden else 0)
    target_xi = 259_881 if forbidden else 259_880
    target_t = 259_926 if forbidden else 259_925
    j0, radius, low, baseline = 614_160, 981_129, 3_730, 45
    high_layers = radius - j0

    blocks = fixture["weight_blocks"]
    need(type(blocks) is list and len(blocks) == 4, "four RLE blocks")
    previous_end = j0 - 1
    previous_multiplicity: int | None = None
    low_mass = total = t46 = 0
    high_counts = [0] * (baseline + 1)
    for index, block in enumerate(blocks):
        need(set(block) == {"start", "end", "multiplicity"}, "RLE keys")
        start, end, multiplicity = block["start"], block["end"], block["multiplicity"]
        need(type(start) is int and type(end) is int and type(multiplicity) is int, "RLE integer types")
        need(start == previous_end + 1 and start <= end, "RLE contiguous")
        need(previous_multiplicity is None or multiplicity != previous_multiplicity, "RLE maximal")
        width = end - start + 1
        if multiplicity == 0:
            need(index == 3 and start == end == radius, "only boundary zero")
        else:
            need(multiplicity > 0, "positive occupied multiplicity")
        if end <= j0:
            low_mass += width * multiplicity
        else:
            need(start > j0, "cutoff-aligned RLE")
            t46 += width * max(0, multiplicity - baseline)
            for level in range(1, baseline + 1):
                high_counts[level] += width if multiplicity >= level else 0
        total += width * multiplicity
        previous_end, previous_multiplicity = end, multiplicity

    c_low = low - low_mass
    credits = sum(high_layers - high_counts[level] for level in range(1, baseline + 1))
    xi = t46 - c_low - credits
    need((low_mass, c_low) == (low, 0), "low fixture")
    need(high_counts[1:] == [high_layers - 1] * baseline, "empty-boundary level counts")
    need((credits, t46, xi, total) == (45, target_t, target_xi, target_total), "signed fixture arithmetic")
    need(fixture["boundary_weight"] == radius and fixture["boundary_multiplicity"] == 0, "explicit empty boundary")
    need(fixture["T46"] == t46 and fixture["Xi46"] == xi and fixture["total_mass"] == total, "fixture summaries")
    need(fixture["source_realized"] is False and fixture["received_word_constructed"] is False, "arithmetic relaxation only")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = load_json(args.manifest)
    need(data["payload_sha256"] == digest_without_seal(data), "payload seal")
    schema = load_json(SCHEMA, require_canonical=False)
    need(schema["$id"] == SCHEMA_ID and schema["additionalProperties"] is False, "closed schema")
    need(set(data) == set(schema["required"]), "exact top-level keys")

    need(data["schema"] == SCHEMA_ID, "schema id")
    need(data["compiler_id"] == COMPILER_ID, "compiler id")
    need(data["architecture_id"] == ARCHITECTURE, "source architecture retained")
    need(data["row_contract"]["unit"] == UNIT and data["row_contract"]["quantifier"] == QUANTIFIER, "row unit/quantifier")

    p = 2**31 - 1
    q = p**4
    n, k, agreement = 2**21, 2**20, 1_116_023
    radius, shift = n - agreement, agreement - k
    budget, forbidden = q // 2**100, q // 2**100 + 1
    j0, low, free = 614_160, 3_730, 45
    layers = radius - j0
    base = low + free * layers
    need((p, radius, shift, budget, forbidden) == (2_147_483_647, 981_129, 67_447, 16_777_215, 16_777_216), "row arithmetic")
    need(decimal(data["row_contract"]["code_field_cardinality"]) == q, "field cardinality")
    need((layers, base, budget - base, forbidden - base) == (366_969, 16_517_335, 259_880, 259_881), "signed threshold")

    partition = data["partition"]
    need(partition["atom_order"] == ATOMS and partition["partition_sha256"] == PARTITION, "five-atom partition")
    need(partition["unit"] == UNIT and partition["quantifier"] == QUANTIFIER, "partition unit/quantifier")
    adapter_path = repo_path(GRAPH[0][1])
    adapter = load_json(adapter_path)
    need(partition["source_manifest_sha256"] == digest(adapter_path.read_bytes()), "adapter file hash")
    need(partition["source_payload_sha256"] == GRAPH[0][2] == adapter["payload_sha256"], "adapter payload")

    atom_state = data["atom_state"]
    need(atom_state["atom_order"] == ATOMS and atom_state["known_sum"] == low, "atom order and low payment")
    need(atom_state["null_atoms"] == ATOMS[1:] and atom_state["row_closed"] is False, "four null atoms")
    need(atom_state["atoms"][0]["value"] == low and atom_state["atoms"][0]["bankable"] is True, "banked low atom")
    need(all(row["value"] is None and row["bankable"] is False for row in atom_state["atoms"][1:]), "null is not zero")

    closure = data["closure_contract"]
    need(closure["exact_signed_expression"] == "Xi46=T46_interior+T46_boundary-C_low-sum_{r=1}^{45}C_r", "signed identity")
    need(closure["signed_comparator"] == "<=" and closure["signed_Xi46_upper_required"] == 259_880, "signed gate")
    need(closure["raw_T46_upper_259880_required"] is False, "raw cap rejected")
    interface = data["candidate_interface"]
    need(interface["accepted_completion_modes"] == ["FIVE_EXACT_NONNEGATIVE_SOURCE_PARTITION_ATOMS", "DIRECT_SIGNED_HISTOGRAM_BOUND"], "two completion modes")
    need(interface["direct_mode_does_not_fabricate_atom_values"] is True, "direct mode preserves null atoms")
    need(interface["negative_refund_atom_interface_available"] is False, "no invented negative atom")
    verify_fixture(data["boundary_free_extremizers"]["safe_sharp"], forbidden=False)
    verify_fixture(data["boundary_free_extremizers"]["first_forbidden"], forbidden=True)

    graph = data["current_artifact_graph"]
    need([row["role"] for row in graph] == [row[0] for row in GRAPH], "route-cut chronology")
    transitive_binding_count = 0
    internal_pin_count = 0
    for actual, (role, path_text, payload, movement) in zip(graph, GRAPH, strict=True):
        source = load_json(repo_path(path_text))
        need(actual["path"] == path_text and actual["payload_sha256"] == payload, f"{role} graph pin")
        need(source["payload_sha256"] == payload == digest_without_seal(source), f"{role} live payload")
        need(actual["terminal_or_scope"] == TERMINALS[role] == at_path(source, TERMINAL_PATHS[role]), f"{role} terminal")
        need(actual["ledger_movement"] == movement, f"{role} movement")
        need(actual["import_mode"] == ("SOURCE_CONTRACT_AND_LOW_PAYMENT" if movement else "ROUTE_CUT_ONLY"), f"{role} mode")
        need(actual["bankable"] is (movement > 0), f"{role} bankability")
        count, pins = verify_embedded_bindings(source, role=role)
        need(actual["source_binding_count"] == count, f"{role} source binding count")
        need(actual["internal_payload_pin_count"] == pins, f"{role} internal pin count")
        transitive_binding_count += count
        internal_pin_count += pins
    need(transitive_binding_count == 172, "transitive source binding census")
    need(internal_pin_count == 29, "internal payload pin census")
    need(data["source_graph_freshness"] == {
        "direct_predecessor_count": len(GRAPH),
        "every_embedded_path_and_sha256_fresh": True,
        "internal_payload_pins_checked_when_present": True,
        "internal_payload_pin_count": internal_pin_count,
        "transitive_source_binding_count": transitive_binding_count,
    }, "source graph freshness summary")

    old = load_json(repo_path(data["historical_compiler"]["path"]), require_canonical=False)
    need(old["payload_sha256"] == "8e1811e91f2b58f2c7497e419047c3e260ef20cdcfef448dc8df0109704797b0", "historical payload")
    need(legacy_digest(old) == old["payload_sha256"], "historical payload seal")
    need(data["historical_compiler"]["active_authority"] is False, "historical demoted for M31 LIST")
    need(data["historical_compiler"]["superseded_as_live_authority_not_refuted"] is True, "historical non-refutation")

    for binding in data["source_bindings"]:
        path = repo_path(binding["path"])
        need(binding["sha256"] == digest(path.read_bytes()), f"source binding: {binding['role']}")

    guards = data["scope_guards"]
    need(guards["signed_Xi46_bound_proved"] is False and guards["five_atom_additive_ledger_complete"] is False, "closure remains open")
    need(guards["high_residual_payment_movement"] == guards["official_row_movement"] == 0, "no ledger movement")
    need(guards["route_cut_registry_contains_payment"] is False, "route cuts not payments")
    need(data["open_pr_admissibility"]["proof_dependency"] is False, "open PR advisory only")
    need(data["open_pr_admissibility"]["pr_1047"]["admissible_payment"] is False, "1047 rejected")
    need(data["open_pr_admissibility"]["pr_1048"]["admissible_payment"] is False, "1048 rejected")
    need(data["open_pr_admissibility"]["pr_1051"]["admissible_payment"] is False, "1051 rejected")

    print("M31 LIST v4 global compiler v2 independent replay: PASS")
    print("source architecture / five codeword atoms / enumerated post-adapter graph: PASS")
    print("safe Xi46=259880 and first-forbidden Xi46=259881 RLE fixtures: PASS")
    print("boundary-only additive/numerical and raw-T46 routes: CUT; row OPEN; movement beyond U_paid=3730 is zero")


if __name__ == "__main__":
    main()
