# High-point incidence exclusion of the `q=14`, `B=42`, `D=44,45` boundary cells

## Theorem

Assume the literal-field `M=212` rank-15 source reduction produces a reduced
arrangement of `B=42` projective lines with exact minimal Jacobian-syzygy
degree `q=14`, isolated field zeros, and boundary data

```text
U=E=0,
R=q^2+q+1=211.
```

Then its arrangement double-point count is neither `D=44` nor `D=45`.

This pays the `D=44,45` subcells of both aggregate rows

```text
(square,n14,n15,P,R_res,I_res)
(31150,2,0,1,1,2),
(31152,0,1,0,0,0).
```

It makes no claim for `D>=46`.

## 1. Exact moments and the high-point lemma

The accepted positive-characteristic boundary theorem makes all 211 field
zeros reduced arrangement intersections and puts exactly 15 distinct
intersections on each arrangement line.  If `n_k` is the number of
`k`-fold arrangement points, then

```text
sum n_k=211,
sum k n_k=42*15=630,
sum binom(k,2)n_k=binom(42,2)=861.                 (1)
```

Every point of multiplicity at least three is marked: in the first aggregate
row the unique residual point has multiplicity two, while the second row has
no residual point.  The source marked-point cap therefore gives `k<=15` at
every higher point.

Fix a line `L`.  Let `d_L` be its number of double points and compare every
higher intersection to a triple point.  The 15 support points on `L` and its
41 intersections with the other arrangement lines give

```text
d_L + t_L + #high(L)=15,
d_L + 2t_L + sum_(P high on L)(mult(P)-1)=41.
```

Subtracting twice the first identity gives the exact formula

```text
d_L=sum_(P high on L)(mult(P)-3)-11.               (2)
```

Consequently, if a high point `P` of multiplicity `k<14` were the only high
point on one of its incident lines, then that line would have
`d_L=k-14<0`, impossible.  Every one of the `k` lines through `P` must contain
another high point.  Distinct lines through `P` require distinct other high
points, since two projective lines cannot share two points.  Therefore, if
the arrangement has `H` high points in total,

```text
k<=H-1                                                    (3)
```

for every high multiplicity `k<14`.

## 2. The four `D=44` moment profiles

Put `x=k-2` at the `211-D` non-double points.  Equations (1) always give

```text
sum x=208,
sum x^2=676,
1<=x<=13.                                                 (4)
```

For `D=44`, the complete bounded partition of (4) consists of exactly

```text
n2=44, n3=163, n11=1, n14=3;
n2=44, n3=163, n12=2, n14=1, n15=1;
n2=44, n3=162, n6=2,  n14=1, n15=2;
n2=44, n3=161, n4=2,  n7=1,  n14=1, n15=2.              (5)
```

Their numbers `H` of high points are respectively `4,4,5,6`.  Choosing a
point of multiplicity `11,12,6,7` in the four rows contradicts (3):

```text
11>3, 12>3, 6>4, 7>5.                                   (6)
```

Thus `D=44` is impossible.

## 3. The four `D=45` moment profiles

For `D=45`, the complete bounded partition is

```text
n2=45, n3=161, high multiplicities [4,12,13,13,15];
n2=45, n3=161, high multiplicities [5,9,14,14,15];
n2=45, n3=160, high multiplicities [4,4,9,13,15,15];
n2=45, n3=160, high multiplicities [5,5,6,14,15,15].     (7)
```

Here `H=5,5,6,6`.  Points of multiplicity `12,5,9,6`, respectively, violate
(3):

```text
12>4, 5>4, 9>5, 6>5.                                    (8)
```

Thus `D=45` is impossible as well.

## Source and scope

The proof uses only the literal source transport, the accepted boundary
extactic theorem, the exact aggregate residual ledger, and projective-plane
incidence.  It is characteristic-free after those inputs and uses no
classification of nets or residue determinant.  The next moment-feasible
double count is `D=46`; six profiles occur there, and (3) alone leaves two.

