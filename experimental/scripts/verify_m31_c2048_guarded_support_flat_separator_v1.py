#!/usr/bin/env python3
"""Verify the M31 c=2048 guarded support-flat separator interface.

This packet certifies an exact interface and converse, not VT(U) itself.
It seals the deployed arithmetic, the static fixed-template block contract,
the target-field hyperplane-union gates, the shifted-locator 15/16 wall, and
an exact small-field guarded-rank fixture.  No ledger atom is moved.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable


SCHEMA_ID = "rs-mca-c2048-guarded-support-flat-separator-v1"
ARCHITECTURE_ID = "M31_C2048_GUARDED_SUPPORT_FLAT_SEPARATOR_V1"
STATUS = "PROVED_EXACT_GLOBAL_SEPARATOR_INTERFACE_VT_OPEN"
GLOBAL_TERMINAL = "UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER"
BOUNDARY_SUBTERMINAL = "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER"
DIAGNOSTIC = "UNPROVEN_GUARDED_SUPPORT_FLAT_SEPARATOR_VT"

P = 2**31 - 1
TARGET_FIELD_SIZE = P**4
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = K - RADIUS
MINIMUM_DISTANCE = N - K + 1
B_STAR = TARGET_FIELD_SIZE // 2**100
U_PAID = 3_730
BOUNDARY_TARGET = 9_216_781
FOLD_DEGREE = 2_048
QUOTIENT_LABELS = N // FOLD_DEGREE
PROFILE_COUNT = 261_192

PARENT_PR = 1044
PARENT_HEAD = "5b097b607ae60f7d46c730654eb04fa8a63c8595"
PARENT_PAYLOAD = "c164f24810e0ed5015b3e538607e8867c7f634d5797de645c455447a08aaa303"
FIXED_TEMPLATE_PR = 1043
FIXED_TEMPLATE_HEAD = "0d93d366072a0ad3f66c73f9b5a6329a232b4293"
FIXED_TEMPLATE_PAYLOAD = "99febb07f517aac958e55eeba466e268a4ada793ef7960a189374603ea4a3ec9"
SHORTENED_FLAT_CERTIFICATE = "45195b2f6276313678e779be7dca17b3e78badf4e66f49e1dc76ac8819873d28"
OCCUPANCY_ATLAS_PAYLOAD = "c312bd2c108634af51cd351a004cdb2942bc10a145eca3e49dbcfe8fe8873a7c"
SOURCE_ADAPTER_PAYLOAD = "21b213e2b3dfc7f8f99049aea44542ce5ae06dd59b62c10555f9faf5aaa882ce"
FOUR_ROW_PAYLOAD = "8e1811e91f2b58f2c7497e419047c3e260ef20cdcfef448dc8df0109704797b0"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_c2048_guarded_support_flat_separator_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_c2048_guarded_support_flat_separator.md"
README_PATH = ROOT / "experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the guarded support-flat separator packet."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Exact arithmetic, theorem-interface, fixture, and mutation replay."),
    ("packet_sage", SAGE_PATH, None,
     "Independent MDS, annihilator, union-avoidance, and locator replay."),
    ("packet_note", NOTE_PATH, None,
     "Symbolic VT interface, converse, matrix compiler, and nonclaims."),
    ("packet_readme", README_PATH, None,
     "Replay commands, exact dependency, and scope contract."),
    ("shortened_flat_note",
     ROOT / "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md",
     None, "Exact shortened-flat and syndrome-hyperplane interface authority."),
    ("shortened_flat_verifier",
     ROOT / "experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py",
     None, "Exact shortened-flat arithmetic and scope replay."),
    ("shortened_flat_sage",
     ROOT / "experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.sage",
     None, "Independent finite-field shortened-flat replay."),
    ("shortened_flat_manifest",
     ROOT / "experimental/data/certificates/m31-shortened-flat-hyperplane-wall/manifest.json",
     "certificate_sha256", "Sealed shortened-flat predecessor."),
    ("fixed_template_1043_note",
     ROOT / "experimental/notes/thresholds/m31_c2048_fixed_template_interleaved_quotient_route_cut.md",
     None, "Positional fixed-template block-cap theorem."),
    ("fixed_template_1043_verifier",
     ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.py",
     None, "Exact fixed-template cap and all-profile census."),
    ("fixed_template_1043_sage",
     ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.sage",
     None, "Independent fixed-template algebra replay."),
    ("parent_1044_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json",
     "payload_sha256", "Exact stacked parent PR #1044."),
    ("parent_1044_note",
     ROOT / "experimental/notes/thresholds/m31_c2048_fixed_template_module_rank_route_cut.md",
     None, "Parent fixed-template module-rank theorem and terminal scope."),
    ("parent_1044_verifier",
     ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.py",
     None, "Parent exact census and semantic gates."),
    ("parent_1044_sage",
     ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.sage",
     None, "Parent independent rank replay."),
    ("fixed_template_1043_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json",
     "payload_sha256", "Exact positional-template block-cap authority PR #1043."),
    ("occupancy_atlas_note",
     ROOT / "experimental/notes/thresholds/m31_c2048_partial_occupancy_30carrier_reduction.md",
     None, "Exhaustive c=2048 occupancy profile authority."),
    ("occupancy_atlas_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json",
     "payload_sha256", "Sealed exhaustive occupancy atlas."),
    ("complete_support_factorization",
     ROOT / "experimental/rs_mca_thresholds.tex", None,
     "Complete-support factorization and free-module coordinates."),
    ("source_adapter_note",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Target-field LIST chronology and boundary residual."),
    ("source_adapter_manifest",
     ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
     "payload_sha256", "Sealed target-field LIST source adapter."),
    ("four_row_note",
     ROOT / "experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md",
     None, "Live four-row null-atom and architecture status authority."),
    ("four_row_certificate",
     ROOT / "experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json",
     "payload_sha256", "Sealed four-row live status certificate."),
    ("global_separator_provenance",
     ROOT / "experimental/notes/thresholds/m31_chebyshev_global_separator.md",
     None, "Prior global-separator provenance; not a payment source."),
    ("sidon_escape_provenance",
     ROOT / "experimental/notes/thresholds/m31_sidon_three_fibre_escape_compiler.md",
     None, "Prior Sidon escape provenance; not a payment source."),
    ("whole_ball_scope_guard",
     ROOT / "experimental/notes/thresholds/m31_whole_ball_source_separator_compiler.md",
     None, "Whole-ball source/separator nonclosure and scope guard."),
    ("active_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active nonnegative LIST chronology and row-sharp target."),
    ("foundation", ROOT / "tex/cs25_cap_v13_2.tex", None,
     "Deployed M31 field, domain, code, and exact-support conventions."),
)


class VerificationError(RuntimeError):
    """Fail-closed certificate error."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (rendered + "\n").encode("ascii")


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON is forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN and infinity are forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, *, canonical: bool = False) -> Any:
    require(len(raw) <= 32 * 1024 * 1024, "JSON size bound")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    value = json.loads(
        text, object_pairs_hook=unique_object, parse_int=int,
        parse_float=reject_float, parse_constant=reject_constant,
    )
    if canonical:
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def strict_json_path(path: Path, *, canonical: bool = False) -> Any:
    require(path.is_file(), f"JSON path exists: {path}")
    return strict_json_bytes(path.read_bytes(), canonical=canonical)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"bound source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_sha256(result)
    return result


