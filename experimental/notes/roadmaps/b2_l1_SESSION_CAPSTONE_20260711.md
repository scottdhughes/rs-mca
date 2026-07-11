# L1/b2 node #5 — session capstone (2026-07-11)

Clean, resumable summary of the 07-10/07-11 work on the max-fiber crux. Working log with all derivations +
numerics is `b2_l1_reduction_ledger.md`; verification scripts are `experimental/scripts/b2_*.py` + one Sage
file. Everything below is VERIFIED numerically (Python, cross-checked with Sage / Codex where noted).

## 1. The object and target

μ_n ⊂ F_p^*, n = 2^21, n | p−1, p = KoalaBear ≈ 2^31. Φ(a) = (a,…,a^w), F(S) = Σ_{a∈S}Φ(a) ∈ F_p^w.
N(v) = #{ m-subsets S : F(S) = v }, N_max = max_v N(v). Deployed: w = 67471, m ≈ 0.468n, μ = C(n,m)/p^w = n^{1.7}.
**TARGET: N_max ≤ n^3.** (Equivalently: # binary weight-m codewords of the cyclic [n,n−w,w+1] RS code.)

## 2. THE crux (one object, reached from ~10 independent angles, all open)

A SIGNED cancellation in Σ_{ξ≠0} e_m({χ_ξ(a)}), χ_ξ(a)=e_p(ξ·Φ(a)), at depth w > √p — equivalently a fiber-
resolved lower bound "the max fiber is not near-Sidon." Truth holds with huge room (N_max ≈ n^1.7 ≪ n^3):
a TRUE-but-provably-hard barrier, not a suspected counterexample. This IS the repo's own open "conjecture Q /
primitive q-collision moment Γ_r" (grande_finale) and LegaSage's #582 "large R=2 fiber can't be near-Sidon."

## 3. Verified ASSETS (proven / clean — do not re-derive)

- ENGINE identities, all w≥2, PROVEN (Newton + orthogonality; Aristotle Lean proof builds clean, 0 sorry):
  Σ_c|τ_w(c)|^2 = p^w n, Σ_c|τ_w(c)|^4 = p^w(2n^2−n). (`b2_engine_identity_proof.md`.)
- 2nd-moment TRADE identity (cross-checked Python+Sage): Σ_v N(v)^2 = C(n,m) + Σ_{s≥3} V(s) C(n−2s,m−s),
  V(s) = # ordered disjoint s-for-s (p_1,p_2)-preserving trades. (`b2_totalenergy_check.py`, `b2_cas_crosscheck.sage`.)
- POSITIVE-COUNT reframe (100% verified): E(F) − (2f^2−f) = 2·#{disjoint-compatible-trade triples} — the razor
  is a non-negative count, no cancellation in the STATEMENT. (`b2_constructive.py`.)
- SELF-SIMILAR: E(F)=Σ N_sub, N_sub = a fiber of the SAME 2-constraint problem on x1△x3 (density 1/2); excess
  localized to nearly-complementary pairs, sub-fibers at scale ≈2m. Density-1/2 fixed point is empirically FLAT
  (R(N,1/2) ≈ 1.2, logR/N→0). (`b2_selfsimilar.py`, `b2_density_half.py`.)
- BERNOULLI relaxation (verified, cost √(2n)): N(v) ≤ Pr_ρ(F=v)/[ρ^m(1−ρ)^{n−m}]; char. function factors over a.
- char-0 count N_0^{(0)} = 0 at deployment (Lam–Leung antipodal; no algebraic backbone; purely analytic).
- w≤3 is a numerically-validated SKELETON, NOT a theorem (deviation-bound deferred; prior "PROVED" corrected).

## 4. Rule-out ledger (each VERIFIED dead for deployment; one unifying reason)

ONE mechanism kills the magnitude family: SIGN-BLINDNESS + p^w frequency count. Specifically:
- L^2 / L^{2k} / restriction / Halász anti-concentration — sign-blind; CS loses p^{w/2}=n^{49784} vs slack n^{1.3}.
- Per-frequency Weil (deg w) — vacuous, w=67471 > √p≈46340. RV-LCD adaptation REDUCES to this (caps w≤22).
- Rudnev / high-dim incidences — only F_p^2, F_p^3; blocked w≥4.
- BSG / Freiman — fiber nearly-Sidon (doubling f^{0.89}→∞), structure theorems vacuous.
- Tower / twist descent — handles only periodic part; heavy PRIMITIVE fibers not confined.
- Clean identities are for the wrong object (2nd moment, not the fiber-resolved 4th-order energy).

## 5. Literature home (found via TheoremSearch; none plugs in)

- Prendiville, "Solving equations in dense Sidon sets" (arXiv 2005.03484): near-Sidon ⇒ spectrally flat via
  Bohr/circle-method transference. MECHANISM adapts (near-Sidon ⇒ flat vs constraint-set ⇒ structured ⇒ razor);
  but 1-dimensional, machinery must be rebuilt for the high-dim Boolean cube.
- Rudelson–Vershynin LCD small-ball = the max-fiber anti-concentration framework (but over F_p reduces to Weil).
- Higher-order Fourier / equidistribution of high-rank forms (Spherical HOFA Thm 5.1; Green 2006) — a cousin
  (our constraints are LINEAR in the bits, rank-2 Vandermonde, not high-rank quadratic forms in x).
- Shkredov energy lower bounds; Mathlib has Finset.addEnergy + pluennecke_ruzsa (a certification path).

## 6. Open levers for a future session (in rough order of promise)

1. Adapt Prendiville's SPECTRAL FLATTENING (near-Sidon ⇒ flat) to the high-dim Boolean cube + moment curve:
   show a near-Sidon fiber would be spectrally flat, contradicting its being a linear-constraint solution set.
2. A SIGNED large-sieve / joint-cancellation-across-dilates estimate for Σ_{ξ} ∏_r S(rξ) at depth w>√p (the
   manuscript's "joint cancellation across the whole character-tuple family").
3. Self-improving INDUCTION on scale via the density-1/2 fixed point + complementation symmetry v↦−v.
4. Inverse Littlewood–Offord / entropy at EXPONENTIAL scale for the vectors Φ(a) (Bernoulli reformulation).

## 7. Cross-model status

Codex 5.6 attacked twice (independently): converged with the above (mass-capacity bound G_0 ≥ P^2/H − 2P,
central-fiber obstruction). ChatGPT 5.6 Pro prompt prepared (`scratchpad/chatgpt56pro_prompt.md`). Ecosystem:
AllenGrahamHart (F3/row-sharp Q, #583–604), LegaSage (max-fiber/C9/Sidon, #565–589) — same crux, all open.
Repo: synced to origin/main e190193; ~25 commits on scott/l1-node5-reduction (fork only, NOT upstream).
