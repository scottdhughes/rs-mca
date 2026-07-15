import AsymptoticSpine.Averaging
import StaircaseLogic.Staircase

namespace AsymptoticSpine

/-!
# Integer MCA staircase and the deep-regime counting core

This module targets two elementary pieces of
`experimental/asymptotic_rs_mca_frontiers.tex`:

* `def:integer-staircase-detail` and equation (1.2): the bad-slope numerator is
  antitone on the integer agreement grid, safety is upward closed, and a first
  safe agreement is unique and antitone in the integer budget;
* `thm:deep-regime-upper`: after two slopes recover a common error pair, the
  remaining argument is a root-incidence double count.  The transverse branch
  assigns at least `t-r` distinct zero coordinates to every bad slope, while
  one affine coordinate can be assigned to at most one slope.  The tangent
  branch assigns one nontrivial support coordinate to every MCA-bad slope.

The finite-field and minimum-distance recovery step is exposed by the abstract
coordinate ledgers in `DeepPairCertificate`; the double count after such a
ledger has been constructed is proved here.  The module does not identify its
natural-number coordinates with field-valued affine roots: that semantic bridge
remains a named input.

The package remains stdlib-only and contains no `sorry`, `native_decide`, or
added axiom.
-/

/-! ## The literal identity-profile scale -/

/-- Stdlib binomial coefficient by Pascal recursion. -/
def staircaseBinom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => staircaseBinom n k + staircaseBinom n (k + 1)

/-- Pascal recursion at two positive indices. -/
@[simp] theorem staircaseBinom_succ_succ (n k : Nat) :
    staircaseBinom (n + 1) (k + 1) =
      staircaseBinom n k + staircaseBinom n (k + 1) := rfl

/-- The first nontrivial column of the Pascal triangle. -/
@[simp] theorem staircaseBinom_one : ∀ n, staircaseBinom n 1 = n
  | 0 => rfl
  | n + 1 => by
      rw [staircaseBinom_succ_succ, staircaseBinom_one]
      simp [staircaseBinom, Nat.add_comm]

/-- Cancellation-free multiplication form of the adjacent binomial identity. -/
theorem staircaseBinom_add_one_mul : ∀ n k,
    (n + 1) * staircaseBinom n k =
      staircaseBinom (n + 1) (k + 1) * (k + 1)
  | 0, 0 => by decide
  | 0, k + 1 => by simp [staircaseBinom]
  | n + 1, 0 => by
      simp [staircaseBinom, staircaseBinom_one, Nat.mul_succ, Nat.add_comm]
  | n + 1, k + 1 => by
      rw [staircaseBinom_succ_succ (n + 1) (k + 1),
        staircaseBinom_succ_succ n k]
      calc
        (n + 1 + 1) *
              (staircaseBinom n k + staircaseBinom n (k + 1)) =
            (n + 1) * staircaseBinom n k + staircaseBinom n k +
              ((n + 1) * staircaseBinom n (k + 1) +
                staircaseBinom n (k + 1)) := by
          simp only [Nat.add_mul, Nat.mul_add, Nat.one_mul]
        _ =
            staircaseBinom (n + 1) (k + 1) * (k + 1) +
              staircaseBinom n k +
                (staircaseBinom (n + 1) (k + 1 + 1) * (k + 1 + 1) +
                  staircaseBinom n (k + 1)) := by
          rw [staircaseBinom_add_one_mul n k,
            staircaseBinom_add_one_mul n (k + 1)]
        _ =
            staircaseBinom (n + 1) (k + 1) * (k + 1) +
              staircaseBinom (n + 1) (k + 1) +
                staircaseBinom (n + 1) (k + 1 + 1) * (k + 1 + 1) := by
          rw [staircaseBinom_succ_succ n k]
          ac_rfl
        _ =
            (staircaseBinom (n + 1) (k + 1) +
                staircaseBinom (n + 1) (k + 1 + 1)) *
              (k + 1 + 1) := by
          simp only [Nat.add_mul, Nat.mul_add, Nat.mul_one]
          ac_rfl

