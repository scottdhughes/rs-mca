#!/usr/bin/env sage
"""Independent finite-field replay of the Q0 co-support adapter."""

from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = (
    ROOT
    / "experimental/data/certificates/m1-kb-branch3-5-mask-contract-v1/"
      "m1_kb_branch3_5_mask_contract_v1.json"
)

F = GF(17)
omega = F.multiplicative_generator()
n = 16
j = 7
D = [omega^index for index in range(n)]
require(len(set(D)) == n, "cyclic domain collision")

R = PolynomialRing(F, "X")
X = R.gen()


def decompose(indices, c):
    points = set(indices)
    require(len(points) == j, "co-support size drift")
    n_c = n // c
    j_c, r_c = divmod(j, c)
    full = []
    covered = set()
    for residue in range(n_c):
        fibre = {residue + lift * n_c for lift in range(c)}
        field_fibre = {
            index for index in range(n)
            if D[index]^c == D[residue]^c
        }
        require(fibre == field_fibre, "exponent fibre disagrees with power map")
        if fibre.issubset(points):
            full.append(residue)
            covered.update(fibre)
    leftover = sorted(points - covered)
    qualifies = len(full) == j_c and len(leftover) == r_c
    return qualifies, full, leftover


def locator(indices):
    return prod(X - D[index] for index in indices)


def check_factorization(indices, c):
    qualifies, full, leftover = decompose(indices, c)
    if not qualifies:
        return False
    quotient_composed = prod(X^c - D[residue]^c for residue in full)
    require(
        locator(indices) == locator(leftover) * quotient_composed,
        "Q0 locator factorization failed",
    )
    return True


def branch4_route_eligible(indices, c):
    qualifies, _, _ = decompose(indices, c)
    return qualifies and j // c >= 1


certificate = json.loads(CERT_PATH.read_text(encoding="utf-8"))
toy = certificate["toy_controls"]
require(toy["row"] == {"j": 7, "n": 16, "ordered_rungs": [2, 4, 8, 16]},
        "certificate toy row drift")

overlap = toy["co_supports"]["overlap_c2_c4"]
c4_only = toy["co_supports"]["c4_only"]
neither = toy["co_supports"]["neither"]

require(check_factorization(overlap, 2), "overlap lost c=2 membership")
require(check_factorization(overlap, 4), "overlap lost c=4 membership")
require(not decompose(c4_only, 2)[0], "c4-only support gained c=2 membership")
require(check_factorization(c4_only, 4), "c4-only support lost c=4 membership")
require(not decompose(neither, 2)[0], "negative support gained c=2 membership")
require(not decompose(neither, 4)[0], "negative support gained c=4 membership")
require(check_factorization(neither, 8), "zero-core c=8 membership lost")
require(check_factorization(neither, 16), "zero-core c=16 membership lost")
require(not branch4_route_eligible(neither, 8),
        "zero-core c=8 entered branch 4")
require(not branch4_route_eligible(neither, 16),
        "zero-core c=16 entered branch 4")

assignments = toy["q0"]["slope_projection_assignments"]
require(assignments == {"17": 2, "19": 4}, "certificate slope projection drift")
require(toy["q0"]["first_witness_only_classifier_would_be_wrong_for_slope"] == 17,
        "witness-order guard drift")
require(toy["witness_projection"]["deep_slope_projection"] == [11],
        "deep existential projection drift")
require(toy["selector_quantifiers"]["mixed_result"]["owner_eligible"] is True,
        "selector existential gate drift")
require(toy["selector_quantifiers"]["all_high_result"]
        ["universal_complement_certified"] is True,
        "selector universal complement drift")
require(toy["selector_quantifiers"]["incomplete_high_result"]
        ["universal_complement_certified"] is False,
        "incomplete selector universe certified a complement")

payload = {
    "schema": "rs-mca-m1-kb-branch3-5-mask-contract-v1-sage-control",
    "status": "PASS",
    "field": "GF(17)",
    "domain_order": n,
    "co_support_size": j,
    "checked_power_map_rungs": [2, 4, 8, 16],
    "overlap_first_rung": 2,
    "c4_only_first_rung": 4,
    "negative_has_rung": False,
    "zero_core_raw_membership": [8, 16],
    "zero_core_branch4_eligible": [],
    "locator_factorizations_checked": 5,
    "scope": "TOY_SEMANTIC_REPLAY_ONLY",
}
print(json.dumps(payload, sort_keys=True, default=int))
