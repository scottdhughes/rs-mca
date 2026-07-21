# M31 full-span forced-collision route-cut certificate

This packet proves an abstract annihilator criterion and gives an exhaustive
`GF(17)` universal-implication falsifier.  It is not a deployed M31
counterexample, list payment, or row closure.

## Exact replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.sage
python3 -m json.tool experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json >/dev/null
```

Schema validation, when `jsonschema` is available:

```bash
/Users/scott/math_code/.venv/bin/python -c 'import json,jsonschema; s=json.load(open("experimental/data/schemas/m31_full_span_forced_collision_route_cut_v1.schema.json")); p=json.load(open("experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json")); jsonschema.Draft202012Validator(s).validate(p); print("schema=PASS")'
```

Predecessor gates:

```bash
python3 experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --check
python3 experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --check
```

Repository checks:

```bash
python3 -m py_compile experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py
git diff --check
```

## Expected exact summary

```text
abstract: forced iff collision polynomial lies in containment span
GF(17): layer=137, locator span=6=K-1, anchors/key spans=6, common functional dim=1
incidences: common=23813, forced collisions=1326, proper=22487
noncoalescence: every key forced; packing=5; transversal=6
deployed route cut: identity-prefix T46>=1993633; raw T46 cap refuted
scope: universal route cut; M31 row OPEN; ledger movement=0
```

## What the certificate establishes

- The common containment-functional space is the annihilator of the selected
  locator-multiple span.
- A pair collision form vanishes identically on that space exactly when its
  representing polynomial belongs to the containment span.
- The representing polynomial contains the full pairwise common locator.
- At maximum containment rank, the common functional space is one line, so
  “identically forced” is equivalent to the collision already present for the
  original functional.
- The complete `GF(17)` layer realizes this maximum-rank branch: every marked
  46-column key also has maximum locator rank and a forced collision, yet the
  natural anchor-extra forced-root unions have packing optimum five and
  transversal number six.
- Independently, the proved deployed identity-prefix center has an exact
  boundary subfamily of at least `1,993,678` codewords.  Hence its raw excess
  satisfies `T46 >= 1,993,633`, refuting the proposed row-uniform raw cap
  `T46 <= 259,880` by `1,733,753`.
- The complete ball around that degree-`a` center is boundary-only.  Its exact
  deficit is `Delta46 = 16,517,290` and
  `Xi46 = M_R - 16,517,335`, so the signed target specializes exactly to the
  open row-sharp Q bound `M_R <= B*`.
- This lower subfamily is below `B*`; the complete-list budget status of that
  center remains `UNKNOWN`.  The route cut requires a signed chronology with
  every missing-layer and missing-anchor credit retained.

## Nonclaims

- The deployed M31 family is not proved to have maximum containment rank.
- No deployed received word above budget is constructed.
- No bound `Xi46 <= 259880`, boundary-to-`U_Q` adapter, or signed-refund
  compiler is proved.
- No existing v4 owner is assigned to annihilator membership.
- `U_paid` remains `3730`; `U_Q`, `U_list-int`, `U_ext`, and high `U_new`
  remain null.
- The factor-one add-back in open PR #1033 is not imported or banked.
- No endpoint, official score, stable-paper theorem, or Lean declaration
  changes.

The exact global successor terminal is

```text
UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER
```

The local scaled-column subterminal remains
`UNPAID_SPLIT_LOCATOR_HYPERPLANE_OWNER_REFUND`.
