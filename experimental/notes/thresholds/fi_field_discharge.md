# (FI-field) reduces to the ambient-field hypothesis; discharged on the prize's poly-field class

## Status

`RECEIVED-LINE CERTIFICATE REDUCED TO AMBIENT-FIELD HYPOTHESIS (PROVED,
unconditional) / DISCHARGED ON THE POLY-FIELD CLASS log|F_n|=o(n) (PROVED) /
NOT IMPLIED BY (A1)-(A7) ALONE (AUDIT, verbatim) / NO ADMISSIBLE PRIZE-RELEVANT
Theta(n)-FIELD WITNESS EXISTS -- every Theta(n)-field construction dilutes below
any fixed target (COMPUTED) / RESIDUAL corner COMPUTED-empty not PROVED-empty`.

This packet **decides** the single open link that our **PR #642**
(`c7_collapse_image_degree.md`, read first) named: does the frontiers paper's
ledger-admissibility `(A1)`--`(A7)` (`def:admissible-sequence`, tex L895--954) or
the Proximity-Prize reserve **already** imply

> **(FI-field).** the C7 effective-image rank-collapse cell's received line is
> confined to a scalar subextension `F'` with `log|F'_n| = o(n)`.

**One-line verdict (PARTIAL, sharp reduction).** *Neither `(A1)`--`(A7)` nor the
target reserve bounds the ambient field `|F_n|`, so neither implies `(FI-field)`
on its own. But the prize's own full-field normalization does the work: subfield
confinement, written in normalized form, gives `e_{MCA}(r) = delta(r)/|F| <=
|F_r|/|F|`, so any **prize-relevant** line (one the target charges,
`e_{MCA}(r) > eps`) has `log|F_r| >= log|F| - log(1/eps)` -- its field of
definition is within `log(1/eps)=128` bits of the ambient field. Therefore
`(FI-field)` for prize-relevant lines is **equivalent** to the ambient-field
hypothesis `log|F_n| = o(n)`, which (i) is the "field hypothesis" the paper's own
scope remark already names (`rem:intro-countertheorem-scope`, L836--840), (ii)
holds for the prize's poly-size smooth-domain rows -- on which the span face
closes **unconditionally** -- and (iii) is violated only by the countertheorem's
scalar extension, whose `log|F| = Theta(n)` construction is diluted to
`e_{MCA} = e^{-Theta(n)} << eps` and is therefore admissible but **not**
prize-relevant. The correct printed input is thus the ambient-field hypothesis
`(FI-field')`, strictly weaker than #642's received-line certificate, and it
belongs in `def:admissible-sequence`, not the C7 paragraph.*

Every number below is recomputed by
`experimental/scripts/verify_fi_field_discharge.py` (stdlib-only, zero-arg,
`RESULT: PASS (59/59)`, ~0.43 s, 13 MB, well under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **COMPUTED** (exact finite
recomputation of a promoted/witness quantity), **MEASURED** (exact finite toy),
**AUDIT** (verbatim interface reading of the tex), **OPEN**.

**Credit.** The field-of-definition law `delta <= |F_r|` (T-FIELD), the
GF(p^d)/antipodal census machinery, and the isolation of `(FI-field)` are our
**#642** (`c7_collapse_image_degree.md`); the collapse-payment arc is
**#635**/**#636**/**#627**/**#625**; the `(S_E)`-vs-admissibility per-condition
walk is our **#622** (`se_on_admissible_leaves.md`, consumed for the `(A1)`--`(A7)`
anchors). The forcing witnesses are **THE PAPER'S OWN** promoted countertheorem
(`thm:intro-countertheorem`, L796--819; eq (4.5) L2077; eq (6.7)/(6.8) L4060--72),
which we only cite and recompute; **Codex #634** (antipodal orientation floor,
separating pole over a scalar extension) and **DannyExperiments #631**
(profilewise separating-pole realization, unbounded extension) are its two
instances; **DannyExperiments #621** is its confined base-field extreme. Codex
**#624**'s Lean of eq (13.3) composition and the challenge-intersection statements
are consumed as the quantifier anchor. No finite M31/KoalaBear survivor count,
adjacent inequality, or target threshold is touched.

---

## HEADLINE (read first): the certificate is on the wrong object

