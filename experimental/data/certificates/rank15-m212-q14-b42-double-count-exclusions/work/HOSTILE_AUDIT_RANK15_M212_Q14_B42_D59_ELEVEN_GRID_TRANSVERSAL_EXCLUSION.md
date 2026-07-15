# Hostile audit: `q=14`, `B=42`, `D=59` eleven-grid-transversal exclusion

## Verdict

`ACCEPT`, with high confidence, for the exact `D=59` boundary subcell.

The audit independently re-enumerates all 958 moment profiles and the three
local packing survivors.  It then checks the two elementary heavy-line cuts
and the complete source-realized grid argument for the third row.

Frozen claimant:

```text
theorem  52fedf346ed2dfda2611f2aacb651c5d813c85491ffe43f47534fff8d47b7f98
verifier cca8e0d20dabbed8ab294ac5fd5fce135fcb4e47b8ba5789c9ab2ff39a4f5579
expected a47cad4e8533c208ee0015d83313c5b606a40027d874b21d421c10412ee2aa98
```

## Checks

1. Ascending-weight enumeration of
   `sum w c_w=56`, `sum w^2 c_w=412` gives 958 profiles.
2. Independent minimal-group packing leaves exactly the three printed rows.
3. Heavy incidence gives at most two no-heavy lines in rows one and three,
   and at most three in row two.  The multiplicity-5 intersection counts
   eliminate rows one and two.
4. In row three, `Q` forces exactly two no-heavy lines and all three heavy
   sides.  Each multiplicity-4 point lies on exactly one no-heavy line and
   connects separately to all three heavy points.
5. The multiplicity-13 center has only ten lines after its two sides and its
   `Q` connector.  Since a line through it meets each no-heavy line once,
   those ten lines force a `10+10` split and pair every small point.
   No center-low line can coincide with either no-heavy line, because the
   latter contains no heavy point; it cannot coincide with a heavy-pair side,
   because that side contains two heavy points and the low-point pair is
   already owned by its no-heavy line.
6. The opposite heavy side has double degree 13 and exactly thirteen
   remaining lines, so all its remaining intersections are distinct doubles.
   Each of the eleven center-low lines therefore uses its sole double there
   and contains thirteen points of the same `13 x 13` pencil grid.
7. Literal `F_p` rationality descends from the parameter-point dualization:
   every listed parameter point is in `F_p^2`, projective duality gives a
   line with `F_p` coefficients, and subsequent deletion only takes a subset.
   Eleven grid transversals give a stabilizer of a 13-set of order at least
   11, hence exactly 13.  This contradicts `(p-1) mod 13=10`.

## Scope

The audit accepts `D=59` only.  The next exact double count is `D=60`.
