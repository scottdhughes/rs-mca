# The resonant-folding precursor: two inverse theorems and an exact three-level decomposition make the forced sixth alternative concrete on the Sidon-paired class

## Status

```text
Status: PROVED (Thm 1, shell structure) that on the Sidon-paired class every
        rho-resonant frequency is digit-structured: |hat f(j)| >= rho M forces
        m(j, delta) <= ln(2 sqrt(B)/rho) / (2 ln sec(pi delta)) generic angles,
        for every j != 0 and delta in (0, 1/4] -- via the contour bound
        |hat f(j)| <= max_phi prod_i 2|cos phi + cos theta_i(j)|
        <= 4^B cos(pi delta)^{2 m(j,delta)} and M >= 4^B/(2 sqrt B).  The
        resonant shell lives inside the near-{0,1/2}-angle (digit-sparse)
        frequencies; the proof chain is verified on full scans, ALL j, at
        (B, base) in {(6,3), (8,3), (6,5)}.
      + PROVED (Thm 2, parity domination) that EVERY frequency's correlation
        is certified by an explicit pair-parity product character: with
        H(j) = {i : cos theta_i(j) < 0} (an exact integer test) and
        psi_j = prod_{i in H(j)} (-1)^{|S cap pair_i|},
            <chi_j o Phi, psi_j> = [z^B] prod_i (1 + z^2 + 2 z |cos theta_i|)
        is real, nonnegative, and >= |hat f(j)| -- with EQUALITY whenever
        H(j) is empty or all of [B] (z -> -z parity); H(j*) = [B] exactly at
        the half-frequency, so the j* resonance is certified by the constant
        character at zero information cost.  Brute-verified over all
        C(12,6) supports at ALL j, both bases.
      + PROVED (Thm 3, exact three-level decomposition) for the parity fold
        v(S)_i = |S cap pair_i| mod 2:  (a) N_v = 2^s C(B-s,(B-s)/2)
        (s = |supp v| == B mod 2), every class inside [2^B/sqrt(2B), 2^B] --
        the fold marginal is FLAT;  (b) <psi_H> = [z^B](1-z)^{2h}(1+z)^{2(B-h)}
        (h = |H|, a Krawtchouk value): +-M exactly at the two constant-on-
        packet characters h in {0, B}, strictly below M for 0 < h < B;
        (c) parity-Parseval sum_H <psi_H>^2 = 2^B sum_v N_v^2 with
        sum_v N_v^2 = [z^B w^B](4zw + (1+z^2)(1+w^2))^B, and the fold
        participation ratio sum_H <psi_H>^2 / M^2 lies in [2, 3] (>= 2
        PROVED; <= 3 COMPUTED, all even B <= 64, decreasing 2.136 -> 2.008):
        at parity resolution the packet is l^2-FLAT, carried by the two +-M
        characters;  (d) M2 = sum_v N_v^2 2^{-s(v)} EXACTLY -- inside class v
        the map Phi takes exactly 2^s values, each on C(B-s,(B-s)/2)
        supports, and no two classes share a value -- so the ENTIRE
        e^{Theta(N)} band excess (L M2 / M^2 = (9/8)^{B-o(B)}) is created by
        the class -> sign-fiber refinement, with its M2-maximizer at
        s* = B/3 exactly at B in {6,12,24,48,96} (|s* - B/3| <= 2 COMPUTED
        for all even B <= 96; s*/B -> 1/3 PROVED by strict concavity of the
        exponent with interior maximum at sigma = 1/3).
      + EXPERIMENTAL (the candidate object): the resonant-folding precursor
        (pairing pi; rho-shell with H(j) per frequency; the Thm-2 parity
        certificates) is packet-scale -- parity classes at s = Theta(B) union
        2^s = e^{Theta(N)} fibers, violating hypothesis (FR) by construction
        -- and costs O(B) bits per shell frequency.  It is proposed as the
        input type for the forced sixth alternative; whether the certificate
        grammar pays it is the OPEN conversion question, stated in Sec 5 and
        NOT claimed.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- the transverse-charge packet proved the sixth
        (packet-scale) alternative of avdeevvadim's #716 Sec 7.1 is FORCED on
        this class and named its resonant spectrum as the first mandatory
        test instance.  This packet supplies that instance's structure
        theory: what resonance implies (Thms 1-2, the inverse direction),
        and what the packet looks like from the parity fold (Thm 3, the
        exact reduction).  Input-2 residual after this packet: UNCHANGED in
        kind -- prove the sixth alternative (now: pay the precursor of Sec 5)
        or exclude the class via atlas totality (the Codex team's lane) --
        but the first branch now has a concrete typed object with exact
        interfaces.  Fence (N1) (thm:aperiodic-one-ray-saturation) respected:
        nothing here pays or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Every combinatorial claim
below is recomputed exactly (`int`/`Fraction`, plus exact integer angle tests)
by `experimental/scripts/verify_resonant_folding_inverse.py` (stdlib only,
deterministic, `RESULT: PASS (84/84)`, `--tamper-selftest` catches `5/5`,
~6 s); Fourier values use floats guarded by the exact Parseval identity
(machine sum matches the exact `c * M2` to `1e-6` relative on every scan).
Machine-readable certificate:
`experimental/data/certificates/resonant-folding/resonant_folding_inverse.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/resonant_folding/` (`lake build` succeeds).
No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`,
`experimental/asymptotic_rs_mca_frontiers.tex`, base commit `2633895`; read,
none edited):
- **`prop:partial-occupancy-fourier` (PO3/PO4)** and **`rem` PO5**: `hat f` is
  the PO3 character sum on the PO5 realized-image group; Theorems 1-2 are
  inverse statements about exactly the characters PO4 cannot flatten on this
  class.
