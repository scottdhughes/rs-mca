# Instantiation examples for the proof objects of `asymptotic_rs_mca.tex`

Status: `REFERENCE` (this section, the steering quote, and every paper
definition/theorem below, quoted verbatim with line refs) / `CONVENTION`
(every leaf's `K,N,m,R,rho`, the Sidon-heavy/high-energy `Delta` thresholds,
the E4 row-family `(rho,beta,n)`, and the E5 toy's `p,k,w,alpha` are stated
parameter choices, not theorems) / `MEASURED` (every table — fiber censuses,
moments, additive energies, `g*` values, E5's polynomial identities — is an
exact recomputation, gated by the verifier below).

**Verifier:** `experimental/scripts/verify_asymptotic_proof_examples.py`
(zero-arg, stdlib-only, self-contained; `RESULT: PASS (548/548 checks)`,
~13 s / ~38 MB peak RSS on the authoring box; best-effort `RLIMIT_AS` guard
via `APEX_AS_CAP_GB`, default 2 GB; `APEX_DATA_DIR` overrides the data
location, default `experimental/data/`). It **recomputes from scratch**
every number below — the finite-field census, exact big-integer moment
sums, exact `O(|F|^2)` additive-energy convolution (dual-checked against an
exact `O(|F|^4)` 4-tuple count when `|F|<=25`), `g*` bisections (tol
`1e-12`), and the E5 polynomial arithmetic over `F_97` — then gates every
number against the committed
`experimental/data/asymptotic_proof_object_examples.json` (exact on
ints/bools/strings/lists, `1e-9` relative on floats), and ends with **seven**
tamper self-tests.

## What this is / is not

Built directly from the steering's own scope, quoted verbatim (`agents.md` @
`eb42b82`, "Highest priority now" item 3, repeated as work target `C0`):

> "Final computations and examples. Produce small and medium examples that
> instantiate the proof objects: bad-line moduli strata, structured cases,
> primitive Boolean prefix fibers, Fourier/Sidon cuts, and the entropy
> threshold. These examples are for auditing and exposition, not for
> replacing the proof."

Every table below is exactly one of those named objects, computed exactly
(exhaustive enumeration or exact bisection) at toy scale, verifier-gated.
This note is **not** a proof or partial proof of any labeled statement in
`asymptotic_rs_mca.tex` and certifies **no** deployed finite row. Several
captions below say explicitly where a toy cannot literally test an
`o(N)`/`exp(o(N))` clause and report the finite analogue instead.

## Weave

- **The paper.** `experimental/asymptotic_rs_mca.tex` (346 lines, read in
  full): `def:primitive-leaf` (L148–158), `lem:moment-max` (L165–178), the
  Sidon cut (section 3, L180–208: `def:sidon-paid` L196) and Boolean
  additive combinatorics (section 4/`sec:bsg`, L210–242: `thm:quasicube`
  L220, `prop:no-high-energy` L228), the entropy envelope `g*(rho,beta)`
  (Statement section, L71–75), `def:cells` (C1) (L91–92), and the
  identity-prefix pole construction (L276–287).
- **Steering `agents.md` @ `eb42b82`.** Priority-3 quote above; the fast
  orientation section calls finite rows "a separate constants and
  certificate project" now, i.e. this packet is audit/exposition of the
  *asymptotic proof's objects*, not a row certificate.
