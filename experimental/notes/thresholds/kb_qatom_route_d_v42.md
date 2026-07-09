# KB-MCA Route-D v42: decouple K_cap multi-tier from card A_SP≤t·p

Status: `PARTIAL` — **Gate A vs Gate B decoupled** PROVED; weak high gates
H1/H2/H17 PROVED as arithmetic; deployed N_ord≤e·p / |H|≤H2 still **OPEN**.

## Two gates (PROVED distinction)

| Gate | Needs | Pays |
|---|---|---|
| **A** multi-tier `(τ,local,ι,δ)` | `|H| ≤ K_cap = 2170` | constructive sides in **one** e·p |
| **B** cardinality | `N_ord ≤ e·p = t·p` | `|A_SP| ≤ t·p` (v17) |

Overflow `|H|>K_cap` blocks **A**, not automatically **B**.

## Card chain (PROVED)

```text
|A_SP|  ≤  N_ord                         (v17)
N_ord   ≤  M_pad · N_side                (v20)
N_side  ≤  |H| · 31 · 30  = 930 |H|      (v36/v25)
```

### Weak |H| gates for Gate B

```text
M_pad ≤ 1:   |H| ≤ H1  = 154583897255   ≈ 1.55e11
M_pad ≤ 2:   |H| ≤ H2  = 77291948627   ≈ 7.73e10   ← Type D residual (v35)
M_pad ≤ 17:  |H| ≤ H17 = 9093170426  ≈ 9.09e9
```

All ≫ K_cap = 2170.

### K_cap still sufficient for both

```text
|H| ≤ 2170  ⇒  N_side ≤ 2018100 ≪ e·p  ⇒  Gate B
            and multi-tier fits                         ⇒  Gate A
```

## Joint enum (PROVED conditional)

```text
μ_all = (i mod e, ⌊i/e⌋)  on all unique free-1 CS pairs
N_side ≤ e·p  ⇒  constructive e·p side mark (no H_core split)
```

## Program impact

```text
v41 overflow fear: |H|>K_cap ⇒ multi-tier fails
v42:              still OK for A_SP≤t·p if N_ord≤e·p
                  (e.g. |H|≤H2 with M_pad≤2 after SR)
```

Preferred attack is no longer `|H|≤2170` alone — prove **`N_ord≤e·p`** or
**`|H|≤H2`**.

## A_SP-prefix toys

| j | w | free_core | #H | N_side | N_ord | A_SP | A≤Nord? | μ_all? | H≤Kcap? |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| 4 | 1 | 1 | 17 | 400 | 3170 | 1363 | True | True | True |
| 4 | 2 | -1 | 164 | 440 | 992 | 857 | True | True | True |
| 5 | 1 | 2 | 17 | 286 | 4386 | 2468 | True | True | True |
| 5 | 2 | 0 | 110 | 260 | 1090 | 1006 | True | True | True |
| 6 | 1 | 3 | 17 | 200 | 4616 | 3144 | True | True | True |
| 6 | 2 | 1 | 65 | 146 | 930 | 882 | True | True | True |
| 7 | 1 | 4 | 17 | 132 | 3666 | 2869 | True | True | True |
| 7 | 2 | 2 | 36 | 80 | 598 | 580 | True | True | True |
| 8 | 2 | 3 | 19 | 42 | 282 | 279 | True | True | True |
| 9 | 2 | 4 | 8 | 16 | 94 | 94 | True | True | True |
| 5 | 2 | 0 | 179 | 568 | 3080 | 2604 | True | True | True |
| 6 | 2 | 1 | 127 | 354 | 3254 | 2977 | True | True | True |
| 7 | 2 | 2 | 85 | 214 | 2558 | 2447 | True | True | True |
| 4 | 2 | -1 | 961 | 11400 | 48780 | 22068 | True | True | True |

## Ambient free-1 (no fiber cut)

| n | e | #H | N_side | H>Kcap? | N_side≤e·p dep? | H≤H2? |
|---|---:|---:|---:|---|---|---|
| 16 | 3 | 224 | 704 | False | True | True |
| 30 | 3 | 961 | 14250 | False | True | True |
| 70 | 3 | 4970 | 550550 | True | True | True |
| 72 | 3 | 5329 | 620688 | True | True | True |

Census: max asp H=961; max amb H=5329;
amb over Kcap=2; all μ_all / A≤Nord on asp rows.

## OPEN

1. Deployed `N_ord ≤ e·p` or `|H| ≤ H2` (M_pad≤2 residual)
2. Or `|H| ≤ K_cap` (both gates)
3. Full `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v42.py --check
```
