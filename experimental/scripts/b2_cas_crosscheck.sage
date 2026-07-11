# Independent Sage verification of the second-moment trade identity + V(s)
def mu_sub(p, n):
    F = GF(p); g = F.multiplicative_generator()
    h = g**((p-1)//n)
    return [h**k for k in range(n)]
def check(p, n, m):
    S = mu_sub(p, n)
    from collections import defaultdict
    from itertools import combinations
    # fibers via (p1,p2); second moment = sum len^2
    buck = defaultdict(int)
    for idx in combinations(range(n), m):
        k = (sum(S[i] for i in idx), sum(S[i]^2 for i in idx))
        buck[k] += 1
    second = sum(c^2 for c in buck.values())
    # V(s) = ordered disjoint s-for-s trades with equal (p1,p2)
    def V(s):
        sb = defaultdict(list)
        for A in combinations(range(n), s):
            k = (sum(S[i] for i in A), sum(S[i]^2 for i in A))
            sb[k].append(frozenset(A))
        c = 0
        for lst in sb.values():
            for A in lst:
                for B in lst:
                    if A.isdisjoint(B): c += 1
        return c
    formula = binomial(n, m) + sum(V(s)*binomial(n-2*s, m-s) for s in range(3, m+1) if n-2*s >= 0)
    print("SAGE  p=%d n=%d m=%d:  Sum_v f_v^2 = %d ;  C(n,m)+Sum_s V(s)C(n-2s,m-s) = %d ;  MATCH=%s"
          % (p, n, m, second, formula, second == formula))
    for s in range(3, min(m,5)+1):
        if n-2*s>=0: print("   V(%d) = %d" % (s, V(s)))
check(13, 12, 5)
check(17, 16, 6)
