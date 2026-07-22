# M31 `c=2048` multiprefix / carrier-activation certificate

This packet proves two exact deployed route cuts following PR #1040.

## Certified results

For every feasible `c=2048` occupancy profile `(u,v)`, fixing all partial
agreement points and varying the `544-v` full agreement fibers gives one
actual base-field received word with at least

```text
L(u,v) = ceil(C(1023-u-v,544-v) / p^min(32,544-v))
```

exact-boundary codewords in that profile.  The complete deployed target-field
ball around the constructed base-field center is boundary-only, and every
codeword in it is base-field-valued.

Exact census:

```text
177 profiles have L(u,v) >= 30
  36 C1-shaped faces
  141 bi-deep profiles

largest bi-deep certified floor: (u,v)=(1,1), L=1,693,898

the exact sufficient-criterion histogram is 124 source profiles at width 29
and 18 at width 30; (8,10), with L=29, is the one profile added beyond the
141 certified floors at least 30
```

The fixed partial-error template sharpens the selected determinantal divisor.
The 18 activated profiles with `u=1` yield a genuine 30-column two-row bound
`65,106 < 67,447` (their 29-column upper remains `67,518 > 67,447`);
124 activated bi-deep profiles have `u>=2` and
already yield a 29-column bound at most `67,366 < 67,447`.  These are actual
source carriers, not hypothetical fixed-width frames.  They remain unpaid.

These are lower-floor certificates for separately constructed received words,
not a classification of all carriers and not one simultaneous list.

The packet also constructs one deployed base-field received word with two
exact `(u,v)=(0,0)` codewords having the same fixed agreement remainder and
the same fixed error remainder, but distinct locator prefixes in both
orientations.  Therefore no common codeword translation or operation leaving
those supports literally fixed can identify the pair's actual monic locators
with one locator-prefix target.  This does not rule out a coarser target or a
non-support-preserving adapter.

The exact arbitrary-word replacement is

```text
Y - P = L_S H,
deg P < K,
deg H <= R-1,
H(x) != 0 on D\S.
```

Translation by a codeword leaves `(L_S,H)` invariant.  The corrected raw face
target is a fixed-syndrome sum over attained prefixes.  A maximum-prefix-fiber
bound alone is insufficient without a target-count or coalescing theorem, and
banking still requires a disjoint first-match owner.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_c2048_multiprefix_30carrier_activation_v1.py --check
python3 -O experimental/scripts/verify_m31_c2048_multiprefix_30carrier_activation_v1.py --check
python3 experimental/scripts/verify_m31_c2048_multiprefix_30carrier_activation_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_c2048_multiprefix_30carrier_activation_v1.py --tamper-selftest
HOME=/tmp TMPDIR=/tmp sage experimental/scripts/verify_m31_c2048_multiprefix_30carrier_activation_v1.sage
```

The Python verifier exhausts all `261,192` profiles with exact big integers,
regenerates the canonical manifest, checks every source hash and predecessor
seal, replays two `GF(17)` controls, and rejects semantic mutations.  The Sage
script independently redoes the deployed census and constructs the two
finite-field fixtures polynomial by polynomial.

## Dependency state

Mechanical parent:

```text
PR #1040 head 02b1b8195a9f219a110ce255b205a3e8aed26956
payload c312bd2c108634af51cd351a004cdb2942bc10a145eca3e49dbcfe8fe8873a7c
```

Logical C1 cross-check only:

```text
PR #1032 head a843a8f7930054617ef1d94169a4a9d3422cb909
```

At preparation, upstream `main` remained
`32a41660e3088eeeb15a16645330856794302ff0`; no rebase or duplicate PR was
needed.

## Nonclaims

- no C1 numerical upper payment;
- no carrier owner or attained-image upper bound;
- no claim that every same-profile frame shares one partial template;
- no simultaneous attainment of different profile floors;
- no bound for the sum over attained prefixes;
- no high-interior, extension, or Q payment;
- no universal arbitrary-word carrier theorem, global numerator floor, or
  counterexample to the M31 row;
- no replacement of the active v4 partition or global terminals;
- no ledger movement, row closure, endpoint, score, stable-paper, or Lean
  change.

The packet-local diagnostic subterminal inside
`HIGH_BOUNDARY_EXACT_CODEWORD` / `U_new` is

```text
M31_C2048_FIXED_SYNDROME_MULTIPREFIX_FACE_CARRIER_OWNER
```
