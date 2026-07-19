# Fixed-27 primitive-quartic branch envelope

## Scope and source pins

This note records a finite, field-specific, data-package-conditional theorem.
It uses `origin/main@3404d21b64c876c6d9b995ad3e29d7120ab27a54` and consumes the
exact dependency heads in the semantic order

- PR #894: `3c048a9637a02525ef41d1c340252200e4b0f41a`;
- PR #902: `f2be578d5b17d546c0cd4437e4927e74c9e47f7c`;
- PR #930: `a724e8bb7146e202d4d7f301ae68484a217f7d0e`;
- this Role 08 theorem.

Thus the required order is PR #894 -> PR #902 -> PR #930 -> Role 08. The file
sets are textually nonoverlapping, but an intermediate merge that exposes this
consumer before its producers is not certified.

Work over `F = F_2130706433`, with `H = mu_(2^21)`, `B=32768`, and
`Lambda=mu_64`. Fix one hypothetical data package that independently satisfies
every literal fixed-27, same-word, same-generator,
same-syndrome-projective-ray, first-match, exact affine-rank-two
primitive-quartic, residual-squarefreeness, splitting, selected-fibre
avoidance, nonzero, and exact-head hypothesis of the three dependencies. This
is an assumption on the data package, not a claim that the upstream compiler
produces one. It has seven distinct selected labels `y_0,...,y_6`, monic
squarefree `H`-split residuals `R_i`, nonzero source scalars, and quotients with

```text
(X^B-y_i)R_i = q_i h + g W_i,
deg R_i = d = 63601,
deg W_i <= w = 28897.
```

Set `c=|Base|<=12997`, `r=d-c`, and `lambda=w-c`. Outside `Base`, every
root has occupancy at most three. Let `n3` be the number of outside-Base roots
of occupancy exactly three and let `U` be the union of the seven residual root
sets.

The affine specialization uses the PR #894 orientation

```text
b_i(z) = a_0(z)/(z-y_i) * (c_i-c(z)).
```

Here `a_0(z)!=0` is a source hypothesis and `z-y_i!=0` follows separately
from selected-fibre avoidance. PR #930 prints the reciprocal scalar. That
nonzero rescaling preserves line incidence, but it is not the source formula
used here.

The symbol `y_0` is only an algebraic normalization anchor. This theorem
assumes that the normalization leaves the upstream first-match owner and its
ordering unchanged. It does not prove that ownership/normalization interface.

## Integer envelopes

For integers `k>=1` and `T>=0`, write `T=kq+s`, `0<=s<k`, and define

```text
Q_k(T) = s(q+1)q + (k-s)q(q-1).
```

For a fixed `c`, let `D(c)` be the powers `M=2^j`, `0<=j<=13`, that divide
`r`. For `M` in `D(c)`, set

```text
b_M = B/M,
L_M = floor(lambda/M),
A_M = (b_M-1)(2L_M-2).
```

All optimizer variables below are integers. Define

```text
T_M^(3) = max { T : 0<=T<=5L_M and Q_5(T)<=A_M },
K_3(c)   = max_{M in D(c)} M T_M^(3).
```

For integers `0<=T<=4L`, define

```text
Q_(4|3,L)(T)
  = min { Q_4(g)+Q_3(T-g) : max(0,T-3L)<=g<=min(L,T) }.
```

Then define

```text
T_M^(4) = max { T : 0<=T<=4L_M and Q_(4|3,L_M)(T)<=A_M },
K_4(c)   = max_{M in D(c)} M T_M^(4),
J(c)     = max(K_3(c),K_4(c),2lambda).
```

## Conditional local theorem

Every qualifying data package in the stated scope satisfies

```text
n3 <= J(c).
```

### Proof

**1. Base cancellation and root-to-line assignment.** PR #894 and PR #930's
Base and direction-gcd cancellation give, for every residual index `i`,

```text
S rho_bar_i = b_i(X^B) * (F,G),
gcd(F,G)=1,
L=max(deg F,deg G)<=lambda,
```

