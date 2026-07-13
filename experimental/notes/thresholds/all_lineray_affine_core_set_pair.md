# All-LineRay affine-core set-pair theorem

## Status and exact delta

```text
Status: PROVED (field-general all-pair theorem, nested two-level corollary,
and LineRay specialization).
HARD INPUT 3 SERVED: residual ray compiler for higher-dimensional balanced
cores, on the global-core and selector/fiber sublinear branches.
```

This packet upgrades the integrated selected-witness affine-core theorem to
the complete deduplicated line-ray object.  It counts every distinct
`(slope,codeword)` pair at once, including arbitrarily many codewords at one
slope.  The base theorem chooses no witness selector; the stronger two-level
corollary works with every one-per-slope selector.

Let `H : F^U -> W` be linear, `N=|U|`, and `mathcal K=ker H`.  Let `P` be a finite
set of distinct pairs `(gamma,e)` satisfying

```text
H e = y_0 + gamma y_1,       y_1 != 0,
wt(e) <= t,                  d(mathcal K) > t,
{y_0,y_1} not subset H(F^supp(e)).                       (1)
```

For nonempty `P`, fix any `e_*` occurring in `P` and put

```text
A_P = span{e-e_* : (gamma,e) in P},
s   = dim A_P,
w   = max_(gamma,e in P) wt(e).                          (2)
```

Then

```text
sum_((gamma,e) in P) 1/binom(s+wt(e),s) <= 1,            (3)

|P| <= binom(s+w,s) <= binom(N,s).                       (4)
```

The empty family is trivial.  If `s=0`, then `|P|<=1`.  If `s=1`, (3)
gives the sharp all-pair bound `|P|<=w+1`; same-slope multiplicity is not an
exception.

For `C=RS_F(D,K)` at agreement `m>=K`, take `H` to be a parity check and
`e=u+gamma v-c` for every pair

```text
(gamma,c) in LineRay_E(u,v;m).
```

After the common-support branch has been removed and `H v != 0`, (1) holds
for every retained pair, `t=n-m`, and therefore

```text
|LineRay_E(u,v;m)| <= binom(s+n-m,s).                    (5)
```

Here `s` is the affine dimension of **all** retained error vectors, not the
minimum dimension of one selected witness per slope.  Thus `s=o(n)` pays the
recorded all-LineRay target with an `exp(o(n))` loss.  Even when `s` is
linear, the nested theorem below pays if both a selector core and every
same-slope core are sublinear.  The remaining branch has linear actual weight
and lacks that two-level low-rank decomposition.

This is a selector-free extension of holmbuar's proof in integrated PR #681.
The Codex team developed and independently audited the all-pair upgrade.

## Source interfaces and ownership boundary

- `experimental/grande_finale.tex`, `def:line-rays`, defines
  `LineRay_E(u,v;m)` as the set of deduplicated `(slope,codeword)` pairs.
- `prop:line-ray-saturation` places this pair count between the slope
  projection and the raw support census.
- `experimental/notes/thresholds/lineray_census_rerecording.md` records the
  all-LineRay target and leaves its upper bound open.
- `experimental/notes/thresholds/a6_actual_witness_core_rank_preflight.md`
  proves (3)--(4) only after fixing one witness for every slope.  Its selector
  sensitivity is explicit in Section 7.
- `experimental/notes/thresholds/canonical_reduced_rational_host_compiler.md`
  identifies its exact rational-host incidence with `LineRay`, but proves no
  upper bound for that count.

The new point is not a different binomial estimate.  It is that the same
zero-mask/set-pair proof applies to the entire pair set.  Same-slope error
differences lie in `ker H` and are automatically included in `A_P`.

## Proof

### 1. Every complete zero mask detects the all-pair affine core

For `(gamma,e) in P`, write

```text
S_e=supp(e),       T_e=U\S_e.
```

First, `H(A_P) subset <y_1>`, since

```text
H(e-f)=(gamma-delta)y_1                                  (6)
```

for any two pairs `(gamma,e),(delta,f)`.

We claim that restriction

```text
A_P -> F^T_e                                                (7)
```

is injective.  Let `z in A_P` vanish on `T_e`.  Then `z` is supported in
`S_e`, so `wt(z)<=wt(e)<=t`.  By (6), write `H z=beta y_1`.

