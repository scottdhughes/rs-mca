# CAP25 v13 Q-fin primitive wall synthesis

Status: AUDIT / EXACT_NEW_WALL / ROUTE_CUT.

This note records the corrected finite Q-fin target left after the
mode-at-null route cut.  It does not prove the adjacent upper ledger and does
not prove

```text
U(1116048) <= B*.
```

Its purpose is narrower: normalize the deployed KoalaBear MCA constants,
separate target-vector symmetry from support quotient structure, and record the
moment-order barrier for the remaining primitive max-orbit flatness problem.

## Source of row authority

There are two experimental row layers in the repository.

* `experimental/cap25_v13_experimental.tex` still contains an older
  identity-frontier table with KoalaBear MCA `(1116043,1116044)`.
* `AGENTS.md` may also contain older experimental target text from before the
  moved-frontier update.
* `experimental/rs_mca_proximity_prize_status.md` is the current
  committee-facing status memo.  It lists KoalaBear MCA as
  `(1116047,1116048)` with a finite fail margin of about `22.2` bits.

This note uses the status memo and the moved-frontier checker as authority for
the live finite adjacent row, not as a proof of the upper ledger.  The checker
verifies the identity-floor lower-side comparisons

```text
binom(n,1116047) > p^67470 B*,
binom(n,1116048) <= p^67471 B*.
```

Thus the current finite target is

```text
unsafe a0 = 1116047,
candidate adjacent row = 1116048,
desired but still-open certificate: U(1116048) <= B* < L_id(1116047).
```

The exact moved-frontier checker is
`experimental/scripts/towards v13/cap25_v13_raw_moved_frontier_checks.py`.

## Live KB-MCA constants

For the deployed KoalaBear MCA row,

```text
p = 2^31 - 2^24 + 1 = 2130706433,
q = p^6,
n = 2^21 = 2097152,
k = 2^20 = 1048576,
B* = floor(q / 2^128) = 274980728111395087.
```

At the unsafe and adjacent safe rows,

```text
m_unsafe = 1116047,   w_unsafe = m_unsafe - k - 1 = 67470,
m_safe   = 1116048,   w_safe   = m_safe   - k - 1 = 67471.
```

The moved-frontier checker reports:

```text
KoalaBear MCA: m=1116047, w=67470, edge=981105/2097152
  pass/fail margins: 8.978 / 22.197 bits
  N1 bit length/log2: 67 / 66.910
  safe adjacent=1116048, finite moment order approx=94196
```

For the safe-row prefix map, the average fiber size is

```text
avg = binom(n,m_safe) / p^w_safe,
log2(avg) ~= 35.735246417.
```

The available finite budget relative to this average is

```text
log2(B*) ~= 57.932108125,
log2(B*/avg) ~= 22.196861708,
floor(B* p^w_safe / binom(n,m_safe)) = 4807520.
```

Thus a primitive max-fiber theorem for the safe row must fit inside about
`22.197` bits of raw slack.  For an integer multiplier certificate, the raw
ambient cap is `4807520` times the exact average before any other first-match
ledger losses are charged.

## Correct Q-fin object

For a multiplicative-coset domain `D = alpha * mu_n`, define the prefix moment
map on `m`-subsets by

```text
Phi_w(M) = (p_1(M), ..., p_w(M)),
p_i(M) = sum_{x in M} x^i.
```

The previous note
`experimental/notes/thresholds/cap25_v13_qfin_mode_at_null_route_cut.md`
shows that the shortcut

```text
|Phi_w^{-1}(z)| <= |Phi_w^{-1}(0)|
```

is false even in the toy row `D = F_17^*`, `m = 9`, `w = 1`.  The remaining
primitive target is therefore max-orbit flatness, not null-fiber extremality:

```text
max_{gcd(n,I(z)) = 1} |Phi_w^{-1}(z)| <= K_rem * avg,
I(z) = { i <= w : z_i != 0 }.
```

For the raw KB-MCA safe-row Q-fin cell before additional ledger charges, the
ambient integer multiplier cap is

```text
K_raw = floor(B* p^w_safe / binom(n,m_safe)) = 4807520.
```

