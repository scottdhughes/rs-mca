#!/usr/bin/env python3
"""Analyze locator-fiber sweep CSV outputs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def current_repo_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


STATUS = "EXPERIMENTAL"
ANALYSIS_CLAIM = (
    "experimental locator-fiber data analysis only; "
    "no RS/list-decoding/MCA safety assertion; "
    "no theorem status upgrade"
)
ANALYSIS_CSV_COLUMNS = (
    "p",
    "n",
    "k",
    "agreement_size",
    "template",
    "seeds",
    "row_count",
    "interpolation_floor",
    "nontrivial_locator_constraint",
    "max_fiber_size",
    "max_fiber_density",
    "quotient_periodic_valid_support_counts",
    "status",
)


def parse_bool(value: str) -> bool:
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"invalid boolean value {value!r}")


def parse_int(value: str, name: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"invalid integer for {name}: {value!r}") from exc


def parse_float(value: str, name: str) -> float | None:
    if value == "null":
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"invalid float for {name}: {value!r}") from exc


def parse_seed(value: str) -> int | None:
    if value in {"", "null", "None"}:
        return None
    return parse_int(value, "seed")


def parse_int_list(value: str) -> list[int]:
    if value in {"", "null", "None"}:
        return []
    return [parse_int(item, "integer list item") for item in value.split(";")]


def parse_int_map(value: str) -> dict[str, int]:
    if value in {"", "null", "None"}:
        return {}
    out: dict[str, int] = {}
    for item in value.split(";"):
        key, raw = item.split(":", 1)
        out[key] = parse_int(raw, f"count for quotient order {key}")
    return out


def csv_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    if isinstance(value, dict):
        return ";".join(f"{key}:{value[key]}" for key in sorted(value, key=int))
    return str(value)


def load_sweep_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "p",
            "n",
            "k",
            "agreement_size",
            "template",
            "seed",
            "supports_checked",
            "fiber_size",
            "fiber_density",
            "interpolation_floor",
            "nontrivial_locator_constraint",
            "nontrivial_quotient_orders",
            "quotient_periodic_valid_support_counts",
            "status",
            "json_file",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required CSV columns: {sorted(missing)}")

        rows = []
        for raw in reader:
            row = {
                "p": parse_int(raw["p"], "p"),
                "n": parse_int(raw["n"], "n"),
                "k": parse_int(raw["k"], "k"),
                "agreement_size": parse_int(
                    raw["agreement_size"],
                    "agreement_size",
                ),
                "template": raw["template"],
                "seed": parse_seed(raw["seed"]),
                "supports_checked": parse_int(
                    raw["supports_checked"],
                    "supports_checked",
                ),
                "fiber_size": parse_int(raw["fiber_size"], "fiber_size"),
                "fiber_density": parse_float(raw["fiber_density"], "fiber_density"),
                "interpolation_floor": parse_bool(raw["interpolation_floor"]),
                "nontrivial_locator_constraint": parse_bool(
                    raw["nontrivial_locator_constraint"]
                ),
                "nontrivial_quotient_orders": parse_int_list(
                    raw["nontrivial_quotient_orders"]
                ),
                "quotient_periodic_valid_support_counts": parse_int_map(
                    raw["quotient_periodic_valid_support_counts"]
                ),
                "status": raw["status"],
                "json_file": raw["json_file"],
            }
            rows.append(row)
    return rows


def group_rows(
    rows: list[dict[str, Any]],
) -> dict[tuple[int, int, int, int, str], list[dict[str, Any]]]:
    grouped: dict[tuple[int, int, int, int, str], list[dict[str, Any]]] = defaultdict(
        list
    )
    for row in rows:
        key = (
            row["p"],
            row["n"],
            row["k"],
            row["agreement_size"],
            row["template"],
        )
        grouped[key].append(row)
    return grouped


def aggregate_quotient_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        for order, count in row["quotient_periodic_valid_support_counts"].items():
            out[order] = max(out.get(order, 0), count)
    return out


def analyze_group(
    key: tuple[int, int, int, int, str],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    p, n, k, agreement_size, template = key
    seeds = sorted(
        (row["seed"] for row in rows if row["seed"] is not None),
    )
    fiber_sizes = [row["fiber_size"] for row in rows]
    densities = [
        row["fiber_density"]
        for row in rows
        if row["fiber_density"] is not None
    ]
    interpolation_floor_values = {row["interpolation_floor"] for row in rows}
    nontrivial_values = {row["nontrivial_locator_constraint"] for row in rows}
    return {
        "p": p,
        "n": n,
        "k": k,
        "agreement_size": agreement_size,
        "template": template,
        "seeds": seeds,
        "row_count": len(rows),
        "interpolation_floor": (
            interpolation_floor_values.pop()
            if len(interpolation_floor_values) == 1
            else None
        ),
        "nontrivial_locator_constraint": (
            nontrivial_values.pop() if len(nontrivial_values) == 1 else None
        ),
        "max_fiber_size": max(fiber_sizes) if fiber_sizes else None,
        "max_fiber_density": max(densities) if densities else None,
        "quotient_periodic_valid_support_counts": aggregate_quotient_counts(rows),
        "rows": sorted(
            rows,
            key=lambda row: csv_value(row["seed"]),
        ),
        "status": STATUS,
    }


def largest_rows(
    rows: list[dict[str, Any]],
    *,
    key: str,
    top_fibers: int,
) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            -(row[key] if row[key] is not None else -1),
            row["p"],
            row["k"],
            row["agreement_size"],
            row["template"],
            csv_value(row["seed"]),
        ),
    )[:top_fibers]


def summarize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "p": row["p"],
        "n": row["n"],
        "k": row["k"],
        "agreement_size": row["agreement_size"],
        "template": row["template"],
        "seed": row["seed"],
        "supports_checked": row["supports_checked"],
        "fiber_size": row["fiber_size"],
        "fiber_density": row["fiber_density"],
        "json_file": row["json_file"],
    }


def sanity_checks(rows: list[dict[str, Any]]) -> dict[str, Any]:
    interpolation_floor_density_violations = [
        summarize_row(row)
        for row in rows
        if row["interpolation_floor"] and row["fiber_density"] != 1.0
    ]
    zero_template_violations = [
        summarize_row(row)
        for row in rows
        if row["template"] == "zero"
        and row["fiber_size"] != row["supports_checked"]
    ]
    return {
        "interpolation_floor_density_violations": (
            interpolation_floor_density_violations
        ),
        "zero_template_violations": zero_template_violations,
    }


def analyze_rows(
    rows: list[dict[str, Any]],
    *,
    top_fibers: int = 20,
) -> dict[str, Any]:
    if top_fibers < 0:
        raise ValueError("top_fibers must be nonnegative")

    grouped = group_rows(rows)
    groups = [
        analyze_group(key, value)
        for key, value in sorted(grouped.items())
    ]
    nontrivial_rows = [
        row for row in rows if row["nontrivial_locator_constraint"]
    ]
    sparse_random_nonzero = [
        summarize_row(row)
        for row in nontrivial_rows
        if row["template"] == "random"
        and row["fiber_size"] > 0
        and row["fiber_size"] < row["supports_checked"]
    ]
    monomial_nonzero = [
        summarize_row(row)
        for row in nontrivial_rows
        if row["template"] == "monomial" and row["fiber_size"] > 0
    ]
    quotient_rows = [
        {
            **summarize_row(row),
            "quotient_periodic_valid_support_counts": row[
                "quotient_periodic_valid_support_counts"
            ],
        }
        for row in nontrivial_rows
        if any(row["quotient_periodic_valid_support_counts"].values())
    ]
    return {
        "schema_version": "locator-fiber-sweep-analysis-0.1.0",
        "status": STATUS,
        "claim": ANALYSIS_CLAIM,
        "group_summaries": groups,
        "sanity_checks": sanity_checks(rows),
        "nontrivial_summary": {
            "largest_by_fiber_size": [
                summarize_row(row)
                for row in largest_rows(
                    nontrivial_rows,
                    key="fiber_size",
                    top_fibers=top_fibers,
                )
            ],
            "largest_by_fiber_density": [
                summarize_row(row)
                for row in largest_rows(
                    nontrivial_rows,
                    key="fiber_density",
                    top_fibers=top_fibers,
                )
            ],
            "sparse_random_nonzero_fiber_cases": sorted(
                sparse_random_nonzero,
                key=lambda row: (
                    -row["fiber_size"],
                    row["p"],
                    row["k"],
                    row["agreement_size"],
                    csv_value(row["seed"]),
                ),
            )[:top_fibers],
            "monomial_cases_with_nonzero_fiber": sorted(
                monomial_nonzero,
                key=lambda row: (
                    -row["fiber_size"],
                    row["p"],
                    row["k"],
                    row["agreement_size"],
                ),
            )[:top_fibers],
            "quotient_periodic_valid_support_summaries": sorted(
                quotient_rows,
                key=lambda row: (
                    -max(row["quotient_periodic_valid_support_counts"].values()),
                    row["p"],
                    row["k"],
                    row["agreement_size"],
                    row["template"],
                ),
            )[:top_fibers],
        },
        "provenance": {
            "generator": (
                "experimental/locator_fiber_sweep_analysis/"
                "analyze_locator_fiber_sweep.py"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
            "parameters": {
                "top_fibers": top_fibers,
            },
        },
    }


def write_analysis_csv(analysis: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ANALYSIS_CSV_COLUMNS)
        writer.writeheader()
        for group in analysis["group_summaries"]:
            writer.writerow(
                {
                    column: csv_value(group[column])
                    for column in ANALYSIS_CSV_COLUMNS
                }
            )


def write_json(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def markdown_table(
    rows: list[dict[str, Any]],
    *,
    empty_text: str = "None.",
) -> list[str]:
    if not rows:
        return [empty_text]
    lines = [
        (
            "| p | n | k | agreement | template | seed | supports | "
            "fiber | density | JSON |"
        ),
        "|---:|---:|---:|---:|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['p']} | {row['n']} | {row['k']} | "
            f"{row['agreement_size']} | {row['template']} | "
            f"{csv_value(row['seed'])} | {row['supports_checked']} | "
            f"{row['fiber_size']} | {csv_value(row['fiber_density'])} | "
            f"{row['json_file']} |"
        )
    return lines


def quotient_markdown_table(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return ["None."]
    lines = [
        (
            "| p | n | k | agreement | template | seed | fiber | "
            "quotient counts | JSON |"
        ),
        "|---:|---:|---:|---:|---|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['p']} | {row['n']} | {row['k']} | "
            f"{row['agreement_size']} | {row['template']} | "
            f"{csv_value(row['seed'])} | {row['fiber_size']} | "
            f"{csv_value(row['quotient_periodic_valid_support_counts'])} | "
            f"{row['json_file']} |"
        )
    return lines


def build_markdown(analysis: dict[str, Any]) -> str:
    sanity = analysis["sanity_checks"]
    nontrivial = analysis["nontrivial_summary"]
    lines = [
        "# Locator-Fiber Sweep Analysis",
        "",
        "Experimental data analysis only.",
        "No RS/list-decoding/MCA safety assertion.",
        "No theorem status upgrade.",
        "",
        "Interpolation-floor rows have agreement_size <= k.",
        "Nontrivial locator-fiber constraints begin at agreement_size > k.",
        "",
        "## Group Summary",
        "",
        (
            "| p | n | k | agreement | template | seeds | rows | floor | "
            "nontrivial | max fiber | max density |"
        ),
        "|---:|---:|---:|---:|---|---|---:|---|---|---:|---:|",
    ]
    for group in analysis["group_summaries"]:
        lines.append(
            "| "
            f"{group['p']} | {group['n']} | {group['k']} | "
            f"{group['agreement_size']} | {group['template']} | "
            f"{csv_value(group['seeds'])} | {group['row_count']} | "
            f"{csv_value(group['interpolation_floor'])} | "
            f"{csv_value(group['nontrivial_locator_constraint'])} | "
            f"{csv_value(group['max_fiber_size'])} | "
            f"{csv_value(group['max_fiber_density'])} |"
        )

    lines.extend(
        [
            "",
            "## Sanity Checks",
            "",
            "### Interpolation-Floor Density Violations",
            "",
        ]
    )
    lines.extend(
        markdown_table(sanity["interpolation_floor_density_violations"])
    )
    lines.extend(["", "### Zero-Template Violations", ""])
    lines.extend(markdown_table(sanity["zero_template_violations"]))

    lines.extend(["", "## Nontrivial Rows", "", "### Largest Fiber Size", ""])
    lines.extend(markdown_table(nontrivial["largest_by_fiber_size"]))
    lines.extend(["", "### Largest Fiber Density", ""])
    lines.extend(markdown_table(nontrivial["largest_by_fiber_density"]))
    lines.extend(["", "### Sparse Random Nonzero Fiber Cases", ""])
    lines.extend(markdown_table(nontrivial["sparse_random_nonzero_fiber_cases"]))
    lines.extend(["", "### Monomial Cases With Nonzero Fiber", ""])
    lines.extend(markdown_table(nontrivial["monomial_cases_with_nonzero_fiber"]))
    lines.extend(["", "### Quotient-Periodic Valid Support Summaries", ""])
    lines.extend(
        quotient_markdown_table(
            nontrivial["quotient_periodic_valid_support_summaries"]
        )
    )

    lines.extend(
        [
            "",
            "## Provenance",
            "",
            f"- Status: {analysis['status']}",
            f"- Claim discipline: {analysis['claim']}",
            f"- Repo commit: {analysis['provenance']['repo_commit']}",
            f"- Created at UTC: {analysis['provenance']['created_at_utc']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(analysis: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_analysis_csv(analysis, out_dir / "locator_fiber_sweep_analysis.csv")
    (out_dir / "locator_fiber_sweep_analysis.md").write_text(
        build_markdown(analysis)
    )
    write_json(analysis, out_dir / "locator_fiber_sweep_analysis.json")


def analyze_sweep(
    csv_path: Path,
    *,
    out_dir: Path | None = None,
    top_fibers: int = 20,
) -> dict[str, Any]:
    rows = load_sweep_csv(csv_path)
    analysis = analyze_rows(rows, top_fibers=top_fibers)
    analysis["provenance"]["parameters"].update(
        {
            "csv": str(csv_path),
            "out_dir": str(out_dir) if out_dir is not None else None,
        }
    )
    write_outputs(analysis, out_dir or csv_path.parent)
    return analysis


def format_summary(analysis: dict[str, Any]) -> str:
    sanity = analysis["sanity_checks"]
    nontrivial = analysis["nontrivial_summary"]
    violation_count = (
        len(sanity["interpolation_floor_density_violations"])
        + len(sanity["zero_template_violations"])
    )
    return "\n".join(
        [
            f"Locator-fiber sweep analysis ({analysis['status']})",
            f"groups={len(analysis['group_summaries'])}",
            f"sanity_violations={violation_count}",
            (
                "sparse_random_nonzero="
                f"{len(nontrivial['sparse_random_nonzero_fiber_cases'])}"
            ),
            "csv=locator_fiber_sweep_analysis.csv",
            "markdown=locator_fiber_sweep_analysis.md",
            "json=locator_fiber_sweep_analysis.json",
            f"claim: {analysis['claim']}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze EXPERIMENTAL locator-fiber sweep outputs."
    )
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--top-fibers", type=int, default=20)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        analysis = analyze_sweep(
            args.csv,
            out_dir=args.out_dir,
            top_fibers=args.top_fibers,
        )
    except ValueError as exc:
        parser.error(str(exc))

    print(format_summary(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
