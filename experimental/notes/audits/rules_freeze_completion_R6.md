# Rules-freeze completion (R6): 2026-07-06 drift recheck, compiler-semantics freeze row, tower-case decision

- **Status:** AUDIT / citation packet (rules reading, not a math proof). 2026-07-06.
- **DAG nodes touched:** `rules_freeze` [TARGET], `certifier_uniformity` [TARGET], `f1_case_tower`
  [TARGET], with `field_cap_check` [PROVED], `generating_escape` [PROVED], `mixed_radix_frontier`
  [PROVED], `rules_m_reading` [PROVED] as inputs.
- **Sibling artifacts (do not duplicate):** `rules_freeze.md`, `field_cap_check.md`,
  `prize_rules_pinning.md`, `m_handling.md`, `axis8_generating.md`. This packet does the three things
  those left explicitly open: (i) a fresh **drift recheck** (the `rules_freeze` title's "SHA drift
  detector"; `rules_freeze.md` Non-Claims and `prize_rules_pinning.md` both defer it), (ii) the
  **compiler-semantics freeze-table row** the `rules_freeze` node asks to ADD, grounded in prize
  sources, (iii) recording the **Q0.1 / tower-case** decision correctly.
- **Sources:** ABF IACR ePrint 2026/680 p.5 (SHA `426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5`
  as pinned in `experimental/data/certificates/rules-freeze/rules_freeze.json`); live proximityprize.org
  (fetched 2026-07-06). **Provenance note (see "Reproducibility" below): items that require network
  access — the 2026-07-06 live-page re-fetch, the "no drift" conclusion, the live-page AI-policy
  wording, and re-hashing the actual ABF PDF against the pinned SHA — are AUTHOR ASSERTIONS not
  reproducible from the repository alone.**

## (i) Drift recheck (2026-07-06): no NEW drift since the 2026-07-03 pinning

`prize_rules_pinning.md` (checked 2026-07-02/03) established the repo-supported baseline: the live page
states the challenge and "assumes the field is sufficiently large," but does **not** print the caps
`k<=2^40`, `|F|<2^256` -- those live in the ePrint/blueprint only (`prize_rules_pinning.md` lines 15,
34, 70). An **author re-fetch on 2026-07-06** (not repo-reproducible) found the operative live-page
rules unchanged from that baseline:
- rates `rho in {1/2,1/4,1/8,1/16}`, `eps* = 2^-128`, list denominator `eps*|F|`, per-code challenge
  ("determine the largest `delta*_C` s.t. `eps_mca(C,delta*_C) <= eps*`"), partials/complementary
  results credited and awards splittable, peer-review + public posting required, formal verification
  encouraged-not-required, AI-aided allowed if human-verified.
- the `k<=2^40 / |F|<2^256` caps remain **ePrint-only** (still not printed live), matching
  `prize_rules_pinning.md`.
**Conclusion (author assertion):** no operative rule appears to have drifted between 2026-07-03 and
2026-07-06. Keep the standing caution (`prize_rules_pinning.md`): the live page labels statements
preliminary, so recheck again -- and re-hash the ABF PDF against the pinned SHA -- before any
public-submission text is finalized. The pinned ABF PDF hash is the authority of record.

## (ii) Compiler-semantics freeze-table row (the `rules_freeze` ADD request)

The `rules_freeze` node notes ask (quoted exactly from `prize_dag.json`):
> ADD TO THE FREEZE TABLE (crux-2-relevant): does a proved-correct per-row decision procedure emitting
> machine-checkable certificates satisfy the grand challenges' 'determine for each admissible C' — i.e.,
> are compiler semantics acceptable? The answer moves the certifier_uniformity burden dramatically.

This packet supplies that freeze-table row with primary-source grounding.

**Prize text.** ABF Sec.1: resolving the challenge "for a code `C` and `eps*` requires specifying a
`delta*_C in [0,1]` along with a **proof** that for all `delta > delta*_C` we have
`eps_mca(C,delta) > eps*`" -- stated **per code `C`**, not as a closed-form `delta*_C(F,L,k)` theorem.
The live page's partials/peer-review/human-verified-AI provisions are the author-asserted (network)
part above.

**Reading (matches the already-adopted project interpretation).** A proved-correct decision procedure
that, for each admissible `C`, outputs `delta*_C` with a machine-checkable certificate **satisfies**
"determine `delta*_C` for each admissible `C`" PROVIDED (a) the procedure's correctness is itself proved,
(b) it clears peer-review, (c) it is human-verified. This is **exactly "Reading B," already adopted as
the project working interpretation on 2026-07-03** (DAG node `certifier_uniformity`, quoted): "WORKING
INTERPRETATION ADOPTED (project decision 2026-07-03): Reading B — the determination artifact is a
proved-correct procedure yielding the certified delta*_C for any admissible C... TOTALITY = free with an
EXACT (complete) solver... the classical uniform distance theorem demotes to insurance-tier." So this
row **cites and grounds** that decision; it does not reopen it.

**Stricter reading (per the node's own instruction "plan against the stricter reading").** Judges may
demand the `delta*_C` **values** on the actual deployed rows (compiler *run*, certificates emitted),
and/or require the correctness meta-theorem peer-reviewed as the deliverable (uniformity relocated, not
eliminated). **Bare per-row certificates without the uniform correctness proof = PARTIAL/complementary
award material, not a full grand-challenge resolution.**

## (iii) Q0.1 / tower case: RESOLVED -> `f1_case_tower` is GENUINELY CRITICAL (not deletable)

R6 flagged `f1_case_tower` as "critical ONLY IF the official family admits non-generating rows (Q0.1)."
Q0.1 is now **settled the critical way**, and the earlier hope that a reading could *delete* this node
is **withdrawn**:
- `field_cap_check` [PROVED, 2026-07-03] statement: the caps determine "whether non-generating rows
  (hence the tower case) are admissible." Its resolution + the `f1_case_tower` node notes (quoted):
  "Family CONFIRMED to include non-generating rows (any field < 2^256 incl. extensions, n up to 2^41):
  the tower case is genuinely critical, no longer family-conditional." (The pinned official cap is
  `k <= 2^40`; the "n up to 2^41" in that node is the induced domain size `|L| = k/rho` at rate 1/2,
  not a separately pinned `n` cap.)
- **Why the deletion argument fails (recorded so it isn't retried):** `generating_escape` [PROVED]
  says non-generating rows are *forced tiny* (`q_gen < 2^128`) -- it **bounds their generated-field
  size, it does not remove them from the family** (see also `axis8_generating.md`). And
  `mixed_radix_frontier` [PROVED, vacuous] is the orthogonal *radix* axis (smooth = 2-power), not the
  *generating* axis. Chaining the two to conclude "no non-generating rows" is invalid; the family has
  non-generating rows via subfield/extension structure regardless of 2-power smoothness.
**Outcome:** Q0.1 resolved; `f1_case_tower` **confirmed critical**. The R6 reading did its job -- it
*decided* the conditional node -- but the decision is "critical," so no node is deleted.

## Net R6 outcome

- **Drift:** author re-fetch 2026-07-06 shows no new drift vs the repo-supported 2026-07-03 baseline;
  caps remain ePrint-only; recheck (and re-hash the PDF) pre-submission.
- **Compiler semantics:** freeze-table row supplied and grounded in ABF Sec.1; consistent with the
  adopted Reading B (`certifier_uniformity`); plan against the stricter "values + peer-reviewed
  meta-theorem" reading; treat bare per-row certificates as partial-award material.
- **`f1_case_tower`:** Q0.1 resolved -> **genuinely critical, not family-conditional, not deletable**
  (corrects an earlier overlap-audit hope that a reading could delete this node; root cause was
  conflating `generating_escape` = "non-generating rows forced *tiny*" with "absent").
- **Honest scope:** this packet mostly records/grounds decisions already present in the DAG. Its
  net-new contributions are the (author-asserted) 2026-07-06 drift recheck and the compiler-semantics
  freeze row grounded in the ABF text. No Paper A-D edit; no threshold proved.

## Reproducibility

Repo-only (reproducible now):
```sh
python3 - <<'PY'
import json
d=json.load(open('experimental/data/prize-dag/prize_dag.json'))
want={'rules_freeze','certifier_uniformity','f1_case_tower','field_cap_check',
      'generating_escape','mixed_radix_frontier','rules_m_reading'}
for n in d['nodes']:
    if (n.get('id') or n.get('name')) in want:
        print(n.get('id'), '|', n.get('status'), '|', (n.get('notes') or n.get('statement') or '')[:160])
PY
```
Requires network (NOT reproduced here): fetch https://proximityprize.org/ and diff against the strings
above; and `shasum -a 256 <the ABF ePrint 2026/680 PDF>` compared to the pinned SHA.
