# L1 mixed-petal residual-frontier ledger

Status: **AUDIT / EXPERIMENTAL**
Date: 2026-07-14
Scope: finite B7--B11 bookkeeping, exact tiny-case falsification, and one
compressed-support incidence census. No theorem is promoted.

## Question

Before introducing a new mixed-petal mechanism, determine what follows from
the proved cofactor injections and B7--B11 gates alone. For each admissible
finite profile, the diagnostic ledger charges

```text
support-pattern count * q^(d-a_max+1)                    (b=0),
support-pattern count * q^max(0,d-max(r,a_max)+1)        (b>0 maximal).
```

The first exponent is Lemma 17. The second is the stronger background-anchor
exponent from Lemma B3. The profile count includes the exact choices of
background support, labelled touched petals, assignments of repeated hit
sizes to those petals, and point subsets inside each petal. It does **not**
include `binom(k-1,d)`: the fixed-pattern cofactor map is injective across the
missed-core locator once `d` is fixed.

## Exact finite ledger

The deterministic verifier is
`experimental/scripts/verify_l1_mixed_petal_frontier_ledger.py`; its frozen
JSON output is under
`experimental/data/certificates/l1-mixed-petal-frontier-ledger/`.
It enumerates all non-planted size profiles with `t>=2`, enforces

```text
lambda = r + sum_i a_i - (ell+d) >= 0,
a_i <= min(ell,d),
the two B8 width floors,
the B9 finite-width inequality,
the B10 Johnson gate,
and the B11 (E,V2,VR) finite-box partition.
```

All arithmetic is exact integer or rational arithmetic. The two frozen rows
give:

| row and fixed cuts | profiles | support patterns | unresolved injection upper-bound mass | verdict |
|---|---:|---:|---:|---|
| `(q,n,k,sigma)=(97,16,8,2)`, `(E,V2,VR)=(0,0,0)` | 16 | 295 | 8,819,919 | needs new structure |
| `(q,n,k,sigma)=(17,16,8,1)`, `(E,V2,VR)=(0,1,1)` | 60 | 945 | 15,402,000 | needs new structure |
| `(q,n,k,sigma)=(17,16,6,1)`, `(E,V2,VR)=(0,0,0)` | 102 | 5,312 | 47,416,332 | needs new structure |

The first row's unresolved mass splits as `267,138` in the bounded-excess
box and `8,552,781` beyond the fixed excess cut. The second splits as
`20,264` and `15,381,736`. These are upper bounds over support profiles, not
realizability counts. The third row splits as `90,848` and `47,325,484`.
In particular, nonzero mass is not evidence for a codeword or a counterexample.

The exact B11 union bounds on the paid boxes are `28,243`, `167,058`, and
`3,066`, respectively. The certificate explicitly records that no asymptotic
family,
`q=poly(n)` hypothesis, L1 lower-cutoff hypothesis, or uniform fixed-threshold
claim is supplied by these two rows.

**Finite-ledger conclusion:** B7--B11 plus the fixed-support cofactor charge do
not close even these toy profile boxes. This is only a gate on that inequality
package: another already-proved owner may still pay a profile, as the
compressed template below demonstrates.

## Scanner extension and exact paid/unpaid fixtures

`experimental/scripts/scan_l1_full_list_quotient_conjecture.py` now emits, for
every exact sunflower extra and before example truncation,

```text
d-ell, G2, GR, t, r, (a_i), lambda, lambda_J, lambda-lambda_J,
the finite (E,V2,VR) box class, the fixed-(D,R_0) auxiliary Johnson
margin, and the first known owner.
```

The helper rejects records violating the theorem-domain identities
`r<ell` (maximal case), `a_i<=d`, or
`lambda=r+sum(a_i)-(ell+d)`. A single finite row is never labelled as a
quantity "tending to infinity." The regression verifier preserves the old
sample/sweep JSON after deleting the append-only `b11_*` fields; the frozen
legacy projection hashes are

```text
sample: 9061192619990d74224005c55572727935d141f680279a9f3bb4f12e7cb99864
sweep:  76048db2e50c7009b752cadcd626896b776dbffe95aa01ca99488732a736472c
```

An exact support-subset decode of the sequential sunflower at
`(p,n,k,s)=(17,16,8,10)` gives 19 listed codewords, of which 16 are extras:

```text
13  ESCAPES_BOUNDED_EXCESS_BOX
 1  ESCAPES_BY_COFACTOR_EXCESS
 1  FULL_PETAL_SEPARATE
 1  PAID_JOHNSON
```

Fourteen extras are low under the **global B10** Johnson gate and
mixed-petal. Seven have the single sorted profile

```text
(d,r,t,a_i,lambda-lambda_J) = (2,0,3,(2,2,1),-1),
d-ell=-1, G2=2, GR=4.
```

They are not genuine residuals after all known owners: for every one of the
fourteen, the fixed-layer auxiliary compiler has

```text
a = sigma+d+1-r,       |T|=M(sigma+1),       a^2>|T|d,
```

so all fourteen route to `PAID_AUXILIARY_JOHNSON`.

A second exact, non-random fixture lies beyond that auxiliary-Johnson
boundary. At
`(p,n,k,s)=(17,16,6,7)`, the maximal sequential sunflower has `ell=2`,
`M=5`, and one background point. Exact support-subset decoding gives 452
listed codewords and 447 extras. At the deliberately sharp diagnostic cuts
`(E,V2,VR)=(0,0,0)`, eleven are full-petal separate and 436 remain
`UNPAID_B11_RESIDUAL` after the global Johnson, auxiliary Johnson, B7, and
exact cyclic-support stabilizer checks. All 436 have stabilizer order one.
This does not exclude every possible quotient descent. This is a
zero-cut fixture, not an absolute owner statement. The largest
bounded-excess `d=2,r=0` compressed target has exactly 59 solutions with

```text
(d,r,t,a_i)=(2,0,3,(2,1,1)),
d-ell=0, G2=1, GR=2, lambda-lambda_J=-2,
a_aux=4, |T|=10, a_aux^2-|T|d=-4.
```

This `(2,1,1)` stratum is the first genuine exact zero-cut frontier template.
Its exact support-pattern count is

```text
binom(1,0) * binom(5,3) * 3 * binom(2,2) * binom(2,1)^2 = 120,
```

and Lemma B3 gives exponent `d-max(r,a_max)+1=1`, hence the present ledger
bound `120*17=2,040`, compared with 59 realized codewords. At the first
positive two-petal cut `V2=1`, all 59 instead route to the existing
`PAID_B11_G2` owner.

## Compressed incidence census for the paid `(2,2,1)` template

For every labelled assignment of `(2,2,1)`, every missed-core pair `D`, and
every compatible support tuple, set `F=L_D` and impose

```text
W - c_i F = L_{S_i} A_i,                  c_i in {1,2,3},
deg W <= 2,                               deg A_i <= 2-|S_i|.
```

There are exactly

