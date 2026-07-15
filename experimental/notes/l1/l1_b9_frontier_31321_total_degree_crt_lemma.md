# Total-degree-six reduced-CRT lemma for the `31321` frontier

## Status

PROVED-LOCAL / EXACT GF(19) / FRESH INDEPENDENT AND CROSS-MODEL GREEN /
FROZEN ROW REFINEMENT BANKED.

This note treats only the frozen sequential row

```text
(q,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2),
(ell,d,r,t,a_i)       = (4,3,1,3,(3,2,1)).
```

It states explicitly the degree-partition extension that is implicit in the
proof of the banked `(3,1,3,(2,2,2))` reduced-CRT lemma.  It does not cite the
older statement verbatim, because that statement assumes three quadratic
support locators.

## Total-degree-six statement

Let `k` be a field.  Let `R,B_1,B_2,B_3 in k[X]` be monic and pairwise
coprime, with

```text
deg R = 1,
(deg B_1,deg B_2,deg B_3) a permutation of (3,2,1).
```

Put `B=B_1B_2B_3`, so `deg B=6`.  Let `c_1,c_2,c_3` be distinct nonzero
elements of `k`, and let `G` be the unique polynomial of degree below six
satisfying

```text
G = c_i R^(-1) mod B_i.
```

The residue `G` is a unit modulo `B`.  For a monic cubic

```text
F = X^3 + f_2 X^2 + f_1 X + f_0,
```

put `V=FG mod B`.  The fixed-syndrome equations are

```text
RV-c_iF = B_i A_i,          i=1,2,3,
deg V <= 2,
deg A_i <= 3-deg B_i.
```

In the original labelled order the quotient bounds are `3-deg(B_i)`; their
multiset is `(0,1,2)`.  Consequently the fixed-`F` coefficient system has
twelve equations and nine unknowns, independently of which labelled petal has
which support size:

```text
3 coefficients of V + (1+2+3) coefficients of the A_i.
```

It has rank nine.  Indeed, a homogeneous solution satisfies `B_i | RV` for
every `i`.  Pairwise coprimality and `gcd(R,B)=1` give `B | V`; since
`deg V<=2<6=deg B`, this forces `V=0`, followed by `A_i=0`.

Adding the three lower coefficients of the monic cubic gives a square
`12 x 12` affine system.  Equivalently, compatibility is the `3 x 3` affine
system obtained by taking the `X^3,X^4,X^5` coefficients of `FG mod B`.

The following dichotomy holds for every fixed cofactor-support key.

1. If the reduced `3 x 3` coefficient matrix has rank three, at most one monic
   cubic `F` is compatible.
2. If its rank is below three and the monic affine system is inconsistent, no
   monic cubic is compatible.
3. If its rank is below three and a monic cubic `F` is compatible, then
   `gcd(F,V)` has positive degree.

Only the total degrees and unit condition enter this dichotomy; equality of the
three individual support degrees is not used.

## Compatible rank drop

Let

```text
U = {F in k[X] : deg F<=3 and deg(FG mod B)<=2}.
```

If the reduced affine system is compatible and its coefficient matrix has
rank below three, its monic solution set in `(f_0,f_1,f_2)` has positive
dimension.  A compatible monic cubic together with a nonzero direction of
that affine solution set therefore gives `dim U>=2`.  Choose independent
`F_0,F_1 in U` with `F_0` the compatible monic cubic, and write
`V_i=F_iG mod B`.  Since `G` is a unit modulo `B`, a nonzero `F_i` cannot have
`V_i=0`.  Moreover

```text
B | F_0V_1-F_1V_0,
deg(F_0V_1-F_1V_0) <= 3+2 = 5 < 6 = deg B.
```

Thus `F_0V_1=F_1V_0` as polynomials.  Write `V_i=gW_i` with
`gcd(W_0,W_1)=1`.  Unique factorization gives `F_i=AW_i`.  If `W_0` were
constant, then `deg A=3`, so the degree bound on `F_1` would force `W_1` to be
constant too, making the two pairs scalar multiples.  Hence `W_0` is
nonconstant and divides both `F_0` and `V_0`.

## Exact-profile bridge

For the frozen sunflower, let the four-point core `C` be split and squarefree,
let `h in C` be the unique restored core agreement, and put

```text
D = C\{h},       F=L_D,       H=L_C/F=X-h.
```

Let `R=X-beta` locate the retained background agreement, assume the core and
background are disjoint, and use the normalized sequential received word,
which is zero on the core and background.  Every exact explaining polynomial
has the form

```text
W=RHV,            deg V<=2.
```

If `B_i=L_{S_i}` locates the exact selected petal support, then on `S_i` the
received word is `c_iL_C=c_iHF`.  Cancelling the nonzero factor `H` on the
petals gives exactly

```text
B_i | RV-c_iF.
```

Thus every exact target enters the displayed reduced-CRT system.  Conversely,
the three congruences give the selected petal agreements.

If compatible rank drop gives a root `alpha` of `gcd(F,V)`, split
squarefreeness gives `alpha in D`.  Since `R(alpha)` and `H(alpha)` are nonzero,

