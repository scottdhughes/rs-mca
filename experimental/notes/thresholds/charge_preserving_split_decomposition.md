# The positive-rooted split decomposition: the fourth charge condition is free, the residual is cardinality — a route-scoped decision of the dichotomy's decomposition step

## Status

```text
Status: PROVED (fourth charge condition is FREE with B_i=A, all pieces, all q>=2)
        + PROVED (all four #716 charge conditions hold for the layer-cake +
        heavy/light split, common band A) + PROVED route-cut COUNTEREXAMPLE
        (the split is NOT an e^{o(N)}-piece decomposition in general; the genuine
        obstruction is CARDINALITY, not the fourth condition) + a first exact
        POSITIVE SEMANTIC EMISSION instance (superincreasing heavy fiber).
HARD INPUT 2 SERVED: the DECOMPOSITION step of avdeevvadim's #716 charge-
        preserving semantic-or-signed dichotomy (Sec 6) -- the last structural
        clause left open after #717 (heavy-fiber admissibility) + #728/#729
        (pruned signed clause + layer-cake).
Verdict per sub-question (route-scoped):
  (i)   Does B_i = A suffice for the fourth condition ||P_{B_i} b_{U_i}||_q >= c_i?
        YES, UNCONDITIONALLY, for every piece of any partition of a positive-
        rooted packet, when c_i = sum_{S in U_i} omega(S).  The global P_A-norming
        dual g is a feasible test function in the duality definition of ||.||_q:
        c_i = Re<P_A b_{U_i}, g> <= ||P_A b_{U_i}||_q ||g||_{q'} = ||P_A b_{U_i}||_q.
  (ii)  Is #716's per-piece K_N-band pigeonhole needed to recover it?  NO -- (i)
        already gives the fourth condition with the single original band A.
  (iii) Is there a genuine obstruction?  YES, but it is NOT the fourth condition
        and NOT any charge condition -- it is the PIECE COUNT.  The split has
        #{heavy fibers} + Wmax_light pieces; minimized over the threshold this is
        Theta(min over the fiber-size staircase), which a heavy fiber + flat
        exponential tail forces to min(L, M/L) = e^{Omega(N)}.  So on
        exponential-image charts the split violates #716's "at most e^{o(N)}
        packets".  The split DOES satisfy, unconditionally, all four charge
        conditions + the per-piece semantic/signed classification.
  Prop 6.1 re-read: it uses the fourth condition at FULL strength (to turn the
        charge-concentration c_i >= e^{-o(N)} Omega_+ into R_{B_i} >= e^{-o(N)} R_A,
        then Y_B >= R_B^q one-way).  The split supplies that for free; the ONLY
        thing it does not guarantee is Prop 6.1's e^{o(N)} SEMANTIC packets.
  Corrected statement (hypothesis-visible): the split IS #716's decomposition,
        and Prop 6.1 goes through, IFF the positive profile is staircase-
        concentrated (e^{o(N)} fibers above a threshold T_h with subexponential
        multiplicity below) -- automatic when L=e^{o(N)}, equivalent to the
        max-fiber concentration question when L=e^{Theta(N)}.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**. Every number below is
recomputed by
`experimental/scripts/verify_charge_preserving_split_decomposition.py`
(stdlib only, deterministic, exact `Fraction` over `G=F_2^k` at `q=2` and
exact-Parseval over `Z_C` for the superincreasing family; `RESULT: PASS (57/57)`,
`--tamper-selftest` catches `1/1`, ~4.4 s). Machine-readable certificate:
`experimental/data/certificates/charge-preserving-split-decomposition/charge_preserving_split_decomposition.json`.
No `.tex`/`.pdf` is edited.

## Interfaces

- **avdeevvadim's #716**
  (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`).
  The whole target is his: the **charge-preserving semantic-or-signed
  dichotomy** (Sec 6), its four charge conditions `c_i>=0`, `sum c_i=Omega_+`,
  `c_i<=sum_{S in U_i} omega(S)`, `||P_{B_i} b_{U_i}||_q >= c_i`, the signed
  clause `c_i<=e^{o(N)} M/L^{1-1/q}`, the point-mass reduction (Prop 1.1) and
  uniform positive owner rooting (Sec 2, `omega(S)=Re conj((P_A g)(Phi(S)))`),
  the band count `K_N=2+ceil(log2 N)`, and **Prop 6.1** (the dichotomy implies
  same-owner semantic emission on a failure).  This packet answers the exact
  warning he flags in Sec 6 -- *"If the charges are defined by signed character
  correlations, their nonnegativity and exact sum are part of the theorem, not
  inferred from an overlap census"* -- by showing that warning does NOT bite for
  genuinely positive-rooted packets, and locating the true residual (Sec 3).