def internal_payload(path: Path, key: str | None) -> str | None:
    if key is None:
        return None
    # Some sealed predecessor certificates predate the repository's compact
    # canonical-byte convention.  Their exact file bytes are hash-bound below;
    # parse them strictly here without rewriting or silently canonicalizing.
    value = strict_json_path(path, canonical=False)
    require(type(value) is dict, f"internal payload object: {path}")
    internal = value.get(key)
    require(type(internal) is str and len(internal) == 64,
            f"internal payload hash: {path}")
    return internal


def expected_source_bindings() -> list[dict[str, Any]]:
    result = []
    for role, path, internal_key, scope in SOURCE_SPECS:
        relative = path.relative_to(ROOT)
        require(PurePosixPath(relative.as_posix()).as_posix() == relative.as_posix(),
                f"canonical source path: {path}")
        internal = internal_payload(path, internal_key)
        if role == "parent_1044_manifest":
            require(internal == PARENT_PAYLOAD, "exact #1044 payload")
        if role == "fixed_template_1043_manifest":
            require(internal == FIXED_TEMPLATE_PAYLOAD, "exact #1043 payload")
        if role == "shortened_flat_manifest":
            require(internal == SHORTENED_FLAT_CERTIFICATE,
                    "exact shortened-flat certificate")
        if role == "occupancy_atlas_manifest":
            require(internal == OCCUPANCY_ATLAS_PAYLOAD,
                    "exact occupancy-atlas payload")
        if role == "source_adapter_manifest":
            require(internal == SOURCE_ADAPTER_PAYLOAD,
                    "exact source-adapter payload")
        if role == "four_row_certificate":
            require(internal == FOUR_ROW_PAYLOAD, "exact four-row payload")
        result.append({
            "binding_id": f"M31_C2048_GUARDED_VT::{role}",
            "path": relative.as_posix(),
            "role": role,
            "scope": scope,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
        })
    return result


