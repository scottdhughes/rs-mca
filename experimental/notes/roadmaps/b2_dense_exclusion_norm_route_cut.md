# Dense-exclusion centered-norm route cut

- **Status:** PROVED route cut / COUNTEREXAMPLE to uniform scalar
  `L2`-smallness.
- **Track:** asymptotic hard input B, corrected dense `w=2,3` add-one
  recursion.
- **Verifier:**
  `python3 experimental/scripts/verify_b2_dense_exclusion_norm_route_cut.py`.

## Scope

This note concerns the actual Reed-Solomon boundary map

```text
Phi_w(x) = (x,x^2,...,x^w),  w in {2,3},
```

on full multiplicative subgroups `D_n` of prime order `n`.  The constructed
fields satisfy `p_n > 2^(n^2)`.  The result is therefore a positive-density
raw source obstruction in a superexponential-field regime.  It is an identity
profile, pre-first-match-atlas statement.  Its realized single and signed-pair
fibers are singletons, but no primitive-atlas survival, ambient image add-back,
A4 payment, or C9 payment is asserted.

## Exact source construction

Let `n >= 5` be prime and

```text
Phi_n(Z) = 1 + Z + ... + Z^(n-1).
```

Define the finite coefficient family

```text
C_n = {c in {-1,0,1,2}^n : 0 <= sum_i c_i <= n-1}.
```

For distinct `c,d in C_n`, put

```text
F_(c,d)(Z) = sum_i (c_i-d_i) Z^i.
```

Then

```text
Res(Phi_n,F_(c,d)) != 0.                                  (R1)
```

Indeed, `Phi_n` is irreducible over `Q` by Eisenstein applied to
`Phi_n(Z+1)`.  If `F_(c,d)` vanished at a primitive complex `n`-th root, then
`deg F_(c,d) <= deg Phi_n` would give `F_(c,d)=t Phi_n` for an integer `t`.
Evaluation at `Z=1` gives

```text
sum_i c_i - sum_i d_i = tn.
```

The left side has absolute value at most `n-1`, so `t=0`, contrary to
`c != d`.  This proves (R1).

Set

```text
Z_n = 6n (2^(n^2))! product_{c != d in C_n, unordered}
                    |Res(Phi_n,F_(c,d))|.                  (R2)
```

Choose a prime divisor `p_n` of `Phi_n(Z_n)` and set
`g_n = Z_n mod p_n`.  If a prime `q` divides `Z_n`, then
`Phi_n(Z_n) = 1 mod q`; hence `gcd(p_n,Z_n)=1`.  Consequently `p_n` divides
neither `6n`, any resultant in (R2), nor any prime at most `2^(n^2)`.  Thus

```text
p_n > 2^(n^2).
```

Also `g_n^n=1`.  The equality `g_n=1` would imply
`p_n | Phi_n(1)=n`, which is impossible.  Since `n` is prime, `g_n` has exact
order `n`.  Let

```text
D_n = <g_n> = {1,g_n,...,g_n^(n-1)} in F_(p_n)^x.
```

If two patterns `c,d in C_n` had the same first power sum modulo `p_n`, then
`g_n` would be a common root of `Phi_n` and `F_(c,d)` modulo `p_n`.  The
common-root property of the resultant would contradict the choice of `p_n`.
Therefore

```text
c |-> sum_i c_i g_n^i                                  (R3)
```

is injective on `C_n`.  It is the first coordinate of the full `Phi_w`
syndrome, so the `w=2,3` syndrome maps are injective on the same patterns.
The family includes every genuine, repeated-coordinate, and cancellation
pattern used below.

## Measures and exact recursions

Work in the additive group `A=(F_(p_n))^w`.  Let `P` be the point measure on
`Phi_w(D_n)`.  Let `nu_r(s)` count `r`-subsets of `D_n` with syndrome `s`,
and let `omega_(a,b)(s)` count ordered disjoint signed pairs `(A_+,A_-)` of
sizes `(a,b)` with syndrome

```text
sum_{x in A_+} Phi_w(x) - sum_{y in A_-} Phi_w(y).
```

For `2 <= r <= n-1`, define

```text
C_r     = nu_(r-1) * P,
kappa_r = C_r - r nu_r,
a_r     = (r-1)/n,
E_r     = kappa_r - a_r C_r.                              (S0)
```

