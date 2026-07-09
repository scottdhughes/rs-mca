# KB-MCA Route-D v25: free-1 high families are disjoint

Status: `PARTIAL` — family packing **PROVED** (`|F_H|≤⌊n/e⌋`, deployed ≤e);
within-family `(ι,δ)` **PROVED**; **cross-high** residual tag still **OPEN**.

## Main theorem (PROVED)

For fixed free-1 high `H`, the fully `D`-split free-1 e-sets `F_H` are
**pairwise disjoint**:

```text
r ∈ U ∈ F_H  ⇒  c0(U) = −H(r)  ⇒  U unique in F_H
```

### Size bound

```text
|F_H|  ≤  ⌊n/e⌋
```

### Deployed

```text
n          = 2097152
e          = 67472
⌊n/e⌋      = 31
⌊n/e⌋ ≤ e  = True
e·p = t·p  = 143763024447376
```

So every free-1 high family injects into `[e]` (e.g. rank by `c0`).

## Within-family pair marks (PROVED)

Free-1 CS pairs share a high. Inside `F_H`:

```text
(U,V)  ↦  (ι(U), δ),   δ = c0U − c0V,   ι = rank by c0 in F_H
```

is injective, and deployed `ι(U) ∈ [e]`.

## Payment reduction (PROVED conditional)

```text
M_pad ≤ 1  and  residual pairs lie in a single high family
    ⇒  (ι,δ) injects into e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

**OPEN gap:** `(ι,δ)` collides across different highs (toys confirm).

## Residual census (toys)

| e | j | w | floor n/e | max |F_H| | max|F|<=e? | max |U|/fiber | max pencil | (ι,δ) global inj? | cross-high coll |
|---|---|---|---:|---:|---|---:|---:|---|---:|
| 2 | 4 | 1 | 8 | 8 | False | 56 | 6 | False | 100 |
| 2 | 5 | 1 | 8 | 8 | False | 56 | 6 | False | 82 |
| 3 | 5 | 2 | 5 | 3 | True | 10 | 3 | False | 44 |
| 2 | 6 | 1 | 8 | 8 | False | 48 | 5 | False | 65 |
| 3 | 6 | 2 | 5 | 3 | True | 12 | 3 | False | 29 |
| 4 | 6 | 3 | 4 | 4 | True | 2 | 2 | False | 16 |
| 3 | 7 | 2 | 5 | 3 | True | 10 | 3 | False | 23 |
| 4 | 7 | 3 | 4 | 4 | True | 2 | 2 | False | 8 |
| 3 | 8 | 2 | 5 | 3 | True | 7 | 3 | False | 10 |
| 4 | 8 | 3 | 4 | 4 | True | 2 | 2 | False | 2 |
| 3 | 9 | 2 | 5 | 3 | True | 4 | 2 | True | 0 |
| 4 | 9 | 3 | 4 | 4 | True | 2 | 2 | True | 0 |
| 4 | 10 | 3 | 4 | 4 | True | 0 | 1 | None | 0 |

- All families disjoint; `|F_H|≤⌊n/e⌋`; within-family marks injective.
- Fiber-local `|U|` can exceed `e` (naive fiber↪[e] fails on small-w toys).
- Cross-high `(ι,δ)` collisions on 10 rows.

Census: families checked=9976 all disjoint.

## OPEN

1. Residual high separation inside e·p budget (or single residual high for A_SP)
2. `M_pad≤1` at free_core=`846161`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v25.py --check
```
