# The chart-free pruned signed bound: escalating first-match pruning to a general source chart, and its interface with the charge-preserving signed clause

## Status

```text
Status: PROVED (general chart-free bound, all finite abelian G, all bands, all
        q>=2, all signs on a pruned support) + PROVED dictionary/discharge for
        pruned nonsemantic packets + PROVED layer-cake residual identity.
        The residual (unpruned/heavy-fiber packets, and q>=q_+) is mapped
        honestly, not closed.
HARD INPUT 2 SERVED: "image-scale MI + MA, or a direct Sidon payment"
        (agents.md L47/L67) -- the signed-minor clause of avdeevvadim's #716
        charge-preserving semantic-or-signed dichotomy, now at the GENERAL
        chart level (not one family).
Verdict per part (route-scoped):
  (1) THEOREM I is chart-free: R_A(g) <= (L/M)(L delta_A)^{1/2-1/q}
      <= L^{3/2-1/q}/M on EVERY finite abelian G, EVERY chart Phi (M supports,
      image size L), EVERY band A, EVERY q>=2, EVERY signed mask |g|<=1 on a
      support with <=1 point per Phi-syndrome (|S|<=L).  No hidden
      family-dependence: both endpoints (l2 contraction, l-infinity
      Cauchy-Schwarz + Parseval) use only |g|<=1, |S|<=L, and character
      orthogonality.  The bound touches the chart ONLY through L, M
      (and delta_A<=1).  Vanishing criterion (exact): e^{-Omega(N)} iff
      (3/2-1/q)logL - logM <= -Omega(N); per-chart top q_+ = 1/(3/2 - logM/logL).
  (2) YES: on any chart passing the density criterion, EVERY pruned (one-per-
      syndrome, |b_{U_i}|<=1) nonsemantic packet of #716's Sec-6 decomposition
      AUTOMATICALLY satisfies the signed clause c_i <= e^{o(N)} M/L^{1-1/q}.
      The dictionary is exact and directions match (compatibility c_i<=||.||_q
      chains with Theorem I's upper bound).  This DISCHARGES the signed clause
      for pruned packets.  What remains is #716's own decomposition step and
      the unpruned pieces (part 3).
  (3) RESIDUAL: the multiplicity-carrying (unpruned) packets.  Layer-cake:
      any mask decomposes into W_max pruned layers, so c_i <= W_max*L^{1/2};
      the clause then holds whenever W_max*L^{3/2-1/q} <= e^{o(N)} M, i.e.
      W_max=e^{o(N)}.  The ONLY residual is W_max=e^{Omega(N)} (a heavy fiber
      -> #716 Sec 2 / #717 semantic side by the heavy-fiber inverse) and the
      q-range q>=q_+ (residual = a signed Sidon estimate, #728 Thm IV).
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**. Every number below is recomputed by
`experimental/scripts/verify_general_pruned_signed_bound.py` (stdlib only,
deterministic, `RESULT: PASS (193359/193359)`, `--tamper-selftest` catches
`6/6`, ~1.6 s). Machine-readable certificate:
`experimental/data/certificates/general-pruned-signed-bound/general_pruned_signed_bound.json`.
No `.tex`/`.pdf` is edited.

## Interfaces

- **avdeevvadim's #716** (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`).
  The normalized band excess `R_A(f)=(L^{1-1/q}/M)||P_A f||_q` (barrier Prop 1.1),
  the kernel `K_A(x)=(1/|G|) sum_{xi in A} chi_xi(x)`, the band projection
  `P_A f=K_A*f` (`hat{K_A}=1_A`), and the **charge-preserving semantic-or-signed
  dichotomy** (barrier Sec 6) with its signed clause `c_i <= e^{o(N)} M/L^{1-1/q}`
  and compatibility `||P_{B_i} b_{U_i}||_q >= c_i` are all his. This packet
  proves the *general-chart* form of the signed clause for pruned packets and
  states exactly what the dichotomy still needs. The point-mass reduction
  (barrier Sec 1-2) is the semantic-side target of part 3.
