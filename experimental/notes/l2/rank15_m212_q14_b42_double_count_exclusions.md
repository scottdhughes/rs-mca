# Rank-15 `M=212`, `q=14`, `B=42` double-count exclusions

## Theorem

Work over the deployed prime field

```text
p = 2,130,706,433.
```

Assume the literal rank-15 source reduction produces 42 individually
`F_p`-rational projective lines with exact minimal Jacobian-syzygy degree 14,
isolated field zeros, and boundary data

```text
U = E = 0,
R = 14^2 + 14 + 1 = 211.
```

Assume also the source boundary input used by the locator-saturation normal
form: all 211 field zeros are reduced arrangement intersections, every
arrangement line contains exactly 15 distinct intersections, and every
intersection of multiplicity at least three is one of the marked points, so
its multiplicity is at most 15.

Then the arrangement double-point count `D` cannot lie in

```text
{39} union {44,45,...,61}.
```

The conclusion applies to both exact aggregate rows

```text
(square,n14,n15,P,R_res,I_res) = (31150,2,0,1,1,2),
(square,n14,n15,P,R_res,I_res) = (31152,0,1,0,0,0).
```

The bounded moment equations are feasible only for `D=39` and
`44<=D<=146`. Thus `D=40,41,42,43` and `D>146` are already infeasible, and
the exact conservative remainder after this theorem is

```text
62 <= D <= 146.
```

## Proof map

The proof is split into six independently replayed cells.

1. `D=39`: the moment row is forced to
   `n2=39,n3=169,n15=3`. The double graph becomes three disjoint stars, and
   the remaining incidence structure is a rational `(3,13)` net. That would
   force `13 | (p-1)`, while `(p-1) mod 13 = 10`.
2. `D=44,45`: exact bounded partitions and the high-point incidence lemma
   eliminate all eight moment profiles.
3. `46<=D<=58`: an exact disjoint-group packing census leaves eight rigid
   profiles. Heavy-incidence, no-heavy-line, grid-transversal, and Kneser
   arguments eliminate them.
4. `D=59`: the census leaves three profiles. Two fail the no-heavy-line gate;
   the last forces eleven complete transversals of one rational `13 x 13`
   pencil grid and again contradicts `(p-1) mod 13 = 10`.
5. `D=60`: six of eight surviving profiles fail direct incidence gates. One
   remaining profile forces eleven rational grid transversals. The other
   violates the exact multiplicative-correlation identity after Kneser's
   theorem and the factorization `p-1=2^24*127`.
6. `D=61`: nine of ten surviving profiles fail direct incidence gates. The
   final profile has two exhaustive no-heavy-line cases; their selected
   correlation masses are at least 139 and 142, respectively, and both
   contradict Kneser's lower bound.

The complete proofs and two independent implementations of every finite
census are preserved in

```text
experimental/data/certificates/
  rank15-m212-q14-b42-double-count-exclusions/
```

## Exact remaining wall

The next conservative source-valid target is the same boundary object with

```text
62 <= D <= 146.
```

A claimant for `D=62,63,64` exists outside this packet, but its frozen hostile
expected-output digest is stale. It is intentionally not consumed here.
The `D=65` diagnostic leaves 13 exact profiles and contains no theorem.

These local exclusions do not prove `D_2(u)<=211` for all 366 children in the
rank-15 recurrence. The previously frozen recurrence still has 261 unsafe
parents `u=1,043,199,...,1,043,459`; its maximum exceeds the target by
`1,319,452,031,112,061`. Affine rank at least 16 remains a separate official
Grand List wall.

## Nonclaims

This note does not claim:

- the held `D=62,63,64` exclusion;
- any exclusion for `65<=D<=146`;
- a complete `M<=211` theorem;
- removal of a recurrence parent;
- a Grand List theorem, Grand MCA theorem, or official score movement.
