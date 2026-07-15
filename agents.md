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

## Current focus: exact-threshold RS MCA submission

The active exact-threshold integration draft is:

```text
experimental/rs_mca_thresholds.tex       coherent exact-threshold paper
experimental/rs_mca_thresholds.pdf       compiled exact-threshold paper
```

This paper is now the first place to look for self-contained exact MCA
staircases, certified prize rows, syndrome--secant geometry, quadratic/
mean-overlap thresholds, half-distance completion, and the target-aware
certificate formula.  It is more coherent than the older frontiers draft for
exact threshold work.  The broader frontiers draft remains useful for audit
comparison and for conditional profile-envelope/cell machinery:

```text
experimental/asymptotic_rs_mca_frontiers.tex       broad frontiers/audit draft
experimental/asymptotic_rs_mca.tex                 compact predecessor / audit reference
experimental/cap25_cap_v13_raw.tex                 long v13 working ledger
experimental/grande_finale.tex                     compact final-ledger note
```

The exact-threshold paper contains the current clean theorem package: exact
deep and quadratic MCA staircases, exact CA/sparse MCA decomposition, a
self-contained half-Johnson bound, certified Proth prime rows at all four
official rates, the F_17^32 exact 6/7 gate, smooth/circle transports, and a
certificate formula for turning matching safe/unsafe rows into delta*.

The remaining hard inputs are still exactly:

```text
witness-exhaustive first-match atlas;
image-scale MI + MA, or a direct Sidon payment;
residual ray compiler for higher-dimensional balanced cores;
complete profile-envelope comparison with the target;
lower reserve / unsafe-side comparison.
```

Agents should treat those five items as the current proof checklist.  Work that
does not reduce, audit, formalize, or falsify one of them is secondary.

The expected submission strategy is:

1. keep the exact finite-row and deep-frontier theorems self-contained;
2. make every conditional compiler input visible in theorem statements;
3. prove or explicitly assume the five hard inputs above;
4. use the Sidon/Fourier split and BSG/quasicube argument only after the
   image-scale MI/MA or direct Sidon payment is available;
5. compare the complete profile envelope, not only the identity prefix term,
   against the actual target and lower reserve.

Do not silently replace this with older Q/BC/SP shorthand.  If Q/BC/SP language
is useful, translate it into the current frontiers-paper vocabulary: image-scale
MI/MA or Sidon payment, balanced-core residual ray compiler, and complete
profile-envelope comparison.

## Highest priority now

1. **Lean formalization.**  Formalize the exact-threshold paper first, then
   the broader frontiers dependencies under `experimental/lean/`.  Highest
   priority tracks are:

   ```text
   experimental/rs_mca_thresholds.tex
   experimental/asymptotic_rs_mca_frontiers.tex
   experimental/lean/rs_mca_thresholds/
   experimental/lean/grande_finale/
   experimental/lean/cap25_cap_v13_raw_compact/
   ```

   Add a new package or module for the thresholds/frontiers papers only if
   it is integrated coherently under `experimental/lean/`.  The formalization
   should prioritize the MCA staircase definition, endpoint conversion, exact
   CA/sparse decomposition, tangent floor, quadratic mean-overlap theorem,
   syndrome-line incidence, first-match disjointization, profile-envelope
   definitions, primitive Boolean slice, moment-to-max equivalence, Sidon split,
   BSG/quasicube step, and target-aware threshold bracket.

2. **Adversarial proof audit.**  Use independent LLM agents or human reviewers
   to attack the proof.  Assign them specific failure modes:

   ```text
   missing witness in the first-match atlas
   incorrect image-scale normalization for MI/MA or Sidon payment
   unsupported major-arc aggregate
   residual higher-dimensional balanced core without ray compiler
   incomplete profile-envelope comparison with the target
   unsafe-side lower reserve not actually crossing the target
   incorrect first-match disjointization
   wrong field denominator or base/extension-field ledger
   misuse of BSG or quasicube growth
   mismatch between asymptotic proof and finite deployed rows
   ```

   Every attack should end as either `NO ISSUE`, `FIXED`, `OPEN GAP`, or
   `COUNTEREXAMPLE_NEW_FLOOR`, with exact file/label references.

