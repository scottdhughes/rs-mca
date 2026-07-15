# Reduced-CRT rank dichotomy for the `(3,2,3,(2,2,1))` frontier

**Status:** PROVED-LOCAL / fresh independent GREEN / BANKED. The symbolic
statement, exact `GF(19)` census, representative Python/Singular/Macaulay2
controls, and complete ledger replay are frozen. Two fresh read-only reviewers
returned ledger authorization YES, and an independent `GF(11)` falsifier found
no counterexample. This closes only the named row; the global mixed-petal
program remains YELLOW.

## Frozen statement

Let `k` be a field. Let `R,B_1,B_2,B_3 in k[X]` be monic, with

\[
\deg R=2,\qquad \{\deg B_1,\deg B_2,\deg B_3\}=\{2,2,1\}.
\]

Assume that the `B_i` are pairwise coprime and that
`gcd(R,B_1B_2B_3)=1`. Put

\[
B=B_1B_2B_3=X^5+b_4X^4+b_3X^3+b_2X^2+b_1X+b_0.
\]

For distinct nonzero labels `c_1,c_2,c_3`, let `G` be the unique residue
class modulo `B` satisfying

\[
G\equiv c_iR^{-1}\pmod{B_i},\qquad
G=g_4X^4+g_3X^3+g_2X^2+g_1X+g_0.
\]

For

\[
F=X^3+f_2X^2+f_1X+f_0,
\]

let `K(F)` be the `X^2,X^3,X^4` coefficient vector of `FG mod B`. Then

\[
K(F)=M(f_0,f_1,f_2)^T+u,
\]

where

\[
M=
\begin{pmatrix}
g_2&-b_2g_4+g_1&b_2b_4g_4-b_2g_3-b_1g_4+g_0\\
g_3&-b_3g_4+g_2&b_3b_4g_4-b_3g_3-b_2g_4+g_1\\
g_4&-b_4g_4+g_3&b_4^2g_4-b_4g_3-b_3g_4+g_2
\end{pmatrix}
\]

and

\[
u=
\begin{pmatrix}
-b_2b_4^2g_4+b_2b_4g_3+b_2b_3g_4+b_1b_4g_4-b_2g_2-b_1g_3-b_0g_4\\
-b_3b_4^2g_4+b_3b_4g_3+b_3^2g_4+b_2b_4g_4-b_3g_2-b_2g_3-b_1g_4+g_0\\
-b_4^3g_4+b_4^2g_3+2b_3b_4g_4-b_4g_2-b_3g_3-b_2g_4+g_1
\end{pmatrix}.
\]

The divided fixed-syndrome equations are

\[
RV-c_iF=B_iA_i,\qquad
\deg V\le1,\qquad
\deg A_i\le3-\deg B_i.
\]

Their fixed-`F` coefficient matrix has shape `12 x 9` and rank nine. After
adjoining the three lower coefficients of monic `F`, the moving matrix has
shape `12 x 12`, and

\[
\operatorname{rank}C=9+\operatorname{rank}M,
\qquad
\operatorname{rank}[C\mid b]=9+\operatorname{rank}[M\mid-u].
\]

The moving system has the following dichotomy.

1. If `rank M=3`, then at most one monic cubic `F` is compatible with the
   fixed support pattern.
2. If `rank M<3` and `rank[M|-u]>rank M`, the affine system is empty.
3. If `rank M<3` and `rank[M|-u]=rank M`, every monic solution pair
   `(F,V)` has `deg gcd(F,V)>0`.

For the profile interpretation, impose the additional hypotheses that the
evaluation blocks are pairwise disjoint, the core `C` consists of four
distinct field points, `R` is the locator of the two retained background
agreements, and let the received word `U` be zero on the core and background
and equal `c_iL_C` on labelled petal `i`. Let the explaining polynomial `P` have degree
less than five, and let `B_i=L_{S_i}` for its exact selected agreement set
`S_i` in petal `i`. If `h` is the unique restored core point, put

\[
D=C\setminus\{h\},\qquad F=L_D,\qquad H=L_C/F=X-h,
\qquad V=FG\bmod B,\qquad P=W=RHV.
\]

Then a compatible rank drop supplies a common root `alpha in D` of `F` and
`V`. Hence `W(alpha)=0=U(alpha)`, so the actual missed core is

