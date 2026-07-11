# Smooth two-fold orientation prefixes retain exponential slope capacity

- **Status:** PROVED-SPECIAL / COUNTEREXAMPLE_NEW_FLOOR / ROUTE CUT.
- **Track:** asymptotic hard input A / unsaturated full-agreement projection.
- **Verifier:**
  `python3 experimental/scripts/verify_full_agreement_orientation_saturation.py`.
- **Promotion gate:** experimental only.  No statement in this packet is
  promoted to the frontiers TeX.

## Exact theorem

For every integer `r>=2`, put

```text
q=3^r,             B=F_q,
n=q-1=2a,          a=(q-1)/2,
w=2 floor(a/(2r)), k=a-w-1,
d=ceil(4a/r),      F=F_(q^d),
D=B^x.
```

Use the complete two-fold map

```text
phi:D -> phi(D),    phi(x)=x^2.
```

For an `a`-set `S subset D`, write

```text
Q_S(X)=X^a+c_1(S)X^(a-1)+...+c_a(S),
Phi_w(S)=(c_1(S),...,c_w(S)).
```

Let

```text
O_r={S subset D : |S intersect {x,-x}|=1 for every phi-fiber {x,-x}}.
```

There is a prefix `z in B^w` and one received line for `RS_F(D,k)`
such that, with

```text
G_z=O_r intersect Phi_w^(-1)(z),       J_z=|G_z|,
```

the following statements hold:

1. every `S in G_z` gives one distinct MCA-bad slope;
2. its witness support and full agreement set are both exactly `S`;
3. these are exactly the witnesses in the canonical joint cell with
   support/agreement profile
   `lambda=(t,m,p,rho)=(0,0,a,a)`; and
4. every ordering of #620's canonical partitioning joint cells retains all
   `J_z` slopes in that cell.

The exact lower floor is

```text
J_z >= ceil(2^a/q^(w/2)),
(log J_z)/n >= log(2)/2-log(3)/4
              = (1/4)log(4/3) > 0.                        (A)
```

Moreover

```text
w/(n/log|B|) -> log(3)/2,       k/n -> 1/2,       a/n=1/2.
```

Thus positive prefix depth at a fixed positive fraction of the critical
`n/log|B|` scale does not force a subexponential actual-slope projection on
this canonical unsaturated orientation cell.

For every `0<=u<=a-2`, there are a prefix `z_u in B^u` and a received
line over the same `F` for `RS_F(D,k_u)`, where `k_u=a-u-1`, whose
canonical `(lambda,lambda)` orientation joint cell contains at least

```text
ceil(2^a/q^ceil(u/2))
```

distinct exact-agreement slopes.  At `u=0` the complete prefix fiber has
`M=binom(2a,a)` distinct slopes, while that canonical orientation joint-cell
count is exactly `2^a`:

```text
H_phi(0,0,a,a)=[z^a](2z)^a=2^a.
```

More generally, for any sequence `u=u_r` with `u log q=o(n)`, the same
bound gives

```text
(log J_(r,u))/n
 >= log(2)/2-ceil(u/2)log(q)/n
 = log(2)/2-o(1).                                          (B)
```

Thus subcritical positive depth alone also fails to collapse the orientation
cell: it nearly attains the zero-depth exponent.  Equation (A) is stronger in
the other direction, showing a positive floor even at a fixed fraction of the
critical `n/log|B|` scale.

## 1. The row is a polynomial-base-field smooth family

The group `D=B^x` is cyclic of order `q-1=2a`.  Because the characteristic is
odd, the kernel of `x -> x^2` on `D` is `{1,-1}`.  Thus `phi` has `N=a`
complete fibers, all of size `c=2`; in the notation of the occupancy atlas,
`D_0=D`, `X` is empty, and `b=0`.  This is the multiplicative coset with
`theta=1` and `H=B^x`, so it is smooth at the retained scale `c=2` in the
sense of `def:structured-folding`.

The base field is not hiddenly exponential relative to the evaluation row:

```text
|B|=q=n+1,          log|B|=O(log n).
```

The scalar extension is exponential but still has linear logarithmic size.
Indeed, from `d=ceil(4a/r)`,

```text
4a <= rd < 4a+r,
2n log(3) <= log|F| < (2n+r)log(3)=Theta(n).
```

The chosen prefix depth is positive and critical-scale, while the code rate
still tends to `1/2`:

