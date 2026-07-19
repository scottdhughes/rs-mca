# Rank-16 fixed-26 Bezout rectangle conductor

**Status:** proved conditional finite local theorem. This note records only the
layer accepted by the independent R31 hostile proof audit. It makes no finite
ledger, parent, recurrence, asymptotic, or official-score payment.

## Literal source cell

Work over

```text
F = F_2130706433,  R = F[X],  K = F(X),
n = 2097152,       B = 32768, T = X^B,
a = 67472,         r = 63601, d = 28897,
L3 = 2r-a = 59730.
```

Fix one literal deployed fixed-26 source cell: one received word and its
actual canonical first-match owner, one monic degree-`a` polynomial `g` with
`gcd(g,X^n-1)=1`, one fixed nonzero representative `xi` of the source residue
ray, one fixed 26-label core, and disjoint four-label sets

```text
A = {a1,a2,a3,a4},  C = {b1,b2,b3,b4}.
```

All sixteen cross-pairs are actual source-valid fixed-26 edges, retaining
exact degree, monicity, squarefreeness, complete `H`-splitting, fibre
avoidance, residual footprint, nonpairing, prior-owner exclusion, and the
actual canonical first-match condition.

For every label `y` in `A union C`, put

```text
F_y = T-y,             F_y V_y = xi + g S_y,
U_yz = (V_y-V_z)/(y-z),
Q_yz = (S_y-S_z)/(y-z).
```

The rank matrix is the common-source matrix `(U_ab)`, not the matrix of
independently monic-normalized locators. Assume all its `3 x 3` minors vanish.
The inherited nonzero `2 x 2` cross-minor theorem then gives rank exactly two.

Let `N0,D0 in R[Z]` be the inherited cofactor pair. Let `c in R` be their
monic joint coefficient content and write

```text
N = N0/c,  D = D0/c.
```

The inherited interface gives coefficient primitivity over `R`, coprimality
over `K[Z]`, `max(deg_Z N,deg_Z D)=2`, and

```text
N(X,y) = V_y(X) D(X,y),  D(X,y) != 0
```

at all eight labels. Write

```text
N = n0+n1 Z+n2 Z^2,  D = d0+d1 Z+d2 Z^2,
alpha = d0 n1-d1 n0,
beta  = d0 n2-d2 n0,
gamma = d1 n2-d2 n1,
mathcal_b = beta^2-alpha gamma.
```

## Theorem

Define the Bezout secant

```text
W(Y,Z) = (N(Y)D(Z)-N(Z)D(Y))/(Y-Z)
       = alpha+beta(Y+Z)+gamma YZ,
D_y = D(X,y).
```

Then the following statements hold.

1. For distinct labels `y,z`,

   ```text
   W(y,z) = D_y D_z U_yz,       D_y D_z | mathcal_b.
   ```

2. Every monic nonconstant irreducible `rho in R` divides at most two of the
   eight values `D_y`. Consequently

   ```text
   product(D_y : y in A union C) | mathcal_b.
   ```

3. For distinct rows `a,a'` and columns `b,b'`, put

   ```text
   Delta = U_ab U_a'b' - U_ab' U_a'b.
   ```

   The exact signed rectangle identity is

   ```text
   D_a D_a' D_b D_b' Delta
     = -(a-a')(b-b') mathcal_b.
   ```

   The inherited source theorem gives `Delta=g kappa`, where `kappa!=0` and
   `deg kappa<=59730`. Thus, up to a nonzero field scalar,

   ```text
   mathcal_b = g kappa D_a D_a' D_b D_b'.
   ```

4. Choose cofactor rows `u1,u2,u3`, omitted row `u4`, cofactor columns
   `v1,v2`, and omitted columns `v3,v4`. The inherited cofactor interpolation
   and the rectangle identity give, up to a nonzero field scalar,

   ```text
   mathcal_b = g c D_u1 D_u2 D_u3 D_v1 D_v2.
   ```

   Therefore, with

   ```text
   P_opp = D_u4 D_v3 D_v4,
   ```

   one has

   ```text
   P_opp | g c,      P_opp/gcd(P_opp,g) | c.
   ```

5. The primitive source identity is coefficientwise:

   ```text
   (T-Z)N-xi D in g R[Z].
   ```

   It implies

   ```text
   D(X,T)=gJ,  D0(X,T)=gJ0,  J0=cJ != 0.
   ```

   Hence `c|J0` and

   ```text
   P_opp/gcd(P_opp,g) | c | J0.
   ```

6. If `pi^e || g`, at most one of the eight labels has `pi|D_y`, and

   ```text
   v_pi(P_opp) <= e+v_pi(c) <= e+v_pi(J0).
   ```

   If `rho` does not divide `g`, then

   ```text
   v_rho(D_u4)+v_rho(D_v3)+v_rho(D_v4)
     <= v_rho(c) <= v_rho(J0).
   ```

