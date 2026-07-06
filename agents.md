# AGENTS.md — Research Guide for MCA / Proximity Prize Agents

This file is for AI agents and new contributors exploring the MCA / Proximity Prize repository.

Your job is not to summarize the papers. Your job is to help prove, refute, audit, or mechanize the missing pieces.

The four papers are:

```text
RS_disproof_v3.tex      Paper A: no-slack obstruction
slackMCA_v4.tex         Paper B: slack / quotient / entropy theory
cs25_cap_v12.tex        Paper D: two-sided cap, safe-side pincer, and certificate grammar
snarks_v5.tex           Paper C: SNARK / protocol ledger
```

Use logical order **A → B → D → C** unless you are working specifically on protocol ledgers.

## Top to-do: close the deployed threshold band

The prize-facing metric is the radius threshold `delta*_C(2^-128)`, not the
largest displayed error margin.  For the deployed KoalaBear sextic row, the
current Paper-D-v12 authority edge is

```text
delta = 15331/32768 ~= 0.467865.
```

The active experimental v13 raw source is:

```text
experimental/cap25_cap_v13_raw.tex          extended raw-working master
```

It moves the KoalaBear MCA experimental unsafe edge to

```text
delta = 981105/2097152 ~= 0.467827320,
unsafe agreement a0 = 1116047,
conjectured first safe agreement = 1116048.
```

Do not mix these statuses: v12 is the current paper authority; v13 raw
is the current experimental final-resolution spine.  In paper-authority mode,
close the band below the v12 edge; in v13 experimental mode, close the adjacent
band below the raw-v13 candidate edge by adjacent staircase certificates:

```text
B* = floor(2^-128 q_line)

B_mca(a0)   > B*
B_mca(a0+1) <= B*
```

Agents should prefer work that shrinks this interval for `delta*_C(2^-128)` over
work that merely increases the already-supercritical error at a larger radius.

## Final road toward FULL RESOLUTION -- experimental v13 raw spine

**Status:** The unsafe side in the v13 raw source is theorem-level
inside that experimental draft.  The exact threshold remains CONJECTURAL /
CONDITIONAL until the safe upper ledgers Q, BC, and SP are proved with constants,
replayed, audited, and promoted into Paper D.

The project should now distinguish three levels of resolution.

1. **Finite deployed one-step resolution.**  For each deployed row, prove an
   adjacent staircase certificate

   ```text
   U(a0 + 1) <= B* < L(a0),
   ```

   where `L` is the exact lower/unsafe staircase, `U` is the complete
   upper/safe ledger, and `B* = floor(epsilon* Q)` is the row's challenge
   budget.  This proves the first safe agreement is `a0 + 1`.

2. **Asymptotic frontier resolution.**  Prove or refute the conjectural match

   ```text
   delta*_C(epsilon*) = 1 - rho - g*(rho, log2 |B|) + o(1)
   ```

   for smooth multiplicative and circle line-round rows.  Polynomial-loss
   quotient equidistribution may be enough here once the agreement reserve is
   larger than `O(log n)`, but it is **not** enough for the finite adjacent
   deployed step unless the constants fit inside the printed bit margins.

3. **Protocol resolution.**  Feed the finite/asymptotic theorem into the Paper C
   ledger: generated field, line field, challenge field, interleaved-list arity,
   MCA/CA/line-decoding object, and endpoint convention must all be printed
   separately.

### Current experimental v13 frontier targets

The identity-prefix floor plus the flexible-budget simple-pole conversion
supersede the old `c=16/32` optimized rows and the proposed `c=2` terminal-scale
rows, unless the identity map is intentionally excluded.  The finite conjecture
is that the first safe agreement is one step after the best proved unsafe
agreement:

| row | proved unsafe agreement `a0` | conjectured first safe agreement |
| --- | ---: | ---: |
| KoalaBear MCA | `1116047` | `1116048` |
| KoalaBear list | `1116046` | `1116047` |
| Mersenne-31 MCA | `1116023` | `1116024` |
| Mersenne-31 list | `1116022` | `1116023` |