#642 pinned `(FI-field)` as a bound on the **received line's field of definition**
`F_r`. That is sharper than the problem needs. In the prize's normalization the
per-line count enters divided by the ambient field, and subfield confinement
`delta(r) <= |F_r|` (T-FIELD, #642) becomes, verbatim in normalized form,

```
   e_{MCA}(r) = delta(r)/|F|  <=  |F_r|/|F|  =  1 / (|F|/|F_r|).        (RED)
```

`(RED)` is not new content -- it is `thm:subfield-confinement-full` (tex
L1930--1934) with both sides divided by `|F| = |Gamma|`. Its consequence is the
whole packet:

```
   e_{MCA}(r) > eps   ==>   |F|/|F_r| < 1/eps   ==>   log|F_r| > log|F| - log(1/eps).
```

So a line the target actually charges has its field of definition **within
`log(1/eps) = 128` bits of the ambient field** -- there is no room for a
"confined subextension" unless the **ambient** field is already small. The
received-line certificate collapses onto the ambient-field size:

```
   (FI-field) on prize-relevant lines   <==>   log|F_n| = o(n)   =: (FI-field').
```

The three columns of the dichotomy, now decided:

| regime | `log|F_n|` | prize-relevant line? | span face | mechanism |
|--------|-----------|---------------------|-----------|-----------|
| poly-field (**the prize**) | `o(n)` | possible | **closes** (PROVED) | `delta <= |F_r| <= |F_n| = e^{o(n)}` |
| exp-field, countertheorem | `Theta(n)` | **no** -- diluted `e_{MCA}=e^{-Theta(n)}` | closes | full-field normalization |
| exp-field, hypothetical | `Theta(n)` | would need `delta ~ |F|` over `|F|~N` | OPEN corner | foreclosed by the `binom(N,2)` separation gate (COMPUTED, not PROVED) |

`(A1)`--`(A7)` place a row in **column 1 or 2 indifferently** (they never bound
`|F_n|`); the prize's poly-size domains place it in **column 1**, where
`(FI-field')` is automatic.

---

## Rung 1 -- EXTRACT (AUDIT, verbatim)

### 1a. The admissibility ledger `(A1)`--`(A7)` (`def:admissible-sequence`, L895--954)

Preamble, L897--899, verbatim:

> "A sequence `(C_n,a_n)`, with `C_n = RS_{F_n}(D_n,k_n)`, is ledger-admissible if
> the following conditions hold **uniformly in every received line**."

The seven conditions, quoting the field-relevant clauses:

- **(A1)** L901--904: "The domains are among the structured classes ... and the
  folding maps have complete uniform fibers." *(constrains domains, not `|F_n|`.)*
- **(A2)** L905--907: "A first-match atlas covers every bad-slope witness and has
  `e^{o(n)}` profiles. **The total distinct-slope contribution of its algebraic
  cells is at most `e^{o(n)} E_n(a_n)`.**" *(This is exactly the distinct-slope
  budget `(FI-field)` feeds; it is a HYPOTHESIS, not derived. No field bound.)*
- **(A3)** L912--923: image normalization; density `m_N/N in [alpha,1-alpha]`;
  `log L_N/q_N = o(N)` with `q_N <= (log N)^C`; "Any use of the ambient scale is
  accompanied by `(FI)`." *(`q_N` is a logarithmic order, not `|F_n|`.)*
- **(A4)** L924--934: `(MI)+(MA)` on the effective span, or an image-normalized
  Sidon payment. *(no field bound.)*
- **(A5)** L935--941: "Every use of power-sum coordinates satisfies
  `R_N < char B_N`." *(a depth-vs-characteristic bound, not `|F_n|`.)*
- **(A6)** L942--945: `(RC)` on shift-pair/balanced-core, or a direct
  distinct-slope bound. *(no field bound.)*
- **(A7)** L946--952: "The profile envelope ... including all quotient subfields
  `B_phi` ... **and all profile fields of definition**, is used in the final
  budget." *(records the profile field of definition in the envelope; it does not
  bound the received line's or the ambient field's size.)*

