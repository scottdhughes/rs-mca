# CAP25 v13: the image-structure theorem for the F_p-span cell — closing the
# surjection PR #422 left OPEN, with occupancy `= p^{-defect}` and the
# classification `image = W_c <=> defect = 0`

Status: `ANALYSIS` (§2.1 the **containment** `image(Phi|_a) subset` a single coset
of the move-subspace `D <= W_c^0`, a complete argument with no hypothesis, and
§2.4 the **strengthened obstruction** `Gamma_2 >= index * p^{defect}` from
containment + Cauchy–Schwarz alone — strictly stronger than #422's
`Gamma_2 >= index`, and free of any surjection) / `PROVED` (§2.2–2.3 the
**occupancy formula** `|image|/|W_c| = p^{-defect}` and the **classification**
`image = W_c <=> defect = 0`, each a complete proof **under the connectivity
hypothesis `Conn_a`**; §3 the **defect = pinned-functional-count** identity and
the trace-hyperplane characterization, unconditional) / `PROVED-AT-TOYS`
(`Conn_a` itself verified by exhaustive census at all seven configs; the two
coordinate laws inherited from #422) / `MEASURED` (§3 the designed `defect in
{0,1,2}` occupancies `1, 1/2, 1/4` — the `m = 2` case **realized**; §4 the exact
connectivity band, toy-exact) / `OPEN` (§4 a closed form for the connectivity
threshold; §8 next measures).

**Verifier:** `experimental/scripts/verify_entropy_inverse_fp_span_surjection.py`
(zero-arg, stdlib-only, self-contained — no lane imports; `RESULT: PASS (253/253
checks)`, exit 0; ~13 s and ~14 MB peak RSS **on the authoring box** — timing and
RSS are environment-specific and deliberately not gated; best-effort `RLIMIT_AS`
guard, default 2 GB, tune or disable via `FP_SURJ_AS_CAP_GB`, never fatal;
`FP_SURJ_DATA_DIR` overrides the data location; `FP_SURJ_DUMP` regenerates the
committed JSON from the run's own recomputation). One script that **recomputes
from scratch** — the finite-field arithmetic (smallest-irreducible modulus), the
moment-curve census, `dim_Fp V_T`, `dim_Fp D` (the move-subspace), `dim_Fp
W_c^flat`, the exact image census and occupancy, the `defect`, the pinned
functionals `ell(s) = Tr(mu s_1)`, the containment bound
`Gamma_2 >= index * p^{defect}`, and the exact connectivity bands — then gates
every recomputed number against the committed data JSON
`experimental/data/cap25_v13_entropy_inverse_fp_span_surjection.json` (exact on
ints / strings / bools, `1e-9` on floats). Dual path: the field multiply table
vs the log/antilog backend (full `F_27` and `F_32` sweeps), plus the identity
`Tr(t) = ` (top coordinate) for the smallest-irreducible `F_64` that pins the
`F64-firstN` cell. It ends with **seven tamper self-tests**: a faked move-span
dim, a faked coset size, a designed non-spanning `T` that **must** show occupancy
`< 1`, a **threshold-violating extreme `a` that must fail coverage** (`a = 1`
never realizes the coset), the exact containment `n_occ <= |D|` on the
`Conn`-**failing** config, the pinned functional's load-bearing test, and the
`m = 2` occupancy-`1/4` test.

**What this is / is not.** This is a **theorem-level closure of the one surjection
PR #422 explicitly left `OPEN`** (#422 §2.3 / §6: "the general surjection
`image = W_c` … is left an `OPEN` sketch"). It answers the #422 review's remaining
ask — *a separately proved theorem promoting `image = W_c` from `MEASURED` to a
characterization* — by proving the exact image is a **coset of the move-subspace
`D`**, deriving the occupancy `p^{-defect}` and the classification
`image = W_c <=> defect = 0` (both under the measured `Conn_a`, which was
verified exhaustively at every shipped config), and identifying the
`F64-firstN` "half" as a
**non-spanning-`T` structure statement** (its `defect = 1` pinned functional
located explicitly as `ell(s) = Tr(s_1)`). It is **not** a proof or refutation of
`prob:entropy-inverse-q`, **not** a row-sharp / deployed-finite claim of any kind,
and **not** a correction to the atom. **Merge framing: an experimental/analysis
note that upgrades the #422 image-span cell from a measured occupancy to a proved
image-structure classification, with the connectivity threshold measured and the
`m >= 2` defect newly realized — asymptotic-lane only, no finite adjacent-row
progress claimed (§9 nonclaims).** Conventions are inherited from PR #420/#421/#422
and extended, never contradicted.

Lineage `#414 -> #416 -> #417 -> #420 -> #421 -> #422 -> ` this packet. PR #422
proved `image(Phi) subset W_c` (containment into the ambient) and MEASURED
`image = W_c` at `S27`/`U16o` (occupancy `1`) but `image = ` half of `W` at
`F64-firstN` (occupancy `0.5`), leaving the **exact image** — the surjection —
`OPEN`. This packet computes the exact image for **every** projective-class
configuration.

---

## 0. The atom's open surjection and what this closes `REFERENCE`

The maintainer's Q1 atom is `prob:entropy-inverse-q` in
`experimental/grande_finale.tex` (L827); its escape clause (L828) asks to "identify
the extra obstruction cell". PR #422 identified the **`F_p`-span cell**: for
projective weights `rho(T) subset c F_p^times` the map `Phi(x) = sum_t x_t v_t`
(columns `v_t = rho(t)(1,t,...,t^{R-1}) in K^R`, `K = F_{p^k}`, slice
`x in {-1,0,1}^T` signed / `{0,1}^T` unsigned with exactly `a` active) has its
image inside the subgroup

> `W_c = { s in K^R : s_0 in c F_p, s_{pj} = c^{1-p} s_j^p whenever pj < R }`
> (head **free** here, as in #422's signed reading; §1 pins the head for the
> unsigned `p = 2` slices and reserves `W_c^flat` for the head-free space),

because the two coordinate laws (`s_0 in c F_p`; the Frobenius law
`s_{pj} = c^{1-p} s_j^p`) hold on every column and are `F_p`-linear. #422 then
**measured** the exact image `= W_c` at two configs and `=` half of `W_c` at a
third, and left the general value `OPEN`. **This note closes it.** All quotes and
line refs (L827 atom, L828 escape, L839 removal, L862/863 alternatives (a)/(b),
L876 `prop:vandermonde-kills-low-rank`) are as in #422 and are present in the
tex at those lines (verified in main `b99b2c4`); the verifier's provenance
block gates the line numbers as committed constants.

---

## 1. Setup and the move-subspace `D` `CONVENTION`

The datum is the literal #422 toy (`ones` weight `rho == 1`, the admissible `c = 1`
representative; the projective-class invariance to general `c` is #422's, and
mul-by-`c` is an `F_p`-automorphism carrying `W_1 -> W_c`, so every statement below
is `c`-uniform). Fix a base slice point `x_0` (so `Phi(x_0) in W_c`). Define the
**move-subspace**

