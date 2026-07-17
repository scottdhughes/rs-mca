# M1 KoalaBear branch-3--5 mask-contract certificate

This directory freezes the source-status, first-match, and quantifier contract
in
`experimental/notes/m1/m1_kb_branch3_5_mask_contract_v1.md`.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --check
python3 -O experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.sage
```

After an intentional source edit, regenerate only after observing the expected
check failure, then replay the checks:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --write
python3 experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --check
```

The verifier strictly rejects duplicate JSON keys and non-finite values,
compares canonical JSON bytes, validates predecessor payload hashes and
load-bearing semantic fields, and recomputes all deployed integers, the
complete dyadic Q0 status table, source hashes, and exact `n=16,j=7` semantic
controls.  The controls
check witness-to-slope existential projection, the universal complement after
an existential owner, complete-selector minimization over a toy list explicitly
declared exhaustive, canonical Q0 full-fibre
membership, and first eligible rung assignment.  The Sage replay independently
checks the exponent fibres against the actual power map on `GF(17)^*` and
verifies the corresponding locator factorizations.  Both implementations also
check the load-bearing `c>j` edge: raw zero-core membership is tautological but
does not create branch-4 route eligibility.

The certificate supports only these conclusions:

```text
BRANCH2_ENVELOPE_STATUS_REFRESHED
BRANCH3_SELECTOR_QUANTIFIERS_FROZEN
Q0_CO_SUPPORT_MEMBERSHIP_EXECUTABLE
Q0_ZERO_CORE_TAUTOLOGY_EXCLUDED_FROM_BRANCH4
GLOBAL_BRANCH1_TO_5_MASK_REPLAY_REMAINS_OPEN
BRANCH5_COMPLEMENT_FORBIDDEN
NO_LEDGER_MOVEMENT
```

It does not prove a deployed slope count, a complete branch-3 projector, a
branch-5 planted family, a complement after branches 3--5, or the KoalaBear
safe row.  In particular, the toy complete-selector helper is not a deployed
selector enumerator; a universal deployed complement still requires a
certified exhaustive complete-selector universe.
