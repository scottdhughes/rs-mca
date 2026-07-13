# The cor:grand 86-bit conditional branch, row by row on the deployed envelope

## Status

`AUDIT (CONDITIONAL record). Follow-up to PR #736's pay-per-bit ledger audit,
which flagged that cor:grand's last sentence (tex/cs25_cap_v12.tex:3567,3584)
gives a sharper number -- epsilon_mca > 2^-42, i.e. 86 bits above the 2^-128
target, versus the unconditional 2^-86 / 42 bits -- when the extra hypothesis
q>=2n holds. This note instantiates cor:grand's FULL printed hypothesis set
(not just q>=2n) on the maintainer-cited deployed anchor rows. Result: q>=2n
holds trivially on every row checked, but cor:grand's other hypotheses do
not -- on 3 of the 4 rows a DIFFERENT, EARLIER hypothesis blocks the
corollary outright, and on the 4th (the one row it does apply to) the
sharper branch is dominated by an already-printed, already-unconditional
row-specific number. Net: citing this branch adds no new pay-per-bit value
on the deployed envelope as currently listed. Not new mathematics: cor:grand
is the maintainer's own printed result; this packet only checks its
hypotheses against rows. No Lean stub required for the audit itself (a small
native_decide integer-fact addendum is included regardless, see section 4).`

## 0. What is being checked, and why it is not just "does q>=2n hold"

`cor:grand` (`tex/cs25_cap_v12.tex:3542-3574`, proof `3575-3585`) reads,
compressed to its hypothesis list and conclusion:

> Let `rho in {1/2,1/4,1/8,1/16}`, `N_rho:=1024` (`rho in {1/2,1/4,1/8}`),
> `N_{1/16}:=2048`. Let `F` be any finite field with `q:=|F|<2^256`, let
> `B<=F` be any subfield, let `D<=B^x` be a multiplicative coset of order
> `n` with `N_rho | n`, and let `k=rho*n<=2^40`. Then `C=RS[F,D,k]`
> satisfies `emca(C,delta) > (1/2k)(1-n/q) >= 2^-86 >> 2^-128` for every
> `delta` in the stated sub-capacity window.
> **If `q>=2n`, the lower bound improves to `>=2^-42`.**

So the sharper branch's full hypothesis set is:

```
H1  rho in {1/2, 1/4, 1/8, 1/16}
H2  N_rho | n            (N_rho = 1024 for rho in {1/2,1/4,1/8}; 2048 for rho=1/16)
H3  q := |F| < 2^256
H4  B <= F any subfield
H5  D <= B^x is a multiplicative coset of order n   (thm:main's own hypothesis,
                                                       tex/cs25_cap_v12.tex:3403-3428)
H6  k = rho*n <= 2^40
H7  q >= 2n               (the sharper branch's own extra hypothesis)
```

`H7` is only meaningful once `H1`-`H6` already hold, because what is being
sharpened is `cor:grand`'s own conclusion. A row that fails an earlier
hypothesis is not "conditionally in the 86-bit branch pending `q>=2n`" -- it
is simply not an instance of `cor:grand` at all, independent of `q` vs `2n`.
Checking only `q>=2n` in isolation would miss exactly this, so every
hypothesis is checked per row below.

`H5` is the one that needs a precise, non-hand-wavy criterion: `thm:main`
(`:3403`) requires `D` to be a literal multiplicative coset, and the paper is
explicit that this is a genuinely narrower notion than the general
"map-smooth" domains used for circle codes. The remark right after
`def:map-smooth` (`:3748`) states it directly: *"a multiplicative coset
`D subseteq B^x` of order `n` is `(X^a,a)`-smooth for every `a|n`"* -- i.e. a
coset is one specific case of a map-smooth domain (`phi=X^a`, the power
map). The circle-row domains use `phi=T_a` (Chebyshev) instead, are proved
`(T_a,a)`-smooth (`lem:cheb-fibers`, invoked in the proof of `cor:circle-grand`
at `:4040`), and are certified through the separate, more general
`thm:phi-cap` (`:3809`), which the paper states *contains* `thm:main` as the
special case `phi=X^a`, `a|k` (`:3739`). `cor:grand`'s printed "if `q>=2n`"
sentence occurs exactly twice in the whole paper (`:3567` in the statement,
`:3584` in the proof) -- nowhere in `cor:circle-grand` (`:4015-4037`) or
`cor:circle-deployed` (`:4049-4077`), which reuse `cor:grand`'s *numerics*
("The error numerics are those of `cor:grand`", `:4044`) but do not print an
analogous sharpening. So `H5` failing is not a technicality -- it means the
row is certified by a structurally different corollary, and `cor:grand`'s
specific printed sharper sentence simply is not about that row.

