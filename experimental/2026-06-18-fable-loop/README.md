# 2026-06-18 Fable Loop

Status: EXPERIMENTAL / AUDIT.

This folder records Codex-managed Opus 4.8 co-director cycles after the manual integration of PR #62 into upstream `main`.

Source policy:

- Main papers are not edited here.
- Raw model outputs are provenance, not promoted claims.
- Audits decide what, if anything, should be treated as `BANKABLE_LEMMA`, `COUNTERPACKET`, `ROUTE_CUT`, or `EXACT_NEW_WALL`.

Cycle 1 target:

- F1 arbitrary-anchor balanced denominator gap in `tex/slackMCA_v3.tex:def:residue`, with balanced `t=sigma`.

Cycle 1 audit:

- `audits/20260618_CYCLE1_F1_ARBITRARY_ANCHOR_AUDIT.md`

Cycle 2 target:

- Adversarial audit of the paired base interpolation-residue readout from Cycle 1.

Cycle 2 first attempt:

- `audits/20260618_CYCLE2_PAIRED_BASE_READOUT_HUNG_RUN.md`
- Status: `HARNESS_FAILED` / `AUDIT`; no mathematics banked.

Cycle 2 retry prompt:

- `prompts/20260618_cycle2_retry_paired_base_readout_short.md`

Bounded local audit:

- `audits/20260618_CODEX_LOCAL_PAIRED_BASE_READOUT_AUDIT.md`

Cycle 2 retry audit:

- `audits/20260618_CYCLE2_PAIRED_BASE_READOUT_RETRY_AUDIT.md`
- Status: `BANKABLE_LEMMA` / `EXACT_NEW_WALL`.

Cycle 3 local audit:

- `audits/20260618_CODEX_LOCAL_NONCONTAINMENT_SUBSET_LEMMA.md`
- Status: `BANKABLE_LEMMA` / `AUDIT`.

Cycle 3 Fable audit:

- `audits/20260618_CYCLE3_W_F1_AA_NONCONTAINMENT_AUDIT.md`
- Status: `BANKABLE_LEMMA` / `EXACT_NEW_WALL`.

Cycle 4 balance-notation audit:

- `audits/20260618_CYCLE4_BALANCE_NOTATION_ROUTE_CUT_AUDIT.md`
- Status: `ROUTE_CUT` for `W-F1-AA-AGR` as a balanced wall; the noncontainment lemma remains banked.

Cycle 5 restored W-F1-AA audit:

- `raw/20260618_CYCLE5_W_F1_AA_RES_RAW.md`
- `audits/20260618_CYCLE5_W_F1_AA_RES_EXACT_WALL_AUDIT.md`
- Status: `EXACT_NEW_WALL` / `AUDIT`.
- Banked conservative content: restored `W-F1-AA` is sharpened to `W-F1-AA-RES`, the reserve-indexed paired-readout rigidity/value-count wall. This is not a proof of F1, not a protocol statement, and not a new corrected-reserve counterpacket.

Cycle 6 VS Code credited-terminal attempt:

- `raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RAW_MALFORMED.json`
- `raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RESPONSE_MALFORMED_VISIBLE_TERMINAL.md`
- `raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RUN_RESULT.json`
- `audits/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_HARNESS_MALFORMED.md`
- Status: `HARNESS_MALFORMED_VISIBLE_TERMINAL` / `AUDIT`.
- No mathematics banked. The apparent rigidity lemma candidate is a retry target only because the VS Code visible-terminal artifact has missing letters/spaces and duplicated fragments; no clean `response.md` was produced.

Cycle 6B clean-retry attempt:

- `raw/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RAW_MALFORMED.json`
- `raw/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RESPONSE_MALFORMED_VISIBLE_TERMINAL.md`
- `raw/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RUN_RESULT.json`
- `raw/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RECOVERED_CLAUDE_JSONL.md`
- `audits/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RECOVERED_AUDIT.md`
- Harness status: `HARNESS_MALFORMED_VISIBLE_TERMINAL`.
- Mathematical audit status: `EXACT_NEW_WALL` / `AUDIT`, based on source-checking
  the recovered structured Claude JSONL answer. Banked route clarification:
  the same-slope kernel `E*F_{<k}[X]` is not the wall; the live wall is
  `W-F1-AA-RES-VALUECOUNT`, a value-count / collision law for distinct slopes
  in the paired-readout image on `F*[Bnum]_E`.

