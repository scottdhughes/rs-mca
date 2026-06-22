# M1 Cycle84 Public Replay Audit

Status: AUDIT / FINITE_MODEL_PROOF / PUBLIC_REPLAY.

Date: 2026-06-22.

Source PR: `#96`, `cycle58-5p5-audit`.

Public replay:

```text
repository: DannyExperiments/rs-mca-prz-fork
workflow: Cycle84 certificate replay
run id: 27889140962
run URL: https://github.com/DannyExperiments/rs-mca-prz-fork/actions/runs/27889140962
head commit: 3914f4d08b6ca5b919c84fe2598e4e74685caec4
event: workflow_dispatch
status: completed
conclusion: success
created: 2026-06-21T01:01:44Z
completed: 2026-06-21T01:09:37Z
```

## Verdict

Cycle84 is interesting and worth banking, but only as a finite-model
certificate. It does not prove the Proximity Prize statement, does not promote
Paper B's corrected MCA conjecture to a theorem, and does not justify edits to
the main papers without a separate transfer theorem.

The public GitHub Actions replay materially improves the provenance of the
finite result: both the lightweight certificate chain and the full projected
census plus kernel-lift replay completed successfully on a public runner.

The banked finite-model certificate is:

```text
compatible pairs        = 52,747,567,104
Occ(beta)               = 52,747,567,092
D                       = 24
double fibers           = 12
fibers of size >= 3     = 0
m_max(beta)             = 2
```

This closes the finite wall:

```text
W-CYCLE84-MITM-DUPLICATE-DETECTOR-EXECUTION
```

by the stronger finite statement:

```text
L-CYCLE84-EXACT-COLOR-FILTERED-MMAX: m_max(beta)=2.
```

## What Was Checked Here

This repository-side audit used git/GitHub metadata and PR blobs as text only.
No PR script was run locally, no artifact zip was unpacked locally, and the PR
branch was not checked out as a worktree.

The public run metadata reported two successful jobs:

```text
Light certificate chain
conclusion: success
job id: 82529457638

Full projected census and kernel lift
conclusion: success
job id: 82529457653
```

The workflow file in PR #96 asserts, in the light job, the markers:

```text
CYCLE84_EXACT_MMAX2_CERTIFICATE_VERIFIED
"exact_true_m_max": 2
"exact_true_occupancy": 52747567092
```

The full replay job recompiles and reruns the projected census and kernel-3
duplicate lift, asserting:

```text
TAU_FOLDED_PROJECTED_MMAX_LE_12
KERNEL_3_DUPLICATE_LIFT_COMPLETE
true_double_fibers = 12
exact_true_ordered_offdiagonal_energy = 24
exact_true_m_max = 2
exact_true_occupancy = 52747567092
```

## Security / Integration Decision

PR #96 should not be merged as-is.

Reasons:

- It adds a live GitHub Actions workflow under `.github/workflows/`.
- The workflow compiles and runs C++/Python code extracted from zip bundles in
  the PR.
- It adds 1,530 files and about 1.17M inserted lines, mostly raw prompt,
  response, archive, and generated provenance material.
- The workflow is `workflow_dispatch`, not `pull_request_target`, and no secret
  use was visible in the YAML inspected here. Still, once merged it would be
  executable infrastructure in this repository, with the usual GitHub runner
  network and token environment available to job code.

Integration policy for this repository:

```text
Bank the compact finite replay receipt and mathematical status.
Do not bank the live workflow, raw zip bundles, generated transcript archive,
or executable replay machinery unless a human explicitly requests a full
artifact-preservation branch.
```

## Why It Matters

Cycle84 removes one finite computational uncertainty from the M1/Fable-loop
route. Earlier cycles only reduced the occupancy problem to a direct
`m_max(beta)<=12` or collision search. Cycle84's public replay says the explicit
finite model is much cleaner than required:

```text
m_max(beta)=2 << 12.
```

That is useful evidence and a reusable finite certificate for later transfer
work. It is not yet a theorem about all smooth Reed--Solomon MCA instances.

## Remaining Wall

The next exact question is not the finite census. It is the transfer/relevance
step:

```text
Which theorem turns the Cycle84 finite color-filtered spectrum into an official
MCA, line-decoding, or Proximity Prize frontier statement?
```

Until that bridge is proved, use Cycle84 as:

```text
AUDIT / FINITE_MODEL_PROOF / PUBLIC_REPLAY
```

and not as:

```text
PROVED prize theorem
PROVED corrected MCA conjecture
main-paper replacement theorem
```
