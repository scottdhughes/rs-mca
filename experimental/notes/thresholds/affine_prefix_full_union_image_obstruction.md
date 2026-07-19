# Affine-prefix full-union image obstruction

## Status

This note records the independently audited increment to the characteristic-
five affine-prefix source family already compiled in PR #903 and partitioned
in PR #959. It is an exact one-row, one-received-line theorem with zero finite-
ledger, asymptotic-ledger, Grand MCA, Grand List, recurrence, and official-
score movement.

The source contract is `origin/main` at
`3404d21b64c876c6d9b995ad3e29d7120ab27a54`. The relevant PR #903 files are
already byte-identical to files on that base. This note adds the full mixed-
stratum effective-span calculation, the full-image Sidon calculation, and the
literal `N=4B` retention condition. It does not add a semantic owner compiler.

## Exact source family

For every integer `B >= 2`, set

```text
F_B = F_(5^(3B)),  n = N = 4B,  k = 2B-1,  m = 2B.
```

Choose an `F_5`-basis

```text
a_1,u_1,v_1,...,a_B,u_B,v_B
```

of `F_B`, put

```text
D_B = {a_i + eps*u_i + eta*v_i :
       1 <= i <= B and eps,eta in {0,1}},
C_B = RS_(F_B)(D_B,2B-1),
R_gamma(X) = X^(2B) + gamma X^(2B-1),
Omega_B = {S subset D_B : |S|=2B}.
```

For `S in Omega_B`, write

```text
Q_S(X) = product_(x in S)(X-x)
       = X^(2B) + c_1(S)X^(2B-1) + ... .
```

Then `gamma=c_1(S)` and `h_S=R_gamma-Q_S` give a degree-`<k` word whose
complete agreement set with `R_gamma` is exactly `S`. Conversely, every exact
`2B` explanation has this form. Thus the displayed incidence is complete, not
only a lower-bound construction.

## Full raw profile

Let

```text
P(y) = 1 + 4y + 5y^2 + 4y^3 + y^4,
Q(y) = 1 + 4y + 4y^2 + 4y^3 + y^4,
L_B = [y^(2B)] P(y)^B,
c_M = [y^(2M)] Q(y)^M,
L_(B,j) = binom(B,j)c_(B-j),
M_B = binom(4B,2B).
```

The exact `c_1` image has `L_B` slopes. Its canonical `j`-stratum has
`L_(B,j)` slopes and every such slope has fibre size `2^j`; hence

```text
sum_(j=0)^B L_(B,j) = L_B,
sum_(j=0)^B 2^j L_(B,j) = M_B.
```

The elementary central-coefficient bounds used below are

```text
15^B/(6B) <= L_B <= 15^B,
16^B/(4B+1) <= M_B <= 16^B.
```

## Effective Fourier obstruction

For the boundary map `Phi_B(S)=c_1(S)=-sum_(x in S)x`, translate by one
point of `D_B`. The differences span

```text
V_B = span_(F_5){u_i,v_i,a_i-a_1 : 1<=i<=B, 2<=i<=B},
dim_(F_5) V_B = 3B-1,
A_eff,B = |V_B| = 5^(3B-1).
```

Applying the source effective-span inequalities to the complete full profile
forces every admissible multiplier `kappa_B` to satisfy

```text
kappa_B >= A_eff,B/L_B >= (1/5)(25/3)^B,
kappa_B >= 2^B A_eff,B/M_B >= (1/5)(125/8)^B.
```

Therefore the unrefined full raw profile admits no subexponential effective-
Fourier multiplier.

## Full-image Sidon obstruction

A `j`-fibre is a Cartesian product of `j` binary diagonal choices. Its
additive energy and normalized energy are exactly

```text
E_(B,j) = 6^j,
Delta_(B,j) = 6^j/(2^j)^3 = (3/4)^j.
```

Set

```text
sigma_* = (1/4) log(4/3).
```

Because `N=4B`, the weak cutoff `Delta <= exp(-sigma_* N)` selects exactly
the unique `j=B` fibre. The full-image normalized Sidon-heavy expression is

```text
G_(Sid,q,sigma_*)(B)
  = L_B^(-1) (M_B/(2^B L_B))^q.
```

For every source-accessible logarithmic order `q_B -> infinity`, with
`q_B <= (log(4B))^C`, the exact normalized rate is

```text
lim_(B->infinity) log G_(Sid,q_B,sigma_*)(B)/(4B q_B)
  = (1/4) log(15/8) > 0.
```

Hence the unrefined full raw profile has no source-strength image-normalized
Sidon payment.

## Conditional retention consequence

The only semantic consequence certified here is conditional. On this exact
row, with active set exactly `T_B=D_B` and `N=4B`, suppose a same-boundary
primitive residual has its full support slice inside `Omega_B`, retains the
complete all-diagonal `gamma_B` fibre `H_B`, and satisfies the source
logarithmic-moment accessibility and Sidon-payment hypotheses. Then its full-
slice residual mean must satisfy

```text
Nbar_(lambda,B) >= 2^(B-o(B))
```

before a source-strength Sidon payment is possible. A later semantic compiler
must instead route `gamma_B` earlier, split `H_B` by refining the boundary,
prove that mean bound, or supply another independently proved source-incidence
mechanism.

## Replay

Run

```bash
python3 experimental/scripts/verify_affine_prefix_full_union_image_obstruction.py
python3 -O experimental/scripts/verify_affine_prefix_full_union_image_obstruction.py
```

Both outputs must match the checked-in expected transcript. The verifier is
standard-library-only. It pins the seven source and predecessor artifacts,
constructs `F_(5^6)` independently, exhausts all `70` supports for `B=2`,
checks the exact fibre histogram and top-fibre energy, verifies the effective
span, and checks the integer coefficient and multiplier ledgers for every
`2 <= B <= 64`. Seven semantic tamper selftests cover the audited mutation
classes.

## Nonclaims and remaining wall

This note does not prove:

- an actual C1--C9 semantic owner, primitive cell, or survival theorem;
- that analytic nonpayment implies semantic non-primitivity;
- a row-uniform theorem, a theorem for larger active sets, or another field;
- unconditional routing, boundary refinement, or recurrence;
- a finite or asymptotic ledger payment;
- Grand MCA hard input 2, Grand MCA, or Grand List;
- any official-score movement.

The remaining wall is to compile the actual primitive semantic first-match
cells and prove a source-valid image-scale or replacement-incidence theorem
for every retained cell, then aggregate disjoint same-line budgets without
interchanging `sup_line sum_lambda` with `sum_lambda sup_line`.