> `D = V_T := span_{F_p}{ v_t : t in T }`               (signed, `p` odd),
> `D := span_{F_p}{ v_t + v_{t'} : t, t' in T }`  (the even column sums, unsigned `p = 2`).

`D` is the `F_p`-span of the **elementary moves** that keep the active count `a`
fixed:

- **unsigned `p = 2`:** the only move is a **swap** `t -> t'` within the support,
  which changes `Phi` by `v_{t'} + v_t` (char 2). So `D` is exactly the swap span.
- **signed `p` odd:** the moves are **swaps** (`+-v_{t'} +- v_t`) and **sign flips**
  `x_t: +1 -> -1`, which change `Phi` by `-2 v_t`. Because `2` is a unit for `p`
  odd, `<-2 v_t>_{F_p} = <v_t>_{F_p}`, so the sign flips alone generate every
  `<v_t>`, giving `D = V_T` (the **full** column span). At `p = 3` this is the
  cited `-2 = 1` collapse; it holds for all odd `p`.

Also define the **head-free ambient**
`W_c^flat := { s : s_0 in c F_p, s_{pj} = c^{1-p} s_j^p }` — the `F_p`-space #422
calls the `s_0`-free `W` — and the **translation subgroup** `W_c^0` of `W_c`:
for signed `p` odd the head is a free `c F_p`-line so `W_c^0 = W_c = W_c^flat`; for
unsigned `p = 2` the head is pinned to the single value `s_0 = (a bmod 2) c` so
`W_c` is an affine coset of `W_c^0 = { s in W_c^flat : s_0 = 0 }`. The verifier
gates the dimensions

