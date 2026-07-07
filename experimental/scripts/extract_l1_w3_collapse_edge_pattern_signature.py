#!/usr/bin/env python3
"""Extract the W3 collapse-edge pattern signature from the compact certificate.

This is a proof-orientation helper.  It does not regenerate GF(137) edge
arithmetic and does not replace the Lean checker.  It reads the integrated
finite Lean certificate plus the compact origin summary and records the
case-level pattern that a later symbolic/general lemma would need to explain.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_LEAN = Path(
    "experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeCertificate.lean"
)
DEFAULT_ORIGIN = Path(
    "experimental/data/certificates/l1-residual-excess-classifier/"
    "w3_collapse_edge_origin_audit_combo012_sizes10_2_3.json"
)
DEFAULT_OUTPUT = Path(
    "experimental/data/certificates/l1-residual-excess-classifier/"
    "w3_collapse_edge_pattern_signature_combo012_sizes10_2_3.json"
)

EXPECTED_SURVIVOR = {"coset_w": 37, "component": [17, 36, 130]}
EXPECTED_SHIFTS = [67, 103, 111, 17, 20, 121]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_int_list(text: str) -> list[int]:
    if not text.strip():
        return []
    return [int(item.strip()) for item in text.split(",") if item.strip()]


def parse_components(text: str) -> list[list[int]]:
    return [parse_int_list(match) for match in re.findall(r"\[([0-9,\s]+)\]", text)]


def parse_edges(text: str) -> list[list[int]]:
    return [[int(a), int(b)] for a, b in re.findall(r"edge\s+(\d+)\s+(\d+)", text)]


def contribution(component: list[int]) -> int:
    return len(component) - 2 if len(component) >= 3 else 0


def degree_histogram(edges: list[list[int]]) -> dict[str, int]:
    degrees: dict[int, int] = {}
    for a, b in edges:
        degrees[a] = degrees.get(a, 0) + 1
        degrees[b] = degrees.get(b, 0) + 1
    histogram: dict[str, int] = {}
    for degree in degrees.values():
        key = str(degree)
        histogram[key] = histogram.get(key, 0) + 1
    return dict(sorted(histogram.items(), key=lambda item: int(item[0])))


def max_degree(edges: list[list[int]]) -> int:
    histogram = degree_histogram(edges)
    return max((int(degree) for degree in histogram), default=0)


def edges_in_component(edges: list[list[int]], component: list[int]) -> list[list[int]]:
    component_set = set(component)
    return [edge for edge in edges if edge[0] in component_set and edge[1] in component_set]


def extract_def_body(kind: str, name: str, lean_text: str) -> str:
    pattern = re.compile(
        rf"def {re.escape(name)} : {kind} :=\n  \{{\n(?P<body>.*?)\n  \}}",
        re.DOTALL,
    )
    match = pattern.search(lean_text)
    if not match:
        raise ValueError(f"could not find {kind} definition {name!r}")
    return match.group("body")


def parse_coset(name: str, lean_text: str) -> dict[str, Any]:
    body = extract_def_body("CosetCert", name, lean_text)
    coset_match = re.search(r"cosetW := (\d+)", body)
    points_match = re.search(r"points := \[(?P<points>[^\]]*)\]", body)
    active_match = re.search(r"activeEdges := \[(?P<edges>.*?)\]\n    components", body, re.DOTALL)
    components_match = re.search(r"components := (?P<components>\[.*\])\s*$", body, re.DOTALL)
    if not (coset_match and points_match and active_match and components_match):
        raise ValueError(f"incomplete coset definition {name!r}")

    active_edges = parse_edges(active_match.group("edges"))
    components = parse_components(components_match.group("components"))
    large = [component for component in components if len(component) >= 3]
    large_component_shapes = [
        {
            "component": component,
            "edge_count": len(edges_in_component(active_edges, component)),
            "degree_histogram": degree_histogram(edges_in_component(active_edges, component)),
        }
        for component in large
    ]
    return {
        "name": name,
        "coset_w": int(coset_match.group(1)),
        "point_count": len(parse_int_list(points_match.group("points"))),
        "active_edges": active_edges,
        "active_edge_count": len(active_edges),
        "max_degree": max_degree(active_edges),
        "degree_histogram": degree_histogram(active_edges),
        "component_sizes": sorted((len(component) for component in components), reverse=True),
        "large_components": large,
        "large_component_shapes": large_component_shapes,
        "contribution": sum(contribution(component) for component in components),
    }


def parse_case(index: int, lean_text: str) -> dict[str, Any]:
    name = f"case{index}"
    body = extract_def_body("CaseCert", name, lean_text)
    shift = int(re.search(r"shift := (\d+)", body).group(1))  # type: ignore[union-attr]
    head_missing = int(re.search(r"headMissing := (\d+)", body).group(1))  # type: ignore[union-attr]
    head_stray = int(re.search(r"headStray := (\d+)", body).group(1))  # type: ignore[union-attr]
    head_name = re.search(r"headCoset := (case\d+_head)", body).group(1)  # type: ignore[union-attr]
    alt_names = re.search(r"alternateCosets := \[(?P<alts>[^\]]+)\]", body).group("alts")  # type: ignore[union-attr]
    alternate_names = [item.strip() for item in alt_names.split(",")]
    survivor_match = re.search(
        r"expectedAlternateLarge := \[\{ cosetW := (?P<coset>\d+), component := \[(?P<component>[^\]]+)\] \}\]",
        body,
    )
    if not survivor_match:
        raise ValueError(f"could not parse expected survivor for {name}")
    expected_survivor = {
        "coset_w": int(survivor_match.group("coset")),
        "component": parse_int_list(survivor_match.group("component")),
    }

    head = parse_coset(head_name, lean_text)
    alternates = [parse_coset(alt_name, lean_text) for alt_name in alternate_names]
    alternate_large = [
        {"coset_w": alt["coset_w"], "component": component}
        for alt in alternates
        for component in alt["large_components"]
    ]
    alternate_contribution = sum(alt["contribution"] for alt in alternates)
    non_survivor_max_component = max(
        (
            size
            for alt in alternates
            if alt["coset_w"] != expected_survivor["coset_w"]
            for size in alt["component_sizes"]
        ),
        default=0,
    )
    return {
        "case_index": index,
        "shift": shift,
        "head_missing": head_missing,
        "head_stray": head_stray,
        "head_coset": {
            "coset_w": head["coset_w"],
            "active_edge_count": head["active_edge_count"],
            "component_sizes": head["component_sizes"],
        },
        "expected_survivor": expected_survivor,
        "alternate_large_components": alternate_large,
        "alternate_contribution": alternate_contribution,
        "alternate_coset_summaries": [
            {
                "coset_w": alt["coset_w"],
                "active_edge_count": alt["active_edge_count"],
                "max_degree": alt["max_degree"],
                "degree_histogram": alt["degree_histogram"],
                "component_sizes": alt["component_sizes"],
                "contribution": alt["contribution"],
                "matching_only": alt["max_degree"] <= 1,
                "large_component_shapes": alt["large_component_shapes"],
            }
            for alt in alternates
        ],
        "non_survivor_max_component": non_survivor_max_component,
        "non_survivor_max_degree": max(
            (
                alt["max_degree"]
                for alt in alternates
                if alt["coset_w"] != expected_survivor["coset_w"]
            ),
            default=0,
        ),
        "survivor_coset_summary": next(
            {
                "coset_w": alt["coset_w"],
                "active_edge_count": alt["active_edge_count"],
                "max_degree": alt["max_degree"],
                "degree_histogram": alt["degree_histogram"],
                "component_sizes": alt["component_sizes"],
                "large_component_shapes": alt["large_component_shapes"],
            }
            for alt in alternates
            if alt["coset_w"] == expected_survivor["coset_w"]
        ),
    }


def summarize_family(case: dict[str, Any], origin_case: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_index": case["case_index"],
        "target_family_id": origin_case["target_family_id"],
        "quotient_member": origin_case["quotient_member"],
        "shift": case["shift"],
        "quotient_projective_coeffs": origin_case.get("quotient_projective_coeffs"),
        "head_coset_w": case["head_coset"]["coset_w"],
        "head_component_sizes": case["head_coset"]["component_sizes"],
        "alternate_contribution": case["alternate_contribution"],
        "alternate_large_components": case["alternate_large_components"],
        "non_survivor_max_component": case["non_survivor_max_component"],
        "non_survivor_max_degree": case["non_survivor_max_degree"],
        "survivor_coset_summary": case["survivor_coset_summary"],
    }


def build_signature(lean_path: Path, origin_path: Path) -> dict[str, Any]:
    lean_text = lean_path.read_text()
    origin = json.loads(origin_path.read_text())
    origin_by_shift = {int(case["shift"]): case for case in origin["case_summaries"]}
    cases = [parse_case(index, lean_text) for index in range(6)]
    shifts = [case["shift"] for case in cases]
    families = [summarize_family(case, origin_by_shift[case["shift"]]) for case in cases]
    issues: list[str] = []
    if shifts != EXPECTED_SHIFTS:
        issues.append(f"unexpected shift sequence: {shifts}")
    if any((case["head_missing"], case["head_stray"]) != (2, 1) for case in cases):
        issues.append("not every case has head antecedent (missing,stray)=(2,1)")
    if any(case["expected_survivor"] != EXPECTED_SURVIVOR for case in cases):
        issues.append("not every case has the expected coset-37 survivor")
    if any(case["alternate_large_components"] != [EXPECTED_SURVIVOR] for case in cases):
        issues.append("not every case has exactly the expected large alternate component")
    if any(case["alternate_contribution"] != 1 for case in cases):
        issues.append("not every case has alternate contribution exactly 1")
    if any(case["non_survivor_max_component"] > 2 for case in cases):
        issues.append("some non-survivor alternate coset has a component of size >=3")
    if any(case["non_survivor_max_degree"] > 1 for case in cases):
        issues.append("some non-survivor alternate coset is not a matching")
    if any(
        case["survivor_coset_summary"]["large_component_shapes"]
        != [{"component": [17, 36, 130], "edge_count": 3, "degree_histogram": {"2": 3}}]
        for case in cases
    ):
        issues.append("survivor large component is not the expected triangle")

    grouped: dict[str, list[int]] = {}
    for family in families:
        key = f"{family['target_family_id']}::{family['quotient_member']}"
        grouped.setdefault(key, []).append(family["shift"])

    return {
        "status": "L1_W3_COLLAPSE_EDGE_PATTERN_SIGNATURE" if not issues else "L1_W3_COLLAPSE_EDGE_PATTERN_SIGNATURE_FAIL",
        "ok": not issues,
        "issues": issues,
        "source_lean": str(lean_path),
        "source_lean_sha256": sha256_text(lean_text),
        "source_origin": str(origin_path),
        "source_origin_sha256": origin.get("source_sha256"),
        "case_count": len(cases),
        "shifts": shifts,
        "dangerous_head_pattern": {"missing": 2, "stray": 1},
        "unique_large_alternate_survivor": EXPECTED_SURVIVOR,
        "alternate_contribution_vector": [case["alternate_contribution"] for case in cases],
        "non_survivor_max_component_vector": [case["non_survivor_max_component"] for case in cases],
        "non_survivor_max_degree_vector": [case["non_survivor_max_degree"] for case in cases],
        "graph_mechanism": {
            "non_survivor_alternates_are_matchings": all(
                case["non_survivor_max_degree"] <= 1 for case in cases
            ),
            "survivor_large_component_is_triangle": all(
                case["survivor_coset_summary"]["large_component_shapes"]
                == [{"component": [17, 36, 130], "edge_count": 3, "degree_histogram": {"2": 3}}]
                for case in cases
            ),
            "survivor_extra_edges_are_disjoint_from_triangle": all(
                case["survivor_coset_summary"]["max_degree"] <= 2 for case in cases
            ),
        },
        "two_family_shift_groups": grouped,
        "family_cases": families,
        "not_claimed": [
            "a symbolic W3 lemma",
            "a global L1 theorem",
            "a reconstruction of GF(137) edge arithmetic",
            "MCA or protocol evidence",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean", type=Path, default=DEFAULT_LEAN)
    parser.add_argument("--origin", type=Path, default=DEFAULT_ORIGIN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    signature = build_signature(args.lean, args.origin)
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(signature, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(signature, indent=2, sort_keys=True))
    else:
        print("OK" if signature["ok"] else "FAIL")
        for issue in signature["issues"]:
            print(issue)
    return 0 if signature["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