- **#717** (`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`).
  The complete-band grammar, the band count `K_N=2+ceil(log2 n)`, the whole-
  residual band-failure Lemma 2.1, and the depth-R locator/power-sum prefix
  chart (`eq:exact-power-sum-map`, `L <= Q^R`, `M=C(N,a)`) evaluated in the
  density table are #717's. The heavy-fiber inverse (its Thm 5.1) is the map
  that sends the part-3 unpruned residual to the semantic side.
- **#728** (`experimental/notes/thresholds/first_match_signed_gain.md`). This
  packet is the escalation of #728's Theorem I from the depth-1 superincreasing
  family (`A_i=5^i`, `C=2 sum A_i+1`, `T={A_i} u {C-A_i}`, `a=B`, `Phi=sum mod C`)
  to a general chart. #728's family is recovered exactly as a special case:
  its `q_+=4.199` is the asymptotic rate limit of the general
  `q_+(chart)=1/(3/2 - logM/logL)` (verified: finite `q_+` climbs 2.586->3.182
  over `B=2..12`, toward `1/(3/2 - log4/log3)=4.1992`).
- **#723** (`signed_minor_payment_clause_census_v1.md`): the census whose
  first-match clause (iii) #728 turned into a theorem on one family; here that
  theorem is chart-free.

---

## 0. Setup and conventions (all #716/#717)

`G` a finite abelian group, `H=|G|`, dual `hat G` (characters `chi_xi`,
`xi in hat G`). A **chart** is a syndrome map `Phi: Omega^0 -> G` on a full
profile slice `Omega^0` (`M=|Omega^0|`), with occupied set `Phi(Omega^0)` and
image size `L=|Phi(Omega^0)|`. `N` is the ambient size parameter
(`log M, log L = O(N)`). A **band** is any `A subseteq hat G \ {0}`;
`delta_A=|A|/H`; `K_A(x)=(1/H) sum_{xi in A} chi_xi(x)`; `P_A f = K_A*f`, so
`hat{P_A f}=1_A hat f` and `P_A` is the orthogonal projection onto
`span{chi_xi : xi in A}`. Counting measure: `||f||_q^q = sum_x |f(x)|^q`,
`||f||_inf=max_x|f(x)|`. Band excess `R_A(f)=(L^{1-1/q}/M)||P_A f||_q`.

**Pruning (the hypothesis).** First-match pruning keeps exactly one support per
occupied syndrome, so the residual count function is `1_S` on `S=Phi(Omega^0)`,
`|S|=L`. A **signed sub-mask on the pruned support** is any `g: G -> [-1,1]`
supported on a set `S` with **at most one point per Phi-syndrome**, hence
`|supp g| <= L` and `|g|<=1`. (Equivalently: `g=0` off the occupied set,
values in `[-1,1]`; any sign/drop vector `eps in {-1,0,1}^S` qualifies.)

---

## 1. Part 1 -- the general chart-free bound (PROVED)

### Lemma 1 (l2 endpoint, chart-free).
For `g` a signed sub-mask on the pruned support,
`||P_A g||_2 <= ||g||_2 <= sqrt(|supp g|) <= sqrt(L)`.
*Proof.* `P_A` is an orthogonal projection so `||P_A g||_2<=||g||_2`;
`||g||_2^2 = sum_{x in supp g}|g(x)|^2 <= |supp g| <= L` since `|g|<=1`. `square`

### Lemma 2 (l-infinity endpoint, chart-free).
`||P_A g||_inf <= max_x sum_{s in supp g}|K_A(x-s)| <= sqrt(L) ||K_A||_2 = sqrt(L delta_A)`.
*Proof.* `|(K_A*g)(x)| <= sum_{s in supp g}|K_A(x-s)||g(s)| <= sum_{s in supp g}|K_A(x-s)|`
(`|g|<=1`). Cauchy-Schwarz over the `<=L` nonzero terms:
`<= sqrt(|supp g|) (sum_{s in supp g}|K_A(x-s)|^2)^{1/2} <= sqrt(L)(sum_{y in G}|K_A(y)|^2)^{1/2}`
(the translates `x-s` are distinct points of `G`). Parseval:
`||K_A||_2^2 = (1/H^2) sum_x |sum_{xi in A}chi_xi(x)|^2 = (1/H^2)|A|H = |A|/H = delta_A`
(character orthogonality). `square`

