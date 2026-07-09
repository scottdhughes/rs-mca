# KB-MCA Route-D v38: SR enum → e·p under |H| gate + load bound on |H|

Status: `PARTIAL` — **μ_enum SR mark size e·p under |H|≤K_cap** PROVED;
**|H|≤(n/e)L** PROVED; L≤70 / ambient |H|≤2170 still **OPEN**.

## SR enumeration mark (PROVED)

Order Type S side keys by `(r_*, c0U, c0V)` lex. Rank `i ∈ {0..N_S−1}`:

```text
μ_enum = (i mod e,  ⌊i/e⌋)
```

Injective. If `N_S ≤ e·p` then `⌊i/e⌋ < p` ⇒ lands in `[e]×F_p`.

### Under |H|≤K_cap=2170

```text
N_S ≤ 2018100 ≤ e·p
⇒ μ_enum is a size-e·p constructive SR injection
```

Local drop of `c0U` from μ₂ (no global rank) still collides on toys.

## Load bound on |H| (PROVED)

```text
L = max_r  #{ A_SP highs whose cover contains r }
|H_A_SP|  ≤  (n/e) · L
```

Deployed: `|H| ≤ 31·L`. Gate: **`L ≤ 70` ⇒ `|H| ≤ 2170`**.

Optional ledger: `H^{≤R_max}` from multi-tier FM has size ≤K_cap by definition.

## Path

```text
L ≤ 70  (or H thinning)
  ⇒ |H| ≤ 2170
  ⇒ μ_enum : SR → e·p
  ⇒ multi-tier sides
  ⇒ Type D residual M_pad ≤ 2
  ⇒ A_SP ≤ t·p path
```

## Toys

| j | w | free_core | #S | #H | L | (n/e)L | enum inj? | μ₂ inj? | ep local coll? | H≤Kcap? |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 4 | 1 | 1 | 0 | 17 | 13 | 104 | None | None | None | True |
| 5 | 1 | 2 | 86 | 17 | 12 | 96 | True | True | True | True |
| 5 | 2 | 0 | 0 | 110 | 51 | 272 | None | None | None | True |
| 6 | 1 | 3 | 86 | 17 | 11 | 88 | True | True | True | True |
| 6 | 2 | 1 | 0 | 65 | 34 | 181 | None | None | None | True |
| 6 | 3 | -1 | 0 | 30 | 19 | 76 | None | None | None | True |
| 7 | 1 | 4 | 52 | 17 | 10 | 80 | True | True | True | True |
| 7 | 2 | 2 | 2 | 36 | 22 | 117 | True | True | None | True |
| 7 | 3 | 0 | 0 | 13 | 10 | 40 | None | None | None | True |
| 8 | 1 | 5 | 28 | 16 | 9 | 72 | True | True | True | True |
| 8 | 2 | 3 | 2 | 19 | 14 | 74 | True | True | None | True |
| 8 | 3 | 1 | 0 | 5 | 4 | 16 | None | None | None | True |
| 9 | 2 | 4 | 0 | 8 | 6 | 32 | None | None | None | True |
| 9 | 3 | 2 | 0 | 1 | 1 | 4 | None | None | None | True |

Census: enum inj=6/6; max L=51.

## OPEN

1. Prove `L ≤ 70` at deployed A_SP (or accept tier thinning)
2. Prefer local SR mark without global enumeration if possible

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v38.py --check
```
