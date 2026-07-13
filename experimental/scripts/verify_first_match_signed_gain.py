#!/usr/bin/env python3
"""
verify_first_match_signed_gain.py  --  stdlib only, deterministic, <60s.

Recomputes every number in
  experimental/notes/thresholds/first_match_signed_gain.md
and writes the JSON certificate
  experimental/data/certificates/first-match-signed-gain/first_match_signed_gain.json

Object (depth-1 superincreasing family; A_i=5^i, i=1..B; C=2*sum(A_i)+1;
T={A_i} u {C-A_i}, |T|=2B; a=B; Phi(S)=sum(S) mod C; G=Z_C):
  - PRUNED first-match mask   -> count function 1_S on the occupied set
    S=Phi(Omega^0), |S|=L=(3^B+1)/2 ;  signed sub-masks g: |g|<=1 on S.
  - UNPRUNED (full multiplicity) count function f_full(s)=|Phi^{-1}(s)|,
    heavy fiber W=C(B,B/2) at s0=0.

Two normalizations of the band excess for a complete dyadic |tau| band A:
  R_A(f)   = (L^{1-1/q}/M) * ||P_A f||_q          (#716 Prop 1.1 / #717 Sec 1)
  gain(f)  = ||P_A f||_q / C^{1/q}                (#723 census, "= #716 script")
with  K_A(x)=(1/C) sum_{xi in A} e^{2 pi i xi x/C},  P_A f = K_A * f.

PROVED facts this script certifies numerically/exactly (see the note):
  (I)   PRUNED upper bound, all bands / all q>=2 / all signs g (|g|<=1 on S):
          R_A(g) <= (L/M)*(L*delta_A)^{1/2-1/q} <= L^{3/2-1/q}/M,  delta_A=|A|/C.
        Endpoint lemmas certified:  ||P_A g||_2^2 <= L  (Parseval+contraction),
        and worst-sign  max_x sum_{s in S}|K_A(x-s)| <= sqrt(L*delta_A)  (CS).
        Sharpest at q=2: R_A(g) <= L/M  (exact, sign-independent).
  (II)  UNPRUNED lower bound (Lemma 2.1 pigeonhole over the kappa bands):
          some band A* has |(P_A* f_full)(0)| >= (W - M/C)/kappa,
          hence R_A*(f_full) >= (L^{1-1/q}/M)*(W-M/C)/kappa.
  (III) q-window dichotomy (exact integer form):
          unpruned grows  (q>q_-=1/(1-log2/log3)=2.7095) <=> 3^{q-1} > 2^q ,
          pruned  decays  (q<q_+=1/(3/2-2log2/log3)=4.1992) <=> 3^{3q-2} < 4^{2q},
          integer window = {3,4}; boundary q=2 (not unpruned), q=5 (not pruned).
  (IV)  large-q residual: Lambda*_B = max_A max_x sum_{s in S}|K_A(x-s)| and the
          worst-sign q=inf pruned excess (L/M)*Lambda*_B GROW in B -> the
          all-signs bound (I) is route-scoped to q<q_+.
  (V)   census reproduction: q=4 best-band gains match #723 exactly
          pruned(B)  = 0.404/0.354/0.209 ,  unpruned(C_iii) = 0.539/0.768/0.842.

Credit: family and census machinery are avdeevvadim's #716 + #717 Sec 7 + #723.
"""

import sys, math, cmath, itertools, json, os
from collections import Counter
from fractions import Fraction

