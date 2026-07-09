# KB-MCA Route-D v20: top-seam pair injection (side keys / M_pad)

Status: `PARTIAL` — pair normal form + M_pad calculus **PROVED**;
`M_pad≤1` and side-pair→`t·p` injection **OPEN**.

## Goal (non-circular)

Pay A_SP by bounding `N_ord` **without** only using `N_ord ≤ 16·N`.

## Normal form (PROVED)

```text
ordered top-seam pair (S,T)  ↔  (C, U, V)
  S=C⊔U, T=C⊔V,  Λ_U − Λ_V = c ≠ 0  (free-1 CS sides)
```

## Side key and M_pad (PROVED)

```text
φ(C,U,V) = (high(U), c0(U), c0(V))
```

- Recovers `(U,V)` from fully split free-1 data
- Fibers of φ = **multi-pads** (same sides, different cores)
- `M_pad(z) = max #pads per side key in fiber z`
- `N_ord(z) ≤ M_pad(z) · N_side(z)`
- **If `M_pad=1`:** pairs inject via φ into side-key space; `N_ord=N_side`

## Core-augmented mark ψ (definition + toys)

```text
ψ = (min C, c0(U), c0(V))   size n·p²  (too big for t·p payment)
```

Toys: **injective for w≥2** on F_17; **fails at w=1**.

## Payment bridge (PROVED)

```text
M_pad ≤ 1  and  side pairs inject into |L|≤t·p
    ⇒  N_ord ≤ t·p  ⇒  |A_SP| ≤ t·p
```

Deployed coincidence: **`t = e = w+1`**, so `t·p = e·p` (one side index + field elem).

## Toys

| j | w | max M_pad | max N_ord | φ inj (Mpad=1)? | ψ inj? |
|---|---|---:|---:|---|---|
| 8 | 1 | 14 | 138 | False | False |
| 8 | 2 | 2 | 10 | False | True |
| 8 | 3 | 1 | 2 | True | True |
| 7 | 1 | 17 | 230 | False | False |
| 7 | 2 | 2 | 12 | False | True |
| 7 | 3 | 1 | 2 | True | True |
| 6 | 2 | 2 | 12 | False | True |
| 6 | 3 | 1 | 2 | True | True |
| 5 | 1 | 9 | 270 | False | False |
| 5 | 2 | 1 | 10 | True | True |
| 9 | 2 | 1 | 4 | True | True |
| 9 | 3 | 1 | 2 | True | True |
| 4 | 1 | 4 | 202 | False | False |
| 4 | 2 | 1 | 12 | True | True |

`M_pad` drops as `w` grows; often `M_pad=1` by `w≥3`.

## OPEN

1. **`M_pad ≤ 1`** at deployed `w` (or after residual deletions)
2. **Inject free-1 CS ordered pairs `(U,V)` into size `e·p = t·p`**

## CAS

- Sage: multi-pad geometry on larger dyadic rows
- msolve: equations for two cores sharing `(U,V,z)` (emptiness ⇒ M_pad=1)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v20.py --check
```
