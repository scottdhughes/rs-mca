import csv
import json
from pathlib import Path

from experimental.locator_fiber_sweep_analysis.analyze_locator_fiber_sweep import main


FIXTURE_CSV = (
    Path(__file__).parent / "examples" / "tiny_locator_fiber_sweep.csv"
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


def write_synthetic_csv(path: Path) -> None:
    rows = [
        {
            "p": 5,
            "n": 4,
            "k": 2,
            "agreement_size": 2,
            "template": "random",
            "seed": 0,
            "supports_checked": 6,
            "fiber_size": 6,
            "fiber_density": 1.0,
            "interpolation_floor": "True",
            "nontrivial_locator_constraint": "False",
            "nontrivial_quotient_orders": "2",
            "quotient_periodic_valid_support_counts": "2:2",
            "status": "EXPERIMENTAL",
            "json_file": "random_a2.json",
        },
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
            "json_file": "monomial_a3.json",
        },
        {
            "p": 5,
            "n": 4,
            "k": 2,
            "agreement_size": 3,
            "template": "random",
            "seed": 0,
            "supports_checked": 4,
            "fiber_size": 1,
            "fiber_density": 0.25,
            "interpolation_floor": "False",
            "nontrivial_locator_constraint": "True",
            "nontrivial_quotient_orders": "2",
            "quotient_periodic_valid_support_counts": "2:0",
            "status": "EXPERIMENTAL",
            "json_file": "random_a3.json",
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
            "json_file": "zero_a3.json",
        },
        {
            "p": 17,
            "n": 16,
            "k": 4,
            "agreement_size": 5,
            "template": "monomial",
            "seed": "null",
            "supports_checked": 4368,
            "fiber_size": 3,
            "fiber_density": 0.0006868131868131869,
            "interpolation_floor": "False",
            "nontrivial_locator_constraint": "True",
            "nontrivial_quotient_orders": "2;4;8",
            "quotient_periodic_valid_support_counts": "2:0;4:1;8:0",
            "status": "EXPERIMENTAL",
            "json_file": "monomial_nonzero.json",
        },
        {
            "p": 7,
            "n": 6,
            "k": 3,
            "agreement_size": 3,
            "template": "random",
            "seed": 0,
            "supports_checked": 20,
            "fiber_size": 19,
            "fiber_density": 0.95,
            "interpolation_floor": "True",
            "nontrivial_locator_constraint": "False",
            "nontrivial_quotient_orders": "2;3",
            "quotient_periodic_valid_support_counts": "2:0;3:0",
            "status": "EXPERIMENTAL",
            "json_file": "floor_violation.json",
        },
        {
            "p": 7,
            "n": 6,
            "k": 3,
            "agreement_size": 4,
            "template": "zero",
            "seed": "null",
            "supports_checked": 15,
            "fiber_size": 14,
            "fiber_density": 0.9333333333333333,
            "interpolation_floor": "False",
            "nontrivial_locator_constraint": "True",
            "nontrivial_quotient_orders": "2;3",
            "quotient_periodic_valid_support_counts": "2:1;3:0",
            "status": "EXPERIMENTAL",
            "json_file": "zero_violation.json",
        },
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path):
    return json.loads(path.read_text())


def read_csv(path: Path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_analyze_locator_fiber_sweep_outputs_reports(tmp_path, capsys):
    sweep_csv = tmp_path / "locator_fiber_sweep.csv"
    write_synthetic_csv(sweep_csv)
    out_dir = tmp_path / "analysis"

    exit_code = main(
        [
            "--csv",
            str(sweep_csv),
            "--out-dir",
            str(out_dir),
            "--top-fibers",
            "3",
        ]
    )

    assert exit_code == 0
    stdout = capsys.readouterr().out
    assert "Locator-fiber sweep analysis (EXPERIMENTAL)" in stdout
    assert "no RS/list-decoding/MCA safety assertion" in stdout
    assert "no theorem status upgrade" in stdout

    assert {
        "locator_fiber_sweep_analysis.csv",
        "locator_fiber_sweep_analysis.md",
        "locator_fiber_sweep_analysis.json",
    } == {path.name for path in out_dir.iterdir()}

    analysis = read_json(out_dir / "locator_fiber_sweep_analysis.json")
    assert analysis["status"] == "EXPERIMENTAL"
    assert "no RS/list-decoding/MCA safety assertion" in analysis["claim"]
    assert analysis["provenance"]["generator"] == (
        "experimental/locator_fiber_sweep_analysis/"
        "analyze_locator_fiber_sweep.py"
    )

    sanity = analysis["sanity_checks"]
    assert len(sanity["interpolation_floor_density_violations"]) == 1
    assert sanity["interpolation_floor_density_violations"][0]["json_file"] == (
        "floor_violation.json"
    )
    assert len(sanity["zero_template_violations"]) == 1
    assert sanity["zero_template_violations"][0]["json_file"] == (
        "zero_violation.json"
    )

    nontrivial = analysis["nontrivial_summary"]
    assert nontrivial["sparse_random_nonzero_fiber_cases"][0]["json_file"] == (
        "random_a3.json"
    )
    assert nontrivial["monomial_cases_with_nonzero_fiber"][0]["json_file"] == (
        "monomial_nonzero.json"
    )
    assert nontrivial["quotient_periodic_valid_support_summaries"][0][
        "json_file"
    ] in {"monomial_nonzero.json", "zero_violation.json"}

    group_rows = read_csv(out_dir / "locator_fiber_sweep_analysis.csv")
    assert len(group_rows) == 7
    random_group = next(
        row
        for row in group_rows
        if row["p"] == "5"
        and row["k"] == "2"
        and row["agreement_size"] == "3"
        and row["template"] == "random"
    )
    assert random_group["seeds"] == "0"
    assert random_group["interpolation_floor"] == "False"
    assert random_group["nontrivial_locator_constraint"] == "True"
    assert random_group["max_fiber_size"] == "1"

    markdown = (out_dir / "locator_fiber_sweep_analysis.md").read_text()
    assert "Experimental data analysis only." in markdown
    assert "Interpolation-Floor Density Violations" in markdown
    assert "Zero-Template Violations" in markdown
    assert "Sparse Random Nonzero Fiber Cases" in markdown
    assert "Quotient-Periodic Valid Support Summaries" in markdown


def test_example_fixture_runs(tmp_path):
    out_dir = tmp_path / "fixture-analysis"

    exit_code = main(
        [
            "--csv",
            str(FIXTURE_CSV),
            "--out-dir",
            str(out_dir),
        ]
    )

    assert exit_code == 0
    analysis = read_json(out_dir / "locator_fiber_sweep_analysis.json")
    assert analysis["status"] == "EXPERIMENTAL"
    assert len(analysis["group_summaries"]) == 4
    assert (
        analysis["nontrivial_summary"]["sparse_random_nonzero_fiber_cases"][0][
            "json_file"
        ]
        == "example_random_a3.json"
    )
