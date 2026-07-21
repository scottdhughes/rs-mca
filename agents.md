# AGENTS.md — RS–MCA Resolution Protocol

> **Updated:** 2026-07-21
> **State snapshot:** `main@a3017697ad1594521d2779fe1d83bccd45d4c06e`
> **Supersedes:** all older priority lists in this file.

Edit this workboard in place. Never append another “current focus”, “highest priority”, or competing task list.

Before starting, compare the snapshot with current `main`, then read the newest entry in `experimental/agents-log.md` and the live four-row completion packet. If the state changed, update the snapshot, authority table, and workboard before doing mathematics.

## 1. Mission and resolution standard

The target is the true numerator

```text
B^MCA_{C,Gamma}(a)
  = maximum, over received lines, of the number of distinct bad slopes.
```

The repository should be driven toward a direct proof or counterexample about this quantity, not toward more summaries, theorem skeletons, or a formally checked unresolved ledger.

Grande Finale v4 is the preferred current completion architecture, but it is not the definition of truth. A uniform direct theorem may bypass it. A counterexample to one proof route need not refute the target inequality.

The primary unresolved official benchmark in the four-row packet is

```text
KoalaBear MCA, target 2^-128:
B^MCA_C(1116048) <= 274980728111395087.
```

Agreement `1116047` is already proved unsafe. Proving the displayed upper bound therefore determines the first safe agreement exactly.

A result counts as resolution progress only if it does at least one of these:

1. proves or refutes a direct benchmark inequality;
2. replaces a live `null` atom by an independently reviewed exact integer;
3. supplies the missing source-bound architecture/owner bridge;
4. proves exhaustive coverage and the correct slope/codeword projection for a live residual;
5. rigorously removes a live route and updates the residual state; or
6. completes the exact add-back and row certificate.

For a family-level or asymptotic resolution, give a matching upper/lower bracket for the true numerator on a precisely declared family. The identity-profile formula remains an identity-candidate conjecture until witness exhaustion and every payment are proved.

Protocol consumption is downstream and is not a current resolution target.

In this file, `Q` means the pruned locator-prefix maximum-fiber atom; `BC` means the balanced-core distinct-slope atom; and `U_list_int` means the arbitrary-word interior codeword atom. These are ledger names, not assumptions that the corresponding bounds are proved.

## 2. Target correction and current verified state

The nonzero-budget packet contains one official primary MCA row and three auxiliary theorem-building rows:

| Row | Role and target | Unsafe `a0` | Candidate `a+` | `B*` | Full-budget Q multiplier floor | Verdict |
|---|---|---:|---:|---:|---:|---|
| KoalaBear MCA | **primary**, `2^-128` | 1116047 | 1116048 | 274980728111395087 | 4807520 | open |
| KoalaBear list | auxiliary, `2^-128` | 1116046 | 1116047 | 274980728111395087 | 4226236 | open |
| Mersenne-31 MCA | auxiliary, `2^-100` | 1116023 | 1116024 | 16777215 | 9 | open |
| Mersenne-31 list | **analytic stress test**, `2^-100` | 1116022 | 1116023 | 16777215 | 8 | open |

**Do not misstate the target.** For the Mersenne-31 code over `F_(p^4)`, target `2^-128` has integer budget `B*=0`; its complete safe set is empty. The `B*=16777215` Mersenne rows are `2^-100` stress tests, not unresolved `2^-128` Prize rows.

At this snapshot:

- CAP25 v13.2 proves the unsafe endpoints and reusable foundation results.
- Grande Finale v4 proves many local identities, order-32/rational-atom reductions, owner localization, and spread-core incidence bounds, but no adjacent safe row.
- The live compiler returns `ARCHITECTURE_ROUTE_CUT_CURRENT_ARTIFACT_SET`, not `SAFE`.
- Every deployed `U_Q` remains `null`.
- The Mersenne-31 LIST source adapter now gives one bankable v4 cell,
  `LOW_EXACT_WEIGHT_PACKING -> U_paid<=3730`, directly over `F_(p^4)`.
  Its high boundary/interior `U_new` residual remains `null`.
