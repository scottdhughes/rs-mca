# M1 a=327 pair-clear diverse chamber front

Status:

CANDIDATE / DCHAMBER_DIRECT_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL

This packet follows `dbad852` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous front scored four full projective chamber scans and found no
support reduction beyond the base nine-row chamber. This branch adds a
diversity layer before spending full scans:

```text
mutation categories: base, single-coordinate, shear, double
candidate diversity: mutation category plus assignment strategy
basis diversity: preferred bases plus ranked/random bases
cheap screen: 50000 sampled projective directions per profile
full audit: all 1508598 projective directions for selected profiles
```

The goal is still local and proxy-level:

```text
find pair-clear directions with >=6 zero coefficient rows
or pair-clear chambers with >=5 zero rows and inactive rank <=4
```

No Sage `GF(17^32)` exact lift is attempted.

## Result

The diverse front generated:

```text
mutations generated = 96
candidate systems constructed = 288
structural-pass candidates = 279
diverse candidates selected = 24
sampled profiles = 48
full profiles scanned = 4
```

The sampled screen found:

```text
sample pair-clear directions = 527002
sample direct support-reduced profiles = 13
sample rank-slack profiles = 19
sample nine-row-or-better profiles = 17
```

The four full projective scans tested:

```text
full directions tested = 6034392
full pair-clear directions = 1441440
full direct support-reduced profiles = 4
full rank-slack profiles = 4
full support-reduced extension profiles = 3
```

This is a real improvement over the base chamber front.

## Best Profile

The best full-scan profile is:

```text
template = ninerow_w2_c0_d1
mutation = w2_c0_d1
assignment = fiber_round_robin
basis = basisaware_0_1_2_3_4_6
basis support sizes = [216,216,179,148,142,111]
coefficient matrix shape = [13,6]
```

Best direct support-reduced chamber:

```text
direction = [1,16,0,14,14,11]
zero row count = 8
zero row classes = [7,8,10,12,15,16,17,18]
inactive rank = 5
inactive kernel nullity = 1
active row count = 5
active row classes = [5,9,11,13,14]
```

The same profile also has rank-slack chambers:

```text
best rank-slack zero row count = 7
best rank-slack inactive rank = 4
best rank-slack inactive kernel nullity = 2
```

and support-reduced one-row extensions:

```text
support-reduced extensions = 28
```

## Interpretation

This breaks the previous nine-row support wall at the GF(17) proxy chamber
level:

```text
old active row count = 9
new best active row count = 5
```

The result does not yet give a coefficient kernel, exact codewords, or a Sage
certificate. It says the next small module to audit is no longer the closed
nine-row base chamber. The new target is the `w2_c0_d1` chamber with only five
active rows and an eight-row inactive support.

## Non-claims

This packet does not claim:

- an `a=327` certificate
- Sage `GF(17^32)` exact lift
- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- global obstruction outside the tested diverse chamber front

## Next Target

Move immediately to a small module audit:

```text
m1-a327-pairclear-diverse-five-row-module-audit
```

Export the best `w2_c0_d1` coefficient matrix over `GF(17)` and verify:

```text
full matrix rank
inactive rank/kernel for zero row classes [7,8,10,12,15,16,17,18]
active rank/kernel for active row classes [5,9,11,13,14]
singleton and small active-row extensions
pair-projection scalars for direction [1,16,0,14,14,11]
```

Use Python and Macaulay2/Singular for this small module certificate. Sage should
still wait until a genuine pair-clear coefficient kernel or exact-lift proxy
appears.
