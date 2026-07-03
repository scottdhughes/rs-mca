#!/usr/bin/env python3
"""Verify the M1 a=327 random-matroid syzygy-rigidity proxy ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_random_matroid_syzygy_rigidity_proxy.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_random_matroid_syzygy_rigidity_proxy.md")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_random_matroid_syzygy_rigidity_proxy.m2")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "global rank rigidity outside the tested proxy front",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    m2_text = M2_SCRIPT_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "c3bb743", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    dep = record["dependency_engineered"]
    require(dep["systems_tested"] == 108, "wrong dependency system count")
    require(dep["proxy_candidates_tested"] == 8, "wrong dependency proxy count")
    require(dep["proxy_basis_profiles_tested"] == 24, "wrong dependency profile count")
    require(dep["proxy_positive_candidates"] == 0, "unexpected dependency positive")
    require(dep["best_template_id"] == "random_matroid_v3_seed_007_m6", "wrong dependency best")
    require(dep["best_proxy_rank"] == 1385, "wrong dependency rank")
    require(dep["best_proxy_nullity"] == 0, "wrong dependency nullity")

    proxy = record["syzygy_proxy"]
    require(proxy["tool"] == "Macaulay2", "wrong tool")
    require(proxy["tool_version"] == "1.26.06", "wrong M2 version")
    require(proxy["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(proxy["template_id"] == "random_matroid_v3_seed_007_m6", "wrong template")
    require(proxy["assignment_strategy"] == "signature_fiber_blocks", "wrong assignment")
    require(proxy["basis_id"] == "deterministic_random_basis_10", "wrong basis")
    require(proxy["functional_classes"] == 47, "wrong functional class count")
    require(proxy["basis_size"] == 6, "wrong basis size")
    require(proxy["nonbasis_constraints"] == 41, "wrong nonbasis count")
    require(proxy["coefficient_matrix_shape"] == [41, 6], "wrong coefficient shape")
    require(proxy["coefficient_rank_python"] == 6, "wrong python coefficient rank")
    require(proxy["right_kernel_nullity_python"] == 0, "wrong python right nullity")
    require(proxy["left_syzygy_dimension_python"] == 35, "wrong python left syzygy dimension")
    require(proxy["quotient_matrix_shape"] == [1626, 1385], "wrong quotient shape")
    require(proxy["quotient_proxy_rank"] == 1385, "wrong quotient rank")
    require(proxy["quotient_proxy_nullity"] == 0, "wrong quotient nullity")
    require(proxy["best_failure_mode"] == "SYZYGY_PROXY_COEFFICIENT_FULL_RANK_QUOTIENT_FULL_RANK", "wrong failure")

    m2 = proxy["m2_result"]
    require(m2["returncode"] == 0, "M2 did not pass")
    parsed = m2["parsed"]
    require(parsed["M2_COEFF_ROWS"] == 41, "M2 row mismatch")
    require(parsed["M2_COEFF_COLS"] == 6, "M2 col mismatch")
    require(parsed["M2_COEFF_RANK"] == 6, "M2 rank mismatch")
    require(parsed["M2_RIGHT_KERNEL_GENS"] == 0, "M2 right kernel mismatch")
    require(parsed["M2_LEFT_SYZYGY_GENS"] == 35, "M2 left syzygy gens mismatch")
    require(parsed["M2_LEFT_SYZYGY_RANK"] == 35, "M2 left syzygy rank mismatch")
    require("Coeff = matrix" in m2_text, "M2 script missing matrix")
    require("M2_RIGHT_KERNEL_GENS" in m2_text, "M2 script missing right kernel line")

    for phrase in [
        "Macaulay2",
        "41 x 6",
        "right kernel = 0",
        "left syzygy dimension = 35",
        "1626 x 1385",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "coefficient_rank": proxy["coefficient_rank_python"],
        "right_kernel_nullity": proxy["right_kernel_nullity_python"],
        "left_syzygy_dimension": proxy["left_syzygy_dimension_python"],
        "quotient_proxy_nullity": proxy["quotient_proxy_nullity"],
        "best_failure_mode": proxy["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 random-matroid syzygy-rigidity proxy (status={result['proof_status']})")


if __name__ == "__main__":
    main()
