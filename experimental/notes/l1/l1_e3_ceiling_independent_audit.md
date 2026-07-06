# L1 KEY LEMMA `E_3 <= ell-2` — independent audit + extremal-locus dissection

- **Status:** AUDIT / INDEPENDENT CORROBORATION (second engine, exact). Not a proof.
- **Agent/model:** Claude Opus 4.8, branch `scott/l1-e3-ceiling-open-chart`.
- **Date:** 2026-07-06.
- **Target:** the KEY LEMMA `E_3 <= ell-2` of
  `experimental/notes/l1/l1_prime_ell_frontier_corrected.md` §3 — the single OPEN core
  gating the vacancy (lower) side of the corrected frontier law `m*(ell) = (ell+3)/2`.
  Independent cross-check of the shipped stdlib-Python verifier
  `verify_l1_prime_ell_frontier_corrected.py`. Sanctioned L1 interaction: audit only;
  does not edit the frontier note or Codex's L1 branches.

## What was reproduced (Sage / native GF(p), independent primitive root + cosets)

`experimental/scripts/verify_l1_e3_ceiling_independent.sage` — recomputes the shipped
witness spectra on Sage's FLINT/PARI GF(p) stack (independent of the hand-rolled `pow`
modular arithmetic in the shipped verifier). All witnesses reproduce **exactly**:

| witness | spectrum head | listing (top-m >= 2ell) | E_3 vs ell-2 |
|---|---|---|---|
| ell=11 p=199 | [4,4,3,3,3,3,2,…] | top-7 = 22 = 2ell (top-6 = 20 <) | 8 <= 9 |
| ell=11 p=331 | [5,5,4,3,2,2,2,…] | top-7 = 23 >= 22 (top-6 = 21 <) | **9 = ell-2 (saturates)** |
| ell=13 p=313 | [5,4,4,3,3,3,3,2,…] | top-8 = 27 >= 26 (top-7 = 25 <) | **11 = ell-2 (saturates)** |
| ell=17 p=409 | [6,5,4,4,4,3,2,…] | top-10 = 34 = 2ell (top-9 = 32 <) | 14 <= 15 |
| ell=17 p=103 | [6,5,5,4,4,3] | — (E_3 anchor) | **15 = ell-2 (saturates)** |

**Consequences.** (a) The achieved-frontier (upper-side) witnesses are real: the codewords
list exactly at `m = (ell+3)/2` and NOT below (`top-(m-1) < 2ell`). (b) The `E_3 <= ell-2`
ceiling is **saturated** at ell = 11, 13, 17 — so `ell-2` is the correct, sharp, un-lowerable
constant (independently confirming the in-PR refutation of the earlier `ell-3` claim).

## Extremal-locus dissection (what the open proof must handle)

`experimental/scripts/extremal_structure_e3.sage` — for each E_3 = ell-2 saturator, recovers
the excess-carrying cosets (mu_b >= 3) as fibers with label `w_b = b^ell` and shared value
`c_b`, and computes over GF(p): `R = rank` of the coincidence rows `{v(x)-v(anchor)}`,
`v(x)=(x,…,x^{ell-1})`; `dim U = ell - R`; `delta = (P-K) - R`, `P = sum mu_k`.

| saturator | K | fiber sizes | P | R | dim U | delta | all pairs delta=0 |
|---|---|---|---|---|---|---|---|
| ell=11 p=331 | 4 | [5,5,4,3] | 17 | 9=ell-2 | 2 | **4 = K** | yes (6 pairs) |
| ell=13 p=313 | 7 | [5,4,4,3,3,3,3] | 25 | 11=ell-2 | 2 | **7 = K** | yes (21 pairs) |
| ell=17 p=103 | 6 | [6,5,5,4,4,3] | 27 | 15=ell-2 | 2 | **6 = K** | yes (15 pairs) |
| ell=17 p=409 (E_3=ell-3, contrast) | 6 | [4,4,3,6,5,4] | 26 | 15=ell-2 | 2 | 5 = K-1 | yes (15 pairs) |

