# Signed-Minor Payment: Source-Clause Census

## Status

```text
Status: EXPERIMENTAL (census / small-case evidence only)
Route: hard input #2 (agents.md L47/L67) -- "image-scale MI + MA, or a direct
       Sidon payment" -- the signed-minor clause of the charge-preserving
       semantic-or-signed dichotomy (avdeevvadim PR #716,
       experimental/notes/audits/primitive_signed_payment_barrier_v1.md,
       section 6).
Claim (route-scoped): census evidence locating which single source-
       realizability clause -- among (i) certified source columns, (ii) one
       complete dyadic |tau| band, (iii) first-match residual mask, (iv)
       owners on one received affine line -- carries the gap between the
       abstract L^{1/2-1/q} kernel-sign construction and a bounded,
       source-realizable signed packet, on exact small instances in TWO
       regimes: a dense-fiber regime (PR #717 Section 7's superincreasing
       depth-1 family, fiber load WL/M ~ (3/2)^B) and a sparse regime
       (moment-curve pairs over F_p, M/L -> 0).
Headline: in the dense regime, exactly one single-clause ablation restores
       absolute gain growth: clause (iii), the first-match residual mask
       (fitted exponent +0.069 vs -0.07..-0.10 for every other set; the
       C_iii/B gain ratio grows 1.33 -> 2.17 -> 4.03). The all-free set A
       does NOT grow even there (slope -0.007): ablating clause (i)
       destroys the superincreasing collision structure that creates the
       dense fiber load in the first place, so the guardrail-type growth
       needs MORE than density -- it needs the certified source columns
       present and the first-match pruning absent. In the sparse regime no
       constraint set grows and the sharpest signal is relative (clause
       (ii)'s ablation opens the largest, L-monotone gap from baseline).
Verifier: verify_signed_minor_payment_clause_census_v1.py -- 470/470 PASS
          (~13s); --tamper-selftest -- 16/16 mutations detected (~14s).
```

This note proves nothing asymptotic about the dichotomy. It maps, on 42
exact small instances (24 sparse + 18 dense, six constraint sets each),
which of PR #716's four source-realizability clauses is load-bearing for
keeping the normalized q-gain bounded, in both a fiber-dense and a
fiber-sparse operationalization. See Nonclaims for what this does not
establish.

## Credit and interfaces

The abstract kernel-sign construction, its exact toy anchor value
(`1.1182491777` at `q=4`, `G=F_3^6`), and the four-clause diagnosis of why it
is not a source-semantic falsifier are **avdeevvadim's**, PR #716
(`experimental/notes/audits/arbitrary_mask_idempotent_guardrail_v1.md`,
`experimental/scripts/verify_arbitrary_mask_idempotent_guardrail_v1.py`, both
open at the time of this census and not copied into this branch -- Step 0
below is an independent reimplementation replaying his exact parameters and
witness). The "charge-preserving semantic-or-signed dichotomy" whose signed
clause is being probed is his, from the same PR's companion note
`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`, section 6.

The dense-regime family is PR #717's
(`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`,
Section 7): the superincreasing depth-1 subset-sum instance `A_i=5^i`,
`C=2*sum(A_i)+1`, `T={A_i} u {C-A_i}`, `a=B`, `Phi(S)=sum(S)`, whose fiber
load `WL/M` grows like `(3/2)^B`. This census replicates that section's
table facts exactly (see the dense-regime section below) and then runs the
six-constraint-set ablation on the same instances. PR #717 also discharges
the heavy-fiber interface obligation that PR #716 leaves open on the
locator-prefix chart (hereditary mask admissibility reduces to plain
emission there, for `R < char(B)` on the power-sum chart), so on that chart
the dichotomy this census probes is the sole remaining input-2 gap.

