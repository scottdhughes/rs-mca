# M1 a327 RS-feasible value-class hypergraph pre-solver

Status: RS_HYPERGRAPH_SEARCH / CANDIDATE / EXPERIMENTAL.

This packet corrects the first value-class hypergraph pre-solver by adding the
hard Reed-Solomon pairwise liftability constraint. It is a discrete selected
received class search, not an exact GF(17^32) lift, not an MCA row, and not a
public proof record.

Track: INTERLEAVED_LIST.

Row: `RS[F_17^32,H,256]`.

Denominator: `17^32`.

Agreement target: `327`.

`mca_counted=false`.

## Pairwise co-occurrence cap lemma

Let `P_i` and `P_j` be distinct degree-`<256` polynomials over `GF(17^32)`,
evaluated on the subgroup `H` of order `512`. If `P_i(h)=P_j(h)` on at least
`256` points of `H`, then `P_i-P_j` is a nonzero degree-`<256` polynomial with
at least `256` roots, impossible. Therefore any exact lift to seven distinct
codewords must satisfy

```text
|{h in H : P_i(h)=P_j(h)}| <= 255
```

for every pair `i != j`.

The best `e4e966a` full-partition hypergraph violates this bound. Its
representative skeleton contains `331` coordinates with block `[1,2,3,4,7]`
and `181` coordinates with block `[2,3,4,5,7]`, so several pairs co-occur on
more than `255` coordinates. The verifier records this as
`RS_HYPERGRAPH_PAIR_CAP_FAIL`.

## Selected received class model

The new model chooses only a selected received class `C_h` at each coordinate:

```text
P_i(h) = r(h) for i in C_h.
```

It does not impose equalities among witnesses outside `C_h`. This avoids
accidental nonselected equalities such as forcing `[5,6]` on hundreds of
coordinates.

The constraints are:

```text
support_i = #{h : i in C_h} >= 327
pair_ij   = #{h : i,j in C_h} <= 255
pair_i7  >= 142  for i=1,...,5
```

The pair-7 lower bound corresponds to the two-witness Hall guard:

```text
B({i,7}) = 512 + pair_i7 >= 654.
```

The first pass tests selected class sizes `4` and `5`, plus a small
`3/4/5` exploratory profile. Sizes `4` and `5` are natural because
`7*327/512 ~= 4.47`.

## Split probes

Split probes are applied to selected classes containing the fragile
`[1,4,5,7]` pattern. They keep the side containing witness `7` and all
non-fragile members of the selected class. This tests whether the selected
received class can survive the same qualitative splits that broke the old
repaired-skeleton basin without globally damaging unrelated pair-support
classes.

The probes are:

- `split_4_from_157`;
- `split_14_vs_57`;
- `split_1_from_457`;
- `split_15_vs_47`;
- `split_17_vs_45`.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- an exact `GF(17^32)` lift.

## Next step

The first scan found RS-feasible selected-class hypergraphs in all five tested
profiles. The best first-pass target has:

```text
supports = [351,351,351,351,351,351,351]
max_pair_count = 231
pair7_counts = [231,231,231,193,231]
pair_B_values = [743,743,743,705,743]
selected_class_size_counts = {4: 103, 5: 409}
best_robustness_score = 24
```

It satisfies the hard pair cap `pair_ij <= 255` with margin at least `24`, and
it keeps all five `{i,7}` Hall guards above `654`.

The next branch should lift this selected-class candidate using explicit
received-word variables `r_h` and equations `P_i(h)=r_h` for `i in C_h`.
If the selected-class lift fails, the proof direction becomes a cycle/rank
obstruction for an RS-feasible support design, not the old value-class
pair-cap issue.