3. **Final computations and examples.**  Produce small and medium examples that
   instantiate the proof objects: bad-line moduli strata, structured cases,
   primitive Boolean prefix fibers, Fourier/Sidon cuts, and the entropy
   threshold.  These examples are for auditing and exposition, not for replacing
   the proof.

4. **Clean write-up.**  Polish `experimental/rs_mca_thresholds.tex` as the coherent exact-threshold paper, while keeping `experimental/asymptotic_rs_mca_frontiers.tex` as the broader audit/frontiers reference.  The write-up should avoid internal
   shorthand where possible, explain Reed--Solomon/MCA for external readers,
   cite paid structured cases by theorem labels, and separate proved statements
   from the five remaining hard inputs.

Finite adjacent rows remain important, but they are now a separate constants
and certificate project, not the main asymptotic proof bottleneck.

## Three resolution tracks

The project now has three different targets.  Keep them separate.

1. **Finite deployed one-step resolution.**  For each deployed row, prove an
   adjacent staircase certificate

   ```text
   U(a0 + 1) <= B* < L(a0),
   ```

   where `L` is the exact lower/unsafe staircase, `U` is the complete
   upper/safe ledger, and `B* = floor(epsilon* Q_row)` is the row's integer
   budget, with `Q_row` equal to the relevant sampling denominator (`q_line`
   for MCA rows and the list denominator for list rows).  This proves the
   first safe agreement is `a0 + 1`.  The current four v13 rows are the main
   targets, but more exact adjacent examples are useful when they stress-test
   the same Q/BC ledger and expose the constants.

2. **Asymptotic frontier resolution.**  Formalize and audit the frontiers paper

   ```text
   delta*_C(epsilon*) = 1 - rho - g*(rho, log2 |B|) + o(1)
   ```

   where the stated hypotheses permit that identity-dominant specialization.
   The active exact-threshold manuscript is `experimental/rs_mca_thresholds.tex`; the broader audit manuscript is `experimental/asymptotic_rs_mca_frontiers.tex`.
   The main work is proving, auditing, or clearly isolating the five hard inputs
   listed above.

3. **Protocol resolution.**  Feed the finite/asymptotic theorem into the Paper C
   ledger.  Generated field, line field, challenge field, list denominator,
   interleaving arity, MCA/CA/list/line-decoding object, and endpoint convention
   must all be printed separately.

## Finite adjacent certificate

A finite deployed threshold proof is an adjacent staircase certificate:

```text
B* = floor(epsilon* Q_row)
L(a0)      > B*
U(a0 + 1) <= B*
```

Here `L` is the exact unsafe lower staircase and `U` is the complete
first-match upper ledger.  `Q_row` is the row's audited denominator, not the
row-sharp Q problem.  Once this is proved, the first safe integer agreement is
`a0 + 1`; the closed-ball endpoint convention must be printed.

The upper ledger should be short and explicit:

```text
U(a) =
  paid_tangent(a)
+ paid_quotient(a)
+ paid_extension(a)
+ paid_Q_prefix_boundary(a)
+ paid_BC_split_pencil(a)
+ explicitly named residuals.
```

Do not hide a residual branch inside a point estimate.  Mark every residual as
`PAID_BY_THEOREM`, `PAID_BY_EXACT_CERTIFICATE`,
`CONDITIONAL_ON_NAMED_INPUT`, `CONJECTURAL_WITH_FALSIFIER`, or
`COUNTEREXAMPLE_NEW_FLOOR`.

The asymptotic theorem is:

```text
delta*_C(epsilon*) = 1 - rho - g*(rho, log2 |B|) + o(1).
```

The exact-threshold paper in `experimental/rs_mca_thresholds.tex` is the
current clean source for finite thresholds and certificate formulas; the broader
frontiers paper in `experimental/asymptotic_rs_mca_frontiers.tex` remains the
source for conditional profile-envelope limitations.  Finite deployed rows
require exact constants and remain a separate certificate project.

