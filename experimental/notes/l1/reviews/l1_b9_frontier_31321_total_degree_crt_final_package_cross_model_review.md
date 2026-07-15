# Cross-model final-package review: L1 B9 `31321` total-degree-six reduced-CRT packet

**Reviewer:** fresh-context Claude Fable 5 read-only local CLI audit, 2026-07-15. No prior session, review conclusion, or cached state was resumed or trusted; all findings below were recomputed in this session. The audit ran in the isolated snapshot `/private/tmp/rs-mca-31321-claude-final.UvMFRP/repo`; the original repository was touched only for read-only git/PR metadata. No repository file was created, edited, staged, committed, or pushed; `--write-certificate` was never invoked; all harnesses and Sage/Python writes stayed under `/tmp` (`DOT_SAGE`/`TMPDIR` redirected; `PYTHONDONTWRITEBYTECODE=1` and `python3 -B` throughout). The live final-package independent review present in the original worktree was neither read nor relied on.

## 1. Hash-pinned frozen artifacts

All seven SHA-256 hashes were independently recomputed and match the declared values exactly; they are byte-identical in the original worktree, and were re-verified unchanged after all replays.

| # | artifact | SHA-256 |
|---|---|---|
| 1 | `experimental/scripts/verify_l1_b9_frontier_31321_owner_partition.py` | `1a1044b60f2df17ee5c50469f086f7254230a39a25de4e8c57ce80ab507e8421` |
| 2 | `experimental/data/certificates/l1-b9-frontier-31321-owner-partition/certificate.json` | `f0b35bc43cb69ae3fcd0bcc095fc5f5185af9294c94af5375efd7324ae921f32` |
| 3 | `experimental/scripts/verify_l1_b9_frontier_31321_total_degree_crt.sage` | `60391b3642f1d15f86ed120646e4c73a78a50b55b1e4338747e0f35c16f58de4` |
| 4 | `experimental/data/certificates/l1-b9-frontier-31321-total-degree-crt/certificate.json` | `f57b458a3b6ba1c7daa5098bcea8f796ba39294ddc046398c9310708d884917b` |
| 5 | `experimental/scripts/verify_l1_b9_frontier_31321_total_degree_crt_ledger.py` | `b94e1cd5e0c547224cb205eb8c944257cba9cc6b0ddcfbbb4e35eb868ae12954` |
| 6 | `experimental/data/certificates/l1-b9-frontier-31321-total-degree-crt/ledger_certificate.json` | `73d18b2694e5c0bb0d6cb4eedf2fcd37881cb801eba6ca840ba0fef56054f9b6` |
| 7 | `experimental/notes/l1/l1_b9_frontier_31321_total_degree_crt_lemma.md` | `a175ebf807a93df85f915e50ff73de9d7d5eaf781b15ae667c2073392b9dfc77` |

`agents.md` was read in full before judging.

## 2. Independent mathematical audit

Each load-bearing step was rederived, not merely replayed.

