# M1 a327 cycleguard functional-collision template synthesis

Status:

EXACT_EXTRACTION_NO_A327 / FCOLL_TEMPLATE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `f2b56ec` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The dependency-forced profile generator showed that the current front can force
support-only duplicate groups into the nonbasis set, but it found no actual
projective coordinate or support-coordinate row collisions. A full-rank basis
also makes literal duplicate coordinate rows impossible unless the underlying
functionals have already merged. This branch therefore moves upstream and
mutates template vectors directly while keeping selected-class masks fixed.

The test asks whether nearby template-vector mutations can alter the compressed
functional-class ledger enough to create basis-quotient proxy nullity while
preserving the support and pair guards.

## Search

The bounded run tested single-entry template-vector perturbations on the first
cycle-guarded base candidates.

```text
mutations tested = 96
structural-pass mutations = 88
basis profiles constructed = 32
proxy ranked profiles = 8
proxy positive profiles = 0
```

The best mutation remained structurally valid:

```text
template = ninerow_P12_shear_c0_d1__fcoll_b0_m1_single_entry_delta
mutation = add 2 to witness 1 coordinate 0
raw functional rows/classes = 1777 / 18
raw collision excess = 1759
forced functional identities = 0
functional span rank = 6
template equal pairs = []
```

The best proxy-ranked profile was:

```text
basis = basisaware_1_4_7_8_9_10
matrix shape = 1092 x 851
proxy rank/nullity = 851 / 0
max functional support = 216
support duplicate excess = 2
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
```

## Interpretation

Template-vector perturbation can preserve the structural guards and the
functional span, but this bounded local mutation family still produces
full-rank proxy systems. The best mutation has many raw row repetitions after
compression, but the resulting support/divisibility structure remains generic
from the basis-quotient proxy perspective.

This says the current local template-vector neighborhood is not enough. The next
constructive move should not be more single-entry perturbations. It should
prescribe a functional-class pattern first, then solve or synthesize template
vectors that realize it.

## Next Step

Move to a prescribed functional-collision realization branch:

- choose desired projective functional classes and support sets explicitly;
- enforce no forced identities and span rank `6`;
- require pair projections not forced equal;
- solve template-vector realization over `GF(17)` or a proxy field;
- only then proxy-rank and, if positive, audit over Sage `GF(17^32)`.

Macaulay2 or Singular may be useful if the realization constraints become a
module/syzygy or elimination problem. Keep Python as the first-line generator
and Sage only for exact `GF(17^32)` certification.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift for any new chamber;
- any MCA/protocol consequence from this list-track proxy;
- global obstruction outside the tested functional-collision template synthesis
  front.