This census is compatible with, and does not decide, PR #713's `(CAT)` atlas
ledger (`experimental/notes/thresholds/atlas_cat_cell_ledger.md`, open):
#713 identifies the blocked cells of hard input #1's per-cell exhaustion as
collapsing to hard input #3 plus the Sidon payment plus one planted census.
The Sidon payment named there is the same open object this census's
constraint set B is trying to locate a source clause for; neither PR decides
the other.

A newer signed-side *structured* payment is **DannyExperiments' PR #719**
(`experimental/notes/thresholds/signed_local_minority_fixed_composition.md`,
open): it pays exact equal-block-occupancy profiles via a product-Johnson /
product-shadow / block-centered-Plotkin route in the source regime, and its
section 7 exhibits a balanced mixed-sign profile that defeats block Plotkin
at every one of its four recorded dyadic rescalings, leaving as the exact
next object "any nonempty primitive first-match residual inside this
balanced mixed-sign profile," payable only by "a signed
phase/Fourier/Sidon/Hankel max-fiber estimate ... or a fully rooted owner
carrying the source's received data, explaining data, first-match ownership,
and slope projection" (#719 section 7). That is exactly the nonstructured
regime this census probes: #719 pays specific structured profiles and stops
at the mixed-sign residual; this census does not pay that residual either,
but maps which single source-realizability clause is doing the work in the
"fully rooted owner" alternative #719 leaves open.

## The normalized q-gain and the four clauses

**Normalized q-gain** (identical in both regimes, and identical to PR #716's
own script): for an ambient finite abelian group `G` (`|G|` written `L` in
the fit tables), a character band `A subset G^\{0}`, and a support mask
inducing the count function `f(x) = #{masked supports S with Phi(S)=x}`,
build `K_A(x) = (1/|G|) sum_{xi in A} chi_xi(x)`, project `P_A f = K_A * f`,
and set

```text
gain(A, f) = ||P_A f||_q / |G|^{1/q},        q = 4 fixed throughout.
```

Six constraint sets at every instance size: **A** (all four clauses
ablated), **B** (all four imposed), **C_i, C_ii, C_iii, C_iv** (exactly one
ablated, the other three imposed).

| Clause | Imposed means | Ablated (free) means |
|---|---|---|
| (i) certified source columns | the regime's actual source columns (moment-curve `(1,t,t^2)` / superincreasing `T`) | a fixed, reproducible, non-source column assignment |
| (ii) one complete dyadic `\|tau\|` band | band = one full dyadic level of `tau(xi) = sum_t chi_xi(v_t)`, `\|tau\|>=1` | band = union of complete symmetric classes (scalar orbits in the sparse arm; complete tau-classes incl `<1` in the dense arm) |
| (iii) first-match residual mask | mask = the fixed lexicographic dedup rule; zero remaining degrees of freedom | mask chosen to maximize gain |
| (iv) owners on one received affine line | mask constrained to factor through the owner map `own(idx) = idx mod n_own` | mask may depend on the full support index |

**A structural note on clause (iv), both regimes:** clause (iv) restricts
the mask's *search space*. When clause (iii) is also imposed, the mask has
no search space left, so clause (iv) has nothing to restrict. Of the six
constraint sets, only **C_iii** has clause (iv) imposed while clause (iii)
is ablated. Consequently **C_iv is numerically identical to B by
construction** (both cells are recomputed independently in the verifier and
the identity is asserted as a cross-check, in both regimes). This is part of
the census finding: clauses (iii) and (iv) are not independent axes in
either operationalization, and any refinement of the dichotomy should say so
rather than listing four apparently-orthogonal clauses.

## Step 0: anchor reproduction

Before running either arm, PR #716's own construction is replayed
independently (own implementation, his published parameters and orbit-index
witness: `G=F_3^6`, `L=729`, `q=4`, his 182-orbit witness list):

```text
recomputed normalized q-gain = 1.1182491776918668
published value              = 1.1182491777
```

Both match to all ten published digits, confirming the
`kernel`/`convolution`/`normalized_gain` machinery before it is reused,
unchanged, in both arms below.

