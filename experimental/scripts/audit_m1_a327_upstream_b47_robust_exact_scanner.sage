#!/usr/bin/env sage
"""Exact upstream B47-robust skeleton scanner over GF(17^32)."""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import sys
import time
from numbers import Integral
from pathlib import Path


TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT

SCAN_PATH = Path("experimental/scripts/scan_m1_a327_upstream_b47_robust_exact_scanner.py")
DATA_PATH = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json")
V2_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_compensated_repaired_skeleton_split_v2.sage")
NATIVE_CACHE_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_repaired_skeleton_sage_native_cache.sage")
REPAIRED_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_repaired_skeleton_nondegenerate_split.sage")

FAMILIES = [
    "alt_14_57",
    "alt_15_47",
    "alt_17_45",
    "alt_145_7",
    "b47_guard",
    "triple_237_b47_guard",
]
BUDGETS = [1, 2, 4, 8]
SPLIT_PROBE_FAMILIES = ["split_4_from_157", "split_14_vs_57", "split_1_from_457"]


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
    module.load = load
    module.save = save
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


def fragile_1457(degenerate_classes):
    return any(sorted(block) == [1, 4, 5, 7] for block in degenerate_classes or [])


def d2_split(degenerate_classes):
    return not any(1 in row and 2 in row for row in degenerate_classes)


def guard_margins(row):
    if row is None or row.get("pair_B_values") is None:
        return {"capacity": None, "B27": None, "B37": None, "B47": None, "B57": None}
    pairs = row["pair_B_values"]
    return {
        "capacity": row["capacity_upper_bound"] - TARGET_AGREEMENT,
        "B27": pairs[1] - PAIR_TARGET,
        "B37": pairs[2] - PAIR_TARGET,
        "B47": pairs[3] - PAIR_TARGET,
        "B57": pairs[4] - PAIR_TARGET,
    }


def robustness_score(row):
    margins = guard_margins(row)
    if any(value is None for value in margins.values()):
        return None
    return min(margins.values())


def classify_probe(row):
    if row is None or row.get("pair_B_values") is None:
        return "UPSTREAM_INCONSISTENT"
    if row["six_class_dominance"] > 0:
        return "UPSTREAM_COLLAPSE_RETURNS"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "UPSTREAM_CAPACITY_NOT_ROBUST"
    pairs = row["pair_B_values"]
    if pairs[1] < PAIR_TARGET or pairs[2] < PAIR_TARGET:
        return "UPSTREAM_PAIR27_37_NOT_ROBUST"
    if pairs[3] < PAIR_TARGET:
        return "UPSTREAM_B47_NOT_ROBUST"
    if pairs[4] < PAIR_TARGET:
        return "UPSTREAM_PAIR57_NOT_ROBUST"
    if fragile_1457(row["degenerate_classes"]):
        return "UPSTREAM_COLLAPSE_UNCHANGED"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "UPSTREAM_EXACT_CANDIDATE"
    if row.get("distinct_codewords") is True:
        return "UPSTREAM_LOW_RESCHEDULE"
    return "UPSTREAM_SPLIT_RESILIENT_SKELETON"


def vector_sort_key(result):
    probe = result.get("best_probe")
    score = result.get("best_robustness_score")
    pre = result.get("pre_split")
    pre_capacity = -1 if pre is None else pre.get("capacity_upper_bound", -1)
    exact_max = -1 if probe is None or probe.get("exact_max_min") is None else probe["exact_max_min"]
    return (
        result.get("failure_mode") == "UPSTREAM_EXACT_CANDIDATE",
        result.get("split_resilient") is True,
        -10**9 if score is None else score,
        pre_capacity,
        exact_max,
        result.get("pre_split_contains_fragile_1457") is False,
    )


def cases():
    out = []
    idx = 0
    for family in FAMILIES:
        for budget in BUDGETS:
            out.append({"case_index": idx, "candidate_family": family, "budget": int(budget)})
            idx += 1
    return out


def selected_cases(limit=None, case_index=None, case_range=None):
    selected = cases()
    if case_index is not None:
        idx = int(case_index)
        if idx < 0 or idx >= len(selected):
            raise ValueError("case index out of range: %s" % idx)
        return [selected[idx]]
    if case_range:
        left, right = case_range.split(":", 1)
        start = int(left) if left else 0
        stop = int(right) if right else len(selected)
        selected = selected[start:stop]
    if limit is not None:
        selected = selected[: int(limit)]
    return selected


def unique_positions(split_ledger, budget):
    positions = []
    seen = set()
    for row in split_ledger["candidate_split_rows"]:
        pos = int(row["coordinate"])
        if pos in seen:
            continue
        seen.add(pos)
        positions.append(pos)
        if len(positions) >= int(budget):
            break
    if len(positions) < int(budget):
        for pos in range(0, 512, 16):
            if pos not in seen:
                positions.append(pos)
                seen.add(pos)
            if len(positions) >= int(budget):
                break
    return positions[: int(budget)]


