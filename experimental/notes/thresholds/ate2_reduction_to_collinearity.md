# A_te-2 upper bound: a conditional reduction (its lemma L1 is FALSE)

Status: **CORRECTED / L1 REFUTED (2026-07-06).** The reduction below proves
`LD_sw(C, A_te-2) <= R3+3` **only in the `L=1` case** (all bad-slope codewords on
one code-line). The collinearity lemma L1 -- that we are ALWAYS in the `L=1`
case -- is **FALSE**: a Sage/CAS construction exhibits configs with 3 bad slopes
whose codewords have rank 2 (non-collinear, `L>1`). The earlier "1200/1200
`L=1`" evidence was a **biased sample** (all perturbations of the a425 witness,
which sits in its own `L=1` basin). Therefore this note does NOT prove the bound;
`A_te-2` is fully OPEN again. The reduction steps (1,3,4,5) remain individually
valid (Codex-verified) as a CONDITIONAL result. Counterexample constructor:
`experimental/scripts/ate2_L1_refute.sage`.

> The rest of this note is retained as the (correct) conditional argument for the
> `L=1` case and the record of how L1 was refuted. Do not read the original
> "PROVED modulo L1" framing as a proof.

## Setup

`C = RS[F_q, D, k]`, `|D|=n`, `m=n-k`, `R3=floor(m/3)`, `A = A_te-2 = n-R3-2`.
`LD_sw(C,A)` = max over received lines `(f,g)` of the number of
support-wise-noncontained bad slopes `z`: there is `S_z`, `|S_z|=A`, with
`w_z=f+zg` restricting to a codeword `c_z` on `S_z` while `g|_{S_z}` does not
extend to a deg-`<k` poly. By the committed **exact-support reduction** (valid
since `A>k`: any larger noncontained witness contains an exact `A`-point
noncontained subwitness) we may take `|S_z|=A` exactly. We assume the deployed
regime `m >= 12`, so `2A-n = n-2R3-4 >= k` (a426's overlap condition), under which
`c_z` is unique and every pairwise overlap has size `>= k`.

## Step 1 -- bad codewords are related through g

For `z,w in Z`, on `S_z cap S_w` (size `>= 2A-n >= k`) both `w_z=c_z`, `w_w=c_w`,
so `(z-w)g = c_z-c_w`, i.e. `g = (c_z-c_w)/(z-w) =: p_{zw}` extends to a deg-`<k`
poly there. (Unconditional corollary: from any two bad slopes,
`(z-w)g = (c_z-c_w) + (e_z-e_w)` with `wt(e_z)<=n-A=R3+2`, so `g` lies within
Hamming distance `2R3+4` of `C` -- just past the Johnson radius, hence not enough
for uniqueness; this is why L1 is nontrivial.)

## Step 2 -- the collinearity lemma L1 (the one open input)

**L1 (FALSE).** "The bad codewords are collinear: `c_z = a + z b` for every
`z in Z`." -- **This is false.** `ate2_L1_refute.sage` constructs, on 4 rows,
configs with 3 bad slopes whose codewords have **rank 2** (non-collinear). The
construction: pick `c_0,c_2` random codewords and `c_1 = (c_0+c_2+h)/2` with `h`
a deg-`<k` poly vanishing on the triple overlap `T` (so the pairwise
difference-polys agree on `T`, making `g` consistently definable) and `h != 0`
(so `c_1` is off the line). Since the triple overlap has size `>= (m mod 3)+k-6`,
i.e. only `~k-6 < k`, three distinct difference-polys CAN agree there -- nothing
forces collinearity. The earlier `L=1` observation was a biased sample (a425
perturbations). So the `L=1` reduction below is CONDITIONAL and does not close the
bound.

## Steps 3-5 -- the reduction (unconditional given L1)

Put `f'=f-a`, `g'=g-b`. On `S_z`: `w_z=c_z=a+zb`, so `f'+zg'=0`, i.e. `f'=-zg'`
pointwise. Hence `S_z subset Z0 cup R_z` with `Z0={f'=g'=0}` and
`R_z={x: g'(x)!=0, -f'(x)/g'(x)=z}`; the `R_z` **partition** `{g'!=0}`, so they are
pairwise disjoint (Step 3, verified).

`z` bad means `g'|_{S_z}` does not extend (`b` is a codeword). On `S_z`, `g'=0`
exactly on `Z0 cap S_z`; if `S_z subset Z0` then `g'|_{S_z}=0` extends,
contradiction. So `|R_z cap S_z| >= 1` and `= A-|Z0 cap S_z| >= A-|Z0|` (Step 4,
verified).

Disjointness gives `sum_{z} |R_z cap S_z| <= |{g'!=0}| <= n-|Z0|` (Step 5):
- `|Z0| <= A-1`: each term `>= A-|Z0| >= 1`, so `|Z| <= (n-|Z0|)/(A-|Z0|)`. This is
  increasing in `|Z0|` (slope sign `= n-A > 0`), so maximal at `|Z0|=A-1`, giving
  `|Z| <= n-A+1 = R3+3`.
- `|Z0| >= A`: `|Z| <= |{g'!=0}| <= n-|Z0| <= n-A = R3+2`.

Either way `|Z| <= R3+3`. Tight at the a425 witness (`L=1`, `|Z0|=A-1`, `|Z|=R3+3`).
QED modulo L1.

## Verification

- **Logic:** Codex adversarial review -- Steps 1,3,4,5 `verified`, L1 confirmed as
  the sole load-bearing gap (without L1 the bound is only `L*(R3+3)` per code-line
  cluster). Caveats folded in above (exact-support reduction; the real hypothesis
  is `2A-n>=k`, not `A>(n+k)/2`).
- **Computation:** `ate2_construct_and_count.py` (Berlekamp-Welch) and an
  independent **Sage** `GRSBerlekampWelchDecoder` cross-check agree on the
  bad-slope count `= R3+3` and on `L=1` (Sage rank `<= 1`, rank `1` on a
  non-degenerate code-line).

## Status / honest scope (CORRECTED)

`A_te-2` is **OPEN**. L1 is **FALSE**, so this note does NOT prove
`LD_sw(A_te-2) <= R3+3`; it proves it only in the (non-universal) `L=1` case.
What survives: (i) the Steps 1,3,4,5 reduction as a correct CONDITIONAL result;
(ii) the unconditional structural fact that `>=2` bad slopes force `g` within
`2R3+4` of `C`; (iii) an explicit family of `L>1` configs (rank 2). The 3-slope
`L>1` configs found so far have `|Z| = 3 < R3+3`, so they do NOT yet disprove the
bound either -- whether `L>1` configs can reach `|Z| > R3+3` (which would CAP the
pin at `A_te-1`) is the reopened question. LESSON: the prior "evidence pin
extends" and "reduced to L1" were both undermined by a **biased search** (a425
basin); the correct next step is an UNBIASED search over `L>1` constructions.
