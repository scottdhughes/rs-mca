# Lean Blueprint Coverage Report

Static source-scan snapshot.  Do not regenerate or treat as authoritative without
manual statement audit.

Scope: source-level scan only. No Lake build was run.

## Summary

- Blueprint nodes: `394`
- Mapped blueprint nodes: `66`
- Unmapped blueprint nodes: `328`
- Related Lean declarations attached to mapped nodes: `125`
- Lean declarations inventoried: `772`
- Lean declarations mapped to at least one blueprint node: `101`

## Mapping Status

- `lean_mixed_proved_and_skeleton_source_scan`: `6`
- `lean_statement_present_no_sorry_source_scan`: `46`
- `lean_statement_skeleton_sorry_source_scan`: `14`
- `not_started`: `328`

## Mapping Confidence

- `curated_alias`: `26`
- `exact_label_match`: `38`
- `mixed`: `2`
- `unmapped`: `328`

## Audit Status

- `mapped_needs_statement_audit`: `2`
- `mapped_skeleton_needs_proof`: `14`
- `mapped_source_scanned_not_built`: `44`
- `mapped_split_package_needs_statement_audit`: `6`
- `unmapped`: `328`

## Mapped Nodes By Module

| Module | Mapped | Total |
| --- | ---: | ---: |
| `bc_split_pencil` | 0 | 21 |
| `ca_mca_definitions` | 8 | 10 |
| `capf_paid_ledgers` | 16 | 35 |
| `capfp_slope_lattice_split_pencil` | 0 | 39 |
| `capg_final_frontier_package` | 0 | 22 |
| `computations_and_certificates` | 0 | 15 |
| `deep_point_and_list_to_ca` | 0 | 8 |
| `extension_and_subfield` | 0 | 5 |
| `frontier_final_targets` | 0 | 11 |
| `genus_one_circle_transport` | 0 | 2 |
| `hankel_and_aperiodic_charts` | 4 | 40 |
| `imported_theorems_and_audits` | 0 | 2 |
| `l1_and_paid_aperiodic_layers` | 6 | 26 |
| `miscellaneous` | 2 | 14 |
| `q_prefix_flatness` | 6 | 26 |
| `quotient_lower_ledgers` | 0 | 2 |
| `safe_side` | 2 | 4 |
| `sp_shift_pairs` | 0 | 14 |
| `staircase_and_certificates` | 2 | 6 |
| `support_and_image_ledgers` | 11 | 55 |
| `universal_cap_and_sandwich` | 9 | 37 |

## Q / BC / SP Dependency Closures

### `target:Q_prefix_flatness`

- Closure nodes including target: `36`
- Mapped in closure: `5`
- Unmapped in closure: `31`
- Mapped:
  - `cor:capf-endpoint` -> `CAP25V13.Threshold.endpoint_radius`
  - `lem:one-support-d-curve` -> `RSCap.lem_one_support_d_curve`
  - `prop:onestep` -> `StaircaseLogic.Staircase.oneStep_isFirstSafe`
  - `thm:capf-staircase` -> `CAP25V13.Threshold.staircase_localization`
  - `thm:deep-mca` -> `RSCap.emcaErr_le_deep`
- Unmapped:
  - `cor:T1-status`
  - `cor:capf-exact-variance`
  - `cor:capff1-sandwich-edges`
  - `cor:capg-adjacent-pairs`
  - `cor:periodic-support-count`
  - `def:capff1-gstar`
  - `def:periodicity-scale`
  - `lem:capf-gcd`
  - `lem:capg-prefix-rigidity`
  - `lem:capg-witness`
  - `prob:band`
  - `prob:capf-primitive-image-fiber`
  - `prob:capff1-frontier`
  - `prob:capfp-F`
  - `prob:capfr1-master-flatness`
  - `prob:capfr1-mode-null`
  - `prob:capfr1-rung-audit`
  - `prob:capg-shiftpairs`
  - `prop:capff1-identity-frontier`
  - `prop:capfp-Q-sandwich`
  - `prop:capg-moved-frontier`
  - `rem:capf-moment-scope`
  - `rem:capfpr-low-moments`
  - `rem:capg-flatness-wiring`
  - `target:Q_prefix_flatness`
  - `thm:capf-first-moment`
  - `thm:capf-second-moment`
  - `thm:capg-second-moment`
  - `thm:conditional-mca`
  - `thm:fiber-descent`
  - `thm:weil-lines`

### `target:BC_base_field_split_pencil`

