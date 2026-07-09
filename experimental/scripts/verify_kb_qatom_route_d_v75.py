#!/usr/bin/env python3
"""KB-MCA Route-D v75: multipad span >= 2e; union not a long AP.

Large-t step after t<=2e injectivity (v74).

Proved:
  (1) Strict size. Any free-1 multipad requires t >= 2e+1.
      (v74: none for t <= 2e; packing needs t >= 2e for two disjoint e-sets.)
  (2) AP-union ban (rescaling). Let A,B be a multipad on the order-n GP, and
        W = A cup B  (so |W|=2e).
      Suppose W is an arithmetic progression of length 2e with difference d >= 1:
        W = { a0 + j d : j = 0,...,2e-1 }.
      Let rho = omega^d and alpha = omega^{a0}. Root values are
        { alpha * rho^j : j = 0,...,2e-1 }.
      Write monic polys f,g for the two parts. Then
        f(X) = alpha^e  f0(X/alpha),  g(X) = alpha^e g0(X/alpha)
      with f0,g0 monic on complementary e-subsets of {1,rho,...,rho^{2e-1}}.
      Now f-g constant iff f0-g0 constant. Thus (f0,g0) is a t=2e multipad for
      the pure GP of ratio rho. If ord(rho) = n/gcd(d,n) > 2e, v74 forbids this.
      In particular, for d=1 one has ord(omega)=n > 2e (deployed and toys with
      2e < n), so W is never a contiguous index interval of length 2e.
  (3) Span strengthening. For a multipad, |W|=2e and span = max(W)-min(W).
      If span = 2e-1 then W fills every integer from min to max, hence is a
      contiguous interval (AP with d=1), forbidden by (2) when n > 2e.
      Therefore
        span(G) = max(supp G) - min(supp G)  >=  2e.
      (Improves v74's span >= e.)
  (4) Hole corollary. With |W|=2e and span >= 2e, the interval [min,max] has
      length span+1 >= 2e+1 > |W|, so W has at least one hole.

CAS:
  (5) All multipad pairs: span >= 2e; W never AP of length 2e; never contiguous.
  (6) First multipad t_* >= 2e+1 always; t_*/e often in ~2.6..5.5 on toys.
  (7) Deployed n' >> 2e still open for full ban.

OPEN:
  Ban multipads for t up to n' (or SoftB). Span>=2e is necessary but far from
  n'-scale obstruction alone.

Does NOT claim |T|<=H2 / A_SP.

  python3 experimental/scripts/verify_kb_qatom_route_d_v75.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v75"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v75.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v75.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v75.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A_DEP = 1_116_048
J = N - A_DEP
T_ROW = A_DEP - 2**20
Wdeg = T_ROW - 1
E = Wdeg + 1
M_C = J - E
FREE_CORE = M_C - Wdeg
N_PRIME = A_DEP + E
H2 = E * P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E
B_STAR = math.sqrt(2 * H2)
TWO_E = 2 * E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_t_ge_2e1() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_requires_t_ge_2e_plus_1",
        "statement": "Any free-1 multipad needs t >= 2e+1.",
        "proof": [
            "Two disjoint e-sets need t >= 2e.",
            "v74: no multipad for t <= 2e. Hence t >= 2e+1.",
        ],
    }


def lemma_ap_ban() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_union_not_AP_of_length_2e",
        "statement": (
            "If n > 2e, multipad index union W is not an arithmetic progression "
            "of length 2e with difference d satisfying ord(omega^d) > 2e. "
            "In particular W is not a contiguous block of length 2e."
        ),
        "proof": [
            "W={a0+jd}_{j=0}^{2e-1} => values alpha * {rho^j} with rho=omega^d.",
            "Monic free-1 multipad scales: f-g constant iff the pure-rho multipad "
            "f0-g0 constant on {0..2e-1}.",
            "v74 forbids pure GP multipads of length 2e when ord(rho)>2e.",
            "d=1 => ord(omega)=n>2e => no contiguous W.",
        ],
    }


def lemma_span_2e() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_span_ge_2e",
        "statement": (
            "For multipad G with n>2e: span(G)=max(supp)-min(supp) >= 2e."
        ),
        "proof": [
            "|W|=2e. If span=2e-1 then W is a contiguous interval of length 2e.",
            "Forbidden by AP-ban with d=1. Hence span >= 2e.",
        ],
    }


def lemma_hole() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_union_has_a_hole",
        "statement": (
            "W=A cup B has a hole in [min W, max W]: "
            "max-min+1 >= 2e+1 > |W|=2e."
        ),
        "proof": ["span >= 2e => max-min+1 >= 2e+1 > 2e."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_large_t_multipad_ban",
        "statement": (
            f"Ban multipads for t up to n'={N_PRIME} (~17.5 e), or SoftB."
        ),
    }


def prim_root(p: int) -> int:
    fac: list[int] = []
    m = p - 1
    d = 2
    while d * d <= m:
        if m % d == 0:
            fac.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no prim root")


def monic_X(roots: list[int], p: int) -> list[int]:
    poly = [1]
    for r in roots:
        new = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            new[j] = (new[j] - (r * c) % p) % p
            new[j + 1] = (new[j + 1] + c) % p
        poly = new
    return poly


def free1_X(poly: list[int], e: int) -> tuple[int, ...]:
    return tuple(poly[1:e])


def is_AP(S: set[int] | list[int]) -> bool:
    S = sorted(S)
    if len(S) <= 2:
        return True
    d = S[1] - S[0]
    if d <= 0:
        return False
    return all(S[i + 1] - S[i] == d for i in range(len(S) - 1))


def is_contiguous(S: set[int]) -> bool:
    if not S:
        return True
    return max(S) - min(S) + 1 == len(S)


def census(p: int, n: int, t: int, e: int) -> dict[str, Any]:
    ensure(2 * e < n, "2e < n for AP ban")
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    buckets: dict[tuple[int, ...], list[set[int]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        buckets[free1_X(monic_X(roots, p), e)].append(set(idxs))

    pairs = 0
    spans: list[int] = []
    n_AP = 0
    n_cont = 0
    for lst in buckets.values():
        if len(lst) < 2:
            continue
        for A, B in itertools.combinations(lst, 2):
            ensure(A.isdisjoint(B), "disjoint")
            W = A | B
            ensure(len(W) == 2 * e, "cup 2e")
            pairs += 1
            sp = max(W) - min(W)
            spans.append(sp)
            if is_AP(W) and len(W) == 2 * e:
                # check ord condition: d = common difference
                Ws = sorted(W)
                d = Ws[1] - Ws[0]
                # ord(omega^d) = n / gcd(d,n)
                ord_rho = n // math.gcd(d, n)
                if ord_rho > 2 * e:
                    n_AP += 1  # forbidden type — must be 0
            if is_contiguous(W):
                n_cont += 1

    return {
        "p": p,
        "t": t,
        "e": e,
        "pairs": int(pairs),
        "injective": bool(pairs == 0),
        "min_span": int(min(spans)) if spans else None,
        "max_span": int(max(spans)) if spans else None,
        "all_span_ge_2e": bool(all(s >= 2 * e for s in spans)) if spans else True,
        "forbidden_AP_count": int(n_AP),
        "contiguous_count": int(n_cont),
        "t_ge_2e1_if_mp": bool(pairs == 0 or t >= 2 * e + 1),
    }


def first_multipad_t(p: int, n: int, e: int, tmax: int | None = None) -> int | None:
    if tmax is None:
        tmax = min(n, max(8 * e, 40))
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    for t in range(e, tmax + 1):
        if math.comb(t, e) > 18000:
            break
        vals = [pow(om, i, p) for i in range(t)]
        buckets: dict[tuple[int, ...], int] = defaultdict(int)
        for idxs in itertools.combinations(range(t), e):
            buckets[free1_X(monic_X([vals[i] for i in idxs], p), e)] += 1
        if any(m >= 2 for m in buckets.values()):
            return t
    return None


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "odd")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(TWO_E + 1 <= N_PRIME, "deployed room")
    ensure(TWO_E < N, "2e < n")
    ensure(FLOOR_NP == 17, "k")

    # t <= 2e still free (v74); t=2e+1 may or may not
    free_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for e in [3, 4, 5]:
            if 2 * e >= n:
                continue
            for t in [2 * e, 2 * e + 1]:
                if t > n or math.comb(t, e) > 25000:
                    continue
                r = census(p, n, t, e)
                if t <= 2 * e:
                    ensure(r["injective"], f"free t={t}")
                free_rows.append(r)

    mp_rows = []
    for p, n, t, e in [
        (61, 60, 13, 3),
        (61, 60, 17, 3),
        (61, 60, 24, 3),
        (101, 100, 9, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 16, 3),
        (127, 126, 21, 4),
        (43, 42, 12, 3),
        (73, 72, 14, 4),
    ]:
        if 2 * e >= n or t > n or math.comb(t, e) > 40000:
            continue
        r = census(p, n, t, e)
        ensure(r["forbidden_AP_count"] == 0, "no forbidden AP")
        ensure(r["contiguous_count"] == 0, "no contiguous")
        if r["pairs"] > 0:
            ensure(r["all_span_ge_2e"], f"span {p},{t},{e}")
            ensure(r["min_span"] is not None and r["min_span"] >= 2 * e, "span val")
            ensure(r["t_ge_2e1_if_mp"], "t>=2e+1")
        mp_rows.append(r)

    ensure(any(r["pairs"] > 0 for r in mp_rows), "some multipads")

    first_rows = []
    for p, n in [(61, 60), (73, 72), (101, 100), (127, 126), (43, 42)]:
        for e in [3, 4, 5]:
            if 2 * e >= n:
                continue
            t0 = first_multipad_t(p, n, e)
            if t0 is not None:
                ensure(t0 >= 2 * e + 1, f"first {p},{e}")
            first_rows.append(
                {
                    "p": p,
                    "e": e,
                    "first_t": t0,
                    "two_e": 2 * e,
                    "ratio": None if t0 is None else float(t0 / e),
                }
            )

    return {
        "status": "PASS",
        "free_rows": free_rows,
        "mp_rows": mp_rows,
        "first_rows": first_rows,
        "summary": {
            "n_mp": len(mp_rows),
            "n_first": len(first_rows),
            "all_span_ge_2e": True,
            "all_no_contiguous_W": True,
            "all_no_forbidden_AP": True,
            "all_first_t_ge_2e1": True,
            "deployed_2e": TWO_E,
            "deployed_n_prime": N_PRIME,
            "deployed_ratio": float(N_PRIME / E),
            "B_star": float(B_STAR),
            "H2": H2,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "two_e": TWO_E,
            "min_span_if_multipad": TWO_E,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "note": (
                "multipad => span>=2e and non-AP union; "
                "still far from n'-scale ban"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v75",
        "title": "Multipad span >= 2e; union not a 2e-AP",
        "status": "SPAN_2E_PROVED_LARGE_T_BAN_OPEN",
        "claims": {
            "proves_multipad_t_ge_2e_plus_1": True,
            "proves_union_not_AP_length_2e": True,
            "proves_span_ge_2e": True,
            "proves_union_has_hole": True,
            "proves_deployed_injectivity": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "t_ge_2e1": lemma_t_ge_2e1(),
            "ap_ban": lemma_ap_ban(),
            "span_2e": lemma_span_2e(),
            "hole": lemma_hole(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"python_nt": "multipad geometry census"},
        "impact_on_program": {
            "closed": (
                "BOARD: multipad => t>=2e+1, span>=2e, W not contiguous/long AP"
            ),
            "wall": "large-t ban to n' or SoftB",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    mp_lines = []
    for r in cert["toy_suite"]["mp_rows"]:
        mp_lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | {r['pairs']} | "
            f"{r['min_span']} | {r['max_span']} | "
            f"{r['contiguous_count']} | {r['forbidden_AP_count']} |"
        )
    mp_tbl = "\n".join(mp_lines)
    first_lines = []
    for r in cert["toy_suite"]["first_rows"]:
        ratio_s = "-" if r["ratio"] is None else f"{r['ratio']:.2f}"
        first_lines.append(
            f"| {r['p']} | {r['e']} | {r['first_t']} | {r['two_e']} | {ratio_s} |"
        )
    first_tbl = "\n".join(first_lines)
    return f"""# KB-MCA Route-D v75: multipad span `≥ 2e`

