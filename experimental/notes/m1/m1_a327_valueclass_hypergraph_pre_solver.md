# M1 a327 value-class hypergraph pre-solver

Status: HYPERGRAPH_SEARCH / CANDIDATE / EXPERIMENTAL.

This packet moves the M1 `a=327` constructive lane one abstraction layer above
exact `GF(17^32)` row schedules. It is a value-class hypergraph pre-solver, not
an exact GF(17^32) lift, not an MCA row, and not a proof record for a public
board entry.

The source checkpoint is `56fd7a9`, the full upstream B47-robust exact scanner.
That exact scanner tested 24 systems, constructed 11 exact vectors, found zero
split-resilient skeletons, and had best robustness score `-92` with best
pre-split capacity `235` and pair values `[575,657,657,575,575]`. The result
does not prove a global obstruction. It says the nearby exact skeleton lineage
remains B47/capacity fragile.

## Scope

Track: INTERLEAVED_LIST.

Row: `RS[F_17^32,H,256]`.

Denominator: `17^32`.

Agreement target: `327`.

`mca_counted=false`.

Non-claims:

- not MCA `N_bad`;
- not protocol soundness;
- not ordinary list decoding beyond the stated interleaved-list predicate;
- not global `Lambda_mu(C,327) <= 6`;
- not exact `Lambda_mu`;
- not exact `delta*_C`;
- not an exact GF(17^32) lift.

## Model

At each of the 512 coordinates, the seven witnesses determine a partition of
`{1,...,7}` into value classes. For a subset `U`, define

```text
B(U) = sum_h max_C |C cap U|.
```

This is the Hall upper bound used throughout the exact lane. For pair subsets
`{i,7}`, the pre-solver records

```text
B({i,7}) = 512 + #{coordinates where i and 7 share a value class}.
```

It also records the all-seven capacity proxy

```text
floor(sum_h max_C |C| / 7).
```

The solver chooses counts of partition types over 512 coordinates and maximizes
a worst guard margin across the unsplit hypergraph and split probes.

## Split-resilient before exact lifting

The key change is that a candidate is not treated as useful merely because its
pre-split guard vector is high. A useful hypergraph must be split-resilient before exact lifting:
it must remain feasible after candidate split probes.

The first split probes are:

- `split_4_from_157`;
- `split_14_vs_57`;
- `split_1_from_457`;
- `split_15_vs_47`;
- `split_17_vs_45`.

Each probe only refines coordinates whose value class actually contains the
fragile `[1,4,5,7]` block. It does not globally split witness 7 away from
unrelated pair-support classes such as `{2,7}` or `{3,7}`.

The robustness score is the minimum over the pre-split state and all split
probes of:

```text
capacity - 327,
B27 - 654,
B37 - 654,
B47 - 654,
B57 - 654.
```

A nonnegative score is a discrete split-resilient Hall-feasible hypergraph. It
would still need an exact polynomial lift over `GF(17^32)`.

## Profiles

The first pass tests bounded partition profiles rather than exact polynomial
systems:

- low-collapse patterns: `2+2+1+1+1`, `3+2+1+1`, `3+3+1`, `4+1+1+1`;
- max-5 partitions with no `[1,4,5,7]`-containing block;
- max-5 partitions with fragile `[1,4,5,7]` caps of 16, 32, and 64;
- all max-5 partitions excluding the six-class basin;
- size-5 capacity-buffer patterns;
- pair-block split-resilience patterns.

The purpose is to decide whether the desired value-class geometry is even
combinatorially plausible before paying for exact `GF(17^32)` lifting.

## Next step

The first scan found split-resilient discrete hypergraphs in 7 of 8 tested
profiles. The best profile has robustness score `38`, capacity upper bound
`365`, pair values `[843,1024,1024,1024,693]`, zero fragile `[1,4,5,7]`
coordinates, and zero six-class-basin coordinates. This is not a witness, but
it is a concrete exact-lifting target.

The next branch should convert the best partition-count skeletons into equality
rows and try an exact lift. If later, broader hypergraph scans fail, the proof
direction would become a combinatorial hypergraph obstruction, still local to
the modeled partition profiles and still not a global `a=327` theorem.
