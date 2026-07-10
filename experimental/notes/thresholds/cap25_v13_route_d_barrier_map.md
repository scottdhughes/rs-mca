# CAP25 v13 Route-D shared barrier map

Status: `SYNTHESIS` / `REFERENCE` / `AUDIT`. This packet claims **no** new
mathematics. It composes the field's integrated Route-D state at the two deployed
rows into a single obstruction map: every node and every proved edge is a
citation to an in-tree file at base `84b393e`. The one non-cited section
(SPECULATIVE EDGES) is fenced and labelled `ANALYSIS-CONJECTURAL`.

**Map + verifier.**
`experimental/data/cap25_v13_route_d_barrier_map.json` (machine-readable ledger)
and `experimental/scripts/verify_route_d_barrier_map.py` (zero-arg, stdlib-only,
`RDMAP_AS_CAP_GB` / `RDMAP_DATA_DIR` knobs; gates file-existence, quote
substrings, constant tokens, edge-DAG, count agreement, and the
proved/speculative fence, plus six tamper self-tests; `RESULT: PASS`, `< 30 s`).

## What this is / is not (merge framing)

This is **a provenance-gated map of the integrated Route-D state at the two
deployed rows — no closure claimed, no new bounds, no row-sharp Q claim.** Its
value is getting the implication structure exactly right and exhaustively
sourced across all five contributor lineages. It:

- does **not** close `prob:row-sharp-q` (`grande_finale.tex` L2177) or
  `def:q-row-atom` (L2043);
- proves **no** deployed safe row — there is no `U(a_+) <= B^*` certificate here;
- derives nothing new: the map is a citation graph, and the only analytical
  content (three speculative edges) is fenced `ANALYSIS-CONJECTURAL`;
- reflects the tree at `84b393e` and **decays as new work lands** — the node and
  edge set is a snapshot, not a standing theorem.