If `beta=0`, then `z in mathcal K`; the distance hypothesis
`d(mathcal K)>t` forces `z=0`.
If `beta!=0`, set `q=beta^{-1}z`.  Both

```text
H q=y_1,
H(e-gamma q)=y_0                                           (8)
```

have lifts supported in `S_e`.  This contradicts the transverse clause in
(1).  Hence (7) is injective.

This argument is pairwise and uses no slope selector.  When two pairs have
the same slope, their difference simply falls into the `beta=0` branch.

### 2. Canonical zero minors recover complete error vectors

Fix a basis `b_1,...,b_s` of `A_P` and let `B` be its `N x s` coordinate
matrix.  Injectivity of (7) says that `B` restricted to `T_e` has column rank
`s`.  Choose an `s`-subset

```text
I_e subset T_e,       det B[I_e] != 0.                    (9)
```

Every error has a unique expression `e=e_*+B x_e`.  Since `e` vanishes on
`I_e`,

```text
B[I_e] x_e = -e_*|I_e.                                   (10)
```

The invertible system (10) recovers the whole vector `e`.

Consequently, for two distinct pairs `(gamma,e)!=(delta,f)`,

```text
I_e intersect supp(f) != empty.                          (11)
```

Indeed, otherwise both `e` and `f` vanish on `I_e`, so (10) gives `e=f`.
Applying `H` and using `y_1!=0` gives `gamma=delta`, contradicting distinctness
of the pairs.

### 3. Nonuniform set-pair charge

The pairs of coordinate sets

```text
(I_e,supp(e))
```

have diagonal disjointness by (9) and ordered cross-intersection by (11).
The nonuniform Bollobas set-pair inequality therefore gives

```text
sum_((gamma,e) in P)
  1/binom(|I_e|+|supp(e)|,|I_e|) <= 1.
```

Since `|I_e|=s`, this is (3).  Every denominator in (3) is at most
`binom(s+w,s)`, proving the first inequality in (4).  For a pair of maximum
weight `w`, injectivity of (7) gives `s<=|T_e|=N-w`; hence `s+w<=N`, proving
the second inequality.

If `s=0`, every error equals `e_*`.  Its syndrome equation and `y_1!=0`
force every slope to be equal as well, so distinctness of pairs gives
`|P|<=1`.  The empty-minor convention agrees with (3)--(4).

If at least two slope values occur, then `H(A_P)=<y_1>` and rank-nullity gives

```text
s=dim(A_P intersect mathcal K)+1.                        (12)
```

If all pairs have one slope, then `A_P subset mathcal K`; the theorem still
counts every codeword in that ray.

## LineRay corollary

Let `C=ker H` be a length-`n` linear code of minimum distance greater than
`t=n-m`, and let `U_gamma=u+gamma v`.  If `H v=0`, then `v` itself is a
codeword and every ray produces a common support: on the zero mask of its
error, `u` agrees with `c-gamma v` and `v` agrees with itself.  Hence the
residual is empty after the common-support branch is removed.

Assume from now on that `H v!=0`.  Then the map

```text
(gamma,c) |-> e_(gamma,c)=u+gamma v-c                    (13)
```

is injective.  A line ray at agreement at least `m` has
`wt(e_(gamma,c))<=t` and the syndrome equation in (1), with
`y_0=H u`, `y_1=H v`.

If both syndromes had lifts supported on `supp(e_(gamma,c))`, then `u` and
`v` would both agree with codewords on the complementary agreement set of
size at least `m`.  This is exactly a common support.  Once that branch is
paid first, every retained ray is transverse.

For Reed--Solomon codes, `d(C)=n-K+1>n-m` whenever `m>=K`.  The general
theorem applied to (13) proves (5).

This is stronger than a slope bound: one slope with many retained codewords
contributes every one of them to the left side and to the affine dimension.
The rational-host equality

```text
M_RH=|LineRay_F(r_0,r_1;m)|
```

from the integrated canonical compiler therefore inherits (5) whenever its
all-pair error core has dimension `s` and its residual rays are transverse.

## Nested slope/fiber theorem

The global affine dimension can be linear merely because different slopes
carry independent kernel directions.  The complete pair count still pays
when that rank decomposes at two levels.

Let `Gamma` be the slope projection of `P`.  For every `gamma in Gamma`,
write

```text
P_gamma={(gamma,e) in P},
```

and choose one representative `a_gamma in P_gamma`.  Let

