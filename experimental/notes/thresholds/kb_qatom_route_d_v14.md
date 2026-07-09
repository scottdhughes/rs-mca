# KB-MCA Route-D v14: residual mass re-anchor

Status: `PARTIAL` — mass criteria + bridges **PROVED**; residual injection / atom **OPEN**.

## North star (on track)

Ledger residual mass at `a+ = 1116048`:

```text
max |R(z)|  ≤  TARGET  =  274836936291722953
```

or any equivalent E1/E2/E5 / N_can / (U_res,M_m^{res}) form below.

Multi-mate geometry (v8–v13) is **support structure**, not a substitute for mass.

## Sufficient budgets (PROVED arithmetic)

| Criterion | Bound | Fits TARGET? |
|---|---|---|
| N_can ≤ TARGET/17 | 16166878605395467 | pack atom |
| N_can ≤ n·p | 4468415257378816 (log2≈51.99) | yes (≤ TARGET/17) |
| N_can ≤ t·p | 143763024447376 | yes |
| N_can ≤ t | 67472 | => |R| ≤ t·p via p-cover |
| |R| ≤ n·p (E5) | 4468415257378816 | yes |
| |R| ≤ t·p (E2) | 143763024447376 | yes |

```text
17 · n · p  =  75963059375439872  ≤  TARGET
17 · t · p  =  2443971415605392  ≤  TARGET
```

## Dualities (PROVED)

```text
R  injects into  C_res x F_p     (lex: S |-> (C_can, c_U))
|R|  <=  p * N_can_prim
N_can_prim  <=  |R|
N_can_prim  <=  U_res * M_m^{res,side}
N_can_prim  <=  U_phi * M_m^{res,phi}
```

## Injection bridges (PROVED as reductions)

- Support injection |R|<=B (E2/E5) => mass.
- Core injection N_can<=B => pack/p-cover mass via budgets above.
- M_m^{res,phi}<=1 => N_can=U_phi; need U_phi<=TARGET/17.

## OPEN_RES_MASS

Prove **one** ledger-residual bound among (i)–(v) in the certificate JSON
(`OPEN_RES_MASS`). Falsifier: residual leaf with mass above TARGET / above the
claimed injection budget.

### Do not

- Re-prove global M_m≤1
- Treat aperiodic toys as ledger residual
- Continue multi-mate taxonomy without mass

## Toy bank (aperiodic proxy only)

Lex dual injective on residual proxy. Naive core marks not injective:

| j | m | w | |R| | N_can | max(min,Phi) | max(min,c0) | max(minS,cU) | lex OK |
|---|---|---|---:|---:|---:|---:|---:|---|
| 9 | 6 | 2 | 11440 | 1716 | 6 | 52 | 1716 | True |
| 7 | 4 | 2 | 11440 | 715 | 3 | 15 | 826 | True |
| 10 | 6 | 3 | 7952 | 923 | 2 | 33 | 922 | True |
| 9 | 5 | 3 | 11440 | 792 | 2 | 24 | 842 | True |
| 6 | 3 | 2 | 7952 | 286 | 1 | 6 | 388 | True |

## Next real math

1. **Ledger** residual support injection into `D x F_p` or `[t] x F_p` (E5/E2), or
2. Residual can-core injection with |L| <= n*p or TARGET/17, or
3. M_m^{res}<=1 plus U_phi (or U_res) atom bound,

using first-match structure (marked incidence, paid cells), not proxy alone.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v14.py
python3 experimental/scripts/verify_kb_qatom_route_d_v14.py --check
```
