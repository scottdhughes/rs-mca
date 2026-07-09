# KB-MCA Route-D v48: attack on H_* (free-1 multipad high count)

Status: `ATTACK` — **e=2 closed**; unrestricted ★ for e≥3 **refuted** on cyclic
domains; refined **★_D** still OPEN for deployed e≈n′/17.5.

## Proved bounds on H_*

| Bound | Status | Closes H2 at deployed e? |
|---|---|---|
| `|H| ≤ p^{e−1}` | PROVED | only if e=2 (`p≤H2`, `p²>H2`) |
| e=2 ⇒ `|H|≤p≤H2` | PROVED | yes for e=2 sides only |
| e > n/2 ⇒ H_*=0 | PROVED | no (`⌊n′/e⌋=17>1`) |
| `|H| ≤ binom(n,e)/2` | PROVED | no (too large) |

## CAS (Sage + stdlib)

Cyclic domains `n|p−1`:

- **e=2:** `|H|=p` (saturation)
- **e=3:** `|H|=p²` on n=p−1 rows (saturation)
- **large e/n:** H_* can be **0** with `⌊n/e⌋≥2` (n=16,e=5)
- **mid e:** H_* ≫ `⌊n/e⌋` (n=30,e=5,nH=4591)

Because `p² > H2`, unrestricted

```text
H_*(any domain of size A+e, e=3) ≤ H2
```

is **false** (take a cyclic domain of size p−1≈ field).

## Refined open problem ★_D

```text
Ω = D \ C,   |C| = m_c,   D = fixed KB n-point domain ⊂ F_p
H_*^D  =  # free-1 multipad highs among e-subsets of Ω
Need:  H_*^D  ≤  H2   (or co-extension-restricted ≤ H2)
```

Deployed: `e/n' = 0.0570 ≈ 1/17.5`, `⌊n'/e⌋=17`.

This is **not** abstract-domain H_*; co-extension + fixed embedding matter.

## Implications for residual card

```text
v47 reduction under C_unique:
  |H_unt| ≤ N_C · H_*(·)
```

- If H_* is unrestricted ambient on size-n′ domains: **dead for e≥3** (this packet).
- Live path: bound **H_*^D** (D-complements only) or **co-extending** free-1 multipads.

e=2 side case: residual untyped card **PROVED** via `|H|≤p≤H2`.

## Toys / census

- e2 sat p: True
- e3 sat p² cyclic: True
- unrestricted Hstar3 ≤ H2: False
- vanish e=5 n=16 (floor≥2): True
- deployed e: 67472, e/n′: 0.0570

## OPEN

1. ★_D on KB complements (or co-extension-restricted)
2. C_unique theorem (v47)
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v48.py --check
```