```text
3 * binom(7,2) * binom(3,2)^2 * binom(3,1) = 1,701
```

labelled fixed-support systems. Sage 10.9, Singular 4.4.1, and Macaulay2
1.26.06 independently give the same census:

```text
rank(A)=7, rank([A|b])=7:       7 systems (unique solutions)
rank(A)=7, rank([A|b])=8:   1,694 systems (inconsistent)
rank(A)<7:                      0 systems
```

The Sage reconstruction verifies exact agreement on all 16 coordinates and
agrees with the exhaustive support-subset decoder on all seven masks. The
seven solutions are distinct and have cyclic stabilizer order one. The sharp
fixed-layer auxiliary Johnson compiler is Corollary
`cor:v13-pma-johnson` in
`experimental/lean/cs25_cap_v13_experimental/cap25_v13_experimental.tex`;
it gives

```text
a=5, |T|=9, d=2, a^2-|T|d=7,
floor(|T|(a-d)/(a^2-|T|d)) = floor(27/7) = 3
```

per fixed `(D,R_0)` layer. Therefore:

- the rank-deficient component is empty for this template;
- the seven surviving solutions lie in full-rank fixed-support strata;
- none is globally B10-Johnson-paid (`lambda=0<lambda_J=1`);
- none is paid by the exact cyclic-support stabilizer owner;
- none is paid at the finite cuts `V2=VR=0`;
- all seven are paid by the fixed-`D,R_0` auxiliary Johnson owner.

Thus the rank-deficient-component question is vacuous for this template, and
the full-rank survivors route to an already-paid owner. The load-bearing
transcripts are frozen in
`experimental/data/certificates/l1-mixed-petal-template-221/certificate.json`;
the independent CAS verifier is
`experimental/scripts/verify_l1_mixed_petal_template_221_cas.py`.

## Uniform rank calculation for the zero-cut `(2,1,1)` template

The exact `(17,16,6,7)` row has a five-point core, five disjoint two-point
petals, and one background point. For a missed-core pair `D`, let

```text
F=L_D,                B_f=(X-u)(X-v),
S_j={gamma},          S_k={delta},
Delta_j=c_j-c_f,      Delta_k=c_k-c_f.
```

The compressed equations are

```text
W-c_f F = B_f A_f,
W-c_j F = (X-gamma) A_j,
W-c_k F = (X-delta) A_k,
```

where `A_f` is constant and `A_j,A_k` are linear. They give a `9 x 8`
full coefficient system. Eliminating `W` gives a `6 x 5` pairwise-difference
system. After permuting the three blocks so the full support comes first, a
maximal minor of either coefficient system is

```text
B_f(delta) = (delta-u)(delta-v).
```

This is nonzero because the petals are disjoint. Hence the rank-deficient
component is **empty uniformly on every valid disjoint `(2,1,1)` chart**.
This conclusion is algebraic, not an extrapolation from the tiny scan.

Consistency is the single augmented-determinant equation

```text
Delta_j F(gamma) B_f(delta) = Delta_k F(delta) B_f(gamma).
```

For `F=X^2+f1 X+f0`, this is an affine line in `(f0,f1)`. Thus the residual
object is a moving-support compatibility incidence, not a low-rank
determinantal component.

There are `120` outside-core support templates and `binom(5,2)=10` core-pair
choices. The exact Sage census and independent Singular/Macaulay2 verifier
agree on all `1,200` systems:

```text
rank(A)=8, rank([A|b])=8:      76 systems (unique)
rank(A)=8, rank([A|b])=9:   1,124 systems (inconsistent)
rank(A)<8:                      0 systems
```

Seventeen of the 76 unique candidates have extra agreements: fifteen gain an
agreement on an untouched petal and two gain the background point. The
remaining 59 have exact `(2,1,1),r=0` support, match the exhaustive decoder,
and have stabilizer one. Across the 120 outside templates, 70 realize no
exact mask, 41 realize one, and nine realize two. The 120 templates define 93
distinct compatibility lines, with line-multiplicity histogram
`70 x 1, 21 x 2, 2 x 4`.

Cyclic stabilizer one rules out only that exact scanner owner; it does not
exclude every possible quotient-descent mechanism.

The frozen transcript is
`experimental/data/certificates/l1-mixed-petal-template-211/certificate.json`.
The generators are
`experimental/scripts/analyze_l1_mixed_petal_template_211.sage` and
`experimental/scripts/verify_l1_mixed_petal_template_211_cas.py`.
Both CAS paths also verify the universal maximal-minor identity. Therefore:

- no quotient-descent or periodicity classification is needed for a
  rank-deficient component here, because that component is empty;
- the 59 exact solutions are full-rank and injective per fixed support;
- at `(E,V2,VR)=(0,0,0)` they are a valid unpaid diagnostic fixture;
- at `V2>=1` they are already paid by B11's `G2=1` owner;
- the next theorem-discovery target must have genuinely escaping B11
  coordinates, rather than merely surviving a zero cutoff.

## The B9-boundary `(2,2,2)` chart at `m=2`

This attack is restricted to the single profile

```text
ell=d=4,       r=2,       t=3,       a_i=(2,2,2).
```

It has `lambda=0`, `G2=GR=4`, B8 widths `(3,3)`, and B9 at equality. A
sequential layout is numerically feasible when

```text
K=k-1 >= 4,       M>=3,       2<=b<4,
n=K+4M+b,         s=K+4.
```

The fixed-layer auxiliary square is `a_aux^2-Nd=36-16M<0`, so that owner
does not pay this chart. These are gate calculations only. They do not
produce a compatible codeword family, and no statement for `m>2` is made.

### Correct full system at `m=2`

Set `m=2`. Let `F=L_D` be the monic quartic missed-core locator, `R` the
quadratic retained-background locator, and `B_i` the three quadratic selected
petal locators. Assume throughout this chart that all locator roots are
distinct across locators and that the three petal labels `c_i` are nonzero
and distinct. Writing `W=RV`, the actual fixed-support equations are

```text
R V - B_i A_i = c_i F,             i=1,2,3,
deg V, deg A_i <= 2.
```

Coefficient comparison gives a `15 x 12` system. It has rank 12 uniformly
when `R,B_1,B_2,B_3` are pairwise coprime: a homogeneous solution would give
one degree-at-most-four polynomial

```text
H=RV=B_1A_1=B_2A_2=B_3A_3
```

divisible by the degree-eight product `R B_1 B_2 B_3`, hence `H=0`. The
earlier `10 x 9` pairwise-difference system also has full column rank, but it
omits `R|W` and is not the load-bearing compatibility test.

Let the six selected support points be `z`, with the appropriate petal label
`c(z)`. The full system is compatible exactly when

```text
[ R(z), z R(z), z^2 R(z), c(z) F(z) ]
```

has rank at most three. Choosing `x11,x12,x21` as interpolation anchors gives
three affine-linear equations in `(f0,f1,f2,f3)` for

