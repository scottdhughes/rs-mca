# CAP25 v13 SP definition and top-stratum audit

Status: REPAIR / BANKABLE_LEMMA / AUDIT.

This note records a narrow source-level repair for the CAP25 v13 primitive
shift-pair input.  It does not prove the adjacent upper ledger and does not
prove

```text
U(1116048) <= B*.
```

Its purpose is to separate the definition of a shift-pair collision from the
quotient-pullback subfamily that is supposed to be deleted before the primitive
SP certificate is applied.

## Definition repair

In the compact v13 raw source, the primitive shift-pair definition currently
describes a depth-`w` collision as equal first `w` moments together with

```text
a nontrivial affine or multiplicative relation carrying one part of the
support to the other inside a quotient scale.
```

That is too narrow for the residual input `SP`.  Quotient-pullback shift pairs
are a paid subclass, not part of the definition of all shift-pair collisions.

The theorem-facing object should be:

```text
A depth-w shift-pair is an ordered pair of disjoint monic split locators
A(T), B(T) of the same degree e over the current support domain D'
such that the two root sets have equal first w power sums.
```

Equivalently, under the deployed characteristic range `char(F) > w`, this is

```text
deg(A - B) <= e - w - 1.
```

The primitive part is what remains after quotient-pullback, complete fiber,
common-divisor, and planted-core explanations have been removed by an explicit
first-match deletion rule.  Affine or multiplicative quotient structure is one
deletion reason, not the definition of the whole SP object.

## Locator-polynomial normal form

Let

```text
A(T) = prod_{a in A0} (T-a),   B(T) = prod_{b in B0} (T-b),
```

where `A0` and `B0` are disjoint `e`-subsets of the active domain.  Equality
of the first `w` power sums is equivalent, by Newton identities in
characteristic greater than `w`, to equality of the first `w` elementary
symmetric coefficients.  For monic degree-`e` locators this is exactly

```text
deg(A(T)-B(T)) <= e-w-1.
```

In particular, the first possible off-diagonal stratum has

```text
e = w + 1,
```

and there the condition is simply that `A(T)-B(T)` is constant.

## Common-core factorization

For a fixed ordered side pair `(A0,B0)` of size `e`, a common residual core
`R` of size `m-e` can be chosen from the complement of `A0 union B0`.
Therefore the raw side-pair contribution factors as

```text
P_e = binom(n-2e, m-e) * sp_w(e; D),
```

where `sp_w(e;D)` counts ordered disjoint monic split locator pairs satisfying
the depth-`w` condition on the full active domain.

The same factorization applies to a primitive count only when the primitive
predicate depends only on the side locators after the stated first-match
deletions.  If planted-core data is part of the predicate, the count should
first be refined by planted-core type and then summed.

## Deployed top-stratum quotient scales

At the first off-diagonal stratum `e=w+1`, quotient-pullback scales are
restricted by the common divisibility of `e` and the multiplicative support
order.  For the deployed adjacent rows this gives a small exact deletion list.

```text
KoalaBear MCA/list top stratum:
  e = 67472 = 2^4 * 4217,
  quotient-pullback scales: 2, 4, 8, 16.

Mersenne-31 MCA/list top stratum:
  e = 67448 = 2^3 * 8431,
  quotient-pullback scales: 2, 4, 8.
```

After these quotient scales have been removed by first match, any remaining
constant-difference split-locator pairs at the top stratum are primitive SP
residue.  This does not bound their number; it only names the correct residual
cell.

## Finite regression witness

The top-stratum phenomenon is already visible in a small multiplicative row.
In `F_97`, inside the order-`16` subgroup `mu_16`, take

```text
U = {1, 22, 50},
V = {8, 18, 47}.
```

The monic locators are

```text
A_U(T) = T^3 + 24 T^2 + 8 T + 64,
A_V(T) = T^3 + 24 T^2 + 8 T + 22,
```

so

```text
A_U(T) - A_V(T) = 42.
```

Thus the two triples have equal first two power sums.  Since here
`e=w+1=3` and the ambient subgroup order is `16`, no nontrivial quotient scale
divides both the subgroup order and the side degree.  This is a compact
regression case for the primitive top-stratum object after quotient-pullback
deletion.

## Audit warning: antipodal selectors

Do not delete every `-1`-paired shift-pair family as quotient-paid.  A complete
quotient pullback through the antipodal map is `-1`-invariant, while an
antipodal selector is anti-invariant: it chooses one element from each pair.
Such selector families must be either explicitly bounded in the primitive SP
certificate or charged by a separate printed deletion rule.

This warning is only an audit target here.  No finite adjacent SP bound is
claimed from it in this note.

## Consequence

The next exact SP target is not a generic quotient deletion statement.  It is
the primitive count

```text
sp_w^prim(e;D)
```

after the quotient-pullback, complete-fiber, common-divisor, and planted-core
deletions have been applied without overlap.  The finite adjacent proof still
needs an explicit integer upper bound for this primitive residue, compatible
with the printed CAP25 v13 margins.
