/-!
# Section-nonpositive rational-host EXTRACTION fails (arithmetic engine)

Statement package for the negative half of the extraction question left open by
the canonical reduced rational-host compiler
(`experimental/notes/thresholds/canonical_reduced_rational_host_compiler.md`,
PR #721, DannyExperiments).  #721 proves that IF a section-nonpositive received
line admits a reduced rational-host presentation `(RH1)-(RH2)` then its
canonical tuple is unique and the witness-exhaustive incidence compiler applies;
its first Nonclaim disclaims extraction ("every `J ≤ 0` received line has a
reduced rational-host presentation") and names it the exact next wall.

Companion note:
`experimental/notes/thresholds/section_nonpositive_extraction_counterexample.md`.
Full stdlib verifier (Lagrange interpolation, gcd reducedness, exhaustive
`(d,L)` search, positive-control iff):
`experimental/scripts/verify_section_nonpositive_extraction.py`.

This file kernel-checks the ARITHMETIC ENGINE of the counterexample — the degree
obstruction — matching the core-only (no-mathlib) house style.  The polynomial
and field semantics are certified by the Python verifier, not re-encoded here.

The obstruction.  Over `F_p`, take `r1 = g|_D` with `deg g = δ`.  A reduced
rational-host presentation with monic denominator `L`, `deg L = d`, forces the
degree-`<n` interpolant of the vector `(L(x) r1(x))_{x∈D}` to have degree
`≤ d+k-1` (the `(B)` ceiling `L c1 - T`, `deg c1 < k`, `deg T < d`).  When
`d + δ ≤ n-1` no reduction modulo `∏_{x∈D}(X-x)` occurs, so that interpolant is
`L·g`, of degree exactly `d + δ`.  Hence the ceiling is violated whenever
`δ ≥ k`.  For the family `k ≤ δ ≤ n-1-(a-k)` this holds at EVERY candidate
denominator degree `d ∈ [1, a-k]`, so no presentation exists for ANY `r0`.

No `sorry`.  No mathlib.  `omega` for the general degree facts, `decide` for the
concrete section-nonpositive rows.
-/

namespace SectionNonpositiveExtraction

/-- Section-nonpositive gate `J = a² - n(k-1) ≤ 0`, as `a² ≤ n(k-1)`.
`abbrev` so `decide` unfolds it to the decidable inequality. -/
abbrev SectionNonpositive (n k a : Nat) : Prop := a * a ≤ n * (k - 1)

/-- Per-denominator obstruction.  If `r1 = g|_D` with `deg g = δ ≥ k` and
`d + δ ≤ n-1` (so the interpolant of `L·r1` is `L·g`, degree `d+δ`, with no
reduction), then that degree strictly exceeds the rational-host `(B)` ceiling
`d + k - 1`.  Route-scoped to reduced rational-host presentations of #721. -/
theorem ceiling_violated
    (n k a d delta : Nat)
    (hk : 1 ≤ k) (hd : 1 ≤ d) (_hda : d ≤ a - k)
    (hdelta_lo : k ≤ delta) (_hdelta_hi : d + delta ≤ n - 1) :
    d + k - 1 < d + delta := by
  omega

/-- Uniform family obstruction.  For a section-nonpositive row with `a ≤ n-1`
and `r1 = g|_D`, `k ≤ δ ≤ n-1-(a-k)`, EVERY candidate denominator degree
`d ∈ [1, a-k]` both avoids interpolation reduction (`d+δ ≤ n-1`) and violates
the ceiling (`d+k-1 < d+δ`).  Since the tuple is otherwise forced, no reduced
rational-host presentation exists — for any `r0`. -/
theorem family_obstruction
    (n k a delta : Nat)
    (hk : 1 ≤ k) (_ha_lo : k + 1 ≤ a) (ha_hi : a ≤ n - 1)
    (hdelta_lo : k ≤ delta) (hdelta_hi : delta ≤ n - 1 - (a - k)) :
    ∀ d, 1 ≤ d → d ≤ a - k → (d + delta ≤ n - 1 ∧ d + k - 1 < d + delta) := by
  intro d _hd hda
  refine ⟨?_, ?_⟩ <;> omega

/-- The three certified counterexample rows carry a genuine denominator search
space and satisfy every family hypothesis.  `(p, n, k, a, δ)`:
`F17 (16,2,4,δ=5)`, `F13 (9,2,3,δ=4)`, `F11 (9,2,3,δ=3)`; each has `J = 0`,
`k+1 ≤ a ≤ n-1`, and `k ≤ δ ≤ n-1-(a-k)`. -/
theorem rows_are_valid :
    (SectionNonpositive 16 2 4 ∧ 2 + 1 ≤ 4 ∧ 4 ≤ 16 - 1
       ∧ 2 ≤ 5 ∧ 5 ≤ 16 - 1 - (4 - 2))
  ∧ (SectionNonpositive 9 2 3 ∧ 2 + 1 ≤ 3 ∧ 3 ≤ 9 - 1
       ∧ 2 ≤ 4 ∧ 4 ≤ 9 - 1 - (3 - 2))
  ∧ (SectionNonpositive 9 2 3 ∧ 2 + 1 ≤ 3 ∧ 3 ≤ 9 - 1
       ∧ 2 ≤ 3 ∧ 3 ≤ 9 - 1 - (3 - 2)) := by
  decide

/-- #721 §4.1 degree gate, boolean form: on every row with `1 ≤ k < n`,
`k+1 ≤ a ≤ n`, the section-nonpositive gate `a² ≤ n(k-1)` forces
`2a - k ≤ n-1`. -/
def gateHoldsUpTo (N : Nat) : Bool :=
  (List.range (N + 1)).all fun n =>
    (List.range n).all fun k =>
      (List.range (n + 1)).all fun a =>
        !(decide (1 ≤ k ∧ k + 1 ≤ a ∧ a * a ≤ n * (k - 1)))
          || decide (2 * a - k ≤ n - 1)

/-- The degree gate holds on every section-nonpositive row with `n ≤ 40`. -/
theorem degree_gate_n_le_40 : gateHoldsUpTo 40 = true := by native_decide

/-- Regime floor: no section-nonpositive row with `a ≤ n-1` exists below `n = 8`
(so a prime field `F_p` hosting `D ⊊ F` needs `p ≥ n+1 ≥ 9`; `F_5, F_7` are
vacuous, `F_11` is the smallest usable prime field). -/
def rowExistsAt (n : Nat) : Bool :=
  (List.range n).any fun k =>
    (List.range n).any fun a =>
      decide (1 ≤ k ∧ k + 1 ≤ a ∧ a ≤ n - 1 ∧ a * a ≤ n * (k - 1))

theorem regime_floor_is_8 :
    ((List.range 8).all fun n => rowExistsAt n = false) ∧ rowExistsAt 8 = true := by
  native_decide

end SectionNonpositiveExtraction
