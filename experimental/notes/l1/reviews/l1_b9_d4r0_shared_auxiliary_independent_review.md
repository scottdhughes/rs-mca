# Independent Review: `d=4,r=0` Shared Auxiliary-Johnson Ledger

## Statement audited

This is a fresh, read-only implication-chain and downstream-ledger audit of the
claim that, for the frozen row

```text
(q,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2),
```

the complete exact `d=4,r=0` stratum is one fixed sunflower auxiliary layer
and therefore has the shared upper bound

```text
135,470 -> 3.
```

The proposed bookkeeping places the single charge `3` on the original
unresolved `(t,a_i)=(3,(3,3,2))` carrier and assigns zero *incremental* charge
to the other ten cells.  It would change the already-banked 41331 totals by

```text
all-profile: 776,979 -> 641,512,
unresolved:  212,755 -> 104,914.
```

This audit does not authorize any aggregation across `r=0` and `r=1`.

## Files and exact source anchors read

- `agents.md`, including the experimental-status, first-match, exact-ledger,
  and review-independence rules.
- `experimental/cap25_cap_v13_raw.tex`:
  - `thm:capf-johnson-list`, lines 6221--6238, and its proof, lines
    6240--6272;
  - `def:capf-concrete-sunflower`, lines 6282--6300;
  - `prop:capf-concrete-sunflower`, lines 6302--6335;
  - `def:capf-sunflower-layer`, lines 6337--6351;
  - `prop:capf-pma`, lines 6353--6365;
  - `cor:capf-pma-johnson`, lines 6367--6381.
- `experimental/scripts/verify_l1_mixed_petal_frontier_ledger.py`:
  the frozen-layout construction, lines 107--135, and the exact profile
  generator, lines 188--325.
- `experimental/scripts/verify_l1_b9_frontier_41331_owner_partition.py`,
  lines 81--87, for the concrete core, petal, and background partition.
- `experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py`
  and
  `experimental/data/certificates/l1-b9-frontier-41331/ledger_certificate.json`
  for the banked predecessor totals and carrier convention.
- `experimental/notes/l1/l1_pma_auxiliary_johnson.md`, especially the
  layer-versus-profile distinction at lines 68--81.
- `experimental/notes/l1/l1_b9_d4r0_shared_auxiliary_johnson.md`, the proposed
  theorem-scope and ledger statement under review.

No sibling `AGENTS.override.md` supplied additional governing instructions.

## Dependencies

- **PROVEN:** The concrete quotient map
  `P -> (P-P_star)/L_(Y\D_0)` injects a complete fixed `(D_0,R_0)` layer into
  degree-`<=d` polynomials (`prop:capf-concrete-sunflower`).
- **PROVEN:** The image agrees with the one auxiliary word `U_(D_0)` on at
  least `a=sigma+d+1-r` points of the common petal domain
  (`prop:capf-pma`).
- **PROVEN:** Two distinct degree-`<=d` polynomials agree on at most `d`
  distinct evaluation points, and `thm:capf-johnson-list(ii)` gives the sharp
  agreement-list bound used by `cor:capf-pma-johnson`.
- **EXACT:** The frozen domain is the disjoint union of a four-point core,
  three four-point petals, and a two-point background.  At `d=4`, the missed
  core is the whole core, so there is exactly one `D_0`; at `r=0`, there is
  exactly one `R_0`, namely the empty set.
- **EXACT:** The eleven profile cells below exhaust and disjointly partition
  the exact `d=4,r=0` support profiles represented by the ledger.
- **IMPORTED AND REPLAYABLE:** The predecessor ledger has banked totals
  `776,979` and `212,755`.  The new certificate must content-address and replay
  that exact predecessor before the candidate values are banked.
- **UNPROVEN AND UNUSED:** A common injection or payment across different
  residual counts `r`, including the suggested replacement of `72+3` by
  `36`.

## Fixed-layer calculation

The concrete fixed layer has

```text
D_0 = core,               number of choices = binom(4,4) = 1,
R_0 = empty,              number of choices = binom(2,0) = 1,
|T| = M*ell = 3*4 = 12,
a   = sigma+d+1-r = 3+4+1-0 = 8,
d   = 4.
```

