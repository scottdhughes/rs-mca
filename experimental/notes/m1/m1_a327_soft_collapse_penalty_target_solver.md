# M1 a=327 soft collapse-penalty target solver

Status: `TESTED_TARGET_SYSTEMS_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `0fb00ee`, where hard split constraints removed the known
six-witness collapse class but destroyed proxy capacity. The purpose here is to
test the interpolation between the two extremes:

```text
high collapse dominance, high capacity, degenerate
hard collapse removal, low capacity
```

The search softly penalizes target rows associated with the collapse class
`[1,3,4,5,6,7]` instead of forcing inhomogeneous split equalities.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

The scanner starts from the top three robust proxy systems and reruns target
coordinate selection with a soft collapse penalty. It uses row budgets:

```text
512, 576, 640
```

and collapse penalty weights:

```text
0.01, 0.03, 0.1, 0.3, 1.0
```

for four objective variants:

- `soft_collapse`;
- `soft_collapse_plus_variance`;
- `soft_collapse_plus_fiber`;
- `soft_collapse_plus_witness2_repair`.

For every selected target system, the scanner solves the homogeneous proxy
coefficient system over `GF(12289)`, samples the nullspace, evaluates the seven
codewords on `H`, and runs the exact proxy received-word rescheduler when the
capacity upper bound is at least `327`.

The Sage script is a gate only. Exact `GF(17^32)` reconstruction is required
for any future proof record and is triggered only after a collapse-reduced
proxy candidate appears.

## Result

The bounded first pass tested:

- 3 robust proxy seed systems;
- row budgets 512, 576, and 640;
- 5 collapse-penalty weights;
- 4 soft objective variants;
- 180 target systems;
- 60 unique selected/RREF cores;
- 2,880 proxy codeword tuple samples.

The soft penalty preserved the high-capacity proxy mechanism:

```text
best proxy max-min = 332
best agreement vector = [332,333,332,332,332,332,332]
best capacity upper bound = 460
proxy-positive systems = 60
```

However, none of the proxy-positive systems reduced the evaluated collapse
class. The best sample remains:

```text
HIGH_CAPACITY_DEGENERATE
best_six_class_dominance = 359
collapse_reduced_proxy_candidates = 0
```

This is a useful contrast with the hard-split checkpoint:

- hard splits reduce six-class dominance to `0` but destroy capacity
  (`best capacity = 162`);
- soft penalties preserve capacity and improve proxy max-min to `332`, but the
  high-capacity samples remain dominated by the `[1,3,4,5,6,7]` collapse.

No exact `GF(17^32)` extraction was triggered.

## Status labels

`CANDIDATE` means a collapse-reduced proxy candidate reached `a>=327` and
needs exact `GF(17^32)` extraction.

`TESTED_TARGET_SYSTEMS_NO_A327` means this bounded soft-penalty layer found no
collapse-reduced proxy `a>=327` candidate.

`PARTIAL` means broader soft objectives, exact-field target selection, and
nonlinear collapse penalties remain open.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
