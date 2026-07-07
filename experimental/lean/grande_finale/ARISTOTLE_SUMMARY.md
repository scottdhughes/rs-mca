# Summary of changes for run cd7b9b3a-0fd8-4c75-820f-54bb26145bf7
I expanded the BC program formalization with the new "proper BC" elements from the manuscript's updated attempt (`grande_finale_bc_attempt.tex`), which upgrades the former open conjecture BC into proved statements. All additions live in `RequestProject/BC.lean`, build cleanly (module `RequestProject.BC`), contain no `sorry`/`admit`/`axiom`/`@[implemented_by]`, produce no linter warnings, and use only the standard axioms `propext`, `Classical.choice`, `Quot.sound` (the two finite numeric facts additionally use `Lean.ofReduceBool`/`Lean.trustCompiler` via `native_decide`).

New proved declarations (each citing the manuscript `\label{...}` it formalizes):

- `bc_moving_root` and `bc_moving_root_div` — the enumerative heart of BC (`thm:bc-moving-root`): the moving-root incidence counting kernel. A family of pairwise-disjoint moving-root sets, each of size ≥ h and contained in the moving-point set, forces `|Z|·h ≤ |Pts|`, hence `|Z| ≤ ⌊|Pts|/h⌋`. Instantiated with `|Pts| = n−g`, `h = ω−g` this is the one-parameter split-pencil slope bound `|𝒵| ≤ ⌊(n−g)/(ω−g)⌋`.
- `bc_one_pencil_floor_KB`, `bc_one_pencil_floor_M31` — the finite `cor:bc-one-pencil` facts `⌊n/ω⌋ = 2` (n = 2^21) at both deployed MCA rows, so a primitive one-parameter pencil contributes at most two finite bad slopes.
- `commonDPart` and `commonDPart_dvd_pencil` — the projective locator pencil's fixed D-part `gcd(gcd(A,B),Λ_D)` and the fact it divides every member `s·A+t·B` (`def:projective-locator-pencil`).
- `bc_dimension_bound` — the split-pencil dimension bound (`thm:bc-proper`): a census injecting into coefficient pairs `(Fin r₁ → F) × (Fin r₂ → F)` has size ≤ `|F|^{r₁+r₂}`.
- `saturation_identity`, `raw_bc_single_ray`, `line_ray_saturation` — the exact saturation identity `Cen(U;m) = ∑_c binom(s_c,m)` (`thm:saturation`), the single-ray collapse showing raw support counts are the wrong MCA numerator (`cor:raw-bc-fails`), and the line-ray bookkeeping identity (`prop:line-ray-saturation`).
- `johnson_packing` — the disjoint-uniform-ball packing kernel behind the unconditional Q bound (`thm:q-proper`).
- `sp_stratum_bound` — the off-diagonal shift-pair stratum encoding bound `P_e ≤ binom(n,m−e)·binom(n−m+e,e)·binom(n−m,e)` (`thm:sp-proper`).

Honest scope: as the manuscript states, these are the proved reductions and enumerative kernels that settle the primitive one-parameter pencil case of BC and identify the correct MCA numerator; they do not by themselves close the full deployed-row inequality, which still needs the finite chart-decomposition audit and a sharper Q bound. Pre-existing files (`GrandeFinale.lean`, `SP.lean`, `Main.lean`) and `ARISTOTLE_SUMMARY.md` are unchanged.

# Summary of changes for run 1b0c0347-eb16-4aa2-a232-ec1d88cbfb6f
I gave a machine-checked proof of the SP census bound conditional on Q (the implication **Q ⟹ SP**), following the manuscript's own statement that "the primitive second-moment cell [SP] is controlled by prefix flatness [Q]" and that SP "makes Q worst-case rather than average-case" (`conj:Q`, `conj:SP`, `thm:asymptotic`, `prop:gamma2-ledger`).