- Closure nodes including target: `44`
- Mapped in closure: `8`
- Unmapped in closure: `36`
- Mapped:
  - `cor:capf-endpoint` -> `CAP25V13.Threshold.endpoint_radius`
  - `lem:cheb-fibers` -> `RSCap.lem_cheb_fibers`
  - `lem:one-support-d-curve` -> `RSCap.lem_one_support_d_curve`
  - `lem:phi-fiber` -> `RSCap.lem_phi_fiber_ii`
  - `lem:quotient-remainder-prefix` -> `RSCap.lem_quotient_remainder_prefix`
  - `prop:onestep` -> `StaircaseLogic.Staircase.oneStep_isFirstSafe`
  - `thm:capf-staircase` -> `CAP25V13.Threshold.staircase_localization`
  - `thm:deep-mca` -> `RSCap.emcaErr_le_deep`
- Unmapped:
  - `cor:T1-status`
  - `cor:capff1-sandwich-edges`
  - `cor:capg-adjacent-pairs`
  - `cor:capg-asymptotic`
  - `cor:periodic-support-count`
  - `def:capff1-gstar`
  - `def:periodicity-scale`
  - `lem:capff1-identity-prefix-floor`
  - `lem:capfp-autodiv`
  - `lem:capfp-functionals`
  - `lem:capfp-pair-descent`
  - `lem:confine`
  - `lem:singular-pencil`
  - `prob:band`
  - `prob:capff1-frontier`
  - `prob:capfp-F`
  - `prob:capfp-R1`
  - `prob:capfp-balanced`
  - `prob:capfp-split`
  - `prop:capff1-identity-frontier`
  - `prop:capfp-detrep`
  - `prop:capfp-kernel`
  - `prop:capfr1-detrep`
  - `prop:capfr1-slope-elimination`
  - `prop:capg-census-floor`
  - `prop:capg-final-active-package`
  - `prop:capg-moved-frontier`
  - `prop:graded-prefix-floor`
  - `target:BC_base_field_split_pencil`
  - `thm:capf-spi`
  - `thm:capfp-Q-unify`
  - `thm:capfp-dichotomy`
  - `thm:capfp-slope-elim`
  - `thm:conditional-mca`
  - `thm:fiber-descent`
  - `thm:weil-lines`

### `target:SP_primitive_shift_pair_control`

- Closure nodes including target: `6`
- Mapped in closure: `0`
- Unmapped in closure: `6`
- Unmapped:
  - `def:periodicity-scale`
  - `lem:capg-prefix-rigidity`
  - `rem:capg-prototype`
  - `target:SP_primitive_shift_pair_control`
  - `thm:capg-second-moment`
  - `thm:fiber-descent`

### `target:finite_adjacent_deployed_ledgers`

- Closure nodes including target: `73`
- Mapped in closure: `9`
- Unmapped in closure: `64`
- Mapped:
  - `cor:capf-endpoint` -> `CAP25V13.Threshold.endpoint_radius`
  - `lem:cheb-fibers` -> `RSCap.lem_cheb_fibers`
  - `lem:one-support-d-curve` -> `RSCap.lem_one_support_d_curve`
  - `lem:phi-fiber` -> `RSCap.lem_phi_fiber_ii`
  - `lem:quotient-remainder-prefix` -> `RSCap.lem_quotient_remainder_prefix`
  - `prop:onestep` -> `StaircaseLogic.Staircase.oneStep_isFirstSafe`
  - `thm:capf-corridor` -> `CAP25V13.Threshold.corridor_lower`
  - `thm:capf-staircase` -> `CAP25V13.Threshold.staircase_localization`
  - `thm:deep-mca` -> `RSCap.emcaErr_le_deep`
