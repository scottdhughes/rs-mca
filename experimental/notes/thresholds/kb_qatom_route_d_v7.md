# KB-MCA Route-D v7: large-free B1 and residual B2 sparseness law

Status: `PARTIAL` — reformulations and structural laws **PROVED**; deployed uniqueness/budget **OPEN**.

## B1 — large-free uniqueness

### Theorem (equivalence)

```text
M_m^{max} <= 1   <=>   Phi_w is injective on m-subsets of D
```

### Theorem (room for injectivity)

```text
C(n,m) < p^w
log2(C(n,m)/p^w) ≈ -18820.25
free = m-w = 846161
```

Pigeonhole does **not** force collisions. Free-0/1 are still the only regimes with
unconditional uniqueness proofs. Large-free parameter count: fibers sit in an
affine space of dimension `846161` (bound `p^{free}`, useless for the atom).

### Deployed B1 OPEN

Prove injectivity of Phi_w on m-subsets at free=`846161` — equivalent to
`M_m^{max}<=1`. Entropy strongly suggests it; free-1 toys show avg<1 is not
by itself a proof.

## B2 — residual sparseness without going through |R|

### Theorem (affine bijection)

For fixed fiber prefix z, `u <-> b = invert_b(z,u)` is a bijection on F_p^w.

### Theorem (U_res = core-prefix image size)

Residual can-cores each determine a unique side-prefix u (side free-1 pencil).
Via the bijection,

```text
U_res(z) = |{ Phi_w(C) : C = C_can(S), S in R(z) }|
         <= N_can_prim(z)
```

with equality when residual can-cores have distinct Phi_w-prefixes.

**This is the residual-only sparseness law:** bound the **Phi_w-image of the
residual can-core family** (an m-subset prefix-image problem), not |R|.

### Why this is not circular

|R| can be up to 17 * N_can_prim. The can-core family is the compressed object.
Bounding its Phi_w-image is strictly about m-subsets selected by residual
geometry.

### Link

If B1 holds (global injectivity), then U_res = N_can_prim automatically, and
both reduce to N_can_prim <= target/17 ≈ 16166878605395467.

## Toy check

Bijection: OK. Equivalence injective <=> maxM<=1: OK.
U_res vs core-prefix image (should match):

| p | n | w | max U_res | max core-prefix image | max N_can_prim |
|---|---|---|---:|---:|---:|
| 17 | 16 | 2 | 34 | 34 | 49 |
| 17 | 16 | 3 | 5 | 5 | 5 |
| 97 | 32 | 2 | 32 | 32 | 32 |
| 97 | 32 | 3 | 7 | 7 | 7 |
| 193 | 64 | 2 | 25 | 25 | 25 |

## Open

| ID | Target |
|---|---|
| B1 | Phi_w injective on m-subsets (free=846161) |
| B2 | residual can-core Phi_w-image size <= target/17 (or t*p/17) |

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v7.py
python3 experimental/scripts/verify_kb_qatom_route_d_v7.py --check
```
