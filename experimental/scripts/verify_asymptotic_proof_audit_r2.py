#!/usr/bin/env python3
"""Verifier for the asymptotic RS-MCA in-paper PROOF audit (round 2).

Zero-arg, stdlib-only. Gates the machine-readable attack->verdict map in
experimental/data/asymptotic_rs_mca_proof_audit_r2.json against the paper and
the two in-tree source ledgers, AND re-runs every numeric check the audit
relies on.

Unlike the citation verifier (#433, verify_asymptotic_ledger_audit.py) this one
attacks the paper's OWN proofs: besides byte-matching the located quotes within
+/-5 lines and checking the four-way verdict tally, it independently recomputes
  - the first-match disjointization toy (A1),
  - the moment-max inequalities and q-th-root squeeze (A2),
  - the sigma block-diagonal constructibility (A3),
  - the BSG(K=e^{o(N)}) + quasicube contradiction arithmetic (A4),
  - the pole-line polynomial division over F_p (A9 algebra),
  - the Stirling exponent and g*(rho,beta) crossing table (A10),
and it runs >=5 tamper self-tests. It does NOT re-prove the imported ledger, BSG,
or the quasicube theorem.

Knobs (environment variables):
  PAUD_AS_CAP_GB  address-space cap in GB via RLIMIT_AS (default 2).
  PAUD_DATA_DIR   repo root holding experimental/ (default: two dirs up).

Exit 0 and print 'RESULT: PASS' on success; exit 1 on any failure.
"""

import copy
import itertools
import json
import math
import os
import resource
import sys

VICINITY = 5
FOURWAY = ("NO_ISSUE", "FIXED", "OPEN_GAP", "COUNTEREXAMPLE_NEW_FLOOR")
MIN_QUOTES = 20


# ---- environment ---------------------------------------------------------

def cap_memory():
    try:
        gb = float(os.environ.get("PAUD_AS_CAP_GB", "2"))
    except ValueError:
        gb = 2.0
    nbytes = int(gb * (1024 ** 3))
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        newhard = hard if hard != resource.RLIM_INFINITY and hard < nbytes else nbytes
        resource.setrlimit(resource.RLIMIT_AS, (nbytes, newhard))
    except (ValueError, OSError):
        pass


def repo_root():
    env = os.environ.get("PAUD_DATA_DIR")
    if env:
        return os.path.abspath(env)
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))  # experimental/scripts -> root


_FILE_CACHE = {}


def read_lines(path):
    if path not in _FILE_CACHE:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            _FILE_CACHE[path] = fh.read().splitlines()
    return _FILE_CACHE[path]


def quote_near(root, relpath, line, quote):
    path = os.path.join(root, relpath)
    if not os.path.isfile(path):
        return False
    lines = read_lines(path)
    lo = max(0, line - 1 - VICINITY)
    hi = min(len(lines), line - 1 + VICINITY + 1)
    return quote in "\n".join(lines[lo:hi])


def iter_quotes(data):
    for atk in data["attacks"]:
        for qd in atk.get("quotes", []):
            yield (qd["file"], qd["line"], qd["quote"], atk["id"])


# ---- prime-field polynomial arithmetic (A9) ------------------------------

