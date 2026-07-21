# M31 `c=2048` partial-occupancy / 30-carrier certificate

This packet certifies an exhaustive exact-boundary reduction for the deployed
Mersenne-31 LIST row.

It proves:

```text
261192 total c=2048 occupancy profiles
    = 616 C1-shaped Euclidean-remainder faces
    + 260576 bi-deep profiles;

260576 bi-deep profiles
    = 31712 visible-arm profiles
    + 228864 double-strict profiles;

bi-deep codewords <= 29*260576 = 7556704
    OR one fixed profile contains a 30-codeword subpacket;

30 columns => nu_1+nu_2 <= 65262 < 67447,
29 columns => current aggregate upper 67680 > 67447.
```

The 30-column statement is over the deployed target field
`GF((2^31-1)^4)`.  The symbolic note explicitly repeats the arbitrary-size
PID/cofactor argument after dividing the common core of the entire exact
layer; it does not truncate the older 46-column frame.

The packet does not pay the resulting carrier.  It also does not turn the
616 C1-shaped faces of an arbitrary target-field word into an active C1
atom.  That step still needs the missing boundary-to-prefix adapter and a
numerical payment.  The conditional boundary allocation includes the full
disjoint charge of both the C1-shaped face owners and every carrier owner:

```text
3730 + 7556704 + 9216781 = 16777215
```

Carrier codewords cannot be deleted for free, and existence of one
30-subpacket is not itself an admissible pruning rule.  The allocation leaves
no reserve for high interior weights and is not a row closure.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_c2048_partial_occupancy_30carrier_v1.py --check
python3 -O experimental/scripts/verify_m31_c2048_partial_occupancy_30carrier_v1.py --check
python3 experimental/scripts/verify_m31_c2048_partial_occupancy_30carrier_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_c2048_partial_occupancy_30carrier_v1.py --tamper-selftest
HOME=/tmp TMPDIR=/tmp sage experimental/scripts/verify_m31_c2048_partial_occupancy_30carrier_v1.sage
```

The Python verifier uses only the standard library.  It regenerates the
manifest, exhausts the deployed profile inequalities, enumerates all `11,440`
supports in an independent four-fiber toy, checks live source hashes and
internal predecessor seals, and rejects every semantic mutation.

The Sage replay independently enumerates the deployed profile pairs, checks
all exact budgets and Forney thresholds, exhausts `GF(17)^*` under
`phi(X)=X^4`, verifies reciprocal unit-division recovery on the visible
faces, and records a genuine bi-deep prefix collision.  That collision is a
guard against falsely extending QR2 to arbitrary partial remainders; it is
not deployed-scale evidence.

## Dependency and chronology contract

Mechanical base:

```text
PR #1039 head ef98012d0b2f6677b62cb006f6c8fcf76db30f2b
predecessor payload 056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7
```

Logical C1 dependency only:

```text
PR #1032 head a843a8f7930054617ef1d94169a4a9d3422cb909
```

The logical dependency is intentionally not merged into this branch.  Its
support-fiber route does not itself supply a codeword projection or a
numerical C1 payment.

## Nonclaims

- no C1 numerical payment;
- no paid 30-column owner;
- no claim that 29-column geometry is impossible;
- no arbitrary boundary-to-Q adapter;
- no quotient-set count on the visible arms;
- no high-interior payment;
- no value for `U_Q`, `U_list_int`, or `U_ext`;
- no ledger movement, row closure, endpoint, stable-paper, or Lean change.

The exact successor terminal is:

```text
M31_C2048_BIDEEP_30COLUMN_OWNER
```
