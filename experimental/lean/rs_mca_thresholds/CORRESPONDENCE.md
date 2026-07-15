# Paper-to-Lean correspondence

- `def:ca-sparse-numerators`: `ColumnFar`, `SparseAt`,
  `sparseMutualChallenge`, `sparseMutualNumerator`.
- Translation argument in `thm:exact-sparsification`:
  `explained_sub_mem_iff`, `explainedPair_sub_mem_iff`,
  `lineExplained_sub_mem_iff`, `mcaBad_sub_mem_iff`,
  `sparseAt_sub_mem_of_explained`.
- `eq:challenge-sparsification` (SP3):
  `exact_sparsification_challenge`.
- `thm:exact-sparsification` (SP2): `exact_sparsification`.
- `thm:exact-half-distance-sparse` (HD1):
  `exact_half_distance_sparse` and `exact_half_distance_mca`.
- Reed--Solomon hypothesis `2r ≤ n-k`:
  `exact_half_distance_sparse_rsDistance` and
  `exact_half_distance_mca_rsDistance`.
- `lem:large-overlap-collapse` (MO1--MO2):
  `large_overlap_quotient_le`, `large_overlap_collapse_from_cells`, and
  `hasLargeOverlapCollapse_of_informationSets`.
- `thm:quadratic-mean-overlap` incidence core (MO5--MO6):
  `sum_degrees_eq`, `sum_degrees_sq_eq`,
  `offDiagonal_intersections_le`, `square_total_degrees_le`, and
  `exists_large_overlap`.
- Reed--Solomon MDS and exact-support bridges:
  `rs_hasMDSInformationSets`,
  `hasExactSupportReduction_of_informationSets`, `rs_hasDeepUpper`, and
  `rs_hasTangentLower`.
- `thm:quadratic-mean-overlap` (MO3--MO4):
  `quadratic_mean_overlap_upper`, `quadratic_mean_overlap_exact`, and the
  fully discharged RS specialization `rs_quadratic_mean_overlap_exact`.
- `cor:mean-overlap-exact` (MO7): `quadraticRoot`,
  `quadraticRoot_is_root`, `quadraticRadius_eq_floor`,
  `quadratic_condition_of_le_floor`, and the literal raw-floor RS theorem
  `rs_quadratic_staircase_exact`.
- `lem:appendix-endpoint`: `B_MCA_challenge_antitone`,
  `safe_errorRadius_iff`, `floor_mul_le_iff_lt_endpoint`, and
  `safe_realRadius_iff`.
- `cor:prize-window-compiler`: `rs_quadratic_target_window` and the
  degenerate branch `rs_zero_budget_radius_zero_unsafe`.
- `cor:half-distance-window-compiler`:
  `half_distance_target_window`, parameterized by the certified exact
  staircase range and tangent lower bound.
- `thm:intro-delta-formula`: `firstSafeAgreement_crossing_bounds`,
  `firstSafeAgreement_isLittleO`, and `certificateRadius_tendsto`.

`MinimumDistanceAtLeast C d` is the exact minimum-distance interface used by
HD1: every nonzero codeword has support cardinality at least `d`. The shared
definitions `GrandeFinale.Explained`, `GrandeFinale.ExplainedPair`,
`GrandeFinale.MCABad`, `GrandeFinale.CABad`, `GrandeFinale.B_MCA`, and
`GrandeFinale.B_CA` are imported and reused verbatim.
