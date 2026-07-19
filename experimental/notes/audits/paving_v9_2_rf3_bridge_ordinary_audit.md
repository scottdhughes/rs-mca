# Ordinary audit of the Paving v9.2 RF3'' global-degree bridge

Status: AUDIT PASS (mathematics); primary-source pins verified 2026-07-19

Target: `experimental/notes/audits/paving_v9_2_rf3_global_degree_bridge.md`
(the integrated PR #893 packet; on-disk SHA-256 pinned by its companion
verifier and unchanged by this audit).

This is the ordinary audit requested at triage before promotion of RF3''
into the next Paving revision.  Method: six independent adversarial review
lanes (mixed frontier models, maximum effort), each instructed to refute its
assigned sections by re-derivation, with boundary sweeps at
a in {1,2}, b=1, w=0, K=1, t in {0,1}, r=0, and e_i>1; plus a
primary-source fetch-and-verify pass.  Gates rerun fresh: verifier
`--check` PASS (semantic_checks=286067) and `--tamper-selftest` 16/16.

## Verdicts

- Sections 1-2 (factorization, regular point, content ledger):
  CONFIRMED.  (3) recomputed from discriminant homogeneity/isobarity; the
  (4) chain and the indispensable leading-coefficient factor at a_i=1
  verified; the Gauss-lemma content bound (7) and the covering assignment
  re-derived, including the C(x_0,gamma) != 0 vs C(X,gamma) = 0 corner.
- Section 3 nonlinear induction (8)-(26): CONFIRMED.  The full corrected
  weight induction was re-derived independently: (10) exactly; the (14)
  negative-exponent case licensed by W | lc_Y(R(x_0,Y,Z)) (multiplicativity
  over F[Z]); both exponents in (18) nonnegative in every index case; (19)
  collapses to L_t term-by-term; (20)-(22) strictly positive at all
  boundaries; (24)-(26) exponent-safe including K=1.
- Section 4 linear branch (27)-(31): CONFIRMED.  Re-proved by hand and by
  2400 randomized exact-arithmetic replays (fresh code, no verifier reuse).
  The t-range question closes cleanly: (I2) with K >= 1 forces U > K, so
  K <= t <= U-1 is never vacuous in a harmful way.
- Sections 5-6 (incidence, chosen support, pair sum): CONFIRMED.  (33)-(36)
  re-derived (the strict |T| > r+1 in (32) is load-bearing: an explicit
  r=5, |T|=6, |B|=6 configuration meets the non-strict variant); (37)-(38)
  and the aggregation are arithmetic-tight against (I3).
- Section 7 binding to v9.2: CONFIRMED.  The hypothesis map is valid for
  all real D_X, D_Y (integer x < real y iff x <= ceil(y)-1); the
  top-comparison hypotheses in fact prove the stronger
  (A-K)(2U-1) > (n-K)(2K+1); all four RF3'' row ceilings recomputed from
  the v9.2 row data byte-exact (274589064742753629, 274721012201293956,
  274578888391562205, 274861787390263486), matching the predecessor table;
  substituting RF3'' into `thm:retained-degree-mca` requires no structural
  change (RF4 existence and the D_X < mA forcing are threshold-independent).
- Companion verifier: PASS.  Case counts reproduced (nonlinear 475, linear
  16, partitions 853); the 475 count re-derived by hand; no tautological
  live checks found (self-test depth gaps listed below).
- Lean companion: source inspection clean — no axiom/sorry/admit; the two
  bridge targets are Prop-valued definitions, never asserted, matching the
  "typed, explicitly unformalized target" claim; proved arithmetic
  identities match independent hand derivations.  Full `lake build`:
  SUCCESS (8040 jobs, 2026-07-19); `#print axioms` reports only the three
  standard kernel axioms (propext, Classical.choice, Quot.sound).

## Primary-source verification (2026-07-19)

