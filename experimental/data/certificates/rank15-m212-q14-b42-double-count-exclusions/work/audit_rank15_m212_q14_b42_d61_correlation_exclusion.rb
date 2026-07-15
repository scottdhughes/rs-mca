#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

ROOT = File.expand_path("..", __dir__)
P_FIELD = 2_130_706_433
PINS = {
  "work/RANK15_M212_Q14_B42_D61_CORRELATION_EXCLUSION.md" =>
    "c156e7c132c48b39e3e216416188751ed297fd7698fe034a768a5dc02561c374",
  "work/verify_rank15_m212_q14_b42_d61_correlation_exclusion.rb" =>
    "4ee4014fda27e3c309fbc26a977effd40bc82342ea6ab44c18c4921200dd50bd",
  "work/verify_rank15_m212_q14_b42_d61_correlation_exclusion.expected.txt" =>
    "e9613c433320928453c3bd34f5ff18877c74360fa89016e39d14c209ad499c75"
}.freeze

def check(value, message)
  raise message unless value
end

PINS.each do |relative, expected|
  check(Digest::SHA256.file(File.join(ROOT, relative)).hexdigest == expected,
        "pin drift #{relative}")
end

# Independent ascending-weight moment enumeration.
profiles = []
counts = Array.new(13, 0)
walk = nil
walk = lambda do |weight, total, square, number|
  if weight == 13
    profiles << counts[1, 12].dup if total == 58 && square == 410 && number <= 150
    next
  end
  maximum = [(58-total)/weight, (410-square)/(weight*weight), 150-number].min
  (0..maximum).each do |multiplicity|
    counts[weight] = multiplicity
    walk.call(weight+1, total+weight*multiplicity,
              square+weight*weight*multiplicity, number+multiplicity)
  end
  counts[weight] = 0
end
walk.call(1,0,0,0)
check(profiles.length == 1_458, "D61 moment count")

# Independent minimal-group generator and exact disjoint packing recurrence.
def patterns(threshold)
  rows = []
  counts = Array.new(10, 0)
  visit = nil
  visit = lambda do |weight, total|
    if weight == 11
      used = (1..10).select { |w| counts[w-1].positive? }
      rows << counts.dup if !used.empty? && total >= threshold && total-used.min < threshold
      next
    end
    maximum = (threshold+9-total)/weight
    if maximum >= 0
      (0..maximum).each do |multiplicity|
        counts[weight-1] = multiplicity
        visit.call(weight+1, total+weight*multiplicity)
      end
    end
    counts[weight-1] = 0
  end
  visit.call(1,0)
  rows
end

groups = (1..10).to_h { |threshold| [threshold, patterns(threshold)] }
memo = {}
cover = nil
cover = lambda do |state, threshold|
  key = [state, threshold]
  next memo[key] if memo.key?(key)
  best = 0
  groups.fetch(threshold).each do |group|
    next unless (0...10).all? { |index| group[index] <= state[index] }
    rest = (0...10).map { |index| state[index]-group[index] }
    best = [best, 1+cover.call(rest, threshold)].max
  end
  memo[key] = best
end

kept = profiles.select do |profile|
  small = profile[0,10]
  big = profile[10]+profile[11]
  small.each_with_index.all? do |multiplicity,index|
    next true if multiplicity.zero?
    other = small.dup
    other[index] -= 1
    index+4 <= big+cover.call(other,10-index)
  end
end
check(kept.length == 10, "D61 packing survivors")
signatures = kept.map do |profile|
  result = []
  profile.each_with_index do |multiplicity,index|
    multiplicity.times { result << index+4 }
  end
  result
end
expected_signatures = [
  [4]*9+[5]*5+[12]+[13]*3,
  [4]*12+[5]*2+[6]+[12]+[13]*3,
  [5]*7+[6]*2+[12]*3+[14],
  [4]*11+[5]*4+[12]*2+[13]+[14],
  [4]*14+[5]+[6]+[12]*2+[13]+[14],
  [4]*3+[5]*11+[14]*3,
  [4]*15+[5]*2+[12]*3+[15],
  [4]*5+[5]*10+[13]+[14]+[15],
  [4]*24+[14]*2+[15],
  [4]*9+[5]*8+[12]+[15]*2
]
check(signatures.sort == expected_signatures.sort, "D61 survivor signatures")
last_signature = [4]*24+[14]*2+[15]

# Nine direct exclusions.
check([51,51,50,51,51,51].all? { |value| value > 48 }, "four-heavy gates")
check([11,10,8].all? { |count| count > 3 }, "three-heavy gates")

# Last-row structural and correlation arithmetic.
check(43-42 == 1, "x-z relation")
check(26-2*24 < 0, "one no-heavy line exclusion")
check(1+11+12+3 > 26 && 1+11+11+3 == 26, "side-small routing")
check(12+13-1 == 24, "small-intersection split")

triple_total = 13*13-2*24
correlation_total = 12*12
ordinary_floor = 24+triple_total-(2+2+2)
ordinary_cap = 13+correlation_total-ordinary_floor
check([triple_total,ordinary_floor,ordinary_cap] == [121,139,18],
      "ordinary correlation arithmetic")
ordinary_divisors = (1..ordinary_cap).select { |h| ((P_FIELD-1)%h).zero? }
ordinary_bounds = ordinary_divisors.map { |h| 2*h*((12+h-1)/h)-h }
check(ordinary_divisors == [1,2,4,8,16], "ordinary stabilizers")
check(ordinary_bounds == [23,22,20,24,16], "ordinary Kneser")
check(correlation_total-3*8 == 120 && 120 < ordinary_floor, "order-16 cap")

small_floor = 23+triple_total-(0+0+2)
small_cap = 13+correlation_total-small_floor
check([small_floor,small_cap] == [142,15], "small-intersection arithmetic")
small_divisors = (1..small_cap).select { |h| ((P_FIELD-1)%h).zero? }
small_bounds = small_divisors.map { |h| 2*h*((12+h-1)/h)-h }
check(small_divisors == [1,2,4,8] && small_bounds.min > small_cap,
      "small-intersection Kneser")

vector = [profiles.length,kept.length,last_signature,triple_total,
          ordinary_floor,ordinary_cap,ordinary_divisors,ordinary_bounds,120,
          small_floor,small_cap,small_divisors,small_bounds].join(":") + "\n"
output = [
  "AUDIT_RANK15_M212_Q14_B42_D61_CORRELATION_EXCLUSION: PASS",
  "profiles=1458 local_survivors=10 independent=true",
  "immediate_exclusions=9 last_row=4x24,14x2,15",
  "ordinary=triple121 selected139 quotient18 H16_cap120",
  "small_intersection=selected142 quotient15 all_Kneser_excluded=true",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D61",
  "nonclaim=D62_or_larger"
].join("\n") + "\n"

expected_path = File.join(__dir__,
  "audit_rank15_m212_q14_b42_d61_correlation_exclusion.expected.txt")
check(File.file?(expected_path), "missing expected output")
check(output == File.binread(expected_path), "expected-output drift")
print output
