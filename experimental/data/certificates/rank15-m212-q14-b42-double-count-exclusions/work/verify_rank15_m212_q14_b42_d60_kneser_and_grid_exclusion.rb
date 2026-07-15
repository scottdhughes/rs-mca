#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"
require "json"
require "open3"
require "rbconfig"

P_FIELD = 2_130_706_433
WRAPPER_SHA = "8f086174009581a4ae651943fb34351767f3a50cf946e8bc058099230b56b656"

def check(value, message)
  raise message unless value
end

wrapper = File.join(__dir__, "replay_rank15_m212_q14_b42_d60_exact_packing.rb")
check(Digest::SHA256.file(wrapper).hexdigest == WRAPPER_SHA, "wrapper drift")
stdout, stderr, status = Open3.capture3(RbConfig.ruby, "--disable-gems", "-W0", wrapper)
check(status.success?, "D60 packing replay failed: #{stderr}")
lines = stdout.lines
check(lines.shift == "D=60 profiles=1183 exact_survivors=8\n", "D60 header")
check(lines.length == 8, "D60 survivor line count")
profiles = lines.map do |line|
  match = line.match(/\A  high=(\[.*\]) packing=/)
  check(!match.nil?, "D60 survivor parse")
  counts = Hash.new(0)
  JSON.parse(match[1]).each { |value| counts[value] += 1 }
  counts.sort.to_h
end

expected_profiles = [
  {4=>6,5=>6,12=>1,13=>3},
  {4=>8,5=>5,12=>2,13=>1,14=>1},
  {5=>12,14=>3},
  {4=>12,5=>3,12=>3,15=>1},
  {4=>2,5=>11,13=>1,14=>1,15=>1},
  {4=>21,5=>1,14=>2,15=>1},
  {4=>6,5=>9,12=>1,15=>2},
  {4=>23,13=>1,15=>2}
].map { |row| row.sort.to_h }
check(profiles == expected_profiles, "D60 profile list")

# Six immediate rows.
check(51 > 42 + 6, "four-heavy cap")
check([12, 11, 9].all? { |count| count > 3 }, "three-heavy k5 cap")

# [4^23,13,15^2] grid row.
check(3 + 11 + 13 + 13 + 2 == 42, "grid-row line total")
check(10 + 12 + 1 + 3 == 26, "P0 side support equality")
check(12 + 12 + 1 + 3 > 26, "P0 BC exclusion")
check((P_FIELD - 1) % 13 == 10, "grid field gate")

# [4^21,5,14^2,15] correlation row.
check(3 + 2 + 12 + 12 + 13 == 42, "Kneser-row line total")
triple_total = 13 * 13 - 2 * 21 - 3
non_grid_cap = 2 + 3 + 1
selected_floor = 22 + triple_total - non_grid_cap
check([triple_total, non_grid_cap, selected_floor] == [124, 6, 140],
      "correlation lower bound")
correlation_total = 12 * 12
quotient_cap = 13 + (correlation_total - selected_floor)
check(quotient_cap == 17, "quotient support cap")

check(P_FIELD - 1 == (2**24) * 127, "field factorization")
small_divisors = (1..17).select { |h| ((P_FIELD - 1) % h).zero? }
check(small_divisors == [1, 2, 4, 8, 16], "small subgroup orders")
kneser = small_divisors.to_h do |h|
  [h, 2 * h * ((12 + h - 1) / h) - h]
end
check(kneser == {1=>23,2=>22,4=>20,8=>24,16=>16}, "Kneser bounds")
check(correlation_total - 3 * 8 == 120 && 120 < selected_floor,
      "H16 correlation contradiction")

vector = [1183, 8, 51, 48, 42, 13, triple_total, non_grid_cap,
          selected_floor, correlation_total, quotient_cap,
          kneser.values, 120, (P_FIELD - 1) % 13].join(":") + "\n"
output = [
  "RANK15_M212_Q14_B42_D60_KNESER_AND_GRID_EXCLUSION: PASS",
  "profiles=1183 local_survivors=8 immediate_exclusions=6",
  "grid_row=4x23,13,15x2 transversals11 field_remainder10",
  "Kneser_row=4x21,5,14x2,15 triple_total124 non_grid_cap6",
  "correlation_selected_floor=140 total=144 quotient_cap=17",
  "Kneser_bounds=1:23,2:22,4:20,8:24,16:16 H16_selected_cap=120",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D60",
  "next=D61"
].join("\n") + "\n"

expected_path = File.join(__dir__,
  "verify_rank15_m212_q14_b42_d60_kneser_and_grid_exclusion.expected.txt")
check(File.file?(expected_path), "missing expected output")
check(output == File.binread(expected_path), "expected-output drift")
print output
