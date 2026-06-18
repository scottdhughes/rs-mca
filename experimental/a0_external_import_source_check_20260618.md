# A0 External Import Source Check, 2026-06-18

- **Status:** AUDIT.
- **Agent/model:** Codex.
- **Scope:** External-source check for the imports used by Paper D's universal
  cap and fallback route.  This note does not certify the CS25 or ABF imports
  as closed.

## Summary

The A0 import audit is still not complete.  The load-bearing Crites--Stewart
and ABF sources could not be retrieved from `eprint.iacr.org` in this local
environment because direct PDF requests returned HTTP 403 Cloudflare challenge
pages.

The BCHKS fallback source is partially checked: the ECCC copy of
Ben-Sasson--Carmon--Haboeck--Kopparty--Saraf, `TR25-169`, was reachable and
converted to text.  Its Theorem 1.9 was located and compared at the level needed
to confirm the broad fallback shape recorded in the local audit notes.  This
does not verify ABF Theorem 5.2, and therefore does not close the Paper D
fallback import.

## Source Access Record

| Source | Local access result | Audit consequence |
|---|---|---|
| CS25, ePrint 2025/2046 PDF | HTTP 403 Cloudflare challenge from direct `curl -L -I https://eprint.iacr.org/2025/2046.pdf`. | CS25 Theorem 2 remains unchecked against the primary source. |
| ABF26, ePrint 2026/680 PDF | HTTP 403 Cloudflare challenge from direct `curl -L -I https://eprint.iacr.org/2026/680.pdf`. | ABF Theorems 5.2 and 5.3 remain unchecked against the survey/restatement. |
| BCHKS25, ePrint 2025/2055 PDF | HTTP 403 Cloudflare challenge from direct `curl -L -I https://eprint.iacr.org/2025/2055.pdf`. | ePrint copy was not accessible directly. |
| BCHKS25, ECCC TR25-169 PDF | HTTP 200 from `https://eccc.weizmann.ac.il/report/2025/169/download/`; `pdftotext` succeeded with annotation warnings only. | BCHKS Theorem 1.9 can be checked against this reachable primary report. |

## BCHKS Theorem 1.9 Check

The ECCC report defines `LDR_{F_q,D,L}(delta)` as the largest radius `gamma`
such that every received word has at most `L` codewords in the radius-`gamma`
ball for `RS[F_q,D,(1-delta)|D|]`.

Theorem 1.9 in the reachable report states the following shape:

```text
C = RS[F_q,D,k], |D|=n, k=(1-delta)n,
gamma = LDR_{F_q,D,q}(delta) + 2/n.
Then there exist f,g:D->F_q with at least q/(2n) values z for which
dist(f+z g,C) <= gamma, while dist([f,g],C^2) >= delta - 1/n.
```

This matches the qualitative fallback risk recorded in the existing audit: past
the list-decoding radius, one can force non-negligible correlated-agreement
mass of order `1/(2n)` in the RS setting.

It does **not** by itself verify the local Paper D statement
`tex/cs25_cap_v4.tex` `thm:B`, because that local statement cites BCHKS
Theorem 1.9 **as restated in ABF26 Theorem 5.2**.  The translation from BCHKS
notation to the exact local parameters

```text
eca(C, delta + 2/n, 1-rho-1/n) < 1/(2n)
    => Lst(C, delta) < |F|
```

still needs the ABF26 restatement or an independent derivation.

## Current A0 Status

| Check | Status | Reason |
|---|---|---|
| E1: CS25 delta range | OPEN | CS25 PDF unavailable. |
| E2: CS25 augmented code `C+` | OPEN | CS25 PDF unavailable. |
| E3: list monotonicity convention | OPEN | Depends on exact CS25/ABF formulation. |
| E4: `eca` normalization | OPEN | CS25/ABF unavailable; local normalization alone is insufficient. |
| E5: extension-field sampling | OPEN | ABF unavailable. |
| E6: constants and ceiling in CS25 import | OPEN | CS25/ABF unavailable. |
| E7: ABF Theorem 5.3 equals local `thm:A` | OPEN | ABF PDF unavailable. |
| E8: ABF Theorem 5.2 equals local `thm:B` | PARTIAL / OPEN | BCHKS Theorem 1.9 source shape checked; ABF restatement still unavailable. |

## Recommendation

Do not promote Paper D's CS25-based cap from `CONDITIONAL` until a human or
browser-backed agent supplies the CS25 and ABF PDFs and verifies E1--E7
directly.

Do not promote the BCHKS fallback from `CONDITIONAL` until ABF Theorem 5.2 is
checked or the local `thm:B` translation is independently derived from BCHKS
Theorem 1.9 with all radius shifts and normalizations explicit.