- **Fixed 12×9 rank nine.** For `deg R = 1`, monic pairwise-coprime `B_i` of degrees a permutation of `(3,2,1)` each coprime to `R`, the fixed-`F` unknowns are 3 coefficients of `V` plus `1+2+3` quotient coefficients, quotient bounds `3−deg(B_i)` with multiset `(0,1,2)`. A homogeneous solution has `B_i | RV` for all `i`; pairwise coprimality and `gcd(R,B)=1` give `B | V`, and `deg V ≤ 2 < 6 = deg B` forces `V = 0`, then `A_i = 0`. The map is injective, hence rank nine. Confirmed by hand and numerically on all 1,152 keys by an independent harness (below).
- **Moving 12×12 vs reduced 3×3.** Solvability of the fixed system at monic cubic `F` is exactly `V ≡ c_iR^{-1}F (mod B_i)` for all `i`, i.e. `V = FG mod B` with `G` the CRT unit; a degree-≤2 `V` exists iff the `X^3,X^4,X^5` coefficients of `FG mod B` vanish, which is affine in `(f_0,f_1,f_2)`. The quotient bounds are automatic since `deg(RV − c_iF) ≤ 3`. The rank relations `rank(C) = 9 + rank(M)` and `rank([C|b]) = 9 + rank([M|−u])` were confirmed on every one of the 1,152 keys by independent code, and the affine identity, the certificate's symbolic `M`, `u`, and `det(M)` strings, and the internal `det_M_sha256` were all reproduced independently in SymPy.
- **Compatible-rank-drop degree-gap/gcd proof.** Two independent kernel pairs give `B | F_0V_1 − F_1V_0` with `deg ≤ 3+2 = 5 < 6`, so the cross-polynomial vanishes identically (generic degree 5 confirmed symbolically); `G` a unit modulo `B` excludes `V_i = 0` for `F_i ≠ 0`; unique factorization/Euclid then forces `gcd(F,V)` nonconstant for every compatible monic cubic. Verified by hand; sound.
- **Bridge.** Under split-squarefree `F = L_D`, zero core/background received data, disjoint blocks, `H = X−h`, `W = RHV`: a root `α` of `gcd(F,V)` lies in `D`, `R(α) ≠ 0`, `H(α) ≠ 0`, so `W(α) = 0` restores a core agreement; missed core is exactly `D\Z(V)`, size ≤ 2, so compatible rank drop cannot realize exact `d = 3`. Sound.
- **Aggregate key / no factor four.** A monic split cubic `F = L_D` determines `D` and hence the restored point `h`, so the full-rank bound of one monic cubic per canonical cofactor key bounds all four restored-core refinements jointly; no factor 4. Not subtracting the twelve periodic refinement payments is the conservative direction for an upper bound. I also rederived the periodic count by hand: the only feasible fibre scale for an 8-point full support in `Z/18` is 2 (shift by 9), and exact case analysis yields precisely 12 periodic full supports in 12 distinct aggregate keys (9 with background index 16, 3 with 17), while every 7-point selected cofactor support is aperiodic since 2∤7 — matching the owner certificate exactly.
- **Exact GF(19) census and vacuity boundary.** A fully independent pure-Python census (zero shared code, own polynomial/rank arithmetic) reproduced: 1,152 unique keys (`2·6·4·6·4`), occupancy histogram 192×6, fixed rank `{9:1152}`, moving `{(11,12):44, (12,12):1108}`, reduced `{(2,3):44, (3,3):1108}`, monic solutions `{0:44, 1:1108}`, **zero** compatible rank drops, and exactly one actual split-core incidence, on a full-rank key, with zero rank-drop incidences and zero bridge failures. The packet correctly declares the compatible-rank-drop finite branch `VACUOUS_ALL_44_RANK_DROPS_ARE_AFFINE_INCONSISTENT` and rests that branch on the universal algebraic proof, retaining the reviewed `31222` row (2 compatible patterns, 38 monic cubics, 0 zero-gcd) strictly as a nonvacuous total-degree-six control with "no theorem is imported".

## 3. Replays

From the snapshot root, all six declared reproduction commands were replayed (with `-B`/`PYTHONDONTWRITEBYTECODE=1`; Sage writes confined to `/tmp`):

```text
owner  normal:  PASS (frozen certificate matched; verdict YELLOW, ledger unchanged 104,914 -> 104,914)
owner  tamper:  PASS, 16/16 mutations CAUGHT
sage   normal:  PASS (full fresh census rebuild == frozen bytes; transcript 2256ea69…d80972; banked: False; verdict YELLOW_LOCAL_PACKET_PENDING_FRESH_INDEPENDENT_REVIEW)
sage   tamper:  PASS, 37/37 mutations CAUGHT (incl. hypotheses, symbolic M, bridge data, all 8 linked-input hashes, bank flag, gate flag)
ledger normal:  PASS
ledger tamper:  PASS, 18/18 mutations CAUGHT (incl. forged self-consistent banked CRT certificate)
```

## 4. Certificates, linkage, and ledger arithmetic

All three JSONs strict-parse with no duplicate keys and single trailing newlines. Every linked-path SHA-256 in both current certificates matches the on-disk bytes (8 links in the CRT certificate, 3 in the ledger certificate); the owner certificate's `previous_ledger` hash matches the d4r0 ledger on disk, which is byte-identical to the blob committed at HEAD. Transcript and pattern-owner hashes recompute exactly. The canonical-key order/set hashes (`314b4052…ada4be`, `2f76b435…33c565`) were reproduced by independent enumeration, and the owner-derived key set hash equals the CRT census set hash and the ledger's `canonical_key_set_sha256` — one shared content-addressed key universe.

