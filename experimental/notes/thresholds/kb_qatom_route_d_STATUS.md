# KB-MCA Route-D residual card — STATUS (v1–v54)

**Goal:** residual free-1 / A_SP card toward `A_SP ≤ t·p` on KoalaBear MCA `a+=1116048`.  
**Does NOT claim** `U ≤ B*` or full MCA close.

**Integration (2026-07-09):** PR [#423](https://github.com/przchojecki/rs-mca/pull/423) was **closed without merge**.
Upstream `main` (`84b393e`) manually integrated **selected high-signal packets** only:
`v25, v45, v46, v48, v49, v51, v53, v54` + this STATUS note.
Full v1–v54 archive remains on fork branch `scottdhughes/scott/kb-qatom-route-d`
(intermediate packets intentionally not promoted).

Last tip packet: **v54**. Verifiers:
`experimental/scripts/verify_kb_qatom_route_d_v{N}.py` with matching notes/certs.

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

| Packet | On `main`? | Result |
|---|---|---|
| **v25** | yes | Free-1 high families `F_H` pairwise disjoint; `|F_H|≤⌊n/e⌋` |
| **v45–v46** | yes | Residual R2 = untyped ⊔ Type D; Type D cores disjoint; card if `|H_R2|≤H2` or `|R2|≤e·p` |
| **v47** | no (draft) | Untyped pair → unique core (def); superseded in part by v53–v54 |
| **v48** | yes | `|H|≤p^{e−1}`; e=2 ⇒ `≤p≤H2`; unrestricted ★ false for e≥3 |
| **v49** | yes | Coext multipads live in index prefixes `I_t`, `t=min(C)∈[2e,n']` |
| **v51** | yes | **U2e:** ≤1 free-1 bipartition of any 2e-set (char≠2); `H_*^{pre}≤C(t,2e)` |
| **v52** | no | Ambient multipads do **not** obey `t_min_pair≤2e+2` |
| **v53** | yes | **C_unique:** untyped core = terminal block `C_*`; `N_C=1` |
| **v54** | yes | Pure-untyped = **stars** at `U_*∋n'−1`; `|H_unt|=|T|` |

---

## What is REFUTED / banked dead (do not retry)

| Claim | Where |
|---|---|
| Ambient `L≤70` / small ambient cover | v40 |
| `|H_R2|≤n`, `≤⌊n/e⌋`, multi-tier confusions | v42–v46 |
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

| v | On `main`? | One-line |
|---:|---|---|
| 40 | no | Ambient L≤70 refuted; L_rep≤R_max |
| 41–43 | no | Overflow / K_cap vs card decoupling |
| 44 | no | CAS free-1 growth + R-cell bulk |
| 45–46 | **yes** | Residual after SR+H_M; R2 untyped vs Type D |
| 47 | no | Untyped high bound draft (superseded in part) |
| 48 | **yes** | Coeff bound; e=2 close; unrestricted ★ dead for e≥3 |
| 49 | **yes** | Coext = prefix geometry → ★_pre |
| 50–51 | 50 no / **51 yes** | Bipartitions; **U2e proved** |
| 52 | no | t-gate census; small-t not ambient law |
| 53 | **yes** | **C_unique proved**; N_C=1 |
| 54 | **yes** | **Terminal star**; `|H_unt|=|T|`; pack-k not H2 |

Full narrative: `experimental/agents-log.md` (upstream has the integration entry;
fork branch keeps the full v1–v54 packet log).  
Dictionary draft: `kb_qatom_route_d_v47_untyped_high_bound_draft.md` (fork only;
C_unique is now a theorem — see v53).

---

## Reproduce tip packets (on `main`)

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v51.py --check  # U2e
python3 experimental/scripts/verify_kb_qatom_route_d_v53.py --check  # C_unique
python3 experimental/scripts/verify_kb_qatom_route_d_v54.py --check  # star / T
```

Certificates: `experimental/data/certificates/kb-qatom-route-d-v{N}/`.

---

## Next session entry

Attack **`|T|≤H2`**: count/bound free-1 partners of e-sets containing index `n'−1` on the KB roots-of-unity arc of length `n'`, with `e` large and `n'≪p`. Work from **upstream `main`** (not the closed PR branch). Do not restart ambient L / pack-k tourism / unrestricted ★.