- **#717**
  (`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`).
  Its Theorem 5.1 (hereditary reduces to plain emission on the locator-prefix
  chart under (H1)-(H4)) is what makes each extracted heavy point mass a
  SEMANTIC candidate; its Sec 7 superincreasing family (`A_i=5^i`,
  `C=2 sum A_i+1`, `T={A_i} u {C-A_i}`, `a=B`, `Phi=sum mod C`) is the bonus
  instance; its Lemma 2.1 (whole-residual band failure) is why a failure forces
  a heavy fiber.
- **#729**
  (`experimental/notes/thresholds/general_pruned_signed_bound.md`).
  Theorem I (`R_A(g) <= L^{3/2-1/q}/M`, i.e. `||P_A g||_q <= sqrt(L)` for a
  pruned signed sub-mask), Theorem D (pruned packets pay the signed clause on a
  density-passing chart), the **layer-cake identity** (`b = sum_{j=1}^{Wmax} g_j`
  into pruned layers) and the density criterion `q_+(chart)=1/(3/2-logM/logL)`
  are all #729's.  This packet uses the layer-cake as a literal *piece-split*
  and finds exactly where that piece-count breaks.
- **#728**
  (`experimental/notes/thresholds/first_match_signed_gain.md`).
  The depth-1 superincreasing instance of Theorem I and the twin-pair
  dissociativity `S = union_{i in P}{A_i, C-A_i}, |P|=B/2` mapping to `0` are
  #728's; that structure is the planted template the bonus emits.

---

## 1. Setup (all #716 / #717 / #729)

`G` a finite abelian group, `H=|G|`, `Phi: Omega^0 -> G` a chart on a full slice
`Omega^0` (`M=|Omega^0|`), occupied set `Phi(Omega^0)` of size `L`. `f` the
count function of a residual/slice mask, `A subseteq hat G\{0}` a band, `P_A` the
(self-adjoint, idempotent) band projection, `R_A(f)=(L^{1-1/q}/M)||P_A f||_q`
the normalized excess, `q>=2`.