Equivalently, `kappa_r(s)` counts pairs `(B,x)` with
`B subset D_n\{x}`, `|B|=r-2`, and syndrome
`sum_(y in B) Phi_w(y)+2 Phi_w(x)=s`.  Splitting the unrestricted added point
according to whether it belongs to the old set gives, pointwise,

```text
C_r = r nu_r + kappa_r.                                  (S-rec)
```

For `2r <= n`, define

```text
D_r = omega_(r-1,r) * P,
h_r = n-2r+2,
T_r = binom(n,r) binom(n-r,r-1).
```

Here `kappa_r^+(s)` counts triples `(C,B,x)` for which `|C|=r-2`, `|B|=r`,
the sets `C`, `B`, and `{x}` are pairwise disjoint, and the syndrome is
`sum_(y in C) Phi_w(y)+2 Phi_w(x)-sum_(z in B) Phi_w(z)=s`.  Splitting the
added point into genuine, positive-repeat, and cancellation cases gives the
pointwise identity

```text
D_r = r omega_(r,r) + kappa_r^+ + h_r omega_(r-1,r-1).   (P-rec)
```

The exact scalar mass match and centered remainder are

```text
b_r = (2r-1)/n,
K_r = kappa_r^+ + h_r omega_(r-1,r-1) - b_r D_r.          (P0)
```

Indeed,

```text
||C_r||_1=n binom(n,r-1),       ||kappa_r||_1=(r-1) binom(n,r-1),
||D_r||_1=n T_r,                ||kappa_r^+ + h_r omega_(r-1,r-1)||_1
                                  =(2r-1) T_r.
```

Thus `a_r` and `b_r` are forced by total mass, so these are the unique scalar
mass-matched centerings.

## Single centered norm

Put `M_r=binom(n,r)`.  Injectivity (R3) gives

```text
|im nu_r| = M_r,                 ||nu_r||_2^2 = M_r,
```

with singleton realized fibers.  The support of `C_r` has two disjoint
sectors:

```text
sector                 count                   E_r value
genuine r-set          M_r                     -a_r r
one positive repeat    (r-1) M_(r-1)           1-a_r.
```

Therefore

```text
||E_r||_2^2
  = M_r (a_r r)^2 + (r-1) M_(r-1) (1-a_r)^2,              (S1)

||E_r||_2^2 / (r^2 ||nu_r||_2^2)
  = a_r^2 + (r-1)(n-r+1)/(r n^2).                         (S2)
```

For any sequence `r/n -> delta in (0,1)`, (S2) gives

```text
||E_r||_2 / (r ||nu_r||_2) -> delta.                      (S3)
```

Because `|im nu_r|=M_r`, this is exactly the realized-image source scale.
Thus the uniform scalar claim

```text
||kappa_r-a_r C_r||_2 = o(r ||nu_r||_2)
```

is false on a positive-density raw source family.

## Signed-pair centered norm

Put

```text
M_r_pm  = binom(n,r) binom(n-r,r),
N_r^0  = binom(n,r-1) binom(n-r+1,r-1),
g_r    = n-2r+1,
c_r    = 1-b_r = g_r/n.
```

The identities

```text
r M_r_pm = g_r T_r,                 h_r N_r^0 = r T_r    (P-id)
```

will be used below.  Again (R3) gives singleton realized fibers:

```text
|im omega_(r,r)| = M_r_pm,          ||omega_(r,r)||_2^2 = M_r_pm.
```

There are exactly three mutually disjoint sectors:

```text
sector                 count                  K_r value
genuine signed pair    M_r_pm                 -b_r r
positive repeat        (r-1) T_r              c_r
cancellation           N_r^0                  c_r h_r.
```

Hence

```text
||K_r||_2^2
  = M_r_pm (b_r r)^2
    + (r-1) T_r c_r^2
    + N_r^0 (c_r h_r)^2,                                      (P1)

||K_r||_2^2 / (r^2 ||omega_(r,r)||_2^2)
  = b_r^2 + (r-1)g_r/(r n^2) + g_r h_r/n^2.                  (P2)
```

If `r/n -> delta in (0,1/2)`, then

```text
||K_r||_2 / (r ||omega_(r,r)||_2)
  -> sqrt(4 delta^2 + (1-2 delta)^2).                         (P3)
```

Thus the pair scalar mass match also has a leading, rather than `o(1)`,
centered remainder at realized-image scale.

## Exact triangle defect

Normalize

