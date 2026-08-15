# Certificate and custody review

Status: **GREEN.**

- Parent SHA is exact and immutable.
- All row parameters are integers copied from the predecessor packet.
- The result is canonical JSON with sorted keys and compact separators.
- The manifest binds every packet file by SHA-256.
- The payload hash binds the parent, result hash, and complete file-hash map.
- Primary and independent verifiers use separate implementations.
- Hostile mutations alter load, parent count, intersection values, weighted
  loads, or prohibited closure claims and are rejected.
- No floating-point value decides a theorem gate.
