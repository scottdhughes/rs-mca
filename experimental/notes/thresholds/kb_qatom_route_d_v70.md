# KB-MCA Route-D v70: multipad vanishing polynomial

Status: **G / P_e structure PROVED**; sparse-G ban at deployed **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## Index polynomial (PROVED)

For a free-1 multipad with index sets `A, B` (disjoint, size `e`):

```text
G(X) = sum_{a in A} X^a - sum_{b in B} X^b   in F_p[X]
G(omega^k) = 0   for k = 0,1,...,e-1
```

Coefficients in `{-1,0,1}`, exactly `2e` nonzeros.

## Division (PROVED)

```text
P_e(X) := prod_{k=0}^{e-1} (X - omega^k)  |  G(X)   in F_p[X]
G = P_e * H,   e <= deg G <= t-1,   deg H <= t-1-e
```

## Completion target

Ban nonzero sparse `G` of this form for

```text
A, B subset {0,1,...,n'-1},  |A|=|B|=e,  A cap B = empty
```

at deployed `(n', e, omega)` with `n'= 1183520`, `e=67472`.

## CAS

| p | e | t | inj? | #pairs chk | min deg G | max deg G | same f'? |
|---|---:|---:|---|---:|---:|---:|---|
| 61 | 3 | 5 | Y | 0 | - | - | Y |
| 61 | 4 | 7 | Y | 0 | - | - | Y |
| 101 | 3 | 5 | Y | 0 | - | - | Y |
| 127 | 4 | 7 | Y | 0 | - | - | Y |
| 61 | 3 | 17 | n | 29 | 12 | 16 | Y |
| 61 | 3 | 24 | n | 40 | 12 | 23 | Y |
| 101 | 3 | 17 | n | 17 | 8 | 16 | Y |
| 101 | 4 | 21 | n | 3 | 19 | 20 | Y |
| 127 | 3 | 18 | n | 5 | 15 | 17 | Y |
| 127 | 4 | 21 | n | 1 | 20 | 20 | Y |
| 61 | 4 | 21 | n | 29 | 15 | 20 | Y |

## Mathlib map (local + AXLE)

Local root: `~/lean-verify/.lake/packages/mathlib/Mathlib`.

| path | status |
|---|---|
| `Algebra/Field/GeomSum.lean` | found |
| `NumberTheory/LegendreSymbol/AddCharacter.lean` | found |
| `NumberTheory/GaussSum.lean` | found |
| `NumberTheory/DirichletCharacter/GaussSum.lean` | found |

AXLE docs: https://axle.axiommath.ai/v1/docs/  
(`check`, `verify_proof` on extracted lemmas when formalizing).

## Link

| item | status |
|---|---|
| multipads disjoint / t&lt;2e inj | CLOSED (v69) |
| **G vanishes / P_e\|G / deg window** | **CLOSED (v70)** |
| no sparse G at deployed | OPEN |
| SoftB fallback | OPEN |
| Lean phase-2 (Mathlib) | mapped, not yet coded |

## OPEN

1. No sparse multipad `G = P_e H` on `{0..n'-1}` at deployed.  
2. Or SoftB_Deployed.  
3. Lean: formalize (1)–(3) via Mathlib; AXLE-verify.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v70.py --check
```
