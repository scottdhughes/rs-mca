# KB-MCA Route-D v22: multipads = core multi-mates + e·p mark bank

Status: `PARTIAL` — multipad→core multi-mate reduction **PROVED**;
natural e·p CS marks **BANKED NEGATIVE**; deployed M_pad still **OPEN**.

## Main theorem (PROVED)

Multipad cores sharing free-1 CS sides `(U,V)` in one fiber satisfy

```text
Phi_w(C) = Phi_w(C')
```

with `|C|=m_c = j−e = j−w−1`. Proof: v21 bound

```text
deg(Λ_C − Λ_{C'}) ≤ j−2w−2 = m_c − w − 1
```

is exactly depth-`w` multi-mate agreement for monic degree-`m_c` locators.

## free_core dictionary (PROVED)

```text
free_core = m_c − w = j − 2w − 1
```

| free_core | j vs 2w | M_pad |
|---:|---|---|
| ≤ 0 | j ≤ 2w+1 | ≤ 1 (Phi_w determines monic core) |
| = 1 | j = 2w+2 | cores free-1 CS regime |
| ≫ 1 | deployed | open |

Deployed:

```text
m_c        = 913632
free_core  = 846161
j ≤ 2w+1?  = False
t = e      = 67472
e·p = t·p  = 143763024447376
```

## Reduction

```text
M_pad ≥ 2
  ⇒  core multi-mates at (m_c, w)
  +  common free-1 CS e-extension (U,V) into the j-fiber
```

Stricter than raw `M_m(m_c,w)`: joint extension by one CS pair.

## Payment path

```text
M_pad ≤ 1  +  CS pairs → e·p (= t·p)
    ⇒  |A_SP| ≤ t·p
```

## e·p mark bank (BANKED NEGATIVE)

Natural free-1 CS ordered-pair marks of size ≤ `e·p`:

| mark | #pairs | #colliding labels (all) | #pairs M_pad=1 | #colliding (M_pad=1) |
|---|---:|---:|---:|---:|
| `minU_mod_e_c0U` | 22244 | 353 | 8948 | 344 |
| `minU_mod_e_c0V` | 22244 | 338 | 8948 | 335 |
| `minU_mod_e_dc` | 22244 | 349 | 8948 | 346 |
| `minUV_mod_e_c0U` | 22244 | 342 | 8948 | 335 |
| `minUV_mod_e_dc` | 22244 | 332 | 8948 | 330 |
| `minU_mod_e_c0U_xor_c0V` | 22244 | 331 | 8948 | 330 |

Conclusion: **no tested natural e·p-scale mark is injective** on CS ordered
pairs (all fibers or M_pad=1-restricted). Injection proof remains OPEN.

## Toys

| j | w | m_c | free_core | max M_pad | #mp | #CS pairs | core Phi eq? | bound |
|---|---|---:|---:|---:|---:|---:|---|---:|
| 6 | 1 | 4 | 3 | 14 | 904 | 4616 | True | 2 |
| 6 | 2 | 3 | 1 | 2 | 2 | 930 | True | 0 |
| 6 | 3 | 2 | -1 | 1 | 0 | 150 | True | -2 |
| 7 | 1 | 5 | 4 | 17 | 620 | 3666 | True | 3 |
| 7 | 2 | 4 | 2 | 2 | 4 | 598 | True | 1 |
| 7 | 3 | 3 | 0 | 1 | 0 | 68 | True | -1 |
| 8 | 1 | 6 | 5 | 14 | 364 | 2162 | True | 4 |
| 8 | 2 | 5 | 3 | 2 | 2 | 282 | True | 2 |
| 8 | 3 | 4 | 1 | 1 | 0 | 18 | True | 0 |
| 9 | 2 | 6 | 4 | 1 | 0 | 94 | True | 3 |
| 9 | 3 | 5 | 2 | 1 | 0 | 2 | True | 1 |
| 10 | 2 | 7 | 5 | 1 | 0 | 20 | True | 4 |
| 10 | 3 | 6 | 3 | 1 | 0 | 0 | True | 2 |
| 5 | 1 | 3 | 2 | 9 | 972 | 4386 | True | 1 |
| 5 | 2 | 2 | 0 | 1 | 0 | 1090 | True | -1 |
| 4 | 1 | 2 | 1 | 4 | 540 | 3170 | True | 0 |
| 4 | 2 | 1 | -1 | 1 | 0 | 992 | True | -2 |

All multipad events have core Phi_w equal (re-check of theorem).

## OPEN

1. Control core multi-mates of size `m_c` with free_core=`846161` that
   share a CS e-extension (⇒ M_pad)
2. Inject free-1 CS pairs into `e·p` labels (need non-natural / structure-aware mark)

## CAS

- Sage: multipad examples already show tight degree + core Phi equality
- Next: structure of core multi-mates that admit common CS sides
- msolve: joint core-pair + side CS system in small fields

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v22.py --check
```