```text
W(alpha)=R(alpha)H(alpha)V(alpha)=0=U(alpha).
```

Therefore the actual missed core is `D\Z(V)` and has size at most two.
Compatible rank drop cannot realize the exact `d=3` row.

## Canonical keys and disjointness

An exact codeword uniquely determines its retained background point and its
three labelled petal agreement sets of sizes `(3,2,1)`.  The number of
cofactor-support keys is

```text
binom(2,1) * 3! * binom(4,3) * binom(4,2) * binom(4,1) = 1,152.
```

The restored core point supplies no factor four.  For a fixed cofactor key,
the full-rank reduced map bounds all monic cubics at once by one; a compatible
rank drop migrates out of exact `d=3`.  A monic split cubic `F=L_D` determines
the missed set `D` and hence the restored point `h`.

Consequently the exact row has at most one codeword per canonical key and at
most `1,152` codewords in total.

## Exact certificates

The Sage certificate enumerates all 1,152 canonical keys and obtains

```text
1,108 * (rank(C),rank([C|b])) = (12,12),
   44 * (rank(C),rank([C|b])) = (11,12),
```

equivalently 1,108 reduced-full-rank systems and 44 affine-inconsistent
rank-two reduced systems.  There is no compatible rank drop in this frozen
`GF(19)` row, so the compatible-drop finite check is explicitly vacuous.  The
universal degree-gap proof supplies that branch; the reviewed `31222` packet
is retained only as a nonvacuous total-degree-six control.

The owner certificate enumerates 1,152 aggregate keys and 4,608 restored-core
refinements.  Exactly twelve full-support refinements are periodic, in twelve
distinct keys, but no refinement-level payment is subtracted.  The CRT and
owner enumerations have the same content-addressed canonical key set.

The certificate validators bind the label, degree, coprimality,
split-squarefree, block-disjointness, zero core/background data, symbolic-map,
rank-relation, key-set, and review hypotheses.  Their mutation suites include
nonsplit and repeated locators, nonzero background data, altered symbolic
matrices, duplicate-key summaries, forged review hashes, and a forged banked
CRT packet.

## Banked ledger consequence

After the independent and Claude reviews both returned GREEN with ledger
authorization YES, the content-addressed 75-row replay banks

```text
profile charge:       21,888 -> 1,152,
all-profile add-back: 641,512 -> 620,776,
unresolved mass:      104,914 ->  84,178.
```

The next largest unresolved row is

```text
(ell,d,r,t,a_i) = (4,4,2,2,(3,3)),
(G2,GR)          = (2,3),
support patterns = 48,
charge           = 48*19^2 = 17,328.
```

Positive unresolved mass remains.  This is a local finite-row refinement, not
closure of the mixed-petal bucket.

## TheoremSearch check

After the compatibility statement was frozen, targeted TheoremSearch queries
returned rational-interpolation and Padé analogues, including Proposition 2.1
of [Claeys--Wielonsky](https://arxiv.org/abs/1112.2887).  None states the
finite-field total-degree-six CRT implication above.  No literature theorem is
imported; the load-bearing step is the elementary degree gap and Euclid's
lemma.

## Review history

The first independent review returned YELLOW because the mathematical packet
was sound but several claim-bearing fields and the banking Boolean were not
fail-closed.  The first broad Claude attempt reached its turn cap and supplied
no verdict.  Both are retained as audit history.  After the validators were
hardened, a fresh independent replay and a narrower Claude replay returned
GREEN/YES on the same four unbanked core hashes, independently rechecked the
algebra and arithmetic, and authorized a mechanistic promotion.  A subsequent
final-package audit caught stale bank-state wording and blank EOF lines in the
retained review history.  The gate was reopened, those nonmathematical defects
were repaired, and a second independent/cross-model pair reviewed the seven
frozen final-package artifacts.  The final certificates hash-link that second
GREEN/YES pair directly; the earlier reviews remain audit history.

## Reproduction

```bash
python3 experimental/scripts/verify_l1_b9_frontier_31321_owner_partition.py
python3 experimental/scripts/verify_l1_b9_frontier_31321_owner_partition.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_l1_b9_frontier_31321_total_degree_crt.sage
/usr/local/bin/sage experimental/scripts/verify_l1_b9_frontier_31321_total_degree_crt.sage --tamper-selftest
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_31321_total_degree_crt_ledger.py
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_31321_total_degree_crt_ledger.py --tamper-selftest
```

## Stop conditions

- Do not treat the zero auxiliary-Johnson margin as a bound.
- Do not subtract isolated periodic restored-core refinements from the
  aggregate cofactor charge without a disjoint refinement-level injection.
- Do not weaken pairwise coprimality, nonzero distinct labels, split
  squarefreeness, block disjointness, or zero core/background data.
- Do not generalize beyond total support degree six or the frozen exact row in
  this packet.
- No `m>2`, PR `#763`, Lean, cross-`r`, or global mixed-petal conclusion is
  claimed.
