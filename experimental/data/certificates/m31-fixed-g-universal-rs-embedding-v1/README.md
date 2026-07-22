# M31 fixed-G universal base-field RS embedding packet

This packet certifies an exact counterexample adapter for the pinned
Mersenne-31 LIST row.  For every `R`-point boundary subset `E0` of the
deployed evaluation domain, every dimension `1 <= d <= R-w`, every
base-field received table, and every ordinary Reed--Solomon list satisfying
agreement `m=d+w`, one common constant translation removes all received-word
zeros and leaves enough points of the complementary anchor set for one split
locator `G` that is coprime to every translated message.

At the deployed ordinary-list size `B_star=16,777,215`, the exact averaging
calculation is

```text
p-R                                      = 2,146,502,518
floor(B_star*a/(p-R))                    = 8,722
a-8,722                                  = 1,107,301
1,107,301-R                              = 126,172
```

The translated ordinary codewords embed as `B_star` distinct nonanchors
sharing the same `G`; the zero anchor supplies the `B_star+1`-st codeword.
Consequently, safety of the deployed M31 row would force the uniform
punctured ordinary-RS upper `B_star-1=16,777,214`.  Conversely, an ordinary
list of size `B_star` on one such shortening is an actual counterexample to
the row.

The exact instance gate is

```text
a - floor(L*a/(p-|r(E0)|)) >= m.
```

The conservative deployed-uniform gate replaces the actual image size by
its worst-case bound:

```text
a - floor(L*a/(p-R)) >= m.
```

It holds simultaneously for every legal `w+1 <= m <= R` for all
`L <= 259,450,259`; the bad-point floors at this endpoint and its successor
are respectively `134,894` and `134,895`.

This is a fixed-`G` subclass equivalence, not a row upper bound.  It applies
to `R`-subsets of the pinned deployed domain; it does not promote a theorem
for generic or arbitrary evaluation sets to that domain.  It proves no
ordinary-RS upper, no exhaustive multi-`G` bound, no Grande Finale v4 owner
payment, and no official endpoint movement.  The live terminal is
`UNPAID_UNIFORM_DETERMINISTIC_PUNCTURED_RS_LIST_BOUND`.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.py
python3 -O experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.py
python3 experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.py --tamper-selftest
sage experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.sage
python3 experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_packet_v1.py
python3 -O experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_packet_v1.py
python3 experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_packet_v1.py --tamper-selftest
```

The packet verifier independently replays the primary verifier in normal
and optimized modes, runs its hostile mutations, runs the Sage finite-field
control, replays the sealed parent packet, checks the closed schema and
canonical manifest, refreshes every source hash, checks the internal parent
payload pin, verifies theorem-note and scope anchors, and runs its own
proof-critical hostile mutations.
