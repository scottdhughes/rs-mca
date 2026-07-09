# KB-MCA Route-D v11: residual can-core family

Status: `PARTIAL` — residual can-core definitions, multi-mate partition, and
`K_res` criterion **PROVED**; `M_m^{res} <= 1` **OPEN**.

## Objects

```text
R(z)            residual j-supports in Fib_w(z)
C_can(S)        lex core (drop e=w+1 smallest exponents)
C_res(z)        { C_can(S) : S in R(z) }
U_res(z)        |{ u(S) }|  side-prefix count
U_phi(z)        |{ Phi_w(C) : C in C_res }|   (= v7 B2 object)
N_can_prim(z)   |C_res(z)|
M_m^{res,side}  max residual cores per side-prefix u
M_m^{res,phi}   max residual cores per core-prefix b
```

## Routing (PROVED)

```text
N_can_prim  <=  U_res  *  M_m^{res,side}
N_can_prim  <=  U_phi  *  M_m^{res,phi}
M_m^{res,*}  <=  M_m^{max}  (global)
```

## Multi-mate partition (PROVED)

If `C != C'` in `C_res` share `Phi_w`, then exactly one of:

| Class | Geometry | Payment candidate |
|---|---|---|
| (i) Tight | free-1 CS of (w+1)-blocks; clique <= k_tight=18 | top-seam / marked incidence |
| (ii) Partial-plant | some c>=w+1 full fiber on a core (v8 lives here) | planted / partial-factor cell |
| (iii) Coset-free non-tight | no such fiber; |∩| < m-w-1 | remaining wall (null/sparse on toys) |

Maximal terminal plants already non-residual (v10). Partial plants not yet paid.

## Criterion — K_res only (PROVED conditional)

```text
M_m^{res,side} <= K_res  and  U_res <= target/(17 K_res)
    =>  |R| <= target
```

| K_res | U_res atom | log2 |
|---:|---:|---:|
| 1 | 16166878605395467 | 53.84 |
| 10 | 1616687860539546 | 50.52 |

Primary target: **K_res = 1**. Do not import global coset lower bound as K_res.

## Toy residual proxy (aperiodic j-supports)

| p | n | j | w | m | Mm_glob | Mm_res_side | Mm_res_phi | U_res | Ncan | side<=1 | pair classes |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| 17 | 16 | 8 | 2 | 5 | 17 | 7 | 7 | 34 | 49 | False | {'cosetfree_nontight': 940, 'tight': 1789, 'tight_and_plant': 11, 'nontight_plant': 4} |
| 17 | 16 | 8 | 3 | 4 | 4 | 2 | 2 | 5 | 5 | False | {'tight': 9} |
| 17 | 16 | 9 | 2 | 6 | 32 | 10 | 10 | 28 | 42 | False | {'tight': 2714, 'cosetfree_nontight': 1912, 'nontight_plant': 69, 'tight_and_plant': 88} |
| 17 | 16 | 9 | 3 | 5 | 3 | 2 | 2 | 5 | 5 | False | {'tight': 32} |
| 17 | 16 | 10 | 3 | 6 | 5 | 2 | 2 | 4 | 4 | False | {'tight': 42} |
| 17 | 16 | 7 | 2 | 4 | 8 | 5 | 5 | 38 | 42 | False | {'tight': 817, 'cosetfree_nontight': 169} |
| 17 | 16 | 6 | 2 | 3 | 3 | 3 | 3 | 29 | 31 | False | {'tight': 278} |

`routing_ok` required on all enumerated rows. Pair classes count multi-mate
pairs in residual heavy core-prefix fibers (tight / plant / coset-free).

## Impact

| Item | Status |
|---|---|
| Global M_m <= 1 | REFUTED (v8) |
| Residual objects formalized | PROVED (this packet) |
| Multi-mate payment partition | PROVED |
| M_m^{res} <= 1 | OPEN |
| Class (iii) empty in true residual | OPEN |
| U_res / U_phi atom bounds | OPEN |

## Next real math

1. Show class (iii) cannot occur for true first-match residual, **or**
2. Pay (i)+(ii) and bound (iii) size, **or**
3. Prove residual Phi_w injectivity on C_res (K_res=1), **or**
4. Bound U_phi directly (B2).

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v11.py
python3 experimental/scripts/verify_kb_qatom_route_d_v11.py --check
```