```text
D_sel   = span{a_gamma-a_gamma0 : gamma in Gamma},
r       = dim D_sel,
A_gamma = span{e-f : (gamma,e),(gamma,f) in P_gamma},
s_gamma = dim A_gamma,
w_sel   = max_gamma wt(a_gamma),
w_gamma = max_((gamma,e) in P_gamma) wt(e).
```

The choice is arbitrary.  Every nonempty family satisfying (1) obeys the
nested nonuniform charge

```text
sum_(gamma in Gamma) sum_((gamma,e) in P_gamma)
  1 / (binom(r+wt(a_gamma),r)
       binom(s_gamma+wt(e),s_gamma)) <= 1.               (TL1)
```

Consequently,

```text
|P| <= binom(r+w_sel,r)
       max_(gamma in Gamma) binom(s_gamma+w_gamma,s_gamma).  (TL2)
```

To prove (TL1), apply (3) first to the representative family.  For a fixed
slope, `A_gamma subset mathcal K`.  If a vector in `A_gamma` vanishes off
`supp(e)`, then it is a kernel word of weight at most `t`, hence is zero.
Thus every zero mask in `P_gamma` detects its local direction space, and the
same minor/set-pair proof gives

```text
sum_((gamma,e) in P_gamma)
  1/binom(s_gamma+wt(e),s_gamma) <= 1.
```

Multiply this local inequality by the representative charge at `gamma` and
sum over slopes.  Equation (TL2) follows by bounding every denominator in
(TL1) by the displayed product.  The result may be minimized over all
one-per-slope selectors.
Under the LineRay specialization (13), `P_gamma` is the full retained
codeword list at slope `gamma`, and `a_gamma` is any one retained ray at
that slope.  Thus (TL1)--(TL2) count the complete LineRay pair set.


The direction spaces satisfy the exact algebraic decomposition

```text
A_P = D_sel + sum_(gamma in Gamma) A_gamma.               (TL3)
```

When at least two slopes occur,

```text
dim(D_sel intersect mathcal K)=r-1,
A_P intersect mathcal K
  =(D_sel intersect mathcal K)+sum_gamma A_gamma.         (TL4)
```

Indeed, subtracting the chosen representative in each fiber proves (TL3).
The syndrome map sends every representative difference to a scalar multiple
of `y_1`, and two distinct slopes make its image one-dimensional; this proves
(TL4).

For `N=O(n)`, (TL2) is `exp(o(n))` whenever some selector has

```text
r=o(n),       max_gamma s_gamma=o(n),
```

uniformly in the actual error weights.  This can hold even if `dim A_P` is
linear.  Therefore an unpaid exponential family cannot have both a
sublinear-rank selector and uniformly sublinear same-slope fibers.  The
remaining structural alternatives are a high-rank same-slope affine
code-coset list or the absence of every low-rank transversal.

The verifier includes an exact split-hierarchy fixture.  Take two
block-diagonal copies of the sharp map below.  Use the `q` errors
`(e_a,0)` at slope zero and the `q` errors `(0,e_a)` at slope one, with

```text
y_0=(H e_0,0),       y_1=(-H e_0,H e_0).
```

The direct-sum kernel still has distance `q>t=q-1`; transversality holds
because each support lies in one block.  The global affine dimension is
three, while `r=1` and both local dimensions are one.  Its nested charge is
`2/q`; the two-level cap is `q^2`, versus the one-level cap
`binom(q+2,3)`, a strict improvement for `q>=3`.

## Sharp same-slope family

The `s=1` constant `w+1` in the field-general linear-code theorem is attained
by pure same-slope multiplicity over every prime field `F_q`.  This is not an
RS/GRS sharpness example.

Take coordinates `U=F_q disjoint_union {infinity}`, target `W=F_q^q`, and
define

```text
H(x)=((x(t)-x(0))_(t in F_q\{0}), x(infinity)).          (14)
```

Then

```text
ker H={<a,a,...,a,0>:a in F_q},       d(ker H)=q.         (15)
```

For each `a in F_q`, put

```text
e_a(t)=a+t  (t in F_q),       e_a(infinity)=0.           (16)
```

All `q` errors have the same syndrome `y_0=H(e_0)`, the same slope `gamma=0`, and
weight `q-1`.  Choose `y_1` to be the last coordinate vector in the target of
`H`.  No support of an `e_a` contains `infinity`, so `y_1` has no lift on that
support; (1) holds with `t=q-1`.  The differences of the errors span the
one-dimensional kernel, so `s=1`, `w=q-1`, and