### Theorem I (chart-free pruned signed bound, PROVED).
For every finite abelian `G`, every chart `Phi` (`M` supports, image size `L`),
every band `A subseteq hat G\{0}` (`delta_A=|A|/H`), every `q in [2,inf]`, and
every signed sub-mask `g` on the pruned support,
```text
R_A(g) = (L^{1-1/q}/M)||P_A g||_q  <=  (L/M)(L delta_A)^{1/2-1/q}  <=  L^{3/2-1/q}/M.
```
*Proof.* Riesz-Thorin/Lyapunov log-convexity of `l^q` norms with `1/q=theta/2`,
`theta=2/q`, and Lemmas 1-2:
`||P_A g||_q <= ||P_A g||_2^{2/q} ||P_A g||_inf^{1-2/q} <= L^{1/q}(L delta_A)^{(1-2/q)/2}`.
Multiply by `L^{1-1/q}/M`:
`R_A(g) <= (L^{1-1/q}/M)L^{1/q}(L delta_A)^{1/2-1/q} = (L/M)(L delta_A)^{1/2-1/q}`;
then `delta_A<=1` and `1/2-1/q>=0` give `<= (L/M)L^{1/2-1/q}=L^{3/2-1/q}/M`. `square`

**KEY OBSERVATION (verified).** The bound is *chart-free*: every step uses only
`|g|<=1`, `|supp g|<=L`, character orthogonality (`||K_A||_2^2=delta_A`), and
functional-analytic interpolation. It never uses the group structure of `G`,
the algebra of `Phi`, or any property of the family beyond the two scalars
`L=|Phi(Omega^0)|` and `M=|Omega^0|` (and `delta_A<=1`). Re-derived on four
different chart types with the same constant (see 1.3); no family-dependent
term appears.

**Sharp consequences.**
- `q=2` (sign-independent, exact): `R_A(g) <= L/M`. This is the widest and
  cleanest window and the natural operating point (see part 2).
- The bound at `q=inf` is `R_A(g) <= (L/M)sqrt(L delta_A)`; it holds but does
  not vanish -- this is #728 Thm IV's route-cut (`sup_g R_A = (L/M)Lambda*(A)`,
  `Lambda*(A)=max_x sum_{s in S}|K_A(x-s)| <= sqrt(L delta_A)` by Lemma 2).

### 1.2 Vanishing criterion (Corollary, exact)

`R_A(g) <= L^{3/2-1/q}/M` is `e^{-Omega(N)}` iff
```text
(3/2 - 1/q) log L - log M  <=  -Omega(N),
```
a **pure density condition on the chart** (only `L, M`). Per-chart top exponent:
```text
q_+(chart) = 1 / (3/2 - logM/logL),
```
so the vanishing window is
```text
logM/logL <= 1        =>  window EMPTY      (M<=L, near-injective chart);
1 < logM/logL < 3/2   =>  window [2, q_+),  q_+ = 1/(3/2 - logM/logL) > 2;
logM/logL >= 3/2      =>  window ALL q>=2   (M >= L^{3/2}).
```
(At `q=2` the coefficient of `log L` is `1`, so `q=2` is in the window iff
`M>L`; large `q` is the restrictive end.) The clause the dichotomy actually
needs is weaker -- `e^{o(N)}`, not `e^{-Omega(N)}` -- so it holds under
`(3/2-1/q)log L <= log M + o(N)` (same threshold `q_+`).

### 1.3 The atlas's actual charts: depth-R prefix, `L <= Q^R`, `M = C(N,a)`