**AUDIT verdict.** **None of `(A1)`--`(A7)` bounds `|F_n|`.** (A2) is the clause
that would need the distinct-slope budget; (A7) merely records fields of
definition in the sum. The ambient field size is nowhere constrained.
[verify BLOCK 6 exhibits an admissible poly-field row and the exp-field boundary.]

### 1b. The reserve (`rem`/`lem:safe-side`, L6135--6144; L1056--1057)

> L6135--6138: "A **target reserve** is the explicit bit slack in one of the two
> comparisons: on the safe side it is the amount by which `log_2 B_n^*` exceeds
> `ell_n + log_2 E_n(a)`, and on the unsafe side ... the amount by which the
> logarithm of a proved bad-slope construction exceeds `log_2 B_n^*`."

The reserve is a **bit margin** between the envelope/numerator and the target
`B_n^* = floor(eps|Gamma_n|)`. It does not bound `|F_n|` either. AUDIT: the
"field hypothesis" and the "reserve hypothesis" the scope remark couples are
**distinct**; `(FI-field)` maps to the field one.

### 1c. The countertheorem scope remark (`rem:intro-countertheorem-scope`, L829--841, verbatim)

> "Here `w_n/n = Theta(1/log n) = o(1)`. The countertheorem therefore refutes
> ambient identity-normalized Sidon payment, identity-only numerator bounds, and
> *row-sharp* threshold derivations ... but it does not by itself refute a coarse
> radius identity with an `o(1)` error. **The domain field `B_n` is
> polynomial-size, whereas the scalar extension used to separate all
> exponentially many slopes has `log|F_n| = Theta(n)`. A claim for a prescribed
> Proximity-Prize target must still use the exact target-aware bracket and verify
> its field and reserve hypotheses.**"

This is the paper **naming the exact gap** and distinguishing poly-size `B_n` from
the countertheorem's `log|F_n| = Theta(n)`. Our reduction shows the missing
"field hypothesis" is precisely `(FI-field') : log|F_n| = o(n)`.

### 1d. The countertheorem separation gate (eq (4.5), `thm:prefix-to-line-hardness`, L2073--2084, verbatim)

> "Let `G ⊆ Phi_w^{-1}(z)` be a fiber of `N` many `m`-sets, with `0<=w<=m-2`, and
> put `k=m-w-1`. Every finite extension `F/B` satisfying `|F| - n > k binom(N,2)`
> admits one received line for `RS_F(D,k)` with at least `N` distinct MCA-bad
> slopes furnished by `G`."

Realizing `N` distinct slopes on one line uses `|F| > n + k binom(N,2) ~ k N^2/2`.
Eq (6.7)/(6.8) (L4060--4072) instantiate the smooth-quotient case with
`N = exp((h(alpha)/4)n)` and, verbatim, "Such extensions exist with degree
`[F:B] = O(n/log n)`" -- i.e. `log|F| = Theta(n)`. [verify BLOCK 5.]

---

## Rung 2 -- THE SHARP FIRST CHECK: are the Theta(n)-witnesses prize-relevant?

`(RED)` reduces the question to one arithmetic fact per witness: is the size ratio
`|F|/|F_r|` bounded (`< 1/eps`, prize-relevant) or unbounded (diluted)? All three
known `Theta(n)`-field witnesses are **admissible-or-nearly** but **not
prize-relevant**, because each pays a `binom(N,2)` separation cost in the field.

**(a) The paper's own countertheorem (eq (4.5)/(6.7)).** `N` distinct slopes need
`|F| > k binom(N,2) ~ N^2`, while subfield confinement gives `|F_r| >= N` and the
bijection `P |-> P(alpha)` (`thm:exact-list-line-bijection`, L2104--2112) puts the
slopes in `F_r = B(alpha)` with `|F_r| ~ N`. Hence

```
   size ratio |F|/|F_r| ~ N^2 / N = N = exp(Theta(n))   (UNBOUNDED),
   e_{MCA} = delta/|F| ~ N / N^2 = 1/N = e^{-Theta(n)}  << eps.
```

**Admissible but NOT prize-relevant** -- it never charges the target.
[verify BLOCK 3: `e_{MCA} = N/|F|` strictly decreasing, `< 2^{-128}` at `N=2^200`;
BLOCK 5: `log(|F|/|F_r|)/n = 0.1733 = Theta(1)` at `n in {1e4,1e6,1e8}`.]

