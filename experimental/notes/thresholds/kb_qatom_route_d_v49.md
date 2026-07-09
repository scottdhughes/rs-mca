# KB-MCA Route-D v49: co-extension free-1 = prefix free-1 multipads

Status: `PARTIAL` — **prefix window geometry PROVED**; residual untyped highs
reduce to `H_*^{pre}` on index arcs; deployed bound still **OPEN**.

## Geometry (PROVED)

A_SP uses `U =` e least indices of `S`, `C = S\U`:

```text
max(U) < min(C) = t
⇒  U ⊆ I_t = {0,1,...,t−1}
```

Multi-U free-1 pencil with core `C` ⇒ all free-1 mates live in **I_t**.

Multipad (`|F|≥2`) forces:

```text
2e  ≤  t  ≤  n − m_c  =  n'  =  A+e
```

Deployed window range:

```text
t ∈ [134944, 1183520]
⌊n'/e⌋ = 17
e/n' ≈ 0.0570
```

## Bound (PROVED)

```text
|H_coext(C)|  ≤  H_*^{pre}(min(C), e)
```

`H_*^{pre}(t,e)` = # free-1 multipad highs among e-subsets of the prefix
`{ω^0,...,ω^{t−1}}` of the fixed KB domain.

Under C_unique (v47):

```text
|H_unt|  ≤  N_C · max_{t ∈ [2e,n']} H_*^{pre}(t,e)
```

## e=2 (PROVED)

`H_*^{pre}(t,2) ≤ p ≤ H2` for all t — coext residual card OK when e=2.

Deployed e=67472 ≫ 2.

## OPEN ★_pre

```text
max_{t ≤ n'} H_*^{pre}(t, e=67472)  ≤  H2 ?
```

Free-1 multipads on a **roots-of-unity arc** of length t, not an abstract
field-cyclic domain of size t (v48: those saturate p^{e−1} for e=3).

## Prefix H_* toys

| n | e | t | nH | floor | ≤floor? | p^{e−1} |
|---|---:|---:|---:|---:|---|---:|
| 16 | 2 | 8 | 10 | 4 | False | 17 |
| 16 | 2 | 16 | 17 | 8 | False | 17 |
| 16 | 3 | 8 | 1 | 2 | True | 289 |
| 16 | 3 | 12 | 36 | 4 | False | 289 |
| 16 | 3 | 16 | 224 | 5 | False | 289 |
| 30 | 2 | 15 | 30 | 7 | False | 31 |
| 30 | 2 | 30 | 31 | 15 | False | 31 |
| 30 | 3 | 12 | 12 | 4 | False | 961 |
| 30 | 3 | 20 | 312 | 6 | False | 961 |
| 30 | 3 | 30 | 961 | 10 | False | 961 |
| 72 | 3 | 18 | 50 | 6 | False | 5329 |
| 72 | 3 | 36 | 2145 | 12 | False | 5329 |
| 72 | 3 | 72 | 5329 | 24 | False | 5329 |
| 100 | 3 | 15 | 11 | 5 | False | 10201 |
| 100 | 3 | 30 | 546 | 10 | False | 10201 |
| 100 | 3 | 50 | 6368 | 16 | False | 10201 |

## Co-extension census (prefix enforced)

| j | w | fc | #H coext | max H/C | #C | min t | max t | t≥2e? |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 4 | 1 | 1 | 17 | 17 | 45 | 6 | 14 | True |
| 5 | 1 | 2 | 17 | 17 | 120 | 6 | 13 | True |
| 5 | 2 | 0 | 110 | 110 | 28 | 8 | 14 | True |
| 6 | 1 | 3 | 17 | 17 | 210 | 6 | 12 | True |
| 6 | 2 | 1 | 65 | 65 | 56 | 8 | 13 | True |
| 7 | 2 | 2 | 36 | 36 | 70 | 8 | 12 | True |
| 8 | 2 | 3 | 19 | 19 | 56 | 8 | 11 | True |
| 5 | 2 | 0 | 179 | 179 | 28 | 10 | 16 | True |
| 6 | 2 | 1 | 127 | 127 | 56 | 10 | 15 | True |
| 7 | 2 | 2 | 85 | 85 | 70 | 10 | 14 | True |
| 4 | 2 | -1 | 961 | 961 | 20 | 10 | 29 | True |

Census: max H/C=961; max coext H=961.

## Path to residual card

```text
SR + Type D + H_M
  → pure-untyped free-1 highs
  → H_*^{pre} on I_t, t=min(C) ∈ [2e,n']
  → need max H_*^{pre} ≤ H2 (or H2/N_C)
```

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v49.py --check
```
