# Q1 atom: the differential-locator and Frobenius-index cell laws, PROVED — upgrading PR #446's three char-p laws from MEASURED to theorems

Status:
`PROVED` (§1 L1 the differential `K`-rank defect law `rank_K Span{v'_t} =
(R-1)-floor((R-1)/p)` with exact `|T|` hypothesis and its Cauchy–Schwarz
collision corollary `Gamma_2 >= q^{defect_K}`; §2 L2 the Frobenius-index closed
form `index = p^{k(1+floor((R-1)/p))-eps}` from the one-line subfield law and its
threshold corollary; §3 L3 prime-field inertness `index=1` under `R<=p`) /
`REFERENCE` (§0 — the atom, its columns, the removed differential-locator cell,
alternative (b), all quoted with line refs) /
`CONVENTION` (§0 — the syndrome/power-sum coordinates and the `index` definition,
inherited unchanged from PR #422/#428/#446) /
`MEASURED` (unchanged, cited not re-derived — the *occupancy* question, i.e.
whether the actual span `V_T` fills the ambient ceiling `W_c` so that `fp_defect=0`;
this is `N`- and `T`-dependent and stays with #427/#428) /
`AUDIT` (§5 — three prose sharpenings against #446's note, each consistent with
#446's own gated JSON) / `OPEN` (§6 — the asymptotic promotion, untouched).

**Verifier:** `experimental/scripts/verify_atom_differential_cell_laws.py`
(zero-arg, stdlib-only, self-contained — no lane imports; `RESULT: PASS
(3333/3333 checks)`, exit 0; ~0.1 s and ~15 MB peak RSS **on the authoring box** —
environment-specific, not gated; best-effort `RLIMIT_AS` guard, default 2 GB, tune
or disable via `DCL_AS_CAP_GB`, never fatal; `DCL_DATA_DIR` overrides the data
location; `DCL_DUMP` regenerates the committed JSON from the run's own
recomputation). One script that **recomputes from scratch** — the finite-field
arithmetic (smallest-irreducible modulus), the moment columns `v_t`, the
derivative columns `v'_t`, `rank_K`, `dim_Fp`, the `free`/`red` split and
`#red=floor((R-1)/p)`, the index closed form, the exhaustive subfield-law check on
syndromes, and the collision census / `Gamma_2` — then gates every committed number
against the data JSON (exact on ints/strings/bools, `1e-9` on floats). Dual path:
field multiply table vs log/antilog on `F_27`, `F_16`, `F_125`. Ends with **seven**
tamper self-tests, each feeding a corrupted value into the *same* live
`geq`/`want_true` gate used in the body and confirming the gate returns `False`
(caught), then retracting the side effect (a faked L1 rank, a faked L1 defect, a
faked L2 index, a faked subfield-law violation, a faked L3 inertness at the
boundary, a below-threshold collision `Gamma_2`, a non-collapsing `E={0}` slice).

**What this is / is not.** PR #446 broke the `R=w` wall and **measured** three
char-`p` laws (its §3 differential-locator `defect_K=1+floor((R-1)/p)`
`PROVED-AT-TOYS`/`ANALYSIS`, its §2/§4 Frobenius index sweep `MEASURED`, its §6
prime-field `index=1` immunity `PROVED-AT-TOYS`). This packet **proves all three at
arbitrary `p, k, R`** with exact hypotheses, and cross-validates the closed forms
against exhaustive computation on a fresh field grid. **It is a proof upgrade in the
asymptotic/experimental lane. It does not** prove or refute `prob:entropy-inverse-q`,
resolve `prob:row-sharp-q` / `def:q-row-atom`, produce a row-sharp `Q`, or touch any
deployed finite row. The three laws are structural facts about the column geometry;
the *occupancy* question (does the span fill the ceiling) is unchanged and stays
`MEASURED` with #427/#428. **No PR #446 law needed correction** — all three
reproduce exactly; the only deltas are three prose sharpenings (§5).

Lineage (credit by PR): `#420/#421` (toy dichotomy / missing-cell hunt — the `R=w`
wall), `#422` (the `F_p`-span cell; the subfield law's `c`-form one-line-proof
home, §2.1), `#427` (twist span-codimension census; the per-subfield `Frob^d` law
`PROVED-AT-TOYS`, §4), `#428` (image-structure theorem: occupancy `p^{-defect}`,
`Gamma_2 >= index*p^{defect}`), `#429`/`#430` (connectivity band / residual
controls), `#446` (broke the wall and measured L1/L2/L3 — this packet's direct
predecessor). This packet consumes no upper cell and instantiates no `U(1116048)`
certificate.

---

## 0. Setup — the atom object, syndromes, and the index `REFERENCE` / `CONVENTION`

The Q1 atom is `prob:entropy-inverse-q` in `experimental/grande_finale.tex` (L827).
Fix a finite field `K = F_{p^k}` (char `p`, degree `k`), a set `T ⊆ K` of `N`
**distinct** points, a depth `R`, and weight `rho ≡ 1` (the admissible `c=1` choice,
L828, "choose nonzero weights `rho(t) ∈ K^×`"). The **moment columns** and their
formal **derivative columns** are

> `v_t = (1, t, t², …, t^{R-1}) ∈ K^R`,  
> `v'_t = d/dX (1,X,…,X^{R-1})|_{X=t} = (0, 1, 2t, 3t², …, (R-1)t^{R-2}) ∈ K^R`.

The removal list (L839, verbatim) is taken *after* "quotient pullbacks,
Chebyshev/dihedral pullbacks, planted common blocks, tangent cells, extension
cells, **differential-locator low-defect cells**, and saturation cells have been
removed"; the derivative geometry `v'_t` **is** that differential-locator cell.
Alternative (b) (L863–865, verbatim) asks for a `K`-rank defect
`rank_K Span{v_t : t∈U} < min(|U|,R)`, which `prop:vandermonde-kills-low-rank`
(L876) forbids for the moment columns but which the derivative columns exhibit (L1).

**Syndrome / power-sum coordinates `CONVENTION` (inherited).** A profile slice
`x ∈ {0,1}^T` (unsigned) or `x ∈ {-1,0,1}^T` (signed), with `x_t` in the prime field
`F_p ⊆ K`, maps to the syndrome `s = Phi(x) = Σ_t x_t v_t ∈ K^R` whose `j`-th
coordinate is the **power sum** `s_j = Σ_t x_t t^j`. The differential syndrome
`s' = Σ_t x_t v'_t` has `j`-th coordinate `j · s_{j-1}` (coefficient `j` reduced mod
`p`). `Gamma_2 = |K|^R Σ_s N(s)² / C²` is the atom's normalized Rényi collision
excess (`def:primitive-logmoment`, L756), `C = |slice|`, `N(s)` the fiber count.

**The index `CONVENTION` (inherited from #422 §2.1, #428, #446).** Write
`#free = #{j : 1≤j≤R-1, p∤j}` and `#red = #{j : 1≤j≤R-1, p|j}`, so
`#free + #red = R-1`. The ambient Frobenius-and-head-constrained subgroups are

> `W_c^flat = { s ∈ K^R : s_0 ∈ F_p, s_{pj} = s_j^p for pj<R }`, dim `flat = 1 + k·#free`;  
> `W_c^0` = its **move/translation** subgroup, dim `w0 = [head_free] + k·#free`,

where `head_free = 1` iff the slice is signed with `p` odd (then `s_0 = Σ_t x_t`
ranges over all of `F_p`, so the fixed-weight slice is not confined to one
`s_0`-value) and `head_free = 0` otherwise (unsigned: `s_0 = a` pinned by the fixed
active count `a`). The **collision index** is

> `index := [K^R : W_c^0] = p^{kR - w0}`.

`fp_defect := flat − dim_{F_p} V_T` (with `V_T = span_{F_p}{v_t}`) is the shortfall
of the *actual* span from the flat ceiling; it is `N`/`T`-dependent (`MEASURED`,
#427/#428), not part of the closed forms proved here.

---

## 1. L1 — the differential `K`-rank defect law `PROVED`

> **Theorem L1.** Let `K = F_{p^k}`, let `T ⊆ K` consist of `N` distinct points,
> and let `R ≥ 1`. Put `E = { j-1 : 1≤j≤R-1, p∤j }` (the *surviving exponents*),
> `M = max E` (with `M = -1` if `E = ∅`). If `N ≥ M+1`, then
> `rank_K Span{v'_t : t∈T} = |E| = (R-1) − floor((R-1)/p)`.
> Consequently, if `N ≥ R` (so `min(N,R)=R`), the `K`-rank defect is
> `defect_K = R − rank = 1 + floor((R-1)/p)`.

**Proof.** Coordinate `j` of `v'_t` is `j·t^{j-1}`, where the integer coefficient `j`
is read in `F_p`. In `K^N` (rows indexed by `t∈T`) the `j`-th *column* of the matrix
`[v'_t]_{t,j}` is the vector `c_j = (j·t^{j-1})_{t∈T} = (j mod p)·(t^{j-1})_{t∈T}`.

*(i) Which columns survive.* `c_0 = 0` (coefficient `0`), and for `1≤j≤R-1`,
`c_j = 0` iff `(j mod p) = 0` iff `p | j`. So `c_j ≠ 0` exactly for the `#free`
indices `j` with `p∤j`, each a nonzero scalar multiple of the power vector
`u_{j-1} := (t^{j-1})_{t∈T}`. Scalars do not change the column span, so
`Span{v'_t} = span{u_e : e ∈ E}` with `E = {j-1 : 1≤j≤R-1, p∤j}`. This is the
char-`p` Wronskian phenomenon: the constant `W(1,X,…,X^{R-1}) = ∏_{i<R} i!` vanishes
iff some `i<R` has `p|i`, and the vanishing factors are exactly the coefficients
killed here (`D X^{pm} = pm·X^{pm-1} = 0`).

*(ii) The surviving columns are independent (Vandermonde on `E`).* Suppose
`Σ_{e∈E} c_e u_e = 0`, i.e. the polynomial `g(X) = Σ_{e∈E} c_e X^e` (degree `≤ M`)
vanishes at every `t ∈ T`. A nonzero polynomial of degree `≤ M` over a field has at
most `M` roots; since `|T| = N ≥ M+1` gives `N` distinct roots, `g ≡ 0`, hence all
`c_e = 0`. (Nothing here needs `0 ∉ T`: the argument is over evaluation at distinct
points, `t = 0` included or not.) So the `|E|` surviving columns are linearly
independent, and `rank = |E|`.

*(iii) Count.* `|E| = #{j : 1≤j≤R-1, p∤j} = (R-1) − #{j : 1≤j≤R-1, p|j} =
(R-1) − floor((R-1)/p)`. The defect statement follows when `N ≥ R`. ∎

**Exact hypotheses and sharpness.** The threshold is `N ≥ M+1` with
`M = max E ≤ R-2`, so `N ≥ R-1` is a clean uniform sufficient condition; the
verifier exhibits at `(F_9,R=3)` etc. that `N = M` drops the rank below `|E|`, so
the bound is sharp. Distinct points are required; `t=0` is admissible (it only adds
the constant column `u_0`, already present when `1∈E`, as one more Vandermonde row).

**Degenerate small `R`.** `R=1`: `E=∅`, `rank = 0`, `defect = 1` (the derivative of
a constant). `R=2`: `E={0}`, every `v'_t = (0,1)` is the *same* vector, `rank = 1`,
`defect = 1`. Both defects are the **trivial head kill** (`Span{v'_t} ⊆ {s_0 = 0}`);
the substantive char-`p` term `floor((R-1)/p)` first appears at `R = p+1` (when
`R-1 ≥ p`), i.e. `defect_K = 1` for `2 ≤ R ≤ p` and grows thereafter. The moment
columns, by contrast, have `defect 0` at every `R` (`prop:vandermonde-kills-low-rank`);
the verifier gates `mom_defect = 0` on all `55` swept configs.

### 1.1 Collision corollary — `Gamma_2 ≥ q^{defect_K}` and total collapse `PROVED`

> **Corollary L1a.** For any fixed-weight slice, `Gamma_2(v') ≥ q^{defect_K}`, where
> `q = |K|` and `defect_K = 1 + floor((R-1)/p)`.

**Proof.** Every differential syndrome `s'(x) = Σ_t x_t v'_t` is a `K`-linear
combination (coefficients `x_t ∈ {0,±1} ⊆ K`) of the columns `v'_t`, so it lies in
`Span_K{v'_t}`, a `K`-space of dimension `rank = R − defect_K`; hence the number of
distinct syndromes satisfies `n_occ ≤ |Span_K{v'_t}| = q^{R-defect_K}`. By
Cauchy–Schwarz over the `n_occ` occupied fibers,
`Σ_s N(s)² ≥ C²/n_occ`, so
`Gamma_2 = q^R Σ_s N(s)²/C² ≥ q^R/n_occ ≥ q^R/q^{R-defect_K} = q^{defect_K}`. ∎

> **Corollary L1b (total collapse, scoped).** `E = {0}` — equivalently the only
> surviving degree is the constant one — holds exactly when every `j ∈ [2,R-1]` is
> divisible by `p`, i.e. iff `R ≤ 2` (trivial) or `(p,R) = (2,3)`. In that case
> every `v'_t = (0,1,0,…,0)` is the same vector, so for a fixed-weight slice the
> syndrome `s' = (a mod p)·(0,1,0,…,0)` is **constant**: `n_occ = 1` and
> `Gamma_2 = q^R` (the strongest possible collision).

**Proof.** `E = {0}` iff the surviving `j`-set is `{1}` iff `p | j` for all
`2 ≤ j ≤ R-1`. For `p ≥ 3`, `j=2` is never divisible, so this forces `R ≤ 2`; for
`p = 2` it forces `{2,…,R-1} ⊆ 2ℤ`, i.e. `R ≤ 3`, giving `(2,3)` as the only
nontrivial case. Then all `v'_t` coincide, the fixed-weight slice sum is the single
value `(a mod p)·e_1`, so `N(s)` is `C` on one syndrome and `0` elsewhere, whence
`Gamma_2 = q^R·C²/C² = q^R`. ∎

This is exactly #446's `F16@R3` observation (`n_occ=1`, `Gamma_2 = q^R = 4096`),
here derived and scoped precisely: total collapse is a `p=2, R=3` (or trivial)
phenomenon, not a general law; the **general** law is the `Gamma_2 ≥ q^{defect_K}`
of L1a. The verifier gates both on `F16`/`F27`/`F5` census configs.

---

## 2. L2 — the Frobenius-index closed form `PROVED`

### 2.1 The subfield law (re-proved in one paragraph)

> **Lemma L2a (subfield law).** For any slice `x` valued in `F_p` and any `d ≥ 1`,
> `s_{p^d j} = Frob^d(s_j) = s_j^{p^d}` whenever `p^d j < R`; and `s_0 ∈ F_p`.

**Proof.** In char `p`, `Frob(a) = a^p` is a field automorphism, so it is additive:
`(a+b)^p = a^p + b^p`. Since `x_t ∈ F_p`, Fermat gives `x_t^p = x_t`. Hence
`s_j^p = (Σ_t x_t t^j)^p = Σ_t x_t^p (t^j)^p = Σ_t x_t t^{pj} = s_{pj}`. Iterating `d`
times gives `s_{p^d j} = s_j^{p^d}`. Taking `j=0`: `s_0^p = s_0`, so `s_0 ∈ F_p`
(the `Frob`-fixed subfield). ∎

This is the `c=1` case of #422 §2.1's projective `c`-form
(`s_{pj} = c^{1-p} s_j^p`) and the `d`-fold subfield law that #427 §4 verifies
exhaustively (`PROVED-AT-TOYS`, F16 `d=2`); re-proved here in one line rather than
imported. The verifier re-checks it on syndromes with **zero violations**: `F16u`
`d=1` (`140` checks) and `d=2` (`70`), `F27s`/`F9s`/`F25s` `d=1`.

### 2.2 The index closed form

> **Theorem L2.** For the moment columns over `K = F_{p^k}` with a fixed-weight
> prime-field slice, the achievable syndromes lie in a single coset of the move
> subgroup `W_c^0` (dim `w0 = [head_free] + k·#free`), and the collision index is
> the closed form
> `index = [K^R : W_c^0] = p^{ k·(1 + floor((R-1)/p)) − eps }`,  `eps = [head_free]`.
> Moreover `Gamma_2 ≥ index`.

**Proof.** *(Containment.)* By Lemma L2a the syndrome coordinates are constrained:
`s_0 ∈ F_p` and, for each reducible index `pj < R`, `s_{pj} = s_j^p` is a *function*
of the lower coordinate `s_j` (and, iterating, of a free coordinate via `Frob^m`).
Thus the achievable syndromes lie in `W_c^flat = {s : s_0∈F_p, s_{pj}=s_j^p}`, whose
free `F_p`-coordinates are `s_0` (one `F_p`-dimension) and the `#free` coordinates
`s_j` with `p∤j` (each a free element of `K`, i.e. `k` dimensions), and whose `#red`
reducible coordinates add nothing. Hence `dim_{F_p} W_c^flat = 1 + k·#free = flat`.
The differences of two same-weight syndromes lie in the translation subgroup
`W_c^0`; its head is free (`+1`) exactly when `head_free` (signed `p` odd, where a
single sign flip moves `s_0` by `2`, a unit of `F_p`, so `s_0` sweeps all of `F_p`)
and pinned otherwise, giving `dim_{F_p} W_c^0 = w0 = [head_free] + k·#free`.

*(Index count.)* `index = [K^R : W_c^0] = |K^R|/|W_c^0| = p^{kR}/p^{w0} =
p^{kR - w0}`. Now `kR − w0 = kR − [head_free] − k·#free = k(R − #free) − [head_free]`,
and `R − #free = R − (R-1-#red) = 1 + #red = 1 + floor((R-1)/p)`. So
`index = p^{k(1+floor((R-1)/p)) − eps}`.

*(Collision bound.)* The same-weight syndromes occupy at most `|W_c^0|` distinct
values (they sit in one `W_c^0`-coset), so `n_occ ≤ |W_c^0| = p^{w0}`, and
Cauchy–Schwarz gives `Gamma_2 ≥ q^R/n_occ ≥ q^R/p^{w0} = index` (this is #428
Theorem D at `c=1`). ∎

The verifier gates `index` (recomputed directly as `q^R // p^{w0}`) against the
closed form on **63** `(p,k,R,signed)` configs, `p∈{2,3,5}`, `k∈{1,2,3,4}`, and
reproduces #446's headline values exactly (§5).

### 2.3 Threshold corollary `PROVED`

> **Corollary L2b.** As a function of `R` (fixed `p,k,head_free`), `index` is
> **constant** `= p^{k − eps}` for `1 ≤ R ≤ p`, and **jumps by the factor `p^k`** at
> each `R = mp+1` (`m = 1,2,…`), where a new reducible coordinate `j = mp < R` enters.
> The **first** jump is at `R = p+1`.

**Proof.** `floor((R-1)/p)` is a step function of `R`: constant `= m` on
`mp+1 ≤ R ≤ (m+1)p`, incrementing by `1` exactly at `R = mp+1`. Since the exponent
of `index` is `k·(1+floor((R-1)/p)) − eps`, `index` is constant on each such block
and multiplies by `p^k` at each increment; the smallest increment point is
`m=1`, `R = p+1`. ∎

**Reading — follow the math, not the slogan.** #446's note phrases the effect as
"the index jumps at `R = p+1`," which is the **first** jump; the exact statement is
that it jumps at **every** `R ≡ 1 (mod p)`, each by `p^k`. #446's own gated JSON
already shows the later jumps (F27 `243 → 6561` at `R = 7 = 2·3+1`; F16 `4096 →
65536` at `R = 7 = 3·2+1`), so this is a sharpening of the prose, not a correction
of the data (§5). Note also the clean link to L1: the index exponent is exactly
`k·defect_K − eps`, where `defect_K = 1 + floor((R-1)/p)` is the **L1** differential
defect — the single count `1 + floor((R-1)/p)` (head `+` reducible coordinates)
governs both laws.

---

## 3. L3 — prime-field inertness `PROVED`

> **Theorem L3.** Over a prime field `K = F_p` (`k = 1`) with a signed fixed-weight
> slice, if `R ≤ p` then `index = 1` (the `F_p`-span cell is definitionally absent).
> The atom's deployed prime-field regime forces this: `T ⊆ F_p^×` gives `N ≤ p-1`,
> and `R ≍ N` gives `R ≤ N ≤ p-1 < p`, so `index = 1` at every reachable `R`.

**Proof (two routes).** *(a) From L2.* With `k = 1` and `R ≤ p`,
`floor((R-1)/p) = 0`, so `#red = 0`; with `head_free = 1` (signed, `p` odd) the L2
formula gives `index = p^{1·(1+0) − 1} = p^0 = 1`. *(b) Direct.* Over `F_p` the
`F_p`-span **is** the `K`-span, and `rank_K{v_t} = min(N,R)` is full by
`prop:vandermonde-kills-low-rank`, so `V_T` is `F_p`-nondeficient; equivalently, no
reducible coordinate is in range (`p | j` with `1≤j≤R-1` needs `j ≥ p ≥ R`, empty),
so the only Frobenius constraint `s_{pj}=s_j` never applies, `W_c^0 = K^R`, and
`index = 1`. The differential-locator map still carries the **trivial** head-kill
defect `defect_K = 1`, but its char-`p` term `floor((R-1)/p) = 0`, so there is no
low-defect cell either. ∎

> **Corollary L3a (honest boundary).** The hypothesis `R ≤ p` is load-bearing. If
> `R > p` were reached over `F_p` (necessarily with `R > N`, since distinct points
> in `F_p` number at most `p`, so outside the atom's `R ≍ N ≤ p-1` regime), the same
> formula gives `index = p^{#red} > 1`.

The verifier gates `index = 1` at **every** `R ≤ p` for `p ∈ {3,5,7,13}` (24 rows),
and gates the boundary `index = p^{floor((R-1)/p)} > 1` at `R = p+2` for each
(F3→3, F5→5, F7→7, F13→13). This matches #446 §6 exactly, which justified
immunity via "`T⊆F_p^×` forces `N≤p-1`, so `R≤N<p`"; the present statement makes the
`R ≤ p` hypothesis explicit (the task's shorthand "`index=1` at every `R`" is true
precisely in that forced regime).

---

## 4. Reproduction and the delta against PR #446 `MEASURED` / `AUDIT`

**Closed forms vs #446's measured values (verifier-gated, exact).**

| law | quantity | closed form | reproduces (all exact) |
|---|---|---|---|
| L1 | `rank_K Span{v'_t}` | `(R-1)-floor((R-1)/p)` | #446 §3 table (F16/F27 `R=3..5`); fresh grid `p∈{2,3,5}, k∈{1,2,3}, R≤10` |
| L1 | `defect_K` | `1+floor((R-1)/p)` | #446 §3 `defect_K` col; §6 prime `defect_K=1` |
| L1a | `Gamma_2(v')` | `≥ q^{defect_K}` | #446 §3 `Gamma_2 ≥ q^{defect_K}`; total collapse `F16@R3` `n_occ=1, Gamma_2=4096=q^R` |
| L2 | `index` | `p^{k(1+floor((R-1)/p))-eps}` | **F27 `9→243`** (`R=3→4=p+1`), **F16 `16→256`** (`R=2→3=p+1`), F27 `R7=6561`, F16 `R5=4096`, `R7=65536` |
| L2a | subfield law | `s_{p^d j}=s_j^{p^d}` | #427 §4 (F16 `d=2`, `0` viol); here `0` viol on 5 configs, up to `1120` checks |
| L3 | `index` (F_p) | `1` for `R≤p` | #446 §6 F5/F7/F13 immunity, exact |

**Three prose sharpenings against #446's note (each consistent with #446's gated
JSON) `AUDIT`.** No law changed; these refine the wording:

1. **L2 threshold.** #446 says "index jumps at `R=p+1`." Exact: it jumps at **every**
   `R = mp+1` by `p^k` (Corollary L2b); `R=p+1` is the first. #446's JSON already
   contains the later jumps (F27 `R7`, F16 `R7`), so this sharpens prose only.
2. **L3 hypothesis.** "index=1 at every `R`" carries the load-bearing hypothesis
   `R ≤ p` (Corollary L3a); #446 §6's own reasoning ("`R≤N<p`") already supplies it,
   so this makes the shorthand precise rather than correcting it.
3. **`fp_defect` stays `MEASURED`.** The **index** is a closed form (proved here); the
   **`fp_defect`** (`flat − dim_{F_p} V_T`, how far the actual span falls short of
   the ceiling) is `N`- and `T`-dependent and is *not* a closed form — e.g. #446 F27
   `R=6` reads `fp_defect = 2` at `N=14` (its §2 control) and `fp_defect = 3` at
   `N=10` (its §4 census), both correct at their `N`. So `fp_defect` correctly
   remains `MEASURED` (the occupancy question, #427/#428); only the ambient index and
   the differential defect are promoted. #446's note §5 prose mixed the two `N`s in
   one column — a cosmetic imprecision, not a law error; its JSON is consistent.

**Net verdict: all three PR #446 laws are correct and now PROVED; zero corrections.**

---

## 5. Cross-validation `MEASURED` (of the proofs, against exhaustive computation)

The verifier recomputes and gates, under `ulimit -v 2 GB` best-effort, small fields
only (every cap reported in the PASS line):

- **L1 rank/defect:** `55` configs, `p∈{2,3,5}`, `k∈{1,2,3}` (`q ≤ 125`), `R ≤ 10`,
  `N ≤ 24`; measured `deriv_rank == (R-1)-floor((R-1)/p)` and
  `defect_K == 1+floor((R-1)/p)` on every one; `mom_defect == 0` on every one.
- **L1 `|T|` threshold:** `36` configs — full derivative rank exactly when
  `N ≥ max(E)+1`, and strictly below when `N = max(E)`.
- **L2 index:** `63` configs (adds `k=4` for the F16 headline); direct
  `q^R // p^{w0}` equals the closed form on every one; block-constancy and the
  `×p^k` jump at each `R=mp+1` gated on F27/F16/F125.
- **L2 subfield law:** `5` exhaustive slice censuses, `0` head + `0` Frobenius
  violations (`140`/`70`/`1120`/`160`/`160` checks).
- **L3:** `24` inert rows (`index=1`, `R≤p`) + `4` boundary rows (`index=p^{#red}>1`).
- **Collision:** `7` census configs, `Gamma_2 ≥ q^{defect_K}` on every one; total
  collapse `n_occ=1, Gamma_2=q^R` at `F16@R3`.
- **Caps:** census (the only exponential step) held to `N ≤ 10`, `a ≤ 4`; largest
  field `F_125`; peak RSS ~15 MB, wall ~0.1 s (both environment-specific, not gated).
- **Dual path:** table multiply == log/antilog on `F_27, F_16, F_125` (`0` mismatch).
- **Tampers:** `7/7` corruptions caught through the live gates (retracted).

---

## 6. Labels, Nonclaims, Weave `AUDIT`

**Per-claim labels.**

- `PROVED` — L1 (rank `(R-1)-floor((R-1)/p)`, defect `1+floor((R-1)/p)`, exact `|T|`
  hypothesis, degenerate `R≤2`); L1a (`Gamma_2 ≥ q^{defect_K}`); L1b (total collapse
  scoped to `(p,R)=(2,3)`/trivial); L2a (subfield law, one-line Frobenius); L2
  (`index = p^{k(1+floor((R-1)/p))-eps}`, containment + count + `Gamma_2 ≥ index`);
  L2b (jumps at every `R=mp+1`); L3 (`index=1` for `R≤p`) and L3a (boundary
  `p^{#red}>1`). Each is a complete argument over arbitrary `p,k,R` and is gated
  against exhaustive computation on a finite grid.
- `MEASURED` (unchanged, cited, **not** promoted) — the *occupancy* question: whether
  `V_T` fills `W_c` (i.e. `fp_defect=0`), and the exact `Gamma_2`/occupancy values,
  remain toy measurements with #427/#428/#446; only the ambient index, the
  differential defect, and their Cauchy–Schwarz collision bounds are proved here.
- `OPEN` — the asymptotic promotion (any `N,R→∞` reading), untouched.

**Nonclaims.**

- This note is an **experimental-lane result; no promotion without review.** It does
  **not** prove or refute `prob:entropy-inverse-q`, does **not** resolve
  `prob:row-sharp-q` / `def:q-row-atom`, and does **not** claim the L839 removal list
  is complete or incomplete — it proves three structural facts about the column
  geometry that #446 measured.
- **No deployed-row claim of any kind:** nothing here certifies a deployed finite
  safe row, instantiates any `U(a_0+1) ≤ B*` certificate, or touches a finite row.
  The deployed KoalaBear / Mersenne-31 rows are prime-field with `R ≍ N ≤ p-1 < p`,
  hence inert twice over by L3 (no `F_p`-span cell) and L1 (`floor((R-1)/p)=0`, no
  char-`p` differential low-defect). Asymptotic/experimental lane only.
- The differential-locator `K`-defect (L1) is a firing of alternative (b) for the
  **removed** differential-locator cell `v'_t` (L839), **not** for the admissible
  moment curve `v_t` (which stays `rank_K`-full, `prop:vandermonde-kills-low-rank`);
  it lands in alternative (a) and validates the removal, exactly as #446 states.
- `head_free`/`eps`, the `firstN` domain, signed-vs-unsigned, and the config grid
  are conventions; the closed forms (L1 rank, L2 index, L3 inertness) are exact and
  robust to any `O(1)` choice.

**Weave (credit by PR number).**

- **PR #446** (`thresholds-atom-toy-r-gt-w`, `atom_toy_r_gt_w.md`) — direct
  predecessor: broke the `R=w` wall and **measured** L1 (§3, `defect_K=1+floor((R-1)/p)`),
  L2 (§2/§4 index sweep) and L3 (§6 prime immunity). This packet proves all three at
  arbitrary `p,k,R` and reproduces its headline numbers (`9→243`, `16→256`, `4096`,
  `65536`, total collapse `4096`) exactly; three prose sharpenings in §5, no
  correction.
- **PR #422** (`cap25_v13_entropy_inverse_fp_span_cell.md`) — the `F_p`-span cell
  mechanism and the subfield law's projective `c`-form one-line proof (§2.1),
  re-proved here at `c=1` (L2a) and used for the L2 containment and index.
- **PR #427** (`cap25_v13_entropy_inverse_fp_span_codim_census.md`) — the census
  packet; its §4 per-subfield law `s_{p^d j}=Frob^d(s_j)` (`PROVED-AT-TOYS`,
  exhaustive F16 `d=2`) is the `d≥1` form of L2a, re-checked here (`0` violations).
- **PR #428** — the image-structure theorem (`Gamma_2 ≥ index·p^{defect}`, occupancy
  `p^{-defect}`); its `c=1` containment bound `Gamma_2 ≥ index` is L2's collision
  clause, and `Gamma_2 ≥ q^{defect_K}` (L1a) is its differential analog.
- **PR #420/#421** (`toy_dichotomy` / `missing_cell_hunt`) — named the `R=w` wall
  whose break #446 built and this packet's laws live past. **PR #429/#430** —
  connectivity band / residual controls, unaffected.
- This packet consumes no upper cell and instantiates no `U(1116048)` certificate.
