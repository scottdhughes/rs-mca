# New result: dyadic quotient-core MCA floor through agreement 352

## Claim

For every multiplicative subgroup `H <= GF(17^32)^*` of order `512`, let

```text
C = RS[GF(17^32), H, 256].
```

Under the finite-slope support-wise MCA convention,

```text
LD_sw(C, a) >= 7 for every 264 <= a <= 352.
```

At the deepest guaranteed rung,

```text
LD_sw(C, 352) >= 16.
```

Since

```text
7 * 2^128 > 17^32,
```

this gives

```text
epsilon_mca(C, 5/16) > 2^-128.
```

## Proof idea

Use dyadic quotient maps

```text
x -> x^c,   c in {4, 8, 16, 32}
```

from `H` onto quotients `Q_c = H^c` of sizes `128, 64, 32, 16`.  The quotient
`Q_c` lies in `GF(17^d)`, where `d = ord_{512/c}(17)`.

For agreement `a = cm + r`, fix `r` exceptional points in one quotient fiber and
choose `m` full quotient fibers.  The locator is

```text
L_A(X) = E_T(X) * product_{y in A}(X^c - y).
```

For the augmented code

```text
C^+ = RS[GF(17^32), H, 257],
```

only degrees `257,...,a-1` need to be fixed.  Those high coefficients depend
only on the short quotient prefix

```text
(e_1(A), ..., e_s(A)),    s = floor((a - 257)/c).
```

Pigeonholing over the small quotient field gives a large family of locators with
common high coefficients. The common-high-coefficient template gives an
augmented-code list. A quantitative deep-point conversion then turns that list
into distinct support-wise MCA-bad slopes.

## Guaranteed table

| agreements | c | quotient size | quotient field degree | guaranteed bad slopes |
|---:|---:|---:|---:|---:|
| 264 | 4 | 128 | 8 | 3,226,994,007,649,539,012,619,581,430 |
| 265--267 | 4 | 128 | 8 | 224,072,473,307,858,360 |
| 268 | 4 | 128 | 8 | 428,078,754,976,207,015 |
| 269--271 | 8 | 64 | 4 | 10,306,126,669,871 |
| 272 | 8 | 64 | 4 | 19,399,767,849,168 |
| 273--279 | 8 | 64 | 4 | 108,878,500 |
| 280 | 8 | 64 | 4 | 199,092,114 |
| 281--287 | 16 | 32 | 2 | 917,587 |
| 288 | 16 | 32 | 2 | 1,631,266 |
| 289--303 | 16 | 32 | 2 | 2,470 |
| 304 | 16 | 32 | 2 | 4,160 |
| 305--319 | 32 | 16 | 1 | 295 |
| 320 | 32 | 16 | 1 | 472 |
| 321--351 | 32 | 16 | 1 | 11 |
| 352 | 32 | 16 | 1 | 16 |

## New frontier

The coarse dyadic quotient-prefix method stops at agreement `353`: the best
coarse row there gives only three slopes.

The next problem is therefore:

```text
agreement 353 / slack 97 / delta = 159/512.
```

Either find genuine quotient-prefix collisions or prove all quotient-periodic,
tangent, and aperiodic branches at agreement 353 stay below seven slopes.

## Non-claims

This does not prove the full Proximity Prize threshold. It does not prove an
upper bound at 353. It is not a protocol theorem. It is a support-wise MCA lower
floor under the finite-slope convention.
