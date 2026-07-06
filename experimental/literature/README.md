# RS-MCA L1 research library

Curated literature for the L1 prime-`ell` listing frontier / KEY LEMMA `E_3 <= ell-2`
(branch `scott/l1-e3-ceiling-open-chart`). **PDFs are git-ignored** (bulky/copyrighted); this
index is tracked so the map survives. Legend: `[LOCAL]` = PDF in this tree; `[BROWSER]` =
Cloudflare-gated eprint, grab in a browser (URL given); `[FIND]` = paywalled journal, get via
library access.

## The organizing finding

Stripped of the RS-MCA framing, the KEY LEMMA is a **finite-field value-set statement**:
a constant-free `Gamma`, `deg <= ell-1`, over `F_p` (`ell | p-1`), and its level-set excess
`E_3 = sum_cosets (mu-2)_+ <= ell-2` across the cosets of `mu_ell`. This is the **Rédei–Szőnyi–
Ball theory of fully-reducible lacunary polynomials / directions** in multiplicative disguise:
- our frontier law `m*(ell) = (ell+3)/2` = the classical `(q+3)/2` direction bound (Ball, Example 1: `X^{(q+1)/2}` determines `(q+3)/2` directions; Rédei/Lovász–Schrijver);
- our **refuted** conjecture `ceil(2ell/3)` = the Gács direction bound `ceil((2/3)(p-1))+1`;
- the proof engine — fully-reducible `f = X^n g + h`, `gcd(g,h)=1` (= our `g_k h_k = X^ell - w_k`
  split) driven by the Wronskian divisibility `f | (Xg+h)(h'g - g'h)` — is exactly what should
  prove our open crux `dim Syz <= K`. See `../notes/l1/l1_e3_lacunary_directions_connection.md`.

---

## A. Lacunary polynomials & directions — THE PROOF ENGINE (highest priority)

- `[LOCAL]` **Ball, "Lacunary Polynomials over Finite Fields" (survey/notes)** —
  `lacunary-directions/Ball-lacunary-polynomials-over-finite-fields-notes.pdf`.
  Thm 1.1 (Rédei `X^p+g` fully reducible ⟹ `g°≥(p+1)/2`); Thm 1.9/1.14 (`f=X^q g+h`,
  `gcd(g,h)=1` classification — the norm/trace cases); directions Thm 1.4; **Example 1**
  (`X^{(q+1)/2}` → `(q+3)/2` dirs); **the divisibility `f|(Xg+h)(h'g-g'h)` (p.6)**. Primary source.
- `[LOCAL]` **Ball–Herranz, lacunary course notes** —
  `lacunary-directions/Ball-Herranz-lacunary-course-notes.pdf`. Expanded proofs of the above.
- `[LOCAL]` **Fancsali–Sziklai, "On rich and poor directions…" (arXiv 1903.03881)** —
  `lacunary-directions/Fancsali-Sziklai-rich-poor-directions-1903.03881.pdf`. Refinements /
  the `|R|<q` regime.
- `[FIND]` Blokhuis, Brouwer, Szőnyi, *The number of directions determined by a function on a
  finite field*, JCTA **70** (1995) 349–353.
- `[FIND]` Blokhuis, Ball, Brouwer, Storme, Szőnyi, *On the number of slopes of the graph of a
  function defined on a finite field*, JCTA **86** (1999) 187–196. (The main classification.)
- `[FIND]` Ball, *The number of directions determined by a function over a finite field*, JCTA
  **104** (2003) 341–350.
- `[FIND]` **Gács, *On a generalization of Rédei's theorem*, Combinatorica 23 (2003) 585–598** —
  the `ceil(2(p-1)/3)` bound (= our refuted conjecture). Key for the numerology.
- `[FIND]` Lovász, Schrijver, *Remarks on a theorem of Rédei*, Studia Sci. Math. Hungar. 16
  (1983) 449–454. (Characterizes the `(p+3)/2` case.)
- `[FIND]` Szőnyi, *On the number of directions determined by a set of points in an affine
  Galois plane*, JCTA **74** (1996) 141–146. (The `(k+3)/2` bound for `k<p`.)
- `[FIND]` Rédei, *Lacunary Polynomials over Finite Fields*, North-Holland (1973). (The book.)

## B. Proximity gaps / correlated agreement — near-capacity failure (POSITIONING / NOVELTY)

- `[LOCAL]` **ABF, "Open Problems in List Decoding and Correlated Agreement" (eprint 2026/680)** —
  `proximity-gaps-mca/ABF-2026-680-open-problems-list-decoding-CA.pdf`. THE prize problem
  statement (Arnon–Boneh–Fenzi). Our target.
