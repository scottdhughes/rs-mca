# KB-MCA Route-D residual card — STATUS (v1–v54)

**Branch:** `scott/kb-qatom-route-d` · **PR:** [#423](https://github.com/przchojecki/rs-mca/pull/423)
**Goal:** residual free-1 / A_SP card toward `A_SP ≤ t·p` on KoalaBear MCA `a+=1116048`.
**Does NOT claim** `U ≤ B*` or full MCA close.

Last tip packet: **v54** on `main`; local attack **v55–v57** on `scott/kb-route-d-T-bound` (not yet PR). Verifiers live under
`experimental/scripts/verify_kb_qatom_route_d_v{N}.py` with matching
notes, certificates, and scanner reports.

---

## Deployed constants

| Symbol | Value | Notes |
|---|---:|---|
| `n` | `2^21` | domain size |
| `e = w+1` | `67472` | free-1 side size |
| `m_c` | `913632` | core size |
| `free_core` | `846161` | `m_c − w` |
| `n' = A+e` | `1183520` | complement size / pure-untyped window |
| `⌊n'/e⌋` | `17` | pack ceiling |
| `p` | `2^31−2^24+1` | KoalaBear prime (odd) |
| `H2` | `⌊e·p/(2·31·30)⌋ ≈ 7.73e10` | high budget for M_pad≤2 card |
| `e·p` | `≈ 1.44e14` | pair budget / `t·p` scale |

---

## Live residual reduction (read this first)

```text
pure-untyped residual highs H_unt
    │  C_unique (v53) + N_C = 1
    ▼
|H_unt| = |T|
    │  star at terminal index n'−1 (v54)
    ▼
T = { e-sets U ⊆ I_{n'} : n'−1 ∈ U and U has a free-1 partner on I_{n'} }
    │
    ├─ e=2: |T| ≤ p ≤ H2          CLOSED (v48/v50)
    └─ e>2: need |T| ≤ H2         OPEN  ← sole wall on this path
```

Alternate close (still open): `|R2| ≤ e·p` after SR + H_M (v45–v46).

---

## What is PROVED (high-signal)

| Packet | Result |
|---|---|
| **v25** | Free-1 high families `F_H` pairwise disjoint; `\|F_H\|≤⌊n/e⌋` |
| **v45–v46** | Residual R2 = untyped ⊔ Type D; Type D cores disjoint; card if `\|H_R2\|≤H2` or `\|R2\|≤e·p` |
| **v47** | Untyped pair → unique core (def); reduction draft under C_unique |
| **v48** | `\|H\|≤p^{e−1}`; e=2 ⇒ `≤p≤H2`; unrestricted ★ false for e≥3 (`p²>H2`) |
| **v49** | Coext multipads live in index prefixes `I_t`, `t=min(C)∈[2e,n']` |
| **v51** | **U2e:** ≤1 free-1 bipartition of any 2e-set (char≠2); `H_*^{pre}(t,e)≤C(t,2e)` |
| **v52** | Ambient multipads do **not** obey `t_min_pair≤2e+2` |
| **v53** | **C_unique:** untyped core = terminal block `C_*={n'…n−1}`; `N_C=1`; `\|H_unt\|≤H_*^{pre}(n',e)` |
| **v54** | Pure-untyped = **stars** at `U_*∋n'−1`; `\|H_unt\|=\|T\|≤C(n'−1,e−1)` |

---

## What is REFUTED / banked dead (do not retry)

| Claim | Where |
|---|---|
| Ambient `L≤70` / small ambient cover | v40 |
| `\|H_R2\|≤n`, `≤⌊n/e⌋`, multi-tier confusions | v42–v46 |
| Unrestricted `H_*≤H2` for e≥3 | v48 |
| Ambient multipad `t≤2e+2` | v52 |
| Pack `k=17` alone ⇒ H2 (e=3 toys ~ `p²`) | v54 |
| Free-regime / Mm uniqueness tourism | v8+ |

---

## OPEN (ordered)

1. **Primary:** `|T| ≤ H2` at deployed `(n',e)` — free-1 partner count for e-sets through the terminal index on a length-`n'` roots-of-unity arc.
2. **Alternate:** residual pair budget `|R2| ≤ e·p` without high bound.
3. **Program:** `A_SP ≤ t·p` (needs residual card close).

---

## Packet map (v40–v54)

| v | One-line |
|---:|---|
| 40 | Ambient L≤70 refuted; L_rep≤R_max |
| 41–43 | Overflow / K_cap vs card decoupling; N_ord / \|H\|≤H2 free_core |
| 44 | CAS free-1 growth + R-cell bulk |
| 45–46 | Residual after SR+H_M; R2 untyped vs Type D |
| 47 | Untyped high bound **draft** (superseded in part by v53–v54) |
| 48 | Coeff bound; e=2 close; unrestricted ★ dead for e≥3 |
| 49 | Coext = prefix geometry → ★_pre |
| 50–51 | Bipartitions; **U2e proved** |
| 52 | t-gate census; small-t not ambient law |
| 53 | **C_unique proved**; N_C=1 |
| 54 | **Terminal star**; \|H_unt\|=\|T\|; pack-k not H2 |

Full narrative: `experimental/agents-log.md` (newest first).
Draft still useful for dictionary: `kb_qatom_route_d_v47_untyped_high_bound_draft.md` (C_unique now theorem — see v53).

---

## Reproduce tip packets

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v51.py --check  # U2e
python3 experimental/scripts/verify_kb_qatom_route_d_v53.py --check  # C_unique
python3 experimental/scripts/verify_kb_qatom_route_d_v54.py --check  # star / T
```

Certificates: `experimental/data/certificates/kb-qatom-route-d-v{N}/`.

---

## Next session entry

Attack **`|T|≤H2`**: count/bound free-1 partners of e-sets containing index `n'−1` on the KB roots-of-unity arc of length `n'`, with `e` large and `n'≪p`. Do not restart ambient L / pack-k tourism / unrestricted ★.

---

## Local in progress (not on `main` yet)

**v55** (`scott/kb-route-d-T-bound`): hierarchy for `|T|` proved; e=2 closed; deployed
random-model entropy `log2 E[multipad pairs] ≈ −1.34×10^6` (heuristic empty);
e≥3 toys show `|T|>p` so no cheap `|T|≤p`. Still need algebraic `|T|≤H2` at deployed e.

**v56**: free-1 ⇔ power sums (char>e); φ-fibre multipad dictionary; dense (t∼p)
vs sparse (t≪p) regime — sparse e≥4 empty on toys, e=3 rare hits; deployed is
sparse. OPEN: prove sparse `|T|≤H2`.

**v57**: terminal high injectivity PROVED; |T|<=nH<=coll/2; partner packing;
gap remains bounding coll << p^(e-1) on GP.