def equality_specs(position, pairs, kind):
    return [
        {"left": int(left), "right": int(right), "position": int(position), "gamma": 0, "kind": kind}
        for left, right in pairs
    ]


def upstream_specs(split_ledger, family, budget):
    positions = unique_positions(split_ledger, budget)
    specs = []
    for idx, pos in enumerate(positions):
        if family == "alt_14_57":
            specs.extend(equality_specs(pos, [(1, 4), (5, 7)], family))
            specs.append({"left": 1, "right": 5, "position": int(pos), "gamma": 1, "kind": family})
        elif family == "alt_15_47":
            specs.extend(equality_specs(pos, [(1, 5), (4, 7)], family))
            specs.append({"left": 1, "right": 4, "position": int(pos), "gamma": 1, "kind": family})
        elif family == "alt_17_45":
            specs.extend(equality_specs(pos, [(1, 7), (4, 5)], family))
            specs.append({"left": 1, "right": 4, "position": int(pos), "gamma": 1, "kind": family})
        elif family == "alt_145_7":
            specs.extend(equality_specs(pos, [(1, 4), (4, 5)], family))
            specs.append({"left": 1, "right": 7, "position": int(pos), "gamma": 1, "kind": family})
        elif family == "b47_guard":
            specs.extend(equality_specs(pos, [(4, 7), (1, 5)], family))
            if idx % 2 == 0:
                specs.append({"left": 1, "right": 4, "position": int(pos), "gamma": 1, "kind": family})
        elif family == "triple_237_b47_guard":
            specs.extend(equality_specs(pos, [(2, 7), (3, 7), (4, 7)], family))
            if idx % 2 == 0:
                specs.append({"left": 1, "right": 4, "position": int(pos), "gamma": 1, "kind": family})
        else:
            raise ValueError("unknown family %s" % family)
    return specs, positions


def evaluate(v2, residual, F, powers, vector_value, metadata):
    row = v2.evaluate_vector(residual, F, powers, vector_value, metadata)
    row["guard_margins"] = guard_margins(row)
    row["robustness_score"] = robustness_score(row)
    row["contains_fragile_1457_class"] = fragile_1457(row["degenerate_classes"])
    return row


