# First-interior BC modular fibers as mixed subset products

## Claim

For a root-free first-interior interpolation-lattice row, every nonempty
fixed-multiplier modular-locator fiber is exactly a fixed-cardinality subset
product fiber in a finite abelian group

\[
  U_h \times (\mathbb F[X]/W_1)^\times.
\]

Here \(U_h\) is the depth-\(h\) truncated-locator group, the second factor
records the residue modulo \(W_1\), and

\[
  h=\max(0,w+\deg B-\deg W_1).
\]

Fourier inversion gives an exact character formula and reduces the proposed
fixed-\(B\) bound to a mixed character-mass estimate.  Two distinct supports
in one such fiber exchange at least

\[
  h+\deg W_1+1
\]

roots.  This is the modular analogue of the ordinary Q collision-rigidity
lemma.

The reduction also exposes an integer-sparsity obstruction that the preceding
packet did not quantify: if

\[
  \binom nm |\mathbb F|^{-(h+\deg W_1)}<1,
\]

then every nonempty slice already forces a normalized overhead at least the
reciprocal of that quantity.  Consequently the rank count alone cannot justify
summing one separately rounded estimate per multiplier.  A finite-row
compiler needs a mixed spectral theorem, an aggregate occupancy theorem across
multipliers, or a direct first-match slope-image bound.

## Status

- **PROVED:** the root-free subset-product equivalence, Fourier identity,
  quotient-unit normalization, and exchange-rigidity bound.
- **PROVED / COUNTEREXAMPLE TO A SHORTCUT:** a subunit heuristic average does
  not make a realized fiber empty or singleton; an exact \(\mathbb F_{101}\)
  first-interior fiber has exactly three elements at average \(20/101\).
- **EXACT EXPERIMENT:** a faithful-average \(\mathbb F_{41}/\mu_{20}\) census
  over all \(167{,}960\) supports, including exact weak-Popov realization of
  one heaviest target in each of ten quotient-algebra cases.
- **AUDIT:** exact real nonempty-slice bounds and their least-integer ceilings
  for both deployed first-interior MCA rows.
- **OPEN GAP:** a row-sharp bound for the mixed character mass or an aggregate
  first-match slope compiler.  No deployed row moves.

This packet advances the higher-dimensional balanced-core residual in
problem prob:saturated-bc.  It does not alter the main Papers A--D.

## 1. Parameters and ownership boundary

Let \(F=\mathbb F_s\) be a finite field and let \(D\subset F\) contain \(n\)
distinct points.  Put

\[
  \Lambda_D(X)=\prod_{x\in D}(X-x).
\]

Retain the first-interior data from
bc_first_interior_general_line_modular_fibers.md:

\[
  m=K+w,\qquad d_1=w+2,\qquad d_2=n-m-1,
\]

and a weak-Popov basis

\[
  g_1=(W_1,N_1),\qquad g_2=(W_2,N_2),
\]

with

\[
  W_1N_2-W_2N_1=\gamma\Lambda_D,\qquad \gamma\ne0.
\]

Assume throughout that \(K\ge3\) and \(w+2\le d_2\).  These are the
hypotheses of the preceding exact-rank theorem; in particular the
first-interior profile has \(0\le\deg W_1\le w+2\).  The \(K\ge3\)
assumption is load-bearing for the rank identification (15).

Fix a nonzero multiplier \(B\) of degree \(b\le1\).  Write

\[
  d=\deg W_1
\]

and assume the root-free, coprime chart

\[
  \gcd(W_1,\Lambda_D)=1,\qquad \gcd(B,W_1)=1.       \tag{1}
\]

The first assumption means that no root of \(W_1\) is a domain point.  The
domain-root strata belong to the earlier common-GCD/gluing owner and are not
silently included here.  The coefficient field is exactly \(F\); no
base/extension transfer is asserted.

For an \(m\)-subset \(T\subset D\), put

\[
  V_T(X)=\prod_{x\in T}(X-x).
\]

The first modular condition is

\[
  c_{B,T}=\frac{N_1+\gamma BV_T}{W_1}\in F[X]_{<K}. \tag{2}
\]

Under (1), the determinant gluing law from the preceding packet makes the
second divisibility automatic whenever (2) holds.

## 2. Support-independent compatibility

Before (2) can define a support fiber, its support-independent highest
coefficients must be compatible.

Put

