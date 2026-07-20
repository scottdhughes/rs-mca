#!/usr/bin/env sage
"""Independent Sage replay for the M31 shortened-flat architecture wall."""

from itertools import combinations, product


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_projective(values, field):
    vector_values = list(values)
    first = next((value for value in vector_values if value != 0), None)
    if first is None:
        raise VerificationError("zero vector has no projective class")
    return tuple(value / first for value in vector_values)


def exact_m31_arithmetic():
    p = 2^31 - 1
    n = 2^21
    k = 2^20
    agreement = 1116023
    sigma = agreement - k
    radius = n - agreement
    budget = p^4 // 2^100
    forbidden = budget + 1

    require(is_prime(p), "M31 prime")
    require(n == 2*k, "n=2K")
    require(sigma == 67447, "sigma")
    require(radius == 981129, "radius")
    require(radius < k + 1, "MDS uniqueness gate")
    require(budget == 16777215, "budget")
    require(forbidden == 2^24, "forbidden size")
    require((p + 1) % n == 0 and (p + 1)//n == 1024, "circle divisor")
    require((p - 1) % n != 0, "not multiplicative subgroup")

    degree = k-1
    berlekamp_welch_agreement = (n+degree+2)//2
    require(berlekamp_welch_agreement == 1572864,
            "Berlekamp-Welch agreement threshold")
    require(berlekamp_welch_agreement-agreement == 456841,
            "Berlekamp-Welch deficit")
    johnson_radicand = n*degree
    johnson_floor = 1482909
    require(johnson_floor^2 < johnson_radicand < (johnson_floor+1)^2,
            "Johnson exact square-root bracket")
    johnson_max_errors = n-(johnson_floor+1)
    require(johnson_max_errors == 614242, "Johnson integer error radius")
    require(radius-johnson_max_errors == 366887,
            "deployed excess over Johnson")
    require(2*(sigma+1) == 134896, "required support distance")
    require(2*67584 == 135168 > 2*(sigma+1),
            "countermodel support distance")

    lambda_floor = floor((QQ(3)/2)^100)
    require(lambda_floor == 406561177535215237, "lambda lower floor")
    require(lambda_floor-forbidden == 406561177518438021,
            "lambda margin")

    rho = QQ(sigma)/k
    x = QQ(n*k)/(p*sigma)
    y = QQ(n)/p
    positive_gap = (1-QQ(1)/p)*(1-y) - (rho/(1-x)+QQ(1)/p)
    negative_gap = (1-y) - (p*rho^8/(1-x)+y^7)
    require(positive_gap > 0, "positive shell gap")
    require(
        positive_gap.numerator()
        == 644050175112195590794125999209377544529,
        "positive shell gap numerator",
    )
    require(
        positive_gap.denominator()
        == 689775867500360194840796213214826201088,
        "positive shell gap denominator",
    )
    require(negative_gap > 0, "negative shell gap")
    require(
        negative_gap.numerator()
        == 15810002823743438754074664582119190973939634949577947321057126025224259167096031283564636761328485464935241283881354308999057975,
        "negative shell gap numerator",
    )
    require(
        negative_gap.denominator()
        == 43909320451064500807291848504517262791994420488823585673489953989734191694632389017761304498854399745203004211946306304544342016,
        "negative shell gap denominator",
    )
    low_gate_1 = p*sigma-100*k*(k+9)
    low_gate_2 = p*(sigma-8)-100*k*(k+9)
    require(low_gate_1 == 34889223043209 > 0, "first low-shell gate")
    require(low_gate_2 == 34872043174033 > 0, "later low-shell gate")

    r2 = QQ(k*(k-1)) / (
        sigma*((sigma-1)+(k+2)*(k-sigma))
    )
    require(
        r2 == QQ(45812940800)/QQ(2891200952995149),
        "shadow ratio",
    )
    require(floor(r2*(QQ(3)/2)^100) == 6442223650591, "shadow floor")
    require(floor((1-r2)*(QQ(3)/2)^100) == 406554735311564645,
            "endpoint cut")

    simplex_length = 2^12-1
    simplex_distance = 2^11
    repeated_length = 33*simplex_length
    repeated_distance = 33*simplex_distance
    binary_length = 2*repeated_length + 710859
    binary_dimension = 24
    binary_distance = repeated_distance
    require(binary_length == radius, "binary length")
    require(binary_distance == 67584, "binary distance")
    require(binary_distance >= sigma+1, "binary distance gate")
    require(2^binary_dimension == forbidden, "binary exact forbidden size")
    require(agreement-binary_distance == k-137, "intersection cap")
    require(n-2*binary_length == 134894, "pair embedding reserve")
    require(p-k-1 == 2146435070, "full-support line points")
    simplex_nonzero = 2^12-1
    weight_distribution = {
        0: 1,
        67584: 2*simplex_nonzero,
        135168: simplex_nonzero^2,
    }
    require(weight_distribution[67584] == 8190, "middle weight count")
    require(weight_distribution[135168] == 16769025, "top weight count")
    require(sum(weight_distribution.values()) == forbidden,
            "weight-distribution mass")

    projective_functionals = (p^4-1)//(p-1)
    killed_functionals = (p^3-1)//(p-1)
    gap = agreement-k+1
    descent_margin = gap*projective_functionals - forbidden*radius*killed_functionals
    require(
        descent_margin == 592061458020761914489814638395392,
        "scalar descent margin",
    )
    return {
        "p": p,
        "n": n,
        "k": k,
        "agreement": agreement,
        "sigma": sigma,
        "radius": radius,
        "budget": budget,
        "forbidden": forbidden,
        "lambda_margin": lambda_floor-forbidden,
        "low_gate_1": low_gate_1,
        "low_gate_2": low_gate_2,
        "bw_deficit": berlekamp_welch_agreement-agreement,
        "johnson_excess": radius-johnson_max_errors,
    }


def flat_syndrome_toy():
    F = GF(7)
    domain = [F(i) for i in range(6)]
    n = len(domain)
    dimension = 3
    radius = 2
    generator = matrix(F, [[x^degree for x in domain]
                           for degree in range(dimension)])
    dual = generator.right_kernel()
    native_dual_matrix = matrix(F, dual.basis())
    dual_matrix = matrix(
        F,
        [[6, 3, 4, 1, 0, 0],
         [4, 1, 1, 0, 1, 0],
         [1, 1, 4, 0, 0, 1]],
    )
    dual_dimension = n-dimension
    require(dual.dimension() == dual_dimension == 3, "dual dimension")
    require(generator*dual_matrix.transpose() == 0, "dual orthogonality")
    require(native_dual_matrix.row_space() == dual_matrix.row_space(),
            "pinned syndrome basis spans native dual")

    def syndrome(error):
        error_vector = vector(F, error)
        return tuple(error_vector.dot_product(row) for row in dual_matrix.rows())

    def shortening_coefficients(excluded):
        if len(excluded) == 0:
            constraints = matrix(F, 0, dual_dimension)
        else:
            constraints = matrix(
                F,
                [[dual_matrix[row, coordinate]
                  for row in range(dual_dimension)]
                 for coordinate in excluded],
            )
        return constraints.right_kernel()

    def contained(functional, subspace):
        functional_vector = vector(F, functional)
        return all(functional_vector.dot_product(row) == 0
                   for row in subspace.basis())

    def flat_count(functional):
        total = 0
        for size in range(radius+1):
            for excluded in combinations(range(n), size):
                flat = shortening_coefficients(excluded)
                if not contained(functional, flat):
                    continue
                exact = True
                for coordinate in excluded:
                    smaller = tuple(x for x in excluded if x != coordinate)
                    if contained(functional, shortening_coefficients(smaller)):
                        exact = False
                        break
                if exact:
                    total += 1
        return total

    errors = []
    counts = {}
    for size in range(radius+1):
        for support in combinations(range(n), size):
            for values in product([F(i) for i in range(1, 7)], repeat=size):
                error = [F(0)]*n
                for coordinate, value in zip(support, values):
                    error[coordinate] = value
                error_tuple = tuple(error)
                key = syndrome(error_tuple)
                counts[key] = counts.get(key, 0) + 1
                errors.append(error_tuple)
    require(len(errors) == 577, "error census")
    left_error = (F(1), F(1), F(0), F(0), F(0), F(0))
    right_error = (F(0), F(0), F(4), F(0), F(1), F(0))
    require(syndrome(left_error) == (F(2), F(5), F(2)),
            "left scope-counterexample syndrome")
    require(syndrome(right_error) == syndrome(left_error),
            "same-syndrome scope counterexample")
    left_support_sum = sum(domain[index] for index, value in enumerate(left_error)
                           if value != 0)
    right_support_sum = sum(domain[index] for index, value in enumerate(right_error)
                            if value != 0)
    require(left_support_sum == F(1) and right_support_sum == F(6),
            "distinct support power sums")

    for entries in product(list(F), repeat=dual_dimension):
        functional = tuple(entries)
        require(flat_count(functional) == counts.get(functional, 0),
                "flat/error equality")
        if any(entry != 0 for entry in functional):
            representative = canonical_projective(functional, F)
            require(counts.get(functional, 0) == counts.get(representative, 0),
                    "projective scaling")
    require(counts.get((F(0),)*dual_dimension, 0) == 1,
            "zero syndrome list")

    weights = []
    for x in domain:
        denominator = prod(x-z for z in domain if z != x)
        weights.append(1/denominator)
    grs_dual = matrix(
        F,
        [[weight*x^degree for x, weight in zip(domain, weights)]
         for degree in range(dual_dimension)],
    )
    require(grs_dual.row_space() == dual_matrix.row_space(),
            "weighted GRS dual")

    R = PolynomialRing(F, "X")
    X = R.gen()
    shift_checks = 0
    for size in range(radius+1):
        for excluded in combinations(range(n), size):
            locator = prod(X-domain[index] for index in excluded)
            shift_rows = [
                vector(F, [weight*(locator*X^shift)(x)
                           for x, weight in zip(domain, weights)])
                for shift in range(dual_dimension-size)
            ]
            coefficient_space = shortening_coefficients(excluded)
            ambient_rows = [row*dual_matrix for row in coefficient_space.basis()]
            left_space = matrix(F, shift_rows).row_space()
            right_space = matrix(F, ambient_rows).row_space()
            require(left_space == right_space, "locator/shortening equality")
            coefficients = locator.list()
            for error in errors:
                error_vector = vector(F, error)
                moments = [
                    sum(error[index]*weights[index]*x^degree
                        for index, x in enumerate(domain))
                    for degree in range(dual_dimension)
                ]
                for shift, row in enumerate(shift_rows):
                    recurrence = sum(coefficients[index]*moments[index+shift]
                                     for index in range(len(coefficients)))
                    require(error_vector.dot_product(row) == recurrence,
                            "syndrome recurrence")
                    shift_checks += 1

    return {
        "field": 7,
        "length": n,
        "dimension": dimension,
        "syndromes": 7^dual_dimension,
        "errors": len(errors),
        "shift_checks": shift_checks,
        "scope_counterexample": True,
    }


def line_law_toy():
    F = GF(3)
    dimension = 3
    raw = [tuple(F(value) for value in entries)
           for entries in product(range(3), repeat=dimension)
           if any(entries)]
    points = sorted(set(canonical_projective(vector_values, F)
                        for vector_values in raw))
    require(len(points) == 13, "PG(2,3) point count")
    lines = set()
    for left, right in combinations(points, 2):
        span = frozenset(
            canonical_projective(
                tuple(a*x+b*y for x, y in zip(left, right)), F
            )
            for a, b in product(list(F), repeat=2)
            if a != 0 or b != 0
        )
        if len(span) == 4:
            lines.add(span)
    require(len(lines) == 13, "PG(2,3) line count")
    hyperplanes = {
        frozenset(point for point in points
                  if sum(a*x for a, x in zip(functional, point)) == 0)
        for functional in points
    }
    feasible = set()
    for chosen in combinations(points, 4):
        selected = frozenset(chosen)
        if all(len(selected.intersection(line)) in (1, 4) for line in lines):
            feasible.add(selected)
    require(feasible == hyperplanes, "one-or-all line characterization")
    return {"points": len(points), "lines": len(lines),
            "candidates": binomial(13, 4), "hyperplanes": len(hyperplanes)}


def local_line_completion_toy():
    F = GF(11)
    n = 8
    dimension = 4
    domain = [F(i) for i in range(n)]
    block = frozenset(range(6))
    generator = matrix(
        F,
        [[x^degree for x in domain] for degree in range(dimension)],
    )
    dual_matrix = matrix(F, generator.right_kernel().basis())
    require(dual_matrix.nrows() == dimension, "local dual dimension")

    raw = [
        tuple(F(value) for value in entries)
        for entries in product(range(11), repeat=dimension)
        if any(entries)
    ]
    points = sorted(set(canonical_projective(entries, F) for entries in raw))
    require(len(points) == (11^dimension-1)//10, "local point count")
    supports = {}
    for point in points:
        ambient = vector(F, point)*dual_matrix
        supports[point] = frozenset(
            index for index, value in enumerate(ambient) if value != 0
        )

    selected = {
        point for point in points
        if len(supports[point]) == dimension+1 and supports[point] <= block
    }
    state_counts = {0: 0, 1: 0, dimension+2: 0}
    shortened_lines = []
    for support_tuple in combinations(range(n), dimension+2):
        support = frozenset(support_tuple)
        line = [point for point in points if supports[point] <= support]
        require(len(line) == 12, "local shortened-line cardinality")
        shortened_lines.append(line)
        state = sum(
            1 for point in line
            if len(supports[point]) == dimension+1 and point in selected
        )
        require(state in state_counts, "local facet state")
        state_counts[state] += 1
        full_support = [point for point in line if supports[point] == support]
        require(len(full_support) == 11-dimension-1,
                "local full-support point count")
        if state == 0:
            selected.add(full_support[0])
        elif state == dimension+2:
            selected.update(full_support)

    bad_lines = sum(
        1 for line in shortened_lines
        if sum(point in selected for point in line) not in (1, 12)
    )
    require(state_counts == {0: 15, 1: 12, 6: 1},
            "local state census")
    require(bad_lines == 0, "local global-completion consistency")
    return {
        "field": 11,
        "length": n,
        "dimension": dimension,
        "lines": len(shortened_lines),
        "state_zero": state_counts[0],
        "state_one": state_counts[1],
        "state_all": state_counts[dimension+2],
        "bad_lines": bad_lines,
    }


def main():
    deployed = exact_m31_arithmetic()
    flat = flat_syndrome_toy()
    lines = line_law_toy()
    local = local_line_completion_toy()
    print("object: independent M31 shortened-flat Sage replay")
    print("status: exact bridge PASS / global row OPEN")
    print(
        "deployed: p={p} n={n} K={k} a={agreement} sigma={sigma} "
        "radius={radius} B*={budget} forbidden={forbidden}".format(**deployed)
    )
    print(
        "external-route arithmetic: BW_deficit={bw_deficit} "
        "Johnson_error_excess={johnson_excess} PASS".format(**deployed)
    )
    print(
        "scalar gates: lambda_margin={lambda_margin} "
        "low=({low_gate_1},{low_gate_2}) PASS".format(**deployed)
    )
    print(
        "flat/syndrome toy: GF({field}) [{length},{dimension}] "
        "syndromes={syndromes} errors={errors} shift_checks={shift_checks} PASS".format(
            **flat
        )
    )
    print(
        "line-law toy: points={points} lines={lines} candidates={candidates} "
        "hyperplanes={hyperplanes} PASS".format(**lines)
    )
    print(
        "local-line semantic toy: GF({field}) [{length},{dimension}] "
        "lines={lines} states=({state_zero},{state_one},{state_all}) "
        "bad={bad_lines} PASS".format(**local)
    )
    print("global cross-support line closure: REQUIRED / UNPROVED")
    print("checks: {} PASS".format(CHECKS))
    print("RESULT: PASS")


main()