/-- Exact adjacent-row identity
`binom(n,k+1) * (k+1) = binom(n,k) * (n-k)`. -/
theorem staircaseBinom_succ_right_eq (n k : Nat) :
    staircaseBinom n (k + 1) * (k + 1) =
      staircaseBinom n k * (n - k) := by
  have e : (n + 1) * staircaseBinom n k =
      staircaseBinom n (k + 1) * (k + 1) +
        staircaseBinom n k * (k + 1) := by
    rw [← Nat.add_mul,
      Nat.add_comm (staircaseBinom n (k + 1)) (staircaseBinom n k),
      ← staircaseBinom_succ_succ, staircaseBinom_add_one_mul]
  rw [← Nat.sub_eq_of_eq_add e, Nat.mul_comm,
    ← Nat.mul_sub_left_distrib, Nat.add_sub_add_right]

/-- The literal identity-profile scale at agreement `a=K+w` from
`def:integer-staircase-detail`.  The unrounded scale
`binom(n,K+w) / |B|^w` is kept as an exact numerator/denominator pair. -/
structure IdentityRawScale where
  n : Nat
  K : Nat
  w : Nat
  baseCard : Nat
  agreement_le : K + w ≤ n
  baseCard_pos : 0 < baseCard

namespace IdentityRawScale

/-- Agreement `a=K+w`. -/
def agreement (S : IdentityRawScale) : Nat := S.K + S.w

/-- Exact numerator `binom(n,K+w)`. -/
def numerator (S : IdentityRawScale) : Nat := staircaseBinom S.n S.agreement

/-- Exact denominator `|B|^w`. -/
def denominator (S : IdentityRawScale) : Nat := S.baseCard ^ S.w

/-- The literal, unrounded identity scale. -/
def ratio (S : IdentityRawScale) : Nat × Nat := (S.numerator, S.denominator)

@[simp] theorem agreement_eq (S : IdentityRawScale) : S.agreement = S.K + S.w := rfl

@[simp] theorem numerator_eq (S : IdentityRawScale) :
    S.numerator = staircaseBinom S.n (S.K + S.w) := rfl

@[simp] theorem denominator_eq (S : IdentityRawScale) :
    S.denominator = S.baseCard ^ S.w := rfl

/-- An in-range Pascal coefficient is positive. -/
theorem staircaseBinom_pos_of_le : ∀ {n a : Nat}, a ≤ n → 0 < staircaseBinom n a := by
  intro n
  induction n with
  | zero =>
      intro a ha
      have hzero : a = 0 := by omega
      subst a
      simp [staircaseBinom]
  | succ n ih =>
      intro a ha
      cases a with
      | zero => simp [staircaseBinom]
      | succ a =>
          simp only [staircaseBinom]
          have hleft : 0 < staircaseBinom n a := ih (by omega)
          omega

/-- The identity-scale numerator is nonzero at an in-block agreement. -/
theorem numerator_pos (S : IdentityRawScale) : 0 < S.numerator :=
  staircaseBinom_pos_of_le S.agreement_le

/-- The identity-scale denominator is nonzero because the base cardinality is
positive. -/
theorem denominator_pos (S : IdentityRawScale) : 0 < S.denominator :=
  Nat.pow_pos S.baseCard_pos

/-- Well-definedness of the exact raw ratio used before any envelope or
rounding argument. -/
theorem ratio_wellDefined (S : IdentityRawScale) :
    S.agreement ≤ S.n ∧ 0 < S.numerator ∧ 0 < S.denominator :=
  ⟨S.agreement_le, S.numerator_pos, S.denominator_pos⟩

/-- The adjacent identity scale at agreement `K + (w + 1)`. -/
def next (S : IdentityRawScale) (hnext : S.agreement + 1 ≤ S.n) :
    IdentityRawScale where
  n := S.n
  K := S.K
  w := S.w + 1
  baseCard := S.baseCard
  agreement_le := by simpa [agreement, Nat.add_assoc] using hnext
  baseCard_pos := S.baseCard_pos

