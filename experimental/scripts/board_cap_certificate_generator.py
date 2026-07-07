#!/usr/bin/env python3
"""Board-scoring Paper-D near-capacity cap certificates for rho in {1/4,1/8,1/16}
(and 1/2), targeting the rsmca.xyz MCA leaderboard.

Each row is an admissible RS[F_q, D, k] with D an order-n multiplicative subgroup,
rho = k/n in {1/2,1/4,1/8,1/16}, at the Paper-D cap divisor N=n: the cap proves
the SAFE bound  delta*_C <= 1 - rho - 2/n, and at that near-capacity radius the
Paper-D error FLOOR  eps >= (q-n)/(2kq)  makes it UNSAFE against target 2^-128,
with proved bad-slope effective numerator

    N_bad = floor((q-n)/(2k)),     certificate:  2^128 * N_bad > q_line,
    score = 128 + log2(N_bad) - log2(q_line)  ~  127 - log2(k).

The field is engineered near the cap ceiling `q <= isqrt(binom(n,k+2)*k)` (with a
safety margin) to maximize the score, as a Proth-certifiable prime `q == 1 (mod n)`.
The committed scanner (certificate_scanner.paper_d_cap) independently confirms the
cap. Current board MCA-cap best: rho=1/2 -> +119, rho in {1/4,1/8,1/16} -> +87;
these rows land at ~+120..+121.5.
"""
from __future__ import annotations
import argparse, json, importlib.util, sys
from dataclasses import dataclass, asdict
from fractions import Fraction
from math import comb, gcd, isqrt, log2
from pathlib import Path
from gmpy2 import is_prime, jacobi, mpz, powmod

TARGET = 128
FIELD_CAP = 1 << 256
K_CAP = 1 << 40
ADMISSIBLE = {Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)}
# SMOOTH power-of-two k = 2^j, chosen as the smallest power of two at or above the
# site's first-grid k-floor for each rate (127/78/58/47), so n = k/rho is a
# power of two (smooth FFT domain) AND k respects the board-admissible floor.
KFLOOR = {2: 128, 4: 128, 8: 64, 16: 64}
REPO = Path(__file__).resolve().parents[2]
SCANNER = REPO / "experimental/notes/certificate_scanner/certificate_scanner.py"


def lcm(a, b): return a // gcd(a, b) * b


