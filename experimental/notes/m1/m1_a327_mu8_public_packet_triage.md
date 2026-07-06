# M1 a=327 mu8 Public-Packet Triage

Status: `PARTIAL / EXPERIMENTAL / NOT_BOARD_READY`.

This remains an `INTERLEAVED_LIST` workstream for
`RS[F_17^32,H,256]`.  The denominator is `17^32`, and
`mca_counted=false`.  This packet does not claim MCA `N_bad`, protocol
soundness, ordinary list decoding beyond the stated interleaved-list predicate,
global `Lambda_mu(C,327) <= 6`, exact `Lambda_mu`, or exact `delta*_C`.

## Purpose

This note compresses the current local `mu_8` a=327 work into a public-usefulness
triage.  The guiding question is whether the local work is ready for a public
repo PR or board update.

The answer is no: there is no exact a=327 witness.  The useful public-shaped
object is a possible route-cut packet, not a certificate.

The machine-readable triage is:

```text
experimental/data/m1_a327_mu8_public_packet_triage.json
```

It was generated from the full local `mu_8` worktree by:

```text
python3 experimental/scripts/mine_m1_a327_mu8_public_packet_triage.py --write --json
```

This compact packet includes the primary evidence ledgers named in the triage
hash map.  It does not include every intermediate scan ledger from the local
worktree, so the miner is provenance tooling rather than the public replay
command for this PR-sized packet.

It is checked by:

```text
python3 experimental/scripts/verify_m1_a327_mu8_public_packet_triage.py --json
```

The miner also scans the local witness-audit ledgers.  In the current
worktree:

```text
witness ledgers scanned: 62
EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS ledgers: 0
```

## Evidence Summary

### Rank-one `mu_8` carriers

The rank-one carrier obstruction is clean:

```text
ansatz: q(Y)=u*f(Y), deg(f)<32
selected incidence ceiling: 2147
required selected incidences: 7*327 = 2289
gap: 142
status: MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION
```

This is theorem-shaped, but only for pair-visible rank-one `mu_8` carriers.
It is not a global `mu_8` route cut.

### Rank-2 `mu_8` carriers

The current rank-2 menus remain support-infeasible:

```text
adaptive front:        min support 314, total incidence 2202
feedback front:        min support 316, total incidence 2224
current menu ceiling:  min support 317, total incidence 2224
support/pair candidates: 0
```

The aggregate adaptive sweep is consistent with that diagnosis:

```text
adaptive ledgers scanned: 50
best min support: 317
best total incidence: 2224
support gap: 10
selected incidence gap: 65
support/pair passing ledgers: 0
```

The mined current frontier has:

```text
support vector: [318,317,318,318,318,317,318]
label deficits: [9,10,9,9,9,10,9]
selected incidence gap: 65
pair max: 254
block histogram: 272 two-blocks + 240 all-label blocks
ratio-line histogram: 34 singleton ratio lines
```

This says the rank-2 bottleneck is still menu/support expressivity.  Since no
support/pair-passing schedule exists, the rank-2 exact interpolation gate has
not produced a witness-relevant system.

Near-front exact diagnostics have also been negative:

```text
rank-2 exact/near-front ledgers scanned: 17
exact systems tested: 39
positive nullity systems: 0
max best nullity: 0
```

### Rank-3 `mu_8` fixed menu

The current rank-3 fixed menu can pass support/pair, but exact Sage audits stay
full rank:

```text
support vector: [327,327,327,327,327,327,327]
selected incidences: 2289
pair max: 255
exact matrix: 156 x 96
rank/nullity over GF(17^32): 96 / 0
```

The singleton fixed-point cap boundary is informative:

```text
max singleton fixed groups 22: support/pair pass, exact full rank
max singleton fixed groups 21: no support/pair pass
max singleton fixed groups 20: no support/pair pass
max singleton fixed groups 18: no support/pair pass
max singleton fixed groups 12: no support/pair pass
max singleton fixed groups 5:  no support/pair pass
```

The row-pressure audit explains the failure mode.  Even when the selected
schedule has fixed-point histogram `{1:22, 2:7}`, the dependency-last pivot core
can still choose a full-rank core from:

```text
28 ZERO groups + 6 singleton fixed POINT groups
dependency rows in core: 12
dependency groups in core: 6
rank/nullity: 96 / 0
```

Thus, for the current fixed menu, removing the six-singleton pivot escape is
incompatible with support/pair.  More mutation of the same menu is unlikely to
help.

The broader exact sweep reinforces that this is not an isolated Sage result:

```text
rank-3 exact ledgers scanned: 50
rank-3 exact systems tested: 167
positive nullity systems: 0
row-pressure ledgers scanned: 28
row-pressure systems tested: 76
positive row-pressure nullity systems: 0
```

## Triage Decision

```text
board_ready: false
exact_a327_witness: false
recommended_public_action: do_not_open_board_pr_yet
route_cut_candidate: true
```

The route-cut candidate is only local:

1. rank-one `mu_8` carriers are structurally cut;
2. current rank-2 menus are support-infeasible;
3. current rank-3 fixed menu passes support/pair only with enough singleton
   fixed groups to expose full-rank pivot cores.

## Next Best Attack

Do not keep squeezing the same fixed rank-3 menu.

The next constructive step should introduce a new dependency family:

1. return to rank-2 feedback carrier synthesis with better balanced carrier
   planes, or
2. build rank-3 menus whose dependency rows cannot be bypassed by singleton
   fixed groups, or
3. formalize the repeated full-rank singleton pivot pattern as a module/syzygy
   obstruction with Macaulay2 or Singular.

## Tools

Use:

```text
OR-Tools CP-SAT     support/pair scheduling
Sage GF(17^32)      exact rank, kernel, and witness audits
Python JSON scripts reproducibility and packet triage
Macaulay2/Singular  only if converting the full-rank pattern into a module/syzygy obstruction
```

Do not prioritize `msolve`, PARI/GP, or Wolfram for the current inner loop.
