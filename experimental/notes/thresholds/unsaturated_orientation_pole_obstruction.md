# Unsaturated orientation survives a separating pole before atlas routing

- **Status:** PROVED PRE-ATLAS ROUTE CUT.
- **Track:** asymptotic hard input A / unsaturated proper-fiber orientation.
- **Verifier:**
  `python3 experimental/scripts/verify_unsaturated_orientation_pole_obstruction.py`.
- **Paper scope:** no stable paper TeX is changed.

## Hostile-audit verdict

The theorem below is proved, but it is not a primitive counterexample.  It
combines the exact partial-occupancy count with the actual locator-prefix pole
bijection and shows that a fixed unsaturated occupancy slice can realize its
local orientation coefficient as distinct finite RS--MCA slopes.

The construction is pre-atlas.  Its superscript `o` refers only to first
matching in the canonical joint support/full-agreement occupancy atlas.  The
argument does not classify the witnesses through the earlier algebraic cells
C1--C8 and therefore does not prove that any displayed slope survives in the
primitive residual of `def:primitive-first-match-residual`.

The correct publication label is consequently **PROVED PRE-ATLAS ROUTE CUT**,
not `COUNTEREXAMPLE` and not a primitive obstruction.

## Setup

Let `B` be a finite field and let `D subset B` have size `n`.  Suppose

```text
D = D_0 disjoint_union X,   |X|=b,
phi : D_0 -> Q,             |Q|=N,
```

and every `phi`-fiber has the same size `c>=2`.  For an `a`-set `S subset D`,
write

```text
lambda_phi(S)=(t,m,p,rho),
```

where `t` is the number of selected exceptional points, `m` is the number of
complete fibers, `p` is the number of nonempty proper fibers, and `rho` is the
number of selected points in those proper fibers.  For a feasible label
`lambda=(t,m,p,rho)`, put

```text
Omega_lambda={S in binom(D,a): lambda_phi(S)=lambda},

H_phi(lambda)
 = binom(b,t) binom(N,p) binom(N-p,m)
   [u^rho] ((1+u)^c-1-u^c)^p.
```

Thus `|Omega_lambda|=H_phi(lambda)` by
`thm:exact-partial-occupancy`.

For every `a`-set, let

```text
Q_S(X)=prod_(x in S)(X-x)
       =X^a+c_1(S)X^(a-1)+...+c_a(S),

Phi_w(S)=(c_1(S),...,c_w(S)).
```

The prefix coordinates are the actual elementary locator coefficients; no
power-sum or characteristic-dependent Newton substitution is used.

## Theorem

**Profilewise separating-pole realization.**  Fix `2<=a<=n`, a nonempty
occupancy slice `Omega_lambda`, and `0<=w<=a-2`.  Put

```text
k=a-w-1.
```

There exist

```text
z in B^w,
a finite extension F/B,
alpha in F\D,
and a received line r=(r_0,r_1) for C=RS_F(D,k)
```

such that, for the full-field challenge and the canonical joint
support/full-agreement occupancy atlas,

```text
|Z^o_(lambda,lambda)(r)|
 = |Omega_lambda intersect Phi_w^(-1)(z)|
 >= ceil(H_phi(lambda)/|B|^w).                         (1)
```

Every slope counted in (1) has one exact-`a` witness, and the witness's full
agreement set equals its support.  In fact the complete prefix fiber, the
complete exact-witness incidence of the line, and its finite bad-slope set are
in bijection.

At `w=0`, the prefix has one value and hence

```text
|Z^o_(lambda,lambda)(r)|=H_phi(lambda).                (2)
```

For `w>0`, equality is asserted with the selected profile intersection in
(1), not with all of `H_phi(lambda)`.

## Proof

### 1. Pigeonhole one actual locator prefix

The restriction

```text
Phi_w : Omega_lambda -> B^w
```

has at most `|B|^w` values.  Choose `z` maximizing its fiber.  Then

```text
M_z:=|Omega_lambda intersect Phi_w^(-1)(z)|
    >= ceil(H_phi(lambda)/|B|^w).                      (3)
```

Let

```text
P_z=Phi_w^(-1)(z),   L_z=|P_z|,
```

where `P_z` is the complete prefix fiber among all `a`-subsets, not only its
intersection with `Omega_lambda`.

### 2. Choose a pole separating the complete prefix fiber

If `S!=T` belong to `P_z`, then `Q_S-Q_T` is a nonzero polynomial and the
common prefix gives

```text
deg(Q_S-Q_T)<=a-w-1=k.                                (4)
```

