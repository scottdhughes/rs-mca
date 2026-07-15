# Band-uniform signed death and the narrow-band cube certificate: the flat-cube reduction extends to every failing band

## Status

```text
Status: PROVED (T1, every failing band, multiplicity-free) that at the
        canonical q=2 rooting of ANY failing band A (||h_A||_2 >=
        e^{eta N} M / L^{1/2}, eta > 0), ANY disjoint pieces {U_i}_{i<=K}
        with ell^2-compatible charges (CS-P) obey
            sum_i ||b_i||_2^2 <= sum_sigma f^2 omega^2 <= f_max^2 ,
            sum_i c_i <= sqrt(K) f_max ,
        so paying Omega_+ requires K >= ||h_A||_2^2 / f_max^2
        >= e^{2 eta N} M^2 / (L f_max^2) = e^{2(eta+kappa)N - o(N)},
        kappa = ln(2/sqrt 3)/2 per N-unit.  The proof uses ONLY piece
        disjointness (sum_i W_i(sigma) <= f(sigma), so
        sum_i W_i^2 <= f^2 pointwise) and the exact integer rate
        f_max^2 L < M^2.  This strictly improves the transverse-charge
        packet's Prop 1 -- same kappa rate with the W = e^{o(N)}
        multiplicity hypothesis REMOVED (their cap sqrt(K W M) becomes
        sqrt(K) f_max ~ sqrt(K M) unconditionally) -- and makes the
        fold-charge packet's Thm A and participation wall band-uniform:
        the ell^2/signed side of the dichotomy is DEAD on every band, for
        every piece shape, within any e^{o(N)} budget.
      + PROVED (T2, narrow-band cube certificate, class-uniform) for any
        symmetric band A not containing 0 and EVERY parity class v
        (unpaired set U, s = |U|): the sign-cube spectrum of h_A on v is
            hcube_v(D) = (1/c) sum_{xi in A} hat f(xi)
                         prod_{i in D}(-i sin theta_i(xi))
                         prod_{i in U \ D}(cos theta_i(xi)) ,
        so ONE certificate -- the list {(xi, hat f(xi))}_{xi in A}, size
        O(|A| B), i.e. e^{o(N)} for narrow bands -- determines h_A on EVERY
        cube simultaneously (the class enters only through which theta_i
        are read).  Float-verified to 2.7e-15 across a six-family band
        battery x all classes s >= 2 x ALL patterns D, both bases, under
        the exact Parseval guard.
      + PROVED (T3, sound payment floor) for every class and pattern:
            2^s |hcube_v(D)| <= sum_eps |h_A(sigma_eps)| ,
        so an emission rule paying 2^s |hcube_v(D*)| for a
        certificate-NAMED pattern D* never exceeds the cube's ell^1 --
        band-uniformly.  At the maximal band with D* = empty this floor is
        EXACT (equals the full cube ell^1 on every class: flatness), and
        the class totals recompute the fold-charge scaled ledger to the
        integer (cross-pinned).
      + The assembly: for EVERY failing band, e^{o(N)}-piece payments are
        (1 - e^{-delta N}) carried by ell^1-emission pieces (T1 kills the
        signed side band-uniformly; the transverse-charge packet's Thm 2
        kills fiber-rooted semantic pieces band-uniformly), and the
        emission input type is the cube spectrum: EXPLICIT for narrow
        bands (T2), CLOSED-FORM for the maximal band (fold-charge packet).
        Certificate COMPRESSION for middle-width bands (|A| = e^{Theta(N)}
        short of maximal) is the named residual: T2's certificate is their
        spectrum too, but its list form is no longer e^{o(N)}.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- fourth packet of the arc (forcing -> typing ->
        reduction -> scope): the flat-cube admission question now covers
        EVERY band at q=2 on this class, its certificate type is pinned
        band-uniformly, and its sound payment floor is explicit.  Input-2
        residual: the admission decision + middle-band certificate
        compression + atlas totality (the Codex team's lane) + the
        unchanged large-q Sidon residual.  Fence (N1)
        (thm:aperiodic-one-ray-saturation) respected: nothing here pays or
        claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Integer claims are exact
(`int` arithmetic) and band scans use floats under the exact Parseval guard,
all recomputed by
`experimental/scripts/verify_band_uniform_reduction.py` (stdlib only,
deterministic, `RESULT: PASS (26/26)`, `--tamper-selftest` catches `6/6`,
~0.6 s).  Machine-readable certificate:
`experimental/data/certificates/band-uniform/band_uniform_cube_reduction.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/band_uniform_reduction/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `2633895`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)** -- T1 is
the statement that no PO4-side aggregation of compatible pieces pays any
failing band within the certificate budget; **`thm:aperiodic-one-ray-
saturation` (SAT1)**: fence (N1).

