#!/usr/bin/env python3
"""Verify L1 prefix Fourier orbit-cancellation identities.

AUDIT / EXPERIMENTAL verifier for
`experimental/notes/l1/l1_prefix_fourier_orbit_cancellation.md`.

The script checks the exact dual-dilation orbit compression of the prefix
Fourier formula:

    N(c) - binom(n,m)/p^sigma
      = p^{-sigma} sum_{[r] != [0]} S_m(r) K_{r,c}.

It also reports finite diagnostics showing why orbit compression is still not
the desired theorem by itself: orbitwise triangle bounds can remain much larger
than the signed orbit sum that determines the actual fiber deviation.

Standard library only.  This script is list/locator-side only; it does not
assert RS list-decoding, MCA, line-decoding, or protocol safety.
"""

import argparse
import itertools
import json
import sys
from collections import defaultdict
from math import comb, sqrt
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from verify_l1_fourier_reduction import S_product, ep, subgroup  # noqa: E402


def dot_mod(left, right, p):
    return sum((a * b) % p for a, b in zip(left, right)) % p


def powers_for_h(h, sigma, p):
    out = []
    cur = 1
    for _ in range(sigma):
        cur = (cur * h) % p
        out.append(cur)
    return tuple(out)


def dual_dilate(r, h, p):
    """Dual dilation action (h*r)_j = h^j r_j, j=1..sigma."""
    return tuple((rj * hj) % p for rj, hj in zip(r, powers_for_h(h, len(r), p)))


def power_sum_key(A_indices, H, sigma, p):
    return tuple(
        sum(pow(H[i], j, p) for i in A_indices) % p
        for j in range(1, sigma + 1)
    )


def brute_histogram(H, m, sigma, p):
    hist = defaultdict(int)
    for A in itertools.combinations(range(len(H)), m):
        hist[power_sum_key(A, H, sigma, p)] += 1
    return dict(hist)


def all_vectors(p, sigma):
    return list(itertools.product(range(p), repeat=sigma))


def build_orbits(rvecs, H, p):
    seen = set()
    orbits = []
    for r in rvecs:
        if r in seen:
            continue
        orbit = sorted({dual_dilate(r, h, p) for h in H})
        orbit_set = set(orbit)
        seen.update(orbit_set)
        stabilizer = [h for h in H if dual_dilate(r, h, p) == r]
        orbits.append({
            "rep": r,
            "members": orbit,
            "size": len(orbit),
            "stabilizer_size": len(stabilizer),
            "is_zero": all(x == 0 for x in r),
        })
    return orbits


def orbit_size_distribution(orbits):
    out = defaultdict(int)
    for orbit in orbits:
        out[orbit["size"]] += 1
    return dict(sorted(out.items()))


def orbit_kernel(orbit, c, p):
    return sum(ep(-dot_mod(r, c, p), p) for r in orbit["members"])


def phase_values(orbit, c, p):
    return sorted({dot_mod(r, c, p) for r in orbit["members"]})


def pearson(xs, ys):
    if len(xs) < 2:
        return 0.0
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return 0.0
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / sqrt(vx * vy)


