# Cross-Model Review: `d=4,r=0` Shared Auxiliary-Johnson Ledger

Review model: Claude CLI, fresh read-only packet review.

The first broad invocation reached its 12-turn limit without a verdict.  It is
not used as evidence.  A second, narrower invocation completed successfully,
read the theorem anchors and exact packet, and returned the review below.

## Statement audited

For the frozen sequential row
`(q,n,k,sigma,ell,M,b)=(19,18,5,3,4,3,2)`, the complete exact `d=4,r=0`
stratum is one fixed sunflower auxiliary layer (`D_0={0,1,2,3}=Y`,
`R_0=empty`), so its combined banked-41331 charge regroups as
`135,470 -> 3`, changing totals to all-profile `776,979 -> 641,512` and
unresolved `212,755 -> 104,914`.  This is a local ledger claim only.

## Checks

- **One concrete layer.**  `d=4` forces `D_0=Y` and `r=0` forces
  `R_0=empty`.  Exact `d=4,r=0` means zero core and background agreements.
  Since `Omega=Y disjoint-union {16,17} disjoint-union T`, the
  no-outside-agreements clause holds.  The injection is `G_P=P-P_star`, has
  degree at most four, and agrees with the one fixed `U_D0` on at least eight
  points of `T`.
- **Johnson cap 3.**  `|T|=12`, `a=8`, and `d=4`.  The uniqueness part is
  inapplicable because `2a=|T|+d`, but the strict list-bound margin is
  `a^2-d|T|=16>0`, and `12*(8-4)/16=3`.
- **Eleven exhaustive disjoint cells.**  The reviewer independently derived
  the one `t=2` cell and ten `t=3` cells, their pattern multiplicities
  `3,1,12,18,12,48,144,96,108,64,288`, aggregate multiplicity `794`, total
  charge `135,470`, and unresolved subtotal `107,844`.
- **Cap and carrier charged once.**  The single carrier is the original
  unresolved `(3,3,2)` cell.  Ten zeroes are explicitly incremental
  bookkeeping, not standalone zero bounds.
- **Totals.**  The reviewer independently recomputed
  `776,979-135,470+3=641,512` and
  `212,755-107,844+3=104,914`.  The next unresolved row is `(3,1,(3,2,1))`
  with charge `21,888`.
- **No cross-`r` saving.**  The banked `r=1` cap `72` is untouched.  No
  `72+3 -> 36` claim is used.
- **Content hashes.**  All six pre-review linked-input hashes were recomputed
  and matched, including the GREEN independent review and the banked 41331
  predecessor.
- **Aggregate-multiplicity nonclaim.**  The packet explicitly says that 794
  is not a realized-codeword census.

## Commands and exact results

```text
python3 -B experimental/scripts/verify_l1_b9_d4r0_shared_auxiliary_ledger.py
PASS: 11 profiles; 135470 -> 3; 776979 -> 641512;
      212755 -> 104914; next charge 21888.

python3 -B experimental/scripts/verify_l1_b9_d4r0_shared_auxiliary_ledger.py \
  --tamper-selftest
PASS: all 21 mutations CAUGHT; TAMPER-SELFTEST: PASS.
```

## Verdict

**GREEN.**  The exact local banking `135,470 -> 3`, with totals `641,512`
and `104,914`, is sound.

## Ledger authorization

**YES.**  `banked=true` is authorized for this local ledger row after the
status flip is regenerated through the verifier and both normal and mutation
modes pass again.

## PR-worthiness

**YES.**  The bounded verifier, certificate, scope note, and reviews are
consistent, hash-linked, replayable, and mutation-tested.  Add the required
`experimental/agents-log.md` entry.

## Remaining risks

1. The final `banked=true` state must itself be regenerated and replayed.
2. The concrete received-word structure is imported from the banked
   41331/owner-partition chain rather than re-derived here.
3. Positive unresolved mass `104,914` remains.  The next row has zero
   auxiliary margin and needs a different owner argument.
4. Full-report equality makes the mutations strong but coarse; a future
   refactor of `build_report` must preserve the individual semantic checks.

## Minimal next action

Flip `banked` to true and the verdict to GREEN through the verifier's write
path, rerun both modes, then commit the bounded packet with an agents-log entry.

No global theorem, `m>2`, PR `#763`, Lean, or cross-`r` saving is authorized.