```text
F=X^4+f3 X^3+f2 X^2+f1 X+f0.
```

The anchor determinant is exactly

```text
R(x11)R(x12)R(x21)
  (x12-x11)(x21-x11)(x21-x12),
```

so this reduction is valid on the disjoint chart. The three residual
polynomials have `(degree,terms)`

```text
(11,1132), (12,1458), (12,1458).
```

The four `3 x 3` coefficient-rank minors share a frozen structural factor.
After exact division by that factor, their residual `(degree,terms)` data,
ordered by the deleted coefficient `(f0,f1,f2,f3)`, are

```text
(12,1212), (11,2060), (10,2446), (9,1632).
```

The expanded-polynomial hashes, rather than the expansions themselves, are
frozen in
`experimental/data/certificates/l1-b9-boundary-222/certificate.json`.
This is an exact localization identity. A generic Gröbner saturation in the
coefficient-locator presentation timed out in both Singular and Macaulay2,
so no completed generic saturation or primary decomposition is claimed.

### Compatible rank drop forces a degree-two quotient template

Let `C` be the resulting `3 x 4` homogeneous compatibility matrix. Its kernel
consists of pairs `(Q,G)` with

```text
deg Q<=2,       deg G<=3,       R(z)Q(z)=c(z)G(z)
```

at all six support points. If `rank(C)<=2`, take two independent kernel
pairs. Then

```text
Q_1 G_2-Q_2 G_1
```

has degree at most five and six distinct roots, so it vanishes identically.
Write all kernel pairs as

```text
(Q,G)=h(A,B),       gcd(A,B)=1.
```

Put `a=deg A`, `b=deg B`, and

```text
h_max=min(2-a,3-b).
```

If `T` is the set of support points where `RA-cB` is nonzero, every allowed
multiplier `h` vanishes on `T`. The multiplier space has dimension at least
two, while degree-at-most-`h_max` polynomials vanishing on `T` have dimension
at most `h_max+1-|T|`. Hence `h_max<=2` and `|T|<=h_max-1`. If `h_max=2`,
then `deg A=0`, `deg B<=1`, and at most one support point is a common base
point. For any compatible monic quartic
`F`, the polynomial `VB-AF` then has degree at most four and at least five
roots. It is zero, forcing `deg V>=3`, a contradiction. Hence the multiplier
degree bound is one; the same dimension inequality gives `T` empty, and

```text
R(z)A(z)=c(z)B(z)
```

at all six support points. Now `VB-AF` has degree at most five and six roots,
so it is identically zero. Since `B|F` and `deg V<=2`, degree comparison
forces

```text
deg A=0,       deg B=2,       F=B H,       V=A H.
```

Therefore every compatible rank-drop chart has a complete-fibre template for the
degree-two rational map `RA/B`: the background pair, the three selected
support pairs, and the quadratic factor of `F` are its fibres. When the
degree-two map is separable, its nontrivial deck transformation is the
corresponding projective involution. Moreover:

- `rank(C)=1` is affine-inconsistent for a monic quartic;
- compatible `rank(C)=2` has the displayed degree-two quotient template;
- `rank(C)=3` leaves an affine one-dimensional family, hence exactly `q`
  compatible ambient monic quartics per fixed `(R,B_1,B_2,B_3)` chart.

### Exactness removes the compatible rank-two component

The quotient-owner question is not the first gate for this exact profile.
Write the compatible rank-two factorization more distinctly as

```text
F=B_* H,       V=A H,       deg B_*=deg H=2,       A!=0.
```

The sunflower reduction defines `D` to be the **exact** missed core and gives

```text
P=L_{C\D} W,       W=R V,       F=L_D.
```

Since the normalized received word is zero on the whole core, exactness of
`D` requires `W` to be nonzero at every root of `F`, equivalently
`gcd(F,W)=1`. But on the disjoint split chart,

```text
W=A R H,       gcd(F,W)=H.
```

Thus the two roots of `H` are additional core agreements. The roots of `B_*`
remain missed because `A`, `R`, and `H` are nonzero there. The canonical exact
profile is therefore

```text
F_new=F/H=B_*,       W_new=W/H=A R,       d_new=2.
```

Cancelling `H` in the three incidence equations preserves the petal
agreements. Hence every compatible `rank(C)=2` template migrates from `d=4`
to `d=2`; it is **not** an exact member of the B9-boundary profile. This is a
profile-exactness argument and does not rely on treating an arbitrary rational
involution as a paid power or Chebyshev quotient.

The GF(13) structural census contains 24 split compatible rank-two locators.
All 24 have `deg gcd(F,W)=2`, all migrate to exact defect two, and none survives
the exact-`d=4` gate. The frozen migration transcript has SHA-256
`f964739fe0b0bb3443ff312fb33d66ed3625515b311ca8de0ef6408f44f0b18d`.

### Domain-compatible owner partition

The exact classifier
`experimental/scripts/verify_l1_b9_rank2_owner_classifier.py` keeps structural
descent separate from payment. For each compatible rank-two chart it derives
the canonical trace-zero matrix

```text
tau(x)=(a*x+b)/(c*x-a),
```

verifies that it swaps the retained-background pair and all three selected
petal pairs, and then applies the gates in this order:

```text
tau(D)=D with no poles and uniform two-point orbits;
declared retained POWER_C2 or CHEBYSHEV_T2 fold;
support descends;
both received words descend;
the explaining polynomial descends;
the natural quotient profile term is certified.
```

Only the final state is `PAID_BY_THEOREM`, with named owners
`prop:quotient-descent` and `prop:stabilizer-payment`. A domain-stable
rational involution that is not a declared power/Chebyshev deck map is emitted
as `UNPAID_RATIONAL_INVOLUTION_ONLY`.

The exact structural partitions are:

| field | compatible rank-two charts | terminal owner status |
|---:|---:|---|
| `GF(11)` | 18 | all `NO_RS_DOMAIN_SUPPLIED` |
| `GF(13)` | 49 | all `NO_RS_DOMAIN_SUPPLIED` |

All 67 records include the induced PGL2 matrix and are frozen by transcript
hashes. They are structural charts, not RS rows, so none is paid. In the actual
sequential `GF(19)` RS domain, the 216 charts split as 215 with
`rank(C)=rank([C|u])=3` and one with `(rank(C),rank([C|u]))=(2,3)`; hence there
is no compatible rank-two chart to route. A declared multiplicative power-fold
positive control reaches the named owner, while mutations of the domain, fold,
support, either received word, explainer, and quotient budget are all rejected.
The positive control validates the classifier; it is not a frontier witness.

### Certified moving-support upper charge at `m=2`

Only the rank-three stratum can contribute to the exact `d=4` target. For a
maximal sunflower row there are exactly

```text
binom(b,2) * binom(M,3) * binom(4,2)^3
  = 216 * binom(b,2) * binom(M,3)
```

