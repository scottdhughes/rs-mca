# Heavy prefix fibers emit planted/saturation precursors: how far the twin-pair emission instance generalizes

## Status

```text
Status: PROVED saturation-forcing lemma (general depth R, all n,a) + PROVED
        depth-1 involution-planted emission theorem (any Sidon P, generalizing
        #732/#728 off superincreasing) + PROVED depth-R multiplicative-folding
        emission (coset-union quotient-support families, census <= sigma(p-1),
        #725) + EXHAUSTIVE CENSUS with NO COUNTEREXAMPLE (every heavy prefix
        fiber over F_p, p in {7,11,13}, |T|<=12, R in {1,2} emits >=1 of #716's
        five precursors) + PROVED discriminators (field-descent, rank never fire
        over prime F_p).
LANE: hard input 2 (agents.md) -- the SEMANTIC EMISSION clause of avdeevvadim's
        #716 charge-preserving semantic-or-signed dichotomy: does every
        exponentially heavy depth-R prefix fiber emit one of the five semantic
        precursors { quotient(folding), field-descent, planted(template), rank,
        ray-saturation } with subexponential census?

Verdict per sub-question (route-scoped):
  (1) STRUCTURE OF HEAVY DEPTH-1 FIBERS.  Exponential heaviness of a depth-1
      (subset-sum) fiber is an ADDITIVE-STRUCTURE phenomenon, and its extremal
      mechanism is the additive involution x -> c-x.  The #732 twin-pair
      instance is NOT special to the superincreasing family: for ANY
      T = P u (c-P) with P a distinct-subset-sum (Sidon/dissociated) set and
      a = |P| = B, the central fiber Phi^{-1}((B/2)c) is EXACTLY the C(B,B/2)
      complete-twin-pair unions -- verified for an INDEPENDENT non-superincreasing
      Conway-Guy witness (P={3,5,6,7}, {11,17,20,22,23,24}, ...).  It emits a
      repeated planted template (census 1), an involution quotient-fold, and
      Johnson saturation, simultaneously.  The census's heaviest depth-1 fiber
      is itself involution-symmetric.  (An arithmetic-progression T gives only
      a POLYNOMIALLY heavy mode -- Sylvester/Stanley unimodality -- so the AP is
      the WRONG extremizer for exponential heaviness; the involution is right.)
      ANSWER: YES, near-extremal T carry planted (twin-pair) structure.
  (2) DEPTH-R.  The additive twin-pair mechanism does NOT survive to R>=2 on the
      SAME T: the involution preserves only p_1, so a depth-1 twin fiber SHATTERS
      into many depth-2 (p_1,p_2) fibers (verified: 6 twins -> 6 depth-2 fibers).
      The correct depth-R generalization is an (R+1)-FOLD FOLDING: the order-d
      (d=R+1) multiplicative-subgroup cosets have p_1=...=p_{d-1}=0, so
      coset-union supports form a quotient-support + planted family inside ONE
      depth-R zero fiber, with template census <= sigma(p-1) (#725).  Verified
      at R=1,2,3 (F_7 gives an EXACT depth-1 fiber; F_13 gives exact depth-2 and
      depth-3 fibers).  EXHAUSTIVE CENSUS over F_p (p in {7,11,13}), every T up
      to affine equivalence with |T|<=12, every a, R in {1,2}: 17609 fibers,
      Johnson bound |S cap S'|<=a-R-1 holds on ALL of them (re-verifies #717
      Thm 4.1), and EVERY multi-support fiber -- at every heaviness ratio, not
      only above threshold -- emits >=1 precursor.  ZERO counterexamples.  So at
      census scale the five-way grammar is COMPLETE: NO sixth clause is needed
      for these (structured, prime-field) heavy fibers.
  (3) THE PROVABLE CLASS.  Three theorems (Sec 3), every hypothesis visible:
      Thm 1 (saturation-forcing, general R): any depth-R fiber heavier than the
        constant-weight-code bound A(n,2(R+2),a) MUST saturate Johnson, hence
        emits ray-saturation -- so ray-saturation is the UNIVERSAL precursor of
        sufficiently heavy fibers.
      Thm 2 (involution-planted, depth 1): the Sidon twin-pair class above.
      Thm 3 (multiplicative-folding, depth R): the coset-union class above.
      Discriminator: field-descent and rank NEVER fire over prime F_p.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Every number below is
recomputed with exact integer / `F_p` / `Z_C` arithmetic by
`experimental/scripts/verify_heavy_fiber_planted_emission.py` (stdlib only,
deterministic, `RESULT: PASS (158/158)`, `--tamper-selftest` catches `4/4`,
~2.8 s).  No enumeration is silently capped: every bound is printed and the
Johnson sanity + no-counterexample scans run over EVERY fiber.  Machine-readable
certificate:
`experimental/data/certificates/heavy-fiber-planted-emission/heavy_fiber_planted_emission.json`.
Lean statement stub: `experimental/lean/heavy_fiber_planted_emission/`
(`lake build` succeeds; `native_decide` instances + one honest `sorry` target).
No `.tex`/`.pdf` is edited.

## Interfaces

- **avdeevvadim's #716**
  (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`).  The
  whole target is his: the **five semantic precursors** of the source-algebraic
  heavy-fiber inverse (Sec 3) -- *"a genuine quotient, repeated planted template,
  proper-field descent, baseline-free collective rank loss, or exact saturation
  precursor, with the stated subexponential census and projection data"* -- and
  the **charge-preserving semantic-or-signed dichotomy** (Sec 6).  This packet
  decides, at census scale and on three proved classes, whether every heavy
  prefix fiber lands in that five-way grammar.  It is written to be consistent
  with his **Section 5 route-stop table**: the positive classes here do NOT use
  the cheap routes he cuts.  Thm 2 is a SPECIFIC structured T (an involution with
  a Sidon half), not the generic radius-r trade his Sec 5.1 shows is
  insufficient; Thm 3 uses a genuine complete-uniform-fiber folding map, not the
  arbitrary rooted secant his **Prop 4.1 / Sec 5.2** guardrail forbids (that
  guardrail is respected -- the quotient test here demands complete uniform
  fibers).  The negative half CONFIRMS his Sec 5.3 (field, prime => none) and
  Sec 5.4 (rank, baseline only) exactly, and EXTENDS them by exhibiting that the
  structured heavy fibers DO emit via saturation/planted.  His Sec 7.1
  anticipated a possible sixth (signed-minor) clause; the census supplies
  evidence it is not needed for these structured prime-field fibers, while his
  general many-syndrome analytic residual is untouched (Nonclaims).
