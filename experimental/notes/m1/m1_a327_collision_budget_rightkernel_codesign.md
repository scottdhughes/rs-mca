# M1 a327 collision-budget right-kernel codesign

Status:

EXACT_EXTRACTION_NO_A327 / RKERNEL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `0108539` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The previous collision-budget syzygy search scored all `240` committed
collision-budget profiles and found no small local row-block dependency:

```text
syzygy profiles scored = 240
syzygy-positive profiles = 0
best syzygy score = 0
```

That made the next test a right-kernel question. Instead of looking for local
duplicate or low-rank row blocks, this branch asks whether the committed
collision-budget front already contains basis profiles whose nonbasis
coefficient rows have a right kernel before full proxy expansion.

## Tools

OR-Tools is available for the next CP-SAT allocation layer:

```text
python = /Users/scott/.venvs/rs-mca-ortools/bin/python
ortools = 9.15.6755
CP-SAT smoke = pass
```

This checkpoint did not require CP-SAT. The committed collision-budget profile
front is small enough to enumerate directly.

## Search

The scanner reconstructed the same committed collision-budget front:

```text
basis profiles constructed = 240
collision-budget profiles = 240
functional class profile counts = {11: 192, 12: 48}
```

For each profile, it computed the rank of the nonbasis coefficient-coordinate
rows over `GF(17)`.

Results:

```text
coefficient kernel nullity counts = {0: 48, 1: 192}
coefficient rank counts = {5: 192, 6: 48}
right-kernel collision-budget profiles = 192
proxy ranked profiles = 12
proxy positive profiles = 0
best failure = RKERNEL_PROXY_FULL_RANK
```

The best right-kernel profile was:

```text
template = lcodesign_0000_basis_simple
basis = collbudget_low_support_basis_support_0_6_7_10_5_2_3
q-variable count = 666
matrix shape = 907 x 666
coefficient rank/nullity = 5 / 1
best coefficient kernel = [1,1,1,16,16,16]
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
forced functional identities = 0
functional span rank = 6
proxy rank/nullity = 666 / 0
```

## Interpretation

Coefficient-level right kernels are common in the committed collision-budget
front. In the `11`-functional-class profiles, there are only five nonbasis
coefficient rows after choosing six basis functionals, so a one-dimensional
coefficient kernel is automatic.

But that kernel is not enough. After the full proxy expansion by support
polynomials and coordinate evaluations over `GF(12289)`, the top `12`
right-kernel collision-budget profiles all had full column rank.

So the current result is:

```text
collision budget: achieved
coefficient right kernel: achieved often
proxy right kernel: not achieved in tested front
```

This confirms the warning from the external review: an arbitrary or shallow
right kernel in reduced coefficient coordinates does not automatically produce a
global RS-shaped dependency. The next branch should prescribe a structured
primal kernel, not merely a coefficient vector.

## Next Step

Move to:

```text
m1-a327-quotient-subgroup-primal-kernel-search
```

Core idea:

Write codeword differences in native RS form:

```text
g_i = f_i - f_7,  i=1,...,6
```

and start with quotient-subgroup kernels:

```text
g_i(X) = P_i(X^s)
```

for:

```text
s = 32, 16, 8, 4
degree(P_i) < 256/s
```

This makes pair caps transparent:

```text
pair agreement <= s * degree(P_i-P_j) <= 255
```

Then use OR-Tools CP-SAT to allocate selected classes across quotient fibers so
that supports reach `327`, pair caps stay under `255`, and pair-to-7 guards
clear. Sage should only be used after the quotient-subgroup/CP-SAT screen
produces an exact candidate or a small exact interpolation target.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track proxy;
- global obstruction outside the tested collision-budget right-kernel front.
