# M1 rank-nine full-projective GM route-cut certificate

This directory freezes the exact `GF((2^23)^6)` compatibility control from
`experimental/notes/m1/m1_kb_rank9_full_projective_gm_route_cut_v1.md`.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_full_projective_gm_route_cut_v1.py --check
python3 experimental/scripts/verify_m1_kb_rank9_full_projective_gm_route_cut_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m1_kb_rank9_full_projective_gm_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m1_kb_rank9_full_projective_gm_route_cut_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_kb_rank9_full_projective_gm_route_cut_v1.sage
```

The Python verifier implements `GF(2^138)` independently with bit-packed
polynomial arithmetic, proves irreducibility of the frozen modulus, rebuilds
the unique `GF(2^23)` subfield and all 55 witnesses, checks the projective
Frobenius rank against every proper absolute subfield, enumerates the 2,047 GM
inequalities, recomputes all ranks and hashes, validates source bindings, and
rejects semantic mutations.  Sage
reconstructs the same object with its native finite-field and matrix systems
and checks the load-bearing values against the JSON certificate.

The certificate supports only these conclusions:

```text
FULL_PROJECTIVE_GM_DECLARED_FAMILY_COMPATIBILITY_CERTIFIED
GENERIC_FULL_PROJECTIVE_OR_GM_EMPTINESS_SHORTCUT_REFUTED
```

It does not classify the control as an existing paid owner or as
`UNPAID_PRIMITIVE`.  The declared 55-slope family is proper, the deployed
KoalaBear domain and first-match masks are absent, and the ledger movement is
exactly zero.
