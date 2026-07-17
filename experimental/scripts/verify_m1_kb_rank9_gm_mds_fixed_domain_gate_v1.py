#!/usr/bin/env python3
"""Verify the KoalaBear rank-nine GM--MDS fixed-domain gate.

For a declared tuple of monic degree-j split locators, the verifier checks
all GM--MDS intersection inequalities.  A failure emits its exact common
core and only a Johnson/common-core *candidate*.  If all inequalities pass,
the verifier computes the locator-coefficient rank over the declared prime
field and returns either an exact independence certificate or an explicit
fixed-domain specialization exception.

The packet is a fail-closed route cut.  Its current polynomial builders are
CONTROL_ONLY at j=10; no deployed-scale executor is implemented.  It supplies
no retained KoalaBear support tuple, pays no owner, moves no ledger, and
closes no rank-nine row.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-rank9-gm-mds-fixed-domain-gate-v1"
ARTIFACT_KIND = "M1_KB_RANK9_GM_MDS_FIXED_DOMAIN_ROUTE_CUT"
STATUS = "PROVED_UNIVERSAL_GATE_DEPLOYED_INPUT_AND_EXECUTOR_MISSING"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-gm-mds-fixed-domain-gate-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_gm_mds_fixed_domain_gate_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_gm_mds_fixed_domain_gate_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-gm-mds-fixed-domain-gate-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.sage"
)
SPARSE_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"
)
SPARSE_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-sparse-chart-boundary-v1/"
    "m1_kb_branch3_rank9_sparse_chart_boundary_v1.json"
)
SPARSE_PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py"
)
GENERIC_CUT_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.md"
)
GENERIC_CUT_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-rank9-regular-locator-span-shortcut-refuted-v1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.json"
)
GENERIC_CUT_PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py"
)
BASE_SLOPE_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_base_slope_universe_v2.md"
)
BASE_SLOPE_CERT_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-1116048-base-slope-universe-v2/"
    "kb_mca_1116048_base_slope_universe_v2.json"
)
BASE_SLOPE_PYTHON_REL = Path(
    "experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py"
)
RAW_V13_REL = Path("experimental/cap25_cap_v13_raw.tex")

P_KB = 2**31 - 2**24 + 1
EXTENSION_DEGREE = 6
N_KB = 2**21
K_KB = 2**20
A_KB = 1_116_048
R_KB = N_KB - K_KB
J_KB = N_KB - A_KB
LOCATOR_COUNT = 11
LOVETT_K_KB = J_KB + 1

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "literature_import",
    "deployed_interface",
    "universal_gate",
    "exact_controls",
    "scope_guards",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not supply an actual retained KoalaBear 11-locator tuple.",
    "This packet does not prove that any locator survives the deployed first-match masks.",
    "This packet does not assign a GM--MDS failure to a paid Johnson owner.",
    "This packet does not infer periodicity or quotient descent from a common core.",
    "This packet does not certify a fixed-domain rank for the deployed KoalaBear residual.",
    "The current Python and Sage implementations are j=10 controls, not deployed-scale executors.",
    "A deployed executor requires a fast product tree, NTT, or streamed nonzero-minor certificate.",
    "This packet does not move U_paid or B_remaining.",
    "This packet does not close rank nine, branch 3, or the KoalaBear row.",
    "This packet does not attack intrinsic rank at least ten.",
    "This packet does not authorize Lean or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """An arithmetic, source, schema, or semantic gate failed."""


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
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
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


def is_prime_32(value: int) -> bool:
    if value < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small:
        if value == prime:
            return True
        if value % prime == 0:
            return False
    exponent = value - 1
    twos = 0
    while exponent % 2 == 0:
        exponent //= 2
        twos += 1
    for base in (2, 3, 5, 7, 11):
        if base >= value:
            continue
        residue = pow(base, exponent, value)
        if residue in (1, value - 1):
            continue
        for _ in range(twos - 1):
            residue = residue * residue % value
            if residue == value - 1:
                break
        else:
            return False
    return True


def poly_mul_mod(
    left: Sequence[int], right: Sequence[int], prime: int
) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % prime
    return result


def locator_coefficients(support: Iterable[int], prime: int) -> list[int]:
    polynomial = [1]
    for point in support:
        polynomial = poly_mul_mod(polynomial, [(-point) % prime, 1], prime)
    return polynomial


def rref_mod(
    rows: Sequence[Sequence[int]], prime: int
) -> tuple[list[list[int]], list[int]]:
    if not rows:
        return [], []
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    matrix = [[value % prime for value in row] for row in rows]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(width):
        chosen = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column] % prime
            ),
            None,
        )
        if chosen is None:
            continue
        matrix[pivot_row], matrix[chosen] = matrix[chosen], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], prime - 2, prime)
        matrix[pivot_row] = [value * inverse % prime for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (value - factor * pivot) % prime
                for value, pivot in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, pivots


def matrix_rank_mod(rows: Sequence[Sequence[int]], prime: int) -> int:
    return len(rref_mod(rows, prime)[1])


def transpose(rows: Sequence[Sequence[int]]) -> list[list[int]]:
    if not rows:
        return []
    return [list(column) for column in zip(*rows, strict=True)]


def normalize_projective(vector: Sequence[int], prime: int) -> list[int]:
    values = [value % prime for value in vector]
    first = next((value for value in values if value), None)
    require(first is not None, "zero vector has no projective normalization")
    inverse = pow(first, prime - 2, prime)
    return [value * inverse % prime for value in values]


def one_null_vector(rows: Sequence[Sequence[int]], prime: int) -> list[int]:
    """Return one normalized nonzero vector in the right kernel."""

    matrix, pivots = rref_mod(rows, prime)
    width = len(rows[0]) if rows else 0
    free = next((column for column in range(width) if column not in pivots), None)
    require(free is not None, "matrix has trivial right kernel")
    vector = [0] * width
    vector[free] = 1
    for row, pivot in reversed(list(enumerate(pivots))):
        vector[pivot] = -sum(
            matrix[row][column] * vector[column]
            for column in range(pivot + 1, width)
        ) % prime
    require(
        all(
            sum(a * b for a, b in zip(row, vector, strict=True)) % prime == 0
            for row in rows
        ),
        "computed null vector failed",
    )
    return normalize_projective(vector, prime)


def support_hash(supports: Sequence[Sequence[int]]) -> str:
    return canonical_hash([list(support) for support in supports])


def classify_locator_tuple(
    *, prime: int, domain: Sequence[int], supports: Sequence[Sequence[int]]
) -> dict[str, Any]:
    require(is_prime_32(prime), "declared modulus is not prime")
    normalized_domain = tuple(point % prime for point in domain)
    require(
        len(normalized_domain) == len(set(normalized_domain)),
        "domain points are not distinct",
    )
    require(len(supports) >= 2, "need at least two locators")
    normalized_supports = [tuple(sorted(point % prime for point in support)) for support in supports]
    degree = len(normalized_supports[0])
    require(degree >= len(supports) - 1, "Lovett parameter is smaller than locator count")
    require(
        all(len(support) == degree for support in normalized_supports),
        "locator degrees disagree",
    )
    require(
        all(len(support) == len(set(support)) for support in normalized_supports),
        "a locator support has a repeated point",
    )
    domain_set = set(normalized_domain)
    require(
        all(set(support) <= domain_set for support in normalized_supports),
        "a locator support leaves the declared domain",
    )
    require(
        len(normalized_supports) == len(set(normalized_supports)),
        "duplicate locator support",
    )

    lovett_k = degree + 1
    violations: list[dict[str, Any]] = []
    minimum_slack: int | None = None
    for size in range(1, len(normalized_supports) + 1):
        for indices in itertools.combinations(range(len(normalized_supports)), size):
            common = set(normalized_supports[indices[0]])
            for index in indices[1:]:
                common.intersection_update(normalized_supports[index])
            bound = lovett_k - size
            slack = bound - len(common)
            minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
            if slack < 0:
                violations.append(
                    {
                        "indices_zero_based": list(indices),
                        "subset_size": size,
                        "common_core": sorted(common),
                        "common_core_size": len(common),
                        "allowed_core_size": bound,
                        "excess": -slack,
                    }
                )

    coefficients = [locator_coefficients(support, prime) for support in normalized_supports]
    require(
        all(len(row) == lovett_k and row[-1] == 1 for row in coefficients),
        "locator coefficient shape or monicity drift",
    )
    rank = matrix_rank_mod(coefficients, prime)

    common_fields = {
        "prime": prime,
        "domain_size": len(normalized_domain),
        "locator_count": len(normalized_supports),
        "locator_degree_j": degree,
        "Lovett_parameter_K": lovett_k,
        "field_size_at_least_domain_plus_K_minus_1": (
            prime >= len(normalized_domain) + lovett_k - 1
        ),
        "checked_nonempty_index_subsets": 2 ** len(normalized_supports) - 1,
        "support_sha256": support_hash(normalized_supports),
        "coefficient_rank": rank,
        "minimum_GM_slack": minimum_slack,
    }

    if violations:
        first = violations[0]
        indices = first["indices_zero_based"]
        core = set(first["common_core"])
        r = first["subset_size"]
        subfamily = [normalized_supports[index] for index in indices]
        pair_distances = [
            degree - len(set(left) & set(right))
            for left, right in itertools.combinations(subfamily, 2)
        ]
        maximum_distance = max(pair_distances, default=0)
        require(len(core) >= degree + 2 - r, "common-core lower bound failed")
        require(
            all(len(set(support) - core) <= r - 2 for support in subfamily),
            "petal bound failed",
        )
        require(maximum_distance <= r - 2, "Johnson radius bound failed")
        require(
            matrix_rank_mod([coefficients[index] for index in indices], prime) <= r - 1,
            "GM failure did not force universal dependence",
        )
        return {
            **common_fields,
            "GM_condition_passes": False,
            "violation_count": len(violations),
            "first_violation": first,
            "common_core_consequence": {
                "each_petal_size_at_most": r - 2,
                "maximum_realized_pair_Johnson_distance": maximum_distance,
                "all_locators_lie_in_space": (
                    f"L_W*F[X]_<= {degree - len(core)}"
                ),
                "space_dimension_at_most": r - 1,
            },
            "owner_status": "JOHNSON_COMMON_CORE_CANDIDATE_NOT_PAID",
            "terminal": "GM_MDS_INTERSECTION_VIOLATION",
        }

    require(minimum_slack is not None and minimum_slack >= 0, "GM scan failed")
    if rank == len(normalized_supports):
        return {
            **common_fields,
            "GM_condition_passes": True,
            "violation_count": 0,
            "fixed_domain_null_relation": None,
            "owner_status": "NO_OWNER_ASSIGNED",
            "terminal": "FIXED_DOMAIN_LOCATOR_INDEPENDENCE_CERTIFIED_FOR_DECLARED_TUPLE",
        }

    relation = one_null_vector(transpose(coefficients), prime)
    require(
        any(relation)
        and all(
            sum(relation[row] * coefficients[row][column] for row in range(len(coefficients)))
            % prime
            == 0
            for column in range(lovett_k)
        ),
        "left null relation failed",
    )
    return {
        **common_fields,
        "GM_condition_passes": True,
        "violation_count": 0,
        "fixed_domain_null_relation": relation,
        "owner_status": "UNPAID_SPECIALIZATION_EXCEPTION",
        "terminal": "FIXED_DOMAIN_GM_SPECIALIZATION_EXCEPTION",
    }


def disjoint_blocks(start: int, count: int, width: int) -> list[tuple[int, ...]]:
    return [
        tuple(range(start + block * width, start + (block + 1) * width))
        for block in range(count)
    ]


def exact_controls() -> dict[str, Any]:
    prime = 127

    # Same-shape specialization exception: K=11, eleven degree-ten locators.
    core8 = set(range(4, 12))
    exception_supports: list[tuple[int, ...]] = [
        tuple(sorted(core8 | {1, 126})),
        tuple(sorted(core8 | {2, 125})),
        tuple(sorted(core8 | {3, 124})),
    ]
    used = set().union(*(set(support) for support in exception_supports))
    remainder = [point for point in range(prime) if point not in used]
    exception_supports.extend(
        tuple(remainder[10 * block : 10 * (block + 1)]) for block in range(8)
    )
    exception_domain = sorted(set().union(*(set(support) for support in exception_supports)))
    exception = classify_locator_tuple(
        prime=prime,
        domain=exception_domain,
        supports=exception_supports,
    )
    require(
        exception["terminal"] == "FIXED_DOMAIN_GM_SPECIALIZATION_EXCEPTION",
        "same-shape specialization exception disappeared",
    )
    require(exception["coefficient_rank"] == 10, "exception rank drift")
    require(
        exception["fixed_domain_null_relation"] == [1, 100, 26] + [0] * 8,
        "exception null relation drift",
    )
    require(
        len(exception_domain) == 94
        and prime >= len(exception_domain) + 11 - 1,
        "exception field-size guard drift",
    )

    # Same-shape GM failure: three distinct locators share a nine-root core.
    core9 = set(range(4, 13))
    failure_supports: list[tuple[int, ...]] = [
        tuple(sorted(core9 | {1})),
        tuple(sorted(core9 | {2})),
        tuple(sorted(core9 | {3})),
    ]
    used_failure = set().union(*(set(support) for support in failure_supports))
    remainder_failure = [point for point in range(prime) if point not in used_failure]
    failure_supports.extend(
        tuple(remainder_failure[10 * block : 10 * (block + 1)])
        for block in range(8)
    )
    failure_domain = sorted(set().union(*(set(support) for support in failure_supports)))
    failure = classify_locator_tuple(
        prime=prime,
        domain=failure_domain,
        supports=failure_supports,
    )
    require(failure["terminal"] == "GM_MDS_INTERSECTION_VIOLATION", "failure branch drift")
    require(
        failure["first_violation"]["indices_zero_based"] == [0, 1, 2]
        and failure["first_violation"]["common_core"] == list(range(4, 13))
        and failure["common_core_consequence"]["maximum_realized_pair_Johnson_distance"] == 1,
        "common-core certificate drift",
    )

    # Positive same-shape control: eleven disjoint ten-point supports.
    full_rank_supports = disjoint_blocks(0, 11, 10)
    full_rank_domain = list(range(110))
    full_rank = classify_locator_tuple(
        prime=prime,
        domain=full_rank_domain,
        supports=full_rank_supports,
    )
    require(
        full_rank["terminal"]
        == "FIXED_DOMAIN_LOCATOR_INDEPENDENCE_CERTIFIED_FOR_DECLARED_TUPLE"
        and full_rank["coefficient_rank"] == 11,
        "full-rank control drift",
    )
    require(
        prime >= len(full_rank_domain) + 11 - 1,
        "full-rank field-size guard drift",
    )

    # Small transparent exception inside the GM--MDS field-size envelope.
    small_supports = ((1, 10), (2, 9), (3, 8))
    small_domain = sorted(set().union(*(set(support) for support in small_supports)))
    small = classify_locator_tuple(
        prime=11,
        domain=small_domain,
        supports=small_supports,
    )
    require(
        small["terminal"] == "FIXED_DOMAIN_GM_SPECIALIZATION_EXCEPTION"
        and small["coefficient_rank"] == 2
        and small["fixed_domain_null_relation"] == [1, 5, 5],
        "small specialization exception drift",
    )
    require(11 >= len(small_domain) + 3 - 1, "small field-size guard drift")

    return {
        "same_shape_fixed_domain_exception": {
            **exception,
            "supports": [list(support) for support in exception_supports],
            "declared_relation_before_normalization": [47, 1, 79] + [0] * 8,
            "relation_identity": (
                "47*(X^2-1)+1*(X^2-4)+79*(X^2-9)=0 mod 127, "
                "then multiply by the common degree-eight locator"
            ),
        },
        "same_shape_GM_failure": {
            **failure,
            "supports": [list(support) for support in failure_supports],
        },
        "same_shape_full_rank": {
            **full_rank,
            "supports": [list(support) for support in full_rank_supports],
        },
        "small_field_size_envelope_exception": {
            **small,
            "supports": [list(support) for support in small_supports],
            "transparent_relation": (
                "9*(X^2-1)+(X^2-4)+(X^2-9)=0 mod 11"
            ),
        },
    }


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing bound source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        binding("packet-note", NOTE_REL, "theorem, proof, route cut, and scope"),
        binding("packet-readme", README_REL, "replay and artifact contract"),
        binding("packet-python", PYTHON_REL, "exact gate and mutation tests"),
        binding("packet-sage", SAGE_REL, "independent finite-field replay"),
        binding("sparse-note", SPARSE_NOTE_REL, "regular split-locator producer"),
        binding("sparse-certificate", SPARSE_CERT_REL, "frozen predecessor state"),
        binding("sparse-python", SPARSE_PYTHON_REL, "predecessor verifier"),
        binding("generic-cut-note", GENERIC_CUT_NOTE_REL, "refuted rank-only shortcut"),
        binding("generic-cut-certificate", GENERIC_CUT_CERT_REL, "frozen route cut"),
        binding("generic-cut-python", GENERIC_CUT_PYTHON_REL, "route-cut replay"),
        binding("base-slope-note", BASE_SLOPE_NOTE_REL, "base-slope owner split"),
        binding("base-slope-certificate", BASE_SLOPE_CERT_REL, "base-slope ledger state"),
        binding("base-slope-python", BASE_SLOPE_PYTHON_REL, "base-slope replay"),
        binding(
            "raw-v13-domain-source",
            RAW_V13_REL,
            "deployed KoalaBear domain is a coset in F_p^times",
        ),
    ]


def contains_all(text: str, anchors: Sequence[str], label: str) -> None:
    for anchor in anchors:
        require(anchor in text, f"{label} semantic anchor missing: {anchor}")


def validate_source_contracts() -> None:
    note = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    contains_all(
        note,
        [
            "Deployed 11-locator GM--MDS/fixed-domain trichotomy",
            "JOHNSON_COMMON_CORE_CANDIDATE_NOT_PAID",
            "FIXED_DOMAIN_GM_SPECIALIZATION_EXCEPTION",
            "FIXED_DOMAIN_LOCATOR_INDEPENDENCE_CERTIFIED_FOR_DECLARED_TUPLE",
            "retained KoalaBear 11-tuple",
            "CONTROL_ONLY",
            "deployed-scale executor is not implemented",
            "no ledger movement",
            "YELLOW",
        ],
        "packet note",
    )
    readme = (ROOT / README_REL).read_text(encoding="utf-8")
    contains_all(
        readme,
        ["--check", "--tamper-selftest", "Sage", "no deployed support tuple"],
        "packet README",
    )
    sparse = (ROOT / SPARSE_NOTE_REL).read_text(encoding="utf-8")
    contains_all(
        sparse,
        ["REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE", "later owner masks"],
        "sparse predecessor",
    )
    generic = (ROOT / GENERIC_CUT_NOTE_REL).read_text(encoding="utf-8")
    contains_all(
        generic,
        [
            "GENERIC_LOCAL_RANK_TO_LOCATOR_SPAN_SHORTCUT_REFUTED",
            "deployed first-match",
        ],
        "generic route cut",
    )
    raw_v13 = (ROOT / RAW_V13_REL).read_text(encoding="utf-8")
    contains_all(
        raw_v13,
        [
            "for the KoalaBear rows that domain is a coset",
            "subgroup of $\\F_p^\\times$",
        ],
        "raw-v13 deployed-domain source",
    )


def expected_literature_import() -> dict[str, Any]:
    return {
        "primary_source": "Shachar Lovett, MDS matrices over small fields: A proof of the GM-MDS conjecture",
        "arxiv": "1803.02523",
        "url": "https://arxiv.org/abs/1803.02523",
        "imported_result": "Definition 1.4 Property V(k) and Theorem 1.7 Property V*(k)",
        "specialization": (
            "For m binary supports T_i of size j and K=j+1, "
            "|I|+|intersection_{i in I}T_i|<=K for every nonempty I "
            "implies formal-root linear independence."
        ),
        "fixed_domain_nonvanishing_claimed": False,
    }


def expected_deployed_interface() -> dict[str, Any]:
    return {
        "row_id": "koalabear-mca-A1116048",
        "p": P_KB,
        "extension_degree": EXTENSION_DEGREE,
        "n": N_KB,
        "k": K_KB,
        "R": R_KB,
        "A": A_KB,
        "j": J_KB,
        "retained_locator_count": LOCATOR_COUNT,
        "Lovett_parameter_K": LOVETT_K_KB,
        "field_size_condition": f"p >= n+(j+1)-1: {P_KB >= N_KB + LOVETT_K_KB - 1}",
        "predecessor_terminal": "REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE",
        "deployed_domain_statement": (
            "D is a coset of the order-2^21 subgroup of F_p^times"
        ),
        "deployed_domain_source": (
            "experimental/cap25_cap_v13_raw.tex, subsection "
            "Proved base cases of the identity-scale collision problem"
        ),
        "base_slope_prepartition": (
            "after earlier global owners, gamma in F_p is assigned to "
            "residual_base_slope_universe; unresolved regular slopes are extension-valued"
        ),
        "required_input": (
            "one declared tuple of 11 distinct retained regular D-split degree-j supports, "
            "including first-match provenance"
        ),
        "actual_retained_tuple_supplied": False,
        "first_match_provenance_supplied": False,
        "deployed_gate_executed": False,
        "implementation_mode": "CONTROL_ONLY_J10",
        "deployed_scale_executor_implemented": False,
        "required_deployed_backend": (
            "fast product tree or NTT coefficient builder, or a streamed exact nonzero-minor certificate"
        ),
    }


def expected_universal_gate() -> dict[str, Any]:
    return {
        "input": "m=11 distinct degree-j split locator supports T_1,...,T_11",
        "GM_condition": "|I|+|INTERSECTION_{i in I}T_i|<=j+1 for every nonempty I",
        "subset_checks": 2**LOCATOR_COUNT - 1,
        "intersection_failure_branch": {
            "witness": "I,W=INTERSECTION_{i in I}T_i",
            "consequence": (
                "|W|>=j+2-|I|, each |T_i\\W|<=|I|-2, "
                "and every pair has Johnson distance at most |I|-2"
            ),
            "universal_dependence": (
                "L_{T_i} lies in L_W*F[X]_{<=j-|W|}, a space of dimension at most |I|-1"
            ),
            "terminal": "JOHNSON_COMMON_CORE_CANDIDATE_NOT_PAID",
        },
        "intersection_success_branch": {
            "generic_result": "formal-root independence by Lovett Theorem 1.7",
            "mandatory_deployed_test": "exact rank of the locator coefficient matrix over F_p",
            "rank_11_support_only_terminal": (
                "FIXED_DOMAIN_LOCATOR_INDEPENDENCE_CERTIFIED_FOR_DECLARED_TUPLE"
            ),
            "deployed_rank_11_terminal_after_provenance": (
                "DEPLOYED_LOCATOR_INDEPENDENCE_CERTIFIED_AFTER_PROVENANCE"
            ),
            "rank_below_11_terminal": "FIXED_DOMAIN_GM_SPECIALIZATION_EXCEPTION",
        },
        "trichotomy_is_exhaustive_for_declared_tuple": True,
        "trichotomy_is_global_owner_payment": False,
    }


def expected_scope_guards() -> dict[str, Any]:
    return {
        "universal_support_gate_proved": True,
        "fixed_specialization_exception_exists_inside_field_size_envelope": True,
        "actual_koalabear_support_tuple_present": False,
        "actual_first_match_provenance_present": False,
        "Johnson_candidate_paid": False,
        "periodic_or_quotient_owner_inferred": False,
        "deployed_fixed_domain_rank_known": False,
        "control_implementation_only": True,
        "deployed_scale_executor_implemented": False,
        "rank9_closed": False,
        "branch3_closed": False,
        "koalabear_row_closed": False,
        "ledger_movement": 0,
        "next_required_object": "ACTUAL_RETAINED_11_SUPPORTS_WITH_FIRST_MATCH_PROVENANCE",
        "next_required_implementation": "FAST_OR_STREAMED_DEPLOYED_FIXED_DOMAIN_MINOR_EXECUTOR",
    }


def expected_audit_sections() -> dict[str, str]:
    return {
        "statement": "11-locator GM intersection / fixed-domain rank trichotomy",
        "dependencies": "Lovett V*(k) import plus direct common-core dimension and exact finite-field rank calculations",
        "parameter_dependence": "exact in j, the declared 11 supports, and the fixed prime-field specialization",
        "layer_cake_dyadic_summability": "NOT_APPLICABLE",
        "moment_markov_chebyshev": "NOT_APPLICABLE",
        "numerical_evidence": "EXACT_FINITE_FIELD_CONTROLS_ONLY_NOT_DEPLOYED_CENSUS",
        "implementation_scale": "CONTROL_ONLY_J10_DEPLOYED_EXECUTOR_NOT_IMPLEMENTED",
        "universal_gate_verdict": "GREEN_PROVED",
        "deployed_owner_or_payment_verdict": "YELLOW_INPUT_AND_EXECUTOR_MISSING",
    }


def expected_certificate() -> dict[str, Any]:
    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "literature_import": expected_literature_import(),
        "deployed_interface": expected_deployed_interface(),
        "universal_gate": expected_universal_gate(),
        "exact_controls": exact_controls(),
        "scope_guards": expected_scope_guards(),
        "audit_sections": expected_audit_sections(),
        "nonclaims": NONCLAIMS,
    }
    certificate["payload_sha256"] = payload_hash(certificate)
    return certificate


def validate_certificate(certificate: dict[str, Any]) -> None:
    validate_source_contracts()
    require(set(certificate) == TOP_KEYS, "certificate top-level key drift")
    require(certificate.get("payload_sha256") == payload_hash(certificate), "payload hash mismatch")
    expected = expected_certificate()
    require(certificate == expected, "certificate differs from exact recomputation")

    interface = certificate["deployed_interface"]
    require(interface["actual_retained_tuple_supplied"] is False, "invented deployed support tuple")
    require(interface["first_match_provenance_supplied"] is False, "invented first-match provenance")
    require(interface["deployed_gate_executed"] is False, "invented deployed gate execution")
    require(
        interface["implementation_mode"] == "CONTROL_ONLY_J10"
        and interface["deployed_scale_executor_implemented"] is False,
        "deployed implementation overclaim",
    )

    controls = certificate["exact_controls"]
    exception = controls["same_shape_fixed_domain_exception"]
    require(exception["GM_condition_passes"] is True, "exception lost GM admissibility")
    require(exception["coefficient_rank"] == 10, "exception rank overclaim")
    require(
        exception["field_size_at_least_domain_plus_K_minus_1"] is True,
        "exception left field-size envelope",
    )
    failure = controls["same_shape_GM_failure"]
    require(
        failure["owner_status"] == "JOHNSON_COMMON_CORE_CANDIDATE_NOT_PAID",
        "common-core candidate was silently paid",
    )
    require(
        controls["same_shape_full_rank"]["coefficient_rank"] == 11,
        "positive control rank drift",
    )
    scope = certificate["scope_guards"]
    require(scope["ledger_movement"] == 0, "ledger moved")
    require(scope["koalabear_row_closed"] is False, "row closure overclaim")
    require(scope["control_implementation_only"] is True, "control-only guard disabled")
    require(
        scope["deployed_scale_executor_implemented"] is False,
        "invented deployed executor",
    )


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def mutation_cases() -> list[tuple[str, tuple[Any, ...], Any]]:
    return [
        ("schema", ("schema",), SCHEMA + "-tampered"),
        ("status", ("status",), "GREEN_KOALABEAR_CLOSED"),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
        ("literature", ("literature_import", "arxiv"), "0000.00000"),
        ("fixed-domain-import", ("literature_import", "fixed_domain_nonvanishing_claimed"), True),
        ("deployed-j", ("deployed_interface", "j"), J_KB + 1),
        ("deployed-tuple", ("deployed_interface", "actual_retained_tuple_supplied"), True),
        ("deployed-provenance", ("deployed_interface", "first_match_provenance_supplied"), True),
        ("deployed-executed", ("deployed_interface", "deployed_gate_executed"), True),
        ("implementation-mode", ("deployed_interface", "implementation_mode"), "DEPLOYED"),
        ("deployed-executor", ("deployed_interface", "deployed_scale_executor_implemented"), True),
        ("gm-formula", ("universal_gate", "GM_condition"), "pairwise only"),
        ("subset-count", ("universal_gate", "subset_checks"), 1023),
        ("failure-paid", ("universal_gate", "intersection_failure_branch", "terminal"), "PAID_JOHNSON"),
        ("success-terminal", ("universal_gate", "intersection_success_branch", "rank_11_support_only_terminal"), "ROW_CLOSED"),
        ("deployed-success-terminal", ("universal_gate", "intersection_success_branch", "deployed_rank_11_terminal_after_provenance"), "ROW_CLOSED"),
        ("exception-terminal", ("universal_gate", "intersection_success_branch", "rank_below_11_terminal"), "IMPOSSIBLE"),
        ("global-payment", ("universal_gate", "trichotomy_is_global_owner_payment"), True),
        ("exception-rank", ("exact_controls", "same_shape_fixed_domain_exception", "coefficient_rank"), 11),
        ("exception-gm", ("exact_controls", "same_shape_fixed_domain_exception", "GM_condition_passes"), False),
        ("exception-relation", ("exact_controls", "same_shape_fixed_domain_exception", "fixed_domain_null_relation", 0), 2),
        ("exception-support", ("exact_controls", "same_shape_fixed_domain_exception", "supports", 0, 0), 2),
        ("exception-field", ("exact_controls", "same_shape_fixed_domain_exception", "field_size_at_least_domain_plus_K_minus_1"), False),
        ("failure-owner", ("exact_controls", "same_shape_GM_failure", "owner_status"), "PAID_JOHNSON"),
        ("failure-core", ("exact_controls", "same_shape_GM_failure", "first_violation", "common_core_size"), 8),
        ("failure-radius", ("exact_controls", "same_shape_GM_failure", "common_core_consequence", "maximum_realized_pair_Johnson_distance"), 2),
        ("full-rank", ("exact_controls", "same_shape_full_rank", "coefficient_rank"), 10),
        ("small-rank", ("exact_controls", "small_field_size_envelope_exception", "coefficient_rank"), 3),
        ("small-relation", ("exact_controls", "small_field_size_envelope_exception", "fixed_domain_null_relation", 1), 6),
        ("scope-tuple", ("scope_guards", "actual_koalabear_support_tuple_present"), True),
        ("scope-provenance", ("scope_guards", "actual_first_match_provenance_present"), True),
        ("scope-Johnson", ("scope_guards", "Johnson_candidate_paid"), True),
        ("scope-periodic", ("scope_guards", "periodic_or_quotient_owner_inferred"), True),
        ("scope-rank", ("scope_guards", "deployed_fixed_domain_rank_known"), True),
        ("scope-control", ("scope_guards", "control_implementation_only"), False),
        ("scope-executor", ("scope_guards", "deployed_scale_executor_implemented"), True),
        ("scope-rank9", ("scope_guards", "rank9_closed"), True),
        ("scope-branch3", ("scope_guards", "branch3_closed"), True),
        ("scope-row", ("scope_guards", "koalabear_row_closed"), True),
        ("scope-ledger", ("scope_guards", "ledger_movement"), 1),
        ("audit-verdict", ("audit_sections", "deployed_owner_or_payment_verdict"), "GREEN"),
        ("nonclaim", ("nonclaims", 0), "A deployed tuple is supplied."),
    ]


def run_tamper_selftest() -> None:
    expected = expected_certificate()
    # A broken baseline must not make every mutation look rejected.
    validate_certificate(expected)
    rejected = 0
    for name, path, replacement in mutation_cases():
        mutated = copy.deepcopy(expected)
        set_path(mutated, path, replacement)
        mutated["payload_sha256"] = payload_hash(mutated)
        try:
            validate_certificate(mutated)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"mutation survived: {name}")

    duplicate = canonical_bytes(expected).decode("utf-8")
    duplicate = duplicate.replace("{", '{"schema":"duplicate",', 1)
    try:
        parse_json(duplicate, "duplicate-key mutation")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("duplicate-key mutation survived")

    nonfinite = '{"x":NaN}'
    try:
        parse_json(nonfinite, "nonfinite mutation")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("nonfinite mutation survived")

    total = len(mutation_cases()) + 2
    require(rejected == total, "tamper rejection count drift")
    print(f"PASS tamper self-test: {rejected}/{total} mutations rejected")


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    certificate = expected_certificate()
    CERT_PATH.write_text(
        json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {CERT_PATH.relative_to(ROOT)}")


def check_certificate() -> None:
    require(CERT_PATH.is_file(), f"missing certificate: {CERT_PATH.relative_to(ROOT)}")
    certificate = load_json(CERT_PATH)
    validate_certificate(certificate)
    controls = certificate["exact_controls"]
    print("PASS M1 KoalaBear rank-nine GM--MDS fixed-domain gate v1")
    print(
        "  controls:",
        controls["same_shape_GM_failure"]["terminal"],
        controls["same_shape_fixed_domain_exception"]["terminal"],
        controls["same_shape_full_rank"]["terminal"],
    )
    print("  deployed gate: INPUT MISSING; no owner payment; no ledger movement")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="write the canonical certificate")
    group.add_argument("--tamper-selftest", action="store_true", help="run mutation tests")
    group.add_argument("--check", action="store_true", help="check the committed certificate")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.write:
        write_certificate()
    elif args.tamper_selftest:
        run_tamper_selftest()
    else:
        check_certificate()


if __name__ == "__main__":
    main()
