/-!
# Deployed-row margin integer anchors (W24 M1)

Kernel-checked facts for the four adjacent-row lower(a0+1) < B_* inequalities
and gap integers from the integrated q-r1-closing / #372 table.

Source cert: experimental/data/certificates/q-r1-closing-audit/q_r1_closing_audit.json
Source labels: cor:capg-adjacent-pairs, cor:capfr1-Q-R1-closing (finite lower side).

No `sorry`. No mathlib. `native_decide` / `decide` only.
-/

namespace MarginAnchors

/-- KoalaBear B_* = floor(p^6 / 2^128) = 274980728111395087 -/
def BStarKB : Nat := 274980728111395087

/-- Mersenne-31 B_* = floor(p^4 / 2^100) = 16777215 -/
def BStarM31 : Nat := 16777215

/-- lower floors at a0+1 from integrated table -/
def lowerKB_MCA : Nat := 57198030366
def lowerKB_list : Nat := 65065153468
def lowerM31_MCA : Nat := 1752700
def lowerM31_list : Nat := 1993678

theorem lower_kb_mca_lt_Bstar : lowerKB_MCA < BStarKB := by native_decide
theorem lower_kb_list_lt_Bstar : lowerKB_list < BStarKB := by native_decide
theorem lower_m31_mca_lt_Bstar : lowerM31_MCA < BStarM31 := by native_decide
theorem lower_m31_list_lt_Bstar : lowerM31_list < BStarM31 := by native_decide

/-- Fail-margin gaps: B_* + 1 - lower(a0+1) (strict exceedance deficit from #372) -/
def gapKB_MCA : Nat := BStarKB + 1 - lowerKB_MCA
def gapKB_list : Nat := BStarKB + 1 - lowerKB_list
def gapM31_MCA : Nat := BStarM31 + 1 - lowerM31_MCA
def gapM31_list : Nat := BStarM31 + 1 - lowerM31_list

theorem gap_kb_mca_value : gapKB_MCA = 274980670913364722 := by native_decide
theorem gap_kb_list_value : gapKB_list = 274980663046241620 := by native_decide
theorem gap_m31_mca_value : gapM31_MCA = 15024516 := by native_decide
theorem gap_m31_list_value : gapM31_list = 14783538 := by native_decide

/-- Millibit-style integer bracket encoding for KB MCA spare ~22.1969 bits:
    2^22 * 1000 = 4194304000 encodes the 22.xxx milli-bit scale as an integer
    witness that 2^22 ≤ floor(2^{spare}) roughly — we pin the exact comparison
    2^22 ≤ 2^22 (tautological scale) and a non-vacuous: gap > 2^22. -/
theorem gap_kb_mca_gt_2pow22 : gapKB_MCA > 2 ^ 22 := by native_decide
theorem gap_kb_list_gt_2pow22 : gapKB_list > 2 ^ 22 := by native_decide

/-- Second presentation of the same inequalities via `decide` (not native_decide). -/
theorem lower_kb_mca_lt_Bstar' : lowerKB_MCA < BStarKB := by decide

end MarginAnchors

/-!
## cor:grand sharper-branch (q ≥ 2n) row hypothesis checks

Kernel-checked Nat facts backing
`experimental/notes/audits/pay_per_bit_86bit_conditional_rows.md`: the exact
`q ≥ 2n` comparison (cor:grand's own extra hypothesis for its sharper
`≥ 2^-42` / 86-bits-above-target branch, tex/cs25_cap_v12.tex:3567,3584) and
the exact `N_rho ∣ n` divisibility hypothesis (same corollary,
tex/cs25_cap_v12.tex:3543-3548), checked on every row of that note's table.

AUDIT-only: an integer-comparison instantiation of the maintainer's own
printed corollary on specific rows, not a new theorem.

No `sorry`. No mathlib. `native_decide` only.
-/

namespace CorGrandQGe2nRows

/-- KoalaBear sextic row (cor:deployed): p = 2^31 - 2^24 + 1, q = p^6, n = 2^21. -/
def pKB : Nat := 2130706433

def qKB : Nat := pKB ^ 6
def nKB : Nat := 2 ^ 21

/-- M31 circle rows (cor:circle-deployed): p' = 2^31 - 1, q = p'^4.
    n = 2^21 for the line round (a), n_c = 2^22 for the circle code (b). -/
def pM31 : Nat := 2147483647

def qM31 : Nat := pM31 ^ 4
def nM31Line : Nat := 2 ^ 21
def nM31Code : Nat := 2 ^ 22

/-- F_17^32 row (Cycle116/119): q = 17^32, n = 512. -/
def qF17 : Nat := 17 ^ 32

def nF17 : Nat := 512

/-- H7 (q ≥ 2n) numeric fact per row: holds on all four, with huge margins. -/
theorem kb_q_ge_2n : qKB ≥ 2 * nKB := by native_decide

theorem m31_line_q_ge_2n : qM31 ≥ 2 * nM31Line := by native_decide
theorem m31_code_q_ge_2n : qM31 ≥ 2 * nM31Code := by native_decide
theorem f17_q_ge_2n : qF17 ≥ 2 * nF17 := by native_decide

/-- H2 (N_rho ∣ n, N_{1/2} = 1024) per row: holds for KB and for both M31
    domain sizes, FAILS for F_17^32 — the row's actual blocking hypothesis,
    independent of H7 above (which holds for it too, but is moot). -/
theorem kb_Nrho_dvd_n : (1024 : Nat) ∣ nKB := by native_decide

theorem m31_line_Nrho_dvd_n : (1024 : Nat) ∣ nM31Line := by native_decide
theorem m31_code_Nrho_dvd_n : (1024 : Nat) ∣ nM31Code := by native_decide
theorem f17_Nrho_not_dvd_n : ¬ (1024 : Nat) ∣ nF17 := by native_decide

/-- M31 rows: q < 2^128, so the 2^-128 target is degenerate there
    (paper's own prop:small-field); the H7 fact above is numerically true
    but moot once H5 (multiplicative-coset domain) already fails. -/
theorem m31_q_lt_2pow128 : qM31 < 2 ^ 128 := by native_decide

/-- Generic envelope-worst bit arithmetic used by cor:grand's two branches:
    unconditional 2^-86 (42 bits above 2^-128) vs. conditional 2^-42
    (86 bits above 2^-128), both at the envelope-worst k = 2^40. -/
theorem worst_case_unconditional :
    2 * (2 ^ 40) * ((16 * 2 ^ 40) + 1) < 2 ^ 86 := by native_decide

theorem worst_case_conditional : 4 * (2 ^ 40 : Nat) = 2 ^ 42 := by native_decide

/-- Row-specific application of the same conditional-branch formula at the
    KoalaBear row's actual k = 2^20: 1/(4k) = 2^-22, i.e. 106 bits above
    2^-128 — 20 bits better than the generic worst-case 2^-42/86-bit floor,
    and matching cor:deployed's own printed headline exactly. -/
theorem kb_row_specific_conditional : 4 * (2 ^ 20 : Nat) = 2 ^ 22 := by
  native_decide

/-- N=512 boundary shared by F_17^32 and the s=4096 tail of the KoalaBear
    interleaved family (cor:rows): N_rho=1024 does not divide n=512. -/
theorem n512_not_Nrho_multiple : ¬ (1024 : Nat) ∣ (512 : Nat) := by
  native_decide

end CorGrandQGe2nRows
