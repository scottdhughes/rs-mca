import cs25_cap_v12.QuotientLedgers

/-!
# Blueprint: the aperiodic Hankel chart atlas (`sec:aperiodic-hankel-certificates`)

Skeletons (proofs `sorry`) for the contributor-facing safe-side chart atlas of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

The aperiodic branch controls all witness supports *outside* a declared
quotient-remainder family.  It is split into charts: a regular overdetermined Hankel
bucket (a single maximal minor already gives an eliminant), finite affine/curve pivot
charts, a projective-infinity chart, and a residual singular bucket (the only genuinely
unresolved piece).

At exact agreement `A ≥ k` write `j = jₐ = n − A`, `t = tₐ = A − k`, `R = n − k`.  The
support-wise finite-slope condition is a rank drop of the affine Hankel pencil
`M_A(Z) = H_{tₐ,jₐ}(u) + Z·H_{tₐ,jₐ}(v)`, where `u = Syn(f)`, `v = Syn(g)` are the
parity-check syndromes.

Formalized here:

* `hankelMat`, `hankelPencil` — the Hankel matrix `H_{t,j}(u)` and the affine pencil.
* `RegularHankelCert` — `def:hankel-regularity-certificate`: a row set of size `j+1`
  whose maximal minor `Δ_A(Z)` is a nonzero polynomial.
* `badAtExact` — a finite slope that is support-wise noncontained on a witness support
  of *exact* size `A`.
* `lem_regular_exact_agreement_eliminant` — `lem:regular-exact-agreement-eliminant`:
  such bad slopes are bounded by `deg Δ_A ≤ n − A + 1`.
* `thm_regular_closed_ball_hankel_packing` — `thm:regular-closed-ball-hankel-packing`:
  the closed-range degree-sum bound `∑_A deg Δ_A`.
* `thm_scanner_checkable_residual_aperiodic_ledger` —
  `thm:scanner-checkable-residual-aperiodic-ledger`: the scanner-checkable overall
  bad-parameter bound, with the singular bucket isolated as an explicit residual
  hypothesis.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- The `t × (j+1)` Hankel matrix `H_{t,j}(u)` with entries `u_{r+c}`, built from a
syndrome sequence `u : ℕ → F`. -/
def hankelMat (u : ℕ → F) (t j : ℕ) : Matrix (Fin t) (Fin (j + 1)) F :=
  fun r c => u (r.val + c.val)

/-- The affine Hankel pencil `M_A(Z) = H_{t,j}(u) + Z·H_{t,j}(v)` as a matrix over
`F[Z]`. -/
noncomputable def hankelPencil (u v : ℕ → F) (t j : ℕ) : Matrix (Fin t) (Fin (j + 1)) (Polynomial F) :=
  fun r c => Polynomial.C (u (r.val + c.val)) + Polynomial.X * Polynomial.C (v (r.val + c.val))

/-- **`def:hankel-regularity-certificate` — regular Hankel minor certificate.**

There is an injective choice of `j+1` rows of the `t × (j+1)` pencil whose square
submatrix has determinant a *nonzero* polynomial `Δ_A(Z) ∈ F[Z]`.  When no such row set
exists the line is *Hankel-singular at `A`*. -/
def RegularHankelCert (u v : ℕ → F) (t j : ℕ) : Prop :=
  ∃ rows : Fin (j + 1) → Fin t, Function.Injective rows ∧
    ((hankelPencil u v t j).submatrix rows id).det ≠ 0

/-- A finite slope `z` is *support-wise noncontained at exact agreement `A`* for the
line `f + z·g`: it is explained on some support `S` of size exactly `A` while `(f, g)`
is not jointly explained on `S`. -/
def badAtExact (dom : ι → F) (k : ℕ) (f g : ι → F) (A : ℕ) (z : F) : Prop :=
  ∃ S : Finset ι, S.card = A ∧
    explainedOn dom k (fun x => f x + z * g x) S ∧ ¬ jointlyExplainedOn dom k f g S

/-- **`lem:regular-exact-agreement-eliminant`.**

