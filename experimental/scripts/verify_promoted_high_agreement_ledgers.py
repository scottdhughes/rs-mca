#!/usr/bin/env python3
"""Clean arithmetic verifier for promoted high-agreement ledgers."""

def budget(q: int, lam: int = 128) -> int:
    return q // (1 << lam)

def line_exact_radius(n: int, k: int) -> int:
    return (n-k)//3

def list_unique_radius(n: int, k: int) -> int:
    return (n-k)//2

def curve_exact_radius(n: int, k: int, d: int) -> int:
    return (n-k)//(d+2)

def main():
    q = 17**32
    n = 512
    k = 256
    B = budget(q)
    print("Promoted high-agreement ledger verifier")
    print(f"q=17^32={q}")
    print(f"floor(q/2^128)={B}")
    print(f"line exact radius floor((n-k)/3)={line_exact_radius(n,k)}")
    print(f"list unique radius floor((n-k)/2)={list_unique_radius(n,k)}")
    print(f"line-alone largest safe radius={B-1}")
    print(f"line+one-list largest safe radius={B-2}")
    assert B == 6
    assert 6*(1<<128) < q < 7*(1<<128)
    assert line_exact_radius(n,k) == 85
    assert list_unique_radius(n,k) == 128
    for d in [1,2,3,4,5,6,7,8]:
        R = curve_exact_radius(n,k,d)
        curve_safe = B//d - 1
        curve_list_safe = (B-1)//d - 1
        print(f"d={d}: curve exact radius<={R}, curve safe r<={curve_safe}, curve+list safe r<={curve_list_safe}")
    print("All checks passed.")

if __name__ == "__main__":
    main()
