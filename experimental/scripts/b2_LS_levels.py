from math import log2, comb, lgamma, log
# deployed cascade: level l has n_l=2^(21-l), w_l=floor(w/2^l), subgroup mu_{n_l} in F_p, p~2^31
a=21; w=67471; log2p=31.0
sqrtp_log2=log2p/2   # log2 sqrt(p) ~ 15.5
print(f"Deployed cascade (p~2^{log2p:.0f}, sqrt(p)~2^{sqrtp_log2:.1f}).  Which levels are the HARD sub-sqrt(p) regime?\n")
print(f"{'l':>3} {'n_l=2^':>7} {'w_l':>7} {'gamma_l':>8} {'regime':>16} {'b_l(mult)':>10} {'Weil w_l*sqrtp vs n_l':>22}")
print("-"*80)
L=0; wl=w
while wl>0:
    l=L
    nlog2=a-l
    nl=2**nlog2
    gamma_l = nlog2/log2p          # log_p(n_l)
    b_l=2**l
    # subgroup regime: large if n_l> sqrt(p) i.e. nlog2>15.5
    regime = "LARGE (n>sqrt p)" if nlog2> sqrtp_log2 else "sub-sqrt(p) HARD"
    weil = wl*(2**sqrtp_log2)      # w_l * sqrt p (per-freq Weil bound scale)
    weil_vs = f"2^{log2(weil):.1f} vs 2^{nlog2}"
    tag = " <= Weil trivial" if weil>nl else ""
    print(f"{l:>3} {nlog2:>7} {wl:>7} {gamma_l:>8.3f} {regime:>16} {b_l:>10} {weil_vs:>22}{tag}")
    wl//=2; L+=1
print(f"\nTotal levels L={L}. Every level: w_l*sqrt(p) >> n_l => per-frequency Weil is TRIVIAL at all levels")
print("(sub-sqrt-p barrier is present throughout, worst at the large-subgroup ROOT where cancellation")
print("must beat the Weil floor). The irreducible core of (LS) = the signed minor-arc cancellation at")
print("the LARGE-subgroup levels l<=5 (n_l>sqrt p); levels l>=6 are small subgroups (BGK regime).")
