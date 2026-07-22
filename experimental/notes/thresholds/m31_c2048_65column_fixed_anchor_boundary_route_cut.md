---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: If the paid low layer plus the complete c=2048 exact-boundary layer exceeds B_star, one of the 261192 occupancy profiles contains 65 codewords. Every selected 65-frame has 50 independent coupled kernel rows below the boundary cutoff and a basis-relative two-column Plücker anchor of degree at most 29004. The deployed source separately realizes 65-codeword packets in 156 profiles, while the target-field proper-hyperplane theorem permits collision-free deformation of every budget-sized prescribed packet unless an identically forced component occurs.
architecture: M31_C2048_65COLUMN_FIXED_ANCHOR_BOUNDARY_ROUTE_CUT_V1
partition_digest: CERTIFICATE_BOUND; no ledger atom assigned
atom_or_cell: HIGH_BOUNDARY_EXACT_CODEWORD / U_new
quantifier: Every target-field received word at the deployed exact boundary; source nonemptiness is one separately constructed base-field word per certified profile.
projection_and_unit: Distinct exact-boundary codewords, same-profile 65-subpackets, coupled locator-numerator kernel rows, and rooted anchor-minor incidences.
claimed_bound: A cap of 64 in every profile gives U_paid+U_boundary=16720018<B_star by 57197; hence a violation forces width 65. The first two joint indices sum to at most 29004, the first four to at most 58008, 50 rows have degree at most 65262, and the cutoff syzygy space has dimension at least 3335543.
status: PROVED
impact: WHOLE_EXACT_BOUNDARY_TRIGGER / FIXED_ANCHOR ROUTE CUT
falsifier: A missing profile, a boundary violation with no 65-member profile, an index sequence exceeding the sharp envelope, failure of the primitive-minor bridge, a floor-65 census mismatch, or an invalid inherited collision-avoidance count.
replay: Python exact atlas, integer optimizer, canonical certificate and mutations; independent Sage arithmetic and polynomial-module replay.
---

# M31 c=2048 whole-boundary 65-column fixed-anchor route cut

## Status

    PROVED whole-exact-boundary trigger
    PROVED 65-column fixed-anchor ladder
    PROVED 65-column sources are populated
    PROVED current collision-only route still stops
    ledger movement = 0
    M31 LIST row closed = false

This packet takes the maximal exact-boundary step after the 30-column
occupancy reduction and the arbitrary-word multiprefix correction. It uses
all 261,192 c=2048 profiles, including both C1-shaped faces, at the actual
LIST budget. Thus it no longer requires a separate face charge before
identifying the carrier forced by a boundary excess.

The result is stronger than another selected 16-column calculation. A
forbidden boundary mass forces 65 same-profile columns. On all 65 columns,
the global coupled kernel contains 50 independent rows below the Padé cutoff
and supplies a basis-relative anchor that is fixed outside a small common
exceptional set. The target-field collision-avoidance theorem, however,
remains valid past every budget-sized prescribed packet. The anchor is
therefore a rigorous successor interface, not a canonical owner predicate or
by itself a paid collision owner.

## 1. Deployed constants and scope

Put

\[
 p=2^{31}-1,\quad n=2^{21}=2097152,\quad K=2^{20}=1048576,
\]
\[
 A=1116023,\quad R=n-A=981129,\quad w=A-K=67447,
\]
\[
 B_*=\left\lfloor\frac{p^4}{2^{100}}\right\rfloor=16777215.
\tag{1.1}
\]

The active source adapter has already paid

\[
 U_{\rm paid}\le3730.
\tag{1.2}
\]

At exact error weight \(R\), the degree-2048 Chebyshev fold partitions the
domain into 1024 complete fibers. The exhaustive occupancy atlas has exactly

\[
 137+479\cdot545=261192
\tag{1.3}
\]

profiles. This is the all-profile count, not only the 260576 bi-deep rows.
The packet concerns HIGH_BOUNDARY_EXACT_CODEWORD inside \(U_{\rm new}\); it
does not include high-interior weights or silently identify a C1-shaped
occupancy face with an already-paid C1 prefix cell.

## 2. Whole-boundary 65-column trigger

### Theorem 2.1

Let \(M_{u,v}(y)\) count exact-boundary codewords of one deployed target-field
received word in profile \((u,v)\), and put

\[
 M_\partial(y)=\sum_{(u,v)}M_{u,v}(y).
\]

If every profile has at most 64 codewords, then

\[
 M_\partial(y)\le64\cdot261192=16716288
\tag{2.1}
\]

and

\[
 U_{\rm paid}+M_\partial(y)
 \le3730+16716288
 =16720018
 =B_*-57197.
\tag{2.2}
\]

Equivalently, if