- **`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1); no rung here
  converts resonance or emission into reserve.

Integrated in-tree packets (consumed and credited, not reproved):
- **avdeevvadim's #716**
  (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`): the
  target frame -- his Sec 5.6 Bohr-wall warning (a Theta(1) correlation "does
  not by itself produce" semantic output) is precisely why this packet ships
  inverse THEOREMS rather than more census; his Sec 7.1 sixth alternative is
  the object being made concrete.  Nothing here weakens either.
- **The transverse-charge packet** (#776,
  `experimental/notes/thresholds/transverse_charge_obstruction_sidon_paired.md`):
  the forcing input -- its Prop 1 + Thms 2-4 killed the five-precursor and
  direct branches, upgrading Sec 7.1's "or" to "must", and its Sec 6 exhibited
  the resonant spectrum this packet now structures.  Its per-pair product
  formula for `hat f` is the ONE identity consumed here; per the
  audit-before-consume rule it is re-proved by brute force inside this
  packet's verifier (V5, all j, both bases at B = 6), and its M2 closed form,
  census pins {42, 58}, and j* values are cross-checked exactly (V7).
- **#739** (`staircase_concentration_sidon_paired.md`) with
  **DannyExperiments' #749-corrected hypotheses**: the class itself
  (2-superincreasing P, hence B[+-2]-dissociated; center bound c > 2 sum P);
  the staircase (fiber `C(B-s,(B-s)/2)`, `C(B,s) 2^s` syndromes per level) is
  Theorem 1 there and reappears here refined into the class/fiber two-level
  structure of Thm 3d (re-verified by brute force, V1/V4).
- **#735** (`heavy_fiber_planted_emission.md`): the five-precursor grammar --
  cited as the NEGATIVE specification: every precursor there roots in
  e^{o(N)} fibers, and the parity classes here are engineered to be exactly
  what that grammar cannot see (Sec 5).
- **Codex team's atlas-totality lane** (in progress, theirs): the other
  remaining input-2 escape.  If it closes, the sixth alternative -- and hence
  the conversion question of Sec 5 -- becomes the WHOLE input-2 residual on
  this class.  Interface only; nothing from that lane is assumed.

---

## 0. Setup

Sidon-paired class in the #749-corrected form: `P = {A_1, ..., A_B}`
2-superincreasing (`A_i > 2 sum_{j<i} A_j`), `c = 2 sum P + 1`,
`T = P u (c - P)`, `N = 2B`, `a = B`, `Phi(S) = sum_{t in S} t mod c`,
`G = Z_c`; scans use `A_i = base^{i-1}`, base 3 (`c = 3^B`) and base 5.
`M = C(2B,B)`, `f(sigma) = |Phi^{-1}(sigma)|`, `f_max = C(B,B/2)`,
`L = (3^B+1)/2`, `M2 = sum_sigma f(sigma)^2`.  Pairs `pair_i = {A_i, c-A_i}`;
angles `theta_i(j) = 2 pi j A_i / c`.  The per-pair factorization (PROVED in
the transverse-charge packet Sec 6; re-proved by brute force here, V5)

```text
hat f(j) = sum_S e_c(-j Phi(S)) = [z^B] prod_{i=1}^B (1 + z^2 + 2 z cos theta_i(j))
```

is the object all three theorems act on.  Exact integer angle tests used
throughout (c odd, so no boundary cases):

```text
cos theta_i(j) < 0            <=>  4 r in (c, 3c),          r = j A_i mod c;
||j A_i / c|| in [d, 1/2 - d] <=>  min(r, c-r) >= d c  AND  |2r - c| >= 2 d c.
```

The second line defines a **generic** angle (distance >= d from BOTH 0 and
1/2 mod 1); `m(j, d)` counts generic scales.  `H(j) = {i : cos theta_i(j) < 0}`
is the **antipodal set**.

**Lemma 0 (central binomial, all n >= 1):** `C(2n, n) >= 4^n / (2 sqrt n)`.
*Proof:* `a_n = 2 sqrt(n) C(2n,n) / 4^n` has `a_1 = 1` and
`(a_{n+1}/a_n)^2 = (2n+1)^2 (n+1) / (4 (n+1)^2 n) = 1 + 1/(4n^2+4n) > 1`,
so `a_n >= 1` for all `n`. `square`  (Used by Thm 1 as `M >= 4^B/(2 sqrt B)`,
cross-multiplied `4 B M^2 >= 16^B`, and by Thm 3a's window; verified as
integers for `B <= 64`, V6.)

**Parity fold.**  `v(S) in {0,1}^B`, `v(S)_i = |S cap pair_i| mod 2`; write
`U = supp(v)` (the unpaired scales), `s = |U|`.  Since `|S| = B`,
`s == B (mod 2)`.  For `H subseteq [B]` the **pair-parity product character**
is `psi_H(S) = prod_{i in H} (-1)^{|S cap pair_i|} = (-1)^{|H cap supp v(S)|}`
-- the pullback of the character lattice of the fold group `(Z_2)^B`.  Note
`psi_emptyset = 1` and `psi_[B] = (-1)^{|S|} = (-1)^B`: the two constant-on-
packet characters.

---

## 1. Theorem 1 (shell structure): resonance forces digit structure

> **Theorem 1.**  For every `j != 0`, every `delta in (0, 1/4]`, and every
> `rho > 0`: if `|hat f(j)| >= rho M` then
> ```text
> m(j, delta) <= ln(2 sqrt(B) / rho) / (2 ln sec(pi delta)).
> ```

**Proof.**  Coefficient extraction on the unit circle gives
`|hat f(j)| <= max_{|z|=1} prod_i |1 + z^2 + 2 z cos theta_i|`; with
`z = e^{i phi}`, each factor is `|e^{-i phi} + e^{i phi} + 2 cos theta_i|
= 2 |cos phi + cos theta_i| <= 2 (1 + |cos theta_i|) <= 4`.  If scale `i` is
generic at `delta`, then `|cos theta_i| <= cos 2 pi delta` (the fractional
part of `j A_i / c` is `delta`-far from both 0 and 1/2, and `|cos 2 pi t|`
on `t in [delta, 1/2 - delta]` peaks at the endpoints), so that factor is
`<= 2 (1 + cos 2 pi delta) = 4 cos^2(pi delta)`.  Hence

```text
rho M <= |hat f(j)| <= 4^B cos(pi delta)^{2 m(j, delta)} .
```

With `M >= 4^B / (2 sqrt B)` (Lemma 0), divide and take logarithms. `square`

Verified (V6): the middle chain `|hat f(j)| <= 4^B cos(pi d)^{2 m(j,d)}`
holds for ALL `j != 0` on full scans at `(B, base) in {(6,3), (8,3), (6,5)}`,
`d in {1/20, 1/10, 3/20}`; the stated bound holds on every shell at
`rho in {1/2, 1/4, 1/10, 1/20}`.  Pinned worst cases at `d = 1/10`: base 3
has `m <= 1 / 1 / 3 / 4` at `rho = 1/2 / 1/4 / 1/10 / 1/20` (both `B`),
against bounds `~ 14-47`; base 5 reaches `m = 6` at `rho = 1/10`.  So the
resonant shell sits far inside the digit-sparse region -- every strongly
resonant frequency has all but O(1) of its `B` angles within `delta` of
`{0, 1/2}`.  The bound is one-directional by design (Sec 4, Nonclaims).

---

## 2. Theorem 2 (parity domination): every correlation has an explicit parity certificate

> **Theorem 2.**  For every `j` (including `j = 0`), with `H = H(j)`:
> ```text
> A(j) := <chi_j o Phi, psi_H> = sum_S e_c(-j Phi(S)) psi_H(S)
>       = [z^B] prod_i (1 + z^2 + 2 z |cos theta_i(j)|)  =: D(j),
> ```
> which is real and nonnegative, and
> ```text
> |hat f(j)| <= D(j),
> ```
> with equality whenever `H(j)` is empty or all of `[B]`.

**Proof.**  Grouping the four choices per pair as in the product formula, the
`psi_H`-twist multiplies the two single-element choices of `pair_i`, `i in H`,
by `-1` and fixes the both/neither choices, so the `i`-th factor becomes
`1 + z^2 - 2 z cos theta_i` for `i in H` and is unchanged otherwise.  By the
definition of `H(j)`, every factor is `1 + z^2 + 2 z |cos theta_i|`: all
coefficients nonnegative, so `A(j) = D(j) >= 0`.  Domination: expanding both
products monomial-by-monomial, each monomial of the `hat f` product is the
corresponding monomial of the `D` product times a sign, so the triangle
inequality gives `|hat f(j)| <= D(j)`.  Equality classes: if `H(j)` is empty,
every `cos theta_i >= 0` and `hat f(j) = D(j)` termwise; if `H(j) = [B]`,
substituting `z -> -z` gives `hat f(j) = (-1)^B D(j)`. `square`

Verified (V5): at `B = 6`, BOTH bases, ALL `j`: the brute-force twisted sum
over all `C(12,6) = 924` supports is real, equals the product form `D(j)`,
and dominates `|hat f(j)|`; the equality classes hold; and the brute
`hat f(j)` matches the consumed product formula (the audit-before-consume
re-proof).  At `B = 8` (base 3, all `j = 0..6560`) the same domination,
nonnegativity, and equality-class statements hold via the product formulas
under the Parseval guard.

**Reading.**  Theorem 2 is the certificate direction of the inverse problem:
given ANY resonant frequency, an explicit parity product character --
`H(j)` decoded by the integer rule `4 (j A_i mod c) in (c, 3c)` -- witnesses
at least that much correlation, through a manifestly nonnegative quantity.
At the half-frequency `j* = (c-1)/2` the antipodal congruence (transverse-
charge packet Sec 6) puts EVERY scale in `H(j*)` -- verified exactly, V5 --
so the certificate is the constant character `psi_[B]` and the certified
value IS `|hat f(j*)| >= 0.70 M` (base 3, `B in {6,8}`; `>= 0.61 M` base 5,
`B = 6`).  Away from the two constant classes the certificate is a genuinely
nonconstant parity functional: the structure a sixth-alternative conversion
gets to consume.

---

## 3. Theorem 3 (exact three-level decomposition): packet -> parity class -> sign fiber

> **Theorem 3.**  Let `N_v = #{S : v(S) = v}`, `s = |supp v|`, and let
> `<psi_H> = sum_S psi_H(S)`, `h = |H|`.  Then:
>
> **(a) Flat marginal.**  `N_v = 2^s C(B-s, (B-s)/2)` if `s == B (mod 2)`,
> else `0`; and every admissible class obeys
> `2^B / sqrt(2B) <= N_v <= 2^B`.
>
> **(b) Fold spectrum.**  `<psi_H> = [z^B] (1-z)^{2h} (1+z)^{2(B-h)}
> = sum_k (-1)^k C(2h,k) C(2B-2h, B-k)` -- a Krawtchouk value depending only
> on `h`; it equals `M` at `h = 0`, `(-1)^B M` at `h = B`, and is STRICTLY
> below `M` in absolute value for every `0 < h < B`.
>
> **(c) Parity-Parseval.**  `sum_H <psi_H>^2 = 2^B sum_v N_v^2`, with the
> exact generating function
> `sum_v N_v^2 = [z^B w^B] (4zw + (1+z^2)(1+w^2))^B`; the participation
> ratio `PR(B) = sum_H <psi_H>^2 / M^2` satisfies `PR >= 2` (PROVED: the two
> constant characters alone contribute `2 M^2`), and `PR <= 3` for all even
> `B <= 64` (COMPUTED; pinned `2.136, 2.092, 2.037, 2.017, 2.008` at
> `B = 6, 8, 16, 32, 64`, decreasing).
>
> **(d) Exact excess localization.**  Inside class `v` the map `Phi` takes
> exactly `2^s` distinct values mod `c` -- one per sign pattern
> `sum_{i in U} +- A_i` -- each on exactly `C(B-s, (B-s)/2)` supports, and no
> two classes share a value; consequently
> ```text
> M2 = sum_v N_v^2 2^{-s(v)} = sum_{s == B (2)} C(B,s) 2^s C(B-s,(B-s)/2)^2 ,
> ```
> the integrated closed form.  The summand is strictly unimodal in `s` with
> maximizer `s*(B)` satisfying `|s* - B/3| <= 2` for all even `B <= 96`
> (equality `s* = B/3` at `B in {6, 12, 24, 48, 96}`), and `s*/B -> 1/3`.

**Proof.**  (a) Scales in `U` contribute one element each (2 ways); scales
off `U` contribute both elements or neither, and `|S| = B` forces exactly
`(B-s)/2` "both" choices among `B - s` scales.  The window: for
`n = (B-s)/2 >= 1`, Lemma 0 gives
`N_v >= 2^s 4^n / (2 sqrt n) = 2^B / (2 sqrt n) >= 2^B / sqrt(2B)`; `s = B`
gives `2^B` exactly, which is also the maximum.
(b) `sum_S z^{|S|} psi_H(S) = prod_{i in H} (1 - 2z + z^2)
prod_{i notin H} (1 + 2z + z^2)`; extract `[z^B]` and expand the convolution
for the Krawtchouk form.  Endpoints: `[z^B](1+z)^{2B} = M` and
`[z^B](1-z)^{2B} = (-1)^B M`.  Interior strictness: the alternating sum has
at least three consecutive nonzero terms for `0 < h < B` (the index window
`[max(0, 2h-B), min(2h, B)]` contains at least three integers), so opposite-
sign terms are present and `|<psi_H>| < sum_k C(2h,k) C(2B-2h,B-k) = M`
(Vandermonde).
(c) `<psi_H> = sum_v N_v (-1)^{|H cap supp v|}` is the `(Z_2)^B` Fourier
transform of `v -> N_v`; Parseval on the fold group.  The generating
function: expand `(4zw + (1+z^2)(1+w^2))^B` by the multinomial in the `s`
positions carrying `4zw` and read off `[z^{B-s} w^{B-s}]` of the rest as
`C(B-s,(B-s)/2)^2`.  `PR >= 2` from the `h in {0, B}` terms.
(d) Distinctness: two sign patterns (same or different classes) differing at
all give `sum_i gamma_i A_i` with `gamma in {-2,...,2}^B` not all zero, which
is nonzero by 2-superincreasing (B[+-2]-dissociation) and of absolute value
`<= 2 sum P < c`, hence nonzero mod `c`.  Both-pairs contribute
`A_i + (c - A_i) == 0 (mod c)`, so `Phi` on class `v` is exactly the signed
sum over `U`.  Summing `(fiber size)^2`: class `v` contributes
`2^s C(B-s,(B-s)/2)^2 = N_v^2 2^{-s}`.  Maximizer location: write
`sigma = s/B`; the exponent of `C(B,s) 2^s C(B-s,(B-s)/2)^2` is
`B g(sigma) + O(log B)` with `g(sigma) = H(sigma) + 2 - sigma` (binary
entropy `H`): `g` is strictly concave with `g'(sigma) =
log2((1-sigma)/sigma) - 1` vanishing exactly at the interior point
`sigma = 1/3`, so the integer maximizer satisfies `s*/B -> 1/3` (the
`O(log B)` correction moves an argmax of a strictly concave exponent by
`O(1)`); unimodality and the finite-`B` location are verified exactly
(V4). `square`

Verified (V1-V4): (a) and the fiber structure of (d) by brute force over all
supports at `B in {4, 6}`, BOTH bases (every one of the `2^B` classes, the
`2^s x C(B-s,(B-s)/2)` fiber grid, cross-class distinctness, brute `M2`);
(b) by brute force over all `2^B` subsets `H` at `B in {4, 6}` both bases,
closed form == Krawtchouk for all `h <= B <= 64`; (c) exactly for all
`B <= 64` (its GF to `B <= 32`); (d)'s closed form cross-checked against the
INDEPENDENT generating function `[z^B w^B](2zw + (1+z^2)(1+w^2))^B` to
`B <= 32` and its reconstruction identity as definitional consistency to
`B <= 64`; `sum_v N_v = M` to `B <= 64`.

**Reading.**  The packet seen through the parity fold is as flat as it could
be: every class the same size up to `sqrt(2B)` (a), the fold spectrum carried
by the two constant characters with everything else strictly and (by the PR
pins) collectively negligible (b, c).  The `e^{Theta(N)}` band excess
`L M2 / M^2 = (9/8)^{B - o(B)}` -- the whole reason this class defeats
decompositions -- is created at the NEXT level down, exactly and only by the
splitting of each flat class into its `2^s` equal sign-fibers (d).  And that
splitting is invisible to any `e^{o(N)}`-piece decomposition: a class at
`s = Theta(B)` unions `2^s = e^{Theta(N)}` fibers.  This is the transverse-
charge obstruction seen structurally: the failure charge lives in a
degeneracy (equal sign-fibers) that fiber-rooted pieces can only see one
`e^{-Theta(N)}`-fraction at a time.

---

## 4. What the theorems say jointly: the inverse direction

The transverse-charge packet left the resonant spectrum as a census
(EXPERIMENTAL: which `j` resonate, how strongly).  Theorems 1-2 upgrade the
census to inverse statements with explicit constants, and Theorem 3 gives the
exact object they certify:

- **Resonance => digit structure** (Thm 1): a `Theta(1)`-of-`M` correlation
  pins all but `O(log(1/rho))` angles to `{0, 1/2}` within `delta`.
- **Resonance => parity witness** (Thm 2): the correlation is certified by
  `psi_{H(j)}`, computable from `j` by an integer rule, through a nonnegative
  product that collapses to `|hat f(j)|` itself on the two constant classes.
- **The certified structure is exactly two-level** (Thm 3): flat classes,
  equal sign-fibers, all constants closed-form.

Census facts (EXPERIMENTAL, cross-pinned to the integrated packet, V5):
shell sizes `#{j != 0 : |hat f(j)| >= M/10} = 42 (B=6), 58 (B=8)` on base 3;
`|hat f(j*)| / M = 0.7006 (B=6), 0.7070 (B=8)` base 3, `0.6122` base 5
`B = 6`.

## 5. EXPERIMENTAL: the resonant-folding precursor (the candidate object)

**Definition.**  The *resonant-folding precursor* of the packet at level
`rho` is the triple

```text
RF_rho = ( pi,  Shell_rho = {j != 0 : |hat f(j)| >= rho M},  j -> (H(j), D(j)) ),
```

the pairing `pi : T -> [B]`, the shell, and the Thm-2 parity certificate of
each shell frequency.

**Properties** (all from Secs 1-3): it is defined by the global involution
`A_i <-> c - A_i` and the fold -- no fiber choice, no syndrome rooting;
parity classes at `s = Theta(B)` union `e^{Theta(N)}` fibers, so the object
violates hypothesis (FR) of the transverse-charge packet BY CONSTRUCTION --
it lives at exactly the scale that packet proved necessary.  Its census cost
is `B` bits (`H(j)`) plus one certified value per shell frequency, and the
observed shell is `O(B)` frequencies at `rho = 1/10`; total `e^{o(N)}`.  By
Thm 3 it certifies the exact reduction: modulo the flat parity level, the
Sidon-paired failure IS the equal-sign-splitting degeneracy, localized at
`s ~ B/3`.

**What it is NOT** (scoping, per the five-precursor boundary): the parity
partition itself has `2^{B-1} = e^{Theta(N)}` classes, so it is NOT a
#716-Sec-6 decomposition (those carry `e^{o(N)}` pieces; the transverse-
charge packet's Thm 3 already forbids that route).  The precursor is a
STRUCTURE CERTIFICATE, not a piece list.

**The open conversion question** (the sixth alternative's residual content,
NOT claimed): does the certificate grammar pay a certified
flat-class + equal-sign-splitting structure -- i.e., is there a compiler rung
whose input type is `(RF_rho, the Thm-3 closed forms)` and whose output is a
paid structure at the compiler interface?  This packet supplies the input
type, its inverse theorems, and the exact reduction; the conversion theorem
is what remains of input 2 on this class (besides atlas totality, the Codex
team's lane).

## Nonclaims

- **NOT a proof of the sixth alternative** -- no conversion theorem, no
  payment, no compiler rung is claimed.  The precursor is a typed candidate
  with proved structure, offered as the conversion target.
- **Theorem 1 is one-directional.**  Digit sparsity does NOT imply resonance:
  mixed antipodal patterns are killed by Thm 3b itself (interior Krawtchouk
  values are exponentially below `M`, e.g. `<psi_H> = -20` vs `M = 924` at
  `B = 6, h = 3`).  The shell is CONTAINED in the digit-sparse set, not equal
  to it.
- **Shell growth `O(B)` and the `PR -> 2` limit are observational** (pinned
  at the scanned sizes; monotone on the scan): the PROVED statements are the
  Thm-1 bound per frequency, `2 <= PR` everywhere, and `PR <= 3` as a
  computed fact for even `B <= 64`.  No asymptotic census claim.
- **Equality in Thm 2 is claimed only on the two constant classes**; strict
  inequality elsewhere is observed, not proved.
- **NOT a reserve payment**: fence (N1) respected; nothing here converts
  resonance, folding, or emission into lower reserve.
- **No new hypotheses on the class**: everything runs under the
  #749-corrected hypotheses; scans instantiate bases 3 and 5.
- Floats appear only in the Fourier scans (V5/V6), always under the exact
  Parseval guard; every angle-set and combinatorial statement is exact
  integer arithmetic.

## Consumers

- **avdeevvadim's #716**: Sec 7.1's sixth alternative acquires a concrete
  input type; his Sec 5.6 Bohr wall is respected -- the packet converts the
  correlation into STRUCTURE (Thms 1-3) and leaves the semantic conversion
  explicitly open.
- **The transverse-charge packet (#776 note)**: its Sec 6 EXPERIMENTAL
  resonant spectrum is upgraded -- product formula re-proved (V5), census
  cross-pinned (V7), and the spectrum now carries inverse theorems; its
  "first mandatory test instance" for any conversion theorem is hereby
  typed.  Its Thm-3 forcing is the reason Sec 5 poses the conversion at
  packet scale.
- **#739 / #749**: the staircase becomes the fiber level of an exact
  three-level tower whose middle (parity) level is new; the `s ~ B/3`
  localization refines where in the staircase the excess concentrates.
- **Codex team's atlas-totality lane**: unchanged interface -- if that lane
  closes, the conversion question of Sec 5 is the whole input-2 residual on
  this class.
- `rs_mca_thresholds.tex`: paste-ready as a remark after the
  `prop:partial-occupancy-fourier` block -- "on the Sidon-paired class the
  PO4-resistant characters are classified: every rho-resonant character is
  digit-structured (explicit bound) and parity-certified (explicit
  nonnegative dominator), and the band excess is exactly the sign-splitting
  of a flat parity fold; the surviving open input is the conversion of that
  certificate into a paid structure."  Visible hypotheses: #749-corrected
  class, base instantiations for scans.

## Reproducibility

```bash
python3 experimental/scripts/verify_resonant_folding_inverse.py
# -> RESULT: PASS (84/84)
python3 experimental/scripts/verify_resonant_folding_inverse.py --tamper-selftest
# -> tamper-selftest: caught 5/5 ; then RESULT: PASS (84/84)
python3 experimental/scripts/verify_resonant_folding_inverse.py --emit-certificate \
  experimental/data/certificates/resonant-folding/resonant_folding_inverse.json
cd experimental/lean/resonant_folding && lake build
# -> Build completed successfully
```