- **PR #433** (`przchojecki/rs-mca`, `audit: asymptotic_rs_mca closed-ledger
  citations`, OPEN). Machine-verified that the two moduli manuscripts cited
  for cell (C9) (`Cho26ModuliSelf`, `Cho26ModuliFinal`) are **absent from the
  repository**, and that the steering's own expected path
  `experimental/rs_mca_moduli_ledger_final.tex` is likewise absent — informs
  the "not instantiable" item below.
- **PR #434** (`przchojecki/rs-mca`, `thresholds: M31 signed-e_m inverse —
  Chebyshev-domain reformulation`, OPEN, sibling timing). Independent
  concurrent work on the finite row-sharp-Q crux (`prob:row-sharp-q`, one
  deployed row's effective-support bound); no content overlap with this
  packet's asymptotic-object toys — noted as the requested concurrent-work
  weave.
- **The fp-span-cell lineage.** `experimental/scripts/verify_entropy_inverse_fp_span_cell.py`
  (PR #422, integrated) supplies the copied machinery — the `GF` class,
  `build_T`/`build_rho`/`moment_columns`, and the unsigned fixed-weight
  census pattern, here extended to `census_members` (retains fiber
  membership, needed for E3's per-fiber energy, absent from the original).
  E1 independently rediscovers that note's char-2 Frobenius
  coordinate-collapse law in a new (unsigned, fixed-`m`) slice.

## E1 — primitive Boolean prefix fibers (`def:primitive-leaf`, L148–158)

Four leaves: `T=build_T(K,N)`, `N=16`, `m=8` (`m/N=0.5`, bounded away from
`0,1`), columns `v_t=rho(t)*(1,t,...,t^{R-1})`, active family
`Omega^circ={x in {0,1}^T: sum x_t=m}` taken in full (no other first-match
cells to remove it from at this toy, so the "residual slice" is the whole
fixed-weight slice — a stated toy simplification), `Phi(x)=sum x_t v_t`,
`L=|im Phi|`, `Nbar=M/L`, `M=C(16,8)=12870`. Two weights per leaf: `ones`
(`rho==1`) and a deterministic `twist` (seed `12345`).

| leaf | `K` | `R` | `rho` | `L` | `Nbar` | `max\|F_s\|` | `max/Nbar` | `log(Nbar)/N` | top-5 `\|F_s\|` |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| F16-R3 | `F_16` | 3 | ones  |    16 | 804.375 | 870 | **1.082** | 0.4181 | 870,800,800,800,800 |
| F16-R3 | `F_16` | 3 | twist | 3856 |   3.338 |   7 | **2.097** | 0.0753 | 7,7,7,7,7 |
| F16-R4 | `F_16` | 4 | ones  |   256 |  50.273 |  72 | **1.432** | 0.2448 | 72,72,72,72,72 |
| F16-R4 | `F_16` | 4 | twist | 12870 |   1.000 |   1 | **1.000** | 0.0000 | 1,1,1,1,1 |
| F27-R3 | `F_27` | 3 | ones  |   729 |  17.654 |  24 | **1.359** | 0.1794 | 24,24,24,24,24 |
| F27-R3 | `F_27` | 3 | twist | 9204 |   1.398 |   5 | **3.576** | 0.0210 | 5,5,5,5,5 |
| F49-R3 | `F_49` | 3 | ones  |  2300 |   5.596 |  17 | **3.038** | 0.1076 | 17,17,17,17,17 |
| F49-R3 | `F_49` | 3 | twist | 12036 |   1.069 |   3 | **2.806** | 0.0042 | 3,3,3,3,3 |

**`Q` holds numerically at every leaf** (`MEASURED`): `max_s|F_s|/Nbar` is a
small constant (`1.00`–`3.58`) at all eight rows, nowhere near the trivial
ceilings `L` (no collisions) or `M` (total collapse). A single finite `N`
cannot literally test `max_s|F_s| <= exp(o(N))*Nbar` (no sequence to take
`o(N)` along at one point); what's shown is the finite analogue.

**`F16-R3` reproduces the fp-span-cell note's Frobenius law as a coordinate
collapse** (`MEASURED`): with `rho=ones`, `s_0=sum_t x_t=m` is forced
constant (pinned to a single value here, since `m` itself is fixed across
the slice — stronger than that note's signed-slice head-pin). In
characteristic 2, Frobenius is additive, so `s_2=(sum x_t t)^2=s_1^2`
**exactly**: `R=3` has one free coordinate, so `L<=16`, and the verifier
confirms `L==16` on the nose (gated `e1.frobenius_collapse.F16_R3.L_eq_q`) —
total collapse. At `R=4` the extra coordinate `s_3` is Frobenius-free (`3`
odd), giving `L=256=16^2`, matching that note's `free={1,3}`,`red={2}` split
at `p=2,R=4` exactly. `F27`/`F49` get no red column at `R=3` (`3,7` divide
neither `1` nor `2`), so only the milder head-pin applies — explaining the
leaf-to-leaf spread above from a different (unsigned, fixed-`m`) slice shape.

`R=5` is omitted: for all three fields at `N<=16`, the effective ambient
`K^{R-1}` already exceeds `C(16,8)=12870`, so no leaf collides at `R=5` under
`rho=ones` (would print the vacuous `L=M`, `Nbar=1`) — the same `R log|K| ~
N` tension the fp-span note's §3 normalization audit found from the other
direction.

## E2 — moment-max equivalence (`lem:moment-max`, L165–178)

Leaf `F49-R3, rho=ones` (`M=12870, L=2300, Nbar=5.5957, max|F_s|=17`, target
`max/Nbar=3.0381`). `Gamma^ord_q=L^{-1} sum_s (|F_s|/Nbar)^q`, via exact
big-integer numerator/denominator (`Gamma_q=L^{q-1}*sum(|F_s|^q)/M^q`),
converted to `float` once at the end; the lemma's two-sided squeeze is
checked as an **exact cross-multiplied integer inequality** at every `q`.

| `q` | lower `L^{-1}(max/Nbar)^q` | `Gamma^ord_q` | upper `(max/Nbar)^q` | squeeze | `Gamma_q^{1/q}` |
|---:|---:|---:|---:|---|---:|
|  2 | `4.013e-03` | `1.4035e+00` | `9.2299e+00` | exact | 1.1847 |
|  4 | `3.704e-02` | `4.2927e+00` | `8.5191e+01` | exact | 1.4394 |
|  8 | `3.155e+00` | `9.7435e+01` | `7.2575e+03` | exact | 1.7725 |
| 16 | `2.290e+04` | `2.5618e+05` | `5.2671e+07` | exact | 2.1779 |
| 32 | `1.206e+12` | `9.8712e+12` | `2.7742e+15` | exact | 2.5473 |

`Gamma_q^{1/q}` climbs `1.18 -> 1.44 -> 1.77 -> 2.18 -> 2.55` monotonically
toward `max/Nbar=3.038` as `q=2..32` (gated `e2.squeeze_monotone`), staying
below the target throughout (`e2.squeeze_below_target`) — the "moment
converges to max" squeeze, exhibited at one toy leaf.

## E3 — Fourier/Sidon cut (sections 3–4, L180–242)

For each leaf's five largest `rho=ones` fibers (subsets of `{0,1}^T subset
Z^T`): exact `E(F)=#{(a,b,c,d) in F^4: a-b=c-d}` via the difference-multiset
identity `E(F)=sum_d r(d)^2` (`O(|F|^2)`), dual-checked against exhaustive
`O(|F|^4)` when `|F|<=25`. `Delta(F)=E(F)/|F|^3`. **Convention**
classification: `Sidon-heavy` if `Delta<=0.2`, `high-energy` if `Delta>=0.5`,
else `mixed` (the paper's own thresholds are asymptotic and cannot be
literally instantiated at one finite `N`).