## Dense regime (primary): PR #717 Section 7 family

**Family** (verbatim from
`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`
Section 7): `A_i = 5^i` for `i=1..B`, `C = 2*sum(A_i)+1`,
`T = {A_i} u {C-A_i}` (`|T| = 2B`), supports = all `B`-subsets of `T` in
lexicographic index order (`M = C(2B,B)`), `Phi(S) = sum(S) mod C`, ambient
group `G = Z_C`. The verifier recomputes PR #717's own table row facts
exactly at every `B`:

```text
B  C      M    L_img  W(fiber@0)  max|S^S'| on fiber  WL/M
2  61     6    5      2           0  (<= a-2 = 0)     1.667
4  1561   70   41     6           2  (<= a-2 = 2)     3.514
6  39061  924  365    20          4  (<= a-2 = 4)     7.900
```

(`s_0 = BC/2 == 0 mod C` at every even `B`: the heavy fiber sits at `0`.)
`M/L_img` grows (`1.20 -> 1.71 -> 2.53`), i.e. this is genuinely the
fiber-dense regime the sparse arm lacks. **B=8 is excluded and stated**:
`C(B=8) = 976561` is prime, so it admits no coprime factor split and the
pure-python Good-Thomas DFT replay used by the verifier is infeasible there;
this is a printed exclusion, not a silent cap.

**Clause operationalization.** (i) imposed = columns are the literal `T`
above; ablated = a fixed deterministic non-superincreasing assignment mod
`C` (recomputed from `(B, C, salt)` by the verifier, checked `!= T`).
(ii) `tau(xi) = sum_{t in T} chi_xi(t)`; imposed = one full dyadic
`|tau|`-level (`|tau|>=1`); ablated = any union of complete tau-classes
including the `<1` class (`<= 2^7-1` unions, swept exhaustively).
(iii) imposed = lexicographic first-match dedup; ablated = free mask.
(iv) `own(idx) = idx mod 2B`; imposed (with (iii) ablated) = mask factors
through owner classes (`2^{2B}` unions, swept exhaustively at every `B` via
exact 4-way moment tensors).

**Search discipline (dense).** Exhaustive: single-level bands (all levels),
level-union bands (all unions), owner-union masks (all `2^{2B}`), free masks
at `B=2` (`2^6`). Certified lower bounds (local search, disclosed budgets in
the JSON): free masks at `B=4` (`2^70` space) and `B=6` (`2^924` space),
searched by warm starts (kernel-sign, heavy-fiber indicator, full mask,
dedup, random) plus greedy single-support flips, after an exact sweep of
four candidate masks across every band union. Every reported gain is
re-evaluated from its stored witness by a fresh DFT before storage, and the
verifier recomputes it again from the JSON witness.

**Results (dense).** `|G| = C in {61, 1561, 39061}` (factor 640). OLS fit of
`log(gain)` against `log|G|`:

```text
                C=61      C=1561    C=39061   | fitted     R^2
                (B=2)     (B=4)     (B=6)     | exponent
A  (free)       0.5051    0.4396    0.4831    | -0.0069    0.100
B  (all 4)      0.4041    0.3543    0.2091    | -0.1018    0.891
C_i  (no i)     0.4199    0.3192    0.2458    | -0.0829    1.000
C_ii (no ii)    0.4913    0.3920    0.3080    | -0.0723    1.000
C_iii(no iii)   0.5391    0.7682    0.8420    | +0.0690    0.898
C_iv (no iv)    0.4041    0.3543    0.2091    | -0.1018    0.891
```

**Reading the dense table.**