- Unmapped:
  - `comp:cap25_v13_raw_moved_frontier_checks`
  - `comp:extension_cell_targets_json`
  - `comp:frontier_adjacent_packet_json`
  - `comp:frontier_adjacent_v13_rows_verifier`
  - `comp:frontier_extension_cell_targets_verifier`
  - `comp:identity_frontier_certificate_packet`
  - `cor:T1-status`
  - `cor:capf-exact-variance`
  - `cor:capff1-sandwich-edges`
  - `cor:capg-adjacent-pairs`
  - `cor:capg-asymptotic`
  - `cor:periodic-support-count`
  - `def:capff1-gstar`
  - `def:periodicity-scale`
  - `lem:capf-gcd`
  - `lem:capff1-identity-prefix-floor`
  - `lem:capfp-autodiv`
  - `lem:capfp-functionals`
  - `lem:capfp-pair-descent`
  - `lem:capg-prefix-rigidity`
  - `lem:capg-witness`
  - `lem:confine`
  - `lem:singular-pencil`
  - `prob:band`
  - `prob:capf-primitive-image-fiber`
  - `prob:capff1-frontier`
  - `prob:capfp-F`
  - `prob:capfp-R1`
  - `prob:capfp-balanced`
  - `prob:capfp-split`
  - `prob:capfr1-master-flatness`
  - `prob:capfr1-mode-null`
  - `prob:capfr1-normalized-band`
  - `prob:capfr1-rung-audit`
  - `prob:capg-shiftpairs`
  - `prop:capff1-closing`
  - `prop:capff1-identity-frontier`
  - `prop:capfp-Q-sandwich`
  - `prop:capfp-detrep`
  - `prop:capfp-kernel`

### `target:RS_MCA_full_resolution`

- Closure nodes including target: `74`
- Mapped in closure: `9`
- Unmapped in closure: `65`
- Mapped:
  - `cor:capf-endpoint` -> `CAP25V13.Threshold.endpoint_radius`
  - `lem:cheb-fibers` -> `RSCap.lem_cheb_fibers`
  - `lem:one-support-d-curve` -> `RSCap.lem_one_support_d_curve`
  - `lem:phi-fiber` -> `RSCap.lem_phi_fiber_ii`
  - `lem:quotient-remainder-prefix` -> `RSCap.lem_quotient_remainder_prefix`
  - `prop:onestep` -> `StaircaseLogic.Staircase.oneStep_isFirstSafe`
  - `thm:capf-corridor` -> `CAP25V13.Threshold.corridor_lower`
  - `thm:capf-staircase` -> `CAP25V13.Threshold.staircase_localization`
  - `thm:deep-mca` -> `RSCap.emcaErr_le_deep`
- Unmapped:
  - `comp:cap25_v13_raw_moved_frontier_checks`
  - `comp:extension_cell_targets_json`
  - `comp:frontier_adjacent_packet_json`
  - `comp:frontier_adjacent_v13_rows_verifier`
  - `comp:frontier_extension_cell_targets_verifier`
  - `comp:identity_frontier_certificate_packet`
  - `cor:T1-status`
  - `cor:capf-exact-variance`
  - `cor:capff1-sandwich-edges`
  - `cor:capg-adjacent-pairs`
  - `cor:capg-asymptotic`
  - `cor:periodic-support-count`
  - `def:capff1-gstar`
  - `def:periodicity-scale`
  - `lem:capf-gcd`
  - `lem:capff1-identity-prefix-floor`
  - `lem:capfp-autodiv`
  - `lem:capfp-functionals`
  - `lem:capfp-pair-descent`
  - `lem:capg-prefix-rigidity`
  - `lem:capg-witness`
  - `lem:confine`
  - `lem:singular-pencil`
  - `prob:band`
  - `prob:capf-primitive-image-fiber`
  - `prob:capff1-frontier`
  - `prob:capfp-F`
  - `prob:capfp-R1`
  - `prob:capfp-balanced`
  - `prob:capfp-split`
  - `prob:capfr1-master-flatness`
  - `prob:capfr1-mode-null`
  - `prob:capfr1-normalized-band`
  - `prob:capfr1-rung-audit`
  - `prob:capg-shiftpairs`
  - `prop:capff1-closing`
  - `prop:capff1-identity-frontier`
  - `prop:capfp-Q-sandwich`
  - `prop:capfp-detrep`
  - `prop:capfp-kernel`

## Nodes With Skeleton Or Mixed Lean Status