def largest_cap_prime(n, k, margin_bits=8):
    """Largest Proth-certifiable prime q == 1 (mod n) satisfying Paper-D's exact
    cap condition binom(n,k+2) >= q*(q/k+1), in exact-integer form binom*k >= q*(q+k),
    with a `margin_bits` safety headroom, q < 2^256."""
    b = comb(n, k + 2)
    q_ceiling = isqrt(b * k)                       # q^2/k <~ binom
    q_ceiling = min(q_ceiling, FIELD_CAP - 1)
    # back off to keep an exact-integer margin: binom >= 2^margin * q*(q//k+1)
    while q_ceiling > n and b * k < (1 << margin_bits) * q_ceiling * (q_ceiling + k):
        q_ceiling -= max(1, q_ceiling >> 20)
    # Proth: q = 1 + step*t, step = lcm(n, 2^s), 2^s > sqrt(q); search t downward.
    s = (q_ceiling.bit_length() // 2) + 1 + 8
    step = lcm(n, 1 << s)
    t = q_ceiling // step
    while t >= 1:
        q = 1 + step * t
        if q <= q_ceiling and is_prime(mpz(q)):
            sv = ((q - 1) & -(q - 1)).bit_length() - 1
            u = (q - 1) >> sv
            if u % 2 == 1 and u < (1 << sv) and (1 << sv) * (1 << sv) > q:
                a = next(a for a in range(2, 1000)
                         if jacobi(a, q) == -1 and powmod(a, (q - 1) // 2, q) == q - 1)
                return q, sv, u, a
        t -= 1
    raise RuntimeError(f"no cap prime for n={n}, k={k}")


def load_scanner():
    spec = importlib.util.spec_from_file_location("certificate_scanner", SCANNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@dataclass
class CapRow:
    id: str; rate: str; n: int; k: int; N: int
    delta_cap: str; agreement_a: int; sigma: int
    q_line: int; N_bad: int; score_bits: float
    proth_s: int; proth_u: int; proth_witness_a: int; field_bitlength: int

    def checks(self, scanner):
        q, n, k = self.q_line, self.n, self.k
        b = comb(n, k + 2)
        cap = scanner.paper_d_cap(scanner.Row(n=n, k=k, q_gen=q, q_line=q, q_chal=q,
                                              q_base=q, rate=Fraction(k, n)), TARGET)
        active = [c for c in cap.get("active_caps", []) if c["N"] == n]
        return {
            "admissible_rate": Fraction(k, n) in ADMISSIBLE,
            "admissible_k_le_2^40": k <= K_CAP,
            "admissible_field_lt_2^256": q < FIELD_CAP,
            "domain_fits_field": n <= q,
            "subgroup_exists": (q - 1) % n == 0,
            "smooth_power_of_two_domain": (n & (n - 1)) == 0 and (k & (k - 1)) == 0,
            "k_above_firstgrid_floor": k >= {2: 127, 4: 78, 8: 58, 16: 47}[n // k],
            "cap_hypothesis_binom": b * k >= q * (q + k),
            "scanner_confirms_cap_at_N=n": bool(active),
            "delta_cap_matches": active and active[0]["delta_cap_fraction"] == self.delta_cap,
            "agreement_is_k_plus_2": self.agreement_a == k + 2,
            "sigma_is_2": self.sigma == 2,
            # unsafe near-capacity floor: eps=(q-n)/(2kq) > 2^-128
            "Nbad_value": self.N_bad == (q - n) // (2 * k),
            "unsafe_exact_2^128_Nbad_gt_q": (1 << TARGET) * self.N_bad > q,
            "error_floor_gt_target_exact": (1 << TARGET) * (q - n) > 2 * k * q,
            # Proth
            "proth_form": self.proth_u * (1 << self.proth_s) + 1 == q,
            "proth_u_odd": self.proth_u % 2 == 1,
            "proth_u_lt_2^s": self.proth_u < (1 << self.proth_s),
            "proth_2^s_gt_sqrt_q": (1 << self.proth_s) ** 2 > q,
            "proth_witness_qnr": jacobi(self.proth_witness_a, q) == -1,
            "proth_witness_pow": powmod(self.proth_witness_a, (q - 1) // 2, q) == q - 1,
        }


def build_cap_row(row_id, den, k):
    rate = Fraction(1, den)
    n = den * k
    assert Fraction(k, n) in ADMISSIBLE
    q, s, u, a = largest_cap_prime(n, k)
    N_bad = (q - n) // (2 * k)
    delta = 1 - rate - Fraction(2, n)
    return CapRow(
        id=row_id, rate=f"1/{den}", n=n, k=k, N=n,
        delta_cap=f"{delta.numerator}/{delta.denominator}",
        agreement_a=k + 2, sigma=2, q_line=q, N_bad=N_bad,
        score_bits=round(128 + log2(N_bad) - log2(q), 3),
        proth_s=s, proth_u=u, proth_witness_a=a, field_bitlength=q.bit_length())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args(argv)
    scanner = load_scanner()
    out, allok = [], True
    for den in (2, 4, 8, 16):
        k = KFLOOR[den]
        row = build_cap_row(f"board-cap-rho1_{den}-k{k}-Nn", den, k)
        chk = row.checks(scanner)
        ok = all(chk.values())
        allok = allok and ok
        d = asdict(row); d["checks"] = chk; d["all_checks_passed"] = ok
        out.append(d)
        print(f"[{'OK ' if ok else 'FAIL'}] rho=1/{den} k={k} n={row.n}: delta_cap={row.delta_cap} "
              f"|F|=2^{row.field_bitlength} score={row.score_bits}  (board best was {'119' if den==2 else '87'})")
        if not ok:
            for kk, vv in chk.items():
                if not vv: print(f"       FAILED: {kk}")
    report = {"target_lambda": TARGET, "track": "mca-nearcapacity-cap", "rows": out,
              "all_rows_passed": allok}
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2))
    print(f"\nAll rows passed: {allok}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
