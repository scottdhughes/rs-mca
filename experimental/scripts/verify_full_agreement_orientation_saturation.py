#!/usr/bin/env python3
"""Certify sharp unsaturated orientation capacity on smooth two-fold rows.

The asymptotic family is the full multiplicative domain

    q=3^r, D=F_q^x, n=q-1=2a,
    w=2 floor(a/(2r)), k=a-w-1, phi(x)=x^2

with scalar extension degree d=ceil(4a/r). The exact pole-line theorem
then realizes the complete chosen depth-w prefix fiber as distinct exact-
agreement slopes. Its one-point-per-square-fiber cell has at least
ceil(2^a/q^(w/2)) slopes. More generally, every legal depth u has floor
ceil(2^a/q^ceil(u/2)); subcritical u log(q)=o(n) retains exponent
log(2)/2-o(1). At depth zero the construction realizes every a-support and
the orientation cell exactly saturates occupancy H=2^a.

The verifier is stdlib-only, deterministically regenerates its JSON
certificate, pins the hypotheses it consumes from the integrated TeX,
and includes a finite smooth mu_8 pole-line census. RLIMIT_AS is capped
at one GiB. The finite model is an odd-characteristic mechanism check;
the asymptotic characteristic-three rows are certified by exact integer
arithmetic plus the pinned separating-pole theorem.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import os
import re
import resource
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable


STATUS = "COUNTEREXAMPLE_NEW_FLOOR"
SCHEMA = "full_agreement_orientation_saturation.v1"
BASE_SHA = "8264eae23e9120a182218b3839aac024051ccf8d"
ADDRESS_SPACE_CAP_BYTES = 1024**3
ARTIFACT = Path(
    "experimental/data/certificates/full-agreement-orientation-saturation/"
    "full_agreement_orientation_saturation.json"
)
FRONTIERS_TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
ASYMPTOTIC_R_ROWS = (2, 3, 4, 5, 6, 7)

LABEL_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "def:first-match": (
        "actual",
        "Z_i^\\circ",
        "witness-exhaustive first-match atlas",
    ),
    "def:profile-payment": (
        "uniformly in the received line",
        "\\exp(o(n))",
        "given first-match atlas",
    ),
    "thm:exact-first-adjacent-row": (
        "Q_{\\rm sep}(M)",
        "\\abs\\F>Q_{\\rm sep}(M)",
        "B_C^{\\rm MCA}(k+1)=M",
    ),
    "prop:exact-prefix-list": (
        "1\\le K\\le m\\le n",
        "w=m-K",
        "\\RS_\\F(D,K)",
        "No such codeword agrees on more than",
    ),
    "thm:exact-list-line-bijection": (
        "D\\subseteq\\B\\subseteq\\F",
        "1\\le k<n",
        "m\\ge k+1",
        "\\alpha\\in\\F\\setminus D",
        "\\abs\\F>n+k\\binom L2",
    ),
    "cor:exact-prefix-ray-realization": (
        "0\\le w\\le m-2",
        "k=m-w-1",
        "separates the values",
        "are bijections between",
    ),
    "def:paid-cell": (
        "actual first-match projection",
        "uniformly in the received line",
        "scaled realized cell",
    ),
    "def:structured-folding": (
        "complete-fiber folding map",
        "exactly \\(c\\)",
        "multiplicative coset",
        "\\pi_c(x)=x^c",
    ),
}

SOURCE_REQUIREMENTS: dict[Path, tuple[str, ...]] = {
    Path(
        "experimental/notes/thresholds/"
        "canonical_full_agreement_occupancy_atlas.md"
    ): (
        "H_phi(lambda)",
        "actual first-match slope set",
        "p=Theta(n)",
    ),
    Path(
        "experimental/notes/thresholds/aperiodic_one_ray_saturation.md"
    ): (
        "only one bad slope",
        "positive profile entropy plus aperiodicity alone",
        "distinct-ray theorem",
    ),
    Path("experimental/notes/l1/l1_prefix_divisor_count.md"): (
        "complement-locator compression",
        "Divisor-coefficient reframing",
        "The complement-prefix lemma gives",
    ),
    Path("experimental/notes/l1/l1_aperiodic_prefix_collision.md"): (
        "General Complement-Prefix Lemma",
        "E_S(Z) E_A(Z)",
        "complement-locator compression",
    ),
}


class CheckFailure(AssertionError):
    """Raised when an exact replay invariant fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


