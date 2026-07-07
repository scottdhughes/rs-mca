# x4b: an unconditional moment-column cap -- option (a) closed at the KB-MCA row (2026-07-07)

Status: PROVED (elementary, with the rigidity core Lean-anchored) + per-row CRITERION + toy landscape.
Scripts: `experimental/scripts/x4b_deployed_budget_audit.py`, `experimental/scripts/x4b_toy_block_landscape.py`
(both runnable, printed constants). Target node: `x4b_moment_trade_exclusion` (feeds `u2c_boundary_scale_column`
-> `b2_modp_giant_extras`). Companion to #397 (row-sharp Q-atom) and #398 (b2 dual barrier map).

## The cap (PROVED, unconditional)

**Lemma 1 (block size; rigidity).** Any `t`-moment-null block `B` (`e_1(B) = ... = e_t(B) = 0`, `B` in the
row domain, `0 not in B`) has `|B| >= t+1`. Proof: if `b = |B| <= t` the locator is `L_B(X) = X^b + e_1 X^{b-1}
+ ... + e_b = X^b`, whose roots are all `0` -- impossible. (Power-sum form via Newton for `char > t`; the
Newton/rigidity core is machine-checked: `PowersumRigidity.powersum_rigidity`, `RigidityCorollaries.pte_rigidity`,
zero-sorry.)

**Lemma 2 (disjointness cap).** Any pairwise-disjoint family of `t`-null blocks in a domain of size `n` has
`k <= floor(n/(t+1))` members.

**Proposition (moment-column cap).** Per prefix, the MomentTradeStaircase multiplicity from any disjoint block
family is `<= 2^{floor(n/(t+1))}` (members = tail plus a sub-union; equal-total-size sub-unions only, so `2^k`
is conservative). **Criterion:** if `t >= n/(2 log2 n) - 1` then the moment column is `<= n^2` -- the x4
primitive budget absorbs it -- UNCONDITIONALLY (no existence/enumeration input needed; the cap holds whether or
not any primitive block exists).

## Row audit (printed constants, `x4b_deployed_budget_audit.py`)

| row | `t+1` | `k <= n/(t+1)` | mass `<= 2^k` | `n^2` | criterion | verdict |
|---|---|---|---|---|---|---|
| **KB-MCA deployed** (`p = 2^31-2^24+1, n = 2^21, t = 67471`) | 67,472 | **31** | `2^31` | `2^42` | `t >= 49,931`: **PASS** | **moment column closed unconditionally; `k <= 31 <= 1.48 log2 n` = option (a)** |
| toy witness row (`193, 64, 3`) | 4 | 16 | `2^16` | `2^12` | `t >= 4`: FAIL | column genuinely live (consistent with the verified witness + `C(R,R/2)` blowup) |
| toy (`97, 32, 2`) | 3 | 10 | `2^10` | `2^10` | PASS (boundary) | closed |

At the KB-MCA row, x4b's option (a) -- "no super-logarithmic disjoint family" -- is **PROVED**: `k <= 31 <=
1.48 log2 n`, log-bounded, by rigidity + pigeonhole alone. The per-prime certification shape is satisfied: the
criterion is one integer comparison per row.

**Conditional sharpening (first-moment window).** `E[#blocks of size b] = C(n,b)/p^t >= 1` iff `b in
[980,913, 1,116,239]` at KB (window `n/2 +- 67,663`). Blocks confined to the window give `k <= 2`, mass `<= 4`.
The `b = t+1` deficit is `1,660,562` bits -- **matching `prop:proper-q-gap`'s `~1.66e6`** (independent
cross-validation of the gap arithmetic). Unconditional exclusion of below-window blocks is Q-wall-hard; the
point of the Proposition is that the BUDGET question does not need it.

## Toy landscape + the U2-C' tension (verified, `x4b_toy_block_landscape.py`)

- The `moment_trade_staircase` witness `B = {11^e : e in {0,1,2,4,16,45,50,60}} subset mu_64` over `F_193` is
  INDEPENDENTLY RE-VERIFIED in full: `p_1 = p_2 = p_3 = 0`, `p_4 = 18`, rotation stabilizer trivial, no
  reflection symmetry. Primitive, exactly as claimed.
- **Consequence for `u2c_boundary_scale_column`:** the residual dichotomy U2-C' ("every t-null block is a
  mu_M-coset union, M >= t, incl. boundary zero-sum patterns") is **FALSIFIED as an all-rows statement** by
  this witness: a block with trivial rotation stabilizer is not a coset union (any full mu_M-coset union is
  mu_M-rotation-invariant), and `M | n = 64`, `M >= 3` forces `M >= 4`. The official-row version of U2-C'
  remains open; the first-moment window (blocks only at `b ~ n/2 +- w`) is the supporting heuristic there.
- Exhaustive small-size enumeration (5 toy rows, `b <= 6`): the only blocks are the forced quotient cosets
  (counts exactly `n/M`); primitive blocks appear only where the first-moment mean crosses `1` -- consistent
  with the Lee-random-like statistics verified in #398 (round n).

## Scope (honest)

- The `2^k` cap covers the PURE moment column (post-strip, per the x4 four-column order); mixed
  moment-x-quotient bookkeeping belongs to the x4 split itself.
- Rows failing the criterion (small `t` relative to `n/log n` -- e.g. LIST-side rows if `n/(t+1)` is large)
  are NOT closed by this cap; there the column needs the window/enumeration input. The criterion is one
  comparison; row owners can evaluate their rows directly.
- The cap bounds the staircase MULTIPLICITY; it does not (and need not) decide whether primitive blocks exist
  at official rows -- that existence question remains the Q-wall.
