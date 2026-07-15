# Fresh independent review: 32221 reduced-CRT rank dichotomy

**Review mode:** read-only, fresh-context Codex reviewers distinct from the
generating agent. The reviewers made no repository edits.

## Statement audited

The local implication chain for

\[
(\ell,d,r,t,(a_i))=(4,3,2,3,(2,2,1)),\qquad (G_2,G_R)=(4,4):
\]

the existing-owner partition, the `12 x 9` fixed system, the `12 x 12`
moving system, the reduced `3 x 3` CRT compatibility map, the compatible
rank-drop common-factor implication, the pointwise migration to `d<=2`, and
the proposed replacement `155,952 -> 432`.

## Files and sections read

- `experimental/notes/l1/l1_b9_frontier_32221_reduced_crt_lemma.md`
- `experimental/scripts/verify_l1_b9_frontier_32221_owner_partition.py`
- `experimental/scripts/analyze_l1_b9_frontier_32221.sage`
- `experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_cas.py`
- all three linked JSON certificates
- the imported scanner helpers and banked 31222 ledger certificate
- the relevant prior 31222 audit history

The final review used the revised standalone hypotheses: `deg P<5`, the
received word `U` is zero on the core/background and equals `c_iL_C` on
labelled petal `i`, `B_i=L_{S_i}`, and `P=W=RHV`.

## Dependencies

- **PROVEN internally:** CRT existence; fixed rank nine; moving/reduced rank
  identities; degree-gap and Euclid-lemma common-factor implication;
  pointwise profile migration; canonical-key disjointness.
- **EXACT FINITE:** all 432 `GF(19)` keys, all 1,728 restored-core
  refinements, all four actual missed-core locators per key, and the
  independent full decoder.
- **IMPORTED/REPLAYED:** the banked all-profile and unresolved totals
  `1,348,447` and `513,283`.
- **NOT IMPORTED:** TheoremSearch returned only rational-interpolation and
  syzygy analogues. No external result is load-bearing.

## Proof checks

### Exhaustivity

Exact `d=3,r=2` supplies three distinct zeroes of `P`, hence

\[
P=RHV,\qquad \deg V\le1.
\]

The printed petal-data hypotheses justify cancellation of `H`; every exact
target satisfies `B_i | (RV-c_iF)`.

### Fixed rank

In the homogeneous fixed system, every `B_i` divides `RV`. Thus
`B=B_1B_2B_3` divides `RV`; disjointness gives `gcd(B,R)=1`, so `B|V`.
Because `deg B=5>deg V`, `V=0`, then every `A_i=0`. The `12 x 9` matrix has
rank nine.

### Reduced compatibility and rank

The cokernel obstructions are exactly the `X^2,X^3,X^4` coefficients of
`FG mod B`. Therefore

\[
\operatorname{rank}C=9+\operatorname{rank}M,
\qquad
\operatorname{rank}[C|b]=9+\operatorname{rank}[M|-u].
\]

### Compatible rank drop

A nonzero homogeneous direction has `F_0!=0`, `deg F_0<=2`, and
`deg V_0<=1`. Cross multiplication gives

\[
B\mid VF_0-V_0F.
\]

The right side has degree at most four, below `deg B=5`, and hence vanishes.
If `gcd(F,V)=1`, Euclid's lemma forces `F|F_0`, contradicting the degrees.
The `V=0` edge case is separately impossible.

### Pointwise migration

For split squarefree `F=L_D`, the common factor supplies `alpha in D`. Since
`R(alpha)H(alpha)!=0`, the core agreement condition is exactly `V(alpha)=0`.
Thus the missed core is `D\setminus Z(V)` and has size at most two. Compatible
rank drop is empty in exact `d=3`.

### Canonical disjointness

An exact word uniquely determines both background agreements, each labelled
petal agreement set, and its restored core point. There are

\[
3\binom42^2\binom41=432
\]

cofactor keys. The full-rank bound is on all monic cubics for a key, so all
four restored-core choices are already included and there is no extra factor
four.

## Replays and mutations

- Owner replay: PASS; 432 unpaid aggregate keys, 1,728 refinements, twelve
  periodic refinements.
- Owner mutations: PASS; duplicate assignment, owner order, owner assignment,
  charge, and prior-ledger link all caught.
- Sage replay: PASS; moving ranks
  `408*(12,12), 23*(11,12), 1*(11,11)` and matching reduced ranks.
- Sage mutations: PASS; five of five caught.
- Independent Python/Singular/Macaulay2 replay: PASS.
- CAS mutations: PASS; eight of eight caught.
- `git diff --check`: PASS in the fresh proof review.

## Independent falsification supplement

A third fresh read-only agent exhaustively scanned the minimal full-profile
`GF(11)` case after the proved normalizations `R={0,1}` and `c_1=1`. It checked
11,340 ordered disjoint support/core partitions and 816,480 normalized
distinct-nonzero label charts. The reduced-rank histogram was

```text
(rank M,rank[M|u])=(3,3): 738,864
                       (2,3):  66,096
                       (2,2):  10,332
                       (1,2):   1,188
```

The 10,332 compatible rank-drop charts contained 113,652 monic cubic
solutions, with zero `gcd(F,V)=1` counterexamples. Of these, 3,024 used an
actual three-of-four split core locator; all migrated out of exact `d=3`.
This is falsification evidence only; the uniform conclusion rests on the
polynomial proof.

The same falsifier also exhaustively checked all monic polynomial locator
configurations satisfying the stated coprimality hypotheses over `GF(4)` and
`GF(5)`, including split, irreducible, and repeated locators. It checked 1,152
monic solutions on 288 compatible rank-drop charts over `GF(4)` and 24,600
solutions on 4,920 compatible charts over `GF(5)`, again with zero
`gcd(F,V)=1` counterexamples.

## Parameter dependence

The algebraic lemma is field-uniform under its explicit locator, label, and
profile hypotheses. The 432-key count and ledger arithmetic are specific to
the frozen sequential `GF(19)` row.

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.

## Edge cases and notation

Ranks zero through two, affine inconsistency, and `V=0` are covered.
Nonsplit/repeated `F`, overlapping blocks, zero labels, or nonzero
core/background data are outside the profile corollary. The same letter `C`
is used for the core and moving matrix in prose, but context resolves it; this
is editorial only.

## Numerical evidence

The `GF(19)` census and `GF(11)` falsifier are exact finite evidence, not
asymptotic evidence. Neither is used in place of the degree-gap proof.

## Verdict

**GREEN - the local proof obligation is satisfied under the revised printed
hypotheses.**

## Ledger authorization

**YES.** The mathematical replacement

\[
155{,}952=432\cdot19^2\longrightarrow432
\]

is authorized, saving `155,520`. The resulting totals should be
`1,192,927` and `357,763`, subject only to a dedicated mutation-tested ledger
replay before the word *banked* is used.

## Remaining risks

This is one local row. It does not close the remaining unresolved mass or
prove a global mixed-petal theorem. No `m>2`, PR `#763`, or Lean consequence
has been reviewed.

## Minimal next action

Run a dedicated 32221 ledger verifier that reconstructs the complete banked
profile list, applies exactly this one 432-key replacement, checks the new
largest row, and rejects charge, duplicate-assignment, total, and linkage
mutations.