/-- Advancing the weight increases agreement by exactly one. -/
@[simp] theorem next_agreement (S : IdentityRawScale)
    (hnext : S.agreement + 1 ≤ S.n) :
    (S.next hnext).agreement = S.agreement + 1 := by
  simp [next, agreement, Nat.add_assoc]

/-- Advancing the weight multiplies the exact denominator by `|B|`. -/
@[simp] theorem next_denominator (S : IdentityRawScale)
    (hnext : S.agreement + 1 ≤ S.n) :
    (S.next hnext).denominator = S.denominator * S.baseCard := by
  simp [next, denominator, Nat.pow_succ]

/-- The adjacent numerator step, stated without division or cancellation. -/
theorem next_numerator_step (S : IdentityRawScale)
    (hnext : S.agreement + 1 ≤ S.n) :
    (S.next hnext).numerator * (S.agreement + 1) =
      S.numerator * (S.n - S.agreement) := by
  simpa [next, numerator, agreement, Nat.add_assoc] using
    staircaseBinom_succ_right_eq S.n S.agreement

/-- Exact adjacent identity-scale ratio in cross-multiplied form:
`I(a+1) / I(a) = (n-a) / ((a+1)|B|)`.

The cross product avoids any divisibility or rational coercion assumptions. -/
theorem adjacent_ratio_cross (S : IdentityRawScale)
    (hnext : S.agreement + 1 ≤ S.n) :
    ((S.next hnext).numerator * S.denominator) *
        ((S.agreement + 1) * S.baseCard) =
      (S.numerator * (S.next hnext).denominator) *
        (S.n - S.agreement) := by
  rw [next_denominator]
  calc
    ((S.next hnext).numerator * S.denominator) *
          ((S.agreement + 1) * S.baseCard) =
        ((S.next hnext).numerator * (S.agreement + 1)) *
          (S.denominator * S.baseCard) := by ac_rfl
    _ = (S.numerator * (S.n - S.agreement)) *
          (S.denominator * S.baseCard) := by
      rw [next_numerator_step]
    _ = (S.numerator * (S.denominator * S.baseCard)) *
          (S.n - S.agreement) := by ac_rfl

end IdentityRawScale

/-! ## The frontiers paper's integer staircase -/

/-- The exact integer agreement staircase attached to an MCA numerator.

The agreement grid is `[k+1,n]`.  `numerator a` is the number of bad challenge
slopes at threshold `a`; increasing `a` can only remove witnesses, hence the
on-grid antitonicity field.  The target-dependent integer budget is supplied
separately, matching `B* = floor (epsilon * |Gamma|)` in equation (1.2). -/
structure FrontiersStaircase where
  numerator : Nat → Nat
  k : Nat
  n : Nat
  k_lt_n : k < n
  antitone : ∀ a b, k + 1 ≤ a → a ≤ b → b ≤ n → numerator b ≤ numerator a

namespace FrontiersStaircase

/-- Agreement belongs to the paper's integer grid `{k+1,...,n}`. -/
def inGrid (S : FrontiersStaircase) (a : Nat) : Prop := S.k + 1 ≤ a ∧ a ≤ S.n

/-- Reuse the repository's proved stdlib staircase kernel on the exact MCA
agreement interval. -/
def toCore (S : FrontiersStaircase) (budget : Nat) : StaircaseLogic.Staircase where
  N := S.numerator
  B := budget
  n := S.n
  amin := S.k + 1
  amax := S.n
  hI := S.k_lt_n
  hn := Nat.le_refl S.n
  antitone := fun a b ha hab hb => S.antitone a b ha hab hb

/-- An agreement is safe when its bad-slope numerator is at most the integer
target budget. -/
def safe (S : FrontiersStaircase) (budget a : Nat) : Prop :=
  (S.toCore budget).safe a

