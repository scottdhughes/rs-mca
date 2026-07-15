#!/usr/bin/env ruby
# Independent hostile replay of the all-profile rank-16 cap 130.
# It does not import the claimant's Python implementation.

require "digest"

U = 913_633
H0 = 5_116
A0 = 72_588
SELECTED = 131
MAX_LOAD = 214

def assert(condition, message)
  raise "AUDIT4 FAILURE: #{message}" unless condition
end

def c2(value)
  value < 2 ? 0 : value * (value - 1) / 2
end

def point_extra(multiplicity)
  c2(multiplicity - 1)
end

def dpw(degree, rho)
  value = (degree - 1) * (degree - rho - 1) + rho * rho
  alpha = 2 * rho + 1 - degree
  value -= c2(alpha + 1) if alpha > 0
  value
end

def balanced_marked(total)
  quotient, remainder = total.divmod(SELECTED)
  (SELECTED - remainder) * c2(quotient + 1) +
    remainder * c2(quotient + 2)
end

def balanced_point(total)
  return 0 if total <= 0
  quotient, remainder = total.divmod(SELECTED)
  (SELECTED - remainder) * point_extra(quotient) +
    remainder * point_extra(quotient + 1)
end

def inverse_marked(budget, geometric_cap)
  return -1 if budget < 0
  low = -1
  high = geometric_cap
  while low < high
    middle = (low + high + 1) / 2
    if balanced_marked(middle) <= budget
      low = middle
    else
      high = middle - 1
    end
  end
  low
end

def raw_cap(lines, rows, columns, rho)
  degree = lines + rows + columns + 1
  budget = dpw(degree, rho) - c2(degree) - c2(rows) - c2(columns)
  inverse_marked(budget, [rows, columns].min * lines)
end

def strict_cap(lines, rows, columns, rho)
  return -1 if rho < rows + columns - 1
  lines + SELECTED - 1 +
    ([rows, columns].min - 1) * (rho - rows - columns + 1)
end

def tau_floor(degree, rho, rows, columns, incidence, deleted)
  remaining_degree = degree - deleted
  q = rho - deleted
  pair_total = c2(remaining_degree)
  zero_cap = q * q + q + 1

  # A divisor line is one of the arrangement lines.  Rows/columns contain
  # at most 14 marked points, a transverse at most min(r,t), and the fixed
  # endpoint line none.
  line_loss = [14, [rows, columns].min].max
  remaining_marked_multiplicity = [
    0, incidence + 2 * SELECTED - deleted * line_loss
  ].max
  known = balanced_point(remaining_marked_multiplicity)
  known += point_extra([0, rows + 1 - deleted].max)
  known += point_extra([0, columns + 1 - deleted].max)

  # Before deletion sum(m-2) at the selected points and endpoints is exactly
  # I+(r-1)+(t-1).  Deletion cannot increase it.
  known_linear_cap = incidence + rows + columns - 2
  forced = pair_total - zero_cap - known - known_linear_cap
  residual = forced <= 0 ? 0 : (forced + 1) / 2
  pair_total + known + residual
end

def isolated_cap(lines, rows, columns, rho, deleted, raw)
  degree = lines + rows + columns + 1
  upper = dpw(degree - deleted, rho - deleted)
  raw.downto(0) do |incidence|
    return incidence if tau_floor(
      degree, rho, rows, columns, incidence, deleted
    ) <= upper
  end
  -1
end

def pencil_cap(lines, rows, columns, degree, deleted)
  remaining = degree - deleted
  trivial = [rows, columns].min * lines
  return trivial if remaining <= [rows + 1, columns + 1, 2].max
  return -1 if deleted < rows + columns - 1
  candidate = lines + SELECTED - 1 +
    ([rows, columns].min - 1) * (deleted - rows - columns + 1)
  [trivial, candidate].min
end

def color_cap(lines, rows, columns)
  degree = lines + rows + columns + 1
  best = -1
  witness = nil
  (0...degree).each do |rho|
    raw = raw_cap(lines, rows, columns, rho)
    next if raw <= best

    if degree > 3 * rho
      value = [raw, strict_cap(lines, rows, columns, rho)].min
      branch = [:strict, rho]
    else
      hmax = [rho, (3 * rho - degree) / 2].min
      isolated = -1
      isolated_h = nil
      (0..hmax).each do |deleted|
        at_h = isolated_cap(lines, rows, columns, rho, deleted, raw)
        if at_h > isolated
          isolated = at_h
          isolated_h = deleted
        end
        break if isolated == raw
      end
      pencil = [raw, pencil_cap(
        lines, rows, columns, degree, rho
      )].min
      value = [isolated, pencil].max
      branch = [:split, rho, hmax, isolated_h, isolated, pencil]
    end

    if value > best
      best = value
      witness = [rho, degree, branch, raw]
    end
  end
  [best, witness]
