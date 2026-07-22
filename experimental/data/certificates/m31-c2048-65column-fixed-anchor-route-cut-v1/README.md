# M31 c=2048 65-column fixed-anchor certificate

This packet compiles the complete c=2048 exact-boundary atlas at the binding
Mersenne-31 LIST budget.

## Certified results

- If the paid low layer plus the exact boundary exceeds \(B_*=16,777,215\),
  one of all 261,192 occupancy profiles contains at least 65 codewords.
- If the predecessor's combined face/carrier charge exceeds 9,216,781, the
  same profile labeling forces width 36. Its first two joint indices sum to
  at most 53,745 and at least 21 module rows lie below the cutoff.
- A cap of 64 per profile would give
  \(3,730+64\cdot261,192=16,720,018\), leaving exact slack 57,197.
- Every selected 65-frame has joint-kernel rank 63 and index sum at most
  913,681. The sharp cumulative bounds for its first four row-reduced
  indices are 14,502, 29,004, 43,506, and 58,008.
- At least 50 independent module rows have degree at most 65,262, and the
  cutoff syzygy space has field dimension at least 3,335,543.
- After choosing a degree-ordered row-reduced basis, the first two rows admit
  a basis-relative fixed Plücker anchor of degree at most 29,004. It is
  nonzero at at least 38,444 variable roots of each of the other 63 reduced
  locators. This is an existence ladder, not a canonical owner predicate;
  anchors at different ranks need not be nested.
- Exact source enumeration finds 156 profiles with a separately realized
  65-codeword packet: 34 faces and 122 bi-deep profiles. Hence neither a
  universal cap of 64 nor carrier emptiness is available.
- The field-generic proper-hyperplane collision-avoidance proof over the
  deployed target field has width-65 margin
  21,267,647,892,944,572,736,998,860,267,723,701,016. It still applies to
  a prescribed packet of size \(B_*+1=16,777,216\), with margin
  21,267,647,892,944,572,608,409,682,375,602,077,697. Its exact target-field
  endpoint is 6,823,032,369,902,110, not the earlier prime-field 67/68
  cutoff. Low syzygies plus a budget-sized packet therefore do not force a
  collision owner without an identically-zero component or complete-layer
  incidence.
- For an actual exact packet, all escape forms are proper. Hence either some
  collision form vanishes identically on the complete containment space, or
  another functional preserves all prescribed supports and exactness while
  removing every prescribed pair collision.

The successor diagnostic is

    M31_C2048_65COLUMN_FIXED_ANCHOR_OWNER

inside HIGH_BOUNDARY_EXACT_CODEWORD / \(U_{\rm new}\).

## Replay

From the repository root:

    python3 experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --check
    python3 -O experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --check
    python3 experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --tamper-selftest
    python3 -O experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py --tamper-selftest
    HOME=/tmp TMPDIR=/tmp /usr/local/bin/sage experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.sage

The Python verifier recomputes the complete profile/source census with exact
big integers, solves the integer index optimizer, checks all budget and
hyperplane margins, validates a strict canonical manifest, seals sources,
and rejects semantic mutations. Sage independently replays the arithmetic,
the census, the optimizer, and a polynomial-module anchor fixture.

## Dependency state

Mechanical parent:

    PR #1041 head 752872ce98754a05f37540cd7780a89b86818222
    payload dacb9136f5818a5f86d9ca8987fbe4d361a57a70ebb490eac50dfc3822e062e4

At preparation, upstream main remained
32a41660e3088eeeb15a16645330856794302ff0. No newer PR, duplicate, or rebase
need was found.

## Nonclaims

- no exact-boundary numerical payment;
- no claim that the fixed anchor is an existing v4 owner;
- no 65-carrier impossibility or universal profile cap of 64;
- no forced collision or classification of identically-zero components;
- no complete-layer exhaustiveness from the prescribed-packet avoidance
  theorem;
- no attained-prefix, high-interior, extension, or Q bound;
- no ledger movement, row closure, endpoint, score, stable-paper, or Lean
  change.
