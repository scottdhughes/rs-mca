# Fixed-27 quartic branch-envelope certificate

The two CSV files are deterministic outputs of
`experimental/scripts/verify_rank16_fixed27_quartic_branch_envelope.py`.

- `fixed27_quartic_branch_envelope.csv` contains all 12,998 Base-layer rows.
- `fixed27_quartic_branch_internal_states.csv` contains all 25,996 admissible
  dyadic `(c,M)` states. Each state is evaluated under both branch formulas.

The verifier reconstructs both files and byte-compares them before reporting
success. It also pins the exact PR #894/#902/#930 theorem and verifier sources.
