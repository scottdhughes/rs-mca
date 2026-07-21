# M31 Chebyshev stabilizer and a four-flat global separator

## Status

**PROVED exact domain/monomial stabilizer / PROVED pairwise survivor and
rank-16 boundary / PROVED separator for one frozen fibre-aligned instance /
GLOBAL M31 LIST ROW OPEN.**

This packet follows the exact arbitrary-center compiler in
`m31_shortened_flat_hyperplane_wall.md`.  It resolves the symmetry adapter
completely and then applies the first genuinely cross-support Macaulay
constraint to a concrete instance of that packet's `2^24` local support
model.

The conclusions are deliberately separated.

1. The deployed standard-position Chebyshev domain has no large hidden
   projective or monomial symmetry.  Its exact non-scalar symmetry is only
   `x -> -x`.
2. Every pair of forbidden blocks is compatible with an actual syndrome
   hyperplane and every one-point escape.  Pairwise projective lines cannot
   close the row.
3. Containment rank first becomes obstructive at sixteen arbitrary flats,
   exactly the existing rank-16 Macaulay/Forney gate.
4. A specially frozen Chebyshev-fibre-aligned embedding of four blocks from
   the local binary model is rejected already by a four-flat global
   separator.  The deployed calculation is certified by one nonzero
   `132 x 132` determinant over `F_p`.

The last item does **not** classify arbitrary pair embeddings, arbitrary
four-block configurations, or the complete rank-16 stratum.  It is an exact
global-line regression and a proof-of-mechanism, not the deployed list bound.
There is no `U_Q` or `U_A` payment and no ledger movement.

The packet is stacked on PR #1001 at
`d019ba8ebeaf28e4589f9282c7598fe2e54741cf`.  Its replay files are

```text
experimental/scripts/verify_m31_chebyshev_global_separator.py
experimental/scripts/verify_m31_chebyshev_global_separator.sage
experimental/data/certificates/m31-chebyshev-global-separator/manifest.json
```

## 1. Exact deployed parameters

Throughout,

```text
p       = 2^31-1       = 2,147,483,647,
n       = 2^21         = 2,097,152,
K       = 2^20         = 1,048,576,
a       = 1,116,023,
sigma   = a-K          = 67,447,
R       = n-a          = 981,129,
B*      = floor(p^4/2^100)=16,777,215,
L       = B*+1         = 2^24.
```

The characteristic and exact-support gates used below are all strict:

```text
p>n,       p>3,       R<d(C)=n-K+1=K+1.
```

Let `D` be the deployed standard-position circle x-domain and put

```text
C=RS_Fp(D,K),             V=C^perp.
```

For an error support `E subset D`, retain the shortened dual flat

```text
W_E={v in V:supp(v) subset D\E}.
```

For a nonzero syndrome functional with hyperplane `H`, the exact-support
indicator is

```text
W_E subset H,
W_(E\{x}) not subset H       for every x in E.             (1.1)
```

These are the containment and one-point escape relations whose symmetry and
cross-support compatibility are audited below.

## 2. The standard-position domain is the zero divisor of `T_n`

Let `U` be the norm-one torus over `F_p`.  It is cyclic of order

```text
p+1=2^31.
```

The standard-position source imported from `tex/cs25_cap_v13_2.tex` has an
element `g` of order `4n=2^23`, the subgroup

```text
H=<g^4>,          |H|=n,
```

and lifted twin coset

```text
mathcal D=gH union g^(-1)H.
```

The two cosets together are exactly the odd powers of `g`.  If
`u in mathcal D`, then `u^n` is one of the two elements of order four.  With

```text
chi(u)=(u+u^(-1))/2,
```

the Chebyshev semiconjugacy gives

```text
T_n(chi(u))=chi(u^n)=0.                                  (2.1)
```

The source proves that `chi` is exactly two-to-one on `mathcal D`, so the
x-domain `D=chi(mathcal D)` has `n` points.  Since `T_n` has degree `n`, (2.1)
gives the exact equality

