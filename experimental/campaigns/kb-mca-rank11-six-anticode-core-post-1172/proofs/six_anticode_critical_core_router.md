# Six-anticode sparse-pair router and critical order-32 common core

## 1. Deployed setup

Use the KoalaBear row

```text
n=2097152, K=1048576, m=1116048, w=m-K=67472,
B*=274980728111395087, near=2w=134944.
```

After the reversible rank gauge, the post-near explanations lie in an affine
flat with direction dimension `s<=10`.  For every selected slope `gamma`, fix
once and for all one actual minimizing pair

```text
e_gamma=(a_gamma,b_gamma)
in (c_0+C') x C'
```

and its complete pair core

```text
H_e={x:r_0(x)=a_e(x), r_1(x)=b_e(x)}.
```

The nonuniform support-margin theorem gives

```text
sum_gamma theta_gamma <= C_10
C_10=106618568137036225644.                          (1)
```

For a cutoff `1<=tau<w`, put

```text
A=m-tau, d=A-K=w-tau,
L_tau={gamma:theta_gamma<=tau},
H_tau={gamma:theta_gamma>=tau+1}.
```

Then

```text
|H_tau| <= floor(C_10/(tau+1)).                       (2)
```

Every low record has `|H_e|>=A`.  One fixed pair type owns at most

```text
n-|H_e| <= n-A                                            (3)
```

slopes, by the fixed-pair outside-core injection.

## 2. Fixed-left anticode cap

A pairwise-rank-one anticode is classified by PR #1171 as fixed-right or
fixed-left.  The fixed-right geometry is uniformly bounded by

```text
R_ray=8147918.                                           (4)
```

For one fixed-left anticode, an invertible endpoint row operation produces a
fixed codeword endpoint `c` and a varying endpoint in an affine RS space of
dimension at most `s`.  Put

```text
G={x:R(x)=c(x)}, g=|G|, q=n-g.
```

The ordinary affine-span list bound on `G`, followed by the same-support
outside-`G` owner injection, gives

```text
F_tau(q)
 =1+q floor( C(K-q+s,s)/C(d+s,s) )
 <=1+q floor( C(K-q+10,10)/C(d+10,10)).                 (5)
```

The initial `1` is the single projective fixed-endpoint direction.

## 3. Five anticodes are paid

Take

```text
tau=1798, A=1114250, d=65674.
```

The exact scan of (5) over `0<=q<=n-A=982902` has one maximizer:

```text
q*=95326,
F_tau(q*)=39537225656384765.                             (6)
```

The high tail is

```text
floor(C_10/1799)=59265463111193010.                      (7)
```

Thus a cover by at most five maximal rank-one anticodes has total

```text
134944 + 59265463111193010 + 5*39537225656384765
=256951591393251779
<B*,                                                        (8)
```

with slack `18029136718143308`.  The fixed-right cap is smaller than the
fixed-left cap, so (8) also covers mixed geometries.

This is a cover statement, not a sum over overlapping owners: assign every
pair type to one maximal anticode first, and count the resulting disjoint
slope groups.

## 4. Every unsafe six-cover is six fixed-left directions

The low mass required by an over-budget line is

```text
L_req=B*-near-floor(C_10/1799)+1
     =215715265000067134.                               (9)
```

Five full fixed-left groups plus one fixed-right group contribute at most

```text
5*39537225656384765+8147918
=197686128290071743<L_req.                              (10)
```

Therefore an unsafe exact six-anticode cover consists of six fixed-left
anticodes.

Let `Z_i` be the disjoint assigned slope group of the `i`-th anticode.  Since
the other five groups each have size at most (6), every group satisfies

```text
|Z_i| >= L_req-5F_tau(q*)
       =18029136718143309.                              (11)
```

The largest `q` for which (5) can reach (11) is exactly

```text
q_0=247518,                                             (12)
```

because

```text
F_tau(247518)=18029257843230307,
F_tau(247519)=18029105617115083.
```

Consequently every fixed endpoint set satisfies

```text
g_i>=n-q_0=1849634.                                    (13)
```

## 5. The six fixed endpoints synchronize to one codeword pair

Take maximal fixed-left anticodes.  Two with the same endpoint direction
have fixed endpoint codewords whose agreement sets intersect in at least

```text
2*1849634-n=1602116>K.
```

Their difference is a degree-`<K` polynomial with more than `K` roots, so the
fixed endpoints are identical and the maximal anticodes coincide.  Hence a
minimal six-cover has six distinct projective endpoint directions.

For any three distinct directions, the three fixed endpoint sets have common
intersection at least

```text
3*1849634-2n=1354598>K.                                (14)
```

Two endpoint functionals form a basis of the dual two-dimensional endpoint
space and therefore reconstruct one global degree-`<K` codeword pair

```text
p=(p_0,p_1).
```

On the triple intersection, the third endpoint functional agrees with its
claimed codeword.  The difference has more than `K` roots, so it vanishes
identically.  Repeating with the remaining directions proves that all six
fixed endpoints are the six linear projections of the same pair `p`.

Put

```text
H={x:(r_0(x),r_1(x))=(p_0(x),p_1(x))},
e=n-|H|.                                                (15)
```

For direction `i`, write

```text
G_i=H disjoint_union E_i.
```

Outside `H`, the received-pair error is a nonzero two-vector.  It lies in the
kernel of at most one of the six distinct endpoint functionals.  Therefore
the sets `E_i` are pairwise disjoint and

