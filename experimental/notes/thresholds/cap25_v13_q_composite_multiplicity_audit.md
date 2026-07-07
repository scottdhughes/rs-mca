# CAP25 v13 Q Composite Multiplicity Audit

**Status:** AUDIT / REPAIR / ROUTE_CUT.

This note records a narrow correction in the Q-prefix quotient-charging layer.
It does not prove any adjacent deployed safe row.

## Exact repair

Let \(S=s_0H\subset \mathbb F_p^\times\) be a multiplicative coset with
\(|H|=N\).  Let \(e\ge1\), \(c=\gcd(e,N)\), and \(S^e=\{a^e:a\in S\}\).
Then the map
\[
        a\mapsto a^e
\]
from \(S\) to \(S^e\) has constant fiber size \(c\), not generally \(e\).
Thus, for \(g(X)=h(X^e)\),
\[
        \sum_{\substack{A\subseteq S\\ |A|=m}}
        \psi\!\left(\sum_{a\in A} h(a^e)\right)
        =
        [T^m]\prod_{b\in S^e}\bigl(1+T\psi(h(b))\bigr)^c .
\]
The older multiplicity \(e\) is valid only in the special case \(e\mid N\).

## First false line

The false line is the unqualified replacement of the power-map fiber size by
\(e\).  For example, take \(S=\mathbb F_5^\times\), so \(N=4\), and take
\(e=3\).  The cube map is a bijection on \(S\), so \(c=\gcd(3,4)=1\), not
\(3\).  With \(m=1\) and \(h(X)=X\), the left side is
\[
        \sum_{a\in \mathbb F_5^\times}\psi(a^3)
        =
        \sum_{b\in \mathbb F_5^\times}\psi(b),
\]
whereas the incorrect exponent \(e=3\) would triple this contribution.

## Usefulness

This repair keeps composite prefix Fourier directions on the correct image
coset with the correct multiplicity.  When \(c>1\), the contribution belongs
to the quotient ledger.  When \(c=1\), there is no quotient multiplicity to
charge.  In both cases, the repair prevents overcharging when the common index
divisor \(e\) does not divide the coset order \(N\).

It does not close the CAP25 v13 Q safe side.  After quotient-pulled-back
directions are charged, the live wall remains primitive max-fiber flatness
with row-sharp constants at the deployed adjacent rows.

## Next target

Attack the primitive Q layer directly:

- prove a row-sharp primitive max-fiber bound with constants fitting the
  KoalaBear and Mersenne-31 adjacent margins; or
- produce a primitive full-orbit heavy-fiber obstruction; or
- extract a finite certificate family that replaces the missing primitive
  max-fiber theorem inside the adjacent upper ledger.