Choose a finite extension `F/B` with

```text
|F|>n+k binom(L_z,2).                                 (5)
```

The union of `D` and the roots in `F` of all differences `Q_S-Q_T` has
strictly fewer than `|F|` elements.  Hence some `alpha in F\D` satisfies

```text
Q_S(alpha)!=Q_T(alpha)  for all distinct S,T in P_z. (6)
```

### 3. Construct the actual pole line

Set

```text
U_z(X)=X^a+sum_(i=1)^w z_i X^(a-i),
P_S(X)=U_z(X)-Q_S(X).
```

For `S in P_z`, the common leading prefix gives `deg P_S<=k`.  On `D`, define

```text
r_0(x)= U_z(x)/(x-alpha),
r_1(x)=-1/(x-alpha),

gamma_S=P_S(alpha),
h_S(X)=(P_S(X)-P_S(alpha))/(X-alpha).
```

The numerator defining `h_S` vanishes at `alpha`, and

```text
deg h_S<k.
```

For every `x in D`, direct subtraction gives

```text
r_0(x)+gamma_S r_1(x)-h_S(x)=Q_S(x)/(x-alpha).        (7)
```

The right side vanishes exactly on `S`, so the full agreement set is exactly
`S`.

The line is support-wise nontrivial there.  If a polynomial `G` of degree
less than `k` explained `r_1` on `S`, then

```text
(X-alpha)G(X)+1
```

would have the `a` distinct roots in `S`, degree at most `k<a`, and value one
at `alpha`, a contradiction.

### 4. Prove the converse and the bijection

Let `(gamma,T,h)` be any exact-`a` witness of this line and put

```text
P(X)=(X-alpha)h(X)+gamma.
```

Then `deg P<=k`, and on every point of `T` the witness equation implies
`P=U_z`.  The monic degree-`a` polynomial `U_z-P` has the `a` distinct roots
in `T`; therefore

```text
U_z-P=Q_T.
```

Since `deg P<=a-w-1`, coefficient comparison gives `Phi_w(T)=z`.  Thus every
exact witness comes from one member of `P_z`.  Evaluating at `alpha` recovers
`gamma=P_T(alpha)`, and division by `X-alpha` recovers `h_T`.

Finally, (6) makes

```text
S -> gamma_S=U_z(alpha)-Q_S(alpha)                    (8)
```

injective.  Hence support, exact witness, and finite slope are in bijection on
the complete prefix fiber.

### 5. Restrict to one diagonal occupancy cell

Equation (7) gives `A((gamma_S,S,h_S))=S`, so a support of profile `lambda`
gives a witness in the diagonal joint cell `(lambda,lambda)`.  The complete
bijection shows that each slope occurs in exactly one joint cell.  No other
joint cell can first-match-delete it, independently of the order of the
canonical joint cells.  Consequently

```text
|Z^o_(lambda,lambda)(r)|
 = |Omega_lambda intersect P_z|=M_z,
```

which proves (1).  At `w=0`, `P_z=binom(D,a)`, proving (2).

## Smooth multiplicative specialization

Fix `c>=2` and `eta in (0,1)`.  Choose a prime `ell` not dividing `c` and a
sequence

```text
q_j=ell^(varphi(c)j),   B_j=F_(q_j),
D_j=B_j^x,              n_j=q_j-1.
```

Euler's theorem gives `c | n_j`.  For

```text
phi_j(x)=x^c
```

on `D_j`, every fiber has size `c`, and the image has

```text
N_j=n_j/c
```

points.  Put, exactly as in the route-cut family,

```text
p_j=floor(eta n_j/c),
a_j=p_j,
w_j=floor(log n_j),
k_j=a_j-w_j-1,
lambda_j=(0,0,p_j,p_j),
```

where `log` is natural.  These parameters satisfy `1<=k_j<n_j` for all large
`j`, `p_j=(eta/c)n_j+O(1)`, and

```text
w_j log|B_j|=O((log n_j)^2)=o(n_j).                  (9)
```

The profile chooses `p_j` fibers and one of their `c` points independently,
so

```text
H_phi_j(lambda_j)=binom(N_j,p_j)c^p_j.               (10)
```

For this profile, deleting the local proper-fiber orientation coefficient
leaves the benchmark

```text
H_phi_j^unoriented(lambda_j)=binom(N_j,p_j).          (11)
```

Applying (1) at depth `w_j` gives

```text
|Z^o_(lambda_j,lambda_j)|
 >= ceil(binom(N_j,p_j)c^p_j/|B_j|^w_j),
```