def _norm(a, p):
    a = [x % p for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _padd(a, b, p):
    n = max(len(a), len(b))
    r = [0] * n
    for i in range(len(a)):
        r[i] = (r[i] + a[i]) % p
    for i in range(len(b)):
        r[i] = (r[i] + b[i]) % p
    return _norm(r, p)


def _psub(a, b, p):
    return _padd(a, [(-x) % p for x in b], p)


def _pmul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return _norm(r, p)


def _peval(a, x, p):
    acc = 0
    for c in reversed(a):
        acc = (acc * x + c) % p
    return acc % p


def _deg(a):
    a = _norm(a, 1 << 61)
    return len(a) - 1 if any(a) else -1


def _from_roots(roots, p):
    r = [1]
    for t in roots:
        r = _pmul(r, [(-t) % p, 1], p)
    return r


def _div_linear(a, alpha, p):
    """a(X) / (X - alpha): synthetic division -> (quotient, remainder)."""
    n = len(a)
    b = [0] * n
    b[n - 1] = a[n - 1] % p
    for i in range(n - 2, -1, -1):
        b[i] = (a[i] + alpha * b[i + 1]) % p
    return _norm(b[1:], p), b[0] % p


def _lagrange(points, p):
    result = [0]
    for i, (xi, yi) in enumerate(points):
        num = [1]
        den = 1
        for j, (xj, _) in enumerate(points):
            if i != j:
                num = _pmul(num, [(-xj) % p, 1], p)
                den = (den * ((xi - xj) % p)) % p
        inv = pow(den, p - 2, p)
        result = _padd(result, [((c * yi) % p) * inv % p for c in num], p)
    return _norm(result, p)


def pole_line_instance(inst):
    """Recompute the A9 algebra; return (zeta_star, deg_h) or raise AssertionError."""
    p, D, S, alpha, k = inst["p"], inst["D"], inst["S"], inst["alpha"], inst["k"]
    m = len(S)
    w = m - k - 1
    assert alpha not in D and set(S) <= set(D) and m == k + 1 + w
    ellS = _from_roots(S, p)
    assert _deg(ellS) == m and ellS[-1] == 1
    Uz = [0] * (m + 1)
    Uz[m] = 1
    for i in range(1, w + 1):          # share top w coeffs below the lead (the prefix z)
        Uz[m - i] = ellS[m - i]
    diff = _psub(Uz, ellS, p)
    assert _deg(diff) <= m - w - 1 == k          # shared top w+1 coeffs
    Ua, La = _peval(Uz, alpha, p), _peval(ellS, alpha, p)
    numer = _psub(diff, [(Ua - La) % p], p)
    assert _peval(numer, alpha, p) == 0
    h, rem = _div_linear(numer, alpha, p)
    assert rem == 0 and _deg(h) < k              # explaining poly has degree < k
    zeta_star = (Ua - La) % p
    inv = lambda x: pow((x - alpha) % p, p - 2, p)
    line_val = lambda x, z: ((_peval(Uz, x, p) - z) % p) * inv(x) % p
    for x in S:                                   # h explains the line on S at zeta*
        assert line_val(x, zeta_star) == _peval(h, x, p)
    # "exactly when": interpolant of line values on S has degree < k iff zeta == zeta*
    for zeta in range(p):
        P = _lagrange([(x, line_val(x, zeta)) for x in S], p)
        if zeta == zeta_star:
            assert _deg(P) < k
        else:
            assert _deg(P) >= k
    # g_alpha = -1/(x-alpha) not explained by degree-<k on any k+1 positions
    checked = 0
    for T in itertools.combinations(sorted(D), k + 1):
        P = _lagrange([(x, (-inv(x)) % p) for x in T], p)
        assert _deg(P) >= k
        checked += 1
        if checked >= 6:
            break
    return zeta_star, _deg(h)


# ---- entropy / Stirling (A10) --------------------------------------------

def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


def phi(g, rho, beta):
    return H2(rho + g) - beta * g


def gstar(rho, beta):
    hi = 1 - rho
    if phi(hi, rho, beta) >= 0:
        return hi
    lo = 0.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if phi(mid, rho, beta) >= 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def stirling_exp_over_n(rho, g, beta, n):
    a = round((rho + g) * n)
    kk = round(rho * n)
    w = a - kk - 1
    if a <= 0 or a >= n:
        return None
    log2binom = (math.lgamma(n + 1) - math.lgamma(a + 1) - math.lgamma(n - a + 1)) / math.log(2.0)
    return (log2binom - w * beta) / n


# ---- gates ---------------------------------------------------------------

def gate_files(data, root):
    fails = []
    declared = set(data["sources"].values())
    for key, rel in data["sources"].items():
        if not os.path.isfile(os.path.join(root, rel)):
            fails.append("declared source '%s' missing: %s" % (key, rel))
    for f, l, q, aid in iter_quotes(data):
        if not os.path.isfile(os.path.join(root, f)):
            fails.append("cited file missing (%s): %s" % (aid, f))
        elif f not in declared:
            fails.append("cited file not a declared source (%s): %s" % (aid, f))
    return fails


def gate_quotes(data, root):
    fails = []
    n = 0
    for f, l, q, aid in iter_quotes(data):
        n += 1
        if not quote_near(root, f, l, q):
            fails.append("quote not within +/-%d of %s:%d (%s): %r"
                         % (VICINITY, f, l, aid, q[:60]))
    if n < MIN_QUOTES:
        fails.append("too few located quotes checked (%d < %d)" % (n, MIN_QUOTES))
    return fails


def gate_totals(data):
    fails = []
    tally = {v: 0 for v in FOURWAY}
    ids = set()
    for atk in data["attacks"]:
        v = atk["verdict"]
        ids.add(atk["id"])
        if v not in tally:
            fails.append("attack %s verdict not in 4-way scheme: %s" % (atk["id"], v))
        else:
            tally[v] += 1
    if len(data["attacks"]) != 10 or len(ids) != 10:
        fails.append("expected exactly 10 distinct attacks, got %d (ids=%d)"
                     % (len(data["attacks"]), len(ids)))
    declared = data["verdict_totals"]
    for v in FOURWAY:
        if tally[v] != declared.get(v):
            fails.append("verdict total mismatch %s: computed %d, declared %s"
                         % (v, tally[v], declared.get(v)))
    # every OPEN_GAP attack must name a missing statement
    for atk in data["attacks"]:
        if atk["verdict"] == "OPEN_GAP" and not atk.get("missing_statement"):
            fails.append("OPEN_GAP attack %s has no missing_statement" % atk["id"])
    if len(data.get("open_gaps", [])) != declared.get("OPEN_GAP"):
        fails.append("open_gaps list length %d != OPEN_GAP total %d"
                     % (len(data.get("open_gaps", [])), declared.get("OPEN_GAP")))
    return fails


def gate_toy(data):
    """A1: recompute first-match classes from the incidence; sums must match."""
    fails = []
    t = data["numeric_checks"]["toy_first_match"]
    inc = {g: set(cells) for g, cells in t["incidence"].items()}
    fm = {g: min(cells) for g, cells in inc.items()}
    classes = {}
    for g, j in fm.items():
        classes.setdefault(j, []).append(g)
    fm_budget = {j: len(v) for j, v in classes.items()}
    total = len(inc)
    raw = {j: len([g for g in inc if j in inc[g]]) for j in set().union(*inc.values())}
    if sum(fm_budget.values()) != total:
        fails.append("first-match budgets do not sum to total: %d != %d"
                     % (sum(fm_budget.values()), total))
    if total != t["expected_total_slopes"] or sum(fm_budget.values()) != t["expected_firstmatch_sum"]:
        fails.append("toy totals mismatch JSON: total=%d firstmatch=%d"
                     % (total, sum(fm_budget.values())))
    if sum(raw.values()) != t["expected_raw_projection_sum"]:
        fails.append("raw projection sum mismatch: %d != %d"
                     % (sum(raw.values()), t["expected_raw_projection_sum"]))
    if sum(raw.values()) < total:
        fails.append("raw projection sum below total (not an upper bound)")
    # projection-minus-earlier == first-match class
    for j in classes:
        proj = {g for g in inc if j in inc[g]}
        earlier = {g for g in inc if any(i < j for i in inc[g])}
        if (proj - earlier) != set(classes[j]):
            fails.append("projection-minus-earlier != first-match class at j=%s" % j)
    exp_b = {int(k): v for k, v in t["expected_first_match_budgets"].items()}
    if fm_budget != exp_b:
        fails.append("first-match budgets mismatch JSON: %s != %s" % (fm_budget, exp_b))
    return fails


def gate_moment_max(data):
    """A2: both inequalities + squeeze on the JSON profiles."""
    fails = []
    mm = data["numeric_checks"]["moment_max"]
    for prof in mm["profiles"]:
        L = len(prof)
        M = sum(prof)
        Nbar = M / L
        R = max(prof) / Nbar
        for q in mm["q_values"]:
            G = (1.0 / L) * sum((f / Nbar) ** q for f in prof)
            lo = (1.0 / L) * R ** q
            hi = R ** q
            if not (lo - 1e-9 <= G <= hi + 1e-9):
                fails.append("moment-max inequality violated prof=%s q=%s" % (prof, q))
        if abs((1.0 / L) * sum((f / Nbar) for f in prof) - 1.0) > 1e-9:
            fails.append("Gamma_1 != 1 for prof=%s" % prof)
        Gq = (1.0 / L) * sum((f / Nbar) ** 40 for f in prof)
        if not (R * L ** (-1.0 / 40) - 1e-9 <= Gq ** (1.0 / 40) <= R + 1e-9):
            fails.append("q-th-root not squeezed to R for prof=%s" % prof)
    return fails


def gate_sigma_block(data):
    """A3: the block-diagonal makes a(sigma_N,N)->0 and sigma_N->0 on an
    adversarially non-uniform per-sigma-null rate a=C/(sigma*sqrt(N))."""
    fails = []
    sb = data["numeric_checks"]["sigma_block_diagonal"]
    C = sb["C"]
    a_rate = lambda s, N: C / (s * math.sqrt(N))
    # per-sigma null (fixed sigma -> 0 as N grows)
    for sigma in (0.5, 0.1, 0.01):
        seq = [a_rate(sigma, 10 ** e) for e in (6, 10, 14, 18)]
        if not all(seq[i] > seq[i + 1] for i in range(len(seq) - 1)) or seq[-1] >= 1e-3:
            fails.append("per-sigma null fails at sigma=%s" % sigma)
    # non-uniform: small-sigma tail stays large
    if not a_rate(1e-6, 10 ** 6) > 1.0:
        fails.append("rate is unexpectedly uniform in sigma")

    def sigma_block(N):
        k = 1
        while (C * (k + 1) ** 2) ** 2 <= N:
            k += 1
        return 1.0 / k

    for N in sb["N_values"]:
        s = sigma_block(N)
        k = round(1.0 / s)
        if (C * k ** 2) ** 2 > N:
            fails.append("block seam invalid at N=%s" % N)
        if a_rate(s, N) > 1.0 / k + 1e-12:
            fails.append("diagonal rate not null at N=%s" % N)
        if not (0 < s <= 1.0):
            fails.append("sigma_N out of (0,1] at N=%s" % N)
    return fails


def gate_bsg(data):
    """A4: BSG(K=e^{o(N)}) + quasicube contradiction arithmetic."""
    fails = []
    b = data["numeric_checks"]["bsg_quasicube"]
    C, c = b["C_abs"], b["c"]
    if not c > 0:
        fails.append("c must be > 0")
    for N in b["N_values"]:
        oN = math.sqrt(N) * math.log(N)
        if oN / N >= 1e-2:
            fails.append("oN not small vs N at N=%s" % N)
        log_Fp = c * N - oN - C * oN               # survives K^{-C}
        if log_Fp < c * N - (1 + C) * oN - 1e-6:
            fails.append("|F'| does not survive K^{-C} at N=%s" % N)
        log_diff_upper = C * oN + log_Fp           # BSG K^{+C}
        log_diff_lower = 1.5 * log_Fp              # quasicube
        if not (log_diff_lower > log_diff_upper):  # incompatible -> contradiction
            fails.append("quasicube lower does not exceed BSG upper at N=%s" % N)
        if not (0.5 * log_Fp > C * oN):
            fails.append("0.5 log|F'| > C*o(N) fails at N=%s" % N)
        if not (c * N > (1 + 3 * C) * oN):
            fails.append("cN <= (1+3C)o(N) not contradicted at N=%s" % N)
    return fails


def gate_pole_line(data):
    """A9 algebra: recompute over F_p; zeta_star and deg_h must match JSON."""
    fails = []
    pl = data["numeric_checks"]["pole_line"]
    for inst in pl["instances"]:
        try:
            zeta_star, deg_h = pole_line_instance(inst)
        except AssertionError as e:
            fails.append("pole-line algebra failed for %s: %r" % (inst, e))
            continue
        if zeta_star != inst["expected_zeta_star"]:
            fails.append("zeta_star mismatch %s: %d != %d"
                         % (inst, zeta_star, inst["expected_zeta_star"]))
        if deg_h != inst["expected_deg_h"]:
            fails.append("deg_h mismatch %s: %d != %d"
                         % (inst, deg_h, inst["expected_deg_h"]))
        if not deg_h < inst["k"]:
            fails.append("deg_h not < k for %s" % inst)
    return fails


def gate_stirling(data):
    """A10: recompute g*, single-crossing, delta*, and Stirling exponent -> phi."""
    fails = []
    sg = data["numeric_checks"]["stirling_gstar"]
    for row in sg["table"]:
        rho, beta = row["rho"], row["beta"]
        gs = gstar(rho, beta)
        if abs(gs - row["expected_gstar"]) > 1e-5:
            fails.append("g* mismatch rho=%s beta=%s: %.6f != %.6f"
                         % (rho, beta, gs, row["expected_gstar"]))
        delta = 1 - rho - gs
        if abs(delta - row["expected_delta_star"]) > 1e-5:
            fails.append("delta* mismatch rho=%s beta=%s: %.6f != %.6f"
                         % (rho, beta, delta, row["expected_delta_star"]))
        boundary = abs(gs - (1 - rho)) < 1e-9
        if not boundary and abs(phi(gs, rho, beta)) > 1e-6:
            fails.append("phi(g*) not ~0 rho=%s beta=%s: %.2e" % (rho, beta, phi(gs, rho, beta)))
        if not boundary:
            for t in (0.2, 0.5, 0.8):
                if phi(gs * t, rho, beta) <= -1e-9:
                    fails.append("phi not >0 below g* rho=%s beta=%s" % (rho, beta))
            for t in (1.05, 1.3):
                gg = gs * t
                if gg < 1 - rho and phi(gg, rho, beta) >= 1e-9:
                    fails.append("phi not <0 above g* rho=%s beta=%s" % (rho, beta))
        # Stirling exponent converges to phi(g) at an interior g
        gtest = gs * 0.6 if gs > 0 else 0.1
        target = phi(gtest, rho, beta)
        vals = [stirling_exp_over_n(rho, gtest, beta, n) for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6)]
        errs = [abs(v - target) for v in vals if v is not None]
        if not (errs and errs[-1] < errs[0] and errs[-1] < 5e-3):
            fails.append("Stirling exponent does not converge to phi rho=%s beta=%s errs=%s"
                         % (rho, beta, errs))
    return fails


