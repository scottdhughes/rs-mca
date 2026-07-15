# Cross-model review: reduced-CRT `(3,1,3,(2,2,2))` lemma

**Reviewer:** Claude Sonnet, read-only CLI pass, fresh non-persistent session.

**Verdict:** YELLOW.

**Ledger authorization:** NO.

## Statement audited

The uniform reduced-CRT incidence lemma in
`experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_lemma.md`, under its
printed hypotheses only. Numerical and CAS outputs were not treated as proof.

## Files read

- `experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_lemma.md`
- `experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_lemma.sage`
- `experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_cas.py`
- `experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_ledger.py`

The owner-partition and prior v4 ledger certificates were hash-linked but were
not independently read in this pass.

## Findings

### Medium: load-bearing semantic bridge is missing

The pure algebra proves that every monic cubic on a compatible rank-drop
stratum has nonconstant `gcd(F,V)`. The audited file does not, however, define
`H`, `L_core`, and `W_expl` sufficiently to prove that a root of
`gcd(F_h,V)` is necessarily an additional core agreement excluding exact
`d=3`. The displayed identities

\[
W_{\rm expl}=RHV,
\qquad
c_iL_{\rm core}=c_iHF
\]

are asserted rather than derived from canonical reconstruction definitions in
the reviewed packet. The profile-migration conclusion therefore remains an
external semantic implication, not a proved consequence of the printed local
hypotheses.

### Low: global ledger disjointness was not independently checked

The Python verifier checks 432 unique pattern IDs, one matched prior-ledger
row, and hash consistency. Whether this replacement is disjoint from every
other project charge still depends on the owner-partition and v4 ledger
certificates, which this review did not read.

### No defect: reduced-CRT algebra

The reviewer independently confirmed:

- `rank M<3` plus affine compatibility gives
  `dim ker[M|u]=4-rank[M|u]>=2`, because `u` is the `f_3=1` column of the
  homogeneous four-column map;
- `B | F_0V_1-F_1V_0` and the degree bound at most five force the cross
  polynomial to vanish;
- the UFD argument forces `deg gcd(F,V)>0` for every monic cubic solution on a
  compatible rank-drop stratum;
- `V=0` is excluded because `G` is a unit modulo `B` and `deg F<deg B`;
- all three columns of `M` and the first row of `u` agree with direct
  polynomial reduction.

Rows two and three of `u` were not hand-rederived, a low-risk residual because
the construction is identical and the exact symbolic identity is separately
certified.

## Consequence

The algebraic common-factor lemma is GREEN. The exact-profile migration and
ledger implication are YELLOW. The proposed charge `432` must not be banked;
the current profile charge remains `155,952`, the current complete add-back
remains `1,503,967`, and current unresolved mass remains `668,803`.

## Minimal next action

Read the canonical sunflower-reconstruction definitions and prove one explicit
bridge lemma: under those definitions, every root of `gcd(F_h,V)` is a genuine
additional core agreement distinct from the restored point `h`. Only after
that implication and the linked ledger disjointness are independently checked
may the conditional `432` charge be promoted.
