#!/usr/bin/env python3
"""Verifier for the signed-payment source-clause census (EXPERIMENTAL).

Route: hard input #2 (agents.md L47/L67) -- "image-scale MI + MA, or a direct
Sidon payment" -- specifically the signed-minor clause of the
charge-preserving semantic-or-signed dichotomy named in avdeevvadim's PR #716
(`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`, section
6). PR #716's abstract kernel-sign mask attains normalized q-gain
`L**(1/2-1/q)` while violating four source-realizability clauses:

  (i)   certified weighted-Vandermonde columns,
  (ii)  one complete dyadic |tau(gamma)| band,
  (iii) first-match residual mask,
  (iv)  owners on one received affine line.

The census has TWO regimes:

SPARSE arm: moment-curve source over F_p (columns rho(t)*(1,t,...,t^{R-1}),
R=3, pair supports, M/L -> 0), p in {3,5,7,11}.

DENSE arm: the superincreasing depth-1 family of PR #717
(`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`,
Section 7): A_i=5^i, C=2*sum(A_i)+1, T={A_i} u {C-A_i}, a=B, Phi(S)=sum(S)
over Z_C, where the fiber load WL/M grows like (3/2)^B; B in {2,4,6}.
(B=8 has prime C=976561: no CRT split for the pure-python DFT, excluded and
stated, not silently capped.)

For each arm this script recomputes every table number in the companion note
from the JSON witnesses: it rebuilds the ambient group, the character band,
the residual mask, and the projected q-norm for each of six constraint sets
(A = no clauses, B = all four imposed, C_i..C_iv = each clause ablated
alone), checks every witness against the clause-compliance predicate its
cell claims, recomputes both arms' log-log gain-vs-|G| exponent fits,
recomputes PR #717 Section 7's own table row facts (M, image size, fiber
size W at 0, s_0 = BC/2 == 0 mod C, Johnson |S^S'| <= a-2 on the fiber), and
independently replicates PR #716's F_3^6 anchor (published normalized q-gain
1.1182491777).

This is a CENSUS, not a proof: it does not establish the dichotomy, does not
touch A4 or primitive Q, and the "local_search" cells are certified lower
bounds on the true per-cell maximum, not exact maxima (the JSON marks each
cell's search_mode; see the Nonclaims section of the companion note).

Stdlib only. Run:
  python3 experimental/scripts/verify_signed_minor_payment_clause_census_v1.py
  python3 experimental/scripts/verify_signed_minor_payment_clause_census_v1.py --tamper-selftest
"""
from __future__ import annotations

import argparse
import cmath
import itertools
import json
import math
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT_PATH = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "signed-minor-payment-clause-census-v1",
    "signed_minor_payment_clause_census_v1.json",
)

FAILS: list[str] = []
NCHECK = 0
GAIN_TOL = 1e-6
FIT_TOL = 1e-6


def check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"   ({detail})"
    print(line)
    if not cond:
        FAILS.append(name)


def close(a: float, b: float, tol: float = GAIN_TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------------------
# Group / character primitives (F_p^R, standard additive characters).
# ---------------------------------------------------------------------------

def group_elements(p: int, R: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(p), repeat=R))


def vec_add(x, y, p):
    return tuple((a + b) % p for a, b in zip(x, y))


def vec_sub(x, y, p):
    return tuple((a - b) % p for a, b in zip(x, y))


def vec_neg(x, p):
    return tuple((-a) % p for a in x)


def vec_scalar(c, x, p):
    return tuple((c * a) % p for a in x)


def vec_dot(x, y, p):
    return sum(a * b for a, b in zip(x, y)) % p


def character(xi, x, p) -> complex:
    return cmath.exp(2j * math.pi * vec_dot(xi, x, p) / p)


def scalar_orbits(group: list[tuple[int, ...]], p: int) -> list[tuple[tuple[int, ...], ...]]:
    zero = tuple(0 for _ in group[0])
    unseen = set(group)
    unseen.discard(zero)
    orbits = []
    while unseen:
        root = min(unseen)
        orbit = frozenset(vec_scalar(c, root, p) for c in range(1, p))
        orbits.append(tuple(sorted(orbit)))
        unseen -= orbit
    orbits.sort()
    return orbits


def is_orbit_closed(band: set, p: int) -> bool:
    """True iff band is a union of complete scalar orbits (closed under all
    nonzero scalar multiplication) -- the structural signature of a "dense
    symmetric" free band, as opposed to an arbitrary character subset."""
    for xi in band:
        for c in range(1, p):
            if vec_scalar(c, xi, p) not in band:
                return False
    return True


def vandermonde_column(t: int, R: int, p: int) -> tuple[int, ...]:
    return tuple(pow(t, j, p) for j in range(R))


def arbitrary_column(t: int, R: int, p: int, salt: int = 20260713) -> tuple[int, ...]:
    """Deterministic, reproducible, non-Vandermonde column formula (clause-i
    ablation). Recomputed here from (t, R, p, salt) alone -- not read as a
    free witness -- so the certificate cannot silently swap in a Vandermonde
    column while claiming clause i is ablated."""
    out = []
    for j in range(R):
        v = (salt * (j + 1) + 7 * t * t + 3 * t * (j + 2) + 11 * j + 5) % p
        out.append(v)
    return tuple(out)


