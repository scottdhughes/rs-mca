# Proximity Prize for Smooth Reed-Solomon Domains

This repository is a working research package for settling the smooth-domain Reed--Solomon **mutual correlated agreement (MCA)** and proximity-list questions that arise in the [Proximity Prize program](https://proximityprize.org/).

See the related [IACR ePrint paper](https://eprint.iacr.org/2026/680.pdf).
Visit the [project's website](https://www.rsmca.xyz/).

The central theme is simple:

> Smooth multiplicative Reed--Solomon domains do **not** appear to have a clean “up to capacity with negligible error” theorem. They have a corrected reserve theory. Any near-capacity theorem must clear explicit entropy, quotient, field-accounting, list-size, and MCA/line-decoding floors.

**Pay-per-bit framing.** If the Proximity Prize is allocated pro-rata by
soundness-gap bits, our current results are naturally scored by certified bits
above the `2^-128` target at an audited radius and denominator. Paper D v12 gives
the cleanest broad record: in its cap range it proves `epsilon_mca > 2^-86`,
which is at least **42 bits above** the target throughout the full prize field
envelope. The strongest finite numerator record on the site is the
Cycle116/119 `F_17^32` row, about **32.82 bits above** target, while the exact
tangent-staircase gate gives a narrow but fully structural 6/7 transition. A
pay-per-bit rule would therefore reward both kinds of progress: larger certified
bit margins and, more importantly, certificates that push the unsafe radius
lower or close the interval for `delta*_C(2^-128)`.

The repo is meant for people and AI agents who want to help turn that corrected theory into proofs, counterexamples, parameter certificates, and eventually protocol-grade statements.

## Repository contents

The core repo consists of four main papers, one prize-facing theorem note, one
experimental asymptotic submission draft, and two guide files. `.tex` versions
of the main papers are in `tex/`, experimental manuscripts are in
`experimental/`, and Python scripts for heuristics and certificates are in
`scripts/` or `experimental/scripts/`.

| File | Short name | Role |
|---|---|---|
| `RS_disproof_v3.tex` | **Paper A: no-slack obstruction** | Refutes the unslacked, support-wise line-MCA reading of “up to capacity” for smooth multiplicative RS domains. Provides explicit lower-bound mechanisms and deployed-field obstructions. |
| `slackMCA_v4.tex` | **Paper B: slack / quotient / entropy theory** | Main theory paper. Builds the corrected reserve framework and now promotes the solved high-agreement line/list/curve boundary layer into the main theory. |
| `cs25_cap_v12.tex` | **Paper D: two-sided cap, safe-side pincer, and certificate grammar** | This is the main Proximity Prize submission reference. It keeps the self-contained cap route and adds the safe-side pincer, deployed-row two-sided intervals, map/rational smooth extensions, circle/genus-one transports, explicit witness machinery, optimized failure profile, and certificate grammar v2. |
| `snarks_v5.tex` | **Paper C: SNARK ledger** | Turns the corrected theory into a protocol-facing certificate and adds a theorem-backed high-agreement ledger compiler for line/list/curve coding numerators. |
| `towards-prize.tex` | **Towards Prize: sparse threshold note** | Compact prize-facing note. It packages the `delta^*` staircase viewpoint, deployed KoalaBear pincer, and the new sparse residual reduction `emca = max(eca, sigma_C/q)` into the current execution target. |
| `experimental/asymptotic_rs_mca_frontiers.tex` | **Asymptotic RS--MCA Frontiers** | Current self-contained asymptotic submission draft. It consolidates exact finite-row geometry, profile-envelope compilers, quotient/remainder obstructions, Sidon/BSG primitive analysis, smooth/circle interfaces, finite certificate interfaces, and the remaining hard inputs. |
| `README.md` | Repo overview | Explains what the papers do, how they depend on each other, and what the project is trying to prove. |
| `AGENTS.md` | Research-agent guide | Gives AI agents and new contributors a prioritized list of proof targets, toy cases, scripts, and “do not confuse these” rules. |

The paper-letter order follows the internal blueprint: A = no-slack, B = slack theory, C = SNARK ledger, D = universal cap. The logical reading order is usually **A → B → D → C**.

## The problem we are trying to settle

Let `C = RS[F, D, k]`, where `D` is a smooth multiplicative domain, usually a subgroup or multiplicative coset of power-of-two order `n`, and `rho = k/n` is one of

```text
rho in {1/2, 1/4, 1/8, 1/16}.
```

The Proximity Prize regime asks for sharp thresholds near capacity, especially for target error

```text
epsilon* = 2^-128,
k <= 2^40,
|F| < 2^256.
```

There are two linked threshold problems.

1. **MCA / correlated-agreement threshold.** Determine how close the radius `delta` can get to `1 - rho` while the MCA error remains negligible.
2. **Interleaved-list threshold.** Determine how close `delta` can get to `1 - rho` while the relevant interleaved list size is at most a negligible fraction of the challenge field.

The prize-facing metric is the **radius threshold**, not the largest displayed
error margin.  For target `epsilon* = 2^-128`, the object to determine is

```text
delta*_C(epsilon*) = sup { delta : epsilon_mca(C, delta) <= epsilon* }.
```

Large error at a large radius is useful only as an auditable crossing
certificate.  A barely-supercritical certificate at a smaller radius is more
important.  Equivalently, on the integer agreement grid `a = (1-delta)n`, if
`B_mca(a)` denotes the number of MCA-bad line parameters at agreement at least
`a`, and `B* = floor(epsilon* q_line)` is the exact integer budget, the ideal
certificate is an adjacent staircase:

```text
B_mca(a0)   > B*,
B_mca(a0+1) <= B*.
```

Such a pair pins `delta*_C(epsilon*)` to one integer agreement step.  The
leaderboard and submission notes should therefore rank results primarily by the
smallest certified unsafe radius, or by the tightest proven interval for
`delta*_C(2^-128)`, with error size used as supporting evidence.

For the deployed KoalaBear sextic row, the best current deployed unsafe edge is

```text
delta = 15331/32768 ~= 0.467865.
```

The remaining task is to close the open band below that edge, ideally by
adjacent staircase certificates.

The active experimental program now splits this into two proof problems:

1. **Finite deployed one-step resolution.**  For each deployed row, prove an
   adjacent certificate `U(a0+1) <= B* < L(a0)`, where `L` is the exact unsafe
   staircase, `U` is the complete safe upper ledger, and `B*` is the integer
   challenge budget.  The unsafe side is supplied by exact certificate claims
   in the v13/frontiers sources; the adjacent safe side still needs exact
   constants for the complete upper ledger.
2. **Asymptotic frontier resolution.**  Prove or refute the entropy-subfield
   envelope

   ```text
   delta*_C(epsilon*) = 1 - rho - g*(rho, log2 |B|) + o(1).
   ```

   The current self-contained draft is
   `experimental/asymptotic_rs_mca_frontiers.tex`.  The remaining hard inputs
   are: a witness-exhaustive first-match atlas; image-scale `MI` + `MA`, or a
   direct Sidon payment; a residual ray compiler for higher-dimensional
   balanced cores; complete profile-envelope comparison with the target; and
   the lower reserve / unsafe-side comparison.

These are protocol-relevant because many proximity/SNARK reductions have a soundness term schematically like

```text
MCA_error(C, delta) + |interleaved_list(C, delta)| / |challenge field| + query_error.
```

A list theorem alone is not enough unless it is connected to the exact MCA, CA, line-decoding, or curve-MCA quantity used by the protocol.

## Current picture

The old hoped-for statement was roughly:

> Smooth-domain Reed--Solomon codes should behave well all the way up to capacity, provided the field is large enough.

The corrected picture is:

> Smooth-domain Reed--Solomon codes have explicit near-capacity obstruction floors. A positive theorem must work at radius `1 - rho - eta`, where `eta` clears every known floor and every protocol ledger.

The ledgers that must be separated are:

1. **Generated-field entropy.** The list/locator entropy denominator is the field generated by the domain and the received word, not automatically the large extension challenge field.
2. **Quotient-core obstructions.** Smooth domains have quotient fibers. If `k` and `n` align with large quotient scales, large lists or bad slopes can appear.
3. **Locator-fiber list size.** Base-code locator fibers must be bounded before they can be used in a protocol list budget.
4. **Interleaved list size.** The protocol often consumes `|Lambda(Int(C, mu), delta)|`, not merely the base-code list size.
5. **Challenge-field division.** The list term is divided by the field in which the verifier samples the relevant challenge. Do not silently replace this by a larger or smaller field.
6. **MCA / CA / line-decoding / curve-MCA.** These are related but not interchangeable without a theorem.
7. **Known failure ladders and universal caps.** Some gaps are ruled out by explicit lower bounds or by the universal cap.

## Current paper versions and leaderboard impact

The current public paper set is **A v3, B v4, D v12, C v5**, plus the compact **towards-prize** threshold note.
The version changes matter for the website and scanner as follows:

- **Paper B v4** promotes the high-agreement tangent/list/curve boundary layer
  from experimental notes into the main theory. Public tangent and
  interleaved-list high-agreement rows should now cite `slackMCA_v4.tex` when
  they use this theorem package.
- **Paper D v12** is the main Proximity Prize submission reference. It keeps the
  headline universal MCA cap self-contained, adds a two-sided threshold
  sandwich, proves the deep-regime safe theorem and MCA-from-CA pincer, extends
  the cap machinery to map/rational smooth domains, and packages deployed-row
  claims in certificate grammar v2. Auditing this paper is currently the main
  project focus.
- **Paper C v5** adds the theorem-backed high-agreement ledger compiler for
  protocol-facing line/list/curve numerator accounting. It changes certificate
  packaging and denominator checks, not the mathematical value of the MCA cap
  rows.
- **`towards-prize.tex`** is a compact companion to Paper D v12, not the final
  submission authority. It does not add a new leaderboard row by itself. Its
  role is to state the `delta^*` staircase problem compactly, record the
  deployed KoalaBear pincer, and reduce the remaining MCA task to the sparse
  residual layer plus CA/list certificates.
- **`experimental/asymptotic_rs_mca_frontiers.tex`** is the current
  self-contained asymptotic RS-MCA submission draft. It supersedes the earlier
  `experimental/rs_mca_entropy_frontiers.tex` filename and should be the main
  target for proof audit, Lean formalization, and clean write-up work.
- **`experimental/rs_mca_proximity_prize_status.md`** is an experimental
  committee-facing status memo for the v12/v13 raw picture. It summarizes the
  entropy-subfield-envelope thesis, the current exact unsafe certificates, and
  the remaining `(Q)`/split-pencil conjectural safe side. Do not cite it as
  paper authority until the relevant claims are promoted into Paper D or
  `towards-prize`.
- **`experimental/cap25_cap_v13_raw.tex` and `experimental/grande_finale.tex`**
  are the current experimental final-resolution sources. The former is the long
  raw v13 ledger; the latter isolates the compact `Q`-focused route. They should
  guide finite adjacent-certificate work and the asymptotic envelope proof, but
  are not Paper D authority until promoted.
- **`experimental/lean/towards_prize/`** is the Mathlib-based Lean track for
  the compact threshold note. Its entry point is `TowardsPrize.lean`; it should
  be reviewed and mapped theorem-by-theorem before any towards-prize claim is
  advertised as Lean-certified.

## How the papers fit together

```text
Paper A: no-slack obstruction
        |
        v
Paper B: slack / entropy / quotient-core theory
        |\
        | \__ Paper D: self-contained MCA universal cap
        |
        v
Paper C: SNARK/protocol ledger consuming B and D
```

### Paper A: no-slack obstruction

`RS_disproof_v3.tex` is the base lower-bound paper.

It shows that the no-slack, support-wise line-MCA version of the up-to-capacity conjecture is false for smooth multiplicative RS domains. The organizing mechanism is the **quotient locator identity**: restricted sums in a smooth quotient subgroup produce many bad slopes for lines of the form

```text
x^(k+a) + z x^k.
```

The paper gives explicit consequences over common smooth prime fields such as BabyBear, KoalaBear, `3*2^30+1`, and Fermat-prime examples. Its role in the repo is to be the lower-bound oracle: if a proposed theorem contradicts Paper A’s obstruction intervals, the theorem is false or missing a reserve hypothesis.

### Paper B: slack / quotient / entropy theory

`slackMCA_v4.tex` is the main theory paper.

It generalizes the obstruction into a corrected positive/negative theory. It separates:

- generated-field entropy floors,
- quotient-core list obstructions,
- characteristic-zero rigidity and finite-field collision sieves,
- exact slack bad-slope calculus,
- dyadic descent and failure ladders,
- tangent and quotient-periodic MCA floors,
- residue-line normal forms,
- local-limit conjectures for list decoding and MCA.

Version v4 additionally closes the theorem-backed high-agreement boundary layer:
affine/projective line and no-loss CA numerators are exact in the tangent range,
interleaved lists are unique in their high-agreement range, and degree-`d`
finite power-curve ledgers have a proved upper envelope with split moving-root
exactness.

Paper B is where most new mathematics should land. It contains the theorem/conjecture shape for a corrected reserve theorem: not “up to capacity,” but “up to capacity minus every explicit floor.”

### Paper D: two-sided cap and certificate grammar

`cs25_cap_v12.tex` is the main Proximity Prize submission reference.

It keeps the self-contained universal MCA cap:

```text
delta*_C(2^-128) <= 1 - rho - 2^-9      for rho in {1/2, 1/4, 1/8},
delta*_C(2^-128) <= 1 - rho - 2^-10     for rho = 1/16,
```

throughout the challenge range `|F| < 2^256`, with the stated smoothness/divisibility hypotheses. It gives error `> 2^-86` uniformly and improves to `> 2^-42` when `|F| >= 2n`.

Version v10 also contains the large-row first-grid cap. For the official
rates, once `k` is at least `127, 78, 58, 47` respectively and `q>n`, the first
closed grid point below capacity is already CA/MCA unsafe:

```text
delta*_C(2^-128) <= 1 - rho - 1/n.
```

It also adds the current safe-side and certificate package: a deep-regime MCA
safe theorem for all linear codes, a reduction from MCA to CA up to half the
minimum distance, a self-contained half-Johnson CA bound, map-smooth and
rational-smooth cap extensions, circle/genus-one transports, explicit witness
machinery, an optimized failure profile, and finite certificate grammar v2.

Paper D supersedes the older internal cap in Paper B for final constants.
Paper B keeps its native quotient-core cap because it explains the mechanism;
Paper D v12 owns the current field-size-universal and two-sided cap package,
and is the canonical source for final submission hypotheses, denominators,
endpoint conventions, and proof status.

Version v12 supersedes v10/v11 as the active draft. The main remaining work is
audit: check the direct conversion/radius conventions, the optional BCIKS
half-distance import, exact-integer certificate replay paths, and the precise
scope of the circle/genus-one model transfers.

### Paper C: SNARK ledger

`snarks_v5.tex` turns the corrected theory into a protocol-facing reserve certificate.

Its purpose is not to prove all missing MCA/list theorems. Its purpose is to prevent protocol analyses from mixing ledgers. In particular, it insists on distinguishing:

- base field vs generated field vs extension challenge field,
- implementation interleaving vs protocol list arity,
- base-code lists vs interleaved lists,
- CA vs MCA vs line-decoding vs curve-MCA,
- theorem-backed mode vs conjectural aggressive mode vs obstruction-audit mode.

Version v5 also adds the high-agreement ledger compiler: before invoking
near-capacity conjectures, a protocol certificate can first check the exact
line/list/curve numerator formulas in the small-radius theorem-backed range.

Paper C is the bridge from theory to systems. Once the missing local-limit and line/MCA statements are proved, Paper C should become a compiler from a code/domain tuple to a soundness certificate.

## What is proved, conditional, and open

A rough status map:

| Topic | Current status |
|---|---|
| No-slack smooth-domain MCA obstruction | Proved in Paper A. |
| Explicit deployed-field lower-bound floors | Proved in Paper A/B for the stated regimes. |
| Quotient-core list obstructions | Proved in Paper B. |
| Exact slack calculus and many failure ladders | Proved in Paper B. |
| Universal field-size MCA cap | Proved in Paper D v12 under its printed divisor/binomial/subfield hypotheses. |
| First-grid and widened deployed-row MCA caps | Proved in Paper D v12 under its printed `k`, `q>n`, subfield, and certificate hypotheses. |
| Safe-side pincer and two-sided threshold sandwich | Proved self-contained up to the deep/half-Johnson edges; half-distance edge depends on the isolated BCIKS import. |
| Map/rational smooth, circle, and genus-one extensions | Proved in Paper D v12 under its stated model hypotheses; these are high-priority audit targets. |
| Certificate grammar and printed deployed certificates | Stated in Paper D v12; every "verified exactly" inequality should have a reproducible script or printed integer certificate. |
| Finite deployed adjacent threshold resolution | Open/experimental. v13 raw gives exact unsafe-side certificate claims; the adjacent safe side needs row-sharp `Q`, finite BC chart decomposition, and quotient/rung audits with constants. |
| Asymptotic entropy-subfield envelope | Active submission draft in `experimental/asymptotic_rs_mca_frontiers.tex`. The remaining hard inputs are a witness-exhaustive first-match atlas, image-scale `MI` + `MA` or direct Sidon payment, residual ray compiler for higher-dimensional balanced cores, complete profile-envelope comparison with the target, and lower reserve / unsafe-side comparison. |
| Generated-field locator local limit above all floors | Open. Main list-side positive theorem target. |
| Corrected MCA / residue-line local limit above all floors | Open. Main MCA-side positive theorem target. |
| Line-decoding formulation of corrected MCA | Open. Important for protocols. |
| Extension-line MCA transfer | Open: prove a clean lift or find counterexamples. |
| Sharp interleaved-list constants near capacity | Open. Important for protocol soundness budgets. |
| Protocol-level FRI/WHIR ledger rewrites | Open engineering/proof task. |
| Certificate scanner | Prototype in `experimental/notes/certificate_scanner/`; emits JSON/Markdown A/B/C/D ledger reports. |

## How to contribute

Good first contributions include:

1. **Proof audits.** Verify individual lemmas and theorem dependencies in the four papers. Flag any hidden field-size, divisibility, monotonicity, or support-wise assumptions.
2. **Scripted certificates.** Implement scanners for entropy reserve, quotient profiles, restricted sums, interleaved-list budgets, and challenge-field accounting.
3. **Toy-case exploration.** Exhaust small fields/domains to discover or refute local-limit behavior.
4. **Paper D v12 audit.** Check direct conversion/radius conventions, ABF
   normalization, the optional BCIKS import, exact-integer certificates, and
   circle/genus-one model transfers.
5. **Hankel certificates.** Use `scripts/aperiodic_eliminant_schema.json` to
   package exact-agreement eliminants, empty chart certificates, or named
   residual obstructions for the Paper D v12 certificate grammar.
6. **Finite/asymptotic threshold work.** Attack the five current hard inputs:
   witness-exhaustive first-match atlas; image-scale `MI` + `MA` or direct
   Sidon payment; residual ray compiler for higher-dimensional balanced cores;
   complete profile-envelope comparison with the target; and lower
   reserve/unsafe-side comparison.
7. **New bounds.** Attack the local-limit conjectures, interleaved-list constants, extension-line MCA, or domain-shattering alternatives.
8. **Protocol rewrites.** Rewrite FRI, WHIR, or other proximity reductions in the exact ledger format of Paper C.

See `AGENTS.md` for a prioritized task list and suggested toy cases.

## Script layer

The first heuristic script is `scripts/run_frontier.py`, an **EXPERIMENTAL** Paper B frontier scanner. For each prime `p` passed on the command line, intended with `32 | p-1`, it builds the order-32 multiplicative subgroup of `F_p`, uses a meet-in-the-middle subset enumeration at fixed `l = 18`, and records which elementary-symmetric fingerprints `(e1, e2)` are realized by `l` subgroup elements. Its coverage line measures how much of `F_p^2` this restricted quotient-locator map hits and appends the result to `frontier_results.txt`; full coverage is evidence about quotient/restricted-sum frontier behavior, not a proof by itself. The script currently requires `numpy` and `sympy`.

The certificate scanner prototype lives in
`experimental/notes/certificate_scanner/`.  It reads a row/config JSON and emits
both a machine-readable report and a Markdown audit for generated-field entropy,
exact-divisibility quotient profile, Paper D cap hypotheses, high-agreement
line/list/curve ledgers, and the combined protocol-ledger verdict.  It is a
ledger-audit tool, not a proof of extension-line MCA, arbitrary-word locator
local limits, aperiodic Hankel-pencil packing, or deployed protocol soundness.

The aperiodic Hankel certificate schema lives at
`scripts/aperiodic_eliminant_schema.json`. It is for Paper D v12 certificate
packets: row and domain hash, exact agreement levels, removed tangent/quotient
ledgers, regular minors, pivot charts, eliminants, empty-chart proofs,
dimension-degree fallbacks, and named residual obstructions.

The broader intended script layer is:

```text
scripts/
  run_frontier.py            # EXPERIMENTAL psi_2 restricted-subset frontier scan
  entropy_margin.py          # generated-field entropy reserve
  quotient_profile.py        # active quotient scales at actual (n, k, a)
  restricted_sum_dp.py       # restricted-sum / DSH verification certificates
  locator_fiber_scan.py      # small-field locator-fiber experiments
  mca_slope_scan.py          # small-field bad-slope / residue-line experiments
  interleaved_budget.py      # base/interleaved list-to-field soundness budget
  certificate_emit.py        # JSON + TeX certificate tables for Paper C
  aperiodic_eliminant_schema.json
                              # Paper D v12 Hankel eliminant certificate schema

experimental/notes/certificate_scanner/
  certificate_scanner.py     # EXPERIMENTAL A/B/C/D + high-agreement ledger scanner
  examples/*.json            # reproducible row configs
  outputs/*.report.{json,md} # replayable scanner outputs
```

A useful script should emit both human-readable output and a machine-checkable certificate. Hand-computed tables should eventually be replaced by script output.

## Conventions

Use these conventions when adding results:

- `rho = k/n` is the rate.
- `delta = 1 - rho - eta` is the proximity radius.
- `eta` is the reserve/gap from capacity.
- `q_gen` is the field generated by the domain/received-word data.
- `q_line` is the field from which line or CA/MCA challenges are sampled.
- `q_chal` is the verifier challenge field; it may or may not equal `q_line`.
- `mu` is protocol list arity.
- `nu` is implementation interleaving.
- `Qprof` is the quotient-profile obstruction ledger.

When in doubt, keep the fields separate. Most false near-capacity claims come from giving the same field-size credit to two different ledgers.

## Citation and release hygiene

When editing the papers:

- Cite companion results with theorem/proposition numbers, not just “the companion proves.”
- Mark every result as proved, conditional, conjectural, experimental, or audit-only.
- Cite the main Paper D v12 MCA cap, safe-side pincer, and certificate grammar
  as the active Paper D package, under their printed hypotheses and audit
  caveats.
- Do not state an error-one result from Paper D’s cap; Paper D caps the threshold and gives a small certified failure probability, but the error-one-in-the-band problem remains open.
- Keep Paper D as the canonical reference for the final universal-cap constants.
- Keep Paper C as the canonical reference for protocol ledgers and field-accounting rules.

## Project goal

The goal is to settle the Proximity Prize MCA/list questions for smooth-domain Reed--Solomon codes in a way that is useful for proof systems.

A positive outcome would be a theorem-backed reserve certificate: given a domain, rate, field, interleaving, and protocol reduction, the repo can certify a near-capacity radius and soundness budget.

A negative outcome is also valuable: every obstruction becomes a new floor, a warning for protocol designers, or a reason to switch to folded/subspace-design codes, random/punctured domains, or domain-shattered constructions.

Either way, the aim is to replace folklore “near-capacity RS should work” claims with exact, checkable mathematics.

The current work was done with GPT-5.5 Pro and Claude Fable 5 and still needs proper revision. Human input is welcome.
