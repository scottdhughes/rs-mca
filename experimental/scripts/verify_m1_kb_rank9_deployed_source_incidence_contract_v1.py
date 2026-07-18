#!/usr/bin/env python3
"""Verify the deployed rank-nine source-incidence readiness contract.

This packet has two deliberately separate jobs.

* It audits the bound predecessor artifacts and fails closed when neither a
  row-uniform theorem nor an exhaustive deployed source/selector census is
  present.
* It executes the rich-pencil identity on small declared source-compatible
  families from raw words, graph coordinates, supports, and K0 generator rows.

It does not construct the missing KoalaBear source family and therefore does
not move the deployed ledger.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-rank9-deployed-source-incidence-contract-v1"
ARTIFACT_KIND = "M1_KB_RANK9_DEPLOYED_SOURCE_INCIDENCE_READINESS_ROUTE_CUT"
STATUS = "PROVED_EXECUTABLE_READINESS_AUDIT_AND_EXACT_TOY_INCIDENCE_KERNEL"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-deployed-source-incidence-contract-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_deployed_source_incidence_contract_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_deployed_source_incidence_contract_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-deployed-source-incidence-contract-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py"
)

MASK_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_5_mask_contract_v1.md"
)
MASK_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-5-mask-contract-v1/"
    "m1_kb_branch3_5_mask_contract_v1.json"
)
SYNDROME_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md"
)
SYNDROME_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-syndrome-rank-reduction-v1/"
    "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.json"
)
CORE_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_actual_core_mds_rank_ladder_v1.md"
)
CORE_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-actual-core-mds-v1/"
    "m1_kb_branch3_actual_core_mds_v1.json"
)
MASK_DEFICIT_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md"
)
MASK_DEFICIT_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-mask-deficit-v1/"
    "m1_kb_branch3_rank9_mask_deficit_v1.json"
)
FIXED_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md"
)
FIXED_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-fixed-basis-fibre-v1/"
    "m1_kb_branch3_rank9_fixed_basis_fibre_v1.json"
)
RICH_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)
RICH_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-rich-pencil-atlas-v1/"
    "m1_kb_branch3_rank9_rich_pencil_atlas_v1.json"
)
TOY_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_t2_core_source_coordinate_cover_v1.md"
)
TOY_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-t2-core-source-coordinate-cover-v1/"
    "m1_kb_branch3_t2_core_source_coordinate_cover_v1.json"
)

P = 2_130_706_433
EXTENSION_DEGREE = 6
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
T = A - K
CORE_R = 8
CUTOFF_D = 18_014
UNIFORM_CAP = 20
TAIL_TARGET = 17_907_572_507_584
Q_LINE = P**EXTENSION_DEGREE
B_STAR = (Q_LINE - 1) // (1 << 128)
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID
E_MAX = (
    5_284_485_264_881_189_380_664_190_436_821_715_347_228_277_374
)


class ContractError(RuntimeError):
    """A source, schema, arithmetic, or semantic contract failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ContractError(f"nonstandard JSON constant: {value}")


def reject_float(value: str) -> None:
    raise ContractError(f"floating-point JSON number: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path}")
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing bound source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def predecessor_fingerprint(relative: Path) -> str:
    data = load_json(ROOT / relative)
    if "payload_sha256" in data:
        require(
            data.get("payload_sha256") == payload_hash(data),
            f"bad predecessor payload: {relative}",
        )
        return "payload-sha256:" + str(data["payload_sha256"])
    return "file-sha256:" + file_hash(relative)


def exact_int(value: Any, label: str) -> int:
    require(type(value) is int, f"{label} must be an exact integer")
    return value


def exact_int_list(value: Any, label: str) -> list[int]:
    require(type(value) is list, f"{label} must be a list")
    result = [exact_int(entry, f"{label}[{index}]") for index, entry in enumerate(value)]
    return result


def inverse_mod(value: int, prime: int) -> int:
    value %= prime
    require(value != 0, "attempted inversion of zero")
    return pow(value, prime - 2, prime)


