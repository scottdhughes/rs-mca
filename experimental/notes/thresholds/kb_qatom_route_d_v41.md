# KB-MCA Route-D v41: overflow when |H| ≫ K_cap

Status: `PARTIAL` — **e·p side budget forces R_max=70** PROVED; **overflow
cardinality/enum gates** PROVED; local overflow marks **BANKED NEGATIVE**;
deployed N_over≤e·p / A_SP≤t·p still **OPEN**. Ambient L≤70 not reopened.

## Why K_cap / R_max are tight (PROVED)

Side mark `(τ, local, ι, δ)` with full within-family `ι < ⌊n/e⌋`:

```text
R · 31 · 31  ≤  e
R_max = 70  ⇒  70·31·31 = 67270 ≤ e = 67472   (slack 202)
R = 71      ⇒  overflows e
```

One e·p cell ⇒ at most one multi-tier layer of |H|≤K_cap=2170.

**Λ≥2 layers cannot share one e·p** (2·67270 > e).

## Overflow size (PROVED)

```text
|H_over|  ≥  max(0, |H| − K_cap)
N_over    ≤  |H_over| · 31 · 30  = 930 |H_over|
```

## Overflow payment (PROVED conditional)

```text
μ_over = (i mod e, ⌊i/e⌋)   on overflow pairs (lex rank i)
N_over ≤ e·p  ⇒  lands in [e]×F_p
```

Worst-family gate:

```text
|H_over| ≤ H_OVER_ENUM_MAX = 154583897255  ≈ 1.546×10^11
```

## TARGET multi-cell arithmetic (PROVED numbers; strategy OPEN)

```text
⌊TARGET / (e·p)⌋ = 1911
⇒ ≤ 4146870 highs via layered multi-tier charged to TARGET
```

Does **not** by itself give A_SP ≤ t·p (single-cell goal).

## Hybrid sketch

| Cell | Content | Size gate |
|---|---|---|
| 1 | H_core (κ,ι,δ) | |H_core|≤K_cap (always by ledger) |
| 2 | μ_over on H_over | N_over≤e·p |

Total 2·e·p if both land — fine vs TARGET (1911 cells),
not fine vs single A_SP≤t·p unless cell2 is out-of-A_SP residual.

## Local marks (BANKED NEGATIVE)

`(c0U,δ)`, `(c0U,c0V)`, `(minU mod e, δ)`, `(minU,c0U)`, `(sumU mod e, δ)`
all collide on overflow pairs in toys with enough pairs.

## Toys

| j | w | #H | R | #H_core | #H_over | #pairs over | N≤bound? | enum? | pigeon? |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| 4 | 2 | 164 | 11 | 49 | 115 | 302 | True | True | True |
| 5 | 1 | 17 | 1 | 6 | 11 | 164 | True | True | True |
| 5 | 2 | 110 | 7 | 28 | 82 | 192 | True | True | True |
| 6 | 1 | 17 | 1 | 5 | 12 | 116 | True | True | True |
| 6 | 2 | 65 | 4 | 15 | 50 | 116 | True | True | True |
| 7 | 1 | 17 | 1 | 5 | 12 | 90 | True | True | True |
| 7 | 2 | 36 | 2 | 6 | 30 | 68 | True | True | True |
| 8 | 2 | 19 | 1 | 3 | 16 | 32 | True | True | True |
| 4 | 2 | 241 | 13 | 65 | 176 | 588 | True | True | True |
| 5 | 2 | 179 | 10 | 50 | 129 | 356 | True | True | True |
| 6 | 2 | 127 | 7 | 31 | 96 | 250 | True | True | True |

Census: over enum 11/11; local-fail rows
11; pigeon 11/11.

## Path (updated)

```text
H_core ≤ 2170          paid in 1 e·p (tight)
H_over                 μ_over if N_over≤e·p
                       else TARGET layers / hybrid OPEN
Ambient L≤70           DEAD (v40)
A_SP ≤ t·p             needs H_over≈∅ or fold overflow into one e·p
```

## OPEN

1. Deployed `N_over ≤ e·p` or `|H|≤K_cap`
2. Local e·p overflow mark (negatives banked)
3. Policy: single t·p vs TARGET multi-cell for overflow

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v41.py --check
```
