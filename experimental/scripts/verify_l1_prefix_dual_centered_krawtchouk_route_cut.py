#!/usr/bin/env python3
"""Verify the centered Krawtchouk route cut.

The script is self-contained: it imports only the Python standard library.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict


def primitive_root(p: int) -> int:
    factors = []
    x = p - 1
    q = 2
    while q * q <= x:
        if x % q == 0:
            factors.append(q)
            while x % q == 0:
                x //= q
        q += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root for p={p}")


def subgroup(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    gen = pow(primitive_root(p), (p - 1) // n, p)
    out = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * gen) % p
    return tuple(sorted(out))


def antipodal_reps(H: tuple[int, ...], p: int) -> tuple[int, ...]:
    remaining = set(H)
    reps = []
    while remaining:
        h = min(remaining)
        reps.append(h)
        remaining.remove(h)
        remaining.remove((-h) % p)
    return tuple(reps)


def odd_exponents(d: int) -> tuple[int, ...]:
    return tuple(2 * i + 1 for i in range(d))


def bessel_law(p: int, lam: float) -> list[float]:
    """Return the Bessel probability law with the prescribed Fourier transform."""

    hats = [
        math.exp(-lam * (math.sin(2.0 * math.pi * t / p) ** 2))
        for t in range(p)
    ]
    law = []
    for x in range(p):
        value = sum(
            hats[t] * math.cos(2.0 * math.pi * x * t / p)
            for t in range(p)
        ) / p
        law.append(value)
    total = sum(law)
    return [max(0.0, value) / total for value in law]


def bessel_hat(p: int, lam: float, x: int) -> float:
    return math.exp(-lam * (math.sin(2.0 * math.pi * (x % p) / p) ** 2))


def energy(values: tuple[int, ...], p: int) -> float:
    return sum(math.sin(2.0 * math.pi * value / p) ** 2 for value in values)


def coeffs_from_support(d: int, support: tuple[int, ...], values: tuple[int, ...]) -> tuple[int, ...]:
    by_exp = {j: value for j, value in zip(support, values)}
    return tuple(by_exp.get(2 * idx + 1, 0) for idx in range(d))


def coeff_word(coeffs: tuple[int, ...], reps: tuple[int, ...], p: int) -> tuple[int, ...]:
    out = []
    for h in reps:
        total = 0
        for idx, coeff in enumerate(coeffs):
            if coeff:
                total = (total + coeff * pow(h, 2 * idx + 1, p)) % p
        out.append(total)
    return tuple(out)


def support_stabilizer_size(coeffs: tuple[int, ...], n: int) -> int:
    support = [2 * idx + 1 for idx, coeff in enumerate(coeffs) if coeff]
    if not support:
        return n
    base = support[0]
    g = n
    for exponent in support:
        g = math.gcd(g, exponent - base)
    return g


def support_average(
    p: int,
    n: int,
    d: int,
    S: tuple[int, ...],
    u: int,
    lam: float,
    primitive_submass: bool = False,
) -> float:
    reps = antipodal_reps(subgroup(p, n), p)
    total = 0.0
    support_count = 0
    for U in itertools.combinations(S, u):
        support_count += 1
        for values in itertools.product(range(1, p), repeat=u):
            coeffs = coeffs_from_support(d, U, values)
            if primitive_submass and support_stabilizer_size(coeffs, n) != 2:
                continue
            total += math.exp(-lam * energy(coeff_word(coeffs, reps, p), p))
    return total / (support_count * ((p - 1) ** u))


def conditional_primitive_average(
    p: int,
    n: int,
    d: int,
    S: tuple[int, ...],
    u: int,
    lam: float,
) -> float | None:
    reps = antipodal_reps(subgroup(p, n), p)
    total = 0.0
    count = 0
    for U in itertools.combinations(S, u):
        for values in itertools.product(range(1, p), repeat=u):
            coeffs = coeffs_from_support(d, U, values)
            if support_stabilizer_size(coeffs, n) != 2:
                continue
            total += math.exp(-lam * energy(coeff_word(coeffs, reps, p), p))
            count += 1
    return None if count == 0 else total / count


def moment_values(y: tuple[int, ...], reps: tuple[int, ...], S: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple(
        sum((yi * pow(h, j, p)) % p for yi, h in zip(y, reps)) % p
        for j in S
    )


def kappa(moment: int, p: int) -> float:
    return 1.0 if moment % p == 0 else -1.0 / (p - 1)


def centered_indicator(moment: int, p: int) -> float:
    return (1.0 if moment % p == 0 else 0.0) - (1.0 / p)


def direct_centered_average(p: int, n: int, S: tuple[int, ...], u: int, lam: float) -> dict[str, float]:
    reps = antipodal_reps(subgroup(p, n), p)
    nu = bessel_law(p, lam)
    torus_kernel = 0.0
    centered = 0.0
    zero_count_kernel = 0.0
    zero_factorial = defaultdict(float)
    for y in itertools.product(range(p), repeat=len(reps)):
        prob = 1.0
        for coord in y:
            prob *= nu[coord]
        moments = moment_values(y, reps, S, p)
        z = sum(1 for value in moments if value == 0)
        for s in range(len(S) + 1):
            if z >= s:
                zero_factorial[s] += math.comb(z, s) * prob
        selected_kernel_sum = 0.0
        selected_centered_sum = 0.0
        for U_indices in itertools.combinations(range(len(S)), u):
            prod_kernel = 1.0
            prod_centered = 1.0
            for idx in U_indices:
                prod_kernel *= kappa(moments[idx], p)
                prod_centered *= centered_indicator(moments[idx], p)
            selected_kernel_sum += prod_kernel
            selected_centered_sum += prod_centered
        torus_kernel += prob * selected_kernel_sum / math.comb(len(S), u)
        centered += prob * selected_centered_sum / math.comb(len(S), u)
        zero_count_kernel += prob * krawtchouk_phi(len(S), u, z, p)
    return {
        "torus_kernel": torus_kernel,
        "centered_scaled": ((p / (p - 1)) ** u) * centered,
        "zero_count_kernel": zero_count_kernel,
        "zero_factorial": dict(zero_factorial),
    }


def krawtchouk_phi(t: int, u: int, z: int, p: int) -> float:
    w = t - z
    total = 0.0
    for k in range(u + 1):
        if k <= w and u - k <= z:
            total += math.comb(w, k) * math.comb(z, u - k) * ((-1.0 / (p - 1)) ** k)
    return total / math.comb(t, u)


def rank_mod_p(matrix: list[list[int]], p: int) -> int:
    rows = [list(row) for row in matrix if any(value % p for value in row)]
    if not rows:
        return 0
    rank = 0
    col_count = len(rows[0])
    for col in range(col_count):
        pivot = None
        for row in range(rank, len(rows)):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % p, p - 2, p)
        rows[rank] = [(value * inv) % p for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank:
                continue
            factor = rows[row][col] % p
            if factor:
                rows[row] = [(a - factor * b) % p for a, b in zip(rows[row], rows[rank])]
        rank += 1
    return rank


def joint_zero_probability(p: int, n: int, T: tuple[int, ...], lam: float) -> float:
    reps = antipodal_reps(subgroup(p, n), p)
    nu = bessel_law(p, lam)
    total = 0.0
    for y in itertools.product(range(p), repeat=len(reps)):
        if any(moment_values(y, reps, T, p)):
            continue
        prob = 1.0
        for coord in y:
            prob *= nu[coord]
        total += prob
    return total


def joint_zero_probability_fourier(p: int, n: int, T: tuple[int, ...], lam: float) -> float:
    reps = antipodal_reps(subgroup(p, n), p)
    total = 0.0
    for alpha in itertools.product(range(p), repeat=len(T)):
        prod = 1.0
        for h in reps:
            coeff = sum(a * pow(h, j, p) for a, j in zip(alpha, T)) % p
            prod *= bessel_hat(p, lam, coeff)
        total += prod
    return total / (p ** len(T))


def deltas_by_size(p: int, n: int, S: tuple[int, ...], lam: float) -> dict[int, float]:
    out = {}
    reps = antipodal_reps(subgroup(p, n), p)
    for s in range(1, len(S) + 1):
        vals = []
        for T in itertools.combinations(S, s):
            rank = rank_mod_p([[pow(h, j, p) for h in reps] for j in T], p)
            baseline = p ** (-rank)
            vals.append(joint_zero_probability(p, n, T, lam) - baseline)
        out[s] = sum(vals) / len(vals)
    return out


def forward_from_deltas(p: int, u: int, deltas: dict[int, float]) -> float:
    total = 0.0
    for s in range(1, u + 1):
        total += math.comb(u, s) * ((-1.0 / p) ** (u - s)) * deltas[s]
    return ((p / (p - 1)) ** u) * total


def inverse_delta_from_avgs(p: int, s: int, avgs: dict[int, float]) -> float:
    return (p ** (-s)) * sum(
        math.comb(s, v) * ((p - 1) ** v) * avgs[v]
        for v in range(1, s + 1)
    )


def beta_bound(p: int, u: int, nu0: float) -> float:
    return ((p * nu0 + 1.0) / (p - 1)) ** u - ((p - 1) ** (-u))


def near_full_criterion_bound(p: int, u: int, L: int, delta_sup: float) -> float:
    head = sum(math.comb(u, j) * (p ** (-j)) * delta_sup for j in range(L))
    tail = sum(math.comb(u, j) * (p ** (-j)) for j in range(L, u))
    return ((p / (p - 1)) ** u) * (head + tail)


def p257_counterexample() -> dict[str, float | bool]:
    p = 257
    N = (p - 1) // 2
    lam = 1.0 / 3.0
    reps = range(1, N + 1)
    nu0 = sum(
        math.exp(-lam * math.sin(2.0 * math.pi * x / p) ** 2)
        for x in range(p)
    ) / p
    prob_zero = sum(
        math.exp(
            -lam
            * sum(
                math.sin(2.0 * math.pi * u * h / p) ** 2
                for h in reps
            )
        )
        for u in range(p)
    ) / p
    centered = (p / (p - 1)) * (prob_zero - 1.0 / p)
    return {
        "p": p,
        "N": N,
        "lambda": lam,
        "nu0": nu0,
        "nu0_power_N_minus_1": nu0 ** (N - 1),
        "prob_M1_zero": prob_zero,
        "uniform_floor": 1.0 / p,
        "centered_A_singleton": centered,
        "counterexample_ok": prob_zero >= 1.0 / p and prob_zero > nu0 ** (N - 1),
    }


def case_data(p: int, n: int, d: int, lam: float) -> dict[str, object]:
    S = odd_exponents(d)
    nu0 = bessel_law(p, lam)[0]
    rows = []
    ok = True
    avgs = {}
    deltas = deltas_by_size(p, n, S, lam)
    for u in range(1, len(S) + 1):
        full = support_average(p, n, d, S, u, lam)
        primitive_sub = support_average(p, n, d, S, u, lam, primitive_submass=True)
        primitive_cond = conditional_primitive_average(p, n, d, S, u, lam)
        centered = direct_centered_average(p, n, S, u, lam)
        avgs[u] = full
        forward = forward_from_deltas(p, u, deltas)
        odlyzko = beta_bound(p, u, nu0)
        criterion = near_full_criterion_bound(p, u, max(1, u // 2), 1e-6)
        row_ok = (
            abs(full - centered["torus_kernel"]) < 1e-10
            and abs(full - centered["centered_scaled"]) < 1e-10
            and abs(full - centered["zero_count_kernel"]) < 1e-10
            and abs(full - forward) < 1e-10
            and primitive_sub <= full + 1e-12
            and full <= odlyzko + 1e-12
            and criterion >= 0.0
        )
        if primitive_cond is not None and primitive_sub > 0:
            # Record that conditional normalization is a different quantity.
            row_ok = row_ok and primitive_cond >= primitive_sub - 1e-12
        ok = ok and row_ok
        rows.append({
            "u": u,
            "full_support_average": full,
            "primitive_submass_same_denominator": primitive_sub,
            "primitive_conditional_average": primitive_cond,
            "centered_product_value": centered["centered_scaled"],
            "zero_count_kernel_value": centered["zero_count_kernel"],
            "joint_deviation_forward_value": forward,
            "odlyzko_beta_bound": odlyzko,
            "near_full_criterion_bound_with_delta_1e_minus_6": criterion,
            "ok": row_ok,
        })
    inverse_rows = []
    for s, delta in deltas.items():
        inv = inverse_delta_from_avgs(p, s, avgs)
        inv_zero = direct_centered_average(p, n, S, len(S), lam)["zero_factorial"][s] / math.comb(len(S), s) - (p ** (-s))
        row_ok = abs(delta - inv) < 1e-10 and abs(delta - inv_zero) < 1e-10
        ok = ok and row_ok
        inverse_rows.append({
            "s": s,
            "bar_delta": delta,
            "inverse_from_A_v": inv,
            "inverse_from_zero_factorial": inv_zero,
            "ok": row_ok,
        })
    positivity_rows = []
    for s in range(1, len(S) + 1):
        for T in itertools.combinations(S, s):
            direct = joint_zero_probability(p, n, T, lam)
            fourier = joint_zero_probability_fourier(p, n, T, lam)
            rank = rank_mod_p(
                [[pow(h, j, p) for h in antipodal_reps(subgroup(p, n), p)] for j in T],
                p,
            )
            delta = direct - (p ** (-rank))
            row_ok = abs(direct - fourier) < 1e-10 and delta >= -1e-12 and direct <= (nu0 ** rank) + 1e-12
            ok = ok and row_ok
            positivity_rows.append({
                "T": T,
                "rank": rank,
                "direct_probability": direct,
                "fourier_probability": fourier,
                "delta": delta,
                "odlyzko_codim_bound": nu0 ** rank,
                "ok": row_ok,
            })
    return {
        "params": {"p": p, "n": n, "N": n // 2, "d": d, "lambda": lam, "S": S},
        "rows": rows,
        "inverse_transform_rows": inverse_rows,
        "positivity_and_odlyzko_rows": positivity_rows,
        "ok": ok,
    }


def reserve_ledger() -> list[dict[str, object]]:
    rows = []
    for N, p_model, u, nu0 in [
        (128, 257, 32, 0.852370283540968),
        (256, 521, 48, 0.80),
        (512, 1031, 80, 0.70),
    ]:
        beta = (p_model * nu0 + 1.0) / (p_model - 1)
        rows.append({
            "N": N,
            "p_model": p_model,
            "u": u,
            "nu0_model": nu0,
            "beta": beta,
            "log_beta_bound_over_N": u * math.log(beta) / N,
            "subexponential_at_u_N_over_logN": True,
        })
    return rows


def run_all() -> dict[str, object]:
    rows = [
        case_data(7, 6, 2, 0.5),
        case_data(11, 10, 2, 0.5),
        case_data(17, 8, 2, 1.0),
    ]
    counterexample = p257_counterexample()
    return {
        "rows": rows,
        "p257_counterexample": counterexample,
        "reserve_ledger": reserve_ledger(),
        "ALL_CHECKS_OK": all(row["ok"] for row in rows) and counterexample["counterexample_ok"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_all()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("L1 dual centered Krawtchouk route-cut verifier")
        for case in result["rows"]:
            params = case["params"]
            print(
                "  p={p} n={n} d={d} lambda={lambda}: ok={ok}".format(
                    ok=case["ok"],
                    **params,
                )
            )
        ce = result["p257_counterexample"]
        print(
            "P257_COUNTEREXAMPLE prob={prob:.12g} nu0^(N-1)={powv:.12g} ok={ok}".format(
                prob=ce["prob_M1_zero"],
                powv=ce["nu0_power_N_minus_1"],
                ok=ce["counterexample_ok"],
            )
        )
        print(f"ALL_CHECKS_OK={result['ALL_CHECKS_OK']}")
    if not result["ALL_CHECKS_OK"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
