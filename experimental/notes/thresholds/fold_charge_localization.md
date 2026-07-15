# Fold-level charge triviality localizes the forced sixth alternative to a single primitive: flat-cube emission on the Sidon-paired class

## Status

```text
Status: PROVED (Thm A, any failing band, unconditional) that fold-measurable
        pieces -- unions of parity classes of the resonant-folding fold -- are
        ell^2-charge-trivial: their per-syndrome multiplicity is the
        within-class fiber size <= f_max and classes have disjoint syndrome
        sets, so K disjoint fold pieces with compatible charges carry
            sum c_i <= sqrt(K) f_max <= e^{-(eta+kappa)N + o(N)} Omega_+,
        kappa = ln(2/sqrt 3)/2 per N-unit.  This is the transverse-charge
        packet's kappa-rate WITHOUT the signed clause and WITHOUT (FR): the
        clause-based cap there gave only e^{-eta N} for quotient-style
        unions; fold pieces are now dead on the signed side at the stronger
        rate, for every band, by multiplicity alone.
      + PROVED (Thm B, exact charge ledger) at the maximal band: the level
        shares are Omega~_+(s) = C(B,s) 2^s w_s (w_s - M/c)_+ exactly;
        levels with w_s <= M/c carry ZERO charge, and ON BASE 3 (c = 3^B)
        this light threshold sits at s/B -> 1 - log2(4/3) = 0.585... -- on
        base 5, M/c -> 0 and EVERY level is heavy (no light threshold; the
        scoping matters, both bases are in scope); the localization is
        base-robust: the ledger exponent is g(sigma) = H(sigma) + 2 - sigma,
        strictly concave, interior max at sigma = 1/3, so levels
        |s/B - 1/3| >= eps carry an exponentially small fraction on BOTH
        bases (COMPUTED pins: s=2 carries 70.1% at B = 6 base 3; away-mass
        (|s/B - 1/3| >= 1/6) strictly decreasing, < 2^{-6} at B = 64;
        base-5 argmax at the same sigma = 1/3 window).
      + PROVED (Thm C, maximal band) cube flatness and the budget wall: h is
        EXACTLY constant on every class's sign-cube (equal fibers), so a
        class's ell^1 charge exceeds its single-piece ell^2 cap by exactly
        sqrt(2^s); globally, ANY ell^2-capped scheme needs
        K >= PN = Omega~_+^2 / sum f^2 h_+^2 pieces, and PN = 2^{B - o(B)}
        (the exponent identity 2 g(1/3) - max(H(sigma) + 4 - 3 sigma) = 1
        closes in closed form; finite pins 31.2 / 138.4 at B = 6 / 8, at
        least doubling per step to B = 32).  The e^{o(N)} grammar budget
        is short by e^{Theta(N)} uniformly over piece shapes.
      + PROVED (Thm D, bridge identity, any band) chi_xi restricted to a
        class's syndrome cube is the product character
        e^{-i sum_{i in U} eps_i theta_i(xi)}; hence the sign-cube Fourier
        coefficients of h on a class are the EXPLICIT theta-product
        transforms of hat f -- the same angles the resonant-folding
        certificates carry.  Maximal band: all off-empty coefficients vanish
        (float-verified to 1e-15 under the exact Parseval guard); the
        structure a paying rule must consume is exactly "certified flat
        cube".
      + The REDUCTION (maximal band): (=>) PROVED CONSTRUCTIVE -- if the
        grammar admits FLAT-CUBE EMISSION (an ell^1 rule paying
        certified-flat sign-cube structure), then <= B/2 + 1 level-block
        pieces (fold-measurable, disjoint, each level uniform: identical
        (2^s, w_s, h) data across its classes) pay Omega~_+ EXACTLY (exact
        rationals).  (<=) PROVED AS CONCENTRATION -- in any e^{o(N)}-piece
        payment, ell^2/signed pieces die (Thm A + PN) and fiber-rooted
        semantic pieces die (transverse-charge Thm 2, consumed with
        hypotheses re-checked), so (1 - e^{-delta N}) of the charge is paid
        ell^1 by non-fiber-rooted pieces on sigma ~ 1/3 levels (Thm B) whose
        cubes are flat (Thm C/D) -- exactly the structure the primitive
        pays.  A piece-SHAPE classification (surviving pieces = unions of
        FULL cubes, vs arbitrary flat-supported sets) is NOT claimed and not
        needed: anything short of ell^1 on certified-flat cube territory is
        dead.  The forced sixth alternative on this class IS the admission
        question for this one primitive.
      + AUDIT (erratum, transverse-charge packet -- the sentence appears in
        BOTH its Status/PROVED block and its Sec 5): "every fiber
        lies in [2M/L, M/sqrt L)" -- the UPPER end is universal (w_s^2 L <
        M^2 for ALL levels, re-verified to B = 64), but the LOWER end fails
        for deep-unpaired levels: w_s < 2M/L exactly on s in {4,6} (B = 6)
        and {4,6,8} (B = 8).  No theorem there consumes the universal lower
        end (heaviness enters as EXISTENCE, f_max L >= 2M, re-verified);
        the sentence should read "the heavy levels' fibers".
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- third packet of the arc: the transverse-charge
        packet FORCED the packet-scale sixth alternative, the
        resonant-folding packet TYPED its candidate object, and this packet
        REDUCES it (maximal band, this class) to one yes/no grammar
        decision: is flat-cube emission admissible?  Input-2 residual after
        this packet: that admission question (+ the unchanged large-q Sidon
        residual and the atlas-totality escape, the Codex team's lane).
        Fence (N1) (thm:aperiodic-one-ray-saturation) respected: nothing
        here pays or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Every claim below except
the bridge floats is recomputed exactly (`int`/`Fraction`) by
`experimental/scripts/verify_fold_charge_localization.py` (stdlib only,
deterministic, `RESULT: PASS (49/49)`, `--tamper-selftest` catches `5/5`,
~3.5 s); the bridge identity (V5) uses floats under the exact Parseval guard.
Machine-readable certificate:
`experimental/data/certificates/fold-charge/fold_charge_localization.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/fold_charge_localization/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `2633895`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)** -- the
ledger and PN quantify exactly how far the PO4 character bound is from
paying this class; **`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1).

Integrated in-tree packets (consumed and credited, not reproved):
- **avdeevvadim's #716**
  (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`): the
  charge-condition split this packet leans on throughout -- signed pieces are
  ell^2-capped (his Sec-6 conditions via Cauchy-Schwarz, the (CS-P) step),
  semantic pieces pay ell^1 but only through emission rules.  The reduction
  turns his Sec 7.1 sixth alternative into a single candidate rule.
