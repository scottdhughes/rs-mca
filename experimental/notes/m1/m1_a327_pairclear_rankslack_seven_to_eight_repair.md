# M1 a=327 pair-clear rank-slack seven-to-eight repair

Status:

CANDIDATE / SEVEN_TO_EIGHT_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL

This packet follows `36eac30` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous deeper rank-slack front found a useful nearby pair:

```text
seven-zero rank-slack chamber:
  zero classes = [6,7,8,14,18,19,20]
  inactive rank = 4
  inactive kernel nullity = 2

eight-zero support-reduced chamber:
  zero classes = [6,7,8,14,17,18,19,20]
  inactive rank = 5
  inactive kernel nullity = 1
```

This branch reconstructs the exact best `w3_c3_d1` profile and directly tests
whether the seven-zero rank-slack chamber can be repaired to eight zero rows
without losing rank slack.

Target profile:

```text
template = ninerow_w3_c3_d1
mutation = w3_c3_d1
assignment = fiber_round_robin
assignment seed = 117186
basis = basisaware_0_1_2_3_5_10
coefficient matrix shape = [15,6]
```

## Search

The scanner performs a full projective enumeration for the target profile:

```text
directions tested = 1508598
pair-clear directions = 360360
distinct pair-clear chambers = 178
direct support-reduced chambers = 1
rank-slack chambers = 20
rank-slack zero-7 chambers = 1
rank-slack zero-8 chambers = 0
```

Then it tests every one-row extension from every rank-slack chamber:

```text
extension attempts = 194
pair-clear extensions = 40
support-reduced pair-clear extensions = 1
rank-preserving extension attempts = 0
rank-preserving pair-clear extensions = 0
deep rank-slack extensions = 0
```

## Target Row-17 Attempt

Adding row class `17` to the seven-zero rank-slack chamber is pair-clear, but
it raises inactive rank:

```text
base zero classes = [6,7,8,14,18,19,20]
base inactive rank = 4
base inactive kernel nullity = 2
added row class = 17
new zero classes = [6,7,8,14,17,18,19,20]
new inactive rank = 5
new inactive kernel nullity = 1
pair-clear direction = [1,0,14,6,11,6]
```

So the extension reproduces the support-reduced chamber, but it does not repair
the deeper rank-slack target.

## Interpretation

The tested local seven-to-eight repair is support-only:

```text
SEVEN_TO_EIGHT_SUPPORT_ONLY
```

The exact row-class transition from seven-zero rank slack to eight-zero support
reduction exists and is pair-clear, but it necessarily raises inactive rank in
the tested target profile. No one-row extension from any rank-slack chamber in
this profile preserved inactive rank at most four.

This is a sharper local obstruction than the previous broad front. The issue is
not finding row class `17`; it is keeping row class `17` in the inactive span
while preserving all 21 pair projections.

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
- global obstruction outside the tested seven-to-eight repair front

## Next Target

Do not keep adding rows to this fixed chamber. The next branch should alter the
local row geometry so row class `17` becomes dependent on the seven-zero
rank-slack inactive span.

Natural next branch:

```text
m1-a327-pairclear-row17-dependence-codesign
```

Objective:

```text
zero classes [6,7,8,14,18,19,20] have inactive rank 4
row class 17 lies in their span
pair-clear kernel remains nonempty
all 21 pair projections stay nonzero
```

Use Python/GF(17) first. Macaulay2 or Singular is useful only if the row-17
dependence relation becomes a small module certificate. Sage should wait until
there is a genuine pair-clear coefficient kernel or exact-lift proxy.
