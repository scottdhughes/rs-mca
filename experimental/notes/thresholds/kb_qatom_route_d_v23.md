# KB-MCA Route-D v23: free_core=1 multipads = free-1 CS cores

Status: `PARTIAL` — free_core=1 stratum **PROVED** (free-1 CS cores + joint
avoidance); deployed free_core=846161 still **OPEN**.

## free_core stratification (PROVED)

```text
free_core = m_c − w = j − 2w − 1
```

| free_core | multipad geometry |
|---:|---|
| ≤ 0 | M_pad ≤ 1 (Phi_w determines monic core) |
| = 1 | free-1 CS core cliques + joint avoid (U,V) |
| ≥ 2 | depth-w multi-mates, deg(diff) ≤ free_core−1 + joint avoid |

Deployed:

```text
m_c         = 913632
free_core   = 846161   (stratum ≥ 2)
e·p = t·p   = 143763024447376
```

## Main theorem (PROVED): free_core = 1

If `free_core = 1` and `C ≠ C'` are multipad cores, then `Λ_C, Λ_{C'}` form a
**free-1 CS pair** of monic degree-`m_c` locators (same free-1 high, distinct
constants), and both jointly avoid the recovered sides `(U,V)`.

Proof: `m_c = w+1` ⇒ `Phi_w` fixes every non-leading non-constant coeff.

## Side-key recovery + joint avoidance (PROVED)

```text
φ = (high, c0U, c0V)  →  unique fully-split free-1 CS pair (U,V)
M_pad ≥ 2  ⇒  U,V ⊆ D \ (C ∪ C')   for every multipad core pair
```

Multipad control ≤ multi-mate control of cores that admit a common free-1 CS
e-pair in their **common complement**.

## Payment path

```text
M_pad ≤ 1  +  CS pairs → e·p (= t·p)  ⇒  |A_SP| ≤ t·p
```

At free_core=1, forbidding multipads = forbidding free-1 CS core pairs with
joint e-extension (CS packing at scale `m_c`). Deployed free_core ≫ 1 so this
reduction does not fire.

## Toys

| j | w | m_c | free_core | max M_pad | #mp | fc1 free1 CS? | joint avoid? | deg bound | max dd |
|---|---|---:|---:|---:|---:|---|---|---:|---:|
| 4 | 1 | 2 | 1 | 4 | 540 | True | True | 0 | 0 |
| 4 | 2 | 1 | -1 | 1 | 0 | None | None | -2 | -1 |
| 5 | 1 | 3 | 2 | 9 | 972 | None | True | 1 | 1 |
| 5 | 2 | 2 | 0 | 1 | 0 | None | None | -1 | -1 |
| 6 | 1 | 4 | 3 | 14 | 904 | None | True | 2 | 2 |
| 6 | 2 | 3 | 1 | 2 | 2 | True | True | 0 | 0 |
| 6 | 3 | 2 | -1 | 1 | 0 | None | None | -2 | -1 |
| 7 | 1 | 5 | 4 | 17 | 620 | None | True | 3 | 3 |
| 7 | 2 | 4 | 2 | 2 | 4 | None | True | 1 | 1 |
| 7 | 3 | 3 | 0 | 1 | 0 | None | None | -1 | -1 |
| 8 | 1 | 6 | 5 | 14 | 364 | None | True | 4 | 4 |
| 8 | 2 | 5 | 3 | 2 | 2 | None | True | 2 | 2 |
| 8 | 3 | 4 | 1 | 1 | 0 | True | None | 0 | -1 |
| 9 | 2 | 6 | 4 | 1 | 0 | None | None | 3 | -1 |
| 9 | 3 | 5 | 2 | 1 | 0 | None | None | 1 | -1 |
| 10 | 2 | 7 | 5 | 1 | 0 | None | None | 4 | -1 |
| 10 | 3 | 6 | 3 | 1 | 0 | None | None | 2 | -1 |

Census: fc1 pair-checks=818 all same-high;
joint-avoid checks=34144 all OK.

## OPEN

1. Bound/eliminate multipads at free_core=`846161` (depth-w multi-mates
   of size `m_c` with joint complement CS-extension)
2. Inject free-1 CS e-pairs into `e·p` (v22 natural marks banked negative)

## CAS

- Model free_core=1 multipad ideal (two monics free-1 CS cores × free-1 CS
  sides, fully split, joint avoid) in Sage/msolve
- Lift emptiness / degree obstructions toward free_core ≫ 1

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v23.py --check
```
