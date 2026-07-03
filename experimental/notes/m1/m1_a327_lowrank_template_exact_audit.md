# M1 a327 low-rank template exact audit

Status: CANDIDATE / LOWRANK_EXACT_TIMEOUT / PARTIAL / EXPERIMENTAL.

This packet isolates the best low-rank template proxy-positive candidate for
exact `GF(17^32)` auditing. It remains INTERLEAVED_LIST work only. It is not an
MCA row, not protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Candidate

The source candidate is the `mixed_rank6` low-rank template from `e56f3ad`.

```text
template_dimension = 6
effective_cost = 1533
variable_count = 1536
proxy_field = GF(12289)
proxy_rank = 1280
proxy_nullity = 256
```

The exact audit reconstructs the same selected-class coordinate ledger and
template vectors over `GF(17^32)`.

The first bounded Sage run reached the dense exact `matrix.rank()` step on the
compressed low-rank matrix and was interrupted without a rank result. This is an
exact-infrastructure timeout, not a mathematical obstruction.

## Exact objective

The audit computes:

```text
exact rank
exact nullity
pair-projection ranks for all 21 pairs
forced equal pairs, if any
explicit vector, if pair projections clear
```

If the exact kernel is nonzero and no pair-projection is identically zero, then
the finite-subspace avoidance argument gives a seven-distinct vector in the
kernel. The received word is defined by the selected class at each coordinate.

## Non-claims

This packet does not claim:

- an `a=327` certificate unless the Sage proof record is present;
- not an MCA row;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

Build a faster exact-rank path for the compressed `1533 x 1536` low-rank
matrix. If exact rank has positive nullity, continue to pair-projection testing
and deterministic kernel sampling.