**(b) Codex #634 (antipodal orientation floor).** `J_z >= ceil(2^a/q^{w/2})`
distinct exact-agreement slopes at a separating pole `alpha in F setminus B`. To
separate `J_z` slopes the pole line again lives over a scalar extension with
`|F| >= Q_sep(J_z) ~ binom(J_z,2)` (same gate; #634's own text: "The separating
pole line necessarily lives over `F`"). Same conclusion: `|F|/|F_r| = e^{Theta(n)}`,
diluted. [BLOCK 0 reproduces #634's base-field corollary `delta(alpha=0)=2` and
the `F_{p^2}` re-expansion column `{8,32,63}` byte-for-byte with #642.]

**(c) DannyExperiments #631 (profilewise separating pole).** One line carries
`H_phi(lambda) = e^{Theta(n)}` slopes over an **unbounded** extension
`|F| > n + k binom(L_z,2)` -- #631's own field bound is the eq (4.5) gate with
`N = L_z`. `[F:B] = Theta(n/log|B|)`, `|F|/|F_r| = e^{Theta(n)}`, diluted.

**No admissible prize-relevant `Theta(n)`-field witness exists.** Every known one
pays `binom(N,2)` in the ambient field, and `(RED)` converts that into
`e_{MCA} = e^{-Theta(n)}`. There is **no REFUTED witness** for the full-field
prize. [This is the COMPUTED half of the verdict; its converse -- that no
construction can beat the `binom(N,2)` gate -- is Rung 5's OPEN corner.]

---

## Rung 3 -- THE QUANTIFIER TRACE (AUDIT, verbatim -- this lane lives or dies here)

**Who chooses the received line, over what field?** L187--188, verbatim:

> "A received pair `r = (r_0,r_1) in (F^D)^2` determines the received line
> `{r_0 + gamma r_1 : gamma in F}`."

The received words are `F`-valued (over the **ambient** field, not forced to `B`),
and L226--227:

> "Every claimed upper bound is uniform over received pairs, whereas a lower
> construction need only exhibit the stated received pair."

So the **adversary (lower construction) picks the pair**, hence picks the field of
definition `F_r ⊆ F`. The slope ranges over the challenge set, L204 + L575--577:

> L204: "`∅ ≠ Gamma ⊆ F` is the **challenge set**, meaning the set of slopes
> allowed in the test."
> L575--577: "the code and challenge field `F` may be a **scalar extension**,
> meaning that the same evaluation points are retained while polynomial
> coefficients and slopes are allowed in a larger field `F ⊇ B`."

So `gamma` ranges over `Gamma ⊆ F` **including** `F setminus B`: the adversary is
**free** to use extension-valued lines. Confinement to `B` is **not** definitional
-- `thm:subfield-confinement-full` confines only a "`B`-valued received line"
(L1933--1934), a hypothesis the adversary need not satisfy.

**The verifier's normalization is what constrains it.** L213--221, verbatim:

> "For the standard full-field challenge we abbreviate
> `e_{MCA}(C,1-a/n) = B_C^{MCA}(a)/|F|` ... Taking `Gamma = F` ... gives exactly
> this customary formulation."

and the prize (L489--492): "MCA error at most a cryptographic target such as
`2^{-128}`" is exactly `e_{MCA} = B^{MCA}/|F| <= eps`. **The prize is the
full-field challenge.** The denominator `|F|` is fixed by the protocol, not chosen
by the adversary. Combining the free numerator field `F_r` with the fixed
denominator `|F|` is `(RED)`: the adversary may range over `F`, but to make
`delta/|F| > eps` the free `F_r` must fill up `F` to within `log(1/eps)` bits.

**Proper challenge subsets.** L1047--1049, verbatim:

> "For a proper challenge subset the exact bracket remains valid, but this
> corollary additionally requires a certified challenge-intersection lower bound;
> `|Gamma_n|` alone does not determine it."

The exact challenge-intersection is the averaging identity in the proof of the
exact unsafe test (`prop:simple-pole-lower`, eq (13.3)), L6204--6206, verbatim:

> "Replacing a line `(r_0,r_1)` by `(r_0 + delta r_1, r_1)` translates `Z` by
> `-delta`. **Averaging over `delta in F_n` gives `|Z||Gamma_n|/q_n` challenge
> slopes**, so some translate has at least the outer-ceiling number."

So a proper subset scales the per-line count by `|Gamma|/q`; the leading
`e_{MCA}` comparison `delta/q > eps` is **the same** as full-field, and the
residual `|Gamma|`-alignment subtlety is the only place `(FI-field)`/a
challenge-intersection theorem could still be load-bearing (Rung 5). [BLOCK 4
verifies `avg_delta |Z ∩ (Gamma - delta)| = |Z||Gamma|/q` exactly over
`GF(7),GF(9),GF(5)`.]

**field of definition**, L2290--2292 verbatim: "The field of definition is the
smallest recorded subfield over which these parameter spaces, equations, and maps
are defined." -- confirms `F_r ⊆ F` is the object `(RED)` bounds.

---

## Rung 4 -- TOY CENSUS (MEASURED, verifier-recomputed)

Exact `GF(p^d)` instantiation; every value is a genuine finite-field computation
(irreducible modulus via a Rabin test; degrees via the Frobenius orbit).

- **BLOCK 0 (subfield confinement census, reproduces #642):** `delta(alpha=0)=2`
  for `p in {7,11,13}` (product parity, = #634's base-field corollary);
  `F_{p^2}` pole max-delta `= {8,32,63}` byte-identical to #642's table; and
  `delta <= |F_r|` for **all** `169`/`121`/`289` poles (subfield confinement).
- **BLOCK 1 (eq (4.5) gate):** for `p=7`, `N=8`, `k=a=3`, `n=6`, the paper's
  sufficient `|F| > n + k binom(N,2) = 90`; separation of all `8` slopes occurs
  already at `|F_r| = 49 < 90` (**the quadratic gate is SUFFICIENT, not
  NECESSARY** -- the honest corner) while `|F_r| >= N = 8` is necessary (subfield).
- **BLOCK 2 (the reduction, core):** over `GF(5^3)`, `delta <= |F_r|` and
  `delta*(|F|/|F_r|) <= |F|` for all `121` poles; and the synthetic fully-bad
  subfield line `Z=F_r` over `GF(2^6)` makes `(RED)` an **equality**
  `e_{MCA} = 1/(|F|/|F_r|)`, so `eps=1/8` selects **exactly** the size-ratio-`1`
  line and excludes ratios `{8,16,32}` -- prize-relevance forces `|F|/|F_r| < 8`.
- **BLOCK 3 (dilution):** `e_{MCA} = N/|F|` for the countertheorem decreases
  `2.5e-3 -> 1.6e-4` over `N in {4..128}`; `< 2^{-128}` exactly at `N=2^200`.
- **BLOCK 4 (challenge-intersection):** `avg |Z ∩ (Gamma-delta)| = |Z||Gamma|/q`
  exactly (eq (13.3) proof) over three fields.
- **BLOCK 5 (countertheorem degrees):** `[F_r:B] = Theta(n/log n)` (ratio stable),
  `log|F_r|/n = 0.1733` (`(FI-field)` FAILS), `log(|F|/|F_r|)/n = 0.1733`
  (size ratio UNBOUNDED, not prize-relevant), for `n in {1e4,1e6,1e8}`.
- **BLOCK 6 (dichotomy):** an admissible poly-field row `GF(11^2)` has every line
  confined `delta <= |F|`; the exp-field boundary needs `log|F_r| >= cn - 128 =
  Theta(n)` for `c in {0.1,0.3,0.7}` at `n=1e6`, i.e. `(FI-field)` can hold only
  as `c -> 0` -- the boundary IS `log|F_n| = o(n)`.

---

## Rung 5 -- VERDICT + paste-ready ledger entry

**Verdict = PARTIAL, with an unconditional reduction.**

- **PROVED (unconditional reduction, `(RED)`):** on every prize-relevant received
  line (`e_{MCA}(r) = delta(r)/|F| > eps`), subfield confinement forces
  `log|F_r| >= log|F| - log(1/eps)`. Hence `(FI-field)` for prize-relevant lines
  is equivalent to the ambient-field hypothesis `(FI-field') : log|F_n| = o(n)`.
- **PROVED (discharge on the poly-field class):** if `log|F_n| = o(n)` -- the
  prize's poly-size smooth-domain regime -- then `delta(r) <= |F_r| <= |F_n| =
  e^{o(n)}` for every line by subfield confinement, and the span face closes
  **unconditionally** on the product/profile class. The C7 collapse cell pays.
- **AUDIT (negative -- admissibility insufficient):** `(A1)`--`(A7)` never bound
  `|F_n|` (Rung 1a, verbatim), and the target reserve is a bit margin, not a field
  bound (Rung 1b). So admissibility/reserve **alone** do not imply `(FI-field)`;
  the ambient-field hypothesis is a genuinely separate input -- exactly the "field
  hypothesis" the scope remark names (L836--840).
- **COMPUTED (no REFUTED witness):** every known `Theta(n)`-field construction
  (countertheorem eq (4.5)/(6.7); Codex #634; DannyExperiments #631) pays the
  `binom(N,2)` separation gate, giving `|F|/|F_r| = e^{Theta(n)}` and
  `e_{MCA} = e^{-Theta(n)} << eps` -- admissible but not prize-relevant.
- **OPEN (the residual corner):** whether an admissible line can be simultaneously
  prize-relevant (`e_{MCA} > eps`) and have `log|F_r| = Theta(n)`. By `(RED)` this
  needs `log|F_n| = Theta(n)` **and** `delta ~ |F|` distinct slopes realized over
  `|F| ~ N` (linear, not `N^2`). The pairwise-separation gate (`binom(N,2)`
  collision conditions, eq (4.5)'s `k binom(N,2)`) forecloses it for every known
  construction, but that gate is proved **sufficient, not necessary** (BLOCK 1
  separates below it), so the corner is **COMPUTED-empty, not PROVED-empty**.

### The pinned minimal printed input (supersedes #642's (FI-field))

> **(FI-field').** *For the prize's smooth/circle row sequence the ambient
> challenge field satisfies `log|F_n| = o(n)` (equivalently
> `[F_n : B_n] = o(n/log|B_n|)`): the challenge is not taken over a scalar
> extension of superpolynomial degree.*

Under `(FI-field')`, every received line has `log|F_r| <= log|F_n| = o(n)`, so
`delta_lambda(r) <= |F_r| <= |F_n| = e^{o(n)}` by subfield confinement -- the
collapse cell pays and the span face closes. `(FI-field')` is **strictly weaker**
than #642's received-line `(FI-field)` (it is a single row-level field-size
condition, not a per-line certificate), and by `(RED)` it is **equivalent to it on
exactly the prize-relevant lines**. It is **necessary** (the countertheorem
violates it and, at fixed positive rate with an exponentially-small-enough target,
would furnish threshold counterexamples -- the scope remark's own caveat) and
**sufficient** (subfield confinement). Print it as a **field condition in
`def:admissible-sequence`** (a companion to (A1), or an explicit `(A0)` field
clause), **not** in the L2450 C7 paragraph: once the ambient field is
poly-size, the C7 cell needs no per-line certificate at all.

### Superseding ledger entry (extends #642's, for the maintainer)

*Discharging `(FI-field)` for the prize. #642 reduced the C7 collapse cell's
per-line degree to `delta_lambda(r) <= |F_r|` (T-FIELD, subfield confinement,
tex L1930--1934) and left one input: whether prize-relevance confines `F_r` to
`log|F_r| = o(n)`. It does, but via the ambient field, not a per-line certificate.
In the full-field normalization `e_{MCA}(r) = delta_lambda(r)/|F|`, subfield
confinement reads `e_{MCA}(r) <= |F_r|/|F|`, so any line the target charges
(`e_{MCA}(r) > eps`) has `log|F_r| >= log|F| - log(1/eps)`: its field of
definition sits within `log(1/eps)` bits of the ambient field. Hence `(FI-field)`
for prize-relevant lines is equivalent to the ambient-field hypothesis
`(FI-field') : log|F_n| = o(n)`, which the scope remark (`rem:intro-countertheorem-
scope`, L836--840) already names ("The domain field `B_n` is polynomial-size,
whereas the scalar extension ... has `log|F_n| = Theta(n)`") and which holds for
the prize's poly-size smooth domains. On that class `delta_lambda(r) <= |F_r| <=
|F_n| = e^{o(n)}` and the span face closes unconditionally. Admissibility
`(A1)`--`(A7)` does not by itself imply it -- no admissibility clause bounds
`|F_n|` -- so `(FI-field')` must be printed, superseding #642's per-line
`(FI-field)`: it is the strictly weaker row-level field condition
`log|F_n| = o(n)`, placed in `def:admissible-sequence`. The paper's own
countertheorem (eq (4.5), `|F| > n + k binom(N,2)`; eq (6.7)/(6.8),
`[F:B] = O(n/log n)`) shows necessity -- but that same `binom(N,2)` separation
cost makes it `e_{MCA} = e^{-Theta(n)} << eps`, so it is admissible yet not
prize-relevant, and there is no admissible prize-relevant witness with
`log|F_r| = Theta(n)`.*

### What closes if `(FI-field')` is printed

```
 span face on poly-field prize rows --THIS--> closes unconditionally
   (delta <= |F_r| <= |F_n| = e^{o(n)}, subfield confinement)
 (FI-field) received-line certificate --RED--> equals (FI-field') on prize lines
 (FI-field') : log|F_n| = o(n)        --scope remark L836-840--> already named
 countertheorem log|F|=Theta(n)       --binom(N,2) gate--> diluted, not prize-relevant
 proper challenge subset Gamma ⊊ F    --residual--> challenge-intersection (L1048)
```

### The 2-3 steps the PI should re-derive (esp. the quantifier)

1. **`(RED)` (the reduction).** Divide `thm:subfield-confinement-full`
   (`delta(r) <= |F_r|`) by `|F| = |Gamma|`: `e_{MCA}(r) <= |F_r|/|F|`. Then
   `e_{MCA}(r) > eps ==> |F|/|F_r| < 1/eps ==> log|F_r| > log|F| - log(1/eps)`.
   One line; the only content is reading `e_{MCA}` with the **full-field**
   denominator `|F|` fixed by the protocol.
2. **The quantifier (make-or-break).** The received pair is `(r_0,r_1) in (F^D)^2`
   (L187), adversary-chosen (L226), slopes over `Gamma = F` (L213--221) **including
   `F setminus B`** (L575--577); confinement to `B` is a hypothesis the adversary
   need not meet. So `F_r` is free in the numerator but `|F|` is fixed in the
   denominator -- that asymmetry is the whole discharge. Verify the prize is the
   full-field challenge (L489--492 vs L213--221) and that a proper subset only
   rescales by `|Gamma|/q` (L6204--6206), leaving the `delta/q > eps` comparison
   unchanged.
3. **Necessity is the paper's, dilution is the paper's.** The forcing witness is
   `thm:intro-countertheorem`/eq (4.5); its `|F| > n + k binom(N,2)` (L2077) is
   both what makes it work and what dilutes it (`e_{MCA} = N/|F| ~ 1/N`,
   BLOCK 3/5). Cross-check `[F:B] = O(n/log n)` (L4072) against `log(|F|/|F_r|)/n
   = 0.1733` (BLOCK 5).

---

## Findings pinned (for the maintainer)

1. **`(FI-field)` was on the wrong object.** A per-line field-of-definition
   certificate is unnecessary; the prize's full-field denominator reduces it to a
   single **ambient**-field size condition `log|F_n| = o(n)`. Print `(FI-field')`,
   not a C7-local certificate.
2. **Place it in `def:admissible-sequence`.** `(A1)`--`(A7)` never bound `|F_n|`;
   this is the one missing field clause. It is the "field hypothesis" already
   named in `rem:intro-countertheorem-scope` (L839) -- give it a symbol and put it
   in the ledger so `thm:main-smooth-circle` can cite it.
3. **The countertheorem is not a prize threat, and the tex can say so.** Its own
   `binom(N,2)` separation cost (eq (4.5)) makes `e_{MCA} = e^{-Theta(n)}`. A
   one-line addition to the scope remark -- that a prize-relevant line needs
   `|F|/|F_r| < 1/eps`, which the separation gate denies the countertheorem --
   would close the "verify its field hypothesis" caveat affirmatively for all
   poly-field rows.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_fi_field_discharge.py   # RESULT: PASS (59/59)
```
