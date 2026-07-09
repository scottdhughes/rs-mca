# KB-MCA Route-D v64: phase `f·G` form, CS bound, soft-B budget

Status: **identities + deployed B_\* arithmetic PROVED**;
`max|S|<=B_\*` at deployed still **OPEN**. Local on `scott/kb-route-d-T-bound`.

## Level-set form (PROVED)

```text
f(s) = sum_{x in S ∩ (s-S)} psi(l1 (s x - x^2))
All  = sum_s psi(-l0 s) f(s) G(-l0 + l1 s)
```

## Cauchy + Plancherel (PROVED)

```text
l1 != 0  =>  sum_s |G(beta(s))|^2 = p t
|All|    <= sqrt(sum |f|^2) * sqrt(p t)
         <= sqrt(E_+(S) p t)
```

## Soft-B budget (PROVED)

```text
coll <= C^2/p^{e-1} + B^2     (v58)
|T|  <= coll/2                 (v57)
want coll <= 2 H2  =>  B <= B_* = sqrt(2 H2 - C^2/p^{e-1})
```

## Deployed arithmetic (PROVED)

| quantity | value |
|---|---:|
| n' | 1183520 |
| e | 67472 |
| H2 | 77291948627 |
| log2 C | 373341.48 |
| log2(C²/p^{e-1}) | -1344154.6 |
| B_\* = √(2 H2) | **393171.6** |

`C²/p^{e-1}` is ~ `2^{-1.34e6}` (negligible).  
**Closing bar at deployed is `max|S| ≤ ~3.93×10^5`, not `|S|≤√C`.**

e=3 `|S|≤√C` remains a clean *method* template; the residual card only needs soft-B.

## CAS

### f·G / CS rows

| p | t | (l0,l1) | |All| | CS bound | v62 | CS/v62 | (sum|f|²)/t² |
|---|---:|---|---:|---:|---:|---:|---:|
| 61 | 12 | 1,1 | 90.1 | 4.6e+02 | 2.5e+03 | 0.18 | 1.97 |
| 61 | 12 | 3,5 | 58.4 | 4.7e+02 | 2.5e+03 | 0.18 | 2.08 |
| 61 | 15 | 1,1 | 147.5 | 6.2e+02 | 3.5e+03 | 0.18 | 1.89 |
| 61 | 15 | 3,5 | 117.6 | 6.0e+02 | 3.5e+03 | 0.17 | 1.77 |
| 101 | 15 | 1,1 | 89.6 | 8.7e+02 | 5.9e+03 | 0.15 | 2.20 |
| 101 | 15 | 3,5 | 250.1 | 8.7e+02 | 5.9e+03 | 0.15 | 2.20 |
| 101 | 20 | 1,1 | 373.4 | 1.3e+03 | 9.0e+03 | 0.14 | 2.11 |
| 101 | 20 | 3,5 | 336.5 | 1.2e+03 | 9.0e+03 | 0.14 | 1.88 |

### max|S| (e=3)

| p | t | max|S| | √C | S/√C |
|---|---:|---:|---:|---:|
| 61 | 15 | 60.0 | 21.3 | 2.81 |
| 61 | 24 | 97.0 | 45.0 | 2.16 |
| 101 | 15 | 57.2 | 21.3 | 2.68 |
| 101 | 24 | 136.2 | 45.0 | 3.03 |
| 127 | 15 | 69.8 | 21.3 | 3.27 |
| 127 | 36 | 221.8 | 84.5 | 2.63 |

- fact err max = 1.5e-11
- CS/v62 in [0.12, 0.18]
- (sum|f|²)/t² in [1.75, 2.20]
- max S/√C = 3.27
- CS still does not force e=3 √-cancel (bound_S/√C max 1.3e+01)

## Link

v58 + soft-B: prove `|S|≤B_\*~393172` at deployed `(n',e)` ⇒ `|T|≤H2`.  
v64 isolates that numerical bar and gives CS handle on e=3 via phased energy `sum|f|²`.

## OPEN

1. **Primary:** `max_{λ≠0} |S(λ)| ≤ B_\*` at deployed `(n',e)` (free-1 highs on GP arc).  
2. Bound `sum|f|²` for GP arcs (e=3 laboratory).  
3. Alternate `|R2|≤e·p` if exp-sums stall.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v64.py --check
```
