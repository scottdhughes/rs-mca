# L1 Prefix Fourier Orbit Cancellation

- **Status:** PROVED (orbit identities) / EXPERIMENTAL (finite diagnostics) /
  CONDITIONAL (large-sieve or higher-moment targets) / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-20.
- **Scope:** Paper B `conj:prefix-local` in the monomial-prefix lane. This note
  does not assert the arbitrary-word `conj:arbitrary-local`, Reed--Solomon
  list-decoding safety, MCA, line-decoding, or protocol safety.

## Purpose

`l1_prefix_divisor_count.md` reduces the monomial-prefix fiber to the Fourier
identity

```text
N(c)
=
p^{-sigma} sum_{r in F_p^sigma} psi(-<r,c>) S_m(r),

S_m(r)
=
sum_{A subset H, |A|=m}
psi(sum_{a in A} g_r(a)),

g_r(X)=sum_{j=1}^sigma r_j X^j.
```

It also shows that the structured/generic frequency split is not enough: the
generic frequencies dominate the triangle-inequality `L1` mass, while the actual
fiber deviations are much smaller. The missing ingredient is phase cancellation
across Fourier frequencies.

This note adds the next exact compression: quotient the Fourier side by the
dual dilation action of the domain. The result is an exact orbit-kernel formula.
It is a better location for the required cancellation estimate than individual
frequency bounds.

## 0. Field Scope and Normalization

This note is stated in the split prime-field setting

```text
H <= F_p^*,       n | p-1,
```

using the additive character

```text
psi(x)=exp(2 pi i x / p)
```

and Fourier group `F_p^sigma`. The verifier implements this prime-field model.

The analogous statement over a non-prime field `F_q` should use trace
characters `psi(Tr_{F_q/F_p}(.))` and a Fourier group over the additive group of
`F_q^sigma`. That extension is not claimed here.

## 1. Dual Dilation Invariance

Let `H <= F_p^*` have order `n`, and let `H` act on `F_p^sigma` by

```text
(h * r)_j = h^j r_j,        1 <= j <= sigma.
```

This is the dual action corresponding to the dilation action
`A |-> hA` on divisor roots and the power-sum coordinates

```text
p_j(A)=sum_{a in A} a^j.
```

**Lemma.** For every `h in H`,

```text
S_m(h * r) = S_m(r).
```

**Proof.** We have

```text
sum_{j=1}^sigma (h^j r_j) p_j(A)
=
sum_{j=1}^sigma r_j p_j(hA).
```

As `A` runs over all `m`-subsets of `H`, so does `hA`. Therefore the defining
sum for `S_m(h*r)` is the same as the defining sum for `S_m(r)`. `square`

Thus `S_m` is constant on dual-dilation orbits.

## 2. Exact Orbit Decomposition

For a nonzero frequency `r`, write

```text
O(r) = {h*r : h in H},
```

with duplicates removed, and define the orbit kernel

```text
K_{r,c}
=
sum_{r' in O(r)} psi(-<r',c>)
=
sum_{h in H / Stab(r)}
psi(-sum_{j=1}^sigma r_j c_j h^j).
```

Since `S_m` is constant on `O(r)`, choosing one representative from each orbit
gives the exact identity

```text
N(c) - binom(n,m)/p^sigma
=
p^{-sigma}
sum_{[r] != [0]} S_m(r) K_{r,c}.
```

This is an identity, not an estimate. It preserves all prefix-fiber information
and replaces frequency-by-frequency phases by structured orbit kernels.

The definition is independent of the representative: if `r_1=h_0*r`, then
`O(r_1)=O(r)`, `S_m(r_1)=S_m(r)`, and the displayed sum over orbit members is the
same.

The useful distinction is:

```text
frequency triangle bound:
  p^{-sigma} sum_{r != 0} |S_m(r)|

orbit triangle bound:
  p^{-sigma} sum_{[r] != [0]} |S_m(r)| |K_{r,c}|.
```

The second bound can be much sharper, but it still need not match the actual
cancellation in the signed orbit sum.