```text
rho_r     = omega_(r,r) / M_r_pm,
q_r       = D_r / (n T_r),
epsilon_r = K_r / (r M_r_pm).
```

Equations (P-rec), (P0), and (P-id) give the exact recursion

```text
rho_r = q_r - epsilon_r.                                     (T0)
```

Let

```text
A_(n,r) = (r-1)g_r/(r n^2),
B_(n,r) = g_r h_r/n^2.
```

The sector calculation gives

```text
||q_r||_2^2       / ||rho_r||_2^2 = c_r^2 + A_(n,r)+B_(n,r),
||epsilon_r||_2^2 / ||rho_r||_2^2 = b_r^2 + A_(n,r)+B_(n,r), (T1)

<q_r,epsilon_r> / ||rho_r||_2^2
  = -b_r c_r + A_(n,r)+B_(n,r).                              (T2)
```

Consequently the exact norm-only triangle factor is

```text
F_(n,r)
 = (||q_r||_2+||epsilon_r||_2)/||rho_r||_2
 = sqrt(c_r^2+A_(n,r)+B_(n,r))
   + sqrt(b_r^2+A_(n,r)+B_(n,r)) > 1.                        (T3)
```

At fixed pair density it converges to

```text
F(delta)
 = sqrt(2)(1-2 delta)
   + sqrt(4 delta^2+(1-2 delta)^2) > 1.                      (T4)
```

To see the strict inequality, put `c=1-2 delta`.  If `c >= 1/sqrt(2)`,
the first summand is at least one.  Otherwise `1-sqrt(2)c>0`, and

```text
(1-c)^2+c^2 - (1-sqrt(2)c)^2 = 2c(sqrt(2)-1) > 0.
```

For example, `F(1/3)=(sqrt(2)+sqrt(5))/3 > 1.21`.  On every compact
subinterval of `(0,1/2)`, the defect is bounded away from one.  Iterating a
norm-only triangle step through linearly many such levels therefore incurs an
`exp(Omega(n))` loss, not an `exp(o(n))` loss.

The signed covariance in (T2) is leading and is exactly what restores

```text
||rho_r||_2^2
 = ||q_r||_2^2 + ||epsilon_r||_2^2
   - 2 <q_r,epsilon_r>.
```

The route cut is specifically against discarding this covariance and treating
the centered remainder as scalar norm-small.

## Exact remaining wall

The single recursion is

```text
r nu_r = (1-a_r) C_r - E_r,
```

so its exact quadratic identity is

```text
r^2 ||nu_r||_2^2
 = (1-a_r)^2 ||C_r||_2^2
   + ||E_r||_2^2 - 2(1-a_r) Re <C_r,E_r>.                   (W1)
```

Likewise

```text
r omega_(r,r) = (1-b_r) D_r - K_r
```

gives

```text
r^2 ||omega_(r,r)||_2^2
 = (1-b_r)^2 ||D_r||_2^2
   + ||K_r||_2^2 - 2(1-b_r) Re <D_r,K_r>.                  (W2)
```

Therefore the first surviving target is realized-image control of the signed
quadratic combinations in (W1) and (W2), not separate smallness of `E_r` or
`K_r`.  In Fourier variables the full single remainder is

```text
Ehat_r
 = sum_(j=2)^r (-1)^j tau_j nuhat_(r-j)
   - a_r tau_1 nuhat_(r-1).                                 (W3)
```

Every higher-dilate Newton term remains in (W3).  Any positive covariance
argument must combine the full signed expression with its cross term before
taking absolute values.

## Finite replay

For

```text
n=7, p=14197, g=1054, r=3,
D={1,1054,3550,7889,9761,9466,10870},
```

the verifier checks all `12,328` coefficient vectors in `C_7`, proves their
first-coordinate residues are distinct, and replays (S-rec) and (P-rec)
pointwise for both `w=2` and `w=3`.  It obtains the exact rational values

```text
||E_3||_2^2 = 330/7,              ||K_3||_2^2 = 5820/7.
```

## Nonclaims

- This does not close the asymptotic or finite RS-MCA ledger.
- This does not refute a signed-covariance or multi-sector recursion.
- This does not place the construction in the shallow regime
  `w log p=o(n)`.
- This does not prove survival as a primitive first-match residual.
- Singleton realized fibers do not provide ambient FI, MI+MA, A4, or C9 here.
- No deployed CAP25 v13, M31, or KoalaBear row is changed.
- No stable paper TeX is changed.
