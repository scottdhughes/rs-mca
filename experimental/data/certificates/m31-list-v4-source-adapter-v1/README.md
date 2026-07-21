# M31 LIST v4 source-adapter certificate

This directory freezes the machine-readable contract for the deployed
Mersenne-31 list row at agreement `1116023` and target `2^-100`.

The certificate records one bankable codeword payment,

```text
LOW_EXACT_WEIGHT_PACKING -> U_paid <= 3730,
```

and an exhaustive boundary/interior `U_new` residual whose integer payment is
still null.  Under a hypothetical list of size at least `16777216`, the exact
occupancy identity forces at least `259881` marked target-codeword keys.
Every such key has a three-row coupled locator--numerator frame of combined
degree at most `62295<67447`.

The manifest does not claim a safe endpoint.  It keeps `U_Q`, `U_list_int`,
`U_ext`, and `U_new` null, treats the lexicographic first-45/excess keys only
as diagnostic witnesses, and makes no quartic-field 68-support cutoff claim.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --check
python3 -O experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --check
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py --check
python3 -O experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py --check
/usr/local/bin/sage experimental/scripts/verify_m31_list_v4_source_adapter_v1.sage
```

The Python verifiers check the exact row arithmetic, strict schema, payload
and partition digests, and live source hashes independently.  The Sage replay
is a toy-scale `GF(11^2)` cross-field control for the algebraic lift; it is
not an asymptotic or deployed-field proof.  The symbolic proof is in
`experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md`.