end

# Independent brute-force checks of both convex floors on small compositions.
def compositions(total, slots, prefix = [], &block)
  if slots == 1
    yield(prefix + [total])
    return
  end
  (0..total).each do |first|
    compositions(total - first, slots - 1, prefix + [first], &block)
  end
end

(1..5).each do |slots|
  (0..11).each do |total|
    marked = nil
    point = nil
    compositions(total, slots) do |parts|
      m = parts.sum { |x| c2(x + 1) }
      e = parts.sum { |x| point_extra(x) }
      marked = m if marked.nil? || m < marked
      point = e if point.nil? || e < point
    end
    q, rem = total.divmod(slots)
    marked_closed = (slots - rem) * c2(q + 1) + rem * c2(q + 2)
    point_closed = (slots - rem) * point_extra(q) +
      rem * point_extra(q + 1)
    assert(marked == marked_closed, "marked convexity")
    assert(point == point_closed, "point convexity")
  end
end

# Preserve the hostile nonmonotonicity regression that invalidates binary
# inversion of the isolated branch.
regression = (0..15).map do |incidence|
  tau_floor(32, 13, 15, 15, incidence, 2)
end
assert(regression == [
  650, 650, 649, 649, 648, 648, 647, 647,
  646, 646, 645, 645, 644, 644, 643, 643
], "nonmonotone isolated branch")
assert(dpw(30, 11) == 643, "nonmonotone DPW")

grid_pairs = []
(13..15).each do |ceiling|
  (1..ceiling).each do |rows|
    (1..ceiling).each do |columns|
      next if SELECTED > rows * columns
      next if SELECTED > 14 * rows || SELECTED > 14 * columns
      grid_pairs << [rows, columns]
    end
  end
end
grid_pairs.uniq!
grid_pairs.sort!
assert(grid_pairs.length == 28, "selected-131 grid census")
assert(grid_pairs.any? { |r, c| r != c }, "nonsquare profiles present")

# Check the fixed-line-center exclusion on every original strict branch,
# including zero transverse load.  This is independent of the scan outcome.
grid_pairs.each do |rows, columns|
  (0..MAX_LOAD).each do |lines|
    degree = lines + rows + columns + 1
    (0...degree).each do |rho|
      next unless degree > 3 * rho
      assert(degree - rho > [rows + 1, columns + 1, 2].max,
             "strict center exclusion")
    end
  end
end

# Every one of the 28 profiles receives the stripped-field sharpening.  There
# is no weaker nonsquare-profile dispatch.
cache = {}
grid_pairs.each do |rows, columns|
  (0..MAX_LOAD).each do |lines|
    cache[[rows, columns, lines]] = color_cap(lines, rows, columns)
  end
end

def row_bound(core)
  (A0 - core) / (H0 - core) - 1
end

def balanced_total(cache, divisor, rows, columns)
  best = nil
  (0..(U / divisor)).each do |low_load|
    max_remainder = [divisor - 1, U - divisor * low_load].min
    low_cap, low_witness = cache.fetch([rows, columns, low_load])
    candidates = [[divisor * low_cap, low_load, 0,
                   low_cap, low_cap, low_witness, low_witness]]
    if max_remainder > 0
      high_cap, high_witness = cache.fetch(
        [rows, columns, low_load + 1]
      )
      candidates << [
        (divisor - max_remainder) * low_cap +
          max_remainder * high_cap,
        low_load, max_remainder, low_cap, high_cap,
        low_witness, high_witness
      ]
    end
    # For fixed low_load the aggregate is affine in the remainder, so its
    # maximum over every M<=U is at one of these two endpoints even when the
    # one-color cap is nonmonotone in load.
    candidates.each do |candidate|
      best = candidate if best.nil? || candidate[0] > best[0]
    end
  end
  best
end