where `S` is root-free on `H`. The exact rank-two and nonzero hypotheses rule
out the simultaneous collapse `F=G=0`. At an outside-Base root of occupancy three, the three
literal label coordinates therefore determine a unique maximal affine line.
For each such line `ell`, its assigned-root set `A_ell` lies in the zero set of
a nonzero constant linear combination of `F,G`; hence
`|A_ell|<=L<=lambda`. No maximal line contains five labels, and distinct
maximal lines intersect in at most one label.

**2. Fixed-fibre localization and the geometric split.** For a three-label
line `{i,j,k}`, PR #902 gives

```text
det(b_i,b_j)=a_0 delta_ij,
delta_ij != 0,
deg delta_ij <= 2.
```

One root is `y_k`; an assigned root `x` supplies the other root `z=x^B`, and
selected-fibre avoidance excludes `z=y_k`. Thus each nonempty three-label line
is localized in one additional fixed `B`-fibre. PR #930's split-quartic Pasch
census and the odd-characteristic Fano obstruction allow at most five such
lines.

If one maximal line `ell_0` contains four labels, an assigned occupancy-three
root omits one label `j`. The degree-two secant argument and selected-fibre
avoidance force `x^B=y_j`, so

```text
A_(ell_0) = disjoint_union_(j in ell_0) A_(ell_0,j),
A_(ell_0,j) subset {x in H : x^B=y_j},
sum_j |A_(ell_0,j)| <= lambda.
```

There are at most three additional maximal lines because each consumes a
distinct complementary label pair. If there are two four-label lines, they
intersect in one label, cover all seven labels, admit no third maximal line,
and directly give `n3<=2lambda`.

**3. Quotient cells and ordered pairs.** At a dyadic composition stage write

```text
F(X)=f(X^M), G(X)=h(X^M), M|B, gcd(f,h)=1.
```

The reduced identities and root-freeness of `S` make every residual root set
and every assigned component invariant under the free `mu_M` action. Hence
`M|r`, `M|n3`, and quotienting by `x -> x^M` maps each fixed `B`-fibre
component into a fixed `b_M`-fibre. Quotient images of distinct assigned
components are disjoint: equality would put their preimages in the same
`mu_M` orbit and contradict the assigned-root partition.

Put `L*=max(deg f,deg h)<=L_M`. For `u in mu_(b_M)`, define

```text
Psi_u(Z)=f(uZ)h(Z)-f(Z)h(uZ).
```

If `Psi_u` is nonzero, its degree is at most `2L*-1` (the top term cancels
when the degrees agree), and `Psi_u(0)=0`; it therefore has at most `2L_M-2`
relevant nonzero roots. A quotient cell of size `tau` contributes the ordered,
not unordered, count `tau(tau-1)`. Each ordered pair has a unique nonidentity
ratio `u`, so if every nonidentity `Psi_u` is nonzero,

```text
sum_cells tau(tau-1) <= (b_M-1)(2L_M-2)=A_M.       (1)
```

**4. Three-label branch.** Put `T=n3/M`. There are at most five quotient
cells, each of size at most `L_M`. Convexity gives
`sum tau(tau-1)>=Q_5(T)`. If `T>5L_M`, capacity already fails; if
`T>T_M^(3)`, the lower bound exceeds `(1)`. Thus `n3>K_3(c)` forces
`Psi_u=0` for some nonidentity `u`.

**5. One-four-label branch.** Let `g` be the total quotient size of the at
most four fixed-fibre components on `ell_0`. Their common line polynomial gives
`0<=g<=L_M`; the at most three other line cells give

```text
max(0,T-3L_M) <= g <= min(L_M,T).
```

Convexity gives `Q_4(g)+Q_3(T-g)`, and minimizing over this interval gives
`Q_(4|3,L_M)(T)`. Hence `n3>K_4(c)` likewise forces a nonidentity identity
`Psi_u=0`.