## 1. Row verdicts

Row list per the task steering and `PR #736`'s note section 1: the
KoalaBear-sextic row (the site/paper's primary deployed row, `cor:deployed`),
the Mersenne-31/QM31 circle rows (`cor:circle-deployed`), and the Cycle116/119
`F_17^32` row. `q`, `n`, `2n`, and the margin `q-2n` are exact integers,
recomputed by the verifier, not transcribed by hand.

| Row | Corollary that certifies it in the paper | `q` (bit length) | `n` (`k`) | `H7`: `q>=2n`, margin | Earlier blocker | `cor:grand` sharper branch |
|---|---|---|---|---|---|---|
| KoalaBear sextic | `cor:deployed` (direct `thm:main`, `N=256`) | `p^6`, `p=2^31-2^24+1` (186 bits) | `2^21` (`2^20`) | **holds**, margin `q-2^22` &asymp; `2^186` | none -- `H1`-`H6` all hold | **applies** (redundant, see 2) |
| M31 circle line round | `cor:circle-deployed(a)` (`thm:phi-cap`) | `p'^4`, `p'=2^31-1` (124 bits) | `2^21` (`2^20`) | holds, margin `q-2^22` &asymp; `2^124` | **`H5`**: `chi(twin coset)` is `(T_a,a)`-smooth, not a multiplicative coset | **blocked** |
| M31 circle code | `cor:circle-deployed(b)` (`thm:phi-cap`, torus) | `p'^4` (124 bits) | `2^22` (`2^21+1`) | holds, margin `q-2^23` &asymp; `2^124` | **`H5`**: twin coset is a union of 2 cosets, and `k_c` is always odd so `a nmid k_c` (`:4010`) | **blocked** |
| `F_17^32` (Cycle116/119) | none of this paper's pigeonhole corollaries -- a direct finite point-count | `17^32` (131 bits) | `512` (`256`) | holds, margin `q-1024` &asymp; `2^131` | **`H2`**: `N_{1/2}=1024` does not divide `n=512` | **blocked** |

Exact integers (all recomputed by the verifier):

```
KoalaBear:   p  = 2130706433                    (= 2^31 - 2^24 + 1, prime)
             q  = 93571093019388561295270373781649880353786165192103559169   (186 bits)
             n  = 2097152 (=2^21), 2n = 4194304
             q - 2n = 93571093019388561295270373781649880353786165192099364865

M31 (both):  p' = 2147483647                    (= 2^31 - 1, prime)
             q  = 21267647892944572736998860269687930881                     (124 bits)
             line round:  n=2097152 (=2^21),  2n=4194304,   q-2n = 21267647892944572736998860269683736577
             circle code: n_c=4194304 (=2^22), 2n_c=8388608, q-2n_c = 21267647892944572736998860269679542273

F_17^32:     q  = 2367911594760467245844106297320951247361                   (131 bits)
             n  = 512, 2n = 1024
             q - 2n = 2367911594760467245844106297320951246337
```

`H7` (`q>=2n`) holds on **every** row here, and not narrowly -- the margin is
always within a few bits of `q` itself, because every deployed row is built
as a small evaluation domain inside a large field (or, for `F_17^32`, a
domain that is merely a small fraction of the full field). So `q>=2n` is
never the operative constraint for any row actually in play; the real
content is in the other hypotheses, per row:

- **KoalaBear sextic**: the only row where `cor:grand`'s full hypothesis set
  (`H1`-`H7`) holds. `rho=1/2` is in the set; `N_{1/2}=1024 | n=2^21`; `D` is
  literally "the subgroup of order `n=2^21`" of `B^x` (`cor:deployed`'s own
  text) -- a genuine multiplicative coset, matching `H5`'s TYPE (not just
  size); `k=2^20<=2^40`; `q=p^6<2^256`. Nothing here is open or assumed --
  every clause is a checked arithmetic fact about a fixed row.