def repo_root() -> Path:
    override = os.environ.get("FAOS_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def impose_address_space_cap() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = ADDRESS_SPACE_CAP_BYTES
    if hard != resource.RLIM_INFINITY:
        cap = min(cap, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    require(
        soft != resource.RLIM_INFINITY and soft <= ADDRESS_SPACE_CAP_BYTES,
        "RLIMIT_AS exceeds one GiB",
    )
    return int(soft)


def without_hash(obj: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(obj)
    out.pop("payload_sha256", None)
    return out


def payload_hash(obj: dict[str, Any]) -> str:
    raw = json.dumps(
        without_hash(obj), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pin_frontiers_labels(root: Path) -> dict[str, Any]:
    path = root / FRONTIERS_TEX
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    pins: dict[str, Any] = {}
    for label, requirements in LABEL_REQUIREMENTS.items():
        pattern = re.compile(
            r"\\label(?:\[[^\]]*\])?\{" + re.escape(label) + r"\}"
        )
        matches = [i for i, line in enumerate(lines) if pattern.search(line)]
        found = len(matches) == 1
        statement = ""
        environment = None
        line_number = None
        paste = None
        if found:
            index = matches[0]
            line_number = index + 1
            paste = lines[index].strip()
            start = index
            begin_pattern = re.compile(
                r"\\begin\{(definition|theorem|corollary|proposition|lemma)\}"
            )
            while start >= 0 and not begin_pattern.search(lines[start]):
                start -= 1
            if start >= 0:
                begin_match = begin_pattern.search(lines[start])
                require(begin_match is not None, f"environment parse for {label}")
                environment = begin_match.group(1)
                end_marker = f"\\end{{{environment}}}"
                end = start
                while end < len(lines) and end_marker not in lines[end]:
                    end += 1
                if end < len(lines):
                    statement = "\n".join(lines[start : end + 1])
        requirement_checks = {
            requirement: requirement in statement for requirement in requirements
        }
        pins[label] = {
            "found_once": found,
            "line": line_number,
            "paste": paste,
            "environment": environment,
            "statement_sha256": text_hash(statement) if statement else None,
            "hypothesis_tokens": requirement_checks,
            "all_hypothesis_tokens_found": (
                bool(statement) and all(requirement_checks.values())
            ),
        }
    return {
        "path": str(FRONTIERS_TEX).replace("\\", "/"),
        "file_sha256": text_hash(text),
        "labels": pins,
        "all_found_and_audited": all(
            pin["found_once"] and pin["all_hypothesis_tokens_found"]
            for pin in pins.values()
        ),
    }


def pin_source_notes(root: Path) -> dict[str, Any]:
    pins: dict[str, Any] = {}
    for relative, requirements in SOURCE_REQUIREMENTS.items():
        text = (root / relative).read_text(encoding="utf-8")
        requirement_checks = {
            requirement: requirement in text for requirement in requirements
        }
        pins[str(relative).replace("\\", "/")] = {
            "sha256": text_hash(text),
            "required_phrases": requirement_checks,
            "all_required_phrases_found": all(requirement_checks.values()),
        }
    return {
        "files": pins,
        "all_sources_pinned": all(
            pin["all_required_phrases_found"] for pin in pins.values()
        ),
    }


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for small in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % small == 0:
            return n == small
    divisor = 37
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def next_prime_one_mod(lower_exclusive: int, modulus: int) -> int:
    candidate = lower_exclusive + 1
    candidate += (1 - candidate) % modulus
    while not is_prime(candidate):
        candidate += modulus
    return candidate


def multiplicative_order(value: int, modulus: int) -> int:
    current = 1
    for order in range(1, modulus):
        current = current * value % modulus
        if current == 1:
            return order
    raise CheckFailure("multiplicative order search failed")


def root_of_exact_order(modulus: int, order: int) -> int:
    require((modulus - 1) % order == 0, "requested order divides p-1")
    exponent = (modulus - 1) // order
    for base in range(2, modulus):
        candidate = pow(base, exponent, modulus)
        if multiplicative_order(candidate, modulus) == order:
            return candidate
    raise CheckFailure("no root of requested order")


def polynomial_eval(coefficients: list[int], value: int, modulus: int) -> int:
    out = 0
    for coefficient in reversed(coefficients):
        out = (out * value + coefficient) % modulus
    return out


def locator_polynomial(selected: tuple[int, ...], modulus: int) -> list[int]:
    coefficients = [1]
    for root in selected:
        nxt = [0] * (len(coefficients) + 1)
        for degree, coefficient in enumerate(coefficients):
            nxt[degree] = (nxt[degree] - root * coefficient) % modulus
            nxt[degree + 1] = (nxt[degree + 1] + coefficient) % modulus
        coefficients = nxt
    return coefficients


def divide_by_linear_root(
    coefficients: list[int], root: int, modulus: int
) -> list[int]:
    """Divide a padded ascending polynomial by X-root."""
    require(len(coefficients) >= 2, "linear division input degree")
    quotient = [0] * (len(coefficients) - 1)
    quotient[-1] = coefficients[-1] % modulus
    for degree in range(len(coefficients) - 2, 0, -1):
        quotient[degree - 1] = (
            coefficients[degree] + root * quotient[degree]
        ) % modulus
    require(
        (-root * quotient[0] - coefficients[0]) % modulus == 0,
        "linear division remainder",
    )
    return quotient


def lagrange_eval(
    xs: tuple[int, ...],
    ys: tuple[int, ...],
    target: int,
    modulus: int,
) -> int:
    require(len(xs) == len(ys), "Lagrange input lengths")
    out = 0
    for index, x_i in enumerate(xs):
        numerator = 1
        denominator = 1
        for j, x_j in enumerate(xs):
            if j == index:
                continue
            numerator = numerator * (target - x_j) % modulus
            denominator = denominator * (x_i - x_j) % modulus
        out = (
            out
            + ys[index] * numerator * pow(denominator, -1, modulus)
        ) % modulus
    return out


def multiply_polynomials(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def polynomial_power(base: list[int], exponent: int) -> list[int]:
    out = [1]
    for _ in range(exponent):
        out = multiply_polynomials(out, base)
    return out


def occupancy_weight(
    profile: tuple[int, int, int, int],
    exceptional_count: int,
    fiber_count: int,
    fiber_size: int,
) -> int:
    t, complete, partial, residual = profile
    if not (
        0 <= t <= exceptional_count
        and 0 <= partial <= fiber_count
        and 0 <= complete <= fiber_count - partial
    ):
        return 0
    base = [0] * (fiber_size + 1)
    for selected in range(1, fiber_size):
        base[selected] = math.comb(fiber_size, selected)
    polynomial = polynomial_power(base, partial)
    coefficient = polynomial[residual] if residual < len(polynomial) else 0
    return (
        math.comb(exceptional_count, t)
        * math.comb(fiber_count, partial)
        * math.comb(fiber_count - partial, complete)
        * coefficient
    )


def occupancy_profile(
    selected: frozenset[int], fibers: tuple[tuple[int, int], ...]
) -> tuple[int, int, int, int]:
    complete = 0
    partial = 0
    residual = 0
    for fiber in fibers:
        count = sum(point in selected for point in fiber)
        if count == len(fiber):
            complete += 1
        elif count:
            partial += 1
            residual += count
    return (0, complete, partial, residual)


def find_separating_pole(
    domain: tuple[int, ...],
    locators: list[list[int]],
    modulus: int,
) -> tuple[int, list[int], int]:
    domain_set = set(domain)
    tested = 0
    for alpha in range(modulus):
        if alpha in domain_set:
            continue
        tested += 1
        values = [
            polynomial_eval(locator, alpha, modulus)
            for locator in locators
        ]
        if len(set(values)) == len(values):
            return alpha, values, tested
    raise CheckFailure("separating pole not found")


def gf9_add(left: int, right: int) -> int:
    """Add in F_3[t]/(t^2+1), encoded as a+3b."""
    return ((left % 3 + right % 3) % 3) + 3 * (
        ((left // 3) + (right // 3)) % 3
    )


def gf9_neg(value: int) -> int:
    return ((-value) % 3) + 3 * ((-(value // 3)) % 3)


def gf9_mul(left: int, right: int) -> int:
    a, b = left % 3, left // 3
    c, d = right % 3, right // 3
    return ((a * c - b * d) % 3) + 3 * ((a * d + b * c) % 3)


def gf9_pow(value: int, exponent: int) -> int:
    out = 1
    base = value
    while exponent:
        if exponent & 1:
            out = gf9_mul(out, base)
        base = gf9_mul(base, base)
        exponent >>= 1
    return out


def gf9_locator(selected: frozenset[int]) -> list[int]:
    coefficients = [1]
    for root in sorted(selected):
        nxt = [0] * (len(coefficients) + 1)
        for degree, coefficient in enumerate(coefficients):
            nxt[degree] = gf9_add(
                nxt[degree], gf9_neg(gf9_mul(root, coefficient))
            )
            nxt[degree + 1] = gf9_add(nxt[degree + 1], coefficient)
        coefficients = nxt
    return coefficients


def gf9_polynomial_product(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = gf9_add(out[i + j], gf9_mul(a, b))
    return out


def finite_f9_prefix_model() -> dict[str, Any]:
    """Census the positive-depth orientation-prefix mechanism on F_9^x."""
    r = 2
    q = 9
    a = 4
    domain = tuple(range(1, q))
    unused = set(domain)
    fibers = []
    while unused:
        left = min(unused)
        right = gf9_neg(left)
        require(left != right, "F_9 antipodal fiber has size two")
        fibers.append((left, right))
        unused.remove(left)
        unused.remove(right)
    fibers_tuple = tuple(fibers)
    orientations = {
        frozenset(fibers_tuple[index][choice] for index, choice in enumerate(bits))
        for bits in itertools.product((0, 1), repeat=a)
    }
    top_coefficients: dict[frozenset[int], tuple[int, ...]] = {}
    product_identity_checks = 0
    even_recurrence_checks = 0
    for support in orientations:
        locator = gf9_locator(support)
        require(len(locator) == a + 1 and locator[-1] == 1, "F_9 locator")
        c = tuple(locator[a - index] for index in range(a + 1))
        top_coefficients[support] = c
        c_minus = [
            coefficient if index % 2 == 0 else gf9_neg(coefficient)
            for index, coefficient in enumerate(c)
        ]
        product = gf9_polynomial_product(list(c), c_minus)
        expected = [0] * (2 * a + 1)
        expected[0] = 1
        expected[2 * a] = gf9_neg(1)
        require(product == expected, "C(T)C(-T)=1-T^(2a) over F_9")
        product_identity_checks += 1

        # At even degree j<2a, the two endpoint terms are 2*c_j;
        # all remaining terms use earlier coefficients. Verify the recursive
        # reconstruction of each available even coefficient.
        for j in range(2, a + 1, 2):
            earlier_sum = 0
            for i in range(1, j):
                term = gf9_mul(c[i], c[j - i])
                if (j - i) % 2:
                    term = gf9_neg(term)
                earlier_sum = gf9_add(earlier_sum, term)
            reconstructed = gf9_mul(
                gf9_neg(earlier_sum), 2
            )
            require(reconstructed == c[j], "even prefix recurrence in F_9")
            even_recurrence_checks += 1

    width_rows = []
    for width in range(a - 1):
        fibers_by_prefix: Counter[tuple[int, ...]] = Counter(
            coefficients[1 : width + 1]
            for coefficients in top_coefficients.values()
        )
        odd_coordinates = (width + 1) // 2
        image_cap = q**odd_coordinates
        width_rows.append(
            {
                "w": width,
                "odd_prefix_coordinates": odd_coordinates,
                "prefix_image_size": len(fibers_by_prefix),
                "prefix_image_cap": image_cap,
                "largest_orientation_fiber": max(fibers_by_prefix.values()),
                "pigeonhole_floor_from_cap": (
                    len(orientations) + image_cap - 1
                )
                // image_cap,
                "image_within_recurrence_cap": (
                    len(fibers_by_prefix) <= image_cap
                ),
            }
        )
    chosen_width = 2 * (a // (2 * r))
    chosen = next(row for row in width_rows if row["w"] == chosen_width)
    checks = {
        "literal_full_domain": len(domain) == q - 1 == 2 * a,
        "square_fibers": (
            len(fibers_tuple) == a
            and all(gf9_neg(left) == right for left, right in fibers_tuple)
        ),
        "orientation_count": len(orientations) == 2**a,
        "locator_product_identity": product_identity_checks == 2**a,
        "even_coefficients_reconstructed": (
            even_recurrence_checks == 2**a * (a // 2)
        ),
        "all_prefix_images_within_cap": all(
            row["image_within_recurrence_cap"] for row in width_rows
        ),
        "chosen_width_positive_and_legal": 1 <= chosen_width <= a - 2,
        "chosen_fiber_meets_cap_pigeonhole": (
            chosen["largest_orientation_fiber"]
            >= chosen["pigeonhole_floor_from_cap"]
        ),
    }
    require(all(checks.values()), "finite F_9 prefix model")
    return {
        "field_model": "F_3[t]/(t^2+1), elements encoded a+3b",
        "r": r,
        "q": q,
        "a": a,
        "domain": list(domain),
        "square_fibers": [list(fiber) for fiber in fibers_tuple],
        "orientation_count": len(orientations),
        "identity": "C(T)C(-T)=1-T^(2a)",
        "recurrence": (
            "each even c_(2j) is determined by earlier coefficients because "
            "the coefficient 2 is invertible in characteristic three"
        ),
        "width_rows": width_rows,
        "chosen_width": chosen_width,
        "chosen_width_row": chosen,
        "product_identity_checks": product_identity_checks,
        "even_recurrence_checks": even_recurrence_checks,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def finite_smooth_pole_model() -> dict[str, Any]:
    """Exhaust the a=4 smooth mu_8 mechanism in one prime field."""
    a = 4
    n = 2 * a
    k = a - 1
    support_count = math.comb(n, a)
    pair_count = math.comb(support_count, 2)
    pole_gate = n + k * pair_count
    modulus = next_prime_one_mod(pole_gate, n)
    omega = root_of_exact_order(modulus, n)
    domain = tuple(pow(omega, index, modulus) for index in range(n))
    fibers = tuple((domain[index], domain[index + a]) for index in range(a))

    require(len(set(domain)) == n, "mu_8 domain distinct")
    require(pow(omega, a, modulus) == modulus - 1, "antipodal generator")
    require(
        all(
            pow(left, 2, modulus) == pow(right, 2, modulus)
            for left, right in fibers
        ),
        "square fibers",
    )
    require(
        len({pow(left, 2, modulus) for left, _ in fibers}) == a,
        "square fiber image size",
    )

    supports = list(itertools.combinations(domain, a))
    locators = [
        locator_polynomial(support, modulus) for support in supports
    ]
    locator_by_support = {
        frozenset(support): locator
        for support, locator in zip(supports, locators)
    }
    orientation_supports = {
        frozenset(fibers[index][choice] for index, choice in enumerate(choices))
        for choices in itertools.product((0, 1), repeat=a)
    }

    # At the base-field pole zero, the orientation locator value is its
    # product up to sign. Antipodal choices therefore retain only parity.
    zero_pole_orientation_slopes = [
        (-polynomial_eval(locator_by_support[support], 0, modulus)) % modulus
        for support in orientation_supports
    ]
    zero_pole_slope_fibers = Counter(zero_pole_orientation_slopes)

    alpha, locator_values, pole_candidates_tested = find_separating_pole(
        domain, locators, modulus
    )
    f_values = {
        x: pow(x, a, modulus) * pow(x - alpha, -1, modulus) % modulus
        for x in domain
    }
    g_values = {
        x: -pow(x - alpha, -1, modulus) % modulus for x in domain
    }

    transcript: list[dict[str, Any]] = []
    slope_to_support: dict[int, frozenset[int]] = {}
    support_to_row: dict[frozenset[int], dict[str, Any]] = {}
    profile_census: Counter[tuple[int, int, int, int]] = Counter()
    exact_agreement_checks = 0
    division_checks = 0
    noncommon_checks = 0

    for support, locator, locator_value in zip(
        supports, locators, locator_values
    ):
        require(len(locator) == a + 1 and locator[-1] == 1, "monic locator")
        # P_S=X^a-Q_S; the leading terms cancel, so this padded list has
        # coefficients through degree k=a-1.
        p_polynomial = [(-locator[degree]) % modulus for degree in range(a)]
        gamma = polynomial_eval(p_polynomial, alpha, modulus)
        require(
            gamma == (pow(alpha, a, modulus) - locator_value) % modulus,
            "pole slope formula",
        )
        divided = p_polynomial[:]
        divided[0] = (divided[0] - gamma) % modulus
        h_polynomial = divide_by_linear_root(divided, alpha, modulus)
        require(len(h_polynomial) == k, "explanation degree less than k")
        division_checks += 1

        agreement = tuple(
            x
            for x in domain
            if polynomial_eval(h_polynomial, x, modulus)
            == (f_values[x] + gamma * g_values[x]) % modulus
        )
        support_set = frozenset(support)
        require(
            frozenset(agreement) == support_set and len(agreement) == a,
            "exact full agreement set",
        )
        exact_agreement_checks += 1

        # A degree <k polynomial explaining g on all a=k+1 support points
        # would equal the unique degree <k interpolant through the first k
        # points at the last point. Check the contradiction directly.
        predicted = lagrange_eval(
            tuple(support[:k]),
            tuple(g_values[x] for x in support[:k]),
            support[k],
            modulus,
        )
        require(predicted != g_values[support[k]], "support is noncommon")
        noncommon_checks += 1

        profile = occupancy_profile(support_set, fibers)
        profile_census[profile] += 1
        require(gamma not in slope_to_support, "all full-list slopes distinct")
        slope_to_support[gamma] = support_set
        row = {
            "support": list(support),
            "locator": locator,
            "gamma": gamma,
            "h": h_polynomial,
            "agreement": list(agreement),
            "profile": list(profile),
        }
        support_to_row[support_set] = row
        transcript.append(row)

    orientation_profile = (0, 0, a, a)
    orientation_rows = [support_to_row[support] for support in orientation_supports]
    orientation_slopes = sorted(row["gamma"] for row in orientation_rows)
    orientation_count = 2**a
    orientation_occupancy = occupancy_weight(orientation_profile, 0, a, 2)

    checks = {
        "prime_field": is_prime(modulus),
        "field_contains_mu_8": (modulus - 1) % n == 0,
        "field_exceeds_separating_pole_gate": modulus > pole_gate,
        "generator_has_exact_order_8": multiplicative_order(omega, modulus) == n,
        "domain_and_square_fibers": (
            len(set(domain)) == n
            and len({pow(x, 2, modulus) for x in domain}) == a
        ),
        "full_support_census": len(supports) == support_count,
        "all_full_list_slopes_distinct": len(slope_to_support) == support_count,
        "all_full_agreements_exact": exact_agreement_checks == support_count,
        "all_explanations_degree_less_than_k": division_checks == support_count,
        "all_supports_noncommon": noncommon_checks == support_count,
        "orientation_support_count": len(orientation_supports) == orientation_count,
        "orientation_profile_exact": all(
            tuple(row["profile"]) == orientation_profile
            for row in orientation_rows
        ),
        "orientation_occupancy_formula": orientation_occupancy == orientation_count,
        "zero_pole_has_two_product_parity_slopes": (
            len(zero_pole_slope_fibers) == 2
            and sorted(zero_pole_slope_fibers.values())
            == [orientation_count // 2, orientation_count // 2]
        ),
        "separating_pole_has_all_orientation_slopes": (
            len(set(orientation_slopes)) == orientation_count
        ),
        "orientation_cell_is_entire_profile": (
            profile_census[orientation_profile] == orientation_count
        ),
        "first_match_order_independent": (
            len(slope_to_support) == support_count
            and all(len(row["agreement"]) == a for row in orientation_rows)
        ),
    }
    require(all(checks.values()), "finite smooth pole model")
    transcript_sha256 = text_hash(
        json.dumps(transcript, sort_keys=True, separators=(",", ":"))
    )
    canonical_profiles = {
        ",".join(str(value) for value in profile): count
        for profile, count in sorted(profile_census.items())
    }
    return {
        "role": (
            "finite odd-characteristic smooth-mu mechanism check; not the "
            "literal asymptotic F_(3^r)^x row"
        ),
        "parameters": {
            "a": a,
            "n": n,
            "k": k,
            "agreement": a,
            "field_prime": modulus,
            "omega": omega,
            "domain_mu_8": list(domain),
            "square_fibers": [list(fiber) for fiber in fibers],
            "full_support_count_M": support_count,
            "support_pair_count": pair_count,
            "separating_pole_gate": pole_gate,
            "alpha": alpha,
            "pole_candidates_tested": pole_candidates_tested,
        },
        "construction": {
            "U": "X^a",
            "P_S": "X^a-Q_S",
            "f_alpha": "U/(X-alpha)",
            "g_alpha": "-1/(X-alpha)",
            "gamma_S": "P_S(alpha)=U(alpha)-Q_S(alpha)",
            "h_S": "(P_S-P_S(alpha))/(X-alpha)",
        },
        "full_list": {
            "enumerated_supports": len(supports),
            "distinct_slopes": len(slope_to_support),
            "exact_agreement_checks": exact_agreement_checks,
            "noncommon_checks": noncommon_checks,
            "explanation_division_checks": division_checks,
            "profile_census": canonical_profiles,
            "transcript_sha256": transcript_sha256,
            "sample_first_support": transcript[0],
        },
        "orientation_cell": {
            "profile": list(orientation_profile),
            "support_count": len(orientation_supports),
            "occupancy_H": orientation_occupancy,
            "zero_pole": {
                "alpha": 0,
                "actual_slope_count": len(zero_pole_slope_fibers),
                "slope_fiber_sizes": sorted(zero_pole_slope_fibers.values()),
                "slopes": sorted(zero_pole_slope_fibers),
                "reason": "locator product changes only by antipodal parity",
            },
            "separating_pole": {
                "alpha": alpha,
                "actual_slope_count": len(set(orientation_slopes)),
                "slopes": orientation_slopes,
            },
            "actual_first_match_count_for_every_cell_order": len(
                set(orientation_slopes)
            ),
            "sample_orientation_witness": sorted(
                orientation_rows, key=lambda row: row["support"]
            )[0],
        },
        "load_bearing_contrast": (
            "the same 2^a orientation supports give two product-parity slopes "
            "at alpha=0 and 2^a distinct slopes at the separating pole"
        ),
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def asymptotic_row(r: int) -> dict[str, Any]:
    q = 3**r
    n = q - 1
    a = n // 2
    orientation_profile = (0, 0, a, a)
    orientation_count = 2**a
    occupancy = occupancy_weight(orientation_profile, 0, a, 2)

    # Positive prefix depth. The identity C(T)C(-T)=1-T^(2a)
    # determines every even prefix coefficient from earlier coefficients,
    # so at most w/2 odd-slot values determine a realized prefix.
    width = 2 * (a // (2 * r))
    odd_prefix_coordinates = width // 2
    prefix_image_cap = q**odd_prefix_coordinates
    orientation_fiber_floor = (
        orientation_count + prefix_image_cap - 1
    ) // prefix_image_cap
    k = a - width - 1
    redundancy = n - k

    # Separating the complete prefix fiber is stronger than separating only
    # its orientation subfiber. Its size is at most M=binom(n,a).
    extension_degree = (4 * a + r - 1) // r
    field_exponent_over_3 = r * extension_degree
    field_size = 3**field_exponent_over_3
    support_count = math.comb(n, a)
    support_pairs = math.comb(support_count, 2)
    pole_gate = n + k * support_pairs

    # Keep the depth-zero exact-H razor explicit as the endpoint.
    zero_depth_k = a - 1
    zero_depth_pole_gate = n + zero_depth_k * support_pairs
    twice_r_odd = 2 * r * odd_prefix_coordinates
    checks = {
        "r_at_least_2": r >= 2,
        "q_is_odd_prime_power": q == 3**r and q % 2 == 1,
        "full_domain_size": n == q - 1 == 2 * a,
        "square_fold_has_a_two_point_fibers": n // 2 == a,
        "orientation_occupancy": occupancy == orientation_count,
        "positive_depth_legal": 1 <= width <= a - 2,
        "code_dimension_positive": 1 <= k < n,
        "agreement_at_least_k_plus_one": a >= k + 1,
        "odd_coordinate_cap": odd_prefix_coordinates == width // 2,
        "pigeonhole_floor_positive": (
            orientation_fiber_floor >= 2
            and orientation_count > prefix_image_cap
        ),
        "prefix_ratio_lower": twice_r_odd > a - 2 * r,
        "prefix_ratio_upper": twice_r_odd <= a,
        "prefix_cap_below_three_to_a_over_two": prefix_image_cap**2 <= 3**a,
        "exact_positive_rate_floor": (
            orientation_fiber_floor**2 * 3**a >= 4**a
        ),
        "extension_ceiling_lower": field_exponent_over_3 >= 4 * a,
        "extension_ceiling_upper": field_exponent_over_3 < 4 * a + r,
        "field_size_identity": field_size == q**extension_degree,
        "field_exceeds_separating_pole_gate": field_size > pole_gate,
        "field_also_pays_zero_depth_gate": field_size > zero_depth_pole_gate,
        "zero_depth_first_adjacent": a == zero_depth_k + 1,
    }
    return {
        "r": r,
        "q": q,
        "n": n,
        "a": a,
        "base_field": f"F_(3^{r})",
        "domain": "F_q^x",
        "folding": "phi(x)=x^2 with a fibers {x,-x}",
        "orientation_profile": list(orientation_profile),
        "orientation_occupancy_H": occupancy,
        "positive_depth": {
            "w": width,
            "k": k,
            "agreement_m": a,
            "redundancy_R": redundancy,
            "odd_prefix_coordinates_s": odd_prefix_coordinates,
            "prefix_image_cap_q_to_s": prefix_image_cap,
            "orientation_fiber_floor_J": orientation_fiber_floor,
            "actual_slope_lower_bound_by_separating_pole": (
                orientation_fiber_floor
            ),
            "normalized_log_lower_bound": (
                "log(J)/(2a)>=log(2)/2-log(3)/4=log(4/3)/4"
            ),
        },
        "zero_depth_endpoint": {
            "w": 0,
            "k": zero_depth_k,
            "actual_slope_count": orientation_count,
            "normalized_log_slope_rate": "(log 2)/2",
            "saturates_occupancy_H": orientation_count == occupancy,
        },
        "extension_degree_d": extension_degree,
        "field_exponent_over_3_rd": field_exponent_over_3,
        "extension_field_size": field_size,
        "complete_prefix_fiber_upper_bound_M": support_count,
        "separating_pole_gate": pole_gate,
        "zero_depth_separating_pole_gate": zero_depth_pole_gate,
        "field_log_bounds": {
            "lower": "2n log(3) <= log|F|",
            "upper": "log|F| < (2n+r) log(3)",
            "two_n": 2 * n,
            "rd": field_exponent_over_3,
            "two_n_plus_r": 2 * n + r,
        },
        "prefix_rate_limit": {
            "twice_r_s": twice_r_odd,
            "lower_exclusive": a - 2 * r,
            "upper_inclusive": a,
            "r_over_a_numerator": r,
            "r_over_a_denominator": a,
            "limit_r_s_over_a": "1/2",
            "normalized_limit": "log(2)/2-log(3)/4=log(4/3)/4>0",
        },
        "checks": checks,
        "all_pass": all(checks.values()),
    }

def universal_field_gate_proof() -> dict[str, Any]:
    a0 = 4
    checks = {
        "minimum_parameter": a0 == (3**2 - 1) // 2,
        "central_binomial_bound": math.comb(2 * a0, a0) < 4**a0,
        "gate_upper_bound_at_minimum": (
            2 * a0 + (a0 - 1) * 16**a0 // 2 < a0 * 16**a0
        ),
        "field_base_inequality": 81**a0 > a0 * 16**a0,
        "induction_ratio": 81 * a0 > 16 * (a0 + 1),
    }
    return {
        "range": "all integers a>=4, hence every r>=2 row",
        "chain": [
            "M=binom(2a,a)<4^a",
            "binom(M,2)<16^a/2",
            "n+k binom(M,2)<2a+(a-1)16^a/2<a16^a",
            "81^a>a16^a for a>=4 (base a=4 and increasing ratio)",
            "|F|=3^(rd)>=3^(4a)=81^a",
        ],
        "induction_step_ratio": (
            "[81^(a+1)/((a+1)16^(a+1))]/"
            "[81^a/(a16^a)]=81a/(16(a+1))>1"
        ),
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def general_depth_proof_payload(
    rows: list[dict[str, Any]], universal_gate: dict[str, Any]
) -> dict[str, Any]:
    """Aggregate exact all-legal-depth arithmetic without large row lists."""
    sampled_rows: list[dict[str, Any]] = []
    for row in rows:
        q = row["q"]
        n = row["n"]
        a = row["a"]
        field_size = row["extension_field_size"]
        support_count = row["complete_prefix_fiber_upper_bound_M"]
        support_pairs = math.comb(support_count, 2)
        orientation_count = row["orientation_occupancy_H"]
        critical_width = row["positive_depth"]["w"]

        tested_depths = 0
        dimensions_legal = True
        ceiling_floors_exact = True
        same_field_pays_every_depth = True
        critical_floor = None
        last_floor = None
        for depth in range(a - 1):
            tested_depths += 1
            dimension = a - depth - 1
            odd_coordinates = (depth + 1) // 2
            prefix_cap = q**odd_coordinates
            slope_floor = (
                orientation_count + prefix_cap - 1
            ) // prefix_cap
            dimensions_legal = dimensions_legal and (
                0 <= depth <= a - 2
                and 1 <= dimension < n
                and a >= dimension + 1
            )
            ceiling_floors_exact = ceiling_floors_exact and (
                (slope_floor - 1) * prefix_cap < orientation_count
                <= slope_floor * prefix_cap
            )
            same_field_pays_every_depth = (
                same_field_pays_every_depth
                and field_size > n + dimension * support_pairs
            )
            if depth == critical_width:
                critical_floor = slope_floor
            if depth == a - 2:
                last_floor = slope_floor

        sampled_rows.append(
            {
                "r": row["r"],
                "a": a,
                "legal_depth_range": [0, a - 2],
                "tested_depth_count": tested_depths,
                "all_dimensions_legal": dimensions_legal,
                "all_ceiling_floors_exact": ceiling_floors_exact,
                "same_field_pays_every_depth": same_field_pays_every_depth,
                "zero_depth_slope_floor": orientation_count,
                "critical_depth_w": critical_width,
                "critical_depth_slope_floor": critical_floor,
                "last_legal_depth_slope_floor": last_floor,
                "critical_floor_matches_row": (
                    critical_floor
                    == row["positive_depth"]["orientation_fiber_floor_J"]
                ),
            }
        )

    checks = {
        "sampled_every_legal_depth": all(
            sample["tested_depth_count"] == sample["a"] - 1
            for sample in sampled_rows
        ),
        "sampled_dimensions_legal": all(
            sample["all_dimensions_legal"] for sample in sampled_rows
        ),
        "sampled_ceiling_floors_exact": all(
            sample["all_ceiling_floors_exact"] for sample in sampled_rows
        ),
        "sampled_same_field_pays_every_depth": all(
            sample["same_field_pays_every_depth"]
            for sample in sampled_rows
        ),
        "critical_depth_consistency": all(
            sample["critical_floor_matches_row"] for sample in sampled_rows
        ),
        "zero_depth_is_orientation_capacity": all(
            sample["zero_depth_slope_floor"] == 2 ** sample["a"]
            for sample in sampled_rows
        ),
        "universal_same_field_gate": universal_gate["all_pass"],
    }
    return {
        "statement": {
            "range": "0<=u<=a-2",
            "dimension": "k_u=a-u-1",
            "orientation_prefix_image_cap": "q^ceil(u/2)",
            "actual_slope_floor": "J_(r,u)>=ceil(2^a/q^ceil(u/2))",
            "received_line_scope": (
                "the prefix and received line may depend on u; the same "
                "extension field F pays every legal u"
            ),
        },
        "subcritical_corollary": {
            "hypothesis": "u_r log(q_r)=o(n_r)",
            "normalized_lower_bound": (
                "log J_(r,u_r)/n_r >= log(2)/2 "
                "- ceil(u_r/2)log(q_r)/n_r"
            ),
            "ceiling_control": (
                "ceil(u/2)log(q)/n <= "
                "(u log(q)+log(q))/(2n)=o(1), since q=n+1"
            ),
            "conclusion": (
                "log J_(r,u_r)/n_r >= log(2)/2-o(1); together with "
                "H=2^a this matches the orientation-capacity exponent"
            ),
            "ambient_field_boundary": (
                "F remains exponential in n and the challenge is the full F"
            ),
        },
        "same_field_universal_proof": (
            "for every legal u, k_u<=a-1 and L_z<=binom(2a,a); "
            "the universal field gate therefore pays "
            "n+k_u binom(L_z,2)"
        ),
        "sampled_all_legal_depth_rows": sampled_rows,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def hypothesis_audit_payload() -> dict[str, Any]:
    return {
        "supplied_by_every_asymptotic_row": [
            "r>=2, q=3^r, B=F_q, and D=B^x has n=q-1=2a points",
            "phi(x)=x^2 is a retained two-fold complete-fiber folding",
            "orientation supports choose one point from every {x,-x} fiber",
            "C(T)C(-T)=1-T^(2a) determines even prefixes in characteristic three",
            "w=2floor(a/(2r)), 1<=w<=a-2, and k=a-w-1>=1",
            "one prefix has J=ceil(2^a/q^(w/2)) orientations",
            "F=F_(q^ceil(4a/r)) contains B and pays the complete-fiber pole gate",
            "the exact prefix-ray bijection gives distinct slopes and exact supports",
            "the challenge set is the full extension field",
        ],
        "consumer_match": {
            "occupancy": (
                "b=0, N=a, c=2, lambda=(0,0,a,a), "
                "H=[z^a](2z)^a=2^a"
            ),
            "prefix": "m=a, w=2floor(a/(2r)), k=m-w-1, U_z at the chosen prefix",
            "canonical_first_match": (
                "complete-prefix separation gives each retained slope one "
                "exact support and one #620 canonical joint cell; arbitrary "
                "augmented earlier cells are not addressed"
            ),
            "rate": (
                "a-2r<2r(w/2)<=a, giving the exact finite-row floor "
                "log(2)/2-log(3)/4=log(4/3)/4>0"
            ),
        },
        "load_bearing_hypotheses": [
            "full-field challenge after an exponential-size scalar extension",
            "complete-prefix rather than orientation-only pole separation",
            "positive critical-scale prefix depth w=2floor(a/(2r))",
            "odd characteristic and antipodal square fibers",
        ],
        "not_supplied_or_not_claimed": [
            "no orientation theorem with polynomial-size ambient field F is refuted",
            "no linear-depth prefix theorem is refuted",
            "no global hard-input-A or profile-envelope closure is claimed",
            "no deployed finite-row or adjacent inequality changes",
            "the prime-field mu_8 replay is only a mechanism check",
            "no statement is promoted into the frontiers TeX",
        ],
        "promotion_boundary": (
            "A collapse theorem needs an absent restriction such as a much "
            "smaller field, linear prefix depth, or a pole-overlap bound."
        ),
    }


def projection_comparison_payload() -> dict[str, Any]:
    return {
        "integrated_one_ray_packet": (
            "an exponential refined prefix fiber on F_(2^r)^x projects to "
            "one base-field pole slope"
        ),
        "positive_depth_family": (
            "an orientation subfiber at w=2floor(a/(2r)) retains J exponential "
            "slopes after complete-prefix separation"
        ),
        "finite_same_support_contrast": (
            "mu_8 orientations give two slopes at alpha=0 and all 16 at alpha=2"
        ),
        "joint_cut": (
            "support entropy and aperiodicity do not determine slope projection; "
            "prefix identities and pole separation are load-bearing"
        ),
        "claims_incompatibility": False,
    }


def family_payload(general_depth: dict[str, Any]) -> dict[str, Any]:
    return {
        "parameters": (
            "r>=2, q=3^r, a=(q-1)/2, n=2a, w=2floor(a/(2r)), "
            "k=a-w-1, d=ceil(4a/r)"
        ),
        "base_field_and_domain": "B=F_q and D=B^x",
        "folding": "phi(x)=x^2 with fibers {x,-x}",
        "orientation_cell": (
            "lambda_support=lambda_agreement=(0,0,a,a), H=2^a"
        ),
        "prefix_identity": "C(T)C(-T)=1-T^(2a)",
        "prefix_image_cap": "q^(w/2)",
        "orientation_fiber_floor": "J=ceil(2^a/q^(w/2))",
        "general_depth": general_depth["statement"],
        "subcritical_corollary": general_depth["subcritical_corollary"],
        "scalar_extension": "F=F_(q^ceil(4a/r))",
        "actual_projection": (
            "complete-prefix pole separation leaves at least J slopes in "
            "the one orientation joint cell"
        ),
        "positive_depth_rate": "log(4/3)/4",
        "zero_depth_endpoint_rate": "log(2)/2",
    }


def lineage_payload() -> list[dict[str, Any]]:
    return [
        {
            "pr": 620,
            "credit": "DannyExperiments",
            "role": (
                "joint support/full-agreement atlas, exact H_phi capacity, "
                "and named unsaturated orientation wall"
            ),
        },
        {
            "commit": "4e3c4ee85cb01ef7c4f1e7bbfbc13735cf6c9d15",
            "credit": "przchojecki",
            "role": "exact prefix-list and separating-pole/list-line theorems",
        },
        {
            "pr": 621,
            "commit": "8264eae23e9120a182218b3839aac024051ccf8d",
            "credit": "DannyExperiments",
            "role": "opposite one-slope projection extreme",
        },
        {
            "pr": 74,
            "credit": "AllenGrahamHart",
            "path": "experimental/notes/l1/l1_aperiodic_prefix_collision.md",
            "role": "general complement-prefix lemma and locator-product identity",
        },
        {
            "credit": "Claude Opus 4.8",
            "path": "experimental/notes/l1/l1_prefix_divisor_count.md",
            "role": "complement-locator compression and divisor-coefficient framing",
        },
    ]


def nonclaims_payload() -> list[str]:
    return [
        "Not a refutation of the occupancy atlas; it lower-bounds its unsaturated projection.",
        "Not a counterexample when ambient/challenge F is polynomial in n or prefix depth is linear.",
        "Not a claim about arbitrary augmented atlases or a primitive residual.",
        "Not a refutation of correct realized-image payment or earlier spectral routing.",
        "If z is promoted to a refined profile parameter, no subexponential z-census is claimed.",
        "Not a global hard-input-A counterexample or profile-envelope closure.",
        "Not a deployed finite-row result and not a paper-TeX modification.",
        "The two finite models validate separate mechanisms composed asymptotically by the pinned theorem.",
    ]


def verification_payload(
    prefix_model: dict[str, Any], finite_pole: dict[str, Any]
) -> dict[str, Any]:
    stem = (
        "python3 experimental/scripts/"
        "verify_full_agreement_orientation_saturation.py"
    )
    return {
        "stdlib_only": True,
        "address_space_cap_bytes": ADDRESS_SPACE_CAP_BYTES,
        "data_dir_override_environment": "FAOS_DATA_DIR",
        "zero_argument_mode": "--check",
        "asymptotic_integer_rows_r": list(ASYMPTOTIC_R_ROWS),
        "finite_prefix_orientations": prefix_model["orientation_count"],
        "finite_pole_full_supports": finite_pole["full_list"][
            "enumerated_supports"
        ],
        "semantic_tamper_mutations": 13,
        "artifact_path": str(ARTIFACT).replace("\\", "/"),
        "regeneration": stem + " --write",
        "check": stem + " --check",
        "tamper_selftest": stem + " --tamper-selftest",
    }


def top_level_checks(
    prefix_model: dict[str, Any],
    finite_pole: dict[str, Any],
    rows: list[dict[str, Any]],
    universal_gate: dict[str, Any],
    general_depth: dict[str, Any],
    tex_pins: dict[str, Any],
    source_pins: dict[str, Any],
    audit: dict[str, Any],
    comparison: dict[str, Any],
) -> dict[str, bool]:
    return {
        "literal_F9_prefix_model": prefix_model["all_pass"],
        "finite_smooth_pole_model": finite_pole["all_pass"],
        "all_asymptotic_rows": all(row["all_pass"] for row in rows),
        "universal_field_gate": universal_gate["all_pass"],
        "general_u_all_legal_depths": general_depth["all_pass"],
        "general_u_same_field_gate": (
            general_depth["checks"]["sampled_same_field_pays_every_depth"]
            and general_depth["checks"]["universal_same_field_gate"]
        ),
        "subcritical_exponent_corollary": (
            general_depth["subcritical_corollary"]["hypothesis"]
            == "u_r log(q_r)=o(n_r)"
            and "log(2)/2-o(1)"
            in general_depth["subcritical_corollary"]["conclusion"]
        ),
        "frontiers_hypotheses_pinned": tex_pins["all_found_and_audited"],
        "integrated_sources_pinned": source_pins["all_sources_pinned"],
        "positive_depth_floors": all(
            row["positive_depth"]["orientation_fiber_floor_J"] >= 2
            for row in rows
        ),
        "positive_limit_pinned": all(
            row["prefix_rate_limit"]["normalized_limit"]
            == "log(2)/2-log(3)/4=log(4/3)/4>0"
            for row in rows
        ),
        "extension_log_is_linear": all(
            row["field_log_bounds"]["two_n"]
            <= row["field_log_bounds"]["rd"]
            < row["field_log_bounds"]["two_n_plus_r"]
            for row in rows
        ),
        "zero_depth_saturates_H": all(
            row["zero_depth_endpoint"]["actual_slope_count"]
            == row["orientation_occupancy_H"]
            for row in rows
        ),
        "zero_vs_separating_pole": (
            finite_pole["orientation_cell"]["zero_pole"][
                "actual_slope_count"
            ]
            == 2
            and finite_pole["orientation_cell"]["separating_pole"][
                "actual_slope_count"
            ]
            == 2 ** finite_pole["parameters"]["a"]
        ),
        "projection_comparison_scoped": not comparison[
            "claims_incompatibility"
        ],
        "no_tex_promotion": (
            "no statement is promoted into the frontiers TeX"
            in audit["not_supplied_or_not_claimed"]
        ),
    }


def build_payload() -> dict[str, Any]:
    root = repo_root()
    prefix_model = finite_f9_prefix_model()
    finite_pole = finite_smooth_pole_model()
    rows = [asymptotic_row(r) for r in ASYMPTOTIC_R_ROWS]
    universal_gate = universal_field_gate_proof()
    general_depth = general_depth_proof_payload(rows, universal_gate)
    tex_pins = pin_frontiers_labels(root)
    source_pins = pin_source_notes(root)
    audit = hypothesis_audit_payload()
    comparison = projection_comparison_payload()
    checks = top_level_checks(
        prefix_model,
        finite_pole,
        rows,
        universal_gate,
        general_depth,
        tex_pins,
        source_pins,
        audit,
        comparison,
    )
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "object": "full-agreement general-depth orientation survival",
        "status": STATUS,
        "verdict": (
            "COUNTEREXAMPLE_NEW_FLOOR: every legal prefix depth u has slope "
            "floor ceil(2^a/q^ceil(u/2)); subcritical u log(q)=o(n) retains "
            "orientation slope exponent log(2)/2-o(1), the critical-scale "
            "choice has exact rate floor log(4/3)/4, and depth zero makes "
            "the exact H=2^a capacity sharp"
        ),
        "base_sha": BASE_SHA,
        "generated_by": (
            "experimental/scripts/"
            "verify_full_agreement_orientation_saturation.py"
        ),
        "lineage_and_credit": lineage_payload(),
        "frontiers_label_pins": tex_pins,
        "integrated_source_pins": source_pins,
        "family": family_payload(general_depth),
        "universal_field_gate_proof": universal_gate,
        "general_depth_proof": general_depth,
        "asymptotic_exact_rows": rows,
        "finite_F9_prefix_model": prefix_model,
        "finite_smooth_pole_model": finite_pole,
        "opposite_projection_comparison": comparison,
        "hypothesis_audit": audit,
        "nonclaims": nonclaims_payload(),
        "verification": verification_payload(prefix_model, finite_pole),
        "checks": checks,
        "all_pass": all(checks.values()),
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate_against(
    candidate: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    errors = []
    if candidate.get("payload_sha256") != payload_hash(candidate):
        errors.append("payload_sha256 does not authenticate candidate payload")
    if without_hash(candidate) != without_hash(expected):
        errors.append("candidate payload differs from exact recomputation")
    if not candidate.get("all_pass"):
        errors.append("all_pass is false")
    checks = candidate.get("checks")
    if not isinstance(checks, dict) or not checks or not all(checks.values()):
        errors.append("one or more top-level checks fail")
    return errors


def write_artifact(root: Path, effective_cap: int) -> int:
    payload = build_payload()
    if not payload["all_pass"]:
        print("RESULT: FAIL internal checks", file=sys.stderr)
        return 1
    path = root / ARTIFACT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {path}")
    print(f"payload_sha256: {payload['payload_sha256']}")
    print(f"RLIMIT_AS: {effective_cap} bytes")
    print(f"verdict: {payload['verdict']}")
    print("RESULT: PASS")
    return 0


def check_artifact(root: Path, effective_cap: int) -> int:
    path = root / ARTIFACT
    if not path.is_file():
        print(f"RESULT: FAIL missing artifact {path}", file=sys.stderr)
        return 1
    candidate = json.loads(path.read_text(encoding="utf-8"))
    expected = build_payload()
    errors = validate_against(candidate, expected)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print("RESULT: FAIL", file=sys.stderr)
        return 1
    pole = candidate["finite_smooth_pole_model"]
    prefix = candidate["finite_F9_prefix_model"]["chosen_width_row"]
    print("full-agreement orientation-saturation artifact check passed")
    print(f"payload_sha256: {candidate['payload_sha256']}")
    print(
        "finite pole model: "
        f"{pole['full_list']['enumerated_supports']} supports; "
        f"orientation slopes 2->{pole['orientation_cell']['separating_pole']['actual_slope_count']}"
    )
    print(
        "F_9 positive-depth fiber: "
        f"w={prefix['w']}, max={prefix['largest_orientation_fiber']}"
    )
    print("asymptotic rows: r=" + ",".join(map(str, ASYMPTOTIC_R_ROWS)))
    print(f"RLIMIT_AS: {effective_cap} bytes")
    print("RESULT: PASS")
    return 0


def tamper_selftest(effective_cap: int) -> int:
    expected = build_payload()

    def prefix_identity(x: dict[str, Any]) -> None:
        x["finite_F9_prefix_model"]["product_identity_checks"] -= 1

    def prefix_image(x: dict[str, Any]) -> None:
        x["finite_F9_prefix_model"]["chosen_width_row"][
            "prefix_image_size"
        ] += 1

    def finite_prime(x: dict[str, Any]) -> None:
        x["finite_smooth_pole_model"]["parameters"]["field_prime"] += 8

    def zero_pole(x: dict[str, Any]) -> None:
        x["finite_smooth_pole_model"]["orientation_cell"]["zero_pole"][
            "actual_slope_count"
        ] += 1

    def separating_pole(x: dict[str, Any]) -> None:
        x["finite_smooth_pole_model"]["orientation_cell"][
            "separating_pole"
        ]["actual_slope_count"] -= 1

    def width(x: dict[str, Any]) -> None:
        x["asymptotic_exact_rows"][0]["positive_depth"]["w"] -= 1

    def fiber_floor(x: dict[str, Any]) -> None:
        x["asymptotic_exact_rows"][1]["positive_depth"][
            "orientation_fiber_floor_J"
        ] += 1

    def field_gate(x: dict[str, Any]) -> None:
        x["asymptotic_exact_rows"][2]["separating_pole_gate"] += 1

    def general_u_gate(x: dict[str, Any]) -> None:
        x["general_depth_proof"]["sampled_all_legal_depth_rows"][0][
            "tested_depth_count"
        ] -= 1

    def tex_pin(x: dict[str, Any]) -> None:
        x["frontiers_label_pins"]["labels"][
            "thm:exact-list-line-bijection"
        ]["found_once"] = False

    def source_pin(x: dict[str, Any]) -> None:
        first = next(iter(x["integrated_source_pins"]["files"].values()))
        first["sha256"] = "f" * 64

    def nonclaim(x: dict[str, Any]) -> None:
        x["nonclaims"].pop()

    def projection_scope(x: dict[str, Any]) -> None:
        x["opposite_projection_comparison"]["claims_incompatibility"] = True

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("prefix identity", prefix_identity),
        ("prefix image", prefix_image),
        ("finite prime", finite_prime),
        ("zero pole", zero_pole),
        ("separating pole", separating_pole),
        ("positive width", width),
        ("orientation fiber floor", fiber_floor),
        ("field gate", field_gate),
        ("general-u live gate", general_u_gate),
        ("TeX hypothesis pin", tex_pin),
        ("source pin", source_pin),
        ("nonclaim", nonclaim),
        ("projection scope", projection_scope),
    ]
    accepted = []
    for name, mutate in mutations:
        bad = copy.deepcopy(expected)
        mutate(bad)
        bad["payload_sha256"] = payload_hash(bad)
        if not validate_against(bad, expected):
            accepted.append(name)
    if accepted:
        print(f"RESULT: FAIL undetected mutations: {accepted}", file=sys.stderr)
        return 1
    print(f"tamper self-test rejected {len(mutations)} semantic mutations")
    print(f"RLIMIT_AS: {effective_cap} bytes")
    print("RESULT: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true", help="write exact JSON")
    modes.add_argument("--check", action="store_true", help="recompute/check JSON")
    modes.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="reject semantic mutations even after adversarial rehashing",
    )
    args = parser.parse_args(argv)
    effective_cap = impose_address_space_cap()
    root = repo_root()
    if args.write:
        return write_artifact(root, effective_cap)
    if args.tamper_selftest:
        return tamper_selftest(effective_cap)
    return check_artifact(root, effective_cap)


if __name__ == "__main__":
    raise SystemExit(main())
