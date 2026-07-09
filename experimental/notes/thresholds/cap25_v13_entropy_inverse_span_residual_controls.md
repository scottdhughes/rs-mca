# CAP25 v13: residual controls for the F_p-span cell — thin-alphabet replication at q=121/125, a prime-field negative control, and a two-field-reading instantiation (PR #422 §6, three items)

Status: `CONVENTION` (§1 — the near-balance-per-field `R` choice inherited
from #422, the `#red=floor((R-1)/p)` thin/has-red split, the `(A)`-reading
offset formula `log|Omega|-R log p`, `excess_generic` reused unchanged) /
`AUDIT` (§2.1 — the confirmed absence of #422's own thin-alphabet-residual
source code, full branch-history grep) / `MEASURED` (§2 the `q=121`/`q=125`
`exc_cond` sweep and the has-red/thin split; §4 the two-field-reading offset
sweep and index survival at the `(A)`-balance `R`) / `PROVED-AT-TOYS` (§3 —
the `F_7` `index=1`/`dim_span_Fp=K_rank` identity, exact at the one toy
checked, not a general argument) / `OPEN` (§5 — what remains unresolved).

**Verifier:**
`experimental/scripts/verify_entropy_inverse_span_residual_controls.py`
(zero-arg, stdlib-only, self-contained — no lane imports; `RESULT: PASS
(250/250 checks)`, exit 0; ~29 s and ~21 MB peak RSS **on the authoring box**
— environment-specific, not gated; best-effort `RLIMIT_AS` guard, default
2 GB, tune/disable via `FP_RESID_AS_CAP_GB`, never fatal; data JSON
resolved relative to the script, `FP_RESID_DATA_DIR` overrides). Copies the
`GF` field class and the census/moment/rank machinery verbatim from PR
#422's `verify_entropy_inverse_fp_span_cell.py`, and extends its
`law_check` with two new fields (`offset_A_bits`, `offset_A_over_N`, the
`(A)`-reading bookkeeping of §4) that leave every previously-gated quantity
unchanged. Six tamper self-tests, three threading a corrupted value through
the live `geq`/`feq` gate.

**What this is / is not.** A **measurement-only** follow-on to PR #422
(`cap25_v13_entropy_inverse_fp_span_cell.md`, fetched read-only from branch
`thresholds-entropy-inverse-fp-span-cell`, not yet merged into main),
answering three items from its §6 `OPEN` list verbatim (`q=121/125`
residual replication, the full-alphabet `p=7` control, the two-field-
reading confirmation) — not the other two (`codim_Fp` vs. twist entropy is
PR #427's job; the `p in {2,3}` equal-fibers surjection is PR #428's proof
task). **It claims no theorem. Merge framing: an experimental measurement
note, asymptotic lane only, no finite claims.** It does **not** resolve
`prob:entropy-inverse-q`, produce a row-sharp `Q`, or touch any deployed
finite row (§6).

Lineage `#414 -> #416 -> #417 -> #420 -> #421 -> #422` (+ its review,
DannyExperiments 2026-07-08) `-> ` this packet, alongside siblings `#427`
(twist span-codimension census) and `#428` (`image=W_c` surjection
theorem). All three fetch #422 read-only and extend it without
contradiction.

---

## 1. Conventions `CONVENTION`

