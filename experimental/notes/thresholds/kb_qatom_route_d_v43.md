# KB-MCA Route-D v43: N_ord / |H|≤H2 at deployed free_core

Status: `PARTIAL` — **complement free-1 degree 16** PROVED; **card criteria
C1–C5** PROVED; **H_M≤31≤H2** PROVED; ambient H2-envelope candidates that
look attractive **REFUTED** as theorems; deployed max N_ord≤e·p / |H|≤H2 **OPEN**.

## Deployed complement degree (PROVED)

```text
n' = A + e = 1183520
⌊n'/e⌋ = 17 = pack_ceil
deg_max free-1 CS mates per e-set in Ω  =  ⌊n'/e⌋ − 1  = 16
```

Every A_SP top-seam pair is a free-1 CS pair in some D\C (v19).

## N_ord ↔ |A_SP| (PROVED)

```text
|A_SP|  ≤  N_ord  ≤  16 · |A_SP|
```

## Card criteria for |A_SP|≤t·p (PROVED conditional)

| ID | Gate | Deployed number |
|---|---|---|
| C1 | max N_ord ≤ e·p | e·p = 143763024447376 |
| C2 | max |A_SP| ≤ e·p/16 | 8985189027961 |
| C3 | max P_multi ≤ e·p/17 | 8456648496904 |
| C4 | M_pad≤2 and |H| ≤ H2 | H2 = 77291948627 |
| C5 | active free-1 e-sets M ≤ M_* | M_* = 4792100814912 |

**Not** K_cap=2170 — that is multi-tier only (v41–v42).

## Matching-supported (PROVED)

```text
|H_M| ≤ ⌊n/e⌋ = 31 ≤ H2
N_side(H_M) ≤ 930 · 31 ≪ e·p
```

M-cell card-closes. Residual unmatched highs / R-cell is the wall.

## H2 envelopes (arithmetic vs theorems)

≤ H2 as numbers: `31n`, `pack·n`, `n'·16`, `A·e`, `31·p`, `K_cap·e`.

**Ambient free-1 REFUTES** as theorems: `|H|≤31n`, `|H|≤n⌊n/e⌋`, `|H|≤31p`,
`|H|≤pack·n` (e.g. n=72,e=3,|H|=5329).

## Ambient free-1 toys

| n | e | #H | max deg | floor−1 | >Kcap? | ≤31n? | ≤31p? | ≤pack·n? |
|---|---:|---:|---:|---:|---|---|---|---|
| 16 | 2 | 17 | 7 | 7 | False | True | True | True |
| 16 | 3 | 224 | 2 | 4 | False | True | True | True |
| 30 | 2 | 31 | 14 | 14 | False | True | True | True |
| 30 | 3 | 961 | 9 | 9 | False | False | True | False |
| 70 | 3 | 4970 | 11 | 22 | True | False | False | False |
| 72 | 3 | 5329 | 23 | 23 | True | False | False | False |

## A_SP-prefix toys

| j | w | free_core | #H | #H_M | N_ord | A_SP | Nord≤16A? | H_M≤floor? |
|---|---|---:|---:|---:|---:|---:|---|---|
| 4 | 1 | 1 | 17 | 7 | 3170 | 1363 | True | True |
| 5 | 1 | 2 | 17 | 6 | 4386 | 2468 | True | True |
| 5 | 2 | 0 | 110 | 4 | 1090 | 1006 | True | True |
| 6 | 1 | 3 | 17 | 6 | 4616 | 3144 | True | True |
| 6 | 2 | 1 | 65 | 4 | 930 | 882 | True | True |
| 7 | 1 | 4 | 17 | 5 | 3666 | 2869 | True | True |
| 7 | 2 | 2 | 36 | 3 | 598 | 580 | True | True |
| 8 | 2 | 3 | 19 | 3 | 282 | 279 | True | True |
| 9 | 2 | 4 | 8 | 2 | 94 | 94 | True | True |
| 9 | 3 | 2 | 1 | 1 | 2 | 2 | True | True |
| 6 | 2 | 1 | 127 | 5 | 3254 | 2977 | True | True |
| 7 | 2 | 2 | 85 | 4 | 2558 | 2447 | True | True |
| 8 | 2 | 3 | 55 | 4 | 1426 | 1399 | True | True |
| 4 | 2 | -1 | 961 | 9 | 48780 | 22068 | True | True |

By free_core (max |H|): fc=-1:maxH=961, fc=0:maxH=110, fc=1:maxH=127, fc=2:maxH=85, fc=3:maxH=55, fc=4:maxH=17

## Path

```text
M-cell (H_M≤31)     card CLOSED
R-cell / ambient H  need C1 or C4 (|H|≤H2) or C5
K_cap=2170          multi-tier only — not the card wall
```

## OPEN

1. `max N_ord ≤ e·p` at deployed free_core
2. `|H_A_SP| ≤ H2` (or residual |H_R|≤H2)
3. `M ≤ M_*` active free-1 e-sets

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v43.py --check
```
