# Section-nonpositive rational-host extraction fails: the exact non-host stratum

**Status (agents.md dialect):**
`COUNTEREXAMPLE (route-scoped to reduced rational-host presentations of #721) /
DECISION CRITERION = THEOREM (PROVED, exact iff) / GENERIC-FAILURE STRATUM =
THEOREM (PROVED under the section-nonpositive gate) / PROVABLE COUNTEREXAMPLE
FAMILY = THEOREM (PROVED) / three exact exhaustively-certified witnesses over
F_11, F_13, F_17.`

This note decides the **extraction** question that DannyExperiments' just-integrated
canonical reduced rational-host compiler (PR `#721`,
`experimental/notes/thresholds/canonical_reduced_rational_host_compiler.md`)
explicitly leaves open and names as its own next wall. It settles it from the
negative side: **extraction is false**, generically, and the exact stratum where
`#721`'s compiler *cannot* apply is a thin, explicitly described union of
low-dimensional subspaces. This completes the reach map of `#721` and sharpens
the `C8`/`(RC)` picture for the manuscript's hard input 3.

**Base:** `upstream/main @ c23dcaa` (the integrated tree containing `#721`).
No `.tex`/`.pdf` is edited.

---

## 0. De-confliction (mandatory, done first)

`#721`'s note **is not** a section-nonpositive extraction theorem, and it
**declares extraction as its own next target**. Verbatim, from its section 10
("Nonclaims and exact remaining wall"):

> "This note does not prove any of the following:
> - every `J<=0` received line has a reduced rational-host presentation;"

and, immediately after the Nonclaims list:

> "The exact next wall is **rational-host extraction plus aggregate payment**.
> For every `J<=0` line and every live first-match partial-occupancy slice, one
> must extract at most `exp(o(n))` line-determined reduced rational-host charts
> and route the complement to named transverse/nonlinear owners."

Its headline also states (section, lines 3-5):

> "This is a narrow `J <= 0` theorem, not a section-nonpositive extraction
> theorem and not a Grand MCA result."

Because Danny declares "rational-host extraction" as **the exact next wall** (his
own next target), this lane takes the **complementary negative hunt only**: a
`J<=0` received line admitting **no** reduced rational-host presentation. A
counterexample decides the question from the other side, collides with nobody,
and — where it lands — defines the exact stratum on which his compiler is
inapplicable, which is equally valuable to input 3. No positive-extraction claim
is made here; that target remains Danny's.

---

## 1. Objects and the class (all hypotheses visible)

Fix a prime field `F = F_p`, a domain `D subseteq F` with `|D| = n`, the code
`C = RS_F(D,k)` with `1 <= k < n`, an agreement parameter `k+1 <= a <= n`, and
the **section-nonpositive gate**

```text
J = a^2 - n(k-1) <= 0.
```

A **received line** is a pair `r = (r_0,r_1) in (F^D)^2` (this is exactly
`#721`'s object and the manuscript's line object of `def:exact-witness-incidence`,
L1324). It admits a **reduced rational-host presentation** (`#721`, RH1-RH2) if
there is `d` with `1 <= d <= a-k` and polynomials, for all `x in D`,

```text
r_0(x) = c_0(x) + U(x)/L(x),   r_1(x) = c_1(x) - T(x)/L(x),      (RH1)
c_0,c_1 in F[X]_{<k};  L monic, deg L = d, L(x)!=0 on D;
0 != T in F[X]_{<d}, gcd(L,T)=1;  deg U = a, ell = lc(U) != 0;
[X^j]U = 0 for d <= j <= d+k-1.                                  (RH2)
```

**The extraction question (input 3, the `C8`/balanced-core need).** Does every
section-nonpositive received line in the deployed/balanced-core class admit at
least one such presentation? The manuscript's `C8` cell
(`sec:cell-catalogue`, "Balanced-core and split-pencil cells", L2456-2474) pays
the projective-dimension-one split pencils and states, verbatim (L2473-2474):

> "Higher-dimensional balanced-core charts require a proved decomposition or a
> direct ray estimate."

