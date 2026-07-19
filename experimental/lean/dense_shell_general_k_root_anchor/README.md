# Dense-shell general-K root anchor

This stdlib-only Lean 4.14 package kernel-checks the algebraic compiler behind
`experimental/notes/thresholds/dense_shell_general_k_root_anchor.md`:

- a constant decoration factors out of an arbitrary finite decorated charge,
  uniformly in the remaining decoration list; and
- opposite paired class sums cancel in the repaired positive-charge identity.

The source-specific trigonometric input `q_1=1/4` is proved directly in the
note from `u_1=+/-1/3`.  The Lean theorem exposes it as the exact `hconst`
hypothesis rather than adding analytic axioms to this stdlib-only package.

Run:

```bash
lake build
```
