# Rank-16 fixed-26 direct eliminant

**Status:** independently accepted narrow local theorem, transcribed for
director replay. This theorem is conditional on one literal common-source
fixed-26 cell and makes no finite or asymptotic payment.

## Literal source cell

Work over

```text
F = F_2130706433,       R = F[X],       K = F(X),
n = 2097152,            b = 32768,      a = 67472,
r = 63601,              d = 28897,      L3 = 59730,
T = X^b,                H = mu_n,       Omega = mu_64.
```

Fix one received word and its canonical first-match owner, one monic
degree-`a` polynomial `g` with `gcd(g,X^n-1)=1`, one nonzero projective
representative `eta`, and the canonical source element

```text
xi = rem_g(G_C^(-1) eta),       deg_X(xi) < a.
```

Fix one 26-label core and eight distinct external labels, partitioned into
four row labels and four column labels. Every one of the sixteen cross-pairs
must be an actual-valid common-source edge: exact locator degree, squarefree
complete `H`-splitting, selected-fibre avoidance, no additional complete
fibre, the required residual footprint, nonpairing, every earlier-owner
exclusion, and canonical first-match ownership all remain hypotheses. Matrix
entries are the source-normalized divided differences `U_yz`; independently
monic-scaled locators cannot be substituted.

Assume all `3 x 3` cross minors vanish. The inherited nonzero `2 x 2` theorem
then makes the cross matrix have rank exactly two over `K`. The strict input
is

```text
r - 2d = 63601 - 2*28897 = 5807 > 0.
```

## Sylvester convention

For formal degrees `u=deg_Z(P)` and `v=deg_Z(Q)`, let `S_(u,v)(P,Q)` be
the determinant of the `(u+v) x (u+v)` matrix whose first `v` rows are the
shifted descending-coefficient rows of `P` and whose next `u` rows are the
shifted descending-coefficient rows of `Q`. Missing high coefficients are
zero padded. Columns are ordered by descending powers
`Z^(u+v-1),...,Z,1`. The ordinary resultant uses the same convention at the
exact degrees.

## Theorem

Under the literal source hypotheses above, after one joint coefficient-content
normalization and rebuilding the base-`T` transfer, there are polynomials

```text
A,B,E in R[Z],       J,M in R
```

such that, with `F(Z)=T-Z` and `m=deg_Z(B)`,

```text
F A - xi B = g E,
B(T)        = g J != 0,
E(T)        = -xi J,
m           in {2,3},
deg_Z(A)    = m-1,
deg_Z(E)    <= m.
```

Every `X`-coefficient of `B` and `E` has degree `<b`; every
`X`-coefficient of `A` has degree `<a`. The branch bounds are

```text
m=2: deg_X(J) <= 30831,
m=3: deg_X(J) <= 57794.
```

There is a unique `M`, possibly zero, satisfying

```text
Res_Z(A,B)       = g^(m-1) M,
S_(m-1,m)(A,E)  = (-xi)^(m-1) M,
S_(m,m)(B,E)    = J M.
```

Repeated factors of `g` are allowed. Equivalently, with the convention
`v_pi(0)=+infinity`, every irreducible `pi` satisfies

```text
v_pi(Res_Z(A,B)) >= (m-1) v_pi(g).
```

If `M != 0`, then

```text
m=2: deg_X(M) <= 100237,
m=3: deg_X(M) <= 133003.
```

In the quadratic branch, `B(X,y)` is nonzero for every `y in Omega`. In the
cubic branch, `B` has at most one scalar root in `Omega`, and that root is
simple.

## Proof

Every actual-valid locator is squarefree, completely `H`-split, and has
degree `r`. If a selected `2 x 2` source minor vanished, the roots of one
locator would be covered by two permitted gcd intersections of degree at most
`d`, contradicting `r>2d`. Thus rank is exactly two over `K`.

Choose three row labels. A left-kernel cofactor vector has entries
`C_i=g h_i` with `h_i != 0` and `deg_X(h_i)<=L3`. Lagrange interpolation from
these cofactors produces a coprime rational pair `N_0,D_0` of maximum
`Z`-degree two. Its values agree with the fixed source at the three selected
rows and four columns. Replacing one selected row gives a second pair; their
cross-polynomial has degree at most four and six distinct roots, hence is
zero. The first pair therefore interpolates all eight labels.