```text
0<w<=a-2,     w=Theta(n/log n),
k/n=(a-w-1)/(2a) -> 1/2,      a/n=1/2.
```

## 2. The separating-pole hypothesis is supplied explicitly

For a prefix `z`, write

```text
F_z=Phi_w^(-1)(z),       L_z=|F_z|,
M=binom(2a,a).
```

The exact list--line theorem requires the complete-fiber gate

```text
|F| > n+k binom(L_z,2).                                  (1)
```

It is not enough to separate only the retained orientation supports.  Here
`L_z<=M`, `k<=a-1`, `M<4^a`, and hence the stronger uniform bound is

```text
n+k binom(L_z,2)
 <= n+(a-1)binom(M,2)
 < 2a + ((a-1)/2)16^a
 =: G_a.                                                   (2)
```

The elementary bound `G_a<3^(4a)` holds for all `a>=4`.  At the first value,

```text
G_4=98,312 < 3^16=43,046,721.
```

Moreover `G_(a+1)<81 G_a`: after subtraction, both terms

```text
160a-2,       ((65a-81)/2)16^a
```

are positive.  Induction proves the bound.  Finally

```text
|F|=3^(rd) >= 3^(4a) > G_a.
```

Thus (1) holds for the complete prefix fiber `F_z`.  It guarantees a pole
`alpha in F\D` separating every `P_S` in the exact list, including all
nonorientation supports.  No collision with an unretained witness is hidden.

## 3. Orientation prefixes have only half the ambient dimension

For `S in O_r`, the set `-S` is exactly `D\S`.  Its locator satisfies

```text
Q_(-S)(X)=(-1)^a Q_S(-X),
Q_S(X)Q_(-S)(X)=X^(2a)-1.
```

Define the reversed locator

```text
C_S(T)=T^a Q_S(T^(-1))
      =1+c_1(S)T+...+c_a(S)T^a.
```

The two identities above give the exact spectral-factor relation

```text
C_S(T)C_S(-T)=1-T^(2a).                                  (3)
```

For `2j<=u<=a-2`, the coefficient of `T^(2j)` in (3) is

```text
2c_(2j)+sum_(i=1)^(2j-1)(-1)^i c_i c_(2j-i)=0.           (4)
```

Characteristic three makes `2` invertible.  Equation (4) recursively
determines every even prefix coefficient from earlier coefficients.  Projection
to the odd slots is therefore injective on the realized orientation-prefix
image; it is not asserted that all odd-slot values occur.  Consequently

```text
|Phi_u(O_r)| <= q^ceil(u/2).                              (5)
```

Pigeonholing the `|O_r|=2^a` orientations over that realized image gives
some printed prefix `z in B^u` with

```text
J_(r,u):=|O_r intersect Phi_u^(-1)(z)|
          >= ceil(2^a/q^ceil(u/2)).                       (6)
```

Now take `u=w=2 floor(a/(2r))`.  The elementary inequality
`a=(3^r-1)/2>=2r` holds for every `r>=2` by induction from equality at
`r=2`.  Thus `w` is positive and
`w<=a/r<=a/2<=a-2`.  It is even, so

```text
q^(w/2)=3^(r floor(a/(2r))) <= 3^(a/2).
```

Combining this with (6) and `n=2a` proves the finite-row rate floor (A).
It also gives

```text
w/(n/log|B|) -> log(3)/2.
```

The displayed choice `w` has critical-order depth
`Theta(n/log|B|)`.  The general `u` corollary in the theorem statement
separately covers the subcritical condition `u log|B|=o(n)`.

The general complement-prefix identity is already used in
AllenGrahamHart PR #74 and in the Claude Opus 4.8 divisor-locator note
`experimental/notes/l1/l1_prefix_divisor_count.md`.  The contribution here
is its antipodal-orientation specialization (3), the half-dimensional prefix
image (5), and the MCA slope consequence below.

This restricted identity does not contradict integrated PR #545's Gap-2
classification of universal F_p-linear relations among full-slice power-sum
coordinates.  Equations (3)--(5) are locator relations that hold only after
restricting to the antipodal orientation class `O_r`; such a restriction can
legitimately add relations.

