# Mersenne reciprocal-gap rigidity: at p == -1 mod n, every t-null block of size b <= 2t+1 has BINOMIAL
# locator X^b + q0 (hence is a mu_b-coset, b | n). Exhaustive check at two rows, all sizes b in [t+1, 8].
from itertools import combinations
R = None
for p, n, t in [(31, 16, 2), (127, 16, 2)]:
    F = GF(p^2, 'a')
    g = F.multiplicative_generator()
    z = g^((p^2 - 1)//n)
    assert z.multiplicative_order() == n
    pts = [z^k for k in range(n)]
    PR = PolynomialRing(F, 'X'); Xv = PR.gen()
    print(f"row (p={p} == -1 mod {n}, t={t}):")
    for b in range(t+1, 9):
        blocks = []
        for B in combinations(pts, b):
            if all(sum(x^j for x in B) == 0 for j in range(1, t+1)):
                blocks.append(B)
        binom = coset = prim = 0
        for B in blocks:
            L = prod(Xv - x for x in B)
            cf = L.coefficients(sparse=False)  # ascending
            is_binom = all(cf[k] == 0 for k in range(1, b))
            binom += is_binom
            # coset test: rotation stabilizer nontrivial
            Bs = set(B); rot = any(all(a*x in Bs for x in B) for a in pts[1:])
            coset += rot
            prim += (not rot)
        tag = "COVERED by thm (b <= 2t+1)" if b <= 2*t+1 else "beyond thm"
        print(f"  b={b}: blocks={len(blocks):4d}  binomial={binom:4d}  coset-union={coset:4d}  PRIMITIVE={prim:4d}   [{tag}]")
        if b <= 2*t+1 and len(blocks) != binom:
            print("  *** THEOREM VIOLATED ***")
print("prediction: for b <= 2t+1 every block is binomial (a mu_b-coset with b | n); primitives only possible b >= 2t+2.")
