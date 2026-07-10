# Asymptotic RS MCA Audit Ledger

This file is the audit companion for `experimental/asymptotic_rs_mca.tex`.
When a PR proposes changes to `asymptotic_rs_mca.tex` or its PDF, do not apply
those files directly.  Record the proposed change here first, with enough detail
for a human maintainer to decide whether the paper should be edited.

Use this ledger for:

- proposed theorem, lemma, proof, or wording changes to `asymptotic_rs_mca.tex`;
- audit results that support or challenge a specific step in the paper;
- references to machine-checkable certificates, scripts, and notes that back an
  audit claim;
- explicit nonclaims and open proof obligations.

For each entry, include the PR/source, proposed paper impact, status, files
preserved elsewhere, and next action.

## Entries

### 2026-07-10 - Profile-envelope audit, C9 support, and threshold wall packets

- **Source:** PRs `#481--#492`.
- **Status:** PROVED / CONDITIONAL / EXPERIMENTAL / AUDIT, depending on the
  packet.  No paper-level TeX/PDF changes were imported in this pass.
- **Paper impact:** These PRs support the current profile-envelope version of
  `experimental/asymptotic_rs_mca.tex`, but they do not yet justify promoting a
  new theorem into the paper.  The strongest direct paper audit is PR `#483`:
  it checks the promoted profile-envelope draft at commit `2acc7be`, reports
  the obstruction construction as replicated, confirms that profile-scale
  payments and the ray-compiler guard are handled explicitly, and leaves two
  small open gaps plus the already-known imported window-uniformity gap.
- **Numerical spine:** PR `#491` recomputes the four deployed
  profile-envelope numerical rows and records exact integer values for
  `U(a0)`, `U(a0+1)`, and `B*`.  It is an arithmetic audit of the displayed
  profile-envelope spine, not a proof of the missing deployed upper ledger.
- **C9 support packets:** PRs `#485--#489` add standalone C9-side notes and
  scripts: coherent-phase Fourier subblock payment, low-complexity endpoint
  cube exclusion, radial-shell route cut, near-norm-gate remainder packing, and
  block-profile Plotkin bounds.  These are useful local tools and route cuts.
  They should be cited as support for the C9/residual proof program only after
  their hypotheses are matched; they do not close C1--C8 exhaustion, add-back,
  the deployed adjacent rows, or the full residual theorem.
- **Threshold wall packets:** PRs `#481`, `#482`, `#484`, and `#490` sharpen
  current M31/KoalaBear threshold subwalls.  The M31 integral-ratio LP packet
  eliminates 187 shell pairs but leaves 3,254,698 open.  The KoalaBear
  Hughes-wall packets reduce the `star3` obstruction to a single point count,
  identify the principal character frequency exactly, and prove that naive
  second-moment / absolute-value large-sieve routes are too weak.  These are
  valuable because they identify the next analytic target, not because they
  close the target.
- **Lean support:** PR `#492` adds a Lean package
  `experimental/lean/m31_few_shell/` formalizing the M31 few-shell theorem
  core.  The package was imported as a formalization artifact only; no local
  Lake build was run in this integration pass.
- **Files preserved elsewhere:** Detailed notes live under
  `experimental/notes/audits/` and `experimental/notes/thresholds/`; JSON
  artifacts under `experimental/data/`; scripts under `experimental/scripts/`;
  Lean under `experimental/lean/m31_few_shell/`.
- **Next action:** Use PR `#483` as the immediate checklist before touching
  `asymptotic_rs_mca.tex`.  For C9, promote only statements whose hypotheses
  match the residual class in the paper.  For the `star3` and M31 packets,
  continue from the named open point-count / shell-pair targets rather than
  re-running the route cuts they already rule out.

### 2026-07-10 - Promoted profile-envelope replacement draft

- **Source:** Maintainer-added `experimental/asymptotic_rs_mca (1).tex`,
  reviewed against the audit findings below.
- **Status:** PROMOTED / CONDITIONAL / COUNTEREXAMPLE.
- **Paper impact:** The new draft was promoted to
  `experimental/asymptotic_rs_mca.tex` and compiled to
  `experimental/asymptotic_rs_mca.pdf`.  It supersedes the earlier compact
  identity-frontier proof.  The replacement keeps the high-energy
  BSG/quasicube elimination, but changes the main theorem to a conditional
  profile-envelope compiler.
