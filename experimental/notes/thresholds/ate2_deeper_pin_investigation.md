# A_te-2 deeper-pin investigation (does the LD_sw pin extend one more step?)

Status: **OPEN** (a425's `EXACT_A425_UPPER_OPEN` stands). Dated 2026-07-06.
**CORRECTION (same day):** the "evidence the pin extends" recorded below came from
a search biased to the a425 witness's basin, and a follow-up CAS construction
found `L>1` configs refuting the collinearity lemma it suggested (see
`ate2_reduction_to_collinearity.md`, `ate2_L1_refute.sage`). So the A_te-2
extension is NOT supported as first claimed -- treat the "evidence extends" below
as biased/inconclusive. What DOES stand: the independent empirical corroboration
of the two-core closure at `A_te-1` (a theorem regardless), and the reusable tool.

## The question

The two-core closure proves `LD_sw(C, A_te-1) = R3+2` (deep pin;
`A_te-1 = n-R3-1`, `R3 = floor((n-k)/3)`). One step further, `a425` shows the
two-core UPPER bound at `A_te-2 = n-R3-2` is loose (Case-A packing gives `7781`
for `n=512`, vs the tangent floor `R3+3`), and marks the exact value OPEN. So:

```text
is  LD_sw(C, A_te-2) = R3+3  (tangent floor tight -> pin extends one more step),
or does it jump above R3+3   (pin capped at A_te-1)?
```

## Why exact computation cannot decide it

The exact worst-case emca staircase (`exact_worstcase_eca_emca_staircase.md`) is
computable only for small `m = n-k` (syndrome classes cost `q^{2m}`). Small-`m`
rows show `emca(r) = r+1` (tangent-tight) up to `r = R3` and then jump to near
saturation -- e.g. `F_7,n=6,k=3` (m=3): `emca = 1,2,7`; `F_11,n=10,k=6` (m=4):
`1,2,9,11`. But those live in the **pre-two-core regime** (`m < 9`, where the
Case-B `c=A-1` witness and the packing lemma do not yet apply). The deployed
regime is `m >= 9`, where `q^{2m}` is infeasible. So exact emca cannot reach the
question.

## Method: construct-and-count via unique decoding

For `A > (n+k)/2` (the unique-decoding radius), each line word `w_z = f + z g`
has at most one nearby codeword, so the bad-slope count of a **given** line is
cheap (Berlekamp-Welch per slope). Both `A_te-1` and `A_te-2` exceed the unique
radius for `rho=1/2, m>=15` (and lower rates sooner), so this reaches moderate
`m >= 9` -- exactly the regime exact emca cannot.

`experimental/scripts/ate2_construct_and_count.py`:
- counts support-wise-noncontained bad slopes of a line `(f,g)` at agreement `A`
  (`z` bad iff `w_z|_S` is a codeword restriction on some `|S|=A` while `g|_S`
  does not extend to a deg-`<k` poly);
- reproduces the `a425` moving-root witness (exactly `n-A+1` bad slopes) as a
  validation baseline;
- searches: the `a425` witness, a low-overlap two-clump construction, and
  aggressive hill-climbing from both.

## Results

Across four diverse rows (varied `m`, rate), the thorough diverse search
(~2000 line evaluations per row) found **nothing beating the tangent floor**:

| q | n | k | m | R3 | max bad @ A_te-2 | floor R3+3 | max bad @ A_te-1 | floor R3+2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 31 | 31 | 15 | 16 | 5 | 8 | 8 | 7 | 7 |
| 37 | 34 | 17 | 17 | 5 | 8 | 8 | 7 | 7 |
| 41 | 40 | 20 | 20 | 6 | 9 | 9 | 8 | 8 |
| 37 | 31 | 10 | 21 | 7 | 10 | 10 | 9 | 9 |

**Two readings:**
1. `A_te-2` best `= R3+3` in every row -> **evidence the pin extends**
   (`LD_sw(A_te-2) = R3+3`), i.e. the answer is *positive*, not capped.
2. `A_te-1` best `= R3+2` in every row, never exceeded -> an **independent
   empirical corroboration** of the two-core closure (the deep pins in PR #381).

## Proof route -> reduced to a single collinearity lemma

A first "gluing" route (force the pairwise polys `p_{zw}` into one global poly)
stalls -- triple overlaps have size `~ (m mod 3) - 6 < k`. **But a stronger route
succeeded in reducing the whole bound to one clean lemma** (see
`ate2_reduction_to_collinearity.md`): the bad-slope codewords empirically lie on
a single code-line `c_z = a+zb` (**collinearity lemma L1**, `L=1` in 1200/1200
configs + Sage rank-1). Given L1, shifting by that code-line makes `f'=-zg'` on
each `S_z`, partitioning the domain by the ratio `-f'/g'`; a disjointness count
then gives `|Z| <= R3+3` unconditionally. That reduction is **verified two ways**
(Codex logic review: Steps 1,3,4,5 sound, L1 the sole gap; Sage CAS: count and
rank cross-checked). So `A_te-2` is now `LD_sw = R3+3` **modulo L1** -- a strict
advance on a425's OPEN, with L1 the crisp remaining target.

## Honest scope

`A_te-2` is **OPEN**. The evidence points to the pin extending, but heuristic
search can miss a rare construction and exact emca is infeasible at `m >= 9`, so
**no deeper certificate is emitted** (a pin whose safe side rests on an unproven
`LD_sw(A_te-2) = R3+3` would overclaim). The durable outputs are: the barrier,
the reusable construct-and-count tool, the empirical corroboration of the deep
pins, and the partial proof route with its explicit stall point.
