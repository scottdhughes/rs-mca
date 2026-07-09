# KB-MCA Route-D v51: U2e PROVED (char ≠ 2)

Status: **U2e PROVED** for all e≥2 in char ≠ 2; hence
`H_*^pre(t,e) ≤ binom(t,2e)` **unconditional**. Full deployed window still OPEN.

## Theorem U2e

Let `F` be a field of characteristic ≠ 2, `e≥2`, and `W ⊂ F` a set of `2e`
distinct elements. There is **at most one** unordered bipartition
`W = U ⊔ V` with `|U|=|V|=e` such that monic `f_U, f_V` share coefficients of
`X^{e−1},…,X^1` (free-1 / equal monic high).

### Proof

1. Free-1 ⇔ `f_U − f_V` is constant, both monic of degree `e`.
2. Write `f_U = R+α`, `f_V = R+β` with `R` monic degree `e` and constant term
   of `R` equal to 0. Then
   ```text
   R² + s R + p = P_W,   s=α+β, p=αβ,   P_W = ∏_{w∈W}(X−w).
   ```
3. **Triangular recovery (char ≠ 2).** Coefficients of `X^{2e−1},…,X^{e+1}`
   in `R²` form a triangular system with diagonal factor `2` in the unknowns
   `r_{e−1},…,r_1`. Hence `R` is uniquely determined by `P_W`.
4. Coefficient of `X^e` fixes `s` uniquely; degrees `e−1..1` are existence
   constraints; degree 0 fixes `p`.
5. `α,β` are the ≤2 roots of `T² − s T + p`. The unordered pair `{R+α,R+β}`
   is unique, so the root-set bipartition is unique.
6. `α=β` forces `f_U=f_V`, impossible for a partition of `2e` distinct points.

Deployed KoalaBear `p = 2^31 − 2^24 + 1` is an odd prime, so char ≠ 2.

## Corollary (was v50 conditional)

```text
H_*^pre(t,e)  ≤  binom(t, 2e)
```

Each multipad high injects into its free-1 pair-cover `W = U∪V` (size `2e`)
by U2e uniqueness.

## Arithmetic residual gate (deployed)

| s | binom(2e+s, s) | ≤ H2? |
|---:|---:|---|
| 2 | 9105143985 | yes |
| 3 | 409570621781265 | **no** |

```text
t ≤ 2e+2  ⇒  H_*^pre(t,e) ≤ H2
```

e=2: already `H_*^pre(t,2) ≤ p ≤ H2` for all t (v48/v50).

## Residual card path

```text
pure-untyped coext residual with min(C) ≤ 2e+2
  ⇒  H_*^pre ≤ H2  ⇒  residual free-1 card (v45–v47)
```

OR improve large-t bound using roots-of-unity / GP structure.

## Toys

| p | e | t | nH | C(t,2e) | multi bip | R-verified free1 |
|---|---:|---:|---:|---:|---:|---:|
| 17 | 4 | 16 | 89 | 12870 | 0 | 0 |
| 31 | 4 | 16 | 24 | 12870 | 0 | 0 |
| 61 | 4 | 16 | 1 | 12870 | 0 | 0 |
| 73 | 4 | 16 | 6 | 12870 | 0 | 0 |
| 101 | 4 | 16 | 0 | 12870 | 0 | 0 |
| 17 | 4 | 15 | 53 | 6435 | 0 | 0 |
| 31 | 4 | 15 | 11 | 6435 | 0 | 0 |
| 61 | 4 | 15 | 0 | 6435 | 0 | 0 |
| 73 | 4 | 15 | 3 | 6435 | 0 | 0 |
| 101 | 4 | 15 | 0 | 6435 | 0 | 0 |
| 17 | 4 | 14 | 30 | 3003 | 0 | 30 |
| 31 | 4 | 14 | 4 | 3003 | 0 | 4 |
| 61 | 4 | 14 | 0 | 3003 | 0 | 0 |
| 73 | 4 | 14 | 1 | 3003 | 0 | 1 |
| 101 | 4 | 14 | 0 | 3003 | 0 | 0 |
| 17 | 4 | 13 | 13 | 1287 | 0 | 13 |

Census: rows=120; all bip unique; all nH≤C(t,2e);
free1 R-reconstructions verified=453.

## OPEN

1. Force residual `t = min(C) ≤ 2e+2`, **or**
2. Bound `H_*^pre(t,e)` for `t ≤ n'=1183520` with `k=⌊t/e⌋≤17`
   tighter than `binom(t,2e)`.
3. `A_SP ≤ t·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v51.py --check
```
