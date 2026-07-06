#!/usr/bin/env python3
"""Exact checks for the CAP25 v13-raw moved MCA frontier.

This verifies the integer comparisons behind prop:v13-raw-moved-frontier:
  binom(n,m) > p^(m-k-1) floor(q/2^t),
  binom(n,m+1) <= p^(m-k) floor(q/2^t),
and the flexible-budget admissibility and zero-collision inequalities.
"""
from math import comb, lgamma, log, log2, ceil

n = 2**21
k = 2**20
ROWS = [
    ("KoalaBear MCA", 2**31 - 2**24 + 1, 6, 128, 1116047),
    ("Mersenne-31 MCA", 2**31 - 1, 4, 100, 1116023),
]

def log2binom(N: int, M: int) -> float:
    return (lgamma(N + 1) - lgamma(M + 1) - lgamma(N - M + 1)) / log(2)

def main() -> None:
    for name, p, ext, t, m in ROWS:
        q = p**ext
        B = q // (2**t)
        w = m - k - 1
        L = comb(n, m)
        pw = p**w
        assert L > pw * B, (name, "pass comparison failed")
        L_next = L * (n - m) // (m + 1)
        assert L_next <= pw * p * B, (name, "next-row fail comparison failed")
        L0 = B + 1
        assert (L0 * (L0 - 1) // 2) * k < q - n, (name, "admissibility q-n failed")
        assert (L0 * (L0 - 1) // 2) * k < q - p, (name, "admissibility q-|B| failed")
        assert q % (2**t) != 0, (name, "strictness failed")
        N1 = (L + pw - 1) // pw
        assert N1 > B, (name, "fiber lower bound not above budget")
        assert N1 * (N1 - 1) * k < 2 * (q - n), (name, "zero-collision inequality failed")
        pass_margin = log2binom(n, m) - w * log2(p) - log2(B)
        fail_margin = -(log2binom(n, m + 1) - (w + 1) * log2(p) - log2(B))
        print(f"{name}: m={m}, w={w}, edge={(n-m)}/{n}")
        print(f"  pass/fail margins: {pass_margin:.3f} / {fail_margin:.3f} bits")
        print(f"  N1 bit length/log2: {N1.bit_length()} / {log2(N1):.3f}")
        print(f"  safe adjacent={m+1}, finite moment order approx={ceil((w+1)*log2(p)/fail_margin)}")
    print("All exact v13-raw moved-frontier checks passed.")

if __name__ == "__main__":
    main()