/-- An agreement is unsafe when its bad-slope numerator exceeds the budget. -/
def Unsafe (S : FrontiersStaircase) (budget a : Nat) : Prop :=
  (S.toCore budget).Unsafe a

/-- The proposition that `a` is the first safe agreement in `{k+1,...,n}`. -/
def IsFirstSafe (S : FrontiersStaircase) (budget a : Nat) : Prop :=
  (S.toCore budget).IsFirstSafe a

/-- Computable first-safe scan on the finite agreement grid.  Its specification
below is asserted only when the paper's defining safe set is nonempty and hence
has a first element. -/
def firstSafe (S : FrontiersStaircase) (budget : Nat) : Nat :=
  (S.toCore budget).firstSafe

/-- The closed integer radius corresponding to agreement `a`. -/
def closedRadius (S : FrontiersStaircase) (a : Nat) : Nat := S.n - a

/-- Safety is upward closed on the agreement grid. -/
theorem safe_up (S : FrontiersStaircase) (budget : Nat) {a b : Nat}
    (ha : S.k + 1 ≤ a) (hab : a ≤ b) (hb : b ≤ S.n)
    (hsafe : S.safe budget a) : S.safe budget b :=
  (S.toCore budget).safe_up ha hab hb hsafe

/-- A first safe agreement is unique, so equation (1.2) is well-defined when
its defining set is nonempty. -/
theorem firstSafe_unique (S : FrontiersStaircase) (budget : Nat) {a b : Nat}
    (ha : S.IsFirstSafe budget a) (hb : S.IsFirstSafe budget b) : a = b :=
  (S.toCore budget).firstSafe_unique ha hb

/-- Every safe point on the finite agreement grid has a first safe predecessor.
This is the existence half of equation (1.2), proved without adding a choice
operator to the threshold definition. -/
theorem exists_firstSafe_of_safe (S : FrontiersStaircase) (budget : Nat) :
    ∀ a, S.k + 1 ≤ a → a ≤ S.n → S.safe budget a →
      ∃ b, S.IsFirstSafe budget b := by
  intro a
  induction a with
  | zero =>
      intro ha _ _
      omega
  | succ a ih =>
      intro ha han hsafe
      by_cases hleft : a + 1 = S.k + 1
      · refine ⟨a + 1, ha, han, hsafe, ?_⟩
        intro b hb hlt
        change S.k + 1 ≤ b at hb
        exact False.elim (by omega)
      · have hpred_lo : S.k + 1 ≤ a := by omega
        have hpred_hi : a ≤ S.n := by omega
        by_cases hpred : S.safe budget a
        · exact ih hpred_lo hpred_hi hpred
        · refine ⟨a + 1, ha, han, hsafe, ?_⟩
          intro b hb hba
          change S.k + 1 ≤ b at hb
          apply ((S.toCore budget).unsafe_iff_not_safe b).2
          intro hbsafe
          have hbp : b ≤ a := by omega
          have hpredSafe := S.safe_up budget hb hbp hpred_hi hbsafe
          exact hpred hpredSafe

/-- The threshold-defining set is nonempty exactly when the top agreement is
safe; in that case a unique first safe agreement exists. -/
theorem threshold_exists_iff_top_safe (S : FrontiersStaircase) (budget : Nat) :
    (∃ a, S.IsFirstSafe budget a) ↔ S.safe budget S.n := by
  constructor
  · rintro ⟨a, ha⟩
    exact S.safe_up budget ha.1 ha.2.1 (Nat.le_refl _) ha.2.2.1
  · intro htop
    have hgrid : S.k + 1 ≤ S.n := S.k_lt_n
    exact S.exists_firstSafe_of_safe budget S.n hgrid (Nat.le_refl _) htop