**Findings.**
1. **The ceiling is a rank identity.** At the boundary `dim U = 2` (i.e. `R = ell-2`,
   the "constants-on-fibers" space is exactly `span{1, Gamma}`), `E_3 = P - 2K` and
   `delta = (P-K) - R = (P-K)-(ell-2)`, so **`E_3 = ell-2 <=> delta = K`** and the forbidden
   `E_3 = ell-1 <=> delta = K+1`. The KEY LEMMA is exactly **`delta <= K`**.
2. **The saturating coupling is irreducibly `K`-way.** Every pairwise (K=2) sub-config has
   `delta = 0` — the PROVED K=2 case — yet the `K` fibers jointly realize `delta = K`. No
   pairwise/local (moment) argument can produce this; it lives entirely in the note's
   **sole OPEN chart: `K >= 3` with affinely-independent fiber data `(w_k, c_k)`**.
3. The explicit `(w_k, c_k)` tuples for each saturator are emitted by the script and are the
   concrete extremal data any proof of the open chart must accommodate.

## Proposed proof route (for the open `K >= 3` chart)

`E_3 <= ell-2 <=> delta <= K <=> rank(fs|_Z) >= dim Z - K` (note §3 rank-lemma reduction).
Candidate attacks, ranked:
1. **Subspace non-vanishing form (note §3 second-pass (i)):** prove
   `dim(V_1 + … + V_K) >= E_3`, `V_k = h_k · F_p[X]_{<= mu_k - 2}`, `h_k = (X^ell - w_k)/g_k`
   the co-fiber locator. Concrete, and the K=2 syzygy minor is the base case — attack its
   `K`-fold generalization (a resultant/syzygy independence of low-degree multiples of the
   `h_k`). **This is the cleanest target; the extremal data above should be checked against
   `dim(sum V_k) = E_3` next.**
2. **Rank-drop rigidity via the affine data `(w_k, c_k)`:** the residue-line coordinate of
   `l1_coset_chart_residue_bridge_v1.md`; show `K+1` dependencies force an affine relation
   among the `(w_k, c_k)`, contradicting affine-independence.

## Subspace-form proof target validated (note §3 second-pass (i))

`experimental/scripts/subspace_form_e3.sage` — tests `dim(V_1+…+V_K) >= E_3`,
`V_k = h_k·F_p[X]_{<=mu_k-2}`, `h_k = (X^ell-w_k)/g_k` the co-fiber locator, at the
saturators. Result: the target **holds and is tight** (`= E_3`) at every saturator:

| config | E_3 | dim(sum V_k) | sum dim V_k (=P-K) |
|---|---|---|---|
| ell=11 p=331 | 9 | 9 (= E_3, tight) | 13 |
| ell=13 p=313 | 11 | 11 (= E_3, tight) | 18 |
| ell=17 p=103 | 15 | 15 (= E_3, tight) | 21 |
| ell=17 p=409 (E_3=ell-3) | 14 | 15 (= ell-2) | 20 |

**Lead (needs a universal check).** `dim(sum V_k) = ell-2` at BOTH the saturator and the one
non-saturator tested. If `dim(sum V_k) <= ell-2` is UNIVERSAL (a codim->=1 structure on the
co-fiber-multiple span) and `dim(sum V_k) >= E_3` is the independence side, then
`E_3 <= dim(sum V_k) <= ell-2` proves the KEY LEMMA as two separable steps. One data point
only — next verification step is a universal `dim(sum V_k) <= ell-2` sweep over random mixed
Gamma at ell = 7, 11, 13, 17.

## Reproducibility

```bash
sage experimental/scripts/verify_l1_e3_ceiling_independent.sage
sage experimental/scripts/extremal_structure_e3.sage
sage experimental/scripts/subspace_form_e3.sage
```

## Honest scope / limits

Independent corroboration of the **statement** (sharp, saturated, correctly reduced to the
`K>=3` chart) — NOT a proof of `E_3 <= ell-2` and NOT an independent counterexample search
above the reserve. The asymptotic/uniform `delta <= K` remains the open proof obligation.