Do not call these Paper-D theorem rows until the exact adjacent upper ledger is
printed and replayed.  The lower/unsafe inequalities are exact certificate
claims inside the experimental raw sources; the first-safe rows are conditional
on finite Q/BC/SP safe certificates.

### The complete upper ledger to build at `a0 + 1`

For each row, a safe upper certificate must be a first-match, deduplicated sum
of paid and residual cells:

```text
U(a) =
  paid_tangent(a)
+ paid_quotient(a)
+ paid_extension(a)
+ paid_plain_CA_or_sparse_layer(a)
+ paid_Q_prefix_quotient(a)
+ paid_BC_split_pencil(a)
+ paid_SP_shift_pair(a)
+ explicitly named residuals.
```

A residual branch may not be hidden inside a point estimate.  It must be one of:

```text
PAID_BY_THEOREM
PAID_BY_EXACT_CERTIFICATE
CONDITIONAL_ON_NAMED_INPUT
CONJECTURAL_WITH_FALSIFIER
COUNTEREXAMPLE_NEW_FLOOR
```

The finite one-step theorem requires actual constants.  A statement of the form
`poly(n)` or `n^C` is only finite-useful if `C` and all constants are printed and
fit inside the row's bit margin.  Otherwise it belongs to the asymptotic road,
not the deployed adjacent proof.

### Row-packet schema for final-resolution work

Every final-resolution packet must print:

```text
row:                   (F, D, k, n, rho)
denominators:          q_gen, q_line, q_chal, q_list
target:                epsilon*, B* = floor(epsilon* Q)
agreement interval:    I = [a_min, a_max] intersect Z
unsafe certificates:   L(a) > B*
safe certificates:     U(a) <= B*
paid cells:            tangent, quotient, extension, sparse/M1, L1/list
residual cells:        named aperiodic, extension, list, SPI, or protocol branch
deduplication rule:    support/image/root coalescing theorem used
endpoint convention:   closed integer ball and real supremum
replay:                script path, command, seed/hash, JSON certificate
status:                PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT / COUNTEREXAMPLE
```

If the packet adds or materially changes files under `experimental/`, it must
also add an entry to `experimental/agents-log.md` with the date, agent/model,
files changed, status, usefulness, and next step.

### Final-resolution DAG

The closure dependency should be treated as:

```text
FULL RESOLUTION
  = finite deployed adjacent theorem
  + asymptotic frontier theorem/refutation
  + protocol ledger compiler
  + exact certificate replay
  + promotion/audit into Paper D/C.
```

The finite MCA node is:

```text
B_C(a_safe - 1) > B*
B_C(a_safe)     <= B*
```

The unsafe side is supplied by the identity-prefix lower staircase and the
flexible simple-pole MCA conversion.  The safe side is the stratified upper sum
`tangent + quotient + extension + Q + BC + SP`, with first-match deduplication.
A counterexample is still useful if it identifies a new obstruction floor and
updates the cell decomposition.

### What counts as progress now

Highest-value contributions are:

1. finite Q maximum-fiber certificates at the four `a0 + 1` rows;
2. finite BC split-pencil census certificates at the four `a0 + 1` rows;
3. finite SP primitive shift-pair certificates at the four `a0 + 1` rows;
4. a complete `frontier-adjacent/*.json` packet family replayed by the
   certificate scanner;
5. asymptotic Q/BC/SP with polynomial or `e^{o(n)}` loss, which closes the
   frontier with logarithmic agreement reserve;
6. an extension-line MCA theorem or explicit corrected-reserve counterexample;
7. a Paper C protocol certificate consuming the exact row packet without
   merging field ledgers;
8. a Lean/formal replay of the staircase, row-packet, and paid-cell compilers.

A negative result is still a resolution if it identifies the new obstruction
floor and updates the certificate logic.

This final-resolution spine does not override the current Paper D v12 audit
priority: promotion of any v13 frontier packet requires the v12/towards-prize
audit gates below to be clean or explicitly waived by a maintainer.

The experimental memo `experimental/rs_mca_proximity_prize_status.md` is a
committee-facing status draft for the v12/v13 raw picture.  Use it to orient
the entropy-subfield-envelope thesis and the current unsafe certificate
frontier, but do not treat its matching-safe-side language as paper
authority until the corresponding claims are promoted into Paper D or
`towards-prize` with replayable certificates.

