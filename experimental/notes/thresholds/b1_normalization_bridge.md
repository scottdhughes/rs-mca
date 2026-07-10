# B1 normalization bridge: the prefix-image scale via the PTE-rigidity-anchored fiber energy (2026-07-09)

Status: `PROVED` (the second-moment identity + T6 base collapse, exact) / `PROVED-anchor` (the base
`D_d = 0` for `1 <= d <= w` is machine-checked: `PowersumRigidity.RigidityCorollaries.pte_rigidity`) /
`MEASURED` (dense-window near-flatness `Gamma2/flat -> 1`, defect `-> 0`) / `OPEN` (the `d>w` energy-tail
`exp(o(N))` bound — a SECOND-moment estimate, strictly easier than the fourth-moment PR crux).
Verifier: `experimental/scripts/b1_prefix_energy_defect.py` (self-checking; second-moment identity gated
exact vs brute census on 5 configs). Target: the B1 OPEN GAP of the `asymptotic_rs_mca.tex` closed-ledger
audit (PR #433/#435) — `thm:fourier-flat-q` pays fibers at the ambient `Q^w` scale, the paper normalizes
by the actual image `L = |im Phi|`; the bridge `|im Phi| = Q^w exp(o(N))` in-window was unprinted.
Complementary to the F_p-span-cell surjection note (span/defect route); this is the second-moment/energy route.

## 1. The bridge reduces to fiber-energy near-flatness (PROVED reduction)

Let `Phi: Omega_m -> E^w` be the depth-`w` prefix (power-sum) map, `R(z) = |Phi^{-1}(z)|`, `Q = |E| = p`
per coordinate, `C = C(N,m)`, `flat = C^2 / Q^w` (the uniform fiber-energy value), `mean = C/Q^w`.
- **Fourier form (Parseval).** `Rhat(c) = sum_{M} prod_{a in M} e_p(f_c(a)) = e_m(v_c)` (`v_a = e_p(f_c(a))`),
  and `Gamma_2 := sum_z R(z)^2 = flat + (1/Q^w) sum_{c != 0} |e_m(v_c)|^2`. So
    **`|im Phi| = Q^w exp(o(N))`  <==  `Gamma_2 <= flat * exp(o(N))`  <==>  `sum_{c!=0} |e_m(v_c)|^2 <= C^2 exp(o(N))`**
  (the second Cauchy-Schwarz step `|im Phi| >= (sum R)^2 / sum R^2 = C^2/Gamma_2`; and `|im Phi| <= Q^w`).
  **This is the SECOND moment of the signed `e_m`.** (The M31 packet #434's crux `PR(Rhat) <= nu*_ref` is
  the FOURTH moment; B1 is its strictly-easier sibling.)
- **Second-moment identity (PROVED, verified exact).**
    `Gamma_2 = sum_{d>=0} C(N-2d, m-d) * D_d`,  `D_d = #{ordered disjoint (A,B), |A|=|B|=d, p_j(A)=p_j(B) for j<=w}`.
- **T6 base (MACHINE-CHECKED).** `pte_rigidity` gives `D_d = 0` for `1 <= d <= w`. Hence
    **`Gamma_2 = C + sum_{d>w} C(N-2d,m-d) D_d`** — the fiber energy has NO low-order (`d <= w`) off-diagonal
  mass; the entire deviation from the diagonal is the `d>w` tail.

## 2. Dense-window behaviour (MEASURED — B1 holds where it is used)

The paper uses B1 in the `o(n)`-window around the crossing, the DENSE regime (`mean >> 1`, deployed
`avg_ceil ~ 2e6`). Exact fiber census (`b1_prefix_energy_defect.py`):

| p | n | m | w | mean | occupancy \|im\|/Q^w | defect | Gamma2/flat |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 41 | 20 | 10 | 1 | 4506 | 1.000 | 0.000 | 1.0000 |
| 41 | 20 | 10 | 2 | 110 | 1.000 | 0.000 | 1.0041 |
| 61 | 20 | 10 | 2 | 50 | 1.000 | 0.000 | 1.0058 |
| 101 | 20 | 10 | 2 | 18 | 1.000 | 0.063 (rounded 0) | 1.0630 |
| 241 | 20 | 10 | 2 | 3.2 | 0.919 | 0.015 | 1.535 |

As `mean -> infinity`, `Gamma_2/flat -> 1`, occupancy `-> 1`, **defect `-> 0`**: the image is near-surjective
and the normalization bridge `|im Phi| = Q^w exp(o(N))` holds. (Consistent with the F_p-span-cell note's
`occupancy = p^{-defect}` with `defect -> 0` in the dense regime — same conclusion, second-moment route.)

## 3. What remains (OPEN, but a second-moment estimate)

The single remaining rigorous step is the `d>w` fiber-energy tail bound
    **`sum_{d>w} C(N-2d, m-d) D_d <= flat * exp(o(N)) = (C^2 / Q^w) exp(o(N))`  in the dense window.**
Equivalently `sum_{c!=0}|e_m(v_c)|^2 <= C^2 exp(o(N))`. This is a SECOND-moment / near-equidistribution
statement (the `s=1` case of the moment ladder) — strictly weaker than the fourth-moment PR crux (#434) and
the sup/max-fiber crux, and the natural target for a Weil/character-sum second-moment or an entropy count on
the `D_d` (PTE-pair) tail. The base (`d<=w` vanishes) is machine-checked; the tail is the concrete open piece.

## Scope
Reduces B1 to a named second-moment estimate with a machine-checked base and dense-window verification; it does
NOT by itself supply the `exp(o(N))` tail bound (that is the remaining OPEN piece). Not a closure of
`prob:entropy-inverse-q` or any deployed-finite claim. Second-moment/energy route; complementary to the
span-cell/defect route of `cap25_v13_entropy_inverse_fp_span_surjection.md`.

## 4. The `d>w` tail: reduced to a per-`d` second-moment bound (2026-07-09 update)

The tail bound reduces to a clean per-`d` estimate. Using the Vandermonde identity
`sum_d C(N-2d,m-d) C(N,d) C(N-d,d) = C(N,m)^2`:
    **if `D_d <= C(N,d) C(N-d,d) Q^{-w} exp(o(N))` for every `d > w`, then `tail <= flat * exp(o(N))`** (B1).
The per-`d` ratio `r_d := D_d / (C(N,d) C(N-d,d) Q^{-w})` is the object; `r_d = e^{o(N)}` for all `d>w` closes it.

**Anchors and verification (`b1_tail_per_d.py`):**
- **`d <= w`: `D_d = 0`** (machine-checked `pte_rigidity` / T6) — the tail starts at `d = w+1`.
- **`d = w+1` (the smallest, hardest): `D_{w+1} <= 30 C(N,w+1)`** — the b2 result T12 (`E_{w+1} = 2*#{U:
  |U|=2(w+1), Qhat^2-P_U perfect square}`, each degree-`(w+1)` locator has `<= n/(w+1)` full fibers).
- **`r_d = O(1)` UNIFORMLY across `d > w`, `-> 1` in the dense window** (verified: at `mean = 18.1`,
  `r_d in [0.33, 1.09]`; the dominant middle `d` sits at `r_d ~ 1.0`). `Gamma_2/flat = 2.09, 1.53, 1.06`
  for `mean = 1.37, 3.2, 18.1` — converging to 1.

**The remaining rigorous step, in its cleanest form.** By Parseval on `d`-subsets,
`D_d^{all} = (1/Q^w)(C(N,d)^2 + sum_{c!=0}|e_d(v_c)|^2)` and `D_d <= D_d^{all}`, so the per-`d` bound is
    **`sum_{c != 0} |e_d(v_c)|^2 <= C(N,d)^2 exp(o(N))`  for every `d`**
— the `s = 1` (second-moment) rung of the signed-`e_d` moment ladder, uniform in `d`. This is DECOUPLED from
and strictly weaker than the `s = infinity` (max-fiber / sup) crux and the `s = 2` (participation-ratio,
#434) crux: it asks only that the signed `e_d` spectrum has near-flat SECOND moment. It is the natural target
for the moment law (b2 T5, `E_c|pi_r|^{2s} <= (2s-1)!! n^s`) fed through Newton-Girard, or a Lang-Weil count on
the PTE variety with the coset stratum (which is `exp(o(N))`) removed. Base `d<=w` machine-checked; `d=w+1`
anchored by T12; `r_d = O(1)` verified across the window; the general-`d` `s=1` rung is the concrete open piece.