\[
D\setminus Z(V)
\]

and has size at most two. Thus compatible rank drop is empty in the exact
`d=3` profile. Full rank contributes at most one exact codeword per canonical
support pattern.

## Proof

### Exhaustivity and the fixed matrix

Let `P` be an exact target codeword polynomial. The received word is zero at
the two background agreements and at the unique core agreement `h`. Since the
blocks are disjoint, these are three distinct roots of `P`; therefore

\[
P=RHV,\qquad \deg V\le1.
\]

For the selected agreement set `S_i` in labelled petal `i`, let
`B_i=L_{S_i}`. On `S_i`, the received word is `c_iL_C=c_iHF`, whereas
`P=RHV`. Since `H` has no petal root, division by `H` gives

\[
RV-c_iF=0\quad\text{on }S_i.
\]

Thus `B_i | (RV-c_iF)`, with quotient degree at most `3-deg B_i`. Every exact
target therefore enters the displayed fixed-syndrome system.

For the associated homogeneous fixed-`F` system, every `B_i` divides `RV`.
Pairwise coprimality gives `B | RV`; since `gcd(B,R)=1`, it follows that
`B | V`. But `deg B=5` and `deg V<=1`, so `V=0`, and then each `A_i=0`.
The nine fixed columns are independent. Hence the `12 x 9` fixed matrix has
rank nine over every field satisfying the stated locator hypotheses.

The CRT congruences are

\[
V\equiv FG\pmod{B_i}\quad(i=1,2,3).
\]

Because `deg V<=1` and `deg B=5`, they are equivalent to vanishing of the
`X^2,X^3,X^4` coefficients of `FG mod B`. Reduction of the four basis
elements `G,XG,X^2G,X^3G` modulo `B` gives the displayed `M,u`. Eliminating
the nine full-rank fixed columns gives the two rank identities above.

### Compatible rank drop forces a common factor

Assume that the moving system is compatible and rank deficient. Choose a
monic solution `(F,V,A_i)` and a nonzero homogeneous affine direction
`(F_0,V_0,A_{i,0})`. Because the leading coefficient of `F` was fixed to one,

\[
\deg F_0\le2,\qquad \deg V_0\le1.
\]

Also `F_0` is nonzero: if `F_0=0`, the direction would lie in the homogeneous
fixed-`F` system, whose kernel was just proved to be zero.

Modulo every `B_i`, the solution and its direction satisfy

\[
RV\equiv c_iF,\qquad RV_0\equiv c_iF_0.
\]

After cross multiplication and subtraction,

\[
B_i\mid R(VF_0-V_0F).
\]

The `B_i` are pairwise coprime and `gcd(B,R)=1`, so

\[
B\mid VF_0-V_0F.
\]

But

\[
\deg(VF_0-V_0F)\le4<5=\deg B.
\]

Therefore `VF_0=V_0F` as a polynomial identity. If `gcd(F,V)=1`, Euclid's
lemma gives `F | F_0`. This is impossible because `F` is monic of degree
three, `F_0` is nonzero, and `deg F_0<=2`. Consequently
`deg gcd(F,V)>0`. (The case `V=0` is itself impossible: the original
congruences would give `B | F` with `deg B=5>3`.)

### Pointwise profile migration

For an actual target locator `F=L_D`, split squarefreeness implies that a
nonconstant common factor of `F` and `V` contains `X-alpha` for some
`alpha in D`. In particular `alpha!=h`. Since `V(alpha)=0` and the received
word is zero on the core,

\[
W(\alpha)=R(\alpha)H(\alpha)V(\alpha)=0=U(\alpha).
\]

More precisely, background/core disjointness gives `R(x)!=0` for `x in D`,
and distinctness of the core gives `H(x)!=0`. Thus

\[
W(x)=U(x)=0\quad\Longleftrightarrow\quad V(x)=0
\qquad(x\in D).
\]

The actual missed core is `D\setminus Z(V)`. Since `deg V<=1` and it shares
at least one root with `F`, at least one point of `D` is restored and the
missed core has size at most two. A compatible rank drop cannot realize exact
`d=3`.

### Canonical-pattern disjointness

