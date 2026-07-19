# Affine-line Steiner saturation is C1 quotient-owned

## Status

`PROVED` for the algebraic owner classification and slope count below.
`AUDIT` for its application to the affine-line equality family in
`augmented_basis_pencil_design_inverse.md`.

This packet does **not** classify arbitrary almost-Steiner residuals and does
not close a profile ledger, a deployed row, or the asymptotic frontier.  It
proves no general almost-Steiner owner theorem, natural-scale C1 payment, row
closure, or threshold claim.

## Claim

The positive-depth affine-line family used to attain the deep-hole all-pair
paving bound does not survive to the primitive balanced-core/design residual.
Every support in that family is a complete fiber of an explicit nontrivial
uniform quotient map. Therefore it is first-match C1 quotient-owned; moreover,
its many support witnesses collapse to only one slope per quotient profile.

More precisely, let

```text
E = F_p,       F = F_q,       q = p^m,
D = F,
```

where `p >= 3` is prime and `m >= 2`. For a nonzero direction `v in F`, put

```text
gamma = v^(p-1),
pi_gamma(x) = x^p - gamma*x.
```

Then:

1. `pi_gamma` is `E`-linear with kernel `E*v`, hence it is a uniform
   `p`-to-one quotient `F -> im(pi_gamma)`.
2. Its fibers are exactly the affine `E`-lines `a + E*v`.
3. If `z = pi_gamma(a)`, the monic locator of the fiber is

   ```text
   product_(x in a+E*v) (X-x) = X^p - gamma*X - z.
   ```
4. For the hosted words

   ```text
   b_0(x) = -x^p,        b_1(x) = x,
   c_(gamma,z)(x) = b_0(x) + gamma*b_1(x) + z,
   ```

   the zero support of `c_(gamma,z)` is the quotient fiber
   `pi_gamma^(-1)(z)`. Thus the support is a pullback of a singleton on the
   smaller quotient domain.
5. Scaling `v` by `E^x` does not change `gamma`, and equality of two values of
   `gamma` forces the directions to be the same. Hence the atlas can be fixed
   in advance with exactly

   ```text
   (q-1)/(p-1)
   ```

   quotient profiles. Each profile contains `q/p` support fibers but projects
   to the single slope `gamma`. The total distinct-slope count is therefore
   `(q-1)/(p-1) <= q = |D|`, while the total support/witness count is

   ```text
   q(q-1)/(p(p-1)).
   ```

In the printed first-match order, C1 precedes C7, C8, and C9. Hence none of
these affine-line witnesses is primitive. Independently, before first-match
deletion, the `q/p` supports at one slope exhibit the local C7-style collapse
from support count to realized-slope count. This is not a general C7 payment
theorem.

## Proof

The map `pi_gamma` is additive and `F_p`-homogeneous because Frobenius is. Its
kernel consists of zero and the nonzero `x` satisfying

```text
x^(p-1) = v^(p-1).
```

Equivalently `(x/v)^(p-1)=1`. The `p-1` roots of this equation in `F_q` are
exactly `F_p^x`, so `ker(pi_gamma)=F_p*v`. Every fiber is therefore a coset of
that kernel and has size `p`.

For a fiber through `a`, write `Y=(X-a)/v`. Since
`product_(t in F_p)(Y-t)=Y^p-Y`,

```text
product_(t in F_p)(X-a-tv)
  = v^p ((X-a)^p/v^p - (X-a)/v)
  = (X-a)^p - v^(p-1)(X-a)
  = X^p - gamma*X - (a^p-gamma*a).
```

The final constant is `-pi_gamma(a)=-z`, proving the locator identity. The
received-line zero-set statement is the same polynomial identity with a minus
sign.

Finally, `v'^(p-1)=v^(p-1)` iff `(v'/v)^(p-1)=1`, iff `v'/v in F_p^x`.
Thus quotient profiles are indexed by one-dimensional `F_p` directions. Their
number is `(q-1)/(p-1)`, each image has `q/p` values, and the fibers form the
affine-geometry Steiner system `S(2,p,q)`.

## Source correspondence

The positive-depth equality fixture in
`augmented_basis_pencil_design_inverse.md` has

```text
K = span{1},  N = q,  kappa = 1,  R = q-1,
a = p,        t = q-p,                 h = p-2 > 0.
```

Its application therefore uses `p >= 3`. The quotient algebra itself also
works at `p=2`, where that source fixture has depth zero; no positive-depth
application is claimed there. The C1 and C7 correspondence is to the ordered
cell catalogue in `experimental/asymptotic_rs_mca.tex`, audited at upstream
base `3404d21b64c876c6d9b995ad3e29d7120ab27a54`.

## Consequence for the current owner wall

The affine-line equality fixture is not a counterexample to a primitive
owner/payment theorem. It is an earlier-owner regression test: any proposed
primitive design residual must explicitly delete all families whose blocks are
fibers of `x -> x^p-gamma*x`, and more generally all named quotient maps,
before invoking a Steiner/almost-Steiner inverse statement.

The genuine remaining case is therefore narrower:

> after C1 quotient pullbacks, C5 proper-field descent, common-core/planted
> owners, and C7 saturation have been removed, can a positive-density
> first-match family of nearly filled core pencils form an almost-Steiner
> packing without an image-normalized deficit?

This packet does not answer that question.

## Scope boundary

The equality fixture uses the additive full domain `D=F_q`, whereas the main
prize rows are smooth multiplicative or circle domains. The theorem therefore
routes the existing sharp fixture; it does not assert that every finite-geometry
design on a prize domain has an additive quotient owner. The atlas contains
`(q-1)/(p-1)` local quotient profiles, potentially on the order of `q`; this
packet does not turn that local classification into a natural-profile aggregate
or a closed row ledger.

## Reproducibility

```bash
python3 experimental/scripts/verify_affine_steiner_quotient_owner.py
python3 -O experimental/scripts/verify_affine_steiner_quotient_owner.py
python3 experimental/scripts/verify_affine_steiner_quotient_owner.py \
  --tamper-selftest
python3 -O experimental/scripts/verify_affine_steiner_quotient_owner.py \
  --tamper-selftest
python3 -m py_compile \
  experimental/scripts/verify_affine_steiner_quotient_owner.py
```

Bare replay is fail-closed against the checked-in certificate; `--check PATH`
may be used to audit an explicit certificate path. The verifier performs exact
arithmetic in `F_9`, `F_25`, `F_49`, and `F_121`. It checks kernels, uniform
fibers, affine-line equality, locator identities, received-line zero sets,
unique quotient-profile ownership, slope multiplicities, total line counts,
and the `S(2,p,p^2)` pair-cover property. The repository fixtures are recovered
exactly:

```text
F_9/F_3:   4 slopes x 3 supports = 12 affine lines,
F_25/F_5:  6 slopes x 5 supports = 30 affine lines.
```
