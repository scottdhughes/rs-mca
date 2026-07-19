# Dyadic complete-fiber slicing route cut

Claim: For every field, finite multiplicative subgroup, admissible `K,m`, arbitrary received word, and divisor `c` of the subgroup order, distinct list polynomials have at most `floor((K-1)/c)` common canonical complete `c`-fibers; the deployed dyadic specialization pays `57121027290597096` elements.
Status: PROVED theorem and finite ROUTE_CUT; the official score remains `0/2`.
Verifier: `experimental/data/certificates/dyadic-complete-fiber-slicing/verify_role07_dyadic_full_fiber_cut.py` replays the deployed integer ledger; `verifier_output.txt` is canonical and `SHA256SUMS` binds both files. `experimental/scripts/verify_dyadic_complete_fiber_intersection_formalization.py` fail-closes the source/Lean correspondence and package locks and includes a tamper self-test.
Consumers: It remains to prove, for each of the `1792` residual nested profiles, a uniform first-match sublist cap of `121502836610262`; a violator forces one profile to contain at least `121502836610263` elements.
Risk-limits: The verifier checks arithmetic, not the field-theoretic proof; no Grand List closure, Grand MCA result, extension-field list theorem, rank-cell closure, or unpublished recurrence is consumed or claimed.

## Exact theorem

Let `F` be a field, let `H <= F^x` be a finite multiplicative subgroup of
order `n`, and let

```text
1 <= K <= m <= n.
```

Fix a total order on `H`. For an arbitrary received word `U : H -> F`, put

```text
L(U) = {P in F[X] : deg(P) < K and |{x in H : P(x)=U(x)}| >= m}.
```

For each `P in L(U)`, let `S_P` be the first exactly `m` agreement points.
For a positive divisor `c | n`, define

```text
pi_c : H -> Q_c,       pi_c(x) = x^c,
Q_c = pi_c(H),         N_c = |Q_c| = n/c,
E_c(P) = {y in Q_c : pi_c^{-1}(y) is contained in S_P},
e_c(P) = |E_c(P)|,     h_c = floor((K-1)/c).
```

Every `pi_c`-fiber has exactly `c` elements. For every two distinct
`P,Q in L(U)`,

```text
|E_c(P) intersect E_c(Q)| <= h_c.                       (1)
```

Consequently, for every fixed `e >= h_c+1`,

```text
#{P in L(U) : e_c(P)=e}
  <= floor(binomial(N_c,h_c+1) / binomial(e,h_c+1)).     (2)
```

Writing `d=e-h_c` and `r=floor((d-1)/2)`, the independent Johnson-ball
packing bound is

```text
#{P in L(U) : e_c(P)=e}
  <= floor(
       binomial(N_c,e)
       / sum_{i=0}^r binomial(e,i) binomial(N_c-e,i)
     ).                                                  (3)
```

The quantifier over `U` is universal. Thus this is a source-realized
received-word theorem, not merely an abstract set-system estimate.

## Proof

For distinct `P,Q`, every `x in S_P intersect S_Q` satisfies
`P(x)=U(x)=Q(x)`. The nonzero polynomial `P-Q` has degree at most `K-1`, so

```text
|S_P intersect S_Q| <= K-1.
```

Each member of `E_c(P) intersect E_c(Q)` contributes its whole, disjoint
`c`-point fiber to this intersection. Hence

```text
c |E_c(P) intersect E_c(Q)| <= K-1,
```

which is (1). No `(h_c+1)`-subset of `Q_c` can occur in two equal-size
fiber sets, proving (2) by double counting. In the Johnson graph `J(N_c,e)`,
(1) gives minimum distance at least `e-h_c`; disjoint balls of radius
`floor((e-h_c-1)/2)` prove (3).

The only group fact used above is that a finite subgroup of a field's
multiplicative group is cyclic. Therefore `c | n` makes the kernel of
`x -> x^c` have exactly `c` elements. In positive characteristic the order
of `H` is automatically prime to the characteristic; no additional
characteristic hypothesis is hidden.

## Deployed ledger

The base-field row is

