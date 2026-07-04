# Agents Log

This file is the working ledger for agent-created material in `experimental/`.
Use it to record every new note, script, scan, formalization stub, or audit before
the material is promoted into `tex/` or `scripts/`.

The log is not a proof-status authority. It is a coordination record: what was
added, why it might matter, and what a human or later agent should check next.
Keep entries concise and link to the relevant files.

## Entry Format

```markdown
### YYYY-MM-DD - Short title

- **Agent/model:** Name the agent or model, for example `GPT-5.5 Pro`,
  `Claude Fable 5`, or `Codex`.
- **Files added or changed:** List paths under `experimental/`, `tex/`,
  or `scripts/`.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE.
- **What is being added:** State the claim, note, scan, script, proof,
  heuristic, or computation
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-07-02 - M1 a327 connected-subtree selected-class construction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_connected_subtree_selected_class_construction.md`,
  `experimental/scripts/scan_m1_a327_connected_subtree_selected_class_construction.py`,
  `experimental/scripts/verify_m1_a327_connected_subtree_selected_class_construction.py`,
  `experimental/scripts/audit_m1_a327_connected_subtree_selected_class_construction.sage`,
  `experimental/data/m1_a327_connected_subtree_selected_class_construction.json`,
  `experimental/agents-log.md`.
- **Status:** CONSTRUCTION_FAIL / CONNECTED_SUBTREE_GLOBAL_COUNT_OBSTRUCTION /
  PARTIAL / EXPERIMENTAL.
- **What is being added:** A connected-subtree selected-class construction
  audit. The proposed cycle-free construction is blocked by a tree-edge
  incidence count: support `327` for seven witnesses forces at least `1777`
  tree-edge incidences, while six tree edges under the RS pair cap allow at
  most `1530`.
- **How it is useful:** Rules out this attractive construction principle before
  spending time on exact lifting, and explains why singleton classes alone do
  not rescue the tree-connected model.
- **What to do next:** Move to a broader low-cycle or bounded-cycle incidence
  model with more than six equality carriers, while retaining enough structure
  to keep tree-rank/cycle-rank constraints controllable.

### 2026-07-02 - M1 a327 RS-feasible hypergraph tree-rank feedback

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_rs_feasible_hypergraph_tree_rank_feedback.md`,
  `experimental/scripts/scan_m1_a327_rs_feasible_hypergraph_tree_rank_feedback.py`,
  `experimental/scripts/verify_m1_a327_rs_feasible_hypergraph_tree_rank_feedback.py`,
  `experimental/scripts/audit_m1_a327_rs_feasible_hypergraph_tree_rank_feedback.sage`,
  `experimental/data/m1_a327_rs_feasible_hypergraph_tree_rank_feedback.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_EXACT_NULLITY_ZERO /
  PARTIAL / EXPERIMENTAL.
- **What is being added:** A rank-feedback selected-class hypergraph scan that
  keeps supports exactly `327`, enforces the RS pair cap, and screens
  tree-divisibility matrices with a finite-field proxy before Sage exact audit.
- **How it is useful:** Tests whether changing the selected-class incidence
  design can produce positive tree-divisibility nullity. The first batch tested
  12 RS-feasible assignments, found zero proxy-positive candidates, and exact
  audited the best proxy case as rank `424`, nullity `0` over `GF(17^32)`.
- **What to do next:** Broaden the feedback model beyond reweighting class
  counts and tree edges; the current data suggests the cycle-rank obstruction
  requires altering the incidence structure more substantially.

### 2026-07-02 - M1 a327 selected-class tree-divisibility lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_selected_class_tree_divisibility_lift.md`,
  `experimental/scripts/scan_m1_a327_selected_class_tree_divisibility_lift.py`,
  `experimental/scripts/verify_m1_a327_selected_class_tree_divisibility_lift.py`,
  `experimental/scripts/audit_m1_a327_selected_class_tree_divisibility_lift.sage`,
  `experimental/data/m1_a327_selected_class_tree_divisibility_lift.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / TREE_DIVISIBILITY_NULLITY_ZERO /
  PARTIAL / EXPERIMENTAL.
- **What is being added:** A Reed-Solomon tree-divisibility compression of the
  selected-class quotient system from `016f04d`. The best tree reduces the
  target to a `2874 x 372` exact matrix over `GF(17^32)`.
- **How it is useful:** Replaces the stalled monolithic `1777 x 1536` quotient
  solve with an exact root-polynomial divisibility system. The reduced best
  tree has rank `372` and nullity `0`; two alternate trees checked separately
  also have nullity `0`.
- **What to do next:** Feed this algebraic-rank obstruction back into the
  RS-feasible selected-class hypergraph search, targeting designs with positive
  tree-divisibility nullity rather than only support and pair-cap feasibility.

### 2026-07-02 - M1 a327 selected-class quotient nullspace lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_selected_class_quotient_nullspace_lift.md`,
  `experimental/scripts/scan_m1_a327_selected_class_quotient_nullspace_lift.py`,
  `experimental/scripts/verify_m1_a327_selected_class_quotient_nullspace_lift.py`,
  `experimental/scripts/audit_m1_a327_selected_class_quotient_nullspace_lift.sage`,
  `experimental/data/m1_a327_selected_class_quotient_nullspace_lift.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / PREFIX_RANK_AUDIT / PARTIAL / EXPERIMENTAL.
- **What is being added:** A quotient-difference formulation of the thin
  selected-class target from `9fcdb02`, using variables
  `D_2,...,D_7` and a `1777 x 1536` exact matrix over `GF(17^32)`.
- **How it is useful:** Removes the auxiliary received-word variables and
  isolates the actual non-diagonal lift question. Prefix ranks for row limits
  `128`, `256`, and `512` are full row rank; the full quotient nullspace and
  pair-projection test remain pending.
- **What to do next:** Build an optimized full solve or prepared matrix cache
  for the quotient system, then compute nullity, test all 21 pair projections,
  and construct an explicit seven-distinct vector if the projection criterion
  clears.

### 2026-07-02 - M1 a327 selected-class thin exact lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_selected_class_thin_exact_lift.md`,
  `experimental/scripts/scan_m1_a327_selected_class_thin_exact_lift.py`,
  `experimental/scripts/verify_m1_a327_selected_class_thin_exact_lift.py`,
  `experimental/scripts/audit_m1_a327_selected_class_thin_exact_lift.sage`,
  `experimental/data/m1_a327_selected_class_thin_exact_lift.json`,
  `experimental/agents-log.md`.
- **Status:** PROOF_RECORD / CANDIDATE / EXACT_EXTRACTION_NO_A327 / PARTIAL.
- **What is being added:** A thin selected-class lift target derived from the
  RS-feasible `2e134d7` hypergraph. The best target has supports exactly
  `[327,327,327,327,327,327,327]`, `2289` selected incidences, max pair count
  `194`, and pair-7 counts `[194,194,194,193,194]`.
- **How it is useful:** Gives the first exact-lift target in this lane that
  keeps the Reed-Solomon pair cap and uses explicit received-word variables
  instead of forcing non-selected value-class equalities.
- **What to do next:** Replace the current prefix-rank-only Sage audit with an
  optimized full exact solve or prepared matrix cache for the `2289 x 2304`
  selected-class system, then sample the nullspace for seven distinct
  degree-`<256` codewords.

### 2026-07-02 - M1 a327 RS-feasible value-class hypergraph pre-solver

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.md`,
  `experimental/scripts/scan_m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.py`,
  `experimental/scripts/verify_m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.py`,
  `experimental/data/m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.json`,
  `experimental/agents-log.md`.
- **Status:** RS_HYPERGRAPH_SEARCH / CANDIDATE / EXPERIMENTAL.
- **What is being added:** A corrected selected-class hypergraph pre-solver
  that enforces the Reed-Solomon pairwise co-occurrence cap
  `pair_ij <= 255` before exact lifting.
- **How it is useful:** Rejects the best `e4e966a` full-partition hypergraph as
  non-liftable, then searches directly for selected received classes satisfying
  support, pair-7, pair-cap, and split-robustness constraints.
- **What to do next:** Lift the best selected-class candidate with explicit
  received-word variables `r_h`. The best first-pass target has supports
  `[351,351,351,351,351,351,351]`, max pair count `231`, and pair-7 counts
  `[231,231,231,193,231]`.

### 2026-07-02 - M1 a327 value-class hypergraph pre-solver

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_valueclass_hypergraph_pre_solver.md`,
  `experimental/scripts/scan_m1_a327_valueclass_hypergraph_pre_solver.py`,
  `experimental/scripts/verify_m1_a327_valueclass_hypergraph_pre_solver.py`,
  `experimental/data/m1_a327_valueclass_hypergraph_pre_solver.json`,
  `experimental/agents-log.md`.
- **Status:** HYPERGRAPH_SEARCH / CANDIDATE / EXPERIMENTAL.
- **What is being added:** A discrete value-class hypergraph pre-solver for the
  M1 `a=327` lane. It chooses partition-count hypergraphs over 512 coordinates
  and optimizes Hall/pair/capacity guards under split probes before any exact
  `GF(17^32)` lift is attempted.
- **How it is useful:** Moves beyond exact local patching of the fragile
  `[1,4,5,7]` basin by asking whether a split-resilient Hall-feasible value
  geometry exists at all.
- **What to do next:** Convert the best split-resilient partition-count
  skeletons into exact equality-row lifting targets over `GF(17^32)`. Treat the
  current result as a discrete candidate only, not as an exact witness or public
  row.

