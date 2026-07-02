# M1 a327 selected-class thin exact lift

Status: PROOF_RECORD / CANDIDATE / EXACT_EXTRACTION_NO_A327 / PARTIAL.

This packet starts from the RS-feasible selected-class hypergraph checkpoint
`2e134d7`, thins the selected supports to exactly `327` for all seven witnesses,
and prepares the explicit received-word exact lift over `GF(17^32)`.

It is still INTERLEAVED_LIST work only. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Source candidate

The source selected-class hypergraph had:

```text
supports = [351,351,351,351,351,351,351]
max_pair_count = 231
pair7_counts = [231,231,231,193,231]
pair_B_values = [743,743,743,705,743]
selected_class_size_counts = {4: 103, 5: 409}
```

It was RS-feasible, but it had `2457` selected incidences. An exact lift with
variables for seven degree-`<256` codewords plus received values has only
`7*256 + 512 = 2304` variables, so the unthinned system is an unnecessarily
overdetermined first target.

## Thin target

The thinning stage removes selected incidences while preserving the coordinate
count. The target constraints are:

```text
supports exactly 327 for all seven witnesses
selected incidences = 7*327 = 2289
pair_ij <= 255 for all pairs
pair_i7 >= 142 for i=1,...,5
```

The first scan found lift targets for all seven thinning strategies. The best
target uses `balanced_support_thin`:

```text
supports = [327,327,327,327,327,327,327]
selected_incidence_count = 2289
max_pair_count = 194
pair7_counts = [194,194,194,193,194]
pair_B_values = [706,706,706,705,706]
selected_class_size_counts = {3: 2, 4: 267, 5: 243}
```

## Exact lift formulation

The exact lift uses explicit received-word variables:

```text
P_1,...,P_7 in GF(17^32)[X]_{<256}
r_h for h in H
P_i(h) = r_h for i in C_h
```

There are `2304` variables and `2289` selected-class equations before any gauge
constraint. The audit may add one gauge equation, such as `r_0=0`, when running
rank/nullity extraction.

No equalities are imposed among witnesses outside the selected received class
`C_h`.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

Run the Sage audit over `GF(17^32)`. If the thin system has useful nullity,
sample exact vectors and evaluate their agreements directly against the solved
received word `r_h`. A board-moving result requires seven distinct
degree-`<256` codewords and agreement at least `327` for all seven witnesses.
