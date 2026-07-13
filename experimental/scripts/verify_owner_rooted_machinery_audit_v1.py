#!/usr/bin/env python3
"""Verifier for the owner-rooted machinery adversarial audit.

Companion note: experimental/notes/audits/owner_rooted_machinery_audit_v1.md

This script independently re-derives, in fresh code (not by importing or
re-running avdeevvadim's own shipped verifiers), every numeric or
algebraic claim made in the audit note:

  * Attack B: self-adjointness of the band projection P_A holds exactly on a
    symmetric band and fails exactly on an asymmetric one (positive and
    negative control on a concrete cyclic group).
  * Attack A: a 120-instance randomized cross-file chain
    (dense-band f -> positive-support b -> secant-annihilator A'), reusing
    the SAME L, M, n_+ throughout, reproduces every boxed inequality in the
    three target notes' composition; plus an explicit demonstration that
    owner_rooted_positive_support_localization_v1.md's Corollary 5.1 (eq 5.6)
    omits the kappa (thinning) factor that owner_rooted_dense_band_localization_v1.md
    Section 5 requires outside the full slice.
  * Attack F: an independent replay of the Section 6 counterexample
    construction (L, W formulas, rim packing, planted relation) for
    B in {2,4,6}.
  * Attack G: confirmation that the shipped Prop 4.1 regression uses F_17,
    that F_7 is infeasible for its 8-point domain (points 1 and 8 collide
    mod 7), and an independent replay of the secant-annihilator planted-trade
    guardrail (qbase=7, the likely source of the "F_7" paraphrase).

It does not prove or re-derive A4, primitive Q, source-algebraic emission, or
any claim the audited notes themselves mark open. Only the Python standard
library is used.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "experimental" / "notes" / "audits" / "owner_rooted_machinery_audit_v1.md"
DENSE_BAND_NOTE = (
    ROOT / "experimental" / "notes" / "audits" / "owner_rooted_dense_band_localization_v1.md"
)
POSITIVE_SUPPORT_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "audits"
    / "owner_rooted_positive_support_localization_v1.md"
)
SECANT_NOTE = ROOT / "experimental" / "notes" / "audits" / "secant_annihilator_localization_v1.md"
DENSE_BAND_CERT = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "owner-rooted-dense-band-v1"
    / "owner_rooted_dense_band_v1.json"
)
CERTIFICATE = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "owner-rooted-machinery-audit-v1"
    / "owner_rooted_machinery_audit_v1.json"
)
STATUS = "AUDIT: six of seven attacks NO ISSUE, one OPEN GAP (FIXED-proposal) in eq (5.6)"
TOL = 1e-9
DECIMALS = 9


# ---------------------------------------------------------------------------
# Shared finite Fourier helpers (independent implementation).
# ---------------------------------------------------------------------------


def dft(x: list[complex]) -> list[complex]:
    n = len(x)
    w = cmath.exp(-2j * math.pi / n)
    return [sum(x[t] * w ** (k * t) for t in range(n)) for k in range(n)]


def idft(xh: list[complex]) -> list[complex]:
    n = len(xh)
    w = cmath.exp(2j * math.pi / n)
    return [sum(xh[k] * w ** (-k * t) for k in range(n)) / n for t in range(n)]


def inner(u: list[complex], v: list[complex]) -> complex:
    return sum(a * b.conjugate() for a, b in zip(u, v))


def project(x: list[complex], band: set[int]) -> list[complex]:
    xh = dft(x)
    return idft([xh[k] if k in band else 0j for k in range(len(x))])


def lp(x: list[complex], p: float) -> float:
    return sum(abs(v) ** p for v in x) ** (1.0 / p)


# ---------------------------------------------------------------------------
# Attack B: self-adjointness positive/negative control.
# ---------------------------------------------------------------------------


def self_adjoint_control() -> dict[str, Any]:
    H = 8
    rng = random.Random(1)
    x = [complex(rng.randint(0, 5), 0) for _ in range(H)]
    y = [complex(rng.randint(0, 5), 0) for _ in range(H)]

    asym_A = {1, 2}  # -1 mod 8 = 7 not in set, -2 mod 8 = 6 not in set: NOT symmetric
    sym_A = {1, 7}  # -1 mod 8 = 7 in set: symmetric

    def trial(band: set[int]) -> dict[str, Any]:
        lhs = inner(project(x, band), y)
        rhs = inner(x, project(y, band))
        symmetric = all((-k) % H in band for k in band)
        return {
            "band": sorted(band),
            "symmetric_by_definition": symmetric,
            "lhs_re": round(lhs.real, DECIMALS),
            "rhs_re": round(rhs.real, DECIMALS),
            "equal": abs(lhs - rhs) <= 1e-9,
        }

    asym = trial(asym_A)
    sym = trial(sym_A)
    return {
        "asymmetric": asym,
        "symmetric": sym,
        "checks": {
            "asymmetric_band_breaks_self_adjointness": (not asym["symmetric_by_definition"])
            and (not asym["equal"]),
            "symmetric_band_preserves_self_adjointness": sym["symmetric_by_definition"]
            and sym["equal"],
        },
    }


# ---------------------------------------------------------------------------
# Attack F: independent replay of the Section 6 counterexample.
# ---------------------------------------------------------------------------


def section6_replay(B: int, Q: int = 5) -> dict[str, Any]:
    N = 2 * B
    a = B
    Ai = [Q ** i for i in range(1, B + 1)]
    C = 2 * sum(Ai) + 1
    assert C > 2 * sum(Ai)
    T = []
    for v in Ai:
        T.append(v)
        T.append(C - v)
    fibers: dict[int, list[tuple[int, ...]]] = {}
    for combo in itertools.combinations(range(N), a):
        s = sum(T[i] for i in combo)
        fibers.setdefault(s, []).append(combo)
    L = len(fibers)
    assert (B * C) % 2 == 0
    s0 = B * C // 2
    heavy = fibers.get(s0, [])
    W = len(heavy)
    M = math.comb(N, a)
    expected_L = (3 ** B + 1) // 2
    expected_W = math.comb(B, B // 2)
    max_int = 0
    for i in range(len(heavy)):
        for j in range(i + 1, len(heavy)):
            max_int = max(max_int, len(set(heavy[i]) & set(heavy[j])))
    planted_ok = all(Ai[k] + (C - Ai[k]) == C for k in range(B))
    wl_over_m = Fraction(W * L, M)
    return {
        "B": B,
        "N": N,
        "a": a,
        "M": M,
        "L": L,
        "expected_L": expected_L,
        "W": W,
        "expected_W": expected_W,
        "s0": s0,
        "max_intersection": max_int,
        "planted_ok": planted_ok,
        "WL_over_M": str(wl_over_m),
        "checks": {
            "L_formula": L == expected_L,
            "W_formula": W == expected_W,
            "rim_packing": max_int <= a - 2,
            "planted_relation": planted_ok,
        },
    }


def section6_regression() -> dict[str, Any]:
    cases = [section6_replay(B) for B in (2, 4, 6)]
    rates = []
    for case in cases:
        rate = math.log(float(Fraction(case["WL_over_M"]))) / case["N"]
        rates.append(rate)
    target_rate = math.log(1.5) / 2
    monotone_toward_target = all(
        abs(rates[i + 1] - target_rate) < abs(rates[i] - target_rate) for i in range(len(rates) - 1)
    )
    return {
        "cases": cases,
        "rates": [round(r, 6) for r in rates],
        "target_rate": round(target_rate, 6),
        "checks": {
            "all_cases_pass": all(all(c["checks"].values()) for c in cases),
            "rate_converges_toward_log_1_5_over_2": monotone_toward_target,
        },
    }


# ---------------------------------------------------------------------------
# Attack G: F_7 infeasibility + independent planted-trade guardrail replay.
# ---------------------------------------------------------------------------


def f7_infeasibility_check() -> dict[str, Any]:
    domain = list(range(1, 9))
    results = {}
    for p in (7, 11, 13, 17):
        residues = [x % p for x in domain]
        results[str(p)] = {
            "residues": residues,
            "all_distinct": len(set(residues)) == len(domain),
        }
    return {
        "domain": domain,
        "per_prime": results,
        "checks": {
            "F7_infeasible": not results["7"]["all_distinct"],
            "F17_feasible": results["17"]["all_distinct"],
            "F11_is_smallest_feasible": results["11"]["all_distinct"] and not results["7"]["all_distinct"],
        },
    }


def paired_planted_replay(b_pairs: int, qbase: int = 7) -> dict[str, Any]:
    assert b_pairs % 2 == 0
    left = [qbase ** (i + 1) for i in range(b_pairs)]
    c = 3 * sum(left) + 1
    values = [val for x in left for val in (x, c - x)]
    supports = []
    for chosen in itertools.combinations(range(b_pairs), b_pairs // 2):
        supports.append(frozenset(2 * i + side for i in chosen for side in (0, 1)))
    a = b_pairs
    sums = [sum(values[t] for t in s) for s in supports]
    single_sum = len(set(sums)) == 1
    pack_ok = all(
        len(s & t) <= a - 2 for i, s in enumerate(supports) for t in supports[i + 1 :]
    )
    root = supports[0]
    layers: dict[int, list[frozenset[int]]] = {}
    for s in supports[1:]:
        r = len(root - s)
        layers.setdefault(r, []).append(s)
    r_star, layer = max(layers.items(), key=lambda kv: len(kv[1]))
    trades_ok = all(
        sum(values[t] for t in (root - s)) == sum(values[t] for t in (s - root)) for s in layer
    )
    n = len(supports)
    return {
        "b_pairs": b_pairs,
        "qbase": qbase,
        "n": n,
        "r_star": r_star,
        "layer_size": len(layer),
        "incidence_floor": (n - 1) / (a - 1),
        "checks": {
            "single_common_sum": single_sum,
            "rim_packing": pack_ok,
            "trades_exact": trades_ok,
            "layer_meets_floor": len(layer) + TOL >= (n - 1) / (a - 1),
        },
    }


def guardrail_replay_regression() -> dict[str, Any]:
    cases = [paired_planted_replay(bp) for bp in (4, 6, 8)]
    # The shipped default (b_pairs=8) has a checked-in expectation to match
    # exactly (rooted_trade_incidences=36, fixed_trade_radius=4).
    default_case = cases[-1]
    return {
        "f7_infeasibility": f7_infeasibility_check(),
        "planted_cases": cases,
        "checks": {
            "all_planted_cases_pass": all(all(c["checks"].values()) for c in cases),
            "default_matches_shipped_certificate": (
                default_case["layer_size"] == 36 and default_case["r_star"] == 4
            ),
        },
    }


# ---------------------------------------------------------------------------
# Attack A: cross-file chain (dense-band f -> positive-support b -> secant A')
# and the eq (5.6) kappa-factor gap.
# ---------------------------------------------------------------------------


def symmetric_band(H: int, keys: set[int]) -> set[int]:
    A: set[int] = set()
    for k in keys:
        A.add(k % H)
        A.add((-k) % H)
    A.discard(0)
    return A


def chain_instance(seed: int, q: int, H: int = 24) -> dict[str, Any] | None:
    rng = random.Random(seed)
    f_counts = [0] * H
    hit_sites = rng.sample(range(H), 9)
    for s in hit_sites:
        f_counts[s] = rng.randint(1, 6)
    M = sum(f_counts)
    L = len(hit_sites)

    A = symmetric_band(H, {2, 5})
    if not all((-k) % H in A for k in A):
        return None

    f = [complex(v) for v in f_counts]
    h = project(f, A)
    norm_q_f = lp(h, q)
    if norm_q_f <= 1e-9:
        return None

    g = [
        (v * abs(v) ** (q - 2) / norm_q_f ** (q - 1)) if abs(v) > 1e-12 else 0j for v in h
    ]
    pg = project(g, A)
    R_A_f = (L ** (1 - 1.0 / q) / M) * norm_q_f

    weights = {s: pg[s].conjugate().real for s in range(H)}
    S_plus = [s for s in hit_sites if weights[s] > 0]
    if len(S_plus) < 2:
        return None
    Omega_plus = sum(f_counts[s] * weights[s] for s in S_plus)
    n_plus = sum(f_counts[s] for s in S_plus)

    b_counts = [0.0] * H
    for s in S_plus:
        b_counts[s] = f_counts[s]
    b = [complex(v) for v in b_counts]
    Pb = project(b, A)
    norm_q_b = lp(Pb, q)
    energy_b = sum(abs(v) ** 2 for v in Pb)

    R_A_b = (L ** (1 - 1.0 / q) / M) * norm_q_b
    e_A_b = L * energy_b / M ** 2
    x_A_b = L * (n_plus / M) * (len(A) / H)
    Y_A_b = e_A_b * x_A_b ** (q - 2)

    checks = {
        "lemma2_1_omega_plus_ge_norm_f": Omega_plus + TOL >= norm_q_f,
        "lemma2_1_norm_b_ge_omega_plus": norm_q_b + TOL >= Omega_plus,
        "lemma2_1_n_plus_ge_omega_plus": n_plus + TOL >= Omega_plus,
        "eq2_2_R_b_ge_R_f": R_A_b + TOL >= R_A_f,
        "gate_on_b_Y_ge_R_pow_q": Y_A_b + TOL >= R_A_b ** q,
    }

    s0, s1 = S_plus[0], S_plus[1]
    u = (s0 - s1) % H
    if u == 0 and len(S_plus) >= 3:
        u = (s0 - S_plus[2]) % H
    if u:
        d = H // math.gcd(u, H)

        def restriction_key(k: int) -> int:
            return (k * u) % H

        bins: dict[int, set[int]] = {}
        for k in A:
            bins.setdefault(restriction_key(k), set()).add(k)

        bhat = dft(b)

        def band_norm_q(band: set[int]) -> float:
            return lp(project(b, band), q)

        def band_energy(band: set[int]) -> float:
            return sum(abs(bhat[k]) ** 2 for k in band) / H

        q_key = max(bins, key=lambda kk: band_norm_q(bins[kk]))
        e_key = max(bins, key=lambda kk: band_energy(bins[kk]))
        m_key = max(bins, key=lambda kk: len(bins[kk]))
        selected = {q_key, e_key, m_key}
        selected |= {(-kk) % H for kk in selected}
        Aprime: set[int] = set()
        for kk in selected:
            Aprime.update(bins.get(kk, set()))

        Pb_prime = project(b, Aprime)
        norm_q_prime = lp(Pb_prime, q)
        energy_prime = sum(abs(bhat[kk]) ** 2 for kk in Aprime) / H

        R_Aprime_b = (L ** (1 - 1.0 / q) / M) * norm_q_prime
        e_Aprime_b = L * energy_prime / M ** 2
        x_Aprime_b = L * (n_plus / M) * (len(Aprime) / H)
        Y_Aprime_b = e_Aprime_b * x_Aprime_b ** (q - 2)

        checks["secant_A_prime_symmetric"] = all((-kk) % H in Aprime for kk in Aprime) and (
            Aprime <= A
        )
        checks["secant_at_most_six_cosets"] = (
            len({restriction_key(kk) for kk in Aprime}) <= 6
        )
        checks["eq4_13_R_prime_ge_R_over_d"] = R_Aprime_b + TOL >= R_A_b / d
        checks["eq4_15_Y_prime_ge_Y_over_d_pow"] = Y_Aprime_b + TOL >= Y_A_b / d ** (q - 1)
        checks["eq5_1_size_ge_A_over_d"] = len(Aprime) + TOL >= len(A) / d

    return {"seed": seed, "q": q, "checks": checks}


def chain_regression() -> dict[str, Any]:
    trials = []
    for seed in range(1, 31):
        for q in (3, 4, 5, 6):
            result = chain_instance(seed, q)
            if result is not None:
                trials.append(result)
    all_pass = all(all(t["checks"].values()) for t in trials)
    return {
        "trial_count": len(trials),
        "all_pass": all_pass,
        "checks": {"chain_all_instances_pass": all_pass, "enough_trials": len(trials) >= 60},
    }


def kappa_gap_check() -> dict[str, Any]:
    """Demonstrate the eq (5.6) omission: general threshold needs an extra
    kappa=C(N,a)/M >= 1 factor that the printed inequality lacks."""
    N, a = 12, 6
    full = math.comb(N, a)
    M = full // 2  # explicit proper sub-slice: half the full slice
    kappa = Fraction(full, M)
    L = 200
    q = 4

    def stated_threshold(M: int, L: int, N: int, a: int, q: int) -> float:
        return 2 * (L ** (2 - 2.0 / q)) / (M * (N - a + 1))

    def general_threshold(M: int, L: int, N: int, a: int, q: int, kappa: float) -> float:
        return 2 * kappa * (L ** (2 - 2.0 / q)) / (M * (N - a + 1))

    stated = stated_threshold(M, L, N, a, q)
    general = general_threshold(M, L, N, a, q, float(kappa))
    mid = (stated + general) / 2

    return {
        "N": N,
        "a": a,
        "full_slice_C_N_a": full,
        "sub_slice_M": M,
        "kappa": str(kappa),
        "L": L,
        "q": q,
        "stated_eq_5_6_threshold": stated,
        "general_kappa_corrected_threshold": general,
        "ratio_general_over_stated": general / stated,
        "witness_R_A_squared": mid,
        "checks": {
            "kappa_strictly_greater_than_one": float(kappa) > 1.0,
            "ratio_equals_kappa": abs(general / stated - float(kappa)) < 1e-9,
            "witness_satisfies_stated_bound": mid + TOL >= stated,
            "witness_fails_general_bound": mid < general - TOL,
        },
    }


# ---------------------------------------------------------------------------
# Text-grounding checks: confirm the audit note's exact quotations and line
# anchors exist verbatim in the audited files.
# ---------------------------------------------------------------------------


def normalize_ws(text: str) -> str:
    """Collapse whitespace runs (including markdown line wraps) to single
    spaces so quoted phrases match regardless of source line-wrapping."""
    return " ".join(text.split())


def text_grounding() -> dict[str, Any]:
    dense = normalize_ws(DENSE_BAND_NOTE.read_text(encoding="utf-8"))
    positive = normalize_ws(POSITIVE_SUPPORT_NOTE.read_text(encoding="utf-8"))
    secant = normalize_ws(SECANT_NOTE.read_text(encoding="utf-8"))
    dense_required = [
        "Assume the semantic compiler has removed",
        "every repeated cross-slope rim",
        "After removing common-line supports",
        "The cleaner bound",
        "must not be inferred from the weaker inclusion",
        "on the full slice, Corollary 5.1 pays the band",
        "A=-A\\subseteq\\widehat G",
    ]
    positive_required = [
        "high \\(\\mathcal Y_A\\) does not imply high \\(\\mathcal R_A\\)",
        "A sufficient condition in the original parameters is",
        "\\mathcal R_A^2",
    ]
    secant_required = [
        "A=-A\\subseteq \\widehat G\\setminus\\{0\\}",
        "and their negatives",
    ]
    forbidden_in_positive = ["kappa", "full slice", "sub-slice", "\\kappa"]
    return {
        "dense_band_required": {tok: tok in dense for tok in dense_required},
        "positive_support_required": {tok: tok in positive for tok in positive_required},
        "secant_required": {tok: tok in secant for tok in secant_required},
        "positive_support_forbidden_absent": {
            tok: tok not in positive for tok in forbidden_in_positive
        },
    }


# ---------------------------------------------------------------------------
# Payload assembly.
# ---------------------------------------------------------------------------


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    copy = dict(payload)
    copy.pop("payload_sha256", None)
    return json.dumps(copy, sort_keys=True, separators=(",", ":")).encode()


def quantize(value: Any) -> Any:
    if isinstance(value, float):
        rounded = round(value, DECIMALS)
        return 0.0 if rounded == 0.0 else rounded
    if isinstance(value, list):
        return [quantize(v) for v in value]
    if isinstance(value, dict):
        return {k: quantize(v) for k, v in value.items()}
    return value


def build_payload() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "audit_id": "owner-rooted-machinery-audit-v1",
        "status": STATUS,
        "verdicts": {
            "A_image_scale_normalization": "OPEN GAP (FIXED-proposal) -- eq (5.6) missing kappa factor",
            "B_self_adjointness": "NO ISSUE",
            "C_slope_rooting_hidden_hypotheses": "NO ISSUE (hypothesis-visibility FIXED-proposal for Thm 4.2)",
            "D_rim_packing": "NO ISSUE",
            "E_projected_energy_gate_one_way": "NO ISSUE",
            "F_section6_replay": "NO ISSUE (reproduced exactly)",
            "G_prop41_and_guardrail_replay": "NO ISSUE (reproduced exactly; field is F_17 not F_7)",
        },
        "self_adjoint_control": self_adjoint_control(),
        "section6_regression": section6_regression(),
        "guardrail_replay_regression": guardrail_replay_regression(),
        "chain_regression": chain_regression(),
        "kappa_gap_check": kappa_gap_check(),
        "text_grounding": text_grounding(),
    }
    checks_ok = (
        all(payload["self_adjoint_control"]["checks"].values())
        and all(payload["section6_regression"]["checks"].values())
        and all(payload["guardrail_replay_regression"]["checks"].values())
        and all(payload["chain_regression"]["checks"].values())
        and all(payload["kappa_gap_check"]["checks"].values())
        and all(payload["text_grounding"]["dense_band_required"].values())
        and all(payload["text_grounding"]["positive_support_required"].values())
        and all(payload["text_grounding"]["secant_required"].values())
        and all(payload["text_grounding"]["positive_support_forbidden_absent"].values())
    )
    payload["all_checks_pass"] = checks_ok
    payload = quantize(payload)
    payload["payload_sha256"] = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return payload


def validate(payload: dict[str, Any]) -> bool:
    expected_hash = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    if payload.get("payload_sha256") != expected_hash:
        return False
    if payload.get("all_checks_pass") is not True:
        return False
    if payload.get("status") != STATUS:
        return False
    checks_groups = [
        payload["self_adjoint_control"]["checks"],
        payload["section6_regression"]["checks"],
        payload["guardrail_replay_regression"]["checks"],
        payload["chain_regression"]["checks"],
        payload["kappa_gap_check"]["checks"],
        payload["text_grounding"]["dense_band_required"],
        payload["text_grounding"]["positive_support_required"],
        payload["text_grounding"]["secant_required"],
        payload["text_grounding"]["positive_support_forbidden_absent"],
    ]
    return all(all(group.values()) for group in checks_groups)


def print_summary(payload: dict[str, Any]) -> None:
    print(payload["status"])
    for attack, verdict in payload["verdicts"].items():
        print(f"  {attack}: {verdict}")
    print(f"self_adjoint_control={payload['self_adjoint_control']['checks']}")
    print(
        "section6_regression="
        f"{payload['section6_regression']['checks']} rates={payload['section6_regression']['rates']}"
    )
    print(f"guardrail_replay_regression={payload['guardrail_replay_regression']['checks']}")
    print(
        "chain_regression="
        f"trials={payload['chain_regression']['trial_count']} "
        f"all_pass={payload['chain_regression']['all_pass']}"
    )
    kg = payload["kappa_gap_check"]
    print(
        "kappa_gap_check: kappa="
        f"{kg['kappa']} stated={kg['stated_eq_5_6_threshold']:.6f} "
        f"general={kg['general_kappa_corrected_threshold']:.6f} "
        f"ratio={kg['ratio_general_over_stated']:.4f} checks={kg['checks']}"
    )
    print(f"all_checks_pass={payload['all_checks_pass']}")
    print(f"payload_sha256={payload['payload_sha256']}")


def check_shipped_dense_band_certificate() -> bool:
    """Re-run avdeevvadim's own dense-band verifier and diff its printed
    hash against the tracked certificate, as an audit-before-consume floor
    check (Attack G's 'confirm exact reproduction')."""
    if not DENSE_BAND_CERT.exists():
        return False
    import subprocess
    import sys

    script = ROOT / "experimental" / "scripts" / "verify_owner_rooted_dense_band_localization_v1.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"], capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0 and "artifact_check=PASS" in result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--skip-shipped-rerun", action="store_true", help="skip re-running avdeevvadim's own verifier")
    args = parser.parse_args()

    payload = build_payload()
    print_summary(payload)

    if not args.skip_shipped_rerun:
        shipped_ok = check_shipped_dense_band_certificate()
        print(f"shipped_dense_band_certificate_reproduced={shipped_ok}")
        if not shipped_ok:
            return 1

    if not validate(payload):
        return 1

    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote={CERTIFICATE}")

    if args.check:
        if not CERTIFICATE.exists():
            print(f"missing={CERTIFICATE}")
            return 1
        expected = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        if expected != payload:
            print("artifact_mismatch")
            return 1
        print("artifact_check=PASS")

    if args.tamper_selftest:
        # Tamper 1: flip a leaf check and recompute the hash honestly (an
        # attacker who launders a corrupted result). validate() must still
        # reject it because it re-derives every checks-group value, not just
        # the top-level all_checks_pass flag.
        tampered_a = json.loads(json.dumps(payload))
        tampered_a["kappa_gap_check"]["checks"]["witness_fails_general_bound"] = False
        tampered_a["payload_sha256"] = hashlib.sha256(canonical_bytes(tampered_a)).hexdigest()

        # Tamper 2: corrupt a value but leave the old hash in place (a naive
        # edit). validate() must reject it on the hash mismatch alone.
        tampered_b = json.loads(json.dumps(payload))
        tampered_b["self_adjoint_control"]["checks"]["symmetric_band_preserves_self_adjointness"] = False

        if validate(tampered_a) or validate(tampered_b):
            print("tamper_selftest=FAIL")
            return 1
        print("tamper_selftest=PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