## What counts as progress now

Highest-value contributions are:

1. Lean formalization of `experimental/rs_mca_thresholds.tex`, then
   `experimental/asymptotic_rs_mca_frontiers.tex` and imported v13 raw / Grande Finale dependencies;
2. adversarial proof audits focused on the five remaining hard inputs:
   witness-exhaustive atlas, image-scale MI/MA or Sidon payment, residual ray
   compiler, profile-envelope target comparison, and lower reserve;
3. proofs, counterexamples, or exact certificate packets for any one of those
   five inputs;
4. final computations and examples illustrating bad-line moduli strata,
   primitive Boolean prefix fibers, image-scale Fourier/Sidon cuts, and target
   reserves;
5. finite adjacent certificates for the deployed rows, with exact constants and
   replayable packets;
6. only after the threshold theorem is stable, a Paper C protocol ledger
   consuming it without merging `q_gen`, `q_line`, `q_chal`, and `q_list`.

Every packet that changes `experimental/` must add a concise entry to
`experimental/agents-log.md`.  A negative result is progress if it identifies a
new obstruction floor and updates the certificate logic.

## Paper authority and promotion rule

`tex/cs25_cap_v12.tex` is the current complete Paper D authority.
`tex/towards-prize.tex` is the compact prize-facing v12 note.
`experimental/asymptotic_rs_mca.tex` is the active compact asymptotic proof.
`experimental/cap25_cap_v13_raw.tex` and `experimental/grande_finale.tex` are
the detailed source ledgers imported by that proof.

Promotion from v13/grande-finale into Paper D requires:

1. exact unsafe certificates and exact safe upper ledgers;
2. a replayable certificate packet or printed integer proof for every finite
   row inequality;
3. a clean audit of endpoint conventions, denominators, and field ledgers;
4. an explicit status split between theorem rows and conditional rows.

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
5. Read `experimental/asymptotic_rs_mca.tex` as the active compact asymptotic
   proof.
6. For its imported structured cases, read `experimental/cap25_cap_v13_raw.tex`
   and `experimental/grande_finale.tex`.
7. Read the certificate ledgers and open problems of `snarks_v5.tex` only when
   working on protocol consumption.
8. Return to Paper B for the exact theorem labels relevant to your task.

### Fast orientation

The current research picture is:

```text
Paper A gives explicit no-slack lower bounds.
Paper B builds the corrected reserve theory and states the main missing local limits.
Paper D v12 gives the current two-sided cap, safe-side pincer, map/rational
smooth extensions, and finite certificate grammar.
experimental/asymptotic_rs_mca.tex gives the active compact asymptotic proof:
structured bad lines are imported from v13 raw / Grande Finale, and the
primitive residual is ruled out by the Sidon/Fourier split plus BSG/quasicube
growth.
Paper C says how a protocol must consume the theory without mixing ledgers.
```

The main remaining work is verification and presentation: formalize the compact
proof, adversarially audit every imported structured case, produce final
examples, and write the clean paper version.

## Current work targets

### L0. Lean formalization of the asymptotic proof

**Goal.** Formalize `experimental/asymptotic_rs_mca.tex` and its imported
dependencies under `experimental/lean/`.

Start with theorem statements for the whole proof, then prove the elementary
pieces first: first-match disjointization, moment-to-max equivalence, the
Sidon split, the Q-to-SP inequality, and the entropy-frontier calculation.
External additive-combinatorics inputs such as BSG and quasicube growth may be
axiomatized initially with exact statements and later linked to Mathlib or a
dedicated formalization.

### A0. Adversarial proof audit

**Goal.** Try to break `experimental/asymptotic_rs_mca.tex`.

Useful adversarial checks:

- Is every bad-line mechanism really covered by the cited structured cases?
- Is the Fourier/Sidon-heavy branch paid without circular use of the conclusion?
- Are major arcs routed to already-paid algebraic cases?
- Is the BSG hypothesis exactly high additive energy in the Boolean fiber?
- Does quasicube growth apply in the correct ambient abelian group?
- Are base field, line field, and challenge denominator kept separate?
- Does the entropy-frontier calculation match the threshold convention?