Exact `d=4,r=0` means that a codeword has no core or background agreement.
Because the frozen 18-point domain is exhausted by the core, background, and
petals, every such listed codeword satisfies the containment condition in
`def:capf-concrete-sunflower`.  Hence all of them enter the same concrete
`(D_0,R_0)` layer; there is no support-pattern or occupancy-profile index in
the auxiliary map.

The strict Johnson margin and bound are

```text
a^2-d|T| = 8^2-4*12 = 16 > 0,
|T|(a-d)/(a^2-d|T|) = 12*(8-4)/16 = 3.
```

The unique-decoding alternative does not apply: `2a=16=|T|+d`, whereas
`thm:capf-johnson-list(i)` requires a strict inequality.  This causes no gap,
because part (ii) has the strict positive margin `16` and gives the asserted
bound `3` directly.

## Eleven-cell exhaustiveness and disjointness

For an exact support profile, write `t` for the number of touched petals and
`a_i` for the nonincreasing positive petal-hit counts.  Listedness gives

```text
sum_i a_i >= ell+d-r = 8,
1 <= a_i <= min(ell,d) = 4.
```

One petal cannot supply eight agreements and only three petals exist.  Thus
`t` is `2` or `3`.  For `t=2`, the only possibility is `(4,4)`.  For `t=3`,
the ten nonincreasing triples in `[1,4]` with sum at least eight are exactly

```text
(4,4,4), (4,4,3), (4,4,2), (4,4,1), (4,3,3),
(4,3,2), (4,3,1), (4,2,2), (3,3,3), (3,3,2).
```

The exact frozen counts are:

| `t` | `a_i` | support patterns | prior charge | prior route |
|---:|---|---:|---:|---|
| 2 | `(4,4)` | 3 | 57 | full petal |
| 3 | `(4,4,4)` | 1 | 19 | full petal |
| 3 | `(4,4,3)` | 12 | 228 | global Johnson |
| 3 | `(4,4,2)` | 18 | 342 | global Johnson |
| 3 | `(4,4,1)` | 12 | 228 | global Johnson |
| 3 | `(4,3,3)` | 48 | 912 | global Johnson |
| 3 | `(4,3,2)` | 144 | 2,736 | global Johnson |
| 3 | `(4,3,1)` | 96 | 1,824 | unresolved |
| 3 | `(4,2,2)` | 108 | 2,052 | unresolved |
| 3 | `(3,3,3)` | 64 | 23,104 | global Johnson |
| 3 | `(3,3,2)` | 288 | 103,968 | unresolved / proposed carrier |

The pattern formula is

```text
binom(2,0) * binom(3,t)
* (multiset assignments to labelled petals)
* product_i binom(4,a_i).
```

It gives `794` patterns.  Applying the predecessor B3 exponent
`max(0,4-max(0,a_1)+1)` gives total charge `135,470`.  The three original
unresolved charges sum to

```text
1,824 + 2,052 + 103,968 = 107,844.
```

Disjointness is exact, not probabilistic: a codeword's exact agreement set has
one intersection with each labelled petal, which determines its positive hit
multiset and therefore one profile cell.  Equal hit sizes are handled by the
multiset-assignment factor and do not duplicate a support pattern.  Exact
`d=4,r=0` also prevents overlap with any other core-defect or background
stratum.  A planted petal codeword agrees on the core and therefore lies at
`d=0`, not in this scope.

## Carrier and ledger arithmetic

The cap `3` is a bound on the union of all eleven cells.  It must be charged
once, not once per support pattern or once per profile.  Placing the sole
carrier on the original unresolved `(3,3,2)` row is sound under the existing
ledger convention:

```text
776,979 - 135,470 + 3 = 641,512,
212,755 - 107,844 + 3 = 104,914.
```

The ten zero entries mean only `COVERED_BY_THE_SHARED_ENVELOPE`; they are not
standalone zero-cardinality claims.  Likewise, the carrier does not license a
second `+3` elsewhere.  Keeping the carrier on an original unresolved row
conservatively retains the common cap once in the unresolved subtotal.