def poly_from_roots(roots: Iterable[int], modulus: int) -> list[int]:
    coefficients = [1]
    for root in roots:
        out = [0] * (len(coefficients) + 1)
        for index, value in enumerate(coefficients):
            out[index] = (out[index] - root * value) % modulus
            out[index + 1] = (out[index + 1] + value) % modulus
        coefficients = out
    return coefficients


def matrix_rank_mod(rows: list[list[int]], modulus: int) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "matrix row widths")
    matrix = [[value % modulus for value in row] for row in rows]
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(matrix))
             if matrix[row][column] % modulus),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, modulus)
        matrix[rank] = [(inverse * value) % modulus
                        for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % modulus
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


TOY_SUPPORT_MASKS = (
    0x289C74A698305B3E, 0x0A9E14273591CFC8,
    0x085C2B48F3FCA189, 0x1363292C82CBEAE1,
    0x1C93B8F7170700C5, 0x0E472F050A2AF8D3,
    0x3990613B5110FADA, 0x0AE93D41D5A88669,
    0x02F8B93C467740B8, 0x02C449E8C56B7E83,
    0x094EB825472CBB92, 0x3708C32432F86BC3,
    0x06D753AB0B001F6A, 0x041DE1E33233CEA2,
    0x11C1D60B357740AB, 0x3C5F30C93700D1F0,
)
TOY_NEGATIVE_MASK = 0x3C5F30C93700D1E1


def support_from_mask(mask: int, domain_size: int) -> list[int]:
    require(mask >= 0 and mask < 1 << domain_size, "toy support mask range")
    return [index for index in range(domain_size) if (mask >> index) & 1]


def toy_fixture() -> dict[str, Any]:
    """Exact rank/escape fixture; GF(67) ranks persist over GF(67^2)."""
    modulus = 67
    target_size = modulus**2
    domain_size = 62
    ambient = 31
    radius = 29
    shift_count = 2
    supports = [support_from_mask(mask, domain_size)
                for mask in TOY_SUPPORT_MASKS]
    require(len(supports) == 16 and len(set(TOY_SUPPORT_MASKS)) == 16,
            "toy support count and uniqueness")
    require(all(len(support) == radius for support in supports),
            "toy support weights")

    locators = [poly_from_roots(support, modulus) for support in supports]
    require(all(len(locator) == radius + 1 and locator[-1] == 1
                for locator in locators), "toy monic locator degrees")
    require(all(((-locator[28]) % modulus, locator[27] % modulus) == (40, 58)
                for locator in locators), "toy common locator prefix")

    shifted_rows: list[list[int]] = []
    for locator in locators:
        shifted_rows.append(locator + [0])
        shifted_rows.append([0] + locator)
    rank_15 = matrix_rank_mod(shifted_rows[:30], modulus)
    rank_16 = matrix_rank_mod(shifted_rows, modulus)
    require(rank_15 == 30 and rank_16 == 30, "toy guarded 15/16 ranks")

    functional = [0] * ambient
    functional[28] = 1
    functional[29] = 40
    functional[30] = 1
    require(all(sum(left * right for left, right in zip(row, functional))
                % modulus == 0 for row in shifted_rows),
            "toy explicit support-flat annihilator")

    escaped = 0
    for support, locator in zip(supports, locators):
        for point in support:
            smaller = poly_from_roots(
                (value for value in support if value != point), modulus)
            rebuilt = poly_from_roots([point], modulus)
            product = [0] * (len(smaller) + 1)
            for left_index, left in enumerate(smaller):
                for right_index, right in enumerate(rebuilt):
                    product[left_index + right_index] = (
                        product[left_index + right_index] + left * right
                    ) % modulus
            require(product == locator, "toy escape locator division")
            escape = smaller + [0, 0]
            require(sum(left * right for left, right in zip(escape, functional))
                    % modulus == 1, "toy functional avoids escape")
            require(matrix_rank_mod(shifted_rows + [escape], modulus) == ambient,
                    "toy escape raises rank")
            escaped += 1
    require(escaped == 16 * radius == 464, "toy escape census")
    require(escaped < target_size and target_size - escaped == 4_025,
            "toy extension-field union gate")

    negative_support = support_from_mask(TOY_NEGATIVE_MASK, domain_size)
    require(len(negative_support) == radius, "toy negative support weight")
    require(set(negative_support) ==
            (set(supports[-1]).difference({4}).union({0})),
            "toy negative one-point replacement")
    negative_locator = poly_from_roots(negative_support, modulus)
    negative_rows = shifted_rows[:30] + [
        negative_locator + [0], [0] + negative_locator,
    ]
    negative_rank = matrix_rank_mod(negative_rows, modulus)
    require(negative_rank == ambient, "toy negative full-span mutation")

    mask_digest = sha256_bytes(canonical_json([
        f"0x{mask:016x}" for mask in TOY_SUPPORT_MASKS
    ]))
    return {
        "role": "EXACT_SMALL_FIELD_INTERFACE_FIXTURE_NOT_DEPLOYED_PROOF",
        "base_field_size": modulus,
        "coefficient_field_size": target_size,
        "domain_size": domain_size,
        "ambient_dimension": ambient,
        "radius": radius,
        "shift_count": shift_count,
        "support_count": len(supports),
        "support_masks_sha256": mask_digest,
        "common_locator_prefix": {"e1": 40, "e2": 58},
        "annihilator_functional": "coefficient_28+40*coefficient_29+coefficient_30",
        "first_15_shifted_rank": rank_15,
        "all_16_shifted_rank": rank_16,
        "all_16_annihilator_dimension": ambient - rank_16,
        "one_point_escape_count": escaped,
        "all_escapes_evaluate_to": 1,
        "union_margin": target_size - escaped,
        "negative_replacement": "support_16: 4 -> 0",
        "negative_shifted_rank": negative_rank,
    }


def union_gate(gate_id: str, U: int) -> dict[str, Any]:
    packet_size = U + 1
    guards = packet_size * RADIUS
    require(guards < TARGET_FIELD_SIZE, f"target-field union gate: {gate_id}")
    return {
        "gate_id": gate_id,
        "U": U,
        "packet_size": packet_size,
        "guard_hyperplane_upper": guards,
        "target_field_margin": str(TARGET_FIELD_SIZE - guards),
        "target_field_gate_strict": True,
        "base_field_gate_holds": guards < P,
    }


def core_payload() -> dict[str, Any]:
    require(P == 2_147_483_647, "Mersenne prime")
    require(TARGET_FIELD_SIZE ==
            21_267_647_892_944_572_736_998_860_269_687_930_881,
            "target field size")
    require((N, K, AGREEMENT, RADIUS, W) ==
            (2_097_152, 1_048_576, 1_116_023, 981_129, 67_447),
            "deployed code parameters")
    require(MINIMUM_DISTANCE == 1_048_577, "MDS distance")
    require(MINIMUM_DISTANCE - RADIUS == W + 1 == 67_448,
            "strict support uniqueness margin")
    require(B_STAR == 16_777_215, "LIST budget")
    require((AGREEMENT // FOLD_DEGREE, AGREEMENT % FOLD_DEGREE) ==
            (544, 1_911), "agreement quotient/remainder")
    require((RADIUS // FOLD_DEGREE, RADIUS % FOLD_DEGREE) ==
            (479, 137), "radius quotient/remainder")

    automatic_width = (K - 1) // W
    base_union_width = (P - 1) // RADIUS
    target_union_width = (TARGET_FIELD_SIZE - 1) // RADIUS
    require(automatic_width == 15, "automatic support-flat width")
    require(base_union_width == 2_188, "base-field union width")
    require(target_union_width == 21_676_709_069_800_783_319_011_934_485_361,
            "target-field union width")

    gates = [
        union_gate("conditional_face_carrier_target", BOUNDARY_TARGET),
        union_gate("post_U_paid_complete_boundary_target", B_STAR - U_PAID),
        union_gate("full_forbidden_packet", B_STAR),
    ]
    require([gate["guard_hyperplane_upper"] for gate in gates] == [
        9_042_852_106_878,
        16_456_953_545_694,
        16_460_613_156_864,
    ], "live union guard products")
    require(all(not gate["base_field_gate_holds"] for gate in gates),
            "live gates require target field")

    rows_15 = 15 * W
    rows_16 = 16 * W
    require((rows_15, K - rows_15) == (1_011_705, 36_871),
            "15-support automatic compatibility")
    require((rows_16, rows_16 - K) == (1_079_152, 30_576),
            "16-support first rank gate")
    require(rows_16 - (K - 1) == 30_577,
            "compatible 16-support syzygy nullity")

    return {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "deployed_parameters": {
            "p": P,
            "coefficient_field": "F_(p^4)",
            "target_field_size": str(TARGET_FIELD_SIZE),
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "w=K-radius": W,
            "minimum_distance": MINIMUM_DISTANCE,
            "strict_uniqueness_margin": MINIMUM_DISTANCE - RADIUS,
            "B_star": B_STAR,
            "U_paid": U_PAID,
            "conditional_boundary_target": BOUNDARY_TARGET,
            "fold_degree": FOLD_DEGREE,
            "quotient_labels": QUOTIENT_LABELS,
            "profile_count": PROFILE_COUNT,
        },
        "support_flat_interface": {
            "dual_dimension": K,
            "boundary_support_size": RADIUS,
            "flat_definition": "W_E={v in C^perp:supp(v) subset D\\E}",
            "flat_dimension": W,
            "one_point_extension_dimension": W + 1,
            "flat_is_codimension_one_in_extension": True,
            "exact_support_criterion": "phi in Ann(W_E) minus union_(x in E) Ann(W_(E\\{x}))",
            "escape_punctures_are_required": True,
            "error_map_on_E_is_injective": True,
            "injectivity_reason": "|E|=radius<d(C)=K+1",
            "syndrome_map_kernel": "C",
            "syndrome_map_rank": K,
            "syndrome_map_surjective_onto": "(C^perp)^*",
            "base_extension_to_target_field_valid": True,
        },
        "varying_template_composition": {
            "profile_count": PROFILE_COUNT,
            "partial_template_is_positional": True,
            "partial_template_includes_received_values": False,
            "fixed_template_cap_source": "PR_1043",
            "cap_for_v_at_least_512": 1,
            "cap_for_v_at_most_511": "floor(C(1023-u-v,512-v)/C(544-v,512-v))",
            "block_load_condition": "|T intersect Omega_(u,v,P0)|<=c_(u,v)",
            "one_support_determines_at_most_one_codeword_for_fixed_syndrome": True,
            "cofactor_jet_multiplicity_preserved": True,
            "fixed_template_caps_are_ledger_charge": False,
        },
        "separator_theorem": {
            "name": "VT(U)",
            "family_size": "U+1",
            "alternative_VT1": "sum_(E in T) W_E=V",
            "alternative_VT2": "exists E in T,x in E with W_(E\\{x}) subset sum_(F in T)W_F",
            "forward_implication": "VT(U) implies every target-field boundary list has size at most U",
            "converse_implication": "failure of VT1 and VT2 plus q>(U+1)R yields one actual target-field received word with every support in T exact",
            "converse_uses_fixed_template_caps": False,
            "converse_guard_hyperplanes": "at most (U+1)R proper hyperplanes in Ann(sum_E W_E)",
            "zero_syndrome_excluded_separately": True,
            "VT_proved_on_complete_deployed_family": False,
        },
        "union_avoidance": {
            "sufficient_gate": "(U+1)*R<q",
            "inequality_is_strict": True,
            "base_field_max_packet_size": base_union_width,
            "target_field_max_packet_size": str(target_union_width),
            "live_gates": gates,
        },
        "shifted_locator_interface": {
            "coefficient_ambient_dimension": K,
            "locator_degree": RADIUS,
            "shifts_per_support": W,
            "flat_basis": "{X^r L_E:0<=r<w}",
            "common_annihilator_dimension": "K-rank(stacked shifted locators)",
            "escape_rows_appended": W + 1,
            "escape_rank_increment_values": [0, 1],
            "increment_zero_means_VT2_absorption": True,
            "increment_one_means_guard_is_proper": True,
            "automatic_compatibility_max_supports": automatic_width,
            "width_15": {
                "shifted_rows": rows_15,
                "automatic_annihilator_dimension_lower": K - rows_15,
            },
            "width_16": {
                "shifted_rows": rows_16,
                "row_excess_over_ambient": rows_16 - K,
                "compatible_rank_upper": K - 1,
                "compatible_shifted_syzygy_nullity_lower": rows_16 - (K - 1),
            },
        },
        "small_field_fixture": toy_fixture(),
        "external_dependencies": {
            "parent_pr": PARENT_PR,
            "parent_head": PARENT_HEAD,
            "parent_payload_sha256": PARENT_PAYLOAD,
            "fixed_template_pr": FIXED_TEMPLATE_PR,
            "fixed_template_head": FIXED_TEMPLATE_HEAD,
            "fixed_template_payload_sha256": FIXED_TEMPLATE_PAYLOAD,
            "shortened_flat_certificate_sha256": SHORTENED_FLAT_CERTIFICATE,
            "occupancy_atlas_payload_sha256": OCCUPANCY_ATLAS_PAYLOAD,
            "source_adapter_payload_sha256": SOURCE_ADAPTER_PAYLOAD,
            "four_row_payload_sha256": FOUR_ROW_PAYLOAD,
        },
        "chronology": {
            "global_terminal": GLOBAL_TERMINAL,
            "boundary_subterminal": BOUNDARY_SUBTERMINAL,
            "boundary_diagnostic": DIAGNOSTIC,
            "boundary_diagnostic_is_first_match_owner": False,
            "global_terminal_unchanged": True,
            "boundary_subterminal_unchanged": True,
            "active_partition_unchanged": True,
            "owner_paid": False,
        },
        "scope": {
            "object": "LIST",
            "row": "Mersenne-31 list at 2^-100",
            "workboard_item": "M1",
            "unit": "DISTINCT_EXACT_BOUNDARY_SUPPORTS_PER_TARGET_FIELD_SYNDROME",
            "impact": "EXACT_VARYING_TEMPLATE_SEPARATOR_INTERFACE_AND_CONVERSE",
            "ledger_movement": 0,
            "deployed_row_closed": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "nonclaims": {
            "VT_U_proved": False,
            "complete_boundary_paid": False,
            "conditional_boundary_target_paid": False,
            "fixed_template_caps_summed_as_global_bound": False,
            "module_rank_drop_classified": False,
            "high_interior_paid": False,
            "U_Q_paid": False,
            "U_list_int_paid": False,
            "U_ext_paid": False,
            "U_new_paid": False,
            "small_field_fixture_is_deployed_proof": False,
            "official_endpoint_or_score_changed": False,
        },
    }


def build_manifest() -> dict[str, Any]:
    payload = core_payload()
    payload["source_bindings"] = expected_source_bindings()
    return seal(payload)


def source_binding_schema() -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": ["binding_id", "internal_payload_sha256", "path",
                     "role", "scope", "sha256"],
        "properties": {
            "binding_id": {"type": "string", "minLength": 1},
            "internal_payload_sha256": {
                "type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
            "path": {"type": "string", "minLength": 1},
            "role": {"type": "string", "minLength": 1},
            "scope": {"type": "string", "minLength": 1},
            "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
    }


def build_schema() -> dict[str, Any]:
    core = core_payload()
    keys = sorted([*core, "payload_sha256", "source_bindings"])
    properties: dict[str, Any] = {key: {"const": value}
                                  for key, value in core.items()}
    properties["payload_sha256"] = {
        "type": "string", "pattern": "^[0-9a-f]{64}$"}
    properties["source_bindings"] = {
        "type": "array", "minItems": len(SOURCE_SPECS),
        "maxItems": len(SOURCE_SPECS), "uniqueItems": True,
        "items": {"$ref": "#/$defs/sourceBinding"},
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "M31 c=2048 guarded support-flat separator certificate",
        "type": "object", "additionalProperties": False,
        "required": keys, "properties": properties,
        "$defs": {"sourceBinding": source_binding_schema()},
    }


def validate_schema(schema: Any, payload: dict[str, Any]) -> None:
    require(type(schema) is dict, "schema object")
    require(schema == build_schema(), "schema exact replay")
    require(set(schema["required"]) == set(payload), "schema root keys")
    require(set(schema["properties"]) == set(payload), "schema properties")


def verify_payload(candidate: dict[str, Any], *, expected: dict[str, Any]) -> None:
    require(type(candidate) is dict, "manifest object")
    require(type(candidate.get("payload_sha256")) is str, "payload hash type")
    require(candidate.get("payload_sha256") == payload_sha256(candidate),
            "payload hash")
    bindings = candidate.get("source_bindings")
    require(type(bindings) is list and len(bindings) == len(SOURCE_SPECS),
            "source binding count")
    ids = [item.get("binding_id") for item in bindings if type(item) is dict]
    require(len(ids) == len(bindings) and len(set(ids)) == len(ids),
            "source binding IDs unique")
    require(candidate == expected, "manifest exact replay")


def write_artifacts() -> None:
    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_PATH.write_bytes(canonical_json(build_schema()))
    MANIFEST_PATH.write_bytes(canonical_json(build_manifest()))


def set_path(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def mutate(payload: dict[str, Any]) -> None:
        target: Any = payload
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    return mutate


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("target field", set_path(("deployed_parameters", "target_field_size"), str(P))),
        ("radius", set_path(("deployed_parameters", "radius"), RADIUS + 1)),
        ("w", set_path(("deployed_parameters", "w=K-radius"), W - 1)),
        ("distance", set_path(("deployed_parameters", "minimum_distance"), K)),
        ("uniqueness margin", set_path(("deployed_parameters", "strict_uniqueness_margin"), W)),
        ("flat dimension", set_path(("support_flat_interface", "flat_dimension"), W + 1)),
        ("escape dimension", set_path(("support_flat_interface", "one_point_extension_dimension"), W)),
        ("drop punctures", set_path(("support_flat_interface", "escape_punctures_are_required"), False)),
        ("error injection", set_path(("support_flat_interface", "error_map_on_E_is_injective"), False)),
        ("syndrome rank", set_path(("support_flat_interface", "syndrome_map_rank"), K - 1)),
        ("base extension", set_path(("support_flat_interface", "base_extension_to_target_field_valid"), False)),
        ("template values", set_path(("varying_template_composition", "partial_template_includes_received_values"), True)),
        ("template cap", set_path(("varying_template_composition", "cap_for_v_at_least_512"), 2)),
        ("cap charge", set_path(("varying_template_composition", "fixed_template_caps_are_ledger_charge"), True)),
        ("VT1", set_path(("separator_theorem", "alternative_VT1"), "sum W_E proper in V")),
        ("VT2 direction", set_path(("separator_theorem", "alternative_VT2"), "X_T subset W_(E\\{x})")),
        ("converse fixed caps", set_path(("separator_theorem", "converse_uses_fixed_template_caps"), True)),
        ("VT proved", set_path(("separator_theorem", "VT_proved_on_complete_deployed_family"), True)),
        ("union strictness", set_path(("union_avoidance", "inequality_is_strict"), False)),
        ("base union width", set_path(("union_avoidance", "base_field_max_packet_size"), 2_189)),
        ("target union width", set_path(("union_avoidance", "target_field_max_packet_size"), "0")),
        ("conditional U", set_path(("union_avoidance", "live_gates", 0, "U"), BOUNDARY_TARGET - 1)),
        ("conditional packet", set_path(("union_avoidance", "live_gates", 0, "packet_size"), BOUNDARY_TARGET)),
        ("conditional guards", set_path(("union_avoidance", "live_gates", 0, "guard_hyperplane_upper"), 9_042_852_106_877)),
        ("post-low guards", set_path(("union_avoidance", "live_gates", 1, "guard_hyperplane_upper"), 16_456_953_545_693)),
        ("full guards", set_path(("union_avoidance", "live_gates", 2, "guard_hyperplane_upper"), 16_460_613_156_863)),
        ("base-field global gate", set_path(("union_avoidance", "live_gates", 2, "base_field_gate_holds"), True)),
        ("15 rows", set_path(("shifted_locator_interface", "width_15", "shifted_rows"), 1_011_704)),
        ("15 annihilator", set_path(("shifted_locator_interface", "width_15", "automatic_annihilator_dimension_lower"), 36_870)),
        ("16 excess", set_path(("shifted_locator_interface", "width_16", "row_excess_over_ambient"), 30_575)),
        ("16 nullity", set_path(("shifted_locator_interface", "width_16", "compatible_shifted_syzygy_nullity_lower"), 30_576)),
        ("escape append", set_path(("shifted_locator_interface", "escape_rows_appended"), W)),
        ("rank absorption", set_path(("shifted_locator_interface", "increment_zero_means_VT2_absorption"), False)),
        ("toy rank 15", set_path(("small_field_fixture", "first_15_shifted_rank"), 29)),
        ("toy rank 16", set_path(("small_field_fixture", "all_16_shifted_rank"), 31)),
        ("toy annihilator", set_path(("small_field_fixture", "annihilator_functional"), "coefficient_28")),
        ("toy escape count", set_path(("small_field_fixture", "one_point_escape_count"), 463)),
        ("toy union margin", set_path(("small_field_fixture", "union_margin"), 4_024)),
        ("toy negative", set_path(("small_field_fixture", "negative_shifted_rank"), 30)),
        ("parent head", set_path(("external_dependencies", "parent_head"), "0" * 40)),
        ("parent payload", set_path(("external_dependencies", "parent_payload_sha256"), "0" * 64)),
        ("fixed-template payload", set_path(("external_dependencies", "fixed_template_payload_sha256"), "0" * 64)),
        ("shortened-flat pin", set_path(("external_dependencies", "shortened_flat_certificate_sha256"), "0" * 64)),
        ("occupancy pin", set_path(("external_dependencies", "occupancy_atlas_payload_sha256"), "0" * 64)),
        ("source-adapter pin", set_path(("external_dependencies", "source_adapter_payload_sha256"), "0" * 64)),
        ("four-row pin", set_path(("external_dependencies", "four_row_payload_sha256"), "0" * 64)),
        ("global terminal", set_path(("chronology", "global_terminal"), "PAID")),
        ("boundary subterminal", set_path(("chronology", "boundary_subterminal"), "PAID")),
        ("diagnostic owner", set_path(("chronology", "boundary_diagnostic_is_first_match_owner"), True)),
        ("owner paid", set_path(("chronology", "owner_paid"), True)),
        ("ledger movement", set_path(("scope", "ledger_movement"), 1)),
        ("row closure", set_path(("scope", "deployed_row_closed"), True)),
        ("global payment", set_path(("nonclaims", "complete_boundary_paid"), True)),
        ("toy promotion", set_path(("nonclaims", "small_field_fixture_is_deployed_proof"), True)),
    ]


def check() -> None:
    expected = build_manifest()
    manifest = strict_json_path(MANIFEST_PATH, canonical=True)
    schema = strict_json_path(SCHEMA_PATH, canonical=True)
    verify_payload(manifest, expected=expected)
    validate_schema(schema, manifest)
    print(
        "PASS: M31 c=2048 guarded support-flat separator interface; "
        f"live_gates={len(expected['union_avoidance']['live_gates'])}, "
        f"toy_escapes={expected['small_field_fixture']['one_point_escape_count']}, "
        f"checks={CHECKS}"
    )


def tamper_selftest() -> None:
    expected = build_manifest()
    rejected = 0
    for label, mutate in mutation_cases():
        forged = copy.deepcopy(expected)
        mutate(forged)
        forged = seal(forged)
        try:
            verify_payload(forged, expected=expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"semantic mutation accepted: {label}")
    malformed = [
        b'{"a":1,"a":2}\n', b'{"x":1.0}\n', b'{"x":NaN}\n',
        b'{"x":"\xc3\xa9"}\n', b'{"x":1}',
    ]
    for raw in malformed:
        try:
            strict_json_bytes(raw, canonical=True)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("malformed JSON mutation accepted")
    total = len(mutation_cases()) + len(malformed)
    require(rejected == total, "all mutations rejected")
    print(f"PASS: rejected {rejected}/{total} mutations; checks={CHECKS}")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.write:
        write_artifacts()
        check()
    elif args.tamper_selftest:
        tamper_selftest()
    else:
        check()


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
