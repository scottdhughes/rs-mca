#!/usr/bin/env python3
"""Verifier for the M1 a=327 all-pair multi-prime sieve."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_allpair_multiprime_sieve.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_allpair_multiprime_sieve_exact_audit.json")

TARGET_AGREEMENT = 327
EXPECTED_PRIMES = [
    7681,
    10753,
    11777,
    12289,
    13313,
    15361,
    17921,
    18433,
    19457,
    23041,
    25601,
    26113,
    32257,
    36353,
    37889,
    39937,
    40961,
    45569,
    50177,
    51713,
    58369,
    59393,
    61441,
]
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_scan(record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["construction_mode"] == "allpair_multiprime_sieve", "wrong construction mode")
    require(record["prime_source"] == "PARI/GP first primes p == 1 mod 512", "wrong prime source")
    require(record["proxy_primes"] == EXPECTED_PRIMES, "wrong prime list")
    require(record["proxy_prime_count"] == len(EXPECTED_PRIMES), "wrong prime count")
    require(all((prime - 1) % 512 == 0 for prime in record["proxy_primes"]), "prime not 1 mod 512")
    require(record["candidate_count"] == 515, "wrong candidate count")
    require(record["deterministic_embedding_count"] == 3, "wrong deterministic embedding count")
    require(record["random_embedding_count"] == 512, "wrong random embedding count")
    require(record["rank_evaluation_count"] == 515 * len(EXPECTED_PRIMES), "wrong rank evaluation count")
    require(record["anomaly_count"] == 0, "unexpected anomaly")
    require(record["rank_anomaly_count"] == 0, "unexpected rank anomaly")
    require(record["capacity_anomaly_count"] == 0, "unexpected capacity anomaly")
    require(record["exact_audit_triggers"] == [], "unexpected exact audit trigger")
    require(record["proof_status"] == "TESTED_EMBEDDINGS_NO_MULTIPRIME_PROXY_ANOMALY", "wrong proof status")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing scan non-claims")
    for row in record["results"]:
        require(row["rank_histogram"] == {"6": len(EXPECTED_PRIMES)}, "non-full rank histogram")
        require(row["min_rank"] == 6, "min rank below full")
        require(row["max_nullity"] == 0, "positive nullity found")
        require(row["singular_prime_count"] == 0, "singular prime found")
        require(row["capacity_anomaly_count"] == 0, "capacity anomaly found")
        require(row["status"] == "MULTIPRIME_PROXY_FULL_RANK", "wrong row status")
        require(row["anomaly_prime_records"] == [], "unexpected anomaly prime record")
        require("prime_rank_profile_hash" in row, "missing prime rank profile hash")
        require("prime_pivot_profile_hash" in row, "missing prime pivot profile hash")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong agreement target")
    require(exact["construction_mode"] == "allpair_multiprime_sieve_exact_audit", "exact wrong mode")
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proof_status"] == scan["proof_status"], "source status mismatch")
    require(exact["source"]["source_candidate_count"] == scan["candidate_count"], "source candidate mismatch")
    require(exact["source"]["source_rank_evaluation_count"] == scan["rank_evaluation_count"], "source rank count mismatch")
    require(exact["source"]["source_anomaly_count"] == scan["anomaly_count"] == 0, "source anomaly mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["degree_bound"] == 256, "wrong degree bound")
    require(exact["exact_trigger_count"] == 0, "unexpected exact trigger count")
    require(exact["exact_audited_count"] == 0, "unexpected exact audit count")
    require(exact["exact_full_rank_count"] == 0, "unexpected exact full-rank count")
    require(exact["exact_positive_nullity_count"] == 0, "unexpected exact positive nullity")
    require(exact["results"] == [], "unexpected exact results")
    require(exact["proof_status"] == "NO_EXACT_AUDIT_TRIGGERED", "wrong exact proof status")
    require(exact["mca_counted"] is False, "exact MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "missing exact non-claims")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    verify_scan(scan)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "candidate_count": scan["candidate_count"],
        "proxy_prime_count": scan["proxy_prime_count"],
        "rank_evaluation_count": scan["rank_evaluation_count"],
        "anomaly_count": scan["anomaly_count"],
        "exact_trigger_count": exact["exact_trigger_count"],
        "proof_status": scan["proof_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "PASS: M1 a=327 all-pair multi-prime sieve "
            f"({result['rank_evaluation_count']} rank evaluations, anomalies={result['anomaly_count']})"
        )


if __name__ == "__main__":
    main()
