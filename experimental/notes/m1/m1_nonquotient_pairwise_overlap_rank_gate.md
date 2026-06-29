# M1 non-quotient pairwise-overlap rank gate

Status: ROUTE_CUT_SUPPORT_DESIGN / COMPUTATIONAL_ROUTE_CUT / EXPERIMENTAL

This note tests the first non-quotient `a=327` support design from
`m1_interleaved_list_nonquotient_witness_search.md` against the exact
pairwise-overlap interpolation gate for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

It remains strictly an `INTERLEAVED_LIST` track audit. It is not an MCA
`N_bad` row and does not claim protocol soundness, ordinary list decoding,
exact `Lambda_mu`, exact `delta*_C`, or a global upper bound at `a=327`.

## Support Design

The support-design checkpoint produced seven subsets

```text
S_0,...,S_6 subset H,    |S_i| = 327,
```

with pair intersections at most `254`. This passes the necessary RS packing
gate because two distinct degree `<256` polynomials can agree in at most `255`
positions.

The design has:

```text
coordinate multiplicities:
  271 coordinates in 4 supports
  241 coordinates in 5 supports

pair intersection min = 142
pair intersection max = 254
sum_{i<j} |S_i cap S_j| = 4036
```

Support packing therefore does not block `a=327`. The question is algebraic
interpolation.

## Reduced Rank Gate

We need seven degree `<256` polynomials `P_i` and one received word `r` such
that

```text
P_i(h) = r(h)    for h in S_i.
```

Equivalently, on overlaps,

```text
P_i(h) = P_j(h)  for h in S_i cap S_j.
```

The diagonal equal-polynomial freedom can be removed by subtracting `P_0`.
Set

```text
D_i = P_i - P_0,  i=1,...,6.
```

Then the reduced system is:

```text
D_i vanishes on S_0 cap S_i,
D_i - D_j vanishes on S_i cap S_j for 1 <= i < j <= 6,
deg D_i < 256.
```

If this reduced system has a nonzero solution, it gives a non-diagonal
interpolation candidate for the support design. If it has nullity zero, then
the original overlap system contains only the diagonal/equal-polynomial
solutions for this support design.

The Sage audit compresses the variables by writing

```text
D_i(X) = Z_i(X) E_i(X),
Z_i = product_{h in S_0 cap S_i} (X-h).
```

For the six difference polynomials, the dimensions are:

```text
i:       1   2   3   4   5   6
dim:    74  81 108  81  36   2
```

So the rank gate is a `2882 x 382` system over `F_17^32`, rather than the
larger received-word system.

## Result

The Sage audit computes:

```text
compressed variables = 382
rank                 = 382
nullity              = 0
```

Thus this support design has no non-diagonal reduced solution. It cannot
produce seven distinct degree `<256` codewords agreeing with one received word
on the proposed seven supports.

## Status Ledger

ROUTE_CUT_SUPPORT_DESIGN:

- the `a=327` support design passes support packing;
- the reduced pairwise-overlap rank gate has nullity `0`;
- this support design cannot produce an `a=327` interleaved-list certificate.

PARTIAL / OPEN:

- other support designs may have different overlap-rank behavior;
- multi-core non-quotient families remain open;
- randomized/non-quotient support searches remain open;
- no global `Lambda_mu(C,327) <= 6` theorem is claimed.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next Step

The next support-design search should optimize for rank slack, not just
pair-intersection feasibility. A useful score should combine:

```text
pair intersections <= 255
low reduced-system rank
positive reduced nullity
balanced support sizes
```

Only a support design with positive reduced nullity should be promoted to
explicit codeword/received-word extraction and Sage witness auditing.
