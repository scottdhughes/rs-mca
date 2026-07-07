# M1 a327 mu8 rank3 forced-bundle route-cut summary

Status: experimental, interleaved-list only.

This packet compresses the fixed rank-3 `mu_8` forced-bundle audit into a
small, hash-addressed route-cut summary.  It is intended as a reviewable
alternative to pulling the larger intermediate ledgers directly into a public
PR.

## Scope

The scope is narrow:

```text
fixed rank-3 mu8 menu
+ forced 12-row projective key bundle
+ singleton-boundary repair attempts
```

It does not cut rank-3 globally, the full `mu_8` route, or the global
`a=327` interleaved-list problem.

## What the packet records

The forced bundle itself is balanced:

- forced selected incidence: `336`,
- forced support vector: `[48, 48, 48, 48, 48, 48, 48]`,
- forced pair-count maximum: `48`,
- residual selected incidence need: `1953`.

The scheduler can reach support/pair only with a singleton escape:

- support/pair candidates: `1`,
- strict support/pair candidates: `0`,
- best support vector: `[328, 328, 327, 330, 327, 327, 327]`,
- best selected incidence: `2294`,
- best pair maximum: `255`,
- non-forced repeated projective keys: `0`,
- non-forced singleton projective-key rows: `29`.

The escaped schedule is exact full rank over `GF(17^32)`:

- matrix shape: `[148, 96]`,
- rank/nullity: `96 / 0`,
- positive-nullity systems: `0`,
- pair-visible systems: `0`.

The strongest mined singleton replacement target has 8 rows and selected
incidence 168, but the shared-point exact system has shape `[104, 3]` and
rank/nullity `3 / 0`.  Nontrivial shared-point replacement groups: `0`.

The projective-line relaxation finds two nontrivial line groups, but the best
line bundle covers only 4 target rows, selected incidence 96, and leaves 25
singleton rows.  Its maximum line support is 2, far below the degree-32
threshold for a repeated quotient-line identity.

## Interpretation

This is a local route cut for the fixed forced-bundle menu:

1. If singleton escape rows are allowed, support/pair can pass but exact
   interpolation is full rank.
2. If singleton escape rows are forbidden, this fixed menu loses the
   support/pair front.
3. Mining the existing singleton rows for shared-point or projective-line
   replacements does not produce a material second dependency family.

The next constructive step should engineer line or multi-line dependency
structure upstream in the carrier/menu generator, rather than continuing to
mine it from this fixed singleton escape schedule.

No exact lift, witness, MCA, protocol, global list bound, exact `Lambda_mu`, or
exact `delta*_C` claim is made.