def kernel_for_band(group, band, p: int, L: int) -> dict:
    band = list(band)
    return {x: sum(character(xi, x, p) for xi in band) / L for x in group}


def convolve_sparse(group, kernel: dict, sparse_values: dict, p: int) -> dict:
    items = [(y, v) for y, v in sparse_values.items() if v != 0]
    out = {}
    for x in group:
        s = 0
        for y, v in items:
            d = vec_sub(x, y, p)
            s += kernel[d] * v
        out[x] = s
    return out


def q_norm(values: dict, q: float) -> float:
    return sum(abs(v) ** q for v in values.values()) ** (1.0 / q)


def normalized_gain(group, kernel, sparse_values, p, L, q) -> float:
    projected = convolve_sparse(group, kernel, sparse_values, p)
    return q_norm(projected, q) / (L ** (1.0 / q))


def tau_all(group, columns_by_t: dict, p: int) -> dict:
    zero = tuple(0 for _ in group[0])
    cols = list(columns_by_t.values())
    out = {}
    for xi in group:
        if xi == zero:
            continue
        out[xi] = sum(character(xi, v, p) for v in cols)
    return out


def dyadic_level(mag: float):
    if mag < 1.0:
        return None
    return int(math.floor(math.log2(mag)))


def dyadic_bands(group, columns_by_t: dict, p: int) -> dict:
    taus = tau_all(group, columns_by_t, p)
    levels: dict = {}
    for xi, tval in taus.items():
        lvl = dyadic_level(abs(tval))
        if lvl is None:
            continue
        levels.setdefault(lvl, []).append(xi)
    return levels


def enumerate_supports(p: int) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(p), 2))


def dedup_mask(supports, columns_by_t, p) -> list[int]:
    """First-match residual mask (clause iii): 1 iff this support is the
    first, in the fixed lexicographic enumeration, to realize its image."""
    seen = set()
    mask = []
    for S in supports:
        img = vec_add(columns_by_t[S[0]], columns_by_t[S[1]], p)
        if img in seen:
            mask.append(0)
        else:
            seen.add(img)
            mask.append(1)
    return mask


def owner_of(idx: int, p: int) -> int:
    return idx % p


# ---------------------------------------------------------------------------
# Cell-level recomputation.
# ---------------------------------------------------------------------------

CLAUSES = ("i", "ii", "iii", "iv")


def recompute_columns(cell: dict, p: int, R: int) -> dict:
    kind = cell["columns_kind"]
    stored = {int(t): tuple(v) for t, v in cell["columns"].items()}
    if kind == "vandermonde":
        recomputed = {t: vandermonde_column(t, R, p) for t in range(p)}
    elif kind == "arbitrary":
        recomputed = {t: arbitrary_column(t, R, p) for t in range(p)}
    else:
        raise AssertionError(f"unknown columns_kind {kind!r}")
    return stored, recomputed


def recompute_cell(cell: dict, group, p: int, R: int, L: int, q: float) -> dict:
    """Recompute the gain and all clause-compliance predicates for one cell.
    Returns a dict of booleans plus the recomputed gain."""
    clauses_imposed = set(cell["clauses_imposed"])
    stored_cols, recomputed_cols = recompute_columns(cell, p, R)

    out: dict[str, Any] = {}

    # Columns must match their own formula exactly (protects both directions:
    # a "vandermonde" cell whose stored columns quietly aren't, or an
    # "arbitrary" cell whose stored columns quietly are).
    out["columns_match_formula"] = (stored_cols == recomputed_cols)

    if "i" in clauses_imposed:
        van = {t: vandermonde_column(t, R, p) for t in range(p)}
        out["clause_i_ok"] = (cell["columns_kind"] == "vandermonde") and (stored_cols == van)
    else:
        van = {t: vandermonde_column(t, R, p) for t in range(p)}
        out["clause_i_ok"] = (cell["columns_kind"] == "arbitrary") and (stored_cols != van)

    supports = enumerate_supports(p)
    images = [vec_add(stored_cols[S[0]], stored_cols[S[1]], p) for S in supports]
    M = len(supports)

    band = [tuple(xi) for xi in cell["band"]["characters"]]
    band_set = set(band)
    out["band_well_formed"] = (len(band) == len(band_set)) and all(len(xi) == R for xi in band)

    if "ii" in clauses_imposed:
        levels = dyadic_bands(group, stored_cols, p)
        lvl = cell["band"]["level"]
        out["clause_ii_ok"] = (lvl in levels) and (set(levels[lvl]) == band_set)
    else:
        out["clause_ii_ok"] = is_orbit_closed(band_set, p) and (len(band_set) > 0)

    mask_bits = list(cell["mask"]["bits"])
    out["mask_well_formed"] = (len(mask_bits) == M) and all(b in (0, 1) for b in mask_bits)

    if "iii" in clauses_imposed:
        expected = dedup_mask(supports, stored_cols, p)
        out["clause_iii_ok"] = (mask_bits == expected)
    else:
        out["clause_iii_ok"] = True  # free; nothing to require structurally

    if "iv" in clauses_imposed and "iii" not in clauses_imposed:
        owners = [owner_of(idx, p) for idx in range(M)]
        ok = True
        seen_owner_val: dict[int, int] = {}
        for idx, b in enumerate(mask_bits):
            o = owners[idx]
            if o in seen_owner_val and seen_owner_val[o] != b:
                ok = False
                break
            seen_owner_val[o] = b
        out["clause_iv_ok"] = ok
    else:
        # iv is either imposed-but-vacuous (iii already fully determines the
        # mask, so there is no remaining freedom for iv to restrict) or
        # explicitly ablated. Either way there is no independent predicate.
        out["clause_iv_ok"] = True

    # Recompute the gain from the witness.
    kernel = kernel_for_band(group, band, p, L)
    sparse = {}
    for idx, b in enumerate(mask_bits):
        if b:
            x = images[idx]
            sparse[x] = sparse.get(x, 0) + 1
    recomputed_gain = normalized_gain(group, kernel, sparse, p, L, q)
    out["recomputed_gain"] = recomputed_gain
    out["gain_matches"] = close(recomputed_gain, cell["gain"])

    search_mode = cell["band"].get("search_mode") or cell["mask"].get("search_mode")
    out["search_mode"] = search_mode

    return out


