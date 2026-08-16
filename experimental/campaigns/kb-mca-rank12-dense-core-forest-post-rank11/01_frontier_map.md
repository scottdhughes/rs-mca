# Frontier map

## Exact parent

Affine-error-rank-eleven global-core payment:
`d01c546f4dca70e256c18c142873821b3bb48ab5`.

## Imported interface

For every shortened row

\[
(n_K,K,m_K)=(R+K,K,d+K),
\qquad
R=1,048,576,\quad d=67,472,
\]

and every selected post-near family of explanation-direction dimension at
most \(s\), the parent stack supplies:

- one frozen minimizing pair and complete pair core per slope;
- \(|H_\gamma|\ge d+K-\theta_\gamma\);
- \(\sum_\gamma\theta_\gamma\le C_s(K)\);
- a heavy-coordinate dichotomy: proper pair-difference span gives a
  source-bound rank drop, while full span makes that coordinate global for
  the whole family and permits complete-agreement shortening.

## New coupled sparse cap

For pair type \(e\), define

\[
\delta_e=\max\{1,m_K-|H_e|\}.
\]

One type of deficiency \(\delta\) owns at most

\[
c_\delta=\left\lfloor\frac{R-d+\delta}{\delta}\right\rfloor
\]

slopes, and every owned slope costs at least \(\delta\) units of the global
margin resource.

The number of types with deficiency at most \(t\) is bounded by the minimum
of:

1. the ordinary affine-pair list cap, under its exact sextic-field guard;
2. a Cauchy--Plotkin bound for cores of size at least \(m_K-t\) with
   pairwise intersection at most \(K-1\).

The monotone closure of these prefix caps and an increasing-cost greedy fill
give the exact selected-cell ceilings.

## Dynamic forest compiler

For a target \(T\), let \(E_s(K;T)\) be the largest load which can evade both
the selected sparse caps and production of a rank-at-most-two descendant of
load at least \(T\).

The base is \(E_2(K;T)=T-1\). If

\[
P_s(K,M)=
\left\lfloor
\frac{M(R+K)+C_s(K)}{d+K}
\right\rfloor,
\]

then

\[
E_s(s;T)=\min\{U_s(s),P_s(s,E_{s-1}(s-1;T))\},
\]

and, for \(K>s\),

\[
E_s(K;T)=
\min\left\{
U_s(K),
\max\left(E_s(K-1;T),
P_s(K,E_{s-1}(K-1;T))\right)
\right\}.
\]

Here \(U_s(K)=+\infty\) except at the nine declared sparse-cap cells.
The maximum is essential: the actual configuration may choose either the
whole-family or proper-span branch.

At \(T=9,342,183\),

```text
E_11(1,048,576;T) = 274,980,718,357,491,817
initial load       = 274,980,728,111,260,144
forcing gap        =           9,753,768,327
```

At \(T+1\), the evasion threshold exceeds the initial load by
`20,216,453,405`.

## Exact remaining joint

The next theorem must pay or synchronize the source-bound rank-two forest.
A one-path descent, another local margin threshold, or an independent sum of
fixed-pair stars cannot do this.