- **What changed:** The paper now explicitly includes the profile envelope
  `Eprof`, identity-dominance as a separate specialization, a direct ray
  compiler condition `RC`, the image/Sidon residual payment, and the
  collision-aware identity lower bound.  It also adds a smooth quotient /
  Sidon / MCA obstruction showing that smoothness and `log |B| = o(n)` do not
  imply an identity-normalized Sidon payment or identity-scale numerator bound.
- **Audit resolution:** This directly addresses the audit ledger concerns from
  PRs `#439`, `#441`, `#442`, and `#444`: B1/image normalization is no longer
  hidden, add-back is stated through residual-to-full profile comparison,
  lower-side pole collisions use the collision-aware identity lower bound, and
  literal C9 is replaced by an explicitly routed Sidon/residual condition.
- **Next action:** Audit the new obstruction proof and the profile-envelope
  theorem statement line by line against `cap25_cap_v13_raw.tex`,
  `grande_finale.tex`, and the imported audit packets.  In particular, check
  that every claimed cell payment is cited at the right natural profile scale
  and that `RC` is not silently inferred from support-pair estimates.

### 2026-07-10 - Initial audit policy for paper-level PR changes

- **Source:** Maintainer instruction during open-PR integration.
- **Status:** AUDIT.
- **Paper impact:** This ledger is now the holding place for proposed
  `asymptotic_rs_mca.tex` / PDF changes.  Paper files are not edited directly
  during PR integration unless a maintainer explicitly promotes the audited
  change.
- **Current scan:** The already-fetched PR refs `#459--#478` contain no
  `.tex` or `.pdf` diffs relative to `main`; their useful asymptotic-paper
  material is in notes, data, Lean, and verifier scripts.
- **Next action:** For future PRs with paper diffs, summarize the intended
  theorem/proof change here, cite the proposed source files, and state whether
  the change is `NO ISSUE`, `NEEDS REVISION`, `COUNTEREXAMPLE`, or
  `PROMOTION CANDIDATE`.

### 2026-07-10 - Second-opinion audit packets for asymptotic_rs_mca.tex

- **Source:** PRs `#459`, `#460`, `#461`, and `#462` by LegaSage.
- **Status:** EXPERIMENTAL / AUDIT.
- **Paper impact:** These PRs do not edit the paper.  They provide independent
  second-opinion checks of four local steps in `asymptotic_rs_mca.tex`:
  Stirling / `g*` table arithmetic, sigma-block diagonal construction,
  BSG/quasicube contradiction arithmetic, and pole-line division over `F_p`.
- **Verdict to preserve:** Each packet reports `NO ISSUE` and agreement with
  the earlier #435 audit route, but this is still audit support rather than a
  paper theorem change.
- **Files preserved elsewhere:** The detailed notes, JSON certificates, and
  verifier scripts should live under `experimental/notes/audits/`,
  `experimental/data/certificates/`, and `experimental/scripts/`.
- **Next action:** If the paper is revised, cite these as independent audit
  support for the corresponding proof steps rather than copying their text into
  the paper.

### 2026-07-10 - C9 / endpoint refinements preserved outside the paper

- **Source:** PRs `#463` and `#464` by DannyExperiments, PR `#465` by
  scottdhughes, and PR `#466` by scottdhughes.
- **Status:** PROVED / EXPERIMENTAL / AUDIT, depending on the subclaim.
- **Paper impact:** These PRs refine the asymptotic C9 story around endpoint
  shortening, split-prime Parseval descent, major-arc value-set structure, and
  Frobenius-closure formal support.  They do not directly edit
  `asymptotic_rs_mca.tex` in this integration pass.
- **Verdict to preserve:** The endpoint Plotkin and split-prime notes are
  useful subregime refinements, but they explicitly do not close the full
  C1--C8 emission/add-back or any deployed finite adjacent row.  The major-arc
  packet is experimental structure evidence explaining why literal C9 fails as
  a standalone target.  The Frobenius-closure Lean packet is useful formal
  backing for the cyclic-code closure primitive invoked by the C9 discussion,
  not a formalization of the whole theorem.
- **Files preserved elsewhere:** Notes are under
  `experimental/notes/thresholds/`, Lean support is under
  `experimental/lean/powersum_rigidity/`, and verifier scripts are under
  `experimental/scripts/`.
- **Next action:** Use these as supporting audit material when revising the
  C9/primitive-residual discussion.  Do not promote them as a complete
  safe-side proof without a separate proof that the residual cells are
  exhausted and paid with constants.

### 2026-07-10 - Closed-ledger citation and in-paper proof audits