### Missing inputs strategy: Q, BC, SP, and legacy `(A)`

The proof-program guide
`experimental/cap25_v13_missing_inputs_strategy.md` is the current agent route
map for the missing v13 safe-side inputs.  It was originally written in the
older two-input language:

```text
(A) aperiodic band / worst-case M1 local-limit upper theorem
(Q) quotient-fiber / quotient-ledger equidistribution upper theorem
```

Read it compatibly with `experimental/cap25_cap_v13_raw.tex` and its compact
companion: Q remains the prefix/quotient flatness input, while the old broad
`(A)` umbrella is now split into BC (base-field-normalized split-pencil census)
and SP (primitive shift-pair control), plus already-paid tangent/quotient/
extension cells.

Use it as a strategy document, not as a theorem.  It makes three points agents
should preserve:

1. The asymptotic frontier can absorb explicitly bounded polynomial losses once
   the agreement reserve is larger than `O(log n)`.
2. The finite deployed adjacent step cannot absorb an unspecified `poly(n)`
   factor; constants must fit inside the printed bit margins.
3. Both inputs should be treated as split-locator flatness problems, with
   quotient/graded strata paid separately and residual aperiodic branches named
   rather than hidden in point estimates.

Near-term useful tasks from that note are:

- normalize the left edge of `prob:band` against the entropy-subfield envelope;
- prove or refute the split-top-chart collapse and Kronecker/Berlekamp-Massey
  singular-bucket lemmas;
- build the exact prefix-collision ledger for `(Q)`;
- run the rung-margin audit for the four deployed v13 adjacent rows;
- test the mode-at-null / exchange-compression extremality conjectures on small
  rows.

## Current priority: audit v13 raw before promotion

The main focus is now **auditing the experimental v13 raw package**
against Paper D v12:

```text
tex/cs25_cap_v12.tex
tex/towards-prize.tex
experimental/cap25_cap_v13_raw.tex
```

`cs25_cap_v12.tex` is the current complete Paper D candidate.  It supersedes
v10/v11 for new work unless a maintainer asks for a historical comparison.
`tex/towards-prize.tex` is the compact prize-facing theorem note.  It should be
kept aligned with v12, but it is not a replacement for the full Paper D ledger.
The v13 raw file is an experimental successor: use it to work on the
final-resolution package, but do not cite it as Paper-D authority until a
maintainer promotes it.

### Main audit task: CS25 / Paper-D cap correctness

Before adding more computations, audit the cap paper itself.  The priority is:

1. Check the direct deep-point conversion and its integer-radius condition
   against Crites--Stewart and ABF conventions.
2. Audit the optional BCIKS half-distance import in the exact normalization of
   `eca` used in v12.
3. Verify that every "verified exactly" deployed-row inequality in v12 and the
   v13 raw package has a reproducible script or a printed integer
   certificate.
4. Check the rational-scale/genus-one and circle/stereographic transports
   against the actual deployed code models.
5. Keep `towards-prize.tex` scoped correctly: it is a compact theorem note for
   the smooth multiplicative prize box, not the full ledger paper.
6. Check that any v13 promotion keeps the status split: unsafe
   exact certificates are theorem-level in the raw draft, while first-safe adjacent
   rows remain conditional on finite Q/BC/SP.
7. Report any issue as `AUDIT`, not as a theorem change, unless the proof fix is
   already written and local.

Only after this audit is stable should agents return to Hankel packets, M5
underdetermined charts, or new leaderboard computations.

## Ground rules

### 1. Do not try to prove the old unslacked theorem

The no-slack support-wise line-MCA statement for smooth multiplicative RS domains is refuted by Paper A. Any positive theorem must have a reserve:

```text
delta = 1 - rho - eta,
```

where `eta` clears the generated-field entropy floor, quotient-core floors, known MCA failure ladders, universal-cap floor, interleaved-list-over-field budget, and the actual field used by the protocol.

### 2. Never merge the field ledgers without a theorem

Keep these distinct:

