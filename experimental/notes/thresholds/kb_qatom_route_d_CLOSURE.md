# KB-MCA Route-D — CLOSURE BOARD (v67)

**Status:** intermediate lemmas **CLOSED**; residual `|T|≤H2` is **CONDITIONAL**
on `SoftB_Deployed` (**OPEN**).  
**Does NOT claim** `|T|≤H2`, `A_SP≤t·p`, or full MCA close.  
Branch: `scott/kb-route-d-T-bound` (local until PR-worthy).

---

## Deployed constants

| symbol | value |
|---|---:|
| p | 2130706433 |
| n | 2097152 |
| e | 67472 |
| n' | 1183520 |
| H2 | 77291948627 |
| B_\* = √(2 H2) | **393171.6** |
| log2(C²/p^{e-1}) | -1344154.6 |
| incomplete \|G\| bound | 744113.1 |
| Plancherel \|G\| | 50202917.8 |

---

## Primary residual chain

```text
H_unt
  --[C_unique v53]--> |H_unt| = untyped terminal
  --[star v54]------> |H_unt| = |T|
  --[v57]-----------> |T| <= coll/2
  --[v58 Plancherel]-> coll <= C^2/p^{e-1} + B^2
  --[v64 soft-B]----> B <= B_* => coll <= 2 H2 => |T| <= H2
                              ^
                              |
                     SoftB_Deployed  (OPEN)
```

e=2 is **unconditionally CLOSED** (`|T|≤p≤H2`).

---

## CLOSED lemmas (13)

| id | packet | statement |
|---|---|---|
| `C_unique` | v53 | Untyped residual core is the terminal block C_*={n'..n-1}; N_C=1; |H_unt| <= H_*… |
| `terminal_star` | v54 | Pure-untyped highs are stars through n'-1; |H_unt|=|T|. |
| `U2e` | v51 | At most one free-1 bipartition of any 2e-set (char != 2). |
| `e2_T_le_H2` | v48/v50 | For e=2: |T| <= p <= H2 at deployed constants. |
| `terminal_high_injectivity` | v57 | Terminal e-sets have pairwise distinct monic highs; |T| <= nH <= coll/2. |
| `plancherel_coll` | v58 | sum_h m_h^2 = p^{-(e-1)} sum_lambda |S(lambda)|^2; if max_{lambda!=0}|S|<=B then… |
| `G_plancherel` | v59 | max_{a!=0}|G(a)| <= sqrt(p t - t^2) for any t-set. |
| `soft_B_budget` | v64 | If max|S|<=B and B^2 + C^2/p^{e-1} <= 2 H2 then |T|<=H2 (via coll/2 and v57-v58)… |
| `deployed_Bstar_arithmetic` | v64 | At deployed params, log2(C^2/p^{e-1}) ~ -1.34e6 (negligible), so B_*=sqrt(2 H2) … |
| `energy_G4` | v65 | E_+(S) = p^{-1} sum |G|^4; Linf/L2 energy bound. |
| `subgroup_G` | v65 | Full multiplicative subgroup H: |sum_{x in H} psi(a x)| <= sqrt(p)+1 for a!=0. |
| `incomplete_GP_G` | v66 | Prefix length t of order-n GP: |G_t(a)| <= (t/n)(sqrt(p)+1) + sqrt(p)(1+ln n) fo… |
| `e3_lab_structure` | v60-v63 | e=3: high formulas, diagonal All=6S+3D2+D3, triple Fourier, W_inf<=sqrt(pt), Gau… |

---

## CONDITIONAL close

**Hypothesis (`SoftB_Deployed`):**  
Let S(lambda) be the free-1 monic high exponential sum over e-subsets of the length-n'=1183520 GP prefix of mu_n in F_p (p=2130706433, e=67472). Then max_{lambda != 0} |S(lambda)| <= B_* with B_* = sqrt(2 H2) = 393171.5875467097.

**Conclusion:** |T| <= H2 = 77291948627 at deployed parameters

**Proof chain:**  
- v53 C_unique: |H_unt| = untyped residual high count
- v54 star: |H_unt| = |T|
- v57: |T| <= coll/2
- v58: coll <= C^2/p^{e-1} + B^2 under max|S|<=B
- v64: C^2/p^{e-1} negligible; B=B_* => coll <= 2 H2 => |T|<=H2

**Does not imply:** A_SP <= t*p (needs residual card fully into A_SP pipeline), U <= B* / full MCA close

---

## OPEN (3)

| id | pri | statement |
|---|---|---|
| `SoftB_Deployed` | P1 | Let S(lambda) be the free-1 monic high exponential sum over e-subsets of the length-n'=118… |
| `R2_pair_budget` | P2 | |R2| <= e*p alternate residual close (v45-v46 path). |
| `A_SP_le_tp` | P3 | A_SP <= t*p on deployed MCA (program goal; needs residual). |

---

## Packet integrity scan

| packet | status | claims |
|---|---|---|
| v51 | `U2E_PROVED_LARGE_T_OPEN` | 4 true / 3 false |
| v53 | `C_UNIQUE_PROVED` | 6 true / 2 false |
| v54 | `STAR_PROVED_H2_OPEN` | 5 true / 2 false |
| v57 | `INJECTIVITY_PROVED_BOUND_OPEN` | 4 true / 2 false |
| v58 | `FOURIER_PROVED_SQRT_CANCEL_OPEN` | 4 true / 3 false |
| v59 | `G_PLANCHEREL_PROVED_SQRT_CANCEL_OPEN` | 3 true / 4 false |
| v64 | `PHASE_CS_SOFTB_PROVED_DEPLOYED_BSTAR_OPEN` | 5 true / 4 false |
| v65 | `ENERGY_SUBGROUP_PROVED_INCOMPLETE_SOFTB_OPEN` | 5 true / 4 false |
| v66 | `INCOMPLETE_G_PROVED_SOFTB_S_OPEN` | 5 true / 3 false |

All scanned packets: **no false claim** of `|T|≤H2` or `A_SP≤t·p`.

---

## Path to completion

1. **Preferred:** ban multipads on `{0..n'−1}` (or SoftB).  
   - CLOSED: packing; `t≤2e` inj; span≥2e; **coll ≤ min((K−1)C, 2 C(t,2e))**.  
   - OPEN residual: coll→0 / SoftB ⇒ `|T|≤H2`.  
2. **PR policy:** only frozen CLOSED board rows.  
3. A_SP only after `|T|≤H2`.  
4. Lean phase 1 done; phase 2 + [AXLE](https://axle.axiommath.ai/v1/docs/).

### Lean roadmap

- Package: `experimental/lean/route_d_residual/`
- Toolchain: `leanprover/lean4:v4.31.0 (match rs_mca_formalization)`
- Phase 1: Deployed constants as Nat (p,n,e,n',H2), B_star_sq = 2 * H2 exact Nat inequality certificates, ProofStatus + ClosureNode records, ConditionalClose Prop (SoftB -> T_le_H2) as statement only
- Phase 2: Finite field F_p, mu_n, incomplete GP G-bound, Plancherel on F_p^{e-1}, C_unique / star combinatorics on index sets, SoftB_Deployed proof or certified bound
- Policy: No sorry in phase-1 arithmetic. SoftB remains an open Prop until proved; do not mark residual CLOSED in Lean until SoftB lands.

---

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v67_closure_board.py --check
# optional deep re-check of tip packets:
python3 experimental/scripts/verify_kb_qatom_route_d_v66.py --check
python3 experimental/scripts/verify_kb_qatom_route_d_v64.py --check
```

Lean (phase 1):

```bash
cd experimental/lean/route_d_residual && lake build
```