def run(p=17, n=16, k=8, sigma=2, tol=1e-6):
    if sigma >= p:
        raise ValueError("this finite verifier assumes sigma < p")
    H = subgroup(p, n)
    m = n - (k + sigma)
    if m < 0:
        raise ValueError("need m = n - (k + sigma) >= 0")

    cvecs = all_vectors(p, sigma)
    rvecs = all_vectors(p, sigma)
    hist = brute_histogram(H, m, sigma, p)
    total = comb(n, m)
    main = total / (p ** sigma)
    Svals = {r: S_product(r, H, m, p) for r in rvecs}
    orbits = build_orbits(rvecs, H, p)
    orbit_distribution = orbit_size_distribution(orbits)

    # S_m invariance on dual dilation orbits.
    max_s_orbit_error = 0.0
    for orbit in orbits:
        rep_s = Svals[orbit["rep"]]
        for r in orbit["members"]:
            max_s_orbit_error = max(max_s_orbit_error, abs(Svals[r] - rep_s))
    s_orbit_invariance_ok = max_s_orbit_error <= tol

    # Orbit-compressed Fourier reconstruction for every c.
    max_reconstruction_error = 0.0
    max_dev = 0.0
    worst_c = None
    raw_l1_bound = sum(abs(Svals[r]) for r in rvecs if any(r)) / (p ** sigma)
    max_orbit_triangle = 0.0
    max_orbit_triangle_generic_prefix = 0.0
    orbit_triangle_at_worst = 0.0
    orbit_triangle_at_worst_generic_prefix = 0.0
    max_dev_generic_prefix = 0.0
    worst_generic_prefix_c = None
    orbit_triangle_by_c = {}
    for c in cvecs:
        compressed = 0j
        orbit_triangle = 0.0
        for orbit in orbits:
            kval = orbit_kernel(orbit, c, p)
            sval = Svals[orbit["rep"]]
            compressed += sval * kval
            if not orbit["is_zero"]:
                orbit_triangle += abs(sval) * abs(kval)
        compressed /= p ** sigma
        expected = hist.get(c, 0)
        err = abs(compressed.real - expected) + abs(compressed.imag)
        max_reconstruction_error = max(max_reconstruction_error, err)
        dev = abs(expected - main)
        orbit_triangle_by_c[c] = orbit_triangle / (p ** sigma)
        if dev > max_dev:
            max_dev = dev
            worst_c = c
        if c and c[0] % p != 0 and dev > max_dev_generic_prefix:
            max_dev_generic_prefix = dev
            worst_generic_prefix_c = c
        max_orbit_triangle = max(max_orbit_triangle, orbit_triangle / (p ** sigma))
        if c and c[0] % p != 0:
            max_orbit_triangle_generic_prefix = max(
                max_orbit_triangle_generic_prefix,
                orbit_triangle / (p ** sigma),
            )
    orbit_reconstruction_ok = max_reconstruction_error <= tol
    if worst_c is not None:
        orbit_triangle_at_worst = orbit_triangle_by_c[worst_c]
    if worst_generic_prefix_c is not None:
        orbit_triangle_at_worst_generic_prefix = orbit_triangle_by_c[
            worst_generic_prefix_c
        ]

    # Kernel L2 orthogonality and second moment identity.
    max_kernel_l2_error = 0.0
    nonzero_orbits = [orbit for orbit in orbits if not orbit["is_zero"]]
    for orbit in nonzero_orbits:
        l2 = sum(abs(orbit_kernel(orbit, c, p)) ** 2 for c in cvecs)
        expected_l2 = (p ** sigma) * orbit["size"]
        max_kernel_l2_error = max(max_kernel_l2_error, abs(l2 - expected_l2))
    kernel_l2_ok = max_kernel_l2_error <= 1e-5

    dev_second_moment = sum((hist.get(c, 0) - main) ** 2 for c in cvecs)
    orbit_second_moment = sum(
        (abs(Svals[orbit["rep"]]) ** 2) * orbit["size"]
        for orbit in nonzero_orbits
    ) / (p ** sigma)
    second_moment_error = abs(dev_second_moment - orbit_second_moment)
    second_moment_ok = second_moment_error <= 1e-5
    zero_c = tuple(0 for _ in range(sigma))
    zero_saturation_error = max(
        abs(abs(orbit_kernel(orbit, zero_c, p)) - orbit["size"])
        for orbit in nonzero_orbits
    ) if nonzero_orbits else 0.0
    zero_prefix_kernel_saturation_ok = zero_saturation_error <= 1e-6
    orthogonal_support_saturation_error = 0.0
    orthogonal_support_saturation_ok = True
    orthogonal_support_details = None
    if sigma >= 2:
        c_orth = tuple([1, 0] + [0] * (sigma - 2))
        r_orth = tuple([0, 1] + [0] * (sigma - 2))
        orth_orbit_members = sorted({dual_dilate(r_orth, h, p) for h in H})
        orth_orbit = {
            "rep": r_orth,
            "members": orth_orbit_members,
            "size": len(orth_orbit_members),
            "stabilizer_size": len(
                [h for h in H if dual_dilate(r_orth, h, p) == r_orth]
            ),
            "is_zero": False,
        }
        orth_kernel = orbit_kernel(orth_orbit, c_orth, p)
        orthogonal_support_saturation_error = abs(orth_kernel - orth_orbit["size"])
        orthogonal_support_saturation_ok = (
            orthogonal_support_saturation_error <= 1e-6
            and c_orth[0] != 0
            and all((rj == 0 or cj == 0) for rj, cj in zip(r_orth, c_orth))
        )
        orthogonal_support_details = {
            "c": c_orth,
            "r": r_orth,
            "orbit_size": orth_orbit["size"],
            "stabilizer_size": orth_orbit["stabilizer_size"],
            "kernel_real": orth_kernel.real,
            "kernel_imag": orth_kernel.imag,
        }

    regression_checks = {}
    if p == 17 and n == 8 and sigma == 2:
        regression_checks[
            "p17_n8_sigma2_orbit_distribution_ok"
        ] = orbit_distribution == {1: 1, 4: 4, 8: 34}
    if p == 17 and n == 8:
        r4 = (0, 0, 0, 1)
        orbit4 = {dual_dilate(r4, h, p) for h in H}
        stabilizer4 = [h for h in H if dual_dilate(r4, h, p) == r4]
        regression_checks[
            "p17_n8_sigma4_r0001_stabilizer_ok"
        ] = len(stabilizer4) == 4 and len(orbit4) == 2

    # Degeneracy and correlation diagnostics.  These are finite diagnostics, not
    # asymptotic claims.
    degeneracy = {
        "pairs_checked": 0,
        "constant_phase_pairs": 0,
        "zero_phase_pairs": 0,
        "max_kernel_abs": 0.0,
        "max_kernel_orbit_size": 0,
        "large_kernel_pairs": 0,
        "generic_prefix_pairs_checked": 0,
        "generic_prefix_constant_phase_pairs": 0,
        "generic_prefix_zero_phase_pairs": 0,
        "generic_prefix_max_kernel_abs": 0.0,
        "generic_prefix_max_kernel_orbit_size": 0,
    }
    s_abs = []
    k_abs = []
    worst_c_kernels = []
    for orbit in nonzero_orbits:
        sval_abs = abs(Svals[orbit["rep"]])
        for c in cvecs:
            vals = phase_values(orbit, c, p)
            kval_abs = abs(orbit_kernel(orbit, c, p))
            degeneracy["pairs_checked"] += 1
            if len(vals) == 1:
                degeneracy["constant_phase_pairs"] += 1
                if vals == [0]:
                    degeneracy["zero_phase_pairs"] += 1
            if c and c[0] % p != 0:
                degeneracy["generic_prefix_pairs_checked"] += 1
                if len(vals) == 1:
                    degeneracy["generic_prefix_constant_phase_pairs"] += 1
                    if vals == [0]:
                        degeneracy["generic_prefix_zero_phase_pairs"] += 1
                if kval_abs > degeneracy["generic_prefix_max_kernel_abs"]:
                    degeneracy["generic_prefix_max_kernel_abs"] = kval_abs
                    degeneracy["generic_prefix_max_kernel_orbit_size"] = orbit["size"]
            if kval_abs > sqrt(orbit["size"]) + tol:
                degeneracy["large_kernel_pairs"] += 1
            if kval_abs > degeneracy["max_kernel_abs"]:
                degeneracy["max_kernel_abs"] = kval_abs
                degeneracy["max_kernel_orbit_size"] = orbit["size"]
            if c == worst_c:
                s_abs.append(sval_abs)
                k_abs.append(kval_abs)
                worst_c_kernels.append({
                    "rep": orbit["rep"],
                    "orbit_size": orbit["size"],
                    "S_abs": sval_abs,
                    "K_abs": kval_abs,
                    "phase_value_count": len(vals),
                })
    corr_at_worst = pearson(s_abs, k_abs)
    top_worst_kernels = sorted(
        worst_c_kernels,
        key=lambda row: row["S_abs"] * row["K_abs"],
        reverse=True,
    )[:8]

    l2_rms = sqrt(dev_second_moment / (p ** sigma))
    l4_mean = sum((hist.get(c, 0) - main) ** 4 for c in cvecs) / (p ** sigma)
    l4_root = l4_mean ** 0.25

    orbit_triangle_insufficient = (
        max_dev > tol and max_orbit_triangle / max_dev > 2.0
    )

    return {
        "status": "AUDIT/EXPERIMENTAL",
        "params": {"p": p, "n": n, "k": k, "sigma": sigma, "m": m},
        "counts": {
            "total_divisors": total,
            "main_term": main,
            "distinct_power_sum_keys": len(hist),
            "max_fiber": max(hist.values()) if hist else 0,
            "nonzero_dual_orbits": len(nonzero_orbits),
            "all_dual_orbits": len(orbits),
            "orbit_size_distribution": orbit_distribution,
        },
        "checks": {
            "S_m_dual_orbit_invariance_ok": s_orbit_invariance_ok,
            "orbit_fourier_reconstruction_ok": orbit_reconstruction_ok,
            "kernel_l2_identity_ok": kernel_l2_ok,
            "orbit_second_moment_identity_ok": second_moment_ok,
            "zero_prefix_kernel_saturation_ok": zero_prefix_kernel_saturation_ok,
            "orthogonal_support_saturation_ok": orthogonal_support_saturation_ok,
            **regression_checks,
        },
        "errors": {
            "max_S_m_orbit_error": max_s_orbit_error,
            "max_orbit_reconstruction_error": max_reconstruction_error,
            "max_kernel_l2_error": max_kernel_l2_error,
            "second_moment_error": second_moment_error,
            "zero_prefix_kernel_saturation_error": zero_saturation_error,
            "orthogonal_support_saturation_error": (
                orthogonal_support_saturation_error
            ),
        },
        "deterministic_examples": {
            "orthogonal_support_saturation": orthogonal_support_details,
        },
        "bounds": {
            "actual_max_deviation": max_dev,
            "worst_c": worst_c,
            "generic_prefix_actual_max_deviation": max_dev_generic_prefix,
            "generic_prefix_worst_c": worst_generic_prefix_c,
            "raw_frequency_l1_bound": raw_l1_bound,
            "max_orbit_triangle_bound": max_orbit_triangle,
            "generic_prefix_max_orbit_triangle_bound": (
                max_orbit_triangle_generic_prefix
            ),
            "orbit_triangle_bound_at_worst_c": orbit_triangle_at_worst,
            "orbit_triangle_bound_at_worst_generic_prefix_c": (
                orbit_triangle_at_worst_generic_prefix
            ),
            "raw_l1_over_actual": raw_l1_bound / max_dev if max_dev else None,
            "orbit_triangle_over_actual": (
                max_orbit_triangle / max_dev if max_dev else None
            ),
            "generic_prefix_orbit_triangle_over_actual": (
                max_orbit_triangle_generic_prefix / max_dev_generic_prefix
                if max_dev_generic_prefix else None
            ),
            "orbit_triangle_insufficient_route_cut": orbit_triangle_insufficient,
            "deviation_l2_rms": l2_rms,
            "deviation_l4_root": l4_root,
        },
        "degeneracy": {
            **degeneracy,
            "max_kernel_abs": degeneracy["max_kernel_abs"],
            "constant_phase_fraction": (
                degeneracy["constant_phase_pairs"] / degeneracy["pairs_checked"]
                if degeneracy["pairs_checked"] else 0.0
            ),
            "zero_phase_fraction": (
                degeneracy["zero_phase_pairs"] / degeneracy["pairs_checked"]
                if degeneracy["pairs_checked"] else 0.0
            ),
            "generic_prefix_constant_phase_fraction": (
                degeneracy["generic_prefix_constant_phase_pairs"]
                / degeneracy["generic_prefix_pairs_checked"]
                if degeneracy["generic_prefix_pairs_checked"] else 0.0
            ),
            "generic_prefix_zero_phase_fraction": (
                degeneracy["generic_prefix_zero_phase_pairs"]
                / degeneracy["generic_prefix_pairs_checked"]
                if degeneracy["generic_prefix_pairs_checked"] else 0.0
            ),
        },
        "correlation": {
            "worst_c_absS_absK_pearson": corr_at_worst,
            "top_worst_c_orbit_contributors": [
                {
                    "rep": list(row["rep"]),
                    "orbit_size": row["orbit_size"],
                    "S_abs": round(row["S_abs"], 6),
                    "K_abs": round(row["K_abs"], 6),
                    "phase_value_count": row["phase_value_count"],
                }
                for row in top_worst_kernels
            ],
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--p", type=int, default=17)
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--sigma", type=int, default=2)
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)

    result = run(args.p, args.n, args.k, args.sigma)
    ok = all(result["checks"].values())

    if args.format == "json":
        print(json.dumps(result, indent=2))
        return 0 if ok else 1

    pp = result["params"]
    cc = result["counts"]
    ee = result["errors"]
    bb = result["bounds"]
    dd = result["degeneracy"]
    print(f"L1 Fourier orbit-cancellation verifier  (status {result['status']})")
    print(
        f"  F_{pp['p']}, n={pp['n']}, k={pp['k']}, "
        f"sigma={pp['sigma']}, m={pp['m']}"
    )
    print(
        f"  dual orbits: {cc['nonzero_dual_orbits']} nonzero / "
        f"{cc['all_dual_orbits']} total"
    )
    print(f"  orbit-size distribution       : {cc['orbit_size_distribution']}")
    print(
        f"  fibers: {cc['distinct_power_sum_keys']} keys, "
        f"max {cc['max_fiber']}, main {cc['main_term']:.6f}"
    )
    for name, passed in result["checks"].items():
        print(f"  [{'OK ' if passed else 'FAIL'}] {name}")
    print("  -- numerical residuals --")
    print(f"     max S_m orbit error        : {ee['max_S_m_orbit_error']:.2e}")
    print(f"     max reconstruction error   : {ee['max_orbit_reconstruction_error']:.2e}")
    print(f"     max kernel L2 error        : {ee['max_kernel_l2_error']:.2e}")
    print(f"     second moment error        : {ee['second_moment_error']:.2e}")
    print(f"     zero-prefix saturation err : {ee['zero_prefix_kernel_saturation_error']:.2e}")
    print(f"     orth-support saturation err: "
          f"{ee['orthogonal_support_saturation_error']:.2e}")
    print("  -- cancellation diagnostics --")
    print(f"     actual max deviation        : {bb['actual_max_deviation']:.6f}")
    print(f"     generic-prefix max dev      : {bb['generic_prefix_actual_max_deviation']:.6f}")
    print(f"     raw frequency L1 bound      : {bb['raw_frequency_l1_bound']:.6f}")
    print(f"     max orbit triangle bound    : {bb['max_orbit_triangle_bound']:.6f}")
    print(f"     generic-prefix orbit bound  : "
          f"{bb['generic_prefix_max_orbit_triangle_bound']:.6f}")
    print(f"     orbit triangle at worst c   : {bb['orbit_triangle_bound_at_worst_c']:.6f}")
    print(f"     orbit triangle at worst gen : "
          f"{bb['orbit_triangle_bound_at_worst_generic_prefix_c']:.6f}")
    print(f"     raw/orbit route-cut ratios  : {bb['raw_l1_over_actual']:.3f} / "
          f"{bb['orbit_triangle_over_actual']:.3f}")
    if bb["generic_prefix_orbit_triangle_over_actual"] is not None:
        print(f"     generic-prefix route ratio : "
              f"{bb['generic_prefix_orbit_triangle_over_actual']:.3f}")
    print(f"     L2 rms / L4 root deviation  : {bb['deviation_l2_rms']:.6f} / "
          f"{bb['deviation_l4_root']:.6f}")
    print("  -- kernel degeneracy --")
    print(f"     pairs checked               : {dd['pairs_checked']}")
    print(f"     constant phase pairs        : {dd['constant_phase_pairs']}")
    print(f"     zero phase pairs            : {dd['zero_phase_pairs']}")
    print(f"     max |K| / orbit size        : {dd['max_kernel_abs']:.6f} / "
          f"{dd['max_kernel_orbit_size']}")
    print(f"     generic c1!=0 max |K|/orbit: "
          f"{dd['generic_prefix_max_kernel_abs']:.6f} / "
          f"{dd['generic_prefix_max_kernel_orbit_size']}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