## Explicit no-cross-`r` finding

`cor:capf-pma-johnson` is stated for one fixed `(D_0,R_0)` layer.  The `r=0`
layer uses `R_0=empty` and agreement threshold `a=8`.  The separately banked
`r=1` result uses two different singleton `R_0` layers and threshold `a=7`.
The cited corollary does not state that their union injects into one common
list without duplicated layer charges, nor does it establish the coverage and
deduplication needed for a cross-`r` ledger regrouping.

Therefore this audit explicitly rejects any present claim

```text
72 + 3 -> 36.
```

The banked `r=1` charge `72` remains unchanged.  A stronger saving would need
a separately stated cross-layer injection and coverage lemma, its own exact
certificate, and a fresh independent review.

## Parameter dependence

This is an exact finite statement at `GF(19)` and
`(n,k,sigma,ell,M,b)=(18,5,3,4,3,2)`.  The cap `3` has no hidden asymptotic
dependence.  The symbol `T` here denotes the twelve-point petal domain, not a
time parameter; there are no parameters `Y`, `mathcal L`,
`mathcal L_(bar I)`, or `h` in the audited implication.  No field, challenge,
generated-field, or denominator ledger is merged.

## Layer-cake / dyadic summability

Not applicable.  There is no layer-cake decomposition, dyadic weighting, or
additive tail error.

## Moment / Markov / Chebyshev

Not applicable.  The proof uses finite incidence counting and the
`kappa`-intersecting Johnson inequality, not a moment bound or probabilistic
tail estimate.

## Edge cases and notation

- The Johnson inequality is used in its strict-margin regime (`16>0`), not at
  a zero denominator.
- The agreement threshold satisfies `0<a=8<=|T|=12`.
- `d=4>0`, so the equivalent few-petal boundary statement is defined.
- `D_0` and `R_0` each have exactly one choice; no restored-core,
  background-choice, profile, or periodic-support multiplier is allowed.
- Empty `R_0` is handled directly by the concrete layer definition: exact
  `r=0` plus the no-outside-agreements clause excludes both background points.
- Zero- and one-petal profiles are impossible; `t>3` is impossible.
- The full-core miss does not create a restored-core refinement.
- `T` and `T_i` are unambiguous petal-domain notation in the source.
- The carrier zeroes are incremental ledger allocations, not profile-size
  assertions.

No edge case or notation ambiguity changes the verdict.

## Numerical evidence

The profile list, support multiplicities, charges, and totals were recomputed
with exact Python integer arithmetic from the frozen profile generator and the
banked 41331 row reconstruction.  These are deterministic finite calculations,
not floating-point or random evidence.  They establish only this frozen local
ledger implication; they do not establish an asymptotic mixed-petal theorem.

## Verdict

**GREEN - proof obligation appears satisfied with dependencies verified.**

## Ledger authorization

**YES, conditionally on certificate replay and hash-link only.**  The theorem
scope, eleven-cell coverage, carrier semantics, and candidate arithmetic are
sound.  Authorize local banking once the new mutation-tested verifier exactly
reconstructs the banked predecessor, emits the eleven-cell scope above,
reproduces `135,470 -> 3`, `641,512`, and `104,914`, rejects cross-`r`
aggregation, and content-addresses this review.  This is not authorization for
a global theorem, `m>2`, PR `#763`, Lean, or a cross-`r` saving.

## Remaining risks

- The new verifier and certificate were not part of this theorem-only review;
  a failed exact replay or hash link blocks banking.
- The predecessor `r=1` cap `72` remains separate and unchanged.
- Positive unresolved mass `104,914` remains after the candidate payment.
- The next largest row `(ell,d,r,t,a_i)=(4,3,1,3,(3,2,1))` has auxiliary
  margin zero and needs a separate owner argument.
- Nothing here identifies the finite ledger with a closed asymptotic profile
  envelope.

## Minimal next action

Run the new ledger verifier in normal and mutation modes, verify its
content-addresses against the banked 41331 certificate, theorem source, scope
note, and this independent review, and bank only if every check reproduces the
exact values above.

Files modified by this review: this review file only.
