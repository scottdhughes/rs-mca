# M31 `c=2048` fixed-template module-rank route-cut certificate

This certificate seals a local dichotomy for every deployed occupancy
profile and every fixed exact partial agreement template.  If the
fixed-template exact-boundary family exceeds its printed conditional threshold
`Lambda_SD(u,v)`, a Chen--Zhang minimal bad subfamily has a difference span whose
free-`F[phi]` coefficient matrix loses rank over `F(T)`.

The exact thresholds have maximum 17 and sum to 1,988,814 over all 261,192
profiles.  Separately realized fixed-multipartial-template rank-one sources
exceed them in 193 profiles, including floors 6,796,405 at `(0,0)` and
1,693,898 at `(1,1)`; these floors are not simultaneous around one received
word.  The sum is conditional arithmetic, not a ledger charge.  The
packet neither classifies module-rank-drop components nor aggregates across
different partial templates.  It moves no atom and does not close the row.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.py --tamper-selftest
HOME=/tmp TMPDIR=/tmp /usr/local/bin/sage experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.sage
/Users/scott/math_code/.venv/bin/python -m jsonschema \
  -i experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json \
  experimental/data/schemas/m31_c2048_fixed_template_module_rank_route_cut_v1.schema.json
```

Regenerate the canonical schema and manifest only after intentional source
changes:

```bash
python3 experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.py --write
```

## Bound dependencies

The manifest hashes this note, both verifiers, the schema, this README, the
exact predecessor #1043 manifest, the full occupancy atlas, the quotient
remainder source, the v4 source adapter and active ledger, and the repository
Chen--Zhang citation.

The imported external statement is the combinatorial strong-subspace-design
argument in Chen--Zhang, arXiv:2408.15925 v3, Appendix B.  No folded
Wronskian, generator orbit, or direct FRS-to-Chebyshev transfer is used.
The audited 31-page primary PDF SHA-256 is
`1d4a4859229351d1c345653e5d7eb63682f855c0b080b947d40fe1ecaf88c56a`.

## Fail-closed nonclaims

- `ledger_movement = 0`;
- the threshold sum is not a global profile or boundary payment;
- module-rank drop is not automatically quotient descent or periodicity;
- varying exact partial templates are not coalesced;
- high interior, extension, and all other v4 residuals remain open.
