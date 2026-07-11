import GrandeFinale.ChallengeIntersection

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.CollisionAwarePole

/-! ## Collision selection -/

variable {F : Type*} [Field F] [DecidableEq F]

/-- Ordered off-diagonal collisions among the evaluations of `P` at `a`. -/
def collisionCount (P : Finset F[X]) (a : F) : Nat :=
  ((Finset.univ : Finset (P × P)).filter fun pq =>
    pq.1 ≠ pq.2 ∧ pq.1.1.eval a = pq.2.1.eval a).card

/-- Two distinct degree-`≤ k` polynomials agree at at most `k` points of `Omega`. -/
theorem poly_agree_card_le {p q : F[X]} {k : Nat} (hpq : p ≠ q)
    (hdeg : (p - q).natDegree ≤ k) (Omega : Finset F) :
    (Omega.filter fun a => p.eval a = q.eval a).card ≤ k := by
  have hroot :
      (Omega.filter fun a => p.eval a = q.eval a).card ≤
        (p - q).roots.toFinset.card := by
    refine Finset.card_le_card ?_
    intro a ha
    rw [Multiset.mem_toFinset, Polynomial.mem_roots (sub_ne_zero.mpr hpq)]
    simpa [IsRoot.def, eval_sub] using sub_eq_zero.mpr (Finset.mem_filter.mp ha).2
  exact hroot.trans <|
    (Multiset.toFinset_card_le _).trans ((Polynomial.card_roots' _).trans hdeg)

/-- The total ordered off-diagonal collision count over all allowed poles. -/
theorem sum_collisionCount_le (P : Finset F[X]) (Omega : Finset F) (k : Nat)
    (hdeg : ∀ p ∈ P, p.natDegree ≤ k) :
    ∑ a ∈ Omega, collisionCount P a ≤ k * P.card * (P.card - 1) := by
  classical
  have hsum :
      ∑ a ∈ Omega, collisionCount P a ≤
        ∑ pq ∈ (Finset.univ : Finset (P × P)).filter (fun pq => pq.1 ≠ pq.2),
          (Omega.filter fun a => pq.1.1.eval a = pq.2.1.eval a).card := by
    simp only [collisionCount, Finset.card_filter]
    rw [Finset.sum_comm, Finset.sum_filter]
    exact Finset.sum_le_sum fun pq _ => by
      split_ifs <;> simp_all
  refine hsum.trans <|
    (Finset.sum_le_sum fun pq hpq =>
      show (Omega.filter fun a =>
        pq.1.1.eval a = pq.2.1.eval a).card ≤ k from ?_).trans ?_
  · have hpq_ne : (pq.1 : F[X]) ≠ pq.2 := by
      exact fun h => (Finset.mem_filter.mp hpq).2 (Subtype.ext h)
    have hdifference : ((pq.1 : F[X]) - pq.2).natDegree ≤ k := by
      exact (Polynomial.natDegree_sub_le _ _).trans <|
        max_le (hdeg pq.1 pq.1.2) (hdeg pq.2 pq.2.2)
    exact poly_agree_card_le hpq_ne hdifference Omega
  · have hoffdiag :
        (Finset.univ : Finset (P × P)).filter (fun pq => pq.1 ≠ pq.2) =
          (Finset.univ : Finset P).offDiag := by
      ext pq
      simp
    rw [hoffdiag, Finset.sum_const, Nat.nsmul_eq_mul, Finset.offDiag_card]
    have hcard : P.card * (P.card - 1) = P.card * P.card - P.card := by
      rw [Nat.mul_sub, Nat.mul_one]
    simpa only [Finset.card_univ, Fintype.card_coe, hcard, Nat.mul_comm,
      Nat.mul_assoc] using
      (le_refl (k * (P.card * P.card - P.card)))

/-- Some allowed pole has at most the average ordered collision count. -/
theorem exists_low_collision_pole (P : Finset F[X]) (Omega : Finset F) (k : Nat)
    (hOmega : Omega.Nonempty) (hdeg : ∀ p ∈ P, p.natDegree ≤ k) :
    ∃ a ∈ Omega,
      Omega.card * collisionCount P a ≤ k * P.card * (P.card - 1) := by
  obtain ⟨a, ha, havg⟩ := GrandeFinale.exists_le_average Omega hOmega (collisionCount P)
  exact ⟨a, ha, havg.trans (sum_collisionCount_le P Omega k hdeg)⟩

/-- Sum of squared evaluation-fiber sizes equals the ordered collision count. -/
theorem sum_sq_fiber_card_pairs {I B : Type*} [Fintype I] [DecidableEq B]
    (f : I → B) :
    ∑ v ∈ Finset.univ.image f,
        (Finset.univ.filter fun i => f i = v).card ^ 2 =
      (Finset.univ.filter fun p : I × I => f p.1 = f p.2).card := by
  classical
  rw [Finset.card_filter, Fintype.sum_prod_type]
  rw [← Finset.sum_fiberwise_of_maps_to (g := f)
    (fun i _ => Finset.mem_image_of_mem f (Finset.mem_univ i))]
  refine Finset.sum_congr rfl (fun v _ => ?_)
  have hinner : ∀ i ∈ Finset.univ.filter (fun i => f i = v),
      (∑ j, if f i = f j then (1 : Nat) else 0) =
        (Finset.univ.filter fun i => f i = v).card := by
    intro i hi
    rw [(Finset.mem_filter.mp hi).2, Finset.card_filter]
    exact Finset.sum_congr rfl (fun j _ => if_congr eq_comm rfl rfl)
  rw [Finset.sum_congr rfl hinner, Finset.sum_const, sq, smul_eq_mul]

/-- Exact distinct-evaluation ceiling at one low-collision pole. -/
theorem exists_eval_image_ceil (P : Finset F[X]) (Omega : Finset F) (k : Nat)
    (hP : P.Nonempty) (hOmega : Omega.Nonempty)
    (hdeg : ∀ p ∈ P, p.natDegree ≤ k) :
    ∃ a ∈ Omega,
      (P.card * Omega.card + (Omega.card + k * (P.card - 1)) - 1) /
          (Omega.card + k * (P.card - 1)) ≤
        (P.image fun p => p.eval a).card := by
  obtain ⟨a, ha, hcollision⟩ := exists_low_collision_pole P Omega k hOmega hdeg
  let f : P → F := fun p => p.1.eval a
  let values : Finset F := Finset.univ.image f
  let mult : F → Nat := fun v => (Finset.univ.filter fun p : P => f p = v).card
  have hsum : ∑ v ∈ values, mult v = P.card := by
    have h := Finset.card_eq_sum_card_fiberwise
      (s := (Finset.univ : Finset P)) (t := values) (f := f)
      (fun p _ => Finset.mem_image_of_mem f (Finset.mem_univ p))
    simpa [values, mult] using h.symm
  have hpairs :
      (Finset.univ.filter fun pq : P × P => f pq.1 = f pq.2).card =
        collisionCount P a + P.card := by
    have heq :
        (Finset.univ.filter fun pq : P × P => f pq.1 = f pq.2) =
          (Finset.univ.filter fun pq : P × P =>
            pq.1 ≠ pq.2 ∧ f pq.1 = f pq.2) ∪
          Finset.diag (Finset.univ : Finset P) := by
      ext pq
      simp
      tauto
    rw [heq, Finset.card_union_of_disjoint]
    · simp [collisionCount, f]
    · exact Finset.disjoint_left.mpr fun pq hpq hdiag =>
        (Finset.mem_filter.mp hpq).2.1 (Finset.mem_diag.mp hdiag).2
  have hsq_eq : ∑ v ∈ values, mult v ^ 2 = P.card + collisionCount P a := by
    rw [add_comm]
    exact (sum_sq_fiber_card_pairs f).trans hpairs
  have hsq :
      Omega.card * ∑ v ∈ values, mult v ^ 2 ≤
        Omega.card * P.card + k * P.card * (P.card - 1) := by
    rw [hsq_eq, Nat.mul_add]
    exact Nat.add_le_add_left hcollision _
  have hfloor := GrandeFinale.distinct_value_floor values mult
    P.card k Omega.card values.card hP.card_pos hsum rfl hsq
  have hdenom : 0 < Omega.card + k * (P.card - 1) :=
    Nat.add_pos_left hOmega.card_pos _
  have hceil := GrandeFinale.nat_ceil_div_le hdenom hfloor
  have hvalues : values = P.image fun p => p.eval a := by
    ext v
    simp [values, f]
  rw [hvalues] at hceil
  exact ⟨a, ha, hceil⟩

/-! ## Simple-pole semantics -/

variable {D : Type*}

/-- Reed--Solomon evaluation code of polynomials of degree `< k`. -/
def rsEval (ev : D → F) (k : Nat) : Submodule F (D → F) :=
  (Polynomial.degreeLT F k).map
    (LinearMap.pi (fun x : D => Polynomial.leval (ev x)))

omit [DecidableEq F] in
theorem mem_rsEval {ev : D → F} {k : Nat} {u : D → F} :
    u ∈ rsEval ev k ↔
      ∃ P : F[X], P.degree < (k : WithBot Nat) ∧ ∀ x, u x = P.eval (ev x) := by
  constructor
  · rintro ⟨P, hP, rfl⟩
    exact ⟨P, Polynomial.mem_degreeLT.mp hP, fun _ => rfl⟩
  · rintro ⟨P, hP, hu⟩
    refine ⟨P, Polynomial.mem_degreeLT.mpr hP, ?_⟩
    ext x
    exact (hu x).symm

/-- First word of the simple-pole line. -/
def fpole (ev : D → F) (U : D → F) (alpha : F) : D → F :=
  fun x => U x * (ev x - alpha)⁻¹

/-- Direction word of the simple-pole line. -/
def gpole (ev : D → F) (alpha : F) : D → F :=
  fun x => -(ev x - alpha)⁻¹

/-- A listed polynomial produces an MCA-bad slope on its agreement support. -/
theorem eval_slope_mcaBad
    (ev : D → F) (hev : Function.Injective ev)
    (k m : Nat) (hkm : k + 1 ≤ m)
    (U : D → F) (P : F[X]) (hPdeg : P.natDegree ≤ k)
    (alpha : F) (halpha : ∀ x, ev x ≠ alpha)
    (S : Finset D) (hmS : m ≤ S.card)
    (hagree : ∀ x ∈ S, U x = P.eval (ev x)) :
    GrandeFinale.MCABad (rsEval ev k : Set (D → F))
      (fpole ev U alpha) (gpole ev alpha) m (P.eval alpha) := by
  classical
  obtain ⟨Q, hQfactor⟩ := X_sub_C_dvd_sub_C_eval (a := alpha) (p := P)
  have hQdeg : Q.degree < (k : WithBot Nat) := by
    by_cases hQ0 : Q = 0
    · simp [hQ0]
    · rw [← natDegree_lt_iff_degree_lt hQ0]
      have hnum : (P - C (P.eval alpha)).natDegree ≤ k :=
        (natDegree_sub_le _ _).trans (by simp [hPdeg])
      have heq :
          (X - C alpha).natDegree + Q.natDegree =
            (P - C (P.eval alpha)).natDegree := by
        rw [hQfactor, natDegree_mul (X_sub_C_ne_zero alpha) hQ0]
      rw [natDegree_X_sub_C] at heq
      omega
  let c : D → F := fun x => Q.eval (ev x)
  have hc : c ∈ rsEval ev k :=
    mem_rsEval.mpr ⟨Q, hQdeg, fun _ => rfl⟩
  refine ⟨S, hmS, ?_, ?_⟩
  · refine ⟨c, hc, ?_⟩
    intro x hx
    have hne : ev x - alpha ≠ 0 := sub_ne_zero.mpr (halpha x)
    have hqe :
        P.eval (ev x) - P.eval alpha =
          (ev x - alpha) * Q.eval (ev x) := by
      have heval := congrArg (Polynomial.eval (ev x)) hQfactor
      simpa [eval_sub, eval_mul, eval_C, eval_X] using heval
    dsimp [c, fpole, gpole]
    rw [hagree x hx]
    field_simp [hne]
    linear_combination -hqe
  · rintro ⟨c1, hc1, c2, hc2, _h1, h2⟩
    obtain ⟨G, hGdeg, hGval⟩ := mem_rsEval.mp hc2
    let R : F[X] := (X - C alpha) * G + 1
    have hRne : R ≠ 0 := by
      intro hR0
      have heval := congrArg (Polynomial.eval alpha) hR0
      simp [R] at heval
    have hRdeg : R.natDegree ≤ k := by
      have hprod : ((X - C alpha) * G).natDegree ≤ k := by
        by_cases hG0 : G = 0
        · simp [hG0]
        · have hGnat : G.natDegree < k :=
            (natDegree_lt_iff_degree_lt hG0).mpr hGdeg
          rw [natDegree_mul (X_sub_C_ne_zero alpha) hG0, natDegree_X_sub_C]
          omega
      change ((X - C alpha) * G + 1).natDegree ≤ k
      exact (natDegree_add_le _ _).trans (by simp [hprod])
    have hroots : S.image ev ⊆ R.roots.toFinset := by
      intro y hy
      obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hy
      rw [Multiset.mem_toFinset, mem_roots hRne]
      simp only [IsRoot.def]
      have hGx : G.eval (ev x) = gpole ev alpha x :=
        (hGval x).symm.trans (h2 x hx)
      have hne : ev x - alpha ≠ 0 := sub_ne_zero.mpr (halpha x)
      simp [R, hGx, gpole, hne]
    have himage : (S.image ev).card = S.card :=
      Finset.card_image_of_injective _ hev
    have hSk : S.card ≤ k := by
      calc
        S.card = (S.image ev).card := himage.symm
        _ ≤ R.roots.toFinset.card := Finset.card_le_card hroots
        _ ≤ R.roots.card := Multiset.toFinset_card_le _
        _ ≤ R.natDegree := Polynomial.card_roots' R
        _ ≤ k := hRdeg
    omega

/-! ## Full collision-aware pole compiler -/
/-- A chosen polynomial representative for one codeword in a finite RS list. -/
noncomputable def polynomialRepresentative
    (ev : D → F) (k : ℕ) (L : Finset (D → F))
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1))
    (c : ↑L) : F[X] :=
  Classical.choose (mem_rsEval.mp (hcode c.1 c.2))