Status: **span ≥ 2e + AP-union ban PROVED**; large-t / deployed ban still **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED

```text
multipad  =>  t >= 2e+1
          =>  span(G) >= 2e
          =>  W = A cup B is not a contiguous 2e-block
          =>  W is not an AP of length 2e with ord(omega^d) > 2e
          =>  W has a hole in [min,max]
```

### Why span ≥ 2e

|W|=2e. Span = 2e−1 ⇒ W contiguous (AP, d=1) ⇒ rescale to pure GP of length 2e  
⇒ forbidden by v74 when n > 2e. Hence span ≥ 2e.

## Deployed

| | |
|---|---:|
| 2e | {d['two_e']} |
| min span if multipad | ≥ {d['min_span_if_multipad']} |
| n' | {d['n_prime']} |
| n'/e | {s['deployed_ratio']:.2f} |

Necessary conditions only — **not** a residual close.

## CAS

### Multipad geometry

| p | e | t | #pairs | min span | max span | #contig | #bad AP |
|---|---:|---:|---:|---:|---:|---:|---:|
{mp_tbl}

### First multipad t

| p | e | first t | 2e | t/e |
|---|---:|---:|---:|---:|
{first_tbl}

## OPEN

Large-t multipad ban up to n', or SoftB — next residual-board hit.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v75.py --check
```
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    cert = build()
    if args.check and CERT_PATH.exists():
        old = json.loads(CERT_PATH.read_text())
        ensure(old["claims"] == cert["claims"], "claims drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    NOTE_PATH.write_text(render_note(cert))
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v75\n\n"
        "Multipad span >= 2e; union not a 2e-AP / contiguous block.\n"
    )
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    REPORT_PATH.write_text(
        f"# v75 report\n\nstatus: {cert['status']}\n"
        f"span >= 2e: PROVED\n"
        f"OPEN large-t ban: True\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  multipad => t >= 2e+1: PROVED")
    print("  multipad => span >= 2e (no contiguous W): PROVED")
    print("  multipad union not long AP (ord rho > 2e): PROVED")
    print(
        f"  deployed: min span if mp >= {d['min_span_if_multipad']}; "
        f"n'={d['n_prime']} (ratio {s['deployed_ratio']:.2f})"
    )
    print(f"  CAS: mp_rows={s['n_mp']}; first_rows={s['n_first']}")
    print("  BOARD: span/AP structure closed; residual still OPEN")


if __name__ == "__main__":
    main()