> `dim_Fp W_c^flat = 1 + k * #free`,   `#free = #{ j in [1,R) : p nmid j }`,
> `dim_Fp W_c^0 = (1 if signed & p>2 else 0) + k * #free`,   `|W_c| = p^{dim W_c^0}`.

The single new datum this packet adds to the #422 grid is the

> **`defect := dim_Fp W_c^flat - dim_Fp V_T >= 0`**,

a property of the **column geometry alone** (independent of `a`, of signed/unsigned,
and of the connectivity below). Everything else is #422's, recomputed.

---

## 2. The image-structure theorem `ANALYSIS` / `PROVED`

### 2.1 Containment: the image is one coset of `D <= W_c^0` `ANALYSIS`

**Theorem A (containment, no hypothesis).** For every `1 <= a <= N-1`,
`image(Phi|_a) subset Phi(x_0) + D`, a single coset of `D`, and `D subset W_c^0`.

*Proof.* `Phi` extends to the `F_p`-linear map `F_p^T -> K^R` (#422 §2.1).

*Unsigned `p = 2`.* Any two exactly-`a` slice points `x, x'` differ by an
**even-weight** vector `x + x' in F_2^T` (both have weight `a`, so the symmetric
difference is even). The even-weight vectors are the subspace
`E = ker(1^T cdot)`, spanned by `{ e_t + e_{t'} }`, and `Phi(E) = span{ v_t + v_{t'} }
= D`. Hence `Phi(x) - Phi(x') = Phi(x + x') in D`, so `image - image subset D`,
i.e. the image lies in one coset `Phi(x_0) + D`. Each generator `v_t + v_{t'}` has
head `1 + 1 = 0 in c F_p` and satisfies the (`F_p`-linear) Frobenius law, so
`v_t + v_{t'} in W_c^0` and `D subset W_c^0`.

*Signed `p` odd.* `Phi(x) = sum_t x_t v_t in V_T = D` trivially (coefficients
`x_t in {-1,0,1} subset F_p`), and `Phi(x_0) in V_T`, so `image subset V_T =
Phi(x_0) + V_T`. Each `v_t` satisfies both laws with head in `c F_p`, so
`V_T subset W_c^flat = W_c^0`. `∎`

**Corollary (occupancy upper bound, exact-count).**
`n_occ = |image| <= |D| = p^{dim_Fp D}`, and `dim_Fp D - dim_Fp W_c^0 = -defect`
in both cases (unsigned: `(dim V_T - 1) - (dim W_c^flat - 1)`; signed:
`dim V_T - dim W_c^flat`). So `|image| <= |W_c| * p^{-defect}`.

### 2.2 The occupancy formula, under connectivity `PROVED`

Let **`Conn_a`** be the hypothesis that the containment of Theorem A is an
**equality**: `image(Phi|_a) = Phi(x_0) + D`. Equivalently (verifier-checked as a
restatement): every coset of the kernel code `ker Phi` whose head-syndrome is
`a bmod p` contains a weight-exactly-`a` word. `Conn_a` is a **combinatorial**
side condition on `a` (§4); Theorem A is its trivial half.

**Theorem B (occupancy).** Under `Conn_a`,
`occupancy := |image| / |W_c| = p^{-defect}` **exactly**.

*Proof.* `Conn_a` gives `|image| = |D| = p^{dim_Fp D}`; divide by `|W_c| =
p^{dim_Fp W_c^0}` and use `dim D - dim W_c^0 = -defect` (§2.1 corollary). `∎`

### 2.3 The classification `PROVED`

**Theorem C (classification).** Under `Conn_a`,
`image = W_c <=> defect = 0 <=> V_T = W_c^flat` — i.e. iff the columns `F_p`-span
the **full** Frobenius-closed head space.

*Proof.* `image subset W_c` and both are `p`-power sets, so `image = W_c <=>
occupancy = 1 <=> p^{-defect} = 1 <=> defect = 0 <=> dim V_T = dim W_c^flat`, and
`V_T subset W_c^flat` makes the last equality `V_T = W_c^flat`. `∎`

This is the ask: **`image = W_c` is no longer a measured occupancy but a
characterization** — surjectivity onto `W_c` is equivalent to a clean algebraic
non-degeneracy of the column set (`defect = 0`), and it holds under the connectivity
band of §4. The two #422 surjective configs and the one half-config are the three
smallest instances (§5).

### 2.4 The strengthened obstruction — free of the surjection `ANALYSIS`

**Theorem D (obstruction).** For every `1 <= a <= N-1` (no `Conn` needed),
`Gamma_2 >= index * p^{defect}`, where `index = [K^R : W_c]`.

*Proof.* `Gamma_2 = q^R sum_s N(s)^2 / C^2 >= q^R (sum_s N(s))^2 / (n_occ * C^2)`
by Cauchy–Schwarz over the `n_occ` occupied fibers `= q^R / n_occ >= q^R / |D|`
(Theorem A) `= q^R / (|W_c| p^{-defect}) = index * p^{defect}`. `∎`

This uses **only containment** (`n_occ <= |D|`), not the surjection, and is
**strictly stronger** than #422's `Gamma_2 >= index` whenever `defect > 0`: the
verifier gates it on all seven configs, including the `Conn`-failing `S27-1HP`
where `Gamma_2 = 38.9 >= index * p = 27` still holds. So the obstruction the atom
cares about survives the surjection being false.

---

## 3. The pinned functionals and the defect `PROVED` / `MEASURED`

**Theorem E (defect = pinned functionals).** `defect` equals the dimension of the
`F_p`-space of functionals on `W_c^flat` vanishing on every column
`{ ell in (W_c^flat)^* : ell(v_t) = 0 for all t in T }` (the **pinned
functionals** — each cuts the image by one further `F_p`-dimension beyond the head).

*Proof.* `defect = dim W_c^flat - dim V_T = dim (V_T)^{perp} cap (W_c^flat)^*`,
the annihilator of `V_T` inside `(W_c^flat)^*`. `∎`

**Their shape.** Every `F_p`-functional on `K^R` is `ell(s) = sum_j Tr_{K/F_p}(
lambda_j s_j)`. On `W_c^flat` the Frobenius law `s_{pj} = s_j^p` (`c = 1`) folds the
reducible coordinates into the free ones (`Tr(lambda_{pj} s_j^p) =
Tr(lambda_{pj}^{1/p} s_j)`), so a functional is `(lambda_0; (nu_j)_{j in free})`
with
`ell(v_t) = Tr(lambda_0 + P(t))`, `P(X) = sum_{j in free} nu_j X^j`. **Pinned**
means `Tr(lambda_0 + P(t)) = 0` for all `t in T`. The head functional (`lambda_0
!= 0`, `nu = 0`, value `Tr(lambda_0) != 0` on every column) is **not** pinned — it
is the even-sum codimension already spent in `W_c^0`. So

> **`T` inside an intersection of `m` independent linear trace-hyperplanes
> `{ t : Tr(mu_i t) = 0 }` forces `defect >= m`** (take `nu_1 = mu_i`, other
> coordinates zero), hence `occupancy <= p^{-m}`.

**`F64-firstN` explained structurally (`defect = 1`).** `T = ` the first `21`
nonzero elements of `F_64 = F_2[x]/(x^6+x+1)`. Every such `t < 32` has its
`x^5`-coordinate `= 0`; for this modulus the absolute trace **is** the
`x^5`-coordinate (`Tr(t) = (t >> 5) & 1`, gated as a dual path), so
`T subset { Tr(t) = 0 }`. The pinned functional is therefore
`ell(s) = Tr(s_1)` — it reads the free coordinate `s_1`, is nonzero on `W_c^flat`,
and vanishes on the whole image (verifier: `ell(image) = {0}`). This is the
"vacancy in the coordinates of the column vectors" the #422 half-occupancy hid: not
`t < 32` per se, but `T` sitting in a **trace-hyperplane** of `K`, which pins the
`s_1`-functional on the image. Occupancy `= p^{-1} = 1/2`, **derived**.

**`m = 2` realized (`defect = 2`, occupancy `1/4`).** Placing `T` in the
intersection of **two** independent trace-hyperplanes pins **two** independent
functionals `ell_1(s) = Tr(mu_1 s_1)`, `ell_2(s) = Tr(mu_2 s_1)`:

| designed config | `q` | `R` | `N` | `a` | `defect` | occupancy | pinned `mu`'s |
|---|---:|---:|---:|---:|---:|---:|---|
| `F32-1HP` (one HP) | `2^5` | 3 | 15 | 7 | **1** | `1/2` | `{1}` |
| `F32-2HP` (two HP) | `2^5` | 3 | 7 | 3 | **2** | `1/4` | `{1, g}` |
| `F64-2HP` (two HP) | `2^6` | 3 | 15 | 7 | **2** | `1/4` | `{1, g}` |

Both `ell_1, ell_2` verified vanishing on the image, `occupancy = 0.2500` exactly,
`Conn` holding. So the defect index is genuinely `p^m` with `m >= 2` attainable —
answering the `m > 1` question in the affirmative; the classification of §2.3 is
sharp across `m in {0, 1, 2}`.

---

## 4. The connectivity threshold `MEASURED` / `OPEN`

`Conn_a` (§2.2) is exactly: **every coset of the kernel code `ker Phi` of the right
head-parity meets the exactly-`a` slice.** `ker Phi` is the code of `F_p`
dependencies among the columns; by `prop:vandermonde-kills-low-rank` its minimum
distance is `R+1` (#422 §4, the exact Vandermonde `R+1` barrier). So `Conn_a` is a
**coset weight-distribution** property of a minimum-distance-`(R+1)` code — a
genuine combinatorial question with **no simple closed form**. The verifier gates
the exact full-`a` band at five toys (exhaustive census):

| config | `q` | `R` | `N` | `dim D` | full-coset `a` band | clean regime |
|---|---:|---:|---:|---:|---|---|
| `U-F16@R3:N10` | `2^4` | 3 | 10 | 4 | `{3,4,5,6,7}` | `[R, N-R]` exactly |
| `U-F8@R3:N7`   | `2^3` | 3 | 7  | 3 | `{3,4}`         | `[R, N-R]` exactly |
| `U-F16@R4:N12` | `2^4` | 4 | 12 | 8 | `{5, 7}`        | `[R+1,N-R-1]` **with a hole at 6** |
| `S-F27@R3:N10` | `3^3` | 3 | 10 | 7 | `{6,7,8}`       | signed band (sign flips shift it) |
| `S-F27@R3:N11` | `3^3` | 3 | 11 | 7 | `{5,...,10}`    | signed band, widens with `N` |

**What is proved and what is measured.** The *containment* half of `Conn_a` and
Theorems A/D are unconditional. For the *reverse* (occupancy `= p^{-defect}`,
Theorems B/C) `Conn_a` is a hypothesis, **verified by exhaustive census at all
seven ship configs** (`PROVED-AT-TOYS`). The exact minimal band is `MEASURED`: in
the **large-kernel** regime it is the clean interval `[R, N-R]` (unsigned, `R` odd)
or `[R+1, N-R-1]` (unsigned, `R` even); the failures are (i) always at the extremes
`a < R` or `a > N-R` (no room to compose swaps — e.g. `a = 1` gives the `N`
raw column images, never a `p`-power coset, the verifier's threshold tamper test),
and (ii) for **small kernels**, isolated interior parities (the `a = 6` hole at
`F16@R4:N12`, where `ker Phi` has dimension `3`, too few codewords to re-balance
that one syndrome). The signed band differs because sign flips add moves. A
closed-form threshold is `OPEN` (§8); it is **not** needed for the obstruction
(Theorem D) or the classification's structural side (`defect`).

---

## 5. Corollaries: the #422 occupancies, derived `PROVED` (under `Conn`)

The three #422 configs are now **derivations**, not measurements (each `Conn_a`
verified exhaustively):

| config | signed | `R` | `N` | `a` | `dim V_T` | `dim W_c^flat` | `defect` | occupancy | why |
|---|:--:|---:|---:|---:|---:|---:|---:|---:|---|
| `S27@R4`   | yes | 4 | 14 | 7 | 7 | 7 | **0** | **1**   | `V_T = W_c^flat`; head free (signed) |
| `U16o@R4`  | no  | 4 | 15 | 8 | 9 | 9 | **0** | **1**   | `V_T = W_c^flat`; even-sum codim = head |
| `F64-fN@R3`| no  | 3 | 21 | 10| 6 | 7 | **1** | **1/2** | `T subset {Tr(t)=0}`, one pinned `Tr(s_1)` |

`S27` and `U16o` have `defect = 0` (the columns fill the Frobenius-closed head
space), so `image = W_c` by Theorem C — the surjection is now **proved** for them.
`F64-firstN` has `defect = 1` from the trace-hyperplane, so `image` is exactly a
**half-`W_c` coset** (Theorem B), a *non-spanning-`T`* statement, not a failure of
the mechanism. The `110x`–`120x` / `23x` collision figures of #422 are unchanged;
what is new is that their exact index is now the **proved** `index * p^{defect}`
lower bound (Theorem D), and the occupancy is a **proved** `p^{-defect}` rather than
a census count.

---

## 6. What this means for #422 and the ledger `ANALYSIS`

- **The #422 review's remaining ask is answered.** #422 §7 (weave) records the
  review (DannyExperiments, 2026-07-08) asking for "a separately proved theorem
  promoting `image = W_c`". Theorems B/C do exactly that: the surjection is a
  **classification** (`image = W_c <=> defect = 0`) under a connectivity band that
  is exhaustively verified at the toys and clean in the large-kernel regime. The
  `OPEN` sketch of #422 §2.3 is discharged into (proved structural side) +
  (measured combinatorial band).
- **The obstruction is now surjection-free and stronger.** Theorem D gives
  `Gamma_2 >= index * p^{defect}` from containment alone, so the #422 cell's
  collision excess never depended on the surjection — and it is a factor `p^{defect}`
  larger than the printed `Gamma_2 >= index` when the cell is non-spanning.
- **The `F64` "failure" is a structure statement.** Its half-occupancy is the
  presence of a pinned functional `Tr(s_1)` from `T` lying in a trace-hyperplane —
  admissible input, `rank_K` still full, and it *sharpens* the cell rather than
  weakening it.
- **The ledger options 1–3 are unmoved in kind, sharper in degree.** The atom's
  three resolutions (add a `rho`-genericity hypothesis / add the `F_p`-span cell /
  restate (b) over the prime field) are #422's; this packet only makes the cell's
  image **exactly computable** (`= Phi(x_0) + D`, occupancy `p^{-defect}`), so
  option 1's "restrict to `defect = 0` weights/supports" and option 2's cell
  definition can now be stated with the exact image, not an occupancy estimate.
  This packet **does not choose** among them.

---

## 7. Guards and verification `AUDIT`

The verifier PASSES **253/253** checks (~13 s, ~14 MB peak RSS **on the authoring
box** — both environment-specific, neither gated), recomputing from scratch and
gating against the committed JSON. Reproducibility knobs: `FP_SURJ_AS_CAP_GB`
(best-effort `RLIMIT_AS`, default 2 GB, never fatal), `FP_SURJ_DATA_DIR` (data
location), `FP_SURJ_DUMP` (regenerate the JSON from the run's own recomputation).
Dual-path and tamper guards:

- **Field multiply dual path.** Table backend equals log/antilog on the full `F_27`
  and `F_32` product tables (`0` mismatch); and `Tr(t) = (t>>5)&1` for the
  smallest-irreducible `F_64` (`0` mismatch), the identity that pins `F64-firstN`.
- **Seven tamper self-tests** (each must be caught): a faked move-span dim (`p^{dim-1}
  != |D|`); a faked coset size (the `index * |W_c| = q^R` identity breaks); the
  designed non-spanning `F64-firstN` **must** show `occupancy < 1`; a
  **threshold-violating extreme `a`** (`a = 1` on `U16o` gives `N` raw images, never
  the `p^{dim D}` coset); the exact containment `n_occ <= |D|` on the
  `Conn`-**failing** `S27-1HP` (proving containment is unconditional); the pinned
  functional load-bearing test (`Tr(s_1)` vanishes on the `F64` image yet is nonzero
  on `W_c^flat`); and the `m = 2` occupancy-`1/4` test (`F32-2HP`).

---

## 8. OPEN — next-measure list `OPEN`

- **Closed-form connectivity threshold.** A closed form for the full-coset `a`
  band as a function of `(q, R, N, signed)` — a coset weight-distribution of the
  minimum-distance-`(R+1)` Vandermonde kernel code. The large-kernel clean regime
  `[R, N-R]` / `[R+1, N-R-1]` is measured; the small-kernel interior holes and the
  signed shift want a proof.
- **`defect` under a generic twist.** Measure `defect` (equivalently
  `codim_{F_p} V_T`) as a function of the twist entropy of `rho`, quantifying how
  much genericity option 1 needs (the #422 §6 twist-codimension census, now with the
  exact-image reading).
- **`m >= 3` and mixed head/`s_j` pinning.** Force three independent pinned
  functionals, and a pinned functional with `lambda_0 != 0` (affine trace-hyperplane
  `Tr(mu t) = 1`), to map the full `defect` lattice.
- **Signed non-spanning witness with `Conn`.** A signed `defect >= 1` config large
  enough for `Conn` to hold (needs `|T|` past the signed band while staying
  exhaustively enumerable) — the unsigned defect witnesses are exact; the signed one
  is currently only structural (`dim V_T < dim W_c^flat` at `S27-1HP`, where `Conn`
  fails at `N = 8`).

---

## 9. Weave and nonclaims `AUDIT`

- **PR #422 `cap25_v13_entropy_inverse_fp_span_cell` (direct predecessor).** Proved
  `image subset W_c`, the two `c`-form laws, `Gamma_2 >= index`, and MEASURED
  `image = W_c` at `S27`/`U16o` with the `F64-firstN` half left `OPEN`. This packet
  proves the exact image (`= Phi(x_0) + D`), derives the occupancies, strengthens
  the bound to `Gamma_2 >= index * p^{defect}`, and locates the `F64` pinned
  functional. It **extends** #422's grid by the single `defect` datum and never
  contradicts it; every #422 census statistic it re-touches (`n_occ`, `index`,
  `G2`, `free`/`red`, `dim V_T`, `K_rank`) is reproduced.
- **The #422 review (DannyExperiments, 2026-07-08).** Its remaining ask — a proved
  theorem promoting `image = W_c` — is the target of §2.2–2.3; the containment +
  Cauchy–Schwarz route that frees the obstruction from the surjection (§2.4) is the
  review's own sharpening, here carried to `index * p^{defect}`. Credited with
  thanks; this note is collaborative follow-through, not a correction.
- **PRs #420/#421 and #414–#417.** The `excess`/baseline discipline, the `R > w`
  moment-curve reading, and the Vandermonde `R+1` barrier (which is exactly the
  kernel-code minimum distance controlling §4) are inherited unchanged.
- **`prop:vandermonde-kills-low-rank` (L876).** Used twice: `rank_K` full (so
  alternative (b) is blind, #422) and `ker Phi` has minimum distance `R+1` (the
  connectivity mechanism, §4).
- **This packet consumes no upper cell and instantiates no `U(1116048)` certificate.**

**Nonclaims.**

- This note does **not** prove or refute `prob:entropy-inverse-q`, and does **not**
  claim the removal list is incomplete as intended — it computes the exact image of
  the #422 cell and leaves the three-option ledger resolution to the program.
- **No finite claim of any kind:** nothing here proves anything about
  `prob:row-sharp-q` / `def:q-row-atom`, certifies **no deployed finite safe row**,
  and instantiates **no `U(a_0+1) <= B*` certificate**. The deployed KoalaBear /
  Mersenne-31 rows are outside the mechanism twice over — prime field (`K = F_p`,
  where `F_p`-span `= K`-span, so `defect = 0` degenerately and there is no cell) and
  active prefix depth below the characteristic (`R-1 < p`, so no reducible columns).
  Asymptotic-lane only.
- Theorems **A** (containment) and **D** (`Gamma_2 >= index * p^{defect}`) are
  complete unconditional arguments (`ANALYSIS`). Theorems **B** (occupancy
  `= p^{-defect}`) and **C** (`image = W_c <=> defect = 0`) are complete **under the
  connectivity hypothesis `Conn_a`**, which is `PROVED-AT-TOYS` (exhaustive census)
  at all seven configs and `MEASURED` in general (§4). Theorem **E** (`defect =
  #pinned functionals`) and the trace-hyperplane characterization are unconditional
  (`PROVED`); the `defect in {1,2}` occupancies and the `m = 2` realization are
  `MEASURED` (exact toy enumeration). No closed-form connectivity threshold is
  claimed.
- `D`, `W_c^flat`, `defect`, `Conn_a`, and the config grid are conventions; the
  classification is reported as robust to any `O(1)` choice, since the occupancy is
  the exact `p^{-defect}` and the obstruction is exact.
