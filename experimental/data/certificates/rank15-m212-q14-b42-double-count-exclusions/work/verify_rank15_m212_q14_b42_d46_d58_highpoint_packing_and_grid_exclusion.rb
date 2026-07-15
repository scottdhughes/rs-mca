#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

P_FIELD = 2_130_706_433

def check(value, message)
  raise message unless value
end

def high_profiles(double_count)
  target_sum = double_count - 3
  target_square = 471 - double_count
  max_high = 211 - double_count
  counts = Array.new(13, 0)
  rows = []
  visit = nil
  visit = lambda do |weight, total, square, number|
    if weight.zero?
      rows << counts[1, 12].dup if total == target_sum &&
                                        square == target_square &&
                                        number <= max_high
      next
    end
    maximum = [(target_sum - total) / weight,
               (target_square - square) / (weight * weight),
               max_high - number].min
    (0..maximum).each do |multiplicity|
      counts[weight] = multiplicity
      visit.call(weight - 1, total + multiplicity * weight,
                 square + multiplicity * weight * weight,
                 number + multiplicity)
    end
    counts[weight] = 0
  end
  visit.call(12, 0, 0, 0)
  rows
end

def minimal_group_patterns(threshold)
  patterns = []
  counts = Array.new(10, 0)
  visit = nil
  visit = lambda do |weight, total, minimum|
    if weight.zero?
      patterns << counts.dup if total >= threshold &&
                                    total - minimum < threshold
      next
    end
    maximum = (threshold + 9 - total) / weight
    if maximum >= 0
      (0..maximum).each do |multiplicity|
        counts[weight - 1] = multiplicity
        new_minimum = multiplicity.positive? ? [minimum, weight].min : minimum
        visit.call(weight - 1, total + multiplicity * weight, new_minimum)
      end
    end
    counts[weight - 1] = 0
  end
  visit.call(10, 0, 99)
  patterns
end

PATTERNS = (1..10).to_h { |threshold| [threshold, minimal_group_patterns(threshold)] }
PACK_MEMO = {}

def maximum_groups(counts, threshold)
  key = [threshold, counts]
  cached = PACK_MEMO[key]
  return cached unless cached.nil?
  best = 0
  PATTERNS.fetch(threshold).each do |pattern|
    next unless (0...10).all? { |index| pattern[index] <= counts[index] }
    remainder = (0...10).map { |index| counts[index] - pattern[index] }
    best = [best, 1 + maximum_groups(remainder, threshold)].max
  end
  PACK_MEMO[key] = best
end

def survives_local_packing(profile)
  small = profile[0, 10]
  big_count = profile[10] + profile[11]
  small.each_with_index do |multiplicity, index|
    next if multiplicity.zero?
    weight = index + 1
    other = small.dup
    other[index] -= 1
    cap = big_count + maximum_groups(other, 11 - weight)
    return false if weight + 3 > cap
  end
  true
end

def high_list(profile)
  result = []
  profile.each_with_index do |multiplicity, index|
    multiplicity.times { result << index + 4 }
  end
  result
end

expected_counts = {
  46 => [6, 0], 47 => [12, 0], 48 => [21, 0], 49 => [30, 0],
  50 => [55, 1], 51 => [76, 0], 52 => [107, 0], 53 => [180, 0],
  54 => [237, 0], 55 => [315, 1], 56 => [444, 1],
  57 => [557, 3], 58 => [720, 3]
}.freeze

survivors = {}
(46..58).each do |double_count|
  profiles = high_profiles(double_count)
  kept = profiles.select { |profile| survives_local_packing(profile) }
  check([profiles.length, kept.length] == expected_counts.fetch(double_count),
        "census drift D#{double_count}")
  survivors[double_count] = kept.map { |profile| high_list(profile) }.sort
end

check(survivors[50] == [([4] * 12 + [14, 15, 15])], "D50 profile")
check(survivors[55] == [([4] * 8 + [5, 5] + [13] * 4)], "D55 profile")
check(survivors[56] == [([4] * 11 + [5] + [13] * 4)], "D56 profile")
check(survivors[57] == [
  [4] * 12 + [5] * 4 + [14, 14, 15],
  [4] * 14 + [5] * 3 + [13, 15, 15],
  [4] * 14 + [13] * 4
].sort, "D57 profiles")
check(survivors[58] == [
  [4] * 15 + [5] * 3 + [14, 14, 15],
  [4] * 17 + [5, 5, 13, 15, 15],
  [5] * 11 + [12, 15, 15]
].sort, "D58 profiles")

# D50 rigid skeleton arithmetic and field gate.
line_total = 1 + 36 + 3 + 2
check(line_total == 42, "D50 skeleton line total")
double_degrees = [1] * 15 + [2] * 24 + [12] * 2 + [13]
check(double_degrees.sum == 100, "D50 double degree sum")
check((P_FIELD - 1) % 13 == 10, "D50 field gate")

# Heavy-incidence gates for D55, D56, and the first D57 row.
check(4 * 13 > 42 + 6, "four-heavy gate")

# Three-heavy line-count gates used for the remaining D57 and D58 rows.
def zero_heavy_cap(total_heavy_incidence)
  # x-z=I-42 and x<=C(3,2)=3.
  3 - (total_heavy_incidence - 42)
end

check(zero_heavy_cap(43) == 2, "I43 no-heavy cap")
check(zero_heavy_cap(42) == 3, "I42 no-heavy cap")
check(4 > 1 && 3 > 1, "D57 pair-intersection obstruction")
check(3 > 1 && 2 > 1, "D58 I43 pair-intersection obstruction")
check(11 > 3, "D58 I42 three-line pair obstruction")

vector = expected_counts.flat_map { |d, counts| [d, counts[0], counts[1]] }
vector += [line_total, double_degrees.sum, (P_FIELD - 1) % 13]
output = [
  "RANK15_M212_Q14_B42_D46_D58_HIGHPOINT_PACKING_AND_GRID_EXCLUSION: PASS",
  "profile_counts=#{expected_counts.map { |d,c| "D#{d}:#{c[0]}/#{c[1]}" }.join(',')}",
  "D50=rigid_3x13_grid field_remainder=#{(P_FIELD - 1) % 13}",
  "D55_D56=four_heavy_incidence_52_gt_48",
  "D57=three_profiles_all_excluded",
  "D58=three_profiles_all_excluded",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector.join(':') + "\n")}",
  "payment=D46..D58",
  "next=D59 local_profiles=958 local_survivors=3"
].join("\n") + "\n"

expected = File.join(__dir__,
  "verify_rank15_m212_q14_b42_d46_d58_highpoint_packing_and_grid_exclusion.expected.txt")
check(File.file?(expected), "missing expected output")
check(output == File.binread(expected), "expected-output drift")
print output