The actual remaining constant `K_rem` must be no larger than `K_raw` after
tangent, quotient, extension, sparse/M1, planted/divisor, and residual cells
are deducted in an exact first-match ledger.

## Target stabilizer is not support quotient

The twist action `M -> zeta M` preserves fiber sizes while sending

```text
(z_1, ..., z_w) -> (zeta z_1, ..., zeta^w z_w).
```

The target-vector stabilizer is

```text
Stab(z) = { zeta in mu_n : zeta^i z_i = z_i for every i <= w }
        = mu_{gcd(n,I(z))}.
```

Here `gcd(n,empty set)=n`, so the all-zero target has full target stabilizer.
More generally, `mu_{gcd(n,I(z))}` denotes the unique subgroup of `mu_n` of
that order.

This is a target-vector property, not a support-level quotient certificate.
One explicit witness is over `D=F_17^*`, with `m=4` and `w=2`:

```text
M = {1, 2, 4, 10},
p_1(M) = 0,
p_2(M) = 2.
```

The target `z = (0,2)` has a nontrivial target stabilizer `mu_2`, but the
support `M` is not a union of `{x,-x}` cosets.  Consequently, stabilized
targets require image-level quotient descent or another explicit ledger
payment; raw support-level quotient counting is not justified by target
stabilizer alone.

## Prefix-collision rigidity and the live off-by-one

If two distinct `m`-subsets have the same first `w` prefixes, write their
locator polynomials as

```text
Lambda_M  = G A,
Lambda_M' = G B,
deg(A) = deg(B) = e = |M \ M'|.
```

In the live row `p>w`, so equality of the first `w` power sums is equivalent,
via Newton identities, to equality of the first `w` top locator
coefficients.  Hence

```text
deg(Lambda_M - Lambda_M') <= m - w - 1.
```

Since `Lambda_M - Lambda_M' = G(A-B)` and `deg(G)=m-e`, this forces

```text
deg(A-B) <= e - w - 1.
```

For `A != B`, this implies

```text
e >= w + 1.
```

At the live KB-MCA safe row,

```text
w = 67471,
w + 1 = 67472,
gcd(2^21, 67472) = 16,
67472 does not divide 2^21.
```

Thus the exact live statement is not the stronger but false shorthand
`gcd(n,w+1)=1`; the correct observation is only that the full minimal
constant-shift prototype requiring `(w+1) | n` is absent at this row.  This
does not, by itself, prove primitive flatness.

## Moment barrier

A soft moment route is too weak for the finite adjacent certificate.  If an
`r`-th moment bridge has the schematic form

```text
max primitive fiber <= avg * p^{w/r}
```

up to constants, then fitting inside the `22.1968617` bit KB-MCA safe-row
slack requires roughly

```text
r >= ceil(w_safe log2(p) / log2(B*/avg)) = 94196
```

even before any extra moment constants are included.  This explains why low
moments, second-moment collision ledgers, and typical-fiber equidistribution
are useful for calibration and descent, but cannot by themselves close the
finite KB-MCA adjacent row.

## Non-claims

This note does not prove any of the following:

```text
U(1116048) <= B*,
primitive max-orbit flatness at the deployed row,
quotient payment from target-vector stabilizer alone,
mode-at-null in any range beyond the already refuted toy shortcut,
or a low-moment proof of the finite safe side.
```

It also does not assert that the older `(1116043,1116044)` experimental table
is wrong in its own context; it records that the committee-facing finite
adjacent target has moved to `(1116047,1116048)`.

## Next exact wall

The live Q-fin wall is:

```text
CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048.
```

The most useful next theorem or counterpacket would do one of the following:

1. prove a fixed-prime primitive max-orbit flatness theorem with explicit
   finite constant below the remaining first-match budget;
2. produce a primitive target vector at the KB-MCA row whose fiber exceeds the
   corrected remaining budget;
3. replace max-orbit flatness by an image-level quotient/descent compiler with
   exact per-rung bit losses; or
4. prove a sharper structural theorem showing that any heavy primitive fiber
   forces a paid nonprimitive, planted, tangent, extension, or residual branch.