Integrated in-tree packets (consumed and credited, not reproved):
- **avdeevvadim's #716**
  (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`): the
  charge-condition split (signed = ell^2-capped via (CS-P), semantic = ell^1
  via emission rules); T1 is a statement about his Sec-6 conditions'
  ell^2 side, closing it band-uniformly.
- **The transverse-charge packet** (#776,
  `transverse_charge_obstruction_sidon_paired.md`): its Prop 1 is the
  direct ancestor of T1 -- the relation is stated precisely in T1's remark
  (multiplicity hypothesis removed, same kappa); its Thm 2 (fiber-rooted
  cap, band-uniform) is consumed in the assembly with hypotheses
  re-checked (canonical q=2 rooting, (CS-K), single-fiber ell^1).
- **The fold-charge packet** (#791, `fold_charge_localization.md` on its
  own branch -- OPEN PR, NOT yet integrated): its Thm A (fold pieces) and
  Thm C(b) (participation wall) become special cases of T1; its maximal-
  band flat specialization is T3's exact case; its scaled-ledger integers
  (1771440 / 475308288) are recomputed independently here (V1/V4).  Every
  consumed fact is re-verified in-packet, so nothing depends on its
  integration.
- **The resonant-folding packet** (#779, `resonant_folding_inverse.md` on
  its own branch -- OPEN PR, NOT yet integrated): T2 generalizes its
  bridge identity from the maximal band to arbitrary bands; its shell
  census (42 at rho = 1/10, base 3) is re-pinned here (V5).  Same
  self-containment: the class/fiber/disjointness structure is re-verified
  by brute force (V5).
- **#739** (`staircase_concentration_sidon_paired.md`) with
  **DannyExperiments' #749-corrected hypotheses**: the class.
- **Codex team's atlas-totality lane** (in progress, theirs): unchanged
  interface.

---

## 0. Setup

Class, fold, rooting, and notation exactly as in the three prior packets:
`P` 2-superincreasing, `c = 2 sum P + 1`, `T = P u (c-P)`, `N = 2B`,
`Phi = sum mod c`, `M = C(2B,B)`, `w_s = C(B-s,(B-s)/2)`,
`f_max = C(B,B/2)`, `L = (3^B+1)/2`; parity classes `v` with unpaired set
`U`, `s = |U|`, syndrome cubes `sigma_eps = sum_{i in U} eps_i A_i`;
`theta_i(xi) = 2 pi xi A_i / c`; scans instantiate bases 3 and 5.
Canonical q=2 rooting of a band `A`: `h = h_A = P_A f`,
`omega = h_+ / ||h||_2`, `Omega_+ = sum_sigma f h_+ / ||h||_2 >= ||h||_2`
(the FULL `L^2(Z_c)` norm throughout: `<f, h> = ||h||_2^2` is the
orthogonal-projection identity on `Z_c`, and `f >= 0` gives
`sum f h_+ >= <f, h>`; the verifier computes `||h||_2` spectrally,
`||h||_2^2 = sum_{xi in A} hat f(xi)^2 / c`, and checks the projection
identity itself per band).  Failure: `||h||_2 >= e^{eta N} M / L^{1/2}`.
A piece `U_i` has `b_i(sigma) = W_i(sigma) omega(sigma)`,
`W_i(sigma) = #{S in U_i : Phi(S) = sigma}`; ell^2 compatibility (CS-P):
`c_i <= ||P_{B_i} b_i||_2 <= ||b_i||_2`.

Band battery for the scans (each symmetric, `0` excluded): the top-2 shell
pair, the top-10 shell, the full `rho = 1/10` shell, two dyadic blocks
(`1..32`, `33..96` symmetrized), and the maximal band `hat G \ {0}`.

---

## 1. Theorem T1: the signed side dies on every band

> **Theorem T1.**  On the Sidon-paired class, at the canonical q=2 rooting
> of ANY failing band, any DISJOINT pieces `{U_i}_{i <= K}` with
> ell^2-compatible charges satisfy
> ```text
> sum_i c_i <= sqrt(K) f_max ,
> ```
> so a payment `sum_i c_i >= (1 - o(1)) Omega_+` forces
> ```text
> K >= (1 - o(1)) ||h_A||_2^2 / f_max^2
>   >= e^{2 eta N} M^2 / (L f_max^2) (1 - o(1)) = e^{2(eta + kappa) N - o(N)}.
> ```

**Proof.**  Disjointness gives `sum_i W_i(sigma) <= f(sigma)` per syndrome,
and `W_i >= 0` gives `sum_i W_i(sigma)^2 <= (sum_i W_i(sigma))^2
<= f(sigma)^2`.  Hence
`sum_i ||b_i||_2^2 = sum_sigma omega^2 sum_i W_i^2
<= sum_sigma f^2 omega^2 <= f_max^2 sum_sigma omega^2 <= f_max^2`
(`||h_+||_2 <= ||h||_2`).  Cauchy-Schwarz over the pieces and (CS-P) give
the cap; `Omega_+ >= ||h||_2` and `f_max^2 L < M^2` (exact integers, V1)
give the count, with `M / (f_max L^{1/2}) = e^{kappa N - o(N)}`. `square`

Remarks.  (i) **Relation to the transverse-charge Prop 1**: that bound,
`sum c_i <= sqrt(K W M)`, requires every piece's multiplicity `W_i <= W`
and is useful only for `W = e^{o(N)}`; T1's pointwise square trick removes
the hypothesis entirely at the same `kappa` rate (`f_max ~ sqrt(M)` up to
poly).  Transverse pieces, fold pieces (fold-charge Thm A), and arbitrary
mixtures are all the same corollary now.  (ii) The fold-charge
participation wall is the maximal-band sharpening (exact `sum f^2 h_+^2`
in place of `f_max^2`); its `K = 2^{B/2}` cross-multiplied
unsatisfiability is re-verified here as exact integers (V1), and the
band battery pins `K_min` between 25.5 and 171.3 already at `B = 6`
(V2, certificate; full-norm `R_A` pinned per band -- the maximal band is
already failing at `B = 6`, `R_A = 1.0156`).  (iii) Sharpness direction: the fiber-indexed partition
(`K = L` point masses) pays every band -- consistently, `L = e^{Theta(N)}`
exceeds every bound above.

---

## 2. Theorem T2: one explicit certificate per narrow band, all cubes at once

> **Theorem T2.**  Let `A` be symmetric with `0 notin A`.  For every class
> `v` and every `D subseteq U`:
> ```text
> hcube_v(D) = (1/c) sum_{xi in A} hat f(xi)
>              prod_{i in D} (-i sin theta_i(xi))
>              prod_{i in U \ D} (cos theta_i(xi)) .
> ```
> In particular the list `{(xi, hat f(xi))}_{xi in A}` -- computable from
> the per-pair product formula, `O(|A| B)` bits, `e^{o(N)}` for
> `|A| = e^{o(N)}` -- determines `h_A` restricted to EVERY sign-cube of
> the packet simultaneously.

**Proof.**  `h_A` is real (`A` symmetric, `hat f` real), so
`h_A(sigma_eps) = (1/c) sum_{xi in A} hat f(xi) cos(sum_{i in U} eps_i
theta_i(xi))`; expand each cosine by the product formula
`prod_i (cos theta_i - i eps_i sin theta_i)` and take the `eps`-cube
transform: pattern `D` picks the `sin` factor exactly on `D`, and summing
`xi` with `-xi` retains the displayed (real) value.  `0 notin A` removes
the DC shift.  Odd-`|D|` coefficients vanish identically by the
`eps -> -eps` symmetry; the identity's substantive content is even `|D|`.
`square`

Verified (V3): all narrow bands in the battery (`|A| <= 200`), all classes
`s >= 2`, ALL `2^s` patterns each, both bases: brute cube transform equals
the formula to `2.7e-15` of `M` (Parseval-guarded), and the odd-`|D|`
vanishing is checked separately on every scanned band.  The maximal band
is `h = f - M/c` exactly and its all-pattern scan is the fold-charge
packet's V5; here it contributes the flat specialization (Sec 3).

**Reading.**  The certificate is CLASS-UNIFORM: the band list is written
once, and every cube's spectrum falls out by reading off which `theta_i`
the class exposes.  This is the resonant-folding precursor doing exactly
what it was typed for: the shell data IS the sign-cube-splitting structure,
now for arbitrary narrow bands.

---

## 3. Theorem T3: the sound payment floor

> **Theorem T3.**  For every band, class, and pattern:
> `2^s |hcube_v(D)| <= sum_eps |h_A(sigma_eps)|`.  An emission rule that
> pays `2^s |hcube_v(D*)|` against certificate-named patterns `D*` (one
> per class) is therefore sound against the cube ell^1, band-uniformly.
> At the maximal band the `D* = empty` floor is exact -- it EQUALS the
> full cube ell^1 on every class -- and recovers the flat-cube rule and
> its ledger.

**Proof.**  A Fourier coefficient of a function on `{0,1}^s` is at most
its mean absolute value.  Exactness at the maximal band is cube constancy
(fold-charge Thm C(a)). `square`

Verified (V4): the floor itself is the triangle inequality (its proof IS
the one-line argument above -- a numerical instance cannot fail), so the
verifier carries its content through two checks with teeth: the
cube-Parseval identity `sum_D hcube_v(D)^2 = 2^{-s} sum_eps h_A(sigma_eps)^2`
on every scanned (band, class), both bases, and the maximal-band
exactness (`D = empty` floor `==` full cube ell^1, to `1e-6 M`); the
scaled-ledger integers (`1771440` / `475308288` at `B = 6 / 8`) are
re-verified exactly (V1).  Parseval accounting bounds any named-pattern
list's ell^2 mass; a canonical multi-pattern payment SCHEDULE is left as a
design point for the admission decision, not claimed here.

---

## 4. Assembly: the admission question now covers every band

For EVERY failing band at the canonical q=2 rooting: within any
`e^{o(N)}`-piece budget, the ell^2/signed side carries
`e^{-Theta(N)} Omega_+` (T1) and fiber-rooted semantic pieces carry
`e^{-(eta+kappa)N} Omega_+` (transverse-charge Thm 2, hypotheses
re-checked in Sec 0), so `(1 - e^{-delta N}) Omega_+` must be paid ell^1
by non-fiber-rooted emission -- and the required certificate is the cube
spectrum: T2's explicit list for narrow bands, the fold-charge closed
forms for the maximal band.  What remains open, in order of consequence:

1. **The admission decision** (unchanged in kind, widened in scope): does
   the grammar admit cube-spectrum emission with T3's floor as its payment
   rule?  All-band coverage raises what admission buys: it is no longer a
   one-band primitive.
2. **Middle-width bands** (`|A| = e^{Theta(N)}`, not maximal): T2 still
   describes their cubes, but the list certificate is too large; a
   compression (structured band families, e.g. dyadic unions of shell
   orbits) is the concrete open piece.
3. Atlas totality (the Codex team's lane) and the large-q Sidon residual
   (#729 Sec 3.3), both unchanged.

## Nonclaims

- **NOT a proof of admission**; no emission rule is added to the grammar.
  T3 gives the floor such a rule would pay and its soundness against the
  cube ell^1 -- the compiler-level soundness obligation (no double counting
  with other rules) is part of the admission decision itself.
- **No claim for middle-width bands** beyond T1/T3 (which are
  band-uniform) and T2's identity (whose LIST form is only `e^{o(N)}` for
  narrow bands): the compression question is named open, not settled.
- **T1 needs disjointness**; overlapping piece families are outside (CS-P)
  and outside every packet in this arc.
- **q = 2 only**, as throughout the arc (the rooting's band-limited norming
  dual); nothing is claimed for `q > 2` roots.
- **Finite pins are pins**: `K_min` values, the identity deviation, and
  census numbers are `B = 6` scan facts; the exponential statements are
  the theorems'.
- **NOT a reserve payment**: fence (N1) respected.
- Floats appear only in the band scans (V2-V4), under the exact Parseval
  guard; V1/V5 are exact integer arithmetic.

## Consumers

- **#716**: the Sec-6 ell^2 side is closed band-uniformly; the sixth
  alternative's certificate type and payment floor are pinned for every
  band.
- **The transverse-charge packet (#776 note)**: Prop 1 acquires its
  multiplicity-free form (T1) -- the W-hypothesis can be dropped wherever
  it is consumed downstream.
- **The fold-charge packet (#791 note)**: its reduction extends in scope
  from the maximal band to all bands (T1 + assembly); its Thm A becomes a
  corollary and its Thm C(b)'s METHOD becomes band-uniform (the exact
  maximal-band wall remains the sharpening); its flat-cube rule is T3's
  exact case.
- **The resonant-folding packet (#779 note)**: its bridge identity and
  certificates are the band-general emission input (T2); its Sec-5
  conversion question is now scoped band-uniformly.
- **#739**: unchanged; the class carries the whole arc.
- `rs_mca_thresholds.tex`: paste-ready as a remark after the PO4 material
  -- "on the Sidon-paired class, within the certificate budget, the signed
  side of the semantic-or-signed dichotomy pays no failing band
  (multiplicity-free cap sqrt(K) f_max); every payment reduces to
  ell^1-emission against sign-cube spectra, explicitly certified for
  narrow bands; the open input is the admission of cube-spectrum emission"
  -- visible hypotheses: #749-corrected class, q=2 rooting, disjoint
  pieces.

## Reproducibility

```bash
python3 experimental/scripts/verify_band_uniform_reduction.py
# -> RESULT: PASS (26/26)
python3 experimental/scripts/verify_band_uniform_reduction.py --tamper-selftest
# -> tamper-selftest: caught 6/6 ; then RESULT: PASS (26/26)
python3 experimental/scripts/verify_band_uniform_reduction.py --emit-certificate \
  experimental/data/certificates/band-uniform/band_uniform_cube_reduction.json
cd experimental/lean/band_uniform_reduction && lake build
# -> Build completed successfully
```