- No row has complete active-architecture `U_paid`, exhaustive MCA balanced-core or list-interior payment, zero/exact residual, and chronology-correct add-back.
- The KoalaBear legacy M1 stack records local `U_paid=422354730332` and local remainder `274980305756664755`, but neither is banked in Grande Finale v4 because the source-bound owner/partition bridge is missing.
- Under the latest corrected direct extension charge, positive extension dimension is excluded on Mersenne-31 and dimension at least two is excluded on KoalaBear. These are route cuts, not payments or nonexistence theorems.
- The M31 LIST algebraic padding bridge and distinguished-column coloop are
  closed: the canonical Popov and masked Padé pairs have the same polynomial
  right kernel, the padding mask is recovered by a monic gcd, and every
  forced key has a simultaneous canonical rank-three frame.  The global
  common-core owner/refund, complete-list incidence, residual, and final
  finite-ledger terminals remain open.
- A schema/hash pass is structural preflight only. The legacy four-row compiler trusted-source registry is empty; the new M31 adapter hash-binds its theorem sources, but parsing either manifest does not itself prove an atom.

## 3. Document authority

| File | Role |
|---|---|
| `experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md` and `experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json` | **Live status authority:** current null atoms, route cuts, architecture IDs, exact row arithmetic, and replay contract. |
| `experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex` | **Direct problem/falsifier authority:** benchmark conjectures, exact compiler requirements, finite barriers, and separation of finite from conjectural asymptotic claims. |
| `experimental/grande_finale.tex` | **Active conditional completion architecture:** proved local theorems, order-32/rational-atom reductions, owner localization, spread-core incidence bounds, and exact completion problems. Hypotheses/problems are not row bounds. |
| `experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md` and `experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json` | **M1 target-source adapter authority:** direct quartic exact-layer lift, bankable low-weight cell, exact global occupancy, coupled rank-46 diagnostic, and explicit unpaid high residual. It does not close the row. |
| `experimental/notes/thresholds/m31_canonical_masked_pade_global_route_cut.md` and `experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json` | **M1 canonical-mask authority:** target-field Popov–Padé right-kernel bridge, exact padding/error classifier, simultaneous rank-three/no-coloop theorem, conditional target-field deformation dichotomy, and exhaustive natural-collision regression. It moves no atom and leaves the row open. |
| `tex/cs25_cap_v13_2.tex` | **Foundation/unsafe authority:** exact unsafe endpoints, field/domain conventions, reductions, and certificate grammar. |
| `experimental/RS_MCA_Paving_v9.2.tex` | **Proved safe-bound toolbox:** shortening, MDS circuit, exact finite, exponential-budget, and conditional Sidon-to-flatness results. It does not solve the subexponential near-capacity frontier. |
| `experimental/rs_mca_thresholds.tex` | **Exact-regime/exposition source:** staircases, below-half-distance results, syndrome geometry, and examples; not unrestricted near-capacity closure authority. |
| `tex/RS_disproof_v3.tex`, `tex/slackMCA_v4.tex`, `tex/snarks_v5.tex` | Stable background for no-slack obstructions, reserve/quotient theory, and later protocol accounting. |
| `archived/` predecessors | Provenance only. Never bank an archived owner or charge without an explicit source-bound bridge. |

`experimental/agents-log.md` is a coordination record, not proof authority.

## 4. The one live workboard

Work on exactly one item below. Every contribution must name its row, direct target, item ID, quantifier, projection, and exact impact.

### Lane K — close or refute KoalaBear MCA at `2^-128`

#### K0. Freeze one active row contract

