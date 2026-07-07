# CAP25 v13 Q first-match leakage compiler

Status: COUNTERPACKET / REPAIR / EXACT_NEW_WALL.

This note records a support-level correction to the CAP25 v13 finite
first-match Q ledger.  It does not prove the adjacent upper ledger and does not
prove

```text
U(1116048) <= B*.
```

The point is narrower: target-label overlap with an earlier paid Q/quotient
cell is not support deletion.  Any finite first-match certificate that uses
prefix-target labels must either prove support-level saturation, or introduce
and pay the leakage branch defined below.

## Claim killed

Let `Q` be a Q prefix-boundary support cell, let `E_<Q` be the union of
support-level cells paid before `Q`, and let `tau` be the prefix target map
used by the finite first-match ledger.  The false support-deletion target is

```text
Q cap tau^{-1}(tau(E_<Q)) <= E_<Q.
```

Equivalently, the false proof line is

```text
same tau-target as an earlier paid witness
    => same support-level cell.
```

The premise is target-level.  Earlier-cell membership is a predicate on the
support or witness itself.

## Explicit counterpacket

Work in `D = F_17^*`, with `m = 4`, and use the prefix target

```text
tau(M) = (p_1(M), p_2(M)),
p_i(M) = sum_{x in M} x^i.
```

The quotient-paid support

```text
E = {4, 6, 11, 13} = {+/-4, +/-6}
```

is a union of `mu_2`-fibers.  Its prefix target is

```text
p_1(E) = 4 + 6 + 11 + 13 = 34 = 0 mod 17,
p_2(E) = 16 + 36 + 121 + 169 = 342 = 2 mod 17.
```

The primitive support

```text
M = {1, 2, 4, 10}
```

has the same target:

```text
p_1(M) = 17 = 0 mod 17,
p_2(M) = 1 + 4 + 16 + 100 = 121 = 2 mod 17.
```

But `M` is not a `mu_2` quotient-pullback support: multiplication by `-1`
sends `1` to `16`, and `16 notin M`.  Thus a target fiber can contain both an
earlier quotient-paid support and a primitive Q support.  This is a direct
counterpacket to support-wise deletion from target equality.

A second small-field form of the same defect appears over `F_11^*`: one can
choose a `mu_2`-closed support and a primitive support with equal first two
power sums.  The phenomenon is not tied to the particular `F_17` numbers.

## Corrected leakage object

The first-match Q cell must be split as

```text
Q = Q_paid dotcup L_Q dotcup Q_new,
```

where

```text
Q_paid = Q cap E_<Q,
L_Q    = (Q cap tau^{-1}(tau(E_<Q))) \ E_<Q,
Q_new  = Q \ tau^{-1}(tau(E_<Q)).
```

Here `L_Q` is the target-label leakage: Q witnesses whose prefix target was
already hit by an earlier support, but which are not themselves earlier-paid
supports.

The deleted theorem is the special case

```text
L_Q = empty.
```

The round of hostile returns gives no reason to believe this special case is
true in the quotient-before-Q interface.  The valid theorem has to be a leakage
compiler:

```text
pay Q by support-level first match:
  paid earlier supports,
  genuinely new Q targets,
  and the explicit leakage branch L_Q.
```

## PR #386 interface

PR #386 records the KoalaBear MCA adjacent candidate row

```text
n = 2^21,
k = 2^20,
A = 1116048,
j = 981104,
t = 67472,
w = 67471,
```

and reports the partial first-match remainder

```text
K_rem = floor((B* - B_gen - B_quot_terminal) * p^w / binom(n,j))
      = 4805007.
```

This note does not replay that integer certificate.  It records the support
soundness condition it must satisfy if Q target labels are used for
deduplication:

```text
p^w * (nu(Q_new) + nu(L_Q)) <= K_rem * binom(n,j),
```

with `nu` equal to the exact numerator convention of the first-match verifier.

The verifier should reject any certificate that subtracts
`tau(E_<Q)` from Q support mass unless one of the following is supplied:

1. a checked support-saturation theorem `L_Q = empty`;
2. an exact row-sharp leakage bound for `nu(L_Q)`;
3. a proof that `tau` is itself the final numerator key for that branch, so
   support multiplicity is irrelevant.

This agrees with PR #386's nonclaim that it does not prove
generated-prefix lift-class support payment from image-cell labels.

## Collision algebra available for leakage

If two `m`-supports `M` and `E` have the same first `w` prefix data, write

```text
Lambda_M  = G A,
Lambda_E  = G B,
deg A = deg B = e = |M \ E| = |E \ M|.
```

Equal first `w` power sums, equivalently equal first `w` elementary symmetric
functions under the deployed characteristic hypotheses, force

```text
deg(A - B) <= e - w - 1.
```

In particular, a nontrivial collision has

```text
e >= w + 1.
```

Minimal leakage therefore has the same split-pair/Pade flavor as the BC/SP
wall rather than being an automatic quotient deletion.  This algebra is useful
only after one also proves a row-sharp count or a support-level assignment of
the resulting leakage pairs.

## Finite-row warning

For KoalaBear MCA, the raw Q slack is about `22.2` bits before all side
ledger deductions.  A generic multiplicative leakage repair can easily spend
bits that the exact finite certificate needs.

For the Mersenne-31 rows, the margins are only about `3.3` and `3.1` bits; in
the current notes these correspond to tiny integer multipliers.  A blanket
factor-2 leakage compiler is therefore not safe for M31 unless it is paired
with an exact residual certificate showing enough unused slack.

Thus the missing theorem is not "Q target labels delete support mass."  It is
a row-sharp support-multiplicity theorem:

```text
CAP25-V13-QFM-MARKED-LEAKAGE-ROW-SHARP-PAYMENT
```

or a counterpacket showing that such payment cannot hold inside the deployed
row constants.

## Nonclaims

This note does not:

* prove `U(1116048) <= B*`;
* certify the KoalaBear MCA first-safe agreement;
* prove primitive Q-fin max-orbit flatness;
* close PR #386's generated-prefix support-multiplicity wall;
* provide a deployed-row counterexample to the finite frontier;
* modify Papers A-D.

It only banks the exact first false line, an explicit finite counterpacket,
and the corrected leakage object required for a sound first-match Q ledger.

## Next target

The next high-value target is a marked leakage payment theorem.  With a
canonical selector `sigma` choosing one earlier support in each prior target
fiber, attempt to inject

```text
M in L_Q
```

into marked collision data

```text
(M, sigma(tau(M)))
```

without paying an unordered-pair factor.  Then prove either:

```text
nu(Q_new) + nu(L_Q) <= row-sharp budget,
```

for the deployed KB/M31 rows, or give a scalable primitive leakage
counterpacket.  The M31 rows are the useful falsifier: any proof that loses a
generic factor is probably too blunt for the finite prize.
