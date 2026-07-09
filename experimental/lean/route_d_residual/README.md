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

## Verification workflow (Scott)

| Layer | Tool |
|---|---|
| **External Lean cert check** | [AXLE](https://axle.axiommath.ai/v1/docs/) (Axiom Lean Engine) — `verify_proof`, `check`, `extract_theorems`, etc. Web UI / `axiom-axle` Python / CLI / HTTP |
| **Local Mathlib search** | Mathlib trees on this machine, e.g. `~/lean-verify/.lake/packages/mathlib/Mathlib` (also other project `.lake/packages/mathlib`). Search there for finite fields, character sums, Gauss sums, geometric progressions before inventing lemmas. |
| **Local build** | `lake build` in this package (phase 1 is stdlib-only; phase 2 will depend on Mathlib) |

When adding theorems: prefer AXLE `check` / `verify_proof` on extracted statements; use local Mathlib for API names and existing lemmas (`Finset`, `ZMod`, `Cyclotomic`, additive characters, etc.).

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