omit [DecidableEq F] in
theorem polynomialRepresentative_spec
    (ev : D → F) (k : ℕ) (L : Finset (D → F))
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1))
    (c : ↑L) :
    (polynomialRepresentative ev k L hcode c).degree <
        (k + 1 : ℕ) ∧
      ∀ x, c.1 x = (polynomialRepresentative ev k L hcode c).eval (ev x) :=
  Classical.choose_spec (mem_rsEval.mp (hcode c.1 c.2))

/-- The chosen representative has the frontiers paper's `degree ≤ k` form. -/
theorem polynomialRepresentative_natDegree_le
    (ev : D → F) (k : ℕ) (L : Finset (D → F))
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1))
    (c : ↑L) :
    (polynomialRepresentative ev k L hcode c).natDegree ≤ k := by
  by_cases hzero : polynomialRepresentative ev k L hcode c = 0
  · simp [hzero]
  · have hlt : (polynomialRepresentative ev k L hcode c).natDegree < k + 1 :=
      (natDegree_lt_iff_degree_lt hzero).mpr
        (polynomialRepresentative_spec ev k L hcode c).1
    omega

omit [DecidableEq F] in
/-- Subtype-indexed choice is injective: equal representatives evaluate to
equal listed codewords, and the list subtype then identifies the sources. -/
theorem polynomialRepresentative_injective
    (ev : D → F) (k : ℕ) (L : Finset (D → F))
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1)) :
    Function.Injective (polynomialRepresentative ev k L hcode) := by
  intro c d hrep
  apply Subtype.ext
  funext x
  calc
    c.1 x = (polynomialRepresentative ev k L hcode c).eval (ev x) :=
      (polynomialRepresentative_spec ev k L hcode c).2 x
    _ = (polynomialRepresentative ev k L hcode d).eval (ev x) := by rw [hrep]
    _ = d.1 x := (polynomialRepresentative_spec ev k L hcode d).2 x |>.symm