\[
 U_{\rm paid}+M_\partial(y)>B_*,
\tag{2.3}
\]

then one occupancy profile contains at least 65 distinct exact-boundary
codewords.

### Proof

Equation (2.1) is the disjoint sum over the exhaustive atlas. Under (2.3),
the integer boundary mass is at least

\[
 B_*-3730+1=16773486.
\]

Since

\[
 \left\lceil\frac{16773486}{261192}\right\rceil=65,
\]

pigeonhole gives the claimed profile. \(\square\)

This theorem is boundary-conditional. Controlling the boundary does not
automatically pay high interior, extension, or the other open atoms.

### Corollary 2.2 (the existing combined gate forces width 36)

The predecessor's conditional combined face/carrier allowance is
\(9,216,781\). Any disjoint codeword charge above that allowance, when
retained with its original occupancy profile, forces 36 members in one
profile, because

\[
 35\cdot261192=9141720=9216781-75061
\tag{2.4}
\]

and

\[
 \left\lceil\frac{9216781+1}{261192}\right\rceil=36.
\tag{2.5}
\]

On 36 columns the joint kernel has rank 34. The sharp integer envelope gives

\[
 \nu_1\le26872,\qquad \nu_1+\nu_2\le53745<67448,
\tag{2.6}
\]

at least 21 independent rows lie at or below the cutoff, and

\[
 \dim\{A\in\ker H:\deg A\le67447\}
 \ge34\cdot67448-913681=1379551.
\tag{2.7}
\]

The one- and two-anchor rooted incidence floors are respectively 1,420,160
and 465,902. This gate-aligned width also lies strictly inside the
target-field collision-nonforcing range proved for every budget-sized
prescribed packet.

Thus there are two exact triggers:

- width 36 for the predecessor's conditional 9,216,781 combined charge;
- width 65 for direct all-profile boundary closure with slack 57,197.

The 65-frame gives stronger local algebra. Neither width crosses the current
deformation wall.

## 3. Sharp cumulative index envelope

Select 65 members of the forced profile. Divide the true common core \(C_R\)
of the complete exact-weight layer and write the coupled columns

\[
 H=\begin{pmatrix}P_1&\cdots&P_{65}\\
                   B_1&\cdots&B_{65}\end{pmatrix}.
\tag{3.1}
\]

The target-field arbitrary-subpacket theorem gives a direct-summand joint
kernel of rank 63. For a row-reduced basis with nondecreasing row degrees,

\[
 0\le\nu_1\le\cdots\le\nu_{63},\qquad
 \sum_{i=1}^{63}\nu_i
 \le2R-K-|C_R|-1
 \le913681=:S.
\tag{3.2}
\]

### Lemma 3.1 (sharp integer prefix optimizer)

Let \(0\le x_1\le\cdots\le x_r\) be integers with
\(\sum x_i\le S\). Write \(S=ar+b\), \(0\le b<r\). Then

\[
 \sum_{i=1}^m x_i
 \le ma+\max(0,m-(r-b))
\tag{3.3}
\]

for \(1\le m\le r\), and the bound is sharp.

### Proof

Put \(t=x_m\). Monotonicity gives

\[
 \sum_{i=1}^m x_i\le mt,\qquad
 \sum_{i=1}^m x_i\le S-(r-m)t.
\]

The maximum over integral \(t\) of the smaller affine bound is attained at
\(t=a\) or \(t=a+1\), giving (3.3). The balanced sequence with \(r-b\)
entries \(a\) and \(b\) entries \(a+1\) attains it. \(\square\)

Here

\[
 S=63\cdot14502+55.
\tag{3.4}
\]

Since \(63-55=8\), Lemma 3.1 gives

\[
\begin{array}{c|rrrr}
m&1&2&3&4\\ \hline
\nu_1+\cdots+\nu_m&14502&29004&43506&58008.
\end{array}
\tag{3.5}
\]

The fifth cumulative degree is \(72510>67448\), so four is the largest ladder
rank forced below the minimum reduced-locator degree by the aggregate sum.

The module is much larger than these first four rows. Since the final 14
indices dominate \(\nu_{50}\),

\[
 \nu_{50}\le\left\lfloor\frac{913681}{14}\right\rfloor
 =65262<67447.
\tag{3.6}
\]

Thus at least 50 independent module rows lie below the boundary cutoff. The
aggregate index sum cannot guarantee a fifty-first: the abstract sequence

\[
 \underbrace{0,\ldots,0}_{50},
 \underbrace{67448,\ldots,67448}_{13}
\tag{3.7}
\]

has total \(876824\le913681\). The predictable-degree Hilbert function also
gives

\[
 \dim_{\mathbb F_{p^4}}
 \{A\in\ker H:\deg A\le67447\}
 \ge63\cdot67448-913681
 =3335543.
\tag{3.8}
\]

