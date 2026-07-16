#!/usr/bin/env python3
"""Audit the fixed-line extension-cell contract and emit an exact falsifier.

This packet does two deliberately narrow things.

1.  It gives an exact rate-one-half, t=2 support-wise RS-MCA line over F_(7^6) whose
    full-degree bad-slope set has size one and is not Frobenius stable.  Thus
    Frobenius-orbit divisibility is not a property of the bad slopes of an
    arbitrary fixed F-valued line.
2.  It separates the direct extension dimension-degree charge Delta*p^e from
    the KoalaBear primitive Q-fin multiplier K_rem.  Unknown U_Q and U_A stay
    null, and no deployed chart or row closure is claimed.

The script uses only the Python standard library.  Sage supplies an independent
replay in verify_frontier_extension_fixed_line_audit_v1.sage.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-frontier-extension-fixed-line-audit-v1"
CERT_DIR = ROOT / "experimental/data/certificates/frontier-extension-fixed-line-audit-v1"
CERT_PATH = CERT_DIR / "frontier_extension_fixed_line_audit_v1.json"
NOTE_REL = Path("experimental/notes/frontier-adjacent/frontier_extension_fixed_line_audit_v1.md")
VERIFIER_REL = Path("experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.py")
SAGE_REL = Path("experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.sage")
V1_TARGET_NOTE_REL = Path("experimental/notes/frontier-adjacent/frontier_extension_cell_targets_v1.md")
V1_TARGET_PACKET_REL = Path("experimental/data/certificates/frontier-adjacent/extension_cell_targets_v1.json")
V1_TARGET_VERIFIER_REL = Path("experimental/scripts/verify_frontier_extension_cell_targets.py")
V1_SCANNER_REL = Path("experimental/scripts/f1_extension_full_orbit_scan.py")
V1_SCANNER_PACKET_REL = Path(
    "experimental/data/certificates/frontier-adjacent/f1_full_orbit_scan_v1.json"
)
BASE_NOTE_REL = Path("experimental/notes/thresholds/kb_mca_1116048_base_slope_universe_v2.md")
BASE_PACKET_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2/"
    "kb_mca_1116048_base_slope_universe_v2.json"
)
BASE_VERIFIER_REL = Path("experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py")
MIN_FIELD_REL = Path("experimental/notes/f1/f1_minimal_field_descent.md")
STABILIZER_REL = Path("experimental/notes/ef/ef_galois_stabilizer_descent.md")
ORBIT_REL = Path("experimental/notes/ef/ef_full_orbit_cycle_descent.md")
COORDINATE_REL = Path("experimental/notes/f1/f1_extension_coordinate_transfer.md")
ATLAS_PACKET_REL = Path(
    "experimental/data/certificates/m1-a4-spi-atlas-manifest-v1/"
    "kb_mca_a1116048_base_generated_family.json"
)
DIMENSION_DEGREE_REL = Path("tex/cs25_cap_v12.tex")
FIRST_FORM_LEDGER_REL = Path("experimental/cap25_cap_v13_raw.tex")

# Exact deployed KoalaBear row arithmetic imported from the #812 packet.
P_KB = 2_130_706_433
E_KB = 6
Q_LINE_KB = P_KB**E_KB
N_KB = 2_097_152
K_KB = 1_048_576
A_KB = 1_116_048
J_KB = N_KB - A_KB
T_KB = A_KB - K_KB
W_KB = T_KB - 1
B_STAR = (Q_LINE_KB - 1) // (1 << 128)
TERMINAL_QUOTIENT = 471_447_040
BASE_SLOPE_CHARGE = P_KB
BASELINE_U_PAID = TERMINAL_QUOTIENT + BASE_SLOPE_CHARGE
B_REM = B_STAR - BASELINE_U_PAID
K_REM_QFIN = 4_807_520

# Exact rate-one-half sextic toy.  The modulus is X^6 + 2 in low-to-high
# coefficient order, and the domain is the full multiplicative group F_7^x.
P_TOY = 7
E_TOY = 6
MODULUS = [2, 0, 0, 0, 0, 0, 1]
N_TOY = 6
K_TOY = 3
A_TOY = 5
T_TOY = A_TOY - K_TOY
DOMAIN_TOY = [1, 2, 3, 4, 5, 6]

TOP_KEYS = {
    "schema",
    "status",
    "artifact_kind",
    "source_bindings",
    "fixed_line_counterexample",
    "koalabear_budget_audit",
    "routing_audit",
    "supersession_gate",
    "deployed_chart_gate",
    "corrected_contract",
    "nonclaims",
    "payload_sha256",
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON value is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def require_json_equal(actual: object, expected: object, label: str) -> None:
    require(canonical_bytes(actual) == canonical_bytes(expected), f"{label} drift")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return canonical_hash(payload)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trim(poly: list[int], p: int = P_TOY) -> list[int]:
    out = [value % p for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out or [0]


def poly_sub(left: list[int], right: list[int], p: int = P_TOY) -> list[int]:
    size = max(len(left), len(right))
    return trim(
        [
            ((left[i] if i < len(left) else 0) - (right[i] if i < len(right) else 0)) % p
            for i in range(size)
        ],
        p,
    )


def poly_mul(left: list[int], right: list[int], p: int = P_TOY) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % p
    return trim(out, p)


def poly_divmod(
    numerator: list[int], denominator: list[int], p: int = P_TOY
) -> tuple[list[int], list[int]]:
    work = trim(numerator, p)
    divisor = trim(denominator, p)
    require(divisor != [0], "polynomial division by zero")
    quotient = [0] * max(1, len(work) - len(divisor) + 1)
    inv = pow(divisor[-1], -1, p)
    while work != [0] and len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        coeff = work[-1] * inv % p
        quotient[shift] = coeff
        subtractor = [0] * shift + [coeff * value % p for value in divisor]
        work = poly_sub(work, subtractor, p)
    return trim(quotient, p), work


def poly_mod(poly: list[int], modulus: list[int], p: int = P_TOY) -> list[int]:
    return poly_divmod(poly, modulus, p)[1]


def poly_gcd(left: list[int], right: list[int], p: int = P_TOY) -> list[int]:
    a, b = trim(left, p), trim(right, p)
    while b != [0]:
        _, remainder = poly_divmod(a, b, p)
        a, b = b, remainder
    if a == [0]:
        return [0]
    inv = pow(a[-1], -1, p)
    return trim([inv * value for value in a], p)


def poly_powmod(
    base: list[int], exponent: int, modulus: list[int], p: int = P_TOY
) -> list[int]:
    out = [1]
    factor = poly_mod(base, modulus, p)
    while exponent:
        if exponent & 1:
            out = poly_mod(poly_mul(out, factor, p), modulus, p)
        factor = poly_mod(poly_mul(factor, factor, p), modulus, p)
        exponent >>= 1
    return trim(out, p)


def modulus_is_irreducible() -> bool:
    # Rabin test for monic degree six: X^(p^6)-X vanishes mod f, while
    # gcd(f, X^(p^2)-X)=gcd(f, X^(p^3)-X)=1.
    x = [0, 1]
    full = poly_sub(poly_powmod(x, P_TOY**E_TOY, MODULUS), x)
    if trim(full) != [0]:
        return False
    for d in (2, 3):
        probe = poly_sub(poly_powmod(x, P_TOY**d, MODULUS), x)
        if poly_gcd(MODULUS, probe) != [1]:
            return False
    return True


def decode(value: int) -> tuple[int, ...]:
    require(0 <= value < P_TOY**E_TOY, "encoded field element out of range")
    coeffs = []
    for _ in range(E_TOY):
        coeffs.append(value % P_TOY)
        value //= P_TOY
    return tuple(coeffs)


def encode(value: tuple[int, ...]) -> int:
    require(len(value) == E_TOY, "wrong extension-coordinate length")
    total = 0
    place = 1
    for coeff in value:
        total += (coeff % P_TOY) * place
        place *= P_TOY
    return total


ZERO = (0,) * E_TOY
ONE = (1,) + (0,) * (E_TOY - 1)
GENERATOR = (0, 1) + (0,) * (E_TOY - 2)


def fadd(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((left[i] + right[i]) % P_TOY for i in range(E_TOY))


def fneg(value: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((-entry) % P_TOY for entry in value)


def fmul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    product = [0] * (2 * E_TOY - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            product[i + j] = (product[i + j] + a * b) % P_TOY
    reduced = poly_mod(product, MODULUS)
    reduced += [0] * (E_TOY - len(reduced))
    return tuple(reduced[:E_TOY])


def fpow(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    out = ONE
    factor = value
    while exponent:
        if exponent & 1:
            out = fmul(out, factor)
        factor = fmul(factor, factor)
        exponent >>= 1
    return out


def minimal_field_degree(value: tuple[int, ...]) -> int:
    for degree in (1, 2, 3, 6):
        if fpow(value, P_TOY**degree) == value:
            return degree
    raise VerificationError("element does not lie in the declared sextic field")


def base_scalar_mul(value: tuple[int, ...], scalar: int) -> tuple[int, ...]:
    return tuple((scalar * entry) % P_TOY for entry in value)


@functools.cache
def interpolation_weights(
    source_indices: tuple[int, ...], target_index: int
) -> tuple[int, ...]:
    target = DOMAIN_TOY[target_index]
    weights = []
    for source_index in source_indices:
        source = DOMAIN_TOY[source_index]
        numerator = 1
        denominator = 1
        for other_index in source_indices:
            if other_index == source_index:
                continue
            other = DOMAIN_TOY[other_index]
            numerator = numerator * (target - other) % P_TOY
            denominator = denominator * (source - other) % P_TOY
        weights.append(numerator * pow(denominator, -1, P_TOY) % P_TOY)
    return tuple(weights)


def support_is_rs_codeword(
    values: list[tuple[int, ...]], support: list[int] | tuple[int, ...]
) -> bool:
    require(len(support) >= K_TOY, "RS support shorter than dimension")
    sources = tuple(support[:K_TOY])
    for target_index in support[K_TOY:]:
        predicted = ZERO
        for source_index, weight in zip(
            sources, interpolation_weights(sources, target_index), strict=True
        ):
            predicted = fadd(predicted, base_scalar_mul(values[source_index], weight))
        if predicted != values[target_index]:
            return False
    return True


def agreeing_supports(values: list[tuple[int, ...]], agreement: int) -> list[list[int]]:
    supports = []
    for support in itertools.combinations(range(len(values)), agreement):
        if support_is_rs_codeword(values, support):
            supports.append(list(support))
    return supports


def max_rs_agreement(values: list[tuple[int, ...]]) -> tuple[int, list[list[int]]]:
    for agreement in range(N_TOY, K_TOY - 1, -1):
        supports = agreeing_supports(values, agreement)
        if supports:
            return agreement, supports
    raise VerificationError("RS interpolation failed on every k-support")


@functools.cache
def derive_counterexample() -> dict[str, Any]:
    irreducible = modulus_is_irreducible()
    require(irreducible, "toy sextic modulus is not irreducible")
    f_word = [fneg(GENERATOR), ZERO, ZERO, ZERO, ZERO, ONE]
    g_word = [ONE, ZERO, ZERO, ZERO, ZERO, ZERO]
    bad_records = []
    for encoded_slope in range(P_TOY**E_TOY):
        slope = decode(encoded_slope)
        values = [fadd(f_word[i], fmul(slope, g_word[i])) for i in range(N_TOY)]
        size_A_supports = agreeing_supports(values, A_TOY)
        if size_A_supports:
            agreement, maximal_supports = max_rs_agreement(values)
            bad_records.append(
                {
                    "slope_encoded": encoded_slope,
                    "slope_coefficients_low_to_high": list(slope),
                    "minimal_field_degree": minimal_field_degree(slope),
                    "max_agreement": agreement,
                    "agreeing_supports_of_size_A": size_A_supports,
                    "maximal_agreeing_supports": maximal_supports,
                    "word_values_encoded": [encode(value) for value in values],
                }
            )

    bad_set = [record["slope_encoded"] for record in bad_records]
    generator_encoded = encode(GENERATOR)
    require(bad_set == [generator_encoded], "toy bad-slope census drift")
    conjugates = []
    current = GENERATOR
    for _ in range(E_TOY):
        conjugates.append(encode(current))
        current = fpow(current, P_TOY)
    require(len(set(conjugates)) == E_TOY, "generator does not have degree six")
    full_degree_count = sum(
        record["minimal_field_degree"] == E_TOY for record in bad_records
    )
    require(full_degree_count == 1, "toy full-degree count drift")
    bad_set_frobenius_stable = all(
        encode(fpow(decode(slope), P_TOY)) in bad_set for slope in bad_set
    )
    require(not bad_set_frobenius_stable, "toy bad set unexpectedly Frobenius stable")
    pair_field_degree = math.lcm(
        *(minimal_field_degree(value) for value in f_word + g_word)
    )
    pair_is_base_valued = all(
        fpow(value, P_TOY) == value for value in f_word + g_word
    )
    require(g_word[0] == ONE, "toy common-scalar anchor drift")
    base_nonzero_scalars = [
        (scalar,) + (0,) * (E_TOY - 1) for scalar in range(1, P_TOY)
    ]
    common_scalar_base_descent_exists = any(
        all(
            fpow(fmul(scalar, value), P_TOY) == fmul(scalar, value)
            for value in f_word + g_word
        )
        for scalar in base_nonzero_scalars
    )
    require(pair_field_degree == E_TOY, "toy received-pair field degree drift")
    require(not pair_is_base_valued, "toy received pair unexpectedly base-valued")
    require(
        not common_scalar_base_descent_exists,
        "toy received pair unexpectedly descends after common scaling",
    )
    support = bad_records[0]["agreeing_supports_of_size_A"][0]
    require(support == [0, 1, 2, 3, 4], "toy unique support drift")
    exact_agreement_not_global = bad_records[0]["max_agreement"] == A_TOY < N_TOY
    f_restriction_is_codeword = support_is_rs_codeword(f_word, support)
    g_restriction_is_codeword = support_is_rs_codeword(g_word, support)
    simultaneously_explained = f_restriction_is_codeword and g_restriction_is_codeword
    require(exact_agreement_not_global, "toy bad word became a global codeword")
    require(not simultaneously_explained, "toy support became a common-line residue")
    return {
        "claim_refuted": (
            "For an arbitrary fixed genuinely F-valued received line, the "
            "minimal-field-F bad slopes form complete Frobenius orbits."
        ),
        "field": {
            "p": P_TOY,
            "extension_degree": E_TOY,
            "order": P_TOY**E_TOY,
            "modulus_coefficients_low_to_high": MODULUS,
            "modulus_irreducible": irreducible,
            "basis": ["1", "a", "a^2", "a^3", "a^4", "a^5"],
            "generator_encoded": generator_encoded,
            "generator_minimal_field_degree": minimal_field_degree(GENERATOR),
        },
        "code": {
            "object": "RS[F_(7^6), D=F_7^x, k=3] support-wise finite-slope MCA",
            "domain_in_base_field": DOMAIN_TOY,
            "n": N_TOY,
            "k": K_TOY,
            "agreement_A": A_TOY,
            "slack_t": T_TOY,
            "codewords": "evaluations of polynomials of degree less than three",
        },
        "received_line": {
            "f_values_encoded": [encode(value) for value in f_word],
            "g_values_encoded": [encode(value) for value in g_word],
            "formula": "f=(-a,0,0,0,0,1), g=(1,0,0,0,0,0)",
            "pair_minimal_field_degree": pair_field_degree,
            "pair_is_base_valued": pair_is_base_valued,
            "pair_descends_to_base_after_common_nonzero_scaling": (
                common_scalar_base_descent_exists
            ),
        },
        "exact_census": {
            "slopes_enumerated": P_TOY**E_TOY,
            "bad_records": bad_records,
            "bad_slope_set_encoded": bad_set,
            "full_degree_bad_slope_count": full_degree_count,
            "full_degree_count_divisible_by_six": full_degree_count % E_TOY == 0,
            "frobenius_conjugates_of_a_encoded": conjugates,
            "bad_set_frobenius_stable": bad_set_frobenius_stable,
            "a_pth_power_is_bad": conjugates[1] in bad_set,
        },
        "local_support_checks_for_the_unique_bad_slope": {
            "support_indices": support,
            "support_domain_points": [DOMAIN_TOY[index] for index in support],
            "exact_agreement_not_global_codeword": exact_agreement_not_global,
            "f_restriction_is_codeword": f_restriction_is_codeword,
            "g_restriction_is_codeword": g_restriction_is_codeword,
            "simultaneously_explained_on_support": simultaneously_explained,
            "earlier_owner_partition_complete": False,
            "use_of_counterexample": "refutes automatic fixed-line Frobenius closure only",
        },
        "verdict": "COUNTEREXAMPLE_TO_FIXED_LINE_FROBENIUS_ORBIT_CLAIM",
    }


@functools.cache
def qfin_replay() -> dict[str, int]:
    binomial = math.comb(N_KB, J_KB)
    numerator = B_REM * P_KB**W_KB
    return {
        "binom_bit_length": binomial.bit_length(),
        "p_to_w_bit_length": (P_KB**W_KB).bit_length(),
        "computed_K_rem": numerator // binomial,
    }


def derive_budget_audit() -> dict[str, Any]:
    replay = qfin_replay()
    require(replay["computed_K_rem"] == K_REM_QFIN, "K_rem replay drift")
    return {
        "row": {
            "p": P_KB,
            "extension_degree": E_KB,
            "q_line": str(Q_LINE_KB),
            "n": N_KB,
            "k": K_KB,
            "agreement_A": A_KB,
            "j": J_KB,
            "t": T_KB,
            "w": W_KB,
            "B_star": str(B_STAR),
        },
        "baseline": {
            "residual_base_slope_charge": str(BASE_SLOPE_CHARGE),
            "terminal_quotient_charge": str(TERMINAL_QUOTIENT),
            "U_paid": str(BASELINE_U_PAID),
            "B_rem": str(B_REM),
            "U_Q": None,
            "U_A": None,
        },
        "K_rem_qfin": {
            "value": K_REM_QFIN,
            "formula": "floor(B_rem*p^w/binom(n,j))",
            "role": "primitive Q-fin max-fiber multiplier relative to the prefix-fiber average",
            "is_direct_extension_degree_ceiling": False,
            **replay,
        },
        "direct_extension_dimension_degree_ledger": {
            "charge_formula": "Delta*p^e_Y",
            "total_open_inequality": "U_Q+U_A<=B_rem",
            "extension_charge_is_component_of": "U_A",
            "required_disjoint_decomposition": "U_A=U_ext+U_A_other",
            "component_available_reserve_formula": "B_rem-U_Q-U_A_other",
            "U_A_other": None,
            "all_remainder_allocation_is_provisional": True,
            "provisional_allocation_assumption": "U_Q=U_A_other=0",
            "max_Delta_if_e_Y_0_and_U_Q_U_A_other_zero": str(B_REM),
            "max_Delta_if_e_Y_1_and_U_Q_U_A_other_zero": B_REM // P_KB,
            "p_squared": str(P_KB**2),
            "e_Y_1_forced_out_by_direct_budget": False,
            "positive_degree_e_Y_ge_2_forced_out_by_direct_budget": P_KB**2 > B_REM,
        },
        "verdict": "K_REM_IS_NOT_THE_DIRECT_EXTENSION_CEILING",
    }


def source_binding(binding_id: str, rel_path: Path, role: str) -> dict[str, str]:
    path = ROOT / rel_path
    require(path.is_file(), f"missing source binding: {rel_path}")
    return {
        "binding_id": binding_id,
        "path": rel_path.as_posix(),
        "sha256": file_hash(path),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("audit-note", NOTE_REL, "corrected fixed-line and budget audit"),
        source_binding("python-verifier", VERIFIER_REL, "exact census and mutation verifier"),
        source_binding("sage-replay", SAGE_REL, "independent finite-field replay"),
        source_binding("v1-extension-target-note", V1_TARGET_NOTE_REL, "superseded target claims"),
        source_binding("v1-extension-target-packet", V1_TARGET_PACKET_REL, "superseded machine target"),
        source_binding(
            "v1-extension-target-verifier",
            V1_TARGET_VERIFIER_REL,
            "historical non-gating verifier with stale G8 source path",
        ),
        source_binding(
            "v1-extension-toy-scanner",
            V1_SCANNER_REL,
            "historical boundedness scanner with correction banner",
        ),
        source_binding(
            "v1-extension-toy-scan-packet",
            V1_SCANNER_PACKET_REL,
            "historical boundedness-only scan output",
        ),
        source_binding("base-slope-note", BASE_NOTE_REL, "corrected deployed paid baseline"),
        source_binding("base-slope-packet", BASE_PACKET_REL, "machine-readable deployed baseline"),
        source_binding("base-slope-verifier", BASE_VERIFIER_REL, "exact K_rem replay"),
        source_binding("minimal-field-descent", MIN_FIELD_REL, "projective datum field bookkeeping"),
        source_binding("galois-stabilizer-descent", STABILIZER_REL, "component routing only"),
        source_binding("full-orbit-cycle-descent", ORBIT_REL, "base-defined orbit-union descent"),
        source_binding("extension-coordinate-transfer", COORDINATE_REL, "multiplication-slice coordinate model"),
        source_binding("atlas-zero-chart-packet", ATLAS_PACKET_REL, "deployed chart provenance gate"),
        source_binding("dimension-degree-theorem", DIMENSION_DEGREE_REL, "direct Delta*p^e_Y charge"),
        source_binding(
            "first-form-aperiodic-ledger",
            FIRST_FORM_LEDGER_REL,
            "U_A definition and U_paid+U_Q+U_A staircase inequality",
        ),
    ]


def derive_routing_audit() -> dict[str, Any]:
    return {
        "base_slope_stratum": {
            "status": "PAID_BY_GLOBAL_BASE_SLOPE_UNIVERSE",
            "charge": str(P_KB),
        },
        "proper_subfield_strata": {
            "degrees": [2, 3],
            "status": "ROUTED_NOT_EXACTLY_PAID",
            "reason": (
                "minimal-field and stabilizer descent identify lower-arity targets but do not "
                "supply disjoint finite charges for the deployed row"
            ),
            "may_be_subtracted_from_extension_numerator_now": False,
        },
        "full_field_stratum": {
            "degree": 6,
            "fixed_line_bad_set_need_not_be_frobenius_stable": True,
            "base_defined_eliminant_root_envelope_is_frobenius_stable": True,
            "inclusion_exclusion_formula_for_base_defined_eliminant": (
                "deg(g6)-deg(g3)-deg(g2)+deg(g1)"
            ),
            "formula_counts_only_minimal_degree_six_roots": True,
            "formula_is_not_the_whole_extension_charge_until_tower_strata_paid": True,
        },
        "verdict": "ROUTING_IS_NOT_PAYMENT",
    }


def derive_supersession_gate() -> dict[str, Any]:
    packet = load_json(ROOT / V1_TARGET_PACKET_REL)
    supersession = packet.get("supersession")
    require(type(supersession) is dict, "v1 machine artifact lacks supersession block")
    expected_invalidations = [
        "bad slopes of one arbitrary fixed F-valued line automatically form complete Frobenius orbits",
        "proper-subfield strata are exactly paid merely because they route to lower arity",
        "Delta_ext_ceiling_int is a direct extension-chart degree ceiling",
    ]
    require(packet["meta"]["status"].startswith("SUPERSEDED_IN_PART"), "v1 meta status not superseded")
    require(supersession.get("status") == "SUPERSEDED_IN_PART", "v1 supersession status drift")
    require(
        supersession.get("superseded_by_certificate") == CERT_PATH.relative_to(ROOT).as_posix(),
        "v1 reverse certificate link drift",
    )
    require_json_equal(
        supersession.get("invalidated_interpretations"),
        expected_invalidations,
        "v1 invalidated interpretations",
    )
    require(supersession.get("acceptance_gate") is False, "v1 artifact remained an acceptance gate")
    scanner_text = (ROOT / V1_SCANNER_REL).read_text(encoding="utf-8")
    require("CORRECTION (2026-07-15)" in scanner_text, "historical scanner lacks correction banner")
    scanner_packet = load_json(ROOT / V1_SCANNER_PACKET_REL)
    require(
        scanner_packet.get("correction_status")
        == "SUPERSEDED_IN_PART / BOUNDEDNESS_EXPERIMENT_ONLY",
        "historical scan output lacks corrected status",
    )
    require(scanner_packet.get("boundedness_only") is True, "historical scan is not boundedness-only")
    require(
        scanner_packet.get("deployed_dimension_inference") is None,
        "historical scan retained a deployed dimension inference",
    )
    require("e_Y=0" not in scanner_packet["overall_verdict"], "historical verdict retained e_Y=0")
    return {
        "machine_artifact": V1_TARGET_PACKET_REL.as_posix(),
        "scanner": V1_SCANNER_REL.as_posix(),
        "scanner_packet": V1_SCANNER_PACKET_REL.as_posix(),
        "status": supersession["status"],
        "invalidated_interpretations": expected_invalidations,
        "historical_acceptance_gate": supersession["acceptance_gate"],
        "reverse_link_verified": True,
        "scanner_banner_verified": True,
        "scanner_output_boundedness_only": True,
    }


def derive_deployed_chart_gate() -> dict[str, Any]:
    packet = load_json(ROOT / ATLAS_PACKET_REL)
    family = packet["compressed_chart_families"][0]
    key = family["canonical_key_prefix"]
    gate = {
        "source_packet_charts_count": len(packet["charts"]),
        "represented_units": packet["coverage"]["represented_units"],
        "locator_chart_id": key["locator_chart_id"],
        "rank_s": key["rank_s"],
        "pivot_rows": key["pivot_rows"],
        "pivot_cols": key["pivot_cols"],
        "extension_valued_excluded": family["gate_scope"]["extension_valued_excluded"],
        "source_derived_deployed_extension_chart_exists": False,
        "missing_inputs": [
            "fixed deployed received pair or uniform symbolic received-pair chart",
            "locator patch equations and localization",
            "pinned F_(p^6) modulus and basis",
            "rank and pivot witnesses",
            "branch-1-through-5 complement equations",
            "localized eliminant or dimension-degree projection certificate",
        ],
        "terminal": "UNPAID_PRIMITIVE",
        "verdict": "RED_NO_SOURCE_DERIVED_DEPLOYED_CHART",
    }
    require(gate["source_packet_charts_count"] == 0, "#810 unexpectedly gained charts")
    require(gate["represented_units"] == 0, "#810 unexpectedly represents units")
    require(gate["locator_chart_id"] == "UNMAPPED_SPI_CHART", "#810 locator provenance drift")
    require(gate["rank_s"] is None, "#810 unexpectedly has a rank")
    require(gate["pivot_rows"] == [] and gate["pivot_cols"] == [], "#810 unexpectedly has pivots")
    require(gate["extension_valued_excluded"] is True, "#810 extension scope drift")
    return gate


def corrected_contract() -> dict[str, Any]:
    return {
        "actual_fixed_line_bad_count": (
            "count directly or by an eliminant over F; no Frobenius divisibility assumed"
        ),
        "base_eliminant_root_envelope": (
            "if E is in F_p[Z], minimal-degree-six roots use inclusion-exclusion and occur in six-orbits"
        ),
        "arbitrary_F_coefficient_eliminant": (
            "a coefficient norm may give an F_p envelope with degree at most six times larger"
        ),
        "tower_strata": "UNPAID_TOWER until exact disjoint lower-arity charges are cited",
        "extension_charge": "sum Delta*p^e_Y directly",
        "total_open_inequality": "U_Q+U_A<=B_rem",
        "extension_component_accounting": (
            "after a disjoint U_A=U_ext+U_A_other partition, U_ext<=B_rem-U_Q-U_A_other"
        ),
        "chart_terminal_without_source_binding": "UNPAID_PRIMITIVE",
        "historical_v1_verifier_is_acceptance_gate": False,
        "historical_v1_verifier_non_gating_reason": (
            "it verifies the superseded ceiling semantics and currently fails only its stale G8 source path"
        ),
        "superseded_v1_machine_artifact": V1_TARGET_PACKET_REL.as_posix(),
        "no_row_claim": True,
    }


NONCLAIMS = [
    "The counterexample does not refute zero-dimensionality or a field-size-independent extension bound.",
    "The counterexample is an exact rate-1/2 t=2 toy, not a deployed KoalaBear received line.",
    "The packet does not pay the F_(p^2) or F_(p^3) tower strata.",
    "The packet does not supply a source-derived deployed SPI chart or eliminant.",
    "The packet does not determine U_Q, U_A, U_A_other, or the final KoalaBear inequality.",
    "The all-remainder dimension caps are provisional allocations, not banked charges.",
]


def build_certificate() -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "COUNTEREXAMPLE_AND_CONTRACT_CORRECTION",
        "artifact_kind": "FIXED_LINE_FROBENIUS_AND_EXTENSION_BUDGET_AUDIT",
        "source_bindings": expected_source_bindings(),
        "fixed_line_counterexample": derive_counterexample(),
        "koalabear_budget_audit": derive_budget_audit(),
        "routing_audit": derive_routing_audit(),
        "supersession_gate": derive_supersession_gate(),
        "deployed_chart_gate": derive_deployed_chart_gate(),
        "corrected_contract": corrected_contract(),
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_certificate(artifact: dict[str, Any]) -> None:
    require(set(artifact) == TOP_KEYS, "top-level keys drift")
    require(artifact["schema"] == SCHEMA, "schema drift")
    require(artifact["status"] == "COUNTEREXAMPLE_AND_CONTRACT_CORRECTION", "status drift")
    require(
        artifact["artifact_kind"] == "FIXED_LINE_FROBENIUS_AND_EXTENSION_BUDGET_AUDIT",
        "artifact kind drift",
    )
    require_json_equal(artifact["source_bindings"], expected_source_bindings(), "source binding")
    require_json_equal(
        artifact["fixed_line_counterexample"], derive_counterexample(), "counterexample"
    )
    require_json_equal(
        artifact["koalabear_budget_audit"], derive_budget_audit(), "budget audit"
    )
    require_json_equal(artifact["routing_audit"], derive_routing_audit(), "routing audit")
    require_json_equal(
        artifact["supersession_gate"], derive_supersession_gate(), "supersession gate"
    )
    require_json_equal(
        artifact["deployed_chart_gate"], derive_deployed_chart_gate(), "chart gate"
    )
    require_json_equal(artifact["corrected_contract"], corrected_contract(), "corrected contract")
    require_json_equal(artifact["nonclaims"], NONCLAIMS, "nonclaims")
    require(artifact["payload_sha256"] == payload_hash(artifact), "payload hash drift")


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(build_certificate(), indent=2) + "\n", encoding="utf-8")


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    current = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def mutation_selftest() -> None:
    base = build_certificate()
    counterexample = base["fixed_line_counterexample"]
    bad_slope = counterexample["exact_census"]["bad_slope_set_encoded"][0]
    first_conjugate = counterexample["exact_census"]["frobenius_conjugates_of_a_encoded"][1]
    cases: list[tuple[str, tuple[Any, ...], Any, bool]] = [
        ("wrong-modulus", ("fixed_line_counterexample", "field", "modulus_coefficients_low_to_high", 0), 3, True),
        ("bool-to-int", ("fixed_line_counterexample", "field", "modulus_irreducible"), 1, True),
        ("wrong-slack", ("fixed_line_counterexample", "code", "slack_t"), 1, True),
        ("wrong-domain", ("fixed_line_counterexample", "code", "domain_in_base_field", 0), 0, True),
        ("false-common-scalar-descent", ("fixed_line_counterexample", "received_line", "pair_descends_to_base_after_common_nonzero_scaling"), True, True),
        ("insert-frobenius-conjugate", ("fixed_line_counterexample", "exact_census", "bad_slope_set_encoded"), [bad_slope, first_conjugate], True),
        ("false-orbit-divisibility", ("fixed_line_counterexample", "exact_census", "full_degree_count_divisible_by_six"), True, True),
        ("false-frobenius-stability", ("fixed_line_counterexample", "exact_census", "bad_set_frobenius_stable"), True, True),
        ("false-global-codeword", ("fixed_line_counterexample", "local_support_checks_for_the_unique_bad_slope", "exact_agreement_not_global_codeword"), False, True),
        ("false-owner-partition", ("fixed_line_counterexample", "local_support_checks_for_the_unique_bad_slope", "earlier_owner_partition_complete"), True, True),
        ("wrong-K-rem-role", ("koalabear_budget_audit", "K_rem_qfin", "is_direct_extension_degree_ceiling"), True, True),
        ("int-to-float", ("koalabear_budget_audit", "K_rem_qfin", "value"), float(K_REM_QFIN), True),
        ("wrong-dimension-one-cap", ("koalabear_budget_audit", "direct_extension_dimension_degree_ledger", "max_Delta_if_e_Y_1_and_U_Q_U_A_other_zero"), 129_056_130, True),
        ("U-A-other-null-to-zero", ("koalabear_budget_audit", "direct_extension_dimension_degree_ledger", "U_A_other"), 0, True),
        ("force-dimension-one-out", ("koalabear_budget_audit", "direct_extension_dimension_degree_ledger", "e_Y_1_forced_out_by_direct_budget"), True, True),
        ("U-Q-null-to-zero", ("koalabear_budget_audit", "baseline", "U_Q"), 0, True),
        ("U-A-null-to-zero", ("koalabear_budget_audit", "baseline", "U_A"), 0, True),
        ("tower-falsely-paid", ("routing_audit", "proper_subfield_strata", "status"), "PAID_BY_THEOREM", True),
        ("subtract-unpaid-tower", ("routing_audit", "proper_subfield_strata", "may_be_subtracted_from_extension_numerator_now"), True, True),
        ("restore-v1-gate", ("supersession_gate", "historical_acceptance_gate"), True, True),
        ("invent-deployed-chart", ("deployed_chart_gate", "source_derived_deployed_extension_chart_exists"), True, True),
        ("false-row-claim", ("corrected_contract", "no_row_claim"), False, True),
        ("promote-historical-gate", ("corrected_contract", "historical_v1_verifier_is_acceptance_gate"), True, True),
        ("source-hash-drift", ("source_bindings", 0, "sha256"), "0" * 64, True),
        ("payload-drift", ("payload_sha256",), "0" * 64, False),
    ]
    caught = 0
    for label, path, replacement, rehash in cases:
        candidate = copy.deepcopy(base)
        set_path(candidate, path, replacement)
        if rehash:
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except VerificationError:
            caught += 1
        else:
            raise VerificationError(f"mutation survived: {label}")

    duplicate = '{"schema":"x","schema":"y"}'
    try:
        parse_json(duplicate, "duplicate-control")
    except VerificationError:
        caught += 1
    else:
        raise VerificationError("duplicate-key mutation survived")
    try:
        parse_json('{"x":NaN}', "constant-control")
    except VerificationError:
        caught += 1
    else:
        raise VerificationError("nonstandard-constant mutation survived")
    require(caught == len(cases) + 2, "mutation count drift")
    print(f"TAMPER SELFTEST: PASS ({caught} mutations caught)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    require(args.write or args.check or args.tamper_selftest, "select --write, --check, or --tamper-selftest")
    if args.write:
        write_certificate()
        print(f"WROTE: {CERT_PATH.relative_to(ROOT)}")
    if args.check:
        artifact = load_json(CERT_PATH)
        validate_certificate(artifact)
        counterexample = artifact["fixed_line_counterexample"]["exact_census"]
        budget = artifact["koalabear_budget_audit"]
        print(
            "CHECK: PASS "
            f"(bad slopes {counterexample['bad_slope_set_encoded']}; "
            f"full-degree count {counterexample['full_degree_bad_slope_count']}; "
            f"B_rem {budget['baseline']['B_rem']}; "
            f"eY1 provisional Delta cap "
            f"{budget['direct_extension_dimension_degree_ledger']['max_Delta_if_e_Y_1_and_U_Q_U_A_other_zero']})"
        )
    if args.tamper_selftest:
        mutation_selftest()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
