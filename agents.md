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

## Current focus: v13 raw plus grande finale

The prize-facing quantity is the threshold `delta*_C(2^-128)`, not the largest
displayed error at an already unsafe radius.  The current Paper-D-v12 authority
edge for the deployed KoalaBear sextic row remains:

```text
delta <= 15331/32768 ~= 0.467865.
```

The active experimental final-resolution sources are:

```text
experimental/cap25_cap_v13_raw.tex          long v13 working ledger
experimental/grande_finale.tex              compact Q-focused target note
experimental/cap25_v13_missing_inputs_strategy.md
```

The v13 raw/grande-finale package moves the experimental unsafe frontier and
asks for one adjacent safe certificate:

| row | proved unsafe agreement `a0` | candidate first safe agreement `a+` | remaining finite margin |
| --- | ---: | ---: | ---: |
| KoalaBear MCA | `1116047` | `1116048` | `22.1969` bits |
| KoalaBear list | `1116046` | `1116047` | `22.0109` bits |
| Mersenne-31 MCA | `1116023` | `1116024` | `3.2589` bits |
| Mersenne-31 list | `1116022` | `1116023` | `3.0730` bits |

The unsafe inequalities are exact certificate claims inside the experimental
sources.  The adjacent safe rows are **not proved**.  Do not cite the v13 rows
as Paper-D theorem rows until the upper ledger is printed, replayed, audited,
and explicitly promoted by a maintainer.

## Main bottleneck: row-sharp Q

The latest `experimental/grande_finale.tex` reduces the old Q/BC/SP proof block:

```text
SP follows from a max-fiber Q theorem.
Primitive one-parameter BC pencils are paid by the moving-root theorem.
The remaining finite safe-side obstruction is row-sharp Q, plus a finite
BC chart-decomposition audit showing that residual BC charts reduce to the
paid one-parameter pencil form.
```

Here Q means the following finite max-fiber problem.  At an adjacent agreement
`a+`, put `K = k+1` on the MCA route and `K = k` on the list route, and set
`w = a+ - K`.  Consider the prefix map sending an agreement support to the first
`w` locator coefficients, after quotient, tangent, planted, extension, and other
paid cells have been removed by first match.  The row-sharp Q atom bound asks:

```text
max_z |P_Q(z)| <= row budget
```

where `P_Q(z)` is the remaining primitive prefix-boundary family over prefix
value `z`.  In normalized form this is an average-fiber bound with only the
printed row margin available.  A generic `poly(n)` or `n^C` statement is not
finite-useful unless every constant is explicit and fits inside the margin.

Start in `experimental/grande_finale.tex` at:

```text
def:q-row-atom
prop:q-exact-target
prop:q-moment-order-floor
prop:bc-not-q
prop:q-not-closed
prob:row-sharp-q
prob:saturated-bc
```

Use `experimental/cap25_cap_v13_raw.tex` for the full ledger and
`experimental/cap25_v13_missing_inputs_strategy.md` for possible proof routes.

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

2. **Asymptotic frontier resolution.**  Prove or refute the conjectural match

   ```text
   delta*_C(epsilon*) = 1 - rho - g*(rho, log2 |B|) + o(1)
   ```

   for smooth multiplicative and circle line-round rows.  This is where a
   polynomial or `e^{o(n)}` Q theorem may be enough, once the agreement reserve
   is larger than `O(log n)`.  It does not automatically solve the finite
   deployed rows, because their bit margins are small.

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

The asymptotic target is still:

```text
delta*_C(epsilon*) = 1 - rho - g*(rho, log2 |B|) + o(1).
```

Polynomial-loss Q/BC statements may be enough for this asymptotic target once
the agreement reserve is larger than `O(log n)`.  They are not enough for the
finite adjacent deployed rows unless constants fit the row budgets.

## What counts as progress now

Highest-value contributions are:

1. a row-sharp Q theorem or exact Q certificate at the four `a+` rows;
2. a finite BC chart-decomposition audit reducing all residual BC charts to the
   paid one-parameter moving-root form, or isolating a new residual obstruction;
3. an exact quotient/rung audit at the four `a+` rows;
4. a replayable `frontier-adjacent/*.json` packet family with row, denominator,
   endpoint, budget, unsafe lower certificate, safe upper certificate, and
   first-match cell decomposition;
5. Lean formalization of the row-sharp Q statement, the BC chart audit, and the
   adjacent staircase compiler under `experimental/lean/`;
6. only after the threshold packet exists, a Paper C protocol ledger consuming
   it without merging `q_gen`, `q_line`, `q_chal`, and `q_list`.

Every packet that changes `experimental/` must add a concise entry to
`experimental/agents-log.md`.  A negative result is progress if it identifies a
new obstruction floor and updates the certificate logic.

## Paper authority and promotion rule

