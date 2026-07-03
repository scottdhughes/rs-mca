# M1 a327 selected-class rank-defect search

Status: EXACT_EXTRACTION_NO_A327 / RANK_DEFECT_PROXY_FULL_RANK / PARTIAL /
EXPERIMENTAL for the first-pass proxy scan.

This packet moves the `a=327` selected-class search from carrier-graph
patching to quotient-rank design. It remains INTERLEAVED_LIST work only. It is
not an MCA row, not protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Rank-defect criterion

For selected classes `C_h subset [7]` with support exactly `327` for each
witness, the received-word formulation has

```text
7 * 327 = 2289 selected incidences.
```

After quotienting by the diagonal codeword and eliminating received-word values,
the quotient system has

```text
1536 variables = 6 * 256
1777 equations = 2289 - 512.
```

A non-diagonal selected-class exact lift requires the quotient equality matrix
to have rank defect:

```text
rank M(C) < 1536.
```

If `rank M(C) < 1536` and no pair projection is identically zero on the
nullspace, then a seven-distinct exact lift exists by avoiding finitely many
proper pair-equality subspaces over `GF(17^32)`.

## Search design

The scanner generates RS-feasible selected-class hypergraphs with:

```text
support_i = 327
pair_ij <= 255
pair_i7 >= 142
```

The Sage audit then builds the full selected-class quotient matrix over the
proxy prime `12289`, which has a multiplicative subgroup of order `512`, and
records whether the proxy rank has positive nullity. Only proxy-positive
designs should be sent to the exact `GF(17^32)` rank audit.

The first profiles are:

```text
fiber_balanced_45
fiber_block_selected_classes
nested_pairset_7_guard
quotient_fiber_rank_defect
residue_class_rank_defect
low_cycle_dependency
mixed_fiber_residual
```

These profiles deliberately vary fiber assignment and pair nesting, because the
current obstruction is algebraic rank, not only support feasibility.

## First-pass result

The scanner generated `14` RS-feasible selected-class hypergraphs. The Sage
audit computed the full `1777 x 1536` quotient-rank proxy over `GF(12289)` for
each candidate. No proxy rank-defect candidate was found:

```text
systems_tested = 14
proxy_rank_defect_candidates = 0
best_proxy_rank = 1536
best_proxy_nullity = 0
best_failure_mode = RANK_DEFECT_PROXY_FULL_RANK
```

Because the proxy rank was already full column rank, this packet did not run
the expensive exact `GF(17^32)` rank audit. This is a first-pass negative for
the named rank-defect profiles, not a global selected-class obstruction.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

The next constructive step should engineer stronger algebraic dependencies
before exact lifting. Candidates should only be sent to `GF(17^32)` once a
proxy rank-defect appears, at which point the Sage audit should test all 21
pair projections and construct an explicit received word only if the nullspace
is nonzero and no pair is forced equal.
