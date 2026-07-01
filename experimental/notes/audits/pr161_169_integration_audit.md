# PR 161--169 Integration Audit

Date: 2026-07-01

Status: AUDIT / INTEGRATION.

This note records the selective integration of the current open PR batch.  The
goal was to keep pieces that advance the Hankel/L1/M1/F1 proof program while
avoiding wholesale promotion of generated, conditional, or leaderboard-looking
material.

## Integrated

### PR #168: L1 arbitrary-local conjecture repair

Author: holmbuar.

Status: AUDIT / TEXT REPAIR.

The important mathematical correction is that the raw support fiber
`Fib_U(s)` is not the right positive L1 target: one low-degree codeword may be
explained by exponentially many supports.  Papers B and C now use the
codeword-image fiber

```text
ImgFib_U(s) = { U mod L_S : S in Fib_U(s) }.
```

The exact list size is `|ImgFib_U(s)|`, while `|Fib_U(s)|` remains only a coarse
upper bound.  This repair was applied directly to the current Paper B/C TeX
copies because it fixes a false formulation, not merely an experimental note.

Integrated verifier:

```text
experimental/scripts/verify_l1_arbitrary_local_conjecture_patch.py
```

### PR #169: full-petal growing-defect witnesses

Author: holmbuar.

Status: EXPERIMENTAL / COUNTEREXAMPLE-STYLE / ROUTE-CUT.

Integrated files:

```text
experimental/notes/l1/l1_full_petal_growing_defect_witnesses.md
experimental/scripts/verify_l1_full_petal_growing_defect_witnesses.py
```

The note gives explicit full-petal sunflower witnesses at positive
`d-ell`.  It does not prove growth, and it does not refute the repaired
image-fiber L1 target.  It does block the shortcut that the full-petal
growing-defect branch is empty.

### PR #165: monomial dyadic descent replay packet

Author: AllenGrahamHart.

Status: PROVED / AUDIT for the stated monomial packet.

Integrated files:

```text
experimental/data/certificates/l1-monomial-dyadic-descent/
experimental/scripts/verify_l1_monomial_dyadic_descent_packet.py
experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md
```

The existing monomial-dyadic note now points to the replay packet and verifier.
This is an L1 monomial-prefix gate, not an arbitrary-word local-limit theorem.

### PR #166: full-overlap low-tail completion

Author: DannyExperiments / Gia.

Status: PROVED / ROUTE-CUT / AUDIT.

Integrated file:

```text
experimental/notes/m1/m1_full_overlap_low_tail_completion_projection_wall.md
```

The note proves the full-overlap low-tail completion identity and separates it
from the remaining projection-to-Graver wall.  It is useful for M1 route
planning, but it does not move the leaderboard and is not a proof of the full
Paper B conjecture.

### PR #167 and PR #162: BETA_2 localization

Author: holmbuar.

Status: AUDIT / CONDITIONAL proof program.

Integrated files:

```text
experimental/notes/m1/m1_beta2_conditional_close.md
experimental/notes/m1/m1_beta2_obstruction_floor.md
experimental/scripts/verify_m1_beta2_conditional_close.py
experimental/scripts/verify_m1_beta2_local_data_dossier.py
experimental/scripts/verify_m1_beta2_p73_resolution.py
experimental/lean/rs_mca_formalization/RsMca/BetaTwoReductionLedger.lean
```

The later conditional-close note supersedes the older obstruction-floor note
for the main route: the finite local data is not enough by itself; the remaining
input is a global big-monodromy or conductor-style theorem.  This is a
localization of the wall, not a closure of M1.

### PR #163 and PR #164: Lean ledger wiring

Author: holmbuar.

Status: FORMALIZATION / AUDIT.

Integrated files:

```text
experimental/lean/rs_mca_formalization/RsMca/F1ExtensionLedger.lean
experimental/lean/rs_mca_formalization/RsMca.lean
```

The Lean root file now imports the quotient-floor bridge, F1 extension ledger,
and BETA_2 reduction ledger.  These files formalize algebraic cores and typed
targets; they do not by themselves prove the full MCA semantics.

### PR #161: selected regular-Hankel artifacts

Author: AllenGrahamHart.

Status: AUDIT / PROOF-PACKET INFRASTRUCTURE.

PR #161 is large and includes many generated packets.  It was not merged
wholesale.  The integrated subset is the reusable M3 material:

```text
experimental/notes/m1/hankel_regular_minor_extractor.md
experimental/notes/m1/hankel_regular_window_plan.md
experimental/notes/m1/f17_32_hankel_row_descriptor.md
experimental/notes/m1/f17_32_m3_generic_regular_minor.md
experimental/notes/m1/f17_32_m3_rank_witness_packet.md
experimental/notes/thresholds/f17_32_high_agreement_tangent_table.md
experimental/scripts/extract_regular_hankel_minors.py
experimental/scripts/plan_f17_regular_hankel_window.py
experimental/scripts/emit_f17_32_hankel_row_descriptor.py
experimental/scripts/verify_f17_32_m3_generic_regular_minor.py
experimental/scripts/verify_f17_32_high_agreement_tangent_table.py
experimental/scripts/emit_f17_32_m3_rank_witness_input.py
experimental/data/certificates/hankel-regular-window-f17-385-426/
experimental/data/certificates/hankel-f17-32-row-descriptor/
experimental/data/certificates/hankel-f17-32-generic-regular-minor/
experimental/data/certificates/hankel-f17-32-high-agreement-tangent-table/
```

The useful content is:

```text
regular window for F_17^32 row: 385 <= A <= 426;
tangent exact range starts at A=427;
finite-slope budget is floor(17^32/2^128)=6;
degree-only regular sum over the window is 4515, so root tables or singular
bucket classification are required;
generic maximal row-set regular minors are nonzero of exact degree j+1.
```

This sharpens the M3 work plan but does not supply a safe-side threshold proof
for the non-tangent window.

## Not promoted

No new public leaderboard row is promoted by this batch.  The high-agreement
tangent table supports the already-known tangent staircase.  The M1/L1/F1
pieces are proof-program and audit material, not new prize-level claims.

Generated low-rank and broad regular-window packets from PR #161 remain out of
tree for now.  They should return as compressed proof packets with a small
auditor note before integration.

## Local verification

The selected Python scripts were syntax-checked with `python3 -m py_compile`.
The following deterministic checks were run locally:

```text
verify_l1_arbitrary_local_conjecture_patch.py
verify_l1_full_petal_growing_defect_witnesses.py --json
verify_l1_monomial_dyadic_descent_packet.py --check ...
verify_m1_beta2_p73_resolution.py --check
verify_m1_beta2_conditional_close.py --check
verify_m1_beta2_local_data_dossier.py --check
plan_f17_regular_hankel_window.py --check ...
emit_f17_32_hankel_row_descriptor.py --check ...
verify_f17_32_m3_generic_regular_minor.py --check ...
verify_f17_32_high_agreement_tangent_table.py --check ...
```

All listed checks passed.  The PR #161 row-descriptor script originally
expected an `is_irreducible_mod_prime` helper exported by the schema checker;
the integrated version now includes a self-contained Rabin-style irreducibility
test for the pinned `F_17^32` modulus.

The touched TeX files

```text
tex/slackMCA_v3.tex
tex/slackMCA_v4.tex
tex/snarks_v4.tex
tex/snarks_v5.tex
```

were compile-checked with `tectonic --outdir /tmp/rs-mca-texcheck`.  They
compiled successfully with only underfull-box warnings.

The Lean files were not built in this integration pass.  They are included as
individually buildable formalization material for contributors who maintain a
local Lean/lake environment.