**Positive-rooted packet (#716 Sec 2 / Prop 6.1).** Fix the `P_A`-norming dual
`g` of `f`: `||g||_{q'}=1`, `<P_A f, g>=||P_A f||_q`. The owner weights are
`omega(S)=Re conj((P_A g)(Phi(S)))`; they are constant on a `Phi`-fiber, and
`sum_S omega(S)=Re<P_A f,g>=||P_A f||_q=R_A(f)*(M/L^{1-1/q})`. The **positive-
rooted packet** is `b_+ = f` restricted to the occupied set `{s: omega_s>0}`,
with `Omega_+=sum_{s: omega_s>0} f(s) omega_s >= R_A(f)*(M/L^{1-1/q})` (#716's
"exact positive correlation"). For a genuine failure `R_A(f)>=e^{eta N}`.

**The split under test (task's proposal, from #729).** Fix a threshold `T_h`.
Extract every heavy positive fiber `f(s) 1_s` with `f(s)>=T_h` as a **heavy point
mass**; layer-cake the light positive remainder `b_L = f*1_{omega>0, f<T_h}` into
its `Wmax_light = max_{s} b_L(s)` **pruned layers** `g_j=1_{b_L>=j}` (one support
per syndrome, `|g_j|<=1`). Assign each piece its **natural charge**
`c_i = sum_{S in U_i} omega(S)`.

---

## 2. The fourth condition is FREE with B_i = A (Theorem A, PROVED)

### Theorem A (per-piece norm-compatibility is automatic)

Let `b_+` be a positive-rooted packet with norming dual `g` (`||g||_{q'}=1`),
and let `{U_i}` be ANY partition of its support multiset into pieces with masks
`b_{U_i}` (`b_{U_i}(s)=#{S in U_i: Phi(S)=s}>=0`) and natural charges
`c_i=sum_{S in U_i} omega(S)`. Then, with the **common band `B_i=A`**, all four
#716 charge conditions hold:

```text
(C1) c_i >= 0                                  [omega_s>0 on b_+]
(C2) sum_i c_i = Omega_+                        [partition]
(C3) c_i <= sum_{S in U_i} omega(S)             [equality, by definition]
(C4) c_i <= ||P_A b_{U_i}||_q                   [duality; see below]
```

**Proof of (C4).** `P_A` is self-adjoint and `P_A g` reproduces the pointwise
weights: `omega_s=Re conj((P_A g)(s))`, so
`c_i = sum_s b_{U_i}(s) omega_s = Re<b_{U_i}, P_A g> = Re<P_A b_{U_i}, g>`.
The `q`-norm has the duality representation
`||P_A b_{U_i}||_q = sup_{||phi||_{q'}<=1} Re<P_A b_{U_i}, phi>`, and `g` is a
**feasible** test function (`||g||_{q'}=1`), hence
`||P_A b_{U_i}||_q >= Re<P_A b_{U_i}, g> = c_i`. `square`

**Why this settles the "hard part".** #716 Sec 6 warns that for charges defined
by signed character correlations, nonnegativity and exact sum are *part of the
theorem*. Theorem A shows this warning does **not** bite for a genuinely
positive-rooted packet: because `omega>0` pointwise, (C1)-(C3) are free from the
partition, and (C4) -- the clause #716 singles out -- is free from a *single*
inequality, `g feasible`, with **no per-piece band search**. Sub-question (i):
**YES**; sub-question (ii): the `K_N`-band pigeonhole is **not needed** for (C4).

**Verification (exact, `G=F_2^k`, `q=2`).** On the `F_2^6` XOR/moment chart
(`H=64`, `M=3876`, `L=32`, band `|A|=20`), the split at `T_h=123` produces
**135 pieces** (13 heavy point masses + 122 pruned layers). Every piece
satisfies (C4) with strict slack (`min ||P_A b_{U_i}||_2^2*||h||_2^2 - c_i^2*(...)
= 237343 > 0`, exact `Fraction`), (C2) holds to `0` exactly, and the layer-cake
identity `b_L = sum_j g_j` is exact. Not a `q=2` artifact: the same 135-piece
split satisfies (C4) numerically at `q in {2,3,4}` with strict slacks
`0.627 / 0.400 / 0.334` and `charge_sum = Omega_+` to machine precision (the dual
is `g=|h|^{q-2}h/||h||_q^{q-1}`; the duality proof is `q`-agnostic).

**Signed clause for the layers (PROVED, from #729).** Each pruned layer `g_j` is
a signed sub-mask on a pruned support, so #729 Theorem I gives
`||P_A g_j||_q <= sqrt(L)`, hence by (C4) `c_j <= ||P_A g_j||_q <= sqrt(L) <=
e^{o(N)} M/L^{1-1/q}` on any chart passing the density criterion
`L^{3/2-1/q} <= e^{o(N)} M` (`q<=q_+`). Verified `||P_A g_j||_2^2 <= L` on every
layer. So **the pruned pieces pay the signed clause**, and **the heavy pieces are
semantic candidates** (#717 Thm 5.1). The split is a *bona fide* four-condition,
semantic-or-signed-classified charge-preserving decomposition -- **per piece**.

---

## 3. The genuine residual is CARDINALITY (COUNTEREXAMPLE, PROVED)

The split satisfies every *local* (per-piece) requirement. What it does not
control is #716's **global** clause: *at most `e^{o(N)}` packets*.

### Piece count of the split

At threshold `T_h` the number of pieces is
```text
P(T_h) = #{s in b_+ : f(s) >= T_h}   (heavy point masses)
       + max{ f(s) : s in b_+, f(s) < T_h }   (pruned layers = Wmax_light).
```
`min_{T_h} P(T_h)` is `Theta` of the "staircase gap" of the positive fiber-size
multiset.

### Proposition 3.1 (spread tails defeat the split, exact)

There is a positive fiber-size profile -- **one heavy fiber `W` plus `K` flat
tail fibers of size `D`** -- for which
```text
min_{T_h} P(T_h) = min(K, D) + 1.
```
Taking `K=D=2^m` (and `W=2^{2m}` so the head is strictly dominant) gives
`M = W + KD = 2^{2m+1}`, `L=2^m+1`, and
```text
min_{T_h} P(T_h) = 2^m + 1 = Theta(sqrt(M)) = e^{Omega(N)}   when M=e^{Theta(N)}.
```

**Proof / verification.** For `m=4,5,6,7`: `min_pieces = 17,33,65,129 = 2^m+1`,
exactly `min(L, floor(M/L))`, strictly growing (exact integer check). At any
`T_h` you either keep all `2^m` tail fibers heavy (`>=2^m` point masses) or
layer-cake a size-`2^m` fiber (`2^m` layers): there is no threshold with both
counts subexponential. `square`

This is realized by an actual chart too: the `F_2^6` XOR chart of Sec 2 is
near-flat (positive part = a size-148 head over a plateau of size-126 fibers),
and its split already needs **135 pieces at `M=3876`**, scaling as `min(L,M/L)`.

### Why a failure packet does not rescue the count

A failure on a density-passing chart *does* force one heavy fiber
(`Wmax >= e^{eta N} M/L^{3/2-1/q}`, #729 Sec 3.1 / #717 Lemma 2.1 -- the layer-
cake upper bound run backwards). But the failure is caused by that **one** fiber;
the remaining `Omega_+ - (head charge)` may be spread adversarially over
`e^{Omega(N)}` medium fibers, so `min_{T_h} P(T_h)` stays `e^{Omega(N)}`. Feeding
the necessary conditions of Prop 6.1 through the split (`#heavy = e^{o(N)}` AND
signed-charge sum `<= e^{o(N)} M/L^{1-1/q}`, i.e. `T_h`-window
`M e^{-o(N)} <= T_h <= e^{o(N)} M/L^{3/2-1/q}`) is feasible **iff
`L = e^{o(N)}`**. Hence:

```text
L = e^{o(N)}      : the split is ALWAYS an e^{o(N)}-piece decomposition
                    (#heavy <= L = e^{o(N)} free; take T_h=e^{o(N)});
L = e^{Theta(N)}  : the split is an e^{o(N)}-piece decomposition IFF the positive
                    profile is staircase-concentrated -- which can FAIL (Prop 3.1).
```

**CORRECTION (2026-07-13, superseding the original print of this paragraph;
see the staircase classification packet, PR #739).** The original text here
called the `#717`/`#728` superincreasing family "concentrated (Sec 5)". That
was a small-`B` (`B<=8`) crossover artifact: #739's exact classification
(`|fiber| = C(B-s,(B-s)/2)` across `C(B,s)*2^s` syndromes per level `s`)
proves the family's heavy fibers are exponentially ABUNDANT --
`#{fiber >= e^{eta N} M/L} = e^{Theta(N)}` for every `eta < ln(3/2)/2` -- and
Sec 5's own piece count `1 + C(B-2,(B-2)/2)` is already exponential. The
family is therefore on the BAD side of Theorem B's dichotomy: the
fiber-indexed split is NOT an `e^{o(N)}`-piece decomposition there. Theorems
A and B of this note are unaffected (the correction concerns only which side
this example lands on). Which side an *actual atlas failure packet* lands on
is exactly the max-fiber / profile-envelope hard input -- open, and #739 shows
the answer is class-dependent.

---

## 4. Prop 6.1 re-read and the corrected decomposition statement

**Does Prop 6.1 use (C4) in full strength?** Yes. Its chain is: charge
concentration `c_i >= e^{-o(N)} Omega_+` (from `e^{o(N)}` semantic packets
carrying `(1-o(1))Omega_+`), then **(C4)** `R_{B_i}(b_{U_i})=||P_{B_i}b_{U_i}||_q
/(M/L^{1-1/q}) >= c_i/(M/L^{1-1/q})` to get `R_{B_i}(b_{U_i}) >= e^{-o(N)} R_A(f)`,
then the one-way gate `Y_{B_i} >= R_{B_i}^q`. So (C4) is load-bearing as a
**norm lower bound by the charge** -- exactly what Theorem A supplies for free.

**Consequently the split meets Prop 6.1's (C4) need for every piece.** The ONLY
Prop-6.1 hypothesis the split does not itself guarantee is *`e^{o(N)}` semantic
packets*. The split's semantic packets are its heavy fibers, so:

### Theorem B (corrected decomposition, hypothesis-visible)

Let `b_+` be a positive-rooted failure packet on chart `Phi` (dual `g`,
`q>=2`), and suppose the density criterion `L^{3/2-1/q}<=e^{o(N)}M` holds. Fix a
threshold `T_h` and take the heavy/light split of Sec 1 with natural charges and
common band `A`. Then:
1. (C1)-(C4) hold for every piece (Theorem A); each pruned layer pays the signed
   clause `c_i<=sqrt(L)<=e^{o(N)}M/L^{1-1/q}` (#729 Thm I); each heavy point mass
   is an admissible rooted packet, hence a semantic candidate, under #717
   (H1)-(H4).
2. The decomposition realizes #716 Sec 6 (`<= e^{o(N)}` packets) **and** Prop 6.1
   IF AND ONLY IF `#{s in b_+: f(s)>=T_h} = e^{o(N)}` and
   `max{f(s): s in b_+, f(s)<T_h}=e^{o(N)}` for some such `T_h`
   (**`T_h`-staircase-concentration** of the positive profile).
3. Condition 2 holds automatically when `L=e^{o(N)}`; when `L=e^{Theta(N)}` it is
   equivalent to `e^{o(N)}` heavy positive fibers -- the max-fiber concentration
   question -- and can fail (Prop 3.1).

**What the split satisfies unconditionally** (the weaker true statement): a
charge-preserving decomposition into `#{heavy} + Wmax_light` pieces meeting
(C1)-(C4) with band `A`, semantic-or-signed classified. The dichotomy's *content*
is thereby sharpened: it is NOT the fourth condition (free) nor charge sign/sum
(free) -- it is precisely the **staircase-concentration / max-fiber** count.

---

## 5. Bonus: a first exact positive semantic emission (superincreasing heavy fiber)

Instantiate the whole split on the #717 Sec 7 / #728 superincreasing family
(`Phi=sum mod C`), `B in {2,4,6,8}`. The heavy fiber `Phi^{-1}(0)` is the
balanced subset-sum level set, `W=C(B,B/2)`. Exactly (verified):

| B | N | M=C(2B,B) | L=(3^B+1)/2 | W=C(B,B/2) | max\|S∩S'\| | a-2 | split pieces |
|---|---|-----------|-------------|------------|-------------|-----|--------------|
| 2 | 4 | 6    | 5    | 2  | 0 | 0 | 2 (1 heavy + 1) |
| 4 | 8 | 70   | 41   | 6  | 2 | 2 | 3 (1 heavy + 2) |
| 6 |12 | 924  | 365  | 20 | 4 | 4 | 7 (1 heavy + 6) |
| 8 |16 | 12870| 3281 | 70 | 6 | 6 |21 (1 heavy + 20)|

**PLANTED-TEMPLATE EMISSION (exact).** Every support of the heavy fiber is a
union of exactly `B/2` twin pairs `{A_i, C-A_i}`:
`Phi^{-1}(0) = { union_{i in P}{A_i,C-A_i} : |P|=B/2 }` (verified
`all_twin_template=True`, all `B`). This is a **repeated planted template** (one
of #716's five semantic precursors): each heavy support is the same twin-pair
template evaluated on a `B/2`-subset of the `B` pairs. It simultaneously
**saturates** the exact-agreement bound `|S cap S'| = a-2` (Johnson `>=2`) for
every `B`, so it also reads as a saturation precursor. As a genuine
decomposition instance the fourth condition holds with strict slack on the
actual failing dyadic band (`R_A(f)_{q=2}=1.02` at `B=4`, `0.95` at `B=6`),
charge-sum `= Omega_+` exactly, and the split is concentrated (1 semantic head +
`a-2`-scale pruned tail). **This is a single exact positive emission instance:
the balanced level set emits the twin-pair planted template at its uniform
positive owner.** It does NOT prove the emission theorem in general.

---

## Nonclaims

- **The dichotomy is NOT closed, even though the decomposition step lands.** The
  semantic *emission* on the heavy fibers -- that an admissible rooted heavy fiber
  actually produces one of #716's five precursors with verifier-checkable
  parameters -- stays open (#717 gives admissibility, not emission). The bonus
  is one *instance* of emission on one family, not the theorem.
- **The split is NOT a general e^{o(N)}-piece decomposition** (Prop 3.1). Its
  sufficiency for #716 Sec 6 / Prop 6.1 is CONDITIONAL on staircase-concentration
  of the positive profile (Theorem B.2), equivalently on `e^{o(N)}` heavy fibers
  when `L=e^{Theta(N)}` -- the max-fiber question, assumed, not proved.
- **Not** a proof of primitive Q / max-fiber flatness, A4, the signed
  minor-arc/Sidon inverse for `q>=q_+`, or the Proximity Prize.
- Theorem A (fourth condition free), the four-condition/layer-cake/Theorem-I
  facts, Prop 3.1 (cardinality counterexample), and the superincreasing
  planted-template emission are PROVED (elementary duality + character
  orthogonality + exact combinatorics, reproduced by the verifier). Theorem B's
  classification is PROVED; its *applicability* to a given packet is
  CONDITIONAL on the visible concentration hypothesis.
- The density criterion `L^{3/2-1/q}<=e^{o(N)}M` (`q<=q_+(chart)`) is #729's and
  is carried as a hypothesis; the signed clause is only discharged inside it.
- Finite instances only (`|G|<=976561`); the `q_+` formula, the layer-cake
  identity, Prop 3.1's scaling, and the twin-template structure are closed-form.

## Consumers

- **#716** (`primitive_signed_payment_barrier_v1.md` Sec 6 / Prop 6.1): the
  fourth charge condition is discharged *for free* (Theorem A) for every
  positive-rooted packet, removing it from the list of things the dichotomy must
  separately establish; the residual is relocated from "signed-correlation
  charge bookkeeping" to "`e^{o(N)}` heavy-fiber cardinality" (Theorem B, Prop
  3.1). Prop 6.1's (C4) use is confirmed load-bearing and now free.
- **#717** (`heavy_fiber_admissibility_transfer.md`): the heavy point masses are
  its admissible rooted packets; the superincreasing heavy fiber it realizes is
  shown to emit a planted-template precursor (Sec 5).
- **#729** (`general_pruned_signed_bound.md`): its layer-cake is promoted from a
  norm-bounding device to a literal piece-split, and the exact point where the
  piece-count breaks (Prop 3.1, `min(L,M/L)`) is identified -- the quantitative
  form of its own Sec 3.1 "the residual is only the heavy-fiber regime".
- **#728** (`first_match_signed_gain.md`): its twin-pair dissociativity is the
  planted template emitted in Sec 5.
- `asymptotic_rs_mca_frontiers.tex`: paste-ready as the decomposition-step
  proposition after #729's layer-cake remark -- the fourth condition is free, the
  open input is max-fiber concentration, stated with visible hypotheses.
- Lean statement stub:
  `experimental/lean/charge_preserving_split_decomposition/` (Theorem A the
  duality bound + the layer-cake integer identity + the cardinality-obstruction
  scaling; statements only, honestly marked unproved-in-Lean, `lake build`
  succeeds).
