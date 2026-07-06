#!/usr/bin/env python3
"""Independent verifier for the multi-rate adjacent-threshold-pin certificates.

Reads adjacent_threshold_pins.json and, for every row, RE-DERIVES the entire
pin from the primitive data (n, k, p) alone -- it does not trust the stored
A_safe/numerator/budget fields, and it does not import the generator.  It
re-checks:

  * admissibility: rho=k/n in {1/2,1/4,1/8,1/16}, k <= 2^40, p < 2^256, n <= p;
  * domain subgroup exists: n | (p-1);
  * budget:  B = floor((p-1)/2^128) equals floor((n-k)/3)+1;
  * Proth deterministic primality: p = u*2^s+1, u odd, u < 2^s, 2^s > sqrt(p),
    and witness a with jacobi(a,p)=-1 and a^((p-1)/2) == -1 (mod p);
  * SAFE side rests on the committed high-agreement EXACT theorem: at
    A_safe = n-floor((n-k)/3) the exact numerator n-A+1 = B and r_safe lies in
    the proved-exact range r <= floor((n-k)/3), with the exact-integer budget
    inequality  numerator_safe * 2^128 <= p-1;
  * UNSAFE side rests only on the committed tangent FLOOR LD_sw >= n-A+1 at the
    adjacent A_unsafe = A_safe-1 (which is >= k+1), with numerator_unsafe = B+1
    and the exact-integer inequality  numerator_unsafe * 2^128 > p-1.

It additionally cross-checks n=512,k=256 against the committed a425/a426 packet
prime p0 = 22275*2^120+1 (budget 87, safe A>=426, first unsafe A=425).

Exit code 0 iff every row and the a426 cross-check pass.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path

from gmpy2 import jacobi, mpz, powmod

TARGET = 128
FIELD_CAP = 1 << 256
K_CAP = 1 << 40
ADMISSIBLE = {Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)}


def proth_certifies_prime(p: int) -> tuple[bool, dict]:
    """Deterministically certify p prime by Proth's theorem, or fail."""
    if p < 3 or p % 2 == 0:
        return False, {"reason": "p not an odd integer > 2"}
    m = p - 1
    s = (m & -m).bit_length() - 1          # v2(p-1)
    u = m >> s
    facts = {
        "s": s, "u_odd": u % 2 == 1,
        "u_lt_2^s": u < (1 << s),
        "2^s_sq_gt_p": (1 << s) * (1 << s) > p,   # 2^s > sqrt(p), exact
        "p_form_u_2s_plus_1": u * (1 << s) + 1 == p,
    }
    if not (facts["u_odd"] and facts["u_lt_2^s"] and facts["2^s_sq_gt_p"] and facts["p_form_u_2s_plus_1"]):
        return False, facts
    # Proth witness: any a with a^((p-1)/2) == -1 (mod p) proves primality.
    witness = None
    for a in range(2, 1000):
        if jacobi(a, p) == -1 and powmod(a, m // 2, p) == p - 1:
            witness = a
            break
    facts["witness_a"] = witness
    facts["witness_valid"] = witness is not None
    return witness is not None, facts


def verify_row(row: dict) -> tuple[bool, dict]:
    n, k, p = int(row["n"]), int(row["k"]), int(row["p"])
    rho = Fraction(k, n)
    R3 = (n - k) // 3
    B = R3 + 1
    A_safe = n - R3
    A_unsafe = A_safe - 1
    r_safe = n - A_safe            # = R3
    r_unsafe = n - A_unsafe        # = R3 + 1
    num_safe = n - A_safe + 1      # exact numerator (high-agreement exact thm)
    num_unsafe = n - A_unsafe + 1  # tangent floor lower bound

    proth_ok, proth = proth_certifies_prime(p)
    c = {
        # admissibility
        "rate_admissible": rho in ADMISSIBLE,
        "k_le_2^40": k <= K_CAP,
        "field_lt_2^256": p < FIELD_CAP,
        "domain_fits_field": n <= p,
        "subgroup_exists": (p - 1) % n == 0,
        # budget derivation
        "budget_matches_floor": (p - 1) // (1 << TARGET) == B,
        "budget_equals_R3_plus_1": B == R3 + 1,
        # SAFE side (needs high-agreement EXACT range)
        "safe_r_in_exact_range": r_safe <= (n - k) // 3,
        "safe_numerator_value": num_safe == R3 + 1 == B,
        "safe_num_le_budget": num_safe <= B,
        "safe_exact_ineq": num_safe * (1 << TARGET) <= p - 1,
        # UNSAFE side (needs only tangent FLOOR, valid for A >= k+1)
        "unsafe_A_ge_k_plus_1": A_unsafe >= k + 1,
        "unsafe_numerator_value": num_unsafe == R3 + 2 == B + 1,
        "unsafe_num_gt_budget": num_unsafe > B,
        "unsafe_exact_ineq": num_unsafe * (1 << TARGET) > p - 1,
        "adjacent": A_unsafe == A_safe - 1,
        # deterministic primality
        "proth_prime": proth_ok,
        # re-derived quantities agree with what the certificate claims
        "claim_A_safe": int(row["A_safe"]) == A_safe,
        "claim_A_unsafe": int(row["A_unsafe"]) == A_unsafe,
        "claim_budget": int(row["budget_B"]) == B,
        "claim_num_safe": int(row["numerator_safe"]) == num_safe,
        "claim_num_unsafe": int(row["numerator_unsafe_lower"]) == num_unsafe,
    }
    detail = {"n": n, "k": k, "rho": f"{rho.numerator}/{rho.denominator}",
              "R3": R3, "B": B, "A_safe": A_safe, "A_unsafe": A_unsafe,
              "delta_safe": f"{r_safe}/{n}", "delta_unsafe": f"{r_unsafe}/{n}",
              "proth": proth, "checks": c}
    return all(c.values()), detail


def a426_crosscheck() -> tuple[bool, dict]:
    """The committed a425/a426 packet must be reproduced by the same logic."""
    p0 = 22275 * 2**120 + 1
    n, k = 512, 256
    B = (p0 - 1) // (1 << TARGET)
    proth_ok, _ = proth_certifies_prime(p0)
    # a426: safe A>=426 (num 87), first unsafe A=425 (num 88)
    num = lambda A: n - A + 1
    ok = (B == 87 and proth_ok
          and num(426) <= B and num(425) > B
          and (p0 - 1) % n == 0)
    return ok, {"p0_budget": B, "proth_prime": proth_ok,
                "safe_A426_num": num(426), "unsafe_A425_num": num(425),
                "reproduces_a426": ok}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path,
                    default=Path("experimental/data/certificates/"
                                 "adjacent-threshold-pins-multirate/"
                                 "adjacent_threshold_pins.json"))
    args = ap.parse_args(argv)
    report = json.loads(args.json.read_text())
    allok = True
    for row in report["rows"]:
        ok, detail = verify_row(row)
        allok = allok and ok
        print(f"[{'OK ' if ok else 'FAIL'}] {row['id']}: rho={detail['rho']} "
              f"pin delta in ({detail['delta_unsafe']} unsafe, {detail['delta_safe']} safe], B={detail['B']}")
        if not ok:
            for kk, vv in detail["checks"].items():
                if not vv:
                    print(f"       FAILED: {kk}")
    ok426, d426 = a426_crosscheck()
    allok = allok and ok426
    print(f"[{'OK ' if ok426 else 'FAIL'}] a426 committed cross-check: {d426}")
    print(f"\nALL VERIFIED: {allok}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
