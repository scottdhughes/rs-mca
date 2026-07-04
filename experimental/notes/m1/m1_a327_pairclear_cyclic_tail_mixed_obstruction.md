# M1 a=327 pair-clear cyclic tail/mixed obstruction

Status:

AUDIT / ROUTE_CUT_LOCAL_PAIRCLEAR_FRONT / EXPERIMENTAL

This note follows `75dc8b8` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

This audit is local to the tested GF(17) rank-slack row-span kernel family:

```text
extended zero classes = [6,7,8,14,17,18,19,20]
extended rank guard = <=4
typical extended kernel nullity = 2
```

It synthesizes three committed checkpoints:

```text
e48c576  tail-pair projection repair
c900d81  P45/P46/P56 codesign
75dc8b8  P46/P67 tradeoff repair
```

The claim is narrow: inside this tested local front, reranking the same
rank-slack nullity-2 kernels cycles between small forced-pair obstructions.

## Evidence

### Tail-pair projection repair

The tail-pair repair tested:

```text
basis profiles tested = 2856
target rows present profiles = 2024
extended rank-slack profiles = 112
tail candidates = 112
deep rank-slack repair profiles = 0
```

Its best profile was:

```text
template = ninerow_P17_shear_c1_d1
basis = targetaware_0_1_2_3_4_13
direction = [0,0,1,1,2,0]
forced pairs = [P45,P46,P56]
```

So the first tail repair moved the obstruction from the tail front into the
P456 front.

### P45/P46/P56 codesign

The P456 codesign tested:

```text
basis profiles tested = 6850
target rows present profiles = 5010
extended rank-slack profiles = 320
exact pair-clear profiles = 0
target repaired profiles = 0
near repair profiles = 0
```

Its best profile was:

```text
template = ninerow_W57_c13_pm1
basis = targetaware_0_1_2_3_4_10
direction = [0,0,0,1,0,2]
target pairs cleared = [P45,P56]
preserve pairs cleared = [P57]
forced pairs = [P14,P16,P17,P46,P47,P67]
```

This reduced the target failure to `P46`, but it lost `P67` and introduced
witness-1/4 spillover.

### P46/P67 tradeoff repair

The P46/P67 tradeoff repair tested:

```text
basis profiles tested = 6850
target rows present profiles = 5010
extended rank-slack profiles = 320
exact pair-clear profiles = 0
tradeoff repaired profiles = 0
clean tradeoff repaired profiles = 0
near repair profiles = 0
```

Its best profile was:

```text
template = ninerow_P14_shear_c1_d1
basis = targetaware_0_1_2_3_4_13
direction = [0,1,1,2,0,0]
repair pairs cleared = [P46]
preserve pairs cleared = [P45]
spillover pairs cleared = [P14,P16,P17,P47]
forced pairs = [P56,P57,P67]
```

This removed the witness-1/4 spillover and repaired `P46`, but it returned to
the old tail front.

## Diagnosis

The observed cycle is:

```text
[P56,P57,P67]
  -> [P45,P46,P56]
  -> [P14,P16,P17,P46,P47,P67]
  -> [P56,P57,P67]
```

So the tested rank-slack row-span family has a local pair-clear conservation
pattern:

```text
tail repair creates P456 pressure
P456 repair creates mixed P46/P67 plus witness-1/4 pressure
P46/P67 tradeoff repair returns to the tail front
```

No tested nullity-2 rank-slack kernel direction co-designs these fronts into a
pair-clear direction.

## Non-claims

This note does not claim:

- an `a=327` certificate
- Sage `GF(17^32)` exact lift
- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- global obstruction outside the tested rank-slack pair-clear front

## Next Step

Do not rerank the same nullity-2 kernels again. The local front is now banked.

The next constructive move needs a genuinely new degree of freedom, for
example:

```text
add one more controlled support class before the extended rank target
change the basis selection model rather than only the nullspace objective
return to a higher-level template/hypergraph line with pair-clear feedback
```

Sage should still wait until there is a genuine pair-clear coefficient kernel
or exact-lift candidate. Macaulay2 or Singular is only useful if the cyclic
front is converted into a small module/syzygy certificate.
