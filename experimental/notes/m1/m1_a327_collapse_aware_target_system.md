# M1 a=327 collapse-aware target system

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `3d12ee1`, which identified the exact high-capacity
degenerate skeleton:

```text
[1,3,4,5,6,7]
[2]
```

The purpose of this search is to stop trying to split that collapse after the
fact. Instead, it modifies the target system so that selected coordinates impose
internal value-class partitions inside `[1,3,4,5,6,7]` from the start.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

The scanner starts from the robust proxy systems and replaces selected
high-overlap target coordinates with inhomogeneous split constraints for the
known collapse class. Tested split partitions are:

- `{1,3,4} | {5,6,7}`;
- `{1,3} | {4,5,6,7}`;
- `{1,3} | {4,5} | {6,7}`.

For each modified proxy system, the scanner solves the affine system over
`GF(12289)`, samples the affine solution space, evaluates all seven codewords,
and runs the exact proxy received-word rescheduler.

The Sage script is a gate: exact `GF(17^32)` extraction is triggered only if
the proxy search finds a candidate reaching `a>=327` while reducing the known
six-witness collapse class.

## Result

The bounded first pass tested:

- 3 robust proxy seed systems;
- split budgets 8, 16, and 32;
- the three split partitions listed above;
- 27 modified affine proxy systems;
- 216 sampled proxy vectors over `GF(12289)`.

All 27 systems solved and sampled, but every sampled vector fell into:

```text
SPLIT_DESTROYS_CAPACITY
```

The best proxy capacity upper bound was only `162`, below the target `327`.
The known six-witness dominance was removed (`best_six_class_dominance = 0`),
but the split constraints destroyed the high-capacity collision skeleton before
any exact `GF(17^32)` audit was triggered.

This is not an exact-field route cut. It is a proxy-level search audit showing
that these direct inhomogeneous collapse-aware target splits are too rigid in
the tested budgets and partitions.

## Status labels

`CANDIDATE` means a proxy candidate reached `a>=327` with reduced collapse and
needs exact `GF(17^32)` extraction.

`EXACT_EXTRACTION_NO_A327` means this bounded proxy layer found no
collapse-reduced `a>=327` candidate.

`PARTIAL` means broader split budgets, partitions, and exact-field target
selection remain open.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
