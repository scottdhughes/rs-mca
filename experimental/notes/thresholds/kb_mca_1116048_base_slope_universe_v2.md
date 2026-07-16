# KoalaBear MCA 1116048 base-slope universe ledger v2

Status: PROVED UPPER-NUMERATOR REPLACEMENT / PARTIAL LEDGER.

This note replaces one conservative charge in the KoalaBear MCA
`A=1,116,048` first-match ledger.  It does not prove the row safe.

## Counted object

For a fixed received pair, the MCA numerator is the number of **distinct bad
slopes**.  It does not count witnesses, supports, SPI charts, or affine image
cells.  This is the definition in `experimental/rs_mca_thresholds.tex`.

Let

```text
B = F_p,
F = F_(p^6),
p = 2130706433.
```

After first-match branches 1 through 6 have removed their assigned slopes,
let `R_base` be the remaining bad slopes that lie in `B`.  Set inclusion gives

```text
R_base subseteq B,
|R_base| <= |B| = p.
```

This is uniform in the received line.  Its coordinates may be arbitrary in
`F`; no base-valued syndrome packet, cyclotomic lift, SPI chart, or affine-row
adapter is required.  Honest and finite-only base slopes are both covered.

The charge is global once.  Earlier first-match owners remain disjoint; branch
7 is widened and renamed from `base_generated_field_collision` to
`residual_base_slope_universe`.  The older generated-collision lemma remains a
valid optional refinement, but its `t*p` bound is replaced, not added.

## Exact arithmetic

For

```text
n = 2097152,
k = 1048576,
A = 1116048,
j = 981104,
t = 67472,
w = 67471,
q_line = p^6,
B_star = floor((q_line-1)/2^128)
       = 274980728111395087,
```

Because `q_line` is odd, this is also exactly
`floor(q_line/2^128)`, the integer budget for the full finite-slope
challenge denominator.

the predecessor charge was

```text
t*p + 471447040 = 143763495894416.
```

The corrected proved paid baseline is

```text
p + 471447040 = 2602153473.
```

Thus

```text
charge reduction = 143760893740943,
B_rem             = 274980725509241614,
K_rem             = floor(B_rem*p^w/binom(n,j))
                  = 4807520.
```

The terminal quotient amount `471447040` is imported unchanged from the
predecessor first-match packet.  It precedes branch 7, so the residual
base-slope universe is disjoint from it by construction.

That imported raw-support charge is also a valid slope charge: if one
noncommon support explained two distinct finite slopes, subtracting the two
explaining codewords would explain both received coordinates on that support.
Thus each noncommon support contributes at most one finite bad slope.  This is
the fixed-support slope uniqueness statement in
`experimental/rs_mca_thresholds.tex`.

## Why the SPI adapter is not the base-slope gate

The proposed coarse SPI-chart-to-affine-row adapter asks for more than the
numerator needs.  A base-valued slope does not force the received line or its
syndrome rows to be base-valued, and a coarse pivot chart need not have a
constant first honest-defect row across all of its split supports.  Those
issues matter for a chart-level generated-collision classifier, but neither
can enlarge a subset of `F_p` beyond `p` slopes.

Accordingly, deployed SPI work should now focus on the unresolved complement

```text
F_(p^6) minus F_p.
```

The 48-pattern GF(19) row remains only a machinery control.

## Verification

Run

```bash
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --check
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --tamper-selftest
```

The verifier binds the MCA definition, the slope-level first-match theorem,
and the predecessor packet; replays the exact big-integer multiplier; and
rejects replacement/addition confusion, owner-order drift, non-global charges,
source-pointer aliases, numeric type drift, false inequality closure, and
malformed JSON.

## Verdict and next lane

The base-slope replacement is proved.  The deployed row remains **YELLOW**:
`U_Q`, `U_A`, and the extension-valued residual are open, so the inequality

```text
U_paid + U_Q + U_A <= B_star
```

is undecided.

The next atlas should quantify only over residual slopes in
`F_(p^6)\F_p`, after the frozen earlier owners.  Any coarse chart used there
must be refined by its actual incidence and first-defect strata; no chart is
paid merely because its slope happens to be base-valued.

## Nonclaims

- This note does not prove the KoalaBear MCA row safe.
- It does not bound extension-valued slopes.
- It does not determine `U_Q` or `U_A`.
- It does not add `p` to the old `t*p` charge; it replaces that charge.
- It does not count or pay support multiplicity.