Cycle 7 value-count attempt:

- `prompts/20260618_cycle7_w_f1_aa_res_valuecount.md`
- `raw/20260618_CYCLE7_W_F1_AA_RES_VALUECOUNT_RECOVERED_CLAUDE_JSONL.md`
- `local_checks/20260618_cycle7_theta_multiplier_check.py`
- `audits/20260618_CYCLE7_W_F1_AA_RES_VALUECOUNT_TWISTED_READOUT_AUDIT.md`
- Harness note: the VS Code terminal `response.md` was visibly damaged despite
  `run_result.json` reporting `BANKABLE_LEMMA`; the clean receipt was recovered
  from Claude structured JSONL.
- Mathematical audit status: `ROUTE_CUT / EXACT_NEW_WALL`.
- Do not bank the claimed exact transfer to a base datum
  `(Ehat,b_hat,w0+theta*w1)`. The nonconstant CRT multiplier `theta` does not
  commute with support interpolation in general.
- Live wall: `W-F1-AA-RES-TWISTED-READOUT`, a value-count/collision theorem or
  counterpacket for `[interp_S(w0)]_Ehat + theta [interp_S(w1)]_Ehat`.

Cycle 8 twisted-readout attempt:

- `prompts/20260618_cycle8_w_f1_aa_res_twisted_readout.md`
- `raw/20260618_CYCLE8_W_F1_AA_RES_TWISTED_READOUT_RECOVERED_CLAUDE_JSONL.md`
- `local_checks/20260618_cycle8_twisted_readout_verify.py`
- `audits/20260618_CYCLE8_W_F1_AA_RES_TWISTED_READOUT_AUDIT.md`
- Harness status: clean structured Claude JSONL used for `response.md`.
- Mathematical audit status: `BANKABLE_LEMMA / EXACT_NEW_WALL`.
- Banked content: `B[X]/Ehat ~= F[X]/E`, so the twisted readout is exactly
  `pi^{-1}([interp_S(w)]_E)`; the commutator with pointwise
  `theta*w1` is locator-divisible.
- Live wall: `W-F1-AA-RES-RESIDUE-COUNT`, a direct value-count/collision theorem
  or counterpacket for `[interp_S(w0)+alpha interp_S(w1)]_E`.

Cycle 9 line-incidence correction:

- `prompts/20260618_cycle9_w_f1_aa_res_residue_count.md`
- `raw/20260618_CYCLE9_W_F1_AA_RES_RESIDUE_COUNT_RECOVERED_CLAUDE_JSONL.md`
- `local_checks/20260618_cycle9_locator_quotient_incidence_check.py`
- `audits/20260618_CYCLE9_W_F1_AA_RES_RESIDUE_COUNT_LINE_INCIDENCE_AUDIT.md`
- Mathematical audit status: `BANKABLE_LEMMA / EXACT_NEW_WALL`.
- Banked content: the source MCA object is not raw residue cardinality. It is
  the bad-line slope/incidence count
  `#{z in F : exists S, [interp_S(w)]_E=z[Bnum]_E}`. The locator-quotient
  identity is `W=L_S Q_S+interp_S(w)`, `deg Q_S<=n-a-1`.
- Live wall: `W-F1-AA-RES-LINE-INCIDENCE`.

Cycle 10 manual route-cut reinforcement:

- `raw/20260618_CYCLE10_MANUAL_W_F1_AA_RES_RESIDUE_COUNT_RESPONSE.md`
- `audits/20260618_CYCLE10_MANUAL_RESIDUE_COUNT_ROUTE_CUT_AUDIT.md`
- Mathematical audit status: `ROUTE_CUT / EXACT_NEW_WALL / AUDIT`.
- Banked content: `ONLINE-SLOPE-COUNT` and `LINE-INCIDENCE` are the same
  source-corrected wall. Do not split them into separate targets.

Cycle 11 t=2, j=2 line-incidence audit:

- `prompts/20260618_cycle11_w_f1_aa_res_line_incidence.md`
- `raw/20260618_CYCLE11_W_F1_AA_RES_LINE_INCIDENCE_RESPONSE.md`
- `raw/20260618_CYCLE11_W_F1_AA_RES_LINE_INCIDENCE_RECOVERED_CLAUDE_JSONL.md`
- `raw/20260618_CYCLE11_W_F1_AA_RES_LINE_INCIDENCE_RUN_RESULT.json`
- `local_checks/20260618_cycle11_t2_j2_line_incidence_verify.py`
- `audits/20260618_CYCLE11_T2_J2_LINE_INCIDENCE_AUDIT.md`
- Harness note: VS Code terminal response was malformed, but clean theorem text
  was recovered from Claude structured JSONL and written to `response.md`.
- Mathematical audit status: `BANKABLE_LEMMA / AUDIT`.
- Banked content: in the restricted regime `t=sigma=2`, `j=n-a=r-t=2`,
  `Q_S=C(X-s_T)+C1`, bad-line landing is one conic `det(s_T,p_T)=0`,
  `[p^2]det=wedge([W]_E,[Bnum]_E)`, and the nonresonant slope count is
  `O(n)` (`C2<=6n`, generically `C2<=4`).
- Not banked: `conj:B`, `j>=3`, `t>=3`, `q_gen` collapse, protocol/MCA/CA/
  list-decoding consequences.
- Next wall: `W-F1-AA-RES-T2J3`; secondary wall `W-F1-AA-RES-T3J2`.

Cycle 12 t=2, j=3 quotient/quadric audit:

- `prompts/20260618_cycle12_w_f1_aa_res_t2j3.md`
- `raw/20260618_CYCLE12_W_F1_AA_RES_T2J3_RESPONSE.md`
- `audits/20260618_CYCLE12_T2_J3_LINE_INCIDENCE_AUDIT.md`
- `local_checks/20260618_cycle12_t2_j3_line_incidence_scan.py`
- Mathematical audit status: `BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT`.
- Banked content: `Q_S` depends on `tau_1,tau_2` and not `tau_3`; bad-line
  landing is a quadric with `[tau_3^2]Delta=wedge([W]_E,[Bnum]_E)`.
- Not banked: a `C2` slope bound. The live wall becomes slope-fiber collapse.

Cycle 13 base-component complete-intersection audit:

- `prompts/20260618_cycle13_base_component_complete_intersection.md`
- `raw/20260618_CYCLE13_BASE_COMPONENT_COMPLETE_INTERSECTION_RESPONSE.md`
- `audits/20260618_CYCLE13_BASE_COMPONENT_COMPLETE_INTERSECTION_AUDIT.md`
- `local_checks/20260618_cycle12_base_component_rank_scan.py`
- Mathematical audit status: `BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT`.
- Banked content: off `R0 union Ra union Rb`, the base components
  `Delta_0,Delta_1` are coprime, so `#landings=O(p)` and hence `C2=O(n)` for
  `D=F_p`, `t=sigma=2`, `j=3`.
- Live wall: resonance strata `Ra/Rb`.

Cycle 14 resonance slope-map audit:

- `prompts/20260618_cycle14_base_component_resonance.md`
- `raw/20260618_CYCLE14_BASE_COMPONENT_RESONANCE_RESPONSE.md`
- `audits/20260618_CYCLE14_BASE_COMPONENT_RESONANCE_AUDIT.md`
- Mathematical audit status: `EXACT_NEW_WALL / AUDIT`.
- Banked content: the resonance strata are not source-excluded by the current
  hypotheses. The residual problem is the explicit slope map on a base surface:
  `q1 z^2-(p1-q2)z-p2=0`, `tau_3=p1-zq1 in B`.
- Live wall: `W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER`.

Cycle 15 surface slope-fiber rank/determinant audit:

- `prompts/20260618_cycle15_surface_slope_fiber.md`
- `raw/20260618_CYCLE15_SURFACE_SLOPE_FIBER_RESPONSE.md`
- `raw/20260618_CYCLE15_SURFACE_SLOPE_FIBER_RECOVERED_CLAUDE_JSONL.md`
- `raw/20260618_CYCLE15_SURFACE_SLOPE_FIBER_RUN_RESULT.json`
- `audits/20260618_CYCLE15_SURFACE_SLOPE_FIBER_AUDIT.md`
- `local_checks/20260618_cycle15_forced_ra_slope_scan.py`
- `local_checks/20260618_cycle15_forced_ra_slope_scan_certificate.md`
- Harness status: clean structured Claude JSONL was promoted to `response.md`;
  terminal transcript is revenue/debug evidence only.
- Mathematical audit status: `EXACT_NEW_WALL / AUDIT`.
- Banked content: the residual surface slope problem reduces to the affine
  equation `L_z(tau)=iota-z mu=0` in `A=F[X]/E`, with explicit `B`-columns
  `c1(z),c2(z),c3(z)` and determinant consistency polynomial
  `Q(z_0,z_1)`.
- Audit correction: rank `3` alone does not imply `Theta(q_line)` slopes.
  The safe wall is the rank/determinant pair: `Q!=0` gives a curve-sized
  slope set, while `Q==0` identically is the possible large-slope regime.
- Live wall:
  `W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DETERMINANT`.

Cycle 16 rank/determinant resonance audit:

- `prompts/20260618_cycle16_rank_determinant_resonance.md`
- `raw/20260618_CYCLE16_RANK_DETERMINANT_RESONANCE_RECOVERED_CLAUDE_JSONL.md`
- `raw/20260618_CYCLE16_RANK_DETERMINANT_RESONANCE_RAW.json`
- `raw/20260618_CYCLE16_RANK_DETERMINANT_RESONANCE_RUN_RESULT.json`
- `raw/20260618_CYCLE16_RANK_DETERMINANT_RESONANCE_RESPONSE_MALFORMED_VISIBLE_TERMINAL.md`
- `audits/20260618_CYCLE16_RANK_DETERMINANT_RESONANCE_AUDIT.md`
- Harness status: `HARNESS_MALFORMED_VISIBLE_TERMINAL`; terminal scrape is
  rejected. Clean structured Claude JSONL recovery is the audited math
  artifact.
- Source-mount audit: Packy source mirror was stale and did not include Cycle
  15 audit/certificate files; ledgers were sufficient for this run, but the
  source mirror must be repaired before Cycle 17.
- Mathematical audit status: `BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT`.
- Banked content: off `R0`, if `Q(z_0,z_1)` is not identically zero, then
  `C2<=4p=O(p)=O(n)` in the `D=F_p`, `t=sigma=2`, `j=3` regime.
- Audit-only content: the proposed trace/Gram criterion for `Q==0` is a useful
  verifier target but is not yet banked as proved.
- Live wall: `W-F1-AA-RES-T2J3-RANK-DET-SPLIT`, the `Q==0` branch restricted
  to distinct `D`-split cubics.

Cycle 17 rank-det split scanner prompt:

- `prompts/20260618_cycle17_rank_det_split_scanner.md`
- Status: `PROMPT / AUDIT`.
- Target: implement a scanner for the Cycle 16 `Q==0` branch and decide
  whether split-distinct cubics give `C2=O(p)` or `C2=Theta(p^2)` in the
  restricted `D=F_p`, `t=sigma=2`, `j=3` toy window.

Cycle 18 resonance slope-map collapse reconstruction:

- `audits/20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`
- `local_checks/20260618_cycle18_resonance_slope_symbolic.py`
- Status: `BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT`.
- Banked content: from the Cycle 14 affine forms,
  `Delta=(p1-tau3)(q2-tau3)-p2 q1`; hence `Delta0` is monic quadratic in
  `tau3` and `Delta1` is at most linear in `tau3`. The non-coprime branch is
  either `Delta1==0` or a graph `tau3=-h/s`, where the slope becomes
  `z=(p1+h/s)/q1`.
- Live wall:
  `W-F1-AA-RES-T2J3-RESONANCE-SLOPE-MAP-COLLAPSE`.
  This is still sub-reserve (`eta=2/n`) and has no list/CA/MCA/protocol
  consequence without a separate conversion theorem.
