import csv
import json

import pytest

from experimental.locator_fiber_crosscheck_report.compare_locator_fiber_outputs import (
    main,
)


CSV_COLUMNS = [
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
]


def write_python_csv(path):
    rows = [
        {
            "p": 5,
            "n": 4,
            "k": 2,
            "agreement_size": 3,
            "template": "monomial",
            "seed": "null",
            "supports_checked": 4,
            "fiber_size": 0,
            "fiber_density": 0.0,
            "interpolation_floor": "False",
            "nontrivial_locator_constraint": "True",
            "nontrivial_quotient_orders": "2",
            "quotient_periodic_valid_support_counts": "2:0",
            "status": "EXPERIMENTAL",
            "json_file": "monomial.json",
        },
        {
            "p": 5,
            "n": 4,
            "k": 2,
            "agreement_size": 3,
            "template": "zero",
            "seed": "null",
            "supports_checked": 4,
            "fiber_size": 4,
            "fiber_density": 1.0,
            "interpolation_floor": "False",
            "nontrivial_locator_constraint": "True",
            "nontrivial_quotient_orders": "2",
            "quotient_periodic_valid_support_counts": "2:0",
            "status": "EXPERIMENTAL",
            "json_file": "zero.json",
        },
        {
            "p": 7,
            "n": 6,
            "k": 3,
            "agreement_size": 4,
            "template": "random",
            "seed": 0,
            "supports_checked": 15,
            "fiber_size": 2,
            "fiber_density": 2 / 15,
            "interpolation_floor": "False",
            "nontrivial_locator_constraint": "True",
            "nontrivial_quotient_orders": "2;3",
            "quotient_periodic_valid_support_counts": "2:0;3:0",
            "status": "EXPERIMENTAL",
            "json_file": "python_only.json",
        },
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def sage_report_case(
    *,
    p,
    n,
    k,
    agreement_size,
    template,
    supports_tested,
    fiber_size,
    nontrivial,
):
    return {
        "status": "EXPERIMENTAL",
        "inputs": {
            "p": p,
            "n": n,
            "k": k,
            "agreement_size": agreement_size,
            "template": template,
        },
        "scan": {
            "supports_tested": supports_tested,
            "fiber_size": fiber_size,
            "nontrivial_locator_constraint": nontrivial,
        },
    }


def write_sage_json(path):
    payload = {
        "status": "EXPERIMENTAL",
        "reports": [
            sage_report_case(
                p=5,
                n=4,
                k=2,
                agreement_size=3,
                template="monomial",
                supports_tested=4,
                fiber_size=0,
                nontrivial=True,
            ),
            sage_report_case(
                p=5,
                n=4,
                k=2,
                agreement_size=3,
                template="zero",
                supports_tested=4,
                fiber_size=3,
                nontrivial=True,
            ),
            sage_report_case(
                p=11,
                n=10,
                k=5,
                agreement_size=6,
                template="monomial",
                supports_tested=210,
                fiber_size=0,
                nontrivial=True,
            ),
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def read_json(path):
    return json.loads(path.read_text())


def test_compare_locator_fiber_outputs_reports_mismatches(tmp_path, capsys):
    python_csv = tmp_path / "locator_fiber_sweep.csv"
    sage_json = tmp_path / "sage_locator.json"
    out_dir = tmp_path / "report"
    write_python_csv(python_csv)
    write_sage_json(sage_json)

    exit_code = main(
        [
            "--python-csv",
            str(python_csv),
            "--sage-json",
            str(sage_json),
            "--out-dir",
            str(out_dir),
        ]
    )

    assert exit_code == 0
    stdout = capsys.readouterr().out
    assert "Locator-fiber cross-check report (EXPERIMENTAL)" in stdout
    assert "no RS/list-decoding/MCA safety assertion" in stdout

    report = read_json(out_dir / "locator_fiber_crosscheck_report.json")
    assert report["status"] == "EXPERIMENTAL"
    assert report["summary"] == {
        "python_rows": 3,
        "sage_rows": 3,
        "matched_cases": 2,
        "mismatched_cases": 1,
        "python_only_cases": 1,
        "sage_only_cases": 1,
        "all_matched_cases_agree": False,
    }
    assert report["mismatches"][0]["case"]["template"] == "zero"
    assert report["mismatches"][0]["mismatches"] == [
        {"field": "fiber_size", "python": 4, "sage": 3}
    ]
    assert report["python_only"][0]["template"] == "random"
    assert report["sage_only"][0]["p"] == 11

    markdown = (out_dir / "locator_fiber_crosscheck_report.md").read_text()
    assert "Experimental comparison only." in markdown
    assert "No theorem status upgrade." in markdown
    assert "Python-Only Cases" in markdown
    assert "Sage-Only Cases" in markdown


def test_compare_locator_fiber_outputs_missing_file_is_parser_error(tmp_path):
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--python-csv",
                str(tmp_path / "missing.csv"),
                "--sage-json",
                str(tmp_path / "missing.json"),
                "--out-dir",
                str(tmp_path / "report"),
            ]
        )

    assert exc_info.value.code == 2
