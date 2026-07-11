# Minimal-polynomial saturation of complete simple-pole lists

**Status:** `PROVED` for the complete-list theorem and finite regressions
below; `ROUTE CUT` for low-residue-rank unsafe constructions. This is not a
claim that the printed C1--C8 atlas already contains the residue cells.

**Verifier:**

```text
python3 experimental/scripts/verify_minimal_polynomial_simple_pole_saturation.py
```

## 1. Complete witness decomposition

Let `D subseteq B subseteq F`, `|D|=n`, `1<=k<n`, and `k+1<=m<=n`. For a
`B`-valued word `U` define its complete dimension-`(k+1)` list

```text
L_m(U)={P in B[X]: deg(P)<=k and |{x in D:U(x)=P(x)}|>=m}.
```

Fix `alpha in F\D` and `delta in F`, and put

```text
f_alpha(x)=U(x)/(x-alpha),
g_alpha(x)=-1/(x-alpha),
r_(alpha,delta)=(f_alpha+delta*g_alpha,g_alpha).
```

For `P in L_m(U)`, write

```text
A_P={x in D:U(x)=P(x)},
h_P(X)=(P(X)-P(alpha))/(X-alpha).
```

Then the literal exact-`m` witness incidence is the disjoint union

```text
W_m(r_(alpha,delta))
 = disjoint_union_{P in L_m(U)}
   {(P(alpha)-delta,S,h_P): S subseteq A_P, |S|=m}.       (1)
```

In particular, the explanation-state map is a bijection

```text
P |-> (P(alpha)-delta,h_P),                               (2)
```

the state associated with `P` has exact retained-support occupancy
`binom(|A_P|,m)`, and the actual bad-slope set is

```text
Z_m(r_(alpha,delta))={P(alpha)-delta:P in L_m(U)}.         (3)
```

No separating-pole hypothesis is used.

To prove (1), on every `x in A_P` one has

```text
f_alpha+P(alpha)g_alpha-h_P=(U-P)/(X-alpha)=0.
```

Conversely, an exact witness `(gamma,S,h)` gives

```text
P=(X-alpha)h+delta+gamma.
```

It has degree at most `k` and agrees with `U` on at least `m>=k+1` points.
Interpolation on `B`-points with `B`-values forces `P in B[X]`; evaluating at
`alpha` recovers `gamma=P(alpha)-delta` and then `h=h_P`.

The support is noncommon: if a degree-`<k` polynomial explained `g_alpha` on
`k+1` points, `(X-alpha)G+1` would have degree at most `k` and `k+1` roots,
yet value one at `alpha`.

## 2. Exact collision quotient

Let `pi_alpha in B[X]` be the monic minimal polynomial of `alpha` and
`d_alpha=deg(pi_alpha)`. For list polynomials `P,Q`,

```text
P(alpha)=Q(alpha)
 iff pi_alpha divides P-Q
 iff rem_(pi_alpha)(P)=rem_(pi_alpha)(Q).                 (4)
```

Evaluation at `alpha` is injective on the remainder space of degree below
`d_alpha`. Therefore it induces a bijection

```text
rem_alpha(L_m(U)) -> Z_m(r_(alpha,delta)),
R |-> R(alpha)-delta.                                    (5)
```

Thus the slope quotient is exactly reduction of the complete list modulo the
pole's minimal polynomial.

## 3. Affine residue-rank bound

Assume the list is nonempty, fix `P0` in it, and define

```text
V_alpha=span_B{rem_alpha(P-P0):P in L_m(U)},
rho_alpha=dim_B(V_alpha),
b=|B|.
```

The smallest `B`-affine space containing the slopes is

```text
P0(alpha)-delta+{R(alpha):R in V_alpha}.                  (6)
```

Consequently

```text
|Z_m(r_(alpha,delta))|<=b^rho_alpha,                      (7)
rho_alpha<=min(d_alpha,k+1,
  dim_B span_B(L_m(U)-P0)).                               (8)
```