### 2026-07-02 - M1 a327 upstream B47 robust exact scanner full grid

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json`,
  `experimental/data/m1_a327_upstream_b47_robust_exact_scanner_cases/*.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** The full 24-system upstream B47-robust exact scanner
  grid. It constructed 11 exact vectors, found 13 inconsistent systems, had no
  timeouts, and found zero split-resilient skeletons.
- **How it is useful:** Tests the first upstream alternatives to the banked
  `[1,4,5,7]` repaired-skeleton basin. The best vector still fails capacity
  robustness, with best capacity 235 and pair values
  `[575,657,657,575,575]`.
- **What to do next:** Treat this as a local exact-search negative for the
  tested upstream scanner, not a global theorem. Decide whether to write a
  broader upstream B47-basin audit or design a materially different upstream
  skeleton family.

### 2026-07-02 - M1 a327 upstream B47 robust exact scanner

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_upstream_b47_robust_exact_scanner.md`,
  `experimental/scripts/scan_m1_a327_upstream_b47_robust_exact_scanner.py`,
  `experimental/scripts/verify_m1_a327_upstream_b47_robust_exact_scanner.py`,
  `experimental/scripts/audit_m1_a327_upstream_b47_robust_exact_scanner.sage`,
  `experimental/scripts/run_m1_a327_upstream_b47_robust_exact_scanner_batch.py`,
  `experimental/scripts/merge_m1_a327_upstream_b47_robust_exact_scanner_results.py`,
  `experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json`,
  `experimental/agents-log.md`.
- **Status:** PROOF_RECORD / CANDIDATE / EXACT_EXTRACTION_NO_A327 / PARTIAL /
  EXPERIMENTAL.
- **What is being added:** A bounded exact-field scanner scaffold for upstream
  B47-robust repaired skeletons, with one-case-at-a-time Sage batching so slow
  GF(17^32) residual solves are recorded as execution facts rather than
  blocking the scan.
- **How it is useful:** Converts the 0500d07 handoff ledger into an exact
  construction lane that tests split resilience before treating a skeleton as
  progress, while preserving the interleaved-list/non-MCA discipline.
- **What to do next:** Run the batched exact scanner across the 24 planned
  systems, merge the case ledgers, and only then interpret whether this
  upstream B47 basin is constructive or another local route cut.

### 2026-07-02 - M1 a327 upstream B47 robust skeleton search

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_upstream_b47_robust_skeleton_search.md`,
  `experimental/scripts/scan_m1_a327_upstream_b47_robust_skeleton_search.py`,
  `experimental/scripts/verify_m1_a327_upstream_b47_robust_skeleton_search.py`,
  `experimental/scripts/audit_m1_a327_upstream_b47_robust_skeleton_search.sage`,
  `experimental/data/m1_a327_upstream_b47_robust_skeleton_search.json`,
  `experimental/agents-log.md`.
- **Status:** PARTIAL / EXPERIMENTAL.
- **What is being added:** An upstream B47-robust skeleton ledger seeded from
  the banked local basin route cut and existing exact lineage data. The ledger
  records candidate skeletons, split-probe outcomes, and split-aware guard
  margins without claiming a new exact construction.
- **How it is useful:** Moves the a=327 search away from the exhausted
  `[1,4,5,7]` compensated split basin and sets the objective for a new
  exact scanner: find repaired skeletons whose B47 and capacity guards survive
  split probes.
- **What to do next:** Implement the exact upstream scanner over
  B47-robust buffer and alternate residual-collapse families, then run bounded
  split probes before attempting exact nondegenerate extraction.

### 2026-07-02 - M1 a327 local basin conservation note

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_local_basin_conservation_note.md`,
  `experimental/data/m1_a327_local_basin_conservation_note.json`,
  `experimental/scripts/verify_m1_a327_local_basin_conservation_note.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / ROUTE_CUT_LOCAL_BASIN / EXPERIMENTAL.
- **What is being added:** A narrow audit note for the full compensated
  repaired-skeleton split v2 grid. The 45 tested systems produced 30 exact
  vectors and 15 inconsistent systems, with zero capacity-preserving or
  pair-guard-preserving vectors.
- **How it is useful:** Banks the repaired-skeleton split/replacement basin as
  a local route cut while explicitly avoiding any global `a=327`, MCA,
  protocol, or `Lambda_mu(C,327) <= 6` claim.
- **What to do next:** Move upstream to a B47-robust repaired-skeleton search
  or another nonlocal target-system redesign rather than rerunning the same
  compensated split v2 family.

### 2026-07-01 - M1 a327 compensated repaired-skeleton split v2 batched runner

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_compensated_repaired_skeleton_split_v2_batched.md`,
  `experimental/scripts/run_m1_a327_compensated_repaired_skeleton_split_v2_batch.py`,
  `experimental/scripts/merge_m1_a327_compensated_repaired_skeleton_split_v2_results.py`,
  `experimental/scripts/audit_m1_a327_compensated_repaired_skeleton_split_v2.sage`,
  `experimental/scripts/verify_m1_a327_compensated_repaired_skeleton_split_v2.py`,
  `experimental/agents-log.md`.
- **Status:** EXACT_INFRASTRUCTURE / PARTIAL / EXPERIMENTAL.
- **What is being added:** A one-case-per-process batch runner and merge layer
  for the cached v2 compensated split grid, plus Sage `--case-index`,
  `--case-range`, and `--list-cases` support. Cases are ordered to test B47
  repair first.
- **How it is useful:** Avoids losing progress to a single slow `GF(17^32)`
  residual solve and makes the 45-system v2 grid resumable under external
  per-case timeouts.
- **What to do next:** Run prioritized batches, merge the per-case ledgers,
  verify the aggregate JSON, and only then decide whether the repaired-skeleton
  basin has a local conservation obstruction.

### 2026-07-01 - M1 a327 compensated split v2 priority batch

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json`,
  `experimental/data/m1_a327_compensated_repaired_skeleton_split_v2_cases/case_0000.json`
  through `case_0007.json`,
  `experimental/notes/m1/m1_a327_compensated_repaired_skeleton_split_v2_batched.md`,
  `experimental/scripts/audit_m1_a327_compensated_repaired_skeleton_split_v2.sage`,
  `experimental/scripts/merge_m1_a327_compensated_repaired_skeleton_split_v2_results.py`,
  `experimental/agents-log.md`.
- **Status:** PARTIAL / EXACT_EXTRACTION_NO_A327-FRONT / EXPERIMENTAL.
- **What is being added:** Results for the first eight B47-priority
  compensated split cases. The batch completed with no timeouts, 6 exact
  vectors, 2 inconsistent cases, and no capacity-preserving or
  pair-guard-preserving vector.
- **How it is useful:** Confirms that the prioritized B47 repair front does not
  restore the repaired-skeleton capacity guard in the tested cases, while the
  full 45-case grid remains incomplete.
- **What to do next:** Run cases `8:45` before writing any local conservation
  note.

### 2026-07-01 - M1 a327 compensated repaired-skeleton split v2

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_compensated_repaired_skeleton_split_v2.md`,
  `experimental/scripts/scan_m1_a327_compensated_repaired_skeleton_split_v2.py`,
  `experimental/scripts/verify_m1_a327_compensated_repaired_skeleton_split_v2.py`,
  `experimental/scripts/audit_m1_a327_compensated_repaired_skeleton_split_v2.sage`,
  `experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json`,
  `experimental/agents-log.md`.
- **Status:** PROOF_RECORD | CANDIDATE | EXACT_EXTRACTION_NO_A327 | PARTIAL /
  EXPERIMENTAL.
- **What is being added:** A cached exact rerun scaffold for the compensated
  repaired-skeleton split grid, using the Sage-native budget-32 skeleton cache
  from `c181b13` instead of rebuilding the `GF(17^32)` repaired context in the
  hot path. The current ledger is partial: 1 of 45 planned cases has completed
  with one exact vector and failure `COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED`.
- **How it is useful:** Tests whether replacement rows can compensate the
  known split damage to capacity, `B({2,7})`, `B({3,7})`, and especially
  `B({4,7})`, while preserving the interleaved-list track discipline.
- **What to do next:** Continue or optimize the resumable Sage audit. If the
  full cached grid produces no exact candidate, decide whether the basin earns
  a local conservation note.

### 2026-07-01 - M1 a327 repaired-skeleton Sage-native cache

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_repaired_skeleton_sage_native_cache.md`,
  `experimental/scripts/scan_m1_a327_repaired_skeleton_sage_native_cache.py`,
  `experimental/scripts/verify_m1_a327_repaired_skeleton_sage_native_cache.py`,
  `experimental/scripts/audit_m1_a327_repaired_skeleton_sage_native_cache.sage`,
  `experimental/data/m1_a327_repaired_skeleton_sage_native_cache.json`,
  `experimental/data/cache/m1_a327_repaired_skeleton_budget32_prepared_state.sobj`,
  `experimental/agents-log.md`.
- **Status:** EXACT_STATE_CACHE / EXPERIMENTAL.
- **What is being added:** A Sage-native prepared linear-algebra cache for the
  budget-32 repaired skeleton, including the independent matrix, RHS, pivot
  columns, free columns, pivot matrix, pivot inverse, base vector, and fixed
  specs.
- **How it is useful:** The cache avoids the `repaired_context()` timeout path
  from `1a75dfe`: the small append test now returns
  `CACHE_SMALL_APPEND_PASS` and constructs an exact vector. The append vector
  has capacity `260`, pair values `[1024,657,656,512,1024]`, and collapse
  `[[1,5,7],[4,6],[3],[2]]`, so it is only an infrastructure success, not an
  `a=327` candidate.
- **What to do next:** Rerun the compensated repaired-skeleton split grid using
  this cache, targeting simultaneous restoration of capacity plus
  `B({2,7})`, `B({3,7})`, and `B({4,7})`.

### 2026-07-01 - M1 a327 repaired-skeleton prepared matrix cache

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_repaired_skeleton_prepared_matrix_cache.md`,
  `experimental/scripts/scan_m1_a327_repaired_skeleton_prepared_matrix_cache.py`,
  `experimental/scripts/verify_m1_a327_repaired_skeleton_prepared_matrix_cache.py`,
  `experimental/scripts/audit_m1_a327_repaired_skeleton_prepared_matrix_cache.sage`,
  `experimental/data/m1_a327_repaired_skeleton_prepared_matrix_cache.json`,
  `experimental/agents-log.md`.
- **Status:** PARTIAL / EXACT_INFRASTRUCTURE_LIMIT / EXPERIMENTAL.
- **What is being added:** A prepared-state cache manifest for the budget-32
  repaired skeleton, recording the available `GF(17^32)` linear-algebra
  metadata: matrix shape `[354,1536]`, rank `354`, nullity `1182`, fixed specs
  count `129`, and the `d2_first_free` pattern.
- **How it is useful:** The manifest confirms the parent exact replay passes
  and that the current cache type is only `RECONSTRUCTION_ONLY`; pivot columns,
  free columns, independent row indices, and a Sage-native prepared matrix are
  not persisted. This explains why the `1a75dfe` compensated grid still timed
  out before constructing exact vectors.
- **What to do next:** Build a stronger Sage-native cache or pivot/free-column
  artifact for the budget-32 skeleton before rerunning compensated
  split/replacement. Do not treat this as evidence that compensated splitting
  fails mathematically.

### 2026-07-01 - M1 a327 compensated repaired-skeleton split

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_compensated_repaired_skeleton_split.md`,
  `experimental/scripts/scan_m1_a327_compensated_repaired_skeleton_split.py`,
  `experimental/scripts/verify_m1_a327_compensated_repaired_skeleton_split.py`,
  `experimental/scripts/audit_m1_a327_compensated_repaired_skeleton_split.sage`,
  `experimental/data/m1_a327_compensated_repaired_skeleton_split.json`,
  `experimental/agents-log.md`.
- **Status:** PARTIAL / EXACT_SETUP_TIMEOUT / EXPERIMENTAL.
- **What is being added:** A damage-aware compensated split selector for the
  budget-32 repaired skeleton, using the `30d0cdb` persistent coordinate
  ledger to plan split/replacement bundles that target capacity plus
  `B({2,7})`, `B({3,7})`, and `B({4,7})` repair.
- **How it is useful:** The branch makes the failed split damage explicit:
  capacity drops `333 -> 315`, `B({2,7})/B({3,7})` drop `657/656 -> 593/592`,
  and `B({4,7})` drops `1024 -> 512`. A first exact attempt remained inside
  `GF(17^32)` skeleton reconstruction before constructing any compensated
  vector, showing that the current exact-state cache is not yet strong enough
  for the intended 45-system compensated grid.
- **What to do next:** Persist a stronger Sage-native prepared state for the
  budget-32 skeleton, such as reusable rows/pivots/free columns or a
  matrix/vector cache, then rerun the same compensated split grid. Do not treat
  this as evidence that compensated split/replacement fails mathematically.

### 2026-07-01 - M1 a327 repaired-skeleton persistent exact state

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_repaired_skeleton_persistent_exact_state.md`,
  `experimental/scripts/scan_m1_a327_repaired_skeleton_persistent_exact_state.py`,
  `experimental/scripts/verify_m1_a327_repaired_skeleton_persistent_exact_state.py`,
  `experimental/scripts/audit_m1_a327_repaired_skeleton_persistent_exact_state.sage`,
  `experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_STATE_REPLAY / PARTIAL / EXPERIMENTAL.
- **What is being added:** A deterministic replay/cache for the budget-32
  repaired skeleton from `2dfd1d9` and the `split_4_from_157` failure from
  `7a02b97`, including exact hashes and a 512-coordinate damage/replacement
  ledger.
- **How it is useful:** The replay confirms the source skeleton at capacity
  `333` with pair values `[1024,657,656,1024,1024]`, and the failed split at
  capacity `315` with pair values `[1024,593,592,512,1024]`. The cached
  coordinate ledger makes later compensated split/replacement searches
  reproducible without treating this branch as a proof record.
- **What to do next:** Use this exact-state cache for a compensated
  repaired-skeleton split search targeting capacity plus `B27/B37/B47`
  restoration, while keeping the row strictly on the interleaved-list track.

### 2026-07-01 - M1 a327 repaired-skeleton nondegenerate split

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_repaired_skeleton_nondegenerate_split.md`,
  `experimental/scripts/scan_m1_a327_repaired_skeleton_nondegenerate_split.py`,
  `experimental/scripts/verify_m1_a327_repaired_skeleton_nondegenerate_split.py`,
  `experimental/scripts/audit_m1_a327_repaired_skeleton_nondegenerate_split.sage`,
  `experimental/data/m1_a327_repaired_skeleton_nondegenerate_split.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A guarded exact `GF(17^32)` split audit starting
  from the budget-32 repaired skeleton with capacity `333`,
  `B({2,7})/B({3,7}) = 657/656`, `B({5,7}) = 1024`, and residual collapse
  `[[1,4,5,7],[6],[3],[2]]`.
- **How it is useful:** The first retained `split_4_from_157` row reduces the
  residual class to `[[1,5,6,7],[4],[3],[2]]`, but capacity drops to `315`
  and pair values fall to `[1024,593,592,512,1024]`. The ledger records all
  `512` coordinates as capacity-critical and pair57-critical in this repaired
  skeleton.
- **What to do next:** Do not treat blind split pins as candidates. Either
  develop a compensated/non-dense split solver that preserves the repaired
  pair guards, or bank this as evidence for a local conservation obstruction
  around the `[1,4,5,7]` residual class.

### 2026-07-01 - M1 a327 post-split pair27/37 microrepair stage 2

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_postsplit_pair27_37_microrepair_stage2.md`,
  `experimental/scripts/scan_m1_a327_postsplit_pair27_37_microrepair_stage2.py`,
  `experimental/scripts/verify_m1_a327_postsplit_pair27_37_microrepair_stage2.py`,
  `experimental/scripts/audit_m1_a327_postsplit_pair27_37_microrepair_stage2.sage`,
  `experimental/data/m1_a327_postsplit_pair27_37_microrepair_stage2.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A stage-2 exact `GF(17^32)` microrepair ladder
  that continues the successful `triple_237` direction from the budget-8
  post-split incumbent through total budgets `12,16,24,32`.
- **How it is useful:** The total-budget-32 case clears the local pair Hall
  targets with capacity `333`, `B({2,7})/B({3,7}) = 657/656`,
  `B({5,7}) = 1024`, pair Hall bound `328`, and six-class dominance `0`.
  It is still not an exact witness because the tuple remains degenerate with
  classes `[[1,4,5,7],[6],[3],[2]]`.
- **What to do next:** Work inside the repaired post-split skeleton on
  nondegeneracy/rescheduling, especially splitting the residual
  `[1,4,5,7]` class without losing the newly repaired pair Hall and capacity
  guards.

### 2026-07-01 - M1 a327 post-split pair27/37 microrepair

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_postsplit_pair27_37_microrepair.md`,
  `experimental/scripts/scan_m1_a327_postsplit_pair27_37_microrepair.py`,
  `experimental/scripts/verify_m1_a327_postsplit_pair27_37_microrepair.py`,
  `experimental/scripts/audit_m1_a327_postsplit_pair27_37_microrepair.sage`,
  `experimental/data/m1_a327_postsplit_pair27_37_microrepair.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` post-split
  microrepair audit starting from the `6c54e44` capacity-preserving
  co-design geometry and testing a matched `triple_237` budget-8 repair.
- **How it is useful:** The checked repair preserves capacity and collapse,
  improving post-split capacity `329 -> 330` and
  `B({2,7})/B({3,7})` from `641/640` to `645/644`, but remains short of
  the `654/654` pair target and produces no exact `a>=327` witness.
- **What to do next:** Either broaden the same microrepair family carefully
  beyond budget 8 or test a nullspace-sampled variant; avoid returning to
  broad capacity buffering until the remaining `9/10` pair-credit gap is
  understood.

### 2026-07-01 - M1 a327 reserve-pairclass co-design before split

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_reserve_pairclass_codesign_before_split.md`,
  `experimental/scripts/scan_m1_a327_reserve_pairclass_codesign_before_split.py`,
  `experimental/scripts/verify_m1_a327_reserve_pairclass_codesign_before_split.py`,
  `experimental/scripts/audit_m1_a327_reserve_pairclass_codesign_before_split.sage`,
  `experimental/data/m1_a327_reserve_pairclass_codesign_before_split.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A split-aware exact `GF(17^32)` co-design audit
  that chooses pre-split pairclass/reserve rows by predicted post-split
  survival rather than raw pre-split capacity alone.
- **How it is useful:** The best completed case clears post-split capacity
  with capacity `329`, preserves `{5,7}`, reduces collapse, and improves
  post-split `B({2,7})/B({3,7})` to `641/640`; the remaining deficit is
  `13/14` pair credits, with no exact `a>=327` witness.
- **What to do next:** Start from the 96-row quotient-fiber buffer geometry
  and add a small B27/B37-only repair layer while preserving capacity `>=327`
  and `B({5,7})>=654`.

### 2026-07-01 - M1 a327 high-buffer pairclass before split

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_high_buffer_pairclass_before_split.md`,
  `experimental/scripts/scan_m1_a327_high_buffer_pairclass_before_split.py`,
  `experimental/scripts/verify_m1_a327_high_buffer_pairclass_before_split.py`,
  `experimental/scripts/audit_m1_a327_high_buffer_pairclass_before_split.sage`,
  `experimental/data/m1_a327_high_buffer_pairclass_before_split.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A 20-system bounded exact `GF(17^32)`
  high-buffer pairclass audit that tries to create capacity reserve before
  applying the known collapse-reducing split.
- **How it is useful:** The best completed case improves post-split
  `B({2,7})/B({3,7})` to `608/608` and capacity to `322`, but no case reaches
  the pre-split buffer target `420` or post-split capacity `327`; 9 larger
  cases time out.
- **What to do next:** Either test a more aggressive upstream capacity-reserve
  construction or write a compact local-basin conservation note explaining why
  the extension-96 buffer schedule remains short of the split threshold.

### 2026-07-01 - M1 a327 compensated split-and-replace

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_compensated_split_replace.md`,
  `experimental/scripts/scan_m1_a327_compensated_split_replace.py`,
  `experimental/scripts/verify_m1_a327_compensated_split_replace.py`,
  `experimental/scripts/audit_m1_a327_compensated_split_replace.sage`,
  `experimental/data/m1_a327_compensated_split_replace.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A 30-system exact `GF(17^32)` compensated
  split-and-replace audit that pairs collapse-reducing split rows with one or
  two capacity-replacement rows.
- **How it is useful:** All 30 constructed vectors preserve `{5,7}`, preserve
  the `B({2,7})/B({3,7})` gain at `593/592`, and reduce collapse, but zero
  vectors restore capacity above `315`.
- **What to do next:** Stop small local surgery in this basin. Either test
  larger compensated exchanges explicitly or redesign the upstream pair-class
  target system so it has capacity slack above `400` before the split.

### 2026-07-01 - M1 a327 capacity-slack split selector

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_capacity_slack_split_selector.md`,
  `experimental/scripts/scan_m1_a327_capacity_slack_split_selector.py`,
  `experimental/scripts/verify_m1_a327_capacity_slack_split_selector.py`,
  `experimental/scripts/audit_m1_a327_capacity_slack_split_selector.sage`,
  `experimental/data/m1_a327_capacity_slack_split_selector.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** An exact `GF(17^32)` coordinate-level capacity
  ledger and slack-ranked split selector for the scalable pair-class
  extension-96 basin.
- **How it is useful:** The ledger shows all 512 coordinates are both
  capacity-critical and `{5,7}`-critical; all retained locally safe split rows
  have score `0`. The selector constructs 36 exact vectors, all preserving
  `{5,7}` and reducing collapse, but none preserve capacity above `315`.
- **What to do next:** Stop using single-coordinate split placement in this
  basin; either add compensated capacity rows with the split or redesign the
  target system so pair-class creation does not make every coordinate
  capacity-critical before splitting.

### 2026-07-01 - M1 a327 capacity-skeleton protected split placement

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_capacity_skeleton_protected_split_placement.md`,
  `experimental/scripts/scan_m1_a327_capacity_skeleton_protected_split_placement.py`,
  `experimental/scripts/verify_m1_a327_capacity_skeleton_protected_split_placement.py`,
  `experimental/scripts/audit_m1_a327_capacity_skeleton_protected_split_placement.sage`,
  `experimental/data/m1_a327_capacity_skeleton_protected_split_placement.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A timeout-bounded exact `GF(17^32)` audit of
  split placements designed to preserve the capacity skeleton, especially
  `{5,7}`, while continuing the scalable `{2,7}` / `{3,7}` pair-class repair.
- **How it is useful:** The audit separates two failure modes: 27 vectors
  preserve `{5,7}` and reduce collapse, but all 45 sampled vectors still fall
  below capacity `327`; the best row keeps pair values
  `[1024,593,592,1024,1024]` but has capacity `315`.
- **What to do next:** Build a coordinate-level capacity ledger and choose
  split placements from actual slack, rather than fixed split families.

### 2026-07-01 - M1 a327 scalable pairclass with 14567 split

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_scalable_pairclass_with_14567_split.md`,
  `experimental/scripts/scan_m1_a327_scalable_pairclass_with_14567_split.py`,
  `experimental/scripts/verify_m1_a327_scalable_pairclass_with_14567_split.py`,
  `experimental/scripts/audit_m1_a327_scalable_pairclass_with_14567_split.sage`,
  `experimental/data/m1_a327_scalable_pairclass_with_14567_split.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A timeout-bounded exact `GF(17^32)` audit that
  combines scalable `{2,7}` / `{3,7}` pair-class creation with controlled
  evaluation split constraints for the persistent `[1,4,5,6,7]` class.
- **How it is useful:** The audit shows both mechanisms work separately in the
  same exact systems: pair values grow to `[1024,593,592,1024,514]`, and all
  36 sampled vectors reduce the `[1,4,5,6,7]` collapse. The obstruction is
  now capacity: zero vectors remain capacity-preserving, with best capacity
  `315`.
- **What to do next:** Choose split coordinates from a capacity-critical
  ledger for the scalable pairclass geometry rather than using generic split
  families; the next goal is split placement that preserves capacity
  `>=327`.

### 2026-06-30 - M1 a327 pair27/37 class creation scalable solve

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_pair27_37_class_creation_scalable.md`,
  `experimental/scripts/scan_m1_a327_pair27_37_class_creation_scalable.py`,
  `experimental/scripts/verify_m1_a327_pair27_37_class_creation_scalable.py`,
  `experimental/scripts/audit_m1_a327_pair27_37_class_creation_scalable.sage`,
  `experimental/data/m1_a327_pair27_37_class_creation_scalable.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A timeout-bounded exact `GF(17^32)` scalable
  class-creation audit that extends the successful size-32 `{2,7}` / `{3,7}`
  class-creation system with structured row blocks for target sizes 64 and 96.
- **How it is useful:** The scalable pass shows the pair-class creation
  mechanism continues to move the exact Hall values in the right direction:
  best pair values improve to `[1024,577,576,1024,1024]` with capacity `384`,
  `D2` split retained, and no timeouts.
- **What to do next:** Couple larger pair-class creation blocks with
  nondegeneracy constraints for the persistent `[1,4,5,6,7]` class; all
  scalable vectors remain degenerate and still fall short of the `654` pair
  target.

### 2026-06-30 - M1 a327 pair27/37 class creation

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_pair27_37_class_creation.md`,
  `experimental/scripts/scan_m1_a327_pair27_37_class_creation.py`,
  `experimental/scripts/verify_m1_a327_pair27_37_class_creation.py`,
  `experimental/scripts/audit_m1_a327_pair27_37_class_creation.sage`,
  `experimental/data/m1_a327_pair27_37_class_creation.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` class-creation probe
  that adds structured first-class target rows for `P_2=P_7` and `P_3=P_7`
  on quotient-fiber coordinate sets of size 32.
- **How it is useful:** The probe raises the weak pair values from
  `B({2,7})=514`, `B({3,7})=513` to `545` and `544` while retaining `D2`
  split and capacity `375`, but it remains a partial repair and all exact
  vectors are still degenerate.
- **What to do next:** Continue class creation with larger structured
  `T_27/T_37` sets and better exact linear-algebra strategy; the size-64+
  systems were left open because dense `GF(17^32)` echelonization was too slow
  for this checkpoint.

### 2026-06-30 - M1 a327 pair27/37 exchange obstruction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_pair27_37_exchange_obstruction.md`,
  `experimental/scripts/scan_m1_a327_pair27_37_exchange_obstruction.py`,
  `experimental/scripts/verify_m1_a327_pair27_37_exchange_obstruction.py`,
  `experimental/scripts/audit_m1_a327_pair27_37_exchange_obstruction.sage`,
  `experimental/data/m1_a327_pair27_37_exchange_obstruction.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** An exact `GF(17^32)` Hall/exchange diagnostic for
  the weak pair subsets `{2,7}` and `{3,7}` inside the stable low-collapse
  post-`D2` split geometry.
- **How it is useful:** The audit analyzes all 78 exact vectors from the
  prior checkpoint and shows the exchange graph is infeasible: `{2,7}` shares
  a value at only 2 coordinates, and `{3,7}` at only 1 coordinate, far below
  the `B>=654` pair target.
- **What to do next:** Stop trying to exchange among existing value classes in
  this tuple. Search for exact perturbations that create new `{2,7}` and
  `{3,7}` pair-credit coordinates while preserving the `D2` split and
  capacity.

### 2026-06-30 - M1 a327 post-D2-split pair-7 repair

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_post_d2split_pair7_repair.md`,
  `experimental/scripts/scan_m1_a327_post_d2split_pair7_repair.py`,
  `experimental/scripts/verify_m1_a327_post_d2split_pair7_repair.py`,
  `experimental/scripts/audit_m1_a327_post_d2split_pair7_repair.sage`,
  `experimental/data/m1_a327_post_d2split_pair7_repair.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` pair-repair audit
  after the capacity-preserving `D_2` split checkpoint. It adds local
  homogeneous `P_2=P_7`, `P_3=P_7`, and `P_2=P_3=P_7` repair rows to the
  stable low-collapse split regime.
- **How it is useful:** All 78 constructed exact vectors retain `D_2` split,
  capacity, and low six-class dominance, but none repair the weak pair values.
  The best remains at pair values `[1024,514,513,1024,1024]`.
- **What to do next:** Replace local homogeneous repair pins with
  pair-Hall-guided exact nullspace sampling inside the stable low-collapse
  capacity-preserving `D_2` split regime.

### 2026-06-30 - M1 a327 capacity-preserving residual [1,2] split

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_capacity_preserving_residual12_split.md`,
  `experimental/scripts/scan_m1_a327_capacity_preserving_residual12_split.py`,
  `experimental/scripts/verify_m1_a327_capacity_preserving_residual12_split.py`,
  `experimental/scripts/audit_m1_a327_capacity_preserving_residual12_split.sage`,
  `experimental/data/m1_a327_capacity_preserving_residual12_split.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` audit that splits
  residual `[1,2]` earlier, before the destructive `anchor_split_34567`
  layer, while preserving the protected-exchange row schedule.
- **How it is useful:** Unlike the prior hard residual split, this search
  finds 48 capacity-preserving `D_2` split vectors, including 24 low-collapse
  capacity-preserving splits. None preserve pair-7 repair; the best capacity
  split returns six-class dominance, while the best low-collapse split leaves
  weak pair values near `512`.
- **What to do next:** Search inside the low-collapse capacity-preserving
  `D_2` split regime for pair-7 repair, especially improving `B({2,7})` and
  `B({3,7})`, without rebuilding the six-class collapse.

### 2026-06-30 - M1 a327 residual [1,2] split pinned nullspace

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_residual_12_split_pinned_nullspace.md`,
  `experimental/scripts/scan_m1_a327_residual_12_split_pinned_nullspace.py`,
  `experimental/scripts/verify_m1_a327_residual_12_split_pinned_nullspace.py`,
  `experimental/scripts/audit_m1_a327_residual_12_split_pinned_nullspace.sage`,
  `experimental/data/m1_a327_residual_12_split_pinned_nullspace.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` residual `[1,2]`
  split and pinned-nullspace audit following `024481e`. It starts from the
  strongest prior split, adds residual `P_2(h)=gamma` pins, and samples
  deterministic `D_2` free-column assignments.
- **How it is useful:** The audit shows the residual `[1,2]` collapse can be
  split exactly, but every tested nondegenerate vector loses capacity. Across
  40 constructed exact vectors, 38 are nondegenerate, zero are
  capacity-preserving, and the best capacity upper bound is `83`.
- **What to do next:** Avoid hard residual pins after the destructive
  `anchor_split_34567` layer. Try a gentler capacity-preserving residual split
  earlier in the partial-split hierarchy or search for `D_2` perturbations
  that preserve protected-exchange pair repair.

### 2026-06-30 - M1 a327 protected-exchange nondegenerate lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_protected_exchange_nondegenerate_lift.md`,
  `experimental/scripts/scan_m1_a327_protected_exchange_nondegenerate_lift.py`,
  `experimental/scripts/verify_m1_a327_protected_exchange_nondegenerate_lift.py`,
  `experimental/scripts/audit_m1_a327_protected_exchange_nondegenerate_lift.sage`,
  `experimental/data/m1_a327_protected_exchange_nondegenerate_lift.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` pinned-lift audit inside
  the protected-exchange row schedule. It tests affine evaluation separation
  pins intended to break the degenerate exact lifts from `a2d31ee`.
- **How it is useful:** The pins split portions of the collapse class but no
  tested pin set produces seven distinct codewords. The best high-capacity
  split has capacity `438` and pair values `[1024,1024,512,1024,1024]`; the
  strongest split leaves only `[1,2]` collapsed but loses capacity.
- **What to do next:** Target the residual `[1,2]` collapse directly, or use
  exact nullspace sampling with nondegeneracy constraints rather than a single
  affine pivot solution.

### 2026-06-30 - M1 a327 protected-exchange exact audit

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_protected_exchange_exact_audit.md`,
  `experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py`,
  `experimental/scripts/verify_m1_a327_protected_exchange_exact_audit.py`,
  `experimental/scripts/audit_m1_a327_protected_exchange_exact_audit.sage`,
  `experimental/data/m1_a327_protected_exchange_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_AUDIT_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` audit of the two
  protected-exchange proxy candidates from `c9f2e4c`, including exact row
  schedule rank checks and proxy-guided exact vector construction.
- **How it is useful:** The audit confirms the tested exact row schedules are
  full row rank but finds no exact `a>=327` witness. All 26 constructed exact
  vectors are degenerate; the best reaches exact max-min `287` with capacity
  `447` and pair values `[575,575,575,575,575]`.
- **What to do next:** Try nondegeneracy-constrained exact lifting inside the
  protected-exchange row schedule before returning to proxy search.

### 2026-06-30 - M1 a327 witness-7 pair protected local exchange

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_witness7_pair_protected_local_exchange.md`,
  `experimental/scripts/scan_m1_a327_witness7_pair_protected_local_exchange.py`,
  `experimental/scripts/verify_m1_a327_witness7_pair_protected_local_exchange.py`,
  `experimental/scripts/audit_m1_a327_witness7_pair_protected_local_exchange.sage`,
  `experimental/data/m1_a327_witness7_pair_protected_local_exchange.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / SAGE_PENDING / PARTIAL / EXPERIMENTAL.
- **What is being added:** A protected local exchange scan around the best
  stage-1 witness-7 pair Hall repair target system. It preserves the existing
  pair repair rows and mutates only the unprotected skeleton complement.
- **How it is useful:** The scan finds two proxy `a>=327` candidates. The best
  reaches proxy max-min `335`, pair values `[671,671,671,671,671]`, capacity
  `461`, and zero added six-class dominance.
- **What to do next:** Run exact `GF(17^32)` extraction/audit for the
  protected-exchange proxy candidates. Do not treat the proxy hit as a public
  row or MCA/protocol evidence.

### 2026-06-30 - M1 a327 witness-7 pair Hall repair stage 2

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_witness7_pair_hall_repair_stage2.md`,
  `experimental/scripts/scan_m1_a327_witness7_pair_hall_repair_stage2.py`,
  `experimental/scripts/verify_m1_a327_witness7_pair_hall_repair_stage2.py`,
  `experimental/scripts/audit_m1_a327_witness7_pair_hall_repair_stage2.sage`,
  `experimental/data/m1_a327_witness7_pair_hall_repair_stage2.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_PAIR7_STAGE2_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A second-stage witness-7 pair Hall repair scan
  around the top first-stage `315` geometries from `8669680`. The bounded run
  tests 108 target systems and 1728 proxy samples.
- **How it is useful:** The scan is a negative local checkpoint: it finds no
  proxy `a>=327` candidate and does not improve the first-stage incumbent.
  Best retained values are proxy max-min `314`, capacity `455`, pair values
  `[628,628,628,628,628]`, and zero added six-class dominance.
- **What to do next:** Preserve the first-stage pair-repair rows as protected
  skeleton rows and try local additive/exchange mutations rather than
  reconstructing a second-stage target system from scratch.

### 2026-06-30 - M1 a327 witness-7 pair Hall repair

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_witness7_pair_hall_repair.md`,
  `experimental/scripts/scan_m1_a327_witness7_pair_hall_repair.py`,
  `experimental/scripts/verify_m1_a327_witness7_pair_hall_repair.py`,
  `experimental/scripts/audit_m1_a327_witness7_pair_hall_repair.sage`,
  `experimental/data/m1_a327_witness7_pair_hall_repair.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_PAIR7_REPAIR_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A surgical witness-7 pair Hall repair scan on top
  of the repaired tangent-skeleton geometries from `d1fd9d0`. The first pass
  tests 125 target systems and 2000 proxy samples.
- **How it is useful:** The scan improves the current bottleneck without
  adding collapse: proxy max-min rises from 308 to 315, pair values rise from
  616 to 631, and added six-class dominance remains 0. It still misses the
  `B({i,7})>=654` pair target by 23 credits.
- **What to do next:** Run a second-stage pair repair around the best 315
  geometry or increase repair budgets while keeping the repaired skeleton and
  zero-added-collapse constraint.

### 2026-06-30 - M1 a327 tangent-skeleton Hall repair

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_tangent_skeleton_hall_repair.md`,
  `experimental/scripts/scan_m1_a327_tangent_skeleton_hall_repair.py`,
  `experimental/scripts/verify_m1_a327_tangent_skeleton_hall_repair.py`,
  `experimental/scripts/audit_m1_a327_tangent_skeleton_hall_repair.sage`,
  `experimental/data/m1_a327_tangent_skeleton_hall_repair.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_TANGENT_HALL_REPAIR_NO_A327 / PARTIAL /
  EXPERIMENTAL.
- **What is being added:** A localized Hall-repair scan inside retained
  low-collapse tangent value-class skeletons. The first pass tests 80 target
  systems and 1280 proxy samples; no proxy `a>=327` candidate is found.
- **How it is useful:** Unlike hard global Hall repair, this branch improves
  the low-collapse tangent proxy max-min from 260 to 308 with capacity 453 and
  zero added six-class dominance. The original three-witness Hall subsets are
  over-repaired, exposing a new pair bottleneck involving witness 7.
- **What to do next:** Target the new tight pair family `{i,7}` inside the
  repaired tangent skeleton; the remaining pair deficit is 38 credits rather
  than the previous 200-credit three-witness deficit.

### 2026-06-30 - M1 a327 collapse-constrained Hall repair

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_collapse_constrained_hall_repair.md`,
  `experimental/scripts/scan_m1_a327_collapse_constrained_hall_repair.py`,
  `experimental/scripts/verify_m1_a327_collapse_constrained_hall_repair.py`,
  `experimental/scripts/audit_m1_a327_collapse_constrained_hall_repair.sage`,
  `experimental/data/m1_a327_collapse_constrained_hall_repair.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_CONSTRAINED_HALL_REPAIR_NO_A327 / PARTIAL /
  EXPERIMENTAL.
- **What is being added:** A hard dominance-cap Hall repair sweep following
  `4d5ce7f`. The scan tests 128 target systems and 2048 proxy tuple samples
  across dominance caps `350..25`, with no acceptable proxy `a>=327`
  candidate.
- **How it is useful:** Measures the Hall-repair/collapse tradeoff directly:
  cap-satisfying samples remove six-class dominance but collapse to capacity
  165, while the strongest rejected repair reaches proxy max-min 334 only by
  returning to six-class dominance 356.
- **What to do next:** Search for Hall repair inside the existing
  low-collapse tangent skeleton, rather than allowing generic Hall rows to
  rebuild the collapse basin or forcing all collapse rows out at once.

### 2026-06-30 - M1 a327 Hall-guided target mutation

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_hall_guided_target_mutation.md`,
  `experimental/scripts/scan_m1_a327_hall_guided_target_mutation.py`,
  `experimental/scripts/verify_m1_a327_hall_guided_target_mutation.py`,
  `experimental/scripts/audit_m1_a327_hall_guided_target_mutation.sage`,
  `experimental/data/m1_a327_hall_guided_target_mutation.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_HALL_MUTATIONS_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A Hall-guided target mutation scan using the tight
  three-witness subsets from `ed4cf43` as first-class target-selection
  objectives. The first bounded pass tests 16 target systems and 256 proxy
  codeword tuples; no acceptable proxy `a>=327` candidate is found.
- **How it is useful:** The best raw sample repairs the Hall obstruction
  strongly, raising the Hall bound to 332 with tight-subset values
  `[1177,1177,1177]`, but it does so by returning to high six-class dominance
  359. This separates "Hall repair works" from "Hall repair currently returns
  the collapse basin."
- **What to do next:** Try collapse-constrained Hall repair: increase
  `B(U)` for the tight subsets while explicitly capping six-class dominance or
  preserving the low-collapse tangent skeleton.

### 2026-06-30 - M1 a327 rescheduler dual Hall obstruction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_rescheduler_dual_hall_obstruction.md`,
  `experimental/scripts/scan_m1_a327_rescheduler_dual_hall_obstruction.py`,
  `experimental/scripts/verify_m1_a327_rescheduler_dual_hall_obstruction.py`,
  `experimental/data/m1_a327_rescheduler_dual_hall_obstruction.json`,
  `experimental/agents-log.md`.
- **Status:** RESCHEDULER_OBSTRUCTION_CERTIFICATE / PARTIAL / EXPERIMENTAL.
- **What is being added:** A Hall-style subset-credit audit for the
  rescheduler bottleneck in the recent line/plane/tangent proxy tuples. The
  scanner replays 86 retained samples, deduplicates them to 30 value-class
  geometries, and finds 11 Hall-tight high-capacity samples.
- **How it is useful:** Explains the current best tangent tuple exactly:
  capacity upper bound 404 and low collapse are not enough because a
  three-witness Hall subset has `B(U)=781`, giving Hall bound 260 and matching
  the exact proxy rescheduler optimum.
- **What to do next:** Use the tight Hall subsets to drive target mutation or
  tangent-direction selection; specifically, increase `B(U)` for the tight
  three-witness subsets rather than optimizing global capacity alone.

### 2026-06-30 - M1 a327 collision-tangent quotient-plane search

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_collision_tangent_quotient_plane_search.md`,
  `experimental/scripts/scan_m1_a327_collision_tangent_quotient_plane_search.py`,
  `experimental/scripts/verify_m1_a327_collision_tangent_quotient_plane_search.py`,
  `experimental/scripts/audit_m1_a327_collision_tangent_quotient_plane_search.sage`,
  `experimental/data/m1_a327_collision_tangent_quotient_plane_search.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_TANGENT_PLANES_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A collision-tangent quotient-plane proxy search
  that constrains second directions to preserve protected dominant value
  classes from the best quotient lines. The first pass builds 20 tangent
  spaces, tests 320 directions and 10,240 `mu` values, and finds no proxy
  `a>=327` candidate.
- **How it is useful:** Shows that tangent directions fix the immediate
  capacity-loss failure from `84d5194`: best capacity remains 404 with
  six-class dominance 4, but the proxy rescheduler only improves from 259 to
  260.
- **What to do next:** Search within the capacity-preserving tangent space for
  better balance objectives or multi-direction combinations; the live
  obstruction is now rescheduler balance, not collapse or capacity loss.

### 2026-06-30 - M1 a327 rescheduler-aware quotient-plane search

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_rescheduler_aware_quotient_plane_search.md`,
  `experimental/scripts/scan_m1_a327_rescheduler_aware_quotient_plane_search.py`,
  `experimental/scripts/verify_m1_a327_rescheduler_aware_quotient_plane_search.py`,
  `experimental/scripts/audit_m1_a327_rescheduler_aware_quotient_plane_search.sage`,
  `experimental/data/m1_a327_rescheduler_aware_quotient_plane_search.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_QUOTIENT_PLANES_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A rescheduler-aware quotient-plane proxy search
  around the best collapse-breaking quotient lines from `ad3d73a`. The first
  pass tests 10 lines, 320 second directions, and 10,240 lambda/mu pairs; all
  samples fail the capacity screen, with best capacity upper bound 165.
- **How it is useful:** Shows that the tested weak-block `q2` perturbations
  reduce the six-class collapse but destroy the high-capacity collision
  skeleton before the rescheduler can help.
- **What to do next:** Refine second-direction selection around
  capacity-preserving tangent directions, or analyze why weak-block repair
  directions are transverse to the high-capacity line skeleton.

### 2026-06-30 - M1 a327 collapse-quotient line search

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_collapse_quotient_line_search.md`,
  `experimental/scripts/scan_m1_a327_collapse_quotient_line_search.py`,
  `experimental/scripts/verify_m1_a327_collapse_quotient_line_search.py`,
  `experimental/scripts/audit_m1_a327_collapse_quotient_line_search.sage`,
  `experimental/data/m1_a327_collapse_quotient_line_search.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_QUOTIENT_LINES_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** An affine quotient-line search around the
  high-capacity collapse anchors from `8dbcb6b`. The first pass tests 6
  anchors, 32 ranked quotient directions, and 3,072 lambda values; the best
  line preserves capacity 403 and reduces six-class dominance to 2, but
  reschedules only to max-min 259.
- **How it is useful:** Shows that quotient-line perturbations can break most
  of the `[1,3,4,5,6,7]` dominance without immediate capacity collapse, but the
  resulting value-class geometry is badly unbalanced.
- **What to do next:** Study two-dimensional quotient planes or rescheduler-
  aware quotient direction selection, targeting the `LINE_LOW_RESCHEDULE`
  failure rather than the earlier capacity-collapse failure.

### 2026-06-29 - M1 a327 collapse-subspace quotient solver

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_collapse_subspace_quotient_solver.md`,
  `experimental/scripts/scan_m1_a327_collapse_subspace_quotient_solver.py`,
  `experimental/scripts/verify_m1_a327_collapse_subspace_quotient_solver.py`,
  `experimental/scripts/audit_m1_a327_collapse_subspace_quotient_solver.sage`,
  `experimental/data/m1_a327_collapse_subspace_quotient_solver.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_QUOTIENT_DIRECTIONS_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A quotient-nullspace diagnostic for the two
  distinct high-performing soft target cores. Each has proxy nullity 896,
  collapse-subspace dimension 103, and quotient dimension 793; 232 sampled
  collapse/quotient directions find no collapse-reduced proxy `a>=327`
  candidate.
- **How it is useful:** Shows that quotient directions exist in abundance, but
  the tested directions either destroy capacity or reschedule below target;
  the best high-capacity sample remains collapse-only with proxy max-min 332.
- **What to do next:** Study the capacity-preserving quotient directions that
  land in `QUOTIENT_DIRECTION_LOW_RESCHEDULE`, or formulate an obstruction
  explaining why leaving the collapse subspace loses the balanced high-capacity
  schedule.

### 2026-06-29 - M1 a327 soft collapse-penalty target solver

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_soft_collapse_penalty_target_solver.md`,
  `experimental/scripts/scan_m1_a327_soft_collapse_penalty_target_solver.py`,
  `experimental/scripts/verify_m1_a327_soft_collapse_penalty_target_solver.py`,
  `experimental/scripts/audit_m1_a327_soft_collapse_penalty_target_solver.sage`,
  `experimental/data/m1_a327_soft_collapse_penalty_target_solver.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_TARGET_SYSTEMS_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A soft collapse-penalty target-selection audit
  starting from the robust proxy systems. It tests 180 target systems and
  2,880 proxy codeword tuple samples; the best proxy max-min improves to 332
  with capacity upper bound 460, but all proxy-positive systems remain
  high-capacity degenerate with no collapse-reduced proxy candidate.
- **How it is useful:** Separates hard-split capacity destruction from soft
  target selection: soft penalties preserve and even improve proxy capacity,
  but do not move the evaluated `[1,3,4,5,6,7]` collapse.
- **What to do next:** Use the proxy-positive soft systems as a diagnostic set
  for collapse-specific exact lifting or add nonlinear/evaluation-level
  collapse penalties, rather than more linear target-row penalties alone.

### 2026-06-29 - M1 a327 collapse-aware target system

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_collapse_aware_target_system.md`,
  `experimental/scripts/scan_m1_a327_collapse_aware_target_system.py`,
  `experimental/scripts/verify_m1_a327_collapse_aware_target_system.py`,
  `experimental/scripts/audit_m1_a327_collapse_aware_target_system.sage`,
  `experimental/data/m1_a327_collapse_aware_target_system.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A collapse-aware proxy target-system audit that
  modifies the robust a=327 proxy systems by inserting internal split
  constraints for the known exact collapse class `[1,3,4,5,6,7]`. The first
  pass tests 27 modified affine proxy systems and 216 sampled vectors; all
  samples destroy capacity, with best proxy capacity upper bound 162.
- **How it is useful:** Shows that direct inhomogeneous target splits remove
  six-class dominance but are too rigid in the tested budgets and partitions:
  they destroy the high-capacity collision skeleton before exact `GF(17^32)`
  extraction is triggered.
- **What to do next:** Try softer collapse penalties or exact-field target
  selection that discourages six-witness collapse without forcing hard split
  equalities at high-overlap coordinates.

### 2026-06-29 - M1 a327 residual-degeneracy separation

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_residual_degeneracy_separation.md`,
  `experimental/scripts/scan_m1_a327_residual_degeneracy_separation.py`,
  `experimental/scripts/verify_m1_a327_residual_degeneracy_separation.py`,
  `experimental/scripts/audit_m1_a327_residual_degeneracy_separation.sage`,
  `experimental/data/m1_a327_residual_degeneracy_separation.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A residual-degeneracy ledger and targeted split
  audit for the high-capacity exact skeleton. In all three tested robust
  systems, the exact high-capacity vector identifies witnesses
  `[1,3,4,5,6,7]` and separates witness `2`; 12 quotient-aware split attempts
  do not break this class while preserving capacity.
- **How it is useful:** Converts the vague degeneracy failure into a precise
  residual identification pattern: the obstacle is a six-witness collapse, not
  arbitrary non-distinctness.
- **What to do next:** Target the `[1,3,4,5,6,7]` class directly by modifying
  the collision skeleton or target rows, rather than adding more off-skeleton
  pins to the same exact solve.

### 2026-06-29 - M1 a327 dominant-collision-preserving separation

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_dominant_collision_preserving_separation.md`,
  `experimental/scripts/scan_m1_a327_dominant_collision_preserving_separation.py`,
  `experimental/scripts/verify_m1_a327_dominant_collision_preserving_separation.py`,
  `experimental/scripts/audit_m1_a327_dominant_collision_preserving_separation.sage`,
  `experimental/data/m1_a327_dominant_collision_preserving_separation.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A safe-coordinate separation audit for the robust
  proxy high-capacity skeleton. The audit tests 24 off-skeleton pairwise or
  evaluation separation pin sets across the top three robust systems; nine
  exact vectors are constructed, but none are both nondegenerate and
  capacity-preserving.
- **How it is useful:** Shows that even separation pins outside the all-seven
  protected collision coordinates fail to combine high capacity with witness
  distinctness in the tested schedules.
- **What to do next:** Study the high-capacity degenerate `374`-capacity
  samples to identify which lower-dimensional witness identifications remain,
  then try quotient-aware separation inside that residual degenerate class.

### 2026-06-29 - M1 a327 collision-preserving nondegenerate lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_collision_preserving_nondegenerate_lift.md`,
  `experimental/scripts/scan_m1_a327_collision_preserving_nondegenerate_lift.py`,
  `experimental/scripts/verify_m1_a327_collision_preserving_nondegenerate_lift.py`,
  `experimental/scripts/audit_m1_a327_collision_preserving_nondegenerate_lift.sage`,
  `experimental/data/m1_a327_collision_preserving_nondegenerate_lift.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A pinned exact-lift audit that starts from the
  high-capacity proxy-support schedules and adds small coefficient pins in the
  other witness blocks. Across three robust proxy systems, 36 exact vectors
  were tested; 18 were nondegenerate but none retained capacity at least 327.
- **How it is useful:** Confirms the sharper obstruction: the tested minimal
  coefficient pins break degeneracy only by destroying the value-class
  collision structure.
- **What to do next:** Try less destructive separation mechanisms, especially
  evaluation or pairwise-separation pins chosen on coordinates outside the
  dominant collision classes, or solve for separation inside a partial exact
  nullspace rather than pinning common-free coefficients directly.

### 2026-06-29 - M1 a327 nondegenerate exact lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_nondegenerate_exact_lift.md`,
  `experimental/scripts/scan_m1_a327_nondegenerate_exact_lift.py`,
  `experimental/scripts/verify_m1_a327_nondegenerate_exact_lift.py`,
  `experimental/scripts/audit_m1_a327_nondegenerate_exact_lift.sage`,
  `experimental/data/m1_a327_nondegenerate_exact_lift.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact `GF(17^32)` lift audit for the top
  robust proxy-positive system from `f9a43ea`. The audit tests 32 exact vectors
  across proxy-support, balanced-block, and seeded common-free schedules with
  four exact value patterns; no vector reaches `a=327`.
- **How it is useful:** Sharpens the exact-lift failure mode: proxy-support
  schedules keep high capacity but remain degenerate, while balanced free
  schedules make codewords distinct but collapse the value-class capacity.
- **What to do next:** Use the nondegeneracy/capacity split to design exact
  schedules that preserve the proxy-support collision structure while forcing
  nonzero coefficient support in all six witness blocks.

### 2026-06-29 - M1 a327 robust-proxy constrained extraction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_robust_proxy_constrained_extraction.md`,
  `experimental/scripts/scan_m1_a327_robust_proxy_constrained_extraction.py`,
  `experimental/scripts/verify_m1_a327_robust_proxy_constrained_extraction.py`,
  `experimental/scripts/audit_m1_a327_robust_proxy_constrained_extraction.sage`,
  `experimental/data/m1_a327_robust_proxy_constrained_extraction.json`,
  `experimental/data/m1_a327_robust_proxy_constrained_extraction_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** CONSTRAINED_SCHEDULE_PROXY_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A constrained extraction diagnostic for the 13
  robust proxy-positive a=327 systems. All 13 have stable pivot columns, free
  columns, and pivot rows across five proxy primes, and the best deterministic
  common-free schedule preserves proxy `a>=327` across all five primes. A
  bounded Sage exact audit finds no `GF(17^32)` witness from the first 64-row
  partial solve.
- **How it is useful:** Narrows the live problem from broad proxy search to
  exact constrained extraction from a stable free-column mechanism.
- **What to do next:** Try larger or block-structured exact partial solves,
  vary free-column values, and use stable proxy pivot rows to avoid dense full
  `GF(17^32)` RREF.

### 2026-06-29 - M1 a327 proxy-positive exact extraction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_proxy_positive_exact_extraction.md`,
  `experimental/scripts/scan_m1_a327_proxy_positive_exact_extraction.py`,
  `experimental/scripts/verify_m1_a327_proxy_positive_exact_extraction.py`,
  `experimental/scripts/audit_m1_a327_proxy_positive_exact_extraction.sage`,
  `experimental/data/m1_a327_proxy_positive_exact_extraction.json`,
  `experimental/data/m1_a327_proxy_positive_exact_extraction_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** MULTIPRIME_ROBUST_PROXY_CANDIDATE / PARTIAL / EXPERIMENTAL.
- **What is being added:** A diagnostic/extraction pass for the 13
  proxy-positive systems from the incumbent-guided target mutation checkpoint.
  All 13 remain proxy-positive over five `p == 1 mod 512` proxy fields with
  rank/nullity `640/896`, and the top system has full row rank in the first 16
  and 32 exact `GF(17^32)` target rows.
- **How it is useful:** Shows that the `a>=327` proxy hit is not merely a
  `GF(12289)` accident, while keeping the exact `GF(17^32)` witness extraction
  boundary explicit.
- **What to do next:** Use the robust multi-prime pivot/free-column structure to
  implement exact constrained extraction over `GF(17^32)` without dense full
  RREF, then Sage-audit any exact sample reaching `a>=327`.

### 2026-06-29 - M1 a327 incumbent-guided target mutation

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_incumbent_guided_target_mutation.md`,
  `experimental/scripts/scan_m1_a327_incumbent_guided_target_mutation.py`,
  `experimental/scripts/verify_m1_a327_incumbent_guided_target_mutation.py`,
  `experimental/scripts/audit_m1_a327_incumbent_guided_target_mutation.sage`,
  `experimental/data/m1_a327_incumbent_guided_target_mutation.json`,
  `experimental/data/m1_a327_incumbent_guided_target_mutation_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / PARTIAL / EXPERIMENTAL.
- **What is being added:** A feedback-driven target mutation pass around the
  best balanced target/codeword solver incumbents. The proxy search tests 50
  mutated systems and 1600 codeword tuple samples over `GF(12289)`, improving
  the best proxy rescheduled max-min from 319 to 329. A bounded Sage lift audit
  over `GF(17^32)` checks the top lifted proxy tuples and finds no exact
  `a=327` lift; full exact nullspace extraction remains open.
- **How it is useful:** Shows that the post-rescheduling deficit can be
  attacked directly by incumbent-guided target mutation, while preserving the
  boundary between proxy candidates and exact interleaved-list proof records.
- **What to do next:** Implement an exact extraction path for the proxy-positive
  target systems, avoiding dense full `GF(17^32)` RREF where possible, then
  Sage-audit any exact nullspace sample that reaches `a>=327`.

### 2026-06-29 - M1 a327 random low-degree list-witness search

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_a327_random_lowdegree_list_witness_search.md`,
  `experimental/data/m1_a327_random_lowdegree_list_witness_search.json`,
  `experimental/scripts/scan_m1_a327_random_lowdegree_list_witness_search.py`,
  `experimental/scripts/verify_m1_a327_random_lowdegree_list_witness_search.py`,
  `experimental/scripts/audit_m1_a327_random_lowdegree_list_witness_search.sage`,
  `experimental/agents-log.md`.
- **Status:** PARTIAL / TESTED_TUPLES_NO_A327 / EXPERIMENTAL.
- **What is being added:** A first direct constructive `a=327`
  interleaved-list search over deterministic low-degree codeword tuples. The
  Sage audit evaluates 116 tuples over `GF(17^32)` and applies the exact
  value-class capacity upper bound; the best upper bound is `291`.
- **How it is useful:** Moves the active thread away from RIM pivot audits and
  back toward positive `a>=327` witness construction, while route-cutting the
  named first-layer random/sparse/root-core/monomial tuple families.
- **What to do next:** Try a more adaptive construction that designs the
  received-word value classes first or uses staged interpolation constraints;
  do not treat this as a global `Lambda_mu(C,327) <= 6` result or MCA evidence.

### 2026-06-29 - M1 a327 value-class-first witness search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_valueclass_first_witness_search.md`,
  `experimental/scripts/scan_m1_a327_valueclass_first_witness_search.py`,
  `experimental/scripts/verify_m1_a327_valueclass_first_witness_search.py`,
  `experimental/scripts/audit_m1_a327_valueclass_first_witness_search.sage`,
  `experimental/data/m1_a327_valueclass_first_witness_search.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_DESIGNS_NO_PROXY_NULLITY / PARTIAL / EXPERIMENTAL.
- **What is being added:** A first value-class-first incidence search for
  the M1 `a=327` interleaved-list target. The scanner builds 14 deterministic
  balanced 4/5 membership designs with support size 327 for each of seven
  witnesses and pair intersections below the 255 cap. The Sage audit runs a
  reduced-rank proxy over `GF(12289)` and finds proxy nullity zero for every
  tested design, so exact `GF(17^32)` extraction is not triggered.
- **How it is useful:** Tests the missing middle between support-first RIM
  gates and codeword-first tuple generation by designing received-word value
  classes before interpolation.
- **What to do next:** Broaden value-class incidence generation toward
  pair-boundary and quotient-fiber-residual designs, or add a stronger
  proxy-positive search objective before spending exact `GF(17^32)` rank time.

### 2026-06-29 - M1 a327 value-class boundary search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_valueclass_boundary_search.md`,
  `experimental/scripts/scan_m1_a327_valueclass_boundary_search.py`,
  `experimental/scripts/verify_m1_a327_valueclass_boundary_search.py`,
  `experimental/scripts/audit_m1_a327_valueclass_boundary_search.sage`,
  `experimental/data/m1_a327_valueclass_boundary_search.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_DESIGNS_NO_PROXY_NULLITY / PARTIAL / EXPERIMENTAL.
- **What is being added:** A boundary-stressed value-class-first search for
  the M1 `a=327` interleaved-list target. The scanner builds 200 deterministic
  incidence designs across pair-boundary, quotient-fiber, and
  boundary-residual families. Every design has seven supports of size 327 and
  three pair intersections at the cap 255. The Sage audit ranks all candidates
  over proxy field `GF(12289)` and finds no proxy-positive reduced-nullity
  candidate.
- **How it is useful:** Tests whether value-class-first designs become more
  promising when they stress the RS pairwise equality cap rather than keeping
  pair intersections around 193..198.
- **What to do next:** Either add an adaptive rank-feedback mutation loop for
  boundary value classes or move to a different constructive mechanism; do not
  treat this proxy screen as an exact `GF(17^32)` route cut.

### 2026-06-29 - M1 a327 value-class boundary exact audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_valueclass_boundary_exact_audit.md`,
  `experimental/scripts/verify_m1_a327_valueclass_boundary_exact_audit.py`,
  `experimental/scripts/audit_m1_a327_valueclass_boundary_exact_audit.sage`,
  `experimental/data/m1_a327_valueclass_boundary_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL.
- **What is being added:** An exact `GF(17^32)` pivot-minor hardening pass for
  five selected boundary-stressed value-class candidates. The audit verifies
  exact full-rank minors for the top retained boundary-residual candidate, a
  quotient-fiber candidate, two pair-boundary variants, and a residual-split
  variant.
- **How it is useful:** Converts part of the proxy-screen boundary search into
  exact route cuts for named candidates without claiming a global `a=327`
  obstruction.
- **What to do next:** If continuing the value-class-first route, use
  rank-feedback mutation to search for proxy-positive candidates rather than
  adding more fixed boundary templates.

### 2026-06-29 - M1 a327 value-class high-overlap beam

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_valueclass_high_overlap_beam.md`,
  `experimental/scripts/scan_m1_a327_valueclass_high_overlap_beam.py`,
  `experimental/scripts/verify_m1_a327_valueclass_high_overlap_beam.py`,
  `experimental/scripts/audit_m1_a327_valueclass_high_overlap_beam.sage`,
  `experimental/data/m1_a327_valueclass_high_overlap_beam.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_DESIGNS_NO_PROXY_NULLITY / PARTIAL / EXPERIMENTAL.
- **What is being added:** A rank-feedback mutation layer for value-class-first
  `a=327` search. The scanner starts from boundary value-class seeds and runs
  degree-preserving two-coordinate mutations allowing membership sizes
  3,4,5,6. It generates 64 candidates, reaching nine pair intersections at
  the cap 255, then Sage screens all candidates over proxy field `GF(12289)`.
- **How it is useful:** Tests a much higher-overlap value-class incidence
  family than the fixed 4/5 boundary templates, while keeping support size 327
  and pair cap 255 exact.
- **What to do next:** If this route continues, exact-audit structurally
  interesting retained candidates or redesign the generator to target equation
  template repetition directly; do not treat the proxy screen as an exact
  `GF(17^32)` route cut.

### 2026-06-29 - M1 a327 value-class high-overlap exact audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_valueclass_high_overlap_exact_audit.md`,
  `experimental/scripts/verify_m1_a327_valueclass_high_overlap_exact_audit.py`,
  `experimental/scripts/audit_m1_a327_valueclass_high_overlap_exact_audit.sage`,
  `experimental/data/m1_a327_valueclass_high_overlap_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL.
- **What is being added:** An exact `GF(17^32)` pivot-minor hardening pass for
  six retained or structurally notable high-overlap value-class candidates.
  The audit verifies exact full-rank minors for all six selected candidates,
  including low-variable boundary-residual variants and nine-capped-pair
  quotient-fiber / pair-boundary variants.
- **How it is useful:** Upgrades the high-overlap value-class beam from a
  proxy-only negative into exact route cuts for named candidates, without
  claiming a global `a=327` obstruction.
- **What to do next:** Stop this exact-audit layer unless a new generator
  produces proxy-positive candidates or a structurally different incidence
  family; no #133 update follows from this route cut.

### 2026-06-29 - M1 a327 value-class MILP incidence seeds

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_valueclass_milp_incidence_seeds.md`,
  `experimental/scripts/scan_m1_a327_valueclass_milp_incidence_seeds.py`,
  `experimental/scripts/verify_m1_a327_valueclass_milp_incidence_seeds.py`,
  `experimental/scripts/audit_m1_a327_valueclass_milp_incidence_seeds.sage`,
  `experimental/data/m1_a327_valueclass_milp_incidence_seeds.json`,
  `experimental/data/m1_a327_valueclass_milp_incidence_seeds_rank_audit.json`,
  `experimental/agents-log.md`.
- **Status:** ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL.
- **What is being added:** A solver-assisted value-class incidence seed search
  using `scipy.optimize.milp`. The MILP count profile can put all 21 pair
  intersections exactly at 255, but Sage proxy-ranks all 18 embedded candidates
  with nullity zero and exact-audits eight selected candidates over
  `GF(17^32)` with full-rank minors.
- **How it is useful:** Separates the combinatorial incidence-count question
  from the algebraic rank gate and shows that even all-pair-boundary
  value-class profiles can remain full rank in tested embeddings.
- **What to do next:** Do not keep maximizing pair-boundary pressure alone;
  any next constructive search should target algebraic row dependencies or
  jointly construct codewords and received-word values.

### 2026-06-29 - M1 a327 singular all-pair-boundary embedding search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_singular_all_pair_boundary_embedding_search.md`,
  `experimental/scripts/scan_m1_a327_singular_all_pair_boundary_embedding_search.py`,
  `experimental/scripts/verify_m1_a327_singular_all_pair_boundary_embedding_search.py`,
  `experimental/scripts/audit_m1_a327_singular_all_pair_boundary_embedding_search.sage`,
  `experimental/data/m1_a327_singular_all_pair_boundary_embedding_search.json`,
  `experimental/data/m1_a327_singular_all_pair_boundary_embedding_search_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** ROUTE_CUT_TESTED_EMBEDDINGS / PARTIAL / EXPERIMENTAL.
- **What is being added:** A placement search for the MILP
  all-pair-boundary value-class multiset. The scanner tests 515 embeddings of
  the same multiset, including deterministic layouts and 512 seeded shuffles;
  all have full proxy rank over `GF(12289)`. Sage exact-audits nine
  representative embeddings over `GF(17^32)` and all nine remain full rank.
- **How it is useful:** Attacks the precise algebraic placement failure mode
  left by the MILP incidence seed search: even with all 21 pair intersections
  at 255 and only six compressed variables, tested placements do not create
  a reduced rank defect.
- **What to do next:** A further search should stop relying on the same MILP
  optimum and instead construct row dependencies directly, or jointly solve
  for codeword coefficients and received-word classes.

### 2026-06-29 - M1 a327 coefficient-nullspace target search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_coefficient_nullspace_target_search.md`,
  `experimental/scripts/scan_m1_a327_coefficient_nullspace_target_search.py`,
  `experimental/scripts/verify_m1_a327_coefficient_nullspace_target_search.py`,
  `experimental/scripts/audit_m1_a327_coefficient_nullspace_target_search.sage`,
  `experimental/data/m1_a327_coefficient_nullspace_target_search.json`,
  `experimental/data/m1_a327_coefficient_nullspace_target_search_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** ROUTE_CUT_TESTED_ROOT_SETS / PARTIAL / EXPERIMENTAL.
- **What is being added:** A coefficient-level scalar nullspace search. The
  scanner chooses 255-root locator sets, writes `D_i=c_i L_i`, tests 10,736
  scalar/root candidates over `GF(12289)`, and finds best capacity upper bound
  293. A Sage exact audit over `GF(17^32)` tests six selected root tuples and
  finds best exact capacity upper bound at most 292.
- **How it is useful:** Directly attacks the six-scalar determinant condition
  left by all-pair-boundary incidence designs, rather than shuffling the same
  membership multiset.
- **What to do next:** Scalar locator models look too low-capacity; the next
  constructive attempt should allow non-scalar residual factors `R_i` or solve
  codeword coefficients and received-word classes jointly.

### 2026-06-29 - M1 a327 degree-1 residual nullspace search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_degree1_residual_nullspace_search.md`,
  `experimental/scripts/scan_m1_a327_degree1_residual_nullspace_search.py`,
  `experimental/scripts/verify_m1_a327_degree1_residual_nullspace_search.py`,
  `experimental/scripts/audit_m1_a327_degree1_residual_nullspace_search.sage`,
  `experimental/data/m1_a327_degree1_residual_nullspace_search.json`,
  `experimental/data/m1_a327_degree1_residual_nullspace_search_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL.
- **What is being added:** A degree-1 residual relaxation of the scalar
  locator nullspace search. The scanner tests 48,048 proxy candidates of the
  form `D_i=c_i L_i R_i`, with `deg L_i=254` and `deg R_i<=1`, over
  `GF(12289)` and finds no `a=327` candidate; a Sage audit then exact-checks
  seven selected candidates over `GF(17^32)` and all remain below capacity
  target.
- **How it is useful:** Tests the first affine residual extension after the
  scalar locator model without returning to support shuffles or RIM replay
  audits.
- **What to do next:** If continuing this locator lane, use a multi-prime
  PARI/GP or Sage sieve for all-pair-boundary embeddings, or move to a
  genuinely joint codeword/received-word construction.

### 2026-06-29 - M1 a327 all-pair multi-prime sieve

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_allpair_multiprime_sieve.md`,
  `experimental/scripts/scan_m1_a327_allpair_multiprime_sieve.py`,
  `experimental/scripts/verify_m1_a327_allpair_multiprime_sieve.py`,
  `experimental/scripts/audit_m1_a327_allpair_multiprime_sieve.sage`,
  `experimental/data/m1_a327_allpair_multiprime_sieve.json`,
  `experimental/data/m1_a327_allpair_multiprime_sieve_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_EMBEDDINGS_NO_MULTIPRIME_PROXY_ANOMALY / PARTIAL /
  EXPERIMENTAL.
- **What is being added:** A PARI/GP-seeded multi-prime proxy sieve for the
  all-pair-boundary scalar-locator embeddings. The scanner tests all 515
  embeddings over 23 primes `p == 1 mod 512`, for 11,845 reduced-rank
  evaluations, and finds no rank or capacity anomaly. The Sage wrapper records
  that no exact `GF(17^32)` audit was triggered.
- **How it is useful:** Hardens the all-pair-boundary scalar-locator negative
  signal across many proxy fields before spending exact field time.
- **What to do next:** Leave the scalar all-pair-boundary locator model unless
  a new anomaly mechanism appears; the next constructive attack should allow
  richer residual factors or jointly solve for codewords and received-word
  classes.

### 2026-06-29 - M1 a327 joint target/codeword solver

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_joint_target_codeword_solver.md`,
  `experimental/scripts/scan_m1_a327_joint_target_codeword_solver.py`,
  `experimental/scripts/verify_m1_a327_joint_target_codeword_solver.py`,
  `experimental/scripts/audit_m1_a327_joint_target_codeword_solver.sage`,
  `experimental/data/m1_a327_joint_target_codeword_solver.json`,
  `experimental/data/m1_a327_joint_target_codeword_solver_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_TARGET_SYSTEMS_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded joint target/codeword proxy solver. It
  selects partial received-word value-class constraints from all-pair-boundary
  embeddings, solves the induced homogeneous systems for six degree `<256`
  difference polynomials over `GF(12289)`, samples 320 nullspace codeword
  tuples, and globally reschedules each tuple with the exact value-class
  max-min solver. The best capacity upper bound is 454, but the best
  rescheduled proxy max-min agreement is 311.
- **How it is useful:** Tests the missing middle between support-first rank
  gates and codeword-first tuple generation by constructing codeword
  coefficients from partial received-word target systems.
- **What to do next:** Use a stronger target-set chooser, such as CP-SAT or
  MILP, to select constraints by predicted post-reschedule balance rather than
  fixed coordinate-order heuristics.

### 2026-06-29 - M1 a327 balanced target MILP codeword solver

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_balanced_target_milp_codeword_solver.md`,
  `experimental/scripts/scan_m1_a327_balanced_target_milp_codeword_solver.py`,
  `experimental/scripts/verify_m1_a327_balanced_target_milp_codeword_solver.py`,
  `experimental/scripts/audit_m1_a327_balanced_target_milp_codeword_solver.sage`,
  `experimental/data/m1_a327_balanced_target_milp_codeword_solver.json`,
  `experimental/data/m1_a327_balanced_target_milp_codeword_solver_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** TESTED_TARGET_SYSTEMS_NO_A327 / PARTIAL / EXPERIMENTAL.
- **What is being added:** A MILP-selected balanced target/codeword layer. It
  tests 120 target systems across three row budgets and five balance
  objectives, samples 1,920 nullspace codeword tuples over `GF(12289)`, and
  globally reschedules each high-capacity proxy tuple. The best raw capacity
  upper bound is 457 and the best proxy rescheduled max-min agreement improves
  to 319.
- **How it is useful:** Directly attacks the imbalance bottleneck exposed by
  the prior joint solver, moving the best proxy max-min from 311 to 319
  without producing an `a=327` certificate.
- **What to do next:** Refine around the best `B512 / fiber_diversity` and
  `hybrid_balance` systems with local target-coordinate mutations and larger
  nullspace sampling.

### 2026-06-29 - Paper D v7 first-grid cap promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v7.tex`, `cs25_cap_v7.pdf`,
  `site/papers/cs25_cap_v7.pdf`,
  `experimental/notes/audits/paperD_v7_vs_v6_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V7_CAP /
  PROVED_PAPERD_V7_FIRST_GRID.
- **What is being added:** Paper D v7 is promoted as the current public Paper D
  source. It preserves the v6 universal fixed-divisor MCA cap, extends the
  no-loss CA endpoint to `floor(delta n) <= n-k-1`, and adds the first-grid
  deep-point cap for large official-envelope rows.
- **How it is useful:** The public board can now show two Paper D theorem
  layers: the older uniform fixed-divisor cap and the stronger large-row
  first-grid cap `delta*_C(2^-128) <= 1-rho-1/n`.
- **What to do next:** Keep first-grid rows separate from exact-threshold
  claims. The missing safe-side work remains the L1/M1/F1/M2 completion package.

### 2026-06-29 - PR #136 width-one fixed-root closure

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:** `experimental/notes/m1/m1_width_one_fixedroot_closure.md`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`, and
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL-CLOSURE / AUDIT.
- **What is being added:** A compact width-one M1 closure note: width-one
  maximal root shadows are bounded-complement rank tests, descend losslessly
  under fixed-root absorption, and inject into one-root fixed-divisor/root-slice
  ledgers.
- **How it is useful:** It reduces the width-one critical-tail branch to the
  existing one-root fixed-root ledger in fixed surplus, giving a smaller target
  for the M1 proof program without promoting a full all-line theorem.
- **What to do next:** Prove or import the polynomial fixed-surplus bound for
  `FixedRootOneRoot_{r1}` after quotient-periodic, tangent, fixed-root, and
  aperiodic charges; do not treat this as a leaderboard row.

### 2026-06-29 - PR #131--#135 triage and frontier rows

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes, and
  Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-29.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_a507_adjacent_bridge_theorem.md`,
  `experimental/notes/m1/m1_a507_plus_one_slope_hunt.md`,
  `experimental/notes/m1/m1_interleaved_list_*.md`,
  `experimental/notes/m1/m1_random_simple_pole_entropy_floor.md`,
  `experimental/notes/m1/m1_coset_packet_finite_slope_floors.md`,
  matching JSON certificates under `experimental/data/`, matching verifiers
  under `experimental/scripts/`, `experimental/experiments.tex`, and site data.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / PROOF_RECORD / LOWER_BOUND /
  ROUTE_CUT / AUDIT.
- **What is being added:** The PR wave adds three useful frontier-facing
  packets: Scott Hughes's interleaved-list hybrid certificate
  `Lambda_mu(C,326) >= 7`, Vadim Avdeev's random simple-pole finite-slope floors
  for `a=257..260`, and Vadim Avdeev's coset-packet finite-slope floors for
  `a=261..288`. AllenGrahamHart's boundary-off external-anchor M1 normal form is
  distilled into a compact proof-program audit, and Scott Hughes's `a=507`
  adjacent-bridge packet is integrated as a route cut rather than a new row.
- **How it is useful:** The finite-slope floors strengthen the low-agreement
  side of the `F_17^32, n=512, k=256` MCA ledger, while the interleaved-list
  packet moves the separate list-track lower-bound row up to agreement `326`.
  The route-cut notes prevent accidental mixing of adjacent line/list
  numerators into the same finite-slope MCA denominator.
- **What to do next:** Human-review the finite-slope-to-MCA noncontainment
  convention before paper promotion, keep #131 as proof-program material until
  it proves a global M1 bound, and treat the Sage scripts in #133 as optional
  independent audits rather than required local verification.

### 2026-06-29 - Paper D v6 promotion and completion-program audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v6.tex`, `cs25_cap_v6.pdf`,
  `site/papers/cs25_cap_v6.pdf`,
  `experimental/notes/audits/paperD_v6_vs_v5_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V6_CAP.
- **What is being added:** Paper D v6 is promoted as the current public Paper D
  source. It keeps the v5 universal MCA cap constants and CS25-free route,
  tightens the conversion collision-count derivation, and adds the
  prize-facing integer-staircase/completion program.
- **How it is useful:** Public rows now cite the strongest Paper D package:
  same cap theorem, clearer prize posture, and explicit conditional MCA/list
  completion theorems for turning the one-sided cap into a full threshold
  determination.
- **What to do next:** Use `PROVED_PAPERD_V6_CAP` for verified Paper D cap rows,
  while keeping the missing L1/M1/F1/M2 completion obligations separate from
  the proved cap itself.

### 2026-06-27 - Root-level paper PDF relocation

- **Agent/model:** Codex.
- **Files added or changed:** `cs25_cap_v5.pdf`, `slackMCA_v4.pdf`,
  `snarks_v5.pdf`, removed generated PDF outputs from `tex/`,
  `site/data/papers.json`, `site/index.html`, `experimental/agents-log.md`.
- **Status:** AUDIT / RELEASE-HYGIENE.
- **What is being added:** The generated Paper B/C/D PDFs are moved out of
  `tex/` into the repository root, matching the README convention that TeX
  sources live under `tex/` and PDFs live at the root. Site-local mirrors under
  `site/papers/` remain for static hosting.
- **How it is useful:** Keeps GitHub PDF links and repository layout aligned
  with the public paper set: B v4, C v5, and D v5.
- **What to do next:** Keep future TeX compile outputs copied to root and, when
  needed, mirrored into `site/papers/` for static-site serving.

### 2026-06-27 - Paper B/C/D version promotion and leaderboard source audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/slackMCA_v4.tex`,
  `slackMCA_v4.pdf`, `tex/snarks_v5.tex`, `snarks_v5.pdf`,
  `site/papers/slackMCA_v4.pdf`, `site/papers/snarks_v5.pdf`, `readme.md`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Two clarification edits are added to the promoted
  Paper B/C versions: the Paper B unsplit curve-envelope lower bound is
  explicitly the line witness embedded as a degree-`d` curve, and Paper C now
  says the curve compiler applies to the finite power-curve/evaluation-domain
  model rather than arbitrary protocol samplers. The README records the current
  public versions B v4, C v5, and D v5.
- **How it is useful:** Keeps the paper prose aligned with the public board:
  Paper D v5 cap rows are proved under their printed scanner hypotheses,
  high-agreement/list rows cite Paper B v4 after promotion, and Paper C v5 is
  framed as protocol-ledger packaging rather than a new cap row.
- **What to do next:** Commit the version promotion after final review, and
  keep future leaderboard rows explicit about whether they are Paper B
  high-agreement theorem rows, Paper D v5 cap rows, or Paper C protocol-ledger
  packaging rows.

### 2026-06-27 - M1 variable-line packet and singleton lemmas

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/experiments.tex`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** Local packet lemmas for non-fixed variable Hankel
  determinant lines: active-new packet mass is reduced to active domain
  singletons, quotient defects, and a different-slope two-exchange codegree
  image.  The singleton term is then reduced to contained/tangent and
  one-outside target images, with the zero-lower class eliminated in the
  high-agreement range `a>(n+1)/2`.
- **How it is useful:** This extracts a reviewable M1 reduction from the
  all-line Hankel packet while keeping it out of the leaderboard.  It narrows
  the remaining non-fixed variable-line branch to explicit target-image and
  codegree estimates.
- **What to do next:** Prove polynomial bounds for the active different-slope
  two-exchange codegree and the one-outside boundary target image inside the
  quotient-aware residue-line ledger; do not cite this as the final M1 theorem.

### 2026-06-27 - Paper D v5 cap status promotion in scanner and board

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `experimental/notes/certificate_scanner/README.md`,
  `experimental/notes/certificate_scanner/outputs/`,
  `experimental/notes/audits/a0_cs25_rational_constant_derivation.md`,
  `experimental/notes/audits/theorem_label_map.md`,
  `experimental/notes/audits/codex-f1-l1-20260617/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT.
- **What is being added:** The scanner now emits `PROVED_PAPERD_V5_CAP` for
  active Paper D v5 cap rows whose divisor, binomial, and field hypotheses pass,
  and `NO_ACTIVE_PAPERD_V5_CAP` when no such row is found. Existing scanner
  reports and leaderboard-sweep outputs are regenerated or mechanically updated
  to remove the old draft/CS25-import status, and stale experimental audit notes
  now mark that import route as relevant only to older CA/list comparisons.
- **How it is useful:** Aligns the public leaderboard and scanner with Paper D
  v5's self-contained MCA cap route. Verified Paper D cap rows are no longer
  marked with the older conditional-import or draft-example statuses.
- **What to do next:** Keep CA/list comparison statements separate from the MCA
  cap status, and update any remaining paper-level prose that still discusses
  the older CS25-dependent route as the main Paper D theorem.

### 2026-06-27 - Finite-row threshold note and pure-MCA scanner profile

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/thresholds/f17_32_finite_mca_threshold.tex`,
  `experimental/notes/thresholds/f17_32_finite_mca_threshold.pdf`,
  `experimental/notes/certificate_scanner/examples/f17_512_mca_only.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL-SCANNER.
- **What is being added:** A standalone finite-row threshold note packages the
  \(\F_{17^{32}}, n=512,k=256\) row as an exact finite-slope support-wise MCA
  threshold: agreement \(506\) is unsafe, agreement \(507\) is safe, and the
  closed-real safe interval is \([0,6/512)\). A pure-MCA scanner profile is
  added so the 506/507 endpoint is not mixed with the optional line-plus-list
  protocol ledger.
- **How it is useful:** Supersedes the old strict264-next threshold plan for
  this finite row and gives the clean packaging needed for the public board and
  `towards-prize.md`. It also isolates the next theorem target: the
  row-independent high-agreement threshold compiler with
  \(B_Q=\lfloor Q/2^{128}\rfloor\).
- **What to do next:** Audit the official MCA sampler definition against the
  finite/projective slope conventions and decide whether to promote the
  row-independent compiler from experimental notes into a paper-level theorem.

### 2026-06-27 - Prime192 leaderboard sweep rows

- **Agent/model:** Codex, auditing `leaderboard_sweep_192`.
- **Files added or changed:** `experimental/notes/certificate_scanner/outputs/leaderboard_sweep_192/`,
  `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`, and
  `site/index.html`.
- **Status:** PROVED_PAPERD_V5_CAP / AUDIT.
- **What is being added:** The scanner sweep contributes four concrete
  prime-field rows with `q` near `2^192`, `k=2^40`, smooth power-of-two
  subgroup domains, and one row per official prize rate. It also records a
  small `F_17^32` Paper D example at agreement `258`.
- **How it is useful:** These rows instantiate the Paper D v5 cap with exact
  field/domain arithmetic, making the theorem-envelope rows concrete without
  claiming a new theorem beyond Paper D or an explicit slope census.
- **What to do next:** Regenerate the sweep from a checked-in sweep script if
  the scanner API changes, and keep CA/list comparison statements separate from
  the proved MCA cap status.

### 2026-06-27 - PR #122--#129 triage and selective integration

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes,
  and Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-27.md`,
  `experimental/notes/l1/l1_prefix_dual_d3_subgroup_twisted_collision_bound.md`,
  `experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md`,
  `experimental/notes/f1/f1_arbitrary_anchor_locator_split.md`,
  `experimental/notes/m1/m1_all_line_hankel_aperiodic_packet_audit.md`,
  `experimental/data/adjacent-ledgers/`, selected verifier scripts, and
  `experimental/experiments.tex`.
- **Status:** PROVED / IMPORTED-STANDARD-INPUT / AUDIT / PROOF PROGRAM /
  EXPERIMENTAL.
- **What is being added:** New bounded L1/F1/M2 notes are integrated, while
  PR #127's large M1 generated packet is distilled into a smaller audit note.
  The public board is updated only for tangent-floor-backed status corrections:
  Cycle116/119 gates are unconditional but their exact Cycle84 numerator remains
  conditional, and reserve272/288/313 are marked as proved only because they are
  subsumed by tangent/strict352 floors.
- **How it is useful:** Adds useful L1 `d=3` proper-subgroup and monomial-prefix
  toy theorems, sharpens the F1 arbitrary-anchor ledger, and records
  challenge-map pullback accounting for protocol-facing high-agreement ledgers
  without promoting non-verified material to theorem status.
- **What to do next:** Split the M1 all-line aperiodic packet into small
  separately auditable verifiers before considering any stronger theorem claim;
  human-review the imported Katz/Gauss inputs in the L1 `d=3` note before moving
  it toward Paper B.

### 2026-06-27 - Promoted high-agreement TeX split

- **Agent/model:** Codex, verifying and promoting the user-supplied
  `experiments_v2.tex` split.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/notes/high_agreement/`,
  `experimental/scripts/verify_promoted_high_agreement_ledgers.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / AUDIT.
- **What is being added:** The bulky high-agreement tangent, CA/projective,
  curve, interleaved-list, current-row protocol, and general threshold compiler
  material is split into reusable TeX fragments under
  `experimental/notes/high_agreement/` and included from the canonical
  `experimental/experiments.tex` wrapper.
- **How it is useful:** Keeps the stable high-agreement theorem package
  reviewable in smaller files while preserving the compiled experimental memo.
  The split also fixes the stale missing backslash before the
  `Towards-Prize Finite-Threshold Theorems` section header.
- **What to do next:** Human-review the curve sampler caveat before citing the
  curve statements in protocol settings, and keep protocol query/folding,
  extension-lift, challenge-field, and cryptographic losses as separate ledger
  terms.

### 2026-06-26 - Generalized high-agreement ledgers

- **Agent/model:** GPT-5.5 Pro generalized-ledgers packet, audited and
  integrated by Codex.
- **Files added or changed:** `experimental/data/generalized-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/data/README.md`, `site/data/updates.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** A row-independent high-agreement ledger calculus for
  `RS[F,D,k]` rows: with `R=n-k`, `r=n-a`, and `B_Q=floor(Q/2^128)`, the exact
  line/CA/projective numerator is `r+1` in the range `r <= floor(R/3)`, the
  degree-`d` curve numerator is `d(r+1)` in the range
  `r <= floor(R/(d+2))`, and interleaved-list uniqueness holds for
  `r <= floor(R/2)`.
- **How it is useful:** This moves the adjacent-ledger conclusions beyond the
  special `F_17^32` row.  It gives a reusable integer calculator for deciding
  when tangent-star high-agreement terms alone can pin a `2^-128` threshold,
  and shows that at prize-scale dimensions the method stops pinning thresholds
  once field sizes are roughly above `2^166` to `2^170`, depending on rate.
- **What to do next:** Use this calculator before adding any new row to the
  public board, and keep quotient-core, generated-field entropy, challenge
  field, folding, query, and cryptographic terms as separate ledgers.

### 2026-06-26 - High-agreement adjacent CA/curve/list ledgers

- **Agent/model:** GPT-5.5 Pro adjacent-ledgers packet, audited and integrated
  by Codex.
- **Files added or changed:** `experimental/data/adjacent-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** The high-agreement tangent staircase is extended to
  no-loss CA, projective-slope support-wise MCA, finite-parameter degree-`d`
  curve CA/MCA, and MDS interleaved-list uniqueness.  For
  `RS[F_17^32,H,256]`, the line-plus-list coding ledger is unsafe at
  agreement `a=507` and safe at `a=508` when no query/folding loss is added.
- **How it is useful:** This answers the immediate adjacent-ledger question
  past the finite-slope `506/507` gate: the high-agreement CA/projective/curve
  and interleaved-list coding objects are now pinned by explicit integer
  formulae, rather than left as open checks.
- **What to do next:** Human-review protocol reductions before using the
  conditional ledger in SNARK claims, and add any query, folding, hash,
  extension-lift, or cryptographic error terms explicitly.

### 2026-06-26 - Tangent-star extremizer barrier

- **Agent/model:** GPT-5.5 Pro tangent-star packet, audited and integrated by
  Codex.
- **Files added or changed:** `experimental/data/tangent-star/`,
  `experimental/experiments.tex`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / NEW-LOCAL / FINITE-SLOPE STRUCTURAL BARRIER.
- **What is being added:** A refinement of the high-agreement tangent
  staircase: in the exact range `3a-2n >= k`, extremal finite-slope
  support-wise `LD_sw` lines are tangent-star lines.  For
  `RS[F_17^32,H,256]`, this rules out a seventh finite-slope bad branch at
  every agreement `a >= 507`.
- **How it is useful:** It closes the previous finite-slope follow-up question
  left by the tangent staircase: no non-tangent mechanism can push the current
  `F_17^32`, `n=512`, `k=256` row past the `506/507` gate under the
  finite-slope support-wise MCA convention.
- **What to do next:** Use the adjacent-ledgers packet for the high-agreement
  CA/projective/curve/list coding objects, and keep protocol, challenge-field,
  extension-lift, folding, query, and cryptographic losses as separate ledgers.

### 2026-06-26 - High-agreement tangent staircase

- **Agent/model:** GPT-5.5 Pro tangent packet, audited and integrated by Codex.
- **Files added or changed:** `experimental/data/tangent/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT / FINITE-SLOPE-THRESHOLD.
- **What is being added:** A generic moving-root tangent floor
  `LD_sw(C,a) >= n-a+1` for Reed--Solomon codes, plus a matching upper bound in
  the very-high-agreement range `3a-2n >= k` using the common code-line
  residual budget.
- **How it is useful:** For `RS[F_17^32,H,256]` with `|H|=512`, this proves
  `LD_sw(C,a)=513-a` for every `a>=427`, so `LD_sw(C,506)=7` and
  `LD_sw(C,507)=6`.  Thus the finite-slope support-wise `2^-128` staircase is
  pinned between agreements `506` and `507`; agreement `353` and the strict352
  quotient-core frontier are superseded by the tangent floor.
- **What to do next:** Human-review the endpoint convention and use the
  adjacent-ledgers packet for the high-agreement CA/projective/curve/list
  coding objects; protocol-facing losses still need separate ledgers.

### 2026-06-26 - L1 d=2 cubic subgroup twisted bound

- **Agent/model:** Scott Hughes PR #121, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_d2_cubic_subgroup_twisted_bound.md`,
  `experimental/notes/triage/l1-prefix-dual-d2-cubic-subgroup-twisted-bound-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_d2_cubic_subgroup_twisted_bound.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / STANDARD-WEIL-INPUT / AUDIT.
- **What is being added:** A `d=2` cubic proper-subgroup collision bound for
  the actual `H^{2k}` object, using exact Fourier reconstruction,
  multiplicative-character expansion of `1_H`, and a conservative
  one-variable mixed character-sum bound.
- **How it is useful:** Separates proper-subgroup counting from full-affine
  Hooley--Katz geometry and gives an L1 template for higher odd-moment twisted
  subgroup bounds.  It is not a new MCA leaderboard row.
- **What to do next:** Pin the imported Katz/Gauss source constants and test
  whether the method extends to higher odd moments with reserve-scale margins.

### 2026-06-26 - L1 odd-moment Hooley-Katz audit

- **Agent/model:** Scott Hughes PR #120, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_odd_moment_projective_geometry.md`,
  `experimental/notes/triage/l1-prefix-dual-odd-moment-hooley-katz-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_odd_moment_hooley_katz_audit.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / IMPORTED-VERIFIED / AUDIT / ROUTE CUT.
- **What is being added:** A projective odd-moment collision-geometry theorem
  for `k>d`, affine-cone conversion, and a Hooley--Katz/Ghorpade--Lachaud
  constant ledger for the full-affine point-count route.
- **How it is useful:** Records why the generic full-affine point-count route
  is not enough for the subgroup L1 reserve-scale problem and prevents ledger
  mixing between full-affine, full-torus, and proper-subgroup counts.
- **What to do next:** Human-check imported theorem citations and use the
  audit as a route cut unless sharper geometry-specific constants are found.

### 2026-06-26 - Strict352 dyadic quotient-core MCA floor audit

- **Agent/model:** Codex, auditing user-supplied strict352 packet.
- **Files added or changed:** `experimental/data/strict352/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / SUPPORT-WISE-MCA-LOWER-BOUND.
- **What is being added:** A dyadic quotient-core proof packet for
  `RS[F_17^32,H,256]`, `|H|=512`, showing `LD_sw(C,a) >= 7` for every
  agreement `264 <= a <= 352`, with `LD_sw(C,352) >= 16` under the
  finite-slope support-wise MCA convention.
- **How it is useful:** Records a quotient-core mechanism for agreements up to
  `352`.  This was briefly the lower-bound frontier, but it is now superseded
  by the generic tangent floor, which gives `LD_sw(C,352) >= 161` and
  `LD_sw(C,353) >= 160`.
- **What to do next:** Keep the packet as a quotient-core mechanism record and
  compare it against any non-tangent mechanisms that might survive past
  agreement `507`.

### 2026-06-26 - Strict264 quotient-floor proof packet

- **Agent/model:** Codex, with user-supplied strict264 packet.
- **Files added or changed:** `experimental/data/strict264/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A strict264 quotient-core proof packet: generated
  field entropy/list-floor notes, a deep-point list-to-MCA conversion section,
  a calculator for entropy/MCA floors, and the concrete
  `RS[F_17^32,H,256]`, `|H|=512`, agreement-264 quotient-floor obstruction.
  The local audit fixed two TeX transcription errors and regenerated the saved
  calculator output with the exact value `log2(17^32)`.
- **How it is useful:** Gives a direct quotient-core route to
  `epsilon_mca(C,31/64)>2^-128`: `binom(64,33)` augmented-code list points
  imply at least nine support-wise bad slopes after the deep-point conversion,
  while seven slopes already clear the `F_17^32` denominator.
- **What to do next:** Keep the theorem package as a quotient-core mechanism
  record.  The moving-root tangent floor supersedes the old strict264/265
  target by giving `LD_sw(C,264) >= 249`.

### 2026-06-26 - Towards-prize finite-threshold theorem section

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** A new `Towards-Prize Finite-Threshold Theorems`
  section for `experiments.tex`: certificate-to-`LD_sw`, fixed-locator
  unique-slope, base-valued subfield confinement, the exact seven-slope
  arithmetic gate over `F_17^32`, and the one-step staircase pinning criterion.
- **How it is useful:** Converts the strict264 and 265 goals into theorem-level
  proof obligations that agents can attack without claiming a new numerator or a
  corrected-reserve MCA theorem.
- **What to do next:** Use the fixed-locator principle to build
  duplicate-aware strict264 and 265 search certificates.

### 2026-06-26 - One-by-one experiment run

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/data/experiment-run-2026-06-26.json`,
  `experimental/notes/triage/experiment-run-2026-06-26.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/updates.json`.
- **Status:** AUDIT / EXPERIMENTAL RUN.
- **What is being added:** A sequential run of the current Cycle120,
  strict264, reserve-ladder, F1, L2, A0, and M2 validators.  All executed
  scripts passed, but no script produced a new retained-slope certificate or
  improved frontier numerator.
- **How it is useful:** Confirms that the current proof infrastructure is
  internally consistent and isolates the exact next strict264 blocker:
  seven explicit retained bad slopes at agreement `264` for the
  `RS[F_17^32,H,256]` row.
- **What to do next:** Build the strict264 seven-slope certificate and an
  independent replayable certificate for the existing `52,747,567,092` count.

### 2026-06-26 - PR #108--#119 proof and audit integration

- **Agent/model:** AllenGrahamHart PRs #108--#112, #114--#118, Scott Hughes
  PRs #113 and #119, reviewed and integrated by Codex with topic-split validity
  checks.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-26.md`,
  `experimental/data/pr-triage-2026-06-26.json`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2}/` and
  `experimental/scripts/`.
- **Status:** PROVED / CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** A one-by-one integration of PRs #108--#119.  The
  theorem-level additions are the F1 syndrome-pencil normal form, the L2
  codegree reduction, the A0 deep-point MCA-cap dependency split, and the M2
  common code-line residual budget.  The remaining material is kept as route
  cuts, audits, or proof programs.
- **How it is useful:** Gives future theory work cleaner local statements for
  F1, L2, Paper D/A0, and M2, while preserving conservative public status.  No
  new prize-worthy numerator or frontier point is claimed.
- **What to do next:** Human-review the theorem-level additions before any
  main-paper promotion, citation-check the mixed-Weil route in PR #119, and
  require a retained-slope proof before treating strict264 as more than a
  target.

### 2026-06-25 - Latest PR integration and estimate audit

- **Agent/model:** AllenGrahamHart PRs #101--#107, ScottDHughes PR #99, and
  Cycle120 audit material from PR #100/#105, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-25.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2,x1}/`,
  `experimental/scripts/`, and `experimental/lean/rs_mca_formalization/`.
- **Status:** AUDIT / EXPERIMENTAL / PROOF-CHECK-NEEDED / CONDITIONAL.
- **What is being added:** A one-by-one integration of PRs #99--#107. The
  Cycle120 numerator is unchanged at `52,747,567,092`; the useful improvements
  are the standalone Cycle120 `LD_sw` proof note, the exact M2
  `epsilon_mca = LD_sw/|F|` bridge, stronger F1 extension-line lower floors,
  an M1 beta-pushforward spectral audit, and sharper L1/L2 proof-program
  targets.
- **How it is useful:** Gives future theory work better normalized estimates
  without editing Papers A--D. In particular, the current ABF-row obstruction
  still points to `epsilon_mca(C,125/256)>2^-128` and the Cycle119 strict
  endpoint `delta*_C <= 249/512`, while L1/L2/F1/X1 now have cleaner
  follow-up notes and standard-library verifiers.
- **What to do next:** Do a human proof review of the standalone Cycle120
  proof chain, then run selected nonmutating verifiers in a controlled pass.
  Treat PR #100's raw generated packet as superseded by the compact audit and
  standalone proof note unless a reviewer explicitly needs the raw replay
  material.

### 2026-06-23 - Cycle119 admissibility review

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus wording cleanup
  in the prior Cycle84 public replay audit.
- **Status:** AUDIT / PROOF-CHECK-NEEDED / COMPUTATION-DEPENDENT.
- **What is being added:** A compact review of the Cycle119 strict-263 claim:
  `LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092`, with `|H|=512`, and an
  admissibility check against the local ABF-aligned definitions and public
  Proximity Prize page.
- **How it is useful:** Separates the potentially important theorem claim from
  Danny's raw/generated PR branch. The branch is not integrable as-is, but the
  two-ended locator transfer is now the right object to demand as a clean proof.
  If the proof and finite computation check out, the right public framing is a
  prize-facing negative counterexample candidate under the printed ABF
  formulation, not an accepted prize solution.
- **What to do next:** Independently fetch and check the ABF PDF, then ask Danny
  for a standalone human-readable proof of the two-ended locator transfer and a
  separate minimal record of the Cycle84 finite computation it consumes.

### 2026-06-23 - Cycle120 ABF counterexample candidate integration

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle120_abf_counterexample_candidate.md`,
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, and `experimental/agents-log.md`.
- **Status:** CONDITIONAL / PROOF-SPINE-CHECKED / COMPUTATION-DEPENDENT /
  SOURCE-AUDIT.
- **What is being added:** A cleaned integration of the Cycle120 ABF-facing
  negative result. It records that Cycle116 agreement `262` is enough for the
  printed ABF closed threshold at `delta=125/256`, while Cycle119 agreement
  `263` checks as a strict-ball strengthening. The note now states explicitly
  that this is only a negative obstruction to
  `epsilon_mca(C,125/256) <= 2^-128` for one row, not ordinary list decoding,
  protocol soundness, or an exact determination of `delta*_C`. It also records
  the endpoint nuance: Cycle116 gives `delta*_C <= 125/256` under a supremum
  convention, while Cycle119 gives `delta*_C <= 249/512 < 125/256`.
- **How it is useful:** Moves the useful part of PR #96 into a compact
  experimental note without importing zips, generated checkers, copied PDFs,
  rendered pages, or raw prompt archives. It gives the project a concrete
  human-review target: the Cycle84/Cycle116 finite proof chain plus the
  optional Cycle119 strict-ball proof.
- **What to do next:** Independently retrieve the ABF PDF, review the finite
  count and fixed-jet transfer, and ask Danny for a minimal nonmutating reviewer
  packet in proof/computation/audit language.

### 2026-06-22 - PR #96-#98 experimental triage

- **Agent/model:** DannyExperiments, avdeevvadim, scottdhughes; integrated by
  Codex.
- **Files added or changed:**
  `experimental/notes/triage/pr-triage-2026-06-22.md`,
  `experimental/notes/m1/m1_cycle84_public_replay_audit.md`,
  `experimental/notes/f1/f1_deep_point_list_to_ca_mca.md`,
  `experimental/scripts/f1_deep_point_list_to_ca_mca_sanity.py`,
  `experimental/notes/l1/l1_prefix_fourier_orbit_cancellation.md`,
  `experimental/scripts/verify_l1_fourier_orbit_cancellation.py`,
  `experimental/SUMMARY.md`, `experimental/README.md`,
  `experimental/scripts/README.md`, and `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE_MODEL_PROOF / PROVED / CONDITIONAL /
  EXPERIMENTAL.
- **What is being added:** A conservative triage of PRs #96--#98. PR #96's
  useful Cycle84 public replay record is kept as an inert audit note:
  `m_max(beta)=2`, `Occ(beta)=52,747,567,092`, `D=24`, twelve double fibers,
  and no fibers of size at least three. PR #97 adds the F1 simple-pole
  deep-point list-to-CA/MCA conversion note and sanity script. PR #98 adds the
  L1 dual-dilation Fourier orbit-kernel reduction note and verifier.
- **How it is useful:** Cycle84 now has a public replay record for the finite
  M1 wall without importing the live workflow or raw archive. The F1 note gives
  a direct special list-to-CA/MCA mechanism to audit against Paper D. The L1
  note moves prefix-local work from individual Fourier frequencies to orbit
  kernels and records a concrete route cut for pointwise kernel saving.
- **What to do next:** Do not treat Cycle84 as a prize-level theorem until a
  transfer theorem is proved. Audit #97 against the exact main-paper `eca` and
  `emca` predicates before any promotion. Run the new scripts only after
  reviewer approval; this triage pass inspected them as text but did not
  execute PR code.

### 2026-06-19 - Experimental folder streamlining

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/README.md`,
  `experimental/notes/README.md`, `experimental/scripts/README.md`,
  `experimental/data/README.md`, plus repository moves under
  `experimental/notes/`, `experimental/scripts/`, `experimental/data/`, and
  `experimental/lean/`.
- **Status:** AUDIT.
- **What is being added:** Reorganized the experimental workspace into four
  durable buckets: notes, scripts, compact data, and Lean. Removed generated
  Python caches and raw/prompt transcript dumps from dated AI-loop outputs.
- **How it is useful:** Future agents now have a small root surface and a clear
  placement policy. Audited summaries and reproducible scripts remain, while
  bulky model-run provenance that was not needed for review is gone.
- **What to do next:** Keep new work inside the existing buckets, update
  `README.md` if a genuinely new bucket is needed, and avoid adding raw
  transcript archives unless they are the only reproducibility record.

### 2026-06-19 - PR #82/#84-#95 experimental integration

- **Agent/model:** AllenGrahamHart, scottdhughes, latifkasuli,
  DannyExperiments PRs, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-19.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/notes/l1/l1_prefix_divisor_count.md`,
  `experimental/notes/l1/l1_quotient_defect_closure.md`,
  `experimental/notes/l1/l1_repaired_locator_theorem_package.md`,
  `experimental/notes/l2/l2_interleaved_dilation_constants.md`,
  the NFB frontier JSON data folder,
  `experimental/notes/m1/m1_residue_line_roadmap.md`, M1 depth-two Kummer notes and
  verifiers, L1/L2 verifier scripts, and the selected
  `experimental/notes/f1/fable-loop/PRZ_REVIEW_INDEX.md` Cycle 49--57 audit
  layer.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT, as
  marked per file.
- **What is being added:** Manual integration of the useful recent PRs:
  PR #93 supersedes #85--#91 as the Scott L1 consolidation; PR #84 adds the
  L1 prefix/divisor/Fourier split; PR #92 adds L2 interleaved dilation and
  quotient-core constants; PR #94 adds a compact `F\B` deep-hole proof
  record; PR #82 adds the M1 low-slack Kummer/depth-two packet; PR #95 is
  integrated only as review index plus cycle audits, not as a raw 225k-line
  archive.
- **How it is useful:** Gives future work clear entry points: L1 quotient
  floors versus aperiodic Fourier cancellation, M1 two-coordinate/conductor
  targets, L2 aligned interleaved constants, an F1/Paper D explicit-line
  proof target, and a compact Fable-loop upper-side route map.
- **What to do next:** Run and review the integrated verifiers, add a
  standalone verifier for the NFB JSON record, audit the M1 Kummer imports
  before consuming constants, and continue the Fable-loop program from the
  high-`j` constant-rate prompt rather than the cut `t=2,j=2` toy regime.

### 2026-06-18 - PR #79-#81 experimental integration

- **Agent/model:** AllenGrahamHart and scottdhughes PRs, integrated by Codex.
- **Files added or changed:** `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_kummer_divisor_geometry.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/l1_arbitrary_fiber_repair.md`,
  `experimental/verify_l1_arbitrary_fiber_repair.py`,
  `experimental/a0_external_import_source_check_20260618.md`,
  `experimental/a0_import_source_probe.py`,
  `experimental/pr-triage-2026-06-18-round3.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL / COUNTEREXAMPLE.
- **What is being added:** Manual integration of PR #79's M1 depth-two
  Kummer-window material, PR #80's L1 arbitrary-fiber repair note, and PR
  #81's A0 external-import source check.  The M1 material is explicitly
  conditional on the isolated Kummer-Weil import; the L1 material repairs a
  false raw-support arbitrary-fiber route; the A0 material records source
  reachability without closing the Paper D import audit.
- **How it is useful:** Narrows three active ledgers without editing Papers
  A--D: M1 gains a sharper lift-window/saturation audit, L1 gets a corrected
  list-object target, and A0 has a reproducible source-access record for the
  universal-cap import chain.
- **What to do next:** Prove or cite the M1 `16p` Kummer estimate, decide
  whether Paper B should promote `ImgFib_U(s)` or another repaired L1 object,
  and obtain the CS25/ABF PDFs needed to close the remaining A0 checks.

### 2026-06-18 - Four-item packet label clarification

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / CLARIFICATION.
- **What is being added:** Adds a self-contained explanation of what the
  AI-packet labels (a)--(d) mean: weak-slack positive regime, finite
  Fermat-prime packet, exponential-field construction, and imported BCHKS
  quotient-locator packet.
- **How it is useful:** Makes the experimental PDF readable without knowing
  the earlier discussion, and separates imported locator material from the
  independent local Paper B divisibility-gate theorem.
- **What to do next:** If the original four-item packet is archived in the
  repo, cross-link this clarification to the exact source file or PR.

### 2026-06-18 - Streamlined imported-locator ledger

- **Agent/model:** Human-provided streamlined note, logged by Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / IMPORTED / WRAPPER / TARGET / NEW-LOCAL.
- **What is being added:** Replaces the narrower attribution note with a
  unified experimental ledger titled *Experimental Theorems and
  Imported-Locator Ledger for RS-MCA*.  The note explicitly imports the
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf quotient-locator construction,
  gives the smooth-quotient notation dictionary, records the shared locator
  identity as imported rather than new, adds a list-fiber pigeonhole wrapper,
  states a slack-two/subfield target for the Paper D route, and preserves the
  Cycle 14--18 Paper B divisibility-gate theorem.
- **How it is useful:** Streamlines promotion decisions for Papers A--D:
  locator proofs from BCHKS must be cited at theorem and proof entry points;
  repository-side contributions are limited to dictionary/wrapper/ledger
  packaging unless separately proved; Paper D gets a precise augmented-code
  and subfield-pigeonhole target; Paper B keeps the independent restricted
  resonance gate as local experimental mathematics.
- **What to do next:** When editing the main papers, add the `BCHKS25`
  bibliography entry and cite Theorems 7.1 and 1.13 exactly where the locator
  construction is used.  Audit the augmented-code rung, slope field
  (`B` versus `F`), locator-codeword distinctness, and slack normalization
  before promoting any wrapper to a theorem.  Continue scanner work on the
  `G==0` divisibility-gate branch for the Paper B resonance window.

### 2026-06-18 - Proximity-gap attribution audit

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / ATTRIBUTION.
- **What is being added:** Records that the AI-generated result (d) should be
  treated as an imported adaptation of Theorem 1.13 of
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf, *On proximity gaps for
  Reed--Solomon codes*, rather than as a new repository contribution.  Also
  records the limitations of items (a)--(c): `1/sqrt(n)` slack, only three
  Fermat primes, and exponential field size.
- **How it is useful:** Gives Papers B/D/C a conservative integration plan:
  cite the external theorem, separate it from the Crites--Stewart import, and
  audit the consumed object before any MCA, line-decoding, or protocol ledger
  claim.
- **What to do next:** Add the bibliographic entry and exact theorem
  cross-reference when the main papers are edited, then verify whether item
  (d) converts to the RS-MCA object actually needed by Paper B.

### 2026-06-18 - PR #78 M1 residual-depth hierarchy

- **Agent/model:** AllenGrahamHart / Codex, integrated by Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_slack_two_depth_two_full_domain.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Integrated Allen's PR #78 M1 residual-depth
  hierarchy: the depth-two/next-slack transition theorem, terminal pure-zero
  residual-depth ledger, first-nonzero frontier partition, full-domain
  slack-two depth-two saturation verifier, and a high-index ceiling for the
  slack-two depth-two frontier.
- **How it is useful:** Separates inherited zero strata from genuinely new
  first-nonzero coefficient images in the M1 canonical-support scanner, giving
  sharper targets for Paper B's corrected MCA residue-line program.
- **What to do next:** Use the new verifier and scanner fields to attack
  proper-subgroup coset-image bounds, especially intermediate-index cases not
  decided by full-domain saturation or the coarse high-index ceiling.

### 2026-06-18 - Experimental theorem note

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** PROVED / HEURISTIC / AUDIT.
- **What is being added:** A standalone LaTeX note collecting restricted
  Cycle 14--18 theorems and heuristics, including the Cycle 18
  divisibility-gate theorem with proof.
- **How it is useful:** Gives the experimental proof material a citable,
  compiled form without editing Papers A--D.
- **What to do next:** Extend the scanner to test the `G==0` gate and decide
  whether any source-valid growing-prime family has two-dimensional slope-map
  image.

### 2026-06-18 - Cycle 18 resonance slope-map reconstruction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/f1/fable-loop/audits/20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/scripts/fable_loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py`,
  `experimental/notes/f1/fable-loop/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROOF-SKETCH / EXACT_NEW_WALL / AUDIT.
- **What is being added:** A local reconstruction of Danny's Cycle 18
  `t=2,j=3` resonance reduction: `Delta` becomes a monic quadratic in
  `tau3`, the alpha component is at most linear, and the non-coprime branch
  reduces to either `Delta1==0` or the graph `tau3=-h/s`. The audit also
  records the divisibility-gate theorem: if the cleared graph polynomial
  `G=s^2 Delta0(tau1,tau2,-h/s)` is nonzero, the branch is already
  curve-sized and contributes only `O(p)` slopes.
- **How it is useful:** Sharpens the Paper B/F1 restricted toy-window wall
  from the Cycle 16 `Q==0` split to a concrete rational slope-map collapse
  question.
- **What to do next:** Extend the Cycle 17 scanner to compute the graph branch
  and projective map image on source-valid split cubics across growing primes,
  with `G==0` as the first exact gate for possible `Theta(p^2)` behavior.

### 2026-06-18 - Paper B counterexample comparison

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/paper_b_counterexample_comparison.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A theory-side comparison between recent
  experimental counterexamples and Paper B's locator-fiber, residue-line,
  extension-field, tangent-floor, and line-decoding statements.
- **How it is useful:** Identifies the raw arbitrary locator-fiber conjecture
  as needing repair, while separating route-cut counterexamples from genuine
  threats to the corrected MCA conjecture.
- **What to do next:** Review the proposed Paper B repairs, especially the
  replacement of raw `Fib_U` by a pruned/full-support arbitrary-word object.

### 2026-06-18 - Experimental summary

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/SUMMARY.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A high-level summary of the recent PR wave and the
  current contents of `experimental/`, organized by how the material advances
  the corrected MCA program.
- **How it is useful:** Gives new agents and human reviewers a map of which
  experimental notes support L1, M1, M2, F1, L2, A0/A1, protocol ledgers, and
  formalization, while keeping proof status conservative.
- **What to do next:** Use the summary as an orientation map, then verify
  individual claims from their source notes and scripts before promotion.

### 2026-06-18 - New PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #67,
  #69, #70, #71, #72, #73, #74, #75, and #77; recorded #68 and #76 as
  superseded by #77; added `experimental/pr-triage-2026-06-18.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** Second open-PR triage pass covering M1, F1, L2,
  M2, L1, A1, Fable-loop, and locator-fiber cross-check contributions.
- **How it is useful:** Banks useful experimental notes, verifiers, scanners,
  and audit provenance while preserving the rule that main papers remain
  unchanged and new material stays in `experimental/`.
- **What to do next:** Run full verifier coverage, review mathematical claims
  before promotion, and close the source PRs as manually integrated or
  superseded once this commit is pushed.

### 2026-06-17 - Open PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #1,
  #2, #3, and #46 through #66; added
  `experimental/pr-triage-2026-06-17.md`; renamed PR #55's dither scanner to
  `experimental/quotient_profile_dither.py` with matching `.md` note.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** One-by-one triage of the open PR queue and local
  integration of accepted experimental notes, scanners, proof records, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
### 2026-07-03 - M1 a327 bounded-cycle carrier hypergraph search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_bounded_cycle_carrier_hypergraph_search.md`,
  `experimental/scripts/scan_m1_a327_bounded_cycle_carrier_hypergraph_search.py`,
  `experimental/scripts/verify_m1_a327_bounded_cycle_carrier_hypergraph_search.py`,
  `experimental/scripts/audit_m1_a327_bounded_cycle_carrier_hypergraph_search.sage`,
  `experimental/data/m1_a327_bounded_cycle_carrier_hypergraph_search.json`,
  `experimental/agents-log.md`.
- **Status:** CONSTRUCTION_FAIL / BOUNDED_CYCLE_COUNT_INFEASIBLE / PARTIAL /
  EXPERIMENTAL for the first-pass graph set.
- **What is being added:** A bounded-cycle carrier graph search that replaces
  the impossible six-edge connected-subtree tree route with 7-9 edge carrier
  graphs. The scanner enforces support, pair-cap, pair-7 guard, and edge-load
  constraints; the Sage audit tests the compressed edge-divisibility lift with
  cycle constraints over `GF(17^32)`.
- **How it is useful:** Turns the connected-subtree incidence obstruction into
  a next-level construction/audit route with enough carrier capacity while
  retaining a small exact lift.
- **What to do next:** Widen the carrier-graph generator or relax the bounded
  carrier model before returning to exact edge-divisibility lifting. Keep the
  result strictly on the INTERLEAVED_LIST track unless a Sage proof record is
  produced.
### 2026-07-03 - M1 a327 selected-class rank-defect search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_selected_class_rank_defect_search.md`,
  `experimental/scripts/scan_m1_a327_selected_class_rank_defect_search.py`,
  `experimental/scripts/verify_m1_a327_selected_class_rank_defect_search.py`,
  `experimental/scripts/audit_m1_a327_selected_class_rank_defect_search.sage`,
  `experimental/data/m1_a327_selected_class_rank_defect_search.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RANK_DEFECT_PROXY_FULL_RANK /
  PARTIAL / EXPERIMENTAL for the first-pass proxy scan.
- **What is being added:** A selected-class quotient-rank search that treats
  positive nullity of the `1777 x 1536` quotient matrix as the primary design
  target. The Python scanner emits candidate selected-class designs; the Sage
  audit ranks them over a proxy field with a 512-subgroup and is gated to exact
  `GF(17^32)` only for proxy-positive designs.
- **How it is useful:** Converts the latest obstruction into a constructive
  rank-defect objective instead of another carrier-graph patch.
- **What to do next:** Engineer stronger dependency structure before returning
  to exact lifting; only run `GF(17^32)` when a proxy rank-defect candidate
  appears. Keep the packet strictly INTERLEAVED_LIST.
### 2026-07-03 - M1 a327 low-rank template selected-class search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_lowrank_template_selected_class_search.md`,
  `experimental/scripts/scan_m1_a327_lowrank_template_selected_class_search.py`,
  `experimental/scripts/verify_m1_a327_lowrank_template_selected_class_search.py`,
  `experimental/scripts/audit_m1_a327_lowrank_template_selected_class_search.sage`,
  `experimental/data/m1_a327_lowrank_template_selected_class_search.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / LOWRANK_TEMPLATE_PROXY_POSITIVE / PARTIAL /
  EXPERIMENTAL.
- **What is being added:** A selected-class construction branch that replaces
  generic witness differences by low-rank coefficient templates
  `P_i=v_i dot A`. The scanner minimizes affine-rank equation cost per
  selected class, and the Sage audit ranks proxy matrices before exact
  `GF(17^32)` lifting.
- **How it is useful:** Directly engineers rank defect into the codeword
  parameterization rather than hoping generic selected-class matrices lose
  rank. The first proxy audit found `8` proxy-positive candidates; the best
  `mixed_rank6` candidate has proxy rank/nullity `1280/256`.
- **What to do next:** If the proxy audit finds positive nullity, bank that
  result first; run exact `GF(17^32)` rank as an explicit follow-on with a
  timeout/batching plan.
### 2026-07-03 - M1 a327 low-rank template exact audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_lowrank_template_exact_audit.md`,
  `experimental/scripts/scan_m1_a327_lowrank_template_exact_audit.py`,
  `experimental/scripts/verify_m1_a327_lowrank_template_exact_audit.py`,
  `experimental/scripts/audit_m1_a327_lowrank_template_exact_audit.sage`,
  `experimental/data/m1_a327_lowrank_template_exact_audit.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / LOWRANK_EXACT_TIMEOUT / PARTIAL / EXPERIMENTAL.
- **What is being added:** A focused exact-audit packet for the best
  `mixed_rank6` proxy-positive low-rank template candidate from `e56f3ad`.
  The scanner extracts the coordinate ledger, row specs, and template vectors;
  the Sage audit builds the compressed low-rank exact matrix and computes exact
  `GF(17^32)` rank/nullity if the dense rank step completes.
- **How it is useful:** Separates the exact-field bottleneck from the broader
  low-rank template search and makes the next proof/no-proof gate explicit.
- **What happened:** A bounded Sage rank-only run reached the dense
  `matrix.rank()` step and was interrupted before rank returned.
- **What to do next:** Build a faster exact-rank path for the compressed
  `1533 x 1536` low-rank matrix; if nullity is positive, continue to
  pair-projection and deterministic kernel sampling.
### 2026-07-03 - M1 a327 low-rank template kernel extraction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_lowrank_template_kernel_extraction.md`,
  `experimental/scripts/scan_m1_a327_lowrank_template_kernel_extraction.py`,
  `experimental/scripts/verify_m1_a327_lowrank_template_kernel_extraction.py`,
  `experimental/scripts/audit_m1_a327_lowrank_template_kernel_extraction.sage`,
  `experimental/data/m1_a327_lowrank_template_kernel_extraction.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / LOWRANK_KERNEL_SQUARE_SOLVE_TIMEOUT / PARTIAL / EXPERIMENTAL.
- **What is being added:** A kernel-extraction packet for the `mixed_rank6`
  low-rank selected-class candidate. It tries square free-column solves and an
  evaluation-basis sparse formulation rather than first computing dense exact
  rank over `GF(17^32)`.
- **How it is useful:** Converts the next proof gate from monolithic rank to
  explicit kernel-vector construction plus raw selected-class certification.
- **What happened:** The metadata pass confirmed the compressed coefficient
  matrix shape `1533 x 1536`. A bounded square free-column solve reached
  `solve_right` and was interrupted in the submatrix rank/echelonization step.
- **What to do next:** Try the evaluation-basis sparse solve or an external
  exact linear algebra backend for the square solve. If a vector is
  constructed, check all 1777 raw rows, seven-codeword distinctness, and the
  agreement vector directly on `H`.
### 2026-07-03 - M1 a327 low-rank functional-divisibility lift

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_lowrank_template_functional_divisibility_lift.md`,
  `experimental/scripts/scan_m1_a327_lowrank_template_functional_divisibility_lift.py`,
  `experimental/scripts/verify_m1_a327_lowrank_template_functional_divisibility_lift.py`,
  `experimental/scripts/audit_m1_a327_lowrank_template_functional_divisibility_lift.sage`,
  `experimental/data/m1_a327_lowrank_template_functional_divisibility_lift.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / FUNC_DIV_METADATA / PARTIAL / EXPERIMENTAL.
- **What is being added:** A functional-divisibility compression of the
  `mixed_rank6` selected-class system. It groups compressed low-rank rows by
  projective functional and replaces pointwise rows by polynomial divisibility
  constraints.
- **Current ledger:** 15 functional classes, 2 forced functional identities,
  2327 quotient variables, estimated functional-divisibility matrix shape
  `3840 x 3863`, and formal full-space nullity lower bound 23.
- **How it is useful:** Shows the row structure is highly repeated and gives a
  proof-oriented formulation for extracting useful `A` components rather than
  treating the `1533 x 1536` coefficient matrix as dense.
- **What to do next:** Extract a nondegenerate `A` component from the
  functional-divisibility system and certify it against all 1777 raw selected
  rows before checking distinctness and agreement.
### 2026-07-03 - M1 a327 low-rank functional-basis extraction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_lowrank_functional_basis_extraction.md`,
  `experimental/scripts/scan_m1_a327_lowrank_functional_basis_extraction.py`,
  `experimental/scripts/verify_m1_a327_lowrank_functional_basis_extraction.py`,
  `experimental/scripts/audit_m1_a327_lowrank_functional_basis_extraction.sage`,
  `experimental/data/m1_a327_lowrank_functional_basis_extraction.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / FUNC_BASIS_PAIR_FORCED_BY_FORCED_IDENTITIES / PARTIAL / EXPERIMENTAL.
- **What is being added:** A forced-identity saturation and functional-basis
  extraction audit for the `mixed_rank6` functional-divisibility candidate.
- **Result:** Saturation raises the forced functional rank to 5, reduces the
  template space to dimension 1, leaves 0 projected functional classes, and
  forces all 21 witness pairs equal.
- **How it is useful:** Converts the previous formal full-space nullity into a
  precise local obstruction: the nullity is not useful for a seven-distinct
  witness because the saturated forced identities annihilate all witness
  template differences.
- **What to do next:** Repair the low-rank template search objective so
  candidates are filtered by forced-identity saturation and pair projections
  before any exact `GF(17^32)` lifting.
### 2026-07-03 - M1 a327 low-rank template forced-identity repair

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_lowrank_template_forced_identity_repair.md`,
  `experimental/scripts/scan_m1_a327_lowrank_template_forced_identity_repair.py`,
  `experimental/scripts/verify_m1_a327_lowrank_template_forced_identity_repair.py`,
  `experimental/scripts/audit_m1_a327_lowrank_template_forced_identity_repair.sage`,
  `experimental/data/m1_a327_lowrank_template_forced_identity_repair.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / LOWRANK_REPAIR_SATURATION_PASS / PARTIAL / EXPERIMENTAL.
- **What is being added:** A forced-identity saturation filter for low-rank
  template candidates before exact lifting.
- **Result:** Tested 10 existing low-rank systems; 8 were proxy-positive and 2
  survived saturation. The survivor family is `random_matroid_seeded_0_m6`,
  with reduced template dimension 6 and no forced pair equality.
- **How it is useful:** Turns the `mixed_rank6` obstruction into a reusable
  template-search filter and identifies the next exact-lift target.
- **What to do next:** Run functional-divisibility / exact-lift extraction on
  the `random_matroid_seeded_0_m6` survivor, not on `mixed_rank6`.
### 2026-07-03 - M1 a327 random-matroid functional lift

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_random_matroid_functional_lift.md`,
  `experimental/scripts/scan_m1_a327_random_matroid_functional_lift.py`,
  `experimental/scripts/verify_m1_a327_random_matroid_functional_lift.py`,
  `experimental/scripts/audit_m1_a327_random_matroid_functional_lift.sage`,
  `experimental/data/m1_a327_random_matroid_functional_lift.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / RANDOM_MATROID_FUNC_LIFT_EXACT_TIMEOUT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** Functional-divisibility lift target for the
  `random_matroid_seeded_0_m6` survivor from `68a0780`.
- **Result:** Reconstructed the survivor, found 35 functional classes with no
  forced functional identities, functional span rank 5, and a best
  `max_support_basis` quotient matrix of shape `1211 x 714`. Proxy rank over
  `GF(12289)` is full, `714 / 0`. An exact Sage rank attempt over `GF(17^32)`
  was interrupted after stalling in echelonization.
- **How it is useful:** Moves the exact target away from `mixed_rank6`, exposes
  the rank-5 functional-span structure, and gives a concrete smaller exact
  matrix for the next infrastructure or rank-feedback move.
- **What to do next:** Do not run a longer blind Sage rank first; try further
  functional quotient reduction, alternative basis profiles, or an
  evaluation/Fourier-basis sparse exact route.
### 2026-07-03 - M1 a327 random-matroid rank-feedback v2

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_random_matroid_rank_feedback_v2.md`,
  `experimental/scripts/scan_m1_a327_random_matroid_rank_feedback_v2.py`,
  `experimental/scripts/verify_m1_a327_random_matroid_rank_feedback_v2.py`,
  `experimental/data/m1_a327_random_matroid_rank_feedback_v2.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded proxy-rank feedback search around the
  `random_matroid_seeded_0_m6` functional-lift target from `3d6bfd4`.
- **Result:** Tested 7 templates and 14 systems, proxy-ranked 6 systems over
  `GF(12289)`, and found 0 proxy-positive candidates. The best candidate,
  `random_matroid_feedback_seed_1_m6`, repairs the functional span to rank 6
  with no annihilator but has quotient proxy rank/nullity `1086 / 0`.
- **How it is useful:** Separates the span-rank repair problem from the quotient
  nullity problem. Nearby random-matroid mutations can fix the rank-5 span, but
  the tested proxy quotients remain full rank.
- **What to do next:** Bias the next generator directly toward quotient nullity
  and dependent nonbasis constraints before running any exact `GF(17^32)` Sage
  audit.
### 2026-07-03 - M1 a327 random-matroid rank-feedback v3

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_random_matroid_rank_feedback_v3.md`,
  `experimental/scripts/scan_m1_a327_random_matroid_rank_feedback_v3.py`,
  `experimental/scripts/verify_m1_a327_random_matroid_rank_feedback_v3.py`,
  `experimental/data/m1_a327_random_matroid_rank_feedback_v3.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A broader proxy-only rank-feedback sweep around the
  random-matroid template family, with hard structural filters and multiple
  basis profiles per proxy-ranked candidate.
- **Result:** Tested 24 templates and 96 systems. 84 systems passed structural
  filters, 8 candidates and 16 basis profiles were proxy-ranked over
  `GF(12289)`, and 0 proxy-positive candidates were found. The best candidate,
  `random_matroid_v3_seed_017_m6`, has functional span rank 6, no annihilator,
  pair7 counts `[233,233,233,233,233]`, and proxy rank/nullity `1348 / 0`.
- **How it is useful:** Confirms that the random-matroid neighborhood has many
  structurally valid systems, but the tested quotient matrices remain full rank.
- **What to do next:** Either build a proxy-nullity-aware generator that
  engineers dependent nonbasis constraints, or bank a rank-rigidity audit for
  the tested random-matroid template family.
### 2026-07-03 - M1 a327 random-matroid rank-rigidity audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_random_matroid_rank_rigidity_audit.md`,
  `experimental/scripts/scan_m1_a327_random_matroid_rank_rigidity_audit.py`,
  `experimental/scripts/verify_m1_a327_random_matroid_rank_rigidity_audit.py`,
  `experimental/data/m1_a327_random_matroid_rank_rigidity_audit.json`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / RANK_RIGIDITY_PROXY_FRONT / PARTIAL / EXPERIMENTAL.
- **What is being added:** A finite audit of the 16 proxy basis profiles tested
  in the v3 random-matroid rank-feedback branch.
- **Result:** All 16 audited proxy basis profiles are full column rank over
  `GF(12289)`, with 0 proxy-positive profiles and uniform row surplus 241.
- **How it is useful:** Clarifies that the tested proxy front is failing at the
  quotient-rank layer, not at support, pair-guard, forced-identity, or span-rank
  filters.
- **What to do next:** Move to a dependency-engineered generator, or formulate
  the repeated full-rank phenomenon as a module/syzygy/determinantal proxy where
  Macaulay2, Singular, or `msolve` can add leverage.
### 2026-07-03 - M1 a327 dependency-engineered rank feedback

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_dependency_engineered_rank_feedback.md`,
  `experimental/scripts/scan_m1_a327_dependency_engineered_rank_feedback.py`,
  `experimental/scripts/verify_m1_a327_dependency_engineered_rank_feedback.py`,
  `experimental/data/m1_a327_dependency_engineered_rank_feedback.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / DEPENDENCY_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A Python/NumPy proxy search that engineers coordinate
  assignments to create duplicate and nested functional support sets before
  quotient-rank testing.
- **Result:** Tested 18 templates and 108 systems. 96 systems passed structural
  filters, 8 candidates and 24 basis profiles were proxy-ranked over
  `GF(12289)`, and 0 proxy-positive candidates were found. The best candidate,
  `random_matroid_v3_seed_007_m6`, has duplicate support groups 14, duplicate
  support pairs 51, nested support pairs 66, and proxy rank/nullity `1385 / 0`.
- **How it is useful:** Shows support-set dependency can be engineered, but the
  tested nonbasis quotient rows remain independent over the proxy field.
- **What to do next:** Either engineer dependencies directly in quotient-row
  coordinates, or move to the Macaulay2/Singular module-syzygy proxy branch.
### 2026-07-03 - M1 a327 random-matroid syzygy-rigidity proxy

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_random_matroid_syzygy_rigidity_proxy.md`,
  `experimental/scripts/scan_m1_a327_random_matroid_syzygy_rigidity_proxy.py`,
  `experimental/scripts/verify_m1_a327_random_matroid_syzygy_rigidity_proxy.py`,
  `experimental/scripts/m2_m1_a327_random_matroid_syzygy_rigidity_proxy.m2`,
  `experimental/data/m1_a327_random_matroid_syzygy_rigidity_proxy.json`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / SYZYGY_RIGIDITY_PROXY / PARTIAL / EXPERIMENTAL.
- **What is being added:** A Macaulay2 module/syzygy proxy for the best
  dependency-engineered profile.
- **Result:** The extracted nonbasis coefficient matrix is `41 x 6` over
  `GF(12289)`. Macaulay2 reports rank 6, right-kernel generators 0, and
  left-syzygy rank 35. The associated full quotient remains `1626 x 1385` with
  proxy rank/nullity `1385 / 0`.
- **How it is useful:** Shows that the current dependencies are row-side
  syzygies, not right-kernel relations capable of producing quotient nullity.
- **What to do next:** Engineer right-kernel relations directly in the nonbasis
  coefficient presentation before expanding polynomial evaluation factors.
### 2026-07-03 - M1 a327 right-kernel-engineered rank feedback

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_right_kernel_engineered_rank_feedback.md`,
  `experimental/scripts/scan_m1_a327_right_kernel_engineered_rank_feedback.py`,
  `experimental/scripts/verify_m1_a327_right_kernel_engineered_rank_feedback.py`,
  `experimental/data/m1_a327_right_kernel_engineered_rank_feedback.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RIGHT_KERNEL_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A Python finite-field screen that tries to choose
  basis profiles whose nonbasis coefficient presentation has a right kernel
  before quotient evaluation factors are expanded.
- **Result:** Tested 18 templates and 108 systems. 96 candidates passed the
  structural filters, 3,276 coefficient profiles were checked, and 0
  right-kernel-positive profiles were found. The best candidate is
  `random_matroid_v3_seed_010_m6` with `signature_fiber_blocks`,
  support `[327,327,327,327,327,327,327]`, pair7 counts
  `[233,233,233,233,233]`, max pair count 233, and 45 functional classes.
- **How it is useful:** Moves the obstruction earlier than quotient proxy rank:
  the tested generator still cannot create a nontrivial right-kernel relation
  in the nonbasis coefficient matrix.
- **What to do next:** Build the coefficient relation first by prescribing a
  right-kernel vector or low-rank coefficient subspace, then fit selected-class
  supports around that relation.
### 2026-07-03 - M1 a327 prescribed right-kernel selected-class search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_prescribed_right_kernel_selected_class_search.md`,
  `experimental/scripts/scan_m1_a327_prescribed_right_kernel_selected_class_search.py`,
  `experimental/scripts/verify_m1_a327_prescribed_right_kernel_selected_class_search.py`,
  `experimental/scripts/m2_m1_a327_prescribed_right_kernel_selected_class_search.m2`,
  `experimental/data/m1_a327_prescribed_right_kernel_selected_class_search.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL.
- **What is being added:** A prescribed-kernel functional proxy that preserves
  structurally valid selected-class support ledgers while forcing nonbasis
  coefficient rows into a chosen right-kernel hyperplane.
- **Result:** Tested 18 templates and 108 systems. 96 candidates passed
  structural filters, 6,912 engineered profiles were formed, 96 candidates had
  right-kernel-positive engineered profiles, and 12/12 proxy-ranked candidates
  were proxy-positive. The best target has coefficient rank/right-kernel nullity
  `5 / 1`, Macaulay2 right-kernel generators 1, and proxy quotient
  rank/nullity `687 / 166`.
- **How it is useful:** Shows that a prescribed coefficient right-kernel can
  survive quotient expansion at the proxy level.
- **What to do next:** Realize the prescribed basis-coordinate rows by actual
  template vectors and selected classes. Until that realization exists, this is
  a synthetic functional proxy target, not a Sage exact-lift candidate.
### 2026-07-03 - M1 a327 prescribed-kernel template realization

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_prescribed_kernel_template_realization.md`,
  `experimental/scripts/scan_m1_a327_prescribed_kernel_template_realization.py`,
  `experimental/scripts/verify_m1_a327_prescribed_kernel_template_realization.py`,
  `experimental/data/m1_a327_prescribed_kernel_template_realization.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / TEMPLATE_REALIZATION_ROWSPACE_FAIL / PARTIAL / EXPERIMENTAL.
- **What is being added:** A `GF(17)` linear realization audit asking whether
  the prescribed right-kernel functional rowspaces can come from actual seven
  template vectors.
- **Result:** The realization matrix is `4193 x 42` with rank/nullity `35 / 7`.
  The diagonal translation space has rank 6 and lies in the kernel, leaving one
  non-diagonal direction. That direction does not realize the prescribed
  rowspaces: 263 samples, 0 rowspace-valid samples, best realized functional
  span rank 5, and 90 coordinate rowspace failures in the representative.
- **How it is useful:** Separates the new obstruction from proxy quotient rank:
  prescribed coefficient right kernels can create proxy nullity, but this
  projected target is not realizable by actual template-vector affine
  difference spaces.
- **What to do next:** Search template vectors and right-kernel relations
  jointly, with rowspace-realization constraints inside the generator rather
  than projecting existing functional rows after the fact.
### 2026-07-03 - M1 a327 joint template right-kernel search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_joint_template_right_kernel_search.md`,
  `experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py`,
  `experimental/scripts/verify_m1_a327_joint_template_right_kernel_search.py`,
  `experimental/scripts/m2_m1_a327_joint_template_right_kernel_search.m2`,
  `experimental/data/m1_a327_joint_template_right_kernel_search.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / JOINT_TEMPLATE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A joint actual-template/right-kernel proxy search
  using rank-5 hyperplane templates with controlled outside directions.
- **Result:** Tested 36 templates and 216 systems. 210 candidates passed
  structural filters, 6 actual-template candidates had coefficient right
  kernels, and 6 candidates were proxy-ranked. All proxy quotient matrices were
  full rank. The best candidate has coefficient rank/right-kernel nullity
  `5 / 1`, Macaulay2 right-kernel generators 1, and proxy quotient
  rank/nullity `277 / 0`.
- **How it is useful:** Reaches the original objective's fallback case with
  actual template vectors: the coefficient right kernel exists, but
  polynomial evaluation / vanishing-factor expansion destroys it.
- **What to do next:** Model the `Z_lambda` expansion directly and search for
  right-kernel relations stable under basis vanishing-factor multiplication, or
  formalize this as the next rank-rigidity obstruction for the tested
  one-outside rank-5 hyperplane family.
### 2026-07-03 - M1 a327 Z_lambda expansion-stability audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_zlambda_expansion_stability_audit.md`,
  `experimental/scripts/scan_m1_a327_zlambda_expansion_stability_audit.py`,
  `experimental/scripts/verify_m1_a327_zlambda_expansion_stability_audit.py`,
  `experimental/data/m1_a327_zlambda_expansion_stability_audit.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / ZEXP_EXPANSION_UNSTABLE / PARTIAL / EXPERIMENTAL.
- **What is being added:** A stability audit for the actual-template
  coefficient right kernels found in `b3d6a79`, testing whether they survive
  the `Z_lambda` basis vanishing-factor expansion.
- **Result:** Audited 30 right-kernel profiles. All 30 have coefficient
  kernels over GF(17), and 6 also have coefficient kernels over GF(12289), but
  zero profiles are stable lift targets. The best profile has coefficient
  rank/nullity `5 / 1`, basis-zero union size 327, stable common multiplier
  dimension 0, and 15 forced pair equalities.
- **How it is useful:** Confirms that the obstruction has moved from
  coefficient right-kernel existence to `Z_lambda` expansion stability and pair
  projection nondegeneracy.
- **What to do next:** Generate actual-template candidates whose right-kernel
  relations have basis-zero union size at most 255 and no forced pair
  projections before running proxy quotient rank.
### 2026-07-03 - M1 a327 Z_lambda-stable right-kernel generator

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_zlambda_stable_right_kernel_generator.md`,
  `experimental/scripts/scan_m1_a327_zlambda_stable_right_kernel_generator.py`,
  `experimental/scripts/verify_m1_a327_zlambda_stable_right_kernel_generator.py`,
  `experimental/data/m1_a327_zlambda_stable_right_kernel_generator.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / ZSTABLE_BASIS_UNION_TOO_LARGE / PARTIAL / EXPERIMENTAL.
- **What is being added:** A stability-aware actual-template generator that
  ranks basis choices by `Z_lambda` zero-set union before attempting proxy
  quotient rank.
- **Result:** Tested 216 systems and 13,440 low-union basis profiles. 30
  profiles had coefficient right kernels, but zero had stable basis-zero union
  and zero had pair-projection-clear lift targets. The best profile remains the
  `single_outside_w7_v1` pattern with coefficient rank/nullity `5 / 1`, union
  size 327, stable common multiplier dimension 0, and 15 forced pair
  equalities.
- **How it is useful:** Shows that in the current actual-template family, the
  low-union basis front is coefficient-full-rank; right kernels only appear
  after the zero-set union is already too large for stable multiplication.
- **What to do next:** Build the stability relation first: prescribe a
  basis-zero union of size at most 255, impose a coefficient right kernel and
  nonzero pair projections there, then fit selected-class supports around it.
### 2026-07-03 - M1 a327 Z_lambda stable-basis relation search

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_zlambda_stable_basis_relation_search.md`,
  `experimental/scripts/scan_m1_a327_zlambda_stable_basis_relation_search.py`,
  `experimental/scripts/verify_m1_a327_zlambda_stable_basis_relation_search.py`,
  `experimental/data/m1_a327_zlambda_stable_basis_relation_search.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / ZREL_STABLE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A relation-first stable-basis search that only tests
  basis profiles with `Z_lambda` zero-set union at most 255 before asking for a
  coefficient right kernel.
- **Result:** The 36-template actual-template family has 23,663,322 stable
  basis combinations across 216 systems. The bounded stable front tested 12,312
  independent stable basis profiles and found zero coefficient-kernel profiles,
  zero pair-projection-clear profiles, and zero proxy candidates.
- **How it is useful:** Separates the obstruction from merely choosing too many
  large-union bases: stable bases exist, but this actual-template family does
  not place the nonbasis coordinate rows into a right-kernel hyperplane on
  those stable bases.
- **What to do next:** Prescribe the stable right-kernel relation itself first,
  then generate nonbasis functionals and selected-class support schedules around
  that relation.
### 2026-07-03 - M1 a327 prescribed Z_lambda-stable relation generator

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_prescribed_zlambda_stable_relation_generator.md`,
  `experimental/scripts/scan_m1_a327_prescribed_zlambda_stable_relation_generator.py`,
  `experimental/scripts/verify_m1_a327_prescribed_zlambda_stable_relation_generator.py`,
  `experimental/data/m1_a327_prescribed_zlambda_stable_relation_generator.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / PZREL_PROXY_PENDING / PARTIAL / EXPERIMENTAL.
- **Realization status:** SYNTHETIC_FUNCTIONAL_PROXY_TARGET.
- **What is being added:** A prescribed stable-relation generator that imposes
  a right-kernel relation on stable bases before proxy rank and filters out
  forced pair projections.
- **Result:** Tested 216 systems and 14,310 engineered profiles. Found 1,770
  pair-projection-clear synthetic targets. The best has basis-zero union size
  85, stable common multiplier dimension 171, coefficient rank/nullity `5 / 1`,
  and no forced pair equalities.
- **How it is useful:** Produces the first stable-relation target satisfying
  the intended right-kernel and pair-projection gates, but only at the synthetic
  functional level.
- **What to do next:** Run a single-case proxy quotient rank for the best target
  with a timeout, then, only if proxy-positive, attempt actual template-vector
  realization.
### 2026-07-03 - M1 a327 prescribed Z_lambda-stable proxy audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_prescribed_zlambda_stable_proxy_audit.md`,
  `experimental/scripts/audit_m1_a327_prescribed_zlambda_stable_proxy.py`,
  `experimental/scripts/verify_m1_a327_prescribed_zlambda_stable_proxy_audit.py`,
  `experimental/data/m1_a327_prescribed_zlambda_stable_proxy_audit.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PZREL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **Realization status:** SYNTHETIC_FUNCTIONAL_PROXY_TARGET.
- **What is being added:** A single-case proxy quotient audit for the best
  prescribed stable-relation target from `70b744e`.
- **Result:** The target retained basis-zero union size 85, stable common
  multiplier dimension 171, coefficient rank/nullity `5 / 1`, and zero forced
  pair equalities. The GF(12289) proxy quotient matrix had shape `1691 x 1450`
  and rank/nullity `1450 / 0`.
- **How it is useful:** Shows that coefficient-level stable relations and
  pair-projection clearance are still not enough; the `Z_lambda` expanded proxy
  quotient relation itself must be engineered.
- **What to do next:** Build a proxy-kernel-prescribed generator that targets
  nullity in the expanded quotient matrix directly, while preserving stable
  basis union and pair-projection nondegeneracy.
### 2026-07-03 - M1 a327 proxy-slot kernel generator

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_proxy_slot_kernel_generator.md`,
  `experimental/scripts/scan_m1_a327_proxy_slot_kernel_generator.py`,
  `experimental/scripts/verify_m1_a327_proxy_slot_kernel_generator.py`,
  `experimental/data/m1_a327_proxy_slot_kernel_generator.json`,
  `experimental/agents-log.md`.
- **Status:** CANDIDATE / PSLOT_PROXY_KERNEL_TARGET / PARTIAL / EXPERIMENTAL.
- **Realization status:** SYNTHETIC_FUNCTIONAL_PROXY_TARGET.
- **What is being added:** A proxy-slot kernel generator that engineers a
  single stable basis coordinate to vanish across all nonbasis rows, making one
  `Q` block a guaranteed kernel block of the expanded proxy quotient matrix.
- **Result:** Tested 216 systems, 12,312 stable basis profiles, and 73,872 slot
  profiles. Found 42 pair-projection-clear proxy-slot kernel targets. The best
  target has stable basis-zero union size 10, coefficient rank/nullity `5 / 1`,
  no forced pair equalities, and a guaranteed proxy nullity lower bound of 253.
  Macaulay2 independently checks the `21 x 6` coefficient matrix with rank 5
  and one right-kernel generator. Direct GF(12289) proxy audit gives matrix
  shape `1761 x 1520` and rank/nullity `1267 / 253`.
- **How it is useful:** This is the first expanded-proxy-positive target after
  the `Z_lambda` full-rank obstruction. It proves the next obstruction is no
  longer proxy nullity in the synthetic functional model, but realization of
  the prescribed functional coefficients as an exact template/lift.
- **What to do next:** Attempt actual template-vector realization for the
  `sheared_outside_seed_001` slot-kernel target, then run Sage GF(17^32) only
  after that realization gate is cleared.
### 2026-07-03 - M1 a327 proxy-slot template realization

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_proxy_slot_template_realization.md`,
  `experimental/scripts/scan_m1_a327_proxy_slot_template_realization.py`,
  `experimental/scripts/verify_m1_a327_proxy_slot_template_realization.py`,
  `experimental/data/m1_a327_proxy_slot_template_realization.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / TEMPLATE_REALIZATION_ROWSPACE_FAIL / PARTIAL / EXPERIMENTAL.
- **What is being added:** A GF(17) template-vector realization audit for the
  `sheared_outside_seed_001` proxy-slot functional target from `ce5589c`.
- **Result:** The realization matrix has shape `4191 x 42`, rank/nullity
  `35 / 7`, diagonal rank 6, and one non-diagonal direction modulo diagonal
  translation. A 519-sample kernel sweep found zero rowspace-valid samples. The
  best distinct sample has realized functional span rank 5 and fails the
  prescribed rowspace at 3 coordinates.
- **How it is useful:** The synthetic proxy-slot target remains genuinely
  proxy-positive, but this named target is not directly realized by actual
  low-rank template vectors in the tested coordinate ledger.
- **What to do next:** Build a realization-aware proxy-slot generator that
  keeps actual template-vector rowspaces inside the search, instead of
  engineering the proxy functional rows first and realizing them afterward.
### 2026-07-03 - M1 a327 realization-aware proxy-slot generator

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_realization_aware_proxy_slot_generator.md`,
  `experimental/scripts/scan_m1_a327_realization_aware_proxy_slot_generator.py`,
  `experimental/scripts/verify_m1_a327_realization_aware_proxy_slot_generator.py`,
  `experimental/data/m1_a327_realization_aware_proxy_slot_generator.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RAWARE_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL.
- **What is being added:** An actual-template-only proxy-slot scan that accepts
  a slot kernel only if it is already present in realized template-vector
  rowspaces, with no synthetic rowspace edits.
- **Result:** Tested 216 systems, 12,312 stable basis profiles, and 73,872 slot
  profiles. Found zero actual zero-slot profiles and zero pair-projection-clear
  actual slots. The closest profile is `single_outside_w7_v3` /
  `signature_fiber_blocks`, basis `slot_union_142_5_7_9_11_13_17`, with only 2
  nonzero rows in the candidate slot, but coefficient rank/nullity `6 / 0` and
  15 forced pair equalities.
- **How it is useful:** Confirms that the proxy-slot kernel mechanism is not
  already present in the bounded actual-template stable-basis front. The next
  useful target is a near-miss repair that kills the two residual slot
  coefficients while preserving pair projections.
- **What to do next:** Start a focused near-miss repair branch around
  `single_outside_w7_v3` / `slot_union_142_5_7_9_11_13_17`, rather than
  broadening random mutation immediately.
### 2026-07-03 - M1 a327 realized-slot near-miss repair

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_realized_slot_nearmiss_repair.md`,
  `experimental/scripts/scan_m1_a327_realized_slot_nearmiss_repair.py`,
  `experimental/scripts/verify_m1_a327_realized_slot_nearmiss_repair.py`,
  `experimental/data/m1_a327_realized_slot_nearmiss_repair.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / NREPAIR_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL.
- **What is being added:** A focused actual-template repair scan around the
  `single_outside_w7_v3` near miss. It preserves the selected-count ledger and
  tests witness-7 single-coordinate mutations plus a second-order refinement
  around the best one-coordinate mutation.
- **Result:** Tested 177 mutation profiles, 1062 systems, and 184,428 stable
  slot profiles. Found zero actual zero-slot profiles. The best mutation is
  `w7_c1_v9`; it keeps support `[327,...,327]`, pair7 counts `[253,...,253]`,
  functional span rank 6, and no forced identities, but still has 2 nonzero
  slot rows. It improves the forced-pair count from 15 to 10.
- **How it is useful:** Confirms that small witness-7 coordinate mutations do
  not produce a realized proxy-slot kernel, but the best mutation gives a
  sharper residual-equation target.
- **What to do next:** Derive the two residual slot coefficients as explicit
  equations in template-vector perturbation variables and solve that small
  repair problem directly, using Python first and Macaulay2/Singular only if
  the equations become a module/elimination problem.
### 2026-07-03 - M1 a327 residual-slot equation repair

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_residual_slot_equation_repair.md`,
  `experimental/scripts/scan_m1_a327_residual_slot_equation_repair.py`,
  `experimental/scripts/verify_m1_a327_residual_slot_equation_repair.py`,
  `experimental/data/m1_a327_residual_slot_equation_repair.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RESIDUAL_SLOT_INVARIANT_NONZERO / PARTIAL / EXPERIMENTAL.
- **What is being added:** A focused residual-equation audit for the best
  `nearmiss_w7_c1_v9` actual-template profile, plus an exhaustive stable-basis
  check for that same actual template.
- **Result:** The two residual rows are classes 1 and 5, with slot coefficient
  `1` in the target slot. In the local parameter model
  `[e3+u,e2+u,e1+u,e4-e5,e3-e5,e6]`, both residual slot coefficients remain
  `[1]` for all 272 nonsingular `(U,V)` values over GF(17). The exhaustive
  stable-basis audit constructs 122 stable profiles and tests 732 slot
  profiles; zero actual zero-slot profiles are found.
- **How it is useful:** Turns the two residual coefficients into an explicit
  local obstruction: the fixed-basis residual equations reduce to `1=0`, and
  the current actual template has no alternative stable zero-slot profile.
- **What to do next:** Move above local witness-7 perturbation. Alter the
  selected-count ledger or template family so the obstruction functional
  `[0,0,0,1,0,0]` is included in a stable basis or no longer projects
  invariantly onto the candidate slot.
### 2026-07-03 - M1 a327 realization-aware ledger perturbation

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_realization_aware_ledger_perturbation.md`,
  `experimental/scripts/scan_m1_a327_realization_aware_ledger_perturbation.py`,
  `experimental/scripts/verify_m1_a327_realization_aware_ledger_perturbation.py`,
  `experimental/data/m1_a327_realization_aware_ledger_perturbation.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / LEDGERPERT_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded selected-count ledger perturbation scan
  around the actual `nearmiss_w7_c1_v9` template, walking the exact
  coordinate/support-count kernel while preserving pair caps and pair-7 guards.
- **Result:** Tested 96 feasible ledgers, 576 actual-template systems, and
  127,800 slot profiles. Found zero actual zero-slot profiles and zero
  pair-projection-clear slots. The best result remains the unperturbed base
  ledger with 2 nonzero slot rows and 10 forced pairs.
- **How it is useful:** Shows that same-mask support-preserving ledger motion
  does not remove the residual slot obstruction in this bounded front.
- **What to do next:** Force the obstruction functional `[0,0,0,1,0,0]` into
  the stable basis, or allow new selected masks/template families rather than
  continuing same-mask count-kernel perturbations.
### 2026-07-03 - M1 a327 obstruction-functional basis forcing

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_obstruction_functional_basis_forcing.md`,
  `experimental/scripts/scan_m1_a327_obstruction_functional_basis_forcing.py`,
  `experimental/scripts/verify_m1_a327_obstruction_functional_basis_forcing.py`,
  `experimental/data/m1_a327_obstruction_functional_basis_forcing.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / BASISFORCE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A forced-basis audit for actual-template profiles,
  requiring the obstruction functional `[0,0,0,1,0,0]` and optionally the
  secondary residual `[0,0,0,1,4,8]` to appear in the stable basis.
- **Result:** Tested 576 systems, 4608 forced stable-basis combinations, and
  576 valid forced stable-basis profiles. Every valid forced profile has full
  coefficient rank; zero coefficient-kernel profiles and zero pair-clear
  profiles are found.
- **How it is useful:** Shows that the direct fix for the residual slot
  obstruction kills the actual right kernel in this bounded front.
- **What to do next:** Co-design basis inclusion and coefficient rank defect
  from the start, rather than perturbing the same ledger after the fact.
### 2026-07-03 - M1 a327 basis/kernel co-design

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_basis_kernel_codesign.md`,
  `experimental/scripts/scan_m1_a327_basis_kernel_codesign.py`,
  `experimental/scripts/verify_m1_a327_basis_kernel_codesign.py`,
  `experimental/data/m1_a327_basis_kernel_codesign.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / CODESIGN_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A broader actual-template co-design scan across the
  existing 36-template candidate generator, forcing obstruction-functional
  basis inclusion during basis selection and requiring coefficient rank defect
  before pair/proxy checks.
- **Result:** Tested 216 systems. Among 210 structural-pass candidates, 144
  contain a target obstruction functional. The scan checked 257,298 forced
  basis combinations and 4,530 valid forced stable-basis profiles. It found
  zero coefficient-kernel profiles.
- **How it is useful:** Shows the existing actual-template generator does not
  co-design obstruction-functional basis inclusion with right-kernel rank
  defect; the failure is broader than the local same-mask front.
- **What to do next:** Move to a determinantal/rank-defect template ansatz:
  prescribe a rank-5 relation among nonbasis coefficient rows first, then solve
  for template vectors or selected masks that realize it.
### 2026-07-03 - M1 a327 rank-defect template ansatz

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_rankdefect_template_ansatz.md`,
  `experimental/scripts/scan_m1_a327_rankdefect_template_ansatz.py`,
  `experimental/scripts/verify_m1_a327_rankdefect_template_ansatz.py`,
  `experimental/data/m1_a327_rankdefect_template_ansatz.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / RANKDEFECT_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL.
- **What is being added:** A new template generator built from rank-5
  hyperplanes plus one outside witness direction, followed by the same
  support/pair, obstruction-basis, and coefficient-kernel gates.
- **Result:** Generated 64 templates and tested 384 systems. All systems are
  structural-pass. 84 contain the target obstruction functional. The scan
  checks 7,498,470 forced basis combinations and 4,260 valid forced stable-basis
  profiles, with zero coefficient-kernel profiles.
- **How it is useful:** Shows that the first explicit rank-defect-oriented
  template ansatz still does not create coefficient rank defect under forced
  obstruction-basis inclusion.
- **What to do next:** Prescribe repeated nonbasis coordinate rows or an
  explicit right-kernel vector for the coefficient matrix, then solve backward
  for template vectors or selected masks.
### 2026-07-03 - M1 a327 nonbasis row dependency ansatz

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_nonbasis_row_dependency_ansatz.md`,
  `experimental/scripts/scan_m1_a327_nonbasis_row_dependency_ansatz.py`,
  `experimental/scripts/verify_m1_a327_nonbasis_row_dependency_ansatz.py`,
  `experimental/data/m1_a327_nonbasis_row_dependency_ansatz.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / NBDEP_NEAR_KERNEL_ONLY / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded exact row-deletion diagnostic over the
  realized rank-defect template rowspaces. For every forced stable-basis
  profile, the scan searches up to three deleted nonbasis coefficient rows for
  a right-kernel vector.
- **Result:** Tested 384 systems and 4,260 forced stable-basis profiles. Found
  zero actual coefficient-kernel profiles, 252 near-kernel profiles within the
  three-row deletion bound, and zero pair-projection-clear actual kernels. The
  best near-kernel removes two rows, gives kernel vector `[0,0,1,1,1,0]`, and
  still forces ten pair equalities.
- **How it is useful:** Refines the full-rank obstruction into a bounded
  near-kernel ledger: the current realized rowspaces are close enough to expose
  residual row classes, but not close enough to yield a usable exact kernel.
- **What to do next:** Prescribe the nonbasis kernel relation directly,
  including pair-projection clearance, then solve backward for selected masks
  or template vectors that realize it.
### 2026-07-03 - M1 a327 prescribed nonbasis kernel generator

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_prescribed_nonbasis_kernel_generator.md`,
  `experimental/scripts/scan_m1_a327_prescribed_nonbasis_kernel_generator.py`,
  `experimental/scripts/verify_m1_a327_prescribed_nonbasis_kernel_generator.py`,
  `experimental/data/m1_a327_prescribed_nonbasis_kernel_generator.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PNK_NEAR_KERNEL_FORCED_PAIR / PARTIAL / EXPERIMENTAL.
- **What is being added:** A bounded pair-clear prescribed-kernel scan over the
  retained best-profile front from `46b73ec`. For each profile, it searches
  deletion-bounded coefficient nullspaces and requires all 21 pair projections
  to be nonzero.
- **Result:** Tested 384 systems and 84 retained forced-basis profiles from
  70 previous-front profile keys. Found zero actual pair-clear kernels and zero
  near pair-clear kernels. The best remains a two-row near-kernel with vector
  `[0,0,1,1,1,0]`, but it still forces ten pair equalities.
- **How it is useful:** Separates the coefficient-kernel obstruction from the
  pair-projection obstruction: bounded near-kernels exist, but none in the
  retained front escape pair collapse.
- **What to do next:** Move to backward synthesis: generate selected masks and
  template vectors while enforcing a prescribed pair-clear kernel from the
  start, rather than searching existing rowspaces after the fact.
### 2026-07-04 - M1 a327 pair-clear kernel backward synthesis

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_pairclear_kernel_backward_synthesis.md`,
  `experimental/scripts/scan_m1_a327_pairclear_kernel_backward_synthesis.py`,
  `experimental/scripts/verify_m1_a327_pairclear_kernel_backward_synthesis.py`,
  `experimental/data/m1_a327_pairclear_kernel_backward_synthesis.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / PKBS_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL.
- **What is being added:** A first backward-synthesis scan using actual
  template specs whose raw slot separates all seven witnesses, followed by
  stable-basis slot-kernel checks.
- **Result:** Tested 4 template specs, 12 assigned systems, 123 stable-basis
  profiles, and 738 coefficient slots. Found zero actual zero-slot profiles and
  zero pair-projection-clear actual slots. The best row has 3 nonzero slot rows
  but still forces 11 pair equalities.
- **How it is useful:** Shows raw template-coordinate pair separation is not
  enough; pair clearance must be enforced in stable-basis coordinates.
- **What to do next:** Move to basis-aware backward synthesis where template
  vectors, selected classes, stable basis functionals, and the coefficient
  kernel vector are co-designed.
### 2026-07-04 - M1 a327 basis-aware pair-clear kernel synthesis

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_a327_basis_aware_pairclear_kernel_synthesis.md`,
  `experimental/scripts/scan_m1_a327_basis_aware_pairclear_kernel_synthesis.py`,
  `experimental/scripts/verify_m1_a327_basis_aware_pairclear_kernel_synthesis.py`,
  `experimental/data/m1_a327_basis_aware_pairclear_kernel_synthesis.json`,
  `experimental/agents-log.md`.
- **Status:** EXACT_EXTRACTION_NO_A327 / BAPK_SLOT_PAIR_CLEAR_BROKEN / PARTIAL / EXPERIMENTAL.
- **What is being added:** A basis-aware scan that enumerates high-support and
  seeded stable-basis candidates, then scores every coefficient slot by pair
  projection and nonbasis support.
- **Result:** Tested 12 systems, 2,976 basis profiles, and 17,856 slot
  profiles. Found zero pair-clear slot profiles and zero pair-clear slot-kernel
  profiles. The best forced-pair count improved from 11 to 4, with remaining
  forced pairs `P12`, `P17`, `P27`, and `P46`.
- **How it is useful:** Confirms basis choice is the right lever: the pair
  collapse obstruction improved substantially, but still did not clear.
- **What to do next:** Target the four remaining forced pairs directly in a
  forced-pair repair branch.