/-- If a first safe point exists, the computable scan returns it and therefore
satisfies the exact first-safe specification. -/
theorem firstSafe_spec (S : FrontiersStaircase) (budget : Nat)
    (h : ∃ a, S.IsFirstSafe budget a) :
    S.IsFirstSafe budget (S.firstSafe budget) := by
  obtain ⟨a, ha⟩ := h
  have heq : S.firstSafe budget = a :=
    (S.toCore budget).firstSafe_eq_of_isFirstSafe ha
  rw [heq]
  exact ha

/-- Direct well-definedness form: if the maximum agreement is safe, the scan
returns the unique first safe agreement. -/
theorem firstSafe_spec_of_top_safe (S : FrontiersStaircase) (budget : Nat)
    (htop : S.safe budget S.n) :
    S.IsFirstSafe budget (S.firstSafe budget) :=
  S.firstSafe_spec budget ((S.threshold_exists_iff_top_safe budget).2 htop)

/-- The first-safe scan lies on the paper's agreement grid whenever the
threshold exists. -/
theorem firstSafe_inGrid (S : FrontiersStaircase) (budget : Nat)
    (h : ∃ a, S.IsFirstSafe budget a) :
    S.inGrid (S.firstSafe budget) := by
  have hs := S.firstSafe_spec budget h
  exact ⟨hs.1, hs.2.1⟩