- `cor:circle-grand` -> `RSCap.cor_circle_grand` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `cor:ecfft-macroscopic` -> `RSCap.cor_ecfft_macroscopic` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `cor:ecfft-onestep` -> `RSCap.cor_ecfft_onestep` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `cor:first-grid-cap` -> `RSCap.cor_first_grid_cap` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `cor:quantitative-first-grid-floor` -> `RSCap.cor_quantitative_first_grid_floor` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `lem:cheb-fibers` -> `RSCap.lem_cheb_fibers` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `lem:circle-rs` -> `RSCap.lem_circle_rs` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `lem:fiber` -> `RSCap.lem_fiber_ii` (lean_mixed_proved_and_skeleton_source_scan, mapped_split_package_needs_statement_audit)
- `lem:heaviest-prefix-locator-floor` -> `RSCap.lem_heaviest_prefix_locator_floor` (lean_mixed_proved_and_skeleton_source_scan, mapped_split_package_needs_statement_audit)
- `lem:phi-fiber` -> `RSCap.lem_phi_fiber_ii` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `lem:quotient-remainder-prefix` -> `RSCap.lem_quotient_remainder_prefix` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `lem:regular-exact-agreement-eliminant` -> `RSCap.lem_regular_exact_agreement_eliminant` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `lem:stereographic` -> `RSCap.lem_stereographic` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `prop:graded-rational-floor` -> `RSCap.prop_graded_rational_floor` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `prop:rational-floor` -> `RSCap.prop_rational_floor` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `thm:explicit-head-floor` -> `RSCap.thm_explicit_head_floor_even` (lean_mixed_proved_and_skeleton_source_scan, mapped_split_package_needs_statement_audit)
- `thm:explicit-pairs` -> `RSCap.thm_explicit_pairs` (lean_mixed_proved_and_skeleton_source_scan, mapped_split_package_needs_statement_audit)
- `thm:main` -> `RSCap.universal_cap_emca_of_fiber_list` (lean_mixed_proved_and_skeleton_source_scan, mapped_split_package_needs_statement_audit)
- `thm:phi-cap` -> `RSCap.thm_phi_cap` (lean_statement_skeleton_sorry_source_scan, mapped_skeleton_needs_proof)
- `thm:regular-closed-ball-hankel-packing` -> `RSCap.thm_regular_closed_ball_hankel_packing` (lean_mixed_proved_and_skeleton_source_scan, mapped_split_package_needs_statement_audit)

## Unmapped High-Priority Nodes