\[
  q=m+b,\qquad t=K+d,\qquad h=\max(0,q-t)=\max(0,w+b-d). \tag{3}
\]

The numerator in (2) must have degree below \(t\).  Therefore:

1. every coefficient of \(N_1\) in degree
   \(j\ge t\) and \(j>q\) must vanish; and
2. if \(q\ge t\), then

   \[
     [X^q]N_1+\gamma\operatorname{lc}(B)=0.          \tag{4}
   \]

These conditions do not depend on \(T\).  If either fails, the fixed-\(B\)
cell is empty.

Assume them from now on.  After the leading cancellation (4), the remaining
degree cap consists of exactly \(h\) equations.  Reading from degree \(q-1\)
downwards, multiplication by \(B\) is triangular with diagonal
\(\operatorname{lc}(B)\ne0\).  Thus those equations fix exactly the first
\(h\) coefficients below the leading coefficient of \(V_T\).

Modulo \(W_1\), equation (2) is

\[
  [V_T]=-[\gamma B]^{-1}[N_1]
       \quad\hbox{in }F[X]/(W_1).                    \tag{5}
\]

The inverse exists by (1).  Moreover the determinant identity and
\(\gcd(W_1,\Lambda_D)=1\) imply \(\gcd(W_1,N_1)=1\), so the target in (5) is a
unit whenever the cell is nonempty.

## 3. Exact mixed subset-product theorem

Define the truncated monic-locator group

\[
  U_h=1+YF[Y]/(Y^{h+1}).
\]

It has \(s^h\) elements; for \(h=0\) it is the trivial group.  Put

\[
  A_{W_1}=F[X]/(W_1),\qquad
  H_{W_1,h}=U_h\times A_{W_1}^{\times}.              \tag{6}
\]

For each \(x\in D\), define

\[
  g_x=(1-xY,\ X-x)\in H_{W_1,h}.                     \tag{7}
\]

The second component is a unit because \(W_1(x)\ne0\).

### Theorem 1 (root-free modular subset-product normal form)

Under (1) and the support-independent compatibility conditions of Section 2,
the glued modular-locator fiber is exactly one fiber of

\[
  \Psi_{W_1,h}:\binom Dm\longrightarrow H_{W_1,h},
  \qquad
  T\longmapsto\prod_{x\in T}g_x.                    \tag{8}
\]

Equivalently,

\[
  \Psi_{W_1,h}(T)=
  \left(
    Y^mV_T(Y^{-1})\bmod Y^{h+1},
    V_T\bmod W_1
  \right).                                           \tag{9}
\]

### Proof

The first component of (9) is

\[
  \prod_{x\in T}(1-xY),
\]

so it records exactly the first \(h\) coefficients below the leading
coefficient of \(V_T\).  Section 2 shows that the high-degree part of (2) fixes
this component.  The second component is exactly (5).  Conversely, fixing
both components gives the high-degree cancellations and divisibility by
\(W_1\), hence (2) with degree below \(K\).

Finally \(V_T\mid\Lambda_D\) and (1) imply
\(\gcd(V_T,W_1)=1\).  The determinant gluing law therefore supplies the second
divisibility with no additional support condition.  This proves equality,
not merely containment.  \(\square\)

### Specializations

- \(d=0\): the quotient-algebra factor is trivial, and (8) is ordinary depth
  \(h=w+b\) Q.
- \(d=1\): the quotient-algebra coordinate is the subset product

  \[
    V_T(\alpha)=\prod_{x\in T}(\alpha-x)
  \]

  at the root \(\alpha\) of \(W_1\).
- split squarefree \(W_1\): the second coordinate is a tuple of such products.
- repeated or irreducible factors: the coordinate lives in the corresponding
  finite quotient algebra and includes principal-unit or extension-field
  characters.  It is not ordinary Q.

Thus the nonconstant-\(W_1\) chart is a joint additive/multiplicative
fixed-cardinality subset-product problem.

## 4. Exact Fourier reduction

Let \(\widehat H\) be the complex character group of \(H=H_{W_1,h}\).  For
\(\chi\in\widehat H\), define

\[
  E_m(\chi)
   =[Z^m]\prod_{x\in D}\left(1+Z\chi(g_x)\right).     \tag{10}
\]

For a target \(u\in H\), character orthogonality gives the exact identity