/-- Increasing the target budget cannot move the first safe agreement to the
right.  Thus the agreement threshold is antitone in `B*`, while the closed
radius frontier is monotone in `B*`. -/
theorem firstSafe_antitone_budget (S : FrontiersStaircase) {budget budget' : Nat}
    (hbudget : budget ≤ budget')
    (h : ∃ a, S.IsFirstSafe budget a)
    (h' : ∃ a, S.IsFirstSafe budget' a) :
    S.firstSafe budget' ≤ S.firstSafe budget := by
  have hs := S.firstSafe_spec budget h
  have hs' := S.firstSafe_spec budget' h'
  apply Nat.le_of_not_gt
  intro hlt
  have hunsafe := hs'.2.2.2 (S.firstSafe budget) hs.1 hlt
  have hsafe := hs.2.2.1
  change budget' < S.numerator (S.firstSafe budget) at hunsafe
  change S.numerator (S.firstSafe budget) ≤ budget at hsafe
  omega

/-- The same budget monotonicity in the paper's radius convention. -/
theorem closedRadius_monotone_budget (S : FrontiersStaircase)
    {budget budget' : Nat} (hbudget : budget ≤ budget')
    (h : ∃ a, S.IsFirstSafe budget a)
    (h' : ∃ a, S.IsFirstSafe budget' a) :
    S.closedRadius (S.firstSafe budget) ≤
      S.closedRadius (S.firstSafe budget') := by
  unfold closedRadius
  have := S.firstSafe_antitone_budget hbudget h h'
  omega

/-- An adjacent unsafe/safe certificate pins the first safe agreement exactly,
the finite-row specialization of the integer staircase. -/
theorem adjacent_isFirstSafe (S : FrontiersStaircase) (budget a0 : Nat)
    (h0 : S.k + 1 ≤ a0) (h1 : a0 + 1 ≤ S.n)
    (hunsafe : S.Unsafe budget a0) (hsafe : S.safe budget (a0 + 1)) :
    S.IsFirstSafe budget (a0 + 1) :=
  (S.toCore budget).oneStep_isFirstSafe a0 h0 h1 hunsafe hsafe

/-- At an adjacent unsafe/safe identity-profile pair, the exact scale ratio
holds and the right endpoint is the unique first-safe agreement. -/
theorem adjacent_identity_ratio_pins_threshold
    (S : FrontiersStaircase) (I : IdentityRawScale) (budget : Nat)
    (hblock : I.n = S.n)
    (hleft : S.k + 1 ≤ I.agreement)
    (hnext : I.agreement + 1 ≤ I.n)
    (hunsafe : S.Unsafe budget I.agreement)
    (hsafe : S.safe budget (I.agreement + 1)) :
    (((I.next hnext).numerator * I.denominator) *
          ((I.agreement + 1) * I.baseCard) =
        (I.numerator * (I.next hnext).denominator) *
          (I.n - I.agreement)) ∧
      S.IsFirstSafe budget (I.agreement + 1) := by
  refine ⟨I.adjacent_ratio_cross hnext, ?_⟩
  apply S.adjacent_isFirstSafe budget I.agreement hleft
  · simpa [hblock] using hnext
  · exact hunsafe
  · exact hsafe

end FrontiersStaircase

/-! ## Root-incidence certificates for the deep regime -/

/-- Pigeonhole for a duplicate-free list of support indices.  This is the
finite-cardinality primitive used in both branches of the deep proof. -/
theorem nodup_lt_length_deep : ∀ (t : Nat) (l : List Nat),
    l.Nodup → (∀ x ∈ l, x < t) → l.length ≤ t := by
  intro t
  induction t with
  | zero =>
      intro l _ hbound
      cases l with
      | nil => simp
      | cons x xs => exact absurd (hbound x (by simp)) (by omega)
  | succ t ih =>
      intro l hnodup hbound
      by_cases ht : t ∈ l
      · have herase : (l.erase t).Nodup := hnodup.erase t
        have hbound' : ∀ x ∈ l.erase t, x < t := by
          intro x hx
          have hx' := hnodup.mem_erase_iff.mp hx
          have hxt := hbound x hx'.2
          omega
        have hlen : (l.erase t).length = l.length - 1 :=
          List.length_erase_of_mem ht
        have hpos : 0 < l.length := List.length_pos_of_mem ht
        have hrec := ih (l.erase t) herase hbound'
        omega
      · have hbound' : ∀ x ∈ l, x < t := by
          intro x hx
          have hxt := hbound x hx
          have hne : x ≠ t := fun heq => ht (heq ▸ hx)
          omega
        exact Nat.le_succ_of_le (ih l hnodup hbound')

/-- Transverse branch after common-error-pair recovery.

`t` is the support size of the recovered error pair.  Each block lists zero
coordinates for one bad slope.  The block has at least `t-r` coordinates;
the flattened list is duplicate-free because a nonzero affine coordinate has
at most one root; and every listed coordinate is an index in the `t`-element
support. -/
structure TransverseRootCertificate (r badCount : Nat) where
  t : Nat
  blocks : List (List Nat)
  count_eq : blocks.length = badCount
  outside_tangent : r < t
  roots_per_slope : ∀ block ∈ blocks, t - r ≤ block.length
  pooled_roots_nodup : blocks.flatten.Nodup
  roots_in_support : ∀ x ∈ blocks.flatten, x < t

/-- Tangent branch after common-error-pair recovery.

Here `t ≤ r`.  `roots` is an abstract injective coordinate ledger, intended to
be constructed from one vanishing support coordinate for every bad slope.
Support-wise MCA nontriviality and the affine root equations are not represented
inside this structure; they belong to the semantic ledger-construction input. -/
structure TangentRootCertificate (r badCount : Nat) where
  t : Nat
  roots : List Nat
  count_eq : roots.length = badCount
  inside_tangent : t ≤ r
  chosen_roots_nodup : roots.Nodup
  roots_in_support : ∀ x ∈ roots, x < t

/-- The abstract coordinate-ledger alternatives consumed after common-error-pair
recovery and affine root verification. -/
def DeepPairCertificate (r badCount : Nat) : Type :=
  Sum (TransverseRootCertificate r badCount) (TangentRootCertificate r badCount)

/-- Transverse root-incidence double count:
`#bad * (t-r) ≤ t`. -/
theorem transverse_root_double_count {r badCount : Nat}
    (C : TransverseRootCertificate r badCount) :
    badCount * (C.t - r) ≤ C.t := by
  have hlow : C.blocks.length * (C.t - r) ≤
      listSum (C.blocks.map List.length) :=
    length_mul_le_listSum_map List.length (C.t - r) C.blocks C.roots_per_slope
  have hcap : C.blocks.flatten.length ≤ C.t :=
    nodup_lt_length_deep C.t C.blocks.flatten C.pooled_roots_nodup C.roots_in_support
  calc
    badCount * (C.t - r) = C.blocks.length * (C.t - r) := by rw [C.count_eq]
    _ ≤ listSum (C.blocks.map List.length) := hlow
    _ = C.blocks.flatten.length := (length_flatten C.blocks).symm
    _ ≤ C.t := hcap

/-- Arithmetic closure of the transverse double count.  If `r<t` and
`z*(t-r)≤t`, then `z≤r+1`. -/
theorem card_le_radius_succ_of_mul_gap_le {z r t : Nat}
    (hrt : r < t) (hmul : z * (t - r) ≤ t) : z ≤ r + 1 := by
  apply Nat.le_of_not_gt
  intro hz
  have hgap : 1 ≤ t - r := by omega
  have hrscale : r ≤ r * (t - r) := by
    have := Nat.mul_le_mul_left r hgap
    simpa using this
  have hstrict : t < (r + 2) * (t - r) := by
    calc
      t = r + (t - r) := by omega
      _ < r * (t - r) + (t - r) + (t - r) := by omega
      _ = (r + 2) * (t - r) := by
        rw [Nat.add_mul, Nat.add_assoc, Nat.two_mul]
  have hlarge : (r + 2) * (t - r) ≤ z * (t - r) :=
    Nat.mul_le_mul_right (t - r) (by omega)
  omega

/-- Every transverse certificate has at most `r+1` bad slopes. -/
theorem transverse_badCount_le {r badCount : Nat}
    (C : TransverseRootCertificate r badCount) : badCount ≤ r + 1 :=
  card_le_radius_succ_of_mul_gap_le C.outside_tangent
    (transverse_root_double_count C)

/-- Every tangent coordinate ledger has at most `r` bad slopes. -/
theorem tangent_badCount_le {r badCount : Nat}
    (C : TangentRootCertificate r badCount) : badCount ≤ r := by
  have hcap : C.roots.length ≤ C.t :=
    nodup_lt_length_deep C.t C.roots C.chosen_roots_nodup C.roots_in_support
  rw [C.count_eq] at hcap
  have ht := C.inside_tangent
  omega

/-- The recovered-pair combinatorial core of `thm:deep-regime-upper`. -/
theorem deep_pair_badCount_le {r badCount : Nat}
    (C : DeepPairCertificate r badCount) : badCount ≤ r + 1 := by
  rcases C with h | h
  · exact transverse_badCount_le h
  · exact Nat.le_trans (tangent_badCount_le h) (Nat.le_succ r)

/-- An exhaustive finite enumeration of received pairs. -/
structure FinitePairEnumeration (Pair : Type) where
  pairs : List Pair
  complete : ∀ p : Pair, p ∈ pairs

/-- Maximum bad-slope numerator over an exhaustive finite pair enumeration. -/
def badSlopeNumerator {Pair : Type} (M : FinitePairEnumeration Pair)
    (badCount : Pair → Nat) : Nat :=
  listMax (M.pairs.map badCount)

/-- **Deep-regime upper bound, finite combinatorial form.**

Put `r=n-a`.  Under `3r≤d-1`, the code/field recovery layer must supply, for
every received pair, one of the two exact root certificates above.  The proved
double count then gives `B_C^MCA(a)≤r+1`, where the left side is represented by
the maximum bad-slope count over the finite received-pair list.

`incidenceLedger` is the unformalized semantic interface: it must construct the
displayed natural-number ledgers from the two-slope linear-code recovery,
support-wise nontriviality, and affine-coordinate root equations.  The
certificates themselves do not encode those field equations.  No Fourier,
atlas, smoothness, or ray-compiler input occurs in this theorem. -/
theorem deep_regime_upper {Pair : Type} (M : FinitePairEnumeration Pair)
    (badCount : Pair → Nat) (n a d : Nat)
    (ha : a ≤ n) (hdeep : 3 * (n - a) ≤ d - 1)
    (incidenceLedger : ∀ p ∈ M.pairs, a ≤ n → 3 * (n - a) ≤ d - 1 →
      DeepPairCertificate (n - a) (badCount p)) :
    badSlopeNumerator M badCount ≤ n - a + 1 := by
  apply listMax_le
  intro z hz
  obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hz
  exact deep_pair_badCount_le (incidenceLedger p hp ha hdeep)

/-- For positive minimum distance, the paper's truncated deep condition is
equivalent to the subtraction-free strict inequality. -/
theorem deep_range_iff_lt {r d : Nat} (hd : 0 < d) :
    3 * r ≤ d - 1 ↔ 3 * r < d := by
  omega

/-! ## Exact certificates exercising both branches -/

/-- Dense/transverse toy: `r=2`, active support `t=3`, and three slopes, each
charged to its unique root coordinate. -/
def denseRootToy : TransverseRootCertificate 2 3 where
  t := 3
  blocks := [[0], [1], [2]]
  count_eq := by decide
  outside_tangent := by decide
  roots_per_slope := by decide
  pooled_roots_nodup := by decide
  roots_in_support := by decide

/-- The dense toy reaches the common `r+1` ceiling exactly. -/
theorem dense_root_toy_exact : 3 = 2 + 1 ∧ 3 ≤ 2 + 1 :=
  ⟨rfl, transverse_badCount_le denseRootToy⟩

/-- Sparse/tangent toy: `r=t=2`, with one distinct nontrivial root coordinate
for each of two bad slopes. -/
def tangentRootToy : TangentRootCertificate 2 2 where
  t := 2
  roots := [0, 1]
  count_eq := by decide
  inside_tangent := by decide
  chosen_roots_nodup := by decide
  roots_in_support := by decide

/-- The tangent toy saturates its active-support injection. -/
theorem tangent_root_toy_exact :
    2 = tangentRootToy.t ∧ 2 ≤ 2 :=
  ⟨rfl, tangent_badCount_le tangentRootToy⟩

#print axioms IdentityRawScale.agreement_eq
#print axioms IdentityRawScale.numerator_eq
#print axioms IdentityRawScale.denominator_eq
#print axioms IdentityRawScale.staircaseBinom_pos_of_le
#print axioms IdentityRawScale.numerator_pos
#print axioms IdentityRawScale.denominator_pos
#print axioms IdentityRawScale.ratio_wellDefined
#print axioms staircaseBinom_succ_right_eq
#print axioms IdentityRawScale.next_numerator_step
#print axioms IdentityRawScale.adjacent_ratio_cross
#print axioms FrontiersStaircase.safe_up
#print axioms FrontiersStaircase.firstSafe_unique
#print axioms FrontiersStaircase.exists_firstSafe_of_safe
#print axioms FrontiersStaircase.threshold_exists_iff_top_safe
#print axioms FrontiersStaircase.firstSafe_spec
#print axioms FrontiersStaircase.firstSafe_spec_of_top_safe
#print axioms FrontiersStaircase.firstSafe_inGrid
#print axioms FrontiersStaircase.firstSafe_antitone_budget
#print axioms FrontiersStaircase.closedRadius_monotone_budget
#print axioms FrontiersStaircase.adjacent_isFirstSafe
#print axioms FrontiersStaircase.adjacent_identity_ratio_pins_threshold
#print axioms nodup_lt_length_deep
#print axioms transverse_root_double_count
#print axioms card_le_radius_succ_of_mul_gap_le
#print axioms transverse_badCount_le
#print axioms tangent_badCount_le
#print axioms deep_pair_badCount_le
#print axioms deep_regime_upper
#print axioms deep_range_iff_lt
#print axioms dense_root_toy_exact
#print axioms tangent_root_toy_exact

end AsymptoticSpine
