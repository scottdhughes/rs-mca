#!/usr/bin/env python3
"""Adjacent-threshold-pin certificate generator for admissible RS rows.

For an admissible Reed-Solomon row

    C = RS[F_p, D, k],   |D| = n,   D an order-n multiplicative subgroup,
    rho = k/n in {1/2, 1/4, 1/8, 1/16},   k <= 2^40,   p < 2^256,

this emits an EXACT-INTEGER two-sided pin of the finite-slope support-wise MCA
threshold LD_sw, consuming only committed repo theorems:

  * tangent floor (proved, all A):        LD_sw(C, A) >= n - A + 1
  * high-agreement exact (proved):        LD_sw(C, A) = n - A + 1  for
                                          A >= n - floor((n-k)/3)
  * budget bridge:                        eps_mca = LD_sw/q_line, so at target
                                          2^-128 the reserve budget is
                                          B = floor((p-1)/2^128); SAFE iff
                                          numerator <= B, UNSAFE iff >= B+1.

Pin recipe (clean tangent-exact, no per-row two-core work):
    R3 = floor((n-k)/3),  B = R3 + 1.
    Engineer a prime p == 1 (mod n) with floor((p-1)/2^128) = B.  Then
        A_safe   = n - R3      : numerator = R3+1 = B          (exact)  -> SAFE
        A_unsafe = n - R3 - 1  : numerator >= R3+2 = B+1  (tangent floor) -> UNSAFE
    which pins delta*_C to the single agreement step [A_unsafe, A_safe],
    i.e. to 1/n resolution.

Primality is a deterministic Proth certificate: p = u*2^s + 1 with u odd,
u < 2^s (so 2^s > sqrt(p)), and a witness a with a^((p-1)/2) == -1 (mod p).
By Proth's theorem this certifies p prime.  The domain subgroup exists because
n | (p-1).
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Optional

from gmpy2 import is_prime, jacobi, mpz, powmod

TARGET = 128  # security parameter lambda; target error 2^-128
FIELD_CAP = 1 << 256  # admissibility: |F| < 2^256
K_CAP = 1 << 40  # admissibility: k <= 2^40
ADMISSIBLE_RATES = {Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)}


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def proth_prime_in_budget(n: int, B: int, extra_margin: int = 8) -> tuple[int, int, int]:
    """Return (p, s, a): a prime p == 1 (mod n) with floor((p-1)/2^128) = B,
    together with a Proth certificate (2-power s and witness a).

    Search p = 1 + step*t, step = lcm(n, 2^s0), over the half-open budget window
    B*2^128 < p <= (B+1)*2^128.  s0 is chosen so 2^s0 > sqrt(p_hi); the emitted
    s is the full 2-adic valuation of p-1 (>= s0), guaranteeing u = (p-1)/2^s is
    odd and u < 2^s (the Proth condition).
    """
    p_lo = B * (1 << TARGET) + 1          # smallest p with floor((p-1)/2^128)=B
    p_hi = (B + 1) * (1 << TARGET)        # largest such p
    # s0: smallest power of two exceeding sqrt(p_hi), plus margin.
    s0 = (p_hi.bit_length() // 2) + 1 + extra_margin
    step = lcm(n, 1 << s0)
    # first t with p = 1 + step*t >= p_lo
    t = (p_lo - 1 + step - 1) // step
    if t < 1:
        t = 1
    while True:
        p = 1 + step * t
        if p > p_hi:
            raise RuntimeError(f"no prime in budget window for n={n}, B={B} (widen margin)")
        if is_prime(mpz(p)):
            s = ((p - 1) & -(p - 1)).bit_length() - 1  # v2(p-1)
            u = (p - 1) >> s
            assert u % 2 == 1 and u < (1 << s), "Proth condition failed"
            a = proth_witness(p)
            return p, s, a
        t += 1


def proth_witness(p: int) -> int:
    """Smallest a>=2 with a^((p-1)/2) == -1 (mod p) (a quadratic nonresidue)."""
    for a in range(2, 1000):
        if jacobi(a, p) == -1:
            if powmod(a, (p - 1) // 2, p) == p - 1:
                return a
    raise RuntimeError(f"no small Proth witness for p={p}")


@dataclass
class PinCertificate:
    id: str
    rate: str
    n: int
    k: int
    R3: int  # floor((n-k)/3)
    budget_B: int  # floor((p-1)/2^128)
    A_safe: int
    r_safe: int
    numerator_safe: int
    delta_safe: str
    A_unsafe: int
    r_unsafe: int
    numerator_unsafe_lower: int
    delta_unsafe: str
    p: int
    proth_s: int
    proth_u: int
    proth_witness_a: int
    field_bitlength: int

    def checks(self) -> dict:
        p, n, k, B, s, u, a = self.p, self.n, self.k, self.budget_B, self.proth_s, self.proth_u, self.proth_witness_a
        R3 = self.R3
        return {
            "admissible_rate": Fraction(k, n) in ADMISSIBLE_RATES,
            "admissible_k_le_2^40": k <= K_CAP,
            "admissible_field_lt_2^256": p < FIELD_CAP,
            "domain_fits_field": n <= p,
            "subgroup_exists_n_divides_p_minus_1": (p - 1) % n == 0,
            "R3_is_floor": R3 == (n - k) // 3,
            "budget_matches": (p - 1) // (1 << TARGET) == B,
            "budget_equals_R3_plus_1": B == R3 + 1,
            # SAFE side: exact numerator = r_safe+1 = B and B <= budget
            "safe_exact_range": self.r_safe <= (n - k) // 3,
            "safe_numerator_is_r_plus_1": self.numerator_safe == self.r_safe + 1,
            "safe_numerator_le_budget": self.numerator_safe <= B,
            # UNSAFE side: tangent floor >= r_unsafe+1 = B+1 > budget
            "unsafe_floor_is_r_plus_1": self.numerator_unsafe_lower == self.r_unsafe + 1,
            "unsafe_floor_gt_budget": self.numerator_unsafe_lower > B,
            "unsafe_is_adjacent": self.A_unsafe == self.A_safe - 1,
            # exact-integer budget inequalities (the certificate core)
            "exact_safe_ineq_num_2^128_le_p_minus_1": self.numerator_safe * (1 << TARGET) <= p - 1,
            "exact_unsafe_ineq_num_2^128_gt_p_minus_1": self.numerator_unsafe_lower * (1 << TARGET) > p - 1,
            # Proth deterministic primality certificate
            "proth_u_odd": u % 2 == 1,
            "proth_u_lt_2^s": u < (1 << s),
            "proth_2^s_gt_sqrt_p": (1 << s) * (1 << s) > p,
            "proth_p_form": u * (1 << s) + 1 == p,
            "proth_witness_qnr": jacobi(a, p) == -1,
            "proth_witness_pow": powmod(a, (p - 1) // 2, p) == p - 1,
        }


def build_pin(row_id: str, n: int, k: int) -> PinCertificate:
    rate = Fraction(k, n)
    if rate not in ADMISSIBLE_RATES:
        raise ValueError(f"rate {rate} not admissible")
    R3 = (n - k) // 3
    B = R3 + 1
    p, s, a = proth_prime_in_budget(n, B)
    u = (p - 1) >> s
    A_safe = n - R3
    A_unsafe = A_safe - 1
    r_safe = n - A_safe          # = R3
    r_unsafe = n - A_unsafe      # = R3 + 1
    return PinCertificate(
        id=row_id,
        rate=f"{rate.numerator}/{rate.denominator}",
        n=n, k=k, R3=R3, budget_B=B,
        A_safe=A_safe, r_safe=r_safe,
        numerator_safe=r_safe + 1,
        delta_safe=f"{r_safe}/{n}",
        A_unsafe=A_unsafe, r_unsafe=r_unsafe,
        numerator_unsafe_lower=r_unsafe + 1,
        delta_unsafe=f"{r_unsafe}/{n}",
        p=p, proth_s=s, proth_u=u, proth_witness_a=a,
        field_bitlength=int(p).bit_length(),
    )


def two_core_upper_bound(n: int, k: int, A: int) -> tuple[int, int, int]:
    """a426 two-core dichotomy upper bound on LD_sw(C,A); returns
    (max_bound, packing_case, overlap_case). See two_core_closure_general.md."""
    from math import comb
    T = n - A
    t_max = 2 * n + k - 3 * A - 1                 # pairwise complement overlap cap
    if t_max < 0:
        packing = n // T if T > 0 else 0
    else:
        j = t_max + 1
        packing = comb(n, j) // comb(T, j) if (T >= j and n >= j) else n  # n = safe cap
    # Case B overlap max_{n+k-A <= c <= A} floor((n-c)/max(1,A-c)).
    # For c=A-d (d>=1): g(d)=1+floor((n-A)/d), non-increasing in d, so the max is
    # at the smallest admissible d=1 (i.e. c=A-1), provided c=A-1 >= n+k-A; the
    # c=A endpoint (d=0) gives n-A. O(1), no loop (prize scale n=2^44).
    overlap = n - A if A <= n else 0              # c=A endpoint = R3+1
    if (A - 1) >= (n + k - A) and A >= 1:         # c=A-1 in Case-B range
        overlap = max(overlap, 1 + (n - A))       # d=1 -> R3+2
    return max(packing, overlap), packing, overlap


def build_deep_pin(row_id: str, n: int, k: int) -> Dict[str, Any]:
    """One-step-deeper pin: SAFE at A_te-1 (LD_sw = R3+2 exact by the two-core
    closure), UNSAFE at A_te-2 (tangent floor >= R3+3). Budget B_deep = R3+2."""
    rate = Fraction(k, n)
    if rate not in ADMISSIBLE_RATES:
        raise ValueError(f"rate {rate} not admissible")
    R3 = (n - k) // 3
    A_safe = n - R3 - 1                            # = A_te - 1
    A_unsafe = A_safe - 1                          # = A_te - 2
    num_safe = n - A_safe + 1                      # = R3 + 2
    num_unsafe = n - A_unsafe + 1                  # = R3 + 3 (tangent floor)
    B = R3 + 2
    tc_max, tc_pack, tc_overlap = two_core_upper_bound(n, k, A_safe)
    p, s, a = proth_prime_in_budget(n, B)
    u = (p - 1) >> s
    cert = {
        "id": row_id, "rate": f"{rate.numerator}/{rate.denominator}",
        "n": n, "k": k, "R3": R3, "budget_B": B,
        "A_safe": A_safe, "r_safe": n - A_safe, "numerator_safe": num_safe,
        "delta_safe": f"{n - A_safe}/{n}",
        "A_unsafe": A_unsafe, "r_unsafe": n - A_unsafe, "numerator_unsafe_lower": num_unsafe,
        "delta_unsafe": f"{n - A_unsafe}/{n}",
        "two_core": {"max_bound": tc_max, "packing_case": tc_pack,
                     "overlap_case": tc_overlap, "equals_R3_plus_2": tc_max == R3 + 2},
        "p": p, "proth_s": s, "proth_u": u, "proth_witness_a": a,
        "field_bitlength": int(p).bit_length(),
    }
    checks = {
        "rate_admissible": rate in ADMISSIBLE_RATES,
        "k_le_2^40": k <= K_CAP,
        "field_lt_2^256": p < FIELD_CAP,
        "subgroup_exists": (p - 1) % n == 0,
        "budget_matches": (p - 1) // (1 << TARGET) == B,
        "budget_equals_R3_plus_2": B == R3 + 2,
        # SAFE side rests on the two-core closure being exact at A_te-1
        "two_core_closes": tc_max == R3 + 2,
        "safe_numerator_is_R3_plus_2": num_safe == R3 + 2,
        "safe_num_le_budget": num_safe <= B,
        "safe_exact_ineq": num_safe * (1 << TARGET) <= p - 1,
        # UNSAFE side uses only the tangent floor at A_te-2 (>= k+1)
        "unsafe_A_ge_k_plus_1": A_unsafe >= k + 1,
        "unsafe_numerator_is_R3_plus_3": num_unsafe == R3 + 3,
        "unsafe_num_gt_budget": num_unsafe > B,
        "unsafe_exact_ineq": num_unsafe * (1 << TARGET) > p - 1,
        "adjacent": A_unsafe == A_safe - 1,
        # Proth
        "proth_u_odd": u % 2 == 1,
        "proth_u_lt_2^s": u < (1 << s),
        "proth_2^s_gt_sqrt_p": (1 << s) * (1 << s) > p,
        "proth_form": u * (1 << s) + 1 == p,
        "proth_witness_qnr": jacobi(a, p) == -1,
        "proth_witness_pow": powmod(a, (p - 1) // 2, p) == p - 1,
    }
    cert["checks"] = checks
    cert["all_checks_passed"] = all(checks.values())
    return cert


RATE_DEN = {"1_2": 2, "1_4": 4, "1_8": 8, "1_16": 16}


def _grid_rows():
    """Coverage grid: each admissible rate over a range of domain sizes n=2^e
    (finer 1/n resolution as e grows), plus the prize-scale k=2^40 row per rate.
    n must be a power of two >= the rate denominator so k=n/den is integral and
    the redundancy gap n-k >= 3 holds."""
    rows = []
    for label, den in RATE_DEN.items():
        for e in (9, 11, 13, 15, 17, 19):        # n = 2^e domains
            n = 1 << e
            k = n // den
            rows.append((f"rho{label}-n2^{e}-k{k}", n, k))
        # prize-scale row: k = 2^40, n = k * den
        k = 1 << 40
        n = k * den
        rows.append((f"prize-rho{label}-k2^40", n, k))
    return rows


DEFAULT_ROWS = _grid_rows()


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", type=Path, default=None)
    ap.add_argument("--deep-json-out", type=Path, default=None,
                    help="also emit the one-step-deeper two-core pins")
    ap.add_argument("--rows", type=Path, default=None, help="optional JSON list of [id,n,k]")
    args = ap.parse_args(argv)
    rows = DEFAULT_ROWS
    if args.rows:
        rows = [tuple(r) for r in json.loads(args.rows.read_text())]
    out = []
    allok = True
    for row_id, n, k in rows:
        cert = build_pin(row_id, n, k)
        checks = cert.checks()
        ok = all(checks.values())
        allok = allok and ok
        d = asdict(cert)
        d["checks"] = checks
        d["all_checks_passed"] = ok
        out.append(d)
        print(f"[{'OK ' if ok else 'FAIL'}] {row_id}: rate {cert.rate}, n={n}, k={k}, "
              f"pin delta in ({cert.delta_unsafe} unsafe, {cert.delta_safe} safe], "
              f"budget B={cert.budget_B}, |F|=2^{cert.field_bitlength-1}..2^{cert.field_bitlength}")
        if not ok:
            for kk, vv in checks.items():
                if not vv:
                    print(f"        FAILED CHECK: {kk}")
    report = {"target_lambda": TARGET, "num_rows": len(out), "all_rows_passed": allok, "rows": out}
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2))

    if args.deep_json_out:
        deep = []
        for row_id, n, k in rows:
            dc = build_deep_pin(row_id, n, k)
            allok = allok and dc["all_checks_passed"]
            deep.append(dc)
            tc = dc["two_core"]
            print(f"[{'OK ' if dc['all_checks_passed'] else 'FAIL'}] DEEP {row_id}: "
                  f"pin delta in ({dc['delta_unsafe']} unsafe, {dc['delta_safe']} safe], "
                  f"B_deep={dc['budget_B']}, two-core max={tc['max_bound']}=R3+2? {tc['equals_R3_plus_2']}")
            if not dc["all_checks_passed"]:
                for kk, vv in dc["checks"].items():
                    if not vv:
                        print(f"        FAILED CHECK: {kk}")
        deep_report = {"target_lambda": TARGET, "num_rows": len(deep),
                       "all_rows_passed": all(d["all_checks_passed"] for d in deep),
                       "depends_on": "two_core_closure_general.md (generalized a426 two-core upper bound)",
                       "rows": deep}
        args.deep_json_out.write_text(json.dumps(deep_report, indent=2))

    print(f"\nAll rows passed: {allok}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
