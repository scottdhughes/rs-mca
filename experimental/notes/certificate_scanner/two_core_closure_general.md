# Two-core closure: `LD_sw(C, A_te-1) = n-A+1` for the emitted admissible rows

Status: `PROVED` for the admissible rates `rho in {1/2,1/4,1/8,1/16}` at **every
power-of-two `n >= 512`** (the universal-in-`n` packing lemma below discharges
Case A for all such `n`, not just per row); generalizes the single-row two-core
upper bound of `a426_two_core_exact_threshold_v26.md` (`n=512,k=256`). It is NOT
claimed for arbitrary `k < n` -- see the scope caveat. Dated 2026-07-06.

**Machine-checked (twice, independently).** The universal packing lemma (Case A,
below) is formally verified in Lean 4 + Mathlib by two independent provers, each
`lake build`-clean with `#print axioms` reporting only
`[propext, Classical.choice, Quot.sound]` (no `sorryAx`):
- `experimental/lean/two_core_packing/` -- `theorem universal_packing`
  (Lean v4.31), `e`-symbolic over `e >= 9` and `den in {2,4,8,16}`: exactly the
  four admissible rates of the claim below.
- `experimental/lean/dyadic_packing/` -- `theorem dyadic_packing_bound`
  (Lean v4.28), the **strictly stronger** statement for **every dyadic rate**
  `rho = 2^{-i}` (`i >= 1`, `n = 2^e >= 512`, `i <= e`). This proves Case A -- and
  hence the whole two-core closure -- for all dyadic-rate RS codes, not just the
  prize four.

(Case B and the tangent-floor / exact-support inputs are the committed
coding-theory results, not re-formalized.)

## Statement

Let `C = RS[F, D, k]` with `|D| = n`, `m := n - k`, `R3 := floor(m/3)`, and set
the one-below-tangent-exact agreement

```text
A := n - R3 - 1   (= A_te - 1, one step below the high-agreement exact range A >= n-R3).
```

Then, **for `rho = k/n in {1/2,1/4,1/8,1/16}` and every power-of-two `n >= 512`**,
the finite-slope support-wise line-decoding numerator satisfies

```text
LD_sw(C, A) = n - A + 1 = R3 + 2      (exact).
```

The lower bound is the committed moving-root tangent floor
`LD_sw(C,A) >= n-A+1`. The content is the matching **upper bound**, a426's
two-core dichotomy, whose two branches we bound at these `(n,k)`: Case B `= R3+2`
unconditionally (any `m >= 9`), and Case A `<= R3+2` by the universal packing
lemma below.

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

### Universal packing lemma (admissible rates, power-of-two `n >= 512`)

**Claim.** For `rho in {1/2,1/4,1/8,1/16}` and `n = 2^e >= 512`, with
`j := t_max+1`, `binom(n,j)/binom(R3+1,j) <= R3+2`.

**(i) `j` is bounded by the rate.** `t_max = -m + 3 floor(m/3) + 2 = 2 - (m mod 3)`,
so `j = t_max+1 = 3 - (m mod 3)`, and `m = (1-rho) n`:
- `rho=1/2`: `m = 2^{e-1}`, never `= 0 (mod 3)`; `2^{e-1} mod 3` alternates `2,1` with `e`,
  so `j` alternates in `{1,2}` (`j <= 2`);
- `rho=1/8`: `m = 7*2^{e-3}`, `7 = 1 (mod 3)`, so `m = 2^{e-3} (mod 3) in {1,2}` alternating,
  `j in {1,2}` (`j <= 2`);
- `rho=1/4`: `m = 3*2^{e-2} = 0 (mod 3)`, so `j = 3` (constant in `e`);
- `rho=1/16`: `m = 15*2^{e-4}`, `15 = 0 (mod 3)`, so `j = 3` (constant in `e`).

So for every `e`, `j <= 2` for `rho in {1/2,1/8}` and `j = 3` for `rho in {1/4,1/16}` --
`j` need not be constant in `e`, but it is bounded per rate, which is all Step (iii) uses.

**(ii) A closed-form packing bound.** The factors of
`binom(n,j)/binom(R3+1,j) = prod_{i=0}^{j-1} (n-i)/(R3+1-i)` are increasing in `i`
(since `n > R3+1`), so each is `<= (n-j+1)/(R3-j+2) <= n/(R3-j+2)`. With
`R3 = floor(m/3) >= (m-2)/3` and `j <= 3`, `R3-j+2 >= (m-2)/3 - 1 = (m-5)/3 = ((1-rho)n-5)/3`,
hence

