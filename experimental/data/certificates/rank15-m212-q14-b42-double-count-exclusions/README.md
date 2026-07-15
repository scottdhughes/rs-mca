# Rank-15 `M=212`, `q=14`, `B=42` certificate packet

This packet supports

```text
experimental/notes/l2/rank15_m212_q14_b42_double_count_exclusions.md
```

The `work/` directory contains six full proof notes, six claimant verifiers,
six frozen claimant outputs, six independent hostile verifiers, six frozen
hostile outputs, and six hostile audit reports. Three source-interface files
and the exact packing replays are included because the hostile verifiers pin
them by SHA-256. The `source/` directory preserves the literal locator normal
form at the source commit.

Run all finite replays from this directory:

```bash
cd experimental/data/certificates/rank15-m212-q14-b42-double-count-exclusions/work
for f in verify_rank15_m212_q14_b42_*.rb \
         audit_rank15_m212_q14_b42_*.rb; do
  ruby --disable-gems -W0 "$f"
done
```

Every script is standard-library only. No downloaded binary or dependency is
required. `SHA256SUMS.txt` covers every preserved input and expected output.

The source pin is

```text
origin/main@2633895a66d3edf516120a87b2eb18c994f977ab
```

The packet pays only `D=39` and `D=44..61` under the hypotheses in the theorem
note. It does not consume the held `D=62..64` claimant and makes no recurrence
or official-score claim.
