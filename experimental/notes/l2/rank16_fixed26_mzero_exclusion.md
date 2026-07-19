# Rank-16 fixed-26 zero-eliminant exclusion

**Status:** independently accepted conditional finite local theorem. This note
records only the layer that survived separate hostile-proof and source/compiler
audits. It makes no finite ledger, parent, recurrence, asymptotic, or official
score payment.

## Literal source cell

Work over

```text
F = F_2130706433,  R = F[X],  K = F(X),
n = 2097152,       b = 32768, T = X^b,
a = 67472,         r = 63601, d = 28897,
L3 = 59730,        Omega = mu_64.
```

Fix one received word and its canonical first-match owner, one monic
degree-`a` polynomial `g` with `gcd(g,X^n-1)=1`, one nonzero projective ray
followed by its canonical source representative `xi`, one fixed 26-label core,
and eight distinct external labels partitioned into four rows and four columns.
All sixteen cross-pairs must be actual-valid common-source edges, retaining the
exact locator degree, monicity, squarefreeness, complete domain splitting,
selected-fibre avoidance, no additional complete fibre, residual footprint,
nonpairing, earlier-owner exclusions, and canonical first-match ownership.

The cross matrix uses the common-source divided differences, not independently
monic-scaled locators. Assume all its `3 x 3` minors vanish. The inherited
nonzero `2 x 2` theorem and

```text
r-2d = 63601-2*28897 = 5807 > 0
```

make its rank exactly two over `K`.

The exact frozen dependencies are PR #957 at
`7e85fd0fa3f7ab4f1be9a968b2382a56eafe2c98` and PR #958 at
`7252e9de66ea1ae05332c82c7079d86eb0c20662`. This note is conditional
on every source-normalization hypothesis stated by those two packages.

## Primitive transfer

After joint coefficient-content normalization, rebuild the transfer rather
than dividing an old base-`T` decomposition by nonconstant content. There are

```text
A,B,E in R[Z],  J,M in R,  m=deg_Z B in {2,3}
```

with

```text
(T-Z)A-xi B = gE,
B(T) = gJ != 0,
E(T) = -xi J,
deg_Z A = m-1,
deg_Z E <= m,
Res_Z(A,B) = g^(m-1) M.
```

Every coefficient of `B` and `E` has `X`-degree below `b`; every coefficient
of `A` has `X`-degree below `a`. The denominator has the unique Euclidean
division

```text
D = B+(T-Z)C,  deg_X B < b.
```

Primitive denominator pairs reconstructed from different cofactor choices are
proportional by a unit of `R`, hence by a scalar in `F^x`. Their denominator
evaluation degrees and `delta=deg_X J` are therefore common. Their removed
contents need not agree, and their unnormalized transfer branches must not be
identified with the normalized branch.

## Theorem

Under the literal source hypotheses above,

```text
M != 0
```

for both `m=2` and `m=3`, including when `g` has repeated irreducible factors.
In the cubic branch,

```text
deg_X J <= 26962 < b,
```

so `B` has no scalar root in `Omega`. The direct-eliminant degree bounds are
therefore unconditional on this exact conditional source locus:

```text
m=2: deg_X M <= 100237,
m=3: deg_X M <= 133003.
```

## Proof

For each triple `e={u,v,w}` containing one row and two distinct columns, use
the complementary three cofactor rows and two cofactor columns. PR #957 gives

```text
P_e := D_u D_v D_w | g c_e,
J_0,e = c_e J_e != 0,
```

where `J_e` differs from `J` only by a field scalar. Every unnormalized
cofactor transfer is quadratic or cubic; degree at most one would specialize
to degree at most `2b-1=65535<a`, impossible for a nonzero multiple of `g`.
The valid universal bound is consequently

```text
deg_X J_0,e <= 57794,
deg_X P_e <= a+57794-delta.                 (1)
```

It is not valid to substitute the sharper unnormalized quadratic cap merely
because the normalized transfer has `m=2`.

Suppose `m=3` and `delta>=26963`. Equation (1) gives

```text
deg_X P_e <= 67472+57794-26963 = 98303 = 3b-1
```