For every challenge subset `Gamma subseteq F`, the same proof gives

```text
|Z_m(r_(alpha,delta)) cap Gamma|<=b^rho_alpha.             (9)
```

This identifies the actual escape resource: the complete-list residue rank,
not merely the size of the ambient scalar field.

## 4. Sharp collision floors

Let `L=|L_m(U)|`, `M=b^rho_alpha`, and let `mu_gamma` count explanation states
at slope `gamma`. If `L=uM+v`, `0<=v<M`, then

```text
max_gamma mu_gamma>=ceil(L/M),
sum_gamma binom(mu_gamma,2)>=M binom(u,2)+uv.              (10)
```

For raw witnesses, let

```text
N_W=sum_{P in L_m(U)} binom(|A_P|,m)
```

and let `omega_gamma` be their slope multiplicities. Writing
`N_W=u_W M+v_W`, `0<=v_W<M`, gives

```text
max_gamma omega_gamma>=ceil(N_W/M),
sum_gamma binom(omega_gamma,2)
 >=M binom(u_W,2)+u_W v_W.                               (11)
```

These are the optimal balanced-bin floors given only the total mass and `M`
available bins.

## 5. Order-stable first-match continuation

After any earlier ordered cells, intersect (1) with the literal residual
slopes not previously claimed. Partition the surviving witnesses by their
minimal-polynomial remainder, equivalently by their actual slope. The
nonempty pieces

```text
D_R=W_>j cap pi_gamma^(-1)(R(alpha)-delta)                (12)
```

are witness-exhaustive, each has one actual slope, and there are at most
`b^rho_alpha` of them. No witness remains after this continuation.

This is a parameterized source-valid residue/slope continuation. It is not
identified with an already printed canonical C7 cell. Nevertheless the
line-wise target consequence is exact:

```text
b^rho_alpha<=B*  implies |Z_m(r_(alpha,delta)) cap Gamma|
                         <=B*.                            (13)
```

Hence an unsafe translated standard simple-pole line in this construction
class must satisfy

```text
rho_alpha>=ceil(log_b(B*+1)).                             (14)
```

Scalar translation changes only the affine coset, not its size or residue
partition.

## 6. Locator-prefix specialization

For a complete depth-`w` locator-prefix fiber, the exact prefix-list theorem
indexes the list by supports `S` through `P_S=U_z-Q_S`, with agreement set
exactly `S`. Then

```text
P_S(alpha)=P_T(alpha)
 iff Q_S=Q_T mod pi_alpha.                                (15)
```

The pole-saturation cells are therefore the locator-remainder classes
`S |-> Q_S mod pi_alpha`. At the base pole `alpha=0`, `pi_alpha=X`, so this
reduces to partition by locator constant coefficient. The merged aperiodic
one-ray theorem is the degree-one specialization of this saturation
component; its separate aperiodicity construction is not subsumed here.

## 7. Validation and remaining wall

The verifier exhausts the `B=F_5`, `D=F_5^*`, `k=1`, `m=2`, `U=X^2`
regression. It finds six list states and six exact witnesses but four base-pole
slopes with multiplicities `2,2,1,1`. At
`alpha=t in F_25=F_5[t]/(t^2-2)`, all six slopes are distinct and the residue
rank is two. It also checks arbitrary earlier masks, the `U=0` raw occupancy
`binom(4,2)=6`, every balanced floor for `1<=M<=6`, `0<=L<=10`, and tamper
regressions.

The next exact unsafe-side target is an explicit high-residue-rank prefix-pole
sequence whose actual slopes still exceed the target after the complete
printed C1--C8 first-match atlas. This note does not produce that survivor,
prove A2/A4/A7, close a deployed row, establish the full unsafe reserve, prove
`U(a0+1)<=B*`, or solve the prize problem.