```text
D=Z_Fp(T_n).                                             (2.2)
```

The classical leading coefficient of `T_n` is `2^(n-1)`, hence the monic
domain locator is

```text
Lambda_D(X)=2^(1-n) T_n(X).                              (2.3)
```

In particular, `D=-D` and `0 notin D`.  The unordered set (2.2) is independent
of the choice of order-`4n` generator.  A byte-level protocol ordering or
specific torus generator is not needed for the abstract stabilizer theorem.

## 3. A quartic covariant determines the exact projective stabilizer

Homogenize

```text
F(X,Z)=Z^n T_n(X/Z)
```

and use the unnormalized transvectant convention

```text
(F,F)_r = sum_(i=0)^r (-1)^i binom(r,i)
  (partial_X^(r-i) partial_Z^i F)
  (partial_X^i partial_Z^(r-i) F).                       (3.1)
```

At `r=n-2`, every derivative in (3.1) is quadratic, so

```text
Q=(F,F)_(n-2)=A X^4+B X^2 Z^2+C Z^4.                    (3.2)
```

The verifier evaluates the three exact one-dimensional factorial sums in
`O(n)` base-field operations.  It obtains

```text
A=462,183,554,
B=751,088,031,
C= 26,070,540                 mod p.                     (3.3)
```

The load-bearing gates are

```text
B^2-4AC       =1,653,303,809 !=0,
I=B^2+12AC    =  299,132,536 !=0,
J=72ABC-2B^3  =1,054,263,609 !=0,
4I^3-J^2      =1,954,910,887 !=0.                        (3.4)
```

The transvectant is `GL_2`-covariant.  Therefore every projective
transformation preserving the zero divisor of `F` also preserves the four
points of `Q`.

For completeness, the quartic classification used here is elementary.  Put
four distinct points into the form `{infinity,0,1,lambda}`.  The kernel of the
cross-ratio action `S_4 -> S_3` is the Klein four group.  Its stabilizer is
larger only in the equianharmonic case

```text
lambda^2-lambda+1=0
```

or the harmonic cases

```text
(1+lambda)(2lambda-1)(lambda-2)=0.
```

These are respectively the vanishing conditions for `I` and `J`, up to
nonzero normalizing factors.  Thus (3.4) makes the geometric stabilizer of
`Q` exactly `V_4`.

Writing the roots of (3.2) as `{+r,-r,+s,-s}`, the four candidates are

```text
x,       -x,       kappa/x,       -kappa/x,
kappa=rs.                                                  (3.5)
```

The reciprocal candidates can be excluded over the algebraic closure, not
merely over `F_p`.  Since `n` is divisible by four, four edge coefficients of
`F` are

```text
f_n     = 2^(n-1),
f_(n-2) = -n 2^(n-3),
f_2     = -n^2/2,
f_0     = 1.                                               (3.6)
```

If `F(kappa Z,X)=mu F(X,Z)`, comparison in (3.6) forces

```text
mu       =2^(1-n),
kappa^2  =(2n)^(-1),
kappa^n  =2^(2-2n).                                       (3.7)
```

But the middle equation also gives

```text
kappa^n=(2n)^(-n/2)=2^(-22*2^20).
```

The element `2` has order `31` in `F_p^*`.  The two required exponents are

```text
-22*2^20 = 9 mod 31,
2-2^22   =29 mod 31,                                     (3.8)
```

which is impossible.  Hence

```text
Stab_PGL2(Fbar_p)(D)=Stab_PGL2(F_p)(D)
                   ={x,-x}=C_2.                          (3.9)
```