rows_out = []
(0..832).each do |core|
  divisor = H0 - core
  ceiling = row_bound(core)
  profiles = []
  grid_pairs.each do |rows, columns|
    next if rows > ceiling || columns > ceiling
    aggregate = balanced_total(cache, divisor, rows, columns)
    profiles << [aggregate[0], rows, columns, aggregate]
  end
  total, rows, columns, aggregate = profiles.max
  need = SELECTED * (62_356 + core)
  rows_out << [core, need - total, need, total, ceiling,
               rows, columns, aggregate]
end

assert(rows_out.all? { |row| row[1] > 0 }, "selected-131 failure")
minimum = rows_out.min_by { |row| row[1] }
assert(minimum[0, 7] == [0, 2_215, 8_168_636, 8_166_421,
                         13, 13, 13], "minimum identity")
assert(minimum[7][1, 4] == [178, 2_985, 1_591, 1_600],
       "minimum load mixture")

# Independent adjacent negative control at c=0.  This proves only sharpness
# of this relaxation, not existence of a source configuration.
Object.send(:remove_const, :SELECTED)
SELECTED = 130
ar = 13
ac = 13
adjacent_cache = {}
(0..MAX_LOAD).each do |lines|
  adjacent_cache[[ar, ac, lines]] = color_cap(lines, ar, ac)
end
adjacent_aggregate = balanced_total(adjacent_cache, H0, ar, ac)
adjacent_total = adjacent_aggregate[0]
adjacent_margin = 130 * 62_356 - adjacent_total
assert([adjacent_margin, ar, ac, adjacent_total] ==
       [-29_445, 13, 13, 8_135_725], "adjacent negative control")

# Restore the selected count only for clarity in all subsequent statements.
Object.send(:remove_const, :SELECTED)
SELECTED = 131

pins = {
  "RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md" =>
    "4229a4859dd3ebec80e646428b8a0a7a1914b7f56638e386a7a7f33b5568080d",
  "RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md" =>
    "09fbf955ee629381a2f4b5f62fcbc0893852668a755c0df79d3daac9cbf9f59f",
  "HOSTILE_AUDIT_RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md" =>
    "036b6050654d3dd1460ff48b959e97ae4ffc7eb1e9c4f217c3980df0c2189bcf",
  "HOSTILE_AUDIT1_RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md" =>
    "eb544b7fe67f95261194883dedb23ad4c84efc8693a3ea8e54f577b1484a1326",
  "HOSTILE_AUDIT3_RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md" =>
    "76f9e64c48cd334c67cb854633695be1f608ab59d7af69d24b82625162d71aa1",
  "RANK16_WEIGHTED_GRID_EXTACTIC_DPW_CAP130.md" =>
    "166e3947422fab3024ca99e4022d6d61e7b0c64a416a16abc533f4bfa96e23e2",
  "verify_rank16_weighted_grid_extactic_dpw_cap130.py" =>
    "3e5f4f3ee3a313db07ee314393bba5db9478d0ba3e360744b27e00a514400e9f",
  "verify_rank16_weighted_grid_extactic_dpw_cap130.expected.txt" =>
    "94929ecbd4b7b5d93677a3d2c6a9a4116de4c0cebb11e0877d5259b29a1000d3"
}
pins.each do |name, expected|
  actual = Digest::SHA256.file(File.join(__dir__, name)).hexdigest
  assert(actual == expected, "pin #{name}: #{actual}")
end

numeric_ledger = rows_out.map do |row|
  a = row[7]
  [row[0], row[1], row[2], row[3], row[4], row[5], row[6],
   a[1], a[2], a[3], a[4]].join(",")
end.join("\n") + "\n"
audit_ledger = Digest::SHA256.hexdigest(numeric_ledger)

puts "HOSTILE_AUDIT4_RANK16_WEIGHTED_GRID_EXTACTIC_DPW_CAP130: PASS"
puts "independent_language=ruby claimant_code_imported=false"
puts "source_and_audit_pins=#{pins.length} all_match=true"
puts "selected=131 all_profiles=28 nonsquare_dispatch=false cores=0..832 failures=0"
puts "strict_center_gate=checked deleted_line_loss=max(14,min(r,t))"
puts "isolated_inversion=exhaustive nonmonotone_regression=true"
puts "uniform_min=c0,grid13x13,loads178/179,high2985,caps1591/1600,margin2215"
puts "adjacent_selected130=c0,grid13x13,margin-29445"
puts "audit_numeric_ledger_sha256=#{audit_ledger}"
puts "local_conclusion=active_pencil_occupancy_at_most_130"
puts "scope=no_owner_theorem,no_rank16_parent_payment,no_official_score_payment"
