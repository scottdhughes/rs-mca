# A_te-2 upper bound reduces to a collinearity lemma

Status: the exact upper bound `LD_sw(C, A_te-2) <= R3+3` (a425's
`EXACT_A425_UPPER_OPEN`) is **PROVED modulo one collinearity lemma L1**. The
reduction below is verified two independent ways: adversarial logic review
(Codex) and CAS cross-check of its computational claims (Sage coding-theory
module). Dated 2026-07-06. Combined with the tangent floor `>= R3+3`, closing L1
would give `LD_sw(A_te-2) = R3+3` -- the pin extends one step past the two-core
range.

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

**L1.** The bad codewords are collinear in the parameter-respecting sense: there
are codewords `a,b` with `c_z = a + z b` for every `z in Z`.

Evidence: `L := #{distinct p_{z z_0}} = 1` in **1200/1200** tested configs
(m=16,17,20,21), and a CAS (Sage) confirms the bad codewords span **rank 1** on a
non-degenerate planted-code-line config (rank 0 for a425, whose bad codewords are
all the zero codeword). L1 is **not** implied by list-decoding (`g` is only
`2R3+4`-close to `C`, past the Johnson radius). It is the sole remaining crux.

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

## Status / honest scope

`A_te-2` remains **OPEN**, but is now reduced to the single crisp collinearity
lemma **L1** (all bad-slope codewords lie on one parameter-respecting code-line),
verified on two independent engines and in 1200 configs. This is a strict advance
on a425's `EXACT_A425_UPPER_OPEN`. No deeper certificate is emitted until L1 is
proved. L1 is a clean, self-contained target (a natural next proof attempt or a
formalization gamble).