| leaf (rank 0) | `\|F\|` | `E(F)` | `Delta` | `\|F-F\|` | class | dual `O(n^4)` |
|---|---:|---:|---:|---:|---|---|
| F16-R3 | 870 | 9,858,330 | 0.01497 | 180,771 | sidon-heavy | skipped (`\|F\|>25`) |
| F16-R4 | 72  | 15,336    | 0.04109 | 2,593   | sidon-heavy | skipped |
| F27-R3 | 24  | 1,200     | 0.08681 | 521     | sidon-heavy | **matches** |
| F49-R3 | 17  | 577       | 0.11744 | 265     | sidon-heavy | **matches** |

**No naturally-occurring census fiber reaches high-energy** (gated
`e3.no_high_energy.*`): all 20 examined fibers classify `sidon-heavy`,
including the packet's single largest fiber (`F16-R3` rank 0, `|F|=870`,
`6.8%` of `M`) — large **and** additively flat, not large **and**
structured. Since the census never populates the high-energy corner at this
scale, an exact **synthetic reference family** pins it directly:

| set | `\|F\|` | `Delta` | class |
|---|---:|---:|---|
| singleton | 1 | **1.00000** | high-energy (`Delta=1` forces `\|F\|=1` — `Z^N` is torsion-free, no nontrivial finite subgroup coset) |
| pair | 2 | 0.75000 | high-energy (universal: `Delta=0.75` for **any** 2-point subset of `Z^N`) |
| cube-`d1..d6` | `2^d` | `0.75^d`: 0.750,0.5625,0.4219,0.3164,0.2373,**0.1780** | high-energy `->` mixed `->` **sidon-heavy** at `d=6` |

