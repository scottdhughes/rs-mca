# Frontier map

## Exact parent

`193b7bf99a5cc7ccea042f25677e698d9f988eee`, the fixed-endpoint successor to
PR #1171.

## Imported frontier

The parent chain supplies four facts on one actual post-near received line.

1. The selected explanation errors have affine rank eleven, so after the
   reversible gauge the explanation-direction code `C'` has dimension
   `s<=10`.
2. The individual support margins satisfy
   `sum theta_gamma <= 106618568137036225644`.
3. At cutoff `1795`, one globally selected minimizing pair owns at least
   `200632` slopes and has complete-core deficiency at most four.
4. Every fixed pair whose complete core has size at least `A` owns at most
   `n-A` selected slopes; ordinary/interleaved pair lists in a fixed
   `r`-dimensional direction container have size at most `Q_r` when
   `Q_r^2<|F|`.

The fixed-right and fixed-left pairwise-rank-one anticodes have already been
paid.  The residual begins with pair-difference row spaces of rank two and a
large common deployed factor.

## New route cut

Center every pair at the dense pair `e_*`.  A low-margin pair gives a subcode

```text
U_e = span(a_e-a_*, b_e-b_*) <= C'
```

of dimension one or two with at least `133004` common zeros in a fixed
`1116044`-coordinate subset of the center core.

Use two zero thresholds:

```text
Z2 = 117731,
Z3 = 23354.
```

A line not contained in a two-plane with `Z2` zeros is a terminal line.
Every other line and every rank-two row space is assigned to one two-plane
with `Z2` zeros.  Ordered bases of evaluation-normal flats count the terminal
lines and two-planes.  If the count fails, the failure itself is a
three-dimensional extension containing an actual `U_e` and having `Z3`
common zeros.

## Exact method wall

At the same cutoff `tau=1936`, replacing `Z3=23354` by `23355` fails even
after exhaustively optimizing `Z2`:

```text
best Z2                 117731
low-margin bound        219,952,702,956,503,040
total                   274,995,846,032,030,976
over budget                  15,117,920,635,889
```

Thus `23354` is the exact adjacent wall for this declared two-level profile.
The theorem itself uses only the paying profile and the exhaustive adjacent
check; no asymptotic or floating-point optimization is load-bearing.

## Remaining theorem

Classify or pay the forced three-dimensional common-factor subcode.  The next
useful statement must preserve the actual center pair, the contained
pair-difference row space, and first-match slope ownership.  Merely cancelling
the common locator separately for many edges is not chronology-safe.
