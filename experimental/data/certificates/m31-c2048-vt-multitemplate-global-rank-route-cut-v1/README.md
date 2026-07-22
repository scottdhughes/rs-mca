# M31 `c=2048` VT multitemplate global-rank route cut v1

This packet is an exact zero-payment successor to PR #1045.  It identifies
primitive global error-locator lines with positional partial-template blocks,
proves the exact two-support inverse-residue escape criterion, and exhausts
what the existing fixed-template module-rank theorem implies for a failed
whole-boundary `VT` packet.

Exact dependency:

```text
PR:      #1045
head:    17883a3087b6c84ba72654cb847eeed1614e4b4b
payload: d0aa51bd3811ad5e93269f7174afc249fc2865715cb484e41cd233bcab775960
```

The module-rank and fixed-template inputs are bound respectively to PR #1044
payload `c164f24810e0ed5015b3e538607e8867c7f634d5797de645c455447a08aaa303`
and PR #1043 payload
`99febb07f517aac958e55eeba466e268a4ada793ef7960a189374603ea4a3ec9`.

## Certified route cut

- Every deployed boundary error locator has a coordinate vector in the
  degree-filtered `F`-vector-space slice
  `F[T]_(<=479)^138 direct_sum F[T]_(<=478)^1910`; monic differences lie
  in the 981,129-dimensional companion slice
  `F[T]_(<=479)^137 direct_sum F[T]_(<=478)^1911`.
  These slices sit in the free module `F[T]^2048`; they are not themselves
  `F[T]`-submodules.
- One primitive `F(T)` locator line is exactly one positional partial-template
  block.  This locator linear rank is not the parent's translated quotient-
  message difference rank.
- For two supports and `x in E minus F`, the declared escape is absorbed exactly when the
  canonical inverse residue
  `q=B(x)^(-1)A_x` has degree `d-1<w=67,447`, equivalently exactly when
  `d<=w`.  If `x in E intersection F`, the pair never absorbs that escape.
  Same-word distinct boundary supports have `d>=w+1`, so pairwise absorption
  never occurs there.
- A live failed-VT packet either has a heavy fixed-template line and enters
  `UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP`, or has at least 542,164,
  986,676, or 986,896 distinct template lines at the three live gates.
- The current block caps and fixed-template threshold/module implications
  permit both abstract load shapes.  The dispersed one-per-line model does
  not assert pairwise distance, VT incidence, or simultaneous realization.
  Those blockwise inputs cannot prove `VT(U)` without a new guarded
  multitemplate line-incidence theorem.
- Canonical depth-32 `H=1` source cosets are injectively labeled by
  `(P_ag,eta,lambda)` whenever `v+v'<=32`.  The five largest separate floors
  formally exceed `B_star` by 429,716 but belong to distinct cosets and
  cannot be summed.  A common root-free cofactor through degree 136 preserves
  this separation; at the first higher degree the current uniform degree
  certificate must refine to depth 33, while individual extra cancellation
  remains possible.  There the existing pigeonhole certificate supplies only
  floor one for each top-five profile.  That floor is not an upper bound on
  attained buckets.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.py --tamper-selftest
HOME=/tmp TMPDIR=/tmp /usr/local/bin/sage experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.sage
```

Artifact regeneration is deterministic:

```bash
python3 experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.py --write
```

Independent schema replay:

```bash
/Users/scott/math_code/.venv/bin/python -m jsonschema \
  -i experimental/data/certificates/m31-c2048-vt-multitemplate-global-rank-route-cut-v1/manifest.json \
  experimental/data/schemas/m31_c2048_vt_multitemplate_global_rank_route_cut_v1.schema.json
```

## Scope guard

The concentrated and dispersed load vectors test only the currently proved
block caps and fixed-template threshold implications, not the pairwise or VT
incidence hypotheses, and are not received-word constructions.
The realized 6,796,405-member fixed-remainder source remains below the live
budget and is not promoted to a counterexample.

The new string
`UNPAID_VT_MULTITEMPLATE_GUARDED_LINE_INCIDENCE` is a diagnostic, not a
first-match owner.  `VT(U)` remains open.  The active boundary and global
terminals remain unchanged, every high LIST atom remains null, and ledger
movement is zero.
