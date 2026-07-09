# KB-MCA Route-D v74: injectivity for `t ≤ 2e`

Status: **`t ≤ 2e` injectivity PROVED** (board threshold raised); deployed residual
still **OPEN** (`n' ≫ 2e`). Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED

```text
On any GP arc of length t <= 2e (with 2e < n, p odd, p does not divide 2e):
free-1 high is injective => coll = 0 => |T| = 0.
```

| range | argument |
|---|---|
| `t < 2e` | packing `m_h ≤ ⌊t/e⌋ = 1` (v73) |
| `t = 2e` | partition + `f(f-δ)=P_{2e}` ⇒ `P_{2e}+γ` square; formal monic sqrt obstruction |

## Span (PROVED)

Multipad `G`: `span(G) = max(supp)-min(supp) ≥ e`.

## Classification at `t = 2e` (PROVED)

```text
U sqcup V = {0,...,2e-1}
f, g monic deg e,  f - g = δ ≠ 0,  f g = P_{2e}
```

## Deployed

| | |
|---|---:|
| 2e | 134944 |
| n' | 1183520 |
| n'/e | 17.54 |
| `t≤2e` closes residual? | **no** |

## CAS

### Injectivity for `t ≤ 2e`

| p | e | t | #mp pairs | inj? |
|---|---:|---:|---:|---|
| 61 | 2 | 2 | 0 | Y |
| 61 | 2 | 3 | 0 | Y |
| 61 | 2 | 4 | 0 | Y |
| 61 | 3 | 3 | 0 | Y |
| 61 | 3 | 5 | 0 | Y |
| 61 | 3 | 6 | 0 | Y |
| 61 | 4 | 4 | 0 | Y |
| 61 | 4 | 7 | 0 | Y |
| 61 | 4 | 8 | 0 | Y |
| 61 | 5 | 5 | 0 | Y |
| 61 | 5 | 9 | 0 | Y |
| 61 | 5 | 10 | 0 | Y |
| 101 | 2 | 2 | 0 | Y |
| 101 | 2 | 3 | 0 | Y |
| 101 | 2 | 4 | 0 | Y |

### Multipad spans (`t > 2e`)

| p | e | t | #pairs | min span | max span |
|---|---:|---:|---:|---:|---:|
| 61 | 3 | 13 | 2 | 12 | 12 |
| 61 | 3 | 17 | 29 | 12 | 16 |
| 61 | 3 | 24 | 383 | 12 | 23 |
| 101 | 3 | 9 | 1 | 8 | 8 |
| 101 | 3 | 17 | 17 | 8 | 14 |
| 101 | 4 | 21 | 3 | 19 | 20 |
| 127 | 3 | 16 | 1 | 15 | 15 |
| 127 | 4 | 21 | 1 | 20 | 20 |

Formal sqrt obstruction rows: 30 (all fire).

## OPEN

Raise multipad-free threshold from `2e` toward `n'` (fewnomial / large-t), or SoftB.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v74.py --check
```
