#!/usr/bin/env python3
r"""Verify the KoalaBear A=1116048 residual base-slope universe charge.

The MCA numerator counts distinct slopes.  After any earlier first-match
owners are removed, the remaining slopes lying in the base field F_p form a
subset of F_p and therefore cost at most p, globally once.  This packet
replaces (rather than adds to) the older conditional t*p image-cell charge.
It does not bound slopes in F_(p^6) \ F_p or close the deployed row.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-kb-1116048-base-slope-universe-v2"
CERT_DIR = ROOT / "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2"
CERT_PATH = CERT_DIR / "kb_mca_1116048_base_slope_universe_v2.json"
NOTE_REL = Path("experimental/notes/thresholds/kb_mca_1116048_base_slope_universe_v2.md")
VERIFIER_REL = Path("experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py")
DEFINITION_REL = Path("experimental/rs_mca_thresholds.tex")
FIRST_MATCH_REL = Path("archived/grande_finale_v2.tex")
V1_NOTE_REL = Path("experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md")
V1_PACKET_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/"
    "kb_mca_1116048_first_match_ledger_v1.json"
)
V1_VERIFIER_REL = Path("experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py")

P = 2_130_706_433
E = 6
Q_LINE = P**E
N = 2_097_152
K = 1_048_576
A = 1_116_048
J = N - A
T = A - K
W = T - 1
DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
TERMINAL_QUOTIENT = 471_447_040
OLD_TP_CHARGE = T * P
OLD_U_PAID = OLD_TP_CHARGE + TERMINAL_QUOTIENT
BASE_SLOPE_CHARGE = P
U_PAID = BASE_SLOPE_CHARGE + TERMINAL_QUOTIENT
B_REM = B_STAR - U_PAID
CHARGE_REDUCTION = OLD_U_PAID - U_PAID
K_REM = 4_807_520

ROW_KEYS = {
    "row_id",
    "p",
    "extension_degree",
    "q_line",
    "n",
    "k",
    "agreement_A",
    "j",
    "t",
    "w",
    "B_star",
    "challenge_scope",
}
THEOREM_KEYS = {
    "name",
    "counted_object",
    "first_match_input",
    "residual_set",
    "set_inclusion",
    "global_once_bound",
    "uniform_in_received_line",
    "infinity_included",
    "requires_affine_row_adapter",
    "requires_base_valued_received_words",
    "requires_honest_lift_classifier",
    "terminal_quotient_support_to_slope_bound",
    "does_not_bound",
}
FIRST_MATCH_KEYS = {
    "v1_order",
    "v2_order",
    "replacement_index_one_based",
    "replacement_owner",
    "earlier_owner_disjointness_required",
    "old_generated_collision_owner_retained_as_optional_refinement",
}
CHARGE_KEYS = {
    "charge_id",
    "owner_id",
    "amount",
    "scope",
    "source_binding_id",
    "source_pointer",
}
ARITHMETIC_KEYS = {
    "old_t_p_charge",
    "old_U_paid",
    "new_base_slope_charge",
    "terminal_quotient_charge",
    "new_U_paid",
    "charge_reduction",
    "B_rem",
    "K_rem",
    "old_charge_is_replaced_not_added",
    "U_Q",
    "U_A",
    "lhs",
    "inequality_status",
}
NONCLAIMS = [
    "This packet does not prove the KoalaBear A=1116048 row safe.",
    "This packet does not bound extension-valued residual slopes.",
    "This packet does not determine U_Q or U_A.",
    "This packet replaces the t*p charge; it must never be added to it.",
    "This packet does not turn supports, witnesses, or SPI charts into counted numerator units.",
]

V1_ORDER = [
    "contained_or_noncontained_failure",
    "rank_drop_or_pivot_failure",
    "tangent_common_line_residue",
    "quotient_periodic_or_divisor_stabilized",
    "planted_prefix_structured",
    "extension_valued_slope",
    "base_generated_field_collision",
    "sparse_sigma_or_sparse_support",
    "m1_half_turn_or_coefficient_shadow",
    "primitive_qfin_residual",
]
V2_ORDER = [*V1_ORDER]
V2_ORDER[6] = "residual_base_slope_universe"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


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


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(relative: Path) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_row() -> dict[str, Any]:
    return {
        "row_id": "koalabear-mca-A1116048",
        "p": P,
        "extension_degree": E,
        "q_line": str(Q_LINE),
        "n": N,
        "k": K,
        "agreement_A": A,
        "j": J,
        "t": T,
        "w": W,
        "B_star": str(B_STAR),
        "challenge_scope": "all finite slopes in F_(p^6)",
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        binding("mca-definition", DEFINITION_REL, "distinct-slope numerator and fixed-support injection"),
        binding("first-match-ledger", FIRST_MATCH_REL, "slope-level disjoint first-match assignment"),
        binding("v1-note", V1_NOTE_REL, "predecessor first-match statement"),
        binding("v1-packet", V1_PACKET_REL, "predecessor exact charges and branch order"),
        binding("v1-verifier", V1_VERIFIER_REL, "predecessor arithmetic replay"),
        binding("v2-note", NOTE_REL, "proof and nonclaims"),
        binding("v2-verifier", VERIFIER_REL, "exact arithmetic and tamper replay"),
    ]


def expected_theorem() -> dict[str, Any]:
    return {
        "name": "residual base-slope universe bound",
        "counted_object": "distinct support-wise MCA-bad finite slopes of one received line",
        "first_match_input": "remove branches 1 through 6 before assigning branch 7",
        "residual_set": "Bad_A(r0,r1) intersect F_p minus all earlier first-match assignments",
        "set_inclusion": "residual_set subseteq F_p",
        "global_once_bound": str(P),
        "uniform_in_received_line": True,
        "infinity_included": False,
        "requires_affine_row_adapter": False,
        "requires_base_valued_received_words": False,
        "requires_honest_lift_classifier": False,
        "terminal_quotient_support_to_slope_bound": "each noncommon support contributes at most one finite bad slope",
        "does_not_bound": "slopes in F_(p^6) minus F_p",
    }


def expected_first_match() -> dict[str, Any]:
    return {
        "v1_order": V1_ORDER,
        "v2_order": V2_ORDER,
        "replacement_index_one_based": 7,
        "replacement_owner": "residual_base_slope_universe",
        "earlier_owner_disjointness_required": True,
        "old_generated_collision_owner_retained_as_optional_refinement": True,
    }


def expected_charges() -> list[dict[str, str]]:
    return [
        {
            "charge_id": "kb-terminal-quotient-raw",
            "owner_id": "quotient_periodic_or_divisor_stabilized",
            "amount": str(TERMINAL_QUOTIENT),
            "scope": "FIRST_MATCH_GLOBAL_ONCE",
            "source_binding_id": "v1-packet",
            "source_pointer": "/deployed_arithmetic/terminal_quotient_raw_paid_cost",
        },
        {
            "charge_id": "kb-residual-base-slope-universe",
            "owner_id": "residual_base_slope_universe",
            "amount": str(BASE_SLOPE_CHARGE),
            "scope": "FIRST_MATCH_GLOBAL_ONCE",
            "source_binding_id": "v1-packet",
            "source_pointer": "/deployed_arithmetic/p",
        },
    ]


def expected_arithmetic() -> dict[str, Any]:
    return {
        "old_t_p_charge": str(OLD_TP_CHARGE),
        "old_U_paid": str(OLD_U_PAID),
        "new_base_slope_charge": str(BASE_SLOPE_CHARGE),
        "terminal_quotient_charge": str(TERMINAL_QUOTIENT),
        "new_U_paid": str(U_PAID),
        "charge_reduction": str(CHARGE_REDUCTION),
        "B_rem": str(B_REM),
        "K_rem": K_REM,
        "old_charge_is_replaced_not_added": True,
        "U_Q": None,
        "U_A": None,
        "lhs": None,
        "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
    }


@functools.cache
def exact_multiplier(budget: int) -> int:
    return (budget * P**W) // math.comb(N, J)


def validate_v1_source() -> dict[str, Any]:
    packet = load_json(ROOT / V1_PACKET_REL)
    arith = packet["deployed_arithmetic"]
    expected_integers = {
        "p": P,
        "q_line": Q_LINE,
        "n": N,
        "k": K,
        "A_adjacent_candidate": A,
        "j": J,
        "t": T,
        "prefix_depth_w": W,
        "B_star_floor_q_minus_1_over_2^128": B_STAR,
        "B_gen_t_times_p": OLD_TP_CHARGE,
        "terminal_quotient_raw_paid_cost": TERMINAL_QUOTIENT,
    }
    for key, expected in expected_integers.items():
        require(type(arith[key]) is int and arith[key] == expected, f"v1 integer drift: {key}")
    branches = packet["first_match_branches"]
    require(type(branches) is list and all(type(branch) is dict for branch in branches), "v1 branch shape drift")
    require([branch["branch"] for branch in branches] == V1_ORDER, "v1 first-match order drift")
    require(branches[3]["deducted_in_proved_ledger"] is True, "v1 terminal quotient is not paid")
    require(branches[6]["deducted_in_proved_ledger"] is True, "v1 generated bucket is not paid")
    return packet


def build_certificate() -> dict[str, Any]:
    validate_v1_source()
    definition = (ROOT / DEFINITION_REL).read_text(encoding="utf-8")
    normalized_definition = " ".join(definition.split())
    require("It counts slopes, not witnesses or supports." in normalized_definition, "MCA numerator semantics drift")
    require(
        "Consequently a noncommon support contributes at most one finite MCA-bad slope." in normalized_definition,
        "fixed-support slope injection drift",
    )
    first_match_source = " ".join((ROOT / FIRST_MATCH_REL).read_text(encoding="utf-8").split())
    require("[first-match upper ledger]" in first_match_source, "first-match definition drift")
    require("are disjoint and cover all bad slopes." in first_match_source, "first-match disjointness drift")
    require(Q_LINE // DENOMINATOR == B_STAR, "full-denominator budget equality drift")
    require(exact_multiplier(B_REM) == K_REM, "exact K_rem drift")
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PROVED_UPPER_NUMERATOR_REPLACEMENT",
        "row": expected_row(),
        "source_bindings": expected_source_bindings(),
        "theorem": expected_theorem(),
        "first_match": expected_first_match(),
        "charges": expected_charges(),
        "arithmetic": expected_arithmetic(),
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    require(set(value) == expected, f"{label} keys drift")


def resolve_pointer(value: Any, pointer: str) -> Any:
    current = value
    for token in pointer.lstrip("/").split("/"):
        current = current[token.replace("~1", "/").replace("~0", "~")]
    return current


def validate_certificate(cert: dict[str, Any]) -> None:
    require_exact_keys(
        cert,
        {"schema", "status", "row", "source_bindings", "theorem", "first_match", "charges", "arithmetic", "nonclaims", "payload_sha256"},
        "top-level",
    )
    require(cert["schema"] == SCHEMA, "schema drift")
    require(cert["status"] == "PROVED_UPPER_NUMERATOR_REPLACEMENT", "status drift")
    require(cert["payload_sha256"] == payload_hash(cert), "payload hash drift")
    row = cert["row"]
    require(type(row) is dict, "row is not an object")
    require_exact_keys(row, ROW_KEYS, "row")
    require(canonical_bytes(row) == canonical_bytes(expected_row()), "row payload or JSON type drift")
    require(type(cert["source_bindings"]) is list, "source_bindings is not a list")
    require(
        canonical_bytes(cert["source_bindings"]) == canonical_bytes(expected_source_bindings()),
        "source binding map drift",
    )
    ids: set[str] = set()
    binding_by_id: dict[str, dict[str, Any]] = {}
    for source in cert["source_bindings"]:
        require(type(source) is dict, "source binding is not an object")
        require_exact_keys(source, {"binding_id", "path", "sha256", "role"}, "source binding")
        require(all(type(source[key]) is str for key in ("binding_id", "path", "sha256", "role")), "source binding type drift")
        source_id = source["binding_id"]
        require(source_id not in ids, "duplicate source binding")
        ids.add(source_id)
        path = Path(source["path"])
        require(not path.is_absolute() and ".." not in path.parts, "unsafe source path")
        require(source["sha256"] == file_hash(path), f"source hash drift: {path}")
        binding_by_id[source_id] = load_json(ROOT / path) if path.suffix == ".json" else {"_text": True}
    require(
        ids == {"mca-definition", "first-match-ledger", "v1-note", "v1-packet", "v1-verifier", "v2-note", "v2-verifier"},
        "source binding ids drift",
    )
    theorem = cert["theorem"]
    require(type(theorem) is dict, "theorem is not an object")
    require_exact_keys(theorem, THEOREM_KEYS, "theorem")
    require(canonical_bytes(theorem) == canonical_bytes(expected_theorem()), "theorem payload or JSON type drift")
    first_match = cert["first_match"]
    require(type(first_match) is dict, "first_match is not an object")
    require_exact_keys(first_match, FIRST_MATCH_KEYS, "first_match")
    require(canonical_bytes(first_match) == canonical_bytes(expected_first_match()), "first-match payload or JSON type drift")
    charges = cert["charges"]
    require(type(charges) is list, "charges is not a list")
    require(canonical_bytes(charges) == canonical_bytes(expected_charges()), "charge specs or JSON types drift")
    for charge in charges:
        require(type(charge) is dict, "charge is not an object")
        require_exact_keys(charge, CHARGE_KEYS, "charge")
        source_value = resolve_pointer(binding_by_id["v1-packet"], charge["source_pointer"])
        require(type(source_value) is int and charge["amount"] == str(source_value), "charge amount/source drift")
    amounts = {charge["owner_id"]: int(charge["amount"]) for charge in charges}
    arith = cert["arithmetic"]
    require(type(arith) is dict, "arithmetic is not an object")
    require_exact_keys(arith, ARITHMETIC_KEYS, "arithmetic")
    require(canonical_bytes(arith) == canonical_bytes(expected_arithmetic()), "arithmetic payload or JSON type drift")
    require(sum(amounts.values()) == U_PAID, "charge sum drift")
    require(arith["K_rem"] == exact_multiplier(B_REM), "K_rem exact replay drift")
    require(cert["nonclaims"] == NONCLAIMS, "nonclaims drift")


def rehash(cert: dict[str, Any]) -> None:
    cert["payload_sha256"] = payload_hash(cert)


def mutation_cases(base: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def changed(label: str, path: tuple[Any, ...], value: Any, *, hash_it: bool = True) -> None:
        candidate = copy.deepcopy(base)
        cursor: Any = candidate
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        if hash_it:
            rehash(candidate)
        cases.append((label, candidate))

    changed("wrong-p", ("row", "p"), P + 1)
    changed("floating-extension-degree", ("row", "extension_degree"), float(E))
    changed("wrong-line-field", ("row", "q_line"), str(Q_LINE + 1))
    changed("wrong-budget", ("row", "B_star"), str(B_STAR + 1))
    changed("support-counted-object", ("theorem", "counted_object"), "supports")
    changed(
        "prefix-preserving-counted-object",
        ("theorem", "counted_object"),
        "distinct support-wise MCA-bad finite slopes plus all support witnesses",
    )
    changed("wrong-base-universe", ("theorem", "global_once_bound"), str(P + 1))
    changed("fractional-base-universe", ("theorem", "global_once_bound"), P + 0.5)
    changed("infinity-included", ("theorem", "infinity_included"), True)
    changed("adapter-required", ("theorem", "requires_affine_row_adapter"), True)
    changed("owner-order-swap", ("first_match", "v2_order"), [V2_ORDER[1], V2_ORDER[0], *V2_ORDER[2:]])
    changed("wrong-replacement-index", ("first_match", "replacement_index_one_based"), 6)
    changed("non-global-charge", ("charges", 1, "scope"), "PER_CHART")
    changed("renamed-charge-id", ("charges", 1, "charge_id"), "arbitrary-base-charge")
    changed("fractional-charge", ("charges", 1, "amount"), P + 0.5)
    changed("wrong-charge-pointer", ("charges", 1, "source_pointer"), "/deployed_arithmetic/t")
    changed("same-value-base-pointer-alias", ("charges", 1, "source_pointer"), "/row_packet/q_gen")
    changed(
        "same-value-quotient-pointer-alias",
        ("charges", 0, "source_pointer"),
        "/quotient_planted_descent/terminal_raw_paid_cost",
    )
    changed("wrong-U-paid", ("arithmetic", "new_U_paid"), str(U_PAID + 1))
    changed("wrong-reduction", ("arithmetic", "charge_reduction"), str(CHARGE_REDUCTION + 1))
    changed("wrong-B-rem", ("arithmetic", "B_rem"), str(B_REM + 1))
    changed("wrong-K-rem", ("arithmetic", "K_rem"), K_REM - 1)
    changed("floating-K-rem", ("arithmetic", "K_rem"), float(K_REM))
    changed("add-old-charge", ("arithmetic", "old_charge_is_replaced_not_added"), False)
    changed("false-closed-inequality", ("arithmetic", "inequality_status"), "PROVED_PASS")
    changed("source-hash-drift", ("source_bindings", 0, "sha256"), "0" * 64)
    changed("source-role-drift", ("source_bindings", 0, "role"), "unrelated role")
    source_alias = copy.deepcopy(base)
    source_alias["source_bindings"][0]["path"] = V1_NOTE_REL.as_posix()
    source_alias["source_bindings"][0]["sha256"] = file_hash(V1_NOTE_REL)
    rehash(source_alias)
    cases.append(("source-path-with-matching-hash-alias", source_alias))
    changed("payload-hash-drift", ("status",), "PARTIAL", hash_it=False)
    unknown = copy.deepcopy(base)
    unknown["theorem"]["unexpected"] = True
    rehash(unknown)
    cases.append(("unknown-key", unknown))
    return cases


def tamper_selftest() -> int:
    base = build_certificate()
    validate_certificate(base)
    cases = mutation_cases(base)
    for label, candidate in cases:
        try:
            validate_certificate(candidate)
        except (VerificationError, KeyError, TypeError, ValueError):
            continue
        raise VerificationError(f"mutation was not rejected: {label}")
    parser_cases = [
        ('{"x":1,"x":2}', "duplicate-key"),
        ('{"x":NaN}', "nonstandard-constant"),
    ]
    for text, label in parser_cases:
        try:
            parse_json(text, label)
        except VerificationError:
            continue
        raise VerificationError(f"parser mutation was not rejected: {label}")
    return len(cases)


def write_artifact() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(build_certificate(), indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the deterministic certificate")
    parser.add_argument("--check", action="store_true", help="validate and exactly regenerate the stored certificate")
    parser.add_argument("--tamper-selftest", action="store_true", help="run semantic and parser mutations")
    args = parser.parse_args()
    if args.write:
        write_artifact()
    if args.check:
        stored = load_json(CERT_PATH)
        validate_certificate(stored)
        require(stored == build_certificate(), "stored certificate drift")
        print(
            "CHECK: PASS (base slope charge %d; U_paid %d; B_rem %d; K_rem %d)"
            % (P, U_PAID, B_REM, K_REM)
        )
    if args.tamper_selftest:
        count = tamper_selftest()
        print(f"TAMPER SELFTEST: PASS ({count} semantic + 2 parser mutations rejected)")
    if not (args.write or args.check or args.tamper_selftest):
        validate_certificate(build_certificate())
        print("generated certificate validates; use --write, --check, or --tamper-selftest")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
