# Multi-rate adjacent-threshold pins (all four grand-challenge rates)

Status: `PROVED_ADJACENT_THRESHOLD_ROW` (finite-slope support-wise line MCA /
`LD_sw`) for a grid of **28 engineered admissible rows**. Exact-integer,
deterministic primality. Dated 2026-07-06.

## What this adds

The repo already pins the finite-slope support-wise MCA threshold for one
`rho=1/2` row (`a426_two_core_exact_threshold_v26.md` / `a425_second_pin_unsafe.md`,
`n=512, k=256`). This packet extends the **same certificate type** to a coverage
grid: **all four grand-challenge rates** `rho in {1/2, 1/4, 1/8, 1/16}` over
domain sizes `n in {2^9, 2^11, 2^13, 2^15, 2^17, 2^19}` (finer `1/n` resolution
as `n` grows) **plus the prize scale** `k=2^40` for each rate. Each row engineers
a prime field so the `2^-128` reserve budget lands exactly between two adjacent
line-decoding numerators, pinning `delta*_C` to a single agreement step
(`1/n` resolution). The board-format curation of all 28 rows (pins + the
complementary Paper D caps) is in `adjacent_threshold_pins_board.md`.

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

28 rows = 4 rates x {`n=2^9,2^11,2^13,2^15,2^17,2^19`} + 4 prize-scale (`k=2^40`).
Representative rows (full list, with per-row primes and Proth witnesses, in
`adjacent_threshold_pins.json`; board-format table in `adjacent_threshold_pins_board.md`):

| id | rho | n | k | budget B | delta (unsafe, safe] | field bits |
|---|---:|---:|---:|---:|---|---|
| rho1_2-n2^9-k256 | 1/2 | 512 | 256 | 86 | (86/512, 85/512] | 135 |
| rho1_2-n2^19-k262144 | 1/2 | 524288 | 262144 | 87382 | (87382/n, 87381/n] | 145 |
| rho1_16-n2^9-k32 | 1/16 | 512 | 32 | 161 | (161/512, 160/512] | 136 |
| prize-rho1_2-k2^40 | 1/2 | 2^41 | 2^40 | 366503875926 | (…926/n, …925/n] | 167 |
| prize-rho1_16-k2^40 | 1/16 | 2^44 | 2^40 | 5497558138881 | (…881/n, …880/n] | 171 |

All 28 rows are admissible: `rho in {1/2,1/4,1/8,1/16}`, `k <= 2^40`,
`|F| < 2^256`, `n <= |F|`. As `n` grows the pin resolution `1/n` sharpens (the
`rho=1/2` pin tightens from `1/512` at `n=2^9` to `1/524288` at `n=2^19`).

## Complementary near-capacity cap (committed scanner)

Run on each engineered prime field, the committed Paper D universal-cap ledger
(`certificate_scanner.py::paper_d_cap`) additionally certifies the one-sided
near-capacity safe bound `delta*_C <= 1 - rho - 2/n` wherever its
divisor/binomial/subfield hypotheses pass (`PROVED_PAPERD_V8_CAP`). **27 of the
28 rows carry BOTH** a tight line-object pin (this packet) and a near-capacity
full-MCA safe cap; the sole exception is the smallest low-rate field
`rho=1/16, n=512` (`binom(512,34)` is below the cap's `|F|(q/k+1)` binomial
threshold), which carries the pin only. Per-row caps + margins are tabulated in
`adjacent_threshold_pins_board.md` (Table 2). The two certificate types concern
different objects (`LD_sw` line vs full MCA) and are not combined into a single
bracket.

## One-step-deeper pins (two-core closure)

`two_core_closure_general.md` proves `LD_sw(C, A_te-1) = R3+2` **exactly** for
each emitted admissible row, by evaluating a426's two-core dichotomy at these
`(n,k)` (a generalization of a426's single-row upper bound; the Case-A packing
branch is a per-row-checked rate/scale condition, not universal in the rate). That lets
each pin be pushed one `1/n` step deeper (matching a426's depth, now for all four
rates): SAFE at `A_te-1` (`LD_sw = R3+2 = B_deep`, two-core exact), UNSAFE at
`A_te-2` (`LD_sw >= R3+3`, tangent floor), budget `B_deep = R3+2`. These 28 deeper
pins are in `adjacent_threshold_pins_deep.json`, each carrying its two-core
witness (`packing`, `overlap`, `max = R3+2`), independently re-derived by the
verifier. Their SAFE side rests on the two-core closure (a strictly stronger
dependency than the two-core-free pins below), and the dichotomy does **not**
close at `A_te-2` (`cf. a425`'s non-exact fallback), so this is the deepest pin
the argument reaches.

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
- Board-format curation (pins + Paper D caps): `experimental/scripts/curate_pin_board.py`
  -> `experimental/notes/certificate_scanner/adjacent_threshold_pins_board.md`
- Independent-engine cross-check: the committed `certificate_scanner.py`, run on
  the engineered `rho=1/2` prime, reports `finite_line_exact = 86` (`PROVED exact`,
  `safe_at_target = True`) at `A=427` and `tangent_lower = 87 > 86` at `A=426`,
  matching the pin.
