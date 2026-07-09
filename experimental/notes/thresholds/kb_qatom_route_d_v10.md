# KB-MCA Route-D v10: residual M_m law

Status: `PARTIAL` — residual routing + partial-plant gap **PROVED**; residual
atom upper bound **OPEN**. Global uniqueness remains **REFUTED** (v8).

## Main message

```text
Global M_m >= 10  (v8 coset pads)
     does NOT force
Residual M_m^res >= 10
```

Routing for the atom uses **residual** can-cores only. The residual criterion
may still close with `K_res = 1`.

## Theorems

### 1 — Residual routing (PROVED)

```text
N_can_prim(z)  <=  U_res(z) * M_m^res(z)
M_m^res(z)     <=  M_m^max   (global)
```

`M_m^res` = max number of residual can-cores in one side-prefix block
(each block sits in one m-subset `Phi_w` fiber).

### 2 — Residual atom criterion (PROVED conditional)

```text
M_m^res <= K_res  and  U_res <= target/(17 K_res)
    =>  |R| <= target
```

| K_res | U_res atom budget | log2 |
|---:|---:|---:|
| 1 | 16166878605395467 | 53.84 |
| 10 | 1616687860539546 | 50.52 |

### 3 — Maximal terminal planted is non-residual (PROVED)

For terminal `c in {65536,131072}`, maximal c-quotient/planted j-supports
(`|Q|=floor(j/c)`, `|P|=j mod c`) are first-match assigned (Q0 raw-paid) and
lie outside `R(z)`.

Deployed: `j mod 131072 = 63600 <= w` (descent applies).

### 4 — Partial single-fiber plant gap (PROVED)

v8 mates are m-sets `R cup U` with **one** full `c=2^17` fiber:

```text
|Q| = 1  <  floor(m/c) = 6
m mod c = 127200 > w
```

These are **not** maximal planted. Residual definition does **not** automatically
delete `|Q|=1` supports. Branch 5 (non-maximal planted) is not a proved payment.

### 5 — Fiber-factor extraction (PROVED)

Every support has a unique maximal decomposition `S = P sqcup pi_c^{-1}(Q)`
with `P` fiber-free.

### 6 — Global lower != residual lower (PROVED)

Logical separation: residual atom with `K_res=1` is compatible with v8.

## Toy evidence

Heaviest m-subset `Phi_w` fibers are often **entirely free** of full e0-coset
factors. Aperiodic residual proxy and `|Q|=0` filters often **do not** reduce
`M_m`. Large fibers are not "just coset pads."

| p | n | m | w | Mm | Mm_ap | Mm_Q=0 | heavy with fiber | k_coset | heavy coset-free |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 17 | 16 | 6 | 2 | 32 | 32 | 32 | 0/32 | 3 | True |
| 17 | 16 | 6 | 3 | 5 | 4 | 5 | 0/5 | 3 | True |
| 17 | 16 | 5 | 2 | 17 | 17 | 17 | 0/17 | 3 | True |
| 17 | 16 | 4 | 2 | 8 | 8 | 8 | 0/8 | 4 | True |
| 17 | 16 | 10 | 4 | 2 | 2 | 2 | 0/2 | 1 | True |
| 17 | 16 | 8 | 5 | 2 | 1 | 1 | 2/2 | 2 | False |
| 17 | 16 | 7 | 3 | 5 | 5 | 5 | 0/5 | 3 | True |
| 17 | 16 | 9 | 4 | 2 | 2 | 2 | 0/2 | 1 | True |
| 17 | 16 | 8 | 6 | 2 | 1 | 1 | 2/2 | 2 | False |

Partial-pad check (`n=16,e0=2,m=6,w=1`): Phi match=True,
Q counts=[1, 1], qmax=3 (partial).

## Impact

| Claim | Status |
|---|---|
| Global `M_m <= 1` | REFUTED (v8) |
| Residual must use `K_res >= 10` | **FALSE** (this packet) |
| `M_m^res <= 1` | OPEN |
| `U_res` atom budget | OPEN |
| B2 residual core-prefix image | OPEN |

## Next real math

1. Prove `M_m^res <= 1` (or small `K_res`) by residual geometry, **or**
2. Pay partial single-fiber / non-tight collision cells in first-match, **or**
3. Bound residual can-core `Phi_w`-image (B2) with no Mm premise.

Do not set residual `K` from the global coset lower bound alone.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v10.py
python3 experimental/scripts/verify_kb_qatom_route_d_v10.py --check
```
