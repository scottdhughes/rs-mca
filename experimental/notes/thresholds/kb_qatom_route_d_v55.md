# KB-MCA Route-D v55: attack `|T| ≤ H2`

Status: **hierarchy PROVED**; **e=2 CLOSED**; deployed e>2 still **OPEN**.
Random-model entropy strongly suggests `T=∅` at deployed scale (heuristic only).

## Setup (v53–v54)

```text
|H_unt| = |T|
T = { U ⊆ I_{n'} : |U|=e, n'−1 ∈ U, U has free-1 partner on I_{n'} }
n'=1183520, e=67472, k=⌊n'/e⌋=17, H2=77291948627
H2/p ≈ 36.2753
```

## Hierarchy (PROVED)

```text
|T|  ≤  min( p^{e−1},  binom(n'−1, e−1),  binom(n'−1, 2e−1) )
```

## e=2 (PROVED)

```text
|T| ≤ min(p, n'−1) ≤ p ≤ H2
```

## Deployed entropy heuristic (NOT a proof)

Random model: `C(n',e)` highs drawn uniformly in `F_p^{e−1}`:

| quantity | log2 |
|---|---:|
| `C(n',e)` | 373341.48 |
| `p^{e−1}` | 2090837.54 |
| `E[# colliding pairs] ≈ C²/(2 p^{e−1})` | **-1344155.6** |
| `H2` | 36.17 |

So under uniformity, expected multipad pairs are `2^{-1.3×10^6}` — empty for all
practical purposes. **Caveat:** free-1 highs on a GP are algebraic; e=2 is a
structured regime with `|T|∼n'` multipads. Large-e needs a real GP argument.

## CAS (toys)

| p | e | t | \|T\| | nH | C(t−1,e−1) | p^{e−1} | T≤p? |
|---|---:|---:|---:|---:|---:|---:|---|
| 127 | 2 | 126 | 125 | 127 | 125 | 127 | True |
| 101 | 2 | 100 | 99 | 101 | 99 | 101 | True |
| 61 | 2 | 60 | 59 | 61 | 59 | 61 | True |
| 31 | 2 | 30 | 29 | 31 | 29 | 31 | True |
| 31 | 2 | 16 | 14 | 30 | 15 | 31 | True |
| 61 | 2 | 16 | 13 | 45 | 15 | 61 | True |
| 101 | 2 | 16 | 9 | 31 | 15 | 101 | True |
| 127 | 2 | 16 | 10 | 29 | 15 | 127 | True |
| 31 | 2 | 10 | 6 | 13 | 9 | 31 | True |
| 61 | 2 | 10 | 3 | 10 | 9 | 61 | True |
| 101 | 2 | 10 | 2 | 3 | 9 | 101 | True |
| 127 | 2 | 10 | 1 | 1 | 9 | 127 | True |
| 31 | 2 | 8 | 3 | 6 | 7 | 31 | True |
| 61 | 2 | 8 | 3 | 4 | 7 | 61 | True |
| 101 | 2 | 8 | 0 | 0 | 7 | 101 | True |
| 127 | 2 | 8 | 0 | 0 | 7 | 127 | True |
| 31 | 2 | 6 | 2 | 3 | 5 | 31 | True |
| 61 | 2 | 6 | 0 | 0 | 5 | 61 | True |
| 101 | 2 | 6 | 0 | 0 | 5 | 101 | True |
| 127 | 2 | 6 | 0 | 0 | 5 | 127 | True |

- All rows: `T ≤ p^{e−1}` and `T ≤ C(t−1,e−1)`.
- e=2: always `T ≤ p`.
- e≥3: **`T > p` occurs** (4+ examples) — no `|T|≤p` for e>2.

## Residual card path

```text
e=2: |T|≤H2 ✓
e>2 deployed: need algebraic |T|≤H2 or T=∅  (entropy suggests empty)
alternate: |R2|≤e·p
```

## OPEN

1. **Prove** `|T|≤H2` or `T=∅` at deployed `(n',e)` on the KB arc.
2. Do not treat random-model entropy as a theorem.
3. `A_SP ≤ t·p`.

## Tools

- Python NT venv: exact enum + log-combinatorics
- Sage: e=3 elementary-symmetric cross-check
- PARI/GP, Oscar available for follow-up character-sum / FF work

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v55.py --check
```
