# M1 KoalaBear rank-nine zero-pencil tangent projection v1

This packet certifies one local source-bound lemma.  For one fixed SP3 sparse
translation, every slope admitting an eligible zero-codeword witness is in
the fixed tangent image

```text
{-epsilon_0(x)/epsilon_1(x) : x in Sigma, epsilon_1(x) != 0}
```

and therefore there are at most `|Sigma| <= j = 981104` such slopes.  The
projection is existential over all eligible witnesses at each slope.  Exact
support-wise noncontainment is the hypothesis that forces a nonzero source
coordinate and hence the tangent ratio.

The certificate also replays an exact `GF(11)` logical control.  It derives two
zero-codeword-witness slopes from raw sparse words, verifies their
zero-codeword
agreement supports, checks toy Reed--Solomon noncontainment by exact linear
algebra, and reconstructs the tangent image and cap.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py --check
python3 -O experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py --check
python3 experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py --tamper-selftest
```

The tamper suite covers statement quantifiers, the zero-pencil hypothesis,
the tangent image and cap, owner/payment status, selector rebuilding, toy
source values and witnesses, scope guards, source hashes, exact JSON parsing,
and the frozen payload hash.

The load-bearing predecessors should also pass:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --check
```

## Scope

The local classification is the existing
`SPARSE_TANGENT_RANK9_CONDITIONAL_CAP`, not `UNPAID_PRIMITIVE`.  The global
tangent projector and source-family deduplication remain unproved.  The
zero-pencil term cannot be removed from the determinant-weighted atlas until
that payment is banked and a complete residual selector is rebuilt.  This
packet does not move the deployed ledger, bound the nonzero plant load, close
KoalaBear rank nine, determine `U_Q` or `U_A`, or authorize rank at least ten,
Lean, or stable-paper promotion.
