# M1 Interleaved-List Threshold Interval Sharpening Sage Audit

Date: 2026-06-27

Status: PROOF RECORD / LOWER BOUND / INDEPENDENT FINITE-FIELD AUDIT.

## Scope

This note audits the sharpened interleaved-list threshold packet for

```text
C = RS[F_17^32,H,256],        |H| = 512.
```

The theorem note proves

```text
Lambda_mu(C,292) >= 7
```

by a 254-root-core linear-overlap construction.  This Sage audit turns the
finite-exclusion existence argument into explicit finite-field witnesses.

It is only an `INTERLEAVED_LIST` lower-bound audit.  It is not an MCA `N_bad`
row and does not assert protocol soundness failure.

## Audited Construction

The Sage script independently:

1. constructs `GF(17^32)`;
2. constructs a cyclic subgroup `H` of order `512`;
3. recomputes `|F|=17^32`, `floor(|F|/2^128)=6`, and
   `minimum_to_clear=7`;
4. builds a 254-root-core polynomial `P_A`;
5. constructs seven degree-`<256` codewords using explicit linear residuals;
6. builds a received word over `H`;
7. verifies that all seven codewords agree with the received word on exactly
   `292` positions;
8. verifies pairwise distinctness of the seven codewords;
9. verifies support intersections are at most `255`, as expected for the
   `[512,256]` Reed-Solomon row;
10. emits canonical support/coefficient hashes.

The controlled overlap pattern is:

```text
x1:  witness 0 and 1
x2:  witness 0 and 2
x3:  witness 0 and 3
x4:  witness 0 and 4
x5:  witness 0 and 5
x6:  witness 0 and 6
y12: witness 1 and 2
y34: witness 3 and 4
```

The resulting overlap counts are

```text
[6,2,2,2,2,1,1].
```

Each witness needs `292-254=38` complement points.  The unique blocks needed
after the controlled overlaps are

```text
[32,36,36,36,36,37,37],
```

which use all remaining `250` complement points after the eight controlled
overlap positions.

## Output

The audit prints:

```text
PASS
Sage reconstructed GF(17^32), subgroup order 512, and a=292 witnesses
Lambda_mu(C,292) >= 7 for the standard interleaved-list predicate
MCA counted: false
witness_descriptors_hash: ...
```

The JSON mode reports:

```text
track = INTERLEAVED_LIST
agreement = 292
lambda_lower = 7
denominator = 17^32
minimum_to_clear = 7
clears_list_gate = true
mca_counted = false
```

## Status Ledger

PROOF_RECORD / LOWER_BOUND:

- `Lambda_mu(C,292) >= 7` for the standard interleaved-list predicate;
- explicit finite-field witnesses over `GF(17^32)`;
- denominator and gate arithmetic verified independently.

NOT CLAIMED:

- no MCA `N_bad`;
- no protocol soundness failure;
- no ordinary list-decoding theorem beyond the stated interleaved-list
  predicate;
- no exact `Lambda_mu(C,292)`;
- no exact `delta*_C`.

## Validation

Run:

```bash
sage experimental/scripts/audit_m1_interleaved_list_threshold_interval_sharpening.sage
sage experimental/scripts/audit_m1_interleaved_list_threshold_interval_sharpening.sage --json
```
