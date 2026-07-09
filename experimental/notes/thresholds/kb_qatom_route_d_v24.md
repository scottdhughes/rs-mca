# KB-MCA Route-D v24: Newton multi-mates + (U,δ) reduction

Status: `PARTIAL` — structure-aware CS-pair injection **PROVED**; free_core=1
fiber automatic (**CAS**); deployed multipad / e-set→[e] still **OPEN**.

## Product identity (PROVED)

```text
(Λ_C − Λ_{C'}) · Λ_U  =  Λ_{C∪U} − Λ_{C'∪U}
```

## Newton multi-mate form (PROVED, p > m_c)

```text
Phi_w(C)=Phi_w(C')  ⇔  p_k(C)=p_k(C') for k=1..w
```

Deployed: `p=2130706433 > m_c=913632` = True.

Multipad cores = depth-w **power-sum multi-mates** of size `m_c` that jointly
avoid a free-1 CS e-pair in the common complement.

## free_core=1 fiber automatic (PROVED + CAS)

At free_core=1 (`m_c=e=w+1`, `j=2w+2`):

```text
Λ_{C∪U} − Λ_{C'∪U} = c · Λ_U ,   deg = e = j−w−1
```

Phi_w fiber room is exactly met ⇒ same-fiber is free. Obstruction = fully-split
+ joint avoidance only.

CAS (Sage): `PASS` — OK
[{'w': 1, 'm': 2, 'j': 4, 'dC_ok': True, 'dS_ok': True, 'room': 2, 'auto': True}, {'w': 2, 'm': 3, 'j': 6, 'dC_ok': True, 'dS_ok': True, 'room': 3, 'auto': True}, {'w': 3, 'm': 4, 'j': 8, 'dC_ok': True, 'dS_ok': True, 'room': 4, 'auto': True}, {'w': 4, 'm': 5, 'j': 10, 'dC_ok': True, 'dS_ok': True, 'room': 5, 'auto': True}]

## Structure-aware mark (PROVED)

```text
ψ(U,V) = (U, δ),   δ = c0(U)−c0(V) ∈ F_p^×
```

injects free-1 CS ordered pairs into `FS_1(e) × F_p^×`.

### Payment reduction (PROVED)

```text
M_pad ≤ 1  and  residual FS_1(e) ↪ [e]
    ⇒  (U,V) ↦ (ι(U), δ) injects into e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

Deployed `e·p = 143763024447376`.

### Mark bank

| mark | #pairs | #colliding labels | inj rows |
|---|---:|---:|---|
| `U_delta` | 1528 | 0 | 12/12 |
| `sumU_mod_e_delta` | 1528 | 241 | 3/12 |
| `minU_mod_e_delta` | 1528 | 247 | 1/12 |
| `prodU_mod_e_delta` | 1528 | 252 | 1/12 |
| `high0_mod_e_delta` | 1528 | 246 | 1/12 |

`U_delta` injective (proved); e-index×δ marks still collide.

## Toys

| j | w | free_core | max M_pad | #mp | #CS pairs | prod id? | newton? | U_δ inj? | sumU mod e ×δ? |
|---|---|---:|---:|---:|---:|---|---|---|---|
| 4 | 1 | 1 | 4 | 540 | 400 | True | True | True | False |
| 5 | 1 | 2 | 9 | 972 | 286 | True | True | True | False |
| 5 | 2 | 0 | 1 | 0 | 260 | None | None | True | False |
| 6 | 1 | 3 | 14 | 904 | 200 | True | True | True | False |
| 6 | 2 | 1 | 2 | 2 | 146 | True | True | True | False |
| 6 | 3 | -1 | 1 | 0 | 60 | None | None | True | False |
| 7 | 2 | 2 | 2 | 4 | 80 | True | True | True | False |
| 7 | 3 | 0 | 1 | 0 | 26 | None | None | True | False |
| 8 | 2 | 3 | 2 | 2 | 42 | True | True | True | False |
| 8 | 3 | 1 | 1 | 0 | 10 | None | None | True | True |
| 9 | 2 | 4 | 1 | 0 | 16 | None | None | True | True |
| 9 | 3 | 2 | 1 | 0 | 2 | None | None | True | True |

Product checks: 16044/16044; Newton:
16044/16044.

## OPEN

1. Bound free_core=`846161` power-sum multi-mates with joint complement CS-extension
2. Inject residual free-1 fully-split e-sets into `[e]`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v24.py --check
```