# ---- tamper self-tests ---------------------------------------------------

def tamper_tests(data, root):
    problems = []

    def expect_reject(name, gate_fn, mutated, *args):
        if not gate_fn(mutated, *args):
            problems.append("tamper '%s' NOT rejected (gate accepted corrupt data)" % name)

    # 1. corrupted quote
    d = copy.deepcopy(data)
    d["attacks"][0]["quotes"][0]["quote"] += "_XYZZY"
    expect_reject("corrupted-quote", gate_quotes, d, root)

    # 2. wrong line number
    d = copy.deepcopy(data)
    d["attacks"][3]["quotes"][0]["line"] += 200
    expect_reject("wrong-line", gate_quotes, d, root)

    # 3. mangled verdict total
    d = copy.deepcopy(data)
    d["verdict_totals"]["NO_ISSUE"] += 1
    expect_reject("mangled-total", gate_totals, d)

    # 4. bad verdict vocabulary
    d = copy.deepcopy(data)
    d["attacks"][1]["verdict"] = "PROBABLY_FINE"
    expect_reject("bad-verdict-vocab", gate_totals, d)

    # 5. missing source file
    d = copy.deepcopy(data)
    d["attacks"][0]["quotes"][0]["file"] = "experimental/does_not_exist.tex"
    expect_reject("missing-source", gate_files, d, root)

    # 6. wrong g* value
    d = copy.deepcopy(data)
    d["numeric_checks"]["stirling_gstar"]["table"][0]["expected_gstar"] = 0.9
    expect_reject("wrong-gstar", gate_stirling, d)

    # 7. broken toy count
    d = copy.deepcopy(data)
    d["numeric_checks"]["toy_first_match"]["expected_firstmatch_sum"] = 99
    expect_reject("broken-toy-count", gate_toy, d)

    # 8. wrong pole-line zeta_star
    d = copy.deepcopy(data)
    d["numeric_checks"]["pole_line"]["instances"][0]["expected_zeta_star"] = 0
    expect_reject("wrong-poleline-zeta", gate_pole_line, d)

    # 9. OPEN_GAP without missing_statement
    d = copy.deepcopy(data)
    for atk in d["attacks"]:
        if atk["verdict"] == "OPEN_GAP":
            atk["missing_statement"] = ""
            break
    expect_reject("open-gap-unnamed", gate_totals, d)

    return problems, 9