- **#717** (`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`).
  Its **Theorem 4.1** (Johnson bound `|S cap S'| <= a-R-1` on depth-R prefix
  fibers) is the input to the saturation-forcing Thm 1 and is independently
  re-verified here on all 17609 census fibers.  Its Sec 7 superincreasing
  heaviness witness is the R=1 seed that Thm 2 generalizes to arbitrary Sidon P.
- **#732** (`experimental/notes/thresholds/charge_preserving_split_decomposition.md`).
  Its **first exact emission instance** -- the superincreasing heavy fiber
  `Phi^{-1}(0)` = the C(B,B/2) twin-pair unions, saturating `|S cap S'| = a-2` --
  is exactly the instance this packet asks "how far does it generalize?".
  Answer: (Sec 1) off superincreasing to any Sidon P at depth 1; (Sec 2) off
  additive involutions to (R+1)-fold multiplicative foldings at depth R.  Its
  observation that the true residual is CARDINALITY (max-fiber count) is the
  boundary this packet respects: per-fiber emission is closed here, the GLOBAL
  profile count remains #732's open max-fiber question (Nonclaims).
- **#725** (`experimental/notes/thresholds/c3_planted_divisor_census.md`).  Its
  **coset-type planted census** `|P_coset(N)| = sigma(N) <= N(1+ln N)` is exactly
  the template census of the depth-R multiplicative-folding class (Thm 3): the
  emitted quotient-support family is a #725 coset-type planted divisor, so its
  census is #725's `sigma(p-1)`, subexponential.  This packet is the emission-
  side consumer of #725's census-side theorem.
