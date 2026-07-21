# M31 whole-ball source/separator compiler certificate

This directory pins the exact certificate for
`m31_whole_ball_source_separator_compiler.md`.

The packet proves a local algebraic theorem and a global route cut; it does
not close either M31 list row. Its strongest local conclusion is that every
rank-deficient factorized parity four-face at the deployed truncation belongs
to one of exactly 137 Pluecker defect cells

```text
tau=0,...,136,
h=137-tau.
```

The whole-ball compiler remains fail-closed because no universal source
selection, interior-weight payment, unrestricted rank-16 classification, or
global disjoint add-back is supplied. Accordingly all ledger atoms are null
and ledger movement is zero.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --check
python3 -O experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --check
python3 experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --tamper-selftest
sage experimental/scripts/verify_m31_whole_ball_source_separator_compiler.sage
```

The Python verifier reconstructs the deployed integer arithmetic, the exact
137-cell defect window, the full `GF(7)` census, all Pluecker signs, the six
CRT congruences, and a `GF(23)` rank-drop control whose twelve-point support
has trivial `PGL_2` stabilizer. The Sage replay independently checks the
symbolic determinant, finite-field ranks, quotients, identities, CRT
residues, and projective stabilizer.

`manifest.json` is canonical and hash-binds the note, both verifiers, this
README, and the inherited source files. Regenerate it only after an intended
source change, then rerun the normal, optimized, tamper, and Sage checks.
