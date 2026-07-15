# Hostile audit: the `M=212`, `q=14`, `B=42`, `D=39` cyclic-net exclusion

## Verdict

`ACCEPT`, with high confidence, for the exact `D=39` subcell only.

This audit is independent of the claimant verifier.  It reconstructs the
source transport from the literal `F_p` two-flat, the bounded moment
partition, the double-graph classification, and the field obstruction.  It
does not consume the theorem for `D>=44`.

Frozen claimant:

```text
work/RANK15_M212_Q14_B42_D39_CYCLIC_NET_EXCLUSION.md
SHA-256 a3fd6920a42ea6da3efc45ef7376ddc103318547190545fc82ab63ca8b73ae37
```

## 1. Literal-field source transport

The source normal form works over an arbitrary field `F` and specializes the
code/list field to the literal deployed `F_p`.  Its exact affine two-flat is

```text
P_0+span_F{V_1,V_2},
```

and every listed polynomial has one parameter point `(s,t) in F^2`.  Thus in
the deployed specialization all 212 listed parameter points lie in
`F_p^2`.  Projective completion sends `(s,t)` to `[s:t:1] in P^2(F_p)`, and
projective duality sends that point to a projective line whose homogeneous
coefficients are in `F_p`.  Deleting inactive or divisorial arrangement
lines only takes a subset of these lines; it cannot change their field of
definition.  Consequently every one of the retained `B=42` lines is
individually `F_p`-rational.

This is the same literal transport printed in the independently frozen
`M=214` source theorem: projectively complete the affine parameter plane,
dualize the listed points to projective lines, then delete a subset.  The
later extension to the algebraic closure is used only for the Jacobian and
intersection geometry; it does not erase the original `F_p` equations.

The audit pins:

```text
source/grand_list/main/experimental/notes/thresholds/
rank15_locator_saturation_normal_form.md
SHA-256 48d72c94743f5a9c900b35197279a69bf00a8a133c7b27bf3ff39004b1257085

work/RANK15_M214_B149_SOURCE_TRANSPORT.md
SHA-256 2f6cbc1c51b4200651df8fe4f4f7aece61cd4334f914f721a2052ee7557a8d68

work/RANK15_POSCHAR_BOUNDARY_EXTACTIC_EXCLUSION.md
SHA-256 1c5a2840aac0bfe4426b50ef10d6abde8a09724a7982967208214f2b695101c6

work/ROOT_HOSTILE_AUDIT_RANK15_POSCHAR_BOUNDARY_EXTACTIC.md
SHA-256 9b05e27b384fcdad254d50550c6840f62329ac9799157c4edd37b93e907e26b3
```

## 2. Why the multiplicity cap applies to every non-double point

The two aggregate rows have residual ledgers

```text
(P,R_res,I_res)=(1,1,2),
(P,R_res,I_res)=(0,0,0).
```

In the first row the unique residual point has multiplicity exactly two,
because `P=binom(2,2)=1`, `R_res=1`, and `I_res=2`.  In the second row there
is no residual point.  Therefore every arrangement point of multiplicity at
least three is a marked listed point.  The source rich-line packing bound
applies there and gives multiplicity at most 15.  This closes the only scope
gap in the claimant's use of `k<=15`.

## 3. Independent moment reconstruction

The accepted positive-characteristic boundary extactic theorem, at
`U=E=0`, gives 211 reduced intersection points and exactly 15 distinct
intersections on each of 42 lines.  Hence

```text
sum n_k=211,
sum k n_k=630,
sum binom(k,2)n_k=861.
```

Fixing `n_2=39`, there are 172 higher points.  With `x=k-2` their first two
moments are `sum x=208` and `sum x^2=676`.  Put `y=x-1`.  The preceding
scope audit gives `0<=y<=12`, while

```text
sum y=36,
sum y^2=432=12 sum y.
```

Termwise `y^2<=12y`, so equality forces `y in {0,12}`.  Thus the unique
partition is

```text
n_2=39, n_3=169, n_15=3.
```

On one line, let `(d,t,h)` count its double, triple, and 15-fold points.
The support and pair-incidence equations are

```text
d+t+h=15,
d+2t+14h=41.
```

Their only nonnegative solutions are `(1,13,1)` and `(13,0,2)`.  Counting
incidences with the three 15-fold points gives 39 leaves of the first type
and three centers of the second.

## 4. Double graph and residue gate

Let `e_CC,e_CL,e_LL` be the three double-edge types.  The center and leaf
degree sums imply `e_CC=e_LL`.  A leaf-leaf double edge is an isolated
two-line component because both leaves have double degree one.  Each line
then has fourteen other, simple radial zeros.  If the reciprocal connection
residues at their double point are `r` and `r^-1`, the line residue identity
on both components gives

```text
r+14=1,
r^-1+14=1.
```

Thus `r=r^-1=-13`, forcing `169=1`, or `168=0` in the field.  This is false
modulo `p=2,130,706,433`.  Hence `e_LL=e_CC=0` and the double graph is three
disjoint `K_(1,13)` stars.

The centers cannot all meet at one 15-fold point: their remaining three
incidences with the other two 15-fold points would make a pair of centers
meet twice.  They form a triangle.  At each vertex lie the two adjacent
centers and thirteen leaves, while each leaf is double with the opposite
center.  Counting the remaining incidences on a leaf shows that every pair
of leaves from two different vertex classes meets at one of the 169 triples,
with exactly one leaf from the third class.  This is a rational `(3,13)` net.

## 5. Field obstruction

Move the rational center triangle to the coordinate triangle by an element
of `PGL_3(F_p)`.  Parameterize the three classes by nonzero slope sets
`A,B,C subset F_p^*`.  After harmless inversion/relabeling, concurrency is

```text
B A^(-1) subset C.
```

All three sets have size 13.  Fix `a_0 in A`.  Each `B/a` has size 13 and
lies in `C`, so `B/a=C=B/a_0`.  Hence the 13-element set `A/a_0` lies in the
multiplicative stabilizer `H={h:hC=C}`.  The free action of `H` partitions
`C` into `H`-orbits, so `|H|` divides 13.  Therefore `|H|=13` and
`13 | (p-1)`.

But `(p-1) mod 13=10`.  Contradiction.

## Scope

The theorem pays both aggregate `q=14,B=42` rows only in their exact `D=39`
subcell.  The moment ledger has no `D=40,41,42,43` partition.  This audit
makes no claim for `D=44` or higher and no claim that the full `q=14,B=42`
cell is closed.

