# Dense-shell general-K root toggle and top-support charge pairing

## Status

```text
Status: PROVED (exact all-depth identities).

For every depth B >= 1 and every decoration set
K subseteq {2,...,B}, inserting the first scan position multiplies the
entire decorated root cascade by exactly 1/4:

  Gcal_B^{K union {1}}(x) = (1/4) Gcal_B^K(x).

For every B >= 2 and V subseteq {0,...,B-2}, adding the top support digit gives
U = V union {B-1} and pairs the two support-class sums exactly:

  Sigma_U = -Sigma_V.

Consequently the predicted class-sum sign margin is identical for the
pair, and the repaired positive-charge interface satisfies

  Omega_U + Omega_V = (M_U + M_V)/2

without a sign-law hypothesis.
```

These are identities, not censuses.  They use no finite grid, `MASTER`,
`INV-TAIL`, cone-purity claim, or positivity assumption.  They do not prove
the remaining root-free decorated charges positive.

Source floor: `upstream/main@3404d21`.  This note uses the repaired C1/C3b/C6
interface in `dense_shell_class_charges.md` (the repair shipped through #917)
and generalizes the terminal root-anchor identity of #924 from the single set
`{B-1,B}` to every remaining decoration set.  The class-charge framework and
repair are due to Holm Buar; the terminal two-level theorem is due to
DannyExperiments.

Two in-session cross-checks preceded shipping.  One re-derived the root and
prefix factorization and checked its scan/support index flip.  The other
checked the Fourier/class-charge parity algebra and compiled the generic Lean
compiler.  These are scoped in-session checks, not external verification.

The deterministic replay is
`experimental/scripts/verify_dense_shell_general_k_root_anchor.py`.  It uses
exact rational arithmetic to exercise every compiler identity through finite
depth, checks required source markers, and has a fail-closed tamper self-test.
The marker check is not a cryptographic source binding.  The finite replay is
a regression check; the proof is the termwise argument below.
The algebraic compiler is kernel-checked in
`experimental/lean/dense_shell_general_k_root_anchor/`.

## 1. Definitions

Let a dense word be `d=(d_1,...,d_B) in {+1,-1}^B`, and define its scan by

```text
u_0(d) = 0,
u_k(d) = (d_k + u_{k-1}(d))/3,
a_k(d) = sin^2(pi u_k(d)),
q_k(d) = a_k(d) - 1/2.
```

Write

```text
P_d(x) = product_{j=1}^B (x-a_j(d)).
```

For `K subseteq {1,...,B}`, introduce the full-root version of the C3b
decorated cascade:

```text
Gcal_B^K(x)
  = sum_{d in {+1,-1}^B}
      (product_{k in K} q_k(d)) P_d(x).
```

This is `G^K(0;x)` in the notation of the integrated class-charge note.  The
identity below is a polynomial identity, so it remains true after taking any
coefficient, changing from the monomial basis to the shifted-Chebyshev basis,
or applying the arcsine inner product used in C3b.

For a support set `X subseteq {0,...,B-1}`, let the class sum be defined over
the inverse transform.  The Fourier cancellation in Section 3 is valid over
`C`; for the absolute/positive masses used in Section 4, assume the dense-shell
inverse values `h(sigma)` are real.  Write

```text
class(X) = {balanced residues with digit support exactly X},
Sigma_X = sum_{sigma in class(X)} h(sigma),
M_X     = sum_{sigma in class(X)} |h(sigma)|,
Omega_X = sum_{sigma in class(X)} max(h(sigma),0),
s_X     = (-1)^(B-|X|).
```

When needed, `W_X` denotes the mass whose pointwise sign is opposite to
`s_X`.  No class-sum sign law is built into these definitions.

## 2. Uniform root-toggle theorem

### Theorem 2.1 (all-K decorated root toggle)

For every `B>=1` and every `K subseteq {2,...,B}`,

```text
Gcal_B^{K union {1}}(x) = (1/4) Gcal_B^K(x)
```

as an exact polynomial identity.

### Proof

At the first scan position,

```text
u_1(d) = d_1/3 in {+1/3,-1/3}.
```

Therefore, word by word,

```text
a_1(d) = sin^2(pi/3) = 3/4,
q_1(d) = a_1(d)-1/2 = 1/4.
```

Because `1 notin K`, every summand on the left is exactly `1/4` times
the corresponding summand on the right.  Summing proves the identity.  No
cancellation and no property of the remaining scan positions is used.  QED.

### Corollary 2.2 (moments and positivity)

For arbitrary leaf weights `w(d)` and

```text
A_K = sum_d w(d) product_{k in K} q_k(d),
```

one has

```text
A_{K union {1}} = (1/4) A_K.
```

The same identity holds for the normalized moment whenever the normalizing
mass is nonzero.  In particular,

```text
A_{K union {1}} > 0  iff  A_K > 0.
```

Thus a minimal failure of the general-K drift-product positivity statement
cannot contain scan position `1`.

### Corollary 2.3 (the exact C3b earliest-decoration prefix window)

Fix `B>=2`.  Let `K` be a nonempty subset of `{2,...,B}` and put
`k_1=min K`.  The prefix window is exactly positions `1,...,k_1-1`:
`pi=(d_1,...,d_{k_1-1})` has length exactly `k_1-1`, its polynomial
`g^pi` uses exactly those scan positions, the suffix cascade ranges over
completions at positions `k_1,...,B`, and its decorations are exactly the
absolute scan positions in `K`.  In the integrated local-cascade notation,
the corresponding relative decoration pattern is
`S={k-k_1+1 : k in K}`.  Let `T_pi(K)` denote the repaired C3b charge on this
exact window.  Then

```text
T_empty({1} union K)
  = (1/4) sum_{pi in {+1,-1}^{k_1-1}} T_pi(K).
```

Indeed, partition the full-word sum defining `Gcal_B^K` by prefixes of
length `k_1-1`, factor `P_d` into its prefix and suffix polynomials, and
apply the linear functional `(-1)^B int (.) dmu`.  Theorem 2.1 supplies the
factor `1/4`.  Hence termwise positivity of all `T_pi(K)` implies positivity
of the root-anchored charge.  The converse is not claimed.

For `K={B-1,B}`, this is exactly the root-anchor deletion used in #924.  The
statement here is uniform in the remaining decoration set.

This is narrower than the original C3 claim in #880.  It is only the exact
root factorization and earliest-decoration prefix partition.  It does not
apply to an arbitrary prefix length, an arbitrary
incoming scan state, or an analytic `MASTER`/purity window, and it restores no
part of C3's missing continuum enclosure.

## 3. Fourier three-point cancellation and support pairing

Let `c=3^B`, `p=3^{B-1}`, and use the inverse transform

```text
h(sigma) = (1/c) sum_{xi dense} hatf(xi) exp(-2 pi i xi sigma/c).
```

Every dense balanced residue satisfies `xi mod 3 in {+1,-1}`.  Thus, for
every `sigma`,

```text
h(sigma-p) + h(sigma) + h(sigma+p) = 0.                 (3.1)
```

This holds termwise in `xi`, because

```text
exp(2 pi i xi/3) + 1 + exp(-2 pi i xi/3)
  = 1 + 2 cos(2 pi xi/3)
  = 0.
```

The sign convention is literal: the inverse character is
`chi_xi(sigma)=exp(-2 pi i xi sigma/c)`.  Hence shifting from `sigma` to
`sigma-p` multiplies an atom by `exp(+2 pi i xi/3)`, while shifting to
`sigma+p` multiplies it by `exp(-2 pi i xi/3)`.

At the hand-computable boundary `B=2`, take `c=9`, `p=3`, `V=empty`, and the
dense residue `xi=1+3=4` with balanced digits `(+1,+1)`.  In this embedding a
balanced least digit `-1` has unsigned residue `2 mod 3`; the proof uses
`xi mod 3 in {1,2}`, corresponding to balanced `{+1,-1}`.  With
`zeta=exp(2 pi i/3)`, the three literal atom values at `sigma=-3,0,3` are

```text
chi_4(-3) = zeta,
chi_4(0)  = 1,
chi_4(3)  = zeta^2,
```

in that order, and `zeta+1+zeta^2=0`.  The verifier checks the ordered triple,
not merely its sum, so swapping the Fourier sign is a caught mutation.

### Theorem 3.1 (top-support class-sum pairing)

Let `B>=2`, let `V subseteq {0,...,B-2}`, and put
`U=V union {B-1}`.  In particular, `B-1 notin V` is a hypothesis.  Then

```text
Sigma_U = -Sigma_V.                                    (3.2)
```

### Proof

Balanced representatives give the disjoint, no-carry decomposition

```text
class(U)
  = {sigma-p : sigma in class(V)}
    disjoint_union
    {sigma+p : sigma in class(V)}.
```

Sum (3.1) over `sigma in class(V)` and rearrange.  QED.

There is no convention for an input `V` that already contains `B-1`.  In that
case `V union {B-1}=V`, so (3.2) would assert `Sigma_V=-Sigma_V` and is false
in general.  Such an input is outside the theorem and must be rejected by a
consumer.

The boundary instances are part of the statement, not limiting shorthand:

- `V=empty` is allowed for every `B>=2`;
- all valid `V` are included at the minimal depths `B=2,3,4`;
- at the #914-analogue boundary `B=4`, `V={0}`, `p=27`, one has
  `class(V)={-1,1}` and
  `class(V union {3})={-28,-26,26,28}`.  Summing (3.1) at
  `sigma=-1,1` gives (3.2) literally.

The verifier gives these cases their own checks and mutations before running
the broader finite regression.

The same result follows from C1.  Under the index flip
`K(X)={B-i : i in X}`, one has `K(U)=K(V) union {1}`.  Theorem 2.1 and
the C1 prefactor give

```text
(-4) q_1 = (-4)(1/4) = -1.
```

Since `s_U=-s_V`, (3.2) also gives the exact margin identity

```text
s_U Sigma_U = s_V Sigma_V.                             (3.3)
```

Therefore the strict predicted class-sum sign law holds for `U` if and only
if it holds for `V`.  All top-anchored sign obligations reduce to their
root-deleted partners; only the `2^{B-1}` support sets omitting `B-1` remain.

## 4. Composition with the repaired charge interface

The always-valid identity from the #917 repair is

```text
2 Omega_X = M_X + Sigma_X.                             (4.1)
```

Adding (4.1) for the pair `(U,V)` and using (3.2) proves, without any sign-law
hypothesis,

```text
Omega_U + Omega_V = (M_U+M_V)/2.                       (4.2)
```

Likewise, directly from the definition of wrong-sign mass,

```text
2 W_X = M_X - s_X Sigma_X,
```

so (3.2)--(3.3) give

```text
W_U + W_V = (M_U+M_V)/2 - s_V Sigma_V,                 (4.3)
Omega_U + Omega_V = W_U+W_V+s_V Sigma_V.               (4.4)
```

Only when the class-sum sign law is known may the correction be rewritten as

```text
Omega_U + Omega_V = W_U+W_V+|Sigma_V|.                 (4.5)
```

This parity restriction is essential.  The packet never uses the false old
formula `Omega=Sigma+W` for both parities.

## 5. Exact scope and nonclaims

- The root-toggle theorem is uniform in `B` and `K`, but only at the global
  root `u_0=0`; it is not an arbitrary incoming-state deletion rule.
- It does not prove `T_pi(K)>0` for root-free `K`, nor does it prove the
  remaining half of the general-K class-sum law.
- Equation (4.2) is an accounting identity.  It supplies no upper bound for
  `M_U+M_V` and therefore is not by itself a class payment.
- Equation (4.5), unlike (4.2)--(4.4), consumes the class-sum sign law.
- The theorem does not consume or upgrade the P11 `B in {6,8}` census.
- The class-pair theorem has the explicit domain `B>=2` and
  `V subseteq {0,...,B-2}`.  A set already containing `B-1` is invalid input.
- Nothing here addresses lower reserve, an official deployed row, or either
  official RS-MCA question.

## 6. Consumer ceiling

The packet may replace only two algebraic duplications: a C3b global-root
decoration containing position `1` reduces to its root-free partner, and a
top-support class-sum sign obligation reduces to the corresponding class
omitting `B-1`.  It does not prove any remaining `T_pi(K)>0`, does not upgrade
P11, and does not restore C3.

Full C3 restoration still requires the named P7 coupled-curve continuum
enclosure, together with the outstanding P9 base and P12 endpoint/share
enclosures recorded in the repaired class-charge note.  None is supplied or
weakened here.

## 7. Reproduction

```bash
python3 experimental/scripts/verify_dense_shell_general_k_root_anchor.py
python3 -O experimental/scripts/verify_dense_shell_general_k_root_anchor.py
python3 experimental/scripts/verify_dense_shell_general_k_root_anchor.py --tamper-selftest

cd experimental/lean/dense_shell_general_k_root_anchor
lake build
```

Expected status: `RESULT: PASS`.  The verifier reports exact rational
equalities only; it does not turn a finite enumeration into the proof.  The
tamper self-test separately mutates the root factor, empty base class, invalid
top-containing input, minimal-depth split, Fourier sign, `B=4` singleton
pairing, repaired charge correction, and source binding (`8/8` expected).
