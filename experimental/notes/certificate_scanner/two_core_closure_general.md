# Two-core closure: `LD_sw(C, A_te-1) = n-A+1` for the emitted admissible rows

Status: `PROVED_FOR_EMITTED_ROWS` (generalizes the row-specific two-core upper
bound of `a426_two_core_exact_threshold_v26.md` from `n=512,k=256` to the emitted
admissible-rate grid; the Case-A packing bound is a rate/scale condition,
verified per row -- see the scope caveat). Dated 2026-07-06.

## Statement

Let `C = RS[F, D, k]` with `|D| = n`, `m := n - k`, `R3 := floor(m/3)`, and set
the one-below-tangent-exact agreement

```text
A := n - R3 - 1   (= A_te - 1, one step below the high-agreement exact range A >= n-R3).
```

Then, **for each emitted admissible row** (`rho = k/n in {1/2,1/4,1/8,1/16}` at
the deployed `n in {2^9,...,2^19}` and prize scale `k=2^40`), the finite-slope
support-wise line-decoding numerator satisfies

```text
LD_sw(C, A) = n - A + 1 = R3 + 2      (exact).
```

The lower bound is the committed moving-root tangent floor
`LD_sw(C,A) >= n-A+1`. The content is the matching **upper bound**, a426's
two-core dichotomy, whose two branches we evaluate at these `(n,k)`. Case B is
unconditional (any `m >= 9`); Case A is a bounded per-row check (see the scope
caveat below) -- the code emits a row only when it passes.

## Upper bound (a426 two-core dichotomy, general `(n,k)`)

By the committed exact-support reduction (valid since `A >= k+1`, i.e.
`m - 2 >= R3`, true for `m >= 3`), restrict to exact witness supports
`|S_z| = A` for each bad slope `z` in the noncontained set `Z`.

**Case B — some pair overlaps `>= n+k-A`.** If two witness supports satisfy
`|S_z cap S_w| = c >= n+k-A`, then (since `n+k-A > k`, i.e. `n-A > 0`) the two
explaining degree-`<k` codewords agree on `> k` points and coincide as a common
code-line on `C0`, `|C0| = c`. For any further bad slope, subtracting the common
code-line leaves a degree-`<k` residual with at least `A + c - n >= k` zeros
(using `c >= n+k-A`), hence zero on that overlap; the common-code-line residual
budget then bounds

```text
|Z| <= max_{ n+k-A <= c <= A }  floor( (n-c) / max(1, A-c) ).
```

At `A = n-R3-1`, write `c = A-1 = n-R3-2` (valid: `A-1 >= n+k-A` reduces to
`m - 3 >= 2 R3`, true for `m >= 9`). Then `n-c = R3+2` and `A-c = 1`, giving the
term `R3+2`. Every other `c` gives a strictly smaller floor (`c=A` gives `R3+1`;
`c<=A-2` gives `<= floor((R3+3)/2) < R3+2`). Hence the Case-B bound is exactly

```text
|Z| <= R3 + 2.
```

**Case A — all pairs overlap `<= n+k-A-1`.** Then the complements
`T_z = D \ S_z` (size `n-A = R3+1`) satisfy

```text
|T_z cap T_w| = n - 2A + |S_z cap S_w| <= 2n + k - 3A - 1 =: t_max in {0,1,2},
```

(`t_max = -m + 3 floor(m/3) + 2`, which is `2,1,0` for `m = 0,1,2 mod 3`). Two
distinct complements therefore cannot share any `(t_max+1)`-subset, so the
`(t_max+1)`-subsets of the `T_z` are distinct inside `D` and

```text
|Z| <= floor( binom(n, t_max+1) / binom(n-A, t_max+1) ).
```

This packing bound is `n`-independent up to `O(1/n)` (it tends to
`(3/(1-rho))^{t_max+1}`, e.g. `36, 64, ...`) and is checked to be `<= R3+2` at
every emitted admissible row (see the table: `35, 63, 11, 32, ...`), so on those
rows it never governs. **It is not universal in the rate** -- see the scope caveat.

**Combine (emitted admissible rows).** `LD_sw(C,A) = |Z| <= max(Case A, Case B)`.
Case B `= R3+2` always (`m >= 9`); Case A `<= R3+2` on every emitted row (checked).
Hence `LD_sw(C,A) <= R3+2`, and with the tangent floor `LD_sw(C, A) = R3+2` exactly. QED.

## Scope caveat (the Case-A condition is NOT universal)

The Case-A packing bound `binom(n,t_max+1)/binom(n-A,t_max+1) <= R3+2` is a
**rate-and-scale condition**, not an identity: it can fail for inadmissible rates
or tiny `n`. Counterexample (Codex R1): `n=10, k=1` (`rho=1/10`, inadmissible),
`m=9, R3=3, A=6, t_max=2` gives `binom(10,3)/binom(4,3) = 30 > R3+2 = 5`, so the
combine step would be invalid there. This is why the theorem is scoped to the
emitted admissible rows and the generator/verifier check `packing <= R3+2` per
row (a row that failed the check would not be emitted). For the four admissible
rates the packing constant `(3/(1-rho))^{t_max+1}` is small (`<= 64`) and the
condition holds for all deployed `n >= 2^9`; the claim is not made for arbitrary
`k < n`.

## Per-row numeric witness (verify-first)

`two_core_closure` in `verify_adjacent_threshold_pins.py` recomputes both
branches for each row and asserts `max = R3+2`. Reproduces a426
(`n=512,k=256,A=426`: packing `35`, overlap `87`, `R3+2 = 87`). For the grid:

| rate | n | k | R3 | A_te-1 | packing | overlap | max = R3+2 |
|---|---:|---:|---:|---:|---:|---:|:--:|
| 1/2 | 512 | 256 | 85 | 426 | 35 | 87 | 87 ✓ |
| 1/4 | 512 | 128 | 128 | 383 | 63 | 130 | 130 ✓ |
| 1/8 | 512 | 64 | 149 | 362 | 11 | 151 | 151 ✓ |
| 1/16 | 512 | 32 | 160 | 351 | 32 | 162 | 162 ✓ |

(and identically at `n = 2^11..2^19` and prize scale; packing is `n`-independent
at fixed rate, overlap `= R3+2` always.)

## Consequence: one-step-deeper pins

With `LD_sw(C, A_te-1) = R3+2` exact, engineer a prime `p == 1 (mod n)` with
budget `B_deep = floor((p-1)/2^128) = R3+2`. Then

```text
SAFE   at A_te-1 = n-R3-1 : LD_sw = R3+2 = B_deep      (two-core EXACT)   <= budget
UNSAFE at A_te-2 = n-R3-2 : LD_sw >= R3+3 = B_deep+1   (tangent FLOOR)    >  budget
```

pinning `delta*` for `LD_sw` to the deeper adjacent step
`( (R3+2)/n unsafe, (R3+1)/n safe ]` -- one `1/n` step past the two-core-free
pin. This is the a426 depth, now for all four admissible rates (at the emitted `n`).

## Honest scope

This is the same `LD_sw` line object as `a425`/`a426`; the deeper pin's SAFE side
rests on this two-core closure (a generalization of a426's argument), a strictly
stronger dependency than the two-core-free pin (which uses only the committed
high-agreement exact theorem). Both are emitted and labeled by dependency. The
two-core dichotomy does NOT close two steps below tangent-exact (`A_te-2`): there
`t_max` grows and the packing bound weakens (cf. `a425`'s non-exact fallback), so
the pin cannot be pushed further by this argument.