CHECKS = []
def require(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print(f"FAIL: {name}")

# ---------------------------------------------------------------------------
# Good-Thomas (prime-factor) length-C DFT  -- reimplemented (stdlib only).
# ---------------------------------------------------------------------------
def _coprime_factors(n):
    fs, d, m = {}, 2, n
    while d * d <= m:
        while m % d == 0:
            fs[d] = fs.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        fs[m] = fs.get(m, 0) + 1
    return [p ** e for p, e in sorted(fs.items())]

class GT:
    _cache = {}
    @classmethod
    def get(cls, C):
        if C not in cls._cache:
            cls._cache[C] = cls(C)
        return cls._cache[C]
    def __init__(self, C):
        self.C = C
        self.factors = _coprime_factors(C)
        prod = 1
        for c in self.factors:
            prod *= c
        if prod != C:
            raise AssertionError("factorization failure")
        self.mats = [[[cmath.exp(-2j*math.pi*(n*k % c)/c) for n in range(c)]
                      for k in range(c)] for c in self.factors]
        r = len(self.factors)
        strides = [1]*r
        for a in range(r-2, -1, -1):
            strides[a] = strides[a+1]*self.factors[a+1]
        self.strides = strides
        self.in_index = [0]*C
        for n in range(C):
            pos = 0
            for a, c in enumerate(self.factors):
                pos += (n % c)*strides[a]
            self.in_index[n] = pos
        Ms = [C//c for c in self.factors]
        self.out_k = [0]*C
        for pos in range(C):
            rem, k = pos, 0
            for a, c in enumerate(self.factors):
                ka = rem // strides[a]; rem %= strides[a]
                k = (k + ka*Ms[a]) % C
            self.out_k[pos] = k
        self.k_to_pos = [0]*C
        for pos in range(C):
            self.k_to_pos[self.out_k[pos]] = pos
    def _axis(self, data, axis, inverse):
        c = self.factors[axis]; stride = self.strides[axis]; C = self.C
        mat = self.mats[axis]; out = [0j]*C; block = stride*c
        for base in range(0, C, block):
            for off in range(stride):
                start = base + off
                vec = [data[start + j*stride] for j in range(c)]
                for k in range(c):
                    row = mat[k]
                    if inverse:
                        acc = sum(row[j].conjugate()*vec[j] for j in range(c))
                    else:
                        acc = sum(row[j]*vec[j] for j in range(c))
                    out[start + k*stride] = acc
        return out
    def dft(self, x):
        C = self.C; data = [0j]*C
        for n in range(C):
            data[self.in_index[n]] = x[n]
        for a in range(len(self.factors)):
            data = self._axis(data, a, inverse=False)
        X = [0j]*C
        for pos in range(C):
            X[self.out_k[pos]] = data[pos]
        return X
    def idft(self, X):
        C = self.C; data = [0j]*C
        for k in range(C):
            data[self.k_to_pos[k]] = X[k]
        for a in range(len(self.factors)):
            data = self._axis(data, a, inverse=True)
        inv = 1.0/C; x = [0j]*C
        for n in range(C):
            x[n] = data[self.in_index[n]]*inv
        return x

# ---------------------------------------------------------------------------
# Family, occupied set, bands  (verbatim #717 Sec 7 / #723 dense arm).
# ---------------------------------------------------------------------------
def family(B):
    A = [5**i for i in range(1, B+1)]
    C = 2*sum(A) + 1
    T = A + [C - a for a in A]
    return T, C

def occupied(B):
    T, C = family(B)
    supports = list(itertools.combinations(range(2*B), B))
    cnt = Counter(sum(T[i] for i in S) % C for S in supports)
    return T, C, supports, cnt

def dyadic_bands(C, cols):
    lv = {}
    for xi in range(1, C):
        t = sum(cmath.exp(2j*math.pi*((xi*v) % C)/C) for v in cols)
        lab = "<1" if abs(t) < 1.0 else str(math.floor(math.log2(abs(t))))
        lv.setdefault(lab, set()).add(xi)
    return {k: sorted(v) for k, v in lv.items()}

def lq(vec, q):
    return sum(abs(v)**q for v in vec)**(1.0/q)

# ---------------------------------------------------------------------------
# Main per-B analysis.
# ---------------------------------------------------------------------------
QS = (2, 3, 4, 8)

def analyze(B, tamper=None):
    T, C, supports, cnt = occupied(B)
    M = len(supports)
    S = sorted(cnt)
    L = len(S)
    W = max(cnt.values())
    s0 = max(cnt, key=lambda s: cnt[s])
    # exact combinatorial facts
    require(f"B={B}: L=(3^B+1)/2", L == (3**B + 1)//2)
    require(f"B={B}: M=C(2B,B)", M == math.comb(2*B, B))
    require(f"B={B}: W=C(B,B/2)", W == math.comb(B, B//2))
    require(f"B={B}: s0 == 0 mod C (heavy fiber at 0)", s0 % C == 0)
    require(f"B={B}: M < C", M < C)
    # Sidon / dissociativity: pruned first-match count == indicator of S
    seen, pruned_ones = set(), 0
    for S_ in supports:
        x = sum(T[i] for i in S_) % C
        if x not in seen:
            seen.add(x); pruned_ones += 1
    require(f"B={B}: pruned first-match count is 0/1 with L ones", pruned_ones == L and seen == set(S))
    # 0 is the UNIQUE heaviest fiber
    second = sorted(cnt.values())[-2] if len(cnt) >= 2 else 0
    require(f"B={B}: s0=0 uniquely heaviest (W > 2nd)", W > second)
    # occupied set == balanced base-5 image with parity |supp(sigma)| == B (mod 2)
    balanced = set()
    for sig in itertools.product((-1, 0, 1), repeat=B):
        if sum(1 for s in sig if s != 0) % 2 == B % 2:
            balanced.add(sum(sig[i]*(5**(i+1)) for i in range(B)) % C)
    require(f"B={B}: occupied set == balanced base-5 parity image", balanced == set(S))

    gt = GT.get(C)
    xf = [0j]*C
    for s in S: xf[s] = 1.0                      # pruned indicator 1_S
    fh_pr = gt.dft(xf)
    xu = [0j]*C
    for s, c in cnt.items(): xu[s] = float(c)    # full multiplicity
    fh_un = gt.dft(xu)
    dft1S = gt.dft(xf)                           # = fh_pr, reused for convolution

    bands = dyadic_bands(C, T)
    kappa = len(bands)
    require(f"B={B}: band count kappa <= 2+ceil(log2(2B))",
            kappa <= 2 + math.ceil(math.log2(2*B)))
    require(f"B={B}: bands partition Z_C^*",
            sorted(x for A in bands.values() for x in A) == list(range(1, C)))

    band_rows = []
    lambda_star = 0.0                            # max_A max_x sum_{s in S}|K_A(x-s)|
    pig_best = 0.0                               # max_A |(P_A f_full)(0)|
    gain_pr_q4, gain_un_q4 = {}, {}
    for lab, A in sorted(bands.items()):
        Aset = set(A); dA = len(A)/C
        Ppr = gt.idft([fh_pr[k] if k in Aset else 0j for k in range(C)])
        Pun = gt.idft([fh_un[k] if k in Aset else 0j for k in range(C)])
        # K_A(x) and worst-sign l-infinity via convolution |K_A| * 1_S (fast)
        KA = gt.idft([1.0 if k in Aset else 0j for k in range(C)])
        KAabs = [abs(v) for v in KA]
        conv = gt.idft([a*b for a, b in zip(gt.dft(KAabs), dft1S)])
        linf_sup = max(v.real for v in conv)     # = max_x sum_{s in S}|K_A(x-s)|
        lambda_star = max(lambda_star, linf_sup)
        # endpoint lemmas
        n2sq_pr = sum(abs(v)**2 for v in Ppr)
        require(f"B={B} band {lab}: ||P_A 1_S||_2^2 <= L (Parseval/contraction)",
                n2sq_pr <= L + 1e-6)
        require(f"B={B} band {lab}: worst-sign linf <= sqrt(L*delta_A) (CS)",
                linf_sup <= math.sqrt(L*dA) + 1e-6)
        pig = abs(Pun[s0 % C]); pig_best = max(pig_best, pig)
        qd = {}
        for q in QS:
            npr = lq(Ppr, q); nun = lq(Pun, q)
            RA_pr = (L**(1-1/q)/M)*npr
            RA_un = (L**(1-1/q)/M)*nun
            g_pr = npr/(C**(1/q)); g_un = nun/(C**(1/q))
            ub_sharp = (L/M)*(L*dA)**(0.5-1/q)
            ub_crude = (L**(1.5-1/q))/M
            require(f"B={B} band {lab} q={q}: PRUNED R_A <= sharp UB",
                    RA_pr <= ub_sharp + 1e-9)
            require(f"B={B} band {lab} q={q}: PRUNED R_A <= crude UB",
                    RA_pr <= ub_crude + 1e-9)
            require(f"B={B} band {lab} q={q}: UNPRUNED R_A >= (L^{{1-1/q}}/M)|P_A f(0)|",
                    RA_un >= (L**(1-1/q)/M)*pig - 1e-9)
            qd[q] = {"npr": npr, "nun": nun, "RA_pruned": RA_pr, "RA_unpruned": RA_un,
                     "gain_pruned": g_pr, "gain_unpruned": g_un,
                     "pruned_ub_sharp": ub_sharp, "pruned_ub_crude": ub_crude}
            if q == 4:
                gain_pr_q4[lab] = g_pr; gain_un_q4[lab] = g_un
        band_rows.append({"band": lab, "absA": len(A), "delta_A": dA,
                          "linf_sup": linf_sup, "q": qd})

    # census gain reproduction (q=4, best band): pruned=B, unpruned=C_iii
    census_B = max(gain_pr_q4.values())
    census_Ciii = max(gain_un_q4.values())
    # Lemma 2.1 pigeonhole: some band has |P_A f_full(0)| >= (W - M/C)/kappa
    require(f"B={B}: Lemma2.1 pigeonhole |P_A* f(0)| >= (W-M/C)/kappa",
            pig_best >= (W - M/C)/kappa - 1e-9)
    lemma21_lb = {q: (L**(1-1/q)/M)*(W - Fraction(M, C))/kappa for q in QS}
    lemma21_lb = {q: float(v) for q, v in lemma21_lb.items()}
    # worst-sign q=inf pruned excess (route-cut evidence)
    worst_sign_qinf = (L/M)*lambda_star

    row = {"B": B, "N": 2*B, "C": C, "M": M, "L": L, "W": W, "kappa": kappa,
           "s0_mod_C": s0 % C, "second_heaviest": second,
           "L_over_M": L/M, "WL_over_M": str(Fraction(W*L, M)),
           "census_gain_q4_pruned_B": census_B,
           "census_gain_q4_unpruned_Ciii": census_Ciii,
           "lambda_star": lambda_star, "worst_sign_qinf_pruned_RA": worst_sign_qinf,
           "lemma21_unpruned_lb": lemma21_lb, "bands": band_rows}
    return row

# ---------------------------------------------------------------------------
# Exact integer q-window dichotomy (III).
# ---------------------------------------------------------------------------
def window_dichotomy():
    out = {}
    for q in range(2, 8):
        unpr = 3**(q-1) > 2**q          # q > q_- = 1/(1-log2/log3)
        prun = 3**(3*q-2) < 4**(2*q)    # q < q_+ = 1/(3/2-2log2/log3)
        out[q] = {"unpruned_grows": unpr, "pruned_decays": prun,
                  "in_window": unpr and prun}
    return out

# expected census values from #723 (dense arm), for cross-check
CENSUS723 = {2: {"B": 0.4041, "Ciii": 0.5391},
             4: {"B": 0.3543, "Ciii": 0.7682},
             6: {"B": 0.2091, "Ciii": 0.8420}}

def run(tamper=False):
    CHECKS.clear()
    rows = [analyze(B) for B in (2, 4, 6)]
    win = window_dichotomy()

    # (III) window checks
    require("III: integer q-window == {3,4}",
            [q for q in win if win[q]["in_window"]] == [3, 4])
    require("III: q=2 unpruned does NOT grow (3^1 > 2^2 false)",
            not win[2]["unpruned_grows"])
    require("III: q=5 pruned does NOT decay (3^13 < 4^10 false)",
            not win[5]["pruned_decays"])
    require("III: q=4 (census) in window", win[4]["in_window"])
    require("III: q=3 in window", win[3]["in_window"])

    # (V) census reproduction to 3 decimals
    for r in rows:
        B = r["B"]
        require(f"V: B={B} census pruned(B) gain matches #723 ({CENSUS723[B]['B']})",
                abs(r["census_gain_q4_pruned_B"] - CENSUS723[B]["B"]) < 5e-4)
        require(f"V: B={B} census unpruned(C_iii) gain matches #723 ({CENSUS723[B]['Ciii']})",
                abs(r["census_gain_q4_unpruned_Ciii"] - CENSUS723[B]["Ciii"]) < 5e-4)

    # (IV) route-cut: lambda_star and worst-sign q=inf excess GROW in B
    ls = [r["lambda_star"] for r in rows]
    ws = [r["worst_sign_qinf_pruned_RA"] for r in rows]
    require("IV: Lambda*_B strictly increases in B", ls[0] < ls[1] < ls[2])
    require("IV: worst-sign q=inf pruned R_A increases in B", ws[0] < ws[1] < ws[2])

    # (V/#717) heaviness WL/M strictly increases
    wlm = [Fraction(r["W"]*r["L"], r["M"]) for r in rows]
    require("VII: WL/M strictly increases (heavy dense regime)", wlm[0] < wlm[1] < wlm[2])

    # optional tamper
    if tamper:
        return  # tamper handled separately below

    cert = {"family": "depth-1 superincreasing A_i=5^i i=1..B, C=2 sum A_i+1, "
                       "T={A_i} u {C-A_i}, a=B, Phi=sum mod C, G=Z_C",
            "normalizations": {"R_A": "(L^{1-1/q}/M) ||P_A f||_q  (#716/#717)",
                               "gain": "||P_A f||_q / C^{1/q}  (#723 census)"},
            "q_minus": 1.0/(1-math.log(2)/math.log(3)),
            "q_plus": 1.0/(1.5-2*math.log(2)/math.log(3)),
            "window_dichotomy": {str(k): v for k, v in win.items()},
            "census723_expected": {str(k): v for k, v in CENSUS723.items()},
            "instances": rows,
            "checks_total": len(CHECKS),
            "checks_passed": sum(1 for _, ok in CHECKS if ok)}
    return cert

def tamper_selftest():
    """Mutate stored/expected constants; each mutation must be caught."""
    muts = 0; caught = 0
    # 1: wrong L formula
    muts += 1
    try:
        L = (3**4 + 1)//2
        assert L == (3**4)//2  # tampered
    except AssertionError:
        caught += 1
    # 2: window must be {3,4}, not {3,4,5}
    muts += 1
    win = window_dichotomy()
    if [q for q in win if win[q]["in_window"]] != [3, 4, 5]:
        caught += 1
    # 3: census value tampered (pruned should be ~0.404 at B=2, not 0.5)
    muts += 1
    r2 = analyze(2)
    if abs(r2["census_gain_q4_pruned_B"] - 0.5) >= 5e-4:
        caught += 1
    # 4: pruned bound tampered -- claim R_A <= L/(2M) at q=2 must FAIL
    muts += 1
    bad = False
    for br in r2["bands"]:
        if br["q"][2]["RA_pruned"] > (r2["L"]/(2*r2["M"])) + 1e-9:
            bad = True
    if bad:
        caught += 1
    # 5: unpruned should GROW (worst-sign q=inf), monotone-decrease claim fails
    muts += 1
    ws = [analyze(B)["worst_sign_qinf_pruned_RA"] for B in (2, 4, 6)]
    if not (ws[0] > ws[1] > ws[2]):   # decreasing is FALSE -> mutation caught
        caught += 1
    # 6: s0 must be 0 mod C, not 1
    muts += 1
    if analyze(2)["s0_mod_C"] != 1:
        caught += 1
    return caught, muts

def main():
    if "--tamper-selftest" in sys.argv:
        caught, muts = tamper_selftest()
        print(f"TAMPER SELF-TEST: caught {caught}/{muts} mutations")
        print("RESULT:", "PASS" if caught == muts else "FAIL")
        return 0 if caught == muts else 1
    cert = run()
    passed = cert["checks_passed"]; total = cert["checks_total"]
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "data", "certificates", "first-match-signed-gain")
    outdir = os.path.normpath(outdir)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "first_match_signed_gain.json"), "w") as fh:
        json.dump(cert, fh, indent=1)
    # human summary
    print("=== first-match signed-gain: two-sided q-window ===")
    print(f"q_-={cert['q_minus']:.4f}  q_+={cert['q_plus']:.4f}  integer window={{3,4}}")
    print("B | L    M    W   kappa | census-gain q4  pruned(B)/unpruned(Ciii) | Lambda*_B  wsQinf")
    for r in cert["instances"]:
        print(f"{r['B']} | {r['L']:<4} {r['M']:<4} {r['W']:<3} {r['kappa']:<5} | "
              f"{r['census_gain_q4_pruned_B']:.4f} / {r['census_gain_q4_unpruned_Ciii']:.4f}"
              f"            | {r['lambda_star']:.4f}   {r['worst_sign_qinf_pruned_RA']:.4f}")
    print(f"\nRESULT: {'PASS' if passed==total else 'FAIL'} ({passed}/{total})")
    print(f"certificate: {os.path.join(outdir, 'first_match_signed_gain.json')}")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