Independently recomputed ledger facts: 75 rows whose canonical hash equals the banked prior `profile_sha256`; exactly one target row `(4,3,1,3,(3,2,1))` with charge `1,152·19 = 21,888`; replacement charge `1,152` (exponent 0); totals `641,512 → 620,776` and `104,914 → 84,178` (`−20,736`); next largest unresolved row `(ℓ,d,r,t,a_i) = (4,4,2,2,(3,3))`, `(G2,GR) = (2,3)`, 48 patterns, charge `48·19² = 17,328`; positive unresolved mass remains. The lemma note states all of these correctly.

## 5. Frozen state, stale-state repairs, and staging honesty

- The two final review paths are absent by design and everything **fails closed**: gate `PENDING_REQUIRED_REVIEW_FILES`, CRT `banked: false` / `YELLOW_LOCAL_PACKET_PENDING_FRESH_INDEPENDENT_REVIEW`, ledger `YELLOW_CANDIDATE…`, promotion gate `NO_PENDING_REVIEW`, all pattern owners `CANDIDATE_PENDING_FRESH_REVIEWS`. Every validation recomputes the gate from disk; forged bank flags and forged gate Booleans are caught.
- Sage and ledger docstrings are bank-state-neutral (bank state "recomputed from the two declared review artifacts"; "remains unbanked until both declared reviews authorize"). The prior `31222` control carries role "control only; no theorem is imported" with no stale review requirement. The owner `still_required` is packet-relative. The zero core/background bridge hypotheses appear consistently in the lemma, both certificates, and the stop conditions. The retained history files (YELLOW, no-verdict attempt 1, and the two first-round GREEN reviews on the superseded pre-repair hashes) end with single newlines; the gate paths now name the second, final-package pair.
- **Staging honesty.** The lemma's status line, banked-ledger section, the agents-log entry, and the mixed-petal ledger additions are written in terminal packaged voice ("banked", "both final reviews GREEN"), while the machine state is unbanked. I judge this honest terminal content-addressed packaging: the review-history paragraph discloses the full sequence (first YELLOW, capped attempt, first GREEN pair, reopened gate over stale wording/EOF defects, second final-package pair), the fail-closed validators make the terminal words machine-true only when both declared files exist with exact standalone GREEN/YES sentinels, and the quoted banked-state tamper counts (39 and 20) are exactly the pending counts (37, 18) plus the two review-hash mutations that activate once the files exist. The dishonest failure mode — claiming banked without the gate — is structurally excluded and was tamper-tested.

## 6. Repository and PR parity

Original repo HEAD is `2671d4a261ceb8f90102ba50f6162e61356b291d` ("L1: bank the d=4,r=0 auxiliary layer"), which is exactly PR #801's `headRefOid` (open, base `main`). The branch `agent/l1-b9-frontier-31321-reduced-crt` sits at that commit with a narrow, purely additive uncommitted delta: two prose files modified (agents-log entry; mixed-petal ledger scope/section, status, totals-chain, next-gate, and reproduction updates — all consistent with the certificates, well-formed Markdown with balanced fences) plus the new scripts, certificates, lemma, and review-history files. No generated caches are in the payload: certificate directories contain only the three JSONs, and `*.sage.py`/`__pycache__` are gitignored ("Sage preparser artifacts"). The reproduction commands are correct as printed (the owner script self-inserts its script dir; the ledger command's `PYTHONPATH` is required and sufficient; `/usr/local/bin/sage` exists, SageMath 10.9).

## 7. Scope and nonclaims

This authorization covers only the frozen local row `(q,n,k,σ,ℓ,M,b) = (19,18,5,3,4,3,2)`, `(ℓ,d,r,t,a_i) = (4,3,1,3,(3,2,1))`, and only the `21,888 → 1,152` replacement with its `620,776`/`84,178` totals. No `m>2`, PR `#763`, Lean, cross-`r`, or global mixed-petal conclusion is claimed or authorized; the zero auxiliary-Johnson margin is not a bound; the twelve periodic refinements are not subtracted; the compatible-rank-drop implication is vacuous in this row and rests on the universal proof; `UNPAID_PRIMITIVE` remains relative to the named owner stack. This memo is one of two required gates: the separate independent final-package review is a distinct gate that I have not read, assumed, or relied on. After both final reviews exist at the declared paths, the maintainer must regenerate both certificates and re-run normal and tamper modes (expect 39/39 and 20/20 caught) before treating the bank as effective.

No substantive or packaging defect remains in the seven frozen artifacts or the accompanying delta.

Verdict: GREEN

Ledger authorization: YES