- `[LOCAL]` **Kambiré, "Proximity Gaps Conjecture Fails Near Capacity over Prime Fields"
  (arXiv 2604.09724)** — `proximity-gaps-mca/Kam26-…`. Proves gaps fail `O(1/log n)` below
  capacity over prime fields (fleshes out Krachun–Kazanin). **Same failure theme as our Paper A —
  position against this.** No roots-of-unity/`(ell+3)/2`/level-set structure ⟹ our mechanism differs.
- `[LOCAL]` **"A Syndrome-Space Approach to Proximity Gaps and CA for Random Linear Codes"
  (arXiv 2605.07595)** — `proximity-gaps-mca/syndrome-space-…`. Syndrome-fiber view; compare to
  our repaired-locator `syndrome` reformulation (`../notes/l1/l1_repaired_locator_theorem_package.md`).
- `[BROWSER]` **KKH26** Krachun–Kazanin–Haböck, *Failure of proximity gaps close to capacity* —
  https://eprint.iacr.org/2026/782 . The other near-capacity-failure result in ABF's refs.
- `[BROWSER]` **CS25** Crites–Stewart, *On Reed–Solomon Proximity Gaps Conjectures* —
  https://eprint.iacr.org/2025/2046 . Impossibility results; the CA/list conversion route.
- `[BROWSER]` **BCHKS25** Ben-Sasson–Carmon–Haböck–Kopparty–Saraf, *Proximity Gaps for RS Codes* —
  https://eprint.iacr.org/2025/2055 . Johnson-radius positive bound (ABF Table 1).
- `[BROWSER]` **Hab25** Haböck, *A note on mutual correlated agreement for RS codes* —
  https://eprint.iacr.org/2025/2110 . Generalizes Guruswami–Sudan to get MCA. Defines our object.
- `[BROWSER]` **BCGM25** Bordage–Chiesa–Guan–Manzur, *All Polynomial Generators Preserve Distance
  with MCA* — https://eprint.iacr.org/2025/2051 . MCA positive direction.
- `[BROWSER]` **BCIKS20** Ben-Sasson–Carmon–Ishai–Kopparty–Saraf, *Proximity Gaps for RS Codes*,
  FOCS 2020 — https://eprint.iacr.org/2020/654 . The foundational proximity-gap paper.
- `[BROWSER]` **GG25** Goyal–Guruswami, *Optimal Proximity Gaps for Subspace-Design & (Random) RS* —
  https://eprint.iacr.org/2025/2054 .

## C. List decoding / RIM machinery (interleaved-list side)

- `[LOCAL]` **Alrabiah–Guruswami–Li, "AG codes have no list-decoding friends…" (arXiv 2308.13424)** —
  `list-decoding-rim/AGL23-…`. Exponential-alphabet lower bounds near generalized Singleton.
- `[FIND]` **AGGLZ25** Alrabiah–Guo–Guruswami–Li–Zhang, *Random RS Codes Achieve List-Decoding
  Capacity with Linear-Sized Alphabets*, Adv. Combinatorics (2025). **The RIM / agreement-hypergraph
  machinery the repo's `l1_high_multiplicity_certificate_roadmap.md` imports (Lemmas 2.3, 2.8, Thm 2.11).**
- `[FIND]` GGR11 Gopalan–Guruswami–Raghavendra, *List Decoding Tensor Products and Interleaved
  Codes*, SICOMP 40 (2011). (Interleaved list bounds — L2 lane.)

---

## Browser-download queue (paste into a browser; save into the matching subdir)
```
https://eprint.iacr.org/2026/782.pdf   -> proximity-gaps-mca/  (KKH26)
https://eprint.iacr.org/2025/2046.pdf  -> proximity-gaps-mca/  (CS25)
https://eprint.iacr.org/2025/2055.pdf  -> proximity-gaps-mca/  (BCHKS25)
https://eprint.iacr.org/2025/2110.pdf  -> proximity-gaps-mca/  (Hab25)
https://eprint.iacr.org/2025/2051.pdf  -> proximity-gaps-mca/  (BCGM25)
https://eprint.iacr.org/2020/654.pdf   -> proximity-gaps-mca/  (BCIKS20)
https://eprint.iacr.org/2025/2054.pdf  -> proximity-gaps-mca/  (GG25)
```
(eprint.iacr.org is Cloudflare-gated; `curl`/WebFetch get a 403, a browser passes trivially.)