choices of retained background pair, three touched petals, and their selected
pairs. For each such chart, rank three leaves exactly `q` ambient monic
quartics. No extra `binom(K,4)` factor is needed: the affine monic-`F` fibre
already ranges over all quartics, and valid split missed-core locators are a
subset of those `q` ambient points. Therefore

```text
# exact (d,r,a_i)=(4,2,(2,2,2)) targets
  <= 216 * binom(b,2) * binom(M,3) * q.
```

The prior fixed-pattern cofactor charge was the same support-chart count times
`q^3`, so the exact Padé conditions save `q^2`. The exact integer verifier
`experimental/scripts/verify_l1_b9_m2_full_rank_ledger.py` first replaces only
this one aggregate profile in the complete finite B7--B11 ledger.  It then
audits the next minimal-row profile against the already-proved fixed-`(D,R_0)`
auxiliary Johnson owner:

The v5 ledger now content-addresses the boundary-222 theorem certificate
before making this substitution. It checks the rigorous local chart status,
the core-recovery rank partition, the `216*binom(b,2)*binom(M,3)*q` formula,
and all three finite-row charges, then records the certificate SHA in every
refined target. Thus the `q^3 -> q` step is replayably linked to its
load-bearing theorem input rather than asserted only in this note.

| row `(q,n,K,M,b)` | target `q^3 -> q` | add-back after `m=2` | after existing owner | after local `(3,2,1)` | unresolved then | after 31222 CRT | unresolved after 31222 | after 32221 CRT | unresolved after 32221 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `(19,18,4,3,2)` | `1,481,544 -> 4,104` | `2,012,848` | `1,701,016` | `1,503,967` | `668,803` | `1,348,447` | `513,283` | `1,192,927` | `357,763` |
| `(23,22,4,4,2)` | `10,512,288 -> 19,872` | `319,781,380` | `319,781,380` | not applied | `264,893,536` | not applied | `264,893,536` | not applied | `264,893,536` |
| `(47,46,4,10,2)` | `2,691,092,160 -> 1,218,240` | `16,186,949,038,331,748` | `16,186,949,038,331,748` | not applied | `2,057,753,055,668,744` | not applied | `2,057,753,055,668,744` | not applied | `2,057,753,055,668,744` |

The last GF(19) substitution has passed the independent proof review recorded
in `experimental/notes/l1/l1_b9_boundary_321_independent_review.md`.  It is a
reviewed local ledger refinement, not a promotion to the global theorem.

Thus the `m=2` refinement is real but does not close any of the three complete
finite add-backs. The minimal exact decoder still realizes zero target
codewords; every displayed quantity is an upper bound, not a realizability
count.

Before the existing-owner pass, the minimal row's largest remaining aggregate
profile was

```text
(d,r,t,a_i)=(4,1,3,(3,2,2)),
(G2,GR)=(3,4),       lambda-lambda_J=-1,
support patterns=864,       current B3 charge=864*19^2=311,904.
```

Here the auxiliary petal domain has size `12` and the required agreement is
`a=7`, so the proved sharp Johnson margin is

```text
a^2-d|T|=49-48=1,
floor(|T|(a-d)/(a^2-d|T|))=36
```

per fixed `(D,R_0)` layer.  Since `K=d=4` and `(b,r)=(2,1)`, there are
`binom(4,4)binom(2,1)=2` fixed layers.  Thus this whole aggregate profile is
paid by `PAID_AUXILIARY_JOHNSON` with charge at most `72`, saving `311,832`.
For the `M=4` and `M=10` rows the corresponding margins are `-15` and `-111`,
so no auxiliary-Johnson payment is claimed there.

After this correction, the minimal row's largest remaining unresolved profile
is

```text
(d,r,t,a_i)=(4,2,3,(3,2,1)),
(G2,GR)=(3,3),       lambda-lambda_J=-1,
support patterns=576,       current B3 charge=576*19^2=207,936.
```

Its auxiliary margin is `6^2-4*12=-12`, so the next attack begins with its
other existing owners and only then forms a new fixed-support rank system.

The exact owner/rank packet
`experimental/scripts/analyze_l1_b9_boundary_321.sage` carries out those two
steps for the sequential `GF(19)` layout.  Among all `576` support patterns,
the exact cyclic-support stabilizer histogram is

```text
order 1: 573,       order 2: 3.
```

Thus periodicity pays only three patterns.  For every pattern the homogeneous
`15 x 12` coefficient matrix is injective over any field with the displayed
supports disjoint: a homogeneous solution would make the degree-`<=4`
polynomial `W=RV` divisible by the pairwise coprime product
`R L_{S_1}L_{S_2}L_{S_3}`, of degree `2+3+2+1=8`, hence `W=0` and all
cofactors vanish.  This proves rank `12`; it does not prove compatibility for
a prescribed missed-core locator.

For the actual core locator in the sequential `GF(19)` word, all `576`
systems have

```text
rank(A)=12,       rank([A|b])=13,
```

so the profile is empty in this fixture.  The independent exact decoder also
finds zero target codewords.  When the four lower coefficients of a moving
monic quartic `F` are adjoined, `574` patterns have full row rank `15` and
therefore exactly `19` ambient affine solutions each.  The remaining two have
`rank(C)=14` but augmented rank `15`, so they admit no monic quartic.  The
total ambient moving-`F` count is therefore `574*19=10,906`.
Python modular elimination, Singular, and Macaulay2 independently reproduce
`rank(C)=14, rank([C|b])=15` on both exceptional patterns.  With the monic
column scaled by `t`, their selected augmented maximal minors factor as
`10t` and `16t` in `GF(19)[t]`; Singular and Macaulay2 independently verify
both identities.  Localizing at the nonzero monic coefficient therefore makes
each representative inconsistency a unit obstruction.

These representative CAS factorizations are controls, not the proof and not a
claimed generic saturation.  After localizing only at the disjoint-locator resultants,
the nonzero labels, and the pairwise label differences, the CRT inverse
argument below shows directly that the affine-compatible rank-drop incidence
is empty.  Thus there is no compatible primitive component to factor or route;
generic saturation and primary decomposition are unnecessary and are not
claimed.

### Local `(3,2,1)` moving-quartic rank dichotomy

Status: **PROVED LOCAL LEMMA / INDEPENDENT REVIEW GREEN**.

Let `B_i=L_{S_i}` have degrees `(3,2,1)`, put `B=B_1B_2B_3`, and assume
`R,B_1,B_2,B_3` are pairwise coprime.  Assume also that the three petal labels
`c_i` are distinct and nonzero.  By CRT there is a unique polynomial `G` of
degree `<6` satisfying

```text
G = c_i R^(-1)  mod B_i.
```

The equations `RV-c_iF=B_iA_i` are compatible exactly when

```text
V = FG mod B,       deg V <= 2.
```