Every audit should end with `NO ISSUE`, `FIXED`, `OPEN GAP`, or
`COUNTEREXAMPLE_NEW_FLOOR`.

### W0. Clean proof write-up

**Goal.** Turn `experimental/asymptotic_rs_mca.tex` into a clean external paper.

Avoid internal shorthand.  Explain Reed--Solomon codes, MCA, bad lines, the
entropy threshold, and the additive-combinatorics step in reader-facing terms.
Replace broad citations such as "v13 raw ledger" with precise theorem labels
from `experimental/cap25_cap_v13_raw.tex` and `experimental/grande_finale.tex`.

### C0. Final computations and examples

**Goal.** Produce examples that make the proof auditable.

Useful examples include small bad-line classifications, primitive Boolean
prefix fibers, Fourier/Sidon-heavy versus high-energy splits, and numerical
entropy-threshold checks.  These examples support audit and exposition; they
do not replace the proof.

### F0. Finite adjacent deployed certificates

**Goal.** Separately from the asymptotic proof, finish exact finite adjacent
certificates for deployed rows.

Each packet must print `L(a0)`, `U(a0+1)`, `B*`, denominators, endpoint
convention, and first-match structured-case decomposition.  This is a constants
project: asymptotic `exp(o(n))` losses do not decide the few-bit finite margins.

### F1. Extension-line MCA theorem or counterexample

**Goal.** Decide whether extension-valued MCA lines create a new corrected
reserve obstruction after base-valued confinement is paid.

This is lower priority than Q for the deployed threshold, but still important
for protocol ledgers.  A good result specifies `B`, `F`, `D`, `k`, `delta`, the
line field, denominator, and whether the witness is genuinely `F`-valued.

### P1. Protocol ledger consumption

**Goal.** After a finite or asymptotic threshold theorem exists, feed it into
Paper C without merging ledgers.

Do not start from protocol claims.  Start from a row packet with exact
`q_gen`, `q_line`, `q_chal`, `q_list`, interleaving arity, object
(`MCA`, `CA`, `list`, `line-decoding`), and endpoint convention.

## Audit targets

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

## Scripts and finite packets

Agents should prefer reproducible scripts over hand calculations, but do not run
heavy computations casually.  For the current v13/grande-finale program, useful
scripts are those that support one of these objects:

```text
row-sharp Q max-fiber or moment bounds
BC chart-decomposition certificates
quotient/composite rung audits
frontier-adjacent row packets
endpoint/denominator/budget arithmetic
small exact counterexamples to proposed Q/BC routes
```

`scripts/run_frontier.py` is still a useful historical Paper B heuristic, but it
is not the current main path unless its output is being used to test a Q,
quotient, or exact adjacent-packet claim.

### Output standard

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

Small toy cases are useful only when they test a named route.  A toy-case note
should say which label it attacks or supports, for example `prob:row-sharp-q`,
`prob:saturated-bc`, a quotient rung audit, or an extension-line residual.

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

1. Write a small exact Q toy packet that tests `prob:row-sharp-q` on a row where
   the full fiber distribution can be enumerated.
2. Produce a quotient/composite rung audit for one active `a+` row, with exact
   integer margins and a short note.
3. Turn one residual BC chart into either a paid one-parameter pencil or a named
   higher-dimensional obstruction.
4. Add a theorem-statement Lean target for row-sharp Q in
   `experimental/lean/grande_finale/`, or the corresponding v13 raw node in
   `experimental/lean/cap25_cap_v13_raw_compact/`, without pretending it is
   proved.
5. Formalize one already-proved `grande_finale` local lemma that is still
   TeX-only, such as the composite-prefix `gcd(e,N)` descent.
6. Build a new exact adjacent example that prints `L(a0)`, `U(a0+1)`, `B*`,
   denominators, endpoint convention, and first-match cells.
7. Audit one Paper D v12/v13 raw finite inequality against its script or printed
   integer certificate.