- **The transverse-charge packet** (#776,
  `transverse_charge_obstruction_sidon_paired.md`): the forcing.  Consumed:
  its Thm 2 fiber-rooted cap (hypotheses re-checked here: canonical q=2
  rooting, (CS-K), single-fiber ell^1) in the reduction's converse; its
  (CS-P) reading of the charge conditions.  Flagged: the Sec-5 window
  erratum above (exact witnesses, V3); nothing downstream is affected.
- **The resonant-folding packet** (#779, `resonant_folding_inverse.md` on
  its own branch -- OPEN PR, NOT yet integrated): the fold, the equal-fiber
  structure (its Thm 3d), and the closed forms that make the flat-cube
  certificate e^{o(N)}-census-able.  Every fact consumed from it is
  RE-VERIFIED self-containedly inside this packet's verifier (brute class /
  fiber / disjointness checks, V4 and V7), so no result here depends on its
  integration; the framing link ("answers its Sec-5 conversion question in
  form") is the only conditional part.
- **#739** (`staircase_concentration_sidon_paired.md`) with
  **DannyExperiments' #749-corrected hypotheses**: the class.
- **Codex team's atlas-totality lane** (in progress, theirs): unchanged
  interface; if it closes, the admission question is the whole input-2
  residual on this class.

---

## 0. Setup

Class, fold, and rooting exactly as in the two prior packets: `P`
2-superincreasing, `c = 2 sum P + 1`, `T = P u (c-P)`, `Phi = sum mod c`,
`M = C(2B,B)`, `w_s = C(B-s,(B-s)/2)` (the level-`s` fiber size),
`f_max = w_0 = C(B,B/2)`, `L = (3^B+1)/2`; parity classes `v` with unpaired
set `U`, `s = |U|`; scans instantiate bases 3 and 5.  Canonical q=2 rooting
of a failing band `A`: `omega = h_+/||h||_2`, `Omega_+ >= ||h||_2
>= e^{eta N} M / L^{1/2}`.  **Maximal band**: `A = hat G \ {0}`,
`h = f - M/c`; unnormalized ledger `Omega~_+ = sum_sigma f h_+` (the
normalization cancels in every ratio below).  Charge-condition split (#716
Sec 6, as read in the transverse-charge packet Sec 0): a SIGNED piece obeys
`c_i <= ||P_{B_i} b_{U_i}||_2 <= ||b_{U_i}||_2` (CS-P); a SEMANTIC piece may
charge up to `sum_{S in U_i} omega(S)` (ell^1) but only via a grammar
emission rule.  A piece is **fold-measurable** if its support is a union of
parity classes.

Facts imported from the resonant-folding packet and re-verified by brute
force here (V4/V7, `B in {4,6}`, both bases): within class `v`, `Phi` takes
exactly `2^s` values, each on exactly `w_s` supports, and distinct classes
have disjoint syndrome sets.

---

## 1. Theorem A: fold pieces are ell^2-charge-trivial, every band

> **Theorem A.**  On the Sidon-paired class, at the canonical q=2 rooting of
> ANY failing band (`||h||_2 >= e^{eta N} M/L^{1/2}`, `eta > 0`), any
> disjoint fold-measurable pieces `{U_i}_{i <= K}` with compatible charges
> (the ell^2 / signed-side condition (CS-P); ell^1-emission pieces are the
> reduction's subject, Sec 5) satisfy
> ```text
> sum_i c_i <= sqrt(K) f_max <= sqrt(K) e^{-(eta + kappa) N + o(N)} Omega_+,
> kappa = ln(2/sqrt 3)/2.
> ```

**Proof.**  A fold piece contains every support of each class it includes,
so its per-syndrome multiplicity is `W_i(sigma) = w_{s(sigma)} <= f_max` on
the syndromes of its classes and `0` elsewhere; distinct classes' syndrome
sets are disjoint, so across disjoint pieces each `sigma` is counted once:
`sum_i ||b_i||_2^2 = sum_i sum_sigma W_i(sigma)^2 omega(sigma)^2
<= f_max^2 sum_sigma omega^2 <= f_max^2` (`||h_+||_2 <= ||h||_2`).
Cauchy-Schwarz over pieces and (CS-P) give `sum c_i <= sqrt(K) f_max`.
Divide by `Omega_+ >= e^{eta N} M/L^{1/2}` and use `f_max L^{1/2}/M
= (sqrt 3/2)^{B - o(B)}` (exact integer form `f_max^2 L < M^2`, V1). `square`

Remarks.  (i) The transverse-charge packet capped quotient-style unions only
through the signed CLAUSE, at rate `e^{-eta N}`; Theorem A caps fold pieces
by MULTIPLICITY, at the stronger rate `e^{-(eta+kappa)N}`, with no clause
and no (FR) -- the same `kappa` as the fiber cap, from the opposite
direction.  (ii) Exact instantiation (V1, `B in {4,6}`, both bases,
maximal band): round-robin `K`-block coarsenings have blocking-invariant
ell^2 mass `sum_i ||b_i||_2^2 = sum_sigma f^2 h_+^2`, and
`K sum_i ||b_i||_2^2 < Omega~_+^2` holds exactly when `K < PN` (Sec 3) --
charge preservation and compatibility are jointly unsatisfiable in exactly
the theorem's regime.

---

## 2. Theorem B: the exact charge ledger, and where the charge lives

> **Theorem B.**  At the maximal band, the level-`s` classes carry exactly
> ```text
> Omega~_+(s) = C(B,s) 2^s w_s (w_s - M/c)_+ ,
> ```
> so:  (a) levels with `w_s <= M/c` carry ZERO charge; ON BASE 3
> (`c = 3^B`, where `M/c ~ (4/3)^B / poly`) the light threshold sits at
> `s/B -> sigma_0 = 1 - log2(4/3) = 0.5849...`, while on base 5
> (`c = (5^B+1)/2`) `M/c -> 0` and EVERY level is heavy -- the threshold is
> a base-3 phenomenon;
> (b) base-robustly, the ledger exponent on the charged range is
> `g(sigma) = H(sigma) + 2 - sigma` (strictly concave, interior maximum at
> `sigma = 1/3`), so for every `eps > 0` the levels `|s/B - 1/3| >= eps`
> carry at most `e^{-c(eps) N + o(N)}` of `Omega~_+` with `c(eps) = (g(1/3)
> - max_{|sigma - 1/3| >= eps} g(sigma)) ln 2 / 2 > 0`.

**Proof.**  The formula is Thm 3d of the resonant-folding packet (equal
fibers `w_s`, `C(B,s) 2^s` syndromes per level) applied to `h = f - M/c`.
(a) `w_s <= M/c` kills `(w_s - M/c)_+`; the threshold: `log2 w_s = (B-s)
- O(log B)` meets `log2(M/c) = B log2(4/3) - O(log B)` at `B - s =
B log2(4/3) + O(log B)`.  (b) entropy expansion of `C(B,s) 2^s w_s^2` (the
`(1 - (M/c)/w_s)` factor is `1 - e^{-Theta(N)}` strictly inside `sigma_0`);
strict concavity of `g` with `g'(1/3) = 0` as in the resonant-folding
packet's Thm 3d. `square`

Pins (V2, exact rationals): `B = 6` shares by level: `15.42% / 70.11% /
14.47% / 0` at `s = 0/2/4/6`; argmax `|s*/B - 1/3| <= 1/12 + 2/B` for all
even `B <= 96`; away-mass (`|s/B - 1/3| >= 1/6`) strictly decreasing along
`B = 8, 16, 32, 64` and below `2^{-6}` at `B = 64`; light-threshold location
within `0.05` of `sigma_0` at `B in {32, 64, 96}` with decreasing deviation
(the `O(log B / B)` correction is visible at these sizes -- the limit is the
theorem's, the finite locations are the pins').

**AUDIT (erratum in the transverse-charge packet; the sentence appears both
in its Status/PROVED block and in its Sec 5).**  The
sentence "Every fiber of the class lies in the half-open window
`[2M/L, M/sqrt L)`" overstates the lower end: `w_s < 2M/L` exactly on
`s in {4, 6}` at `B = 6` (fibers `2, 1` against `2M/L = 5.06...`) and
`s in {4, 6, 8}` at `B = 8` (V3, exact).  The UPPER end is universal
(`w_s^2 L < M^2`, all levels, even `B <= 64`, V3), and the two facts that
packet's theorems consume -- existence of heavy fibers (`f_max L >= 2M`) and
no fiber at carrying scale (upper end) -- are both intact (re-verified).
Corrected reading: "the heavy levels' fibers lie in the window; deep-unpaired
levels are light" -- the same phenomenon as Theorem B(a)'s light threshold,
with a different constant (`2M/L` here vs `M/c` there; on base 3 both cuts
sit at `s/B -> sigma_0 + O(log B / B)`, and the finite sets differ: `{4,6}`
vs `{6}` at `B = 6`).

---

## 3. Theorem C: cube flatness and the budget wall (maximal band)

> **Theorem C.**  At the maximal band:  (a) `h` is EXACTLY constant on each
> class's sign-cube, so a class's available ell^1 charge exceeds any single
> compatible piece's cap by exactly `sqrt(2^s)`:
> `(class ell^1)^2 = 2^s * (class ell^2)^2`.  (b) Any disjoint pieces with
> ell^2-compatible charges (no other structural assumption) satisfy
> `sum c_i <= sqrt(K * sum_sigma f^2 h_+^2)`, so paying `Omega~_+` needs
> ```text
> K >= PN := Omega~_+^2 / sum_sigma f^2 h_+^2 = 2^{B - o(B)} :
> ```
> the exponent identity `2 g(1/3) - max_sigma (H(sigma) + 4 - 3 sigma) = 1`
> holds in closed form (the max sits at `sigma = 1/9`, and
> `H(1/9) = 2 log2 3 - 8/3` exactly).

**Proof.**  (a) equal fibers (re-verified brute, V4).  (b) `b_i(sigma) =
W_i(sigma) omega(sigma)` with `sum_i W_i(sigma) <= f(sigma)`, so
`sum_i ||b_i||_2^2 <= sum_sigma f^2 omega^2`; Cauchy-Schwarz.  The exponent
of `sum f^2 h_+^2` is `max_sigma B (H(sigma) + sigma + 4(1 - sigma))
+ O(log B)` with maximizer `log2((1-sigma)/sigma) = 3`, i.e.
`sigma = 1/9`; `H(1/9) = (1/9) log2 9 + (8/9) log2(9/8) = 2 log2 3 - 8/3`,
so `max = H(1/9) + 4 - 1/3 = 2 log2 3 + 1`, while `2 g(1/3) = 2 (H(1/3) +
5/3) = 2 + 2 log2 3`.  Difference: exactly `1`, i.e. `PN = 2^{B - o(B)}`.
`square`

Pins (V4): `PN = 31.2 / 138.4` at `B = 6 / 8`, at least doubling at
each step through `B = 32`; `K = 2^{B/2}` pieces are exactly
cross-multiply-unsatisfiable at `B in {6, 8, 16, 32}`.  Note `PN` counts
what ell^2 caps can aggregate: the fiber-indexed partition (`K = L =
e^{Theta(N)}` point masses) pays -- consistently, since `L > PN` -- but no
`e^{o(N)}` budget does.  The wall is the budget, not the fold: the FULL fold
partition's ell^1 recovers `Omega~_+` exactly (V6).

---

## 4. Theorem D: the bridge -- the certificate is flatness

> **Theorem D.**  For any class `v` (unpaired set `U`, `|U| = s`) and any
> band, the restriction of `chi_xi` to the class's syndrome cube
> `{sum_{i in U} eps_i A_i}` is the product character
> `e^{-i sum_{i in U} eps_i theta_i(xi)}`, and the sign-cube Fourier
> coefficient of `h` on `v` at `D subseteq U` is
> ```text
> hcube_v(D) = (1/c) sum_xi hat f(xi) prod_{i in D} (-i sin theta_i(xi))
>              prod_{i in U \ D} (cos theta_i(xi))     (minus M/c at D = 0).
> ```
> At the maximal band `hcube_v(D) = 0` for every `D != 0`.

**Proof.**  `chi_xi(sum eps_i A_i) = prod e^{-i eps_i theta_i(xi)}`; expand
each factor as `cos theta_i - i eps_i sin theta_i` and take the
`eps`-cube transform: pattern `D` picks the `-i sin` factor exactly on `D`.
Summing against `hat f` is Fourier inversion on `Z_c` restricted to the
cube.  Vanishing at the maximal band: `h` is constant on the cube (Thm C(a)).
`square`

Verified (V5): every class, every level `s >= 2`, EVERY pattern `D`
(`B = 6`, both bases): brute cube-transform equals the theta-product formula
(max deviation `~1e-15` of `M`), off-empty coefficients vanish, all under
the exact Parseval guard.  The consequence for the program: the angle data
`{theta_i(xi)}` -- exactly what the resonant-folding certificates carry --
IS the sign-cube spectrum of the rooting weights.  A rule that pays flat
cubes needs precisely the certificate that packet already constructs, and a
general band's cube spectrum is computable from the shell by this formula.

---

## 5. The reduction: the sixth alternative is one admission decision

**FLAT-CUBE EMISSION (the candidate primitive):** a grammar rule that pays
the ell^1 charge `sum_{S in piece} omega(S)` of a piece consisting of full
sign-cubes certified flat (certificate: the level's closed forms
`(C(B,s) 2^s, w_s)` from the resonant-folding packet plus `hcube = 0` off
`D = 0`, Thm D).

> **Theorem (reduction, maximal band).**
> (=>) If the grammar admits flat-cube emission, then the `<= B/2 + 1`
> admissible LEVELS, as level-block pieces, are fold-measurable, disjoint,
> each uniform (all classes of a level carry identical `(2^s, w_s, h)`
> data; V6), and their ell^1 charges sum to `Omega~_+` EXACTLY (V6, exact
> rationals, both bases at `B in {4,6}`).  `O(B)` pieces, `e^{o(N)}` census:
> the failure is PAID.
> (<=) Any decomposition into `e^{o(N)}` pieces paying `(1 - e^{-delta N})
> Omega~_+`: its ell^2/signed pieces carry `e^{-Theta(N)} Omega~_+`
> (Thm A for fold-measurable ones; Thm C(b) for arbitrary ones, since
> `e^{o(N)} < PN`); its fiber-rooted semantic pieces carry
> `e^{-(eta+kappa)N} Omega~_+` (transverse-charge Thm 2, hypotheses
> re-checked in Sec 0); so `(1 - e^{-delta' N}) Omega~_+` is paid ell^1 by
> non-fiber-rooted pieces, concentrated on levels `|s/B - 1/3| < eps`
> (Thm B), where every cube is flat (Thm C(a)/D).  Up to exponentially small
> remainders, the payment is ell^1 charge on certified-flat cube territory --
> exactly what the primitive pays.  (A piece-SHAPE classification -- full
> cubes vs arbitrary flat-supported sets -- is NOT claimed; the reduction
> does not need it.)

So on this class, at the operating band, avdeevvadim's #716 Sec 7.1 sixth
alternative is no longer a shape of theorem to be found: it is the single
yes/no question **"does the certificate grammar admit flat-cube emission?"**
-- with the (=>) construction showing exactly what admission buys, and the
three packets jointly supplying the certificate the rule would consume.

## Nonclaims

- **NOT a proof that the compiler admits the primitive** -- no emission rule
  is added, no payment is claimed.  Admission is the surviving open
  question, and it is a grammar-design decision (with a soundness
  obligation: a rule paying ell^1 on flat cubes must not overpay elsewhere),
  not a computation.
- **The reduction is stated at the maximal band** (the dichotomy's operating
  point; `h` constant per class).  Theorems A and D are band-uniform;
  Theorems B/C(a) and the reduction use maximal-band flatness.  General
  bands' cube spectra are computable (Thm D) but their payment structure is
  not classified here.
- **PN's exponent is proved; finite `PN` values are pins.**  Similarly the
  ledger localization constants: `c(eps)` is explicit, the finite shares are
  pins.
- **The erratum is prose-level**: no transverse-charge theorem is affected;
  both facts it consumes are re-verified here (V3).
- **NOT a reserve payment**: fence (N1) respected.
- Floats appear only in the bridge scans (V5), under the exact Parseval
  guard; everything else is exact `int`/`Fraction` arithmetic.

## Consumers

- **#716**: Sec 7.1's alternative becomes an admission decision with an
  explicit candidate rule, an exact construction showing what it buys, and
  the impossibility of everything short of it.
- **The transverse-charge packet (#776 note)**: its forcing is sharpened to
  a named primitive; its Sec-5 window sentence gets the erratum above (with
  exact witnesses; corrected reading supplied).
- **The resonant-folding packet (#779 note)**: its Sec-5 conversion question
  is answered in FORM -- the conversion target is flat-cube emission, and
  its certificates are exactly the required input (Thm D).
- **#739**: the staircase's levels acquire their exact charge shares and the
  light threshold.
- **Codex team's atlas-totality lane**: unchanged interface.
- `rs_mca_thresholds.tex`: paste-ready as a remark after the PO4 material --
  "on the Sidon-paired class, all decompositions within the certificate
  budget reduce, up to exponentially small remainders, to one candidate
  rule: ell^1 payment of certified-flat sign-cubes at the B/3 levels; the
  open input is whether the grammar admits it" -- visible hypotheses:
  #749-corrected class, maximal band, q=2 rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_fold_charge_localization.py
# -> RESULT: PASS (49/49)
python3 experimental/scripts/verify_fold_charge_localization.py --tamper-selftest
# -> tamper-selftest: caught 5/5 ; then RESULT: PASS (49/49)
python3 experimental/scripts/verify_fold_charge_localization.py --emit-certificate \
  experimental/data/certificates/fold-charge/fold_charge_localization.json
cd experimental/lean/fold_charge_localization && lake build
# -> Build completed successfully
```