Remove the monic joint coefficient content `c` of `N_0,D_0`. Since
`D_0(u_i)=h_i product_(k!=i)(u_i-u_k)`, the content divides every `h_i`.
Rebuild the transfer from the normalized cofactors `h_i/c`; dividing an old
block decomposition by `c(X)` is not valid.

For every source label `y`, the fixed-26 compiler gives

```text
(T-y)V_y = xi + g S_y.
```

Since `N(y)=V_y D(y)` at all eight labels, the degree-at-most-three polynomial
`(T-Z)N-xi D` vanishes coefficientwise modulo `g`; four distinct labels and
the Vandermonde map suffice even when `R/(g)` is nonreduced. Hence

```text
(T-Z)N-xi D = g E_0.
```

Actual-validity makes `xi` a unit modulo `g`. Evaluation at `Z=T` gives
`g|D(T)`. If `D(T)=0`, then `T-Z` divides both `D` and, by the eight-label
block-factor argument, `N`, contradicting coprimality. Thus `D(T)=gJ!=0`.

Write each normalized cofactor uniquely as `h_i=A_i+T B_i` and set

```text
C(Z) = sum_i B_i l_i(Z),
B(Z) = sum_i (A_i+Z B_i) l_i(Z).
```

Then `D=B+(T-Z)C`, `B(T)=gJ`, every coefficient of `B` has degree `<b`,
and `deg_Z(B)<=3`. A degree-at-most-one `B` would make the nonzero multiple
`B(T)` of the degree-`a` polynomial `g` have degree below `a`; therefore
`m` is two or three. The base-`T` degree calculation gives the two displayed
`J` bounds.

Put `A^(0)=N-xi C`, reduce each of its `Z`-coefficients modulo the same monic
`g`, and absorb the quotient into `E`. This gives `FA-xi B=gE`, the stated
coefficient bounds, and `deg_Z(A)=m-1`. Evaluation at `T` gives
`E(T)=-xi J`.

For the eliminant triangle, put `p=m-1`. Scaling the second Sylvester
argument by `g` scales its `p` rows. Row additions remove the `(T-Z)A`
part of `gE=(T-Z)A-xi B`, giving

```text
g^p S_(p,m)(A,E) = (-xi)^p Res_Z(A,B).
```

Since `gcd(g,xi)=1`, unique factorization gives `g^p|Res_Z(A,B)`; define
`M=Res_Z(A,B)/g^p`. The first companion identity follows by cancellation.
Likewise, multiplicativity and the fixed sign convention give

```text
g^m S_(m,m)(B,E)
  = Res_Z(B,(T-Z)A)
  = Res_Z(B,T-Z) Res_Z(B,A)
  = g^m J M,
```

so `S_(m,m)(B,E)=JM`. This coefficient-ring proof neither splits nor lifts
roots of `g`, and therefore covers repeated factors and `M=0`.

Homogeneity of the resultant yields

```text
deg Res_Z(A,B) <= m(a-1)+(m-1)(b-1).
```

Subtracting `(m-1)a` when `M` is nonzero gives 100,237 and 133,003.
Finally, a scalar root `y in Omega` forces `X^b-y|J`. Distinct scalar roots
give coprime degree-`b` factors. The strict bounds `deg J<b` and
`deg J<2b` prove the quadratic and cubic assertions, while a repeated cubic
root would force `(X^b-y)^2|J` and is impossible.

## Nonclaims and exact wall

This theorem does not exclude either transfer branch. It does not prove
`M!=0`, classify the common-factor branch when `M=0`, prove that any source
locator or source-incidence polynomial divides `M`, or improve the baseline
valuation to a strict excess. The cubic branch may retain one simple scalar
fibre. No owner collision, first-match collision, recurrence, field transfer,
finite payment, asymptotic payment, Grand List theorem, Grand MCA theorem, or
official-score movement follows.

The exact remaining wall is to derive a genuine source-incidence divisor of
`M`, or classify `M=0`, strongly enough to exclude both `m=2` and `m=3`
under the literal source contract. The finite owner subtotal remains
`274854110496187589 = 274854110496187592-3`. Official score remains `0/2`.

## Replay scope

`experimental/scripts/verify_rank16_fixed26_direct_eliminant.py` pins the
inherited source files, checks the deployed arithmetic, replays the three
signed Sylvester identities in deterministic nonzero, zero-resultant,
repeated-`g`, and nonconstant-`xi` models, verifies the local quotient form,
and rejects semantic scope mutations. It does not establish that a literal
source cell exists and is not a substitute for the proof above.
