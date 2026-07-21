#!/usr/bin/env python3
"""Verify the M31 Chebyshev fixed-remainder C1 boundary-source packet.

The symbolic lemma is a polynomial-fold locator-prefix argument.  This exact
replay pins the deployed integers, exhausts a GF(17) control, replays the
moving-cutoff packing optimizer, and guards the chronology/nonclaim contract.
It does not prove a row-sharp Q upper bound or close the M31 list row.
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
from typing import Any, Sequence


SCHEMA_ID = "rs-mca-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1"
ARCHITECTURE_ID = "M31_CHEBYSHEV_FIXED_REMAINDER_C1_BOUNDARY_SOURCE_ROUTE_CUT_V1"
STATUS = "PROVED_FIXED_REMAINDER_EXACT_C1_BOUNDARY_SOURCE_RAW_ROUTE_CUT_ROW_OPEN"

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
SHIFT = AGREEMENT - K
B_STAR = P**4 // 2**100
FORBIDDEN = B_STAR + 1

FOLD_DEGREE = 2_048
QUOTIENT_SIZE = N // FOLD_DEGREE
REMAINDER_SIZE = 1_911
QUOTIENT_SUPPORT_SIZE = 544
QUOTIENT_PREFIX_DEPTH = 32
FIXED_REMAINDER_CANDIDATES = math.comb(
    QUOTIENT_SIZE - 1, QUOTIENT_SUPPORT_SIZE
)
FIXED_REMAINDER_PREFIX_BOX = P**QUOTIENT_PREFIX_DEPTH

LOW_CUTOFF = 614_160
LOW_CAP = 3_730
HIGH_LAYER_COUNT = RADIUS - LOW_CUTOFF
RAW_BASELINE = 45
SIGNED_ALLOWANCE = 259_880
FORNEY_SUM_MAX = 2 * RADIUS - K - 1
SOURCE_OPTIMIZER_SHA256 = (
    "bed6d505904de120e76e7e4b5464b9682756a015dec8c993e4ed4c8d11815763"
)

TOY_P = 17
TOY_DOMAIN = tuple(range(1, 17))
TOY_K = 4
TOY_C = 2
TOY_R = 1
TOY_F = 3
TOY_T = 1
TOY_A = TOY_R + TOY_C * TOY_F

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the exact C1 boundary-source route-cut certificate."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Primary exact arithmetic, toy census, optimizer, and mutation replay."),
    ("packet_sage", SAGE_PATH, None,
     "Independent finite-field polynomial-fold and deployed arithmetic replay."),
    ("packet_note", NOTE_PATH, None,
     "Symbolic fixed-remainder theorem, chronology specialization, and route cut."),
    ("packet_readme", README_PATH, None,
     "Replay commands, provenance, and nonclaim contract."),
    ("fixed_remainder_arithmetic_note",
     ROOT / "experimental/notes/thresholds/20260709_m31_chebyshev_fixed_remainder_floor/cap25_v13_m31_chebyshev_fixed_remainder_floor.md",
     None, "Banked c=2048 fixed-remainder arithmetic floor."),
    ("fixed_remainder_arithmetic_replay",
     ROOT / "experimental/notes/thresholds/20260709_m31_chebyshev_fixed_remainder_floor/m31_chebyshev_fixed_remainder_floor.py",
     None, "Exact integer replay of the c=2048 floor."),
    ("chebyshev_domain_and_prefix_source", ROOT / "tex/cs25_cap_v13_2.tex",
     None, "Deployed twin-coset Chebyshev fibers and locator-prefix construction."),
    ("exact_prefix_list_source", ROOT / "experimental/rs_mca_thresholds.tex",
     None, "Exact locator-prefix/list bijection and quotient-remainder normal form."),
    ("v4_source_adapter_note",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Exact target-field weight histogram and signed occupancy identity."),
    ("v4_source_adapter_manifest",
     ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
     "payload_sha256", "Sealed v4 source adapter contract."),
    ("rank46_optimizer_source",
     ROOT / "experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py",
     None, "Exact moving-cutoff packing cap and Forney arithmetic source."),
    ("predecessor_route_cut_note",
     ROOT / "experimental/notes/thresholds/m31_full_span_forced_collision_route_cut.md",
     None, "Immediate predecessor and corrected global terminal."),
    ("predecessor_route_cut_manifest",
     ROOT / "experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json",
     "payload_sha256", "Sealed predecessor route-cut contract."),
    ("admissibility_authority",
     ROOT / "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex",
     None, "Non-oracular first-match codeword-payment rules."),
    ("active_v4_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active nonnegative five-atom LIST chronology and Q target."),
)


class VerificationError(RuntimeError):
    """Fail-closed exact-certificate error."""


CHECKS = 0


def require(value: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not value:
        raise VerificationError(label)


def ceil_div(numerator: int, denominator: int) -> int:
    require(denominator > 0, "positive denominator")
    return (numerator + denominator - 1) // denominator


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
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_json_path(path: Path, *, canonical: bool = False) -> Any:
    raw = path.read_bytes()
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
        require(raw == canonical_json(value), f"canonical JSON bytes: {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


def poly_mul(left: Sequence[int], right: Sequence[int], prime: int) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x_value in enumerate(left):
        for j, y_value in enumerate(right):
            out[i + j] = (out[i + j] + x_value * y_value) % prime
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def locator(points: Sequence[int], prime: int) -> tuple[int, ...]:
    out: tuple[int, ...] = (1,)
    for point in points:
        out = poly_mul(out, ((-point) % prime, 1), prime)
    return out


def poly_eval(polynomial: Sequence[int], value: int, prime: int) -> int:
    result = 0
    for coefficient in reversed(polynomial):
        result = (result * value + coefficient) % prime
    return result


def poly_sub(left: Sequence[int], right: Sequence[int], prime: int) -> tuple[int, ...]:
    out = [0] * max(len(left), len(right))
    for index in range(len(out)):
        out[index] = (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        ) % prime
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def toy_model() -> dict[str, Any]:
    quotient = tuple(sorted({x * x % TOY_P for x in TOY_DOMAIN}))
    base_point = 1
    remainder = (1,)
    require(quotient == (1, 2, 4, 8, 9, 13, 15, 16), "toy quotient image")
    require(tuple(x for x in TOY_DOMAIN if x * x % TOY_P == base_point) == (1, 16),
            "toy complete base fiber")

    buckets: dict[tuple[int, ...], list[dict[str, Any]]] = {}
    for selected in itertools.combinations(
        tuple(value for value in quotient if value != base_point), TOY_F
    ):
        quotient_locator = locator(selected, TOY_P)
        prefix = (quotient_locator[-2],)
        support = tuple(sorted(
            set(remainder)
            | {x for x in TOY_DOMAIN if x * x % TOY_P in selected}
        ))
        support_locator = locator(support, TOY_P)
        require(len(support) == TOY_A, "toy support size")
        require(len(support_locator) == TOY_A + 1 and support_locator[-1] == 1,
                "toy monic locator")
        buckets.setdefault(prefix, []).append({
            "quotient_support": list(selected),
            "support": list(support),
            "locator": list(support_locator),
        })

    heavy_prefix = min(
        buckets, key=lambda prefix: (-len(buckets[prefix]), prefix)
    )
    heavy = buckets[heavy_prefix]
    require(len(buckets) == 16, "toy attained quotient-prefix image")
    require(heavy_prefix == (1,) and len(heavy) == 3, "toy heavy bucket")
    require(len(heavy) >= ceil_div(math.comb(7, 3), TOY_P), "toy floor")

    first_locator = tuple(heavy[0]["locator"])
    global_prefix_low_to_high = tuple(first_locator[TOY_K:TOY_A])
    global_prefix = tuple(reversed(global_prefix_low_to_high))
    require(global_prefix == (16, 1, 16), "toy global prefix")
    received = tuple(
        first_locator[index] if index >= TOY_K else 0
        for index in range(TOY_A + 1)
    )

    codewords = []
    for row in heavy:
        support_locator = tuple(row["locator"])
        require(tuple(support_locator[TOY_K:TOY_A]) == global_prefix_low_to_high,
                "toy structured global-prefix agreement")
        codeword = poly_sub(received, support_locator, TOY_P)
        require(len(codeword) <= TOY_K, "toy codeword degree")
        agreements = tuple(
            x for x in TOY_DOMAIN
            if poly_eval(received, x, TOY_P) == poly_eval(codeword, x, TOY_P)
        )
        require(agreements == tuple(row["support"]), "toy exact agreement support")
        codewords.append(codeword)
    require(len(set(codewords)) == len(codewords), "toy distinct codewords")

    full_prefix_fiber = []
    for support in itertools.combinations(TOY_DOMAIN, TOY_A):
        support_locator = locator(support, TOY_P)
        if tuple(support_locator[TOY_K:TOY_A]) == global_prefix_low_to_high:
            full_prefix_fiber.append(support)
    require(len(full_prefix_fiber) == 3, "toy complete global prefix fiber")
    require({tuple(row["support"]) for row in heavy} == set(full_prefix_fiber),
            "toy structured bucket equals complete prefix fiber")

    return {
        "prime": TOY_P,
        "domain": list(TOY_DOMAIN),
        "fold": "phi(X)=X^2 on GF(17)^*",
        "fold_degree": TOY_C,
        "quotient_image": list(quotient),
        "quotient_size": len(quotient),
        "fixed_remainder": list(remainder),
        "quotient_support_size": TOY_F,
        "quotient_prefix_depth": TOY_T,
        "agreement": TOY_A,
        "dimension": TOY_K,
        "candidate_quotient_supports": math.comb(7, 3),
        "attained_quotient_prefixes": len(buckets),
        "heavy_quotient_prefix": list(heavy_prefix),
        "heavy_structured_bucket_size": len(heavy),
        "global_locator_prefix": list(global_prefix),
        "complete_global_prefix_fiber_size": len(full_prefix_fiber),
        "exact_boundary_agreement": True,
        "distinct_codewords": True,
        "structured_supports": [row["support"] for row in heavy],
    }


def balanced_pair_lower(member_count: int, set_size: int) -> tuple[int, int, int]:
    quotient, remainder = divmod(member_count * set_size, N)
    lower = N * quotient * (quotient - 1) // 2 + remainder * quotient
    return lower, quotient, remainder


def packing_feasible(member_count: int, set_size: int) -> bool:
    lower, _, _ = balanced_pair_lower(member_count, set_size)
    upper = math.comb(member_count, 2) * (K - 1)
    return lower <= upper


def packing_cutoff_caps() -> tuple[dict[int, int], str]:
    start = K // 2
    cap = 1
    caps: dict[int, int] = {}
    digest = hashlib.sha256()
    for cutoff in range(start, RADIUS):
        set_size = N - cutoff
        if set_size * set_size <= N * (K - 1):
            break
        require(packing_feasible(cap, set_size), "moving packing cap feasible")
        while packing_feasible(cap + 1, set_size):
            cap += 1
        require(not packing_feasible(cap + 1, set_size), "moving first exclusion")
        caps[cutoff] = cap
        digest.update(f"{cutoff},{cap}\n".encode("ascii"))
    require(len(caps) == 89_955, "packing scan row count")
    require(max(caps) == 614_242 and caps[614_242] == 1_001_281,
            "packing scan endpoint")
    require(digest.hexdigest() == SOURCE_OPTIMIZER_SHA256,
            "packing scan source digest")
    return caps, digest.hexdigest()


def baseline_row(caps: dict[int, int], baseline: int) -> dict[str, Any]:
    best: int | None = None
    ties: list[tuple[int, int]] = []
    for cutoff, cap in caps.items():
        safe_raw_tail = B_STAR - cap - baseline * (RADIUS - cutoff)
        if best is None or safe_raw_tail > best:
            best = safe_raw_tail
            ties = [(cutoff, cap)]
        elif safe_raw_tail == best:
            ties.append((cutoff, cap))
    require(best is not None, "baseline optimizer nonempty")
    source_floor = fixed_remainder_floor() - baseline
    return {
        "baseline": baseline,
        "forced_packet_rank": baseline + 1,
        "safe_raw_tail_cap": best,
        "forbidden_raw_tail_floor": best + 1,
        "canonical_first_optimal_cutoff": ties[0][0],
        "canonical_first_optimal_low_cap": ties[0][1],
        "all_optimal_cutoff_cap_pairs": [list(pair) for pair in ties],
        "fixed_remainder_raw_tail_floor": source_floor,
        "source_compatibility_margin": best - source_floor,
        "source_compatible": best >= source_floor,
    }


def ordered_prefix_max(total: int, count: int, prefix_count: int) -> int:
    quotient, remainder = divmod(total, count)
    return prefix_count * quotient + max(0, remainder - (count - prefix_count))


def fixed_remainder_floor() -> int:
    return ceil_div(FIXED_REMAINDER_CANDIDATES, FIXED_REMAINDER_PREFIX_BOX)


def expected_source_bindings() -> list[dict[str, Any]]:
    bindings = []
    for role, path, internal_key, scope in SOURCE_SPECS:
        require(path.exists() and path.is_file(), f"source exists: {role}")
        try:
            relative = path.relative_to(ROOT).as_posix()
        except ValueError as exc:
            raise VerificationError(f"source outside repository: {path}") from exc
        pure = PurePosixPath(relative)
        require(not pure.is_absolute() and ".." not in pure.parts, "safe source path")
        internal: str | None = None
        if internal_key is not None:
            source = strict_json_path(path, canonical=True)
            require(type(source) is dict, "source manifest object")
            internal = source.get(internal_key)
            require(type(internal) is str and len(internal) == 64,
                    "source internal payload hash")
        bindings.append({
            "binding_id": f"M31_CHEB_FIXED_REMAINDER_C1::{role}",
            "role": role,
            "path": relative,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
            "scope": scope,
        })
    return bindings


def build_payload() -> dict[str, Any]:
    floor = fixed_remainder_floor()
    degree_bound = (
        REMAINDER_SIZE
        + FOLD_DEGREE * (QUOTIENT_SUPPORT_SIZE - QUOTIENT_PREFIX_DEPTH - 1)
    )
    caps, optimizer_digest = packing_cutoff_caps()
    baseline_rows = {baseline: baseline_row(caps, baseline)
                     for baseline in range(2, RAW_BASELINE + 1)}
    b27 = baseline_rows[27]
    b28 = baseline_rows[28]
    b29 = baseline_rows[29]
    kernel_indices = 28 - 2
    first_sum = ordered_prefix_max(FORNEY_SUM_MAX, kernel_indices, 1)
    first_two_sum = ordered_prefix_max(FORNEY_SUM_MAX, kernel_indices, 2)
    baseline28_first_two_sum = ordered_prefix_max(FORNEY_SUM_MAX, 29 - 2, 2)
    baseline29_first_two_sum = ordered_prefix_max(FORNEY_SUM_MAX, 30 - 2, 2)
    source_compatible = [baseline for baseline, row in baseline_rows.items()
                         if row["source_compatible"]]
    two_row_forney = [
        baseline for baseline in range(3, RAW_BASELINE + 1)
        if ordered_prefix_max(FORNEY_SUM_MAX, baseline - 1, 2) < K - RADIUS
    ]
    require(source_compatible == list(range(2, 28)),
            "exact source-compatible baseline interval")
    require(two_row_forney == list(range(29, RAW_BASELINE + 1)),
            "exact two-row Forney baseline interval")
    require(set(source_compatible).isdisjoint(two_row_forney),
            "flat-baseline/Forney intersection empty")
    return {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "scope": {
            "workboard_item": "M1",
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "impact": "PROVED_C1_BOUNDARY_SOURCE_AND_RAW_ARCHITECTURE_ROUTE_CUT",
            "deployed_row_closed": False,
            "ledger_movement": 0,
            "is_m31_counterexample": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "general_theorem": {
            "name": "FIXED_REMAINDER_POLYNOMIAL_FOLD_EXACT_BOUNDARY_LIST",
            "hypotheses": {
                "fold": "monic degree-c phi in B[X], restricted D->Q with complete c-point fibers",
                "fixed_remainder": "R0 subset phi^-1(beta0), |R0|=r<c",
                "moving_quotient_support": "E subset Q\\{beta0}, |E|=f",
                "prefix_depth": "first t nonleading coefficients of V_E",
                "degree_gate": "r+c(f-t-1)<K",
            },
            "structured_floor": "ceil(binomial(|Q|-1,f)/|B|^t)",
            "locator": "L_E=L_R0*(V_E composed with phi)",
            "codeword": "c_E=U-L_E with degree(c_E)<K",
            "agreement_support": "R0 disjoint_union phi^-1(E)",
            "structured_codewords_distinct": True,
            "complete_list_is_global_locator_prefix_fiber": True,
            "degree_A_center_makes_complete_ball_boundary_only": True,
            "extension_field_list_descends_to_base_field": True,
        },
        "deployed_parameters": {
            "p": P,
            "code_field_cardinality": str(P**4),
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "shift": SHIFT,
            "B_star": B_STAR,
            "forbidden_size": FORBIDDEN,
            "fold": "monic normalization of T_2048",
            "fold_degree": FOLD_DEGREE,
            "quotient_size": QUOTIENT_SIZE,
            "fixed_remainder_size": REMAINDER_SIZE,
            "quotient_support_size": QUOTIENT_SUPPORT_SIZE,
            "quotient_prefix_depth": QUOTIENT_PREFIX_DEPTH,
            "candidate_quotient_supports": str(FIXED_REMAINDER_CANDIDATES),
            "prefix_box_size": str(FIXED_REMAINDER_PREFIX_BOX),
            "structured_list_floor": floor,
            "codeword_degree_upper": degree_bound,
            "degree_headroom_below_K": K - degree_bound,
            "complete_ball_boundary_only": True,
            "complete_ball_base_field_valued": True,
            "complete_list_cardinality_known_exactly": False,
            "budget_status": "UNKNOWN",
        },
        "c1_owner_classification": {
            "fold_scale_exponent": 11,
            "agreement_complete_fibers": QUOTIENT_SUPPORT_SIZE,
            "agreement_remainder_size": REMAINDER_SIZE,
            "agreement_QR2_visible": True,
            "complement_complete_fibers": QUOTIENT_SIZE - 1 - QUOTIENT_SUPPORT_SIZE,
            "complement_remainder_size": FOLD_DEGREE - REMAINDER_SIZE,
            "complement_size": RADIUS,
            "complement_identity": "981129=479*2048+137",
            "complement_QR2_visible": True,
            "fixed_remainder_across_structured_family": True,
            "declared_first_match_route": "AT_OR_BEFORE_C1_QUOTIENT_REMAINDER",
            "owner_order_is_declared_hypothesis": True,
            "under_declared_C1_order_structured_family_post_C1_primitive_Q_residual": 0,
            "complete_prefix_fiber_post_C1_residual_known": False,
            "C1_numerical_upper_payment_proved": False,
            "classification_scope":
                "the certified fixed-R structured subfamily only; arbitrary supports in the complete global prefix fiber are not classified",
        },
        "chronology_specialization": {
            "N_low": 0,
            "interior_layers_empty": True,
            "boundary_layer_floor": floor,
            "T46_floor": floor - RAW_BASELINE,
            "raw_T46_proposed_cap": SIGNED_ALLOWANCE,
            "raw_T46_cap_violation_margin": floor - RAW_BASELINE - SIGNED_ALLOWANCE,
            "Delta46": LOW_CAP + RAW_BASELINE * (HIGH_LAYER_COUNT - 1),
            "Xi46_formula": "M_R-16517335",
            "signed_Xi46_cap": SIGNED_ALLOWANCE,
            "signed_target_equivalent_to": "M_R<=16777215=B_star",
            "complete_list_is_global_boundary_prefix_fiber": True,
            "structured_floor_is_pre_first_match_raw_source": True,
            "raw_quantities_are_ledger_payments": False,
            "is_U_Q_upper_payment": False,
            "arbitrary_boundary_to_Q_adapter_proved": False,
            "v4_negative_refund_interface_exists": False,
            "route_terminal": "M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL",
            "next_exact_target":
                "C1_NUMERICAL_CODEWORD_PAYMENT_AND_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL",
        },
        "raw_baseline_optimizer": {
            "cutoff_scan_interval": [K // 2, max(caps)],
            "rows_scanned": len(caps),
            "rows_sha256": optimizer_digest,
            "safe_cap_formula": "B_star-low_cap(J)-b*(R-J)",
            "source_floor_formula": "6796405-b",
            "monotone_incompatibility":
                "for every fixed J the compatibility margin strictly decreases with b because R-J-1>0",
            "largest_source_compatible_baseline": 27,
            "baseline_27": b27,
            "baseline_28": b28,
            "baseline_29": b29,
            "all_baselines_at_least_28_source_incompatible": True,
        },
        "flat_baseline_forney_route_cut": {
            "baseline_scan_interval": [2, RAW_BASELINE],
            "source_compatible_baseline_interval": [2, 27],
            "two_row_forney_baseline_interval": [29, RAW_BASELINE],
            "simultaneously_admissible_baselines": [],
            "packet_columns": 28,
            "joint_kernel_rank": kernel_indices,
            "joint_index_sum_upper": FORNEY_SUM_MAX,
            "source_cutoff_min": K - RADIUS,
            "first_ordered_partial_sum_upper": first_sum,
            "first_two_ordered_partial_sum_upper": first_two_sum,
            "rank_one_partial_degree_below_cutoff": True,
            "rank_two_minor_degree_below_cutoff_certified": False,
            "baseline_28_packet_columns": 29,
            "baseline_28_first_two_ordered_partial_sum_upper":
                baseline28_first_two_sum,
            "baseline_28_two_row_below_cutoff": False,
            "baseline_29_packet_columns": 30,
            "baseline_29_first_two_ordered_partial_sum_upper":
                baseline29_first_two_sum,
            "baseline_29_two_row_below_cutoff": True,
            "first_baseline_with_two_row_below_cutoff": 29,
            "no_flat_baseline_survives_source_and_two_row_forney": True,
            "interpretation":
                "b=27 is the largest source-compatible baseline but lacks two-row control; b=29 is the first with two-row control but every b>=28 is source-incompatible",
        },
        "toy_control": toy_model(),
        "nonclaims": {
            "structured_floor_is_complete_list_size": False,
            "row_sharp_Q_upper_bound_proved": False,
            "C1_numerical_upper_payment_proved": False,
            "variable_remainder_orientation_residual_paid": False,
            "raw_baseline_27_closes_row": False,
            "adverse_forney_sequence_geometrically_realized": False,
            "M31_list_row_closed": False,
            "official_endpoint_or_score_changed": False,
        },
        "source_bindings": expected_source_bindings(),
    }


def exact_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"{label}: exact keys")


def verify_payload(payload: dict[str, Any]) -> None:
    exact_keys(payload, {
        "schema", "architecture_id", "status", "payload_sha256", "scope",
        "general_theorem", "deployed_parameters", "c1_owner_classification",
        "chronology_specialization",
        "raw_baseline_optimizer", "flat_baseline_forney_route_cut", "toy_control",
        "nonclaims", "source_bindings",
    }, "payload")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["architecture_id"] == ARCHITECTURE_ID, "architecture id")
    require(payload["status"] == STATUS, "status")
    require(payload["payload_sha256"] == payload_sha256(payload), "payload seal")

    scope = payload["scope"]
    require(scope == {
        "workboard_item": "M1",
        "row": "Mersenne-31 list at 2^-100",
        "object": "LIST",
        "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
        "impact": "PROVED_C1_BOUNDARY_SOURCE_AND_RAW_ARCHITECTURE_ROUTE_CUT",
        "deployed_row_closed": False,
        "ledger_movement": 0,
        "is_m31_counterexample": False,
        "stable_paper_modified": False,
        "lean_used": False,
    }, "exact scope contract")

    theorem = payload["general_theorem"]
    require(theorem == {
        "name": "FIXED_REMAINDER_POLYNOMIAL_FOLD_EXACT_BOUNDARY_LIST",
        "hypotheses": {
            "fold": "monic degree-c phi in B[X], restricted D->Q with complete c-point fibers",
            "fixed_remainder": "R0 subset phi^-1(beta0), |R0|=r<c",
            "moving_quotient_support": "E subset Q\\{beta0}, |E|=f",
            "prefix_depth": "first t nonleading coefficients of V_E",
            "degree_gate": "r+c(f-t-1)<K",
        },
        "structured_floor": "ceil(binomial(|Q|-1,f)/|B|^t)",
        "locator": "L_E=L_R0*(V_E composed with phi)",
        "codeword": "c_E=U-L_E with degree(c_E)<K",
        "agreement_support": "R0 disjoint_union phi^-1(E)",
        "structured_codewords_distinct": True,
        "complete_list_is_global_locator_prefix_fiber": True,
        "degree_A_center_makes_complete_ball_boundary_only": True,
        "extension_field_list_descends_to_base_field": True,
    }, "exact theorem contract")
    require(theorem["structured_codewords_distinct"] is True,
            "structured injectivity")
    require(theorem["complete_list_is_global_locator_prefix_fiber"] is True,
            "complete prefix fiber")
    require(theorem["degree_A_center_makes_complete_ball_boundary_only"] is True,
            "boundary-only theorem")
    require(theorem["extension_field_list_descends_to_base_field"] is True,
            "target-field descent")

    deployed = payload["deployed_parameters"]
    exact_keys(deployed, {
        "p", "code_field_cardinality", "n", "K", "agreement", "radius",
        "shift", "B_star", "forbidden_size", "fold", "fold_degree",
        "quotient_size", "fixed_remainder_size", "quotient_support_size",
        "quotient_prefix_depth", "candidate_quotient_supports",
        "prefix_box_size", "structured_list_floor", "codeword_degree_upper",
        "degree_headroom_below_K", "complete_ball_boundary_only",
        "complete_ball_base_field_valued", "complete_list_cardinality_known_exactly",
        "budget_status",
    }, "deployed parameters")
    require(deployed["p"] == P and deployed["n"] == N and deployed["K"] == K,
            "deployed row")
    require(deployed["agreement"] == AGREEMENT and deployed["radius"] == RADIUS,
            "deployed agreement/radius")
    require(deployed["shift"] == SHIFT == 67_447, "deployed shift")
    require(deployed["B_star"] == B_STAR == 16_777_215, "deployed budget")
    require(deployed["fold_degree"] == FOLD_DEGREE, "fold degree")
    require(deployed["fold"] == "monic normalization of T_2048", "fold name")
    require(deployed["quotient_size"] == QUOTIENT_SIZE == 1_024,
            "quotient size")
    require(deployed["fixed_remainder_size"] == REMAINDER_SIZE,
            "fixed remainder size")
    require(deployed["quotient_support_size"] == QUOTIENT_SUPPORT_SIZE,
            "quotient support size")
    require(deployed["quotient_prefix_depth"] == QUOTIENT_PREFIX_DEPTH,
            "quotient prefix depth")
    require(deployed["candidate_quotient_supports"] ==
            str(FIXED_REMAINDER_CANDIDATES), "candidate quotient supports")
    require(deployed["prefix_box_size"] == str(FIXED_REMAINDER_PREFIX_BOX),
            "prefix box size")
    require(deployed["code_field_cardinality"] == str(P**4),
            "target field cardinality")
    require(deployed["forbidden_size"] == FORBIDDEN,
            "forbidden list size")
    require(REMAINDER_SIZE + FOLD_DEGREE * QUOTIENT_SUPPORT_SIZE == AGREEMENT,
            "fixed-remainder agreement")
    require(QUOTIENT_PREFIX_DEPTH * FOLD_DEGREE + REMAINDER_SIZE == SHIFT,
            "global prefix depth")
    require(deployed["structured_list_floor"] == fixed_remainder_floor() == 6_796_405,
            "fixed-remainder floor")
    require(deployed["codeword_degree_upper"] == 1_048_439,
            "codeword degree upper")
    require(deployed["degree_headroom_below_K"] == 137,
            "degree headroom")
    require(deployed["complete_ball_boundary_only"] is True,
            "complete deployed ball boundary-only")
    require(deployed["complete_ball_base_field_valued"] is True,
            "complete deployed list base-field valued")
    require(deployed["complete_list_cardinality_known_exactly"] is False,
            "floor not exact total")
    require(deployed["budget_status"] == "UNKNOWN", "budget status")

    c1 = payload["c1_owner_classification"]
    require(c1 == {
        "fold_scale_exponent": 11,
        "agreement_complete_fibers": 544,
        "agreement_remainder_size": 1_911,
        "agreement_QR2_visible": True,
        "complement_complete_fibers": 479,
        "complement_remainder_size": 137,
        "complement_size": RADIUS,
        "complement_identity": "981129=479*2048+137",
        "complement_QR2_visible": True,
        "fixed_remainder_across_structured_family": True,
        "declared_first_match_route": "AT_OR_BEFORE_C1_QUOTIENT_REMAINDER",
        "owner_order_is_declared_hypothesis": True,
        "under_declared_C1_order_structured_family_post_C1_primitive_Q_residual": 0,
        "complete_prefix_fiber_post_C1_residual_known": False,
        "C1_numerical_upper_payment_proved": False,
        "classification_scope":
            "the certified fixed-R structured subfamily only; arbitrary supports in the complete global prefix fiber are not classified",
    }, "exact declared C1 route classification")
    require(QUOTIENT_SIZE - 1 - QUOTIENT_SUPPORT_SIZE == 479,
            "complement complete-fiber count")
    require(FOLD_DEGREE - REMAINDER_SIZE == 137,
            "complement remainder size")
    require(479 * FOLD_DEGREE + 137 == RADIUS,
            "complement size identity")
    require(REMAINDER_SIZE <= SHIFT and 137 <= SHIFT,
            "agreement and complement QR2 visibility")

    chronology = payload["chronology_specialization"]
    exact_keys(chronology, {
        "N_low", "interior_layers_empty", "boundary_layer_floor", "T46_floor",
        "raw_T46_proposed_cap", "raw_T46_cap_violation_margin", "Delta46",
        "Xi46_formula", "signed_Xi46_cap", "signed_target_equivalent_to",
        "complete_list_is_global_boundary_prefix_fiber",
        "structured_floor_is_pre_first_match_raw_source",
        "raw_quantities_are_ledger_payments", "is_U_Q_upper_payment",
        "arbitrary_boundary_to_Q_adapter_proved", "v4_negative_refund_interface_exists",
        "route_terminal", "next_exact_target",
    }, "chronology specialization")
    require(chronology["N_low"] == 0 and chronology["interior_layers_empty"] is True,
            "boundary-only chronology")
    require(chronology["boundary_layer_floor"] == 6_796_405,
            "boundary floor")
    require(chronology["T46_floor"] == 6_796_360,
            "T46 floor")
    require(chronology["raw_T46_cap_violation_margin"] == 6_536_480,
            "raw T46 route-cut margin")
    require(chronology["raw_T46_proposed_cap"] == SIGNED_ALLOWANCE,
            "raw T46 proposed cap")
    require(chronology["Delta46"] == 16_517_290,
            "exact boundary deficit")
    require(chronology["signed_target_equivalent_to"] ==
            "M_R<=16777215=B_star", "signed Q equivalence")
    require(chronology["complete_list_is_global_boundary_prefix_fiber"] is True,
            "global boundary prefix fiber")
    require(chronology["structured_floor_is_pre_first_match_raw_source"] is True,
            "pre-first-match raw source")
    require(chronology["raw_quantities_are_ledger_payments"] is False,
            "raw quantities are not ledger payments")
    require(chronology["is_U_Q_upper_payment"] is False,
            "not a Q upper payment")
    require(chronology["arbitrary_boundary_to_Q_adapter_proved"] is False,
            "no arbitrary boundary adapter")
    require(chronology["v4_negative_refund_interface_exists"] is False,
            "no negative refund interface")
    require(chronology["route_terminal"] ==
            "M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL", "route terminal")
    require(chronology["next_exact_target"] ==
            "C1_NUMERICAL_CODEWORD_PAYMENT_AND_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL",
            "next exact target")

    optimizer = payload["raw_baseline_optimizer"]
    exact_keys(optimizer, {
        "cutoff_scan_interval", "rows_scanned", "rows_sha256",
        "safe_cap_formula", "source_floor_formula", "monotone_incompatibility",
        "largest_source_compatible_baseline", "baseline_27", "baseline_28",
        "baseline_29", "all_baselines_at_least_28_source_incompatible",
    }, "raw baseline optimizer")
    require(optimizer["cutoff_scan_interval"] == [K // 2, 614_242]
            and optimizer["rows_scanned"] == 89_955,
            "optimizer scan domain")
    require(optimizer["rows_sha256"] == SOURCE_OPTIMIZER_SHA256,
            "optimizer source digest")
    require(optimizer["largest_source_compatible_baseline"] == 27,
            "largest compatible baseline")
    row27 = optimizer["baseline_27"]
    require(row27["canonical_first_optimal_cutoff"] == 614_134,
            "baseline27 cutoff")
    require(row27["canonical_first_optimal_low_cap"] == 2_835,
            "baseline27 low cap")
    require(row27["safe_raw_tail_cap"] == 6_865_515,
            "baseline27 safe cap")
    require(row27["fixed_remainder_raw_tail_floor"] == 6_796_378,
            "baseline27 source floor")
    require(row27["source_compatibility_margin"] == 69_137
            and row27["source_compatible"] is True,
            "baseline27 headroom")
    require(row27["all_optimal_cutoff_cap_pairs"] ==
            [[614_134, 2_835], [614_135, 2_862],
             [614_136, 2_889], [614_137, 2_916]],
            "baseline27 complete optimizer ties")
    row28 = optimizer["baseline_28"]
    require(row28["canonical_first_optimal_cutoff"] == 614_137,
            "baseline28 cutoff")
    require(row28["canonical_first_optimal_low_cap"] == 2_916,
            "baseline28 low cap")
    require(row28["safe_raw_tail_cap"] == 6_498_523,
            "baseline28 safe cap")
    require(row28["fixed_remainder_raw_tail_floor"] == 6_796_377,
            "baseline28 source floor")
    require(row28["source_compatibility_margin"] == -297_854
            and row28["source_compatible"] is False,
            "baseline28 contradiction")
    require(row28["all_optimal_cutoff_cap_pairs"] ==
            [[614_137, 2_916], [614_138, 2_944], [614_139, 2_972]],
            "baseline28 complete optimizer ties")
    row29 = optimizer["baseline_29"]
    require(row29["canonical_first_optimal_cutoff"] == 614_139,
            "baseline29 cutoff")
    require(row29["canonical_first_optimal_low_cap"] == 2_972,
            "baseline29 low cap")
    require(row29["safe_raw_tail_cap"] == 6_131_533,
            "baseline29 safe cap")
    require(row29["fixed_remainder_raw_tail_floor"] == 6_796_376,
            "baseline29 source floor")
    require(row29["source_compatibility_margin"] == -664_843
            and row29["source_compatible"] is False,
            "baseline29 contradiction")
    require(row29["all_optimal_cutoff_cap_pairs"] == [[614_139, 2_972]],
            "baseline29 complete optimizer ties")
    require(optimizer["all_baselines_at_least_28_source_incompatible"] is True,
            "all higher baselines cut")

    forney = payload["flat_baseline_forney_route_cut"]
    exact_keys(forney, {
        "baseline_scan_interval", "source_compatible_baseline_interval",
        "two_row_forney_baseline_interval", "simultaneously_admissible_baselines",
        "packet_columns", "joint_kernel_rank", "joint_index_sum_upper",
        "source_cutoff_min", "first_ordered_partial_sum_upper",
        "first_two_ordered_partial_sum_upper",
        "rank_one_partial_degree_below_cutoff",
        "rank_two_minor_degree_below_cutoff_certified",
        "baseline_28_packet_columns",
        "baseline_28_first_two_ordered_partial_sum_upper",
        "baseline_28_two_row_below_cutoff", "baseline_29_packet_columns",
        "baseline_29_first_two_ordered_partial_sum_upper",
        "baseline_29_two_row_below_cutoff",
        "first_baseline_with_two_row_below_cutoff",
        "no_flat_baseline_survives_source_and_two_row_forney", "interpretation",
    }, "flat baseline Forney route cut")
    require(forney["packet_columns"] == 28 and forney["joint_kernel_rank"] == 26,
            "rank28 dimensions")
    require(forney["joint_index_sum_upper"] == 913_681,
            "rank28 index sum")
    require(forney["first_ordered_partial_sum_upper"] == 35_141,
            "rank28 first sum")
    require(forney["first_two_ordered_partial_sum_upper"] == 70_282,
            "rank28 first two sum")
    require(35_141 < 67_447 < 70_282, "rank28 cutoff route cut")
    require(forney["rank_one_partial_degree_below_cutoff"] is True,
            "rank-one certificate")
    require(forney["rank_two_minor_degree_below_cutoff_certified"] is False,
            "no rank-two certificate")
    require(forney["baseline_28_packet_columns"] == 29
            and forney["baseline_28_first_two_ordered_partial_sum_upper"] == 67_680
            and forney["baseline_28_two_row_below_cutoff"] is False,
            "baseline28 Forney transition")
    require(forney["baseline_29_packet_columns"] == 30
            and forney["baseline_29_first_two_ordered_partial_sum_upper"] == 65_262
            and forney["baseline_29_two_row_below_cutoff"] is True,
            "baseline29 Forney transition")
    require(forney["first_baseline_with_two_row_below_cutoff"] == 29,
            "first two-row baseline")
    require(forney["baseline_scan_interval"] == [2, 45]
            and forney["source_compatible_baseline_interval"] == [2, 27]
            and forney["two_row_forney_baseline_interval"] == [29, 45]
            and forney["simultaneously_admissible_baselines"] == [],
            "exhaustive baseline intervals")
    require(forney["no_flat_baseline_survives_source_and_two_row_forney"] is True,
            "flat-baseline/Forney intersection empty")
    require(forney["interpretation"] ==
            "b=27 is the largest source-compatible baseline but lacks two-row control; b=29 is the first with two-row control but every b>=28 is source-incompatible",
            "Forney route-cut interpretation")

    require(payload["toy_control"] == toy_model(), "toy exact replay")
    nonclaims = payload["nonclaims"]
    require(nonclaims == {
        "structured_floor_is_complete_list_size": False,
        "row_sharp_Q_upper_bound_proved": False,
        "C1_numerical_upper_payment_proved": False,
        "variable_remainder_orientation_residual_paid": False,
        "raw_baseline_27_closes_row": False,
        "adverse_forney_sequence_geometrically_realized": False,
        "M31_list_row_closed": False,
        "official_endpoint_or_score_changed": False,
    }, "exact nonclaim contract")
    require(payload["source_bindings"] == expected_source_bindings(),
            "live source bindings")


def mutate_path(payload: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def tamper_selftest(expected: dict[str, Any]) -> None:
    mutations: tuple[tuple[str, tuple[Any, ...], Any], ...] = (
        ("status", ("status",), "CLOSED"),
        ("ledger", ("scope", "ledger_movement"), 1),
        ("counterexample", ("scope", "is_m31_counterexample"), True),
        ("fold", ("deployed_parameters", "fold_degree"), 1_024),
        ("remainder", ("deployed_parameters", "fixed_remainder_size"), 1_910),
        ("prefix-depth", ("deployed_parameters", "quotient_prefix_depth"), 31),
        ("floor", ("deployed_parameters", "structured_list_floor"), 6_796_404),
        ("degree", ("deployed_parameters", "codeword_degree_upper"), 1_048_440),
        ("headroom", ("deployed_parameters", "degree_headroom_below_K"), 136),
        ("boundary", ("deployed_parameters", "complete_ball_boundary_only"), False),
        ("base-field", ("deployed_parameters", "complete_ball_base_field_valued"), False),
        ("exact-total", ("deployed_parameters", "complete_list_cardinality_known_exactly"), True),
        ("C1-route", ("c1_owner_classification", "declared_first_match_route"), "U_Q"),
        ("C1-complement", ("c1_owner_classification", "complement_complete_fibers"), 480),
        ("C1-order", ("c1_owner_classification", "owner_order_is_declared_hypothesis"), False),
        ("C1-residual", ("c1_owner_classification", "under_declared_C1_order_structured_family_post_C1_primitive_Q_residual"), 1),
        ("C1-complete-overclaim", ("c1_owner_classification", "complete_prefix_fiber_post_C1_residual_known"), True),
        ("T46", ("chronology_specialization", "T46_floor"), 6_796_359),
        ("T46-margin", ("chronology_specialization", "raw_T46_cap_violation_margin"), 6_536_479),
        ("Delta", ("chronology_specialization", "Delta46"), 16_517_289),
        ("Q-payment", ("chronology_specialization", "is_U_Q_upper_payment"), True),
        ("negative-refund", ("chronology_specialization", "v4_negative_refund_interface_exists"), True),
        ("baseline", ("raw_baseline_optimizer", "largest_source_compatible_baseline"), 28),
        ("b27-cap", ("raw_baseline_optimizer", "baseline_27", "safe_raw_tail_cap"), 6_865_514),
        ("b27-margin", ("raw_baseline_optimizer", "baseline_27", "source_compatibility_margin"), 69_136),
        ("b28-compatible", ("raw_baseline_optimizer", "baseline_28", "source_compatible"), True),
        ("b29-margin", ("raw_baseline_optimizer", "baseline_29", "source_compatibility_margin"), -664_842),
        ("optimizer-hash", ("raw_baseline_optimizer", "rows_sha256"), "0" * 64),
        ("kernel-rank", ("flat_baseline_forney_route_cut", "joint_kernel_rank"), 25),
        ("first-sum", ("flat_baseline_forney_route_cut", "first_ordered_partial_sum_upper"), 35_142),
        ("two-sum", ("flat_baseline_forney_route_cut", "first_two_ordered_partial_sum_upper"), 67_446),
        ("rank2", ("flat_baseline_forney_route_cut", "rank_two_minor_degree_below_cutoff_certified"), True),
        ("b28-two-sum", ("flat_baseline_forney_route_cut", "baseline_28_first_two_ordered_partial_sum_upper"), 67_447),
        ("b29-two-sum", ("flat_baseline_forney_route_cut", "baseline_29_first_two_ordered_partial_sum_upper"), 67_447),
        ("first-two-row", ("flat_baseline_forney_route_cut", "first_baseline_with_two_row_below_cutoff"), 28),
        ("route-cut", ("flat_baseline_forney_route_cut", "no_flat_baseline_survives_source_and_two_row_forney"), False),
        ("intersection", ("flat_baseline_forney_route_cut", "simultaneously_admissible_baselines"), [27]),
        ("toy-size", ("toy_control", "heavy_structured_bucket_size"), 2),
        ("toy-prefix", ("toy_control", "global_locator_prefix", 0), 15),
        ("false-Q", ("nonclaims", "row_sharp_Q_upper_bound_proved"), True),
        ("false-geometric", ("nonclaims", "adverse_forney_sequence_geometrically_realized"), True),
        ("false-close", ("nonclaims", "M31_list_row_closed"), True),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
    )
    rejected = 0
    for label, path, value in mutations:
        trial = copy.deepcopy(expected)
        mutate_path(trial, path, value)
        trial = seal(trial)
        try:
            verify_payload(trial)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")
    require(rejected == len(mutations), "all semantic mutations rejected")
    print(f"tamper_selftest=PASS rejected={rejected}/{len(mutations)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not any((args.check, args.print_template, args.tamper_selftest)):
        args.check = True

    expected = seal(build_payload())
    verify_payload(expected)

    if args.check:
        require(MANIFEST_PATH.exists(), "manifest exists")
        actual = strict_json_path(MANIFEST_PATH, canonical=True)
        require(type(actual) is dict, "manifest object")
        verify_payload(actual)
        require(actual == expected, "manifest equals regenerated payload")
        print("M31 Chebyshev fixed-remainder C1 boundary-source route cut: PASS")
        print("exact source: c=2048 floor=6796405; complete ball boundary-only")
        print("route: QR2 fixed-R; removed by/at C1; primitive-Q residual=0")
        print("chronology: T46>=6796360; raw cap missed by 6536480")
        print("optimizer: b=27 compatible by 69137; every b>=28 incompatible")
        print("Forney: b27 p2=70282; b28 p2=67680; b29 p2=65262<67447")
        print("route cut: no flat baseline survives source and gains two-row control")
        print("scope: C1 numerical payment and variable-R residual OPEN; ledger movement=0")

    if args.tamper_selftest:
        tamper_selftest(expected)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
    else:
        print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
