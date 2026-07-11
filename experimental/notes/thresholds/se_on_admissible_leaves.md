# (S_E) versus admissibility on primitive leaves

## Status

`MAPPING PINNED (PROVED) / ADMISSIBILITY STRATIFIED (AUDIT) / (S_E) ON
BRANCH-1 (PROVED) / BRANCH-2 COLLAPSE = C7 ASSUMED INPUT (AUDIT/WALL)`.

Research packet deciding the question our **PR #614**
(`minimal_phase_supplement.md`) made decisive for input 2's **span face**:
do the frontiers paper's admissibility conditions `(A1)`--`(A7)`
(`def:admissible-sequence`, tex L896--954) already **exclude** the
`(S_E)`-violating profiles — the profiles with large dodged-band spectral
energy `E = sum_{chi in V_g^ \ (A-A)} |hat_mu(chi)|^2 = e^{Theta(N)}` on which
the master identity `L >= A_eff/(1+E)` (our #614) fails to certify the image
clause `L >= e^{-o(N)} A_eff`?

**One-line answer.** *No — not by exclusion. Admissibility ADMITS the canonical
violator (avdeev's block-parabola) as an image-normalized leaf, because its
singleton fibers make image-normalized primitive-Q trivial (the #609 escape
hatch), which satisfies the second, image-normalized branch of both `(A4)` and
`(A5)`. But that leaf carries **no span face**: `(FI)` fails exponentially and
it is **routed** as an effective-image rank-collapse profile whose projection
degree the paper leaves as an assumed enumerative input (the C7 cell,
tex L2451--2452; our #539). So the span face on the collapse class does **not**
follow from `(A1)`--`(A7)`; it rests on that same C7 assumption. `(S_E)` is the
minimal SPECTRAL hypothesis that would discharge it instead — and it is the
free `L^2`-fragment of the `(MI)`+`(MA)` payment on the OTHER `(A4)` branch,
where the span face already closes.*

Every number below is recomputed by
`experimental/scripts/verify_se_admissible.py` (stdlib-only, zero-arg,
`RESULT: PASS (208/208)`, ~0.03 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **MEASURED** (exact finite toy,
asymptotics not proved from the toy), **AUDIT** (interface reading of the tex or
a sibling note), **WALL** (identified obstruction), **OPEN**.

Credit. The block-parabola family and the `(CF*)` identities are
**avdeevvadim's** (PR #558, integrated at `e190193`). The J2 magnitude-blindness
impossibility is our **#609**; the master identity `L >= A_eff/(1+E)` and the
minimal supplement `(S_E)` are our **#614**. The `(FI)` two-gap split and the
finding that the C7 effective-image-collapse routing is an **assumed enumerative
input, not a theorem**, is our **#539** (`fi_full_image_primitive.md`),
consumed here as the routing-status audit. No LegaSage/hughes audit is consumed
in this packet beyond the #614 cross-references.

---

## Rung 1 — MAPPING: the block-parabola as a leaf (PROVED)

**The family** (avdeev #558, `asymptotic_primitive_profile_character_frame_v1.md`
L247--354): odd prime `p`, `k` disjoint blocks each `= F_p`, exactly one
selected point per block, blockwise two-moment phase

```
   Omega_k = (F_p)^k,  N_k = pk,  m_k = k,
   Phi_k(t_1,...,t_k) = ((t_1,t_1^2),...,(t_k,t_k^2)) in G_k = (F_p^2)^k.
```

**Leaf dictionary** (`sec:primitive-leaf`, tex L4789--4863; verifier BLOCK A):

| leaf object | tex symbol | value for the k-block family |
|-------------|-----------|------------------------------|
| active coordinate set `T` | `abs T = N` (L4792) | `N = pk` |
| support size | `m` (L4793) | `m = k` (one per block) |
| density | `m_N/N` (A3, L916) | `1/p` (fixed in `(0,1)` for fixed `p`) |
| prefix map | `Phi(x)=sum_t x_t(t,...,t^R)` (9.1, L4818) | per-block `(t,t^2)` |
| prefix depth | `R = w = a-K` (L4829) | `R = 2` per block; `R_prod = 2k` global |
| effective span | `V_g = Span_Fp{g(t)-g(t_0)}` (EF1, L2860) | `= G_k`, `rank_Fp = 2k` (det 2 != 0) |
| span size | `A_eff = abs V_g` | `A_eff = p^{2k}` |
| realized image | `S = Phi(Omega)`, `L = abs S` | `L = p^k` (injective, `M = L`) |
| ambient codomain | `A = abs B^R` | `A = p^{2k}` (`B=F_p`, `R=2k`) |
| image scale | `barN^img = M/L` | `= 1` |

So `A_eff = A = p^{2k}` (no Gap-2 span/ambient collapse) but
`L = p^k << A_eff` (**Gap-1 effective-image collapse** by the exact factor
`A_eff/L = p^k`), tex L4850, L877. This is the canonical
`(S_E)`-violator: `E = p^k - 1` (verifier BLOCK C).

**The chart is per-block, not the paper's global power-sum map (PROVED,
decisive).** The paper's primitive-leaf chart (9.1) is the **single global**
power-sum map `Phi(x) = sum_{t in T} x_t (t,t^2,...,t^R)`, whose coordinates
are the symmetric power sums `p_j(S) = sum_{t in S} t^j` of the *whole* support.
Those are symmetric and **cannot recover** the per-block assignment
`(t_1,t_1^2;...;t_k,t_k^2)`. To realize the block-parabola image one needs the
**block partition**: either (i) `R_prod = 2k` per-block prefix equations, or
(ii) the block-occupancy profile as extra chart data. Consequently the
block-parabola is **not** an unprofiled global-power-sum leaf; its faithful
single-leaf reading carries the block profile. Under any bounded-`R` global
chart the collapse **disappears** (verifier BLOCK E: profiled and unprofiled
slices both have collapse ratio `<= q`, far below `p^k`). **The exponential
collapse is a feature of the per-block chart / block PROFILE, not of any
primitive global-power-sum leaf.**

**Routing target: the C7 effective-image-collapse cell** (tex L2440--2454;
`Saturation and effective-image-collapse cells`). The block-occupancy is a
structured folding whose realized image is "exponentially fewer boundary values
than its ambient codomain" (L2453) — exactly this cell. avdeev's own note flags
it (L352--354): *"its visible block occupancy may be routed by an earlier
structural cell in the final atlas."*

---

## Rung 2 — ADMISSIBILITY TEST: per-condition verdict (AUDIT)

Read the k-block family (fixed odd `p`, `k -> infinity`) as a candidate leaf of
a ledger-admissible sequence and test every printed condition. The pivotal fact
is that **every image-normalized escape clause is satisfied** because the
fibers are singletons (`max_s f_s = 1 = barN^img`, verifier BLOCK G), so
image-normalized primitive-Q (`def:primitive-q`, L4912) holds trivially with
`kappa = 1` — this is precisely the #609 escape.

| cond | anchor | verdict | reason |
|------|--------|---------|--------|
| **(A1)** structured/circle domains, complete uniform fibers | L901--904 | **SATISFIED** | `k` disjoint `F_p` blocks with one-per-block occupancy = a uniform folding tower with complete fibers |
| **(A2)** first-match atlas, `e^{o(n)}` profiles, algebraic cells `<= e^{o(n)} E_n` | L905--911 | **SATISFIED-BY-ROUTING** | the block-occupancy is routed to the C7 collapse cell (L877--881) — but C7's projection degree is an **assumed enumerative input** (L2451--2452, #539). Conditional. |
| **(A3)** image normalization; `m_N/N in [alpha,1-alpha]`; `log L_N/q_N=o(N)`; ambient scale needs `(FI)` | L912--923 | **SATISFIED (image-norm only)**; **(FI) rider VIOLATED** | density `1/p` OK; but `(FI): L>=e^{-o}A_eff` fails (`p^k<<p^{2k}`), so the span/ambient scale is **barred** — leaf is locked to image scale (consistent with #609) |
| **(A4)** `(MI)`+`(MA)` on `V_g`, **or** image-normalized Sidon payment | L924--934 | **branch-1 VIOLATED; branch-2 SATISFIED** | `(MI)` minor aggregate `= C_p^k - 1 = e^{Theta(N)}` (#558's own `kappa_abs`), fails; but the image-normalized Sidon payment (`def:sidon-paid-cell`, L5130) is **trivial** for singleton fibers, so `(A4)` holds via branch-2 |
| **(A5)** power-sum columns need `R_N < char B_N`; else elementary coords **or** a direct Sidon/Q theorem | L935--941 | **`R<char` VIOLATED; direct-Q escape SATISFIED** | single-leaf chart has `R_prod = 2k >= p` for `k >= ceil(p/2)` (verifier BLOCK A,E), so `R<char` fails; but the "direct Sidon/Q" escape is met by the same trivial image-normalized Q |
| **(A6)** `(RC)` on residual shift-pair / balanced-core charts | L942--945 | **N/A** | singleton-occupancy blocks produce no residual shift-pair or balanced-core chart |
| **(A7)** profile envelope incl. all quotient subfields | L946--952 | **SATISFIED** | the block-occupancy sits as a profile term in `E_n(a_n)` |
| **(FI)** span face `L >= e^{-o(N)} A_eff` | L875, L4844 | **VIOLATED** exponentially | `L/A_eff = p^{-k} = e^{-Theta(N)}` — the whole point (#609/#614) |

**Verdict of the table (AUDIT).** No printed admissibility condition **excludes**
the block-parabola: every one has a satisfied route, all routed through the
image-normalized escape (singleton fibers). It is a bona-fide **admissible
image-normalized leaf**. What it lacks is `(FI)` — the span face — and
admissibility does **not** require `(FI)` of it: `(A2)`/`(A3)` **route** it as an
effective-image rank-collapse profile, and that routing is the C7 assumed
enumerative input, not a theorem. **Admissibility does not exclude the
`(S_E)`-violating profile; it shunts it to the assumed-input cell.**

---

## Rung 3 — THE THEOREM (stratified: PROVED on branch-1, WALL on branch-2)

The two `(A4)` branches split the admissible leaves by normalization, and
`(S_E)` is decided on each.

### T1 (PROVED). `(A4)`-branch-1 admissible leaves satisfy `(S_E)` for free.

On any admissible primitive leaf paid through branch-1 (`(MI)`+`(MA)` on the
effective span), write `mu(z) = N_g(z)/M`, `M = binom(N,m)`, so
`hat_mu(chi) = e_m(chi(g(t)-g(t_0)))/M` and `abs hat_mu(chi) <= hat_mu(1) = 1`.
Then, using `L^2 <= L^1` because `abs hat_mu <= 1`,

```
   E = sum_{1 != chi in V_g^} |hat_mu(chi)|^2
     <= sum_{1 != chi in V_g^} |hat_mu(chi)|
      = M^{-1} sum_{1 != chi} |e_m(chi(g(t)-g(t_0)))|
      = M^{-1} ( (MI-sum) + (MA-sum) )  <=  e^{o(N)},           (T1)
```

by `(MI)` (L3086) and `(MA)` (L2990). **Hence `(S_E)` holds.** Equivalently,
`(S_E)` is exactly the `L^2`-fragment of branch-1's `L^1` payment
`(EFP)`/`(MI)`+`(MA)` (`def:effective-fourier-payment`, L2936). And branch-1
already delivers the span face directly: `prop:effective-mi-ma-flatness`
(L3097--3110) gives `EF5` **and** "the realized image has size at least
`e^{-o(abs T)} A_eff`". So on branch-1 leaves `(S_E)` is **redundant** — the
span face is already free (this is #539's Gap-1 = effective-scale Q). Verifier
BLOCK D recomputes `E <= L^1` aggregate on the parabola factors and on random
measures; BLOCK G ties it to the branch split.

### T2 (AUDIT / PROVED-negative). Admissibility admits an `(S_E)`-violating leaf.

The block-parabola is admissible via branch-2 (Rung 2), violates `(S_E)`
exponentially (`E = p^k - 1`, verifier BLOCK C), and has no span face
(`L/A_eff = p^{-k}`). **Therefore `(S_E)` is NOT implied by `(A1)`--`(A7)`.**
Its span face is discharged only by the C7 collapse routing (L2451--2452),
which #539 identified as an assumed enumerative input of the same class as the
`(A2)` atlas-exhaustiveness assumption — **not** a theorem.

### T3 (PROVED, structural). The violating class is exactly the collapse PRODUCTS.

`E + 1 = A_eff * P_2` (Parseval, `P_2 = sum_z mu(z)^2`) is **multiplicative**
across independent product factors: `E(X x Y) + 1 = (E_X+1)(E_Y+1)`
(verifier BLOCK C, exact through `k=4`). A single admissible factor is
subexponential:

- a single block (`R=2 < char = p`, non-Artin-Schreier phase, Weil holds) has
  `E_1 = p - 1 = O(N)`, so `log(1+E_1)/N = log(p)/p -> 0` — **`(S_E)` HOLDS**
  (verifier BLOCK D, monotone decay `p in {3,...,127}`);
- more generally every census single leaf (free `m`-subsets, global power-sum
  map, `R < char`) has polynomially-small `E` (verifier BLOCK F).

The exponential `E = p^k - 1` requires the **`k`-fold product**, i.e. the
block-occupancy PROFILE, whose faithful single-leaf chart has `R_prod = 2k >=`
char (fails `(A5)`'s `R<char`) and whose collapse is invisible to any bounded-`R`
global chart (BLOCK E). **No single admissible primitive power-sum leaf
(bounded `R < char`, non-Artin-Schreier) violates `(S_E)`.** The two named
residual mechanisms of #614 are exactly the two ways out of branch-1, and both
are handled *outside* the primitive-leaf class:

1. **Artin-Schreier-degenerate phases** (`def:artin-schreier-phase`, L2800;
   the `p=2` parabola, where `t^2=t` makes the phase linear). These are
   **annihilator modes** on `V_g` (`lem:constant-modes-annihilator`, L2957):
   they are trivial on the effective span and drop out of the effective sum, so
   effective normalization already removes them.
2. **Effective-image collapse** (block-parabola, odd `p`). A **product /
   profile** phenomenon, routed to C7 — the assumed enumerative input.

### Consequence for the span face

- **Branch-1 leaves:** span face **closes** (free, `prop:effective-mi-ma-flatness`;
  `(S_E)` redundant).
- **Branch-2 collapse profiles:** span face does **NOT** follow from
  `(A1)`--`(A7)`. It requires **either** the C7 enumerative-input assumption
  (status quo, #539) **or** a printed hypothesis. `(S_E)` (or `(FI)` itself) is
  that hypothesis; since the parabola violates `(S_E)`, printing `(S_E)` would
  **route the collapse profiles out** (they have no span face and would no longer
  claim one) — consistent and clean.

**This is the refined counterexample-class steering of Rung 3(b): the paper
cannot get the image clause on the collapse class from admissibility alone; it
needs a printed hypothesis, and it currently supplies one implicitly as the C7
assumed enumerative input.** `(S_E)` is the explicit, checkable, spectral form
of that same input, and it is free (redundant) on all branch-1 leaves.

### The exact next atomic lemma (WALL)

> **Conjecture (routing = spectrum).** Every `(S_E)`-violating admissible leaf
> is non-primitive: it is caught by first-match and routed to the C7
> effective-image-collapse cell. Equivalently, every primitive residual
> satisfies `(S_E)`.

The block-parabola **supports** the conjecture (it is a block-occupancy profile
routed to C7). Proving it **is** paying the C7 projection degree — the assumed
enumerative input (L2451--2452). So the conjecture is the C7 assumption restated
spectrally; discharging it is the honest wall. If proved, `(S_E)` holds on all
primitive residuals and the span face closes on primitives with no new
hypothesis.

---

## Rung 4 — CENSUS: dodged-band energy across admissible toy leaves (MEASURED)

Verifier BLOCK F, exact `E = A_eff * P_2 - 1`, single admissible power-sum
leaves (prime field `F_p`, free `m`-subsets, global power-sum map, `R < p`):

| p | N | R | m | L | A_eff | E | `log(1+E)/N` | `(S_E)` |
|---|---|---|---|---|-------|---|--------------|---------|
| 3 | 2 | 1 | 1 | 2 | 3 | 1/2 | 0.203 | HOLDS |
| 5 | 2 | 1 | 1 | 2 | 5 | 3/2 | 0.458 | HOLDS |
| 5 | 3 | 1 | 2 | 3 | 5 | 2/3 | 0.170 | HOLDS |
| 5 | 3 | 2 | 2 | 3 | 25 | 22/3 | 0.707 | HOLDS |
| 7 | 3 | 1 | 2 | 3 | 7 | 4/3 | 0.282 | HOLDS |
| 7 | 4 | 2 | 2 | 6 | 49 | 43/6 | 0.525 | HOLDS |
| 7 | 5 | 2 | 2 | 10 | 49 | 39/10 | 0.318 | HOLDS |

Single leaves: `E` is polynomial and `log(1+E)/N` **decays** as `N` grows at
fixed structure. Contrast — the parabola PRODUCT rows (`E = p^k - 1`,
`log(1+E)/N = log(p)/p` **constant `> 0`**, exponential):

| p | k | N=pk | L=p^k | A_eff=p^{2k} | E=p^k-1 | `log(1+E)/N` |
|---|---|------|-------|--------------|---------|--------------|
| 3 | 1 | 3 | 3 | 9 | 2 | 0.366 |
| 3 | 2 | 6 | 9 | 81 | 8 | 0.366 |
| 3 | 4 | 12 | 81 | 6561 | 80 | 0.366 |
| 5 | 4 | 20 | 625 | 390625 | 624 | 0.322 |
| 7 | 4 | 28 | 2401 | 5764801 | 2400 | 0.278 |

**Empirical content.** Single admissible leaves have a **decaying** dodged-band
energy rate; the parabola family sits at a **constant positive** rate
`log(p)/p`, the signature of the `k`-fold product. `(S_E)` is a
product-multiplicativity phenomenon, not a single-leaf pathology.

---

## Verdict ledger

| item | verdict | label |
|------|---------|-------|
| parabola -> leaf: `N=pk`, `m=k`, `R_prod=2k`, `A_eff=A=p^{2k}`, `L=p^k` | mapping exact | **PROVED** (BLOCK A) |
| per-block chart is not the global power-sum map; collapse is profile-induced | global chart shows no exp collapse | **PROVED** (BLOCK E) |
| admissibility `(A1)`--`(A7)` does NOT exclude the parabola (image-norm leaf) | every escape via singleton-fiber Q | **AUDIT** (Rung 2) |
| `(A4)`-branch-1 `(MI)`+`(MA)` `=> (S_E)` (`L^2 <= L^1`) | one Cauchy-Schwarz line (T1) | **PROVED** (BLOCK D/G) |
| span face free on branch-1 (`prop:effective-mi-ma-flatness`) | redundant with `(S_E)` there | **AUDIT/PROVED** |
| `(S_E)` NOT implied by `(A1)`--`(A7)`; parabola admissible + violates it | branch-2 escape | **PROVED-negative** (T2) |
| `E+1` multiplicative; single leaf subexp, product exponential | `E=p^k-1`, `L=A_eff/(1+E)` tight | **PROVED** (BLOCK C) |
| violating class = collapse products = C7 profiles = assumed enumerative input | `#539` routing status | **AUDIT/WALL** (T3) |
| conjecture: `(S_E)`-violator `=>` non-primitive (routed) `<=>` C7 projection degree | next atomic lemma | **OPEN/WALL** |

**Proposed ledger entry (for the maintainer).** *Alongside #614's pinning of the
minimal supplement `(S_E)`: on the `(MI)`+`(MA)` branch of `(A4)`, `(S_E)` is the
free `L^2`-fragment of the printed `L^1` payment and the span face already closes
(`prop:effective-mi-ma-flatness`). On the image-normalized-Sidon branch of
`(A4)`, admissibility admits `(S_E)`-violating effective-image-collapse leaves
(avdeev's block-parabola), and the span face for them is not implied by
`(A1)`--`(A7)`: it is discharged only by the C7 effective-image-collapse routing,
an assumed enumerative input (#539). Print either the C7 projection-degree bound
or the spectral hypothesis `(S_E)` (`sum_{chi in V_g^ \ (A-A)} |hat_mu|^2
<= e^{o(N)}`) as the input that pays the span face on the collapse class; `(S_E)`
routes the block-parabola out. This is an OPEN input, not an established fact —
the packet pins WHICH input and that admissibility does not already supply it.*

### The 2-3 steps the PI should re-derive

1. **T1, the one-line implication (branch-1 `=> (S_E)`).** With
   `abs hat_mu(chi) <= 1`, `E = sum |hat_mu|^2 <= sum |hat_mu| = M^{-1}(`MI-sum`
   + `MA-sum`) <= e^{o(N)}`. Confirm `(S_E)` is the `L^2`-fragment of the `L^1`
   payment `(A4)` already demands, and that `prop:effective-mi-ma-flatness`
   already gives the span face there (so `(S_E)` is redundant on branch-1).
2. **The escape (branch-2), Rung 2.** Confirm the block-parabola's singleton
   fibers make image-normalized primitive-Q trivial (`max_s f_s = 1 = barN^img`),
   satisfying the image-normalized escape clauses of both `(A4)` and `(A5)`;
   so admissibility does not exclude it, yet `(FI)` fails (`p^k << p^{2k}`) and it
   is routed to the C7 cell (L2451--2452) — the assumed enumerative input.
3. **T3, multiplicativity.** Confirm `E+1 = A_eff*P_2` is multiplicative, a
   single block has `E = p-1 = O(N)` (`(S_E)` holds), and only the `k`-fold
   product blows `E` to `p^k-1`; hence the violator is a profile
   (`R_prod = 2k >= char`), not a primitive global-power-sum leaf.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_se_admissible.py   # RESULT: PASS (208/208)
```