On the depth-R locator/power-sum prefix chart (#717 Sec 1: `L<=Q^R`,
`Q=|B|` the coefficient field, `M=C(N,a)`, `N=|T|`, `beta=a/N`):
`log L <= R log Q`, and `N h(beta) - log(N+1) <= log M <= N h(beta)`
(binary-entropy bracket, `h` in nats). Hence `logM/logL >= logM/(R log Q)`, and
the **readable sufficient density condition** for a nonempty window (`q=2`) is
```text
R log Q  <  N h(a/N)   (prefix-image rate below the slice entropy),
```
with the whole `q`-range covered when `R log Q <= (2/3) N h(a/N)`. For bounded
depth `R` and polynomial `Q` this is automatic (`R log Q = O(log N) = o(N)`);
it only binds when `R log Q` grows linearly in `N` (deep prefixes over large
fields). Exact table (verifier, exact `L` by enumeration):

| chart (depth-R prefix) | Q | N | a | R | L | Q^R | M=C(N,a) | logM/logL | q_+ | window |
|---|---|---|---|---|---|---|---|---|---|---|
| F5  a2 R1 | 5  | 5  | 2 | 1 | 5   | 5   | 10   | 1.431 | 14.43 | [2,14.43) |
| F7  a3 R1 | 7  | 7  | 3 | 1 | 7   | 7   | 35   | 1.827 | inf   | all q     |
| F7  a3 R2 | 7  | 7  | 3 | 2 | 28  | 49  | 35   | 1.067 | 2.309 | [2,2.309) |
| F11 a4 R1 | 11 | 11 | 4 | 1 | 11  | 11  | 330  | 2.418 | inf   | all q     |
| F11 a4 R2 | 11 | 11 | 4 | 2 | 110 | 121 | 330  | 1.234 | 3.755 | [2,3.755) |
| F11 a5 R1 | 11 | 11 | 5 | 1 | 11  | 11  | 462  | 2.559 | inf   | all q     |
| F13 a6 R1 | 13 | 13 | 6 | 1 | 13  | 13  | 1716 | 2.904 | inf   | all q     |

Reading: shallow prefixes (`R=1`) over a small field collapse `M` onto a tiny
image (`L<=Q`), giving `logM/logL` large and an **all-q** window; deepening `R`
(more prefix coordinates) enlarges `L` toward `Q^R` and shrinks the window
(F7 a3: `R=1` all-q -> `R=2` only `[2,2.309)`). The window closes exactly when
the prefix becomes near-injective (`M ~ L`).

### 1.4 Instantiation across chart TYPES (verifier)

Theorem I is verified (bound never violated, `max R_A/UB <= 1`) on:

| chart | type | G | M | L | kappa | logM/logL | q_+ | signs tested |
|---|---|---|---|---|---|---|---|---|
| chart1 | depth-1 elementary prefix (F7, a3) | Z_7 | 10 | 7 | 5 | 1.183 | 3.158 | **EXHAUSTIVE** `{-1,0,1}^S` |
| chart2 | depth-2 moment curve `v_t=(t,t^2)` (F11, a4) | Z_11^2 | 330 | 110 | 6 | 1.234 | 3.755 | 240 sampled signed/fractional |
| chart3 | **arbitrary** random `Phi` (seeded hash) | Z_40 | 126 | 37 | 5 | 1.339 | 6.225 | 240, **arbitrary bands** (no columns) |
| chart4 | depth-2 elementary prefix (F5, a2) | Z_5^2 | 10 | 10 | 5 | 1.000 | 2.000 | 160 sampled (empty window: `M=L`) |

chart3 has **no algebraic/column structure at all** and uses **arbitrary** (non-
dyadic) bands -- the strongest demonstration that the bound is chart- and band-
free. chart4 is a genuine near-injective instance (`M=L=10`, `q_+=2`, empty
window): Theorem I's *inequality* still holds (max ratio 0.980), it simply does
not vanish -- the criterion reports this correctly. Endpoints (`||K_A||_2^2 =
delta_A`, l2 contraction, l-infinity CS) are checked separately on every band.