def linreg(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den else float("nan")
    intercept = mean_y - slope * mean_x
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")
    return slope, intercept, r2


def recompute_fit(fit: dict) -> tuple[float, float, float]:
    Ls = fit["L"]
    gains = fit["gain"]
    xs = [math.log(L) for L in Ls]
    ys = [math.log(max(g, 1e-12)) for g in gains]
    return linreg(xs, ys)


def recompute_anchor(anchor: dict) -> float:
    p = anchor["p"]
    R = anchor["rank"]
    q = anchor["q"]
    orbit_indices = anchor["orbit_indices"]

    group = group_elements(p, R)
    L = len(group)
    orbits = scalar_orbits(group, p)
    chosen = [orbits[i] for i in orbit_indices]
    band = set()
    for orb in chosen:
        band |= set(orb)
    kernel = kernel_for_band(group, band, p, L)

    sign_mask = {y: 1.0 if kernel[vec_neg(y, p)].real >= 0 else 0.0 for y in group}
    projected = convolve_sparse(group, kernel, sign_mask, p)
    qn = q_norm(projected, q)
    return qn / (L ** (1.0 / q))


# ---------------------------------------------------------------------------
# Dense arm: PR #717 Section 7 superincreasing family over Z_C.
# ---------------------------------------------------------------------------

def _coprime_factors(n: int) -> list[int]:
    fs, d, m = {}, 2, n
    while d * d <= m:
        while m % d == 0:
            fs[d] = fs.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        fs[m] = fs.get(m, 0) + 1
    return [p ** e for p, e in sorted(fs.items())]


class GoodThomasDFT:
    """Length-C DFT via the prime-factor (Good-Thomas) algorithm; C = product
    of pairwise-coprime prime powers. Input map n -> (n mod c_a); output map
    k = sum_a k_a * (C/c_a) mod C. No twiddle factors."""

    _cache: dict[int, "GoodThomasDFT"] = {}

    @classmethod
    def get(cls, C: int) -> "GoodThomasDFT":
        if C not in cls._cache:
            cls._cache[C] = cls(C)
        return cls._cache[C]

    def __init__(self, C: int):
        self.C = C
        self.factors = _coprime_factors(C)
        prod = 1
        for c in self.factors:
            prod *= c
        if prod != C:
            raise AssertionError("factorization failure")
        self.mats = []
        for c in self.factors:
            self.mats.append(
                [[cmath.exp(-2j * math.pi * (n * k % c) / c) for n in range(c)] for k in range(c)]
            )
        r = len(self.factors)
        strides = [1] * r
        for a in range(r - 2, -1, -1):
            strides[a] = strides[a + 1] * self.factors[a + 1]
        self.strides = strides
        self.in_index = [0] * C
        for n in range(C):
            pos = 0
            for a, c in enumerate(self.factors):
                pos += (n % c) * strides[a]
            self.in_index[n] = pos
        Ms = [C // c for c in self.factors]
        self.out_k = [0] * C
        for pos in range(C):
            rem, k = pos, 0
            for a, c in enumerate(self.factors):
                ka = rem // strides[a]
                rem %= strides[a]
                k = (k + ka * Ms[a]) % C
            self.out_k[pos] = k
        self.k_to_pos = [0] * C
        for pos in range(C):
            self.k_to_pos[self.out_k[pos]] = pos

    def _axis(self, data, axis, inverse):
        c = self.factors[axis]
        stride = self.strides[axis]
        C = self.C
        mat = self.mats[axis]
        out = [0j] * C
        block = stride * c
        for base in range(0, C, block):
            for off in range(stride):
                start = base + off
                vec = [data[start + j * stride] for j in range(c)]
                for k in range(c):
                    row = mat[k]
                    if inverse:
                        acc = sum(row[j].conjugate() * vec[j] for j in range(c))
                    else:
                        acc = sum(row[j] * vec[j] for j in range(c))
                    out[start + k * stride] = acc
        return out

    def dft(self, x):
        C = self.C
        data = [0j] * C
        for n in range(C):
            data[self.in_index[n]] = x[n]
        for a in range(len(self.factors)):
            data = self._axis(data, a, inverse=False)
        X = [0j] * C
        for pos in range(C):
            X[self.out_k[pos]] = data[pos]
        return X

    def idft(self, X):
        C = self.C
        data = [0j] * C
        for k in range(C):
            data[self.k_to_pos[k]] = X[k]
        for a in range(len(self.factors)):
            data = self._axis(data, a, inverse=True)
        inv = 1.0 / C
        x = [0j] * C
        for n in range(C):
            x[n] = data[self.in_index[n]] * inv
        return x


def dense_superincreasing_columns(B: int) -> tuple[list[int], int]:
    A = [5 ** i for i in range(1, B + 1)]
    C = 2 * sum(A) + 1
    return A + [C - a for a in A], C


def dense_arbitrary_columns(B: int, C: int, salt: int = 20260713) -> list[int]:
    out = []
    for t in range(2 * B):
        v = (salt * (t + 3) + 7 * t * t * t + 11 * t + 5) % C
        if v == 0:
            v = 1
        out.append(v)
    return out


def dense_supports(B: int) -> list[tuple[int, ...]]:
    return list(itertools.combinations(range(2 * B), B))


def dense_images(supports, columns, C) -> list[int]:
    return [sum(columns[i] for i in S) % C for S in supports]


def dense_dedup_mask(supports, images) -> list[int]:
    seen, mask = set(), []
    for idx in range(len(supports)):
        x = images[idx]
        if x in seen:
            mask.append(0)
        else:
            seen.add(x)
            mask.append(1)
    return mask


def dense_tau_classes(C: int, columns: list[int]) -> dict[str, set[int]]:
    """Dyadic |tau| partition of Z_C^* (label '<1' included as its own class)."""
    levels: dict[str, set[int]] = {}
    for xi in range(1, C):
        tau = sum(cmath.exp(2j * math.pi * ((xi * v) % C) / C) for v in columns)
        mag = abs(tau)
        lab = "<1" if mag < 1.0 else str(math.floor(math.log2(mag)))
        levels.setdefault(lab, set()).add(xi)
    return levels


def dense_gain(C: int, band: set[int], f: dict[int, int], q: float) -> float:
    gt = GoodThomasDFT.get(C)
    x = [0j] * C
    for y, v in f.items():
        x[y] = complex(v)
    fh = gt.dft(x)
    gh = [fh[k] if k in band else 0j for k in range(C)]
    g = gt.idft(gh)
    s = 0.0
    for v in g:
        s += abs(v) ** q
    return s ** (1.0 / q) / (C ** (1.0 / q))


def recompute_dense_cell(cell: dict, q: float) -> dict:
    B = cell["B"]
    C = cell["C"]
    clauses_imposed = set(cell["clauses_imposed"])
    stored_cols = list(cell["columns"])
    out: dict[str, Any] = {}

    sup_cols, sup_C = dense_superincreasing_columns(B)
    out["C_matches_family"] = (sup_C == C)
    if cell["columns_kind"] == "superincreasing":
        recomputed = sup_cols
    elif cell["columns_kind"] == "arbitrary":
        recomputed = dense_arbitrary_columns(B, C)
    else:
        raise AssertionError(f"unknown dense columns_kind {cell['columns_kind']!r}")
    out["columns_match_formula"] = (stored_cols == recomputed)

    if "i" in clauses_imposed:
        out["clause_i_ok"] = (cell["columns_kind"] == "superincreasing") and (stored_cols == sup_cols)
    else:
        out["clause_i_ok"] = (cell["columns_kind"] == "arbitrary") and (stored_cols != sup_cols)

    supports = dense_supports(B)
    images = dense_images(supports, stored_cols, C)
    M = len(supports)
    out["M_matches"] = (cell["M"] == M)

    band = set(cell["band"]["characters"])
    out["band_well_formed"] = len(band) == len(cell["band"]["characters"]) and all(
        isinstance(xi, int) and 1 <= xi <= C - 1 for xi in band
    )

    classes = dense_tau_classes(C, stored_cols)
    if "ii" in clauses_imposed:
        lab = cell["band"]["level"]
        out["clause_ii_ok"] = (lab in classes) and (lab != "<1") and (classes[lab] == band)
    else:
        # ablated: band must still be an exact union of complete tau-classes
        # (the dense free-band family; '<1' allowed).
        covered = set()
        ok = True
        for lab, xis in classes.items():
            inter = band & xis
            if inter:
                if inter != xis:
                    ok = False
                    break
                covered |= xis
        out["clause_ii_ok"] = ok and (covered == band) and len(band) > 0

    mask_bits = list(cell["mask"]["bits"])
    out["mask_well_formed"] = (len(mask_bits) == M) and all(b in (0, 1) for b in mask_bits)

    if "iii" in clauses_imposed:
        out["clause_iii_ok"] = (mask_bits == dense_dedup_mask(supports, images))
    else:
        out["clause_iii_ok"] = True

    if "iv" in clauses_imposed and "iii" not in clauses_imposed:
        n_owner = 2 * B
        seen_owner_val: dict[int, int] = {}
        ok = True
        for idx, b in enumerate(mask_bits):
            o = idx % n_owner
            if o in seen_owner_val and seen_owner_val[o] != b:
                ok = False
                break
            seen_owner_val[o] = b
        out["clause_iv_ok"] = ok
    else:
        out["clause_iv_ok"] = True

    f: dict[int, int] = {}
    for idx, b in enumerate(mask_bits):
        if b:
            x = images[idx]
            f[x] = f.get(x, 0) + 1
    recomputed_gain = dense_gain(C, band, f, q)
    out["recomputed_gain"] = recomputed_gain
    out["gain_matches"] = close(recomputed_gain, cell["gain"])
    out["search_mode"] = cell["band"].get("search_mode") or cell["mask"].get("search_mode")
    return out


def recompute_717_row(B: int) -> dict:
    """Recompute PR #717 Section 7's table row facts for this B."""
    cols, C = dense_superincreasing_columns(B)
    supports = dense_supports(B)
    images = dense_images(supports, cols, C)
    M = len(supports)
    L_img = len(set(images))
    fiber = [supports[i] for i in range(M) if images[i] == 0]
    W = len(fiber)
    max_int = 0
    for i in range(W):
        for j in range(i + 1, W):
            inter = len(set(fiber[i]) & set(fiber[j]))
            max_int = max(max_int, inter)
    return {
        "B": B,
        "C": C,
        "M": M,
        "L_image": L_img,
        "L_image_formula": (3 ** B + 1) // 2,
        "W_fiber_at_0": W,
        "W_formula": math.comb(B, B // 2),
        "s0_int": B * C // 2,
        "s0_mod_C": (B * C // 2) % C,
        "max_fiber_pair_intersection": max_int,
        "johnson_bound_a_minus_2": B - 2,
    }


# ---------------------------------------------------------------------------
# Top-level validation (shared by the normal run and the tamper self-test).
# ---------------------------------------------------------------------------

def _mk_checker(verbose: bool):
    def c(name, cond, detail=""):
        if verbose:
            check(name, cond, detail)
        else:
            if not cond:
                raise AssertionError(f"{name} :: {detail}")
    return c


def validate_sparse_cells(cert: dict, c, only_p=None) -> dict:
    R = cert["params"]["R"]
    q = cert["params"]["q"]
    by_constraint: dict[str, list[tuple[int, float]]] = {}
    for cell in cert["cells"]:
        p = cell["p"]
        if only_p is not None and p != only_p:
            continue
        L = cell["L"]
        group = group_elements(p, R)
        c(f"cell {cell['constraint_set']} p={p}: L matches p^R", len(group) == L)
        out = recompute_cell(cell, group, p, R, L, q)
        tag = f"cell {cell['constraint_set']} p={p}"
        c(f"{tag}: columns match stored formula", out["columns_match_formula"])
        c(f"{tag}: clause i compliance", out["clause_i_ok"])
        c(f"{tag}: band well-formed", out["band_well_formed"])
        c(f"{tag}: clause ii compliance", out["clause_ii_ok"])
        c(f"{tag}: mask well-formed", out["mask_well_formed"])
        c(f"{tag}: clause iii compliance", out["clause_iii_ok"])
        c(f"{tag}: clause iv compliance", out["clause_iv_ok"])
        c(
            f"{tag}: gain recomputes to claimed value",
            out["gain_matches"],
            f"claimed={cell['gain']!r} recomputed={out['recomputed_gain']!r} mode={out['search_mode']}",
        )
        by_constraint.setdefault(cell["constraint_set"], []).append((L, out["recomputed_gain"]))
    if only_p is None:
        b_by_p = {cell["p"]: cell["gain"] for cell in cert["cells"] if cell["constraint_set"] == "B"}
        civ_by_p = {cell["p"]: cell["gain"] for cell in cert["cells"] if cell["constraint_set"] == "C_iv"}
        for p in b_by_p:
            c(
                f"structural identity: C_iv == B at p={p}",
                close(b_by_p[p], civ_by_p[p], tol=1e-9),
                f"B={b_by_p[p]!r} C_iv={civ_by_p[p]!r}",
            )
    return by_constraint


def validate_dense_cells(cert: dict, c, only_B=None) -> dict:
    q = cert["params"]["q"]
    by_constraint: dict[str, list[tuple[int, float]]] = {}
    for cell in cert["dense_cells"]:
        B = cell["B"]
        if only_B is not None and B != only_B:
            continue
        out = recompute_dense_cell(cell, q)
        tag = f"dense cell {cell['constraint_set']} B={B}"
        c(f"{tag}: C matches family formula", out["C_matches_family"])
        c(f"{tag}: M matches C(2B,B)", out["M_matches"])
        c(f"{tag}: columns match stored formula", out["columns_match_formula"])
        c(f"{tag}: clause i compliance", out["clause_i_ok"])
        c(f"{tag}: band well-formed", out["band_well_formed"])
        c(f"{tag}: clause ii compliance", out["clause_ii_ok"])
        c(f"{tag}: mask well-formed", out["mask_well_formed"])
        c(f"{tag}: clause iii compliance", out["clause_iii_ok"])
        c(f"{tag}: clause iv compliance", out["clause_iv_ok"])
        c(
            f"{tag}: gain recomputes to claimed value",
            out["gain_matches"],
            f"claimed={cell['gain']!r} recomputed={out['recomputed_gain']!r} mode={out['search_mode']}",
        )
        by_constraint.setdefault(cell["constraint_set"], []).append((cell["L"], out["recomputed_gain"]))
    if only_B is None:
        b_by = {cell["B"]: cell["gain"] for cell in cert["dense_cells"] if cell["constraint_set"] == "B"}
        civ_by = {cell["B"]: cell["gain"] for cell in cert["dense_cells"] if cell["constraint_set"] == "C_iv"}
        for B in b_by:
            c(
                f"dense structural identity: C_iv == B at B={B}",
                close(b_by[B], civ_by[B], tol=1e-9),
                f"B={b_by[B]!r} C_iv={civ_by[B]!r}",
            )
    return by_constraint


def validate_717_anchor(cert: dict, c) -> None:
    for row in cert["pr717_table_replication"]:
        B = row["B"]
        rec = recompute_717_row(B)
        tag = f"PR #717 Sec 7 row B={B}"
        c(f"{tag}: C recomputes", rec["C"] == row["C"], f"{rec['C']} vs {row['C']}")
        c(f"{tag}: M = C(2B,B) recomputes", rec["M"] == row["M"])
        c(
            f"{tag}: image size == (3^B+1)/2",
            rec["L_image"] == rec["L_image_formula"] == row["L_image"],
            f"observed={rec['L_image']} formula={rec['L_image_formula']}",
        )
        c(
            f"{tag}: fiber at 0 has W == C(B,B/2)",
            rec["W_fiber_at_0"] == rec["W_formula"] == row["W_fiber_at_0"],
        )
        c(f"{tag}: s0 = BC/2 == 0 mod C", rec["s0_mod_C"] == 0)
        c(
            f"{tag}: Johnson |S^S'| <= a-2 on the fiber",
            rec["max_fiber_pair_intersection"] <= rec["johnson_bound_a_minus_2"],
            f"max={rec['max_fiber_pair_intersection']} bound={rec['johnson_bound_a_minus_2']}",
        )


def validate_fits_block(fits: dict, by_constraint: dict, c, label: str,
                        use_recomputed: bool = True) -> None:
    for cs, fit in fits.items():
        if use_recomputed:
            stored_pairs = sorted(zip(fit["L"], fit["gain"]))
            recomputed_pairs = sorted(by_constraint[cs])
            c(
                f"{label} fit {cs}: table L/gain matches per-cell recomputation",
                all(
                    a[0] == b[0] and close(a[1], b[1], tol=1e-9)
                    for a, b in zip(stored_pairs, recomputed_pairs)
                ),
            )
        slope, intercept, r2 = recompute_fit(fit)
        c(
            f"{label} fit {cs}: slope recomputes ({slope:.4f})",
            close(slope, fit["slope"], tol=FIT_TOL) or abs(slope - fit["slope"]) < 1e-6,
        )
        c(f"{label} fit {cs}: intercept recomputes", close(intercept, fit["intercept"], tol=FIT_TOL))
        c(f"{label} fit {cs}: r2 recomputes", close(r2, fit["r2"], tol=FIT_TOL))


def validate(cert: dict, verbose: bool = True) -> None:
    c = _mk_checker(verbose)

    anchor = cert["anchor_replication"]
    anchor_gain = recompute_anchor(anchor)
    c(
        "anchor: PR #716 F_3^6 q=4 replica matches 1.1182491777",
        close(anchor_gain, anchor["claimed_normalized_q_gain"], tol=1e-9)
        and round(anchor_gain, 10) == round(1.1182491777, 10),
        f"recomputed={anchor_gain!r}",
    )

    validate_717_anchor(cert, c)

    by_sparse = validate_sparse_cells(cert, c)
    validate_fits_block(cert["fits"], by_sparse, c, "sparse")

    by_dense = validate_dense_cells(cert, c)
    validate_fits_block(cert["dense_fits"], by_dense, c, "dense")


def load_cert() -> dict:
    with open(CERT_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Tamper self-test.
# ---------------------------------------------------------------------------

def tamper_selftest() -> None:
    base = load_cert()
    validate(base, verbose=False)  # sanity: untampered cert must pass first

    # Each mutation carries a revalidation SCOPE so the self-test stays fast:
    # the scoped revalidation runs exactly the checks that must catch it.

    def mutate_gain(cert):
        cert["cells"][0]["gain"] += 0.05

    def mutate_mask_bit_dedup(cert):
        for cell in cert["cells"]:
            if "iii" in cell["clauses_imposed"] and cell["p"] == 3:
                bits = cell["mask"]["bits"]
                bits[0] = 1 - bits[0]
                return
        raise AssertionError("no clause-iii-imposed cell found to tamper")

    def mutate_column_swap(cert):
        for cell in cert["cells"]:
            if cell["columns_kind"] == "vandermonde" and cell["p"] == 3:
                cell["columns"]["0"] = [c + 1 for c in cell["columns"]["0"]]
                return
        raise AssertionError("no vandermonde cell found to tamper")

    def mutate_band_drop(cert):
        for cell in cert["cells"]:
            if "ii" in cell["clauses_imposed"] and cell["p"] == 3 and len(cell["band"]["characters"]) > 1:
                cell["band"]["characters"].pop()
                return
        raise AssertionError("no clause-ii-imposed cell found to tamper")

    def mutate_band_add_spurious(cert):
        # Add a character absent from a clause-ii-imposed cell's band (scan
        # the whole dual until one is found; some p=3 bands are near-full).
        R = cert["params"]["R"]
        for cell in cert["cells"]:
            if "ii" in cell["clauses_imposed"] and cell["p"] == 3:
                p = cell["p"]
                have = {tuple(x) for x in cell["band"]["characters"]}
                for cand in itertools.product(range(p), repeat=R):
                    if any(cand) and cand not in have:
                        cell["band"]["characters"].append(list(cand))
                        return
        raise AssertionError("no clause-ii-imposed cell found to tamper")

    def mutate_owner_violation(cert):
        for cell in cert["cells"]:
            if cell["constraint_set"] == "C_iii" and cell["p"] == 5:
                p = cell["p"]
                bits = cell["mask"]["bits"]
                owners = [idx % p for idx in range(len(bits))]
                for idx in range(1, len(bits)):
                    if owners[idx] == owners[0] and bits[idx] == bits[0]:
                        bits[idx] = 1 - bits[idx]
                        return
                for idx in range(1, len(bits)):
                    if owners[idx] == owners[0]:
                        bits[idx] = 1 - bits[0]
                        return
        raise AssertionError("no C_iii cell found to tamper")

    def mutate_fit_slope(cert):
        cert["fits"]["A"]["slope"] += 1.0

    def mutate_civ_breaks_identity(cert):
        for cell in cert["cells"]:
            if cell["constraint_set"] == "C_iv":
                cell["gain"] += 0.1
                return
        raise AssertionError("no C_iv cell found to tamper")

    # --- dense-arm mutations ---

    def mutate_dense_gain(cert):
        for cell in cert["dense_cells"]:
            if cell["B"] == 4:
                cell["gain"] += 0.05
                return
        raise AssertionError("no dense B=4 cell found")

    def mutate_dense_mask_dedup(cert):
        for cell in cert["dense_cells"]:
            if cell["B"] == 4 and "iii" in cell["clauses_imposed"]:
                cell["mask"]["bits"][0] = 1 - cell["mask"]["bits"][0]
                return
        raise AssertionError("no dense clause-iii cell found")

    def mutate_dense_columns(cert):
        for cell in cert["dense_cells"]:
            if cell["B"] == 2 and cell["columns_kind"] == "superincreasing":
                cell["columns"][0] += 1
                return
        raise AssertionError("no dense superincreasing cell found")

    def mutate_dense_band_break_class(cert):
        # remove one character from a dense clause-ii-imposed band
        for cell in cert["dense_cells"]:
            if cell["B"] == 4 and "ii" in cell["clauses_imposed"] and len(cell["band"]["characters"]) > 1:
                cell["band"]["characters"].pop()
                return
        raise AssertionError("no dense clause-ii cell found")

    def mutate_dense_owner_violation(cert):
        for cell in cert["dense_cells"]:
            if cell["constraint_set"] == "C_iii" and cell["B"] == 4:
                bits = cell["mask"]["bits"]
                n_owner = 2 * cell["B"]
                for idx in range(1, len(bits)):
                    if idx % n_owner == 0 % n_owner and bits[idx] == bits[0]:
                        bits[idx] = 1 - bits[idx]
                        return
                bits[n_owner] = 1 - bits[0]
                return
        raise AssertionError("no dense C_iii B=4 cell found")

    def mutate_dense_civ_identity(cert):
        for cell in cert["dense_cells"]:
            if cell["constraint_set"] == "C_iv":
                cell["gain"] += 0.1
                return
        raise AssertionError("no dense C_iv cell found")

    def mutate_dense_fit_slope(cert):
        cert["dense_fits"]["C_iii"]["slope"] -= 0.5

    def mutate_717_row(cert):
        cert["pr717_table_replication"][0]["W_fiber_at_0"] += 1

    # (name, mutate, scope) -- scope picks the cheapest revalidation that
    # must catch the mutation.
    mutations = [
        ("gain_value", mutate_gain, ("sparse", 3)),
        ("mask_bit_dedup", mutate_mask_bit_dedup, ("sparse", 3)),
        ("column_swap", mutate_column_swap, ("sparse", 3)),
        ("band_drop", mutate_band_drop, ("sparse", 3)),
        ("band_add_spurious", mutate_band_add_spurious, ("sparse", 3)),
        ("owner_violation", mutate_owner_violation, ("sparse", 5)),
        ("fit_slope", mutate_fit_slope, ("fits_sparse",)),
        ("civ_breaks_identity", mutate_civ_breaks_identity, ("identity_sparse",)),
        ("dense_gain", mutate_dense_gain, ("dense", 4)),
        ("dense_mask_dedup", mutate_dense_mask_dedup, ("dense", 4)),
        ("dense_columns", mutate_dense_columns, ("dense", 2)),
        ("dense_band_break_class", mutate_dense_band_break_class, ("dense", 4)),
        ("dense_owner_violation", mutate_dense_owner_violation, ("dense", 4)),
        ("dense_civ_identity", mutate_dense_civ_identity, ("identity_dense",)),
        ("dense_fit_slope", mutate_dense_fit_slope, ("fits_dense",)),
        ("pr717_row", mutate_717_row, ("anchor717",)),
    ]

    def scoped_validate(cert, scope):
        c = _mk_checker(verbose=False)
        kind = scope[0]
        if kind == "sparse":
            validate_sparse_cells(cert, c, only_p=scope[1])
        elif kind == "dense":
            validate_dense_cells(cert, c, only_B=scope[1])
        elif kind == "fits_sparse":
            # slope/intercept/r2 recomputation from the stored fit table
            validate_fits_block(cert["fits"], {}, c, "sparse", use_recomputed=False)
        elif kind == "fits_dense":
            validate_fits_block(cert["dense_fits"], {}, c, "dense", use_recomputed=False)
        elif kind == "identity_sparse":
            b_by = {cell["p"]: cell["gain"] for cell in cert["cells"] if cell["constraint_set"] == "B"}
            civ_by = {cell["p"]: cell["gain"] for cell in cert["cells"] if cell["constraint_set"] == "C_iv"}
            for p in b_by:
                if not close(b_by[p], civ_by[p], tol=1e-9):
                    raise AssertionError(f"identity C_iv==B broken at p={p}")
            # also fits-table consistency catches gain edits
            validate_fits_block(cert["fits"], {}, c, "sparse", use_recomputed=False)
            for cs, fit in cert["fits"].items():
                stored = {cell["p"]: cell["gain"] for cell in cert["cells"] if cell["constraint_set"] == cs}
                Lmap = dict(zip(fit["L"], fit["gain"]))
                for p, g in stored.items():
                    if not close(Lmap[p ** cert["params"]["R"]], g, tol=1e-9):
                        raise AssertionError(f"fit table vs cell gain mismatch {cs} p={p}")
        elif kind == "identity_dense":
            b_by = {cell["B"]: cell["gain"] for cell in cert["dense_cells"] if cell["constraint_set"] == "B"}
            civ_by = {cell["B"]: cell["gain"] for cell in cert["dense_cells"] if cell["constraint_set"] == "C_iv"}
            for B in b_by:
                if not close(b_by[B], civ_by[B], tol=1e-9):
                    raise AssertionError(f"dense identity C_iv==B broken at B={B}")
            for cs, fit in cert["dense_fits"].items():
                stored = {cell["C"]: cell["gain"] for cell in cert["dense_cells"] if cell["constraint_set"] == cs}
                Lmap = dict(zip(fit["L"], fit["gain"]))
                for C, g in stored.items():
                    if not close(Lmap[C], g, tol=1e-9):
                        raise AssertionError(f"dense fit table vs cell gain mismatch {cs} C={C}")
        elif kind == "anchor717":
            validate_717_anchor(cert, c)
        else:
            raise AssertionError(f"unknown scope {scope}")

    detected = 0
    for name, mutate, scope in mutations:
        bad = json.loads(json.dumps(base))
        mutate(bad)
        try:
            scoped_validate(bad, scope)
        except AssertionError:
            detected += 1
            print(f"[PASS] tamper-selftest detected: {name}")
            continue
        raise AssertionError(f"tamper self-test FAILED to detect mutation: {name}")

    print(f"tamper self-test passed: {detected}/{len(mutations)} mutations detected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        tamper_selftest()
        return

    cert = load_cert()
    validate(cert, verbose=True)

    print()
    print(f"{NCHECK} checks run, {len(FAILS)} failed")
    if FAILS:
        print("RESULT = FAIL")
        for name in FAILS:
            print(f"  - {name}")
        sys.exit(1)
    print("RESULT = PASS")


if __name__ == "__main__":
    main()