(`cube-d` = product-cube `{0,1}^d x {0}^{N-d}`, energy multiplying
coordinatewise.) The synthetic family alone exhibits the crossover
(`Delta` strictly falling `1 -> 2 -> 4 -> ... -> 64`, leaving high-energy by
`d=3`, entering Sidon-heavy by `d=6`), and the real fibers (`|F|` in the
hundreds) extend the trend further. **Every one of the 28 instances**
satisfies the quasicube bound exactly (`thm:quasicube`, integer inequality
`|F-F|^2>=|F|^3`, gated `e3.quasicube.*`) — e.g. `F16-R3` rank 0 has
`|F-F|=180771` against `|F|^{1.5}=25661.31`, and the singleton achieves the
degenerate floor `|F-F|=1=1^{1.5}` exactly.

## E4 — entropy threshold `g*(rho,beta)`

`H2(x)=-x log2 x-(1-x)log2(1-x)`; `g*(rho,beta)=sup{g in [0,1-rho]:
H2(rho+g)>=beta*g}` by bisection to `1e-12` (the feasible set is `[0,g*]`
since `g |-> H2(rho+g)-beta*g` is concave, `>=0` at `g=0`, `<0` at `g=1-rho`
— asserted at every grid point before bisecting).

| `beta \ rho` | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.7072 | 0.6383 | 0.5666 | 0.4925 | 0.4160 | 0.3375 | 0.2568 | 0.1740 | 0.0888 |
| 2 | 0.4886 | 0.4616 | 0.4246 | 0.3800 | 0.3295 | 0.2737 | 0.2131 | 0.1478 | 0.0775 |
| 3 | 0.3284 | 0.3323 | 0.3195 | 0.2956 | 0.2632 | 0.2239 | 0.1782 | 0.1264 | 0.0680 |
| 4 | 0.2283 | 0.2480 | 0.2483 | 0.2364 | 0.2154 | 0.1869 | 0.1515 | 0.1095 | 0.0603 |
| 8 | 0.0869 | 0.1119 | 0.1228 | 0.1248 | 0.1198 | 0.1088 | 0.0922 | 0.0698 | 0.0406 |

Every value satisfies `|H2(rho+g*)-beta*g*|<1e-9` (gated `e4.root.*`) — a
genuine root, not a placeholder.

**Frontier crossing, one row family** (`rho=0.5,beta=2,n=120`,
`k=round(rho*n)=60`, `g*=0.329464`, `n*g*=39.536`). Tabulating exactly
`log2(Nbar_{n,a})/n=[log2 C(n,a)-w*beta]/n` (exact binomial, `a=k+1+w`)
against the closed form `H2(rho+g)-beta*g`, `g=w/n`:

| `w` | `g` | `log2(Nbar)/n` (exact) | `H2(rho+g)-beta*g` (closed form) |
|---:|---:|---:|---:|
| 37 | 0.3083 | +0.04219 | +0.08828 |
| 38 | 0.3167 | **+0.00744** | +0.05398 |
| 39 | 0.3250 | **−0.02799** | +0.01902 |
| 40 | 0.3333 | −0.06412 | **−0.01664** |
| 41 | 0.3417 | −0.10100 | −0.05303 |

