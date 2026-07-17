# M1 KoalaBear rank-nine fixed-basis fibre route cut v1

This packet checks a proposed basis-incidence route to the missing rank-nine
deficit tail.

It proves:

1. every fixed eight-row \(K_0\)-basis fibre lies on one affine word line;
2. if that line has union support \(M>j\), then
   `J*(M-j) <= M`;
3. the exact deployed threshold forcing at most 20 slopes is
   `M >= 1030160`;
4. a uniform cap 20 would imply
   `H_18014 <= 17411776716968`, while cap 21 is insufficient;
5. the exact aggregate excess allowance that still pays the desired tail is
   `5284485264881189380664190436821715347228277374`;
6. the uniform cap 20 is false: an exact `GF(2^37)`, `j=20` five-pencil
   rank-nine family has one fixed basis in 21 all-zero-deficit masks.

The counterexample is generic-local and complete only on its explicitly
declared retained family.  It does not instantiate the KoalaBear domain,
exhaust the ambient bad-slope set, disprove the deployed aggregate tail, move
the ledger, or close branch 3.

Replay:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.sage

python3 -B \
  experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py \
  --tamper-selftest
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --tamper-selftest
```

The Python checker uses exact integers and rejects duplicate keys,
non-standard constants, floats, source drift, payload drift, semantic owner
mutations, and type confusion.  Sage independently constructs all 105
declared finite-field witnesses and the 21-fold fixed-basis fibre.
