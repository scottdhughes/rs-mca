# KB-MCA Route-D v40: ambient L≤70 REFUTED; L_rep≤70 PROVED

Status: `PARTIAL` — **matched representative load L_rep ≤ R_max = 70
PROVED**; ambient **L≤70 / L≤2176 REFUTED**; full-cover L_core≤R **REFUTED**.

## Resolution of the L-gate

| Claim | Status |
|---|---|
| Ambient free-1 load L ≤ 70 | **REFUTED** |
| Ambient free-1 load L ≤ 2176 | **REFUTED** |
| Full-cover load on H_core ≤ R | **REFUTED** (mates) |
| Matched **representative** load L_rep ≤ R_max = 70 | **PROVED** |
| |H_core| ≤ R_max·⌊n/e⌋ = 2170 | **PROVED** (packing) |

```text
ambient L        can be ≫ 70, ≫ 2176
L_rep (U_rep)    ≤ R_max = 70     ← surviving L≤70
L_cover_core     can exceed R     ← mates touch extra points
|H_core|         ≤ 70 · 31 = 2170 ← packing (v39)
```

## Matched representative load (PROVED)

Multi-tier first-match, R = R_max tiers, each matched high has U_rep:

- Within one tier, claiming U_rep∋r removes r from `free` ⇒ ≤1 matched high with r∈U_rep per tier.
- R_max tiers ⇒ **L_rep(r) ≤ 70**.

This is **not** full-cover load: cover(H)=⋃F_H can include mates V≠U_rep through r.

## |H_core| (PROVED, packing)

```text
|H_core| ≤ R_max · ⌊n/e⌋ = 70 · 31 = 2170 = K_cap
```

## Ambient refutation (BANKED)

| n | e | #H | L | L>70? | L>2176? |
|---|---:|---:|---:|---|---|
| 16 | 2 | 17 | 15 | False | False |
| 16 | 3 | 224 | 96 | True | False |
| 16 | 4 | 89 | 49 | False | False |
| 30 | 3 | 961 | 406 | True | False |
| 70 | 3 | 4970 | 2346 | True | True |
| 72 | 3 | 5329 | 2485 | True | True |

Max ambient L: **2485**. A_SP-prefix also hits L>70.

## Other proved lemmas

1. **Injection:** L(r) ≤ C(n−1,e−1).
2. **Multi-mate count:** |F_H|≥2 ⇒ |H| ≤ n·L/(2e).

## A_SP toys

| j | w | free_core | #H | L | L_rep | L_cover_core | R | #H_core | L_rep≤R? | cover>R? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 4 | 1 | 1 | 17 | 13 | 3 | 13 | 5 | 17 | True | True |
| 4 | 2 | -1 | 164 | 72 | 35 | 72 | 35 | 147 | True | True |
| 5 | 1 | 2 | 17 | 12 | 4 | 12 | 5 | 17 | True | True |
| 5 | 2 | 0 | 110 | 51 | 25 | 51 | 25 | 98 | True | True |
| 6 | 1 | 3 | 17 | 11 | 4 | 11 | 5 | 17 | True | True |
| 6 | 2 | 1 | 65 | 34 | 16 | 31 | 16 | 59 | True | True |
| 6 | 3 | -1 | 30 | 19 | 10 | 17 | 10 | 24 | True | True |
| 7 | 1 | 4 | 17 | 10 | 5 | 10 | 5 | 17 | True | True |
| 7 | 2 | 2 | 36 | 22 | 10 | 18 | 10 | 31 | True | True |
| 7 | 3 | 0 | 13 | 10 | 6 | 10 | 6 | 13 | True | True |
| 8 | 1 | 5 | 16 | 9 | 5 | 9 | 5 | 16 | True | True |
| 8 | 2 | 3 | 19 | 14 | 6 | 11 | 6 | 16 | True | True |
| 8 | 3 | 1 | 5 | 4 | 3 | 4 | 4 | 5 | True | False |
| 9 | 2 | 4 | 8 | 6 | 4 | 6 | 4 | 8 | True | True |
| 9 | 3 | 2 | 1 | 1 | 1 | 1 | 3 | 1 | True | False |
| 4 | 2 | -1 | 241 | 105 | 43 | 101 | 43 | 209 | True | True |
| 5 | 2 | 0 | 179 | 78 | 32 | 77 | 32 | 152 | True | True |
| 6 | 2 | 1 | 127 | 59 | 24 | 55 | 24 | 106 | True | True |

Census: L_rep ok=18; cover exceeds R on 16 rows;
max L_rep=43; max L_cover_core=101;
A_SP L>70 rows=3.

## Program path

```text
Ambient L≤70     DEAD
L_rep ≤ 70       PROVED (representatives only)
|H_core| ≤ 2170  PROVED (packing / v39 ledger)
SR + sides       on H_core
Overflow         v39 μ_over / residual OPEN
```

## OPEN

1. Overflow when ambient |H| ≫ K_cap
2. A_SP ≤ t·p full close

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v40.py --check
```
