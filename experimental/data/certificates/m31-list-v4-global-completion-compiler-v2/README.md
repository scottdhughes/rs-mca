# M31 LIST v4 global completion compiler v2

This certificate freezes the live Grande Finale v4 Mersenne-31 LIST
chronology in its actual unit: distinct codewords per received word.  It
retains the source partition digest, the banked low-weight charge
`U_paid=3730`, and four null atoms.

The certificate derives the exact signed completion gate

```text
Xi46 = T46_interior + T46_boundary - C_low - sum_(r=1)^45 C_r
Xi46 <= 259880.
```

It does not prove that this gate holds for every received word.

It also contains sharp safe and first-forbidden boundary-free arithmetic RLE
fixtures.  They are not received-word constructions.  Their role is to prove
that boundary-only additive/numerical owner hypotheses cannot close the
current global compiler.
The replay also checks all 172 embedded source file hashes and 29 internal
payload/certificate pins in the enumerated post-adapter graph.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --check
python3 -O experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --check
python3 experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --tamper-selftest
python3 experimental/scripts/verify_m31_list_v4_global_completion_compiler_independent.py --check
python3 -O experimental/scripts/verify_m31_list_v4_global_completion_compiler_independent.py --check
```

Passing replay does **not** prove the M31 LIST row safe.  It certifies a
fail-closed contract and a route cut.  `U_Q`, `U_list_int`, `U_ext`, and
`U_new` remain null, and the signed cross-weight theorem remains open.