Collaborative credit, by lineage: **scottdhughes** (KB-MCA Route-D residual
free-1 / A_SP card, curated by the maintainer from PR #423 — the eight integrated
packets v25/45/46/48/49/51/53/54 and the standing-wall STATUS index);
**avdeevvadim** (singleton-heavy top-seam Route-D compiler, PR #425);
**DannyExperiments** (M31 moment-order floor + Chebyshev fixed-remainder floor +
the c=1024 paired-prefix follow-up, PRs #424/#426); **holmbuar** (the row-sharp Q
Fourier lineage: #407 kappa, #412 p^{w/2} floor, #414/#416 participation ratio,
#417 lift-class refutation, the KB/M31 rung audits); **AllenGrahamHart** (#405
independent row-sharp Q calibration, cited as consistency context in #407); and
the **maintainer** (the grande_finale.tex steering objects, and the curation note
that assembled the scottdhughes packets from PR #423).

## Deployed rows and steering objects (`grande_finale.tex`, quoted with lines)

- `def:q-row-atom` (L2043): `R_Q^max = |B|^w max_z |P_Q(z)| / C(n,a_+) <= 2^{Δ_Q}`;
  equivalently `max_z |P_Q(z)| <= B*`. **The missing theorem.**
- `prob:row-sharp-q` (L2177): `max_z |P_Q(z)| <= R_Q^row · C(n,a_+) |B|^{-(a_+-K)}`.
- `prop:q-exact-target` (L2061): budgets `B*_KB = 274980728111395087` (L2067),
  `B*_M31 = 16777215` (L2069–2070); ratios `4807520.9295 / 4226236.5253 /
  9.5722 / 8.4152` — **the binding Q problem is the Mersenne-31 list row** (~8.42x).
- Deployed rows this map covers: **KoalaBear MCA `a_+ = 1116048`** (L200) and
  **Mersenne-31 list `a_+ = 1116023`** (L203); `B* = 16777215` is the M31 budget.

`TOTALS: nodes=34 proved_edges=16 speculative_edges=3 dead_routes=14`
(machine-checked against the JSON and its arrays by gate (e)).

---

## 1. NODE LEDGER

Every named obligation / wall / floor / dead route / steering object, with owner
lineage, source file + section, one-line statement, status, and the numeric
constants it pins. IDs match the JSON. `SF` paths are repo-root-relative.

### 1a. scottdhughes — KB-MCA Route-D residual free-1 / A_SP card (PR #423)

Deployed (`kb_qatom_route_d_STATUS.md`): `n=2^21`, `e=w+1=67472`, `m_c=913632`,
`free_core=846161`, `n'=A+e=1183520`, `⌊n'/e⌋=17`, `p=2130706433`,
`H2=⌊e·p/(2·31·30)⌋=77291948627`, `e·p=t·p=143763024447376`.

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `H-DEPLOY` | STATUS · Deployed constants | the deployed KB-MCA Route-D row | REFERENCE | 67472, 913632, 846161, 1183520, 17 |
| `H-V25` | v25 · Main theorem | free-1 high families pairwise disjoint; `\|F_H\|≤⌊n/e⌋=31`; `e·p=t·p` is the pair budget | PROVED (cross-high (ι,δ) OPEN) | 31, 143763024447376 |
| `H-V45` | v45 · Residual card criteria | R2/H_R2 after SR+H_M; closes if `\|R2\|≤e·p` **or** `\|H_R2\|≤H2` | criteria PROVED / gates OPEN | 77291948627, 143763024447376 |
| `H-V46` | v46 · Decomposition | `R2 = R2_unt ⊔ R2_D`; `\|R2\|≤930·\|H_R2\|`; `\|H_R2\|≤n` REFUTED | decomp PROVED / envelope REFUTED | 930, 952 |
| `H-V48` | v48 · Proved bounds | `\|H\|≤p^{e−1}`; e=2⇒≤p≤H2 CLOSED; unrestricted ★ for e≥3 REFUTED (`p²>H2`) | MIXED | 67472 |
| `H-V49` | v49 · Geometry | coext free-1 = prefix multipads; `\|H_coext(C)\|≤H_*^pre(min(C),e)`; `t∈[134944,1183520]` | PROVED (geometry) | 134944, 1183520, 17 |
| `H-V51` | v51 · Theorem U2e | U2e PROVED (char≠2) ⇒ `H_*^pre(t,e)≤C(t,2e)`; `t≤2e+2⇒≤H2` (C(2e+2,2)=9105143985; C(2e+3,3)=409570621781265>H2) | PROVED (window OPEN) | 9105143985, 409570621781265 |
| `H-V53` | v53 · Theorem C_unique | untyped core = terminal block `C_*={n'…n−1}`; `N_C=1`; `\|H_unt\|≤H_*^pre(n',e)` | PROVED | 1183520 |
| `H-V54` | v54 · Terminal star | pure-untyped = terminal stars `U_*∋n'−1`; `\|H_unt\|=\|T\|≤C(n'−1,e−1)`; `n'−2e=2^20` so `≫H2` | PROVED (star); `\|T\|≫H2` for e>2 | 1048576 |
| **`H-WALL`** | STATUS · OPEN | **e>2: need `\|T\|≤H2` — the sole open wall on the primary path**; e=2 CLOSED; alternate open close `\|R2\|≤e·p` | **OPEN wall** | 67472 |

### 1b. avdeevvadim — singleton-heavy top-seam Route-D compiler (PR #425)

Deployed (`rowsharp_q_singleton_topseam_v1.md`): `p=2130706433`, `n=2097152`,
`agreement a_+=1116048`, `t=67472`, `w=67471`, `K_rem=4805007`.

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `A0` | topseam · Conditional Counting Closure | if the four realizations hold and `\|R_D\|≤t`, unpaid supports `≤ t·p = 143763024447376`; vs `target_floor=274836936291722953` the paid+retained `t·p+11440` leaves integer slack `274693173267264137` (~57.9 bits / ~10.9 mult) | CONDITIONAL | 143763024447376, 274836936291722953, 274693173267264137, 11440, 1116048, 4805007 |
| `A1` | topseam · planted_switch_core_fiber_cost | Rule 1 proved as exact planted-switch descent; printed cost `\|G_{β,A}\|−1` must be accepted by a planted/core ledger | CONDITIONAL obligation | — |
| `A2` | topseam · weighted_primitive_sp_pade_bound | Rule 2 realized as multiplicity-aware SP/Padé cert (support cost 1); full-rank residual → fixed-key split-shift `X_{r,c,U0,H,β}(z)`; needs printed finite `N_WSP_full` | CONDITIONAL obligation | — |
| `A3` | topseam · strict_distance_child | `d(S,S')≥r+1` paid only if a strict-distance Route-D/RIM/window-shadow payment theorem is imported | OPEN obligation | — |
| `A4` | topseam · charged_row_budget | all charged top-seam rows in a set of size `≤t` (else restricted to the first exposed seam) | OPEN scope obligation | — |
| `A397` | rowsharp_q_prefix_atom_reductions_v1 · additive stratum | additive stratum bound with `\|E_ret\|≤C(16,7)=11440` imported-PROVED; the open primitive full-rank signed-defect certificate is the **primal** side of the holmbuar Fourier crux | REFERENCE (cert OPEN) | 11440 |

### 1c. DannyExperiments — M31 moment / Chebyshev floors (PRs #424/#426)

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `D-MOM` | q_moment_floor_note · Active-row arithmetic | mass-sensitive moment floor `r ≥ (w log2\|B\| − log2 L)/(Δ − log2 θ)`; r-floors `94196/94991/641593/680397`; M31-list `680397` (no orbit gain, L=1; full 2^21 orbit → only 680390); a 100000-moment theorem needs residual mass `< 2^-17.8356` | PROVED floor / ROUTE_CUT | 94196, 641593, 680397, 2097152, 17.835570427166 |
| `D-CHEB` | m31_chebyshev_fixed_remainder_floor · Exact replay | M31-list `c=2048` Chebyshev fixed-remainder floor `F_c=6796405` (exact lower floor); residual `B*−F=9980810` = 2.3237 bits above avg; naive dyadic sum `16548620` (gap 228595) is NOT a counterpacket without co-location | PROVED floor / EXACT_NEW_WALL | 2048, 6796405, 9980810, 1911, 16777215 |
| `D-C1024` | m31_c1024_paired_prefix_audit · surviving wall | small-core `\|core\|≤65` c=1024 defects collapse to the c=2048 factor-through floor; **first live non-factor-through wall = the m=67 even-defect divisor count** (degree-34 `D(Z)\|T_1024(2Z−1)`, 32-even-completion layer choosing 511 of 956 pairs); not paid by `cor:bc-one-pencil` | OPEN wall (refines M31 residual) | 67, 65, 1024, 511, 956 |
| `D-RECON` | q_moment_floor_reconciliation · Exact table | precision reconciliation confirming `94196/94991/641593/680397` and superseding two #384 entries | AUDIT | 94196, 94991, 641593, 680397, 641584, 94992 |

### 1d. holmbuar — row-sharp Q Fourier lineage

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `O407` | q_atom_binding_row_calibration · Verdict | measured `kappa = R_prim ≤ 1.221` on every heavy row vs binding `8.4152`; crossover `avg*≈1205`; atom SUPPORTED | MEASUREMENT (no proof) | 1.221, 8.4152, 1205 |
| `O412` | q_pw2_concentration_floor · Headline | every second-moment (r=2 / Cauchy–Schwarz / Fourier-Plancherel) route DEAD by 1,045,396.58 bits, global & per-stratum; crux = signed-`e_m` inverse; `target_floor=274836936291722953=K_rem·avg` | PROVED floor / crux OPEN | 1045396.58, 274836936291722953, 4805007, 143763024447376 |
| `O414` | q_em_inverse_participation_ratio · Headline | `(STAR) ⟺ PR(Rhat) ≤ nu*=(K_rem−1)²/(Γ2−1)`; `nu*_ref=23088082660036`; L∞ route dead by 2,090,815.35 bits; binding M31-list target ≈55 | REDUCED / crux OPEN | 23088082660036, 2,090,815.35, 4805007 |
| `O416` | q_eq_masked_participation_ratio · Headline | `(STAR)_masked ⟺ PR(E_Q) ≤ nu*_masked` transfers verbatim; `M_gen` pulls triangle `10.472846→5.967<8.4152` (tau=0.4107) but CONDITIONAL on the unpaid lift-class removal; tau<1 raw-avg artifact | REDUCED / CONDITIONAL | 10.472846, 8.4152, 0.4107 |
| `O417` | liftclass_cost_model_refuted · Refutation | keep-one-per-target lift-class removal at cost `w·p` is NOT a row-indexed payment (margins `2^2090812.77 / 2^2090815.35`); resolves #416's condition negatively | REFUTED-DEAD | 4807520, 4805007, 11440 |
| `O-RUNGKB` | qfin_rung_audit · Aggregate | conj:Q rung audit at KB-MCA GREEN; descent (D) PROVED; charge 35624 of `K_raw=4807520`, residual 4771896 (0.0107-bit loss); wall → primitive core + 4-rung ladder `L_1..L_4` (OPEN-REDUCTION) | AUDIT / GREEN | 4807520, 35624, 4771896 |
| `O-RUNGM31` | qfin_rung_audit_m31 · Aggregate | conj:Q rung audit at M31-MCA NOT-GREEN; same descent (D) PROVED; pessimistic 3-rung ladder EXCEEDS `K_raw=9` by ~4.66x (charge 42, residual −33); not a refutation | AUDIT / NOT-GREEN | 42, K_raw=9 |

### 1e. maintainer — grande_finale.tex steering objects

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `GF-ATOM` | grande_finale · def:q-row-atom (L2043) | `R_Q^max ≤ 2^{Δ_Q}`, equiv `max_z\|P_Q(z)\|≤B*` — the missing theorem | OPEN (target) | 1116048, 1116023 |
| `GF-PROB` | grande_finale · prob:row-sharp-q (L2177) | prove `max_z\|P_Q(z)\|≤R_Q^row C(n,a_+)\|B\|^{−(a_+−K)}`; moment proof must fit the finite margin | OPEN (target) | — |
| `GF-TARGET` | grande_finale · prop:q-exact-target (L2061) | four-row budgets; `B*_KB=274980728111395087`, `B*_M31=16777215`; binding = M31-list `8.4152` | REFERENCE | 274980728111395087, 16777215, 4807520.9295, 8.4152 |

### 1f. AUDIT / discrepancy-guard nodes (see §6)

`AUD-TARGETFLOOR`, `AUD-384`, `AUD-M31MCA-CONV`, `AUD-RUNGROUND` — detailed in §6.

---

## 2. EDGE LEDGER — proved implications & preconditions

Each edge carries a verbatim quote (byte-checked by gate (b)) and its
file+section. Types: `precondition`, `used-in-proof`, `reduces-to`,
`alternate-close`, `special-case-of`, `transfers-to`,
`resolves-condition-negatively`, `same-object-dual-view`, `refines`,
`constrains`, `provides-budget`.

**avdeevvadim — the four obligations gate the conditional closure.**
`A1, A2, A3, A4 → A0` (precondition), all four supported by topseam
§Conditional Counting Closure: *"If the branch-realization checks hold and
`|R_D| <= t`, then:"* — the compiler's `sum_B(outdeg_unpaid(B)-1) <= |R_D|*(p-1)
<= t*(p-1)` follows only when every named obligation discharges.

**scottdhughes — the internal reduction chain to the wall.**
- `H-V25 → H-V54` (used-in-proof): v54 §Theorem uses *"v25 disjointness"*.
- `H-V53 → H-V54` (used-in-proof): v54 §Theorem uses *"v53 forces"* the terminal
  index on untyped pairs.
- `H-V54 → H-WALL` (reduces-to): v54 collapses the untyped residual card to
  `|H_unt| = |T|`, so the wall is exactly `|T|≤H2`.
- `H-V45 → H-WALL` (alternate-close): STATUS names the second open branch,
  *"Alternate close (still open): `|R2| ≤ e·p`"*.

**holmbuar — the Fourier lineage.**
- `O412 → O414` (special-case-of): #414 §2 — *"The parent packet's p^{w/2} floor
  is the trivial-support special case"* of the participation-ratio bound.
- `O414 → O416` (transfers-to): #416 — the equivalence *"transfers **verbatim**
  to the masked"* residual `E_Q`.
- `O417 → O416` (resolves-condition-negatively): #417 §7 — #416's headline
  *"resolves negatively at deployment"* because the lift-class removal is unpaid.

**cross-lineage — the holmbuar Fourier crux = the avdeev/#397 Route-D certificate.**
- `O412 → A397` (same-object-dual-view): #412 §7 names the crux as
  *"strictly the same content as PR #397's"* primitive full-rank certificate.
- `O414 → A397` (same-object-dual-view): #414 §7 — Route-D *"is the **primal**
  side of the object §1 names on the Fourier side"*. (The two Route-D lineages
  also agree on `target_floor` to the digit — see §6, `AUD-TARGETFLOOR`.)

**DannyExperiments + steering.**
- `D-CHEB → D-C1024` (refines): the 3x3 residual audit *"refines this broad
  target to the"* c=1024 paired-prefix wall.
- `D-MOM → GF-PROB` (constrains): the moment floor bounds *"any moment-only proof
  of the row atom bound"*.
- `GF-TARGET → GF-ATOM` (provides-budget): prop:q-exact-target supplies `B*`;
  *"the binding Q problem is the Mersenne-31 list row"*.

The 16 proved edges form a DAG (gate (d)); `A397` is the shared cross-lineage sink.

## 2b. SPECULATIVE EDGES — `ANALYSIS-CONJECTURAL` (fenced; NOT in the proved ledger)

> The following three edges are **plausible but not stated in any source**. They
> carry no verbatim quote and are excluded from the proved graph by the verifier
> fence (gate (f)). Do not read them as established.

- `H-WALL ~ A0` (complementary-decomposition-of-same-A_SP-residual): hughes's
  `|T|≤H2` free-1 high card and avdeev's charged-row `R_D` top-seam compiler both
  bound the KB-MCA Route-D residual toward `A_SP ≤ t·p = e·p`, but **no source
  identifies** the free-1 high / `|T|` object with the charged-row object — and
  the topseam explicitly *"does not supersede a full Route-D residual support
  certificate"* (#423). Same target, distinct decompositions; identification
  unproven.
- `H-V25 ~ A2` (apparent-shift-pair-overlap): hughes's free-1 pairs
  (`f_U−f_V` constant) and avdeev's Rule-2 multiplicity-aware SP/Padé shift-pairs
  (`U≠U0`, same cell) are both shift-pair structures on the KB-MCA residual, but
  no source demonstrably identifies them.
- `D-C1024 ~ A2` (cross-row-planted-shift-pair-analogy): Danny's M31 m=67
  even-defect wall has a named `M31-PLANTED-RESIDUAL-SHIFT-PAIR-INVERSE` incidence
  route structurally analogous to avdeev's KB `weighted_primitive_sp_pade_bound`;
  but they are **different rows** (M31 vs KB) and no source links them.

---

## 3. SINGLE-LEMMA FRONTIER (ranked, per row)

Statements each of which, if proved, closes a **named** branch. Ranked by
concreteness / proximity to a branch closure.

### KoalaBear MCA row (`a_+ = 1116048`)

1. **[holmbuar / avdeev-#397] max-fiber signed-`e_m` inverse** —
   `Σ_{t≠0}|e_m(v_t)| ≤ (K_rem−1)C(n,m)`, i.e. `PR(Rhat) ≤ nu*_ref=(K_rem−1)²=2^44.39`
   (effective Fourier support). *Closes:* the **direct** row-sharp Q atom
   (`def:q-row-atom`) at KB-MCA — it is the Fourier side of #397's primitive
   full-rank certificate (`O412→A397`, `O414→A397`). *After it:* the KB rung
   audit is GREEN, so the reduction to the primitive core is already clean; the
   BC chart audit (`prob:saturated-bc`) is the separate remaining branch.
   *Owner:* holmbuar (Fourier) / avdeevvadim (primal, #397).
2. **[scottdhughes] `|T| ≤ H2 = 77291948627`** — the free-1 partner count for
   e-sets through terminal index `n'−1` on the KB roots-of-unity arc of length
   `n'=1183520` (`e=67472`). *Closes:* the scottdhughes primary Route-D residual
   free-1 / A_SP card (via `H-V53` C_unique + `H-V54` terminal star,
   `|H_unt|=|T|`). *After it:* `A_SP ≤ t·p` follows for that decomposition; the
   full `U(1116048)≤B*` still needs the BC audit + first-match ledger.
   *Owner:* scottdhughes. *Alternate (same owner):* `|R2| ≤ e·p`.
3. **[avdeevvadim] `weighted_primitive_sp_pade_bound`** — a printed finite bound
   `N_WSP_full(z) ≤ B_WSP_full` on the fixed-key split-shift pencils. *Closes:*
   the top-seam compiler's Rule-2 residual (given `A1`, `A3`, `A4`) — a distinct
   Route-D decomposition of the same A_SP residual. *Owner:* avdeevvadim.
4. **[avdeevvadim] each of `A1` / `A3` / `A4`** — the planted-core-fiber cost
   ledger, the strict-distance payment theorem, and the `|R_D|≤t` scope — each
   closes its own named branch of the conditional closure `A0`. *Owner:* avdeevvadim.

### Mersenne-31 list row (`a_+ = 1116023`) — the binding row (`8.4152`)

1. **[holmbuar] max-fiber signed-`e_m` inverse at M31-list** —
   `PR(Rhat) ≤ nu*_ref = 2^5.781 ≈ 55` (effective Fourier support ≈55 of
   `2^2090857` directions). Per #414 this is *"the sharpest, most concrete
   standalone target the program has"* for the direct atom. *Closes:*
   `def:q-row-atom` at the binding row. *Owner:* holmbuar.
2. **[DannyExperiments] the m=67 even-defect divisor count**
   (`CAP25-V13-M31-T2048-EVEN-DEFECT-DIVISOR-COUNT`) — bound or refute the
   admissible oriented completions of the degree-34 divisor `D(Z)|T_1024(2Z−1)`
   (32-even-completion layer, 511 of 956 pairs). *Closes:* the first live
   non-factor-through wall of the c=1024 paired-prefix packet (small-core rigidity
   already collapses `|core|≤65` to the c=2048 floor `6796405`). *After it:* the
   `m≥69` defects and the upper-ledger fit inside `2.3237` bits above avg remain.
   *Owner:* DannyExperiments.
3. **[DannyExperiments, sibling M31-MCA] genuinely tighter `L_1,L_2,L_3`** — the
   M31-MCA rung ladder needs row-specific quotient-flatness bounds strictly below
   the generic `K_raw=9` bar (the pessimistic ladder overdraws by 4.66x). *Closes:*
   the rung-audit reduction at M31-MCA. *Owner:* holmbuar (audit) — needs new math.

---

## 4. DEAD-ROUTE LEDGER

Everything proved dead / banked, with the killing citation (all quotes byte-checked).

| id | route (owner) | status | killing citation |
|---|---|---|---|
| `DR-O1` | any r=2 / Cauchy–Schwarz / Fourier-Plancherel bound (holmbuar) | PROVED-DEAD by 1,045,396.58 bits | #412 §2 *"every r=2 route is rigorously dead"* |
| `DR-O2` | uniform L∞ per-direction `|e_m|≤β*C` (holmbuar) | PROVED-DEAD by 2,090,815.35 bits | #414 §3 *"the L-infinity route contributes nothing"* |
| `DR-O3` | keep-one-per-target lift-class removal at `w·p` (holmbuar) | REFUTED, `2^2090812.77` | #417 title *"the finite-field lift-class cost model is unpayable"* |
| `DR-O4` | anticode fiber cap (holmbuar) | PROVED-DEAD (p-independent), 1,717,478 bits | #412 §3 *"DEAD (separately"* |
| `DR-O5` | frequency-quotient mask `M_quot` alone (holmbuar) | MEASURED-DEAD (worsens 10.58→11.89) | #416 §1 *"frequency-quotient mask alone WORSENS it"* |
| `DR-D1` | moment-only proof below `r=680397/94196` (DannyExperiments) | ROUTE-CUT | #424 *"rules out a class of finite proof shortcuts"* |
| `DR-D2` | additive stacking of dyadic Chebyshev floors (DannyExperiments) | ROUTE-CUT (not a counterpacket) | #424 *"no additivity/stacking theorem is being"* |
| `DR-D3` | multiplicative orbit amplification, M31-list `L=1` (DannyExperiments) | DEAD (2^21 orbit → only 680390) | #424 *"orbit amplification is not a finite solution mechanism"* |
| `DR-H1` | ambient `L≤70` / small ambient cover (scottdhughes, v40) | REFUTED | STATUS *"small ambient cover"* |
| `DR-H2` | `\|H_R2\|≤n` / `≤⌊n/e⌋` / multi-tier (scottdhughes, v42–46) | REFUTED (max H_R2=952) | STATUS *"multi-tier confusions"* |
| `DR-H3` | unrestricted `H_*≤H2` for e≥3 (scottdhughes, v48) | REFUTED (`p²>H2`) | STATUS *"Unrestricted `H_*≤H2`"* |
| `DR-H4` | ambient multipad `t≤2e+2` (scottdhughes, v52) | REFUTED | STATUS *"Ambient multipad"* |
| `DR-H5` | pack `k=17` alone ⇒ H2 (scottdhughes, v54) | REFUTED (e=3 toys ~ p²) | STATUS *"Pack `k=17` alone"* |
| `DR-H6` | free-regime / `M_m` uniqueness tourism (scottdhughes, v8+) | REFUTED-BANKED | STATUS *"Free-regime / Mm uniqueness tourism"* |

---

## 5. CROSS-ROW TABLE — KB row vs M31-list row

| object | KoalaBear MCA (`a_+=1116048`) | Mersenne-31 list (`a_+=1116023`) | transfers? / why |
|---|---|---|---|
| budget `B*` (`prop:q-exact-target`) | `274980728111395087` (~22.20-bit margin) | `16777215` (~3.07-bit margin) | row-specific: different prime & extension |
| binding budget ratio | `4807520.9295` | `8.4152` (the binding row) | row-specific |
| domain / symmetry | multiplicative coset `α·μ_n ⊂ F_p^*` | Chebyshev / twin-coset (`chi` on the norm-one torus) | row-specific geometry (rung-audit §1) |
| scottdhughes free-1 high card (`\|T\|≤H2`) | the standing wall (`H-WALL`) | **no analog stated** — free-1 machinery is on `μ_n` | KB-specific; M31 has no multiplicative subgroup |
| avdeev top-seam compiler | `A0`..`A4`, `1116048` | not deployed | KB-specific |
| Danny Chebyshev fixed-remainder floor | not stated | `F_2048=6796405`, residual `9980810` | M31-specific (Chebyshev fold) |
| holmbuar signed-`e_m` inverse (`prop:fourier-audit`) | `nu*_ref=2^44.39` | `nu*_ref=2^5.781≈55` (binding) | transfers (all four rows); `nu*` row-specific |
| moment-order floor `r0` | `94196` (twist orbit saves 1 order) | `680397` (no orbit gain, `L=1`) | same object, row-specific `r0` |
| conj:Q rung audit (MCA rows) | `1116048` **GREEN**, `K_raw=4807520`, 0.0107-bit loss | `1116024` **NOT-GREEN**, `K_raw=9`, 4.66x over | descent (D) PROVED both; verdict flips on the tiny M31 budget |
| `v2(m_safe)` (ladder depth) | 4 (4-rung ladder) | 3 (3-rung ladder) | row-specific 2-adic valuation |

The two rung audits (`O-RUNGKB`, `O-RUNGM31`) share the **same** PROVED descent
identity (D); the GREEN/NOT-GREEN split is purely the budget scale
(`K_raw` 4807520 vs 9) and `v2(m_safe)` (4 vs 3), not a difference in the proof.

---

## 6. AUDIT / discrepancy nodes

- **`AUD-TARGETFLOOR` (cross-lineage AGREEMENT + conflation guard).**
  `target_floor = 274836936291722953` (`= K_rem·avg`, the Q-actionable residual
  max-fiber target) is used **identically** by avdeevvadim (topseam
  §deployed_arithmetic_closure) and by holmbuar (#412 §0, #414 §0). It is a
  **distinct object** from `grande_finale` `B* = 274980728111395087` (the full
  per-fiber budget); the two differ by `~t·p = 143763024447376`, and
  `target_floor < B*` because `t·p` is reserved for non-Q first-match cells. This
  is **not** a contradiction — the two Route-D lineages agree on `target_floor`
  to the digit — but **`target_floor` must not be conflated with `B*`.**
  (DannyExperiments correctly uses the full `B*` in `D-MOM`; only the KB-MCA
  Route-D residual packets use `K_rem·avg`.)
- **`AUD-384` (resolved, superseded).** The moment-order-floor entries KB-list
  `94992→94991` and M31-MCA `641584→641593` from #384 are superseded by the
  reconciliation note (rounded 4-decimal margin input vs exact real-average
  `Δ_Q`); resolved in-tree, not an open discrepancy.
- **`AUD-M31MCA-CONV`.** M31-MCA is the unique convention-sensitive moment row:
  `r_ceil=641594` vs `r_real=641593`; the maintainer's table uses the real-average
  column.
- **`AUD-RUNGROUND`.** The KB rung-audit aggregate charge is a ±1 convention
  (`ceil 35624` adopted vs `floor 35623` in Lane C's script); every per-rung share
  and verdict is identical either way.

No source-vs-source **contradiction** on a constant or a claimed implication was
found. The one number that looks like a clash (`target_floor` vs `B*`) is two
legitimately different objects, recorded above.

---

## 7. Weave (context only — sibling arcs this map does not re-derive)

- The integrated files this map composes: scottdhughes v25/45/46/48/49/51/53/54 +
  STATUS (PR #423, maintainer-curated); avdeev topseam (PR #425) and the
  integrated #397 prefix-atom reductions; DannyExperiments moment-floor /
  Chebyshev / c1024 notes (PRs #424/#426) + the in-tree reconciliation; holmbuar
  #407/#412/#414/#416/#417 and the KB/M31 rung audits.
- **fp-span sibling arc (context only):** the entropy-inverse F_p-span cell family
  (`cap25_v13_entropy_inverse_fp_span_*`) is the asymptotic-side sibling of the
  finite Route-D program mapped here; `prob:entropy-inverse-q` and its
  `rem:entropy-inverse-skeleton` (steps 4–6) are the asymptotic counterpart of the
  holmbuar finite crux (#414 §5). This map does not touch that arc; it is named
  only to place the Route-D state in the larger Q program.
- **AllenGrahamHart (#405)** independently calibrated row-sharp Q (max/mean ≈1.21
  matching holmbuar's measured kappa cap 1.221); cited by #407 as consistency
  context, not a dependency of any node here.

## 8. Reproduce

```bash
python3 experimental/scripts/verify_route_d_barrier_map.py
#   RESULT: PASS  (< 30 s; six gates + six tamper self-tests)
```

## 9. Nonclaims (restated)

This packet does **not** prove `U(1116048) ≤ B*`, `U(1116023) ≤ B*`, any deployed
safe row, `prob:row-sharp-q`, `def:q-row-atom`, or any single node's open lemma.
It composes the integrated Route-D state into one provenance-gated map. It claims
no new mathematics; the three speculative edges are `ANALYSIS-CONJECTURAL` and are
fenced out of the proved ledger. The map reflects the tree at `84b393e` and decays
as new work lands.
