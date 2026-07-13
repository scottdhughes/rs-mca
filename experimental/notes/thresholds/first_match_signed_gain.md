# First-match pruning bounds the signed q-gain: a two-sided q-window theorem on the superincreasing family

## Status

```text
Status: PROVED (two-sided q-window separation, route-scoped) + PROVED core
        lemmas + route-cut COUNTEREXAMPLE (large-q all-signs) + EXPERIMENTAL
        residual (indicator beyond q_+).
HARD INPUT 2 SERVED: "image-scale MI + MA, or a direct Sidon payment"
        (agents.md L47/L67) -- the signed-minor clause of avdeevvadim's #716
        charge-preserving semantic-or-signed dichotomy, ON ONE FAMILY.
Verdict (route-scoped): on the depth-1 superincreasing family, first-match
        pruning is EXACTLY the clause that bounds the signed q-gain. For every
        complete dyadic band A, every q>=2, and every signed sub-mask on the
        pruned support, the band-excess R_A is bounded by an explicit
        L^{3/2-1/q}/M (Theorem I); it -> 0 for 2<=q<q_+=4.199. On the SAME
        family the UNPRUNED (full-multiplicity) mask has R_A -> infinity for
        q>q_-=2.709 (Theorem II). So for q in the window (q_-,q_+) ={3,4}
        (integer) the pair (pruned bounded / unpruned growing) is a THEOREM,
        not evidence (Theorem III). The all-signs bound is route-scoped: at
        q -> infinity the sign-aligned pruned excess grows (Theorem IV).
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**. Every number below is recomputed
by `experimental/scripts/verify_first_match_signed_gain.py` (stdlib only,
deterministic, `RESULT: PASS (215/215)`, `--tamper-selftest` catches `6/6`,
~14 s). Machine-readable certificate:
`experimental/data/certificates/first-match-signed-gain/first_match_signed_gain.json`.
No `.tex`/`.pdf` is edited.

## Interfaces

- **avdeevvadim's #716** (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`,
  `experimental/notes/audits/arbitrary_mask_idempotent_guardrail_v1.md`). The
  normalized q-gain and the projection machinery are his and are replicated
  exactly: band excess `R_A(f)=(L^{1-1/q}/M)||P_A f||_q` (barrier Prop 1.1),
  census gain `||P_A f||_q/C^{1/q}` (guardrail-script normalization),
  `K_A(x)=(1/C) sum_{xi in A} chi_xi(x)`, `P_A f=K_A*f`. This packet proves the
  **signed-minor clause** of his Sec-6 *charge-preserving semantic-or-signed
  dichotomy* on the concrete family: the signed-packet charge requirement
  `c_i <= e^{o(N)} M/L^{1-1/q}` is precisely `R_A(g) <= e^{o(N)}`, which
  Theorem I establishes (all bands, all signs) for `q<q_+`.
- **#717** (`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`).
  The family (Sec 7: `A_i=5^i`, `C=2 sum A_i+1`, `T={A_i} u {C-A_i}`, `a=B`,
  `Phi=sum` over `Z_C`), the complete dyadic `|tau|` band decomposition and
  `R_A` (Sec 1), and the whole-residual band-failure identity (Lemma 2.1) are
  #717's. Theorem II is its Lemma 2.1 instantiated at the heavy fiber `s0=0`.
- **#723** (`experimental/notes/thresholds/signed_minor_payment_clause_census_v1.md`).
  The measured mechanism this packet turns into a theorem: in the dense regime
  ONLY ablating clause (iii) (first-match) restores absolute gain growth. The
  census's exact q=4 dense values are reproduced here to all printed digits:
  pruned (its "B") `0.404/0.354/0.209`, unpruned (its "C_iii") `0.539/0.768/0.842`.
  Theorems I+III are the theorem form of that census.

## 1. Family, occupied set, pruning notion, conventions

