# M31 exact all-weight anchor-exchange Padé bijection

This packet proves an exact complete-list reduction relative to any actual
listed anchor.  Every nonanchor codeword is represented uniquely by a pair
`(G,b)` satisfying strict degree, coprimality, full-gcd, and radius gates.
The exact error locator is

```text
G * (L0 / gcd(L0, G - b*V)).
```

Writing `t=R-j0` and `m=deg(G)-t` cancels the anchor slack exactly:

```text
w0 = w+t,  m >= w+1,  deg(b) < m-w,
deg(gcd(L0,G-b*V)) >= m,  j = R+m-deg(gcd(L0,G-b*V)).
```

For M31 this means `m >= 67,448`; a nonanchor can exist only when
`t <= 913,681`.

The fresh-symbol boundary-forcing lemma uses
`B_star+1 = 16,777,216 < p^4`: any counterexample sublist of that size can
be preserved while changing the received word so that one retained codeword
has exact radius `R`.  Therefore the deployed closing census needs only
boundary anchors `t=0`, but it must still allow arbitrary unit `V`.

The module orientation is load-bearing:

```text
M_U = {(W,N): N == W*U mod A0*L0}
basis = (L0,0), (V,A0).
```

The packet also proves a route cut: one exact anchor permits every unit `V`
modulo `L0`, so rank two alone cannot force rational, periodic, quotient, or
low-degree structure.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m31_all_weight_anchor_exchange_pade_bijection_v1.py
python3 -O experimental/scripts/verify_m31_all_weight_anchor_exchange_pade_bijection_v1.py
/usr/local/bin/sage experimental/scripts/verify_m31_all_weight_anchor_exchange_pade_bijection_v1.sage
python3 experimental/scripts/verify_m31_all_weight_anchor_exchange_packet_v1.py --check
python3 -O experimental/scripts/verify_m31_all_weight_anchor_exchange_packet_v1.py --check
python3 experimental/scripts/verify_m31_all_weight_anchor_exchange_packet_v1.py --tamper-selftest
```

Passing replay does not prove the M31 LIST upper bound.  The remaining exact
theorem is a uniform upper bound of `16,777,214` on the nonanchor pair census
for every boundary-anchor M31 triple `(A0,L0,V)`.  This packet has zero
ledger, endpoint, and score movement.
