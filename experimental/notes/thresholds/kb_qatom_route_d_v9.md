# KB-MCA Route-D v9: M_m structural law (post-uniqueness)

Status: `PARTIAL` — intersection / tight-pair / tight-clique / padding reduction / anticode
**PROVED**; atom-scale upper bound on `M_m` **OPEN** (and tight-clique is **not** one).

## Snapshot

| Quantity | Deployed value | Role |
|---|---:|---|
| Coset lower bound `k_coset` | 10 | Achieved (v8, e0=2^17) |
| Tight-clique cap `k_tight` | 18 | Upper for *pairwise-tight* subfamilies only |
| Anticode log2 | 1693127.62 | Proved upper, atom-useless |
| Atom-scale `M_m` upper | OPEN | Blocks setting small K |

## Theorems

### I — Intersection law (PROVED)

If `S ≠ T` and `Phi_w(S)=Phi_w(T)`, then

```text
|S ∩ T|  ≤  m − w − 1  =  free − 1
```

Proof: `deg(Λ_S − Λ_T) ≤ m−w−1` and `S ∩ T` sits in the roots of that difference.

### II — Tight pairs are free-1 CS pads (PROVED)

Equality `|S ∩ T| = m−w−1` holds iff `R = S ∩ T` has size `m−(w+1)` and
`U = S\T`, `V = T\S` form a free-1 constant-shift pair of `(w+1)`-sets:

```text
Λ_U − Λ_V  =  c  ∈  F_p^×,     Λ_S − Λ_T  =  c Λ_R
```

### III — Tight-clique bound (PROVED)

Any *pairwise-tight* subfamily of a fiber has size

```text
|F|  ≤  k_tight  =  1 + floor((n−m)/(w+1))  =  18
```

**Not** an upper bound on full `M_m`: fibers may use non-tight pairs.

### IV — Padding reduction (PROVED)

A `Phi_w` fiber of `e0`-sets with `k` pairwise-disjoint members pads with common `R`
(`|R|=m−e0`) to a size-`k` fiber of m-sets, provided room `n − k e0 ≥ m − e0`.

Special case e0 | n pure cosets: v8, `M_m ≥ 10`.

### V — Anticode (PROVED, weak)

```text
M_m^<built-in function max>  ≤  C(n, free) / C(m, free)
log2(bound) ≈ 1693127.62   (≫ 53.84 atom bits)
```

### VI — Tight-clique ≠ fiber upper (PROVED by toy)

On `(p,n,m,w) = (17,16,6,2)`: `k_tight = 4`, coset `k_max = 3`, measured `M_m = 32`.

## Toy table (intersection law + gap)

| p | n | m | w | Mm | k_tight | k_coset | Mm>k_tight | max∩ / cap |
|---|---|---|---|---:|---:|---:|---|---|
| 17 | 16 | 6 | 2 | 32 | 4 | 3 | True | 3/3 |
| 17 | 16 | 8 | 2 | 54 | 3 | 3 | True | 5/5 |
| 17 | 16 | 6 | 3 | 5 | 3 | 3 | True | 2/2 |
| 17 | 16 | 8 | 4 | 2 | 2 | 2 | False | 2/3 |
| 17 | 16 | 5 | 2 | 17 | 4 | 3 | True | 2/2 |
| 17 | 16 | 4 | 2 | 8 | 5 | 4 | True | 1/1 |
| 17 | 16 | 8 | 6 | 2 | 2 | 2 | False | 0/1 |
| 17 | 16 | 10 | 4 | 2 | 2 | 1 | False | 4/5 |

All rows: intersection law holds. Several rows: `Mm > k_tight`.

## Budgets if one assumes `M_m ≤ K`

| Assumed K | U_res atom budget | log2 |
|---:|---:|---:|
| 10 (coset lower only) | 1616687860539546 | 50.52 |
| 18 (tight-clique, unjustified for full fiber) | 898159922521970 | 49.67 |

## Impact

| Item | Status |
|---|---|
| B1 uniqueness `M_m ≤ 1` | REFUTED (v8) |
| `M_m ≥ 10` | PROVED (v8) |
| `M_m ≤ 18` via tight-clique | **FALSE hope** — only tight subfamilies |
| Atom-scale `M_m` upper | OPEN |
| B2 residual can-core `Phi_w`-image | OPEN (still the wall) |

## Next real math

1. Atom-scale upper bound on full `M_m` that accounts for non-tight pairs, **or**
2. Prove residual (post first-match) fibers have no non-tight pairs / size ≤ 1, **or**
3. Bound residual can-core `Phi_w`-image (B2) without any small-`M_m` premise.

Do not re-prove `M_m ≤ 1`. Do not claim `M_m ≤ k_tight` for full fibers.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v9.py
python3 experimental/scripts/verify_kb_qatom_route_d_v9.py --check
```