---

## 2. Part 2 -- the dictionary and the discharge (PROVED)

### 2.1 Exact dictionary to #716's charge normalization

The dichotomy (#716 Sec 6) decomposes the positive correlation `Omega_+` into
`<= e^{o(N)}` rooted packets `(B_i, U_i, c_i)` with `c_i>=0`, `sum c_i=Omega_+`,
`c_i <= sum_{S in U_i} omega(S)`, and the **compatibility** condition
`||P_{B_i} b_{U_i}||_q >= c_i`; each packet is either one of five semantic
precursors or a **signed-minor packet** required to satisfy the **signed clause**
`c_i <= e^{o(N)} M/L^{1-1/q}`. The exact translation to our normalization:
```text
||P_{B_i} b_{U_i}||_q = (M / L^{1-1/q}) R_{B_i}(b_{U_i}),
  so  c_i <= ||P_{B_i} b_{U_i}||_q = (M/L^{1-1/q}) R_{B_i}(b_{U_i}).
```
The clause threshold `M/L^{1-1/q}` is exactly `||P_A f||_q` at `R_A(f)=1`. Thus
the signed clause is literally "`R_{B_i}(b_{U_i}) <= e^{o(N)}` **and** compatibility".
Directions match: compatibility is a *lower* bound on the norm by the charge,
which chains with Theorem I's *upper* bound on the norm to cap `c_i`.

### 2.2 Theorem D (signed clause discharged for pruned packets, PROVED).
Let the chart satisfy the density criterion `(3/2-1/q) log L <= log M + o(N)`
(equivalently `q <= q_+(chart)`). Then every nonsemantic packet `(B_i,U_i,c_i)`
of the #716 Sec-6 decomposition whose mask `b_{U_i}` is **pruned** (at most one
support per syndrome, `|b_{U_i}|<=1`, hence `|supp b_{U_i}|<=L`) automatically
satisfies the signed clause:
```text
c_i <= ||P_{B_i} b_{U_i}||_q <= L^{1/2} <= e^{o(N)} M / L^{1-1/q}.
```
*Proof.* Compatibility gives `c_i <= ||P_{B_i}b_{U_i}||_q`. `b_{U_i}` is a
signed sub-mask on the pruned support (one support per syndrome, weights in
`[-1,1]`), so Theorem I applies band-uniformly (`delta_{B_i}<=1`):
`||P_{B_i}b_{U_i}||_q = (M/L^{1-1/q})R_{B_i}(b_{U_i}) <= (M/L^{1-1/q})(L^{3/2-1/q}/M) = L^{1/2}`.
The density criterion is exactly `L^{1/2} <= e^{o(N)} M/L^{1-1/q}`
(`L^{3/2-1/q} <= e^{o(N)}M`). `square`

So the escalation resolves part (2) affirmatively: **on every chart passing the
density criterion, the general theorem discharges the signed clause for every
pruned nonsemantic packet, band-uniformly, with no family hypothesis.** Verified:
the discharge norm bound `||P_A g||_q <= L^{1/2}` holds on all four charts for
`q in {2,3,4}` (identity `(M/L^{1-1/q})(L^{3/2-1/q}/M)=L^{1/2}` checked exactly).

### 2.3 No fundamental mismatch (checked)

The three subtleties flagged for this interface all resolve cleanly:
- **normalization** -- the map `||.||_q <-> R_A` is the exact scalar
  `M/L^{1-1/q}`; no hidden factor.
- **charge-vs-norm direction** -- `c_i <= ||.||_q` (compatibility, a lower bound
  on the norm) composes correctly with Theorem I (an upper bound on the norm);
  there is no direction clash.
- **band-completeness** -- Theorem I holds for *every* `A subseteq hat G\{0}`,
  not only complete/symmetric bands, so the packet's own band `B_i` is covered
  and `delta_{B_i}<=1` gives the band-uniform crude bound. (Completeness is only
  used elsewhere to bound `kappa<=K_N` in the decomposition, part 3.)