1. **Clause (iii) is the load-bearing clause in the dense regime.** C_iii is
   the only constraint set whose absolute gain GROWS with `|G|`
   (`0.539 -> 0.768 -> 0.842`, fitted exponent `+0.069`); every other set
   declines. The gap over the fully-imposed baseline widens geometrically:

   ```text
   C          C_iii / B
   61         1.3342
   1561       2.1680
   39061      4.0259
   ```

   The winning C_iii witness at every `B` is the FULL mask (all owner
   classes selected): no cherry-picked owner union is needed -- simply NOT
   applying first-match dedup lets the heavy-fiber multiplicities
   (`W = C(B,B/2)` supports on the single image point `0`) carry the
   projected norm. First-match dedup flattens every fiber to multiplicity 1
   and kills exactly this. This is consistent with PR #717 Section 7's
   witness being a pre-first-match object, and with PR #716 section 4.3's
   diagnosis that the abstract mask "is not shown to be the output of the
   semantic first-match atlas": in this family, the first-match rule is
   precisely the clause that separates bounded from growing.

2. **Set A does not grow even in the dense regime** (slope `-0.007`,
   `R^2=0.10`; plainly: flat). The reason is structural, and is itself a
   census finding: ablating clause (i) replaces the superincreasing columns
   by generic ones, whose subset sums are nearly collision-free
   (`L_img(arb) = 850` of `M = 924` at `B=6`, versus `365` for the certified
   columns) -- so the fiber load, i.e. the density `M/L_img` and the heavy
   fiber `W`, collapses, and the free mask has no multiplicity mass to
   concentrate. **The guardrail-type growth at these sizes needs more than
   density in the abstract: it needs the certified source columns present
   (to create the collision structure) and the first-match mask absent (to
   keep it).** Growth is therefore visible exactly in the cells that keep
   (i) and drop (iii) -- C_iii -- and nowhere else.

3. The observed growth exponent (`+0.069`) is well below the abstract
   `L^{1/2-1/q} = L^{1/4}` rate (q=4). At these sizes the fiber mechanism
   (`W ~ 2^B` against `|G|^{1/4} ~ 5^{B/4}`) is what carries the growth; no
   claim is made that the fitted exponent is the asymptotic rate (see
   Nonclaims).

## Sparse regime (secondary): moment-curve pairs over F_p

This was the census's first arm; it is retained in full because it carries
two findings the dense arm does not replace: the relative clause-(ii) gap
and the (iv)-redundant-given-(iii) observation (the latter now confirmed in
both regimes).

**Construction.** Rank `R=3`, `G = F_p^3`, `L = |G| = p^3`, source points
`T = F_p`, supports = all pairs (`M = C(p,2)`), `Phi(S) = v_i + v_j`,
columns `v_t = (1,t,t^2)` (imposed) or a fixed non-Vandermonde formula
(ablated, recomputed from `(t,R,p,salt)` by the verifier and checked to
differ at every source point); `tau(xi) = sum_t chi_xi(v_t)` with dyadic
levels over `|tau|>=1`; owner `own(idx) = idx mod p` (one point moving along
the line `z |-> 0 + z*1` in `F_p`); first-match dedup in the fixed
lexicographic support order. The ablated band family is unions of complete
scalar orbits of `G^`. Witnesses in the JSON. Note `M/L = O(1/p) -> 0`: the
support family thins as `p` grows -- the opposite regime from the dense arm,
and the reason the dense arm exists.

