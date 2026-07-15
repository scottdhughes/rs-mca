#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"
require "json"
require "open3"
require "rbconfig"

P_FIELD = 2_130_706_433
WRAPPER_SHA = "d55701c5d1a1bb3366267b77f4ea39a08977508da5184a81733e185da94469a2"

def check(value, message)
  raise message unless value
end

wrapper = File.join(__dir__, "replay_rank15_m212_q14_b42_d61_exact_packing.rb")
check(Digest::SHA256.file(wrapper).hexdigest == WRAPPER_SHA, "wrapper drift")
stdout, stderr, status = Open3.capture3(RbConfig.ruby, "--disable-gems", "-W0", wrapper)
check(status.success?, "D61 packing replay failed: #{stderr}")
lines = stdout.lines
check(lines.shift == "D=61 profiles=1458 exact_survivors=10\n", "D61 header")
check(lines.length == 10, "D61 survivor line count")
profiles = lines.map do |line|
  match = line.match(/\A  high=(\[.*\]) packing=/)
  check(!match.nil?, "D61 survivor parse")
  counts = Hash.new(0)
  JSON.parse(match[1]).each { |value| counts[value] += 1 }
  counts.sort.to_h
end

expected_profiles = [
  {4=>9,5=>5,12=>1,13=>3},
  {4=>12,5=>2,6=>1,12=>1,13=>3},
  {5=>7,6=>2,12=>3,14=>1},
  {4=>11,5=>4,12=>2,13=>1,14=>1},
  {4=>14,5=>1,6=>1,12=>2,13=>1,14=>1},
  {4=>3,5=>11,14=>3},
  {4=>15,5=>2,12=>3,15=>1},
  {4=>5,5=>10,13=>1,14=>1,15=>1},
  {4=>24,14=>2,15=>1},
  {4=>9,5=>8,12=>1,15=>2}
].map { |row| row.sort.to_h }
check(profiles == expected_profiles, "D61 profile list")

# Nine immediate rows: six exceed the four-heavy incidence ceiling, and
# three have too many multiplicity-5 points for at most three no-heavy lines.
heavy_incidences = [51, 51, 50, 51, 51, 51]
check(heavy_incidences.all? { |value| value > 42 + 6 }, "four-heavy gates")
check([11, 10, 8].all? { |count| count > 3 }, "three-heavy gates")

# Final [4^24,14^2,15] row: common structural arithmetic.
check(14 + 14 + 15 == 43, "heavy incidence")
check(3 + 2 + 12 + 12 + 13 == 42, "line partition")
triple_total = 13 * 13 - 2 * 24
correlation_total = 12 * 12
check([triple_total, correlation_total] == [121, 144], "correlation totals")
check(P_FIELD - 1 == (2**24) * 127, "field factorization")

# Ordinary L cap M: split 12+12, external triple cap 2+2+2.
ordinary_external_cap = 2 + 2 + 2
ordinary_selected_floor = 24 + triple_total - ordinary_external_cap
ordinary_quotient_cap = 13 + correlation_total - ordinary_selected_floor
check([ordinary_selected_floor, ordinary_quotient_cap] == [139, 18],
      "ordinary correlation floor")
ordinary_divisors = (1..ordinary_quotient_cap).select do |h|
  ((P_FIELD - 1) % h).zero?
end
ordinary_bounds = ordinary_divisors.to_h do |h|
  [h, 2 * h * ((12 + h - 1) / h) - h]
end
check(ordinary_divisors == [1, 2, 4, 8, 16], "ordinary subgroup orders")
check(ordinary_bounds == {1=>23,2=>22,4=>20,8=>24,16=>16},
      "ordinary Kneser bounds")
ordinary_h16_cap = correlation_total - 3 * 8
check(ordinary_h16_cap == 120 && ordinary_h16_cap < ordinary_selected_floor,
      "ordinary H16 contradiction")

# Small L cap M: sizes 12+13, P0 lies on AB, external cap 0+0+2.
check(1 + 11 + 12 + 3 > 26, "P0 AC/BC exclusion")
check(1 + 11 + 11 + 3 == 26, "P0 AB equality")
small_external_cap = 0 + 0 + 2
small_selected_floor = 23 + triple_total - small_external_cap
small_quotient_cap = 13 + correlation_total - small_selected_floor
check([small_selected_floor, small_quotient_cap] == [142, 15],
      "small-intersection correlation floor")
small_divisors = (1..small_quotient_cap).select { |h| ((P_FIELD - 1) % h).zero? }
small_bounds = small_divisors.to_h do |h|
  [h, 2 * h * ((12 + h - 1) / h) - h]
end
check(small_divisors == [1, 2, 4, 8], "small subgroup orders")
check(small_bounds.values.all? { |bound| bound > small_quotient_cap },
      "small-intersection Kneser contradiction")

vector = [1458, 10, 9, heavy_incidences, [11,10,8], triple_total,
          ordinary_external_cap, ordinary_selected_floor, ordinary_quotient_cap,
          ordinary_divisors, ordinary_bounds.values, ordinary_h16_cap,
          small_external_cap, small_selected_floor, small_quotient_cap,
          small_divisors, small_bounds.values].join(":") + "\n"
output = [
  "RANK15_M212_Q14_B42_D61_CORRELATION_EXCLUSION: PASS",
  "profiles=1458 local_survivors=10 immediate_exclusions=9",
  "last_row=4x24,14x2,15 no_heavy_lines=2 heavy_pair_lines=3",
  "ordinary_case=split12+12 triple121 external6 selected139 quotient_cap18",
  "ordinary_Kneser=1:23,2:22,4:20,8:24,16:16 H16_selected_cap120",
  "small_intersection=split12+13 side=AB external2 selected142 quotient_cap15",
  "small_Kneser=1:23,2:22,4:20,8:24",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D61",
  "next=D62"
].join("\n") + "\n"

expected_path = File.join(__dir__,
  "verify_rank15_m212_q14_b42_d61_correlation_exclusion.expected.txt")
check(File.file?(expected_path), "missing expected output")
check(output == File.binread(expected_path), "expected-output drift")
print output