- **M31 circle rows**: blocked at `H5` for a structural reason, not a size
  technicality -- these domains are provably not multiplicative cosets (see
  section 0). The circle-code row additionally can never satisfy `thm:main`'s
  `a|k` hypothesis at all, since `k_c=2w+1` is always odd while the usable
  dyadic folding scales `a` are always even (`:4010`: *"the useful folding
  scales `a` on a dyadic torus twin coset are even, ... so `a nmid k_c`
  always"*) -- a parity obstruction, not a missing proof.
- **`F_17^32`**: blocked at `H2`. `n=512 < N_{1/2}=1024`, so `1024` cannot
  divide `512`; this is a pure size failure (the domain TYPE is fine -- the
  site records `"domainKind": "multiplicative-subgroup"` for this row,
  `site/data/rate-leaderboards.json:563,609`, same type as KoalaBear).

## 2. The one row where it does apply: still no new bits

On the KoalaBear row, `cor:grand`'s sharper branch is a true, fully checked
statement -- but it is dominated by a number the paper already prints
directly, with no `q>=2n` hypothesis needed at all:

```
generic worst-case conditional floor (envelope-worst k=2^40): 1/(4k) = 2^-42   -> 86 bits above 2^-128
same branch formula at THIS row's actual k=2^20:               1/(4k) = 2^-22   -> 106 bits above 2^-128
cor:deployed's own printed bound (no q>=2n invoked):     (1-2^-164)*2^-21 > 2^-22 -> 106 bits (exact value sits just under 2^-21, i.e. just under 107 bits)
```

The middle and bottom rows coincide at the printed headline `2^-22` -- not a
coincidence: both are the same core inequality `(1/2k)(1-n/q)` from
`thm:main`, one evaluated with the branch's worst-case relaxation `1-n/q>=1/2`
at this row's actual `k`, the other evaluated at the row's actual (and here,
astronomically favorable) `n/q`. `cor:deployed` already sits in the regime
the `q>=2n` branch exists to reach, using the row's real numbers rather than
the generic envelope-worst constants (`k<=2^40`, `q` as small as `2n`) that
give the generic `2^-42`/86-bit headline. Invoking the generic branch for
this row would understate what is already on record by 20 bits (`106-86=20`).
For the two M31 rows and `F_17^32`, the branch does not apply at all (section
1), so the comparison is moot there; their own printed/derived numbers are
`2^-22` (78 bits above the row's correct target `2^-100`, not `2^-128`: `q<2^128`
makes `delta*_C(2^-128)` degenerate for M31, `prop:small-field`, `:4738`),
`2^-23` (77 bits above `2^-100`), and `32.82` bits above `2^-128` (`F_17^32`,
reusing PR #736's own recomputation of `52747567092/17^32` -- notably *below*
even the generic *unconditional* 42-bit floor, with no contradiction since
`cor:grand` never covered this row to begin with).

**Diagnostic (not part of `cor:grand`'s hypothesis, offered only to explain
why `F_17^32` is hard, not just technically excluded):** `cor:rows` rescues
the KoalaBear interleaved family's divisibility hypothesis by using
`thm:main` directly with `N=256` instead of `cor:grand`'s packaged
`N_rho=1024`. Trying the same move on `F_17^32` (`N=256`, `ell_2=130`, same
as `cor:deployed`) fails: `thm:main`'s own entropy hypothesis `eq:hyp` needs
`binom(256,130) >= |B|(q/k+1)`; here `B=F` (this row has no smaller subfield
to shrink `|B|`, unlike KoalaBear/M31, where `|B|` is a fixed 31-bit prime
inside a much larger extension field), so `|B|(q/k+1) = q(q/k+1) approx
2^253.6` against `binom(256,130) approx 2^251.6` -- short by about `1.97`
bits. This is one candidate `N`, not an exhaustive search, so it is evidence
rather than a proof that no `N` rescues the row -- but it shows concretely
that the row's flat-field structure, not a one-clause technicality, is what
keeps it outside this paper's pigeonhole method. (Full numbers in the
certificate, `diagnostic_N256_eq_hyp_check`.)

