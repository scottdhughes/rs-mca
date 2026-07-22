#!/usr/bin/env python3
"""Verify the M31 c=2048 multiprefix / 30-carrier activation packet.

The replay is standard-library-only and exact.  It checks the deployed
fixed-multipartial source theorem, exhausts every feasible occupancy profile,
verifies the fixed-remainder multiprefix obstruction (including a GF(17)
fixture), binds the packet sources, and rejects semantic mutations.

It proves route cuts and source floors.  It does not prove a C1 or carrier
upper payment and does not close the M31 list row.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable


SCHEMA_ID = "rs-mca-c2048-multiprefix-30carrier-activation-v1"
ARCHITECTURE_ID = "M31_C2048_MULTIPREFIX_30CARRIER_ACTIVATION_ROUTE_CUT_V1"
STATUS = "PROVED_MULTIPREFIX_ROUTE_CUT_AND_30CARRIER_ACTIVATION_ROW_OPEN"
OLD_TERMINAL = "M31_C2048_BIDEEP_30COLUMN_OWNER"
NEW_TERMINAL = "M31_C2048_FIXED_SYNDROME_MULTIPREFIX_FACE_CARRIER_OWNER"

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
B_STAR = P**4 // 2**100

C = 2_048
FIBERS = N // C
ERROR_QUOTIENT = RADIUS // C
ERROR_REMAINDER = RADIUS % C
AGREEMENT_QUOTIENT = AGREEMENT // C
AGREEMENT_REMAINDER = AGREEMENT % C
QUOTIENT_PREFIX_DEPTH = W // C

PREDECESSOR_PAYLOAD = "c312bd2c108634af51cd351a004cdb2942bc10a145eca3e49dbcfe8fe8873a7c"
FIXED_REMAINDER_PAYLOAD = "056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7"
LOGICAL_C1_HEAD = "a843a8f7930054617ef1d94169a4a9d3422cb909"
UPSTREAM_MAIN = "32a41660e3088eeeb15a16645330856794302ff0"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_c2048_multiprefix_30carrier_activation_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_c2048_multiprefix_30carrier_activation_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_c2048_multiprefix_30carrier_activation_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_c2048_multiprefix_30carrier_activation_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the multiprefix/carrier-activation certificate."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Primary exact profile census, constructions, hashes, and mutations."),
    ("packet_sage", SAGE_PATH, None,
     "Independent finite-field source and multiprefix constructions."),
    ("packet_note", NOTE_PATH, None,
     "Symbolic fixed-template theorem, deployed source, and adapter route cut."),
    ("packet_readme", README_PATH, None,
     "Replay, dependency, and nonclaim contract."),
    ("predecessor_30carrier_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json",
     "payload_sha256", "Sealed immediate predecessor #1040 packet."),
    ("fixed_remainder_source_manifest",
     ROOT / "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json",
     "payload_sha256", "Sealed fixed-remainder source packet #1039."),
    ("exact_prefix_and_qr_source", ROOT / "experimental/rs_mca_thresholds.tex",
     None, "Exact prefix-list bijection and quotient-remainder normal form."),
    ("paving_qr_source", ROOT / "RS_MCA_Paving_v9.2.tex",
     None, "Root-level exact QR theorem and deployed algebraic basis."),
    ("target_field_source_adapter",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Arbitrary-word target-field exact-layer and five-atom chronology."),
    ("coupled_subpacket_theorem",
     ROOT / "experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md",
     None, "Field-generic arbitrary-subpacket kernel and 30-column theorem."),
    ("active_v4_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active nonnegative five-atom LIST chronology."),
    ("admissibility_authority",
     ROOT / "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex",
     None, "Non-oracular first-match and attained-image requirements."),
)


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def ceil_div(a: int, b: int) -> int:
    require(type(a) is int and type(b) is int and a >= 0 and b > 0,
            "ceil-div domain")
    return (a + b - 1) // b


def canonical_json(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (encoded + "\n").encode("ascii")


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
    value = strict_json_path(path, canonical=True)
    require(type(value) is dict, f"internal manifest object: {path}")
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
        if role == "predecessor_30carrier_manifest":
            require(internal == PREDECESSOR_PAYLOAD, "exact #1040 payload")
        if role == "fixed_remainder_source_manifest":
            require(internal == FIXED_REMAINDER_PAYLOAD, "exact #1039 payload")
        result.append({
            "binding_id": f"M31_C2048_MULTIPREFIX::{role}",
            "path": relative.as_posix(),
            "role": role,
            "scope": scope,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
        })
    return result


def feasible_profiles() -> list[tuple[int, int]]:
    profiles: list[tuple[int, int]] = []
    for u in range(480):
        vmax = 136 if u == 0 else 544
        for v in range(vmax + 1):
            h = u + v + 1
            r_err = ERROR_REMAINDER + C * u
            r_agr = AGREEMENT_REMAINDER + C * v
            require(r_err + r_agr == C * h, "profile color sum")
            require(h <= r_err <= h * (C - 1), "profile error feasibility")
            require(h <= r_agr <= h * (C - 1), "profile agreement feasibility")
            profiles.append((u, v))
    require(len(profiles) == 261_192, "profile count")
    require(len(set(profiles)) == len(profiles), "profile uniqueness")
    return profiles


def deterministic_partial_sizes(h: int, total: int) -> list[int]:
    require(h >= 1 and h <= total <= h * (C - 1), "partial-size feasibility")
    sizes = [1] * h
    remaining = total - h
    for i in range(h):
        take = min(C - 2, remaining)
        sizes[i] += take
        remaining -= take
    require(remaining == 0, "partial-size completion")
    require(sum(sizes) == total, "partial-size sum")
    require(all(1 <= x <= C - 1 for x in sizes), "partial-size bounds")
    return sizes


def profile_source_row(u: int, v: int) -> tuple[int, ...]:
    h = u + v + 1
    full_agreement = AGREEMENT_QUOTIENT - v
    partial_agreement = AGREEMENT_REMAINDER + C * v
    available = FIBERS - h
    t = min(QUOTIENT_PREFIX_DEPTH, full_agreement)
    require(partial_agreement + C * full_agreement == AGREEMENT,
            "source profile agreement size")
    require(full_agreement <= available, "source quotient availability")
    deterministic_partial_sizes(h, partial_agreement)
    candidates = math.comb(available, full_agreement)
    floor = ceil_div(candidates, P**t)
    if t < full_agreement:
        degree_bound = partial_agreement + C * (full_agreement - t - 1)
        require(degree_bound == AGREEMENT - C * (t + 1),
                "source degree cancellation")
        require(degree_bound < K, "source codeword degree gate")
    else:
        degree_bound = -1
        require(candidates < P**t or candidates == 1,
                "full coefficient bucket floor one")
        require(floor == 1, "full coefficient source floor")
    return (u, v, h, full_agreement, partial_agreement, available, t,
            degree_bound, candidates, floor)


def profile_census() -> dict[str, Any]:
    digest = hashlib.sha256()
    activated: list[tuple[int, int, int]] = []
    all_rows = []
    for u, v in feasible_profiles():
        row = profile_source_row(u, v)
        all_rows.append(row)
        digest.update((",".join(str(x) for x in row) + "\n").encode("ascii"))
        if row[-1] >= 30:
            activated.append((u, v, row[-1]))

    faces = [row for row in activated if row[0] == 0 or row[1] == 0]
    bideep = [row for row in activated if row[0] >= 1 and row[1] >= 1]
    require(len(activated) == 177, "activated profile count")
    require(len(faces) == 36, "activated face count")
    require(len(bideep) == 141, "activated bi-deep count")
    width_30 = []
    width_29 = []
    optimized_activations = []
    for row in all_rows:
        u, v, *_rest, floor = row
        if u < 1 or v < 1:
            continue
        index_sum_upper = 2 * RADIUS - K - 1 - (ERROR_REMAINDER + C * u)
        q_min = next(
            q for q in range(4, 1_025)
            if (2 * index_sum_upper) // (q - 2) < W
        )
        if floor >= q_min:
            optimized_activations.append((u, v, floor, q_min))
            if q_min == 30:
                width_30.append((u, v, floor))
            elif q_min == 29:
                width_29.append((u, v, floor))
            else:
                raise VerificationError(f"unexpected activated width q={q_min}")
    require(len(width_30) == 18, "source-specific 30-column profiles")
    require(len(width_29) == 124, "source-specific 29-column profiles")
    require(len(optimized_activations) == 142,
            "optimized source-threshold activation count")
    require({q: sum(1 for *_row, qq in optimized_activations if qq == q)
             for q in {qq for *_row, qq in optimized_activations}}
            == {29: 124, 30: 18}, "optimized threshold histogram")
    require(not any(floor < 29 for _u, _v, floor, _q in optimized_activations),
            "no lower-floor optimized activation")
    require([row for row in width_29 if row[2] == 29] == [(8, 10, 29)],
            "extra source-specific 29-column profile")
    require(max(activated, key=lambda row: row[2]) == (0, 0, 6_796_405),
            "global structured maximum")
    require(max(bideep, key=lambda row: row[2]) == (1, 1, 1_693_898),
            "bi-deep structured maximum")

    frontier = []
    expected_last_floors = [33, 30, 51, 46, 41, 37, 33, 54, 48, 42,
                            37, 32, 51, 44, 38]
    expected_vmax = [18, 17, 15, 14, 13, 12, 11, 9, 8, 7, 6, 5, 3, 2, 1]
    for u, expected_v, expected_floor in zip(
            range(1, 16), expected_vmax, expected_last_floors, strict=True):
        rows = [(v, floor) for uu, v, floor in bideep if uu == u]
        require(rows and rows[-1] == (expected_v, expected_floor),
                f"activation frontier u={u}")
        require(rows == [(v, profile_source_row(u, v)[-1])
                         for v in range(1, expected_v + 1)],
                f"activation row contiguous u={u}")
        frontier.append({"u": u, "max_v": expected_v,
                         "floor_at_max_v": expected_floor})
    require(not any(u >= 16 for u, _v, _floor in bideep),
            "no later activated bi-deep row")

    row_11 = profile_source_row(1, 1)
    require(row_11[2:8] == (3, 543, 3_959, 1_021, 32, 1_048_439),
            "profile (1,1) source data")
    require(row_11[-1] == 1_693_898, "profile (1,1) source floor")
    require(profile_source_row(0, 0)[-1] == 6_796_405,
            "predecessor floor specialization")

    return {
        "profile_count": len(all_rows),
        "profile_rows_sha256": digest.hexdigest(),
        "activated_profile_count": len(activated),
        "activated_face_count": len(faces),
        "activated_bideep_count": len(bideep),
        "activated_width_30_count": len(width_30),
        "activated_width_29_count": len(width_29),
        "certified_source_threshold_bideep_count": len(width_30) + len(width_29),
        "certified_minimum_width_histogram": {"29": 124, "30": 18},
        "minimum_certified_source_floor": 29,
        "extra_width_29_profile": {"u": 8, "v": 10, "source_floor": 29},
        "global_maximum": {"u": 0, "v": 0, "source_floor": 6_796_405},
        "bideep_maximum": {"u": 1, "v": 1,
                            "source_floor": 1_693_898},
        "bideep_frontier": frontier,
    }


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def poly_sub(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0)
                  - (b[i] if i < len(b) else 0)) % p
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_eval(a: list[int], x: int, p: int) -> int:
    value = 0
    for coeff in reversed(a):
        value = (value * x + coeff) % p
    return value


def locator(points: set[int] | tuple[int, ...], p: int) -> list[int]:
    result = [1]
    for point in sorted(points):
        result = poly_mul(result, [(-point) % p, 1], p)
    return result


def locator_prefix(points: set[int], width: int, p: int) -> list[int]:
    coeffs = locator(points, p)
    require(len(coeffs) >= width + 1 and coeffs[-1] == 1,
            "monic locator prefix")
    return [coeffs[-2 - i] for i in range(width)]


def toy_multiprefix_obstruction() -> dict[str, Any]:
    p = 17
    domain = set(range(1, 17))
    s1 = {1, 2, 3, 4, 9, 13, 14, 15, 16}
    s2 = {1, 5, 6, 7, 9, 10, 11, 12, 16}
    intersection = s1 & s2
    omitted = domain - (s1 | s2)
    require(intersection == {1, 9, 16}, "toy support intersection")
    require(omitted == {8}, "toy omitted remainder")
    g = locator(intersection, p)
    require(g == [9, 16, 8, 1], "toy bridge polynomial")
    require(len(g) - 1 == 3 < 7, "toy bridge degree")

    values = {}
    for x in sorted(domain):
        gx = poly_eval(g, x, p)
        if x in s1:
            values[x] = 0
        elif x in s2:
            values[x] = gx
        else:
            values[x] = 1
            require(values[x] not in {0, gx}, "toy outside avoidance")
    agreement_zero = {x for x in domain if values[x] == 0}
    agreement_g = {x for x in domain if values[x] == poly_eval(g, x, p)}
    require(agreement_zero == s1, "toy exact zero agreement")
    require(agreement_g == s2, "toy exact g agreement")
    agr_prefixes = [locator_prefix(s1, 2, p), locator_prefix(s2, 2, p)]
    err_prefixes = [locator_prefix(domain - s1, 2, p),
                    locator_prefix(domain - s2, 2, p)]
    require(agr_prefixes == [[8, 4], [8, 8]], "toy agreement prefixes")
    require(err_prefixes == [[9, 9], [9, 5]], "toy error prefixes")
    return {
        "field": 17,
        "domain": list(range(1, 17)),
        "dimension": 7,
        "agreement": 9,
        "radius": 7,
        "prefix_depth": 2,
        "common_agreement_remainder": [9],
        "common_error_remainder": [8],
        "intersection": sorted(intersection),
        "bridge_polynomial_ascending": g,
        "agreement_prefixes": agr_prefixes,
        "error_prefixes": err_prefixes,
        "received_word": [values[x] for x in range(1, 17)],
        "exact_agreement_sets": [sorted(s1), sorted(s2)],
    }


def toy_fixed_template_source() -> dict[str, Any]:
    p = 17
    domain = set(range(1, 17))
    phi = lambda x: x * x % p
    quotient = sorted({phi(x) for x in domain})
    partial = {1, 2, 3}
    partial_labels = {phi(x) for x in partial}
    available = [b for b in quotient if b not in partial_labels]
    require(len(quotient) == 8 and len(available) == 5,
            "toy quotient counts")
    lp = locator(partial, p)
    # U=L_P*(X^2)^3=L_P*X^6.  Coefficients are ascending.
    center = [0] * 6 + lp
    supports = []
    codewords = []
    for e in itertools.combinations(available, 3):
        full_points = {x for x in domain if phi(x) in e}
        support = partial | full_points
        le = locator(support, p)
        codeword = poly_sub(center, le, p)
        require(len(codeword) - 1 < 8, "toy source codeword degree")
        require({x for x in domain
                 if poly_eval(center, x, p) == poly_eval(codeword, x, p)}
                == support, "toy source exact agreement")
        supports.append(tuple(sorted(support)))
        codewords.append(tuple(codeword))
    require(len(supports) == 10 and len(set(supports)) == 10,
            "toy source support count")
    require(len(set(codewords)) == 10, "toy source codeword count")
    require(all(len(s) == 9 for s in supports), "toy source agreement size")
    return {
        "field": 17,
        "domain_size": 16,
        "dimension": 8,
        "agreement": 9,
        "radius": 7,
        "fold": "X^2",
        "fiber_count": 8,
        "partial_fiber_count": 3,
        "partial_template": sorted(partial),
        "available_quotient_labels": available,
        "full_agreement_fibers": 3,
        "quotient_prefix_depth": 0,
        "candidate_and_codeword_count": 10,
        "degree_bound": 7,
        "boundary_only": True,
    }


def build_manifest() -> dict[str, Any]:
    census = profile_census()
    intersection = 65 * C + AGREEMENT_REMAINDER
    require(65 + 479 + 479 + 1 == FIBERS,
            "multiprefix quotient partition")
    require(intersection == 135_031 < K,
            "multiprefix bridge degree")
    require(AGREEMENT_REMAINDER + ERROR_REMAINDER == C,
            "common partial-fiber split")
    require(AGREEMENT_QUOTIENT == 65 + 479,
            "agreement quotient size")
    require(ERROR_QUOTIENT == 479, "error quotient size")
    require(P % 2 == 1 and P > 2, "unequal-sum swap field gate")
    require(QUOTIENT_PREFIX_DEPTH == 32, "deployed quotient prefix depth")
    source_core_11 = ERROR_REMAINDER + C
    source_sum_11 = 2 * RADIUS - K - 1 - source_core_11
    source_two_row_30 = 2 * source_sum_11 // 28
    source_two_row_29_u1 = 2 * source_sum_11 // 27
    source_core_u2 = ERROR_REMAINDER + 2 * C
    source_two_row_29_u2 = 2 * (2 * RADIUS - K - 1 - source_core_u2) // 27
    require(source_core_11 == 2_185, "profile (1,1) fixed error core")
    require(source_sum_11 == 911_496, "profile (1,1) index sum")
    require(source_two_row_30 == 65_106 < W,
            "profile (1,1) sharpened carrier")
    require(source_two_row_29_u1 == 67_518 > W,
            "u=1 29-column noncertificate")
    require(source_two_row_29_u2 == 67_366 < W,
            "u=2 sharpened 29-column carrier")

    payload = {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "scope": {
            "workboard_item": "M1",
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "field": "GF((2^31-1)^4) with constructions over GF(2^31-1)",
            "unit": "DISTINCT_EXACT_BOUNDARY_CODEWORDS_PER_RECEIVED_WORD",
            "impact": "NEW_BIDEEP_PROFILE_FLOOR_AND_ROUTE_COUNTEREXAMPLE",
            "deployed_row_closed": False,
            "ledger_movement": 0,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "deployed_parameters": {
            "p": P, "n": N, "K": K, "agreement": AGREEMENT,
            "radius": RADIUS, "prefix_depth": W, "B_star": B_STAR,
            "fold_degree": C, "fiber_count": FIBERS,
            "error_quotient": ERROR_QUOTIENT,
            "error_remainder": ERROR_REMAINDER,
            "agreement_quotient": AGREEMENT_QUOTIENT,
            "agreement_remainder": AGREEMENT_REMAINDER,
            "quotient_prefix_depth": QUOTIENT_PREFIX_DEPTH,
        },
        "fixed_multipartial_source": {
            "formula": "ceil(binomial(1023-u-v,544-v)/p^min(32,544-v))",
            "partial_fiber_count": "h=u+v+1",
            "full_agreement_fibers": "f=544-v",
            "partial_agreement_size": "r=1911+2048v",
            "available_quotient_labels": "1023-u-v",
            "uniform_degree_bound_for_f_gt_32": 1_048_439,
            "degree_margin_below_K": 137,
            "construction_is_one_received_word_per_profile": True,
            "construction_combines_profiles_in_one_word": False,
            "complete_target_field_ball_boundary_only": True,
            "complete_target_field_ball_base_field_valued": True,
            **census,
        },
        "carrier_activation": {
            "old_route_terminal": OLD_TERMINAL,
            "profile_u": 1,
            "profile_v": 1,
            "partial_fibers": 3,
            "full_agreement_fibers": 543,
            "partial_agreement_points": 3_959,
            "available_quotient_labels": 1_021,
            "candidate_quotient_sets": str(math.comb(1_021, 543)),
            "quotient_prefix_buckets": str(P**32),
            "certified_codeword_floor": 1_693_898,
            "carrier_columns": 30,
            "fixed_error_core_size": source_core_11,
            "source_specific_joint_index_sum_upper": source_sum_11,
            "source_specific_two_row_degree_upper": source_two_row_30,
            "generic_two_row_degree_upper": 65_262,
            "boundary_cutoff": 67_447,
            "activated_width_30_profile_count": 18,
            "activated_width_29_profile_count": 124,
            "certified_source_threshold_bideep_profile_count": 142,
            "extra_width_29_profile": [8, 10, 29],
            "width_29_first_u": 2,
            "width_29_u1_two_row_degree_upper": source_two_row_29_u1,
            "width_29_u1_not_certified": True,
            "width_29_u2_two_row_degree_upper": source_two_row_29_u2,
            "width_29_uses_fixed_error_core": True,
            "universal_profile_cap_29_false": True,
            "carrier_nonexistence_route_false": True,
            "carrier_owner_paid": False,
        },
        "single_prefix_obstruction": {
            "profile": [0, 0],
            "common_partial_fiber": True,
            "common_agreement_remainder_size": 1_911,
            "common_error_remainder_size": 137,
            "common_quotient_labels": 65,
            "first_private_quotient_labels": 479,
            "second_private_quotient_labels": 479,
            "quotient_partition_exhaustive": True,
            "unequal_private_label_sums_exist": True,
            "agreement_intersection_size": intersection,
            "bridge_polynomial_degree": intersection,
            "bridge_polynomial_is_codeword": True,
            "outside_points": 137,
            "exact_boundary_codewords": 2,
            "agreement_locator_prefixes_distinct": True,
            "error_locator_prefixes_distinct": True,
            "common_codeword_translation_changes_supports": False,
            "common_codeword_translation_changes_locator_prefixes": False,
            "literal_support_preserving_locator_prefix_identification_exists": False,
            "non_support_preserving_adapter_ruled_out": False,
            "coarser_attained_target_adapter_ruled_out": False,
            "logical_C1_dependency_head": LOGICAL_C1_HEAD,
        },
        "arbitrary_word_pade_representation": {
            "identity": "Y-P=L_S*H",
            "codeword_degree_upper": K - 1,
            "H_degree_upper": RADIUS - 1,
            "exactness_condition": "H(x)!=0 for x in D\\S",
            "translation_preserves_L_S_and_H": True,
            "canonical_prefix_center_H": "1",
            "separate_recentering_preserves_common_received_word": False,
            "correct_aggregate": "sum_z N_y^C1(z)",
            "insufficient_bound_without_target_count": "max_z N_y^C1(z)",
        },
        "chronology": {
            "boundary_diagnostic_subterminal": NEW_TERMINAL,
            "parent_atom": "U_new",
            "parent_cell": "HIGH_BOUNDARY_EXACT_CODEWORD",
            "active_partition_replaced": False,
            "C1_numerical_payment_proved": False,
            "carrier_owner_paid": False,
            "conditional_boundary_allowance": 9_216_781,
            "high_interior_paid": False,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "high_U_new": None,
            "upstream_main_at_preparation": UPSTREAM_MAIN,
        },
        "toy_controls": {
            "fixed_template_source": toy_fixed_template_source(),
            "fixed_remainder_multiprefix": toy_multiprefix_obstruction(),
        },
        "external_dependencies": {
            "mechanical_parent": "PR #1040 exact head 02b1b8195a9f219a110ce255b205a3e8aed26956",
            "logical_C1_dependency": f"PR #1032 exact head {LOGICAL_C1_HEAD}",
            "open_PR_duplicate_found": False,
            "rebase_needed_at_preparation": False,
        },
        "nonclaims": {
            "M31_list_row_closed": False,
            "C1_upper_payment_proved": False,
            "carrier_upper_payment_proved": False,
            "all_30_frames_share_partial_template": False,
            "profile_source_floors_are_simultaneously_attained": False,
            "sum_over_prefix_targets_bounded": False,
            "high_interior_bound_proved": False,
            "official_endpoint_or_score_changed": False,
            "direct_M31_row_counterexample_proved": False,
            "global_numerator_floor_proved": False,
            "universal_arbitrary_word_carrier_theorem_proved": False,
            "active_partition_or_global_terminal_replaced": False,
        },
        "source_bindings": expected_source_bindings(),
    }
    return seal(payload)


def validate_schema_subset(schema: Any, payload: dict[str, Any]) -> None:
    require(type(schema) is dict, "schema object")
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
            "schema dialect")
    require(schema.get("$id") == SCHEMA_ID, "schema id")
    require(schema.get("type") == "object", "schema root object")
    require(schema.get("additionalProperties") is False,
            "schema rejects root extras")
    required = schema.get("required")
    require(type(required) is list and set(required) == set(payload),
            "schema exact root keys")
    properties = schema.get("properties")
    require(type(properties) is dict and set(properties) == set(payload),
            "schema root properties")
    for key, value in payload.items():
        if key in {"payload_sha256", "source_bindings"}:
            continue
        require(properties[key] == {"const": value},
                f"schema exact const {key}")
    require(properties["payload_sha256"] == {
        "type": "string", "pattern": "^[0-9a-f]{64}$"},
        "schema payload contract")
    require(properties["source_bindings"] == {
        "type": "array", "minItems": len(SOURCE_SPECS),
        "maxItems": len(SOURCE_SPECS), "uniqueItems": True,
        "items": {"$ref": "#/$defs/sourceBinding"}},
        "schema source-binding array")
    expected_binding = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "binding_id", "internal_payload_sha256", "path", "role",
            "scope", "sha256"],
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
    defs = schema.get("$defs")
    require(type(defs) is dict and defs == {"sourceBinding": expected_binding},
            "schema exact source-binding definition")


def verify_payload(candidate: dict[str, Any], *, compare_expected: bool = True,
                   expected: dict[str, Any] | None = None) -> None:
    require(type(candidate) is dict, "manifest object")
    require(type(candidate.get("payload_sha256")) is str,
            "payload hash type")
    require(candidate.get("payload_sha256") == payload_sha256(candidate),
            "payload hash")
    bindings = candidate.get("source_bindings")
    require(type(bindings) is list and len(bindings) == len(SOURCE_SPECS),
            "source binding count")
    ids = [item.get("binding_id") for item in bindings if type(item) is dict]
    require(len(ids) == len(bindings) and len(set(ids)) == len(ids),
            "source binding IDs unique")
    if compare_expected:
        if expected is None:
            expected = build_manifest()
        require(candidate == expected, "manifest exact replay")


def write_manifest() -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_bytes(canonical_json(build_manifest()))


def mutation_cases(base: dict[str, Any]) -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("p", lambda x: x["deployed_parameters"].__setitem__("p", P - 2)),
        ("dimension", lambda x: x["deployed_parameters"].__setitem__("K", K + 1)),
        ("agreement", lambda x: x["deployed_parameters"].__setitem__("agreement", AGREEMENT - 1)),
        ("source formula", lambda x: x["fixed_multipartial_source"].__setitem__("formula", "wrong")),
        ("degree gate", lambda x: x["fixed_multipartial_source"].__setitem__("uniform_degree_bound_for_f_gt_32", K)),
        ("target-field base descent", lambda x: x["fixed_multipartial_source"].__setitem__("complete_target_field_ball_base_field_valued", False)),
        ("profile count", lambda x: x["fixed_multipartial_source"].__setitem__("profile_count", 261_191)),
        ("activation total", lambda x: x["fixed_multipartial_source"].__setitem__("activated_profile_count", 176)),
        ("activation bi-deep", lambda x: x["fixed_multipartial_source"].__setitem__("activated_bideep_count", 140)),
        ("29-width count", lambda x: x["fixed_multipartial_source"].__setitem__("activated_width_29_count", 123)),
        ("source-threshold certificate count", lambda x: x["fixed_multipartial_source"].__setitem__("certified_source_threshold_bideep_count", 141)),
        ("certified width histogram", lambda x: x["fixed_multipartial_source"]["certified_minimum_width_histogram"].__setitem__("28", 1)),
        ("profile digest", lambda x: x["fixed_multipartial_source"].__setitem__("profile_rows_sha256", "0" * 64)),
        ("carrier floor", lambda x: x["carrier_activation"].__setitem__("certified_codeword_floor", 29)),
        ("carrier core", lambda x: x["carrier_activation"].__setitem__("fixed_error_core_size", 2_184)),
        ("carrier sharpened sum", lambda x: x["carrier_activation"].__setitem__("source_specific_joint_index_sum_upper", 911_497)),
        ("29-column bound", lambda x: x["carrier_activation"].__setitem__("width_29_u2_two_row_degree_upper", 67_447)),
        ("u1 29-column guard", lambda x: x["carrier_activation"].__setitem__("width_29_u1_not_certified", False)),
        ("carrier owner", lambda x: x["carrier_activation"].__setitem__("carrier_owner_paid", True)),
        ("cap 29", lambda x: x["carrier_activation"].__setitem__("universal_profile_cap_29_false", False)),
        ("J size", lambda x: x["single_prefix_obstruction"].__setitem__("common_quotient_labels", 64)),
        ("intersection", lambda x: x["single_prefix_obstruction"].__setitem__("agreement_intersection_size", K)),
        ("equal sums", lambda x: x["single_prefix_obstruction"].__setitem__("unequal_private_label_sums_exist", False)),
        ("agreement prefix", lambda x: x["single_prefix_obstruction"].__setitem__("agreement_locator_prefixes_distinct", False)),
        ("error prefix", lambda x: x["single_prefix_obstruction"].__setitem__("error_locator_prefixes_distinct", False)),
        ("translation", lambda x: x["single_prefix_obstruction"].__setitem__("common_codeword_translation_changes_locator_prefixes", True)),
        ("literal locator-prefix identification", lambda x: x["single_prefix_obstruction"].__setitem__("literal_support_preserving_locator_prefix_identification_exists", True)),
        ("overclaim", lambda x: x["single_prefix_obstruction"].__setitem__("non_support_preserving_adapter_ruled_out", True)),
        ("coarser-target overclaim", lambda x: x["single_prefix_obstruction"].__setitem__("coarser_attained_target_adapter_ruled_out", True)),
        ("H bound", lambda x: x["arbitrary_word_pade_representation"].__setitem__("H_degree_upper", RADIUS)),
        ("H invariance", lambda x: x["arbitrary_word_pade_representation"].__setitem__("translation_preserves_L_S_and_H", False)),
        ("aggregate", lambda x: x["arbitrary_word_pade_representation"].__setitem__("correct_aggregate", "max_z N_y^C1(z)")),
        ("terminal", lambda x: x["chronology"].__setitem__("boundary_diagnostic_subterminal", OLD_TERMINAL)),
        ("parent atom", lambda x: x["chronology"].__setitem__("parent_atom", "U_Q")),
        ("active partition", lambda x: x["chronology"].__setitem__("active_partition_replaced", True)),
        ("C1 paid", lambda x: x["chronology"].__setitem__("C1_numerical_payment_proved", True)),
        ("interior paid", lambda x: x["chronology"].__setitem__("high_interior_paid", True)),
        ("ledger movement", lambda x: x["scope"].__setitem__("ledger_movement", 1)),
        ("row closed", lambda x: x["scope"].__setitem__("deployed_row_closed", True)),
        ("universal carrier", lambda x: x["nonclaims"].__setitem__("universal_arbitrary_word_carrier_theorem_proved", True)),
        ("simultaneous profiles", lambda x: x["nonclaims"].__setitem__("profile_source_floors_are_simultaneously_attained", True)),
        ("duplicate source", lambda x: x["source_bindings"].__setitem__(1, copy.deepcopy(x["source_bindings"][0]))),
        ("drop source", lambda x: x["source_bindings"].pop()),
        ("source hash", lambda x: x["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("extra root key", lambda x: x.__setitem__("unexpected", 1)),
        ("payload", lambda x: x.__setitem__("payload_sha256", "0" * 64)),
    ]


def run_tamper_selftest() -> int:
    base = build_manifest()
    rejected = 0
    for label, mutate in mutation_cases(base):
        bad = copy.deepcopy(base)
        mutate(bad)
        bad = seal(bad) if label != "payload" else bad
        try:
            verify_payload(bad, expected=base)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {label}")

    malformed = [
        b'{"a":1,"a":2}\n',
        b'{"x":1.5}\n',
        b'{"x":NaN}\n',
        '{"x":"é"}\n'.encode("utf-8"),
    ]
    for raw in malformed:
        try:
            strict_json_bytes(raw)
        except (VerificationError, json.JSONDecodeError):
            rejected += 1
        else:
            raise VerificationError("malformed JSON accepted")
    print(f"PASS: rejected {rejected}/{len(mutation_cases(base)) + len(malformed)} mutations; checks={CHECKS}")
    return 0


def run_check() -> int:
    candidate = strict_json_path(MANIFEST_PATH, canonical=True)
    require(type(candidate) is dict, "manifest root")
    verify_payload(candidate)
    schema = strict_json_path(SCHEMA_PATH)
    validate_schema_subset(schema, candidate)
    print(f"PASS: profiles=261192 floor30=177 bi-deep-floor30=141 source-threshold-certified=142 floor(1,1)=1693898 checks={CHECKS}")
    print(f"payload_sha256={candidate['payload_sha256']}")
    print(f"route_terminal={NEW_TERMINAL}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_manifest()
            print(f"WROTE {MANIFEST_PATH}")
            return 0
        if args.tamper_selftest:
            return run_tamper_selftest()
        return run_check()
    except (VerificationError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
