#!/usr/bin/env python3
"""Independent verifier for the board near-capacity cap certificates.

Re-derives every row from (rate, k, q) alone -- does NOT import the generator --
and independently re-checks: admissibility, the Paper-D cap hypothesis
binom(n,k+2) >= q*(q//k+1), the committed scanner's cap ledger, the exact-integer
near-capacity unsafe floor 2^128*N_bad > q_line with N_bad = (q-n)//(2k), the
score, and the Proth primality certificate.
"""
from __future__ import annotations
import argparse, importlib.util, json, sys
from fractions import Fraction
from math import comb, log2
from pathlib import Path
from gmpy2 import jacobi, powmod

TARGET = 128
FIELD_CAP = 1 << 256
K_CAP = 1 << 40
ADMISSIBLE = {Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)}
REPO = Path(__file__).resolve().parents[2]
SCANNER = REPO / "experimental/notes/certificate_scanner/certificate_scanner.py"


def load_scanner():
    spec = importlib.util.spec_from_file_location("certificate_scanner", SCANNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def proth_certifies(q):
    m = q - 1
    s = (m & -m).bit_length() - 1
    u = m >> s
    if not (u % 2 == 1 and u < (1 << s) and (1 << s) ** 2 > q):
        return False
    for a in range(2, 1000):
        if jacobi(a, q) == -1 and powmod(a, m // 2, q) == q - 1:
            return True
    return False


def verify_row(row, scanner):
    q, k = int(row["q_line"]), int(row["k"])
    rate = Fraction(1, int(row["rate"].split("/")[1]))
    n = k * rate.denominator                      # n = k/rate
    b = comb(n, k + 2)
    N_bad = (q - n) // (2 * k)
    delta = 1 - rate - Fraction(2, n)
    cap = scanner.paper_d_cap(scanner.Row(n=n, k=k, q_gen=q, q_line=q, q_chal=q,
                                          q_base=q, rate=Fraction(k, n)), TARGET)
    active = [c for c in cap.get("active_caps", []) if c["N"] == n]
    c = {
        "rate_admissible": Fraction(k, n) in ADMISSIBLE,
        "k_le_2^40": k <= K_CAP,
        "field_lt_2^256": q < FIELD_CAP,
        "domain_fits": n <= q,
        "subgroup_exists": (q - 1) % n == 0,
        "smooth_power_of_two": (n & (n - 1)) == 0 and (k & (k - 1)) == 0,
        "k_above_firstgrid_floor": k >= {2: 127, 4: 78, 8: 58, 16: 47}[rate.denominator],
        "cap_hypothesis": b * k >= q * (q + k),
        "scanner_confirms_cap": bool(active),
        "delta_cap_value": f"{delta.numerator}/{delta.denominator}" == row["delta_cap"],
        "agreement_k_plus_2": int(row["agreement_a"]) == k + 2,
        # near-capacity unsafe error floor, exact integers
        "Nbad_formula": N_bad == int(row["N_bad"]),
        "unsafe_2^128_Nbad_gt_q": (1 << TARGET) * N_bad > q,
        "error_floor_exact": (1 << TARGET) * (q - n) > 2 * k * q,
        "score_matches": round(128 + log2(N_bad) - log2(q), 3) == round(float(row["score_bits"]), 3),
        "proth_prime": proth_certifies(q),
        "claim_n": int(row["n"]) == n,
    }
    return all(c.values()), c, round(128 + log2(N_bad) - log2(q), 3)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=REPO / "experimental/data/certificates/"
                    "board-nearcapacity-caps/board_cap_certificates.json")
    args = ap.parse_args(argv)
    scanner = load_scanner()
    report = json.loads(args.json.read_text())
    allok = True
    for row in report["rows"]:
        ok, c, score = verify_row(row, scanner)
        allok = allok and ok
        print(f"[{'OK ' if ok else 'FAIL'}] {row['id']}: rho={row['rate']} k={row['k']} "
              f"delta_cap={row['delta_cap']} score={score}")
        if not ok:
            for kk, vv in c.items():
                if not vv: print(f"       FAILED: {kk}")
    print(f"\nALL VERIFIED: {allok}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