### Lean formalization correspondence

All Lean material for this repository belongs under:

```text
experimental/lean/
```

Keep package names, module paths, and Lake `globs` coherent; for example a
package named `Foo` should have either a root `Foo.lean` or modules under
`Foo/`.

The two most important formalization tracks are:

```text
experimental/lean/grande_finale/              final-ledger components
experimental/lean/cap25_cap_v13_raw_compact/  v13 raw companion formalization
experimental/lean/asymptotic_rs_mca/          add this if building the compact proof
```

Treat these as co-priority.  The first track targets
`experimental/grande_finale.tex`: first-match ledger, BC reduction, SP-from-Q,
Sidon/Fourier payment, and adjacent-threshold logic.  The second track targets
the v13 raw/compact certificate ledger: identity-prefix floors, conversion
steps, structured-cell payments, finite certificates, and the theorem nodes
that may later be promoted into Paper D.  The compact proof track should target
`experimental/asymptotic_rs_mca.tex`: closed-ledger package, primitive Boolean
slice, BSG/quasicube proof, and entropy-frontier conclusion.

Already represented in `experimental/lean/grande_finale/`:

```text
budget and staircase kernels
support-wise CA/MCA predicates
moment kernels for Q
BC moving-root and saturation lemmas
SP-from-Q
selected finite arithmetic anchors
```

Still missing there:

```text
formal statement of the closed-ledger package used by asymptotic_rs_mca.tex
full theorem-by-theorem map from asymptotic_rs_mca.tex to v13 raw / grande_finale
formal primitive Boolean slice proof through BSG and quasicube growth
formal entropy-frontier calculation
finite adjacent deployed safe rows with exact constants
```

Use `experimental/lean/lean-blueprint.json` as the older formalization
blueprint for `experimental/cap25_cap_v13_raw.tex`, and compare it against the
package `experimental/lean/cap25_cap_v13_raw_compact/` when auditing v13
coverage.  The blueprint is useful orientation, not a substitute for direct
TeX/Lean statement comparison.  The current important v13 nodes are Q prefix
flatness, BC chart decomposition, finite adjacent ledgers, identity-prefix
floors, conversion/certificate steps, and full RS-MCA resolution; SP should be
read together with the theorem `SP follows from Q` in `grande_finale`.

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

The highest-priority formalization tasks are now:

1. formalize `experimental/asymptotic_rs_mca.tex` end to end, at least as
   theorem statements plus proved elementary steps;
2. in `experimental/lean/grande_finale/`, connect the imported structured
   cases to the closed-ledger package used by the compact proof;
3. in `experimental/lean/cap25_cap_v13_raw_compact/`, keep the v13 raw
   companion formalization aligned with the raw/compact TeX ledger, especially
   identity-prefix floors, structured-cell payments, and finite certificates;
4. separately, formalize finite adjacent deployed certificates only after the
   exact constants and replay packets are stable.

The supplementary v13 package `experimental/lean/cs25_cap_v13_experimental/`
can be used for threshold/list-side compiler pieces if it matches the current
raw ledger.  Paper D v12 still has a substantial Lean skeleton under
`experimental/lean/cs25_cap_v12/`, but that is now secondary unless a
maintainer explicitly asks for Paper D v12 formalization.

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

- a Lean theorem or accurately stated Lean target for
  `experimental/asymptotic_rs_mca.tex`;
- an adversarial audit that finds and fixes a real gap, or records a
  checked `NO ISSUE` result with exact references;
- a theorem-label map from `asymptotic_rs_mca.tex` to the v13 raw and Grande
  Finale structured-case results;
- a clean proof rewrite that is suitable for external readers;
- a final computation or example that illustrates and checks a key proof
  mechanism;
- an exact finite adjacent certificate with all constants and denominators
  printed;
- a counterexample that identifies a new obstruction floor;
- a protocol ledger that consumes an already-proved threshold theorem without
  merging field denominators.

A negative result is valuable. If a conjecture fails, identify the new obstruction floor and update the certificate logic accordingly.
