# KB-MCA Route-D residual card — STATUS (v1–v54)

**Branch:** `scott/kb-qatom-route-d` · **PR:** [#423](https://github.com/przchojecki/rs-mca/pull/423)
**Goal:** residual free-1 / A_SP card toward `A_SP ≤ t·p` on KoalaBear MCA `a+=1116048`.
**Does NOT claim** `U ≤ B*` or full MCA close.

Last tip packet: **v54** on `main`; local attack **v55–v70** on `scott/kb-route-d-T-bound` (not yet PR). Verifiers live under
`experimental/scripts/verify_kb_qatom_route_d_v{N}.py` with matching
notes, certificates, and scanner reports.

**Closure board:** `experimental/notes/thresholds/kb_qatom_route_d_CLOSURE.md`
(+ JSON `kb-qatom-route-d-v67`, Lean phase-1 `experimental/lean/route_d_residual/`).

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

**Primary:** ban sparse multipad G=P_e*H on {0..n'-1} (v70). t<2e inj CLOSED;
n'>=2e. Fallback SoftB. Lean phase-1 + Mathlib/AXLE map. No ambient L/pack-k.

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

**v58**: Plancherel coll identity; coll <= C^2/p^(e-1)+B^2; sqrt-cancel => T=0 deployed (conditional). OPEN: prove |S|<=sqrt(C).

**v59**: Plancherel max|G|<=sqrt(pt-t^2) PROVED; e=2 S from G; that bound does not yield sqrt-cancel when t<<p. Full F_p^*: |S|=1.

**v60**: e=3 S reduced to W_inf (quadratic Weyl on arc); |S|<=(1/6)(sqrt(p)W^3+O(t^2)) PROVED but weak. OPEN: sharp W_inf.

**v61**: W_inf <= sqrt(p t) PROVED (per-A Plancherel, any t-set). e=3 envelope
|S|<=(1/6)(p^2 t^{3/2}+O(t^2)) PROVED and **structurally dead** for √-cancel
(factor ~ p^2/sqrt(6)). OPEN: oscillatory cancel in triple Fourier
All = p^{-1} sum hatH(-xi) hat_mu(xi)^3.

**v62**: Gauss |hatH|=sqrt(p) flat PROVED; refined |All|<=sqrt(p) t W_inf
<= p t^{3/2} (factor ~sqrt(p/t) better than v61 in sparse). Still weak for
√-cancel (factor ~ p/sqrt(6)). OPEN: phase of hat_mu^3 vs hatH.

**v63**: Bilinear factorization All = sum_{i,j} psi(K) G(alpha) PROVED;
|All|<=sum r2|G|<=t^2(1+M) PROVED (beats v62 iff t<<sqrt(p); deployed
t/sqrt(p)~25 so v62 tighter). Fourth-moment = additive energy of highs
PROVED; L2 RMS sits at sqrt(C) when injective. OPEN: oscillatory bilinear
sum (keep phases of K and G).

**v64**: Level-set All = sum_s psi(-l0 s) f(s) G(beta(s)) PROVED;
CS |All|<=sqrt(sum|f|^2) sqrt(p t) PROVED; phased energy <= E_+(S).
**Deployed soft-B bar clarified:** C^2/p^{e-1} has log2~-1.34e6 (~0), so
B_*=sqrt(2 H2)~3.93e5 suffices for |T|<=H2 via v58. e=3 |S|<=sqrt(C) is a
method template, not the deployed numerical target. OPEN: max|S|<=B_* at
deployed (n',e).

**v65**: E_+=p^{-1} sum|G|^4 PROVED; Linf/L2 energy bound PROVED; multiplicative
subgroup |G|<=sqrt(p)+1 PROVED (Gauss chars). Deployed arc is incomplete
prefix n'<n of mu_n — subgroup law not automatic. CAS incomplete still
Gmax<=sqrt(p)+1 on toys. OPEN: incomplete GP |G|; soft-B max|S|<=B_*.

**v66**: Incomplete GP bound PROVED:
|G_t(a)| <= (t/n)(sqrt(p)+1) + sqrt(p)(1+ln n) for a!=0
(Dirichlet completion + mixed Gauss J). Deployed |G| <= ~7.44e5
(~67x better than Plancherel ~5e7; ~1.9x B_*). OPEN: soft-B max|S|<=B_*
for free-1 highs (linear G is not S).

**v67**: Master **closure board** — 13 CLOSED intermediate lemmas; CONDITIONAL
`SoftB_Deployed => |T|<=H2`; primary OPEN SoftB; packet integrity scan (no
false full-close). Lean phase-1 `route_d_residual` builds (constants + B*
arithmetic + ledger). Honest: full residual NOT closed.

**v68**: Injectivity path: free-1 high injective => coll=0 => |T|=0 PROVED.
S=e_e(u) identity PROVED; multipad monic poly criterion PROVED; deployed
pigeonhole room + random E[coll]~0 certified. CAS sparse e=4 injective.
OPEN: deployed injectivity (preferred) or SoftB.

**v69**: Multipads always disjoint (root/delta argument) PROVED; same derivative;
**t<2e => injectivity => |T|=0** PROVED. GP index form p_k=sum omega^{ak}.
Deployed n'>=2e so threshold misses; OPEN: no GP multipad on {0..n'-1}.

**v70**: Multipad index poly G(X)=sum_A X^a-sum_B X^b vanishes at omega^k
(k=0..e-1); P_e|G in F_p[X]; deg window [e,t-1]; support 2e. Mathlib map
(AddChar/GaussSum/GeomSum/Cyclotomic) + AXLE docs for phase-2. OPEN: ban
sparse G=P_e*H at deployed.