If an index exceeds the cutoff, replacing its truncated zero contribution
by the corresponding negative affine term only lowers the right side, so
(3.8) remains valid.

## 4. Basis-relative fixed-anchor ladder

### Theorem 4.1

For \(1\le m\le4\), choose a row-reduced kernel basis ordered by nondecreasing
row degree, label the columns, take the first \(m\) rows, and choose any
nonzero \(m\)-minor \(\Delta_{J_m}\). Then:

1. \(\Delta_{J_m}\ne0\) and

   \[
   \deg\Delta_{J_m}\le D_m,\qquad
   (D_1,D_2,D_3,D_4)=(14502,29004,43506,58008);
   \tag{4.1}
   \]

2. for every nonanchor column \(k\notin J_m\), the anchor has full rank at
   all but at most \(D_m\) roots of \(P_k\);
3. uniformly in the common core,

   \[
   \deg P_k\ge67448,
   \tag{4.2}
   \]

   and hence the rooted nonanchor incidence lower bounds are

   \[
   \begin{array}{c|rrrr}
   m&1&2&3&4\\ \hline
   (65-m)(67448-D_m)
   &3388544&2421972&1484404&575840.
   \end{array}
   \tag{4.3}
   \]

### Proof

The full joint kernel is a direct summand of
\(\mathbb F_{p^4}[X]^{65}\). Any subset of a basis of that kernel extends to
a basis of the ambient free module. The \(m\)-row matrix is therefore
primitive: its maximal minors generate the unit ideal. At least one minor is
nonzero, so the lexicographic choice exists. Predictable degree and (3.5)
give (4.1).

A nonzero polynomial \(\Delta_{J_m}\) vanishes at at most its degree many
distinct domain points. It therefore has full anchor rank at all but
\(D_m\) roots of every squarefree \(P_k\).

For (4.2), put \(c=|C_R|\) and \(e=\deg P_k=R-c\). Two distinct RS codewords
have error-support union of size at least \(K+1\). Their intersection
contains \(C_R\), so

\[
 K+1\le|E_i\cup E_j|\le2R-c.
\]

Thus \(c\le2R-K-1=913681\) and \(e\ge67448\). Subtracting (4.1) and summing
over the \(65-m\) nonanchor columns proves (4.3). \(\square\)

The choices for different \(m\) need not be nested. This is an existence
ladder, not a canonical flag or a non-oracular first-match predicate. Once a
basis and minor are chosen, the same minor is fixed for every root and every
nonanchor column; that is the only sense of “fixed anchor” used here.

For \(m=2\), one fixed two-column Plücker chart of degree at most 29,004 is
valid on at least 38,444 variable error points of each of the other 63
columns. This removes the predecessor's root-dependent choice of a covering
minor. It is not automatically an affine-rank, common-zero, support-flag,
quotient, or Johnson owner: its coefficients vary with the evaluation point,
and no existing v4 theorem identifies this polynomial chart with a
codeword-direction chart.

## 5. The terminal is populated

The predecessor fixed-multipartial source constructs, separately for every
feasible profile \((u,v)\), one base-field received word with at least

\[
 L_{u,v}=
 \left\lceil
 \binom{1023-u-v}{544-v}
 p^{-\min(32,544-v)}
 \right\rceil
\tag{5.1}
\]

exact-boundary codewords in that profile. Its complete target-field ball is
boundary-only and base-field-valued. Exact big-integer enumeration gives

    profiles with L_(u,v) >= 65: 156
      C1-shaped faces:             34
      bi-deep profiles:           122

    largest bi-deep floor:
      (u,v)=(1,1), L_(1,1)=1,693,898

The bi-deep floor-65 frontier is

\[
\begin{array}{c|rrrrrrrrrrrrrr}
u&1&2&3&4&5&6&7&8&9&10&11&12&13&14\\ \hline
\max v&16&15&14&13&12&11&9&8&7&6&5&3&2&1\\
L_{u,\max v}&120&108&97&87&78&69&115&102&89&78&68&109&94&81.
\end{array}
\tag{5.2}
\]

These are 156 separately constructed words, not simultaneous profile counts
for one word. They nevertheless prove that a universal profile cap of 64,
or a claim that the 65-column terminal is empty, is false.

## 6. Collision-only route cut at width 65

The full-locator hyperplane proof is field-generic. Over a finite coefficient
field \(\mathbb K\), it considers a prescribed packet of \(M_0\) supports.
Conditional on none of the escape or collision forms vanishing identically
on the \(\mathbb K\)-linear containment-functional space, it avoids all
proper hyperplanes whenever

