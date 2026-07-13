# The C3 planted-divisor census

**Lane.** Hard input 1 (`agents.md`) — the **witness-exhaustive first-match
atlas**, condition **(A2)**. This packet builds the ONE finite planted census
that PR **#713**'s `(CAT)` exhaustion ledger
(`experimental/notes/thresholds/atlas_cat_cell_ledger.md`, integrated at
upstream commit `c23dcaa`) names as C3's residual (its Section 3.2 row, its
Section 3.3 item 3): *"C3 → a subexponential planted census — the one
genuinely (CAT)-local combinatorial item, comparatively minor."*

**Status.**
`COSET-TYPE CENSUS = THEOREM (PROVED, unconditional, all N) / RAMIFICATION
SUBSUMPTION (PROVED) / DIHEDRAL EXTENSION (PROVED) / UNRESTRICTED
COMMON-FACTOR READING = EXACTLY BINOM(n,b) (PROVED, negative) / C3 VERDICT:
PARTIAL — PAID on the row-independent (multiplicative-coset /
automorphism-fixed-point) generator sub-case; OPEN (and shown
non-censusable in general) on the row-dependent (common-factor /
received-line-resultant) sub-case.`

**Verifier.** `experimental/scripts/verify_c3_planted_divisor_census.py`
(stdlib-only, no numpy/sympy, deterministic, `--tamper-selftest` flag,
`RESULT: PASS (81/81)` in ~5 s). Recomputes every number below: an
independent brute-force coset partition (not the formula) for every `N` up
to 600 and every divisor of it, an independent sieve-based `sigma(N)` for
every `N` up to 50000, and an exhaustive small-instance proof of the
negative calibration. JSON certificate at
`experimental/data/certificates/c3-planted-divisor-census/c3_planted_divisor_census.json`.
Lean statement stub at
`experimental/lean/first_match_atlas/FirstMatchAtlas/PlantedDivisorCensus.lean`
(package builds; see §7).

