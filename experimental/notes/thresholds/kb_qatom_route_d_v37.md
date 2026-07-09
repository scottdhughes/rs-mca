# KB-MCA Route-D v37: SR e·p² near-miss + multi-tier under |H|≤K_cap

Status: `PARTIAL` — SR mark **μ₂ size e·p²** injective on toys (near-miss);
pure **e·p SR** banked negative; multi-tier **no R-cell if |H|≤K_cap** PROVED.

## SR mark compression

| mark | size | toy inj on Type S? | vs e·p |
|---|---|---|---|
| `(r_*, c0U, c0V)` | n·p² | yes | factor n·p/e |
| **`(r_* mod e, c0U, δ)`** | **e·p²** | **yes (all S rows)** | **factor p** |
| `(r_* mod e, δ)` | e·p | no (large n_S) | target |
| `(r_* mod e, c0U)` | e·p | no | target |
| `(ι, δ)` alone | ⌊n/e⌋·p | no (large n_S) | under budget but collides |

Deployed: e·p² / e·p = p = 2130706433.

## Multi-tier without M-cell (PROVED conditional)

```text
|H_A_SP| ≤ K_cap = 2170
  ⇒ multi-tier FM tags all highs
  ⇒ all A_SP pairs covered (no R-cell)
```

Ambient `|H|≤2170` still OPEN. Toys always have |H|≪K_cap.

## Path to A_SP ≤ t·p

```text
|H| ≤ K_cap
  ⇒ SR-cell cardinality ≪ e·p (v36) + multi-tier sides
  ⇒ only constructive SR e·p (kill factor p in μ₂) remains for SR
Type D residual M_pad ≤ 2 (v35)
```

## Toys

| j | w | free_core | #S keys | #H | H≤Kcap? | μ₂ inj? | (r mod e,δ)? | (ι,δ) S? | all pairs (ι,δ)? | multi-tier covers? |
|---|---|---:|---:|---:|---|---|---|---|---|---|
| 4 | 1 | 1 | 0 | 17 | True | None | None | None | False | True |
| 5 | 1 | 2 | 86 | 17 | True | True | False | False | False | True |
| 5 | 2 | 0 | 0 | 110 | True | None | None | None | False | True |
| 6 | 1 | 3 | 86 | 17 | True | True | False | False | False | True |
| 6 | 2 | 1 | 0 | 65 | True | None | None | None | False | True |
| 6 | 3 | -1 | 0 | 30 | True | None | None | None | False | True |
| 7 | 1 | 4 | 52 | 17 | True | True | False | False | False | True |
| 7 | 2 | 2 | 2 | 36 | True | True | True | True | False | True |
| 7 | 3 | 0 | 0 | 13 | True | None | None | None | False | True |
| 8 | 1 | 5 | 28 | 16 | True | True | False | False | False | True |
| 8 | 2 | 3 | 2 | 19 | True | True | True | True | False | True |
| 8 | 3 | 1 | 0 | 5 | True | None | None | None | False | True |
| 9 | 2 | 4 | 0 | 8 | True | None | None | None | True | True |
| 9 | 3 | 2 | 0 | 1 | True | None | None | None | True | True |

Census: S rows=6; μ₂ inj=6; pure e·p coll rows=4.

## OPEN

1. Remove factor `p` from μ₂ to reach e·p SR mark
2. `|H_A_SP| ≤ 2170` (unlocks multi-tier full-side path)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v37.py --check
```