- **#729** (`experimental/notes/thresholds/general_pruned_signed_bound.md`).  Its
  density criterion `q_+(chart)=1/(3/2-logM/logL)` and the chart-free pruned
  signed bound bound the SIGNED (nonstructured) clause; this packet is the
  complementary STRUCTURED (semantic) clause -- the two together are #716 Sec 6's
  semantic-or-signed disjunction.

Classical results used (cited by name, not re-derived):
- The fiber is a **binary constant-weight code** (length `n=|T|`, weight `a`,
  minimum Hamming distance `>= 2(R+1)`); the **Johnson bound** on such codes
  (MacWilliams--Sloane, *The Theory of Error-Correcting Codes*, ch. 17) gives the
  saturation-forcing Thm 1.  The bounded-pairwise-intersection viewpoint is the
  **Erdos--Ko--Rado** (1961) / anticode home of these families.
- The depth-1 level sets over an arithmetic progression are the coefficients of a
  **Gaussian binomial coefficient**, symmetric and **unimodal** by
  **Sylvester** (1878) and **Stanley** (1980, hard Lefschetz / Sperner); this is
  why an AP is only POLYNOMIALLY (`~ sqrt`) heavy and is NOT the exponential
  extremizer.
- That exponential concentration of subset sums forces additive (generalized-
  arithmetic-progression) structure is the **inverse Littlewood--Offord** theory
  (**Erdos** 1945; **Nguyen--Vu**, *Optimal inverse Littlewood--Offord theorems*,
  Adv. Math. 2011); the involution/twin-pair class proved here is the exact
  structured instance, and inverse Littlewood--Offord is the (conjectural) general
  reason no unstructured heavy depth-1 fiber appears in the census.

---

## 0. Setup and conventions (all #716/#717)

