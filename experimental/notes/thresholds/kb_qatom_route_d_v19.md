# KB-MCA Route-D v19: P_multi / |A_SP| cost laws

Status: `PARTIAL` — graph cost chain **PROVED**; max-fiber pair bound **OPEN**.

## Cost chain (PROVED)

```text
N_ord  =  sum degrees on multi-member top-seam cliques
|A_SP|  ≤  N_ord  ≤  (pack−1) · |A_SP|  ≤  (pack−1) · N
|A_SP|  ≤  pack · P_multi
P_multi  ≤  floor(|A_SP|/2)  ≤  floor(N/2)
```

Deployed: `pack = 17`, `Δ = 16`.

## Global sum (PROVED)

```text
sum_z N_ord(z)  =  sum_{ |C|=j-e } Nord_CS(e; D\C)
```

Ambient size `n' = n-j+e = A+e = 1183520`.

Ambient bound: `Nord_CS(e, Omega) <= C(|Omega|,e) * max(floor(|Omega|/e)-1, 0)`.

This controls **sums**, not **max_z**.

## Payment criteria (PROVED conditional)

| Criterion | Implies |
|---|---|
| `max N_ord <= t*p` | `|A_SP| <= t*p` |
| `max P_multi <= t*p/17 = 8456648496904` | `|A_SP| <= t*p` |

`t*p ~ 2^{47.03}` (generated-field scale).

## Circular warning

`N_ord <= 16*N` reduces A_SP cost to a multiple of the **prefix fiber max** —
the Q atom itself. Useful only with a **direct pair injection** into size `<= t*p`.

## Toys

| j | w | max N | max A_SP | max P_multi | max N_ord | P≤N/2 |
|---|---|---:|---:|---:|---:|---|
| 4 | 1 | 108 | 85 | 30 | 202 | True |
| 4 | 2 | 8 | 7 | 3 | 12 | True |
| 5 | 1 | 257 | 151 | 61 | 270 | True |
| 5 | 2 | 17 | 10 | 5 | 10 | True |
| 6 | 2 | 32 | 12 | 6 | 12 | True |
| 6 | 3 | 5 | 2 | 1 | 2 | True |
| 7 | 2 | 42 | 10 | 5 | 12 | True |
| 8 | 2 | 54 | 7 | 3 | 10 | True |
| 8 | 3 | 7 | 2 | 1 | 2 | True |
| 9 | 2 | 42 | 4 | 2 | 4 | True |
| 9 | 3 | 5 | 2 | 1 | 2 | True |
| 10 | 3 | 5 | 0 | 0 | 0 | True |
| 10 | 4 | 2 | 0 | 0 | 0 | True |

Multi-pencils shrink as `w` grows; some rows have `maxP=0`.

## OPEN

Prove `max N_ord ≤ t·p` or inject top-seam pairs into a size-`t·p` set
(marked incidence with a small, ledger-legal mark).

## CAS next

- Sage/PARI: pair-count vs N on larger dyadic rows
- Relate Nord_CS on punctured cosets to group structure

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v19.py --check
```