Thus the three compatibility equations are precisely the coefficients of
`X^3,X^4,X^5` in `FG mod B`.  They form a `3 x 4` linear map in the four lower
coefficients of the monic quartic `F`; the `X^4` coefficient of `F` is the
affine column.  Equivalently, if `A` is the universal `15 x 12` fixed-unknown
matrix and `C` is the original `15 x 16` moving-quartic matrix, then the three
rows are the compatibility equations obtained from the three-dimensional left
kernel of `A`, and

```text
rank(C)=rank(A)+rank(C_reduced)=12+rank(C_reduced).
```

Hence the original condition `rank(C)=15` is exactly reduced rank three.

If the lower-coefficient map has rank three, its affine fibre has size at most
`q`.  Suppose instead that its rank is at most two and a monic quartic is
compatible.  Then the full `3 x 5` map on all degree-`<=4` polynomials also has
rank at most two.  Since `G` is a unit modulo `B`, write
`J=G^(-1) mod B`.  The kernel is

```text
P_4 intersect J P_2   inside F[X]/(B).
```

It has dimension at least three, while `J P_2` has dimension exactly three;
hence `J P_2` is contained in `P_4`.  Write

```text
B=X^6+b_5X^5+...+b_0,       J=j_5X^5+...+j_0.
```

The `X^5` coefficients of `J`, `XJ mod B`, and `X^2J mod B` are

```text
j_5,
j_4-b_5j_5,
j_3-b_5j_4+(b_5^2-b_4)j_5.
```

Their vanishing gives `j_5=j_4=j_3=0`, so `deg J<=2`.  The compatible monic
quartic lies in the ordinary product `J P_2`, so it forces `deg J=2`.  If
`B_j` is the cubic support locator, then

```text
J = c_j^(-1) R  mod B_j.
```

Both sides have degree at most two, hence they are equal as polynomials.  For
either other positive-degree support locator `B_i`, the same congruence would
make `B_i` divide `(c_j^(-1)-c_i^(-1))R`, impossible because `c_i!=c_j` and
`gcd(B_i,R)=1`.  Therefore every rank drop is affine-inconsistent.  No new
unpaid component occurs under the printed hypotheses.

The verifier
`experimental/scripts/verify_l1_b9_boundary_321_dichotomy.sage` records the
three CRT equations, the symbolic triangular step, and exact normalized
finite-field falsification controls.  On the frozen GF(19) layout the three
periodic patterns route to the existing owner and the remaining 573 patterns
cost at most `573q=10,887`, replacing `207,936` in the post-periodic first-match
ledger.  The independently reviewed unresolved mass is therefore `668,803`.
The isolated all-pattern expression would be `3+573q=10,890`; the extra three
are absent from the residual ledger only because the periodic owner already
pays them.

Before the reduced-CRT refinement, the then-largest remaining profile was

```text
(d,r,t,a_i)=(3,1,3,(2,2,2)),
(G2,GR)=(4,5),       lambda-lambda_J=-1,
support patterns=432,       current B3 charge=432*19^2=155,952.
```

The independent review found no gap in the CRT kernel argument, verified every
domain/label hypothesis, and independently counted the three periodic support
patterns. The existing-owner audit and reduced-CRT attack described below were
then carried out. No `m>2` or PR `#763` work is authorized by this history.

The `121,502,836,610,262` cap from upstream PR `#763` is not a target for this
chart: that deployed row has `sigma+1=67,472`, whereas the local `m=2` chart
requires `sigma+1=4`. The verifier reproduces #763's conditional complete
add-back and margin `992` as a crosswalk, but marks the chart comparison
`INAPPLICABLE_TO_LOCAL_M2_CHART` rather than silently mixing the domains.

### Exact falsification controls

With the background normalized to `{0,1}`, exhaustive labelled-pair censuses
give:

| field | charts | rank 1 | rank 2 | rank 3 | monic-compatible rank 1 | monic-compatible rank 2 |
|---:|---:|---:|---:|---:|---:|---:|
| `GF(11)` | 7,560 | 2 | 82 | 7,476 | 0 | 18 |
| `GF(13)` | 41,580 | 5 | 383 | 41,192 | 0 | 49 |

In both fields, the monic-compatible rank-two charts are exactly the charts
where one projective involution swaps the background and all three support
pairs. This agrees with the local proof; it is not being used as that proof.
The `GF(13)` scan also contains eight such charts with split quartic locators,
three locators per chart. One explicit structural witness is

```text
background={0,1},
support pairs={2,6},{8,9},{4,12},       labels=1,2,3,
B=(X-3)(X-7),       A=9,       involution gamma=7,
R A-c_i B = 0 on the corresponding support pair.
```

For `F` with roots `{3,5,7,10}`, the reconstructed common factor has roots
`{5,10}`. Those are recovered core agreements, while the migrated exact missed
core is `{3,7}`. The structural quotient witness is therefore valid, but it is
not an exact `d=4` witness.

Finally, the smallest sequential RS layout has

```text
(p,n,k,s)=(19,18,5,8),       K=4, M=3, b=2.
```

There are `binom(4,2)^3=216` fixed-support systems. Sage, Singular, and
Macaulay2 independently give

```text
rank(A)=12,       rank([A|b])=13
```

for all 216, so none is compatible. The independent exact support-subset
decoder gives four listed codewords, three planted words, one extra, and zero
with `(d,r,a_i)=(4,2,(2,2,2))`. This emptiness is a tiny-case falsification
control, not a general non-realization theorem.

## Existing-owner audit and exact `(3,1,3,(2,2,2))` control

The first-match existing-owner audit for the new largest profile uses the
declared order

```text
periodicity, quotient descent, auxiliary Johnson, global Johnson, B11 G2/GR.
```

All `2*binom(4,2)^3=432` labelled cofactor-support patterns remain unpaid by
that stack. Each selected seven-point support has trivial cyclic stabilizer,
but it is not the full agreement support: adding each possible restored core
hit gives 1,728 exact eight-point refinements, of which nine have stabilizer
order two. Each of those nine is paid at support level by the existing
one-support-one-line periodic owner, with bound one; this direct support count
does not require witness-data descent. However, the `q^2` cofactor injection
is aggregate over the four restored-core refinements of one seven-point
pattern. No disjoint bound has been proved for the three aperiodic refinements,
so subtracting the nine periodic units from that aggregate charge would be
unjustified without a disjoint injection. The fixed-`(D,R_0)`
auxiliary-Johnson margin is exactly zero,
the global row has `lambda-lambda_J=-1`, and B11 gives
`(d-ell,G2,GR)=(-1,4,5)`, outside the frozen zero-excess boxes. Hence the
periodic support owner is recorded but the bankable ledger mass is unchanged:

```text
profile charge:       155,952 -> 155,952,
all-profile add-back: 1,503,967 -> 1,503,967,
unresolved mass:      668,803 -> 668,803.
```

Here `UNPAID_PRIMITIVE` is the required terminal label, deliberately scoped to
this existing-owner stack. It is not a certificate of full primitivity. In
particular, seven-point cofactor-support aperiodicity is not a claim about the
full support, and the periodic support count is kept distinct from invariant
quotient descent.