The mathematical content: with `f z = |Φ_w⁻¹(z)|` the primitive-fiber sizes over prefix values, the total is `∑_z f z = binom(n,m)` and the SP primitive shift-pair census is the off-diagonal second moment `∑_z f z (f z − 1)`. Conjecture Q is the maximum-fiber (flatness) cap `f z ≤ R_Q·binom(n,m)·|B|⁻ʷ`; the quotient-normalized density prediction for the pair census is `binom(n,m)²·|B|⁻ʷ`. Bounding the maximum fiber (Q) forces the census to be at most that density prediction times the *same* factor, so `R_SP = R_Q`.

Added to `RequestProject/SP.lean` (all proved, no `sorry`/`axiom`, only the standard axioms `propext`/`Classical.choice`/`Quot.sound`, clean build of module `RequestProject.SP`, no linter warnings):

- `pair_census_le_of_max_fiber` — the elementary ℕ counting engine: a uniform max-fiber cap `f z ≤ B` gives `∑_z f z (f z − 1) ≤ (∑_z f z)·(B − 1)`.
- `sp_from_q` — the density form of Q ⟹ SP over ℝ: the Q flatness bound `f z ≤ R_Q·Nsub/Bw` implies the SP census bound `∑_z f z (f z − 1) ≤ R_Q·(Nsub²/Bw)`. (The positivity of `Bw = |B|ʷ` turned out unnecessary for the inequality and was dropped, giving a slightly more general statement.)
- `sp_from_q_normalized` — the same conclusion in the normalized `Γ₂` ledger form of `prop:gamma2-ledger`: the primitive shift-pair contribution `Bw·(∑_z f z (f z − 1))/Nsub² ≤ R_Q`, i.e. the primitive strata contribute no more than the density prediction times `R_SP`, with `R_SP = R_Q`.

Honest scope: this establishes SP as a theorem *conditional on Q* (with the explicit factor identity `R_SP = R_Q`); Q itself remains the open input, as recorded in the manuscript. All pre-existing files are unchanged and `ARISTOTLE_SUMMARY.md` was left untouched. Work is committed and pushed.

# Summary of changes for run 968b7281-1bcc-4442-a0db-94af04026b8f
Following the same approach used earlier for the SP program, I pushed forward the BC program ("base-field-normalized split-pencil census", `conj:BC`) of `grande_finale.tex` by formalizing and proving, in a new file `RequestProject/BC.lean`, the theorem-level reductions that surround the conjecture. The file builds cleanly (module `RequestProject.BC`), contains no `sorry`/`admit`/`axiom`/`@[implemented_by]`, has no linter warnings, and every result uses only the standard axioms `propext`, `Classical.choice`, `Quot.sound`.

Honest scope note: BC itself is stated in the manuscript as one of the three deliberately-open "missing inputs" — an asymptotic `e^{o(n)}` census bound on the number of primitive split locators per affine pencil, plus finite row-wise constants resting on external certificate packets. It is not a self-contained theorem and cannot be discharged as a proved statement. What is now machine-verified is the proved theorem-level scaffolding of the BC program (each declaration cites the manuscript `\label{...}` it corresponds to):