- `cor:capfr1-Q-R1-closing` (bc_split_pencil, corollary)
- `cor:capfr1-balanced-line` (bc_split_pencil, corollary)
- `cor:capfr1-terminal-package` (bc_split_pencil, corollary)
- `lem:capfr1-autodiv` (bc_split_pencil, lemma)
- `lem:capfr1-interpolation-test` (bc_split_pencil, lemma)
- `lem:capfr1-pair-descent` (bc_split_pencil, lemma)
- `lem:capfr1-unimodular` (bc_split_pencil, lemma)
- `prob:capfr1-balanced-core` (bc_split_pencil, remark)
- `prob:capfr1-rank-one-census` (bc_split_pencil, remark)
- `prob:capfr1-split-pencil` (bc_split_pencil, remark)
- `prob:capg-split-pencil-B` (bc_split_pencil, remark)
- `prop:capfr1-detrep` (bc_split_pencil, proposition)
- `prop:capfr1-lattice-census` (bc_split_pencil, proposition)
- `prop:capfr1-slope-elimination` (bc_split_pencil, proposition)
- `rem:capfr1-pair-descent-gap` (bc_split_pencil, remark)
- `rem:capg-boundary-offbyone` (bc_split_pencil, remark)
- `rem:capg-slopeelim-closure` (bc_split_pencil, remark)
- `rem:capg-subfield-scope` (bc_split_pencil, remark)
- `rem:capg-supportside` (bc_split_pencil, remark)
- `target:BC_base_field_split_pencil` (bc_split_pencil, conjectural_target)
- `thm:capfr1-near-rational-dichotomy` (bc_split_pencil, theorem)
- `cor:capg-adjacent-pairs` (capg_final_frontier_package, corollary)
- `cor:capg-asymptotic` (capg_final_frontier_package, corollary)
- `cor:capg-budget-conversion` (capg_final_frontier_package, corollary)
- `cor:capg-singular` (capg_final_frontier_package, corollary)
- `cor:capg-spib` (capg_final_frontier_package, corollary)
- `def:capg-syndrome` (capg_final_frontier_package, definition)
- `lem:capg-class0-section` (capg_final_frontier_package, lemma)
- `lem:capg-constdiv` (capg_final_frontier_package, lemma)
- `lem:capg-dictionary` (capg_final_frontier_package, lemma)
- `lem:capg-gcdwindow` (capg_final_frontier_package, lemma)
- `lem:capg-relclosed` (capg_final_frontier_package, lemma)
- `lem:capg-residue` (capg_final_frontier_package, lemma)
- `lem:capg-small` (capg_final_frontier_package, lemma)
- `lem:capg-window` (capg_final_frontier_package, lemma)
- `lem:capg-witness` (capg_final_frontier_package, lemma)
- `prop:capg-class0` (capg_final_frontier_package, proposition)
- `prop:capg-moved-frontier` (capg_final_frontier_package, proposition)
- `rem:capg-band` (capg_final_frontier_package, remark)
- `rem:capg-quantsplit` (capg_final_frontier_package, remark)
- `rem:capg-witnessrel` (capg_final_frontier_package, remark)
- `thm:capg-aperiodic-floor` (capg_final_frontier_package, theorem)
- `thm:capg-tangentborne` (capg_final_frontier_package, theorem)
- `cor:conditional-half` (frontier_final_targets, corollary)
- `cor:self-contained-safe` (frontier_final_targets, corollary)
- `def:capff1-gstar` (frontier_final_targets, definition)
- `prob:capff1-frontier` (frontier_final_targets, conjecture)
- `prob:capfr1-mode-null` (frontier_final_targets, remark)
- `prop:capff1-identity-frontier` (frontier_final_targets, proposition)
- `rem:capff1-closure` (frontier_final_targets, remark)
- `rem:entropy-frontier` (frontier_final_targets, remark)
- `rem:exact-frontier` (frontier_final_targets, remark)
- `rem:twotier` (frontier_final_targets, remark)
- `target:RS_MCA_full_resolution` (frontier_final_targets, final_goal)
- `def:capg-prefix` (q_prefix_flatness, definition)
- `lem:capff1-identity-prefix-floor` (q_prefix_flatness, lemma)
- `lem:capfr1-kernel-distance` (q_prefix_flatness, lemma)
- `prob:capfr1-normalized-band` (q_prefix_flatness, remark)
- `prop:capff1-composite` (q_prefix_flatness, proposition)
- `prop:capfr1-collision-ledger` (q_prefix_flatness, proposition)
- `prop:capfr1-moment-kernel` (q_prefix_flatness, proposition)
- `rem:capff1-calibration` (q_prefix_flatness, remark)
- `rem:capff1-collision-gap` (q_prefix_flatness, remark)
- `rem:capfr1-packing-bits` (q_prefix_flatness, remark)
- `rem:capfr1-packing-gap` (q_prefix_flatness, remark)
- `rem:capg-evenm` (q_prefix_flatness, remark)
- `rem:lines` (q_prefix_flatness, remark)
- `rem:no-divisibility` (q_prefix_flatness, remark)
- `rem:phi-cap-scope` (q_prefix_flatness, remark)
- `rem:slacktwo` (q_prefix_flatness, remark)
- `rem:subpigeon` (q_prefix_flatness, remark)
- `target:Q_prefix_flatness` (q_prefix_flatness, conjectural_target)
- `thm:capff1-collision-base` (q_prefix_flatness, theorem)
- `thm:list-recursion` (q_prefix_flatness, theorem)
- `cor:capg-anticode-cap` (sp_shift_pairs, corollary)
- `cor:capg-deployed-floor` (sp_shift_pairs, corollary)
- `lem:capg-prefix-rigidity` (sp_shift_pairs, lemma)
- `prob:capg-shiftpairs` (sp_shift_pairs, remark)
- `prop:capg-active-interface` (sp_shift_pairs, proposition)
- `prop:capg-census-floor` (sp_shift_pairs, proposition)
- `prop:capg-final-active-package` (sp_shift_pairs, proposition)
- `rem:capg-calibration` (sp_shift_pairs, remark)
- `rem:capg-flatness-wiring` (sp_shift_pairs, remark)
- `rem:capg-prototype` (sp_shift_pairs, remark)
- `rem:capg-rigidcompare` (sp_shift_pairs, remark)
- `rem:capg-secondmom-rel` (sp_shift_pairs, remark)
- `target:SP_primitive_shift_pair_control` (sp_shift_pairs, conjectural_target)
- `thm:capg-second-moment` (sp_shift_pairs, theorem)
- `cor:base-rational-line-inertness-chart` (staircase_and_certificates, corollary)
- `cor:capff1-collision-head` (staircase_and_certificates, corollary)
- `prop:finite-certificate` (staircase_and_certificates, proposition)
- `target:finite_adjacent_deployed_ledgers` (staircase_and_certificates, certificate_target)

## Reverse Inventory Notes

`lean-inventory.json` is a static reverse-list snapshot of Lean declarations. A declaration with an empty `blueprint_matches` list exists in Lean but is not yet mapped to a CAP25 v13 raw blueprint node.