```text
q_gen    generated field for entropy / locator fibers
q_line   field used in line, CA, MCA, or line-decoding experiments
q_chal   verifier challenge field
B        base/generated subfield, when F is an extension
F        ambient or extension field
```

A common error is to use a large extension field to pay for a generated-field entropy deficit. Do not do this unless a theorem explicitly transfers the object to the extension field.

### 3. Keep list, CA, MCA, line-decoding, and curve-MCA separate

These objects are related, but not interchangeable.

A protocol proof may consume:

- base-code list size,
- interleaved list size,
- CA,
- support-wise MCA,
- line-decoding,
- curve-MCA or polynomial-generator MCA.

Identify the exact object before using a theorem.

### 4. Label proof status

Every contribution should be tagged as one of:

```text
PROVED          complete proof under stated assumptions
CONDITIONAL     proof depends on an imported theorem or explicit assumption
CONJECTURAL     plausible statement without proof
EXPERIMENTAL    script or small-case evidence only
AUDIT           verification / citation / constants check
COUNTEREXAMPLE  refutation of a proposed statement
```

Do not promote conditional or experimental results to proved statements.

### 5. Leave the main papers unchanged by default

Treat Papers A-D as stable reference documents unless a maintainer explicitly asks for edits:

```text
tex/RS_disproof_v3.tex
tex/slackMCA_v4.tex
tex/cs25_cap_v12.tex
tex/snarks_v5.tex
```

New material should go into `experimental/` first, except for explicit maintainer
requests to edit the active Paper D/towards-prize drafts. Use separate files
there for proof notes, audits, theorem-label maps, formalization plans,
reproducible experiments, and certificate generators. After review, stable
`.tex` contributions can be promoted to `tex/`, and stable `.py` scripts can be
promoted to `scripts/`.

Whenever you add or materially change something under `experimental/`, add an entry to `experimental/agents-log.md` with the date, agent/model, files changed, status, usefulness, and next step.

## Start here

### Minimal reading path

1. Read the abstract and scope section of `RS_disproof_v3.tex`.
2. Read the introduction and frontier/open-problems section of `slackMCA_v4.tex`.
3. Read the abstract, direct conversion theorem, safe-side pincer, certificate
   grammar, and open problems of `cs25_cap_v12.tex`.
4. Read `tex/towards-prize.tex` as the compact prize-facing version of the v12
   theorem package.
5. For v13 work, read `experimental/cap25_cap_v13_raw.tex` as the active raw
   master ledger.
6. Read the certificate ledgers and open problems of `snarks_v5.tex`.
7. Return to Paper B for the exact theorem labels relevant to your task.

### Fast orientation

The current research picture is:

```text
Paper A gives explicit no-slack lower bounds.
Paper B builds the corrected reserve theory and states the main missing local limits.
Paper D v12 gives the current two-sided cap, safe-side pincer, map/rational
smooth extensions, and finite certificate grammar.
Experimental v13 raw moves the unsafe frontier and reduces the final
safe side to Q, BC, and SP, but it is not yet Paper-D authority.
Paper C says how a protocol must consume the theory without mixing ledgers.
```

The main mathematical unknowns are not in Paper A. They are in the positive local-limit, line/MCA, extension-transfer, and interleaved-list directions of Papers B/C/D.

## Highest-priority proof targets

### L1. Generated-field locator local limit

**Goal.** Prove polynomial codeword-image locator-fiber bounds for generated-field smooth domains above the entropy and quotient reserves.

A useful target statement is:

```text
For smooth domains H_n of size n, rate rho, and generated field q_gen = poly(n),
all arbitrary received words U have image locator fiber size |ImgFib_U(k+sigma)| <= n^B once
sigma * log2(q_gen) exceeds log2 binomial(n, k + sigma)
and active quotient-core contributions are absent or budgeted.
```

Raw support fibers `Fib_U` can be exponentially inflated by many supports
explaining the same codeword.  The exact list object is the image fiber
`ImgFib_U`; use raw `Fib_U` only as a coarse upper bound when multiplicity is
explicitly budgeted.

**Why it matters.** This is the main positive list theorem missing from Paper B. Paper C needs it to create list certificates.

