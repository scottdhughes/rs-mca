# M31 Sidon / three-fibre / escape compiler certificate

This directory pins the fail-closed certificate for
`m31_sidon_three_fibre_escape_compiler.md`.

The packet proves four exact statements.

1. Every forbidden-size exact list contains at least 36 same-weight supports.
2. A forbidden-size Sidon support model satisfies the frozen pairwise,
   `K+2`-shadow, and independently completed local-line constraints while
   containing no factorized parity four-face.
3. Every conditionally selected PR #1003 rank-drop cell produces a separable
   rational map with three almost-complete fibres in the literal Chebyshev
   domain.
4. Every such face is exactly `ESCAPE_KILLED` by one of twelve quotient
   collisions, or is an `ACTUAL_HYPERPLANE_SURVIVOR`.  Every `tau=0` face is
   in the second class.

The exact `T8/F31` replay further gives 720 rank-three ordered faces, all
escape-valid; their 30 unordered support faces are primitive with respect to
the full domain `PGL_2` stabilizer and nontrivial dyadic folds.  No claim is
made about every unrelated ledger owner.  One explicit center has a complete
radius-three list of size five.  These are toy-scale falsifiers, not deployed
M31 evidence.

The packet does not extract a source-valid parity face from the same-weight
packet, classify general rank packets, prove a data-compatible quotient
owner, cover the interior, or give a global disjoint add-back.  Accordingly
all ledger atoms are null and ledger movement is zero.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --check
python3 -O experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --check
python3 experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --tamper-selftest
sage experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.sage
```

The Python verifier reconstructs all deployed integers, all 137 cells, the
Sidon arithmetic, the complete `T8/F31` rank/escape census, and the explicit
closed toy list.  The Sage replay independently verifies the exact extension
field modulus, Sidon control, Chebyshev census, full domain stabilizer,
Pluecker quotients, three-fibre identity, escape guards, and toy list.

`manifest.json` is canonical and hash-binds the note, both verifiers, this
README, and the inherited PR #1001/#1003 sources.  Regenerate it only after an
intended source change, then rerun every normal, optimized, tamper, Sage, and
predecessor check.
