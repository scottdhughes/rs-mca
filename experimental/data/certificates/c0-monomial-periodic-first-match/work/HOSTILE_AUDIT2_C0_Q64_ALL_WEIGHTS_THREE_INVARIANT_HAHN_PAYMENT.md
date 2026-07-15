# Hostile audit 2: all fixed-residual `q=64` full-block weights

## Verdict

```text
POST-AUDIT BROADENING: INDEPENDENTLY RE-AUDITED
EVERY FIXED RESIDUAL SUPPORT: PASS, SEPARATELY
EVERY FULL-BLOCK WEIGHT f=0,...,29: PASS
606,060-STATE A8 TABLE: PASS
ALL-WEIGHT HAHN CERTIFICATES AND CAPS: PASS
AT MOST 64 REALIZED SCALAR CELLS PER FIXED LANE/RAY: PASS
SUM OVER RESIDUAL SUPPORTS: NOT CLAIMED BY THE MAIN THEOREM
GENERAL g / UNIFORM c=0 / OFFICIAL PAYMENT: NOT PROVED
```

The broadened claimant was treated as untrusted and hash-pinned at

```text
work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md
99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b

work/verify_c0_q64_three_invariant_hahn_payment.rb
baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5

work/verify_c0_q64_three_invariant_hahn_payment.expected.txt
28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1.
```

No claimant file was edited in this audit.

## 1. Arbitrary fixed-residual cancellation

Let `B=32,768`, `a=67,472`, and fix any residual support `R` in the literal
multiplicative evaluation domain.  Its locator

```text
A_R(X)=product_(x in R)(X-x)
```

has nonzero constant coefficient because every `x` is nonzero.  Therefore
`A_R` is a unit in `F_p[X]/(X^a)`, irrespective of its degree.  For two
periodic locators in the same fixed-residual lane,

```text
L_S=A_R Q_S(X^B),       L_T=A_R Q_T(X^B),
```

both equality and scalar proportionality modulo `X^a` may be canceled by
`A_R`.  Since

```text
2B<a<3B,
```

the result is exactly equality or proportionality of the three coefficients
of `Y^0,Y^1,Y^2` in the quotient block polynomials.  At fixed cardinality
`f`, these are equivalently the product and the first two inverse power sums
used by the claimant.  The signs depend on `f` but are fixed within the lane
and introduce no collision.

This proves the cancellation for every fixed residual support.  It does not
permit cancellation between two different residual locators and therefore
does not by itself sum their fibers.

## 2. The actual quotient universe and safe embedding

Let `Omega_R` be the quotient labels of complete `mu_B` cosets disjoint from
`R`.  Source-valid periodic supports have

```text
S in binom(Omega_R,f).
```

The number of labels touched by `R` is irrelevant to the upper bound:
`Omega_R` is a subset of the literal `mu_64`, so each fixed-invariant fiber
is a subcode of the corresponding fiber in `J(64,f)`.  Empty or small
`Omega_R` only shrinks it.  This validates the full-`mu_64` relaxation for
every `f=0,...,29` without asserting that the added supports are deployed
locators in that fixed-residual lane.

The distance translation is unchanged for every weight.  Equal fibers give
disjoint inverse wings with equal `e_1`, equal `e_2`, and equal product.  The
locked short-trade inputs remove distances one through seven, including the
product deletion of the size-four `mu_4`-coset trades.  Thus every nontrivial
fiber code has minimum Johnson distance at least eight.  In weights below
eight this forces fiber size one.

## 3. Independent all-weight distance-eight census

For each `f=8,...,29`, a support has at most `floor(f/4)` full `mu_4`
cosets, while its complement has at most `floor((64-f)/4)` empty cosets.
Extending smaller disjoint full/empty sets to these maximal sizes can only
add legal exchanges.  The independent verifier enumerates every maximal
completion and compares each selected coset pair against each empty coset
pair directly; it does not use the claimant's pair-sum histograms.

The exact number of enumerated states is

```text
606,060.
```

The independently recovered `A_8` caps in weight order `8,...,29` are

```text
7,6,6,6,18,16,16,16,32,28,28,28,46,40,40,40,
59,52,52,52,72,72.
```

Every claimant table entry is reproduced.

## 4. Distance-nine input

The audit rechecks all 55 source-pinned two-moment representatives literally
in the deployed field, recomputes both products, and again finds exactly one
product-equal orbit.  Expansion and unordered-pair deduplication give 64
literal trades.  Paying the whole global population at each point gives the
valid uniform bound

```text
A_9<=64
```