**6. Identity-to-composition descent.** If `Psi_u=0`, coprimality gives
`f(uZ)=alpha f(Z)` and `h(uZ)=alpha h(Z)`. If `m>1` is the order of `u`, all
exponents in both polynomials have one common residue modulo `m`. A positive
residue would make both divisible by `Z`, so the residue is zero and
`f,h in F[Z^m]`. The composition depth strictly increases to `M'=Mm|B`, and
invariance gives `M'|r`. Repeat while `M'<=8192`. A stage `M'>=16384` is
impossible because

```text
49152 < 50604 <= r <= 63601 < 65536
```

contains no multiple of `16384`. Therefore the identities forced in the two
branches are impossible, while the two-four-label branch already has
`n3<=2lambda`. This proves `n3<=J(c)`.

**7. Finite comparison and support floor.** The deterministic replay computes
all 12,998 values of `J(c)` and all 25,996 admissible `(c,M)` states. Across
those states, each evaluated under both branch formulas,

```text
K_4(c) > K_3(c) for 0<=c<=7009,
K_4(c) = K_3(c) for c in {7010,7011,7012},
K_3(c) > K_4(c) for 7013<=c<=12997.
```

The term `2lambda` never governs. Relative to PR #930,

```text
J(c) < 5lambda-7320 for 0<=c<=12996,
J(12997) = 5lambda-7320 = 72180.
```

Thus the integer interval

```text
J(c)+1 <= n3 <= 5lambda-7320
```

is excluded on every nonmaximal Base layer. Its width ranges from 3 to
37,170. The union estimate is

```text
|U| >= V(c) := c + ceil((7(63601-c)-J(c))/2).
```

Consequently, `V(c)>=154023` for `0<=c<=12996`, with equality only at
`c=12996`, while `V(12997)=154021`.

**8. Endpoint saturation.** At `c=12997`, `r=50604` and `lambda=15900`.
PR #894 gives `Q_res!=0`, `C_Base^4|Q_res`, and
`deg Q_res<=4c=51988`, so `Q_res=kappa C_Base^4`. If
`beta_1,...,beta_4` are the roots of `a_0`, counted with multiplicity, and
`E_(beta_nu)=C_Base e_nu`, then `deg e_nu<=15900`. The product identity and
Base cancellation give

```text
product_(nu=1)^4 e_nu = kappa' s,
deg s = 63600 = 4*15900.
```

Thus every `e_nu` has degree 15,900. The individual factors live over a
splitting field of `a_0` and are root-free on `H`. This is a saturation
identity, not a source-realized extremizer.

## Replay

Run

```bash
python3 experimental/scripts/verify_rank16_fixed27_quartic_branch_envelope.py
python3 -O experimental/scripts/verify_rank16_fixed27_quartic_branch_envelope.py
python3 experimental/scripts/verify_rank16_fixed27_quartic_branch_envelope.py --tamper-selftest
```

The verifier uses only the Python standard library. It pins six dependency
files, reconstructs all 12,998 Base rows and 25,996 dyadic states, checks the
branch crossover, exact selected rows, support minima, and endpoint identities,
and byte-compares both committed CSV certificates.

## Nonclaims and remaining wall

This does not prove fixed-27 quartic cap six. It does not prove that any data
package in scope exists, exclude every seven-label primitive-quartic cell, or
construct a received word, codewords, residuals, quotients, generator,
syndrome ray, and first-match owner realizing any surviving row. Equality and
failure of the next integer comparison do not prove optimality among all source
arguments.

There is no global owner theorem, source-cell disjointness theorem, add-back or
aggregation theorem, parent closure, recurrence, all-rank result, asymptotic
result, Grand MCA theorem, or Grand List theorem. The finite and asymptotic
ledger deltas are zero, and the official score remains `0/2`.

The remaining theorem-facing wall is to compile every actual primitive
first-match source cell, prove the required incidence for each retained cell,
and aggregate disjoint same-line budgets. The lower-`n3` region and the maximal
Base equality layer remain open.
