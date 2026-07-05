#!/usr/bin/env sage
"""Exact rank-2 mu_8 carrier menu, interpolation, and witness audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
H_ORDER = 512
MU_ORDER = 8
QUOTIENT_ORDER = 64
QUOTIENT_DEGREE_BOUND = 32
DEGREE_BOUND = 256
TARGET_AGREEMENT = 327
LIST_SIZE = 7
PAIR_CAP = 255

MENU_INPUT = Path("experimental/data/m1_a327_mu8_rank2_carrier_menu_scan.json")
SCHEDULE_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_carrier_schedule_candidates.json")
EXACT_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_carrier_exact_interpolation.json")
WITNESS_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_exact_witness_audit.json")

NOT_CLAIMED = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
]


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return str(payload)


def hash_payload(payload):
    return hashlib.sha256(
        json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def exact_field():
    return GF(Integer(P) ** FIELD_DEGREE, name="z")


def load_menu():
    with MENU_INPUT.open() as handle:
        return json.load(handle)


def pair_labels():
    return [(left, right) for left in range(LIST_SIZE) for right in range(left + 1, LIST_SIZE)]


PAIR_LABELS = pair_labels()
PAIR_INDEX = {pair: idx for idx, pair in enumerate(PAIR_LABELS)}


def vector_from_ints(F, values):
    return [F(Integer(value)) for value in values]


def canonical_ratio(a, b):
    F = a.parent()
    if a == 0 and b == 0:
        return None
    if a != 0:
        scale = F(1) / a
        return (F(1), b * scale)
    return (F(0), F(1))


def ratio_key(ratio):
    if ratio is None:
        return "NONE"
    return "%s|%s" % (str(ratio[0]), str(ratio[1]))


def value_for_label(u, v, ratio, rep, gamma, phase, label):
    a, b = ratio
    x = rep * (gamma ** phase)
    total = rep.parent()(0)
    for ridx, residue in enumerate(range(1, MU_ORDER)):
        coeff = a * u[ridx] + b * v[ridx]
        total += coeff * (gamma ** (label * residue)) * (x ** residue)
    return total


def partition_labels(values):
    blocks = []
    used = set()
    for label, value in enumerate(values):
        if label in used:
            continue
        block = [other for other, other_value in enumerate(values) if other_value == value]
        used.update(block)
        blocks.append(block)
    blocks.sort(key=lambda block: (-len(block), block))
    return blocks


def pair_value(u, v, ratio, rep, gamma, phase, left, right):
    a, b = ratio
    x = rep * (gamma ** phase)
    total = rep.parent()(0)
    for ridx, residue in enumerate(range(1, MU_ORDER)):
        coeff = a * u[ridx] + b * v[ridx]
        total += coeff * (gamma ** (left * residue) - gamma ** (right * residue)) * (x ** residue)
    return total


def ratio_candidates_for_qidx(u, v, rep, gamma, limit):
    ratios = {}
    for phase in range(MU_ORDER):
        x = rep * (gamma ** phase)
        for left, right in PAIR_LABELS:
            gu = rep.parent()(0)
            gv = rep.parent()(0)
            for ridx, residue in enumerate(range(1, MU_ORDER)):
                factor = (gamma ** (left * residue) - gamma ** (right * residue)) * (x ** residue)
                gu += u[ridx] * factor
                gv += v[ridx] * factor
            ratio = canonical_ratio(-gv, gu)
            if ratio is None:
                continue
            key = ratio_key(ratio)
            ratios[key] = ratio
    ordered = sorted(ratios.values(), key=ratio_key)
    return ordered[:limit]


def empty_counts():
    return [0 for _ in range(LIST_SIZE)], [0 for _ in PAIR_LABELS]


def counts_for_blocks(blocks_by_phase):
    inc, pairs = empty_counts()
    for block in blocks_by_phase:
        for label in block:
            inc[label] += 1
        for left, right in combinations(block, 2):
            pairs[PAIR_INDEX[(left, right)]] += 1
    return inc, pairs


def option_total(option):
    return sum(option["incidence"])


def make_option(option_id, kind, rows, ratio, blocks_by_phase):
    inc, pairs = counts_for_blocks(blocks_by_phase)
    return {
        "option_id": option_id,
        "kind": kind,
        "rows": rows,
        "ratio": ratio,
        "blocks_by_phase": blocks_by_phase,
        "incidence": inc,
        "pair_counts": pairs,
        "total_incidence": sum(inc),
        "max_pair_count": max(pairs) if pairs else 0,
    }


def zero_options():
    options = []
    all_labels = list(range(LIST_SIZE))
    zero_patterns = [all_labels]
    for size in [6, 5]:
        for start in range(LIST_SIZE):
            block = sorted(((start + offset) % LIST_SIZE for offset in range(size)))
            zero_patterns.append(block)
    seen = set()
    for idx, block in enumerate(zero_patterns):
        key = tuple(block)
        if key in seen:
            continue
        seen.add(key)
        blocks = [block[:] for _ in range(MU_ORDER)]
        options.append(make_option("ZERO_%02d" % idx, "ZERO", 2, None, blocks))
    return options


def free_options():
    options = []
    for shift in range(LIST_SIZE):
        blocks = [[(phase + shift) % LIST_SIZE] for phase in range(MU_ORDER)]
        options.append(make_option("FREE_%d" % shift, "FREE", 0, None, blocks))
    return options


def ratio_option(u, v, rep, gamma, ratio, idx):
    blocks = []
    for phase in range(MU_ORDER):
        values = [value_for_label(u, v, ratio, rep, gamma, phase, label) for label in range(LIST_SIZE)]
        partition = partition_labels(values)
        blocks.append(partition[0])
    return make_option("RATIO_%03d" % idx, "RATIO", 1, ratio, blocks)


def build_menus_for_plane(F, omega, gamma, plane, ratio_limit):
    u = vector_from_ints(F, plane["u"])
    v = vector_from_ints(F, plane["v"])
    menus = []
    for qidx in range(QUOTIENT_ORDER):
        rep = omega ** qidx
        options = []
        options.extend(zero_options())
        ratios = ratio_candidates_for_qidx(u, v, rep, gamma, ratio_limit)
        for idx, ratio in enumerate(ratios):
            option = ratio_option(u, v, rep, gamma, ratio, idx)
            if option["total_incidence"] > MU_ORDER:
                options.append(option)
        options.extend(free_options())
        deduped = []
        seen = set()
        for option in sorted(options, key=lambda row: (-row["total_incidence"], row["rows"], row["option_id"])):
            key = (
                option["kind"],
                tuple(option["incidence"]),
                tuple(option["pair_counts"]),
                tuple(tuple(block) for block in option["blocks_by_phase"]),
                ratio_key(option["ratio"]),
            )
            if key in seen:
                continue
            seen.add(key)
            deduped.append(option)
        menus.append({"qidx": qidx, "options": deduped[: max(24, ratio_limit + 16)]})
    return menus


def add_counts(left, right):
    return [a + b for a, b in zip(left, right)]


def counts_within_cap(left, right, cap):
    return all(a + b <= cap for a, b in zip(left, right))


def schedule_score(option, support, pair_counts):
    need = [max(0, TARGET_AGREEMENT - value) for value in support]
    support_gain = sum(need[idx] * option["incidence"][idx] for idx in range(LIST_SIZE))
    total_gain = 4 * option["total_incidence"]
    row_penalty = 8 * option["rows"]
    pair_penalty = 0
    for idx, value in enumerate(option["pair_counts"]):
        projected = pair_counts[idx] + value
        if projected > PAIR_CAP:
            pair_penalty += 100000
        elif projected > 220:
            pair_penalty += 80 * (projected - 220) * (projected - 220)
    return support_gain + total_gain - row_penalty - pair_penalty


def choose_schedule_for_plane(plane, menus):
    best = None
    best_nonzero = [
        max((option_total(opt) for opt in row["options"] if opt["kind"] != "ZERO"), default=0)
        for row in menus
    ]
    order_by_low_nonzero = sorted(range(QUOTIENT_ORDER), key=lambda qidx: (best_nonzero[qidx], qidx))
    for zero_count in range(18, 49):
        zero_set = set(order_by_low_nonzero[:zero_count])
        support = [0 for _ in range(LIST_SIZE)]
        pair_counts = [0 for _ in PAIR_LABELS]
        choices = [None for _ in range(QUOTIENT_ORDER)]
        feasible = True
        for qidx in sorted(zero_set):
            zero_candidates = [opt for opt in menus[qidx]["options"] if opt["kind"] == "ZERO"]
            zero_candidates.sort(
                key=lambda opt: (
                    -schedule_score(opt, support, pair_counts),
                    max(opt["pair_counts"]),
                    opt["option_id"],
                )
            )
            chosen = None
            for option in zero_candidates:
                if counts_within_cap(pair_counts, option["pair_counts"], PAIR_CAP):
                    chosen = option
                    break
            if chosen is None:
                feasible = False
                break
            support = add_counts(support, chosen["incidence"])
            pair_counts = add_counts(pair_counts, chosen["pair_counts"])
            choices[qidx] = chosen
        if not feasible:
            continue
        remaining = [qidx for qidx in range(QUOTIENT_ORDER) if qidx not in zero_set]
        remaining.sort(key=lambda qidx: (-best_nonzero[qidx], qidx))
        for qidx in remaining:
            candidates = [opt for opt in menus[qidx]["options"] if opt["kind"] != "ZERO"]
            candidates = [opt for opt in candidates if counts_within_cap(pair_counts, opt["pair_counts"], PAIR_CAP)]
            if not candidates:
                candidates = [opt for opt in menus[qidx]["options"] if opt["kind"] == "FREE"]
            chosen = max(candidates, key=lambda opt: schedule_score(opt, support, pair_counts))
            support = add_counts(support, chosen["incidence"])
            pair_counts = add_counts(pair_counts, chosen["pair_counts"])
            choices[qidx] = chosen
        for _ in range(2):
            improved = False
            for qidx in remaining:
                current = choices[qidx]
                base_support = [support[i] - current["incidence"][i] for i in range(LIST_SIZE)]
                base_pairs = [pair_counts[i] - current["pair_counts"][i] for i in range(len(PAIR_LABELS))]
                candidates = [
                    opt for opt in menus[qidx]["options"]
                    if opt["kind"] != "ZERO" and counts_within_cap(base_pairs, opt["pair_counts"], PAIR_CAP)
                ]
                if not candidates:
                    continue
                replacement = max(candidates, key=lambda opt: schedule_score(opt, base_support, base_pairs))
                old_min = min(support)
                new_support = add_counts(base_support, replacement["incidence"])
                if min(new_support) > old_min or (min(new_support) == old_min and sum(new_support) > sum(support)):
                    choices[qidx] = replacement
                    support = new_support
                    pair_counts = add_counts(base_pairs, replacement["pair_counts"])
                    improved = True
            if not improved:
                break
        candidate = {
            "candidate_id": "%s_z%02d" % (plane["plane_id"], zero_count),
            "plane_id": plane["plane_id"],
            "support_vector": support,
            "min_support": min(support),
            "pair_count_max": max(pair_counts) if pair_counts else 0,
            "pair_counts": pair_counts,
            "selected_incidence_total": sum(support),
            "zero_count": zero_count,
            "interpolation_rows": sum(choice["rows"] for choice in choices),
            "choices": choices,
        }
        passes = (
            candidate["min_support"] >= TARGET_AGREEMENT
            and candidate["selected_incidence_total"] >= LIST_SIZE * TARGET_AGREEMENT
            and candidate["pair_count_max"] <= PAIR_CAP
        )
        candidate["guard_pass"] = passes
        if best is None or (
            passes,
            candidate["min_support"],
            candidate["selected_incidence_total"],
            -candidate["pair_count_max"],
            -candidate["interpolation_rows"],
        ) > (
            best["guard_pass"],
            best["min_support"],
            best["selected_incidence_total"],
            -best["pair_count_max"],
            -best["interpolation_rows"],
        ):
            best = candidate
    return best


def serialize_choice(choice):
    return {
        "option_id": choice["option_id"],
        "kind": choice["kind"],
        "rows": choice["rows"],
        "ratio": None if choice["ratio"] is None else [str(choice["ratio"][0]), str(choice["ratio"][1])],
        "blocks_by_phase": choice["blocks_by_phase"],
        "incidence": choice["incidence"],
        "pair_counts": choice["pair_counts"],
        "total_incidence": choice["total_incidence"],
    }


def serialize_candidate(candidate):
    row = dict(candidate)
    row["choices"] = [serialize_choice(choice) for choice in candidate["choices"]]
    row["choices_hash"] = hash_payload(row["choices"])
    return row


def interpolation_rows(F, omega, candidate):
    rows = []
    metadata = []
    for qidx, choice in enumerate(candidate["choices"]):
        y = omega ** (MU_ORDER * qidx)
        powers = [y ** power for power in range(QUOTIENT_DEGREE_BOUND)]
        if choice["kind"] == "ZERO":
            rows.append(powers + [F(0) for _ in range(QUOTIENT_DEGREE_BOUND)])
            rows.append([F(0) for _ in range(QUOTIENT_DEGREE_BOUND)] + powers)
            metadata.extend([{"qidx": qidx, "kind": "ZERO_F"}, {"qidx": qidx, "kind": "ZERO_G"}])
        elif choice["kind"] == "RATIO":
            a, b = choice["ratio"]
            rows.append([b * value for value in powers] + [-a * value for value in powers])
            metadata.append({"qidx": qidx, "kind": "RATIO", "ratio": ratio_key(choice["ratio"])})
    return rows, metadata


def pair_map_vector(vec, u, v, gamma, left, right):
    F = gamma.parent()
    out = [F(0) for _ in range(DEGREE_BOUND)]
    f_coeffs = vec[:QUOTIENT_DEGREE_BOUND]
    g_coeffs = vec[QUOTIENT_DEGREE_BOUND:]
    for ridx, residue in enumerate(range(1, MU_ORDER)):
        phase = gamma ** (left * residue) - gamma ** (right * residue)
        for power in range(QUOTIENT_DEGREE_BOUND):
            coeff = (u[ridx] * f_coeffs[power] + v[ridx] * g_coeffs[power]) * phase
            out[residue + MU_ORDER * power] += coeff
    return out


def classify_kernel(kernel_basis, u, v, gamma):
    forced = []
    for left, right in PAIR_LABELS:
        if all(not any(pair_map_vector(vec, u, v, gamma, left, right)) for vec in kernel_basis):
            forced.append([left + 1, right + 1])
    if not forced:
        status = "MU8_RANK2_CARRIER_PAIR_VISIBLE"
    elif len(forced) == len(PAIR_LABELS):
        status = "MU8_RANK2_CARRIER_PAIR_FORCED"
    else:
        status = "MU8_RANK2_CARRIER_MIXED_PAIR_FORCED"
    return status, forced


def deterministic_avoidance(kernel_basis, u, v, gamma):
    if not kernel_basis:
        return None
    F = gamma.parent()
    x = None
    processed = []
    scalars = [F(i) for i in range(P)]
    z = F.gen()
    scalars.extend(z ** exp for exp in range(1, 96))
    for left, right in PAIR_LABELS:
        if x is not None and any(pair_map_vector(x, u, v, gamma, left, right)):
            processed.append((left, right))
            continue
        y = None
        for basis_vec in kernel_basis:
            if any(pair_map_vector(basis_vec, u, v, gamma, left, right)):
                y = basis_vec
                break
        if y is None:
            return None
        if x is None:
            x = F(0) * y
        forbidden = {F(0)}
        for prev_left, prev_right in processed:
            ux = pair_map_vector(x, u, v, gamma, prev_left, prev_right)
            uy = pair_map_vector(y, u, v, gamma, prev_left, prev_right)
            pivot = None
            for idx, value in enumerate(uy):
                if value != 0:
                    pivot = idx
                    break
            if pivot is None:
                continue
            a0 = -ux[pivot] / uy[pivot]
            if all(ux[idx] + a0 * uy[idx] == 0 for idx in range(len(ux))):
                forbidden.add(a0)
        chosen = None
        for scalar in scalars:
            if scalar not in forbidden:
                chosen = scalar
                break
        if chosen is None:
            return None
        x = x + chosen * y
        processed.append((left, right))
    return x


def p_eval(vec, u, v, omega, gamma, label, point):
    y = point ** MU_ORDER
    f_coeffs = vec[:QUOTIENT_DEGREE_BOUND]
    g_coeffs = vec[QUOTIENT_DEGREE_BOUND:]
    F = point.parent()
    f_value = F(0)
    g_value = F(0)
    for power in range(QUOTIENT_DEGREE_BOUND):
        f_value += f_coeffs[power] * (y ** power)
        g_value += g_coeffs[power] * (y ** power)
    total = F(0)
    for ridx, residue in enumerate(range(1, MU_ORDER)):
        total += (u[ridx] * f_value + v[ridx] * g_value) * (gamma ** (label * residue)) * (point ** residue)
    return total


def verify_witness(vec, candidate, u, v, omega, gamma):
    points = []
    received = []
    raw_rows_ok = True
    for qidx, choice in enumerate(candidate["choices"]):
        rep = omega ** qidx
        for phase, block in enumerate(choice["blocks_by_phase"]):
            point = rep * (gamma ** phase)
            anchor = block[0]
            value = p_eval(vec, u, v, omega, gamma, anchor, point)
            points.append(point)
            received.append(value)
            for label in block:
                if p_eval(vec, u, v, omega, gamma, label, point) != value:
                    raw_rows_ok = False
    agreements = []
    for label in range(LIST_SIZE):
        count = 0
        for point, value in zip(points, received, strict=True):
            if p_eval(vec, u, v, omega, gamma, label, point) == value:
                count += 1
        agreements.append(count)
    pair_agreements = {}
    for left, right in PAIR_LABELS:
        count = 0
        for point in points:
            if p_eval(vec, u, v, omega, gamma, left, point) == p_eval(vec, u, v, omega, gamma, right, point):
                count += 1
        pair_agreements["P%d%d" % (left + 1, right + 1)] = count
    return {
        "constructed": True,
        "raw_selected_class_rows_ok": raw_rows_ok,
        "agreement_vector": agreements,
        "min_agreement": min(agreements),
        "pair_agreement_max": max(pair_agreements.values()),
        "seven_distinct": all(value <= DEGREE_BOUND - 1 for value in pair_agreements.values()),
        "pair_agreements": pair_agreements,
        "vector_hash": hash_payload([str(value) for value in vec]),
    }


def audit(plane_limit, candidate_limit, ratio_limit):
    menu = load_menu()
    F = exact_field()
    gen = F.multiplicative_generator()
    omega = gen ** ((F.order() - 1) // H_ORDER)
    gamma = omega ** (H_ORDER // MU_ORDER)
    planes = menu["carrier_planes"][:plane_limit]
    schedule_rows = []
    exact_rows = []
    witness = None
    for plane in planes:
        menus = build_menus_for_plane(F, omega, gamma, plane, ratio_limit)
        candidate = choose_schedule_for_plane(plane, menus)
        if candidate is None:
            continue
        serialized = serialize_candidate(candidate)
        schedule_rows.append(serialized)
        if not candidate["guard_pass"]:
            continue
        u = vector_from_ints(F, plane["u"])
        v = vector_from_ints(F, plane["v"])
        rows, metadata = interpolation_rows(F, omega, candidate)
        matrix = Matrix(F, rows) if rows else Matrix(F, 0, 64)
        rank = int(matrix.rank())
        nullity = int(matrix.ncols() - rank)
        status = "MU8_RANK2_CARRIER_INTERPOLATION_FULL_RANK"
        forced_pairs = []
        if nullity > 0:
            kernel_basis = matrix.right_kernel().basis()
            status, forced_pairs = classify_kernel(kernel_basis, u, v, gamma)
            if status == "MU8_RANK2_CARRIER_PAIR_VISIBLE" and witness is None:
                vec = deterministic_avoidance(kernel_basis, u, v, gamma)
                if vec is not None:
                    audit_row = verify_witness(vec, candidate, u, v, omega, gamma)
                    audit_row["candidate_id"] = candidate["candidate_id"]
                    audit_row["plane_id"] = plane["plane_id"]
                    witness = audit_row
        exact_rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "plane_id": plane["plane_id"],
                "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
                "rank": rank,
                "nullity": nullity,
                "forced_equal_pairs": forced_pairs,
                "row_metadata_hash": hash_payload(metadata),
                "status": status,
            }
        )
        if len(exact_rows) >= candidate_limit:
            break
    candidate_passes = [row for row in schedule_rows if row["guard_pass"]]
    exact_positive = [row for row in exact_rows if row["nullity"] > 0]
    schedule_status = (
        "CANDIDATE / MU8_RANK2_CARRIER_SCHEDULE_GUARD_PASS / PARTIAL / EXPERIMENTAL"
        if candidate_passes
        else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_GUARD_PASS / PARTIAL / EXPERIMENTAL"
    )
    exact_status = (
        "CANDIDATE / MU8_RANK2_CARRIER_INTERPOLATION_NULLITY / PARTIAL / EXPERIMENTAL"
        if exact_positive
        else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_INTERPOLATION_FULL_RANK / PARTIAL / EXPERIMENTAL"
        if exact_rows
        else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE / PARTIAL / EXPERIMENTAL"
    )
    witness_pass = (
        witness is not None
        and witness["seven_distinct"]
        and witness["raw_selected_class_rows_ok"]
        and witness["min_agreement"] >= TARGET_AGREEMENT
    )
    schedule_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "83c6f93",
        "schedule_candidates": {
            "planes_audited": len(planes),
            "constructed": len(schedule_rows),
            "guard_passing": len(candidate_passes),
            "selected_for_exact_interpolation": len(exact_rows),
            "best_min_support": max([row["min_support"] for row in schedule_rows], default=None),
            "best_selected_incidence_total": max([row["selected_incidence_total"] for row in schedule_rows], default=None),
            "best_failure_mode": "MU8_RANK2_CARRIER_SCHEDULE_GUARD_PASS" if candidate_passes else "MU8_RANK2_CARRIER_NO_GUARD_PASS",
        },
        "candidates": schedule_rows[:candidate_limit],
        "proof_status": schedule_status,
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    exact_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "83c6f93",
        "exact_interpolation": {
            "field": "GF(17^32)",
            "systems_tested": len(exact_rows),
            "positive_nullity_systems": len(exact_positive),
            "pair_visible_systems": sum(1 for row in exact_rows if row["status"] == "MU8_RANK2_CARRIER_PAIR_VISIBLE"),
            "best_nullity": max([row["nullity"] for row in exact_rows], default=0),
            "best_failure_mode": "MU8_RANK2_CARRIER_INTERPOLATION_NULLITY" if exact_positive else "MU8_RANK2_CARRIER_INTERPOLATION_FULL_RANK" if exact_rows else "MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE",
        },
        "systems": exact_rows,
        "proof_status": exact_status,
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    witness_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "83c6f93",
        "witness_audit": witness if witness is not None else {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "min_agreement": None,
            "status": "NO_EXACT_WITNESS_CONSTRUCTED",
        },
        "proof_status": "PROOF_RECORD / EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS / EXPERIMENTAL" if witness_pass else "EXACT_EXTRACTION_NO_A327 / NO_EXACT_WITNESS_CONSTRUCTED / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    return schedule_record, exact_record, witness_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--plane-limit", type=int, default=12)
    parser.add_argument("--candidate-limit", type=int, default=12)
    parser.add_argument("--ratio-limit", type=int, default=12)
    args = parser.parse_args()
    schedule_record, exact_record, witness_record = audit(
        plane_limit=args.plane_limit,
        candidate_limit=args.candidate_limit,
        ratio_limit=args.ratio_limit,
    )
    if args.write_json:
        SCHEDULE_OUTPUT.write_text(json.dumps(jsonable(schedule_record), indent=2, sort_keys=True) + "\n")
        EXACT_OUTPUT.write_text(json.dumps(jsonable(exact_record), indent=2, sort_keys=True) + "\n")
        WITNESS_OUTPUT.write_text(json.dumps(jsonable(witness_record), indent=2, sort_keys=True) + "\n")
    summary = {
        "schedule_status": schedule_record["proof_status"],
        "exact_status": exact_record["proof_status"],
        "witness_status": witness_record["proof_status"],
        "planes_audited": schedule_record["schedule_candidates"]["planes_audited"],
        "guard_passing": schedule_record["schedule_candidates"]["guard_passing"],
        "systems_tested": exact_record["exact_interpolation"]["systems_tested"],
        "best_nullity": exact_record["exact_interpolation"]["best_nullity"],
    }
    if args.json:
        print(json.dumps(jsonable(summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_MU8_RANK2_CARRIER_READY")


if __name__ == "__main__":
    main()