This finite-field proof is independent of the rational classification in
[Mosunov, Theorem 1.3](https://arxiv.org/pdf/2101.00348), which is used only as
a comparison source.  The verifier also records why tiny analogues cannot be
trusted blindly: `Z_F31(T_8)` has an exceptional stabilizer of order six,
whereas `Z_F127(T_16)` already has stabilizer two.

## 4. Full permutation and monomial automorphism groups

Let `r=K-1`.  If

```text
gamma(x)=(ax+b)/(cx+d)
```

preserves `D`, define

```text
(M_gamma z)_x=(cx+d)^r z_(gamma(x)).                     (4.1)
```

For every polynomial `f` of degree at most `r`, the right side evaluates

```text
(cX+d)^r f(gamma(X)),
```

again of degree at most `r`.  Thus `M_gamma C=C`.

Conversely, a monomial automorphism of `C` induces a projective row operation
that maps the `n` Vandermonde columns to themselves.  Those columns lie on
the normal rational curve in `P^(K-1)`.  Here

```text
n>=K+2,       K<p.
```

Lemma 2.9 and Theorem 2.10 of
[Beelen--Glynn--Høholdt--Kaipa](https://arxiv.org/pdf/1611.04341) show that the
row operation comes from a unique element of `PGL_2(F_p)` stabilizing `D`.
This is the precise primary-source adapter; the cited statements were read
and checked under the displayed parameter gates.

The kernel contains only global scalars.  Indeed, suppose a diagonal
`diag(d_x)` preserves `C`.  Applying it to the constant word gives

```text
d_x=h(x),       deg h<K.
```

Applying it to `x^(K-1)` gives a polynomial `g`, `deg g<K`, such that

```text
x^(K-1)h(x)-g(x)=0       on D.
```

The left side has degree at most `2K-2<n=2K`, so it vanishes identically.
This forces `h` to be constant.  Since `-x` lifts as the pure coordinate
permutation `P_-`, (3.9) yields

```text
PermAut(C)=C_2,
MonAut(C)={alpha I,alpha P_-:alpha in F_p^*}
          =F_p^* x C_2.                                  (4.2)
```

Duality sends a monomial automorphism to its inverse transpose, so the same
statements hold for `V=C^perp`.

There is also a direct weighted-dual check.  From (2.3), `Lambda_D` is even,
so for

```text
u_x=1/Lambda_D'(x)
```

one has `u_(-x)=-u_x`.  Therefore

```text
P_-((u_x h(x))_x)=(u_x[-h(-x)])_x,                       (4.3)
```

which preserves the weighted GRS presentation of `V`.

## 5. Exact preservation of containment, escape, and lines

The correct dual lift of (4.1) is

```text
N_gamma=M_gamma^(-T).
```

It satisfies

```text
N_gamma W_E=W_(gamma^(-1)E),
<M_gamma y,N_gamma v>=<y,v>.                             (5.1)
```

Consequently,

```text
W_E subset H_y
iff W_(gamma^(-1)E) subset H_(M_gamma y),                (5.2)
```

and for every `x in E`,

```text
W_(E\{x}) not subset H_y
iff W_(gamma^(-1)E\{gamma^(-1)x})
    not subset H_(M_gamma y).                            (5.3)
```

Projective lines are likewise carried to projective lines.  Thus sign is a
faithful symmetry of the **entire** exact optimizer, not only of shell
totals.

This does not provide a useful global quotient.  Hyperplanes must first be
split into sign orbits, and then supports may be quotiented only by the
stabilizer of the chosen hyperplane.  Most hyperplanes have trivial sign
stabilizer.  Even in the best case the support orbit has size two.  The exact
automorphism theorem therefore banks a route cut:

```text
large Chebyshev/PGL orbit compression is unavailable.    (5.4)
```

## 6. The first cross-support line and the pairwise survivor

The local `K+2` lines in PR #1001 couple dual points whose supports lie in a
single `K+2` coordinate set.  The smallest abstract nonlocal line lies in a
shortening on `K+3` coordinates.  More generally, for `|U|=K+r`, put

```text
G_U(X)=product_(z in D\U)(X-z).
```

Then

```text
V_U={v in V:supp(v) subset U}
   ={u G_U A:deg A<r},       dim V_U=r.                  (6.1)
```

A minimum-support projective point has the form

```text
P_A=[u G_U L_A],       |A|=r-1.
```

Three such points are collinear precisely when their locator coefficient
vectors have wedge zero.  If

```text
p_ij=c(A)_i c(B)_j-c(A)_j c(B)_i,
```

the exact equations are

```text
p_ij c(C)_k-p_ik c(C)_j+p_jk c(C)_i=0
for 0<=i<j<k<r.                                         (6.2)
```

At `r=3`, for disjoint pairs `A={a,b}`, `B={c,d}`, `C={e,f}`, this is the
single determinant

```text
det [[1,-(a+b),ab],
     [1,-(c+d),cd],
     [1,-(e+f),ef]]=0.                                  (6.3)
```

However, the binary blocks in PR #1001 meet in at most

```text
K-137.
```

Two minimum dual supports drawn from distinct blocks therefore have union at
least

```text
2(K+1)-(K-137)=K+139.                                   (6.4)
```

The first applicable pencil has `r=139`, `9,591` Plücker coordinates and
`437,989` displayed wedge coordinates.  Sign merely pairs this union with
its negative; it does not reduce its dimension.

More strongly, every **pair** of agreement blocks of size `a` with
intersection at most `K-1` is compatible with a literal exact-support
syndrome.  For their error supports `E_1,E_2`, the shortened spaces satisfy

```text
W_(E_1) intersect W_(E_2)=0,
dim Ann(W_(E_1)+W_(E_2))=K-2 sigma=913,682.              (6.5)
```

For `x in E_i`, the one-dimensional extension represented by
`L_(E_i)/(X-x)` is outside `W_(E_1)+W_(E_2)`; otherwise the weighted dual MDS
code would contain a nonzero word on at most `K` coordinates.  Each failed
escape therefore cuts one proper hyperplane from the annihilator in (6.5).
There are `2R` guards and

```text
p-2R=2,145,521,389>0.                                   (6.6)
```

The union bound leaves at least

```text
p^913681 (p-2R)
```

functionals satisfying both containments and all escapes.  Surjectivity of
the syndrome map realizes them by actual centers.

Thus pairwise lines do not merely fail to prove a bound: the complete
two-flat exact-support system has a large literal survivor family.

## 7. Why rank sixteen is the first containment-only gate

For `t` boundary flats the locator/Macaulay map has `t sigma` source
dimensions and at most `K` target dimensions.  At the deployed row,

```text
15 sigma=1,011,705<K,
16 sigma=1,079,152>K.                                   (7.1)
```

Consequently, containment rank alone cannot obstruct fifteen arbitrary
boundary flats.  At sixteen, a common nonzero syndrome requires rank at most
`K-1`, hence locator-syzygy nullity at least

```text
16 sigma-(K-1)=30,577.                                  (7.2)
```

Equivalently, the Forney profile must have an index at least

```text
sigma+1=67,448.                                         (7.3)
```

This is exactly the object already proved and named in
`experimental/notes/l2/rank16_left_kernel_forney_route_cut.md`; it is not a
newly invented obstruction.  Escape-aware separators on three through
fifteen flats are not excluded by (7.1) and remain open.

## 8. A fibre-aligned four-flat global separator

This section freezes one literal embedding of four words from PR #1001's
binary support code and rejects it by the full shortened-flat system.

### 8.1 The four binary words

The first half of the binary code is a 33-fold repetition of the
`[4095,12,2048]_2` simplex code.  Restrict its message space to a fixed
two-dimensional subspace and freeze the other 12-dimensional half at zero.
On each repeat, the nonzero columns restrict to

```text
1,023 zero functionals,
1,024 copies of each of the three nonzero F_2^2 functionals.
```

Across 33 repeats, each of the three variable groups has

```text
33*1,024=33,792
```

binary coordinates.  The four messages `00,10,01,11` therefore have
variable error locators

```text
P_ab=A_a B_b C_(a+b),                                   (8.1)
```

each of degree

```text
e=3*33,792=101,376.                                     (8.2)
```

Let `E_core` be the set of all remaining error positions, common to the four
words.  Its size is

```text
c=R-e=879,753.                                          (8.3)
```

### 8.2 The exact Chebyshev-fibre embedding

Set

```text
Y=T_1024(X).
```

Exact Chebyshev smoothness maps `D` onto the 2,048-point quotient domain

```text
D'=Z_Fp(T_2048),
```

with every fibre of `Y` containing exactly 1,024 points.

Fix the norm-one generator produced by stereographic parameter `t=2`, raise
it to `2^18`, and list the 2,048 quotient labels as the x-coordinates of its
odd powers.  Take the first 198 labels in six consecutive 33-label chunks

```text
A_0,A_1,B_0,B_1,C_0,C_1.                                (8.4)
```

For each of the 33 repeat indices, pair the complete 1,024-point fibre over
the corresponding label in `A_0` with the complete fibre over the
corresponding label in `A_1`, using any pointwise bijection.  Bit zero selects
the first entire fibre and bit one the second.  Do the same for the `B` and
`C` chunks.

This detail matters: one even-Chebyshev fibre is itself a union of sign pairs
and is **not** a one-from-each-sign-pair transversal.  The binary coordinate
pairs are between two distinct complete fibres, not inside one fibre.

The construction consumes

```text
198*1,024=202,752 points
                 =2*101,376 points
                 =101,376 variable pairs.
```

The other `879,753` fixed error coordinates consume `1,759,506` remaining
points in arbitrary pairs, leaving exactly

```text
2,097,152-202,752-1,759,506=134,894
```

unused points, as required by PR #1001.

### 8.3 The quotient determinant

For each chunk in (8.4), let the corresponding lower-case letter denote its
monic degree-33 locator in the quotient variable `Y`.  Define

```text
q_00=a_0 b_0 c_0,
q_10=a_1 b_0 c_1,
q_01=a_0 b_1 c_1,
q_11=a_1 b_1 c_0.                                       (8.5)
```

Each `q_ab` has degree 99.  The square lower Macaulay map is

```text
theta_33: direct_sum_(ab) F_p[Y]_<33 -> F_p[Y]_<132,
theta_33((h_ab))=sum q_ab h_ab.                          (8.6)
```

Using coefficient order `1,Y,...`, the exact determinant is

```text
det(theta_33)=398,200,308 mod p !=0.                     (8.7)
```

The quotient labels, their order, a prefix checksum, every polynomial, and
the determinant calculation are regenerated by both verifiers.  The six
chunk locators are pairwise coprime, and no chunk locator divides all four
polynomials in (8.5), so

```text
gcd(q_00,q_10,q_01,q_11)=1.
```

For this primitive polynomial row, the three Forney indices sum to its row
degree `99`.  Bijectivity of (8.6) says that there is no nonzero syzygy all of
whose entries have degree below `33`.  Each index is therefore at least 33,
and their sum forces the exact lower profile

```text
(33,33,33).                                             (8.8)
```

The lift requires a base-change argument, not composition alone.  Put

```text
S=F_p[Y] subset R=F_p[X],        Y maps to T_1024(X).
```

Because `T_1024` has degree 1,024 and nonzero leading coefficient, polynomial
division makes `R` a free, hence flat, `S`-module with basis
`1,X,...,X^1023`.  Tensoring the exact lower syzygy sequence with `R` shows
that a lower syzygy basis base-changes to an `R`-basis of the syzygies among
the four polynomials `q_ab(T_1024(X))`.  Choose the lower basis row-reduced.
Substitution multiplies every row degree by 1,024 and scales its full-rank
leading-row matrix by nonzero powers of the leading coefficient of
`T_1024`; row-reducedness is preserved.  Thus the deployed Forney profile is
exactly

```text
(33,792,33,792,33,792).                                 (8.9)
```

It remains to bridge this module statement to the strict shortening bounds.
The actual monic variable locator `P_ab` is a common nonzero scalar multiple
of `q_ab(T_1024(X))`.  For `D>=33`, write

```text
theta_D: direct_sum_(ab) F_p[Y]_<D -> F_p[Y]_<(D+99).
```

Bijectivity of `theta_33` implies surjectivity of every `theta_D`: induct on
`D`, representing the new top monomial by shifting a `theta_33` preimage of
`Y^131`, and use the previous bound for the lower terms.  Now use the free
`F_p[Y]`-module basis

```text
1,X,...,X^1023.
```

The source and target bounds decompose as

```text
sigma                 = 65*1,024+887,
K-|E_core|=sigma+e    =164*1,024+887.                   (8.10)
```

For basis residues `0<=r<=886`, `theta_66` maps the source bound `<66` onto
the target bound `<165`.  For `887<=r<=1023`, `theta_65` maps `<65` onto
`<164`.  Multiplication by `X^r` respects exactly the strict bounds in
(8.10).  Finally, in the weighted-dual locator presentation,

```text
L_(E_ab)=L_(E_core) P_ab,
W_(E_ab)={u L_(E_core) P_ab A_ab:deg A_ab<sigma},
W_(E_core)={u L_(E_core) B:deg B<K-|E_core|}.
```

The residuewise surjectivity statements are therefore precisely

```text
sum_(ab) W_(E_ab)=W_(E_core).                            (8.11)
```

### 8.4 The escape contradiction

Suppose one syndrome hyperplane `H` contained all four `W_(E_ab)`.  By
(8.11), it would contain `W_(E_core)`.  For any variable point
`x in E_ab\E_core`, the
smaller error support still contains the common core:

```text
E_core subset E_ab\{x}.
```

Therefore

```text
W_(E_ab\{x}) subset W_(E_core) subset H,                 (8.12)
```

contradicting the one-point escape in (1.1).  Thus the four frozen supports
cannot simultaneously occur as exact errors around one center.

This is the first separator in the present stack that reads a genuinely
cross-support Macaulay relation and rejects an explicit instance of the
`2^24` local model.  It does not say that every embedding of that binary
model has the determinant (8.7), nor does it bound an arbitrary support
family by `B*`.

## 9. Exact scope and ledger

```text
standard-position domain = roots(T_n):        proved
PGL2 stabilizer:                              C2, proved
permutation automorphism group of C and V:    C2, proved
monomial automorphism group of C and V:       F_p^* x C2, proved
containment/escape equivariance:              proved
pairwise exact-support survivor:              proved
first containment-only count:                 16, proved
frozen fibre-aligned four-flat instance:      rejected, proved
all pair embeddings rejected:                 false
rank-16 h=1 stratum classified:               false
prime-field M31 list row closed:              false
quartic-field M31 list row closed:            false
U_Q:                                          null
U_A:                                          null
ledger movement:                              0
prize claim:                                  false
```

The maximal remaining mathematical object is no longer an unspecified
Chebyshev quotient.  It is the literal multi-flat Macaulay/Forney system on
the actual domain, with all escapes:

```text
classify the complete rank-16 h=1 stratum and every
escape-aware 3-through-15 primitive component.            (9.1)
```

Every component must end in a budget-fitting exact certificate, an actual
hyperplane counterexample, a named paid owner, or an explicit primitive
route cut.  Sign can identify mirror components but supplies at most one bit
of compression.

## 10. Replay

```text
python3 experimental/scripts/verify_m31_chebyshev_global_separator.py --check
python3 -O experimental/scripts/verify_m31_chebyshev_global_separator.py --check
python3 experimental/scripts/verify_m31_chebyshev_global_separator.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_chebyshev_global_separator.py --tamper-selftest
sage experimental/scripts/verify_m31_chebyshev_global_separator.sage
```

The Python manifest is fail-closed and pins all source hashes.  Its 28
semantic mutations are resealed before validation, while two raw corruptions
exercise the self-hash failure path.  The Sage replay independently recomputes
the quotient determinant, deployed arithmetic, finite-field quartic gates,
and small exact controls.