```text
sum_i |E_i| <= e.
```

Since `q_i=n-|G_i|=e-|E_i|`,

```text
sum_{i=1}^6 q_i >=5e.                                  (16)
```

## 6. Exact six-load extremal theorem

For `tau=1798`, define

```text
D=C(65684,10),
G(q)=q C(K-q+10,10),
Phi(q)=1+G(q)/D.                                        (17)
```

Equation (5) gives `F_tau(q)<=Phi(q)`.  The exact first and second difference
signs, independently checked at every deployed integer, imply:

```text
G is increasing through q=95326 and decreasing afterward;
G is discretely concave on 0..190651;
G is discretely convex and decreasing on 190652..982902. (18)
```

Take

```text
e_0=167814, S_0=5e_0=839070.                           (19)
```

We maximize `sum_i G(q_i)` subject to

```text
0<=q_i<=982902, sum_i q_i>=S_0.                        (20)
```

Split by the number `h` of entries in the convex interval
`190652..982902`.

- The remaining `6-h` entries are in the concave interval.  For a required
  total above `(6-h)*95326`, discrete concavity balances them; below that
  threshold their maximum is attained by setting every entry to the peak
  `95326`.
- For a fixed total of the `h` convex-interval entries, convexity moves all
  but at most one entry to an interval endpoint.  Thus an extremizer has
  `k` entries at `982902`, `h-k-1` entries at `190652`, and one residual
  entry.  The exact verifier exhausts all such endpoint/residual choices.

The seven exact maxima are all below `L_req`.  The worst case is `h=0`, with

```text
(q_1,...,q_6)=(139845,...,139845).
```

Its gap below the required low mass is the positive rational

```text
5039866042250644297697303907940552741600048679872
----------------------------------------------------------------
7575576854420300947226509036769468677

=665278187932.304... .                                  (21)
```

Hence (20) is incompatible with an over-budget six-cover.  Therefore

```text
e<=167813.                                              (22)
```

For larger `e`, the feasible set in (20) only shrinks, so no additional
optimization is needed.

Choosing `p_1` as the direction gauge shows that the minimum direction support
is at most the pair-error union support `e`.  The separately proved full-lift
prefix pays minimum direction support through `96150`.  Thus an unpaid exact
six-cover is confined to

```text
96151 <= minimum direction support <=167813.            (23)
```

No claim is made that the pair-error support equals the minimum direction
support.

## 7. Order-32 common-core synchronization

Now take

```text
tau=3304,
A=m-tau=1112744,
d=w-tau=64168.
```

Equations (1)--(2) force at least

```text
L_32
=B*-near-floor(C_10/3305)+1
=242720949552398957                                    (24)
```

low slopes in an over-budget line.

Each such slope has a complete pair core of size at least `A`.  Count
incidences `(gamma,C)` where `C` is a 32-subset of the complete pair core.
The average number of incident slopes over all 32-subsets of the domain is

```text
L_32 C(A,32)/C(n,32).
```

Its ceiling is

```text
378013809.                                              (25)
```

Therefore some actual 32-coordinate set `C_*` is contained in the complete
pair core of at least that many slopes.

One pair type owns at most

```text
n-A=984408                                              (26)
```

slopes.  Hence at least

```text
ceil(378013809/984408)=385                              (27)
```

distinct actual minimizing pair types share `C_*`.

Cancel the common coordinate locator and delete these 32 coordinates.  The
shortened row has

```text
(n',K',A')=(n-32,K-32,A-32),
n'-K'=K,
A'-K'=64168.
```

If the affine endpoint-variation dimension were at most two, the ordinary
rank-two affine list cap and the sub-square interleaving collapse would give
at most

```text
floor(C(K+2,2)/C(64170,2))=267                          (28)
```

distinct ordered pair types.  The field guard `267^2<2130706433^6` holds.
Equations (27)--(28) contradict each other.  Therefore the shortened endpoint
variation has affine dimension at least three.

Every selected explanation agrees with the received affine word on `C_*`.
An exact size-`m` support can be reselected to contain `C_*` and at least one
coordinate outside its pair core, so same-support noncontainment is retained.
Thus line-global common-core cancellation preserves all `378013809` distinct
slopes.

## 8. Complete cutoff and method-wall audit

The exact scan over all `1<=tau<w` gives:

```text
9675 cutoffs force the dimension-three conclusion at core size 32;
tau=3304 maximizes synchronized pair types: 385;
tau=2673 maximizes the excess over the rank-two cap: 119.
```

Repeating the identical certificate class with 33-subsets never forces a
contradiction.  Its closest cell is

```text
tau=2815,
198803088 synchronized slopes,
203 pair types,
rank-two pair cap 262,
deficit 59.                                             (29)
```

Thus core size 32 is maximal for this exact averaging plus pair-cap method.
Equation (29) is a method wall, not a construction or counterexample.

## 9. Final theorem boundary

Every unsafe post-near affine-error-rank-eleven line satisfies both of the
following:

1. its low pair types cannot be covered by five rank-one anticodes; an exact
   six-cover synchronizes to one codeword-pair owner and survives only in the
   support window (23);
2. it contains a 32-shortened actual subfamily of at least `378013809` slopes,
   with at least `385` minimizing pair types and endpoint-variation dimension
   at least three.

The theorem does not pay cover number at least seven, the support interval in
(23), or the dimension-at-least-three shortened family.  No active-v4 atom or
row certificate moves.