\[
  |\Psi_{W_1,h}^{-1}(u)|
  =\frac1{|H|}
    \sum_{\chi\in\widehat H}\chi(u)^{-1}E_m(\chi).   \tag{11}
\]

The trivial character contributes \(\binom nm\).  Put

\[
  \mathcal A_{W_1,h}
   =\binom nm^{-1}
     \sum_{\substack{\chi\in\widehat H\\\chi\ne1}}
       |E_m(\chi)|.                                  \tag{12}
\]

If the distinct monic irreducible divisors of \(W_1\) are \(P\), then

\[
  |A_{W_1}^{\times}|
   =s^d\prod_{P\mid W_1}(1-s^{-\deg P}).
\]

Define

\[
  \kappa(W_1)
   =\frac{s^d}{|A_{W_1}^{\times}|}
   =\prod_{P\mid W_1}(1-s^{-\deg P})^{-1}.           \tag{13}
\]

Repeated factors occur only once in this product.  From (11),

\[
  |\operatorname{MLFib}_B|
  \le
  \kappa(W_1)(1+\mathcal A_{W_1,h})
  \binom nm\,s^{-(h+d)}.                              \tag{14}
\]

The monic fixed-\(B\) rank theorem in the preceding packet gives, under (1),

\[
  \operatorname{rank}_{\rm monic}L_B
   =\max(d,w+b)=h+d.                                  \tag{15}
\]

Therefore (14) has exactly the predicted linear-algebra exponent.  The
missing content is now precise: it is control of the nontrivial mixed
character mass (12), not another rank computation.  The quotient-unit defect
\(\kappa\) is explicit and usually small; it does not control the character
mass.

## 5. Modular collision rigidity

### Theorem 2 (exchange lower bound)