The **exact** quantity flips sign between `w=38,39` (`g in (0.317,0.325)`);
the **closed form** flips between `w=39,40`, i.e. at `g*=0.3295` exactly, by
construction. The exact curve sits uniformly below the closed form (the
standard Stirling correction to `log2 C(n,a)` vs `n*H2(a/n)`), so the finite
flip leads the idealized `g*` slightly — precisely the theorem's own
`+o(1)`. Sweeping `n`:

| `n` | empirical flip `g` | `\|gap\|` to `g*=0.329464` |
|---:|---:|---:|
| 120 | 0.32500 | 0.00446 |
| 600 | 0.32833 | 0.00113 |
| 3000 | 0.32900 | 0.00046 |
| 15000 | 0.32933 | 0.00013 |

the gap shrinks monotonically (gated `e4.family.gap_shrinks`): the finite
crossing converges to `g*` as `n` grows — the content behind "+o(1)."

## E5 — structured-case spot example: the (C1) mechanism only

**Exposition of the mechanism, not a payment verification of any row or cell
budget.** `def:cells` (C1), verbatim: "Quotient-pullback cells. The support
or locator descends along a nontrivial finite map `D -> D'`." Toy: `D` = the
order-16 subgroup of `F_97^*` (`p=97`, `96=2^5*3`), squaring map
`phi(x)=x^2`, image `D'=phi(D)` the order-8 subgroup:

```
D  = [1, 8, 12, 18, 22, 27, 33, 47, 50, 64, 70, 75, 79, 85, 89, 96]
D' = [1, 22, 33, 47, 50, 64, 75, 96]     (8 fibers {d,-d}, e.g. {1,96},{8,89},...)
```

`D` is closed under negation (`-D=D`, `MEASURED`), so `phi` is exactly 2-to-1
with fibers `{d,-d}`. Take `k=3,w=2,m=k+1+w=6` (the paper's `a_n=k_n+1+w_n`
convention) and build the bad-line witness support `S` as a **union of 3
whole fibers** (`{1,96},{8,89},{12,85}`), manifestly a pullback along `phi`:

```
S = [1, 8, 12, 85, 89, 96]                       (|S| = 6 = m)
ell_S(X)     = 96 + 15 X^2 + 82 X^4 + X^6        (odd coefficients exactly 0)
tilde_ell(Y) = 96 + 15 Y + 82 Y^2 + Y^3          (locator of S' = phi(S) = {1,47,64})
```

**The locator genuinely descends**: `ell_S(X)==tilde_ell(X^2)` exactly
(gated `e5.locator_descends`) — the defining content of a quotient-pullback
support. Applying the paper's identity-prefix pole construction (L276–287)
at pole `alpha=0 not in D`: build `U_z(X)=X^6+82X^4` by copying `ell_S`'s own
top `w+1=3` coefficients and zeroing the rest (`U_z` genuinely differs from
`ell_S` below the prefix, gated `lower_differs`). Then

```
zeta_bad = U_z(alpha) - ell_S(alpha) = 0 - 96 = 1   (mod 97, nonzero)
```

and **exact verification** that `f_alpha(x)=U_z(x)/(x-alpha)`,
`g_alpha(x)=-1/(x-alpha)` satisfy `f_alpha(x)+zeta_bad*g_alpha(x)=h(x)` at
**every** `x in S`, for the genuine low-degree witness `h(X)=82*X` (degree
`1<k=3`; `(U_z-ell_S-zeta_bad)/(X-alpha)` has **exact zero remainder**,
gated `e5.h_rem_zero`). Separately `g_alpha` itself is **not** explained by
any degree-`<k` polynomial on `S`: the degree-`<3` interpolant through the
first 3 points of `S` disagrees with `g_alpha` at **all 3** remaining points
(gated `e5.g_alpha_not_explained`) — so `(r_1,r_2)=(f_alpha,g_alpha)` at
slope `gamma=zeta_bad=1` is a genuine MCA-bad witness (Statement section,
L60–65) whose support descends along the quotient map by construction.

