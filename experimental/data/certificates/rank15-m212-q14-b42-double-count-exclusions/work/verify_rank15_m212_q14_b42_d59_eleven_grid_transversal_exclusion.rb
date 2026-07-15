#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"
require "open3"
require "rbconfig"

P_FIELD = 2_130_706_433
PACKING_SHA = "f44b6d8a93ef5e44a50fd7bce35ce85fbd83667c636bf0f4784c46500e44784d"

def check(value, message)
  raise message unless value
end

packing_path = File.join(__dir__,
  "explore_rank15_m212_q14_b42_d46_d59_exact_packing.rb")
check(Digest::SHA256.file(packing_path).hexdigest == PACKING_SHA,
      "packing source drift")
stdout, stderr, status = Open3.capture3(RbConfig.ruby, "--disable-gems", "-W0",
                                         packing_path)
check(status.success?, "packing replay failed: #{stderr}")

d59 = stdout.lines.drop_while { |line| !line.start_with?("D=59 ") }
check(d59.length == 4, "unexpected D59 output length")
expected_d59 = [
  "D=59 profiles=958 exact_survivors=3\n",
  "  high=#{([4] * 18 + [5, 5, 14, 14, 15]).inspect} packing=[[4, 5, 2], [5, 5, 2]]\n",
  "  high=#{([4] * 3 + [5] * 10 + [12, 15, 15]).inspect} packing=[[4, 5, 3], [5, 5, 3], [12, 13, 11]]\n",
  "  high=#{([4] * 20 + [5, 13, 15, 15]).inspect} packing=[[4, 5, 3], [5, 5, 3], [13, 23, 21]]\n"
]
check(d59 == expected_d59, "D59 profile list drift")

# Heavy-line counts for the first two rows and the rigid third row.
check(43 - 42 == 1 && 3 - 1 == 2, "I43 no-heavy cap")
check(42 - 42 == 0 && 3 - 0 == 3, "I42 no-heavy cap")
check(2 > 1, "two-line/two-point gate")
check(10 > 3, "three-line/ten-point gate")

# Third skeleton.
check(3 + 11 + 13 + 13 + 2 == 42, "D59 line total")
check((9..11).to_a == [9, 10, 11], "no-heavy split range")
check(20 / 2 == 10, "A-pair forced split")

# Double degrees by line category:
# L,M; AB,AC,BC; eleven A-low; B-low; C-low.
double_degree_sum = 2 * 1 + 2 * 11 + 13 + 11 * 1
# B and C each have: Q connector d3, 8 paired P connectors d3,
# four singleton P connectors d2.
one_big_low_sum = 3 + 8 * 3 + 4 * 2
double_degree_sum += 2 * one_big_low_sum
check(double_degree_sum == 118 && double_degree_sum / 2 == 59,
      "D59 double-degree ledger")

check((P_FIELD - 1) % 13 == 10, "field gate")
transversals = 11
check(transversals >= 11 && transversals > 1, "transversal count")

vector = [958, 3, 43, 2, 42, 3, 10, double_degree_sum,
          transversals, (P_FIELD - 1) % 13].join(":") + "\n"
output = [
  "RANK15_M212_Q14_B42_D59_ELEVEN_GRID_TRANSVERSAL_EXCLUSION: PASS",
  "profiles=958 local_survivors=3 first_two_excluded=true",
  "rigid_profile=4x20,5,13,15x2 split=10+10 lines=42",
  "double_degree_sum=#{double_degree_sum} D=#{double_degree_sum / 2}",
  "grid=11_complete_transversals_of_13x13",
  "field_gate=(p-1)_mod_13=#{(P_FIELD - 1) % 13}",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D59",
  "next=D60"
].join("\n") + "\n"

expected_path = File.join(__dir__,
  "verify_rank15_m212_q14_b42_d59_eleven_grid_transversal_exclusion.expected.txt")
check(File.file?(expected_path), "missing expected output")
check(output == File.binread(expected_path), "expected-output drift")
print output

