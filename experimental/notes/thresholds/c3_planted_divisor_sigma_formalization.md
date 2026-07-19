# C3 planted-divisor sigma-bound formalization

## Claim

For the direct trial-scan divisor list used by the existing C3 Lean module,
the sum of divisors satisfies the exact discrete bound

```text
∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N).
```

The theorem is
`FirstMatchAtlas.PlantedDivisorCensus.sigmaOf_le_mul_one_add_log2`.
The earlier `sigmaOf_subexponential` name and the historical declaration
`sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED` are retained as proved
compatibility aliases with the same proposition.

## Status

PROVED

## Parameters

One natural number `N`.  The printed `N ≥ 1` hypothesis is preserved from the
source wrapper, although the Lean proof also establishes the inequality at
`N = 0`.

There is no field, support, row, rate, agreement radius, or protocol
denominator in this theorem.  It concerns only the row-independent
multiplicative-coset planted-divisor census already isolated by the source
packet.

## Existing paper dependency

This discharges the sole explicit `sorry` in
`experimental/lean/first_match_atlas/FirstMatchAtlas/PlantedDivisorCensus.lean`,
integrated in upstream commit `9262f63cf093a7510a2df435f220390f59e2bcd5`.
That module maps to the coset-type subcase of C3 in
`experimental/notes/thresholds/c3_planted_divisor_census.md`, and ultimately
to `prop:planted-payment` and `def:algebraically-planted` in
`experimental/asymptotic_rs_mca_frontiers.tex`.

The Lean statement formalizes a discrete `O(N log N)` census consequence.
It does not formalize the source note's real-valued formula
`σ(N) ≤ N(1+ln N)`.  In particular, it does not derive the Nat theorem from
`ln N ≤ log₂ N`: `Nat.log2` is floored, so that shortcut is invalid.

## Proof idea

For every divisor `d` of `N`, take the complementary divisor `q = N/d`.
Division recovers `d` from `q`, so complementing is injective on the divisor
list.  The divisor sum is therefore bounded by

```text
Σ q in {1,...,N}, N / q.
```

Partition the positive denominators into dyadic blocks
`[2^j,2^(j+1))`.  Block `j` has exactly `2^j` entries and every entry is at
most `N / 2^j`; `Nat.mul_div_le` bounds the whole block by `N`.
`Nat.lt_log2_self` puts every denominator at most `N` into the first
`1 + Nat.log2 N` blocks.  Summing the block bounds gives the result.

The kernel-reported axioms for all three public declarations are exactly
`[propext, Classical.choice, Quot.sound]`; none of the declarations depends on
`sorryAx` or a custom axiom.

## Ledger impact

This turns the C3 module's general integer census target into a checked Lean
theorem and removes the package's only placeholder.  It strengthens the
formal evidence for the row-independent quotient-fiber/ramification census.
It does not change the source packet's overall `PARTIAL` verdict.

Critical nonclaims: Lean does not prove the general identity
`cosetCensusTotal N = sigmaOf N` (only the existing spot instances), the
real `ln`/integral inequality, asymptotic notation, or the bridge to
`e^{o(N)}`.  This theorem does not census row-dependent common factors or
received-line resultants; prove the dihedral or ramification statements for
all parameters; establish the residual prefix estimate or slope projection;
pay C7, C8, or C9; prove a witness-exhaustive atlas; close a complete profile
envelope; prove a lower reserve; certify a finite deployed row; or establish
an MCA threshold or prize claim.

## Constants

The only bound is the displayed exact natural-number inequality.  No sharper
Grönwall/Wigert `O(N log log N)` estimate is formalized or claimed.

## Reproducibility

```sh
cd experimental/lean/first_match_atlas
lake clean
lake build
cd ../../..
python3 experimental/scripts/verify_c3_planted_divisor_census.py
python3 experimental/scripts/verify_c3_planted_divisor_census.py --tamper-selftest
python3 experimental/scripts/verify_c3_planted_divisor_sigma_formalization.py --check
python3 experimental/scripts/verify_c3_planted_divisor_sigma_formalization.py --check --tamper-selftest
```

Expected results are a warning-free clean Lean build, the original census
verifier's `RESULT: PASS (82/82)`, its anchor/coset mutation self-test passing,
and complete rejection of every formalization-correspondence mutation.