## 3. The interleaved KoalaBear family (bonus, not a required row)

`cor:rows` (`:3644`) interleaves `C_s=RS[F_{p^6},D_s,k_s]` for `s=2^j`,
`0<=j<=12`, `n_s=2^21/s`. `q` is fixed (same field for every `s`), so `q>=2n_s`
holds for every `s` in the family by a huge margin. Checking `cor:grand`'s
own `N_{1/2}=1024 | n_s` hypothesis specifically (not `cor:rows`' own `N=256`
choice, which `cor:rows` uses precisely to avoid this restriction): it holds
for `j<=11` (`s<=2048`) and fails at `j=12` (`s=4096`, `n_s=512`) -- the same
`n=512` boundary as the `F_17^32` row above. This does not affect `cor:rows`
itself (it never routes through `cor:grand`'s `N_rho`), only whether
`cor:grand` specifically covers that one extreme interleaving.

## 4. Verdict

`q>=2n` holds on every deployed row checked, always by a wide margin -- but
that was never the binding constraint. `cor:grand`'s full printed hypothesis
set is satisfied by exactly one of the four maintainer-cited anchor rows
(KoalaBear sextic); the other three are certified by structurally different
machinery (`cor:circle-grand`/`cor:circle-deployed` for the M31 rows;
a direct finite count for `F_17^32`) that is not an instance of `cor:grand`.
On the one row it does cover, the sharper branch is strictly dominated by an
already-printed, already-unconditional row-specific bound (106 bits above
target vs. the branch's generic 86). **The 86-bit conditional record adds no
new pay-per-bit value on the deployed envelope as currently listed.** This is
not a defect in `cor:grand` -- it is exactly what a universal, envelope-worst-case
corollary is for, and the paper already prints the better row-specific
numbers separately (`cor:deployed`, `cor:circle-deployed`). Discharging `H5`
for the circle rows (i.e. proving an analogous `q>=2n` sharpening for
`thm:phi-cap`) looks mechanically plausible from the proof pattern but is not
printed anywhere and is not attempted here -- and, per section 2, would not
move any currently-cited number even if added, since `cor:circle-deployed`
already exceeds it. `H2` for `F_17^32` is not "one clause away" either
(section 2's diagnostic): it reflects the row's flat-field structure.

## 5. Reproducibility

`experimental/scripts/verify_pay_per_bit_86bit_conditional_rows.py --check`
recomputes every integer/Fraction/Decimal quantity above from scratch (no
transcribed numbers trusted), checks the exact `tex/cs25_cap_v12.tex` anchors
and line numbers cited, and cross-validates against
`experimental/data/certificates/pay-per-bit-86bit-conditional-rows/certificate.json`.
`--tamper-selftest` mutates five independent facts (a row's applicability
flag, a big-integer margin, the `128-42` bit-arithmetic constant, the
`F_17^32` rounded bit margin, and the `F_17^32` `H2` verdict) and confirms
each is caught. A companion `native_decide` Lean fact file for the pure
integer comparisons (`q` vs `2n`, `N_rho | n`) is in
`experimental/lean/margin_anchors/MarginAnchors.lean`
(`CorGrandQGe2nRows` namespace).

## Credit

`cor:grand` (including its own printed `q>=2n` sharper branch) is the
maintainer's result (`tex/cs25_cap_v12.tex`); PR #736 first flagged the
sharper branch as worth a follow-up footnote. This packet only instantiates
the corollary's printed hypotheses on rows -- no new theorem is claimed.