What Theorem D does **not** do (stated precisely for part 3): it does not perform
#716's decomposition (producing the pruned pieces), and it does not cover
multiplicity-carrying pieces.

---

## 3. Part 3 -- the honest residual map (one page)

After Theorem I + Theorem D, exactly three things remain of the signed clause in
general. None is claimed closed here.

### 3.1 Multiplicity-carrying (unpruned) packets -- the semantic side

If a packet's mask carries multiplicity (`|b_{U_i}(s)| > 1` at some syndrome,
i.e. several supports share `s`), Lemma 1 fails (`||b||_2^2 <= L` needs
`|b|<=1`) and Theorem I does not apply. **Layer-cake identity (PROVED,
verified).** Any integer-valued mask `b` with max multiplicity
`W_max = max_s |b(s)|` decomposes as `b = sum_{j=1}^{W_max} g_j`,
`g_j = 1_{b>=j} - 1_{b<=-j} in {-1,0,1}^G` a *pruned* signed mask on
`supp b subseteq Phi(Omega^0)` (`|supp g_j|<=L`). Triangle inequality + Theorem I
per layer:
```text
||P_{B_i} b||_q <= sum_{j=1}^{W_max} ||P_{B_i} g_j||_q <= W_max * L^{1/2},
  so  c_i <= W_max * L^{1/2},
```
and the signed clause holds whenever `W_max * L^{3/2-1/q} <= e^{o(N)} M`, i.e.
**`W_max = e^{o(N)}`** on a density-passing chart. The clause therefore survives
for *every* packet with subexponential multiplicity; the ONLY residual is
`W_max = e^{Omega(N)}` -- a genuinely **heavy fiber**.

