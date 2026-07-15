# Independent final-package review: `31321`

**Reviewer:** fresh-context Codex read-only final-package audit, 2026-07-15.

Verdict: GREEN

Ledger authorization: YES

No blocking mathematical, certificate, scope, formatting, or replay defect was
found in the seven frozen unbanked final-package artifacts below.

## Frozen artifacts reviewed

| artifact | SHA-256 |
|---|---|
| owner verifier | `1a1044b60f2df17ee5c50469f086f7254230a39a25de4e8c57ce80ab507e8421` |
| owner certificate | `f0b35bc43cb69ae3fcd0bcc095fc5f5185af9294c94af5375efd7324ae921f32` |
| CRT verifier | `60391b3642f1d15f86ed120646e4c73a78a50b55b1e4338747e0f35c16f58de4` |
| CRT certificate | `f57b458a3b6ba1c7daa5098bcea8f796ba39294ddc046398c9310708d884917b` |
| ledger verifier | `b94e1cd5e0c547224cb205eb8c944257cba9cc6b0ddcfbbb4e35eb868ae12954` |
| ledger certificate | `73d18b2694e5c0bb0d6cb4eedf2fcd37881cb801eba6ca840ba0fef56054f9b6` |
| lemma note | `a175ebf807a93df85f915e50ff73de9d7d5eaf781b15ae667c2073392b9dfc77` |

The certificates are correctly unbanked at these hashes because the two new
final-package review files do not yet exist.  That is the intended input state
for this review, not a mathematical YELLOW.

## Mathematical and ledger findings

- The owner packet enumerates 1,152 unique aggregate keys and 4,608
  restored-core refinements.  It leaves all 1,152 keys to the algebraic layer,
  records twelve periodic refinements without subtracting them, and preserves
  the no-factor-four aggregate-key semantics.
- For support degrees `(3,2,1)`, the fixed system is `12 x 9` of rank nine and
  the moving monic system is `12 x 12`; its compatibility quotient is the
  affine `3 x 3` map in coefficients `X^3,X^4,X^5`.
- A compatible rank drop gives
  `B | F_0 V_1-F_1 V_0` with cross-degree at most five below
  `deg(B)=6`.  The resulting common-factor argument is sound.  Under the
  explicit split-squarefree, block-disjoint, zero core/background-data bridge,
  it migrates exact `d=3` to `d<=2`.
- The exact `GF(19)` census remains 1,108 full-rank systems and 44
  affine-inconsistent rank-two systems, with no compatible rank drop.  The
  finite compatible-drop branch is therefore correctly labelled vacuous; the
  universal degree-gap proof, not the census, carries the implication.
- The complete 75-row replay recomputes the local replacement
  `21,888 -> 1,152`, the all-profile total `641,512 -> 620,776`, and the
  unresolved total `104,914 -> 84,178`.  The dynamically selected next row is
  `(4,4,2,2,(3,3))`, `(G2,GR)=(2,3)`, with charge `17,328`.

## Final-package and stale-state audit

- The CRT and ledger module docstrings now describe the content-addressed gate
  conditionally and no longer claim that the final packet is still awaiting
  the earlier review wave.
- The prior `31222` control is now labelled only as a nonvacuous degree-six
  control; it no longer says the already reviewed specialization still needs
  its own review.
- The owner certificate's YELLOW is layer-local and remains accurate: the
  existing-owner stack alone does not perform or authorize the CRT payment.
  Its interface wording no longer presents discharged downstream work as
  currently pending.
- The lemma names the actual next unresolved row, preserves zero
  core/background data in the stop conditions, and distinguishes the earlier
  four-core-hash review wave from this seven-artifact final-package wave.  It
  says only the latter pair is linked by the final certificates.
- The two prior GREEN reviews, the earlier YELLOW review, and the turn-limit
  attempt are retained only as audit history.  No stale PENDING/YELLOW claim
  remains in a final banked artifact outside conditional gate branches or the
  truthful owner-layer status.

## Replays and package checks

- Owner normal replay: PASS; supplied tamper suite: 16/16 caught.
- CRT normal replay: PASS; supplied tamper suite: 37/37 caught in the frozen
  no-final-review state.
- Ledger normal replay: PASS; supplied tamper suite: 18/18 caught in the same
  state.
- All three JSON certificates parse; all present declared paths and SHA-256
  links match; in-memory Python source compilation passes.
- Tracked `git diff --check` and an untracked-inclusive
  `git diff --no-index --check` sweep are clean.
- Every script path printed in the reproduction blocks exists, and
  `/usr/local/bin/sage` is executable.
- No cache, bytecode, or Sage-preparser output is tracked.  Local generated
  `__pycache__` and `*.sage.py` files remain ignored.
- The worktree base is exactly PR #801 head
  `2671d4a261ceb8f90102ba50f6162e61356b291d`; the candidate diff is confined
  to the `31321` owner/CRT/ledger packet, its lemma, ledger/log integration,
  and explicitly retained review history.

## Authorization and remaining scope

I authorize adding this review, obtaining a genuinely distinct fresh Claude
review of the same seven hashes, regenerating the CRT and ledger certificates
so the two-review gate banks, and replaying all normal and tamper checks.  The
mechanical post-review regeneration must not change any mathematical
fingerprint, census value, ledger total, or next-row selection.

This authorization is only for the frozen local `21,888 -> 1,152`
replacement.  It does not authorize periodic-refinement subtraction, a
restored-core factor four, `m>2`, PR #763, Lean, cross-`r` aggregation, or a
global mixed-petal theorem.