def matrix_rank_mod(rows: list[list[int]], prime: int) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    work = [[entry % prime for entry in row] for row in rows]
    rank = 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inverse_mod(work[rank][column], prime)
        work[rank] = [(entry * scale) % prime for entry in work[rank]]
        for index in range(len(work)):
            if index == rank or work[index][column] == 0:
                continue
            factor = work[index][column]
            work[index] = [
                (left - factor * right) % prime
                for left, right in zip(work[index], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def polynomial_values(coefficients: list[int], domain: list[int], prime: int) -> list[int]:
    values: list[int] = []
    for point in domain:
        value = 0
        for coefficient in reversed(coefficients):
            value = (value * point + coefficient) % prime
        values.append(value)
    return values


def polynomial_degree(coefficients: list[int], prime: int) -> int:
    for index in range(len(coefficients) - 1, -1, -1):
        if coefficients[index] % prime:
            return index
    return -1


def line_key(alpha: tuple[int, ...], beta: tuple[int, ...]) -> str:
    return ",".join(map(str, alpha)) + "|" + ",".join(map(str, beta))


def explicit_high_fixture() -> dict[str, Any]:
    return {
        "schema": "rs-mca-explicit-source-incidence-fixture-v1",
        "scope": "DECLARED_SELECTED_FAMILY_TOY",
        "field_prime": 7,
        "domain": [0, 1, 2, 3, 4, 5],
        "k": 3,
        "j": 3,
        "cutoff_D": 1,
        "core_rank": 2,
        "uniform_cap": 2,
        "generator_rows": [[1, point] for point in range(6)],
        "u": [0, 0, 0, 1, 1, 1],
        "v": [0, 0, 0, 1, 2, 3],
        "source_pair": {
            "epsilon_0": [0, 0, 0, 1, 1, 1],
            "epsilon_1": [0, 0, 0, 1, 2, 3],
        },
        "selected": [
            {"slope": eta, "z": [0, 0], "error_support": support, "delta": delta}
            for eta, support, delta in [
                (0, [3, 4, 5], 0),
                (1, [3, 4, 5], 0),
                (2, [3, 4], 1),
                (3, [3, 5], 1),
            ]
        ],
        "line_lifts": {
            "0,0|0,0": {"P_coefficients": [0], "Q_coefficients": [0]}
        },
        "expected": {
            "declared_slope_count": 4,
            "filtered_slope_count": 4,
            "independent_basis_count": 15,
            "rich_line_count": 1,
            "rich_line_sizes": [4],
            "beta_profile": [3],
            "direct_excess": 6,
            "atlas_excess": 6,
        },
    }


def explicit_low_fixture() -> dict[str, Any]:
    value = explicit_high_fixture()
    value["selected"] = value["selected"][:2]
    value["line_lifts"] = {}
    value["expected"] = {
        "declared_slope_count": 2,
        "filtered_slope_count": 2,
        "independent_basis_count": 15,
        "rich_line_count": 0,
        "rich_line_sizes": [],
        "beta_profile": [],
        "direct_excess": 0,
        "atlas_excess": 0,
    }
    return value


def explicit_empty_fixture() -> dict[str, Any]:
    value = explicit_high_fixture()
    value["selected"] = []
    value["line_lifts"] = {}
    value["expected"] = {
        "declared_slope_count": 0,
        "filtered_slope_count": 0,
        "independent_basis_count": 15,
        "rich_line_count": 0,
        "rich_line_sizes": [],
        "beta_profile": [],
        "direct_excess": 0,
        "atlas_excess": 0,
    }
    return value


def validate_explicit_fixture(document: dict[str, Any]) -> dict[str, Any]:
    require(
        document.get("schema") == "rs-mca-explicit-source-incidence-fixture-v1",
        "explicit fixture schema mismatch",
    )
    require(
        document.get("scope") == "DECLARED_SELECTED_FAMILY_TOY",
        "explicit fixture scope is not the declared toy family",
    )
    prime = exact_int(document.get("field_prime"), "field_prime")
    require(prime >= 3, "fixture prime is too small")
    # Trial division is sufficient for the intentionally tiny exact controls.
    require(
        all(prime % divisor for divisor in range(2, math.isqrt(prime) + 1)),
        "fixture field characteristic is not prime",
    )
    domain = exact_int_list(document.get("domain"), "domain")
    require(len(domain) == len(set(domain)), "duplicate domain point")
    require(all(0 <= point < prime for point in domain), "domain point outside field")
    n = len(domain)
    k = exact_int(document.get("k"), "k")
    j = exact_int(document.get("j"), "j")
    cutoff = exact_int(document.get("cutoff_D"), "cutoff_D")
    core_rank = exact_int(document.get("core_rank"), "core_rank")
    cap = exact_int(document.get("uniform_cap"), "uniform_cap")
    require(1 <= k <= n, "invalid k")
    require(0 <= j <= n, "invalid j")
    require(0 <= cutoff <= j, "invalid deficit cutoff")
    require(1 <= core_rank <= n, "invalid core rank")
    require(cap >= 1, "invalid uniform cap")

    generator_rows_raw = document.get("generator_rows")
    require(type(generator_rows_raw) is list and len(generator_rows_raw) == n, "generator row count")
    generator_rows = [
        exact_int_list(row, f"generator_rows[{index}]")
        for index, row in enumerate(generator_rows_raw)
    ]
    require(all(len(row) == core_rank for row in generator_rows), "generator width")
    generator_rows = [[entry % prime for entry in row] for row in generator_rows]
    require(matrix_rank_mod(generator_rows, prime) == core_rank, "K0 generator not full rank")

    u = exact_int_list(document.get("u"), "u")
    v = exact_int_list(document.get("v"), "v")
    require(len(u) == len(v) == n, "u/v word length")
    u = [entry % prime for entry in u]
    v = [entry % prime for entry in v]

    source_pair = document.get("source_pair")
    require(type(source_pair) is dict, "missing source pair")
    epsilon_0 = exact_int_list(source_pair.get("epsilon_0"), "epsilon_0")
    epsilon_1 = exact_int_list(source_pair.get("epsilon_1"), "epsilon_1")
    require(len(epsilon_0) == len(epsilon_1) == n, "source word length")
    epsilon_0 = [entry % prime for entry in epsilon_0]
    epsilon_1 = [entry % prime for entry in epsilon_1]
    sigma = {
        index
        for index, (left, right) in enumerate(zip(epsilon_0, epsilon_1))
        if left != 0 or right != 0
    }
    require(len(sigma) <= j, "sparse source union exceeds j")

    selected_raw = document.get("selected")
    require(type(selected_raw) is list, "selected frontier must be a list")
    records: list[dict[str, Any]] = []
    seen_slopes: set[int] = set()
    for index, raw in enumerate(selected_raw):
        require(type(raw) is dict, f"selected[{index}] is not an object")
        slope = exact_int(raw.get("slope"), f"selected[{index}].slope") % prime
        require(slope not in seen_slopes, "duplicate selected slope")
        seen_slopes.add(slope)
        z = exact_int_list(raw.get("z"), f"selected[{index}].z")
        require(len(z) == core_rank, "graph-coordinate width")
        z = [entry % prime for entry in z]
        support = exact_int_list(
            raw.get("error_support"), f"selected[{index}].error_support"
        )
        require(support == sorted(set(support)), "support not sorted and unique")
        require(all(0 <= coordinate < n for coordinate in support), "support coordinate outside domain")
        word = [
            (
                u[coordinate]
                + slope * v[coordinate]
                + sum(
                    z_entry * generator_entry
                    for z_entry, generator_entry in zip(z, generator_rows[coordinate])
                )
            )
            % prime
            for coordinate in range(n)
        ]
        actual_support = [coordinate for coordinate, entry in enumerate(word) if entry]
        require(actual_support == support, "declared error support disagrees with source word")
        require(len(support) <= j, "selected error exceeds j")
        delta = exact_int(raw.get("delta"), f"selected[{index}].delta")
        require(delta == j - len(support), "declared deficit disagrees with support")
        records.append(
            {
                "slope": slope,
                "z": tuple(z),
                "support": frozenset(support),
                "zero": frozenset(set(range(n)) - set(support)),
                "delta": delta,
            }
        )

    filtered_records = [record for record in records if 0 <= record["delta"] <= cutoff]

    independent_bases: list[tuple[int, ...]] = []
    for basis in itertools.combinations(range(n), core_rank):
        rows = [generator_rows[coordinate] for coordinate in basis]
        if matrix_rank_mod(rows, prime) == core_rank:
            independent_bases.append(basis)

    direct_excess = 0
    rich_basis_owners: dict[tuple[int, ...], str] = {}
    for basis in independent_bases:
        owner_records = [record for record in filtered_records if set(basis) <= record["zero"]]
        multiplicity = len(owner_records)
        if multiplicity <= cap:
            continue
        direct_excess += multiplicity - cap
        first = owner_records[0]
        second = owner_records[1]
        denominator = (second["slope"] - first["slope"]) % prime
        beta = tuple(
            ((right - left) * inverse_mod(denominator, prime)) % prime
            for left, right in zip(first["z"], second["z"])
        )
        alpha = tuple(
            (entry - first["slope"] * direction) % prime
            for entry, direction in zip(first["z"], beta)
        )
        require(
            all(
                record["z"]
                == tuple(
                    (a_entry + record["slope"] * b_entry) % prime
                    for a_entry, b_entry in zip(alpha, beta)
                )
                for record in owner_records
            ),
            "rich basis graph points are not collinear",
        )
        rich_basis_owners[basis] = line_key(alpha, beta)

    candidate_lines: dict[str, tuple[tuple[int, ...], tuple[int, ...], list[int]]] = {}
    for left_index, right_index in itertools.combinations(range(len(filtered_records)), 2):
        left = filtered_records[left_index]
        right = filtered_records[right_index]
        denominator = (right["slope"] - left["slope"]) % prime
        beta = tuple(
            ((right_entry - left_entry) * inverse_mod(denominator, prime)) % prime
            for left_entry, right_entry in zip(left["z"], right["z"])
        )
        alpha = tuple(
            (entry - left["slope"] * direction) % prime
            for entry, direction in zip(left["z"], beta)
        )
        members = [
            index
            for index, record in enumerate(filtered_records)
            if record["z"]
            == tuple(
                (a_entry + record["slope"] * b_entry) % prime
                for a_entry, b_entry in zip(alpha, beta)
            )
        ]
        if len(members) >= cap + 1:
            candidate_lines[line_key(alpha, beta)] = (alpha, beta, members)

    line_lifts = document.get("line_lifts")
    require(type(line_lifts) is dict, "line_lifts must be an object")
    require(set(line_lifts) == set(candidate_lines), "rich-line lift inventory is not exact")

    atlas_excess = 0
    beta_profile: list[int] = []
    line_sizes: list[int] = []
    for key in sorted(candidate_lines):
        alpha, beta, members = candidate_lines[key]
        a_word = [
            (u[index] + sum(a * g for a, g in zip(alpha, generator_rows[index])))
            % prime
            for index in range(n)
        ]
        b_word = [
            (v[index] + sum(b * g for b, g in zip(beta, generator_rows[index])))
            % prime
            for index in range(n)
        ]
        common_zero = {
            index
            for index, (left, right) in enumerate(zip(a_word, b_word))
            if left == 0 and right == 0
        }
        basis_mass = sum(
            1 for basis in independent_bases if set(basis) <= common_zero
        )
        beta_profile.append(basis_mass)
        line_sizes.append(len(members))
        atlas_excess += basis_mass * (len(members) - cap)

        lift = line_lifts[key]
        require(type(lift) is dict, f"line lift {key} is not an object")
        p_coefficients = exact_int_list(lift.get("P_coefficients"), f"{key}.P")
        q_coefficients = exact_int_list(lift.get("Q_coefficients"), f"{key}.Q")
        require(polynomial_degree(p_coefficients, prime) < k, f"P_L degree exceeds k on {key}")
        require(polynomial_degree(q_coefficients, prime) < k, f"Q_L degree exceeds k on {key}")
        p_values = polynomial_values(p_coefficients, domain, prime)
        q_values = polynomial_values(q_coefficients, domain, prime)
        require(
            all((epsilon_0[index] - p_values[index]) % prime == a_word[index] for index in range(n)),
            f"source coupling failed for a_L on {key}",
        )
        require(
            all((epsilon_1[index] - q_values[index]) % prime == b_word[index] for index in range(n)),
            f"source coupling failed for b_L on {key}",
        )

    require(direct_excess == atlas_excess, "direct and atlas excess disagree")
    require(
        set(rich_basis_owners.values()) <= set(candidate_lines),
        "a rich basis has no unique graph-line owner",
    )
    result = {
        "declared_slope_count": len(records),
        "filtered_slope_count": len(filtered_records),
        "independent_basis_count": len(independent_bases),
        "rich_line_count": len(candidate_lines),
        "rich_line_sizes": sorted(line_sizes),
        "beta_profile": sorted(beta_profile),
        "direct_excess": direct_excess,
        "atlas_excess": atlas_excess,
    }
    expected = document.get("expected")
    require(type(expected) is dict, "fixture expected block missing")
    require(canonical_bytes(result) == canonical_bytes(expected), "fixture expected result drift")
    return result


def predecessor_semantics() -> dict[str, Any]:
    mask = load_json(ROOT / MASK_CERT_REL)
    rich = load_json(ROOT / RICH_CERT_REL)
    toy = load_json(ROOT / TOY_CERT_REL)
    for relative, document in [(RICH_CERT_REL, rich), (TOY_CERT_REL, toy)]:
        require(
            document.get("payload_sha256") == payload_hash(document),
            f"bad predecessor payload: {relative}",
        )
    require(mask["first_match"]["complete_global_replay"] is False, "global replay status drift")
    require(
        mask["branch3"]["low_excess_selector_owner"]["deployed_complete_selector_inventory_present"]
        is False,
        "deployed selector inventory status drift",
    )
    require(mask["branch5"]["status"] == "UNBOUND_SOURCE_FAMILY", "branch 5 status drift")
    require(
        mask["downstream_contract"]["exact_after_branches_3_5_residual_available"]
        is False,
        "post-branches-3-5 residual status drift",
    )
    require(
        rich["hostile_scalar_relaxation"]["deployed_selector_constructed"] is False,
        "rich deployed-selector status drift",
    )
    require(
        rich["audit"]["deployed_field_census_performed"] is False,
        "rich deployed-census status drift",
    )
    require(
        rich["first_match_contract"]["current_terminal"]
        == "UNPAID_SOURCE_BOUND_RICH_PENCIL_AGGREGATE",
        "rich terminal drift",
    )
    require(toy["scope_guards"]["deployed_field_instantiated"] is False, "toy field scope drift")
    require(
        toy["scope_guards"]["rank9_geometry_checked_for_every_source_line"] is False,
        "toy source-line scope drift",
    )
    return {
        "complete_global_first_match_replay": False,
        "deployed_complete_selector_inventory": False,
        "post_branches_3_5_residual": False,
        "branch5_source_family": "UNBOUND_SOURCE_FAMILY",
        "deployed_rich_pencil_selector_constructed": False,
        "deployed_rich_pencil_census": False,
        "paying_selector_source_family_coverage": False,
        "toy_coordinate_cover_deployed_field": False,
        "toy_coordinate_cover_all_deployed_source_lines": False,
        "current_terminal": "UNPAID_SOURCE_BOUND_RICH_PENCIL_AGGREGATE",
    }


def expected_certificate() -> dict[str, Any]:
    high = validate_explicit_fixture(explicit_high_fixture())
    low = validate_explicit_fixture(explicit_low_fixture())
    empty = validate_explicit_fixture(explicit_empty_fixture())
    semantics = predecessor_semantics()
    sources = [
        source_binding("packet-note", NOTE_REL, "readiness manifest and route cut"),
        source_binding("packet-readme", README_REL, "replay instructions"),
        source_binding("packet-python", PYTHON_REL, "readiness audit and exact toy kernel"),
        source_binding("mask-contract-note", MASK_NOTE_REL, "first-match quantifiers"),
        source_binding("mask-contract-certificate", MASK_CERT_REL, "deployed source status"),
        source_binding("syndrome-note", SYNDROME_NOTE_REL, "same-selector syndrome equations"),
        source_binding("actual-core-note", CORE_NOTE_REL, "K0 and selector provenance"),
        source_binding("mask-deficit-note", MASK_DEFICIT_NOTE_REL, "H-tail compiler"),
        source_binding("fixed-basis-note", FIXED_NOTE_REL, "E20 compiler"),
        source_binding("rich-pencil-note", RICH_NOTE_REL, "canonical atlas identity"),
        source_binding("rich-pencil-certificate", RICH_CERT_REL, "current aggregate terminal"),
        source_binding("toy-coordinate-cover-note", TOY_NOTE_REL, "reusable toy source machinery"),
        source_binding("toy-coordinate-cover-certificate", TOY_CERT_REL, "toy scope guards"),
    ]
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": sources,
        "predecessor_fingerprints": {
            "mask_contract": predecessor_fingerprint(MASK_CERT_REL),
            "syndrome_rank_reduction": predecessor_fingerprint(SYNDROME_CERT_REL),
            "actual_core_mds": predecessor_fingerprint(CORE_CERT_REL),
            "mask_deficit": predecessor_fingerprint(MASK_DEFICIT_CERT_REL),
            "fixed_basis": predecessor_fingerprint(FIXED_CERT_REL),
            "rich_pencil": predecessor_fingerprint(RICH_CERT_REL),
            "toy_coordinate_cover": predecessor_fingerprint(TOY_CERT_REL),
        },
        "row": {
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "q_line": str(Q_LINE),
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "t": T,
            "core_rank": CORE_R,
            "cutoff_D": CUTOFF_D,
            "uniform_cap": UNIFORM_CAP,
        },
        "implementation_scope": {
            "deployed_readiness_audit_executable": True,
            "explicit_toy_incidence_kernel_executable": True,
            "full_deployed_producer_validator_implemented": False,
            "complete_selector_exhaustion_checked_by_toy_kernel": False,
            "global_owner_dedup_checked_by_toy_kernel": False,
            "nonzero_pencil_gcd_and_plant_checked_by_toy_kernel": False,
        },
        "producer_field_manifest": {
            "scope": "WHOLE_DECLARED_BRANCH3_RANK9_SUCCESSOR",
            "domain_encoding_fields": [
                "base_field_prime",
                "extension_degree",
                "extension_modulus",
                "extension_basis",
                "field_element_encoding",
                "domain_generator_omega",
                "domain_order_n",
            ],
            "selector_context_fields": [
                "source_id",
                "selector_id",
                "f",
                "g",
                "H_V",
                "V",
                "K0_generator",
                "d_V",
                "y_0",
                "y_1",
                "u",
                "v",
                "c_0",
                "c_1",
                "epsilon_0",
                "epsilon_1",
                "Sigma",
            ],
            "slope_record_fields": [
                "eta",
                "S_eta",
                "c_eta",
                "e_eta",
                "E_eta",
                "delta_eta",
                "z_eta",
                "exact_A_witness",
                "noncontained",
                "branch3_successor_membership",
                "syndrome_equation_verified",
                "transversality_verified",
            ],
            "selector_assertion_fields": [
                "complete_selector",
                "selector_universe_exhaustive",
                "affine_difference_rank_9",
                "column_rank_10",
                "K0_dimension_8",
                "same_H_V_for_all_records",
                "same_selector_for_all_records",
            ],
            "regular_chart_fields": [
                "H1",
                "H2",
                "Delta_value",
                "Delta_nonzero",
                "locator_coefficients",
                "locator_support_O_eta",
                "locator_size_j",
                "locator_split_squarefree_on_D",
                "kernel_equation_zero",
                "H2_locator_value",
                "H2_locator_nonzero",
            ],
            "rich_line_fields": [
                "line_id",
                "member_slope_ids",
                "alpha",
                "beta",
                "a_L",
                "b_L",
                "J_L",
                "M_L",
                "x_L",
                "Z_L",
                "beta_L",
                "P_L",
                "Q_L",
                "codeword_pencil_zero",
                "G_L_or_null",
                "deg_G_L_or_null",
                "planted_source_count_or_null",
                "unique_basis_owner_records",
            ],
            "zero_pencil_contract": [
                "P_L=Q_L=0",
                "a_L=epsilon_0",
                "b_L=epsilon_1",
                "W_L=Sigma",
                "x_L<=0",
                "G_L=deg_G_L=planted_source_count=null",
            ],
            "nonzero_pencil_contract": [
                "at least one of P_L,Q_L is nonzero",
                "G_L divides gcd(P_L,Q_L)",
                "deg_G_L>=A-x_L-|Sigma|",
                "planted_source_count>=t-x_L+1",
            ],
            "global_coverage_fields": [
                "coverage_mode",
                "uniform_theorem_binding_or_null",
                "source_family_exhaustive_or_uniform",
                "one_paying_complete_rank9_selector_per_source_family",
                "selector_universe_exhaustive_if_rank_minimizer_or_complement_claimed",
                "rich_line_partition_exhaustive",
                "owner_order",
                "deduplicated_global_addback",
            ],
            "source_equalities": [
                "e_eta=f+eta*g-c_eta",
                "epsilon_0=f-c_0",
                "epsilon_1=g-c_1",
                "a_L=epsilon_0-ev(P_L)",
                "b_L=epsilon_1-ev(Q_L)",
            ],
            "low_deficit_filter": "Gamma_D={eta:0<=delta_eta<=18014}",
            "coverage_disjunction": [
                "SOURCE_BOUND_PAYING_COMPLETE_RANK9_SELECTOR_FOR_EVERY_SOURCE_FAMILY",
                "ROW_UNIFORM_EXISTENCE_OF_A_PAYING_COMPLETE_SELECTOR",
                "EXHAUSTIVE_SOURCE_FAMILY_CENSUS_WITH_ONE_PAYING_SELECTOR_EACH",
            ],
            "summary_moments_without_source_map_accepted": False,
            "single_supplied_selector_proves_complement": False,
            "branch5_binding_required_for_monotone_whole_branch3_strategy": False,
        },
        "compiler": {
            "identity": "E_20=sum_{L subset Gamma_D:J_L>=21} beta_L*(J_L-20)",
            "Gamma_D": "{eta:0<=delta_eta<=18014}",
            "E_max": str(E_MAX),
            "sufficient_gate": "E_20<=E_max IMPLIES H_18014<=tail_target",
            "tail_target": str(TAIL_TARGET),
            "reverse_implication_claimed": False,
        },
        "current_inputs": semantics,
        "route_assessment": {
            "source_bound_paying_selector_for_every_source_family_present": False,
            "uniform_theorem_present": False,
            "exhaustive_deployed_source_family_census_present": False,
            "coverage_disjunction_satisfied": False,
            "first_missing_gate": "PAYING_SELECTOR_SOURCE_FAMILY_COVERAGE",
            "secondary_missing_gates": [
                "PINNED_SEXTIC_REPRESENTATION_AND_EXTENSION_SLOPE_ENCODING",
                "COMPRESSED_EXACT_A_SOURCE_WITNESS_GENERATOR",
                "SAME_SELECTOR_SOURCE_SUPPORT_AND_REGULAR_CHART_RECORDS",
                "COMPRESSED_BETA_L_DETERMINANT_MASS_THEOREM",
                "OWNER_ORDER_AND_DEDUPLICATED_GLOBAL_ADDBACK",
            ],
            "terminal": "UNBOUND_DEPLOYED_SOURCE_INCIDENCE",
        },
        "exact_fixture_engine": {
            "classification": "EXACT_SMALL_PRIME_ATLAS_SOURCE_EQUALITY_SMOKE_CONTROLS",
            "reconstructs_words_from_u_v_K0_z": True,
            "recomputes_error_supports": True,
            "derives_graph_lines_from_pairs": True,
            "enumerates_independent_bases": True,
            "checks_source_polynomial_lifts": True,
            "checks_direct_equals_atlas": True,
            "complete_selector_exhaustion_checked": False,
            "global_owner_dedup_checked": False,
            "nonzero_pencil_gcd_and_plant_checked": False,
            "low_fixture": low,
            "high_fixture": high,
            "empty_fixture": empty,
            "deployed_field_instantiated": False,
        },
        "ledger": {
            "B_star": str(B_STAR),
            "U_paid_before": str(U_PAID),
            "U_paid_after": str(U_PAID),
            "B_remaining_before": str(B_REMAINING),
            "B_remaining_after": str(B_REMAINING),
            "U_Q": None,
            "U_A": None,
            "movement": "0",
        },
        "audit": {
            "packet_verdict": "GREEN_EXECUTABLE_READINESS_AUDIT_AND_EXACT_TOY_KERNEL",
            "global_verdict": "YELLOW_DEPLOYED_SOURCE_INCIDENCE_OPEN",
            "proof": "CONDITIONAL_COMPILER_AND_FROZEN_PRODUCER_FIELD_MANIFEST",
            "empirical_evidence": "EXACT_TOY_FIXTURES_ONLY",
            "conjecture": "NONE_BANKED",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
        },
        "nonclaims": [
            "No deployed source or complete-selector producer is constructed.",
            "No full deployed producer schema is validated by the toy incidence kernel.",
            "The fixtures are declared selected families, not exhaustive eligible frontiers.",
            "The fixtures exercise the zero-codeword-pencil source equality, not the nonzero GCD/plant contract.",
            "No toy fixture is extrapolated to the KoalaBear field or domain.",
            "No post-branches-3-5 residual is declared.",
            "No branch-5 source family or branch-1 projector is invented.",
            "No E_20 or H_18014 deployed bound is proved.",
            "No KoalaBear ledger value moves.",
            "U_Q and U_A remain null.",
            "Rank at least ten, Lean, and stable-paper promotion remain out of scope.",
        ],
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def strict_match(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type mismatch at {path}")
    if type(expected) is dict:
        require(actual.keys() == expected.keys(), f"key mismatch at {path}")
        for key in expected:
            strict_match(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_match(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"value mismatch at {path}")


def validate_certificate(document: dict[str, Any]) -> None:
    expected = expected_certificate()
    strict_match(document, expected)
    require(document["payload_sha256"] == payload_hash(document), "payload hash mismatch")
    require(B_STAR == 274_980_728_111_395_087, "B_star drift")
    require(B_REMAINING == 274_980_725_508_892_088, "remaining budget drift")
    require(not document["route_assessment"]["coverage_disjunction_satisfied"], "coverage invented")
    require(document["ledger"]["movement"] == "0", "ledger moved")
    require(document["ledger"]["U_Q"] is None and document["ledger"]["U_A"] is None, "owner null drift")
    require(
        document["exact_fixture_engine"]["high_fixture"]["direct_excess"]
        == document["exact_fixture_engine"]["high_fixture"]["atlas_excess"]
        == 6,
        "high fixture identity drift",
    )
    require(
        document["exact_fixture_engine"]["empty_fixture"]["direct_excess"]
        == document["exact_fixture_engine"]["empty_fixture"]["atlas_excess"]
        == 0,
        "empty fixture identity drift",
    )


def rehash(document: dict[str, Any]) -> None:
    document["payload_sha256"] = payload_hash(document)


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def certificate_mutations() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-bad")),
        ("row-p", lambda d: d["row"].__setitem__("p", P + 2)),
        ("row-j", lambda d: d["row"].__setitem__("j", J + 1)),
        ("full-validator", lambda d: d["implementation_scope"].__setitem__("full_deployed_producer_validator_implemented", True)),
        ("toy-exhaustion", lambda d: d["implementation_scope"].__setitem__("complete_selector_exhaustion_checked_by_toy_kernel", True)),
        ("toy-plant", lambda d: d["implementation_scope"].__setitem__("nonzero_pencil_gcd_and_plant_checked_by_toy_kernel", True)),
        ("same-selector", lambda d: d["producer_field_manifest"]["selector_context_fields"].pop()),
        ("domain-encoding", lambda d: d["producer_field_manifest"]["domain_encoding_fields"].pop()),
        ("manifest-filter", lambda d: d["producer_field_manifest"].__setitem__("low_deficit_filter", "ALL_SLOPES")),
        ("summary-moments", lambda d: d["producer_field_manifest"].__setitem__("summary_moments_without_source_map_accepted", True)),
        ("single-selector", lambda d: d["producer_field_manifest"].__setitem__("single_supplied_selector_proves_complement", True)),
        ("identity", lambda d: d["compiler"].__setitem__("identity", "E_20=0")),
        ("gamma-filter", lambda d: d["compiler"].__setitem__("Gamma_D", "ALL_SELECTED_SLOPES")),
        ("emax", lambda d: d["compiler"].__setitem__("E_max", str(E_MAX + 1))),
        ("reverse", lambda d: d["compiler"].__setitem__("reverse_implication_claimed", True)),
        ("canonical-selector", lambda d: d["route_assessment"].__setitem__("source_bound_paying_selector_for_every_source_family_present", True)),
        ("uniform", lambda d: d["route_assessment"].__setitem__("uniform_theorem_present", True)),
        ("census", lambda d: d["route_assessment"].__setitem__("exhaustive_deployed_source_family_census_present", True)),
        ("coverage", lambda d: d["route_assessment"].__setitem__("coverage_disjunction_satisfied", True)),
        ("terminal", lambda d: d["route_assessment"].__setitem__("terminal", "PAID")),
        ("selector-status", lambda d: d["current_inputs"].__setitem__("deployed_complete_selector_inventory", True)),
        ("paying-coverage-status", lambda d: d["current_inputs"].__setitem__("paying_selector_source_family_coverage", True)),
        ("branch5", lambda d: d["current_inputs"].__setitem__("branch5_source_family", "PAID")),
        ("fixture-high", lambda d: d["exact_fixture_engine"]["high_fixture"].__setitem__("atlas_excess", 5)),
        ("fixture-empty", lambda d: d["exact_fixture_engine"]["empty_fixture"].__setitem__("atlas_excess", 1)),
        ("fixture-deployed", lambda d: d["exact_fixture_engine"].__setitem__("deployed_field_instantiated", True)),
        ("ledger", lambda d: d["ledger"].__setitem__("movement", "1")),
        ("uq", lambda d: d["ledger"].__setitem__("U_Q", "0")),
        ("global-green", lambda d: d["audit"].__setitem__("global_verdict", "GREEN_CLOSED")),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("predecessor", lambda d: d["predecessor_fingerprints"].__setitem__("rich_pencil", "payload-sha256:" + "0" * 64)),
        ("type-confusion", lambda d: d["row"].__setitem__("core_rank", True)),
    ]


def fixture_mutations() -> list[Mutation]:
    return [
        ("fixture-schema", lambda d: d.__setitem__("schema", "bad")),
        ("fixture-scope", lambda d: d.__setitem__("scope", "EXHAUSTIVE_SELECTED_FRONTIER_TOY")),
        ("fixture-composite", lambda d: d.__setitem__("field_prime", 9)),
        ("fixture-domain-duplicate", lambda d: d["domain"].__setitem__(1, 0)),
        ("fixture-source-wide", lambda d: d.__setitem__("j", 2)),
        ("fixture-source-coupling", lambda d: d["source_pair"]["epsilon_0"].__setitem__(3, 2)),
        ("fixture-cutoff", lambda d: d.__setitem__("cutoff_D", 0)),
        ("fixture-k-type", lambda d: d.__setitem__("k", True)),
        ("fixture-generator-rank", lambda d: d["generator_rows"].__setitem__(1, [1, 0])),
        ("fixture-duplicate-slope", lambda d: d["selected"][1].__setitem__("slope", 0)),
        ("fixture-z-width", lambda d: d["selected"][0]["z"].pop()),
        ("fixture-support-duplicate", lambda d: d["selected"][0].__setitem__("error_support", [3, 3, 4, 5])),
        ("fixture-support-forged", lambda d: d["selected"][0].__setitem__("error_support", [3, 4])),
        ("fixture-deficit-forged", lambda d: d["selected"][2].__setitem__("delta", 0)),
        ("fixture-z-forged", lambda d: d["selected"][0]["z"].__setitem__(0, 1)),
        ("fixture-missing-line", lambda d: d.__setitem__("line_lifts", {})),
        ("fixture-polynomial", lambda d: d["line_lifts"]["0,0|0,0"].__setitem__("P_coefficients", [1])),
        ("fixture-polynomial-degree", lambda d: d["line_lifts"]["0,0|0,0"].__setitem__("P_coefficients", [0, 6, 0, 0, 0, 0, 0, 1])),
        ("fixture-expected-beta", lambda d: d["expected"]["beta_profile"].__setitem__(0, 2)),
        ("fixture-expected-direct", lambda d: d["expected"].__setitem__("direct_excess", 5)),
        ("fixture-type", lambda d: d.__setitem__("uniform_cap", True)),
    ]


def run_tamper_selftest() -> int:
    passed = 0
    baseline = expected_certificate()
    for name, mutate in certificate_mutations():
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        rehash(candidate)
        try:
            validate_certificate(candidate)
        except (ContractError, KeyError, TypeError, ValueError):
            passed += 1
        else:
            raise ContractError(f"certificate mutation escaped: {name}")

    fixture = explicit_high_fixture()
    for name, mutate in fixture_mutations():
        candidate = copy.deepcopy(fixture)
        mutate(candidate)
        try:
            validate_explicit_fixture(candidate)
        except (ContractError, KeyError, TypeError, ValueError):
            passed += 1
        else:
            raise ContractError(f"fixture mutation escaped: {name}")

    parser_cases = {
        "duplicate": '{"schema":"a","schema":"b"}',
        "nan": '{"x":NaN}',
        "infinity": '{"x":Infinity}',
        "float": '{"x":1.0}',
        "overflow-float": '{"x":1e9999}',
    }
    for name, text in parser_cases.items():
        try:
            parse_json(text, name)
        except ContractError:
            passed += 1
        else:
            raise ContractError(f"parser mutation escaped: {name}")

    # The payload itself must also be protected without refreshing its hash.
    candidate = copy.deepcopy(baseline)
    candidate["payload_sha256"] = "0" * 64
    try:
        validate_certificate(candidate)
    except ContractError:
        passed += 1
    else:
        raise ContractError("payload mutation escaped")

    print(f"tamper_selftest=PASS ({passed}/{passed})")
    return passed


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    document = expected_certificate()
    CERT_PATH.write_text(
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote={CERT_PATH.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--tamper-selftest", action="store_true")
    action.add_argument("--write", action="store_true")
    action.add_argument("--check-explicit", type=Path)
    args = parser.parse_args()

    if args.write:
        write_certificate()
        return
    if args.tamper_selftest:
        run_tamper_selftest()
        return
    if args.check_explicit is not None:
        document = load_json(args.check_explicit)
        result = validate_explicit_fixture(document)
        print(json.dumps(result, indent=2, sort_keys=True))
        print("explicit_check=PASS")
        return

    document = load_json(CERT_PATH)
    validate_certificate(document)
    print(f"schema={SCHEMA}")
    print(f"E_max={E_MAX}")
    print(f"tail_target={TAIL_TARGET}")
    print("uniform_theorem_present=false")
    print("source_bound_paying_selector_for_every_source_family_present=false")
    print("exhaustive_deployed_source_family_census_present=false")
    print("terminal=UNBOUND_DEPLOYED_SOURCE_INCIDENCE")
    print("ledger_movement=0")
    print("check=PASS")


if __name__ == "__main__":
    main()
