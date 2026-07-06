# Multi-rate adjacent-threshold pins (all four grand-challenge rates)

Status: `PROVED_ADJACENT_THRESHOLD_ROW` (finite-slope support-wise line MCA /
`LD_sw`) for eight engineered admissible rows. Exact-integer, deterministic
primality. Dated 2026-07-06.

## What this adds

The repo already pins the finite-slope support-wise MCA threshold for one
`rho=1/2` row (`a426_two_core_exact_threshold_v26.md` / `a425_second_pin_unsafe.md`,
`n=512, k=256`). This packet extends the **same certificate type** to the three
missing grand-challenge rates `rho in {1/4, 1/8, 1/16}` at `n=512`, and to all
four rates at **prize scale** `k=2^40`. Each row engineers a prime field so the
`2^-128` reserve budget lands exactly between two adjacent line-decoding
numerators, pinning `delta*_C` to a single agreement step (`1/n` resolution).

No new theorem is proved. The packet **compiles committed repo theorems** into
new exact-integer rows and is Codex-cross-reviewed and independently verified by
a from-scratch checker.

## Object and consumed theorems (all committed)

For `C = RS[F_p, D, k]` with `|D| = n`, `D` an order-`n` multiplicative subgroup
of `F_p^*` (exists iff `n | p-1`), the finite-slope support-wise line-decoding
numerator `LD_sw(C, A)` satisfies, from existing repo results:

```text
tangent floor (all A >= k+1):        LD_sw(C, A) >= n - A + 1
high-agreement EXACT (A >= n - floor((n-k)/3)):
                                     LD_sw(C, A) = n - A + 1
budget bridge (eps_mca = LD_sw/q_line, target 2^-128):
                                     B = floor((p-1)/2^128);
                                     SAFE  iff LD_sw <= B,
                                     UNSAFE iff LD_sw >= B+1.
```

## The pin recipe

Let `R3 = floor((n-k)/3)` and `B = R3 + 1`. Engineer a prime `p == 1 (mod n)`
with `floor((p-1)/2^128) = B`. Then

```text
A_safe   = n - R3      : LD_sw = R3+1 = B      (high-agreement EXACT)  -> SAFE
A_unsafe = n - R3 - 1  : LD_sw >= R3+2 = B+1   (tangent FLOOR only)    -> UNSAFE
```

so `delta*_C` (for the `LD_sw` object) is pinned to the adjacent step

```text
safe:        closed radius <= R3/n
first unsafe: closed radius = (R3+1)/n.
```

The exact-integer core of each certificate is the pair of inequalities

```text
numerator_safe   * 2^128 <= p-1     (safe),
numerator_unsafe * 2^128 >  p-1     (unsafe),
```

with `numerator_safe = B`, `numerator_unsafe = B+1`.

The SAFE side never leaves the proved-exact range (`r_safe = R3 <= floor((n-k)/3)`),
and the UNSAFE side uses only the tangent floor (`A_unsafe >= k+1`), so the two
sides are strictly weaker inputs than the per-row two-core upper bound used in
`a426`; no two-core packing argument is needed here.

## Deterministic primality (Proth)

Each `p` is engineered as `p = u*2^s + 1` with `u` odd and `u < 2^s` (hence
`2^s > sqrt(p)`). By Proth's theorem, `p` is prime iff some `a` has
`a^((p-1)/2) == -1 (mod p)`; the certificate records such a witness `a`. This is
a deterministic proof, not a probabilistic test. Because `n | 2^s | p-1`, the
order-`n` subgroup domain exists.

## Rows

| id | rho | n | k | budget B | delta (unsafe, safe] | field |
|---|---:|---:|---:|---:|---|---|
| rho1_2-n512-k256 | 1/2 | 512 | 256 | 86 | (86/512, 85/512] | 2^134..2^135 |
| rho1_4-n512-k128 | 1/4 | 512 | 128 | 129 | (129/512, 128/512] | 2^135..2^136 |
| rho1_8-n512-k64 | 1/8 | 512 | 64 | 150 | (150/512, 149/512] | 2^135..2^136 |
| rho1_16-n512-k32 | 1/16 | 512 | 32 | 161 | (161/512, 160/512] | 2^135..2^136 |
| prize-rho1_2-k2^40 | 1/2 | 2^41 | 2^40 | 366503875926 | (…926/n, …925/n] | 2^166..2^167 |
| prize-rho1_4-k2^40 | 1/4 | 2^42 | 2^40 | 1099511627777 | (…777/n, …776/n] | 2^168..2^169 |
| prize-rho1_8-k2^40 | 1/8 | 2^43 | 2^40 | 2565527131478 | (…478/n, …477/n] | 2^169..2^170 |
| prize-rho1_16-k2^40 | 1/16 | 2^44 | 2^40 | 5497558138881 | (…881/n, …880/n] | 2^170..2^171 |

All rows are admissible: `rho in {1/2,1/4,1/8,1/16}`, `k <= 2^40`, `|F| < 2^256`,
`n <= |F|`.

## Complementary near-capacity cap (committed scanner)

Run on each engineered prime field, the committed Paper D universal-cap ledger
(`certificate_scanner.py::paper_d_cap`) additionally certifies the one-sided
near-capacity safe bound `delta*_C <= 1 - rho - 2/n` wherever its
divisor/binomial/subfield hypotheses pass (`PROVED_PAPERD_V8_CAP`):

| id | Paper D cap `delta <= 1-rho-2/N` | hyp margin |
|---|---|---:|
| rho1_2-n512-k256 | 127/256 | 246.3 bits |
| rho1_4-n512-k128 | 191/256 | 150.9 bits |
| rho1_8-n512-k64 | 223/256 | 15.2 bits |
| rho1_16-n512-k32 | (no active cap: `binom(512,34)` below `|F|(q/k+1)` threshold) | — |
| prize-rho1_2..1_16 (k=2^40) | 1-rho-2/n, all four | > 2^41 bits |

So seven of the eight rows carry BOTH a tight line-object pin (this packet) and
a near-capacity full-MCA safe cap (committed scanner); the `rho=1/16, n=512`
field is below the cap's binomial hypothesis and carries the pin only. The two
certificate types concern different objects (`LD_sw` line vs full MCA) and are
not combined into a single bracket.

## Honest scope

These pin the **finite-slope support-wise line** object `LD_sw` (the same object
as `a425`/`a426`), not the full multi-family MCA threshold. The pinned radius is
`~ (1-rho)/3`, well below capacity `1-rho`: it is the exact point where the
committed line-decoding floor crosses the `2^-128` budget, which is a
conservative but rigorous two-sided pin. These are tight (margin `~0`) pins — the
complement to the near-capacity Paper D universal caps (`leaderboard_sweep_192`),
which are one-sided safe bounds with large margin.

## Reproducibility

- Generator: `experimental/scripts/pin_certificate_generator.py`
- Independent verifier (re-derives every pin from `(n,k,p)` alone; does not import
  the generator; cross-checks the committed `a426` prime):
  `experimental/scripts/verify_adjacent_threshold_pins.py`
- Certificate: `experimental/data/certificates/adjacent-threshold-pins-multirate/adjacent_threshold_pins.json`
- Independent-engine cross-check: the committed `certificate_scanner.py`, run on
  the engineered `rho=1/2` prime, reports `finite_line_exact = 86` (`PROVED exact`,
  `safe_at_target = True`) at `A=427` and `tangent_lower = 87 > 86` at `A=426`,
  matching the pin.