at every weight.  This is an overcount, not an assertion that all 64 trades
cross any one support.

## 5. Independent all-weight Hahn reconstruction

For every weight, the independent verifier starts with the ordinary
polynomial whose roots are the claimant's displayed zero set.  It expands
that polynomial in the complete normalized Hahn basis of `J(64,f)` from
its values at `0,...,m`, and only then scales the Hahn-degree-zero
coefficient to one.  This differs from the claimant's inhomogeneous
prescribed-zero solve.

For all 22 weights:

1. every nonconstant Hahn coefficient is strictly positive;
2. the ordinary-product and Hahn evaluations agree at every integer distance
   `0,...,f`;
3. the polynomial is nonpositive at every unpaid distance `10,...,f`;
4. the exact pointwise `A_8` and `A_9` payments reproduce the claimed cap.

The independent canonical coefficient stream has digest

```text
6b9fdd32619e2fd8ae53b05ac16de82e6c532bc18afecbeafda3fc66187d1d20.
```

The exact caps for `f=0,...,29` are

```text
1,1,1,1,1,1,1,1,8,11,26,91,220,516,1091,3093,
10217,20908,57196,145025,296899,614503,1241710,2465809,
3954000,6287643,10193410,14641173,20826085,25307496.
```

The maximum occurs at weight 29.  Its pre-floor value is independently
reproduced as

```text
7162373179063296/283013891=25,307,496.9350...,
```

so the uniform fixed-absolute-cell cap is `25,307,496`.

## 6. Projective scalar cells

Fix both `R` and `f`.  Canceling `A_R` also preserves projective
proportionality.  The constant coefficient of `Q_S` is

```text
(-1)^f P_S in mu_64.
```

Thus the ratio between the constant coefficients of any two realized
absolute cells in one projective ray lies in `mu_64`.  There are at most 64
nonempty scalar cells in that ray.  This argument is uniform in `R` and
`f`, but it applies separately to each fixed lane.

The arithmetic is

```text
(p-1)*25,307,496 =53,922,844,505,014,272<T,
margin            220,931,265,991,173,320,

64*25,307,496     =1,619,679,744<T,
margin            274,854,108,876,507,848.
```

The first line safely pays all `p-1` possible scalar cells, most of which
are empty.  The second uses the proved realizable-cell count.  Neither line
sums fibers belonging to different residual supports.

## 7. Separate maximal-weight residual-uniqueness observation

There is one valid strengthening not consumed by the main claimant.  It is
specific to the monomial generator `g=X^a` in the pinned periodic reduction
and to `f=29`.

At `f=29`, every residual locator has degree

```text
t-29B=30,833<B.
```

Suppose two such locators, now allowing different residual supports, lie on
one projective residue ray modulo `X^a`:

```text
A_R(X)Q_S(X^B) == lambda A_R'(X)Q_T(X^B) mod X^a.
```

Reducing further modulo `X^B` gives an equality of ordinary polynomials

```text
c_0(S)A_R = lambda c_0(T)A_R',
```

because both residual locators have degree below `B`.  They are monic and
both constants `c_0` are nonzero.  Comparison of leading coefficients gives
`c_0(S)=lambda c_0(T)`, hence `A_R=A_R'` and therefore `R=R'`.

Consequently, inside the **f=29 subpopulation only**, one projective ray
cannot mix residual supports.  The cap `1,619,679,744` therefore pays the
union over all `f=29` residual supports for the pinned `g=X^a` periodic
model.

This does not extend to `f<29`, where the residual degree is at least `B`
and reduction modulo `X^B` sees only a truncation.  It also does not prevent
an `f=29` locator and an `f<29` locator from occupying the same projective
ray.  Hence it does not pay the union over all block weights, and it says
nothing about general monic `g`.

## Exact scope and nonclaims

The broadened theorem is accepted for each fixed residual support and each
full-block weight separately.  The additional residual-uniqueness lemma pays
the union over residual supports only in the `f=29`, `g=X^a` subpopulation.
No theorem here sums residual supports for `f=0,...,28`, mixes all block
weights, covers nonperiodic supports, or treats arbitrary degree-`67,472`
generators.  No uniform `c=0`, higher-`c`, or official payment follows.

## Independent artifacts

```text
work/audit2_c0_q64_all_weights_three_invariant_hahn_payment.rb
work/audit2_c0_q64_all_weights_three_invariant_hahn_payment.expected.txt
```

Run

```bash
ruby --disable-gems -w \
  work/audit2_c0_q64_all_weights_three_invariant_hahn_payment.rb
```

and require byte equality with the expected output.
