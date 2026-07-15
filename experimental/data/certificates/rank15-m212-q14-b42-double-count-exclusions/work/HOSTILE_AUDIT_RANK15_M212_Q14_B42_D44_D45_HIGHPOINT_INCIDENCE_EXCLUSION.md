# Hostile audit: `q=14`, `B=42`, `D=44,45` high-point incidence exclusion

## Verdict

`ACCEPT`, with high confidence, conditional only on the already accepted
`U=E=0` boundary transport.  The proof is a finite incidence theorem and
does not use the cyclic-net classification from `D=39`.

## Independent checks

1. The aggregate residual ledgers imply that every unmarked residual
   intersection is double.  Thus every point of multiplicity at least three
   is marked and has multiplicity at most 15.
2. The three exact moment equations reduce, for fixed `D`, to a bounded
   partition of `211-D` integers `x in 1..13` with `sum x=208` and
   `sum x^2=676`.
3. Independent ascending-part enumeration gives exactly four partitions at
   `D=44` and four at `D=45`, equal to those printed in the theorem.
4. On a line, subtracting twice the support equation from the other-line
   incidence equation gives

   ```text
   d_L=sum_(high P on L)(mult(P)-3)-11.
   ```

   If a `k<14` high point is alone on an incident line then `d_L=k-14<0`.
   Therefore all `k` lines through it must use distinct other high points,
   forcing `k<=H-1`.
5. The four `D=44` rows violate this with `(k,H)=(11,4),(12,4),(6,5),(7,6)`.
   The four `D=45` rows violate it with
   `(12,5),(5,5),(9,6),(6,6)`.

No field arithmetic, residue normalization, or assumption about the double
graph is hidden in this argument.

## Scope

This audit pays only `D=44,45`.  At `D=46` the bounded moment census has six
profiles; the lemma removes four and leaves two exact profiles.  No full
`q=14,B=42` closure is claimed here.