```text
sum_a 1/binom(q,1)=1,       |P|=q=w+1.                  (17)
```

For a literal LineRay realization with slope set `E={0}`, take `u=e_0`, let
`v` be the unit vector at `infinity`, and put `c_a=u-e_a in ker H`.  Then all
`(0,c_a)` are distinct line rays of one received word, each with agreement
exactly two.  These are all threshold-two rays at that slope, and there is no
common two-support.  Thus a selector that keeps one codeword at the slope
loses a factor `q`, while the all-pair theorem is exact.

## Consequences

### Asymptotic payment

For `N=O(n)`,

```text
log binom(s+w,s)
 <= min(s log(e(s+w)/s), w log(e(s+w)/w)).                (18)
```

Hence either `s=o(n)` or `w=o(n)` makes the complete pair count
`exp(o(n))`.  Since the recorded LineRay target has a `max(1,...)` scale,
this pays it on every such transverse chart.  The nested theorem additionally
pays `r=o(n)` together with `max_gamma s_gamma=o(n)`, even for linear global
`s`.  An unpaid positive-rate chart must have linear actual weight and must
either contain a linear-rank same-slope fiber or admit no sublinear-rank
selector.

### Exact finite calibration

The verifier replays the two orientation rows printed in the LineRay target
note.  Conditional on `s=1`, (5) gives

```text
KoalaBear:   n=2097152, m=1116046, |LineRay|<=981107,
Mersenne-31: n=2097152, m=1116022, |LineRay|<=981131.
```

These are below the respective first-interior stripped pair floors
`65065153468` and `1993678`.  This is a conditional branch payment, not a
certificate that either deployed residual has `s=1`; the machine certificate
marks both deployed residual dimensions uncertified.

## Verification and formalization target

Run

```bash
python3 experimental/scripts/verify_all_lineray_affine_core.py --check
python3 -O experimental/scripts/verify_all_lineray_affine_core.py --check
python3 experimental/scripts/verify_all_lineray_affine_core.py --tamper-selftest
(cd experimental/lean/grande_finale && lake env lean GrandeFinale/AllLineRayAffineCore.lean)
```

The standard-library verifier uses exact prime-field arithmetic.  It
enumerates every transverse complete pair set for the canonical parity-check
map over `F_2` and `F_3`, recomputes the all-pair affine dimension, checks
every zero-mask restriction and canonical minor, and verifies the
cross-intersection system and exact Fraction form of (3).  It also checks
2,456 nested charges across the complete, deletion, and same-slope families.
Over `F_2,F_3,F_5,F_7` it verifies both the sharp same-slope list and the
split-hierarchy fixture, including exact ray exhaustiveness and absence of a
common two-support.  Finally it replays the finite orientation arithmetic and
rejects fourteen strict-JSON tamper classes.

The Lean module is an **UNPROVED STATEMENT TARGET**.  It type-checks the
field-general hypotheses, the all-pair affine dimension, both nonuniform
charges, the one-per-slope representative condition, both product bounds,
the (TL3)--(TL4) direction-space and kernel-intersection identities, and the
generic and LineRay error specializations.  It does not claim a Lean
proof.

## Nonclaims and exact remaining wall

- No general payment is proved for a linear-rank, linear-weight same-slope
  affine code-coset list.
- No theorem forces a sublinear-rank selector or uniformly sublinear local
  fiber ranks from RS moment, locator, first-match, or profile structure.
- Raw LineRay pairs are not declared transverse before the common-support
  branch is removed; (5) must not be used without that hypothesis.
- No witness-exhaustive atlas, chart census, profile-envelope sum, Q theorem,
  signed-minor payment, lower reserve, Grand MCA/List theorem, finite adjacent
  crossing, or prize threshold is claimed.
- The rational-host consequence is conditional on host membership; no general
  section-nonpositive host extraction is asserted.
- No stable paper TeX or PDF is changed.

The exact next target is a low-rank transversal theorem for the affine fibers
`P_gamma`, with the alternative producing one linear-rank same-slope
RS/GRS-coset list.  Such a high-rank local list then needs a polynomial-value
or beyond-Johnson input rather than another mask-by-mask generalized-weight
count.