/-- Duplicate-free polynomial representative set of the codeword list. -/
noncomputable def polynomialRepresentatives
    (ev : D → F) (k : ℕ) (L : Finset (D → F))
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1)) : Finset F[X] :=
  L.attach.image (polynomialRepresentative ev k L hcode)

theorem polynomialRepresentatives_card
    (ev : D → F) (k : ℕ) (L : Finset (D → F))
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1)) :
    (polynomialRepresentatives ev k L hcode).card = L.card := by
  classical
  rw [polynomialRepresentatives,
    Finset.card_image_of_injective _
      (polynomialRepresentative_injective ev k L hcode)]
  simp

/-- Convert a finite nonempty codeword list into an equally large finite set of
distinct degree-`≤ k` polynomial representatives, preserving each member's
agreement support with the received word. -/
theorem exists_polynomialRepresentatives
    (ev : D → F) (k m : ℕ) (U : D → F)
    (L : Finset (D → F)) (hL : L.Nonempty)
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1))
    (hagree : ∀ c ∈ L, ∃ S : Finset D,
      m ≤ S.card ∧ ∀ x ∈ S, U x = c x) :
    ∃ P : Finset F[X],
      P.Nonempty ∧
      P.card = L.card ∧
      (∀ p ∈ P, p.natDegree ≤ k) ∧
      (∀ p ∈ P, ∃ S : Finset D,
        m ≤ S.card ∧ ∀ x ∈ S, U x = p.eval (ev x)) := by
  classical
  refine ⟨polynomialRepresentatives ev k L hcode, ?_,
    polynomialRepresentatives_card ev k L hcode, ?_, ?_⟩
  · obtain ⟨c, hc⟩ := hL
    refine ⟨polynomialRepresentative ev k L hcode ⟨c, hc⟩, ?_⟩
    simp [polynomialRepresentatives]
  · intro p hp
    rw [polynomialRepresentatives, Finset.mem_image] at hp
    obtain ⟨c, _hc, rfl⟩ := hp
    exact polynomialRepresentative_natDegree_le ev k L hcode c
  · intro p hp
    rw [polynomialRepresentatives, Finset.mem_image] at hp
    obtain ⟨c, _hc, rfl⟩ := hp
    obtain ⟨S, hScard, hUS⟩ := hagree c.1 c.2
    refine ⟨S, hScard, ?_⟩
    intro x hx
    exact (hUS x hx).trans ((polynomialRepresentative_spec ev k L hcode c).2 x)