def case_record(case, artifact, scalable, residual, repaired, v2, split_ledger, powers):
    start = time.time()
    F = artifact["matrix"].base_ring()
    specs, positions = upstream_specs(split_ledger, case["candidate_family"], case["budget"])
    vector_value, solve_meta = v2.solve_cached_append(artifact, scalable, residual, powers, specs)
    if vector_value is None:
        return {
            **case,
            "candidate_specs_count": len(specs),
            "candidate_positions": positions,
            "failure_mode": "UPSTREAM_INCONSISTENT",
            "solve_meta": solve_meta,
            "probe_results": [],
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }

    pre = evaluate(
        v2,
        residual,
        F,
        powers,
        vector_value,
        {
            **case,
            "phase": "upstream_b47_robust_exact_scanner_pre_split",
            "candidate_specs_count": len(specs),
            "candidate_positions": positions,
            **solve_meta,
        },
    )

    probes = []
    for split_family in SPLIT_PROBE_FAMILIES:
        split_specs, selected_split_rows = repaired.selected_split_specs(split_ledger, split_family, 1, 8)
        probe_value, probe_solve = v2.solve_cached_append(artifact, scalable, residual, powers, specs + split_specs)
        if probe_value is None:
            probes.append(
                {
                    "split_family": split_family,
                    "failure_mode": "UPSTREAM_INCONSISTENT",
                    "selected_split_rows": selected_split_rows,
                    "solve_meta": probe_solve,
                }
            )
            continue
        probe = evaluate(
            v2,
            residual,
            F,
            powers,
            probe_value,
            {
                **case,
                "phase": "upstream_b47_robust_exact_scanner_split_probe",
                "candidate_specs_count": len(specs),
                "candidate_positions": positions,
                "split_family": split_family,
                "split_specs": split_specs,
                "selected_split_rows": selected_split_rows,
                **probe_solve,
            },
        )
        probe["split_family"] = split_family
        probe["selected_split_rows"] = selected_split_rows
        probe["failure_mode"] = classify_probe(probe)
        probes.append(probe)

    scored = [probe for probe in probes if probe.get("robustness_score") is not None]
    best_probe = max(scored, key=lambda row: (row["robustness_score"], row.get("capacity_upper_bound", -1))) if scored else None
    split_resilient = any(probe.get("failure_mode") in {
        "UPSTREAM_SPLIT_RESILIENT_SKELETON",
        "UPSTREAM_LOW_RESCHEDULE",
        "UPSTREAM_EXACT_CANDIDATE",
    } for probe in probes)
    failure_mode = "UPSTREAM_INCONSISTENT"
    if best_probe is not None:
        failure_mode = classify_probe(best_probe)
    if split_resilient and failure_mode not in {"UPSTREAM_EXACT_CANDIDATE", "UPSTREAM_LOW_RESCHEDULE"}:
        failure_mode = "UPSTREAM_SPLIT_RESILIENT_SKELETON"

    return {
        **case,
        "candidate_specs_count": len(specs),
        "candidate_positions": positions,
        "pre_split": pre,
        "pre_split_contains_fragile_1457": pre["contains_fragile_1457_class"],
        "probe_results": probes,
        "split_resilient": split_resilient,
        "best_probe": best_probe,
        "best_robustness_score": None if best_probe is None else best_probe.get("robustness_score"),
        "failure_mode": failure_mode,
        "elapsed_seconds": float(round(float(time.time() - start), 3)),
    }


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def scanner_from_results(results):
    scan = load_python_module(SCAN_PATH, "upstream_b47_robust_exact_scanner_scan")
    best = sorted(results, key=vector_sort_key, reverse=True)[0] if results else None
    probe_vectors = [probe for result in results for probe in result.get("probe_results", []) if probe.get("pair_B_values") is not None]
    exact_scanner = {
        "systems_planned": len(cases()),
        "systems_tested": len(results),
        "timeouts": 0,
        "exact_vectors_constructed": sum(1 for result in results if result.get("pre_split") is not None),
        "split_probe_vectors": len(probe_vectors),
        "split_resilient_skeletons": sum(1 for result in results if result.get("split_resilient") is True),
        "candidate_families": FAMILIES,
        "budgets": BUDGETS,
        "split_probe_families": SPLIT_PROBE_FAMILIES,
        "best_pre_split_capacity": None if best is None or best.get("pre_split") is None else best["pre_split"].get("capacity_upper_bound"),
        "best_pre_split_pair_B_values": None if best is None or best.get("pre_split") is None else best["pre_split"].get("pair_B_values"),
        "best_probe_split_capacity": None if best is None or best.get("best_probe") is None else best["best_probe"].get("capacity_upper_bound"),
        "best_probe_split_pair_B_values": None if best is None or best.get("best_probe") is None else best["best_probe"].get("pair_B_values"),
        "best_robustness_score": None if best is None else best.get("best_robustness_score"),
        "best_collapse_pattern": None if best is None or best.get("best_probe") is None else best["best_probe"].get("degenerate_classes"),
        "best_exact_max_min": None if best is None or best.get("best_probe") is None else best["best_probe"].get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "failure_mode_counts": failure_counts(results),
        "results": results,
    }
    return scan.build_record(exact_scanner=exact_scanner)


def audit_record(limit=None, case_index=None, case_range=None):
    native = load_source_module(NATIVE_CACHE_AUDIT_PATH, "native_cache_for_upstream_b47")
    repaired = load_source_module(REPAIRED_AUDIT_PATH, "repaired_split_for_upstream_b47")
    v2 = load_source_module(V2_AUDIT_PATH, "compensated_v2_for_upstream_b47")

    artifact, _ = native.load_cache_artifact()
    scalable, residual = native.load_eval_helpers()
    F = artifact["matrix"].base_ring()
    H = artifact.get("H", [])
    if len(H) != 512:
        _, _, rebuilt_H = residual.field_context()
        H = [F(value) for value in rebuilt_H]
    powers = residual.precompute_powers(F, H)
    split_ledger = v2.split_ledger_from_artifact(artifact, repaired, residual, F, powers)

    results = [
        case_record(case, artifact, scalable, residual, repaired, v2, split_ledger, powers)
        for case in selected_cases(limit=limit, case_index=case_index, case_range=case_range)
    ]
    return jsonable(scanner_from_results(results))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--case-index", type=int)
    parser.add_argument("--case-range")
    parser.add_argument("--list-cases", action="store_true")
    args = parser.parse_args()
    if args.list_cases:
        print(json.dumps(jsonable({"cases": cases(), "systems_planned": len(cases())}), indent=2, sort_keys=True))
        return
    record = audit_record(limit=args.limit, case_index=args.case_index, case_range=args.case_range)
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        scanner = record["exact_scanner"]
        print("SAGE_AUDIT_M1_A327_UPSTREAM_B47_ROBUST_EXACT_SCANNER_OK")
        print("systems_tested: %d" % scanner["systems_tested"])
        print("exact_vectors_constructed: %d" % scanner["exact_vectors_constructed"])
        print("split_probe_vectors: %d" % scanner["split_probe_vectors"])
        print("split_resilient_skeletons: %d" % scanner["split_resilient_skeletons"])
        print("best_failure_mode: %s" % scanner["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
