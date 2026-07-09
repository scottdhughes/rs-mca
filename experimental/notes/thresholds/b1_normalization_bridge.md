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
