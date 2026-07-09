# KB-MCA Route-D v60: e=3 free-1 high sums — triple Fourier reduction

Status: **e=3 structural reduction PROVED**; sharp `|S|<=√C` still **OPEN**.
Local on `scott/kb-route-d-T-bound`.

## Setup

Free-1 monic high for three arc values `u,v,w` (char != 2):

```text
h0 = -(u+v+w)
h1 = uv+uw+vw = ((u+v+w)^2 - (u^2+v^2+w^2))/2
S(l0,l1) = sum_{i<j<k < t} psi(l0 h0 + l1 h1)
```

## Diagonal identity (PROVED)

```text
All = 6 S + 3 D2 + D3
|S| <= (1/6)( |All| + 3 t(t-1) + t )
```

## Triple Fourier (PROVED, l1 != 0)

```text
All = sum_s H(s) (mu * mu * mu)(s)
H(s) = psi((l1/2) s^2 - l0 s)
mu   = sum_{i<t} psi((-l1/2) v_i^2)  delta_{v_i}
```

## All bound by quadratic Weyl (PROVED)

```text
W_inf = max_{A,B} |sum_{i<t} psi(A v_i^2 + B v_i)|
|All| <= sqrt(p) * W_inf^3
|S|   <= (1/6)( sqrt(p) W_inf^3 + 3t(t-1)+t )
```

## CAS

| p | t | max|S| | bound | √C | S/√C | W_inf |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 15 | 60.0 | 4.5e+03 | 21.3 | 2.81 | 15.0 |
| 61 | 24 | 97.0 | 1.8e+04 | 45.0 | 2.16 | 24.0 |
| 61 | 36 | 175.5 | 6.1e+04 | 84.5 | 2.08 | 36.0 |
| 101 | 15 | 57.2 | 5.8e+03 | 21.3 | 2.68 | 15.0 |
| 101 | 24 | 136.2 | 2.3e+04 | 45.0 | 3.03 | 24.0 |
| 101 | 36 | 221.0 | 7.9e+04 | 84.5 | 2.62 | 36.0 |
| 127 | 15 | 69.8 | 6.4e+03 | 21.3 | 3.27 | 15.0 |
| 127 | 24 | 127.1 | 2.6e+04 | 45.0 | 2.83 | 24.0 |
| 127 | 36 | 221.8 | 8.8e+04 | 84.5 | 2.63 | 36.0 |

- Identities hold (diag/Fourier err ~ 1e-12).  
- Bound holds but **bound/√C ~ 1045** (too weak for √-cancel).  
- Empirical S/√C max = 3.27.  
- W_inf/√(pt) max = 0.77 (suggests W_inf = O(√(pt))).

## Link to residual card

v58: `|S|<=√C` ⇒ `coll <= C^2/p^{e-1}` ⇒ `T=0` at deployed.  
v60 reduces e=3 `|S|` to **W_inf** but the proved estimate is not yet ≤√C.

Deployed e=67472 ≫ 3 needs a general-e lift after e=3 is sharp.

## OPEN

1. Prove `W_inf <= sqrt(p t)` (or better) for quadratic phases on GP arcs.  
2. Sharpen `|All|` beyond `sqrt(p) W_inf^3` (e.g. using Gauss structure of hatH).  
3. Reach `|S|<=√C` sparsely for e=3, then generalize e.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v60.py --check
```