```text
p = 2130706433, n = 2097152, K = 1048576,
sigma = 67471, m = 1116047, t = 981105,
T = 274854110496187592.
```

The verifier proves `p` prime and `p-1=1016n`. At level `c=2^15=32768`,
`N_15=64` and `h_15=31`. The disjoint paid categories are

```text
e_15=33:                                  55534064877048198
e_15=34:                                   1586961812468508
e_15<=32 and e_16=16:                        601080390
paid total U_dyadic:                      57121027290597096
```

The first line uses (2), the second uses the radius-one case of (3), and the
third uses (2) at `c=2^16`. The categories are disjoint: a complete
`2^(j+1)`-fiber is the union of two complete `2^j`-fibers, so
`e_j >= 2e_(j+1)`. In particular, `e_16=17` was already paid by
`e_15>=34`, while the new `e_16=16` category outside `e_15>=33` forces
`(e_15,e_16)=(32,16)`.

Every residual element therefore has

```text
(e_15,e_16,e_17,e_18,e_19,e_20) <= (32,15,7,3,1,0)
and e_j >= 2e_(j+1).
```

There are exactly `1792` such integer profiles. If `|L(U)| >= T+1`, the
residual has size at least

```text
T+1-U_dyadic = 217733083205590497,
```

so one profile has at least `121502836610263` elements. Conversely, the
still-unproved uniform residual cap `121502836610262` gives

```text
U_dyadic + 1792 * 121502836610262
  = 274854110496186600
  = T-992.
```

This last implication is exact, but its fixed-profile premise is not proved.

## Source and field ledger

For a weighted GRS code with nonzero multipliers, coordinatewise division by
the multiplier vector preserves every coordinate equality and reduces the
list problem to the ordinary RS word `U`. For a fixed syndrome, choosing one
received representative identifies nearby codewords with errors in that
syndrome coset. Since the theorem holds for every `U`, it applies to every
base-field syndrome.

All polynomials, evaluations, roots, received words, and fibers above live
over `F_p`. The extension-size quantity `p^6` appears only in the challenge
denominator used to derive `T`; no list theorem over `F_(p^6)` is asserted.
The canonical first-`m` rule makes the paid and residual classes disjoint and
exhaustive even when a codeword has more than `m` agreements.

## Novelty and nonclaims

At `origin/main@c35a6da31`, no deployed constant in this note occurs in the
tree. Existing complete-fiber machinery is not rebranded: the new delta is
the arbitrary-received-word root-intersection compiler, its fixed-`e`
packings, and the exact `2^15/2^16` disjoint ledger. The ordinary Hahn lanes
owned by PRs `#755` and `#756` are separate and are neither duplicated nor
used as proof inputs.

The literal Grand List theorem remains open, and the official score remains
`0/2`. No counterexample, fixed-profile Pade ceiling, rank-15 or rank-16
closure, universal extra Forney defect, Fourier maximum-from-average step,
Grand MCA theorem, asymptotic theorem, or recurrence claim is included.

The standalone Lean 4.28 / Mathlib package at
`experimental/lean/dyadic_complete_fiber_slicing/` now proves equation (1) as
`DyadicCompleteFiberSlicing.completeFiberIntersection`, with the field,
subgroup, order, degree, agreement, divisor, received-word, and distinctness
hypotheses printed above.  Its local classical `DecidableEq F` is an
elaboration instance and does not add a public theorem parameter.  The Lean
result does not certify the packing consequences (2)--(3), the deployed
integer ledger, the residual `1792`-profile cap, the GRS/syndrome transport,
Grand List, Grand MCA, or an exact-threshold conclusion.

## Artifact audit

The verifier in this package is byte-identical to the readable source embedded
in the R17B Role 07 return. Its actual SHA-256 is
`ae75af706c6fa222fba4251bdbd4344798762ed7fca41122d25292b8fe36b27c`.
The return's separate claimed verifier digest
`262ee4f55cf2990b96103c0e0e7f93aa33969b528ed7bbb955222f0eca101cc7`
does not match that embedded source and is not propagated. The claimed output
digest does match the canonical transcript:
`7d884ffb903d13964c5376046baa6f370d476e7a6da9e881817b146be2e6ba3e`.
