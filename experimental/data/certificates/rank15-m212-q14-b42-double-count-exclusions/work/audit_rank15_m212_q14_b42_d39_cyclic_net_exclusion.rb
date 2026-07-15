#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent hostile replay.  This file does not load the claimant verifier.

require "digest"

ROOT = File.expand_path("..", __dir__)
P_FIELD = 2_130_706_433

PINS = {
  "source/grand_list/main/experimental/notes/thresholds/rank15_locator_saturation_normal_form.md" =>
    "48d72c94743f5a9c900b35197279a69bf00a8a133c7b27bf3ff39004b1257085",
  "work/RANK15_M214_B149_SOURCE_TRANSPORT.md" =>
    "2f6cbc1c51b4200651df8fe4f4f7aece61cd4334f914f721a2052ee7557a8d68",
  "work/RANK15_POSCHAR_BOUNDARY_EXTACTIC_EXCLUSION.md" =>
    "1c5a2840aac0bfe4426b50ef10d6abde8a09724a7982967208214f2b695101c6",
  "work/ROOT_HOSTILE_AUDIT_RANK15_POSCHAR_BOUNDARY_EXTACTIC.md" =>
    "9b05e27b384fcdad254d50550c6840f62329ac9799157c4edd37b93e907e26b3",
  "work/RANK15_M212_Q14_B42_D39_CYCLIC_NET_EXCLUSION.md" =>
    "a3fd6920a42ea6da3efc45ef7376ddc103318547190545fc82ab63ca8b73ae37"
}.freeze

def check(value, message)
  raise message unless value
end

PINS.each do |relative, expected|
  path = File.join(ROOT, relative)
  check(File.file?(path), "missing pin #{relative}")
  actual = Digest::SHA256.file(path).hexdigest
  check(actual == expected, "hash drift #{relative}: #{actual}")
end

# Reconstruct the moment row by an implementation distinct from the claimant's
# descending recursive partition search.
solutions = []
counts = Array.new(14, 0)
walk = nil
walk = lambda do |x, count_left, sum_left, square_left|
  if x.zero?
    if count_left.zero? && sum_left.zero? && square_left.zero?
      solutions << counts.dup
    end
    return
  end
  maximum = [count_left, sum_left / x, square_left / (x * x)].min
  (0..maximum).each do |multiplicity|
    c = count_left - multiplicity
    s = sum_left - multiplicity * x
    q = square_left - multiplicity * x * x
    next if s < c || q < c
    next if x > 1 && (s > c * (x - 1) || q > c * (x - 1) * (x - 1))
    counts[x] = multiplicity
    walk.call(x - 1, c, s, q)
  end
  counts[x] = 0
end
walk.call(13, 172, 208, 676)

check(solutions.length == 1, "nonunique D39 partition")
row = solutions.fetch(0)
check(row[1] == 169 && row[13] == 3 && row.sum == 172,
      "wrong D39 partition")

types = []
(0..15).each do |d|
  (0..15).each do |t|
    (0..15).each do |h|
      types << [d, t, h] if d + t + h == 15 &&
                              d + 2 * t + 14 * h == 41
    end
  end
end
check(types.sort == [[1, 13, 1], [13, 0, 2]], "line-type drift")

leaf_count = 39
center_count = 3
check(leaf_count + center_count == 42, "line count")
check(leaf_count * 1 + center_count * 13 == 78, "double degree sum")
check(leaf_count * 1 + center_count * 2 == 45, "high incidence sum")

# Isolated K2: (1-14)^2 must be one for reciprocal residues.
k2_gap = (1 - 14)**2 - 1
check(k2_gap == 168 && (k2_gap % P_FIELD) != 0, "K2 gate vanished")
field_remainder = (P_FIELD - 1) % 13
check(field_remainder == 10, "field remainder drift")

vector = [211, 630, 861, 39, row[1], row[13], leaf_count,
          center_count, k2_gap, field_remainder].join(":") + "\n"
output = [
  "AUDIT_RANK15_M212_Q14_B42_D39_CYCLIC_NET_EXCLUSION: PASS",
  "source_transport=literal_Fp_parameter_points_dual_to_individually_Fp_lines",
  "residual_scope=row1_unique_residual_double;row2_no_residual_points",
  "moments=n2:39,n3:169,n15:3 unique=true",
  "line_types=39_leaves_(1,13,1);3_centers_(13,0,2)",
  "double_graph=three_K1,13_stars K2_gap=#{k2_gap}",
  "net=Fp_rational_(3,13) forces_13_divides_p_minus_1",
  "field_gate=(p-1)_mod_13=#{field_remainder}",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D39_only",
  "nonclaim=D44_or_larger"
].join("\n") + "\n"

expected = File.join(__dir__,
  "audit_rank15_m212_q14_b42_d39_cyclic_net_exclusion.expected.txt")
check(File.file?(expected), "missing expected output")
check(output == File.binread(expected), "expected-output drift")
print output
