# KB-MCA Route-D v77: residual criterion (multipad-free ⇒ `|T|=0`)

Status: **residual close criterion PROVED**; deployed multipad-free still **OPEN**.  
This is the board target for a residual PR. Local on `scott/kb-route-d-T-bound`.

## BOARD: residual close criterion (PROVED)

```text
no free-1 multipad on GP arc of length n'
        ⇒  coll = 0
        ⇒  |T| = 0  ≤ H2
```

| path | status |
|---|---|
| **Primary: multipad-free / injective high** | criterion PROVED; hypothesis OPEN |
| Alternate: SoftB `max\|S\|≤B_*` | criterion PROVED (v64); hypothesis likely hard |

### Why SoftB is alternate

e=3 CAS: `max|S|/√C ~ 2–3`. SoftB needs `|S|≤B_*≈3.93×10^5`.  
At large `C`, `√C ≫ B_*`, so SoftB is much stronger than empirical square-root scale.  
Random-model `E[coll]~0` supports **injectivity**, not SoftB.

Deployed: `log2 E[coll] ≈ -1344154.6` (expected multipad-free).

## Multipad two-value form (PROVED)

```text
phi(X) = X * m1(X)   (monic deg e, phi(0)=0)
phi takes exactly two values on the 2e root-values, each e times
```

## CAS (e=3)

| p | t | max\|S\| | √C | S/√C | coll |
|---|---:|---:|---:|---:|---:|
| 61 | 12 | 41.0 | 14.8 | 2.77 | 0 |
| 61 | 17 | 69.7 | 26.1 | 2.67 | 58 |
| 61 | 24 | 97.0 | 45.0 | 2.16 | 766 |
| 101 | 15 | 57.2 | 21.3 | 2.68 | 22 |
| 101 | 20 | 99.4 | 33.8 | 2.94 | 72 |
| 127 | 18 | 90.4 | 28.6 | 3.16 | 10 |

max S/√C = 3.16; two-value form OK on multipad samples.

## Infrastructure (already CLOSED)

t≤2e inj · packing · span≥2e · coll≤min((K−1)C, 2 C(t,2e)) · P_e algebra

## OPEN — residual PR

Prove **multipad-free** on the deployed GP prefix (length n', e=67472).

Then ship residual PR: `|T|≤H2`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v77.py --check
```
