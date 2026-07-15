# Cross-Model Review: 41331 Shared Auxiliary-Johnson Ledger

## Reviewer and execution record

The reviewer was the locally configured Claude Code CLI in a fresh,
read-only, strict-MCP session. Two earlier broad review invocations were
stopped after they produced no output within the local review window. The
bounded eight-turn review below completed successfully. No reviewer process
modified the worktree.

## Verdict

**GREEN.**

## Ledger authorization

**YES.**

## Findings

- Johnson arithmetic was recomputed independently:
  `|T|=3*4=12`, `a=3+4+1-1=7`, `a^2-d|T|=49-48=1`, and the sharp bound is
  `floor(12*(7-4)/1)=36` per fixed layer.  Corollary
  `cor:capf-pma-johnson` is at
  `experimental/cap25_cap_v13_raw.tex:6367-6377`; the conservative two-layer
  union cap is `binom(4,4)*binom(2,1)*36=72`.
- The fifteen cells are exactly the nonincreasing petal-hit vectors in
  `{1,2,3,4}` with `t` in `{2,3}` and total at least seven. A one-petal cell
  is impossible because one petal has only four points. The two exact `r=1`
  layers are disjoint according to which background point, 16 or 17, is hit.
- Charge arithmetic was recomputed by hand. The fifteen post-32221 charges
  sum to `416,020`; their unresolved-route subtotal is
  `912+5,472+138,624+72=145,080`. Therefore
  `1,192,927-416,020+72=776,979` and
  `357,763-145,080+72=212,755`.
- Normal replay and the nine-mutation self-test passed against the frozen
  shared-ledger certificate. The prior 32221 ledger, owner partition, v5
  common cap, theorem source, and scope-note hashes were current.
- The fourteen zero allocations are explicitly incremental rather than
  standalone zero bounds. The stronger cross-`R_0` charge 36, the next
  `d=4,r=0` row, and all global, `m>2`, and PR `#763` claims remain excluded.
- The periodic-support pattern adds no extra `+1`; the certificate enforces
  `periodic_owner_bound_added_to_cap=false`.
- Coverage by the two fixed layers is sound. With `d=ell=4`, `Y=D_0`, and the
  frozen evaluation domain is exhausted by `Y`, the two background points,
  and `T`; exact `d=4,r=1` codewords satisfy the concrete layer conditions and
  inject through `prop:capf-pma`.

## Non-blocking promotion note

At review time the certificate deliberately remained `banked=false` with a
pending-review verdict. The reviewer authorized the mechanical follow-up:
hash-link this review, flip the pending fields to banked GREEN, regenerate the
certificate, and replay the normal and mutation modes.

Files modified by this review: none.