**Search discipline (sparse).** `p=3` (`L=27`): band search exhaustive (13
orbits, `2^13` subsets); mask search exhaustive (`M=3`). `p=5` (`L=125`):
band search local (31 orbits); mask search exhaustive (`M=10`). `p=7`
(`L=343`): band search local (57 orbits); owner/dyadic-cell mask searches
exhaustive (`M=21`); the fully free mask search in A is local. `p=11`
(`L=1331`): band search local (133 orbits); free mask search local (`M=55`);
owner-restricted mask search exhaustive (`2^11`). Reported maxima in
`local_search` cells are certified lower bounds with
`candidates_tried`/`candidates_total` printed in the JSON; exhaustive cells
are exact maxima over the stated candidate family (itself a modeling
choice: "union of complete scalar orbits" and "free 0/1 mask on the
realized image").

**Results (sparse).** `L in {27, 125, 343, 1331}` (factor ~49). OLS fit of
`log(gain)` against `log L`:

```text
                L=27      L=125     L=343     L=1331    | fitted     R^2
                (p=3)     (p=5)     (p=7)     (p=11)    | exponent
A  (free)       0.5248    0.3588    0.9730    0.3209    | -0.0521    0.029
B  (all 4)      0.3964    0.3405    0.3104    0.2757    | -0.0932    0.999
C_i  (no i)     0.3423    0.3405    0.3703    0.2757    | -0.0452    0.346
C_ii (no ii)    0.5135    0.4894    0.4670    0.4322    | -0.0441    0.979
C_iii(no iii)   0.3964*   0.3557    0.3256    0.2922    | -0.0787    0.998
C_iv (no iv)    0.3964    0.3405    0.3104    0.2757    | -0.0932    0.999
```

`*` at `p=3`, `M = C(3,2) = 3 = p`, so the owner map is a bijection on the
three supports and C_iii's owner-restricted search coincides with a free
per-support search; this coincidence is specific to `p=3`.

No constraint set grows here -- including A (its fit is dominated by the
`L=343` outlier `0.973`; `R^2=0.029`). The regime explanation, now confirmed
by the dense arm: with `a=2` fixed, `M/L -> 0` and there is no fiber mass
for any mask to concentrate. The sharpest sparse signal is *relative*: C_ii
(free band, fixed dedup mask) exceeds B at every `L` with a monotonically
growing ratio:

```text
L        C_ii / B
27       1.2953
125      1.4372
343      1.5046
1331     1.5680
```

So in the fiber-sparse regime, where the mask has nothing to exploit, the
band restriction (ii) is the clause whose ablation opens the clearest
relative gap -- whereas in the fiber-dense regime the mask clause (iii)
dominates and the band freedom matters little. The two regimes locate
different load-bearing clauses; a proof of the dichotomy's signed clause has
to be uniform across exactly this kind of regime split.

## Nonclaims

This packet does **not**:

- prove the charge-preserving semantic-or-signed dichotomy, or any half of
  it;
- prove or disprove the primitive Sidon/Fourier payment, A4, or primitive Q;
- establish an asymptotic statement of any kind -- every number above is an
  exact or certified-lower-bound value at one finite instance, not an
  `N -> infinity` limit; in particular the dense-arm fitted exponent
  `+0.069` is not claimed to be (or to converge to) the abstract
  `L^{1/2-1/q}` rate;
- decide PR #713's `(CAT)` ledger or its blocked cells, or pay PR #719's
  balanced mixed-sign residual;
- claim the `local_search` maxima are exact -- see each arm's search
  discipline; `B=8` is excluded with the printed reason (prime `C`), and
  the dense free-band family is the family of complete-tau-class unions,
  a strict subfamily of all symmetric bands (disclosed modeling choice,
  matched to the exhaustively-sweepable structure);
- claim the four clauses are independent -- see the clause-(iv) structural
  note (confirmed in both regimes);
- claim the specific column/band/mask formalizations here are the unique or
  canonical way to operationalize PR #716's four clauses; they are one
  concrete, replayable instantiation per regime.

## Replay

```bash
python3 experimental/scripts/verify_signed_minor_payment_clause_census_v1.py
python3 experimental/scripts/verify_signed_minor_payment_clause_census_v1.py --tamper-selftest
```

Certificate:
`experimental/data/certificates/signed-minor-payment-clause-census-v1/signed_minor_payment_clause_census_v1.json`
(sparse cells under `cells`/`fits`, dense cells under
`dense_cells`/`dense_fits`, PR #717 table replication under
`pr717_table_replication`, PR #716 anchor under `anchor_replication`).