for all 24 row-plus-two-column triples. Every triple therefore contains a
label `y` with `deg_X D(X,y)<b`. The minimum hitting-set size of these 24
triples is three, so at least three labels are low. From
`D=B+(T-Z)C`, a low label forces `C(X,y)=0`: otherwise the leading term of
`(T-y)C(X,y)` has degree at least `b` and cannot cancel against `B(X,y)`.
Since `deg_Z C<=2`, three distinct roots force `C=0`, hence `D=B`, contrary
to `deg_Z D<=2<3=deg_Z B`. Thus `delta<=26962`. A scalar root of `B` would
force a degree-`b` factor `X^b-y` of `J`, so no scalar root survives.

Now assume `M=0`. The zero resultant gives a primitive common factor
`H_0 in R[Z]` of positive `Z`-degree:

```text
A=H_0 A_*,  B=H_0 B_*.
```

Gauss's lemma also gives `E=H_0 E_*`, and cancellation yields

```text
(T-Z)A_*-xi B_* = gE_*.
```

Put `h=deg_Z H_0` and `q=deg_Z B_*=m-h`. Then
`1<=h<=m-1`. Coefficient-height additivity and the coefficient caps give
`ht_X(B_*)<=b-1`. Evaluation at `Z=T`, together with `gcd(g,xi)=1`, shows
that `B_*(T)` is a nonzero multiple of `g`, while

```text
deg_X B_*(T) <= (q+1)b-1.
```

Hence `q>=2`, because `2b-1<a`. This immediately excludes `m=2`. For
`m=3`, the only survivor is `(h,q)=(1,2)`. Write
`H_0=h_0+h_1 Z` with `h_1!=0`. Height additivity gives
`deg_X h_i<=b-1`, so

```text
deg_X H_0(T)=b+deg_X h_1>=b.
```

Since `B_*(T)=gJ_*` and `B(T)=gJ`, cancellation gives
`J=H_0(T)J_*`, whence `deg_X J>=b`, contradicting the cubic bound
`deg_X J<=26962`. Thus `M=0` is impossible in both branches.

No step radicalizes `g`, divides by `g'`, or assumes `R/(g)` is reduced, so
repeated irreducible factors are covered. Homogeneity of the resultant gives
the displayed `M`-degree bounds after subtracting `(m-1)a`.

## Verification and provenance

The hostile-proof audit accepted exactly the repaired layer above:

```text
packet SHA-256: 55df7721f45642841be1e65e3f7717da3e5411e6055a70981669a320f7808937
response SHA-256: b82da9df90723b8c2f7df3d95447f063208fbfc430242e6c2ef7f4693a0f237f
```

The distinct source/compiler audit independently accepted the same scope:

```text
packet SHA-256: ad5e8223e91a6d84aadd23f16fd2fccbfe47d1d8c5a2af2f3caa436a48b2d91c
response SHA-256: 3205bf0cf6a67c86759aa918067a22e2a5e3284dbe0b4c462537a9339ef25dcf
```

The standard-library verifier pins the inherited main-source files, checks the
deployed endpoint arithmetic, enumerates all 24 omitted triples and their
minimum hitting-set size, exhausts the cancellation degree patterns, checks
the resultant degree bounds, rejects semantic contract mutations, and closes
the package hashes. It does not construct a literal source cell or replace the
algebraic proof.

## Nonclaims and exact remaining wall

This theorem does not prove existence or constructibility of a literal source
cell satisfying its hypotheses. It does not prove unconditional quadratic
rigidity `C=0,D=B`, all eight denominator evaluations below `b`, a source
incidence divisor of `M`, strict valuation excess, a source census, an owner or
first-match collision, an add-back theorem, or disjoint aggregation over cells,
words, owners, generators, rays, cores, or labels.

It proves no finite payment, recurrence, field transfer, asymptotic theorem,
Grand List theorem, Grand MCA theorem, or official theorem. The finite ledger
delta is zero and the official score remains `0/2`.

The exact remaining wall is a literal source-cell existence or incidence
theorem that consumes this `M!=0` exclusion, followed by a separate source-valid
global aggregation theorem.