7. In the inherited quadratic branch `deg J0<=30831`,

   ```text
   deg(P_opp/gcd(P_opp,g)) <= 30831,
   deg P_opp <= 98303 = 3B-1,
   min(deg D_u4,deg D_v3,deg D_v4) <= 32767 = B-1.
   ```

   In the inherited cubic branch `deg J0<=57794`,

   ```text
   deg(P_opp/gcd(P_opp,g)) <= 57794,
   deg P_opp <= 125266,
   min(deg D_u4,deg D_v3,deg D_v4) <= 41755.
   ```

## Proof

Expanding `N(Y)D(Z)-N(Z)D(Y)` proves the displayed secant and its sign.
At two source labels, substitution of `N(y)=V_yD_y` gives
`W(y,z)=D_yD_zU_yz`.

For fixed `y`, the polynomial `W(y,Z)` is linear in `Z`. The numerator before
division by `y-Z` equals `D_y(V_yD(Z)-N(Z))`; the parenthesis vanishes at
`Z=y`. Therefore `D_y` divides both coefficients of `W(y,Z)`. Taking the
determinant of these two coefficient vectors at distinct `y,z` gives
`D_yD_z | mathcal_b` because `y-z` is a field unit.

If an irreducible `rho` divided three denominator evaluations, the reductions
of both degree-at-most-two polynomials `D` and `N` modulo `rho` would vanish at
three distinct field constants. Every coefficient of both would then be
divisible by `rho`, contradicting joint coefficient primitivity. Pairwise
divisibility, applied valuation by valuation, now proves that the product of
all eight denominator evaluations divides `mathcal_b`.

Writing `W` as the bilinear form with matrix
`[[alpha,beta],[beta,gamma]]` and taking its `2 x 2` evaluation determinant
gives the negative rectangle sign. Substitution of the source secants and the
inherited nonzero factorization `Delta=g kappa` proves the rectangle formula.

For a cofactor row `u_i`, the inherited cofactor quotient `h_i` satisfies
`D0(u_i)=h_i product_{m!=i}(u_i-u_m)`. The label product is a field unit, so
`h_i` is a nonzero field scalar times `cD_u_i`. Substituting this into the
corresponding rectangle factorization gives the five-label formula. Cancelling
its five nonzero denominator factors from the full eight-label divisor proves
`P_opp|gc`, including when factors are shared.

Modulo `g`, the degree-at-most-three polynomial
`(T-Z)N-xi D` vanishes at the eight labels. Four labels and the unit
Vandermonde determinant suffice even when `R/(g)` is nonreduced, proving the
coefficientwise identity. An actual valid edge makes `xi` a unit modulo `g`.
Specializing `Z=T`, using the inherited nonzero specialization, and cancelling
in `R` gives `D(T)=gJ` and `J0=cJ!=0`.

For `pi^e||g`, polynomial division in `(R/(pi^e))[Z]` gives
`D=(T-Z)L_pi`, `deg_Z L_pi<=1`. The source identity and injectivity of
multiplication by the unit-leading polynomial `T-Z` give `N=xi L_pi`.
Primitivity implies `L_pi mod pi` is nonzero. Since each `T-y` is a unit
modulo `pi`, `pi|D_y` exactly when `L_pi(y)=0`; a nonzero linear polynomial
has at most one such label. The valuation and degree statements now follow
from `P_opp|gc`, `J0=cJ`, and the two inherited branch bounds.

## Verification and provenance

The independent hostile proof audit accepted exactly this theorem layer:

```text
packet SHA-256:
16f814dbc226e0f9cb84b2a093473beb7551f16b261ab963611c148d10126a7a
response SHA-256:
ae3f898ccf445060dbdb2d77dd8de7e2f4a8919bbe45baa8f66cd72e946f0e7d
```

The standard-library verifier
`experimental/scripts/verify_rank16_fixed26_bezout_rectangle_conductor.py`
checks the deployed ledger, source pins, exact Bezout and rectangle identities
in a deterministic polynomial model, the cofactor/omitted-triple conductor
specialization, a nonreduced prime-power model, degree endpoints, explicit
hypothesis counterexamples, semantic mutations, package hashes, and frozen
ordinary/optimized output parity.

## Nonclaims and exact remaining wall

This theorem does not exclude either source-valid terminal

```text
deg_Z B3=2 with deg J0<=30831,
deg_Z B3=3 with deg J0<=57794.
```

It does not turn a low-degree omitted denominator into a contradiction with
splitting, fibre avoidance, footprint, nonpairing, or first-match ownership.
It proves no cap six, global owner, add-back, rank-16 parent, recurrence,
Grand List, Grand MCA, or official theorem. The official score remains `0/2`.

The exact next wall is a source-incidence theorem showing that the displayed
conductor divisor and degree bounds are impossible in both the quadratic and
cubic branches, followed by a separate source-valid global aggregation.