Because an aggregate unpaid residual survived, freeze one missed core point `H`, its
degree-three complementary locator `F`, a retained background locator `R` of
degree one, three quadratic support locators `B_i`, and write

```text
R V - c_i F = B_i A_i,
deg(V)<=2,       deg(A_i)<=1,       F monic of degree 3.
```

The fixed-`F` coefficient matrix is `12 x 9`. It has universal rank nine: in
the homogeneous system, each pairwise-coprime `B_i` divides `RV`, hence their
degree-six product divides a polynomial of degree at most three. Its
three-dimensional left kernel gives the CRT compatibility equations

```text
[X^3](FG mod B)=[X^4](FG mod B)=[X^5](FG mod B)=0,
B=B_1B_2B_3,       G=c_i R^(-1) mod B_i.
```

Adjoining the three lower coefficients of a monic cubic gives a `12 x 12`
moving matrix `C`. Equivalently, the lower-coefficient compatibility map is
`3 x 3`, the monic `X^3` contribution is the affine column, and

```text
rank(C)=9+rank(C_reduced).
```

The exact sequential `GF(19)` census gives

| moving stratum | support patterns | ambient monic cubics per pattern |
|---|---:|---:|
| `rank(C)=12=rank([C|b])` | 408 | 1 |
| `rank(C)=11<rank([C|b])=12` | 22 | 0 |
| `rank(C)=rank([C|b])=11` | 2 | 19 |

All four actual degree-three missed-core locators are inconsistent in every
pattern: `rank(A)=9`, `rank([A|b_F])=10`. Restricting the 446 ambient monic
cubics to those four locators therefore leaves zero valid core-locator
solutions and zero exact target codewords. A separate full support-subset
decoder also returns zero target codewords. This is an exact finite
falsification control, not a uniform zero theorem and not a ledger payment.

The two compatible rank-drop lines first appeared as unpaid templates:

```text
background 16; supports {4,6},{8,11},{13,14};
(f0,f1,f2)=(0,4,4)+s(1,1,5),

background 17; supports {4,7},{9,10},{12,15};
(f0,f1,f2)=(0,17,0)+s(1,0,9).
```

Neither line meets any of the four actual missed-core locator points in the
frozen `GF(19)` layout. The uniform reduced-CRT lemma now discharges the
symbolic obligation: compatibility and rank drop make the homogeneous
degree-at-most-three kernel at least two-dimensional; for two kernel pairs,
`B | F_0V_1-F_1V_0` while the cross polynomial has degree at most five, hence
it vanishes. Unique factorization then forces every monic cubic solution to
share a nonconstant factor with its degree-at-most-two remainder. At an actual
locator `F_h=L_core/(X-h)`, this common factor restores another core point, so
the component migrates to `d<=2` and is empty in the exact `d=3` profile.
Thus these compatible ambient lines are no longer primitive survivors.

The profile interpretation is direct and exhaustive. For an arbitrary exact
target polynomial `P`, the unique core agreement `h` and background agreement
`beta` are distinct zeros because the received word is zero on both blocks.
Hence

```text
P=(X-beta)(X-h)V=R H V,       deg(V)<=2.
```

On each exact two-point petal support, cancellation of the nonvanishing core
factor `H` gives `B_i | (RV-c_iF)`, so every exact target enters the reduced
system. Put `D=C\{h}`, `F=L_D`, and `H=L_C/F=X-h`. If
`(X-alpha)|gcd(F,V)`, then split squarefreeness gives `alpha in D` and
`alpha!=h`; therefore `W(alpha)=0=U(alpha)`. For every `x in D`, distinctness
of the core and core/background disjointness give `R(x)H(x)!=0`, so the exact
missed core is

```text
D \ Z(V),
```

of size at most two. This proves the migration, rather than inferring it from
the toy-scale zero count.

Independent Python modular elimination, Singular, and Macaulay2 reproduce the
two compatible `(11,11)` and representative inconsistent `(11,12)` rank pairs.
For the compatible cases they verify nonzero `11 x 11` minors of `C`; for the
inconsistent controls they verify augmented minors `18t` over `GF(19)[t]`.
These are representative exact checks, not generic saturation.

An exact target uniquely determines its one background support, its two points
in each labelled petal, and its restored core point. Thus it has one canonical
cofactor key among

```text
binom(2,1)*binom(4,2)^3=432.
```

The rank-three bound is on all monic cubics for one key, hence across all four
possible restored core points; there is no extra factor four. The fresh
cross-model review independently replayed the Sage, owner, ledger, and mutation
gates and returned GREEN with ledger authorization YES. A supplemental fresh
pass read the upstream background-free/full-petal reconstruction note in full
and confirmed that it is consistency context only, not an imported dependency
of this mixed-background proof.

The reviewed replacement is therefore banked:

```text
profile charge:       155,952 -> 432,
all-profile add-back: 1,503,967 -> 1,348,447,
unresolved mass:      668,803 -> 513,283.
```

The new largest profile is
`(ell,d,r,t,a_i)=(4,3,2,3,(2,2,1))`, `(G2,GR)=(4,4)`, with charge `155,952`.

A targeted TheoremSearch query on the frozen simultaneous-congruence statement
returned general rank-two syzygy-module results for triples of coprime
univariate polynomials. No returned theorem directly supplies the required
finite-field rank-drop classification, so no literature theorem is imported
into this packet.

## Banked `(3,2,3,(2,2,1))` reduced-CRT refinement

The frozen existing-owner pass enumerates

```text
3 * binom(4,2)^2 * binom(4,1) = 432
```

canonical labelled cofactor keys. All 432 remain `UNPAID_PRIMITIVE` under the
first-match stack. Among their 1,728 restored-core refinements, exactly twelve
full supports are periodic. Each lies in a different aggregate key whose other
three refinements are aperiodic, so the twelve one-support owner bounds are not
subtracted from the aggregate `q^2` injection. Invariant quotient descent is
fail-closed without all-data descent; auxiliary Johnson has margin `-11`;
global Johnson misses by one; and B11 gives `(d-ell,G2,GR)=(-1,4,4)`, hence
`ESCAPES_BOUNDED_EXCESS_BOX` at the frozen zero cuts.

For a surviving key, the exact equations are

```text
R*V-c_i*F=B_i*A_i,
deg(R)=2, deg(V)<=1, deg(F)=3,
deg(B_i)=(2,2,1), deg(A_i)<=(1,1,2).
```

The fixed-`F` matrix is `12 x 9` of universal rank nine. With
`B=B_1B_2B_3` of degree five and `G=c_iR^(-1) mod B_i`, the moving monic
system is `12 x 12`; its three compatibility equations are the `X^2,X^3,X^4`
coefficients of `FG mod B`.

If a compatible moving rank drop occurs, take a monic solution `(F,V)` and a
nonzero homogeneous direction `(F_0,V_0)`. Then

```text
B | V*F_0-V_0*F,
deg(V*F_0-V_0*F) <= 4 < 5 = deg(B),
```

