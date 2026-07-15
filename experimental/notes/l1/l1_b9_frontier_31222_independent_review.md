# Independent audit: L1 B9 frontier `(3,1,3,(2,2,2))`

Date: 2026-07-14
Reviewer: fresh-context Codex read-only audit
Verdict: **YELLOW -- promising but unresolved; do not authorize global proof.**

## Statement audited

The implication chain for the frozen profile

```text
(ell,d,r,t,a_i)=(4,3,1,3,(2,2,2)),
(G2,GR)=(4,5),
```

from the existing-owner partition through the unchanged ledger, the frozen
fixed-syndrome cubic system, the exact `GF(19)` census, the two compatible
ambient rank-drop lines, and the representative CAS replay.

## Files/sections read

- `experimental/notes/l1/l1_mixed_petal_residual_frontier_ledger.md`, the
  `(3,1,3,(2,2,2))` section and proof-status ledger.
- `experimental/scripts/verify_l1_b9_frontier_31222_owner_partition.py` and its
  v3 certificate.
- `experimental/scripts/analyze_l1_b9_frontier_31222.sage` and its census
  certificate.
- `experimental/scripts/verify_l1_b9_frontier_31222_cas.py` and its CAS
  certificate.
- `experimental/cap25_cap_v13_raw.tex`,
  `thm:stabilizer-partition` and `cor:periodic-support-count`.
- `experimental/asymptotic_rs_mca_frontiers.tex`,
  `prop:stabilizer-payment`, `prop:quotient-descent`, and the stabilizer and
  invariant-descent packages.

The review modified no files. During review the generating agent corrected two
findings raised by the reviewer: the missing restored-core support refinements,
and the distinction between direct periodic-support counting and invariant
quotient descent.

## Dependencies

- **PROVEN:** The 432 cofactor-support patterns have 1,728 restored-core
  refinements. Exactly nine full supports have stabilizer order two. Each has
  the existing one-support-one-line periodic owner with bound one; the other
  1,719 refinements remain unpaid after that first match.
- **PROVEN:** Periodic support counting does not require received-word descent;
  invariant quotient descent does.
- **PROVEN:** The fixed coefficient matrix is `12 x 9` of rank nine. The three
  CRT compatibility equations are the `X^3,X^4,X^5` coefficients of
  `FG mod B`, and the moving monic-cubic system satisfies
  `rank(C)=9+rank(C_reduced)`.
- **EXACT FINITE:** The exhaustive `GF(19)` census and independent
  support-subset decoder agree on zero actual target codewords.
- **EXACT REPRESENTATIVE:** Python, Singular, and Macaulay2 agree on the two
  compatible `(11,11)` and representative inconsistent `(11,12)` systems and
  their displayed minors.
- **IMPORTED:** The previous all-profile bound `1,503,967` and unresolved bound
  `668,803` are hash-linked, but were not re-audited end to end here.
- **UNPROVEN:** A uniform symbolic classification or payment of the compatible
  rank-drop locus.

## Parameter dependence

The computation is fixed at

```text
(p,n,k,sigma,ell,M,b)=(19,18,5,3,4,3,2)
```

with the sequential multiplicative domain and labels `(1,2,3)`. The charge
`155,952=432*19^2` is finite-row arithmetic, not a uniform-in-`q` theorem.

The unchanged ledger is conservative. The `q^2` injection bounds the aggregate
of four restored-core refinements; it does not imply a `q^2-1` bound after one
refinement receives a separate owner. The periodic owner bound nine is
recorded, but no mass is subtracted without a disjoint injection.

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.

## Edge cases / notation

- The selected seven-point cofactor support is not the full eight-point
  agreement support; the v3 certificate now checks both levels.
- Auxiliary Johnson has margin `6^2-12*3=0`, so the strict gate does not pay.
- Global Johnson has `lambda-lambda_J=-1`.
- B11 has `(d-ell,G2,GR)=(-1,4,5)`, so neither zero-excess gate pays.
- `UNPAID_PRIMITIVE` is only an aggregate terminal label for the named owner
  stack, not a certificate of full primitivity.
- Neither compatible ambient cubic line meets the four actual split
  missed-core locator points. The lines remain unpaid.
- Zero target codewords for the frozen received word do not imply a uniform
  profile payment.

## Numerical evidence

The exhaustive `GF(19)` census gives:

```text
408 patterns: (rank(C),rank([C|b]))=(12,12),
 22 patterns: (rank(C),rank([C|b]))=(11,12),
  2 patterns: (rank(C),rank([C|b]))=(11,11), 19 ambient cubics each,
all 1,728 fixed actual-core systems: (rank(A),rank([A|b_F]))=(9,10),
ambient monic cubics: 446,
actual target occurrences: 0,
independent-decoder targets: 0.
```

This exactly describes the frozen finite instance only.

## Verdict

**YELLOW -- promising but unresolved; do not authorize global proof.**

The v3 packet is internally coherent and suitable for handoff. The aggregate
no-subtraction decision is conservative. This is a fresh internal audit, not a
cross-model or human review, and no new charge is banked.

## Remaining risks

- The prior complete ledger totals remain imported rather than independently
  rederived in this audit.
- The `q^2` injection is not disjoint by restored core hit, so the nine
  periodic owners do not improve the banked charge.
- The CAS packet checks four hardcoded representatives; it does not
  independently discover all rank strata.
- The two compatible lines may be finite artifacts or shadows of a genuine
  uniform primitive component.
- The zero-target result is specific to the frozen sequential sunflower.

## Minimal next action

Prove one uniform reduced-CRT lemma: classify the rank-deficient components of
the `3 x 3` lower-coefficient map for pairwise-coprime
`R,B_1,B_2,B_3` and distinct nonzero labels, and show that every compatible
component either misses the split degree-three core-locator locus or routes to
a named existing owner. Any surviving component must remain explicitly unpaid.
