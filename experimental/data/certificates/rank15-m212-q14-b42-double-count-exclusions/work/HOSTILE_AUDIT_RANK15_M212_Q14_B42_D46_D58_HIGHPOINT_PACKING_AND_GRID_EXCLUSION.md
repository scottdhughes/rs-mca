# Hostile audit: `q=14`, `B=42`, `D=46..58` packing and grid exclusion

## Verdict

`ACCEPT`, with high confidence, for the exact `U=E=0` boundary cell.

The audit independently reconstructs the moment variables, the disjoint
group gate, the exceptional profile list, the `D=50` source-to-grid
transport, and the heavy/no-heavy incidence arguments.  It does not consume
the result at `D=59`.

Frozen claimant objects:

```text
work/RANK15_M212_Q14_B42_D46_D58_HIGHPOINT_PACKING_AND_GRID_EXCLUSION.md
SHA-256 d1a7d00115ed1293feb4106c51161bdd13e5523de1261d3f113151902fd6a9fa

work/verify_rank15_m212_q14_b42_d46_d58_highpoint_packing_and_grid_exclusion.rb
SHA-256 e7554e05287853419b381bf1eb568970f3a31ef5aff1fdf3df7c1b7fe667621b

expected output
SHA-256 c3795f60fc85db2cdacda6f4bcadfd115b5d0a9d3d5aa619e05a1b953bdf6c7e
```

## 1. Moment and line equations

Writing `w=k-3` at a point of multiplicity `k>=4`, direct elimination from
the three boundary moments gives

```text
sum w c_w=D-3,
sum w^2 c_w=471-D.
```

On a line, direct elimination from its 15 support points and 41 other-line
incidences gives `d=S-11` and `t=26-S-s`.  These signs and constants replay;
in particular the group threshold is `11-w`, not `10-w` or `12-w`.

The aggregate residual rows leave no unmarked higher point.  Thus the source
cap `k<=15`, equivalently `1<=w<=12`, is legitimately applied to every high
point.

## 2. Packing algorithm

For a fixed point, two distinct incident lines cannot use the same second
high point.  Hence their other-point sets are disjoint.  A weight-11-or-12
point supplies at most one line, and all lower weights must be packed into
disjoint groups of total weight at least `11-w`.

The independent audit enumerates moment profiles in ascending weight order.
It generates inclusion-minimal group count vectors independently and uses a
separate memo table for their maximum disjoint packing.  It exactly
reproduces every profile/survivor count from `D=46` through `D=58`, including
the eight exceptional profiles.

## 3. `D=50` geometry

Equality at each of the twelve multiplicity-4 points forces three big-point
connectors and one line through at least eleven of the twelve small points.
The two-line intersection axiom forces all twelve onto the same line.

The big points cannot be collinear: the required connector and singleton
counts would total 43 lines.  In the triangular case the line total is 42
and the double-degree multiset is

```text
1^15, 2^24, 12^2, 13.
```

The side joining the two multiplicity-15 points has exactly thirteen other
lines available and needs thirteen distinct non-high support points, so all
are doubles.  This validates the claimant's assertion that each opposite
connector spends its sole double there.  Its twelve remaining ordinary
points are triples, each pairing one line from the 13-line `B` pencil with
one from the 13-line `C` pencil.  Thus every one of twelve distinct
`A`-connectors carries a complete 13-point grid transversal.

All lines descend to `F_p`: they are duals of literal `F_p` parameter points,
and deletion preserves their equations.  Coordinate normalization is
therefore in `PGL_3(F_p)`.  The twelve grid transversals yield at least twelve
elements in the stabilizer of a 13-set in `F_p^*`; freeness makes the
stabilizer order divide 13.  This forces order 13, contradicted by
`(p-1) mod 13=10`.

## 4. Remaining exceptions

For four multiplicity-13 heavy points, total heavy incidence is 52 while 42
lines and six heavy pairs allow at most 48.  This pays `D=55,56` and the first
`D=57` exception.

For three heavy points, total incidence 43 permits at most two no-heavy
lines; total incidence 42 permits at most three.  Every multiplicity-5 point
needs at least two no-heavy lines.  At most one point can lie on two fixed
lines, and at most three points can lie on at least two of three fixed lines.
These bounds exclude the remaining `D=57,58` profiles exactly as printed.

## Scope

The audit accepts `D=46..58` only.  It specifically preserves the `D=59`
wall and makes no recurrence or official-score claim by itself.