- **`law_check`/`exc_cond`/`excess_generic`/balance guard** — reused from
  #422 **unchanged**: `exc_cond=G2_cond/exp_cond` is the conditional excess
  on the predicted coset `W_c` (index accounting only); `excess_generic`
  divides `Gamma_2` of the moment curve by `Gamma_2` of a generic random
  `K^R` map of the same shape; `offset_over_N > -0.25` is the finite-balance
  guard (#420/#421) against the small-family Poisson trap.
- **Per-field near-balance `R`, inherited from #422.** Its own headline
  table already used a *different* `R` per field near that field's own
  balance `R*` (regime JSON `balance_R`: `U16: 3`, `S27: 4`). Here that
  choice is made mechanical: `R` is fit near `R*=log2(Omega)/log2(q)` at the
  sweep's own `(N,a)` — `CONVENTION`, not re-derived per point.
- **The `#red=0` thin/has-red split (#422 §2.3's own criterion, reused, not
  new).** `#red=floor((R-1)/p)` counts Frobenius-reducible columns. At the
  near-balance `R` for a large prime (`p>=5`), `R<=p` typically, so `#red=0`
  — the *only* surviving constraint is the coord-0 head law (`s_0 in
  c.F_p`), confining the head to a genuinely thin `p`-element sub-alphabet
  of the `q`-element `K`: "thin-alphabet" as operationalized here (§2.1).
- **The `(A)`-reading offset (repair (A) of #422 §3, new bookkeeping).**
  `offset_A_over_N := (log2(Omega) - R log2(p))/N`, replacing `log2(q)` by
  `log2(p)` — normalizing by the `O(1)` base field `B` (`|B|=p`) while
  columns still live in the growing point field `E=K` (`|E|=q`). A pure
  bookkeeping redefinition; changes no census, index, or `exc_cond`.

---

## 2. M1 — thin-alphabet residual replication at `q=121`, `q=125`

### 2.1 What is and is not recoverable `AUDIT`

#422 §4 reports: *"The residual-above-`W` conditional excess has an
intrinsic floor `~1.44` at balance; the `N`-sweep is `1.05 -> 1.16 -> 1.40 ->
1.44 -> 1.37` (`N=8..16`)."* Its §6 `OPEN` list asks to replicate this at a
third prime. **A full-history `git grep` across every local and remote
branch for `thin_alphabet`, `generic_floor`, `exc_cond_mean` finds exactly
one hit: the output recorded in `cap25_v13_entropy_inverse_fp_span_cell_
nulls.json`.** No script on any branch computes them. Bit-for-bit protocol
replication is therefore impossible from the committed artifacts, and this
packet does not attempt it. What follows is a reconstruction built **only**
from #422's own exact, already-gated `exc_cond` primitive, applied via an
explicit, gated `N`-sweep — it will **not** reproduce `1.05..1.44`
bit-for-bit, but it answers the same question honestly.

### 2.2 Measured sweep `MEASURED`

Signed slice, `rho=ones`, `a=floor(N/2)`, `N in {8,10,12,14,16}` (`{8,10,12,
14}` for the has-red baseline fields, to bound runtime — §5). `R` is each
field's own near-balance value (§1):

| field | `p,k` | `R` | regime | `exc_cond` (`N=8,10,12,14[,16]`) | at-balance peak |
|---|---:|---:|---|---|---:|
| F16 | `2,4` | 3 | has-red (`red=[2]`) | `1.038, 1.014, 1.003, 1.001` | `~1.00` |
| F27 | `3,3` | 4 | has-red (`red=[3]`) | `0.998` (`N=14` only) | `~1.00` |
| F49 | `7,2` | 3 | **thin** (`red=[]`) | `1.363, 1.514, 2.039, 1.700` | `2.04` (`N=12`) |
| **F121** | `11,2` | 3 | **thin** (`red=[]`) | `3.22, 16.00, 12.29, 7.93, 4.83` | `7.93` (`N=14`) |
| **F125** | `5,3` | 3 | **thin** (`red=[]`) | `1.39, 1.99, 4.30, 6.46, 5.60` | `6.46` (`N=14`) |

("at-balance peak" = the largest `exc_cond` among the `N` that pass the
`offset_over_N > -0.25` guard.) The `F27` row is bit-identical to #422's own
published `S27` `exc_cond=0.9979801241245693` (gated exactly), validating
the copied `law_check` machinery independently of the reconstruction.

**Reading and answer to the OPEN question.** The has-red fields sit at
`exc_cond~1` throughout, matching #422's already-proved mechanism
("conditioning on `W` removes all the excess"). All three thin fields —
`F49` and the two **new** primes — show a **bounded but clearly
non-trivial** residual: `2x`-`16x`, nowhere near the `>100x` main-mechanism
scale, peaking near the balance guard and (for `F121`) falling past it, the
same qualitative shape #422 reports even though the magnitudes differ
substantially from its `~1.44`. So the phenomenon — a bounded, non-1
residual in the `R-1<p` corner — **is measured to persist at both new,
larger primes**, i.e. it is **not** a `p in {2,3,7}` coincidence in the
qualitative sense; but it is **not a universal constant `~1.44`** either —
the at-balance peaks (`2.04, 7.93, 6.46` for `p=7,11,5`) vary by nearly
`4x` across three points, with no monotone trend recoverable from a sample
this small.

---

## 3. M2 — full-alphabet `p=7` control (prime-field negative control) `PROVED-AT-TOYS`

`T=` all of `F_7^x={1,...,6}` (`N=6`, the **full** prime field unit group),
`K=F_7` (`k=1`). Per #422 §7's own nonclaim, the `F_p`-span cell is
**definitionally absent** at a prime field (`F_p`-span **is** the
`K`-span). This also instantiates `cor:large-characteristic-fourier-
examples` (`experimental/grande_finale.tex` L949, corollary statement L950,
verbatim):

> If \(T=E=\F_p\), \(m/p\to\rho\in(0,1)\), and \(w=o(\sqrt p)\), then the
> leaf is strongly Fourier-flat.

— the same `T=E=F_p` corner, approached from the Fourier-flat side.

Signed, `rho=ones`, `R=3`, `a=3` (`offset_over_N=-0.183`, passes the
guard). Gated exactly:

| quantity | value | reading |
|---|---:|---|
| `law0_violations` | `0` | coord-0 collapse — **trivially**: `s_0` already `in K=F_7` |
| `dim_span_Fp = K_rank` | `3 = 3` | **exactly equal** |
| `ambient_Fp = K_rank_full` | `3 = 3` | both **full** |
| `pred_W` | `343 = 7^3 = q^R` | predicted coset is the **entire ambient** |
| `index = [K^R:W_c]` | **`1`** | **no index inflation, exactly** |
| `exc_cond` / `excess_generic` | `1.008` / `1.044` | `~1`, no excess |

The arithmetic is exact, not approximate: at `k=1`, `c0=p=q`, so `pred_W =
q . q^{R-1} = q^R` identically — the coord-0 "constraint" ranges over all of
`c.K`, i.e. constrains nothing. A clean, exact confirmation of the
deployed-row immunity argument at an actual toy: `K=F_p` kills the cell by a
literal index-formula identity, not an approximation.

---

## 4. M3 — two-field-reading confirmation (repair (A)) `MEASURED`

`F16` (`q=16,p=2,k=4`), `N=15` (`=N_real`, unsigned, `a=8`, `rho=ones`), `R`
swept `3..14`:

| `R` | `offset_over_N` (B, `log q`) | `offset_A_over_N` (A, `log p`) | `index` | `exc_cond` |
|---:|---:|---:|---:|---:|
| 3 | `+0.043` | `+0.643` | `256` | `0.998` |
| 4 | `-0.223` | `+0.577` | `256` | `0.976` |
| 8 | `-1.290` | `+0.310` | `65\,536` | `0.911` |
| 12 | `-2.357` | `+0.043` | `16\,777\,216` | `1.000` |
| **13** | `-2.623` | `-0.023` | **`268\,435\,456`** | `1.000` |
| 14 | `-2.890` | `-0.090` | `268\,435\,456` | `1.000` |

The `(B)`-reading straddles `0` at `R in {3,4}` (matching #422's own `U16
balance_R=3`); the `(A)`-reading straddles `0` at `R in {12,13}` instead —
a factor of `~k=4` apart, exactly as repair (A) predicts (`R*_A ~ k.R*_B`,
since `log q = k log p`). **The span-cell index inflation survives at
balance under the `(A)`-reading**: at `R=13`, `index=268\,435\,456` and
`exc_cond=1.000` — the exact-index mechanism is fully intact there, the
same kind as #422's `S27`/`U16o` rows, at a different `R`.

**Scope, stated once.** The `(A)`-reading offset formula is this packet's
own bookkeeping instantiation of repair (A) (§1), not part of #422's
printed atom. `offset_A_over_N approx 0` at a finite `R=13` toy realizes
the *intent* of the repaired reading; **it does not certify the atom's
printed asymptotic clause** `log|Omega^circ|-R log|K|=o(N)`, which is a
limit statement no finite toy can satisfy or falsify — the same discipline
#422 uses for its own `(B)`-reading toys. Gated explicitly
(`printed_oN_clause_claimed=False`).

---

## 5. Guards, verification, and `OPEN` `AUDIT` / `OPEN`

`250/250` checks, ~29 s, ~21 MB peak RSS, everything recomputed from scratch
and gated against the committed data JSON. The M1 grid is deliberately
smaller than a full `5`-point sweep on every field (`F16`/`F49` drop
`N=16`, `F27` keeps only its `N=14` cross-check) to bound the dominant cost
(`C(N,a).2^a` per signed point); the two new primes keep the full `N=8..16`
grid. Six tamper self-tests: three thread a corrupted value through the
live `geq`/`feq` gate (a faked `exc_cond`, a faked span`=`rank identity, a
faked `index`) and confirm it is caught before retracting; three are direct
structural checks (the thin/has-red classification rejects a mislabeling of
the baseline fields; the `(B)`-reading offset is confirmed far from
straddling zero at the `(A)`-balance `R`; a full `q x q` dual-path
field-multiply sweep on both new primes).

**What remains open.** *Magnitude vs. characteristic*: three thin-regime
peaks (`2.04, 7.93, 6.46` for `p=7,11,5`) do not settle whether the residual
grows with `p`, `q`, or is finite-`N` noise — a `p in {13,17,19,...}` sweep
at matched `(N,R)` is the natural next step. *The uncommitted original
protocol*: if #422's own thin-alphabet script resurfaces, a true
bit-for-bit replication would supersede §2's reconstruction. *M3 is one
field*: whether the `~k`-factor separation between the two balance `R`'s
holds as cleanly at other `(p,k)` (e.g. `F121`/`F125`) is untested here.

---

## 6. Weave and nonclaims `AUDIT`

- **PR #422** (direct predecessor, not yet merged; fetched read-only from
  `thresholds-entropy-inverse-fp-span-cell`). Answers three of its §6
  `OPEN` items verbatim; reuses its `law_check`/`exc_cond`/`excess_generic`/
  balance-guard machinery unchanged (§1), extending only with the
  `(A)`-reading offset field. **The #422 review** (DannyExperiments,
  2026-07-08) established the `c`-form laws and the sharp `floor((R-1)/p)`
  criterion this packet's thin/has-red split reuses directly.
- **PR #427** (sibling, fetched read-only from `thresholds-fp-span-codim-
  census`, not yet merged) answers #422 §6's *codim vs. twist entropy*
  item; **PR #428** targets the `p in {2,3}` equal-fibers `image=W_c`
  surjection (a proof task). This packet answers three *different*,
  cheap-measurement items; none of the three overlap.
- **`cor:large-characteristic-fourier-examples`** (`grande_finale.tex`
  L949–956) is the `T=E=F_p` corollary M2 instantiates from the span-cell
  side.
- **This packet consumes no upper cell and instantiates no `U(1116048)`
  certificate.**

**Nonclaims.** Does **not** prove or refute `prob:entropy-inverse-q`, and
does **not** resolve any of #422's three ledger options (its §2.4) — it
only measures three items its §6 queued. **No finite claim of any kind:**
nothing here touches `prob:row-sharp-q` / `def:q-row-atom`, certifies no
deployed finite safe row, and instantiates no `U(a_0+1)<=B*` certificate at
any deployed row; asymptotic-lane only. **M1 is an explicit reconstruction,
not a replication** (§2.1): the exact shape `1.05..1.44` reported by #422
is not reproduced and is not claimed to be; only the qualitative phenomenon
(bounded, non-1, present across all five tested characteristics) is
measured and gated. **M2 reinforces, and does not extend, the prime-field
immunity nonclaim** already stated by #422 §7: a fresh toy-exact
confirmation at `F_7`, not a new argument, and it says nothing about any
deployed row beyond what #422 already stated. **M3's `(A)`-reading offset
is this packet's own bookkeeping convention** (§1, §4), not a claim that
the atom's printed asymptotic normalization clause is satisfied by any
finite toy — stated explicitly and gated. No theorem is promoted anywhere
in this note; M2's `index=1`/`dim_span_Fp=K_rank` identity is
`PROVED-AT-TOYS` (one exact toy, not a general argument) at most.
