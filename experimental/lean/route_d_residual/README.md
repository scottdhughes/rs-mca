# Route-D residual — Lean phase 1

Stdlib-only formalization seed for the KB-MCA Route-D residual card.

## What is formalized now

- Deployed constants (`p`, `n`, `e`, `n'`, `H2`, `BstarSq`) with `native_decide` certificates
- Soft-B square bound `B * B ≤ 2 * H2` and floor `BstarFloor = 393171`
- Closure ledger nodes (closed / open / conditional) matching the Python board
- Honest flag `fullResidualClosed = false`

## What is NOT formalized

- `SoftB_Deployed` (analytic free-1 high bound) — **OPEN**
- Unconditional `|T| ≤ H2`
- `A_SP ≤ t·p`
- Finite-field / GP character sums (needs Mathlib; phase 2)

## Build

```bash
cd experimental/lean/route_d_residual
lake build
```

Toolchain: `leanprover/lean4:v4.31.0` (same pin as `experimental/lean/rs_mca_formalization`).

## Sources of truth

| Layer | Path |
|---|---|
| Human closure board | `experimental/notes/thresholds/kb_qatom_route_d_CLOSURE.md` |
| JSON certificate | `experimental/data/certificates/kb-qatom-route-d-v67/` |
| Python verifier | `experimental/scripts/verify_kb_qatom_route_d_v67_closure_board.py` |
| STATUS | `experimental/notes/thresholds/kb_qatom_route_d_STATUS.md` |

## Policy

Do not flip `fullResidualClosed` to `true` until `SoftB_Deployed` is proved
and composed with the combinatorial chain (v53–v58). Prefer reviewer ≠ generator
for SoftB when it lands.
