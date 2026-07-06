# L1 identity-scale ceiling `E_3 <= ell-2`: status, CAP25 v13 connection, and route map

- **Status:** PROVED (upper half) + REDUCTION + banked route-eliminations. The headline
  `E_3 <= ell-2` is OPEN — and confirmed to be the same finite max-fiber problem CAP25 v13 leaves
  open. Index note for the `l1_e3_*` contribution set.
- **Agent/model:** Claude Opus 4.8 (verifications cross-checked on 4 CAS engines). 2026-07-06.

## The problem (identity scale `c=1`)

`ell` odd prime, `ell | p-1`, `Gamma` constant-free with `deg <= ell-1`, `Gamma != 0`. Cosets of
`mu_ell` (fibers of `x -> x^ell`); `mu(C) = max_lambda #{x in C : Gamma(x)=lambda}`;
`E_3 = sum_C (mu(C)-2)_+`. **Ceiling: `E_3 <= ell-2`** (sharp; NUMERIC-tight in the frontier note).

## What is PROVED here (cross-checked on Sage / PARI / FLINT / Macaulay2)

With excess fibers `F_k` (`mu_k>=3`), `g_k` (fiber locator), `h_k=(X^ell-w_k)/g_k` (co-fiber
locator), `V_k = h_k * F_p[X]_{<=mu_k-2}`, `Syz = {(q_k): sum h_k q_k=0, deg q_k<=mu_k-2}`:

- **Upper half:** `dim(sum V_k) <= ell-2`, via `L(A)=[X^{ell-1}](A*Gamma)` (every `V_k subset ker L`);
  elementary, verified from scratch on FLINT (`verify_l1_e3_flint_crosscheck.py`) and M2
  (`m2_syz_crosscheck.m2`). See `l1_e3_subspace_upper_bound.md`.
- **Reduction:** `E_3 <= ell-2  <=>  dim(sum V_k) >= E_3  <=>  dim Syz <= K`. So the whole ceiling
  reduces to the rank statement **`dim Syz <= K`** (the `K>=3` chart is the sole open crux; `K=2` proved).
- **Realizability is essential:** for arbitrary pairwise-coprime `h_k`, `dim Syz` can exceed `K`
  unboundedly; the single-`Gamma` structure is the operative hypothesis.

## Connection to CAP25 v13 (Chojecki, `experimental/cap25_cap_v13_raw.pdf`)

`E_3 <= ell-2` **is** the paper's *identity-scale collision problem* / *finite max-fiber
inequality* (§16, Remark 16.10, Prop 16.17). The paper independently reaches our conclusion:
character maxima face a **`sqrt(p)` barrier** (Remark 16.10), so second-moment / character-sum
methods give only the asymptotic frontier up to a `poly(n)` / `O(log n)` reserve, and the finite
adjacent pair (deployed margins 22.2/22.0/3.3/3.1 bits) is **left open** ("an unspecified
polynomial factor can exceed those margins"). Our reduction to `dim Syz <= K` is the exact rank
(not analytic) form the paper names as the remaining target.

## Ruled-out routes (each verified; failures preserved)

1. **Additive lacunary / Ball Thm 1.9:** does not transfer — our `x->x^ell` is Kummer (`ell|p-1`),
   not Frobenius (`p^e`); `R(W,c)` has degree `<< p` (`redei_RWc_structure.sage`). The correct home
   is the **cyclotomic-class / Carlitz-McConnel** rigidity theory (Xiong-Yip et al.);
   `m*(ell)=(ell+3)/2` = the classical `(q+3)/2` direction bound. See `l1_e3_lacunary_directions_connection.md`.
2. **Character sums (pair-cap):** `sum_C sum_c N(N-1) <= (ell-1)(ell-2)` (verified) gives only
   `E_3 <= (ell-1)(ell-2)/6` — not sharp (matches CAP25's `sqrt(p)` barrier). `l1_e3_charsum_paircap.md`.
3. **Pencil / `s_k` conditions:** `X^ell - t*Gamma - b_k(t) = g_k(h_k-t s_k)` is exact (the `F_k` are
   common level sets of the pencil `phi=(X^ell,Gamma)`), but `sum s_k q_k=0` is a DEPENDENT
   consequence of `sum h_k q_k=0` and does not cut `Syz` (`pencil_cut_test.sage`). `l1_e3_aristotle_run.md`.
4. **Leading-coeff / `dim U` / evaluation-map injectivity:** circular — `dim U = 2` is invariant, and
   `(q_k)->(q_k(alpha_k))` is injective for *generic* anchors (reflects `dim Syz=K`, does not prove it).

## Aristotle

Two obligations submitted (`aristotle_e3_obligation{,_v2}.md`); the run produced a faithful Lean
formalization (`../../lean/l1_e3_aristotle/`, backbone proved, main inequality an annotated `sorry`)
and independently reproduced the upper half + a verified pencil identity. v2 (sharpened) is running.

## Honest bottom line

`E_3 <= ell-2` is a genuinely open, named problem in the current CAP25 spine. This contribution
supplies the **proved upper half**, the **exact rank reduction** (`dim Syz <= K`), the correct
**cyclotomic-directions framing**, a 4-engine cross-check, a Lean formalization, and four verified
route-eliminations — narrowing the finite max-fiber problem to a single `K>=3` rank statement.