# ---- driver --------------------------------------------------------------

def main():
    cap_memory()
    root = repo_root()
    data_path = os.path.join(root, "experimental", "data",
                             "asymptotic_rs_mca_proof_audit_r2.json")
    if not os.path.isfile(data_path):
        print("RESULT: FAIL\n  data file not found: %s" % data_path)
        return 1
    with open(data_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    gates = [
        ("a  cited source files exist", gate_files(data, root)),
        ("bc quotes byte-match at +/-%d lines" % VICINITY, gate_quotes(data, root)),
        ("d  verdict tally self-consistent (8/0/2/0)", gate_totals(data)),
        ("e  A1 first-match disjointization toy recomputes", gate_toy(data)),
        ("f  A2 moment-max inequalities + squeeze", gate_moment_max(data)),
        ("g  A3 sigma block-diagonal constructible", gate_sigma_block(data)),
        ("h  A4 BSG(K=e^{o(N)})+quasicube contradiction", gate_bsg(data)),
        ("i  A9 pole-line polynomial division over F_p", gate_pole_line(data)),
        ("j  A10 Stirling exponent + g* crossing table", gate_stirling(data)),
    ]
    tampers, n_tampers = tamper_tests(data, root)

    ok = True
    print("asymptotic-proof-audit-r2 verifier")
    print("  root: %s" % root)
    for name, fails in gates:
        print("  [%s] gate %s" % ("PASS" if not fails else "FAIL", name))
        for f in fails:
            ok = False
            print("        - %s" % f)
    print("  [%s] %d tamper self-tests (negative controls)"
          % ("PASS" if not tampers else "FAIL", n_tampers))
    for t in tampers:
        ok = False
        print("        - %s" % t)

    n_quotes = sum(1 for _ in iter_quotes(data))
    print("  checked: %d located quotes, %d attacks, %d tamper tests"
          % (n_quotes, len(data["attacks"]), n_tampers))
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
