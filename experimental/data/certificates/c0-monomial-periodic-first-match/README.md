# Frozen periodic first-match packet

This directory preserves the complete proof trail for the local theorem in
`experimental/notes/l2/c0_monomial_periodic_first_match_payments.md`.

## Components

- `C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md` proves the fixed-residual q64
  three-invariant cap for every full-fiber weight `0..29`.
- `C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md` proves the complete
  projective-ray cap `1,619,679,744` at q64 `f=29`.
- `C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT.md` proves the complete projective-ray
  cap `83,970,774,720` at q64 `f=28`.
- `C0_Q128_F59_SINGLETON_B1_7_PAYMENT.md` proves the q128 certificate and
  prints the coarse-first new subtotal `16,501,819,170,137,728` for `b=5,7`.

Each theorem has a claimant verifier and canonical output plus a separately
written hostile audit and replay.  The original `work/` layout is preserved so
the frozen verifiers can enforce their source hashes.  Run all eight scripts:

```bash
cd work
for f in verify_*.rb audit_*.rb audit2_*.rb; do
  ruby --disable-gems -w "$f"
done
```

The source proofs state complete periodic strata.  The repository-facing note
applies the additional current-main first-match deletion: q64 footprint at
most 31 is owned before these cells.  Thus only q64 `f=29` residual footprint
at least 3, q64 `f=28` residual footprint at least 4, and q128 `b=5,7` are
charged.  The q32 `f=14` alternate decomposition and q128 `b=1,3` are not
additional owners.

This is a local monomial-owner packet.  It proves no complete parent and no
official score change.