The resulting `q^(w/2)` image cap is a candidate effective-image-collapse
trigger in the C7 geography of open PRs #625 and #627.  This packet proves
neither that trigger's projection-degree payment nor survival past the
pre-primitive router.  Open PR #626 rules out direct profile enumeration as a
general C7 payment mechanism on its product/profile class.  Thus the present
floor is not asserted on a post-C7 primitive residual.

## 4. A complete prefix ray realizes the exponential cell

Fix a prefix `z` supplied by Section 3 and set

```text
U_z(X)=X^a+sum_(i=1)^w z_i X^(a-i).
```

For every `S in F_z=Phi_w^(-1)(z)`, put

```text
P_S(X)=U_z(X)-Q_S(X).
```

The leading term and first `w` coefficients cancel, so
`deg(P_S)<=a-w-1=k`, and `P_S` agrees with `U_z` exactly on `S`.
Conversely, if `deg(P)<=k` and `P` agrees with `U_z` on at least `a`
points, then the monic degree-`a` polynomial `U_z-P` is the locator of one
unique `a`-set and coefficient comparison puts that set in `F_z`.  Hence

```text
L_a(U_z)={P_S:S in F_z},       |L_a(U_z)|=L_z.             (7)
```

Choose the pole `alpha` supplied by Section 2 and define

```text
r_0(x)=U_z(x)/(x-alpha),
r_1(x)=-1/(x-alpha).
```

The exact list--line bijection (`thm:exact-list-line-bijection`) and
`cor:exact-prefix-ray-realization` give bijections

```text
S |-> gamma_S=P_S(alpha)=U_z(alpha)-Q_S(alpha)
  |-> (gamma_S,S,h_S),

h_S(X)=(P_S(X)-P_S(alpha))/(X-alpha)                       (8)
```

from the complete prefix fiber to the bad slopes and the entire
exact-agreement-`a` witness incidence.  In particular, the slopes are
pairwise distinct, `deg(h_S)<k`, and each full agreement set is exactly
`S`.  The support is noncommon: an explanation of `r_1` on `k+1` of its
`a>=k+1` points would make `(X-alpha)G+1` a degree-at-most-`k`
polynomial with `k+1` roots but value one at `alpha`.

Every `S in O_r` has occupancy profile

```text
lambda_phi(S)=(0,0,a,a),
```

and conversely every `a`-set with this profile is in `O_r`.  Its full
agreement profile is identical.  The canonical occupancy formula gives

```text
H_phi(0,0,a,a)
 = binom(0,0)binom(a,a)binom(0,0)
   [z^a]((1+z)^2-1-z^2)^a
 = [z^a](2z)^a
 = 2^a.                                                    (9)
```

Therefore the canonical joint `(lambda,lambda)` cell for this fixed received
line contains exactly the `J_z` witnesses in `G_z` and exactly `J_z`
distinct slopes.  No other canonical joint profile contains any of those
slopes, because (8) makes the exact witness unique.  Every ordering among
#620's partitioning joint cells therefore has

```text
|Z_(lambda,lambda)^o|=J_z
 >=ceil(2^a/q^(w/2))
 >=exp((log(4/3)/4)n).                                    (10)
```

The unsaturated density is `p/n=1/2`.  Equation (10) rules out a
subexponential budget at the orientation-deleted scale.  It does not contradict
payment at the realized image-normalized scale.  At depth zero, `G_z=O_r`
and (9)--(10) specialize to exact capacity saturation `J_z=H_phi=2^a`.

The exact adjacent-row and pole-line package was added by maintainer
`przchojecki` in commit `4e3c4ee`.  This packet adds the smooth antipodal
prefix compression, its field gate, and the canonical-cell consequence.

## Hypothesis audit

| Consumed statement | Printed hypothesis | Supplied here |
|---|---|---|
| `def:structured-folding` | multiplicative coset and a retained divisor `c` | `D=B^x`, `c=2`, `phi=x^2` |
| canonical occupancy atlas | `D=D_0 disjoint_union X`, common fiber size `c>=2` | `D_0=D`, `X=empty`, `b=0`, `N=a`, `c=2` |
| joint atlas | exact support size `a>=k+1` and noncommon support | `a=k+w+1`; `r_1` is not explainable on `k+1` points |
| exact list--line bijection | `D subset B subset F`, `1<=k<n`, agreement `m>=k+1` | `m=a>=k+1`, `a>=4`, and the displayed field tower |
| separating pole | injective evaluation on the complete list | the strict gate (1) separates every member of `F_z` |
| prefix-ray corollary | `0<=w<=m-2`, `k=m-w-1`, complete prefix fiber | the chosen positive `w<=a-2`, `k=a-w-1`, and complete `F_z` |
| first-match projection | an ordered witness-exhaustive atlas | the canonical joint atlas is exhaustive; uniqueness gives order-independence within that partition |
| challenge restriction | retained slopes lie in `Gamma` | take the full-field challenge `Gamma=F` |
| asymptotic smooth row | fixed `c`, `b=o(n)`, positive-density partial fibers | `c=2`, `b=0`, `p/n=1/2` |

