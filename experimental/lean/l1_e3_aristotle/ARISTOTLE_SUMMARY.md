# Summary of changes for run 528d145d-b2e2-4b8f-82e4-9b5c18d9e965
## Summary

I formalized the coset level-set problem in `RequestProject/Main.lean` (builds cleanly against Mathlib) and documented the mathematical status in `NOTES.md`.

### Faithful statement (verified to compile)
In `ZMod p` (`[Fact p.Prime]`) I defined:
- `cosetF p ℓ w` — the coset `{x ≠ 0 : x^ℓ = w}` (a fiber of `x ↦ x^ℓ`);
- `levelMax p ℓ Γ w` — `μ(C) = max_λ #{x ∈ C : Γ(x)=λ}`;
- `powersF p ℓ` — the nonzero ℓ-th powers indexing the cosets;
- `E3 p ℓ Γ = Σ_w (levelMax w − 2)` (truncated ℕ-subtraction realizes the positive part `(·)₊`).

The target is `theorem E3_le : E3 p ℓ Γ ≤ ℓ - 2` under exactly the stated hypotheses (`ℓ` odd prime, `ℓ ∣ p−1`, `Γ ≠ 0`, no constant term, `deg Γ ≤ ℓ−1`). I validated the statement by exhaustive computation for `(p,ℓ)=(7,3)` and `(11,5)`, including checking that dropping `Γ ≠ 0` breaks it.

### Proved with no `sorry` and only standard axioms
- `levelMax_le_card`, `card_cosetF_le`, `levelMax_le_ell`: `μ(C) ≤ |C| ≤ ℓ`.
- `card_cosetF_eq`: every nonempty coset has exactly `ℓ` elements.
- `card_powersF`: there are exactly `n = (p−1)/ℓ` cosets.

Together these verify the partition backbone the problem describes (`𝔽_p^*` splits into `(p−1)/ℓ` cosets of size `ℓ`).

### The main inequality (left as a documented `sorry`)
`E3_le` reduces to the crux the problem itself flags as open: `dim(V_1+⋯+V_K) ≥ E₃`, equivalently `dim Syz ≤ K`. I confirmed a key point requested ("flag any additional hypothesis"): the crux is NOT true for arbitrary pairwise-coprime co-fiber locators — a rank–nullity counterexample (`K=3`, `h=X−1,X−2,X²−X−1`) gives `dim Syz ≥ 6 > K`. So the single-`Γ` global structure is essential, not just coprimality. `NOTES.md` records the full reduction, the verified upper half, the counterexample, and a genuine new lead I derived: every degree-bounded syzygy of the `h_k` is also a syzygy of the polynomials `s_k = (Γ−c_k)/g_k` (obtained via an `X^ℓ`-degree separation after multiplying by `Γ`). This narrows the syzygy space but does not by itself close the crux, which remains open.

I was unable to produce a complete Lean proof of the main inequality; consistent with the honesty constraints I did not introduce axioms or a vacuous restatement, leaving the single `sorry` clearly annotated. All other declarations are fully proved. Files: `RequestProject/Main.lean`, `NOTES.md`.