variable [Fintype D] [DecidableEq D] [Fintype F]

/--
An explicit nonempty finite list of degree-`≤ k` polynomials, each agreeing with
one received word on at least `m` evaluation points, forces the exact
collision-aware simple-pole lower bound for the MCA numerator.
-/
theorem collisionAwarePole_le_B_MCA
    (ev : D → F) (hev : Function.Injective ev)
    (k m : Nat) (hkm : k + 1 ≤ m)
    (U : D → F) (P : Finset F[X]) (hP : P.Nonempty)
    (hPdeg : ∀ p ∈ P, p.natDegree ≤ k)
    (hagree : ∀ p ∈ P, ∃ S : Finset D,
      m ≤ S.card ∧ ∀ x ∈ S, U x = p.eval (ev x))
    (hqn : Fintype.card D < Fintype.card F) :
    P.card * (Fintype.card F - Fintype.card D) ⌈/⌉
        ((Fintype.card F - Fintype.card D) + k * (P.card - 1)) ≤
      GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) m := by
  let Omega : Finset F := Finset.univ \ Finset.univ.image ev
  have hOmegaCard : Omega.card = Fintype.card F - Fintype.card D := by
    simp [Omega, Finset.card_sdiff, Finset.card_image_of_injective _ hev]
  have hOmega : Omega.Nonempty := by
    rw [← Finset.card_pos, hOmegaCard]
    omega
  obtain ⟨alpha, halphaOmega, hceil⟩ :=
    exists_eval_image_ceil P Omega k hP hOmega hPdeg
  have halpha : ∀ x, ev x ≠ alpha := by
    intro x heq
    exact (Finset.mem_sdiff.mp halphaOmega).2 <|
      Finset.mem_image.mpr ⟨x, Finset.mem_univ x, heq⟩
  let bad : Finset F := Finset.univ.filter fun gamma =>
    GrandeFinale.MCABad (rsEval ev k : Set (D → F))
      (fpole ev U alpha) (gpole ev alpha) m gamma
  have himage_bad : (P.image fun p => p.eval alpha) ⊆ bad := by
    intro gamma hgamma
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hgamma
    obtain ⟨S, hmS, hS⟩ := hagree p hp
    exact Finset.mem_filter.mpr ⟨Finset.mem_univ _,
      eval_slope_mcaBad ev hev k m hkm U p (hPdeg p hp)
        alpha halpha S hmS hS⟩
  have himage_card :
      (P.image fun p => p.eval alpha).card ≤ bad.card :=
    Finset.card_le_card himage_bad
  have hbad_B : bad.card ≤
      GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) m := by
    change
      (Finset.univ.filter fun gamma : F =>
        GrandeFinale.MCABad (rsEval ev k : Set (D → F))
          (fpole ev U alpha) (gpole ev alpha) m gamma).card ≤
      Finset.univ.sup (fun p : (D → F) × (D → F) =>
        (Finset.univ.filter fun gamma : F =>
          GrandeFinale.MCABad (rsEval ev k : Set (D → F))
            p.1 p.2 m gamma).card)
    exact Finset.le_sup
      (f := fun p : (D → F) × (D → F) =>
        (Finset.univ.filter fun gamma : F =>
          GrandeFinale.MCABad (rsEval ev k : Set (D → F))
            p.1 p.2 m gamma).card)
      (Finset.mem_univ (fpole ev U alpha, gpole ev alpha))
  rw [Nat.ceilDiv_eq_add_pred_div]
  rw [← hOmegaCard]
  exact hceil.trans (himage_card.trans hbad_B)