Both pinned ECCC artifacts were fetched and hash byte-exact matches to the
bridge note's pins:

- ECCC TR20-083 revision 3 (BCIKS):
  `84264f52e16dc40108321c8d5b33ac3a03392fc0a9326fd49a229f7e30b804b1`.
- ECCC TR25-169 (BCHKS):
  `f1be50e43e26809f868c7d042104063a4f7353a7923f68b98ba8a6912e500206`.

Local copies live at `experimental/literature/proximity-gaps-mca/`
(gitignored per repository literature policy; the annotated index carries
the pins).  Against the printed TR20-083 rev3 Appendix A:

- Claim A.2 prints xi = W(Z)^{d-2} zeta — the negative exponent at d=1 is
  as the bridge claims (repair 1 confirmed as printed).
- The Claim A.2 base case prints the equality Lambda(T) = Lambda(W) + 1,
  which the bridge's H = Y^2 + Z^3 witness refutes (repair 2 confirmed as
  printed).
- The printed numerator estimate Lambda(xi) <= (D-1) + (d-2)Lambda(W) is
  exceeded by the bridge's F_5 witness (degree 4 > 3), confirming that the
  full weight induction, not just the base case, required replacement.
- The declaration "Lemma A.1 is used as printed" is ACCURATE: the printed
  lemma and its resultant proof already carry the weight
  Lambda(T) = D + 1 - d_H = ell fixed in Appendix A.2, exactly as used in
  display (11).
- TR25-169: the content-free D_Z redefinition ("the (1,1) weighted (Y,Z)
  degree of the content-free part of R(x_0,Y,Z)") and the accompanying
  content-degree bookkeeping appear in the Section-3.2 material as
  described; the bridge's refusal to import that replacement is the
  correct boundary, per the predecessor obstruction witness.

ePrint 2020/654 and 2025/2055 remain Cloudflare-gated to non-browser
fetches and are different artifacts from the ECCC pins (different cover
pages, different hashes).  The canonical pins for the v9.2 retained-factor
audit chain are the two ECCC hashes above; the v8 audit's ePrint-2025/2055
pin belongs to the superseded v8 packet and is out of scope here.

## Punch list for the next Paving revision (all minor; none blocking)

1. State g >= a where (13) concludes chi >= a-1 (the bound needs it; it is
   immediate since R_i carries Y^{a}).
2. State the d <= V-1 ceiling conversion in Section 7, as done for
   E <= U-1.
3. Show the top-comparison algebra, or state the stronger (2K+1) form it
   actually proves.
4. Give the one-line product-monotonicity derivation of (39).
5. Define L in the a=1 branch (L = F(Z)) before Section 5's "common
   output" refers to Gamma in L[X].
6. Fix five bare `qquad` typos (bridge note lines 372, 379, 512, 519,
   525).
7. Reword the vacuous conditional "If a_* := sum_i a_i <= d" (always true;
   only a_i <= d is used).

## Verifier/Lean hardening (optional; non-blocking)

- Four tamper-selftest mutations (base-case-defect, derivative-defect,
  nonlinear-L, RF3-content-coefficient) are intercepted by shallow
  parameter self-comparison guards before reaching the deep check they
  nominally target; the deep checks do fire when reached.
- The 853-partition sweep exercises no e_i > 1 case (a single hardcoded
  multiplicity-2 factor elsewhere does) and the eq (3)-(4) regular-point
  chain only runs at K=2.
- Lean `nonlinearL` uses coefficient 2t-1 unconditionally and so does not
  cover the note's t=0 base case (nothing instantiates it there;
  CORRESPONDENCE.md should scope it explicitly).

## Conclusion

The RF3'' integer core theorem and its v9.2 corollary survive adversarial
re-derivation intact; every issue found is presentational or
defense-in-depth.  With the source pins now verified against the fetched
primary artifacts, the packet meets the ordinary-audit bar for promotion:
a future release can state RF3'' and adopt the four exact ceilings.
