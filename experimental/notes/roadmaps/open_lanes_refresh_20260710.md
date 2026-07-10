# Open-lanes refresh — mining of the upstream repo (2026-07-10)

Supersedes `open_certificate_lanes_mined.md` (2026-07-06), which is now stale:
the entire `asymptotic_rs_mca.tex` "compact proof" sprint (PRs #431-449) landed
since, and most `PROVABLE` DAG nodes have been claimed. This note re-maps the
current ownership + genuinely-open remainder, so no agent re-runs the same scout
or collides. Method: per-node status was read from the actual note (NOT the DAG
JSON — see the stale-status warning below), plus PR authors and git recency.

## Headline

The repo has converged onto ONE object: the compact asymptotic RS-MCA frontier
proof (`experimental/asymptotic_rs_mca.tex`). Its audit-identified gaps are being
closed in a fast sprint. The clean analytic-NT / certificate lanes are claimed.
The genuinely-open remainder is the set of deep cruxes (all `sqrt(p)`- or
`WALL`-class) plus a few deep conjecture cores.

## The DAG `PROVABLE` labels are STALE (re-confirmed)

`prize_dag.json` (337 nodes: 102 PROVED / 94 TARGET / 68 PROVABLE / 26 CONJECTURE
/ 19 CONDITIONAL / 12 TEST / 6 WALL / 10 REFUTED). The 68 `PROVABLE` are NOT a
work queue — many are already PROVED in their notes. Verified-stale examples:
`graded_collision_radius`, `collision_norm_criterion`, `are_exceptional_density`,
`are_sharp_constant`, `kernel_lattice_reframing`, `f_support_lattice` all read
`Status: PROVED` in-note (with verifiers + certificates) while the DAG says
`PROVABLE`. **Always read the node's note (and the `m1/` prefix = M1-owned)
before claiming.**

## Current ownership map (who is where — do not collide)

| Area | Owner | State (2026-07-10) |
|---|---|---|
| `asymptotic_rs_mca` proof gaps: B1 convention (#436/#439/#440), A6/add-back (#441/#445), B3 (#443), pole lower-side (#442), stdlib spine (#438), target-norm compiler (#449) | **holmbuar** (+ latifkasuli, avdeevvadim, DannyExperiments) | active sprint, closing out |
| e1-collision / value-set certificate cluster: `collision_norm_criterion`, `graded_collision_radius`, `single_swap_injectivity`, `exceptional_density`, `are_sharp_constant`, `kernel_lattice_reframing` | **AllenGrahamHart** / Codex | PROVED (verifiers + certs) |
| M1: `a327`/`mu8` rank-2 residue-line slope search; `fm1` first-moment | **avdeevvadim** | do NOT touch (separate terminal) |
| C9 image-normalized interface (`#439`) | **avdeevvadim** | tex interface repaired |
| M31 signed-`e_m` inverse `#434` (r~4 participation ratio, Chebyshev domain) | **holmbuar** | PARTIAL, open crux |
| census / Conjecture-F (`f_*`) / XR (`xr_*`) clusters | mixed | notes exist; mostly PROVED or audit-scoped |
| B1 second moment (`#448`) | **this (L1) terminal** | reduction + route-cut; SUBSUMED by C9 (see below) |

## Genuinely-open remainder (all deep)

These survived the scout as actually-open AND not obviously claimed, but every
one is a deep crux, not a clean win:

- **C9 — the Fourier/Sidon `L^1` flatness** (`def:sidon-paid`): `sum_{c!=0}|e_m(v_c)| <= C exp(o(N))`,
  the paper's IMPORTED input (`Cho26ModuliFinal`). Equivalent to: every `c` with
  large `|e_m(v_c)|` is "algebraic" (a major arc routed to C1-C8). This is the
  `sqrt(p)` / large-values-of-`e_m` wall, the actual prize engine, and it is
  UNCLAIMED. Our `#448` established the moment ladder `sum_c|e_m|^r`: C9 (r=1) /
  B1 (r=2, ours, subsumed by C9) / `#434` (r~4); all rungs share the `sqrt(p)`
  barrier (our r=2 T5->NG route-cut; `#434`'s r=4 dead-route margins). Attacking
  C9 = attacking that wall; our `b2` minimal-value-set work is the closest handle.
- **XR-inverse** (`xr_inverse` CONJECTURE, `xr_wall` WALL): the Johnson-graph
  exchange-rigidity inverse theorem (large `E_k` => structured), the 2nd L1 route.
  The "easy-direction" imports (`xr_kms_import`, `xr_small_set_engine` = KMS 2-to-2
  / KLLM global hypercontractivity) are the only sub-parts near-tractable, but the
  route's payoff sits behind the WALL. L1-adjacent (crowded-adjacent).
- **Conjecture-F core** (`f_primitive_case`, `f_many_sparse_structure`,
  `f_pair_bound_envelope`, `perfiber` WALL, `spi_wall` WALL): plane-section /
  dual-code descent; deep algebraic-geometry conjecture with many sub-lemmas.
- The six `WALL` nodes (`graver_wall`, `monodromy_route`, `projected_locator_wall`,
  `perfiber`, `spi_wall`, `xr_wall`) are declared barriers — not lanes.

## Recommendation for this (L1) terminal

No clean uncrowded win remains; the honest options are (a) take on **C9** (our
lane, unclaimed, but the `sqrt(p)` wall — continuous with the `b2`/B1 arc), or
(b) hold at scoping (this note + the `#448` moment-ladder map) and monitor the
asymptotic sprint for a sub-piece that falls out. The `#448` finding that B1 is
subsumed by C9, and that the whole signed-`e_m` ladder shares one barrier, is the
current durable contribution; the next real math is behind the C9 wall.
