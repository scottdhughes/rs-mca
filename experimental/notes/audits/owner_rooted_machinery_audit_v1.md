# Owner-Rooted Machinery Adversarial Audit

```text
Status: AUDIT.  Six of seven assigned attacks: NO ISSUE.  One attack (image-scale
normalization) finds a real, LOCAL gap in one corollary, with an evident fix
(FIXED-proposal); it does not touch the packet's main theorem chain.
Audited packets (avdeevvadim, integrated at c23dcaa):
  owner_rooted_dense_band_localization_v1.md      (the main machinery)
  owner_rooted_positive_support_localization_v1.md
  secant_annihilator_localization_v1.md
Companion notes read for context (not primary targets, not re-audited here):
  primitive_signed_payment_barrier_v1.md, arbitrary_mask_idempotent_guardrail_v1.md
Verifier: experimental/scripts/verify_owner_rooted_machinery_audit_v1.py
  (stdlib, --check, --tamper-selftest, ~1s)
```

## Purpose

avdeevvadim's owner-rooted machinery is load-bearing: it is cited as the
active interface obligation by `heavy_fiber_admissibility_transfer.md`
(consumer note, in-tree at c23dcaa; reported to be shipped upstream as #717),
and is reported to be consumed further by two packets not present on this
tree (#723, #728; see Interfaces).  No in-tree audit of the machinery existed
before this note.  This packet runs the seven attacks named for this lane
against the three primary target notes, re-derives every boxed identity used
in the attacks by hand and independently in code (not by re-running
avdeevvadim's own verifiers and trusting their output), and replays the two
named finite constructions (Section 6's counterexample, Proposition 4.1's
regression) with fresh, independently written implementations.

All three shipped verifiers were rerun first (audit-before-consume floor):

```text
verify_owner_rooted_dense_band_localization_v1.py        --check --tamper-selftest : PASS
verify_owner_rooted_positive_support_localization_v1.py  --check                   : PASS
verify_secant_annihilator_localization_v1.py              --check                  : PASS
```

## Verdict table

| # | Attack | Target | Verdict |
|---|--------|--------|---------|
| A | Image-scale normalization (M/L consistency, norming dual to sparse-band corollary to projected-energy gate) | dense-band Prop 2.1 / Cor 5.1 / Thm 8.1 **vs.** positive-support Cor 5.1 (eq 5.6) | **OPEN GAP** in positive-support Cor 5.1 eq (5.6) only — FIXED-proposal below. Everything else checked: NO ISSUE |
| B | Norming-dual self-adjointness (band symmetry `A = -A` in every use) | dense-band Sec 1/Prop 2.1; positive-support Lemma 2.1; secant-annihilator Sec 1/Sec 2/Sec 4 | **NO ISSUE** |
| C | Slope rooting (Props 3.1/3.2) hidden hypotheses | dense-band Sec 3 | **NO ISSUE**, with a hypothesis-visibility FIXED-proposal for Thm 4.2 (shared with D) |
| D | Rim packing (Thm 4.2): double-counting direction, undeclared field-size dependence | dense-band Sec 4 | **NO ISSUE** |
| E | Projected-energy gate (Thm 8.1) one-way misuse downstream | dense-band Thm 8.1/Sec 9-10; positive-support Sec 1; secant-annihilator; barrier note | **NO ISSUE** |
| F | Section 6 counterexample: replay construction, verify parameters | dense-band Sec 6 | **NO ISSUE** — independently reproduced exactly |
| G | Prop 4.1 regression + guardrail scripts: replay, confirm exact reproduction | dense-band Prop 4.1 + `verify_owner_rooted_dense_band_localization_v1.py`, `verify_secant_annihilator_localization_v1.py` | **NO ISSUE** — reproduced exactly; the assigned field is `F_17`, not `F_7` (see G) |

---

## Attack A — image-scale normalization

**Claim under test.** Is the `M/L` normalization used consistently between
Prop 2.1 (norming-dual pullback), Cor 5.1 (sparse-band corollary), and Thm
8.1 (projected-energy gate), and between `f` and its positive-support
descendant `b`?

**What checks out.** The prefactor
`R_A = (L^{1-1/q}/M) ||P_A f||_q` is used identically across all three
target notes.  I re-derived by hand (and cross-checked in the verifier)
that Thm 8.1's `e_A, x_A` (dense-band L534-543) reconstruct exactly the
same `R_A`:

```text
e_A^{1/q} * x_A^{1-2/q} = (L^{1-1/q}/M) * E_A^{1/q} * (W*delta_A)^{1-2/q}
```

which matches the interpolation bound `||P_Af||_q <= ||P_Af||_2^{2/q} ||P_Af||_inf^{1-2/q}`
term for term (the verifier's `m_exponent`/`l_exponent` bookkeeping,
dense-band L177-178, both cancel to `0`, confirmed independently). Cor 5.1's
derivation from eq (18) (dense-band L374-381) is exact once `kappa=1` is
substituted (full slice), which I re-derived symbolically (see the note
below) and matches `exp(o(N)) * M/L^{1-1/q}` exactly. `owner_rooted_positive_support_localization_v1.md`
Lemma 2.1 (L81-155) and `secant_annihilator_localization_v1.md` Sec 4
(L322-434) both reuse the **same** `L`, `M` inherited from the original
`Omega^0`/`f` when defining `R_A(b)`, `Y_A(b)`, `x_B(b)` — they do not
recompute a smaller image size from `b`'s own support, which is exactly the
convention Attack A is checking for. A 120-instance randomized cross-file
chain (dense-band `f` -> positive-support `b` -> secant-annihilator `A'`,
same `H, M, L, n_+` threaded through all three stages, `q in {3,4,5,6}`)
reproduces every boxed inequality in this chain with zero failures
(verifier `chain_regression`).

**What does not check out.** `owner_rooted_positive_support_localization_v1.md`
Corollary 5.1 (L357-378), specifically the "sufficient condition in the
original parameters" at eq (5.6) (L367-376):

```text
boxed: R_A^2 >= 2*L^(2-2/q) / (M*(N-a+1))          [claimed sufficient for Omega_+^2 >= 2*n_+]
```

This is derived from `n_+ <= W <= M/(N-a+1)`.  But that bound on `W` is only
the **full-slice** specialization of dense-band Theorem 4.2's general bound
(dense-band eq 15-16, L320-357):

```text
W <= (1/(N-a+1)) * C(N,a)  =  kappa * M / (N-a+1),   kappa = C(N,a)/M >= 1
```

with `kappa = 1` **only** when `Omega^0` is the full slice `{T choose a}`.
The dense-band note itself is careful about exactly this: Section 5 states
in prose (L359-361) "The cleaner bound `rho <= 1/(N-a+1)` requires the
full-slice identity `M = C(N,a)`. It must not be inferred from the weaker
inclusion `Omega^0 subseteq {T choose a}`," and Theorem 8.1 (L585-586)
re-attaches the qualifier every time it cites Cor 5.1 ("If ... **on the
full slice**, Corollary 5.1 pays the band"). The positive-support note's own
Corollary 5.1 does the same derivation one level down (substituting `n_+`
for `W`) but never states the full-slice restriction, and the string
`kappa`/`full slice`/`sub-slice` does not occur anywhere in
`owner_rooted_positive_support_localization_v1.md` (grepped; zero hits).

**Minimal broken instance (verified in code, `kappa_gap_check`).** Take
`N=12, a=6` (so `C(N,a)=924`), and a genuine proper sub-slice `Omega^0` with
`M = 462` (half the full slice, `kappa = 924/462 = 2`), `L=200`, `q=4`. The
correct general sufficient condition needs `R_A^2 >= 2*kappa*L^{2-2/q}/(M(N-a+1)) approx 3.498`;
the note's literal eq (5.6) only demands `R_A^2 >= 1.749`. An `R_A^2` in
between (e.g. `2.624`) satisfies the printed hypothesis but not the bound
that actually controls `n_+` on this sub-slice, so eq (5.6) as printed does
not establish its own conclusion outside the full-slice case. I have **not**
constructed a full end-to-end `(f, Omega^circ)` pair that actually attains a
tight `n_+` on a sub-slice (that would require an explicit near-extremal
rim-packing construction on a proper sub-slice, a separate combinatorial
task) — the gap shown here is the missing `kappa` factor in the printed
inequality itself, which is sufficient to invalidate the corollary as
literally stated outside `kappa=1`.

**Blast radius.** Low/local. `secant_annihilator_localization_v1.md`
Theorem 5.1 (the note's actual "flat rooted source inverse theorem")
branches on `Omega_+^2 vs 2n_+` **directly** (Sec 3/Sec 4), never through eq
(5.6); eq (5.6) is presented as a convenience aside ("a sufficient condition
in the original parameters"), not a hypothesis of any downstream theorem in
the three target notes. I did not find any other use of it.

**Verdict: OPEN GAP, FIXED-proposal.** Either (a) restate eq (5.6) as
`R_A^2 >= 2*kappa*L^{2-2/q}/(M(N-a+1))` with `kappa` carried from the parent
note, or (b) restrict the corollary's header to "on the full slice
(`kappa=1`)" exactly as dense-band Cor 5.1 and Thm 8.1 point 1 already do.
Either repair is a one-line change to `owner_rooted_positive_support_localization_v1.md`
L367-376 and does not touch any other claim in the three notes.

---

## Attack B — norming-dual self-adjointness

**Claim under test.** Prop 2.1 (dense-band, Sec 2) and its reuses need the
band `A` to be genuinely symmetric (`A = -A`, closed under `gamma -> bar
gamma`) in *every* use, or `P_A` is not self-adjoint and Corollary 2.2's
positive mass and every downstream rooted-weight argument breaks.

**Numeric control (verifier `self_adjoint_control`).** On `Z/8`, a
deliberately asymmetric band `A = {1,2}` (since `-1 mod 8 = 7 notin A`)
gives `<P_A x,y> != <x,P_A y>` for random `x,y` (verified: they differ by a
nonzero imaginary part, `2i*Im(...)`, exactly the self-adjointness failure
one expects from an unbalanced multiplier). The symmetric band `A={1,7}`
(`-1 mod 8 = 7 in A`) gives exact equality to `1e-9`. This confirms the
hypothesis is load-bearing, not decorative.

**Where the hypothesis is actually invoked, and whether it holds every
time:**

1. Dense-band Sec 1 (L81-90) states `A=-A` as a standing hypothesis before
   Prop 2.1 is ever used, and gives the concrete justification for dyadic
   `|tau|`-bands (`tau(-gamma) = conj(tau(gamma))`). Prop 2.1's proof
   (L149-151) invokes self-adjointness directly ("The multiplier of `P_A`
   is the real indicator of the symmetric set `A`, so `P_A = P_A^*`").
2. `owner_rooted_positive_support_localization_v1.md` Lemma 2.1 (proof,
   L131-138) reuses self-adjointness of the **same, unmodified** `A`
   inherited from the parent note — no new band is constructed there, so
   the hypothesis carries over unchanged.
3. `secant_annihilator_localization_v1.md` restates `A=-A` explicitly at
   the top (L14-18) before reusing it in Sec 2's positive-subpacket lemma
   (L119-121, "self-adjointness of `P_A`... give[s]...").
4. The **one** place a genuinely new band is built is Sec 4's `A'`
   (L312-320): `A' = union` over `J`, and the note explicitly closes `J`
   under negation first ("Let `J` consist of these three restrictions **and
   their negatives**"), so `A'` is symmetric by construction, independent
   of whether the individual classes `A_chi` are. I confirmed
   `verify_secant_annihilator_localization_v1.py`'s own code enforces this
   (`selected_keys |= {(-key) % h for key in tuple(selected_keys)}`,
   L131) rather than merely asserting it in prose.
5. The individual restriction classes `A_chi = A cap r^{-1}(chi)` (L275-286)
   are **not** claimed symmetric on their own, and I checked the note never
   treats them as such: the operator applied to a single class is `Q_chi`
   (eq 4.10, L324-336), whose only properties used are contractivity
   (`||Q_chi h||_q <= ||h||_q`, an isometry-of-translation argument, L332-337)
   and an exact Fourier-orthogonality identity
   (`Q_{chi_q} P_{A'} b = P_{A_{chi_q}} b`, L340-344) — never
   self-adjointness of `P_{A_chi}` alone. So the asymmetry of the individual
   `A_chi` is never a problem because self-adjointness is never asked of
   them.

**Verdict: NO ISSUE.** The symmetric-band hypothesis is stated once,
explicitly, at the start of every note that needs it, is never silently
dropped, and the one place a new band is built, it is proved symmetric by
construction (and the construction is what the shipped verifier's code
actually enforces, not just what the prose claims).

---

## Attack C — slope rooting (Props 3.1/3.2) hidden hypotheses

**Prop 3.1 (fixed-support slope uniqueness, dense-band L198-221).**
Re-derived by hand: given `z != z'` (given) and `a >= k+1` (stated
immediately above, L175 area — "Assume `a>=k+1`"), the subtraction
`v|_S = (h_z-h_{z'})/(z-z')|_S` is well-defined because `F` is a field and
`z-z' != 0` is invertible; `h_z, h_{z'}` both have degree `<k` so their
difference does too. Back-substitution gives the same for `u|_S`. No
distinctness hypothesis is used beyond the two that are explicitly given
(`z != z'`, `a >= k+1`, the latter making "degree-`<k` restriction" a
nontrivial condition on an `a`-point set rather than a vacuous one). This
proof is airtight.

**Prop 3.2 (lossless rooting, L238-261) — the actual finding.** The
partition identity `W_+ = sum_z W_z` requires the owner map
`o: Omega^circ -> Z` to be a genuine (total, single-valued) function on
`Omega^circ`, which requires every support in `Omega^circ` at this point to
be *not* common-line (Prop 3.1 only rules out multi-ownership for
non-common-line supports). The note handles this correctly by construction:
"After removing common-line supports, let `o: Omega^circ -> Z` be the
unique owner map" (L223-224) redefines `Omega^circ`, from this point in the
note onward, as the common-line-free residual. That much is fine — it is
exactly why the note's own "Purpose" list (L13-21) enumerates "unique
noncommon slope ownership roots its positive mass" as one sequential step
in a pipeline, and the shipped verifier's `enumerate_line` explicitly
excludes `common` supports before computing `exact_owner` and the
`retained` rim-packing family (script L274-296: `exact_supports` is built
with `support not in common`).

The gap is one level up: **Theorem 4.2's own hypothesis list** ("Assume the
semantic compiler has removed: (i) every strict-excess/saturation packet...;
(ii) every repeated cross-slope rim...", L301-306) never explicitly
restates "no common-line supports remain," even though its proof's
same-owner case ("If their owner is the same slope...", L339) presupposes
both `S` and `S'` have a well-defined single owner — which is exactly the
fact established one section earlier and never re-cited here. Concretely: a
common-line support is a witness at *every* slope `z in F` simultaneously
(since `U_z|_S = u|_S + z*v|_S` is a degree-`<k` restriction for every `z`
once both `u|_S` and `v|_S` are), so if one were left inside `Omega^circ` at
the point Theorem 4.2 is invoked, the proof's two-case dichotomy ("distinct
owners" / "same owner") does not obviously cover it, since it does not have
a single owner to fall into either case.

I could not construct an actual counterexample to the *bound* (15) itself —
every downstream use (the verifier, Section 6's replayed construction, the
secant-annihilator chain) is internally consistent with reading `Omega^circ`
as already common-line-free by the time Theorem 4.2 is applied, matching
the note's declared pipeline order. This is a hypothesis-visibility gap, not
a broken instance: the fact used by the proof is true throughout by
construction, it is just not repeated at the point where the proof needs it.

**Verdict: NO ISSUE** (the bound (15) is correct under the note's own
pipeline convention), **with a FIXED-proposal**: add "no common-line
supports remain in `Omega^circ`" as an explicit third hypothesis bullet to
Theorem 4.2 (dense-band L301-306), or a one-line forward reference to L223's
redefinition. This is the same house rule the packet's own companion notes
apply to *others* ("A statement carries every hypothesis its proof uses" —
this is the one place the packet does not quite apply that standard to
itself.)

---

## Attack D — rim packing (Thm 4.2): double-counting direction and field-size dependence

**Double-counting direction.** Re-derived independently: each `S in
Omega^circ` contributes exactly `a` rims (`(a-1)`-subsets of an `a`-set);
global rim-disjointness (proved via the two-case argument, modulo the
Attack-C hypothesis-visibility point above) means the map `S -> {rims of
S}` has pairwise-disjoint images, so summing `a` once per support and
comparing against the total number of available rims `C(N,a-1)` in the
ambient coordinate set is a valid injective counting argument, not reversed
(`a*|Omega^circ| <= C(N,a-1)`, matching L320-329 exactly, `(1/a)*C(N,a-1) =
C(N,a)/(N-a+1)` verified by the standard binomial identity
`C(N,a-1)/C(N,a) = a/(N-a+1)`).

**Field-size dependence.** The bound (15) is purely combinatorial in `N`
(ambient coordinate/domain size) and `a` (support size); it never contains
`|F|` or the field characteristic. The only place field arithmetic enters
the *proof* is the interpolation-uniqueness fact "two degree-`<k`
polynomials agreeing on `>= k` points are identical," which needs the
shared points to be distinct field elements — automatic since `S, S'
subseteq D subseteq F` are genuine point sets, and needs no bound on `|F|`
beyond `|F| >= N` (implicit from `D subseteq F`, `|D|=N`). I checked the
edge case `a=N` (`N-a+1=1`, no division issue) and confirmed `a<=N` is
forced automatically since `S subseteq D`, `|S|=a`, `|D|=N`. **No hidden
`|F|`-dependent constant found.**

**Shared finding.** Theorem 4.2's proof does rely on the Attack-C
hypothesis-visibility point (common-line exclusion); see Attack C for the
exact location and proposed one-line fix. That is a hypothesis-listing gap,
not a double-counting or field-size error.

**Verdict: NO ISSUE.**

---

## Attack E — projected-energy gate (Thm 8.1) one-way misuse

**Claim under test.** `R_A^q <= Y_A` (eq 32, dense-band L575) is one-way;
does any downstream statement quietly use the reverse (`Y_A` large `=>`
`R_A` large)?

I traced every use of `Y_A`/`R_A` together across all three target notes
plus the two companion notes (`primitive_signed_payment_barrier_v1.md`,
`arbitrary_mask_idempotent_guardrail_v1.md`) that the dense-band note cites
by name in Sections 9-10:

- Thm 8.1 point 2 (L586-593): `Y_A <= e^{eps*Nq}` `=>` `R_A <= e^{eps*N}` —
  the *q*-th root of the TRUE direction `R_A^q <= Y_A`. Correct.
- Thm 8.1 point 3 (L595-607): `R_A >= e^{eta N}` `=>` `Y_A >= e^{eta Nq}` —
  raises the *hypothesis* to the `q`-th power and chains through the TRUE
  direction `Y_A >= R_A^q`. This is "`R_A` large forces `Y_A` large," never
  the reverse. Correct.
- `owner_rooted_positive_support_localization_v1.md` **opens** with a
  section (Sec 1, L32-58) whose entire purpose is to flag exactly this
  failure mode in the abstract ("high `Y_A` does not imply high `R_A`. ...
  The high-load inequality is a derived tag, not a replacement for (1.1)"),
  then *proves* `R_A(b) >= R_A(f)` directly from Lemma 2.1 (eq 2.2, never
  inferring it from `Y_A(b)`).
- `secant_annihilator_localization_v1.md` derives `R_A'(b) >= R_A(b)/d` (eq
  4.13, L360-367) via a **direct** Minkowski/averaging argument on the
  `q`-norm itself (Sec 4.1), and `Y_A'(b) >= Y_A(b)/d^{q-1}` (eq 4.15,
  L390-397) via a **separate** direct averaging argument on energy and
  density (Sec 4.2) — the two lower bounds are proved independently of one
  another, so there is no place a large `Y_A'` is used to infer a large
  `R_A'`.
- `primitive_signed_payment_barrier_v1.md` Sec 6, Prop 6.1 explicitly says
  the derived bound "does **not** imply `Y_{B_i} >= e^{-o(Nq)} Y_A`, because
  [the packet] only prove[s] `R_A^q <= Y_A` in the opposite direction"
  (L536-539) — the companion note states the guard verbatim.
- `arbitrary_mask_idempotent_guardrail_v1.md` Sec 6 repeats the same guard
  ("Retained q-excess gives only `Y_{B_i} >= R_{B_i}^q >= ...`; it does not
  imply relative retention of the original `Y_A`," L180-188).

**Verdict: NO ISSUE.** Every use of the gate in all five notes I read for
this attack goes in the true direction, and two of the five notes state the
one-way warning verbatim as a standing guard rather than merely respecting
it silently.

---

## Attack F — Section 6 counterexample replay

Independently reimplemented (fresh code, not the shipped verifier) the
construction at dense-band L406-480: `B` even, `N=2B`, `a=B`, `A_i = Q^i`
(`Q=5`), `C = 2*sum(A_i)+1` (the minimal valid odd `C > 2*sum(A_i)`),
`T = {A_i, C-A_i}`, full slice, `Phi(S) = sum(S)`, heavy fiber at
`s_0 = B*C/2`.

```text
B=2: N=4  M=6    L=5   (exp 5,   ok) W=2  (exp 2,  ok) max_int=0<=a-2=0  planted=True
B=4: N=8  M=70   L=41  (exp 41,  ok) W=6  (exp 6,  ok) max_int=2<=a-2=2  planted=True
B=6: N=12 M=924  L=365 (exp 365, ok) W=20 (exp 20, ok) max_int=4<=a-2=4  planted=True
```

`L=(3^B+1)/2` (eq 20) and `W=C(B,B/2)` (eq 21) reproduce exactly for all
three `B`; the heavy fiber's pairwise intersections are exactly `<= a-2`
(eq 22, the global `(a-1)`-rim-packing property), and the planted relation
`A_i + (C-A_i) = C` (eq 25) holds for every `i`. The asymptotic rate
`(1/N)*log(W*L/M)` trends toward `log(3/2)/2 approx 0.2027` as `B` grows
(`0.128, 0.157, 0.172, 0.180` for `B=2,4,6,8`), consistent with the note's
claimed `exp(B*log(3/2)+O(log B))` (eq 23) — the visible finite-`B` gap is
exactly the declared `O(log B)` correction, shrinking as `B` grows, not a
discrepancy.

**Verdict: NO ISSUE.** The construction, its two formulas, the rim-packing
property, and the planted-relation certificate all reproduce exactly under
an independent implementation.

---

## Attack G — Prop 4.1 regression and guardrail-script replay

**On "F_7."** The assigned brief names an "F_7 regression" for Prop 4.1.
The actual field used by `verify_owner_rooted_dense_band_localization_v1.py`'s
`incidence_regression` (which replays dense-band Prop 4.1, "saturation
packet equivalence," L283-299) is `p=17`, with an 8-point domain
`list(range(1,9))`. I checked why: the domain values `1..8` must be
*distinct field elements*; at `p=7`, `8 mod 7 = 1 = 1 mod 7`, so points `1`
and `8` collide and the construction is not even well-formed (verified
directly: `[x % 7 for x in range(1,9)] = [1,2,3,4,5,6,0,1]`, not distinct;
the smallest prime that keeps all 8 points distinct is `p=11`). So `F_7` is
combinatorially infeasible for this exact regression, and the shipped
choice of `p=17` is a valid (if not minimal) substitute. The most likely
source of the "`F_7`" label is `secant_annihilator_localization_v1.md`'s
own guardrail regression (`paired_planted_regression` in
`verify_secant_annihilator_localization_v1.py`), which uses an integer
parameter named `qbase=7` (superincreasing base `7^i`, **not** a field) —
I replayed that one too, independently, and it is a plausible paraphrase
source given the shared numeral.

**Prop 4.1 replay (`p=17`, dense-band L283-299).** Re-ran
`verify_owner_rooted_dense_band_localization_v1.py --check`: reproduces the
tracked certificate `experimental/data/certificates/owner-rooted-dense-band-v1/owner_rooted_dense_band_v1.json`
byte-for-byte (`payload_sha256=521718304111fd22c3ede51a876376715a19531209b78e06f36fcfbeca22bf9e`,
`artifact_check=PASS`). The forward direction (saturation `=>` all
sub-witnesses) and converse (all sub-witnesses at one slope `=>` one
polynomial) both instantiate on the constructed line
(`witness_record_count=5`, `exact_support_count=5`,
`saturation_packets_complete=True`, `global_rims_unique=True`,
`packing_bound: 20<=56`).

**Guardrail-script replay.** Independently reimplemented (fresh code):

- The Section 6 rim-free guardrail (`paired_rim_free_regression`) — see
  Attack F; reproduces exactly.
- The secant-annihilator planted-trade guardrail
  (`paired_planted_regression`, `qbase=7`) — reproduced independently for
  `b_pairs in {4,6,8}`; at `b_pairs=8` (the shipped default) I obtain
  `n=70` supports, a single common sum, global `<=a-2` rim packing, heaviest
  trade layer at radius `r*=4` with `36` incidences (matching the shipped
  certificate's `rooted_trade_incidences=36`, `fixed_trade_radius=4` exactly),
  and every trade in that layer exactly balanced
  (`sum(S_0\S) == sum(S\S_0)`).
- `verify_owner_rooted_positive_support_localization_v1.py`'s rooted
  example on `Z/13` reproduces its printed numbers exactly across
  `q in {4,6,8}` (spot-checked directly against the module's own
  `check_rooted_localization`).

**Verdict: NO ISSUE.** Every regression and guardrail construction I could
locate under the three target notes reproduces exactly; the field is `F_17`
(not `F_7`), for the concrete, checkable reason above.

---

## Interfaces

- **avdeevvadim** authored all three audited packets and the two companion
  notes read for context (`primitive_signed_payment_barrier_v1.md`,
  `arbitrary_mask_idempotent_guardrail_v1.md`), all integrated together at
  `c23dcaa`. The machinery is careful and, aside from the one local
  normalization gap in Attack A and the hypothesis-listing note in
  Attack C/D, holds up exactly as printed under adversarial replay — six of
  seven attacks are clean, and two of the companion notes independently
  restate the Attack-E one-way guard verbatim, which is good practice this
  audit is glad to confirm rather than have to invent.
- `heavy_fiber_admissibility_transfer.md` (in-tree at c23dcaa, reported as
  #717) consumes this packet directly: it discharges the "Heavy-fiber
  interface" item from dense-band Sec 10's open list, quoting `R_A`, `L`,
  `M` with the exact same normalization audited clean in Attack A, and its
  own Sec 2 sharpening (`Lemma 2.1`, whole-residual band-failure transfer)
  is consistent with everything checked here.
- **#723** and **#728** are reported (not present on this tree at c23dcaa,
  so not independently audited here) to extend the machinery further: a
  two-regime clause census on the four admissibility clauses from
  `primitive_signed_payment_barrier_v1.md` Sec 8, and a signed band-excess
  threshold theorem pair on the Section 6 superincreasing family. Both
  consume the same `R_A`/`Y_A`/`M`/`L` objects audited here; neither
  touches the Attack A gap (eq 5.6 is local to
  `owner_rooted_positive_support_localization_v1.md` and is not part of the
  admissibility-clause or superincreasing-family machinery they build on).

## Nonclaims

This audit does not prove or refute `A4`, primitive `Q`, the Proximity
Prize theorem, source-algebraic emission, the charge-preserving
semantic-or-signed dichotomy, or any claim the audited notes themselves
mark open (dense-band Sec 10; positive-support Sec 4-6;
secant-annihilator Sec 6-7). It checks the seven assigned failure modes
against the three named packets only; it does not re-audit
`primitive_signed_payment_barrier_v1.md` or
`arbitrary_mask_idempotent_guardrail_v1.md` beyond confirming the dense-band
note's own characterization of them (Sec 9-10) is accurate, since those two
notes are read here for context, not as primary targets.