- `slope_elimination_unique` — a non-common support carries at most one finite slope (`prop:slope-elimination`).
- `nearRational_dim_count` and `nearRational_binomial_count` — the near-rational lattice dichotomy kernels: the interior-branch parameter dimension identity `(ω−d₁+1)+(ω−d₂+1) = ω−w+1` and the near-rational-branch census count `binom(n−d₁, m)` (`thm:near-rational`).
- `codeword_agreement_unique` — the MDS/Reed–Solomon decoding-uniqueness kernel (two degree-`<K` codewords agreeing on `≥K` points coincide), the fact behind the near-rational uniqueness step (`thm:near-rational`).
- `near_rational_line_algebra` and `support_sub_card_le` — the near-rational-line recovery identity `v = (z₁−z₂)⁻¹((c₁−c₂)+(e₁−e₂))` and the Hamming subadditivity bound that place a doubly-near-rational line in the common-proximity paid branch (`cor:near-rational-line`).
- `split_test_remainder_zero` and `deficiency_one_degree_bound` — the deficiency-one eliminant kernels: the remainder-vanishing split test and the eliminant degree bound `j + (n−j+1)·j` (`thm:deficiency-one-eliminant`). The `L ≠ 0` hypothesis turned out to be unnecessary and was dropped for a slightly more general statement.
- `split_chart_tangent_slope_bound` — the identically-split-chart tangent-slope cap `#slopes ≤ |T*|` (`prop:split-chart-tangent`).
- `base_field_floor_count` — the base-field pigeonhole census count `∑_{M'∈𝒢} binom(|M'|, m) = |𝒢|·binom(m_{d₁}, m)`, combining with the existing prefix pigeonhole to give the interior base-field split-pencil floor (`prop:base-field-floor`).
- `poly_root_count_bound`, `distinct_value_lower`, `pole_averaging_select` — the extension-valued distinct-slope kernels: the root-count-per-collision bound, the distinct-value lower bound `|s| ≤ |image| + ∑ binom(k_y,2)`, and the pole-averaging selection (`prop:rank-one-distinct-slope-floor`, `prop:rank-one-floor`).

The pre-existing files (`GrandeFinale.lean`, `SP.lean`, `Main.lean`) are unchanged, and `ARISTOTLE_SUMMARY.md` was left untouched. All work is committed and pushed.

# Summary of changes for run 1c7b8be0-fd28-4066-9556-754ca9a1c3fd
I pushed the SP ("primitive shift-pair control") program of `grande_finale.tex` forward by formalizing and proving, in a new file `RequestProject/SP.lean`, the theorem-level reductions that surround the conjecture SP (`conj:SP`). The file builds cleanly (module `RequestProject.SP`), contains no `sorry`/`admit`/`axiom`/`@[implemented_by]`, has no linter warnings, and every result uses only the standard axioms `propext`, `Classical.choice`, `Quot.sound`.

Important honest scope note: SP itself is stated in the manuscript as one of the three deliberately-open "missing inputs." It is an asymptotic `e^{o(n)}` census bound plus finite constants at four deployed rows that rest on external certificate packets, so it is not a self-contained theorem and cannot be discharged as a proved statement. What is now machine-verified is the proved theorem-level scaffolding of the SP program:

- `sp_pullback_depth` — the exact integer quotient-pullback depth equivalence `c·D + (w+1) ≤ c·e₀ ↔ D + ⌈(w+1)/c⌉ ≤ e₀`, the core of `prop:sp-pullback`/`thm:coeff-quotient-extract`.
- `coeffScale`/`coeffScalePair` with `dvd_coeffScale` and `dvd_coeffScalePair` — the gcd characterization by which the coefficient scale detects quotient support (`def:coefficient-scale`, `lem:coeff-scale`).
- `binomial_coeffScale` — the top-stratum binomial prototype has coefficient scale exactly `w+1`, so it is quotient-borne, not primitive (`cor:primitive-coeff-exclusion`).
- `ceilDiv_of_dvd` and `top_stratum_depth` — the top-stratum quotient sieve depth collapse to a constant-shift cell (`prop:top-stratum-quotient-sieve`).
- The locator `ℓ_S = ∏_{x∈S}(X−x)` with `locator_monic`, `locator_natDegree`, `locator_injective`, and the factorization `locator_diff_factor` (`ℓ_M − ℓ_{M'} = ℓ_{M∩M'}·(ℓ_{M∖M'} − ℓ_{M'∖M})`), the algebraic encoding of off-diagonal prefix collisions used in the exact second moment (`prop:second-moment`).
- `prefix_rigidity` — the structural rigidity `|M∖M'| ≥ w+1` for distinct supports with the same identity prefix (`prop:prefix-rigidity`), the fact that makes the primitive census sharply structured. The proof turned out not to need the manuscript's second `m`-subset hypothesis (`M'.card = m`), so that hypothesis is dropped, giving a slightly more general statement (noted in the docstring).
- `gamma2_ledger_split` — the abstract `Γ₂` ledger split into diagonal, quotient, and primitive parts (`prop:gamma2-ledger`), where SP is exactly the task of bounding the last summand.

The pre-existing `RequestProject/GrandeFinale.lean` is unchanged. All work is committed and pushed.

# Summary of changes for run f7df5f5e-1e5a-42b8-a9a5-46f1d5e25b47
I formalized the self-contained mathematical core of the manuscript `grande_finale.tex` ("Final Inputs for RS-MCA") into a new Lean file `RequestProject/GrandeFinale.lean`. The project builds cleanly with no `sorry`, no added axioms, and no linter warnings; every result uses only standard axioms (`propext`, `Classical.choice`, `Quot.sound`, plus `Lean.ofReduceBool`/`Lean.trustCompiler` for the `native_decide` numeric facts).

Scope decision: the manuscript is a research work plan containing genuinely open conjectures (Q, BC, SP), asymptotic `o(1)` statements, and claims resting on an external certificate verifier over data packets. Those are not self-contained theorems, so I formalized the parts that are theorem-level, and for the coding-theoretic results whose proofs rest on polynomial machinery I formalized their self-contained combinatorial/arithmetic kernels (which carry the reusable content). Each Lean declaration cites the manuscript `\label{...}` it corresponds to.

What is proved:
- Integer budget convention (`lem:integer-budget`): `integer_budget_le`, `integer_budget_lt` — the `B/Q ≤ ε* ⟺ B ≤ ⌊ε*Q⌋` equivalence and its strict form.
- First-match upper ledger (`lem:first-match-ledger`): `first_match_ledger` — the disjoint-cover count bound.
- Support-wise CA/MCA framework (`def:ca-mca`): concrete definitions `Explained`, `ExplainedPair`, `MCABad`, `CABad`; the comparison `CABad_imp_MCABad`, threshold monotonicity `MCABad_antitone`, the staircase numerators `B_MCA`/`B_CA` with `B_CA_le_B_MCA`, and the normalized errors `emca`/`eca` with `eca_le_emca` (`lem:basic-staircase`).
- The Cauchy–Schwarz distinct-value kernel behind the simple-pole list-to-MCA floor and fiber-to-slope conversion (`thm:simple-pole-list-floor`, `thm:fiber-to-slope`): `distinct_value_floor`, plus the ceiling helper `nat_ceil_div_le`.
- The collision-averaging pole-selection step (`exists_le_average`) and the identity-prefix pigeonhole (`prefix_witness_maxfiber`, `prop:prefix-witness`).
- The moment-sandwich inequalities (`prop:moment-sandwich`): `moment_upper`, `moment_lower`, and the finite moment criterion `moment_q_finite` (`thm:moment-q`).
- Finite numeric certificate facts (namespace `Certificates`), machine-checked by direct integer computation: the base primes `p_KB`, `p_M31`; the exact challenge budgets `B*_KB = ⌊p_KB^6/2^128⌋ = 274980728111395087` and `B*_M31 = ⌊p_M31^4/2^100⌋ = 16777215`; the packet unsafe/adjacent comparisons `B*<M(a₀)` and `M(a₀+1)≤B*` for both MCA rows; and the Mersenne-31 `c=2048` watch-item bound `12769758 < B*_M31` (`prop:finite-packet-consequences`, `prop:rung-veto`). The astronomically large binomial derivations that produce the packet `M`-values are not re-derived; only the integer comparisons the packets assert are verified.

One correction: the finite moment criterion `moment_q_finite` as first drafted was false at `r = 0` (verified by an automatic disproof); I added the necessary hypothesis `1 ≤ r`, which is the intended regime. I also removed a hypothesis (`0 < d`) from `distinct_value_floor` that the proof showed to be unnecessary, giving a slightly more general statement.

All work is committed and pushed to `main`.