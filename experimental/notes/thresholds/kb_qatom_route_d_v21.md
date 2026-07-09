# KB-MCA Route-D v21: M_pad degree obstruction

Status: `PARTIAL` — multipad **degree bound** PROVED; deployed `M_pad≤1` **OPEN**.

## Multipad degree bound (PROVED)

If two distinct cores share the same free-1 CS sides `(U,V)` and the same
fiber prefix via `C∪U`:

```text
deg(Λ_C − Λ_{C'})  ≤  j − 2w − 2
```

### Corollary

```text
j < 2w + 2   ⇒   M_pad(z) ≤ 1  for all z
```

## Deployed arithmetic

```text
j           = 981104
2w+2        = 134944
j < 2w+2?   = False
j−2w−2      = 846160   (≥ 0: degree room for multipads)
t = e = w+1 = 67472
t·p = e·p   = 143763024447376
```

So the **sufficient** condition `j<2w+2` does **not** apply to KB-MCA.
Multipads are not ruled out by degree alone.

## Payment path (still)

```text
M_pad ≤ 1  +  CS pairs inject into e·p
    ⇒  N_ord ≤ e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

## Toys

| j | w | j<2w+2? | max M_pad | max N_ord | deg bound | max core diff deg |
|---|---|---|---:|---:|---:|---:|
| 6 | 1 | False | 14 | 288 | 2 | 2 |
| 6 | 2 | False | 2 | 12 | 0 | 0 |
| 6 | 3 | True | 1 | 2 | -2 | -1 |
| 6 | 4 | True | 1 | 0 | -4 | -1 |
| 7 | 2 | False | 2 | 12 | 1 | 1 |
| 7 | 3 | True | 1 | 2 | -1 | -1 |
| 8 | 2 | False | 2 | 10 | 2 | 2 |
| 8 | 3 | False | 1 | 2 | 0 | -1 |
| 8 | 4 | True | 1 | 0 | -2 | -1 |
| 9 | 2 | False | 1 | 4 | 3 | -1 |
| 9 | 3 | False | 1 | 2 | 1 | -1 |
| 10 | 2 | False | 1 | 2 | 4 | -1 |
| 10 | 3 | False | 1 | 0 | 2 | -1 |
| 5 | 1 | False | 9 | 270 | 1 | 1 |
| 5 | 2 | True | 1 | 10 | -1 | -1 |
| 4 | 1 | False | 4 | 202 | 0 | 0 |
| 4 | 2 | True | 1 | 12 | -2 | -1 |

When `j<2w+2`, measured `M_pad=1`. When multipads exist, core diff degrees
respect `≤ j−2w−2`.

## OPEN

1. **Deployed M_pad≤1** by split-support / residual reasons beyond degree
2. **Inject free-1 CS pairs into e·p** (natural: index in `{0..e−1}` × F_p)

## CAS

Sage/msolve: system for two monic split cores with
`(Λ_C−Λ_{C'})Λ_U` of degree `≤ j−w−1` — restrict to regimes or find
structural constraints forcing `C=C'`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v21.py --check
```