**First attacks.**

- Prove monomial-prefix cases first.
- Separate quotient-periodic fibers from aperiodic fibers.
- Use characteristic-zero rigidity where possible.
- Convert finite-field collisions into algebraic-integer divisibility or norm events.
- Below norm thresholds, look for density-over-primes theorems first.
- Build small scanners that enumerate locator fibers and collision templates.

**Useful toy cases.**

```text
q = 17,      n = 16,      rho = 1/2 or 1/4
q = 257,     n = 256,     rho = 1/2 or 1/4
q = 65537,   n = 65536,   rho = 1/2 or 1/4, only with optimized scripts
n = 32,64,128 over small extension fields for collision-template scans
```

Start with tiny `n` and exact enumeration. Do not jump straight to deployed sizes.

### M1. Corrected MCA / residue-line local limit

**Goal.** Prove that, above the corrected reserve, residue-line packing is small enough to give an MCA bound in the polynomial-field window.

**Why it matters.** This is the main MCA-side positive theorem missing from Paper B. Without it, Paper C remains conjectural outside theorem-backed fallback regimes.

**First attacks.**

- Work in the residue-line normal form from Paper B.
- Classify low-slack templates first.
- Prove aperiodic packing bounds after quotient-periodic components are removed.
- Use inverse Littlewood--Offord style arguments for support-sum collisions.
- Search for small counterexamples where list fibers are small but MCA bad slopes remain large.

**Toy cases.**

```text
slack t = 1, 2, 3
quotient order N = 8, 16, 32
rates rho = 1/2, 1/4
canonical directions before arbitrary directions
zero-base or canonical-base strata before arbitrary-base strata
```

### M2. Line-decoding form of the corrected conjecture

**Goal.** Restate the corrected MCA conjecture as a line-decoding theorem with explicit parameters.

**Why it matters.** Many protocol analyses consume line-decoding more naturally than support-wise MCA. A clean line-decoding statement could make the SNARK ledger easier to use.

**First attacks.**

- Translate a support-wise MCA-bad slope into a line-decoding ambiguity.
- Identify the exact `(delta, a_LD, n+1)` parameters.
- Determine whether line-decoding is equivalent to residue-line packing or strictly stronger.
- Look for separations: small MCA but large line-decoding, or vice versa.

### F1. Extension-line MCA lift or counterexample

**Goal.** Decide whether MCA bounds over a base/generated field `B` lift cleanly to extension-valued lines over `F`, or whether genuinely `F`-valued residue denominators create new bad slopes.

**Why it matters.** Protocols often use extension challenges. Paper D shows that below the cap, `F`-valued witnesses exist and are not merely `B`-rational. A clean lift theorem or counterexample is needed.

**First attacks.**

- Do not search only among `B`-rational lines; Paper D’s confinement result makes that search incomplete.
- Parameterize residue-line denominators `E in F[X] \ B[X]`.
- Start with quadratic and cubic extensions of small fields.
- Compare extension-code/interleaving identities on the list side with MCA behavior.

**Toy cases.**

```text
B = F_p, F = F_{p^2} for p = 5, 7, 17
B = F_p, F = F_{p^3} for small p
H <= B^* of order 4, 8, 16
rho = 1/2, slack t = 1 or 2
```

A good counterexample should specify `B`, `F`, `H`, `k`, `delta`, the bad line family, and why no base-field theorem explains it.

### L2. Sharp interleaved-list constants near capacity

**Goal.** Bound

```text
|Lambda(Int(C, mu), 1 - rho - eta)|
```

for the concrete arities used in protocols, without overpaying by the trivial Cartesian-product exponent.

**Why it matters.** Protocol soundness uses interleaved list size divided by the challenge field. Overcharging the exponent can make a good parameter set look impossible.

**First attacks.**

- Replace independent base lists by simultaneous agreement-support families.
- Try to inject interleaved lists into feasible supports plus low-dimensional polynomial choices.
- Test whether quotient-core lower bounds multiply under interleaving or share the same support structure.
- Compare product bounds with GGR-style bounds near capacity.