`tex/cs25_cap_v12.tex` is the current complete Paper D authority.
`tex/towards-prize.tex` is the compact prize-facing v12 note.
`experimental/cap25_cap_v13_raw.tex` and `experimental/grande_finale.tex` are
the active experimental final-resolution sources.

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
safe side to row-sharp Q plus a finite BC chart audit; SP is downstream from Q.
It is not yet Paper-D authority.
Paper C says how a protocol must consume the theory without mixing ledgers.
```

The main mathematical unknown is now precise: prove row-sharp Q, or find the
new obstruction floor that replaces it.

## Current proof targets

### Q1. Row-sharp Q for deployed adjacent rows

**Goal.** Prove the max-fiber bound in `prob:row-sharp-q` of
`experimental/grande_finale.tex` for the four active adjacent rows.

This is the bottleneck.  The proof must control the first-match residual
prefix-boundary family `P_Q(z)` after quotient, tangent, planted, extension,
and other paid cells are removed.  The finite target is not just
`average * poly(n)`; it must fit the exact row margins printed in
`prop:q-exact-target`.

Useful first attacks:

- Prove a row-sharp primitive prefix-fiber theorem for the Mersenne-31 list row,
  the tightest margin.
- Strengthen moment methods beyond the obstruction in
  `prop:q-moment-order-floor`, or explain why a different method is required.
- Test exchange-compression or mode-at-null claims only as falsifiable routes;
  do not promote them without exact finite constants.
- Keep quotient/composite directions separate using the `gcd(e,N)` descent
  repair in `grande_finale`.

### Q2. Asymptotic Q and the entropy-subfield envelope

**Goal.** Prove or refute the asymptotic Q input needed for

```text
delta*_C(epsilon*) = 1 - rho - g*(rho, log2 |B|) + o(1).
```

For this target, explicit polynomial or `e^{o(n)}` losses may be acceptable
once the agreement reserve is larger than `O(log n)`.  The result should still
state the base field `B`, the line/challenge denominator, quotient exclusions,
and whether it applies to multiplicative domains, circle domains, or both.

### B1. Finite BC chart-decomposition audit

**Goal.** Show that every residual balanced-core split-pencil chart at the
active adjacent rows either is already paid or reduces to a primitive
one-parameter pencil covered by the moving-root theorem.

This is no longer a raw-support counting problem.  `grande_finale` proves that
raw support BC can overcount the MCA numerator, and it pays primitive
one-parameter pencils.  The remaining task is structural: verify the chart
decomposition and name any genuine higher-dimensional residual.

### R1. Exact rung and quotient audits

**Goal.** Audit every quotient/composite rung at the four `a+` rows.

If a rung exceeds budget, the adjacent candidate fails for a paid reason and
the frontier moves.  If all rungs are below budget with printed margins, the
remaining problem is genuinely primitive Q plus the BC chart audit.  Keep this
as exact integer arithmetic, not floating evidence.

### E1. Additional finite adjacent examples

**Goal.** Produce more exact adjacent staircase examples, preferably near the
same entropy-subfield envelope.

Useful examples are those that clarify whether Q is the true final obstruction:
new base fields, circle rows, controlled quotient scales, or smaller rows where
the complete safe ledger can be replayed.  Each example must print `L(a0)`,
`U(a0+1)`, `B*`, denominators, endpoint convention, and first-match cell
decomposition.

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
experimental/lean/grande_finale/              Q-focused final attempt
experimental/lean/cap25_cap_v13_raw_compact/  v13 raw companion formalization
```

Treat these as co-priority.  The first track targets
`experimental/grande_finale.tex`: row-sharp Q, BC reduction, SP-from-Q, and
adjacent-threshold logic.  The second track targets the v13 raw/compact
certificate ledger: identity-prefix floors, conversion steps, BC/SP ledgers,
finite certificates, and the theorem nodes that may later be promoted into
Paper D.

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
row-sharp Q atom theorem
finite BC chart-decomposition audit
adjacent deployed safe rows
composite-prefix gcd(e,N) descent
full theorem-by-theorem map to grande_finale.tex
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

1. in `experimental/lean/grande_finale/`, state and prove as much of
   row-sharp Q and the finite BC chart audit as possible;
2. in `experimental/lean/cap25_cap_v13_raw_compact/`, keep the v13 raw
   companion formalization aligned with the raw/compact TeX ledger, especially
   the finite certificates and promotion-ready theorem nodes.

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

- a proof or exact certificate for row-sharp Q;
- a BC chart-decomposition audit that leaves no unpaid high-dimensional branch;
- a quotient/rung audit with exact margins;
- a new adjacent finite example that clarifies the Q frontier;
- a Lean theorem or accurately stated Lean target for the final-resolution
  objects;
- a counterexample that identifies a new obstruction floor;
- a protocol ledger that consumes an already-proved threshold theorem without
  merging field denominators.

A negative result is valuable. If a conjecture fails, identify the new obstruction floor and update the certificate logic accordingly.