/--
Source-exact collision-aware pole conversion from a finite codeword list.
-/
theorem collisionAwarePole_of_codewordList
    (ev : D → F) (hev : Function.Injective ev)
    (k m : Nat) (hkm : k + 1 ≤ m)
    (U : D → F) (L : Finset (D → F)) (hL : L.Nonempty)
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1))
    (hagree : ∀ c ∈ L, ∃ S : Finset D,
      m ≤ S.card ∧ ∀ x ∈ S, U x = c x)
    (hqn : Fintype.card D < Fintype.card F) :
    L.card * (Fintype.card F - Fintype.card D) ⌈/⌉
        ((Fintype.card F - Fintype.card D) + k * (L.card - 1)) ≤
      GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) m := by
  obtain ⟨P, hP, hcard, hPdeg, hPagree⟩ :=
    exists_polynomialRepresentatives ev k m U L hL hcode hagree
  have hbound := collisionAwarePole_le_B_MCA
    ev hev k m hkm U P hP hPdeg hPagree hqn
  simpa only [hcard] using hbound

omit [DecidableEq D] in
/--
The collision-aware full-field floor composed with exact proper-challenge
averaging. The finite codeword list remains an explicit input.
-/
theorem collisionAwarePole_challenge_of_codewordList
    (ev : D → F) (hev : Function.Injective ev)
    (k m : Nat) (hkm : k + 1 ≤ m)
    (U : D → F) (L : Finset (D → F)) (hL : L.Nonempty)
    (hcode : ∀ c ∈ L, c ∈ rsEval ev (k + 1))
    (hagree : ∀ c ∈ L, ∃ S : Finset D,
      m ≤ S.card ∧ ∀ x ∈ S, U x = c x)
    (hqn : Fintype.card D < Fintype.card F) (Gamma : Finset F) :
    (Gamma.card *
        (L.card * (Fintype.card F - Fintype.card D) ⌈/⌉
          ((Fintype.card F - Fintype.card D) + k * (L.card - 1)))) ⌈/⌉
        Fintype.card F ≤
      GrandeFinale.ChallengeIntersection.B_MCA_challenge
        (rsEval ev k : Set (D → F)) m Gamma := by
  have hfull :
      L.card * (Fintype.card F - Fintype.card D) ⌈/⌉
          ((Fintype.card F - Fintype.card D) + k * (L.card - 1)) ≤
        GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) m :=
    collisionAwarePole_of_codewordList (F := F) (D := D)
      ev hev k m hkm U L hL hcode hagree hqn
  exact GrandeFinale.ChallengeIntersection.challenge_floor_of_full_floor
    (C := rsEval ev k) (a := m)
    (M := L.card * (Fintype.card F - Fintype.card D) ⌈/⌉
      ((Fintype.card F - Fintype.card D) + k * (L.card - 1)))
    (Gamma := Gamma) hfull

end GrandeFinale.CollisionAwarePole
