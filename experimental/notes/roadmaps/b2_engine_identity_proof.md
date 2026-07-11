# The moment-curve Sidon engine identities (RIGOROUS, all w >= 2)

This note isolates and PROVES the one genuinely rigorous ingredient of the w<=3 analysis: the exact
second- and fourth-moment identities for the moment-curve exponential sum over mu_n. Everything here is a
theorem (Newton's identities + orthogonality); no incidence bound, no numerics, no deferral.

## Setup
p an odd prime, n | (p-1), mu_n = { a in F_p : a^n = 1 } (|mu_n| = n). For w >= 1 and a in mu_n put
Phi(a) = (a, a^2, ..., a^w) in (F_p)^w. For c in (F_p)^w define the curve sum
    tau_w(c) = sum_{a in mu_n} e_p( c . Phi(a) ) = sum_{a in mu_n} e_p( sum_{j=1}^w c_j a^j ),   e_p(t)=e^{2 pi i t/p}.

## Theorem (engine identities). For every w >= 2 (and p > 2):
    (E2)   sum_{c in F_p^w} |tau_w(c)|^2 = p^w * n.
    (E4)   sum_{c in F_p^w} |tau_w(c)|^4 = p^w * (2 n^2 - n).

## Proof.
Expand and use orthogonality  sum_{c in F_p^w} e_p(c . V) = p^w * [V = 0]  (V in F_p^w).

(E2):  |tau_w(c)|^2 = sum_{a,b in mu_n} e_p( c . (Phi(a) - Phi(b)) ). Summing over c:
    sum_c |tau_w(c)|^2 = p^w * #{ (a,b) in mu_n^2 : Phi(a) = Phi(b) }.
Phi(a)=Phi(b) forces (first coordinate) a = b. Hence the count is n, giving (E2).

(E4):  |tau_w(c)|^4 = sum_{a,b,c',d' in mu_n} e_p( c . (Phi(a)+Phi(b)-Phi(c')-Phi(d')) ). Summing over c:
    sum_c |tau_w(c)|^4 = p^w * Q,   Q = #{ (a,b,c',d') in mu_n^4 : Phi(a)+Phi(b) = Phi(c')+Phi(d') }.
The vector equation Phi(a)+Phi(b) = Phi(c')+Phi(d') is the system of power-sum equations
    a^j + b^j = c'^j + d'^j   for j = 1, ..., w.
Since w >= 2 it INCLUDES j=1 and j=2:
    a + b   = c' + d'          (equal 1st power sums),
    a^2+b^2 = c'^2 + d'^2.
From these, ab = ((a+b)^2 - (a^2+b^2))/2 = ((c'+d')^2 - (c'^2+d'^2))/2 = c'd'  (division by 2 is legal, p>2).
Thus the pairs {a,b} and {c',d'} have equal elementary symmetric functions e_1, e_2, hence are the two roots
of the SAME monic quadratic  X^2 - (a+b) X + ab. Therefore {a,b} = {c',d'} as multisets. (The higher
equations j=3..w are then automatically consistent and impose nothing further.)

Count the ordered solutions: for each ordered pair (a,b) in mu_n^2, the ordered pairs (c',d') with
{c',d'}={a,b} are (a,b) and (b,a) -- two of them when a != b, and one (namely (a,a)) when a = b. So
    Q = 2 * #{(a,b): a != b} + 1 * #{(a,b): a = b} = 2(n^2 - n) + n = 2 n^2 - n.
This gives (E4).  QED.

## Status / verification
- Exact integer solution counts confirm Q = 2n^2 - n and the 2-fold count = n for
  (p,n,w) = (97,16,2), (97,16,3), (193,16,4), (97,32,2), (257,16,5)  -- see `verify_engine_exact.py`.
- The proof uses ONLY: orthogonality of additive characters, and that the first two power sums determine an
  unordered pair (Newton, p>2). It is uniform in w >= 2 -- the engine is NOT what fails at w >= 4.

## What this does and does NOT give
- GIVES (rigorously, all w): the "Sidon-optimal" 2nd/4th moments -- the moment curve over mu_n has NO
  nontrivial additive quadruple. This is the load-bearing large-sieve engine.
- Does NOT give the target additive-energy bound E_d^{(2)} <~ random for d-SUBSET syndromes with d > 2:
  that requires controlling the ORDER-RECURSION's higher (4-fold moment) energy E^{(2),4}, which needs
  point-plane / curve incidence bounds in F_p^w (Rudnev, available only F_p^2 / F_p^3). See the ledger:
  that closure is NUMERICALLY validated for w<=3 but NOT carried out rigorously here.
