# Hostile audit: `D=61` correlation exclusion

## Verdict

**PASS.**  The claimant pays exactly the `q=14,B=42,U=E=0,D=61` cell.
It does not pay `D>=62` or transport a recurrence by itself.

The audit independently re-enumerates the moment profiles and implements the
disjoint-group gate without invoking the claimant wrapper.  It reproduces
1,458 exact profiles and the same ten survivors.  Six survivors violate the
four-heavy incidence ceiling and three further survivors have too many
multiplicity-5 points for their at most three no-heavy lines.

For the remaining `[4^24,14^2,15]` row, the audit checked the omitted-looking
degeneracies explicitly:

* `x-z=1`, every small point needs a no-heavy line, and one such line cannot
  carry all 24, so exactly two no-heavy lines and all three heavy sides occur;
* `AC,BC` cannot contain a small point by the line equation; a small point on
  `AB` needs both no-heavy lines and is therefore precisely their intersection;
* if the no-heavy intersection is ordinary, all 24 small points are low-pencil
  grid points and the `A` pencil forces the `12+12` split;
* if it is small, the split is `12+13`, the intersection point lies on `AB`,
  and exactly the other 23 small points are low-pencil grid points.

The two correlation calculations independently reproduce selected mass floors
139 and 142, quotient-support caps 18 and 15, and the stated Kneser
contradictions.  The only surviving stabilizer in the ordinary case is order
16; its three unselected correlations each have mass at least eight, giving
the sharp selected cap 120.  The small-intersection case has no surviving
stabilizer order.

All multiplicative parameters remain in the literal prime field because the
source arrangement lines are individually `F_p`-rational.  No algebraic-
closure subgroup is imported.

## Frozen claimant pins

```text
c156e7c132c48b39e3e216416188751ed297fd7698fe034a768a5dc02561c374  work/RANK15_M212_Q14_B42_D61_CORRELATION_EXCLUSION.md
4ee4014fda27e3c309fbc26a977effd40bc82342ea6ab44c18c4921200dd50bd  work/verify_rank15_m212_q14_b42_d61_correlation_exclusion.rb
e9613c433320928453c3bd34f5ff18877c74360fa89016e39d14c209ad499c75  work/verify_rank15_m212_q14_b42_d61_correlation_exclusion.expected.txt
```

The independent verifier must byte-match its expected output under both
warnings-enabled and warnings-suppressed Ruby runs.