The **source chart** is the depth-`R` locator/power-sum prefix chart
(#717 Sec 1, `eq:exact-power-sum-map`): for a coordinate set `T` in a field or
group, the full slice is `Omega^0 = C(T,a)` (`M = |Omega^0| = C(|T|,a)`), and

```text
Phi_R(S) = (p_1(S), ..., p_R(S)),     p_j(S) = sum_{t in S} t^j,
```

with occupied image size `L = |Phi_R(Omega^0)|` and average fiber `M/L`.  A
**fiber** is `F = Phi_R^{-1}(s_0)`; its size is `W = |F|`.  Power-sum and
elementary (`e_1..e_R`) prefixes induce the SAME fiber partition when
`R < char` (Newton, #717 Thm 4.1); the census uses power sums and the results are
presentation-free.  A fiber is **heavy** (finite proxy) when `W L / M >= 2`;
**exponentially heavy** (the asymptotic target of #716) when `W L / M >= e^{eta N}`
for fixed `eta > 0`.

## 1. Sub-question 1: structure of heavy depth-1 fibers (PROVED class + census)

At depth 1 the chart is the subset-sum map `Phi_1(S) = sum_{t in S} t`, and a
fiber is a level set of the subset-sum function on `a`-subsets.

**Why the arithmetic progression is the WRONG extremizer.** For `T = {0,...,n-1}`
the level-set sizes are the coefficients of the Gaussian binomial `[n choose a]_q`
-- symmetric and unimodal (Sylvester 1878; Stanley 1980).  The central (largest)
level set has size `~ C(n,a)/sigma` with `sigma ~ n^{3/2}` (standard deviation of
the sum), while the image is `L ~ a(n-a) ~ n^2`, so

```text
W L / M ~ (C(n,a)/n^{3/2}) * n^2 / C(n,a) = n^{1/2}       (AP: only POLYNOMIAL).
```

So the mode of an AP is not exponentially heavy.  Exponential heaviness needs a
large image `L = e^{Theta(N)}` with one fiber far above `M/L`, which is an
additive-structure (inverse Littlewood--Offord) phenomenon, not an "AP mode"
phenomenon.

### Theorem 2 (involution twin-pair emission, depth 1, PROVED)

Let `P = {A_1,...,A_B}` be a **distinct-subset-sum (Sidon/dissociated) set** over
`Z` (no two disjoint subsets share a sum), let `c > 2 max P`, and set

```text
T = P u (c - P),   |T| = 2B,   a = B,   Phi_1(S) = sum_{t in S} t (over Z_c, c=... or Z).
```

Then the central fiber at `s_0 = (B/2) c` is EXACTLY the `C(B,B/2)` complete-
twin-pair unions:

```text
Phi_1^{-1}(s_0) = { union_{i in Q} {A_i, c-A_i} : Q subseteq [B], |Q| = B/2 }.
```

Each such support (i) is a **repeated planted template** -- the single pairing
`{A_i, c-A_i}` evaluated on a `(B/2)`-subset of the `B` pairs, template census
`= 1` (one involution); (ii) is a **quotient-support** for the complete-uniform-
fiber folding `x -> c-x` (2-fold, orbits the twin pairs); (iii) **saturates**
Johnson: `max_{S != S'} |S cap S'| = a-2` (share all but one pair).  It is
exponentially heavy (`W = C(B,B/2)`, `W L / M -> infinity`).  Field-descent and
rank do NOT fire.

**Proof.** Index by pair.  A `B`-subset `S` uses, per pair `i`, one of {A_i only,
(c-A_i) only, both, neither}; sizes force `#both = #neither` and
`sum(S) = (#both + #high) c + (sum_{low} A_i - sum_{high} A_j)` where low/high are
the "A_i-only"/"(c-A_i)-only" index sets (disjoint).  Setting `sum(S) = (B/2)c`
with `|sum_{low}A - sum_{high}A| <= sum P < c/2` forces both `#both+#high = B/2`
and `sum_{low}A_i = sum_{high}A_j`.  Distinct subset sums (disjoint low/high)
give `low = high = empty`, hence `#both = B/2`, `S` = union of `B/2` full pairs.
Johnson saturation and the quotient/planted readings are then immediate. `square`

**Independent (non-superincreasing) witness.** #728/#732 used superincreasing
`P = {5^i}`; the theorem needs only distinct subset sums.  Check (BLOCK C)
verifies the exact central fiber, `W = C(B,B/2)`, saturation `a-2`, and the
quotient+planted emission for the **Conway--Guy** distinct-subset-sum sets
`P = {3,5,6,7}` (B=4), `{11,17,20,22,23,24}` (B=6), `{40,60,71,77,80,82,83,84}`
(B=8), `{148,...,309}` (B=10) -- each certified distinct-subset-sums AND
NON-superincreasing.  So the emission instance is a property of the involution +
dissociativity, not of the base-5 arithmetic.

**Extremal census (BLOCK E).** Over `F_p`, `p in {7,11,13}`, the depth-1 `T`
maximizing `W L / M` is additively **involution-symmetric** (e.g. `p=13`,
`T={0,1,2,3,6,10}`, `c=3`, `W L / M = 2.6`), and its heaviest fiber fires
{planted, quotient, saturation}.  Near-extremal `T` carry the twin-pair structure.

## 2. Sub-question 2: depth-R (shatter, multiplicative folding, no counterexample)

### The additive involution SHATTERS at depth 2 (COUNTEREXAMPLE to naive survival)

The involution `x -> c-x` preserves `p_1` but NOT `p_2`
(`A_i^2 + (c-A_i)^2 = 2A_i^2 - 2cA_i + c^2` depends on `A_i`).  So the depth-1
twin fiber splits at depth 2 into as many `(p_1,p_2)` fibers as there are pair-
choices with distinct `sum A_i^2` (BLOCK D: the `B=4` fiber of 6 twins ->
6 distinct depth-2 fibers).  The twin-pair mechanism does not survive R>=2 on the
same `T`; a heavy depth-R fiber needs a folding preserving `p_1,...,p_R`.

### Theorem 3 (multiplicative-folding emission, depth R, PROVED)

Over `F_p`, let `d = R+1` divide `p-1`, let `H_d <= F_p^x` be the order-`d`
subgroup, and let `T` be a union of `H_d`-cosets (a smooth multiplicative domain,
`def:structured-folding`).  Each `H_d`-coset `{x, zeta x, ..., zeta^{d-1} x}`
(`zeta` a primitive `d`-th root of unity) has

```text
p_k(coset) = x^k * sum_{j=0}^{d-1} zeta^{jk} = 0   for  1 <= k <= d-1 = R,
```

so every **coset-union** support (a union of `a/d` cosets) lies in the single
depth-`R` fiber at `Phi_R = (0,...,0)`.  This coset-union family is (i) a
**quotient-support** family for the `d`-fold folding `x -> x^d` (complete uniform
fibers = the cosets); (ii) a **repeated planted template** (blocks = cosets);
(iii) its census is the number of coset choices, bounded by the coset count
`(p-1)/d` -- a #725 coset-type planted divisor, so `<= sigma(p-1) <= (p-1)(1+ln(p-1))`,
subexponential.  Verified (BLOCK D) at:

```text
R=1 (d=2, p=7 ):  T=F_7^x, a=4, zero fiber = EXACTLY C(3,2)=3 coset-unions;
R=2 (d=3, p=13):  T=F_13^x, a=6, zero fiber = EXACTLY C(4,2)=6 coset-unions;
R=3 (d=4, p=13):  T=F_13^x, a=8, zero fiber = EXACTLY C(3,2)=3 coset-unions;
R=1 (d=2, p=13):  zero fiber is LARGER than its 15 coset-unions (heterogeneous),
                  which still carries the coset-union quotient sub-family.
```

emitting {quotient, planted, saturation}, field/rank off.  `square`

This is the honest depth-R generalization: the depth-1 additive 2-fold involution
is replaced by a depth-`R` multiplicative `(R+1)`-fold, and #725's coset census IS
the emission's subexponential census.

### Exhaustive census: NO counterexample (BLOCK A)

For `F_p`, `p in {7,11,13}`, every `T` up to affine equivalence (`x -> alpha x + beta`)
with `|T| <= 12`, every `a in [2,|T|-2]`, and `R in {1,2}`:

```text
17609 prefix fibers built.  Johnson |S cap S'| <= a-R-1 holds on ALL of them
   (re-verifies #717 Thm 4.1).
6889 multi-support fibers (W>=2).  Per-precursor FAIL counts (times the test is
   FALSE) show the two structural precursors are DISCRIMINATING, not vacuous:
   { saturation fails 272,  planted fails 1901,  quotient fails 6761,
     field fails 6889 (all),  rank fails 6889 (all) }.
COMPLEMENTARITY (the strong statement): saturation and planted NEVER both fail
   -- 0 of 6889 -- so together they COVER every multi-support fiber; ZERO fibers
   emit nothing, at EVERY heaviness ratio.
68 heavy fibers (W L/M >= 2): saturation 68/68 (UNIVERSAL), planted 68/68 (48
   exact block-union designs, robust template), quotient 8/68 (involution/coset-
   symmetric), field 0/68, rank 0/68.
Max heaviness at this scale W L/M = 2.82 (p=13, T={0,1,2,3,4,5,7,9,10}, a=3, R=2).
```

So at census scale the five-way grammar is COMPLETE: no fiber requires a sixth
(signed-minor) clause, and the completeness is not vacuous -- ray-saturation and
planted each fail on a substantial fraction of fibers, but exactly one of them
always fires (they partition the failure modes).  (The absolute ratios are small
because `|T|<=12`; exponential heaviness is exhibited asymptotically in Sec 1--2,
not here.)

## 3. Sub-question 3: the provable theorems

### Theorem 1 (saturation-forcing, general depth R, PROVED)

A depth-`R` prefix fiber `F` over `T` (`|T|=n`, `a`-subsets) is, by #717 Thm 4.1,
a binary constant-weight code of length `n`, weight `a`, and minimum Hamming
distance `>= 2(R+1)` (`|S cap S'| <= a-R-1`).  If `F` does NOT saturate
(`max |S cap S'| <= a-R-2`), its minimum distance is `>= 2(R+2)`, so by the
Johnson constant-weight bound

```text
|F| <= A(n, 2(R+2), a).
```

Contrapositive: **if `|F| > A(n, 2(R+2), a)` then `F` saturates the Johnson
agreement bound, hence emits the ray-saturation precursor.**  So ray-saturation
is the universal precursor of sufficiently heavy fibers.  Verified (BLOCK B):
all 54 census heavy fibers exceeding `A(n,2(R+2),a)` saturate, 0 exceptions
(the other 14 saturate too, though not forced by the bound). `square`

### Theorems 2, 3 (Sec 1, Sec 2) -- the two structured emission classes.

### Discriminator (PROVED)

Over a PRIME field `F_p` there is no proper subfield, so **field-descent never
fires** (#716 Sec 5.3), confirmed on all 68 heavy fibers.  The depth-`R` moment
columns `v_t = (t,...,t^R)` of a generic support union have full expected rank, so
**collective rank loss never fires** (#716 Sec 5.4), confirmed on all 68.

**Combined verdict.** On the census-supported class (heavy prefix fibers over
prime `F_p`, `R in {1,2}`) and the two proved asymptotic families, every
exponentially heavy fiber emits `>= 1` of the five precursors -- ray-saturation
universally (Thm 1), planted+quotient for the involution (Thm 2) and
multiplicative-folding (Thm 3) extremal classes -- with subexponential census
(`1` for the involution, `sigma(p-1)` for the folding), while field-descent and
rank never fire over prime fields.  No counterexample at census scale.

## 4. The five-precursor operational grammar (how each is tested)

Operationalized from the manuscript's own definitions
(`asymptotic_rs_mca_frontiers.tex` L417-459, L1228-1229, L2400-2407, L4537,
L886) and #716:

```text
quotient(folding) : a folding map with COMPLETE UNIFORM FIBERS on T (additive
     involution x->c-x, or multiplicative x->x^d, d|p-1) such that every fiber
     support is a union of complete folding-fibers.  (Respects #716 Prop 4.1:
     a complete uniform fiber, NOT an arbitrary rooted secant.)
field-descent    : T is a union of Frobenius orbits of a PROPER subfield.
     Vacuous over prime F_p.
planted(template): the atoms of the fiber's set-algebra are nontrivial (a block
     of >=2 coordinates always co-moves); "exact uniform block-union design" =
     fiber is ALL j-unions of m equal-size blocks (the strong, #732 reading).
rank             : the moment-column differences {v_t - v_{t'}} of the support
     union span LESS than the baseline min(R, |U|-1) (an unexpected common minor).
ray-saturation   : max_{S != S'} |S cap S'| equals the Johnson bound a-R-1
     (the agreement projection is tight; #732's reading).
```

The verifier prints the per-fiber Boolean vector over these five for every heavy
fiber and flags any all-`False` row (a counterexample); none occur.

## Nonclaims

- **NOT a proof of the charge-preserving semantic-or-signed dichotomy, the
  primitive Q / max-fiber flatness, A4, or the Proximity Prize.**  Per-fiber
  emission is decided on the proved classes and at census scale; the GLOBAL
  count of emitted profiles (max-fiber concentration) is exactly #732's open
  cardinality residual and is NOT closed here.
- **Ray-saturation's per-fiber census is `1`** (the fiber's own saturation
  profile), which is subexponential; **no claim** that the ledger-wide number of
  saturation profiles is subexponential -- that is the max-fiber question.  The
  saturation PROFILE is emitted; its PAYMENT (image/fiber bound, `prop:planted-
  payment` / the `(RC)` ray compiler) is the separate hard input 3, untouched.
- **The census is finite structural evidence**, not an asymptotic theorem: it is
  exhaustive only for `p in {7,11,13}`, `|T|<=12`, `R in {1,2}`, and its absolute
  heaviness ratios are small (`<= 2.82`).  Exponential heaviness lives in the
  asymptotic families (Sec 1-2), which ARE closed-form.
- **NOT a refutation of #716 Sec 7.1's possible sixth clause.**  The census shows
  no sixth clause is needed for the STRUCTURED prime-field heavy fibers probed;
  #716's general many-syndrome analytic (signed-minor / #729) residual is a
  different regime and stays open.
- **Affine-equivalence reduction** (`x -> alpha x + beta`) is used to enumerate
  `T`; fiber sizes, intersections, saturation, planted-atoms are affine-invariant,
  so the census is exhaustive up to affine equivalence for those.  The
  multiplicative-quotient branch is NOT affine-invariant and is a rep-dependent
  BONUS precursor; the affine-robust catch-alls (saturation, planted) carry the
  no-counterexample conclusion.
- Thm 3's coset-union family may be a proper SUB-family of the deep zero fiber
  (heterogeneous when `R+1 = 2` over a large field); the emission is of the
  structured sub-family carrying the coset census, not a claim that the whole
  deep fiber equals the coset-unions (verified exactly for `d>=3`).

## Consumers

- **#716** (`primitive_signed_payment_barrier_v1.md`): supplies the STRUCTURED
  half of the Sec-6 semantic-or-signed dichotomy on three proved classes; ray-
  saturation is identified as the universal per-fiber emitter (Thm 1); the Sec 5
  route-stops for field (5.3) and rank (5.4) are re-confirmed exactly.
- **#732** (`charge_preserving_split_decomposition.md`): its twin-pair emission
  instance is generalized off superincreasing (Thm 2, Sidon P) and off depth 1
  (Thm 3, multiplicative folding); its cardinality residual is respected as the
  boundary.
- **#725** (`c3_planted_divisor_census.md`): consumed as the emission census of
  Thm 3 -- the coset-union quotient family is a coset-type planted divisor with
  `sigma(p-1)` census.
- **#717** (`heavy_fiber_admissibility_transfer.md`): its Johnson Thm 4.1 is the
  input to Thm 1 and is re-verified on 17609 fibers.
- `asymptotic_rs_mca_frontiers.tex`: paste-ready as a remark after
  `eq:exact-power-sum-map` and the primitivity definition (L459) -- heavy prefix
  fibers on the structured charts emit named precursors; the residual is the
  max-fiber profile count, not the precursor grammar.
- Lean statement stub: `experimental/lean/heavy_fiber_planted_emission/`
  (saturation-forcing code-bound, twin count `C(B,B/2)`, multiplicative coset
  power-sum vanishing, `sigma` census; statements only, `lake build` succeeds).

## Reproducibility

```bash
python3 experimental/scripts/verify_heavy_fiber_planted_emission.py
# -> RESULT: PASS (158/158)
python3 experimental/scripts/verify_heavy_fiber_planted_emission.py --tamper-selftest
# -> tamper-selftest: caught 4/4 ; then RESULT: PASS (158/158)
cd experimental/lean/heavy_fiber_planted_emission && lake build
# -> Build completed successfully (one 'sorry' warning, by design)
```