## 3. Kernel Degeneracies

For fixed `(r,c)`, put

```text
phi_{r,c}(h)=sum_{j=1}^sigma r_j c_j h^j.
```

Then `K_{r,c}` is the additive character sum of `-phi_{r,c}` over the orbit
`H/Stab(r)`.

The completely degenerate case is

```text
r_j c_j = 0       for every 1 <= j <= sigma,
```

in which case `phi_{r,c}=0` and

```text
K_{r,c}=|O(r)|.
```

More generally, the phase is degenerate when the values of `phi_{r,c}` on
`H/Stab(r)` occupy a proper subset of the orbit size. These degeneracies are
visible in finite checks by evaluating the phase on the orbit.

The important ledger point is that many large kernels arise from sparse or
symmetric prefix coordinates and structured frequency support. Those are exactly
the slices already singled out by the quotient/folding theory of
`l1_prefix_divisor_count.md`.

This does not prove the local limit. It identifies which orbit kernels should be
charged to known quotient/folding structure and which kernels belong to the
remaining generic cancellation problem.

There is also an immediate algebraic route cut that survives even in the
quotient-free prefix slice.

**Lemma (orthogonal-support saturation).** Let

```text
supp(r)={j : r_j != 0},        supp(c)={j : c_j != 0}.
```

If

```text
supp(r) and supp(c) are disjoint,
```

then

```text
K_{r,c}=|O(r)|.
```

**Proof.** For every `h in H`,

```text
<h*r,c> = sum_{j=1}^sigma h^j r_j c_j = 0,
```

because each product `r_j c_j` is zero. Every summand in the orbit kernel is
therefore `psi(0)=1`. `square`

Taking `c=0` gives the immediate corollary

```text
K_{r,0}=|O(r)|
```

for every nonzero orbit. More importantly, saturation can occur with
`c_1 != 0`. For example, at `sigma=2`,

```text
c=(1,0),        r=(0,1)
```

has `g_c=1`, so the existing prefix theory classifies the fiber as quotient-free
and purely aperiodic, but the orbit phase is still constant.

Therefore no uniform pointwise kernel saving of the form
`|K_{r,c}| << |O(r)|` can hold, even after restricting to the quotient-free
prefix class `g_c=1` or the convenient sufficient slice `c_1 != 0`. Any
successful theorem must use averaging, higher moments, correlation with
`S_m(r)`, cancellation across different frequency orbits, or a finer joint
nondegeneracy condition on `(r,c)`. The verifier reports diagnostics both over
all prefixes and over the generic prefix slice `c_1 != 0`.

## 4. Orthogonality and the Second-Moment Barrier

The orbit kernels are mutually orthogonal as functions of `c`:

```text
sum_{c in F_p^sigma} K_{r,c} conjugate(K_{s,c})
=
0       if O(r) != O(s),
```

and

```text
sum_{c in F_p^sigma} |K_{r,c}|^2
=
p^sigma |O(r)|.
```

Consequently,

```text
sum_c |N(c)-binom(n,m)/p^sigma|^2
=
p^{-sigma}
sum_{[r] != [0]} |S_m(r)|^2 |O(r)|.
```

This is the exact second moment in orbit form. It is useful, but it is still an
average over `c`; it does not by itself give a uniform worst-case bound. The
remaining problem is a worst-case orbit-kernel cancellation estimate.

## 5. Sufficient Analytic Targets

The prefix local-limit target would follow from any one of the following
uniform estimates after the quotient/folding slices are separately budgeted.

### Orbit Large-Sieve Target

For the relevant nondegenerate orbit set `Omega`, prove a bound

```text
sup_c |sum_{O in Omega} a_O K_{O,c}|^2
<=
LS(n,p,sigma) sum_{O in Omega} |a_O|^2 |O|
```

with `a_O=S_m(O)` and with `LS` small enough that

```text
p^{-sigma} sqrt(LS sum_O |S_m(O)|^2 |O|) <= n^B.
```

