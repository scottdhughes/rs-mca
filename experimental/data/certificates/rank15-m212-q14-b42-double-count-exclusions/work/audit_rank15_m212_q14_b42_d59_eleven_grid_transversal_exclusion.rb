#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

ROOT = File.expand_path("..", __dir__)
PINS = {
  "work/RANK15_M212_Q14_B42_D59_ELEVEN_GRID_TRANSVERSAL_EXCLUSION.md" =>
    "52fedf346ed2dfda2611f2aacb651c5d813c85491ffe43f47534fff8d47b7f98",
  "work/verify_rank15_m212_q14_b42_d59_eleven_grid_transversal_exclusion.rb" =>
    "cca8e0d20dabbed8ab294ac5fd5fce135fcb4e47b8ba5789c9ab2ff39a4f5579",
  "work/verify_rank15_m212_q14_b42_d59_eleven_grid_transversal_exclusion.expected.txt" =>
    "a47cad4e8533c208ee0015d83313c5b606a40027d874b21d421c10412ee2aa98"
}.freeze

def check(value, message)
  raise message unless value
end

PINS.each do |relative, expected|
  check(Digest::SHA256.file(File.join(ROOT, relative)).hexdigest == expected,
        "pin drift #{relative}")
end

# Independent ascending profile enumeration at D=59.
profiles = []
counts = Array.new(13, 0)
walk = nil
walk = lambda do |weight, total, square, number|
  if weight == 13
    profiles << counts[1, 12].dup if total == 56 && square == 412 && number <= 152
    next
  end
  maximum = [(56 - total) / weight, (412 - square) / (weight * weight),
             152 - number].min
  (0..maximum).each do |multiplicity|
    counts[weight] = multiplicity
    walk.call(weight + 1, total + weight * multiplicity,
              square + weight * weight * multiplicity, number + multiplicity)
  end
  counts[weight] = 0
end
walk.call(1, 0, 0, 0)
check(profiles.length == 958, "D59 profile total")

def group_patterns(threshold)
  rows = []
  counts = Array.new(10, 0)
  visit = nil
  visit = lambda do |weight, total|
    if weight == 11
      used = (1..10).select { |w| counts[w - 1].positive? }
      rows << counts.dup if !used.empty? && total >= threshold &&
                                total - used.min < threshold
      next
    end
    maximum = (threshold + 9 - total) / weight
    if maximum >= 0
      (0..maximum).each do |multiplicity|
        counts[weight - 1] = multiplicity
        visit.call(weight + 1, total + weight * multiplicity)
      end
    end
    counts[weight - 1] = 0
  end
  visit.call(1, 0)
  rows
end

PATTERNS = (1..10).to_h { |threshold| [threshold, group_patterns(threshold)] }
MEMO = {}
cover = nil
cover = lambda do |state, threshold|
  key = [state, threshold]
  next MEMO[key] if MEMO.key?(key)
  best = 0
  PATTERNS.fetch(threshold).each do |group|
    next unless (0...10).all? { |i| group[i] <= state[i] }
    rest = (0...10).map { |i| state[i] - group[i] }
    best = [best, 1 + cover.call(rest, threshold)].max
  end
  MEMO[key] = best
end

kept = profiles.select do |profile|
  small = profile[0, 10]
  big = profile[10] + profile[11]
  small.each_with_index.all? do |multiplicity, index|
    next true if multiplicity.zero?
    other = small.dup
    other[index] -= 1
    index + 4 <= big + cover.call(other, 10 - index)
  end
end

high_lists = kept.map do |profile|
  profile.each_with_index.flat_map { |multiplicity, index| [index + 4] * multiplicity }
end.sort
expected_high = [
  [4] * 18 + [5, 5, 14, 14, 15],
  [4] * 3 + [5] * 10 + [12, 15, 15],
  [4] * 20 + [5, 13, 15, 15]
].sort
check(high_lists == expected_high, "D59 survivor rows")

check(3 + 11 + 13 + 13 + 2 == 42, "line total")
check(2 + 22 + 13 + 11 + 2 * 35 == 118, "double degree sum")
check((2_130_706_433 - 1) % 13 == 10, "field gate")

vector = [profiles.length, kept.length, 42, 118, 11, 10].join(":") + "\n"
output = [
  "AUDIT_RANK15_M212_Q14_B42_D59_ELEVEN_GRID_TRANSVERSAL_EXCLUSION: PASS",
  "profiles=958 local_survivors=3 independent=true",
  "skeleton=10+10 split lines42 double_degree_sum118",
  "grid=11_transversals stabilizer_order13",
  "field_remainder=10",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D59",
  "nonclaim=D60_or_larger"
].join("\n") + "\n"

expected_path = File.join(__dir__,
  "audit_rank15_m212_q14_b42_d59_eleven_grid_transversal_exclusion.expected.txt")
check(File.file?(expected_path), "missing expected output")
check(output == File.binread(expected_path), "expected-output drift")
print output

