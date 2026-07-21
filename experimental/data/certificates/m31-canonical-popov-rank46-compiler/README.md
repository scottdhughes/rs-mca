# M31 canonical-Popov rank-46 compiler

This directory pins the exact contract for
`experimental/notes/thresholds/m31_canonical_popov_rank46_compiler.md`.

The packet separates hand proof from executable evidence.  The accompanying
note proves four scoped statements:

1. every radius-`981,129` list injects bijectively into the lex-first masked
   degree-`R` locus of one Paper-D rank-two interpolation lattice;
2. the complete list mass in weights at most `614,160` is at most `3,730`, by
   the exact integer-balanced incidence inequality (plain Cauchy is too weak);
3. a forbidden list forces signed occupancy at least `259,881` and hence at
   least that many marked rank-46 actual-error packets; and
4. every such packet has a uniform rank-three Forney--Pluecker frame of degree
   at most `62,295<67,447`, terminating in an unpaid common-core or rank-two
   coloop branch.

The executable certificate pins the deployed integer arithmetic, the claimed
terminal labels, and hashes of the proof packet; it does not formalize the
global canonical-injection or Forney--Pluecker arguments.  It also guards the
load-bearing non-merger as an explicit fail-closed contract: an interior global
locator is the actual error locator times a canonical agreement-padding
factor.  It does not automatically share the actual-error syzygy module.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --check
python3 -O experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --check
python3 experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_canonical_popov_rank46_compiler.sage
```

`manifest.json` is regenerated canonically by the Python verifier.  The Sage
script independently replays the exact deployed arithmetic.  Its finite-field
canonical-selector, padding, Popov, Pluecker-divisibility, and coloop examples
are toy controls, not deployed-scale evidence or a formal proof of the hand
lemmas.

The packet fails closed:

```text
M31 list row: OPEN
ledger movement: 0
owner charge: null
```
