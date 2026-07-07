# Open certificate lanes — mining of the upstream repo (2026-07-06)

A scan of the upstream board, prize DAG, and execution queue for runnable,
non-M1, certificate-producible lanes. Key finding: the repo is **mature and very
active** (26 open PRs across L1/M1/Lean/BC/CAP-g); the prize DAG's `PROVABLE`
statuses are **stale** (e.g. `dyadic_profile_evaluation` is listed PROVABLE but
its note is `Status: PROVED` with a verifier). So the JSON status cannot be
trusted -- each candidate's actual note/PR state must be checked.

## Ranked runnable lanes (open, non-M1)

1. **Complete the low-rate board lanes (RAN this).** Directly observable from
   `site/data/rate-leaderboards.json`: `rho in {1/4,1/8,1/16}` are structurally
   sparse (4 rows each) and lack the exact-gate/tangent row *types* that
   `rho=1/2` carries (`prime-a425-a426-adjacent-gate`, `tangent*`, etc.). Filled:
   - near-capacity **caps** (+87 -> ~+121) -- `board_cap_certificate_generator.py`;
   - **exact-gate** rows -- `curate_pin_gate_board_rows.py`, from the already-verified
     adjacent-threshold pins (a425/a426 gate type, now for the low rates).
   Non-overlapping with M1 (which owns the crowded `rho=1/2` proof-record rows).

2. **`fm1` exact aligned-count identity** `E[#aligned] = C(n,j)(1-q^{-t})q^{1-t}`
   -- DAG `PROVABLE`, no dedicated note found (its adjacent-jump ratio is in
   `staircase_steepness.md`, but the expectation identity itself may be
   uncaptured). If open, a clean Lean-verifiable target like the two-core packing
   lemma. STATUS CHECK NEEDED before claiming.

3. **Other certificate-flavoured `PROVABLE` nodes** (`paid_tan_fn`,
   `paid_quot_fn`, `collision_norm_criterion`, `spi_dim1`, `u1_cramer`) -- require
   reading each note for actual PROVED/open state; several are likely M/L or
   partly addressed in open PRs. Not yet triaged individually.

4. **Board-sweep widening** (a k-ladder of cap rows per rate) -- low marginal
   value (near-duplicate rows); skip.

## What was excluded

- M1 lanes (interleaved-list, a327/mu8, the crowded `rho=1/2` proof-records) --
  owned by the M1 terminal.
- Already-PROVED DAG nodes despite `PROVABLE` JSON status (`dyadic_profile_evaluation`,
  `staircase_steepness`, ...).
- Deep open cruxes (b2 sqrt-p barrier, corrected E_3, `A_te-2`) -- not certificate
  production.

## Method note

The reliable signal for "open" is the board (current, not stale) and each node's
actual note status, NOT the prize-DAG JSON `status` field. Cross-check open PRs
(`gh pr list`) before claiming any queue item (standing order 6).