\[
 F(M_0)=M_0R+\binom{M_0}{2}(2R-K-1)<|\mathbb K|.
\tag{6.1}
\]

Indeed, a proper hyperplane has at most
\(|\mathbb K|^{\dim\Lambda-1}\) points, so fewer than
\(|\mathbb K|\) such hyperplanes cannot cover the containment space. For the
deployed target field \(\mathbb K=\mathbb F_{p^4}\), the exact
boundary-trigger count is

\[
 F(65)=1964229865<p^4
\tag{6.2}
\]

with margin

\[
 p^4-F(65)
 =21267647892944572736998860267723701016.
\tag{6.3}
\]

More strongly, at the first forbidden integer list size,

\[
 F(B_*+1)
 =F(16777216)
 =128589177894085853184<p^4.
\tag{6.4}
\]

Its target-field margin is

\[
 21267647892944572608409682375602077697.
\tag{6.5}
\]

The exact integer endpoint of this same target-field union bound is

\[
\begin{aligned}
F(6823032369902110)&<p^4,\\
F(6823032369902111)&\ge p^4.
\end{aligned}
\tag{6.6}
\]

The prime-field 67/68 endpoint from the earlier local packet is not
transferred; (6.2)--(6.6) are the correct quartic-field specialization.

For an actual exact packet, every one-point escape form is automatically a
proper linear form on the containment space: the functional producing the
actual received word evaluates it nonzero. There is therefore an exhaustive
two-case alternative at width 65, at width 36, and for any prescribed packet
within (6.6):

1. some pair-collision form vanishes identically on the complete containment
   space; this is a genuine forced-collision component, but it still needs a
   chronology-valid owner and exact refund;
2. every pair-collision form is proper, so the union theorem supplies a
   second functional for which all prescribed supports remain exact and
   every prescribed pair collision is absent.

Consequently the implication

    65 same-profile columns plus low coupled syzygies
        => a positive pair collision
        => an existing collision owner

does not follow from homogeneous containment and proper-hyperplane
hypotheses alone. In particular, every budget-sized target-field packet with
only proper collision forms has an exact collision-free deformation.

This does not prove that the resulting packet is the complete exact layer:
changing the functional can create additional supports. It also does not
exclude the decisive alternative that a collision form vanishes identically
on a forced component. Those are precisely the new facts a successful owner
theorem must exploit.

The successor must therefore prove at least one of:

1. the fixed two-anchor chart forces an identically-zero escape or collision
   component for the complete same-profile layer;
2. a chronology-valid paid v4 owner applies to the fixed polynomial chart,
   with exact codeword add-back;
3. a complete-layer incidence theorem not preserved when the containment
   functional changes; or
4. a direct count of the primitive fixed-anchor residual below the exact
   57,197 whole-boundary slack.

## 7. Chronology and nonclaims

The predecessor terminal was

    M31_C2048_FIXED_SYNDROME_MULTIPREFIX_FACE_CARRIER_OWNER.

The exact successor diagnostic is

    M31_C2048_65COLUMN_FIXED_ANCHOR_OWNER.

It remains inside HIGH_BOUNDARY_EXACT_CODEWORD / \(U_{\rm new}\). A valid
owner must be fixed and non-oracular, retain the codeword-count projection,
respect the declared first-match order, and assign every charged codeword
once. The basis-relative anchor is deliberately not claimed to be a
canonical or admissible earlier owner predicate.

This packet proves no value for \(U_Q\), \(U_{\rm list,int}\), \(U_{\rm ext}\),
or high \(U_{\rm new}\). It proves no high-interior bound, attained-prefix
sum, ledger movement, endpoint, or score change. It does not modify a stable
theorem or use Lean.

## 8. Replay and dependence

    python3 experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --check
    python3 -O experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --check
    python3 experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --tamper-selftest
    python3 -O experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --tamper-selftest
    HOME=/tmp TMPDIR=/tmp /usr/local/bin/sage experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.sage

The Python verifier recomputes the full atlas and source floors with exact
integers, solves the sharp cumulative-index optimizer, checks all budget and
hyperplane margins, seals source hashes, and rejects semantic mutations.
Sage independently replays the deployed arithmetic, profile census, integer
optimizer, and a polynomial-module fixed-anchor fixture.

The mechanical parent is PR #1041 at exact head
752872ce98754a05f37540cd7780a89b86818222, sealed by payload
dacb9136f5818a5f86d9ca8987fbe4d361a57a70ebb490eac50dfc3822e062e4.
At preparation, upstream main remained
32a41660e3088eeeb15a16645330856794302ff0, with no newer PR or rebase need.

There is no layer-cake, dyadic summation, moment, Markov, or probabilistic
Chebyshev step. Chebyshev denotes the deployed polynomial fold.
