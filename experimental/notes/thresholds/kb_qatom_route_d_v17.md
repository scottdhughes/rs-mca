# KB-MCA Route-D v17: A_SP cost algebra + mark search

Status: `PARTIAL` — A_SP **cost identities** PROVED; **P_multi bound** and
**mark injectivity** OPEN. Local E2/E5 marks **fail** on toys.

## Fiber partition (PROVED)

```text
Fib_w(z) = A_SP(z)  ⊔  R_sing(z)
```

- `A_SP` = multi-member top-seam core pencils (A_SP assignment set)
- `R_sing` = singleton pencils = matching-free residual after A_SP

## A_SP printed cost (PROVED)

```text
|A_SP| = sum_{k≥2} k
|A_SP| ≤ pack_ceil · P_multi     (deployed pack_ceil = 17)
|A_SP| ≤ N_ord = sum_{k≥2} k(k-1)   (ordered seam pairs)
```

**Conditional payment:** if `P_multi ≤ t·p/17 = 8456648496904`
(~2^{42.94}), then `|A_SP| ≤ t·p`.

**OPEN:** bound `max P_multi` (or `max |A_SP|` / `max N_ord`).

## First-match form (PROVED)

```text
pay A_SP cell (bound U_A_SP)
residual ⊆ R_sing
max residual mass ≤ U_A_SP + max |R_sing|
```

## R_sing marks (PROVED reduction + negative bank)

On `R_sing`, `S ↔ C_can` bijective — mark supports or cores equivalently.

**Toy search:** no tested **n·p-scale** mark is injective on all rows.
`(min, a_{w+1}, a_{w+2})` (n·p²) works sometimes, not always, and is too large for E2/E5.

### A_SP mass toys

| j | w | multi_S | P_multi | N_ord | frac multi | max |A_SP| | max |R_sing| |
|---|---|---:|---:|---:|---:|---:|---:|
| 8 | 2 | 279 | 139 | 282 | 0.0217 | 7 | 54 |
| 9 | 2 | 94 | 47 | 94 | 0.0082 | 4 | 42 |
| 7 | 2 | 580 | 287 | 598 | 0.0507 | 10 | 42 |
| 6 | 2 | 882 | 433 | 930 | 0.1101 | 12 | 31 |
| 10 | 3 | 0 | 0 | 0 | 0.0000 | 0 | 5 |
| 5 | 2 | 1006 | 489 | 1090 | 0.2303 | 10 | 17 |
| 9 | 3 | 2 | 1 | 2 | 0.0002 | 2 | 5 |

### Mark injectivity toys (R_sing)

| j | w | any n·p mark inj? | aw1_aw2 inj? | worst max fiber |
|---|---|---|---|---:|
| 8 | 2 | False | False | 27 |
| 9 | 2 | False | False | 27 |
| 7 | 2 | False | False | 21 |
| 6 | 2 | False | True | 13 |
| 10 | 3 | False | True | 4 |
| 5 | 2 | True | True | 7 |
| 9 | 3 | False | True | 5 |

## Bridge to atom

```text
U_A_SP ≤ t·p  and  |R_sing| ≤ t·p (or n·p)
    ⇒  full fiber mass controlled at E2 scale after A_SP payment
```

## OPEN (real next theorems, refined)

1. **Bound P_multi or |A_SP|** with printed cost (establish A_SP as paid cell).
2. **Injective R_sing mark** into t·p or n·p via ledger structure (pivot/RIM/selector) —
   not another local (min, ·) experiment without new geometry.

## Non-claims

Not A_SP ≤ t·p. Not mark injectivity. Not `U(1116048)≤B*`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v17.py
python3 experimental/scripts/verify_kb_qatom_route_d_v17.py --check
```