Maintain one canonical manifest containing fields, domain, `n`, `k`, target, endpoint convention, challenge denominator, active architecture ID, partition digest, owner order, object `MCA`, unit “distinct bad slopes per received line”, and exact budget. Every candidate atom binds to it.

#### K1. Make existing KoalaBear work bankable

Either:

- prove a source-bound, owner-by-owner bridge from the legacy M1 partition into the active Grande Finale v4 first-match partition, including inherited charge and exhaustive scope; or
- re-prove the useful local payments directly inside the active partition.

Do not add more legacy-local charges unless they independently prove the direct numerator inequality or include this bridge. Matching parameters and similar cell names are not a composition theorem.

#### K2. Prove the exact pruned row-sharp Q atom

Prove one joint maximum over the frozen first-match residual, using the actual domain, attained image, target map, orientation transport, support-to-parameter coalescing, and a uniform received-line quantifier. Output an exact integer `U_Q`.

The factor `4807520` is only a full-budget calibration before other atoms consume reserve. A shell bound, average, lower floor, target value, separately normalized residual, or conditional allocation is not `U_Q`.

#### K3. Pay MCA projection and residual geometry

Produce exhaustive balanced-core coverage in units of distinct affine slopes. The moving-root theorem pays only charts proved to be genuine pencils. A line-by-line decomposition also needs an exact count of relevant lines. Higher-dimensional cores require a proved ray/slope compiler with exact multiplicities.

#### K4. Close algebraic routing and add-back

Pay or eliminate quotient, extension, periodic/descent, rank, padding, common-core, planted, sparse, shortened, interleaved-list, and every other named cell in the same first-match chronology. Prove `U_new=0` or give an exact integer for each survivor.

#### K5. Emit the row certificate

Prove with exact integers

```text
U_total = U_paid + U_Q + U_BC + U_new
        <= 274980728111395087.
```

Replay it with independent implementations and mutation tests. Then state:

```text
first safe agreement       = 1116048
largest safe grid radius   = 981104/2097152
real safe set              = [0, 981105/2097152)
real supremum              = 981105/2097152, not attained
```

A direct uniform proof of `B^MCA_C(1116048)<=B*` may replace K1-K5, but it must still provide independently checkable constants and endpoint conversion.

### Lane M — use Mersenne-31 list at `2^-100` as the tight falsification test

#### M0. Decide the direct inequality

Prove or refute

```text
B^list_C(1116023) <= 16777215.
```

This is a codeword-count statement; the MCA ray compiler is inapplicable.

#### M1. Resolve the binding primitive-fiber/list-interior problem

The full-budget target is only about `8.4152` times the full-slice average, and the true allowance is smaller after other payments. Prove a realized-image, frozen-residual maximum or construct a received word exceeding the budget. Existing one-shell and rooted-shell packets are local reductions, not exhaustive row bounds.

Current source-bound status: the v4 adapter lifts the complete exact-support,
common-core, Padé, and coupled-kernel chain directly to the deployed
quartic field.  The fixed low-weight predicate is bankable as
`U_paid<=3730`.  Every remaining target codeword lies in one explicit
boundary or interior `U_new` residual.  Any hypothetical forbidden list
forces at least `259881` distinct marked target-codeword keys, and every key
has three independent simultaneous canonical Popov--Padé rows of combined
degree at most `62295<67447`.  The discarded-agreement mask and actual error
locator are recovered exactly by a monic gcd; fixed-layer transport obeys an
exact diagonal-saturation law; and deleting the distinguished column cannot
drop the rank.  The conditional target-field deformation dichotomy proves
that selected-family cardinality cannot force a collision unless a collision
form is identically zero on the common containment space.  An exhaustive
same-received-word `GF(17)` layer has disjoint-packing optimum five and
natural collision-root transversal number six, so the local coupled data do
not force four-root overlap coalescence.
`U_Q`, `U_list-int`, `U_ext`, and the high `U_new` value remain null.  The
exact terminal is `UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND`.  The next
M1 theorem must classify every identically forced component and route it with
chronology-correct refunds, prove an M31-specific complete-list/cross-weight
incidence theorem, eliminate the primitive masked component, or bound the
complete distinguished-codeword projection by `259880`; another standalone
fixed-width computation cannot close the row.

