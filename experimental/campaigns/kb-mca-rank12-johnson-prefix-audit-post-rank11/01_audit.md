# Audit of the exploratory rank-12/13 packet

## Executable defect

At exploratory head `74baa3a7a3661120ee760efd8e20f845077e67e8`, the verifier contains

```python
#__best12,__first12=best_endpoint(3,R12[3])
#__best13,__first13=best_endpoint(4,R13[4])
assert __best12 == ...
assert __best13 == ...
```

so a clean execution raises `NameError` before checking either claimed payment. A certificate whose load-bearing names are undefined is not a passing certificate.

## Mathematical defect

The global-core lemma gives, at a heavy coordinate, either:

- whole-family shortening at the same direction rank; or
- a proper-rank incident **subfamily** after shortening.

If the proper drop occurs at ambient dimension `K>s`, the child has ambient dimension `K-1`, not the full-row endpoint `s-1`. The exploratory proof replaces that branch by the endpoint recurrence at `K=s` without proving that all earlier-drop children are paid or that their disjoint branch loads may be summed. The statement that the endpoint incidence is the weakest local drop does not supply this missing global branch accounting.

A sound continuation needs a barrier recurrence of the form

\[
F_s(K)\le \min\left\{B_s(K),\max\left(F_s(K-1),
\left\lfloor\frac{(R+K)F_{s-1}(K-1)+C_s(K)}{d+K}\right\rfloor\right)\right\},
\]

with a proved ambient-dimension cap `B_s(K)` at every cell used. This packet adds one exact Johnson-scheme component of such a cap but does not claim the recurrence has yet fallen below the KoalaBear budget.
