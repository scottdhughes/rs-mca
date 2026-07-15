#!/usr/bin/env python3
"""Exact all-profile Chern/Tjurina replay for the rank-16 cap 130."""

from __future__ import annotations

from bisect import bisect_right
from hashlib import sha256
from pathlib import Path


A0 = 72_588
H0 = 5_116
U = 913_633
MAX_LOAD = 214
SELECTED = 131


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("CHECK FAILED: " + message)


def c2(value: int) -> int:
    return 0 if value < 2 else value * (value - 1) // 2


def dpw_upper(degree: int, rho: int) -> int:
    value = (degree - 1) * (degree - rho - 1) + rho * rho
    alpha = 2 * rho + 1 - degree
    return value - (c2(alpha + 1) if alpha > 0 else 0)


class Scan:
    def __init__(self, selected: int) -> None:
        self.selected = selected
        self.marked = [self.marked_floor(i)
                       for i in range(selected * MAX_LOAD + 1)]

    def marked_floor(self, total: int) -> int:
        q, r = divmod(total, self.selected)
        return ((self.selected - r) * c2(q + 1) + r * c2(q + 2))

    @staticmethod
    def point_extra(multiplicity: int) -> int:
        return c2(multiplicity - 1)

    def balanced_point_extra(self, total: int) -> int:
        if total <= 0:
            return 0
        q, r = divmod(total, self.selected)
        return ((self.selected - r) * self.point_extra(q)
                + r * self.point_extra(q + 1))

    def raw_cap(self, lines: int, rows: int, columns: int, rho: int) -> int:
        degree = lines + rows + columns + 1
        budget = (dpw_upper(degree, rho) - c2(degree)
                  - c2(rows) - c2(columns))
        return min(min(rows, columns) * lines,
                   bisect_right(self.marked, budget) - 1)

    def strict_cap(self, lines: int, rows: int, columns: int,
                   rho: int) -> int:
        if rho < rows + columns - 1:
            return -1
        return (lines + self.selected - 1
                + (min(rows, columns) - 1)
                * (rho - rows - columns + 1))

    def tau_floor(self, degree: int, rho: int, rows: int, columns: int,
                  incidence: int, deleted: int) -> int:
        remaining_degree = degree - deleted
        q = rho - deleted
        pair_total = c2(remaining_degree)
        point_cap = q * q + q + 1
        line_loss = max(14, min(rows, columns))
        selected_multiplicity = max(
            0, incidence + 2 * self.selected - deleted * line_loss)
        known = self.balanced_point_extra(selected_multiplicity)
        known += self.point_extra(max(0, rows + 1 - deleted))
        known += self.point_extra(max(0, columns + 1 - deleted))
        known_linear_cap = incidence + rows + columns - 2
        forced = pair_total - point_cap - known - known_linear_cap
        residual = max(0, (forced + 1) // 2)
        return pair_total + known + residual

    def isolated_cap(self, lines: int, rows: int, columns: int, rho: int,
                     deleted: int, raw: int) -> int:
        degree = lines + rows + columns + 1
        upper = dpw_upper(degree - deleted, rho - deleted)
        for incidence in range(raw, -1, -1):
            if self.tau_floor(degree, rho, rows, columns,
                              incidence, deleted) <= upper:
                return incidence
        return -1

    def pencil_cap(self, lines: int, rows: int, columns: int,
                   degree: int, deleted: int) -> int:
        size = degree - deleted
        trivial = min(rows, columns) * lines
        if size <= max(rows + 1, columns + 1, 2):
            return trivial
        if deleted < rows + columns - 1:
            return -1
        return min(trivial,
                   lines + self.selected - 1
                   + (min(rows, columns) - 1)
                   * (deleted - rows - columns + 1))

    def color_cap(self, lines: int, rows: int, columns: int):
        degree = lines + rows + columns + 1
        best = -1
        witness = None
        for rho in range(degree):
            raw = self.raw_cap(lines, rows, columns, rho)
            if raw <= best:
                continue
            if degree > 3 * rho:
                value = min(raw, self.strict_cap(lines, rows, columns, rho))
                branch = ("strict", rho)
            else:
                hmax = min(rho, (3 * rho - degree) // 2)
                isolated = -1
                isolated_h = None
                for deleted in range(hmax + 1):
                    cap = self.isolated_cap(
                        lines, rows, columns, rho, deleted, raw)
                    if cap > isolated:
                        isolated, isolated_h = cap, deleted
                    if isolated == raw:
                        break
                pencil = min(raw, self.pencil_cap(
                    lines, rows, columns, degree, rho))
                value = max(isolated, pencil)
                branch = ("split", rho, hmax, isolated_h,
                          isolated, pencil)
            if value > best:
                best, witness = value, (rho, degree, branch, raw)
        return best, witness

    def grid_pairs(self):
        pairs = set()
        for ceiling in (13, 14, 15):
            for rows in range(1, ceiling + 1):
                for columns in range(1, ceiling + 1):
                    if self.selected > rows * columns:
                        continue
                    if (self.selected > 14 * rows
                            or self.selected > 14 * columns):
                        continue
                    pairs.add((rows, columns))
        return sorted(pairs)

    def cache(self, pairs):
        return {(rows, columns, lines): self.color_cap(lines, rows, columns)
                for rows, columns in pairs
                for lines in range(MAX_LOAD + 1)}

    @staticmethod
    def row_bound(core: int) -> int:
        return (A0 - core) // (H0 - core) - 1

    def balanced_total(self, cache, divisor: int, rows: int, columns: int):
        best = None
        for low_load in range(U // divisor + 1):
            remainder = min(divisor - 1, U - divisor * low_load)
            low_cap, low_witness = cache[(rows, columns, low_load)]
            candidates = [(divisor * low_cap, low_load, 0,
                           low_cap, low_cap, low_witness, low_witness)]
            if remainder:
                high_cap, high_witness = cache[
                    (rows, columns, low_load + 1)]
                candidates.append((
                    (divisor - remainder) * low_cap + remainder * high_cap,
                    low_load, remainder, low_cap, high_cap,
                    low_witness, high_witness))
            for candidate in candidates:
                if best is None or candidate[0] > best[0]:
                    best = candidate
        return best

    def full_scan(self):
        pairs = self.grid_pairs()
        cache = self.cache(pairs)
        rows_out = []
        for core in range(833):
            divisor = H0 - core
            ceiling = self.row_bound(core)
            profiles = []
            for rows, columns in pairs:
                if rows <= ceiling and columns <= ceiling:
                    aggregate = self.balanced_total(
                        cache, divisor, rows, columns)
                    profiles.append((aggregate[0], rows, columns, aggregate))
            total, rows, columns, aggregate = max(profiles)
            need = self.selected * (62_356 + core)
            rows_out.append((core, need - total, need, total, ceiling,
                             rows, columns, aggregate))
        return pairs, rows_out


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parent
    pins = {
        "RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md":
            "4229a4859dd3ebec80e646428b8a0a7a1914b7f56638e386a7a7f33b5568080d",
        "RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md":
            "09fbf955ee629381a2f4b5f62fcbc0893852668a755c0df79d3daac9cbf9f59f",
    }
    for name, expected in pins.items():
        check(file_hash(root / name) == expected, "source pin " + name)

    # Directly pins the hostile nonmonotonicity that forbids binary inversion.
    regression = Scan(140)
    floors = [regression.tau_floor(32, 13, 15, 15, i, 2)
              for i in range(16)]
    check(floors == [650, 650, 649, 649, 648, 648, 647, 647,
                     646, 646, 645, 645, 644, 644, 643, 643],
          "nonmonotone isolated branch")

    scan = Scan(SELECTED)
    pairs, rows = scan.full_scan()
    check(len(pairs) == 28, "selected-131 grid census")
    check(all(row[1] > 0 for row in rows), "selected-131 failure")
    minimum = min(rows, key=lambda row: row[1])
    check(minimum[:7] == (0, 2_215, 8_168_636, 8_166_421,
                          13, 13, 13), "minimum identity")
    check(minimum[7][1:5] == (178, 2_985, 1_591, 1_600),
          "minimum load mixture")
    ledger = "\n".join(repr(row) for row in rows) + "\n"
    ledger_hash = sha256(ledger.encode("ascii")).hexdigest()
    check(ledger_hash ==
          "edc0e5f7398d5c9ce02e25b58572712cf1cc50ed8f1b769cb89393c9b7417351",
          "selected-131 ledger hash " + ledger_hash)

    # Exact adjacent negative control.  It is sufficient to replay c=0,
    # whose 13x13 profile already survives with the stated deficit.
    adjacent = Scan(130)
    adjacent_pairs = [(r, c) for r, c in adjacent.grid_pairs()
                      if r <= 13 and c <= 13]
    adjacent_cache = adjacent.cache(adjacent_pairs)
    adjacent_profiles = []
    for r, c in adjacent_pairs:
        aggregate = adjacent.balanced_total(adjacent_cache, H0, r, c)
        adjacent_profiles.append((aggregate[0], r, c, aggregate))
    adjacent_total, ar, ac, adjacent_aggregate = max(adjacent_profiles)
    adjacent_margin = 130 * 62_356 - adjacent_total
    check((adjacent_margin, ar, ac, adjacent_total) ==
          (-29_445, 13, 13, 8_135_725),
          "selected-130 negative control")

    print("RANK16_WEIGHTED_GRID_EXTACTIC_DPW_CAP130: PASS")
    print("selected=131 all_profiles=28 cores=0..832 failures=0")
    print("uniform_min=c0,grid13x13,loads178/179,high2985,"
          "caps1591/1600,need8168636,total8166421,margin2215")
    print("adjacent_selected130=c0,grid13x13,"
          "need8106280,total8135725,margin-29445")
    print("scan_sha256=" + ledger_hash)
    print("conclusion=UNIFORM_ACTIVE_PENCIL_OCCUPANCY_AT_MOST_130")


if __name__ == "__main__":
    main()