This is a true worst-case substitute for the second moment.

### Higher-Moment Target

For some fixed or slowly growing `L`, prove

```text
sum_c |N(c)-binom(n,m)/p^sigma|^{2L}
```

is small enough that the trivial passage from moment to maximum still gives
`n^B`. This is the Fourier version of controlling high-order collision
certificates rather than only pairwise intersections.

### Direct Orbit-Correlation Target

Prove cancellation in

```text
sum_{[r] != [0]} S_m(r) K_{r,c}
```

by exploiting correlation between the coefficient phase of `S_m(r)` and the
orbit kernel `K_{r,c}`. This is stronger than bounding `|S_m(r)|` and
`|K_{r,c}|` separately, and finite data show that separate absolute-value
bounds remain too large.

All three targets are CONJECTURAL here.

## 6. Exponent Ledger

Work in the generated-field split case `q=p=n^A` and the intended reserve scale

```text
sigma = C n / log n.
```

The main term has exponent

```text
log binom(n,m) - sigma log q
~= n H(m/n) - AC n.
```

Thus the entropy reserve requires `AC > H(m/n)` up to slack. Once that is paid,
the main term is polynomially small or better.

The nonzero Fourier sum still has `q^sigma = exp(AC n)` frequencies. A bound on
individual generic subgroup sums is insufficient because the number of generic
frequencies is exponentially large in `n`. The necessary saving is therefore not
only a Weil saving inside `S_m(r)`; it must also include cancellation across the
dual frequency orbits.

In orbit language, the target is

```text
|sum_{[r] != [0]} S_m(r) K_{r,c}|
<=
q^sigma n^B
```

uniformly in `c`, after removing quotient/folding terms. The left side is a
signed orbit sum over roughly `q^sigma/n` generic orbits. Any proof that only
gives

```text
sum_{[r]} |S_m(r)| |K_{r,c}|
```

at the generic Weil scale still has to beat this exponential orbit count. The
finite verifier reports both the raw frequency triangle bound and the
orbit-compressed triangle bound. In the checked tiny cases, the orbit-compressed
triangle bound is still too large to prove the desired estimate by itself.

## 7. Boundary with the Arbitrary-Word Lane

This note concerns the monomial-prefix fiber `Phi_sigma^{-1}(c)` and
`conj:prefix-local`. It does not prove the arbitrary-word robustly aperiodic
determinantal-shell or RIM-certificate counting statements.

The arbitrary-word notes

```text
l1_repaired_locator_theorem_package.md
l1_syndrome_catalecticant_shells.md
l1_determinantal_support_criterion.md
l1_periodic_support_multisequence_reduction.md
l1_quotient_defect_closure.md
```

define a separate syndrome/determinantal shell problem. A future theorem may
bridge prefix Fourier cancellation to part of that problem, but such a bridge is
not asserted here.

## 8. Verifier

`experimental/scripts/verify_l1_fourier_orbit_cancellation.py` checks, on tiny
split prime-field cases:

- exact Fourier reconstruction after orbit compression;
- invariance of `S_m(r)` on dual dilation orbits;
- exact orbit-kernel values;
- kernel orthogonality and the orbit second-moment identity;
- phase-degeneracy classification by direct evaluation;
- comparison of raw `L1`, orbit-triangle, and actual signed deviations.
- deterministic orthogonal-support saturation at `sigma=2`, with
  `c=(1,0)` and `r=(0,1)`, showing that full kernel saturation can occur inside
  the quotient-free `c_1 != 0` prefix slice;
- a proper-subgroup regression at `p=17,n=8,sigma=2`, where the `17^2`
  frequencies decompose into `34` orbits of size `8`, `4` orbits of size `4`,
  and `1` zero orbit of size `1`;
- a targeted `p=17,n=8,sigma=4` stabilizer check where
  `r=(0,0,0,1)` has stabilizer size `4` and orbit size `2`.

The script is finite experimental evidence plus identity verification. It does
not prove the asymptotic cancellation estimate.