In the overdetermined range `tₐ ≥ jₐ + 1` (i.e. `2A ≥ n + k + 1`), if the line's
syndromes `u = Syn(f)`, `v = Syn(g)` admit a regular Hankel minor certificate, then
every finite support-wise noncontained slope at exact agreement `A` is a root of the
eliminant `Δ_A`; hence their number is at most `deg Δ_A ≤ n − A + 1`. -/
theorem lem_regular_exact_agreement_eliminant (dom : ι → F) {k A : ℕ}
    (f g : ι → F) (u v : ℕ → F)
    (hover : Fintype.card ι - A + 1 ≤ A - k)
    (hcert : RegularHankelCert u v (A - k) (Fintype.card ι - A)) :
    (Finset.univ.filter (fun z : F => badAtExact dom k f g A z)).card
      ≤ Fintype.card ι - A + 1 := by
  sorry

/-- **`thm:regular-closed-ball-hankel-packing`.**

If for each exact agreement `A ∈ {a, …, n}` in the overdetermined range a regular
Hankel minor certificate is supplied (with degree bound `dA ≥ deg Δ_A`), then the total
number of finite support-wise noncontained slopes whose exact witness size lies in this
regular bucket is at most `∑_A dA`. -/
theorem thm_regular_closed_ball_hankel_packing (dom : ι → F) {k a : ℕ}
    (f g : ι → F) (u v : ℕ → F)
    (dA : ℕ → ℕ)
    (hcert : ∀ A, a ≤ A → A ≤ Fintype.card ι → Fintype.card ι - A + 1 ≤ A - k →
        RegularHankelCert u v (A - k) (Fintype.card ι - A) ∧ Fintype.card ι - A + 1 ≤ dA A) :
    (Finset.univ.filter (fun z : F =>
        ∃ A, a ≤ A ∧ A ≤ Fintype.card ι ∧ Fintype.card ι - A + 1 ≤ A - k ∧
          badAtExact dom k f g A z)).card
      ≤ ∑ A ∈ Finset.Icc a (Fintype.card ι), dA A := by
  sorry

/-
**`thm:scanner-checkable-residual-aperiodic-ledger`.**

The scanner-checkable aperiodic ledger: assembling the regular bucket
(`thm_regular_closed_ball_hankel_packing`), the finite affine/curve pivot charts, and
the projective-infinity chart, the number of aperiodically-witnessed bad slopes is
bounded by the sum `Ureg + Upivot + Uproj` of the supplied chart counts — *provided* the
residual singular bucket is empty (`hsingular`), the only genuinely unresolved piece.
Here the aperiodic branch is the complement of a declared quotient-remainder support
family `𝒮quot`.

The classification of a bad slope into the regular / pivot / projective charts is given
by the predicates `reg`, `piv`, `proj`; the singular residual is the fourth predicate
`sing`.  Every aperiodically-witnessed bad slope falls into one of these charts
(`hcover`), each finite chart has its supplied count bound, and the singular bucket is
empty (`hsingular`).  The conclusion is the assembled ledger bound.
-/
theorem thm_scanner_checkable_residual_aperiodic_ledger (dom : ι → F) {k a : ℕ}
    (f g : ι → F) (Ureg Upivot Uproj : ℕ)
    (reg piv proj sing : F → Prop)
    (hcover : ∀ z : F, (∃ A, a ≤ A ∧ A ≤ Fintype.card ι ∧ badAtExact dom k f g A z) →
        reg z ∨ piv z ∨ proj z ∨ sing z)
    (hreg : (Finset.univ.filter reg).card ≤ Ureg)
    (hpiv : (Finset.univ.filter piv).card ≤ Upivot)
    (hproj : (Finset.univ.filter proj).card ≤ Uproj)
    (hsingular : ∀ z : F, ¬ sing z) :
    (Finset.univ.filter (fun z : F => ∃ A, a ≤ A ∧ A ≤ Fintype.card ι ∧
        badAtExact dom k f g A z)).card ≤ Ureg + Upivot + Uproj := by
  refine' le_trans ( Finset.card_le_card _ ) _;
  exact Finset.filter reg Finset.univ ∪ Finset.filter piv Finset.univ ∪ Finset.filter proj Finset.univ;
  · grind;
  · exact le_trans ( Finset.card_union_le _ _ ) ( add_le_add ( le_trans ( Finset.card_union_le _ _ ) ( add_le_add hreg hpiv ) ) hproj )

end RSCap