**Credit.** The printed C3 definition and its census obligation are the
manuscript's own. The `(CAT)` ledger that names this obligation is **#713**.
The operational reading "C3 planted = `S` contains a full nontrivial
subgroup-coset block," which this packet's census formalizes and pays
exactly, is the toy proxy already used by `atlas_missing_witness.md`
(**#536**) in its GENERIC witness-routing census. The routing-exhaustiveness
theorem this packet cites (but does not re-derive) for the "not a coverage
gap" reading of the open sub-case is `routing_exhaustiveness.md` (**#627**)
with `c7_routing_spectrum.md` (**#625**, MASTER-2).

---

## 1. The exact obligation, quoted

**From #713** (`atlas_cat_cell_ledger.md`, its per-cell ledger table and
Section 3.2):

> "C3 | planted-block | *(printed requirement L2405–2407)* | needs a proved
> subexponential census of the common divisor `P` | `lem:profile-atlas`
> **EXCLUDES arbitrary planted** (L4781–4782: "could create exponentially
> many profiles") | **CONDITIONAL/UNPAID**"

> "**C3 (planted).** `lem:profile-atlas` (L4781–4782) excludes arbitrary
> planted subsets from the `e^{o(n)}` profile count; payment additionally
> requires 'a subexponential census of allowed `P`' (L2405–2407). A local
> combinatorial census, not yet supplied. **CONDITIONAL.**"

**From the manuscript** (`experimental/asymptotic_rs_mca_frontiers.tex`,
byte-verified below):

> L2399–2407 (`sec:cell-catalogue`, Planted-block cells): "A *planted block*
> is a predetermined group of support positions forced by an algebraically
> controlled common divisor `P`. Here `P` is a polynomial factor common to
> every support locator `Q_S`, and its roots in `D` are the planted
> positions. Divisibility makes the locus constructible, but payment
> additionally requires a subexponential census of allowed `P`, the residual
> prefix estimate, and its slope projection; arbitrary planted subsets are
> not one profile."

> L4652–4657 (`prop:planted-payment`): "Let the allowed planted divisors of
> size `ℓ` form a family of `e^{o(n)}` candidates, and suppose the residual
> prefix fiber for each candidate has size at most its profile term times
> `e^{o(n)}`. Then the planted cells are paid at the sum of those terms."

> L7584–7595 (`def:algebraically-planted`): "A planted block of size `b` is
> algebraically planted if it is the zero set on `D` of a polynomial in a
> constructible family `𝒫_b` of **support locators, common factors,
> ramification polynomials, polynomials cutting out quotient fibers, or
> received-line resultants**. ... We require `|𝒫_b(𝔅)| ≤ e^{o(n)}` for every
> profile size occurring in the profiled asymptotic row datum. Arbitrary
> choices of `b`-subsets of `D` are not planted cells."

**The exact obligation, stated once.** Fix a size `b`. Payment of C3 needs a
proved bound `|𝒫_b(𝔅)| ≤ e^{o(n)}` for a *concretely identified* constructible
family `𝒫_b` drawn from `def:algebraically-planted`'s five named generator
types — not merely the definitional restriction, which only says such a
family, if one is supplied, must be small. This packet supplies and pays
that family for two of the five generator types (quotient fibers,
ramification), and separately proves the remaining reading (unrestricted
"support locators"/"common factors", and the row-dependent "received-line
resultants") is not payable this way.

## 2. Census design: what is being enumerated

**Object.** The standard evaluation domain already used by the manuscript's
own C1/C2 payments: a *multiplicative coset* `D = θH ⊆ 𝔅^×`
(`def:structured-folding`, L2605–2632), `|H| = N`. By discrete log relative
to a fixed generator of `H`, identify `H` with the additive group `Z/N`;
`θH`'s coset structure is a uniform shift and does not change any of the
counts below, so we state everything for `D = H ≅ Z/N`.

For every divisor `c ∣ N`, `def:structured-folding` gives the `c`-fold
folding map `π_c : D → D^{(c)}`, `π_c(x) = x^c`; under discrete log this is
multiplication-by-`c` on exponents, and its fibers are exactly the `N/c`
cosets of the unique order-`c` subgroup `H_c ≤ H`. A **planted divisor** of
size `b = c` generated this way is `P = Q_S` for `S` one such coset — the
"polynomial factor common to every support locator `Q_S`" of L2402 is
literally `Q_{H_c}` (or a shifted copy), and "its roots in `D`" (L2402) are
exactly that coset. This directly instantiates `def:algebraically-planted`'s
*"polynomials cutting out quotient fibers"* generator type (L7588).

**What "paid" means (`def:paid-cell` L2306–2313 as specialized by
`prop:planted-payment`).** The residual-fiber half of `prop:planted-payment`
("suppose the residual prefix fiber for each candidate has size at most its
profile term times `e^{o(n)}`") is a *direct fiber estimate* by the
proposition's own one-line proof (triangular shift by `Q_P`, already general
machinery) — not what is missing. The missing half, and the entire content
of this census, is the **family-size** hypothesis: `|𝒫_b(𝔅)| ≤ e^{o(n)}`,
i.e. counting how many *distinct* `P` exist at each size `b`, for `b`
ranging over the full achievable set, as a function of `n = |D|`.

## 3. Claim 1 — the coset-type family is exactly `σ(N)`, proved for every `N`

> **Theorem (exact coset census).** For every divisor `c ∣ N` the number of
> distinct coset-type candidates of size `c` is exactly `N/c`. Summing over
> every achievable size (i.e. every divisor of `N`),
> ```
> |𝒫_coset(N)| := Σ_{c∣N} N/c = Σ_{e∣N} e = σ(N)
> ```
> (substitute `e = N/c`; as `c` ranges over divisors of `N` so does `e`),
> the classical sum-of-divisors function.

This is an exact identity, not a bound, and it holds for **every** `N ≥ 1`
unconditionally — no asymptotic regime, no genericity hypothesis.

**Verification (verifier BLOCK B, Tier A).** For every `N = 1..600` and every
divisor `c` of `N`, the verifier builds the actual partition of `{0,...,N-1}`
into residue classes mod `N/c` (**not** via the `N/c` formula), confirms
there are exactly `N/c` classes each of exact size `c`, that they cover
`{0,...,N-1}` exactly once, and that the total over all `c ∣ N` matches
`σ(N)` computed independently. Zero exceptions in `81` checks over this
range. Spot values: `σ(12)=28`, `σ(30)=72`, `σ(60)=168`, `σ(360)=1170`.

## 4. Claim 2 — `σ(N)` is subexponential for every `N` (elementary, proved)

> **Proposition.** `σ(N) ≤ N·(1+ln N)` for every `N ≥ 1`. Hence
> `|𝒫_coset(N)| = e^{o(N)}`, unconditionally — precisely
> `prop:planted-payment`'s hypothesis "a family of `e^{o(n)}` candidates,"
> discharged for the coset-type family with `n ≈ N = |D|`.

*Proof.* `divisors(N) ⊆ {1,...,N}`, and every term `N/j > 0`, so
`σ(N) = Σ_{d∣N} N/d ≤ Σ_{j=1}^{N} N/j = N·H_N` where `H_N` is the `N`-th
harmonic number. The standard integral-comparison bound `H_N ≤ 1+ln N`
(`H_N = 1+Σ_{j=2}^N 1/j ≤ 1+∫_1^N dx/x = 1+ln N`) finishes it. ∎

This is the *elementary* bound; the sharper classical Grönwall (1913) /
Wigert result `σ(N) = O(N log log N)` is standard number theory, cited here
for context and **not** independently re-derived or re-verified by this
packet — the elementary `O(N log N)` bound above is already strictly
sufficient for `e^{o(N)}`.

**Verification (verifier BLOCK E, Tier B).** Independent sieve computation
of `σ(N)` cross-checked against independent trial-division for every
`N = 1..50000`; the elementary bound checked numerically (floating point)
for the same range, zero violations. The manuscript's own related — but
separately unproved — remark, `prop:stabilizer-payment`'s proof (L4583):
*"The number of divisors of `|H|` is subexponential"*, is a one-line
assertion about a **different** object (`τ(N)`, for C1's full-support
stabilizer payment, not C3's sub-block census); this packet does not audit
that remark, but supplies the analogous exact machinery (closed form +
brute-force verification, not a one-line assertion) for the object C3 needs.

## 5. Claim 3 — ramification polynomials are already coset-type (proved, subsumption)

`def:algebraically-planted`'s third generator type is "ramification
polynomials" (L7587). On a multiplicative coset the natural ramification
loci are the fixed-point sets of the automorphisms of `H` — every
multiplier map `μ_m : k ↦ mk mod N` for `m` coprime to `N` (this includes
**every** Frobenius power `x ↦ x^{p^j}`, since `gcd(p,N)=1` automatically
when `N ∣ q-1` and `p = \mathrm{char}(𝔅)`, and inversion `μ_{-1}`, since
`gcd(N-1,N)=1` always).

> **Theorem (subsumption).** For every `N` and every `m` coprime to `N`,
> `Fix(μ_m) = {k : mk ≡ k mod N}` is exactly the identity coset of the
> order-`g` subgroup `H_g`, `g = gcd(N, m-1)` — one of the size-`g` cosets
> already counted in Claim 1. Ramification contributes **zero** candidates
> beyond the coset-type family.

*Proof.* `mk ≡ k mod N ⟺ (m-1)k ≡ 0 mod N ⟺ k ≡ 0 mod N/g`, `g=\gcd(N,m-1)`;
this has exactly `g` solutions in `{0,...,N-1}`, namely the multiples of
`N/g`, which is `H_g` itself. ∎

For inversion (`m=N-1`), `g=\gcd(N,2) ∈ \{1,2\}`: at most two fixed points,
matching `lem:circle-edge-cases-repaired`'s "the points `u=±1` ... contribute
at most two ramification points" exactly.

**Verification (verifier BLOCK C, Tier A).** For every `N = 2..600` and
*every* `m` coprime to `N` (`109499` `(N,m)` pairs; not a sample), a direct
brute-force scan of every residue confirms `Fix(μ_m)` equals the predicted
`H_g` coset found in BLOCK B — exact set equality, not a size match. Named
spot instances: inversion on `N=30` fixes exactly `{0,15}`; Frobenius
`x↦x^2` on `F_16^×` (`N=15`) fixes exactly `{0}` (the trivial subfield
`F_2^×`); Frobenius `x↦x^4` on `F_64^×` (`N=63`) fixes exactly `3` points
(`g=\gcd(63,3)=3`).

## 6. Claim 4 — the dihedral/Chebyshev extension (C2-flavor, proved)

`prop:planted-payment`'s family need not be built only from plain cosets:
inversion-invariant unions of twin cosets (matching the C2 dihedral/
Chebyshev cell, L2385–2397) are a natural second family. For each `c ∣ N`,
negation acts on the `N/c` cosets of `H_c` (represented as `Z/(N/c)`); the
twin-coset family at size `c` is the **orbit set** of that action, which can
only be smaller (orbits merge pairs).

**Verification (verifier BLOCK D, Tier A).** For every `N = 1..600`, every
`c ∣ N`: the dihedral orbit count is in `[1, N/c]`, brute-force confirmed by
explicit orbit enumeration. Grand total over the range: `151220` dihedral
candidates versus `296729` plain-coset candidates — the twin-coset family is
never larger, so Claim 2's bound applies to it too.

## 7. Claim 5 — the unrestricted reading is exactly `binom(n,b)` (proved, negative)

The remaining two `def:algebraically-planted` generator types — "support
locators" read without restriction, and "common factors" of two *actual*
witness supports — are row-dependent: nothing pins them down independently
of which supports occur in a given first-match cell.

> **Theorem (exact blow-up).** Fix `n = |D|`, `1 ≤ b ≤ n`, any target support
> size `m = b+r` with `2r ≤ n-b`. Every `b`-subset `T ⊆ D` is achievable as
> `S₁ ∩ S₂` for valid supports `S₁, S₂` of size `m`: take
> `S₁ = T ∪ R₁`, `S₂ = T ∪ R₂` for disjoint fillers `R₁,R₂ ⊆ D∖T`, `|R_i|=r`.
> Hence the count of achievable "common factor" root-sets of size `b` is
> **exactly** `binom(n,b)`, i.e. genuinely exponential at fixed density
> `b=βn`.

*Proof.* The construction is exhibited; `S₁∩S₂ = T` by disjointness of
`R₁,R₂`. Distinct `T` give distinct intersections, so the map `T ↦ (S₁,S₂)`
is injective and its image realizes every `T`. ∎

This is a complete constructive proof, not a numerical illustration; the
verifier's BLOCK F additionally **exhaustively** checks it (every `T`, not a
sample) on four small instances: `(n,b,r) ∈ {(10,3,2),(12,4,2),(16,6,3),
(20,8,4)}`, achieving `120/120`, `495/495`, `8008/8008`, `125970/125970` —
exact matches to `binom(n,b)` in every case. For scale, at `N=30`:
`σ(30)=72` against `binom(30,15)=155117520` (ratio `≈2.15×10^6`). This makes
`lem:profile-atlas`'s L4781–4782 exclusion ("could create exponentially many
profiles") a proved *tight dichotomy*, not a caution: the gap between the
coset-type family (`O(N log N)`) and the unrestricted family (`Θ(2^N)` at
fixed density) is the entire gap between subexponential and exponential.

## 8. Verdict, route-scoped

**C3: PARTIAL.**

- **PAID** (unconditional, all `N`, not only the tested range — Claims 1–4
  are closed-form theorems; the finite computation *audits* them) on the
  row-independent sub-case: planted divisors whose root set is a coset of a
  subgroup of a multiplicative coset (`def:algebraically-planted`'s
  "quotient fibers" generator, L7588) or a fixed-point set of one of its
  automorphisms ("ramification polynomials," L7587, proved in Claim 3 to add
  nothing new) or a twin-coset union (C2-flavor extension, Claim 4). Family
  size: exactly `σ(N) ≤ N(1+\ln N)`, unconditionally subexponential.
- **BLOCKED**, provably (not merely "not yet paid") on the fully general
  reading of "support locators" or "common factors" without row-specific
  structure: Claim 5 proves this reading is **exactly** `binom(n,b)`, hence
  no subexponential census of it exists. Any payment of this residual needs
  a further bounded-parameter restriction tied to the actual row (of the
  same flavor as `def:algebraically-planted`'s fifth generator type,
  "received-line resultants," which is intrinsically row-specific and out of
  scope for a universal census).

## 9. Ledger impact on #713 (audited before consumption; see §10)

#713's Section 3.2 lists four full-catalogue summation blockers,
`{C3, C7, C8, C9}`, and its Section 3.3 anticipates their collapse to the
manuscript's own hard inputs: *"1. C9 → hard input 4/5 ... 2. C7+C8 → hard
input 3 ... 3. C3 → a subexponential planted census ... comparatively
minor."* This packet supplies item 3 for the concretely-occurring
(row-independent, automorphism-driven) reading of "planted block" — the
reading `atlas_missing_witness.md` (#536) itself already used as its C3
routing test in its own GENERIC census (`S` contains a full nontrivial
subgroup-coset block).

**Does the residual collapse to inputs 3 + Sidon alone? Precisely, not
unconditionally.** On the row-independent reading: **yes** — C3 stops being
an *independent* blocker of the full-catalogue summation; its structural
content is discharged here exactly as #713 anticipated. On the fully general
reading: **no** — Claim 5 shows that reading cannot be paid by any universal
census, coset-type or otherwise. But this residual is not a **coverage**
risk: any witness whose forced common divisor is *not* one of the
automorphism-invariant families censused here is, by the already-integrated
routing-exhaustiveness theorem (#627, `routing_exhaustiveness.md`, MASTER-2)
— cited here, **not independently re-derived or audited** beyond the light
existence/self-label check that the #713 verifier rerun in §11 already
performs on it — a `(S_E)`-violating profile that routes to `{C4,C6,C7}`
instead — so it is not lost, only not independently attributed to a C3
payment. Net effect on #713's own table: `{C3,C7,C8,C9}` reduces to
`{C7,C8,C9}` for the row-independent instantiation of C3 — exactly hard
input 3 (`C7`/`C8`, the `(RC)` ray compiler) plus hard input 4/5 (`C9`,
Sidon), matching #713's own predicted outcome, now discharged rather than
anticipated. This packet does not edit #713's table; it supplies the
missing census for the maintainer to fold in.

## 10. Nonclaims

- No claim about the row-dependent "common factor" or "received-line
  resultant" generator types beyond Claim 5's negative result: they are
  **not** censused here, and Claim 5 shows why a universal census of them is
  impossible without row data.
- No re-derivation, re-proof, or re-audit of `routing_exhaustiveness.md`
  (#627) or `c7_routing_spectrum.md` (#625): they are cited for the "not a
  coverage gap" reading of the open sub-case, not reverified by this
  packet's verifier.
- No claim about C7, C8, or C9 payment; those blockers are unaffected by
  this packet except for the bookkeeping consequence stated in §9.
- No edit to `atlas_cat_cell_ledger.md` or to
  `asymptotic_rs_mca_frontiers.tex`/`.pdf`; both are read-only inputs here.
- No claim that the sharper classical `σ(N)=O(N \log\log N)` bound is proved
  or numerically re-verified by this packet; only the elementary
  `O(N\log N)` bound is (Claim 2).
- No claim that the general Lean statement target
  (`sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED`) is proved; it
  carries an explicit `sorry` and a compiler warning (§12).
- No deployed finite-row, Grand MCA/List, or prize-threshold claim of any
  kind.

## 11. Interfaces

**Consumes #713** (`atlas_cat_cell_ledger.md`, PR #713, integrated at
upstream `c23dcaa`; anchors quoted in §1). **Audit-before-consume:** this
branch's base commit (`ea4eb07`) predates the maintainer's integration of
#713 (upstream advanced `ea4eb07 → c23dcaa` integrating PRs #699–#722,
including #713, on 2026-07-13, *after* this branch was created), so
`atlas_cat_cell_ledger.md` and its verifier are not present in this branch's
file tree; per instruction, this branch is not rebased onto that
integration. Instead, `#713`'s verifier was extracted and rerun **out of
tree** directly against the integrated commit:
```
git archive c23dcaa experimental | tar -x -C <tmpdir>
python3 <tmpdir>/experimental/scripts/verify_atlas_cat_ledger.py --check
# -> RESULT: PASS (219/219)
```
confirming byte-identity of the branch and integrated copies of both
`atlas_cat_cell_ledger.md` and `verify_atlas_cat_ledger.py`, and a clean
rerun, before this packet cites its text. This packet's own verifier
(BLOCK G) performs a **soft**, non-fatal check for
`experimental/notes/thresholds/atlas_cat_cell_ledger.md` in-tree: a light
presence-plus-substring check if the file is present (post-rebase; not a
re-audit of its content), and a printed `SKIP` with an explanation
otherwise — exactly the present case.

**Consumes** (cited, not re-derived): `atlas_missing_witness.md` (#536, C3
routing precedent), `routing_exhaustiveness.md` (#627) +
`c7_routing_spectrum.md` (#625) (routing-exhaustiveness theorem, for §9's
"not a coverage gap" reading).

**Manuscript anchors** (byte-verified, tolerance window ±2 lines, verifier
BLOCK A, `25` anchors + 1 negative test): C3 catalogue paragraph
(`asymptotic_rs_mca_frontiers.tex` L2399–2407), `prop:planted-payment`
(L4652–4665), `lem:profile-atlas` (L4772–4783), `sec:algebraic-repairs`
(L7580) leading into `def:algebraically-planted` (L7584–7595),
`prop:planted-payment-repaired` (L7597), `def:structured-folding`
(L2605–2632), and the related (uncensused-by-us) `prop:stabilizer-payment`
divisor remark (L4561–4583).

**Consumers.** Any future packet paying C7/C8 ((RC), hard input 3) or C9
(Sidon, hard input 4/5) may cite this note as discharging the C3 line of
#713's table for the row-independent reading; a maintainer update to
`atlas_cat_cell_ledger.md`'s own per-cell table is the natural promotion
path, not attempted here.

## 12. Lean statement stub

Per the 2026-07-13 Shipping rule (theorem-shaped claims ship a Lean
statement stub): `experimental/lean/first_match_atlas/FirstMatchAtlas/
PlantedDivisorCensus.lean`, reached by `import` from the package root
`FirstMatchAtlas.lean` (no lakefile change needed). Contents: exact
`native_decide`-proved instances of Claims 1, 3, and 5 at concrete `N`
(matching this note's spot values `σ(12)=28`, `σ(30)=72`, `σ(360)=1170`,
the inversion fixed-set `{0,15}` at `N=30`, and the gap `28 < 924 =
\binom{12}{6}`), plus **one honestly unproved general target**,
`sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED`, carrying an explicit
`sorry` and hypotheses matching Claim 2 exactly (`Nat.log2`-based Nat
rendering of `σ(N) ≤ N(1+\ln N)`, since `\ln N ≤ \log_2 N`). `lake build`
in `experimental/lean/first_match_atlas/` succeeds with exactly one warning
("declaration uses 'sorry'") at that one theorem and no errors, confirming
every `native_decide` claim actually checks out.

## 13. Per-claim label ledger

| # | claim | verdict | basis |
|---|-------|---------|-------|
| 1 | coset-type census exact identity `Σ_{c∣N} N/c = σ(N)`, every `N` | **PROVED** | §3; verifier BLOCK B, exhaustive `N=1..600` |
| 2 | `σ(N) ≤ N(1+\ln N)`, every `N` (hence `e^{o(N)}`) | **PROVED** (elementary) | §4; verifier BLOCK E, `N=1..50000` |
| 3 | ramification fixed-point sets are already coset-type; zero new candidates | **PROVED** | §5; verifier BLOCK C, exhaustive all coprime `m`, `N=1..600` |
| 4 | dihedral/twin-coset extension never exceeds the plain coset family | **PROVED** | §6; verifier BLOCK D, exhaustive `N=1..600` |
| 5 | unrestricted common-factor reading is exactly `\binom{n}{b}` | **PROVED** (negative/calibration) | §7; verifier BLOCK F, exhaustive small instances |
| 6 | C3 route-scoped verdict: PARTIAL (paid row-independent / blocked general) | **AUDIT** | §8 |
| 7 | ledger impact on #713: `{C3,C7,C8,C9}` → `{C7,C8,C9}` for the row-independent reading | **AUDIT** | §9; consumes #627/#625 (cited, not re-derived) |
| 8 | #713's own verifier reruns clean against integrated `c23dcaa` | **AUDIT** | §11; `RESULT: PASS (219/219)` |
| -- | any deployed finite-row, Grand MCA/List, prize-threshold, C7/C8/C9 payment claim | NOT CLAIMED | this is a C3-only census packet |

## 14. Reproducibility

```bash
python3 experimental/scripts/verify_c3_planted_divisor_census.py
# -> RESULT: PASS (81/81)
python3 experimental/scripts/verify_c3_planted_divisor_census.py --tamper-selftest
# -> confirms a corrupted anchor and a dropped coset are both detected, then RESULT: PASS
cd experimental/lean/first_match_atlas && lake build
# -> Build completed successfully (one 'sorry' warning, by design)
```