- **Source:** PRs `#433`, `#435`, `#436`, `#443`, `#449`, and `#450`.
- **Status:** AUDIT.
- **Paper impact:** These packets audit the compact asymptotic paper rather
  than directly changing it.  The main record is:
  `#433` finds the closed-ledger citations mostly exact but identifies C9
  source material, B1 normalization, B3 window uniformity, and B4 lower-side
  collision loss as gaps or bridge obligations; `#435` audits in-paper proofs
  and reports `8 NO ISSUE / 2 OPEN GAP`; `#436` isolates the B1
  image-vs-ambient normalization issue; `#443` discharges the window slide for
  established cells down to single-point closure; `#449` records the
  target-normalized frontier compiler caveat; `#450` compares the asymptotic
  crossing against the finite deployed adjacent rows.
- **Verdict to preserve:** These are promotion/audit inputs.  They support
  rewriting the paper more carefully, but they do not by themselves prove the
  remaining C9 / Q / safe-side obligations or any finite deployed adjacent row.
- **Files preserved elsewhere:** Detailed notes and verifier scripts are under
  `experimental/notes/`, `experimental/notes/audits/`, and
  `experimental/scripts/`; JSON certificates live under `experimental/data/`.
- **Next action:** When revising the paper, use these audits as a checklist:
  all C9, B1, add-back, lower-side, and finite-vs-asymptotic status labels must
  remain explicit.

### 2026-07-10 - Proposed TeX repairs held as audit material

- **Source:** PRs `#439`, `#441`, and `#442`.
- **Status:** PROMOTION CANDIDATE / AUDIT; not applied directly.
- **Paper impact:** These PRs proposed direct edits to
  `experimental/asymptotic_rs_mca.tex` and, in `#439`, a regenerated PDF.  The
  paper files were deliberately not imported.  Their proposed mathematical
  changes are recorded as follows:

  - `#439` proposes the image-normalized B1/C9 interface: use
    `L=|im Phi|`, state the safe ambient-to-image moment direction, and keep
    C9 as an explicit image-normalized input.
  - `#441` proposes the add-back repair: introduce a profile non-degeneracy
    condition and make the add-back lemma conditional on it, with a falsifier
    showing the condition is load-bearing.
  - `#442` proposes the lower-side reroute: avoid an unproved pole-reservoir
    collision-loss assertion by routing through the collision-free
    identity-prefix floor plus the existing list-to-agreement bridge.

- **Verdict to preserve:** All three look useful and should inform the next
  paper revision, but they must be reconciled with the current
  `experimental/asymptotic_rs_mca.tex` state and with the later
  `grande_finale` / v13 raw picture before promotion.
- **Files preserved elsewhere:** Imported only their notes, data, and verifier
  scripts:
  `experimental/notes/audits/asymptotic_b1_image_scale_repair.md`,
  `experimental/notes/audits/asymptotic_addback_profile_decomposition.md`,
  `experimental/notes/audits/asymptotic_lowerside_collision_free_reroute.md`,
  plus matching JSON/script artifacts where present.
- **Next action:** Prepare a maintainer-authored TeX revision that combines
  these three repairs coherently rather than applying their diffs piecemeal.

### 2026-07-10 - Literal C9 counterexample and corrected residual target

- **Source:** PR `#444` by avdeevvadim, with related support from `#451`,
  `#448`, `#447`, and `#446`.
- **Status:** COUNTEREXAMPLE / AUDIT / EXPERIMENTAL.
- **Paper impact:** The literal quantitative C9 interface is too broad: `#444`
  records a counterexample floor showing that the phrase "surviving C1--C8"
  must be made into an exact residual predicate.  `#451` supplies a strict
  Frobenius cyclotomic-defect subregime theorem; `#448` reduces the B1 bridge
  to a signed-`e_m` second-moment problem and records a dead Newton--Girard
  route; `#447` proves differential-locator/Frobenius-index cell laws; `#446`
  records extension-field toy instrumentation for the `R>w` wall.
- **Verdict to preserve:** Do not state a standalone literal C9 theorem in the
  paper.  State the residual class and paid cells precisely, then use the
  positive subregime/cell-law results only within their printed hypotheses.
- **Files preserved elsewhere:** Notes under `experimental/notes/audits/` and
  `experimental/notes/thresholds/`, with JSON/script artifacts under
  `experimental/data/` and `experimental/scripts/`.
- **Next action:** Any C9/Q section should cite this as a specification guard:
  a corrected theorem must exclude or pay the counterexample family, not assume
  it away.