#### M2. Transfer the theorem or record a new floor

If true, isolate exactly what transfers to KoalaBear Q or other list/MCA cells, with field and projection hypotheses explicit. If false, record the witness mechanism, update the benchmark conjecture/lower floor, and remove every invalidated closure route.

Never describe this auxiliary `2^-100` row as an unresolved `2^-128` Prize row.

### Lane T — cross-row theorems only when they specialize to a live integer

A Sidon/Fourier, entropy, incidence, shortening, or ray theorem belongs here only if it supplies:

- a bankable exact atom in Lane K or M;
- a direct benchmark upper theorem;
- a direct benchmark counterexample; or
- a rigorous route cut that updates the compiler residual.

An `exp(o(n))` bound, unspecified polynomial loss, fixed low moment, heuristic, or theorem skeleton does not decide the few-bit Mersenne margins and does not automatically fit KoalaBear.

## 5. Exact bankability contract

For Grande Finale v4, every bad object enters one declared, non-oracular, witness-exhaustive first-match partition.

```text
MCA:  U_total = U_paid + U_Q + U_BC       + U_new
LIST: U_total = U_paid + U_Q + U_list_int + U_ext + U_new
```

Every atom shares the same row/target, object, architecture ID, partition digest, owner order, received-line/word quantifier, unit, and source-bound dependencies. Every value is an exact nonnegative integer.

No atom may consume the full budget unless all other atoms are proved zero. Lower bounds, capacities, headrooms, averages, and allocations are not upper payments.

A direct theorem outside the compiler is welcome, but it must state the same row, object, uniform quantifier, unit, and exact target inequality.

Every note, audit, script packet, or PR begins with:

```yaml
workboard_item: K0/K1/K2/K3/K4/K5/M0/M1/M2/T
row: exact row name
object: MCA/LIST/CA/LINE/OTHER
target_epsilon: exact value
agreement: exact integer
B_star: exact integer
direct_statement: exact theorem or inequality
architecture: DIRECT or exact architecture id
partition_digest: required unless DIRECT
atom_or_cell: exact owner/atom, or DIRECT
quantifier: exact maximum/uniform statement
projection_and_unit: slopes/rays/codewords/supports/pairs
claimed_bound: exact integer or symbolic theorem
status: PROVED/CONDITIONAL/CONJECTURAL/EXPERIMENTAL/AUDIT/COUNTEREXAMPLE
impact: ROW_CLOSURE/ROW_COUNTEREXAMPLE/BANKABLE_ATOM/ARCHITECTURE_BRIDGE/ROUTE_CUT/LOCAL_ONLY
falsifier: explicit invalidating condition or witness
replay: commands and source hashes, when computational
```

`PROVED LOCAL` is not automatically `BANKABLE_ATOM`. State the remaining bridge to the row numerator.

## 6. Stop rules

The following do not count by themselves as resolution progress:

```text
new theorem statements without proofs;
Lean stubs, axiomatized global conjectures, or correspondence names;
new survey or “final” paper drafts;
theorem-label maps and clean rewrites;
toy examples not testing a live claim;
random-fiber heuristics or small scans without a lifting theorem;
structural JSON/schema acceptance;
proofs inside an unmapped archived architecture;
a lower construction falling below budget;
a shell, pencil, or chart silently treated as exhaustive;
an asymptotic loss substituted for an exact finite reserve.
```

Do not start protocol accounting, broad end-to-end formalization, or another grand synthesis paper while the direct benchmark and live atoms remain open.

## 7. Audit, replay, and Lean

### Adversarial audits