```text
binom(n,j)/binom(R3+1,j) <= ( 3n / ((1-rho)n - 5) )^j = ( 3 / ((1-rho) - 5/n) )^j.
```

**(iii) Compare to `R3+2`.** `R3+2 >= (m-2)/3 + 2 = (1-rho)n/3 + 4/3 > (1-rho)n/3`.
It remains to check `( 3/((1-rho)-5/n) )^j <= (1-rho)n/3` for all `n >= 512`.
Since the base `3/((1-rho)-5/n) > 1`, the left side is increasing in `j`, so it
suffices to check the **worst-case (largest) `j`** each rate can take (by (i):
`j=2` for `rho in {1/2,1/8}`, `j=3` for `rho in {1/4,1/16}`). At that `j` the left
side is decreasing in `n` and the right side increasing, so it suffices at `n=512`:
`rho=1/2, j=2`: `(3/(0.5-0.01))^2 = 37.5 <= 85.3`;
`rho=1/8, j=2`: `12.0 <= 149.3`;
`rho=1/4, j=3`: `66.6 <= 128`;
`rho=1/16, j=3`: `33.8 <= 160`.
All hold, and by monotonicity for every `n >= 512` and every admissible actual `j`.
Hence `binom(n,j)/binom(R3+1,j) <= R3+2`. QED.

(Deployed values at `n=512`: packing `35, 63, 11, 32`; the slack only grows with
`n`. For the `j=3` rates packing is `n`-independent (`63, 32`); for the `j in {1,2}`
rates it alternates with `e` but stays below the `j=2` worst case -- densely
re-checked to `n=2^30` in the generator's development.)

**Combine.** `LD_sw(C,A) = |Z| <= max(Case A, Case B) = R3+2` (Case B `= R3+2`
for `m>=9`; Case A `<= R3+2` by the lemma). With the tangent floor,
`LD_sw(C, A) = R3+2` exactly. QED.

## Scope caveat (NOT universal in the rate)

The lemma uses `j = 3 - (m mod 3)` being pinned by `rho` (step (i)) and the small
packing constant of the four admissible rates. It is **not** an identity for
arbitrary `k < n`: e.g. `n=10, k=1` (`rho=1/10`, inadmissible), `m=9, j=3` gives
`binom(10,3)/binom(4,3) = 30 > R3+2 = 5` (Codex R1). The claim is made only for
the four grand-challenge rates at power-of-two `n >= 512`; the generator/verifier
additionally check `packing <= R3+2` per row, so any non-power-of-two or otherwise
out-of-scope row would be caught rather than silently emitted.

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

(and identically at `n = 2^10..2^21` and prize scale; overlap `= R3+2` always;
packing is `n`-independent for the `j=3` rates `1/4,1/16` (`63, 32`) and
alternates in `e` for the `j in {1,2}` rates `1/2,1/8` (e.g. `35, 5, 35, ...`),
always `<= R3+2` by the lemma above.)

## Connection to prize-DAG node `a426_universal_numerator`

The first grid row (`rho=1/2, n=512, k=256`) is exactly the prize-DAG node
**`a426_universal_numerator`**: "`LD_sw(RS[F,D,256],426) = 87` for **every** field
`F` and **every** 512-point domain `D`" (`A_te-1 = 512-85-1 = 426`, `R3+2 = 87`).
As of the live DAG (allengrahamhart.github.io/prize-dag) that node is still
`PROVABLE`, its proof written but un-integrated (PR #204, a Hankel-free single-row
argument).

**This theorem proves it — and generalizes it.** The domain/field universality the
node asks for is intrinsic here: the statement is `C = RS[F, D, k]` for an arbitrary
`n`-point `D` over an arbitrary `F`, and neither branch of the dichotomy uses any
structure of `D` beyond `|D| = n` (Case A is the purely combinatorial packing lemma;
Case B is the code-line overlap argument; the tangent-floor and exact-support inputs
are the committed general-`D` results). So the `= 87` value holds for every field and
every 512-domain, matching the node verbatim. Beyond the node, this theorem also
covers **all four admissible rates and every power-of-two `n >= 512`** (the grid
above), and its Case-A crux is **Lean-verified twice** (`two_core_packing`,
`dyadic_packing`) — strictly stronger evidence than the single un-integrated instance.
No new claim is made about non-power-of-two `n` or arbitrary `k` (see Honest scope).

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
