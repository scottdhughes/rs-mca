#!/usr/bin/env python3
"""Exact finite counterexample to the rank-by-rank Eq. 29 bound.

Parameters:
    p=17, n=8=2^3, w=6, m=7, d=n-w-1=1, c=w+1=7.

The script computes, by exact dynamic programming (not sampling),

    Sigma_v = sum_{lambda in F_p^n, A_lambda != 0}
              chi(A_lambda) e_p(Phi_v(lambda)),

where for d=1
    A_lambda = sum_a lambda_a a^2,
    Phi_v = gamma - ell^2/(4 A_lambda).

It verifies
    Sigma_v1 = 16*17^6*tau,   Sigma_v0 = 0,
where |tau|=sqrt(17).  Consequently the centered Eq. 29 bound cannot
hold for all v, since the difference is more than twice the proposed bound.
"""

from collections import defaultdict
from math import sqrt

P = 17
N = 8
W = 6
M = 7
D = N - W - 1
C = W + 1

assert D == 1

# mu_8 in F_17; 9 has order 8.
H = [1, 9, 13, 15, 16, 8, 4, 2]
assert len(set(H)) == N
assert all(pow(a, N, P) == 1 for a in H)


def inv(x: int) -> int:
    return pow(x % P, P - 2, P)


def legendre(x: int) -> int:
    x %= P
    if x == 0:
        return 0
    return 1 if pow(x, (P - 1) // 2, P) == 1 else -1


def g_values(v: tuple[int, ...]) -> list[int]:
    """Evaluate the fixed interpolation polynomial g_v on H.

    Its coefficients are alpha_0=m/n, alpha_1=0, and
    alpha_{n-j}=v_j/n for 1<=j<=w.  The alpha_1 coordinate is the
    single free variable u in f_u=g_v+uX.
    """
    assert len(v) == W
    alpha = [0] * N
    alpha[0] = M * inv(N) % P
    for j, value in enumerate(v, start=1):
        alpha[N - j] = value * inv(N) % P

    out = []
    for a in H:
        out.append(sum(alpha[r] * pow(a, r, P) for r in range(N)) % P)
    return out


def phase_coefficients(v: tuple[int, ...], full_support: bool = False) -> list[int]:
    """Return exact C[r] with Sigma_v = sum_r C[r] e_p(r).

    Dynamic-programming state is (A, ell, gamma).  Each lambda_a ranges
    over all of F_p.  The condition A != 0 is exactly rank(A_lambda)=d=1.
    """
    gv = g_values(v)
    acoef = [(a * a) % P for a in H]
    lcoef = [((2 * g - 1) * a) % P for g, a in zip(gv, H)]
    qcoef = [(g * g - g) % P for g in gv]

    dp: dict[tuple[int, int, int], int] = {(0, 0, 0): 1}
    for aa, ll, qq in zip(acoef, lcoef, qcoef):
        nxt: dict[tuple[int, int, int], int] = defaultdict(int)
        for (A, ell, gamma), count in dp.items():
            lambdas = range(1, P) if full_support else range(P)
            for lam in lambdas:
                key = (
                    (A + lam * aa) % P,
                    (ell + lam * ll) % P,
                    (gamma + lam * qq) % P,
                )
                nxt[key] += count
        dp = dict(nxt)

    coeff = [0] * P
    for (A, ell, gamma), count in dp.items():
        if A == 0:
            continue
        phi = (gamma - ell * ell * inv(4 * A)) % P
        coeff[phi] += legendre(A) * count
    return coeff


def expected_vector(scale: int) -> list[int]:
    return [0] + [scale * legendre(r) for r in range(1, P)]


# A 7-subset is the complement of one b in mu_8.  Take b=2.
# Its first six power sums are -2^j.
v1 = tuple((-pow(2, j, P)) % P for j in range(1, W + 1))
v0 = (0,) * W

c1 = phase_coefficients(v1)
c0 = phase_coefficients(v0)

# The full-support sub-sum used in the question (all lambda_a != 0).
c1_star = phase_coefficients(v1, full_support=True)
c0_star = phase_coefficients(v0, full_support=True)

scale = (P - 1) * P ** (N - 2)  # 16*17^6
assert c1 == expected_vector(scale), (c1, expected_vector(scale))
assert c0 == [0] * P, c0

full_scale_1 = 237_783_657
full_scale_0 = -36
assert c1_star == expected_vector(full_scale_1), c1_star
assert c0_star == expected_vector(full_scale_0), c0_star
full_difference_scale = full_scale_1 - full_scale_0
assert full_difference_scale**2 * P > (2 * P**6)**2

# |Sigma_v1-Sigma_v0| = scale*sqrt(P), since the quadratic Gauss sum
# tau=sum_r chi(r)e_p(r) has absolute value sqrt(P).
sigma_difference_squared = scale * scale * P
sigma_bound = P ** (N / 2 + 2)  # p^6
assert sigma_bound == P**6

# If both centered values were <= sigma_bound, their difference would be
# <= 2*sigma_bound.  Compare squares using integers only.
assert sigma_difference_squared > (2 * int(sigma_bound)) ** 2

# For T_d itself there is one additional Gauss factor of absolute value
# sqrt(P), so |T_d(v1)-T_d(v0)|=(p-1)p^(n-1).
t_difference = (P - 1) * P ** (N - 1)
eq29_bound = P ** (N + 2 - C / 2)  # p^(13/2)
ratio_to_twice_bound = t_difference / (2 * eq29_bound)

print(f"p={P}, n={N}, w={W}, m={M}, d={D}, c={C}")
print(f"mu_n={H}")
print(f"v1={v1}")
print(f"v0={v0}")
print(f"phase coefficient scale = (p-1)p^(n-2) = {scale}")
print("C_v1[r] = scale*chi(r) for r!=0, and C_v1[0]=0: VERIFIED")
print("C_v0[r] = 0 for every r: VERIFIED")
print(f"|Sigma_v1-Sigma_v0| = {scale}*sqrt({P})")
print("full-support sub-sum:")
print(f"  C_v1^*[r] = {full_scale_1}*chi(r), C_v0^*[r] = {full_scale_0}*chi(r)")
print(f"  |S_v1^*-S_v0^*| = {full_difference_scale}*sqrt({P})")
print(f"  full-support difference / (2*p^6) = {full_difference_scale*sqrt(P)/(2*P**6):.12f}")
print(f"proposed per-v Sigma bound = p^(n/2+2) = {int(sigma_bound)}")
print(f"difference / (2*bound) = {scale*sqrt(P)/(2*sigma_bound):.12f}")
print(f"|T_d(v1)-T_d(v0)| = (p-1)p^(n-1) = {t_difference}")
print(f"Eq.29 bound = p^(n+2-c/2) = {eq29_bound:.12f}")
print(f"T difference / (2*Eq.29 bound) = {ratio_to_twice_bound:.12f}")
print("Therefore at least one centered T_d(v) exceeds the Eq.29 bound.")