If distinct supports \(T,T'\in\binom Dm\) lie in one fiber of (8), then

\[
  |T\setminus T'|=|T'\setminus T|
  \ge h+d+1.                                         \tag{16}
\]

### Proof

Let \(C=T\cap T'\), let \(e=|T\setminus T'|\), and factor

\[
  V_T=V_C P,\qquad V_{T'}=V_C Q,
\]

where \(P,Q\) are distinct monic degree-\(e\) locators on the exchanged
roots.  The common factor is a unit both in \(U_h\) and modulo \(W_1\), so it
cancels from equality of the two group products.

Equality in \(U_h\) says that \(P\) and \(Q\) have the same first \(h\)
coefficients below their leading coefficient.  Hence

\[
  \deg(P-Q)\le e-h-1.
\]

Equality modulo \(W_1\) says \(W_1\mid(P-Q)\).  Since \(P\ne Q\),

\[
  d\le\deg(P-Q)\le e-h-1,
\]

which is (16).  \(\square\)

The bound is sharp in both exact experiments below.  It supplies a
constant-weight packing bound, but the existing Q audits already show that
distance alone is far too weak for the deployed row-sharp target.

## 6. Integer-sparsity obstruction

Put

\[
  r=h+d,\qquad
  \mu_{\rm lin}=\binom nm s^{-r}.                    \tag{17}
\]

This is the heuristic scale suggested by linear rank.  If a fiber is nonempty,
its integer size is at least one.  Therefore any inequality of the form

\[
  |\operatorname{MLFib}_B|
  \le R_B\binom nm s^{-r}
\]

must have

\[
  R_B\ge\mu_{\rm lin}^{-1}                            \tag{18}
\]

whenever \(\mu_{\rm lin}<1\).  The true average over the group (6) is
\(\kappa(W_1)\mu_{\rm lin}\), not \(\mu_{\rm lin}\), but this does not remove
the integer floor.

Average below one does **not** imply singleton fibers.  It only says that most
formal group targets are empty.

### Exact sharpness example over \(\mathbb F_{101}\)

Take

\[
  D=\{0,1,2,3,4,5\},\quad n=6,\quad K=m=3,\quad w=0,
\]

and

\[
  W_1=1,\quad B=X,\quad\gamma=1,\quad
  N_1=-X^4+7X^3.
\]

Here \(h=r=1\) and

\[
  \binom63/101=20/101<1.
\]

The three supports

\[
  T_0=\{0,2,5\},\qquad
  T_1=\{0,3,4\},\qquad
  T_2=\{1,2,4\}
\]

are exactly the three triples in \(D\) with sum \(7\).  Thus their monic
cubic locators have the same \(X^2\) coefficient, and all three

\[
  N_1+XV_{T_i}
\]

have degree below \(K=3\).  Conversely this degree cap forces the root sum to
be \(7\), so the fiber has exactly three elements.  The exchange size between
\(T_1\) and \(T_2\) is \(2=r+1\), so (16) is sharp.

This is a genuine first-interior basis, not an abstract target.  Divide
\(\Lambda_D=N_1S+R\) with \(\deg R<4\) and put

\[
  g_2=(-S,R).
\]

Then

\[
  W_1R-(-S)N_1=\Lambda_D,
\]

and the two shifted row degrees are \((2,2)=(w+2,\omega-1)\).

## 7. Faithful-average exact census

The verifier

experimental/scripts/verify_bc_modular_subset_product.py

uses

\[
  F=\mathbb F_{41},\quad D=\mu_{20},\quad
  (K,m,w,d_1,d_2)=(7,9,2,4,10).
\]

Every support is cyclic-aperiodic because \(\gcd(9,20)=1\).  The common monic
rank in the strict numerator-leading cases is

\[
  r=w+1=3,
\]

and the heuristic average is faithfully above one:

\[
  \binom{20}{9}/41^3
  =167960/68921
  =2.436993079\ldots.                                 \tag{19}
\]

The script enumerates every support once and compares root-free \(W_1\)'s of
degrees \(0,1,2,3\), keeping \(h+d=3\).  It reports the complete nonempty
occupancy histogram, image size, and second moment; the compact maximum-fiber
table is:

| \(d\) | quotient-algebra type | \(h\) | image size | max fiber | \(s^r\max/\binom nm\) | min exchange |
|---:|---|---:|---:|---:|---:|---:|
| 0 | ordinary Q | 3 | 59,200 | 13 | 5.334443 | 4 |
| 1 | root-free linear | 2 | 63,331 | 10 | 4.103417 | 4 |
| 2 | irreducible | 1 | 64,177 | 10 | 4.103417 | 4 |
| 2 | split distinct | 1 | 61,563 | 10 | 4.103417 | 4 |
| 2 | repeated | 1 | 63,032 | 9 | 3.693076 | 4 |
| 3 | irreducible | 0 | 63,952 | 10 | 4.103417 | 4 |
| 3 | linear times irreducible | 0 | 63,037 | 10 | 4.103417 | 4 |
| 3 | split distinct | 0 | 60,883 | 9 | 3.693076 | 4 |
| 3 | double plus linear | 0 | 62,062 | 10 | 4.103417 | 4 |
| 3 | triple root | 0 | 63,125 | 10 | 4.103417 | 4 |

All ten cases attain the exchange lower bound \(r+1=4\).  The largest unit
defect is only \(1.076891\), at the split cubic; factorization changes the
image and collision statistics, but no tested mixed case is heavier than the
ordinary Q control.

### Exact weak-Popov realization

For the lexicographically first heaviest target in each case, the verifier
chooses one locator \(V_0\), fixes

\[
  B=X,\qquad N_1=-XV_0,
\]

and solves

\[
  W_1N_2-W_2N_1=X^{20}-1
\]

with the exact second-row degree caps.  For every locator \(V\) in the target,

\[
  c_V=\frac{X(V-V_0)}{W_1}
\]

has degree below \(K\).  The script then recovers

\[
  A_V=\frac{N_2-W_2c_V}{V}
\]

and checks

\[
  A_VW_1+XW_2=\frac{X^{20}-1}{V},\qquad
  A_VN_1+XN_2=c_V\frac{X^{20}-1}{V}.
\]

Every basis has profile \((4,10)\), every determinant and gluing check passes,
and the realized heaviest fiber sizes are exactly those in the table.  Thus
the census targets are actual first-interior modular fibers, not arbitrary
affine signatures.

The experiment is finite evidence about the character mass.  It is not a
theorem of equidistribution.

## 8. Exact deployed integer floors

The verifier recomputes the complete binomial integers.  To make the audit
optimistic, the coefficient-field size is taken to be the printed prime even
for Mersenne-31.  Using an extension coefficient field only decreases the
heuristic averages and increases the bounds.

The strict numerator-leading coprime rank is \(w+1\); the full-denominator
coprime rank is \(w+2\).  For a real overhead, the exact necessary nonempty
slice bound is \(R_B\ge s^r/\binom nm\), whose bit value is
\(-\log_2\mu_{\rm lin}\).  If a compiler records a positive integral
overhead, its least possible value is

\[
  R_B^{\mathbb Z}=\left\lceil s^r/\binom nm\right\rceil.
\]

| row | slice | rank | \(\log_2\mu_{\rm lin}\) | exact real-bound bits | least integer \(R_B^{\mathbb Z}\) | integer bits |
|---|---|---:|---:|---:|---:|---:|
| KoalaBear | strict numerator-leading | 67,472 | 4.746562 | -4.746562 | 1 | 0 |
| KoalaBear | full denominator | 67,473 | -26.242123 | 26.242123 | 79,371,788 | 26.242123 |
| Mersenne-31 | strict numerator-leading | 67,448 | -10.258853 | 10.258853 | 1,226 | 10.259743 |
| Mersenne-31 | full denominator | 67,449 | -41.258853 | 41.258853 | 2,631,190,720,614 | 41.258853 |

The pinned \(\mathbb F_{97}/\mu_{16}\) full-denominator fixture in the preceding
packet has rank four and nonempty slices, so its least positive integral
overhead is at least

\[
  \left\lceil\frac{97^4}{\binom{16}{7}}\right\rceil
  =7739.                                              \tag{20}
\]

These numbers are not a deployed row verdict.  They prove a narrower and
load-bearing point: a uniform small-overhead theorem for each fixed multiplier
cannot be obtained from the rank exponent alone.  In the subunit cases every
valid real overhead must absorb the exact real-bound bits; integral compiler
bookkeeping must absorb the displayed ceilings.

## 9. Correction to the preceding compiler target

Equation (17) of
bc_first_interior_general_line_modular_fibers.md proposed a fixed-\(B\)
row-sharp input

\[
  |\operatorname{MLFib}_B|
  \le R_B\binom nm s^{-\operatorname{rank}_{\rm monic}L_B}.
\]

It remains a logically sufficient conditional inequality, but the phrase
that the fixed-word dimension balance was exact was too strong.  The rank
exponent is exact; a useful overhead is not automatic.  On a root-free chart,
one sufficient Fourier choice supplied by this packet is

\[
  R_B^{\rm Fourier}:=
  \kappa(W_1)(1+\mathcal A_{W_1,h}),                 \tag{21}
\]

while (18) constrains every admissible choice on a nonempty subunit slice.

Consequently, naively adding an integer-rounded estimate over up to \(s\) or
\(s^2\) multipliers may contribute a dominant slice-count term.  The next
finite compiler must instead prove one of:

1. an aggregate fixed-word incidence bound

   \[
     \sum_{B\in\mathcal B_{\rm rem}}
       |\operatorname{MLFib}_B|
     \le R_{\rm agg}\binom nm s^{-w};
   \]

2. a bound after ray deduplication rather than raw modular coordinates; or
3. a direct first-match slope-image theorem along the received line.

The first is still only fixed-word.  A deployed MCA theorem ultimately needs
the third projection or a theorem transferring the aggregate bound to it.

## Replay

Run

    python3 experimental/scripts/verify_bc_modular_subset_product.py

A successful run ends with:

    RESULT: PASS; mixed subset-product fibers enumerated, exchange rigidity verified, one heaviest target per case realized, real/integer floors recomputed

Typical runtime is under two minutes with the exact deployed big integers.

## Ledger impact

- **Balanced-core residual ray compiler:** the root-free fixed-\(B\) wall is
  reduced from an unnamed split-divisor estimate to the explicit mixed
  character mass (12).
- **Q:** constant \(W_1\) is exactly ordinary Q; nonconstant \(W_1\) adds a
  quotient-algebra factor and is not implied by Q alone.
- **First match:** domain-root \(W_1\), periodic/quotient supports, and
  extension-field transfer remain separate earlier owners.
- **Finite rows:** the fixed-slice integer floors rule out a silent
  per-multiplier dimension-count payment.  No row changes status.

## Nonclaims

- No bound on \(\mathcal A_{W_1,h}\) is proved.
- No arbitrary-\(W_1\) domain-root or gluing stratum is included.
- No base/extension-field transfer is asserted.
- No aggregate multiplier, LineRay, or slope-image bound is proved.
- No deployed upper ledger or adjacent threshold is closed.
- The faithful-average census is evidence and a regression surface, not an
  asymptotic equidistribution theorem.
