#!/usr/bin/env sage
"""Build and audit a Sage-native cache for the repaired M1 a=327 skeleton."""

from __future__ import annotations

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import sys
import time
from numbers import Integral
from pathlib import Path


TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
REPAIRED_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_repaired_skeleton_nondegenerate_split.sage")
SCALABLE_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_pair27_37_class_creation_scalable.sage")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_repaired_skeleton_sage_native_cache.py")
DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_sage_native_cache.json")
CACHE_BASENAME = Path("experimental/data/cache/m1_a327_repaired_skeleton_budget32_prepared_state")
CACHE_PATH = Path(str(CACHE_BASENAME) + ".sobj")


def load_python_module(path, module_name):
    script_dir = str(path.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_source_module(path, module_name):
    loader = importlib.machinery.SourceFileLoader(module_name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    module.Integer = Integer
    module.GF = GF
    module.Matrix = Matrix
    module.vector = vector
    return module


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


def hash_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def vector_hash(values):
    return hash_payload([str(value) for value in values])


def matrix_shape(matrix):
    return [int(matrix.nrows()), int(matrix.ncols())]


def build_cache_artifact():
    start = time.time()
    repaired = load_source_module(REPAIRED_AUDIT_PATH, "repaired_skeleton_cache_build_helpers")
    context = repaired.repaired_context()
    scalable = context["scalable"]
    residual = context["residual"]
    F = context["F"]
    base = context["base"]
    rows_pin, rhs_pin = scalable.pin_rows(residual, F, base["powers"], context["repaired_fixed_specs"])
    rows = base["rows"] + rows_pin
    rhs = base["rhs"] + rhs_pin
    independent_rows, independent_rhs, system_meta = context["codesign"].independent_system(F, residual, rows, rhs)
    A = Matrix(F, independent_rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    free_columns = [int(col) for col in range(residual.VARIABLE_COUNT) if int(col) not in set(pivots)]
    pivot_matrix = A.matrix_from_columns(pivots[: len(independent_rows)]) if len(pivots) >= len(independent_rows) else None
    if pivot_matrix is None:
        raise RuntimeError("base pivot matrix unavailable")
    artifact = {
        "cache_version": 1,
        "cache_type": "SAGE_NATIVE",
        "field": "GF(17^32)",
        "H_order": 512,
        "matrix": A,
        "rhs": vector(F, independent_rhs),
        "pivots": pivots,
        "free_columns": free_columns,
        "pivot_matrix": pivot_matrix,
        "pivot_inverse": pivot_matrix.inverse(),
        "base_vector": vector(F, context["repaired_base_vector"]),
        "H": list(base["powers"][1]),
        "fixed_specs": context["repaired_fixed_specs"],
        "base_row": context["repaired_base_row"],
        "system_meta": system_meta,
        "build_elapsed_seconds": float(round(float(time.time() - start), 3)),
    }
    CACHE_BASENAME.parent.mkdir(parents=True, exist_ok=True)
    save(artifact, str(CACHE_BASENAME), compress=False)
    if not CACHE_PATH.exists():
        raise RuntimeError("Sage save did not produce expected artifact: %s" % CACHE_PATH)
    return artifact, {
        "cache_path": str(CACHE_PATH),
        "sage_cache_hash": hash_file(CACHE_PATH),
        "build_elapsed_seconds": artifact["build_elapsed_seconds"],
    }


def load_cache_artifact():
    if not CACHE_PATH.exists():
        artifact, meta = build_cache_artifact()
        return artifact, meta
    artifact = load(str(CACHE_BASENAME))
    if len(artifact.get("H", [])) != 512:
        _, residual = load_eval_helpers()
        F = artifact["matrix"].base_ring()
        _, _, rebuilt_H = residual.field_context()
        artifact["H"] = [F(value) for value in rebuilt_H]
        save(artifact, str(CACHE_BASENAME), compress=False)
    if "pivot_inverse" not in artifact:
        artifact["pivot_inverse"] = artifact["pivot_matrix"].inverse()
        save(artifact, str(CACHE_BASENAME), compress=False)
    return artifact, {
        "cache_path": str(CACHE_PATH),
        "sage_cache_hash": hash_file(CACHE_PATH),
        "build_elapsed_seconds": None,
    }


def load_eval_helpers():
    scalable = load_source_module(SCALABLE_AUDIT_PATH, "scalable_for_sage_native_cache")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_for_sage_native_cache")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual_for_sage_native_cache")
    return scalable, residual


def one_row_append_vector(artifact, residual):
    F = artifact["matrix"].base_ring()
    A = artifact["matrix"]
    pivots = artifact["pivots"]
    pivot_inverse = artifact["pivot_inverse"]
    base_vector = list(artifact["base_vector"])
    spec = {"left": 4, "right": 1, "position": 87, "gamma": 1, "kind": "split_4_from_157_cache_append"}
    H = artifact.get("H", [])
    if len(H) != 512:
        _, _, rebuilt_H = residual.field_context()
        H = [F(value) for value in rebuilt_H]
    powers = residual.precompute_powers(F, H)
    row = residual.evaluation_row(F, powers, spec["left"], spec["right"], spec["position"])
    rhs = F(Integer(spec["gamma"]))
    current = sum(row[idx] * base_vector[idx] for idx in range(len(base_vector)))
    delta = rhs - current
    if delta == 0:
        return base_vector, spec, {"free_column_used": None, "append_delta": "0"}
    row_nonzero_free = [int(col) for col in artifact["free_columns"] if row[int(col)] != 0]
    candidate_free_columns = row_nonzero_free + [int(col) for col in artifact["free_columns"] if row[int(col)] == 0]
    for free_col in candidate_free_columns:
        col = A.column(int(free_col))
        sol = pivot_inverse * (-col)
        coeff = row[int(free_col)]
        for idx, pivot_col in enumerate(pivots[: A.nrows()]):
            coeff += row[int(pivot_col)] * sol[idx]
        if coeff == 0:
            continue
        scale = delta / coeff
        out = list(base_vector)
        out[int(free_col)] += scale
        for idx, pivot_col in enumerate(pivots[: A.nrows()]):
            out[int(pivot_col)] += scale * sol[idx]
        return out, spec, {
            "free_column_used": int(free_col),
            "append_delta": str(delta),
            "append_coefficient": str(coeff),
        }
    return None, spec, {"error": "no nonzero residual coefficient found"}


def evaluate_append(artifact):
    start = time.time()
    scalable, residual = load_eval_helpers()
    vector_value, spec, solve_meta = one_row_append_vector(artifact, residual)
    if vector_value is None:
        return {
            "run": True,
            "timeout": False,
            "status": "CACHE_PIVOT_REUSE_FAILS",
            "vector_constructed": False,
            "append_spec": spec,
            "solve_meta": solve_meta,
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    F = artifact["matrix"].base_ring()
    H = artifact.get("H", [])
    if len(H) != 512:
        _, _, rebuilt_H = residual.field_context()
        H = [F(value) for value in rebuilt_H]
    row = scalable.evaluate_with_failure(
        residual,
        F,
        residual.precompute_powers(F, H),
        vector_value,
        {
            "phase": "sage_native_cache_small_append",
            "append_spec": spec,
            **solve_meta,
        },
    )
    return {
        "run": True,
        "timeout": False,
        "status": "CACHE_SMALL_APPEND_PASS",
        "vector_constructed": True,
        "append_spec": spec,
        "free_column_used": solve_meta.get("free_column_used"),
        "capacity": row["capacity_upper_bound"],
        "pair_B_values": row["pair_B_values"],
        "collapse_pattern": row["degenerate_classes"],
        "six_class_dominance": row["six_class_dominance"],
        "distinct_codewords": row["distinct_codewords"],
        "exact_max_min": row.get("exact_max_min"),
        "elapsed_seconds": float(round(float(time.time() - start), 3)),
    }


def prepared_state_from_artifact(artifact, meta):
    A = artifact["matrix"]
    pivots = [int(col) for col in artifact["pivots"]]
    free_columns = [int(col) for col in artifact["free_columns"]]
    return {
        "cache_type": "SAGE_NATIVE",
        "matrix_shape": matrix_shape(A),
        "rank": len(pivots),
        "nullity": len(free_columns),
        "fixed_specs_count": len(artifact["fixed_specs"]),
        "pivot_columns_hash": hash_payload(pivots),
        "free_columns_hash": hash_payload(free_columns),
        "independent_rows_hash": hash_payload({"matrix_shape": matrix_shape(A), "rank": len(pivots), "sage_cache_hash": meta["sage_cache_hash"]}),
        "sage_cache_hash": meta["sage_cache_hash"],
        "sage_cache_path": meta["cache_path"],
        "base_vector_hash": vector_hash(artifact["base_vector"]),
        "base_value_class_hash": None,
        "build_elapsed_seconds": meta["build_elapsed_seconds"],
    }


def audit_record():
    scan = load_python_module(SCAN_PATH, "sage_native_cache_scan")
    artifact, meta = load_cache_artifact()
    prepared_state = prepared_state_from_artifact(artifact, meta)
    append_test = evaluate_append(artifact)
    return scan.build_record(prepared_state=prepared_state, append_test=append_test)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--build-cache", action="store_true")
    args = parser.parse_args()
    if args.build_cache:
        artifact, meta = build_cache_artifact()
        print(json.dumps(jsonable({"cache_path": meta["cache_path"], "sage_cache_hash": meta["sage_cache_hash"], "matrix_shape": matrix_shape(artifact["matrix"])}), sort_keys=True))
        return
    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_REPAIRED_SKELETON_SAGE_NATIVE_CACHE_OK")
        print("cache_type: %s" % record["prepared_state"]["cache_type"])
        print("append_status: %s" % record["append_test"]["status"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
