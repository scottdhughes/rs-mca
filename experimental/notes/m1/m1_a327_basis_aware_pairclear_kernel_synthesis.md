# M1 a=327 basis-aware pair-clear kernel synthesis

Status:

EXACT_EXTRACTION_NO_A327 / BAPK_SLOT_PAIR_CLEAR_BROKEN / PARTIAL / EXPERIMENTAL

This packet follows `a1bb7cf` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous backward-synthesis scan showed that pair clearance in a raw
template coordinate does not survive arbitrary stable-basis coordinates. This
branch makes the basis choice part of the search: for the same pair-clear
template specs, it enumerates basis candidates from the highest-support
functional classes plus deterministic random bases, then scores every basis
slot by pair-projection clearance and nonbasis slot support.

No Sage exact lift is attempted in this branch.

## Result

The bounded basis-aware scan tested:

```text
template specs tested = 4
MILP profiles constructed = 4
systems tested = 12
top classes = 14
random bases = 64
structural-pass candidates = 3
basis profiles tested = 2976
slot profiles tested = 17856
pair-clear slot profiles = 0
pair-clear slot-kernel profiles = 0
```

Screen/failure counts:

```text
BAPK_FORCED_IDENTITY = 6
BAPK_LOW_FUNCTIONAL_SPAN = 3
BAPK_SLOT_PAIR_CLEAR_BROKEN = 3
```

The best row is:

```text
template = pairclear_slot5_pair7_guarded
assignment = pair7_block
basis = basisaware_5_8_13_12_14_16
coefficient matrix shape = [11,6]
coefficient rank/nullity = 6/0
best stable-basis slot = 4
slot nonzero rows = 8
forced pair count = 4
forced pairs = P12,P17,P27,P46
```

This improves the previous best forced-pair count from `11` to `4`, so
basis-aware selection is moving the correct obstruction. It still does not
produce a pair-clear coefficient direction in this bounded front.

## Interpretation

This is not a global obstruction. It is a bounded local negative for the first
basis-aware pair-clear synthesis front. The useful signal is that choosing the
basis directly matters: the pair-collapse obstruction dropped substantially.

The remaining issue is now sharper:

```text
stable-basis pair projection can be improved,
but the tested basis families still leave four forced pairs and no slot kernel.
```

The next branch should use the four forced pairs as a repair target, not expand
blindly.

## Non-claims

This packet does not claim:

- an `a=327` certificate
- Sage `GF(17^32)` exact lift
- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- failure outside this bounded basis-aware front

## Next Target

Move to:

```text
m1-a327-basis-aware-forced-pair-repair
```

The target should explicitly repair the remaining forced pairs:

```text
P12, P17, P27, P46
```

Use Python first to bias basis selection and template variants against those
four projection zeros. If this becomes a small algebraic template constraint
system, use Macaulay2/Singular or `msolve`; Sage should still wait until a
realized proxy-positive, pair-clear target exists.
