# M1 KoalaBear rank-nine projective source-load v1

This certificate freezes one exact post-tangent reduction:

~~~text
E_20^nz = sum_L w_L = sum_(h in Sigma) Lambda_h,
Lambda_h = sum_(L: h in S_L) w_L / |S_L|.
~~~

It also freezes the positive source-plant floor, the finite/infinity
projective source partition, the coefficient-rank-one/rank-two dichotomy, and
the reduced rank-two root cap obtained after removing forced common roots
outside the sparse source.

Support-wise nontriviality is tied to the selected witness support. The packet
therefore does not infer `x_L>=1` from simultaneous explanation on a different
common-zero subset; it uses only the rich-line upper bound `x_L<=49055`.

The certificate does not contain a deployed post-tangent selector or a paying
weighted incidence theorem. Its live deployed terminal is therefore
`UNBOUND_POST_TANGENT_SOURCE_LOAD`. The stronger terminal
`UNPAID_PRIMITIVE_PROJECTIVE_SOURCE_FIBER` is reserved for a future actual,
source-bound compatible component with no existing owner.

## Replay

Run from the repository root:

~~~bash
python3 -B experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --check
python3 -B -O experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --tamper-selftest
python3 -B -O experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --tamper-selftest
sage experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.sage
~~~

Certificate freshness is checked by comparing the committed JSON with the
verifier's canonical output:

~~~bash
python3 -B experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --print-certificate > /tmp/m1_kb_rank9_projective_source_load_v1.json
diff -u experimental/data/certificates/m1-kb-rank9-projective-source-load-v1/m1_kb_rank9_projective_source_load_v1.json /tmp/m1_kb_rank9_projective_source_load_v1.json
~~~

The committed JSON is generated only through the verifier's `--write` mode.

Load-bearing predecessor replays are:

~~~bash
python3 -B experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py --check
~~~

## Exact controls

The Python and Sage replays independently reconstruct four deterministic
GF(11) controls. Two rank-one controls show that positive rich-line weight
survives both an absent tangent-image finite zero slope and an infinity pencil.
Two rank-two controls remove the forced outside-source factor `X-2` and reach
the injective reduced cap `d_proj=1`; one has only finite plant fibers and the
other has one finite and one infinity plant fiber. All rational loads are
computed exactly.

These are generic-local implication controls, not affine-rank-nine selectors,
not a deployed-field census, and not evidence that a deployed primitive
component exists.

## Scope

This packet moves no ledger quantity. It does not prove the pointwise source
load target, pay rank nine, determine `U_Q` or `U_A`, close the KoalaBear row,
authorize rank at least ten, or promote a result to Lean or the stable paper.