and therefore

```text
|Z^o_(lambda_j,lambda_j)| / H_phi_j^unoriented(lambda_j)
 >= c^p_j/|B_j|^w_j
  = exp((eta log(c)/c)n_j-o(n_j)).                    (12)
```

At `w=0`, the exact ratio is `c^p_j`.  Thus the proper-fiber orientation
factor is realized by actual slopes before C1--C8 routing, even at growing
shallow depth.  This cuts any route that deletes the coefficient at the raw
joint-occupancy layer.

## Why this is not a primitive counterexample

The frontiers paper routes algebraic loci before declaring a primitive
residual.  This note has not determined the first destination of the pole
family in any of the following cells:

```text
C1  quotient / periodic,
C2  dihedral / Chebyshev,
C3  planted block,
C4  tangent / deep / common line,
C5  extension / field descent,
C6  differential locator,
C7  saturation / effective-image collapse,
C8  balanced core / split pencil.
```

The uniqueness of the witness inside the canonical joint occupancy atlas does
not imply that its slope was absent from an earlier C1--C8 profile.  Therefore
the result does not contradict a theorem stated only on the literal
post-C1--C8 residual.

The theorem also uses the full-field challenge `Gamma=F` (or any challenge set
known to contain the constructed slopes).  For an arbitrary proper challenge
set, only

```text
|Z^o_(lambda,lambda) intersect Gamma|<=|Gamma|
```

is automatic.  No lower bound on that intersection follows from `|Gamma|`
alone.  A challenge cap may therefore pay or erase the displayed lower bound.

## Exact routing wall

For the smooth family, let

```text
G_j=Omega_lambda_j intersect Phi_w_j^(-1)(z_j)
```

be the selected profile-prefix family and let

```text
Theta_j(S)=U_z_j(alpha_j)-Q_S(alpha_j).
```

The theorem proves that `Theta_j` is injective on `G_j`.  Let
`G_j^res subset G_j` be the supports whose unique witnesses remain after the
literal C1--C8 first-match excision.  Before a challenge restriction, the
post-atlas contribution of this family is therefore exactly

```text
|Theta_j(G_j^res)|=|G_j^res|.                         (13)
```

To justify orientation deletion on this family, the next theorem must do one
of the following:

1. classify the first C1--C8 destination of the removed supports and pay all
   of their slopes in the corresponding earlier cell budgets;
2. prove the residual thinning estimate

   ```text
   |G_j^res|<=exp(o(n_j)) binom(N_j,p_j);             (14)
   ```

3. prove that the actual challenge intersection supplies the missing cap.

Because `Theta_j` is injective, a slope-collision claim cannot reduce (13) on
this particular line.  A genuine primitive counterexample would require the
opposite of (14), after the complete C1--C8 classification and for the relevant
challenge set.  This note proves neither direction.  Equation (14), together
with exact earlier-cell add-back, is the routing wall left by the result.

## Ledger effect

- **Hard input A / A2:** no closure.  The result rules out deleting the local
  orientation coefficient before algebraic first-match routing.
- **A7 / profile envelope:** no contradiction.  The exact occupancy term
  `H_phi(lambda)` and the coarser identity support term can pay the family.
- **Primitive ray compiler:** untouched; no post-C1--C8 residual is certified.
- **Challenge ledger:** untouched for proper challenge sets.
- **Finite deployed ledger:** none.  No M31 or KoalaBear survivor count, safe
  row, unsafe row, budget, or adjacent inequality changes.

## Verifier scope

The stdlib-only verifier independently checks:

- exact occupancy-profile counts and full add-back on several uniform-fiber
  systems;
- a proper scalar-extension pole bijection over `F_25/F_5`;
- the depth-zero `F_10009` examples with orientation factors `2^p` for
  `p=2,3,4`;
- the positive-depth `F_109` example with `a=p=3`, `w=1`, `z=0`, four profile
  supports, and four distinct actual slopes;
- the degree bounds, line identity, exact full agreement set,
  support-wise nontriviality, converse prefix criterion, and slope injection.

These finite checks replay the algebra used in the proof; they are not an
asymptotic or post-atlas certificate.

## Nonclaims

- No witness is called primitive.
- No survival through C1--C8 is proved.
- No arbitrary challenge-set lower bound is proved.
- No global orientation-free theorem is refuted on the literal primitive
  residual.
- No linear-depth statement with `w log|B|=Theta(n)` is made.
- No finite deployed threshold changes.
- No full hard-input-A, A7, or lower-reserve closure is claimed.
- No stable paper TeX is edited.