### L3. Quotient-profile constants and dimension dithering

**Goal.** Turn the quotient profile into a finite-length scanner and theorem.

**Why it matters.** Many obstructions disappear when `k = rho*n` is changed to `k = rho*n - 1` or another low-divisibility dimension. This must be proven and checked at actual parameters.

**First attacks.**

- Prove maximal-remainder lemmas for `k = rho*n - r`, not only `r = 1`.
- Write a divisor scanner for active quotient scales.
- Compare exact-rate and dithered dimensions across all prize rates.
- Connect dithered `k` to real AIR/R1CS/Plonkish degree bounds.

**Toy cases.**

```text
n = 2^m, m = 8..20
rho in {1/2, 1/4, 1/8, 1/16}
k0 = rho*n
k = k0 - r for r = 1..16
quotient orders N = 2^c dividing n
```

Record which quotient scales remain active.

### X1. List--CA--MCA equivalence without square-root loss

**Goal.** Determine when a corrected-reserve list bound implies a corrected-reserve CA/MCA/line-decoding bound at essentially the same radius.

**Why it matters.** Paper D v12 uses a self-contained deep-point conversion and
safe-side pincer to cap and sandwich the MCA challenge; older list-to-agreement
routes remain relevant for CA/list comparison audits. A forward positive
equivalence would be powerful, but may be false.

**First attacks.**

- Translate many MCA-bad slopes into locator fibers.
- Use line-decoding as a middle object.
- Track all field-size factors; a true asymptotic implication may still be too weak for `2^-128`.
- Search for examples with small lists but large MCA error.

### X3. Domain shattering and alternatives to smooth subgroups

**Goal.** Characterize domains by quotient degeneracy and find FFT-friendly domain modifications that destroy quotient-core obstructions.

**Why it matters.** If smooth subgroups cannot support the desired reserve, protocols may need folded/subspace-design codes, random/punctured domains, circle domains, or partially shattered smooth domains.

**First attacks.**

- Treat `Qprof` as a degeneracy measure.
- Study random puncturing of smooth subgroups.
- Study unions of cosets and mixed-radix domains.
- Test whether quotient locator identities survive partial shattering.
- Preserve FFT structure as much as possible.

## Highest-priority audit targets

### A0. Audit Paper D v12 and older imported CA/list conversions

Paper D v12 is now the main Paper D package. Its direct conversion route is
self-contained, while its half-distance safe edge uses an isolated BCIKS import
and older CS25/ABF list-to-agreement routes remain relevant for CA and
list-comparison statements. Audit:

- exact admissible radius range,
- exact definition of the augmented code,
- normalization of CA error,
- sampling field for the agreement parameter,
- constants in the `eta = 1/2` specialization,
- monotonicity/list-subcode steps used in the contrapositive.

Output should be a short note or PR that says either:

```text
The import matches exactly.
```

or

```text
The import needs the following hypothesis/constant correction: ...
```

### A1. Reproduce Paper A finite claims

Build a verification table for:

- quotient locator identity,
- DSH/restricted-sum coverage,
- deployed field divisors,
- Fermat-prime examples,
- extension-tower density variants,
- exact small-field computations.

Every finite claim should be backed by either a symbolic inequality or a script certificate.

### A2. Theorem-number and cross-citation audit

Whenever a paper says “the companion proves,” replace it with a theorem/proposition/corollary number.

Maintain a mapping like:

```text
Paper B thm:qcore          quotient-core list obstruction
Paper B prop:qfloor        quotient-exact MCA floor
Paper B thm:qnecessity     necessity of quotient profile for MCA
Paper B prop:prize         prime-field challenge cap below ~150--162 bits
Paper D thm:main           universal field-size cap
Paper C thm:ledger         reserve-certificate ledger
```

Update this map if theorem numbers or labels change.

## Suggested scripts

Agents should prefer reproducible scripts over hand calculations.

Planned scripts:

```text
scripts/run_frontier.py
scripts/entropy_margin.py
scripts/quotient_profile.py
scripts/restricted_sum_dp.py
scripts/locator_fiber_scan.py
scripts/mca_slope_scan.py
scripts/extension_line_scan.py
scripts/interleaved_budget.py
scripts/certificate_emit.py
```

