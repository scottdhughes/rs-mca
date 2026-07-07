# b2 Phase-0 literature pin: PIONEER, not port (2026-07-06)

- **Status:** literature scoping (Phase-0 of the b2 attack plan). Cross-checked against
  primary sources (arXiv / ar5iv full text); single-source claims flagged inline.
- **Question asked:** is "count the divisors of a fixed object (integer N, or the polynomial
  `X^n-1`) with prescribed leading coefficients / in residue classes, at LARGE depth
  (constraints ~ log-scale, not O(1))" a solved problem we can PORT, or open?
- **Verdict:** **PIONEER — open even over ℤ.** No drop-in theorem exists for the
  fixed-object divisor-SET problem at large depth. Confirms `b2_step0_object_pinned.md`.

## The key distinction (why the big literature does not apply)

The deployed b2 object (via Newton) is: count `m`-subsets of the subgroup `mu_n` with
`p_1=...=p_w=0` — an **exponential sum over subsets of a subgroup weighted by power sums**,
i.e. "divisors of the FIXED polynomial `X^n-1` with a prescribed leading-coefficient window."
This is **NOT** `sum_{g in short interval} d_k(g)` (a divisor-FUNCTION short sum). Almost all
of the powerful function-field machinery targets the latter.

## State of the art (both settings)

**ℤ — fixed-N divisors in residue classes at large depth: OPEN.**
- Hall (JNT 1970/71) + Hall–Tenenbaum, *Divisors* (1988): only **almost-all `n`** and
  **small modulus `k`** ("divisors evenly distributed provided `k` not too large"). Not fixed-N,
  not large depth.
- Fouvry–Ganguly–Kowalski–Michel, arXiv:1301.0214 (CMH 2014): `d(n)` in residue classes is
  Gaussian, but **restricted modulus range**, averaged over `n`, via Kloosterman-sheaf monodromy.
  A bounded-depth ceiling.
- Character reformulation (my synthesis, not a quoted theorem): power-saving needs
  `prod_{p|N}(1+chi(p))` small uniformly over `~log N` characters — uncontrolled for a single
  fixed `N` with `omega(N) -> inf`. That IS the open point.

**F_q[X] — same gap for the fixed-`f` divisor set.**
- He–Zhang, arXiv:1709.00820: variance of divisor-in-residue-class **averaged over monic `f`**,
  via Selberg–Delange (not Katz). The exact F_q analogue of Hall — average + small modulus only.
- Large-q RMT/Katz family (bounded depth in fixed `q`): Keating–Rudnick arXiv:1204.0708
  (`lim_{q->inf} q^{-(h+1)}Var = n-h-2`, error one `sqrt q`); KRRR arXiv:1504.07804 (range
  `min(n-5,(1-1/k)n-2)` **shrinks as `k` grows**); Rodgers arXiv:1609.02967 (S_n cycle stats).
  All are the `q -> inf` limit, wrong object.

**The one large-depth power-saving result — and why it is the WRONG object.**
- Sawin, arXiv:1809.05137, "Square-root cancellation for sums of factorization functions over
  short intervals": genuine `sqrt`-cancellation reaching depth `(1-eps)n` — but (i) for
  `sum_{deg g<h} d_k(f+g)`, a divisor-FUNCTION short sum, not our fixed-`f` divisor set; and
  (ii) needs **large characteristic** (the combinatorial factor `(k+2)^{2n-h}` is absorbed only
  when `q^{1/(log k+2)}` is large). This is the template to adapt, and its two limitations name
  exactly the new ideas needed: a fixed-`f` divisor-set analogue + small-characteristic control.

## The sqrt(p) barrier — confirmed and mechanized

Each prescribed leading coefficient = one more power-sum/codimension-1 condition = one more
fiber-product, multiplying the Betti/complexity bound by a bounded `C`. Error `~ C^d q^{-1/2}`
beats the main term only for `d <~ (log q)/(2 log C)` — the bounded ~20-constraint cap, matching
the repo's proved head depth `w_0 = 21-22` (KoalaBear) / `10-11` (Mersenne). Made explicit in
Sawin's `(k+2)^{2n-h}` factor; Quantitative Sheaf Theory (Sawin–Forey–Fresán–Kowalski,
arXiv:2101.00635, JAMS 2023) is the uniform-in-`q` machinery that CONTROLS `C^d` but does not by
itself remove the cap.

**BGK is powerless here (hypothesis corrected).** Bourgain–Glibichuk–Konyagin (JLMS 2006):
`|sum_{x in H} e_p(ax)| <= |H| p^{-nu}` requires `|H| >= p^gamma`, but is an *improvement* only for
**sparse** `H` (`|H| << p^{1/2}`); for a dense/large subgroup the classical Weil bound already
gives `O(sqrt p)` and BGK adds nothing (Kowalski, arXiv:2401.04756). Our `mu_n` is dense ⟹ stuck
at the one-Weil barrier.

## Reading list (priority order) + next step

1. **Sawin arXiv:1809.05137** — the only method that breaks the depth barrier; study the
   singular-locus computation + the large-characteristic dependence. Template + its gaps.
2. **Quantitative Sheaf Theory, arXiv:2101.00635 (JAMS 2023)** — uniform-in-`q` complexity/Betti
   lever on the `C^d` growth.
3. **Sawin–Shusterman, arXiv:2512.24080 (Dec 2025)** — frontier: near-`sqrt`-cancellation for
   short sums of trace functions, fixed large `q`, under monodromy hypotheses (slopes <=1 at inf,
   no Artin–Schreier factors). Most likely reusable input; its monodromy conditions are the
   realistic obstruction to verify for the cyclotomic/`mu_n` setting.

**Consequence for the attack:** there is no shortcut. The route is to adapt Sawin's singular-locus
`sqrt`-cancellation to the fixed-`X^n-1` divisor-set object and confront small characteristic —
original mathematics. Phase-0 numerics (`b2_dense_extras.py`, dense-band regime) should measure
whether `#extras <= n^3` holds with slack just past `w_0`, to confirm the target before investing.
