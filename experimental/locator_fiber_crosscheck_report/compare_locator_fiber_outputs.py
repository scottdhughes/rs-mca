#!/usr/bin/env python3
"""Compare Python locator-fiber sweep rows with Sage cross-check JSON."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATUS = "EXPERIMENTAL"
CLAIM = (
    "experimental locator-fiber cross-check comparison only; "
    "no RS/list-decoding/MCA safety assertion; "
    "no theorem status upgrade"
)
CASE_FIELDS = ("p", "n", "k", "agreement_size", "template")


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


def parse_bool(value: Any, name: str) -> bool:
    if isinstance(value, bool):
        return value
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"invalid boolean for {name}: {value!r}")


def parse_int(value: Any, name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid integer for {name}: {value!r}") from exc


def case_key(row: dict[str, Any]) -> str:
    return "|".join(str(row[field]) for field in CASE_FIELDS)


def case_label(row: dict[str, Any]) -> str:
    return (
        f"p={row['p']} n={row['n']} k={row['k']} "
        f"a={row['agreement_size']} template={row['template']}"
    )


def load_python_csv(path: Path) -> dict[str, dict[str, Any]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "p",
            "n",
            "k",
            "agreement_size",
            "template",
            "supports_checked",
            "fiber_size",
            "nontrivial_locator_constraint",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required Python CSV columns: {sorted(missing)}")

        rows: dict[str, dict[str, Any]] = {}
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
                "supports_checked": parse_int(
                    raw["supports_checked"],
                    "supports_checked",
                ),
                "fiber_size": parse_int(raw["fiber_size"], "fiber_size"),
                "nontrivial_locator_constraint": parse_bool(
                    raw["nontrivial_locator_constraint"],
                    "nontrivial_locator_constraint",
                ),
                "source": "python_csv",
            }
            key = case_key(row)
            if key in rows:
                raise ValueError(f"duplicate Python CSV case: {case_label(row)}")
            rows[key] = row
    return rows


def sage_reports(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if "reports" in payload:
        reports = payload["reports"]
        if not isinstance(reports, list):
            raise ValueError("sage JSON reports field must be a list")
        return reports
    return [payload]


def normalize_sage_report(report: dict[str, Any]) -> dict[str, Any]:
    inputs = report.get("inputs")
    scan = report.get("scan")
    if not isinstance(inputs, dict) or not isinstance(scan, dict):
        raise ValueError("sage report must contain inputs and scan objects")
    row = {
        "p": parse_int(inputs.get("p"), "sage inputs.p"),
        "n": parse_int(inputs.get("n"), "sage inputs.n"),
        "k": parse_int(inputs.get("k"), "sage inputs.k"),
        "agreement_size": parse_int(
            inputs.get("agreement_size"),
            "sage inputs.agreement_size",
        ),
        "template": inputs.get("template"),
        "supports_checked": parse_int(
            scan.get("supports_tested"),
            "sage scan.supports_tested",
        ),
        "fiber_size": parse_int(scan.get("fiber_size"), "sage scan.fiber_size"),
        "nontrivial_locator_constraint": parse_bool(
            scan.get("nontrivial_locator_constraint"),
            "sage scan.nontrivial_locator_constraint",
        ),
        "source": "sage_json",
    }
    if not isinstance(row["template"], str):
        raise ValueError("sage inputs.template must be a string")
    return row


def load_sage_json(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text())
    rows: dict[str, dict[str, Any]] = {}
    for report in sage_reports(payload):
        row = normalize_sage_report(report)
        key = case_key(row)
        if key in rows:
            raise ValueError(f"duplicate Sage JSON case: {case_label(row)}")
        rows[key] = row
    return rows


def compare_case(
    key: str,
    python_row: dict[str, Any],
    sage_row: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "supports_checked": (
            python_row["supports_checked"],
            sage_row["supports_checked"],
        ),
        "fiber_size": (python_row["fiber_size"], sage_row["fiber_size"]),
        "nontrivial_locator_constraint": (
            python_row["nontrivial_locator_constraint"],
            sage_row["nontrivial_locator_constraint"],
        ),
    }
    mismatches = [
        {
            "field": field,
            "python": values[0],
            "sage": values[1],
        }
        for field, values in checks.items()
        if values[0] != values[1]
    ]
    return {
        "key": key,
        "case": {field: python_row[field] for field in CASE_FIELDS},
        "python": {
            "supports_checked": python_row["supports_checked"],
            "fiber_size": python_row["fiber_size"],
            "nontrivial_locator_constraint": python_row[
                "nontrivial_locator_constraint"
            ],
        },
        "sage": {
            "supports_checked": sage_row["supports_checked"],
            "fiber_size": sage_row["fiber_size"],
            "nontrivial_locator_constraint": sage_row[
                "nontrivial_locator_constraint"
            ],
        },
        "matches": not mismatches,
        "mismatches": mismatches,
    }


def compare_rows(
    python_rows: dict[str, dict[str, Any]],
    sage_rows: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    shared = sorted(set(python_rows) & set(sage_rows))
    python_only = sorted(set(python_rows) - set(sage_rows))
    sage_only = sorted(set(sage_rows) - set(python_rows))
    comparisons = [
        compare_case(key, python_rows[key], sage_rows[key])
        for key in shared
    ]
    mismatches = [item for item in comparisons if not item["matches"]]
    return {
        "schema_version": "locator-fiber-crosscheck-report-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "summary": {
            "python_rows": len(python_rows),
            "sage_rows": len(sage_rows),
            "matched_cases": len(comparisons),
            "mismatched_cases": len(mismatches),
            "python_only_cases": len(python_only),
            "sage_only_cases": len(sage_only),
            "all_matched_cases_agree": not mismatches,
        },
        "comparisons": comparisons,
        "mismatches": mismatches,
        "python_only": [python_rows[key] for key in python_only],
        "sage_only": [sage_rows[key] for key in sage_only],
        "provenance": {
            "generator": (
                "experimental/locator_fiber_crosscheck_report/"
                "compare_locator_fiber_outputs.py"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
        },
    }


def markdown_case_table(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return ["None."]
    lines = [
        "| p | n | k | agreement | template | supports | fiber | nontrivial |",
        "|---:|---:|---:|---:|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['p']} | {row['n']} | {row['k']} | "
            f"{row['agreement_size']} | {row['template']} | "
            f"{row['supports_checked']} | {row['fiber_size']} | "
            f"{row['nontrivial_locator_constraint']} |"
        )
    return lines


def build_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Locator-Fiber Cross-Check Report",
        "",
        "Experimental comparison only.",
        "No RS/list-decoding/MCA safety assertion.",
        "No theorem status upgrade.",
        "",
        "## Summary",
        "",
        f"- Python rows: {summary['python_rows']}",
        f"- Sage rows: {summary['sage_rows']}",
        f"- Matched cases: {summary['matched_cases']}",
        f"- Mismatched cases: {summary['mismatched_cases']}",
        f"- Python-only cases: {summary['python_only_cases']}",
        f"- Sage-only cases: {summary['sage_only_cases']}",
        f"- All matched cases agree: {summary['all_matched_cases_agree']}",
        "",
        "## Matched Comparisons",
        "",
        (
            "| p | n | k | agreement | template | supports | "
            "Python fiber | Sage fiber | agree |"
        ),
        "|---:|---:|---:|---:|---|---:|---:|---:|---|",
    ]
    for item in report["comparisons"]:
        case = item["case"]
        lines.append(
            "| "
            f"{case['p']} | {case['n']} | {case['k']} | "
            f"{case['agreement_size']} | {case['template']} | "
            f"{item['python']['supports_checked']} | "
            f"{item['python']['fiber_size']} | "
            f"{item['sage']['fiber_size']} | {item['matches']} |"
        )

    lines.extend(["", "## Mismatches", ""])
    if not report["mismatches"]:
        lines.append("None.")
    else:
        for item in report["mismatches"]:
            lines.append(f"- {case_label(item['case'])}")
            for mismatch in item["mismatches"]:
                lines.append(
                    "  - "
                    f"{mismatch['field']}: "
                    f"python={mismatch['python']} sage={mismatch['sage']}"
                )

    lines.extend(["", "## Python-Only Cases", ""])
    lines.extend(markdown_case_table(report["python_only"]))
    lines.extend(["", "## Sage-Only Cases", ""])
    lines.extend(markdown_case_table(report["sage_only"]))
    lines.extend(
        [
            "",
            "## Provenance",
            "",
            f"- Status: {report['status']}",
            f"- Claim discipline: {report['claim']}",
            f"- Repo commit: {report['provenance']['repo_commit']}",
            f"- Created at UTC: {report['provenance']['created_at_utc']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def write_outputs(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(report, out_dir / "locator_fiber_crosscheck_report.json")
    (out_dir / "locator_fiber_crosscheck_report.md").write_text(
        build_markdown(report)
    )


def compare_files(
    *,
    python_csv: Path,
    sage_json: Path,
    out_dir: Path,
) -> dict[str, Any]:
    report = compare_rows(
        load_python_csv(python_csv),
        load_sage_json(sage_json),
    )
    report["provenance"]["inputs"] = {
        "python_csv": str(python_csv),
        "sage_json": str(sage_json),
        "out_dir": str(out_dir),
    }
    write_outputs(report, out_dir)
    return report


def format_summary(report: dict[str, Any]) -> str:
    summary = report["summary"]
    return "\n".join(
        [
            f"Locator-fiber cross-check report ({report['status']})",
            f"matched_cases={summary['matched_cases']}",
            f"mismatched_cases={summary['mismatched_cases']}",
            f"python_only_cases={summary['python_only_cases']}",
            f"sage_only_cases={summary['sage_only_cases']}",
            f"all_matched_cases_agree={summary['all_matched_cases_agree']}",
            f"claim: {report['claim']}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare EXPERIMENTAL locator-fiber Python/Sage outputs."
    )
    parser.add_argument("--python-csv", type=Path, required=True)
    parser.add_argument("--sage-json", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = compare_files(
            python_csv=args.python_csv,
            sage_json=args.sage_json,
            out_dir=args.out_dir,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(format_summary(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
