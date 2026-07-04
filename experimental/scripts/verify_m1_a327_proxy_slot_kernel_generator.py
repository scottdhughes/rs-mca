#!/usr/bin/env python3
"""Verify the M1 a=327 proxy-slot kernel generator ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_proxy_slot_kernel_generator.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_proxy_slot_kernel_generator.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "realized exact template vectors for the prescribed coefficients",
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

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong target")
    require(record["source_commit"] == "b51e74d", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "SYNTHETIC_FUNCTIONAL_PROXY_TARGET", "wrong realization status")
    require(record["proof_status"] == "CANDIDATE / PSLOT_PROXY_KERNEL_TARGET / PARTIAL / EXPERIMENTAL", "wrong proof status")

    previous = record["previous_proxy_audit"]
    require(previous["proxy_rank"] == 1450, "wrong previous proxy rank")
    require(previous["proxy_nullity"] == 0, "wrong previous proxy nullity")
    require(previous["best_failure_mode"] == "PZREL_PROXY_FULL_RANK", "wrong previous failure mode")

    search = record["proxy_slot_kernel_search"]
    require(search["systems_tested"] == 216, "wrong systems tested")
    require(search["stable_basis_combinations"] == 23663322, "wrong stable-basis combination count")
    require(search["stable_basis_profiles_tested"] == 12312, "wrong stable-basis profile count")
    require(search["slot_profiles_tested"] == 73872, "wrong slot profile count")
    require(search["zero_row_free_slot_profiles"] == 73872, "wrong zero-row-free count")
    require(search["pair_projection_clear_slot_profiles"] == 42, "wrong pair-projection-clear count")
    require(search["proxy_slot_kernel_targets"] == 42, "wrong target count")
    require(search["best_template_id"] == "sheared_outside_seed_001", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best assignment")
    require(search["best_basis_zero_union_size"] == 10, "wrong basis union")
    require(search["best_forced_pair_count"] == 0, "unexpected forced pair")
    require(search["best_guaranteed_proxy_nullity_lower_bound"] == 253, "wrong proxy nullity lower bound")
    require(search["best_failure_mode"] == "PSLOT_PROXY_KERNEL_TARGET", "wrong best failure mode")

    candidate = record["best_candidate"]
    require(candidate["template_id"] == "sheared_outside_seed_001", "wrong candidate template")
    require(candidate["assignment_strategy"] == "signature_fiber_blocks", "wrong candidate assignment")
    require(candidate["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(candidate["pair7_counts"] == [233, 233, 233, 233, 233], "pair7 mismatch")
    require(candidate["max_pair_count"] == 233, "max pair mismatch")
    require(candidate["functional_classes"] == 27, "wrong functional class count")
    require(candidate["functional_span_rank"] == 6, "wrong functional span rank")
    require(candidate["forced_functional_identities"] == 0, "unexpected forced identity")

    profile = candidate["best_profile"]
    require(profile["source_basis_id"] == "slot_union_10_17_18_23_24_25_26", "wrong source basis")
    require(profile["basis_id"] == "slot_union_10_17_18_23_24_25_26__slot_0", "wrong engineered basis")
    require(profile["basis_class_indices"] == [17, 18, 23, 24, 25, 26], "wrong basis indices")
    require(profile["basis_support_sizes"] == [3, 3, 3, 3, 3, 1], "wrong basis supports")
    require(profile["basis_zero_union_size"] == 10, "wrong basis union")
    require(profile["stable_common_multiplier_dimension"] == 246, "wrong stable dimension")
    require(profile["q_variable_count"] == 1520, "wrong q variable count")
    require(profile["coefficient_matrix_shape"] == [21, 6], "wrong coefficient shape")
    require(profile["coefficient_rank"] == 5, "wrong coefficient rank")
    require(profile["right_kernel_nullity"] == 1, "wrong right-kernel nullity")
    require(profile["right_kernel_verified"] is True, "right kernel not verified")
    require(profile["proxy_kernel_slot"] == 0, "wrong kernel slot")
    require(profile["proxy_kernel_vector"] == [1, 0, 0, 0, 0, 0], "wrong kernel vector")
    require(profile["proxy_kernel_block_degree"] == 253, "wrong block degree")
    require(profile["guaranteed_proxy_nullity_lower_bound"] == 253, "wrong guaranteed nullity")
    require(profile["forced_pair_count"] == 0, "unexpected forced pair")
    require(profile["forced_pairs"] == [], "forced pair list nonempty")

    audit = record["proxy_audit"]
    require(audit["status"] == "PROXY_RANK_PASS", "proxy audit did not pass")
    proxy = audit["proxy_result"]
    require(proxy["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(proxy["proxy_matrix_shape"] == [1761, 1520], "wrong proxy shape")
    require(proxy["proxy_rank"] == 1267, "wrong proxy rank")
    require(proxy["proxy_nullity"] == 253, "wrong proxy nullity")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "proxy matrix shape = `1761 x 1520`",
        "proxy rank/nullity = `1267 / 253`",
        "basis-zero union size = 10",
        "guaranteed proxy nullity lower bound = 253",
        "forced pair count = 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "realization_status": record["realization_status"],
        "proxy_rank": proxy["proxy_rank"],
        "proxy_nullity": proxy["proxy_nullity"],
        "proxy_slot_kernel_targets": search["proxy_slot_kernel_targets"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 proxy-slot kernel generator (status={result['proof_status']})")


if __name__ == "__main__":
    main()
