import json
import shutil
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SAGE_SCRIPT = (
    REPO_ROOT
    / "experimental"
    / "sage_locator_fiber_crosscheck"
    / "sage_locator_fiber_crosscheck.sage"
)
README = (
    REPO_ROOT / "experimental" / "sage_locator_fiber_crosscheck" / "README.md"
)


def test_sage_locator_crosscheck_metadata_documents_optional_status():
    script = SAGE_SCRIPT.read_text()
    readme = README.read_text()
    normalized_readme = " ".join(readme.split())

    assert "no RS/list-decoding/MCA safety assertion" in script
    assert "does not upgrade any theorem status" in readme
    assert "Sage is not part of the core Python requirements" in readme
    assert "independent verification aids" in normalized_readme
    assert "Status: EXPERIMENTAL" in readme


def test_sage_locator_crosscheck_tiny_smoke_if_sage_is_available(tmp_path):
    sage = shutil.which("sage")
    if sage is None:
        pytest.skip("sage is not present on PATH")

    out = tmp_path / "sage_locator_crosscheck.json"
    result = subprocess.run(
        [
            sage,
            "-python",
            str(SAGE_SCRIPT),
            "--p",
            "5",
            "--n",
            "4",
            "--k",
            "2",
            "--agreement-size",
            "3",
            "--template",
            "monomial",
            "--max-witnesses",
            "2",
            "--json-out",
            str(out),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    report = json.loads(out.read_text())

    assert "Sage locator-fiber cross-check (EXPERIMENTAL)" in result.stdout
    assert "no RS/list-decoding/MCA safety assertion" in result.stdout
    assert report["status"] == "EXPERIMENTAL"
    assert report["inputs"]["p"] == 5
    assert report["inputs"]["n"] == 4
    assert report["inputs"]["k"] == 2
    assert report["inputs"]["agreement_size"] == 3
    assert report["inputs"]["template"] == "monomial"
    assert report["scan"]["supports_tested"] == 4
    assert report["scan"]["fiber_size"] == 0
    assert report["scan"]["nontrivial_locator_constraint"] is True
    assert report["source_comparison"]["python_pipeline_case_id"] == (
        "locator_fiber_p5_n4_k2_a3_monomial"
    )


def test_sage_locator_crosscheck_selected_if_sage_is_available(tmp_path):
    sage = shutil.which("sage")
    if sage is None:
        pytest.skip("sage is not present on PATH")

    out = tmp_path / "sage_locator_selected.json"
    subprocess.run(
        [
            sage,
            "-python",
            str(SAGE_SCRIPT),
            "--preset",
            "selected",
            "--max-witnesses",
            "0",
            "--json-out",
            str(out),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    report = json.loads(out.read_text())
    assert report["status"] == "EXPERIMENTAL"
    assert report["preset"] == "selected"
    assert len(report["reports"]) == 3
    fibers = {
        item["source_comparison"]["python_pipeline_case_id"]: item["scan"][
            "fiber_size"
        ]
        for item in report["reports"]
    }
    assert fibers["locator_fiber_p5_n4_k2_a3_monomial"] == 0
    assert fibers["locator_fiber_p5_n4_k2_a3_zero"] == 4
    assert fibers["locator_fiber_p17_n16_k8_a9_monomial"] == 0
