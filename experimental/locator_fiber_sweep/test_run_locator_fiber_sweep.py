import csv
import json
import math

from experimental.locator_fiber_sweep.run_locator_fiber_sweep import (
    SweepCase,
    analyze_case,
    main,
    run_sweep,
)


def read_json(path):
    return json.loads(path.read_text())


def read_csv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_analyze_case_zero_template_counts_all_supports():
    case = SweepCase(
        p=17,
        n=16,
        k=8,
        agreement_size=9,
        template="zero",
        seed=None,
    )

    report = analyze_case(
        case,
        max_witnesses=2,
        max_supports=20_000,
        parameters={"test": "zero"},
    )

    assert report["status"] == "EXPERIMENTAL"
    assert "no RS/list-decoding/MCA safety assertion" in report["claim"]
    assert report["inputs"]["p"] == 17
    assert report["inputs"]["n"] == 16
    assert report["inputs"]["k"] == 8
    assert report["inputs"]["agreement_size"] == 9
    assert report["domain"]["type"] == "F_p^*"
    assert report["scan"]["candidate_supports"] == math.comb(16, 9)
    assert report["scan"]["supports_tested"] == math.comb(16, 9)
    assert report["scan"]["support_enumeration_complete"] is True
    assert report["scan"]["fiber_size"] == math.comb(16, 9)
    assert report["scan"]["fiber_density"] == 1.0
    assert report["scan"]["interpolation_floor"] is False
    assert report["scan"]["nontrivial_locator_constraint"] is True
    assert "agreement_size <= k" in report["scan"][
        "interpolation_floor_explanation"
    ]
    assert report["quotient_periodic_support_flags"][
        "nontrivial_quotient_orders"
    ] == [2, 4, 8]
    assert len(report["witnesses"]["valid_supports"]) == 2
    assert report["witnesses"]["valid_supports"][0]["polynomial_degree"] is None


def test_analyze_case_monomial_template_has_no_degree_lt_k_supports():
    case = SweepCase(
        p=17,
        n=16,
        k=8,
        agreement_size=9,
        template="monomial",
        seed=None,
    )

    report = analyze_case(
        case,
        max_witnesses=3,
        max_supports=20_000,
        parameters={"test": "monomial"},
    )

    assert report["received_word"]["template"] == "monomial"
    assert report["received_word"]["monomial_degree"] == 8
    assert report["scan"]["candidate_supports"] == math.comb(16, 9)
    assert report["scan"]["fiber_size"] == 0
    assert report["scan"]["fiber_density"] == 0.0
    assert report["witnesses"]["valid_supports"] == []


def test_locator_fiber_sweep_tiny_cli(tmp_path, capsys):
    exit_code = main(
        [
            "--out-dir",
            str(tmp_path),
            "--p",
            "5",
            "--k",
            "2",
            "--agreement-size",
            "2",
            "--agreement-size",
            "3",
            "--template",
            "zero",
            "--template",
            "monomial",
            "--template",
            "random",
            "--seed",
            "0",
            "--max-witnesses",
            "2",
            "--parameter",
            "test_suite=locator_fiber_sweep",
        ]
    )

    assert exit_code == 0
    stdout = capsys.readouterr().out
    assert "Locator-fiber sweep (EXPERIMENTAL)" in stdout
    assert "no RS/list-decoding/MCA safety assertion" in stdout

    expected_files = {
        "locator_fiber_sweep.csv",
        "locator_fiber_sweep.md",
        "locator_fiber_p5_n4_k2_a2_zero.json",
        "locator_fiber_p5_n4_k2_a3_zero.json",
        "locator_fiber_p5_n4_k2_a2_monomial.json",
        "locator_fiber_p5_n4_k2_a3_monomial.json",
        "locator_fiber_p5_n4_k2_a2_random_seed0.json",
        "locator_fiber_p5_n4_k2_a3_random_seed0.json",
    }
    assert expected_files == {path.name for path in tmp_path.iterdir()}

    rows = read_csv(tmp_path / "locator_fiber_sweep.csv")
    assert len(rows) == 6
    assert set(rows[0]) == {
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
    assert {row["status"] for row in rows} == {"EXPERIMENTAL"}
    assert {row["template"] for row in rows} == {"zero", "monomial", "random"}

    zero_a3 = next(
        row
        for row in rows
        if row["template"] == "zero" and row["agreement_size"] == "3"
    )
    assert zero_a3["supports_checked"] == "4"
    assert zero_a3["fiber_size"] == "4"
    assert zero_a3["fiber_density"] == "1.0"
    assert zero_a3["nontrivial_quotient_orders"] == "2"

    monomial_a3_report = read_json(
        tmp_path / "locator_fiber_p5_n4_k2_a3_monomial.json"
    )
    assert monomial_a3_report["scan"]["fiber_size"] == 0
    assert monomial_a3_report["scan"]["interpolation_floor"] is False
    assert monomial_a3_report["scan"]["nontrivial_locator_constraint"] is True
    assert "no RS/list-decoding/MCA safety assertion" in monomial_a3_report[
        "claim"
    ]
    assert monomial_a3_report["provenance"]["parameters"]["test_suite"] == (
        "locator_fiber_sweep"
    )

    random_a2_report = read_json(
        tmp_path / "locator_fiber_p5_n4_k2_a2_random_seed0.json"
    )
    assert random_a2_report["inputs"]["template"] == "random"
    assert random_a2_report["inputs"]["seed"] == 0
    assert random_a2_report["scan"]["interpolation_floor"] is True
    assert random_a2_report["scan"]["nontrivial_locator_constraint"] is False
    assert random_a2_report["scan"]["fiber_size"] == random_a2_report["scan"][
        "supports_tested"
    ]

    markdown = (tmp_path / "locator_fiber_sweep.md").read_text()
    assert "Tiny exhaustive experimental output only." in markdown
    assert "interpolation-floor sanity rows" in markdown
    assert "Nontrivial locator-fiber constraints begin" in markdown
    assert "No RS/list-decoding/MCA safety assertion." in markdown
    assert "No theorem status upgrade." in markdown
    assert "Optional CAS tools are not required" in markdown


def test_locator_fiber_sweep_default_case_count(tmp_path):
    summary = run_sweep(
        tmp_path,
        p_values=(5, 17),
        templates=("zero", "random"),
        seeds=(0, 1),
        max_witnesses=0,
    )

    assert summary["status"] == "EXPERIMENTAL"
    assert len(summary["rows"]) == 27
    assert "no RS/list-decoding/MCA safety assertion" in summary["claim"]
    assert (tmp_path / "locator_fiber_sweep.csv").exists()
    assert (tmp_path / "locator_fiber_sweep.md").exists()
