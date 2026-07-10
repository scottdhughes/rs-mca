#!/usr/bin/env python3
"""Hughes Route-D terminal wall at small side sizes: exact pins and witnesses.

Scott Hughes's Route-D chain (v51 U2e -> v53 C_unique -> v54 terminal star)
reduces the KB-row pure-untyped residual card to one open bound,

    |T| <= H2 = 77291948627,
    T = { e-sets U of I_{n'} : n'-1 in U, U has a free-1 partner in I_{n'} },

at deployed (p, n, n', e) = (2130706433, 2^21, 1183520, 67472).  This packet
pins that statement exactly (constants, inequality direction, partner
structure, generator convention), and maps the side-size-parametric family
T(n', e_s) with the same fixed budget H2:

  PROVED   e_s = 2 close re-derivation: |T(t,2)| <= p <= H2 (p <= H2 iff the
           deployed e = 67472 >= 1860; v48 credit).
  PROVED   terminal uniqueness for every side size: each high signature has at
           most one terminal e-set, so partners of terminal sets are
           automatically non-terminal and distinct equal-high sets are
           automatically disjoint.
  PROVED   deployed-row witnesses at canonical omega: T(n',3) >= 8 and
           T(n',4) >= 12, by explicit exactly-verified free-1 pairs (the first
           deployed-row members of T at any side size).  Constructions use the
           antipodal mechanism omega^(n/2) = -1 with t - n/2 = 134944 > 0.
  PROVED   (as integer arithmetic) budget landscape: the trivial terminal
           bound C(n'-1,2) exceeds H2 by the exact factor 9.0612... at
           e_s = 3; the v48 coefficient bound p^2 exceeds H2 by 5.87e7; the
           birthday-model load C(n'-1,e-1)*C(n'-1,e)/p^(e-1) is below H2 at
           e_s = 3 (0.5515*H2), above it for all 4 <= e_s <= 59 (peak
           2^46*H2 at e_s = 26), below again from e_s = 60, and below
           2^-1344158 at the chain's own case e_s = 67472.
  MEASURED exhaustive toy ladder at KB-shape arcs t = 9n/16 including the
           exact deployed subgroup index q = 1016: T > 0 onset at sparse
           index appears exactly where the load model predicts.
  OPEN     |T(n',3)| <= H2 (heuristically true at 0.55*H2, no proof) and the
           deployed wall |T(n',67472)| <= H2 itself.

Zero-argument default: full deterministic recompute (toy ladder, witness
searches, arithmetic gates), exact comparison against the checked-in JSON
certificate, and a live tamper suite.  ``--generate`` rewrites the
certificate (maintainer only).

All heavy loops are chunked; the script imposes RLIMIT_AS = 2 GiB on itself.
Reference run: about 2 minutes, peak RSS < 500 MiB.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import resource
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = ROOT / "experimental" / "data" / "cap25_v13_hughes_wall_small_e.json"

ADDRESS_SPACE_CAP_BYTES = 2 * 1024**3

# ---- deployed KB row (source: verify_kb_qatom_route_d_v54.py, STATUS note) ----
P_KB = 2**31 - 2**24 + 1          # 2130706433
N_KB = 2**21                      # 2097152
A_KB = 1_116_048
E_KB = 67_472                     # deployed side size e = w+1
NP_KB = A_KB + E_KB               # n' = 1183520
H2_KB = E_KB * P_KB // (2 * 31 * 30)   # 77291948627 (v45 M_pad<=2 budget)
EP_KB = E_KB * P_KB               # 143763024447376
HALF = N_KB // 2                  # 2^20
CAP_ANTI = NP_KB - HALF           # 134944 antipodal-capable base indices
INDEX_KB = (P_KB - 1) // N_KB     # 1016 exactly

# witness search registration
E4_TARGET = 12
E4_PAIR_CAP = 400_000
E3_TARGET = 8
E3_TRIAL_CAP = 150_000_000
E4_FAMILY_SAMPLE = 2_000          # deterministic first-2000 antipodal centers

# toy ladder registration: (block id, p, n, t, e, steps)
GRADIENT_PRIMES = [(4, 257), (18, 1_153), (67, 4_289), (253, 16_193),
                   (513, 32_833), (1_017, 65_089)]
LADDER_BLOCKS = [
    ("kb_shape_n128_e3_allsteps", 129_793, 128, 72, 3, "all"),
    ("kb_shape_n256_e3", 259_841, 256, 144, 3, [1, 3]),
    ("kb_shape_n512_e3_q1016", 520_193, 512, 288, 3, [1, 3, 5]),
    ("kb_shape_n1024_e3_onset", 1_038_337, 1024, 576, 3, [1, 3]),
    ("kb_shape_n128_e4", 129_793, 128, 72, 4, [1, 3]),
    ("kb_shape_n256_e4", 259_841, 256, 144, 4, [1]),
]
BAND_E_MAX = 80


class CheckFailure(AssertionError):
    pass


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.passed = 0

    def check(self, condition: bool, label: str) -> None:
        self.total += 1
        if not condition:
            raise CheckFailure(label)
        self.passed += 1

    def equal(self, actual: Any, expected: Any, label: str) -> None:
        self.check(actual == expected, f"{label}: {actual!r} != {expected!r}")


def impose_address_space_cap() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = ADDRESS_SPACE_CAP_BYTES
    if hard != resource.RLIM_INFINITY:
        cap = min(cap, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    if soft > ADDRESS_SPACE_CAP_BYTES:
        raise CheckFailure("RLIMIT_AS exceeds 2 GiB")
    return int(soft)


def is_prime(n: int) -> bool:
    """Deterministic Miller--Rabin, valid for all 64-bit integers."""
    if n < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % sp == 0:
            return n == sp
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 325, 9_375, 28_178, 450_775, 9_780_504, 1_795_265_022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


@lru_cache(maxsize=None)
def primitive_root(p: int) -> int:
    if not is_prime(p):
        raise CheckFailure(f"nonprime modulus {p}")
    fac = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise CheckFailure(f"no primitive root mod {p}")


@lru_cache(maxsize=None)
def subgroup_base(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise CheckFailure(f"n={n} does not divide p-1")
    omega = pow(primitive_root(p), (p - 1) // n, p)
    for q in prime_factors(n):
        if pow(omega, n // q, p) == 1:
            raise CheckFailure("omega has too small an order")
    vals = [1] * n
    v = 1
    for i in range(1, n):
        v = v * omega % p
        vals[i] = v
    if len(set(vals)) != n:
        raise CheckFailure("subgroup values are not distinct")
    return tuple(vals)


def locator_coefficients(indices, values, p: int) -> list[int]:
    """Monic locator prod (X - values[i]); descending coefficient list."""
    co = [1]
    for i in indices:
        r = values[i]
        nxt = [0] * (len(co) + 1)
        for j, c in enumerate(co):
            nxt[j] = (nxt[j] + c) % p
            nxt[j + 1] = (nxt[j + 1] - r * c) % p
        co = nxt
    return co


# --------------------------- deployed arc (cached) ---------------------------

_ARC_CACHE: dict[str, Any] = {}


def deployed_arc() -> tuple[list[int], dict[int, int]]:
    if "arc" not in _ARC_CACHE:
        g = primitive_root(P_KB)
        if g != 3:
            raise CheckFailure("canonical KB generator drifted (expected g=3)")
        omega = pow(g, (P_KB - 1) // N_KB, P_KB)
        if pow(omega, HALF, P_KB) != P_KB - 1:
            raise CheckFailure("omega^(n/2) != -1")
        arc = [1] * NP_KB
        v = 1
        for i in range(1, NP_KB):
            v = v * omega % P_KB
            arc[i] = v
        _ARC_CACHE["arc"] = arc
        _ARC_CACHE["idx"] = {val: i for i, val in enumerate(arc)}
        _ARC_CACHE["omega"] = omega
    return _ARC_CACHE["arc"], _ARC_CACHE["idx"]


# ----------------------------- exact arithmetic ------------------------------

def sig6(x: float) -> str:
    return "%.6g" % x


def band_row(e: int) -> dict[str, Any]:
    """Exact birthday-load comparison at side size e (deployed n', p, H2)."""
    num = math.comb(NP_KB - 1, e - 1) * math.comb(NP_KB - 1, e)
    den = P_KB ** (e - 1)
    over = num > H2_KB * den
    nb, db = num.bit_length(), den.bit_length()
    if nb - db < 200:
        loadf = num / den if nb - db > -900 else math.exp(
            (nb - db) * math.log(2)
        ) * 0.0
        ratio = sig6(loadf / H2_KB) if loadf else "0"
        load_s = sig6(loadf)
    else:
        load_s = f"2^{nb - db}approx"
        ratio = "huge"
    return {
        "e": e,
        "load": load_s,
        "load_over_H2": ratio,
        "exceeds_H2": over,
        "num_bits": nb,
        "den_bits": db,
    }


def deployed_arithmetic() -> dict[str, Any]:
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    c4 = math.comb(NP_KB - 1, 4)
    band = [band_row(e) for e in range(2, BAND_E_MAX + 1)]
    over = [r["e"] for r in band if r["exceeds_H2"]]
    e_lo, e_hi_last = min(over), max(over)
    # peak by exact integer comparison around e=26
    peaks = {}
    for e in (24, 25, 26, 27, 28):
        peaks[e] = math.comb(NP_KB - 1, e - 1) * math.comb(NP_KB - 1, e) * (
            P_KB ** (28 - e)
        )
    peak_e = max(peaks, key=peaks.get)
    # chain-case margin, exact
    ca = math.comb(NP_KB - 1, E_KB - 1)
    cb = math.comb(NP_KB - 1, E_KB)
    den = pow(P_KB, E_KB - 1)
    nb = (ca * cb).bit_length()
    db = den.bit_length()
    margin = db - nb
    if not (ca * cb) << (margin - 1) < den:
        raise CheckFailure("chain-case margin shift gate")
    return {
        "H2": H2_KB,
        "H2_formula_check": H2_KB == E_KB * P_KB // 1860,
        "e_times_p": EP_KB,
        "p_le_H2": P_KB <= H2_KB,
        "e2_close_gate_1860": E_KB >= 1860,
        "C_np1_2": c2,
        "C_np1_3": c3,
        "C_np1_4": c4,
        "trivial_e3_deficit_num": c2,
        "trivial_e3_deficit_den": H2_KB,
        "trivial_e3_deficit": sig6(c2 / H2_KB),          # 9.0612
        "v48_e3_deficit": sig6(P_KB * P_KB / H2_KB),      # 5.87e7
        "e3_load_below_H2_exact": c2 * c3 < H2_KB * P_KB * P_KB,
        "e3_load_over_H2": sig6(c2 * c3 / (P_KB * P_KB) / H2_KB),
        "e4_load_above_H2_exact": c3 * c4 > H2_KB * P_KB**3,
        "e4_load_over_H2": sig6(c3 * c4 / P_KB**3 / H2_KB),
        "band_first_over": e_lo,
        "band_last_over": e_hi_last,
        "band_reentry": e_hi_last + 1,
        "band_peak_e": peak_e,
        "band": band,
        "chain_case_e": E_KB,
        "chain_num_bits": nb,
        "chain_den_bits": db,
        "chain_margin_bits": margin,
        "antipodal_capacity": CAP_ANTI,
        "antipodal_capacity_check": CAP_ANTI == NP_KB - HALF,
        "coset_d_ge_4_dies": N_KB - NP_KB > N_KB // 4,
        "coset_d_2_survives": HALF > N_KB - NP_KB,
        "subgroup_index": INDEX_KB,
    }


# ------------------------------- toy ladder ----------------------------------

def stepped_values(p: int, n: int, step: int) -> list[int]:
    base = subgroup_base(p, n)
    return [base[(step * i) % n] for i in range(n)]


def scan_e3(p: int, n: int, t: int, step: int) -> dict[str, int]:
    vals = stepped_values(p, n, step)
    x = vals[t - 1]
    term: dict[tuple[int, int], tuple[int, int]] = {}
    for i in range(t - 1):
        a = vals[i]
        sax = a + x
        pax = a * x % p
        for j in range(i + 1, t - 1):
            b = vals[j]
            key = ((-(sax + b)) % p, (pax + b * sax) % p)
            if key in term:
                raise CheckFailure("two terminal 3-sets share a high")
            term[key] = (i, j)
    tset = set()
    pairs = 0
    get = term.get
    for i in range(t - 1):
        a = vals[i]
        for j in range(i + 1, t - 1):
            b = vals[j]
            sab = a + b
            pab = a * b % p
            for k in range(j + 1, t - 1):
                c = vals[k]
                u = get(((-(sab + c)) % p, (pab + sab * c) % p))
                if u is not None:
                    if {u[0], u[1], t - 1} & {i, j, k}:
                        raise CheckFailure("equal-high sets not disjoint")
                    pairs += 1
                    tset.add(u)
    return {"T": len(tset), "partner_pairs": pairs}


def scan_e4(p: int, n: int, t: int, step: int) -> dict[str, int]:
    vals = stepped_values(p, n, step)
    x = vals[t - 1]
    term: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    for i in range(t - 1):
        a = vals[i]
        for j in range(i + 1, t - 1):
            b = vals[j]
            s2 = a + b + x
            p2 = (a * b + (a + b) * x) % p
            p3 = a * b % p * x % p
            for k in range(j + 1, t - 1):
                c = vals[k]
                key = ((-(s2 + c)) % p, (p2 + c * s2) % p, (-(p3 + c * p2)) % p)
                if key in term:
                    raise CheckFailure("two terminal 4-sets share a high")
                term[key] = (i, j, k)
    tset = set()
    pairs = 0
    get = term.get
    for i in range(t - 1):
        a = vals[i]
        for j in range(i + 1, t - 1):
            b = vals[j]
            sab = a + b
            pab = a * b % p
            for k in range(j + 1, t - 1):
                c = vals[k]
                s3 = sab + c
                q2 = (pab + sab * c) % p
                q3 = pab * c % p
                for m in range(k + 1, t - 1):
                    d = vals[m]
                    u = get(
                        ((-(s3 + d)) % p, (q2 + d * s3) % p, (-(q3 + d * q2)) % p)
                    )
                    if u is not None:
                        if {u[0], u[1], u[2], t - 1} & {i, j, k, m}:
                            raise CheckFailure("equal-high sets not disjoint")
                        pairs += 1
                        tset.add(u)
    return {"T": len(tset), "partner_pairs": pairs}


def primitive_steps(n: int) -> list[int]:
    return [r for r in range(1, n) if math.gcd(r, n) == 1]


def model_ET(t: int, e: int, p: int) -> str:
    lam = math.comb(t - 1, e) / p ** (e - 1)
    return sig6(math.comb(t - 1, e - 1) * -math.expm1(-lam))


def gradient_block() -> dict[str, Any]:
    rows = []
    for q, p in GRADIENT_PRIMES:
        for e in (3, 4):
            print(f"[scan] gradient q={q} p={p} e={e}", flush=True)
            res = scan_e3(p, 64, 36, 1) if e == 3 else scan_e4(p, 64, 36, 1)
            rows.append(
                {
                    "q": q,
                    "p": p,
                    "n": 64,
                    "t": 36,
                    "e": e,
                    "step": 1,
                    "subsets": math.comb(36, e),
                    "model_ET": model_ET(36, e, p),
                    **res,
                }
            )
    return {"status": "EXACT_STEP1_GRADIENT_CROSSCHECK_PR468", "rows": rows}


def ladder_block() -> dict[str, Any]:
    rows = []
    for block_id, p, n, t, e, steps in LADDER_BLOCKS:
        step_list = primitive_steps(n) if steps == "all" else list(steps)
        print(f"[scan] {block_id}: {len(step_list)} step(s)", flush=True)
        tc, pc = [], []
        for st in step_list:
            res = scan_e3(p, n, t, st) if e == 3 else scan_e4(p, n, t, st)
            tc.append(res["T"])
            pc.append(res["partner_pairs"])
        rows.append(
            {
                "id": block_id,
                "q": (p - 1) // n,
                "p": p,
                "n": n,
                "t": t,
                "e": e,
                "steps": step_list,
                "steps_mode": "all_units" if steps == "all" else "registered_subset",
                "step_T_counts": tc,
                "step_partner_pair_counts": pc,
                "T_sum": sum(tc),
                "T_max": max(tc),
                "subsets_per_step": math.comb(t, e),
                "subsets_total": len(step_list) * math.comb(t, e),
                "model_ET_per_step": model_ET(t, e, p),
            }
        )
    return {"status": "EXACT_REGISTERED_LADDER", "rows": rows}


# --------------------------- deployed-row witnesses ---------------------------

def witness_record(uidx, vidx, e: int, family: str) -> dict[str, Any]:
    arc, _ = deployed_arc()
    cu = locator_coefficients(uidx, arc, P_KB)
    cv = locator_coefficients(vidx, arc, P_KB)
    if cu[:-1] != cv[:-1] or cu[-1] == cv[-1]:
        raise CheckFailure("invalid free-1 witness")
    return {
        "e": e,
        "family": family,
        "U_indices": list(uidx),
        "V_indices": list(vidx),
        "U_values": [arc[i] for i in uidx],
        "V_values": [arc[i] for i in vidx],
        "high_signature": cu[1:-1],
        "constant_U": cu[-1],
        "constant_V": cv[-1],
    }


def search_e4_witnesses() -> dict[str, Any]:
    """U = {zeta, u1, u2, -u2} with u1 = omega^134943 (so -u1 = zeta), partner
    V = {v1, -v1, v2, -v2}; collision u1^2+u2^2 = v1^2+v2^2 on squares."""
    arc, _ = deployed_arc()
    sq = [x * x % P_KB for x in arc[:CAP_ANTI]]
    x0 = sq[CAP_ANTI - 1]
    smap: dict[int, int] = {}
    for j2 in range(CAP_ANTI - 1):
        s = x0 + sq[j2]
        if s >= P_KB:
            s -= P_KB
        smap[s] = j2
    found: dict[int, tuple[int, int]] = {}
    pairs = 0
    for k1 in range(CAP_ANTI - 1):
        if len(found) >= E4_TARGET or pairs >= E4_PAIR_CAP:
            break
        a = sq[k1]
        for k2 in range(k1 + 1, CAP_ANTI):
            pairs += 1
            if pairs > E4_PAIR_CAP:
                break
            s = a + sq[k2]
            if s >= P_KB:
                s -= P_KB
            j2 = smap.get(s)
            if j2 is None:
                continue
            if CAP_ANTI - 1 in (k1, k2) or j2 in (k1, k2):
                continue
            if j2 not in found:
                found[j2] = (k1, k2)
                if len(found) >= E4_TARGET:
                    break
    wits = []
    for j2, (k1, k2) in found.items():
        u = sorted([CAP_ANTI - 1, NP_KB - 1, j2, j2 + HALF])
        v = sorted([k1, k1 + HALF, k2, k2 + HALF])
        wits.append(witness_record(u, v, 4, "antipodal_square_pair"))
    return {"witnesses": wits, "pairs_scanned": pairs, "pair_cap": E4_PAIR_CAP}


def search_e3_witnesses() -> dict[str, Any]:
    """U = {zeta, x, y} terminal; partner V = {a, -a, c} with c = zeta+x+y in
    arc and a^2 = -(zeta(x+y)+xy) in mu_{n/2}, both roots' indices < t."""
    arc, arcdict = deployed_arc()
    arcset = set(arc)
    zeta = arc[NP_KB - 1]
    found = []
    trials = 0
    i = 0
    while len(found) < E3_TARGET and i < NP_KB - 2 and trials < E3_TRIAL_CAP:
        x = arc[i]
        zx = (zeta + x) % P_KB
        for j in range(i + 1, NP_KB - 1):
            y = arc[j]
            s = zx + y
            if s >= P_KB:
                s -= P_KB
            trials += 1
            if trials > E3_TRIAL_CAP:
                break
            if s not in arcset:
                continue
            if s == zeta or s == x or s == y:
                continue
            d = (-(zeta * (x + y) + x * y)) % P_KB
            if d == 0 or pow(d, HALF, P_KB) != 1:
                continue
            a1 = tonelli_sqrt(d)
            i1 = arcdict.get(a1)
            if i1 is None:
                a1 = P_KB - a1
                i1 = arcdict.get(a1)
            i0 = i1 if i1 < HALF else i1 - HALF
            if i0 >= CAP_ANTI:
                continue
            cidx = arcdict[s]
            uidx = sorted([NP_KB - 1, i, j])
            vidx = sorted([i0, i0 + HALF, cidx])
            if set(uidx) & set(vidx):
                continue
            e3u = zeta * x % P_KB * y % P_KB
            e3v = arc[i0] * arc[i0 + HALF] % P_KB * s % P_KB
            if e3u == e3v:
                continue
            found.append(witness_record(uidx, vidx, 3, "antipodal_point"))
            print(f"[wit] e3 #{len(found)} trials={trials}", flush=True)
            if len(found) >= E3_TARGET:
                break
        i += 1
    return {"witnesses": found, "trials": trials, "trial_cap": E3_TRIAL_CAP}


def scan_e4_family() -> dict[str, Any]:
    """Exact partner census over the first E4_FAMILY_SAMPLE antipodal centers.

    For j2 < sample, U(j2) = {omega^134943, zeta, omega^j2, -omega^j2} is a
    distinct terminal 4-set; it has an antipodal-quad partner iff
    s = x0 + sq[j2] is a sum sq[k1] + sq[k2] of a different square pair.
    Every partnered j2 is exactly verified by locator expansion, so the
    partnered count is a PROVED lower bound on |T(n',4)|."""
    arc, _ = deployed_arc()
    sq = [x * x % P_KB for x in arc[:CAP_ANTI]]
    sqdict = {v: i for i, v in enumerate(sq)}
    x0 = sq[CAP_ANTI - 1]
    partnered: list[list[int]] = []
    lookups = 0
    for j2 in range(E4_FAMILY_SAMPLE):
        s = x0 + sq[j2]
        if s >= P_KB:
            s -= P_KB
        hit = None
        for k1 in range(CAP_ANTI):
            lookups += 1
            if k1 == CAP_ANTI - 1 or k1 == j2:
                continue
            r = s - sq[k1]
            if r < 0:
                r += P_KB
            k2 = sqdict.get(r)
            if k2 is None or k2 == k1 or k2 == CAP_ANTI - 1 or k2 == j2:
                continue
            hit = (k1, k2)
            break
        if hit is not None:
            u = sorted([CAP_ANTI - 1, NP_KB - 1, j2, j2 + HALF])
            v = sorted([hit[0], hit[0] + HALF, hit[1], hit[1] + HALF])
            cu = locator_coefficients(u, arc, P_KB)
            cv = locator_coefficients(v, arc, P_KB)
            if cu[:-1] != cv[:-1] or cu[-1] == cv[-1]:
                raise CheckFailure("family scan produced invalid pair")
            partnered.append([j2, hit[0], hit[1]])
    lam = (CAP_ANTI - 1) * (CAP_ANTI - 2) / 2 / P_KB
    return {
        "sample": E4_FAMILY_SAMPLE,
        "partnered_count": len(partnered),
        "partnered_rate": sig6(len(partnered) / E4_FAMILY_SAMPLE),
        "model_rate": sig6(-math.expm1(-lam)),
        "lookups": lookups,
        "partnered_triples": partnered,
    }


@lru_cache(maxsize=None)
def _ts_nonresidue() -> int:
    z = 2
    while pow(z, (P_KB - 1) // 2, P_KB) != P_KB - 1:
        z += 1
    return z


def tonelli_sqrt(a: int) -> int:
    if a == 0:
        return 0
    if pow(a, (P_KB - 1) // 2, P_KB) != 1:
        raise CheckFailure("tonelli on non-residue")
    q = P_KB - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    m, c = s, pow(_ts_nonresidue(), q, P_KB)
    t = pow(a, q, P_KB)
    r = pow(a, (q + 1) // 2, P_KB)
    while t != 1:
        i, tmp = 0, t
        while tmp != 1:
            tmp = tmp * tmp % P_KB
            i += 1
        b = pow(c, 1 << (m - i - 1), P_KB)
        m, c = i, b * b % P_KB
        t, r = t * c % P_KB, r * b % P_KB
    return r


# ------------------------------ lemma records ---------------------------------

def lemma_records() -> dict[str, Any]:
    return {
        "L1_disjointness": {
            "status": "PROVED",
            "statement": (
                "If U != V are e-sets with equal high signature then "
                "f_U - f_V is a nonzero constant, so f_U and f_V share no "
                "roots and U, V are disjoint (any field, any e)."
            ),
            "credit": "implicit in Hughes v25/v51 and the PR #468 scan gates",
        },
        "L2_terminal_uniqueness": {
            "status": "PROVED",
            "statement": (
                "For each high signature h there is at most one terminal "
                "e-set: a monic locator through zeta with high h has its "
                "constant term forced to -(zeta^e + sum_i h_i zeta^i).  "
                "Hence partners of terminal sets are automatically "
                "non-terminal, |T| <= C(n'-1, e-1), and Hughes's star center "
                "U_* is the unique terminal holder of its high."
            ),
            "credit": "cleanup of Hughes v53/v54 (disjointness route)",
        },
        "L3_coset_classification": {
            "status": "PROVED",
            "statement": (
                "For d | n, d > 1, a mu_d-coset of mu_n lies in the prefix "
                "I_t iff d = 2 and the base index is < t - n/2 = 134944: the "
                "complement window has length n - t = 913632 >= n/d for all "
                "d >= 4, so every mu_d-coset (d >= 4) meets it, while d = 2 "
                "spacing n/2 = 1048576 exceeds the window.  The only "
                "coset-structured free-1 pairs on the deployed arc are the "
                "antipodal e=2 family."
            ),
        },
        "L4_e4_family": {
            "status": "PROVED",
            "statement": (
                "For antipodal quadruples, f = X^4 - (u1^2+u2^2) X^2 + "
                "u1^2 u2^2; two disjoint quadruples with equal square-sums "
                "and distinct square-pairs form a free-1 pair.  With "
                "u1 = omega^134943 the quadruple contains zeta and is "
                "terminal."
            ),
        },
        "L5_e3_family": {
            "status": "PROVED",
            "statement": (
                "V = {a, -a, c} has e_1 = c, e_2 = -a^2, e_3 = -a^2 c; U = "
                "{zeta, x, y} has a partner of this form iff c := zeta+x+y "
                "is in the arc, D := -(zeta(x+y)+xy) is in mu_{n/2}, both "
                "square roots' indices are < t, the sets are disjoint, and "
                "e_3 differs."
            ),
        },
        "L6_e2_close": {
            "status": "PROVED",
            "statement": (
                "|T(t,2)| <= p <= H2 for every t <= n': the e=2 high is the "
                "single coefficient e_1, and p <= H2 holds iff the deployed "
                "e = 67472 >= 1860.  The e=2 close is deployment-dependent "
                "through H2."
            ),
            "credit": "Hughes v48/v50; re-derived",
        },
    }


# ------------------------------- certificate ----------------------------------

def build_certificate() -> dict[str, Any]:
    arith = deployed_arithmetic()
    grad = gradient_block()
    ladder = ladder_block()
    w4 = search_e4_witnesses()
    fam = scan_e4_family()
    w3 = search_e3_witnesses()
    subset_total = sum(r["subsets"] for r in grad["rows"]) + sum(
        r["subsets_total"] for r in ladder["rows"]
    )
    return {
        "packet": "cap25_v13_hughes_wall_small_e",
        "date": "2026-07-10",
        "status": "WITNESSES_PROVED_WALL_OPEN",
        "claims": {
            "pins_wall_statement": True,
            "proves_T3_ge": len(w3["witnesses"]),
            "proves_T4_ge": len(w4["witnesses"]),
            "proves_T4_family_scan_ge": fam["partnered_count"],
            "proves_e2_close_rederived": True,
            "proves_terminal_uniqueness_all_e": True,
            "proves_exact_budget_arithmetic": True,
            "proves_registered_toy_counts": True,
            "proves_deployed_T_le_H2": False,
            "proves_e3_wall": False,
            "proves_e4_wall": False,
            "counterexample_to_wall_found": False,
            "refutes_any_hughes_claim": False,
            "witnesses_beyond_canonical_omega": False,
            "proves_A_SP_le_tp": False,
            "proves_R2_le_ep": False,
        },
        "deployed": {
            "p": P_KB,
            "n": N_KB,
            "a_plus": A_KB,
            "n_prime": NP_KB,
            "e": E_KB,
            "H2": H2_KB,
            "subgroup_index": INDEX_KB,
            "generator": 3,
            "omega": pow(3, (P_KB - 1) // N_KB, P_KB),
            "zeta_index": NP_KB - 1,
            "wall_status": "OPEN",
        },
        "wall_statement": (
            "T = { U subset I_{n'} : |U| = e, n'-1 in U, exists V subset "
            "I_{n'}, |V| = e, V != U, f_U - f_V a nonzero constant }; "
            "Hughes chain (v51+v53+v54, v45/v46 accounting) needs "
            "|T| <= H2 = 77291948627 at (n', e) = (1183520, 67472).  "
            "Upper bounds on |T| suffice: |H_unt| <= |T| by the v54 star "
            "injection."
        ),
        "faithfulness_pins": {
            "F1_H2_fixed": (
                "H2 = floor(e*p/1860) with e = 67472 the deployed side "
                "size; the budget does not rescale with side size in the "
                "parametric family (v45: 930*H2 <= e*p/2 pays M_pad<=2)."
            ),
            "F2_direction": (
                "v54's |H_unt| = |T| display is loose; the proved content "
                "is the injection H -> U_* giving |H_unt| <= |T|, and the "
                "chain only consumes upper bounds on |T|."
            ),
            "F3_partner_structure": (
                "Partners are automatically disjoint from U (L1) and "
                "automatically non-terminal (L2); T is well-defined "
                "without either restriction stated."
            ),
            "F4_generator": (
                "T is read on the canonical arc omega = 3^((p-1)/n); "
                "PR #468 proved phase invariance and exhausted primitive "
                "steps at its toy rows; witnesses here are canonical-omega "
                "only, though the antipodal mechanism (index shift n/2 for "
                "every odd step) is step-universal."
            ),
        },
        "lemmas": lemma_records(),
        "arithmetic": arith,
        "gradient_crosscheck": grad,
        "toy_ladder": ladder,
        "witnesses_e4": w4,
        "witnesses_e4_family": fam,
        "witnesses_e3": w3,
        "caps": {
            "address_space_bytes": ADDRESS_SPACE_CAP_BYTES,
            "ladder_subset_evaluations": subset_total,
            "e3_trials_used": w3["trials"],
            "e3_trial_cap": E3_TRIAL_CAP,
            "e4_pairs_used": w4["pairs_scanned"],
            "e4_pair_cap": E4_PAIR_CAP,
            "e4_family_lookups": fam["lookups"],
        },
        "verdict": {
            "e2": "CLOSED (Hughes v48; re-derived, gate e>=1860)",
            "e3": (
                "OPEN; heuristically true at 0.55*H2 with witnesses >= "
                f"{len(w3['witnesses'])}; needs exactly a 9.0612x "
                "improvement over the terminal-injection bound C(n'-1,2)"
            ),
            "e4_to_59": (
                "heuristic overload band (30.2x H2 at e=4, peak 2^46 x H2 "
                "at e=26); uniform-in-e proof routes are doomed; witnesses "
                f">= {fam['partnered_count']} at e=4 (family scan, rate "
                f"{fam['partnered_rate']} vs model {fam['model_rate']})"
            ),
            "e60_plus": "heuristically true, margin grows without bound",
            "chain_case": (
                "e = 67472: load < 2^-1344158; wall heuristically true by "
                "total paucity (likely |T| = 0); proof remains OPEN"
            ),
        },
        "lineage": {
            "supports_scott_hughes_route_d": True,
            "source": "Hughes Route-D v1-v54 (PR #423, integrated STATUS)",
            "builds_on_pr468_sparse_arc_scan": True,
            "independent_followup": True,
        },
    }


# ------------------------------- validation -----------------------------------

def validate_witness(w: dict[str, Any], checks: Checks) -> None:
    arc, _ = deployed_arc()
    e = w["e"]
    u = w["U_indices"]
    v = w["V_indices"]
    checks.equal(len(u), e, "witness |U|")
    checks.equal(len(v), e, "witness |V|")
    checks.equal(u, sorted(set(u)), "witness U sorted-set")
    checks.equal(v, sorted(set(v)), "witness V sorted-set")
    checks.check(all(0 <= i < NP_KB for i in u + v), "witness prefix bounds")
    checks.check(NP_KB - 1 in u, "witness terminal mark")
    checks.check(not (set(u) & set(v)), "witness disjoint")
    checks.equal(w["U_values"], [arc[i] for i in u], "witness U values")
    checks.equal(w["V_values"], [arc[i] for i in v], "witness V values")
    cu = locator_coefficients(u, arc, P_KB)
    cv = locator_coefficients(v, arc, P_KB)
    checks.equal(cu[:-1], cv[:-1], "witness equal high")
    checks.check(cu[-1] != cv[-1], "witness distinct constants")
    checks.equal(w["high_signature"], cu[1:-1], "witness signature")
    checks.equal(w["constant_U"], cu[-1], "witness constant U")
    checks.equal(w["constant_V"], cv[-1], "witness constant V")
    if w["family"] == "antipodal_square_pair":
        checks.check(
            all(i + HALF in u or i - HALF in u for i in u), "U antipodal quad"
        )
        checks.check(
            all(i + HALF in v or i - HALF in v for i in v), "V antipodal quad"
        )
    if w["family"] == "antipodal_point":
        anti = [i for i in v if (i + HALF in v) or (i - HALF in v)]
        checks.equal(len(anti), 2, "V has one antipodal pair")


def validate_certificate(
    cert: dict[str, Any], replay: dict[str, Any] | None, checks: Checks
) -> None:
    checks.equal(cert["packet"], "cap25_v13_hughes_wall_small_e", "packet")
    checks.equal(cert["status"], "WITNESSES_PROVED_WALL_OPEN", "status")
    dep = cert["deployed"]
    checks.equal(dep["p"], P_KB, "p")
    checks.check(is_prime(P_KB), "p prime")
    checks.equal(dep["n"], N_KB, "n")
    checks.equal(dep["n_prime"], NP_KB, "n prime")
    checks.equal(dep["e"], E_KB, "e")
    checks.equal(dep["H2"], H2_KB, "H2")
    checks.equal(dep["subgroup_index"], INDEX_KB, "index 1016")
    checks.equal(dep["wall_status"], "OPEN", "wall stays OPEN")
    cl = cert["claims"]
    checks.equal(cl["proves_deployed_T_le_H2"], False, "nonclaim deployed H2")
    checks.equal(cl["proves_e3_wall"], False, "nonclaim e3 wall")
    checks.equal(cl["proves_e4_wall"], False, "nonclaim e4 wall")
    checks.equal(cl["counterexample_to_wall_found"], False, "nonclaim cx")
    checks.equal(cl["refutes_any_hughes_claim"], False, "nonclaim refute")
    checks.equal(cl["proves_A_SP_le_tp"], False, "nonclaim ASP")
    checks.equal(cl["proves_R2_le_ep"], False, "nonclaim R2")
    checks.equal(
        cert["lineage"]["supports_scott_hughes_route_d"], True, "lineage"
    )

    # exact arithmetic gates, recomputed
    ar = cert["arithmetic"]
    checks.equal(ar["H2"], E_KB * P_KB // 1860, "H2 formula")
    checks.equal(ar["e_times_p"], 143763024447376, "e*p")
    checks.check(P_KB <= H2_KB, "p <= H2")
    checks.check(E_KB >= 1860, "1860 gate")
    c2 = math.comb(NP_KB - 1, 2)
    c3 = math.comb(NP_KB - 1, 3)
    c4 = math.comb(NP_KB - 1, 4)
    checks.equal(ar["C_np1_2"], c2, "C(n'-1,2)")
    checks.equal(c2, 700358019921, "C(n'-1,2) pinned")
    checks.check(9 * H2_KB < c2 < 10 * H2_KB, "trivial e3 deficit in (9,10)")
    checks.check(P_KB * P_KB > H2_KB, "v48 method break at e=3")
    checks.check(c2 * c3 < H2_KB * P_KB * P_KB, "e3 load < H2 exact")
    checks.check(c3 * c4 > 30 * H2_KB * P_KB**3, "e4 load > 30*H2 exact")
    checks.check(c3 * c4 < 31 * H2_KB * P_KB**3, "e4 load < 31*H2 exact")
    checks.equal(ar["band_first_over"], 4, "band starts at 4")
    checks.equal(ar["band_last_over"], 59, "band ends at 59")
    checks.equal(ar["band_reentry"], 60, "band reentry 60")
    checks.equal(ar["band_peak_e"], 26, "band peak 26")
    for row in ar["band"]:
        e = row["e"]
        num = math.comb(NP_KB - 1, e - 1) * math.comb(NP_KB - 1, e)
        den = P_KB ** (e - 1)
        checks.equal(row["exceeds_H2"], num > H2_KB * den, f"band e={e}")
    checks.equal(ar["chain_margin_bits"], 1344159, "chain margin bits")
    checks.equal(ar["antipodal_capacity"], 134944, "antipodal capacity")
    checks.check(ar["coset_d_ge_4_dies"], "coset d>=4 dies")
    checks.check(ar["coset_d_2_survives"], "coset d=2 survives")

    # witnesses, re-verified from scratch
    w3 = cert["witnesses_e3"]["witnesses"]
    w4 = cert["witnesses_e4"]["witnesses"]
    checks.check(len(w3) >= E3_TARGET, "e3 witness count")
    checks.check(len(w4) >= E4_TARGET, "e4 witness count")
    checks.equal(cl["proves_T3_ge"], len(w3), "T3 claim consistency")
    checks.equal(cl["proves_T4_ge"], len(w4), "T4 claim consistency")
    for w in w3:
        checks.equal(w["e"], 3, "e3 witness side size")
        validate_witness(w, checks)
    for w in w4:
        checks.equal(w["e"], 4, "e4 witness side size")
        validate_witness(w, checks)
    checks.equal(
        len({tuple(w["U_indices"]) for w in w3}), len(w3), "e3 distinct U"
    )
    checks.equal(
        len({tuple(w["U_indices"]) for w in w4}), len(w4), "e4 distinct U"
    )

    # family scan: exact structural gates + subsampled full verification
    fam = cert["witnesses_e4_family"]
    trip = fam["partnered_triples"]
    checks.equal(fam["sample"], E4_FAMILY_SAMPLE, "family sample size")
    checks.equal(fam["partnered_count"], len(trip), "family count consistency")
    checks.equal(cl["proves_T4_family_scan_ge"], len(trip), "family claim")
    checks.check(len(trip) >= E4_TARGET, "family scan beats witness floor")
    j2s = [t[0] for t in trip]
    checks.equal(j2s, sorted(set(j2s)), "family j2 strictly increasing")
    checks.check(all(0 <= t[0] < E4_FAMILY_SAMPLE for t in trip), "family j2 range")
    arc, _ = deployed_arc()
    for pos in range(0, len(trip), 50):
        j2, k1, k2 = trip[pos]
        checks.check(
            len({j2, k1, k2, CAP_ANTI - 1}) == 4 and 0 <= min(k1, k2)
            and max(k1, k2) < CAP_ANTI,
            "family triple indices",
        )
        u = sorted([CAP_ANTI - 1, NP_KB - 1, j2, j2 + HALF])
        v = sorted([k1, k1 + HALF, k2, k2 + HALF])
        cu = locator_coefficients(u, arc, P_KB)
        cv = locator_coefficients(v, arc, P_KB)
        checks.equal(cu[:-1], cv[:-1], f"family pair high (pos {pos})")
        checks.check(cu[-1] != cv[-1], f"family pair constants (pos {pos})")
    checks.check(
        cert["caps"]["e3_trials_used"] <= cert["caps"]["e3_trial_cap"],
        "e3 trial cap",
    )
    checks.check(
        cert["caps"]["e4_pairs_used"] <= cert["caps"]["e4_pair_cap"],
        "e4 pair cap",
    )

    # toy rows: identities
    for row in cert["gradient_crosscheck"]["rows"]:
        checks.check(is_prime(row["p"]), "gradient p prime")
        checks.equal(row["p"], row["q"] * row["n"] + 1, "gradient index")
        checks.equal(row["subsets"], math.comb(row["t"], row["e"]), "gradient subsets")
    pr468 = {(4, 3): (55, 58), (18, 3): (4, 4), (67, 3): (0, 0),
             (253, 3): (0, 0), (513, 3): (0, 0), (1017, 3): (0, 0),
             (4, 4): (11, 11), (18, 4): (0, 0), (67, 4): (0, 0),
             (253, 4): (0, 0), (513, 4): (0, 0), (1017, 4): (0, 0)}
    for row in cert["gradient_crosscheck"]["rows"]:
        exp = pr468[(row["q"], row["e"])]
        checks.equal((row["T"], row["partner_pairs"]), exp,
                     f"PR468 crosscheck q={row['q']} e={row['e']}")
    for row in cert["toy_ladder"]["rows"]:
        checks.check(is_prime(row["p"]), "ladder p prime")
        checks.equal(row["p"], row["q"] * row["n"] + 1, "ladder index")
        checks.equal(row["t"] * 16, 9 * row["n"], "ladder shape 9/16")
        checks.equal(
            row["subsets_total"],
            len(row["steps"]) * math.comb(row["t"], row["e"]),
            "ladder subsets",
        )
        checks.equal(row["T_sum"], sum(row["step_T_counts"]), "ladder T sum")
        checks.equal(row["T_max"], max(row["step_T_counts"]), "ladder T max")
    onset = next(
        r for r in cert["toy_ladder"]["rows"] if r["id"] == "kb_shape_n1024_e3_onset"
    )
    checks.check(onset["T_max"] > 0, "onset row exhibits T > 0 at sparse index")
    q1016 = next(
        r for r in cert["toy_ladder"]["rows"] if r["id"] == "kb_shape_n512_e3_q1016"
    )
    checks.equal(q1016["q"], 1016, "exact KB index row present")

    if replay is not None:
        checks.equal(cert, replay, "full exact replay")


# ------------------------------- tamper suite ----------------------------------

def tamper_suite(cert: dict[str, Any], replay: dict[str, Any]) -> tuple[int, int]:
    def m_claim(d):
        d["claims"]["proves_deployed_T_le_H2"] = True

    def m_cx(d):
        d["claims"]["counterexample_to_wall_found"] = True

    def m_h2(d):
        d["deployed"]["H2"] += 1

    def m_wit_idx(d):
        d["witnesses_e3"]["witnesses"][0]["U_indices"][1] += 1

    def m_wit_sig(d):
        d["witnesses_e4"]["witnesses"][0]["high_signature"][0] ^= 1

    def m_wit_term(d):
        w = d["witnesses_e3"]["witnesses"][1]
        w["U_indices"], w["V_indices"] = w["V_indices"], w["U_indices"]
        w["U_values"], w["V_values"] = w["V_values"], w["U_values"]

    def m_onset(d):
        row = next(
            r for r in d["toy_ladder"]["rows"]
            if r["id"] == "kb_shape_n1024_e3_onset"
        )
        row["step_T_counts"] = [0] * len(row["step_T_counts"])
        row["T_sum"] = 0
        row["T_max"] = 0

    def m_band(d):
        d["arithmetic"]["band_last_over"] = 58

    def m_margin(d):
        d["arithmetic"]["chain_margin_bits"] = 1

    def m_grad(d):
        d["gradient_crosscheck"]["rows"][0]["T"] += 1

    def m_lineage(d):
        d["lineage"]["supports_scott_hughes_route_d"] = False

    def m_family_triple(d):
        d["witnesses_e4_family"]["partnered_triples"][0][1] += 1

    def m_family_count(d):
        d["witnesses_e4_family"]["partnered_count"] += 1

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("promote-deployed-H2", m_claim),
        ("fake-counterexample", m_cx),
        ("H2-drift", m_h2),
        ("witness-index", m_wit_idx),
        ("witness-signature", m_wit_sig),
        ("witness-terminal-swap", m_wit_term),
        ("onset-zeroed", m_onset),
        ("band-edge", m_band),
        ("margin-bits", m_margin),
        ("gradient-count", m_grad),
        ("lineage", m_lineage),
        ("family-triple", m_family_triple),
        ("family-count", m_family_count),
    ]
    caught = 0
    for label, mutate in mutations:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            validate_certificate(bad, replay, Checks())
        except (CheckFailure, KeyError, IndexError, TypeError, ValueError, StopIteration):
            caught += 1
            print(f"[tamper] CAUGHT {label}")
        else:
            print(f"[tamper] MISSED {label}")
    return caught, len(mutations)


# ----------------------------------- main --------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    cap = impose_address_space_cap()
    print(f"[cap] RLIMIT_AS={cap} bytes")
    t0 = time.time()
    replay = build_certificate()
    print(f"[time] recompute {time.time() - t0:.1f}s", flush=True)

    if args.generate:
        checks = Checks()
        validate_certificate(replay, None, checks)
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")
        print(f"RESULT: GENERATED ({checks.passed}/{checks.total} checks)")
        print(f"certificate: {CERT_PATH}")
        return

    if not CERT_PATH.exists():
        raise CheckFailure(f"missing certificate: {CERT_PATH}")
    stored = json.loads(CERT_PATH.read_text())
    checks = Checks()
    validate_certificate(stored, replay, checks)
    caught, total = tamper_suite(stored, replay)
    checks.check(total >= 8, "at least eight tampers")
    checks.equal(caught, total, "all tampers caught")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(
        f"RESULT: PASS ({checks.passed}/{checks.total} checks; "
        f"tampers {caught}/{total})"
    )
    print(f"peak RSS: {rss // 1024} MiB; wall time {time.time() - t0:.1f}s")
    print(
        "status: witnesses PROVED (T(n',3) >= "
        f"{len(stored['witnesses_e3']['witnesses'])}, T(n',4) >= "
        f"{stored['witnesses_e4_family']['partnered_count']} by family "
        "scan); deployed wall |T| <= H2 remains OPEN"
    )


if __name__ == "__main__":
    main()
