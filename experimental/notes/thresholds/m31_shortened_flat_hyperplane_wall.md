# M31 arbitrary-center list: exact shortened-flat compiler and the global-line wall

## Status

**PROVED exact bridge / PROVED scalar-and-local route cut / GLOBAL LIST ROW
OPEN.**  This packet identifies the exact finite object whose closure would
prove the deployed Mersenne-31 list row.  It also proves that three natural
relaxations do not close it:

1. scalar coset weight and MacWilliams data;
2. pairwise support intersection and the exact `K+2` shadow; and
3. every coordinate-shortened `K+2` projective-line law.

The remaining object is the full cross-support projective-line system, or an
equally strong GRS-specific separator.  No orbit compression is claimed.

This packet is stacked on the reviewed M31 `rho=9` architecture wall at
commit `8ba8939fb66db0f2509bb364368355b9e01b4731` (PR #1000).  The Python
verifier, independent Sage replay, and canonical manifest are:

```text
experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py
experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.sage
experimental/data/certificates/m31-shortened-flat-hyperplane-wall/manifest.json
```

### Provenance and novelty boundary

This packet specializes and composes existing upstream machinery; it does not
claim to rediscover it.  The generic scalar-profile and global projective-line
wall is reused from PR #720 at head
`2f7af1a248f59d0942b8cb76df01c7983490aba3`, now present as
`experimental/notes/thresholds/projective_line_lift_feasibility_wall.md`.
The weighted-GRS coset/support framing is reused from PR #748 at head
`f79711a0b47fc191aa579ae1cde58d2fbed158f5`, now present as
`experimental/notes/thresholds/weighted_grs_mds_coset_packing.md`.  The
syndrome/Hankel predecessor is
`experimental/notes/l1/l1_syndrome_catalecticant_shells.md`.  The M31
prime-to-quartic equivalence is reused from PR #993 at head
`8242ea37f4aa018c241c02fe9287f9914e9fd56a`.  PR #1000 at
`8ba8939fb66db0f2509bb364368355b9e01b4731` supplies the separate rho-nine ADE
regression target.

The new content here is the exact M31 specialization, the duplicate-free
shortened-flat objective with every one-point escape guard, the explicit
syndrome-versus-prefix scope separation, and the forbidden-size binary
support model with a globally consistent coordinate-shortened-line
completion.  The canonical certificate pins hashes of every reused source
and verifier named above.

## 1. Exact row and field ledger

The prime-field row is

```text
p            = 2^31-1          = 2,147,483,647,
n            = 2^21            = 2,097,152,
K            = 2^20            = 1,048,576,
a            = 1,116,023       = K+67,447,
t            = n-a             = 981,129,
d(C)         = n-K+1           = K+1 = 1,048,577,
B*           = floor(p^4/2^100)= 16,777,215,
L            = B*+1            = 2^24.
```

The evaluation domain `D` is the M31 Chebyshev/twin-coset domain contained
in `F_p`; it is not a multiplicative subgroup of order `n`.  The code-general
arguments below use only that `D` consists of `n` distinct base-field points.
The Chebyshev geometry becomes relevant only to a future valid compression.

Let

```text
C = RS_Fp(D,K),              V=C^perp.
```

Then `C` and `V` are `[n,K,K+1]` MDS codes, with `V` a weighted GRS code.
The previously proved scalar-descent theorem gives, at the forbidden size
`L`,

```text
B_F_(p^4)(a) >= L  if and only if  B_F_p(a) >= L.
```

Its strict deployed incidence margin is

```text
592061458020761914489814638395392.
```

Thus a prime-field upper of `B*` would also close the quartic-field list row.
This packet proves neither upper.

## 2. Exact shortened-flat list theorem

For `y in F_p^D`, define the syndrome functional

```text
phi_y:V -> F_p,       phi_y(v)=<y,v>,
H_y=ker(phi_y).
```

For `E subset D`, define the shortened dual space

```text
W_E={v in V:supp(v) subset D\E}.
```

### Theorem 2.1 (support-flat equivalence)

Let `C` be any linear `[n,K]` MDS code over a finite field, put
`V=C^perp`, and let `|E|<d(C)`.  There exists a unique error `e` such that

```text
supp(e) subset E,       y-e in C
```

if and only if

```text
W_E subset H_y.                                             (2.1)
```

Under (2.1), the unique error has exact support `E` if and only if

```text
W_(E\{x}) not subset H_y       for every x in E.            (2.2)
```

Consequently, for every `t<d(C)`, the closed radius-`t` list size is exactly

```text
|L_t(y)| = sum_(E subset D, |E|<=t)
  1[ W_E subset H_y
     and W_(E\{x}) not subset H_y for every x in E ].       (2.3)
```

The sum is duplicate-free.

### Proof

Let `pi_E:V -> F^E` be coordinate restriction.  Its kernel is `W_E`.
The transpose

```text
pi_E^*:F^E -> V^*
```

sends a vector on `E`, extended by zero outside `E`, to its syndrome
functional on `V`.  Finite-dimensional linear algebra gives

```text
image(pi_E^*)=Ann(W_E).
```

Therefore an error supported inside `E` has syndrome `phi_y` precisely when
`phi_y` vanishes on `W_E`, proving existence in (2.1).

If two such errors existed, their difference would be a codeword supported on
at most `|E|<d(C)` coordinates.  The MDS minimum-distance gate forces that
difference to be zero, proving uniqueness.

For `x in E`, the recovered error has zero `x`-coordinate precisely when the
same syndrome can be realized by an error supported inside `E\{x}`.  Applying
(2.1) to the smaller set gives

```text
e_x=0  if and only if  W_(E\{x}) subset H_y.
```

Negating this condition for every `x` proves (2.2).  Finally, every listed
codeword gives the unique error `e=y-c` and therefore one exact support.
Conversely every support counted by (2.3) supplies one unique error and one
codeword.  This proves (2.3) without double counting.  `square`

### M31 dimensions

For `|E|=j<=t`, MDS shortening gives

```text
dim W_E=K-j.
```

At the boundary:

```text
dim W_E          = K-t   = 67,447,
dim W_(E\{x})    = K-t+1 = 67,448.                         (2.4)
```

Thus the amplitude/nonzero-coordinate guard is not optional: flat containment
alone counts errors supported on proper subsets repeatedly.

### Zero syndrome

If `y in C`, then `phi_y=0` and `H_y=V`, not a projective hyperplane.  Since
`t<d(C)`, the radius-`t` list contains exactly `y` and (2.3) counts only
`E=emptyset`: every nonempty `E` fails all-point escape.  The projective
optimizer below therefore handles zero syndrome separately with value one.

For nonzero syndrome, scalar multiples of `phi_y` have the same kernel and
the same support distribution.  Hence nonzero cosets may be indexed by their
projective syndrome hyperplanes for this objective.

## 3. Exact shifted-locator/syndrome bridge

Choose the usual nonzero dual multipliers

```text
u_x = product_(z in D\{x}) (x-z)^(-1).
```

Then

```text
V={ (u_x g(x))_(x in D) : deg g<K }.
```

For an error support `E`, put

```text
L_E(X)=product_(x in E)(X-x).
```

A dual word is supported inside `D\E` precisely when its polynomial is
divisible by `L_E`.  Therefore

```text
W_E=span{ (u_x L_E(x)x^r)_(x in D) : 0<=r<K-|E| }.        (3.1)
```

For a center `y`, define weighted syndrome moments

```text
s_j(y)=sum_(x in D) y_x u_x x^j.
```

Writing `L_E(X)=sum_i ell_i X^i`, equations (2.1) and (3.1) give the exact
fixed-syndrome recurrence

```text
sum_i ell_i s_(i+r)(y)=0,       0<=r<K-|E|.                (3.2)
```

At `|E|=t`, (3.2) consists of exactly `sigma=67,447` shifted-locator
equations.  Thus the shortened-flat optimizer and the complete
fixed-syndrome Hankel/key-equation system are the same object in two
coordinate systems.

This is **not** the deployed fixed weight-plus-power-sum prefix fiber.  One
syndrome fiber can contain supports with different support power sums and
different leading locator coefficients.  The shipped `F_7` toy gives an
exact scope regression: syndrome `(2,5,2)` has exact weight-two errors on
supports `{0,1}` and `{2,4}`, whose first support power sums are respectively
`1` and `6` modulo seven.  Consequently this bridge neither identifies nor
pays `U_Q`.

The Python verifier exhausts every support through radius two for the
`[6,3,4]` RS code over `F_7`.  Across all `7^3=343` syndromes it checks the
duplicate-free flat count against all `577` errors of weight at most two.  It
also verifies the weighted-GRS equality (3.1) and every locator/syndrome
recurrence on the same census, while explicitly checking the scope
counterexample above.  Sage independently replays the same theorem
using its native finite-field kernels.

## 4. Exact projective-hyperplane compiler

The syndrome map

```text
F_p^D -> V^*,       y |-> (v |-> <y,v>)
```

is surjective: its kernel is `V^perp=C`, so its rank is `n-K=dim V^*`.
Consequently every functional on `V`, and hence every projective syndrome
hyperplane, is realized by an actual center; the optimization below neither
adds nor loses syndrome classes.

For a nonzero syndrome let `H=H_y`.  Put

```text
P=P(V),       epsilon_P=1[P subset H].
```

For every projective line `ell subset P(V)`,

```text
sum_(P in ell) epsilon_P = 1+p eta_ell,
eta_ell in {0,1}.                                           (4.1)
```

Indeed, either the corresponding two-dimensional vector space lies in `H`
and all `p+1` points are selected, or the restricted functional is nonzero
and its kernel supplies one point.  The normalization is

```text
sum_P epsilon_P=(p^(K-1)-1)/(p-1).                          (4.2)
```

Conversely, a proper projective point set satisfying (4.1) and (4.2) is a
projective hyperplane.  If a line contains two selected points, (4.1) puts
the whole line in the set.  The selected vectors plus zero are therefore a
linear subspace.  Codimension at least two would leave a projective line
disjoint from it, contradicting (4.1).  The subspace is consequently a
hyperplane.

Add support variables `z_E` for every `E` with `|E|<=t`, with the exact
implications

```text
z_E=1  iff P(W_E) subset {P:epsilon_P=1}
          and P(W_(E\{x})) is not contained for every x in E.  (4.3)
```

The objective

```text
1 for zero syndrome, or sum_(|E|<=t) z_E for nonzero syndrome              (4.4)
```

is exactly the arbitrary-center prime-field list size.  Optimizing (4.4)
under the full line system is not a relaxation and does not require a
first-match atlas.  A bound by `B*` would directly close the prime-field row;
scalar descent would then close the quartic row.

The full system is astronomical.  No orbit quotient of (4.1)--(4.4) has been
proved faithful for the M31 Chebyshev domain.  In particular, the cyclic
coordinate compression available for a multiplicative subgroup must not be
silently imported here.

The verifier exhausts the converse line theorem in `PG(2,2)`, `PG(2,3)`, and
`PG(3,2)`: every subset of hyperplane cardinality obeying the one-or-all line
law is one of the literal hyperplanes.

## 5. Scalar-shell route cut at the forbidden size

The full line system is necessary.  First, shell totals alone admit an exact
formal profile with tail `L=2^24`.

For an integer `q`, define

```text
Z_q(X)=sum_(u=0)^K binom(n,u)p^(K-u)(X-1)^u
       +q( X^a-sum_(u=0)^K binom(a,u)(X-1)^u ).             (5.1)
```

The coefficient of `X^a` is `q`, all coefficients strictly between `K` and
`a` vanish, and the first `K+1` binomial moments agree with an MDS coset.
Put

```text
lambda=binom(n,K)/binom(a,K).
```

Every factor `(n-i)/(a-i)` is larger than `3/2`, since the first-factor gate
is

```text
K-3 sigma=846,235>0.
```

In particular,

```text
floor((3/2)^100)=406,561,177,535,215,237>L.                (5.2)
```

At the rational endpoint `lambda`, coefficient extraction and the partial
alternating-binomial identity give, for `0<=j<=K`, `r=K-j`,

```text
[X^j]Z_lambda / binom(n,j)
 = sum_(v=0)^(r-1)(-1)^v binom(n-j,v)p^(r-v)
   +(-1)^r binom(n-j,r)r/(sigma+r).                         (5.3)
```

The terms in the alternating prefix decrease because `n/p<1`; `p>2n`
makes the last term smaller than the retained first difference.  Hence the
endpoint is coefficientwise nonnegative, and affine interpolation proves
nonnegativity for every integral `0<=q<=lambda`, including `q=L`.

The Krawtchouk transform of (5.1) has the exact form

```text
sum_w A_w(q) K_l(w)=p^K(p N_l(q)-R_l),                     (5.4)
```

where `R_l` is the number of projective weight-`l` points in `V`.  The
standard alternating-shell comparison proving `0<=N_l(q)<=R_l` reduces at
the M31 endpoint to the following exact positive gates, all recomputed by the
verifier:

```text
g_plus numerator =
644050175112195590794125999209377544529 > 0,

g_minus numerator =
15810002823743438754074664582119190973939634949577947321057126025224259167096031283564636761328485464935241283881354308999057975 > 0,

p sigma     -100K(K+9)=34,889,223,043,209 > 0,
p(sigma-8)  -100K(K+9)=34,872,043,174,033 > 0.             (5.5)
```

The proof is the same finite alternating-series split encoded in the
verifier: shells through seven use the two integer gates in (5.5), and the
tail uses `g_minus`; the positive branch uses `g_plus`.  Thus `q=L` satisfies
all scalar integrality, MacWilliams congruence, total-mass, and projective
shell-range conditions.  It is a formal profile, not a received word.

The verifier additionally replays all `287` profiles of the complete small
`[16,8]` scalar model over `F_1009`, checking every Krawtchouk transform and
projective shell interval.  Scalar shells cannot prove the M31 ceiling.

## 6. Exact `K+2` shadow and local-line route cut

Choose one `a`-subset of agreement coordinates from each listed word.  Two
such blocks meet in at most `K-1` points, since two degree-less-than-`K`
polynomials agreeing on `K` points are equal.  The exact `K+2` shadow gives

```text
list <= floor(r_2 lambda),

r_2=K(K-1)/[sigma((sigma-1)+(K+2)(K-sigma))]
   =45812940800/2891200952995149.                           (6.1)
```

This is a genuine cut, but even the elementary lower endpoint gives

```text
floor(r_2(3/2)^100)=6,442,223,650,591 > 2^24.              (6.2)
```

The first complete local atom is also insufficient.  Consider the binary
direct sum

```text
two 33-fold coordinate repetitions of [2^12-1,12,2^11]_2,
710,859 zero coordinates.
```

It is a

```text
[981,129,24,67,584]_2
```

code with exactly `2^24=L` words.  Embed its coordinates into `981,129`
disjoint pairs
of the `n` evaluation positions.  Each binary word chooses one point from
each pair; let `E_z` be that transversal and `S_z=D\E_z`.  Then

```text
|S_z|=a,
|S_z intersect S_z'|=a-d(z,z')<=a-67,584=K-137<K.          (6.3)
```

These `L` blocks therefore obey every pairwise agreement constraint and
already exceed the allowed budget by one:

```text
2^24-B*=1.
```

Its exact weight distribution is

```text
1 + 8,190 z^67,584 + 16,769,025 z^135,168,
```

whose coefficients sum to `2^24`.

For a `(K+2)`-set `S`, let `a_S` be the number of its `(K+1)` facets
contained in selected blocks.  Equation (6.3) forces

```text
a_S in {0,1,K+2}.                                          (6.4)
```

The shortened dual on `S` is two-dimensional.  Its projective line consists
of one minimum-support point on each of the `K+2` facets and

```text
p-K-1=2,146,435,070
```

full-support points.  Complete each local line independently:

```text
a_S=0:    select one full-support point;
a_S=1:    select no full-support point;
a_S=K+2:  select every full-support point.
```

Every coordinate-shortened line then contains exactly one or `p+1` selected
points.  These local assignments are mutually consistent.  A weight-`K+1`
projective point has one support `Q`, so its globally defined status `x_Q` is
the same in every `K+2` line containing it.  A full-support point of weight
`K+2` has one support `S`, so it belongs to exactly the coordinate-shortened
line indexed by `S` and cannot receive two local assignments.

The first two selected dual-shell totals are therefore exactly

```text
N_(K+1)=L binom(a,K+1),

N_(K+2)=binom(n,K+2)
        +L[p binom(a,K+2)-(K-1)binom(a,K+1)].              (6.5)
```

For (6.5), sum the selected facet counts over all `S`: every selected
`(K+1)`-support lies in `n-K-1=K-1` such sets, while exactly
`L binom(a,K+2)` sets lie wholly inside one block.  Substituting the three
completion rules gives the displayed formula.  The verifier pins both exact
formulas and exhausts an independent `[8,4,5]` GRS toy over `F_11`: its 28
shortened lines realize the state census `(a_S=0,1,6)=(15,12,1)`, with zero
bad one-or-all line counts.

These are jointly the first two selected-shell values of the scalar profile
in (5.4) at `q=L`: at `q=0`,

```text
N_(K+1)(0)=0,                 N_(K+2)(0)=binom(n,K+2),
```

and the respective slopes are

```text
binom(a,K+1),
p binom(a,K+2)-(K-1)binom(a,K+1).
```

Thus the local completion and scalar pseudo-profile agree on both overlapping
shells; they are not two incompatible route cuts.

This constructs a consistent truncated support/line model at the forbidden
size.  It is not a single hyperplane of `V`: local completions do not impose
projective lines spanning points from different supports.

Therefore pairwise packing, the exact `K+2` shadow, the first two nonzero dual
shells, and all coordinate-shortened `K+2` line laws cannot close the row.

## 7. External route audit and maximal remaining attack

A targeted audit of the named primary sources found no theorem that supplies
the missing global separator; this is not an exhaustive nonexistence claim.

- Berlekamp--Welch uniqueness requires agreement
  `(n+(K-1)+1)/2=1,572,864`, a deficit of `456,841`.  The
  Guruswami--Sudan/Johnson condition requires agreement strictly above
  `sqrt(n(K-1))`, hence at least `1,482,910`, or at most `614,242` errors.
  The deployed radius exceeds that by `366,887`.  Powered key equations also
  reach the Johnson radius only and may fail on patterns within it.  See
  [Sudan](https://people.csail.mit.edu/madhu/papers/1996/reeds-journ.pdf),
  [Guruswami--Sudan](https://people.csail.mit.edu/madhu/papers/1998/gs.pdf),
  and [Rosenkilde](https://arxiv.org/pdf/1505.02111).
- The normal-rational-curve extension theorems checked do not count the
  present family of shortened flats through one syndrome point.
  [Seroussi--Roth](https://docs.switzernet.com/people/emin-gabrielyan/060708-thesis-ref/papers/Seroussi86.pdf)
  require an MDS-extension range whose M31 upper endpoint is
  `n-floor((p-1)/2)=-1,071,644,671`, while
  [Ball--De Beule](https://web.mat.upc.edu/simeon.michael.ball/normalrationalcurve.pdf)
  study extension from `3K-6=3,145,722` normal-rational-curve points, more
  than the `n` available here.  Both concern arc extension, not this secant
  incidence count.
- The explicit subspace designs of
  [Guruswami--Kopparty](https://www.math.toronto.edu/swastik/subspace-designs.pdf)
  are particular consecutive-evaluation or multiplicity-vanishing families,
  not the collection `Ann(W_E)` for all M31 supports.  Proving the latter is a
  weak `1`-design with bound `B*` would be a stronger containment-only
  sufficient theorem; it is not the exact escaped-support objective because
  the escape guards can delete contained flats.
- Standard constant-weight/Terwilliger bounds only see support weight and
  distance.  Section 6 already gives `2^24` supports with binary distance
  `135,168`, stronger than the required `2(sigma+1)=134,896`; such a
  relaxation cannot prove a ceiling of `2^24-1`.

Automorphism theory is useful only as an adapter: any valid quotient must use
the actual monomial stabilizer of the M31 twin-coset evaluation divisor and
must preserve every containment and escape relation.  Even a faithful
stabilizer quotient is only preprocessing for the global separator below,
not the separator itself.

The route now has a sharp pass/fail contract.  A candidate global separator
must preserve the literal Chebyshev weighted-GRS incidences and must reject:

1. the scalar tail-`2^24` profile of Section 5;
2. the exact `2^24`-block independently completed local-line model of
   Section 6; and
3. PR #1000's `rho=9` ADE pseudo-realization.

The maximal live problem is:

```text
maximize the exact objective (4.4)
over literal projective hyperplanes satisfying (4.1)--(4.3),
and prove that the optimum is at most 2^24-1.               (7.1)
```

A tractable relaxation is admissible only after proving that its orbit or
moment variables preserve every shortened-flat containment and one-point
escape on the actual M31 Chebyshev domain.  A degree-two/Terwilliger,
divided-difference, or Plucker system is useful only if it ends in one of:

```text
EXACT_DUAL_CERTIFICATE_LE_BUDGET,
ACTUAL_HYPERPLANE_COUNTEREXAMPLE,
PSEUDOHYPERPLANE_ROUTE_CUT_WITH_MISSING_INVARIANT,
EXPLICIT_PRIMITIVE_COMPONENT.
```

Do not force a pseudo-hyperplane into an owner, claim an orbit compression
without a preservation proof, or charge this bridge as `U_Q`.  A success in
(7.1) bypasses the local first-match ledger and proves the complete
arbitrary-center list upper directly.

## 8. Ledger impact and nonclaims

```text
prime-field M31 list row closed:    false
quartic-field M31 list row closed:  false
U_Q:                                null
U_A:                                null
ledger movement:                    0
prize claim:                        false
```

This packet proves no global list bound, no M31 MCA statement, no exhaustive
first-match atlas, no Chebyshev orbit quotient, and no deployed safe row.  The
toy computations prove the algebraic compiler, not the deployed inequality.

## 9. Replay

```text
python3 experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --check
python3 -O experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --check
python3 experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --tamper-selftest
sage experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.sage
```

The canonical and optimized Python modes perform the same checks.  The
mutation suite reseals each modified manifest before validation, so rejection
tests semantic gates rather than merely detecting a stale self-hash.