Test witness exhaustion, first-match chronology, uniformity, attained-image normalization, projection to slopes/codewords, field/orbit/rank/degree multiplicities, owner composition, integer rounding, endpoints, and any local-to-exhaustive jump.

End every audit with exactly one verdict:

```text
NO ISSUE
FIXED
OPEN GAP
COUNTEREXAMPLE_NEW_FLOOR
```

An `OPEN GAP` names the workboard item and smallest missing theorem/integer. A counterexample updates the direct target, compiler residual, or obstruction floor.

### Computational packets

A closing packet includes exact inputs, source labels and hashes, integer-only gates, canonical JSON, human-readable proof summary, an independently written verifier, optimized/non-optimized replay where relevant, mutation tests, and explicit nonclaims. Floating point never decides a gate. A stale source pin is a failed provenance gate.

### Lean policy

Lean verifies frozen mathematics; it is not a substitute for missing mathematics. High-value targets are proved local theorems used by live atoms, first-match/add-back kernels, endpoint/integer conversion, final row certificates, and counterexample correspondence.

A declaration is certified only after the package builds and its statement is manually matched to the proof source. An axiom, `sorry`, theorem target, or skeleton is not a proof or success criterion. Do not formalize Grande Finale v4 “end to end” while its global inputs remain hypotheses.

## 8. Stable invariants

- Keep base/coefficient field, ambient/code field, line field, challenge field, and every denominator distinct unless a theorem transfers them.
- Keep list, CA, support-wise MCA, line decoding, supports, pairs, rays, and affine slopes distinct.
- MCA counts each affine slope once; an enormous support census may represent one slope.
- Use exact integer budgets and closed-ball endpoint conventions.
- Do not use an extension field to pay a base-field image/entropy deficit without a transfer theorem.
- Do not call a residual predicate a payment or a first-match list exhaustive merely because its last cell is “other”.
- Do not merge atoms from different partitions, owner orders, normalizations, or quantifiers.
- Keep Papers A-D stable unless the maintainer requests edits; new work starts in `experimental/`.
- Log every material experimental change in `experimental/agents-log.md`.
- Preserve status labels; never promote conditional, experimental, or local results to proved row statements.

## 9. Minimal reading path and promotion

1. Live four-row compiler note and canonical JSON.
2. Introduction, exact compiler, finite benchmark, and finite-closure problem in `Conjectures_and_Barriers_RS_MCA_v4_1.tex`.
3. Audited-status, finite-Q barrier, and exact-completion sections of `grande_finale.tex`.
4. Exact unsafe-row/certificate sections of `cs25_cap_v13_2.tex`.
5. Main theorem/status sections of `RS_MCA_Paving_v9.2.tex`.
6. Only then, row-specific notes and scripts named by the live compiler.
7. Use `rs_mca_thresholds.tex` for solved exact regimes; use archives only for provenance.

Do not begin by reading every historical note. Start from the direct inequality and follow only dependencies that can change its truth or exact bound.

Promote a result only after its direct statement and quantifiers are frozen, dependencies are source-bound, finite specialization is replayed, projection/ownership is audited, status is proved, and the workboard is updated. Close or refute a row before writing the paper that calls it a resolution.

## 10. Definition of done

The primary finite program is done when one of these is checked in and independently audited:

### KoalaBear safe resolution

```text
B^MCA_C(1116047) > 274980728111395087
B^MCA_C(1116048) <= 274980728111395087
```

with the exact half-open safe set and endpoint data from K5.

### KoalaBear counterexample/new floor

An explicit received line has more than `274980728111395087` bad slopes at agreement `1116048`, together with the resulting later unsafe edge or obstruction mechanism.

### Uniform theorem

A proved theorem specializes to the KoalaBear inequality and states exactly whether and how it transfers to the auxiliary list and Mersenne stress rows.

For the broader RS-MCA problem, “done” means a direct, peer-auditable classification of the true numerator or safe set on the declared family, not completion of a chosen ledger, a conditional identity profile, or a formalized conjecture.