`scripts/run_frontier.py` is an EXPERIMENTAL Paper B heuristic: it fixes `N = 32` and `l = 18`, expects primes with `32 | p-1`, splits the multiplicative subgroup, and uses meet-in-the-middle enumeration to test coverage of the `psi_2` elementary-symmetric map `(e1, e2)`. Similar frontier heuristics are useful when they isolate one exact quotient, locator, residue-line, or interleaved-list object, make all parameters explicit, and record coverage or counterexample witnesses before anyone tries to promote the pattern to a theorem.

### Script output standard

A script should output:

```text
1. input parameters
2. exact mathematical object being checked
3. result
4. proof certificate or reproducibility seed
5. theorem/problem ID it supports
6. whether the output is PROVED, EXPERIMENTAL, or COUNTEREXAMPLE
```

JSON plus a human-readable table is preferred.

## Toy-case menu

### Restricted sums and quotient locators

Start with:

```text
H = cyclic subgroup of order n
Q = quotient of order N
N in {4, 8, 16, 32}
rho in {1/2, 1/4}
slack t in {1, 2, 3}
```

Compute restricted sums in `Q`, coverage of the field/subgroup, and the corresponding bad-slope counts.

### Quotient-profile dithering

For each `n = 2^m`, compare:

```text
k = rho*n
k = rho*n - 1
k = rho*n - 2
...
k = rho*n - 16
```

Record active quotient orders `N`, contribution size, and whether the dither is compatible with a plausible proof-system degree bound.

### Locator fibers

For small fields, enumerate feasible agreement supports and locator polynomials.

Start with monomial-prefix received words, then random received words, then adversarially chosen received words.

Look for:

- quotient-periodic families,
- aperiodic collision templates,
- unexpectedly large fibers after quotient removal,
- field-size thresholds where characteristic-zero behavior transfers.

### MCA bad slopes

For small `q,n,k`, enumerate pairs `(f,g)` and slopes `z` where `f + z g` is close to the code but no common support explains `f` and `g`.

Record whether the witness is:

```text
canonical direction
zero-base direction
quotient-periodic
residue-line normal form
extension-valued only
```

### Extension-line witnesses

Use tiny extensions first:

```text
F_{p^2}, F_{p^3}, F_{p^4}
```

Search for bad lines with denominator polynomial `E` not defined over the base field. Compare against base-field confinement statements.

### Circle / Chebyshev analogues

For small analogues of circle-group or isogeny-smooth domains, replace multiplicative locators `X^a - b` by Chebyshev-style locators. Test whether the universal-cap fiber construction still has an analogue.

## What not to do

Do **not**:

- claim smooth RS is safe up to capacity without a reserve;
- use `q_line` to pay a `q_gen` entropy bill;
- use extension challenges to shrink list/MCA error unless the code object also lives over the extension;
- ignore quotient profiles at exact dyadic rates;
- assume `k = rho*n - 1` is free in a real arithmetization;
- replace interleaved-list size by base-list size without a bridge theorem;
- replace MCA by CA or line-decoding without stating the conversion;
- cite Paper D’s cap as error-one in the forbidden band;
- present a small-case experiment as a theorem.
- edit the main Papers A-D directly unless a maintainer explicitly asks for that change; put new material in `experimental/` first.

## Contribution template

When proposing a new result, use this structure:

```markdown
## Claim
State the theorem/conjecture/counterexample precisely.

## Status
PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT / COUNTEREXAMPLE

## Parameters
q, q_gen, q_line, field tower, n, k, rho, delta, eta, interleaving/list arity.

## Existing paper dependency
Which paper theorem/lemma/problem does this use or modify?

## Proof idea or experiment
Give the proof skeleton or script description.

## Ledger impact
Which ledgers improve or worsen: entropy, quotient, interleaved list, MCA, line-decoding, field transfer, query budget?

## Constants
Give explicit constants, not only asymptotics.

## Reproducibility
Attach script, seed, exact command, or symbolic certificate.
```

## Good first PRs