`B` even. `A_i=5^i` (`i=1..B`), `C=2 sum_i A_i + 1 = (5^{B+1}-3)/2`,
`T=(A_1,...,A_B,C-A_1,...,C-A_B)` (`|T|=2B`, indices `0..2B-1`), `a=B`,
`G=Z_C`, `Phi(S)=sum_{i in S} T_i mod C`. Full slice `Omega^0=C([2B],B)`,
`M=|Omega^0|=C(2B,B)`. Occupied set `S=Phi(Omega^0)`, `L=|S|`. Heavy fiber
`Phi^{-1}(0)`, `W=|Phi^{-1}(0)|`.

Characters `chi_xi(x)=e^{2 pi i xi x/C}` (`xi in Z_C`). A **complete dyadic
band** `A` is one level of `tau(xi)=sum_{t in T} chi_xi(t)`:
`A_j={xi!=0 : floor(log2|tau(xi)|)=j}` (with the `|tau|<1` class as its own
band); the bands partition `Z_C\{0}` into `kappa <= K_N=2+ceil(log2(2B))` sets,
each symmetric (`-A=A`, so `K_A` is real). `K_A(x)=(1/C) sum_{xi in A} chi_xi(x)`,
`P_A f=K_A*f`; `hat{K_A}=1_A`, so `P_A` is the orthogonal band projection.
`||f||_q^q = sum_x |f(x)|^q` (counting measure). Two normalizations:

```text
R_A(f)    = (L^{1-1/q}/M) ||P_A f||_q     [#716 Prop 1.1 / #717 Sec 1]
gain_A(f) = ||P_A f||_q / C^{1/q}          [#723 census; = #716 script]
```

