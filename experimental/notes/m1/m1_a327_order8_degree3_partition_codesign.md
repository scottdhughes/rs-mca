# M1 a327 order-8 degree-3 partition codesign

Status:

PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The previous primal-kernel codesign showed that the minimal three-root locator
family is too rigid. This packet keeps the primal-kernel direction but widens
the construction to partition-first order-8 degree-3 quotient codewords.

The first five nonbaseline witnesses still need three quotient roots to clear
the pair-to-7 guard. The sixth witness is allowed to be any nonzero degree-3
quotient word. For each sampled degree-3 tuple, the scanner derives actual
order-8 equality partitions first, then asks CP-SAT for selected-block
allocation.

## Method

The tested quotient family has:

```text
T = X^64
P_i(T) degree <= 3
f_i(X) = P_i(X^64)
degree(f_i) <= 192 < 256
```

The scanner samples:

```text
witnesses 1..5: nonzero degree-3 words with exactly three zeros
witness 6: any nonzero degree-3 word
witness 7: zero baseline
```

For each tuple it computes the eight quotient-bucket value partitions over
`GF(17)` and uses CP-SAT to test support 327, pair caps, and pair-to-7 guards.

## Result

The bounded run is recorded in the JSON ledger.

```text
candidates tested = 3008
feasible allocations = 0
exact candidates = 0
best label = random_locator5_general6_2471
best max ambient pair count = 192
best failure = ORDER8_PARTITION_ALLOCATION_INFEASIBLE
status = EXACT_EXTRACTION_NO_A327 / ORDER8_DEGREE3_NO_ALLOCATION / PARTIAL / EXPERIMENTAL
```

The best sampled candidate is admissible at the quotient-codeword level: the
seven quotient codewords are distinct and the maximum ambient pair equality on
`H` is `192`, below the RS pair cap `255`. It still cannot allocate selected
received-word blocks to meet support 327 and the pair-to-7 guards.

## Interpretation

This is a local negative for the sampled order-8 degree-3 partition-first
family, not a global a=327 obstruction. The next widening should make the
partition design itself a CP-SAT object and impose degree-3 interpolation as a
separate feasibility check, instead of sampling quotient polynomials first.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track order-8 quotient
  construction;
- global obstruction outside the tested order-8 degree-3 partition codesign
  family.
