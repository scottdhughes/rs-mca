# M1 a=327 pair-clear diverse five-row module audit

Status:

AUDIT / DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL

This packet follows `e7dada7` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The diverse chamber front found a support-reduced pair-clear profile:

```text
template = ninerow_w2_c0_d1
mutation = w2_c0_d1
assignment = fiber_round_robin
basis = basisaware_0_1_2_3_4_6
direction = [1,16,0,14,14,11]
zero row classes = [7,8,10,12,15,16,17,18]
active row classes = [5,9,11,13,14]
```

This branch exports that small module over `GF(17)` and checks it with Python
and Macaulay2.

## Result

Python over `GF(17)` gives:

```text
full matrix shape = [13,6]
full rank = 6
full right-kernel nullity = 0
full left-syzygy dimension = 7

inactive matrix shape = [8,6]
inactive rank = 5
inactive right-kernel nullity = 1
inactive left-syzygy dimension = 3
inactive kernel projective basis = [[1,16,0,14,14,11]]

active matrix shape = [5,6]
active rank = 5
active right-kernel nullity = 1
```

The target direction spans the inactive kernel:

```text
direction = [1,16,0,14,14,11]
direction_spans_inactive_kernel = true
```

All pair projections are nonzero:

```text
forced_pairs = []
```

Every singleton active-row extension destroys the inactive kernel:

```text
singleton extensions tested = 5
singleton full-rank count = 5
```

Every two-active-row extension is also full rank:

```text
pair extensions tested = 10
pair full-rank count = 10
```

Macaulay2 independently confirms:

```text
M2 full rank = 6
M2 active rank = 5
M2 inactive rank = 5
M2 inactive right-kernel generators = 1
M2 rank-slack rank = 4
M2 rank-slack right-kernel generators = 2
M2 extension ranks = 6 for all 5 singleton extensions
```

## Rank-Slack Chamber

The adjacent rank-slack chamber from the diverse front is also recorded:

```text
rank-slack zero row classes = [7,8,10,12,16,17,18]
rank-slack matrix shape = [7,6]
rank-slack rank = 4
rank-slack right-kernel nullity = 2
rank-slack kernel projective basis =
  [[0,0,1,1,0,0], [1,16,3,0,14,11]]
```

This matters because the five-active-row chamber is obtained by imposing one
more active row on a rank-slack kernel. The five-row chamber itself has only a
one-dimensional kernel, so it is not the right place to search for further
active-row removal.

## Interpretation

This is a useful local module certificate:

- the old base front had 9 active rows;
- the diverse front found a 5-active-row pair-clear chamber;
- this audit verifies the new inactive kernel and confirms all five active rows
  kill it one at a time.

So the next search should not try to remove another row from the final
one-dimensional five-row inactive chamber. It should work in the adjacent
rank-slack 2D kernel and ask which active-row constraints can be added while
keeping pair projections clear.

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
- global obstruction outside the audited five-row module front

## Next Target

Move to:

```text
m1-a327-pairclear-diverse-rankslack-kernel-repair
```

Start from the 2D rank-slack kernel:

```text
zero row classes = [7,8,10,12,16,17,18]
kernel projective basis = [[0,0,1,1,0,0], [1,16,3,0,14,11]]
```

Search projective combinations in that kernel and active-row extensions. The
target is:

```text
pair-clear direction with >=9 zero rows
```

or an exact coefficient kernel. Use Python first; use Macaulay2/Singular only
for a small pinned module certificate. Sage should wait until a genuine
pair-clear coefficient kernel or exact-lift proxy appears.