**Toy budget arithmetic** (illustrative only — **not** a claim about any
row's paid-cell budget): possible quotient-pullback supports at this
`(n,m)` number `C(n/2,m/2)=C(8,3)=56` (choices of 3 fibers out of 8), against
the raw count `C(n,m)=C(16,6)=8008` — a `143x` shrinkage
(`raw_budget/c1_budget=143.0`, gated `e5.budget_shrinks`): the toy shape of
why a first-match cell that only answers for descending supports is
typically far cheaper than the raw count, not a computation of any real
row's `(C1)` payment.

## Not instantiable: "bad-line moduli strata"

Not instantiated: the moduli manuscript(s) cell (C9) cites (`Cho26ModuliSelf`,
`Cho26ModuliFinal`) are absent from the repository, and PR #433
machine-verified this and named the steering's own expected path,
`experimental/rs_mca_moduli_ledger_final.tex`, as likewise absent at
`eb42b82`. There is no in-tree moduli-strata object to instantiate a small
example of; fabricating one would misrepresent an absent source as present.
Moving on per the task's own instruction.

## Guards and verification

The verifier recomputes every table above from scratch and gates it against
the committed JSON (`RESULT: PASS (548/548 checks)`, ~13 s, ~38 MB RSS on
the authoring box — environment-specific, not gated). Structural
cross-checks beyond the raw data gate: `Q` holds numerically at all 8 E1
rows; the E1 Frobenius collapse (`L==16` exactly, `F16-R3`); the E2 squeeze
is monotone and stays below target at every `q`; no census fiber reaches
high-energy in E3 while the synthetic family does, and all 28 E3 instances
pass the exact quasicube inequality; every E4 grid point is a genuine root
to `1e-9` and the row-family flip sits within `0.02` of `g*`; the E5 support
closure, locator descent, pole-construction identity, and
non-explainability of `g_alpha` alone all check out exactly.

**Seven tamper self-tests**, each independently confirmed caught: (1) a
faked `L+1` desyncs `Nbar`; (2) a fake `max/2` collapses the E2 upper bound
below the true `Gamma_32`; (3) a corrupted E3 pairwise-difference count
breaks the `O(n^2)`-vs-`O(n^4)` dual path; (4) a too-small fake `|F-F|=2`
breaks the quasicube inequality for any real fiber; (5) perturbing `g` by
`0.01` off `g*` breaks the root equation by orders of magnitude; (6)
replacing one element of `S` by a non-paired point breaks locator descent;
(7) a wrong `zeta` breaks the pole-construction identity's zero remainder.

## Nonclaims

- Proves nothing about, and closes no gap in, any labeled statement of
  `asymptotic_rs_mca.tex` — `thm:frontier`, `thm:closed-ledger-package`,
  `thm:primitive-q`, `def:sidon-paid`, `prop:no-high-energy` are quoted and
  instantiated at toy scale only, never proved or extended here. E1–E4
  exactly instantiate definitions/lemmas already proved in the paper; the
  toy numbers illustrate the objects, not independent evidence for the
  paper's open reduction (audited separately by PR #433) or `thm:frontier`.
- E3's classification thresholds and E1's field/size choices are this
  packet's own conventions, not paper values; the paper's own thresholds are
  asymptotic (`Delta<=e^{-sigma N}`) and cannot be literally instantiated at
  one finite `N`. No toy here is claimed to satisfy the paper's printed
  asymptotic side conditions (e.g. `log|Omega^circ|-R log|K|=o(N)`)
  literally — a single finite instance cannot satisfy or falsify an
  asymptotic clause; each section states the finite analogue actually
  checked.
- E5 is a mechanism illustration for cell (C1) only — no computation,
  bound, or estimate of any real row's `(C1)` payment, no touch on
  `prob:row-sharp-q`, no certificate of any kind; see PR #434 for the actual
  open finite-row work this packet deliberately does not duplicate.
- Machinery is copied, not imported, from
  `experimental/scripts/verify_entropy_inverse_fp_span_cell.py`, per this
  repository's standalone-verifier convention; this note does not modify or
  supersede that script or its note.
