# M31 canonical-masked Padé global route-cut certificate

This directory seals the exact certificate for
`M31_CANONICAL_MASKED_PADE_GLOBAL_ROUTE_CUT_V1`.

The packet has two logically distinct parts: a proved symbolic bridge over
the deployed target field and a contained toy-scale universal-implication
falsifier.

1. A nontrivial-padding `GF(17)` fixture checks the load-bearing canonical
   masked bridge: `B(LQ)=Q B(L)`, `gcd(W,B(W))=Q`, recovery of `L`, the
   codeword and interpolation-numerator transforms, both padding factors in
   every canonical pair minor, and equality of the masked/interpolation
   polynomial right-kernel conditions.
2. A complete exact weight-six layer for one `GF(17)` received word contains
   137 distinct codewords.  Its canonical first 45 anchors produce 92
   rank-46 keys.  Every key has polynomial row rank two and at least three
   degree-zero coupled relations, yet the natural anchor-extra collision-root
   unions have exact disjoint set-packing (intersection-matching) optimum
   five and exact root-transversal minimum six (with all four minimum
   transversals recorded).  This refutes automatic overlap-root coalescence
   witnessed by either a packing cap of four or a four-point root
   transversal; it does not refute arbitrary grouping by unrelated
   polynomials or non-root owners.

The deployed arithmetic also checks the conditional target-field hyperplane
dichotomy.  For `L=2^24`, `R=981129`, and `sigma=913681`, the escape and
pair-collision forms number at most
`128589177894085853184 < 2^67 < 2^68 < p^4`.  If every selected form is proper on
the common containment space, another functional preserves every selected
support and escape while avoiding every selected common-error collision.
Additional exact supports may appear, so this branch is neither a row
counterexample construction nor a payment.

The second part falsifies a parameter-uniform automatic four-root
overlap-coalescence implication from the current local hypotheses.  It is toy-scale:
it is not an M31 received-word counterexample, supplies no v4 payment, and
does not rule out a theorem using the deployed M31 domain, cross-weight
incidence, a chronology-correct owner/refund, primitive elimination, or a
direct distinguished-codeword projection cap.

The manifest records the complete ordered 137-support layer, all 92 key
collision unions, the five-key witness, all minimum root transversals,
exact polynomial records for every nontrivially padded codeword, and live
SHA-256 bindings for all theorem and replay sources.  Its JSON bytes are
canonical and its unsigned payload is sealed by `payload_sha256`.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.sage
```

Additional release-gate replays:

```bash
~/math_code/.venv/bin/python -c 'import json; from jsonschema import Draft202012Validator; s=json.load(open("experimental/data/schemas/m31_canonical_masked_pade_global_route_cut_v1.schema.json")); m=json.load(open("experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json")); Draft202012Validator.check_schema(s); Draft202012Validator(s).validate(m); print("jsonschema=PASS")'
python3 experimental/scripts/verify_m31_full_packet_pade_forney.py --check
python3 experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py --check
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --check
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py --check
python3 experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --tamper-selftest
python3 -m py_compile experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py
git diff --check
```

The primary `--check` regenerates and compares every live SHA-256 source
binding.  The older rank-46 pinned `--check` is intentionally not listed:
its manifest predates the Grande Finale v4 promotion and has one stale
`experimental/grande_finale.tex` hash.  Its regenerated live arithmetic and
34/34 hostile mutations pass through `--tamper-selftest`; this packet does
not silently reseal that unrelated predecessor.

The primary verifier is standard-library only and uses explicit exceptions,
so optimized execution retains every check.  It never writes the manifest;
`--print-template` emits canonical candidate bytes for review and sealing.

Expected terminal:

```text
UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND
```

Ledger movement is zero and the deployed M31 list row remains open.
