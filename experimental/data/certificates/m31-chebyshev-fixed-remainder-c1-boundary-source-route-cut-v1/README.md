# M31 Chebyshev fixed-remainder exact C1 boundary-source route-cut certificate

This packet proves that the exact `c=2048` fixed-remainder floor is realized
by an actual deployed received word whose complete target-field ball is one
exact boundary prefix fiber.  It also exhausts the flat-baseline optimizer and
cuts the unqualified flat raw-tail plus aggregate-Forney architecture.  The
certified fixed-remainder subfamily is removed by or at C1
quotient/remainder under the declared order; it is not a primitive Q parent.
This is not a numerical C1 payment, a row-sharp Q upper
bound, or an M31 row closure.

## Exact replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.sage
```

Schema validation, when `jsonschema` is available:

```bash
/Users/scott/math_code/.venv/bin/python -c 'import json,jsonschema; s=json.load(open("experimental/data/schemas/m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.schema.json")); p=json.load(open("experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json")); jsonschema.Draft202012Validator(s).validate(p); print("schema=PASS")'
```

Source and predecessor gates:

```bash
python3 experimental/notes/thresholds/20260709_m31_chebyshev_fixed_remainder_floor/m31_chebyshev_fixed_remainder_floor.py
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --check
python3 experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --tamper-selftest
python3 experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --check
```

Repository checks:

```bash
python3 -m py_compile experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py
python3 -m json.tool experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json >/dev/null
git diff --check
```

## Expected exact summary

```text
exact source: c=2048 floor=6796405; complete ball boundary-only
route: QR2 fixed-R; removed by/at C1; primitive-Q residual=0
chronology: T46>=6796360; raw cap missed by 6536480
optimizer: b=27 compatible by 69137; every b>=28 incompatible
Forney: b27 p2=70282; b28 p2=67680; b29 p2=65262<67447
route cut: no flat baseline survives source and gains two-row control
scope: C1 numerical payment and variable-R residual OPEN; ledger movement=0
```

## What is proved

- A general fixed-remainder polynomial-fold lemma constructs a common
  received word and distinct exact-agreement codewords from one quotient
  prefix bucket.
- On the deployed `T_2048` domain, the structured list has at least
  `6,796,405` members.
- The complete `F_(p^4)` ball around the constructed degree-`a` center is
  boundary-only and base-field-valued.
- The structured floor has the exact complement profile
  `981129 = 479*2048 + 137`; under the declared order QR2 removes this
  fixed-remainder subfamily by or at `C1_QUOTIENT_REMAINDER`, so its post-C1
  primitive-Q residual is zero.
- The source forces `T46 >= 6,796,360`, refuting `T46 <= 259,880` by
  `6,536,480`.
- After optimizing every legal low cutoff, baseline 27 is the largest flat
  raw baseline compatible with the source.  Baseline 28 already fails by
  `297,854`.
- The baseline-27 28-column aggregate joint-index theorem certifies a first
  partial degree `35,141` below `67,447`, but not a two-row degree:
  `70,282 > 67,447`.  Two-row control begins only at baseline 29, which the
  source already refutes.

## Nonclaims

- `6,796,405` is a lower floor, not the exact complete-list size.
- The constructed received word is not proved above budget.
- No `U_Q` upper payment or arbitrary-boundary adapter is supplied.
- No numerical C1 upper payment is supplied, and arbitrary supports in the
  complete global prefix fiber are not classified as C1.
- No value moves for `U_Q`, `U_list-int`, `U_ext`, or high `U_new`.
- No geometrically realized adverse Forney sequence is asserted.
- No dyadic floors are stacked additively.
- The M31 list row, official endpoints, scores, stable papers, and Lean remain
  unchanged.

The surviving terminal for this route is

```text
M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL
```

and the next exact target is a joint numerical C1 codeword payment plus the
variable-remainder/orientation residual.  Under the same declared first-match
convention, fixed-remainder `c=1024` families are also removed by or at C1 and
are not the next primitive-Q target.