Three stronger conditions are deliberately **not** supplied: a `B`-valued
received line, bounded scalar-extension degree, or survival after an earlier
overlapping algebraic/effective-image atlas.  Linear depth is a legal
specialization of the general-`u` construction, but bound (6) is then vacuous
and no linear-depth collapse theorem is refuted.  Any repair using one of the
three absent conditions must state it.

The prefix `z` is fixed in the construction of the received line; #620's
unrefined occupancy cell does not use it as a profile parameter.  If a refined
atlas records `z`, it must print that realized parameter, and no
subexponential census of such parameters is proved here.

The separating pole line necessarily lives over `F`.
`thm:subfield-confinement-full` would cap a `B`-valued line by
`|B|=n+1` slopes.  At the sole base-field pole `alpha=0`, the same chosen
orientation prefix projects to at most two product-parity slopes; at depth
zero the full orientation family gives exactly two.  Extension-field
separation is visibly load-bearing.

## Ledger effect and the new frontier

PR #620 by DannyExperiments proved the canonical full-agreement occupancy
atlas and named the remaining unsaturated orientation-collapse wall.  This
packet answers the support/agreement-profile-only and positive-depth-only
versions negatively, including positive subcritical depth.  On a full
multiplicative domain with polynomial-size base field, fixed smooth fiber
size, exact full agreement, and a linear-log scalar field, the canonical
orientation cell has slope rate `log(2)/2-o(1)` whenever
`u log|B|=o(n)`.  At the highlighted critical-order depth it still has the
explicit positive rate `log(4/3)/4`.

The mechanism also identifies the missing hypothesis.  At general depth `u`,
the realized orientation-prefix image has size at most `q^ceil(u/2)`, not the
ambient `q^u`; `q^(w/2)` is the highlighted even-`w` case.  Thus an
ambient-prefix orientation payment cannot divide by `q^u` without full-image
information.  A correct image-normalized payment, or an earlier
spectral/effective-image cell that routes this locus, is not contradicted.
This is a sharpness/route-cut theorem for #620, not a defect in its compiler.

DannyExperiments PR #621, integrated as the aperiodic one-ray packet, gives
the opposite projection extreme: exponentially many exact supports can
collapse to one pole slope over the base field.  Here a separating scalar
extension realizes an exponential prefix fiber as distinct slopes.  Taken
together, the packets show that none of support entropy, aperiodicity,
smooth-domain membership, exact agreement, or positive prefix depth alone
determines slope projection; no conjunction of all five is asserted here.
Realized prefix image and pole separation are load-bearing.

The highest-value remaining versions are therefore:

1. route or pay the antipodal spectral-factor locus by an earlier effective-
   image cell, with witness-exhaustive first-match overlap proved;
2. prove a bound under a stated restriction on scalar extension or on the
   field of definition of the received line; or
3. decide the linear-depth regime `u=Theta(n)`, where the prefix-image bound
   (5) by itself becomes vacuous.

## Nonclaims

- No global hard-input-A or profile-envelope closure is claimed.
- No counterexample to the canonical occupancy or weighted-cover theorem is
  claimed; its capacity is exactly attained only in the depth-zero corollary.
- No correctly image-normalized payment at the realized prefix image is
  refuted.
- No result for an arbitrary overlapping atlas, a post-algebraic primitive
  residual, or a ledger-admissible row is claimed.
- No theorem under a base-valued received line, bounded extension degree, or
  linear prefix depth `u=Theta(n)` is refuted.
- No subexponential census of prefix parameters `z` is claimed.
- No finite M31 or KoalaBear survivor count changes.
- No deployed adjacent inequality or target threshold changes.
- No C9/Sidon, SE, PTE, or Lean result is claimed.
- No paper TeX is changed.