1. Implement `quotient_profile.py` for dyadic `n` and dithered `k`.
2. Implement `entropy_margin.py` and reproduce the reserve inequalities used in the papers.
3. Write a theorem-label map across the four papers.
4. Audit older Crites--Stewart/ABF imports used by CA/list comparison routes.
5. Exhaust `q=17`, `n=16`, `rho=1/2,1/4` for locator fibers and MCA bad slopes.
6. Compare base-list product bounds with direct interleaved-list enumeration for tiny `mu=2` cases.
7. Search for the first genuinely extension-valued bad line over `F_{p^2}`.
8. Produce a JSON schema for Paper C reserve certificates.
9. Extend the Lean formalization packages under `experimental/lean/`.

### Lean formalization correspondence

Use `experimental/lean/lean-blueprint.json` as the current formalization
blueprint for `experimental/cap25_cap_v13_raw.tex`.  It is a dependency graph:
each node records the TeX label, statement kind, module bucket, `depends_on`,
reverse `implies`, and a `formalization` slot.  The important final targets are:

```text
target:Q_prefix_flatness
target:BC_base_field_split_pencil
target:SP_primitive_shift_pair_control
target:finite_adjacent_deployed_ledgers
target:RS_MCA_full_resolution
```

Do not fill a `lean_file` / `lean_name` slot by guesswork.  Fill or update it
only when an actual Lean declaration exists under `experimental/lean/` and the
statement has been matched to the blueprint node.

Maintain TeX/Lean correspondence manually.  Bulk source-scanning tools are not
part of the workflow because they can attach generic helper declarations to the
wrong theorem labels or overwrite curated notes.  When a Lean declaration is
added, compare its statement directly against the TeX node before recording it.

Interpret existing correspondence fields carefully:

```text
mapping_confidence  exact_label_match / curated_alias / name_heuristic / mixed
audit_status        whether the match still needs statement audit or proof work
related_lean        all Lean declarations supporting a split blueprint node
statement_status    source-scan status; not a Lake build result
```

`lean-inventory.json` and `lean-blueprint-report.md` are static orientation
snapshots, not authorities.  Prefer package-local README files, correspondence
notes, and direct theorem-statement audits when deciding what has really been
formalized.

If you complete a Lean theorem, update the relevant package README or
correspondence note by hand, add an entry to `experimental/agents-log.md`, and
record any blueprint change explicitly.  Only call a result Lean-certified after
the relevant Lake package has actually been built and the theorem statement has
been compared against the TeX node.

The highest-priority formalization task is now to make
`experimental/lean/cs25_cap_v12/` a complete Lean formalization of Paper D
v12.  The package already has a substantial proved core and a named skeleton
queue; the next agent should attack the `Fiber.lean` skeleton first, because it
supplies the fiber-list input consumed by the universal-cap reduction.  After
that, close the regular Hankel, quotient-remainder, interleaving witness,
circle-code, and ECFFT/rational-map skeletons.  This is a good task for
Claude Code Opus 4.8 or Claude Fable 5 style agents: keep changes modular,
remove one `sorry` at a time, and update the package README/agents log after
each completed theorem.

For the compact prize-facing theorem note, use the separate Mathlib package
`experimental/lean/towards_prize/`.  Its entry point is `TowardsPrize.lean` and
it targets `tex/towards-prize.tex`: MCA/CA definitions, sparse layer,
half-distance/deep-regime statements, identity-prefix floor, and deep-point
conversion.  Before citing any towards-prize result as Lean-certified, run the
package in a Mathlib-enabled Lean 4.28 environment and add a theorem-by-theorem
map; the deployed binomial-entropy cap rows remain outside this package unless
explicitly formalized.

## Success criteria

The project advances if an agent produces any of the following:

- a new theorem clearing one reserve ledger,
- a counterexample showing a proposed positive theorem is false,
- a sharper explicit constant for a known bound,
- a verified script certificate replacing a hand calculation,
- a protocol reduction rewritten in exact ledger form,
- a toy-case database that reveals a new obstruction template,
- an audit that upgrades or corrects a conditional import.

A negative result is valuable. If a conjecture fails, identify the new obstruction floor and update the certificate logic accordingly.