so `VF_0=V_0F`. Coprimality of `F,V` would force the degree-three `F` to
divide the nonzero degree-at-most-two `F_0`, a contradiction. Thus
`gcd(F,V)` is nonconstant. For an actual split missed-core locator `F=L_D`,
the common root restores a point of `D`; the exact missed core is `D\Z(V)` and
has size at most two. Compatible rank drop is therefore empty in exact `d=3`,
whereas full rank contributes at most one monic cubic across all four possible
restored core points for the key.

Sage checks all 432 `GF(19)` keys and gives moving-rank pairs

```text
408 * (12,12),  23 * (11,12),  1 * (11,11).
```

The unique compatible ambient line is

```text
F=(X+t)(X^2+16),    V=18(X+t).
```

An independent Python census, Singular, and Macaulay2 reproduce the ranks,
representative minors, and common factor. Fresh read-only proof and certificate
reviewers returned GREEN with ledger authorization YES. Independent exhaustive
falsification over `GF(4)`, `GF(5)`, and a normalized full-profile `GF(11)`
scan found zero coprime compatible-rank-drop solutions.

The mutation-tested complete ledger replay banks

```text
profile charge:       155,952 -> 432,
all-profile add-back: 1,348,447 -> 1,192,927,
unresolved mass:        513,283 ->   357,763.
```

The new largest unresolved row is
`(ell,d,r,t,a_i)=(4,4,1,3,(3,3,1))`, `(G2,GR)=(2,4)`, with 384 keys and
charge `384*19^2=138,624`. TheoremSearch returned rational-interpolation and
syzygy analogues only; no literature theorem is imported into the proof.

## Exact `d=4,r=1` shared auxiliary-owner scope

The existing-owner audit for the new 41331 row finds 384 canonical full
supports. Since `d=ell`, there is no restored-core refinement. Exactly one
support is fixed by shift nine and first-matches to periodic support; the
other 383 first-match to auxiliary Johnson. No `UNPAID_PRIMITIVE` pattern
survives.

More importantly, the sharp auxiliary theorem used earlier is layer-level,
not profile-level. For every fixed `(D_0,R_0)` with `d=4,r=1`,

```text
|T|=12, a=7, d=4, a^2-d|T|=1,
floor(|T|(a-d)/(a^2-d|T|))=36.
```

There is one `D_0` and two `R_0` choices, so `72` bounds the union of all
fifteen exact profile cells with `d=4,r=1`. Their post-32221 charges total
`416,020`; the earlier ledger attached the same `72` envelope only to the
`(3,2,2)` cell and conservatively retained the other fourteen charges. The
correct shared-envelope bookkeeping is therefore

```text
15-profile shared scope: 416,020 -> 72,
all-profile add-back:   1,192,927 -> 776,979,
unresolved mass:          357,763 -> 212,755.
```

The unresolved subtotal follows the existing convention and retains the one
`72` carrier charge. The fourteen zero allocations are incremental ledger
charges, not standalone zero bounds. The unique periodic support is already
inside the common auxiliary envelope and adds no extra `+1`.

The next largest unchanged row is
`(ell,d,r,t,a_i)=(4,4,0,3,(3,3,2))`, `(G2,GR)=(2,5)`, with charge
`288*19^2=103,968`. The stronger possible cross-`R_0` charge `36`, and any
payment of the `r=0` row, are deliberately not used without a separate frozen
lemma and review.

## Exact `d=4,r=0` shared auxiliary-owner scope

The separate frozen audit supplies that next lemma without combining residual
layers.  On the concrete partition

```text
Omega = Y disjoint-union {16,17} disjoint-union T,
Y = {0,1,2,3},        D_0=Y,        R_0=empty,
```

exact `d=4,r=0` excludes every core and background agreement.  Thus all
agreements lie on the common twelve-point petal domain, and the concrete
sunflower map is `G_P=P-P_star` with degree at most four and at least eight
agreements with the single auxiliary word `U_D0`.  The sharp Johnson audit is

```text
|T|=12, a=8, d=4, a^2-d|T|=16,
floor(|T|(a-d)/(a^2-d|T|))=3.
```

The exact profile generator gives eleven disjoint cells: the sole `t=2` cell
`(4,4)` and the ten nonincreasing `t=3` triples with entries at most four and
sum at least eight.  Their aggregate support-pattern multiplicity is `794`,
their post-41331 charge is `135,470`, and their unresolved-route subtotal is
`107,844`.  The multiplicity is not a realized-codeword census.

One bookkeeping carrier on the original unresolved `(3,3,2)` row charges the
common envelope once; the other ten zeroes are only incremental allocations.
Fresh independent and cross-model reviews are GREEN, and the mutation-tested
content-addressed replay banks

```text
11-profile shared scope: 135,470 -> 3,
all-profile add-back:     776,979 -> 641,512,
unresolved mass:          212,755 -> 104,914.
```

The separately banked `r=1` charge `72` remains unchanged; no cross-`r`
`72+3 -> 36` saving is used.  The next largest unresolved row is
`(ell,d,r,t,a_i)=(4,3,1,3,(3,2,1))`, `(G2,GR)=(3,4)`, with 1,152 aggregate
patterns and charge `1,152*19=21,888`.  Its auxiliary margin is zero.

## Proof status and stop condition

- **Rigorous for the frozen finite rows:** profile enumeration, support-pattern
  multiplicities, cofactor upper bounds conditional on the cited proved
  lemmas, B7--B11 coordinates, and the three-CAS tiny-template rank censuses.
- **Rigorous local algebra:** the disjoint `(2,1,1)` coefficient system has
  full rank, with compatibility controlled by the displayed single augmented
  determinant. On the disjoint `m=2` `(2,2,2)` chart, the full system has
  rank 12; every compatible coefficient-rank drop has a degree-two
  complete-fibre template and recovers exactly two missed-core points. Thus
  every exact `d=4` survivor is rank three, giving the displayed moving-support
  `q`-fibre bound. For `(3,2,1)`, pairwise-coprime support locators prove the
  fixed-support coefficient matrix has rank 12. The CRT inverse argument above
  proves every moving-monic-quartic rank drop is affine-inconsistent under
  disjoint locators and distinct nonzero labels; full-rank charts cost at most
  `q`. The independent review is GREEN under exactly these printed hypotheses.
  For `(3,1,3,(2,2,2))`, the reduced-CRT degree-gap/UFD argument proves that
  compatible moving-cubic rank drop forces a nonconstant `gcd(F,V)`;
  full-rank charts cost at most one monic cubic per fixed support pattern. The
  direct factorization of every exact target into `RHV` proves exhaustivity,
  and the pointwise formula identifies the missed core as `D\Z(V)`, making the
  compatible rank-drop component empty in exact `d=3`. Fresh cross-model review
  is GREEN under the printed split-squarefree, block-disjointness, and zero-core
  received-data hypotheses. For `(3,2,3,(2,2,1))`, the degree-five CRT modulus,
  degree-at-most-four cross polynomial, and Euclid's lemma give the analogous
  common-factor migration with `deg V<=1`. Two fresh read-only reviews are
  GREEN under the printed standalone profile hypotheses.
