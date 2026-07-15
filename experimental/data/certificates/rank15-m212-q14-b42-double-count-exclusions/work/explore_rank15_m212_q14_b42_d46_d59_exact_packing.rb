#!/usr/bin/env ruby
# frozen_string_literal: true

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
      visit.call(weight - 1,
                 total + multiplicity * weight,
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
MEMO = {}

def maximum_groups(counts, threshold)
  key = [threshold, counts]
  cached = MEMO[key]
  return cached unless cached.nil?

  best = 0
  PATTERNS.fetch(threshold).each do |pattern|
    next unless (0...10).all? { |index| pattern[index] <= counts[index] }
    remainder = (0...10).map { |index| counts[index] - pattern[index] }
    best = [best, 1 + maximum_groups(remainder, threshold)].max
  end
  MEMO[key] = best
end

def survives_exact_packing(profile)
  small = profile[0, 10]
  big_count = profile[10] + profile[11]
  witnesses = []
  small.each_with_index do |multiplicity, index|
    next if multiplicity.zero?
    weight = index + 1
    other = small.dup
    other[index] -= 1
    groups = maximum_groups(other, 11 - weight)
    line_cap = big_count + groups
    witnesses << [weight + 3, line_cap, groups]
    return [false, witnesses] if weight + 3 > line_cap
  end
  [true, witnesses]
end

def rendered_high(profile)
  result = []
  profile.each_with_index do |multiplicity, index|
    multiplicity.times { result << index + 4 }
  end
  result
end

(46..59).each do |double_count|
  profiles = high_profiles(double_count)
  survivors = []
  profiles.each do |profile|
    survives, witness = survives_exact_packing(profile)
    survivors << [rendered_high(profile), witness] if survives
  end
  puts "D=#{double_count} profiles=#{profiles.length} exact_survivors=#{survivors.length}"
  survivors.each { |high, witness| puts "  high=#{high.inspect} packing=#{witness.inspect}" }
end
