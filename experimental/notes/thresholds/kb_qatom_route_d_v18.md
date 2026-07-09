# KB-MCA Route-D v18: CAS tools + μ_E5 collision algebra

Status: `PARTIAL` — collision constraints **PROVED**; injectivity / P_multi **OPEN**.

## Tools on this machine (use for open walls)

| Problem | Tools |
|---|---|
| Bound `P_multi` / `|A_SP|` | Sage, PARI (enum); Wolfram (gen fn / asymptotics); grande_finale L2 identities |
| Kill/find residual marks | Sage, msolve, M2, Singular (collision ideals); PARI (poly gcd audits) |
| Deployed-scale Gröbner | **Not feasible** at `(j,w)~10^5` — structure only |

## μ_E5 collision algebra (PROVED)

If `μ_E5(S)=μ_E5(T)` with same fiber prefix:

```text
deg(Λ_S − Λ_T)  ≤  j − w − 2     (= 913631 deployed)
min root α ∈ S ∩ T
```

On **R_sing** (after A_SP): collisions have **distinct can-cores**
(because S ↔ C_can is bijective).

So failures of μ_E5 are not within-pencil noise — they are cross-core
with shared min and one extra agreed free coefficient.

## Toy (stdlib re-check of Sage audit)

| j | w | #coll pairs | max μ_E5 | diff C? | deg OK? | bound |
|---|---|---:|---:|---|---|---:|
| 8 | 2 | 3576 | 5 | True | True | 4 |
| 9 | 2 | 3386 | 5 | True | True | 5 |
| 6 | 2 | 594 | 3 | True | True | 2 |
| 10 | 3 | 10 | 2 | True | True | 5 |
| 5 | 2 | 57 | 3 | True | True | 1 |

## Still open

1. `P_multi ≤ t·p/17` (or other printed A_SP cost)
2. Mark with empty collision set on ledger residual

## Optional Sage replay

```text
sage -c '...'  # see packet development notes / agents-log
```

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v18.py --check
```