**First-match pruning (the hypothesis, exact -- #723 `dense_dedup_mask`).**
Enumerate `Omega^0` in lexicographic order; **keep `S` iff `Phi(S)` has not
occurred earlier**, else delete. The kept set holds exactly one support per
occupied syndrome; its count function is the indicator `1_S`. A **signed
sub-mask on the pruned support** is any `g: Z_C -> [-1,1]` with `g=0` off `S`
(in particular any sign/drop vector `eps in {-1,0,1}^S`).

## 2. Sidon / dissociativity structure (Lemma V, PROVED)

The map `sigma |-> sum_{i=1}^B sigma_i 5^i` is injective on `{-1,0,1}^B`
(balanced base 5, digits in `{-1,0,1}` -> no carries), with image in
`(-(5^{B+1}-5)/4, +(5^{B+1}-5)/4) subset (-C/2, C/2)`. A support using `u`
"`A_i`-only", `v` "`(C-A_i)`-only", `p` "both", `z` "neither" indices has
`u+v+2p=B` (size) and `u+v+p+z=B` (indices), so `z=p` and

```text
Phi(S) = sum_i sigma_i A_i,  sigma_i in {+1,-1,0},  #{sigma_i!=0}=u+v == B (mod 2).
```

Hence `S = { sum sigma_i 5^i mod C : sigma in {-1,0,1}^B, |supp sigma| == B (2) }`
and `L = sum_{k == B (2)} C(B,k) 2^k = (3^B+1)/2`. The `B/2`-twin-pair supports
(`S = union_{i in P}{A_i, C-A_i}`, `|P|=B/2`) all map to `0`, giving
`W = C(B,B/2)`; superincreasing distinctness makes `0` the **unique** heaviest
fiber and forces the first-match residual count to be **exactly `1_S`** (`0/1`,
`L` ones). Verified per `B` (occupied set `==` balanced base-5 parity image,
`W>` second-heaviest). This dissociativity is what powers the exact `q=2`
orthogonality below.

Exact table (matches #717 Sec 7, `Phi=sum mod C`, `s0=BC/2 == 0`):

| B | N=2B | C     | M=C(2B,B) | L=(3^B+1)/2 | W=C(B,B/2) | kappa | WL/M    |
|---|------|-------|-----------|-------------|------------|-------|---------|
| 2 | 4    | 61    | 6         | 5           | 2          | 3     | 5/3     |
| 4 | 8    | 1561  | 70        | 41          | 6          | 4     | 123/35  |
| 6 | 12   | 39061 | 924       | 365         | 20         | 5     | 1825/231|

## 3. Theorem I -- pruned upper bound (PROVED, all bands / all q>=2 / all signs)

**Lemma I-a (l2 endpoint).** For `g` supported on `S`, `|g|<=1`:
`||P_A g||_2 <= ||g||_2 <= sqrt(L)`. (`P_A` orthogonal projection => contraction;
`||g||_2^2 = sum_{s in S}|g(s)|^2 <= L`.)

**Lemma I-b (l-infinity endpoint, Cauchy-Schwarz).**
`||P_A g||_inf <= max_x sum_{s in S}|K_A(x-s)| <= sqrt(L) ||K_A||_2 = sqrt(L delta_A)`,
`delta_A=|A|/C`. (`|g|<=1`; CS over the `<=L` nonzero terms; and
`||K_A||_2^2 = (1/C^2) sum_x |sum_{xi in A} chi_xi(x)|^2 = |A|/C = delta_A`.)

**Theorem I.** For every complete dyadic band `A`, every `q in [2,inf]`, and
every signed sub-mask `g` on the pruned support,

```text
R_A(g) <= (L/M) (L delta_A)^{1/2-1/q} <= L^{3/2-1/q}/M.
```

*Proof.* Log-convexity of `l^q` norms (Riesz interpolation between `2` and
`inf`): `||P_A g||_q <= ||P_A g||_2^{2/q} ||P_A g||_inf^{1-2/q}
<= L^{1/q} (L delta_A)^{(1-2/q)/2}`. Multiply by `L^{1-1/q}/M`:
`R_A(g) <= (L^{1-1/q}/M) L^{1/q}(L delta_A)^{(1-2/q)/2}
= (L/M)(L delta_A)^{1/2-1/q}`; then `delta_A<=1`. `square`

**Consequences.**
- `q=2` (sharpest, sign-independent): `R_A(g) <= L/M` **exactly**. `L/M -> 0`
  (`= (sqrt(pi B)/2)(3/4)^B (1+o(1))`), so the signed q-gain vanishes.
- Subexponential range: `log(L^{3/2-1/q}/M) = B log 3 [ (3/2-1/q) - 2 log2/log3 ] + o(B)`,
  so `R_A(g) -> 0` (`o(1)`, hence `e^{o(N)}`) for all `2 <= q < q_+`, where

```text
q_+ = ( 3/2 - 2 log2/log3 )^{-1} = 4.19920...
```

The census's fixed `q=4 < q_+` is inside this range. Verified: pruned `R_A <=`
both bounds for every band and `q in {2,3,4,8}` (215/215).

## 4. Theorem II -- unpruned lower bound (PROVED; #717 Lemma 2.1 at s0=0)

Let `b=f_full` be the full-multiplicity count (`b(s)=|Phi^{-1}(s)|`),
`b(0)=W`. Fourier inversion at `0` minus the trivial character (`hat b(0)=M`):
`b(0) - M/C = sum_A (P_A b)(0)` over the `kappa` complete bands. Pigeonhole:
some band `A*` has `|(P_{A*} b)(0)| >= (W-M/C)/kappa`, and `||P_{A*} b||_q >=
|(P_{A*} b)(0)|`, so

```text
R_{A*}(f_full)    >= (L^{1-1/q}/M) (W - M/C)/kappa,
gain_{A*}(f_full) >= (W - M/C)/(kappa C^{1/q}).
```

Since `M<C` and `W>=2`, `W-M/C >= W/2`. The `R`-form `-> infinity` for
`q > q_- = (1 - log2/log3)^{-1} = 2.70951...`; the census-gain form `-> infinity`
for `q > log2(5) = 2.32193`, and at `q=4` its best-band value reproduces #723's
`C_iii` (`0.539, 0.768, 0.842`) exactly. This is a genuine band failure of the
whole unpruned mask (not a point-mass tag): `WL/M ~ (3/2)^B` (table above).

## 5. Theorem III -- separation window (PROVED)

For integer `q in (q_-, q_+) = (2.7095, 4.1992)`, i.e. `q in {3,4}`, Theorems I
and II hold simultaneously: `sup_g R_A(g) -> 0` for **every** band while
`max_A R_A(f_full) -> infinity`. So `(pruned bounded / unpruned growing)` is a
**theorem pair**, one normalization, one `q`. Exact integer certificate (no
logs):

```text
unpruned grows  (q > q_-)  <=>  3^{q-1} > 2^q          [q=3: 9>8; q=4: 27>16]
pruned  decays  (q < q_+)  <=>  3^{3q-2} < 4^{2q}      [q=3: 2187<4096; q=4: 59049<65536]
both  <=>  q in {3,4}      [boundary: q=2 fails 1st (3<4); q=5 fails 2nd]
```

`q=4` is the census's fixed exponent, so the census's own measured split
(pruned "B" decreasing `0.404->0.209`, unpruned "C_iii" increasing
`0.539->0.842`) sits inside a proved window.

## 6. Theorem IV -- large-q residual (route-cut COUNTEREXAMPLE + EXPERIMENTAL)

The all-signs clause of Theorem I is **route-scoped to `q<q_+`**. At `q=inf`,
taking `g(s)=sgn K_A(x*-s)` at the argmax gives
`sup_g ||P_A g||_inf = max_x sum_{s in S}|K_A(x-s)| =: Lambda*(A)`, hence
`sup_g R_A(g) = (L/M) Lambda*(A)`. Measured (verifier):

```text
B         2       4       6
Lambda*_B 1.171   2.013   5.561    (= max_A Lambda*(A))
(L/M)Lambda*_B 0.975 1.179 2.197   (= sup_g R_A at q=inf, worst band)
```

Both increase in `B` (`Lambda*_B ~ 0.29 sqrt(L)` at these sizes), so the sup
over signs exceeds any fixed bound as `q -> inf`: no all-`q` signed bound holds.
The first-match **indicator** `1_S` (all `+1`) is measured to stay bounded and
DECREASING for every tested `q` (its `||P_A 1_S||_q` enjoys Fourier
cancellation, not merely `|g|<=1`) -- but this is **not proved here beyond
`q_+`**. The residual analytic input is exactly a signed character-sum (Sidon)
estimate `sum_{s in S}|K_A(x-s)| = e^{o(N)}` on the dissociated set `S`.

## Nonclaims

- **One family, one chart.** Depth-1 superincreasing, `G=Z_C`. This is **not**
  the charge-preserving semantic-or-signed dichotomy, **not** A4, **not**
  primitive Q or max-fiber flatness, **not** the Proximity Prize. It is the
  signed clause discharged on #717 Sec 7 only.
- **Route-scoped in q.** Theorem I's "all signs -> 0" is for `q<q_+=4.199`
  only. For `q>=q_+` the adversarial-signed excess grows (Theorem IV); no
  all-`q` signed bound is claimed. The indicator's boundedness for `q>=q_+` is
  **EXPERIMENTAL** (`B<=6`).
- **Not an image-scale MI/MA or a general Sidon payment.** The signed payment
  is proved on this family; a general chart still needs the character-sum
  estimate of Theorem IV. The two normalizations have different thresholds
  (`R_A`: `q_-=2.71`; census gain: `2.32`); both are stated.
- **Finite instances.** `B in {2,4,6}`; measured constants (`Lambda*_B`,
  gains) are not asymptotic rates. The `q`-thresholds `q_-, q_+` and the
  integer window `{3,4}` ARE closed-form/exact.

## Consumers

- `asymptotic_rs_mca_frontiers.tex`: the signed-minor alternative of the
  hard-input-2 dichotomy, discharged on the `eq:exact-power-sum-map` depth-1
  chart; paste-ready as a proposition after #717's heavy-fiber remark.
- #716 (`primitive_signed_payment_barrier_v1.md` Sec 6): supplies the signed
  charge bound `c_i <= e^{o(N)} M/L^{1-1/q}` (Theorem I) on this family and
  isolates its `q`-range; the many-syndrome analytic residual is Theorem IV.
- #723: the census's dense-regime finding is now a two-sided theorem pair
  (Theorem III), q=4 values reproduced exactly.
- Lean statement stub: `experimental/lean/first_match_signed_gain/`
  (exact family arithmetic + integer q-window dichotomy; analytic `l^q` bounds
  are proved in this note/verifier, not in Lean -- honest Nonclaim in-package).
