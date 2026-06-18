import json
import subprocess
from pathlib import Path

import pytest

from experimental.locator_fiber_local_packet.run_locator_fiber_local_packet import (
    packet_cases,
    run_packet,
)


def fake_sage_report(command):
    value = {}
    for index, item in enumerate(command):
        if item.startswith("--"):
            value[item] = command[index + 1]
    p = int(value["--p"])
    n = int(value["--n"])
    k = int(value["--k"])
    agreement_size = int(value["--agreement-size"])
    template = value["--template"]
    if p == 5 and template == "monomial":
        fiber_size = 0
    elif p == 5 and template == "zero":
        fiber_size = 4
    else:
        raise AssertionError(f"unexpected fake Sage case: {command}")
    return {
        "schema_version": "sage-locator-fiber-crosscheck-0.1.0",
        "status": "EXPERIMENTAL",
        "claim": "fake test report",
        "inputs": {
            "p": p,
            "n": n,
            "k": k,
            "agreement_size": agreement_size,
            "template": template,
            "seed": int(value["--seed"]),
        },
        "scan": {
            "candidate_supports": 4,
            "supports_tested": 4,
            "fiber_size": fiber_size,
            "fiber_density": fiber_size / 4,
            "interpolation_floor": False,
            "nontrivial_locator_constraint": True,
        },
    }


def fake_command_runner(command, *, cwd, capture_output, text, check):
    assert cwd
    assert capture_output is True
    assert text is True
    assert check is True
    json_out = Path(command[command.index("--json-out") + 1])
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(fake_sage_report(command), indent=2) + "\n")
    return subprocess.CompletedProcess(
        args=command,
        returncode=0,
        stdout="fake sage ok\n",
        stderr="",
    )


def test_packet_cases_are_bounded():
    tiny = packet_cases("tiny")
    selected = packet_cases("selected")
    assert len(tiny) == 2
    assert len(selected) == 3
    assert all(case.p in {5, 17} for case in selected)


def test_run_packet_tiny_with_fake_sage(tmp_path):
    manifest = run_packet(
        out_dir=tmp_path / "packet",
        case_set="tiny",
        max_witnesses=0,
        command_runner=fake_command_runner,
    )

    assert manifest["status"] == "EXPERIMENTAL"
    assert "no RS/list-decoding/MCA safety assertion" in manifest["claim"]
    assert manifest["case_set"] == "tiny"
    assert manifest["python_sweep"]["rows"] == 2
    assert manifest["comparison"]["summary"] == {
        "python_rows": 2,
        "sage_rows": 2,
        "matched_cases": 2,
        "mismatched_cases": 0,
        "python_only_cases": 0,
        "sage_only_cases": 0,
        "all_matched_cases_agree": True,
    }
    packet_dir = Path(manifest["output_directory"])
    assert (packet_dir / "packet_manifest.json").exists()
    assert (packet_dir / "packet.md").exists()
    assert (packet_dir / "python_sweep" / "locator_fiber_sweep.csv").exists()
    assert (
        packet_dir
        / "sage_crosscheck"
        / "sage_locator_fiber_packet.json"
    ).exists()
    assert (
        packet_dir
        / "comparison"
        / "locator_fiber_crosscheck_report.json"
    ).exists()


def test_run_packet_rejects_unknown_case_set(tmp_path):
    with pytest.raises(ValueError):
        run_packet(
            out_dir=tmp_path / "packet",
            case_set="unknown",
            command_runner=fake_command_runner,
        )
