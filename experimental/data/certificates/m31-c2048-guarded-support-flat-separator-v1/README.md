# M31 `c=2048` guarded support-flat separator v1

This packet is an exact theorem-interface and converse certificate stacked on
PR #1044.  It does **not** prove the separator `VT(U)`, move a ledger atom, or
close the M31 LIST row.

Exact dependency:

```text
PR:      #1044
head:    5b097b607ae60f7d46c730654eb04fa8a63c8595
payload: c164f24810e0ed5015b3e538607e8867c7f634d5797de645c455447a08aaa303
```

The positional fixed-template caps are bound directly to PR #1043 at
`0d93d366072a0ad3f66c73f9b5a6329a232b4293`, payload
`99febb07f517aac958e55eeba466e268a4ada793ef7960a189374603ea4a3ec9`.

## Certified interface

- A boundary support `E` is exact for a syndrome `phi` precisely when `phi`
  annihilates `W_E` and no one-point extension `W_(E minus x)`.
- The complete profile/template/cofactor-jet sum is duplicate-freely
  reindexed by those punctured support-flat incidences.  A partial template
  here is positional; it does not include received values.
- `VT(U)` is sufficient for a boundary cap `U`.
- If `VT(U)` fails and `p^4>(U+1)R`, hyperplane-union avoidance constructs an
  actual target-field received word with all `U+1` supports exact.
- Shifted locators give the exact rank/escape compiler.  Fifteen supports are
  automatically containment-compatible; escape absorption remains the
  possible obstruction.  Sixteen are the first full-rank gate.

The exact small-field control uses `GF(67^2)`, `n=62`, `K=31`, `R=29`, and
`w=2`.  Sixteen pinned supports have shifted rank 30, a common explicit
annihilator, and 464/464 proper one-point escapes.  A one-point mutation of
the sixteenth support raises the shifted rank to 31.  This fixture tests the
interface; it is not evidence that deployed `VT(U)` holds.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.py --check
python3 -O experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.py --check
python3 experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.py --tamper-selftest
HOME=/tmp TMPDIR=/tmp /usr/local/bin/sage experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.sage
```

Artifact regeneration is deterministic:

```bash
python3 experimental/scripts/verify_m31_c2048_guarded_support_flat_separator_v1.py --write
```

If `jsonschema` is available, validate the generated manifest independently:

```bash
/Users/scott/math_code/.venv/bin/python -m jsonschema \
  -i experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/manifest.json \
  experimental/data/schemas/m31_c2048_guarded_support_flat_separator_v1.schema.json
```

## Scope guard

The active global terminal remains
`UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER`.  Its boundary subterminal
remains `UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`.  The new boundary
diagnostic `UNPROVEN_GUARDED_SUPPORT_FLAT_SEPARATOR_VT` is not a first-match owner.
`U_paid`, `U_Q`, `U_list-int`, `U_ext`, and `U_new` are unchanged.
