# KB-MCA Route-D v15: ledger residual injection (top-seam / marked incidence)

Status: `PARTIAL` — matching-free mass law + E2/E5 bridges **PROVED**;
H_seam and actual injection **OPEN**.

## Attack surface (on track)

Close residual mass by **injection**, not multi-mate tourism:

```text
E2:  residual injects into {0,...,t-1} x F_p     size t*p = 143763024447376
E5:  residual injects into D x F_p                 size n*p = 4468415257378816
```

Both fit under TARGET = 274836936291722953 (v14).

## Top-seam graph (PROVED)

Vertices: supports in `Fib_w(z)`.
Edges: same lex can-core, sides in core pencil `U(C,z)` (free-1 CS).
Components: cliques of size ≤ pack_ceil = 17.

## Matching-free mass law (PROVED)

If `R ⊆ Fib_w(z)` is **matching-free** (no seam edge inside R):

```text
|R| = N_can_prim(R)
pack covering: |R| ≤ 1 · N_can_prim
```

Residual mass = residual can-core count. Side is determined by `(z, C)`.

## H_seam (conditional / open)

Ledger residual (v1 deletions include `sp_shift_pair`, `bc_chart`) is **intended**
to be matching-free. Not proved here without an SP/BC payment theorem that
removes multi-member core pencils from residual support.

```text
H_seam  =>  |R| = N_can_prim
H_seam + E2/E5 injection  =>  residual mass atom
```

## Marked incidence (PROVED normal form, not mass)

With **marked** core G, top-seam neighbors inject into `(B, c)` split-translate
data. Unmarked counting is invalid (hostile audit). Oriented first-mate (v2)
labels non-isolated vertices — vacuous under matching-free residual.

## OPEN_LEDGER_RESIDUAL_INJECTION

1. Prove **H_seam** for ledger residual, and
2. Inject residual supports/cores into `[t] x F_p` or `D x F_p`

using first-match marks (selector, pivot row, …).

## Toy bank (aperiodic + seam-free proxy)

| j | w | max full | max ap | max strong | Ncan | R=Ncan | max(minS,cU) | max(minU,cU) | lex |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| 9 | 2 | 42 | 42 | 42 | 42 | True | 10 | 10 | 1 |
| 7 | 2 | 42 | 42 | 42 | 42 | True | 7 | 7 | 1 |
| 10 | 3 | 5 | 4 | 4 | 4 | True | 2 | 2 | 1 |
| 6 | 2 | 32 | 32 | 31 | 31 | True | 5 | 5 | 1 |
| 9 | 3 | 5 | 5 | 5 | 5 | True | 2 | 2 | 1 |
| 5 | 2 | 17 | 17 | 17 | 17 | True | 2 | 2 | 1 |

Strong proxy: `|R|=N_can`. Naive D×F_p-scale marks still collide.

## Non-claims

Not `U(1116048)≤B*`. Not H_seam. Not E2/E5 injection. Not global uniqueness.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v15.py
python3 experimental/scripts/verify_kb_qatom_route_d_v15.py --check
```