That obligation is condition `(RC)` (`hyp:ray-compiler`, L6033-6051;
`rem:balanced-core-exhaustion`, L4763-4767; `def:balanced-quotient-core`,
L3431-3443: "in higher dimension this definition supplies no distinct-ray
bound, and the separate ray compiler is required"). `#721`'s compiler is a
per-chart engine that presupposes a rational-host chart *has already been
extracted*; extraction is the missing converse.

---

## 2. The exact decision criterion (PROVED, an iff)

**Theorem 1 (per-denominator decision, route-scoped to RH1-RH2).**
Let `R_0, R_1 in F[X]_{<n}` be the interpolants of `r_0, r_1` on `D`, let
`M_D = prod_{x in D}(X-x)`, and for a candidate `(d,L)` (`L` monic, `deg L = d`,
`1 <= d <= a-k`, `L(x)!=0` on `D`) put

```text
P_0 = (L * R_0) mod M_D,   P_1 = (L * R_1) mod M_D   (deg < n).
```

Then `r` admits a reduced rational-host presentation with this exact `(d,L)` if
and only if both

```text
(A)  deg P_0 = a;                       [then c_0, U are forced by (RH2)]
(B)  deg P_1 <= d+k-1  AND  T := (-P_1 mod L) != 0  AND  gcd(L,T) = 1.
                                        [then c_1 = (P_1 + T)/L, deg c_1 < k]
```

*Proof.* `r_0 = c_0 + U/L` on `D` iff `L c_0 + U` interpolates `(L(x)r_0(x))`;
since `deg(L c_0) <= d+k-1 <= a-1 < a = deg U < n`, this polynomial equals its
own interpolant `P_0`, so `deg P_0 = a` and `[X^a]P_0 = ell`. Given `deg P_0 = a`,
`#721` section 4.2's triangular map (diagonal 1) uniquely returns `c_0 in
F[X]_{<k}` with `U = P_0 - L c_0` satisfying the gauge and `deg U = a`; this is
(A). Symmetrically `r_1 = c_1 - T/L` on `D` iff `L c_1 - T = P_1`, forcing
`deg P_1 <= d+k-1`, `T = -(P_1 mod L)` (as `deg T < d`), `c_1 = (P_1+T)/L`; the
reducedness clauses `T != 0`, `gcd(L,T)=1` are (B). The tuple `(d,L,T,c_0,c_1,U)`
is `#721`'s unique canonical normal form (its Theorem, parts 2-4), so ranging
over `(d,L)` alone is exhaustive. ∎

The verifier validates Theorem 1 in **both directions**: it reconstructs `#721`
section 7's own two rational-host lines (a `d=1` and a `d=2` host) and the same
engine **finds** their presentations, reconstructing `r` on `D` byte-for-byte;
on the counterexamples below it certifies **none**.

**Consequence.** The only search dimension is `(d,L)`. Exhausting every monic
`L` of degree `d <= a-k` nonvanishing on `D` certifies non-existence exactly,
with no silent cap — the search space is
`sum_{d=1}^{a-k} #{monic deg-d L, L!=0 on D} <= sum_{d=1}^{a-k} p^d`.

---

## 3. The provable counterexample family (PROVED)

**Theorem 2 (section-nonpositive extraction fails; explicit family).**
Let `J <= 0` with `a <= n-1`. Let `g in F[X]` with

```text
k <= deg g <= n-1-(a-k).
```

Then for **any** `r_0`, the received line `r = (r_0, g|_D)` admits **no** reduced
rational-host presentation. (Note `deg g >= k` forces `g|_D notin C`, so `r_1` is
not a codeword: this is a genuine non-degenerate line, not the `r_1 in C`
boundary.)

*Proof.* For every candidate `(d,L)`, `deg(L g) = d + deg g <= (a-k)+(n-1-(a-k))
= n-1 < n`, so no reduction occurs and `P_1 = (L g) mod M_D = L g`, of degree
`d + deg g >= d + k > d + k - 1`. Criterion (B) fails at every `(d,L)`; by
Theorem 1 no presentation exists. ∎

The interval `[k, n-1-(a-k)]` is nonempty exactly when `a <= n-1`, and then
offers `n-a >= 1` admissible degrees for `g`. The kernel-checked arithmetic
engine is `family_obstruction` in the Lean package (section 6).

**Boundary remark (the `T=0` wall).** If instead `r_1 in C` (i.e. `r_1 = c_1|_D`,
`deg < k`), then `P_1 mod L = 0`, forcing `T = 0`, which the reduced direction
forbids: such lines also have no presentation, but for the *reducedness* reason
rather than the degree reason. Extraction thus fails on **both** sides of the
host degree window `[k, n-1-(a-k)]`.

---

## 4. Three exact certified witnesses

Exhaustive `(d,L)` search (verifier `--emit-cert`), zero presentations each:

| p  | D            | n  | k | a | J | a-k | r_1 = g\|_D (deg) | valid denominators searched | presentations |
|----|--------------|----|---|---|---|-----|-------------------|-----------------------------|---------------|
| 17 | {0,...,15}   | 16 | 2 | 4 | 0 | 2   | 1+3X²+X⁵ (5)      | 138 (`d=1`: 15, `d=2`: 123) | **0**         |
| 13 | {0,...,8}    | 9  | 2 | 3 | 0 | 1   | 2+X²+X⁴ (4)       | 4                           | **0**         |
| 11 | {0,...,8}    | 9  | 2 | 3 | 0 | 1   | 1+2X²+X³ (3)      | 2                           | **0**         |

The `F_17` row has `a-k=2`, so its exhaustion exercises the **genuinely-new
degree-2 denominators** — exactly the `d>1` normal form that is `#721`'s new
content — and still finds nothing.

---

## 5. The generic-failure stratum (PROVED under `J<=0`)

**Theorem 3 (the non-host stratum is almost everything).** Under `J <= 0`, the
set of received lines admitting a presentation projects, in the `r_1`
coordinate, into

```text
H = union_{d=1}^{a-k} union_{L monic, deg d, L!=0 on D}  L^{-1} . RS_F(D, d+k),
```

a union of at most `sum_{d=1}^{a-k} p^d` subspaces, each of `F`-dimension
`d+k <= a`. Hence

```text
|H| <= (a-k) . p^{2a-k},
```

and the section-nonpositive gate forces `2a - k <= n-1` (`#721` section 4.1;
kernel-checked `degree_gate_n_le_40` and exhausted to `n=64` by the verifier),
so `|H| <= (a-k) p^{n-1}`. Therefore a fraction at least

```text
1 - (a-k)/p
```

of the `p^n` vectors `r_1` admit **no** presentation, for any `r_0`. Extraction
fails **generically**, not exceptionally.

*Proof.* `deg P_1 <= d+k-1` says `(L(x)r_1(x))_{x in D}` is the evaluation of a
polynomial of degree `< d+k`, i.e. `L . r_1 in RS_F(D,d+k)` as a vector; since
`L(x)!=0` on `D`, `r_1 in L^{-1} RS_F(D,d+k)`. Union over the `<= sum p^d`
denominators, each image of dimension `d+k <= a`, gives `|H|`. The counting and
the gate `2a-k<=n-1` finish. ∎

This `H` is the **exact stratum where `#721`'s compiler can apply** — the
"reduced rational-host stratum" it identifies its `LineRay` object on. Theorem 3
says its complement (where extraction, hence the compiler, is unavailable) is a
`1 - O((a-k)/p)` fraction of all `J<=0` lines. Certified for the three rows: e.g.
`F_17`, host-lines `<= 4.83e7` inside an ambient `4.87e19`.

**Small-field note.** No section-nonpositive row with `a <= n-1` exists below
`n = 8` (first at `k=3, a=4, J=0`; kernel-checked `regime_floor_is_8`). A prime
field hosting `D subsetneq F` needs `p >= n+1 >= 9`, so among `{5,7,11,13}` the
fields `F_5, F_7` are **vacuous** for this regime and `F_11` is the smallest
usable prime field — which is why the witnesses use `p in {11,13,17}`.

---

## 6. Reproducibility

```bash
python3 experimental/scripts/verify_section_nonpositive_extraction.py
python3 -O experimental/scripts/verify_section_nonpositive_extraction.py
python3 experimental/scripts/verify_section_nonpositive_extraction.py --tamper-selftest
python3 experimental/scripts/verify_section_nonpositive_extraction.py \
    --emit-cert experimental/data/certificates/section-nonpositive-extraction/section_nonpositive_extraction.json
```

Stdlib-only, deterministic, `< 1 s`. The script AST-self-scans and contains no
Python `assert` (so `-O` runs the identical checks). `--tamper-selftest` mutates
a counterexample row into a genuine `d=1` rational-host line and confirms the
engine then **finds** the planted presentation (the search is not vacuously
empty). Certificate JSON:
`experimental/data/certificates/section-nonpositive-extraction/section_nonpositive_extraction.json`.

Lean statement package (core-only Lean 4 `v4.14.0`, no mathlib, no `sorry`,
`lake build` clean): `experimental/lean/section_nonpositive_extraction/`. It
kernel-checks the arithmetic engine (`ceiling_violated`, `family_obstruction`
by `omega`), the concrete row hypotheses (`rows_are_valid` by `decide`), the
degree gate (`degree_gate_n_le_40`), and the regime floor (`regime_floor_is_8`).
The polynomial/field semantics of Theorem 1 live in the Python verifier, not the
Lean file — labeled accordingly.

---

## 7. Interfaces and credit

- **DannyExperiments, PR `#721`** (`canonical_reduced_rational_host_compiler.md`):
  the reduced rational-host presentation (RH1-RH2), the uniqueness/incidence
  compiler this lane is scoped against, the degree-room lemma `a<n`, `k+2d<n`
  (section 4.1) bounding the search, and the two section-7 examples used here as
  positive controls. This note *completes the reach map* of that compiler by
  deciding its disclaimed converse from the negative side. The extraction target
  itself remains Danny's declared next wall.
- **DannyExperiments, PR `#704`** (`a6_all_witness_line_section_compiler.md`):
  the A6 transverse all-parameter line-section frontier, the other input-3
  attack this complements (it bounds retained slopes on an *extracted* chart;
  this note characterizes when a chart can be extracted at all).
- **`#713`** (`atlas_cat_cell_ledger.md`): the `C8` cell status
  "PAID (dim 1) / CONDITIONAL on (RC) (higher-dim = input 3)". Theorem 3 makes
  precise that the rational-host route to `(RC)` covers only the thin stratum
  `H`; the higher-dimensional balanced cores generically fall in its complement.
- **`ray_compiler_balanced_core.md` (PR `#528`)**: the PROVED per-chart
  transverse-secant bound and CONDITIONAL `(RC)` discharge on bounded-kernel
  cores. This note is disjoint (it decides *extraction*, not the ray count) and
  consistent (a chart must be extracted before `#528`'s bound applies).
- **Manuscript anchors** (`experimental/asymptotic_rs_mca_frontiers.tex`, base
  `c23dcaa`), byte-read here: `def:exact-witness-incidence` L1324; `C8`
  L2456-2474; `def:balanced-quotient-core` L3431-3443;
  `sec:ledger-closure`/balanced-core scope L4515; `rem:balanced-core-exhaustion`
  L4763-4767; `hyp:ray-compiler` `(RC)` L6033-6051.

## 8. Nonclaims

This note does **not**:

- prove any positive extraction statement (that target remains Danny's declared
  next wall) — it refutes the *universal* extraction claim and maps its failure
  stratum;
- assert that the balanced-core lines actually arising in the first-match atlas
  all fall in `H`'s complement — it proves the *ambient* generic failure and
  identifies `H` exactly; whether the atlas-realized `C8` charts are inside or
  outside `H` is the remaining positive question `(RC)` must still answer;
- close condition `(RC)`, the `C8` higher-dimensional balanced-core payment, or
  hard input 3; it *sharpens* what a positive extraction must achieve (it must
  land in `H`, a `O((a-k)/p)` fraction);
- make any Grand MCA / Grand List / global `LineRay`-census / profile-envelope /
  finite-deployed-row / prize-threshold claim;
- edit any `.tex`/`.pdf` or claim promotion.