That residual is exactly the **semantic side** of the dichotomy, by design.
- The heavy point mass `f = W 1_{s0}` roots with uniform positive owner weight
  `omega(S)=||P_A f||_q/W>0` (#716 Sec 2); by the heavy-fiber inverse
  (#717 Thm 5.1: hereditary reduces to plain emission on the prefix chart, `R<char`,
  `R<=m-2`) it is an admissible rooted packet -> a semantic precursor.
- Theorem II direction (`#717` Lemma 2.1 / `#728` Thm II): the unpruned excess
  can genuinely exceed the pruned ceiling. Pigeonhole over the `<=K_N` bands
  gives `|(P_{A*} b)(s0)| >= (W - M/H)/K_N`, so `R_{A*}(b) >= (L^{1-1/q}/M)(W-M/H)/K_N`,
  which **grows with `W`**. The layer-cake upper bound `W_max L^{3/2-1/q}/M`
  and this lower bound bracket the unpruned excess: it scales like `W_max`,
  hence violates the signed clause precisely when `W_max` is exponential.

Concrete crossover (verifier, #728 family, no large DFT): `W=C(B,B/2)` overtakes
`sqrt(L)` at `B=6` (`W=20 > sqrt(365)=19.1`) and stays above for `B>=6`, because
`W ~ 2^B/sqrt(B)` grows faster than `sqrt(L) ~ 3^{B/2}/sqrt 2`. Below the
crossover the pruned bound already covers the whole (unpruned) mask; above it,
the heavy fiber must route to the semantic branch. This is the quantitative
statement that the residual is *only* the heavy-fiber (semantic) regime.

### 3.2 The decomposition step (#716's, not ours)

Theorem D discharges the clause **given** that a packet is pruned (or has
`W_max=e^{o(N)}`, via 3.1). It does not perform #716 Sec-6's decomposition of
`Omega_+` into `<= e^{o(N)}` charge-preserving pieces. The layer-cake shows a
packet of total multiplicity `mu` splits into `<= mu` pruned layers; so the
decomposition is `e^{o(N)}`-bounded and every non-semantic piece is
clause-compliant **iff** the packet multiplicity census is subexponential except
on heavy (semantic) fibers -- i.e. there is no "third kind" of packet that is
unpruned-but-nonsemantic with `W_max=e^{Omega(N)}`. Ruling out that third kind
is #716's decomposition obligation (and #717's heavy-fiber admissibility), which
this packet interfaces with but does not prove.

### 3.3 The q-range outside the window

For `q >= q_+(chart)` (charts with `logM/logL < 3/2`), Theorem I's bound
`L^{3/2-1/q}/M` no longer vanishes and the all-signs clause is route-cut
(#728 Thm IV: adversarial signs give `sup_g R_A(g)=(L/M)Lambda*(A)` growing at
`q=inf`). Two mitigations, both stated honestly:
- **Use `q=2`.** The dichotomy's moment order is a free parameter `>=2`, and
  `q=2` is always in the window when `M>L` (every colliding chart), where the
  bound is sign-independent and exact (`R_A(g)<=L/M`). For consumers that can
  operate at `q=2`, part 3.3 is vacuous.
- If a consumer pins a large `q >= q_+`, the residual analytic input is exactly
  a **signed character-sum (Sidon) estimate** `sum_{s in S}|K_A(x-s)| = e^{o(N)}`
  on the (dissociated) occupied set -- #728's Thm IV residual, a genuine Sidon
  payment not provided by chart-free interpolation.

---

## Nonclaims

- **Not the dichotomy.** This packet does not prove #716's charge-preserving
  semantic-or-signed dichotomy, its decomposition step (3.2), or the
  heavy-fiber inverse. It proves the *signed clause for pruned packets* and maps
  the residual.
- **Not A4, not primitive Q / max-fiber flatness, not the Proximity Prize.**
- **Not a general Sidon payment.** The `q >= q_+` regime (3.3) still needs the
  signed character-sum estimate; only `q < q_+` is discharged by interpolation.
- **Heavy fibers are excluded, not paid.** `W_max = e^{Omega(N)}` packets are
  routed to the semantic side (via #716 Sec 2 / #717); the signed clause is
  neither expected nor claimed to hold for them.
- **Finite instances.** Charts 1-4 and the density/crossover tables are finite
  (`|G| <= 343`); the `q_+` formula, the density criterion, and the layer-cake
  identity are closed-form/exact. `q_+(chart)` is finite; #728's `q_+=4.199` is
  its asymptotic RATE limit, reached only as `B->inf`.
- **Label honesty.** Theorem I, Theorem D, Lemmas 1-2, and the layer-cake
  identity are PROVED (elementary functional analysis + character orthogonality,
  reproduced numerically). The reduction of the residual to "heavy-fiber +
  q>=q_+ Sidon" is a PROVED map, not a closure of those two inputs.

## Consumers

- `asymptotic_rs_mca_frontiers.tex`: the signed-minor alternative of the
  hard-input-2 dichotomy, discharged for pruned packets on ANY source chart
  passing the density criterion (not only the #717 Sec-7 family); paste-ready
  as a general proposition after #717's heavy-fiber remark and #728's
  family instance.
- #716 (`primitive_signed_payment_barrier_v1.md` Sec 6): the signed clause
  `c_i <= e^{o(N)} M/L^{1-1/q}` is supplied (Theorem D) for every pruned
  nonsemantic packet; the residual is isolated to the decomposition step and the
  heavy-fiber (semantic) branch, matching the barrier's own Sec 8 boundary.
- #717 (`heavy_fiber_admissibility_transfer.md`): the layer-cake (3.1) names
  the exact object -- `W_max=e^{Omega(N)}` fibers -- that #717's Thm 5.1 sends
  to plain emission.
- #728 (`first_match_signed_gain.md`): generalized; its family and `q_+=4.199`
  are the depth-1 rate-limit special case.
- Lean statement stub: `experimental/lean/general_pruned_signed_bound/`
  (chart-free `q_+` density criterion + depth-R window classification +
  layer-cake integer identity; the analytic `l^q` bounds are PROVED in this
  note/verifier, not in Lean -- honest Nonclaim in-package).
