# KB-MCA Route-D v73: fibre packing `m_h ≤ ⌊t/e⌋`

Status: **fibre packing PROVED** (board row); residual `|T|≤H2` still **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED

```text
m_h := #{ e-subsets with free-1 high h }  <=  floor(t/e)
```

### Proof

Any two distinct e-sets with the same free-1 high are multipads ⇒ **disjoint** (v69).  
Pairwise disjoint e-subsets of a t-set ⇒ at most `⌊t/e⌋` of them.

### Corollaries (PROVED)

| claim | result |
|---|---|
| `t < 2e` | `⌊t/e⌋=1` ⇒ injective ⇒ `\|T\|=0` (recovers v69) |
| collisions | `coll = Σ m(m-1) ≤ (K-1) C` with `K=⌊t/e⌋`, `C=binom(t,e)` |
| deployed | `K = ⌊n'/e⌋ = 17` ⇒ `m_h ≤ 17`, `coll ≤ 16 C` |

## Deployed

| | |
|---|---:|
| n' | 1183520 |
| e | 67472 |
| K = ⌊n'/e⌋ | **17** |
| coll ≤ | `16 · C` |
| closes residual alone? | **no** (still ≫ H2) |

## CAS

| p | e | t | K | max m | coll | (K-1)C | #mp highs | pack ok? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 61 | 3 | 4 | 1 | 1 | 0 | 0 | 0 | Y |
| 61 | 3 | 5 | 1 | 1 | 0 | 0 | 0 | Y |
| 61 | 4 | 5 | 1 | 1 | 0 | 0 | 0 | Y |
| 61 | 4 | 7 | 1 | 1 | 0 | 0 | 0 | Y |
| 61 | 5 | 6 | 1 | 1 | 0 | 0 | 0 | Y |
| 61 | 5 | 9 | 1 | 1 | 0 | 0 | 0 | Y |
| 101 | 3 | 4 | 1 | 1 | 0 | 0 | 0 | Y |
| 101 | 3 | 5 | 1 | 1 | 0 | 0 | 0 | Y |
| 101 | 4 | 5 | 1 | 1 | 0 | 0 | 0 | Y |
| 101 | 4 | 7 | 1 | 1 | 0 | 0 | 0 | Y |
| 101 | 5 | 6 | 1 | 1 | 0 | 0 | 0 | Y |
| 101 | 5 | 9 | 1 | 1 | 0 | 0 | 0 | Y |
| 127 | 3 | 4 | 1 | 1 | 0 | 0 | 0 | Y |
| 127 | 3 | 5 | 1 | 1 | 0 | 0 | 0 | Y |
| 127 | 4 | 5 | 1 | 1 | 0 | 0 | 0 | Y |
| 127 | 4 | 7 | 1 | 1 | 0 | 0 | 0 | Y |
| 127 | 5 | 6 | 1 | 1 | 0 | 0 | 0 | Y |
| 127 | 5 | 9 | 1 | 1 | 0 | 0 | 0 | Y |
| 61 | 3 | 13 | 4 | 2 | 4 | 858 | 2 | Y |
| 61 | 3 | 17 | 5 | 2 | 58 | 2720 | 29 | Y |
| 61 | 3 | 24 | 8 | 4 | 766 | 14168 | 326 | Y |
| 61 | 3 | 30 | 10 | 5 | 3410 | 36540 | 1084 | Y |
| 101 | 3 | 9 | 3 | 2 | 2 | 168 | 1 | Y |
| 101 | 3 | 17 | 5 | 2 | 34 | 2720 | 17 | Y |
| 101 | 4 | 21 | 5 | 2 | 6 | 23940 | 3 | Y |
| 127 | 3 | 16 | 5 | 2 | 2 | 2240 | 1 | Y |
| 127 | 4 | 21 | 5 | 2 | 2 | 23940 | 1 | Y |
| 61 | 4 | 16 | 4 | 2 | 2 | 5460 | 1 | Y |
| 61 | 4 | 21 | 5 | 2 | 58 | 23940 | 29 | Y |

- all rows: packing + disjointness + coll bound hold  
- max observed `max m` = 5

## Link

| item | status |
|---|---|
| multipads disjoint | CLOSED (v69) |
| H gap law | CLOSED (v72) |
| **fibre packing m_h≤⌊t/e⌋** | **CLOSED (v73)** |
| deployed multipad ban / SoftB | OPEN |
| `\|T\|≤H2` | OPEN |

## OPEN

Packing is board-true but not residual-final. Next residual board hit remains:
ban multipads at deployed or SoftB.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v73.py --check
```