An exact word in this profile uniquely determines both background agreements,
the labelled petal agreement sets of sizes `(2,2,1)` in some order, and its
restored core point. The cofactor key omits only the restored core point.
There are

\[
3\binom42^2\binom41=432
\]

canonical keys. The full-rank bound is on all monic cubics for one key, hence
on all four possible restored core points together; there is no extra factor
four. Rank drop contributes no exact target. Therefore the candidate uniform
bound is at most one exact word per key, or `432` for the row.

## Exact controls

The owner certificate first checks all 432 canonical keys in the frozen order.
All 432 remain `UNPAID_PRIMITIVE`; twelve periodic full-support refinements are
recorded, but none pays its aggregate `q^2` key. Auxiliary Johnson has margin
`-11`, global Johnson misses by one, and B11 returns
`ESCAPES_BOUNDED_EXCESS_BOX`. The existing-owner audit therefore leaves the
banked `513,283` ledger unchanged.

The Sage census derives the symbolic `M,u`, verifies the affine identity, and
checks all 432 frozen `GF(19)` patterns. It finds

```text
fixed A: rank 9 on all 432 patterns
moving (rank C, rank[C|b]):
  408 x (12,12)
   23 x (11,12)
    1 x (11,11)
reduced (rank M, rank[M|-u]):
  408 x (3,3)
   23 x (2,3)
    1 x (2,2)
all 1,728 actual missed-core locators: (rank A,rank[A|b_F])=(9,10)
exact target words: 0 by both the incidence census and the full decoder
```

The unique compatible ambient chart has

\[
(S_1,S_2,S_3)=(\{5\},\{8,11\},\{14,15\}),
\]

and its 19-point affine line is

\[
V=18(X+t),\qquad F=(X+t)(X^2+16).
\]

Thus every point visibly has the forced common factor. The quadratic factor
is irreducible over `GF(19)`, so this frozen line contains no actual split core
locator.

An independent Python implementation rebuilds all 432 reduced maps. Singular
and Macaulay2 then reproduce representative full-rank, affine-inconsistent,
and compatible ranks and minors, and independently verify the displayed
factorization. The localization is only by explicit nonzero root differences
and distinct nonzero label factors; generic saturation is not used.

The certificates are:

- `experimental/data/certificates/l1-b9-frontier-32221-owner-partition/certificate.json`
- `experimental/data/certificates/l1-b9-frontier-32221/certificate.json`
- `experimental/data/certificates/l1-b9-frontier-32221/cas_certificate.json`
- `experimental/data/certificates/l1-b9-frontier-32221/ledger_certificate.json`

## TheoremSearch check

After the compatibility statement was frozen, targeted TheoremSearch queries
returned rational-interpolation uniqueness analogues, including Proposition
2.1 of Claeys--Wielonsky (arXiv:1112.2887), Theorem 5.1 of
Cortadellas Benitez--D'Andrea--Montoro (arXiv:1808.02575), and a general
rank-two syzygy-module statement in Theorem 4.2 of Vidunas--Kitaev
(arXiv:0810.2766). None directly
states the finite-field degree-five CRT rank-drop implication above. No
literature theorem is imported into this proof; the load-bearing step is the
elementary degree gap and Euclid's lemma.

## Banked ledger consequence

The fresh proof and certificate reviewers both returned GREEN with ledger
authorization YES. A dedicated ledger verifier reconstructs the complete
post-31222 profile list, validates all 432 canonical assignments, and applies
exactly this local replacement:

\[
432\cdot19^2=155{,}952
\]

by `432`, a saving of `155,520`. The mutation-tested banked totals are

```text
all-profile add-back: 1,348,447 -> 1,192,927
unresolved mass:        513,283 ->   357,763
```

The new largest unresolved row is

\[
(\ell,d,r,t,(a_i))=(4,4,1,3,(3,3,1)),\qquad (G_2,G_R)=(2,4),
\]

with 384 support patterns and charge `384*19^2=138,624`. Positive unresolved
mass remains.

## Reproduction

```bash
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_owner_partition.py
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_owner_partition.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_frontier_32221.sage
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_frontier_32221.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_cas.py
python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_cas.py --tamper-selftest
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_ledger.py
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_ledger.py --tamper-selftest
```

No `m>2`, PR `#763`, Lean, commit, or GitHub action is authorized by this
local packet.
