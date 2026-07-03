#!/usr/bin/env sage
"""Kernel extraction for the mixed_rank6 M1 a=327 low-rank template."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_kernel_extraction.json")


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    try:
        if hasattr(payload, "__float__"):
            return float(payload)
    except Exception:
        pass
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def exact_field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for _degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def row_basis(F, vectors, members):
    if len(members) <= 1:
        return []
    anchor = [F(value) for value in vectors[int(members[0]) - 1]]
    rows = []
    for witness in members[1:]:
        rows.append([F(value) - anchor[idx] for idx, value in enumerate(vectors[int(witness) - 1])])
    matrix = Matrix(F, rows)
    return [list(row) for row in matrix.row_space().basis()]


def build_coefficient_matrix(F, powers, coordinate_classes, template_vectors, variable_count):
    entries = {}
    row_index = 0
    m = variable_count // K
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        members = [int(value) for value in coord["members"]]
        for diff in row_basis(F, template_vectors, members):
            for block in range(m):
                if diff[block] == 0:
                    continue
                start = block * K
                for degree in range(K):
                    entries[(row_index, start + degree)] = (
                        entries.get((row_index, start + degree), F(0))
                        + diff[block] * powers[degree][pos]
                    )
            row_index += 1
    return Matrix(F, row_index, variable_count, entries, sparse=True)


def build_eval_sparse_matrix(F, H, coordinate_classes, template_vectors, m):
    entries = {}
    row_index = 0
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        members = [int(value) for value in coord["members"]]
        for diff in row_basis(F, template_vectors, members):
            for block in range(m):
                if diff[block] != 0:
                    entries[(row_index, block * N + pos)] = diff[block]
            row_index += 1
    for block in range(m):
        offset = block * N
        for frequency in range(K, N):
            for pos, point in enumerate(H):
                entries[(row_index, offset + pos)] = point ** (-frequency)
            row_index += 1
    return Matrix(F, row_index, m * N, entries, sparse=True)


def free_column_sets(variable_count, limit):
    candidates = [
        ("tail_free_columns", [variable_count - 3, variable_count - 2, variable_count - 1]),
        ("block_high_degree", [K - 1, 2 * K - 1, 3 * K - 1]),
        ("block_constants", [0, K, 2 * K]),
        ("last_block_tail", [5 * K + K - 3, 5 * K + K - 2, 5 * K + K - 1]),
    ]
    seed = 1729
    for idx in range(8):
        cols = []
        state = seed + 7919 * idx
        while len(cols) < 3:
            state = (1103515245 * state + 12345) % (2**31)
            col = state % variable_count
            if col not in cols:
                cols.append(col)
        candidates.append(("random_seeded_%d" % idx, sorted(cols)))
    return candidates[:limit]


def square_solve_trial(F, matrix, free_cols, free_values):
    free_set = set(int(col) for col in free_cols)
    pivot_cols = [col for col in range(matrix.ncols()) if col not in free_set]
    if len(pivot_cols) != matrix.nrows():
        raise ValueError("pivot column count does not match row count")
    submatrix = matrix.matrix_from_columns(pivot_cols)
    rhs = vector(F, [F(0) for _ in range(matrix.nrows())])
    for col, value in zip(free_cols, free_values):
        rhs -= value * matrix.column(int(col))
    solution = submatrix.solve_right(rhs)
    candidate = vector(F, [F(0) for _ in range(matrix.ncols())])
    for idx, col in enumerate(pivot_cols):
        candidate[col] = solution[idx]
    for col, value in zip(free_cols, free_values):
        candidate[int(col)] = value
    residual = matrix * candidate
    if any(value != 0 for value in residual):
        raise ValueError("constructed vector failed matrix residual check")
    return candidate


def component_values_from_coefficients(F, powers, vector_row, m):
    values = []
    for block in range(m):
        block_values = []
        start = block * K
        for pos in range(N):
            acc = F(0)
            for degree in range(K):
                acc += vector_row[start + degree] * powers[degree][pos]
            block_values.append(acc)
        values.append(block_values)
    return values


def coefficients_from_eval_values(F, H, eval_vector, m):
    coeffs = []
    inv_n = F(1) / F(N)
    for block in range(m):
        block_coeffs = []
        offset = block * N
        for degree in range(K):
            acc = F(0)
            for pos, point in enumerate(H):
                acc += eval_vector[offset + pos] * (point ** (-degree))
            block_coeffs.append(inv_n * acc)
        coeffs.extend(block_coeffs)
    return vector(F, coeffs)


def component_values_from_eval_vector(eval_vector, m):
    values = []
    for block in range(m):
        offset = block * N
        values.append([eval_vector[offset + pos] for pos in range(N)])
    return values


def raw_row_violations(F, component_values, row_specs):
    violations = 0
    for spec in row_specs:
        pos = int(spec["position"])
        diff = [F(value) for value in spec["template_difference"]]
        acc = F(0)
        for block, scalar in enumerate(diff):
            if scalar != 0:
                acc += scalar * component_values[block][pos]
        if acc != 0:
            violations += 1
    return violations


def codeword_coefficients(F, vector_row, template_vectors):
    m = len(template_vectors[0])
    codewords = []
    for witness in range(LIST_SIZE):
        coeffs = [F(0) for _ in range(K)]
        for block in range(m):
            scalar = F(template_vectors[witness][block])
            start = block * K
            for degree in range(K):
                coeffs[degree] += scalar * vector_row[start + degree]
        codewords.append(coeffs)
    return codewords


def evaluate_candidate(F, powers, vector_row, coordinate_classes, template_vectors):
    coeffs = codeword_coefficients(F, vector_row, template_vectors)
    values = []
    for witness in range(LIST_SIZE):
        witness_values = []
        for pos in range(N):
            acc = F(0)
            for degree in range(K):
                acc += coeffs[witness][degree] * powers[degree][pos]
            witness_values.append(acc)
        values.append(witness_values)
    r_values = []
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        anchor = min(int(value) for value in coord["members"])
        r_values.append(values[anchor - 1][pos])
    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [hash_payload([str(value) for value in row]) for row in coeffs]
    return {
        "agreement_vector": agreements,
        "exact_max_min": min(agreements),
        "seven_distinct": len(set(codeword_hashes)) == LIST_SIZE,
        "received_word_hash": hash_payload([str(value) for value in r_values]),
        "codeword_hashes": codeword_hashes,
    }


def process_coeff_vector(F, powers, record, vector_row):
    proxy = record["proxy_candidate"]
    template_vectors = proxy["template_vectors"]
    m = int(proxy["template_dimension"])
    component_values = component_values_from_coefficients(F, powers, vector_row, m)
    violations = raw_row_violations(F, component_values, record["row_specs"])
    record["kernel_extraction"]["exact_vectors_constructed"] += 1
    record["kernel_extraction"]["raw_rows_checked"] = int(proxy["raw_selected_class_rows"])
    record["kernel_extraction"]["raw_row_violations"] = int(violations)
    if violations:
        record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_RAW_ROW_VIOLATION"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_KERNEL_RAW_ROW_VIOLATION / PARTIAL / EXPERIMENTAL"
        return False
    evaluated = evaluate_candidate(F, powers, vector_row, record["coordinate_classes"], template_vectors)
    if not evaluated["seven_distinct"]:
        record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_DEGENERATE"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_KERNEL_DEGENERATE / PARTIAL / EXPERIMENTAL"
        return False
    record["pair_projection_test"]["seven_distinct_vectors"] += 1
    if evaluated["exact_max_min"] < TARGET_AGREEMENT:
        record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_SUPPORT_LOSS"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_KERNEL_SUPPORT_LOSS / PARTIAL / EXPERIMENTAL"
        return False
    record["candidate"].update(
        {
            "constructed": True,
            "seven_distinct": True,
            "agreement_vector": evaluated["agreement_vector"],
            "received_word_hash": evaluated["received_word_hash"],
            "codeword_hashes": evaluated["codeword_hashes"],
        }
    )
    record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_EXACT_CANDIDATE"
    record["proof_status"] = "PROOF_RECORD / LOWRANK_KERNEL_EXACT_CANDIDATE / EXPERIMENTAL"
    return True


def run_square_strategy(F, powers, record, max_trials):
    proxy = record["proxy_candidate"]
    matrix = build_coefficient_matrix(
        F,
        powers,
        record["coordinate_classes"],
        proxy["template_vectors"],
        int(proxy["variable_count"]),
    )
    record["kernel_extraction"]["coefficient_matrix_shape"] = [int(matrix.nrows()), int(matrix.ncols())]
    alpha = F.multiplicative_generator()
    any_singular = False
    for label, free_cols in free_column_sets(matrix.ncols(), max_trials):
        record["kernel_extraction"]["square_solves_tested"] += 1
        trial = {"strategy": "square_free_column_solve", "label": label, "free_columns": free_cols, "status": None}
        record["kernel_extraction"]["trial_results"].append(trial)
        free_values = [F(1), alpha, alpha**2]
        try:
            vector_row = square_solve_trial(F, matrix, free_cols, free_values)
        except Exception as err:
            trial["status"] = "SINGULAR_OR_FAILED"
            trial["error"] = str(err)
            any_singular = True
            continue
        trial["status"] = "VECTOR_CONSTRUCTED"
        if process_coeff_vector(F, powers, record, vector_row):
            return True
    if any_singular and record["kernel_extraction"]["best_failure_mode"] is None:
        record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_SQUARE_SOLVE_SINGULAR"
        record["proof_status"] = "CANDIDATE / LOWRANK_KERNEL_SQUARE_SOLVE_SINGULAR / PARTIAL / EXPERIMENTAL"
    return False


def run_eval_sparse_strategy(F, H, powers, record, max_trials):
    proxy = record["proxy_candidate"]
    m = int(proxy["template_dimension"])
    matrix = build_eval_sparse_matrix(F, H, record["coordinate_classes"], proxy["template_vectors"], m)
    record["kernel_extraction"]["eval_sparse_matrix_shape"] = [int(matrix.nrows()), int(matrix.ncols())]
    alpha = F.multiplicative_generator()
    for label, free_cols in free_column_sets(matrix.ncols(), max_trials):
        record["kernel_extraction"]["eval_sparse_solves_tested"] += 1
        trial = {"strategy": "eval_sparse_solve", "label": label, "free_columns": free_cols, "status": None}
        record["kernel_extraction"]["trial_results"].append(trial)
        free_values = [F(1), alpha, alpha**2]
        try:
            eval_vector = square_solve_trial(F, matrix, free_cols, free_values)
        except Exception as err:
            trial["status"] = "SINGULAR_OR_FAILED"
            trial["error"] = str(err)
            continue
        trial["status"] = "VECTOR_CONSTRUCTED"
        coeff_vector = coefficients_from_eval_values(F, H, eval_vector, m)
        if process_coeff_vector(F, powers, record, coeff_vector):
            return True
    if record["kernel_extraction"]["best_failure_mode"] is None:
        record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_SQUARE_SOLVE_SINGULAR"
        record["proof_status"] = "CANDIDATE / LOWRANK_KERNEL_SQUARE_SOLVE_SINGULAR / PARTIAL / EXPERIMENTAL"
    return False


def audit(strategy="metadata", max_trials=1):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    _q, F, H = exact_field_context()
    powers = precompute_powers(F, H)
    if strategy in ("metadata", "square", "both"):
        if "square_free_column_solve" not in record["kernel_extraction"]["strategies_tested"]:
            record["kernel_extraction"]["strategies_tested"].append("square_free_column_solve")
        if strategy == "metadata":
            matrix = build_coefficient_matrix(
                F,
                powers,
                record["coordinate_classes"],
                record["proxy_candidate"]["template_vectors"],
                int(record["proxy_candidate"]["variable_count"]),
            )
            record["kernel_extraction"]["coefficient_matrix_shape"] = [int(matrix.nrows()), int(matrix.ncols())]
            return record
        if run_square_strategy(F, powers, record, max_trials):
            return record
    if strategy in ("eval-sparse", "both"):
        if "eval_sparse_solve" not in record["kernel_extraction"]["strategies_tested"]:
            record["kernel_extraction"]["strategies_tested"].append("eval_sparse_solve")
        run_eval_sparse_strategy(F, H, powers, record, max_trials)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strategy", choices=["metadata", "square", "eval-sparse", "both"], default="metadata")
    parser.add_argument("--max-trials", type=int, default=1)
    args = parser.parse_args()
    record = audit(strategy=args.strategy, max_trials=args.max_trials)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        kernel = record["kernel_extraction"]
        print("SAGE_AUDIT_M1_A327_LOWRANK_TEMPLATE_KERNEL_EXTRACTION_OK")
        print("strategies_tested: %s" % kernel["strategies_tested"])
        print("coefficient_matrix_shape: %s" % kernel["coefficient_matrix_shape"])
        print("eval_sparse_matrix_shape: %s" % kernel["eval_sparse_matrix_shape"])
        print("exact_vectors_constructed: %s" % kernel["exact_vectors_constructed"])
        print("best_failure_mode: %s" % kernel["best_failure_mode"])


if __name__ == "__main__":
    main()
