# Contribution summary: exact thresholds, a machine-checked theorem, and board certificates

A self-contained package of **partial / complementary results** for the smooth-domain
RS MCA problem, all exact-integer and independently cross-checked (Codex logic review,
Lean/Aristotle machine proof, Sage CAS). Everything lives under `experimental/`; no
frozen paper is touched. Four pieces, in order of strength.

## 1. Two-core closure — a machine-checked exact theorem

`experimental/notes/certificate_scanner/two_core_closure_general.md`. Generalizes a426's
single-row two-core upper bound to a theorem: for the four grand-challenge rates at every
power-of-two `n >= 512`,

```
LD_sw(C, A_te-1) = R3 + 2   exactly,   R3 = floor((n-k)/3),  A_te-1 = n-R3-1,
```

so the finite-slope support-wise line threshold is pinned one step past the committed
high-agreement exact range. The crux **universal packing lemma** (`binom(n,j) <= (R3+2)
binom(R3+1,j)`) is formally verified in Lean 4 + Mathlib **twice, independently**:
- `experimental/lean/two_core_packing/` (Opus, v4.31) -- the four admissible rates;
- `experimental/lean/dyadic_packing/` (Aristotle, v4.28) -- the strictly stronger form for
  *every* dyadic rate `2^-i`.

Both `lake build` clean, `#print axioms` = `[propext, Classical.choice, Quot.sound]` (no
`sorryAx`); rebuilt and axiom-checked from scratch.

## 2. Multi-rate adjacent-threshold pins (64 rows)

`experimental/scripts/pin_certificate_generator.py`, `verify_adjacent_threshold_pins.py`,
note `adjacent_threshold_pins_multirate.md`. Extends the committed a425/a426 `LD_sw` pin
(previously only `rho=1/2`) to a grid of 64 admissible rows -- all four rates over
`n = 2^9..2^21` plus prize scale `k=2^40`. Each engineers a Proth-certifiable prime
(`p=u*2^s+1`, `2^s>sqrt(p)`, deterministic primality) so the `2^-128` budget lands between
adjacent line-decoding numerators, pinning `delta*` for `LD_sw` to `1/n`. Consumes only
committed theorems; the deep (two-core, item 1) rows push each pin one step deeper.

## 3. Board-scoring near-capacity caps (4 rows)

`experimental/scripts/board_cap_certificate_generator.py`, `verify_board_cap_certificates.py`,
note `board_nearcapacity_caps.md`, site rows `board_cap_site_rows.json`. Fills the sparse
low-rate MCA leaderboard lanes: `rho in {1/4,1/8,1/16}` currently top out at +87; these land
at ~+120..+121 (and `rho=1/2` at +120). Each is a smooth power-of-two row where the Paper-D
cap holds (`binom(n,k+2)*k >= q*(q+k)`, confirmed by the committed `certificate_scanner`) and
the near-capacity error floor makes it unsafe (`2^128 * floor((q-n)/(2k)) > q_line`, exact).
Score `= 128 + log2(N_bad) - log2(q_line)`, matching the board convention (F17^32 -> +119,
prize192 -> +87). Labeled near-capacity failure/cap certificates, not exact thresholds.

## 4. The A_te-2 frontier -- honest, open

`experimental/notes/thresholds/ate2_reduction_to_collinearity.md`,
`ate2_deeper_pin_investigation.md`, scripts `ate2_construct_and_count.py`, `ate2_L1_refute.sage`.
Whether the pin extends a further step (`LD_sw(A_te-2) = R3+3`) is a425's `EXACT_A425_UPPER_OPEN`.
Recorded faithfully: a Codex-verified conditional reduction (the `L=1` case), the CAS refutation
of the collinearity lemma `L1` it hoped for, and the honest conclusion that the `L>1` maximum
is undetermined (exact `emca` is `q^{2m}`-infeasible above the unique-decoding radius). Kept as
a negative/partial record, not overclaimed.

## Discipline

Reviewer != generator throughout: every load-bearing claim is checked on a second engine
(Codex logic, Lean kernel, Sage coding-theory / the committed scanner). Exact-integer
arithmetic; no floats in certificate cores. Non-overlapping with the M1 (interleaved-list)
lane. Verifiers re-derive from primitives and do not import the generators.