- **Exact domain/owner partition:** all 67 compatible structural tiny-field
  charts emit their PGL2 involution but remain unowned without an RS domain.
  The actual sequential `GF(19)` domain has no compatible rank-two chart. The
  positive and mutation controls distinguish declared power-fold payment from
  noninvariance, undeclared rational symmetry, and witness-data nondescents.
- **Exact full-rank and owner add-back:** replacing `q^3` by `q` only on the
  `m=2` target and replacing the minimal `(4,1,3,(3,2,2))` charge by the
  proved fixed-layer auxiliary-Johnson sum reproduces the first two refinement
  columns above. The independently reviewed `(3,2,1)` substitution gives
  complete add-back `1,503,967` and unresolved mass `668,803` on the
  frozen GF(19) layout. The reviewed reduced-CRT replay further improves these
  first to `1,348,447` and `513,283`, then the reviewed 32221 replay improves
  them to `1,192,927` and `357,763`. The fresh independent and cross-model
  GREEN 41331 review then authorizes the shared `d=4,r=1` auxiliary envelope,
  giving banked values `776,979` and `212,755`. A separate pair of GREEN
  reviews authorizes the one-layer `d=4,r=0` envelope, giving banked values
  `641,512` and `104,914`, respectively. Positive unresolved mass remains.
- **Empirical/exact finite evidence:** the 19-codeword list and seven surviving
  template solutions, the `GF(11)`/`GF(13)` structural censuses, the empty
  216-fibre `p=19` control, and the 576-pattern `(3,2,1)` census with its
  two independently replayed inconsistent rank drops. The new 432-pattern
  `(3,1,3,(2,2,2))` census has zero exact targets but two compatible ambient
  cubic-line templates; the reduced-CRT lemma routes every actual split-core
  incidence to exact-profile migration. The 32221 census has zero exact targets
  and one compatible ambient line; its forced factor is reproduced by three
  engines and by separate small-field falsification scans. Exact does not mean
  asymptotic.
- **Unproved:** domain-compatible payment for any non-exact rank-two frontier
  template, closure of the remaining finite profiles, identification with a
  closed asymptotic profile envelope, the fixed-profile cap required by PR
  `#763`, any higher-`m` analogue, or a bound for the full mixed-petal bucket.

Verdict: **YELLOW -- promising but unresolved; do not authorize a global
proof or theorem statement.**

The `m=2` rank-two domain partition, full-rank finite add-back, first
existing-owner correction, and local `(3,2,1)` CRT proof are now frozen as an
experimental packet. They give a negative closure result: unresolved mass
remains, and none applies to #763's deployed row. The CRT kernel review has
passed. The existing-owner audit for `(3,1,3,(2,2,2))` has now been completed
and pays no mass by itself. Its exact finite rank census leaves two compatible
ambient cubic-line templates, while the reduced-CRT pointwise bridge excludes
both from exact `d=3`. The `432` charge and resulting `1,348,447`/`513,283`
totals were banked after GREEN cross-model review. The 32221 owner partition
leaves all 432 aggregate keys unpaid, but its independently reviewed
degree-five reduced-CRT lemma now banks the further `432` charge and resulting
`1,192,927`/`357,763` totals. The exact 41331 owner partition leaves no unpaid
support, and its reviewed shared-layer replay banks the further
`776,979`/`212,755` totals. The separately reviewed `d=4,r=0` layer replay then
banks `641,512`/`104,914` without combining it with `r=1`. The next gate is the
existing-owner partition for
`(ell,d,r,t,a_i)=(4,3,1,3,(3,2,1))`, `(G2,GR)=(3,4)`, charge `21,888`.
Cross-`r` aggregation remains unbanked. The global theorem remains out of scope
until the remaining profiles have named payments and the whole implication
chain survives independent review.

## Reproduction

```bash
python3 experimental/scripts/verify_l1_imgfib_crosswalk_audit.py
python3 experimental/scripts/verify_l1_imgfib_crosswalk_audit.py --tamper-selftest
python3 experimental/scripts/verify_l1_mixed_petal_frontier_ledger.py
python3 experimental/scripts/verify_l1_mixed_petal_frontier_ledger.py --tamper-selftest
python3 experimental/scripts/verify_l1_b11_frontier_scanner_schema.py
python3 experimental/scripts/verify_l1_b11_frontier_scanner_schema.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/analyze_l1_mixed_petal_template_221.sage
python3 experimental/scripts/verify_l1_mixed_petal_template_221_cas.py
python3 experimental/scripts/verify_l1_mixed_petal_template_221_cas.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/analyze_l1_mixed_petal_template_211.sage
python3 experimental/scripts/verify_l1_mixed_petal_template_211_cas.py
python3 experimental/scripts/verify_l1_mixed_petal_template_211_cas.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_boundary_222.sage
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_boundary_222.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_boundary_222_cas.py
python3 experimental/scripts/verify_l1_b9_boundary_222_cas.py --tamper-selftest
python3 experimental/scripts/verify_l1_b9_rank2_owner_classifier.py
python3 experimental/scripts/verify_l1_b9_rank2_owner_classifier.py --tamper-selftest
python3 experimental/scripts/verify_l1_b9_m2_full_rank_ledger.py
python3 experimental/scripts/verify_l1_b9_m2_full_rank_ledger.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_boundary_321.sage
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_boundary_321.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_boundary_321_cas.py
python3 experimental/scripts/verify_l1_b9_boundary_321_cas.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_l1_b9_boundary_321_dichotomy.sage
/usr/local/bin/sage experimental/scripts/verify_l1_b9_boundary_321_dichotomy.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_31222_owner_partition.py
python3 experimental/scripts/verify_l1_b9_frontier_31222_owner_partition.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_frontier_31222.sage
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_frontier_31222.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_31222_cas.py
python3 experimental/scripts/verify_l1_b9_frontier_31222_cas.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_lemma.sage
/usr/local/bin/sage experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_lemma.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_cas.py
python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_cas.py --tamper-selftest
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_ledger.py
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_ledger.py --tamper-selftest
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_owner_partition.py
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_owner_partition.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_frontier_32221.sage
/usr/local/bin/sage experimental/scripts/analyze_l1_b9_frontier_32221.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_cas.py
python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_cas.py --tamper-selftest
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_ledger.py
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_ledger.py --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_41331_owner_partition.py
python3 experimental/scripts/verify_l1_b9_frontier_41331_owner_partition.py --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py
python3 experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py --tamper-selftest
python3 experimental/scripts/verify_l1_b9_d4r0_shared_auxiliary_ledger.py
python3 experimental/scripts/verify_l1_b9_d4r0_shared_auxiliary_ledger.py --tamper-selftest
```
