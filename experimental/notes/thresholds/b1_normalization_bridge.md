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

## 3b. B1 in one line: the signed-`e_m` second moment (verified identity)

Since `R_hat(c) = sum_{|S|=m} prod_{a in S} e_p(f_c(a)) = e_m(v_c)` (the SIGNED elementary symmetric of round o),
Parseval on the moment map gives the EXACT identity
    **`Gamma_2 / flat = 1 + (1 / C(N,m)^2) * sum_{c != 0} |e_m(v_c)|^2`**   (`flat = C(N,m)^2 / Q^w`),
verified to machine precision (`b1_em_second_moment_identity` check: 3 configs, `match=True`). Hence
    **B1  <=>  `sum_{c != 0} |e_m(v_c)|^2 <= C(N,m)^2 * exp(o(N))`.**
This is a SECOND-moment statement at level `d = m` (full subsets), which is ALWAYS dense
(`C(N,m) >> Q^w` in the deployed regime), so the sparse-diagonal pathology that defeats a per-`d` `|e_d|^2`
bound at small `d` does not arise here. It is the `s = 1` rung of the signed-`e_m` ladder and is decoupled
from the `s = infinity` (max-fiber / sup) crux and the `s = 2` (participation-ratio, #434) crux. The per-`d`
disjoint decomposition below (Section 4) is the structural refinement of the SAME `Gamma_2`, indexed by
symmetric-difference size, exposing the T6 (`d<=w`) and T12 (`d=w+1`) rigidity content.

## 3c. Analytic path: the signed-`e_m` second moment is a Newton–Girard polynomial in DILATED character sums

The remaining bound `sum_{c!=0}|e_m(v_c)|^2 <= C(N,m)^2 exp(o(N))` has a concrete character-sum route, not just
a Lang–Weil hand-wave. The power sums of `v_c = e_p(f_c(.))` are dilates of the SAME sum `pi(c) := sum_{a in mu_n} e_p(f_c(a))`:
    **`p_r(v_c) = sum_{a} v_a^r = sum_a e_p(r f_c(a)) = sum_a e_p(f_{rc}(a)) = pi(r c)`**   (verified exact, `b1_dilation_bridge.py`).
By Newton–Girard, `e_m(v_c)` is therefore a FIXED universal polynomial in `pi(c), pi(2c), ..., pi(mc)`
(verified: NG reconstruction from `{pi(rc)}` matches the direct `e_m(v_c)` to machine precision). Hence
    **`sum_{c!=0}|e_m(v_c)|^2` is governed by the JOINT moments of `pi` at dilates `{rc}`,**
and the b2 moment law T5, `E_c |pi(c)|^{2s} <= (2s-1)!! n^s`, is the direct analytic input (via Cauchy–Schwarz
across the NG monomials). This unifies B1 with the b2 dilated-`pi` ladder: the dilates `rc` are exactly the
resonance frequencies of the b2 subgroup-`4`-moment analysis. CAVEAT (honest scope): for deployed `m ~ n/2 ~ 10^6`
the NG polynomial has degree `m`, so turning the joint-moment control into the `exp(o(N))` bound (managing the
`m`-fold NG monomial sum, and the `r ≡ 0 mod p` trivial-dilate terms `pi(0)=n`) is the substantial remaining work.
This is the concrete open problem: a second-moment bound for a degree-`m` symmetric function of dilated Weil sums.

## 3d. ROUTE-CUT: executing T5 -> Newton-Girard -> triangle is insufficient (magnitude control kills the cancellation)

Executed the §3c path in full and it is a DEAD END for deployed B1 (banked per "failures preserved").
Expanding `e_m(v_c) = sum_{lambda|-m} (eps_lambda/z_lambda) prod_r pi(rc)^{m_r}`, bounding each term's `L^2(c)`
norm by Holder (weights `q_r=ell/m_r`) + T5 (`E_c|pi(rc)|^{2ell}=E_c|pi|^{2ell}<=(2ell-1)!! n^ell`, dilation
`c->rc` measure-preserving for `r<p`), then Minkowski over partitions gives `Gamma_2 = E_c|e_m|^2 <= B^2` with
a CLOSED FORM (unsigned Stirling 1st kind, since `sum_{lambda|-m,#parts=ell} 1/z_lambda = |s(m,ell)|/m!`):
    **`B = (1/m!) sum_{ell=1}^{m} |s(m,ell)| sqrt((2ell-1)!! n^ell)`.**
Write the shortfall exponent `g/n := (2 log2 C(n,m) - log2 B^2)/n`; then `Gamma_2 <= flat * 2^{w log2 Q - g}`,
so B1 closes iff `w log2 Q <= g`. VERIFIED (`b1_t5_newton_girard_routecut.py`, self-checking; closed form ==
direct partition enumeration; T5 constant asymptotically tight):

| moment constant `E_c|pi|^{2ell} <= c_ell n^ell` | `g/n` (limit, `m=n/2`) | vs deployed need `w log2 Q / n ~ 0.997` |
|---|---|---|
| `(2ell-1)!!`  (T5, PROVEN)          | `-0.048` | fails — WORSE than trivial `|e_m|<=C(n,m)` |
| `ell!`  (complex-Gaussian, sharper) | `+0.331` | fails by `~0.67 n` |
| `1`  (ideal — INCONSISTENT)         | `-> 2`   | clears it, but is false |

The T5-constant bound is even worse than the trivial `|e_m| <= C(n,m)` (`g/n<0`). The only constant that clears
the deployed requirement is `c_ell=1` (`|pi(rc)|<=sqrt n` for ALL `c`, giving `B=C(sqrt n+m-1, m)=2^{o(N)}`),
but that is inconsistent: at `c=0`, `pi(0)=n` (and at structured / small-value-set `c`, `|pi|` is large), and
the `c=0` term alone forces `Gamma_2 >= flat`. **So no CONSISTENT magnitude-only bound on `{|pi(rc)|}`, combined
via the triangle inequality, closes deployed B1 — it is short by `e^{Theta(N)}`.** The entire shortfall is the
discarded `eps_lambda` sign cancellation among the `p(m)` Newton-Girard terms; T5 (and any magnitude/moment law)
is blind to it. The missing ingredient is JOINT PHASE cancellation among the dilated Weil sums `{pi(rc)}` — the
`sqrt(p)/BGK` barrier that the b2/L1 arc already identifies as the shared deep crux. **This cuts the T5->NG
route; it does NOT weaken the reduction (§3b) or the dilation bridge (§3c), which stand.**

## 4. The `d>w` tail: reduced to a per-`d` second-moment bound (2026-07-09 update)

The tail bound reduces to a clean per-`d` estimate. Using the Vandermonde identity
`sum_d C(N-2d,m-d) C(N,d) C(N-d,d) = C(N,m)^2`:
    **if `D_d <= C(N,d) C(N-d,d) Q^{-w} exp(o(N))` for every `d > w`, then `tail <= flat * exp(o(N))`** (B1).
The per-`d` ratio `r_d := D_d / (C(N,d) C(N-d,d) Q^{-w})` is the object; `r_d = e^{o(N)}` for all `d>w` closes it.

**The object is the DISJOINT count, not the fiber energy.** `D_d` counts *ordered disjoint* PTE pairs
`(A,B)`, `|A|=|B|=d`, `A cap B = empty`, matching `p_1..p_w`. This is NOT the diagonal-inclusive fiber
energy `D_d^{all} = (1/Q^w)(C(N,d)^2 + sum_{c!=0}|e_d(v_c)|^2)`: the two differ by the `A=B` diagonal (and
partial overlaps). The distinction is decisive in the SPARSE regime `Q^w > C(N,d)`, where `D_d^{all}` is
diagonal-DOMINATED (`D_d^{all} ~ C(N,d) >> exp_d`) so a `sum_{c!=0}|e_d|^2 <= C(N,d)^2` bound is simply
FALSE there. The disjoint `D_d` carries no diagonal and stays generic in both regimes.

**Anchors and verification (`b1_tail_per_d.py`; interior-crossover run `p=101,n=20,m=10,w=2`, `Q^w=10201`):**
- **`d <= w`: `D_d = 0`** (machine-checked `pte_rigidity` / T6) — the tail starts at `d = w+1`.
- **`d = w+1` (the smallest): `D_{w+1} <= 30 C(N,w+1)`** — the b2 result T12, an ABSOLUTE ceiling
  (`E_{w+1} = 2*#{U: |U|=2(w+1), Qhat^2-P_U perfect square}`, each degree-`(w+1)` locator has `<= n/(w+1)`
  full fibers). It is generically LOOSE: measured `D_3 = 80` vs the T12 ceiling `30*C(20,3)=34200`.
- **`r_d = D_d/exp_d ~ 1` UNIFORMLY across ALL `d>w`, sparse AND dense** — the key correction. Measured
  `r_d`: `d=3` (sparse, `C=1140<Q^w`) `1.053`; `d=4` (sparse, `C=4845<Q^w`) `1.087`; `d=5..9` (dense)
  `1.00, 0.97, 1.01, 1.04, 1.04`; `d=10` (extreme, `exp_d=18`) `0.33` (small-count noise). No sparse/dense
  break — the disjoint count is generic throughout. `Gamma_2(tail)/flat = 1.0078`.

**The remaining rigorous step, corrected.** The per-`d` target is the DISJOINT PTE-pair count law
    **`D_d = C(N,d) C(N-d,d) Q^{-w} (1 + o(1))`  for every `d > w`**  (equivalently `r_d = e^{o(N)}`),
which is a Lang–Weil / moment-map equidistribution for `w` power-sum constraints on *disjoint* `d`-subsets —
the generic count `C(N,d)C(N-d,d)Q^{-w}` plus a coset-structured over-count that is lower order and absolutely
capped by the T12 rigidity ceiling (`D_{w+1} <= 30 C(N,w+1)`, generalizing to `D_d <= (structured) C(N,d)`).
Because the disjoint constraint removes the diagonal, this is a genuine variety count and holds UNIFORMLY in
`d` (verified above), unlike the diagonal-contaminated `sum|e_d|^2`. It remains a SECOND-moment statement,
decoupled from and strictly weaker than the `s=infinity` (max-fiber / sup) and `s=2` (participation-ratio,
#434) cruxes. Base `d<=w` machine-checked; `d=w+1` ceiling from T12; `r_d ~ 1` verified across sparse+dense;
the uniform-in-`d` disjoint-count equidistribution is the concrete open piece.
